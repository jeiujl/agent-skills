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
