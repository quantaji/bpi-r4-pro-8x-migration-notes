# M05 Audit Round 1 Agent 3

**Verdict:** accept-with-minor-edits

**Evidence Read:** no prior audit logs read. I inspected the M05 review markdown/TSV, by-step JSON, step-file index, required rules/schema/roadmap/map, all assigned and cross-sample diff files, direct 8X DTS `mt7988a-bananapi-bpi-r4-pro-8x.dts`, target OpenWrt 25.12 AS21xxx firmware/driver package files, target MT7988 switch support, and vendor MxL86252 DSA/tag sources.

**Structural Checks:** PASS
- M05 JSON: 92 files, 254 feature assignments.
- TSV: 92 rows, 92 unique `file_id`.
- Coverage: no missing, extra, or duplicate IDs.
- Exact JSON/TSV parity: `status`, `path`, `file_kind`, `route_classes`, `features` all pass.
- Legal dispositions/owners: pass.
- `step-file-index.tsv`: 92 M05 rows, exact ID match.
- TSV counts: `A:88`, `M:4`; dispositions `rewrite:22`, `superseded-by-target:16`, `needs-evidence:15`, `review-only:13`, `drop:24`, `defer:1`, `static-only:1`.

**Semantic Checks:** PASS with minor edits below
- Direct 8X DTS file_id `000859` supports static topology only; I found no runtime success claim.
- Direct 8X evidence confirms SFP1/SFP2, AS21xxx PHY24/PHY28, `as21x1x_fw.bin`, MxL86252, `mxl862_8021q`, passive muxes, shared `mod-def0`, and multiple DSA members.
- AQR/CUX is not promoted to 8X hardware truth; direct 8X DTS has no AQR/CUX evidence.
- Target 25.12 really provides `kmod-phy-aeonsemi-as21xxx` and `aeonsemi-as21xxx-firmware`.
- Target 25.12 lacks MxL86252 DSA/tag/mux support.
- `001124` split is correct: M05 owns multiple-DSA/user-port behavior; M08 keeps PPPQ/QDMA/PPE/WED/offload.
- No M05 implementation pull-in found for Wi-Fi, storage/sysupgrade, NAND/eMMC, or acceleration.
- Assigned low-risk rows and cross-sample rows were checked against diff content and relevant source; dispositions are broadly sound.

**Findings:**
1. `000958` minor semantic overbreadth: [M05 TSV](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M05-full-wired-switch-sfp-and-10g.files.tsv:55) marks `net/dsa/tag_mxl862xx.c` as `rewrite` using direct 8X `mxl862_8021q` evidence, but this diff implements the non-802.1Q `mxl862` tag path. Direct 8X DTS selects `dsa-tag-protocol = "mxl862_8021q"` at the MxL CPU port. Suggested edit: narrow the row note to adjacent/fallback tag support, or make it `review-only` unless the chosen MxL driver design requires both tag paths.

2. `000869` wording cleanup: [M05 TSV](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M05-full-wired-switch-sfp-and-10g.files.tsv:40) describes `mt7988a-rfb-mxl86252.dts` as "RFB MxL/SFP overlays," but the diff content is SFP/passive-mux/AQR-oriented and contains no MxL switch/tag evidence. Since it is `review-only` and actual RFB MxL evidence is elsewhere, this is non-blocking wording cleanup.

**No-Issue Confirmations:**
- Assigned rows `000830`, `000835`, `000836`, `000838`, `000839`, `000854`, `000861`, `000874`, `001002`, `001012`, `001014`, `001015`, `001032`, `001061`, `001064`, `001066`, `001067`, `001069`, `001079` are acceptable.
- Cross-sample rows `000834`, `000837`, `001000`, `001001`, `001010`, `001013`, `001044`, `001078`, `001083` are acceptable.

**Residual Risk:** runtime behavior remains unproven for SFP, DSA, MxL86252, AS21xxx, 10G, VLAN, and mux behavior; the M05 document correctly treats direct DTS as topology evidence, not validation evidence.
