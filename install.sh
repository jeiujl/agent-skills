#!/usr/bin/env bash
# Install skills from this library into Claude Code (~/.claude/skills) and
# Codex (~/.agents/skills), and The Agency's agents into ~/.claude/agents and
# ~/.codex/agents. Run ./install.sh --help for options.
#
# Only skills and agents this script installed are ever replaced or removed:
# it keeps a list of them in each folder (.agent-skills-managed), so your own
# skills and agents are left alone.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
INDEX="$ROOT/index.tsv"
CORE="$ROOT/profiles/core.txt"
AGENT_INDEX="$ROOT/agents/index.tsv"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
CODEX_DIR="$HOME/.agents/skills"
CLAUDE_AGENTS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/agents"
CODEX_AGENTS="${CODEX_HOME:-$HOME/.codex}/agents"
MANIFEST=".agent-skills-managed"
# REA (Reverse Engineer Anything) version that --setup-rea runs; it matches
# library/reverse-engineer-anything. Official package: npm rea-agents (github.com/morluto/rea).
REA_VERSION="6.8.0"

TARGET="both"
DRY_RUN=0
RESET=0
LIST=""
DO_LIST=0
LIST_AGENTS=""
DO_LIST_AGENTS=0
PROFILE_GIVEN=0
NO_AGENTS=0
SETUP_REA=0
SETUP_GRAPHIFY=0
WANT=()
DROP=()
AGENT_WANT=()
AGENT_DROP=()

usage() {
  cat <<'EOF'
Usage: ./install.sh [options]

With no options, installs the core skills and all of The Agency's agents into
Claude Code and Codex.

Skills
  --profile core|all     Install a whole profile (default: core), plus all agents
  --add NAMES            Install skills by name or category, comma-separated
                         (e.g. --add gsap-timeline,motion,seo)
  --remove NAMES         Remove skills (names or categories) this script installed
  --list [CATEGORY]      List skills (* = core) and exit

Agents (The Agency, msitarzewski/agency-agents)
  --agents NAMES         Install agents by division or name, comma-separated
                         (e.g. --agents engineering,design or --agents all)
  --no-agents            Don't install agents in this run
  --remove-agents [NAMES]
                         Remove agents this script installed (all if no names)
  --list-agents [DIVISION]
                         List agents and exit

REA (Reverse Engineer Anything)
  --setup-rea            Also run REA's own setup (npx rea-agents@VERSION setup),
                         which registers its MCP server with your agents. Needs
                         Node.js 22.23.4+, 24.22.1+ or 26.12.1+. Never run by default.

Graphify
  --setup-graphify       Also install the graphifyy Python package that the graphify
                         skill uses (via uv, pipx or pip). Needs Python 3.10+.

  --reset                Remove every skill and agent this script installed
  --target claude|codex|both
                         Where to install (default: both)
  --dry-run              Show what would change without changing anything
  -h, --help             Show this help

Skill categories: design motion html frontend backend tokens workflow testing
                  security marketing sales seo ads research learning automation writing agents
Agent divisions:  academic design engineering finance game-development gis healthcare
                  marketing paid-media product project-management research sales
                  security spatial-computing specialized support testing
EOF
}

split() { echo "$1" | tr ',' '\n' | sed '/^$/d'; }
has_value() { [ $# -gt 1 ] && [ "${2#-}" = "$2" ]; }

while [ $# -gt 0 ]; do
  case "$1" in
    --profile) WANT+=("$2"); PROFILE_GIVEN=1; shift 2 ;;
    --add) while read -r n; do WANT+=("$n"); done < <(split "$2"); shift 2 ;;
    --remove) while read -r n; do DROP+=("$n"); done < <(split "$2"); shift 2 ;;
    --agents) while read -r n; do AGENT_WANT+=("$n"); done < <(split "$2"); shift 2 ;;
    --no-agents) NO_AGENTS=1; shift ;;
    --remove-agents)
      if has_value "$@"; then while read -r n; do AGENT_DROP+=("$n"); done < <(split "$2"); shift; else AGENT_DROP+=(all); fi
      shift ;;
    --reset) RESET=1; shift ;;
    --target) TARGET="$2"; shift 2 ;;
    --list) DO_LIST=1; if has_value "$@"; then LIST="$2"; shift; fi; shift ;;
    --list-agents) DO_LIST_AGENTS=1; if has_value "$@"; then LIST_AGENTS="$2"; shift; fi; shift ;;
    --setup-rea) SETUP_REA=1; shift ;;
    --setup-graphify) SETUP_GRAPHIFY=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

case "$TARGET" in
  claude) DIRS=("$CLAUDE_DIR"); AGENT_DIRS=("$CLAUDE_AGENTS") ;;
  codex) DIRS=("$CODEX_DIR"); AGENT_DIRS=("$CODEX_AGENTS") ;;
  both) DIRS=("$CLAUDE_DIR" "$CODEX_DIR"); AGENT_DIRS=("$CLAUDE_AGENTS" "$CODEX_AGENTS") ;;
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

if [ "$DO_LIST_AGENTS" = 1 ]; then
  awk -F'\t' -v d="$LIST_AGENTS" 'NR > 1 && (d == "" || $2 == d) { printf "%-48s %-20s %s\n", $1, $2, $4; n++ }
    END { printf "\n%d agents\n", n }' "$AGENT_INDEX"
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

# Turn divisions and agent names into index rows: id <tab> division <tab> codex name
expand_agents() {
  for token in "$@"; do
    awk -F'\t' -v t="$token" 'NR > 1 && (t == "all" || $1 == t || $2 == t || $3 == t) { found = 1; print $1 "\t" $2 "\t" $3 }
      END { exit !found }' "$AGENT_INDEX" ||
      echo "  ! no agent or division called '$token' (see ./install.sh --list-agents)" >&2
  done | awk '!seen[$0]++'
}

is_managed() { [ -f "$1/$MANIFEST" ] && grep -qxF "$2" "$1/$MANIFEST"; }

mark_managed() {
  is_managed "$1" "$2" || echo "$2" >> "$1/$MANIFEST"
}

unmark() {
  [ -f "$1/$MANIFEST" ] || return 0
  grep -vxF "$2" "$1/$MANIFEST" > "$1/$MANIFEST.tmp" || true
  mv "$1/$MANIFEST.tmp" "$1/$MANIFEST"
}

managed_count() {
  if [ -f "$1/$MANIFEST" ]; then sed '/^$/d' "$1/$MANIFEST" | wc -l | tr -d ' '; else echo 0; fi
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
  # Some skills ship a Windows version of SKILL.md; only install.ps1 uses it
  rm -f "$dir/$name/SKILL.windows.md"
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

# Agents are single files: <id>.md for Claude Code, <codex name>.toml for Codex
agent_file() {
  if [ "$1" = "$CODEX_AGENTS" ]; then echo "$4.toml"; else echo "$2.md"; fi
}

agent_source() {
  if [ "$1" = "$CODEX_AGENTS" ]; then echo "$ROOT/agents/codex/$4.toml"; else echo "$ROOT/agents/claude/$3/$2.md"; fi
}

sync_agents() {
  local dir="$1" added=0 updated=0 removed=0 id div codex file
  if [ "$RESET" = 1 ] || [ ${#AGENT_DROP[@]} -gt 0 ]; then
    local drop_files=""
    if [ "$RESET" = 1 ] || printf '%s\n' "${AGENT_DROP[@]}" | grep -qx all; then
      [ -f "$dir/$MANIFEST" ] && drop_files="$(cat "$dir/$MANIFEST")"
    else
      drop_files="$(expand_agents "${AGENT_DROP[@]}" | while IFS="$(printf '\t')" read -r id div codex; do agent_file "$dir" "$id" "$div" "$codex"; done)"
    fi
    while read -r file; do
      [ -n "$file" ] && is_managed "$dir" "$file" || continue
      if [ "$DRY_RUN" = 0 ]; then rm -f "${dir:?}/$file"; unmark "$dir" "$file"; fi
      removed=$((removed + 1))
    done <<< "$drop_files"
  fi
  if [ ${#AGENT_WANT[@]} -gt 0 ]; then
    [ "$DRY_RUN" = 1 ] || mkdir -p "$dir"
    local wanted
    wanted="$(expand_agents "${AGENT_WANT[@]}")"
    while IFS="$(printf '\t')" read -r id div codex; do
      [ -n "$id" ] || continue
      file="$(agent_file "$dir" "$id" "$div" "$codex")"
      if [ -e "$dir/$file" ] && ! is_managed "$dir" "$file"; then
        echo "  - $file: skipped, you already have your own agent with this name"
        continue
      fi
      if [ -e "$dir/$file" ]; then updated=$((updated + 1)); else added=$((added + 1)); fi
      [ "$DRY_RUN" = 1 ] && continue
      cp "$(agent_source "$dir" "$id" "$div" "$codex")" "$dir/$file"
      mark_managed "$dir" "$file"
    done <<< "$wanted"
    # After a full install, drop agents this script installed that are no longer in the library
    if printf '%s\n' "${AGENT_WANT[@]}" | grep -qx all && [ -f "$dir/$MANIFEST" ]; then
      local current
      current="$(echo "$wanted" | while IFS="$(printf '\t')" read -r id div codex; do agent_file "$dir" "$id" "$div" "$codex"; done)"
      while read -r file; do
        [ -n "$file" ] || continue
        echo "$current" | grep -qxF "$file" && continue
        if [ "$DRY_RUN" = 0 ]; then rm -f "${dir:?}/$file"; unmark "$dir" "$file"; fi
        removed=$((removed + 1))
      done < <(cat "$dir/$MANIFEST")
    fi
  fi
  [ "$added$updated$removed" = 000 ] || echo "  agents: +$added new, $updated refreshed, -$removed removed"
}

DEFAULT_RUN=0
if [ "$RESET" = 0 ] && [ ${#DROP[@]} -eq 0 ] && [ ${#WANT[@]} -eq 0 ] &&
   [ ${#AGENT_WANT[@]} -eq 0 ] && [ ${#AGENT_DROP[@]} -eq 0 ]; then
  DEFAULT_RUN=1; WANT=(core)
fi
if [ "$NO_AGENTS" = 1 ]; then AGENT_WANT=()
elif [ ${#AGENT_WANT[@]} -eq 0 ] && { [ "$DEFAULT_RUN" = 1 ] || [ "$PROFILE_GIVEN" = 1 ]; }; then AGENT_WANT=(all)
fi

[ "$DRY_RUN" = 1 ] && echo "Dry run: nothing will be changed."
[ "$RESET" = 1 ] || [ ${#DROP[@]} -gt 0 ] || [ ${#WANT[@]} -gt 0 ] || DIRS=()
for dir in ${DIRS[@]+"${DIRS[@]}"}; do
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
  echo "  $(managed_count "$dir") skills from this library installed here"
done

if [ "$RESET" = 1 ] || [ ${#AGENT_WANT[@]} -gt 0 ] || [ ${#AGENT_DROP[@]} -gt 0 ]; then
  for dir in "${AGENT_DIRS[@]}"; do
    echo "$dir"
    sync_agents "$dir"
    echo "  $(managed_count "$dir") agents from The Agency installed here"
  done
fi

setup_rea() {
  local cmd=(npx --yes "rea-agents@$REA_VERSION" setup --skill=false)
  echo
  echo "REA setup: ${cmd[*]}"
  echo "  (registers the REA MCP server; the reverse-engineer-anything skill comes from this library)"
  if [ "$DRY_RUN" = 1 ]; then echo "  dry run: not running it"; return 0; fi
  if ! command -v npx >/dev/null || ! command -v node >/dev/null; then
    echo "  ! REA needs Node.js 22.23.4+, 24.22.1+ or 26.12.1+ (https://nodejs.org). Install it, then run ./install.sh --setup-rea again." >&2
    return 1
  fi
  if ! node -e 'const [a,b,c]=process.versions.node.split(".").map(Number);
      const ok=(a===22&&(b>23||(b===23&&c>=4)))||(a===24&&(b>22||(b===22&&c>=1)))||a>26||(a===26&&(b>12||(b===12&&c>=1)));
      process.exit(ok?0:1)'; then
    echo "  ! REA needs Node.js 22.23.4+, 24.22.1+ or 26.12.1+; you have $(node -v). Update Node, then run ./install.sh --setup-rea again." >&2
    return 1
  fi
  "${cmd[@]}"
}

REA_FAILED=0
if [ "$SETUP_REA" = 1 ]; then
  setup_rea || REA_FAILED=1
  rea_skill=0
  for dir in "${DIRS[@]}"; do is_managed "$dir" reverse-engineer-anything && rea_skill=1; done
  [ "$rea_skill" = 1 ] || [ "$DRY_RUN" = 1 ] || echo "  Note: the REA skill isn't installed. Add it with ./install.sh --add reverse-engineer-anything"
fi

setup_graphify() {
  echo
  echo "Graphify setup: installing the graphifyy package (the graphify skill runs it)"
  if [ "$DRY_RUN" = 1 ]; then echo "  dry run: not installing"; return 0; fi
  if command -v uv >/dev/null; then uv tool install --upgrade graphifyy
  elif command -v pipx >/dev/null; then pipx install --force graphifyy
  elif command -v python3 >/dev/null; then python3 -m pip install --user --upgrade graphifyy
  else
    echo "  ! Graphify needs Python 3.10+ (https://www.python.org/downloads/). Install it, then run ./install.sh --setup-graphify again." >&2
    return 1
  fi
}
GRAPHIFY_FAILED=0
if [ "$SETUP_GRAPHIFY" = 1 ]; then setup_graphify || GRAPHIFY_FAILED=1; fi

echo
echo "Done. Restart Claude Code / Codex to pick up the changes."
echo "Every installed skill and agent adds its description to each session, so keep the active set lean."
[ "$REA_FAILED" = 0 ] && [ "$GRAPHIFY_FAILED" = 0 ] || exit 1
