# Tools that aren't plain skills

These came up alongside the skills, but they're apps, plugins or background services that run code on your computer. They aren't copied into this repo. Install the ones you want yourself, with the commands below (taken from each project's README). Commands that start with `/plugin` are typed inside Claude Code.

> **Don't double up.** Several projects offer both a plugin and plain skills. If you install the plugin version of superpowers, caveman, ponytail, UI UX Pro Max or impeccable, remove the copy this repo installed (for example `./install.sh --remove caveman`), so Claude doesn't see the same skill twice.

## Agent Reach

[Agent Reach](https://github.com/Panniantong/Agent-Reach) provides read-only platform search and reading. The library contains its instructions and references, not its Python program, browser or channel tools. Add the skill first:

```powershell
.\install.ps1 -Add agent-reach -NoAgents
```

Mac / Linux: `./install.sh --add agent-reach --no-agents`.

Then install the CLI with [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python 3.10+). The following pins the CLI to the same reviewed source commit as the bundled skill (1.6.1):

```text
uv tool install https://github.com/Panniantong/Agent-Reach/archive/c70ae6da5d39bc90e09ad2ae0575ccc89f31e284.zip
agent-reach setup
agent-reach doctor --text
```

**Do not run `pip install agent-reach` or `uv tool install agent-reach`: the PyPI package with that name is a different project.** Use the official GitHub URL above. Upstream's [installation guide](https://github.com/Panniantong/Agent-Reach/blob/c70ae6da5d39bc90e09ad2ae0575ccc89f31e284/docs/install.md) also offers the latest release.

`setup` enables default channels, installs their dependencies and registers the skill with detected agents; it may refresh this library's copy with a generated version. `doctor` reports local readiness; `agent-reach check <channel> --text` tests a channel online. Setup success does not verify every platform.

Add other platforms only when needed with `agent-reach add <channel>`. Some channels install browser tools and can reuse that site's existing browser session; otherwise `agent-reach login <channel>` opens a window for you to sign in. Keys are entered locally through `agent-reach configure <key>`. Sessions and configuration live under `~/.agent-reach/`. The bundled skill forbids posting, commenting, liking and messaging.

Use `agent-reach update` to upgrade the CLI, channel tools and generated skill together. That moves beyond the commit pinned in this library.

## Claude Security (official Anthropic plugin)
Deep vulnerability scanning of your own code inside Claude Code. Each finding is double-checked before it's reported.
```
/plugin install claude-security@claude-plugins-official
```
The same official marketplace also has `security-guidance`, which warns about risky code as Claude writes it.

## OmniRoute: AI gateway ⚠️ read the privacy note first
A local server (`http://localhost:20128/v1`) that sends your AI tools' requests through 375+ providers, many on free tiers, with automatic fallback and prompt compression.
```
npm install -g omniroute
# or with Docker:
docker run -d --name omniroute --restart unless-stopped --stop-timeout 40 \
  -p 127.0.0.1:20128:20128 -v omniroute-data:/app/data diegosouzapw/omniroute:latest
```
**Privacy:** everything you send, including code, client data and files, goes to whichever third-party provider OmniRoute picks, under that provider's terms. Free tiers often use your data for training. **Don't use it for client work** if you've promised clients their data stays private. Using another company's paid subscription through a gateway may also break that company's terms.

## claude-mem: long-term memory for Claude Code
Captures what happens in your sessions, compresses it, and gives it back to Claude in later sessions. It installs hooks and runs a background worker with a local web viewer.
```
npx claude-mem install
```
Note: `npm install -g claude-mem` only installs the library, not the plugin. Your session history is stored on your computer, so treat it like your code.

## Ruflo: agent "meta-harness" for Claude Code and Codex
A large framework for agent teams, swarms and memory. It adds plugins, hooks and an MCP server, and its 300+ skills depend on it, so they aren't in this library.
```
/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo
# or the setup wizard:
npx ruflo@latest init wizard
```
It changes how Claude Code behaves quite a lot. Try it in a test project first.

## browser-use: Python browser agent
A Python library that lets an AI drive a real browser. The `browser-use` and `qa` skills in this library use its command-line tool.
```
uv add browser-use            # in a Python project
uv tool install browser-use   # the CLI the skills use
```
Needs Python and [uv](https://docs.astral.sh/uv/).

## Graphify: knowledge graph of a codebase (saves tokens)
Builds a knowledge graph of a folder (code, docs, PDFs, images, even video transcripts) so Claude and Codex can answer questions about it from the graph instead of re-reading every file. The `graphify` skill in this library's core set runs the `graphifyy` Python package (two y's), which needs Python 3.10+. Install it with the installer:
```
.\install.ps1 -SetupGraphify          # Windows
./install.sh --setup-graphify          # Mac / Linux
```
That uses uv, pipx or pip, whichever you have (uv is best: `uv tool install graphifyy`). Then, in a project, type `/graphify .` once; after that the skill answers architecture and "where is / what calls" questions from `graphify-out/`, and `/graphify . --update` refreshes it after changes. On Windows the installer puts graphify's Windows version of the skill in place automatically.

Don't also run `graphify install`: it writes its own copy of the same skill into your skills folder, and this repo's installer already does that (it would just overwrite it on the next run).

## context-mode: keeps big tool output out of the context window (saves tokens)
An MCP server plus hooks that store large outputs outside the conversation and let Claude search them. Its skills need the server, so they aren't in this library.
```
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
npm install -g context-mode
```

## REA (Reverse Engineer Anything): reverse engineering tools for your agent
An MCP server and CLI that lets Claude Code and Codex inspect apps and binaries on your computer: native programs, Electron/JavaScript apps, .NET, Android APKs, firmware, saved network captures and websites. Analysis runs locally; your agent gets the results. Its skill, `reverse-engineer-anything`, is already in this library's core set.

> ⚠️ **Official sources only.** Install REA only from npm [`rea-agents`](https://www.npmjs.com/package/rea-agents) or [github.com/morluto/rea](https://github.com/morluto/rea). Look-alike "reverse engineer anything" repos exist, some offering Windows zip downloads; don't run those.
>
> **Authorised use only.** Use it on software you own or are allowed to analyse (your own apps, security research, malware analysis, interoperability, CTFs). REA's own terms rule out DRM or licence-check circumvention, game cheats and bypassing access controls.

Needs Node.js **22.23.4+**, **24.22.1+** or **26.12.1+** ([nodejs.org](https://nodejs.org)). Then run, from this repo:
```
.\install.ps1 -SetupRea          # Windows
./install.sh --setup-rea         # Mac / Linux
```
That runs REA's official setup pinned to the reviewed release: `npx --yes rea-agents@6.8.0 setup --skill=false`. Setup lists the agents it can connect (Claude Code, Codex, Cursor and others), shows the exact config changes and asks before writing anything. `--skill=false` is there because this library already installs the matching skill. Restart your agents afterwards and check that REA's tools appear.

Optional analysis engines, used only for the tasks that need them (REA never installs these for you, except Hopper with your approval):
- **Ghidra** (free, needs a Java JDK), **Hopper** or **IDA** for native binaries
- **JADX** and a JDK for Android APKs; a Chrome-family browser for websites
- JavaScript and Electron apps need nothing extra

Check what's missing for a task: `npx rea-agents@6.8.0 doctor --json`. Remove REA's registrations: `npx rea-agents@6.8.0 uninstall` (this leaves the library's skill in place; remove it with `./install.sh --remove reverse-engineer-anything`).

**Updating to a newer REA:** run `npx rea-agents@latest setup` yourself. That also installs REA's newer skill, so remove this library's copy first (`./install.sh --remove reverse-engineer-anything`) so the two don't overwrite each other.

## Free open-source apps that replace paid ones

Nine apps from an Instagram list (@chiefagent.ai, Nov 2026), each checked on GitHub on Nov 9, 2026 (the commit is the one checked). They are full apps, not skills, so nothing is copied here. "Free" means no subscription for the software: you still host it yourself or bring your own API keys. Get them **only from the repos below**: several have copycat forks (OpenSEO alone has at least three).

| Replaces | App | Repo (commit) | Licence | How you run it | Worth it for Flowa? |
|---|---|---|---|---|---|
| Calendly | Cal.diy | [calcom/cal.diy](https://github.com/calcom/cal.diy) (`2eb48ec`) | MIT | Self-host (Docker, Node, Postgres). Cal.com's own hosted plan is closed-source now; Cal.diy is its open community edition | **Yes**: a booking link for jerryliu.ca and for client builds. If you don't want to run a server, Cal.com's free hosted plan does the same job |
| Intercom | Chatwoot | [chatwoot/chatwoot](https://github.com/chatwoot/chatwoot) (`fa611d2`) | MIT (except its `enterprise/` folder) | Self-host (Docker) or Chatwoot Cloud | **Yes**: one inbox for chat, email, WhatsApp and Instagram DMs; a good base for client lead follow-up systems |
| Semrush / Ahrefs | OpenSEO | [every-app/open-seo](https://github.com/every-app/open-seo) (`46b815b`) | MIT | Self-host (it can run on Cloudflare); you pay only for the SEO data you use (data-provider API key) | **Yes** for HayesX and local SEO work, instead of a $140+/mo plan |
| Loom | Cap | [CapSoftware/Cap](https://github.com/CapSoftware/Cap) (`5a2823d`) | AGPL-3.0 (a few parts MIT) | Desktop app (Mac, Windows) | Yes: demo videos for prospects |
| Higgsfield | ComfyUI | [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) (`fca60fe`) | GPL-3.0 | Runs on your own computer; needs a strong GPU (NVIDIA best) to be usable | Only with a good graphics card; otherwise keep Higgsfield |
| ElevenLabs | VoiceStudio | [debpalash/voicestudio](https://github.com/debpalash/voicestudio) (`0095a56`) | AGPL-3.0 | Runs on your own computer (a GPU helps) | Later: voiceovers for ad videos. Only clone voices you have permission to use |
| Wispr Flow | OpenWhispr | [OpenWhispr/openwhispr](https://github.com/OpenWhispr/openwhispr) (`2e4768a`) | MIT | Desktop app; local models, or cloud models with your own key | Optional: dictate prompts and emails |
| Notion | AppFlowy | [AppFlowy-IO/AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) (`8fcee27`) | AGPL-3.0 | Desktop and mobile apps; optional self-hosted sync | Skip for now |
| Asana | OpenProject | [opf/openproject](https://github.com/opf/openproject) (`384689f`) | GPL-3.0 | Self-host (Docker) | Skip for now |

**Before you build client work on one of these:**
- **AGPL apps** (Cap, VoiceStudio, AppFlowy): if you change the code and run it as a service for a client, you must share your changed source. Using them unmodified, or for yourself, is fine.
- **Self-hosting is a job:** updates, backups and security are on you, or on your client's monthly fee if you run it for them. Price that in.
- Check each repo's README for its current install steps; these change often.

## Plugin versions of skills in this library
Use one of these *instead of* the copies in `library/` if you'd like automatic updates from the authors:
```
/plugin install superpowers@claude-plugins-official

/plugin marketplace add JuliusBrussee/caveman
/plugin install caveman@caveman

/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail

/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

npx impeccable install      # in a terminal, not inside Claude Code
```

The 11 Closer sales skills (`sales` category) also come as a plugin. If you use it, remove this repo's copies first (`./install.sh --remove sales`), because the plugin's skills are named `/closer-skill:prospector` and so on, and Claude would see both:
```
/plugin marketplace add Jakeschincariol/closer-skill
/plugin install closer-skill@closer-skill
```

## The `skills` command
[skills.sh](https://skills.sh) has a command that installs single skills from GitHub into Claude Code, Codex and other agents. For example, the one you mentioned:
```
npx skills add mattpocock/skills --skill chief-of-staff
```
(`chief-of-staff` is already in this library's core set.)
