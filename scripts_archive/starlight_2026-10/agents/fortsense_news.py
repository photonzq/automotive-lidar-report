"""Fetch the Fortsense (fortsense.com) news list and individual news items as plain text.

Usage:
  python fortsense_news.py list              -> prints id, date, title for listed news
  python fortsense_news.py show <id> [<id>]  -> prints the plain text of news items and
                                                saves the html under news_html/
"""
import re
import sys
import os
import html
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://www.fortsense.com"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
HERE = os.path.dirname(os.path.abspath(__file__))


def get(url, tries=4):
    import time
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:  # retry on timeouts / resets
            last = e
            time.sleep(5 * (k + 1))
    raise last


def strip(h):
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?is)<br\s*/?>|</p>|</div>|</li>|</h\d>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t\r\f\v]+", " ", h)
    h = re.sub(r"\n\s*\n+", "\n", h)
    return h.strip()


def cmd_list():
    seen = {}
    for page in range(1, 15):
        url = f"{BASE}/News?page={page}"
        try:
            h = get(url)
        except Exception as e:
            print("fail", url, e)
            break
        items = re.findall(r'href="/News/show\?status=1&(?:amp;)?id=(\d+)"(.*?)</a>', h, flags=re.S)
        new = 0
        for nid, inner in items:
            txt = strip(inner).replace("\n", " ")
            if nid not in seen or len(txt) > len(seen[nid]):
                if nid not in seen:
                    new += 1
                seen[nid] = txt
        if new == 0:
            break
    for nid in sorted(seen, key=lambda x: -int(x)):
        print(nid, "|", seen[nid][:200])


def cmd_show(ids):
    os.makedirs(os.path.join(HERE, "news_html"), exist_ok=True)
    for nid in ids:
        url = f"{BASE}/News/show?status=1&id={nid}"
        h = get(url)
        with open(os.path.join(HERE, "news_html", f"news_{nid}.html"), "w", encoding="utf-8") as f:
            f.write(h)
        t = strip(h)
        # crop navigation boilerplate
        t = re.sub(r"首页\s*\n\s*应用领域\s*\n\s*乘用车.*?产品发布", "", t, flags=re.S)
        t = re.sub(r"Front Page\s*\n\s*Application areas.*?Product release", "", t, flags=re.S)
        t = re.sub(r"相关 新闻.*?Back Top", "", t, flags=re.S)
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', h)
        print("=" * 20, nid, url)
        print(t[:12000])
        print("IMAGES:", [i for i in imgs if "uploads" in i][:60])


if __name__ == "__main__":
    if sys.argv[1] == "list":
        cmd_list()
    else:
        cmd_show(sys.argv[2:])
