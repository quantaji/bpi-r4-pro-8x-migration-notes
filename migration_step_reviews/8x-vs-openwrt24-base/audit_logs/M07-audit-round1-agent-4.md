Reviewer: M07-audit-round1-agent-4
Agent id: 019ebd91-e417-7163-8769-7abdfa73befe
Verdict: accept-with-minor-edits

Evidence Read:
- Review artifacts: `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.md`, `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.files.tsv`
- Routing inputs: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M07-wireless-userspace-mlo-afc-and-policy.json`, `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Diff evidence root: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files`
- Direct 8X vendor evidence: `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`, `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`
- Target evidence included mac80211 patch 350, hostapd patch 370, iw patch 310, target iw patches 010/130/200/310, and same-path target files or absence checks for hostapd/wifi-scripts/iw rows.
- The agent stated it did not read `audit_logs/` and did not modify files.

Structural Checks:
- PASS: TSV has 600 data rows; JSON has `file_count=600`, 600 files, and `assignment_count=892`.
- PASS: TSV vs JSON file IDs match with no missing, extra, or duplicate IDs.
- PASS: field parity checked for status, path, file_kind, route_classes, and features.
- PASS: step-file-index has 600 M07 rows and matches TSV.
- PASS: dispositions and owner steps are legal.
- PASS: `needs-evidence` and `defer` rows have TODO/gap coverage.
- PASS: Dense-read rows count 49 and sampled/high-risk Dense-read summaries matched patch bodies.

Common High-Risk Rows Checked:
- 000034 OK, 000035 OK, 000036 OK: regdb 6 GHz, UNII-4, and country VV patch semantics checked.
- 000225 OK, 000256 OK, 000289 OK: WED/offload rows remain M08.
- 000330 minor issue: evidence supports related target radio-mask work, but wording should clarify target mac80211 patch 350 is not same-path VIF patch.
- 000497 OK, 000498 OK, 000499 OK, 000500 OK, 000501 OK, 000502 OK, 000503 OK: wifi-scripts dense-read rows verified.
- 000509 OK, 000510 OK, 000511 OK, 000512 OK: hostapd Makefile/AFC cert/ucode rows verified.
- 000513 OK, 000514 OK, 000515 OK: broad baseline/source/patch-stack sync reviewed as provenance/churn, not replayed.
- 000516 OK, 000517 OK, 000518 OK, 000519 OK, 000520 OK: AFCD, 160/320, op-class 137, AFC client, and AFC TPE rows verified.
- 000571 OK, 000616 OK: `mld_primary` and A-TTLM behavior verified.
- 000621 OK, 000646 OK, 000655 OK, 000677 OK, 000720 OK: AFC/LPI, DFS offchain/background, txpower vendor command, and DFS detect-mode rows verified.
- 000746 OK, 000773 OK, 000782 OK, 000783 OK: deleted hostapd/source rows are target-missing and deferred.
- 000787 OK, 000788 OK, 000789 OK, 000790 OK, 000791 OK, 000792 OK, 000793 OK, 000794 OK, 000795 OK, 000796 OK, 000797 OK, 000798 OK, 000799 OK, 000800 OK, 000801 OK, 000802 OK, 000803 OK, 000804 OK, 000805 OK, 000806 OK, 000807 OK, 000808 OK, 000809 OK, 000810 OK: iw tooling/API/provenance rows checked; runtime proof not claimed.

Assigned Low-Risk Rows Checked:
- 000175 OK: rt2x00/MT7620 not direct 8X mt76/mt7996 path.
- 000200 OK: Realtek rtw88 source not 8X Wi-Fi hardware path.
- 000249 OK: probe-client warning behavior verified.
- 000252 OK: per-link CAC/DFS fields verified.
- 000332 OK: deleted radio-mask channel-context behavior is target-churn sensitive.
- 000537 OK: ZWDFS/BW160 behavior verified.
- 000563 OK: ACS scan/freq-list check removal verified.
- 000640 OK: REMOVE_MLD lifecycle behavior verified.
- 000672 OK: colocated RNR beacon update path verified.
- 000766 OK: target same-path OpenWrt patch verified.

Self-Selected Additional Rows:
- Exactly five selected: 000054, 000293, 000534, 000612, 000623.
- Rationale: 000054 is target-baseline/backports sensitive; 000293 is AFC/regulatory power-policy adjacent; 000534 is broad nl80211 API provenance; 000612 and 000623 are deleted target-equivalence rows where same-path verification matters.
- 000054 OK: target has newer mac80211 baseline without vendor SOURCE_PATH/-Werror/debug churn.
- 000293 OK: per-link txpower API/config body verified; no power success claim.
- 000534 minor issue: disposition correct, but TODO should say target package lacks extracted `src/drivers/nl80211_copy.h` and needs UAPI/upstream-source comparison.
- 000612 OK: target same-path mesh DFS patch verified.
- 000623 OK: target same-path deterministic mesh CSA patch verified.

Batch-by-Batch Findings:
- B1: regdb rows correctly remain `needs-evidence`; non-8X driver drops are supported by direct 8X mt76/mt7996 DTS/DTSO evidence.
- B2: mac80211 WED rows correctly defer to M08; radio-mask rows are target-sensitive evidence gaps/churn.
- B3: wifi-scripts and early hostapd rows contain concrete patch-body summaries; no unsupported runtime/AP/MLO/AFC claim found.
- B4-B5: hostapd MLD/A-TTLM/AFC/DFS dense rows match actual hunks and stay `needs-evidence`.
- B6: deleted target-present rows have target evidence; target-missing rows remain `defer`/`needs-evidence`; iw rows are tooling/API provenance.

Row Findings:
- 000330: Minor wording edit. Target mac80211 patch 350 is related radio-mask/radar-scan work, not a same-path replacement for deleted `330-wifi-cfg80211-add-option-for-vif-allowed-radios.patch`. Keep `needs-evidence`.
- 000534: Minor wording edit. Target 25.12 package tree did not contain `src/drivers/nl80211_copy.h`; TODO should direct comparison to target kernel UAPI/upstream hostapd extracted source, not imply a present same-path file.

No-Issue Confirmations:
- All required common high-risk rows, all assigned low-risk rows, and exactly five self-selected rows were checked against actual diff/source or target evidence.
- Dense-read summaries matched relevant patch bodies.
- Superseded-by-target rows had target same-path or target-equivalent evidence.
- Target-missing/defer rows had absence/gap checks.
- No reviewed row claimed runtime success, build success, AP success, MLO success, DFS success, AFC success, or direct 8X hardware truth.

Residual Risk:
- This audit verifies review quality only. Rows left as `needs-evidence` or `defer` still require regulatory/legal provenance, target UAPI comparison, M08 offload review, M11 target-churn review, and later runtime validation where appropriate.
