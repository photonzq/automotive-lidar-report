"""Make downscaled previews: python -E -P preview.py MAXPX file1 [file2 ...]"""
import sys, os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 300_000_000
mx = int(sys.argv[1])
outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fmcw_img", "prev")
os.makedirs(outdir, exist_ok=True)
for f in sys.argv[2:]:
    im = Image.open(f)
    im = im.convert("RGB")
    im.thumbnail((mx, mx))
    out = os.path.join(outdir, os.path.splitext(os.path.basename(f))[0] + "_prev.jpg")
    im.save(out, quality=85)
    print(out, im.size)
