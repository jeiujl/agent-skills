# Tools that aren't plain skills

These came up alongside the skills, but they're apps, plugins or background services that run code on your computer. They aren't copied into this repo. Install the ones you want yourself, with the commands below (taken from each project's README). Commands that start with `/plugin` are typed inside Claude Code.

> **Don't double up.** Several projects offer both a plugin and plain skills. If you install the plugin version of superpowers, caveman, ponytail, UI UX Pro Max or impeccable, remove the copy this repo installed (for example `./install.sh --remove caveman`), so Claude doesn't see the same skill twice.

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
Builds a graph of a folder so Claude can answer questions about it without re-reading every file. The `graphify` skill in this library needs the package:
```
pip install graphifyy && graphify install
```
(The package is temporarily called `graphifyy` with two y's.)

## context-mode: keeps big tool output out of the context window (saves tokens)
An MCP server plus hooks that store large outputs outside the conversation and let Claude search them. Its skills need the server, so they aren't in this library.
```
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
npm install -g context-mode
```

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

## The `skills` command
[skills.sh](https://skills.sh) has a command that installs single skills from GitHub into Claude Code, Codex and other agents. For example, the one you mentioned:
```
npx skills add mattpocock/skills --skill chief-of-staff
```
(`chief-of-staff` is already in this library's core set.)
