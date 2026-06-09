Verdict: accept-with-minor-edits

Evidence Read:
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Diff files inspected: `target/linux/mediatek/filogic/base-files/etc/board.d/02_network.patch`, `target/linux/mediatek/filogic/base-files/etc/config/network.patch`, `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts.patch`, dnsmasq `Makefile.patch`, dnsmasq deleted/modified patch rows `0001`, `0002`, `0003`, `200-ubus_dns`, and M04-risk patches `999-2700`, `999-2704`, `999-2707`, `999-9800`.
- Direct 8X vendor source inspected: `.../target/linux/mediatek/filogic/base-files/etc/board.d/02_network`, `.../etc/config/network`, `.../etc/config/firewall`, `.../target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`.
- Target 25.12 source inspected: `.../target/linux/mediatek/filogic/base-files/etc/board.d/02_network`, `.../package/network/services/dnsmasq/Makefile`, `.../package/network/services/dnsmasq/patches/200-ubus_dns.patch`, dnsmasq patch directory, `.../target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch`, and mediatek `patches-6.12` search results.

Structural Checks:
- Coverage: JSON has 111 files and 115 feature assignments; TSV has 111 data rows; step-file-index has 111 M04 rows.
- Status counts match draft: A=102, D=4, M=5.
- Disposition counts: defer=76, drop=23, needs-evidence=2, review-only=2, rewrite=2, superseded-by-target=6.
- Owner counts: M04=35, M05=17, M07=2, M08=53, M10=4.
- Missing/extra/duplicates: no missing TSV rows vs JSON, no extra TSV rows vs JSON, no duplicate file_ids, no duplicate paths.
- JSON/TSV field match: exact match for file_id, status, path, file_kind, route_classes, and feature order.
- TSV/index field match: one ordering-only mismatch for file_id `000960`; same feature set, but TSV/JSON order differs from step-file-index order.
- Disposition/owner legality: all dispositions are in the expected set; all owner_step values are legal for this draft.

Findings:
1. Minor: file_id `001124` needs an explicit M08 secondary handoff. TSV line 112 assigns `001124` to M05 with only an M05 TODO, and markdown line 211 lists it as M05 with “M04 prerequisite only.” That is directionally right for multiple-DSA/full-wired primary ownership, but the patch also contains PPPQ/PPE/offload work: the diff adds DSA PPPQ offset handling at `.../999-9800-mt7988a-bananapi-bpi-r4pro-support-multiple-dsa-switch-fixed.patch.patch:42`, changes PPE DSA tagging at line 208, and changes flow/offload queue selection around lines 451-496. Add M08 as a secondary review risk for `001124`; keep M05 primary.
2. Minor structural: file_id `000960` feature ordering differs between artifacts. TSV line 47 and JSON lines 1164/1188/1196 put `openwrt:board-d:network` before `network:vlan:bridge`; step-file-index line 546 puts `network:vlan:bridge` before `openwrt:board-d:network`. This is not semantic, but an exact-field audit should either normalize feature ordering or update the TSV/JSON/index generator expectation.

No-Issue Confirmations:
- `000960`: direct 8X board.d evidence is valid for LAN/WAN: vendor `02_network` lines 196-197 set LAN to `lan0 lan3 mxl_lan0 mxl_lan1 mxl_lan2 mxl_lan3 mxl_lan5` and WAN to `eth1`. MAC evidence is correctly tied to direct 8X DTS nvmem cells, not treated as generic MT7988 board.d truth.
- `000963`: static vendor network config is not accepted wholesale; TSV line 49 and markdown lines 138/220 correctly limit it to wired port-group evidence and exclude static ULA, fixed `192.168.1.1`, and WWAN/cellular interfaces.
- `000859`: direct 8X DTS is correctly review-only for M04 evidence. The draft preserves the M03/M05/M10 split: M04 uses GMAC/MAC/MDIO evidence, M05 owns MxL/SFP/10G/DSA runtime, and M10 owns storage/env/rootdisk.
- `001018` and `001022`: both are correctly marked `needs-evidence`; the patches change MDIO reset delay and MDC divider behavior, and the draft does not accept them from MTK SDK code alone.
- dnsmasq rows `000504`-`000508`: superseded-by-target is supported. Vendor diffs are a 2.90 to 2.91 refresh plus patch deletion/rebase; target 25.12 already has dnsmasq 2.91 and a current patch stack.
- forced-reset row `001025`: superseded-by-target is supported by target `target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch`.
- No full DSA/SFP/10G, HNAT/WED/PPE/offload, Wi-Fi userspace, or storage behavior is pulled into M04 as an implementation requirement.

Residual Risk:
- No hardware/runtime validation was performed. M04 still carries real implementation risk around 8X link enumeration, management reachability over `eth1`, bridge membership, Factory MAC assignment behavior, and MDIO timing.
- After the two minor edits above, I would accept the M04 draft for coordinator use.
