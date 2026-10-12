import json,sys
sys.stdout.reconfigure(encoding='utf-8')
for id in sys.argv[1:]:
    d=json.load(open(f'c_{id}.json',encoding='utf-8'))
    print('=====',id,d['acronym'],'|',d['title'])
    print('dates',d['startDate'],d['endDate'],'dur',d.get('duration'),'total',d['totalCost'],'EC',d['ecMaxContribution'],'status',d['status'])
    rel=d.get('relations',{})
    for a in rel.get('associations',[]):
        ct=a.get('contenttype')
        at=a.get('attributes',{})
        if ct=='organization':
            print('  ORG',at.get('type'),'|',a.get('legalName'),'|',a.get('address',{}).get('country'),'| EC',at.get('ecContribution'),'| sme',at.get('sme'),'| term',at.get('terminated'))
        elif ct in ('call','programme','topic','fundingScheme'):
            print('  ',ct,at.get('type'),a.get('identifier') or a.get('code'),'|',a.get('title'))
        else:
            print('  ',ct,at.get('type'),'|',a.get('title') or a.get('code'))
    for k,v in rel.items():
        if k!='associations':
            for x in v:
                print('  REL',k,'|',x.get('code') or x.get('identifier'),'|',x.get('title'),'|',x.get('attributes',{}).get('type'))
