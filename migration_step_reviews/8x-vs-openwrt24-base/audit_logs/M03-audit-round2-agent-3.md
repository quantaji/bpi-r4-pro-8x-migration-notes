# M03 Audit Round 2 Agent 3

Reviewer id: `M03-audit-round2-agent-3`

Agent id: `019eaa4a-e8f0-7303-b2e0-68c124263025`

Nickname: `Noether`

## Raw Output

**Verdict: accept**

**Evidence Read**
- Review/rules: [project_guidelines.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/project_guidelines.md), [repository_map.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/repository_map.md), [migration_step_batch_review_skill.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_batch_review_skill.md), [rules/disposition-tags-v1.json](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/rules/disposition-tags-v1.json), [schemas/migration-step-batch-review-v1.schema.json](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/schemas/migration-step-batch-review-v1.schema.json), [migration_roadmap.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_roadmap.md), [feature_migration_step_map.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/feature_migration_step_map.md).
- M03 review files: [M03 markdown](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md), [M03 TSV](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.files.tsv).
- Inputs: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M03-board-identity-power-i2c-gpio-factory-data.json`, `summary/step-file-index.tsv`.
- Diff files read under `analysis/diffsets/8x-vs-openwrt24-base/files/`: `000031`, `000037`-`000041`, `000855`-`000859`, `000960`, `001003`, `001126`, `001127`, `001129`, `001130`, `001140` path-based patches, plus AQR/AS21xxx firmware binary patch metadata.
- Direct 8X vendor source read: base DTS, RTC/Wi-Fi/eMMC/SD overlays, `02_network`, `uboot-envtools/files/mediatek_filogic`, AQR Makefile/firmware metadata, AS21xxx Makefile/Kconfig/firmware metadata, and patches `001003`, `001126`, `001127`, `001129`, `001130`, `001140`.
- Target 25.12 references read: `target/linux/mediatek/filogic/base-files/etc/board.d/02_network`, `package/boot/uboot-tools/uboot-envtools/files/mediatek_filogic`, and MT7988/BPI-R4 structure patches `170`, `182`, `183`, `184`, `189`, `911`.

**Structural Checks**
- TSV coverage: PASS. by-step JSON has 87 files; TSV has 87 rows; no missing, extra, or duplicate file IDs.
- Field match: PASS. TSV `file_id/status/path/file_kind/route_classes/features` exactly matches by-step JSON and M03 rows in `step-file-index.tsv`.
- Counts: PASS. Status `A=78`, `M=9`; route assignments `primary=170`, `supporting=22`.
- Dispositions: PASS. `defer=37`, `drop=39`, `migrate=1`, `needs-evidence=4`, `review-only=5`, `rewrite=1`; all legal.
- Owners: PASS. `M03=47`, `M05=29`, `M06=2`, `M08=2`, `M10=7`; all match `MNN`.
- TODO/schema obligations: PASS. `defer` and `needs-evidence` rows have owner and actionable notes/TODO coverage; no `static-only` rows.

**Findings**
None.

**No-Issue Confirmations**
- `000859` as `rewrite` is correct. Direct 8X DTS has model/compatible at [base DTS](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:35), keys/LEDs at lines 61/77, RT5190A/CPU supply at lines 411/436, PCA9545 devices at line 497, Factory MAC cells at line 670, and later storage/runtime content at lines 563/621/644.
- `000856` as `migrate` is correct: RTC overlay is 8X-compatible and targets `&pcf8563` at [RTC DTSO](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-rtc.dtso:11).
- `000858` defer to M06 is correct, while preserving M03 evidence. Wi-Fi overlay uses GPIO4 for `wifi_12v` at [Wi-Fi DTSO](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso:13), targets `&i2c_wifi` at line 25, and adds EEPROM cells at line 29. Base DTS instead labels `imux3_wifi` and already has `wifi_eeprom@51` at [base DTS](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:546). GPIO4 conflict with `switch_hrstn` is real at line 601 and is explicitly handed off in the review at [M03 markdown](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:208).
- SD/eMMC are not overclaimed. eMMC has `ubootenv`/`rootdisk-emmc` at [eMMC DTSO](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-emmc.dtso:38); SD has GPIO12 and `rootdisk-sd` at [SD DTSO](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso:21). M03 leaves boot/storage policy to M02/M10.
- Factory MAC evidence is bounded correctly. Direct DTS defines `gmac2=0xfffee`, `gmac1=0xffffa`, `gmac0=0xffff4` at [base DTS](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:679); vendor `02_network` reads `0xFFFF4/0xFFFFA` at [02_network](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/board.d/02_network:323); M04 still owns interface defaults.
- AS21xxx/AQR boundary is acceptable. Direct DTS names `as21x1x_fw.bin` at [base DTS](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:184); AS21xxx package installs that firmware at [AS21xxx Makefile](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/package/kernel/as21xxx/Makefile:63). AQR remains `needs-evidence`.
- Off-matrix handoffs are visible: `000031` and `001126/001127/001129/001140` are called out at [M03 markdown](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:203), with TODOs at line 226. `001130` correctly needs paired `001129` driver context because `001129` consumes `calibration-data` at [cpufreq patch](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/patches-6.6/999-cpufreq-01-cpufreq-add-support-to-adjust-cpu-volt-by-efuse-cali.patch:49), while `001130` only adds DTS nvmem cells.

**Residual Risk**
Later validation remains for M04 LAN/WAN and MAC assignment, M05 wired switch/SFP/10G/AS21xxx/AQR proof, M06 Wi-Fi overlay/runtime and GPIO4 ownership, M08 acceleration, M09 USB/PCIe/fan/extras, and M10 eMMC/NAND/rootdisk/env/sysupgrade/install. M03 implementation-time runtime checks for I2C devices, RTC, PCA9555 LEDs, keys, Factory nvmem reads, and power rails are still needed, but they are not matrix defects.
