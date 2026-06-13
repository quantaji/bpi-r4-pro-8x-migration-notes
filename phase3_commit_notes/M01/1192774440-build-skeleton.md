# M01: BPI-R4 Pro 8X Build Skeleton

Commit: `1192774440f00726a5313bd3af69b6b28811b9b6`
Short commit: `1192774440`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
GitHub: `quantaji/openwrt-bpi-r4-pro-8x-adaptation@1192774440f00726a5313bd3af69b6b28811b9b6`
GitHub URL:
`https://github.com/quantaji/openwrt-bpi-r4-pro-8x-adaptation/commit/1192774440f00726a5313bd3af69b6b28811b9b6`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-13

## Scope

M01 only. This commit adds a clean build/image skeleton for
`bananapi_bpi-r4-pro-8x`.

This commit proves only that the target profile, TF-A/U-Boot build metadata,
kernel DTB/DTBO closure, and expected image artifact names can be built. It does
not claim SD boot, eMMC/SNAND install, sysupgrade safety, networking, Wi-Fi,
SFP/10G, USB, PCIe/NVMe, fan, RTC, LEDs/buttons, or release readiness.

The OpenWrt generated `version.buildinfo` for this build is
`r32933-4ccb782af7`. The local migration commit hash is not automatically
embedded in the default OpenWrt release metadata. For flash-test traceability,
use the commit hash in this note together with the artifact SHA256 values below,
or add a later explicit version-marking strategy.

## Source Aliases

- `OW25`: OpenWrt 25.12.4 target tree and current target build patterns.
- `ULNX`: upstream Linux DTS tree.
- `UBOOT-UP`: upstream U-Boot tree.
- `V8X`: direct vendor 8X tree.
- `V4E`: direct vendor 4E tree.
- `MTK25`: MTK OpenWrt 25.12 tree/feed.
- `PR21083`: external OpenWrt PR reference only.
- `OLD-BOOT`: old ImmortalWrt bootable experiment, reference only.

`PR21083` and `OLD-BOOT` were not used as implementation sources for this
commit.

## File Provenance

| File | Action | Primary source | Secondary source | Why in M01 | Deferred owner |
|---|---|---|---|---|---|
| `package/boot/arm-trusted-firmware-mediatek/Makefile` | `target-pattern-write` | `OW25` | `V8X` | Adds scoped MT7988 4 GB DDR TF-A build targets needed by 8X artifacts without mutating shared comb targets. | `M02/M10` for boot/install validation |
| `package/boot/uboot-mediatek/Makefile` | `copy+adapt` | `V8X` | `OW25` | Adds eMMC, SDMMC, and SNAND U-Boot compile targets tied to the 8X profile. | `M02/M10` |
| `package/boot/uboot-mediatek/patches/469-add-bpi-r4-pro-8x.patch` | `copy+adapt` | `V8X` | `OW25`, `UBOOT-UP` reference only | Provides U-Boot DTS, defconfig, and env compile skeleton. The env is reduced to a non-booting M01 placeholder. | `M02` SD boot env; `M10` install/write flows |
| `target/linux/mediatek/image/filogic.mk` | `target-pattern-write` | `OW25` | `V8X`, `ULNX`, `MTK25` | Adds selectable 8X profile and build-only image artifact skeleton with an R4 Pro common helper, not regular R4 common inheritance. | `M02/M03/M05/M06/M09/M10` |
| `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | `upstream-copy+adapt` | `ULNX` | `OW25`, `MTK25`, `V8X`, `V4E` | Ports the upstream Linux R4 Pro split into OpenWrt 25.12 `patches-6.12` style for DTB/DTBO build closure. | `M02/M03/M05/M06/M09/M10` runtime validation |

## Accepted Behavior

- Scoped MT7988 4 GB DDR TF-A targets:
  `mt7988-emmc-comb-4bg`, `mt7988-sdmmc-comb-4bg`, and
  `mt7988-spim-nand-ubi-comb-4bg`.
- 8X U-Boot eMMC, SDMMC, and SNAND compile targets.
- 8X OpenWrt image/profile skeleton.
- Upstream Linux R4 Pro common DTSI plus minimal 8X top-level DTS.
- Shared R4 Pro SD/eMMC DTBO build closure.

## Dropped / Deferred Behavior

- No direct vendor kernel DTS as the primary source.
- No vendor 8X RTC or Wi-Fi overlay in M01.
- No 4E OpenWrt profile.
- No runtime package closure.
- No `board.d`, preinit, or `platform.sh`.
- No U-Boot install, write, reset-factory, or `saveenv` flow.
- No `emmc.img.gz`, `snand-factory.bin`, or `mt798x-r4pro-gpt`.
- SD boot is deferred to M02.
- Board identity, GPIO, I2C, and factory data are deferred to M03.
- Basic wired management defaults are deferred to M04.
- SFP/10G/switch/PHY behavior is deferred to M05.
- Wi-Fi hardware, firmware, EEPROM, and radio detection are deferred to M06.
- USB, PCIe/NVMe, fan, RTC, LEDs, and buttons are deferred to M09.
- eMMC/SNAND install, GPT/layout semantics, and sysupgrade/write behavior are
  deferred to M10.

## Artifact Semantics

| Artifact | M01 meaning only |
|---|---|
| `sdcard.img.gz` | Build/image skeleton artifact can be generated. Does not prove SD boot or SD layout correctness. |
| `emmc-gpt.bin` | Generic build artifact name can be generated. Does not prove R4 Pro GPT/layout correctness. |
| `emmc-preloader.bin` | eMMC BL2 artifact can be built using scoped 4 GB DDR TF-A target. Does not prove eMMC boot or install. |
| `emmc-bl31-uboot.fip` | eMMC U-Boot FIP can be built. Does not prove eMMC runtime or writes. |
| `snand-preloader.bin` | SNAND BL2 artifact can be built using scoped 4 GB DDR TF-A target. Does not prove SNAND boot or install. |
| `snand-bl31-uboot.fip` | SNAND U-Boot FIP can be built. Does not prove NAND/eMMC install path. |
| `initramfs-recovery.itb` | Recovery FIT artifact can be generated. Does not prove recovery boot. |
| `squashfs-sysupgrade.itb` | Sysupgrade artifact name can be generated. Does not prove sysupgrade safety. |

## Validation Evidence

The commit was made before the final package build. The output artifacts below
were generated after commit `1192774440f00726a5313bd3af69b6b28811b9b6`.

Commands executed from the notes repo:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
```

Both commands passed. `make defconfig` reported no `.config` change. The full
build completed through `package/index`, `json_overview_image_info`, and
`checksum`.

Earlier M01 validation also built TF-A, U-Boot, `target/linux/compile`, and
`target/linux/install` directly with maximum-thread commands. The final
commit-coupled evidence is the post-commit full package build above.

## Artifact Hashes

All hashes are from
`../worktrees/openwrt-bpi-r4-pro-8x/bin/targets/mediatek/filogic/sha256sums`
after the post-commit build.

| SHA256 | Artifact |
|---|---|
| `d056e77fa1b596bfc3219f3c991f5a851782116e2ab0440e41a184d5c4fbd94b` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-bl31-uboot.fip` |
| `6decc5e0ac9ef38bc78f4de8d4df825473a248898c24add4252cd74006f2fd20` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-gpt.bin` |
| `96f53f08f2065d74ac8ad0eb262f4381d1def4116ad2feefb87aca8821455144` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-preloader.bin` |
| `083cbafc13b06f732fd56036420e0c840e032a3acbfa9b2e7daac752c89e5de2` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-initramfs-recovery.itb` |
| `8ebab4e641791fb965672bfe481735b7792020860956c9d630a79682bbd7e7af` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz` |
| `2897bac39495d901493cf12aa25a79575d8b0606db123748bc4861381b1b23e7` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-bl31-uboot.fip` |
| `9d4995e95d32f7a0aa4736ef534490215395a6926d5bad25691c4e18596a191a` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-preloader.bin` |
| `506269c0c227ebef8e1b35d2dfda0fe74bf6a0a4a0bf788b14fe0b9cb105e589` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb` |
| `cbf016b746aaf2409d73dcee69276ca5bf48c678bc42790ab8026b67e0f48554` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x.manifest` |

## Interface Naming Status

M01 does not lock runtime interface names.

The kernel DTS imported from upstream Linux contains compile-time hardware
labels such as `mgmt` for `gsw_port0` and SFP node names such as `sfp1` and
`sfp2`. This is DTS build closure only in M01 and is not a final OpenWrt network
interface naming decision.

The earlier `mx-wan` / `mx-lan` to `combo-wan` / `combo-lan` naming decision
belongs later:

- M04 owns the minimal management network default needed to make the board
  reachable.
- M05 owns the full wired switch/SFP/10G naming and behavior, including final
  user-facing names for combo copper/SFP ports.

If M04 must choose a temporary management naming convention, it should record
that as provisional and hand final combo-port naming to M05.

## Residual Risk

Build success only. No runtime evidence exists for this commit. SD boot,
GPT/layout correctness, eMMC/SNAND install, sysupgrade safety, wired networking,
Wi-Fi, SFP/10G, PCIe/NVMe, USB, fan, RTC, LEDs/buttons, and release readiness
remain deferred to later migration steps.
