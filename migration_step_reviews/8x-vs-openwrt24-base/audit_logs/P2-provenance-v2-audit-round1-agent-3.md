Verdict: accept-with-minor-edits

Evidence Read: exact files inspected
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/run.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/sources.snapshot.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/candidates/all-candidates.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/candidates/by-source/*.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/{row-summary.tsv,file-summary.tsv,deleted-rows.tsv,unresolved.tsv}`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/scripts/build-row-provenance.py`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/rules/provenance-sources-v1.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/audit_logs/P2-provenance-v2-audit-round1-coverage-plan.json`
- Diff patches for audited IDs: all 33 corresponding files under `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/`.
- Reference sources: all 147 unique candidate source files referenced by `all-candidates.tsv` for the audited IDs; no missing candidate paths. Independent recomputation checked 236 candidate rows with 0 match-metric mismatches.

Structural Checks: pass
- `run.json`: `input_rows=1662`, `file_summaries=1181`, `candidate_rows_written=8014`, `unresolved_rows=327`, `basename_search=true`.
- Stable columns: `all-candidates.tsv` 36 columns / 8015 lines including header; `row-summary.tsv` 20 columns / 1663 lines; `file-summary.tsv` 10 columns / 1182 lines.
- Additional shape checks passed: all `candidates/by-source/*.tsv`, `deleted-rows.tsv`, and `unresolved.tsv` have stable column counts.

Common High-Risk Rows: row-by-row result
- `000857`: OK. Direct 8X normalized-exact only; correctly `direct-only-postimage`, manual review yes, not treated as origin.
- `000955`: OK. Multiple exact `1.0000` non-direct sources preserved, plus direct postimage.
- `000886`: OK. Multiple exact BPI/MTK non-direct sources preserved; direct 8X remains postimage confirmation.
- `000972`: OK. Direct 1.0000, non-direct only medium/low; correctly `medium-source-evidence` and manual review yes.
- `000343`: OK. BPI sibling and direct line-containment 1.0000; weaker target/upstream retained as related, not promoted.
- `000380`: OK. Exact BPI sibling/direct candidates; duplicate same-source candidate rows do not collapse row-level `source_scores`.
- `000055`: OK. Deleted row class `removed-by-vendor-but-target-still-has-content`; baseline and target exact; commit-level overclaim warning present.
- `000505`: OK. Deleted row class `target-aligned-deletion-candidate`; baseline exact and target absent; commit-level overclaim warning present.

Assigned Random Rows: row-by-row result
- `000763`: OK. Deleted content exact in target/openwrt/MTK/baseline; class and manual-review wording reasonable.
- `000155`: Minor wording issue. Target evidence is medium `deleted-content-related:0.9128`, but class says target still has content. Scores disclose the nuance.
- `000340`: OK. Baseline and MTK 24.10 exact; target absent; target-aligned deletion class reasonable.
- `000730`: OK. Exact deleted content across target/openwrt/MTK/BPI/baseline.
- `000863`: OK. Multiple high matches exist, but only one normalized signal line; unresolved/manual flag is reasonable and not hiding evidence.
- `000731`: OK. Strong deleted-content evidence, target exact, openwrt-main near-exact; wording acceptable.
- `000129`: OK. Exact target/openwrt/MTK/baseline deleted-content evidence.
- `000023`: OK. Exact deleted workflow content in target/openwrt/MTK/baseline.
- `000018`: OK. Exact target/MTK/baseline and high openwrt-main deleted-content evidence.
- `000152`: Minor wording issue. Target evidence is medium `deleted-content-related:0.8571`, but class says target still has content. Scores disclose the nuance.
- `001017`: OK. Multiple exact non-direct sources preserved.
- `000816`: OK. Multiple exact BPI/MTK non-direct sources preserved.
- `001147`: OK. Multiple exact MTK/BPI/feed sources preserved.
- `000570`: OK. Exact BPI sibling non-direct sources plus direct postimage.
- `000650`: OK. Exact BPI sibling non-direct sources plus direct postimage.
- `000240`: OK. Exact BPI sibling sources; MTK related scores preserved separately.
- `000860`: OK. Multiple high line-containment sources, direct postimage not sole origin.
- `000412`: OK. Exact BPI sibling sources plus direct postimage.
- `001074`: OK. Multiple exact BPI/MTK/feed sources preserved.
- `000947`: OK. Multiple exact MTK/BPI/feed sources; older related scores retained.

Self-Selected Rows: row-by-row result
- Selected IDs: `000025`, `000032`, `000033`, `000859`, `000960`.
- `000025`: Selected for direct-only plus one-line signal. OK: manual review yes; no origin overclaim.
- `000032`: Selected for direct-only with weak non-direct related candidates. OK: non-direct scores remain low and row stays unresolved.
- `000033`: Selected for large direct-only U-Boot patch. OK: direct exact only, manual review yes.
- `000859`: Selected for large DTS direct-only with weak same-basename upstream hit. OK: weak upstream candidate remains `no-strong-match`; direct not origin.
- `000960`: Selected for `multi-source-high` where non-direct scores are high but not exact. OK: non-direct high line-containment scores are preserved, direct 1.0000 is still only postimage.

Findings: concrete issues, ordered by severity
- Minor: 16 deleted rows globally, including audited `000155` and `000152`, use `removed-by-vendor-but-target-still-has-content` even though target evidence is medium `deleted-content-related` rather than exact/present. This is not blocking because `target_coverage`, `source_scores`, and unresolved wording expose the confidence, but the class text could be softened to avoid implying exact target retention.

No-Issue Confirmations
- Direct 8X vendor evidence is consistently labeled as postimage confirmation, not origin proof.
- Multiple `1.0000` source scores are preserved in row summaries; 1617 rows contain multiple exact `1.0000` sources.
- Deleted rows consistently carry `deleted-action is source-tree inferred, not commit-level provenance`.
- Unresolved rows are reasonable: deleted inference, direct-only postimage, medium-only evidence, or very short signal.
- Independent recomputation found no candidate existence, normalized-exact, or line-containment mismatches for audited rows.

Residual Risk
- Row-level provenance remains evidence indexing, not migration decisioning.
- Short-signal rows such as `000863` can score high from trivial containment; the manual-review flag mitigates this.
- Medium deleted target matches need human interpretation when used for Phase 3 navigation.

Recommendation: whether Phase 3 can use provenance as a navigation aid
- Yes. Phase 3 can use these provenance v2 outputs as a navigation/index input, with the minor wording caveat above and with M00-M11 review decisions remaining authoritative.
