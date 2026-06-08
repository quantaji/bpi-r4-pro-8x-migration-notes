## Repository Map

Current local source workspace:

```text
./reference-source-codes
├── MTK
│   ├── mtk-openwrt-feeds
│   ├── openwrt-21.02-mtk
│   ├── openwrt-24.10-mtk
│   └── openwrt-25.12-mtk
├── upstreams
│   ├── linux
│   ├── linux-v6.12.62
│   ├── linux-v6.12.87
│   ├── linux-v6.18
│   ├── linux-v6.6.104
│   ├── mt76
│   ├── openwrt-24.10.0
│   ├── openwrt-25.12.4
│   ├── openwrt-main
│   └── u-boot
└── vendors
    ├── BPI-R4Lite-OPENWRT-V24.10.0-Master-Devel
    ├── BPI-R4-MT76-OPENWRT-V21.02
    ├── BPI-R4PRO-4E-OPENWRT-V24.10.0-Master-Devel
    └── BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel
```

### MTK Sources

#### `MTK/mtk-openwrt-feeds`

This is the raw MediaTek OpenWrt feed and SDK integration source.

It is not just a normal OpenWrt package feed. It contains feed packages, OpenWrt tree overlays, base patches, feed patches, build recipes, and commit mapping information.

Use this repo to answer:

```text
Did a vendor change come from MTK?
Which MTK release line did it come from?
Does MTK have a newer version of the same functionality?
Is a file from MTK feed overlay, MTK base patches, MTK feed patches, or MTK package sources?
```

Do not treat MTK feed code as final quality. It is a SoC vendor reference.

#### `MTK/openwrt-21.02-mtk`

This is an applied MTK OpenWrt 21.02 reference tree.

Use it only when a change appears to come from older MTK SDK history or when checking old BPI-R4 MT76 vendor code.

It is not a target baseline for BPI-R4 Pro 8X 25.12 migration.

#### `MTK/openwrt-24.10-mtk`

This is the applied MTK OpenWrt 24.10 SDK reference tree.

Use it to classify BPI-R4 Pro 8X vendor changes.

Primary questions:

```text
Is this 8X vendor change inherited from MTK 24.10?
Did BPI modify an MTK 24.10 file?
Is this behavior MTK platform support or BPI board-specific support?
```

This is one of the most important reference trees for Phase 1 tagging.

#### `MTK/openwrt-25.12-mtk`

This is the applied MTK OpenWrt 25.12 SDK reference tree.

Use it to determine whether MTK already has a 25.12-era implementation of a feature that appears in the 8X vendor 24.10 tree.

Primary questions:

```text
Does MTK 25.12 already replace this 24.10 implementation?
Should the 25.12 port use MTK 25.12 as reference instead of BPI 24.10?
Was a 24.10 MTK patch dropped, split, renamed, or redesigned in 25.12?
```

This repo is a target-era reference, not the final target structure.

### Upstream Sources

#### `upstreams/openwrt-24.10.0`

This is the OpenWrt 24.10 upstream baseline.

Use it as the baseline for the first BPI-R4 Pro 8X vendor diff.

Primary use:

```text
BPI-R4PRO-8X vendor tree
vs
OpenWrt 24.10 upstream
```

This diff defines the initial changed-file inventory.

#### `upstreams/openwrt-25.12.4`

This is the OpenWrt 25.12 target baseline.

Final implementation should be structured as a clean delta against this tree.

Use it to answer:

```text
Does OpenWrt 25.12 already support this function?
What is the correct 25.12 directory structure?
What should the final patch series be based on?
```

This is the target source of truth for OpenWrt structure.

#### `upstreams/openwrt-main`

This is the current OpenWrt main reference.

Use it only as a lookup source.

Primary questions:

```text
Has OpenWrt main already accepted a newer version of this feature?
Is there a newer R4, Filogic, MxL switch, PHY, SFP, DSA, or MT7988 implementation?
Did a relevant PR already land after 25.12.4?
```

Do not use OpenWrt main as the target baseline unless the project goal changes.

#### `upstreams/linux`

This is the main Linux repository clone used to manage Linux worktrees.

Do not use it as a full diff input.

Use it for provenance and worktree management.

#### `upstreams/linux-v6.6.104`

This is the Linux kernel reference corresponding to the MTK 24.10 / kernel 6.6.104 SDK line.

Use it when checking whether a vendor 24.10 kernel patch is already in the base 6.6 kernel or was added by MTK/BPI.

#### `upstreams/linux-v6.12.62`

This is the Linux kernel reference corresponding to the MTK 25.12 / kernel 6.12.62 SDK line.

Use it when comparing MTK 25.12 kernel patches against their underlying Linux baseline.

#### `upstreams/linux-v6.12.87`

This is the Linux kernel reference corresponding to the OpenWrt 25.12.4 target kernel level.

Use it to check whether a Linux-side feature is already present in the target kernel version, even if OpenWrt packaging or patch layout differs.

#### `upstreams/linux-v6.18`

This is a newer Linux reference used to check later upstream implementations.

Use it for:

```text
PHY
DSA
phylink
PCS
SFP
SFP/RJ45 combo abstractions
MxL switch
AS21xxx PHY
RSS/LRO
crypto acceleration
offload-related driver work
```

This is a provenance and future-direction reference. It is not the target kernel.

#### `upstreams/u-boot`

This is upstream U-Boot.

Use it to check whether U-Boot patches in `package/boot/uboot-mediatek` are upstream, MTK downstream, BPI-specific, or temporary hacks.

Do not use it for OpenWrt userland files.

#### `upstreams/mt76`

This is the upstream mt76 wireless driver repository.

Use it for Wi-Fi, WED, BE14/BE19, firmware loading, EEPROM/calibration, and mt76-related provenance checks.

Do not use it for Ethernet, boot chain, sysupgrade, or board.d logic.

### Vendor Sources

#### `vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel`

This is the primary vendor source for the target board.

Use it as the behavior source for BPI-R4 Pro 8X.

The first analysis pass starts from its diff against `upstreams/openwrt-24.10.0`.

This tree is not trusted as final structure. It may contain vendor hacks, large unreviewable patches, build noise, stale files, or code inherited from MTK SDK.

#### `vendors/BPI-R4PRO-4E-OPENWRT-V24.10.0-Master-Devel`

This is the main R4 Pro family reference.

Use it to determine whether an 8X change is specific to 8X or shared across R4 Pro variants.

Primary questions:

```text
Is this change R4 Pro common?
Should the final 25.12 design use a shared R4 Pro DTSI or shared script logic?
Which network, storage, LED, fan, PCIe, or sysupgrade behavior is common across 8X and 4E?
```

Do not copy 4E networking behavior into 8X without checking the actual hardware topology.

#### `vendors/BPI-R4-MT76-OPENWRT-V21.02`

This is an older BPI-R4 MT7988 vendor reference.

Use it cautiously.

It can help identify older MT7988, MT76, boot, Wi-Fi, or BPI vendor patterns, but it is based on an older OpenWrt line and should not be treated as a direct 25.12 migration source.

If OpenWrt 25.12 already contains a better R4 implementation, prefer the OpenWrt 25.12 version as the structural reference.

#### `vendors/BPI-R4Lite-OPENWRT-V24.10.0-Master-Devel`

This is a BPI R4 Lite vendor reference.

Use it mainly for BPI vendor style and common script patterns.

It may help classify:

```text
BPI board.d style
BPI sysupgrade style
BPI LED/button conventions
BPI modem or USB package choices
BPI default package choices
```

Do not use it to infer BPI-R4 Pro 8X Ethernet, 10G combo, AS21010P, MxL86252, or MT7988-specific behavior.
