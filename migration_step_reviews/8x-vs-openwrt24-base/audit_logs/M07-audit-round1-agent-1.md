Reviewer: M07-audit-round1-agent-1
Agent id: 019ebd91-e36c-71a2-b79a-21c580d6b918
Verdict: accept-with-minor-edits

Evidence Read:
- Review artifacts: `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.md`, `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.files.tsv`
- Routing inputs: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M07-wireless-userspace-mlo-afc-and-policy.json`, `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Diff evidence root: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files`
- Direct 8X vendor evidence: `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`
- Target evidence: wireless-regdb patch directory, mac80211 `patches/subsys/350-mac80211-allow-scanning-while-on-radar-channel.patch`, wifi-scripts same-path files, hostapd `Makefile`, selected hostapd source/patch files, and iw target patches `010-Revert-iw-allow-specifying-CFLAGS-LIBS-externally.patch`, `130-survey-bss-rx-time.patch`, `200-reduce_size.patch`, `310-vif_radio_mask.patch`
- The agent stated it did not read `audit_logs/`, launch sub-agents, modify files, or commit.

Structural Checks:
- PASS: TSV has 600 data rows and JSON has `file_count=600`.
- PASS: file IDs and core fields match JSON for the checked structural scope; no missing, extra, or duplicate required IDs found.
- PASS: step-file-index coverage matched M07 IDs for checked scope.
- PASS: dispositions were treated as legal: `defer`, `drop`, `needs-evidence`, `review-only`, `superseded-by-target`.
- PASS: owner steps were legal: `M07`, `M08`, `M11`.
- PASS: checked `defer` and `needs-evidence` rows had TODO/gap wording.
- Minor structural issue: markdown label `Route-class assignment split` says `primary 170 review-only 590`, while JSON assignment class counts are `primary 302 review-only 590`. Agent says TSV value appears to be a collapsed file-level route-class count, not assignment count; rename the line or show both counts.

Common High-Risk Rows Checked:
- B1 regdb: 000034 OK, 000035 OK, 000036 OK. Patch bodies for 6 GHz world/US, UNII-4/NO-IR, and synthetic country VV policy were read; all correctly remain `needs-evidence`.
- B2 M08 boundary and radio-mask: 000225 OK, 000256 OK, 000289 OK, 000330 OK. WED/offload rows correctly defer to M08; 000330 overlaps target radio-mask stack but remains target-comparison sensitive.
- B3 wifi-scripts and early hostapd/AFC: 000497 OK, 000498 OK, 000499 OK, 000500 OK, 000501 OK, 000502 OK, 000503 OK, 000509 OK, 000510 OK, 000511 OK, 000512 OK, 000513 OK, 000514 OK, 000515 OK, 000516 OK, 000517 OK, 000518 OK, 000519 OK, 000520 OK. Dense script/AFC summaries matched patch bodies; broad hostapd sync was not replayed.
- B4 hostapd MLO/A-TTLM: 000571 OK, 000616 OK. `mld_primary` and A-TTLM body semantics were checked.
- B5 AFC/DFS/txpower: 000621 OK, 000646 OK, 000655 OK, 000677 OK, 000720 OK. AFC/LPI power, DFS offchain/background, txpower vendor command, and DFS detect-mode summaries matched body semantics.
- B6 deleted hostapd and iw: 000746 OK, 000773 OK, 000782 OK, 000783 OK, 000787 OK, 000788 OK, 000789 OK, 000790 OK, 000791 OK, 000792 OK, 000793 OK, 000794 OK, 000795 OK, 000796 OK, 000797 OK, 000798 OK, 000799 OK, 000800 OK, 000801 OK, 000802 OK, 000803 OK, 000804 OK, 000805 OK, 000806 OK, 000807 OK, 000808 OK, 000809 OK, 000810 OK. Target-equivalent iw rows were checked against target patches; target-missing rows remained `needs-evidence` or `defer`.

Assigned Low-Risk Rows Checked:
- 000105: OK. ath9k AR933x/AR934x workaround is not direct 8X mt76/mt7996 evidence.
- 000158: OK. rt2x00 EEPROM swap is non-8X.
- 000196: OK. rtw88/RTL8812A row is non-8X.
- 000306: OK. scan prohibited-band behavior has related target radar/scan work but not identical acceptance.
- 000334: OK. deleted monitor-channel API patch is M11 provenance-sensitive.
- 000566: OK. wpa_supplicant association-frequency fix needs target comparison.
- 000582: OK. MLD link readiness state machine remains evidence-needed.
- 000622: minor issue. WDS free-BSS crash patch may leave stack `name` uninitialized when `ifname_wds` is NULL; row should flag the unresolved risk.
- 000683: OK. WMM IE length helper is concrete hostapd behavior.
- 000780: OK. target same-path ucode source exists.

Self-Selected Additional Rows:
- Exactly five selected: 000293, 000300, 000534, 000608, 000632.
- 000293: OK. per-link txpower/AFC-adjacent API correctly remains `needs-evidence`.
- 000300: issue. Vendor patch `0091-mtk-mac80211-sync-from-felix.patch.patch` calls `cfg80211_radio_chandef_valid(radio, chandef)` without assigning `radio = &wiphy->radio[i]`; target mac80211 patch 350 assigns `radio`. Review should flag apparent patch-body defect/provenance hazard.
- 000534: OK. broad hostapd `nl80211` header sync remains target/provenance sensitive.
- 000608: OK. dynamic MLD link-add state machine absent in target patterns.
- 000632: OK. MLD partner-link STA cleanup correctly remains evidence-needed.

Batch-by-Batch Findings:
- Batch 1: no row-level issue.
- Batch 2: row issue on 000300; add explicit provenance/patch-body defect note.
- Batch 3: no row-level issue.
- Batch 4: no disposition issue.
- Batch 5: row issue on 000622; wording should not imply the WDS NULL fix is complete.
- Batch 6: no row-level issue.

Row Findings:
- 000300: add explicit note for apparent uninitialized `radio` pointer/provenance hazard versus target implementation.
- 000622: add explicit note that the vendor patch appears to attempt a WDS crash fix but may leave `name` uninitialized when `ifname_wds` is NULL.
- Markdown structural wording: clarify route-class assignment/file-level count wording.

No-Issue Confirmations:
- Required common high-risk rows, assigned low-risk rows, and exactly five self-selected rows were checked against actual diff/source/target evidence.
- No checked `superseded-by-target` row was accepted without target same-path or target-equivalent evidence.
- No checked row claimed build success, runtime success, AP success, MLO success, DFS success, or AFC success.

Residual Risk:
- Source review only. It does not prove build, runtime, AP, MLO, DFS, AFC, or 8X hardware behavior beyond the direct DTS/source facts inspected.
