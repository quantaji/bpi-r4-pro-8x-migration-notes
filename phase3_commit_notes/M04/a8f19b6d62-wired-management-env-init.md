# M04: BPI-R4 Pro 8X Wired Management And Firstboot Env Init

Commit: `a8f19b6d6282c2e755774d376a941fefede5a61f`
Short commit: `a8f19b6d62`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
GitHub: `quantaji/openwrt-bpi-r4-pro-8x-adaptation@a8f19b6d6282c2e755774d376a941fefede5a61f`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-14

## Scope

This commit closes the functional M04 bring-up target for BPI-R4 Pro 8X.

M04 provides a conservative wired management path and a persistent MAC identity
fallback. It does not claim final full wired topology, MxL86252 switch runtime,
SFP, combo RJ45/SFP switching, AS21xxx behavior, WAN policy, hardware offload,
Factory raw repair, onboard install, or release readiness.

## Source Aliases

- `OW25`: OpenWrt 25.12.4 filogic target structure.
- `V8X`: direct vendor 8X DTS and `02_network` evidence.
- `SCHEMATIC`: 8X schematic evidence used to confirm GSW port routing.
- `RUNTIME`: real BPI-R4 Pro 8X serial and shell validation.
- `M03`: preceding board-service and Factory partition implementation.
- `M05`: next full wired switch/SFP/10G owner.

## Design Decisions

### Conservative M04 Port Exposure

M04 exposes only the built-in MT7988 GSW management ports:

- `lan5`: ETH5, front-panel 1G RJ45 LAN, MT7988 GSW port 0.
- `fpc`: ETH8, 1G FPC LAN connector, MT7988 GSW port 3.

The earlier skeleton label `mgmt` was removed because it had no vendor,
schematic, or official board evidence. The 8X schematic and vendor DTS indicate
ordinary LAN-style use rather than a dedicated management-only port.

M04 intentionally does not expose the MxL86252 ports, SFP cages, combo ports, or
WAN defaults. Those need the M05 DSA/PHY/SFP runtime stack before they are
truthful OpenWrt defaults.

### MAC Source Policy

M04 uses this source order:

1. NAND `Factory` triplet only if all three vendor offsets are present, valid
   unicast MACs, and mutually unique.
2. Active U-Boot env `ethaddr`, `eth1addr`, `eth2addr` if the triplet is valid
   and unique.
3. Runtime `eth0` as a base, then derive `+1` and `+2`.

The tested board's Factory offsets were all `ff:ff:ff:ff:ff:ff`, so Factory is
valid as static geometry/evidence from M03 but not as a usable MAC source on
this board.

### U-Boot Env As First Persistent Target

Raw Factory writes are deliberately deferred. The first persistent M04 target is
the active U-Boot env because U-Boot can pass `ethaddr` into Linux early enough
for the kernel runtime MAC path to become stable before network defaults run.

The implementation writes all three variables as a triplet:

- `ethaddr`
- `eth1addr`
- `eth2addr`

This follows the vendor behavior of deriving a contiguous triplet from one base
MAC when no valid Factory triplet exists.

## Problems Found And Fixes

### Incomplete External Env Can Break Reboot

During testing, `fw_setenv` made an MMC U-Boot env valid even though it did not
contain the complete 8X SD boot environment. On reboot, U-Boot selected that
incomplete external env and dropped to a menu with only `Exit`.

Fix:

- replace the M01 skeleton defenvs with firstboot-capable SD, eMMC, and
  SPI-NAND environments;
- add an `Initialize environment` firstboot menu item;
- run `saveenv` during firstboot before normal boot;
- gate all Linux-side `fw_setenv` writes on a complete 8X boot env.

The SD path was validated on real hardware. The eMMC and SPI-NAND paths are
implemented now so the file does not need a structural rewrite later, but their
runtime validation remains an M10 storage/install task.

### `02_network` Env Guard Must Match Firstboot Shape

After firstboot, `bootmenu_0` becomes:

```text
Run default boot command.=run boot_default
```

and `boot_default` then calls `bootcmd` or recovery. The final tree therefore
checks `bootmenu_0` for `run boot_default` and checks `boot_default` for both
`run bootcmd` and `run boot_recovery`. This matches the uci-defaults script and
the manual provisioning tool.

### Factory Is Blank, Not A M04 Failure

Runtime repeatedly showed the vendor Factory offsets were blank. M04 treats
that as an input condition, not as a failed implementation. The fallback path
persists a stable U-Boot env triplet instead of attaching invalid nvmem cells to
GMACs.

### M04 Script Warnings

The early acceptance script warned that `network.lan.macaddr` was missing. That
was a script-level assumption, not a target failure. The actual generated config
sets device MAC state for the exposed ports and bridge behavior; final per-port
LAN/WAN MAC policy belongs to M05 when all ports exist.

## Files Changed

| File | Action | Purpose |
|---|---|---|
| `package/boot/uboot-mediatek/patches/469-add-bpi-r4-pro-8x.patch` | `target-pattern-write` | Adds firstboot-capable SD/eMMC/SPI-NAND defenvs for 8X. |
| `target/linux/mediatek/patches-6.12/191-arm64-dts-mediatek-add-bananapi-bpi-r4-pro-8x.patch` | `copy+adapt` / `target-pattern-write` | Renames GSW port 0 to `lan5`, enables GSW port 3 as `fpc`, keeps ports 1/2 disabled. |
| `target/linux/mediatek/filogic/base-files/etc/board.d/02_network` | `target-pattern-write` | Adds staged 8X LAN defaults `lan5 fpc`, MAC source order, and boot-env completeness gate. |
| `target/linux/mediatek/base-files/etc/uci-defaults/99_fwenv-store-ethaddr.sh` | `target-pattern-write` | Persists a complete 8X MAC triplet only when the active env is safe to write. |
| `target/linux/mediatek/filogic/base-files/usr/sbin/bpi-r4-pro-8x-mac-provision` | `target-pattern-write` | Keeps the manual provisioning tool aligned with the firstboot env guard. |

## Runtime Evidence

Fresh SD boot from a cleared card showed the intended firstboot behavior:

```text
Loading Environment from MMC... *** Warning - bad CRC, using default environment
*** Warning: MAC address is randomly set ...
bootmenu_0=Initialize environment.=run _firstboot
```

After firstboot, Linux showed a stable triplet:

```text
ethaddr=a2:33:c9:89:c2:67
eth1addr=a2:33:c9:89:c2:68
eth2addr=a2:33:c9:89:c2:69
cat /sys/class/net/eth0/address
a2:33:c9:89:c2:67
```

The follow-up reboot showed the env persisted:

```text
Loading Environment from MMC... Reading from MMC(0)... OK
```

with no repeat bad-CRC path and no new random MAC. The same triplet was visible
through `fw_printenv` after reboot.

The M04 runtime check also showed:

- board compatible `bananapi,bpi-r4-pro-8x`;
- `br-lan` over `lan5 fpc`;
- `lan5` present and linked when cabled;
- `fpc` present with no carrier when unused;
- no `mgmt` netdev;
- no MxL/SFP/combo/WAN leakage;
- Factory MAC offsets still blank, as expected for the tested board.

## Build And Check Evidence

The M04 image used for runtime validation was built through the notes repo
container wrapper with all available cores:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
```

After the runtime pass, the final tree also received the `02_network`
boot-env-guard synchronization described above. Static checks on the final tree
passed:

```sh
git diff --check
sh -n target/linux/mediatek/base-files/etc/uci-defaults/99_fwenv-store-ethaddr.sh
sh -n target/linux/mediatek/filogic/base-files/etc/board.d/02_network
sh -n target/linux/mediatek/filogic/base-files/usr/sbin/bpi-r4-pro-8x-mac-provision
sh -n package/boot/uboot-tools/uboot-envtools/files/mediatek_filogic
```

The final post-guard-sync tree was not re-imaged before this note; the
functional runtime evidence applies to the built M04 image immediately before
that shell-only consistency fix.

## Deferred Work

M05 must implement and validate:

- MxL86252 DSA driver/tag/runtime;
- AS21xxx firmware and PHY behavior;
- SFP1/SFP2;
- combo RJ45/SFP runtime switching with SFP priority;
- final LAN/WAN defaults including `combo-lan` and `combo-wan`;
- final per-port MAC policy once all netdevs exist.

M09 must validate before enabling:

- raw Factory MAC repair/write path;
- NAND-aware provisioning safety and recovery procedure.

M10 must validate:

- eMMC and SPI-NAND firstboot env behavior;
- install/sysupgrade/storage policy;
- recovery/default env behavior on non-SD media.

## M04 Closure

M04 is functionally closed for SD-based basic wired management. The remaining
items are explicit handoffs, not hidden M04 requirements.
