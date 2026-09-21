#!/usr/bin/env bash
# scripts/lint-one-moon.sh — the fleet-wide one-moon lint.
#
# Ruling (0018.07.02, the Admiral): "we only have one moon. and we can see it outside."
# The 28-day BFT month is a block count and never wears the moon's name. This lint fails
# any line that names "moon" on the same line as "month", "D01", or "new year"
# (case-insensitive) — the shape of the retired "calendar's moon" doctrine — unless the
# file, or that exact line, is allowlisted.
#
# Usage:
#   scripts/lint-one-moon.sh <path>      # a file, or a directory tree to scan
#
# Scans .py / .md / .html files, skipping .git, __pycache__, build/, *.egg-info,
# node_modules.
#
# Allowlist: <this script's directory>/one-moon-allowlist.txt — one entry per line:
#   a bare relative path         whole file exempt
#   a relative path:LINENO       one line exempt
#   a relative path ending /**   whole subtree exempt (glob prefix)
#   blank lines and lines starting with # are ignored
#
# This is a plain co-occurrence grep with no understanding of negation — a line that
# correctly states the ruling ("the month never wears the moon's name") trips the same
# pattern as a line that wrongly asserts the retired doctrine. Sky-true / correction /
# history lines are expected to show up here and belong in the allowlist with a comment
# explaining why; that is a deliberate design choice (see task-359's SUMMARY for the
# judged list), not a bug to code around with negation-detection heuristics.
#
# Exit 0 = clean (no un-allowlisted hits). Exit 1 = one or more hits, printed as
# file:line:content. Exit 2 = usage error.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ALLOWLIST="$SCRIPT_DIR/one-moon-allowlist.txt"

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  echo "usage: $0 <path>" >&2
  exit 2
fi
if [ ! -e "$TARGET" ]; then
  echo "$0: no such path: $TARGET" >&2
  exit 2
fi

if [ -d "$TARGET" ]; then
  ROOT="$(cd "$TARGET" && pwd)"
else
  ROOT="$(cd "$(dirname "$TARGET")" && pwd)"
fi

is_allowlisted() {
  # $1 = relative path, $2 = line number
  local rel="$1" lineno="$2" entry prefix p n
  [ -f "$ALLOWLIST" ] || return 1
  while IFS= read -r entry; do
    case "$entry" in
      ''|'#'*) continue ;;
    esac
    case "$entry" in
      */'**')
        prefix="${entry%/**}"
        case "$rel" in
          "$prefix"/*|"$prefix") return 0 ;;
        esac
        ;;
      *:*)
        p="${entry%:*}"; n="${entry##*:}"
        [ "$rel" = "$p" ] && [ "$lineno" = "$n" ] && return 0
        ;;
      *)
        [ "$rel" = "$entry" ] && return 0
        ;;
    esac
  done < "$ALLOWLIST"
  return 1
}

if [ -d "$TARGET" ]; then
  mapfile -d '' -t files < <(find "$ROOT" \
    \( -path '*/.git' -o -name '__pycache__' -o -name 'build' -o -name '*.egg-info' -o -name 'node_modules' \) -prune \
    -o -type f \( -name '*.py' -o -name '*.md' -o -name '*.html' \) -print0)
else
  files=("$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")")
fi

hit=0
for file in "${files[@]}"; do
  [ -f "$file" ] || continue
  rel="${file#"$ROOT"/}"
  [ "$rel" = "$file" ] && rel="$(basename "$file")"
  while IFS=: read -r lineno content; do
    [ -n "${lineno:-}" ] || continue
    if ! is_allowlisted "$rel" "$lineno"; then
      printf '%s:%s:%s\n' "$rel" "$lineno" "$content"
      hit=1
    fi
  done < <(grep -nE -i 'moon' "$file" 2>/dev/null | grep -iE ':.*(month|d01|new year)')
done

exit "$hit"
