# M03 Audit Round 2 Agent 2

Reviewer id: `M03-audit-round2-agent-2`

Agent id: `019eaa4a-e8a9-7053-8d44-2cd45813599b`

Nickname: `Ptolemy`

## Raw Output

**Verdict:** `accept-with-minor-edits`

**Evidence Read:**
- Review files: `migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md`; `.files.tsv`.
- Routing inputs: M03 by-step JSON; `summary/step-file-index.tsv`; key diff files for `000031`, `000037`-`000040`, `000859`, `000856`, `000858`, `000855`, `000857`, `000960`, `001003`, `001126`, `001127`, `001129`, `001130`, `001140`.
- Direct 8X source: base DTS, RTC/Wi-Fi/eMMC/SD overlays, `02_network`, AQR/AS21xxx package files, AS21xxx driver snippets, cpufreq/clock/serial handoff patches.
- Target 25.12 references: `target/linux/mediatek/image/filogic.mk`, `filogic/base-files/etc/board.d/02_network`, MT7988 DTS references/patches including BPI-R4 PCA9545 and storage/RTC overlays. Used as structure reference only.

**Structural Checks:**
- TSV coverage: pass. JSON declares 87 files; TSV has 87 rows; summary index has 87 M03 rows.
- Missing/extra/duplicate file IDs: pass, none.
- Field match: pass. `status/path/file_kind/route_classes/features` match by-step JSON and summary index exactly.
- Status counts: pass, `A=78`, `M=9`.
- Dispositions: pass, all legal. Counts: `defer=37`, `drop=39`, `migrate=1`, `needs-evidence=4`, `review-only=5`, `rewrite=1`.
- Owners: pass, all legal. Counts: `M03=47`, `M05=29`, `M06=2`, `M08=2`, `M10=7`.
- TODO obligations: pass overall via markdown TODOs; one row-local wording issue below.

**Findings:**
- Minor, [files.tsv](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.files.tsv:5), affected `000040`-`000049`: AS21xxx `defer` rows name M05 ownership but do not use the explicit `M05 TODO:` wording used by other deferred rows. The markdown does cover this at [line 229](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:229), so this is not blocking. Recommended fix: add row-local `M05 TODO: verify AS21xxx driver/firmware package closure and runtime PHY validation`.

**No-Issue Confirmations:**
- `000859` as `rewrite` is correct. Direct 8X base DTS has model/compatible at [line 35](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:35), keys at [line 61](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:61), LEDs via PCA9555 at [line 77](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:77), RT5190A at [line 436](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:436), PCA9545/PCF8563/AT24/PCA9555 at [line 497](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:497), and Factory MAC cells at [line 679](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:679). The markdown splits its wired/Wi-Fi/extras/storage content to M04/M05/M06/M09/M10 at [line 209](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:209).
- `000856` as `migrate` is correct: the RTC overlay is 8X-compatible and targets `&pcf8563` at [line 11](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-rtc.dtso:11).
- `000858` is correctly deferred to M06 while preserving M03 evidence: Wi-Fi overlay uses GPIO4 `wifi_12v` at [line 13](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso:13), targets `&i2c_wifi` at [line 26](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso:26), and adds EEPROM cells at [line 29](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso:29). Base DTS labels the mux channel `imux3_wifi` and already has `wifi_eeprom@51` at [line 546](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:546).
- GPIO4 conflict is not minimized: base DTS hogs GPIO4 as `switch_hrstn` at [line 601](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:601); M03 records a cross-step TODO at [line 225](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:225).
- Factory MAC boundary is correct: DTS offsets are `gmac2=0xfffee`, `gmac1=0xffffa`, `gmac0=0xffff4` at [line 679](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:679); board.d also reads `0xFFFF4/0xFFFFA` at [line 323](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/board.d/02_network:323), while LAN/WAN defaults are left to M04.
- AS21xxx/AQR split is correct: direct 8X DTS names `as21x1x_fw.bin` at [line 190](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts:190); AQR remains M05 `needs-evidence`.
- No M03 runtime success claim found; markdown explicitly excludes wired/Wi-Fi/storage/runtime success at [line 49](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M03-board-identity-power-i2c-gpio-factory-data.md:49).

**Residual Risk:**
- Later M04/M05/M06/M08/M09/M10 still need runtime validation for network defaults, AS21xxx/AQR applicability, Wi-Fi overlay merge/regulator behavior, acceleration, board extras, and storage/sysupgrade. These are correctly not treated as M03 defects.
