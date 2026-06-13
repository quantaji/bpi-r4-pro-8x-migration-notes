#!/usr/bin/env python3
"""Build Phase 3 implementation worklists from audited Phase 2 artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_VERSION = "1"
DIFFSET_NAME = "8x-vs-openwrt24-base"
MIGRATION_STEPS = [f"M{idx:02d}" for idx in range(12)]

BASE_FIELDS = [
    "phase3_row_id",
    "phase3_source",
    "phase3_row_kind",
    "phase3_priority",
    "phase3_attention_flags",
    "phase3_read_first",
    "phase3_drilldown_refs",
]

OWNER_FIELDS = [
    "owner_step",
    "source_step",
    "handoff_status",
    "owner_step_tsv_has_file_id",
    "owner_step_md_mentions_file_id",
    "file_id",
    "status",
    "path",
    "file_kind",
    "route_classes",
    "features",
    "group",
    "disposition",
    "evidence",
    "notes",
    "minimalism_gate",
]

HANDOFF_FIELDS = [
    "audit_bucket",
    "audit_action",
    "audit_rationale",
    "handoff_attention",
]

PROVENANCE_FIELDS = [
    "primary_provenance",
    "source_scores",
    "direct_8x_postimage",
    "baseline_preimage",
    "target_coverage",
    "deleted_row_class",
    "needs_provenance_review",
    "provenance_unresolved_reason",
    "provenance_decision_reason",
    "provenance_source_count",
    "provenance_high_source_count",
    "provenance_has_mtk",
    "provenance_has_bpi_sibling",
    "provenance_has_target",
    "provenance_has_upstream",
    "provenance_has_direct",
    "provenance_multi_source",
]

FILE_PROVENANCE_FIELDS = [
    "file_primary_provenance",
    "file_source_scores",
    "file_needs_provenance_review",
    "file_provenance_unresolved_reason",
]

OUTPUT_HEADER = BASE_FIELDS + OWNER_FIELDS + HANDOFF_FIELDS + PROVENANCE_FIELDS + FILE_PROVENANCE_FIELDS

IMPLEMENTATION_RELEVANT_DISPOSITIONS = {
    "migrate",
    "rewrite",
    "needs-evidence",
    "static-only",
    "defer",
}

LOW_RELEVANCE_DISPOSITIONS = {
    "drop",
    "review-only",
    "superseded-by-target",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], header: list[str] = OUTPUT_HEADER) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def join_parts(parts: list[str]) -> str:
    return ";".join(dict.fromkeys(part for part in parts if part))


def row_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row["owner_step"], row["source_step"], row["file_id"], row["path"])


def parse_source_scores(source_scores: str) -> list[tuple[str, str, float]]:
    parsed: list[tuple[str, str, float]] = []
    for part in source_scores.split(";"):
        if not part:
            continue
        pieces = part.rsplit(":", 2)
        if len(pieces) != 3:
            continue
        source, label, score_text = pieces
        try:
            score = float(score_text)
        except ValueError:
            continue
        parsed.append((source, label, score))
    return parsed


def provenance_flags(source_scores: str) -> dict[str, str]:
    parsed = parse_source_scores(source_scores)
    high = [(source, label, score) for source, label, score in parsed if score >= 0.95]
    has_mtk = any(source.startswith("mtk-") or "mtk-" in label for source, label, _ in parsed)
    has_bpi = any("bpi-" in source or "bpi-" in label for source, label, _ in parsed)
    has_target = any(source.startswith("target-") or label.startswith("target-") for source, label, _ in parsed)
    has_upstream = any("upstream" in source or "upstream" in label for source, label, _ in parsed)
    has_direct = any(source == "direct-8x-vendor" for source, _, _ in parsed)
    return {
        "provenance_source_count": str(len(parsed)),
        "provenance_high_source_count": str(len(high)),
        "provenance_has_mtk": yes_no(has_mtk),
        "provenance_has_bpi_sibling": yes_no(has_bpi),
        "provenance_has_target": yes_no(has_target),
        "provenance_has_upstream": yes_no(has_upstream),
        "provenance_has_direct": yes_no(has_direct),
        "provenance_multi_source": yes_no(len(parsed) > 1),
    }


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def handoff_attention(audit_bucket: str) -> str:
    if audit_bucket in {"true-owner-gap", "needs-human-decision", "wrong-owner-or-source"}:
        return "yes"
    if audit_bucket in {"covered-by-topic", "global-worklist-only"}:
        return "maybe"
    return "no"


def phase3_priority(row: dict[str, str], audit_bucket: str, needs_provenance_review: str, flags: list[str]) -> str:
    if audit_bucket == "needs-human-decision" or "human-decision" in flags:
        return "P0-human-decision"
    if audit_bucket in {"true-owner-gap", "wrong-owner-or-source"}:
        return "P1-handoff-risk"
    if "direct-only-postimage" in flags:
        return "P1-provenance-risk"
    if row.get("owner_step") == "M10" and row.get("disposition") in IMPLEMENTATION_RELEVANT_DISPOSITIONS:
        return "P1-storage-risk"
    if needs_provenance_review == "yes" and row.get("disposition") in IMPLEMENTATION_RELEVANT_DISPOSITIONS:
        return "P1-provenance-risk"
    if row.get("disposition") in IMPLEMENTATION_RELEVANT_DISPOSITIONS:
        return "P2-implementation-relevant"
    if audit_bucket or flags:
        return "P2-review-attention"
    return "P3-reference"


def phase3_row_kind(audit_bucket: str, needs_provenance_review: str) -> str:
    if audit_bucket == "needs-human-decision":
        return "owner-row-needs-human-decision"
    if audit_bucket:
        return "owner-row-with-handoff-risk"
    if needs_provenance_review == "yes":
        return "owner-row-with-provenance-risk"
    return "normal-owner-row"


def build_attention_flags(
    row: dict[str, str],
    audit_bucket: str,
    primary_provenance: str,
    deleted_row_class: str,
    needs_provenance_review: str,
) -> list[str]:
    flags: list[str] = []
    if audit_bucket:
        flags.append(f"handoff:{audit_bucket}")
    if audit_bucket == "needs-human-decision":
        flags.append("human-decision")
    if needs_provenance_review == "yes":
        flags.append("provenance-review")
    if primary_provenance == "direct-only-postimage":
        flags.append("direct-only-postimage")
    if deleted_row_class:
        flags.append("deleted-row")
    if deleted_row_class == "removed-by-vendor-target-related-content":
        flags.append("target-related-deleted-content")
    if row.get("owner_step") == "M10":
        flags.append("storage-install-sysupgrade-boundary")
    if row.get("owner_step") in {"M07", "M08"} and row.get("file_kind") == "patch":
        flags.append("large-patch-stack-expected")
    if row.get("disposition") in LOW_RELEVANCE_DISPOSITIONS and (audit_bucket or needs_provenance_review == "yes"):
        flags.append("low-disposition-with-attention")
    return flags


def read_first(row: dict[str, str], audit_bucket: str, needs_provenance_review: str) -> str:
    refs = [
        f"M-step:{row.get('owner_step', '')}",
        "P2-owner-step-worklist.tsv",
    ]
    if audit_bucket:
        refs.append("P2-unacknowledged-owner-handoffs.tsv")
    if needs_provenance_review == "yes":
        refs.append("provenance/summaries/unresolved.tsv")
    refs.append("provenance/summaries/row-summary.tsv")
    refs.append("provenance/candidates/best-by-source.tsv")
    return ";".join(refs)


def drilldown_refs(row: dict[str, str]) -> str:
    file_id = row["file_id"]
    return ";".join(
        [
            f"diff-file:{row['path']}.patch",
            f"provenance-row:file_id={file_id},owner_step={row['owner_step']},source_step={row['source_step']}",
            f"provenance-file:file_id={file_id}",
            f"best-by-source:file_id={file_id}",
        ]
    )


def load_handoff_index(rows: list[dict[str, str]]) -> dict[tuple[str, str, str, str], dict[str, str]]:
    index: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = row_key(row)
        if key in index:
            existing = index[key]
            for field in ["audit_bucket", "audit_action", "audit_rationale"]:
                existing[field] = join_parts([existing.get(field, ""), row.get(field, "")])
        else:
            index[key] = row
    return index


def load_row_summary_index(rows: list[dict[str, str]]) -> dict[int, dict[str, str]]:
    return {int(row["row_index"]): row for row in rows}


def load_file_summary_index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["file_id"]: row for row in rows}


def build_worklist(
    owner_rows: list[dict[str, str]],
    handoff_rows: list[dict[str, str]],
    row_summary_rows: list[dict[str, str]],
    file_summary_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    handoff_index = load_handoff_index(handoff_rows)
    row_summary_index = load_row_summary_index(row_summary_rows)
    file_summary_index = load_file_summary_index(file_summary_rows)
    output: list[dict[str, Any]] = []
    missing_provenance: list[str] = []
    missing_handoff_owner_rows: list[str] = []

    owner_keys = {row_key(row) for row in owner_rows}
    for key in handoff_index:
        if key not in owner_keys:
            missing_handoff_owner_rows.append("|".join(key))

    for idx, owner_row in enumerate(owner_rows, 1):
        row_summary = row_summary_index.get(idx)
        if row_summary is None:
            missing_provenance.append(str(idx))
            row_summary = {}
        file_summary = file_summary_index.get(owner_row["file_id"], {})
        handoff_row = handoff_index.get(row_key(owner_row), {})
        audit_bucket = handoff_row.get("audit_bucket", "")
        audit_action = handoff_row.get("audit_action", "")
        audit_rationale = handoff_row.get("audit_rationale", "")
        needs_provenance_review = row_summary.get("needs_manual_review", "")
        primary_provenance = row_summary.get("primary_provenance", "")
        deleted_row_class = row_summary.get("deleted_row_class", "")
        attention = handoff_attention(audit_bucket)
        flags = build_attention_flags(
            owner_row,
            audit_bucket,
            primary_provenance,
            deleted_row_class,
            needs_provenance_review,
        )
        output_row: dict[str, Any] = {
            "phase3_row_id": f"P3-{idx:04d}",
            "phase3_source": "owner-worklist+handoff" if audit_bucket else "owner-worklist",
            "phase3_row_kind": phase3_row_kind(audit_bucket, needs_provenance_review),
            "phase3_priority": phase3_priority(owner_row, audit_bucket, needs_provenance_review, flags),
            "phase3_attention_flags": ";".join(flags),
            "phase3_read_first": read_first(owner_row, audit_bucket, needs_provenance_review),
            "phase3_drilldown_refs": drilldown_refs(owner_row),
        }
        for field in OWNER_FIELDS:
            output_row[field] = owner_row.get(field, "")
        output_row.update(
            {
                "audit_bucket": audit_bucket,
                "audit_action": audit_action,
                "audit_rationale": audit_rationale,
                "handoff_attention": attention,
                "primary_provenance": primary_provenance,
                "source_scores": row_summary.get("source_scores", ""),
                "direct_8x_postimage": row_summary.get("direct_8x_postimage", ""),
                "baseline_preimage": row_summary.get("baseline_preimage", ""),
                "target_coverage": row_summary.get("target_coverage", ""),
                "deleted_row_class": deleted_row_class,
                "needs_provenance_review": needs_provenance_review,
                "provenance_unresolved_reason": row_summary.get("unresolved_reason", ""),
                "provenance_decision_reason": row_summary.get("decision_reason", ""),
                "file_primary_provenance": file_summary.get("primary_provenance", ""),
                "file_source_scores": file_summary.get("source_scores", ""),
                "file_needs_provenance_review": file_summary.get("needs_manual_review", ""),
                "file_provenance_unresolved_reason": file_summary.get("unresolved_reason", ""),
            }
        )
        output_row.update(provenance_flags(row_summary.get("source_scores", "")))
        output.append(output_row)

    diagnostics = {
        "missing_provenance_row_indices": missing_provenance,
        "handoff_rows_without_owner_row": missing_handoff_owner_rows,
    }
    return output, diagnostics


def write_readme(path: Path) -> None:
    path.write_text(
        """# Phase 3 Worklists: 8x-vs-openwrt24-base

This directory is generated by `migration-notes-repo/scripts/build-phase3-worklists.py`.

`phase3-worklist.tsv` is the canonical Phase 3 implementation index. It joins
the audited Phase 2 owner-step worklist, global handoff audit overlay, and
provenance v2 summaries. It does not replace the M00-M11 review matrices and it
does not make final migration decisions.

Flat step views:

- `M00.tsv` through `M11.tsv`: rows filtered by `owner_step`.

Queues:

- `unacknowledged-handoffs.tsv`: rows with Phase 2 global handoff audit overlay.
- `human-decision.tsv`: rows that need human decision before implementation.
- `provenance-review.tsv`: rows whose provenance summary requires manual review.
- `direct-only.tsv`: rows where direct 8X postimage is the only strong evidence.
- `deleted-rows.tsv`: deleted rows and rows with deleted-row provenance classes.

Use `source_scores` for multi-source provenance. Use
`analysis/provenance/8x-vs-openwrt24-base/candidates/best-by-source.tsv` for
drill-down evidence from each source score.
""",
        encoding="utf-8",
    )


def clean_output(output_root: Path) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)


def write_outputs(output_root: Path, rows: list[dict[str, Any]], run: dict[str, Any]) -> None:
    clean_output(output_root)
    write_tsv(output_root / "phase3-worklist.tsv", rows)
    for step in MIGRATION_STEPS:
        write_tsv(output_root / f"{step}.tsv", [row for row in rows if row["owner_step"] == step])
    write_tsv(output_root / "unacknowledged-handoffs.tsv", [row for row in rows if row["audit_bucket"]])
    write_tsv(output_root / "human-decision.tsv", [row for row in rows if row["phase3_priority"] == "P0-human-decision"])
    write_tsv(output_root / "provenance-review.tsv", [row for row in rows if row["needs_provenance_review"] == "yes"])
    write_tsv(output_root / "direct-only.tsv", [row for row in rows if row["primary_provenance"] == "direct-only-postimage"])
    write_tsv(output_root / "deleted-rows.tsv", [row for row in rows if row["status"] == "D" or row["deleted_row_class"]])
    write_readme(output_root / "README.md")
    write_json(output_root / "run.json", run)


def counts_for(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field, "")) for row in rows).items()))


def build_run_manifest(args: argparse.Namespace, rows: list[dict[str, Any]], diagnostics: dict[str, Any]) -> dict[str, Any]:
    return {
        "script": "scripts/build-phase3-worklists.py",
        "script_version": SCRIPT_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "diffset": DIFFSET_NAME,
        "inputs": {
            "owner_worklist": str(args.owner_worklist.resolve()),
            "unacknowledged_handoffs": str(args.unacknowledged_handoffs.resolve()),
            "provenance_row_summary": str(args.provenance_row_summary.resolve()),
            "provenance_file_summary": str(args.provenance_file_summary.resolve()),
        },
        "outputs": {
            "output_root": str(args.output_root.resolve()),
            "phase3_worklist": str((args.output_root / "phase3-worklist.tsv").resolve()),
        },
        "counts": {
            "rows": len(rows),
            "unique_file_ids": len({row["file_id"] for row in rows}),
            "by_owner_step": counts_for(rows, "owner_step"),
            "by_phase3_priority": counts_for(rows, "phase3_priority"),
            "by_phase3_row_kind": counts_for(rows, "phase3_row_kind"),
            "by_audit_bucket": counts_for(rows, "audit_bucket"),
            "by_primary_provenance": counts_for(rows, "primary_provenance"),
            "needs_provenance_review": counts_for(rows, "needs_provenance_review"),
            "queue_rows": {
                "unacknowledged_handoffs": sum(1 for row in rows if row["audit_bucket"]),
                "human_decision": sum(1 for row in rows if row["phase3_priority"] == "P0-human-decision"),
                "provenance_review": sum(1 for row in rows if row["needs_provenance_review"] == "yes"),
                "direct_only": sum(1 for row in rows if row["primary_provenance"] == "direct-only-postimage"),
                "deleted_rows": sum(1 for row in rows if row["status"] == "D" or row["deleted_row_class"]),
            },
        },
        "diagnostics": diagnostics,
        "notes": [
            "This is a derived implementation index, not a new review decision.",
            "A file_id may appear in multiple owner_step views when one changed file affects multiple migration steps.",
            "M00 is kept as a Phase 3 evidence/triage view; most direct implementation starts at M01.",
        ],
    }


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--owner-worklist",
        type=Path,
        default=root / "migration_step_reviews/8x-vs-openwrt24-base/P2-owner-step-worklist.tsv",
    )
    parser.add_argument(
        "--unacknowledged-handoffs",
        type=Path,
        default=root / "migration_step_reviews/8x-vs-openwrt24-base/P2-unacknowledged-owner-handoffs.tsv",
    )
    parser.add_argument(
        "--provenance-row-summary",
        type=Path,
        default=root / "../analysis/provenance/8x-vs-openwrt24-base/summaries/row-summary.tsv",
    )
    parser.add_argument(
        "--provenance-file-summary",
        type=Path,
        default=root / "../analysis/provenance/8x-vs-openwrt24-base/summaries/file-summary.tsv",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=root / "../analysis/phase3-worklists/8x-vs-openwrt24-base",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.owner_worklist = args.owner_worklist.resolve()
    args.unacknowledged_handoffs = args.unacknowledged_handoffs.resolve()
    args.provenance_row_summary = args.provenance_row_summary.resolve()
    args.provenance_file_summary = args.provenance_file_summary.resolve()
    args.output_root = args.output_root.resolve()

    owner_rows = read_tsv(args.owner_worklist)
    handoff_rows = read_tsv(args.unacknowledged_handoffs)
    row_summary_rows = read_tsv(args.provenance_row_summary)
    file_summary_rows = read_tsv(args.provenance_file_summary)

    rows, diagnostics = build_worklist(owner_rows, handoff_rows, row_summary_rows, file_summary_rows)
    run = build_run_manifest(args, rows, diagnostics)
    write_outputs(args.output_root, rows, run)

    print(f"wrote Phase 3 worklists for {len(rows)} rows to {args.output_root}")
    print(f"unique file_id: {run['counts']['unique_file_ids']}")
    print(f"unacknowledged handoff rows: {run['counts']['queue_rows']['unacknowledged_handoffs']}")
    print(f"provenance review rows: {run['counts']['queue_rows']['provenance_review']}")
    print(f"direct-only rows: {run['counts']['queue_rows']['direct_only']}")
    print(f"deleted rows: {run['counts']['queue_rows']['deleted_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
