# M05 Audit Round 1 Agent 2

**Verdict:** accept

**Evidence Read:**  
Rules/review files read: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/project_guidelines.md`, `migration_step_batch_review_skill.md`, `rules/disposition-tags-v1.json`, `schemas/migration-step-batch-review-v1.schema.json`, `migration_roadmap.md`, `feature_migration_step_map.md`, M05 `.md`, and M05 `.files.tsv`.

Required inputs read: M05 by-step JSON, `summary/step-file-index.tsv`, and assigned/cross-sample diff patches under `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/`.

Source evidence read/searched: direct 8X DTS `mt7988a-bananapi-bpi-r4-pro-8x.dts`, 8X Wi-Fi overlay `mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`, vendor `filogic.mk`, vendor `package/kernel/as21xxx/Makefile`, vendor `package/kernel/aqr10g-phy-fw/Makefile`, RFB AQR/CUX/AN8831X DTSO files, target `package/kernel/linux/modules/netdevices.mk`, target `package/firmware/linux-firmware/aeonsemi.mk`, target AS21xxx backport patch, target mediatek `Makefile`, `filogic/config-6.12`, and target MT7988/PCS/DSA patches.

Assigned/cross-sample diff rows inspected: `000831`, `000834`, `000837`, `000838`, `000841`, `000847`, `000862`, `000864`, `000866`, `000867`, `000876`, `000877`, `000884`, `000959`, `000978`, `000998`, `000999`, `001010`, `001011`, `001013`, `001015`, `001064`, `001065`, `001071`, `001072`, `001073`, `001076`, `001081`, `001083`, `001084`; also `001124` for the mandatory split check.

**Structural Checks:** pass

TSV has 92 data rows matching by-step JSON `file_count=92`; feature assignments total 254 matching JSON `assignment_count=254`. No missing, extra, or duplicate `file_id`. TSV `status`, `path`, `file_kind`, `route_classes`, and feature names exactly match by-step JSON. Status split is `A=88`, `M=4`; feature route-class assignment split is `primary=224`, `supporting=30`. All dispositions are legal. Owner steps are legal: `M05=91`, `M08=1`. Required TODO dispositions have TODO text. Step-file-index contains the same 92 M05 IDs and same feature sets; 12 rows differ only in feature order versus by-step/TSV.

**Semantic Checks:** pass

Direct 8X DTS `000859` supports static topology claims only: SFP1/SFP2 cages, AS21xxx C45 PHY24/PHY28 with `as21x1x_fw.bin`, MxL86252 `mxl,86252`, `mxl862_8021q`, passive mux/shared mod-def0 GPIOs, and multiple DSA members are present. No runtime success is inferred.

AQR/CUX is not promoted to 8X hardware truth. Direct 8X DTS has no AQR/CUX binding; AQR/CUX appears in RFB/package evidence only, and AQR rows remain `needs-evidence` or `review-only`.

AS21xxx superseded-by-target is supported: target 25.12 provides `kmod-phy-aeonsemi-as21xxx` and `aeonsemi-as21xxx-firmware`, installing `as21x1x_fw.bin`. MxL rewrite is supported: target searches found no MxL86252 DSA/tag support.

Assigned/cross-sample rows are consistent: MT7987 rows are correctly dropped as non-8X, RFB rows are review-only, Aquantia rows are evidence-gated, MxL tag/driver/PHY rows are rewrite, debug/netlink rows are dropped, and target-backport rows are superseded by target 6.12 context. `001124` correctly keeps multiple-DSA/user-port queue behavior in M05 while deferring PPPQ/QDMA/PPE/WED/offload review to M08.

**Findings:** no actionable findings.

**No-Issue Confirmations:**

No runtime success is claimed for SFP, DSA, MxL86252, AS21xxx, 10G, VLAN, or mux behavior. M05 does not pull Wi-Fi, NAND/eMMC/sysupgrade/storage, or acceleration into implementation work; mentions are exclusions, handoffs, or TODOs. GPIO4 `switch_hrstn` versus Wi-Fi `wifi_12v` remains visible for M06.

**Residual Risk:**

Remaining risk is implementation-time, not review correctness: target 6.12 API fit for MxL86252/tag/PHY work, passive mux/shared mod-def0 behavior, AS21xxx firmware load at runtime, SFP module quirks with limited hardware, multiple-DSA queue mapping, VLAN bridge behavior, and unresolved AQR/CUX existence on real 8X hardware. These are recorded as TODOs or `needs-evidence`/`static-only` boundaries. No files were edited or committed.
