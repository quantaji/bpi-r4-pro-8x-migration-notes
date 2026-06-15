# M05 MxL86252 Feature Split

Purpose: record the M05.01 boundary for MxL86252 before implementation starts, so
optional or later-stage switch features are not lost and are not accidentally
mixed into basic wired bring-up.

## Hardware Relationship

MxL86252 and AS21xxx are peer devices in the M05 wired topology, not a parent
and child pair.

- MxL86252 is the external DSA switch behind the MT7988 GMAC2 path. It owns the
  2.5G switch ports and the MxL-side 10G combo path.
- AS21xxx PHYs are 10G copper PHYs on combo paths. They are required for RJ45
  10G behavior and can block combo runtime validation, but they are not part of
  the MxL switch driver itself.
- SFP1/SFP2 are physical endpoints, not user-facing interface names. M05 must
  keep hardware endpoint names, kernel/netdev labels, and OpenWrt logical roles
  separate.

Recommended implementation order:

1. M05.01: MxL86252 DSA/tagger/package/DTS/old-firmware compatibility.
2. M05.02: AS21xxx firmware, C45 binding, autoneg, IPC, and cold-boot behavior.
3. M05.03: SFP/RJ45 combo mux runtime switching with SFP priority.
4. M05.04: final OpenWrt logical roles and defaults.
5. M05.05: runtime validation contract.

## M05.01 Required MxL Scope

M05.01 should include the switch functionality needed for a normal OpenWrt
wired runtime:

- MxL86252 DSA driver core and package glue;
- MxL native tagger and 802.1Q tagger, with 802.1Q tag behavior treated as
  required for 8X. Use the OpenWrt main tag protocol naming from the selected
  driver stack, currently `mxl862xx-8021q`, and adapt the 8X DTS instead of
  preserving the vendor-only `mxl862_8021q` spelling;
- MDIO, host interface, CRC, cleanup, and built-in PHY support required by the
  driver stack;
- phylink, SerDes, PCS, port enable/disable, and port MTU behavior required for
  the 8X topology;
- bridge, VLAN, FDB, MDB, STP, link-local or multicast trap behavior needed for
  ordinary OpenWrt switching;
- ethtool statistics and get_stats64 as normal support and diagnostics;
- old firmware compatibility for board firmware 1.0.70 / 1.0.70.70, including
  feature/version gating, legacy PCS fallback, old-PCE-rule avoidance, and
  longer command timeout where required. The exact old-firmware patch subset
  must be re-read before implementation, especially patches marked
  DO-NOT-SUBMIT;
- driver structure must leave the MxL-side combo mux implementable, but the
  runtime mux glue itself is an M05.03 combo-switching deliverable, not the
  M05.01 DSA-base gate.

## MxL Pending Feature Decision

Decision update: if an MxL feature already exists in the OpenWrt main
backport/pending patch stack, M05 may import the implementation together with
the MxL driver stack instead of postponing the source changes. Validation and
runtime ownership still stay split so acceleration, firmware-write, and
diagnostic behavior do not hide basic wired bring-up failures.

| Feature | Stage | Reason |
| --- | --- | --- |
| MxL HNAT/PPE/WED/offload tag integration | M08 | Hardware acceleration must not hide basic wired defects; do not enable or validate acceleration during M05. |
| MxL LAG hardware offload | Implement with MxL pending stack if dependency-clean; runtime/performance validation in M08 | LAG hardware offload can reduce CPU load and belongs with acceleration/offload validation; generic Linux/OpenWrt bonding is separate. |
| Switch hardware bridge/VLAN acceleration beyond normal DSA correctness | M08 validation | Normal DSA bridge/VLAN correctness is M05; performance/offload validation belongs after non-offloaded switching is correct. |
| Temporary 6.12 combo mux glue | M05.03 | Required for SFP/RJ45 runtime switching, but it should be a separate, future-replaceable layer rather than part of the MxL DSA-base gate. |
| MxL devlink firmware flash/update | Implementation may be imported with pending stack; actual flash testing gated by M10 recovery strategy and M11 release validation | M05 must support old firmware without requiring upgrade; switch firmware flashing has recovery risk and no known required blob. |
| MxL devlink version/reporting only | Implement with pending stack if present; validate in M11 | Safe read-only reporting is useful diagnostics, but it is not a basic wired runtime gate. |
| PRBS/BERT SerDes self-test | Implement with pending stack if present; validate in M11 | Link self-test is useful diagnostics, not required for normal OpenWrt wired operation. |
| Mirror port support | Implement with pending stack if dependency-clean; validate in M11 | Useful for packet capture and admin workflows, not a base runtime requirement. |
| MxL custom debugfs/netlink diagnostics | M11, with M08 ownership if tied to offload debug | Private debug/control ABIs should not enter M05 unless required to diagnose bring-up or already part of the selected upstream-style stack. |

## Upstream Acceptance Notes

The direct vendor MxL driver is evidence for 8X hardware behavior, but it is not
automatically upstream-ready. An OpenWrt-acceptable version should preserve
authorship and license provenance, avoid private board-specific hacks, fit DSA
and phylink conventions, avoid new userspace ABI without review, and keep
temporary combo-mux glue clearly replaceable by the future upstream mux model.
