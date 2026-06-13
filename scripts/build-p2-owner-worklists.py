#!/usr/bin/env python3
"""Build Project Phase 2 owner-step worklists from migration-step reviews."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


BASE_HEADER = [
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

AUDIT_HEADER = ["audit_bucket", "audit_action", "audit_rationale"]

STEP_RE = re.compile(r"^(M\d{2})-.+\.files\.tsv$")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def step_from_tsv(path: Path) -> str:
    match = STEP_RE.match(path.name)
    if not match:
        raise ValueError(f"cannot infer migration step from {path}")
    return match.group(1)


def file_id_sort_key(value: str) -> tuple[int, str]:
    try:
        return int(value), value
    except ValueError:
        return 10**9, value


def load_review_rows(review_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(review_dir.glob("M??-*.files.tsv")):
        source_step = step_from_tsv(path)
        for row in read_tsv(path):
            copied = dict(row)
            copied["_source_step"] = source_step
            rows.append(copied)
    return rows


def load_markdown_texts(review_dir: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for path in sorted(review_dir.glob("M??-*.md")):
        step = path.name[:3]
        texts[step] = path.read_text(encoding="utf-8")
    return texts


def build_owner_worklist(review_rows: list[dict[str, str]], markdown_texts: dict[str, str]) -> list[dict[str, str]]:
    file_ids_by_step: dict[str, set[str]] = {}
    for row in review_rows:
        step = row["_source_step"]
        file_ids_by_step.setdefault(step, set()).add(row["file_id"])

    output: list[dict[str, str]] = []
    for row in review_rows:
        owner_step = row["owner_step"]
        source_step = row["_source_step"]
        file_id = row["file_id"]
        owner_has_file = file_id in file_ids_by_step.get(owner_step, set())
        owner_md_mentions = file_id in markdown_texts.get(owner_step, "")

        if owner_step == source_step:
            handoff_status = "owned-in-source-step"
        elif owner_has_file:
            handoff_status = "covered-by-owner-step-tsv"
        elif owner_md_mentions:
            handoff_status = "acknowledged-in-owner-step-md"
        else:
            handoff_status = "external-handoff-not-reacknowledged"

        output.append(
            {
                "owner_step": owner_step,
                "source_step": source_step,
                "handoff_status": handoff_status,
                "owner_step_tsv_has_file_id": "yes" if owner_has_file else "no",
                "owner_step_md_mentions_file_id": "yes" if owner_md_mentions else "no",
                "file_id": file_id,
                "status": row["status"],
                "path": row["path"],
                "file_kind": row["file_kind"],
                "route_classes": row["route_classes"],
                "features": row["features"],
                "group": row["group"],
                "disposition": row["disposition"],
                "evidence": row["evidence"],
                "notes": row["notes"],
                "minimalism_gate": row["minimalism_gate"],
            }
        )

    return sorted(output, key=lambda item: (item["owner_step"], item["source_step"], file_id_sort_key(item["file_id"]), item["path"]))


def load_bucket_rules(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    obj = json.loads(path.read_text(encoding="utf-8"))
    return obj.get("rules", [])


def value_matches(expected: Any, actual: str) -> bool:
    if isinstance(expected, list):
        return actual in {str(item) for item in expected}
    return str(expected) == actual


def rule_matches(rule: dict[str, Any], row: dict[str, str]) -> bool:
    match = rule.get("match", {})
    return all(value_matches(expected, row.get(key, "")) for key, expected in match.items())


def apply_bucket_rules(row: dict[str, str], rules: list[dict[str, Any]]) -> dict[str, str]:
    for rule in rules:
        if rule_matches(rule, row):
            return {
                "audit_bucket": str(rule["audit_bucket"]),
                "audit_action": str(rule["audit_action"]),
                "audit_rationale": str(rule["audit_rationale"]),
            }
    raise ValueError(
        "no audit bucket rule matched "
        f"{row['owner_step']} <- {row['source_step']} {row['file_id']} {row['path']}"
    )


def build_unacknowledged_rows(worklist_rows: list[dict[str, str]], rules: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows = [row.copy() for row in worklist_rows if row["handoff_status"] == "external-handoff-not-reacknowledged"]
    if rules:
        for row in rows:
            row.update(apply_bucket_rules(row, rules))
    return rows


def validate(rows: list[dict[str, str]], header: list[str], label: str) -> None:
    missing = [field for field in header if any(field not in row for row in rows)]
    if missing:
        raise ValueError(f"{label} rows are missing fields: {sorted(set(missing))}")


def print_summary(worklist_rows: list[dict[str, str]], unack_rows: list[dict[str, str]]) -> None:
    handoff_counts = Counter(row["handoff_status"] for row in worklist_rows)
    print(f"owner worklist rows: {len(worklist_rows)}")
    print(f"unique file_id: {len({row['file_id'] for row in worklist_rows})}")
    for status, count in sorted(handoff_counts.items()):
        print(f"handoff_status {status}: {count}")
    print(f"unacknowledged rows: {len(unack_rows)}")
    if unack_rows and "audit_bucket" in unack_rows[0]:
        for bucket, count in sorted(Counter(row["audit_bucket"] for row in unack_rows).items()):
            print(f"audit_bucket {bucket}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review-dir",
        type=Path,
        default=Path("migration_step_reviews/8x-vs-openwrt24-base"),
        help="Directory containing M00-M11 review markdown and .files.tsv files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to --review-dir.",
    )
    parser.add_argument(
        "--bucket-rules",
        type=Path,
        default=Path("rules/p2-handoff-bucket-rules-v1.json"),
        help="Optional JSON bucket rules used to add audit_bucket columns to the unacknowledged handoff TSV",
    )
    parser.add_argument(
        "--no-bucket-rules",
        action="store_true",
        help="Do not add audit_bucket columns to the unacknowledged handoff TSV",
    )
    args = parser.parse_args()

    review_dir = args.review_dir.resolve()
    output_dir = (args.output_dir or args.review_dir).resolve()
    bucket_rules_path = None if args.no_bucket_rules else args.bucket_rules.resolve()

    review_rows = load_review_rows(review_dir)
    markdown_texts = load_markdown_texts(review_dir)
    bucket_rules = load_bucket_rules(bucket_rules_path)

    worklist_rows = build_owner_worklist(review_rows, markdown_texts)
    unack_rows = build_unacknowledged_rows(worklist_rows, bucket_rules)
    unack_header = BASE_HEADER + (AUDIT_HEADER if bucket_rules else [])

    validate(worklist_rows, BASE_HEADER, "owner worklist")
    validate(unack_rows, unack_header, "unacknowledged handoff")

    write_tsv(output_dir / "P2-owner-step-worklist.tsv", BASE_HEADER, worklist_rows)
    write_tsv(output_dir / "P2-unacknowledged-owner-handoffs.tsv", unack_header, unack_rows)
    print_summary(worklist_rows, unack_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
