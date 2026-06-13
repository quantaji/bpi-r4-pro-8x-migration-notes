# M01 DTS Source Boundary

Date: 2026-06-13

This note records the supervisor boundary decision for the BPI-R4 Pro 8X
OpenWrt 25.12 M01 implementation after reviewing the first implementation
draft. It is not implementation evidence and does not claim runtime boot.

## Scope

M01 is only the clean build and image skeleton step. It may add the minimum
target metadata, boot-loader build metadata, and kernel DTB/DTBO build closure
needed for a `bananapi_bpi-r4-pro-8x` profile to compile and emit expected
artifact names.

M01 must not claim SD boot, eMMC/NAND install, sysupgrade safety, wired
networking, SFP/10G, Wi-Fi runtime, USB, fan control, PCIe/NVMe, acceleration,
or release readiness. Those belong to later migration steps.

## Source Priority

For the kernel DTS work, the current source priority is:

1. OpenWrt 25.12 target structure and patch style.
2. Upstream Linux R4 Pro DTS structure:
   `../reference-source-codes/upstreams/linux/arch/arm64/boot/dts/mediatek/`.
3. MTK OpenWrt 25.12 feed/tree as target-era secondary reference.
4. Direct vendor 8X/4E trees as behavior confirmation and gap evidence.
5. External PRs and the old bootable ImmortalWrt experiment as reference only,
   never as design authority.

The first implementation draft treated the direct vendor 8X kernel DTS files as
the main source. That is not the best M01 basis because upstream Linux already
has a cleaner R4 Pro split that matches the target-era DTS labels better.

## R4 Pro Common Decision

Use an R4 Pro common split for kernel DTS. Upstream Linux already defines:

- `mt7988a-bananapi-bpi-r4-pro.dtsi`
- `mt7988a-bananapi-bpi-r4-pro-8x.dts`
- `mt7988a-bananapi-bpi-r4-pro-4e.dts`
- shared Pro overlays such as `mt7988a-bananapi-bpi-r4-pro-sd.dtso` and
  `mt7988a-bananapi-bpi-r4-pro-emmc.dtso`

The 8X and 4E top-level DTS files differ only by model and compatible string in
the upstream Linux source. Therefore, M01 should keep the common boundary
compatible with a later 4E profile, but it should not implement or advertise
4E in M01 unless the migration step is explicitly expanded.

In image metadata, a `Device/bananapi_bpi-r4-pro-common` helper is reasonable if
it contains only true R4 Pro common image/build metadata. It must not inherit
plain `Device/bananapi_bpi-r4-common`, because regular R4 and R4 Pro are
different boards and that helper includes regular R4 package/overlay/storage
assumptions.

There is no need for a `bananapi_bpi-r4-pro-8x-common` helper in M01 unless
there are multiple 8X-specific OpenWrt profiles that share nontrivial metadata.
For one 8X profile it is extra structure without value.

## DTS Implementation Decision

For M01, the main-agent rewrite should:

- port/adapt the upstream Linux R4 Pro DTS split into the OpenWrt 25.12 kernel
  patch structure;
- keep the 8X top-level DTS minimal and model/compatible-specific;
- place shared R4 Pro hardware description in the R4 Pro common DTSI;
- re-evaluate each vendor-copied 8X overlay against upstream R4 Pro overlays
  before retaining it;
- record whether each DTS/DTSO file is copied, copied-and-adapted, or newly
  written from target patterns.

The previous draft's vendor 8X overlays `-rtc`, `-sd`, `-emmc`, and
`-wifi-mt7996a` were direct vendor copies. The `-sd` and `-emmc` behavior should
be compared with the upstream R4 Pro shared overlays. The RTC behavior is
already present in the upstream R4 Pro common DTSI rather than as a separate
overlay. Wi-Fi overlay behavior is M06-owned and should be dropped/deferred from
M01 unless it is strictly required for DTB/DTBO build closure. Any retained
direct vendor copy must be explicitly justified against upstream Linux and
target OpenWrt 25.12.

Wi-Fi overlay behavior belongs to M06. Storage runtime semantics belong to
M02/M10. RTC/fan/USB/PCIe/LED/button runtime checks belong to M03/M09. If a
node is included in M01 only because the upstream common DTSI requires it for
compile closure, mark it as compile-only and do not claim runtime validation.

## Known Target API Differences

The direct vendor 8X kernel tree is a 6.6-era source and uses labels that do not
match the OpenWrt 25.12 / upstream 6.12-era DTS API:

- vendor uses `uart0`, `uart1`, `uart2`; target/upstream uses `serial0`,
  `serial1`, `serial2`;
- vendor uses `xphy`; target/upstream uses `xsphy` and related xphy port labels;
- vendor places a `fan` node in the SoC DTSI, while target/upstream board DTSI
  carries the board fan node.

Do not fix these by copying unrelated plain BPI-R4 common content. The correct
fix is to port the R4 Pro DTS against the OpenWrt 25.12 target DTS labels and
patch order.

## TF-A, U-Boot, and Image Metadata

TF-A:

- Preserve the 4 GB DDR behavior, but keep it scoped to new 8X/R4-Pro-specific
  targets rather than changing shared MT7988 comb targets.
- This is a narrow build metadata change for M01.

U-Boot:

- Vendor 8X U-Boot build targets are useful evidence for the eMMC/SDMMC/SNAND
  variants, but the patch must be adapted to current OpenWrt U-Boot patch/env
  style.
- U-Boot env files in M01 must stay build-skeleton-only. Do not add install,
  flash-write, reset-factory, `saveenv`, `mmc write`, `mtd write`, or UBI write
  flows in M01.
- Upstream U-Boot has the same R4 Pro DTS split available as reference, but its
  details still need comparison; do not blindly copy either vendor or upstream
  U-Boot DTS.

Image recipe:

- Add only the 8X profile and M01-required artifacts.
- Do not pull in regular R4 common metadata wholesale.
- Do not add vendor factory/install artifacts such as `emmc.img.gz`,
  `snand-factory.bin`, or `mt798x-r4pro-gpt` unless a later step explicitly
  owns and validates those flows.

## Validation Gate

All build and verification commands should use maximum available parallelism:

```sh
make -j$(nproc)
make -j$(nproc) V=s
```

Do not use single-threaded or fixed four-thread validation commands for this
project unless the user explicitly requests a one-off diagnostic exception.

M01 validation may prove only:

- profile selection and `defconfig`;
- TF-A and U-Boot build metadata compile;
- kernel DTB/DTBO build closure;
- expected image/artifact names under `bin/targets/mediatek/filogic/`.

M01 validation does not prove boot, networking, Wi-Fi, storage install,
sysupgrade, or runtime hardware behavior.

## Handoffs

- M02 owns SD boot, SD overlay/rootdisk semantics, U-Boot SD boot path, and
  serial boot evidence with no NAND/eMMC writes.
- M03 owns board identity, GPIO, I2C, and factory data.
- M04 owns basic wired management network.
- M05 owns full wired switch, SFP, and 10G behavior.
- M06 owns Wi-Fi hardware, firmware, EEPROM, and radio detection.
- M09 owns board extras such as fan, RTC, LEDs, buttons, USB, PCIe, and NVMe.
- M10 owns onboard storage, install, sysupgrade, and any NAND/eMMC write path.

The M01 report must list changed files, source/action per file, preserved
behavior, rejected/deferred behavior, build evidence, and residual risks.
