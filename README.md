# bpi-r4-pro-8x-migration-notes

Notes, rules, review matrices, and reproducible helper scripts for the BPI-R4
Pro 8X OpenWrt 25.12 migration.

Start with:

- `project_guidelines.md`: project phases, source authority, and review rules.
- `repository_map.md`: local source tree roles and generated artifact map.
- `migration_roadmap.md`: migration-step order M00-M11.
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
