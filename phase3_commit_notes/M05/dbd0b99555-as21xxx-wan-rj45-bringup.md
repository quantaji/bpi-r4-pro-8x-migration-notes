# M05.02: BPI-R4 Pro 8X AS21xxx WAN RJ45 Bring-Up

Commit: `dbd0b99555f00acc8cff2d41ab53057de8208f23`
Short commit: `dbd0b99555`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-15

## Scope

This commit closes the M05.02 AS21xxx / WAN RJ45 base bring-up target for the
BPI-R4 Pro 8X.

M05.02 proves the GMAC1-side copper path:

```text
MT7988 GMAC1 -> USXGMII PCS1/XFI TPHY1 -> AS21xxx PHY28 -> WAN RJ45
```

The runtime-proven user-visible test endpoint is the temporary test interface:

```text
eth1 / m05wan / 192.168.9.1
```

This is not the final OpenWrt logical role naming. The final user-facing role
should become `combo-wan` after M05.03/M05.04, not a bare hardware endpoint
name such as SFP2 or PHY28.

This commit also describes `phy24` and includes combo mux scaffolding needed by
the next step, but it does not prove the MxL-side `combo-lan` path and it does
not prove SFP runtime switching.

## Source Aliases

- `OWMAIN`: OpenWrt main / newer OpenWrt patch stack used as the implementation
  direction for AS21xxx and MT7988 PCS behavior.
- `OW25`: current OpenWrt 25.12.4 target structure.
- `AIROHA`: OpenWrt Airoha target AS21xxx fixes that were not yet effective in
  the local Mediatek 6.12 target.
- `MTK25`: MTK 25.12 downstream feed used as supporting evidence for XFI TPHY
  ownership and passive mux behavior.
- `V8X`: direct BPI-R4 Pro 8X vendor topology evidence, especially PHY24/PHY28,
  SFP1/SFP2, and combo mux channel layout.
- `RUNTIME`: real BPI-R4 Pro 8X board validation through serial, SSH, ping,
  tcpdump, ethtool, sysfs counters, and ifdown/ifup cycling.

Old ImmortalWrt bring-up evidence was useful earlier for risk discovery, but
this M05.02 implementation is not copied from the old repo. The final code
path is based on OpenWrt/Linux-style drivers and explicit 8X topology.

## Hardware Naming Model

M05.02 keeps the three naming layers separate:

| Layer | Names used here |
| --- | --- |
| Hardware endpoint | WAN RJ45, SFP2, PHY28, GMAC1, USXGMII PCS1 |
| Kernel/netdev label | `eth1` for GMAC1 during this test image |
| OpenWrt logical role | future `combo-wan`, not finalized in this commit |

The same distinction remains for the next step:

| Layer | Names for future combo-lan |
| --- | --- |
| Hardware endpoint | LAN combo RJ45, SFP1, PHY24, MxL combo port |
| Kernel/netdev label | to be determined by the MxL DSA implementation |
| OpenWrt logical role | future `combo-lan` |

## Design Decisions

### Use The OpenWrt AS21xxx Driver Direction

The vendor package driver was not imported wholesale. The commit uses the
in-kernel AS21xxx driver direction and backports the missing AS21xxx fixes into
the local Mediatek 6.12 patch stack.

The AS21xxx patches are narrow:

- avoid firmware reset on PHY detach;
- fix link/autoneg corner cases;
- fix 2.5G/5G/10G speed reporting;
- force Clause 45 operations for autoneg;
- add the AS21xxx C45 read workaround already carried in newer OpenWrt target
  context.

This keeps the code closer to a future upstream/OpenWrt main adaptation than a
direct vendor package import would.

### Treat RJ45 As USXGMII, SFP As 10GBase-R

The decisive runtime change was to stop describing the WAN RJ45 copper channel
as `10gbase-r`.

The final DTS model is:

```text
combo-wan RJ45 channel 0: phy28, usxgmii
combo-wan SFP2  channel 1: sfp2, 10gbase-r
gmac1 initial path:        phy28, usxgmii
```

This is compatible with the future combo model: the two physical endpoints can
use different interface modes because the selected mux channel supplies the
phylink parameters. Only one endpoint is selected on the shared lane at a time.

### Let PCS Own XFI TPHY

The initial model left XFI TPHY ownership on GMAC nodes. That made the MAC and
PCS layers both relevant to the same SerDes resource and did not produce a
working RJ45 data path.

The commit moves XFI TPHY references to the PCS nodes and lets the MTK USXGMII
PCS driver reset, power, and set the PHY mode. The old MAC-owned `pextp`
control path is removed.

This aligns with the newer OpenWrt/main and MTK direction: the PCS is the layer
that knows whether the active lane should be USXGMII, 10GBase-R, or another
SerDes mode.

### Keep GMAC1 / GSW Boundaries Intact

The XGMAC force-mode / force-link split was backported, but the implementation
explicitly avoids treating the built-in GSW/lan5 path as an ordinary external
XGMAC link.

This mattered because an earlier too-broad adaptation broke `lan5`. The final
patch keeps the generic force-mode transitions away from the GMAC1-to-GSW path
and preserves the M04 `lan5/fpc` boundary.

### Mark Diagnostics As Temporary

Patch `807` is explicitly a temporary M05.02 diagnostic patch. It reads PCS and
XGMAC/XFI state and prints ratelimited log lines. It is not intended to be part
of final M05 closeout.

The diagnostics were useful for showing which interface mode and PCS branch the
system actually entered, but the final functional proof is from runtime traffic,
not from the debug lines.

## Files Changed

| File or patch | Source direction | Purpose | Final status |
| --- | --- | --- | --- |
| `target/linux/mediatek/image/filogic.mk` | `OW25` target packaging style | Add `kmod-phy-aeonsemi-as21xxx`; include `ethtool-full`, `tcpdump`, and `ip-full` for runtime diagnosis. | AS21 package is required; debug tools should be re-reviewed before final M05 closeout. |
| `190-arm64-dts-mediatek-mt7988a-move-xfi-tphys-to-pcs-nodes.patch` | `OWMAIN` + `MTK25` + `V8X` evidence | Move XFI TPHY references from GMAC nodes to PCS nodes. | Required with `808-01/808-02` for the working USXGMII path. |
| `191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | direct `V8X` topology plus target DTS style | Add AS21 PHY24/PHY28, LED names, hex unit-address cleanup, combo-wan mux node, and set GMAC1/RJ45 channel to `usxgmii`. | Required; PHY28 is runtime-proven, PHY24 is described but not yet link-proven. |
| `801-01` / `801-02` AS21 detach no-reset | `AIROHA` / newer OpenWrt AS21 stack | Prevent PHY detach from resetting firmware through GPIO reset. | Important for ifdown/ifup and future mux switching; retained. |
| `802-01` AS21 link/autoneg corner | `AIROHA` / newer OpenWrt AS21 stack | Avoid reporting link up while autoneg is still incomplete. | Correctness fix; retained. |
| `802-02` AS21 speed handling | `AIROHA` / newer OpenWrt AS21 stack | Read actual speed from AS21 vendor status register and parse pause separately. | Important for reliable 2.5G/5G/10G reporting; runtime showed 2.5G. |
| `802-03` AS21 C45 autoneg ops | `AIROHA` / newer OpenWrt AS21 stack | Force Clause 45 generic autoneg operations. | Important for high-speed autoneg; retained. |
| `804` AS21 C45 read workaround | `AIROHA` / newer OpenWrt AS21 stack | Work around unstable AS21 C45 reads. | Stability fix; retained. |
| `805` MTK XGMAC force-mode/link split | upstream Linux / `OWMAIN` direction, `MTK25` supporting evidence | Split force-mode and force-link bits and avoid old BIT(31) misinterpretation. | Retained with GMAC1/GSW boundary after an earlier broad version broke `lan5`. |
| `806-01` shared SFP mod-def0 GPIO | `MTK25` + `V8X` vendor evidence | Allow SFP and mux glue to share module-detect GPIO. | Not needed for RJ45-only proof; needed for M05.03 SFP priority. |
| `806-02` passive mux glue | `MTK25` + `V8X` vendor evidence, rewritten for local stack | Add temporary 6.12 GMAC-side passive mux glue. | Needed for future `combo-wan` switching; current proof used the RJ45 channel. |
| `807` temporary diagnostics | local diagnostic code | Print PCS/XGMAC state while isolating RX=0. | Must be removed or disabled before final M05 closeout. |
| `808-01` PCS manages XFI TPHY | `OWMAIN` / `MTK25` direction | Make USXGMII PCS power/reset/mode the XFI TPHY. | Required for final working path. |
| `808-02` drop MAC-owned pextp | `OWMAIN` / `MTK25` direction | Remove duplicate MAC-owned SerDes control. | Required with `190/808-01` to avoid ownership conflict. |

## Implementation Attempts And Results

### Attempt 1: AS21 DTS + Driver Binding

The first M05.02 step added AS21 PHY nodes and the AS21 driver package.

Result:

```text
Aeonsemi AS21010PB1 mdio-bus:18: Firmware Version: 1.9.1
Aeonsemi AS21010PB1 mdio-bus:1c: Firmware Version: 1.9.1
```

This proved that both PHY24 and PHY28 could be discovered and firmware-loaded.
It did not prove the data path.

Cleanups from this phase:

- DTS unit-address cleanup:
  - `reg = <24>` -> `ethernet-phy@18`;
  - `reg = <28>` -> `ethernet-phy@1c`.
- LED node names were made unique:
  - `as21xxx_phy24_led0@0`, `as21xxx_phy24_led1@1`;
  - `as21xxx_phy28_led0@0`, `as21xxx_phy28_led1@1`.

This avoided noisy LED name collision behavior and made the DTS more reviewable.

### Attempt 2: 10GBase-R RJ45 Model

Direct 8X evidence described a combo mux with PHY28 and SFP2. The early target
model kept the RJ45 path too close to a `10gbase-r` style description.

Result:

- PHY binding and firmware load worked.
- Link could come up at 2.5G.
- The data path was not reliable; earlier runtime checks showed the pattern
  that motivated the RX=0 investigation.

Conclusion:

For AS21 copper RJ45, the working OpenWrt/MTK-compatible path is USXGMII on the
GMAC/PCS side, not a fixed 10GBase-R copper description.

### Attempt 3: Passive Mux Bring-Up And GPIO Polarity

The GMAC-side passive mux glue was added for the future `combo-wan` runtime
switching model. Tests showed the mux node and GPIO ownership could come up,
but simply toggling or reasoning about mux state was not sufficient to explain
the missing receive path.

Result:

- The mux glue is useful and needed for M05.03.
- The RJ45 RX failure was not solved just by mux state handling.
- The next investigation needed to focus on PCS/SerDes ownership and interface
mode.

### Attempt 4: XGMAC Force Mode / Force Link

The MTK XGMAC status register had different force-mode and force-link bits in
newer code. A backport was added.

Pitfall:

An early broad version disturbed `lan5`, because it treated the GSW side like a
normal external XGMAC path. That was wrong for this board and violated the M04
`lan5/fpc` boundary.

Final adaptation:

- split `MTK_XGMAC_FORCE_MODE()` and `MTK_XGMAC_FORCE_LINK()`;
- keep the force-mode transition for the external XGMAC paths;
- keep GMAC1/GSW handling out of the generic path that broke `lan5`;
- preserve existing M04 management ports.

Result:

This patch remains useful and corrects the local 6.12 driver semantics, but it
was not by itself the final fix for the WAN RJ45 RX path.

### Attempt 5: Temporary Diagnostics

Patch `807` was added to print PCS and XGMAC state at link setup.

Useful diagnostic observations:

- GMAC1 entered `phy/usxgmii` only after the DTS and PCS changes;
- PCS link status was visible;
- eth1 XGMAC link-up happened with speed 2500/full once the final path was in
  place.

Pitfall:

Low-level diagnostics around MAC/PCS registers are easy to overuse. They must
remain temporary and should not be mistaken for a functional fix.

### Attempt 6: USXGMII RJ45 + PCS-Owned TPHY

The final working combination was:

1. describe WAN RJ45 channel 0 and `gmac1` as `usxgmii`;
2. keep SFP2 channel 1 as `10gbase-r`;
3. move XFI TPHY references to PCS nodes;
4. have the USXGMII PCS driver reset, power, and mode the XFI TPHY;
5. remove MAC-owned `pextp` handling;
6. keep AS21xxx C45/autoneg/read-status fixes.

Result:

The WAN RJ45 path became bidirectional and stable at 2.5G with no RX/TX errors.

## Runtime Validation

### Boot And Binding

The tested image booted and showed both AS21 PHYs:

```text
Aeonsemi AS21010PB1 mdio-bus:18: Firmware Version: 1.9.1
Aeonsemi AS21010PB1 mdio-bus:1c: Firmware Version: 1.9.1
```

The WAN RJ45 test path showed:

```text
mtk_soc_eth 15100000.ethernet eth1: PHY [mdio-bus:1c] driver [Aeonsemi AS21010PB1]
mtk_soc_eth 15100000.ethernet eth1: configuring for phy/usxgmii link mode
mtk_soc_eth 15100000.ethernet eth1: Link is Up - 2.5Gbps/Full - flow control rx/tx
```

### Temporary Network Setup

Runtime test setup used:

```text
br-lan / LAN management: 192.168.8.1
eth1 / m05wan test:      192.168.9.1
host eno2:               192.168.9.2
```

At first, host-to-router ping failed with:

```text
Destination Port Unreachable
```

This was not a link failure. `tcpdump` showed the router received ICMP echo
requests on `eth1` and returned ICMP unreachable. The cause was firewall policy:
the temporary interface `m05wan` was not in any firewall zone and default input
was `REJECT`.

Runtime-only fix:

```sh
uci add_list firewall.@zone[1].network='m05wan'
/etc/init.d/firewall reload
```

No `uci commit firewall` was used for this runtime proof.

### ICMP Matrix

Host to router:

```text
ping -I eno2 -c 20 -W 1 -s 1400 192.168.9.1
20 packets transmitted, 20 received, 0% packet loss
```

Router to host:

```text
ping -I eth1 -c 10 -W 1 -s 1400 192.168.9.2
10 packets transmitted, 10 packets received, 0% packet loss
```

Smaller packet sizes were also tested:

```text
56 bytes:   10/10
512 bytes:  10/10
1400 bytes: 10/10
```

### TCP Data Transfer

Router-to-host TCP transfer used BusyBox `nc` from the router and netcat on the
host.

Router sent:

```text
dd if=/dev/zero bs=1024 count=4096 | nc 192.168.9.2 5001
4096+0 records in
4096+0 records out
```

Host received:

```text
4194304 /tmp/m05_as21_router_to_host.bin
```

That proves more than ARP or small ICMP; it proves real TCP data over the AS21
WAN RJ45 path.

### Interface Restart Recovery

The test ran three `ifdown m05wan` / `ifup m05wan` style cycles. Each cycle
re-attached the PHY and relinked:

```text
eth1: configuring for phy/usxgmii link mode
eth1: Link is Up - 2.5Gbps/Full - flow control rx/tx
```

After relink, router-to-host ping recovered with 0% packet loss.

No persistent `-22`, `-110`, timeout, or phylink creation failure was seen in
the AS21/eth1 path after the final image.

### Final Link State

```text
Speed: 2500Mb/s
Duplex: Full
Auto-negotiation: on
Port: Twisted Pair
PHYAD: 28
Transceiver: external
Link detected: yes
```

Final eth1 counters:

```text
rx_packets=703
tx_packets=3317
rx_bytes=105164
tx_bytes=4457398
rx_errors=0
tx_errors=0
rx_dropped=0
tx_dropped=0
rx_crc_errors=0
rx_frame_errors=0
```

## What Actually Made It Work

The successful result was not caused by a single patch.

The required working set was:

1. AS21xxx driver and AS21 fixes;
2. PHY28 DTS and firmware-name wiring;
3. GMAC1 / WAN RJ45 described as `usxgmii`;
4. XFI TPHY moved to PCS nodes;
5. USXGMII PCS owns XFI TPHY reset/power/mode;
6. MAC-owned pextp handling removed;
7. XGMAC force-mode/link split kept in a GMAC-boundary-safe form;
8. runtime firewall zoning fixed for the temporary `m05wan` test interface.

The first seven are code/image requirements. The eighth is only test network
policy; it does not require a new image.

## Pits Avoided

### Do Not Treat SFP1/SFP2 As User-Facing Interface Names

SFP1/SFP2 are physical cages. PHY24/PHY28 are hardware PHY endpoints. The final
OpenWrt roles should be `combo-lan` and `combo-wan`.

M05.02 only proves the `combo-wan` RJ45 half through temporary `eth1/m05wan`.

### Do Not Copy The Vendor AS21 Package Wholesale

The vendor package includes many private debugfs/BBU and production-style
control paths. M05.02 did not copy them. The accepted path is to use the kernel
AS21 driver and add narrow fixes that can be reasoned about.

Useful vendor-only features such as logs, monitoring, WOL, EEE, downshift, and
firmware maintenance remain follow-up requirements, not M05.02 gates.

### Do Not Apply MTK XGMAC Changes Too Broadly

The force-mode/link backport is real, but applying it without respecting the
board's GMAC1/GSW boundary broke `lan5` in an earlier iteration. The final
patch is deliberately narrower.

### Do Not Diagnose Firewall Rejects As Link Failure

The initial ping failure after the data path was working looked like a network
failure from the host. Packet capture proved otherwise:

- echo-request reached `eth1`;
- router returned ICMP unreachable;
- adding `m05wan` to a firewall zone made ping pass.

This is a network-defaults/M05.04 issue, not an AS21 hardware issue.

### Do Not Keep 807 As Final Code

The diagnostic patch is useful during M05.02/M05.03 development but should not
remain in the final M05 closeout unless it is replaced by accepted diagnostics.

## Mainstream / OpenWrt Main Adaptation Plan

If this work is adapted toward OpenWrt main, the preferred path is:

1. Use the newest in-tree AS21xxx driver as the base.
2. Drop any AS21 patches already present upstream or in the target branch.
3. Keep only missing AS21 fixes as narrow, provenance-marked backports:
   - detach no-reset;
   - autoneg/link status;
   - speed read_status;
   - C45 autoneg;
   - C45 read workaround.
4. Use upstream/main MT7988 PCS/TPHY ownership if already available.
5. Put `phys = <&xfi_tphy*>` on PCS nodes, not GMAC nodes.
6. Describe RJ45 copper PHY channels as `usxgmii` when using AS21 over the
   MT7988 USXGMII PCS.
7. Keep SFP channel descriptions independent, e.g. `10gbase-r` with in-band
   status.
8. Replace private `mediatek,eth-mux` / `mxl862xx,ds-mux` glue with upstream
   `phy_port`, MII mux, or port-state style APIs once those are available.
9. Do not include temporary diagnostics or broad vendor debugfs interfaces in a
   PR.
10. Decide final OpenWrt network defaults in a separate commit, using logical
    roles (`combo-wan`, `combo-lan`) rather than hardware endpoint names.

For 25.12 backport maintenance, this commit is acceptable as a scoped migration
step, but for upstreaming it should be split into smaller PR-sized pieces:

- AS21 fixes already accepted or backported;
- MT7988 PCS/TPHY ownership;
- BPI-R4 Pro 8X DTS topology;
- optional temporary downstream combo mux glue kept out of upstream until an
  accepted API exists.

## Current Stage

M05.02 is functionally successful for the tested WAN RJ45 copper path:

- PHY28 binds as `Aeonsemi AS21010PB1`.
- Firmware load succeeds.
- GMAC1 enters `phy/usxgmii`.
- WAN RJ45 negotiates 2.5Gbps/full with the available host NIC.
- Bidirectional ICMP works after runtime firewall zoning.
- 1400-byte ping works both directions.
- Router-to-host TCP data transfer works.
- Three ifdown/ifup cycles recover.
- No AS21/eth1 `-22`, `-110`, timeout, RX drop, TX drop, CRC, or frame errors
  were seen after the final image.

## Not Claimed

This commit does not claim:

- PHY24 / `combo-lan` RJ45 data path success;
- SFP1 or SFP2 data path success;
- runtime RJ45/SFP switching success;
- final `combo-lan` / `combo-wan` OpenWrt default naming;
- 5G or 10G copper link success, because the available host negotiated 2.5G;
- AS21 optional features such as WOL, EEE, downshift, monitoring, logs, or
  firmware flash/update;
- hardware offload, Wi-Fi, storage, sysupgrade, or Factory repair.

## Recommended Next Step

M05.03 should not start with SFP switching first.

Recommended order:

1. bring up `combo-lan` RJ45 statically through PHY24 and the MxL DSA combo
   port;
2. validate the MxL port mapping and old firmware 1.0.70 behavior;
3. then implement runtime switching for `combo-wan`;
4. then implement runtime switching for `combo-lan`;
5. finally move temporary `m05wan`/test-network behavior into the M05.04 final
   OpenWrt logical defaults.

The reason is that `combo-wan` RJ45 is now proven, while `combo-lan` still has
an unproven MxL DSA-side path and is expected to be the higher-risk combo port.
