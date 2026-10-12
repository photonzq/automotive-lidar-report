"""Read-only audit of the links in index.html: kinds of href, relative targets that are missing from the published
tree, anchors with no matching id, malformed external URLs, and bare URLs left as plain text.
Usage: python link_audit.py <report folder>
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

root = Path(sys.argv[1])
soup = BeautifulSoup((root / "index.html").read_text(encoding="utf-8"), "html.parser")
tracked = set(subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True,
                             encoding="utf-8").stdout.split("\n"))
ids = {t.get("id") for t in soup.find_all(id=True)}

kinds = Counter()
rel_missing, rel_ok, anchors_missing, odd_ext = [], Counter(), [], []
for a in soup.find_all("a", href=True):
    h = a["href"]
    sp = urlsplit(h)
    if sp.scheme in ("http", "https"):
        kinds["external"] += 1
        if re.search(r"\s|[)\];,.]$|&amp;|%25", h) or h.count("(") != h.count(")"):
            odd_ext.append((h, a.get_text(" ", strip=True)[:60]))
    elif h.startswith("#"):
        kinds["anchor"] += 1
        if h[1:] not in ids:
            anchors_missing.append(h)
    elif sp.scheme:
        kinds[sp.scheme] += 1
    else:
        kinds["relative"] += 1
        path = unquote(sp.path)
        if path in tracked:
            rel_ok[path.split("/")[0]] += 1
        else:
            rel_missing.append((h, a.get_text(" ", strip=True)[:70]))

print("href kinds:", dict(kinds))
print("relative links that resolve to published files:", dict(rel_ok))
print(f"relative links to files NOT in the published tree: {len(rel_missing)}")
for h, t in rel_missing:
    print(f"   {h}   [link text: {t}]")
print(f"anchors with no matching id: {len(anchors_missing)}", anchors_missing[:10])
print(f"external hrefs that look malformed: {len(odd_ext)}")
for h, t in odd_ext[:40]:
    print(f"   {h}   [text: {t}]")

# bare URLs in text that are not inside a link
bare = []
for s in soup.body.find_all(string=re.compile(r"https?://")):
    if any(p.name in ("a", "code", "pre", "script", "style") for p in s.parents if p is not None and p.name):
        continue
    for m in re.finditer(r"https?://\S+", str(s)):
        bare.append(m.group(0))
print(f"bare URLs in text, not clickable: {len(bare)}")
for u in bare[:15]:
    print("   ", u)
