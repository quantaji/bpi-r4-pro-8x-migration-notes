# BPI-R4 Pro 8X OpenWrt 25.12 Migration Project Guide

## 1. Project Goal

This project migrates the BPI-R4 Pro 8X vendor OpenWrt 24.10 implementation to a clean OpenWrt 25.12.4 implementation.

The goal is not to mechanically copy vendor patches. The goal is to preserve the real hardware behavior of the BPI-R4 Pro 8X while re-expressing that behavior using OpenWrt 25.12 structure and upstream-compatible design principles.

The final result should be suitable for later migration to ImmortalWrt 25.12, but ImmortalWrt-specific changes are not part of the initial hardware bring-up.

This project is not a minimal-change port. It is a systematic migration and redesign where needed.

## 2. Source Roles

The project uses several source trees, but they do not have the same authority.

The BPI-R4 Pro 8X vendor tree is the primary behavior source. It shows what the vendor implementation tried to support, but it is not automatically a good implementation.

OpenWrt 25.12.4 is the target structure source. Final code should be organized as a clean delta against this tree.

OpenWrt 24.10 upstream is the baseline used to understand what the BPI 8X vendor tree changed.

MTK OpenWrt feed and the applied MTK trees are SoC vendor references. They help identify whether a change came from MTK, whether MTK has a newer 25.12 version, and whether a BPI change is board-specific or inherited from the MTK SDK.

BPI-R4 Pro 4E, BPI-R4, and BPI-R4 Lite are reference vendor trees. They are used to classify commonality and vendor style. They are not primary behavior sources for the 8X.

Linux, U-Boot, mt76, and OpenWrt main are provenance references. They are used to check whether a change already exists upstream or should be represented as an upstream backport.

## 3. Core Method

The project should not start by reading every repo-to-repo diff.

The main analysis unit is a changed file or hunk from the BPI-R4 Pro 8X vendor tree relative to OpenWrt 24.10 upstream.

Each changed file or hunk should be tagged for source, scope, function, target status, risk, and intended action. The tag definitions belong in a separate tagging guide.

The tags decide which reference source needs to be inspected. This avoids treating all repositories and all diffs as equally important.

The project is file-driven first, then cluster-driven, then migration-driven.

The primary review input is the vendor delta `A - B`, where `A` is the
BPI-R4 Pro 8X vendor OpenWrt 24.10 tree and `B` is upstream OpenWrt 24.10.
Using the delta as the analysis unit prevents unmodified upstream baseline code
from being mistaken for vendor behavior. The full vendor tree `A` is still
needed to resolve full-file context, added files, generated image recipes,
hardware DTS truth, and deleted-file interpretation. The baseline tree `B`
explains what the diff removed or changed. Provenance and migration decisions
should therefore start from the row/patch in `A - B`, then consult `A`, `B`,
target OpenWrt 25.12, MTK trees, sibling vendor trees, and upstream references
as evidence sources.

## 4. Project Phase 1: Diff and Tag

Project Phase 1 builds an inventory of the BPI-R4 Pro 8X vendor delta.

The input is the diff between the BPI-R4 Pro 8X vendor tree and OpenWrt 24.10 upstream.

The purpose is to identify what changed, where each change likely came from, what function it serves, how broadly it applies, and what should happen to it in OpenWrt 25.12.

Project Phase 1 does not migrate code. It produces a structured inventory that later Project Phases and migration steps can rely on.

Expected outputs:

```text
analysis/8x_changed_files.csv
analysis/8x_file_tags.csv
analysis/8x_file_decisions.csv
````

## 5. Project Phase 2: Cluster Diff

Project Phase 2 groups tagged files and hunks into functional clusters.

A cluster represents a complete hardware or software behavior. It is not simply a directory or patch file.

Examples of clusters include boot chain, storage and sysupgrade, MAC address handling, DTS structure, Ethernet MAC and PCS, DSA switch, PHY support, SFP and RJ45 combo behavior, Wi-Fi, modem support, hardware acceleration, LEDs, buttons, fan, and image recipe.

For each cluster, determine which files belong to it, what hardware behavior it represents, what comes from MTK, what is BPI-specific, what is shared with other boards, what OpenWrt 25.12 already supports, and what remains uncertain.

Project Phase 2 should separate hardware facts, vendor behavior, MTK SDK implementation, OpenWrt target structure, upstream implementation, and temporary workarounds.

Expected outputs:

```text
analysis/clusters/<cluster-name>.md
```

## 6. Project Phase 3: Cluster Migration

Project Phase 3 migrates clusters into OpenWrt 25.12.

Migration happens cluster by cluster, not by vendor patch order.

The implementation should preserve hardware behavior while preferring OpenWrt 25.12 structure and upstream-compatible abstractions.

Vendor code may be reused only when it is correct, necessary, and maintainable. MTK code may be used as reference, but it is not automatically final. Temporary hacks must be isolated and documented.

Unrelated clusters should not be mixed in one patch. Hardware acceleration should not be prioritized before basic correctness. Dynamic SFP/RJ45 combo behavior should not be attempted before static modes are understood.

Each commit must be reviewed for accidental minimal-change behavior. If a commit only preserves vendor structure because it is the shortest path, it should be rewritten unless the shortcut is explicitly justified as a temporary, isolated, documented workaround.

Expected outputs:

```text
patch-series/
tests/<cluster-name>-test-report.md
known-limitations.md
```

## 7. General Principles

Do not use minimal change as the guiding principle.

This project is not trying to produce the smallest possible diff that makes the board boot. A minimal patch can be worse than a larger patch if it preserves the wrong abstraction, hides vendor hacks, mixes unrelated concerns, or makes future maintenance harder.

Every change should be judged by hardware correctness, OpenWrt 25.12 structure, upstream compatibility, testability, and long-term maintainability. A change is not better merely because it is smaller.

Before accepting each commit, explicitly check whether the commit is following a minimal-change shortcut against the project instructions. If it is, reject or rewrite it unless there is a documented reason to keep the minimal form temporarily.

Every Project Phase review, migration-step review, checkpoint, and commit review must check for unreported minimal-change behavior. If a change or decision used a minimal shortcut without explicitly reporting it, documenting why it was accepted, and assigning a follow-up TODO, the review is incomplete.

Do not use "minimal fix" as an excuse to avoid reading context. Before choosing an implementation strategy, inspect the relevant vendor files, target OpenWrt 25.12 files, feature-routing records, and cluster notes. If the context has not been inspected, the correct action is to inspect it, not to guess a small patch.

Work must be bounded by the current migration objective, but the current objective must still be completed properly. Do not pre-implement the next migration step only because it is nearby. Do not under-implement the current migration objective only because a smaller local change appears to pass an immediate test.

When a minimal or incomplete implementation is forced by missing evidence, hardware access, time, or dependency order, mark it explicitly. The marker must include:

1. what was intentionally left incomplete,
2. why the minimal form was accepted,
3. which evidence or test is missing,
4. which later Project Phase or migration step owns the follow-up,
5. a concrete TODO in the cluster notes, commit message, or known-limitations file.

Temporary minimal changes are allowed only when all of the following are true:

1. The limitation is explicitly documented.
2. The affected hardware behavior is understood.
3. The change is isolated from unrelated clusters.
4. There is a planned replacement or cleanup path.
5. The temporary nature is visible in the commit message or cluster notes.
6. A follow-up TODO names the owning Project Phase or migration step and the evidence required to close it.

Do not assume vendor code is correct.

Do not assume OpenWrt upstream code is perfect.

Do not assume MTK SDK code is clean.

Do not infer source from filename alone.

Do not migrate full repo diffs.

Do not let one large vendor patch define final patch granularity.

Do not treat `.config` as hardware truth.

Do not mix build profile changes with hardware support.

Do not hide uncertainty. Mark uncertain items explicitly and defer them until evidence is available.

## 8. Commit Review Rule

Every commit must answer these questions before it is accepted:

1. Which cluster does this commit belong to?
2. Which hardware or software behavior does it implement or preserve?
3. Is the implementation chosen because it is correct, or merely because it is the smallest diff?
4. Does it preserve any vendor or MTK workaround?
5. If it preserves a workaround, is the workaround isolated and documented?
6. Does the commit mix unrelated clusters?
7. Does the commit make future migration to OpenWrt main, Linux upstream, or ImmortalWrt harder?
8. What runtime evidence or test plan validates it?
9. Which relevant context files were inspected before choosing this implementation?
10. Does the commit finish the current objective without silently pulling in the next migration step?
11. If the implementation is intentionally minimal or incomplete, where is the TODO and which Project Phase or migration step owns it?

A commit that only minimizes local diff size without satisfying the project principles should be rejected.

## 9. Success Criteria

The project succeeds when the OpenWrt 25.12 implementation is:

1. behaviorally faithful to the BPI-R4 Pro 8X hardware,
2. cleaner than the vendor 24.10 implementation,
3. organized by functional clusters,
4. testable,
5. suitable for later ImmortalWrt migration,
6. free from unjustified minimal-change shortcuts.
