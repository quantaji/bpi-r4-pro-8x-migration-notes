#!/usr/bin/env python3
"""Generate Project Phase 1a feature-routing seed output from a diffset."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONFIDENCE_RANK = {"low": 1, "medium": 2, "high": 3}
EVIDENCE_RANK = {
    "path": 1,
    "path+status": 2,
    "path+file-kind": 3,
    "path+keywords": 4,
    "patch-subject": 5,
    "patch-inner-target": 6,
    "patch-content-keyword": 7,
    "binary-path": 8,
    "manual-review": 9
}


@dataclass
class WorkItem:
    file_id: str
    status: str
    old_path: str | None
    new_path: str | None
    effective_path: str
    file_kind: str
    is_binary: bool
    numstat_added: int | None
    numstat_deleted: int | None
    patch_path: Path | None
    patch_text: str
    patch_subjects: list[str]
    patch_targets: list[str]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    data = path.read_bytes()
    if limit is not None:
        data = data[:limit]
    return data.decode("utf-8", errors="replace")


def parse_name_status(path: Path) -> list[tuple[str, str | None, str | None, str]]:
    rows: list[tuple[str, str | None, str | None, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split("\t")
        status = parts[0]
        if status.startswith(("R", "C")):
            if len(parts) < 3:
                raise ValueError(f"bad rename/copy line in {path}: {raw}")
            old_path = parts[1]
            new_path = parts[2]
            effective_path = new_path
        else:
            if len(parts) < 2:
                raise ValueError(f"bad name-status line in {path}: {raw}")
            old_path = parts[1] if status == "D" else None
            new_path = None if status == "D" else parts[1]
            effective_path = parts[1]
        rows.append((status, old_path, new_path, effective_path))
    return rows


def simplify_numstat_path(raw_path: str) -> list[str]:
    paths = [raw_path]
    if " => " in raw_path:
        # Git may write paths such as a/{old => new}/file. Keep the raw path and
        # a best-effort right-side approximation for lookup.
        paths.append(raw_path.replace("{", "").replace("}", "").split(" => ")[-1])
    return paths


def parse_numstat(path: Path) -> dict[str, tuple[int | None, int | None]]:
    out: dict[str, tuple[int | None, int | None]] = {}
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip():
            continue
        parts = raw.split("\t")
        if len(parts) < 3:
            continue
        added_raw, deleted_raw, file_path = parts[0], parts[1], parts[2]
        added = None if added_raw == "-" else int(added_raw)
        deleted = None if deleted_raw == "-" else int(deleted_raw)
        for key in simplify_numstat_path(file_path):
            out[key] = (added, deleted)
    return out


def classify_file_kind(path: str) -> str:
    name = Path(path).name
    suffix = Path(path).suffix.lower()
    if name in {".config", ".config.old"}:
        return "config"
    if name == "Makefile":
        return "makefile"
    if name == "Kconfig":
        return "kconfig"
    if suffix == ".patch":
        return "patch"
    if suffix == ".dts":
        return "dts"
    if suffix == ".dtsi":
        return "dtsi"
    if suffix == ".dtso":
        return "dtso"
    if suffix in {".c", ".cc", ".cpp"}:
        return "source"
    if suffix == ".h":
        return "header"
    if suffix in {".sh", ".bash"}:
        return "shell"
    if suffix in {".uc", ".lua", ".py", ".pl"}:
        return "script"
    if suffix in {".bin", ".cld", ".fw", ".ucode", ".elf"}:
        return "firmware"
    if suffix in {".md", ".txt"}:
        return "doc"
    if suffix in {".json", ".yml", ".yaml"}:
        return "metadata"
    return "unknown"


def per_file_patch_path(diffset: Path, effective_path: str) -> Path:
    return diffset / "files" / f"{effective_path}.patch"


def strip_outer_prefix(line: str) -> str:
    if not line:
        return line
    if line[0] in {"+", "-", " "}:
        return line[1:]
    return line


def extract_patch_subjects_and_targets(
    patch_text: str,
    old_path: str | None,
    new_path: str | None,
    effective_path: str
) -> tuple[list[str], list[str]]:
    subjects: list[str] = []
    targets: list[str] = []
    changed_paths = {p for p in [old_path, new_path, effective_path] if p}

    for raw_line in patch_text.splitlines():
        line = strip_outer_prefix(raw_line).strip()
        if line.startswith("Subject:"):
            subject = line[len("Subject:"):].strip()
            if subject and subject not in subjects:
                subjects.append(subject)

        diff_match = re.match(r"diff --git a/(.+?) b/(.+)$", line)
        if diff_match:
            for target in diff_match.groups():
                if target not in changed_paths and target not in targets:
                    targets.append(target)
            continue

        path_match = re.match(r"(?:---|\+\+\+) ([ab])/(.+)$", line)
        if path_match:
            target = path_match.group(2)
            if target not in changed_paths and target not in targets:
                targets.append(target)

    return subjects, targets


def build_work_items(diffset: Path) -> list[WorkItem]:
    name_status_path = diffset / "name-status.tsv"
    if not name_status_path.exists():
        raise FileNotFoundError(f"missing {name_status_path}")

    numstat = parse_numstat(diffset / "numstat.tsv")
    binary_files = set()
    binary_path = diffset / "binary-files.txt"
    if binary_path.exists():
        binary_files = {
            line.strip()
            for line in binary_path.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip()
        }

    items: list[WorkItem] = []
    for index, (status, old_path, new_path, effective_path) in enumerate(parse_name_status(name_status_path), 1):
        patch_path = per_file_patch_path(diffset, effective_path)
        patch_text = read_text(patch_path, limit=700_000)
        subjects, targets = extract_patch_subjects_and_targets(patch_text, old_path, new_path, effective_path)
        added, deleted = numstat.get(effective_path, (None, None))
        items.append(
            WorkItem(
                file_id=f"{index:06d}",
                status=status,
                old_path=old_path,
                new_path=new_path,
                effective_path=effective_path,
                file_kind=classify_file_kind(effective_path),
                is_binary=effective_path in binary_files,
                numstat_added=added,
                numstat_deleted=deleted,
                patch_path=patch_path if patch_path.exists() else None,
                patch_text=patch_text,
                patch_subjects=subjects,
                patch_targets=targets,
            )
        )
    return items


def matches_glob(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def combined_text(item: WorkItem) -> str:
    parts = [
        item.effective_path,
        item.old_path or "",
        item.new_path or "",
        item.file_kind,
        "\n".join(item.patch_subjects),
        "\n".join(item.patch_targets),
        item.patch_text[:300_000],
    ]
    return "\n".join(parts)


def scoped_text(item: WorkItem, scopes: list[str]) -> str:
    parts: list[str] = []
    for scope in scopes:
        if scope == "path":
            parts.extend([item.effective_path, item.old_path or "", item.new_path or "", item.file_kind])
        elif scope in {"patch_subjects", "subjects"}:
            parts.append("\n".join(item.patch_subjects))
        elif scope in {"patch_targets", "targets"}:
            parts.append("\n".join(item.patch_targets))
        elif scope in {"patch_content", "content"}:
            parts.append(item.patch_text[:300_000])
        elif scope == "combined":
            parts.append(combined_text(item))
        else:
            raise ValueError(f"unknown text_scope value: {scope}")
    return "\n".join(parts)


def rule_matches(rule: dict[str, Any], item: WorkItem) -> bool:
    match = rule.get("match", {})
    path = item.effective_path

    prefixes = match.get("status_prefixes")
    if prefixes and not any(item.status.startswith(prefix) for prefix in prefixes):
        return False

    file_kinds = match.get("file_kinds")
    if file_kinds and item.file_kind not in set(file_kinds):
        return False

    binary = match.get("binary")
    if binary is not None and bool(binary) != item.is_binary:
        return False

    path_globs = match.get("path_globs")
    if path_globs and not matches_glob(path, path_globs):
        return False

    path_regex = match.get("path_regex")
    if path_regex and not re.search(path_regex, path):
        return False

    text_regex = match.get("text_regex")
    if text_regex:
        scopes = match.get("text_scope")
        text = scoped_text(item, scopes) if scopes else combined_text(item)
        if not re.search(text_regex, text):
            return False

    return True


def better_confidence(a: str, b: str) -> str:
    return a if CONFIDENCE_RANK[a] >= CONFIDENCE_RANK[b] else b


def better_evidence(a: str, b: str) -> str:
    return a if EVIDENCE_RANK[a] >= EVIDENCE_RANK[b] else b


def make_evidence(rule: dict[str, Any], item: WorkItem) -> list[str]:
    evidence = [f"rule:{rule['id']}"]
    evidence.append(f"status:{item.status}")
    evidence.append(f"path:{item.effective_path}")
    if item.patch_subjects:
        evidence.append("subjects:" + " | ".join(item.patch_subjects[:3]))
    if item.patch_targets:
        evidence.append("inner_targets:" + " | ".join(item.patch_targets[:5]))
    if item.is_binary:
        evidence.append("binary-file:true")
    text_scope = rule.get("match", {}).get("text_scope")
    if text_scope:
        evidence.append("text_scope:" + ",".join(text_scope))
    return evidence


def seed_assignments(
    items: list[WorkItem],
    seed_rules: dict[str, Any],
    allowed_tags: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    assignments_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    candidate_rows: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []

    for item in items:
        item_review_reasons: list[str] = []
        for rule in seed_rules["rules"]:
            if not rule_matches(rule, item):
                continue

            tags = rule.get("tags", [])
            if not tags:
                if rule.get("needs_review"):
                    item_review_reasons.append(rule.get("review_reason", f"matched {rule['id']}"))
                continue

            invalid = [tag for tag in tags if tag not in allowed_tags]
            if invalid:
                rejected_rows.append(
                    {
                        "record_type": "rejected-candidate",
                        "file_id": item.file_id,
                        "path": item.effective_path,
                        "rule_id": rule["id"],
                        "invalid_tags": invalid,
                        "reason": "feature tag is not in feature-tags-v1.json"
                    }
                )
                continue

            for tag in tags:
                evidence = make_evidence(rule, item)
                candidate = {
                    "record_type": "candidate",
                    "file_id": item.file_id,
                    "path": item.effective_path,
                    "feature": tag,
                    "role": rule.get("role", "secondary"),
                    "confidence": rule.get("confidence", "low"),
                    "evidence_level": rule.get("evidence_level", "path"),
                    "evidence": evidence,
                    "rule_id": rule["id"],
                    "needs_review": bool(rule.get("needs_review", False)),
                    "review_reason": rule.get("review_reason", "")
                }
                candidate_rows.append(candidate)

                key = (item.file_id, tag)
                existing = assignments_by_key.get(key)
                if existing is None:
                    assignments_by_key[key] = {
                        "record_type": "assignment",
                        "file_id": item.file_id,
                        "path": item.effective_path,
                        "feature": tag,
                        "role": rule.get("role", "secondary"),
                        "confidence": rule.get("confidence", "low"),
                        "evidence_level": rule.get("evidence_level", "path"),
                        "evidence": evidence,
                        "state": "seeded",
                        "rule_ids": [rule["id"]],
                        "needs_review": bool(rule.get("needs_review", False)),
                        "review_reasons": [rule.get("review_reason", "")] if rule.get("review_reason") else [],
                        "notes": "Mechanical feature routing seed; origin/scope are deferred."
                    }
                    continue

                existing["role"] = "primary" if "primary" in {existing["role"], rule.get("role", "secondary")} else "secondary"
                existing["confidence"] = better_confidence(existing["confidence"], rule.get("confidence", "low"))
                existing["evidence_level"] = better_evidence(existing["evidence_level"], rule.get("evidence_level", "path"))
                existing["evidence"] = sorted(set(existing["evidence"] + evidence))
                existing["rule_ids"] = sorted(set(existing["rule_ids"] + [rule["id"]]))
                existing["needs_review"] = existing["needs_review"] or bool(rule.get("needs_review", False))
                if rule.get("review_reason"):
                    existing["review_reasons"] = sorted(set(existing["review_reasons"] + [rule["review_reason"]]))

        if item_review_reasons:
            # Review-only rules do not create assignments, but their reasons are
            # folded into the file record by adding a synthetic candidate note.
            candidate_rows.append(
                {
                    "record_type": "candidate-note",
                    "file_id": item.file_id,
                    "path": item.effective_path,
                    "rule_ids": [],
                    "needs_review": True,
                    "review_reasons": sorted(set(item_review_reasons))
                }
            )

    assignments = sorted(assignments_by_key.values(), key=lambda row: (row["file_id"], row["feature"]))
    return assignments, candidate_rows, rejected_rows


def file_confidence(assignments: list[dict[str, Any]]) -> str:
    if not assignments:
        return "low"
    rank = min(CONFIDENCE_RANK[row["confidence"]] for row in assignments)
    for name, value in CONFIDENCE_RANK.items():
        if value == rank:
            return name
    return "low"


def build_file_records(
    diff_id: str,
    items: list[WorkItem],
    assignments: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in assignments:
        by_file[row["file_id"]].append(row)

    review_notes: dict[str, list[str]] = defaultdict(list)
    for row in candidate_rows:
        if row.get("record_type") == "candidate-note":
            review_notes[row["file_id"]].extend(row.get("review_reasons", []))

    records: list[dict[str, Any]] = []
    for item in items:
        item_assignments = by_file.get(item.file_id, [])
        tags = sorted(row["feature"] for row in item_assignments)
        reasons = sorted(set(
            review_notes.get(item.file_id, [])
            + [
                reason
                for row in item_assignments
                for reason in row.get("review_reasons", [])
                if reason
            ]
        ))
        needs_review = bool(reasons) or not tags
        records.append(
            {
                "record_type": "file",
                "file_id": item.file_id,
                "diffset": diff_id,
                "status": item.status,
                "old_path": item.old_path,
                "new_path": item.new_path,
                "effective_path": item.effective_path,
                "file_kind": item.file_kind,
                "is_binary": item.is_binary,
                "numstat": {
                    "added": item.numstat_added,
                    "deleted": item.numstat_deleted
                },
                "feature_tags": tags,
                "confidence": file_confidence(item_assignments),
                "evidence_levels": sorted(set(row["evidence_level"] for row in item_assignments), key=lambda x: EVIDENCE_RANK[x]),
                "needs_review": needs_review,
                "review_reasons": reasons,
                "notes": "Feature routing only; provenance and applicability are deferred."
            }
        )
    return records


def write_manifest(out_dir: Path, diffset: Path, diff_id: str, rules_dir: Path, files_count: int, assignments_count: int) -> None:
    manifest = [
        f'diff_id: "{diff_id}"',
        f'diffset: "{diffset}"',
        'project_phase: "1a-feature-routing"',
        'schema: "feature-routing-v1"',
        f'rules_dir: "{rules_dir}"',
        f'created_at_utc: "{datetime.now(timezone.utc).isoformat()}"',
        f'files_count: {files_count}',
        f'assignments_count: {assignments_count}',
        'forbidden_fields: "origin,scope,mtk_version,deletion_reason"',
        'notes: "Mechanical seeded feature routing; cluster analysis decides origin, scope, action, and migration design."'
    ]
    (out_dir / "manifest.yaml").write_text("\n".join(manifest) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diffset", type=Path, help="Path to analysis/diffsets/<diff-id>")
    parser.add_argument("output_dir", type=Path, help="Output directory for feature routing results")
    parser.add_argument("--rules-dir", type=Path, default=Path(__file__).resolve().parents[1] / "rules")
    parser.add_argument("--diff-id", default=None)
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing output directory")
    args = parser.parse_args()

    diffset = args.diffset.resolve()
    out_dir = args.output_dir.resolve()
    rules_dir = args.rules_dir.resolve()
    diff_id = args.diff_id or diffset.name

    if out_dir.exists() and any(out_dir.iterdir()) and not args.force:
        print(f"error: output directory exists and is not empty: {out_dir}", file=sys.stderr)
        print("use --force to overwrite generated files", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    tags_data = load_json(rules_dir / "feature-tags-v1.json")
    allowed_tags = set(tags_data["allowed_tags"])
    seed_rules = load_json(rules_dir / "feature-seed-rules-v1.json")

    items = build_work_items(diffset)
    assignments, candidates, rejected = seed_assignments(items, seed_rules, allowed_tags)
    file_records = build_file_records(diff_id, items, assignments, candidates)

    write_jsonl(out_dir / "files.jsonl", file_records)
    write_jsonl(out_dir / "assignments.jsonl", assignments)
    write_jsonl(out_dir / "candidates.jsonl", candidates)
    write_jsonl(out_dir / "rejected-candidates.jsonl", rejected)
    write_manifest(out_dir, diffset, diff_id, rules_dir, len(file_records), len(assignments))

    print(f"wrote {len(file_records)} files and {len(assignments)} feature assignments to {out_dir}")
    if rejected:
        print(f"warning: {len(rejected)} rejected candidates; see rejected-candidates.jsonl", file=sys.stderr)
    unrouted = sum(1 for row in file_records if not row["feature_tags"])
    if unrouted:
        print(f"warning: {unrouted} files have no feature_tags and need review", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
