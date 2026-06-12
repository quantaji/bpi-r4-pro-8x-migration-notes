# Migration Step M07 Batch Review: Wireless Userspace, MLO, AFC, And Policy

Diffset: `8x-vs-openwrt24-base`

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M07-wireless-userspace-mlo-afc-and-policy.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.files.tsv`

This review is part of Project Phase 2. It does not migrate code, compile images, or claim Wi-Fi/AP/MLO/AFC/DFS/runtime success.

## Audit Status

This file is the M07 round1-audited batch review rebuilt from scratch after rejecting the earlier failed draft as classification evidence.

Formal round1 no-context audit status: completed on 2026-06-12 with four independent agents.

Round1 verdicts: M07-audit-round1-agent-1 `accept-with-minor-edits`; M07-audit-round1-agent-2 `accept-with-minor-edits`; M07-audit-round1-agent-3 `revise-before-accept`; M07-audit-round1-agent-4 `accept-with-minor-edits`.

Agent-3's `review-only` disposition finding was rejected as a false positive because `rules/disposition-tags-v1.json` explicitly allows `review-only`. The actionable round1 minor edits were accepted and addressed: route-class count wording, `000300` unassigned-radio provenance hazard, `000622` WDS uninitialized-name risk, `000330` related-but-not-same-path target radio-mask wording, and `000534` target UAPI/upstream-source comparison wording.

## Scope / Non-goals

M07 covers wireless userspace and policy: wifi-scripts/netifd/ucode, hostapd/wpa_supplicant build and policy, MLO/MLD/link handling, TTLM/eMLSR/EPCS/QoS, AFC/LPI/6 GHz/regulatory, DFS/CSA/background radar/offchain behavior, mac80211/cfg80211/nl80211 policy interfaces, iw tooling, and OpenWrt patch-stack churn that affects those areas.

M07 does not cover M06 Wi-Fi hardware enumeration, firmware/calibration/EEPROM/PCIe bring-up; M08 WED/HNAT/PPE/offload; M09 generic PCIe/USB expansion; M10 storage/install/sysupgrade; or runtime success. Broad route tags are not treated as migration instructions.

## Structural Summary

M07 by-step input contains 600 files and 892 feature assignments.

Status split:

| status | count |
| --- | ---: |
| `A` | 334 |
| `D` | 250 |
| `M` | 11 |
| `R053` | 1 |
| `R057` | 1 |
| `R069` | 1 |
| `R074` | 1 |
| `R082` | 1 |

Route-class counts:

JSON top-level `class_counts` are assignment-level:

| route class | assignments |
| --- | ---: |
| `primary` | 302 |
| `review-only` | 590 |

TSV `route_classes` are collapsed file-level memberships:

| route class | files |
| --- | ---: |
| `primary` | 170 |
| `review-only` | 590 |

File-kind split:

| file_kind | count |
| --- | ---: |
| `header` | 6 |
| `makefile` | 2 |
| `patch` | 576 |
| `script` | 5 |
| `shell` | 3 |
| `source` | 6 |
| `unknown` | 2 |

Feature split:

| feature | count |
| --- | ---: |
| `wireless:hostapd:build` | 277 |
| `wireless:hostapd:ucode` | 12 |
| `wireless:mac80211:patch` | 313 |
| `wireless:mlo:config` | 117 |
| `wireless:mlo:runtime` | 124 |
| `wireless:regulatory:db` | 35 |
| `wireless:wifi-scripts:netifd` | 7 |
| `wireless:wifi-scripts:ucode` | 7 |

Disposition summary:

| disposition | count |
| --- | ---: |
| `defer` | 20 |
| `drop` | 140 |
| `needs-evidence` | 301 |
| `review-only` | 40 |
| `superseded-by-target` | 99 |

Owner-step summary:

| owner_step | count |
| --- | ---: |
| `M07` | 580 |
| `M08` | 3 |
| `M11` | 17 |

## Topic Coverage Table

| group | rows | disposition counts | owner counts |
| --- | ---: | --- | --- |
| `M07-B-ordinary-ap-userspace` | 7 | `needs-evidence` 7 | `M07` 7 |
| `M07-E-afc-lpi-6ghz-regulatory` | 3 | `needs-evidence` 3 | `M07` 3 |
| `M07-hostapd-AFC-daemon-client-TPE-LPI-regulatory` | 8 | `needs-evidence` 8 | `M07` 8 |
| `M07-hostapd-DFS-CSA-background-radar-offchain` | 28 | `needs-evidence` 28 | `M07` 28 |
| `M07-hostapd-EMLSR` | 2 | `needs-evidence` 2 | `M07` 2 |
| `M07-hostapd-FT-over-MLD` | 9 | `needs-evidence` 9 | `M07` 9 |
| `M07-hostapd-MBSSID-beacon-RNR-BPCC` | 20 | `needs-evidence` 20 | `M07` 20 |
| `M07-hostapd-MLO-MLD-base` | 37 | `needs-evidence` 37 | `M07` 37 |
| `M07-hostapd-QoS-SCS-MSCS-EPCS` | 8 | `needs-evidence` 8 | `M07` 8 |
| `M07-hostapd-TTLM-A-TTLM-Neg-TTLM` | 6 | `needs-evidence` 6 | `M07` 6 |
| `M07-hostapd-WDS-4addr-extender` | 6 | `needs-evidence` 6 | `M07` 6 |
| `M07-hostapd-baseline-revert-sync-churn` | 4 | `needs-evidence` 2, `review-only` 2 | `M07` 4 |
| `M07-hostapd-link-add-remove` | 4 | `needs-evidence` 4 | `M07` 4 |
| `M07-hostapd-ordinary-AP-WPA-SAE-RSNO-config-generation` | 26 | `needs-evidence` 26 | `M07` 26 |
| `M07-hostapd-per-link-auth-deauth-key` | 17 | `needs-evidence` 17 | `M07` 17 |
| `M07-hostapd-target-superseded-or-deleted-openwrt-churn` | 68 | `defer` 5, `superseded-by-target` 63 | `M07` 63, `M11` 5 |
| `M07-hostapd-ucode-integration` | 12 | `needs-evidence` 12 | `M07` 12 |
| `M07-hostapd-vendor-command-certification-debug-controls` | 22 | `review-only` 22 | `M07` 22 |
| `M07-iw-iw-Rxxx-openwrt-buildflag-rename` | 1 | `superseded-by-target` 1 | `M07` 1 |
| `M07-iw-iw-Rxxx-renamed-churn` | 1 | `needs-evidence` 1 | `M07` 1 |
| `M07-iw-iw-Rxxx-survey-tooling-rename` | 1 | `superseded-by-target` 1 | `M07` 1 |
| `M07-iw-iw-Rxxx-vif-radio-mask-rename` | 1 | `superseded-by-target` 1 | `M07` 1 |
| `M07-iw-iw-deleted-target-missing-provenance-gap` | 1 | `needs-evidence` 1 | `M07` 1 |
| `M07-iw-iw-deleted-target-present-openwrt-churn` | 1 | `superseded-by-target` 1 | `M07` 1 |
| `M07-iw-iw-low-risk-tooling-cleanup` | 4 | `review-only` 4 | `M07` 4 |
| `M07-iw-iw-nl80211-header-sync` | 2 | `needs-evidence` 2 | `M07` 2 |
| `M07-iw-iw-validation-tooling-mlo-radio` | 12 | `review-only` 12 | `M07` 12 |
| `M07-mac80211-AFC-regulatory-6GHz-adjacent` | 1 | `needs-evidence` 1 | `M07` 1 |
| `M07-mac80211-DFS-CSA-radar-channel-policy` | 18 | `needs-evidence` 18 | `M07` 18 |
| `M07-mac80211-MLO-MLD-TTLM-EMLSR-core` | 18 | `needs-evidence` 18 | `M07` 18 |
| `M07-mac80211-Makefile-backports-baseline` | 1 | `superseded-by-target` 1 | `M07` 1 |
| `M07-mac80211-deleted-openwrt-churn` | 41 | `defer` 12, `needs-evidence` 1, `superseded-by-target` 28 | `M07` 29, `M11` 12 |
| `M07-mac80211-non-8X-driver-family/ath` | 8 | `drop` 8 | `M07` 8 |
| `M07-mac80211-non-8X-driver-family/ath10k` | 8 | `drop` 8 | `M07` 8 |
| `M07-mac80211-non-8X-driver-family/ath11k` | 8 | `drop` 8 | `M07` 8 |
| `M07-mac80211-non-8X-driver-family/ath12k` | 2 | `drop` 2 | `M07` 2 |
| `M07-mac80211-non-8X-driver-family/ath5k` | 5 | `drop` 5 | `M07` 5 |
| `M07-mac80211-non-8X-driver-family/ath9k` | 27 | `drop` 27 | `M07` 27 |
| `M07-mac80211-non-8X-driver-family/brcm` | 17 | `drop` 17 | `M07` 17 |
| `M07-mac80211-non-8X-driver-family/mt7601u` | 1 | `drop` 1 | `M07` 1 |
| `M07-mac80211-non-8X-driver-family/mwl` | 6 | `drop` 6 | `M07` 6 |
| `M07-mac80211-non-8X-driver-family/rt2x00` | 26 | `drop` 26 | `M07` 26 |
| `M07-mac80211-non-8X-driver-family/rtl` | 32 | `drop` 32 | `M07` 32 |
| `M07-mac80211-offload-WED-boundary` | 3 | `defer` 3 | `M08` 3 |
| `M07-mac80211-subsys-core-cfg80211-nl80211-mac80211` | 67 | `needs-evidence` 64, `superseded-by-target` 3 | `M07` 67 |

## Ordinary AP vs Advanced Wi-Fi 7 Split

Ordinary AP rows are not accepted wholesale. `000497`-`000503`, `000511`, `000512`, and the hostapd ordinary AP/config-generation subtopic are all `needs-evidence` unless target comparison proves an actual ordinary AP gap. MLO/MLD, TTLM/eMLSR/EPCS, AFC/LPI/6 GHz, DFS/CSA, vendor cert/debug, and iw tooling are separated so they cannot contaminate the minimal AP path.

## Hostapd Taxonomy

Hostapd rows: 277. All six remediation batches now use patch-body/source-body or target same-path/provenance evidence where applicable. High-risk rows are dense-read only where explicitly marked.

| subtopic | rows | sample ids | target true/false |
| --- | ---: | --- | --- |
| `AFC-daemon-client-TPE-LPI-regulatory` | 8 | `000510`, `000516`, `000518`, `000519`, `000520` | true=1, false=7 |
| `DFS-CSA-background-radar-offchain` | 28 | `000529`, `000532`, `000533`, `000535`, `000537` | true=0, false=28 |
| `EMLSR` | 2 | `000589`, `000697` | true=0, false=2 |
| `FT-over-MLD` | 9 | `000642`, `000665`, `000666`, `000668`, `000691` | true=0, false=9 |
| `MBSSID-beacon-RNR-BPCC` | 20 | `000547`, `000552`, `000597`, `000602`, `000609` | true=0, false=20 |
| `MLO-MLD-base` | 37 | `000568`, `000570`, `000571`, `000572`, `000575` | true=0, false=37 |
| `QoS-SCS-MSCS-EPCS` | 8 | `000546`, `000550`, `000551`, `000618`, `000671` | true=0, false=8 |
| `TTLM-A-TTLM-Neg-TTLM` | 6 | `000616`, `000656`, `000657`, `000658`, `000659` | true=0, false=6 |
| `WDS-4addr-extender` | 6 | `000574`, `000580`, `000622`, `000625`, `000626` | true=0, false=6 |
| `baseline-revert-sync-churn` | 4 | `000509`, `000513`, `000514`, `000534` | true=0, false=4 |
| `link-add-remove` | 4 | `000608`, `000632`, `000638`, `000639` | true=0, false=4 |
| `ordinary-AP-WPA-SAE-RSNO-config-generation` | 26 | `000517`, `000521`, `000522`, `000531`, `000542` | true=0, false=26 |
| `per-link-auth-deauth-key` | 17 | `000528`, `000562`, `000566`, `000567`, `000576` | true=0, false=17 |
| `target-superseded-or-deleted-openwrt-churn` | 68 | `000515`, `000612`, `000623`, `000721`, `000722` | true=64, false=4 |
| `ucode-integration` | 12 | `000511`, `000512`, `000556`, `000557`, `000594` | true=0, false=12 |
| `vendor-command-certification-debug-controls` | 22 | `000523`, `000524`, `000525`, `000526`, `000527` | true=0, false=22 |

Disposition policy: AFC, DFS, MLO/MLD, TTLM, ucode, ordinary AP, WDS/extender, per-link auth/key, MBSSID/beacon, and QoS rows default to `needs-evidence` until target comparison and runtime prerequisites are available. Vendor/cert/debug rows are `review-only`. Deleted target-present churn is `superseded-by-target`; target-missing release churn is `defer -> M11`.

## Mac80211 Taxonomy

Mac80211 rows: 289. Shared core rows were separated from non-8X driver-family rows. Non-8X family rows were sampled by family and are not 8X migration inputs.

| subtopic | rows | sample ids | target true/false |
| --- | ---: | --- | --- |
| `AFC-regulatory-6GHz-adjacent` | 1 | `000293` | true=0, false=1 |
| `DFS-CSA-radar-channel-policy` | 18 | `000247`, `000307`, `000219`, `000221`, `000229`, `000263` | true=0, false=18 |
| `MLO-MLD-TTLM-EMLSR-core` | 18 | `000279`, `000244`, `000248`, `000258`, `000272`, `000312` | true=0, false=18 |
| `Makefile-backports-baseline` | 1 | `000054` | true=1, false=0 |
| `deleted-openwrt-churn` | 41 | `000330`, `000130`, `000131`, `000132`, `000322`, `000342` | true=28, false=13 |
| `non-8X-driver-family/ath` | 8 | `000055`, `000056`, `000057`, `000059`, `000062` | true=8, false=0 |
| `non-8X-driver-family/ath10k` | 8 | `000063`, `000064`, `000065`, `000067`, `000070` | true=8, false=0 |
| `non-8X-driver-family/ath11k` | 8 | `000071`, `000072`, `000073`, `000075`, `000078` | true=4, false=4 |
| `non-8X-driver-family/ath12k` | 2 | `000079`, `000080` | true=1, false=1 |
| `non-8X-driver-family/ath5k` | 5 | `000081`, `000082`, `000083`, `000085` | true=5, false=0 |
| `non-8X-driver-family/ath9k` | 27 | `000086`, `000087`, `000088`, `000099`, `000112` | true=23, false=4 |
| `non-8X-driver-family/brcm` | 17 | `000113`, `000114`, `000115`, `000121`, `000129` | true=16, false=1 |
| `non-8X-driver-family/mt7601u` | 1 | `000145` | true=1, false=0 |
| `non-8X-driver-family/mwl` | 6 | `000146`, `000147`, `000148`, `000149`, `000151` | true=6, false=0 |
| `non-8X-driver-family/rt2x00` | 26 | `000152`, `000153`, `000154`, `000165`, `000177` | true=21, false=5 |
| `non-8X-driver-family/rtl` | 32 | `000178`, `000179`, `000180`, `000194`, `000209` | true=0, false=32 |
| `offload-WED-boundary` | 3 | `000225`, `000256`, `000289` | true=0, false=3 |
| `subsys-core-cfg80211-nl80211-mac80211` | 67 | `000210`, `000300`, `000211`, `000212`, `000255`, `000316` | true=0, false=67 |

Important correction: `000330` is not blindly deferred to M11. Same-path target is missing, and target mac80211 patch 350 is related radio-mask/radar-scan work rather than a same-path replacement for vendor deleted `330-wifi-cfg80211-add-option-for-vif-allowed-radios.patch`; related target evidence also exists in hostapd 370 and iw 310, so it remains `needs-evidence -> M07` pending direct target behavior comparison.

## Iw Tooling Taxonomy

Iw rows: 24. Target iw patch stack checked: `010-Revert-iw-allow-specifying-CFLAGS-LIBS-externally.patch`, `130-survey-bss-rx-time.patch`, `200-reduce_size.patch`, `310-vif_radio_mask.patch`.

| subtopic | rows | sample ids | target true/false |
| --- | ---: | --- | --- |
| `iw-Rxxx-openwrt-buildflag-rename` | 1 | `000799` | true=1, false=0 |
| `iw-Rxxx-renamed-churn` | 1 | `000795` | true=0, false=1 |
| `iw-Rxxx-survey-tooling-rename` | 1 | `000800` | true=1, false=0 |
| `iw-Rxxx-vif-radio-mask-rename` | 1 | `000801` | true=1, false=0 |
| `iw-deleted-target-missing-provenance-gap` | 1 | `000810` | true=1, false=0 |
| `iw-deleted-target-present-openwrt-churn` | 1 | `000809` | true=1, false=0 |
| `iw-low-risk-tooling-cleanup` | 4 | `000787`, `000789`, `000790`, `000791` | true=0, false=4 |
| `iw-nl80211-header-sync` | 2 | `000792`, `000808` | true=1, false=1 |
| `iw-validation-tooling-mlo-radio` | 12 | `000788`, `000793`, `000794`, `000796`, `000797` | true=0, false=12 |

Iw validation/config tooling is not runtime proof. Rxxx rows with target-equivalent OpenWrt tooling are `superseded-by-target`; `000810` remains `needs-evidence` because same-path target is missing and related radio-mask tooling must be compared.

## Deleted / Renamed / Churn Handling

Deleted rows are handled by target evidence and family context, not by status alone. Target-present OpenWrt churn is `superseded-by-target`. Target-missing release-validation churn is `defer -> M11`. Non-8X deleted driver-family rows are `drop` after representative sampling because direct 8X Wi-Fi is mt7996/mt76, not ath/brcm/mwl/rtl/rt2x00/mt7601u.

## Provenance Gaps

| area | representative rows | gap |
| --- | --- | --- |
| hostapd AFC packaging | `000509`, `000510`, `000516`-`000520` | vendor has AFC/afcd/CA/libcurl/libjson-c path; target hostapd is newer but lacks same AFC packaging |
| regulatory database | `000034`-`000036` | vendor regdb changes are not hardware truth and require regulatory/legal provenance |
| MLO/TTLM/eMLSR | `000571`, `000616`, hostapd/mac80211 MLO groups | target has partial/newer support; vendor MTK internal command stack cannot be replayed blindly |
| DFS/background radar | `000646`, `000655`, `000720`, mac80211 DFS rows | needs target behavior comparison and runtime validation after M06 |
| radio-mask tooling/API | `000330`, `000801`, `000810` | target has related radio-mask patches, but target mac80211 350 is not a same-path replacement for vendor `000330` |
| mac80211 provenance hazard | `000300` | vendor Felix sync has an unassigned-radio risk in one `ieee80211_chandef_radio_mask` hunk; target 350 assigns `radio` before validation |
| hostapd WDS cleanup | `000622` | vendor WDS crash fix may leave stack `name` uninitialized when `ifname_wds == NULL`; target WDS cleanup comparison is required |
| hostapd nl80211 header sync | `000534` | target package tree lacks same-path `src/drivers/nl80211_copy.h` comparison target; compare kernel UAPI and upstream/extracted hostapd source |
| WED/offload | `000225`, `000256`, `000289` | M08 owns hardware flow/offload semantics |

## High-risk Dense-read Coverage

The TSV currently contains `Dense-read` wording for 49 high-risk rows: `000034`, `000035`, `000036`, `000225`, `000256`, `000289`, `000330`, `000497`, `000498`, `000499`, `000500`, `000501`, `000502`, `000503`, `000509`, `000510`, `000511`, `000512`, `000516`, `000517`, `000518`, `000519`, `000520`, `000571`, `000616`, `000646`, `000655`, `000720`, `000787`, `000788`, `000789`, `000790`, `000791`, `000792`, `000793`, `000794`, `000795`, `000796`, `000797`, `000798`, `000801`, `000802`, `000803`, `000804`, `000805`, `000806`, `000807`, `000808`, `000810`.

High-risk evidence remediation is complete across six explicit main-agent batches; formal round1 x4 no-context audit is completed, with minor edits addressed after audit. Batch 1 is complete for `000034`-`000180`: `000034`-`000036` now record concrete regdb patch semantics, including world-domain 6 GHz/UNII-4 changes and `country VV` 2.4 GHz, 4.9 GHz, 5 GHz, 5030-5090 MHz, and 6 GHz rules. Non-8X mac80211 driver-family rows in this range are explicitly marked as group-level classification with representative patch-body reads by family, and deleted build/backports churn rows are based on target same-path presence plus sampled target body comparison rather than deletion status alone.

Batch 2 is complete for `000181`-`000330`: RTL rows now record representative rtw88/RTL USB patch-body semantics before being dropped as non-8X driver-family evidence; mac80211/cfg80211/nl80211 core rows now record concrete patch-body hunk behavior; DFS/CSA/radar rows now name CAC, NOP, CSA, background radar, MLO radar, and scan-relax behavior; MLO/MLD/TTLM/EMLSR rows now name the API or behavior they modify; `000225`, `000256`, and `000289` remain explicit M08 offload handoffs; and `000330` keeps M07 target radio-mask / vif-radio-mask provenance instead of being pushed to M11.

Batch 3 is complete for the M07 rows in `000331`-`000520` (31 TSV rows; `000343`-`000496` are not present in the M07 by-step input): `000331`-`000342` now use target same-path/source-presence checks or explicit provenance-gap wording rather than deletion status; `000497`-`000503` now record individual wifi-scripts hunks for ordinary AP config, RSNO/SAE-ext, EHT detection, hardcoded EHT capability, 320 MHz width, MLD/radio-mask, and runtime-policy contamination; `000509` now records the hostapd Makefile source-date/version delta, AFC/afcd packaging, libcurl/json-c dependencies, CA install, build flags, and target-first policy; `000510`-`000512` now record AFC CA and hostapd/wpa_supplicant ucode behavior; `000513`-`000515` are documented as broad revert/sync/churn carriers and are not replayed over target; and `000516`-`000520` now record concrete AFCD, AFC client, channel/TPE, LPI/6 GHz semantics. Later high-risk rows were covered in subsequent remediation batches and round1 audit.

Batch 4 is complete for `000521`-`000620`: early/mid hostapd patch-stack rows now record inner patch-body semantics instead of generic triage; ordinary AP/WPA/SAE/RSNO rows are separated from MLO/MLD, DFS/CSA/background radar, MBSSID/RNR, QoS/SCS, WDS/4addr, ucode integration, AFC/LPI/txpower, and vendor debug/cert controls; vendor MU/AMSDU/available-color/no_beacon/CSI rows were narrowed to `review-only`; `000571` keeps a concrete `mld_primary` Dense-read record; `000616` keeps a concrete A-TTLM Dense-read record covering `SET_ATTLM`, disabled_links/switch_time/duration, driver events, beacon advertisement, and critical-update behavior; broad API/churn row `000534` is target-first provenance only and must compare target kernel UAPI plus upstream/extracted hostapd source because target lacks same-path `src/drivers/nl80211_copy.h`; and no row claims AP/MLO/AFC/DFS runtime success. Later high-risk rows were covered in subsequent remediation batches and round1 audit.

Batch 5 is complete for `000621`-`000720`: hostapd patch-stack rows now record inner patch-body semantics instead of generic triage; DFS/offchain/background radar/detect-mode rows name the ctrl_iface, hostapd_cli, DFS state-machine, and driver/vendor command paths; `000646`, `000655`, and `000720` keep concrete Dense-read records; TTLM/A-TTLM/Neg-TTLM, MLO/MLD lifecycle, FT-over-MLD, MBSSID/RNR/BPCC, QoS/MSCS/EPCS, WDS/extender, ucode radio-mask, and ordinary AP/auth rows are separated; `000622` now records the WDS uninitialized-name risk instead of treating the vendor patch as a complete fix; vendor Air Monitor, BSS color, EDCCA, cert, and compile-only controls are narrowed to `review-only`; and no row claims AP/MLO/AFC/DFS runtime success. Batch 6 is now complete; formal round1 x4 no-context audit is completed and minor edits are addressed.

Batch 6 is complete for `000721`-`000810` and is the final main-agent remediation batch: actual TSV coverage is 89 rows (`000721`-`000785` plus `000787`-`000810`; no `000786` exists). Hostapd deleted/churn rows now distinguish target same-path OpenWrt-owned patch/source evidence from target-missing provenance gaps (`000746`, `000773`, `000782`, `000783` remain `defer -> M11`). iw rows now record concrete patch-body semantics for puncturing, HE scan decode, nl80211 header/API sync, VIF radio mask, per-link bitrate/txpower/offchannel, station/link dump, per-radio antenna/radio-mask scan tooling, target-equivalent OpenWrt patches, and the target-missing `300-wiphy_radios.patch` provenance gap. `000801` was added to Dense-read coverage because it is the high-risk VIF radio-mask renamed row. iw remains validation/config/tooling/API evidence only and no row claims AP/MLO/DFS/AFC runtime success. Formal round1 x4 no-context audit is completed and minor edits are addressed.

## Secondary Review Handoffs

| file_id / group | primary owner | secondary review | reason |
| --- | --- | --- | --- |
| `000034`-`000036`, AFC/regdb rows | `M07` | `M11` | regulatory/release validation needed after M07 policy decision |
| `000497`-`000503`, `000511`, `000512` | `M07` | `M06` prerequisite | userspace policy depends on stable radio enumeration, firmware, calibration, and MAC source |
| `000225`, `000256`, `000289` | `M08` | `M07` context only | WED/PPE/hardware flow/offload boundary |
| target-missing OpenWrt churn | `M11` | `M07` context | release validation must verify renamed/reworked replacements |
| iw tooling | `M07` | M06/M07/M08 consumers | observation/config tooling cannot prove runtime success |

## Minimalism Gate

Gate result: pass for round1-audited review. Minimal decisions are reported explicitly: non-8X rows name sampled families, target-superseded rows require target evidence, target-missing churn is visible, and unresolved M07 semantics remain `needs-evidence` rather than being hidden under M11 or `review-only`.

## Remaining Risk

Formal round1 x4 no-context audit is completed and minor edits from that audit are addressed. Major residual risks remain deferred to follow-up review/implementation: target equivalence for hostapd/mac80211 MLO/AFC/DFS semantics, ordinary AP regressions hidden inside broad config-generation patches, regulatory provenance for AFC/regdb, target-missing churn replacement, iw/mac80211 radio-mask API alignment, and later runtime testing. Runtime, build, AP, MLO, AFC, and DFS success are out of scope for this review.

## M07 Audit Preparation

Round1 x4 no-context audit is complete. Any later audit should inspect the M07 markdown and TSV, M07 JSON, diff files, direct 8X vendor source, and target 25.12 source, and should treat this review as source-review evidence only, not implementation/build/runtime proof.
