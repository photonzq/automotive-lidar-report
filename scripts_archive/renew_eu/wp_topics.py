"""Parse Horizon Europe work-programme PDFs into a topic table and flag sensing/lidar topics.

For every topic header of the form "HORIZON-CLx-YYYY-...: Title (...)" the script records
the work-programme file, the page, the title, the type of action, the indicative topic
budget and the expected EU contribution per project, and it counts keyword hits in the
topic text (from its header to the next topic header): lidar terms, 3-D/depth sensing,
generic sensing/perception terms, photonics terms, and the partnership tag.

Usage:
    python wp_topics.py <wp_pdf_dir> <out_csv>

<wp_pdf_dir> holds the work-programme PDFs downloaded from
https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/<period>/
"""
import csv
import glob
import os
import re
import sys

import pymupdf

TOPIC_RE = re.compile(r'(HORIZON-[A-Z0-9]+-\d{4}-[A-Z0-9-]*?\d{2}(?:-[A-Z0-9]+)?(?:-\d{2})?)\s*:\s*')
KW = {
    'lidar': r'(?<![a-z])(?:lidars?|ladars?)(?![a-z])|laser[- ]radar',
    'depth3d': r'3d[- ](?:sensing|imaging|vision)|depth[- ](?:sensing|perception)|time[- ]of[- ]flight|range[- ]finding|ranging',
    'perception': r'perception|environment(?:al)? sensing|sensor fusion|sensors?\b',
    'photonics': r'photonic|optical|laser',
    'photonics_partnership': r'photonics partnership',
    'ccam_partnership': r'ccam partnership|connected, cooperative and automated mobility',
    'sovereignty': r'sovereign|strategic autonomy|dependenc',
}


def page_texts(path):
    doc = pymupdf.open(path)
    return [doc[i].get_text() for i in range(doc.page_count)]


def main(wp_dir, out_csv):
    rows = []
    for path in sorted(glob.glob(os.path.join(wp_dir, '*.pdf'))):
        texts = page_texts(path)
        # concatenate with page markers so positions map back to pages
        offs, full = [], ''
        for i, t in enumerate(texts):
            offs.append(len(full))
            full += t + '\n'
        heads = []
        for m in TOPIC_RE.finditer(full):
            # a header is followed (within ~600 chars) by a "Call:" box
            tail = full[m.end(): m.end() + 900]
            if 'Call:' not in tail and 'Specific conditions' not in tail:
                continue
            title = tail.split('Call:')[0].split('Specific conditions')[0]
            title = ' '.join(title.split())
            heads.append((m.start(), m.group(1), title))
        # de-duplicate repeated headers at the same id (keep the first full one)
        seen = set()
        uniq = []
        for h in heads:
            if h[1] in seen:
                continue
            seen.add(h[1])
            uniq.append(h)
        for k, (pos, tid, title) in enumerate(uniq):
            end = uniq[k + 1][0] if k + 1 < len(uniq) else len(full)
            body = full[pos:end]
            page = max(i for i, o in enumerate(offs) if o <= pos)
            b = re.search(r'total indicative budget for the topic is EUR\s*([\d.,]+)\s*million', body)
            e = re.search(r'EU contribution of (?:between |around |up to )?EUR\s*([\d.,]+)(?:\s*(?:and|to)\s*(?:EUR\s*)?([\d.,]+))?\s*million', body)
            t = re.search(r'Type of Action\s+([^\n]+)', body)
            row = dict(wp=os.path.basename(path), page_1based=page + 1, topic=tid, title=title,
                       action=(t.group(1).strip() if t else ''),
                       budget_meur=(b.group(1) if b else ''),
                       per_project_meur=((e.group(1) + ('-' + e.group(2) if e.group(2) else '')) if e else ''))
            low = body.lower()
            for name, pat in KW.items():
                row['n_' + name] = len(re.findall(pat, low))
            rows.append(row)
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print('topics', len(rows), '->', out_csv)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
