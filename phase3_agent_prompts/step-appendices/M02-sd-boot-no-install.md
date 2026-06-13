# M02 Appendix: SD Boot, No Install

This appendix is used with `../shared-phase3-agent-base.md` for Phase 3 M02.

M02 is a reading/design/implementation step for SD boot only. A reading-only
preflight must not edit files, build, commit, push, or start runtime testing.

## Scope Lock

M02 should make the BPI-R4 Pro 8X SD-card image bootable from SD and collect
evidence for that claim.

M02 may touch the SD boot path only:

- SD image boot artifact semantics,
- SD-related U-Boot environment behavior,
- SD overlay/rootdisk semantics needed for Linux boot,
- FIT initramfs/recovery/rootfs behavior needed for SD boot,
- serial/runtime evidence proving SD boot.

M02 must not implement or claim:

- NAND install,
- eMMC install,
- sysupgrade success,
- onboard storage write safety,
- final GPT/layout policy,
- wired management readiness,
- full SFP/10G behavior,
- Wi-Fi behavior,
- board identity/factory MAC final policy,
- release readiness.

Any vendor behavior that writes to NAND/eMMC, rewrites SD production/recovery
partitions, creates/removes UBI volumes, saves U-Boot env, or installs from SD
to onboard storage belongs to M10 unless the user explicitly reopens scope.

## Required Step Documents

Read these exact documents before making an M02 design:

- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_agent_prompts/shared-phase3-agent-base.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/project_guidelines.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_roadmap.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/repository_map.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_implementation_protocol.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_external_issue_watchlist.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_commit_notes/M01/1192774440-build-skeleton.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_supervisor_notes/M01-dts-source-boundary.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.files.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/P2-owner-step-worklist.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/P2-unacknowledged-owner-handoffs.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/P2-cross-step-coherence-audit.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/phase3-worklists/8x-vs-openwrt24-base/M02.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/phase3-worklists/8x-vs-openwrt24-base/unacknowledged-handoffs.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/phase3-worklists/8x-vs-openwrt24-base/provenance-review.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/row-summary.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/file-summary.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/unresolved.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/rules/provenance-sources-v1.json`

## Required Source Files To Inspect

Inspect the current work-repo state after M01:

- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/worktrees/openwrt-bpi-r4-pro-8x/target/linux/mediatek/image/filogic.mk`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/worktrees/openwrt-bpi-r4-pro-8x/package/boot/uboot-mediatek/Makefile`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/worktrees/openwrt-bpi-r4-pro-8x/package/boot/uboot-mediatek/patches/469-add-bpi-r4-pro-8x.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/worktrees/openwrt-bpi-r4-pro-8x/target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch`

Inspect direct 8X vendor sources named by the M02 review. Resolve the exact
source roots through `rules/provenance-sources-v1.json` if needed:

- direct 8X U-Boot patch:
  `package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch`
- direct 8X base DTS:
  `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`
- direct 8X SD overlay:
  `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso`
- direct 8X eMMC overlay for contrast only:
  `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-emmc.dtso`
- direct 8X image recipe:
  `target/linux/mediatek/image/filogic.mk`

Inspect target OpenWrt 25.12 patterns before proposing code:

- existing MediaTek filogic image recipes,
- existing `uboot-mediatek` target definitions and env patch style,
- existing MediaTek 6.12 DTS patch style,
- existing FIT/rootdisk/rootfs_data handling in the target tree.

Inspect upstream or MTK 25.12 only when it answers a concrete M02 question,
such as whether the SD overlay, chosen rootdisk property, or U-Boot env pattern
already has a cleaner target-era source.

## Key Evidence Already Known From Phase 2

Direct 8X SD overlay evidence:

- targets `/soc/mmc@11230000`,
- uses 4-bit SD,
- uses card-detect GPIO `cd-gpios = <&pio 12 GPIO_ACTIVE_LOW>`,
- sets `no-mmc`,
- defines an SD `ubootenv`,
- defines `sd_rootfs` on partition `production`,
- sets `/chosen/rootdisk-sd = <&sd_rootfs>`.

Direct 8X eMMC overlay is context only for M02:

- same MMC controller,
- 8-bit eMMC,
- `no-sd` / `no-sdio`,
- eMMC `ubootenv`,
- `/chosen/rootdisk-emmc`.

Direct 8X base DTS is context only for M02:

- bootargs include `root=/dev/fit0`,
- base `/chosen` has SPI-NAND rootdisk context,
- board identity and most hardware description belong to M03 or later,
- onboard storage policy belongs to M10.

Direct 8X U-Boot SD environment evidence:

- adds `bananapi_bpi-r4-pro-8x_sdmmc_env`,
- normal SD boot uses `bootconf_sd`,
- recovery/TFTP recovery references `bootconf_emmc`,
- SD boot menu also includes write/install flows that are not M02,
- excluded M10 flows include `mmc write`, `mtd write`, UBI create/remove/write,
  `replacevol`, install-to-NAND, install-to-eMMC, SD production/recovery update,
  and `saveenv`.

External issue watchlist items relevant to M02:

- `EXT-004`: SD boot can fail because BL2/FIP/U-Boot variant or boot-media
  selection is wrong; validate serial logs before changing Linux descriptions.
- `EXT-005`: SD GPT/image layout may be intentionally truncated after rootfs;
  decide whether this is acceptable documentation or needs image padding.

M00 handoff relevant to M02:

- `999-fitblk-01-parse-and-mount-ramdisk.patch` can affect FIT ramdisk mapping
  and SD/recovery boot. Review it for SD/recovery validation, but persistent
  rootfs/sysupgrade remains M10.

## M02 Reading-Only Report Format

For a reading-only preflight, report these sections and stop:

```text
Documents Read
Source Files Read
M02 Scope Lock
Vendor SD Boot Behavior Summary
Vendor Implementation Anatomy
Current M01 Target State
Provenance / Target Comparison
Likely Design Questions Before Implementation
Strict No-Go List
Handoffs To Later Steps
Evidence Needed Before Code
```

Do not write code, do not build, do not commit, and do not start runtime
validation during this preflight.
