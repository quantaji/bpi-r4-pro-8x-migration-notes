# Archived Legacy Semantic Tagging Rule

Archived on 2026-06-08.

This document is not used for the current Phase 1a feature-routing pass.
Phase 1a now assigns only `feature_tags` with `feature_routing_skill.md`,
`rules/feature-tags-v1.json`, and `rules/feature-seed-rules-v1.json`.

The `origin`, `scope`, and related semantic tagging model below is kept only as
legacy reference for later feature-cluster review and migration design.

# Modification Tag Guide

## 1. Purpose

This document defines three modification-level tag sets:

```text
origin
scope
migration_feature
```

These tags describe a local modification. They do not make final migration decisions.

Final decisions belong to cluster-level analysis.

## 2. Tagging Unit

Preferred unit:

```text
semantic modification
```

A semantic modification may be:

```text
one diff hunk
several adjacent hunks with one purpose
one added board case
one changed device definition
one deleted file
one package/config change with one clear purpose
```

If a file has unrelated changes, split it into multiple semantic modifications.

If a file is small and single-purpose, file-level tagging is acceptable.

Recommended output columns:

```text
mod_id
file_path
hunk_hint
short_description
origin
scope
migration_feature
evidence
notes
```

`migration_feature` may contain multiple comma-separated values.

---

# 3. Origin Tag

`origin` answers:

```text
Where did this modification most likely come from?
```

It describes provenance only. It does not decide whether the change is good, correct, or should be migrated.

## 3.1 Allowed Values

```text
openwrt-upstream
mtk-inherited
mtk-plus-bpi
bpi-only
openwrt-main
linux-upstream-backport
uboot-upstream-backport
mt76-upstream-backport
bpi-other-board
build-noise
unknown
```

## 3.2 Definitions

### `openwrt-upstream`

The modification already exists in relevant OpenWrt upstream, or the vendor version is materially equivalent.

Evidence:

```text
same/equivalent logic in OpenWrt upstream
same/equivalent logic in OpenWrt 25.12
vendor diff caused by baseline mismatch
```

Do not use only because the file exists upstream. The modification itself must match.

### `mtk-inherited`

The modification appears inherited from MTK SDK/feed without meaningful BPI-specific change.

Evidence:

```text
same path modified by mtk-openwrt-feeds
same/equivalent content in openwrt-24.10-mtk or openwrt-25.12-mtk
patch-id/content match
generic MTK/Filogic/MT7988 support
```

This does not imply the code should be copied.

### `mtk-plus-bpi`

The modification is based on MTK code, with BPI board-specific changes.

Evidence:

```text
same file/patch exists in MTK
vendor adds BPI compatible/device/image entry
vendor modifies MTK RFB/DTS/DTSO for BPI behavior
vendor changes board.d/sysupgrade on top of MTK logic
```

Interpret as two layers:

```text
MTK base functionality
BPI board-specific delta
```

### `bpi-only`

The modification appears created by BPI, with no clear MTK or upstream origin.

Evidence:

```text
not found in MTK 21.02/24.10/25.12/master
not found in OpenWrt upstream
not found in Linux/U-Boot/mt76 upstream
contains BPI-specific compatible/device/board logic
exists only in BPI vendor sources
```

### `openwrt-main`

The modification or equivalent implementation exists in OpenWrt main, but not in the target OpenWrt 25.12 baseline.

Evidence:

```text
same/equivalent patch in openwrt-main
device/target integration landed after 25.12 branch
```

### `linux-upstream-backport`

Linux kernel change from Linux upstream, newer stable, net-next, or submitted upstream series.

Evidence:

```text
same commit in Linux mainline/stable/newer version
patch-id match
same subject/content on mailing list
touches kernel driver, DTS, binding, PHY, DSA, PCS, SFP, MTD, PCIe, crypto, networking core
```

Use only for Linux-side changes.

### `uboot-upstream-backport`

U-Boot change from upstream U-Boot or newer U-Boot branch.

Evidence:

```text
same patch in upstream U-Boot
same board/driver change in U-Boot mainline
touches package/boot/uboot-* or U-Boot source integration
```

### `mt76-upstream-backport`

mt76-specific wireless change from upstream mt76.

Evidence:

```text
same patch in openwrt/mt76
touches mt76 driver, firmware loading, EEPROM/calibration, WED, Wi-Fi 7 support
```

Do not use for generic mac80211, hostapd, or wifi-scripts unless clearly mt76-specific.

### `bpi-other-board`

Modification likely copied or adapted from another BPI board vendor tree.

Evidence:

```text
similar logic in BPI-R4 Pro 4E
similar logic in BPI-R4
similar script pattern in BPI-R4 Lite
not clearly MTK or upstream
```

This is source, not applicability.

### `build-noise`

Not meaningful source modification for hardware/software behavior.

Evidence:

```text
generated files
download/cache/build output
CI metadata
editor/system files
vendor tree missing upstream metadata
```

Usually excluded from cluster analysis unless needed for reproducibility.

### `unknown`

Source cannot be determined.

Use instead of guessing. Record what was checked.

Example note:

```text
Checked OpenWrt 24.10, OpenWrt 25.12, MTK 24.10, MTK 25.12. No exact match found.
```

---

# 4. MTK Version Field

`mtk_version` is a companion field to `origin`. It should not replace `origin`.

Allowed values:

```text
none
mtk-21.02
mtk-24.10
mtk-25.12
mtk-master
mixed
unknown
```

Definitions:

```text
none        no MTK source relation
mtk-21.02  closest MTK source is 21.02
mtk-24.10  closest MTK source is 24.10
mtk-25.12  closest MTK source is 25.12
mtk-master closest visible source is MTK master
mixed       parts come from different MTK versions
unknown     MTK-related but version unknown
```

Prefer splitting a modification over using `mixed`.

Examples:

```text
origin = mtk-plus-bpi
mtk_version = mtk-24.10

origin = linux-upstream-backport
mtk_version = none
```

---

# 5. Scope Tag

`scope` answers:

```text
How broadly does this modification apply?
```

It describes applicability, not source.

Allowed values:

```text
8x-only
r4-pro-common
mt7988-common
filogic-common
bpi-style-common
openwrt-generic
build-only
unknown
```

## 5.1 Definitions

### `8x-only`

Specific to BPI-R4 Pro 8X.

Evidence:

```text
only in 8X vendor tree
contains 8X device name/compatible
8X image definition
8X port layout
8X 10G SFP/RJ45 combo behavior
AS21010P or MxL86252 behavior specific to 8X
not shared with 4E, R4, or Lite
```

### `r4-pro-common`

Applicable to both BPI-R4 Pro 8X and BPI-R4 Pro 4E.

Evidence:

```text
same/similar semantic change in 8X and 4E
common R4 Pro board structure
shared storage, LED, fan, PCIe, sysupgrade, DTSI, or board logic
not present in non-Pro R4 or Lite
```

Do not use only because both boards edit the same file. The semantic behavior must be shared.

### `mt7988-common`

Applicable to MT7988-based boards generally.

Evidence:

```text
shared by R4 Pro and R4
MT7988 Ethernet, PCS, PPE, WED, PCIe, SNAND, clock, pinctrl, CPU/thermal
not specific to one BPI board
```

Board wiring may still be board-specific even if the SoC block is common.

### `filogic-common`

Applicable across broader MediaTek Filogic family.

Evidence:

```text
similar logic across MT7981/MT7986/MT7987/MT7988
generic Filogic image, storage, package, board.d, or driver-family pattern
not tied to one SoC or board
```

Use carefully. Similarity across BPI repos may be vendor style rather than hardware commonality.

### `bpi-style-common`

BPI vendor coding style or tree organization, not proof of shared hardware.

Evidence:

```text
similar shell style across BPI boards
similar package/default config pattern
similar vendor patch organization
similar habit of modifying RFB files instead of adding clean board files
not clearly tied to shared hardware
```

### `openwrt-generic`

Generic OpenWrt behavior, not board-specific or MTK-specific.

Evidence:

```text
generic OpenWrt scripts
generic package/build logic
generic image commands
generic tooling
affects all targets or many unrelated targets
```

Use with caution because generic changes can affect many devices.

### `build-only`

Only affects local build configuration, repository shape, build metadata, or non-source generated artifacts.

Evidence:

```text
.config package selection
feeds.conf for vendor build reproduction
deleted CI/.github files
download cache
generated output
```

May help reproduce vendor build, but is not hardware support by default.

### `unknown`

Applicability cannot be determined.

Use when:

```text
semantic sharing unclear
may be board-specific or SoC-common
requires hardware documentation, runtime testing, or comparison with 4E/R4/Lite/MTK/upstream
```

---

# 6. Origin and Scope Are Independent

Do not conflate source and applicability.

Examples:

```text
origin = mtk-inherited
scope = mt7988-common
```

Generic MT7988 change inherited from MTK.

```text
origin = bpi-only
scope = 8x-only
```

BPI-created 8X-specific change.

```text
origin = bpi-other-board
scope = r4-pro-common
```

Likely copied/adapted from another BPI Pro board and applicable to R4 Pro variants.

```text
origin = openwrt-upstream
scope = openwrt-generic
```

Generic OpenWrt behavior already represented upstream.

```text
origin = mtk-plus-bpi
scope = 8x-only
```

MTK-derived implementation with BPI 8X-specific additions.

---

# 7. Migration Feature Tag

`migration_feature` answers:

```text
Which migration task or functional area does this modification serve?
```

It should help derive task order, cluster membership, and test scope.

Format:

```text
domain:subsystem:function
```

Examples:

```text
boot:uboot:env
network:phy:10gbase-t
network:combo:sfp-rj45
wireless:mt76:firmware
cellular:sim:interface
accel:ppe:flow-offload
```

Rules:

```text
Use router-generic feature tags at modification level.
Do not bind too early to 8X-specific chips or ports.
Bind concrete 8X hardware in cluster metadata.
Multiple migration_feature values are allowed.
```

Example:

```text
migration_feature = network:phy:10gbase-t, firmware:phy:runtime
cluster = as21010p-10g-rj45
hardware_binding = AS21010P, 10G RJ45 WAN/LAN
```

## 7.1 Source / Build

```text
source:tree:metadata
source:tree:cleanup
source:feeds:base-feed-config
source:feeds:external-feed-config

build:toolchain:config
build:tools:host-tool
build:scripts:helper
build:kernel:config
build:package:makefile
```

Typical files:

```text
feeds.conf.default
tools/Makefile
scripts/feeds
scripts/mkits.sh
config/Config-kernel.in
package/Makefile
.config
```

## 7.2 Boot Chain

```text
boot:tf-a:build
boot:tf-a:bl2
boot:tf-a:fip

boot:uboot:build
boot:uboot:target
boot:uboot:dts
boot:uboot:defconfig
boot:uboot:env
boot:uboot:bootmenu
boot:uboot:recovery
boot:uboot:storage-layout

boot:recovery:initramfs
boot:recovery:failsafe
boot:recovery:factory-install
```

Typical files:

```text
package/boot/arm-trusted-firmware-mediatek/Makefile
package/boot/uboot-mediatek/Makefile
package/boot/uboot-mediatek/patches/*
package/boot/uboot-envtools/files/mediatek_filogic
target/linux/mediatek/image/filogic.mk
```

## 7.3 Device Tree / Hardware Description

```text
dts:soc:base
dts:board:base
dts:board:variant
dts:overlay:storage
dts:overlay:pcie
dts:overlay:network
dts:overlay:combo
dts:overlay:wifi
dts:overlay:cellular

dts:gpio:control
dts:pinctrl:function
dts:clock-reset:binding
dts:regulator:power
dts:nvmem:factory-data
dts:partition:layout
dts:led:definition
dts:button:definition
dts:thermal:zone
dts:fan:pwm
```

Typical files:

```text
target/linux/mediatek/files-*/arch/arm64/boot/dts/mediatek/*.dts
target/linux/mediatek/files-*/arch/arm64/boot/dts/mediatek/*.dtsi
target/linux/mediatek/files-*/arch/arm64/boot/dts/mediatek/*.dtso
target/linux/mediatek/patches-*/*.patch
```

## 7.4 Storage / Partition / Sysupgrade

```text
storage:emmc:boot
storage:emmc:rootfs
storage:sd:boot
storage:sd:rootfs
storage:spi-nand:boot
storage:spi-nand:ubi
storage:spi-nand:nmbm
storage:spi-nor:boot
storage:partition:factory
storage:partition:fip
storage:partition:recovery
storage:partition:rootfs
storage:factory-data:nvmem
storage:sysupgrade:platform
storage:sysupgrade:compatibility
storage:sysupgrade:backup-restore
```

Typical files:

```text
target/linux/mediatek/image/filogic.mk
target/linux/mediatek/filogic/base-files/lib/upgrade/platform.sh
package/boot/uboot-envtools/files/mediatek_filogic
DTS partition nodes
```

## 7.5 Identity / MAC / Factory Data

```text
identity:mac:ethernet
identity:mac:wifi
identity:mac:wwan
identity:nvmem:factory
identity:uboot-env:ethaddr
identity:calibration:wifi
identity:calibration:phy
```

Typical files:

```text
board.d/*
uci-defaults/*
DTS nvmem cells
uboot-envtools
factory partition handling
```

## 7.6 Wired Network Core

```text
network:mac:mtk-eth
network:pcs:usxgmii
network:pcs:10gbase-r
network:mdio:bus
network:phy:generic
network:phy:2p5gbase-t
network:phy:10gbase-t
network:sfp:cage
network:sfp:hotplug
network:dsa:switch
network:dsa:tagging
network:dsa:port-map
network:port-label:lan-wan
network:default-config:bridge
network:default-config:wan
network:vlan:bridge
network:led:port
```

Typical files:

```text
target/linux/mediatek/patches-*/*
target/linux/mediatek/files-*/arch/arm64/boot/dts/mediatek/*
target/linux/mediatek/filogic/base-files/etc/board.d/02_network
package/kernel/linux/modules/netdevices.mk
```

## 7.7 Wired Switch / PHY

```text
network:switch:external-dsa
network:switch:firmware
network:switch:port-statistics
network:switch:vlan-offload
network:switch:lag
network:switch:mirror

network:phy:firmware
network:phy:multi-rate
network:phy:led
network:phy:reset
network:phy:interrupt
```

Cluster binding examples:

```text
network:switch:external-dsa -> MxL86252/MxL86282 cluster
network:phy:multi-rate + network:phy:firmware -> AS21010P cluster
```

## 7.8 SFP / RJ45 Combo

```text
network:combo:static-selection
network:combo:gpio-mux
network:combo:sfp-rj45
network:combo:wan-path
network:combo:lan-path
network:combo:runtime-switch
network:combo:offload-flush
network:sfp:module-detect
network:sfp:tx-disable
network:sfp:i2c
```

Use for combo behavior, not ordinary Ethernet.

Recommended migration order:

```text
ordinary MAC/PCS/MDIO
static SFP path
static RJ45 PHY path
static combo variants
runtime dynamic switching
```

## 7.9 Wireless

```text
wireless:pcie:nic
wireless:mt76:driver
wireless:mt76:firmware
wireless:mt76:eeprom
wireless:mac80211:patch
wireless:hostapd:build
wireless:hostapd:ucode
wireless:wifi-scripts:netifd
wireless:wifi-scripts:ucode
wireless:mlo:config
wireless:mlo:runtime
wireless:regulatory:db
wireless:calibration:eeprom
wireless:wed:firmware
wireless:wed:runtime
```

Do not mix wireless with cellular. Cellular is a separate domain.

## 7.10 Cellular / WWAN / SIM

```text
cellular:slot:m2-bkey
cellular:slot:minipcie
cellular:usb:composition
cellular:modem:qmi
cellular:modem:mbim
cellular:modem:serial
cellular:modem:firmware
cellular:sim:interface
cellular:sim:mux
cellular:sim:detect
cellular:power:control
cellular:reset:control
cellular:hotplug:wwan
cellular:userspace:uqmi
cellular:userspace:umbim
cellular:userspace:modemmanager
cellular:network:wan-interface
```

Use for M.2 B-key, miniPCIe cellular, SIM, modem userspace, and WWAN network integration.

## 7.11 Expansion / Peripheral Bus

```text
bus:pcie:controller
bus:pcie:lane-map
bus:pcie:reset
bus:pcie:power
bus:pcie:hotplug

bus:usb:controller
bus:usb:hub
bus:usb:power
bus:usb:otg

bus:i2c:controller
bus:i2c:mux
bus:spi:controller
bus:mdio:controller
bus:gpio:controller
```

```text
expansion:nvme:m2-mkey
expansion:nvme:power
expansion:nvme:pcie
expansion:minipcie:wifi
expansion:minipcie:cellular
expansion:m2-bkey:cellular
```

Use for buses and slots, not the final device behavior. For example, cellular modem work should use both `bus:*` and `cellular:*` when appropriate.

## 7.12 Thermal / Fan / UI

```text
thermal:zone:soc
thermal:fan:pwm
thermal:fan:policy
thermal:cooling-device:binding
thermal:trip-point:config

ui:led:power
ui:led:network-port
ui:led:wifi
ui:button:reset
ui:button:wps
ui:button:bootstrap
```

Fan/thermal should be available before heavy network, Wi-Fi, or acceleration testing.

## 7.13 Firmware / Calibration

```text
firmware:wifi:runtime
firmware:wifi:eeprom
firmware:phy:runtime
firmware:switch:runtime
firmware:wed:wo
firmware:cellular:modem
firmware:boot:blob
firmware:calibration:factory
```

Firmware tags should also appear in the relevant hardware cluster. Do not treat firmware as unrelated package selection.

## 7.14 Hardware Acceleration

```text
accel:ppe:flow-offload
accel:hnat:nat
accel:hnat:routing
accel:wed:wifi-offload
accel:tops:tunnel-offload
accel:crypto:eip
accel:rss:rx-distribution
accel:lro:rx-aggregation
accel:switch:vlan-offload
accel:switch:bridge-offload
accel:flowtable:nft
```

Hardware acceleration should be migrated after correctness. It can hide bugs by bypassing slow paths.

## 7.15 OpenWrt Runtime Integration

```text
openwrt:base-files:board-detect
openwrt:board-d:network
openwrt:board-d:leds
openwrt:uci-defaults:factory
openwrt:hotplug:network
openwrt:hotplug:wifi
openwrt:hotplug:cellular
openwrt:init:service
openwrt:package:device-packages
openwrt:package:kernel-modules
openwrt:firewall:defaults
openwrt:network:defaults
```

Use for OpenWrt behavior and defaults. Do not encode OpenWrt policy in DTS.

---

# 8. Migration Order Implied by `migration_feature`

Use this as a rough ordering guide:

```text
0. source/build hygiene
   source:*, build:*

1. boot and recovery
   boot:*, minimal image:*

2. base hardware description
   dts:board:base, dts:soc:base, dts:gpio:control, dts:pinctrl:function,
   dts:regulator:power, dts:thermal:zone, dts:fan:pwm

3. storage, partition, sysupgrade, identity
   storage:*, identity:*, boot:uboot-env:*

4. minimal manageability
   network:mac:mtk-eth, network:mdio:bus, network:port-label:lan-wan,
   openwrt:board-d:network

5. wired network completeness
   network:pcs:*, network:phy:*, network:dsa:*, network:switch:*, network:vlan:*

6. SFP/RJ45 combo
   network:sfp:*, network:combo:*

7. expansion buses
   bus:*, expansion:*

8. wireless
   wireless:*, firmware:wifi:*, firmware:wed:*

9. cellular and SIM
   cellular:*, firmware:cellular:*, openwrt:hotplug:cellular

10. UI and runtime defaults
   ui:*, openwrt:network:defaults, openwrt:firewall:defaults

11. hardware acceleration and performance
   accel:*
```

---

# 9. Cluster Binding

`migration_feature` should remain router-generic.

8X-specific hardware binding belongs to cluster metadata.

Example:

```text
cluster_name: as21010p-10g-rj45
migration_features:
  - network:phy:10gbase-t
  - network:phy:multi-rate
  - firmware:phy:runtime
hardware_binding:
  board: BPI-R4 Pro 8X
  chips:
    - AS21010P
  ports:
    - 10G RJ45 WAN
    - 10G RJ45 LAN
dependencies:
  - mt7988-wired-core
  - sfp-rj45-combo-mux
```

Example:

```text
cluster_name: cellular-wwan
migration_features:
  - cellular:slot:m2-bkey
  - cellular:usb:composition
  - cellular:sim:interface
  - cellular:userspace:uqmi
  - cellular:network:wan-interface
hardware_binding:
  board: BPI-R4 Pro 8X
  slots:
    - M.2 B-key
  tested_modules:
    - RM500U
    - EM05
dependencies:
  - bus:usb:controller
  - openwrt:hotplug:cellular
```

---

# 10. Evidence Rules

Tags should be backed by evidence.

Acceptable evidence:

```text
same file path in reference tree
same patch target in MTK feed
same content or small semantic diff
patch-id match
same compatible string
same device name
same board.d case
same U-Boot target
same kernel function or driver change
same upstream commit
same runtime behavior
```

Weak evidence:

```text
similar filename only
similar directory only
nearby commit date only
vendor naming convention only
```

Do not assign strong claims based only on weak evidence.

---

# 11. Common Mistakes

Do not tag a whole large file as one modification if it contains unrelated changes.

Do not use `mtk-inherited` only because the same file exists in an MTK tree.

Do not use `r4-pro-common` only because 8X and 4E edit the same file.

Do not use `filogic-common` when the similarity is only BPI vendor style.

Do not tag repository metadata deletion as hardware-relevant.

Do not infer upstream provenance from patch filename alone.

Do not turn origin/scope/migration_feature tags into migration decisions. Decisions belong to cluster analysis.

Do not use minimal change as the guiding principle. A smaller local diff is not better if it preserves the wrong abstraction or hides vendor hacks.
