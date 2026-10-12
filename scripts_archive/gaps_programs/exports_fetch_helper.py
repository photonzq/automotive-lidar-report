"""Download a web page with a generic browser User-Agent, save raw bytes and visible text, print keyword snippets.

Purpose
    Helper used on 2026-10-03 to fetch the trade-press, regulator and company pages behind the
    Chinese-brand lidar export estimate (exports_lidar_estimate.py), and to confirm verbatim
    quotes against the raw page text rather than a summary.

Inputs
    Command line: URL, output file path (relative, e.g. data/page.html), then optional regular
    expressions to search for in the visible text.

Outputs
    <output>       raw response bytes
    <output>.txt   visible text (scripts and styles removed)
    Printed status line and merged keyword snippets (or the first 6,000 characters).

Notes
    No contact details, credentials or e-mail addresses are sent; the User-Agent is a generic
    browser string. Some sites (sec.gov, autostat.ru, zhihu.com) refuse such requests.

Date: 2026-10-03
"""
import sys, re, os, requests
from html import unescape
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def text_of(html):
    html = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', html)
    html = re.sub(r'(?is)<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>|</td>|</th>', '\n', html)
    t = re.sub(r'(?s)<[^>]+>', ' ', html)
    t = unescape(t)
    t = re.sub(r'[ \t\r\f\v\u3000\xa0]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t
def snippets(t, pats, w=250, maxn=40):
    spans = []
    for p in pats:
        for m in re.finditer(p, t, flags=re.I):
            spans.append((max(0, m.start()-w), min(len(t), m.end()+w)))
    spans.sort()
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    for s, e in merged[:maxn]:
        print('---[%d]' % s); print(t[s:e].replace('\n', ' | '))
    if len(merged) > maxn: print('... %d more' % (len(merged)-maxn))
def get(url, out, extra_headers=None):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,de;q=0.7,ru;q=0.6"}
    if extra_headers: h.update(extra_headers)
    r = requests.get(url, headers=h, timeout=90)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'wb').write(r.content)
    enc = r.encoding
    if enc is None or enc.lower() == 'iso-8859-1':
        m = re.search(rb'charset=["\']?([\w-]+)', r.content[:3000])
        enc = m.group(1).decode() if m else (r.apparent_encoding or 'utf-8')
    html = r.content.decode(enc, errors='replace')
    t = text_of(html)
    open(out + '.txt', 'w', encoding='utf-8').write(t)
    return r, t
if __name__ == '__main__':
    url, out = sys.argv[1], sys.argv[2]
    pats = sys.argv[3:]
    r, t = get(url, out)
    print('STATUS', r.status_code, 'LEN', len(r.content), 'TEXTLEN', len(t), 'FINAL', r.url)
    if pats: snippets(t, pats)
    else: print(t[:6000])
