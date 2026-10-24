"""Build library/ from the cloned sources in src/.

Picks one canonical copy of each skill per repo, applies per-repo include
lists, renames clashing or Windows-unsafe names, drops large demo media, and
writes build/selection.json (what was copied, from where, under which licence)
plus build/remote.json (skills without a redistributable licence, installed
from their source at install time, pinned to the reviewed commit).
"""
import json, os, re, shutil, subprocess

SRC = 'src'
OUT = 'out/agent-skills'
LIB = os.path.join(OUT, 'library')
inv = json.load(open('inventory.json'))

# Repo -> (short label, priority for name clashes: lower wins, include rule)
ALL = None
ECC_KEEP = set('''accessibility api-design article-writing backend-patterns brand-discovery brand-voice browser-qa
click-path-audit code-tour codebase-onboarding coding-standards content-engine context-budget contract-first
cost-aware-llm-pipeline crosspost dashboard-builder database-migrations deep-research deployment-patterns design-system
docker-patterns documentation-lookup e2e-testing email-ops error-handling frontend-a11y frontend-design-direction
frontend-patterns git-workflow github-ops iterative-retrieval lead-intelligence liquid-glass-design
make-interfaces-feel-better market-research marketing-campaign motion-advanced motion-foundations motion-patterns
nextjs-turbopack postgres-patterns prisma-patterns product-lens production-audit prompt-caching-strategy
prompt-optimizer python-patterns react-patterns react-performance react-testing regex-vs-llm-structured-text
repo-scan search-first security-review security-scan seo social-publisher strategic-compact taste taste-application
tdd-workflow token-budget-advisor ui-demo verification-loop video-editing vite-patterns vue-patterns
investor-materials competitive-report-structure google-workspace-ops'''.split())
TOB_KEEP = set('''differential-review semgrep semgrep-rule-creator codeql property-based-testing mutation-testing
supply-chain-risk-auditor secure-workflow-guide sharp-edges second-opinion review-pr review-walkthrough pr-improver
modern-python reproduce-bug validate-bug entry-point-analyzer audit-context-building audit-prep-assistant gh-cli
github-triage devcontainer-setup coverage-analysis code-maturity-assessor guidelines-advisor spec-to-code-compliance
patching-bugs variant-analysis diagramming-code code-improver skill-improver agentic-actions-auditor open-sourcing
slicing-code-context sarif-parsing testing-handbook-generator'''.split())
HTML_KEEP = set('''saas-landing pricing-page waitlist-page web-proto-brutalist web-proto-editorial web-proto-soft
prototype-web mobile-app mobile-onboarding mockup-device-3d dashboard live-dashboard data-report deck-pitch
deck-product-launch deck-simple deck-swiss-international deck-magazine-web poster-hero magazine-poster social-carousel
card-twitter social-x-post-card email-marketing blog-post docs-page resume-modern invoice wireframe-sketch
motion-frames frame-liquid-bg-hero competitive-teardown exec-briefing-memo weekly-update info-funnel'''.split())
ANTHROPIC_FREE = set('''academy-guide algorithmic-art brand-guidelines canvas-design discernment-nudge frontend-design
internal-comms mcp-builder skill-creator slack-gif-creator theme-factory web-artifacts-builder webapp-testing claude-api'''.split())

REPOS = {
    # repo dir: (label, priority, keep-set or ALL, licence override)
    'anthropics_skills': ('anthropic', 0, ANTHROPIC_FREE, 'Apache-2.0'),
    'obra_superpowers': ('superpowers', 1, ALL, None),
    'mattpocock_skills': ('mattpocock', 1, ALL, None),
    'coreyhaines31_marketingskills': ('marketingskills', 1, ALL, None),
    'nextlevelbuilder_ui-ux-pro-max-skill': ('uupm', 1, ALL, None),
    'emilkowalski_skills': ('emil', 1, ALL, None),
    'pbakaus_impeccable': ('impeccable', 1, {'impeccable'}, None),
    'leonxlnx_taste-skill': ('taste', 1, ALL, None),
    'dietrichgebert_ponytail': ('ponytail', 1, ALL, None),
    'Graphify-Labs_graphify': ('graphify', 1, ALL, None),
    'mvanhorn_last30days-skill': ('last30days', 1, ALL, None),
    'LinklyAI_best-skills': ('best-skills', 2, ALL, None),
    'vercel-labs_skills': ('vercel', 2, {'find-skills'}, None),
    'addyosmani_agent-skills': ('addyosmani', 2, ALL, None),
    'JuliusBrussee_caveman': ('caveman', 2, ALL, None),
    'greensock_gsap-skills': ('gsap', 2, ALL, None),
    'google-labs-code_stitch-skills': ('stitch', 3, ALL, None),
    'miqdadbadjuber_anti-slop': ('antislop', 3, ALL, None),
    'uizze_uizze': ('uizze', 3, ALL, None),
    'cathrynlavery_diagram-design': ('diagram-design', 3, ALL, None),
    'zarazhangrui_frontend-slides': ('frontend-slides', 3, ALL, None),
    'OthmanAdi_planning-with-files': ('planning-with-files', 3, {'planning-with-files'}, None),
    'AgriciDaniel_claude-seo': ('claude-seo', 3, ALL, None),
    'AgriciDaniel_claude-ads': ('claude-ads', 3, ALL, None),
    'czlonkowski_n8n-skills': ('n8n', 3, ALL, None),
    'nexu-io_html-anything': ('html', 4, HTML_KEEP, None),
    'trailofbits_skills': ('trailofbits', 4, TOB_KEEP, 'CC-BY-SA-4.0'),
    'cloudflare_security-audit-skill': ('cloudflare', 3, ALL, None),
    'vercel-labs_agent-browser': ('agent-browser', 3, {'agent-browser', 'dogfood'}, None),
    'browser-use_browser-use': ('browser-use', 3, {'browser-use', 'qa'}, None),
    'supabase_agent-skills': ('supabase', 3, ALL, None),
    'prisma_skills': ('prisma', 3, ALL, None),
    'iannuttall_seo': ('iannuttall', 4, ALL, None),
    'wheresryan22_anatomy': ('anatomy', 4, ALL, None),
    'Nutlope_hallmark': ('hallmark', 4, ALL, None),
    'designed-by-ai_skills': ('designed-by-ai', 4, ALL, None),
    'flowkit-labs_skills': ('flowkit', 4, ALL, None),
    'affaan-m_ecc': ('ecc', 5, ECC_KEEP, None),
}
# No redistributable licence: installed from source at install time instead.
REMOTE = {
    'vercel-labs_agent-skills': ('vercel-labs/agent-skills', ALL),
    'remotion-dev_skills': ('remotion-dev/skills', ALL),
    'multica-ai_andrej-karpathy-skills': ('multica-ai/andrej-karpathy-skills', ALL),
    'anthropics_skills': ('anthropics/skills', {'docx', 'pdf', 'pptx', 'xlsx', 'doc-coauthoring'}),
}

# Clearer names for generic ones, and names that aren't valid folder names on Windows
RENAME = {
    ('nextlevelbuilder_ui-ux-pro-max-skill', n): 'uupm-' + n
    for n in ['design', 'design-system', 'brand', 'slides', 'banner-design', 'ui-styling']
}
RENAME.update({('nexu-io_html-anything', n): 'html-' + n for n in HTML_KEEP})

SKIP_PATH = re.compile(r'(^|/)(tests?|i18n|examples?|fixtures|integrations|template|docs/[a-z]{2}(-[A-Z]{2})?)(/|$)')
MEDIA = re.compile(r'\.(png|jpe?g|gif|webp|mp3|mp4|mov|webm|wav)$', re.I)
PATH_PRIORITY = ['skills/', '.claude/skills/', 'plugin/skills/', 'plugins/', '.agents/skills/']


def path_rank(rel):
    for i, p in enumerate(PATH_PRIORITY):
        if rel.startswith(p):
            return i
    return len(PATH_PRIORITY)


def canonical(repo):
    best = {}
    for o in inv:
        if o['repo'] != repo or not o['hasfm'] or not o['name']:
            continue
        rel = o['dir'][len(repo) + 1:]
        if SKIP_PATH.search(rel) and not rel.startswith('skills/'):
            continue
        key = o['name']
        if key not in best or (path_rank(rel), len(rel)) < (path_rank(best[key][1]), len(best[key][1])):
            best[key] = (o, rel)
    return best


def safe(name):
    return re.sub(r'[^a-z0-9-]+', '-', name.lower()).strip('-')


def commit(repo):
    return subprocess.check_output(['git', '-C', os.path.join(SRC, repo), 'rev-parse', 'HEAD'], text=True).strip()


def main():
    shutil.rmtree(LIB, ignore_errors=True)
    os.makedirs(LIB)
    chosen = {}  # final name -> record
    order = sorted(REPOS.items(), key=lambda kv: kv[1][1])
    for repo, (label, prio, keep, lic_override) in order:
        for name, (o, rel) in sorted(canonical(repo).items()):
            if keep is not ALL and name not in keep:
                continue
            final = RENAME.get((repo, name), safe(name))
            if final in chosen:
                final = f'{label}-{final}' if not final.startswith(label) else f'{label}-{prio}-{final}'
            if final in chosen:
                print('still clashing, skipped:', repo, name)
                continue
            chosen[final] = dict(name=final, original=name, repo=repo, label=label, path=rel,
                                 license=lic_override or o['license'], commit=commit(repo), desc=o['desc'])
    dropped = []
    for final, rec in chosen.items():
        src = os.path.join(SRC, rec['repo'], rec['path'])
        dst = os.path.join(LIB, final)
        ignore = shutil.ignore_patterns('.git', 'node_modules', '.DS_Store', '__pycache__')
        if os.path.exists(os.path.join(src, '__init__.py')):
            # The skill file lives inside a Python package (graphify): the package
            # is installed with pip, so only the skill file belongs here.
            os.makedirs(dst)
            shutil.copy2(next(os.path.join(src, f) for f in os.listdir(src) if f.lower() == 'skill.md'), os.path.join(dst, 'SKILL.md'))
        elif rec['path'] in ('.', ''):
            # A skill at the root of its repo: copy the skill file, the licence and
            # only the folders the skill file refers to, not the whole repo.
            skill_text = open(os.path.join(src, 'SKILL.md'), errors='ignore').read()
            os.makedirs(dst)
            for entry in os.listdir(src):
                full = os.path.join(src, entry)
                if os.path.isfile(full) and (entry == 'SKILL.md' or entry.upper().startswith('LICEN')):
                    shutil.copy2(full, dst)
                elif os.path.isdir(full) and entry not in ('data', 'docs', 'site', 'tests', 'evals', 'examples', '.github') \
                        and re.search(rf'(^|[\s`(/]){re.escape(entry)}/', skill_text):
                    shutil.copytree(full, os.path.join(dst, entry), ignore=ignore)
        else:
            shutil.copytree(src, dst, symlinks=False, ignore=ignore)
        for root, _, files in os.walk(dst):
            for f in files:
                p = os.path.join(root, f)
                if MEDIA.search(f) and os.path.getsize(p) > 300_000:
                    dropped.append(os.path.relpath(p, LIB)); os.remove(p)
        # The folder name and the frontmatter name must match
        sk = next(os.path.join(dst, f) for f in os.listdir(dst) if f.lower() == 'skill.md')
        if os.path.basename(sk) != 'SKILL.md':
            os.rename(sk, os.path.join(dst, 'SKILL.md')); sk = os.path.join(dst, 'SKILL.md')
        text = open(sk, encoding='utf-8', errors='replace').read()
        text = re.sub(r'^(﻿?---\s*\n(?:.*\n)*?)name:[^\n]*\n', lambda m: m.group(1) + f'name: {final}\n', text, count=1)
        open(sk, 'w', encoding='utf-8').write(text)
    remote = []
    for repo, (slug, keep) in REMOTE.items():
        for name, (o, rel) in sorted(canonical(repo).items()):
            if keep is not ALL and name not in keep:
                continue
            final = safe(name)
            if final in chosen:
                final = f'{slug.split("/")[0]}-{final}'
            remote.append(dict(name=final, original=name, repo=slug, path=rel, commit=commit(repo), desc=o['desc'],
                               license=o['license'] or 'none stated'))
    os.makedirs('build', exist_ok=True)
    json.dump(sorted(chosen.values(), key=lambda r: r['name']), open('build/selection.json', 'w'), indent=1)
    json.dump(remote, open('build/remote.json', 'w'), indent=1)
    json.dump(dropped, open('build/dropped-media.json', 'w'), indent=1)
    print('library:', len(chosen), 'remote:', len(remote), 'media dropped:', len(dropped))


main()
