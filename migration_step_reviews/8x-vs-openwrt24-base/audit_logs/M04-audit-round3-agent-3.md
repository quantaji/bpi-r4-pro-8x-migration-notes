Verdict: accept

Evidence Read:
- Review artifacts inspected: `migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.md`; `migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv`.
- Rules/input indexes inspected: `rules/disposition-tags-v1.json`; `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json`; `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`.
- Diff files inspected: per-file diffs for `000490`, `000494`, `000496`, `000504`, `000505`, `000507`, `000508`, `000830`, `000859`, `000861`, `000896`, `000960`, `000961`, `000963`, `001003`, `001018`, `001022`, `001025`, `001027`, `001124` under `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files/`.
- Direct 8X/vendor source inspected: vendor `target/linux/mediatek/filogic/base-files/etc/board.d/02_network` lines 196-197 and 362-364; vendor `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts` lines 149-168, 182, 213, 242, 275-330, 649-688; vendor `target/linux/mediatek/filogic/base-files/etc/config/network` lines 9-59; vendor `target/linux/mediatek/filogic/base-files/etc/config/firewall` lines 12-26; vendor patch/source files for sampled kernel/netifd/dnsmasq/reset/RFB/MT7987/HNAT/RSS rows.
- Target 25.12 source inspected: target dnsmasq `Makefile` lines 10-17; target dnsmasq `patches/200-ubus_dns.patch` lines 1-30 and 169-278; target dnsmasq patch directory listing; target generic forced-reset dump patch `target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch` lines 4-7, 44-90, 101-104; target netifd packet steering init lines 3-23.

Structural Checks:
- TSV schema: pass. Header is the expected 12 columns at TSV line 1.
- Coverage: pass. TSV has 111 rows, 111 unique `file_id`s, no missing/extra/duplicate IDs against the M04 by-step JSON.
- Assignment count: pass. JSON reports 111 files / 115 assignments; computed JSON feature assignments also 115.
- Field match: pass. TSV `status`, `path`, `file_kind`, `features`, and `route_classes` match the M04 by-step JSON exactly. `000960` follows JSON feature order: JSON lines 1164, 1172, 1180, 1188, 1196 match TSV line 47.
- Step index: pass with documented upstream-input difference. M04 rows in `step-file-index.tsv` are also 111 files / 115 assignments; the only index-vs-JSON mismatch is `000960` feature order, already documented in markdown line 21.
- Dispositions: pass. All TSV dispositions are legal under `rules/disposition-tags-v1.json`.
- Owners/TODOs: pass. Owner steps are legal (`M04`, `M05`, `M07`, `M08`, `M10`). All `defer` and `needs-evidence` rows have named owners and TODO text; no `static-only` rows are present.
- Markdown counts: pass. Markdown input scope says 111 files / 115 assignments at lines 63-65; status split lines 69-73 matches JSON/TSV; disposition and owner summaries at lines 171-188 match TSV.
- Audit bookkeeping: pass. Markdown records round 1 and round 2 summaries at lines 15-35 and says rounds 1/2 completed at line 270. It does not claim round 3 completion.

Dense Sampling Coverage:
- Direct 8X evidence/action rows: sampled `000960`, `000963`, `000859`.
- M04 needs-evidence rows: sampled `001018`, `001022`.
- Superseded-by-target rows: sampled dnsmasq `000504`, `000508`, plus deleted dnsmasq patch rows `000505`/`000507` by diff/source context, and `001025`.
- M05 defer rows: sampled `001124` and RFB row `000861`.
- M08 defer rows: sampled HNAT row `000896` and RSS/LRO row `001027`.
- M07 defer rows: sampled `000496`.
- M10 defer rows: sampled `000490`.
- Drop rows: sampled non-8X MT7987 DTS row `000830` and generic service row `000494`.
- Expansion: no sampled mismatch required full-cluster expansion. `001025` required only a wider target-source search before acceptance because the comparable patch lives under target `generic/hack-6.12`, not `mediatek/patches-6.12`.

Findings:
- No blocking or minor findings.

No-Issue Confirmations:
- `000960`: TSV line 47 correctly marks M04 rewrite. Direct vendor board.d has the `bananapi,bpi-r4-pro-8x` case setting LAN to `lan0 lan3 mxl_lan0 mxl_lan1 mxl_lan2 mxl_lan3 mxl_lan5` and WAN to `eth1` at vendor `02_network` lines 196-197. The TSV feature order matches by-step JSON, not the global index.
- `000963`: TSV line 49 correctly uses the static config only as evidence. Vendor network config repeats `br-lan` ports and `br-wan` over `eth1` at lines 11-36, but also contains static ULA/IP and WWAN/cellular-style devices at lines 9, 24-26, 45-59, so wholesale copy rejection is correct.
- `000859`: TSV line 30 correctly marks direct 8X DTS as M04 review-only evidence with M03/M05/M10 split. DTS enables `gmac0`/`gmac1`/`gmac2` with nvmem cells at lines 149-168; MxL/SFP/full wired evidence appears at lines 98-143 and 242-330; Factory MAC cells are at lines 679-688; SPI-NAND/Factory context starts at lines 649-671.
- `001018` and `001022`: TSV lines 52 and 55 correctly keep both as `needs-evidence`. Vendor `001018` adds `mtk_mdio_reset()` and `mdelay(150)` at patch lines 18-35. Vendor `001022` moves MDC divider setup into `mtk_hw_init()` at lines 4-8 and 101-107. These are plausible MDIO basics but not proven by direct 8X runtime evidence.
- `001124`: TSV line 112 and markdown line 234 correctly keep M05 primary with M08 secondary. Vendor patch contains DSA/multiple-switch logic and PPPQ offsets at lines 42-57, QDMA queue changes at lines 142-149, PPE/offload changes at lines 183-211 and 278-490.
- `001003`: markdown line 238 correctly records it as off-matrix M03 handoff, not a TSV row. Vendor patch fixes `gmac1_mac` to `0xffffa` and `gmac0_mac` to `0xffff4` at lines 25-32, matching direct DTS lines 683-688.
- Superseded rows: dnsmasq TSV lines 10-14 are supported by target dnsmasq 2.91 evidence at target Makefile lines 10-17 and current target patch stack, including `200-ubus_dns.patch`. `001025` TSV line 58 is supported by target generic forced-reset dump patch lines 4-7, 44-90, and 101-104.
- Boundary checks passed: M04 does not pull in full DSA/SFP/10G runtime, HNAT/WED/PPE/offload, Wi-Fi userspace, storage/sysupgrade, reset-boot-count policy, or runtime success claims. Markdown minimalism checks at lines 257-266 are consistent with sampled source.

Residual Risk:
- M04 implementation still needs real 8X runtime validation for link enumeration, wired management reachability, `eth1` copper WAN behavior, bridge membership, Factory MAC assignment behavior, and MDIO timing.
- Deferred later work remains real but is not an M04 matrix defect: M05 full wired/DSA/SFP/10G, M07 wireless userspace policy, M08 acceleration/offload/performance, and M10 reset-boot-count/storage/sysupgrade.
