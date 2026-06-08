#!/usr/bin/env python3
"""Build by-file, by-feature, and summary indexes from feature-routing JSONL."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["_line"] = line_no
            rows.append(row)
    return rows


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_tsv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for row in rows:
            fh.write("\t".join("" if value is None else str(value) for value in row) + "\n")


def ensure_clean_generated_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.is_file() and child.suffix in {".json", ".tsv"}:
            child.unlink()


def feature_filename(feature: str) -> str:
    return feature.replace(":", "__") + ".json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("routing_dir", type=Path, help="Directory containing files.jsonl and assignments.jsonl")
    args = parser.parse_args()

    routing_dir = args.routing_dir.resolve()
    files = load_jsonl(routing_dir / "files.jsonl")
    assignments = load_jsonl(routing_dir / "assignments.jsonl")

    by_file_dir = routing_dir / "by-file"
    by_feature_dir = routing_dir / "by-feature"
    summary_dir = routing_dir / "summary"
    for path in [by_file_dir, by_feature_dir, summary_dir]:
        ensure_clean_generated_dir(path)

    files_by_id = {row["file_id"]: row for row in files}
    assignments_by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    assignments_by_feature: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in assignments:
        row = {k: v for k, v in row.items() if k != "_line"}
        assignments_by_file[row["file_id"]].append(row)
        assignments_by_feature[row["feature"]].append(row)

    for file_id, file_row in files_by_id.items():
        clean_file = {k: v for k, v in file_row.items() if k != "_line"}
        write_json(
            by_file_dir / f"{file_id}.json",
            {
                "file": clean_file,
                "assignments": sorted(assignments_by_file.get(file_id, []), key=lambda row: row["feature"])
            }
        )

    feature_index = []
    for feature, rows in sorted(assignments_by_feature.items()):
        files_for_feature = []
        for row in sorted(rows, key=lambda item: item["file_id"]):
            file_row = files_by_id.get(row["file_id"], {})
            files_for_feature.append(
                {
                    "file_id": row["file_id"],
                    "status": file_row.get("status"),
                    "path": row["path"],
                    "file_kind": file_row.get("file_kind"),
                    "role": row["role"],
                    "confidence": row["confidence"],
                    "needs_review": row["needs_review"],
                    "rule_ids": row.get("rule_ids", [])
                }
            )
        feature_obj = {
            "feature": feature,
            "file_count": len(files_for_feature),
            "files": files_for_feature
        }
        write_json(by_feature_dir / feature_filename(feature), feature_obj)
        feature_index.append({"feature": feature, "file_count": len(files_for_feature)})

    write_json(by_feature_dir / "index.json", feature_index)

    feature_counts = Counter(row["feature"] for row in assignments)
    domain_counts = Counter(row["feature"].split(":", 1)[0] for row in assignments)
    status_counts = Counter(row["status"] for row in files)
    kind_counts = Counter(row["file_kind"] for row in files)
    confidence_counts = Counter(row["confidence"] for row in assignments)
    review_counts = Counter("needs_review" if row["needs_review"] else "no_review" for row in files)

    write_tsv(
        summary_dir / "feature-counts.tsv",
        ["feature", "file_count"],
        [[feature, count] for feature, count in sorted(feature_counts.items(), key=lambda item: (-item[1], item[0]))]
    )
    write_tsv(
        summary_dir / "domain-counts.tsv",
        ["domain", "assignment_count"],
        [[domain, count] for domain, count in sorted(domain_counts.items(), key=lambda item: (-item[1], item[0]))]
    )
    write_tsv(
        summary_dir / "status-counts.tsv",
        ["status", "file_count"],
        [[status, count] for status, count in sorted(status_counts.items())]
    )
    write_tsv(
        summary_dir / "file-kind-counts.tsv",
        ["file_kind", "file_count"],
        [[kind, count] for kind, count in sorted(kind_counts.items(), key=lambda item: (-item[1], item[0]))]
    )
    write_tsv(
        summary_dir / "assignment-confidence-counts.tsv",
        ["confidence", "assignment_count"],
        [[confidence, count] for confidence, count in sorted(confidence_counts.items())]
    )
    write_tsv(
        summary_dir / "file-review-counts.tsv",
        ["review_state", "file_count"],
        [[state, count] for state, count in sorted(review_counts.items())]
    )

    write_tsv(
        summary_dir / "unrouted-files.tsv",
        ["file_id", "status", "path", "file_kind"],
        [
            [row["file_id"], row["status"], row["effective_path"], row["file_kind"]]
            for row in files
            if not row.get("feature_tags")
        ]
    )
    write_tsv(
        summary_dir / "files-needing-review.tsv",
        ["file_id", "status", "path", "file_kind", "feature_tags", "review_reasons"],
        [
            [
                row["file_id"],
                row["status"],
                row["effective_path"],
                row["file_kind"],
                ",".join(row.get("feature_tags", [])),
                " | ".join(row.get("review_reasons", []))
            ]
            for row in files
            if row.get("needs_review")
        ]
    )

    print(f"built indexes for {len(files)} files and {len(assignments)} assignments in {routing_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
