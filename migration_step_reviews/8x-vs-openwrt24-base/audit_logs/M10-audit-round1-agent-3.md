Verdict: `accept-with-minor-edits`

**Evidence Read**
Reviewed the M10 artifacts, routing JSON, M10 rows in `step-file-index.tsv`, and diff/source bodies for all required rows. Key source evidence included direct 8X vendor U-Boot patch, 8X DTS/DTBOs, `filogic.mk`, `platform.sh`, `mtk_mmc.sh`, `mtk_nand.sh`, `uboot-envtools`, fstools dual-boot patch, image/FIT patches, and SPI/UBI/kernel patches. Target 25.12 evidence checked: filogic `platform.sh`, `uboot-tools/uboot-envtools/files/mediatek_filogic`, image/mkits files, and SPI calibration patch context.

**Structural Checks**
PASS:
- TSV has 43 data rows.
- JSON reports 43 files / 65 feature assignments.
- `step-file-index.tsv` has 43 M10 rows.
- No duplicate TSV `file_id`.
- No TSV vs JSON mismatch for `status`, `path`, `file_kind`, `features`, or `route_classes`.
- Valid dispositions only: `needs-evidence` 16, `review-only` 25, `static-only` 2.
- Owner is `M10` for all 43 rows.
- Every `needs-evidence` and `static-only` row has non-empty evidence plus an explicit TODO.

**Findings Ordered By Severity**
1. MINOR, `000033`, report wording: `M10-onboard-storage-install-and-sysupgrade.md` lines 100-102 say eMMC/SD/SPI-NAND envs “boot” production/recovery paths. The surrounding text correctly says no runtime success is claimed, but this wording is close to implying boot success. Recommend changing to “defines commands to load/attempt boot” or similar. Not blocking because lines 9, 23-25, 90-92, and 167-174 preserve the safety boundary.

**Common High-risk Findings**
No blocking issues.
- `000033` is correctly `needs-evidence`; vendor U-Boot contains destructive `mmc erase/write`, `mtd erase/write`, UBI create/write, SD-to-NAND, and NAND-to-eMMC flows.
- `000855` static-only is correct for direct 8X eMMC topology; it does not hide eMMC write validation.
- `000857` review-only is correct: direct 8X SD overlay is M02 boot context, M10 persistent-storage context only.
- `000859` static-only is correct for direct 8X SPI-NAND/UBI topology; TODOs cover partition/UBI/rootfs/recovery work.
- `000966` is correctly held open; vendor and target platform scripts lack explicit 8X board handling, and helper scripts contain real write paths.
- `000972` is correctly `needs-evidence`; image/GPT/artifact recipes do not prove install/sysupgrade success.
- `000811`, `000812`, `001131`-`001133`, `001141`-`001143` are correctly `needs-evidence`.
- `001144`/`001145` are correctly `review-only`; no direct 8X SPI-NOR rootdisk requirement found.

**Assigned Non-high-risk Findings**
No issues. Rows `000827`, `000829`, `000832`, `000846`, `000852`, `000858`, and `000971` are correctly scoped as supporting context or route-class bleed. `000858` is direct 8X but Wi-Fi/nvmem only, not storage.

**Self-selected Additional Rows**
Selected `000843`, `000845`, `000851`, `000860`, `000872` because they are storage-looking SD/eMMC/SPI-NAND/RFB-family rows that could be over-promoted.
Findings: no issues. All are non-8X or RFB/R4Lite support only. `000872` includes NMBM but direct 8X DTS `000859` does not prove NMBM, so `review-only` is correct.

**Static-only / Review-only / Needs-evidence Checks**
PASS. Static-only rows do not hide future work. Needs-evidence rows remain open with actionable TODOs. Review-only rows are supporting, non-8X, SPI-NOR, or keyword-bleed context; no hidden direct 8X storage requirement found.

**Storage Safety Boundary Checks**
PASS with the minor wording edit above. No NAND/eMMC/sysupgrade/install success is accepted. eMMC remains gated after SD and SPI-NAND recovery confidence. SD no-install boot remains outside M10 except for persistent implications.

**Minimalism Gate**
PASS. The matrix does not silently take a minimal shortcut: direct 8X U-Boot/DTS/image evidence is retained, destructive write paths are not accepted, SPI-NOR/RFB/MT7987 rows are not promoted, and optional secure/encrypted FIT behavior remains open.

**No-Issue Confirmations**
No title-only or filename-only classifications found in inspected rows. No review-only row hides a direct 8X storage requirement. No `needs-evidence` row should be accepted now.

**Residual Risk**
Implementation risk remains for U-Boot install splitting, 8X platform sysupgrade design, SPI-NAND CASN need, UBI/rootfs_data policy, GPT/payload offsets, and eMMC recovery. These are correctly left outside acceptance.
