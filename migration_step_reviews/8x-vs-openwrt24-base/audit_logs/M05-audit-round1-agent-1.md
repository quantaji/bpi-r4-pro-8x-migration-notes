# M05 Audit Round 1 Agent 1

**Verdict:** accept

**Evidence Read:** required rules/artifacts, M05 markdown/TSV, M05 routing JSON, `step-file-index.tsv`, direct 8X DTS `000859`, assigned/cross-sample diff patches, vendor RFB AQR/CUX DTS references, target OpenWrt 25.12 AS21xxx/AN8855/MT7987/PHYA patches, target Linux 6.12 SFP/PCS sources, and target searches for MxL86252 absence. I did not read prior audit logs.

Assigned/cross diff files inspected were for:
`000832, 000833, 000836, 000837, 000840, 000842, 000851, 000863, 000865, 000868, 000875, 000877, 000884, 000885, 000998, 001000, 001001, 001009, 001012, 001013, 001016, 001044, 001049, 001070, 001071, 001072, 001073, 001076, 001078, 001079, 001083`.

**Structural Checks:** pass

- M05 by-step JSON: 92 files, 254 feature assignments.
- TSV: 92 rows plus header, 254 feature assignments.
- `step-file-index.tsv`: 92 M05 rows, 254 assignments.
- Coverage: no missing, extra, or duplicate `file_id`.
- Exact field match against JSON: `status`, `path`, `file_kind`, `route_classes`, and `features` all match.
- Status counts: `A=88`, `M=4`.
- Dispositions legal: pass. Counts: `drop=24`, `rewrite=22`, `superseded-by-target=16`, `needs-evidence=15`, `review-only=13`, `defer=1`, `static-only=1`.
- Owner steps legal: pass. Counts: `M05=91`, `M08=1`.
- Required TODO coverage: pass for all 17 `defer`/`static-only`/`needs-evidence` rows.

**Semantic Checks:** pass

- `000859` direct 8X DTS supports static topology only; the review correctly avoids runtime success claims.
- Direct 8X evidence confirms SFP1/SFP2, PHY24/PHY28 with `as21x1x_fw.bin`, MxL86252, `mxl862_8021q`, passive muxes, shared mod-def0 GPIOs, and multiple DSA members.
- AQR/CUX is not promoted to 8X hardware truth; direct 8X DTS has no AQR/CUX node, while AQR/CUX appears only in RFB/vendor-package evidence.
- AS21xxx supersession is valid: target 25.12 provides `kmod-phy-aeonsemi-as21xxx` and `aeonsemi-as21xxx-firmware`, and the firmware installs `as21x1x_fw.bin`.
- Target 25.12 lacks MxL86252 DSA/tag/mux support; rewrite disposition for MxL rows is supported.
- `000998` supersession is valid: Linux 6.12 `sfp_select_interface()` already handles `2500baseT_Full` as `2500BASEX`.
- `001016` supersession is valid: target has `741-net-pcs-mtk-lynxi-add-phya-tx-rx-clock-path.patch`.
- `001124` split is correct: M05 keeps multiple-DSA/user-port queue behavior visible and defers PPPQ/QDMA/PPE/WED/offload to M08.
- No Wi-Fi, NAND/eMMC/sysupgrade/storage, or acceleration implementation is pulled into M05.

**Findings:** no actionable findings.

**No-Issue Confirmations:**

- Assigned MT7987/R4Lite rows are correctly dropped as non-8X topology.
- Assigned RFB rows are correctly `review-only`.
- Assigned AQR/Aquantia and module-specific SFP quirks are correctly evidence-gated.
- Debug/netlink rows are not treated as required hardware support.
- Runtime validation remains TODO-only, not claimed as complete.

**Residual Risk:** implementation-time only: MxL86252 driver/tag API fit on 6.12, AS21xxx firmware/link runtime, SFP module-specific quirks, shared mod-def0 mux behavior, multiple-DSA queue mapping, VLAN bridge correctness, and whether actual hardware ever exposes an AQR/CUX path.
