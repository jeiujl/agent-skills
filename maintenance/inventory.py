import os, re, json, sys
SRC='src'
def frontmatter(text):
    m=re.match(r'^﻿?---\s*\n(.*?)\n---\s*\n', text, re.S)
    if not m: return None, text
    fm={}
    cur=None
    for line in m.group(1).splitlines():
        mm=re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$', line)
        if mm:
            cur=mm.group(1); fm[cur]=mm.group(2).strip()
        elif cur and line.startswith((' ','\t')):
            fm[cur]=(fm[cur]+' '+line.strip()).strip()
    for k,v in fm.items():
        v=v.strip()
        if v in ('>','|','>-','|-'): v=''
        fm[k]=v.strip('"\'' )
    return fm, text[m.end():]
def lic(repo):
    for n in os.listdir(os.path.join(SRC,repo)):
        if n.upper().startswith(('LICENSE','LICENCE','COPYING')):
            t=open(os.path.join(SRC,repo,n),errors='ignore').read(3000)
            for k,pat in [('MIT','MIT License|Permission is hereby granted'),('Apache-2.0','Apache License'),('CC-BY-4.0','Creative Commons Attribution 4.0|CC BY 4.0'),('BSD','BSD'),('GPL','GNU GENERAL PUBLIC'),('AGPL','AFFERO'),('MPL','Mozilla Public')]:
                if re.search(pat,t): return k
            return 'other:'+n
    return None
out=[]
for repo in sorted(os.listdir(SRC)):
    L=lic(repo)
    for root,dirs,files in os.walk(os.path.join(SRC,repo)):
        dirs[:]=[d for d in dirs if d not in ('.git','node_modules')]
        for f in files:
            if f.lower()=='skill.md':
                p=os.path.join(root,f)
                t=open(p,errors='ignore').read()
                fm,body=frontmatter(t)
                sdir=root
                extra=[]
                for r2,d2,f2 in os.walk(sdir):
                    d2[:]=[d for d in d2 if d not in ('.git','node_modules')]
                    for x in f2:
                        extra.append(os.path.relpath(os.path.join(r2,x),sdir))
                size=sum(os.path.getsize(os.path.join(sdir,x)) for x in extra if os.path.exists(os.path.join(sdir,x)))
                out.append(dict(repo=repo,dir=os.path.relpath(sdir,SRC),name=(fm or {}).get('name',''),desc=(fm or {}).get('description','')[:400],license=L,nfiles=len(extra),size=size,
                    scripts=[x for x in extra if re.search(r'\.(sh|py|js|mjs|cjs|ts|ps1|bat|rb|go)$',x)][:20],bodylen=len(body),hasfm=fm is not None))
json.dump(out,open('inventory.json','w'),indent=0)
import collections
c=collections.Counter(o['repo'] for o in out)
lics={o['repo']:o['license'] for o in out}
for r,n in c.most_common(): print(f"{r:45} {n:5} uniq-names={len(set(o['name'] for o in out if o['repo']==r)):4} lic={lics[r]}")
print('total',len(out))
