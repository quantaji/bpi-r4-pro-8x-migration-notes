# Phase 3 Implementation Protocol

This protocol governs Project Phase 3 implementation work for the BPI-R4 Pro
8X OpenWrt 25.12 migration.

Phase 3 does not mechanically replay vendor patches. Each migration step must
first reconstruct vendor behavior, then decide how that behavior should be
represented in OpenWrt 25.12, then implement and verify the selected design.

## Required Inputs

Before implementing a migration step, read these inputs:

1. `project_guidelines.md`
2. `migration_roadmap.md`
3. `repository_map.md`
4. `migration_step_reviews/8x-vs-openwrt24-base/P2-owner-step-worklist.tsv`
5. `migration_step_reviews/8x-vs-openwrt24-base/P2-unacknowledged-owner-handoffs.tsv`
6. the relevant `Mxx-*.md` and `Mxx-*.files.tsv`
7. `analysis/provenance/8x-vs-openwrt24-base/summaries/row-summary.tsv`
8. `analysis/provenance/8x-vs-openwrt24-base/summaries/file-summary.tsv`
9. `analysis/provenance/8x-vs-openwrt24-base/summaries/unresolved.tsv`
10. relevant 8X vendor, target OpenWrt 25.12, MTK, sibling vendor, and upstream files.

The Phase 2 review matrix and provenance outputs are navigation and evidence.
They do not replace implementation judgment.

## Required Work Order

Each migration step must proceed in this order.

### 1. Vendor Behavior Reconstruction

Summarize what the 8X vendor implementation is trying to make work.

The summary must identify:

1. hardware or software behavior,
2. direct 8X files involved,
3. vendor scripts, DTS/DTSO, packages, patches, image recipes, or configs involved,
4. MTK, sibling vendor, target OpenWrt, or upstream provenance evidence,
5. direct-only or unresolved provenance rows,
6. deleted rows and their deletion semantics,
7. known vendor workarounds, debug-only code, stale code, or broad SDK carry-over.

Do not infer behavior from filenames alone. Inspect the relevant diff patches
and source files.

### 2. Target 25.12 Design Review

Compare the vendor behavior against OpenWrt 25.12 structure.

The design review must answer:

1. Does OpenWrt 25.12 already provide this behavior?
2. Does MTK 25.12 provide a cleaner target-era version?
3. Is the vendor implementation board-specific, SoC-wide, SDK-wide, or stale?
4. Which part of the vendor behavior must be preserved for BPI-R4 Pro 8X?
5. Which part of the vendor implementation should be rewritten, dropped, or deferred?
6. Does the proposed design fit OpenWrt 25.12 APIs, directory layout, package structure, and testing model?
7. Does the design avoid preserving vendor structure only because it is the shortest path?

OpenWrt upstream, Linux upstream, U-Boot upstream, and mt76 upstream may guide
structure, APIs, and maintainability. They do not override direct 8X hardware
evidence.

### 3. Implementation Plan

Before editing code, write a short implementation plan in the chat or task
notes.

The plan must state:

1. files to modify,
2. files intentionally not modified,
3. expected build or runtime evidence,
4. migration-step boundary,
5. handoff rows from `P2-unacknowledged-owner-handoffs.tsv` that affect the step,
6. provenance unresolved rows that need manual attention,
7. temporary limitations and owning follow-up step, if any.

Do not implement adjacent future-step behavior unless the roadmap explicitly
requires it for the current step.

### 4. Code Changes

Implement the chosen design as a clean OpenWrt 25.12 delta.

Code changes must:

1. preserve real BPI-R4 Pro 8X hardware behavior,
2. prefer OpenWrt 25.12 structure over vendor 24.10 structure,
3. keep unrelated clusters separate,
4. isolate temporary workarounds,
5. avoid broad vendor patch-stack replay,
6. avoid `.config` as hardware truth,
7. keep deleted-row semantics explicit.

If vendor code is reused, document why it is correct, necessary, and
maintainable.

### 5. Verification

Each migration step must produce evidence appropriate to its boundary.

Examples:

1. M01 requires target/profile/image skeleton build evidence, not runtime success.
2. M02 requires SD boot evidence, not NAND/eMMC install evidence.
3. M04 requires basic wired management evidence, not full DSA/SFP/10G evidence.
4. M06 requires basic Wi-Fi hardware/radio detection evidence, not MLO/AFC policy success.
5. M10 is the first step allowed to validate NAND/eMMC install and sysupgrade behavior.

Do not claim hardware, build, boot, install, sysupgrade, acceleration, wired, or
wireless success without matching evidence.

### 6. Minimalism Gate

Every Phase 3 checkpoint and commit must explicitly check for unreported
minimal-change behavior.

Reject or rewrite the work unless any minimal or incomplete form is explicitly
documented with:

1. what is incomplete,
2. why the minimal form is accepted,
3. which evidence or test is missing,
4. which later migration step owns the follow-up,
5. where the TODO is recorded.

A small diff is not automatically better than a larger clean design.

## Required Per-Step Report

Each implementation step must end with a report containing these sections:

```text
Vendor Behavior Summary
Vendor Implementation Anatomy
Provenance Evidence
Target 25.12 Design Decision
Accepted Vendor Behavior
Rejected Or Deferred Vendor Implementation
Code Changes
Build Evidence
Runtime Evidence
Minimalism Gate
TODO And Residual Risk
```

If a section does not apply, state why. Do not omit it silently.

## Commit Acceptance Checklist

Before a commit is accepted, answer:

1. Which migration step and feature cluster does this commit implement?
2. Which 8X hardware or software behavior is preserved?
3. Which vendor files, diff rows, provenance rows, and target 25.12 files were inspected?
4. Is the design correct for OpenWrt 25.12, or merely the smallest copyable vendor delta?
5. Does the commit preserve any vendor or MTK workaround?
6. If a workaround remains, is it isolated, documented, and assigned a cleanup owner?
7. Does the commit mix unrelated migration steps?
8. Does the commit pull in a future step without a roadmap reason?
9. What build or runtime evidence validates the commit?
10. What remains unresolved?

If these questions cannot be answered, the commit is not ready.
