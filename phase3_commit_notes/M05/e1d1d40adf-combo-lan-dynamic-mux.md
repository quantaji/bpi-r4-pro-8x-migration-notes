# M05.03.c: BPI-R4 Pro 8X Dynamic Combo-LAN Mux

Commit: `e1d1d40adf`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Worktree commit message: `M05.03.c`
Date: 2026-06-16

## Scope

This records the combo-lan runtime mux work after the static combo-lan RJ45 and
SFP1 bring-up in `93e15e5915`.

The goal was to make the MxL-backed combo-lan port dynamically switch between:

```text
SFP selected:  MxL port 13 -> passive mux channel 0 -> SFP1 / 10gbase-r
RJ45 selected: MxL port 13 -> passive mux channel 1 -> AS21xxx PHY24 / usxgmii
```

The mux policy is the same high-level policy already validated for combo-wan:

```text
SFP MOD_DEF0 present = 1 -> select SFP channel
SFP MOD_DEF0 present = 0 -> select RJ45 channel
```

Link state is not the mux selection signal. A present SFP module owns the combo
lane even if the SFP Ethernet link is down.

## Worktree Changes

The commit changes two OpenWrt patch files:

| File | Purpose |
| --- | --- |
| `target/linux/generic/pending-6.12/760-21-DO-NOT-SUBMIT-net-dsa-mxl862xx-add-passive-mux-support.patch` | New MxL862xx DSA-side passive mux implementation for combo-lan. |
| `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | Switches `combo-lan` back to the RJ45 PHY24 default endpoint and adds a `mux-bus` description for SFP/RJ45 runtime switching. |

The new `760-21` patch creates and modifies these kernel files at build time:

```text
drivers/net/dsa/mxl862xx/Makefile
drivers/net/dsa/mxl862xx/mxl862xx-mux.c
drivers/net/dsa/mxl862xx/mxl862xx-mux.h
drivers/net/dsa/mxl862xx/mxl862xx.c
drivers/net/dsa/mxl862xx/mxl862xx.h
```

No kernel source files are committed directly outside the patch stack.

## Source And Reference Boundary

The new MxL mux code is not a direct copy of vendor code.

Reference inputs used:

1. Direct 8X topology evidence:

   ```text
   MxL combo-lan attach port: 13
   SFP1 module-detect GPIO:   GPIO69 / MOD_DEF0 / active-low at the pin
   Passive mux select GPIO:   GPIO54
   RJ45 PHY:                  AS21xxx PHY24
   SFP channel:               10gbase-r / managed in-band
   RJ45 channel:              usxgmii / phy-handle PHY24
   ```

2. Previously validated static behavior:

   ```text
   GPIO54 low  -> SFP1 side works
   PHY24/usxgmii -> combo-lan RJ45 works
   SFP1/10gbase-r -> combo-lan SFP works
   MOD_DEF0 detects module presence independently of link-up
   ```

3. The combo-wan `806-02` mux state-machine shape:

   ```text
   read SFP present
   choose desired channel
   stop active netdev path
   select channel GPIO
   reconnect phylink endpoint
   restart active path
   poll every 100 ms
   ```

4. Vendor / MTK behavior was used as implementation guidance for topology and
   policy, but the code is written against the current OpenWrt 25.12 / kernel
   6.12 MxL862xx DSA driver APIs.

The implementation intentionally does not introduce a shared C file between
combo-wan and combo-lan. The common part is the state-machine structure and
function naming style; the hardware-specific operations remain local to the
respective driver.

## Design Rules Followed

The combo-lan mux keeps the same logical function suffixes as the combo-wan mux
where the operations are equivalent:

```text
mxl_mux_read_sfp_present()
mxl_mux_choose_channel()
mxl_mux_is_running()
mxl_mux_stop()
mxl_mux_select_channel()
mxl_mux_start()
mxl_mux_switch_channel()
mxl_mux_poll()
mxl_mux_parse_channel()
mxl_mux_validate_channels()
mxl_mux_init_default()
```

The MxL-specific phylink lifetime helpers are split around the DSA constraints:

```text
mxl_mux_create_phylink()
mxl_mux_connect_phy()
mxl_mux_install_channel()
mxl_mux_apply_channel()
mxl_mux_restore_channel()
mxl_mux_rollback_channel()
```

The important design choice is two-stage create-before-destroy switching:

```text
1. Create the new phylink for the target channel first.
2. Stop the running DSA user port if it is up.
3. Under RTNL, disconnect the old PHY, select the mux GPIO, install the new
   phylink, and connect the new PHY.
4. Restart the DSA user port on the new phylink.
5. Destroy the old phylink only after the new path is installed and started.
6. If install/start fails, restore the old channel and old phylink.
```

This avoids the earlier runtime panic window where `combo-lan` could be observed
by a MediaTek device event while the DSA user port had no valid phylink.

## DTS Changes

The final DTS patch leaves `combo-lan` as the normal logical LAN interface but
sets its default endpoint to the RJ45 side:

```dts
port@13 {
    reg = <13>;
    label = "combo-lan";
    phy-mode = "usxgmii";
    phy-connection-type = "usxgmii";
    phy-handle = <&phy24>;
    status = "okay";
};
```

The runtime mux is described under the MxL switch node:

```dts
mux-bus {
    mxl_mux13: ds-mux@13 {
        compatible = "mxl862xx,ds-mux";
        reg = <13>;
        chan-sel-gpios = <&pio 54 GPIO_ACTIVE_HIGH>;
        mod-def0-gpios = <&pio 69 GPIO_ACTIVE_LOW>;
        sfp-present-channel = <0>;

        channel@0 {
            reg = <0>;
            phy-mode = "10gbase-r";
            phy-connection-type = "10gbase-r";
            managed = "in-band-status";
            sfp = <&sfp1>;
        };

        channel@1 {
            reg = <1>;
            phy-mode = "usxgmii";
            phy-connection-type = "usxgmii";
            phy-handle = <&phy24>;
        };
    };
};
```

The old static SFP GPIO hog is removed because channel selection is now owned by
the mux driver.

## Build And Image Verification

The combo-lan mux images were rebuilt with the project container helper using
all available cores. After the panic fix, the generated patched kernel source
was cleaned and the image was rebuilt again so the final image came only from
the patch stack.

The relevant checks were:

```text
container build helper with make -j$(nproc)
target/linux clean/prepare before final image rebuild
git diff --check on the worktree patches
image artifact verification after packaging
runtime DT and kernel behavior checked on the router
```

The runtime image contained the MxL mux code from `760-21` and the final DTS
state from `191`.

## Runtime Environment

The final dynamic combo-lan tests used:

```text
host USB Ethernet -> router lan1 / br-lan / 192.168.8.1 for SSH
host eno1         -> SFP adapter -> combo-lan SFP1
host eno2         -> combo-lan RJ45
```

The host network namespaces still carried the older temporary names:

```text
combo-rj45 netns -> physically eno1 / SFP side / 192.168.8.201
combo-sfp  netns -> physically eno2 / RJ45 side / 192.168.8.202
```

Because of the name mismatch, the physical wiring was treated as authoritative
during result interpretation.

## Static Runtime Checks

With SFP inserted and linked, the router selected the SFP channel:

```text
mxl862xx mdio-bus:10: Ethernet mux: MOD_DEF0 SFP present=1, desired channel 0
mxl862xx mdio-bus:10 combo-lan: configuring for inband/10gbase-r link mode
mxl862xx mdio-bus:10: Ethernet mux: switched channel 1 -> 0
mxl862xx mdio-bus:10 combo-lan: Link is Up - 10Gbps/Full - flow control off
```

`ethtool combo-lan` reported:

```text
Supported ports: [ FIBRE ]
Speed: 10000Mb/s
Duplex: Full
Port: FIBRE
Link detected: yes
```

Data-plane result:

```text
SFP side 192.168.8.201 <-> router 192.168.8.1: OK
RJ45 side 192.168.8.202 -> router 192.168.8.1: FAIL
```

With SFP removed and RJ45 connected, the router selected the RJ45 channel:

```text
sfp sfp1: module removed
mxl862xx mdio-bus:10: Ethernet mux: MOD_DEF0 SFP present=0, desired channel 1
mxl862xx mdio-bus:10 combo-lan: PHY [mdio-bus:18] driver [Aeonsemi AS21010PB1] (irq=POLL)
mxl862xx mdio-bus:10 combo-lan: configuring for phy/usxgmii link mode
mxl862xx mdio-bus:10: Ethernet mux: switched channel 0 -> 1
mxl862xx mdio-bus:10 combo-lan: Link is Up - 2.5Gbps/Full - flow control rx/tx
```

Data-plane result:

```text
RJ45 side 192.168.8.202 -> router 192.168.8.1: OK
SFP side 192.168.8.201 -> router 192.168.8.1: FAIL
```

## Dynamic Insert/Remove Checks

### Operation 9: RJ45 Active, Insert SFP With Cable Attached

Starting state:

```text
SFP removed
RJ45 selected and linked at 2.5G
```

Action:

```text
Insert the SFP adapter/module with the SFP-side cable attached.
```

Observed signal:

```text
mxl862xx mdio-bus:10: Ethernet mux: MOD_DEF0 SFP present=1, desired channel 0
br-lan: port 5(combo-lan) entered disabled state
mxl862xx mdio-bus:10 combo-lan: configuring for inband/10gbase-r link mode
mxl862xx mdio-bus:10: Ethernet mux: switched channel 1 -> 0
sfp sfp1: module XZSNET XZS-SFP10G-T ...
mxl862xx mdio-bus:10 combo-lan: Link is Up - 10Gbps/Full - flow control off
```

Result:

```text
No kernel panic
SFP data path OK
RJ45 data path disconnected as expected
```

### Step 10A: Remove Only The SFP-Side Cable

Action:

```text
Keep the SFP module inserted.
Remove only the SFP-side Ethernet cable.
```

Observed behavior:

```text
combo-lan link went down
MOD_DEF0 did not change
no mux channel switch occurred
```

Result:

```text
No kernel panic
This confirms link-down is not treated as a request to fall back to RJ45.
```

### Step 10B: Reconnect The SFP-Side Cable

Action:

```text
Reconnect the SFP-side Ethernet cable while the SFP module remains inserted.
```

Observed behavior:

```text
combo-lan link returned to 10G
MOD_DEF0 did not change
no mux channel switch occurred
```

Result:

```text
No kernel panic
SFP data path OK after link flap
```

### Remove SFP Module And Return To RJ45

Action:

```text
Remove the SFP adapter/module.
```

Observed signal:

```text
sfp sfp1: module removed
mxl862xx mdio-bus:10: Ethernet mux: MOD_DEF0 SFP present=0, desired channel 1
mxl862xx mdio-bus:10: Ethernet mux: switched channel 0 -> 1
mxl862xx mdio-bus:10 combo-lan: Link is Up - 2.5Gbps/Full - flow control rx/tx
```

Result:

```text
No kernel panic
RJ45 data path OK
```

### Operation 13: Repeat RJ45 Active -> SFP Insert

Operation 13 is the same state-machine transition as operation 9:

```text
SFP absent + RJ45 selected
    ->
SFP present + switch to SFP
```

The difference is only test history: operation 13 repeats the transition after
prior SFP link flaps, SFP removal, and RJ45 fallback.

Observed signal:

```text
mxl862xx mdio-bus:10: Ethernet mux: MOD_DEF0 SFP present=1, desired channel 0
br-lan: port 5(combo-lan) entered disabled state
mxl862xx mdio-bus:10 combo-lan: configuring for inband/10gbase-r link mode
mxl862xx mdio-bus:10: Ethernet mux: switched channel 1 -> 0
sfp sfp1: module XZSNET XZS-SFP10G-T ...
mxl862xx mdio-bus:10 combo-lan: Link is Up - 10Gbps/Full - flow control off
```

Control-plane result:

```text
router uptime continued past the transition
no Oops
no kernel panic
no mtk_device_event crash stack
```

Data-plane result:

```text
SFP side ping router:       4/4 OK
router ping SFP side:       4/4 OK
RJ45 side ping router:      0/4, expected because mux selected SFP
SFP -> router TCP payload:  32 MiB OK, about 0.67 s
router -> SFP TCP payload:  32 MiB OK, about 0.70 s
```

## Panic Regression Result

Before the create-before-destroy fix, old operation 9 / 13 logs showed the mux
entering the SFP-present transition and then panicking in this shape:

```text
mxl862xx mdio-bus:10: Ethernet mux: MOD_DEF0 SFP present=1, desired channel 0
mxl862xx mdio-bus:10 combo-lan: Link is Down
Unable to handle kernel read ...
phylink_ethtool_ksettings_get
dsa_user_get_link_ksettings
__ethtool_get_link_ksettings
mtk_device_event
Kernel panic - not syncing: Oops: Fatal exception
```

The final code avoids that failure mode by keeping a valid old phylink until a
new phylink has been created and installed, and by rolling back to the old
channel if the target channel cannot be installed or started.

The repeated `RJ45 -> SFP` transitions after the fix did not reproduce the old
panic. The log shows normal mux transitions and the data plane works after the
switch.

## Remaining Test Gap

The final image has not yet repeated one exact high-risk physical case:

```text
Start from RJ45 selected.
Insert an SFP module without connecting the SFP-side Ethernet cable.
Leave the SFP link down.
```

Older static testing proved that a no-cable SFP module is still detected by
MOD_DEF0 and has readable EEPROM/DDM data. The old panic logs also matched the
`present=1` plus `Link is Down` signal shape. The final mux fix has already
survived:

```text
present=1 RJ45 -> SFP transitions where link later came up
SFP link-down and link-up flaps while the SFP module remained present
SFP removal and RJ45 fallback
repeat RJ45 -> SFP transition after prior flaps/removal
```

The no-cable insertion case remains useful as a final regression test because
it combines channel switching with an SFP endpoint that stays down.
