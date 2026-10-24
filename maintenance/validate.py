import os, re, sys, yaml
LIB = sys.argv[1] if len(sys.argv) > 1 else 'out/agent-skills/library'
bad = []
for name in sorted(os.listdir(LIB)):
    p = os.path.join(LIB, name, 'SKILL.md')
    if not os.path.exists(p):
        bad.append((name, 'no SKILL.md')); continue
    t = open(p, encoding='utf-8').read()
    m = re.match(r'^﻿?---\s*\n(.*?)\n---\s*(\n|$)', t, re.S)
    if not m:
        bad.append((name, 'no frontmatter')); continue
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        bad.append((name, 'yaml: ' + str(e).splitlines()[0])); continue
    if not isinstance(fm, dict):
        bad.append((name, 'frontmatter not a mapping')); continue
    if fm.get('name') != name:
        bad.append((name, f"name {fm.get('name')!r} != folder"))
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name) or len(name) > 64:
        bad.append((name, 'invalid folder name'))
    d = fm.get('description')
    if not isinstance(d, str) or not d.strip():
        bad.append((name, 'missing description'))
    elif len(d) > 1024:
        bad.append((name, f'description {len(d)} chars > 1024'))
print(len(os.listdir(LIB)), 'skills,', len(bad), 'problems')
for b in bad: print(' ', *b)
