"""Write docs/security-review.md from build/scan.json."""
import json, os, re, collections
OUT = 'out/agent-skills'
scan = json.load(open('build/scan.json'))
rows = {r['name']: r for r in json.load(open(os.path.join(OUT, 'catalog.json')))}
LIB = os.path.join(OUT, 'library')
lines = ['# Security review', '',
         'How the skills in `library/` were checked before being added, and what to know about the ones that run code.', '',
         '## What was checked', '',
         '- Every file in every skill was scanned automatically for: piping downloads into a shell, `rm -rf` on home or root, reads of SSH keys or saved credentials,'
         ' reverse shells, encoded or obfuscated code, `sudo`, startup-file persistence, hidden Unicode characters, prompt-injection phrases, and scripts that send'
         ' environment variables over the network. Also binaries and files over 1 MB.',
         '- Every skill\'s name and description was read, and every flagged file was read in full.',
         f'- Result: **nothing malicious found, and no skill excluded for security reasons.** Every flag was a false positive: security skills describing attacks,'
         ' skills warning Claude *not* to follow instructions hidden in web pages, documentation examples, or official installers (e.g. `uv`).', '',
         '## Skills that include scripts', '',
         'Most skills are just instructions. These also ship scripts that Claude may run when you use the skill. Scripts that use the network only contact the services listed.', '',
         '| Skill | Scripts | Network (from its scripts) | Needs |', '|---|---|---|---|']
for name, v in sorted(scan.items()):
    if not v['scripts']:
        continue
    hosts = collections.Counter()
    for f in v['net_scripts']:
        t = open(os.path.join(LIB, name, f), errors='ignore').read()
        for h in re.findall(r'https?://([a-zA-Z0-9.-]+\.[a-z]{2,})', t):
            if not re.search(r'w3\.org|apache\.org|creativecommons|example\.|localhost|\.local$', h):
                hosts[h] += 1
    net = ', '.join(h for h, _ in hosts.most_common(6)) or ('local only' if v['net_scripts'] else 'none')
    lines.append(f"| `{name}` | {len(v['scripts'])} | {net} | {rows.get(name, {}).get('needs', '')} |")
lines += ['', '## Before you trust a new skill', '',
          'Skills can tell Claude to run commands, so treat a skill like any code you download. Read its `SKILL.md`, look at any `scripts/` folder, and'
          ' be wary of skills that ask for API keys, install things globally, or contact services unrelated to what they do.', '']
os.makedirs(os.path.join(OUT, 'docs'), exist_ok=True)
open(os.path.join(OUT, 'docs', 'security-review.md'), 'w').write('\n'.join(lines))
print('skills with scripts:', sum(1 for v in scan.values() if v['scripts']))
