#!/usr/bin/env bash
set -euo pipefail

OLD_TREE="${1:?OLD_TREE required}"
NEW_TREE="${2:?NEW_TREE required}"
DIFF_ID="${3:?DIFF_ID required}"
OUT_ROOT="${4:-analysis/diffsets}"
OLD_REF="${5:-}"
NEW_REF="${6:-}"

case "$DIFF_ID" in
  .|..|*/*)
    echo "error: DIFF_ID must be a single directory name, not a path: ${DIFF_ID}" >&2
    exit 1
    ;;
esac

OLD_TREE_ABS="$(realpath "$OLD_TREE")"
NEW_TREE_ABS="$(realpath "$NEW_TREE")"
OUT="${OUT_ROOT}/${DIFF_ID}"
FILES_OUT="${OUT}/files"

RSYNC_EXCLUDES=(
  --exclude='.git/'
  --exclude='feeds/'
  --exclude='dl/'
  --exclude='tmp/'
  --exclude='build_dir/'
  --exclude='staging_dir/'
  --exclude='bin/'
  --exclude='logs/'
  --exclude='ccache/'
  --exclude='node_modules/'
  --exclude='.DS_Store'
  --exclude='*.swp'
  --exclude='*.swo'
  --exclude='*~'
)

yaml_quote() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '"%s"' "$value"
}

get_commit() {
  local tree="$1"
  local ref="${2:-}"
  if git -C "$tree" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if [ -n "$ref" ]; then
      git -C "$tree" rev-parse "${ref}^{commit}"
    else
      git -C "$tree" rev-parse HEAD
    fi
  else
    if [ -n "$ref" ]; then
      echo "error: commit/ref supplied for non-git tree: ${tree}" >&2
      exit 1
    fi
    echo "unknown"
  fi
}

get_dirty_status() {
  local tree="$1"
  if git -C "$tree" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if [ -n "$(git -C "$tree" status --short)" ]; then
      echo "dirty"
    else
      echo "clean"
    fi
  else
    echo "not-a-git-repo"
  fi
}

export_git_ref() {
  local tree="$1"
  local commit="$2"
  local dest="$3"

  mkdir -p "$dest"
  git -C "$tree" archive --format=tar "$commit" | tar -x -C "$dest"
}

OLD_COMMIT="$(get_commit "$OLD_TREE_ABS" "$OLD_REF")"
NEW_COMMIT="$(get_commit "$NEW_TREE_ABS" "$NEW_REF")"
OLD_STATUS="$(get_dirty_status "$OLD_TREE_ABS")"
NEW_STATUS="$(get_dirty_status "$NEW_TREE_ABS")"

rm -rf "$OUT"
mkdir -p "$FILES_OUT"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/openwrt-diffset.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

BASE="${WORK}/base"
mkdir -p "$BASE"

OLD_SOURCE="$OLD_TREE_ABS"
NEW_SOURCE="$NEW_TREE_ABS"
OLD_SOURCE_MODE="working-tree"
NEW_SOURCE_MODE="working-tree"

if [ -n "$OLD_REF" ]; then
  OLD_SOURCE="${WORK}/old-source"
  OLD_SOURCE_MODE="git-archive"
  export_git_ref "$OLD_TREE_ABS" "$OLD_COMMIT" "$OLD_SOURCE"
fi

if [ -n "$NEW_REF" ]; then
  NEW_SOURCE="${WORK}/new-source"
  NEW_SOURCE_MODE="git-archive"
  export_git_ref "$NEW_TREE_ABS" "$NEW_COMMIT" "$NEW_SOURCE"
fi

rsync -a "${RSYNC_EXCLUDES[@]}" "${OLD_SOURCE}/" "$BASE/"

git -C "$BASE" init -q
git -C "$BASE" config user.name "OpenWrt Diffset"
git -C "$BASE" config user.email "openwrt-diffset@example.invalid"
git -C "$BASE" add -A

DIFF_ARGS=(--cached --find-renames HEAD)
git -C "$BASE" commit --allow-empty -q -m "old tree"

rsync -a --checksum --delete "${RSYNC_EXCLUDES[@]}" "${NEW_SOURCE}/" "$BASE/"
git -C "$BASE" add -A

{
  printf "diff_id: "
  yaml_quote "$DIFF_ID"
  printf "\nold_tree: "
  yaml_quote "$OLD_TREE_ABS"
  printf "\nnew_tree: "
  yaml_quote "$NEW_TREE_ABS"
  printf "\nold_commit: "
  yaml_quote "$OLD_COMMIT"
  printf "\nnew_commit: "
  yaml_quote "$NEW_COMMIT"
  printf "\nold_ref: "
  yaml_quote "${OLD_REF:-working-tree}"
  printf "\nnew_ref: "
  yaml_quote "${NEW_REF:-working-tree}"
  printf "\nold_source_mode: "
  yaml_quote "$OLD_SOURCE_MODE"
  printf "\nnew_source_mode: "
  yaml_quote "$NEW_SOURCE_MODE"
  printf "\nold_status: "
  yaml_quote "$OLD_STATUS"
  printf "\nnew_status: "
  yaml_quote "$NEW_STATUS"
  printf "\ncreated_by: "
  yaml_quote "$0"
  printf "\nnotes: "
  yaml_quote "excludes generated build artifacts and external feed checkouts"
  printf "\n"
} > "${OUT}/manifest.yaml"

git -C "$BASE" diff "${DIFF_ARGS[@]}" --name-status > "${OUT}/name-status.tsv"
git -C "$BASE" diff "${DIFF_ARGS[@]}" --numstat > "${OUT}/numstat.tsv"
git -C "$BASE" diff "${DIFF_ARGS[@]}" --stat > "${OUT}/stat.txt"
git -C "$BASE" diff "${DIFF_ARGS[@]}" --binary > "${OUT}/full.patch"

: > "${OUT}/binary-files.txt"

while IFS=$'\t' read -r status path1 path2; do
  [ -n "${status:-}" ] || continue

  case "$status" in
    A|M|D)
      file_path="$path1"
      ;;
    R*|C*)
      file_path="${path2:-$path1}"
      ;;
    *)
      continue
      ;;
  esac

  [ -n "$file_path" ] || continue

  out_file="${FILES_OUT}/${file_path}.patch"
  mkdir -p "$(dirname "$out_file")"

  git -C "$BASE" diff "${DIFF_ARGS[@]}" --binary -- "$file_path" > "$out_file"

  if grep -q '^Binary files ' "$out_file" || grep -q '^GIT binary patch' "$out_file"; then
    echo "$file_path" >> "${OUT}/binary-files.txt"
  fi
done < "${OUT}/name-status.tsv"

echo "Created diff set: ${OUT}"
