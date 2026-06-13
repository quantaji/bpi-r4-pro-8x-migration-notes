# M08 Audit Round 2 Agent 2 Raw Report

- Verdict: accept-with-minor-edits

- Evidence Read:
  - Audit artifacts: `migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.md`, `M08-acceleration-and-offload.files.tsv`
  - Required inputs: M08 by-step JSON, `summary/step-file-index.tsv`, diffset patches under `analysis/diffsets/8x-vs-openwrt24-base/files/`
  - Reference source: vendor `.config`, vendor `target/linux/mediatek/image/filogic.mk`, vendor/target `package/kernel/mt76/Makefile`, vendor/target `package/kernel/linux/modules/netfilter.mk`, vendor `mt7988a.dtsi`, target WED backports `731-v6.18...MT7992...patch` and `733-v6.18...GFP_DMA32...patch`
  - Patch/source bodies inspected for all common high-risk rows, assigned rows, remediation rows, and self-selected rows.

- Structural Checks:
  - JSON file count: pass, 87 declared / 87 actual.
  - JSON assignment count: pass, 165 declared / 165 actual.
  - TSV rows: pass, 87.
  - Missing/extra/duplicate TSV file_id: pass, none.
  - Exact TSV match for `status/path/file_kind/features/route_classes`: pass.
  - Disposition counts verified: `needs-evidence=60`, `defer=10`, `review-only=9`, `drop=4`, `superseded-by-target=4`.
  - Owner counts verified: `M08=77`, `M07=10`.

- Common High-Risk Findings:
  - No technical disposition/owner issue found.
  - `000052`/`000471`: correct `needs-evidence`; vendor adds `nf-flow-netlink`/`NFNL_SUBSYS_FLOWTABLE`, target has normal `nf-flow`/`nft-offload` but not same netlink/libnfnetlink evidence.
  - `000441`, `000442`, `000455`, `000456`: drops are package-evidence based, not title-only. Direct 8X image selects `kmod-mt7996-firmware`, `kmod-mt7996-233-firmware`, `mt7988-wo-firmware`, not mt7990/mt7992 firmware packages.
  - `001107`, `001113`: target-superseded claims verified against OpenWrt 25.12 backports `733-v6.18` and `731-v6.18`.
  - HNAT rows `000897`-`000904`, `000957`, `001056`-`001062`: correct `needs-evidence`; target lacks vendor HNAT tree and direct 8X config leaves `kmod-mediatek_hnat` unset.
  - Mixed-title/debug remediation rows `000350`, `000374`, `000375`, `000400`, `000421`, `000426`, `001063`, `001116`, `001118`: correct `needs-evidence`; actual bodies include shared WED/RRO/HWRRO/PPE/tunnel metadata behavior, not safe drops/review-only.

- Assigned Low-Risk Findings:
  - `000347`: WED RRO NAPI init behavior; `needs-evidence` M08 correct.
  - `000384`: RX status `wcid_idx`/RCU-adjacent behavior; `needs-evidence` M08 correct.
  - `000409`: testmode refactor only; `review-only` M08 correct.
  - `000431`: scan dwell-time policy; `defer` M07 correct.
  - `001102`: `DEV_PATH_MTK_WDMA` nft flow path; `needs-evidence` M08 correct.
  - `001105`: nft flow memory-leak fix conditional on vendor nft extension; `needs-evidence` M08 correct.
  - `001121`: WDMA disable flow during Wi-Fi L1 SER; `needs-evidence` M08 correct.

- Self-Selected Rows and Findings:
  - `000393`: selected because review-only common debug APIs could hide runtime changes. Body is debug API/common debug mask plumbing; `review-only` OK.
  - `000471`: selected because flowtable UAPI can gate userspace. Header-only `NFNL_SUBSYS_FLOWTABLE` addition lacks target equivalence; `needs-evidence` OK.
  - `000894`: selected because debugfs source has register/reset write controls. Diagnostics only, not acceptance evidence; `review-only` OK.
  - `001035`: selected because LRO GLO_MEM is shared datapath-adjacent. `needs-evidence` OK.
  - `001103`: selected because DSCP learning changes nft policy semantics. `needs-evidence` OK.

- Drop/Superseded Checks:
  - Drops are limited to non-8X firmware package payloads and do not hide shared/generic code.
  - Superseded rows have same-semantic target evidence for firmware packaging and WED backports.

- Boundary Checks:
  - Pass. M08 markdown/TSV do not claim basic wired success, Wi-Fi runtime success, MLO/AFC success, storage/sysupgrade success, or throughput-only acceptance.

- Findings Ordered by Severity:
  - Minor: `M08-acceleration-and-offload.md:7` says no second audit round has been launched. Under this round2 audit, that status text is stale and should be updated when round2 is recorded. No TSV or technical disposition impact.

- No-Issue Confirmations:
  - No missing/extra/duplicate coverage issue.
  - No actionable disposition/owner error found.
  - No title-based drop found.
  - No silent migration/runtime success claim found.

- Residual Risk:
  - High residual implementation risk remains in WED/RRO/HWRRO, PPE/nft/xt, RSS/LRO, HNAT, and TOPS rows because most are intentionally `needs-evidence` and require target 6.12/API/runtime comparison before migration.
