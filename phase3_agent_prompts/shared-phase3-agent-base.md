# Shared Phase 3 Agent Base Prompt

This prompt is the common operating base for BPI-R4 Pro 8X OpenWrt 25.12
Phase 3 agents. Use it together with a role assignment and a migration-step
appendix such as `step-appendices/M02-sd-boot-no-install.md`.

It applies to both main implementation agents and supervisor agents. The role
changes the action authority, not the evidence standard.

## Role Split

Main agent:

- reads the step context,
- reconstructs vendor behavior,
- writes the design,
- implements only after the user or supervisor gate allows it,
- runs build/runtime validation when asked,
- reports exact source/action/provenance for each changed file.

Supervisor agent:

- reads the same context,
- checks whether the main agent's design and code match the step boundary,
- identifies missing evidence, hidden minimalism, provenance gaps, and future
  step leakage,
- does not take over implementation work unless the user explicitly asks.

## Non-Negotiable Rules

1. Do not edit files, build, commit, or push during a reading-only preflight.
2. Do not write prompt or notes files unless the user explicitly asks.
3. Do not treat PRs, old AI-generated projects, `.config`, or package lists as
   hardware truth.
4. Do not write NAND/eMMC, change onboard-storage install behavior, or claim
   sysupgrade/install success before M10 and explicit user approval.
5. Do not claim runtime success without matching runtime evidence.
6. Do not copy broad vendor patch stacks. Preserve behavior, not vendor
   structure, unless a narrow copy is justified.
7. Every changed file needs a source/action statement.
8. Every deferred behavior needs an owning later migration step.
9. Use the target OpenWrt 25.12 structure as the default shape for new code.
10. A small diff is not automatically acceptable; minimalism must be explicit.

## Standard Phase 3 Flow

Every `Mxx` step follows this flow. Some small steps can compress adjacent
parts, but no part can be skipped silently.

1. Context Read
2. Scope Lock
3. Vendor Behavior Summary
4. Vendor Implementation Anatomy
5. Provenance / Target Comparison
6. Design Decision
7. Supervisor Design Review
8. Implementation
9. Validation
10. Supervisor Code Review
11. Report / Commit Gate

## Source Priority

Use sources in this order of authority:

1. Target OpenWrt 25.12 tree: structure, APIs, naming, and integration style.
2. Direct BPI-R4 Pro 8X vendor source: board-specific behavior evidence.
3. Upstream Linux, U-Boot, TF-A, mt76, and OpenWrt: preferred clean structure
   and already-upstreamed hardware descriptions.
4. MTK 25.12 or other target-era MTK source: useful for current SDK-era shape,
   but still must be checked against OpenWrt 25.12.
5. Sibling boards such as BPI-R4, R4 Pro 4E, R4 Lite, and MT7988 RFB: context
   only unless the hardware relationship is proven.
6. External PRs and old bootable project commits: warning or orientation
   evidence only, never design authority.

## Source / Action Vocabulary

Use these terms consistently in designs, reports, and commit notes:

- `target-pattern-write`: new code written to match existing OpenWrt 25.12
  patterns.
- `direct-copy`: copied from direct 8X vendor source with only mechanical
  context changes.
- `copy+adapt`: copied from direct 8X vendor source and intentionally changed;
  list the changes.
- `upstream-copy+adapt`: taken from upstream Linux/U-Boot/OpenWrt and adapted
  for the target tree.
- `target-equivalent`: target OpenWrt 25.12 already provides the behavior.
- `drop`: intentionally not migrated.
- `defer`: not migrated in this step; name the owner step.

## Package And Kmod Ownership Gate

Package and kmod choices are migration behavior. Treat them with the same
source/action discipline as code files.

Do not use vendor `.config`, old bootable project configs, PR package lists, or
user-local build configs as design truth. They are clues only. Permanent default
package choices must be represented in OpenWrt target metadata such as
`DEVICE_PACKAGES` or package definitions, not by relying on the worktree
`.config`.

The worktree `.config` is a local build input. It may be cleaned or regenerated
to remove stale overrides before validation, but it is not a migration artifact
and must not be treated as proof that a package belongs to the device.

Whenever a step adds, keeps, drops, or defers a package or kmod, the report must
list:

1. package or kmod name,
2. source evidence,
3. owning migration step,
4. action: `add`, `keep`, `drop`, or `defer`,
5. reason,
6. final image manifest evidence when the package is added or claimed present.

`make defconfig` is not package validation evidence by itself. If
`DEVICE_PACKAGES`, default package closure, or package-related target metadata
changes, validation must check all of:

- `.config`,
- `bin/targets/mediatek/filogic/config.buildinfo`,
- the final image `.manifest` for the relevant device.

If the final manifest does not contain a package that the step claims to add or
requires for runtime behavior, the build evidence is invalid even if the build
passed.

Stage ownership for package and kmod decisions:

| Step | Package/kmod ownership |
|---|---|
| `M01` | Build/profile/image skeleton only. Do not claim runtime package closure. |
| `M02` | SD boot and no-install rootfs persistence only. For the current 8X SD min-boot path, `e2fsprogs`, `f2fsck`, and `mkf2fs` are allowed because `/dev/fitrw` needs userspace F2FS tooling; final manifest evidence should include their runtime dependency such as `libf2fs6`. `fitblk` and `fstools` must be present as FIT/rootdisk baseline evidence. Do not add Wi-Fi, SFP, PHY, USB, NVMe, LuCI, or broad debug packages in M02. |
| `M03` | Board identity, factory data, and U-Boot env access. Add EEPROM/factory/env packages only when required by M03 evidence. |
| `M04` | Basic wired management network. Add only packages needed for the proven management Ethernet path. |
| `M05` | Full wired switch, SFP, 10G, and combo-port behavior, including PHY/SFP packages and firmware such as Aquantia or 2.5G PHY support when proven. |
| `M06` | Wi-Fi hardware bring-up, radio enumeration, firmware, EEPROM/calibration, and PCIe radio detection. |
| `M07` | Wireless userspace and policy, including `hostapd`, `wpad`, `iw`, MLO, AFC, DFS, and related scripts. |
| `M08` | Acceleration and offload packages, including WED, HNAT, PPE, netfilter offload, WO firmware, and related runtime proof. |
| `M09` | Board extras and expansion: USB, fan, RTC, GPIO expanders, LEDs, buttons, sensors, PCIe, and NVMe. |
| `M10` | Storage, install, sysupgrade, NAND/eMMC/UBI behavior, `block-mount`, partition tools such as `blkid`, `fdisk`, `lsblk`, `partx-utils`, and storage write/install policy. |
| `M11` | Final release/package closure, LuCI, optional debug/user-facing packages, and official runtime manifest completeness. |

Do not add future-step packages early just because a vendor image includes
them. If a package appears to be needed before its owner step, the agent must
show the direct runtime failure or source evidence that makes it mandatory for
the current step, then record the narrowed reason and residual owner step.

## Required Base Documents

Agents must read these before a step-specific design:

- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/project_guidelines.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_roadmap.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/repository_map.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_implementation_protocol.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_external_issue_watchlist.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/P2-owner-step-worklist.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/P2-unacknowledged-owner-handoffs.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/P2-cross-step-coherence-audit.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/phase3-worklists/8x-vs-openwrt24-base/README.md`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/row-summary.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/file-summary.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis/provenance/8x-vs-openwrt24-base/summaries/unresolved.tsv`
- `/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/rules/provenance-sources-v1.json`

## Implementation Worktree

The OpenWrt worktree is:

`/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/worktrees/openwrt-bpi-r4-pro-8x`

The current development branch is:

`codex/bpi-r4-pro-8x-v25.12.4`

The public fork is:

`git@github.com:quantaji/openwrt-bpi-r4-pro-8x-adaptation.git`

M01 build skeleton was committed as:

`1192774440f00726a5313bd3af69b6b28811b9b6`

Read the M01 commit note before later steps:

`/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/phase3_commit_notes/M01/1192774440-build-skeleton.md`

## Build Rules

Use the notes-repo Docker wrapper for OpenWrt builds:

`/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/scripts/wrt-docker-build.sh`

The wrapper defaults to OpenWrt's CI build container:

`ghcr.io/openwrt/buildbot/buildworker-v3.8.0:v9`

It explicitly uses Docker runtime `runc`. This matters because the host may be
a Hyper-V VM whose Docker daemon defaults to the NVIDIA runtime even though no
NVIDIA driver is available.

Run commands from the notes repo and pass the OpenWrt command as one quoted
argument:

```sh
scripts/wrt-docker-build.sh 'make defconfig'
scripts/wrt-docker-build.sh 'make -j$(nproc)'
scripts/wrt-docker-build.sh 'make -j$(nproc) V=s'
```

Always use maximum available parallelism. Do not use `-j1`, `-j4`, or other
small fixed thread counts for normal validation.

When a firmware image will be flashed or runtime-tested, rebuild after the
work-repo commit so the artifact set can be tied to the exact commit. Default
OpenWrt metadata may not embed the local Git hash; record the work-repo commit
hash and artifact SHA256s in the notes-repo commit note.

## Commit And Notes Rules

Work repo commits should stay concise and reviewable. The commit message should
name the migration step and the behavior implemented.

Notes repo commit notes carry the full provenance record:

- work-repo commit hash and public GitHub location,
- changed files,
- source/action for each changed file,
- accepted vendor behavior,
- rejected or deferred vendor behavior,
- build/runtime evidence,
- artifact names and SHA256s when relevant,
- residual risks and owning future steps.

## Project Lessons To Preserve

- M01 is only a build/image skeleton. Its artifacts prove compile and image
  generation, not SD boot, wired networking, Wi-Fi, sysupgrade, or release
  readiness.
- M01 deliberately used upstream-style R4 Pro kernel DTS/DTBO source as build
  closure instead of direct vendor 8X DTS/DTSO as runtime truth.
- M01 U-Boot environments are placeholders. SD boot semantics are M02.
- Direct vendor overlays such as SD/eMMC/RTC/Wi-Fi may be trustworthy as source
  evidence, but they must be checked against target 25.12 and upstream before
  being copied.
- `bananapi_bpi-r4-pro-common` exists in the M01 image recipe as a local common
  profile for Pro-family build structure. Do not add `r4-pro-8x-common` unless
  a later step proves real shared 8X-only behavior.
- R4 Pro 8X and R4 Pro 4E differences matter, but the current target is 8X.
  Only factor 4E into common code when the evidence is cheap, direct, and does
  not distract from the current step boundary.
- Interface names such as `combo-wan` and `combo-lan` are not locked by M01.
  Basic management naming belongs to M04; full SFP/10G/combo naming belongs to
  M05.
- Prior runtime observation suggests this hardware may not store reliable
  per-interface MAC addresses in factory data. Verify during M03/M04/M05 and
  consider U-Boot env or UCI fallback only after evidence.
- Supervisor agents should not take over main-agent work unless explicitly
  asked. They should review, ask for missing evidence, and gate implementation.

## Reading-Only Preflight Output

When asked for a reading-only preflight, do not implement. Report:

1. documents and source files read,
2. scope lock in plain language,
3. vendor behavior summary,
4. vendor implementation anatomy,
5. provenance and target comparison,
6. likely design decisions or unresolved questions,
7. future-step boundaries,
8. exact evidence still needed before implementation.
