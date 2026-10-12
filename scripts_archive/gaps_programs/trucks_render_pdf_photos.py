"""Render PDF pages, extract embedded photos and crop sensor regions for photo-based counts.

Purpose
    Support the photo check of Aurora's second-generation (International LT) trucks in
    Aurora's Q2 2026 Business Review presentation and 23 Sep 2026 Investor Day deck
    (report Appendix 1, Aurora lidar-count item). Pages are rendered with PyMuPDF,
    embedded images wider than a threshold are saved at native resolution, a contact
    sheet of all pages is built, and optional crop boxes are cut out and enlarged.

Inputs (command line)
    pdf                  path to a downloaded PDF (relative or absolute)
    --out DIR            output folder (default: ./data/png)
    --tag NAME           file-name prefix (default: pdf stem)
    --dpi N              page render resolution (default 60 for the contact sheet)
    --pages P [P ...]    1-based pages whose embedded images are extracted (default: all)
    --minw N             minimum embedded-image width to keep (default 300 px)
    --crop IMG x0 y0 x1 y1 SCALE   repeatable; crop box on an extracted image, enlarged by SCALE

Outputs
    DIR/<tag>_NN.png             page renders
    DIR/sheet_<tag>.png          contact sheet (4 columns)
    DIR/<tag>_pgN_xXREF_WxH.png  embedded images
    DIR/crop_<k>.png             enlarged crops

Date: 2026-10-03
"""
import argparse
import os
import sys

import pymupdf
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default=os.path.join("data", "png"))
    ap.add_argument("--tag")
    ap.add_argument("--dpi", type=int, default=60)
    ap.add_argument("--pages", type=int, nargs="*")
    ap.add_argument("--minw", type=int, default=300)
    ap.add_argument("--crop", nargs=6, action="append", default=[],
                    metavar=("IMG", "X0", "Y0", "X1", "Y1", "SCALE"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = a.tag or os.path.splitext(os.path.basename(a.pdf))[0][:20]
    doc = pymupdf.open(a.pdf)
    renders = []
    for i in range(doc.page_count):
        fn = os.path.join(a.out, f"{tag}_{i + 1:02d}.png")
        doc[i].get_pixmap(dpi=a.dpi).save(fn)
        renders.append(fn)
    ims = [Image.open(f) for f in renders]
    w, h = ims[0].size
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), "white")
    draw = ImageDraw.Draw(sheet)
    for k, (fn, im) in enumerate(zip(renders, ims)):
        x, y = (k % cols) * w, (k // cols) * h
        sheet.paste(im.resize((w, h)), (x, y))
        draw.text((x + 5, y + 5), os.path.basename(fn), fill="red")
    sheet.save(os.path.join(a.out, f"sheet_{tag}.png"))
    pages = a.pages or list(range(1, doc.page_count + 1))
    for p in pages:
        for img in doc[p - 1].get_images(full=True):
            xref = img[0]
            pix = pymupdf.Pixmap(doc, xref)
            if pix.n - pix.alpha > 3:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            if pix.width >= a.minw:
                fn = os.path.join(a.out, f"{tag}_pg{p}_x{xref}_{pix.width}x{pix.height}.png")
                pix.save(fn)
                print("image:", fn)
    for k, (img, x0, y0, x1, y1, scale) in enumerate(a.crop):
        im = Image.open(img)
        box = tuple(int(v) for v in (x0, y0, x1, y1))
        s = float(scale)
        out = im.crop(box).resize((int((box[2] - box[0]) * s), int((box[3] - box[1]) * s)),
                                  Image.LANCZOS)
        fn = os.path.join(a.out, f"crop_{k}.png")
        out.save(fn)
        print("crop:", fn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
