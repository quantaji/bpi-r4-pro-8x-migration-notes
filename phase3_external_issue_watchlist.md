# Phase 3 External Issue Watchlist

This watchlist records external integration issues and observed runtime/build
risks that Phase 3 implementation agents should check while migrating BPI-R4
Pro 8X support to OpenWrt 25.12.

It is not an implementation plan and not a source of hardware truth. Direct
8X vendor source, current target OpenWrt 25.12 source, board schematics, and
fresh runtime evidence still decide the final design.

Use this file as a warning index:

1. read the matching Phase 3 worklist row first,
2. inspect direct 8X vendor evidence,
3. inspect target OpenWrt 25.12 structure and APIs,
4. use PR discussion only as integration context,
5. verify any observed issue against current source/runtime before changing
   code.

## Source Labels

- `PR21083`: OpenWrt PR #21083, "mediatek: add support for BananaPi BPi-R4 Pro 8X".
- `PR23477`: OpenWrt PR #23477, "generic: update MxL862xx DSA switch driver".
- `PR23664`: OpenWrt PR #23664, "generic: mxl862xx: allow CPU/SerDes ports to probe on firmware < 1.0.84".
- `observed-risk`: local runtime/build issue observation that must be revalidated
  in the current migration before use.

## Issues

| ID | Migration step | Area | Possible issue | Required Phase 3 handling | Source |
| --- | --- | --- | --- | --- | --- |
| EXT-001 | M01 | Build skeleton / DTSO | Early PR discussion reported build failures from missing DTSO files. | Do not declare M01 complete until DTS/DTSO selection and generated image metadata are checked against the target build. | PR21083 |
| EXT-002 | M01 | U-Boot target naming | U-Boot config/DTS filenames may be easy to mis-name across SD/eMMC/SPI-NAND variants. | Verify U-Boot defconfig names, TF-A/FIP output names, image recipe names, and generated artifact names as one set. | PR21083 |
| EXT-003 | M01 | Kernel version split | PR #21083 currently carries 6.18 patches, while this migration targets OpenWrt 25.12.4 source state. | Treat PR patch layout as structure/reference only; port against the actual target kernel patch stack. | PR21083 |
| EXT-004 | M02 | SD boot switch / boot media | SD card boot can fail for reasons unrelated to Linux DTS if BL2/FIP/U-Boot variant selection is wrong. | Validate serial boot logs and boot-media selection before changing Linux hardware descriptions. | PR21083 |
| EXT-005 | M02 | SD image layout | A truncated SD image can have valid primary GPT and boot offsets but still warn about the backup GPT. | Decide explicitly whether release images should be padded to the full GPT span or documented as truncated-after-rootfs. | observed-risk |
| EXT-006 | M03 | GPIO4 ownership | GPIO4 has conflicting interpretations: switch reset versus Wi-Fi 12V enable. | Resolve from direct 8X vendor source, schematic, and live runtime. Do not copy a Wi-Fi regulator using GPIO4 unless that evidence is confirmed. | observed-risk |
| EXT-007 | M03 | Factory MAC data | Factory nvmem cells may not provide valid usable MACs on all boards. | Verify Factory offsets on real hardware before wiring MAC consumers. If invalid, design a documented fwenv/UCI fallback. | observed-risk |
| EXT-008 | M03 | I2C EEPROM inventory | Wi-Fi EEPROM at `0x51` is stronger evidence than a second unverified `0x52` device. | Do not model a second Wi-Fi EEPROM or pcie1 nvmem cell without live DT/I2C evidence or direct 8X proof. | observed-risk |
| EXT-009 | M03 | PMIC rails | RT5190A buck/LDO values may affect board peripherals and should not be guessed from related boards. | Verify voltage values against direct vendor source, schematic, or live regulator state before changing DTS. | observed-risk |
| EXT-010 | M04 | `board.d` network defaults | PR discussion says the UCI network config was wrong while only an internal switch port worked. | Generate board defaults only from kernel-exposed netdevs and direct 8X topology. Do not invent final port names from PR or vendor text alone. | PR21083 |
| EXT-011 | M04 | Temporary management path | A one-port management path can be valid for early bring-up but must not become final topology. | Keep M04 separate from M05. Mark any internal-switch-only path as management/temporary unless full 8X topology is validated. | observed-risk |
| EXT-012 | M05 | Missing MxL86252 support | PR discussion identifies missing MaxLinear switch support as a blocker for router-class wired behavior. | Treat MxL86252 DSA/tagger/PHY support as an M05 design item, not a board.d naming issue. | PR21083 |
| EXT-013 | M05 | MxL firmware version gate | Boards may ship MxL firmware `1.0.70`, while later upstream driver work may gate behavior on newer firmware. | Design for the firmware actually present on 8X hardware or provide a verified firmware-update path. | PR23477; PR23664 |
| EXT-014 | M05 | Empty phylink supported interfaces | Old MxL firmware can leave CPU/SerDes port interface support empty and prevent switch probing. | Check current target driver behavior for old-firmware CPU/SerDes ports, especially ports used by 8X. | PR23664 |
| EXT-015 | M05 | MxL old-firmware DSA setup timeout | Old MxL firmware can time out during DSA/tag/VLAN setup. | Keep old-firmware compatibility as a first-class runtime gate. Do not assume a firmware blob exists unless found and tested. | observed-risk |
| EXT-016 | M05 | Eth mux dependency | PR discussion says SFP/10G behavior depends on eth-mux work and that downstream mux hacks are not preferred upstream. | Prefer target-compatible upstream/backport structure, but preserve verified 8X mux behavior. Document any downstream-only bridge. | PR21083 |
| EXT-017 | M05 | SFP/RJ45 combo behavior | PR discussion says SFP slots may not be usable without mux support; temporary GPIO-hog approaches may only force one side. | Validate SFP1/SFP2, RJ45, and combo switching separately. Do not claim combo behavior from no-cable enumeration. | PR21083 |
| EXT-018 | M05 | AS21010P / AS21xxx PHY binding | External 10G PHYs can appear as generic C45 or unbound until firmware/model handling is correct. | Verify PHY ID, DT compatible, firmware load ordering, supported modes, and final driver binding on both external PHYs. | observed-risk |
| EXT-019 | M05 | AS21xxx IPC timing | AS21xxx IPC can fail with timeouts if firmware readiness, command matching, or loader-busy states are mishandled. | Treat `-110` and empty firmware-version reads as driver sequencing problems, not as proof to change board topology. | observed-risk |
| EXT-020 | M05 | AS21xxx phylink `-22` | `mtk_open: could not attach PHY: -22` can come from speed-less supported masks or early open timing. | Fix the driver/phylink evidence path before changing DTS PHY mode or topology. | observed-risk |
| EXT-021 | M05 | Vendor versus PR DSA port numbering | Vendor DTS port numbers may not map directly to PR/upstream driver binding semantics. | Translate port indexes through the selected driver binding and document the translation. Do not mechanically copy `reg` values. | observed-risk |
| EXT-022 | M05 | SFP module compatibility | SFP module quirks and bad checksum handling can affect final link behavior. | Keep module-compatibility quirks as M05/M09 follow-up unless a real SFP test reproduces them. | observed-risk |
| EXT-023 | M06 | MT7996 firmware startup | Official-style Wi-Fi can work on cold start but still show hot-start firmware patch startup failures. | Validate reload, reboot, and warm-start Wi-Fi behavior, not only first boot firmware load. | observed-risk |
| EXT-024 | M06 | PCIe Wi-Fi modeling | PCIe child nodes and nvmem cells for Wi-Fi can be over-modeled from overlay-only evidence. | Keep pcie0/pcie1 and EEPROM modeling tied to direct 8X or live runtime evidence. | observed-risk |
| EXT-025 | M06 | PCIe probe timeouts | Some PCIe controllers can report probe timeout symptoms during baseline runtime. | Separate harmless absent-device probe noise from Wi-Fi/NVMe/expansion failures before changing pinctrl or reset logic. | observed-risk |
| EXT-026 | M07 | Ordinary AP versus MLO | Vendor userspace patches mix ordinary AP behavior with MLO/MLD/radio-mask policy. | Preserve ordinary AP bring-up separately from MLO/AFC/6GHz policy; do not replay the whole userspace stack. | observed-risk |
| EXT-027 | M07 | 6GHz/AFC/regulatory | PR and vendor work do not prove that 6GHz/AFC/regulatory policy is correct for release. | Treat 6GHz/AFC/regdb changes as needs-evidence until target policy and runtime behavior are checked. | observed-risk |
| EXT-028 | M07 | Hostapd and iw provenance | MLO/radio-mask work may already exist in target in a different form. | Compare target hostapd/iw/mac80211 stack before importing vendor patches. Preserve ordinary AP path. | observed-risk |
| EXT-029 | M08 | LuCI/offload ambiguity | UI hardware-flow-offload state does not prove vendor HNAT/PPE/WED behavior. | Validate forwarding datapath counters and traffic directionality; do not rely on UI flags. | observed-risk |
| EXT-030 | M08 | WED and 8GB memory | WED/mt76 DMA mask and GFP_DMA32 behavior can matter on boards with 4GB or more DRAM. | Audit target WED/mt76 allocation paths before declaring WED reliable on 8GB 8X hardware. | observed-risk |
| EXT-031 | M08 | DSA/PPE tag participation | MxL DSA tags and internal VLANs can affect PPE binding and flow classification. | Validate PPE entries for MxL DSA paths, not only internal MT7530 paths. | observed-risk |
| EXT-032 | M08 | PPPQ/QDMA/virtual interface paths | Vendor offload patches may cover macvlan, PPPoE, VLAN, bridge, and syncdial-like paths differently. | Test routed forwarding, bridge-nf policy, PPPoE, VLAN-over-DSA, and macvlan separately. | observed-risk |
| EXT-033 | M08 | WED/roaming stale flows | Vendor roaming teardown and WED/WDMA reset fixes may need mt76-side cooperation. | Validate Wi-Fi-to-wired offload, Wi-Fi reload, station roam, and stale-flow teardown after M06/M07 are stable. | observed-risk |
| EXT-034 | M08 | HNAT/netlink/tunnel stack | Full vendor HNAT/netlink/tunnel userland may not be required if nft/PPE/WED paths cover the use case. | Keep HNAT/netlink/tunnel import as an explicit design decision, not an automatic vendor replay. | observed-risk |
| EXT-035 | M09 | PCIe/NVMe support | PR review requested PCIe/NVMe support beyond the initial board support. | Verify PCIe overlays, pinctrl, reset, and package selection before declaring expansion support. | PR21083 |
| EXT-036 | M09 | PCIe mux side effects | PCIe mux decisions can affect Wi-Fi, NVMe, and M.2 B-Key expansion. | Treat PCIe mux as a board-level design item and test each slot/role independently. | observed-risk |
| EXT-037 | M09 | USB controller quirks | Vendor DTS may delete or alter USB speed-fixup properties. | Verify target base DTS and USB runtime before changing USB behavior. | observed-risk |
| EXT-038 | M09 | Fan/RTC/power monitors | Board extras such as fan PWM, RTC, INA226, LEDs, and buttons are easy to make compile-only. | Require runtime enumeration and function checks before closing M09 extras. | observed-risk |
| EXT-039 | M10 | Boot-media U-Boot variants | PR discussion says U-Boot behavior differs by SD, SPI-NAND, and eMMC because install menus differ. | Keep separate boot-media U-Boot/FIP/env validation. Do not use one boot mode to prove all modes. | PR21083 |
| EXT-040 | M10 | Onboard install order | SD can be used to install SPI-NAND, and SPI-NAND can then install eMMC; direct eMMC/NAND ordering must be chosen deliberately. | Do not write onboard media until SD boot and serial recovery are repeatably proven. Validate SPI-NAND/eMMC flows separately. | PR21083 |
| EXT-041 | M10 | Missing eMMC artifacts | Vendor-style eMMC outputs may include GPT, preloader, FIP, and full image artifacts not present in a simple SD skeleton. | Decide which artifacts are required for this migration and document any deliberate omission. | observed-risk |
| EXT-042 | M10 | Missing SPI-NAND artifacts | Vendor-style SPI-NAND outputs may include preloader, FIP, and factory image artifacts. | Keep SPI-NAND factory/install generation separate from SD boot until storage policy is settled. | observed-risk |
| EXT-043 | M10 | SPI-NAND partition map | SPI-NAND `Factory` and `ubi` offsets must match direct 8X/runtime evidence. | Verify `/proc/mtd`, UBI rootdisk binding, and rootfs behavior before enabling install/sysupgrade. | observed-risk |
| EXT-044 | M10 | Reset boot count | reset-boot-count behavior can involve SMC/procfs or DTS properties not present in direct 8X evidence. | Keep reset-boot-count as evidence-only unless direct 8X target policy proves it is needed. | observed-risk |
| EXT-045 | M11 | Open PR state | PR #21083 is open and not a final accepted upstream design. | Use it as integration context and source of review objections, not as target truth. | PR21083 |
| EXT-046 | M11 | Related landed PRs | Related MxL fixes may land separately from the board-support PR. | Recheck target OpenWrt before porting any PR-derived MxL/PHY/SFP workaround. | PR23477; PR23664 |
| EXT-047 | M11 | Firmware/package closure | Official runtime includes AS21xxx, AQR, EIP197, mt7988 WO, and mt7996 firmware families; missing packages may cause silent runtime gaps. | Compare final image package manifest against direct 8X runtime needs and target package names. | observed-risk |
| EXT-048 | M11 | Release success claims | Build success, no-cable enumeration, link-up, traffic, offload, Wi-Fi AP, sysupgrade, and onboard install are separate claims. | Keep release notes and acceptance evidence split by feature and test type. | observed-risk |

## PR Source Links

- `PR21083`: https://github.com/openwrt/openwrt/pull/21083
- `PR21083.diff`: https://github.com/openwrt/openwrt/pull/21083.diff
- `PR21083.patch`: https://github.com/openwrt/openwrt/pull/21083.patch
- `PR23477`: https://github.com/openwrt/openwrt/pull/23477
- `PR23664`: https://github.com/openwrt/openwrt/pull/23664

Archived PR data is stored outside this notes repository:

```text
../analysis/external-evidence/openwrt-pr-21083-bpi-r4-pro-8x/raw/
```

The PR head source checkout is stored outside this notes repository:

```text
../reference-source-codes/external-prs/openwrt-pr-21083-bpi-r4-pro-8x/
```
