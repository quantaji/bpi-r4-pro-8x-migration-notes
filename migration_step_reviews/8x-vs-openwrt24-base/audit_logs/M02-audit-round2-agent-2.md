# M02 Audit Round 2 Agent 2 Raw Report

Reviewer id: `M02-audit-round2-agent-2`

Agent id: `019ea9d8-d5c8-7d91-8457-b98410255652`

Nickname: `Mill`

Verdict: `accept-with-minor-edits`

## Raw Feedback

**Verdict: `accept-with-minor-edits`**

未修改文件，未提交代码。整体可作为 Phase 2 M02 batch review matrix 接受；只有一个低严重度措辞问题，建议修掉以免后续实现误读边界。

**Structural Checks**

- TSV coverage: PASS. by-step JSON 为 35 files / 41 feature assignments；TSV 为 35 data rows，无 missing / extra / duplicate `file_id`。
- TSV field match: PASS. `status/path/file_kind/features/route_classes` 与 by-step JSON 逐项一致。
- Counts: status `A=28`, `M=7`; feature route assignments `primary=32`, `supporting=6`, `deferred=3`。
- Disposition: PASS. `defer=12`, `drop=18`, `review-only=3`, `migrate=1`, `rewrite=1`，全部合法。
- Owner: PASS. `M02=23`, `M03=1`, `M06=1`, `M10=10`；非 defer 行归 `M02`，defer 行归后续 step。
- `step-file-index.tsv`: PASS. 35 个 M02 row 与 JSON 匹配；`001134` 只在 M00 出现。
- Audit log organization: PASS. 三个 raw reports 已分离到 `audit_logs/`；主文档未嵌入完整 raw reports，只保留 concise summary；主文档明确写 formal three-agent audit completed on `2026-06-08`。raw logs 中 “draft/audit not completed” 类评论已有 pre-recording historical note。

**Findings**

- Low, [M02-sd-boot-no-install.md](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.md:299), affected `000033`: TODO 3 仍写 “M02: explicitly audit `boot_recovery` and `boot_tftp_recovery`”，但 `boot_tftp_recovery` 是已被要求排除的 SD write/update flow。同文件下一行又正确把 `boot_tftp_recovery` 交给 M10/later，因此这是边界措辞歧义，不是结构性失败。
  Why it matters: 后续实现者可能把 TFTP recovery/update flow 当作 M02 no-install boot 的迁移对象。
  Recommended fix: 将 TODO 3 改成只审 `boot_recovery`，或明确 `boot_tftp_recovery` 仅作 read-only bootconf evidence，不执行、不迁移，流程 owner 仍为 M10/later explicit install review。

**No-Issue Confirmations**

- `M02-audit-agent-2` 的 low finding 已实质应用：TSV `000033` 行明确排除 `bootmenu_4/5`, `boot_tftp_production`, `boot_tftp_recovery`, `sdmmc_write_production`, `sdmmc_write_recovery`, `replacevol`，并交给 M10/later review：[files.tsv](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo/migration_step_reviews/8x-vs-openwrt24-base/M02-sd-boot-no-install.files.tsv:3)。
- 直接 8X vendor patch 证实这些确为写入/更新路径：`bootmenu_4/5` 设置 `replacevol`，`boot_tftp_*` 可调用 `sdmmc_write_*`：[vendor patch](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch:772)。
- `000857` 是唯一 M02 migrate DTSO；直接 8X SD overlay 包含 `mmc@11230000`, `cd-gpios`, `no-mmc`, `rootdisk-sd`：[SD DTSO](/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso:13)。
- `000855` eMMC overlay correctly stays context/defer to M10; `000858` Wi-Fi overlay correctly defers to M06。
- `000490`-`000493` defer to M10 remains justified: reset service is DT-property-gated, and direct 8X DTS evidence does not provide `mediatek,reset-boot-count`。
- `000811`/`000812` and `001131`-`001133` defer to M10 remains reasonable: bootparam, dual-boot, UBI/rootfs, and rootfs_data policy are persistent storage/sysupgrade behavior, not M02 no-install SD boot。
- `001134` correctly remains outside the 35-row M02 TSV and is handled as M00 handoff evidence before SD/recovery FIT validation, with persistent rootfs/sysupgrade implications handed to M10。
- No filename-only drop/defer issue found; non-8X RFB/MT7987/Lite rows are documented as routing noise/supporting context, not 8X truth。

**Residual Risk**

Runtime SD boot still needs later M02 validation: serial log, selected SD overlay, `/chosen/rootdisk-sd`, FIT/rootfs mapping, and recovery behavior. M03 still owns env/identity review, M06 owns Wi-Fi overlay bring-up, and M10 owns NAND/eMMC install, sysupgrade, bootcount, dual-boot/rootfs_data policy, and all SD/TFTP write/update flows.
