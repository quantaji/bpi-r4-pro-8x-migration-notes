# Migration Step M02 Batch Review: SD Boot No Install

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M02-sd-boot-no-install.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.files.tsv`

This review is part of Project Phase 2. It does not migrate code.

## Audit Status

This file is the formally audited M02 batch review.

Formal three-agent no-context audit status: completed on 2026-06-08.

| reviewer id | agent id | verdict |
| --- | --- | --- |
| `M02-audit-agent-1` | `019ea9c6-7936-7990-a1a6-945d88708e7e` | `accept` |
| `M02-audit-agent-2` | `019ea9c6-795e-7ab3-a6fe-3d2930b720b8` | `accept-with-minor-edits` |
| `M02-audit-agent-3` | `019ea9c6-7993-70c1-ad8c-9e2d194f3b02` | `accept` |

Second-round no-context re-audit status: completed on 2026-06-08.

| reviewer id | agent id | verdict |
| --- | --- | --- |
| `M02-audit-round2-agent-1` | `019ea9d8-5ea6-70f1-8c86-f1b1230ae920` | `accept` |
| `M02-audit-round2-agent-2` | `019ea9d8-d5c8-7d91-8457-b98410255652` | `accept-with-minor-edits` |
| `M02-audit-round2-agent-3` | `019ea9d9-4bc9-74b2-bfdf-8b06021bbe31` | `accept` |

Third-round no-context re-audit status: completed on 2026-06-08.

| reviewer id | agent id | verdict |
| --- | --- | --- |
| `M02-audit-round3-agent-1` | `019ea9ec-f890-7060-b48c-37fbb97c8773` | `accept` |
| `M02-audit-round3-agent-2` | `019ea9ed-6813-7e43-b54a-8ff36329aa3a` | `accept` |
| `M02-audit-round3-agent-3` | `019ea9ed-d8ab-74f0-8f1d-b36885ccda6e` | `accept` |

Outcome: formal audit completed with one low-severity accepted edit. The
`M02-audit-agent-2` recommendation to explicitly exclude SD write/update flows
from `000033` was accepted and applied to this markdown and the TSV. No audit
recommendations were rejected. No migration code was changed.

Second-round outcome: accepted with one low-severity wording edit. The
`M02-audit-round2-agent-2` recommendation to clarify that `boot_tftp_recovery`
is excluded from M02 migration was accepted and applied to the TODOs. No
second-round audit recommendations were rejected. No migration code was changed.

Third-round outcome: accepted with no findings. No migration code was changed.


First-round formal audit summary:

| reviewer id | verdict | structural checks | actionable findings | main-agent action |
| --- | --- | --- | --- | --- |
| `M02-audit-agent-1` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners. | None. | No change. |
| `M02-audit-agent-2` | `accept-with-minor-edits` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners. | Low: `000033` should explicitly exclude SD write/update flows from M02 no-install boot. | Accepted and applied to this markdown and TSV. |
| `M02-audit-agent-3` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners. | None. | No change. |

Accepted audit changes:

1. `M02-audit-agent-2` recommended naming `000033` SD write/update flows as
   out of M02 no-install boot scope.
2. Main agent accepted the recommendation and updated the `000033` TSV notes,
   Direct 8X U-Boot evidence, Routing Conclusions, Secondary Review Handoffs,
   and TODOs.

Rejected audit changes: none.

Second-round formal audit summary:

| reviewer id | verdict | structural checks | actionable findings | main-agent action |
| --- | --- | --- | --- | --- |
| `M02-audit-round2-agent-1` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners, review organization acceptable. | None. | No change. |
| `M02-audit-round2-agent-2` | `accept-with-minor-edits` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners, review organization acceptable. | Low: TODO 3 still made `boot_tftp_recovery` look like an M02 no-install boot task. | Accepted and applied to TODO 3. |
| `M02-audit-round2-agent-3` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners, review organization acceptable. | None. | No change. |

Accepted second-round audit changes:

1. `M02-audit-round2-agent-2` recommended removing ambiguity around
   `boot_tftp_recovery` in TODO 3.
2. Main agent accepted the recommendation and clarified that M02 audits
   `boot_recovery` as no-install recovery boot evidence, while
   `boot_tftp_recovery` remains excluded from M02 migration as a write/update
   flow.

Rejected second-round audit changes: none.

Third-round formal audit summary:

| reviewer id | verdict | structural checks | actionable findings | main-agent action |
| --- | --- | --- | --- | --- |
| `M02-audit-round3-agent-1` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners, concise summaries accepted. | None. | No change. |
| `M02-audit-round3-agent-2` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners, concise summaries accepted. | None. | No change. |
| `M02-audit-round3-agent-3` | `accept` | Passed: 35/35 TSV coverage, no missing/extra/duplicate, fields matched JSON, legal dispositions/owners, concise summaries accepted. | None. | No change. |

Accepted third-round audit changes: none.

Rejected third-round audit changes: none.

## Review Purpose

Migration Step M02 decides which vendor changes are needed to boot the BPI-R4
Pro 8X from SD card without writing to NAND or eMMC.

M02 answers:

1. which direct 8X SD overlay semantics must be preserved,
2. which U-Boot SD environment behavior is needed for SD no-install boot,
3. which FIT/rootfs or initramfs-recovery behavior must be reviewed before SD/recovery boot validation,
4. which storage, install, sysupgrade, dual-boot, or runtime hardware behavior must be handed to later steps,
5. which RFB, MT7987, BPI-R4 Lite, or non-8X files are only routing noise or background.

## Migration Step Boundary

Allowed in M02:

1. SD boot path review only,
2. direct 8X SD DTSO semantics,
3. direct 8X U-Boot SD environment semantics,
4. FIT initramfs-recovery/rootfs boot evidence needed for SD or recovery boot,
5. SD image artifact semantics needed to understand the boot path,
6. context needed to avoid unsafe NAND/eMMC assumptions.

Not allowed in M02:

1. NAND install behavior,
2. eMMC install behavior,
3. declaring onboard storage install or sysupgrade success,
4. writing to NAND or eMMC,
5. pulling full dual-boot or storage policy into M02,
6. treating RFB, MT7987, or BPI-R4 Lite files as direct 8X authority,
7. treating `.config` or package lists as hardware truth.

## Input Scope

M02 by-step input contains 35 files and 41 feature assignments.

Status split:

| status | file count |
| --- | ---: |
| `A` | 28 |
| `M` | 7 |

Route-class split:

| route class | assignment count |
| --- | ---: |
| `primary` | 32 |
| `supporting` | 6 |
| `deferred` | 3 |

M00 handoff check:

1. M00 has one `owner_step == M02` row outside the M02 by-step JSON: `001134`.
2. `001134` is `target/linux/mediatek/patches-6.6/999-fitblk-01-parse-and-mount-ramdisk.patch`.
3. The TSV remains a strict 35-row matrix for the M02 by-step JSON. `001134` is reviewed in this markdown as M00 handoff evidence so the TSV coverage check still has no extra rows.

## Direct 8X Evidence

Direct 8X SD overlay:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso`

Key evidence checked:

1. compatible is `bananapi,bpi-r4-pro-8x`, `mediatek,mt7988a`,
2. targets `/soc/mmc@11230000`,
3. uses 4-bit SD mode,
4. uses `cd-gpios = <&pio 12 GPIO_ACTIVE_LOW>`,
5. sets `no-mmc`,
6. defines a `ubootenv` partition with U-Boot env layout,
7. defines `sd_rootfs` on partition `production`,
8. sets `/chosen/rootdisk-sd = <&sd_rootfs>`.

Conclusion: this is the primary M02 DTSO input. It can be migrated for SD boot
semantics, but SD boot success still requires later serial/runtime evidence.

Direct 8X eMMC overlay:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-emmc.dtso`

Key evidence checked:

1. targets the same MMC controller path as SD,
2. uses 8-bit non-removable eMMC mode,
3. sets `no-sd` and `no-sdio`,
4. defines an eMMC `ubootenv` partition,
5. sets `/chosen/rootdisk-emmc = <&emmc_rootfs>`.

Conclusion: this is context only for M02. It prevents mixing SD and eMMC modes,
but eMMC runtime, install, and storage behavior belongs to M10.

Direct 8X base DTS:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`

Key evidence checked:

1. board compatible is direct 8X,
2. bootargs include `root=/dev/fit0`,
3. base DTS names `rootdisk-spim-nand = <&ubi_rootfs>`,
4. no `mediatek,dual-boot`, `mediatek,no-split-fitrw`, or `mediatek,reset-boot-count` property was found in the direct 8X DTS/DTSO set.

Conclusion: base DTS is M02 context for rootdisk naming only. Board identity is
M03. NAND/rootfs storage policy is M10.

Direct 8X U-Boot SD environment:

`package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch`

Key evidence checked:

1. adds `bananapi_bpi-r4-pro-8x_sdmmc_env`,
2. `bootcmd` runs recovery when `pstore check` is true, otherwise runs SD boot,
3. production SD boot uses `bootconf_sd`,
4. recovery boot and TFTP recovery use `bootconf_emmc`,
5. SD boot menu includes write-to-SD entries and install-to-NAND behavior,
6. install flow reads SNAND/eMMC install payloads from the SD `install` partition and writes UBI/eMMC-related targets,
7. `bootmenu_4/5`, `boot_tftp_production`, `boot_tftp_recovery`, `sdmmc_write_production`, `sdmmc_write_recovery`, and `replacevol` are write/update flows, not M02 no-install boot.

Conclusion: M02 owns the SD boot environment semantics needed for no-install
boot. Any install, UBI write, eMMC install payload, SD write/update flow, or
persistent storage action is M10 or a later explicit install review.

Direct 8X image recipe context:

`target/linux/mediatek/image/filogic.mk`

Key evidence checked:

1. 8X image recipe emits `sdcard.img.gz`,
2. SD image includes SD BL2/FIP and initramfs-recovery payload,
3. the same SD artifact also carries SNAND/eMMC boot and install payload areas,
4. GPT/partition layout is needed to understand SD boot reads, but not to claim install success.

Conclusion: M02 may use SD image artifact semantics as boot-path evidence only.
Install and sysupgrade semantics remain M10.

M00 handoff evidence:

`target/linux/mediatek/patches-6.6/999-fitblk-01-parse-and-mount-ramdisk.patch`

Key evidence checked:

1. M00 moved `001134` to M02 because FIT ramdisk/rootfs parsing can affect SD/recovery boot before onboard install work,
2. the patch lets fitblk treat FIT `ramdisk` images similarly to `loadable` images,
3. the patch lets FIT image type `ramdisk` be mapped as a rootfs partition,
4. this can affect initramfs-recovery/rootfs behavior used by the SD recovery path.

Conclusion: `001134` is not in the M02 by-step JSON and is not in the TSV, but
M02 must review it before SD/recovery FIT boot validation. Persistent
rootfs/sysupgrade implications are M10.

Reset-boot-count evidence:

`package/mtk/reset-boot-count`

Key evidence checked:

1. init script loads the module only when `/sys/firmware/devicetree/base/mediatek,reset-boot-count` exists,
2. direct 8X DTS/DTSO evidence does not provide `mediatek,reset-boot-count`,
3. the module resets MTK non-reset boot count registers through SMC,
4. no direct 8X SD boot dependency was proven.

Conclusion: reset-boot-count is not an M02 SD no-install requirement. M10 may
revisit it only if persistent dual-boot or A/B bootcount policy is deliberately
introduced.

## Disposition Summary

The TSV review matrix assigns one disposition per M02 by-step file.

| disposition | file count | meaning in M02 |
| --- | ---: | --- |
| `migrate` | 1 | Direct 8X SD DTSO semantics to preserve for SD no-install boot. |
| `rewrite` | 1 | Direct 8X U-Boot SD environment semantics to preserve, with install/storage behavior split out. |
| `review-only` | 3 | Direct or same-SoC context only; no M02 migration action. |
| `drop` | 18 | Non-8X RFB/MT7987/BPI-R4 Lite routing noise or files outside SD boot scope. |
| `defer` | 12 | Real follow-up input owned by later migration steps. |

Owner split:

| owner step | file count | reason |
| --- | ---: | --- |
| `M02` | 23 | M02 migration inputs, review-only context, and current-step drops. |
| `M03` | 1 | Linux uboot-envtools/env identity handling. |
| `M06` | 1 | Direct 8X Wi-Fi overlay routed by storage keyword bleed. |
| `M10` | 10 | eMMC, reset-boot-count, fstools, dual-boot, rootfs, NAND/eMMC install, and sysupgrade policy. |

## Evidence Groups

| group | count | disposition pattern |
| --- | ---: | --- |
| `linux-uboot-envtools-boundary` | 1 | `defer` to M03, with M10 secondary review noted |
| `direct-8x-uboot-sd-env` | 1 | `rewrite` in M02 |
| `recovery-boot-count-boundary` | 4 | `defer` to M10 |
| `storage-policy-boundary` | 5 | `defer` to M10 |
| `non-8x-reference-storage` | 1 | `drop` |
| `mt7987-reference-storage` | 4 | `drop` |
| `mt7987-reference-network-drop` | 1 | `drop` |
| `mt7987-reference-soc` | 2 | `drop` |
| `r4-lite-reference` | 1 | `drop` |
| `mt7987-reference-board` | 1 | `drop` |
| `direct-8x-emmc-context` | 1 | `defer` to M10 |
| `direct-8x-sd-overlay` | 1 | `migrate` in M02 |
| `direct-8x-wifi-overlay` | 1 | `defer` to M06 |
| `direct-8x-base-dts-context` | 1 | `review-only` in M02 |
| `mt7988-rfb-storage-reference` | 4 | `drop` or `review-only` in M02 |
| `mt7988-rfb-network-drop` | 1 | `drop` |
| `mt7988-rfb-wired-drop` | 1 | `drop` |
| `mt7988-rfb-board-reference` | 1 | `drop` |
| `mt7988-soc-reference` | 1 | `review-only` in M02 |
| `mt7988d-rfb-drop` | 2 | `drop` |

## Routing Conclusions

1. The direct 8X SD DTSO is the only DTSO to migrate in M02.
2. The direct 8X U-Boot SD environment must be rewritten for target 25.12 structure and bounded to no-install SD boot.
3. U-Boot install menus, UBI writes, SNAND/eMMC install payloads, and sysupgrade/storage semantics are M10.
4. U-Boot SD write/update flows, including `bootmenu_4/5`, `boot_tftp_production`, `boot_tftp_recovery`, `sdmmc_write_production`, `sdmmc_write_recovery`, and `replacevol`, are not M02 no-install boot.
5. `001134` fitblk ramdisk/rootfs behavior must be reviewed before SD/recovery FIT boot validation, even though it entered M02 through M00 handoff rather than the M02 by-step JSON.
6. Reset-boot-count is not required for M02 based on direct 8X evidence; M10 may revisit it for persistent dual-boot policy.
7. Fstools bootparam and kernel dual-boot/rootfs patches are M10, not M02.
8. eMMC overlay is direct 8X evidence but only context for M02; do not migrate or validate eMMC in this step.
9. MT7987, MT7988 RFB, MT7988D RFB, and BPI-R4 Lite files cannot decide 8X SD hardware truth.
10. Target 25.12 BPI-R4 files are useful for style and structure, but not for 8X hardware facts.

## Secondary Review Handoffs

The TSV schema has one `owner_step` per file. Mixed-owner files are therefore
kept under their primary owner and called out here.

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `000031` | `M03` | `M10` | Linux uboot-envtools/env access affects identity in M03 and persistent env/storage policy in M10; it is not required to prove M02 SD boot. |
| `000033` | `M02` | `M10` | SD U-Boot env belongs to M02; install-to-NAND, UBI writes, eMMC install payloads, storage-layout behavior, and SD write/update flows such as `bootmenu_4/5`, `boot_tftp_production`, `boot_tftp_recovery`, `sdmmc_write_production`, `sdmmc_write_recovery`, and `replacevol` belong to M10 or a later explicit install review. |
| `000490`-`000493` | `M10` | none | reset-boot-count is not required for SD no-install boot, but M10 may revisit it if persistent dual-boot bootcount policy is introduced. |
| `000811` | `M10` | none | fstools bootparam library and dependencies are storage/rootfs policy, not SD boot minimum. |
| `000812` | `M10` | none | dual-boot fstools behavior is persistent storage policy, not M02 no-install boot. |
| `000855` | `M10` | `M02` context only | eMMC overlay confirms shared MMC controller but eMMC runtime/install belongs to M10. |
| `000857` | `M02` | `M10` | SD rootdisk and `production` partition naming are required for M02; persistent partition/sysupgrade implications must be checked by M10. |
| `000858` | `M06` | none | direct 8X Wi-Fi overlay is routed into M02 only by keyword bleed. |
| `000859` | `M02` | `M03`, `M10` | base DTS gives board compatible and rootdisk context; board identity is M03, NAND/rootfs storage is M10. |
| `001131`-`001133` | `M10` | none | dual-boot and rootfs policy patches require M10 storage/install/sysupgrade review. |
| `001134` | `M02` handoff from M00 | `M10` | fitblk ramdisk parsing may affect SD/recovery boot, while persistent rootfs/sysupgrade implications remain M10. |

## TODOs

1. Migration Step M02: port direct 8X SD overlay semantics from `000857` into target 25.12 style.
2. Migration Step M02: rewrite direct 8X SD U-Boot environment behavior from `000033`, preserving no-install SD production/recovery boot semantics only.
3. Migration Step M02: explicitly audit `boot_recovery` as no-install recovery boot evidence, because vendor SD env uses `bootconf_emmc` while production uses `bootconf_sd`; `boot_tftp_recovery` is excluded from M02 migration as a write/update flow.
4. Migration Step M10 or a later explicit install review: own `000033` SD write/update flows including `bootmenu_4/5`, `boot_tftp_production`, `boot_tftp_recovery`, `sdmmc_write_production`, `sdmmc_write_recovery`, and `replacevol`.
5. Migration Step M02: review M00 handoff `001134` before SD/recovery FIT boot validation; do not defer this past SD boot.
6. Migration Step M03: decide whether 8X needs a uboot-envtools board case for early env/ethaddr handling.
7. Migration Step M06: own the 8X Wi-Fi overlay and any storage-tag keyword bleed from EEPROM data.
8. Migration Step M10: own reset-boot-count if persistent dual-boot bootcount policy is introduced.
9. Migration Step M10: own fstools bootparam, kernel dual-boot/rootfs patches, eMMC overlay, NAND/eMMC install, sysupgrade, and persistent storage policy.
10. Migration Step M10: review SD artifact install payload areas from the image recipe before any install path is attempted.

## Unreported Minimalism Gate

Result: passed for the main-agent M02 draft after content checks.

Minimalism risks checked:

1. Direct 8X SD overlay was inspected before marking it as the only M02 DTSO migration input.
2. Direct 8X U-Boot SD env was inspected before splitting boot semantics from install/storage commands.
3. The reset-boot-count package was checked against direct 8X DTS properties before being deferred out of M02.
4. Fstools and kernel dual-boot patches were checked for required DTS properties before deferring to M10.
5. `001134` from M00 handoff was not ignored merely because it is absent from the M02 by-step JSON.
6. MT7987, RFB, and BPI-R4 Lite files were not used as direct 8X authority.
7. Target 25.12 BPI-R4 files were used for structure only, not for 8X hardware truth.
8. No SD boot, recovery, sysupgrade, NAND/eMMC install, or runtime hardware success is claimed by this review.

Remaining risk:

Formal three-agent no-context audit is completed. One low-severity
`M02-audit-agent-2` finding was accepted and applied. Runtime SD boot, serial
log validation, FIT recovery behavior, and all install/storage/sysupgrade
behavior remain unvalidated and are deferred to the listed owner steps,
especially M02 validation follow-up and M03/M06/M10.
