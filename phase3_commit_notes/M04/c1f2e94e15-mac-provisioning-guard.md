# M04.01: BPI-R4 Pro 8X MAC Provisioning Guard

Commit: `c1f2e94e155f7a6a59d0f9373653e20596fb1e6f`
Short commit: `c1f2e94e15`
Worktree: `../worktrees/openwrt-bpi-r4-pro-8x`
GitHub: `quantaji/openwrt-bpi-r4-pro-8x-adaptation@c1f2e94e155f7a6a59d0f9373653e20596fb1e6f`
Branch: `codex/bpi-r4-pro-8x-v25.12.4`
Date: 2026-06-14

## Scope

M04.01 only. This commit adds the first BPI-R4 Pro 8X Ethernet MAC identity
policy and provisioning guard.

It does not claim final LAN/WAN defaults, port topology, switch/SFP/10G runtime
correctness, AS21xxx/MxL behavior, raw Factory repair, onboard install,
sysupgrade safety, or release readiness.

The immediate M04.01 goal is narrower:

- expose a stable MAC source order for 8X;
- avoid changing LAN/WAN/interface policy before M05 topology work;
- provide a user-invoked provisioning tool;
- make automatic U-Boot env writes safe enough to run during first boot;
- keep raw NAND Factory writes blocked until M09 storage/recovery validation.

## Source Aliases

- `OW25`: OpenWrt 25.12.4 target tree and current filogic base-files patterns.
- `V8X`: direct vendor 8X DTS and board.d evidence.
- `M03`: preceding board-service commit that exposes Factory partition and
  vendor MAC offsets as unconsumed nvmem evidence.
- `RUNTIME`: real BPI-R4 Pro 8X boot and shell validation from the SD image.
- `OLD-BOOT`: old ImmortalWrt 25.12 bring-up experiment, evidence only.

## Design Decision

M04.01 uses a conservative MAC source order:

1. Use the NAND `Factory` triplet only if all three vendor offsets are present,
   valid unicast MACs, and mutually unique.
2. Else use active U-Boot env `ethaddr`, `eth1addr`, and `eth2addr` if the
   triplet is valid and unique.
3. Else use runtime `eth0` as a base and derive `+1` / `+2`.

This commit intentionally does not attach DTS `nvmem-cells` consumers to GMACs.
It also does not set `lan_mac`, `wan_mac`, or per-port MAC policy in
`02_network`. M05 owns the actual wired topology and port mapping.

The OpenWrt-visible output in this step is only `label_mac`.

## Why U-Boot Env Is The First Persistent Target

Runtime evidence showed that the tested board's M03 Factory offsets were blank:

- `gmac0 @ 0xffff4`: `ff:ff:ff:ff:ff:ff`
- `gmac1 @ 0xffffa`: `ff:ff:ff:ff:ff:ff`
- `gmac2 @ 0xfffee`: `ff:ff:ff:ff:ff:ff`

The AT24 board EEPROM at I2C `3-0057` contained a board identity string such as
`R4PRO8X-BBC30219`, not an Ethernet MAC triplet.

Therefore M04.01 does not trust Factory as a present runtime MAC source on the
tested board. The active U-Boot env is a better first persistent target because
U-Boot can pass `ethaddr` into Linux early enough for the kernel MAC assignment
path to see a stable address.

## Critical Boot-Env Safety Incident

During M04.01 runtime testing, a first implementation wrote MAC variables with
`fw_setenv` into an active MMC U-Boot env that was readable but did not contain
the complete 8X SD boot environment.

The next reboot dropped to a U-Boot menu with only:

```text
*** U-Boot Boot Menu ***
  0. Exit
MT7988>
```

At that point U-Boot showed:

```text
bootcmd=run distro_bootcmd
bootmenu_0 not defined
bootmenu_1 not defined
```

The root cause was not the Linux image itself. `fw_setenv` had made an external
MMC env valid, and U-Boot then used that incomplete external env instead of its
built-in default 8X SD environment.

The board was recovered from the U-Boot prompt with:

```text
env default -a
setenv ethaddr 02:00:11:22:33:44
setenv eth1addr 02:00:11:22:33:45
setenv eth2addr 02:00:11:22:33:46
saveenv
boot
```

After recovery, the active env contained the expected 8X SD boot variables:

```text
bootcmd=if pstore check ; then run boot_recovery ; else run boot_sdmmc ; fi
bootmenu_0=Run default boot command.=run bootcmd
bootmenu_1=Boot production system from SD card.=run boot_production
bootmenu_2=Boot recovery system from SD card.=run boot_recovery
bootconf_sd=mt7988a-bananapi-bpi-r4-pro-sd
boot_production=led $bootled_pwr on ; run sdmmc_read_production && bootm $loadaddr#$bootconf#$bootconf_sd#$bootconf_extra ; led $bootled_pwr off
boot_recovery=led $bootled_rec on ; run sdmmc_read_recovery && bootm $loadaddr#$bootconf#$bootconf_emmc#$bootconf_extra ; led $bootled_rec off
boot_sdmmc=run boot_production ; run boot_recovery
```

This incident is the reason both write paths now have a boot-env completeness
gate before any `fw_setenv` write.

## File Provenance

| File | Action | Primary source | Why in M04.01 | Deferred owner |
|---|---|---|---|---|
| `package/boot/uboot-tools/uboot-envtools/files/mediatek_filogic` | `target-pattern-write` | `OW25` BPI-R3/R4 FIT bootdev envtools group | Adds `bananapi,bpi-r4-pro-8x` so `/etc/fw_env.config` points at the active FIT bootdev env. | `M09/M10` for inactive media and install/storage policy |
| `target/linux/mediatek/base-files/etc/uci-defaults/99_fwenv-store-ethaddr.sh` | `target-pattern-write` | Existing Banana Pi fwenv persistence script plus 8X runtime evidence | Adds 8X-only automatic MAC triplet persistence with Factory/env/runtime source order and complete 8X boot-env guard. | `M05` topology; `M09` raw Factory repair |
| `target/linux/mediatek/filogic/base-files/etc/board.d/02_network` | `target-pattern-write` | `V8X` Factory offsets, `M03` nvmem evidence, `RUNTIME` blank Factory result | Adds 8X `label_mac` selection only; avoids LAN/WAN/per-port policy. | `M05` final wired topology and interface mapping |
| `target/linux/mediatek/filogic/base-files/usr/sbin/bpi-r4-pro-8x-mac-provision` | `target-pattern-write` | M04.01 design decision and runtime failure analysis | Adds an 8X-only manual provisioning utility with safe active-env writes and disabled Factory write stub. | `M09` Factory write validation and inactive env import |
| `target/linux/mediatek/image/filogic.mk` | `target-pattern-write` | M04.01 debug needs | Adds `nand-utils` so future Factory diagnostics can use NAND-aware tools. | `M09` audited raw NAND repair path |

## Code Changes

- Added `bananapi,bpi-r4-pro-8x` to the existing filogic FIT bootdev envtools
  group.
- Added 8X MAC source selection in `02_network`:
  - Factory triplet if all three offsets are valid and unique;
  - active U-Boot env triplet if valid and unique;
  - runtime `eth0` derived `+1/+2` fallback if needed.
- Set only `label_mac` for 8X.
- Added an automatic 8X uci-defaults persistence path:
  - checks `/etc/fw_env.config`;
  - requires `fw_printenv` and `fw_setenv`;
  - requires active env readability;
  - requires a complete 8X SD boot env before any write;
  - writes `ethaddr`, `eth1addr`, and `eth2addr` only through `fw_setenv`;
  - never overwrites an already valid and unique triplet unnecessarily.
- Added `bpi-r4-pro-8x-mac-provision`:
  - `status`;
  - `write-env --source current`;
  - `write-env --source random-base`;
  - `write-env --source random-triplet`;
  - `write-env --source manual`;
  - `write-env --source env-active`;
  - inactive `env-nand`, `env-emmc`, and `env-sd` sources/targets fail closed;
  - raw Factory write path exists only as a documented M09 stub and always
    refuses to perform the write.
- Added `nand-utils` to the 8X profile.

## Boot-Env Guard

Both the automatic script and manual provisioning tool now refuse U-Boot env
writes unless the active env contains the expected 8X SD boot variables.

The guard checks values including:

- `bootcmd`;
- `bootmenu_0`, `bootmenu_1`, `bootmenu_2`;
- `bootconf`;
- `bootconf_sd`;
- `bootconf_emmc`;
- `part_default`;
- `part_recovery`;
- `boot_production`;
- `boot_recovery`;
- `boot_sdmmc`;
- `mmc_read_vol`;
- `sdmmc_read_production`;
- `sdmmc_read_recovery`.

This is deliberately stricter than "fw_printenv is readable". A readable env can
still be incomplete and dangerous.

## User-Kernel Boundary

There is no kernel-side U-Boot env writer in this design.

The kernel and boot firmware decide the initial runtime MAC address. User-space
can persist MAC values only through explicit `fw_setenv` writes. The M04.01
automatic script is still user-space; it runs during OpenWrt first-boot
initialization.

The scripts therefore must be responsible for not activating an incomplete
U-Boot env.

## Runtime MAC Notes

The manually recovered test value was:

```text
ethaddr=02:00:11:22:33:44
eth1addr=02:00:11:22:33:45
eth2addr=02:00:11:22:33:46
```

This is a locally administered unicast triplet and is syntactically valid. It
was not produced by the random generator; it was manually set during U-Boot
recovery. The earlier runtime-generated value seen before persistence was
`b2:58:97:35:3b:00`.

An address starting with `99` would not be a normal unicast station MAC because
the least significant bit of the first octet is set.

## Rejected Or Deferred Behavior

Rejected from M04.01:

- GMAC DTS `nvmem-cells` consumers;
- LAN/WAN defaults;
- per-port MAC assignment;
- writing raw Factory NAND;
- guessing inactive NAND/eMMC/SD U-Boot env locations;
- automatic Factory repair;
- kernel-side MAC persistence.

Deferred:

- final wired topology and interface naming to M05;
- AS21xxx/MxL/SFP/RJ45 switching behavior to M05;
- inactive env import/export and raw Factory repair validation to M09;
- install/sysupgrade/onboard storage policy to M10.

## Build Evidence

The final M04.01 build was run from the notes repo using the project container
wrapper and all available cores:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
```

`make defconfig` reported no `.config` change.

Static checks run before the final build:

```sh
sh -n package/boot/uboot-tools/uboot-envtools/files/mediatek_filogic
sh -n target/linux/mediatek/base-files/etc/uci-defaults/99_fwenv-store-ethaddr.sh
sh -n target/linux/mediatek/filogic/base-files/etc/board.d/02_network
sh -n target/linux/mediatek/filogic/base-files/usr/sbin/bpi-r4-pro-8x-mac-provision
git diff --cached --check
```

The final manifest contains:

- `uboot-envtools - 2025.10-r2`
- `nand-utils - 2.3.0-r1`
- `ubi-utils - 2.3.0-r1`
- `kmod-eeprom-at24 - 6.12.87-r1`
- `kmod-gpio-pca953x - 6.12.87-r1`
- `kmod-i2c-mux-pca954x - 6.12.87-r1`
- `kmod-rtc-pcf8563 - 6.12.87-r1`

The rootfs staging tree contains:

- `/etc/uci-defaults/99_fwenv-store-ethaddr.sh`
- `/usr/sbin/bpi-r4-pro-8x-mac-provision`

## Artifact Hashes

All hashes are from
`../worktrees/openwrt-bpi-r4-pro-8x/bin/targets/mediatek/filogic/sha256sums`
after the final M04.01 rebuild.

| SHA256 | Artifact |
|---|---|
| `d056e77fa1b596bfc3219f3c991f5a851782116e2ab0440e41a184d5c4fbd94b` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-bl31-uboot.fip` |
| `4ecd44300972267270cd021b2965f01c85dd58155d23609886f308853e0ff5ce` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-gpt.bin` |
| `96f53f08f2065d74ac8ad0eb262f4381d1def4116ad2feefb87aca8821455144` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-emmc-preloader.bin` |
| `a8bd8d7b3ecf8c8a650ed87d95ae851aefeac1478a865ad08f601675f2e51f6b` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-initramfs-recovery.itb` |
| `19c8a5c262b6914fccb90beb80d64cd9713dcf6ce3a063e278953db9f506cd85` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-sdcard.img.gz` |
| `2897bac39495d901493cf12aa25a79575d8b0606db123748bc4861381b1b23e7` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-bl31-uboot.fip` |
| `9d4995e95d32f7a0aa4736ef534490215395a6926d5bad25691c4e18596a191a` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-snand-preloader.bin` |
| `64d0f7a1e4142c03d352883643bf3a9e7ed0c9973273c6a4cb5955c5f07954fd` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x-squashfs-sysupgrade.itb` |
| `92506225691fe7877fb6339f1cc6ae0bfe828efd32d20dae66174cac45b1df38` | `openwrt-mediatek-filogic-bananapi_bpi-r4-pro-8x.manifest` |

## Runtime Evidence

After U-Boot env recovery and reboot, Linux showed:

```text
fw_printenv ethaddr eth1addr eth2addr
ethaddr=02:00:11:22:33:44
eth1addr=02:00:11:22:33:45
eth2addr=02:00:11:22:33:46

cat /sys/class/net/eth0/address
02:00:11:22:33:44

cat /sys/class/net/eth0/addr_assign_type
0
```

This means the runtime MAC is now stable and passed in as a normal address, not
as the previous transient fallback.

The active env was located on MMC:

```text
/dev/mmcblk0p2 0x0     0x40000 0x40000 1
/dev/mmcblk0p2 0x40000 0x40000 0x40000 1
```

## Residual Risk

- M04.01 proves the active-env MAC persistence direction, not final wired
  topology.
- Factory remains blank on the tested board and must not be written before M09.
- Inactive NAND/eMMC/SD env import remains unimplemented by design.
- If a user manually corrupts U-Boot env outside Linux, they may still need
  U-Boot-side recovery with `env default -a; saveenv`.
- `02_network` still sets only `label_mac`; M05 must decide LAN/WAN/interface
  mapping when wired hardware work is ready.
