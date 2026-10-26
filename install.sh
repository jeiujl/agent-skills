#!/usr/bin/env bash
# Install skills from this library into Claude Code (~/.claude/skills) and
# Codex (~/.agents/skills). Run ./install.sh --help for options.
#
# Only skills this script installed are ever replaced or removed: it keeps a
# list of them in each skills folder (.agent-skills-managed), so your own
# skills are left alone.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
INDEX="$ROOT/index.tsv"
CORE="$ROOT/profiles/core.txt"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
CODEX_DIR="$HOME/.agents/skills"
MANIFEST=".agent-skills-managed"

TARGET="both"
DRY_RUN=0
RESET=0
LIST=""
DO_LIST=0
WANT=()
DROP=()

usage() {
  cat <<'EOF'
Usage: ./install.sh [options]

With no options, installs the core set into Claude Code and Codex.

  --profile core|all     Install a whole profile (default: core)
  --add NAMES            Install skills by name or category, comma-separated
                         (e.g. --add gsap-timeline,motion,seo)
  --remove NAMES         Remove skills (names or categories) this script installed
  --reset                Remove every skill this script installed
  --target claude|codex|both
                         Where to install (default: both)
  --list [CATEGORY]      List skills (* = core) and exit
  --dry-run              Show what would change without changing anything
  -h, --help             Show this help

Categories: design motion html frontend backend tokens workflow testing
            security marketing seo ads research learning automation writing agents
EOF
}

split() { echo "$1" | tr ',' '\n' | sed '/^$/d'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --profile) WANT+=("$2"); shift 2 ;;
    --add) while read -r n; do WANT+=("$n"); done < <(split "$2"); shift 2 ;;
    --remove) while read -r n; do DROP+=("$n"); done < <(split "$2"); shift 2 ;;
    --reset) RESET=1; shift ;;
    --target) TARGET="$2"; shift 2 ;;
    --list) DO_LIST=1; if [ $# -gt 1 ] && [ "${2#-}" = "$2" ]; then LIST="$2"; shift; fi; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

case "$TARGET" in
  claude) DIRS=("$CLAUDE_DIR") ;;
  codex) DIRS=("$CODEX_DIR") ;;
  both) DIRS=("$CLAUDE_DIR" "$CODEX_DIR") ;;
  *) echo "--target must be claude, codex or both" >&2; exit 1 ;;
esac

core_names() { grep -v '^#' "$CORE" | sed '/^$/d'; }
field() { awk -F'\t' -v n="$1" -v c="$2" 'NR > 1 && $1 == n { print $c; exit }' "$INDEX"; }

if [ "$DO_LIST" = 1 ]; then
  core="$(core_names)"
  awk -F'\t' -v cat="$LIST" 'NR > 1 && (cat == "" || $3 == cat) { print $1 "\t" $3 }' "$INDEX" |
    while IFS="$(printf '\t')" read -r name cat; do
      mark=" "; echo "$core" | grep -qx "$name" && mark="*"
      printf '%s %-40s %s\n' "$mark" "$name" "$cat"
    done
  exit 0
fi

# Turn names, categories and profiles into a list of skill names
expand() {
  for token in "$@"; do
    case "$token" in
      core) core_names ;;
      all) awk -F'\t' 'NR > 1 { print $1 }' "$INDEX" ;;
      *)
        if awk -F'\t' -v t="$token" 'NR > 1 && $3 == t { found = 1; print $1 } END { exit !found }' "$INDEX"; then :
        elif [ -n "$(field "$token" 1)" ]; then echo "$token"
        else echo "  ! no skill or category called '$token' (see ./install.sh --list)" >&2
        fi ;;
    esac
  done | awk '!seen[$0]++'
}

is_managed() { [ -f "$1/$MANIFEST" ] && grep -qx "$2" "$1/$MANIFEST"; }

mark_managed() {
  is_managed "$1" "$2" || echo "$2" >> "$1/$MANIFEST"
}

unmark() {
  [ -f "$1/$MANIFEST" ] || return 0
  grep -vx "$2" "$1/$MANIFEST" > "$1/$MANIFEST.tmp" || true
  mv "$1/$MANIFEST.tmp" "$1/$MANIFEST"
}

# Skills without a licence that allows copying them here are downloaded from
# their own repository, pinned to the commit that was reviewed.
fetch_remote() {
  local repo="$1" commit="$2" path="$3"
  local cache="$ROOT/.cache/$(echo "$repo" | tr '/' '_')@$commit"
  if [ ! -d "$cache/$path" ]; then
    command -v git >/dev/null || { echo "  ! git is needed to install $repo skills" >&2; return 1; }
    mkdir -p "$cache"
    if [ ! -d "$cache/.git" ]; then
      git -c gc.auto=0 -C "$cache" init -q
      git -c gc.auto=0 -C "$cache" remote add origin "https://github.com/$repo"
      git -c gc.auto=0 -C "$cache" fetch -q --depth 1 --filter=blob:none origin "$commit"
    fi
    git -c gc.auto=0 -C "$cache" checkout -q FETCH_HEAD -- "$path"
  fi
  echo "$cache/$path"
}

install_one() {
  local dir="$1" name="$2" kind src
  kind="$(field "$name" 2)"
  if [ -e "$dir/$name" ] && ! is_managed "$dir" "$name"; then
    echo "  - $name: skipped, you already have your own skill with this name"
    return
  fi
  if [ "$DRY_RUN" = 1 ]; then echo "  + $name ($kind)"; return; fi
  if [ "$kind" = remote ]; then
    src="$(fetch_remote "$(field "$name" 4)" "$(field "$name" 5)" "$(field "$name" 6)")" || return 0
  else
    src="$ROOT/library/$name"
  fi
  rm -rf "${dir:?}/$name"
  cp -R "$src" "$dir/$name"
  mark_managed "$dir" "$name"
  echo "  + $name"
}

remove_one() {
  local dir="$1" name="$2"
  if ! is_managed "$dir" "$name"; then return; fi
  if [ "$DRY_RUN" = 1 ]; then echo "  - $name"; return; fi
  rm -rf "${dir:?}/$name"
  unmark "$dir" "$name"
  echo "  - $name"
}

if [ "$RESET" = 0 ] && [ ${#DROP[@]} -eq 0 ] && [ ${#WANT[@]} -eq 0 ]; then WANT=(core); fi

for dir in "${DIRS[@]}"; do
  echo "$dir"
  [ "$DRY_RUN" = 1 ] || mkdir -p "$dir"
  if [ "$RESET" = 1 ] && [ -f "$dir/$MANIFEST" ]; then
    while read -r name; do remove_one "$dir" "$name"; done < <(cat "$dir/$MANIFEST")
  fi
  if [ ${#DROP[@]} -gt 0 ]; then
    while read -r name; do remove_one "$dir" "$name"; done < <(expand "${DROP[@]}")
  fi
  if [ ${#WANT[@]} -gt 0 ]; then
    while read -r name; do install_one "$dir" "$name"; done < <(expand "${WANT[@]}")
  fi
  count=0
  [ -f "$dir/$MANIFEST" ] && count="$(sed '/^$/d' "$dir/$MANIFEST" | wc -l | tr -d ' ')"
  echo "  $count skills from this library installed here"
done

echo
echo "Done. Restart Claude Code / Codex to pick up the changes."
echo "Every installed skill adds its description to each session, so keep the active set lean."
