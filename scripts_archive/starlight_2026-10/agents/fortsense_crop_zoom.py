"""Crop a region of an image and upscale it for reading small labels.

Usage: python crop_zoom.py <image> <x0> <y0> <x1> <y1> [scale] [out]
"""
import sys
import os
from PIL import Image

img = sys.argv[1]
x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
scale = float(sys.argv[6]) if len(sys.argv) > 6 else 3.0
out = sys.argv[7] if len(sys.argv) > 7 else os.path.splitext(img)[0] + f"_crop{x0}_{y0}_{x1}_{y1}.png"
im = Image.open(img).convert("RGB")
c = im.crop((x0, y0, x1, y1))
c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
c.save(out)
print(out, c.size)
