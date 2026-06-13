# M08 Audit Round 1 Agent 1 Raw Report

Verdict: revise-before-accept

Evidence Read:
- Audit targets: `migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.md`, `.files.tsv`
- Routing inputs: `M08-acceleration-and-offload.json`, `summary/step-file-index.tsv`
- Direct vendor evidence: `.config`, `target/linux/mediatek/image/filogic.mk`, `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a.dtsi`, `mt7988a-bananapi-bpi-r4-pro-8x.dts`
- Target evidence: `package/kernel/mt76/Makefile`, `package/kernel/linux/modules/netfilter.mk`, `target/linux/mediatek/patches-6.12/198-dts-mt7988a-enable-wed.patch`, `target/linux/generic/backport-6.12/731-v6.18-net-mediatek-wed-Introduce-MT7992-WED-support-to-MT7.patch`, `733-v6.18-net-mtk-wed-add-dma-mask-limitation-and-GFP_DMA32-fo.patch`
- Diff/vendor patches inspected for common/sample/self-selected rows: netfilter/libnfnetlink, mt76 `0003`, `0005`, `0007`, `0031`, `0032`, `0050`, `0057`, `0064`, `0066`, `0078`, `0083`; mediatek kernel `999-2709`, `2710`, `2711`, `2720`, `2741`, `2742`, `2743`, `2745`, `2746`, `3000`, `3001`, `3014`, `3020`-`3026`, `3028`, `3030`-`3032`, `3034`, `4100`
- Vendor HNAT/PPE source inspected: `mtk_hnat/hnat.c`, `hnat.h`, `hnat_debugfs.c`, `hnat_mcast.c`, `hnat_nf_hook.c`, `hnat_stag.c`, `nf_hnat_mtk.h`, `include/net/ra_nat.h`, `mtk_eth_dbg.c`

Structural Checks:
- JSON file count: pass, 87 files.
- JSON assignment count: pass, 165 assignments.
- TSV rows: pass, 87 data rows.
- Duplicate/missing/extra file_id: pass, none.
- Exact TSV vs JSON match for `file_id/status/path/file_kind/route_classes/features`: pass.
- Step index vs JSON file IDs: pass.
- TSV status counts: pass, `A=85`, `M=2`.
- TSV route class counts: pass, `primary=84`, `review-only=3`; assignment-level JSON classes match `primary=162`, `review-only=3`.
- Dispositions: `needs-evidence=57`, `review-only=12`, `defer=10`, `drop=4`, `superseded-by-target=4`.
- Owners: `M08=77`, `M07=10`.

Common High-Risk Findings:
- No actionable issue found in the required common high-risk rows.
- Self-QC rows `000374`, `000375`, `000400`, `000421`, `000426`, `001113`, `001118` are correctly not title-dropped. Patch bodies really touch shared mt76/WED/RRO/HWRRO or target-superseded WED semantics.
- HNAT/PPE/netfilter/TOPS rows are correctly conservative as `needs-evidence` or `review-only`; they do not claim runtime acceleration success.
- Firmware drops `000441`, `000442`, `000455`, `000456` are supported by direct 8X recipe/config evidence selecting mt7996/mt7996-233 plus `mt7988-wo-firmware`, not mt7990/mt7992 runtime/testmode firmware.

Assigned Low-Risk Findings:
- `000346`: correct `needs-evidence`; patch clears `wed_enable`/`has_rro` on WED attach failure.
- `000348`: correct `needs-evidence`; patch removes WED stop during L1 SER.
- `000894`: correct `review-only`; `mtk_eth_dbg.c` is debugfs/diagnostic register tooling, not datapath enablement.
- `001088`: acceptable `needs-evidence`; PPE internal debugfs is diagnostic but coupled to PPE import decision.
- `001111`: correct `needs-evidence`; WDMA ring cleanup on Wi-Fi module reinsertion is WED runtime-adjacent.
- `001115`: correct `needs-evidence`; hwpath WMM changes cross PPE/offload/WED APIs.
- `001117`: correct `needs-evidence`; RRO RX-D init flow is WED/RRO datapath.

Self-Selected Rows and Findings:
- Selected `000350` because a huge "debug tools" patch is risky to classify by subject. Finding below: it is misclassified.
- Selected `000393` because common debug API movement could hide shared runtime changes. No issue; inspected body is debug API relocation.
- Selected `000407` because testmode/calibration rows often touch runtime firmware paths. No issue; it is RX gain calibration/testmode.
- Selected `000409` because testmode refactor is broad. No issue; body remains testmode/debug/calibration handling.
- Selected `001112` because MLO throughput wording could violate M08 boundary. No issue; TSV keeps it `needs-evidence` and does not accept throughput as success.

Drop/Superseded Checks:
- Drops pass: only non-8X firmware rows are dropped; direct 8X recipe lines around vendor `filogic.mk:590-597` and device wrapper at `:655` select mt7996/mt7996-233 and `mt7988-wo-firmware`.
- Superseded pass: `000458`/`000468` are target-packaged in target mt76 Makefile lines `709` and `731`; `001107` matches target generic backport `733`; `001113` matches target generic backport `731`.

Boundary Checks:
- Pass overall: no basic wired, Wi-Fi association/runtime, MLO/AFC, NAND/eMMC/sysupgrade/storage, or throughput-only success is claimed.
- Needs-evidence rows generally state target/runtime evidence gaps and do not silently claim migration success.

Findings Ordered By Severity:
- High: `000350`, `M08-acceleration-and-offload.files.tsv:7`, should not be `review-only`. The patch `package/kernel/mt76/patches/0007-mtk-mt76-add-debug-tools.patch` is mostly debug/testmode, but it also changes real WED datapath/resource behavior: `mt76_token_consume()` offsets token allocation when WED is active, `mt76_wed_release_rx_buf()` drains WED RX page fragments, and WED offload enable/disable forces `MT76_WED_SW_TOKEN_SIZE`; see vendor patch around lines `31064-31160`. This row should be `needs-evidence` under M08, or split so the non-debug WED hunks are not hidden by the debug-tools disposition.

No-Issue Confirmations:
- Structural coverage is clean.
- Common high-risk rows, including all self-QC rows, are otherwise correctly conservative.
- Assigned low-risk rows pass.
- Superseded-by-target claims have same-semantic target evidence.
- Drops are not title-only drops of shared code; they are firmware package closure decisions.

Residual Risk:
- Large WED/RRO/HWRRO and PPE/HNAT patch stacks still require target 6.12/mt76 semantic comparison and runtime validation later. This audit found one disposition defect, not evidence of runtime success or failure.
