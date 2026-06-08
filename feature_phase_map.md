# Feature To Phase Roadmap

This file maps Phase 1a feature-routing tags to the migration phases in `migration_roadmap.md`.

The map is an inspection index, not a migration decision. Each feature cluster still needs evidence review before code is migrated.

## Review Classes

`primary`: core feature for the phase.

`supporting`: may be needed by the phase but should not drive design alone.

`review-only`: inspect for applicability, deletion semantics, or provenance before migration.

`static-only`: represent static topology or package support, but runtime validation is not available with current hardware.

`deferred`: intentionally postponed until a later phase or until evidence is available.

## Mandatory Check For Every Feature

Every feature review must run the Unreported Minimalism Gate:

1. Did the proposed action choose the smallest local change without reading context?
2. Did it preserve vendor structure only because it was convenient?
3. Did it skip a relevant 8X vendor, vendor-family, MTK, or target OpenWrt file?
4. Did it silently leave current-phase behavior incomplete?
5. Did it pull in next-phase behavior without declaring the boundary?

If yes, the review must either reject the action or record why the minimal form is accepted, which evidence is missing, which phase owns the follow-up, and where the TODO is stored.

## Phase 00: Vendor Evidence And Polarity Gate

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `source:tree:metadata` | 26 | primary | Source metadata and repo-level noise. |
| `source:feeds:base-feed-config` | 1 | primary | Feed baseline review. |

Review-only:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `dts:soc:base` | 187 | review-only | Broad and noisy; do not use alone for design decisions. |
| `network:phy:generic` | 80 | review-only | Inspect only when tied to 8X network evidence. |
| `network:phy:multi-rate` | 123 | review-only | Large PHY cluster; split before migration. |
| `wireless:mac80211:patch` | 313 | review-only | Broad wireless patch bucket; inspect polarity and applicability first. |
| `wireless:hostapd:build` | 277 | review-only | Broad hostapd build bucket; split in Phase 07. |

## Phase 01: Clean Build And Image Skeleton

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `image:device-recipe` | 4 | primary | 8X profile and image recipe. |
| `image:dts-selection` | 4 | primary | DTS/DTSO selection. |
| `image:factory-image` | 4 | primary | Artifact generation only; install behavior belongs later. |
| `image:fit` | 2 | primary | FIT image handling for boot skeleton. |
| `openwrt:package:device-packages` | 26 | primary | Device package list. |
| `openwrt:package:kernel-modules` | 4 | primary | Kernel module package closure. |
| `boot:tf-a:build` | 14 | primary | Needed for boot artifacts. |
| `boot:uboot:build` | 2 | primary | U-Boot build integration. |
| `boot:uboot:target` | 2 | primary | U-Boot target selection. |
| `boot:uboot:dts` | 1 | primary | U-Boot board DTS. |
| `firmware:boot:blob` | 14 | primary | Boot firmware artifacts. |
| `build:package:makefile` | 19 | primary | Package build integration. |
| `build:tools:host-tool` | 29 | primary | Host tools required for image generation. |
| `build:scripts:helper` | 11 | supporting | Build helper scripts. |
| `build:kernel:config` | 5 | supporting | Kernel config fragments. |
| `build:toolchain:config` | 2 | review-only | Usually not board-specific; review before accepting. |

## Phase 02: SD Boot No Install

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `dts:overlay:storage` | 24 | primary | SD/eMMC/NAND overlays; only SD path is active in this phase. |
| `storage:partition:rootfs` | 5 | primary | Rootfs partition references for boot. |
| `boot:uboot:env` | 2 | primary | SD boot environment review. |
| `boot:uboot:bootmenu` | 1 | primary | Review menu actions, but do not use install entries. |
| `boot:uboot:recovery` | 1 | supporting | Only enough to understand SD recovery boot behavior. |
| `boot:recovery:failsafe` | 4 | supporting | Boot safety only; not factory install. |
| `identity:uboot-env:ethaddr` | 1 | supporting | Use only if needed for early boot identity. |

Deferred from this phase:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `boot:uboot:storage-layout` | 1 | deferred | Persistent install layout belongs to Phase 10. |
| `boot:recovery:factory-install` | 2 | deferred | Factory install belongs to Phase 10. |

## Phase 03: Board Identity, Power, I2C, GPIO, Factory Data

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `dts:board:base` | 62 | primary | Board-level DTS facts. |
| `dts:board:variant` | 52 | primary | 8X variant identity. |
| `dts:nvmem:factory-data` | 17 | primary | Factory data nodes. |
| `storage:factory-data:nvmem` | 17 | primary | Factory data storage source. |
| `identity:nvmem:factory` | 4 | primary | Factory identity source. |
| `identity:mac:ethernet` | 5 | primary | Ethernet MAC assignment. |
| `identity:calibration:phy` | 13 | primary | PHY calibration identity. |
| `dts:clock-reset:binding` | 17 | supporting | Review where board nodes depend on reset/clock bindings. |
| `dts:pinctrl:function` | 1 | supporting | Pinctrl ownership. |
| `bus:gpio:controller` | 1 | supporting | GPIO ownership and conflicts. |
| `bus:spi:controller` | 2 | supporting | SPI bus context before NAND install. |
| `bus:mdio:controller` | 1 | supporting | MDIO bus context before full wired phase. |

## Phase 04: Basic Wired Management

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `network:mac:mtk-eth` | 73 | primary | Ethernet MAC driver and integration. |
| `network:mdio:bus` | 19 | primary | MDIO bus behavior. |
| `openwrt:board-d:network` | 1 | primary | 8X LAN/WAN defaults. |
| `openwrt:network:defaults` | 9 | primary | Default network config. |
| `network:default-config:bridge` | 1 | primary | Bridge default. |
| `network:default-config:wan` | 1 | primary | WAN default. |
| `network:port-label:lan-wan` | 1 | primary | Port labels. |
| `network:vlan:bridge` | 1 | supporting | Basic bridge semantics only. |
| `openwrt:firewall:defaults` | 1 | supporting | Default policy, not hardware proof. |
| `openwrt:init:service` | 8 | supporting | Init behavior required for basic networking. |

## Phase 05: Full Wired Switch, SFP, And 10G

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `network:dsa:switch` | 29 | primary | DSA switch support. |
| `network:dsa:tagging` | 29 | primary | DSA tag protocol. |
| `network:switch:external-dsa` | 29 | primary | External DSA switch. |
| `network:switch:vlan-offload` | 14 | primary | Switch VLAN behavior before acceleration. |
| `network:phy:10gbase-t` | 29 | primary | 10G copper PHY behavior. |
| `network:phy:firmware` | 13 | primary | PHY runtime firmware. |
| `firmware:phy:runtime` | 21 | primary | PHY firmware packages/files. |
| `network:pcs:10gbase-r` | 9 | primary | 10GBase-R PCS. |
| `network:pcs:usxgmii` | 9 | primary | USXGMII PCS. |
| `network:sfp:cage` | 11 | primary | SFP cage definitions. |
| `network:sfp:i2c` | 11 | primary | SFP I2C path. |
| `network:sfp:module-detect` | 11 | primary | Module detect behavior. |
| `network:sfp:hotplug` | 6 | primary | Hotplug behavior. |
| `network:combo:gpio-mux` | 1 | primary | GPIO mux behavior. |
| `network:combo:runtime-switch` | 1 | primary | Runtime combo switch behavior. |
| `network:combo:sfp-rj45` | 1 | primary | SFP/RJ45 combo behavior. |
| `dts:overlay:network` | 30 | supporting | Network overlays; inspect against direct 8X topology. |

## Phase 06: Basic Wi-Fi Hardware

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `dts:overlay:wifi` | 6 | primary | Wi-Fi overlay. |
| `wireless:pcie:nic` | 6 | primary | PCIe Wi-Fi NIC. |
| `bus:pcie:controller` | 20 | primary | PCIe controller context. |
| `wireless:mt76:driver` | 128 | primary | mt76 driver changes; inspect for 8X applicability. |
| `wireless:mt76:firmware` | 34 | primary | Wi-Fi firmware. |
| `wireless:mt76:eeprom` | 34 | primary | mt76 EEPROM path. |
| `wireless:calibration:eeprom` | 34 | primary | Wi-Fi calibration EEPROM. |
| `identity:calibration:wifi` | 34 | primary | Wi-Fi calibration identity. |
| `firmware:wifi:eeprom` | 34 | primary | Wi-Fi EEPROM firmware/data handling. |
| `firmware:wifi:runtime` | 34 | primary | Runtime Wi-Fi firmware. |
| `openwrt:hotplug:wifi` | 7 | supporting | Hotplug needed for radio init. |

## Phase 07: Wireless Userspace, MLO, AFC, And Policy

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `wireless:hostapd:ucode` | 12 | primary | hostapd ucode integration. |
| `wireless:wifi-scripts:netifd` | 7 | primary | netifd Wi-Fi scripts. |
| `wireless:wifi-scripts:ucode` | 7 | primary | Wi-Fi ucode scripts. |
| `wireless:mlo:config` | 117 | primary | MLO config behavior. |
| `wireless:mlo:runtime` | 124 | primary | MLO runtime behavior. |
| `wireless:regulatory:db` | 35 | primary | Regulatory behavior; high review burden. |
| `wireless:hostapd:build` | 277 | review-only | Split before migration; broad bucket. |
| `wireless:mac80211:patch` | 313 | review-only | Split before migration; broad bucket. |

## Phase 08: Acceleration And Offload

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `accel:ppe:flow-offload` | 28 | primary | PPE flow offload. |
| `accel:wed:wifi-offload` | 49 | primary | WED Wi-Fi offload. |
| `wireless:wed:runtime` | 35 | primary | Wireless WED runtime. |
| `firmware:wed:wo` | 35 | primary | WO firmware. |
| `accel:hnat:nat` | 6 | primary | HNAT NAT behavior. |
| `accel:hnat:routing` | 6 | primary | HNAT routing behavior. |
| `accel:flowtable:nft` | 2 | primary | nft flowtable. |
| `accel:tops:tunnel-offload` | 1 | primary | TOPS tunnel offload. |
| `accel:crypto:eip` | 3 | review-only | Only migrate if required and justified. |

## Phase 09: Board Extras And Expansion

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `dts:led:definition` | 7 | primary | LED definitions. |
| `dts:button:definition` | 5 | primary | Button definitions. |
| `ui:button:reset` | 5 | primary | Reset button behavior. |
| `ui:button:wps` | 5 | primary | WPS button behavior. |
| `dts:fan:pwm` | 3 | primary | Fan DTS. |
| `thermal:fan:pwm` | 3 | primary | Fan runtime behavior. |
| `dts:thermal:zone` | 2 | primary | Thermal zones. |
| `bus:usb:controller` | 17 | primary | USB controller behavior. |
| `dts:overlay:pcie` | 16 | supporting | PCIe overlays. |
| `dts:overlay:cellular` | 1 | static-only | Static topology only without module. |
| `cellular:slot:m2-bkey` | 1 | static-only | No 4G/5G module available. |
| `cellular:slot:minipcie` | 1 | static-only | No 4G/5G module available. |
| `cellular:sim:interface` | 1 | static-only | Static SIM wiring only. |
| `cellular:network:wan-interface` | 2 | static-only | Do not claim runtime validation. |
| `expansion:m2-bkey:cellular` | 1 | static-only | Static expansion mapping. |
| `expansion:minipcie:cellular` | 1 | static-only | Static expansion mapping. |

## Phase 10: Onboard Storage, Install, And Sysupgrade

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `storage:spi-nand:boot` | 3 | primary | SPI-NAND boot support. |
| `storage:spi-nand:ubi` | 3 | primary | UBI layout. |
| `storage:spi-nor:boot` | 2 | review-only | Review before applying to 8X. |
| `dts:partition:layout` | 17 | primary | Persistent partition layout; SD rootfs-only handling is Phase 02. |
| `storage:sysupgrade:platform` | 4 | primary | Platform sysupgrade. |
| `storage:sysupgrade:backup-restore` | 1 | primary | Backup and restore behavior. |
| `storage:sysupgrade:compatibility` | 1 | primary | Compatibility checks. |
| `image:sysupgrade-image` | 6 | primary | Sysupgrade artifacts. |
| `boot:recovery:factory-install` | 2 | primary | Factory install behavior. |
| `boot:uboot:storage-layout` | 1 | primary | U-Boot persistent storage layout. |
| `boot:uboot:recovery` | 1 | primary | Recovery path after persistent storage work. |

## Phase 11: Release Validation

Primary:

| Feature tag | Count | Class | Notes |
| --- | ---: | --- | --- |
| `openwrt:base-files:board-detect` | 9 | primary | Board detect closure. |
| `openwrt:package:kernel-modules` | 4 | primary | Recheck package closure. |
| `image:factory-image` | 4 | primary | Recheck factory artifacts. |
| `image:sysupgrade-image` | 6 | primary | Recheck sysupgrade artifacts. |
| `openwrt:network:defaults` | 9 | primary | Recheck defaults after all phases. |
| `openwrt:init:service` | 8 | supporting | Service closure. |

## Cross-Phase Tags

These tags intentionally appear in more than one phase and must be resolved by evidence in the local cluster:

| Feature tag | Primary phases | Reason |
| --- | --- | --- |
| `dts:overlay:storage` | Phase 02, Phase 10 | SD boot early, NAND/eMMC install late. |
| `boot:uboot:recovery` | Phase 02, Phase 10 | SD safety early, persistent recovery late. |
| `image:factory-image` | Phase 01, Phase 11 | Build artifact early, release validation late. |
| `image:sysupgrade-image` | Phase 10, Phase 11 | Storage migration then final validation. |
| `openwrt:network:defaults` | Phase 04, Phase 11 | Basic management then final closure. |
| `openwrt:package:kernel-modules` | Phase 01, Phase 11 | Build closure then final package closure. |

## Tags Requiring Manual Split Before Migration

These feature tags are too broad to migrate as one unit:

1. `wireless:mac80211:patch`
2. `wireless:hostapd:build`
3. `dts:soc:base`
4. `network:phy:generic`
5. `network:phy:multi-rate`
6. `wireless:mt76:driver`

For each broad tag, split files by:

1. `A/M/D/R` polarity,
2. direct 8X evidence versus MTK-wide or upstream-wide behavior,
3. runtime necessity for the current phase,
4. risk of preserving vendor shortcuts.
