"""Make a contact sheet of PDF pages (thumbnails with page numbers) to locate tables/figures.
Usage: python contact.py <pdf> <out.png> <first_1based> <last_1based> [cols] [thumb_width_px]
"""
import sys
import pymupdf
from PIL import Image, ImageDraw

pdf, out = sys.argv[1], sys.argv[2]
first, last = int(sys.argv[3]), int(sys.argv[4])
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 5
tw = int(sys.argv[6]) if len(sys.argv) > 6 else 300
d = pymupdf.open(pdf)
last = min(last, d.page_count)
thumbs = []
for i in range(first - 1, last):
    pg = d[i]
    zoom = tw / pg.rect.width
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, 60, 22], fill=(255, 255, 0))
    dr.text((4, 4), f"p{i + 1}", fill=(0, 0, 0))
    thumbs.append(im)
th = max(t.height for t in thumbs)
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
for k, t in enumerate(thumbs):
    sheet.paste(t, ((k % cols) * tw, (k // cols) * th))
sheet.save(out)
print(out, sheet.size)
