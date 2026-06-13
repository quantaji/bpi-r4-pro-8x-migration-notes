**Verdict:** accept-with-minor-edits

**Evidence Read:** `project_guidelines.md`, `repository_map.md`, `migration_roadmap.md`, `migration_step_batch_review_skill.md`; `P2-unacknowledged-owner-handoffs.tsv`, coverage plan JSON, `P2-owner-step-worklist.tsv`, `P2-cross-step-coherence-audit.md`; M00-M11 review markdowns and relevant `.files.tsv` rows. Also read actual patch/source bodies for `000051`, `000053`, `000825`, `000826`, `001054`, `001114`, `001120`, `001136`, `000225`, `000256`, `000289`, plus self-selected `000973`, `001052`, `001055`, `001059`, `001136`.

**Mechanical Checks:** pass. TSV has 173 data rows, 19 columns, all required columns present, and every row has `handoff_status=external-handoff-not-reacknowledged`.

**Rows Audited:** assigned non-covered rows `27,34-95,102,113-114,133-137,147,149-173`; assigned covered rows `3,6,11,12,18,19,97,98,99,101,108,111,115,124,148`; self-selected extras `96,100,103,104,142`.

**Bucket Summary Checked:** assigned rows: `true-owner-gap=93`, `covered-by-topic=15`, `global-worklist-only=2`, `needs-human-decision=1`, `wrong-owner-or-source=1`. Including extras: `covered-by-topic=20`, total checked `117`.

**Disagreements:**
- Row `148:M09<-M06:001136`, current `covered-by-topic`, proposed `true-owner-gap`.
  Patch body changes `pcie-mediatek-gen3.c` MSI grouping, IRQ mapping, and affinity handling. M06 explicitly hands this to M09 as PCIe IRQ affinity/controller-performance policy, but M09 owner artifacts only cover PCIe static slot/topology context and do not mention IRQ affinity/MSI/controller policy. Direct 8X DTS has PCIe nodes but no `msi_type` or `msi-map`. Reading only M09 would likely miss this row.
- Extra row `142:M09<-M00:001136`, same proposed change for the same reason.

**No-Issue Confirmations:** `000051` correctly stays `needs-human-decision` because it mixes Airoha PHY package closure, HNAT package closure, and M11 package validation. `001114` and `001120` correctly stay `global-worklist-only`: actual bodies are MT7988D RFB option-type-2 PCIe/Wi-Fi and MT7987 WED DTS support, not direct 8X truth. `000053` correctly stays `wrong-owner-or-source`; M11 already owns package closure, while M09 only depends on USB runtime validation. All `true-owner-gap` rows had no exact file-id match in the owner TSV/markdown checks and would be missed by owner-only reading. M05/M08 covered rows are semantically covered by exact owner topics such as M05 target-superseded PHY/EEE/backport/full-wired topics and M08 netfilter/HNAT/PPE/RSS/LRO/flow-offload topics.

**Residual Risk:** I did not dense-read every one of the 93 true-owner-gap bodies; I body-read the high-risk/suspicious rows and relied on TSV plus owner-artifact absence for the rest. The only requested edit is to backfill/rebucket `001136` PCIe IRQ affinity instead of treating M09 topic coverage as sufficient.
