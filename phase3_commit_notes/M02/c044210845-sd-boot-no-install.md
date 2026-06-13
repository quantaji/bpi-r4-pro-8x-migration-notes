# M02: BPI-R4 Pro 8X SD Boot No-Install

Commit: `c0442108456b2ce35bb66fa74774c6170ef4db24`
Short commit: `c044210845`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
GitHub: `quantaji/openwrt-bpi-r4-pro-8x-adaptation@c0442108456b2ce35bb66fa74774c6170ef4db24`
GitHub URL after push:
`https://github.com/quantaji/openwrt-bpi-r4-pro-8x-adaptation/commit/c0442108456b2ce35bb66fa74774c6170ef4db24`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-13

## Scope

M02 only. This commit enables the SD production boot no-install path for
`bananapi_bpi-r4-pro-8x`.

The target artifact is
`openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz`.

This commit does not claim hardware runtime boot success. It does not claim
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
| `package/boot/uboot-mediatek/patches/469-add-bpi-r4-pro-8x.patch` | `copy+adapt` | `V8X` | `OW25` | Replaces the M01 SD env placeholder with read-only SD production/recovery boot commands and removes vendor write/install menus. | `M10` for eMMC/SNAND env and onboard storage flows |
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
- Replaced the SDMMC U-Boot env placeholder with read-only SD boot commands:
  `bootcmd`, `boot_sdmmc`, `boot_production`, `boot_recovery`,
  `sdmmc_read_production`, `sdmmc_read_recovery`, `mmc_read_vol`, `bootargs`,
  `bootconf`, `bootconf_sd`, `bootconf_emmc`, `bootconf_extra`,
  `part_default=production`, and `part_recovery=recovery`.
- Kept eMMC and SNAND envs as M01 placeholder/defer entries.
- Added SD overlay GPT/rootdisk semantics in the shared R4 Pro SD overlay.

## Artifact Semantics

| Artifact | M02 meaning only |
|---|---|
| `sdcard.img.gz` | SD production boot image layout and read-only SD boot path are compile/image-ready. Does not prove hardware boot until serial runtime evidence exists. |
| `initramfs-recovery.itb` | Recovery FIT is generated and placed in the Pro recovery region. Does not prove recovery runtime success. |
| `squashfs-sysupgrade.itb` | Production FIT/rootfs payload is generated for the SD production region. Does not prove sysupgrade safety. |
| `emmc-gpt.bin` | Pro eMMC GPT payload is generated and embedded in the SD payload area. Does not enable an eMMC install path in M02. |
| `emmc-preloader.bin` | eMMC BL2 payload is generated for image payload context only. No eMMC install/write command is enabled. |
| `emmc-bl31-uboot.fip` | eMMC U-Boot FIP payload is generated for image payload context only. No eMMC boot/install claim is made. |
| `snand-preloader.bin` | SNAND BL2 payload is generated for image payload context only. No NAND install/write command is enabled. |
| `snand-bl31-uboot.fip` | SNAND U-Boot FIP payload is generated for image payload context only. No NAND install/write claim is made. |

## Build Evidence

The commit was made before the final package build. The output artifacts below
were generated after commit `c0442108456b2ce35bb66fa74774c6170ef4db24`.

Commands executed from the notes repo:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
```

Both commands passed. `make defconfig` reported no `.config` change. The full
build completed through `package/index`, `json_overview_image_info`, and
`checksum`.

## Artifact Hashes

All hashes are from
`../worktrees/openwrt-bpi-r4-pro-8x/bin/targets/mediatek/filogic/sha256sums`
after the post-commit build.

| SHA256 | Artifact |
|---|---|
| `d056e77fa1b596bfc3219f3c991f5a851782116e2ab0440e41a184d5c4fbd94b` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-bl31-uboot.fip` |
| `4ecd44300972267270cd021b2965f01c85dd58155d23609886f308853e0ff5ce` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-gpt.bin` |
| `96f53f08f2065d74ac8ad0eb262f4381d1def4116ad2feefb87aca8821455144` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-preloader.bin` |
| `a75998ecb282baa0efb5c93e32dabb5e77eb5f56b66e6d1564dd54e8eb2bd922` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-initramfs-recovery.itb` |
| `e5edbfa55cefaae0fc5c171489f2e529636ab083154c281f2694981a028dbc73` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz` |
| `2897bac39495d901493cf12aa25a79575d8b0606db123748bc4861381b1b23e7` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-bl31-uboot.fip` |
| `9d4995e95d32f7a0aa4736ef534490215395a6926d5bad25691c4e18596a191a` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-preloader.bin` |
| `a2601a3dbeafe17a14223fb18a666dcf11aecc0c4e0fcf3e14bacf51c7603b68` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb` |
| `cbf016b746aaf2409d73dcee69276ca5bf48c678bc42790ab8026b67e0f48554` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x.manifest` |

## Runtime Evidence

Runtime validation was not performed for this commit.

Therefore SD boot is compile/image readiness only. It is not hardware-proven SD
runtime success.

If this commit is later flashed, the runtime gate must record serial evidence
for:

- SD BL2/FIP/U-Boot variant.
- SD production path.
- `sdmmc_read_production`.
- `bootconf_sd`.
- Kernel boot.
- `root=/dev/fit0` or actual rootfs mount success.
- No NAND/eMMC write commands executed.

## Minimalism Gate

Is this a hidden minimal image-only build? No.

M02 implements all three required SD production boot readiness surfaces:

- U-Boot SD env read-only boot path.
- Pro GPT image layout for the 8X SD artifact.
- SD rootdisk and U-Boot env semantics in the shared R4 Pro SD overlay.

Remaining limitations are explicit and assigned:

- Runtime SD boot evidence belongs to the post-commit/runtime gate.
- Recovery runtime and ramdisk fitblk evidence remain future work.
- Onboard storage, install, write, and sysupgrade behavior belongs to M10.
- Non-M02 hardware and release topics belong to later migration steps.

## TODO And Residual Risk

- SD runtime boot is unproven until serial test.
- Recovery runtime is not proven.
- `bootconf_emmc` for SD recovery is preserved by design but not runtime
  validated.
- Vendor/M00 ramdisk fitblk patch remains deferred.
- M10 owns onboard storage boot, install, write, and sysupgrade paths.
- M04, M05, M06, M09, and M11 own non-M02 hardware and release topics.
