#!/usr/bin/env bash
# scripts/lint-finding1.sh — the fleet-wide Finding-1 lint.
#
# Finding 1 (REVIEW-L01 §1): the display year counts bitcoin's block-years — it is not
# "how old bitcoin is," not "bitcoin's age," and the 364-vs-365.24 solar drift is not a
# single flattened "~1.24 days" number (it has a separate, non-constant measured part on
# top of the designed one). This lint fails a line naming the single-part drift figure —
# "~1.24 days", "1.24 d/yr", or the "1¼ days" fraction-notation disguise (with or without
# a leading "~") — or either age-doctrine phrasing ("bitcoin's age", "how old bitcoin is"
# / "how old is bitcoin"), UNLESS that same line also carries a correction tag (a
# "was false" / "corrected" / "retired" / "Finding 1" / "RULED" / "historical" /
# "superseded" frame) — a line that quotes the old claim while retracting it is legal by
# construction — or the file/line is allowlisted (for generated or pending files that
# can't carry a tag yet).
#
# Usage:
#   scripts/lint-finding1.sh <path>      # a file, or a directory tree to scan
#
# Scans .py / .md / .html / .ts / .tsx / .js files, skipping .git, __pycache__, build/,
# *.egg-info, node_modules.
#
# Allowlist: <this script's directory>/finding1-allowlist.txt — same format as
# scripts/one-moon-allowlist.txt (bare path / path:LINENO / path/** prefix).
#
# Exit 0 = clean. Exit 1 = one or more hits, printed as file:line:content. Exit 2 = usage
# error.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
ALLOWLIST="$SCRIPT_DIR/finding1-allowlist.txt"

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

FALSE_RE='1\.24 days|1\.24 d/yr|~?1¼ days|bitcoin.s age|how old bitcoin is|how old is bitcoin'
TAG_RE='corrected|was false|retired|finding 1|ruled|historical|superseded'

if [ -d "$TARGET" ]; then
  mapfile -d '' -t files < <(find "$ROOT" \
    \( -path '*/.git' -o -name '__pycache__' -o -name 'build' -o -name '*.egg-info' -o -name 'node_modules' \) -prune \
    -o -type f \( -name '*.py' -o -name '*.md' -o -name '*.html' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' \) -print0)
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
    if printf '%s' "$content" | grep -qiE "$TAG_RE"; then
      continue   # correction tag / was-false frame on the same line — legal by construction
    fi
    if ! is_allowlisted "$rel" "$lineno"; then
      printf '%s:%s:%s\n' "$rel" "$lineno" "$content"
      hit=1
    fi
  done < <(grep -nEi "$FALSE_RE" "$file" 2>/dev/null)
done

exit "$hit"
