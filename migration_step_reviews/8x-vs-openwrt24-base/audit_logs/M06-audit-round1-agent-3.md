**Verdict:** accept

**Evidence Read:**  
Audit objects: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M06-basic-wifi-hardware.md`, `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M06-basic-wifi-hardware.files.tsv`

Inputs: `M06-basic-wifi-hardware.json`, `step-file-index.tsv`, selected files under `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/`

Source/diff evidence inspected: direct 8X DTS/DTSO `mt7988a-bananapi-bpi-r4-pro-8x.dts`, `mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`; vendor/target `package/kernel/mt76/Makefile`; vendor `target/linux/mediatek/image/filogic.mk`; mt76 patches `0005`, `0006`, `0029`, `0032`, `0037`, `0064`, `0073`, `0085`, plus second-pass spot patches `0038`, `0043`, `0063`, `0082`, `0088`, `0095`; PCIe patches `999-pcie-01`, `999-pcie-02`, `999-pcie-03`, `999-pcie-04`; firmware binary/diff entries `mt7990_eeprom.bin`, `mt7992_wm_tm.bin`; DTS samples `mt7987.dtsi`, `mt7988d-rfb.dts`; userspace diff `package/network/config/wifi-scripts/files/lib/netifd/hostapd.sh.patch`.

**Structural Checks:**  
PASS. TSV has 155 data rows / 371 feature assignments matching JSON.  
PASS. No missing, extra, or duplicate `file_id`.  
PASS. `status`, `path`, `file_kind`, `route_classes`, and normalized `features` exactly match JSON.  
PASS. TSV has 12 columns and no empty fields.  
PASS. All `disposition` and `owner_step` values are legal.  
PASS. `defer`, `needs-evidence`, and `static-only` rows have actionable notes/TODOs.  
PASS. Markdown says main-agent draft and formal audit not completed.  
PASS. No runtime Wi-Fi success is claimed.

**Common High-risk Row Checks:**  
PASS `000858`: direct 8X DTSO confirms GPIO4 `wifi_12v`, AT24 EEPROM `0x51/0x52`, `&i2c_wifi`, `pcie0/pcie1` mt76 nodes, and `nvmem-cell-names = "mac-address"`.  
PASS `000859`: direct base DTS confirms `imux3_wifi`, existing `eeprom@51`, `pcie0 mt7996@0,0`, `mediatek,mtd-eeprom = <&factory 0x0>`, and GPIO4 `switch_hrstn`; static-only/M03 handoff is correct.  
PASS `000343`: vendor mt76 date `2025-06-01`; target date `2026-03-19`; target defines `mt7996e`, `mt7996-firmware`, `mt7996-233-firmware`; direct image packages include AT24 and mt7996 firmware closure; no wholesale stack copy promoted.  
PASS `000372`: external EEPROM patch is real but tied to mt7992/mt7990 external/golden EEPROM and debug/testmode/writeback paths; `needs-evidence` is justified for direct 8X factory/AT24 split.  
PASS `000380`: nvmem partition name/offset patch is testmode/write-back metadata, not required read-path calibration evidence; `review-only` is justified.  
PASS `000428`: VOW/init-work ordering may affect registration time but needs target/runtime evidence; `needs-evidence` is correct.  
PASS `001135`: patch adds DT `max-link-width`; direct 8X DTS/DTSO has no such property; `needs-evidence` is correct.  
PASS `001137`: patch adds `wifi-reset-msleep`/`wifi-reset` GPIO flow; direct 8X has no reset properties and has GPIO4 conflict; `needs-evidence` is correct.  
PASS `001138`: soft off/on API is PCIe reset/power infrastructure without direct 8X proof; not over-promoted.

**Assigned Low-risk Sampling Coverage:**  
Inspected assigned rows: `000348`, `000375`, `000407`, `000416`, `000456`, `000847`, `000878`. All pass.  
Self-chosen rows: `000349` debug/recovery review-only, `000362` advanced 4-address/PS M07 handoff, `000438` non-8X target firmware closure, `000497` userspace/hotplug M07 boundary, `001136` generic PCIe IRQ affinity M09 handoff. Chosen to cover lower-risk strata outside the common list; all pass.

**Findings:**  
None.

**No-Issue Confirmations:**  
Second-pass QC did not introduce JSON/TSV mismatches. Checked correction rows align with patch content.  
M06/M07/M08/M09 boundaries are materially consistent in inspected rows.  
Target firmware superseded/drop rows match target mt76 Makefile install lists.  
Direct 8X evidence was not replaced by RFB/MT7987/vendor-family assumptions.  
No hidden runtime Wi-Fi success, MLO/AFC/6GHz, WED/offload, or generic PCIe expansion claim found.

**Residual Risk:**  
No build, compile, runtime radio probe, firmware-load, calibration-load, or association test was performed. Remaining implementation risk is in GPIO4 ownership, `i2c_wifi` vs `imux3_wifi`, duplicate `wifi_eeprom@51`, calibration source selection, target mt76 equivalence for `needs-evidence` rows, and PCIe reset/reprobe behavior.
