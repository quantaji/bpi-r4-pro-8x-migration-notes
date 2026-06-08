# Diff File Analysis Guide

## 1. Purpose

This guide defines how an AI agent should analyze one changed file from an OpenWrt diffset.

The goal is to turn a changed file into one or more semantic modification records with:

```text
origin
scope
migration_feature
````

This guide does not decide final migration action. Final decisions belong to cluster-level analysis.

## 2. Available Source Trees

Reference source trees:

```text
reference-source-codes/
├── MTK/
│   ├── mtk-openwrt-feeds
│   ├── openwrt-21.02-mtk
│   ├── openwrt-24.10-mtk
│   └── openwrt-25.12-mtk
├── upstreams/
│   ├── linux
│   ├── linux-v6.6.104
│   ├── linux-v6.12.62
│   ├── linux-v6.12.87
│   ├── linux-v6.18
│   ├── mt76
│   ├── openwrt-24.10.0
│   ├── openwrt-25.12.4
│   ├── openwrt-main
│   └── u-boot
└── vendors/
    ├── BPI-R4Lite-OPENWRT-V24.10.0-Master-Devel
    ├── BPI-R4-MT76-OPENWRT-V21.02
    ├── BPI-R4PRO-4E-OPENWRT-V24.10.0-Master-Devel
    └── BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel
```

Available diffsets:

```text
analysis/diffsets/
├── 8x-vs-openwrt24-base
├── 8x-vs-mtk24-base
├── mtk24-vs-openwrt24-base
├── mtk25-vs-openwrt25-base
├── 4e-vs-mtk24-base
├── r4-vs-mtk21-base
├── mtk21-packages-patches-feeds
├── mtk24-packages-patches-feeds
└── mtk25-packages-patches-feeds
```

Primary diffset:

```text
analysis/diffsets/8x-vs-openwrt24-base
```

All first-pass analysis starts from this diffset.

Other diffsets are reference evidence, not primary analysis input.

## 3. Output Format

For each semantic modification, output one record.

Recommended columns:

```text
mod_id
file_path
status
unit_type
hunk_hint
short_description
origin
mtk_version
scope
migration_feature
deletion_reason
evidence
needs_lookup
notes
```

`deletion_reason` is only used for deleted files. Use `none` otherwise.

`migration_feature` may contain multiple comma-separated values.

Example:

```text
mod_id: filogic.mk::bpi-r4-pro-8x-device-entry
file_path: target/linux/mediatek/image/filogic.mk
status: M
unit_type: semantic-hunks
hunk_hint: BPI device definition block
short_description: modifies Filogic image recipe for BPI-R4 Pro 8X
origin: mtk-plus-bpi
mtk_version: mtk-24.10
scope: 8x-only
migration_feature: image:device-recipe,image:dts-selection,openwrt:package:device-packages
deletion_reason: none
evidence: 8x-vs-openwrt24-base primary diff; similar image structure in MTK24
needs_lookup: compare mtk25 filogic.mk during cluster analysis
notes: final rewrite decision belongs to image-recipe cluster
```

## 4. Top-Level Decision Tree

For each changed file:

```text
1. Read file status from name-status.tsv.
   Status may be A, M, D, R, C.

2. If status is D:
   Use the deletion flow.
   Usually one deleted file becomes one record.

3. If status is A or M:
   Use the modification/addition flow.
   Split into semantic modifications if the file contains multiple purposes.

4. If status is R or C:
   Treat as rename/copy plus modification.
   Analyze old path, new path, and content delta.

5. Assign origin and scope for each semantic modification.

6. Assign migration_feature for each semantic modification.

7. Record evidence and unresolved lookup needs.
```

## 5. Deletion Flow

A deletion means:

```text
OLD tree has this file.
NEW tree does not.
```

Do not automatically interpret deletion as intentional hardware behavior.

For the primary diff:

```text
OLD = OpenWrt 24.10 upstream
NEW = BPI-R4 Pro 8X vendor
```

So a deleted file means OpenWrt had it, vendor tree does not.

For `8x-vs-mtk24-base`:

```text
OLD = openwrt-24.10-mtk
NEW = BPI-R4 Pro 8X vendor
```

So a deleted file means MTK24 applied tree had it, vendor tree does not.

This is evidence of absence, not proof of intentional removal.

## 5.1 Deletion Reasons

Use `deletion_reason` as an auxiliary field.

Allowed values:

```text
none
repo-metadata-pruned
build-artifact-pruned
external-feed-pruned
baseline-mismatch
vendor-tree-trimmed
package-stack-divergence
wireless-stack-divergence
replaced-elsewhere
obsolete-upstream-file
intentional-disable
high-risk-removed-support
unknown
```

### `repo-metadata-pruned`

Use for deleted repository metadata.

Examples:

```text
.github/*
.devcontainer/*
.gitattributes
.gitignore
README-only housekeeping
```

Typical tags:

```text
origin = build-noise
scope = build-only
migration_feature = source:tree:metadata
```

Usually stop after this.

### `build-artifact-pruned`

Use for deleted generated files, temporary files, build products, caches.

Examples:

```text
bin/
build_dir/
staging_dir/
tmp/
logs/
dl/
```

Typical tags:

```text
origin = build-noise
scope = build-only
migration_feature = source:tree:cleanup
```

Usually stop after this.

### `external-feed-pruned`

Use when deleted files belong to external feed checkouts, not OpenWrt base tree.

Examples:

```text
feeds/packages/*
feeds/routing/*
feeds/luci/*
```

Usually exclude from base-tree analysis.

### `baseline-mismatch`

Use when deletion is likely caused by comparing against a different source commit rather than vendor intent.

Evidence:

```text
file exists in one upstream snapshot but not another
diff includes many unrelated targets
deleted file unrelated to BPI-R4 Pro 8X
same deletion pattern appears across unrelated packages or targets
```

Typical notes:

```text
Do not infer hardware behavior from this deletion.
```

### `vendor-tree-trimmed`

Use when the vendor source tree appears to omit upstream files to reduce repository size or keep only build-relevant pieces.

Evidence:

```text
many deleted upstream patch/source files
deletions concentrated in package stacks not relevant to BPI 8X
no replacement logic visible in vendor tree
```

### `package-stack-divergence`

Use when vendor tree differs from upstream package patch/source organization.

Examples:

```text
package/network/services/hostapd/patches/*
package/network/utils/iw/patches/*
package/network/services/dnsmasq/patches/*
```

This may affect runtime behavior, but often should be handled as one package-stack issue, not one file at a time.

### `wireless-stack-divergence`

Use for large deletions in wireless package stacks.

Examples:

```text
package/kernel/mac80211/patches/*
package/network/services/hostapd/patches/*
package/network/services/hostapd/src/*
package/network/utils/iw/patches/*
```

Typical tags:

```text
origin = openwrt-upstream
scope = openwrt-generic or build-only
migration_feature = wireless:mac80211:patch or wireless:hostapd:build
```

Do not deep-read every deleted wireless patch unless a cluster depends on it.

### `replaced-elsewhere`

Use when the deleted file appears replaced by another file, newer source layout, different package, or different patch stack.

Evidence:

```text
same logic appears in another path
same package changed from source-in-tree to downloaded source
same driver patch exists under another directory or version
```

### `obsolete-upstream-file`

Use when the deleted file is obsolete in 25.12 or newer upstream.

Evidence:

```text
file absent in OpenWrt 25.12
function replaced by newer upstream implementation
patch already merged into upstream source
```

### `intentional-disable`

Use only when there is evidence the vendor intentionally disabled functionality.

Evidence:

```text
Makefile removes package
config explicitly disables feature
comment says disabled
board logic excludes feature
```

Do not infer this from deletion alone.

### `high-risk-removed-support`

Use for deleted files that may affect 8X hardware support.

High-risk deletion paths:

```text
target/linux/mediatek/*
package/boot/*
package/kernel/mt76/*
package/firmware/*
package/network/config/wifi-scripts/*
package/network/services/hostapd/Makefile
package/network/services/hostapd/files/*
package/kernel/linux/modules/*
scripts/mkits.sh
include/image-commands.mk
```

High-risk deletion requires lookup or cluster attention.

### `unknown`

Use when the deletion reason is unclear.

Record what was checked.

## 5.2 Deletion Decision Tree

```text
D1. Is the deleted path repository metadata?
    yes -> deletion_reason=repo-metadata-pruned
           origin=build-noise
           scope=build-only
           feature=source:tree:metadata
           stop.

D2. Is it generated/build/cache/download output?
    yes -> deletion_reason=build-artifact-pruned
           origin=build-noise
           scope=build-only
           feature=source:tree:cleanup
           stop.

D3. Is it inside external feeds/?
    yes -> deletion_reason=external-feed-pruned
           origin=build-noise
           scope=build-only
           feature=source:feeds:external-feed-config
           stop unless specifically requested.

D4. Is it a large package/wireless patch-stack deletion?
    yes -> deletion_reason=wireless-stack-divergence or package-stack-divergence
           create one deletion record per file, but do not deep-read each file.
           group later under wireless/package stack cluster.

D5. Is it in a high-risk path?
    yes -> deletion_reason=high-risk-removed-support or unknown
           assign feature based on path.
           inspect same path in OpenWrt 25.12, MTK24, MTK25, and relevant vendor trees.

D6. Does OpenWrt 25.12 also lack this file or has a replacement?
    yes -> deletion_reason=obsolete-upstream-file or replaced-elsewhere.

D7. Is there explicit evidence of disabling?
    yes -> deletion_reason=intentional-disable.

D8. Otherwise:
    deletion_reason=baseline-mismatch, vendor-tree-trimmed, or unknown.
```

## 6. Modification / Addition Flow

For status `M` or `A`, do not automatically tag the whole file as one unit.

Use the file as the dispatch unit, but produce semantic modification records.

## 6.1 When File-Level Tagging Is Enough

File-level tagging is acceptable when:

```text
file is small
file has one clear purpose
all hunks serve one function
deleted file is low-risk
Makefile change is a single package option
single DTS overlay with one purpose
```

## 6.2 When to Split Into Semantic Modifications

Split when a file contains multiple functions.

Must split these file types when they contain multiple hunks:

```text
target/linux/mediatek/image/filogic.mk
target/linux/mediatek/filogic/base-files/etc/board.d/02_network
target/linux/mediatek/filogic/base-files/lib/upgrade/platform.sh
package/boot/uboot-mediatek/Makefile
package/boot/uboot-envtools/files/mediatek_filogic
DTS/DTSI/DTSO files
kernel patch files touching multiple target files
kernel config files
wifi-scripts
hostapd Makefile/files
package/kernel/linux/modules/*.mk
```

## 6.3 Semantic Split Rules

Split by purpose, not by raw diff hunk.

Use one semantic modification for:

```text
one board case
one device definition
one DTS node group
one DTS overlay behavior
one U-Boot target
one image recipe block
one sysupgrade behavior
one network default behavior
one MAC/factory-data behavior
one kernel driver function
one kernel module definition
one package build option
one firmware inclusion
one userspace script behavior
```

Combine adjacent hunks if they serve the same purpose.

Split adjacent hunks if they serve different functions.

## 6.4 Kernel Patch File Rule

A `*.patch` file may contain more than one semantic change.

For kernel patches, split by:

```text
upstream commit subject if visible
target source file
driver subsystem
DTS binding vs driver logic
hardware function
```

Examples:

```text
one patch modifies both PHY driver and DTS binding
    -> split into network:phy:* and dts:* records

one patch modifies switch driver and OpenWrt module packaging
    -> split into network:switch:* and openwrt:package:* records
```

## 6.5 DTS Rule

DTS/DTSI/DTSO should be split by hardware node or behavior.

Examples:

```text
partition layout
nvmem cells
Ethernet MAC/PCS/PHY
SFP cage
GPIO mux
PCIe slot
USB hub
fan/thermal
LED/button
Wi-Fi slot
cellular slot/SIM
```

Do not treat an entire board DTS as one tag if multiple hardware areas are changed.

## 7. Origin Decision Tree

For each semantic modification:

```text
O1. Is it build/repo noise?
    yes -> origin=build-noise.

O2. Is the same or equivalent modification already in OpenWrt 25.12?
    yes -> origin=openwrt-upstream.
    Evidence must be semantic equivalence, not merely same path.

O3. Is the same/equivalent modification in OpenWrt main but not 25.12?
    yes -> origin=openwrt-main.

O4. Does MTK 24.10 feed or openwrt-24.10-mtk contain the same modification?
    yes:
      if vendor is materially same -> origin=mtk-inherited, mtk_version=mtk-24.10.
      if vendor adds BPI-specific behavior -> origin=mtk-plus-bpi, mtk_version=mtk-24.10.

O5. Does MTK 25.12 contain the closest version?
    yes:
      origin=mtk-inherited or mtk-plus-bpi as appropriate.
      mtk_version=mtk-25.12.
      note that this may be target-era reference, not vendor source.

O6. Does MTK 21.02 contain the closest version?
    yes -> origin=mtk-inherited or mtk-plus-bpi, mtk_version=mtk-21.02.
    Use mainly for old R4/MT76 history.

O7. Is it a Linux kernel backport?
    Check linux-v6.6.104, linux-v6.12.62, linux-v6.12.87, linux-v6.18, linux master.
    If found -> origin=linux-upstream-backport, mtk_version=none.

O8. Is it a U-Boot upstream backport?
    Check upstreams/u-boot.
    If found -> origin=uboot-upstream-backport, mtk_version=none.

O9. Is it mt76-specific and present in upstreams/mt76?
    yes -> origin=mt76-upstream-backport, mtk_version=none.

O10. Does it appear copied/adapted from another BPI board?
    Check 4E, R4, Lite.
    If yes -> origin=bpi-other-board.

O11. Is it only visible in BPI 8X vendor tree?
    yes -> origin=bpi-only.

O12. Otherwise -> origin=unknown.
```

## 8. Scope Decision Tree

For each semantic modification:

```text
S1. Is it build/repo noise only?
    yes -> scope=build-only.

S2. Is it generic OpenWrt behavior affecting many targets?
    yes -> scope=openwrt-generic.

S3. Is it explicitly BPI-R4 Pro 8X-specific?
    Evidence:
      8X device name/compatible
      8X image recipe
      8X port layout
      8X 10G SFP/RJ45 combo
      AS21010P or MxL86252 use specific to 8X
    yes -> scope=8x-only.

S4. Does the same semantic behavior appear in BPI-R4 Pro 4E?
    yes -> scope=r4-pro-common.
    Require semantic similarity, not only same file path.

S5. Does the same semantic behavior apply to MT7988 boards generally?
    Evidence:
      also in BPI-R4 or OpenWrt R4
      MT7988 Ethernet/PCS/PPE/WED/PCIe/SNAND/clock/pinctrl/thermal
    yes -> scope=mt7988-common.

S6. Does it apply across broader Filogic family?
    Evidence:
      similar logic across MT7981/MT7986/MT7987/MT7988
      generic Filogic image/storage/board.d/package/driver pattern
    yes -> scope=filogic-common.

S7. Is it only BPI vendor style shared across boards?
    Evidence:
      similar shell style
      similar packaging pattern
      similar habit of modifying RFB files
      no clear shared hardware behavior
    yes -> scope=bpi-style-common.

S8. Otherwise -> scope=unknown.
```

## 9. Migration Feature Assignment

Assign one or more `migration_feature` tags based on semantic purpose.

Use format:

```text
domain:subsystem:function
```

Do not bind too early to concrete 8X chips or ports. Concrete hardware binding belongs to cluster metadata.

Examples:

```text
network:phy:10gbase-t
network:combo:sfp-rj45
wireless:mt76:firmware
cellular:sim:interface
accel:ppe:flow-offload
```

## 9.1 Feature by Path Hints

Use path as a hint, not proof.

```text
package/boot/arm-trusted-firmware-mediatek/*
    boot:tf-a:build
    boot:tf-a:bl2
    boot:tf-a:fip

package/boot/uboot-mediatek/*
    boot:uboot:build
    boot:uboot:target
    boot:uboot:dts
    boot:uboot:defconfig
    boot:uboot:bootmenu
    boot:uboot:recovery
    boot:uboot:storage-layout

package/boot/uboot-envtools/*
    boot:uboot:env
    identity:uboot-env:ethaddr
    storage:sysupgrade:platform

target/linux/mediatek/image/*
    image:device-recipe
    image:dts-selection
    image:fit
    image:factory-image
    image:sysupgrade-image
    openwrt:package:device-packages

target/linux/mediatek/files-*/arch/*/boot/dts/*
    dts:*
    network:*
    storage:*
    bus:*
    thermal:*
    ui:*
    cellular:* if modem/SIM/WWAN slots are described

target/linux/mediatek/patches-*/*
    depends on patch content:
      dts:*
      network:*
      storage:*
      bus:*
      accel:*
      firmware:*

target/linux/mediatek/*/base-files/etc/board.d/02_network
    openwrt:board-d:network
    network:port-label:lan-wan
    network:default-config:bridge
    network:default-config:wan
    network:vlan:bridge
    identity:mac:ethernet

target/linux/mediatek/*/base-files/etc/board.d/01_leds
    openwrt:board-d:leds
    ui:led:power
    ui:led:network-port
    ui:led:wifi

target/linux/mediatek/*/base-files/lib/upgrade/platform.sh
    storage:sysupgrade:platform
    storage:sysupgrade:compatibility
    storage:sysupgrade:backup-restore

package/kernel/mt76/*
    wireless:mt76:driver
    wireless:mt76:firmware
    wireless:mt76:eeprom
    wireless:wed:runtime
    firmware:wifi:runtime
    firmware:wifi:eeprom

package/kernel/mac80211/*
    wireless:mac80211:patch
    wireless:regulatory:db

package/network/services/hostapd/*
    wireless:hostapd:build
    wireless:hostapd:ucode
    wireless:mlo:config

package/network/config/wifi-scripts/*
    wireless:wifi-scripts:netifd
    wireless:wifi-scripts:ucode
    wireless:mlo:runtime
    openwrt:hotplug:wifi

package/network/utils/uqmi/*
package/network/utils/umbim/*
modemmanager-related package paths
    cellular:userspace:uqmi
    cellular:userspace:umbim
    cellular:userspace:modemmanager
    cellular:network:wan-interface

package/kernel/linux/modules/*
    openwrt:package:kernel-modules
    plus hardware feature implied by module

package/firmware/*
    firmware:*
    plus matching hardware feature

scripts/mkits.sh
include/image-commands.mk
    image:fit
    image:sysupgrade-image
    build:scripts:helper
```

## 9.2 Core Migration Feature Set

Use these tags when applicable.

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

image:device-recipe
image:dts-selection
image:fit
image:factory-image
image:sysupgrade-image
image:device-packages

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

identity:mac:ethernet
identity:mac:wifi
identity:mac:wwan
identity:nvmem:factory
identity:uboot-env:ethaddr
identity:calibration:wifi
identity:calibration:phy

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

expansion:nvme:m2-mkey
expansion:nvme:power
expansion:nvme:pcie
expansion:minipcie:wifi
expansion:minipcie:cellular
expansion:m2-bkey:cellular

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

firmware:wifi:runtime
firmware:wifi:eeprom
firmware:phy:runtime
firmware:switch:runtime
firmware:wed:wo
firmware:cellular:modem
firmware:boot:blob
firmware:calibration:factory

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

## 10. Evidence Requirements

Each record must state evidence.

Good evidence:

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
nearby date only
vendor naming convention only
```

Do not assign strong claims from weak evidence.

## 11. Lookup Policy

Do not inspect every reference repo for every modification.

Use lookup only when needed.

```text
MTK lookup:
  use mtk-openwrt-feeds, mtk24-vs-openwrt24-base, 8x-vs-mtk24-base, mtk25-vs-openwrt25-base

R4 Pro common lookup:
  use 4e-vs-mtk24-base and 4E source tree

Old R4 / MT7988 lookup:
  use r4-vs-mtk21-base, R4 vendor tree, OpenWrt 25.12 R4 support

Upstream kernel lookup:
  use linux-v6.6.104, linux-v6.12.62, linux-v6.12.87, linux-v6.18, linux master

U-Boot lookup:
  use upstreams/u-boot

mt76 lookup:
  use upstreams/mt76

Feed package lookup:
  use mtk21/24/25-packages-patches-feeds when package-level evidence is needed
```

## 12. Common Mistakes

Do not analyze all diffsets equally.

Do not tag a large file as one modification if it contains unrelated changes.

Do not use `mtk-inherited` only because the same file exists in MTK.

Do not use `r4-pro-common` only because 8X and 4E edit the same file.

Do not use `filogic-common` when the similarity is only BPI vendor style.

Do not treat deletion as intentional removal without evidence.

Do not deeply analyze every mac80211/hostapd deleted patch unless a wireless cluster needs it.

Do not infer upstream provenance from patch filename alone.

Do not convert tags into migration decisions. Decisions belong to cluster analysis.

Do not use minimal change as the guiding principle. A smaller local diff is not better if it preserves the wrong abstraction or hides vendor hacks.



