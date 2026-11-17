"""PDF helper (run with: python -E -P pdftool.py ...).

    heads PDF [N]          print page number and first N characters of text per page
    find PDF REGEX         print pages whose text matches REGEX with context
    render PDF OUTDIR DPI PAGES   render 1-based pages (e.g. 3,5-7) to PNG
    images PDF PAGES       list embedded images (xref, pixel size) on 1-based pages
"""
import sys
import os
import re
import pymupdf


def parse_pages(spec, n):
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [p for p in out if 1 <= p <= n]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    cmd, pdf = sys.argv[1], sys.argv[2]
    d = pymupdf.open(pdf)
    if cmd == "heads":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        print("pages", d.page_count, d.metadata)
        for i, p in enumerate(d):
            t = re.sub(r"\s+", " ", p.get_text())
            print(i + 1, "|", t[:n])
    elif cmd == "find":
        pat = sys.argv[3]
        for i, p in enumerate(d):
            t = re.sub(r"\s+", " ", p.get_text())
            for m in re.finditer(pat, t, re.I):
                a = max(0, m.start() - 250)
                b = min(len(t), m.end() + 250)
                print("p%d: ...%s..." % (i + 1, t[a:b]))
    elif cmd == "render":
        outdir, dpi, spec = sys.argv[3], int(sys.argv[4]), sys.argv[5]
        os.makedirs(outdir, exist_ok=True)
        base = os.path.splitext(os.path.basename(pdf))[0]
        for pn in parse_pages(spec, d.page_count):
            pix = d[pn - 1].get_pixmap(dpi=dpi)
            fn = os.path.join(outdir, "%s_p%d.png" % (base, pn))
            pix.save(fn)
            print("saved", fn, pix.width, pix.height)
    elif cmd == "images":
        spec = sys.argv[3]
        for pn in parse_pages(spec, d.page_count):
            for img in d[pn - 1].get_images(full=True):
                print("p%d xref %d %dx%d" % (pn, img[0], img[2], img[3]))


if __name__ == "__main__":
    main()
