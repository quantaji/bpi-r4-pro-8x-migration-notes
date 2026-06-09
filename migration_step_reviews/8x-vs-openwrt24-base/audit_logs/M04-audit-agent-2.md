Verdict: accept-with-minor-edits

Evidence Read:
- `migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.md`
- `migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Direct 8X vendor source:
  - `.../BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/board.d/02_network`
  - `.../BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/config/network`
  - `.../BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/filogic/base-files/etc/config/firewall`
  - `.../BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`
- Target 25.12 source:
  - `.../openwrt-25.12.4/target/linux/mediatek/filogic/base-files/etc/board.d/02_network`
  - `.../openwrt-25.12.4/package/network/services/dnsmasq/Makefile`
  - `.../openwrt-25.12.4/package/network/services/dnsmasq/patches/{001-CVE-2026-2291.patch,002-CVE-2026-4890.dnsmasq-2.91.patch,003-CVE-2026-4891.patch,004-CVE-2026-4892.patch,005-CVE-2026-4893.patch,006-CVE-2026-5172.patch,100-remove-old-runtime-kernel-support.patch,200-ubus_dns.patch}`
  - `.../openwrt-25.12.4/target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch`
- Relevant diff files inspected under `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/`:
  - `target/linux/mediatek/filogic/base-files/etc/board.d/02_network.patch`
  - `target/linux/mediatek/filogic/base-files/etc/config/network.patch`
  - `target/linux/mediatek/filogic/base-files/etc/config/firewall.patch`
  - `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts.patch`
  - `target/linux/mediatek/patches-6.6/999-2700-net-ethernet-mtk_eth_soc-add-mdio-reset-delay.patch.patch`
  - `target/linux/mediatek/patches-6.6/999-2704-net-ethernet-mtk_eth_soc-revise-mdc-divider-configur.patch.patch`
  - `target/linux/mediatek/patches-6.6/999-2707-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch.patch`
  - `target/linux/mediatek/patches-6.6/999-9800-mt7988a-bananapi-bpi-r4pro-support-multiple-dsa-switch-fixed.patch.patch`
  - `package/network/services/dnsmasq/Makefile.patch`
  - `package/network/services/dnsmasq/patches/0001-Fix-spurious-resource-limit-exceeded-messages.patch.patch`
  - `package/network/services/dnsmasq/patches/0002-PATCH-Fix-error-introduced-in-51471cafa5a4fa44d6fe49.patch.patch`
  - `package/network/services/dnsmasq/patches/0003-Handle-DS-queries-to-auth-zones.patch.patch`
  - `package/network/services/dnsmasq/patches/200-ubus_dns.patch.patch`
  - `package/network/config/netifd/files/usr/libexec/network/packet-steering.uc.patch`
  - `package/network/config/netifd/patches/mtk-0001-Revert-wireless-reload-wireless-device-if-any-vif-ne.patch.patch`

Structural Checks:
- Coverage count: JSON says 111 files / 115 assignments; TSV has 111 data rows; step-file-index has 111 M04 rows.
- Missing/extra/duplicates: none between TSV and JSON file IDs; no duplicate TSV file IDs; no duplicate M04 index file IDs.
- TSV schema: all rows have 12 fields.
- Diff artifact existence: all 111 TSV paths map to existing per-file diff artifacts.
- Disposition counts match markdown: defer 76, drop 23, needs-evidence 2, review-only 2, rewrite 2, superseded-by-target 6.
- Owner counts match markdown: M04 35, M05 17, M07 2, M08 53, M10 4.
- Disposition/owner legality: all disposition values are known; all owners are valid migration steps; all `defer` rows have non-M04 owners and TODO-bearing notes.
- JSON/TSV field match: file_id/status/path/file_kind/route_classes/features match exactly.
- JSON/index field match: same file set and same field values, except feature ordering for file_id `000960`.

Findings:
1. Minor handoff gap for file_id `001124`: M05 is correctly primary, but the row and markdown do not explicitly record the M08 secondary risk.
   - TSV line 112 classifies `001124` as `full-wired-pcs-dsa-sfp`, `defer`, owner `M05`, with no M08 secondary mention.
   - Markdown line 211 lists `001124` under M05 with only “M04 prerequisite only”.
   - The patch includes PPPQ/PPE/offload-relevant changes, e.g. QDMA/PPPQ queue mapping and DSA offsets at diff lines 42-58, PPE/DSA path changes at lines 188-201, and `mtk_ppe_offload.c` changes beginning at line 284.
   - Required edit: keep M05 as primary, but add M08 secondary risk/handoff for PPPQ/PPE/offload parts.

2. Minor structural mismatch: feature order for `000960` differs between by-step JSON and step-file-index.
   - JSON lines 1161-1203 order features as `bridge, wan, port-label, openwrt:board-d:network, vlan`.
   - Index line 546 orders them as `bridge, wan, port-label, vlan, openwrt:board-d:network`.
   - TSV line 47 follows the JSON order. This is a set-equivalent ordering mismatch only, but it fails strict exact JSON/index field matching.

No-Issue Confirmations:
- `000960`: direct 8X board.d source has `bananapi,bpi-r4-pro-8x` LAN `lan0 lan3 mxl_lan0 mxl_lan1 mxl_lan2 mxl_lan3 mxl_lan5` and WAN `eth1`; rewrite disposition is correct.
- `000963`: static network config is not accepted wholesale; the draft correctly excludes fixed ULA/IP and WWAN/cellular-style interfaces.
- `000859`: direct 8X DTS is used as M04 evidence only; M03/M05/M10 split is correctly stated.
- `001018` and `001022`: `needs-evidence` is correct; the vendor patches are not accepted from MTK SDK code alone.
- dnsmasq rows: `superseded-by-target` is supported by target 25.12 dnsmasq 2.91 plus current patch stack.
- forced-reset dump row `001025`: `superseded-by-target` is supported by target 25.12 `730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch`.
- No full DSA/SFP/10G, HNAT/WED/PPE/offload, Wi-Fi userspace, or storage behavior is pulled into M04 implementation scope.

Residual Risk:
- Implementation-time risk remains for 8X link enumeration, `eth1` management reachability, bridge membership, Factory MAC handling, and MDIO timing.
- Full MxL86252/DSA/SFP/10G validation remains M05 work.
- Acceleration/offload/PPPQ/PPE/WED risk remains M08 work, with `001124` needing explicit secondary handoff.
- Storage/rootdisk/env/sysupgrade implications remain M10 work.
