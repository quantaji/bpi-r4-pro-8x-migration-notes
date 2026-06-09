Verdict: accept-with-minor-edits

Evidence Read:
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/filogic/base-files/etc/board.d/02_network.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/filogic/base-files/etc/config/network.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-2700-net-ethernet-mtk_eth_soc-add-mdio-reset-delay.patch.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-2704-net-ethernet-mtk_eth_soc-revise-mdc-divider-configur.patch.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-9800-mt7988a-bananapi-bpi-r4pro-support-multiple-dsa-switch-fixed.patch.patch`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/target/linux/mediatek/patches-6.6/999-2707-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch.patch`
- dnsmasq diff files `0001`, `0002`, `0003`, `200-ubus_dns.patch.patch`, and `Makefile.patch`
- Direct vendor source: `02_network`, `etc/config/network`, `etc/config/firewall`, `mt7988a-bananapi-bpi-r4-pro-8x.dts`
- Target 25.12 source: `02_network`, dnsmasq `Makefile`, dnsmasq `patches/200-ubus_dns.patch`, `target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch`

Structural Checks:
- Coverage: TSV has 111 data rows; JSON `file_count` is 111 and `assignment_count` is 115; step-file-index has 111 M04 rows.
- Missing/extra/duplicates: none between JSON, TSV, and M04 index file IDs.
- JSON/TSV field match: file_id/status/path/file_kind/route_classes/features match.
- Index/TSV field match: set-equivalent, but one exact string-order mismatch for `000960` features. See Finding 2.
- Disposition counts match markdown: defer 76, drop 23, needs-evidence 2, review-only 2, rewrite 2, superseded-by-target 6.
- Owner counts match markdown: M04 35, M05 17, M07 2, M08 53, M10 4.
- Disposition/owner legality: no illegal owner/disposition combinations found; all defer rows point to non-M04 owners, and rewrite/needs-evidence/drop/review-only/superseded rows are M04-owned.

Findings:
1. Medium: `001124` needs an explicit M08 secondary-risk handoff.
   - `M04-basic-wired-management.md:211` lists `001124` as M05 with only “M04 prerequisite only”.
   - `M04-basic-wired-management.files.tsv:112` defers `001124` to M05 and mentions DSA/PPPQ, but the TODO only names M05 full-wired validation.
   - The diff directly touches PPPQ/QDMA queue mapping and offload paths: `999-9800...patch.patch:42`, `:101`, `:208`, `:451`, `:466`, `:526`.
   - Keep M05 as primary owner, but add M08 as secondary risk for PPPQ/QDMA/PPE/WED/offload portions.

2. Low: `000960` feature field ordering is not exact between step-file-index and TSV.
   - `step-file-index.tsv:546` orders features as `...network:vlan:bridge,openwrt:board-d:network`.
   - `M04-basic-wired-management.files.tsv:47` and JSON order them as `...openwrt:board-d:network,network:vlan:bridge`.
   - This is set-equivalent and not a coverage error, but it fails strict exact-string matching.

No-Issue Confirmations:
- `000960` direct 8X board.d evidence is valid. Vendor `02_network:196-197` sets `bananapi,bpi-r4-pro-8x` LAN to `lan0 lan3 mxl_lan0 mxl_lan1 mxl_lan2 mxl_lan3 mxl_lan5` and WAN to `eth1`. Vendor generic MAC helper uses Factory `0xFFFF4`/`0xFFFFA` at `02_network:323-326`, and direct DTS independently defines `gmac0_mac`/`gmac1_mac` at `dts:683-688`.
- `000963` is correctly not copied wholesale. Vendor static network config has the useful port evidence at `etc/config/network:11-33`, but also hard-coded ULA/IP and WWAN-style interfaces at `:8-9`, `:23-27`, `:43-62`.
- `000859` is correctly review-only M04 evidence. Direct DTS enables GMACs and MAC nvmem cells at `dts:149-169`, MDIO/C45 PHYs and MxL/SFP topology at `:182-358`, and storage/env content at `:658-717`; markdown splits these to M03/M05/M10.
- `001018` and `001022` are correctly `needs-evidence`: the patch texts add a fixed MDIO reset wait and move MDC divider configuration, but do not prove direct 8X runtime need.
- dnsmasq superseded-by-target rows are supported: target 25.12 carries dnsmasq 2.91 at target `Makefile:11-17` and current `200-ubus_dns.patch`.
- forced-reset dump superseded-by-target is supported by target `target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch:4-12` and implementation at `:44-101`.
- No full DSA/SFP/10G, HNAT/WED/offload, Wi-Fi userspace, or storage behavior is pulled into M04. The markdown excludes these at `M04-basic-wired-management.md:31-39` and defers them at `:139-145`, `:238-243`.

Residual Risk:
- M04 still has implementation-time risk around actual link enumeration, management reachability, `eth1` direct copper behavior, bridge membership, Factory MAC assignment, and MDIO timing.
- Full wired DSA/SFP/10G remains M05; Wi-Fi/userspace remains M07; acceleration/offload remains M08; storage/bootcount remains M10.
- No files were edited and no commit was made.
