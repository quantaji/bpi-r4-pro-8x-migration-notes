# Phase 02 Batch Review: SD Boot No Install

Diffset: `8x-vs-openwrt24-base`

Phase index: `analysis/phase-routing/8x-vs-openwrt24-base/by-phase/02-sd-boot-no-install.json`

Review purpose: decide which Phase 02 files are real SD boot inputs, which are only evidence, and which must be deferred to onboard storage or later phases.

This review does not migrate code.

## Phase Boundary

Phase 02 handles SD boot only.

Allowed:

1. SD boot overlay semantics,
2. SD U-Boot boot environment semantics,
3. boot-to-userspace rootdisk selection,
4. safety review of recovery/failsafe behavior needed for SD boot.

Not allowed:

1. NAND install,
2. eMMC install,
3. sysupgrade policy,
4. persistent dual-boot design,
5. Wi-Fi, wired, acceleration, or board-extras runtime bring-up.

## Direct 8X Evidence

Direct 8X SD overlay:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso`

Key evidence:

1. targets `/soc/mmc@11230000`,
2. uses 4-bit SD mode,
3. uses `cd-gpios = <&pio 12 GPIO_ACTIVE_LOW>`,
4. sets `no-mmc`,
5. defines `block-partition-env` with `partname = "ubootenv"`,
6. defines `sd_rootfs` with `partname = "production"`,
7. sets `/chosen/rootdisk-sd = <&sd_rootfs>`.

Direct 8X eMMC overlay:

`target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-emmc.dtso`

Key evidence:

1. targets the same `/soc/mmc@11230000`,
2. uses 8-bit eMMC mode,
3. sets `non-removable`,
4. sets `no-sd`,
5. defines `/chosen/rootdisk-emmc`.

Conclusion: SD and eMMC share the controller path. Phase 02 must not mix eMMC install or eMMC runtime validation into SD boot.

Direct 8X image recipe evidence:

`target/linux/mediatek/image/filogic.mk`

Key evidence:

1. 8X profile includes `mt7988a-bananapi-bpi-r4-pro-8x-sd`,
2. `sdcard.img.gz` contains SD bootloader and SD rootfs image path,
3. the same SD image also carries NAND/eMMC install payload areas,
4. install payloads must be documented but not exercised in Phase 02.

Direct 8X U-Boot evidence:

`package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch`

Key evidence:

1. adds `mt7988a-bananapi_bpi-r4-pro-8x-sd.dts`,
2. adds `mt7988a_bananapi_bpi-r4-pro-8x-sdmmc_defconfig`,
3. adds `bananapi_bpi-r4-pro-8x_sdmmc_env`,
4. SD environment boots production with `bootconf_sd`,
5. SD environment boots recovery/TFTP recovery with `bootconf_emmc`,
6. SD boot menu includes install-to-NAND behavior.

Conclusion: SD boot env is in scope, but install-to-NAND and eMMC install behavior are Phase 10. The `bootconf_emmc` use in SD recovery is a TODO for Phase 02 review before implementation.

## Batch Disposition Matrix

| file_id | status | path | features | disposition | owner_phase | evidence | notes | minimalism_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `000031` | M | `package/boot/uboot-envtools/files/mediatek_filogic` | `boot:uboot:env`, `identity:uboot-env:ethaddr` | `needs-evidence` | Phase 02 | Vendor patch adds generic RFB env handling and existing BPI-R4 handling, but not an explicit `bananapi,bpi-r4-pro-8x` case. | Verify target 25.12 uboot-envtools handling for 8X SD `ubootenv` partition. Do not copy broad RFB logic blindly. | TODO required. |
| `000033` | A | `package/boot/uboot-mediatek/patches/999-add-bananapi_bpi-r4-pro-8x.patch` | `boot:uboot:bootmenu`, `boot:uboot:env`, `boot:uboot:recovery`, `boot:uboot:storage-layout` | `rewrite` | Phase 02 and Phase 10 split | Direct 8X U-Boot patch contains SD DTS, SD defconfig, SD env, and install payload behavior. | Preserve SD boot semantics. Defer install-to-NAND/eMMC parts to Phase 10. Audit `boot_recovery` using `bootconf_emmc` in SD env. | Boundary split required. |
| `000490` | A | `package/mtk/reset-boot-count/Makefile` | `boot:recovery:failsafe` | `needs-evidence` | Phase 02 | Package is recovery/failsafe support, but no direct SD boot dependency was proven. | Verify whether U-Boot pstore/bootcount flow requires this for SD boot safety. | TODO required. |
| `000491` | A | `package/mtk/reset-boot-count/files/reset-boot-count.init` | `boot:recovery:failsafe` | `needs-evidence` | Phase 02 | Same package as `000490`. | Verify runtime trigger and whether it belongs in early SD image. | TODO required. |
| `000492` | A | `package/mtk/reset-boot-count/src/Makefile` | `boot:recovery:failsafe` | `needs-evidence` | Phase 02 | Same package as `000490`. | Treat as package-internal until package necessity is proven. | TODO required. |
| `000493` | A | `package/mtk/reset-boot-count/src/reset-boot-count.c` | `boot:recovery:failsafe` | `needs-evidence` | Phase 02 | Same package as `000490`. | Inspect only if reset-boot-count package is retained. | TODO required. |
| `000811` | M | `package/system/fstools/Makefile` | `boot:recovery:factory-install`, `storage:partition:rootfs` | `defer` | Phase 10 | Adds `libfstools-bootparam` and dual-boot dependency plumbing. | Not required for SD no-install unless later evidence proves SD root selection needs it. | Deferred with owner phase. |
| `000812` | A | `package/system/fstools/patches/0001-add-support-for-dual-boot.patch` | `boot:recovery:factory-install`, `storage:partition:rootfs` | `defer` | Phase 10 | Adds boot-param library, hides dual-boot block devices, and redirects rootfs_data lookup. | Persistent dual-boot/sysupgrade behavior. Not SD-only. | Deferred with owner phase. |
| `000827` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7981-rfb-spim-nor.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7981 RFB, not 8X. | Phase 02 false positive from storage keyword. | Context checked. |
| `000829` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-emmc.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 eMMC overlay, not 8X. | Not a vendor-family authority for 8X SD boot. | Context checked. |
| `000832` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-netsys-eth0-an8855.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 network overlay, not 8X SD storage. | Routing noise. | Context checked. |
| `000842` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-pinctrl.dtsi` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 pinctrl, not 8X. | Not a Phase 02 input. | Context checked. |
| `000843` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-sd.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 SD overlay, not 8X. | Can be MTK background later, but not current evidence. | Context checked. |
| `000845` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-spim-nand.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 NAND overlay, not 8X. | Not SD no-install. | Context checked. |
| `000846` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-spim-nor.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 NOR overlay, not 8X. | Not SD no-install. | Context checked. |
| `000847` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987.dtsi` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 SoC file, not 8X. | Not current hardware. | Context checked. |
| `000851` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987a-bananapi-bpi-r4-lite.dts` | `dts:overlay:storage` | `drop` | Phase 02 | BPI-R4 Lite vendor-family file, not 8X and not SD boot authority. | Can be background only if later needed. | Context checked. |
| `000852` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987a-rfb.dts` | `dts:overlay:storage` | `drop` | Phase 02 | MT7987 RFB, not 8X. | Not current hardware. | Context checked. |
| `000855` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-emmc.dtso` | `dts:overlay:storage` | `defer` | Phase 10 | Direct 8X eMMC overlay confirms shared controller and `rootdisk-emmc`. | Use as Phase 02 evidence only; eMMC runtime/install is Phase 10. | Deferred with owner phase. |
| `000857` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-sd.dtso` | `dts:overlay:storage` | `migrate` | Phase 02 | Direct 8X SD overlay defines SD bus, env partition, production rootfs, and `rootdisk-sd`. | Primary SD boot input. Port semantics into target 25.12. | Context checked. |
| `000858` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x-wifi-mt7996a.dtso` | `dts:overlay:storage` | `defer` | Phase 06 | Direct 8X Wi-Fi overlay; storage tag is keyword bleed from EEPROM. | Not SD boot. | Deferred with owner phase. |
| `000859` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts` | `dts:overlay:storage` | `review-only` | Phase 02 | Direct 8X base DTS provides board compatible and base NAND `rootdisk-spim-nand`. | Needed as context for SD overlay; full board/NAND handling belongs Phase 03/10. | Context checked. |
| `000860` | M | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb-emmc.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB eMMC overlay, not 8X. | Not board authority. | Context checked. |
| `000861` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb-eth0-gsw.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB network overlay, not SD storage. | Routing noise. | Context checked. |
| `000869` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb-mxl86252.dts` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB MxL switch board, not 8X SD boot. | Wired switch context belongs Phase 05 if needed, not Phase 02. | Context checked. |
| `000870` | M | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb-sd.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB SD overlay, not 8X. | Can be MTK background, not migration input. | Context checked. |
| `000872` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb-spim-nand-nmbm.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB NAND overlay, not 8X. | Not SD no-install. | Context checked. |
| `000873` | M | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb-spim-nor.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB NOR overlay, not 8X. | Not SD no-install. | Context checked. |
| `000874` | M | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-rfb.dts` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988 RFB board DTS, not 8X. | Not board authority. | Context checked. |
| `000875` | M | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a.dtsi` | `dts:overlay:storage` | `review-only` | Phase 02 | MT7988 SoC DTSI can affect MMC controller availability. | Check target 25.12 SoC support if SD overlay fails to compile or boot. Do not migrate broad SoC changes by default. | Context checked. |
| `000876` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988d-rfb-eth0-gsw.dtso` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988D RFB network overlay, not 8X. | Routing noise. | Context checked. |
| `000878` | A | `target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988d-rfb.dts` | `dts:overlay:storage` | `drop` | Phase 02 | MT7988D RFB board DTS, not 8X. | Not board authority. | Context checked. |
| `001131` | A | `target/linux/mediatek/patches-6.6/999-dual-boot-01-do-not-auto-mount-ubi-rootfs.patch` | `storage:partition:rootfs` | `defer` | Phase 10 | Patch depends on `mediatek,dual-boot`; direct 8X DTS did not show this property. | Persistent UBI dual-boot behavior, not SD no-install. | Deferred with owner phase. |
| `001132` | A | `target/linux/mediatek/patches-6.6/999-dual-boot-02-ubi-allow-no-default-rootdev.patch` | `storage:partition:rootfs` | `defer` | Phase 10 | Adds `ubiblock.no_default_rootdev` control. | Storage/rootfs policy, not SD boot minimum. | Deferred with owner phase. |
| `001133` | A | `target/linux/mediatek/patches-6.6/999-dual-boot-03-fitblk-do-not-split-rootfs_data-if-required.patch` | `storage:partition:rootfs` | `defer` | Phase 10 | Patch depends on `mediatek,no-split-fitrw`; direct 8X DTS did not show this property. | Persistent rootfs_data/fitrw behavior, not SD no-install. | Deferred with owner phase. |

## Disposition Counts

| disposition | count |
| --- | ---: |
| `migrate` | 1 |
| `rewrite` | 1 |
| `drop` | 19 |
| `defer` | 7 |
| `review-only` | 2 |
| `needs-evidence` | 5 |

## TODOs

1. Phase 02: verify whether target OpenWrt 25.12 `uboot-envtools` needs an explicit `bananapi,bpi-r4-pro-8x` case for SD `ubootenv`.
2. Phase 02: audit 8X SD U-Boot `boot_recovery` and `boot_tftp_recovery`, because vendor SD env uses `bootconf_emmc` for recovery while production uses `bootconf_sd`.
3. Phase 02: verify whether `reset-boot-count` is required for SD boot safety or can be deferred.
4. Phase 10: own fstools dual-boot and kernel rootfs policy patches.
5. Phase 10: own eMMC overlay and NAND/eMMC install behavior.
6. Phase 06: own Wi-Fi overlay despite its accidental Phase 02 routing.

## Unreported Minimalism Gate

Result: passed for this review.

Minimalism risks found:

1. copying the full 8X U-Boot patch would silently bring NAND/eMMC install behavior into Phase 02,
2. accepting all `dts:overlay:storage` matches would pull many MT7987/RFB files into SD boot,
3. treating fstools dual-boot as SD boot minimum would over-scope Phase 02.

Mitigation:

1. direct 8X SD overlay is the only `migrate` DTS overlay in this phase,
2. eMMC/install/dual-boot changes are deferred,
3. RFB/MT7987 false positives are dropped or review-only,
4. unresolved SD env and reset-boot-count questions are marked `needs-evidence`.
