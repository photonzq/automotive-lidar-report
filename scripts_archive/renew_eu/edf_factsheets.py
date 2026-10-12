"""Download the European Defence Fund (EDF) project factsheets linked from the Commission's
"Result of the EDF <year> calls for proposals" pages and search them for lidar and
laser-sensing terms.

For each year the script fetches the results page (trying the "result-" and "results-"
URL spellings), collects every linked factsheet PDF, downloads it once into
<out_dir>/<year>/, extracts the text with PyMuPDF and counts keyword hits. It writes
<out_dir>/edf_factsheet_hits.csv with one row per factsheet: year, file name, project
acronym and ID (from the file name), keyword counts, the EU funding figure if one is printed,
and a short text window around the first lidar or laser-sensing hit.

Usage:
    python edf_factsheets.py <out_dir> [years...]
Example:
    python edf_factsheets.py edf 2021 2022 2023 2024 2025
"""
import csv
import os
import re
import subprocess
import sys
import time

import pymupdf

BASE = 'https://defence-industry-space.ec.europa.eu'
# the Commission site has moved these pages between path prefixes over the years
PAGES = [BASE + '/{p}/calls-proposals/{r}-edf-{{y}}-calls-proposals_en'.format(p=p, r=r)
         for p in ('funding-opportunities', 'funding-opportunities-0', 'funding-and-grants')
         for r in ('result', 'results')]
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
TERMS = {
    'lidar': r'(?<![a-z])(?:lidars?|ladars?)(?![a-z])|laser radar',
    'laser_range': r'laser range[- ]?find\w*|laser rang\w*|rangefinder\w*|range finder\w*',
    'active_imaging': r'active imaging|gated (?:viewing|imaging)|laser illuminat\w*',
    'laser': r'\blasers?\b',
    'optronic': r'optronic\w*|electro[- ]optic\w*|\beo/ir\b|infrared',
    'counter_uas': r'counter[- ]?(?:uas|uav|drone)s?|c-uas|anti[- ]drone',
    'fmcw_coherent': r'fmcw|coherent',
    'photonic': r'photonic\w*',
}


def curl(url, out):
    subprocess.run(['curl', '-s', '-L', '-m', '300', '-A', UA, '-o', out, url], check=False)


def is_pdf(path):
    try:
        with open(path, 'rb') as f:
            return f.read(5) == b'%PDF-'
    except OSError:
        return False


def fetch_pdf(url, path, tries=5, pause=3.0):
    """Download a PDF politely; the server answers bursts with HTTP 429 pages, so validate
    the %PDF header and back off before retrying."""
    for k in range(tries):
        if is_pdf(path):
            return True
        curl(url, path)
        time.sleep(pause * (k + 1))
    return is_pdf(path)


def page_links(year, tmp):
    for pat in PAGES:
        url = pat.format(y=year)
        curl(url, tmp)
        try:
            html = open(tmp, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        links = sorted(set(re.findall(r'href="([^"]*(?:FACTSHEET|Factsheet|factsheet)[^"]*)"', html)))
        if links:
            return url, [l if l.startswith('http') else BASE + l for l in links]
    return None, []


def main(out_dir, years):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for y in years:
        ydir = os.path.join(out_dir, str(y))
        os.makedirs(ydir, exist_ok=True)
        page, links = page_links(y, os.path.join(ydir, '_results_page.html'))
        print(y, page, len(links), 'factsheets')
        for link in links:
            m = re.search(r'filename=([^&"]+)', link)
            name = (m.group(1) if m else link.rsplit('/', 1)[-1]).replace('+', '_')
            name = re.sub(r'[^A-Za-z0-9_.-]', '_', name)
            if not name.lower().endswith('.pdf'):
                name += '.pdf'
            path = os.path.join(ydir, name)
            if not fetch_pdf(link.replace('&amp;', '&'), path):
                print('  not a PDF after retries:', name)
                continue
            try:
                doc = pymupdf.open(path)
                text = ' '.join(doc[i].get_text() for i in range(doc.page_count))
            except Exception as exc:  # not a PDF (error page)
                print('  skip', name, exc)
                continue
            flat = ' '.join(text.split())
            low = flat.lower()
            row = dict(year=y, file=name)
            idm = re.search(r'_(\d{9})_([^.]+)\.pdf$', name)
            row['project_id'] = idm.group(1) if idm else ''
            row['acronym'] = idm.group(2) if idm else ''
            for k, p in TERMS.items():
                row['n_' + k] = len(re.findall(p, low))
            eu = re.search(r'EU (?:funding|contribution)[^0-9€]{0,40}(?:EUR|€)?\s*([\d.,]+\s*(?:million|M)?)', flat, re.I)
            row['eu_funding_text'] = eu.group(1) if eu else ''
            hit = re.search(TERMS['lidar'] + '|' + TERMS['laser_range'] + '|' + TERMS['active_imaging'], low)
            row['context'] = flat[max(0, hit.start() - 200): hit.end() + 200] if hit else ''
            rows.append(row)
    out = os.path.join(out_dir, 'edf_factsheet_hits.csv')
    if rows:
        with open(out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print('rows', len(rows), '->', out)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], [int(a) for a in sys.argv[2:]])
