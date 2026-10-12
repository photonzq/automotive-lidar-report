"""Strip an HTML file to readable text (main content heuristics).

Usage: python html2text.py <file.html> [start_marker] [end_marker]
Prints visible text; optional markers trim output to the region between them.
"""
import sys
import re
import html as htmlmod

path = sys.argv[1]
raw = open(path, "rb").read()
for enc in ("utf-8", "shift_jis", "euc-jp", "latin-1"):
    try:
        txt = raw.decode(enc)
        break
    except UnicodeDecodeError:
        continue

txt = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", txt)
txt = re.sub(r"(?i)<br\s*/?>", "\n", txt)
txt = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|table|section|article|dd|dt)>", "\n", txt)
txt = re.sub(r"(?s)<[^>]+>", " ", txt)
txt = htmlmod.unescape(txt)
txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
txt = re.sub(r"\n\s*\n+", "\n", txt)

if len(sys.argv) > 2:
    s = txt.find(sys.argv[2])
    if s >= 0:
        txt = txt[s:]
if len(sys.argv) > 3:
    e = txt.find(sys.argv[3])
    if e >= 0:
        txt = txt[:e]

sys.stdout.reconfigure(encoding="utf-8")
print(txt)
