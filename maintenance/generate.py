"""Write the catalog, index, licences and notices for out/agent-skills from the
build results (build/selection.json, build/remote.json, build/scan.json)."""
import json, os, re, shutil, yaml

OUT = 'out/agent-skills'
LIB = os.path.join(OUT, 'library')
sel = json.load(open('build/selection.json'))
remote = json.load(open('build/remote.json'))
scan = json.load(open('build/scan.json'))

REPO_URL = {r['repo']: None for r in sel}
SLUG = {}
for d in os.listdir('src'):
    try:
        url = os.popen(f'git -C src/{d} remote get-url origin').read().strip()
        SLUG[d] = url.replace('https://github.com/', '').removesuffix('.git')
    except Exception:
        pass

CATEGORIES = [
    ('design', 'Design & UI/UX'),
    ('motion', 'Animation & motion'),
    ('html', 'Design templates (HTML pages, decks, posters)'),
    ('frontend', 'Frontend & web dev'),
    ('backend', 'Backend & data'),
    ('tokens', 'Token & context savers'),
    ('workflow', 'Workflow & planning'),
    ('testing', 'Testing, debugging & code review'),
    ('security', 'Security'),
    ('marketing', 'Marketing & growth'),
    ('seo', 'SEO'),
    ('ads', 'Paid ads'),
    ('research', 'Research'),
    ('automation', 'Automation & browser agents'),
    ('writing', 'Writing, docs & decks'),
    ('agents', 'Skills, agents & Claude tooling'),
]
CAT_NAME = dict(CATEGORIES)

LABEL_CAT = {
    'superpowers': 'workflow', 'mattpocock': 'workflow', 'marketingskills': 'marketing', 'uupm': 'design',
    'emil': 'design', 'impeccable': 'design', 'taste': 'design', 'antislop': 'design', 'uizze': 'design',
    'stitch': 'design', 'hallmark': 'design', 'designed-by-ai': 'design', 'diagram-design': 'design',
    'anatomy': 'design', 'html': 'html', 'ponytail': 'tokens', 'caveman': 'tokens', 'graphify': 'tokens',
    'last30days': 'research', 'best-skills': 'research', 'vercel': 'agents', 'addyosmani': 'workflow',
    'gsap': 'motion', 'frontend-slides': 'writing', 'planning-with-files': 'workflow', 'claude-seo': 'seo',
    'claude-ads': 'ads', 'iannuttall': 'seo', 'n8n': 'automation', 'trailofbits': 'security',
    'cloudflare': 'security', 'agent-browser': 'automation', 'browser-use': 'automation', 'supabase': 'backend',
    'prisma': 'backend', 'flowkit': 'marketing', 'ecc': 'workflow', 'anthropic': 'agents',
    'vercel-labs': 'frontend', 'remotion-dev': 'motion', 'multica-ai': 'workflow',
}
# Checked in order; the first match wins (name-based, so it applies across sources)
KEYWORDS = [
    (r'^(seo|.*-seo$|.*seo-|programmatic-seo|schema|site-architecture|link-building|directory-submissions|aso)', 'seo'),
    (r'^(ads?$|ads-|ad-|claude-ads)', 'ads'),
    (r'animat|^motion|gsap|remotion|video', 'motion'),
    (r'security|secure|semgrep|codeql|sharp-edges|supply-chain|sarif|variant-analysis|entry-point|audit-context|audit-prep|agentic-actions', 'security'),
    (r'test|tdd|e2e|^qa$|verification|debug|diagnos|review|reproduce|validate-bug|coverage|mutation|patching|second-opinion|break-ui|dogfood', 'testing'),
    (r'token|context|compact|prompt-caching|cost-aware|iterative-retrieval|search-first|regex-vs-llm|caveman|ponytail|cave', 'tokens'),
    (r'react|vue|vite|nextjs|frontend-(patterns|a11y|ui)|accessibility|web-artifacts|webapp|performance|shadcn|swift|mobile-native|expo|composition', 'frontend'),
    (r'postgres|prisma|supabase|database|backend|api-|docker|deploy|devcontainer|ci-cd|observability|migration', 'backend'),
    (r'design|taste|ui|liquid-glass|make-interfaces|brand|canvas|theme|algorithmic-art|gif|apple|prototype|image-to', 'design'),
    (r'research|last30days|documentation-lookup|best-skills|customer-research|competitor', 'research'),
    (r'market|crosspost|social|content|lead|investor|competitive|launch|pricing|offers|referral|churn|email|sms|cold-|prospect|revops|sales|onboarding|signup|paywall|popup|cro$|ab-testing|analytics|attribution|conversion|events|influencer|community|public-relations|free-tools|co-marketing|product-marketing|reddit', 'marketing'),
    (r'writ|article|slides|deck|comms|doc|copy|handoff|academy', 'writing'),
    (r'skill|mcp|claude-api|agent|subagent|wizard', 'agents'),
    (r'n8n|browser|automation', 'automation'),
]


OVERRIDE = {
    'vercel-cli-with-tokens': 'backend', 'deploy-to-vercel': 'backend', 'academy-guide': 'agents', 'codebase-design': 'workflow',
    'guidelines-advisor': 'security', 'karpathy-guidelines': 'workflow', 'lean-build': 'tokens', 'mcp-builder': 'agents',
    'writing-guidelines': 'writing', 'antislop-code': 'testing', 'ab-testing': 'marketing',
    'dispatching-parallel-agents': 'agents', 'pdf': 'writing', 'pptx': 'writing', 'xlsx': 'writing',
    'python-patterns': 'backend', 'prompt-optimizer': 'agents', 'brand-voice': 'writing', 'antislop-human': 'writing',
}


def category(name, label):
    if name in OVERRIDE:
        return OVERRIDE[name]
    if label == 'html':
        return 'html'
    if label in ('n8n', 'agent-browser', 'browser-use'):
        return 'automation'
    for pat, cat in KEYWORDS:
        if re.search(pat, name):
            return cat
    return LABEL_CAT.get(label, 'workflow')


# What a skill needs beyond the skill itself (from reading them)
NEEDS = {
    'graphify': 'pip install graphifyy && graphify install',
    'agent-browser': 'npm i -g agent-browser',
    'dogfood': 'agent-browser CLI',
    'browser-use': 'browser-use CLI (uv tool install browser-use)',
    'qa': 'uv + browser-use (it offers to install uv)',
    'caveman-compress': 'Claude Code CLI or ANTHROPIC_API_KEY',
    'last30days': 'Python 3; optional keys for more sources',
    'design-mobile-apps': 'SLEEK_API_KEY (sleek.design)',
    'hallmark': 'optional TOGETHER_API_KEY for images',
    'taste-application': 'optional FAL_KEY for images',
    'uupm-design': 'optional GEMINI_API_KEY for logos',
    'iannuttall-seo': 'Search Console MCP server',
    'context-budget': '',
    # Key names that only appear in examples, not things the skill needs
    'backend-patterns': '', 'ci-cd-and-automation': '', 'claude-api': '', 'deployment-patterns': '', 'devcontainer-setup': '',
    'docker-patterns': '', 'n8n-expression-syntax': '', 'security-review': '', 'repo-scan': '', 'n8n-self-hosting': '',
    # Optional integrations
    'ads-setup': 'optional ad-platform API tokens', 'claude-ads-ads': 'optional ad-platform API tokens',
    'caveman-setup': 'optional provider API key', 'supabase': 'Supabase CLI / SUPABASE_ACCESS_TOKEN',
    'lead-intelligence': 'APOLLO_API_KEY, EXA_API_KEY', 'video-editing': 'optional ELEVENLABS_API_KEY',
    'prisma-compute': 'Prisma Data Platform account',
}
for n in ['n8n-agents', 'n8n-mcp-tools-expert', 'n8n-node-configuration', 'n8n-subworkflows', 'n8n-validation-expert', 'using-n8n-mcp-skills']:
    NEEDS[n] = 'n8n-mcp server (N8N_API_KEY)'
for n in ['stitch-code-to-design', 'stitch-extract-design-md', 'stitch-extract-static-html', 'stitch-generate-design',
          'stitch-manage-design-system', 'stitch-react-components', 'stitch-react-native', 'stitch-upload-to-stitch', 'stitch-loop']:
    NEEDS[n] = 'Google Stitch MCP server'
for n in ['uizze-ui', 'ui-design', 'ui-radar', 'anti-ui-slop']:
    NEEDS[n] = 'uizze.com account'
KEY_RE = re.compile(r'\b([A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+)*_(?:API_KEY|TOKEN|SECRET|KEY))\b')

CORE = '''ui-ux-pro-max impeccable design-taste-frontend frontend-design emil-design-eng make-interfaces-feel-better
antislop-ui web-design-guidelines improve-animations animation-performance gsap-core gsap-scrolltrigger
ponytail caveman context-budget strategic-compact token-budget-advisor graphify
brainstorming writing-plans executing-plans systematic-debugging test-driven-development verification-before-completion
requesting-code-review chief-of-staff grill-me karpathy-guidelines planning-with-files
skill-creator find-skills last30days deep-research
marketing-psychology copywriting cro seo-audit ai-seo pricing
n8n-workflow-patterns agent-browser security-review'''.split()


def short(desc):
    d = re.sub(r'\s+', ' ', (desc or '').strip().strip('>|').strip())
    m = re.match(r'(.{30,180}?[.!?])(\s|$)', d)
    return (m.group(1) if m else d[:180]).replace('|', '/')


def fix_long_descriptions():
    """The skill format allows descriptions up to 1024 characters; trim longer
    ones at the last full sentence that fits."""
    fixed = []
    for name in os.listdir(LIB):
        p = os.path.join(LIB, name, 'SKILL.md')
        t = open(p, encoding='utf-8').read()
        m = re.match(r'^(﻿?---\s*\n)(.*?)(\n---\s*\n)', t, re.S)
        fm = yaml.safe_load(m.group(2))
        d = fm.get('description', '')
        if isinstance(d, str) and len(d) > 1024:
            cut = d[:1024]
            fm['description'] = cut[:cut.rfind('. ') + 1] if '. ' in cut else cut
            t = m.group(1) + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=10_000).rstrip('\n') + m.group(3) + t[m.end():]
            open(p, 'w', encoding='utf-8').write(t)
            fixed.append(name)
    return fixed


def main():
    fixed = fix_long_descriptions()
    rows = []
    for r in sel:
        text = open(os.path.join(LIB, r['name'], 'SKILL.md'), encoding='utf-8').read()
        needs = NEEDS.get(r['name'])
        if needs is None:
            keys = sorted(set(KEY_RE.findall(text)) - {'ANTHROPIC_API_KEY'})
            needs = ', '.join(keys[:3])
        s = scan.get(r['name'], {})
        rows.append(dict(name=r['name'], kind='library', category=category(r['name'], r['label']), source=SLUG[r['repo']],
                         license=r['license'], commit=r['commit'], path=r['path'], original=r['original'],
                         desc=short(r['desc']), needs=needs, scripts=bool(s.get('scripts')), core=r['name'] in CORE))
    for r in remote:
        label = r['repo'].split('/')[0]
        rows.append(dict(name=r['name'], kind='remote', category=category(r['name'], label), source=r['repo'],
                         license=r['license'], commit=r['commit'], path=r['path'], original=r['original'],
                         desc=short(r['desc']), needs='git (installed from source)', scripts=False, core=r['name'] in CORE))
    rows.sort(key=lambda x: x['name'])
    missing = [c for c in CORE if c not in {x['name'] for x in rows}]
    assert not missing, missing

    os.makedirs(os.path.join(OUT, 'profiles'), exist_ok=True)
    open(os.path.join(OUT, 'profiles', 'core.txt'), 'w').write(
        '# The core set: installed by default. One skill name per line; edit freely.\n' + '\n'.join(sorted(CORE)) + '\n')
    with open(os.path.join(OUT, 'index.tsv'), 'w', newline='\n') as f:
        f.write('name\tkind\tcategory\trepo\tcommit\tpath\n')
        for x in rows:
            f.write(f"{x['name']}\t{x['kind']}\t{x['category']}\t{x['source']}\t{x['commit']}\t{x['path']}\n")
    json.dump(rows, open(os.path.join(OUT, 'catalog.json'), 'w'), indent=1, ensure_ascii=False)

    # Licences and attribution
    lic_dir = os.path.join(OUT, 'licenses')
    shutil.rmtree(lic_dir, ignore_errors=True); os.makedirs(lic_dir)
    copied = sorted({r['repo'] for r in sel})
    notice = ['# Notices\n', 'The skills in `library/` are copied unchanged from the projects below (apart from the `name:` line,'
              ' which matches each folder name, and descriptions trimmed to the 1,024-character limit where noted). Each project\'s licence is in `licenses/`.\n',
              '| Source | Licence | Skills |', '|---|---|---|']
    for repo in copied:
        slug = SLUG[repo]
        src_lic = next((os.path.join('src', repo, n) for n in os.listdir(os.path.join('src', repo)) if n.upper().startswith(('LICEN', 'COPYING'))), None)
        if repo == 'anthropics_skills':
            src_lic = 'src/anthropics_skills/skills/skill-creator/LICENSE.txt'
        if src_lic:
            shutil.copy(src_lic, os.path.join(lic_dir, slug.replace('/', '__') + '.txt'))
        n = sum(1 for r in sel if r['repo'] == repo)
        lic = next(r['license'] for r in sel if r['repo'] == repo)
        notice.append(f'| [{slug}](https://github.com/{slug}) | {lic} | {n} |')
    notice += ['', 'Skills listed as "installed from source" in the catalog have no licence that allows copying them here, so the'
               ' installer downloads them from their own repository, pinned to the commit that was reviewed.', '']
    if fixed:
        notice.append('Descriptions trimmed to 1,024 characters: ' + ', '.join(fixed) + '.')
    open(os.path.join(OUT, 'NOTICE.md'), 'w').write('\n'.join(notice) + '\n')

    # CATALOG.md
    lines = ['# Catalog', '',
             f"{sum(1 for x in rows if x['kind']=='library')} skills in `library/`, plus {sum(1 for x in rows if x['kind']=='remote')} installed from their source repo."
             f" **{len(CORE)}** are in the core set (★), installed by default.", '',
             'Install any of them by name or by category, e.g. `./install.sh --add gsap-timeline` or `./install.sh --add motion` (Windows: `.\\install.ps1 -Add motion`).', '']
    for slug, title in CATEGORIES:
        items = [x for x in rows if x['category'] == slug]
        if not items:
            continue
        lines += [f'## {title} (`{slug}`, {len(items)})', '', '| Skill | What it does | Source | Needs |', '|---|---|---|---|']
        for x in sorted(items, key=lambda x: (not x['core'], x['name'])):
            star = '★ ' if x['core'] else ''
            src = f"[{x['source']}](https://github.com/{x['source']})" + (' · from source' if x['kind'] == 'remote' else '')
            lines.append(f"| {star}`{x['name']}` | {x['desc']} | {src} | {x['needs']} |")
        lines.append('')
    open(os.path.join(OUT, 'CATALOG.md'), 'w').write('\n'.join(lines))
    from collections import Counter
    print('rows', len(rows), 'core', len(CORE), 'fixed', fixed)
    print(Counter(x['category'] for x in rows).most_common())


main()
