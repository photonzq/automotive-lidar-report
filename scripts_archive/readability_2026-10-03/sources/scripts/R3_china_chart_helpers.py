"""Small helpers used to read values off chart and table images (PNG/JPEG).

These reproduce the one-off commands used during the source check:
  gridlines  <img> <x>                 print y of light-grey horizontal gridlines
                                       crossing pixel column x
  labelrows  <img> <x0> <x1>           print vertical extents (y0, y1, centre) of
                                       dark text rows between columns x0..x1
                                       (used to locate axis tick labels)
  linetrace  <img> <x0> <x1> <step> <y_zero> <px_per_unit>
                                       follow a purple/violet line (e.g. a
                                       year-on-year growth curve) and convert
                                       its y position to axis units
  crop       <img> <x0> <y0> <x1> <y1> <out.png> [scale]
                                       crop a region and upscale it (LANCZOS)
                                       so that small table digits can be read
No network access; images are local files saved by R3_china_fetch_render.py.
"""
import sys
from PIL import Image


def gridlines(path, x):
    im = Image.open(path).convert("RGB")
    for y in range(im.size[1]):
        p = im.getpixel((x, y))
        if p[0] < 235 and abs(p[0] - p[1]) < 10 and abs(p[1] - p[2]) < 10:
            print(y, p)


def labelrows(path, x0, x1):
    im = Image.open(path).convert("RGB")
    rows = [y for y in range(im.size[1])
            if any(sum(im.getpixel((xx, y))) < 300 for xx in range(x0, x1))]
    groups = []
    for y in rows:
        if groups and y - groups[-1][-1] <= 1:
            groups[-1].append(y)
        else:
            groups.append([y])
    print([(g[0], g[-1], (g[0] + g[-1]) / 2) for g in groups])


def linetrace(path, x0, x1, step, y_zero, px_per_unit):
    im = Image.open(path).convert("RGB")

    def purple(p):
        return p[2] > 90 and p[2] - p[1] > 40 and p[0] < 180

    for x in range(x0, x1, step):
        ys = [y for y in range(int(y_zero)) if purple(im.getpixel((x, y)))]
        if ys:
            yc = (ys[0] + ys[-1]) / 2
            print(x, ys[0], ys[-1], "value~%.1f" % ((y_zero - yc) / px_per_unit))


def crop(path, x0, y0, x1, y1, out, scale=2):
    im = Image.open(path)
    c = im.crop((x0, y0, x1, y1))
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    c.save(out)
    print("saved", out, c.size)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gridlines":
        gridlines(a[1], int(a[2]))
    elif a[0] == "labelrows":
        labelrows(a[1], int(a[2]), int(a[3]))
    elif a[0] == "linetrace":
        linetrace(a[1], int(a[2]), int(a[3]), int(a[4]), float(a[5]), float(a[6]))
    elif a[0] == "crop":
        crop(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6],
             int(a[7]) if len(a) > 7 else 2)
