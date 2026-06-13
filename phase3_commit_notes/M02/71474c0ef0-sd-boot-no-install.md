# M02: BPI-R4 Pro 8X SD Boot No-Install

Commit: `71474c0ef01f4c8652e7afae218f5c1abce95a6a`
Short commit: `71474c0ef0`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
GitHub: `quantaji/openwrt-bpi-r4-pro-8x-adaptation@71474c0ef01f4c8652e7afae218f5c1abce95a6a`
GitHub URL after push:
`https://github.com/quantaji/openwrt-bpi-r4-pro-8x-adaptation/commit/71474c0ef01f4c8652e7afae218f5c1abce95a6a`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-13

## Scope

M02 only. This commit enables the SD production boot no-install path for
`bananapi_bpi-r4-pro-8x`.

The target artifact is
`openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz`.

This commit has SD production min-boot runtime evidence. It does not claim
NAND/eMMC install, sysupgrade safety, onboard storage boot, wired networking,
SFP/10G, Wi-Fi, factory MAC correctness, recovery runtime success, or release
readiness.

## Source Aliases

- `OW25`: OpenWrt 25.12.4 target tree and current target build patterns.
- `V8X`: direct vendor 8X source.
- `V4E`: direct vendor 4E source.
- `ULNX`: upstream Linux DTS context inherited through M01 DTS base work.
- `PR21083`: external OpenWrt PR reference only.
- `OLD-BOOT`: old ImmortalWrt bootable experiment, warning/orientation only.

`PR21083` and `OLD-BOOT` were not implementation authority for this commit.

## Vendor Behavior Summary

The direct vendor Pro images use a Pro-specific SD/eMMC partition layout rather
than the regular BPI-R4 layout. The SD image places recovery at `128M@12M`, an
installer payload area at `20M@140M`, and production rootfs/FIT content at
`@160M`.

Vendor SD boot reads the GPT `production` partition for normal boot. Production
uses the SD boot configuration, while the SD recovery command uses the eMMC
boot configuration. Vendor DTS overlays also provide SD card detect, no-eMMC-on
SD-slot behavior, U-Boot environment partition description, SD production
rootdisk labeling, and `/chosen/rootdisk-sd`.

Vendor code also contains install/write behavior. Those write paths are not part
of M02 and were rejected or deferred.

## Vendor Implementation Anatomy

The vendor implementation spans image layout, U-Boot env, and SD overlay
semantics:

- Image layout: Pro GPT layout for SD/eMMC images with recovery, install, and
  production regions.
- U-Boot SD env: normal boot reads the SD `production` partition; recovery reads
  the SD `recovery` partition.
- SD overlay: declares card detect, `no-mmc`, GPT partitions, `ubootenv`, SD
  production rootfs, and `/chosen/rootdisk-sd`.
- Install/write flows: vendor menus and commands can write SD, NAND, eMMC, MTD,
  and UBI volumes.

M02 keeps only the read-only boot and rootdisk behavior needed for SD production
boot readiness.

## Provenance Evidence

The M02 implementation was derived from these source classes:

- `V8X`: direct 8X Pro SD env, SD overlay intent, and Pro layout context.
- `V4E`: direct Pro-series layout corroboration.
- `OW25`: current OpenWrt image recipe style, U-Boot env style, and final SD
  overlay shape.
- `ULNX`: inherited M01 DTS base context only.

The final SD overlay shape intentionally follows OW25 BPI-R4/BPI-R4 Lite target
style: `card@0 -> partitions`. It does not keep the vendor-style
`block { compatible = "block-device"; }` layer.

## Target 25.12 Design Decision

M02 adapts vendor behavior into OpenWrt 25.12 style instead of copying vendor
files literally.

The Pro layout is implemented as `mt798x-r4pro-gpt` and applied to the 8X SD
artifact and 8X eMMC GPT artifact. Production starts at `@160M`, and
`IMAGE_SIZE` is `160 + CONFIG_TARGET_ROOTFS_PARTSIZE`. This is a
supervisor/user-approved target adaptation; it is not the earlier generic
`64 + ...` skeleton layout.

The SD U-Boot env is reduced to read-only boot commands. The SD overlay is kept
in the shared R4 Pro SD overlay, but only for Pro-series common SD boot
semantics. No 8X-only, 4E-only, Wi-Fi, SFP, PHY, factory MAC, install policy, or
storage policy was added to the shared overlay.

The vendor/M00 ramdisk fitblk patch was not migrated. M02 production boot is
covered by OW25 `rootdisk-sd`, `root=/dev/fit0`, `CONFIG_UIMAGE_FIT_BLK=y`, and
`external-with-rootfs`. Recovery ramdisk behavior remains future evidence/risk.

## Accepted Vendor Behavior

- Pro GPT layout:
  - recovery `128M@12M`
  - install payload area `20M@140M`
  - production `@160M`
- SD production boot reads GPT `production`.
- SD production uses `bootconf_sd`.
- SD recovery command remains read-only and uses `bootconf_emmc`.
- SD overlay keeps:
  - `cd-gpios = <&pio 12 GPIO_ACTIVE_LOW>`
  - `no-mmc`
  - GPT `ubootenv`
  - `sd_rootfs`
  - `/chosen/rootdisk-sd`

## Rejected Or Deferred Vendor Implementation

Rejected from M02:

- `mmc write`
- `mmc erase`
- `mtd write`
- `mtd erase`
- `ubi create/remove/write`
- `replacevol`
- `saveenv`
- `eraseenv`
- reset factory
- TFTP write menu
- install-to-NAND
- install-to-eMMC
- SD production/recovery rewrite

Deferred:

- Vendor/M00 ramdisk fitblk patch, unless recovery runtime is later claimed.
- eMMC/SNAND env, onboard storage boot, install, write, and sysupgrade behavior
  to M10.
- Wired/SFP/Wi-Fi/factory MAC and other hardware or release topics to later M
  steps, including M04, M05, M06, M09, and M11.

## File Provenance

| File | Action | Primary source | Secondary source | Why in M02 | Deferred owner |
|---|---|---|---|---|---|
| `target/linux/mediatek/image/filogic.mk` | `copy+adapt` | `V8X`, `V4E` | `OW25` | Adds Pro layout `mt798x-r4pro-gpt` and aligns 8X SD/eMMC image layout to production `@160M`; `IMAGE_SIZE=160+...` is supervisor/user-approved target adaptation, not vendor literal `64+...`. | `M10` for install/write/sysupgrade validation |
| `package/boot/uboot-mediatek/patches/469-add-bpi-r4-pro-8x.patch` | `copy+adapt` | `V8X` | `OW25` | Replaces the M01 SD env placeholder with read-only SD production/recovery boot commands, adds a read-only SD boot menu, uses the shared Pro SD/eMMC overlay config names, and removes vendor write/install menus. | `M10` for eMMC/SNAND env and onboard storage flows |
| `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | `target-pattern-write` | `OW25` | `V8X`, `V4E`, `ULNX` | Adds shared R4 Pro SD rootdisk/env semantics using the OW25 BPI-R4/BPI-R4 Lite `card@0 -> partitions` pattern, not the vendor `block-device` layer. | Later hardware steps for non-M02 DTS semantics |

## Code Changes

- Added `Build/mt798x-r4pro-gpt`.
- Changed the 8X SD artifact to use `mt798x-r4pro-gpt sdmmc`.
- Changed the 8X eMMC GPT artifact and SD-embedded eMMC GPT payload to use
  `mt798x-r4pro-gpt emmc`.
- Increased SD recovery FIT size allowance to `128m`.
- Moved SD payload offsets to the Pro layout: `140M`, `141M`, `147M`, `148M`,
  and `152M`.
- Moved SD production FIT/rootfs placement to `pad-to 160M`.
- Set `IMAGE_SIZE := $(shell expr 160 + $(CONFIG_TARGET_ROOTFS_PARTSIZE))m`.
- Added M02 minimum SD overlay/rootfs packages:
  `e2fsprogs f2fsck mkf2fs`. These are needed for first-boot F2FS overlay
  initialization on `/dev/fitrw`; the runtime dependency `libf2fs6` is pulled
  into the final manifest.
- Replaced the SDMMC U-Boot env placeholder with read-only SD boot commands:
  `bootcmd`, `boot_sdmmc`, `boot_production`, `boot_recovery`,
  `sdmmc_read_production`, `sdmmc_read_recovery`, `mmc_read_vol`, `bootargs`,
  `bootconf`, `bootconf_sd`, `bootconf_emmc`, `bootconf_extra`,
  `part_default=production`, and `part_recovery=recovery`.
- Added a minimal read-only SD boot menu for the default, production, and
  recovery boot choices.
- Corrected SD overlay config names to the shared Pro overlays:
  `mt7988a-bananapi-bpi-r4-pro-sd` and
  `mt7988a-bananapi-bpi-r4-pro-emmc`.
- Kept eMMC and SNAND envs as M01 placeholder/defer entries.
- Added SD overlay GPT/rootdisk semantics in the shared R4 Pro SD overlay.

## Artifact Semantics

| Artifact | M02 meaning only |
|---|---|
| `sdcard.img.gz` | SD production boot image layout and read-only SD boot path are runtime-proven for M02 min-boot. Does not prove recovery, sysupgrade, or onboard install behavior. |
| `initramfs-recovery.itb` | Recovery FIT is generated and placed in the Pro recovery region. Does not prove recovery runtime success. |
| `squashfs-sysupgrade.itb` | Production FIT/rootfs payload is generated for the SD production region. Does not prove sysupgrade safety. |
| `emmc-gpt.bin` | Pro eMMC GPT payload is generated and embedded in the SD payload area. Does not enable an eMMC install path in M02. |
| `emmc-preloader.bin` | eMMC BL2 payload is generated for image payload context only. No eMMC install/write command is enabled. |
| `emmc-bl31-uboot.fip` | eMMC U-Boot FIP payload is generated for image payload context only. No eMMC boot/install claim is made. |
| `snand-preloader.bin` | SNAND BL2 payload is generated for image payload context only. No NAND install/write command is enabled. |
| `snand-bl31-uboot.fip` | SNAND U-Boot FIP payload is generated for image payload context only. No NAND install/write claim is made. |

## Permission Incident And Pre-Build Gate

During runtime debug, an image built from the pre-amend worktree reached
`procd: - ubus -` but did not enter `procd: - init -`. Failsafe testing showed
that `ubusd` could run as root, but a daemon running as the `ubus` user could
not complete the client handshake while `/etc/passwd` and `/etc/group` were
not world-readable.

The root cause was local worktree file-mode pollution in
`package/base-files/files`. The affected source files had content identical to
the OpenWrt tree, but several were mode `0600`; Git did not report this because
the index records them as `100644`. OpenWrt `base-files` copies those files
with preserved mode, so the bad mode was inherited into the rootfs.

Before the final build, this was corrected and checked:

- no `package/base-files/files` source file remained mode `0600`;
- source `package/base-files/files/etc/passwd` and `etc/group` were readable;
- final rootfs `etc/passwd` and `etc/group` are `0644`;
- final rootfs `etc/shadow` is `0600`;
- final rootfs contains `ubus:x:81:81:ubus:/var/run/ubus:/bin/false` and
  group `ubus:x:81:ubus`.

This was a local file-mode hygiene issue, not an M02 board-design change.

## Build Evidence

The final output artifacts below were generated after commit
`71474c0ef01f4c8652e7afae218f5c1abce95a6a`.

Commands executed from the notes repo:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
```

Both commands passed. `make defconfig` reported no `.config` change. The full
build completed through `package/index`, `json_overview_image_info`, and
`checksum`.

Final manifest contains the M02 minimum package closure:

- `e2fsprogs - 1.47.3-r1`
- `f2fsck - 1.16.0-r4`
- `fitblk - 2`
- `fstools - 2026.02.15~8d377aa6-r1`
- `libf2fs6 - 1.16.0-r4`
- `mkf2fs - 1.16.0-r4`
- `uboot-envtools - 2025.10-r2`

## Artifact Hashes

All hashes are from
`../worktrees/openwrt-bpi-r4-pro-8x/bin/targets/mediatek/filogic/sha256sums`
after the post-commit build.

| SHA256 | Artifact |
|---|---|
| `d056e77fa1b596bfc3219f3c991f5a851782116e2ab0440e41a184d5c4fbd94b` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-bl31-uboot.fip` |
| `4ecd44300972267270cd021b2965f01c85dd58155d23609886f308853e0ff5ce` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-gpt.bin` |
| `96f53f08f2065d74ac8ad0eb262f4381d1def4116ad2feefb87aca8821455144` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-preloader.bin` |
| `4b19eb8f19d0ce391a35a93d17a8351703903a8f6da6a8e449a5bec99badaafd` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-initramfs-recovery.itb` |
| `54945d49642c8b43966537c074d66e54b60ab86a3b12d6961b8c4f80fe744784` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz` |
| `2897bac39495d901493cf12aa25a79575d8b0606db123748bc4861381b1b23e7` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-bl31-uboot.fip` |
| `9d4995e95d32f7a0aa4736ef534490215395a6926d5bad25691c4e18596a191a` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-preloader.bin` |
| `46228ad291c09d1d0429077afcd64735c2b3b717a58da24566763c05514be32f` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb` |
| `3b5fd4ee38e95d970d93cda39f2ba98a66c78ab8b596933ed5bbf0f03d4d8a13` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x.manifest` |

## Runtime Evidence

SD production min-boot was runtime validated on hardware after the final M02
fixes and rebuild.

Serial evidence showed:

- BL2 entered the SDMMC variant:
  `OpenWrt v2025.07.11~78a0dfd9-1 (mt7988-sdmmc-comb-4bg)`.
- U-Boot identified `Model: BananaPi BPI-R4 Pro 8X`.
- U-Boot showed the `OpenWrt [SD card]` menu.
- SD production boot read from MMC:
  `MMC read: dev # 0, block # 327680`.
- FIT selected `config-mt7988a-bananapi-bpi-r4-pro-8x`.
- FIT loaded the shared SD overlay:
  `fdt-mt7988a-bananapi-bpi-r4-pro-sd`.
- U-Boot set `/chosen/rootdisk` to `rootdisk-sd`.
- Kernel command line was:
  `console=ttyS0,115200n1 pci=pcie_bus_perf root=/dev/fit0 rootwait`.
- Linux mapped SD production FIT/rootfs:
  `block mmcblk0p7: mapped 1 uImage.FIT filesystem sub-image as /dev/fit0`
  and `mapped remaining space as /dev/fitrw`.
- Root mounted successfully:
  `/dev/root on /rom type squashfs`.
- Overlay mounted successfully:
  `/dev/fitrw on /overlay type f2fs`.
- procd passed the prior failure point:
  `procd: - ubus -`, `procd: - init -`, and `procd: - init complete -`.
- Serial login succeeded on `ttyS0`.
- `ubus list` returned system objects.

No M02 runtime evidence showed execution of vendor NAND/eMMC install/write
commands.

## Minimalism Gate

Is this a hidden minimal image-only build? No.

M02 implements all three required SD production boot readiness surfaces:

- U-Boot SD env read-only boot path.
- Pro GPT image layout for the 8X SD artifact.
- SD rootdisk and U-Boot env semantics in the shared R4 Pro SD overlay.

Remaining limitations are explicit and assigned:

- Recovery runtime and ramdisk fitblk evidence remain future work.
- Onboard storage, install, write, and sysupgrade behavior belongs to M10.
- Non-M02 hardware and release topics belong to later migration steps.

## TODO And Residual Risk

- Recovery runtime is not proven.
- `bootconf_emmc` for SD recovery is preserved by design but not runtime
  validated.
- Vendor/M00 ramdisk fitblk patch remains deferred.
- M10 owns onboard storage boot, install, write, and sysupgrade paths.
- M04, M05, M06, M09, and M11 own non-M02 hardware and release topics.
- `gpio-leds` reports a deferred probe for `sys-led-red`; this is not an M02
  SD boot blocker and belongs to a later board-extras/LED stage.
- Wi-Fi userspace logs report missing `ucode` wireless helpers; Wi-Fi is not in
  M02 and belongs to later Wi-Fi/package-closure work.
