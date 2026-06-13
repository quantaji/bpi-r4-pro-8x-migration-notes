#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/wrt-docker-build.sh [command...]

Run an OpenWrt build command inside Docker for the BPI-R4 Pro 8X worktree.
If no command is provided, an interactive shell is opened.

Default worktree:
  ../worktrees/openwrt-bpi-r4-pro-8x

Container modes:
  scripts/wrt-docker-build.sh 'make defconfig'
    Run a one-shot Docker container.

  WRT_CONTAINER=... scripts/wrt-docker-build.sh 'make defconfig'
    Execute inside an already-running container, matching the older
    wrt-in-container.sh workflow.

Important environment:
  WRT_IMAGE             Docker image for one-shot docker run mode.
                        Default: ghcr.io/openwrt/buildbot/buildworker-v3.8.0:v9
                        when WRT_CONTAINER is unset.
  WRT_CONTAINER         Existing container name/ID for docker exec mode.
  WRT_WORKTREE          Host OpenWrt worktree path.
  WRT_INNER             Container worktree path. Default: /workspaces/openwrt-bpi-r4-pro-8x
  WRT_DOCKER_RUNTIME    Docker runtime for docker run mode. Default: runc
  WRT_USER              User override. Default: no override for docker run,
                        buildbot for docker exec.
  WRT_HOME              HOME inside the container. Default: /builder.
  WRT_NOFILE_LIMIT      nofile ulimit inside the container. Default: 4096

Examples:
  scripts/wrt-docker-build.sh
  scripts/wrt-docker-build.sh 'make defconfig'
  scripts/wrt-docker-build.sh 'make -j$(nproc) V=s'
  WRT_IMAGE=my-openwrt-build-image scripts/wrt-docker-build.sh 'make defconfig'
  WRT_CONTAINER=openwrt-build scripts/wrt-docker-build.sh 'make target/linux/compile V=s'

Notes:
  docker run always uses --runtime "${WRT_DOCKER_RUNTIME:-runc}" so Hyper-V
  hosts with a broken NVIDIA default runtime can still run CPU-only builds.
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTES_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_WORKTREE="$(cd "$NOTES_ROOT/.." && pwd)/worktrees/openwrt-bpi-r4-pro-8x"

WRT_WORKTREE="${WRT_WORKTREE:-$DEFAULT_WORKTREE}"
WRT_INNER="${WRT_INNER:-/workspaces/openwrt-bpi-r4-pro-8x}"
WRT_DOCKER_RUNTIME="${WRT_DOCKER_RUNTIME:-runc}"
WRT_NOFILE_LIMIT="${WRT_NOFILE_LIMIT:-4096}"
WRT_CONTAINER="${WRT_CONTAINER:-}"
WRT_IMAGE="${WRT_IMAGE:-}"
WRT_USER="${WRT_USER:-}"
WRT_HOME="${WRT_HOME:-/builder}"

if [ -z "$WRT_CONTAINER" ]; then
  WRT_IMAGE="${WRT_IMAGE:-ghcr.io/openwrt/buildbot/buildworker-v3.8.0:v9}"
fi

case "$WRT_NOFILE_LIMIT" in
  ''|*[!0-9]*)
    echo "WRT_NOFILE_LIMIT must be a positive integer" >&2
    exit 2
    ;;
esac

if [ ! -d "$WRT_WORKTREE" ]; then
  echo "OpenWrt worktree not found: $WRT_WORKTREE" >&2
  exit 2
fi

if [ -n "$WRT_CONTAINER" ] && [ -n "$WRT_IMAGE" ]; then
  echo "Set only one of WRT_CONTAINER or WRT_IMAGE" >&2
  exit 2
fi

printf -v WRT_INNER_Q '%q' "$WRT_INNER"
printf -v WRT_HOME_Q '%q' "$WRT_HOME"

if [ "$#" -eq 0 ]; then
  INNER_CMD="cd $WRT_INNER_Q && mkdir -p $WRT_HOME_Q && { ulimit -n $WRT_NOFILE_LIMIT 2>/dev/null || true; } && exec bash"
else
  INNER_CMD="cd $WRT_INNER_Q && mkdir -p $WRT_HOME_Q && { ulimit -n $WRT_NOFILE_LIMIT 2>/dev/null || true; } && $*"
fi

tty_args=()
if [ -t 0 ] && [ -t 1 ]; then
  tty_args=(-it)
else
  tty_args=(-i)
fi

if [ -n "$WRT_CONTAINER" ]; then
  WRT_USER="${WRT_USER:-buildbot}"
  exec docker exec "${tty_args[@]}" \
    -u "$WRT_USER" \
    -e "HOME=$WRT_HOME" \
    "$WRT_CONTAINER" \
    bash -lc "$INNER_CMD"
fi

user_args=()
if [ -n "$WRT_USER" ]; then
  user_args=(--user "$WRT_USER")
fi

exec docker run --rm "${tty_args[@]}" \
  --runtime "$WRT_DOCKER_RUNTIME" \
  --ulimit "nofile=$WRT_NOFILE_LIMIT:$WRT_NOFILE_LIMIT" \
  "${user_args[@]}" \
  -e "HOME=$WRT_HOME" \
  -v "$WRT_WORKTREE:$WRT_INNER" \
  -w "$WRT_INNER" \
  "$WRT_IMAGE" \
  bash -lc "$INNER_CMD"
