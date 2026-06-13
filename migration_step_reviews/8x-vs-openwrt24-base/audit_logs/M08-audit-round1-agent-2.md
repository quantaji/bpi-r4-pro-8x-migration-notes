# M08 Audit Round 1 Agent 2 Raw Report

Verdict: accept-with-minor-edits

Evidence Read: exact files/patches/source files inspected
- Audit targets:
  - migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.md
  - migration_step_reviews/8x-vs-openwrt24-base/M08-acceleration-and-offload.files.tsv
- Required inputs:
  - analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M08-acceleration-and-offload.json
  - analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv
  - analysis/diffsets/8x-vs-openwrt24-base/files/
- Direct 8X / target source evidence:
  - vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/.config
  - vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/image/filogic.mk
  - vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/package/kernel/mt76/Makefile
  - vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/package/kernel/linux/modules/netfilter.mk
  - upstreams/openwrt-25.12.4/package/kernel/mt76/Makefile
  - upstreams/openwrt-25.12.4/package/kernel/linux/modules/netfilter.mk
  - upstreams/openwrt-25.12.4/package/libs/libnfnetlink/
  - upstreams/openwrt-25.12.4/target/linux/generic/backport-6.12/731-v6.18-net-mediatek-wed-Introduce-MT7992-WED-support-to-MT7.patch
  - upstreams/openwrt-25.12.4/target/linux/generic/backport-6.12/733-v6.18-net-mtk-wed-add-dma-mask-limitation-and-GFP_DMA32-fo.patch
- Diffset row patches/sources inspected:
  - Common high-risk rows: 000052, 000343, 000374, 000375, 000400, 000421, 000426, 000441, 000442, 000455, 000456, 000458, 000468, 000471, 000897, 000898, 000899, 000900, 000902, 000903, 000904, 000957, 001027, 001028, 001029, 001037, 001056, 001057, 001058, 001060, 001062, 001063, 001087, 001101, 001107, 001113, 001118, 001119, 001123.
  - Assigned low-risk rows: 001104, 001103, 001017, 000368, 000359, 000417, 000469.
  - Self-selected rows: 001092, 001102, 001112, 001115, 000385.

Structural Checks: counts and pass/fail
- PASS: JSON reports 87 files / 165 assignments; TSV has 87 data rows and 87 unique file_id values.
- PASS: no missing, extra, or duplicate file_id in TSV versus JSON.
- PASS: exact TSV/JSON match for status, path, file_kind, features, and route_classes.
- PASS: assignment route class counts match JSON: primary=162, review-only=3.
- PASS: TSV disposition counts match markdown: defer=10, drop=4, needs-evidence=57, review-only=12, superseded-by-target=4.
- PASS with one markdown inconsistency: owner counts are M08=77, M07=10 in TSV, but markdown line 185 still lists 000375 under M07 despite TSV line 16 and markdown lines 80/109/123/196 placing 000375 in M08.

Common High-Risk Findings
- 000052 and 000471: disposition needs-evidence is correct. Vendor adds nf-flow-netlink packaging and NFNL_SUBSYS_FLOWTABLE; target 25.12 has nf-flow/nft-offload but no nf-flow-netlink/NF_FLOW_TABLE_NETLINK/libnfnetlink flowtable hit. No runtime/offload success is claimed.
- 000343: needs-evidence is correct. Vendor mt76 Makefile mixes source bump, MODPARAMS.mt7996e:=wed_enable=1, debugfs/testmode flags, mt7990 package, and *_wm_tm firmware. Target lacks the vendor module param/testmode installs.
- 000374, 000400, 000421, 000426, 001118: self-QC disposition needs-evidence is correct. Patch bodies touch shared mt76/mt7996 or generic WED/RRO/HWRRO code despite mt7990/mt7987/mt7992 title text; not title-dropped.
- 000375: TSV disposition needs-evidence/M08 is correct because body touches WED TXS BA status and WDMA forward-path TID mapping. Minor markdown handoff bug noted below.
- 000441, 000442, 000455, 000456: drop is supported. They are binary non-8X mt7990/mt7992 firmware rows; direct 8X image recipe selects kmod-mt7996-firmware, kmod-mt7996-233-firmware, and mt7988-wo-firmware, while direct 8X .config leaves mt7990/mt7992 firmware unset.
- 000458 and 000468: superseded-by-target is supported. Target mt76 Makefile installs mt7996_dsp.bin and mt7996_wm_233.bin in the ordinary mt7996 package paths.
- 000897-000904 and 000957: needs-evidence is correct. Vendor HNAT tree is real acceleration/HNAT code, but direct 8X .config has CONFIG_PACKAGE_kmod-mediatek_hnat unset; target lacks vendor HNAT tree.
- 001027, 001028, 001029, 001037, 001056, 001057, 001058, 001060, 001062, 001087, 001101, 001119, 001123: needs-evidence is correct. These are real RSS/LRO/PPE/HNAT/netfilter/WED/TOPS candidates and remain target/API/runtime-gated.
- 001063 and 001017: review-only is correct. Crypto/EIP adjacency is not direct proof for M08 WED/PPE/TOPS migration.
- 001107 and 001113: superseded-by-target is supported. Target backport 733 carries the same DMA32/dma-mask semantics; target backport 731 carries the same MT7988 second WDMA RX ring / MT7992 WED support semantics.

Assigned Low-Risk Findings
- 001104: needs-evidence is correct; xt_FLOWOFFLOAD memory leak fix only applies if vendor xt flowoffload extension is retained.
- 001103: needs-evidence is correct; nft DSCP learning changes nft_flow_offload semantics and needs target comparison.
- 001017: review-only is correct; EIP197 secure-support changes are crypto-specific.
- 000368: needs-evidence is correct; patch separates HWRRO from WED and changes RRO queues/page-pool/token handling.
- 000359: defer/M07 is correct; dynamic preamble-puncturing vendor/debug commands are wireless policy/debug, not M08 acceptance.
- 000417: defer/M07 is correct; ADDBA-after-authorized is association/aggregation policy. It does not silently claim WED success.
- 000469: review-only is correct; mt7996_wm_tm.bin is testmode firmware and target runtime packaging does not install it.

Self-Selected Rows and Findings
- 001092 selected because DEV_PATH_MTK_WDMA in xt_FLOWOFFLOAD bridges netfilter/PPE/WED routing. Finding: needs-evidence/M08 is correct.
- 001102 selected because DEV_PATH_MTK_WDMA in nft_flow_offload has the same PPE/WED/netfilter crossing. Finding: needs-evidence/M08 is correct.
- 001112 selected because title says MLO throughput, but body changes WED WPDMA TX_DDONE behavior. Finding: needs-evidence/M08 is correct; MLO-performance aspect remains boundary text only.
- 001115 selected because hwpath WMM touches mtk_ppe, mtk_ppe_offload, mtk_wed, and public WED headers. Finding: needs-evidence/M08 is correct.
- 000385 selected because compile-version gates WED/RRO cleanup paths and moves WDMA TID behavior. Finding: needs-evidence/M08 is correct.

Drop/Superseded Checks
- Drops are limited to binary firmware rows 000441, 000442, 000455, 000456. I found no hidden generic/shared code in those drops.
- Superseded-by-target rows are 000458, 000468, 001107, 001113. Target 25.12 evidence supports same-semantic coverage for all four.

Boundary Checks
- PASS: no basic wired, SFP/10G, Wi-Fi association, MLO/AFC, NAND/eMMC/sysupgrade/storage, or throughput-only success is accepted.
- PASS: needs-evidence rows state concrete target/API/runtime gaps and do not silently claim migration success.
- PASS: self-QC rows 000374, 000375, 000400, 000421, 000426, 001113, 001118 were appropriately scrutinized and mostly corrected away from title-based drops.

Findings ordered by severity
- Minor: markdown line 185 lists 000375 under M07 handoffs, contradicting TSV line 16 and markdown lines 80, 109, 123, and 196, which correctly keep 000375 as M08 needs-evidence. Remove 000375 from the M07 handoff list or qualify only the ordinary ADDBA-policy aspect.

No-Issue Confirmations
- No structural JSON/TSV coverage issue found.
- No incorrect drop found.
- No unsupported superseded-by-target claim found.
- No boundary violation found.
- No actionable disposition/owner error found in the TSV.

Residual Risk
- High technical residual risk remains because many M08 rows are large WED/PPE/HNAT/netfilter patch stacks needing target 6.12/mt76 comparison and runtime validation. This is already represented as needs-evidence and is not an audit blocker.
