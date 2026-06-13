#!/usr/bin/env python3
"""Build row-level provenance evidence from vendor diff rows.

This tool is a provenance evidence generator. It does not decide migration
policy. It compares each row in the Project Phase 2 owner-step worklist against
configured reference source trees, then writes candidate evidence and summary
views under ../analysis/provenance/<diffset>/ by default.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_VERSION = "2"
DIFFSET_NAME = "8x-vs-openwrt24-base"

CONFIDENCE_HIGH = 0.95
CONFIDENCE_MEDIUM = 0.70
CONFIDENCE_LOW = 0.30

TEXT_CACHE: dict[tuple[str, int], tuple[str, bool]] = {}
SHA256_CACHE: dict[str, str] = {}
PATCH_ID_CACHE: dict[str, str] = {}
NORMALIZED_LINES_CACHE: dict[str, list[str]] = {}
TOKEN_SET_CACHE: dict[str, set[str]] = {}
CHAR_NGRAM_CACHE: dict[tuple[str, int], set[str]] = {}
PAIR_METRIC_CACHE: dict[tuple[str, str, int, int], tuple[int, float, float, float, float | None, float | None]] = {}

OUTPUT_CANDIDATE_HEADER = [
    "row_index",
    "candidate_rank",
    "file_id",
    "owner_step",
    "source_step",
    "status",
    "path",
    "file_kind",
    "route_classes",
    "features",
    "diff_patch",
    "signal_side",
    "signal_line_count",
    "source_name",
    "source_type",
    "source_role",
    "source_path",
    "candidate_kind",
    "source_label",
    "primary_metric",
    "primary_score",
    "confidence",
    "patch_id_match",
    "normalized_exact",
    "binary_sha256_exact",
    "line_containment",
    "token_jaccard",
    "char_5gram_jaccard",
    "ordered_lcs_ratio",
    "edit_similarity",
    "row_patch_id",
    "candidate_patch_id",
    "row_binary_sha256",
    "candidate_binary_sha256",
    "evidence",
    "notes",
]

ROW_SUMMARY_HEADER = [
    "row_index",
    "file_id",
    "owner_step",
    "source_step",
    "status",
    "path",
    "file_kind",
    "route_classes",
    "features",
    "signal_side",
    "signal_line_count",
    "primary_provenance",
    "source_scores",
    "direct_8x_postimage",
    "baseline_preimage",
    "target_coverage",
    "deleted_row_class",
    "needs_manual_review",
    "unresolved_reason",
    "decision_reason",
]

FILE_SUMMARY_HEADER = [
    "file_id",
    "path",
    "statuses",
    "owner_steps",
    "source_steps",
    "row_count",
    "primary_provenance",
    "source_scores",
    "needs_manual_review",
    "unresolved_reason",
]

BEST_BY_SOURCE_HEADER = OUTPUT_CANDIDATE_HEADER

DELETED_HEADER = [
    "row_index",
    "file_id",
    "owner_step",
    "source_step",
    "path",
    "signal_line_count",
    "deleted_row_class",
    "content_sources",
    "target_presence",
    "baseline_presence",
    "decision_reason",
]

UNRESOLVED_HEADER = ROW_SUMMARY_HEADER

SKIP_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "bin",
    "build_dir",
    "dl",
    "logs",
    "node_modules",
    "staging_dir",
    "tmp",
}

BINARY_SUFFIXES = {
    ".bin",
    ".blob",
    ".dtb",
    ".elf",
    ".fw",
    ".gz",
    ".img",
    ".ipk",
    ".itb",
    ".ko",
    ".o",
    ".so",
    ".tar",
    ".tgz",
    ".xz",
    ".zip",
}

BINARY_FILE_KINDS = {
    "binary",
    "firmware",
}


@dataclass(frozen=True)
class Source:
    name: str
    source_type: str
    root: Path
    role: str


@dataclass(frozen=True)
class PatchSignal:
    patch_path: Path | None
    side: str
    raw_lines: list[str]
    lines: list[str]
    text: str
    patch_id: str
    notes: str


@dataclass(frozen=True)
class Candidate:
    source: Source
    path: Path
    candidate_kind: str


@dataclass(frozen=True)
class CandidateScore:
    candidate: Candidate
    source_label: str
    primary_metric: str
    primary_score: float
    confidence: str
    patch_id_match: bool
    normalized_exact: bool
    binary_sha256_exact: bool
    line_containment: float
    token_jaccard: float
    char_5gram_jaccard: float
    ordered_lcs_ratio: float | None
    edit_similarity: float | None
    candidate_patch_id: str
    row_binary_sha256: str
    candidate_binary_sha256: str
    evidence: str
    notes: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], header: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def decode_bytes(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def read_text_lossy(path: Path, max_bytes: int) -> tuple[str, bool]:
    cache_key = (str(path), max_bytes)
    if cache_key in TEXT_CACHE:
        return TEXT_CACHE[cache_key]
    data = path.read_bytes()
    truncated = len(data) > max_bytes
    if truncated:
        data = data[:max_bytes]
    result = (decode_bytes(data), truncated)
    TEXT_CACHE[cache_key] = result
    return result


def file_sha256(path: Path) -> str:
    cache_key = str(path)
    if cache_key in SHA256_CACHE:
        return SHA256_CACHE[cache_key]
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    value = digest.hexdigest()
    SHA256_CACHE[cache_key] = value
    return value


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_line(line: str) -> str:
    return " ".join(line.strip().split())


def normalized_lines(text: str) -> list[str]:
    cache_key = stable_hash(text)
    if cache_key in NORMALIZED_LINES_CACHE:
        return NORMALIZED_LINES_CACHE[cache_key]
    output: list[str] = []
    for line in text.splitlines():
        clean = normalize_line(line)
        if not clean:
            continue
        if clean.startswith(("diff --git ", "index ", "@@ ", "+++ ", "--- ")):
            continue
        output.append(clean)
    NORMALIZED_LINES_CACHE[cache_key] = output
    return output


def normalized_text_from_lines(lines: list[str]) -> str:
    return "\n".join(lines)


def token_set(text: str) -> set[str]:
    cache_key = stable_hash(text)
    if cache_key not in TOKEN_SET_CACHE:
        TOKEN_SET_CACHE[cache_key] = set(re.findall(r"[A-Za-z0-9_./:+-]+", text.lower()))
    return TOKEN_SET_CACHE[cache_key]


def char_ngrams(text: str, n: int = 5) -> set[str]:
    cache_key = (stable_hash(text), n)
    if cache_key in CHAR_NGRAM_CACHE:
        return CHAR_NGRAM_CACHE[cache_key]
    compact = re.sub(r"\s+", " ", text.strip().lower())
    if not compact:
        CHAR_NGRAM_CACHE[cache_key] = set()
        return CHAR_NGRAM_CACHE[cache_key]
    if len(compact) <= n:
        CHAR_NGRAM_CACHE[cache_key] = {compact}
        return CHAR_NGRAM_CACHE[cache_key]
    CHAR_NGRAM_CACHE[cache_key] = {compact[i : i + n] for i in range(len(compact) - n + 1)}
    return CHAR_NGRAM_CACHE[cache_key]


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left.intersection(right)) / len(left.union(right))


def lcs_ratio(left: list[str], right: list[str], max_cells: int) -> float | None:
    if not left or not right:
        return 0.0
    if len(left) * len(right) > max_cells:
        return None
    prev = [0] * (len(right) + 1)
    for left_item in left:
        curr = [0]
        for idx, right_item in enumerate(right, 1):
            if left_item == right_item:
                curr.append(prev[idx - 1] + 1)
            else:
                curr.append(max(prev[idx], curr[-1]))
        prev = curr
    return prev[-1] / len(left)


def levenshtein_similarity(left: str, right: str, max_chars: int) -> float | None:
    if not left or not right:
        return 0.0
    if len(left) > max_chars or len(right) > max_chars:
        return None
    if left == right:
        return 1.0
    if len(left) < len(right):
        left, right = right, left
    prev = list(range(len(right) + 1))
    for i, left_char in enumerate(left, 1):
        curr = [i]
        for j, right_char in enumerate(right, 1):
            cost = 0 if left_char == right_char else 1
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j - 1] + cost))
        prev = curr
    distance = prev[-1]
    return 1.0 - (distance / max(len(left), len(right)))


def patch_id_for_text(text: str) -> str:
    if not text.strip():
        return ""
    cache_key = stable_hash(text)
    if cache_key in PATCH_ID_CACHE:
        return PATCH_ID_CACHE[cache_key]
    try:
        proc = subprocess.run(
            ["git", "patch-id", "--stable"],
            input=text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return ""
    if proc.returncode != 0 or not proc.stdout.strip():
        PATCH_ID_CACHE[cache_key] = ""
        return ""
    value = proc.stdout.split()[0]
    PATCH_ID_CACHE[cache_key] = value
    return value


def is_binary_row(row: dict[str, str]) -> bool:
    file_kind = row.get("file_kind", "")
    suffix = Path(row.get("path", "")).suffix.lower()
    return file_kind in BINARY_FILE_KINDS or suffix in BINARY_SUFFIXES


def confidence_for_score(score: float, exact: bool) -> str:
    if exact:
        return "high"
    if score >= CONFIDENCE_HIGH:
        return "high"
    if score >= CONFIDENCE_MEDIUM:
        return "medium"
    if score >= CONFIDENCE_LOW:
        return "low"
    return "none"


def source_role_group(source: Source) -> str:
    if source.source_type == "direct-8x-vendor":
        return "direct-postimage"
    if source.source_type == "openwrt-baseline":
        return "baseline-preimage"
    if source.source_type == "target-openwrt":
        return "target-reference"
    if source.source_type in {"openwrt-upstream", "linux-upstream", "mt76-upstream", "u-boot-upstream"}:
        return "upstream-reference"
    if source.source_type in {"mtk-openwrt-sdk", "mtk-feeds"}:
        return "mtk-reference"
    if source.source_type == "bpi-sibling-vendor":
        return "bpi-sibling-reference"
    return "reference"


def load_sources(path: Path, root: Path) -> list[Source]:
    obj = read_json(path)
    sources: list[Source] = []
    for row in obj["sources"]:
        source_root = (root / row["path"]).resolve()
        if not source_root.exists():
            continue
        sources.append(
            Source(
                name=row["name"],
                source_type=row["source_type"],
                root=source_root,
                role=row.get("role", ""),
            )
        )
    return sources


def sources_snapshot(path: Path, root: Path, sources: list[Source]) -> dict[str, Any]:
    original = read_json(path)
    return {
        "source_config": original,
        "resolved_sources": [
            {
                "name": source.name,
                "source_type": source.source_type,
                "role_group": source_role_group(source),
                "root": str(source.root),
                "exists": source.root.exists(),
            }
            for source in sources
        ],
        "notes_repo_root": str(root),
    }


def resolve_diff_patch(diff_root: Path, row_path: str) -> Path | None:
    candidate = diff_root / f"{row_path}.patch"
    if candidate.exists():
        return candidate
    return None


def parse_patch_signal(diff_root: Path, row: dict[str, str]) -> PatchSignal:
    patch_path = resolve_diff_patch(diff_root, row["path"])
    if patch_path is None:
        return PatchSignal(None, "missing-diff", [], [], "", "", "diff patch not found")

    text = patch_path.read_text(encoding="utf-8", errors="replace")
    added: list[str] = []
    removed: list[str] = []
    for line in text.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            removed.append(line[1:])

    status = row.get("status", "")
    if status == "D" and removed:
        side = "removed"
        signal_raw_lines = removed
    elif added:
        side = "added"
        signal_raw_lines = added
    elif removed:
        side = "removed"
        signal_raw_lines = removed
    else:
        side = "patch-body"
        signal_raw_lines = text.splitlines()

    signal_text = "\n".join(signal_raw_lines) + "\n"
    normalized = normalized_lines(signal_text)
    patch_id = patch_id_for_text(signal_text) if row["path"].endswith(".patch") else ""
    return PatchSignal(patch_path, side, signal_raw_lines, normalized, signal_text, patch_id, "")


def direct_binary_sha256(row: dict[str, str], sources: list[Source]) -> str:
    if not is_binary_row(row):
        return ""
    direct = next((source for source in sources if source.source_type == "direct-8x-vendor"), None)
    if direct is None:
        return ""
    direct_path = direct.root / row["path"]
    if not direct_path.exists() or not direct_path.is_file():
        return ""
    try:
        return file_sha256(direct_path)
    except OSError:
        return ""


def candidate_same_path(source: Source, row_path: str) -> Candidate | None:
    path = source.root / row_path
    if path.exists() and path.is_file():
        return Candidate(source, path, "same-path")
    return None


def basename_index(sources: list[Source], basenames: set[str]) -> dict[tuple[str, str], list[Path]]:
    index: dict[tuple[str, str], list[Path]] = defaultdict(list)
    if not basenames:
        return index
    for source in sources:
        for root, dirs, files in os.walk(source.root):
            dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
            matched = basenames.intersection(files)
            if not matched:
                continue
            root_path = Path(root)
            for name in sorted(matched):
                index[(source.name, name)].append(root_path / name)
    return index


def collect_candidates(
    row: dict[str, str],
    sources: list[Source],
    basename_paths: dict[tuple[str, str], list[Path]],
    max_basename_candidates: int,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    seen: set[tuple[str, str]] = set()
    basename = Path(row["path"]).name
    for source in sources:
        same = candidate_same_path(source, row["path"])
        if same is not None:
            rel = str(same.path.relative_to(source.root))
            seen.add((source.name, rel))
            candidates.append(same)

        for path in basename_paths.get((source.name, basename), [])[:max_basename_candidates]:
            if not path.is_file():
                continue
            rel = str(path.relative_to(source.root))
            key = (source.name, rel)
            if key in seen:
                continue
            seen.add(key)
            candidates.append(Candidate(source, path, "same-basename"))
    return candidates


def source_label_for(row: dict[str, str], source: Source, primary_score: float, exact: bool) -> str:
    if primary_score < CONFIDENCE_LOW and not exact:
        return "no-strong-match"

    status = row.get("status", "")
    source_type = source.source_type
    highish = exact or primary_score >= CONFIDENCE_HIGH

    if source_type == "direct-8x-vendor":
        if status == "D":
            return "deleted-content-present-in-direct" if highish else "direct-weak-match"
        return "postimage-confirmed" if highish else "postimage-related"

    if status == "D":
        return "deleted-content-present" if highish else "deleted-content-related"

    if source_type == "openwrt-baseline":
        return "preimage-confirmed" if highish else "baseline-related"
    if source_type == "target-openwrt":
        return "target-covered" if highish else "target-related"
    if source_type == "openwrt-upstream":
        return "openwrt-upstream-shared" if highish else "openwrt-upstream-related"
    if source_type == "mtk-openwrt-sdk":
        return "mtk-sdk-shared" if highish else "mtk-sdk-related"
    if source_type == "mtk-feeds":
        return "mtk-feed-shared" if highish else "mtk-feed-related"
    if source_type == "bpi-sibling-vendor":
        return "bpi-sibling-shared" if highish else "bpi-sibling-related"
    if source_type in {"linux-upstream", "mt76-upstream", "u-boot-upstream"}:
        return "upstream-shared" if highish else "upstream-related"
    return "source-shared" if highish else "source-related"


def choose_primary_metric(
    patch_id_match: bool,
    normalized_exact: bool,
    binary_sha256_exact: bool,
    line_containment: float,
    token_jaccard_score: float,
    char_5gram_score: float,
    ordered_lcs_score: float | None,
    edit_score: float | None,
) -> tuple[str, float]:
    if patch_id_match:
        return "patch-id", 1.0
    if normalized_exact:
        return "normalized-exact", 1.0
    if binary_sha256_exact:
        return "binary-sha256", 1.0
    if line_containment > 0:
        return "line-containment", line_containment
    if token_jaccard_score > 0:
        return "token-jaccard", token_jaccard_score
    if ordered_lcs_score is not None and ordered_lcs_score > 0:
        return "ordered-lcs", ordered_lcs_score
    if char_5gram_score > 0:
        return "char-5gram", char_5gram_score
    if edit_score is not None and edit_score > 0:
        return "edit-similarity", edit_score
    return "none", 0.0


def pair_metrics(
    signal_lines: list[str],
    candidate_lines: list[str],
    signal_text_normalized: str,
    candidate_text_normalized: str,
    max_lcs_cells: int,
    max_edit_chars: int,
) -> tuple[int, float, float, float, float | None, float | None]:
    signal_hash = stable_hash(signal_text_normalized)
    candidate_hash = stable_hash(candidate_text_normalized)
    cache_key = (signal_hash, candidate_hash, max_lcs_cells, max_edit_chars)
    if cache_key in PAIR_METRIC_CACHE:
        return PAIR_METRIC_CACHE[cache_key]

    signal_set = set(signal_lines)
    candidate_set = set(candidate_lines)
    if signal_set and candidate_set:
        shared_lines = len(signal_set.intersection(candidate_set))
        line_containment = shared_lines / len(signal_set)
    else:
        shared_lines = 0
        line_containment = 0.0

    token_jaccard_score = jaccard(token_set(signal_text_normalized), token_set(candidate_text_normalized))
    char_5gram_score = jaccard(char_ngrams(signal_text_normalized, 5), char_ngrams(candidate_text_normalized, 5))
    promising = line_containment > 0 or token_jaccard_score >= 0.10
    ordered_lcs_score = lcs_ratio(signal_lines, candidate_lines, max_lcs_cells) if promising else None
    edit_score = (
        levenshtein_similarity(signal_text_normalized, candidate_text_normalized, max_edit_chars)
        if promising
        else None
    )
    result = (shared_lines, line_containment, token_jaccard_score, char_5gram_score, ordered_lcs_score, edit_score)
    PAIR_METRIC_CACHE[cache_key] = result
    return result


def score_candidate(
    signal: PatchSignal,
    row: dict[str, str],
    candidate: Candidate,
    max_bytes: int,
    max_lcs_cells: int,
    max_edit_chars: int,
    row_binary_sha256: str,
) -> CandidateScore:
    notes: list[str] = []
    try:
        text, truncated = read_text_lossy(candidate.path, max_bytes)
    except OSError as exc:
        return CandidateScore(
            candidate,
            "read-error",
            "none",
            0.0,
            "none",
            False,
            False,
            False,
            0.0,
            0.0,
            0.0,
            None,
            None,
            "",
            row_binary_sha256,
            "",
            "",
            str(exc),
        )

    if truncated:
        notes.append("candidate text truncated before scoring")

    candidate_sha256 = ""
    binary_sha256_exact = False
    if row_binary_sha256 and candidate.path.is_file():
        try:
            candidate_sha256 = file_sha256(candidate.path)
            binary_sha256_exact = candidate_sha256 == row_binary_sha256
        except OSError as exc:
            notes.append(f"candidate sha256 failed: {exc}")

    candidate_patch_id = patch_id_for_text(text) if candidate.path.name.endswith(".patch") else ""
    patch_id_match = bool(signal.patch_id and candidate_patch_id and signal.patch_id == candidate_patch_id)

    candidate_lines = normalized_lines(text)
    signal_text_normalized = normalized_text_from_lines(signal.lines)
    candidate_text_normalized = normalized_text_from_lines(candidate_lines)
    normalized_exact = bool(signal.lines and stable_hash(signal_text_normalized) == stable_hash(candidate_text_normalized))

    (
        shared_lines,
        line_containment,
        token_jaccard_score,
        char_5gram_score,
        ordered_lcs_score,
        edit_score,
    ) = pair_metrics(
        signal.lines,
        candidate_lines,
        signal_text_normalized,
        candidate_text_normalized,
        max_lcs_cells,
        max_edit_chars,
    )

    primary_metric, primary_score = choose_primary_metric(
        patch_id_match,
        normalized_exact,
        binary_sha256_exact,
        line_containment,
        token_jaccard_score,
        char_5gram_score,
        ordered_lcs_score,
        edit_score,
    )
    exact = patch_id_match or normalized_exact or binary_sha256_exact
    confidence = confidence_for_score(primary_score, exact)
    source_label = source_label_for(row, candidate.source, primary_score, exact)

    evidence_parts: list[str] = []
    if patch_id_match:
        evidence_parts.append("stable patch-id matches")
    if normalized_exact:
        evidence_parts.append("normalized signal text equals normalized candidate text")
    if binary_sha256_exact:
        evidence_parts.append("binary sha256 matches direct 8X postimage")
    if line_containment > 0:
        signal_unique_count = len(set(signal.lines))
        evidence_parts.append(f"{shared_lines}/{signal_unique_count} normalized signal lines found in candidate")
    if not evidence_parts:
        evidence_parts.append("candidate path/name exists but no strong signal match")
    if is_binary_row(row) and not binary_sha256_exact:
        notes.append("binary-or-firmware row; non-sha256 text metrics are weak")
    promising_for_notes = patch_id_match or normalized_exact or binary_sha256_exact or line_containment > 0 or token_jaccard_score >= 0.10
    if ordered_lcs_score is None and promising_for_notes:
        notes.append("ordered LCS skipped by max cell limit")
    if edit_score is None and promising_for_notes:
        notes.append("edit similarity skipped by max char limit")

    return CandidateScore(
        candidate,
        source_label,
        primary_metric,
        primary_score,
        confidence,
        patch_id_match,
        normalized_exact,
        binary_sha256_exact,
        line_containment,
        token_jaccard_score,
        char_5gram_score,
        ordered_lcs_score,
        edit_score,
        candidate_patch_id,
        row_binary_sha256,
        candidate_sha256,
        "; ".join(evidence_parts),
        "; ".join(notes),
    )


def sort_scores(scores: list[CandidateScore]) -> list[CandidateScore]:
    return sorted(
        scores,
        key=lambda item: (
            item.primary_score,
            item.patch_id_match,
            item.normalized_exact,
            item.binary_sha256_exact,
            item.candidate.candidate_kind == "same-path",
            item.candidate.source.source_type != "direct-8x-vendor",
            item.candidate.source.name,
            str(item.candidate.path),
        ),
        reverse=True,
    )


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}"


def bool_text(value: bool) -> str:
    return "yes" if value else "no"


def candidate_row(row_index: int, row: dict[str, str], signal: PatchSignal, score: CandidateScore, rank: int) -> dict[str, Any]:
    source = score.candidate.source
    try:
        source_path = str(score.candidate.path.relative_to(source.root))
    except ValueError:
        source_path = str(score.candidate.path)
    return {
        "row_index": row_index,
        "candidate_rank": rank,
        "file_id": row["file_id"],
        "owner_step": row.get("owner_step", ""),
        "source_step": row.get("source_step", ""),
        "status": row.get("status", ""),
        "path": row["path"],
        "file_kind": row.get("file_kind", ""),
        "route_classes": row.get("route_classes", ""),
        "features": row.get("features", ""),
        "diff_patch": str(signal.patch_path) if signal.patch_path else "",
        "signal_side": signal.side,
        "signal_line_count": len(signal.lines),
        "source_name": source.name,
        "source_type": source.source_type,
        "source_role": source_role_group(source),
        "source_path": source_path,
        "candidate_kind": score.candidate.candidate_kind,
        "source_label": score.source_label,
        "primary_metric": score.primary_metric,
        "primary_score": format_float(score.primary_score),
        "confidence": score.confidence,
        "patch_id_match": bool_text(score.patch_id_match),
        "normalized_exact": bool_text(score.normalized_exact),
        "binary_sha256_exact": bool_text(score.binary_sha256_exact),
        "line_containment": format_float(score.line_containment),
        "token_jaccard": format_float(score.token_jaccard),
        "char_5gram_jaccard": format_float(score.char_5gram_jaccard),
        "ordered_lcs_ratio": format_float(score.ordered_lcs_ratio),
        "edit_similarity": format_float(score.edit_similarity),
        "row_patch_id": signal.patch_id,
        "candidate_patch_id": score.candidate_patch_id,
        "row_binary_sha256": score.row_binary_sha256,
        "candidate_binary_sha256": score.candidate_binary_sha256,
        "evidence": score.evidence,
        "notes": "; ".join(part for part in [signal.notes, score.notes] if part),
    }


def no_candidate_row(row_index: int, row: dict[str, str], signal: PatchSignal) -> dict[str, Any]:
    return {
        "row_index": row_index,
        "candidate_rank": 0,
        "file_id": row["file_id"],
        "owner_step": row.get("owner_step", ""),
        "source_step": row.get("source_step", ""),
        "status": row.get("status", ""),
        "path": row["path"],
        "file_kind": row.get("file_kind", ""),
        "route_classes": row.get("route_classes", ""),
        "features": row.get("features", ""),
        "diff_patch": str(signal.patch_path) if signal.patch_path else "",
        "signal_side": signal.side,
        "signal_line_count": len(signal.lines),
        "source_name": "",
        "source_type": "",
        "source_role": "",
        "source_path": "",
        "candidate_kind": "",
        "source_label": "no-candidate",
        "primary_metric": "none",
        "primary_score": "0.0000",
        "confidence": "none",
        "patch_id_match": "no",
        "normalized_exact": "no",
        "binary_sha256_exact": "no",
        "line_containment": "0.0000",
        "token_jaccard": "0.0000",
        "char_5gram_jaccard": "0.0000",
        "ordered_lcs_ratio": "",
        "edit_similarity": "",
        "row_patch_id": signal.patch_id,
        "candidate_patch_id": "",
        "row_binary_sha256": "",
        "candidate_binary_sha256": "",
        "evidence": "no candidate files found",
        "notes": signal.notes,
    }


def best_by_source(scores: list[CandidateScore]) -> list[CandidateScore]:
    best: dict[str, CandidateScore] = {}
    for score in sort_scores(scores):
        key = score.candidate.source.name
        if key not in best:
            best[key] = score
    return sort_scores(list(best.values()))


def source_scores_text(scores: list[CandidateScore], min_score: float = CONFIDENCE_LOW) -> str:
    entries: list[str] = []
    for score in best_by_source(scores):
        if score.primary_score < min_score and score.confidence == "none":
            continue
        entries.append(f"{score.candidate.source.name}:{score.source_label}:{score.primary_score:.4f}")
    return ";".join(entries)


def score_filter(scores: list[CandidateScore], *, include_direct: bool = True) -> list[CandidateScore]:
    output: list[CandidateScore] = []
    for score in scores:
        if not include_direct and score.candidate.source.source_type == "direct-8x-vendor":
            continue
        if score.confidence in {"high", "medium"}:
            output.append(score)
    return sort_scores(output)


def has_source_type(scores: list[CandidateScore], source_type: str, min_confidence: set[str] | None = None) -> bool:
    allowed = min_confidence or {"high", "medium"}
    return any(score.candidate.source.source_type == source_type and score.confidence in allowed for score in scores)


def deleted_class(row: dict[str, str], scores: list[CandidateScore]) -> tuple[str, str]:
    if row.get("status") != "D":
        return "", ""
    baseline = has_source_type(scores, "openwrt-baseline", {"high", "medium"})
    target_high = has_source_type(scores, "target-openwrt", {"high"})
    target_medium = has_source_type(scores, "target-openwrt", {"medium"})
    mtk_newer = any(
        score.candidate.source.name == "mtk-openwrt-25.12" and score.confidence in {"high", "medium"}
        for score in scores
    )
    mtk_any = any(
        score.candidate.source.source_type in {"mtk-openwrt-sdk", "mtk-feeds"}
        and score.confidence in {"high", "medium"}
        for score in scores
    )
    if baseline and target_high:
        return "removed-by-vendor-but-target-still-has-content", "baseline and target both retain matching removed content"
    if baseline and target_medium:
        return (
            "removed-by-vendor-target-related-content",
            "baseline has exact/strong removed content; target has only medium related content",
        )
    if baseline and not (target_high or target_medium):
        return "target-aligned-deletion-candidate", "baseline has removed content; target lacks strong matching candidate"
    if mtk_any and not mtk_newer:
        return "mtk-aligned-deletion-candidate", "MTK-era source has removed content; newer MTK source lacks strong matching candidate"
    if mtk_any:
        return "deleted-content-mtk-family-present", "MTK source still has matching removed content"
    return "vendor-only-or-unresolved-deletion", "no strong baseline/target/MTK deletion alignment found"


def direct_postimage(scores: list[CandidateScore]) -> str:
    direct_scores = [
        score for score in scores if score.candidate.source.source_type == "direct-8x-vendor" and score.confidence in {"high", "medium"}
    ]
    if not direct_scores:
        return "absent-or-not-matched"
    best = sort_scores(direct_scores)[0]
    return f"{best.source_label}:{best.primary_score:.4f}"


def source_presence(scores: list[CandidateScore], source_type: str) -> str:
    matches = [
        score for score in scores if score.candidate.source.source_type == source_type and score.confidence in {"high", "medium"}
    ]
    if not matches:
        return "absent-or-not-matched"
    best = sort_scores(matches)[0]
    return f"{best.source_label}:{best.primary_score:.4f}"


def summarize_row(row_index: int, row: dict[str, str], signal: PatchSignal, scores: list[CandidateScore]) -> dict[str, Any]:
    sorted_scores = sort_scores(scores)
    non_direct = score_filter(sorted_scores, include_direct=False)
    high_non_direct = [score for score in non_direct if score.confidence == "high"]
    medium_non_direct = [score for score in non_direct if score.confidence == "medium"]
    direct_state = direct_postimage(sorted_scores)
    deleted_row_class, deleted_reason = deleted_class(row, sorted_scores)

    unresolved_reasons: list[str] = []
    decision_reason: list[str] = []
    status = row.get("status", "")

    if status == "D":
        primary_provenance = f"deleted-row:{deleted_row_class}"
        decision_reason.append(deleted_reason)
        unresolved_reasons.append("deleted-action is source-tree inferred, not commit-level provenance")
    elif high_non_direct:
        if len(high_non_direct) > 1:
            primary_provenance = "multi-source-high"
            decision_reason.append("multiple non-direct high-confidence source candidates")
        else:
            source = high_non_direct[0].candidate.source
            primary_provenance = f"single-source-high:{source.name}"
            decision_reason.append("one non-direct high-confidence source candidate")
    elif medium_non_direct:
        primary_provenance = "medium-source-evidence"
        decision_reason.append("non-direct medium-confidence source evidence only")
        unresolved_reasons.append("source evidence is medium-confidence")
    elif direct_state.startswith("postimage"):
        primary_provenance = "direct-only-postimage"
        decision_reason.append("direct 8X postimage confirmed but no non-direct source candidate")
        unresolved_reasons.append("direct 8X is postimage evidence, not origin evidence")
    else:
        primary_provenance = "no-strong-source"
        decision_reason.append("no high/medium source candidate")
        unresolved_reasons.append("no high/medium source candidate")

    exact_present = any(score.patch_id_match or score.normalized_exact or score.binary_sha256_exact for score in sorted_scores)
    if len(signal.lines) < 3 and not exact_present:
        unresolved_reasons.append("signal has fewer than 3 normalized lines and no exact match")
    if is_binary_row(row) and not any(score.binary_sha256_exact for score in sorted_scores):
        unresolved_reasons.append("binary/firmware row lacks sha256 exact match")

    return {
        "row_index": row_index,
        "file_id": row["file_id"],
        "owner_step": row.get("owner_step", ""),
        "source_step": row.get("source_step", ""),
        "status": status,
        "path": row["path"],
        "file_kind": row.get("file_kind", ""),
        "route_classes": row.get("route_classes", ""),
        "features": row.get("features", ""),
        "signal_side": signal.side,
        "signal_line_count": len(signal.lines),
        "primary_provenance": primary_provenance,
        "source_scores": source_scores_text(sorted_scores),
        "direct_8x_postimage": direct_state,
        "baseline_preimage": source_presence(sorted_scores, "openwrt-baseline"),
        "target_coverage": source_presence(sorted_scores, "target-openwrt"),
        "deleted_row_class": deleted_row_class,
        "needs_manual_review": bool_text(bool(unresolved_reasons)),
        "unresolved_reason": "; ".join(dict.fromkeys(unresolved_reasons)),
        "decision_reason": "; ".join(decision_reason),
    }


def deleted_summary_row(row_summary: dict[str, Any], scores: list[CandidateScore]) -> dict[str, Any]:
    content_sources = []
    for score in best_by_source(scores):
        if score.confidence in {"high", "medium"}:
            content_sources.append(f"{score.candidate.source.name}:{score.source_label}:{score.primary_score:.4f}")
    return {
        "row_index": row_summary["row_index"],
        "file_id": row_summary["file_id"],
        "owner_step": row_summary["owner_step"],
        "source_step": row_summary["source_step"],
        "path": row_summary["path"],
        "signal_line_count": row_summary["signal_line_count"],
        "deleted_row_class": row_summary["deleted_row_class"],
        "content_sources": ";".join(content_sources),
        "target_presence": row_summary["target_coverage"],
        "baseline_presence": row_summary["baseline_preimage"],
        "decision_reason": row_summary["decision_reason"],
    }


def summarize_files(row_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in row_summaries:
        by_file[row["file_id"]].append(row)

    output: list[dict[str, Any]] = []
    for file_id in sorted(by_file):
        rows = by_file[file_id]
        path = rows[0]["path"]
        statuses = ";".join(sorted({row["status"] for row in rows if row["status"]}))
        owner_steps = ";".join(sorted({row["owner_step"] for row in rows if row["owner_step"]}))
        source_steps = ";".join(sorted({row["source_step"] for row in rows if row["source_step"]}))
        primary = ";".join(dict.fromkeys(row["primary_provenance"] for row in rows if row["primary_provenance"]))
        scores = ";".join(dict.fromkeys(part for row in rows for part in row["source_scores"].split(";") if part))
        unresolved = ";".join(dict.fromkeys(row["unresolved_reason"] for row in rows if row["unresolved_reason"]))
        needs_review = any(row["needs_manual_review"] == "yes" for row in rows)
        output.append(
            {
                "file_id": file_id,
                "path": path,
                "statuses": statuses,
                "owner_steps": owner_steps,
                "source_steps": source_steps,
                "row_count": len(rows),
                "primary_provenance": primary,
                "source_scores": scores,
                "needs_manual_review": bool_text(needs_review),
                "unresolved_reason": unresolved,
            }
        )
    return output


def selected_rows(rows: list[dict[str, str]], file_ids: set[str], limit: int | None) -> list[dict[str, str]]:
    selected = [row for row in rows if not file_ids or row.get("file_id") in file_ids]
    if limit is not None:
        selected = selected[:limit]
    return selected


def clean_output_dir(output_root: Path) -> None:
    for child in ["candidates", "summaries"]:
        path = output_root / child
        if path.exists():
            shutil.rmtree(path)
    for child in ["run.json", "sources.snapshot.json"]:
        path = output_root / child
        if path.exists():
            path.unlink()


def write_by_source(candidate_rows: list[dict[str, Any]], output_root: Path) -> None:
    by_source_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidate_rows:
        source_type = row.get("source_type") or "no-source"
        by_source_type[source_type].append(row)
    by_source_dir = output_root / "candidates/by-source"
    for source_type, rows in sorted(by_source_type.items()):
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "-", source_type).strip("-") or "unknown"
        write_tsv(by_source_dir / f"{safe_name}.tsv", rows, OUTPUT_CANDIDATE_HEADER)


def score_rows(
    rows: list[dict[str, str]],
    sources: list[Source],
    diff_root: Path,
    basename_paths: dict[tuple[str, str], list[Path]],
    top_n: int,
    max_bytes: int,
    max_basename_candidates: int,
    max_lcs_cells: int,
    max_edit_chars: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_rows: list[dict[str, Any]] = []
    best_by_source_rows: list[dict[str, Any]] = []
    row_summaries: list[dict[str, Any]] = []
    deleted_rows: list[dict[str, Any]] = []

    for row_index, row in enumerate(rows, 1):
        signal = parse_patch_signal(diff_root, row)
        candidates = collect_candidates(row, sources, basename_paths, max_basename_candidates)
        row_binary_digest = direct_binary_sha256(row, sources)
        scores = [
            score_candidate(
                signal,
                row,
                candidate,
                max_bytes,
                max_lcs_cells,
                max_edit_chars,
                row_binary_digest,
            )
            for candidate in candidates
        ]
        sorted_scores = sort_scores(scores)
        top_scores = sorted_scores[:top_n]
        if not top_scores:
            candidate_rows.append(no_candidate_row(row_index, row, signal))
        else:
            for rank, score in enumerate(top_scores, 1):
                candidate_rows.append(candidate_row(row_index, row, signal, score, rank))
        for rank, score in enumerate(best_by_source(sorted_scores), 1):
            best_by_source_rows.append(candidate_row(row_index, row, signal, score, rank))

        row_summary = summarize_row(row_index, row, signal, sorted_scores)
        row_summaries.append(row_summary)
        if row.get("status") == "D":
            deleted_rows.append(deleted_summary_row(row_summary, sorted_scores))

    return candidate_rows, best_by_source_rows, row_summaries, deleted_rows


def count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[str(row.get(field, ""))] += 1
    return dict(sorted(counts.items()))


def build_run_manifest(
    args: argparse.Namespace,
    root: Path,
    rows: list[dict[str, str]],
    candidate_rows: list[dict[str, Any]],
    best_by_source_rows: list[dict[str, Any]],
    row_summaries: list[dict[str, Any]],
    file_summaries: list[dict[str, Any]],
    deleted_rows: list[dict[str, Any]],
    unresolved_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "script": "scripts/build-row-provenance.py",
        "script_version": SCRIPT_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "notes_repo_root": str(root),
        "diffset": DIFFSET_NAME,
        "inputs": {
            "rows": str(args.rows.resolve()),
            "diff_root": str(args.diff_root.resolve()),
            "sources": str(args.sources.resolve()),
        },
        "outputs": {
            "output_root": str(args.output_root.resolve()),
            "all_candidates": str((args.output_root / "candidates/all-candidates.tsv").resolve()),
            "best_by_source": str((args.output_root / "candidates/best-by-source.tsv").resolve()),
            "row_summary": str((args.output_root / "summaries/row-summary.tsv").resolve()),
            "file_summary": str((args.output_root / "summaries/file-summary.tsv").resolve()),
            "deleted_rows": str((args.output_root / "summaries/deleted-rows.tsv").resolve()),
            "unresolved": str((args.output_root / "summaries/unresolved.tsv").resolve()),
        },
        "parameters": {
            "file_id": args.file_id,
            "limit": args.limit,
            "top_n": args.top_n,
            "max_bytes": args.max_bytes,
            "basename_search": args.basename_search,
            "max_basename_candidates": args.max_basename_candidates,
            "max_lcs_cells": args.max_lcs_cells,
            "max_edit_chars": args.max_edit_chars,
        },
        "thresholds": {
            "high": CONFIDENCE_HIGH,
            "medium": CONFIDENCE_MEDIUM,
            "low": CONFIDENCE_LOW,
        },
        "counts": {
            "input_rows": len(rows),
            "candidate_rows_written": len(candidate_rows),
            "best_by_source_rows_written": len(best_by_source_rows),
            "row_summaries": len(row_summaries),
            "file_summaries": len(file_summaries),
            "deleted_rows": len(deleted_rows),
            "unresolved_rows": len(unresolved_rows),
            "row_primary_provenance": count_by(row_summaries, "primary_provenance"),
            "row_needs_manual_review": count_by(row_summaries, "needs_manual_review"),
            "candidate_source_type": count_by(candidate_rows, "source_type"),
            "candidate_confidence": count_by(candidate_rows, "confidence"),
            "best_by_source_type": count_by(best_by_source_rows, "source_type"),
            "best_by_source_confidence": count_by(best_by_source_rows, "confidence"),
        },
        "notes": [
            "direct-8x-vendor is treated as postimage confirmation, not as sole origin proof",
            "deleted row classes are source-tree inference, not commit-level deletion provenance",
            "provenance evidence does not replace M00-M11 migration review decisions",
        ],
    }


def parse_args() -> argparse.Namespace:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rows",
        type=Path,
        default=root / "migration_step_reviews/8x-vs-openwrt24-base/P2-owner-step-worklist.tsv",
        help="Input TSV. Defaults to the P2 owner-step worklist.",
    )
    parser.add_argument(
        "--diff-root",
        type=Path,
        default=root / "../analysis/diffsets/8x-vs-openwrt24-base/files",
        help="Diffset files root containing per-path .patch files.",
    )
    parser.add_argument(
        "--sources",
        type=Path,
        default=root / "rules/provenance-sources-v1.json",
        help="Reference source configuration JSON.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=root / "../analysis/provenance/8x-vs-openwrt24-base",
        help="Output directory for provenance artifacts.",
    )
    parser.add_argument("--file-id", action="append", default=[], help="Restrict to one file_id; can be repeated.")
    parser.add_argument("--limit", type=int, default=None, help="Limit rows after optional file_id filtering.")
    parser.add_argument("--top-n", type=int, default=5, help="Number of candidates to write per row.")
    parser.add_argument("--max-bytes", type=int, default=2_000_000, help="Maximum bytes read from each candidate file.")
    parser.add_argument(
        "--basename-search",
        action="store_true",
        help="Also scan reference trees for same-basename candidates. Slower, but useful for moved/renamed patch files.",
    )
    parser.add_argument(
        "--max-basename-candidates",
        type=int,
        default=25,
        help="Maximum same-basename candidates per source and row.",
    )
    parser.add_argument(
        "--max-lcs-cells",
        type=int,
        default=200_000,
        help="Skip ordered LCS when signal lines * candidate lines exceeds this value.",
    )
    parser.add_argument(
        "--max-edit-chars",
        type=int,
        default=4_000,
        help="Skip edit similarity when either normalized text exceeds this character count.",
    )
    return parser.parse_args()


def main() -> int:
    root = repo_root()
    args = parse_args()
    args.rows = args.rows.resolve()
    args.diff_root = args.diff_root.resolve()
    args.sources = args.sources.resolve()
    args.output_root = args.output_root.resolve()

    rows = selected_rows(read_tsv(args.rows), set(args.file_id), args.limit)
    sources = load_sources(args.sources, root)
    basenames = {Path(row["path"]).name for row in rows} if args.basename_search else set()
    basename_paths = basename_index(sources, basenames) if basenames else {}

    candidate_rows, best_by_source_rows, row_summaries, deleted_rows = score_rows(
        rows,
        sources,
        args.diff_root,
        basename_paths,
        args.top_n,
        args.max_bytes,
        args.max_basename_candidates,
        args.max_lcs_cells,
        args.max_edit_chars,
    )
    file_summaries = summarize_files(row_summaries)
    unresolved_rows = [row for row in row_summaries if row["needs_manual_review"] == "yes"]

    clean_output_dir(args.output_root)
    write_tsv(args.output_root / "candidates/all-candidates.tsv", candidate_rows, OUTPUT_CANDIDATE_HEADER)
    write_tsv(args.output_root / "candidates/best-by-source.tsv", best_by_source_rows, BEST_BY_SOURCE_HEADER)
    write_by_source(candidate_rows, args.output_root)
    write_tsv(args.output_root / "summaries/row-summary.tsv", row_summaries, ROW_SUMMARY_HEADER)
    write_tsv(args.output_root / "summaries/file-summary.tsv", file_summaries, FILE_SUMMARY_HEADER)
    write_tsv(args.output_root / "summaries/deleted-rows.tsv", deleted_rows, DELETED_HEADER)
    write_tsv(args.output_root / "summaries/unresolved.tsv", unresolved_rows, UNRESOLVED_HEADER)
    write_json(args.output_root / "sources.snapshot.json", sources_snapshot(args.sources, root, sources))
    write_json(
        args.output_root / "run.json",
        build_run_manifest(
            args,
            root,
            rows,
            candidate_rows,
            best_by_source_rows,
            row_summaries,
            file_summaries,
            deleted_rows,
            unresolved_rows,
        ),
    )

    print(f"wrote provenance v{SCRIPT_VERSION} artifacts for {len(rows)} input rows to {args.output_root}")
    print(f"candidate rows: {len(candidate_rows)}")
    print(f"best-by-source rows: {len(best_by_source_rows)}")
    print(f"row summaries: {len(row_summaries)}")
    print(f"file summaries: {len(file_summaries)}")
    print(f"unresolved rows: {len(unresolved_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
