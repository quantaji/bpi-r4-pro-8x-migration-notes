#!/usr/bin/env python3
"""Build migration phase indexes from Phase 1a feature-routing output."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


CLASS_ORDER = {
    "primary": 0,
    "supporting": 1,
    "review-only": 2,
    "static-only": 3,
    "deferred": 4
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["_line"] = line_no
            rows.append(row)
    return rows


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")


def write_tsv(path: Path, header: list[str], rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for row in rows:
            fh.write("\t".join("" if value is None else str(value) for value in row) + "\n")


def ensure_generated_dirs(output_dir: Path) -> None:
    for subdir in ["by-phase", "summary"]:
        path = output_dir / subdir
        path.mkdir(parents=True, exist_ok=True)
        for child in path.iterdir():
            if child.is_file() and child.suffix in {".json", ".jsonl", ".tsv"}:
                child.unlink()


def phase_filename(phase: dict[str, Any]) -> str:
    return f"{phase['id']}-{phase['slug']}.json"


def clean_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "_line"}


def class_rank(value: str) -> int:
    return CLASS_ORDER.get(value, 99)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("routing_dir", type=Path, help="Feature-routing output directory with files.jsonl and assignments.jsonl")
    parser.add_argument("--phase-map", type=Path, default=Path("rules/feature-phase-map-v1.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-missing", action="store_true", help="Write indexes even if a feature is missing from the phase map")
    args = parser.parse_args()

    routing_dir = args.routing_dir.resolve()
    phase_map_path = args.phase_map.resolve()
    output_dir = args.output_dir.resolve()

    phase_map = load_json(phase_map_path)
    files = load_jsonl(routing_dir / "files.jsonl")
    assignments = load_jsonl(routing_dir / "assignments.jsonl")

    feature_routes: dict[str, list[dict[str, str]]] = phase_map["feature_routes"]
    phases: list[dict[str, str]] = phase_map["phases"]
    phases_by_id = {phase["id"]: phase for phase in phases}
    broad_tags = set(phase_map.get("broad_tags_needing_split", []))

    routed_features = set(feature_routes)
    seen_features = {row["feature"] for row in assignments}
    missing_features = sorted(seen_features - routed_features)
    extra_features = sorted(routed_features - seen_features)

    if missing_features and not args.allow_missing:
        for feature in missing_features:
            print(f"missing feature route: {feature}")
        return 2

    ensure_generated_dirs(output_dir)

    files_by_id = {row["file_id"]: clean_row(row) for row in files}
    phase_assignments: dict[str, list[dict[str, Any]]] = defaultdict(list)
    phase_file_features: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    feature_phase_counts: Counter[tuple[str, str, str]] = Counter()
    broad_split_rows: list[dict[str, Any]] = []
    missing_assignment_rows: list[dict[str, Any]] = []

    for assignment in assignments:
        feature = assignment["feature"]
        file_row = files_by_id.get(assignment["file_id"], {})
        routes = feature_routes.get(feature, [])
        if not routes:
            missing_assignment_rows.append(clean_row(assignment))
            continue

        for route in routes:
            phase_id = route["phase"]
            phase = phases_by_id[phase_id]
            enriched = {
                "assignment": clean_row(assignment),
                "file": file_row,
                "phase": {
                    "id": phase_id,
                    "slug": phase["slug"],
                    "title": phase["title"]
                },
                "route": {
                    "class": route["class"],
                    "note": route.get("note", "")
                }
            }
            phase_assignments[phase_id].append(enriched)
            phase_file_features[phase_id][assignment["file_id"]].append(
                {
                    "feature": feature,
                    "route_class": route["class"],
                    "role": assignment.get("role"),
                    "confidence": assignment.get("confidence"),
                    "needs_review": assignment.get("needs_review", False),
                    "note": route.get("note", "")
                }
            )
            feature_phase_counts[(phase_id, feature, route["class"])] += 1

    for feature in sorted(seen_features & broad_tags):
        routes = feature_routes[feature]
        broad_split_rows.append(
            {
                "feature": feature,
                "phase_routes": ",".join(f"{route['phase']}:{route['class']}" for route in routes),
                "assignment_count": sum(1 for row in assignments if row["feature"] == feature),
                "reason": "broad tag must be split by polarity, direct 8X evidence, runtime necessity, and minimalism risk"
            }
        )

    phase_file_index_rows: list[list[Any]] = []
    review_only_rows: list[list[Any]] = []
    static_only_rows: list[list[Any]] = []
    deferred_rows: list[list[Any]] = []

    for phase in phases:
        phase_id = phase["id"]
        files_for_phase = []
        for file_id, feature_rows in sorted(phase_file_features.get(phase_id, {}).items()):
            file_row = files_by_id[file_id]
            route_classes = sorted({row["route_class"] for row in feature_rows}, key=class_rank)
            phase_features = sorted({row["feature"] for row in feature_rows})
            needs_review = bool(file_row.get("needs_review")) or any(row.get("needs_review") for row in feature_rows)
            file_obj = {
                "file_id": file_id,
                "status": file_row.get("status"),
                "path": file_row.get("effective_path"),
                "file_kind": file_row.get("file_kind"),
                "needs_review": needs_review,
                "route_classes": route_classes,
                "features": sorted(feature_rows, key=lambda row: (class_rank(row["route_class"]), row["feature"])),
                "review_reasons": file_row.get("review_reasons", [])
            }
            files_for_phase.append(file_obj)

            phase_file_index_rows.append(
                [
                    phase_id,
                    phase["slug"],
                    file_id,
                    file_row.get("status"),
                    file_row.get("effective_path"),
                    file_row.get("file_kind"),
                    ",".join(route_classes),
                    ",".join(phase_features),
                    needs_review,
                    "yes",
                    " | ".join(file_row.get("review_reasons", []))
                ]
            )

            review_classes = {row["route_class"] for row in feature_rows}
            if "review-only" in review_classes:
                review_only_rows.append(
                    [
                        phase_id,
                        file_id,
                        file_row.get("status"),
                        file_row.get("effective_path"),
                        file_row.get("file_kind"),
                        ",".join(row["feature"] for row in feature_rows if row["route_class"] == "review-only"),
                        "review-only feature route; inspect before migration"
                    ]
                )
            if "static-only" in review_classes:
                static_only_rows.append(
                    [
                        phase_id,
                        file_id,
                        file_row.get("status"),
                        file_row.get("effective_path"),
                        file_row.get("file_kind"),
                        ",".join(row["feature"] for row in feature_rows if row["route_class"] == "static-only"),
                        "static-only due to unavailable runtime hardware or topology-only scope"
                    ]
                )
            if "deferred" in review_classes:
                deferred_rows.append(
                    [
                        phase_id,
                        file_id,
                        file_row.get("status"),
                        file_row.get("effective_path"),
                        file_row.get("file_kind"),
                        ",".join(row["feature"] for row in feature_rows if row["route_class"] == "deferred"),
                        "deferred from this phase by roadmap boundary"
                    ]
                )

        write_json(
            output_dir / "by-phase" / phase_filename(phase),
            {
                "phase": phase,
                "file_count": len(files_for_phase),
                "assignment_count": len(phase_assignments.get(phase_id, [])),
                "class_counts": dict(Counter(row["route"]["class"] for row in phase_assignments.get(phase_id, []))),
                "status_counts": dict(Counter(row["status"] for row in files_for_phase)),
                "files": files_for_phase
            }
        )

    phase_counts_rows = []
    phase_status_rows = []
    phase_class_rows = []
    for phase in phases:
        phase_id = phase["id"]
        files_for_phase = phase_file_features.get(phase_id, {})
        assignments_for_phase = phase_assignments.get(phase_id, [])
        class_counts = Counter(row["route"]["class"] for row in assignments_for_phase)
        phase_counts_rows.append(
            [
                phase_id,
                phase["slug"],
                phase["title"],
                len(files_for_phase),
                len(assignments_for_phase),
                class_counts.get("primary", 0),
                class_counts.get("supporting", 0),
                class_counts.get("review-only", 0),
                class_counts.get("static-only", 0),
                class_counts.get("deferred", 0)
            ]
        )
        status_counts = Counter(files_by_id[file_id].get("status") for file_id in files_for_phase)
        for status, count in sorted(status_counts.items()):
            phase_status_rows.append([phase_id, phase["slug"], status, count])
        for route_class, count in sorted(class_counts.items(), key=lambda item: class_rank(item[0])):
            phase_class_rows.append([phase_id, phase["slug"], route_class, count])

    write_tsv(
        output_dir / "summary" / "phase-counts.tsv",
        [
            "phase",
            "slug",
            "title",
            "file_count",
            "assignment_count",
            "primary_assignments",
            "supporting_assignments",
            "review_only_assignments",
            "static_only_assignments",
            "deferred_assignments"
        ],
        phase_counts_rows
    )
    write_tsv(
        output_dir / "summary" / "phase-status-counts.tsv",
        ["phase", "slug", "status", "file_count"],
        phase_status_rows
    )
    write_tsv(
        output_dir / "summary" / "phase-class-counts.tsv",
        ["phase", "slug", "route_class", "assignment_count"],
        phase_class_rows
    )
    write_tsv(
        output_dir / "summary" / "phase-feature-counts.tsv",
        ["phase", "feature", "route_class", "assignment_count"],
        [
            [phase_id, feature, route_class, count]
            for (phase_id, feature, route_class), count in sorted(feature_phase_counts.items())
        ]
    )
    write_tsv(
        output_dir / "summary" / "phase-file-index.tsv",
        [
            "phase",
            "slug",
            "file_id",
            "status",
            "path",
            "file_kind",
            "route_classes",
            "features",
            "needs_review",
            "minimalism_gate_required",
            "review_reasons"
        ],
        phase_file_index_rows
    )
    write_tsv(
        output_dir / "summary" / "review-only-files.tsv",
        ["phase", "file_id", "status", "path", "file_kind", "review_only_features", "reason"],
        review_only_rows
    )
    write_tsv(
        output_dir / "summary" / "static-only-files.tsv",
        ["phase", "file_id", "status", "path", "file_kind", "static_only_features", "reason"],
        static_only_rows
    )
    write_tsv(
        output_dir / "summary" / "deferred-files.tsv",
        ["phase", "file_id", "status", "path", "file_kind", "deferred_features", "reason"],
        deferred_rows
    )
    write_tsv(
        output_dir / "summary" / "broad-tags-needing-split.tsv",
        ["feature", "assignment_count", "phase_routes", "reason"],
        [
            [row["feature"], row["assignment_count"], row["phase_routes"], row["reason"]]
            for row in broad_split_rows
        ]
    )
    write_tsv(
        output_dir / "summary" / "missing-feature-routes.tsv",
        ["feature"],
        [[feature] for feature in missing_features]
    )
    write_tsv(
        output_dir / "summary" / "extra-feature-routes.tsv",
        ["feature"],
        [[feature] for feature in extra_features]
    )
    write_jsonl(output_dir / "missing-assignments.jsonl", missing_assignment_rows)
    write_json(
        output_dir / "manifest.json",
        {
            "phase": "1b-phase-routing",
            "routing_dir": str(routing_dir),
            "phase_map": str(phase_map_path),
            "files": len(files),
            "assignments": len(assignments),
            "mapped_features": len(seen_features - set(missing_features)),
            "missing_features": missing_features,
            "extra_feature_routes": extra_features,
            "notes": "Generated phase index. Migration decisions still require evidence review and the unreported-minimalism gate."
        }
    )

    print(
        f"built phase indexes for {len(files)} files, {len(assignments)} assignments, "
        f"{len(seen_features)} features in {output_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
