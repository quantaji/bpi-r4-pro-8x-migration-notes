# M03: BPI-R4 Pro 8X Board Services And Factory Data

Commit: `dd50c843a4ee2c3d442ac2afdc9352f429881be1`
Short commit: `dd50c843a4`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
GitHub: `quantaji/openwrt-bpi-r4-pro-8x-adaptation@dd50c843a4ee2c3d442ac2afdc9352f429881be1`
GitHub URL:
`https://github.com/quantaji/openwrt-bpi-r4-pro-8x-adaptation/commit/dd50c843a4ee2c3d442ac2afdc9352f429881be1`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-13

## Scope

M03 only. This commit adds the static board-service layer for
`bananapi_bpi-r4-pro-8x`.

It describes the board identity, I2C mux and local board-service devices,
PCA9555-backed LEDs, PCF8563 RTC, AT24 EEPROM, and SPI-NAND Factory partition
geometry. It also records the direct vendor Factory MAC offsets as unconsumed
fixed-layout nvmem cells.

This commit does not claim Ethernet MAC identity, LAN/WAN defaults, SFP/10G,
AS21xxx, MxL86252, Wi-Fi, fan, USB, PCIe/NVMe, eMMC/SNAND install, persistent
environment, sysupgrade safety, or release readiness.

## Source Aliases

- `OW25`: OpenWrt 25.12.4 target tree and current target build patterns.
- `ULNX`: upstream Linux R4 Pro DTS split inherited through M01.
- `V8X`: direct vendor 8X source.
- `V4E`: direct vendor 4E source.
- `SCHEMATIC`: BPI-R4 Pro 8X schematic evidence read during M03 review.
- `OLD-BOOT`: old ImmortalWrt 25.12 bring-up experiment, evidence only.
- `PR21083`: external OpenWrt PR reference only.

`OLD-BOOT` and `PR21083` were not implementation authority. They were used only
to identify risks and avoid repeating known runtime mistakes.

## Design Decision

M03 does not replay the vendor 8X DTS file. It rewrites the 8X board-service
facts into the existing OpenWrt 25.12 / R4 Pro DTS split created by M01 and
extended by M02.

The direct vendor 8X DTS is used for 8X-specific hardware facts:

- PCA9545 mux address and channel layout;
- PCF8563, AT24, and PCA9555 local I2C devices;
- reset/WPS keys and red/blue LEDs;
- SPI-NAND `Factory` partition geometry;
- Factory MAC offset evidence.

OpenWrt 25.12 and upstream Linux structure decide how those facts are expressed
in the target patch stack.

## PMIC Decision

No PMIC rail values were changed in M03.

The direct vendor 8X/4E DTS wrote lower `buck4` / `ldo` voltages, but the 8X
schematic review identified those rails as 1.8 V rails:

- Buck4 feeds `DVDD1V8_SOC`.
- The PMIC LDO feeds `AVDD18`.

Therefore M03 keeps the target R4 Pro 1.8 V constraints and treats the vendor
`850000` / `1200000` values as rail-mapping mistakes. AVDD12 is a separate
1.2 V regulator in the schematic and is not the PMIC LDO described here.

## File Provenance

| File | Action | Primary source | Secondary source | Why in M03 | Deferred owner |
|---|---|---|---|---|---|
| `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | `copy+adapt` / `target-pattern-write` | `V8X` hardware facts | `OW25`, `ULNX`, `SCHEMATIC`, `OLD-BOOT` | Adds M03-owned board-service DTS facts inside the existing R4 Pro split; corrects static SPI-NAND Factory geometry and exposes Factory MAC offsets as unconsumed evidence. | `M04` MAC/interface policy; `M05` wired runtime; `M06` Wi-Fi; `M09` extras; `M10` install/storage policy |
| `target/linux/mediatek/image/filogic.mk` | `target-pattern-write` | `OW25` package pattern | `V8X` device needs, M02 package baseline | Adds only the kmods needed for M03 board services while preserving M02 F2FS packages. | Later package closure for wired, Wi-Fi, fan, USB, HNAT, and install flows |

## Code Changes

- Kept the 8X top-level DTS/profile skeleton from M01/M02.
- Kept RT5190A / PMIC rail values at the target 1.8 V values.
- Kept or added stable PCA9545 labels:
  `pca9545`, `imux0`, `imux1_sfp1`, `imux2_sfp2`, and `imux3_wifi`.
- Kept the local mux channel devices:
  `pca9555: i2c-gpio-expander@20`, `pcf8563: rtc@51`, and AT24 24c02 at
  `0x57`.
- Did not add vendor `ina226@40`; U13 is not populated on the referenced 8X
  schematic and runtime probe failed.
- Kept reset and WPS keys and the red/blue PCA9555-backed LEDs.
- Split SPI-NAND into:
  - `bl2` at `0x0`, size `0x200000`;
  - `factory: partition@200000`, label `Factory`, size `0x400000`;
  - `partition@600000`, compatible `linux,ubi`, label `ubi`, size
    `0xfa00000`.
- Added Factory fixed-layout nvmem cells:
  - `gmac2_mac` at `0xfffee`, size `0x6`;
  - `gmac1_mac` at `0xffffa`, size `0x6`;
  - `gmac0_mac` at `0xffff4`, size `0x6`.
- Added M03 board-service packages:
  `kmod-i2c-mux-pca954x`, `kmod-gpio-pca953x`, `kmod-eeprom-at24`, and
  `kmod-rtc-pcf8563`.
- Preserved M02 packages:
  `e2fsprogs`, `f2fsck`, and `mkf2fs`.

## Rejected Or Deferred Behavior

Rejected from M03:

- enabled `ina226@40`;
- `kmod-hwmon-ina2xx`;
- GMAC `nvmem-cells` consumers;
- `02_network` changes;
- UBI volume declarations;
- rootdisk, bootargs, env, install, or sysupgrade semantics.

Deferred:

- Ethernet MAC source and fallback policy to M04.
- Full wired switch/SFP/10G/PHY runtime to M05.
- Wi-Fi overlay, radio EEPROM, and Wi-Fi GPIO conflicts to M06.
- Fan, USB, PCIe/NVMe, and other runtime extras to M09.
- eMMC/SNAND install, persistent env, and storage write policy to M10.

## Debug Notes

Two M03 issues were found during runtime validation and resolved before this
commit:

1. Board-service kmods must be present in the final image, not merely in DTS.
   The final manifest includes the PCA9545, PCA953x, AT24, and PCF8563 kmods.

2. Vendor `ina226@40` should not be enabled. The first M03 runtime showed
   `ina2xx 3-0040` probe failure, and vendor runtime showed the same class of
   failure. Schematic evidence then showed U13 is an optional, not-populated
   INA226 footprint and R78 is not a valid milliohm sense resistor.

MAC validation found that the tested board's Factory offsets did not contain
valid Ethernet MAC data. That is not an M03 failure because M03 intentionally
does not attach those cells to GMAC consumers. M04 must close the MAC source and
fallback policy.

## Build Evidence

The final image used for runtime validation was built from the same worktree
content that was later committed as
`dd50c843a4ee2c3d442ac2afdc9352f429881be1`.

Commands used by the implementation build from the notes repo:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
```

Both commands use the project container wrapper. The project rule is that build
and debug builds must use all available cores through `make -j$(nproc)`.

Final manifest contains:

- `kmod-eeprom-at24 - 6.12.87-r1`
- `kmod-gpio-pca953x - 6.12.87-r1`
- `kmod-i2c-mux-pca954x - 6.12.87-r1`
- `kmod-rtc-pcf8563 - 6.12.87-r1`
- `e2fsprogs - 1.47.3-r1`
- `f2fsck - 1.16.0-r4`
- `mkf2fs - 1.16.0-r4`

The final manifest does not contain `kmod-hwmon-ina2xx`.

## Artifact Hashes

All hashes are from
`../worktrees/openwrt-bpi-r4-pro-8x/bin/targets/mediatek/filogic/sha256sums`
after the final M03 rebuild.

| SHA256 | Artifact |
|---|---|
| `d056e77fa1b596bfc3219f3c991f5a851782116e2ab0440e41a184d5c4fbd94b` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-bl31-uboot.fip` |
| `4ecd44300972267270cd021b2965f01c85dd58155d23609886f308853e0ff5ce` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-gpt.bin` |
| `96f53f08f2065d74ac8ad0eb262f4381d1def4116ad2feefb87aca8821455144` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-preloader.bin` |
| `e86f4f9d3a59f45e6eab268eca990785cb73eb489321d00d55e4792daf79c6ec` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-initramfs-recovery.itb` |
| `633771d441fe50018899fb6cc5dfada5c210d308a91127b781d54150d53606cf` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz` |
| `2897bac39495d901493cf12aa25a79575d8b0606db123748bc4861381b1b23e7` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-bl31-uboot.fip` |
| `9d4995e95d32f7a0aa4736ef534490215395a6926d5bad25691c4e18596a191a` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-preloader.bin` |
| `79ca34a87a7aed6e096a44a6ae24e83ef87412f60abec29f2fbccf1b9bf82780` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb` |
| `fe4808495f35c7f4db9a7d2ed6cd8326650a146d4aaeb2983923583b42fe5372` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x.manifest` |

## Runtime Evidence

Runtime validation was done on real BPI-R4 Pro 8X hardware after the final M03
fixes and rebuild.

Serial boot evidence showed:

- `Machine model: Bananapi BPI-R4 Pro 8X`;
- SPI-NAND partition geometry:
  - `0x000000000000-0x000000200000 : "bl2"`;
  - `0x000000200000-0x000000600000 : "Factory"`;
  - `0x000000600000-0x000010000000 : "ubi"`;
- UBI attached from `mtd2`, not from the Factory range.

The M03 kmod debug script showed:

- installed: `kmod-i2c-mux-pca954x`, `kmod-gpio-pca953x`,
  `kmod-eeprom-at24`, `kmod-rtc-pcf8563`;
- not installed: `kmod-hwmon-ina2xx`;
- `2-0070` bound to `DRIVER=pca954x`;
- mux-created adapters `i2c-3`, `i2c-4`, `i2c-5`, and `i2c-6`;
- `3-0020 name=pca9555`;
- `3-0051 name=pcf8563`;
- `3-0057 name=24c02`;
- `rtc0` registered from PCF8563;
- PCA9555 GPIO chip present;
- `red:` and `blue:` LEDs present;
- no remaining `ina2xx 3-0040` probe error.

## MAC Status

M03 exposes the vendor Factory offset convention but does not trust it as a
runtime MAC source.

The tested board showed:

- AT24 `0x57` contains a board-id string like `R4PRO8X-BBC30219`, not an
  Ethernet MAC block.
- The Factory offsets around `0xffff4`, `0xffffa`, and `0xfffee` did not expose
  valid Ethernet MAC values.
- Runtime Ethernet still used a random/local MAC.

M04 must decide the final MAC source and fallback policy. This may involve
U-Boot env, UCI, eMMC/SNAND evidence, or a deterministic generated fallback,
but M03 deliberately leaves GMAC consumers disconnected.

## Residual Risk

- Ethernet MAC identity is unresolved and owned by M04.
- Wired topology, AS21xxx, MxL86252, SFP/RJ45 switching, and cold-boot link
  behavior are unresolved and owned by M05.
- Wi-Fi EEPROM/radio behavior is unresolved and owned by M06.
- PCIe/MMC/USB/fan/runtime extras remain outside M03.
- Dummy regulator messages for PCA9545/PCA9555/AT24 are non-blocking in M03
  because the devices probe and work, but later cleanup can model supplies if
  a future step needs that precision.
