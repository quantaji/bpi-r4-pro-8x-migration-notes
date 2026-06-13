# Migration Step M04 Batch Review: Basic Wired Management

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv`

This review is part of Project Phase 2. It does not migrate code.

## Audit Status

This file is the M04 round3-audited batch review.

Formal three-agent no-context audit status: completed through round 3 on 2026-06-08 PDT.

Round 1 verdicts: `accept-with-minor-edits`, `accept-with-minor-edits`, `accept-with-minor-edits`.

Round 2 verdicts: `accept-with-minor-edits`, `accept`, `accept`.

Round 3 verdicts: `accept`, `accept`, `accept`.

Minor edits from rounds 1 and 2 have been applied where accepted. Round 3 reported no actionable findings. The remaining `000960` feature-order difference is an upstream input artifact difference between by-step JSON and step-file-index; this TSV intentionally follows the by-step JSON exact order.

## Formal No-Context Audit Results

Round 1 completed on 2026-06-08 PDT.

| reviewer id | verdict | structural checks | findings summary | accepted/rejected changes |
| --- | --- | --- | --- | --- |
| `M04-audit-agent-1` | `accept-with-minor-edits` | Passed 111/111 coverage, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match; reported set-equivalent `000960` JSON/index feature-order difference. | `001124` should keep M05 primary but add M08 secondary risk; `000960` ordering differs between by-step JSON and step-file-index. | Accepted `001124` M08 secondary handoff. Rejected TSV reorder for `000960` because this matrix must match by-step JSON exactly. |
| `M04-audit-agent-2` | `accept-with-minor-edits` | Passed 111/111 coverage, no missing/extra/duplicate file ids, 12-column TSV schema, legal dispositions/owners, JSON/TSV exact match; reported set-equivalent `000960` JSON/index feature-order difference. | `001124` needs explicit M08 secondary handoff for PPPQ/PPE/offload hunks; `000960` ordering differs between by-step JSON and step-file-index. | Accepted `001124` M08 secondary handoff. Rejected TSV reorder for `000960` because this matrix must match by-step JSON exactly. |
| `M04-audit-agent-3` | `accept-with-minor-edits` | Passed 111/111 coverage, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match; reported set-equivalent `000960` JSON/index feature-order difference. | `001124` needs explicit M08 secondary-risk handoff; `000960` ordering differs between by-step JSON and step-file-index. | Accepted `001124` M08 secondary handoff. Rejected TSV reorder for `000960` because this matrix must match by-step JSON exactly. |

Round 2 completed on 2026-06-08 PDT.

| reviewer id | verdict | structural checks | findings summary | accepted/rejected changes |
| --- | --- | --- | --- | --- |
| `M04-audit-round2-agent-1` | `accept-with-minor-edits` | Passed 111/111 coverage, 115 assignments, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match. | `000961` wording said WWAN zones; source evidence is WWAN networks listed under the WAN zone. | Accepted wording clarification for `000961`; disposition remains `drop`. |
| `M04-audit-round2-agent-2` | `accept` | Passed 111/111 coverage, 115 assignments, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match. | No actionable findings. | No changes required. |
| `M04-audit-round2-agent-3` | `accept` | Passed 111/111 coverage, 115 assignments, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match. | No actionable findings. | No changes required. |

Round 3 completed on 2026-06-08 PDT.

| reviewer id | verdict | structural checks | findings summary | accepted/rejected changes |
| --- | --- | --- | --- | --- |
| `M04-audit-round3-agent-1` | `accept` | Passed 111/111 coverage, 115 assignments, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match, dense sampling across all required clusters. | No actionable findings. | No changes required. |
| `M04-audit-round3-agent-2` | `accept` | Passed 111/111 coverage, 115 assignments, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match, dense sampling across all TSV groups. | No actionable findings. | No changes required. |
| `M04-audit-round3-agent-3` | `accept` | Passed 111/111 coverage, 115 assignments, no missing/extra/duplicate file ids, legal dispositions/owners, JSON/TSV exact match, dense sampling across all required clusters. | No actionable findings. | No changes required. |

## Review Purpose

Migration Step M04 decides which vendor changes are needed for basic wired management on BPI-R4 Pro 8X.

M04 covers:

1. Ethernet MAC and MDIO basics needed before management over wired Ethernet,
2. direct 8X LAN/WAN defaults,
3. MAC address assignment for LAN/WAN,
4. basic bridge and WAN default configuration,
5. a direct copper management path as configuration/evidence only.

M04 does not cover:

1. full DSA switch behavior,
2. MxL86252 runtime validation,
3. SFP cages, SFP I2C, module detect, combo SFP/RJ45 mux runtime, or complete 10G behavior,
4. HNAT, PPE, WED, RSS/LRO, flow offload, PPPQ, or performance tuning,
5. Wi-Fi userspace/runtime behavior,
6. NAND/eMMC/rootdisk/env/sysupgrade/storage policy,
7. wired runtime success claims.

## Input Scope

M04 by-step input contains 111 files and 115 feature assignments.

Status split:

| status | file count |
| --- | ---: |
| `A` | 102 |
| `D` | 4 |
| `M` | 5 |

Route-class split:

| route class | assignment count |
| --- | ---: |
| `primary` | 105 |
| `supporting` | 10 |

These are feature-assignment route-class counts from the by-step JSON, not a count of distinct per-file `route_classes` values.

Feature split:

| feature | assignment count |
| --- | ---: |
| `network:default-config:bridge` | 1 |
| `network:default-config:wan` | 1 |
| `network:mac:mtk-eth` | 73 |
| `network:mdio:bus` | 19 |
| `network:port-label:lan-wan` | 1 |
| `network:vlan:bridge` | 1 |
| `openwrt:board-d:network` | 1 |
| `openwrt:firewall:defaults` | 1 |
| `openwrt:init:service` | 8 |
| `openwrt:network:defaults` | 9 |

Strict TSV scope:

1. The TSV contains exactly the 111 files from the M04 by-step JSON.
2. M00 and M03 handoffs are reviewed in this markdown when relevant but are not added as TSV rows unless they are also in the M04 JSON.
3. Direct 8X vendor source is authoritative for 8X hardware behavior. MT7988 RFB, MT7987, BPI-R4 Lite, MTK SDK, and target 25.12 files are supporting or structure references only.

Prior-step handoff check:

1. M00 handed Ethernet MAC, MDIO, and basic wired patch groups to M04. This draft reviewed those patches and split them by M04, M05, and M08 boundaries rather than treating the broad `network:mac:mtk-eth` tag as one migration instruction.
2. M03 handed Factory MAC cell evidence and direct 8X base DTS network/MAC context to M04. `000859` is in the M04 TSV as review-only evidence.
3. M03 handed `000960` Factory MAC context and LAN/WAN assignment to M04. `000960` is the primary M04 board.d row.
4. M03 treated `001003` as Factory MAC offset evidence for M04/M05, but `001003` is not in the M04 by-step input and is therefore recorded here only as an off-matrix handoff.

## Direct 8X Evidence

Direct 8X board.d network file:

`target/linux/mediatek/filogic/base-files/etc/board.d/02_network`

Key evidence checked:

1. The direct 8X board case is `bananapi,bpi-r4-pro-8x`.
2. Vendor `02_network` has a direct `bananapi,bpi-r4-pro-8x` board case that sets LAN ports to `lan0 lan3 mxl_lan0 mxl_lan1 mxl_lan2 mxl_lan3 mxl_lan5` and WAN to `eth1`.
3. The direct 8X DTS, not the generic `mediatek,mt7988*` board.d case alone, is the authoritative Factory MAC evidence for `gmac0_mac` at `0xffff4` and `gmac1_mac` at `0xffffa`.
4. The generic vendor MT7987/MT7988 switch-detection and MAC helper cases are supporting context only and should not be copied as the M04 design.

Direct 8X base DTS:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`

Key evidence checked:

1. `gmac0`, `gmac1`, and `gmac2` are enabled and consume Factory nvmem MAC cells.
2. Factory nvmem cells are `gmac0_mac` at `0xffff4`, `gmac1_mac` at `0xffffa`, and `gmac2_mac` at `0xfffee`.
3. `gmac1` is connected to `phy28` with 10GBase-R semantics and is the vendor WAN interface in `02_network`.
4. `gmac2` is connected to the MxL86252 DSA switch CPU port via fixed 10G link.
5. MxL86252 ports, SFP cages, AS21xxx firmware, GPIO switch reset, and combo mux topology are real 8X evidence, but their runtime validation belongs to M05.
6. SPI-NAND Factory/rootdisk/env content in the same DTS belongs to M10.

Direct 8X static network config:

`target/linux/mediatek/filogic/base-files/etc/config/network`

This file repeats the 8X br-lan port set and `br-wan` over `eth1`, but it also hard-codes ULA, `192.168.1.1`, WWAN/WWAN6/cellular-style interfaces, and a static target config file. M04 may use the wired port-group evidence, but the migration should be expressed through target-style board defaults, not by copying the whole static config.

Direct 8X firewall file:

`target/linux/mediatek/filogic/base-files/etc/config/firewall`

This file is broad policy and opens WAN input/forward while listing WWAN networks under the WAN zone. It is not 8X hardware truth and should not be migrated as M04 wired management.

Target OpenWrt 25.12 structure evidence:

1. Target 25.12 `02_network` has BPI-R4/BPI-R4 Lite examples and generic mediatek network-default style, but no direct 8X board case.
2. Target 25.12 already carries dnsmasq 2.91-era package state and current patches, so vendor dnsmasq refresh files are superseded by target.
3. Target 25.12 carries MT7987 Ethernet support patches as target structure/reference; they do not establish 8X hardware truth.
4. Target 25.12 has a comparable mtk_eth forced-reset dump patch, so the vendor diagnostic dump patch is not a M04 migration input.

## Routing Conclusions

1. `000960` is the core M04 input and should be rewritten into target 25.12 board.d style, using direct 8X DTS nvmem cells for MAC-offset evidence where explicit LAN/WAN MAC assignment is needed.
2. `000963` supports the same 8X wired port grouping, but the static config file must not be copied wholesale.
3. `000859` is direct 8X DTS evidence for GMAC/MDIO/MAC cells, but M03 owns the DTS rewrite and M05/M10 own its full wired/storage content.
4. `001018` and `001022` are the only M04 `needs-evidence` Ethernet driver rows: MDIO reset delay and MDC divider behavior may matter for 8X management, but cannot be accepted from MTK SDK code alone.
5. MT7987, BPI-R4 Lite, and MT7988 RFB files are not direct 8X authority; MT7987/R4Lite rows are dropped and RFB wired rows are deferred to M05 as supporting references.
6. PCS, XGMAC force mode, passive mux, EEE, SFP debug, multiple DSA, MxL86252, and 10G runtime behavior are deferred to M05.
7. HNAT, PPE, WED, RSS/LRO, jumbo frame, QDMA/PPPQ, flow offload, and performance tuning are deferred to M08.
8. reset-boot-count is deferred to M10, and wireless/netifd/RSNO userspace policy is deferred to M07.
9. No wired runtime success, SFP success, DSA success, 10G success, offload success, or storage behavior is claimed.

## Disposition Summary

| disposition | file count |
| --- | ---: |
| `defer` | 76 |
| `drop` | 23 |
| `needs-evidence` | 2 |
| `review-only` | 2 |
| `rewrite` | 2 |
| `superseded-by-target` | 6 |

Owner-step summary:

| owner_step | file count |
| --- | ---: |
| `M04` | 35 |
| `M05` | 17 |
| `M07` | 2 |
| `M08` | 53 |
| `M10` | 4 |

Group summary:

| group | file count |
| --- | ---: |
| `acceleration-performance-ppe-wed` | 42 |
| `basic-mdio-needs-evidence` | 2 |
| `direct-8x-boardd-network-defaults` | 1 |
| `direct-8x-dts-network-context` | 1 |
| `direct-8x-network-config-evidence` | 1 |
| `dnsmasq-version-sync` | 5 |
| `ethernet-mux-refactor` | 1 |
| `full-wired-pcs-dsa-sfp` | 11 |
| `hnat-driver-acceleration` | 9 |
| `mt7987-ethernet-driver-reference` | 2 |
| `mt7988-rfb-wired-reference` | 5 |
| `mtk-eth-forced-reset-dump` | 1 |
| `mtk-eth-probe-cleanup` | 1 |
| `mtk-eth-proprietary-debugfs` | 4 |
| `non-8x-mt7987-wired-reference` | 12 |
| `non-wired-optee-init` | 1 |
| `packet-steering-generic-netifd` | 2 |
| `pppq-acceleration-init` | 1 |
| `relayd-generic-init` | 1 |
| `reset-boot-count-storage-init` | 4 |
| `ser-monitor-runtime-robustness` | 1 |
| `vendor-firewall-policy` | 1 |
| `wifi-userspace-policy` | 1 |
| `wireless-netifd-policy` | 1 |

## Secondary Review Handoffs

The TSV schema has one `owner_step` per file. Mixed-owner files are therefore kept under their primary owner and called out here.

| file_id | primary owner | required secondary review | reason |
| --- | --- | --- | --- |
| `000490`-`000493` | `M10` | `M02` context | reset-boot-count is boot/storage policy, not M04 wired management. |
| `000496` | `M07` | none | netifd wireless reload policy belongs to wireless userspace review. |
| `000825` | `M08` | `M04` prerequisite only | PPPQ/EBL acceleration must wait for base wired path. |
| `000826` | `M07` | none | RSNO/MLO wireless policy belongs to wireless userspace review. |
| `000859` | `M04` review-only | `M03`, `M05`, `M10` | M03 owns DTS rewrite; M04 uses GMAC/MAC evidence; M05 owns MxL/SFP/10G; M10 owns storage/env. |
| `000861`, `000865`, `000868`, `000869`, `000876` | `M05` | M04 evidence only | same-SoC RFB wired overlays may help M05 but cannot decide 8X M04 hardware truth. |
| `000960` | `M04` | `M05`, `M10` | M04 owns LAN/WAN/MAC defaults; MxL/SFP runtime and storage/env implications remain later work. |
| `000963` | `M04` | `M07`, `M09` | wired port grouping is M04 evidence; WWAN/cellular-style interfaces are not M04. |
| `001015`, `001016`, `001020`, `001021`, `001026`, `001031`, `001032`, `001038`, `001046`, `001076` | `M05` | `M04` prerequisite only | full wired PCS/XGMAC/SFP/DSA behavior depends on basic network defaults but is not M04. |
| `001124` | `M05` | `M08`, `M04` prerequisite only | multiple DSA switch behavior is M05 primary; PPPQ/QDMA/PPE/offload hunks require M08 secondary review. |
| `001018`, `001022` | `M04` | `M05` if PHY-specific | MDIO reset/MDC divider evidence may affect basic enumeration, but PHY/switch runtime details belong to M05. |
| `001027`-`001047` acceleration/performance subset | `M08` or `M05` per TSV | `M04` prerequisite only | broad mtk_eth_soc tag contains performance/offload/full-wired behavior that must not be pulled into M04. |
| `001060`-`001122` HNAT/PPE/WED subset | `M08` | `M04`, `M06` prerequisites | acceleration/offload requires stable base wired and Wi-Fi behavior first. |
| `001003` | off-matrix M03 handoff | `M04`, `M05` | supports Factory MAC offset polarity but is not in the M04 by-step JSON/TSV. |

## TODOs

1. Migration Step M04: rewrite `000960` into target 25.12 board.d style for `bananapi,bpi-r4-pro-8x` LAN/WAN defaults and any explicit Factory MAC assignment needed from direct DTS nvmem evidence.
2. Migration Step M04: use `000963` only as supporting wired port-group evidence; do not add the vendor static `etc/config/network` file or its WWAN/cellular interfaces.
3. Migration Step M04: validate direct 8X MDIO bus and PHY enumeration before accepting or rejecting `001018` and `001022`.
4. Migration Step M04: keep target dnsmasq and firewall defaults unless direct runtime evidence proves a board-specific need.
5. Migration Step M05: validate MxL86252, DSA tagging, SFP cages, AS21xxx firmware, PCS/XGMAC force mode, passive mux, EEE, and 10G runtime behavior.
6. Migration Step M07: review wireless netifd reload and RSNO/MLO policy rows outside M04.
7. Migration Step M08: review HNAT/PPE/WED/RSS/LRO/QDMA/PPPQ/jumbo/performance patches only after base wired and Wi-Fi paths are stable, including the PPPQ/QDMA/PPE/offload portions of `001124`.
8. Migration Step M10: review reset-boot-count with persistent env/storage/sysupgrade policy.

## Unreported Minimalism Gate

Result: passed for the M04 round3-audited review after content checks.

Minimalism risks checked:

1. Direct 8X `02_network`, direct 8X base DTS, and direct 8X static network/firewall files were inspected before assigning M04 core dispositions.
2. `000960` was not copied wholesale; the draft requires a target-style rewrite and rejects generic vendor MT7987/MT7988 switch-detection and MAC helper cases as direct 8X truth.
3. `000963` was not accepted as an easy static config copy; only its wired port grouping is M04 evidence.
4. MT7987, BPI-R4 Lite, and RFB files were not promoted to 8X authority.
5. Broad `network:mac:mtk-eth` patches were split into M04 needs-evidence, M05 full-wired, M08 acceleration/performance, target-superseded diagnostics, or drops.
6. HNAT/WED/PPE/offload behavior was not pulled into M04.
7. Full DSA/SFP/10G behavior was not pulled into M04.
8. reset-boot-count, Wi-Fi userspace policy, and storage policy were assigned to later owner steps.
9. Every `defer` and `needs-evidence` row has a named owner and an actionable TODO in the TSV notes and this markdown.
10. No runtime wired success claim is made.

## Remaining Risk

Formal three-agent no-context audit rounds 1, 2, and 3 are completed, with accepted minor edits applied.

M04 implementation-time risk remains for actual link enumeration, management reachability, `eth1` direct copper behavior, bridge membership, Factory MAC assignment, and MDIO timing. Full wired behavior is deferred to M05, wireless/userspace policy to M07, acceleration/offload to M08, and storage/bootcount policy to M10.
