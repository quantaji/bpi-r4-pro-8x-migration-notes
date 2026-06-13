# P2 Cross-Step Coherence Audit

Generated from existing M00-M11 review matrices. This file does not migrate code and does not claim build/runtime success.

## Scope

- Source matrices: `migration_step_reviews/8x-vs-openwrt24-base/M*.files.tsv`
- Routing index: `analysis/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Purpose: preserve the cross-step handoffs that are not visible when reading only one migration step TSV.

## Coverage Summary

| Metric | Count |
| --- | ---: |
| Diffset patch files | 1181 |
| Step-file-index unique file_id | 1181 |
| M00-M11 TSV rows | 1662 |
| M00-M11 TSV unique file_id | 1181 |
| Structural missing unique file_id | 0 |

## Owner-Step Worklist Counts

| owner_step | rows |
| --- | ---: |
| `M00` | 112 |
| `M01` | 73 |
| `M02` | 28 |
| `M03` | 53 |
| `M04` | 61 |
| `M05` | 213 |
| `M06` | 98 |
| `M07` | 652 |
| `M08` | 196 |
| `M09` | 53 |
| `M10` | 76 |
| `M11` | 47 |

## Handoff Status

| handoff_status | rows | percent of TSV rows |
| --- | ---: | ---: |
| `owned-in-source-step` | 1243 | 74.79% |
| `covered-by-owner-step-tsv` | 238 | 14.32% |
| `external-handoff-not-reacknowledged` | 173 | 10.41% |
| `acknowledged-in-owner-step-md` | 8 | 0.48% |

Definitions:

- `owned-in-source-step`: the row is owned by the same step that contains it.
- `covered-by-owner-step-tsv`: another step handed off the row, and the owner step also contains the same file_id in its TSV.
- `acknowledged-in-owner-step-md`: another step handed off the row; the owner step does not contain it in TSV, but its markdown mentions the file_id.
- `external-handoff-not-reacknowledged`: another step handed off the row, and the owner step artifacts do not mention the same file_id. These are not structurally missing, but they can be missed during implementation unless this global worklist is used.

## External Handoffs Not Reacknowledged

Total: `173` rows, `10.41%` of the global TSV rows.

| owner_step | rows |
| --- | ---: |
| `M05` | 33 |
| `M06` | 1 |
| `M07` | 61 |
| `M08` | 42 |
| `M09` | 11 |
| `M10` | 8 |
| `M11` | 17 |

Top source -> owner pairs:

| source_step | owner_step | rows |
| --- | --- | ---: |
| `M06` | `M07` | 48 |
| `M00` | `M05` | 26 |
| `M04` | `M08` | 19 |
| `M00` | `M08` | 17 |
| `M07` | `M11` | 17 |
| `M08` | `M07` | 10 |
| `M00` | `M09` | 9 |
| `M04` | `M05` | 6 |
| `M02` | `M10` | 4 |
| `M04` | `M10` | 4 |
| `M07` | `M08` | 3 |
| `M01` | `M05` | 1 |
| `M03` | `M06` | 1 |
| `M01` | `M07` | 1 |
| `M04` | `M07` | 1 |
| `M11` | `M07` | 1 |
| `M03` | `M08` | 1 |
| `M05` | `M08` | 1 |
| `M11` | `M08` | 1 |
| `M01` | `M09` | 1 |

These rows must not be interpreted as lost. They are present in the global worklist and usually have a TODO in their source step. The risk is operational: an implementation agent that reads only `Mxx.files.tsv` will miss them.

## Global Handoff Bucket Audit Status

P2 global handoff bucket audit round1 is completed with five no-context agents.
All five verdicts were `accept-with-minor-edits`. Raw audit logs and the
coverage plan are saved under `audit_logs/`.

The accepted round1 remediation was applied to
`P2-unacknowledged-owner-handoffs.tsv`.

Final bucket counts:

| audit_bucket | rows |
| --- | ---: |
| `true-owner-gap` | 100 |
| `covered-by-topic` | 68 |
| `global-worklist-only` | 2 |
| `wrong-owner-or-source` | 1 |
| `needs-human-decision` | 2 |

Remediation rows:

| handoff row | bucket change |
| --- | --- |
| `M09 <- M00 001135` | `covered-by-topic -> true-owner-gap` |
| `M09 <- M00 001136` | `covered-by-topic -> true-owner-gap` |
| `M09 <- M00 001138` | `covered-by-topic -> true-owner-gap` |
| `M09 <- M00 001146` | `covered-by-topic -> true-owner-gap` |
| `M09 <- M00 001147` | `covered-by-topic -> true-owner-gap` |
| `M09 <- M00 001148` | `covered-by-topic -> true-owner-gap` |
| `M09 <- M06 001136` | `covered-by-topic -> true-owner-gap` |
| `M08 <- M04 001044` | `covered-by-topic -> needs-human-decision` |

Interpretation:

1. `true-owner-gap` rows are not missing from Phase 2. They are operational
   handoff risks: the source-step review captured the handoff, but the owner
   step artifacts do not explicitly re-acknowledge the same file_id/topic.
2. Do not backfill M00-M11 automatically yet. Backfill or a formal global
   handoff addendum should be decided before implementation of affected owner
   steps.
3. Future implementation agents must use both `P2-owner-step-worklist.tsv` and
   `P2-unacknowledged-owner-handoffs.tsv`, not only per-step Mxx TSVs.

## Targeted Coherence Check Result

| file_id | final coherence verdict | involved steps | split coherence | future implementation must read | later backfill need |
| --- | --- | --- | --- | --- | --- |
| `000343` | `coherent` | M01, M06, M08 | M01 correctly treats the mt76 Makefile as build/package boundary; M06 uses target 25.12 mt76 package structure for basic Wi-Fi closure; M08 keeps vendor `wed_enable=1`, WO/WED firmware, debugfs/testmode, and mt7990 package implications as acceleration evidence. | M01/M06/M08 TSV rows, vendor `package/kernel/mt76/Makefile` diff, target 25.12 `package/kernel/mt76/Makefile`. | No later Mxx backfill required; keep M08 package/offload TODO visible. |
| `000374` | `coherent` | M06, M08 | M06 can drop the mt7990/non-8X basic Wi-Fi side; M08 correctly keeps the large shared mt76/mt7996 support surface because the patch body touches debugfs, DMA, EEPROM, init, MCU, PCI, register, firmware and WED/RRO-adjacent paths. | M06/M08 TSV rows and vendor `0031-mtk-mt76-mt7990-use-device-id-macro-in-internal-debug-file` patch body. | No later Mxx backfill required. |
| `000400` | `coherent` | M06, M08 | M06 can reject it for basic radio bring-up because the title is mt7990/mt7987; M08 correctly keeps it because the body modifies generic mt76 DMA/RRO handling, HWRRO mode, RXDMAD_C queue handling, WED RX capability checks, and WED v3/v3.1 behavior. | M06/M08 TSV rows and vendor `0057-mtk-mt76-mt7990-add-mt7987-wed-hw-path-support` patch body. | No later Mxx backfill required. |
| `000426` | `coherent` | M06, M08 | M06 can drop the mt7990 low-power policy from basic 8X Wi-Fi hardware; M08 correctly keeps a needs-evidence row because the patch adds `lp_ctrl`, PCIe L1SS/TPO/ultra-save/PST controls, MCU commands, debugfs knobs, and shared mt7996 code changes. | M06/M08 TSV rows and vendor `0083-mtk-mt76-mt7996-add-low-power-control-for-mt7990` patch body. | No later Mxx backfill required. |
| `000961` | `coherent` | M04, M09, M11 | M04 and M11 correctly avoid copying vendor firewall policy wholesale; M09 keeps only static cellular/WWAN firewall context. The vendor file adds WWAN networks to the WAN zone and broadly opens WAN input/forward, which is not wired runtime proof. | M04/M09/M11 TSV rows and vendor `target/linux/mediatek/filogic/base-files/etc/config/firewall` diff. | No later Mxx backfill required; M09/M11 implementation must keep cellular limitation visible. |
| `001044` | `needs-human-decision` | M00, M04, M05, M08 | The patch body handles both non-DSA devices in `mtk_device_event` and QDMA queue speed selection. M05 has exact primary `rewrite` ownership for mixed DSA/non-DSA 10G behavior, while M08 has secondary QDMA/rate/performance/offload adjacency from M04. | M04/M05/M08 rows, global unack handoff row, and vendor `999-2727-net-ethernet-mtk_eth_soc-add-non-DSA-devices-handling.patch` body. | Yes. Decide an explicit M05-primary/M08-secondary split before implementation, or add a formal handoff note. |
| `001135` | `coherent-with-global-handoff` | M00, M06, M09 | M06 keeps this as a Wi-Fi enumeration `needs-evidence` row because direct 8X DTS/DTSO does not use `max-link-width`; M00 hands controller/expansion behavior to M09. Current M09 artifacts cover PCIe topology but not this controller max-link-width behavior. | M00/M06 rows, global unack handoff row, direct 8X DTS PCIe nodes, target PCIe controller source, and vendor `999-pcie-01` body. | Yes, or future M09 implementation must read the global handoff TSV. |
| `001136` | `coherent-with-global-handoff` | M00, M06, M09 | M06 correctly defers PCIe IRQ affinity/MSI grouping out of basic Wi-Fi bring-up; M00 also assigns it to M09. Current M09 artifacts cover static PCIe slots but not IRQ affinity, MSI group mapping, or controller-performance policy. | M00/M06 rows, global unack handoff rows from M00 and M06, direct 8X DTS PCIe nodes, target PCIe controller source, and vendor `999-pcie-02` body. | Yes, or future M09 implementation must read the global handoff TSV. |
| `001138` | `coherent-with-global-handoff` | M00, M06, M09 | M06 keeps Wi-Fi dependency as `needs-evidence`; M00 assigns generic PCIe power-management/controller behavior to M09. Current M09 artifacts do not explicitly cover exported PCIe soft off/on APIs or config access suppression while soft-off. | M00/M06 rows, global unack handoff row, direct 8X DTS PCIe nodes, target PCIe controller source, and vendor `999-pcie-04` body. | Yes, or future M09 implementation must read the global handoff TSV. |
| `001146` | `coherent-with-global-handoff` | M00, M09 | M00 correctly routes MediaTek TPHY PCIe 2-lane efuse support to M09, not Ethernet PHY work. Current M09 artifacts cover USB/PCIe topology, but not TPHY v4, lane1 efuse, or PCIe 2-lane efuse driver behavior. | M00 row, global unack handoff row, direct 8X DTS `tphy`/PCIe/USB context, target TPHY source, and vendor `999-tphy-01` body. | Yes, or future M09 implementation must read the global handoff TSV. |
| `001147` | `coherent-with-global-handoff` | M00, M09 | M00 correctly routes TPHY auto-load-valid behavior to M09. Current M09 artifacts do not explicitly cover `auto_load_valid`, `auto_load_valid_ln1`, nvmem cell reads, or skip/force efuse programming behavior in `phy-mtk-tphy`. | M00 row, global unack handoff row, direct 8X DTS `tphy`/PCIe/USB context, target TPHY source, and vendor `999-tphy-02` body. | Yes, or future M09 implementation must read the global handoff TSV. |
| `001148` | `coherent-with-global-handoff` | M00, M09 | M00 correctly routes TPHY USB3 PLL/SSC tuning to M09. Current M09 artifacts cover USB/PCIe static topology but not `mediatek,usb3-pll-ssc-delta*` parsing or U3 PHY PLL SSC register programming. | M00 row, global unack handoff row, direct 8X DTS USB/TPHY context, target TPHY source, and vendor `999-tphy-03` body. | Yes, or future M09 implementation must read the global handoff TSV. |

## Phase Interpretation

The Phase 2 review has full structural coverage of the 1181 diff files. The main gap is not missing review rows; it is that cross-step owner handoffs are distributed across source-step TSVs and markdowns. Future implementation must use `P2-owner-step-worklist.tsv` filtered by `owner_step`, not only the per-step TSV.

## Closeout State

The recommended no-context global handoff bucket audit has been completed and
the accepted bucket remediation has been applied. No migration implementation,
build, boot, flash, install, sysupgrade, or runtime success is claimed by this
closeout.
