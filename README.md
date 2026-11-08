# Agent skills

A library of **526 agent skills** and **283 agents** for **Claude Code** and **Codex**. The skills come from 44 open-source projects plus a few added by hand, and focus on design and UI/UX, animation, token savers, and coding workflow, plus marketing, sales, SEO, automation and security. The agents are [The Agency](https://github.com/msitarzewski/agency-agents): specialist personas from frontend developer to brand strategist.

- **499** skills are copied in `library/`. **27** more are downloaded from their own repo when you install them, because their licence doesn't allow copying them here.
- **58** of the best are the **core set** (`profiles/core.txt`), installed by default. The rest wait in the library until you add them.
- **283 agents** in `agents/`, all installed by default (see [Agents](#agents-the-agency)).
- **REA (Reverse Engineer Anything)**: its skill is in the core set, and `-SetupRea` connects the REA tool itself (see [REA](#rea-reverse-engineer-anything)).
- Everything was checked before being added. See [`docs/security-review.md`](docs/security-review.md).

Browse everything in **[CATALOG.md](CATALOG.md)**.

## Install

You need [git](https://git-scm.com/downloads). Clone this repo once, then run the installer.

**Windows (PowerShell):**
```powershell
git clone https://github.com/jeiujl/agent-skills.git
cd agent-skills
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

**Mac / Linux:**
```bash
git clone https://github.com/jeiujl/agent-skills.git
cd agent-skills
./install.sh
```

This installs the core skills and all agents into:
- **Claude Code:** skills in `~/.claude/skills`, agents in `~/.claude/agents` (Windows: `%USERPROFILE%\.claude\...`)
- **Codex:** skills in `~/.agents/skills`, agents in `~/.codex/agents` (Windows: `%USERPROFILE%\.agents\skills`, `%USERPROFILE%\.codex\agents`)

Restart Claude Code or Codex afterwards. Claude and Codex then pick the right skill on their own when a task matches, or you can call one by name, e.g. `/ui-ux-pro-max`.

## Add, remove, list

Use a skill name, a category, or a profile. Commas separate several.

| What | Windows | Mac / Linux |
|---|---|---|
| Add skills or a category | `.\install.ps1 -Add motion,gsap-timeline` | `./install.sh --add motion,gsap-timeline` |
| Remove | `.\install.ps1 -Remove seo` | `./install.sh --remove seo` |
| Install everything | `.\install.ps1 -Profile all` | `./install.sh --profile all` |
| Only Claude Code (or Codex) | `.\install.ps1 -Target claude` | `./install.sh --target claude` |
| List a category (`*` = core) | `.\install.ps1 -List design` | `./install.sh --list design` |
| Preview changes | add `-DryRun` | add `--dry-run` |
| Remove everything it installed | `.\install.ps1 -Reset` | `./install.sh --reset` |
| Skip the agents | `.\install.ps1 -NoAgents` | `./install.sh --no-agents` |

**Categories:** `design` `motion` `html` `frontend` `backend` `tokens` `workflow` `testing` `security` `marketing` `sales` `seo` `ads` `research` `learning` `automation` `writing` `agents`

The installer only ever replaces or removes skills *it* installed (it keeps a list in each skills folder), so your own skills are safe. If you already have a skill with the same name, it's skipped.

## Why only 58 skills are active

Every installed skill's name and description is loaded into every session, so 500 active skills would cost thousands of tokens each time. They'd also make it harder for Claude to pick the right one. Keep the active set to what you use, and add a category when a project needs it, such as `seo` for an SEO job.

## What's in the core set

- **Design & UI/UX:** `ui-ux-pro-max`, `impeccable`, `design-taste-frontend`, `frontend-design`, `emil-design-eng`, `make-interfaces-feel-better`, `antislop-ui`, `web-design-guidelines`
- **Animation:** `improve-animations`, `animation-performance`, `gsap-core`, `gsap-scrolltrigger`
- **Token savers:** `ponytail`, `caveman`, `context-budget`, `strategic-compact`, `token-budget-advisor`, `graphify`
- **Workflow:** `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `requesting-code-review`, `chief-of-staff`, `grill-me`, `karpathy-guidelines`, `planning-with-files`
- **Research & skills:** `last30days`, `deep-research`, `skill-creator`, `find-skills`
- **Marketing:** `marketing-psychology`, `copywriting`, `cro`, `seo-audit`, `ai-seo`, `pricing`
- **Automation & security:** `n8n-workflow-patterns`, `agent-browser`, `security-review`, `reverse-engineer-anything` (REA)
- **Learning & writing:** `learn`, `study-guide-builder`, `humanizer`, `false-flag-humanizer`
- **Sales (Closer):** `prospector`, `researcher`, `follow-up`, `scheduler`, `sales-coach`, `proposal-writer`, `contract-writer`, `pipeline`, `record-keeper`, `win-back`, `forecaster`. Install or remove these 11 together (`-Add sales` / `-Remove sales`): they share one CRM, and the others need `pipeline` next to them.

Edit `profiles/core.txt` to change it. Some skills need an extra tool or API key; see the **Needs** column in the catalog (e.g. `graphify` needs `pip install graphifyy`).

## Update

```bash
git pull
./install.sh            # or .\install.ps1 on Windows: refreshes the skills and agents it installed
```

## Agents (The Agency)

`agents/` holds all 283 agents from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT), in 18 divisions. An agent is a specialist persona (a "Frontend Developer", "Growth Hacker" or "Reality Checker") that Claude Code or Codex can hand a task to. Ask for one by name, e.g. *"Use the Reality Checker agent to verify this is production-ready."*

- **Claude Code** gets the original files in `~/.claude/agents`.
- **Codex** gets the same agents converted to its custom-agent format (`.toml`) in `~/.codex/agents`.

| What | Windows | Mac / Linux |
|---|---|---|
| Install only some divisions | `.\install.ps1 -Agents engineering,design` | `./install.sh --agents engineering,design` |
| Remove a division | `.\install.ps1 -RemoveAgents marketing` | `./install.sh --remove-agents marketing` |
| Remove all agents | `.\install.ps1 -RemoveAgents all` | `./install.sh --remove-agents` |
| List agents (or one division) | `.\install.ps1 -ListAgents engineering` | `./install.sh --list-agents engineering` |

**Divisions:** `academic` `design` `engineering` `finance` `game-development` `gis` `healthcare` `marketing` `paid-media` `product` `project-management` `research` `sales` `security` `spatial-computing` `specialized` `support` `testing`

Like skills, each installed agent's description is loaded into every session. All 283 together are about 63,000 characters (roughly 16,000 tokens) per session. If that's too much, keep only the divisions you use: `-RemoveAgents all` then `-Agents engineering,design,marketing`. Your own agents are never touched; an agent of yours with the same file name is skipped.

## REA (Reverse Engineer Anything)

[REA](https://github.com/morluto/rea) (MIT) lets Claude Code and Codex reverse engineer apps and binaries on your computer: native programs, Electron and JavaScript apps, Android APKs, firmware and websites. It works with Ghidra, Hopper or IDA if you have them.

It has two parts:
1. **The skill** `reverse-engineer-anything` (in the core set, installed by default). It tells the agent how to work with REA.
2. **The REA tool itself**, an MCP server that does the analysis. It needs [Node.js](https://nodejs.org) 22.23.4+ (or 24.22.1+). Connect it with:

   ```powershell
   .\install.ps1 -SetupRea      # Mac / Linux: ./install.sh --setup-rea
   ```

   This runs REA's official setup (`npx rea-agents@6.8.0 setup`), which shows the changes it will make and asks before applying them. The installer never runs it unless you ask. Restart Claude Code / Codex afterwards.

Analysis runs locally. Use it only on software you own or are allowed to analyse. Only install REA from npm `rea-agents` or github.com/morluto/rea: look-alike "reverse engineer anything" repos exist, some offering suspicious downloads. More in [tools/SETUP.md](tools/SETUP.md#rea-reverse-engineer-anything).

## Apps and plugins

OmniRoute, claude-mem, Ruflo, browser-use, context-mode, the Claude Security plugin, and plugin versions of some skills aren't plain skills. They run code on your computer. Install commands and warnings are in **[tools/SETUP.md](tools/SETUP.md)**.

## Claude in the browser or desktop app

These installers are for Claude Code and Codex. To use a skill in regular Claude chats, zip its folder from `library/` and upload it in Claude's settings under Skills.

## Credits

Every skill and agent belongs to its authors; see [NOTICE.md](NOTICE.md) and `licenses/`. `maintenance/` has the scripts used to build this library, if you want to refresh it from the sources.
