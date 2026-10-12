"""Render the two key Fortsense primary sources for reading: the China Securities Journal page carrying the
Xintong Electronics announcement (one broadsheet page, rendered as overlapping tiles around the Fortsense
blocks) and the Tower Semiconductor press release (two pages)."""
import re
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
OUT = HERE / "render"
OUT.mkdir(exist_ok=True)

# Tower press release: whole pages
d = pymupdf.open(HERE / "tower_fortsense_20230911.pdf")
for i, p in enumerate(d):
    p.get_pixmap(dpi=160).save(OUT / f"tower_p{i + 1}.png")
    print("tower page", i + 1, "rendered", p.rect)

# CS broadsheet: find the text blocks that mention Fortsense and render the column regions around them
d = pymupdf.open(HERE / "cs_20260808_B053.pdf")
p = d[0]
print("CS page rect", p.rect)
blocks = p.get_text("blocks")
hit = [b for b in blocks if re.search(r"阜时|SPAD|激光雷达|极氪", b[4])]
print(len(blocks), "blocks;", len(hit), "with Fortsense keywords")
for b in hit[:60]:
    print(f"  ({b[0]:.0f},{b[1]:.0f})-({b[2]:.0f},{b[3]:.0f}) {re.sub(chr(10), ' ', b[4])[:70]}")
if hit:
    x0 = min(b[0] for b in hit) - 5
    y0 = min(b[1] for b in hit) - 5
    x1 = max(b[2] for b in hit) + 5
    y1 = max(b[3] for b in hit) + 5
    print("bounding region", x0, y0, x1, y1)
    # tile the region into column strips of about 200 pt height for legible rendering
    W = x1 - x0
    ncol = max(1, int(W // 230) + 1)
    tile_w = W / ncol
    k = 0
    y = y0
    while y < y1:
        for c in range(ncol):
            clip = pymupdf.Rect(x0 + c * tile_w, y, x0 + (c + 1) * tile_w, min(y + 260, y1))
            k += 1
            p.get_pixmap(dpi=200, clip=clip).save(OUT / f"cs_tile_{k:02d}.png")
        y += 250
    print(k, "tiles rendered")
