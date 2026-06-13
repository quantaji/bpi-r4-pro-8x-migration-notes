# M10: Onboard Storage, Install, And Sysupgrade

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M10-onboard-storage-install-and-sysupgrade.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M10-onboard-storage-install-and-sysupgrade.files.tsv`

Audit status: formal no-context audit round1 completed. Verdicts: agent-1 `accept`, agent-2 `accept-with-minor-edits`, agent-3 `accept-with-minor-edits`. No TSV classification changes were required; only minor markdown wording remediation was applied after audit.

No migration code was written, no image was compiled, no NAND/eMMC write was attempted, and no install, sysupgrade, or runtime storage success is claimed by this review.

## Scope

M10 is the persistent-storage review step. It covers direct 8X evidence for SPI-NAND, eMMC, SD-derived installer payloads, U-Boot storage layout, FIT/sysupgrade artifacts, factory install behavior, UBI/rootfs selection, and the kernel/fstools pieces needed to understand those paths.

The safety order for any later implementation remains:

1. SD evidence and recovery confidence first.
2. SPI-NAND install/sysupgrade before eMMC.
3. eMMC write path only after recovery strategy is validated.

Out of scope:

- Writing NAND or eMMC.
- Declaring sysupgrade, factory install, or onboard boot success.
- Treating SD no-install boot as proof of NAND/eMMC install.
- Treating RFB, MT7987, R4Lite, or MT7988D storage layouts as direct 8X truth.
- Pulling wired, Wi-Fi, USB, fan, or acceleration runtime behavior into M10.

## Structural Summary

| Item | Count |
| --- | ---: |
| M10 JSON files | 43 |
| M10 TSV rows | 43 |
| Feature assignments | 65 |
| JSON status A | 31 |
| JSON status M | 12 |
| JSON route assignments primary | 63 |
| JSON route assignments review-only | 2 |

Disposition counts:

| Disposition | Count | Meaning in this draft |
| --- | ---: | --- |
| `needs-evidence` | 16 | High-risk storage/sysupgrade/install behavior requiring target comparison or runtime/recovery proof before migration. |
| `review-only` | 25 | Supporting context or route-class bleed that must not drive M10 migration by itself. |
| `static-only` | 2 | Direct 8X DTS storage topology recorded without runtime/install claims. |

Owner counts:

| Owner | Count |
| --- | ---: |
| `M10` | 43 |

## Input Checklist

U-Boot/recovery/storage layout:

- `000033`

Direct 8X SD/eMMC/base DTS:

- `000855`, `000857`, `000858`, `000859`

Sysupgrade/image/platform scripts:

- `000028`, `000031`, `000823`, `000966`, `000969`, `000970`, `000971`, `000972`

fstools dual-boot / factory install / UBI / fitblk:

- `000811`, `000812`, `001131`, `001132`, `001133`

SPI-NAND/SPI-NOR kernel patches:

- `001141`, `001142`, `001143`, `001144`, `001145`

RFB/MT7987/Lite supporting storage overlays and SoC storage context:

- `000827`, `000829`, `000832`, `000842`, `000843`, `000845`, `000846`, `000847`, `000851`, `000852`
- `000860`, `000861`, `000869`, `000870`, `000872`, `000873`, `000874`, `000875`, `000876`, `000878`

## Direct 8X Evidence

`000859` is the direct 8X base DTS storage anchor. It sets `ubi.block=0,firmware root=/dev/fit0`, declares `rootdisk-spim-nand = <&ubi_rootfs>`, enables SPI-NAND, and defines fixed partitions for `bl2`, `Factory`, `ubi`, UBI volumes `ubootenv`, `ubootenv2`, and `fit`, plus the `nandflash` span. This is `static-only`: it records topology, not write safety.

`000855` is the direct 8X eMMC overlay. It targets `mmc@11230000`, uses 8-bit non-removable eMMC, HS200/HS400 properties, `ubootenv`, `production`, and `rootdisk-emmc`. This is also `static-only`; eMMC write/install is still gated behind SD and SPI-NAND recovery confidence.

`000857` is the direct 8X SD overlay. M02 owns no-install SD boot. M10 uses it only to compare shared MMC controller use, `ubootenv`, `production`, and `rootdisk-sd` naming.

`000033` is the direct 8X U-Boot high-risk row. It contains eMMC, SD, and SPI-NAND defconfigs and env files. The envs include `mmc erase/write`, `mtd erase/write`, `ubi create/write`, SD-to-NAND install, and NAND-to-eMMC install commands. This row remains `needs-evidence` because the commands are authoritative evidence of vendor intent but not safe acceptance evidence.

`000972` is the direct 8X image artifact high-risk row. It creates the 8X GPT helper, eMMC GPT/preloader/FIP/image artifacts, SD image payload areas for SNAND and eMMC install, SNAND factory image, UBINIZE `fip` and `recovery` parts, and `sysupgrade.itb`. This row remains `needs-evidence`; artifact names and offsets do not prove boot, install, or sysupgrade success.

## Topic Summary

### U-Boot Storage Layout

`000033` is the central U-Boot storage-layout evidence. The review preserves these facts:

- eMMC env defines commands to load/attempt production/recovery from eMMC partitions and can write BL2, FIP, production, and recovery.
- SD env defines commands to load/attempt production/recovery from SD and includes an install-to-NAND path.
- SPI-NAND env defines commands to load/attempt FIT/recovery from UBI and includes install-to-eMMC behavior.
- All destructive U-Boot menu actions require later recovery-backed validation before migration.

### DTS Storage Topology

Direct 8X storage topology is limited to `000855`, `000857`, and `000859`. Non-8X MT7987, R4Lite, RFB, and MT7988D storage overlays are `review-only`. They help identify common MediaTek naming patterns such as `rootdisk-sd`, `rootdisk-emmc`, `rootdisk-spim-nand`, `ubootenv`, `production`, `FIP`, `Factory`, and UBI `fit`, but they do not decide 8X layout.

### Sysupgrade And Image Artifacts

`000028`, `000823`, `000969`, and `000970` add optional secure-boot, encrypted FIT, anti-rollback, OP-TEE, hashed squashfs, and ramdisk-rootdev behavior. These rows are `needs-evidence` because they can affect sysupgrade artifact semantics but direct 8X default policy is not proven.

`000966` adds platform upgrade routing around `fitblk`, `dmsetup`, `CI_METHOD`, eMMC, default, and UBI flows for RFB boards. It does not explicitly match the 8X board, while direct vendor `mtk_mmc.sh` and `mtk_nand.sh` show high-risk `dd`, `ubiupdatevol`, `fw_setenv`, and rootfs_data flows. Therefore it remains `needs-evidence`.

`000971` is MT7988D RFB image context only.

### fstools / UBI / fitblk

`000811` and `000812` introduce a bootparam library, block-device hiding, `rootfs_data` selection, `no-split-fitrw`, `boot-rootfs_data-part`, and rootdisk/UBI mount behavior changes. These are persistent runtime policy changes and remain `needs-evidence`.

`001131`, `001132`, and `001133` alter kernel UBI/rootdev/fitblk behavior around dual boot, `no_default_rootdev`, and `mediatek,no-split-fitrw`. They are high-risk M10 rows and remain `needs-evidence`.

### SPI-NAND And SPI-NOR

`001141`, `001142`, and `001143` are SPI-NAND boot-risk rows. `001143` is the largest: it adds CASN page detection/recovery, advanced ECC status parsing, CASN OOB layout, read/write/update variants, and CASN-based spinand init with read-ID fallback. M10 must identify the actual 8X SPI-NAND part and target 6.12 support before migrating any of this.

`001144` and `001145` are SPI-NOR review-only rows. Direct 8X evidence does not show SPI-NOR as the rootdisk path.

## High-Risk Rows

- `000033`: direct 8X U-Boot install/write menus.
- `000855`: direct 8X eMMC topology; static only.
- `000859`: direct 8X SPI-NAND/UBI topology; static only.
- `000966`: platform sysupgrade path lacks explicit 8X board match.
- `000972`: direct 8X GPT, SD, eMMC, SNAND, and sysupgrade artifact recipe.
- `000811`, `000812`, `001131`, `001132`, `001133`: fstools/kernel dual-boot/rootfs policy.
- `001141`, `001142`, `001143`: SPI-NAND boot support and CASN behavior.

## Secondary Review Handoffs

| File ID | Primary in M10 | Secondary owner(s) | Reason |
| --- | --- | --- | --- |
| `000033` | U-Boot storage layout and install-menu evidence | M02 | SD no-install boot semantics were reviewed in M02; M10 must not reopen M02 as install proof. |
| `000857` | SD rootdisk naming context only | M02 | M02 owns SD no-install boot; M10 only checks persistent partition/sysupgrade implications. |
| `000858` | none, route bleed only | M06 | Wi-Fi hardware overlay is M06; M10 records that no storage behavior is present. |
| `000859` | SPI-NAND/rootdisk topology | M03, M04, M05, M06, M09 | Same direct 8X DTS also contains board identity, wired, Wi-Fi, and board-extra content. |
| `000966` | sysupgrade platform logic | M11 | Final release validation must exercise sysupgrade after implementation. |
| `000972` | image artifacts and persistent storage layout | M01, M02, M05, M06, M08, M09, M11 | M01 owns image skeleton, M02 SD boot artifacts, M05/M06/M08/M09 package/runtime side effects, and M11 final validation. |
| `001144`, `001145` | SPI-NOR review-only | none | No direct 8X SPI-NOR rootdisk evidence. |

## TODOs

1. Verify actual 8X SPI-NAND part and whether CASN is required before deciding `001141`-`001143`.
2. Compare target 25.12 kernel UBI, fitblk, and fstools behavior against `001131`-`001133` and `000812`.
3. Design an explicit 8X platform.sh sysupgrade case before using `000966`.
4. Split `000033` U-Boot evidence into bootconf/rootdisk selection, recovery boot, NAND write, and eMMC write tasks.
5. Validate `000972` GPT offsets and SD install payload layout against U-Boot env expectations.
6. Keep eMMC write path disabled until SD recovery and SPI-NAND recovery confidence are established.
7. Decide whether optional secure boot, encrypted FIT, anti-rollback, and OP-TEE image behavior from `000028`, `000823`, `000969`, and `000970` is in scope.
8. Ensure non-8X RFB/MT7987/Lite layouts remain supporting evidence only during implementation.

## Unreported Minimalism Gate

Gate result: pass for round1-audited review. This review does not silently use a minimal-storage shortcut:

- Direct 8X U-Boot env, DTS, and image recipe rows were read before classification.
- Destructive write/install paths are explicitly `needs-evidence`, not accepted as vendor truth.
- Direct DTS topology is only `static-only`, with runtime and write TODOs.
- Non-8X RFB/MT7987/R4Lite storage layouts are retained as `review-only` evidence instead of being copied or dropped from filename alone.
- Optional secure boot/encryption/anti-rollback rows are not treated as successful sysupgrade behavior.

## Remaining Risk

Formal no-context audit round1 is completed. M10 still has implementation and runtime storage-write risk around SPI-NAND CASN support, UBI volume policy, rootfs_data preservation, fitblk split/no-split behavior, U-Boot install menu safety, SD image install payloads, platform sysupgrade matching, and eMMC write recovery. This review still does not prove NAND/eMMC install, sysupgrade, or onboard boot success.

## Next Audit Instructions

No-context auditors should verify:

- TSV coverage against the 43-file M10 JSON.
- Exact parity for `status`, `path`, `file_kind`, `route_classes`, and `features`.
- Whether every `needs-evidence` and `static-only` row has an actionable TODO.
- Direct 8X evidence for `000033`, `000855`, `000857`, `000859`, and `000972`.
- That `000966` is not accepted as direct 8X platform logic without an explicit 8X board case.
- That non-8X/RFB/MT7987/R4Lite rows are not promoted to 8X hardware truth.
- That no install, sysupgrade, NAND/eMMC write, or runtime success is claimed.
