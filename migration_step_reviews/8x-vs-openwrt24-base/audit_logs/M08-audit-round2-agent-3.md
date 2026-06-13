# M08 Audit Round 2 Agent 3 Raw Report

Verdict: accept-with-minor-edits

Evidence Read: exact files/patches/source files inspected

- Audit artifacts: `migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.md`, `.files.tsv`
- Required inputs: M08 JSON, `summary/step-file-index.tsv`
- Direct 8X source: vendor `.config`, `target/linux/mediatek/image/filogic.mk`, `files-6.6/arch/arm64/boot/dts/mediatek/mt7988a.dtsi`, `mt7988a-bananapi-bpi-r4-pro-8x.dts`, `mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`
- Target 25.12 source: `package/kernel/mt76/Makefile`, `package/kernel/linux/modules/netfilter.mk`, `package/firmware/linux-firmware/mediatek.mk`, `target/linux/mediatek/patches-6.12/198-dts-mt7988a-enable-wed.patch`, `target/linux/generic/backport-6.12/731-v6.18-net-mediatek-wed-Introduce-MT7992-WED-support-to-MT7.patch`, `733-v6.18-net-mtk-wed-add-dma-mask-limitation-and-GFP_DMA32-fo.patch`
- Diffsets inspected for all common high-risk rows, assigned rows, remediation rows, and self-selected rows under `analysis/diffsets/8x-vs-openwrt24-base/files/`, including netfilter, mt76 Makefile, mt76 WED/RRO patches, firmware rows, HNAT source/header rows, PPE/RSS/LRO/netfilter patches, kernel WED patches, crypto-inline, and TOPS tunnel patch.

Structural Checks: pass

- JSON file count: 87 actual / 87 declared.
- JSON assignment count: 165 actual / 165 declared.
- TSV rows: 87 data rows.
- TSV vs JSON: no missing file_id, no extra file_id, no duplicate file_id.
- Exact TSV match for `status`, `path`, `file_kind`, collapsed `features`, and collapsed `route_classes`: pass.
- Step index M08 subset: 87 rows / 165 assignments.
- TSV disposition counts match markdown: `needs-evidence=60`, `defer=10`, `review-only=9`, `drop=4`, `superseded-by-target=4`.
- TSV owner counts: `M08=77`, `M07=10`.

Common High-Risk Findings

No blocking issue found in the common high-risk rows. I inspected all listed common rows against diff/source evidence.

- `000052`, `000471`: correctly `needs-evidence`; vendor adds `nf-flow-netlink` and libnfnetlink flowtable constant, target has nf-flow/nft-offload but no same package/patch.
- `000343`: correctly `needs-evidence`; vendor mixes `wed_enable=1`, source bump, debug flags, mt7990/testmode firmware; target has ordinary firmware closure but not the vendor WED policy.
- `000374`, `000375`, `000400`, `000421`, `000426`, `001118`: correctly not dropped by title; bodies touch shared mt76/mt7996/WED/RRO/HWRRO or generic APIs.
- `000441`, `000442`, `000455`, `000456`: drops are limited to non-8X firmware binaries; direct 8X recipe/config selects mt7996/mt7996-233 plus `mt7988-wo-firmware`, not mt7990/mt7992 packages.
- HNAT rows `000897`-`000904`, `000957`, `001056`-`001062`: correctly `needs-evidence`; real HNAT/PPE/netfilter/tunnel hooks exist, but direct 8X config leaves `kmod-mediatek_hnat` unset.
- `001107`, `001113`: target same-semantic superseded evidence confirmed in 25.12 generic backports 733 and 731.
- `001123`: correctly `needs-evidence`; patch adds tunnel type metadata only, no direct 8X tunnel runtime policy.

Assigned Low-Risk Findings

No issue found.

- `000394`: defer to M07 is correct; patch is chanctx/scan/ROC/MLO policy.
- `001035`: M08 `needs-evidence` is correct; GLO_MEM/LRO behavior is acceleration-adjacent and target/runtime dependent.
- `001112`: M08 `needs-evidence` is correct despite MLO throughput wording; patch changes WED WPDMA TX_DDONE behavior.
- `000436`: defer to M07 is correct; MLO affiliated-link token policy, with only adjacency to M08.
- `001092`: M08 `needs-evidence` is correct; adds `DEV_PATH_MTK_WDMA` handling to xt flowoffload.
- `001109`: M08 `needs-evidence` is correct; WED assignment logic changes from PCI-domain to WED hardware list.
- `000407`: review-only is correct; testmode RX gain calibration, not runtime offload acceptance.

Self-Selected Rows and Findings

Selected exactly 5 suspicious rows from remaining M08 rows: `000350`, `000368`, `000385`, `001116`, `001121`.

- `000350`: selected because "debug tools" title can hide datapath changes. Finding: TSV is correct; patch changes WED token allocation, RX buffer/page-fragment release, offload enable/disable sizing, and DMA setup.
- `000368`: selected because HWRRO separation is broad. Finding: TSV is correct; patch adds RRO queue helpers, RX token/page-pool handling, RRO indication processing.
- `000385`: selected because "compile flag" title can hide kernel-version cleanup behavior. Finding: TSV is correct; patch gates RRO page/token free paths and moves WDMA TID assignment.
- `001116`: selected because "debugfs" title can hide runtime behavior. Finding: TSV is correct; patch changes WED reset polling and attach revision read outside debugfs.
- `001121`: selected because Wi-Fi L1 SER can be misrouted to M07. Finding: TSV is correct; patch toggles PSE WDMA link-down bits in WED reset/start path, so M08 evidence-needed is appropriate.

Drop/Superseded Checks

- Drops `000441`, `000442`, `000455`, `000456`: confirmed not title-based and not hiding generic/shared code; they are firmware binaries. Direct 8X image/config evidence supports exclusion from 8X package closure.
- Superseded `000458`, `000468`: target 25.12 mt76 Makefile installs `mt7996_dsp.bin` and `mt7996_wm_233.bin`.
- Superseded `001107`: target backport 733 carries same DMA32/dma-mask semantic.
- Superseded `001113`: target backport 731 carries same MT7992-on-MT7988 second WDMA RX ring / WED v3-or-greater semantic.

Boundary Checks

Pass. M08 does not claim basic wired success, Wi-Fi runtime success, MLO/AFC success, storage/sysupgrade success, or throughput-only acceptance. Markdown lines 9, 22-24, and 195 explicitly reject those boundaries.

Findings Ordered By Severity

- Low/editorial: `M08-acceleration-and-offload.md:7` says "No second audit round has been launched." In this round2 audit context that sentence is stale and should be updated by the coordinator/editor. This is not a technical disposition defect.

No-Issue Confirmations

No actionable row-level correctness issue found. Disposition/owner choices were supported by actual diff bodies and direct 8X/target evidence. Remediation rows `000350`, `000374`, `000375`, `000400`, `000421`, `000426`, `001063`, `001113`, `001116`, `001118` look correctly handled.

Residual Risk

High residual implementation risk remains because many rows are intentionally `needs-evidence` and require target 6.12/25.12 API comparison plus later runtime validation. The matrix represents a review queue, not proof of offload success.
