Verdict: accept

Evidence Read:
- Review artifacts inspected:
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.md
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/rules/disposition-tags-v1.json
- JSON/index inputs inspected:
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv
- Diff files inspected:
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/filogic/base-files/etc/board.d/02_network.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/filogic/base-files/etc/config/network.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-2700-net-ethernet-mtk_eth_soc-add-mdio-reset-delay.patch.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-2704-net-ethernet-mtk_eth_soc-revise-mdc-divider-configur.patch.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-2707-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-9800-mt7988a-bananapi-bpi-r4pro-support-multiple-dsa-switch-fixed.patch.patch
  - dnsmasq Makefile/0001/0002/200 patch diffs, mt7988a-rfb-eth0-gsw.dtso.patch, 999-2713 EEE patch, hnat.c.patch, 999-2710 RSS patch, 999-2730 PPPQ patch, netifd wireless reload patch, rsno-off.sh.patch, reset-boot-count Makefile/init/src patches, mt7987a-bananapi-bpi-r4-lite.dts.patch, packet-steering.uc.patch, relay.init.patch, and off-matrix 999-2004 MAC-address patch.
- Direct 8X vendor source inspected:
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/board.d/02_network
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/config/network
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts
- Target 25.12 source inspected:
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4/target/linux/mediatek/filogic/base-files/etc/board.d/02_network
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4/package/network/services/dnsmasq/Makefile
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4/package/network/services/dnsmasq/patches/200-ubus_dns.patch
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4/package/network/services/dnsmasq/patches/
  - /mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4/target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch

Structural Checks:
- TSV schema: pass. Header is exactly the expected 12 columns.
- TSV coverage against M04 by-step JSON: pass. JSON says 111 files / 115 assignments; TSV has 111 data rows, 111 unique file_id values, no missing, no extra, no duplicates.
- TSV exact field match against JSON: pass. status/path/file_kind/route_classes/features all matched JSON exactly.
- step-file-index cross-check: pass with known non-TSV caveat. M04 index has 111 rows and the same IDs; only index-vs-JSON mismatch is `000960` feature order. TSV intentionally follows by-step JSON exact order.
- Legal dispositions: pass. Counts: defer 76, drop 23, needs-evidence 2, review-only 2, rewrite 2, superseded-by-target 6.
- Owner steps: pass. Counts: M04 35, M05 17, M07 2, M08 53, M10 4.
- TODO/owner obligations: pass. All defer and needs-evidence rows have named Mxx owner and actionable TODO text.
- Markdown summaries: pass. Disposition, owner, and group summaries match TSV counts. Markdown records round 1 and round 2 summaries only; it does not claim round 3 completion.

Dense Sampling Coverage:
- M04 direct evidence/action rows: `000960` TSV line 47, `000963` line 49, `000859` line 30.
- M04 needs-evidence rows: `001018` line 52, `001022` line 55.
- Superseded-by-target rows: `000504` line 10, `000505` line 11, `000506` line 12, `000508` line 14, `001025` line 58.
- M05 defer rows: `000861` line 31, `001031` line 64, `001124` line 112.
- M08 defer rows: `000897` line 39, `001028` line 61, `001047` line 80, plus `000825` line 16 context.
- M07 defer rows: `000496` line 9, `000826` line 17.
- M10 defer rows: `000490` line 3, `000491` line 4, `000493` line 6.
- Drop rows: `000851` line 29, `000495` line 8, `000786` line 15.
- No sample exposed a mismatch requiring full-cluster expansion.

Findings:
- None.

No-Issue Confirmations:
- `000960` is correctly M04 rewrite, not wholesale copy. Direct vendor board.d has `bananapi,bpi-r4-pro-8x` LAN ports `lan0 lan3 mxl_lan0 mxl_lan1 mxl_lan2 mxl_lan3 mxl_lan5` and WAN `eth1` at vendor `02_network`:196-197; the generic vendor MT7987/MT7988 MAC helper uses Factory offsets at lines 323-327, so the review correctly treats direct DTS nvmem cells as authoritative MAC evidence.
- `000963` is correctly limited to wired port-group evidence. Vendor static config has br-lan ports at `etc/config/network`:12-21 and br-wan/eth1 at lines 30-40, but also hard-coded LAN IP and WWAN entries at lines 23-28 and 53-59.
- `000859` is correctly review-only M04 evidence with M03/M05/M10 split. Direct 8X DTS enables GMAC0/1/2 with nvmem cells at lines 149-173, has C45 PHY evidence at lines 213-219, MxL/SFP/DSA topology at lines 242-334, Factory MAC cells at lines 679-688, and U-Boot env/NAND storage content at lines 699-720.
- `001018` and `001022` are correctly `needs-evidence`, not accepted from MTK SDK alone. Vendor patch `999-2700` adds MDIO reset delay at lines 18-35; `999-2704` moves/configures MDC divider logic at lines 4-8 and 23-107. Direct 8X DTS shows relevant C45 MDIO devices at lines 213-219, but that is not runtime enumeration proof.
- `001124` is correctly M05 primary with M08 secondary. The patch has multiple-DSA/PPPQ queue mapping at diff lines 42-112 and PPE/offload changes at lines 189-201 and 300-454.
- `001003` is correctly recorded only as an off-matrix handoff. Markdown records it at lines 110 and 238; M04 JSON and TSV contain no `001003`; the patch fixes LAN/WAN MAC offset polarity at vendor patch lines 23-32.
- dnsmasq superseded-by-target rows are supported. Vendor diff moves dnsmasq to 2.91-era state at dnsmasq Makefile patch lines 10-18 and deletes old 0001/0002 patches; target 25.12 Makefile already has upstream version 2.91 and matching hash at lines 11-17, and target patch directory carries current patches including `200-ubus_dns.patch`.
- `001025` superseded-by-target is supported. Vendor forced-reset dump patch is diagnostic at lines 4-7 and adds dump helpers at lines 46-151; target 25.12 already carries comparable generic patch `730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch` at lines 4-7 and 44-101.
- M04 boundary is respected. Full DSA/SFP/10G/EEE rows are M05; HNAT/PPE/WED/RSS/LRO/QDMA/PPPQ rows are M08; wireless userspace rows are M07; reset-boot-count/storage policy is M10. Markdown line 167 explicitly avoids runtime wired/SFP/DSA/10G/offload/storage success claims.

Residual Risk:
- M04 still needs implementation-time/runtime validation for link enumeration, management reachability, `eth1` copper behavior, bridge membership, Factory MAC assignment, and MDIO timing.
- Later M05, M07, M08, and M10 work remains necessary for full wired switch/SFP/10G behavior, wireless userspace policy, acceleration/offload/performance, and storage/bootcount policy. These are correctly treated as residual work, not M04 matrix defects.
