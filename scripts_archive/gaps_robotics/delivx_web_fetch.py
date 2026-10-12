"""Fetch press-release pages as plain text and crop press photos for inspection.

Used for the "Delivery robots outside China" open item of the automotive
perception report (Appendix 1; section B4a, subsection 4) to read Serve
Robotics' and Ouster's press releases at mirrors (PR Newswire, Robotics
Tomorrow, StockTitan, Electrek, New Atlas) when the companies' own investor
sites timed out, and to count the lidars visible on Serve's second- and
third-generation robots in a published press photo.

Commands
--------
``text URL NAME [--out DIR] [--pattern REGEX] [--context N]``
    Downloads URL with a generic browser User-Agent, strips scripts, styles
    and tags, saves ``DIR/NAME.html`` and ``DIR/NAME.txt`` and prints every
    hit of the pattern (default: lidar|Ouster|sensor) with context.

``images HTMLFILE [--grep WORD]``
    Lists the .jpg/.png/.webp URLs found in a saved HTML page, optionally
    only those containing WORD.

``get URL FILE``
    Downloads one image.

``crop FILE OUT x0 y0 x1 y1 [--ref-width W] [--scale S]``
    Crops a region given in the coordinates of a W-pixel-wide preview of the
    image (default 1600), so that boxes chosen on the preview map onto the
    full-resolution original, and enlarges the crop by S.

Usage example (as used for the Serve photos)
--------------------------------------------
    python delivx_web_fetch.py text https://www.prnewswire.com/news-releases/serve-robotics-announces-expanded-los-angeles-delivery-extended-lidar-supply-agreement-302184458.html prn_serve_ouster_2024
    python delivx_web_fetch.py images web/newatlas_gen3.html --grep serve
    python delivx_web_fetch.py get <image-url> img/gen2_gen3.jpg
    python delivx_web_fetch.py crop img/gen2_gen3.jpg img/gen3_top.jpg 980 300 1180 470 --scale 5

No login, cookie or personal data is sent.
"""
import argparse
import html
import os
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.8"}


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def to_text(raw):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>", "\n", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t\xa0]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t)


def cmd_text(a):
    os.makedirs(a.out, exist_ok=True)
    raw = fetch(a.url).decode("utf-8", errors="replace")
    with open(os.path.join(a.out, a.name + ".html"), "w", encoding="utf-8") as f:
        f.write(raw)
    t = to_text(raw)
    with open(os.path.join(a.out, a.name + ".txt"), "w", encoding="utf-8") as f:
        f.write(t)
    print(a.name, len(t), "characters")
    last = -1
    for m in re.finditer(a.pattern, t, re.I):
        if m.start() < last:
            continue
        s, e = max(0, m.start() - a.context), min(len(t), m.end() + a.context)
        print("...", t[s:e].replace("\n", " "), "...\n")
        last = e


def cmd_images(a):
    with open(a.htmlfile, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    urls = sorted(set(re.findall(r"https?://[^\"' >]+?\.(?:jpg|jpeg|png|webp)", raw, re.I)))
    for u in urls:
        if not a.grep or a.grep.lower() in u.lower():
            print(u)


def cmd_get(a):
    d = fetch(a.url)
    os.makedirs(os.path.dirname(a.file) or ".", exist_ok=True)
    with open(a.file, "wb") as f:
        f.write(d)
    print(a.file, len(d), "bytes")


def cmd_crop(a):
    from PIL import Image  # Pillow ships with the Anaconda distribution
    im = Image.open(a.file)
    k = im.size[0] / a.ref_width
    box = tuple(int(v * k) for v in (a.x0, a.y0, a.x1, a.y1))
    c = im.crop(box)
    c = c.resize((int((a.x1 - a.x0) * a.scale), int((a.y1 - a.y0) * a.scale)))
    c.save(a.out)
    print(a.out, c.size)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pt = sub.add_parser("text")
    pt.add_argument("url")
    pt.add_argument("name")
    pt.add_argument("--out", default="web")
    pt.add_argument("--pattern", default=r"lidar|Ouster|sensor")
    pt.add_argument("--context", type=int, default=400)
    pi = sub.add_parser("images")
    pi.add_argument("htmlfile")
    pi.add_argument("--grep", default="")
    pg = sub.add_parser("get")
    pg.add_argument("url")
    pg.add_argument("file")
    pc = sub.add_parser("crop")
    pc.add_argument("file")
    pc.add_argument("out")
    for n in ("x0", "y0", "x1", "y1"):
        pc.add_argument(n, type=float)
    pc.add_argument("--ref-width", type=float, default=1600)
    pc.add_argument("--scale", type=float, default=4)
    a = p.parse_args()
    {"text": cmd_text, "images": cmd_images, "get": cmd_get, "crop": cmd_crop}[a.cmd](a)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
