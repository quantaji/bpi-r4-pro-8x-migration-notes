#!/usr/bin/env python3
"""Validate Phase 1a feature-routing output."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


FORBIDDEN_FIELDS = {"origin", "scope", "mtk_version", "deletion_reason"}
CONFIDENCE = {"high", "medium", "low"}
EVIDENCE_LEVELS = {
    "path",
    "path+status",
    "path+file-kind",
    "path+keywords",
    "patch-subject",
    "patch-inner-target",
    "patch-content-keyword",
    "binary-path",
    "manual-review"
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            row["_source"] = f"{path.name}:{line_no}"
            rows.append(row)
    return rows


def check_forbidden(row: dict[str, Any], errors: list[str]) -> None:
    present = sorted(FORBIDDEN_FIELDS.intersection(row))
    if present:
        errors.append(f"{row.get('_source', '<unknown>')}: forbidden fields present: {','.join(present)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("routing_dir", type=Path, help="Directory containing files.jsonl and assignments.jsonl")
    parser.add_argument("--tags", type=Path, default=Path(__file__).resolve().parents[1] / "rules" / "feature-tags-v1.json")
    args = parser.parse_args()

    routing_dir = args.routing_dir.resolve()
    allowed_tags = set(load_json(args.tags.resolve())["allowed_tags"])
    errors: list[str] = []
    warnings: list[str] = []

    files_path = routing_dir / "files.jsonl"
    assignments_path = routing_dir / "assignments.jsonl"
    candidates_path = routing_dir / "candidates.jsonl"
    rejected_path = routing_dir / "rejected-candidates.jsonl"

    for required in [files_path, assignments_path]:
        if not required.exists():
            errors.append(f"missing required file: {required}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    files = load_jsonl(files_path)
    assignments = load_jsonl(assignments_path)
    candidates = load_jsonl(candidates_path) if candidates_path.exists() else []
    rejected = load_jsonl(rejected_path) if rejected_path.exists() else []

    files_by_id: dict[str, dict[str, Any]] = {}
    assignment_tags_by_file: dict[str, set[str]] = defaultdict(set)
    assignment_ids = set()

    for row in files:
        check_forbidden(row, errors)
        if row.get("record_type") != "file":
            errors.append(f"{row['_source']}: record_type must be file")
        file_id = row.get("file_id")
        if not file_id:
            errors.append(f"{row['_source']}: missing file_id")
            continue
        if file_id in files_by_id:
            errors.append(f"{row['_source']}: duplicate file_id {file_id}")
        files_by_id[file_id] = row
        if row.get("confidence") not in CONFIDENCE:
            errors.append(f"{row['_source']}: invalid confidence {row.get('confidence')}")
        for tag in row.get("feature_tags", []):
            if tag not in allowed_tags:
                errors.append(f"{row['_source']}: invalid feature tag {tag}")
        if not row.get("feature_tags") and not row.get("needs_review"):
            errors.append(f"{row['_source']}: unrouted file must set needs_review=true")
        for level in row.get("evidence_levels", []):
            if level not in EVIDENCE_LEVELS:
                errors.append(f"{row['_source']}: invalid evidence level {level}")

    for row in assignments:
        check_forbidden(row, errors)
        if row.get("record_type") != "assignment":
            errors.append(f"{row['_source']}: record_type must be assignment")
        file_id = row.get("file_id")
        feature = row.get("feature")
        if file_id not in files_by_id:
            errors.append(f"{row['_source']}: assignment references unknown file_id {file_id}")
        if feature not in allowed_tags:
            errors.append(f"{row['_source']}: invalid feature tag {feature}")
        if row.get("confidence") not in CONFIDENCE:
            errors.append(f"{row['_source']}: invalid confidence {row.get('confidence')}")
        if row.get("evidence_level") not in EVIDENCE_LEVELS:
            errors.append(f"{row['_source']}: invalid evidence level {row.get('evidence_level')}")
        if row.get("role") not in {"primary", "secondary"}:
            errors.append(f"{row['_source']}: invalid role {row.get('role')}")
        key = (file_id, feature)
        if key in assignment_ids:
            errors.append(f"{row['_source']}: duplicate assignment {file_id} {feature}")
        assignment_ids.add(key)
        if file_id and feature:
            assignment_tags_by_file[file_id].add(feature)

    for row in candidates:
        check_forbidden(row, errors)

    for row in rejected:
        check_forbidden(row, errors)
    if rejected:
        warnings.append(f"{len(rejected)} rejected candidates are present")

    for file_id, row in files_by_id.items():
        file_tags = set(row.get("feature_tags", []))
        assignment_tags = assignment_tags_by_file.get(file_id, set())
        if file_tags != assignment_tags:
            errors.append(
                f"{row['_source']}: feature_tags do not match assignments "
                f"file_tags={sorted(file_tags)} assignment_tags={sorted(assignment_tags)}"
            )

    unrouted = [row for row in files if not row.get("feature_tags")]
    low_confidence = [row for row in assignments if row.get("confidence") == "low"]
    needs_review = [row for row in files if row.get("needs_review")]

    feature_counts = Counter(row["feature"] for row in assignments if row.get("feature"))
    domain_counts = Counter(row["feature"].split(":", 1)[0] for row in assignments if row.get("feature"))

    print(f"files: {len(files)}")
    print(f"assignments: {len(assignments)}")
    print(f"features: {len(feature_counts)}")
    print(f"files_needing_review: {len(needs_review)}")
    print(f"unrouted_files: {len(unrouted)}")
    print(f"low_confidence_assignments: {len(low_confidence)}")
    print("domain_assignments: " + ", ".join(f"{domain}={count}" for domain, count in sorted(domain_counts.items())))

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
