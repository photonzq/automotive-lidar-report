"""Crop a region of a PNG (fractions of width/height) and save it.
Usage: python crop.py <in.png> <out.png> x0 y0 x1 y1   (fractions 0..1)
"""
import sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = (float(v) for v in sys.argv[3:7])
im = Image.open(src)
w, h = im.size
im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))).save(dst)
print(dst, im.size)
