Verdict: accept

Evidence Read:
- Audit objects: `M06-basic-wifi-hardware.md`, `M06-basic-wifi-hardware.files.tsv`
- Required inputs: `M06-basic-wifi-hardware.json`, `step-file-index.tsv`, diffset files under `analysis/diffsets/8x-vs-openwrt24-base/files/`
- Direct 8X/vendor/target evidence inspected: direct 8X DTS/DTSO, vendor and target `package/kernel/mt76/Makefile`, vendor/target `filogic.mk`, relevant mt76 patch files `0006`, `0029`, `0037`, `0076`, `0078`, `0085`, `0090`, PCIe patches `999-pcie-01..04`, hotplug diffs `mac80211.uc` and `wifi-detect.uc`, sampled MT7987/RFB DTS/DTSO files.

Structural Checks:
- PASS: TSV coverage matches JSON: 155 files / 371 feature assignments.
- PASS: no missing, extra, or duplicate `file_id`.
- PASS: `status`, `path`, `file_kind`, `route_classes`, `features` match JSON exactly after feature CSV normalization.
- PASS: TSV has 12 columns; no empty fields.
- PASS: legal dispositions observed: `defer`, `drop`, `needs-evidence`, `review-only`, `rewrite`, `static-only`, `superseded-by-target`.
- PASS: legal owners observed: `M06`, `M07`, `M08`, `M09`.
- PASS: all `defer`, `needs-evidence`, and `static-only` rows have actionable notes/TODOs.
- PASS: markdown states main-agent draft and formal audit not completed.
- PASS: no runtime Wi-Fi success is claimed.

Common High-risk Row Checks:
- PASS `000858`: direct 8X overlay has `wifi_12v` on GPIO4, AT24 EEPROM devices/cells at `0x51/0x52`, `&i2c_wifi`, and `pcie0`/`pcie1` `mediatek,mt76` nodes using `mac-address` nvmem cells. Rewrite/TODOs are appropriate.
- PASS `000859`: base DTS has `imux3_wifi`, existing `wifi_eeprom@51`, `pcie0` `mt7996@0,0`, `mediatek,mtd-eeprom = <&factory 0x0>`, and GPIO4 `switch_hrstn`. Static-only M06 evidence with M03 ownership boundary is correct.
- PASS `000343`: vendor mt76 date is `2025-06-01`; target 25.12 is `2026-03-19` and defines/installs `mt7996e`, `mt7996-firmware`, `mt7996-233-firmware`. Direct 8X image selects `kmod-eeprom-at24` and both mt7996 firmware packages. No wholesale vendor mt76 copy.
- PASS `000372`: patch adds external EEPROM/debugfs/write callback paths, mainly justified for mt7992/mt7990 golden EEPROM. `needs-evidence` is justified and notes correctly separate AT24 MAC cells, factory MTD calibration, and mt76 external EEPROM support.
- PASS `000380`: patch parses nvmem partition/offset for testmode/atenl flash write-back. `review-only` is justified; not required read-path calibration evidence.
- PASS `000428`: patch only reorders VOW/init work to reduce registration time. `needs-evidence` is justified without target/runtime proof.
- PASS `001135`: patch adds DT-driven `max-link-width`; direct 8X DTS/DTSO has no such property. `needs-evidence` is correct.
- PASS `001137`: patch adds `wifi-reset-msleep`/`wifi-reset` handling; direct 8X DTS/DTSO has no reset properties, and GPIO4 conflict is explicit. Not promoted into M06 runtime behavior.
- PASS `001138`: patch adds PCIe soft off/on API; no direct 8X evidence that basic Wi-Fi probe depends on it. `needs-evidence` is correct.

Assigned Low-risk Sampling Coverage:
- Assigned inspected: `000419`, `000421`, `000433`, `000500`, `000851`, `000860`, `001136`.
- PASS `000419`: RX SKB sanity patch is plausible stability-only; `needs-evidence` is correct.
- PASS `000421`: HWRRO3.1/WED/RRO/offload content; defer to M08 correct.
- PASS `000433`: mt7990 critical-packet-mode patch; drop for direct 8X M06 correct.
- PASS `000500`: hotplug/userspace diff hardcodes MLO/6G/EHT/policy; defer to M07 correct.
- PASS `000851`: MT7987 BPI-R4 Lite DTS; non-8X drop correct.
- PASS `000860`: MT7988 RFB eMMC/Wi-Fi calibration reference; review-only supporting correct.
- PASS `001136`: PCIe IRQ affinity is generic controller/performance; defer to M09 correct.
- Self-chosen inspected: `000349` debug/recovery review-only sample, `000442` testmode firmware drop sample, `000458` target firmware-closure sample, `000503` userspace detection sample, `000874` same-SoC RFB DTS reference sample. Chosen to cover lower-risk debug, firmware, hotplug, and RFB strata.

Findings:
- None requiring edits.

No-Issue Confirmations:
- Second-pass QC classifications matched sampled patch/source content.
- Direct 8X hardware truth was not replaced by RFB/MT7987/R4Lite assumptions.
- M06/M07/M08/M09 boundaries held in all inspected rows.
- Superseded firmware/package rows sampled had target Makefile evidence.
- Markdown and TSV avoid runtime Wi-Fi success claims.

Residual Risk:
- No build, compile, or runtime test was performed per instruction.
- Unsampled lower-risk rows retain ordinary sampling risk, though all required high-risk and assigned sample rows were inspected.
- Implementation risk remains around GPIO4 ownership, `i2c_wifi` vs `imux3_wifi`, duplicate `wifi_eeprom@51`, calibration source selection, and whether PCIe reset/reprobe behavior is needed on actual 8X hardware.
