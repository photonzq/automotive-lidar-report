"""show.py CHUNK LITERAL [width] [section-start-literal] - print contexts of a literal string in a chunk."""
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
cid, lit = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 100
t = (here / f"chunk{cid}" / f"chunk{cid}.md").read_text(encoding="utf-8")
if len(sys.argv) > 4:
    a = t.index(sys.argv[4])
    t = t[a:]
i = 0
n = 0
while True:
    j = t.find(lit, i)
    if j < 0:
        break
    n += 1
    print(f"--- #{n} at {j}:", repr(t[max(0, j - w):j + len(lit) + w]))
    i = j + len(lit)
print("total", n)
