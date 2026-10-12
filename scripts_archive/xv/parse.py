import json,sys
def L(x):
    if x is None: return []
    return x if isinstance(x,list) else [x]
for fn in sys.argv[1:]:
    d=json.load(open(fn,encoding='utf-8'))
    hits=L(d['hits']['hit'])
    print('=====',fn,d['result']['header'].get('totalHits'))
    for h in hits:
        p=h.get('project')
        if not p: print('non-project', list(h.keys())); continue
        print('\n---', p.get('id'), p.get('acronym'), '|', p.get('title'))
        for k in ['startDate','endDate','totalCost','ecMaxContribution','status','ecSignatureDate','duration']:
            print('  ',k,':',p.get(k))
        rel=p.get('relations',{}).get('associations',{})
        for c in L(rel.get('call')): print('   call:',c['@attributes']['type'],c.get('identifier'))
        for pr in L(rel.get('programme')): print('   prog:',pr.get('code'),'|',pr.get('title'), pr['@attributes'].get('type'))
        orgs=L(rel.get('organization'))
        print('   n_orgs',len(orgs))
        for o in orgs:
            a=o.get('@attributes',{})
            nm=o.get('legalName')
            if a.get('type')=='coordinator' or any(x in str(nm).upper() for x in ['XENOMATIX','VOXEL']):
                print('   ORG:',nm,'|',a.get('type'),'| ec=',a.get('ecContribution'),'net=',a.get('netEcContribution'),'tc=',a.get('totalCost'),'sme=',a.get('sme'),'|',o.get('address',{}).get('city'))
        print('   OBJ:',p.get('objective','')[:3000])
