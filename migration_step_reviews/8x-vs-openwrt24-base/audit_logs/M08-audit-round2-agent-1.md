# M08 Audit Round 2 Agent 1 Raw Report

Verdict: accept-with-minor-edits

Evidence Read:
- Audit targets: `migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.md`, `.files.tsv`
- Routing inputs: `.../by-step/M08-acceleration-and-offload.json`, `.../summary/step-file-index.tsv`
- Diffset base inspected: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/`
- Inspected diff/source evidence for all common high-risk rows, assigned rows, and self-selected rows, including:
  - `package/kernel/linux/modules/netfilter.mk.patch`
  - `package/kernel/mt76/Makefile.patch`
  - mt76 patches: `0003`, `0007`, `0009`, `0013`, `0025`, `0031`, `0032`, `0050`, `0057`, `0063`, `0078`, `0083`
  - firmware binary diff entries: `mt7990_wm.bin`, `mt7990_wm_tm.bin`, `mt7992_wm_23.bin`, `mt7992_wm_tm.bin`, `mt7996_dsp.bin`, `mt7996_wm_233.bin`
  - HNAT files: `hnat.c`, `hnat.h`, `hnat_debugfs.c`, `hnat_mcast.c`, `hnat_nf_hook.c`, `hnat_stag.c`, `nf_hnat_mtk.h`, `ra_nat.h`
  - mediatek kernel patches: `999-2709`, `999-2710`, `999-2711`, `999-2720`, `999-2741`, `999-2742`, `999-2743`, `999-2745`, `999-2746`, `999-2747`, `999-3000`, `999-3001`, `999-3004`, `999-3013`, `999-3014`, `999-3015`, `999-3020`, `999-3026`, `999-3029`, `999-3031`, `999-3032`, `999-4100`
- Direct vendor source inspected: 8X `.config`, `target/linux/mediatek/image/filogic.mk`, `package/kernel/mt76/Makefile`, MT7988/WED DTS evidence.
- Target 25.12 inspected: `package/kernel/mt76/Makefile`, `package/firmware/linux-firmware/mediatek.mk`, `package/kernel/linux/modules/netfilter.mk`, `target/linux/mediatek/patches-6.12/198-dts-mt7988a-enable-wed.patch`, generic backports `731-v6.18...MT7992-WED...patch` and `733-v6.18...GFP_DMA32...patch`.

Structural Checks:
- PASS: JSON file count is 87 actual / 87 stated.
- PASS: JSON assignment count is 165 actual / 165 stated.
- PASS: TSV has 87 rows and 87 unique `file_id`s.
- PASS: no missing, extra, or duplicate `file_id`.
- PASS: exact match for `status`, `path`, `file_kind`, `features`, and `route_classes`.
- PASS: TSV disposition counts match markdown summary: `needs-evidence=60`, `defer=10`, `review-only=9`, `drop=4`, `superseded-by-target=4`.

Common High-Risk Findings:
- No blocking issue found.
- The conservative `needs-evidence` treatment is correct for WED/RRO/HWRRO shared-code rows such as `000350`, `000374`, `000375`, `000400`, `000421`, `000426`, `001116`, `001118`, and `001119`; patch bodies contain runtime/shared code, not just debug/title-only or non-8X material.
- `001107` and `001113` superseded-by-target claims are supported by target 25.12 backports with same-semantic GFP_DMA32/dma-mask and MT7992-on-MT7988 second WDMA RX ring support.
- Non-8X firmware drops `000441`, `000442`, `000455`, `000456` are not title-only code drops; they are binary firmware rows not selected by direct 8X package closure. Target 25.12 independently packages some non-8X firmware, but that does not make it an 8X migration requirement.

Assigned Low-Risk Findings:
- `001091`: correct `needs-evidence`; patch adds DSCP learning into xt flow offload/PPE path.
- `000406`: correct M07 defer; EPCS is vendor command/MCU/EHT policy, not M08 offload enablement.
- `000356`: correct M07 defer; TX/RX rate reporting via MCU is telemetry/wireless behavior, not WED/PPE enablement.
- `001100`: correct `needs-evidence`; PPE cache preserved-line lock is flow-offload implementation detail.
- `001019`: correct review-only; safexcel AEAD 3DES/MD5 crypto expansion has no proven M08 network offload dependency.
- `000352`: correct M07 defer; EMLSR is MLO policy/runtime.
- `000393`: correct review-only; debug API relocation does not prove or gate WED/RRO runtime.

Self-Selected Rows and Findings:
- Selected `000346` because it is a compact WED attach failure patch. Finding: correct `needs-evidence`; it clears `wed_enable` and `dev->has_rro` on attach failure.
- Selected `000368` because it is a large HWRRO/RRO split. Finding: correct `needs-evidence`; it adds RX token/page-pool/RRO indication handling.
- Selected `001088` because terse debugfs wording could hide behavior. Finding: correct `needs-evidence`; it is mostly internal PPE debugfs visibility, but target comparison is appropriate.
- Selected `001102` because WDMA/nft integration is terse but high-impact. Finding: correct `needs-evidence`; patch adds `DEV_PATH_MTK_WDMA` to `nft_flow_offload`.
- Selected `001116` because debugfs title could hide runtime changes. Finding: correct `needs-evidence`; patch changes `mtk_wed_rx_reset` polling and `mtk_wed_attach` revision handling outside debugfs.

Drop/Superseded Checks:
- PASS: all `drop` rows are firmware binaries not selected by direct 8X image/package evidence; no generic/shared/MT7988-adjacent source code is hidden under drop.
- PASS: all `superseded-by-target` rows checked against target 25.12 same-semantic evidence: `000458`, `000468`, `001107`, `001113`.

Boundary Checks:
- PASS: M08 does not claim basic wired success, Wi-Fi runtime success, MLO/AFC success, storage/sysupgrade/install success, or throughput-only acceptance.
- PASS: `needs-evidence` rows consistently state evidence gaps and avoid silent migration/runtime success claims.

Findings Ordered By Severity:
- Minor: `M08-acceleration-and-offload.md:7` says "No second audit round has been launched." That is stale once this round2 audit is incorporated. Update the status sentence after coordinator aggregation.
- No blocking findings.

No-Issue Confirmations:
- Remediation rows `000350`, `000374`, `000375`, `000400`, `000421`, `000426`, `001063`, `001113`, `001116`, and `001118` are correctly handled after patch-body inspection.
- Direct 8X `.config` enables flowtable/nf-flow-netlink packages but leaves `kmod-mediatek_hnat` unset; M08 correctly treats this as config evidence, not hardware/runtime proof.
- Target 25.12 has WED DTS/backport/package support, but the matrix does not overclaim runtime offload success.

Residual Risk:
- High residual implementation risk remains in later M08 work because many WED/PPE/HNAT/netfilter patches require hunk-by-hunk target 6.12 comparison and runtime validation. No audit-target issue requires rejection.
