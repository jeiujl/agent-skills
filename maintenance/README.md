# Rebuilding the library

These scripts built `library/`, the catalog and the security review. To refresh from the latest versions of the sources:

```bash
cd maintenance
./fetch.sh                 # clone or update every source into ./src
python3 inventory.py       # list every SKILL.md in the sources
python3 build.py           # pick canonical copies → ./out/agent-skills/library
python3 scan.py            # security scan → ./build/scan.json
python3 generate.py        # catalog, index, core profile, licences
python3 secdoc.py          # docs/security-review.md
python3 validate.py        # check every skill's frontmatter
```

Then **read the scan results** (`build/scan.json`) and any new or changed scripts before copying `out/agent-skills/*` over the repo. What to include from each source, renames and the core set are set at the top of `build.py` and `generate.py`. Needs Python 3 with PyYAML.

`learn`, `humanizer`, `study-guide-builder` and `false-flag-humanizer` were added to `library/` by hand (not from `sources.txt`), along with their rows in `index.tsv`, `catalog.json`, `CATALOG.md` and `profiles/core.txt`. A rebuild from the sources doesn't know about them, so copy them back over the rebuilt output.

The 11 `sales` skills (`contract-writer`, `follow-up`, `forecaster`, `pipeline`, `proposal-writer`, `prospector`, `record-keeper`, `researcher`, `sales-coach`, `scheduler`, `win-back`) were added by hand from [Jakeschincariol/closer-skill](https://github.com/Jakeschincariol/closer-skill) at commit `0b0107690e202010710a59eb7d0b47d331255e59`, with their rows in `index.tsv`, `catalog.json`, `CATALOG.md` and `profiles/core.txt`. Keep their folder names unchanged: their scripts load `../pipeline/deals.py` by relative path.

`ai-ads-strategist` was added by hand from [zubair-trabzada/ai-ads-claude](https://github.com/zubair-trabzada/ai-ads-claude) at commit `d1df3f544249191cbc600c8301e2b9d5ddd121c8`: upstream `ads/SKILL.md` plus the added frontmatter and layout note is `SKILL.md`, and upstream `skills/`, `agents/` and `scripts/` (with `requirements.txt` moved into `scripts/`) are copied into the folder, with `~/.claude/skills/ads/` rewritten to `~/.claude/skills/ai-ads-strategist/`. Copy it back after a rebuild.

`reverse-engineer-anything` was also added by hand, from the npm package `rea-agents` (it ships in `package/skills/`). To update it, download the new version's tarball, check its hash against `npm view rea-agents@<version> dist.integrity`, copy `package/skills/reverse-engineer-anything` over `library/`, and change `REA_VERSION` in `install.sh` and `$ReaVersion` in `install.ps1` to the same version, so the skill and the server always match.

## Agents

`agents/` is built by `build_agents.py` from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents), plus the ads worker agents of [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) with `--ads`. Always pass `--ads`, or the `ads` division is dropped. To refresh:

```bash
git clone --depth 1 https://github.com/msitarzewski/agency-agents /tmp/agency
git clone --depth 1 https://github.com/AgriciDaniel/claude-ads /tmp/claude-ads
python3 -I maintenance/build_agents.py /tmp/agency "$(git -C /tmp/agency rev-parse HEAD)" \
  --ads /tmp/claude-ads "$(git -C /tmp/claude-ads rev-parse HEAD)"
```

`--ads` copies claude-ads' `agents/*.md` (except `release-verifier.md` and `skill-reviewer.md`, which are for its maintainers) into the `ads` division and rewrites `ads/SKILL.md` and `ads/references/` to `claude-ads-ads/...`, the skill's folder name here. Use the same claude-ads commit as the `claude-ads-*` skills in `index.tsv`.

`profiles/agents-core.txt` lists the agents installed by default; check its ids still exist after a refresh (`./install.sh --list-agents` marks them with `*`). `library/library-router` was written by hand for this library: its `{{AGENT_SKILLS_ROOT}}` placeholder is replaced with the repo's path by the installers.

It reads only the division folders listed in the checkout's `divisions.json`, copies the agent files to `agents/claude/` unchanged, writes Codex `.toml` versions to `agents/codex/` (checking each one parses back to the same text), and rewrites `agents/index.tsv`, which the installers read. Scan the new files (the same rules as `scan.py`) before committing, then update the agent counts in `README.md`, the agents list in `CATALOG.md` and the commit in `NOTICE.md`. Agents removed upstream are removed from people's machines the next time they run the installer.

## Graphify

`library/graphify` is updated by hand from [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify): `graphify/skill.md` becomes `SKILL.md`, `graphify/skill-windows.md` becomes `SKILL.windows.md` (install.ps1 swaps it in on Windows; install.sh deletes it), and `graphify/skills/claude/references/` becomes `references/`. Update the commit in `index.tsv` and `catalog.json` when you refresh it. The skill needs the `graphifyy` package, which `--setup-graphify` / `-SetupGraphify` installs.
