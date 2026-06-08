# Feature Routing Skill

## 1. Purpose

This skill defines Phase 1a feature routing for the BPI-R4 Pro 8X migration.

The goal is to assign one or more `feature_tags` to each changed file in the
`8x-vs-openwrt24-base` diffset so later cluster work can answer:

```text
which files should I inspect for this migration feature?
which migration features does this changed file touch?
```

This phase does not decide provenance, applicability, migration action, or final
patch structure.

Do not output or store:

```text
origin
scope
mtk_version
deletion_reason
```

Those fields belong to later cluster analysis.

## 2. Inputs

Primary input:

```text
analysis/diffsets/8x-vs-openwrt24-base
```

Expected files:

```text
manifest.yaml
name-status.tsv
numstat.tsv
binary-files.txt
files/<changed-path>.patch
```

The per-file patch under `files/` is the preferred input for routing.

Reference source trees are not required for normal Phase 1a routing. Use them
only if a file cannot be routed from path, status, file kind, patch subject, or
inner patch targets.

## 3. Output Model

The canonical outputs are:

```text
files.jsonl
assignments.jsonl
```

`files.jsonl` contains one record per changed file.

`assignments.jsonl` contains one record per file-feature assignment.

Generated indexes such as `by-file/` and `by-feature/` must be derived from
the canonical JSONL files, not edited by hand.

## 4. File-Level Routing

The routing unit is a changed file.

A file may have multiple `feature_tags`.

Do not split by hunk in Phase 1a. If a file is clearly multi-purpose, attach
multiple feature tags and mark it for review.

Examples:

```text
DTS with storage and network nodes:
    dts:board:variant
    dts:overlay:storage
    dts:overlay:network

PHY driver package with firmware blob:
    network:phy:10gbase-t
    network:phy:multi-rate
    firmware:phy:runtime

hostapd patch touching MLO config:
    wireless:hostapd:build
    wireless:mlo:config
```

## 5. Evidence Levels

Use the weakest sufficient evidence level.

Allowed values:

```text
path
path+status
path+file-kind
path+keywords
patch-subject
patch-inner-target
patch-content-keyword
binary-path
manual-review
```

Meaning:

```text
path:
    the directory is sufficient for broad routing

path+status:
    deletion/addition/rename helps route the file

path+file-kind:
    extension or file kind helps route the file

path+keywords:
    filename keywords such as sfp, aqr, mxl, mlo, sim, wwan

patch-subject:
    the inner patch subject identifies the feature

patch-inner-target:
    target paths inside a *.patch identify the feature

patch-content-keyword:
    patch contents identify the feature but should be reviewed

binary-path:
    firmware/blob path identifies the feature

manual-review:
    feature was assigned after human or agent review
```

## 6. Confidence

Allowed values:

```text
high
medium
low
```

Use `high` when the path or patch target is specific and unambiguous.

Use `medium` when the feature is likely but should be checked during cluster
analysis.

Use `low` when a file needs review or the tag is a broad fallback.

## 7. Mechanical Seed Rules

The first pass should be mechanical.

Use:

```text
rules/feature-tags-v1.json
rules/feature-seed-rules-v1.json
scripts/phase-1-feature-route.py
```

Mechanical rules may use:

```text
status
path glob
path regex
file kind
binary file list
patch subject
inner patch target paths
content keywords
```

Mechanical routing creates seeded assignments. Seeded assignments are allowed
to be imperfect. They must remain auditable through `rule_ids` and evidence.

When a mechanical rule uses `text_regex`, prefer the narrowest useful
`text_scope`:

```text
path:
    outer diff path, old/new path, and file kind

patch_subjects:
    Subject lines found inside patch files

patch_targets:
    inner paths touched by a patch file

patch_content:
    full per-file patch text, including changed content
```

For kernel patch routing, use `path`, `patch_subjects`, and `patch_targets`
first. Use `patch_content` only when changed code text is genuinely needed;
otherwise patch headers, trailers, and unrelated context can cause false
feature tags.

## 8. Patch Files

For a changed file that is itself a `*.patch`, do not route only from the patch
file directory.

Use:

```text
outer changed path
inner Subject lines
inner diff target paths
obvious content keywords
```

Examples:

```text
target/linux/mediatek/patches-6.6/*.patch
    route from inner kernel target paths when available

package/network/services/hostapd/patches/*.patch
    wireless:hostapd:build
    plus wireless:mlo:config if subject/content mentions MLO/802.11be

package/kernel/mac80211/patches/*.patch
    wireless:mac80211:patch
    plus wireless:regulatory:db if regulatory/regdb content is present
```

If a patch is too broad or squashes many upstream patches, keep the broad feature
tag and mark `needs_review = true`.

## 9. DTS Files

DTS, DTSI, and DTSO files should be routed at file level in Phase 1a.

Use broad tags from filename, path, and obvious node keywords:

```text
dts:board:base
dts:board:variant
dts:overlay:storage
dts:overlay:network
dts:overlay:wifi
dts:overlay:cellular
dts:gpio:control
dts:partition:layout
dts:thermal:zone
dts:fan:pwm
```

Do not attempt full hardware interpretation in Phase 1a. Exact node semantics
belong to the DTS cluster.

## 10. Deleted Files

Deleted files still receive feature tags.

Examples:

```text
deleted hostapd patch:
    wireless:hostapd:build

deleted mac80211 patch:
    wireless:mac80211:patch

deleted repo metadata:
    source:tree:metadata
```

Do not store `deletion_reason` in Phase 1a.

## 11. Rename / Copy

For status `R*` or `C*`, route using both old and new paths plus patch subject
and inner target paths.

Mark `needs_review = true` because rename/copy may change patch order or package
application semantics.

## 12. Review Policy

After mechanical routing:

```text
1. Validate JSON and allowed tags.
2. Review unrouted files.
3. Review low-confidence assignments.
4. Review T3/high-risk feature groups before migration.
5. Build generated indexes from canonical JSONL.
```

High-risk groups include:

```text
boot:*
image:*
dts:*
storage:*
identity:*
network:*
firmware:phy:*
wireless:wifi-scripts:*
cellular:*
accel:*
```

Bulk wireless patch-stack routing may remain broad until the wireless cluster
is opened.

## 13. Final Checks

Before accepting Phase 1a output:

```text
1. Every changed file has a files.jsonl record.
2. Every assignment feature is listed in feature-tags-v1.json.
3. No record contains origin, scope, or mtk_version.
4. Files without feature tags are marked needs_review.
5. by-file and by-feature indexes are generated, not hand-written.
6. The validator exits cleanly or reports only known review items.
```
