import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
def aslist(x):
    if x is None: return []
    return x if isinstance(x, list) else [x]
def norm(p):
    r = p.get('relations', {}) or {}
    a = r.get('associations', {}) or {}
    calls = [c.get('identifier') or c.get('title') for c in aslist(a.get('call'))]
    progs = []
    for g in aslist(a.get('programme')):
        progs.append((g.get('@attributes',{}).get('type'), g.get('code'), g.get('title')))
    cats = aslist((r.get('categories') or {}).get('category'))
    fs = [c.get('code') for c in cats if c.get('@attributes',{}).get('classification')=='projectFundingSchemeCategory']
    orgs = []
    for o in aslist(a.get('organization')):
        at = o.get('@attributes', {})
        act = None
        oc = aslist(((o.get('relations') or {}).get('categories') or {}).get('category'))
        for c in oc:
            if c.get('@attributes',{}).get('classification')=='organizationActivityType':
                act = c.get('code')
        orgs.append(dict(name=o.get('legalName'), type=at.get('type'), sme=at.get('sme'), ec=at.get('ecContribution'), act=act, country=(o.get('address') or {}).get('country'), order=at.get('order')))
    return dict(id=p['id'], acronym=p.get('acronym'), title=p.get('title'), start=p.get('startDate'), end=p.get('endDate'),
                ec=p.get('ecMaxContribution'), tc=p.get('totalCost'), status=p.get('status'), calls=calls, progs=progs, fs=fs, orgs=orgs,
                objective=p.get('objective') or '', keywords=p.get('keywords') or '')
def scheme(n):
    s = ' '.join([c or '' for c in n['calls']] + [ (x[1] or '') for x in n['progs']] + n['fs'])
    S = s.upper()
    if 'PATHFINDEROPEN' in S: return 'EIC Pathfinder Open'
    if 'PATHFINDERCHALLENGE' in S: return 'EIC Pathfinder Challenge'
    if 'TRANSITION' in S and 'EIC' in S: return 'EIC Transition'
    if 'ACCELERATOR' in S and 'EIC' in S: return 'EIC Accelerator'
    if 'HORIZON-EIC' in S or 'HORIZON.3.1' in S: return 'EIC other'
    if 'FETOPEN-03' in S or 'FETOPEN-04' in S or 'LAUNCHPAD' in S: return 'FET Innovation Launchpad'
    if 'FETOPEN' in S: return 'FET Open'
    if 'FETPROACT' in S: return 'FET Proactive'
    if 'FETFLAG' in S or 'FETHPC' in S: return 'FET Flagship/HPC'
    if 'SMEINST' in S or 'SME-1' in S or 'SME-2' in S or 'SMEINST' in S:
        if 'SME-1' in S or '-1-' in S: return 'SME Instrument ph1'
        if 'SME-2' in S or '-2-' in S: return 'SME Instrument ph2 / EIC Accel. pilot'
        return 'SME Instrument (?)'
    if 'FTI' in S: return 'Fast Track to Innovation'
    if 'H2020-EU.1.2' in S: return 'FET (other)'
    return 'other'
if __name__ == '__main__':
    allp = json.load(open(sys.argv[1], encoding='utf-8'))
    out = []
    for pid, p in allp.items():
        n = norm(p); n['scheme'] = scheme(n); out.append(n)
    json.dump(out, open('normalized.json','w',encoding='utf-8'))
    from collections import Counter
    print(Counter(n['scheme'] for n in out))
