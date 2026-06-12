Reviewer: M07-audit-round1-agent-2
Agent id: 019ebd91-e3c6-7f10-b047-516eae8c4818
Verdict: accept-with-minor-edits

Evidence Read:
- Review artifacts: `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.md`, `migration_step_reviews/8x-vs-openwrt24-base/M07-wireless-userspace-mlo-afc-and-policy.files.tsv`
- Routing inputs: `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M07-wireless-userspace-mlo-afc-and-policy.json`, `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Direct 8X hardware evidence: `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`, `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso`
- Diff and target evidence: checked row patches under `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/diffsets/8x-vs-openwrt24-base/files`, wifi-scripts same paths, hostapd Makefile/files/patches, mac80211 target patch 350, hostapd target patch 370, and iw target patches 010/130/200/310.

Structural Checks:
- PASS: TSV has 600 rows plus header.
- PASS: JSON `file_count=600`; step-file-index has 600 M07 rows.
- PASS: no duplicate IDs, no TSV-vs-JSON missing/extra IDs, and no checked field parity mismatches for `status`, `path`, `file_kind`, `route_classes`, or `features`.
- PASS: legal dispositions only: `needs-evidence`, `defer`, `drop`, `review-only`, `superseded-by-target`.
- PASS: legal owners only: `M07`, `M08`, `M11`.
- PASS: checked `needs-evidence` and `defer` rows had TODO coverage.
- PASS: checked `superseded-by-target` rows had target same-path or target-equivalent evidence.
- Minor structural edit requested: clarify that JSON/markdown `class_counts` are assignment-count semantics, while TSV row split is collapsed file-level route-class count. Agent reports TSV row split `primary=170`, `review-only=590`; JSON assignment split `primary=302`, `review-only=590`.

Common High-Risk Rows Checked:
- 000034 OK: 6 GHz regdb hunk checked; target same-path absent.
- 000035 OK: UNII-4/NO-IR policy checked; evidence gap retained.
- 000036 OK: country VV regulatory override checked; not treated as hardware truth.
- 000225 OK: WED receive-path/offload boundary correctly deferred to M08.
- 000256 OK: MLD hardware forward-path address handling correctly deferred to M08.
- 000289 OK: version-gated offload hook policy correctly deferred to M08.
- 000330 OK: target has related radio-mask support but no same-path vendor patch; `needs-evidence` is correct.
- 000497 OK, 000498 OK, 000499 OK, 000500 OK, 000501 OK, 000502 OK, 000503 OK: wifi-scripts RSNO/SAE/MLO/EHT320/radio-mask deltas were checked and remain unresolved.
- 000509 OK: hostapd Makefile AFC/afcd/libcurl/json-c/CA/build-source delta checked; target baseline newer and target-first policy appropriate.
- 000510 OK: AFC CA trust material checked; target path absent.
- 000511 OK, 000512 OK: MLD/radio-mask ucode paths checked; evidence gap retained.
- 000513 OK, 000514 OK, 000515 OK: broad hostapd baseline/source/patch-stack churn correctly not replayed; 000515 deferred to M11.
- 000516 OK, 000517 OK, 000518 OK, 000519 OK, 000520 OK: AFCD daemon/client, usable-channel 160/320, op-class 137, AFC client, and TPE AFC power behavior checked and left unresolved.
- 000571 OK: `mld_primary` parser/config field verified.
- 000616 OK: A-TTLM ctrl/events/beacon state verified.
- 000621 OK: AFC/LPI txpower vendor path absent in target; needs evidence.
- 000646 OK: DFS offchain set/get controls verified.
- 000655 OK: standalone background-radar behavior verified.
- 000677 OK: txpower vendor ABI changes checked.
- 000720 OK: DFS detect-mode vendor command checked.
- 000746 OK, 000773 OK, 000782 OK, 000783 OK: target-missing deleted hostapd/source rows correctly defer to M11.
- 000787 OK, 000788 OK, 000789 OK, 000790 OK, 000791 OK, 000793 OK, 000794 OK, 000796 OK, 000797 OK, 000798 OK, 000802 OK, 000803 OK, 000804 OK, 000805 OK, 000806 OK, 000807 OK: iw rows are tooling/API/display only, not runtime proof.
- 000792 OK, 000795 OK, 000808 OK, 000810 OK: iw/nl80211 header/API provenance rows correctly remain evidence-needed.
- 000799 OK, 000800 OK, 000801 OK, 000809 OK: target same-path/equivalent iw patches verified.

Assigned Low-Risk Rows Checked:
- 000061 OK: ath regulatory patch is non-8X driver-family.
- 000077 OK: ath11k regulatory patch is non-8X driver-family.
- 000172 OK: rt2x00 patch is non-8X driver-family.
- 000260 OK: MLD address translation remains unresolved.
- 000328 OK: target same-path DFS grace-period patch verified.
- 000340 OK: target same-path antenna-mask patch missing; M11 defer valid.
- 000619 OK: 6G EHT BW320 channel-switch behavior verified.
- 000638 OK: dynamic main-BSS removal remains evidence-needed.
- 000667 OK: reassoc callback address handling verified.
- 000764 OK: target same-path `720-iface_max_num_sta.patch` verified.

Self-Selected Additional Rows:
- Exactly five selected: 000293, 000307, 000312, 000534, 000589.
- 000293 OK: per-link txpower API requires target/policy comparison.
- 000307 OK: DFS scan-relax behavior not claimed as proven.
- 000312 OK: radio index/radio-mask channel-context fix remains unresolved.
- 000534 OK: target lacks same `nl80211_copy.h` sync; needs-evidence remains correct.
- 000589 OK: EMLSR vendor command/IE support absent in target search; evidence gap valid.

Batch-by-Batch Findings:
- Regdb/AFC policy: conservative; no regulatory behavior accepted.
- mac80211/offload: WED/PPE rows correctly deferred to M08.
- wifi-scripts/userspace: dense summaries matched actual diffs.
- hostapd/AFC/MLO/DFS: dense summaries matched patch bodies and remain unresolved.
- iw tooling/API: target-equivalent rows verified; vendor-only header/tooling rows not treated as runtime proof.
- non-8X driver drops: direct 8X DTS/DTSO supports mt7996/mt76, not sampled ath/ath11k/rt2x00 rows.

Row Findings:
- No blocking row findings.
- Minor structural edit: clarify route-class assignment-count wording in markdown.

No-Issue Confirmations:
- All required common high-risk rows, assigned low-risk rows, and exactly five self-selected rows were checked against actual patch/source evidence.
- Checked `superseded-by-target` rows had target same-path or target-equivalent evidence.
- Target-missing/defer rows were verified as missing same-path or unresolved-equivalent rather than trusted from TSV wording.

Residual Risk:
- This audit does not prove runtime AP, MLO, DFS, AFC, build, or hardware success. Many rows intentionally remain `needs-evidence` or `defer`, which the agent judged appropriate.
