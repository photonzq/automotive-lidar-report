"""Fetch Google Patents pages and print metadata, abstract, first claim, and
keyword-in-context snippets from the description.

Usage: python gpatent_text.py <PUBNUM> [<PUBNUM> ...]
Env var KW (optional): '|'-separated keywords for snippets (default: blooming-related terms).
Saved HTML goes to gp_html/.
"""
import sys
import os
import re
import time
import html
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
HERE = os.path.dirname(os.path.abspath(__file__))
KW = os.environ.get("KW", "高反|膨胀|饱和|串扰|光晕|强光|鬼影|寻址|分区|动态范围|堆积|pile")


def get(url):
    last = None
    for k in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:
            last = e
            time.sleep(8 * (k + 1))
    raise last


def text(h):
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h)
    return re.sub(r"\s+", " ", h).strip()


def meta(h, name):
    return [html.unescape(m) for m in re.findall(r'<meta name="%s" content="([^"]*)"' % re.escape(name), h)]


def section(h, itemprop):
    m = re.search(r'<section itemprop="%s".*?</section>' % itemprop, h, flags=re.S)
    return text(m.group(0)) if m else ""


def main():
    os.makedirs(os.path.join(HERE, "gp_html"), exist_ok=True)
    for pn in sys.argv[1:]:
        url = f"https://patents.google.com/patent/{pn}"
        try:
            h = get(url)
        except Exception as e:
            print("=" * 10, pn, "FAILED", e)
            continue
        with open(os.path.join(HERE, "gp_html", f"{pn}.html"), "w", encoding="utf-8") as f:
            f.write(h)
        print("=" * 10, pn, url)
        print("title:", meta(h, "DC.title"))
        print("assignee/inventors:", meta(h, "DC.contributor"))
        print("dates:", meta(h, "DC.date"), "| citation_patent_publication:",
              meta(h, "citation_patent_publication_number"))
        st = re.findall(r'itemprop="legalStatusIfi"[^>]*>\s*<span[^>]*>([^<]*)<', h)
        st2 = re.findall(r'<span itemprop="status">([^<]*)</span>', h)
        print("status:", st, st2[:3])
        ab = section(h, "abstract")
        print("ABSTRACT:", ab[:1500])
        cl = section(h, "claims")
        print("CLAIMS(first 1500):", cl[:1500])
        desc = section(h, "description")
        hits = [m.start() for m in re.finditer(KW, desc)]
        print(f"DESC length {len(desc)}; keyword hits {len(hits)}")
        last = -10000
        shown = 0
        for i in hits:
            if i - last < 300:
                continue
            last = i
            print("  ...", desc[max(0, i - 200): i + 300], "...")
            shown += 1
            if shown >= 8:
                break
        time.sleep(6)


if __name__ == "__main__":
    main()
