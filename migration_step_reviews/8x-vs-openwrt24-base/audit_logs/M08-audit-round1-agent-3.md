# M08 Audit Round 1 Agent 3 Raw Report

Verdict: revise-before-accept

Evidence Read:
- Audit targets: `migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.md`, `.files.tsv`
- Required inputs: `M08-acceleration-and-offload.json`, `summary/step-file-index.tsv`, diffset `analysis/diffsets/8x-vs-openwrt24-base/files/`
- Direct 8X source checked: vendor `.config`, `target/linux/mediatek/image/filogic.mk`, `package/kernel/mt76/Makefile`, `package/kernel/linux/modules/netfilter.mk`, HNAT sources under `target/linux/mediatek/files-6.6/drivers/net/ethernet/mediatek/mtk_hnat/`
- Target 25.12 checked: `package/kernel/mt76/Makefile`, `package/kernel/linux/modules/netfilter.mk`, `target/linux/mediatek/image/filogic.mk`, `target/linux/generic/backport-6.12/731-v6.18-net-mediatek-wed-Introduce-MT7992-WED-support-to-MT7.patch`, `733-v6.18-net-mtk-wed-add-dma-mask-limitation-and-GFP_DMA32-fo.patch`
- Diff patches/source inspected for all common high-risk rows, assigned rows, and self-selected rows, including the exact diffset files for `000052`, `000343`, `000350`, `000358`, `000366`, `000374`, `000375`, `000400`, `000421`, `000426`, `000441`, `000442`, `000455`, `000456`, `000458`, `000468`, `000471`, `000897`-`000904`, `000957`, `001027`-`001029`, `001037`, `001056`-`001058`, `001060`, `001062`, `001063`, `001087`, `001099`, `001101`, `001107`, `001110`, `001113`, `001116`, `001118`, `001119`, `001122`, `001123`.

Structural Checks:
- JSON expected `file_count=87`, `assignment_count=165`: pass.
- TSV data rows: 87: pass.
- TSV unique `file_id`: 87, duplicates: none: pass.
- Missing/extra TSV IDs vs JSON: none: pass.
- Exact TSV vs JSON match for `status/path/file_kind/features/route_classes`: pass.
- `step-file-index.tsv` contains M08 rows for audited IDs; notable lines: `000350` line 1464, `001063` line 1518, `001116` line 1539.

Common High-Risk Findings:
- Finding: `001063` disposition is too weak. TSV line 61 marks `target/linux/mediatek/patches-6.6/999-2747-crypto-eth-inline.patch` as `review-only` crypto, but the patch adds non-HNAT fallback tunnel metadata directly to `drivers/net/ethernet/mediatek/mtk_eth_soc.h`: `struct tnl_desc`, `TNL_MAGIC_TAG`, `skb_tnl_cdrt`, and `is_tnl_tag_valid` at diff lines 13-51. Direct 8X vendor `.config` has `# CONFIG_PACKAGE_kmod-mediatek_hnat is not set`, so this non-HNAT branch is exactly the 8X config state. This should be `needs-evidence` or explicitly tied to M08 TOPS/tunnel-offload evidence, not left as pure crypto review-only.
- No other common high-risk row produced an actionable issue. Self-QC rows `000374`, `000375`, `000400`, `000421`, `000426`, `001113`, `001118` are conservatively classified: mixed-title shared-code rows are not dropped, and `001107`/`001113` target-superseded claims are backed by target 25.12 generic backports.

Assigned Low-Risk Findings:
- Finding: `000350` is incorrectly `review-only`. TSV line 7 says the giant mt76 debug tools patch is debug infrastructure, but the patch body changes shared WED/RRO datapath behavior: `dma.c`, `mt7996/dma.c`, `mt7996/mac.c`, `mt7996/mmio.c`, `tx.c`, and `wed.c` are changed at diff lines 60-110; WED token allocation is changed at lines 31070-31085; WED RX buffer release/offload enable/disable and DMA setup are changed at lines 31092-31164. It should be `needs-evidence` with hunk splitting, not review-only.
- Finding: `001116` is incorrectly `review-only`. TSV line 82 says extended WED debugfs is diagnostics-heavy, but its patch changes runtime WED code outside debugfs: `mtk_wed_rx_reset` polls `MTK_WED_WDMA_STATUS` instead of `MTK_WED_WPDMA_STATUS` at diff lines 47-54, and `mtk_wed_attach` reads `dev->hw->soc->regmap.wed_rev_id` at lines 58-63. This should be `needs-evidence` or at least split so non-debug WED reset/attach hunks are not hidden under debugfs.
- Assigned rows `001110`, `001122`, `001099`, `000358`, and `000366` otherwise look correctly routed/dispositioned.

Self-Selected Rows and Findings:
- Self-selected exactly 5 non-overlapping rows: `000348`, `000368`, `000385`, `000393`, `001112`.
- Selection reasons: WED SER reset behavior (`000348`), HWRRO/WED split (`000368`), kernel-version-gated WED cleanup (`000385`), review-only common debug API movement (`000393`), and MLO-throughput-titled WED datapath change (`001112`).
- Findings: no additional actionable issue. `000348`, `000368`, `000385`, and `001112` are correctly retained as M08 `needs-evidence`; `000393` appears genuinely debug/common logging focused, unlike `000350`.

Drop/Superseded Checks:
- Drops `000441`, `000442`, `000455`, `000456` are supported by direct 8X image/package evidence: 8X selects mt7996/mt7996-233 and mt7988 WO firmware, not mt7990/mt7992 firmware. Not title-only.
- Superseded rows `000458`, `000468` are backed by target mt76 firmware packaging.
- Superseded rows `001107`, `001113` are backed by target generic backports `733-v6.18` and `731-v6.18`; no runtime success is inferred.

Boundary Checks:
- Pass. M08 does not claim basic wired success, Wi-Fi runtime success, MLO/AFC success, NAND/eMMC/sysupgrade/storage success, or throughput-only acceptance.
- Needs-evidence rows generally state target/runtime evidence gaps and avoid migration/runtime success claims.
- Exception is classification, not boundary wording: `000350`, `001063`, and `001116` hide M08-adjacent code behind review-only labels.

Findings Ordered by Severity:
1. `000350` TSV line 7: review-only is unsafe; patch changes shared mt76 WED/RRO/offload token and DMA behavior. Evidence: diff lines 60-110, 31070-31164.
2. `001063` TSV line 61: review-only crypto classification hides non-HNAT tunnel metadata used in the direct 8X HNAT-disabled state. Evidence: diff lines 13-51; vendor `.config` has `kmod-mediatek_hnat` unset.
3. `001116` TSV line 82: review-only debugfs classification hides WED reset/attach runtime changes. Evidence: diff lines 47-63.

No-Issue Confirmations:
- Structural coverage is clean.
- Final drop rows are not title-based.
- Target-superseded claims checked against target 25.12 same-semantic evidence.
- HNAT/PPE/RSS/LRO/netfilter/TOPS rows remain evidence-gated.
- No files were modified, no compile was run, no prior audit logs were read.

Residual Risk:
- High residual technical risk remains because many WED/mt76/PPE/HNAT patches are large and require target 6.12 hunk-by-hunk comparison. After fixing the three dispositions above, M08 can proceed as a conservative evidence matrix rather than an acceptance proof.
