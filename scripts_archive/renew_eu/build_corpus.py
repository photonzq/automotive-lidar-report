"""Build one normalized table of all FP7, Horizon 2020 and Horizon Europe projects from the
CORDIS bulk JSON downloads.

Sources (European Commission, CORDIS open data, https://data.europa.eu):
    https://cordis.europa.eu/data/cordis-fp7projects-json.zip      (tables: project.json, organization.json, ...)
    https://cordis.europa.eu/data/cordis-h2020projects-json.zip    (one JSON record per project)
    https://cordis.europa.eu/data/cordis-HORIZONprojects-json.zip  (one JSON record per project)
Unzip each archive into a folder of the same name (without .zip) inside <bulk_dir>.

For every project the table keeps: framework programme, id, acronym, title, objective,
keywords, start/end/signature dates, status, total cost, maximum EU contribution, master
and sub call, topic code and title, legal-basis (programme) codes, funding-scheme code,
coordinator (name, country, activity type, SME flag), the number of participants, and a
compact list of all participants (name | country | role | EU contribution | SME).

Usage:
    python build_corpus.py <bulk_dir> <out_pickle>
"""
import glob
import json
import os
import sys

import pandas as pd


def aslist(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def fnum(x):
    try:
        return float(str(x).replace(',', '.'))
    except (TypeError, ValueError):
        return float('nan')


def load_fp7(folder):
    proj = json.load(open(os.path.join(folder, 'project.json'), encoding='utf-8'))
    orgs = json.load(open(os.path.join(folder, 'organization.json'), encoding='utf-8'))
    tops = json.load(open(os.path.join(folder, 'topics.json'), encoding='utf-8'))
    by_p = {}
    for o in orgs:
        by_p.setdefault(str(o['projectID']), []).append(o)
    top_t = {}
    for t in tops:
        top_t.setdefault(str(t['projectID']), []).append((t.get('topic', ''), t.get('title', '')))
    rows = []
    for p in proj:
        pid = str(p['id'])
        os_ = by_p.get(pid, [])
        coord = [o for o in os_ if o.get('role') == 'coordinator']
        c = coord[0] if coord else {}
        tt = top_t.get(pid, [])
        rows.append(dict(
            fp='FP7', id=pid, acronym=p.get('acronym', ''), title=p.get('title', ''),
            objective=p.get('objective', '') or '', keywords=p.get('keywords', '') or '',
            startDate=p.get('startDate', ''), endDate=p.get('endDate', ''),
            ecSignatureDate=p.get('ecSignatureDate', ''), status=p.get('status', ''),
            totalCost=fnum(p.get('totalCost')), ecMax=fnum(p.get('ecMaxContribution')),
            masterCall=p.get('masterCall', '') or '', subCall=p.get('subCall', '') or '',
            topic=';'.join(x[0] for x in tt) or (p.get('topics', '') or ''),
            topicTitle=';'.join(x[1] for x in tt),
            legalBasis=p.get('legalBasis', '') or '', fundingScheme=p.get('fundingScheme', '') or '',
            coordName=c.get('name', ''), coordCountry=c.get('country', ''),
            coordType=c.get('activityType', ''), coordSME=str(c.get('SME', '')),
            nPart=len(os_),
            parts=' || '.join(f"{o.get('name','')}|{o.get('country','')}|{o.get('role','')}|{o.get('ecContribution','')}|{o.get('SME','')}" for o in os_),
        ))
    return rows


def load_rcn_folder(folder, fp):
    rows = []
    for path in glob.glob(os.path.join(folder, 'project-rcn-*.json')):
        d = json.load(open(path, encoding='utf-8'))
        rel = d.get('relations', {}) or {}
        master = sub = ''
        topics, ttitles, lbs = [], [], []
        orgs = []
        for a in aslist(rel.get('associations')):
            ct = a.get('contenttype')
            at = a.get('attributes', {}) or {}
            if ct == 'call':
                if at.get('type') == 'relatedMasterCall':
                    master = a.get('identifier', '')
                elif at.get('type') == 'relatedSubCall':
                    sub = a.get('identifier', '')
            elif ct == 'programme':
                if at.get('type') == 'relatedTopic':
                    topics.append(a.get('code', ''))
                    ttitles.append(a.get('title', ''))
                elif at.get('type') == 'relatedLegalBasis':
                    lbs.append(a.get('code', ''))
            elif ct == 'organization':
                act = ''
                for cat in aslist(((a.get('relations') or {}).get('categories'))):
                    if (cat.get('attributes') or {}).get('classification') == 'organizationActivityType':
                        act = (cat.get('code') or '').strip('/')
                orgs.append(dict(name=a.get('legalName', ''), country=((a.get('address') or {}).get('country', '')),
                                 role=at.get('type', ''), ec=at.get('ecContribution', ''), sme=at.get('sme', ''),
                                 act=act, terminated=at.get('terminated', '')))
        fs = ''
        for cat in aslist(rel.get('categories')):
            if (cat.get('attributes') or {}).get('classification') == 'projectFundingSchemeCategory':
                fs = (cat.get('code') or '').strip('/')
        coord = [o for o in orgs if o['role'] == 'coordinator']
        c = coord[0] if coord else {}
        rows.append(dict(
            fp=fp, id=str(d.get('id', '')), acronym=d.get('acronym', ''), title=d.get('title', ''),
            objective=d.get('objective', '') or '', keywords=d.get('keywords', '') or '',
            startDate=d.get('startDate', ''), endDate=d.get('endDate', ''),
            ecSignatureDate=d.get('ecSignatureDate', ''), status=d.get('status', ''),
            totalCost=fnum(d.get('totalCost')), ecMax=fnum(d.get('ecMaxContribution')),
            masterCall=master, subCall=sub, topic=';'.join(topics), topicTitle=';'.join(ttitles),
            legalBasis=';'.join(lbs), fundingScheme=fs,
            coordName=c.get('name', ''), coordCountry=c.get('country', ''),
            coordType=c.get('act', ''), coordSME=c.get('sme', ''),
            nPart=len([o for o in orgs if o['role'] in ('coordinator', 'participant')]),
            parts=' || '.join(f"{o['name']}|{o['country']}|{o['role']}|{o['ec']}|{o['sme']}" for o in orgs),
        ))
    return rows


def main(bulk_dir, out_pickle):
    rows = load_fp7(os.path.join(bulk_dir, 'cordis-fp7projects-json'))
    print('FP7', len(rows))
    r2 = load_rcn_folder(os.path.join(bulk_dir, 'cordis-h2020projects-json'), 'H2020')
    print('H2020', len(r2))
    r3 = load_rcn_folder(os.path.join(bulk_dir, 'cordis-HORIZONprojects-json'), 'HORIZON')
    print('HORIZON', len(r3))
    df = pd.DataFrame(rows + r2 + r3)
    print('total', len(df), 'unique ids', df['id'].nunique())
    df.to_pickle(out_pickle)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
