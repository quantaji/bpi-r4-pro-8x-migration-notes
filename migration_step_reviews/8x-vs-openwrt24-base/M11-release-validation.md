# M11: Release Validation

Migration step index: `analysis/migration-step-routing/8x-vs-openwrt24-base/by-step/M11-release-validation.json`

Review matrix: `migration_step_reviews/8x-vs-openwrt24-base/M11-release-validation.files.tsv`

Audit Status: formal no-context audit round1 completed. Verdicts: agent-1 `accept`, agent-2 `accept-with-minor-edits`, agent-3 `accept`. Only minor TSV wording remediation was applied for `000051`; no classification changes were required.

No migration code was written, no image was compiled, and this review does not claim build success, boot success, sysupgrade success, NAND/eMMC install success, wired runtime success, Wi-Fi runtime success, USB runtime success, or acceleration/offload success.

## Scope

M11 is the release-validation checklist step. It records which release artifacts, package closures, default configs, init/services, board.d/base-files, upgrade scripts, target package state, and known limitations must be rechecked after implementation exists.

M11 does not own the implementation of earlier migration steps:

- M01 owns clean build and image skeleton policy.
- M02 owns SD boot no-install.
- M04/M05 own basic and full wired behavior.
- M06/M07 own Wi-Fi hardware and userspace policy.
- M08 owns acceleration/offload.
- M09 owns board extras and expansion runtime.
- M10 owns onboard storage install/sysupgrade destructive paths.

Out of scope:

- Writing migration code.
- Building or booting an image.
- Writing NAND/eMMC or proving sysupgrade.
- Treating package lists as functional success.
- Treating static UCI files as runtime network/firewall/storage behavior.
- Treating target OpenWrt 25.12 target-owned code as direct 8X hardware truth.

## Structural Summary

| Item | Count |
| --- | ---: |
| M11 JSON files | 33 |
| M11 TSV rows | 33 |
| Feature assignments | 40 |
| JSON status A | 15 |
| JSON status M | 14 |
| JSON status D | 4 |
| File-level route_classes primary memberships | 27 |
| File-level route_classes supporting memberships | 8 |
| Feature-level route_class primary assignments | 32 |
| Feature-level route_class supporting assignments | 8 |
| Feature role primary assignments | 27 |
| Feature role secondary assignments | 13 |

## Disposition Summary

| Disposition | Count | Meaning in this draft |
| --- | ---: | --- |
| `needs-evidence` | 18 | Final release validation evidence is required after the owning implementation step exists. |
| `superseded-by-target` | 6 | Target OpenWrt 25.12 already provides the package/version/patch behavior to use for release closure. |
| `drop` | 3 | Generic or unsafe vendor policy should not be carried into the release without later proof. |
| `defer` | 3 | The row is owned by M07 or M08 behavior validation before M11 can recheck release closure. |
| `static-only` | 2 | Static default-config evidence only; no runtime behavior accepted. |
| `review-only` | 1 | Non-8X RFB artifact reference only. |

Owner counts:

| Owner | Count |
| --- | ---: |
| `M11` | 30 |
| `M07` | 2 |
| `M08` | 1 |

## Evidence Read

All 33 M11 rows were read from their diffset patch/source bodies. Target OpenWrt 25.12 was checked where target-owned closure or superseded-by-target was claimed. Direct 8X vendor source was checked for 8X image/package/board evidence and for reset-boot-count property absence.

Key evidence:

- `000028`, `000823`, `000969`, and `000970` add optional secure FIT, firmware encryption, OP-TEE, ramdisk rootfs, dm-verity, and anti-rollback build behavior. These are release artifact risks, not success proof.
- `000050`-`000053` change package module closure for dm/dm-verity, Airoha PHY, HNAT, netfilter flowtable netlink, and MediaTek xHCI debugfs. They are package manifest risks only.
- `000490`-`000493` implement reset-boot-count as an SMC/procfs module gated by a DTS property. Direct 8X source search did not find `mediatek,reset-boot-count`.
- `000494`-`000508` touch packet steering, netifd wireless policy, dnsmasq version/patch state, and relayd trigger behavior. Target 25.12 keeps packet steering service and already carries dnsmasq 2.91 with the relevant ubus patch.
- `000825` and `000826` are PPPQ/EBL and RSNO/MLO policy scripts, so their implementation decisions remain M08 and M07.
- `000960` is the direct 8X board.d network default row. It records LAN/WAN defaults but does not prove wired runtime.
- `000961`-`000963` are static default config files; the draft rejects wholesale firewall/network copying and records only static validation risks.
- `000964`-`000966` are destructive or high-risk upgrade helpers and platform routing; M10 owns implementation safety.
- `000972` is the direct 8X release artifact row and remains high-risk checklist evidence only.

## High-Risk Rows

- `000028`: FIT/sysupgrade helper changes for secure/encrypted/anti-rollback artifacts.
- `000050`-`000053`: package closure for dm, PHY, HNAT, flowtable netlink, and USB xHCI.
- `000490`-`000493`: reset-boot-count package/init/module; no direct 8X property evidence yet.
- `000494`-`000508`: generic network defaults, packet steering, wireless netifd policy, dnsmasq target closure, and relayd trigger policy.
- `000823`: mkits FIT cipher/signature/anti-rollback generation.
- `000825`: PPPQ/EBL debugfs toggle; M08 boundary.
- `000826`: RSNO/MLO wireless policy script; M07 boundary.
- `000960`-`000966`: board.d defaults, static UCI policy, and upgrade helper/platform scripts.
- `000969`-`000972`: image secure-boot config/build helpers, non-8X RFB artifact reference, and direct 8X artifact recipe.

## Cross-Step Handoffs

| File ID | M11 treatment | Owner / secondary review | Reason |
| --- | --- | --- | --- |
| `000028`, `000823`, `000969`, `000970` | release artifact validation | M01, M10, M11 | M01/M10 decide image/storage semantics; M11 rechecks final release artifacts and documents optional secure-boot scope. |
| `000050` | package closure | M10, M11 | dm/dm-verity package state depends on storage/secure-boot decisions. |
| `000051` | package closure | M05, M08, M11 | Airoha PHY and HNAT package closure depends on wired and acceleration outcomes. |
| `000052` | package closure | M08, M11 | Flowtable netlink package state depends on acceleration design. |
| `000053` | package closure | M09, M11 | USB package closure depends on board extras validation. |
| `000490`-`000493` | bootcount validation | M10, M11 | Reset-boot-count must be tied to storage/recovery policy before release. |
| `000496`, `000826` | deferred | M07 | Wireless userspace policy must be decided before release validation can recheck it. |
| `000825` | deferred | M08 | PPPQ/EBL debugfs policy is acceleration/offload scope. |
| `000960`, `000963` | default config validation | M04, M05, M09, M11 | LAN/WAN defaults, MxL/SFP context, and cellular defaults must be validated without copying static vendor config wholesale. |
| `000964`-`000966`, `000972` | release/storage validation | M10, M11 | Upgrade helpers and artifacts must wait for safe storage/sysupgrade design. |

## TODOs

1. Validate final package manifest against rows `000050`-`000053` after M05/M08/M09/M10 decisions.
2. Decide whether optional secure boot, firmware encryption, OP-TEE, dm-verity, and anti-rollback rows are explicitly out of scope or validated release features.
3. Confirm reset-boot-count is absent or intentionally enabled in migrated 8X DTS/package state; do not infer success from package code.
4. Recheck target-owned dnsmasq and packet steering behavior during release validation without copying vendor churn.
5. Validate M04-generated network defaults from `000960` and static `000963` evidence without declaring wired runtime success.
6. Keep `000961` firewall policy dropped unless M09/M11 later prove a specific cellular firewall default is required.
7. Validate `000964`-`000966` only after M10 storage/sysupgrade safety exists.
8. Validate `000972` artifact names, package closure, metadata, and storage boundaries after implementation; do not treat artifact generation as boot/flash/sysupgrade success.

## Minimalism Gate

Gate result: pass for main-agent draft.

This draft does not silently use a minimal release shortcut:

- All 33 M11 rows were read from patch/source body evidence, not sampled.
- Deleted dnsmasq rows were checked against target 25.12 package/version evidence instead of dropped from status alone.
- `review-only`, `drop`, `superseded-by-target`, and `static-only` rows include body-level evidence and state why they do not prove runtime behavior.
- Package lists are treated as package closure only.
- Static firewall/network/fstab files are not copied wholesale.
- Upgrade helpers and image artifacts remain validation risks rather than storage/sysupgrade success evidence.
- M07/M08/M10 behavior is handed off instead of being absorbed into M11.

## Remaining Risk

Formal no-context audit round1 is completed. M11 still has release-validation risk around package manifest closure, target-owned dnsmasq/netifd/relayd behavior, optional secure FIT/OP-TEE/dm-verity policy, reset-boot-count absence or inclusion, static default config policy, M04/M05/M06/M07/M08/M09/M10 runtime outcomes, sysupgrade safety, and final artifact naming/metadata.

This draft does not prove build success, image boot success, sysupgrade success, NAND/eMMC install success, wired runtime success, Wi-Fi runtime success, USB runtime success, acceleration/offload success, or release readiness.

## Next Audit Instructions

No-context auditors should verify:

- TSV coverage against the 33-file M11 JSON and 40 feature assignments.
- Exact parity for `status`, `path`, `file_kind`, `route_classes`, and `features`.
- Legal dispositions and owner steps, especially `defer -> M07/M08`.
- Body-level evidence for every row, not only high-risk rows.
- Target evidence for all `superseded-by-target` rows.
- That `drop` rows are not filename/status-only decisions.
- That `static-only` rows have TODOs and do not claim runtime success.
- That release artifact/package/default-config rows do not claim build, boot, flash, sysupgrade, or runtime success.
