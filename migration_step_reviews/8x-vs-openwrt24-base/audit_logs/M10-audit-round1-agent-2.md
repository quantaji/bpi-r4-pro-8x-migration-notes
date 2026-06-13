**Verdict: accept-with-minor-edits**

**Evidence Read**

Artifact inputs inspected:
- `migration_step_reviews/8x-vs-openwrt24-base/M10-onboard-storage-install-and-sysupgrade.md`
- `migration_step_reviews/8x-vs-openwrt24-base/M10-onboard-storage-install-and-sysupgrade.files.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M10-onboard-storage-install-and-sysupgrade.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`

Direct 8X vendor source inspected:
- `package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch`
- `target/linux/mediatek/dts/mt7988a-bananapi-bpi-r4-pro-8x.dts`
- `target/linux/mediatek/dts/mt7988a-bananapi-bpi-r4-pro-8x-emmc.dtso`
- `target/linux/mediatek/dts/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso`
- `target/linux/mediatek/dts/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`
- `target/linux/mediatek/image/filogic.mk`

Diffset patches inspected:
- `include/image-commands.mk.patch`
- `package/boot/uboot-envtools/files/mediatek_filogic.patch`
- `package/system/fstools/Makefile.patch`
- `package/system/fstools/patches/0001-add-support-for-dual-boot.patch.patch`
- `scripts/mkits.sh.patch`
- `target/linux/mediatek/filogic/base-files/lib/upgrade/platform.sh.patch`
- `target/linux/mediatek/filogic/base-files/lib/upgrade/mtk_mmc.sh.patch`
- `target/linux/mediatek/filogic/base-files/lib/upgrade/mtk_nand.sh.patch`
- `target/linux/mediatek/image/Config.in.patch`
- `target/linux/mediatek/image/Makefile.patch`
- `target/linux/mediatek/image/filogic.mk.patch`
- `target/linux/mediatek/image/filogic-extra.mk.patch`
- kernel patches `001131`-`001133`, SPI/SPI-NAND patches `001141`-`001143`, SPI-NOR patches `001144`-`001145`

Assigned and additional source rows inspected:
- `mt7988a-rfb-spim-nand-nmbm.dtso`, `mt7988a.dtsi`, `mt7988a-rfb-mxl86252.dts`, `mt7988a-rfb-sd.dtso`, `mt7987.dtsi`, `mt7987a-bananapi-bpi-r4-lite.dts`, `mt7988a-rfb-emmc.dtso`
- self-selected: `mt7981-rfb-spim-nor.dtso`, `mt7987-spim-nand.dtso`, `mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`, `mt7988a-rfb-spim-nor.dtso`, `filogic-extra.mk.patch`

Target OpenWrt 25.12 inspected:
- `target/linux/mediatek/filogic/base-files/lib/upgrade/platform.sh`
- `target/linux/mediatek/image/filogic.mk`
- repository search for `bananapi,bpi-r4-pro-8x`, `bpi-r4-pro-8x`, `BPI-R4-PRO-8X`, `r4pro`: no matches.

**Structural Checks**

- PASS: TSV has 43 data rows.
- PASS: JSON reports 43 files and 65 assignments.
- PASS: no missing, extra, or duplicate `file_id`.
- PASS: TSV exactly matches JSON for `status`, `path`, `file_kind`, `features`, and `route_classes`.
- PASS: all dispositions are valid: `needs-evidence`, `static-only`, `review-only`.
- PASS: all rows have `owner_step=M10`.
- PASS: every `needs-evidence` and `static-only` row has explicit evidence/TODO text.
- PASS: `step-file-index.tsv` contains the expected 43 M10 rows.

**Findings Ordered By Severity**

1. Minor: `000033`, TSV line 4, MD lines 100-102.
   The review correctly marks direct 8X U-Boot install/write menus as `needs-evidence`, and MD lines 9 and 23-27 clearly disclaim NAND/eMMC/sysupgrade/runtime success. However, MD lines 100-102 use wording such as “eMMC env boots,” “SD env boots,” and “SPI-NAND env boots.” The source only proves U-Boot environment commands and destructive install/write paths exist; it does not prove successful boot/install behavior. Suggested edit: replace “env boots” with “env defines commands to read/attempt boot” or equivalent.

No major or blocking findings found.

**Common High-risk Findings**

- `000028`, TSV line 2: `needs-evidence` is correct. FIT signing/encryption/anti-rollback/rootfs-as-initrd pipeline is high-risk and not accepted as runtime-safe.
- `000031`, TSV line 3: `needs-evidence` is correct. `uboot-envtools` adds board/env/storage handling, but no direct 8X runtime storage safety follows from it.
- `000033`, TSV line 4: `needs-evidence` is correct. Direct 8X U-Boot patch includes destructive eMMC, SPI-NAND, UBI, factory reset, and install paths. Minor wording issue noted above.
- `000811` / `000812`, TSV lines 5-6: `needs-evidence` is correct. fstools dual-boot, boot-param, `rootfs_data`, and `no-split-fitrw` behavior require implementation validation.
- `000823`, TSV line 7: `needs-evidence` is correct. `mkits.sh` secure/encrypted FIT behavior is not proof of install/sysupgrade success.
- `000855`, TSV line 18: `static-only` is acceptable. Direct 8X eMMC DTS records static topology only: eMMC node, ubootenv, production, rootdisk-emmc. It does not hide a claimed safe write path.
- `000857`, TSV line 19: `static-only` is acceptable. Direct 8X SD overlay records SD topology and persistent implications; SD no-install boot remains outside M10 and belongs to M02.
- `000859`, TSV line 21: `needs-evidence` is correct. Direct 8X base DTS contains SPI-NAND, UBI, FIT/rootdisk topology and dual-root hints; this is not merely harmless background.
- `000966`, TSV line 32: `needs-evidence` is correct. Platform sysupgrade patch has no explicit 8X board case; helper scripts contain real write/update behavior and cannot be treated as 8X-safe.
- `000969` / `000970`, TSV lines 33-34: `needs-evidence` is correct. Image config/makefile secure boot, encryption, OP-TEE, anti-rollback, and rootdev conversion need explicit handling.
- `000972`, TSV line 36: `needs-evidence` is correct. Direct 8X image recipe defines GPT, SD/eMMC/SPI-NAND artifacts, sysupgrade ITB, and factory images, but does not prove install or upgrade safety.
- `001131`-`001133`, TSV lines 37-39: `needs-evidence` is correct. Kernel UBI/rootdev/fitblk dual-boot changes alter rootfs and overlay behavior and need validation.
- `001141`-`001143`, TSV lines 40-42: `needs-evidence` is correct. SPI/SPI-NAND/CASN behavior affects boot media reliability and should remain open.
- `001144` / `001145`, TSV lines 43-44: `review-only` is correct. These are SPI-NOR patches; no direct 8X SPI-NOR storage requirement was found.

**Assigned Non-high-risk Findings**

- `000872`, TSV line 26: `review-only` is correct. MT7988A RFB SPI-NAND/NMBM topology supports understanding only, not 8X truth.
- `000875`, TSV line 29: `review-only` is correct. MT7988A SoC controller context only.
- `000869`, TSV line 24: `review-only` is correct. MT7988A RFB DTS is non-8X support context.
- `000870`, TSV line 25: `review-only` is correct. MT7988A RFB SD overlay is not direct 8X evidence.
- `000847`, TSV line 15: `review-only` is correct. MT7987 SoC storage-controller context only.
- `000851`, TSV line 16: `review-only` is correct. R4Lite/MT7987 DTS is not direct 8X evidence.
- `000860`, TSV line 22: `review-only` is correct. MT7988A RFB eMMC topology is support context only.

**Self-selected Additional Rows and Findings**

Exactly five selected, excluding common high-risk and assigned rows:

- `000827`, TSV line 8: selected because non-8X SPI-NOR review-only rows could hide a NOR requirement. Source is MT7981 RFB SPI-NOR only; `review-only` is correct.
- `000845`, TSV line 13: selected because MT7987 SPI-NAND topology resembles 8X NAND topology. Source is MT7987, not 8X; `review-only` is correct.
- `000858`, TSV line 20: selected because it is direct 8X and could hide storage via nvmem. Source is Wi-Fi/EEPROM/PCIe overlay only; no rootdisk/install/partition requirement. Current classification is acceptable.
- `000873`, TSV line 27: selected because MT7988A RFB SPI-NOR could be confused with 8X. Source is non-8X RFB SPI-NOR; `review-only` is correct.
- `000971`, TSV line 35: selected because image recipe/sysupgrade artifacts could be over-promoted. Source is MT7988D RFB image recipe, not direct 8X; `review-only` is correct.

**Static-only / Review-only / Needs-evidence Checks**

- `static-only`: direct 8X DTS rows `000855` and `000857` are static topology records with explicit TODO/evidence. They do not claim NAND/eMMC success.
- `needs-evidence`: high-risk rows are held open and not silently accepted. This is especially important for `000033`, `000859`, `000966`, and `000972`.
- `review-only`: inspected review-only SPI-NOR, RFB, MT7987, MT7988D, and R4Lite rows. No hidden direct 8X storage requirement found.
- No row appeared title-only or filename-only classified among the evaluated rows.

**Storage Safety Boundary Checks**

- PASS: no NAND/eMMC write path is accepted as safe from vendor evidence alone.
- PASS: no sysupgrade success is inferred from `platform.sh` or image recipes.
- PASS: eMMC remains after SD and SPI-NAND recovery confidence in the review text.
- PASS: SD no-install boot remains M02; M10 handles persistent-storage implications only.
- PASS with minor edit: MD safety disclaimers are strong, but `000033` wording should avoid “env boots” phrasing.

**Minimalism Gate**

PASS. The matrix does not appear to use a small/minimal shortcut. Direct 8X DTS rows marked `static-only` are limited to topology; SPI-NOR rows marked `review-only` are non-8X/supporting; RFB/MT7987/MT7988D rows are not used to decide 8X storage truth.

**No-Issue Confirmations**

- No direct 8X SPI-NOR requirement found.
- No direct 8X storage truth was overridden by target OpenWrt 25.12 or vendor-family sources.
- No evidence that `review-only` hides a direct 8X storage/install requirement.
- No evidence that `static-only` hides required rewrite work without TODO.
- No evidence that `needs-evidence` rows are silently accepted as implemented or safe.

**Residual Risk**

The remaining risk is implementation risk, not audit-structure risk: 8X U-Boot destructive menus, SPI-NAND/UBI/rootfs_data behavior, fitblk/no-split handling, CASN/SPI-NAND boot behavior, missing explicit 8X sysupgrade case, GPT/image artifacts, and eMMC write sequencing all still require later proof and recovery validation.
