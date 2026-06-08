# Phase Batch Review Skill

This skill defines how to review a migration phase batch after Phase 1a feature routing and Phase 1b phase routing.

It is used to answer:

```text
For this phase, which changed files are migration inputs, which are only evidence,
which must be deferred, and which should be dropped?
```

It does not migrate code.

## Inputs

Use these inputs for each review:

1. `analysis/phase-routing/<diffset>/by-phase/<phase>.json`
2. `analysis/phase-routing/<diffset>/summary/phase-file-index.tsv`
3. `analysis/diffsets/<diffset>/files/<path>.patch`
4. direct 8X vendor files under `reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel`
5. vendor-family files only as supporting references
6. target OpenWrt 25.12 files when deciding final migration design

## Output

Each batch review must produce:

1. a phase summary,
2. a direct 8X evidence summary,
3. a table assigning one disposition to each file,
4. TODOs for `defer`, `static-only`, and `needs-evidence`,
5. an explicit unreported-minimalism gate result.

## Dispositions

Use only the dispositions in `rules/disposition-tags-v1.json`.

Every disposition must be phase-local. A file may be `defer` in the current phase and later become `migrate` or `rewrite` in its owning later phase.

## Evidence Order

Use evidence in this order:

1. direct 8X vendor source,
2. vendor-family source,
3. MTK vendor source,
4. target OpenWrt 25.12 structure,
5. upstream discussion or implementation as background only.

Do not let upstream similar hardware decide 8X hardware behavior.

## Mandatory Gates

### Context Gate

Do not assign `migrate`, `rewrite`, or `drop` from filename alone when the file could affect 8X behavior. Inspect the relevant diff or vendor file.

### Polarity Gate

Separate `A`, `M`, `D`, and `R*` files before deciding disposition.

### Phase Boundary Gate

Do not pull later-phase behavior into the current phase. For example, SD boot can read NAND/eMMC evidence, but NAND/eMMC install belongs to the storage phase.

### Unreported Minimalism Gate

Every review must ask:

1. Did we skip context because the small answer looked obvious?
2. Did we preserve vendor structure only because it was the shortest path?
3. Did we under-complete the current phase to keep the change small?
4. Did we silently pull in next-phase behavior?
5. Did any deferred or incomplete decision lack a TODO?

If yes, the review is incomplete until it records the reason, missing evidence, owner phase, and TODO.

## Review Table Columns

Use this table shape:

```text
file_id
status
path
route_classes
features
disposition
owner_phase
evidence
notes
minimalism_gate
```

`owner_phase` is the current phase unless the disposition is `defer`, `static-only`, or `needs-evidence`.
