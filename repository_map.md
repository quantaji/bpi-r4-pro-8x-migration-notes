## Repository Map

This notes repository is the control plane for the migration. It stores project
rules, routing scripts, migration-step reviews, and audit evidence. The source
trees and generated diffsets live one directory above this repository.

### Notes Repository Layout

```text
./
├── archive/
├── migration_step_reviews/
├── rules/
├── schemas/
├── scripts/
├── feature_migration_step_map.md
├── migration_roadmap.md
├── migration_step_batch_review_skill.md
├── phase3_implementation_protocol.md
├── project_guidelines.md
└── repository_map.md
```

#### `phase3_implementation_protocol.md`

Required workflow for Project Phase 3 implementation. It tells implementation
agents how to reconstruct vendor behavior, compare it with OpenWrt 25.12
structure, make design decisions, implement code, verify results, and pass the
minimalism gate. Read it before writing migration code.

#### `phase3_external_issue_watchlist.md`

External PR and observed issue watchlist for Project Phase 3. It records
possible integration problems by migration step, including OpenWrt PR sources
where applicable. It is warning evidence only; implementation agents must still
verify each issue against direct 8X vendor source, target OpenWrt 25.12 source,
hardware documents, and current runtime evidence before changing code.

#### `migration_step_reviews/8x-vs-openwrt24-base`

This directory stores Project Phase 2 review artifacts for the 8X vendor source
diff against OpenWrt 24.10.

The per-step files are the audited source-step review matrices:

```text
M00-*.md / M00-*.files.tsv
...
M11-*.md / M11-*.files.tsv
```

The global P2 files are implementation-entry indexes derived from the audited
M00-M11 matrices:

```text
P2-owner-step-worklist.tsv
P2-unacknowledged-owner-handoffs.tsv
P2-cross-step-coherence-audit.md
```

Their meanings:

- `P2-owner-step-worklist.tsv`: all M00-M11 review rows, regrouped by
  `owner_step`. This is the main implementation worklist for Project Phase 3.
  It preserves the source step that produced each row.
- `P2-unacknowledged-owner-handoffs.tsv`: the subset of owner handoffs that are
  present in a source-step TSV but not explicitly re-acknowledged by the owner
  step's own TSV or markdown. These rows are not missing from Phase 2; they are
  operational handoff risks for implementation agents that read only one
  per-step TSV.
- `P2-cross-step-coherence-audit.md`: human-readable closeout summary for the
  global owner-step worklist, handoff bucket audit, and targeted cross-step
  coherence checks.

Do not fold these global files back into the audited M00-M11 TSVs by default.
The per-step TSVs preserve the original review trace, while the P2 global files
are derived implementation indexes.

#### `rules`

Rules used by scripts and reviews.

- `p2-handoff-bucket-rules-v1.json` records the accepted bucket classifications
  for unacknowledged P2 handoffs after the global no-context audit. The
  classifications are audit decisions, not purely mechanical routing facts.

#### `scripts`

Reproducible helper scripts.

- `build-p2-owner-worklists.py` rebuilds `P2-owner-step-worklist.tsv` and
  `P2-unacknowledged-owner-handoffs.tsv` from the audited M00-M11 review TSVs
  and markdown files. By default it applies
  `rules/p2-handoff-bucket-rules-v1.json`.
- `build-row-provenance.py` builds row-level provenance evidence from the vendor
  diff rows. It compares the `A - B` diff signal against the configured source
  trees in `rules/provenance-sources-v1.json`, then writes candidate evidence
  and summary views under `../analysis/provenance/8x-vs-openwrt24-base/`.
  Same-path candidates are checked by default; use `--basename-search` for the
  canonical slower, higher-recall same-name scan.
- `build-phase3-worklists.py` builds the Phase 3 implementation index from the
  audited P2 owner-step worklist, global handoff overlay, and provenance
  summaries. It writes flat M00-M11 and queue views under
  `../analysis/phase3-worklists/8x-vs-openwrt24-base/`.

Example:

```sh
scripts/build-p2-owner-worklists.py
```

Use an output directory when checking reproducibility without overwriting the
committed artifacts:

```sh
scripts/build-p2-owner-worklists.py --output-dir /tmp/p2-owner-worklists-check
```

Example provenance run:

```sh
scripts/build-row-provenance.py
```

Canonical high-recall provenance run:

```sh
scripts/build-row-provenance.py --basename-search
```

Example provenance sample without overwriting canonical analysis output:

```sh
scripts/build-row-provenance.py --limit 20 --output-root /tmp/p2-row-provenance-sample
```

Example Phase 3 worklist run:

```sh
scripts/build-phase3-worklists.py
```

The provenance output is mechanical evidence. It should be reviewed before it
is used to decide whether a row is vendor-local, MTK-derived, upstreamed,
target-covered, or unknown. Direct 8X vendor matches are treated as postimage
confirmation, not as sole origin proof.

### Generated Analysis Artifacts

#### `analysis/provenance/8x-vs-openwrt24-base`

This directory is generated by `scripts/build-row-provenance.py`.

```text
analysis/provenance/8x-vs-openwrt24-base/
├── run.json
├── sources.snapshot.json
├── candidates/
│   ├── all-candidates.tsv
│   └── by-source/
└── summaries/
    ├── row-summary.tsv
    ├── file-summary.tsv
    ├── deleted-rows.tsv
    └── unresolved.tsv
```

Meanings:

- `candidates/all-candidates.tsv`: top-N source candidates per input row with
  per-source labels and metric fields.
- `candidates/best-by-source.tsv`: best candidate per input row and source.
  Use this when drilling down from `source_scores`; `all-candidates.tsv` is
  top-N output and may omit lower-ranked source-score entries.
- `candidates/by-source/*.tsv`: convenience views split by source type. These
  are derived from `all-candidates.tsv`.
- `summaries/row-summary.tsv`: one row per P2 owner-step row, with semicolon
  joined source scores and a conservative primary provenance summary.
- `summaries/file-summary.tsv`: one row per `file_id`, merging provenance across
  all owner/source steps.
- `summaries/deleted-rows.tsv`: deleted-row content/deletion-alignment evidence.
  Deletion action provenance is source-tree inference unless a later commit-level
  audit is performed. Rows with only medium target evidence are labeled as
  target-related, not as exact target-retained content.
- `summaries/unresolved.tsv`: rows that need human review because evidence is
  weak, direct-only, deletion-action inferred, binary without SHA256 exact match,
  or otherwise ambiguous.
- `run.json`: parameters, thresholds, input/output paths, and run counts.
- `sources.snapshot.json`: resolved source configuration used by the run.

#### `analysis/phase3-worklists/8x-vs-openwrt24-base`

This directory is generated by `scripts/build-phase3-worklists.py`.

```text
analysis/phase3-worklists/8x-vs-openwrt24-base/
├── README.md
├── run.json
├── phase3-worklist.tsv
├── M00.tsv
├── ...
├── M11.tsv
├── unacknowledged-handoffs.tsv
├── human-decision.tsv
├── provenance-review.tsv
├── direct-only.tsv
└── deleted-rows.tsv
```

Meanings:

- `phase3-worklist.tsv`: canonical Phase 3 implementation index. One row is a
  `file_id + owner_step + source_step` implementation row. A `file_id` may
  appear in multiple migration-step views when one changed file affects multiple
  features.
- `M00.tsv` through `M11.tsv`: flat owner-step views. `M00.tsv` is retained as
  an evidence/triage view; most implementation work starts from M01.
- `unacknowledged-handoffs.tsv`: rows with Phase 2 global handoff audit overlay.
- `human-decision.tsv`: rows that require human decision before implementation.
- `provenance-review.tsv`: rows whose provenance evidence is unresolved,
  direct-only, deletion-action inferred, short-signal, or otherwise requires
  manual review.
- `direct-only.tsv`: rows where direct 8X postimage is the only strong source
  evidence.
- `deleted-rows.tsv`: deleted rows and rows with deleted-row provenance classes.
- `run.json`: input paths, output paths, counts, and diagnostics.

#### `analysis/external-evidence/openwrt-pr-21083-bpi-r4-pro-8x`

Raw external evidence archive for OpenWrt PR #21083. It stores the PR metadata,
diff, patch, changed-file list, issue comments, review comments, reviews, and
timeline pages captured from GitHub.

Use this archive to understand upstream integration discussion, review
objections, and problem reports. Do not treat it as accepted upstream truth or
as BPI-R4 Pro 8X hardware authority.

Current local source workspace:

```text
./reference-source-codes
├── external-prs
│   └── openwrt-pr-21083-bpi-r4-pro-8x
├── MTK
│   ├── mtk-openwrt-feeds
│   ├── openwrt-21.02-mtk
│   ├── openwrt-24.10-mtk
│   └── openwrt-25.12-mtk
├── upstreams
│   ├── linux
│   ├── linux-v6.12.62
│   ├── linux-v6.12.87
│   ├── linux-v6.18
│   ├── linux-v6.6.104
│   ├── mt76
│   ├── openwrt-24.10.0
│   ├── openwrt-25.12.4
│   ├── openwrt-main
│   └── u-boot
└── vendors
    ├── BPI-R4Lite-OPENWRT-V24.10.0-Master-Devel
    ├── BPI-R4-MT76-OPENWRT-V21.02
    ├── BPI-R4PRO-4E-OPENWRT-V24.10.0-Master-Devel
    └── BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel
```

### MTK Sources

#### `MTK/mtk-openwrt-feeds`

This is the raw MediaTek OpenWrt feed and SDK integration source.

It is not just a normal OpenWrt package feed. It contains feed packages, OpenWrt tree overlays, base patches, feed patches, build recipes, and commit mapping information.

Use this repo to answer:

```text
Did a vendor change come from MTK?
Which MTK release line did it come from?
Does MTK have a newer version of the same functionality?
Is a file from MTK feed overlay, MTK base patches, MTK feed patches, or MTK package sources?
```

Do not treat MTK feed code as final quality. It is a SoC vendor reference.

#### `MTK/openwrt-21.02-mtk`

This is an applied MTK OpenWrt 21.02 reference tree.

Use it only when a change appears to come from older MTK SDK history or when checking old BPI-R4 MT76 vendor code.

It is not a target baseline for BPI-R4 Pro 8X 25.12 migration.

#### `MTK/openwrt-24.10-mtk`

This is the applied MTK OpenWrt 24.10 SDK reference tree.

Use it to classify BPI-R4 Pro 8X vendor changes.

Primary questions:

```text
Is this 8X vendor change inherited from MTK 24.10?
Did BPI modify an MTK 24.10 file?
Is this behavior MTK platform support or BPI board-specific support?
```

This is one of the most important reference trees for Phase 1 tagging.

#### `MTK/openwrt-25.12-mtk`

This is the applied MTK OpenWrt 25.12 SDK reference tree.

Use it to determine whether MTK already has a 25.12-era implementation of a feature that appears in the 8X vendor 24.10 tree.

Primary questions:

```text
Does MTK 25.12 already replace this 24.10 implementation?
Should the 25.12 port use MTK 25.12 as reference instead of BPI 24.10?
Was a 24.10 MTK patch dropped, split, renamed, or redesigned in 25.12?
```

This repo is a target-era reference, not the final target structure.

### Upstream Sources

#### `upstreams/openwrt-24.10.0`

This is the OpenWrt 24.10 upstream baseline.

Use it as the baseline for the first BPI-R4 Pro 8X vendor diff.

Primary use:

```text
BPI-R4PRO-8X vendor tree
vs
OpenWrt 24.10 upstream
```

This diff defines the initial changed-file inventory.

#### `upstreams/openwrt-25.12.4`

This is the OpenWrt 25.12 target baseline.

Final implementation should be structured as a clean delta against this tree.

Use it to answer:

```text
Does OpenWrt 25.12 already support this function?
What is the correct 25.12 directory structure?
What should the final patch series be based on?
```

This is the target source of truth for OpenWrt structure.

#### `upstreams/openwrt-main`

This is the current OpenWrt main reference.

Use it only as a lookup source.

Primary questions:

```text
Has OpenWrt main already accepted a newer version of this feature?
Is there a newer R4, Filogic, MxL switch, PHY, SFP, DSA, or MT7988 implementation?
Did a relevant PR already land after 25.12.4?
```

Do not use OpenWrt main as the target baseline unless the project goal changes.

### External PR Sources

#### `external-prs/openwrt-pr-21083-bpi-r4-pro-8x`

Checkout of the OpenWrt PR #21083 head branch for BPI-R4 Pro 8X board support.

Use it as an external integration reference for patch organization, review
context, and target-era design discussion. It is not merged upstream and must
not override direct 8X vendor source, schematic evidence, or current target
OpenWrt 25.12 API/structure.

#### `upstreams/linux`

This is the main Linux repository clone used to manage Linux worktrees.

Do not use it as a full diff input.

Use it for provenance and worktree management.

#### `upstreams/linux-v6.6.104`

This is the Linux kernel reference corresponding to the MTK 24.10 / kernel 6.6.104 SDK line.

Use it when checking whether a vendor 24.10 kernel patch is already in the base 6.6 kernel or was added by MTK/BPI.

#### `upstreams/linux-v6.12.62`

This is the Linux kernel reference corresponding to the MTK 25.12 / kernel 6.12.62 SDK line.

Use it when comparing MTK 25.12 kernel patches against their underlying Linux baseline.

#### `upstreams/linux-v6.12.87`

This is the Linux kernel reference corresponding to the OpenWrt 25.12.4 target kernel level.

Use it to check whether a Linux-side feature is already present in the target kernel version, even if OpenWrt packaging or patch layout differs.

#### `upstreams/linux-v6.18`

This is a newer Linux reference used to check later upstream implementations.

Use it for:

```text
PHY
DSA
phylink
PCS
SFP
SFP/RJ45 combo abstractions
MxL switch
AS21xxx PHY
RSS/LRO
crypto acceleration
offload-related driver work
```

This is a provenance and future-direction reference. It is not the target kernel.

#### `upstreams/u-boot`

This is upstream U-Boot.

Use it to check whether U-Boot patches in `package/boot/uboot-mediatek` are upstream, MTK downstream, BPI-specific, or temporary hacks.

Do not use it for OpenWrt userland files.

#### `upstreams/mt76`

This is the upstream mt76 wireless driver repository.

Use it for Wi-Fi, WED, BE14/BE19, firmware loading, EEPROM/calibration, and mt76-related provenance checks.

Do not use it for Ethernet, boot chain, sysupgrade, or board.d logic.

### Vendor Sources

#### `vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel`

This is the primary vendor source for the target board.

Use it as the behavior source for BPI-R4 Pro 8X.

The first analysis pass starts from its diff against `upstreams/openwrt-24.10.0`.

This tree is not trusted as final structure. It may contain vendor hacks, large unreviewable patches, build noise, stale files, or code inherited from MTK SDK.

#### `vendors/BPI-R4PRO-4E-OPENWRT-V24.10.0-Master-Devel`

This is the main R4 Pro family reference.

Use it to determine whether an 8X change is specific to 8X or shared across R4 Pro variants.

Primary questions:

```text
Is this change R4 Pro common?
Should the final 25.12 design use a shared R4 Pro DTSI or shared script logic?
Which network, storage, LED, fan, PCIe, or sysupgrade behavior is common across 8X and 4E?
```

Do not copy 4E networking behavior into 8X without checking the actual hardware topology.

#### `vendors/BPI-R4-MT76-OPENWRT-V21.02`

This is an older BPI-R4 MT7988 vendor reference.

Use it cautiously.

It can help identify older MT7988, MT76, boot, Wi-Fi, or BPI vendor patterns, but it is based on an older OpenWrt line and should not be treated as a direct 25.12 migration source.

If OpenWrt 25.12 already contains a better R4 implementation, prefer the OpenWrt 25.12 version as the structural reference.

#### `vendors/BPI-R4Lite-OPENWRT-V24.10.0-Master-Devel`

This is a BPI R4 Lite vendor reference.

Use it mainly for BPI vendor style and common script patterns.

It may help classify:

```text
BPI board.d style
BPI sysupgrade style
BPI LED/button conventions
BPI modem or USB package choices
BPI default package choices
```

Do not use it to infer BPI-R4 Pro 8X Ethernet, 10G combo, AS21010P, MxL86252, or MT7988-specific behavior.
