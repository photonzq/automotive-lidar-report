import json, sys, subprocess, urllib.parse, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '../search')
from classify import norm, scheme
names = sys.argv[1:]
res = {}
for nm in names:
    q = f"contenttype='project' AND '{nm}'"
    p = 1; hits = []
    while True:
        fn = f"n_{nm.replace(' ','_')}_p{p}.json"
        if not os.path.exists(fn) or os.path.getsize(fn) < 300:
            subprocess.run(['curl','-s','-m','180','https://cordis.europa.eu/search/en?q='+urllib.parse.quote(q)+f'&format=json&p={p}&num=50','-o',fn])
        try: d = json.load(open(fn, encoding='utf-8'))
        except Exception as e: print('ERR', nm, e); break
        h = d.get('hits',{}).get('hit',[]) if d.get('hits') else []
        if isinstance(h, dict): h=[h]
        hits += h
        tot = int(d['result']['header']['totalHits'])
        if len(hits) >= tot or not h or p > 6: break
        p += 1
    print(f'### {nm}: total {tot}')
    for x in hits:
        pr = x.get('project', x); n = norm(pr); sc = scheme(n)
        mine = [o for o in n['orgs'] if nm.lower().split()[0] in (o['name'] or '').lower()]
        role = '; '.join(f"{o['type']} sme={o['sme']} ec={o['ec']}" for o in mine) or '(name not in org list)'
        coord = [o['name'] for o in n['orgs'] if o['type']=='coordinator']
        print(f"  {n['id']} {n['acronym']} | {sc} | {n['start']}..{n['end']} | EU {n['ec']} | coord {coord} | {role} | {(n['title'] or '')[:90]}")
