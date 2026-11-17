"""Print body text, byline/date and article images of saved Electronics360 pages.

Usage: python -I e360_body.py NAME [NAME ...]   (reads ../raw/NAME.html)
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
here = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(os.path.dirname(here), "raw")


def clean(s):
    s = re.sub(r"(?is)<script.*?</script>", " ", s)
    s = re.sub(r"(?is)<style.*?</style>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|div|h[1-6]|li|figcaption)>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


for name in sys.argv[1:]:
    raw = open(os.path.join(rawdir, name + ".html"), "rb").read().decode("utf-8", "replace")
    print("=" * 30, name, "=" * 30)
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    print("TITLE:", html.unescape(m.group(1)).strip() if m else "")
    for pat in (r'"datePublished"\s*:\s*"([^"]+)"', r'property="article:published_time" content="([^"]+)"',
                r'class="[^"]*(?:date|byline)[^"]*"[^>]*>(.*?)</', r'"author"\s*:\s*\{[^}]*"name"\s*:\s*"([^"]+)"'):
        for mm in re.finditer(pat, raw, re.S):
            print("META:", clean(mm.group(1))[:200])
    # article body: between first <article or itemprop=articleBody and the end
    a = re.search(r'(?is)(itemprop="articleBody"|class="[^"]*article-body[^"]*"|<article)', raw)
    start = a.start() if a else 0
    body = raw[start:start + 120000]
    endm = re.search(r'(?is)(Related Articles|More from|Comments|Sponsored|Recommended)', body[2000:])
    if endm:
        body = body[:2000 + endm.start()]
    print(clean(body)[:7000])
    print("---- images ----")
    for mm in re.finditer(r'(?is)<img[^>]+>', body):
        tag = mm.group(0)
        src = re.search(r'(?:data-src|src)\s*=\s*"([^"]+)"', tag)
        alt = re.search(r'alt\s*=\s*"([^"]*)"', tag)
        w = re.search(r'width\s*=\s*"(\d+)"', tag)
        h = re.search(r'height\s*=\s*"(\d+)"', tag)
        if src:
            print(src.group(1), "| alt:", alt.group(1) if alt else "", "|", w.group(1) if w else "", "x", h.group(1) if h else "")
