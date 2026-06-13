# M09 Board Extras And Expansion Batch Review

Project Phase 2 / Migration Step M09: Board Extras And Expansion.

## Audit Status

This file is the M09 round1-audited batch review. Formal no-context audit round1 is completed; all three reviewers returned `accept`, and no actionable findings were reported. Raw audit reports and the sampling plan are saved in the local audit logs.

No migration code was written, no image was compiled, no runtime USB/PCIe/cellular/fan result is claimed, and no storage/install/sysupgrade behavior is accepted here.

## Formal No-Context Audit Summary

- `M09-audit-round1-agent-1`: `accept`; no actionable findings.
- `M09-audit-round1-agent-2`: `accept`; no actionable findings.
- `M09-audit-round1-agent-3`: `accept`; no actionable findings.

Informational note: agent 3 observed that `step-file-index.tsv` feature ordering differs from the by-step JSON for 7 rows, but the M09 TSV matches the by-step JSON exactly. No M09 artifact change is required for that note.

## Scope / Non-goals

Allowed M09 scope:

- Direct 8X static board extras: LEDs, buttons, fan/PWM, thermal/fan wiring, USB controller topology, PCIe expansion slot topology, M.2 key-B / miniPCIe cellular slot mapping.
- Static cellular network/firewall defaults needed to understand expansion interfaces.
- USB/xHCI patches only as board-extra evidence until target equivalence and runtime need are proven.
- Non-8X MT7987/RFB/R4Lite DTS only as supporting references.

Not allowed in M09:

- Declaring USB, PCIe, cellular, fan thermal, Wi-Fi, wired, storage, NAND/eMMC, sysupgrade, or install runtime success.
- Treating MT7987, RFB, BPI-R4Lite, or other vendor-family files as direct 8X hardware truth.
- Copying vendor `etc/config/network` or firewall defaults wholesale.
- Pulling M04/M05 wired behavior, M06/M07 Wi-Fi behavior, M08 offload, or M10 storage/install semantics into M09.

## Structural Summary

- Input JSON file count: 42 files.
- Input JSON assignment count: 71 assignments.
- Input status counts: `A=39`, `M=3`.
- JSON assignment-level route class counts: `primary=47`, `supporting=16`, `static-only=8`.
- TSV collapsed file-level route class counts: `primary=31`, `supporting=16`, `static-only=3`.
- TSV rows: 42, one row per M09 by-step input file.

Disposition counts:

- `defer`: 3
- `needs-evidence`: 2
- `review-only`: 34
- `rewrite`: 1
- `static-only`: 2

Owner counts:

- `M09`: 39
- `M10`: 3

## Direct 8X Evidence

- Direct 8X base DTS `000859` is the authoritative M09 hardware source. It defines reset GPIO13, WPS GPIO14, PCA9555 red/blue system LEDs, PCIe0/PCIe1 as mPCIe SIM2/SIM3, PCIe2 as M.2 key-B SIM1, PCIe3 as M.2 key-M SSD, PWM fan on pwm0, ssusb0 as U2-only because U3 serdes is shared with pcie2, and ssusb1 enabled.
- Direct 8X Wi-Fi overlay `000858` confirms pcie0 and pcie1 are used for mt7996 Wi-Fi overlay nodes, but M09 uses that only as PCIe topology context. Wi-Fi hardware/userspace behavior remains M06/M07.
- Direct vendor network/firewall files add static WWAN/WWAN6 on `usb0` and WWAN_Q/WWAN6_Q on `wwan0_1`, and include those interfaces in the WAN firewall zone. This is static cellular default evidence only because no cellular module runtime evidence is available.
- Target OpenWrt 25.12 has MT7987 and other MT7988 DTS references, but no direct 8X DTS. Target 25.12 has MT7988 USB DTS patches for ssusb/t-phy/xsphy context, but the vendor USBIF/HQA toolkit files and embedded-host TPL patch are not accepted as direct runtime requirements without further evidence.

## Topic/Substep Summary

### M09-A Direct 8X Board Extras

`000859` is `rewrite -> M09`. It is the only direct 8X base DTS row that carries M09-owned LED/button/fan/PWM/USB/PCIe/cellular-slot static topology. The row must be rewritten into target 25.12 DTS structure rather than copied wholesale, because the same file also contains M04/M05 wired, M06 Wi-Fi, and M10 storage content.

### M09-B PCIe Expansion And Cellular Slots

Direct 8X PCIe truth comes from `000859`: pcie0 and pcie1 are mPCIe SIM slots, pcie2 is M.2 key-B SIM1, and pcie3 is M.2 key-M SSD. `000858` is supporting evidence for pcie0/pcie1 Wi-Fi overlay use only. MT7987/RFB/R4Lite PCIe overlays are `review-only` because they help explain vendor style but cannot decide 8X topology.

### M09-C Static Cellular Boundary

`000961` and `000963` are `static-only -> M09`. They document vendor defaults for `usb0` and `wwan0_1` cellular interfaces and WAN-zone firewall inclusion. They do not prove a modem is present, do not validate QMI/MBIM naming, and must not be copied wholesale over target network/firewall defaults.

### M09-D USB / xHCI Controller Evidence

`000941`-`000954` plus `001150` form a MediaTek USBIF/HQA compliance/debug toolkit and are `review-only`. `001149` is also `review-only` because direct 8X DTS deletes `mediatek,p0_speed_fixup` on ssusb0. `001151` is `needs-evidence -> M09` because it changes USB core embedded-host/TPL behavior and xhci-mtk `tpl_support`, which is functional enough to require target and direct DTS comparison before any migration decision.

### M09-E Non-8X DTS Supporting Evidence

MT7987, MT7988 RFB, MT7988D RFB, and BPI-R4Lite DTS rows are `review-only` unless their primary body is storage/rootdisk policy. RFB/R4Lite LEDs, buttons, PCIe, USB, fan, and thermal snippets are not direct 8X authority.

### M09-F Storage Overlay Boundary

`000845`, `000860`, and `000872` are `defer -> M10`. They include SPIM-NAND/eMMC/rootdisk/NMBM semantics and only incidental PCIe slot clues. M09 must not accept NAND/eMMC/rootdisk/storage policy.

## High-risk Rows

- `000859`: direct 8X base DTS; rewrite only static M09 board extras/topology and hand off wired/Wi-Fi/storage content.
- `000875`: mixed MT7988 SoC dtsi row; needs target comparison because it touches lvts default status plus M04/M08 SoC network/crypto changes.
- `000941`-`000954`: dense-read USB HQA/debug toolkit sources; review-only, not runtime.
- `001149`: direct 8X DTS deletes the property that enables the patch path; review-only.
- `001150`: wrapper for USBIF/HQA debugfs toolkit; review-only.
- `001151`: embedded-host/TPL functional patch; needs evidence before migration.
- `000961`/`000963`: static cellular UCI defaults; static-only, no runtime modem proof.

## Static-only Cellular Boundary

M09 records cellular slot/interface facts but does not validate a modem:

- DTS static topology: pcie0 mPCIe SIM2, pcie1 mPCIe SIM3, pcie2 M.2 key-B SIM1.
- Network defaults: `WWAN`/`WWAN6` on `usb0`; `WWAN_Q`/`WWAN6_Q` on `wwan0_1`.
- Firewall defaults: those four WWAN interfaces are added to the WAN zone.

The static-only TODO is to validate actual modem enumeration, protocol naming, hotplug behavior, and firewall policy once cellular hardware is available. Until then, the UCI rows are evidence, not runtime acceptance.

## Secondary Review Handoffs

- M04/M05: Network/PHY/DSA/SFP/10G content inside `000859`, RFB Ethernet LED overlays `000861`/`000862`/`000864`/`000865`/`000867`/`000876`, and RFB MXL content in `000869`.
- M06/M07: Wi-Fi overlay behavior in `000858` and pcie0/pcie1 Wi-Fi nodes inside `000859`.
- M08: SoC dtsi crypto/EIP and Ethernet/offload-adjacent hunks in `000875`.
- M10: Storage/rootdisk/partition/install semantics in `000845`, `000860`, `000872`, and storage portions of `000859`.
- M11: Runtime validation for USB devices, PCIe expansion, fan thermal behavior, and cellular module enumeration after implementation exists.

## TODOs

- Rewrite direct 8X M09 static DTS content from `000859` into target 25.12 structure without copying unrelated wired/Wi-Fi/storage hunks.
- Compare `000875` against target 25.12 MT7988 DTS/6.12 patches to decide whether any thermal/fan/LVTS foundation hunk remains M09-owned.
- Compare `001151` against target 25.12 USB host/TPL behavior and direct 8X DTS properties before deciding whether embedded-host support is needed.
- Keep `000941`-`000954` and `001150` out of the migration unless explicit USBIF/HQA compliance testing requires the debug toolkit.
- Validate cellular `usb0`/`wwan0_1` defaults with real cellular hardware before promoting static-only defaults to runtime behavior.
- M10 must review SPIM-NAND/eMMC/rootdisk rows `000845`, `000860`, and `000872`.

## Unreported Minimalism Gate

Gate result: pass for round1-audited review. The review does not use a hidden small-diff shortcut: direct 8X DTS was read before classifying topology, USB source bodies were dense-read before being kept review-only, storage rows were explicitly deferred to M10, and static cellular defaults record missing runtime evidence and TODOs. Non-8X DTS rows are not dropped or promoted from filename alone; they are scoped as supporting evidence.

## Remaining Risk

Formal no-context audit round1 is completed. M09 still has implementation/runtime risk around target 25.12 DTS integration, MT7988 LVTS/fan foundation, USB embedded-host/TPL behavior, cellular enumeration, and the M10 storage/rootdisk boundary. Runtime risks are deferred to listed owner steps, especially M04/M05/M06/M07/M08/M10/M11.

## Future Review Instructions

Implementation review should re-check direct 8X `000859`, target 25.12 DTS integration, USB high-risk rows `000941`-`000954` and `001149`-`001151`, the M10 storage boundary, and static cellular defaults before any runtime claims.
