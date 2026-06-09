# Migration Step M03 Batch Review: Board Identity, Power, I2C, GPIO, Factory Data

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M03-board-identity-power-i2c-gpio-factory-data.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.files.tsv`

This review is part of Project Phase 2. It does not migrate code.

## Audit Status

This file is the M03 main-agent draft batch review with first- and
second-round no-context audit feedback applied.

Formal three-agent no-context audit status: first and second rounds completed
on 2026-06-08; second-round verdicts were `accept`, `accept-with-minor-edits`,
and `accept`.

First-round no-context audit summary:

| reviewer id | verdict | structural checks | actionable findings | main-agent action |
| --- | --- | --- | --- | --- |
| `M03-audit-agent-1` | `accept-with-minor-edits` | Passed: 87/87 TSV coverage, exact JSON field match, legal dispositions, legal owners, and TODO obligations covered. | Minor: `000858` should explicitly hand off the Wi-Fi overlay `i2c_wifi` vs `imux3_wifi` target mismatch and existing base `wifi_eeprom@51` merge/restructure question to M06. | Accepted and applied to the markdown and TSV. |
| `M03-audit-agent-2` | `accept` | Passed: 87/87 TSV coverage, exact JSON field match, legal dispositions, legal owners, and TODO obligations covered. | None. | No change. |
| `M03-audit-agent-3` | `accept` | Passed: 87/87 TSV coverage, exact JSON field match, legal dispositions, legal owners, and TODO obligations covered. | None. | No change. |

Accepted first-round audit changes:

1. `M03-audit-agent-1` recommended expanding the `000858` M06 handoff for
   the Wi-Fi overlay target-label and existing EEPROM-node issue.
2. Main agent accepted the recommendation and updated the `000858` TSV row,
   Direct 8X Wi-Fi overlay evidence, Secondary Review Handoffs, and TODOs.

Rejected first-round audit changes: none.

Second-round no-context audit summary:

| reviewer id | verdict | structural checks | actionable findings | main-agent action |
| --- | --- | --- | --- | --- |
| `M03-audit-round2-agent-1` | `accept` | Passed: 87/87 TSV coverage, exact JSON field match, legal dispositions, legal owners, and TODO obligations covered. | None. | No change. |
| `M03-audit-round2-agent-2` | `accept-with-minor-edits` | Passed: 87/87 TSV coverage, exact JSON field match, legal dispositions, legal owners, and TODO obligations covered. | Minor: `000040`-`000049` AS21xxx `defer` rows should use explicit row-local `M05 TODO:` wording. | Accepted and applied to the TSV. |
| `M03-audit-round2-agent-3` | `accept` | Passed: 87/87 TSV coverage, exact JSON field match, legal dispositions, legal owners, and TODO obligations covered. | None. | No change. |

Accepted second-round audit changes:

1. `M03-audit-round2-agent-2` recommended making the `000040`-`000049`
   AS21xxx deferred rows use explicit row-local `M05 TODO:` wording.
2. Main agent accepted the recommendation and updated the TSV notes for those
   rows without changing their disposition or owner.

Rejected second-round audit changes: none.

## Review Purpose

Migration Step M03 decides which vendor changes are needed to establish BPI-R4 Pro 8X board identity and foundational board services before runtime hardware steps.

M03 covers:

1. direct 8X `model` and `compatible`,
2. static board DTS structure needed by later steps,
3. RT5190A PMIC and CPU/CCI supply wiring as static power evidence,
4. PCA9545 I2C mux, PCA9555 GPIO expander, PCF8563 RTC, AT24 EEPROMs, INA226, reset/WPS keys, LEDs, and GPIO ownership,
5. Factory nvmem cells and MAC/calibration data source paths,
6. SoC/DTS context only when needed for 8X board identity.

M03 does not cover:

1. wired PHY, switch, SFP, DSA, or 10G runtime behavior,
2. Wi-Fi bring-up or mt76 runtime,
3. acceleration/offload,
4. USB, PCIe, fan, thermal, or expansion runtime validation,
5. NAND/eMMC install, persistent storage, sysupgrade, or rootfs policy,
6. runtime success claims.

## Input Scope

M03 by-step input contains 87 files and 192 feature assignments.

Status split:

| status | file count |
| --- | ---: |
| `A` | 78 |
| `M` | 9 |

Route-class split:

| route class | assignment count |
| --- | ---: |
| `primary` | 170 |
| `supporting` | 22 |

Strict TSV scope:

1. The TSV contains only the 87 files from the M03 by-step JSON.
2. M00/M01/M02 handoffs are reviewed in this markdown when relevant but are not added as TSV rows unless they are also in the M03 JSON.
3. Direct 8X evidence is authoritative. MT7988 RFB, MT7987, BPI-R4 Lite, and target 25.12 files are supporting or structure references only.

Prior-step handoff check:

1. M00 requires M03 to read the direct 8X base DTS before board identity, GPIO, I2C, factory data, and SoC foundation work.
2. M00 has SoC-foundation handoffs to M03 outside this TSV: `001126`, `001127`, `001129`, and `001140`. `001130` is in the M03 JSON and appears in the TSV.
3. M01 marks `000972` as secondary M03 evidence because the image recipe points at DTS/board identity closure, but `000972` remains an M01 file and is not an M03 TSV row.
4. M02 marks `000031` as M03/M10 handoff for uboot-envtools/env identity. It is not in the M03 JSON and is therefore reviewed here as a TODO, not as a TSV row.
5. M02 marks `000859` as M03/M10 handoff. `000859` is in the M03 JSON and is the main direct 8X base DTS row.

## Direct 8X Evidence

Direct 8X base DTS:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`

Key evidence checked:

1. `model = "Bananapi BPI-R4-PRO-8X"` and compatible is `bananapi,bpi-r4-pro-8x`, `mediatek,mt7988a`.
2. I2C aliases include base controllers and PCA9545 mux channels: `i2c3` as local mux channel, `i2c4`/`i2c5` for SFP cages, and `i2c6` for Wi-Fi.
3. `gpio-keys` defines reset on GPIO13 and WPS on GPIO14.
4. `gpio-leds` defines red and blue LEDs through PCA9555 GPIO expander pins 15 and 14.
5. RT5190A PMIC is on `i2c0` at 0x64, with `buck1`, `vcore`, `vproc`, `buck4`, and `ldo`; CPUs and CCI use `rt5190_buck3` as `proc-supply`.
6. PCA9545 at 0x70 exposes local board devices: INA226 at 0x40, PCF8563 RTC at 0x51, AT24 24c02 EEPROM at 0x57, and PCA9555 at 0x20.
7. Factory nvmem cells in SPI-NAND Factory partition define `gmac2_mac` at 0xfffee, `gmac1_mac` at 0xffffa, and `gmac0_mac` at 0xffff4.
8. Ethernet GMAC nodes consume those nvmem cells, but port mapping and interface defaults are M04.
9. Direct 8X wired content includes AS21xxx firmware names and MxL86252/SFP topology, but wired runtime is M05.
10. `switch_hrstn` uses GPIO4 as a reset hog for MxL86252, while the Wi-Fi overlay also uses GPIO4 for `wifi_12v`; this conflict must be resolved across M05/M06.
11. Base DTS includes SPI-NAND rootdisk, UBI env volumes, PCIe, USB, fan, and Wi-Fi nodes. Those are not M03 runtime/storage claims.

Direct 8X RTC overlay:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-rtc.dtso`

The overlay is 8X-compatible and targets `&pcf8563`. M03 may preserve this static RTC overlay, but this review does not claim runtime RTC validation.

Direct 8X eMMC and SD overlays:

`000855` and `000857` both carry direct 8X compatible strings, but their useful semantics are storage/rootdisk/env layout. `000857` also records SD card-detect GPIO12, which remains SD-boot evidence for M02 rather than a M03 runtime claim. M03 uses only board-compatible/GPIO context. M02 owns SD boot, and M10 owns persistent storage/install/sysupgrade.

Direct 8X Wi-Fi overlay:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`

The overlay adds a fixed `wifi_12v` regulator on GPIO4 and Wi-Fi AT24 EEPROM MAC cells at 0x51 and 0x52. It targets `&i2c_wifi`, while the base DTS labels the mux channel `imux3_wifi` and already defines `wifi_eeprom@51`; M06 must resolve the target label and merge/replace the existing 0x51 EEPROM node. M03 records this as static GPIO/EEPROM evidence only. M06 owns Wi-Fi overlay migration and runtime bring-up.

Direct 8X PHY package evidence:

The direct 8X base DTS names `as21x1x_fw.bin` for PHY24 and PHY28. That supports the AS21xxx package cluster as later wired evidence, but M05 owns driver/firmware package closure and runtime PHY validation. AQR firmware appears in RFB AQR/CUX references, not direct 8X DTS, so AQR remains `needs-evidence` for M05.

Direct 8X Factory MAC evidence:

The direct 8X base DTS defines `gmac0_mac` at 0xffff4, `gmac1_mac` at 0xffffa, and `gmac2_mac` at 0xfffee. Vendor `02_network` and patch `001003` support the same offset polarity, but interface assignment and LAN/WAN defaults remain M04.

Target OpenWrt 25.12 structure evidence:

Target 25.12 already has MT7988/BPI-R4 DTS restructuring and examples for RT5190A, PCA9545, PCF8563 overlays, SD/eMMC overlays, and Factory MAC handling. These are structure references only; they do not decide BPI-R4 Pro 8X hardware facts.

## Routing Conclusions

1. `000859` is the primary M03 input and should be rewritten into target 25.12 structure, splitting out later-step content.
2. `000856` is a direct 8X RTC overlay and is a M03 `migrate` input.
3. `000855`, `000857`, and `000858` are direct 8X overlays but not M03 migration owners: eMMC and SD are storage/boot context, and Wi-Fi belongs to M06.
4. `000037`-`000039` AQR firmware/package entries need M05 evidence because direct 8X DTS names AS21xxx firmware instead.
5. `000040`-`000049` AS21xxx firmware/driver files are directly suggested by 8X DTS, but full handling belongs to M05.
6. MT7987 and BPI-R4 Lite files are not direct 8X authority and should not be copied into M03.
7. MT7988 RFB files can be same-SoC supporting references, but direct 8X DTS remains authoritative.
8. `001130` needs M03 follow-up with paired M00 handoff `001129`; the DTS nvmem-cell addition alone is not enough to migrate CPU voltage calibration.
9. Storage/SPI-NAND/rootdisk/env behavior is explicitly handed to M10.
10. No runtime wired, Wi-Fi, acceleration, USB, fan, storage, sysupgrade, or install success is claimed.

## Disposition Summary

| disposition | file count |
| --- | ---: |
| `defer` | 37 |
| `drop` | 39 |
| `migrate` | 1 |
| `needs-evidence` | 4 |
| `review-only` | 5 |
| `rewrite` | 1 |

Owner-step summary:

| owner_step | file count |
| --- | ---: |
| `M03` | 47 |
| `M05` | 29 |
| `M06` | 2 |
| `M08` | 2 |
| `M10` | 7 |

Group summary:

| group | file count |
| --- | ---: |
| `acceleration-hnat-patch` | 1 |
| `aqr-phy-firmware-needs-evidence` | 3 |
| `as21xxx-phy-firmware-driver` | 10 |
| `boardd-mac-context` | 1 |
| `direct-8x-base-board-dts` | 1 |
| `direct-8x-emmc-storage-context` | 1 |
| `direct-8x-rtc-overlay` | 1 |
| `direct-8x-sd-overlay-context` | 1 |
| `direct-8x-wifi-eeprom-gpio-context` | 1 |
| `factory-mac-offset-supporting-patch` | 1 |
| `mt7988-cpufreq-nvmem-calibration` | 1 |
| `mt7988-rfb-soc-reference` | 2 |
| `mt7988-rfb-storage-reference` | 4 |
| `mt7988-rfb-unneeded-reference` | 2 |
| `mt7988-rfb-wired-reference` | 11 |
| `non-8x-mt7981-reference` | 2 |
| `non-8x-mt7987-reference` | 36 |
| `spi-nand-storage-patch` | 2 |
| `wifi-pcie-option-reference` | 1 |
| `wired-phy-sfp-patch-reference` | 5 |

## Secondary Review Handoffs

The TSV schema has one `owner_step` per file. Mixed-owner files are therefore kept under their primary owner and called out here.

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `000031` | `M03` handoff from M02 | `M10` | uboot-envtools/env access may affect identity/env handling, while persistent env location and storage policy belong to M10. It is not in the M03 by-step TSV. |
| `000037`-`000039` | `M05` | none | AQR firmware/package remains `needs-evidence`; direct 8X DTS names AS21xxx firmware, not AQR. |
| `000040`-`000049` | `M05` | `M03` evidence only | Direct 8X base DTS names `as21x1x_fw.bin`, but driver/firmware runtime belongs to M05. |
| `000855` | `M10` | `M03` context only | eMMC overlay carries direct 8X compatible context but eMMC env/rootdisk/install semantics are M10. |
| `000857` | `M03` review-only | `M02`, `M10` | SD overlay has board-compatible context; SD boot is M02 and persistent rootdisk/env implications are M10. |
| `000858` | `M06` | `M03`, `M05` | Wi-Fi overlay contains AT24 Wi-Fi EEPROM and GPIO4 `wifi_12v`; M06 owns Wi-Fi and must resolve `i2c_wifi` vs `imux3_wifi` plus the existing base `wifi_eeprom@51`, while M05 must account for GPIO4 conflict with base DTS `switch_hrstn`. |
| `000859` | `M03` | `M04`, `M05`, `M06`, `M09`, `M10` | base DTS mixes M03 board identity/static services with Ethernet defaults/MAC use, wired PHY/SFP/MxL, Wi-Fi nodes, USB/PCIe/fan extras, and SPI-NAND/rootdisk/env storage. |
| `000860`, `000870`, `000872`, `000873` | `M10` | none | same-SoC RFB storage overlays are supporting references only; storage/rootdisk/env policy belongs to M10. |
| `000861`-`000869`, `000876`, `000877` | `M05` | none | same-SoC RFB wired overlays are supporting references only; wired PHY/SFP/DSA belongs to M05. |
| `000960` | `M03` review-only | `M04` | board.d Factory MAC offsets support M03 identity evidence; network defaults and LAN/WAN assignment are M04. |
| `000999`-`001002`, `001076` | `M05` | none | PCS, AQR, and SFP debug patches are full wired/SFP work, not M03. |
| `001003` | `M03` review-only | `M04`, `M05` | supports Factory MAC offset polarity but interface mapping and wired behavior remain later-step work. |
| `001060`, `001120` | `M08` | `M05`, `M06` as prerequisites | HNAT/WED acceleration must wait for base wired and Wi-Fi behavior. |
| `001114` | `M06` | `M09` | MT7988D RFB option type 2 is Wi-Fi/PCIe supporting reference, not direct 8X board identity. |
| `001126`, `001127`, `001129`, `001140` | `M03` handoffs from M00 | later split if needed | M00 handed these SoC foundation patches to M03; only `001130` is in the M03 TSV. Review them before implementation without adding extra TSV rows. |
| `001130` | `M03` | none | CPU voltage calibration DTS cells need paired driver/context review before migration. |
| `001141`, `001143` | `M10` | none | SPI calibration/CASN SPI-NAND behavior belongs to onboard storage/install/sysupgrade review. |

## TODOs

1. Migration Step M03: rewrite direct 8X base DTS `000859` into target 25.12 style for board identity, RT5190A, PCA9545, PCA9555, PCF8563, AT24 EEPROMs, keys, LEDs, and Factory nvmem cells.
2. Migration Step M03: preserve direct 8X RTC overlay `000856` in target style without claiming runtime RTC validation.
3. Migration Step M03/M05/M06: resolve or explicitly document the GPIO4 conflict between base DTS `switch_hrstn` and Wi-Fi overlay `wifi_12v` before enabling both behaviors.
4. Migration Step M03: review M02 handoff `000031` and decide whether 8X needs a uboot-envtools board case for identity/env access; defer persistent env/storage layout to M10.
5. Migration Step M03: review M00 handoff patches `001126`, `001127`, `001129`, and `001140` before implementation; pair `001130` with `001129` before deciding CPU voltage calibration migration.
6. Migration Step M04: review `000960` and direct DTS Factory MAC cells for LAN/WAN defaults and interface assignment.
7. Migration Step M05: verify AS21xxx driver/firmware package closure against direct 8X DTS and runtime PHY enumeration.
8. Migration Step M05: prove or reject AQR/Aquantia applicability for 8X before migrating `000037`-`000039` or AQR patches.
9. Migration Step M05: review same-SoC RFB wired/SFP/PHY files only as supporting references after direct 8X wired topology is inspected.
10. Migration Step M06: own direct 8X Wi-Fi overlay `000858`, Wi-Fi EEPROM MAC cells, Wi-Fi PCIe nodes, and Wi-Fi regulator runtime; resolve `i2c_wifi` vs `imux3_wifi` and decide whether the overlay should merge, replace, or restructure the existing base `wifi_eeprom@51` node.
11. Migration Step M08: review HNAT/WED acceleration only after base wired and Wi-Fi paths are stable.
12. Migration Step M09: review USB, PCIe expansion, fan, PWM, thermal, and runtime board extras after core identity/networking are stable.
13. Migration Step M10: review eMMC, SD persistent env/rootdisk implications, SPI-NAND, rootdisk, UBI, install, sysupgrade, and storage policy.

## Unreported Minimalism Gate

Result: passed for the M03 main-agent draft after content checks.

Minimalism risks checked:

1. Direct 8X base DTS was inspected before marking `000859` as `rewrite`.
2. Direct 8X overlays were split by owner instead of being migrated wholesale.
3. MT7987, BPI-R4 Lite, and RFB files were not promoted to direct 8X authority.
4. AQR firmware was not accepted from RFB references because direct 8X DTS names AS21xxx firmware.
5. AS21xxx package files were not migrated in M03 even though direct 8X DTS names the firmware; M05 owns runtime package closure.
6. Storage, SD/eMMC, rootdisk, install, sysupgrade, Wi-Fi, wired, acceleration, USB, PCIe, fan, and thermal behavior were handed to owner steps instead of pulled into M03.
7. `001130` was not migrated from a DTS tag alone; paired driver/context evidence is required.
8. Every `defer` and `needs-evidence` row has a named owner and an actionable TODO in the TSV notes and this markdown.
9. No runtime success claim is made.

## Remaining Risk

Formal no-context audit rounds completed for the M03 review matrix.

Runtime enumeration remains unvalidated for I2C devices, RTC, GPIO expander, keys, LEDs, Factory nvmem cells, and power rails. GPIO4 ownership remains a cross-step conflict until M03/M05/M06 resolve it. Later-step risks are explicitly deferred to M04, M05, M06, M08, M09, and M10.
