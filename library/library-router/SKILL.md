---
name: library-router
description: "Find and use the best specialist skill or agent from Jerry's agent-skills library (500+ skills, 300+ agents) when a task needs expertise that isn't already installed: a specific ad platform, SEO or AI-search audit, sales asset, design style, niche engineering, research method, and so on. Use before starting specialised work, or when asked for the best skill or agent for something. Reads only the 1-3 that fit, so the rest cost nothing."
---

# Library router

Only a small core set of skills and agents is installed, to keep every session cheap. The full library stays on disk, and this skill picks from it when a task calls for it.

**Library location:** `{{AGENT_SKILLS_ROOT}}`
(If that folder doesn't exist, for example in a cloud session, say so and carry on with what's installed. The library is the private GitHub repo `jeiujl/agent-skills`.)

## When to use it
- The task needs specialist knowledge that no installed skill or agent covers well (check the installed ones first).
- The user asks for "the best skill/agent for X", or names one that isn't installed.
- Skip it for everyday work that installed skills already handle, and for one-line questions.

## How to pick
1. **Search the indexes, not the folders.** They are small and cheap to read:
   - Skills: `{{AGENT_SKILLS_ROOT}}/catalog.json` (fields: `name`, `category`, `desc`, `needs`, `kind`) or `index.tsv`.
   - Agents: `{{AGENT_SKILLS_ROOT}}/agents/index.tsv` (columns: `id`, `division`, `codex`, `name`, `description`).
   - Grep for the task's key words and the category or division (`ads`, `seo`, `design`, `marketing`, `sales`, `engineering`, ...). Don't read whole folders.
2. **Choose 1-3, not more.** Prefer the most specific match. Prefer skills from the official or best-known sources in the catalog (anthropics, vercel-labs, obra, pbakaus, coreyhaines31, AgriciDaniel, trailofbits) when two overlap.
3. **Check `needs`.** If a skill needs an API key, account or tool the user doesn't have, say so before relying on it.

## How to use what you picked
- **A skill:** read `{{AGENT_SKILLS_ROOT}}/library/<name>/SKILL.md` and follow it. Open its `references/` or other files only when the SKILL.md tells you to. Skills of kind `remote` aren't in `library/`; they are installed from their source with the installer (below).
- **An agent:** read `{{AGENT_SKILLS_ROOT}}/agents/claude/<division>/<id>.md`. Either work in that role yourself, or hand the task to a subagent with the agent file's body as its instructions (in Codex the same agent is `agents/codex/<codex>.toml`).
- **The ads stack:** the `ads` division agents (audit-meta, audit-google, creative-strategist, copy-writer...) are workers for the `claude-ads-ads` conductor skill. Read `library/claude-ads-ads/SKILL.md` first and let it decide which workers to use.
- Say in one line which skill or agent you used, so the user learns what's in the library.

## Making one permanent
If the same library skill or agent keeps being useful, suggest installing it (don't run the installer without asking):
- Windows: `.\install.ps1 -Add <skill>` or `.\install.ps1 -Agents <agent-id or division>`
- Mac/Linux: `./install.sh --add <skill>` or `./install.sh --agents <agent-id or division>`
