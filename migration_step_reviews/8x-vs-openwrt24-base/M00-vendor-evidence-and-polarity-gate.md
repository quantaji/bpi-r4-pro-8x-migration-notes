# Migration Step M00 Batch Review: Vendor Evidence And Polarity Gate

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M00-vendor-evidence-and-polarity-gate.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M00-vendor-evidence-and-polarity-gate.files.tsv`

This review is part of Project Phase 2. It does not migrate code.

## Review Purpose

Migration Step M00 turns broad/noisy feature routing into a safer evidence matrix
for later migration steps.

M00 answers:

1. which files are direct 8X evidence,
2. which files are supporting vendor-family or MTK SDK evidence,
3. which files are broad routing noise,
4. which later migration step owns each non-M00 follow-up,
5. which files can be dropped from migration review.

## Input Scope

M00 contains 289 files and 417 feature assignments.

Status split:

| status | file count |
| --- | ---: |
| `A` | 259 |
| `D` | 25 |
| `M` | 5 |

Feature split:

| feature | route class | assignment count |
| --- | --- | ---: |
| `dts:soc:base` | `review-only` | 187 |
| `network:phy:generic` | `review-only` | 80 |
| `network:phy:multi-rate` | `review-only` | 123 |
| `source:tree:metadata` | `primary` | 26 |
| `source:feeds:base-feed-config` | `primary` | 1 |

## Direct 8X Evidence

Direct 8X base DTS:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`

Key evidence checked:

1. `compatible = "bananapi,bpi-r4-pro-8x", "mediatek,mt7988a"`,
2. SFP1 and SFP2 cages are present,
3. external Airoha AN8831X PHY nodes use `firmware-name = "as21x1x_fw.bin"`,
4. MxL86252 switch node is present with `dsa-tag-protocol = "mxl862_8021q"`,
5. direct board DTS combines M03 board identity, M05 wired hardware, M09 board extras, and M10 storage context.

Conclusion: direct 8X DTS is primary evidence, but it is not migrated in M00.
Later migration steps own the actual implementation.

Direct 8X image recipe evidence:

`target/linux/mediatek/image/filogic.mk`

Key evidence checked:

1. the 8X profile includes `kmod-sfp`, hardware monitor, I2C mux, EEPROM, RTC, USB, Wi-Fi firmware, and storage tools,
2. the 8X profile does not explicitly include `phy-as21xxx`, `as21xxx-firmware`, or `aqr10g-phy-firmware` in the checked vendor recipe,
3. M05 must decide whether package closure needs to add AS21xxx driver/firmware and whether AQR firmware is applicable.

Direct 8X PHY package evidence:

`package/kernel/as21xxx`

Key evidence checked:

1. package defines `kmod-phy-as21xxx`,
2. package defines `as21xxx-firmware`,
3. firmware install path provides `as21x1x_fw.bin`,
4. direct 8X base DTS names `as21x1x_fw.bin` on external AN8831X PHY nodes.

Conclusion: AS21xxx package files are deferred to Migration Step M05.

## Disposition Summary

The TSV review matrix assigns one disposition per M00 file.

| disposition | file count | meaning in M00 |
| --- | ---: | --- |
| `drop` | 26 | Repo metadata/README only; no migration input. |
| `review-only` | 86 | Evidence or background only; do not migrate from M00. |
| `needs-evidence` | 10 | AQR/Aquantia applicability must be proven in M05. |
| `defer` | 167 | Later migration step owns the actual review and migration decision. |

Owner split:

| owner step | file count | reason |
| --- | ---: | --- |
| `M00` | 112 | Metadata drops plus evidence-only references. |
| `M05` | 72 | PHY, switch, PCS, SFP, DSA, and 10G evidence. |
| `M08` | 52 | Offload, WED, PPE, HNAT, tunnel, and crypto acceleration. |
| `M04` | 26 | Ethernet MAC, MDIO, and basic wired behavior. |
| `M09` | 12 | PCIe, USB, thermal, PWM, and board extras. |
| `M10` | 8 | Storage, rootfs, dual-boot, and flash policy. |
| `M03` | 5 | SoC/board foundation dependencies. |
| `M02` | 1 | FIT ramdisk/rootfs behavior needed for SD/recovery boot review. |
| `M06` | 1 | Wi-Fi PCIe reset path. |

## Evidence Groups

| group | count | disposition pattern |
| --- | ---: | --- |
| `source-metadata` | 26 | `drop` |
| `feed-baseline` | 1 | `review-only` |
| `direct-8x-board-dts` | 1 | `review-only` |
| `direct-8x-phy-package` | 10 | `defer` to `M05` |
| `aqr-firmware-reference` | 3 | `needs-evidence` in `M05` |
| `aqr-or-10g-phy-patch` | 7 | `needs-evidence` in `M05` |
| `mt7988-rfb-reference` | 14 | `review-only` |
| `mt7987-reference` | 33 | `review-only` |
| `phy-driver-reference` | 35 | `review-only` |
| `wired-phy-switch-patch` | 52 | `defer` to `M05` |
| `ethernet-mac-patch` | 26 | `defer` to `M04` |
| `acceleration-patch` | 52 | `defer` to `M08` |
| `storage-policy-patch` | 8 | `defer` to `M10` |
| `board-extras-patch` | 6 | `defer` to `M09` |
| `soc-foundation-patch` | 5 | `defer` to `M03` |
| `pcie-expansion-patch` | 6 | `defer` to `M09` |
| `wifi-pcie-patch` | 1 | `defer` to `M06` |
| `debug-diagnostics-reference` | 1 | `review-only` |
| `crypto-security-reference` | 1 | `review-only` |
| `fitblk-recovery-rootfs-patch` | 1 | `defer` to `M02` |

## Routing Conclusions

1. Repo metadata and the README banner are safe to drop from migration review.
2. `feeds.conf.default` is provenance evidence only. It records vendor feed pins and external feeds, but M01 must use a clean target feed strategy.
3. Direct 8X base DTS is the key cross-step evidence file. It must be read by M03, M05, M09, and M10 before implementation.
4. AS21xxx driver/firmware files are directly relevant because the 8X DTS names `as21x1x_fw.bin`.
5. AQR/Aquantia files and patches are not proven direct 8X requirements in M00. They are assigned `needs-evidence` for M05.
6. MT7987 and BPI-R4 Lite files are vendor-family/SDK references only. They must not decide 8X hardware behavior.
7. MT7988 RFB files are supporting evidence only. Direct 8X source remains the authority.
8. Broad kernel patch stacks were split by subject into M04, M05, M08, M09, M10, M03, or review-only buckets.

## Audit Corrections

M00 quality audit corrected mechanical keyword false positives before
handoff to later migration steps:

1. `000994` and `001078` moved from M08 to M05 after content check; both are PHY/SFP patches, not acceleration patches.
2. `001054` moved from M05 to M08 because it adds DSA hardware flow table offload.
3. `001018` and `001044` moved from M05 to M04 because they modify `mtk_eth_soc` MDIO/basic Ethernet MAC handling.
4. `001146`, `001147`, and `001148` moved from M05 to M09 because MediaTek TPHY/PCIe patches are expansion PHY work, not Ethernet PHY work.

An independent full-file audit agent then reviewed all 289 TSV rows and graded
the pre-correction M00 matrix as medium quality. The audit found that several
flow/offload dependencies were still hidden in `review-only` M00 buckets. The
matrix was corrected as follows:

1. `001050`, `001051`, `001052`, `001053`, `001055`, `001093`, `001101`, `001103`, and `001105` moved from M00 network-stack review-only to M08 acceleration review.
2. `001048` moved to M08 as an explicit PPTP/tunnel-offload applicability decision point.
3. `001059` moved to M08 because it exports a hook used by the vendor HNAT path.
4. `001111` moved to M08 because it modifies `mtk_wed.c`.
5. `001141` moved to M10 because it touches SPI-NAND/SPI calibration behavior.
6. `001008` moved from M09 to M00 review-only because the patch is MT7987 PWM breathing-light support, not proven 8X board-extra behavior.
7. `001003` and `001114` stayed M00 review-only but were reclassified as MT7988 RFB references instead of broad kernel patches.

Two additional blind full-file audit agents then reviewed M00 from no forked
context. Both graded the pre-correction matrix as medium quality and found
more owner-routing holes. Those findings were applied as follows:

1. `000973` moved to M08 because MTK evidence ties optional TCP window check to an MT7988 HNAT unbind fix.
2. `001017` and `001019` moved to M08 because direct 8X inherits the MT7988 Safexcel EIP197 crypto node, while M08 owns crypto acceleration only if required and justified.
3. `001063` moved to M08 because the patch adds HNAT/TOPS tunnel descriptor helpers in `mtk_eth_soc.h`; the crypto filename was misleading.
4. `001134` moved to M02 because FIT ramdisk/rootfs parsing can affect SD/recovery boot before onboard install work.
5. `001124` remains M05 primary owner for DSA/switch behavior, but the TSV notes now require M08 to review its PPE/WED/offload hunks before acceleration is enabled.

## Secondary Review Handoffs

The TSV schema has one `owner_step` per file. Mixed-owner files are therefore
kept under their primary owner and must be called out explicitly here.

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `001124` | `M05` | `M08` | Multiple-DSA-switch fix also touches `mtk_ppe`, `mtk_ppe_offload`, and WED flow paths. |

## TODOs

1. Migration Step M01: choose target 25.12 feed policy explicitly; do not copy vendor `feeds.conf.default`.
2. Migration Step M02: review `001134` before SD/recovery FIT rootfs boot validation; defer persistent install implications to M10.
3. Migration Step M03: read direct 8X base DTS before board identity, GPIO, I2C, factory data, and SoC foundation work.
4. Migration Step M04: review M00 `ethernet-mac-patch` files before basic wired bring-up.
5. Migration Step M05: verify AS21xxx driver/firmware package closure against direct 8X DTS and runtime PHY enumeration.
6. Migration Step M05: verify whether AQR/Aquantia firmware or patches apply to any actual 8X 10G copper path.
7. Migration Step M05: review MxL86252, SFP, PCS, DSA, and 10G patch groups before full wired migration.
8. Migration Step M06: inspect Wi-Fi PCIe reset patch only if basic Wi-Fi hardware bring-up needs it.
9. Migration Step M08: review acceleration/offload patches, including generic flow-table, nft flow offload, HNAT hook, PPTP/tunnel, WED, EIP197 crypto, and mixed-owner PPE/WED dependency patches, only after base wired and Wi-Fi behavior is correct.
10. Migration Step M09: review PCIe, USB, TPHY, PWM, and thermal patches after core boot/networking is stable.
11. Migration Step M10: review storage/rootfs/dual-boot patches only after SD boot and runtime hardware are stable.

## Unreported Minimalism Gate

Result: passed after content-check corrections for this M00 triage pass.

Minimalism risks checked:

1. Hardware files were not dropped from filename alone.
2. Direct 8X DTS was inspected before classifying AS21xxx, SFP, and MxL evidence.
3. AQR/Aquantia files were not treated as direct 8X requirements without proof.
4. MT7987 and RFB files were kept as supporting references, not copied as 8X hardware truth.
5. Broad `dts:soc:base` and `network:phy:*` tags were split into later owner steps instead of being treated as one migration cluster.
6. Substring false positives were checked and corrected instead of being silently accepted.
7. Independent full-file audit findings were applied before treating M00 as a handoff matrix.
8. Two blind no-context audits were run after the first correction pass, and their confirmed findings were applied.

Remaining risk:

The M00 TSV is a routing/evidence matrix. Later migration steps must still inspect their assigned files before making `migrate`, `rewrite`, or `drop` decisions.
