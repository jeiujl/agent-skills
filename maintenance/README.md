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

`reverse-engineer-anything` was also added by hand, from the npm package `rea-agents` (it ships in `package/skills/`). To update it, download the new version's tarball, check its hash against `npm view rea-agents@<version> dist.integrity`, copy `package/skills/reverse-engineer-anything` over `library/`, and change `REA_VERSION` in `install.sh` and `$ReaVersion` in `install.ps1` to the same version, so the skill and the server always match.

## Agents (The Agency)

`agents/` is built from [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) by `build_agents.py`. To refresh it:

```bash
git clone --depth 1 https://github.com/msitarzewski/agency-agents /tmp/agency
python3 -I maintenance/build_agents.py /tmp/agency "$(git -C /tmp/agency rev-parse HEAD)"
```

It reads only the division folders listed in the checkout's `divisions.json`, copies the agent files to `agents/claude/` unchanged, writes Codex `.toml` versions to `agents/codex/` (checking each one parses back to the same text), and rewrites `agents/index.tsv`, which the installers read. Scan the new files (the same rules as `scan.py`) before committing, then update the agent counts in `README.md`, the agents list in `CATALOG.md` and the commit in `NOTICE.md`. Agents removed upstream are removed from people's machines the next time they run the installer.
