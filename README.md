# bpi-r4-pro-8x-migration-notes

Notes, rules, review matrices, and reproducible helper scripts for the BPI-R4
Pro 8X OpenWrt 25.12 migration.

Start with:

- `project_guidelines.md`: project phases, source authority, and review rules.
- `repository_map.md`: local source tree roles and generated artifact map.
- `migration_roadmap.md`: migration-step order M00-M11.
- `phase3_implementation_protocol.md`: required workflow for Phase 3
  implementation, design review, verification, and commit acceptance.
- `migration_step_reviews/8x-vs-openwrt24-base/`: Project Phase 2 review
  matrices and global handoff closeout artifacts.

To regenerate the Project Phase 2 owner-step worklists:

```sh
scripts/build-p2-owner-worklists.py
```

This rebuilds:

- `migration_step_reviews/8x-vs-openwrt24-base/P2-owner-step-worklist.tsv`
- `migration_step_reviews/8x-vs-openwrt24-base/P2-unacknowledged-owner-handoffs.tsv`

The bucket labels in the unacknowledged handoff TSV are applied from
`rules/p2-handoff-bucket-rules-v1.json`, which records the accepted global
handoff audit remediation.

To build row-level provenance evidence:

```sh
scripts/build-row-provenance.py --basename-search
```

The provenance scan starts from the vendor diff rows (`A - B`) and compares the
diff signal against configured reference sources in
`rules/provenance-sources-v1.json`. By default it writes reproducible analysis
artifacts to:

```text
../analysis/provenance/8x-vs-openwrt24-base/
```

The output includes candidate evidence, row/file summaries, deleted-row
summaries, unresolved rows, a source snapshot, and a run manifest. This is
mechanical provenance evidence, not a final migration decision. Omit
`--basename-search` for a faster same-path-only dry run.

To build the Phase 3 implementation worklists from audited Phase 2 and
provenance artifacts:

```sh
scripts/build-phase3-worklists.py
```

This writes the canonical Phase 3 implementation index and flat M00-M11/queue
views under:

```text
../analysis/phase3-worklists/8x-vs-openwrt24-base/
```
