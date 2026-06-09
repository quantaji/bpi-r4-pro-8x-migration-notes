# M03 Audit Agent 1 Raw Output

Reviewer id: `M03-audit-agent-1`

Agent id: `019eaa37-d833-74a3-bd19-916cd006db6c`

Nickname: `Arendt`

## Raw Output

**Verdict:** `accept-with-minor-edits`

No files edited. No commits made. No sub-agents launched.

**Evidence Read**

Roots:
`$REPO=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo`
`$AN=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis`
`$V8X=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel`
`$OW25=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4`

Review/rule files read:
`$REPO/project_guidelines.md`, `repository_map.md`, `migration_step_batch_review_skill.md`, `rules/disposition-tags-v1.json`, `schemas/migration-step-batch-review-v1.schema.json`, `migration_roadmap.md`, `feature_migration_step_map.md`, M03 review markdown, M03 TSV.

By-step/index/diff files read:
`$AN/migration-step-routing/8x-vs-openwrt24-base/by-step/M03-board-identity-power-i2c-gpio-factory-data.json`, `summary/step-file-index.tsv`, plus diff patches for `000031`, `000855`, `000856`, `000857`, `000858`, `000859`, `000960`, `001003`, `001129`, `001130`, AQR Makefile, AS21xxx Makefile/Kconfig.

Direct 8X vendor source read:
base DTS, RTC/Wi-Fi/eMMC/SD overlays, `02_network`, `uboot-envtools/files/mediatek_filogic`, AS21xxx Makefile/Kconfig, AQR Makefile, Factory MAC patch `999-2004...`, cpufreq patches `999-cpufreq-01/02`, clock/serial M00 handoff patches `001126`, `001127`, `001140`. Firmware binaries were metadata-listed, not decoded.

Target 25.12 references read:
`$OW25/target/linux/mediatek/image/filogic.mk`, `target/linux/mediatek/filogic/base-files/etc/board.d/02_network`, `package/boot/uboot-tools/uboot-envtools/files/mediatek_filogic`, and R4 Lite DTS/SD/eMMC/NAND files under `target/linux/mediatek/dts`.

**Structural Checks**

PASS: by-step JSON has 87 files and 192 feature assignments. TSV has 87 rows, 87 unique IDs, no missing, extra, or duplicate IDs.

PASS: TSV `status/path/file_kind/features/route_classes` match by-step JSON exactly. Status counts match: `A=78`, `M=9`.

PASS: dispositions legal. Counts: `defer=37`, `drop=39`, `migrate=1`, `needs-evidence=4`, `review-only=5`, `rewrite=1`.

PASS: owner steps legal. Counts: `M03=47`, `M05=29`, `M06=2`, `M08=2`, `M10=7`.

PASS with note: defer/needs-evidence rows have owners and actionable follow-up. AS21xxx TSV rows do not literally say `TODO`, but markdown TODO line 212 covers them.

**Findings**

1. Severity: minor for M03, potential M06 functional risk
   File/line: `$REPO/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:107`, `:191`, `:215`; affected `000858`.
   Problem: M03 records `wifi_12v` GPIO4 and Wi-Fi EEPROM cells, but misses that the 8X Wi-Fi overlay targets `&i2c_wifi` while the 8X base DTS defines the mux channel as `imux3_wifi`. Source: Wi-Fi overlay uses `target = <&i2c_wifi>` at `$V8X/.../mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso:25-27`; base DTS has `imux3_wifi: i2c@3` and already defines `wifi_eeprom: eeprom@51` at `$V8X/.../mt7988a-bananapi-bpi-r4-pro-8x.dts:546-557`.
   Why it matters: M06 could inherit a non-applying overlay target or create duplicate 0x51 AT24 nodes instead of merging/rewriting the base Wi-Fi EEPROM node with nvmem layout.
   Recommended fix: add a M06 TODO in markdown and TSV row `000858`: resolve `i2c_wifi` vs `imux3_wifi`, and decide whether the overlay should merge the existing base `eeprom@51` node or replace/restructure it.

**No-Issue Confirmations**

`000859` is correctly `rewrite`: direct DTS has model/compatible at lines 35-37, keys at 61-74, PCA9555 LEDs at 77-89, RT5190A and CPU/CCI supply at 411-483, PCA9545/PCF8563/AT24/PCA9555 at 497-531, Factory MAC cells at 679-689, GPIO4 `switch_hrstn` at 601-607, and mixed wired/storage/runtime content later split by review lines 123 and 192.

`000856` is correctly `migrate`: RTC overlay is 8X-compatible and targets `&pcf8563` at `$V8X/...-rtc.dtso:10-17`; review/TSV keep it static without RTC runtime claim.

Storage boundary is acceptable: eMMC overlay has env/rootdisk semantics at `$V8X/...-emmc.dtso:38-60`; SD overlay has GPIO12 plus env/rootdisk at `$V8X/...-sd.dtso:21-58`. M03 hands these to M02/M10 and does not claim SD/eMMC boot success.

Factory MAC evidence is correctly limited: direct DTS has `gmac2=0xfffee`, `gmac1=0xffffa`, `gmac0=0xffff4` at lines 679-689; vendor `02_network` reads Factory `0xFFFF4/0xFFFFA` at lines 323-327; patch `001003` supports the same polarity at lines 23-32. M04 owns LAN/WAN defaults.

AS21xxx/AQR boundary is acceptable: direct 8X DTS names `as21x1x_fw.bin` for PHY24/PHY28 at lines 184-190 and 213-219. AS21xxx package installs that firmware at `$V8X/package/kernel/as21xxx/Makefile:63-67`. AQR package exists, but direct 8X DTS has no AQR/Aquantia/CUX reference, so `needs-evidence` for M05 is correct.

Off-matrix handoffs are visible: markdown covers `000031` at lines 186 and 209, M00 handoffs `001126/001127/001129/001140` at lines 200 and 210, and pairs `001130` with `001129`. Source confirms `001129` driver consumes `calibration-data`, while `001130` only adds CPU nvmem cells.

**Residual Risk**

Later validation remains for M04 wired defaults/MAC assignment, M05 switch/SFP/AS21xxx/AQR proof, M06 Wi-Fi overlay/runtime, M08 acceleration, M09 USB/PCIe/fan/extras, and M10 storage/install/sysupgrade. These are deferred risks, not M03 matrix defects.
