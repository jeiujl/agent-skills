"""Build agents/ from a checkout of msitarzewski/agency-agents.

    python3 -I maintenance/build_agents.py <agency-agents checkout> <commit>

Writes, replacing what is there:
  agents/claude/<division>/<file>.md   the agent files, copied unchanged
  agents/codex/<slug>.toml             Codex custom agents (name, description,
                                       developer_instructions), the same mapping
                                       as upstream's scripts/convert.sh
  agents/index.tsv                     id, division, codex, name, description
  agents/SOURCE                        repo and commit the files came from

Nothing from the checkout is executed; it is only read.
"""
import json, os, re, shutil, sys, tomllib

SRC, COMMIT = sys.argv[1], sys.argv[2]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'agents')
DIVISIONS = list(json.load(open(os.path.join(SRC, 'divisions.json'), encoding='utf-8'))['divisions'])


def field(text, key):
    """First `key:` in the frontmatter; indented continuation lines fold into one line,
    and one pair of outer quotes is removed (as upstream's get_field does)."""
    lines = text.split('\n')
    fm, value = 0, None
    for line in lines:
        if line == '---':
            fm += 1
            if fm == 2:
                break
            continue
        if fm != 1:
            continue
        if value is None:
            if line.startswith(key + ': '):
                value = line[len(key) + 2:]
        elif re.match(r'^[ \t]+[^ \t]', line):
            value += ' ' + line.lstrip(' \t')
        else:
            break
    if value is None:
        return ''
    value = value.strip(' \t')
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
    elif len(value) >= 2 and value[0] == value[-1] == "'":
        value = value[1:-1].replace("''", "'")
    return value


def body(text):
    """Everything after the frontmatter, without trailing newlines."""
    lines, fm = text.split('\n'), 0
    for i, line in enumerate(lines):
        if line == '---':
            fm += 1
            if fm == 2:
                return '\n'.join(lines[i + 1:]).rstrip('\n')
    return ''


def slugify(name):
    s = re.sub(r'[^a-z0-9]', '-', name.lower())
    return re.sub(r'-+', '-', s).strip('-')


def toml_str(s):
    out = []
    for ch in s:
        o = ord(ch)
        if ch == '\\': out.append('\\\\')
        elif ch == '"': out.append('\\"')
        elif ch == '\n': out.append('\\n')
        elif ch == '\r': out.append('\\r')
        elif ch == '\t': out.append('\\t')
        elif ch == '\f': out.append('\\f')
        elif ch == '\b': out.append('\\b')
        elif o < 0x20 or o == 0x7f: out.append('\\u%04X' % o)
        else: out.append(ch)
    return '"' + ''.join(out) + '"'


def tsv(s):
    return re.sub(r'[\t\r\n]+', ' ', s).strip()


for sub in ('claude', 'codex'):
    shutil.rmtree(os.path.join(OUT, sub), ignore_errors=True)
os.makedirs(os.path.join(OUT, 'codex'))

rows, slugs, ids = [], {}, {}
for div in DIVISIONS:
    for r, _, files in sorted(os.walk(os.path.join(SRC, div))):
        for f in sorted(files):
            path = os.path.join(r, f)
            if not f.endswith('.md') or os.path.islink(path):
                continue
            raw = open(path, 'rb').read()
            text = raw.decode('utf-8')
            if not text.startswith('---\n'):
                continue
            name, desc = field(text, 'name'), field(text, 'description')
            if not name or not desc:
                sys.exit(f'{path}: missing name or description')
            agent_id, slug = f[:-3], slugify(name)
            if agent_id in ids or slug in slugs:
                sys.exit(f'{path}: duplicate id or Codex name ({agent_id} / {slug})')
            ids[agent_id], slugs[slug] = path, path

            dest = os.path.join(OUT, 'claude', div, f)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, 'wb').write(raw)

            toml = (f'name = {toml_str(name)}\n'
                    f'description = {toml_str(desc)}\n'
                    f'developer_instructions = {toml_str(body(text))}\n')
            parsed = tomllib.loads(toml)
            assert parsed == {'name': name, 'description': desc, 'developer_instructions': body(text)}, path
            open(os.path.join(OUT, 'codex', slug + '.toml'), 'w', encoding='utf-8', newline='\n').write(toml)
            rows.append((agent_id, div, slug, tsv(name), tsv(desc)))

with open(os.path.join(OUT, 'index.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('id\tdivision\tcodex\tname\tdescription\n')
    for row in rows:
        fh.write('\t'.join(row) + '\n')
open(os.path.join(OUT, 'SOURCE'), 'w', encoding='utf-8', newline='\n').write(
    f'msitarzewski/agency-agents {COMMIT}\n')
print(f'{len(rows)} agents in {len(DIVISIONS)} divisions')
