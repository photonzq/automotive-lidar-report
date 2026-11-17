"""Print the article as an ordered sequence of short text snippets and image
markers (index + URL), so each image can be matched to the text around it.

Usage: python -I seq_text_img.py NAME [start_marker] [img_host_substring]
Reads ../raw/NAME.html.
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
here = os.path.dirname(os.path.abspath(__file__))
rawdir = os.path.join(os.path.dirname(here), "raw")
name = sys.argv[1]
start_marker = sys.argv[2] if len(sys.argv) > 2 else ""
host = sys.argv[3] if len(sys.argv) > 3 else ""
raw = open(os.path.join(rawdir, name + ".html"), "rb").read().decode("utf-8", "replace")
raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
if start_marker:
    k = raw.find(start_marker)
    if k > 0:
        raw = raw[k:]
tokens = re.split(r"(<img[^>]*>)", raw)
n = 0
for tok in tokens:
    if tok.lower().startswith("<img"):
        m = re.search(r'(?:data-src|src)\s*=\s*"([^"]+)"', tok)
        if m and (host in m.group(1)):
            print(f"[IMG {n}] {html.unescape(m.group(1))[:160]}")
            n += 1
    else:
        t = re.sub(r"(?s)<[^>]+>", " ", tok)
        t = html.unescape(t)
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            print("   " + t[-260:])
