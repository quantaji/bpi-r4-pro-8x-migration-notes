# M02 Audit Agent 2 Raw Report

Reviewer id: `M02-audit-agent-2`

Agent id: `019ea9c6-795e-7ab3-a6fe-3d2930b720b8`

Verdict: `accept-with-minor-edits`

Note: this file preserves the agent's original feedback. Any line numbers or
comments about audit status refer to the pre-recording draft.

## Raw Feedback

Verdict: `accept-with-minor-edits`

**Structural Checks**
- M02 by-step JSON: 35 files, 41 feature assignments.
- TSV: 35 data rows, no missing/extra/duplicate `file_id`.
- `step-file-index.tsv`: 35 M02 rows, matching the JSON exactly; `001134` appears only under M00.
- TSV fields matched JSON for `file_id`, `status`, `path`, `file_kind`, `route_classes`, and `features`.
- Status split matches: `A=28`, `M=7`.
- Dispositions are legal: `migrate=1`, `rewrite=1`, `review-only=3`, `drop=18`, `defer=12`.
- Owners are legal/reasonable: `M02=23`, `M03=1`, `M06=1`, `M10=10`; all `defer` rows have later owners and TODO/notes coverage.

**Findings**
- Low, [M02-sd-boot-no-install.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.md:137), [M02-sd-boot-no-install.files.tsv](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.files.tsv:3), file_id `000033`: the review identifies SD write-to-SD boot menu entries, but the handoff language emphasizes NAND/eMMC/UBI and does not explicitly name `bootmenu_4/5`, `boot_tftp_production/recovery`, `sdmmc_write_production`, `sdmmc_write_recovery`, and `replacevol` as excluded from M02 no-install boot.
  Why it matters: later implementation could preserve SD write/update menu behavior while thinking only NAND/eMMC install was excluded.
  Recommended fix: add one explicit note that all TFTP/write-to-SD flows are out of M02 and belong to M10/storage-install policy review or another explicit non-M02 install review.

**No-Issue Confirmations**
- `000857` is correctly the only M02 migrate DTSO. `000855` is eMMC context/defer to M10; `000858` is Wi-Fi/defer to M06; RFB/MT7987/Lite DTSOs are not used as 8X truth.
- `000033` is correctly split: SD boot env in M02; install-to-NAND, UBI writes, eMMC install payloads, and persistent storage behavior in M10.
- `000490`-`000493` defer to M10 is justified: direct 8X DTS/DTSO lacks `mediatek,reset-boot-count`, and the init script is property-gated.
- `000811`/`000812` and `001131`-`001133` defer to M10 is reasonable: they are bootparam, dual-boot, UBI/rootfs, or rootfs_data policy, not SD no-install boot.
- `001134` is handled correctly as an M00 handoff, not a TSV row; it should be reviewed before SD/recovery FIT validation, with persistent rootfs/sysupgrade implications handed to M10.
- No filename-only drop/defer problem found; non-8X drops are identified as non-authoritative routing noise, and direct 8X files are inspected.

**Residual Risk**
- Runtime SD boot remains unvalidated: serial log, selected overlay, `/chosen/rootdisk-sd`, FIT/rootfs mapping, and recovery path still need M02 validation.
- M10 must later validate NAND/eMMC install, sysupgrade, dual-boot/rootfs_data policy, and SD artifact install payload areas.
- M03/M06 must still review identity/env and Wi-Fi overlay implications in their own step reviews.
