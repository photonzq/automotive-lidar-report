"""R6_C10_part2-02 and -07: fetch every post linked from Voyant Photonics' news index and
search each for antenna counts, sub-array sizes and data-centre switching wording.

Usage: python R6_voyant_blog_scan.py <outdir>
Writes one text file per post into <outdir> and prints the title, date line and matching
sentences. Generic browser User-Agent; no e-mail address, key or credentials.
"""
import html
import re
import sys
import time
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
INDEX = "https://voyantphotonics.com/news/"
PATTERNS = [r"antenna", r"5,0\d\d", r"\b5\d{3}\b", r"sub-?array", r"4\s*[x×]\s*80",
            r"30 ?Hz", r"switch", r"data ?cent", r"optical circuit", r"pixels?"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>|</div>", "\n", raw)
    txt = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    return re.sub(r"\n\s*\n+", "\n", txt)


def main(outdir):
    links = sorted(set(re.findall(r'href="(https://voyantphotonics.com/news/\d+/)"', fetch(INDEX))),
                   key=lambda u: int(u.rstrip("/").split("/")[-1]))
    for url in links:
        try:
            txt = to_text(fetch(url))
        except Exception as exc:  # report and continue
            print(url, "ERROR", exc)
            continue
        pid = url.rstrip("/").split("/")[-1]
        open(f"{outdir}/voyant_post_{pid}.txt", "w", encoding="utf-8").write(txt)
        title = re.search(r"\n\s*([^\n]{20,200})\n", txt)
        print("=" * 100)
        print(url, "|", (title.group(1).strip() if title else ""))
        for line in txt.split("\n"):
            if re.search(r"(January|February|March|April|May|June|July|August|September|"
                         r"October|November|December) \d{1,2}, 20\d\d", line):
                print("  DATE:", line.strip()[:160])
                break
        for sent in re.split(r"(?<=[.!?])\s+", txt):
            if any(re.search(p, sent, re.I) for p in PATTERNS[:6]):
                print("  >>", sent.strip()[:400])
        time.sleep(1.0)


if __name__ == "__main__":
    main(sys.argv[1])
