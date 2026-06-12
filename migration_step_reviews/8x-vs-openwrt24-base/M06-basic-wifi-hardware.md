# Migration Step M06 Batch Review: Basic Wi-Fi Hardware

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M06-basic-wifi-hardware.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M06-basic-wifi-hardware.files.tsv`

This review is part of Project Phase 2. It does not migrate code, build images, or claim Wi-Fi runtime success.

## Audit Status

This file is the M06 round-1-audited batch review.

Formal three-agent no-context audit status: completed on 2026-06-12.

Round-1 formal no-context audit reviewers:

| reviewer id | verdict | structural checks | findings summary |
| --- | --- | --- | --- |
| `M06-audit-round1-agent-1` | `accept` | pass: 155/155 rows, 371 assignments, no missing/extra/duplicate, JSON parity, legal disposition/owner, TODO coverage | no actionable findings |
| `M06-audit-round1-agent-2` | `accept` | pass: 155/155 rows, 371 assignments, no missing/extra/duplicate, JSON parity, legal disposition/owner, TODO coverage | no actionable findings |
| `M06-audit-round1-agent-3` | `accept` | pass: 155/155 rows, 371 assignments, no missing/extra/duplicate, JSON parity, legal disposition/owner, TODO coverage | no actionable findings |

Sampling plan: common high-risk rows were checked by all reviewers; each reviewer also checked 7 coordinator-assigned low-risk rows from randomized seed `16058559765735391962` and 5 self-chosen low-risk rows. Accepted changes: none required after audit. Rejected changes: none.

## Scope / Non-goals

M06 covers direct 8X basic Wi-Fi hardware bring-up evidence only: PCIe Wi-Fi NIC topology, Wi-Fi power/regulator behavior, mt7996 driver and firmware package closure, calibration/EEPROM/MAC source selection, and the minimum hotplug context needed for radio detection.

M06 does not cover MLO/AFC/6 GHz policy, full hostapd/mac80211/netifd policy, WED/HWRRO/PPE/HNAT/offload, generic PCIe expansion behavior, NAND/eMMC/install/sysupgrade/storage, or runtime success claims. A Wi-Fi 6 association test is the intended M06 exit direction after implementation, but this review does not claim that test has passed.

Evidence order used here: direct 8X vendor source first, vendor-family/RFB/MT7987/R4Lite as supporting only, and target OpenWrt 25.12 only for target package/API or superseded-by-target decisions.

## Structural Summary

M06 by-step input contains 155 files and 371 feature assignments.

Status split:

| status | count |
| --- | ---: |
| `A` | 145 |
| `M` | 10 |

Route-class assignment split:

| route class | count |
| --- | ---: |
| `primary` | 364 |
| `supporting` | 7 |

Feature split:

| feature | count |
| --- | ---: |
| `bus:pcie:controller` | 20 |
| `dts:overlay:wifi` | 6 |
| `firmware:wifi:eeprom` | 34 |
| `firmware:wifi:runtime` | 34 |
| `identity:calibration:wifi` | 34 |
| `openwrt:hotplug:wifi` | 7 |
| `wireless:calibration:eeprom` | 34 |
| `wireless:mt76:driver` | 128 |
| `wireless:mt76:eeprom` | 34 |
| `wireless:mt76:firmware` | 34 |
| `wireless:pcie:nic` | 6 |

Disposition summary:

| disposition | count |
| --- | ---: |
| `defer` | 62 |
| `drop` | 20 |
| `needs-evidence` | 16 |
| `review-only` | 26 |
| `rewrite` | 1 |
| `static-only` | 1 |
| `superseded-by-target` | 29 |

Owner-step summary:

| owner_step | count |
| --- | ---: |
| `M06` | 93 |
| `M07` | 55 |
| `M08` | 6 |
| `M09` | 1 |

Topic/group summary:

| group | count |
| --- | ---: |
| `M06-A-direct-8x-base-wifi-topology` | 1 |
| `M06-A-direct-8x-wifi-overlay` | 1 |
| `M06-A-mt7988-rfb-wifi-pcie-reference` | 5 |
| `M06-A-non-8x-mt7987-r4lite-dts` | 9 |
| `M06-D-firmware-target-closure` | 28 |
| `M06-D-mt76-package-closure` | 1 |
| `M06-D-testmode-or-unused-firmware` | 5 |
| `M06-E-mt76-advanced-mac-policy-handoff` | 3 |
| `M06-E-mt76-basic-bringup-needs-evidence` | 13 |
| `M06-E-mt76-beacon-mbssid-policy-handoff` | 7 |
| `M06-E-mt76-calibration-tooling-review-only` | 1 |
| `M06-E-mt76-debug-testmode-review-only` | 20 |
| `M06-E-mt76-dfs-csa-policy-handoff` | 7 |
| `M06-E-mt76-mlo-afc-policy-handoff` | 14 |
| `M06-E-mt76-non8x-or-unused-path` | 6 |
| `M06-E-mt76-offchannel-policy-handoff` | 1 |
| `M06-E-mt76-offload-wed-handoff` | 6 |
| `M06-E-mt76-preamble-puncture-policy-handoff` | 1 |
| `M06-E-mt76-qos-scs-policy-handoff` | 4 |
| `M06-E-mt76-rate-control-policy-handoff` | 2 |
| `M06-E-mt76-regulatory-power-policy-handoff` | 6 |
| `M06-E-mt76-vendor-cert-policy-handoff` | 3 |
| `M06-F-pcie-controller-needs-evidence` | 1 |
| `M06-F-pcie-controller-policy-handoff` | 1 |
| `M06-F-pcie-soft-onoff-needs-evidence` | 1 |
| `M06-F-wifi-pcie-reset-needs-evidence` | 1 |
| `M06-G-hotplug-userspace-boundary` | 7 |

Strict TSV scope:

1. The TSV contains exactly the 155 files from the M06 by-step JSON.
2. `status`, `path`, `file_kind`, `route_classes`, and `features` are copied exactly from the by-step JSON.
3. M00/M01/M03/M05 handoffs are reviewed where relevant but are not added as TSV rows unless they are in the M06 JSON.
4. No row uses filename-only disposition; rows are based on direct 8X DTS/DTSO, target mt76 Makefile/package evidence, patch subjects/content keywords, and migration-step boundaries.

## Topic/Substep Summary

### M06-A Direct 8X Wi-Fi Hardware Topology

Direct 8X base DTS `000859` enables PCIe controllers and contains a `pcie0` child `mt7996@0,0` with `compatible = "mediatek,mt76"` and `mediatek,mtd-eeprom = <&factory 0x0>`. The direct 8X Wi-Fi overlay `000858` adds `pcie0` and `pcie1` `mediatek,mt76` child nodes with `nvmem-cell-names = "mac-address"` sourced from AT24 cells.

M06 routes `000858` as `rewrite` and `000859` as `static-only`. M03 still owns the base DTS rewrite, but M06 owns Wi-Fi node semantics and must decide how the overlay should merge with or restructure the base `pcie0` Wi-Fi node.

MT7987, R4Lite, and RFB Wi-Fi/PCIe DTS rows are not direct 8X authority. MT7987/R4Lite rows are dropped; MT7988 RFB rows are review-only supporting references.

### M06-B Power / Regulator / GPIO Conflict

The direct 8X Wi-Fi overlay adds a fixed `wifi_12v` regulator on GPIO4. The direct 8X base DTS already hogs GPIO4 as `switch_hrstn` for the MxL86252 switch reset. This is a hard M05/M06 cross-step conflict and cannot be silently skipped under a minimal principle.

M06 records the conflict in `000858`, `000859`, and the secondary handoffs. The review does not choose a runtime GPIO owner. TODO: implementation must prove actual board wiring and choose a safe target DTS representation before enabling both Wi-Fi power and MxL86252 reset behavior.

### M06-C EEPROM / Calibration / MAC Identity

M06 separates four concepts:

1. AT24 EEPROM MAC address cells from `000858` at I2C addresses `0x51` and `0x52`,
2. factory MTD Wi-Fi calibration from `000859` through `mediatek,mtd-eeprom = <&factory 0x0>`,
3. mt7996 firmware/eeprom binary packages from mt76,
4. nvmem `mac-address` cells consumed by the overlay Wi-Fi nodes.

High-risk mismatch: `000858` targets `&i2c_wifi`, while `000859` labels the mux channel `imux3_wifi` and only aliases it as `i2c6`. The base DTS also already has `wifi_eeprom@51`, while the overlay adds another `wifi_eeprom@51` with nvmem-layout. M06 must resolve target label, duplicate node, and merge/replace/restructure policy before implementation.

mt76 EEPROM/nvmem/efuse patches that may affect calibration loading are marked `needs-evidence` rather than blindly ported from the vendor stack.

### M06-D Firmware / Package Closure

Direct 8X image evidence selects `kmod-eeprom-at24`, `kmod-mt7996-firmware`, and `kmod-mt7996-233-firmware`. Target 25.12 mt76 Makefile is newer than the vendor Makefile and already defines `kmod-mt7996e`, `kmod-mt7996-firmware`, and `kmod-mt7996-233-firmware`.

Firmware binaries installed by target 25.12 packages are marked `superseded-by-target`. Vendor `*_wm_tm*.bin` testmode binaries are dropped from M06 because target does not install them and direct 8X basic bring-up evidence does not require testmode firmware. Non-8X mt7990/mt7992 firmware rows are not treated as 8X hardware proof even when target provides those packages.

### M06-E mt76 Driver Patch Triage

The vendor mt76 patch stack is broad and is not copied into M06. M06 accepts only evidence needed for basic radio probe, firmware load, calibration source selection, and basic association. Because target 25.12 mt76 is newer than the vendor mt76 source, remaining `needs-evidence` rows are limited to plausible M06 probe, firmware-event, calibration, DMA, registration, RX/TX, association, or stability semantics.

Second-pass QC split the previous broad M07 bucket into MLO/TTLM, DFS/CSA, regulatory/power, QoS/SCS, beacon/MBSSID, vendor/certification, advanced MAC, rate-control, preamble-puncture, and off-channel handoffs. WED/RRO/HWRRO/offload-adjacent patches are deferred to M08. Debug/testmode/coredump/monitor instrumentation and calibration write-back tooling are review-only unless a concrete M06 bring-up failure requires them.

### M06-F PCIe Controller Support

PCIe controller patches `001135`-`001138` are reviewed separately from Wi-Fi driver patches. Direct 8X DTS/DTSO does not include `max-link-width`, `wifi-reset-gpios`, or `wifi-reset-msleep` on Wi-Fi PCIe nodes. Therefore max-link-width, WIFI HW reset, and soft on/off are `needs-evidence` rather than automatic M06 migrations. PCIe IRQ affinity is deferred to M09 as generic controller/performance policy.

### M06-G Minimal Hotplug / Radio Init

Rows `000497`-`000503` are supporting hotplug/userspace evidence but mostly change hostapd, netifd, mac80211 scripts, MLO, EHT, RSNO, or policy. They are deferred to M07. M06 may rely on target defaults for radio detection and only reopen a minimal hotplug row if the radio fails to initialize after hardware, firmware, and calibration are correct.

## High-risk Findings

| file_id | disposition / owner | evidence | action |
| --- | --- | --- | --- |
| `000858` | `rewrite` -> `M06` | Direct 8X Wi-Fi DTSO adds wifi_12v on GPIO4, AT24 EEPROM MAC cells at 0x51/0x52, and pcie0/pcie1 mediatek,mt76 child nodes with nvmem mac-address cells. | Rewrite into target 25.12 DTS style. TODO: resolve GPIO4 conflict, target label i2c_wifi vs base imux3_wifi, duplicate wifi_eeprom@51, and calibration vs MAC-source split before claiming radio enumeration. |
| `000859` | `static-only` -> `M06` | Direct 8X base DTS enables pcie0/pcie1, defines pcie0 mt7996@0,0 with mediatek,mtd-eeprom = <&factory 0x0>, labels imux3_wifi, and already has wifi_eeprom@51. | M06 TODO: preserve Wi-Fi topology evidence while M03 owns base DTS rewrite; decide whether the overlay merges, replaces, or restructures the base pcie0 mt7996 node and 0x51 EEPROM node. |
| `000343` | `superseded-by-target` -> `M06` | Vendor mt76 Makefile uses source date 2025-06-01; target 25.12 mt76 Makefile uses newer 2026-03-19 source and defines mt7996e, mt7996-firmware, and mt7996-233-firmware packages. | Use target mt76 package structure for basic 8X Wi-Fi closure. Do not copy vendor mt76 Makefile or vendor patch stack wholesale; M08 owns WED/offload package implications. |
| `000372` | `needs-evidence` -> `M06` | Patch [29/95] adds external EEPROM support and ext_eeprom debugfs/write callbacks mainly for mt7992/mt7990 golden EEPROM flows; direct 8X has AT24 MAC cells plus factory MTD calibration, so runtime relevance is unproven. | M06 TODO: verify target mt7996 eeprom path against direct 8X factory/AT24 design. Rewrite only if basic calibration/MAC loading requires this semantic. |
| `000388` | `needs-evidence` -> `M06` | Patch [45/95] uses `GFP_DMA32` for page-pool allocation to support 64-bit environments; possible DMA stability relevance for 8X, but target equivalence is not yet proven. | M06 TODO: inspect target page-pool allocation path and radio probe/RX logs; port only if target lacks the needed DMA32 behavior. |
| `000402` | `needs-evidence` -> `M06` | Patch [59/95] changes ADIE efuse merge/cal-free patchback flow so firmware initializes hwcfg after driver patchback; this is calibration-path relevant but target equivalence is unknown. | M06 TODO: compare target mt7996 calibration merge path and verify calibration logs before porting. |
| `000428` | `needs-evidence` -> `M06` | Patch [85/95] fixes long registration time by initializing VOW before init work, with a reported boot-time reduction; possible probe/registration relevance but target 25.12 may already differ. | M06 TODO: measure radio registration timing and compare target init/VOW ordering before porting. |
| `001135` | `needs-evidence` -> `M06` | Vendor PCIe max-link-width patch adds DT-driven link width handling, but direct 8X DTS/DTSO does not use max-link-width on Wi-Fi PCIe nodes. | M06 TODO: prove Wi-Fi enumeration requires max-link-width on actual 8X or drop/defer this controller patch; do not migrate from patch name alone. |
| `001137` | `needs-evidence` -> `M06` | Vendor PCIe WIFI HW reset patch adds wifi-reset GPIO handling, but direct 8X DTS/DTSO has wifi_12v regulator on GPIO4 and no wifi-reset-gpios or wifi-reset-msleep property. | M06 TODO: prove whether 8X Wi-Fi enumeration requires a reset GPIO flow; if yes, design a clean target DT binding without conflicting with GPIO4 switch_hrstn. |
| `001138` | `needs-evidence` -> `M06` | Vendor PCIe soft off/on API is reset/power-management infrastructure; direct 8X DTS/DTSO does not show that basic Wi-Fi probe depends on this API. | M06 TODO: keep out of basic bring-up unless radio reset/reprobe fails and target 6.12 lacks equivalent recovery; M09 may later review generic PCIe power management. |
| `000497` | `defer` -> `M07` | This wifi-scripts/hostapd userspace row is supporting evidence for radio init but mostly changes wireless policy, MLO, EHT, RSNO, or detection behavior outside hardware probe. | M07 TODO: review userspace policy after M06 proves radios enumerate and calibration loads. M06 may use target defaults for minimal radio detection; do not claim MLO/AFC/6GHz/Wi-Fi 7 success here. |

## Second-pass Classification QC

Second-pass QC read the current M06 markdown/TSV and checked all 155 rows for classification drift. Row-level review was applied to every `rewrite`, `static-only`, `needs-evidence`, `superseded-by-target`, and `defer` row. `drop` and `review-only` rows were sampled by group, with direct 8X, PCIe, firmware, and mt76 high-risk rows checked individually.

For mt76, all 94 patch rows were checked at least through patch header, subject, commit message, changed-file list, and the first 80-120 diff lines. EEPROM/calibration, probe/registration, PCIe/reset, firmware-load, RX/TX stability, and association-adjacent rows were read to enough detail to decide owner and disposition. Large debug/testmode rows, especially the giant debug tools patch, were not dense-read full text beyond that triage window; they remain `review-only` and are not used as M06 acceptance evidence.

Corrections made in this pass:

1. `000437` remains `defer -> M07`, but is now classified as off-channel TX/action-frame behavior, not MLO/AFC evidence.
2. The previous broad MLO/AFC M07 bucket was split into more precise DFS/CSA, QoS/SCS, beacon/MBSSID, regulatory/power, vendor/certification, advanced MAC, rate-control, preamble-puncture, off-channel, and true MLO/TTLM/AFC groups.
3. `000349` moved from `needs-evidence` to `review-only` because the patch is SER debug/recovery instrumentation.
4. `000380` moved from `needs-evidence` to `review-only` because it is nvmem/atenl flash write-back tooling, not required evidence for reading 8X factory/AT24 data.
5. `000381`, `000386`, `000406`, `000425`, and `000431` moved from M06 `needs-evidence` to M07 `defer` because patch content is DFS scan policy, vendor-command/radio-index policy, EPCS policy, TX duty-cycle policy, or scan dwell userspace policy.
6. Remaining M06 `needs-evidence` rows were tightened to patch-specific evidence instead of a generic "could affect basic bring-up" formula.

No JSON-derived TSV fields were changed in this pass.

## Secondary Review Handoffs

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `000858` | `M06` | `M03`, `M05` | Direct 8X Wi-Fi overlay owns Wi-Fi nodes/MAC cells/regulator, but M03 owns DTS structure and M05 owns GPIO4 conflict with `switch_hrstn`. |
| `000859` | `M06` static Wi-Fi evidence | `M03`, `M04`, `M05`, `M09`, `M10` | Base DTS mixes Wi-Fi PCIe/calibration with board identity, Ethernet, full wired, PCIe/USB/fan, and storage/rootdisk content. |
| `000343` | `M06` package closure | `M08`, `M07` | mt76 package closure is M06, while WED/offload package implications are M08 and userspace/MLO behavior is M07. |
| `000346`-`000348`, `000368`, `000385`, `000421` | `M08` | `M06` prerequisite | WED/RRO/HWRRO/offload rows require stable basic radios first. |
| MLO/TTLM/AFC/LPI, DFS/CSA, QoS/SCS, beacon/MBSSID, regulatory/power, vendor-certification, advanced MAC, rate-control, preamble-puncture, and `000437` off-channel rows | `M07` | `M06` prerequisite | Userspace and advanced wireless behavior must wait for hardware probe, firmware, and calibration. |
| `000497`-`000503` | `M07` | `M06` prerequisite only | Broad wifi-scripts/hostapd/netifd policy is not M06, except target defaults may be used for minimal detection. |
| `001136` | `M09` | `M06` prerequisite only | PCIe IRQ affinity is generic controller/performance policy, not proof of basic Wi-Fi enumeration. |
| `001137`, `001138` | `M06` needs-evidence | `M09` possible later | Wi-Fi reset and soft on/off need direct 8X property/runtime proof before M06; generic PCIe power policy can be revisited in M09. |

## TODOs

1. M06: resolve `000858` overlay target `&i2c_wifi` versus base `imux3_wifi` before any DTS migration.
2. M06: resolve duplicate/merge behavior for base `wifi_eeprom@51` and overlay `wifi_eeprom@51` with nvmem-layout.
3. M06/M05: resolve GPIO4 ownership between Wi-Fi `wifi_12v` and MxL86252 `switch_hrstn` before enabling both behaviors.
4. M06: prove whether calibration should use factory MTD `mediatek,mtd-eeprom = <&factory 0x0>`, AT24 EEPROM data, mt7996 package EEPROM binaries, or a combination.
5. M06: inspect target mt76 source or run basic Wi-Fi 6 association before porting any `needs-evidence` mt76 patch.
6. M06: prove whether PCIe `wifi-reset` or soft on/off flow is required for 8X radio enumeration; direct DTS/DTSO currently lacks the expected properties.
7. M07: review deferred MLO/TTLM/AFC/LPI, DFS/CSA, QoS/SCS, beacon/MBSSID, regulatory/power, vendor-certification, advanced MAC, rate-control, preamble-puncture, and off-channel TX/action-frame behavior only after M06 radios enumerate.
8. M08: review WED/RRO/HWRRO/offload only after basic Wi-Fi and wired paths are stable.
9. M09: review generic PCIe IRQ affinity/controller performance outside M06.

## Minimalism Gate

Gate result: pass for round-1-audited review.

Checks performed:

1. Direct 8X `000858` and `000859` were read before deciding Wi-Fi topology, regulator, EEPROM, calibration, and PCIe rows.
2. GPIO4 conflict was not hidden under a minimal overlay migration; it is explicitly recorded as a blocking implementation-time TODO.
3. `i2c_wifi` vs `imux3_wifi` and duplicate `wifi_eeprom@51` were not silently papered over.
4. Vendor mt76 patch stack was not copied wholesale; second-pass QC split broad M07 handoffs into patch-specific groups and kept only plausible basic bring-up rows as M06 needs-evidence.
5. Target mt76 package evidence was checked before marking firmware/package rows superseded.
6. R4/R4Lite/MT7987/RFB DTS files were not used as direct 8X hardware truth.
7. No M06 row claims Wi-Fi probe, firmware load, calibration load, association, MLO, AFC, 6 GHz, Wi-Fi 7, or offload runtime success.
8. Every `defer`, `static-only`, and `needs-evidence` row has a named owner and actionable TODO in the TSV notes or this markdown.

## Remaining Risk

M06 formal no-context audit round 1 is complete and accepted by all three reviewers.

M06 implementation risk remains high around GPIO4 ownership, overlay target labels, duplicate EEPROM nodes, calibration source selection, target mt76 source equivalence, PCIe reset/reprobe behavior, and whether target default hotplug is sufficient for radio detection. Later-step risks are deferred to M07 for advanced wireless userspace, MLO/TTLM/AFC/LPI, DFS/CSA, QoS/SCS, beacon/MBSSID, regulatory/power, vendor-certification, advanced MAC, rate-control, preamble-puncture, and off-channel policy; M08 for WED/HWRRO/offload; M09 for generic PCIe controller/expansion behavior; and M10 for storage/sysupgrade.

## Future Review Focus

Future implementation review should continue to verify:

1. TSV coverage against M06 by-step JSON: 155/155, 371 assignments, exact field parity.
2. Direct 8X evidence for `000858` and `000859`, especially GPIO4, `i2c_wifi` vs `imux3_wifi`, duplicate `wifi_eeprom@51`, pcie0/pcie1 nodes, factory `mediatek,mtd-eeprom`, and AT24 MAC cells.
3. Target 25.12 mt76 Makefile claims for `mt7996e`, `mt7996-firmware`, `mt7996-233-firmware`, and firmware binary installs.
4. mt76 patch triage boundaries: M06 basic bring-up only; M07 advanced wireless/userspace/MLO/DFS/QoS/beacon/regulatory/vendor/rate/off-channel behavior; M08 WED/offload.
5. PCIe patches `001135`-`001138` are not promoted without direct 8X DT property or runtime enumeration evidence.
6. R4/R4Lite/MT7987/RFB rows are not treated as direct 8X truth.
7. No hidden minimalism: no filename-only drop/defer and no unreported runtime assumptions.
