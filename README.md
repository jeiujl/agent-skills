# Agent skills

A library of **527 agent skills** and **306 agents** for **Claude Code** and **Codex**. The skills come from 44 open-source projects plus a few added by hand, and focus on design and UI/UX, animation, token savers, and coding workflow, plus marketing, sales, SEO, automation and security. The agents are [The Agency](https://github.com/msitarzewski/agency-agents) (specialist personas from frontend developer to brand strategist) plus the ads workers from [claude-ads](https://github.com/AgriciDaniel/claude-ads).

- **500** skills are copied in `library/`. **27** more are downloaded from their own repo when you install them, because their licence doesn't allow copying them here.
- **59** of the best are the **core set** (`profiles/core.txt`), installed by default. The rest wait in the library until you add them.
- **306 agents** in `agents/`. The **23** best are installed by default (`profiles/agents-core.txt`); the rest stay in the repo (see [Agents](#agents)).
- **`library-router`** (a core skill) searches the whole library when a task needs a specialist, and reads only the 1-3 skills or agents that fit. So nothing is ever removed, and you only pay for what a task uses.
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

This installs the core skills and the core agents into:
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

## Why only 59 skills and 23 agents are active

Every installed skill's and agent's name and description is loaded into every session, so all 527 skills and 306 agents would cost tens of thousands of tokens each time. They'd also make it harder for Claude to pick the right one. So only the best are installed, and everything else stays in the repo:

- **`library-router`** finds the right specialist on demand. When a task needs one (a Meta ads audit, programmatic SEO, a niche framework), it searches `catalog.json` and `agents/index.tsv`, then reads only the 1-3 that fit. It tells you which one it used, and suggests installing it if you keep needing it.
- **Add a category** when a project needs it for a while, such as `-Add seo` for an SEO job.

## What's in the core set

- **Design & UI/UX:** `ui-ux-pro-max`, `impeccable`, `design-taste-frontend`, `frontend-design`, `emil-design-eng`, `make-interfaces-feel-better`, `antislop-ui`, `web-design-guidelines`
- **Animation:** `improve-animations`, `animation-performance`, `gsap-core`, `gsap-scrolltrigger`
- **Token savers:** `ponytail`, `caveman`, `context-budget`, `strategic-compact`, `token-budget-advisor`, `graphify`
- **Workflow:** `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `requesting-code-review`, `chief-of-staff`, `grill-me`, `karpathy-guidelines`, `planning-with-files`
- **Research & skills:** `last30days`, `deep-research`, `skill-creator`, `find-skills`
- **Marketing:** `marketing-psychology`, `copywriting`, `cro`, `seo-audit`, `ai-seo`, `pricing`
- **Automation & security:** `n8n-workflow-patterns`, `agent-browser`, `security-review`, `reverse-engineer-anything` (REA)
- **Library:** `library-router` (finds anything else in this library on demand)
- **Learning & writing:** `learn`, `study-guide-builder`, `humanizer`, `false-flag-humanizer`
- **Sales (Closer):** `prospector`, `researcher`, `follow-up`, `scheduler`, `sales-coach`, `proposal-writer`, `contract-writer`, `pipeline`, `record-keeper`, `win-back`, `forecaster`. Install or remove these 11 together (`-Add sales` / `-Remove sales`): they share one CRM, and the others need `pipeline` next to them.

Edit `profiles/core.txt` to change it. Some skills need an extra tool or API key; see the **Needs** column in the catalog (e.g. `graphify` needs its Python package: run `.\install.ps1 -SetupGraphify` or `./install.sh --setup-graphify`).

## Update

```bash
git pull
./install.sh            # or .\install.ps1 on Windows: refreshes the skills and agents it installed
```

A plain run also sets the agents back to the 23 core ones. If you added a division you want to keep, include it each time: `.\install.ps1 -Agents core,ads`.

## Agents

`agents/` holds **306 agents** in 19 divisions:
- **283** from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) (MIT). An agent is a specialist persona (a "Frontend Developer", "Growth Hacker" or "Reality Checker") that Claude Code or Codex can hand a task to. Ask for one by name, e.g. *"Use the Reality Checker agent to verify this is production-ready."*
- **23** ads workers (division `ads`) from [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) (MIT): platform auditors (Meta, Google, TikTok, LinkedIn, Amazon and more), tracking, budget and compliance auditors, and creative workers (strategist, copywriter, visual designer). They work under the `claude-ads-ads` skill, which decides which ones to run.

Where they go:
- **Claude Code** gets the original files in `~/.claude/agents`.
- **Codex** gets the same agents converted to its custom-agent format (`.toml`) in `~/.codex/agents`.

**Only the 23 core agents are installed by default** (★ in the catalog, listed in `profiles/agents-core.txt`): UI and UX design, AI, backend and frontend engineering, code review, multi-agent architecture, rapid prototyping, content, growth, SEO and social, paid social, PPC and tracking, product and project management, sales discovery, outbound, offers and proposals, accessibility and the Reality Checker. Edit that file to change them. The other 283 stay in the repo, and `library-router` reads one when a task needs it.

| What | Windows | Mac / Linux |
|---|---|---|
| Install the core agents (default) | `.\install.ps1` | `./install.sh` |
| Add divisions or agents | `.\install.ps1 -Agents core,ads` | `./install.sh --agents core,ads` |
| Install all 306 | `.\install.ps1 -Agents all` | `./install.sh --agents all` |
| Remove a division | `.\install.ps1 -RemoveAgents marketing` | `./install.sh --remove-agents marketing` |
| Remove all agents | `.\install.ps1 -RemoveAgents all` | `./install.sh --remove-agents` |
| List agents (`*` = core) | `.\install.ps1 -ListAgents ads` | `./install.sh --list-agents ads` |

`core` and `all` make the installed set match exactly, so a plain re-run goes back to the 23 core agents. List a division with `core` (e.g. `-Agents core,ads`) to keep it on top of the core set.

**Divisions:** `academic` `ads` `design` `engineering` `finance` `game-development` `gis` `healthcare` `marketing` `paid-media` `product` `project-management` `research` `sales` `security` `spatial-computing` `specialized` `support` `testing`

Each installed agent's description is loaded into every session. The 23 core agents are about 5,000 characters (roughly 1,300 tokens); all 306 would be about 74,000 characters (roughly 18,000 tokens). Your own agents are never touched; an agent of yours with the same file name is skipped.

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
