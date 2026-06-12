Reviewer: M07-audit-round1-agent-3
Agent id: 019ebd91-e3ef-7cf3-854a-7adb7ba6c4ba
Verdict: revise-before-accept

Evidence Read:
- Review artifacts: `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.md`, `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.files.tsv`
- Routing inputs: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M07-wireless-userspace-mlo-afc-and-policy.json`, `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Direct 8X vendor evidence: `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`, `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`, `package/network/services/hostapd/files/afc_ca.pem`
- Target evidence: hostapd `Makefile`, `files/hostapd.uc`, `files/wpa_supplicant.uc`, wifi-scripts `hostapd.sh`, `mac80211.sh`, `common.uc`, `wifi-detect.uc`, mac80211 patch 350, hostapd patches 021/170/191/200/212/370, iw patches 010/130/200/310.
- Absence checks: target-missing claims for hostapd `330`, `804`, `src/wpa_supplicant/ubus.c`, `src/wpa_supplicant/ubus.h`, `files/afc_ca.pem`, iw `0006`, `0009`, `0022`, and `300-wiphy_radios`.

Structural Checks:
- PASS: TSV rows 600; JSON files 600; JSON `file_count=600`; assignment count 892.
- PASS: TSV vs JSON file IDs had no missing, extra, or duplicate IDs.
- PASS: TSV vs JSON parity had no mismatches for file ID, path, file kind, status, route classes, or features.
- PASS: step-file-index M07 rows 600 and matched JSON IDs.
- PASS: non-M07 owners point to M08/M11 handoff ownership and appear intentional.
- PASS: checked `needs-evidence` and `defer` rows had TODO/gap wording.
- PASS: checked superseded rows had target same-path or target-equivalent evidence.
- Agent-reported issue: TSV/markdown use `review-only` as disposition in 40 rows; the agent believed this was not a legal migration disposition and therefore gave `revise-before-accept`.

Coordinator note:
- Local rules file `rules/disposition-tags-v1.json` defines `review-only` as a legal disposition. The agent-3 taxonomy finding is therefore a false positive against the project rules, not an accepted blocker.

Common High-Risk Rows Checked:
- 000034 OK, 000035 OK, 000036 OK: regdb 6 GHz, UNII-4, and country VV patch bodies matched summaries; target same-path absent where relevant.
- 000225 OK, 000256 OK, 000289 OK: WED/offload-sensitive rows correctly defer to M08.
- 000330 OK: deleted radio-mask API patch accurately summarized; target has related but not same-path coverage.
- 000497 OK, 000498 OK, 000499 OK, 000500 OK, 000501 OK, 000502 OK, 000503 OK: wifi-scripts RSN/MLO/EHT/radio-mask changes matched patch bodies.
- 000509 OK: hostapd Makefile AFC/afcd packaging delta matched; target lacks afcd packaging.
- 000510 OK: WFA AFC root certificate exists in vendor and target path absent.
- 000511 OK, 000512 OK: MLD/radio-mask ucode changes matched.
- 000513 reported issue only because disposition is `review-only`; body summary itself matched broad baseline revert.
- 000514 reported issue only because disposition is `review-only`; body summary itself matched source sync.
- 000515 OK: broad patch-stack carrier accurately deferred to M11.
- 000516 OK, 000517 OK, 000518 OK, 000519 OK, 000520 OK: AFCD/curl/TLS/socket, 160/320 channel usability, op-class 137, AFC client, and AFC TPE IE logic matched.
- 000571 OK: `mld_primary` config plumbing matched.
- 000616 OK: SET_ATTLM/A-TTLM CLI, events, and driver plumbing matched.
- 000621 OK, 000646 OK, 000655 OK, 000677 OK, 000720 OK: AFC/LPI vendor power, DFS offchain, background radar, txpower vendor command, and DFS detect-mode rows matched body semantics.
- 000746 OK, 000773 OK, 000782 OK, 000783 OK: deleted hostapd/source rows are target-missing and correctly deferred to M11.
- 000787, 000788, 000789, 000790, 000791, 000793, 000794, 000796, 000797, 000798, 000802, 000803, 000804, 000805, 000806, 000807: agent marked body semantics as matched but reported issues solely because disposition is `review-only`.
- 000792 OK, 000795 OK, 000808 OK, 000810 OK: iw/nl80211 header/API provenance rows remain evidence-needed.
- 000799 OK, 000800 OK, 000801 OK, 000809 OK: target same-path/equivalent iw patches present.

Assigned Low-Risk Rows Checked:
- 000083 OK: ath5k-only; direct 8X DTS shows mt76/mt7996 PCIe Wi-Fi.
- 000100 OK: ath9k-only LED/platform behavior; not direct 8X hardware.
- 000116 OK: b43/brcm-only; no direct 8X match.
- 000184 OK: rtw88/RTL USB-only; direct 8X DTS does not support keeping it for 8X.
- 000265 OK: legacy AP scan channel constraint change matched; needs-evidence valid.
- 000331 OK: target same-path absent; related radio-mask target evidence exists; M11 defer valid.
- 000526 reported issue only because disposition is `review-only`; patch body matched three-wire PTA vendor control.
- 000639 OK: enable/disable single BSS controls matched.
- 000663 OK: interface setup context plumbing matched.
- 000736 OK: target same-path patch present.

Self-Selected Additional Rows:
- Exactly five selected: 000293, 000534, 000608, 000665, 000721.
- 000293 OK: per-link txpower API plumbing matched; needs-evidence valid.
- 000534 OK: dense `nl80211` sync summary matched MLO/A-TTLM/DFS/EHT/AFC-adjacent symbols.
- 000608 OK: LINK_ADD/MLD reconfiguration body matched.
- 000665 OK: FT Auth MLD key/address/MIC handling matched.
- 000721 OK: target same semantic station re-add fix present.

Batch-by-Batch Findings:
- B1 regdb: no false target-equivalence claim found.
- B2 mac80211/WED/radio-mask: M08 handoffs and M07 evidence gaps supported by patch bodies and target checks.
- B3 wifi-scripts/hostapd/AFC: dense summaries matched actual patch bodies; target has partial script support but not vendor AFC/afcd packaging.
- B4/B5 MLO/A-TTLM/AFC/DFS: patch bodies matched review summaries; runtime capability not claimed.
- B6 hostapd deleted patches and iw: superseded rows had target evidence; target-missing rows were missing; recurring reported issue is the false-positive `review-only` taxonomy claim.

Row Findings:
- Agent finding: 40 rows use `review-only`; agent considered this illegal. Coordinator rejects this as false positive because project disposition rules explicitly allow `review-only`.
- No checked `superseded-by-target` row lacked target evidence.
- No checked `needs-evidence`, `defer`, or target-missing row was accepted without inspecting patch or source evidence.
- No direct 8X hardware claim was accepted from TSV/markdown alone.

No-Issue Confirmations:
- TSV, JSON, and step-file-index coverage matched exactly for M07.
- Duplicate, missing, and extra file IDs: none found.
- Dense-read rows checked against patch bodies were materially accurate.
- Direct 8X hardware evidence supports dropping sampled ath5k/ath9k/brcm/rtl rows for 8X.
- AFC certificate and afcd claims were verified against vendor files and target absence.
- Target equivalence for checked superseded rows was verified in OpenWrt 25.12 source.

Residual Risk:
- The audit did not test runtime behavior, builds, AP operation, MLO operation, DFS operation, AFC operation, or hardware behavior. Remaining risk is evidence completeness for unchecked `needs-evidence` rows and regulatory/provenance review for AFC/regdb policy changes.
