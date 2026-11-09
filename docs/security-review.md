# Security review

How the skills in `library/` were checked before being added, and what to know about the ones that run code.

## What was checked

- Every file in every skill was scanned automatically for: piping downloads into a shell, `rm -rf` on home or root, reads of SSH keys or saved credentials, reverse shells, encoded or obfuscated code, `sudo`, startup-file persistence, hidden Unicode characters, prompt-injection phrases, and scripts that send environment variables over the network. Also binaries and files over 1 MB.
- Every skill's name and description was read, and every flagged file was read in full.
- Result: **nothing malicious found, and no skill excluded for security reasons.** Every flag was a false positive: security skills describing attacks, skills warning Claude *not* to follow instructions hidden in web pages, documentation examples, or official installers (e.g. `uv`).

`reverse-engineer-anything` (REA) was taken from the published npm package `rea-agents` 6.8.0, whose download matched npm's recorded sha512 hash, and every file was scanned and read. It is instructions only, with no scripts. The REA tool it works with is not in this repo: it is an MCP server that runs analysis tools (and, with your approval, Ghidra, Hopper or IDA) on files on your computer. The installer only runs its official setup when you pass `--setup-rea` / `-SetupRea`, pinned to version 6.8.0, and that setup asks before changing anything.

The 283 agents in `agents/` (The Agency) were scanned with the same checks. They are Markdown instructions with no scripts or binaries; no names clash. The 21 flagged lines were all false positives: security agents describing attacks they defend against (exfiltration, persistence checks during incident response, detection rules for `Invoke-Expression`), a prompt-engineering agent that tests "ignore previous instructions" attacks, and CI examples using a keychain profile. 17 agents declare a `tools:` list (Read, Write, Edit, WebFetch, WebSearch, and for 7 of them Bash), which limits what those agents may use in Claude Code. The Codex `.toml` files are generated from the same text by `maintenance/build_agents.py`.

The 23 ads worker agents from AgriciDaniel/claude-ads (division `ads`, commit `fc3908e`) were scanned with the same checks: no flags, no hidden characters, no scripts. Each declares its tools: 20 may only read files (Read, Glob, Grep), `research-worker` and `source-verifier` may also search and fetch web pages, and `visual-designer` may also write files. The only change from upstream is the path rewrite noted in NOTICE.md.

`ai-ads-strategist` (zubair-trabzada/ai-ads-claude, commit `d1df3f5`) was scanned with the same checks and its PDF script read in full: it uses only the Python standard library plus reportlab, reads the JSON file you give it and writes one PDF, with no network use. The only flags were the `curl … | bash` install line in upstream's README and installer, neither of which is copied here. Its skills tell Claude to use web search and fetch on the business being analysed and its competitors. Its CPM, CPC, CPA and ROAS figures are industry estimates, so the added note in `SKILL.md` says to label them as estimates for clients.

`library-router` was written for this library. It is instructions only: it reads this repo's `catalog.json`, `index.tsv` and `agents/index.tsv`, then the 1-3 skill or agent files it picks, and never runs the installers without asking. The installers fill in the repo's location in its `SKILL.md` when they copy it.

The 11 Closer sales skills (`sales` category, from Jakeschincariol/closer-skill at commit `0b01076`) were scanned with the same checks (no flags) and every SKILL.md and script was read in full. The scripts use only the Python standard library and write only inside a `closer/` folder in your project (the pipeline file, leads, briefs, proposals, contracts, call notes, calendar `.ics` files), with file names built from cleaned-up contact names. Two of them read the internet: `prospector` fetches one public page per prospect website and `researcher` up to four, each with a 15-second timeout and a user agent that names the project; neither sends anything else. `contract-writer` runs your own Chrome in headless mode to print the contract to PDF. No script sends email: the instructions draft every email, invite and contract and send it through Claude's Gmail and Calendar connectors only after your explicit "yes" for that one message (never "yes to all"), and a scheduled run never sends. `sales-coach` reads live call captions as text and tells you to let everyone on the call know first, since some places require everyone's consent. Their bundled unit tests were not run here.

The four skills added by hand later (`learn`, `humanizer`, `study-guide-builder`, `false-flag-humanizer`) were checked by reading every file in full. Their two scripts use only the Python standard library, make no network calls, and only read the input file and write the output files you name.

## Skills that include scripts

Most skills are just instructions. These also ship scripts that Claude may run when you use the skill. Scripts that use the network only contact the services listed.

| Skill | Scripts | Network (from its scripts) | Needs |
|---|---|---|---|
| `ai-ads-strategist` | 1 | none | reportlab |
| `algorithmic-art` | 1 | none |  |
| `anatomy` | 72 | local only |  |
| `antislop-human` | 2 | none |  |
| `brainstorming` | 4 | primeradiant.com, github.com |  |
| `caveman-compress` | 7 | local only | Claude Code CLI or ANTHROPIC_API_KEY |
| `caveman-explore` | 1 | none |  |
| `caveman-learn` | 2 | none |  |
| `claude-api` | 4 | api.anthropic.com |  |
| `codeql` | 15 | none |  |
| `contract-writer` | 2 | none (runs your local Chrome to make the PDF) | Python 3.8+ |
| `conversion-tracking` | 28 | none |  |
| `design-taste-frontend` | 12 | archive.org, www.artic.edu, collectionapi.metmuseum.org, api.openverse.org, api.artic.edu, images-api.nasa.gov |  |
| `devcontainer-setup` | 2 | none |  |
| `diagnosing-bugs` | 1 | none |  |
| `diagram-design` | 6 | none |  |
| `diagramming-code` | 2 | none |  |
| `false-flag-humanizer` | 1 | none | Python 3 |
| `follow-up` | 2 | none | Python 3.8+ |
| `forecaster` | 2 | none | Python 3.8+ |
| `frontend-design-direction` | 1 | none |  |
| `frontend-slides` | 4 | none |  |
| `git-guardrails-claude-code` | 1 | none |  |
| `github-triage` | 1 | none |  |
| `hallmark` | 10 | upload.wikimedia.org, github.com, api.together.xyz | optional TOGETHER_API_KEY for images |
| `idea-refine` | 1 | none |  |
| `impeccable` | 6 | local only |  |
| `last30days` | 131 | github.com, api.github.com, www.youtube.com, www.reddit.com, x.ai, x.com | Python 3; optional keys for more sources |
| `mcp-builder` | 2 | none |  |
| `n8n-self-hosting` | 1 | none |  |
| `open-sourcing` | 2 | none |  |
| `pipeline` | 3 | none | Python 3.8+ |
| `planning-with-files` | 22 | none |  |
| `proposal-writer` | 2 | none | Python 3.8+ |
| `prospector` | 2 | prospects' public websites (one page per site) | Python 3.8+ |
| `record-keeper` | 2 | none | Python 3.8+ |
| `remotion` | 1 | storage.googleapis.com |  |
| `researcher` | 2 | prospects' public websites (up to 4 pages per site) | Python 3.8+ |
| `review-walkthrough` | 1 | none |  |
| `sales-coach` | 2 | none | Python 3.8+ |
| `sarif-parsing` | 2 | none |  |
| `scheduler` | 2 | none | Python 3.8+ |
| `security-audit` | 4 | none |  |
| `semgrep` | 3 | none |  |
| `setup-ts-deep-modules` | 1 | none |  |
| `shadcn-ui` | 1 | none |  |
| `skill-creator` | 10 | none |  |
| `slack-gif-creator` | 4 | none |  |
| `slicing-code-context` | 2 | none |  |
| `stitch-extract-static-html` | 3 | local only | Google Stitch MCP server |
| `stitch-react-components` | 2 | local only | Google Stitch MCP server |
| `stitch-react-native` | 2 | local only | Google Stitch MCP server |
| `stitch-upload-to-stitch` | 1 | stitch.googleapis.com | Google Stitch MCP server |
| `study-guide-builder` | 1 | none | Python 3 |
| `supply-chain-risk-auditor` | 8 | registry.npmjs.org, api.github.com, api.osv.dev, api.npmjs.org, pypi.org, proxy.golang.org |  |
| `systematic-debugging` | 2 | none |  |
| `taste-application` | 61 | fal.ai | optional FAL_KEY for images |
| `ui-ux-pro-max` | 18 | local only |  |
| `uupm-brand` | 5 | none |  |
| `uupm-design` | 11 | api.atlascloud.ai, api.muapi.ai | optional GEMINI_API_KEY for logos |
| `uupm-design-system` | 10 | none |  |
| `uupm-ui-styling` | 4 | none |  |
| `web-artifacts-builder` | 2 | none |  |
| `webapp-testing` | 4 | none |  |
| `win-back` | 2 | none | Python 3.8+ |
| `wizard` | 1 | none |  |
| `writing-skills` | 1 | none |  |

## Agent Reach addition

The Agent Reach instructions (English entry point and three upstream reference files) were read before inclusion at commit `c70ae6da5d39bc90e09ad2ae0575ccc89f31e284`, with its MIT licence. The added folder contains Markdown only: no executable scripts, binaries, bundled dependencies or credentials. Version and channel-table placeholders were resolved and a first-time setup note was added.

This review covers the bundled instructions, not a full audit or live validation of the separate CLI and its dependencies. Setup and channel additions download and run tools; browser channels may copy a site's existing session into a dedicated browser. Queries can send URLs, search terms and platform requests to external services. Platform login and optional keys remain separate setup steps. The skill restricts use to reading and forbids asking for passwords or printing credentials. See [setup](../tools/SETUP.md#agent-reach).

## Before you trust a new skill

Skills can tell Claude to run commands, so treat a skill like any code you download. Read its `SKILL.md`, look at any `scripts/` folder, and be wary of skills that ask for API keys, install things globally, or contact services unrelated to what they do.
