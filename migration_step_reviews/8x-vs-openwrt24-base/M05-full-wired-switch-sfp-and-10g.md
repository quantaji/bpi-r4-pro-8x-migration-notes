# Migration Step M05 Batch Review: Full Wired Switch, SFP, And 10G

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M05-full-wired-switch-sfp-and-10g.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M05-full-wired-switch-sfp-and-10g.files.tsv`

This review is part of Project Phase 2. It does not migrate code.

## Audit Status

This file is the M05 round-1-audited batch review.

Formal three-agent no-context audit status: completed for round 1 on 2026-06-11.

Reviewers: `M05-audit-round1-agent-1`, `M05-audit-round1-agent-2`, `M05-audit-round1-agent-3`.

Verdicts: `accept` / `accept` / `accept-with-minor-edits`.

Round-1 result: no blocking findings. The minor findings from agent 3 were accepted: `000958` was narrowed to non-802.1Q fallback/adjacent tag review-only, and `000869` wording was narrowed to avoid treating an RFB SFP/passive-mux/AQR DTS as direct 8X MxL switch/tag evidence.

## Formal No-Context Audit Results

| reviewer id | verdict | structural checks | findings summary | accepted/rejected changes |
| --- | --- | --- | --- | --- |
| `M05-audit-round1-agent-1` | `accept` | pass: 92 files, 254 assignments, no missing/extra/duplicate, JSON/TSV fields exact, legal disposition/owner | no actionable findings | no changes requested |
| `M05-audit-round1-agent-2` | `accept` | pass: 92 files, 254 assignments, no missing/extra/duplicate, JSON/TSV fields exact, legal disposition/owner | no actionable findings; noted step-file-index feature-order differences only | no changes requested |
| `M05-audit-round1-agent-3` | `accept-with-minor-edits` | pass: 92 files, 254 assignments, no missing/extra/duplicate, JSON/TSV fields exact, legal disposition/owner | minor wording/scope issues in `000958` and `000869` | accepted both minor edits |

## Review Purpose

M05 decides which vendor changes are needed for full wired hardware behavior on BPI-R4 Pro 8X: MxL86252 external DSA switch, MT7988 built-in switch interaction, AS21xxx 10G PHY closure, PCS/10GBase-R/USXGMII, SFP cages and hotplug, SFP/RJ45 mux behavior, and VLAN bridge behavior before acceleration.

M05 does not cover HNAT/PPE/WED/flow-offload, Wi-Fi, NAND/eMMC/sysupgrade/storage, MT7988 RFB or MT7987/R4Lite topology as 8X truth, or any runtime success claim.

## Input Scope

M05 by-step input contains 92 files and 254 feature assignments.

Status split:

| status | count |
| --- | ---: |
| `A` | 88 |
| `M` | 4 |

Route-class split:

| route class | count |
| --- | ---: |
| `primary` | 224 |
| `supporting` | 30 |

Feature split:

| feature | count |
| --- | ---: |
| `dts:overlay:network` | 30 |
| `firmware:phy:runtime` | 21 |
| `network:combo:gpio-mux` | 1 |
| `network:combo:runtime-switch` | 1 |
| `network:combo:sfp-rj45` | 1 |
| `network:dsa:switch` | 29 |
| `network:dsa:tagging` | 29 |
| `network:pcs:10gbase-r` | 9 |
| `network:pcs:usxgmii` | 9 |
| `network:phy:10gbase-t` | 29 |
| `network:phy:firmware` | 13 |
| `network:sfp:cage` | 11 |
| `network:sfp:hotplug` | 6 |
| `network:sfp:i2c` | 11 |
| `network:sfp:module-detect` | 11 |
| `network:switch:external-dsa` | 29 |
| `network:switch:vlan-offload` | 14 |

Strict TSV scope:

1. The TSV contains exactly the 92 files from the M05 by-step JSON.
2. M00/M01/M03/M04 handoffs are reviewed here when relevant but are not added as TSV rows unless they are also in the M05 JSON.
3. Direct 8X vendor source is authoritative. MT7988 RFB, MT7987, BPI-R4 Lite, MTK SDK, and target 25.12 are supporting or target-structure references only.

Prior-step handoff check:

1. M00 requires M05 to decide AS21xxx closure, prove or reject AQR/Aquantia applicability, and review MxL/SFP/PCS/DSA/10G patch groups.
2. M01 handed AS21xxx/AQR package closure and `000972` package-list implications to M05.
3. M03 handed direct 8X base DTS `000859`, AS21xxx rows `000040`-`000049`, AQR rows `000037`-`000039`, RFB wired references, and the GPIO4 `switch_hrstn` vs Wi-Fi `wifi_12v` conflict to M05.
4. M04 handed `000859`, RFB wired references, full-wired PCS/SFP/DSA rows, and `001124` to M05. M04 audit required `001124` to keep M05 multiple-DSA review while handing PPPQ/QDMA/PPE/WED/offload to M08.

## Direct 8X Evidence

Direct 8X base DTS:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`

Key evidence checked:

1. `sfp1` and `sfp2` are direct 8X SFP cages. `sfp1` uses I2C `imux1_sfp1`, LOS GPIO70, mod-def0 GPIO69, and TX-disable GPIO21. `sfp2` uses I2C `imux2_sfp2`, LOS GPIO2, mod-def0 GPIO1, and TX-disable GPIO0.
2. `gmac1` uses 10GBase-R through `phy28`; `gmac2` uses 10GBase-R fixed-link as the external DSA CPU path.
3. Direct 8X MDIO has AS21xxx/AN8831X-compatible C45 PHYs at addresses 24 and 28. Both set `firmware-name = "as21x1x_fw.bin"`.
4. The MxL86252 switch is `compatible = "mxl,86252"`, address 16, `dsa,member = <0 0>`, with CPU tag `mxl862_8021q`.
5. MxL user ports are `mxl_lan0`, `mxl_lan1`, `mxl_lan2`, `mxl_lan3`, and `mxl_lan5`; `mxl_lan4` is disabled.
6. MxL port 12 has a `mxl862xx,ds-mux` between SFP1 and AS21xxx PHY24. The SoC Ethernet mux switches `gmac1` between AS21xxx PHY28 and SFP2. These muxes share the same mod-def0 GPIOs as their SFP cages.
7. The built-in MT7988 switch is enabled with `dsa,member = <1 0>`, so M05 has a multiple-DSA topology.
8. GPIO4 is a hogged high reset for the MxL86252 switch. M03 noted that the Wi-Fi overlay also wants GPIO4 as `wifi_12v`; M05 must keep that conflict visible for M06.

Package and target evidence:

1. The vendor 8X image recipe includes `kmod-sfp` but does not include vendor `phy-as21xxx` or `as21xxx-firmware` packages.
2. Target 25.12 provides `kmod-phy-aeonsemi-as21xxx` and `aeonsemi-as21xxx-firmware`; target firmware installs `as21x1x_fw.bin` under `/lib/firmware`, matching the direct 8X DTS firmware-name.
3. AQR firmware/package files exist in the vendor tree, but no direct 8X DTS node binds AQR/CUX. AQR remains evidence-gated.
4. Target 25.12 has MT7988 switch-node support and filogic config enables target-style MT7530/MMIO DSA support.
5. Target 25.12 does not appear to provide an MxL86252 DSA driver or MxL86252 DSA tag protocol, so MxL support remains an M05 rewrite item.

## Routing Conclusions

1. `000859` is the direct 8X wired topology authority. M05 uses it as `static-only` topology evidence and does not claim runtime success.
2. `000040`-`000049` prove AS21xxx closure is required, but vendor AS21xxx source/package is superseded by target 25.12 packages.
3. `000037`-`000039`, AQR RFB overlays, and AQR/Aquantia patches remain `needs-evidence` or supporting only because direct 8X DTS names AS21xxx, not AQR/CUX.
4. MT7987 and BPI-R4 Lite files are dropped from 8X M05 migration. MT7988 RFB wired overlays are review-only supporting references.
5. MxL86252 driver, selected direct 8X DSA tag path, kernel integration, passive mux, shared mod-def0 handling, and selected PCS behavior are M05 rewrite inputs; the non-802.1Q `mxl862` tag path is review-only unless the final driver design requires fallback or shared support.
6. Target-superseded generic backports are not migrated from vendor 6.6 patches.
7. DSA netlink/debug, AN8855 netlink, SFP debug-only patches, and non-8X PHY updates are dropped unless later runtime debugging explicitly reopens them.
8. DSA flow-table offload and PPPQ/QDMA/PPE/WED/offload hunks are handed to M08.
9. No M05 row declares SFP, DSA, MxL, AS21xxx, 10G, VLAN, or combo mux runtime success.

## Disposition Summary

| disposition | count |
| --- | ---: |
| `defer` | 1 |
| `drop` | 24 |
| `needs-evidence` | 15 |
| `review-only` | 14 |
| `rewrite` | 21 |
| `static-only` | 1 |
| `superseded-by-target` | 16 |

Owner-step summary:

| owner_step | count |
| --- | ---: |
| `M05` | 91 |
| `M08` | 1 |

Group summary:

| group | count |
| --- | ---: |
| `air-en8811h-non-8x` | 1 |
| `an8855-netlink-non-8x` | 3 |
| `aqr-aquantia-needs-evidence` | 7 |
| `aqr-firmware-needs-evidence` | 3 |
| `as21xxx-target-package-closure` | 10 |
| `direct-8x-full-wired-topology` | 1 |
| `dsa-flow-offload-boundary` | 1 |
| `dsa-netlink-debug-nonessential` | 1 |
| `ethernet-passive-mux` | 1 |
| `fs-copper-sfp-needs-evidence` | 1 |
| `mt7531-finetune-non-8x` | 1 |
| `mt753x-ageing-tweak-needs-evidence` | 1 |
| `mt753x-gsw-target-structure` | 1 |
| `mt7988-rfb-an8831x-reference` | 2 |
| `mt7988-rfb-aqr-cux-reference` | 4 |
| `mt7988-rfb-mxl-sfp-reference` | 3 |
| `mt7988-rfb-soc-wired-reference` | 4 |
| `mtk-eth-non-dsa-event-handling` | 1 |
| `multiple-dsa-with-offload-risk` | 1 |
| `mxl86252-built-in-phy-support` | 1 |
| `mxl86252-driver-and-tag` | 10 |
| `mxl86252-kernel-integration` | 2 |
| `non-8x-mt7987-network-reference` | 14 |
| `non-8x-mt7987-pcs-support` | 1 |
| `non-8x-mt7987-sfp-r4lite-reference` | 2 |
| `pcs-lynxi-autoneg-power` | 3 |
| `pcs-polarity-needs-evidence` | 1 |
| `pcs-xfi-tphy-reset` | 2 |
| `sfp-checksum-war-needs-evidence` | 1 |
| `sfp-debug-info` | 1 |
| `sfp-rollball-module-needs-evidence` | 1 |
| `sfp-shared-mod-def0` | 1 |
| `target-superseded-eee-backport` | 1 |
| `target-superseded-eee-fixup` | 1 |
| `target-superseded-mt7988-dts-pcs` | 1 |
| `target-superseded-phya-clock-path` | 1 |
| `target-superseded-sfp-backport` | 1 |

## Secondary Review Handoffs

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `000859` | `M05` static topology evidence | `M03`, `M06`, `M09`, `M10` | M05 owns full wired topology review; M03 owns board DTS identity/static services, M06 owns GPIO4 Wi-Fi conflict, M09 owns USB/PCIe/fan extras, and M10 owns storage/rootdisk/env content in the same DTS. |
| `000960`, `000963` | off-matrix M04 evidence | `M05` | board.d/static network config confirms LAN/WAN names but does not prove DSA/SFP/10G runtime behavior. |
| `001003` | off-matrix M03/M04 evidence | `M05` | Factory MAC offset polarity supports interface identity but is not an M05 by-step row. |
| `001026`, `001068` | `M05` | `M04` prerequisite only | passive mux and shared mod-def0 behavior depends on basic Ethernet and board defaults but is full-wired work. |
| `001054` | `M08` | `M05` prerequisite only | DSA flow table offload must wait for working full wired paths. |
| `001124` | `M05` | `M08`, `M04` prerequisite only | multiple DSA switch behavior belongs to M05; PPPQ/QDMA/PPE/WED/offload hunks require M08 review before acceleration is enabled. |
| `000858` | off-matrix M06 | `M05` | Wi-Fi overlay GPIO4 `wifi_12v` conflicts with direct 8X MxL86252 `switch_hrstn` GPIO hog. |
| AQR rows `000037`-`000039`, `001000`-`001002`, `001064`-`001066`, `001083` | `M05` needs-evidence | none | M05 must prove or reject AQR/CUX applicability; RFB references cannot decide 8X hardware truth. |

## TODOs

1. Migration Step M05: validate direct 8X multiple-DSA topology from `000859`, including built-in switch member `<1 0>` and external MxL86252 member `<0 0>`.
2. Migration Step M05: use target 25.12 `kmod-phy-aeonsemi-as21xxx` and `aeonsemi-as21xxx-firmware` for AS21xxx closure; verify PHY24/PHY28 firmware load and link modes at runtime.
3. Migration Step M05: prove or reject AQR/CUX applicability before migrating any AQR firmware or Aquantia-specific patch.
4. Migration Step M05: port/rewrite MxL86252 DSA driver, direct 8X `mxl862_8021q` DSA tag protocol, and built-in PHY support against target 6.12 APIs; review the non-802.1Q `mxl862` tag path only if the selected driver design needs fallback/shared support.
5. Migration Step M05: verify SFP1 and SFP2 separately for I2C, mod-def0/module detect, TX-disable/LOS, link, and hotplug behavior with the available module.
6. Migration Step M05: validate SFP/RJ45 combo mux switching for both AS21xxx copper paths and SFP paths, including shared mod-def0 GPIO handling.
7. Migration Step M05: validate VLAN bridge behavior before enabling any acceleration or offload.
8. Migration Step M05/M06: resolve or explicitly document GPIO4 ownership between MxL86252 `switch_hrstn` and Wi-Fi `wifi_12v` before both are enabled.
9. Migration Step M08: review DSA hardware flow-table offload and `001124` PPPQ/QDMA/PPE/WED/offload hunks only after M05 full wired behavior is stable.
10. Migration Step M10: keep NAND/eMMC/sysupgrade/storage semantics out of M05 even when the same DTS or image context mentions storage nodes.

## Unreported Minimalism Gate

Gate result: pass for round-1-audited review.

Checks performed:

1. Direct 8X `000859` was read before deciding MxL86252, AS21xxx, SFP, mux, built-in switch, and GPIO4 conclusions.
2. MT7988 RFB, MT7987, and R4Lite files were not used as direct 8X hardware truth.
3. Vendor AQR package/patches were not migrated from package presence or RFB references; AQR remains evidence-gated.
4. Vendor AS21xxx package/source was not copied merely because direct DTS needs AS21xxx; target 25.12 package and firmware closure was checked.
5. MxL86252 driver/tag files were not dropped from target absence alone; direct DTS compatible/tag evidence was checked, and the non-802.1Q `mxl862` tag path was not promoted beyond review-only fallback evidence.
6. Debug/netlink and module-specific SFP quirks were not promoted to hardware support without direct module evidence.
7. Offload and acceleration pieces were handed to M08 instead of being pulled into M05.
8. Every `defer`, `static-only`, and `needs-evidence` row has a named owner and actionable TODO in the TSV notes and this markdown.
9. No row claims runtime success for DSA, SFP, 10G, AS21xxx, MxL86252, VLAN, or combo mux behavior.

## Remaining Risk

M05 round-1 formal no-context audit is complete. Residual risks are implementation-time and runtime-validation risks, not review-acceptance blockers.

M05 implementation-time risk remains for target 6.12 API fit of the MxL86252 driver/tag, AS21xxx firmware/package selection, PHY24/PHY28 runtime firmware load, SFP module quirks, shared mod-def0 GPIO behavior, multiple-DSA queue mapping, VLAN bridge correctness, and whether any AQR/CUX path exists on actual 8X hardware. Later-step risks are explicitly deferred to M06 for GPIO4 Wi-Fi conflict, M08 for acceleration/offload, M09 for board extras, and M10 for storage/sysupgrade.
