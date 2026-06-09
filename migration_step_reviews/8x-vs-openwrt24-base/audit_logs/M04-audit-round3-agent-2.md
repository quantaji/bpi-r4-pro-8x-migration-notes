Verdict: accept

**Evidence Read**

Path aliases:
- `R=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/migration-notes-repo`
- `A=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/analysis`
- `D=$A/diffsets/8x-vs-openwrt24-base/files`
- `V=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/vendors/BPI-R4PRO-8X-OPENWRT-V24.10.0-Master-Devel`
- `T=/mnt/nvmefs/Hobbies/bpi-r4-pro-8x-migration/reference-source-codes/upstreams/openwrt-25.12.4`

Review/rule files inspected:
- `R/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.md`
- `R/migration_step_reviews/8x-vs-openwrt24-base/M04-basic-wired-management.files.tsv`
- `R/rules/disposition-tags-v1.json`
- `R/rules/feature-migration-step-map-v1.json`
- No audit log contents were read.

JSON/index files inspected:
- `A/migration-step-routing/8x-vs-openwrt24-base/by-step/M04-basic-wired-management.json`
- `A/migration-step-routing/8x-vs-openwrt24-base/summary/step-file-index.tsv`
- Single off-matrix lookup: `A/migration-step-routing/8x-vs-openwrt24-base/by-step/M03-board-identity-power-i2c-gpio-factory-data.json` for `001003` membership only.

Direct 8X vendor source files inspected:
- `V/target/linux/mediatek/filogic/base-files/etc/board.d/02_network`
- `V/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7988a-bananapi-bpi-r4-pro-8x.dts`
- `V/target/linux/mediatek/filogic/base-files/etc/config/network`
- `V/target/linux/mediatek/filogic/base-files/etc/config/firewall`

Target 25.12 files inspected:
- `T/target/linux/mediatek/filogic/base-files/etc/board.d/02_network`
- `T/package/network/services/dnsmasq/Makefile`
- `T/package/network/services/dnsmasq/patches/200-ubus_dns.patch`
- `T/target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch`
- `T/target/linux/mediatek/patches-6.12/750-net-ethernet-mtk_eth_soc-add-mt7987-support.patch`
- `T/target/linux/mediatek/patches-6.12/751-net-ethernet-mtk_eth_soc-revise-hardware-configuration-for-mt7987.patch`

**Structural Checks**

Pass:
- TSV schema: exact 12-column header at `M04-basic-wired-management.files.tsv:1`.
- TSV rows: 111 data rows, 111 unique file IDs.
- JSON expected counts: 111 files / 115 assignments at `M04-basic-wired-management.json:2` and `:7`.
- Missing/extra/duplicate file IDs vs M04 JSON: none.
- Exact TSV-vs-M04-JSON field match for `status`, `path`, `file_kind`, `features`, `route_classes`: 0 mismatches.
- Legal dispositions: all values are allowed by `rules/disposition-tags-v1.json:4-36`.
- Legal owner steps: all owner steps are in `M00` through `M11`, defined at `feature-migration-step-map-v1.json:911-971`.
- `defer` / `needs-evidence` TODO check: 0 failures; each has a named legal owner and actionable TODO.
- Markdown counts match TSV/JSON: status and feature counts at `M04-basic-wired-management.md:65-97`; disposition/owner/group counts at `:169-217`.

Observed non-defect:
- `step-file-index.tsv:546` still orders `000960` features as `...network:vlan:bridge,openwrt:board-d:network`, while M04 JSON orders `openwrt:board-d:network` before `network:vlan:bridge` at JSON `:1164-1196`. TSV line `47` follows the M04 by-step JSON exact order, as documented in markdown `:21`.

**Dense Sampling Coverage**

Sampled all TSV groups at least once:
- `direct-8x-boardd-network-defaults`: `000960`
- `direct-8x-network-config-evidence`: `000963`
- `direct-8x-dts-network-context`: `000859`
- `basic-mdio-needs-evidence`: `001018`, `001022`
- `dnsmasq-version-sync`: `000504`, `000505`, `000508`
- `mtk-eth-forced-reset-dump`: `001025`
- `full-wired-pcs-dsa-sfp`: `001015`, `001124`
- `mt7988-rfb-wired-reference`: `000861`
- `ethernet-mux-refactor`: `001034`
- `hnat-driver-acceleration`: `000896`
- `acceleration-performance-ppe-wed`: `001027`, `001106`
- `pppq-acceleration-init`: `000825`
- `ser-monitor-runtime-robustness`: `001030`
- `wireless-netifd-policy`: `000496`
- `wifi-userspace-policy`: `000826`
- `reset-boot-count-storage-init`: `000493`
- `non-8x-mt7987-wired-reference`: `000830`
- `mt7987-ethernet-driver-reference`: `001033`
- `mtk-eth-proprietary-debugfs`: `001023`
- `mtk-eth-probe-cleanup`: `001085`
- `non-wired-optee-init`: `000482`
- `packet-steering-generic-netifd`: `000495`
- `relayd-generic-init`: `000786`
- `vendor-firewall-policy`: `000961`

No sample exposed a mismatch requiring full-cluster expansion.

**Sample Evidence Map**

- `000482`, TSV `:2`: OP-TEE service only starts/stops `tee-supplicant`; diff `D/package/mtk/optee-mediatek/files/optee.init.patch:13-24`.
- `000493`, TSV `:6`: bootcount helper is A/B boot counter logic, not wired; diff `D/package/mtk/reset-boot-count/src/reset-boot-count.c.patch:31-95`, init gating at `D/package/mtk/reset-boot-count/files/reset-boot-count.init.patch:13-18`.
- `000495`, TSV `:8`: generic packet-steering regex change only; diff `D/package/network/config/netifd/files/usr/libexec/network/packet-steering.uc.patch:7-12`.
- `000496`, TSV `:9`: wireless reload revert; diff `D/package/network/config/netifd/patches/mtk-0001-Revert-wireless-reload-wireless-device-if-any-vif-ne.patch.patch:10-16` and `:26-67`.
- `000504`, TSV `:10`: vendor dnsmasq 2.90 to 2.91 refresh; diff `D/package/network/services/dnsmasq/Makefile.patch:8-18`; target already 2.91 at `T/package/network/services/dnsmasq/Makefile:10-17`.
- `000505`, TSV `:11`: vendor deletes dnsmasq 2.91 upstream-fix patch; diff `D/package/network/services/dnsmasq/patches/0001-Fix-spurious-resource-limit-exceeded-messages.patch.patch:7-27`; target 2.91 evidence above.
- `000508`, TSV `:14`: ubus patch refresh; diff `D/package/network/services/dnsmasq/patches/200-ubus_dns.patch.patch:11-25`; target patch exists at `T/package/network/services/dnsmasq/patches/200-ubus_dns.patch:1-36`.
- `000786`, TSV `:15`: relayd reload-to-restart service trigger; diff `D/package/network/services/relayd/files/relay.init.patch:5-10`.
- `000825`, TSV `:16`: PPPQ/EBL init writes `qos_toggle` under HNAT/PPE debugfs; diff `D/target/linux/mediatek/base-files/etc/init.d/pppq-ebl.init.patch:13-20`.
- `000826`, TSV `:17`: RSNO/MLO wireless UCI changes; diff `D/target/linux/mediatek/base-files/sbin/rsno-off.sh.patch:9-30`.
- `000830`, TSV `:18`: MT7987 overlay uses `gmac0`, MDIO phy31, HNAT eth0; not 8X authority. Diff `D/target/linux/mediatek/files-6.6/arch/arm64/boot/dts/mediatek/mt7987-netsys-eth0-an8801sb.dtso.patch:14-43`.
- `000859`, TSV `:30`: direct 8X DTS enables GMACs and MAC cells; vendor DTS `:149-168`, MDIO/C45/MxL at `:182-245`, nvmem cells at `:679-688`.
- `000861`, TSV `:31`: MT7988 RFB overlay, not 8X board; vendor RFB DTS `:19-21`, switch/MDIO at `:42-74`.
- `000896`, TSV `:38`: HNAT driver makefile; diff `D/target/linux/mediatek/files-6.6/drivers/net/ethernet/mediatek/mtk_hnat/Makefile.patch:9-15`.
- `000960`, TSV `:47`: direct 8X board.d LAN/WAN defaults at vendor `02_network:196-197`; generic MAC helper at `:323-327`; direct 8X nvmem confirmation in DTS `:679-688`. TSV feature order matches M04 JSON `:1164-1196`, not step index `:546`.
- `000961`, TSV `:48`: firewall opens WAN and lists WWAN networks in WAN zone; vendor firewall `:17-27`.
- `000963`, TSV `:49`: static config repeats wired ports but also hardcodes static/non-wired defaults; vendor network `:11-41`, WWAN at `:43-61`; diff `D/target/linux/mediatek/filogic/base-files/etc/config/network.patch:17-67`.
- `001015`, TSV `:50`: PCS polarity/SGMII behavior; diff `D/target/linux/mediatek/patches-6.6/999-2607-net-pcs-mtk-lynxi-add-individual-polarity-control.patch.patch:10-19`, `:47-57`, `:90-110`.
- `001018`, TSV `:52`: MDIO reset delay patch; diff `D/target/linux/mediatek/patches-6.6/999-2700-net-ethernet-mtk_eth_soc-add-mdio-reset-delay.patch.patch:24-41`; direct 8X C45 PHYs/switch exist in DTS `:182-245`, but no runtime proof.
- `001022`, TSV `:55`: MDC divider reconfiguration patch; diff `D/target/linux/mediatek/patches-6.6/999-2704-net-ethernet-mtk_eth_soc-revise-mdc-divider-configur.patch.patch:12-14`, `:29-38`, `:60-113`; direct 8X DTS only supports need for validation, not acceptance.
- `001023`, TSV `:56`: proprietary debugfs support; diff `D/target/linux/mediatek/patches-6.6/999-2705-net-ethernet-mtk_eth_soc-support-proprietary-debugfs.patch.patch:14-17`, `:106-120`.
- `001025`, TSV `:58`: forced-reset dump diagnostic; vendor diff `D/target/linux/mediatek/patches-6.6/999-2707-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch.patch:10-13`, `:52-101`; target comparable patch `T/target/linux/generic/hack-6.12/730-net-ethernet-mtk_eth_soc-add-hw-dump-for-forced-rese.patch:4-7`, `:44-101`.
- `001027`, TSV `:60`: RSS/LRO register support; diff `D/target/linux/mediatek/patches-6.6/999-2709-net-ethernet-mtk_eth_soc-add-rss-lro-reg.patch.patch:10-16`, `:72-80`, `:117-120`.
- `001030`, TSV `:63`: SER monitor runtime recovery; diff `D/target/linux/mediatek/patches-6.6/999-2712-net-ethernet-mtk_eth_soc-refactor-SER-monitor.patch.patch:10-15`, `:61-120`.
- `001033`, TSV `:66`: MT7987 support, not 8X; diff `D/target/linux/mediatek/patches-6.6/999-2715-net-ethernet-mtk_eth_soc-add-mt7987-support.patch.patch:10-13`; target has MT7987 patch at `T/target/linux/mediatek/patches-6.12/750-net-ethernet-mtk_eth_soc-add-mt7987-support.patch:4-7`.
- `001034`, TSV `:67`: Ethernet mux capability refactor; diff `D/target/linux/mediatek/patches-6.6/999-2716-net-ethernet-mtk_eth_soc-convert-cap_bit-in-mtk_eth_.patch.patch:10-15`, `:27-31`.
- `001085`, TSV `:85`: notifier cleanup, review-only; diff `D/target/linux/mediatek/patches-6.6/999-2771-net-ethernet-mtk_eth_soc-add-unregister-notifier.patch.patch:21-32`, `:38-43`.
- `001106`, TSV `:97`: adaptive PPPQ/PPE mode; diff `D/target/linux/mediatek/patches-6.6/999-3019-net-ethernet-mtk_ppe-add-adaptive-PPPQ-mode.patch.patch:10-16`, `:94-107`, `:129-134`.
- `001124`, TSV `:112`: multi-DSA plus PPPQ/QDMA/PPE/offload mixed patch; diff `D/target/linux/mediatek/patches-6.6/999-9800-mt7988a-bananapi-bpi-r4pro-support-multiple-dsa-switch-fixed.patch.patch:42-58`, `:101-110`, `:148-181`, `:299-317`, `:451-476`, `:521-527`.
- `001003`, off-matrix: M04 markdown records it only as handoff at `M04-basic-wired-management.md:110` and `:238`; no TSV row; not in M04 JSON. Diff confirms MAC offset polarity topic at `D/target/linux/mediatek/patches-6.6/999-2004-arm64-dts-mt7988-fix-typo-for-the-LAN-and-WAN-MAC-address.patch.patch:25-38`.

**Findings**

No actionable findings.

**No-Issue Confirmations**

- M04 boundary is correctly stated: covered scope at markdown `:45-51`, excluded DSA/SFP/10G/offload/Wi-Fi/storage/runtime success at `:53-61`.
- `000960` is correctly the core rewrite row, based on direct 8X `02_network` and direct 8X DTS nvmem evidence.
- `000963` is correctly limited to wired port-group evidence and not accepted as a static config copy.
- `000859` is correctly review-only for M04, with DTS rewrite/storage/full-wired work handed to M03/M10/M05.
- `001018` and `001022` are correctly `needs-evidence`, not accepted from MTK SDK patches alone.
- `001124` correctly keeps M05 primary ownership and records M08 secondary review for PPPQ/QDMA/PPE/offload hunks.
- DNSMasq rows and `001025` are properly treated as target-superseded structure/diagnostic claims, not 8X hardware truth.
- Round 1 and round 2 audit summaries are recorded without raw logs at markdown `:15-39`; no round 3 completion claim was found.

**Residual Risk**

Runtime validation remains for actual 8X wired reachability, link enumeration, MDIO timing, `eth1` copper WAN behavior, bridge membership, and Factory MAC assignment. Later work remains correctly outside M04: M05 for full switch/SFP/10G/DSA, M07 for wireless userspace policy, M08 for acceleration/offload/performance, and M10 for storage/sysupgrade/boot-count policy.
