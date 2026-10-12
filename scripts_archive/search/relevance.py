import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
out = json.load(open('normalized.json', encoding='utf-8'))
pats = {
 'lidar': r'\bli?dars?\b|\blidar|lidar\b|\bladar|laser radar',
 'fmcw': r'fmcw|frequency[- ]modulated continuous[- ]wave',
 'opa': r'optical phased[- ]array',
 'tof': r'time[- ]of[- ]flight|\btof\b',
 'spad': r'\bspads?\b|single[- ]photon avalanche',
 'ranging': r'(?<!wide-)(?<!wide )(?<!far-)(?<!far )(?<!wide)\branging\b|range[- ]?finder|distance measurement|absolute distance|range measurement',
 '3d': r'3d[- ](sensing|imaging|camera|vision|scanner)|depth[- ](sensing|camera|map|imaging)|point[- ]cloud',
 'steer': r'beam[- ]steering',
 'comb': r'microcomb|frequency comb|dual[- ]comb',
 'auto': r'autonomous (driving|vehicle|car)|automotive|self-driving|adas\b',
}
rows = []
for n in out:
    if n['scheme'] == 'other': continue
    text = ' '.join([n['title'] or '', n['objective'] or '', n['keywords'] or '']).lower()
    hits = {k: len(re.findall(v, text)) for k, v in pats.items()}
    hits = {k: v for k, v in hits.items() if v}
    coord = [o for o in n['orgs'] if o['type'] == 'coordinator']
    c = coord[0] if coord else {}
    rows.append((n['scheme'], n['start'] or '', n['id'], n['acronym'], n['title'], n['ec'], c.get('name'), c.get('sme'), c.get('act'), c.get('country'), len(n['orgs']), hits))
rows.sort()
for r in rows:
    print(' | '.join(str(x) for x in r))
