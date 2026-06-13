**Verdict:** accept-with-minor-edits

**Evidence Read:**  
Read `run.json`, `sources.snapshot.json`, `candidates/all-candidates.tsv`, all `candidates/by-source/*.tsv`, `summaries/row-summary.tsv`, `summaries/file-summary.tsv`, `summaries/deleted-rows.tsv`, `summaries/unresolved.tsv`, `scripts/build-row-provenance.py`, `rules/provenance-sources-v1.json`, and the coverage plan. For all audited IDs below, read the matching diff patch under `analysis/diffsets/8x-vs-openwrt24-base/files/<path>.patch` and opened every emitted candidate source file resolved from `sources.snapshot.json` plus `all-candidates.tsv` for those row indices. No files modified; no sub-agents used.

**Structural Checks:** pass  
`run.json`: `input_rows=1662`, `file_summaries=1181`, `candidate_rows_written=8014`, `unresolved_rows=327`, `basename_search=true`.  
Stable columns: `all-candidates.tsv` 8015 rows including header, 36 columns throughout; `row-summary.tsv` 1663 rows, 20 columns throughout; `file-summary.tsv` 1182 rows, 10 columns throughout.  
Additional consistency: `deleted-rows.tsv` 285 rows, 11 columns; `unresolved.tsv` 328 rows, 20 columns; all by-source TSVs total 8014 candidate rows.

**Common High-Risk Rows:**  
`000857`: rows 202/249/1590, 8X SD DTSO. Only direct 8X exact evidence; correctly marked `direct-only-postimage`, manual review required.  
`000955`: rows 95/261, `mediatek,mt7987-clk.h`. Multiple exact non-direct sources preserved, including BPI siblings, U-Boot upstream, MTK feed/SDK; `multi-source-high` is consistent.  
`000886`: row 495, `mxl862xx/Kconfig`. Multiple exact BPI/MTK/direct matches; `multi-source-high` consistent.  
`000972`: rows 156/1607/1662, `filogic.mk`. Direct exact, strongest non-direct is BPI 4E at 0.9281; `medium-source-evidence` and manual review are appropriate.  
`000343`: rows 542/546/1410, `package/kernel/mt76/Makefile`. BPI sibling exact matches plus weaker OpenWrt/MTK related scores; `multi-source-high` consistent.  
`000380`: row 561, mt76 patch. Exact BPI sibling/direct evidence; multiple 1.0000 sources preserved; `multi-source-high` consistent.  
`000055`: row 703, deleted ath patch. Baseline, target, OpenWrt main, MTK all retain exact removed content; deleted class is reasonable and not commit-level provenance.  
`000505`: rows 297/1646, deleted dnsmasq patch. Baseline exact only; no target same-path/basename hit; `target-aligned-deletion-candidate` is reasonable.

**Assigned Random Rows:**  
`000775`: deleted `hostapd/src/src/ap/ubus.c`; baseline/MTK 1.0000, target 0.9990; unresolved deletion classification reasonable.  
`000058`: deleted ath regd patch; multiple 1.0000 target/baseline/MTK/OpenWrt sources; deletion wording stays source-tree based.  
`000773`: deleted hostapd patch; baseline and MTK 24.10 exact, target absent; `target-aligned-deletion-candidate` reasonable.  
`000169`: deleted rt2x00 patch; baseline/target/MTK exact; class reasonable.  
`000734`: deleted hostapd LTO patch; baseline/target/MTK exact; class reasonable.  
`000122`: deleted brcm patch; baseline and MTK 24.10 exact, target absent; class reasonable.  
`000761`: deleted hostapd reload patch; baseline/MTK exact, target related at 0.9286; class is usable, but see wording finding.  
`000181`: deleted rtw88 patch; baseline and MTK 24.10 exact, target absent; class reasonable.  
`000335`: deleted mac80211 patch; baseline and MTK 24.10 exact, target absent; class reasonable.  
`000154`: deleted rt2x00 patch; baseline, MTK 24.10/21.02, and old BPI exact; target absent; class reasonable.  
`000662`: hostapd patch; BPI sibling/direct exact, `multi-source-high` consistent.  
`000864`: four rows for RFB DTSO; BPI, direct, MTK feed/SDK exact; multiple 1.0000 sources preserved.  
`000541`: hostapd patch; BPI sibling/direct exact; `multi-source-high` consistent.  
`000905`: AN8855 Kconfig; BPI/direct/MTK exact; `multi-source-high` consistent.  
`000286`: mac80211 patch; BPI sibling/direct exact; `multi-source-high` consistent.  
`000941`: USB unusual declaration header; MTK/BPI/direct exact; `multi-source-high` consistent.  
`000241`: mac80211 cert-mode patch; BPI/direct exact plus MTK 0.9744; `multi-source-high` consistent.  
`000664`: hostapd patch; BPI sibling/direct exact; `multi-source-high` consistent.  
`000565`: hostapd patch; BPI sibling/direct exact; `multi-source-high` consistent.  
`000987`: 2.5G PHY EEE backport patch; BPI sibling/direct exact; `multi-source-high` consistent.

**Self-Selected Rows:**  
Selected IDs: `000025`, `000032`, `000033`, `000069`, `001124`.

`000025`: selected because it is a one-line direct-only README change. Direct line containment is 1.0000, same-basename non-direct candidates are no-strong-match; manual review is correct.  
`000032`: selected because it is direct-only despite several weak non-direct related scores. Direct score 1.0000; non-direct scores stay low, so `direct-only-postimage` is correct.  
`000033`: selected because it is a large direct-only U-Boot 8X patch repeated across rows. Direct normalized exact only; no origin proof is inferred.  
`000069`: selected because deleted-row `source_scores` include a direct 8X weak match. Target/baseline/MTK exact evidence correctly drives the deleted-row class; direct weak match is not treated as origin.  
`001124`: selected because it is `single-source-high` rather than multi-source. Direct exact plus one BPI 4E high non-direct source; `single-source-high:bpi-r4pro-4e-vendor` is consistent.

**Findings:**  
Low: `all-candidates.tsv` is top-N emitted evidence, not exhaustive evidence for every `source_scores` entry. I found 957 row summaries with source names in `source_scores` that are not present among emitted candidate rows for that row, due `top_n=5`. This is documented in `run.json`, but Phase 3 users should not assume every summarized source has a corresponding candidate row in `all-candidates.tsv`.

Low: deleted-row wording can sound stronger than the score in medium target cases. Example `000761` has `target_coverage=deleted-content-related:0.9286`, while `decision_reason` says baseline and target both retain matching removed content. This does not overclaim commit-level deletion provenance, but wording should distinguish exact/high target presence from medium related target content.

**No-Issue Confirmations:**  
Direct 8X evidence is consistently labeled postimage confirmation, not sole origin proof. Multiple 1.0000 sources are preserved in `source_scores`. Primary provenance reflects strongest trusted non-direct evidence where present. Deleted rows are unresolved/manual-review and explicitly described as source-tree inference, not commit-level deletion provenance. Assigned unresolved rows did not hide obvious high-confidence non-deleted origin evidence.

**Residual Risk:**  
Line containment can give strong navigation evidence without proving historical origin. Basename search can surface exact matches for short/common snippets, though short-signal rows are flagged. Deleted-row classes remain source-tree state inference, not commit history.

**Recommendation:**  
Phase 3 can use this provenance output as a navigation/index aid, with the two minor wording/traceability caveats above. It should not replace M00-M11 review decisions or be treated as commit-level provenance.
