# M03/M05 PHY Port Forward-Compatibility Boundary

Date: 2026-06-14

This note records the supervisor design decision after reviewing the direct 8X
vendor DTS, the current OpenWrt 25.12 worktree, the local upstream Linux
`phy_port` implementation, and the public netdev discussion.

It is a Phase 3 implementation guide, not runtime evidence. It does not change
the Phase 2 review matrix.

## Decision Summary

Do not backport Linux 7.0 `phy_port` into the 25.12 / Linux 6.12 target.

Prepare for future upstream support by splitting M03/M05 work into two classes:

1. Stable hardware-description work that should survive future upstream
   `phy_port`/MII-mux support with little or no change.
2. Temporary Linux 6.12 compatibility glue that implements real SFP/RJ45
   runtime switching now and is explicitly marked for deletion/replacement when
   upstream OpenWrt carries the final APIs.

This changes how M05 should structure the implementation, but it does not
change the M03 feature scope.

## Upstream Evidence

Local upstream Linux:

- `origin/linux-6.12.y` and `origin/linux-6.18.y` do not contain
  `drivers/net/phy/phy_port.c` or `include/linux/phy_port.h`.
- `origin/linux-7.0.y` contains:
  - `drivers/net/phy/phy_port.c`
  - `include/linux/phy_port.h`
  - `Documentation/networking/phy-port.rst`
  - `Documentation/devicetree/bindings/net/ethernet-connector.yaml`

Public netdev series:

- `https://lore.kernel.org/netdev/20260108080041.553250-1-maxime.chevallier@bootlin.com/`
- `https://lore.kernel.org/netdev/20260108080041.553250-2-maxime.chevallier@bootlin.com/`
- `https://lore.kernel.org/netdev/20260108080041.553250-4-maxime.chevallier@bootlin.com/`
- `https://lore.kernel.org/netdev/20260108080041.553250-15-maxime.chevallier@bootlin.com/`

The upstream design says the current phase only instantiates PHY-controlled
ports. Future work is expected for port state, netlink uAPI, raw MAC ports, and
MII muxing.

## Current Worktree Shape

Current 8X kernel DTS work is carried by:

`/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/worktrees/openwrt-bpi-r4-pro-8x/target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch`

The patch currently adds:

- `mt7988a-bananapi-bpi-r4-pro.dtsi`
- `mt7988a-bananapi-bpi-r4-pro-8x.dts`
- shared Pro SD/eMMC overlays
- Makefile DTB/DTBO entries

Later agents should edit this patch, or add a follow-up DTS patch if the change
is clearly outside M03. Do not copy direct vendor DTS files wholesale.

## M03 Implementation Plan

M03 is the board identity, power, I2C, GPIO, RTC, EEPROM, and Factory data
step. It must not implement wired/SFP/DSA/10G runtime behavior.

### Files To Modify

Primary file:

- `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch`

M03 may touch only the DTS/DTSI hunks in that patch, and only for board identity
and static board-service facts.

M03 should not modify these for wired/runtime policy:

- `target/linux/mediatek/image/filogic.mk`, except for packages strictly
  required by M03 board services.
- `target/linux/mediatek/filogic/base-files/etc/board.d/02_network`.
- kernel drivers under `drivers/net/`, `drivers/net/phy/`, or `drivers/net/dsa/`.
- MxL86252, AS21xxx, SFP, Wi-Fi, PCIe, USB, fan, install, sysupgrade, or
  storage-runtime package sets.

### Copy/Adapt Rules

Do not copy the vendor 8X base DTS as a file.

M03 should rewrite direct 8X hardware facts into the existing OpenWrt 25.12 /
R4 Pro DTS split:

- keep shared R4 Pro facts in `mt7988a-bananapi-bpi-r4-pro.dtsi`;
- keep 8X board identity in `mt7988a-bananapi-bpi-r4-pro-8x.dts`;
- use target 6.12 label names such as `serial0` and `xsphy`, not vendor 6.6
  names such as `uart0` or `xphy`;
- use direct 8X vendor evidence only for actual 8X hardware facts;
- use upstream/target R4 Pro structure as the style and label reference.

### Required M03 Features

M03 should implement or verify these static facts:

1. Board identity:
   - model and compatible for `bananapi,bpi-r4-pro-8x`;
   - retain target-era compatible hierarchy if already used by the skeleton.

2. RT5190A PMIC and CPU/CCI supply:
   - RT5190A at I2C0 address `0x64`;
   - `vin2`, `vin3`, `vin4` from `rt5190_buck1`;
   - CPU and CCI `proc-supply = <&rt5190_buck3>`.

   Final M03 decision: keep the target R4 Pro `buck4` and `ldo` values at
   1.8 V. The 8X schematic identifies these rails as `DVDD1V8_SOC` and
   `AVDD18`. The direct vendor 8X/4E `850000` / `1200000` values are treated
   as rail-mapping mistakes, not as hardware truth.

3. I2C mux and local board devices:
   - PCA9545 at I2C2 address `0x70`;
   - stable mux channel labels:
     - `imux0`
     - `imux1_sfp1`
     - `imux2_sfp2`
     - `imux3_wifi`
   - local channel devices:
     - PCF8563 at `0x51`, with a `pcf8563:` label;
     - AT24 24c02 at `0x57`;
     - PCA9555 at `0x20`.

   Final M03 decision: do not enable vendor `ina226@40`. The 8X schematic marks
   U13 as `NC\INA226AIDGSR`, R78 is a 0R jumper rather than a milliohm shunt,
   and both vendor 24.10 runtime and the first M03 25.12 runtime showed
   `ina2xx 3-0040` probe failure. Treat this as an optional footprint, not
   populated hardware. Do not add a disabled DTS node or `kmod-hwmon-ina2xx`.

4. GPIO keys and LEDs:
   - reset key on GPIO13;
   - WPS key on GPIO14;
   - red LED on PCA9555 GPIO15;
   - blue LED on PCA9555 GPIO14.

5. Factory partition and MAC evidence:
   - split SPI-NAND static partition geometry so Factory does not overlap UBI;
   - preserve `bl2` at `0x0` size `0x200000`;
   - add `factory: partition@200000`, label `Factory`, size `0x400000`;
   - record the direct 8X vendor MAC offset evidence:
     - `gmac2_mac` at `0xfffee`, size `0x6`;
     - `gmac1_mac` at `0xffffa`, size `0x6`;
     - `gmac0_mac` at `0xffff4`, size `0x6`;
   - move the plain UBI partition to `0x600000`, size `0xfa00000`.

   Gate: this is a controlled static partition-geometry correction, not M10
   storage policy. M03 must not import vendor UBI volumes, `ubootenv`,
   `ubootenv2`, `ubi_rootfs`, rootdisk nodes, bootargs, install logic, or
   sysupgrade semantics.

   Additional gate from the old 25.12 bring-up: the tested board's documented
   Factory MAC window was all `ff`, and the vendor image used random/local MAC
   assignment. Therefore M03 must not wire GMAC MAC consumers or claim MAC
   identity is solved. If fixed-layout MAC cells are added at all, treat them as
   unconsumed evidence nodes and hand the actual MAC policy to M04.

   Accepted implementation decision after checking committed M02 code: M02 only
   added the SD no-install rootdisk overlay and did not fix SPI-NAND Factory
   geometry. M03 should correct the static NAND geometry to `bl2` + `Factory`
   + `ubi`, but should not add `nvmem-cells` consumers under `gmac0`, `gmac1`,
   or `gmac2`.

6. RTC overlay semantics:
   - if the base DTSI already contains PCF8563, a separate RTC overlay is not
     required merely to match vendor file shape;
   - if an RTC overlay is kept, it must target the target-era `pcf8563` label;
   - M03 does not claim runtime RTC validation.

### M03 Must Not Do

M03 must not implement:

- SFP cages as runtime-ready;
- `mediatek,eth-mux`;
- `mxl862xx,ds-mux`;
- AS21xxx PHY runtime, firmware package closure, or link validation;
- MxL86252 switch/DSA/tag driver;
- board.d LAN/WAN defaults or interface MAC policy;
- Wi-Fi overlay/runtime, including GPIO4 `wifi_12v`;
- fan, USB, PCIe/NVMe, or thermal runtime behavior;
- eMMC/NAND install, rootdisk, persistent env, or sysupgrade.

If these nodes already exist from the M01 skeleton, M03 should avoid expanding
or validating them. M03 may adjust only direct conflicts that block its own
board-service facts.

## M05 Forward-Compatible Design

M05 owns full wired switch, SFP, 10G, AS21xxx, MxL86252, DSA, and combo-port
runtime behavior.

M05 must implement both combo ports. Fixed-one-side operation is not acceptable.
The selected rule is SFP priority unless the user later changes it.

### Stable M05 Hardware Description

These DTS facts should be written as hardware truth and should mostly survive a
future upstream `phy_port`/MII-mux migration:

- SFP1 cage:
  - I2C bus `imux1_sfp1`;
  - LOS GPIO70;
  - MODDEF0 GPIO69;
  - TX disable GPIO21;
  - power limit 3000 mW.
- SFP2 cage:
  - I2C bus `imux2_sfp2`;
  - LOS GPIO2;
  - MODDEF0 GPIO1;
  - TX disable GPIO0;
  - power limit 3000 mW.
- AS21xxx C45 PHYs:
  - `phy24` at MDIO address 24;
  - `phy28` at MDIO address 28;
  - reset GPIOs and reset timings from direct 8X DTS;
  - `firmware-name = "as21x1x_fw.bin"`.
- GMAC/PCS/DSA physical modes:
  - `10gbase-r` where the vendor DTS uses it;
  - `usxgmii` for the MxL CPU/user port paths where applicable.
- MxL86252 switch:
  - compatible, MDIO address, DSA member, CPU port, user-port labels, and
    `mxl862_8021q` tag protocol from direct 8X evidence.

### Optional Future Connector Nodes

The upstream `phy_port` series adds an `ethernet-connector.yaml` binding and
parses PHY-side connector descriptions under:

```dts
mdi {
        connector-0 {
                media = "BaseT";
                pairs = <4>;
        };
};
```

Plain-language meaning: this describes the front-panel RJ45 copper connector
behind a PHY as BaseT using four pairs.

This is not the full combo-port API and it does not implement switching.
It only records media-side connector facts that a future `phy_port`
implementation can read.

M05 may add these nodes under the AS21xxx copper PHYs only if target 6.12 DTS
validation tolerates them. If strict `dtbs_check` rejects them in the 6.12
target, defer them and record the hardware facts in the M05 note instead.

M03 must not add these nodes.

### Temporary Linux 6.12 Mux Glue

M05 may implement narrow compatibility glue for the current 6.12 target.
Every such patch must include a comment similar to:

```c
/*
 * Temporary BPI-R4 Pro 8X Linux 6.12 compatibility glue.
 * Replace with upstream MII-mux/phy_port/port-state support once available
 * in OpenWrt main. The hardware facts are kept in DTS; this code only
 * performs runtime switching for the pre-upstream API.
 */
```

Vendor rule and selected policy:

```c
new_channel = sfp_present ? sfp_present_channel : !sfp_present_channel;
```

This means SFP is preferred. No SFP module means fall back to the copper PHY
channel.

Direct 8X channel facts:

- SoC/GMAC mux:
  - compatible `mediatek,eth-mux`;
  - `chan-sel-gpios = <&pio 3 GPIO_ACTIVE_HIGH>`;
  - `mod-def0-gpios = <&pio 1 GPIO_ACTIVE_LOW>`;
  - `sfp-present-channel = <1>`;
  - channel 0 is `phy28`;
  - channel 1 is `sfp2`.
- MxL/DSA mux:
  - compatible `mxl862xx,ds-mux`;
  - `chan-sel-gpios = <&pio 54 GPIO_ACTIVE_HIGH>`;
  - `mod-def0-gpios = <&pio 69 GPIO_ACTIVE_LOW>`;
  - `sfp-present-channel = <0>`;
  - channel 0 is `sfp1`;
  - channel 1 is `phy24`.

### Expected M05 Functions/Logic

The exact target 6.12 APIs must be checked during implementation, but the
function-level design is now clear.

For the SoC GMAC side mux:

- define a small mux state structure with:
  - owning MAC pointer;
  - current channel;
  - `mod_def0_gpio`;
  - `chan_sel_gpio`;
  - `sfp_present_channel`;
  - two channel records containing OF node and phylink pointer;
  - delayed work for polling;
- add a `mtk_add_mux_channel()` equivalent:
  - parse `reg`;
  - parse `phy-mode`;
  - create a phylink for that channel;
  - store channel OF node and phylink pointer;
- add a `mtk_add_mux()` equivalent:
  - parse mux `reg`;
  - request `mod-def0` input GPIO;
  - request `chan-sel` output GPIO;
  - parse `sfp-present-channel`;
  - parse two child channels;
  - start delayed polling;
- add a polling/switch function:
  - read MODDEF0;
  - compute SFP-priority channel;
  - if unchanged or netdev down, reschedule;
  - take RTNL lock;
  - stop the netdev/MAC path;
  - swap the MAC OF node/phylink to the selected channel;
  - set the mux GPIO;
  - reopen/restart the netdev/MAC path;
  - release RTNL lock;
  - reschedule;
- add cleanup/release functions to cancel work, destroy phylinks, and put GPIOs.

For the MxL86252 DSA-side mux:

- define a DSA-port mux structure with:
  - owning DSA port;
  - current channel;
  - initialization flag;
  - `mod_def0_gpio`;
  - `chan_sel_gpio`;
  - `sfp_present_channel`;
  - two channel records containing OF node and phylink pointer;
  - delayed work for polling;
- add a `ds_add_mux_channel()` equivalent:
  - parse `reg`;
  - parse `phy-mode`;
  - create a phylink using the DSA port phylink config and MAC ops;
  - store channel OF node and phylink pointer;
- add a `ds_add_mux()` equivalent:
  - parse mux `reg` as the affected switch port;
  - request GPIOs;
  - parse `sfp-present-channel`;
  - set default channel to non-SFP until polling sees a module;
  - parse child channels;
  - start delayed polling;
- add an SFP monitor/switch function:
  - read MODDEF0;
  - compute SFP-priority channel;
  - if unchanged or netdev down, reschedule;
  - take RTNL lock;
  - `phylink_stop()` current port;
  - `phylink_disconnect_phy()`;
  - swap `dp->dn` and `dp->pl` to the selected channel;
  - `phylink_of_phy_connect()` for the selected channel;
  - `phylink_start()`;
  - set the mux GPIO;
  - release RTNL lock;
  - reschedule;
- add cleanup/release functions to cancel work, destroy phylinks, and put GPIOs.

The code amount should be modest, but it is not risk-free because it touches
phylink, netdev state, and DSA port state.

## Future Replacement Gate

When OpenWrt main carries upstream `phy_port` plus the needed MII mux or
port-state APIs:

1. Keep stable hardware DTS facts where they match the upstream binding.
2. Replace private `mediatek,eth-mux` and `mxl862xx,ds-mux` bindings with the
   upstream-approved mux/port representation.
3. Delete the polling/switching compatibility glue.
4. Reuse or adapt `mdi/connector` nodes only if they match the final binding.
5. Re-test both combo ports with SFP inserted and removed.

## Open Design Points

Current decisions:

- both combo ports must support runtime switching;
- SFP priority is selected and matches vendor behavior;
- `phy_port` itself is not backported;
- temporary mux glue is acceptable in M05 if clearly marked as replaceable.

Still implementation-gated:

- whether target 6.12 DTS validation accepts `mdi/connector` nodes;
- exact MxL86252 driver/tag import strategy against target 6.12 APIs;
- whether any direct 8X hardware evidence exists for AQR/CUX paths; current
  direct 8X evidence points to AS21xxx, not AQR;
- GPIO4 ownership conflict between MxL reset and Wi-Fi 12 V remains an
  M05/M06 coordination item.
