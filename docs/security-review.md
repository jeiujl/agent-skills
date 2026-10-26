# Security review

How the skills in `library/` were checked before being added, and what to know about the ones that run code.

## What was checked

- Every file in every skill was scanned automatically for: piping downloads into a shell, `rm -rf` on home or root, reads of SSH keys or saved credentials, reverse shells, encoded or obfuscated code, `sudo`, startup-file persistence, hidden Unicode characters, prompt-injection phrases, and scripts that send environment variables over the network. Also binaries and files over 1 MB.
- Every skill's name and description was read, and every flagged file was read in full.
- Result: **nothing malicious found, and no skill excluded for security reasons.** Every flag was a false positive: security skills describing attacks, skills warning Claude *not* to follow instructions hidden in web pages, documentation examples, or official installers (e.g. `uv`).

The four skills added by hand later (`learn`, `humanizer`, `study-guide-builder`, `false-flag-humanizer`) were checked by reading every file in full. Their two scripts use only the Python standard library, make no network calls, and only read the input file and write the output files you name.

## Skills that include scripts

Most skills are just instructions. These also ship scripts that Claude may run when you use the skill. Scripts that use the network only contact the services listed.

| Skill | Scripts | Network (from its scripts) | Needs |
|---|---|---|---|
| `algorithmic-art` | 1 | none |  |
| `anatomy` | 72 | local only |  |
| `antislop-human` | 2 | none |  |
| `brainstorming` | 4 | primeradiant.com, github.com |  |
| `caveman-compress` | 7 | local only | Claude Code CLI or ANTHROPIC_API_KEY |
| `caveman-explore` | 1 | none |  |
| `caveman-learn` | 2 | none |  |
| `claude-api` | 4 | api.anthropic.com |  |
| `codeql` | 15 | none |  |
| `conversion-tracking` | 28 | none |  |
| `design-taste-frontend` | 12 | archive.org, www.artic.edu, collectionapi.metmuseum.org, api.openverse.org, api.artic.edu, images-api.nasa.gov |  |
| `devcontainer-setup` | 2 | none |  |
| `diagnosing-bugs` | 1 | none |  |
| `diagram-design` | 6 | none |  |
| `diagramming-code` | 2 | none |  |
| `false-flag-humanizer` | 1 | none | Python 3 |
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
| `planning-with-files` | 22 | none |  |
| `remotion` | 1 | storage.googleapis.com |  |
| `review-walkthrough` | 1 | none |  |
| `sarif-parsing` | 2 | none |  |
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
| `wizard` | 1 | none |  |
| `writing-skills` | 1 | none |  |

## Before you trust a new skill

Skills can tell Claude to run commands, so treat a skill like any code you download. Read its `SKILL.md`, look at any `scripts/` folder, and be wary of skills that ask for API keys, install things globally, or contact services unrelated to what they do.
