"""Page through the EU Funding & Tenders portal search API for one free-text query and save
every result page as raw JSON, then print a summary by data source and type.

The API is the one the public portal itself calls; "SEDIA" is the portal's public key
constant (no login, no personal data is sent). Results mix call topics, funded projects,
organisations, tenders and FAQs; the DATASOURCE and type metadata tell them apart.

Usage:
    python ft_search.py <query_text> <tag> <out_dir> [max_pages]
Example:
    python ft_search.py lidar lidar ft_raw 25
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse

API = 'https://api.tech.ec.europa.eu/search-api/prod/rest/search'


def fetch_page(text, page, size=100):
    # curl's bare POST (no body, no content type) is what the API accepts
    qs = urllib.parse.urlencode({'apiKey': 'SEDIA', 'text': text, 'pageSize': size, 'pageNumber': page})
    out = subprocess.run(['curl', '-s', '-m', '180', '-X', 'POST', API + '?' + qs],
                         capture_output=True, check=True).stdout
    return json.loads(out.decode('utf-8'))


def main(text, tag, out_dir, max_pages=25):
    os.makedirs(out_dir, exist_ok=True)
    allres = []
    page = 1
    while page <= max_pages:
        fn = os.path.join(out_dir, f'{tag}_p{page}.json')
        if os.path.exists(fn):
            d = json.load(open(fn, encoding='utf-8'))
        else:
            d = fetch_page(text, page)
            json.dump(d, open(fn, 'w', encoding='utf-8'))
            time.sleep(0.5)
        res = d.get('results', [])
        allres += res
        tot = int(d.get('totalResults', 0))
        if not res or len(allres) >= tot:
            break
        page += 1
    from collections import Counter
    c = Counter((r.get('metadata', {}).get('DATASOURCE', ['?'])[0], (r.get('metadata', {}).get('type') or ['?'])[0]) for r in allres)
    print(tag, 'total', tot, 'fetched', len(allres))
    for k, v in c.most_common():
        print('  ', k, v)
    json.dump(allres, open(os.path.join(out_dir, f'{tag}_all.json'), 'w', encoding='utf-8'))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 25)
