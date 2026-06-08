# Archived Legacy Semantic Tagging Skill

Archived on 2026-06-08.

This skill is not used for the current Project Phase 1a feature-routing pass. Project Phase 1a
now routes files by `feature_tags` only, using `feature_routing_skill.md`,
`rules/feature-tags-v1.json`, and `rules/feature-seed-rules-v1.json`.

The semantic workflow below is retained only as legacy reference for later
feature-cluster review, where origin, scope, applicability, and migration design
can be evaluated with more evidence.

# Diff File Analysis Skill

## 1. Purpose

This skill defines how an AI agent should analyze one changed file from an OpenWrt diffset.

The goal is to turn each changed file into one or more semantic modification records.

Each record should describe:

```text
what changed
what the change likely means
where it likely came from
how broadly it applies
which migration feature it serves
what evidence was used
what still needs lookup
```

This skill does not make final migration decisions.

Final migration decisions belong to cluster-level analysis.

## 2. Required Tag Reference

Do not redefine tag values in this file.

The complete tag definitions are in:

```text
tag_rules.md
```

Before assigning `origin`, `scope`, or `migration_feature`, read and follow that file.

This skill only explains when and how to apply those tags.

## 3. Available Source Trees

Reference source trees:

```text
reference-source-codes/
├── MTK/
│   ├── mtk-openwrt-feeds
│   ├── openwrt-21.02-mtk
│   ├── openwrt-24.10-mtk
│   └── openwrt-25.12-mtk
├── upstreams/
│   ├── linux
│   ├── linux-v6.6.104
│   ├── linux-v6.12.62
│   ├── linux-v6.12.87
│   ├── linux-v6.18
│   ├── mt76
│   ├── openwrt-24.10.0
│   ├── openwrt-25.12.4
│   ├── openwrt-main
│   └── u-boot
└── vendors/
    ├── BPI-R4Lite-OPENWRT-V24.10.0-Master-Devel
    ├── BPI-R4-MT76-OPENWRT-V21.02
    ├── BPI-R4PRO-4E-OPENWRT-V24.10.0-Master-Devel
    └── BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel
```

Available diffsets:

```text
analysis/diffsets/
├── 8x-vs-openwrt24-base
├── 8x-vs-mtk24-base
├── mtk24-vs-openwrt24-base
├── mtk25-vs-openwrt25-base
├── 4e-vs-mtk24-base
├── r4-vs-mtk21-base
├── mtk21-packages-patches-feeds
├── mtk24-packages-patches-feeds
└── mtk25-packages-patches-feeds
```

Primary diffset:

```text
analysis/diffsets/8x-vs-openwrt24-base
```

All first-pass analysis starts from the primary diffset.

Other diffsets are evidence sources, not primary reading targets.

## 4. Analysis Unit

Dispatch unit:

```text
one changed file
```

Tagging unit:

```text
one semantic modification
```

A semantic modification may be:

```text
one diff hunk
several adjacent hunks with one purpose
one added board case
one changed device definition
one deleted file
one package/config change with one clear purpose
one patch-file inner change
```

If a file has unrelated changes, split it into multiple semantic modification records.

If a file is small and single-purpose, one file-level record is acceptable.

## 5. Output Record Format

For each semantic modification, output:

```text
mod_id
file_path
status
unit_type
hunk_hint
short_description
origin
mtk_version
scope
migration_feature
deletion_reason
evidence
needs_lookup
notes
```

Field rules:

```text
origin:
    use tag_rules.md

mtk_version:
    use tag_rules.md

scope:
    use tag_rules.md

migration_feature:
    use tag_rules.md

deletion_reason:
    only for deleted files
    use "none" otherwise

needs_lookup:
    short list of missing checks
    use "none" if no further lookup is needed

notes:
    concise explanation
```

Example:

```text
mod_id: filogic.mk::bpi-r4-pro-8x-device-entry
file_path: target/linux/mediatek/image/filogic.mk
status: M
unit_type: semantic-hunks
hunk_hint: BPI device definition block
short_description: modifies Filogic image recipe for BPI-R4 Pro 8X
origin: mtk-plus-bpi
mtk_version: mtk-24.10
scope: 8x-only
migration_feature: image:device-recipe,image:dts-selection,openwrt:package:device-packages
deletion_reason: none
evidence: primary diff; similar image structure in MTK24
needs_lookup: compare MTK25 filogic.mk during image-recipe cluster analysis
notes: final rewrite decision belongs to cluster analysis
```

## 6. Top-Level Decision Tree

For each changed file:

```text
1. Read file status from name-status.tsv.
   Status may be A, M, D, R, or C.

2. If status is D:
   use Deletion Flow.
   Usually one deleted file becomes one record.

3. If status is A or M:
   use Modification / Addition Flow.
   Split into semantic modifications if the file contains multiple purposes.

4. If status is R or C:
   use Rename / Copy Rule.
   Analyze old path, new path, whether content changed, and whether the move changes build behavior.

5. If file is binary/firmware:
   do not rely on textual diff.
   Analyze package metadata, install path, runtime loader, and version/source if available.

6. Assign origin, scope, and migration_feature for each semantic modification.

7. Record evidence and lookup needs.
```

## 6.1 Rename / Copy Rule

For status `R` or `C`, do not treat the file as a normal addition.

Analyze:

```text
old path
new path
whether content changed
whether the move changes build behavior or only file location
```

If the file was only renamed or copied without semantic change, create a path-movement record.

If the renamed/copied file also changed semantically, create semantic modification records for the changed hunks.

For copied files, also check whether the copied content becomes a new board/device/package behavior or is only reused infrastructure.

## 7. Evidence Layers

Use three evidence layers.

```text
Layer 1: diff hunk
Layer 2: old and new full file
Layer 3: inner target source context, if the changed file is a *.patch
```

Default rule:

```text
start with diff
read full files if context is needed
reconstruct or inspect patch target source only for high-risk or migration-relevant patches
```

## 7.1 Full-File Context Rule

When full-file context is required, read both old and new full files.

Reading only the new file is insufficient for determining whether a change is new vendor behavior, inherited upstream behavior, or a context-only change.

This rule especially applies to:

```text
filogic.mk
board.d scripts
platform.sh
uboot-envtools
U-Boot Makefile
DTS/DTSI/DTSO
wifi-scripts
hostapd.uc
wpa_supplicant.uc
kernel module Makefiles
```

## 8. Ordinary File Analysis

For ordinary source/script/Makefile/config files:

```text
1. Read per-file patch.
2. Identify changed hunks.
3. Decide whether hunks are one semantic modification or several.
4. If meaning is unclear, read old full file and new full file.
5. Assign tags per semantic modification.
```

Diff alone is enough only when:

```text
file is small
change is local
all hunks serve one clear purpose
the surrounding file structure is irrelevant
```

Read old and new full files when:

```text
file contains multiple board cases
hunk depends on shell case structure or variables
hunk affects fallback/default behavior
hunk may affect boards other than 8X
diff omits important context
file is high-risk
```

Files that usually require full-file context:

```text
target/linux/mediatek/image/filogic.mk
target/linux/mediatek/filogic/base-files/etc/board.d/02_network
target/linux/mediatek/filogic/base-files/etc/board.d/01_leds
target/linux/mediatek/filogic/base-files/lib/upgrade/platform.sh
package/boot/uboot-mediatek/Makefile
package/boot/uboot-envtools/files/mediatek_filogic
package/network/config/wifi-scripts/*
package/network/services/hostapd/files/*.uc
package/kernel/linux/modules/*.mk
kernel config files
```

## 9. DTS / DTSI / DTSO Analysis

DTS-class files almost always require full context.

For:

```text
*.dts
*.dtsi
*.dtso
```

Read:

```text
per-file diff
old full file
new full file
relevant include files
base DTS/DTSI referenced by overlays
labels or paths targeted by overlays
```

Why:

```text
node meaning depends on parent node
phandles and labels matter
overlay target matters
port graph matters
pinctrl, regulator, clock, reset, interrupt, nvmem, partition context matters
```

Split DTS modifications by hardware node or behavior:

```text
partition layout
nvmem cells
Ethernet MAC/PCS/PHY
SFP cage
GPIO mux
PCIe slot
USB hub
fan/thermal
LED/button
Wi-Fi slot
cellular slot/SIM
regulator/power control
MDIO/I2C/SPI bus
```

Do not tag an entire board DTS as one semantic modification if multiple hardware areas changed.

## 10. Patch File Analysis

If the changed file is itself a `*.patch`, distinguish two layers.

```text
outer diff:
    how the patch file changed between two OpenWrt trees

inner patch:
    what the patch applies to kernel/U-Boot/package source
```

Examples:

```text
target/linux/mediatek/patches-6.6/*.patch
package/boot/uboot-mediatek/patches/*.patch
package/kernel/mac80211/patches/*.patch
package/network/services/hostapd/patches/*.patch
```

For `*.patch` files:

```text
1. Read outer diff.
2. Classify patch file status:
   added, deleted, modified, copied, renamed, refreshed.
3. Read inner patch content.
4. Identify target files modified by inner patch.
5. Assign migration_feature mainly from inner patch semantics.
6. Use target source context when needed.
```

Important:

```text
origin/scope may use outer diff evidence.
migration_feature must use inner patch semantics.
```

Example:

```text
outer file:
    target/linux/mediatek/patches-6.6/777-foo.patch

inner patch:
    modifies drivers/net/phy/as21xxx.c

migration_feature:
    network:phy:10gbase-t, firmware:phy:runtime
```

## 10.1 Patch File Full-Context Rule

If the changed file is a `*.patch`, do not rely only on the outer diff.

For modified `*.patch` files, read:

```text
outer diff
old full patch file
new full patch file
inner patch target paths
target source context when needed
```

The outer diff explains how the patch file changed. The old and new full patch files explain what each patch version actually does.

For deleted `*.patch` files, inspect the deleted patch content if it touches high-risk subsystems. A deleted patch may represent removed kernel, U-Boot, package, driver, DTS, firmware, or runtime behavior.

For added `*.patch` files, inspect the full added patch and its inner target paths before assigning `migration_feature`.

For renamed or copied `*.patch` files, analyze both path movement and semantic content change. A moved patch may change patch order or package application semantics even when content is unchanged.

## 11. When to Reconstruct Patch Target Source

Do not reconstruct every patch.

Use three levels.

### Level 1: read patch only

Use when:

```text
patch is low-risk
patch is clearly unrelated to 8X
patch is part of bulk wireless/package deletion
patch is a simple context refresh
patch content contains enough context
```

### Level 2: read patch plus target source

Use when:

```text
patch touches relevant subsystem
patch is medium-risk
patch target function context matters
patch may be reused or compared
```

Read:

```text
patch file
target source in OpenWrt 24.10
target source in OpenWrt 25.12
Linux/U-Boot/mt76 upstream target source if relevant
```

### Level 3: reconstruct inner old/new source

Use when:

```text
patch is high-risk
patch is migration candidate
patch semantics are unclear
patch modifies multiple subsystems
patch touches network/PHY/DSA/SFP/combo/MTD/sysupgrade/firmware/Wi-Fi7/WED/cellular/boot
```

Generate or inspect:

```text
inner-old-file
inner-new-file
inner-diff
```

Caution:

```text
OpenWrt kernel patches apply on top of OpenWrt patch stack, not plain Linux.
U-Boot package patches apply on top of package source plus earlier package patches.
For serious migration, patch order matters.
```

## 12. High-Risk Patch Targets

Patch files require deeper analysis if the inner patch touches:

```text
drivers/net/
drivers/net/phy/
drivers/net/dsa/
drivers/phy/
net/dsa/
phylink
PCS
SFP
MDIO
PPE
HNAT
WED
TOPS
crypto/EIP
MTD
NAND
NMBM
UBI
partition code
DTS bindings
DTS files
U-Boot board files
U-Boot storage/env/bootmenu/recovery
mt76
Wi-Fi 7 / MLO
hostapd runtime behavior
cellular modem support
firmware loading
```

## 13. Deletion Flow

A deletion means:

```text
OLD tree has this file.
NEW tree does not.
```

Do not automatically interpret deletion as intentional hardware behavior.

For the primary diff:

```text
OLD = OpenWrt 24.10 upstream
NEW = BPI-R4 Pro 8X vendor
```

A deleted file means OpenWrt had it, vendor tree does not.

For `8x-vs-mtk24-base`:

```text
OLD = openwrt-24.10-mtk
NEW = BPI-R4 Pro 8X vendor
```

A deleted file means MTK24 applied tree had it, vendor tree does not.

This is evidence of absence, not proof of intentional removal.

## 14. Deletion Reasons

Use `deletion_reason`.

Allowed values:

```text
none
repo-metadata-pruned
build-artifact-pruned
external-feed-pruned
baseline-mismatch
vendor-tree-trimmed
package-stack-divergence
wireless-stack-divergence
replaced-elsewhere
obsolete-upstream-file
intentional-disable
high-risk-removed-support
unknown
```

Definitions:

```text
repo-metadata-pruned:
    .github, .devcontainer, CI metadata, repository housekeeping.

build-artifact-pruned:
    generated files, build output, cache, downloads.

external-feed-pruned:
    files under external feeds/ checkout.

baseline-mismatch:
    deletion likely caused by comparing different source commits.

vendor-tree-trimmed:
    vendor tree appears to omit upstream files to reduce or reshape source.

package-stack-divergence:
    package patch/source organization differs from upstream.

wireless-stack-divergence:
    large deletions under mac80211, hostapd, iw, wireless patch stacks.

replaced-elsewhere:
    same logic appears in another file/path/package.

obsolete-upstream-file:
    file absent or replaced in OpenWrt 25.12 or newer upstream.

intentional-disable:
    explicit evidence vendor disabled functionality.

high-risk-removed-support:
    deleted file may affect 8X hardware support.

unknown:
    reason unclear.
```

## 15. Deletion Decision Tree

```text
D1. Is the deleted path repository metadata?
    yes:
        deletion_reason = repo-metadata-pruned
        origin = build-noise
        scope = build-only
        migration_feature = source:tree:metadata
        stop.

D2. Is it generated/build/cache/download output?
    yes:
        deletion_reason = build-artifact-pruned
        origin = build-noise
        scope = build-only
        migration_feature = source:tree:cleanup
        stop.

D3. Is it inside external feeds/?
    yes:
        deletion_reason = external-feed-pruned
        origin = build-noise
        scope = build-only
        migration_feature = source:feeds:external-feed-config
        stop unless specifically requested.

D4. Is it large package/wireless patch-stack deletion?
    yes:
        deletion_reason = wireless-stack-divergence or package-stack-divergence
        create one record per file
        do not deep-read each file unless a cluster depends on it.

D5. Is it in a high-risk path?
    yes:
        deletion_reason = high-risk-removed-support or unknown
        assign migration_feature based on path
        inspect same path in relevant references.

D6. Does OpenWrt 25.12 also lack this file or has replacement?
    yes:
        deletion_reason = obsolete-upstream-file or replaced-elsewhere.

D7. Is there explicit evidence of disabling?
    yes:
        deletion_reason = intentional-disable.

D8. Otherwise:
        deletion_reason = baseline-mismatch, vendor-tree-trimmed, or unknown.
```

High-risk deletion paths:

```text
target/linux/mediatek/*
package/boot/*
package/kernel/mt76/*
package/firmware/*
package/network/config/wifi-scripts/*
package/network/services/hostapd/Makefile
package/network/services/hostapd/files/*
package/kernel/linux/modules/*
scripts/mkits.sh
include/image-commands.mk
```


Deleted `*.patch` files require extra care. If a deleted patch touched high-risk subsystems, parse the deleted patch content and classify by its inner patch target before assigning a final deletion reason.

## 16. Modification / Addition Flow

For status `M` or `A`:

```text
1. Read per-file patch.
2. Identify semantic purposes.
3. Split if multiple purposes exist.
4. Read full files if context is needed.
5. Read reference sources only when needed.
6. Assign origin, scope, migration_feature.
7. Record evidence and lookup needs.
```

File-level tagging is enough when:

```text
file is small
file has one clear purpose
all hunks serve one function
Makefile change is single-purpose
single DTS overlay has one behavior
```

Split into semantic modifications when:

```text
file contains multiple board cases
file contains multiple hardware areas
file changes both build and runtime behavior
file changes both package selection and image recipe
patch file modifies multiple target source files
DTS file changes several independent nodes
```

## 17. Semantic Split Rules

Split by purpose, not raw hunk count.

Use one record for:

```text
one board case
one device definition
one DTS node group
one DTS overlay behavior
one U-Boot target
one image recipe block
one sysupgrade behavior
one network default behavior
one MAC/factory-data behavior
one kernel driver function
one kernel module definition
one package build option
one firmware inclusion
one userspace script behavior
```

Combine adjacent hunks if they serve one purpose.

Split adjacent hunks if they serve different purposes.

## 18. Origin Decision Tree

For each semantic modification:

```text
O1. Is it build/repo noise?
    yes -> origin=build-noise.

O2. Is the same or equivalent modification in OpenWrt 25.12?
    yes -> origin=openwrt-upstream.

O3. Is it in OpenWrt main but not 25.12?
    yes -> origin=openwrt-main.

O4. Is it in MTK 24.10 feed or openwrt-24.10-mtk?
    yes:
        if vendor is materially same:
            origin=mtk-inherited
            mtk_version=mtk-24.10
        if vendor adds BPI-specific behavior:
            origin=mtk-plus-bpi
            mtk_version=mtk-24.10

O5. Is closest visible version in MTK 25.12?
    yes:
        origin=mtk-inherited or mtk-plus-bpi as appropriate
        mtk_version=mtk-25.12
        note as target-era reference if not proven vendor source.

O6. Is closest visible version in MTK 21.02?
    yes:
        origin=mtk-inherited or mtk-plus-bpi as appropriate
        mtk_version=mtk-21.02

O7. Is it a Linux kernel backport?
    check linux-v6.6.104, linux-v6.12.62, linux-v6.12.87, linux-v6.18, linux master
    if found -> origin=linux-upstream-backport, mtk_version=none.

O8. Is it a U-Boot upstream backport?
    check upstreams/u-boot
    if found -> origin=uboot-upstream-backport, mtk_version=none.

O9. Is it mt76-specific and present in upstreams/mt76?
    yes -> origin=mt76-upstream-backport, mtk_version=none.

O10. Does it appear copied or adapted from another BPI board?
    check 4E, R4, Lite
    if yes -> origin=bpi-other-board.

O11. Is it only visible in BPI 8X vendor tree?
    yes -> origin=bpi-only.

O12. Otherwise -> origin=unknown.
```

Use semantic equivalence, not only same path.

Do not infer origin from filename alone.

## 19. Scope Decision Tree

For each semantic modification:

```text
S1. Is it build/repo noise only?
    yes -> scope=build-only.

S2. Is it generic OpenWrt behavior affecting many targets?
    yes -> scope=openwrt-generic.

S3. Is it explicitly BPI-R4 Pro 8X-specific?
    evidence:
        8X device name/compatible
        8X image recipe
        8X port layout
        8X 10G SFP/RJ45 combo
        AS21010P or MxL86252 behavior specific to 8X
    yes -> scope=8x-only.

S4. Does same semantic behavior appear in BPI-R4 Pro 4E?
    yes -> scope=r4-pro-common.
    require semantic similarity, not only same file path.

S5. Does same semantic behavior apply to MT7988 boards generally?
    evidence:
        also in BPI-R4 or OpenWrt R4
        MT7988 Ethernet/PCS/PPE/WED/PCIe/SNAND/clock/pinctrl/thermal
    yes -> scope=mt7988-common.

S6. Does it apply across broader Filogic family?
    evidence:
        similar logic across MT7981/MT7986/MT7987/MT7988
        generic Filogic image/storage/board.d/package/driver pattern
    yes -> scope=filogic-common.

S7. Is it only BPI vendor style shared across boards?
    evidence:
        similar shell style
        similar package/default config
        similar vendor patch organization
        no clear shared hardware behavior
    yes -> scope=bpi-style-common.

S8. Otherwise -> scope=unknown.
```

## 20. Migration Feature Assignment

Assign one or more `migration_feature` tags using `tag_rules.md`.

Rules:

```text
use domain:subsystem:function
use router-generic tags
do not bind too early to 8X-specific chips or ports
concrete 8X hardware binding belongs to cluster metadata
```

Use path as a hint, not proof.

Common path hints:

```text
package/boot/arm-trusted-firmware-mediatek/*
    boot:tf-a:*

package/boot/uboot-mediatek/*
    boot:uboot:*

package/boot/uboot-envtools/*
    boot:uboot:env
    identity:uboot-env:ethaddr
    storage:sysupgrade:platform

target/linux/mediatek/image/*
    image:device-recipe
    image:dts-selection
    image:fit
    image:factory-image
    image:sysupgrade-image
    openwrt:package:device-packages

target/linux/mediatek/files-*/arch/*/boot/dts/*
    dts:*
    network:*
    storage:*
    bus:*
    thermal:*
    ui:*
    cellular:* if modem/SIM/WWAN slots are described

target/linux/mediatek/patches-*/*
    depends on inner patch content

target/linux/mediatek/*/base-files/etc/board.d/02_network
    openwrt:board-d:network
    network:port-label:lan-wan
    network:default-config:bridge
    network:default-config:wan
    network:vlan:bridge
    identity:mac:ethernet

target/linux/mediatek/*/base-files/etc/board.d/01_leds
    openwrt:board-d:leds
    ui:led:power
    ui:led:network-port
    ui:led:wifi

target/linux/mediatek/*/base-files/lib/upgrade/platform.sh
    storage:sysupgrade:platform
    storage:sysupgrade:compatibility
    storage:sysupgrade:backup-restore

package/kernel/mt76/*
    wireless:mt76:*
    wireless:wed:runtime
    firmware:wifi:*

package/kernel/mac80211/*
    wireless:mac80211:patch
    wireless:regulatory:db

package/network/services/hostapd/*
    wireless:hostapd:*
    wireless:mlo:config

package/network/config/wifi-scripts/*
    wireless:wifi-scripts:*
    wireless:mlo:runtime
    openwrt:hotplug:wifi

uqmi/umbim/modemmanager-related paths
    cellular:userspace:*
    cellular:network:wan-interface

package/kernel/linux/modules/*
    openwrt:package:kernel-modules
    plus implied hardware feature

package/firmware/*
    firmware:*
    plus matching hardware feature

scripts/mkits.sh
include/image-commands.mk
    image:fit
    image:sysupgrade-image
    build:scripts:helper
```

## 21. Lookup Policy

Do not inspect every reference repo for every modification.

Use lookup only when needed.

```text
MTK lookup:
    mtk-openwrt-feeds
    mtk24-vs-openwrt24-base
    8x-vs-mtk24-base
    mtk25-vs-openwrt25-base

R4 Pro common lookup:
    4e-vs-mtk24-base
    BPI-R4PRO-4E vendor tree

Old R4 / MT7988 lookup:
    r4-vs-mtk21-base
    BPI-R4 vendor tree
    OpenWrt 25.12 R4 support

Linux lookup:
    linux-v6.6.104
    linux-v6.12.62
    linux-v6.12.87
    linux-v6.18
    linux master

U-Boot lookup:
    upstreams/u-boot

mt76 lookup:
    upstreams/mt76

Feed package lookup:
    mtk21-packages-patches-feeds
    mtk24-packages-patches-feeds
    mtk25-packages-patches-feeds
```

## 21.1 Patch-Collection Diffsets

The following diffsets are patch-collection artifacts, not tree diffsets:

```text
mtk21-packages-patches-feeds
mtk24-packages-patches-feeds
mtk25-packages-patches-feeds
```

They may contain:

```text
manifest.yaml
patch-list.tsv
target-paths.tsv
package-paths.tsv
stat.txt
files/
```

Do not expect normal tree-diff files such as `name-status.tsv`, `numstat.tsv`, or `full.patch` unless they were explicitly generated.

Use these diffsets only to determine which external packages are affected by MTK `patches-feeds`.

When analyzing a patch-collection entry, treat the copied `*.patch` file as an existing patch file and apply the Patch File Analysis rules: inspect inner patch targets, classify package paths, and avoid treating the collection itself as an applied tree.

## 22. When Not to Deep-Read

Do not deep-read:

```text
bulk deleted mac80211 patches
bulk deleted hostapd patches
bulk deleted repo metadata
unrelated target deletions
non-8X wireless chipset patches
generated/build/cache files
```

Unless a cluster specifically depends on them.

## 23. Common Mistakes

Do not analyze all diffsets equally.

Do not tag a large file as one modification if it contains unrelated changes.

Do not use `mtk-inherited` only because the same file exists in MTK.

Do not use `r4-pro-common` only because 8X and 4E edit the same file.

Do not use `filogic-common` when similarity is only BPI vendor style.

Do not treat deletion as intentional removal without evidence.

Do not deeply analyze every mac80211/hostapd deleted patch unless a wireless cluster needs it.

Do not infer upstream provenance from patch filename alone.

Do not assign migration_feature for `*.patch` based only on the patch file path; inspect inner patch semantics.

Do not convert tags into migration decisions. Decisions belong to cluster analysis.

Do not use minimal change as the guiding principle. A smaller local diff is not better if it preserves the wrong abstraction or hides vendor hacks.

## 24. Final Checklist

Before returning analysis for a file, verify:

```text
1. Did I identify file status correctly?
2. If deleted, did I assign deletion_reason?
3. If modified/added, did I split unrelated semantic changes?
4. If DTS, did I consider full-file and include context?
5. If status is R/C, did I distinguish path movement from semantic change?
6. If full-file context is required, did I read both old and new full files?
7. If *.patch, did I distinguish outer diff from inner patch semantics?
8. If *.patch is modified, did I check old and new full patch files?
9. If *.patch is deleted or added, did I inspect inner patch targets when high-risk?
10. If using MTK packages-patches-feeds, did I treat it as a patch collection, not a tree diffset?
11. Did I use tag_rules.md for origin/scope/migration_feature?
12. Did I cite evidence from available diffsets or source trees?
13. Did I avoid turning tags into final migration decisions?
14. Did I record unresolved lookup needs?
15. Did I avoid minimal-change reasoning?
```

## 25. Self-Check

Check 1:
All deletion, modification, DTS, patch-file, reconstruction, rename/copy, full-file context, and patch-collection rules are included.

Check 2:
Full tag definitions are not duplicated; this skill references tag_rules.md.

Check 3:
The skill includes source trees, diffsets, output format, decision trees, evidence layers, lookup policy, and common mistakes.

Check 4:
Patch files are handled in both layers: outer diff and inner patch semantics.

Check 5:
MTK packages-patches-feeds diffsets are explicitly treated as patch collections, not tree diffsets.
