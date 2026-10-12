import json, sys, os, subprocess, collections
sys.stdout.reconfigure(encoding='utf-8')
ids = sys.argv[1:]
def clean(s): return (s or '').replace('\n',' ').replace('\r',' ')
for pid in ids:
    fn = f'cordis/p{pid}.json'
    if not os.path.exists(fn) or os.path.getsize(fn) < 500:
        subprocess.run(['curl','-s','-m','90',f'https://cordis.europa.eu/project/id/{pid}?format=json','-o',fn])
    try:
        d = json.load(open(fn, encoding='utf-8'))
    except Exception as e:
        print('FAIL', pid, e); continue
    print('='*100)
    print(pid, d.get('acronym'), '|', d.get('title'))
    print('dates', d.get('startDate'), '->', d.get('endDate'), '| status', d.get('status'), '| totalCost', d.get('totalCost'), '| EC max', d.get('ecMaxContribution'))
    print('keywords:', d.get('keywords'))
    assoc = d.get('relations',{}).get('associations',[])
    cats = d.get('relations',{}).get('categories',[])
    for c in cats:
        if c.get('attributes',{}).get('classification') in ('projectFundingSchemeCategory',):
            print('FS category:', c.get('code'), c.get('title'))
    types = collections.Counter(a.get('contenttype') for a in assoc)
    print('assoc types:', dict(types))
    for a in assoc:
        ct = a.get('contenttype'); at = a.get('attributes',{})
        if ct in ('call','programme'):
            print('  ', ct, at.get('type'), a.get('code') or a.get('identifier'), '-', a.get('title'))
    orgs = [a for a in assoc if a.get('contenttype')=='organization']
    def order(a):
        try: return int(a.get('attributes',{}).get('order','999'))
        except: return 999
    orgs.sort(key=order)
    for a in orgs:
        at = a['attributes']
        print(f"  ORG {str(at.get('type')):18s} sme={str(at.get('sme')):5s} ec={str(at.get('ecContribution','-')):>14s} tc={str(at.get('totalCost','-')):>14s} term={at.get('terminated')} | {a.get('legalName')} ({a.get('address',{}).get('country')}) url={a.get('address',{}).get('url','')}")
    for a in assoc:
        ct = a.get('contenttype')
        if ct not in ('organization','call','programme','article') and 'PUBLI' not in str(a.get('id','')):
            print('  OTHER', ct, a.get('id'), '|', a.get('title'), '|', clean(a.get('teaser') or a.get('description'))[:1500])
    pubs = [a for a in assoc if 'PUBLI' in str(a.get('id',''))]
    print('  n publications:', len(pubs))
    for p in pubs[:40]:
        print('    PUB:', clean(p.get('title'))[:160])
    arts = [a for a in assoc if a.get('contenttype')=='article']
    for p in arts:
        print('    ARTICLE:', clean(p.get('title'))[:160], p.get('id'))
    print('OBJECTIVE:', clean(d.get('objective'))[:4000])
