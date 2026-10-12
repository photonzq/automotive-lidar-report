import json, sys, os, subprocess
sys.stdout.reconfigure(encoding='utf-8')
for pid in sys.argv[1:]:
    fn = f'cordis/p{pid}.json'
    if not os.path.exists(fn) or os.path.getsize(fn) < 500:
        subprocess.run(['curl','-s','-m','90',f'https://cordis.europa.eu/project/id/{pid}?format=json','-o',fn])
    try: d = json.load(open(fn, encoding='utf-8'))
    except Exception as e: print('FAIL', pid, e); continue
    assoc = d.get('relations',{}).get('associations',[])
    calls = sorted(set(a.get('identifier') or a.get('code') for a in assoc if a.get('contenttype') in ('call',) ))
    topics = [a.get('code') + ' ' + (a.get('title') or '') for a in assoc if a.get('contenttype')=='programme' and a.get('attributes',{}).get('type')=='relatedTopic']
    fs = [c.get('code') for c in d.get('relations',{}).get('categories',[]) if c.get('attributes',{}).get('classification')=='projectFundingSchemeCategory']
    print(f"## {pid} {d.get('acronym')} | {d.get('startDate')}..{d.get('endDate')} | {d.get('status')} | TC {d.get('totalCost')} | EU {d.get('ecMaxContribution')} | FS {fs} | {calls} | {topics}")
    print('   title:', d.get('title'))
    orgs = [a for a in assoc if a.get('contenttype')=='organization']
    def order(a):
        try: return int(a.get('attributes',{}).get('order','999'))
        except: return 999
    for a in sorted(orgs, key=order):
        at = a['attributes']
        act = None
        for c in (a.get('relations') or {}).get('categories', []) or []:
            if c.get('attributes',{}).get('classification')=='organizationActivityType': act = c.get('code')
        print(f"   {at.get('type'):17s} sme={at.get('sme'):5s} act={act} ec={at.get('ecContribution','-')} | {a.get('legalName')} ({a.get('address',{}).get('country')}) term={at.get('terminated')}")
