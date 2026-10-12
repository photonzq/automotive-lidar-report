"""Read bar heights from a bar-chart PNG by pixel colour.

Usage: python R3_china_bar_reader.py <chart.png> <x1,x2,...> <y_zero_px> <y_ref_px> <ref_value> [r,g,b] [tol]
For each x (a pixel column through a bar) the script scans DOWNWARD from the
top of the image and reports the first pixel whose colour is within `tol`
(sum of absolute RGB differences) of the bar colour and is followed by at least
4 more bar-coloured pixels; that y is the bar top. The value is obtained by
linear scaling between the zero line (value 0) and a reference gridline
(ref_value). If no colour is given, the colour 3 px above the zero line in the
first column is used. Overlaid watermarks or labels can hide part of a bar, so
check several columns per bar and look at the image as well.
"""
import sys
from PIL import Image


def close(p, q, tol):
    return sum(abs(p[i] - q[i]) for i in range(3)) <= tol


def main():
    path = sys.argv[1]
    xs = [int(v) for v in sys.argv[2].split(",")]
    y0 = float(sys.argv[3])
    yref = float(sys.argv[4])
    vref = float(sys.argv[5])
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if len(sys.argv) > 6:
        col = tuple(int(v) for v in sys.argv[6].split(","))
    else:
        col = im.getpixel((xs[0], int(y0) - 3))
    tol = int(sys.argv[7]) if len(sys.argv) > 7 else 30
    print("image size", w, h, "bar colour", col, "tol", tol)
    for x in xs:
        top = None
        for y in range(0, int(y0)):
            if all(close(im.getpixel((x, y + k)), col, tol) for k in range(5)):
                top = y
                break
        if top is None:
            print(f"x={x}: no bar found")
            continue
        val = (y0 - top) / (y0 - yref) * vref
        print(f"x={x}: top y={top}, value~{val:,.0f}")


if __name__ == "__main__":
    main()
