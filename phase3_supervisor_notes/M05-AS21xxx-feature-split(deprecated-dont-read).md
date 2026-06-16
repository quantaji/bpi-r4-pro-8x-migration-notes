# M05 AS21xxx Feature Split

Purpose: record the AS21xxx scope decision before M05.02 implementation, so
the basic 10G PHY bring-up stays separate from useful but non-blocking PHY
features.

## M05.02 Required Scope

M05.02 should use the OpenWrt/Linux in-kernel AS21xxx driver as the base. Do
not import the vendor `package/kernel/as21xxx` tree wholesale.

Required M05.02 work:

- add the 8X GMAC1/AS21xxx DTS topology and image package selection needed for
  `kmod-phy-aeonsemi-as21xxx`;
- apply the OpenWrt 25.12.4/Airoha AS21xxx fixes to the mediatek target where
  they are not already effective;
- add minimal runtime fixes still missing from the OpenWrt driver when needed:
  model-specific `.get_features`, firmware-loader retry/defer, IPC reply
  matching by active opcode, firmware-readiness `config_init`, and AS21010PB1
  autoneg configuration;
- prove stable AS21xxx binding, firmware load, and no persistent `-22` or
  `-110` runtime failure before combo mux work builds on top of it.

## Follow-Up PHY Features To Preserve

The vendor driver exposes several useful AS21xxx functions through private
debugfs/BBU paths. These should not be copied as-is, but the features are worth
preserving for a later OpenWrt-style implementation.

| Feature | Target stage | Required direction |
| --- | --- | --- |
| WOL | AS21xxx PHY feature follow-up after M05.02 basic runtime | WOL is for waking the local router/host from a low-power state on a matching Ethernet packet. It is not the mechanism for waking downstream client devices; the router can send WOL magic packets to clients without PHY WOL support. Implement through standard PHY/ethtool WOL hooks, not vendor debugfs. |
| EEE / AutoEEE | AS21xxx PHY feature follow-up after M05.02 basic runtime | Useful for idle power management but can affect latency or link stability on marginal links. Implement through standard EEE plumbing where possible, not private debugfs commands. |
| Fast retrain | AS21xxx PHY feature follow-up after M05.02 physical link validation | Useful for faster recovery on noisy or marginal copper links. Implement only after baseline link and combo behavior are stable. |
| Downshift | AS21xxx PHY feature follow-up after M05.02 physical link validation | Useful when 10G cannot train and the PHY should settle at 5G/2.5G/1G. Prefer standard PHY tunable/ethtool-style control if available. |
| Monitoring and logs | AS21xxx PHY diagnostics follow-up after M05.02 basic runtime | Vendor temperature, firmware log, error/status, and runtime-monitoring commands are useful and should be preserved as requirements. Reimplement them through accepted kernel diagnostics, ethtool stats, devlink health/info, hwmon, tracepoints, or debug-only mechanisms with clear ABI boundaries rather than copying the vendor private debugfs control surface. |

These features are not M05.02 bring-up gates. They become implementation
requirements for the later AS21xxx PHY feature follow-up once the base
GMAC1/AS21xxx and combo paths are stable enough to test them without masking
basic wiring or firmware issues.

## Excluded From M05

AS21xxx firmware flash/update is not part of M05. It has recovery risk and
should be handled only in a later firmware-maintenance stage with an
OpenWrt/Linux-appropriate interface such as devlink flash or another accepted
firmware-management path. The vendor debugfs/BBU flash path must not be copied
into M05.

Other vendor-only diagnostic or production interfaces, such as eye scan, cable
diagnostics, raw register poke/read debugfs files, firmware image burn helpers,
test modes, SMI command passthrough, private IRQ controls, and broad debugfs
control nodes, are evidence sources only. Monitoring and log retrieval are
explicit follow-up requirements, but the vendor private control ABI must not be
copied into M05. These functions may be reconsidered later as standard
diagnostics, but they are not required for M05 wired runtime closure.
