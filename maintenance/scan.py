import os, re, json, collections
LIB = 'out/agent-skills/library'
TEXT = re.compile(r'\.(md|txt|sh|bash|zsh|py|js|mjs|cjs|ts|tsx|jsx|ps1|bat|cmd|rb|go|json|ya?ml|toml|html|css)$', re.I)
SCRIPT = re.compile(r'\.(sh|bash|zsh|py|js|mjs|cjs|ts|ps1|bat|cmd|rb|go)$', re.I)
RULES = {
    'pipe-to-shell': r'(curl|wget|iwr|Invoke-WebRequest)[^\n|]{0,200}\|\s*(sudo\s+)?(ba|z)?sh\b|iex\s*\(|Invoke-Expression',
    'destructive-rm': r'rm\s+-rf?\s+(/|~|\$HOME|\*)(\s|$|")',
    'credential-paths': r'\.ssh/|id_rsa|id_ed25519|\.aws/credentials|\.netrc|keychain|Login Data|cookies\.sqlite|\.git-credentials|/etc/shadow',
    'reverse-shell': r'/dev/tcp/|nc\s+-e\s|bash\s+-i\s+>&|socat\s+exec',
    'obfuscation': r'base64\s+(-d|--decode)[^\n]*\|\s*(ba)?sh|eval\s*\(\s*(atob|Buffer\.from|base64)|exec\s*\(\s*(base64|codecs\.decode|bytes\.fromhex)|fromCharCode\([^)]{80,}',
    'privilege': r'\bsudo\s+(rm|chmod|chown|curl|bash|sh)\b|chmod\s+777',
    'hidden-unicode': '[​-‏‪-‮⁦-⁩﻿\U000e0000-\U000e007f]',
    'prompt-injection': r'(?i)ignore (all )?(previous|prior|above) instructions|do not (tell|inform|show) the user|without (telling|informing) the user|exfiltrat|disregard (the )?(system|user)',
    'persistence': r'crontab\s+-|LaunchAgents|systemctl\s+enable|\.bashrc|\.zshrc|\.profile\b|HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run',
    'env-secrets-send': r'(os\.environ|process\.env)[^\n]{0,120}(requests\.(post|put)|fetch\(|axios\.post|urlopen)',
}
NET = re.compile(r'requests\.(get|post|put)|urllib\.request|urlopen|http\.client|fetch\(|axios|XMLHttpRequest|curl\s|wget\s|Invoke-WebRequest|websocket', re.I)
report = collections.defaultdict(lambda: {'flags': collections.defaultdict(list), 'scripts': [], 'net_scripts': [], 'binaries': [], 'big': []})
for name in sorted(os.listdir(LIB)):
    root = os.path.join(LIB, name)
    for r, _, files in os.walk(root):
        for f in files:
            p = os.path.join(r, f); rel = os.path.relpath(p, root)
            size = os.path.getsize(p)
            if size > 1_000_000: report[name]['big'].append(f'{rel} ({size//1024} KB)')
            if not TEXT.search(f):
                with open(p, 'rb') as fh:
                    head = fh.read(4)
                if head[:4] in (b'\x7fELF', b'MZ\x90\x00') or head[:2] == b'MZ' or f.endswith(('.exe', '.dll', '.so', '.dylib', '.bin')):
                    report[name]['binaries'].append(rel)
                continue
            t = open(p, encoding='utf-8', errors='ignore').read()
            if SCRIPT.search(f):
                report[name]['scripts'].append(rel)
                if NET.search(t): report[name]['net_scripts'].append(rel)
            for rule, pat in RULES.items():
                for m in re.finditer(pat, t):
                    line = t.count('\n', 0, m.start()) + 1
                    snippet = t[max(0, m.start()-60):m.end()+60].replace('\n', ' ')
                    report[name]['flags'][rule].append(f'{rel}:{line}: …{snippet}…')
                    if len(report[name]['flags'][rule]) > 6: break
out = {k: {'flags': dict(v['flags']), 'scripts': v['scripts'], 'net_scripts': v['net_scripts'], 'binaries': v['binaries'], 'big': v['big']} for k, v in report.items()}
json.dump(out, open('build/scan.json', 'w'), indent=1)
tot = collections.Counter()
for k, v in out.items():
    for rule in v['flags']: tot[rule] += 1
print('skills with scripts:', sum(1 for v in out.values() if v['scripts']), '| with network in scripts:', sum(1 for v in out.values() if v['net_scripts']),
      '| binaries:', sum(1 for v in out.values() if v['binaries']))
print('skills flagged per rule:', dict(tot))
