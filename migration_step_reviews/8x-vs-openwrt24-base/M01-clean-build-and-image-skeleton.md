# Migration Step M01 Batch Review: Clean Build And Image Skeleton

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M01-clean-build-and-image-skeleton.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M01-clean-build-and-image-skeleton.files.tsv`

This review is part of Project Phase 2. It does not migrate code.

## Audit Status

This file is the formally audited M01 batch review.

Formal three-agent no-context audit status: completed on 2026-06-08.

Traceability note: M01 predates the later standard of saving standalone raw
audit logs under `audit_logs/`. The formal audit summary above records the
reviewer IDs and verdicts; absence of standalone raw logs is a logging
limitation, not evidence that the M01 classifications are invalid.

Final no-context reviewers:

| reviewer id | agent id | verdict |
| --- | --- | --- |
| `M01-audit-agent-1` | `019ea9a0-5471-7d72-a6a3-84c972223351` | `accept` |
| `M01-audit-agent-2` | `019ea9a0-549f-72b2-afd5-d4bb4b153363` | `accept` |
| `M01-audit-agent-3` | `019ea9a0-544b-7290-b7c7-228c33ac0a03` | `accept` |

## Formal No-Context Audit Results

Pre-final accepted changes:

1. A first-round no-context audit report from agent `019ea995-0d62-7153-9727-82bec36682ed` recommended expanding the `000972` secondary-review handoff because the 8X image recipe package list also points at later runtime closure owners. The main agent accepted this recommendation. It is reflected in the `000972` row of the Secondary Review Handoffs table.
2. First-round no-context audit reports from agents `019ea995-0d89-7a92-96f8-c2003a5d2a1b` and `019ea995-0dc0-78f0-bf07-619976aa684b` recommended matching TSV `features` order to the by-step JSON. The main agent accepted this recommendation. It is reflected in the TSV rows for `000001`, `000002`, `000028`, and `000823`.

Final audit results:

| reviewer id | verdict | structural checks result | findings summary | accepted/rejected changes |
| --- | --- | --- | --- | --- |
| `M01-audit-agent-1` | `accept` | Passed: 88 by-step files, 88 TSV rows, no missing/extra/duplicate IDs; `status`, `path`, `file_kind`, `features`, and `route_classes` matched; dispositions and owner rules passed. | No actionable findings. Confirmed M01 boundary, high-impact TF-A/U-Boot/`filogic.mk` evidence split, secure-boot exclusion, and audit status handling. | Accepted changes: none after final audit. Rejected changes: none. |
| `M01-audit-agent-2` | `accept` | Passed: 88 TSV rows for 88 inputs; 12-column TSV shape; dispositions legal; deferred and needs-evidence rows owned by later steps. | No blocking or material findings. Confirmed no runtime, install, sysupgrade, USB, acceleration, or secure-boot success claims. | Accepted changes: none after final audit. Rejected changes: none. |
| `M01-audit-agent-3` | `accept` | Passed: 88 by-step files, 88 TSV rows, exact field match, valid dispositions, valid owners, and TODO obligations covered by TSV notes plus markdown TODOs. | No findings. Confirmed direct 8X evidence handling, AQR `needs-evidence`, non-8X `filogic.mk` hunks blocked, and later-step residual risk split. | Accepted changes: none after final audit. Rejected changes: none. |

## Review Purpose

Migration Step M01 decides the minimum source inputs needed to make a clean
target 25.12 build and an 8X image skeleton exist.

M01 answers:

1. which files define the 8X device profile, image recipe, TF-A target, and U-Boot target skeleton,
2. which vendor files are only generated build clues,
3. which package entries are only build-closure hints and not runtime validation,
4. which optional secure-boot, firmware-encryption, OP-TEE, dm-verity, or anti-rollback files are out of baseline scope,
5. which files must be deferred to later runtime or install migration steps.

## Migration Step Boundary

Allowed in M01:

1. 8X target device profile and image recipe skeleton,
2. DTS and DTSO selection needed for image construction,
3. package list review only as build closure for an image recipe,
4. TF-A and U-Boot build-target selection needed to emit artifacts,
5. clean target 25.12 feed policy.

Not allowed in M01:

1. NAND or eMMC install behavior,
2. declaring SD boot, sysupgrade, or recovery success from an artifact name,
3. wired, Wi-Fi, storage, acceleration, USB, or board-extra runtime bring-up,
4. treating vendor `.config` or `.config.old` as hardware truth,
5. copying vendor `feeds.conf.default` or vendor feed script behavior,
6. enabling optional secure-boot, firmware-encryption, OP-TEE, dm-verity, or anti-rollback flows just because vendor support files exist.

## Input Scope

M01 contains 88 files and 143 feature assignments.

Status split:

| status | file count |
| --- | ---: |
| `A` | 59 |
| `D` | 1 |
| `M` | 28 |

Route-class split:

| route class | assignment count |
| --- | ---: |
| `primary` | 125 |
| `review-only` | 2 |
| `supporting` | 16 |

M00 handoff check:

1. the M00 TSV currently has no `owner_step == M01` rows,
2. the M00 markdown TODO for M01 is feed policy: choose a clean target 25.12 feed policy and do not copy vendor `feeds.conf.default`.

## Direct 8X Evidence

Direct 8X image recipe:

`target/linux/mediatek/image/filogic.mk`

Key evidence checked:

1. vendor adds `Device/bananapi_bpi-r4-pro-8x`,
2. the profile selects the base DTS and four overlays: eMMC, RTC, SD, and Wi-Fi MT7996A,
3. the package list names SFP, hwmon, I2C mux, EEPROM, RTC, USB, Wi-Fi firmware, and storage tools,
4. the recipe emits FIT, sysupgrade, SD, eMMC, and SNAND artifact names,
5. target 25.12 already has BPI-R4 and BPI-R4 Lite recipes but no 8X recipe.

Conclusion: this file is the primary M01 rewrite input. The target 25.12
structure should be used, while install and boot-success semantics are left to
M02 and M10.

Direct 8X TF-A evidence:

`package/boot/arm-trusted-firmware-mediatek/Makefile`

Key evidence checked:

1. vendor adds `DDR4_4BG_MODE:=1` to MT7988 eMMC, SDMMC, and SPIM-NAND-UBI comb targets,
2. target 25.12 already supports the `DDR4_4BG_MODE` flag but does not set it on those MT7988 comb targets.

Conclusion: M01 must preserve the 8X boot-artifact requirement, but should not
globally mutate shared MT7988 targets unless later evidence proves the setting
is platform-wide.

Direct 8X U-Boot evidence:

`package/boot/uboot-mediatek/Makefile`

`package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch`

Key evidence checked:

1. vendor adds eMMC, SDMMC, and SNAND 8X U-Boot package targets,
2. those targets use 8X `BUILD_DEVICES`, bootdev selection, TF-A dependencies, and 8X defconfigs,
3. the patch adds U-Boot DTS/DTSI, defconfigs, and environment files,
4. the environment files contain SD boot and install-menu behavior.

Conclusion: M01 owns U-Boot build-target and defconfig skeleton review only.
M02 owns SD boot environment behavior. M10 owns NAND/eMMC install and persistent
storage policy.

Generated config clue:

`.config`

`.config.old`

Key evidence checked:

1. both generated configs select `TARGET_DEVICE_mediatek_filogic_DEVICE_bananapi_bpi-r4-pro-8x=y`,
2. both show `CONFIG_MTK_SECURE_BOOT` and `CONFIG_PACKAGE_optee-mediatek` disabled.

Conclusion: these files are clues only. They justify excluding optional secure
boot from the baseline M01 skeleton, but they do not prove hardware behavior.

## Disposition Summary

The TSV review matrix assigns one disposition per M01 file.

| disposition | file count | meaning in M01 |
| --- | ---: | --- |
| `rewrite` | 4 | Direct 8X image, TF-A, and U-Boot skeleton inputs that must be ported into target 25.12 style. |
| `review-only` | 47 | Evidence, generated clues, target references, or optional helper context with no direct M01 migration action. |
| `drop` | 22 | Routing noise or optional vendor support not needed for the clean M01 skeleton. |
| `defer` | 14 | Real migration input, but owned by a later runtime or install step. |
| `needs-evidence` | 1 | Possible later package dependency that still needs direct 8X proof. |

Owner split:

| owner step | file count | reason |
| --- | ---: | --- |
| `M01` | 73 | Build/image skeleton inputs, references, and M01 drops. |
| `M02` | 4 | SD boot environment and reset-boot-count questions. |
| `M05` | 4 | AS21xxx and AQR/PHY package applicability. |
| `M06` | 1 | mt76 driver and firmware closure. |
| `M07` | 3 | mac80211 and hostapd/wpad userspace policy. |
| `M08` | 1 | flowtable/offload package boundary. |
| `M09` | 1 | USB kernel module policy. |
| `M10` | 1 | fstools bootparam, dual-boot, rootfs, and install policy. |

## Evidence Groups

| group | count | disposition pattern |
| --- | ---: | --- |
| `accel-module-boundary` | 1 | `defer` to M08 |
| `board-extra-module-boundary` | 1 | `defer` to M09 |
| `boot-artifact-tfa` | 1 | `rewrite` in M01 |
| `boot-artifact-uboot` | 2 | `rewrite` in M01 |
| `build-diagnostic-tool` | 2 | `drop` |
| `config-clue` | 2 | `review-only` in M01 |
| `diagnostic-package` | 3 | `drop` |
| `direct-8x-image-recipe` | 1 | `rewrite` in M01 |
| `feed-policy-boundary` | 1 | `drop` |
| `generic-package-version` | 1 | `drop` |
| `host-tool-overreach` | 1 | `drop` |
| `kernel-config-clue` | 1 | `review-only` in M01 |
| `legacy-hash-tool` | 3 | `drop` |
| `network-module-boundary` | 1 | `defer` to M05, with M08 secondary review noted |
| `phy-package-boundary` | 3 | `defer` or `needs-evidence` to M05 |
| `recovery-boot-count` | 4 | `defer` to M02 |
| `rfb-reference-image` | 1 | `drop` |
| `secure-boot-host-tool` | 27 | `drop` or `review-only` in M01 |
| `secure-boot-kconfig` | 1 | `review-only` in M01 |
| `secure-boot-kernel-modules` | 1 | `drop` |
| `secure-boot-optee` | 13 | `review-only` in M01 |
| `secure-fit-helper` | 6 | `review-only` in M01 |
| `storage-policy-boundary` | 1 | `defer` to M10 |
| `vendor-config-tool` | 6 | `drop` |
| `wireless-build-boundary` | 2 | `defer` to M06 or M07 |
| `wireless-userspace-boundary` | 2 | `defer` to M07 |

## Routing Conclusions

1. The M01 implementation should start from target 25.12 structure and add the 8X image skeleton deliberately.
2. The direct 8X image recipe is a rewrite source, not a file to copy wholesale.
3. TF-A and U-Boot build-target selection are in scope, but U-Boot environment boot policy and install menus are split to M02 and M10.
4. FIT, firmware, sysupgrade, SD, eMMC, and SNAND artifact names are build outputs only in M01. They do not prove boot, install, or sysupgrade success.
5. The vendor package list is useful only as an image build-closure clue. It does not validate wired, Wi-Fi, storage, acceleration, USB, or board-extra runtime behavior.
6. Secure boot, firmware encryption, OP-TEE, dm-verity, anti-rollback, and related host tools are excluded from the baseline because direct config evidence has secure boot disabled.
7. Vendor feed configuration and `scripts/feeds` subdirectory support are not part of the target 25.12 M01 baseline.
8. `.config` and `.config.old` remain clue-only evidence and must not decide hardware truth.

## Secondary Review Handoffs

The TSV schema has one `owner_step` per file. Mixed-owner files are therefore
kept under their primary owner and called out here.

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `000033` | `M01` | `M02`, `M10` | U-Boot patch DTS, defconfig, and build target belong to M01; SD boot env belongs to M02; NAND/eMMC install menu behavior belongs to M10. |
| `000051` | `M05` | `M08` | Shared kernel module file adds both AN8801SB PHY packaging and MediaTek HNAT packaging. |
| `000343` | `M06` | `M08` | mt76 package changes include WED/offload behavior, but M06 owns basic Wi-Fi driver and firmware closure first. |
| `000972` | `M01` | `M02`, `M03`, `M05`, `M06`, `M08`, `M09`, `M10` | `filogic.mk` 8X image skeleton belongs to M01. SD/recovery artifacts require M02; DTS/board identity requires M03; SFP/PHY package closure requires M05; Wi-Fi package closure requires M06; `mt7988-wo-firmware` and offload implications require M08; USB, RTC, I2C, and hwmon extras require M09; GPT, partition layout, NAND/eMMC install artifacts, sysupgrade, and storage semantics require M10. |

## TODOs

1. Migration Step M01: port the 8X device profile and image skeleton into target 25.12 style.
2. Migration Step M01: decide clean target 25.12 feed policy explicitly; do not copy vendor `feeds.conf.default` or depend on vendor `scripts/feeds` subdirectory support.
3. Migration Step M01: preserve direct 8X TF-A boot-artifact requirements while avoiding broad shared MT7988 Makefile mutation unless separately justified.
4. Migration Step M01: port U-Boot build targets, DTS, and defconfig skeleton only; leave SD env boot semantics to M02 and install menus to M10.
5. Migration Step M02: review SD U-Boot environment behavior and reset-boot-count before SD boot validation.
6. Migration Step M05: verify AS21xxx driver/firmware package closure against direct 8X DTS and prove or reject AQR firmware applicability.
7. Migration Step M06: review mt76 driver and firmware package closure before enabling Wi-Fi runtime claims.
8. Migration Step M07: review mac80211, hostapd, and wpad-openssl userspace policy separately from M01.
9. Migration Step M08: review HNAT, flow-netlink, and WED/offload behavior only after base wired and Wi-Fi behavior is stable.
10. Migration Step M09: review USB module policy as board extras, not M01 image skeleton.
11. Migration Step M10: review fstools bootparam, dual boot, rootfs selection, NAND/eMMC install, and sysupgrade policy after SD boot is stable.
12. Optional secure boot, firmware encryption, OP-TEE, dm-verity, and anti-rollback support remains out of M01 baseline unless the project explicitly makes secure boot a goal.

## Unreported Minimalism Gate

Result: passed for the formally audited M01 review after content checks.

Minimalism risks checked:

1. `.config` and `.config.old` were used only as clues.
2. Direct 8X image recipe evidence was separated from boot, install, and sysupgrade success claims.
3. U-Boot build selection was separated from SD boot environment and NAND/eMMC install behavior.
4. Package list entries were treated as build-closure hints only, not runtime validation.
5. Secure-boot helper files were isolated from the baseline because direct vendor config has secure boot disabled.
6. Broad wireless, network, acceleration, storage, USB, and board-extra package changes were deferred to their owner steps.
7. MT7987, RFB, and target 25.12 files were used as references only, not as direct 8X authority.
8. Vendor feeds were not copied into the M01 plan.

Remaining risk:

M01 formal no-context audit is completed. Residual risks are deferred to their
listed owner steps, especially M02, M03, M05, M06, M08, M09, and M10.
