# M05.01: BPI-R4 Pro 8X MxL86252 DSA LAN Bring-Up

Commit: `02b17850876b9aa46dd8a45bea7a9effa340a9ca`
Short commit: `02b1785087`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-14

## Scope

This commit closes the M05.01 base MxL86252 bring-up target for the BPI-R4 Pro
8X.

M05.01 provides the external MxL86252 DSA switch stack, the image/package
wiring needed to load it, the 8X DTS description for the currently exposed MxL
LAN ports, old MxL firmware compatibility for the tested 1.0.70 board, and the
fresh-config OpenWrt LAN default that bridges `lan1` through `lan4` together
with the existing M04 `lan5` and `fpc` ports.

It does not claim AS21xxx 10G copper PHY bring-up, SFP cage support, combo
RJ45/SFP runtime switching, final `combo-lan` / `combo-wan` logical roles,
hardware acceleration validation, Wi-Fi, storage/install behavior, or raw
Factory repair.

## Source Aliases

- `OWMAIN`: OpenWrt main MxL862xx backport/pending patch stack used as the
  implementation base.
- `OW25`: OpenWrt 25.12.4 target structure and packaging style.
- `V8X`: direct 8X vendor topology evidence for hardware port wiring and old
  board behavior.
- `OLD25`: old ImmortalWrt 25.12 bring-up evidence used only to identify
  runtime risks, not copied as direct source.
- `RUNTIME`: real BPI-R4 Pro 8X serial and shell validation.
- `M04`: previous `lan5` / `fpc` management boundary, preserved by this
  commit.

## Design Decisions

### Use The OpenWrt Main MxL Stack

The MxL implementation is based on the OpenWrt main patch stack rather than the
direct vendor driver or the old ImmortalWrt downstream code. The commit imports
the MxL GPY/MxL86252 PHY support, MxL862xx DSA driver, native tag format,
802.1Q tagger, bridge/VLAN/FDB/MDB behavior, statistics, SerDes/phylink support,
devlink plumbing present in the selected stack, and related driver cleanups.

The 8X DTS uses the OpenWrt main tag protocol spelling:

```text
mxl862xx-8021q
```

instead of the vendor-only spelling used by older downstream code.

### Keep Naming Layers Separate

M05.01 exposes only the MxL LAN switch ports as kernel netdevs:

- `lan1`
- `lan2`
- `lan3`
- `lan4`

It preserves the M04 MT7988 GSW ports:

- `lan5`
- `fpc`

SFP1/SFP2 remain physical endpoints, not user-facing interface names. The
future combo roles must be expressed as logical OpenWrt roles such as
`combo-lan` and `combo-wan`, not as bare SFP cage names.

### Model Only The Proven M05.01 MxL Ports

The DTS models the MxL86252 switch at MDIO address `0x10`, exposes MxL ports
1-4 as `lan1` through `lan4`, keeps the currently unused MxL PHY4 path disabled,
and uses MxL port 9 as the fixed GMAC2 CPU port.

The CPU port is described as fixed `10gbase-r`. This matches the selected
OpenWrt-main style driver behavior for the tested board and avoids phylink
treating the fixed CPU link as an in-band USXGMII link.

### Preserve Old Firmware Support

The tested board runs old MxL firmware:

```text
firmware 1.0.70 (build 70)
```

M05.01 must support that firmware without asking the user to upgrade. The old
firmware path is kept explicitly version-gated instead of relying on new
firmware behavior.

## Problems Found And Fixes

### Old Firmware Triggered PHYLINK `-22`

The first MxL image loaded the switch firmware and internal PHYs but failed DSA
probe with:

```text
phylink: error: empty supported_interfaces
error creating PHYLINK: -22
```

Cause:

- old MxL firmware below 1.0.84 uses the legacy PCS path;
- the selected patch stack did not expose phylink interface capabilities for
  that legacy PCS path on the 8X CPU port;
- phylink rejected the port because `supported_interfaces` was empty.

Fix:

- keep old-firmware PCS selection limited to the known SerDes ports 9 and 13;
- expose legacy PCS capabilities for old firmware, including `10gbase-r` and
  the other legacy SerDes modes needed by the imported stack;
- keep the old-firmware command-timeout increase from the selected pending
  stack.

This is a downstream compatibility patch for the 8X old-firmware case. It is
not direct vendor code and should be re-reviewed when the MxL stack is rebased.

### Fixed USXGMII CPU Port Produced A PCS Warning

After the `-22` fix, the switch probed and linked, but the CPU port logged:

```text
firmware wants fixed mode, but PCS requires inband
```

Cause:

- the DTS used fixed-link with `phy-mode = "usxgmii"`;
- the legacy PCS path reports USXGMII as requiring in-band status;
- the 8X CPU link is intended to be a fixed 10G host link for this stage.

Fix:

- change the MxL CPU port to `phy-mode = "10gbase-r"` while keeping the
  fixed-link 10G description.

Runtime validation after this change shows the warning is gone.

### Fresh LAN Defaults Needed To Include MxL LAN Ports

The M04 default LAN bridge intentionally included only `lan5 fpc`. Once M05.01
proved `lan1-lan4` as real MxL DSA netdevs, the fresh-config LAN default needed
to include them.

Fix:

```text
lan1 lan2 lan3 lan4 lan5 fpc
```

This is a fresh configuration default. Existing `/etc/config/network` files on
already-booted systems still need firstboot or manual UCI adjustment.

## Files Changed

| File or directory | Action | Purpose |
|---|---|---|
| `target/linux/generic/backport-6.12/730-09*` through `730-11*` | `copy+adapt` from `OWMAIN` | GPY PHY fixes needed by the selected MxL stack. |
| `target/linux/generic/backport-6.12/760*` through `780*` | `copy+adapt` from `OWMAIN` | Base MxL862xx PHY, DSA, tagger, bridge/VLAN/statistics support. |
| `target/linux/generic/pending-6.12/760-01*` through `760-20*` | `copy+adapt` plus downstream old-firmware compatibility | SerDes, 802.1Q tagger, feature gating, LAG/mirror/devlink pieces present in the selected stack, and 8X old-firmware fixes. |
| `package/kernel/linux/modules/netdevices.mk` | `target-pattern-write` | Adds `kmod-dsa-mxl862xx`. |
| `target/linux/generic/config-6.12` | `target-pattern-write` | Adds MxL862xx DSA/tagger config symbols. |
| `target/linux/mediatek/image/filogic.mk` | `target-pattern-write` | Includes `kmod-dsa-mxl862xx` in the 8X image. |
| `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | `target-pattern-write` | Adds the MxL86252 switch node, ports `lan1-lan4`, disabled MxL-reserved port, and fixed `10gbase-r` CPU port. |
| `target/linux/mediatek/filogic/base-files/etc/board.d/02_network` | `target-pattern-write` | Adds `lan1-lan4` to the fresh LAN bridge defaults while preserving `lan5 fpc`. |
| `target/linux/mediatek/patches-6.12/732-net-phy-mxl-gpy-don-t-use-SGMII-AN-if-using-phylink.patch` | `delete` | Removes an obsolete local GPY patch superseded by the selected upstream-style stack. |

## Runtime Evidence

The final tested image booted on a board with MxL firmware 1.0.70 and showed:

```text
mxl862xx mdio-bus:10: switch ready after 2410ms, firmware 1.0.70 (build 70)
mxl862xx mdio-bus:10: configuring for fixed/10gbase-r link mode
mxl862xx mdio-bus:10: Link is Up - 10Gbps/Full - flow control off
mxl862xx mdio-bus:10 lan1 (uninitialized): PHY [mdio-bus:10-mii:00]
mxl862xx mdio-bus:10 lan2 (uninitialized): PHY [mdio-bus:10-mii:01]
mxl862xx mdio-bus:10 lan3 (uninitialized): PHY [mdio-bus:10-mii:02]
mxl862xx mdio-bus:10 lan4 (uninitialized): PHY [mdio-bus:10-mii:03]
```

The runtime check showed:

```text
OK: no PHYLINK create error
OK: no fixed/inband warning
OK: lan1-lan4 exist
```

Loaded modules:

```text
mxl862xx_dsa
tag_mxl862xx_8021q
```

With a cable connected to `lan3`, the board showed:

```text
lan3 state=up carrier=1 master=br-lan
mxl862xx mdio-bus:10 lan3: Link is Up - 2.5Gbps/Full - flow control rx/tx
```

The generated network default on the tested image included:

```text
network.@device[0].ports='lan1' 'lan2' 'lan3' 'lan4' 'lan5' 'fpc'
```

## Build And Check Evidence

The final image was built through the notes repo container wrapper:

```sh
scripts/wrt-docker-build.sh 'make -j$(nproc) V=s'
```

after a target clean used during patch-application iteration:

```sh
scripts/wrt-docker-build.sh 'make target/linux/clean'
```

The build completed successfully and produced:

```text
bin/targets/mediatek/filogic/openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz
```

Static patch checks passed before commit:

```sh
git diff --check
git diff --cached --check
```

## Current Stage

M05.01 is closed as base MxL86252 DSA/LAN bring-up:

- MxL driver and tagger are built into the image as a kmod package.
- MxL switch probe succeeds on old firmware 1.0.70.
- `lan1-lan4` are kernel netdevs backed by the MxL DSA switch.
- `lan1-lan4 lan5 fpc` are fresh-config OpenWrt LAN bridge ports.
- `lan3` was runtime-proven with carrier at 2.5Gbps while cabled.

## Deferred Work

M05.02 must handle AS21xxx 10G copper PHY behavior:

- firmware load timing;
- cold-boot readiness;
- C45 access;
- autoneg behavior;
- IPC and `mtk_open -22` class failures.

M05.03 must handle combo mux runtime switching:

- MxL-side `combo-lan` path, including the MxL port 13 old-firmware PCS path;
- GMAC1-side `combo-wan` path;
- SFP priority;
- temporary 6.12 mux glue that is clearly replaceable by future upstream
  `phy_port` / port-state style APIs.

Later M05 work must finish final logical roles and validation. Acceleration,
Wi-Fi, storage/install, sysupgrade, raw Factory writes, and firmware flashing
remain outside the M05.01 closure.
