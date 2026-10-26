# Agent skills

A library of **514 agent skills** for **Claude Code** and **Codex**, collected from 42 open-source projects plus a few added by hand. It focuses on design and UI/UX, animation, token savers, and coding workflow, plus marketing, SEO, automation and security.

- **487** skills are copied in `library/`. **27** more are downloaded from their own repo when you install them, because their licence doesn't allow copying them here.
- **46** of the best are the **core set** (`profiles/core.txt`), installed by default. The rest wait in the library until you add them.
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

This installs the core set into:
- **Claude Code:** `~/.claude/skills` (Windows: `%USERPROFILE%\.claude\skills`)
- **Codex:** `~/.agents/skills` (Windows: `%USERPROFILE%\.agents\skills`)

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

**Categories:** `design` `motion` `html` `frontend` `backend` `tokens` `workflow` `testing` `security` `marketing` `seo` `ads` `research` `learning` `automation` `writing` `agents`

The installer only ever replaces or removes skills *it* installed (it keeps a list in each skills folder), so your own skills are safe. If you already have a skill with the same name, it's skipped.

## Why only 46 are active

Every installed skill's name and description is loaded into every session, so 500 active skills would cost thousands of tokens each time. They'd also make it harder for Claude to pick the right one. Keep the active set to what you use, and add a category when a project needs it, such as `seo` for an SEO job.

## What's in the core set

- **Design & UI/UX:** `ui-ux-pro-max`, `impeccable`, `design-taste-frontend`, `frontend-design`, `emil-design-eng`, `make-interfaces-feel-better`, `antislop-ui`, `web-design-guidelines`
- **Animation:** `improve-animations`, `animation-performance`, `gsap-core`, `gsap-scrolltrigger`
- **Token savers:** `ponytail`, `caveman`, `context-budget`, `strategic-compact`, `token-budget-advisor`, `graphify`
- **Workflow:** `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `requesting-code-review`, `chief-of-staff`, `grill-me`, `karpathy-guidelines`, `planning-with-files`
- **Research & skills:** `last30days`, `deep-research`, `skill-creator`, `find-skills`
- **Marketing:** `marketing-psychology`, `copywriting`, `cro`, `seo-audit`, `ai-seo`, `pricing`
- **Automation & security:** `n8n-workflow-patterns`, `agent-browser`, `security-review`
- **Learning & writing:** `learn`, `study-guide-builder`, `humanizer`, `false-flag-humanizer`

Edit `profiles/core.txt` to change it. Some skills need an extra tool or API key; see the **Needs** column in the catalog (e.g. `graphify` needs `pip install graphifyy`).

## Update

```bash
git pull
./install.sh            # or .\install.ps1 on Windows: refreshes the skills it installed
```

## Apps and plugins

OmniRoute, claude-mem, Ruflo, browser-use, context-mode, the Claude Security plugin, and plugin versions of some skills aren't plain skills. They run code on your computer. Install commands and warnings are in **[tools/SETUP.md](tools/SETUP.md)**.

## Claude in the browser or desktop app

These installers are for Claude Code and Codex. To use a skill in regular Claude chats, zip its folder from `library/` and upload it in Claude's settings under Skills.

## Credits

Every skill belongs to its authors; see [NOTICE.md](NOTICE.md) and `licenses/`. `maintenance/` has the scripts used to build this library, if you want to refresh it from the sources.
