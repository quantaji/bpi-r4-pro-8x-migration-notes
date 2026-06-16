# M05.03b: BPI-R4 Pro 8X Dynamic WAN Combo Mux

Commit: `e77a42256c5edc8496c4db5188f7a03a872cff2b`
Short commit: `e77a42256c`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-16

## Scope

M05.03b enables and validates the dynamic WAN RJ45/SFP2 combo mux for the
BPI-R4 Pro 8X.

The tested shared GMAC1 path is:

```text
RJ45 selected: MT7988 GMAC1 -> USXGMII PCS1/XFI TPHY1 -> AS21xxx PHY28 -> WAN RJ45
SFP selected:  MT7988 GMAC1 -> USXGMII PCS1/XFI TPHY1 in 10GBase-R mode -> WAN SFP2
```

The mux policy validated in this step is SFP-module-present priority:

```text
MOD_DEF0 present = 0 -> channel 0 / WAN RJ45
MOD_DEF0 present = 1 -> channel 1 / WAN SFP2
```

Link state is not the mux selection signal in M05.03b. A present SFP module
without an Ethernet link still owns the combo lane and does not fall back to
RJ45.

## Implementation Summary

The commit changes two patches:

| Patch | M05.03b change |
| --- | --- |
| `191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | Enable `ethernet-mux@1`, remove the static SFP GPIO hog from M05.03a, restore GMAC1's default path to RJ45/PHY28 USXGMII, and keep SFP2 as the channel 1 `10gbase-r` mux endpoint. |
| `806-02-net-ethernet-mtk_eth_soc-support-ethernet-passive-mux.patch` | Rewrite the passive mux glue into an explicit state-machine-shaped implementation with 100 ms MOD_DEF0 polling, desired/selected/active channel tracking, phylink reconnect on channel changes, rollback on failed switches, and diagnostic log lines for MOD_DEF0 and mux transitions. |

The main mux helper structure is intentionally local to `806-02`. It matches
the generic state-machine shape discussed for combo muxes, but it does not move
the logic into a shared C file.

Important helper names in the rewritten mux code:

```text
mtk_mux_read_sfp_present()
mtk_mux_choose_channel()
mtk_mux_is_running()
mtk_mux_stop()
mtk_mux_disconnect()
mtk_mux_select_channel()
mtk_mux_connect()
mtk_mux_start()
mtk_mux_apply_channel()
mtk_mux_rollback_channel()
mtk_mux_switch_channel()
mtk_mux_poll()
mtk_mux_parse_channel()
mtk_mux_validate_channels()
mtk_mux_init_default()
```

## Build And Image Verification

The image was rebuilt after the mux rewrite. The build used the container
helper and all available cores.

Validation performed before runtime testing:

```text
make target/linux/clean
make target/linux/prepare V=s
make defconfig
make -j$(nproc) V=s
sha256sum -c sha256sums --ignore-missing
```

The generated image manifest included both required runtime pieces:

```text
kmod-phy-aeonsemi-as21xxx
kmod-sfp
```

## Runtime Setup

The runtime test used two independent host NICs on the same test subnet:

```text
host eno1 -> router WAN RJ45
host eno2 -> SFP adapter -> router WAN SFP2
host USB Ethernet -> router lan1 / br-lan / 192.168.8.1 for SSH
```

Temporary host-side addresses:

```text
eno1: 192.168.9.2/24
eno2: 192.168.9.3/24
```

The router WAN test endpoint was configured as the normal OpenWrt `wan`
interface to avoid firewall confusion from the earlier temporary `m05wan`
name:

```text
network.wan.device='eth1'
network.wan.proto='static'
network.wan.ipaddr='192.168.9.1'
network.wan.netmask='255.255.255.0'
```

Because both host NICs were on `192.168.9.0/24`, data-plane checks used
interface-bound pings:

```text
ping -I eno1 192.168.9.1
ping -I eno2 192.168.9.1
```

The polling loop sampled:

```text
host eno1/eno2 link state
router eth1 link state
/sys/class/net/eth1/carrier
dmesg lines matching Ethernet mux, sfp2 module, eth1 Link, and MOD_DEF0
interface-bound ping through eno1 and eno2
```

## Dynamic Signal Test

### Baseline: SFP Removed, RJ45 Connected

Physical state:

```text
eno1 connected to WAN RJ45
SFP module removed
eno2 not connected to the router
```

Observed router signal:

```text
sfp sfp2: module removed
Ethernet mux: MOD_DEF0 SFP present=0, desired channel 0
Ethernet mux: switched channel 1 -> 0
mtk_soc_eth ... eth1: Link is Up - 10Gbps/Full - flow control rx/tx
```

Data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: OK
eno2/SFP  -> 192.168.9.1: FAIL
```

### Step 1: Insert SFP Module Without SFP Cable

Physical action:

```text
Insert the SFP adapter/module into WAN SFP2.
Do not connect eno2 to the SFP adapter yet.
Keep eno1 connected to WAN RJ45.
```

Observed router signal:

```text
Ethernet mux: MOD_DEF0 SFP present=1, desired channel 1
mtk_soc_eth ... eth1: Link is Down
Ethernet mux: switched channel 0 -> 1
sfp sfp2: module XZSNET XZS-SFP10G-T ...
```

Data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: FAIL
eno2/SFP  -> 192.168.9.1: FAIL
```

This proves the mux policy is SFP-present priority. The driver does not wait
for SFP link-up before switching away from RJ45.

### Step 2: Connect eno2 Cable To The Inserted SFP Module

Physical action:

```text
Connect eno2 to the already inserted SFP adapter.
Keep eno1 connected to WAN RJ45.
```

Observed router signal:

```text
mtk_soc_eth ... eth1: Link is Up - 10Gbps/Full - flow control off
```

The SFP copper module showed several expected link flaps before settling.
There was no new mux switch, because MOD_DEF0 did not change and the mux was
already on channel 1.

Final data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: FAIL
eno2/SFP  -> 192.168.9.1: OK
```

### Step 3: Remove Only The eno2 Cable

Physical action:

```text
Remove the eno2 cable from the SFP adapter.
Leave the SFP adapter inserted in WAN SFP2.
Keep eno1 connected to WAN RJ45.
```

Observed router signal:

```text
host eno2: DOWN / NO-CARRIER
router eth1: DOWN / NO-CARRIER
mtk_soc_eth ... eth1: Link is Down
```

No `MOD_DEF0` change and no `Ethernet mux: switched channel` line were
observed.

Data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: FAIL
eno2/SFP  -> 192.168.9.1: FAIL
```

This confirms that SFP cable link-down does not trigger RJ45 fallback while the
SFP module remains present.

### Step 4: Remove The SFP Module

Physical action:

```text
Remove the SFP adapter/module from WAN SFP2.
Keep eno1 connected to WAN RJ45.
```

Observed router signal:

```text
sfp sfp2: module removed
Ethernet mux: MOD_DEF0 SFP present=0, desired channel 0
Ethernet mux: switched channel 1 -> 0
mtk_soc_eth ... eth1: Link is Up - 10Gbps/Full - flow control rx/tx
```

Data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: OK
eno2/SFP  -> 192.168.9.1: FAIL
```

### Step 5: Reinsert SFP With eno2 Path Available

Physical action:

```text
Reconnect the eno2 path to the SFP adapter and insert the SFP adapter again.
Keep eno1 connected to WAN RJ45.
```

The exact physical operation may be split depending on the adapter/cable
mechanics. The relevant signal order observed in this run was module-present
first, followed by SFP link-up.

Observed router signal:

```text
Ethernet mux: MOD_DEF0 SFP present=1, desired channel 1
mtk_soc_eth ... eth1: Link is Down
Ethernet mux: switched channel 0 -> 1
sfp sfp2: module XZSNET XZS-SFP10G-T ...
mtk_soc_eth ... eth1: Link is Up - 10Gbps/Full - flow control off
```

The module again had a short link flap sequence:

```text
Link is Up
Link is Down
Link is Up
```

Final data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: FAIL
eno2/SFP  -> 192.168.9.1: OK
```

This confirms that a live RJ45 connection is preempted by SFP module presence.

### Step 6: Remove The SFP Path In Split Operations

The SFP adapter and eno2 cable could not always be removed as one physical
assembly. The final removal was therefore performed in split operations. That
is valid and useful because it covers both cases:

1. SFP cable/link removal while the module remains present.
2. SFP module removal, which changes MOD_DEF0.

Observed router signal for the module removal:

```text
mtk_soc_eth ... eth1: Link is Down
sfp sfp2: module removed
Ethernet mux: MOD_DEF0 SFP present=0, desired channel 0
Ethernet mux: switched channel 1 -> 0
mtk_soc_eth ... eth1: Link is Up - 10Gbps/Full - flow control rx/tx
```

Final stable data-plane result:

```text
eno1/RJ45 -> 192.168.9.1: OK
eno2/SFP  -> 192.168.9.1: FAIL
```

## Result

M05.03b is functionally complete.

The tested state transitions were:

| Transition | Trigger | Result |
| --- | --- | --- |
| RJ45 -> SFP | SFP MOD_DEF0 present becomes `1` | `switched channel 0 -> 1`, SFP owns the lane. |
| SFP -> RJ45 | SFP MOD_DEF0 present becomes `0` | `switched channel 1 -> 0`, RJ45 owns the lane. |
| SFP link down, module still present | eno2 cable removed from SFP adapter | No mux switch, no RJ45 fallback. |
| SFP link up, module already present | eno2 cable connected to SFP adapter | No mux switch, SFP data path comes up. |

The decisive 806-02 input is the logical MOD_DEF0/SFP-present signal. Runtime
testing showed that this signal is correctly captured by the mux polling path
and is sufficient to drive the intended M05.03b state machine.

If a future product policy wants RJ45 fallback when the SFP module is present
but has no link, that is a different mux policy. It is not the behavior
implemented or validated in M05.03b.
