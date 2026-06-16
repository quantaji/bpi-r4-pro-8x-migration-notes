# M05.03a: BPI-R4 Pro 8X Static WAN SFP2 Bring-Up

Commit: `09fb066f18a93aa8691e6dd0a282a7a5ba4bb9fc`
Short commit: `09fb066f18`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-16

## Scope

M05.03a is the static WAN SFP2 validation step. It proves that the BPI-R4 Pro
8X WAN SFP path can be brought up as a fixed SFP endpoint before the dynamic
SFP/RJ45 combo mux state machine is enabled.

The tested static path is:

```text
MT7988 GMAC1 -> USXGMII PCS1/XFI TPHY1 in 10GBase-R mode -> SFP2 cage
```

The runtime test endpoint remained the temporary interface:

```text
eth1 / m05wan / 192.168.9.1
```

This is not the final OpenWrt logical role naming. The final user-facing role
should become `combo-wan` after the dynamic mux work, not a bare hardware
endpoint name such as SFP2 or PHY28.

M05.03a intentionally disables the runtime mux node and forces the external
combo select GPIO to the SFP side. It does not claim dynamic switching between
WAN RJ45 and SFP2.

## Implementation Summary

The commit makes the smallest static SFP change needed for runtime proof:

1. Disable `ethernet-mux@1` for this test image.
2. Change `gmac1` from the AS21xxx PHY28 USXGMII RJ45 path to:

   ```dts
   phy-mode = "10gbase-r";
   phy-connection-type = "10gbase-r";
   managed = "in-band-status";
   sfp = <&sfp2>;
   ```

3. Add a GPIO hog for GPIO3:

   ```dts
   sfp2-mux-select-hog {
       gpio-hog;
       gpios = <3 GPIO_ACTIVE_HIGH>;
       output-high;
       line-name = "wan-sfp2-mux-select";
   };
   ```

4. Include `kmod-sfp` in the BPI-R4 Pro 8X image package list.

No extra kernel driver patch was needed for the static SFP proof. The existing
SFP core, MDIO-I2C support, MTK PCS behavior, and the current 8X DTS topology
were sufficient once the image included `kmod-sfp`.

## Build And Image Verification

Before building, the interrupted/old worktree build output was cleaned with:

```text
scripts/wrt-docker-build.sh 'make clean'
```

The image was built through the container helper with all available cores:

```text
scripts/wrt-docker-build.sh 'make -j$(nproc) V=s'
```

The first full build produced images but did not include `kmod-sfp` in the
final manifest because the local source-build `.config` still had
`CONFIG_PACKAGE_kmod-sfp` unset. After enabling the local build selection and
rerunning `make defconfig` plus the full-core build, the final image manifest
contained:

```text
kmod-phy-aeonsemi-as21xxx - 6.12.87-r1
kmod-sfp - 6.12.87-r1
```

The final kernel configuration contained:

```text
CONFIG_SFP=m
CONFIG_MDIO_I2C=m
CONFIG_DEBUG_FS=y
```

Final artifacts were generated under:

```text
bin/targets/mediatek/filogic/
```

with the tested 8X outputs:

```text
openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb
openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz
```

The generated board DTB was decompiled and checked. It contained:

1. `gmac1` as `10gbase-r` with `managed = "in-band-status"` and `sfp = <&sfp2>`.
2. `ethernet-mux@1` still present in the tree but with `status = "disabled"`.
3. `sfp2-mux-select-hog` driving GPIO3 high.

## Runtime Setup

The hardware was connected as:

```text
host USB Ethernet -> router lan1 / br-lan / 192.168.8.1
host eno2         -> SFP adapter -> router WAN SFP2 / eth1 / 192.168.9.1
```

SSH access was through the LAN side:

```text
ssh root@192.168.8.1
```

For data-plane testing only, the host network namespace was given a temporary
SFP-side IPv4 address:

```text
192.168.9.2/24 on eno2
```

This temporary address was removed after the test.

## Baseline Runtime Evidence

The loaded modules included:

```text
as21xxx
mdio_i2c
mxl862xx_dsa
sfp
```

`eth1` reported a 10G fiber link:

```text
Settings for eth1:
    Supported ports: [ FIBRE ]
    Supported link modes: 10000baseSR/Full
    Speed: 10000Mb/s
    Duplex: Full
    Port: FIBRE
    Link detected: yes
```

SFP2 debugfs reported:

```text
Module state: present
Device state: up
Main state: link_up
Signalling rate: 10313 kBd
moddef0: 1
rx_los: 0
tx_fault: 0
tx_disable: 0
```

The module EEPROM was readable through `ethtool -m eth1`. The tested module was:

```text
Identifier: SFP
Transceiver type: 10G Ethernet: 10G Base-SR
Vendor name: XZSNET
Vendor PN: XZS-SFP10G-T
Vendor SN: CO2601241234
Date code: 260124
```

GPIO debugfs showed the SFP2 and mux-select inputs:

```text
gpio-512 ( |tx-disable          ) out lo
gpio-513 ( |mod-def0            ) in  lo IRQ ACTIVE LOW
gpio-514 ( |los                 ) in  lo IRQ
gpio-515 ( |wan-sfp2-mux-select ) out hi
gpio-581 ( |mod-def0            ) in  hi IRQ ACTIVE LOW
```

For SFP2, raw `gpio-513` low plus `ACTIVE LOW` corresponds to the logical
gpiod value `1`, matching SFP core `moddef0: 1` and the value that the
806-02 mux code would read through `gpiod_get_value_cansleep()`.

## Firewall Boundary During Data-Plane Tests

Initial ICMP from host `eno2` to router `192.168.9.1` reached the router but was
rejected by firewall policy. This was not a link failure.

Evidence from host-side tcpdump:

```text
58:11:22:ab:7d:9c > a2:3d:96:32:45:a4:
    192.168.9.2 > 192.168.9.1: ICMP echo request
a2:3d:96:32:45:a4 > 58:11:22:ab:7d:9c:
    192.168.9.1 > 192.168.9.2: ICMP protocol 1 port unreachable
```

The temporary test interface is named `m05wan`, while the default firewall
`wan` zone only listed `wan` and `wan6`. Therefore `m05wan` fell through to the
default input `REJECT` behavior.

For data-plane confirmation only, a temporary non-persistent nft rule allowed
ICMP echo requests on `eth1`. With that temporary rule, SFP-side ping passed:

```text
5 packets transmitted, 5 received, 0% packet loss
rtt min/avg/max/mdev = 0.253/0.270/0.295/0.015 ms
```

The temporary nft rule was deleted after the tests.

## Signal Variation Test

The runtime signal test used a router-side polling loop that sampled:

1. `/sys/kernel/debug/gpio` for `mod-def0` and `wan-sfp2-mux-select`.
2. `/sys/kernel/debug/sfp2/state` for module state, main state, `moddef0`,
   `rx_los`, and `tx_disable`.
3. `/sys/class/net/eth1/carrier`, `/speed`, and `/duplex`.
4. `dmesg` link and module events.

The local notes helper `scripts/m05-03a-sfp-moddef0-probe.sh` is a reference
for interpreting MOD_DEF0 and mux channel selection. The actual runtime loop
used an inline `/tmp` probe on the router because the router BusyBox shell did
not provide a reliable 100 ms userspace sleep primitive.

### Signal Matrix

| Step | Physical action | MOD_DEF0 GPIO | SFP core state | Link signal | Conclusion |
| --- | --- | --- | --- | --- | --- |
| 1 | Baseline: SFP adapter and cable inserted | `gpio-513 in lo IRQ ACTIVE LOW` | `Module state: present`, `moddef0: 1`, `rx_los: 0` | `eth1 carrier=1`, `speed=10000`, `link_up` | Static SFP2 path is up at 10G. |
| 2 | Unplug cable, leave SFP adapter inserted | unchanged: raw low, logical present | `Module state: present`, then `Main state: wait_los`, `rx_los: 1` | `eth1 carrier=0`, `Link is Down` | Module presence and link loss are distinct. |
| 3 | Remove the SFP adapter | `gpio-513 in hi IRQ ACTIVE LOW` | `Module state: empty`, `moddef0: 0`, `tx_disable: 1` | carrier remains 0 | MOD_DEF0 presence input changes correctly. |
| 4 | Insert SFP adapter without cable | raw low, logical present | `Module state: present`, `moddef0: 1`, `rx_los: 1`, `Main state: wait_los` | carrier remains 0 | Module insertion is detected even without link. |
| 5 | Insert cable into already inserted adapter | raw low, logical present | `rx_los: 0`, `Main state: link_up` | final `eth1 carrier=1`, `10Gbps/Full` | Link restores from present/no-link state. |
| 6A | Remove cable, then remove SFP adapter | raw high after module removal | `Module state: empty`, `moddef0: 0` | carrier 0 | Full removal path repeats correctly. |
| 6B | Insert adapter and cable as a combined assembly | raw low after module insertion | `present`, brief `wait_los`, then `link_up` | final `eth1 carrier=1`, `10Gbps/Full` | Realistic combined insertion recovers to 10G. |

During steps 5 and 6B the 10G link flapped several times before settling:

```text
eth1: Link is Up - 10Gbps/Full - flow control off
eth1: Link is Down
eth1: Link is Up - 10Gbps/Full - flow control off
```

After the transient sequence, no new state changes appeared during the final
observation window and the final state was stable:

```text
Module state: present
Device state: up
Main state: link_up
moddef0: 1
rx_los: 0
tx_disable: 0
eth1 carrier=1
speed=10000
duplex=full
```

Final data-plane confirmation after step 6B:

```text
5 packets transmitted, 5 received, 0% packet loss
rtt min/avg/max/mdev = 0.199/0.290/0.434/0.077 ms
```

## 806-02 Mux Implications

In this M05.03a image, `ethernet-mux@1` is disabled. Therefore the 806-02 mux
code does not instantiate a runtime state machine and does not own GPIO3.

The disabled mux node still documents the future channel model:

```text
channel 0: PHY28 / RJ45 / usxgmii
channel 1: SFP2 / 10gbase-r / sfp2
sfp-present-channel = <1>
mod-def0-gpios = <&pio 1 GPIO_ACTIVE_LOW>
chan-sel-gpios = <&pio 3 GPIO_ACTIVE_HIGH>
```

The M05.03a runtime evidence validates the input polarity and signal diversity
needed by 806-02:

1. Raw MOD_DEF0 low with `GPIO_ACTIVE_LOW` maps to logical `sfp_present = 1`.
2. Raw MOD_DEF0 high maps to logical `sfp_present = 0`.
3. Cable removal changes `rx_los` and link state but does not change
   `sfp_present`.
4. GPIO3 high selects the SFP channel for the static test.

The 806-02 source uses a 100 ms delayed work loop:

```text
mod_delayed_work(system_wq, &mux->poll, msecs_to_jiffies(100));
```

It reads MOD_DEF0 with `gpiod_get_value_cansleep()`, so it will see the logical
active-low value, not the raw debugfs `hi`/`lo` text. That matches the observed
SFP core value and the M05.03a probe interpretation.

For M05.03b, dynamic mux logic should treat module presence as the mux-select
input and link/LOS as link health. The short 10G carrier flaps during cable or
combined insertion are normal recovery events and should not be treated as mux
presence transitions.

## Cleanup Performed

After runtime testing:

1. The temporary nft ICMP allow rule was removed.
2. The host temporary `192.168.9.2/24` address on `eno2` was removed.
3. The router temporary `/tmp/m05-03a-gpio-probe.sh` script was removed.
4. The router polling SSH session was stopped.

## Remaining Work

M05.03b should re-enable or replace the mux state machine and validate dynamic
switching between the RJ45 PHY28 channel and SFP2. That work needs to handle:

1. shared MOD_DEF0 ownership between SFP core and mux logic;
2. GPIO3 channel-select ownership;
3. phylink recreation or an equivalent upstream-style dynamic port model;
4. transient 10G link flaps after insertion without confusing them with module
   presence changes;
5. final OpenWrt role naming, likely `combo-wan`, rather than `eth1` or SFP2.
