# M05.03.b: BPI-R4 Pro 8X Combo-LAN Static RJ45/SFP1 Bring-Up

Commit: `93e15e5915e70d87f06aec3a811b732821019179`
Short commit: `93e15e5915`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-16

## Scope

This records the combo-lan static validation work after the WAN combo mux step.
The goal was to prove the MxL-backed combo-lan path before adding the
combo-lan runtime mux.

Two static modes were validated on the same physical combo-lan front-panel
area:

```text
RJ45 static validation:
host eno1 -> combo-lan RJ45 -> MxL port 13 -> br-lan

SFP1 static validation:
host eno2 -> SFP adapter -> combo-lan SFP1 -> MxL port 13 -> br-lan
```

The final work commit keeps combo-lan in the static SFP1 mode so that the SFP1
module-detect and link signals can be validated before writing the combo-lan
mux state machine.

## Implementation Summary

The final committed code changes are:

1. `02_network` now gives the 8X formal wired roles:

   ```text
   LAN: lan1 lan2 lan3 lan4 combo-lan lan5 fpc
   WAN: combo-wan
   ```

2. The 8X DTS patch names GMAC1 as `combo-wan`:

   ```dts
   &gmac1 {
       openwrt,netdev-name = "combo-wan";
       ...
   };
   ```

3. MxL switch port 13 is exposed as `combo-lan`.

4. The final static combo-lan endpoint is SFP1:

   ```dts
   port@13 {
       reg = <13>;
       label = "combo-lan";
       phy-mode = "10gbase-r";
       phy-connection-type = "10gbase-r";
       managed = "in-band-status";
       sfp = <&sfp1>;
       status = "okay";
   };
   ```

5. GPIO54 is forced to the SFP1 side for this static image:

   ```dts
   combo-lan-sfp1-mux-select-hog {
       gpio-hog;
       gpios = <54 GPIO_ACTIVE_HIGH>;
       output-low;
       line-name = "combo-lan-sfp1-mux-select";
   };
   ```

The AS21xxx PHY24 RJ45 path is intentionally not bound to `combo-lan` in the
final static SFP1 commit. It remains a later combo-lan mux input.

## Build And Image Verification

The static SFP1 image was rebuilt with the container helper and all available
cores:

```text
scripts/wrt-docker-build.sh 'make -j$(nproc) target/linux/clean V=s'
scripts/wrt-docker-build.sh 'make -j$(nproc) target/linux/prepare V=s'
scripts/wrt-docker-build.sh 'make -j$(nproc) defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc) V=s'
```

Validation after the build:

```text
git diff --check: clean
sha256sum -c sha256sums --ignore-missing: all generated 8X artifacts OK
```

The generated manifest included the required runtime pieces:

```text
aeonsemi-as21xxx-firmware
kmod-dsa-mxl862xx
kmod-phy-aeonsemi-as21xxx
kmod-sfp
```

The final DTB was decompiled and checked. It contained:

```text
combo-lan:
    phy-mode = "10gbase-r"
    phy-connection-type = "10gbase-r"
    managed = "in-band-status"
    sfp = <...>

combo-lan-sfp1-mux-select-hog:
    gpios = <0x36 0x00>
    output-low
```

No `phy-handle = <&phy24>` remained on the final `combo-lan` endpoint.

Generated 8X artifacts included:

```text
openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb
openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz
openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-initramfs-recovery.itb
```

## Router Test Setup Script

`scripts/router_test_setup.sh` was updated to match the formal interface names
used by the current images:

```text
network.wan.device='combo-wan'
old network.m05wan and network.mxwan entries are removed
the status summary includes combo-wan and combo-lan
```

This avoids the earlier firewall confusion caused by testing through a
temporary WAN interface name.

## Static RJ45 Validation

Before switching the final code to static SFP1, combo-lan was tested in a
static RJ45 configuration:

```text
host USB Ethernet -> router lan1 / br-lan / 192.168.8.1 for SSH
host eno1         -> combo-lan RJ45
```

The validated RJ45 mode used:

```text
MxL port 13 -> AS21xxx PHY24 -> combo-lan RJ45
phy-mode = "usxgmii"
```

Observed behavior:

```text
combo-lan@eth2: UP, LOWER_UP
combo-lan entered br-lan
host eno1 negotiated link
ICMP traffic over the combo-lan RJ45 side passed
```

This proved that the MxL port 13 and PHY24 RJ45 path can be brought up when the
port is statically bound to the copper PHY. That static RJ45 binding is not the
final state of commit `93e15e5915`; the final commit switches the same exposed
`combo-lan` interface to SFP1 for module-detect validation.

## Static SFP1 Functional Validation

Runtime setup for the final static SFP1 image:

```text
host USB Ethernet -> router lan1 / br-lan / 192.168.8.1 for SSH
host eno1         -> combo-lan RJ45, physically connected but not selected
host eno2         -> SFP adapter -> combo-lan SFP1
```

Baseline router state:

```text
combo-lan@eth2: UP, LOWER_UP
br-lan:         UP, LOWER_UP
combo-wan:      DOWN / NO-CARRIER / 192.168.9.1
```

`ethtool combo-lan` reported:

```text
Supported ports: [ FIBRE ]
Speed: 10000Mb/s
Duplex: Full
Port: FIBRE
Link detected: yes
```

`ethtool -m combo-lan` successfully read the SFP1 EEPROM and DDM data:

```text
Identifier: SFP
Transceiver type: 10G Ethernet: 10G Base-SR
Vendor name: XZSNET
Vendor PN: XZS-SFP10G-T
Vendor SN: CO2601241234
Date code: 260124
DDM temperature, voltage, TX power, and RX power were readable
```

Kernel and netifd logs showed the expected static SFP1 path:

```text
mxl862xx mdio-bus:10 combo-lan: configuring for inband/10gbase-r link mode
mxl862xx mdio-bus:10 combo-lan: Link is Up - 10Gbps/Full - flow control off
br-lan: port 5(combo-lan) entered forwarding state
netifd: Network device 'combo-lan' link is up
```

Data-plane tests used temporary router-side `/32` routes and addresses only for
test isolation. They were removed after the tests.

Observed data-plane result:

```text
router -> eno2 normal ICMP: 20/20, 0% loss
eno2 -> router normal ICMP: 20/20, 0% loss
router -> eno2 1472-byte payload: 10/10, 0% loss
eno2 -> router DF 1472-byte payload: 10/10, 0% loss
```

Counters after the tests remained clean:

```text
combo-lan RxBadBytes: 0
combo-lan MtuExceedDiscardPkts: 0
combo-lan TxAcmDroppedPkts: 0
host eno2 rx_errors: 0
host eno2 tx_errors: 0
host eno2 rx_crc_errors: 0
host eno2 tx_dropped: 0
```

A TCP SYN from host eno2 to a temporary router-side br-lan address returned
`Connection refused`, proving the TCP packet reached the router and a RST came
back over the SFP path. The target service was not bound to that temporary
address, so this was treated as a path-level TCP round-trip check rather than a
service test.

## SFP1 Hotplug Signal Validation

Only the SFP side was tested in this round. RJ45 fallback was intentionally not
part of the static SFP1 signal test.

### Baseline

Physical state:

```text
host eno2 -> SFP adapter -> combo-lan SFP1
```

Observed:

```text
combo-lan@eth2: UP, LOWER_UP
ethtool combo-lan: Link detected: yes
ethtool -m combo-lan: EEPROM/DDM readable
RX optical power: about -3.98 dBm
```

### Step 1: Remove Only The eno2 Cable

Physical action:

```text
Remove the cable between host eno2 and the already inserted SFP adapter.
Do not remove the SFP adapter/module from SFP1.
```

Observed signal:

```text
combo-lan@eth2: DOWN / NO-CARRIER
ethtool combo-lan: Link detected: no
ethtool -m combo-lan: still readable
RX optical power: about -40.00 dBm
mxl862xx ... combo-lan: Link is Down
br-lan: port 5(combo-lan) entered disabled state
netifd: Network device 'combo-lan' link is down
```

No `sfp sfp1: module removed` event occurred.

### Step 2: Reconnect The eno2 Cable

Observed signal:

```text
combo-lan@eth2: UP, LOWER_UP
ethtool combo-lan: Link detected: yes
ethtool -m combo-lan: still readable
mxl862xx ... combo-lan: Link is Up - 10Gbps/Full - flow control off
br-lan: port 5(combo-lan) entered forwarding state
netifd: Network device 'combo-lan' link is up
```

No new module insert/remove event occurred.

### Step 3: Remove The SFP Adapter/Module

Observed signal:

```text
combo-lan@eth2: DOWN / NO-CARRIER
ethtool combo-lan: Link detected: no
ethtool -m combo-lan: netlink error: No such device
mxl862xx ... combo-lan: Link is Down
sfp sfp1: module removed
```

This is distinct from a cable-only removal: `ethtool -m` fails and the SFP core
reports module removal.

### Step 4: Insert The SFP Module Without The eno2 Cable

Observed signal:

```text
sfp sfp1: module XZSNET XZS-SFP10G-T rev 02 sn CO2601241234 dc 260124
ethtool -m combo-lan: readable again
combo-lan@eth2: DOWN / NO-CARRIER
ethtool combo-lan: Link detected: no
RX optical power: about -40.00 dBm
```

This proves module present is independent from Ethernet link-up.

### Step 5: Reconnect The eno2 Cable With The Module Already Inserted

Observed signal:

```text
combo-lan@eth2: UP, LOWER_UP
ethtool combo-lan: Link detected: yes
RX optical power: about -3.98 dBm
```

The link flapped several times during training before settling:

```text
mxl862xx ... combo-lan: Link is Up - 10Gbps/Full - flow control off
mxl862xx ... combo-lan: Link is Down
mxl862xx ... combo-lan: Link is Up - 10Gbps/Full - flow control off
...
final state: up
```

No SFP module insert/remove event occurred during this cable-only recovery.

### Step 6: Remove The SFP Module Again

Observed signal:

```text
ethtool -m combo-lan: netlink error: No such device
sfp sfp1: module removed
combo-lan@eth2: DOWN / NO-CARRIER
```

### Step 7: Restore Module And Cable Together

Observed signal:

```text
sfp sfp1: module XZSNET XZS-SFP10G-T rev 02 sn CO2601241234 dc 260124
mxl862xx ... combo-lan: Link is Up - 10Gbps/Full - flow control off
br-lan: port 5(combo-lan) entered forwarding state
netifd: Network device 'combo-lan' link is up
```

There were several transient link up/down events during physical restoration,
but the final state was stable up:

```text
combo-lan@eth2: UP, LOWER_UP
ethtool combo-lan: Link detected: yes
ethtool -m combo-lan: EEPROM/DDM readable
```

## Signal Conclusions For Combo-LAN Mux

The static SFP1 test proves that the future combo-lan mux should use the SFP
module-present signal as the selection input, not the Ethernet link state.

The observed distinction was:

| Physical condition | SFP module present | `ethtool -m` | combo-lan link | SFP core event |
| --- | --- | --- | --- | --- |
| Cable removed, module inserted | yes | readable | down | none |
| Cable inserted, module inserted | yes | readable | up | none |
| Module removed | no | `No such device` | down | `sfp sfp1: module removed` |
| Module inserted without cable | yes | readable | down | `sfp sfp1: module ...` |

For mux policy this means:

```text
module present/absent: primary mux selection input
link up/down: secondary link state only
```

A present SFP module without link must still select the SFP side. Link flaps
while the module remains present must not cause RJ45 fallback.
