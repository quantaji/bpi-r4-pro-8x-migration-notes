Verdict: accept

Evidence Read: inspected `run.json`, `sources.snapshot.json`, `candidates/all-candidates.tsv`, all `candidates/by-source/*.tsv`, `summaries/row-summary.tsv`, `summaries/file-summary.tsv`, `summaries/deleted-rows.tsv`, `summaries/unresolved.tsv`, generator `scripts/build-row-provenance.py`, source rules `rules/provenance-sources-v1.json`, and the round coverage plan. For the 33 audited file_ids, I read all 51 row-summary entries, all matching file-summary entries, all 228 candidate rows, all 33 diff patches, and all 150 unique referenced candidate source files from `reference-source-codes`. Recomputed signal side/count, normalized-exact, line-containment, and binary SHA evidence: 0 mismatches.

Structural Checks: pass. `run.json` has `input_rows=1662`, `file_summaries=1181`, `candidate_rows_written=8014`, `unresolved_rows=327`, `basename_search=true`. Column stability passed: `all-candidates.tsv` 36 fields / 8014 data rows; `row-summary.tsv` 20 fields / 1662 data rows; `file-summary.tsv` 10 fields / 1181 data rows. `deleted-rows.tsv` and `unresolved.tsv` were also stable.

Common High-Risk Rows:
- `000857`: pass. Direct 8X exact postimage only across 3 rows; correctly `direct-only-postimage`, manual review yes.
- `000955`: pass. Multiple exact 1.0000 sources preserved, including BPI siblings, MTK, U-Boot, direct postimage.
- `000886`: pass. Multiple exact 1.0000 non-direct sources preserved; direct treated as postimage.
- `000972`: pass. Direct is 1.0000, strongest non-direct is medium BPI sibling 0.9281; `medium-source-evidence` and manual review are appropriate.
- `000343`: pass. BPI sibling and direct line-containment 1.0000; weaker target/upstream scores remain auxiliary.
- `000380`: pass. Exact BPI sibling and direct candidates preserved; no false single-origin collapse.
- `000055`: pass. Deleted class `removed-by-vendor-but-target-still-has-content` is supported by baseline and target content; wording stays source-tree inferred.
- `000505`: pass. Deleted class `target-aligned-deletion-candidate` is supported by baseline-only strong content; manual review retained.

Assigned Random Rows:
- `000612`: pass. Deleted row with baseline/MTK exact and target medium; class and manual-review wording reasonable.
- `000770`: pass. Deleted row with baseline/MTK exact and target 0.9902; class preserves target content presence.
- `000065`: pass. Deleted row with multiple exact retained-content sources.
- `000764`: pass. Deleted row with target/baseline/MTK exact retained-content evidence.
- `000101`: pass. Target-aligned deletion: baseline/MTK/sibling evidence present, no target strong candidate.
- `000206`: pass. Target-aligned deletion: baseline and MTK evidence only.
- `000328`: pass. Deleted row with baseline/MTK exact and target 0.9681; class reasonable.
- `000324`: pass. Deleted row with multiple 1.0000 retained-content sources.
- `000133`: pass. Deleted row with multiple exact retained-content sources.
- `000205`: pass. Target-aligned deletion: baseline and MTK evidence only.
- `000367`: pass. Multi-source high exact BPI sibling/direct rows preserved.
- `000281`: pass. Multi-source high exact BPI sibling/direct rows preserved.
- `000354`: pass. Multi-source high exact BPI sibling/direct rows preserved.
- `000878`: pass. Five repeated rows preserve BPI/direct exact and MTK high evidence.
- `000670`: pass. Multi-source high exact BPI sibling/direct evidence.
- `001140`: pass. Multi-source high exact BPI/direct/MTK evidence.
- `001143`: pass. Three rows preserve exact BPI, direct, MTK feed/SDK evidence.
- `000558`: pass. Multi-source high exact BPI sibling/direct evidence.
- `001174`: pass. Many 1.0000 sources preserved in `source_scores`; top candidates are MTK/BPI exact.
- `001180`: pass. Exact BPI/direct/MTK feed evidence preserved.

Self-Selected Rows:
- `000025`: selected for direct-only plus one-line signal. Pass: marked manual review, not treated as origin.
- `000032`: selected for direct 1.0000 with only low non-direct scores. Pass: remains `direct-only-postimage`.
- `000041`: selected for firmware/binary SHA evidence. Pass: binary SHA matches BPI sibling/direct/MTK 25.12; weak nonmatching binary candidate is not promoted.
- `000828`: selected for medium U-Boot same-basename candidate among high source evidence. Pass: high MTK/BPI sources drive provenance; U-Boot remains auxiliary.
- `000963`: selected for rare `single-source-high`. Pass: direct postimage is not sole origin; BPI 4E is the only high non-direct source, siblings remain medium.

Findings: none blocking or correctness-significant.

No-Issue Confirmations:
- Direct 8X vendor matches are consistently labeled postimage evidence.
- Multiple 1.0000 sources are preserved in `source_scores`.
- Primary provenance reflects strongest trusted non-direct evidence, not direct-only scoring.
- Deleted-row wording does not overclaim commit-level deletion provenance.
- Sampled unresolved rows are reasonable and expose their strong evidence rather than hiding it.
- Metrics in sampled candidate rows match the referenced patches/source files.

Residual Risk: provenance remains an evidence/navigation index, not a migration decision source. `top_n=5` means `all-candidates.tsv` is the written top-candidate set, while summaries may preserve broader best-by-source scores. Low-signal rows, direct-only rows, binary evidence, and deleted rows still require human review.

Recommendation: Phase 3 can use this provenance output as a navigation aid, with the stated caveat that it must not replace M00-M11 review decisions.
