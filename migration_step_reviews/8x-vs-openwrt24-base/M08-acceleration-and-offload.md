# M08 Acceleration And Offload Batch Review

Project Phase 2 / Migration Step M08: Acceleration And Offload.

## Audit Status

This file is the M08 round2-audited batch review. Formal three-agent no-context audit round1 completed with verdicts `revise-before-accept`, `accept-with-minor-edits`, and `revise-before-accept`; the actionable round1 findings have been remediated in this review matrix. Formal three-agent no-context audit round2 also completed with verdicts `accept-with-minor-edits`, `accept-with-minor-edits`, and `accept-with-minor-edits`; the only shared round2 minor finding was stale audit-status text, now corrected here.

No migration code was written, no image was compiled, no runtime throughput/offload result is claimed, and no storage/install/sysupgrade behavior is accepted here.

## Scope / Non-goals

Allowed M08 scope:

- WED / WO / HWRRO / RRO Wi-Fi offload evidence.
- MediaTek PPE, HNAT, RSS, LRO, flowtable, nft/xt offload evidence.
- TOPS tunnel offload evidence.
- Package/firmware closure only where it gates acceleration/offload review.

Not allowed in M08:

- Declaring basic wired, SFP/10G, Wi-Fi association, MLO/AFC, NAND/eMMC install, sysupgrade, storage, or image boot success.
- Treating vendor throughput-only results as sufficient acceptance.
- Treating `.config` or package lists as hardware truth.
- Promoting MT7987, mt7990, mt7992, RFB, or generic vendor-family hunks to direct 8X requirements without direct 8X evidence.

## Structural Summary

- Input JSON file count: 87 files.
- Input JSON assignment count: 165 assignments.
- Input status counts: `A=85`, `M=2`.
- JSON assignment-level route class counts: `primary=162`, `review-only=3`.
- TSV collapsed file-level route class counts: `primary=84`, `review-only=3`.
- TSV rows: 87, one row per M08 by-step input file.

Feature assignment counts:

- `accel:flowtable:nft`: 2
- `accel:wed:wifi-offload`: 49
- `firmware:wed:wo`: 35
- `wireless:wed:runtime`: 35
- `accel:ppe:flow-offload`: 28
- `accel:hnat:nat`: 6
- `accel:hnat:routing`: 6
- `accel:crypto:eip`: 3
- `accel:tops:tunnel-offload`: 1

Disposition counts:

- `defer`: 10
- `drop`: 4
- `needs-evidence`: 60
- `review-only`: 9
- `superseded-by-target`: 4

Owner counts:

- `M07`: 10
- `M08`: 77

## Direct 8X Evidence

- Direct 8X vendor image recipe selects `kmod-mt7996-firmware`, `kmod-mt7996-233-firmware`, and `mt7988-wo-firmware` for the 8X image skeleton. This supports mt7996/mt7996-233 and WO firmware closure, not mt7990 or MT7987 firmware migration. MT7992-named WED patches still require patch-body and target comparison when they alter MT7988 WED behavior.
- Direct 8X vendor `.config` enables `kmod-nft-offload`, `kmod-nf-flow`, `kmod-nf-flow-netlink`, and `netfilter-flowtable`, but leaves `kmod-mediatek_hnat` unset. This is package/config evidence only, not hardware truth or runtime proof.
- Direct 8X vendor MT7988 SoC DTS contains WED0/1/2, WO EMI/data reserved memory, WO CCIF/ILM/DLM/cpuboot syscons, and Ethernet `mediatek,wed = <&wed0>, <&wed1>, <&wed2>`. Target 25.12 also has MT7988 WED DTS enable/refactor patches, but runtime WED/PPE behavior still needs M08 validation.
- Target OpenWrt 25.12 already packages `mt7988-wo-firmware` and common mt799x runtime firmware, and carries the upstream WED DMA32 backport corresponding to `001107`. It does not prove vendor WED module parameter, HNAT tree, or vendor netfilter extension equivalence.

## Topic/Substep Summary

### M08-A Netfilter / nft Flowtable Boundary

`000052` and `000471` remain `needs-evidence`: the vendor adds an nf-flow-netlink package and a libnfnetlink flowtable subsystem constant, while target 25.12 has nf-flow/nft-offload but no direct nf-flow-netlink package or libnfnetlink patch. M08 must compare kernel 6.12 UAPI and target userspace before adding anything.

### M08-B mt76 Package, WED Module Param, WO/Firmware Closure

`000343` is `needs-evidence` because the vendor Makefile mixes source update, `wed_enable=1`, debugfs/testmode flags, mt7990 packaging, and testmode firmware. Direct 8X requires mt7996/mt7996-233 plus WO firmware; target already contains the ordinary runtime firmware but not the vendor WED enable policy. Non-8X mt7990/mt7992 firmware rows are the only remaining M08 drops, ordinary 8X mt7996 runtime firmware rows are target-superseded, and testmode firmware rows are review-only.

### M08-C mt76 WED / RRO / HWRRO Patch Stack

WED/RRO/HWRRO candidate rows such as `000346`, `000347`, `000348`, `000350`, `000366`, `000368`, `000384`, and `000385` are `needs-evidence`. They touch WED attach failure, RRO NAPI timing, L1 SER handling, token allocation, WED RX buffer release, offload enable/disable token sizing, HWRRO separation, RX status WCID handling, and kernel 6.6 cleanup paths. Self-QC also moved `000374`, `000400`, `000421`, and `000426` out of `drop` because their patch bodies modify shared mt76/mt7996 WED/RRO/HWRRO or public driver policy code despite mt7990/mt7987 titles. Pure MLO/EMLSR/preamble puncture/rate/scan/policy rows remain M07 handoffs; `000375` moved back to M08 because it changes WED TXS and WDMA forward-path binding semantics.

### M08-D MediaTek HNAT Source And Legacy Hooks

The HNAT source/header set (`000897`-`000904`, `000957`) and HNAT kernel patches (`001056`-`001062`) are `needs-evidence`. They define large HNAT hook, FOE, debugfs, multicast, DSA/STAG, tunnel, and PPE-flow-check behavior, but direct 8X config leaves `kmod-mediatek_hnat` unset and target 25.12 lacks the vendor HNAT tree.

### M08-E PPE / RSS / LRO / Netfilter Flow Offload

RSS/LRO/PPE and xt/nft flow-offload rows (`001027`-`001037`, `001087`-`001105`) remain `needs-evidence`. These are real acceleration candidates, especially bridge, DSCP, WDMA, cache, and memory-leak changes, but they require target 6.12 API comparison and M04/M05 wired-path validation before migration.

### M08-F Kernel WED Patch Stack

`001107` is `superseded-by-target` because target 25.12 carries the upstream WED DMA32/dma-mask backport. `001113` is also `superseded-by-target` because target 25.12 carries generic backport `731-v6.18` with the same MT7992-on-MT7988 second WDMA RX ring / WED v3-or-greater behavior. Other WED rows (`001108`-`001122`) remain `needs-evidence` or review-only depending on scope: SER double-free, WED assignment, WDMA RX hang, ring leak, WMM/PPE drop, RRO init, IRQ false-alarm, and `001116` WED reset/attach runtime hunks are M08 candidates. `001118` is mixed MT7987-only plus generic/MT7988-adjacent WED/HWRRO refactor content and must be split-compared instead of dropped by title.

### M08-G TOPS Tunnel Offload

`001123` is `needs-evidence`: TOPS only adds tunnel type metadata (`flow_offload_tnl` and `tnl_type`) to flow offload hardware path structures, and M08 has no direct 8X tunnel policy or target equivalence yet.

### M08-H Crypto / EIP Rows

`001017` and `001019` remain review-only crypto/EIP provenance. `001063` is `needs-evidence` after round1 audit because the crypto-eth-inline patch adds HNAT-disabled tunnel metadata and skb tunnel helpers in `mtk_eth_soc.h`; direct 8X leaves `kmod-mediatek_hnat` unset, so this path must be compared rather than treated as pure crypto background.

## Self-QC Remediation Pass

Self-QC re-read the M08 TSV against all 87 input rows, with actual diff bodies checked for textual patch/source rows and package linkage checked for firmware rows. The pass specifically rejected title-only non-8X drops when the body modifies generic WED/PPE/HNAT/netfilter code, MT7988-adjacent data, or public mt76/WED APIs.

Rows changed by this pass:

- `000374`: `drop` -> `needs-evidence`; mt7990 title, but the body changes shared mt7996 driver code and includes WED/RRO configuration, txfree, prefetch, DMA, MCU, and debugfs changes.
- `000375`: `defer -> M07` -> `needs-evidence -> M08`; ordinary ADDBA policy remains M07-adjacent, but this patch also changes WED TXS BA status handling and WDMA forward-path TID mapping.
- `000400`: `drop` -> `needs-evidence`; mt7990/mt7987 title, but body changes generic mt76 DMA/RRO, `hwrro_mode`, RXDMAD_C, WED RX data queues, and mt7996 WED setup.
- `000421`: `drop` -> `needs-evidence`; body adds generic HWRRO3.1 RXDMAD_C/EMI queue handling and public mt76 driver ops despite mt7992/mt7990-only subject text.
- `000426`: `drop` -> `needs-evidence`; mt7990 low-power path is not an M08 runtime requirement, but the body changes shared mt76/mt7996 MCU/init/debugfs/regs code and must be target-compared before being ignored.
- `001113`: `drop` -> `superseded-by-target`; target 25.12 backport `731-v6.18-net-mediatek-wed-Introduce-MT7992-WED-support-to-MT7.patch` carries the same MT7992-on-MT7988 WED second WDMA RX ring / v3-or-greater behavior.
- `001118`: `drop` -> `needs-evidence`; body mixes MT7987-only data with generic and MT7988-adjacent WED/HWRRO v3/v3.1 refactor content.

Rows changed by round1 audit remediation:

- `000350`: `review-only` -> `needs-evidence`; the debug-tools patch also changes WED token allocation, WED RX buffer release, offload enable/disable token sizing, and mt7996 DMA setup.
- `001063`: `review-only` -> `needs-evidence`; crypto-eth-inline adds HNAT-disabled tunnel metadata and skb tunnel helpers relevant to the direct 8X HNAT-disabled config state.
- `001116`: `review-only` -> `needs-evidence`; extended WED debugfs also changes WED reset/attach runtime behavior outside debugfs.

Final `drop` rows are limited to binary firmware that direct 8X image/package evidence does not select: `000441`, `000442`, `000455`, and `000456`.

## High-risk Rows

- `000052`: `needs-evidence` -> `M08`; M08-A-netfilter-nft-flowtable-boundary; Dense-read: vendor netfilter.mk adds KernelPackage/nf-flow-netlink for CONFIG_NF_FLOW_TABLE_NETLINK and nf_flow_table_netlink.ko; target 25.12 has nf-flow and nft-offload packages but no nf-flow-netlink package; direct 8X .config enables kmod-nf-flow-netlink but config is not hardware truth.
- `000343`: `needs-evidence` -> `M08`; M08-B-mt76-package-WED-WO-firmware-boundary; Dense-read: vendor mt76 Makefile updates source to 2025-06-01, adds MODPARAMS.mt7996e:=wed_enable=1, debugfs build flags, ADDITIONAL_CFLAGS date macros, mt7990 firmware package, and *_wm_tm firmware installs; target 25.12 has mt799x firmware packaging and mt7988-wo-firmware in filogic images but not the vendor wed_enable module param or testmode firmware installs.
- `000350`: `needs-evidence` -> `M08`; M08-C-mt76-WED-debug-tools-datapath-needs-evidence; Dense-read: despite the debug-tools title, the giant mt76 patch changes real shared WED/RRO/offload datapath behavior, including WED token allocation ranges in `mt76_token_consume`, WED RX buffer/page-fragment release, offload enable/disable token sizing, and mt7996 DMA queue setup.
- `000374`: `needs-evidence` -> `M08`; M08-C-mt76-shared-mt7990-WED-RRO-support-needs-evidence; Dense-read: large mt7990 support patch modifies shared mt7996 driver files, including coredump/debugfs/dma/eeprom/init/mac/main/mcu/mmio/pci/regs paths, and includes mt7990 tx/rx/fwdl/txfree/prefetch plus WED/RRO configuration; although mt7990 is not direct 8X hardware, this is not safe to drop from title alone because it changes shared mt76/mt7996 code.
- `000375`: `needs-evidence` -> `M08`; M08-C-mt76-WED-BA-hwpath-binding-needs-evidence; Dense-read: ADDBA patch explicitly says hw-path binding depends on BA state, refactors mt7996_check_tx_ba_status, refreshes BA from WED TXS when WED is active, and changes mt7996_net_fill_forward_path WDMA AMSDU TID mapping through qos_map[dscp].
- `000400`: `needs-evidence` -> `M08`; M08-C-mt76-generic-WED-HWRRO31-needs-evidence; Dense-read: despite mt7990/mt7987 title, patch changes generic mt76 DMA/RRO handling, adds MT_WED_RRO_Q_RXDMAD_C, hwrro_mode enum, mt76_wed_check_rx_cap, MT_RXQ_WED_RX_DATA, WED v3.1/RRO3.1 RXDMAD_C host path, and mt7996 mmio/init/dma WED setup.
- `000368`: `needs-evidence` -> `M08`; M08-C-mt76-WED-RRO-HWRRO-runtime; Dense-read: patch separates HWRRO from WED, adds WED_RRO queue helpers, RX token/page-pool handling, RRO indication processing, and init crash fixes for kernel 6.6 page-pool behavior.
- `000385`: `needs-evidence` -> `M08`; M08-C-mt76-WED-RRO-HWRRO-runtime; Dense-read: patch gates RRO page/token free paths with LINUX_VERSION_IS_LESS(6,6,0), moves WDMA TID assignment, and adds TODO comments for kernel 6.6 WED cleanup behavior.
- `000421`: `needs-evidence` -> `M08`; M08-C-mt76-generic-HWRRO31-sw-path-needs-evidence; Dense-read: patch says sw path HWRRO3.1 is for mt7992/mt7990 but modifies generic mt76 DMA queue reset/kick/dequeue/RX process, adds MT_QFLAG_EMI_EN, mt76_rro_rxdmad_c descriptor, rx_init_rxdmad_c/rx_rro_rxdmadc_process driver ops, and mt7996 RRO RXDMAD_C/EMI handling.
- `000426`: `needs-evidence` -> `M08`; M08-C-mt76-shared-mt7990-low-power-policy-needs-evidence; Dense-read: low-power patch is mt7990-oriented and gated by is_mt7990, but it still modifies shared mt76_connac_mcu and mt7996 init/mcu/header/debugfs/regs code, adds lp_ctrl module parameter, PCIe L1SS, TPO, ultra-save, PST commands, and debugfs knobs.
- `000441`: `drop` -> `M08`; M08-B-non-8X-mt7990-mt7992-firmware-drop; Direct 8X image recipe uses kmod-mt7996-firmware, kmod-mt7996-233-firmware, and mt7988-wo-firmware; mt7990_wm.bin is mt7990/mt7992 firmware and is not direct 8X package closure.
- `000442`: `drop` -> `M08`; M08-B-non-8X-mt7990-mt7992-firmware-drop; Direct 8X image recipe uses kmod-mt7996-firmware, kmod-mt7996-233-firmware, and mt7988-wo-firmware; mt7990_wm_tm.bin is mt7990/mt7992 firmware and is not direct 8X package closure.
- `000455`: `drop` -> `M08`; M08-B-non-8X-mt7990-mt7992-firmware-drop; Direct 8X image recipe uses kmod-mt7996-firmware, kmod-mt7996-233-firmware, and mt7988-wo-firmware; mt7992_wm_23.bin is mt7990/mt7992 firmware and is not direct 8X package closure.
- `000456`: `drop` -> `M08`; M08-B-non-8X-mt7990-mt7992-firmware-drop; Direct 8X image recipe uses kmod-mt7996-firmware, kmod-mt7996-233-firmware, and mt7988-wo-firmware; mt7992_wm_tm.bin is mt7990/mt7992 firmware and is not direct 8X package closure.
- `000458`: `superseded-by-target` -> `M08`; M08-B-mt7996-firmware-target-closure; Target 25.12 mt76 Makefile installs mt7996_dsp.bin in the mt7996/mt7996-233 firmware package path, and direct 8X image selects those packages.
- `000468`: `superseded-by-target` -> `M08`; M08-B-mt7996-firmware-target-closure; Target 25.12 mt76 Makefile installs mt7996_wm_233.bin in the mt7996/mt7996-233 firmware package path, and direct 8X image selects those packages.
- `000469`: `review-only` -> `M08`; M08-B-mt7996-testmode-firmware-review-only; Vendor adds mt7996_wm_tm.bin as *_wm_tm testmode firmware through mt76 Makefile; target 25.12 common mt7996 firmware packaging does not install this testmode binary, and direct 8X runtime packages do not prove testmode need.
- `000470`: `review-only` -> `M08`; M08-B-mt7996-testmode-firmware-review-only; Vendor adds mt7996_wm_tm_233.bin as *_wm_tm testmode firmware through mt76 Makefile; target 25.12 common mt7996 firmware packaging does not install this testmode binary, and direct 8X runtime packages do not prove testmode need.
- `000897`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: hnat.c defines global HNAT state, exported ra_sw_nat_hook_rx/tx hooks, WDMA port callbacks, roam/workqueue handling, and HNAT initialization paths.
- `000898`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: hnat.h defines PPE register offsets, FOE/table structures, HNAT constants, and helper declarations for the vendor HNAT driver.
- `000899`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: hnat_debugfs.c exposes HNAT debugfs controls and BIND/UNBIND/FIN state inspection for IPv4/IPv6 HNAT reasons.
- `000900`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: hnat_mcast.c manages PPE multicast table entries, VLAN IDs, MAC keys, and multicast register programming.
- `000902`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: hnat_nf_hook.c wires bridge/IPv6/netfilter hooks, VLAN/WAN device lookup, Wi-Fi hook indexes, and skb HNAT metadata handling.
- `000903`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: hnat_stag.c fills DSA service tags into FOE entries and preserves VLAN layers for PPE offload.
- `000904`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: nf_hnat_mtk.h defines skb control-block HNAT metadata, magic tags, tops field, and descriptor formats.
- `000957`: `needs-evidence` -> `M08`; M08-D-MediaTek-HNAT-driver-and-legacy-hooks; Dense-read: ra_nat.h provides legacy HW NAT skb macros, VLAN helpers, magic tag helpers, and FOE CPU reason definitions.
- `001027`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Dense-read: patch adds RSS/LRO register definitions for MTK ethernet SoC, including LRO control and RSS global config offsets.
- `001028`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Dense-read: patch adds RSS support and reshapes HWLRO init/uninit/IP validation paths around PPE index and ring state.
- `001029`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Dense-read: patch adds HW LRO receive stats/update handling and LRO ring initialization in mtk_eth_soc RX path.
- `001037`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Dense-read: patch refactors PSE PPE port link-down flow for NETSYS SER and iterates PPE ports instead of hard-coding PPE0/1/2 link-down bits.
- `001056`: `needs-evidence` -> `M08`; M08-D-HNAT-kernel-patch-stack; Dense-read: patch adds virtual-interface acceleration hooks across netdevice, nf_flow_table, vlan_dev, and ip6_tunnel paths.
- `001057`: `needs-evidence` -> `M08`; M08-D-HNAT-kernel-patch-stack; Dense-read: patch adds tunnel-interface offload checks and netdevice path handling for L2TP/PPP adjacency.
- `001058`: `needs-evidence` -> `M08`; M08-D-HNAT-kernel-patch-stack; Dense-read: patch adjusts IPv6 pskb_expand_head limitation in skbuff core for HNAT tunnel/offload behavior.
- `001060`: `needs-evidence` -> `M08`; M08-D-HNAT-kernel-patch-stack; Dense-read: patch adds NET_MEDIATEK_HNAT Kconfig/object wiring, mt7988a-rfb DTS changes, mtketh PPE count, and skb HNAT magic tag handling.
- `001062`: `needs-evidence` -> `M08`; M08-D-HNAT-kernel-patch-stack; Dense-read: patch adds PPE flow-check interrupt definitions and HNAT/PPE interrupt plumbing.
- `001063`: `needs-evidence` -> `M08`; M08-H-crypto-EIP-HNAT-disabled-tunnel-metadata-needs-evidence; Dense-read: crypto-eth-inline patch adds non-HNAT fallback tunnel metadata in `mtk_eth_soc.h`, including `struct tnl_desc`, `TNL_MAGIC_TAG`, `skb_tnl_cdrt`, `skb_tnl_magic_tag`, and `is_tnl_tag_valid`; direct 8X config leaves `kmod-mediatek_hnat` unset, so this HNAT-disabled tunnel/offload path cannot be dismissed as pure crypto review-only.
- `001087`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Dense-read: patch adds bridging support to xt_FLOWOFFLOAD via br_fdb and xt_FLOWOFFLOAD changes so bridged traffic can bind.
- `001088`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch changes mtk_ppe debugfs to an internal mode; diagnostic behavior only matters if target PPE import needs it.
- `001090`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch changes mtk_ppe internal QoS mode; requires target PPE/nft offload comparison before migration.
- `001091`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch adds DSCP learning to xt_FLOWOFFLOAD; policy and nft/xt behavior must be checked against target flowtable.
- `001092`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch adds DEV_PATH_MTK_WDMA handling to xt_FLOWOFFLOAD for relay/WED path integration.
- `001099`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch deletes ib2 multicast bit from PPE entries; requires PPE entry-format comparison.
- `001100`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch adds PPE cache preserved line lock; requires target PPE cache-line behavior comparison.
- `001101`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Dense-read: patch adds bridging support to nft_flow_offload, includes bridge private data, and adds bridging detection for nft flow binding.
- `001102`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch adds DEV_PATH_MTK_WDMA handling to nft_flow_offload; crosses PPE/WED/nft flowtable path.
- `001103`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch adds DSCP learning to nft_flow_offload; target nft semantics and policy must be compared.
- `001104`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch fixes xt_FLOWOFFLOAD memory leak; only applicable if the vendor xt flowoffload extension is retained.
- `001105`: `needs-evidence` -> `M08`; M08-E-PPE-RSS-LRO-netfilter-flow-offload; Patch fixes nft_flow_offload memory leak; only applicable if the vendor nft extension is retained.
- `001107`: `superseded-by-target` -> `M08`; M08-F-kernel-WED-target-superseded; Dense-read: vendor patch adds GFP_DMA32 allocation and dma_set_mask_and_coherent(DMA_BIT_MASK(32)) for WED buffers on boards with more than 4GB DRAM; target 25.12 generic backport 733-v6.18 carries the same semantic with upstream-reviewed WED code.
- `001108`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch avoids double-free of HWRRO buffer during SER by removing mtk_wed_hwrro_free_buffer from rx_reset.
- `001109`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch refactors mtk_wed_assign away from PCI-domain based selection and iterates WED hardware list.
- `001110`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch fixes WDMA RX hang on wed1 after SER by restoring WDMA RX prefetch/DDONE configuration during reset.
- `001111`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch frees configured RX/TX WDMA rings on Wi-Fi module reinsertion to address memory leaks.
- `001112`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch changes WED WPDMA TX_DDONE check behavior to address Eagle MLO throughput; this is WED datapath with MLO-performance adjacency.
- `001113`: `superseded-by-target` -> `M08`; M08-F-kernel-WED-target-superseded; Dense-read: vendor patch adds MT7988 WED second WDMA RX ring support with wpdma_rx_ring1=0x7d8, wpdma_rx array handling, WED v3 second RX ring writes, and RRO MSDU page count init; target 25.12 generic backport 731-v6.18 introduces the same MT7992-on-MT7988 WED support with wpdma_rx_ring array and v3-or-greater handling.
- `001115`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch adds hwpath WMM support across mtk_ppe, mtk_ppe_offload, mtk_wed, and WED public headers.
- `001116`: `needs-evidence` -> `M08`; M08-F-kernel-WED-debugfs-runtime-needs-evidence; Dense-read: extended WED debugfs patch is diagnostics-heavy, but it also changes runtime WED behavior outside debugfs: `mtk_wed_rx_reset` polls WDMA status instead of WPDMA status, and `mtk_wed_attach` reads the WED revision ID from soc regmap.
- `001117`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch refactors RRO_RX_D_DRV init flow by removing one RX_D config clear before ring setup.
- `001118`: `needs-evidence` -> `M08`; M08-F-kernel-WED-generic-HWRRO-refactor; Dense-read: despite the mt7987 title, the patch body is a large WED refactor with MT7987-only data plus generic and MT7988-adjacent changes: MT7988 msdu_pg_ring2_cfg/wo_support fields, WED v3/v3.1 handling, HWRRO v3/v3.1 branches, WO support gating, register/header/public mtk_wed API changes, and WED MCU/debugfs adjustments.
- `001119`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch adds PPE drop configuration helpers for PSE_PPE_DROP registers and exposes WED PPE drop control.
- `001121`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch adds WDMA disable flow during Wi-Fi L1 SER by toggling PSE_WDMA_PORT link-down bits to prevent stuck incomplete packets.
- `001122`: `needs-evidence` -> `M08`; M08-F-kernel-WED-PPE-runtime-stack; Dense-read: patch narrows mtk_wed_irq_get external mask to avoid false alarms from TKID WO payload status.
- `001123`: `needs-evidence` -> `M08`; M08-G-TOPS-tunnel-offload; Dense-read: TOPS tunnel offload patch adds enum flow_offload_tnl values for GRETAP/PPTP/L2TP/VXLAN/NATT and a tnl_type field to flow_offload_hw_path; no direct 8X tunnel policy or target equivalence is proven yet.

## Secondary Review Handoffs

- M07: `000352`, `000356`, `000358`, `000359`, `000360`, `000394`, `000406`, `000417`, `000431`, `000436`, and the MLO-performance aspect of `001112` need wireless userspace/MLO policy review. For `000375`, only the ordinary ADDBA policy aspect is M07-adjacent; the row owner remains M08 because the patch affects WED TXS and WDMA forward-path behavior.
- M04/M05: PPE, flowtable, HNAT, WDMA, bridge, DSCP, RSS/LRO, and SFP/10G datapath interactions in `001027`-`001105`, `001119`, and `001123` depend on basic/full wired validation before M08 runtime acceptance.
- M06: mt76/WED rows require basic Wi-Fi hardware probe and firmware-load closure before WED offload can be tested.
- M11: throughput, stability, and long-run performance validation belongs after M08 implementation evidence exists; M08 review matrix alone is not performance acceptance.

## TODOs

- Compare target 25.12 kernel 6.12 netfilter flowtable UAPI against vendor `nf-flow-netlink` and libnfnetlink `NFNL_SUBSYS_FLOWTABLE`.
- Compare target mt76 WED default/module-param behavior against vendor `MODPARAMS.mt7996e:=wed_enable=1`.
- Split-compare `000350` debug/testmode/procfs hunks from functional WED/RRO/offload datapath hunks before deciding migration.
- Establish whether target 25.12 WED/RRO/HWRRO stack already covers the vendor mt76 and kernel WED SER/RRO fixes.
- Split-compare shared mt76/mt7996 WED/HWRRO rows `000374`, `000400`, `000421`, and `000426`; do not drop them from non-8X title text, and do not migrate mt7990/mt7987-only hunks into 8X.
- Compare `000375` target BA/WED forward-path behavior because its body affects WED TXS BA status and WDMA AMSDU TID mapping.
- Compare `001063` target tunnel/offload/crypto Ethernet inline handling because the vendor patch changes HNAT-disabled tunnel metadata in the direct 8X config state.
- Split-compare `001116` debugfs/counter visibility from WED reset/attach runtime hunks.
- Split-compare `001118` against target 6.12 `mtk_wed` and mt76 WED stack hunk-by-hunk; extract only direct 8X-relevant gaps if any, and do not migrate or ignore the entire vendor patch as one unit.
- Decide whether HNAT is intentionally out of scope because direct 8X does not enable `kmod-mediatek_hnat`, or whether a later explicit M08 policy will import/rewrite it.
- Validate PPE/nft/xt bridge, DSCP, WDMA, RSS/LRO, TOPS, and WED behavior only after M04/M05/M06 prerequisites are stable.

## Unreported Minimalism Gate

Gate result: pass for round2-audited remediation. The matrix does not use hidden minimalism to drop acceleration work. Conservative `needs-evidence` rows explicitly name missing target/runtime evidence and owner step. Final drops are limited to non-8X firmware package rows, while mixed-title WED/mt76 rows such as `000350`, `000374`, `000400`, `000421`, `000426`, `001116`, and `001118` are not dropped or review-only from the filename or subject alone. Review-only/debug/testmode rows are separated from runtime acceptance unless their patch body also changes datapath or runtime behavior.

## Remaining Risk

Formal three-agent no-context audits round1 and round2 are completed, and round1 remediation has been applied. M08 still has high residual implementation risk because many vendor acceleration patches are large, target 25.12 has newer kernel/mt76/netfilter/WED code, and direct 8X evidence proves topology/package prerequisites but not runtime offload success. Mixed-title or debug-named shared-code rows `000350`, `000374`, `000400`, `000421`, `000426`, `001116`, and `001118` remain split-comparison risks requiring target 25.12/6.12 review. Residual risks are deferred to the listed owner steps, especially M04/M05/M06/M07/M08/M11.

## Next Audit Instructions

Any follow-up auditors should verify TSV coverage against the M08 JSON, dense-read the high-risk rows listed above, compare target 25.12 for every `superseded-by-target` claim, confirm the remaining non-8X firmware drops against direct 8X image package evidence, check mixed-title or debug-named shared-code WED/mt76 rows such as `000350`, `000374`, `000400`, `000421`, `000426`, `001116`, and `001118` against actual patch body and target code, and check that M08 does not claim wired/Wi-Fi/runtime/storage success.
