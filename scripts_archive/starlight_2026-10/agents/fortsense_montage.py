"""Tile several images into one contact sheet for quick viewing.

Usage: python montage.py <out.png> <cols> <tile_width> <img1> <img2> ...
"""
import sys
from PIL import Image

out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ims = [Image.open(p).convert("RGB") for p in sys.argv[4:]]
tiles = []
for im in ims:
    h = int(im.height * tw / im.width)
    tiles.append(im.resize((tw, h), Image.LANCZOS))
rows = (len(tiles) + cols - 1) // cols
row_h = [max(t.height for t in tiles[r * cols:(r + 1) * cols]) for r in range(rows)]
sheet = Image.new("RGB", (cols * tw, sum(row_h)), "white")
y = 0
for r in range(rows):
    for c, t in enumerate(tiles[r * cols:(r + 1) * cols]):
        sheet.paste(t, (c * tw, y))
    y += row_h[r]
sheet.save(out)
print(out, sheet.size)
