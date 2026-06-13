Verdict: `accept`

Evidence Read:
- Artifacts: `M10-onboard-storage-install-and-sysupgrade.md`, `M10-onboard-storage-install-and-sysupgrade.files.tsv`, M10 routing JSON, `step-file-index.tsv`.
- Diff/source bodies inspected under `analysis/diffsets/8x-vs-openwrt24-base/files/`: all 43 TSV row patch files. For broad SoC DTSI rows, I read the storage-relevant body sections found by full-file search.
- Direct vendor source inspected: 8X U-Boot patch, direct 8X DTS/eMMC/SD/Wi-Fi files, vendor `filogic.mk`, vendor `platform.sh`, `mtk_mmc.sh`, `mtk_nand.sh`.
- Target 25.12 inspected: `target/linux/mediatek/filogic/base-files/lib/upgrade/platform.sh`, `target/linux/mediatek/image/filogic.mk`, and target DTS tree search for `bpi-r4-pro-8x`/`r4-pro` evidence. No target direct 8X platform/image/DTS match was found.
- No prior M10 audit logs were read.

Structural Checks:
- PASS: TSV has 43 data rows, 44 lines including header.
- PASS: JSON has `file_count=43`, `assignment_count=65`, status counts `A=31`, `M=12`, route class counts `primary=63`, `review-only=2`.
- PASS: no missing, extra, or duplicate `file_id`.
- PASS: exact TSV match to JSON for `status`, `path`, `file_kind`, `features`, `route_classes`.
- PASS: all dispositions valid: `needs-evidence=16`, `review-only=25`, `static-only=2`.
- PASS: all `owner_step` values are `M10`.
- PASS: every `needs-evidence` and `static-only` row has a clear TODO.

Findings Ordered By Severity:
- No blocking findings.
- No revise-before-accept findings.
- No minor safety findings. I did not find title-only, filename-only, or subject-only classification in the rows inspected.

Common High-risk Findings:
- `000033`, TSV line 4: correct `needs-evidence`. Direct 8X U-Boot envs contain destructive `mmc erase/write`, `mtd erase/write`, `ubi create/write`, SD-to-NAND install, and NAND-to-eMMC install flows. Review does not accept these as safe.
- `000855`, line 18: correct `static-only`. Direct 8X eMMC overlay records topology only; TODO preserves eMMC write/install validation after SD and SPI-NAND confidence.
- `000857`, line 19: correct `review-only` for M10. Direct 8X SD overlay is M02 no-install boot context; M10 only uses persistent partition/rootdisk naming.
- `000859`, line 21: correct `static-only`. Direct 8X base DTS records SPI-NAND/UBI/rootdisk topology without claiming NAND write or boot success.
- `000966`, line 32: correct `needs-evidence`. Vendor and target platform logic match RFB boards, not direct 8X; vendor `mtk_mmc.sh`/`mtk_nand.sh` contain destructive `dd`, `ubiupdatevol`, `fw_setenv`, rootfs_data flows.
- `000972`, line 36: correct `needs-evidence`. Direct 8X image recipe defines GPT, eMMC, SD install payload, SNAND, UBINIZE, and sysupgrade artifacts; review does not infer install/sysupgrade success.
- `000811`/`000812`, lines 5-6: correct `needs-evidence`; fstools changes affect bootparam, hidden block devices, rootfs_data, no-split-fitrw, UBI/rootdisk behavior.
- `001131`-`001133`, lines 37-39: correct `needs-evidence`; kernel UBI/rootdev/fitblk behavior changes are runtime-persistent policy.
- `001141`-`001143`, lines 40-42: correct `needs-evidence`; SPI-NAND calibration/CASN changes are boot-relevant and require actual flash/target proof.
- `001144`/`001145`, lines 43-44: correct `review-only`; direct 8X evidence shows SPI-NAND rootdisk, not SPI-NOR rootdisk.
- `000028`/`000031`/`000823`/`000969`/`000970`, lines 2-3, 7, 33-34: correct `needs-evidence`; optional secure/FIT/env/image pipeline changes are held open and not treated as required or successful.

Assigned Non-high-risk Findings:
- `000876`, line 30: correct `review-only`; MT7988D GSW overlay has switch/PHY/nvmem content, no storage/rootdisk/install.
- `000878`, line 31: correct `review-only`; MT7988D RFB bootargs are supporting, non-8X evidence.
- `000873`, line 27: correct `review-only`; MT7988A RFB SPI-NOR rootdisk-nor is not direct 8X.
- `000845`, line 13: correct `review-only`; MT7987 SPI-NAND/NMBM-like topology is support only, not 8X truth.
- `000842`, line 11: correct `review-only`; MT7987 pinctrl has storage pin groups only.
- `000843`, line 12: correct `review-only`; MT7987 SD layout is support only.
- `000861`, line 23: correct `review-only`; MT7988A RFB GSW overlay is network/nvmem route bleed.

Self-selected Additional Rows and Findings:
- `000827`, line 8: selected because SPI-NOR layouts can hide rootdisk assumptions. Finding: correct `review-only`; MT7981 RFB NOR is non-8X.
- `000829`, line 9: selected because eMMC topology resembles 8X eMMC. Finding: correct `review-only`; MT7987 eMMC is not direct 8X.
- `000851`, line 16: selected because R4Lite family evidence could be over-promoted. Finding: correct `review-only`; bootargs are MT7987/R4Lite support only.
- `000872`, line 26: selected because RFB SPI-NAND/NMBM could tempt copying. Finding: correct `review-only`; direct 8X base DTS lacks proven NMBM requirement.
- `000971`, line 35: selected because image recipes can be mistaken for sysupgrade proof. Finding: correct `review-only`; MT7988D RFB image recipe is non-8X.

Static-only / Review-only / Needs-evidence Checks:
- `static-only`: PASS for `000855` and `000859`; both record direct 8X topology and preserve future validation work.
- `needs-evidence`: PASS; all 16 held open with TODOs and no silent acceptance.
- `review-only`: PASS; SPI-NOR, RFB, MT7987, MT7988D, and route-bleed rows do not hide direct 8X storage requirements.

Storage Safety Boundary Checks:
- PASS: no NAND/eMMC write path accepted as safe from vendor evidence alone.
- PASS: no sysupgrade success inferred from `filogic.mk` or `platform.sh`.
- PASS: eMMC remains after SD and SPI-NAND recovery confidence.
- PASS: SD no-install boot remains M02; M10 only records persistent implications.

Minimalism Gate:
- PASS. The matrix does not silently use a minimal shortcut. Direct 8X U-Boot, DTS, image recipe, platform/sysupgrade, fstools, kernel UBI/fitblk, and SPI-NAND/CASN evidence are all represented, with destructive paths held open.

No-Issue Confirmations:
- No direct 8X SPI-NOR requirement found.
- No review-only row inspected promoted non-8X evidence to 8X truth.
- No wording found that claims NAND/eMMC/sysupgrade/install success.
- No row appeared classified by filename/title alone.

Residual Risk:
Implementation remains risky around U-Boot destructive menus, GPT offsets, SD install payloads, SPI-NAND CASN need, UBI volume/rootfs_data policy, platform sysupgrade board matching, and eMMC recovery. These are correctly recorded as future evidence/implementation risks, not accepted behavior.
