# BPI-R4 Pro 8X Migration Roadmap

This roadmap defines the working order for migrating the BPI-R4 Pro 8X vendor OpenWrt 24.10 behavior into a clean OpenWrt 25.12.4 implementation.

It is not a patch list. It is the order in which feature clusters should be inspected, designed, implemented, and tested.

## Evidence Policy

Use evidence in this order:

1. BPI-R4 Pro 8X vendor source code is the behavior authority.
2. BPI-R4 Pro 4E, BPI-R4, and BPI-R4 Lite vendor source code are strong vendor-family references.
3. MTK vendor trees and feeds are SoC and SDK implementation references.
4. OpenWrt upstream, Linux upstream, U-Boot upstream, and mt76 upstream are target API, structure, history, and discussion references. They do not decide BPI-R4 Pro 8X hardware behavior.

Do not copy upstream or similar-board hardware behavior into 8X without checking 8X vendor evidence and board-specific topology.

## Universal Gates

Every phase must pass these gates before implementation is accepted.

### Context Gate

Before choosing an implementation, inspect the relevant 8X vendor files, target OpenWrt 25.12 files, feature-routing records, and any cluster notes.

If the context has not been inspected, do not guess a small patch.

### Polarity Gate

Separate added, modified, deleted, and renamed files before making migration decisions.

`A` files may represent vendor additions. `M` files may represent integration changes. `D` files often represent vendor removal or replacement of upstream behavior. `R*` files need both old and new paths reviewed.

Do not treat deleted upstream patches or packages as hardware support until the deletion semantics are understood.

### Unreported Minimalism Gate

Every phase review, checkpoint, and commit review must ask whether the work used an unreported minimal-change shortcut.

Triggers include:

1. preserving vendor structure only because it is the shortest path,
2. skipping source/context inspection because the local edit looks obvious,
3. under-implementing the current phase because a smaller change passes a quick test,
4. pulling in next-phase behavior because it is nearby,
5. accepting a workaround without naming why it is temporary.

If any trigger is present, the work is accepted only if it documents the reason, missing evidence, owning later phase, and a concrete TODO.

### Phase Boundary Gate

Complete the current phase properly. Do not pre-implement later phases just because the code is adjacent.

When a later-phase dependency blocks the current phase, create a TODO and stop at the documented boundary.

## Phase 00: Vendor Evidence And Polarity Gate

Goal: build the evidence matrix that later phases use.

Primary work:

1. group feature tags by phase,
2. split files by `A/M/D/R` status,
3. identify direct 8X files versus vendor-family or MTK-wide changes,
4. mark noisy broad tags that must not drive decisions alone.

Must inspect:

1. `analysis/feature-routing/8x-vs-openwrt24-base`,
2. 8X vendor DTS, DTSO, image, U-Boot, and board.d files,
3. matching 4E vendor files only as vendor-family reference.

Exit criteria:

1. each feature tag has an owning phase or an explicit deferred/static/review-only status,
2. each phase has a file list grouped by `A/M/D/R`,
3. broad tags such as `wireless:mac80211:patch`, `wireless:hostapd:build`, and low-confidence `dts:soc:base` are not used as direct migration instructions.

## Phase 01: Clean Build And Image Skeleton

Goal: create the minimal clean OpenWrt 25.12 target structure needed to build a BPI-R4 Pro 8X image.

This phase builds structure, not complete hardware behavior.

Primary work:

1. 8X device profile,
2. DTS and DTSO selection,
3. image recipe and artifact declarations,
4. required package lists,
5. build helper and host tool requirements,
6. TF-A and U-Boot build integration needed for images.

Do not:

1. enable NAND/eMMC install behavior,
2. claim wired, wireless, storage, or acceleration runtime success,
3. migrate broad wireless or acceleration patch stacks.

Exit criteria:

1. OpenWrt 25.12 can select and build the 8X target image skeleton,
2. image artifacts are named and generated intentionally,
3. every included boot/image/package change has a direct reason tied to 8X buildability.

## Phase 02: SD Boot No Install

Goal: boot from SD card without writing to NAND or eMMC.

Primary work:

1. SD overlay and rootdisk selection,
2. SD-specific U-Boot environment behavior,
3. FIT/rootfs boot path,
4. recovery behavior only as needed to boot SD safely.

Do not:

1. use vendor boot menu install actions,
2. write NAND or eMMC,
3. validate sysupgrade or factory install paths.

Exit criteria:

1. board boots from SD to userspace,
2. serial log confirms expected SD overlay and rootfs path,
3. NAND/eMMC install menu paths are documented but not exercised.

## Phase 03: Board Identity, Power, I2C, GPIO, Factory Data

Goal: establish board identity and foundational board services that other phases depend on.

Primary work:

1. `model` and `compatible`,
2. factory MAC and calibration data sources,
3. RT5190A PMIC,
4. PCA9545 I2C mux,
5. PCA9555 GPIO expander,
6. AT24 EEPROM devices,
7. PCF8563 RTC presence,
8. reset/WPS buttons,
9. GPIO conflicts and ownership.

Special audit:

Check GPIO4 carefully because 8X vendor DTS uses it as MxL86252 reset hog while the Wi-Fi overlay also uses it for `wifi_12v`.

Exit criteria:

1. board identity is correct,
2. MAC and calibration data source paths are understood,
3. I2C mux channels enumerate as expected,
4. GPIO ownership conflicts are resolved or documented with TODOs.

## Phase 04: Basic Wired Management

Goal: bring up enough wired networking to manage and test the board.

Primary work:

1. Ethernet MAC and MDIO basics,
2. board.d LAN/WAN defaults,
3. MAC address assignment,
4. basic bridge/WAN configuration,
5. direct copper management path.

Do not:

1. generalize from 4E port layout,
2. validate full DSA/SFP behavior,
3. enable hardware acceleration.

Exit criteria:

1. board is reachable over wired network,
2. LAN/WAN defaults match 8X vendor topology,
3. no 4E-only port assumption is present.

## Phase 05: Full Wired Switch, SFP, And 10G

Goal: validate complete wired hardware behavior.

Primary work:

1. MxL86252 external DSA switch,
2. DSA tagging,
3. Airoha PHY firmware,
4. multi-rate PHY behavior,
5. 10GBase-R and USXGMII PCS,
6. SFP cages and I2C,
7. SFP/RJ45 combo mux behavior,
8. VLAN bridge behavior without acceleration assumptions.

Hardware constraint:

Only one SFP module is available. Test SFP1 and SFP2 separately. Use the two available 10G copper ports for interactive 10G tests.

Exit criteria:

1. expected DSA ports appear,
2. copper ports pass link and traffic tests,
3. SFP1 and SFP2 each pass module-detect and link tests when tested individually,
4. combo mux behavior is understood and documented.

## Phase 06: Basic Wi-Fi Hardware

Goal: bring up Wi-Fi radios at the hardware and driver level.

Primary work:

1. PCIe Wi-Fi NIC nodes,
2. mt7996 driver and firmware,
3. Wi-Fi EEPROM and calibration sources,
4. Wi-Fi 12V regulator behavior,
5. hotplug enough to initialize radios.

Do not:

1. tune MLO,
2. optimize performance,
3. migrate broad hostapd/mac80211 patch stacks unless required for basic radio bring-up.

Exit criteria:

1. Wi-Fi radios enumerate,
2. calibration data is loaded from the expected source,
3. a Wi-Fi 6 client can associate for basic functional testing.

## Phase 07: Wireless Userspace, MLO, AFC, And Policy

Goal: migrate wireless userspace and policy behavior after basic radios work.

Primary work:

1. hostapd changes,
2. mac80211 behavior changes,
3. ucode and netifd Wi-Fi scripts,
4. MLO config and runtime,
5. AFC and regulatory behavior.

Do not:

1. use broad wireless patch count as proof of 8X necessity,
2. mix performance offload with userspace correctness,
3. accept regulatory changes without explicit review.

Exit criteria:

1. configured APs start reliably,
2. MLO-related behavior is either working or explicitly deferred,
3. regulatory and AFC changes have clear applicability notes.

## Phase 08: Acceleration And Offload

Goal: enable and test acceleration only after base wired and Wi-Fi paths are correct.

Primary work:

1. PPE flow offload,
2. WED and Wi-Fi offload,
3. WO firmware,
4. HNAT/NAT/routing acceleration,
5. TOPS tunnel offload,
6. crypto acceleration only if required and justified.

Do not:

1. use acceleration to hide basic network defects,
2. combine offload enablement with initial wired or Wi-Fi bring-up,
3. accept throughput-only success without correctness tests.

Exit criteria:

1. offload can be enabled and disabled intentionally,
2. non-offloaded path remains correct,
3. performance and regression tests are documented.

## Phase 09: Board Extras And Expansion

Goal: finish non-core board runtime features after boot, wired, and Wi-Fi are stable.

Primary work:

1. LEDs,
2. fan and thermal zones,
3. buttons,
4. USB controllers,
5. PCIe expansion slots,
6. cellular slot static wiring.

Hardware constraint:

No 4G/5G module is available. Cellular work is static-only unless hardware becomes available.

Exit criteria:

1. LEDs, fan, buttons, and USB behave as expected,
2. PCIe expansion topology is understood,
3. cellular support is documented as static-only or deferred.

## Phase 10: Onboard Storage, Install, And Sysupgrade

Goal: handle persistent onboard storage only after all major runtime hardware is stable from SD.

Primary work:

1. SPI-NAND boot and UBI,
2. sysupgrade platform logic,
3. backup and restore behavior,
4. factory install behavior,
5. eMMC boot and install path,
6. U-Boot storage layout and boot menu review.

Order:

Use `SD -> SPI-NAND -> eMMC`.

Rationale:

SD and eMMC share the same controller path, while SPI-NAND is independent. Keep eMMC until after SD boot and recovery confidence are high.

Exit criteria:

1. NAND install and sysupgrade are tested before eMMC,
2. eMMC write path is tested only after recovery strategy is validated,
3. U-Boot recovery and production bootconf choices are audited before any persistent write.

## Phase 11: Release Validation

Goal: verify the migrated implementation as a coherent OpenWrt 25.12 board target.

Primary work:

1. package closure,
2. build reproducibility,
3. boot and recovery tests,
4. wired, Wi-Fi, USB, fan, LED, button, and storage regression tests,
5. known limitations,
6. commit and patch series review.

Exit criteria:

1. every phase has test evidence or documented limitation,
2. every temporary minimal implementation has a TODO and owning phase,
3. no unreported minimal-change shortcut remains,
4. the remaining diff is organized by feature clusters rather than vendor patch order.
