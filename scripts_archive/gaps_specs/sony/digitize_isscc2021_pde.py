"""Digitize the two PDE curves of Sony's ISSCC 2021 paper 7.3 (Fig. 7.3.4, bottom).

Paper: O. Kumagai et al., "A 189x600 Back-Illuminated Stacked SPAD Direct
Time-of-Flight Depth Sensor for Automotive LiDAR Systems", ISSCC 2021,
paper 7.3, pp. 110-112, doi:10.1109/ISSCC42613.2021.9365961.

Method
- Render the bottom of Fig. 7.3.4 (page 2 of the digest PDF) at 600 dpi.
- Find the two plot frames from long dark lines (column and row sums of
  non-white pixels). The left plot spans -50..140 degC on x (its 0 degC line
  is drawn darker and serves as a check); the right plot spans 850..940 nm.
  Both span 0..40 % PDE on y.
- The data markers sit on a red connecting line, so the red trace is sampled
  at the nominal x positions of the markers (read off the figure: -40, -20, 60
  and 125 degC; 850, 865, 880, 895, 905, 910, 925 and 940 nm). The red
  "Median" labels are excluded with boxes in data units.

Inputs : the paper PDF, path in the environment variable ISSCC21_PDF.
Outputs: printed PDE values; a PNG of the plotted region written to the
         folder given by GAPS_SPECS_RAW (default ".").
Accuracy: about +/-0.5 percentage points, limited by the low-resolution
         figure embedded in the digest PDF.
"""
import os
import numpy as np
import pymupdf

PDF = os.environ.get("ISSCC21_PDF", "isscc2021_7.3.pdf")
OUT = os.environ.get("GAPS_SPECS_RAW", ".")
DPI = 600

doc = pymupdf.open(PDF)
page = doc[1]
W, H = page.rect.width, page.rect.height
clip = pymupdf.Rect(W / 2, 0.485 * H, W, 0.625 * H)
pix = page.get_pixmap(dpi=DPI, clip=clip)
pix.save(os.path.join(OUT, "isscc21_fig734_pde_plots.png"))
img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(int)

gray = img.mean(axis=2)
nonwhite = gray < 200
cols = np.where(nonwhite.sum(axis=0) > 0.5 * img.shape[0])[0]
rows = np.where(nonwhite.sum(axis=1) > 0.35 * img.shape[1])[0]


def groups(idx):
    """Collapse runs of consecutive indices to their mean position."""
    out, run = [], [idx[0]]
    for i in idx[1:]:
        if i - run[-1] <= 2:
            run.append(i)
        else:
            out.append(float(np.mean(run)))
            run = [i]
    out.append(float(np.mean(run)))
    return out


vlines = groups(cols)   # left-plot left, 0 degC line, left-plot right, right-plot left, right-plot right
hlines = groups(rows)   # the last two are the plot top (40 %) and bottom (0 %)
top, bot = hlines[-2], hlines[-1]
L1, Z0, R1, L2, R2 = vlines[:5]
print("frame lines (px):", [round(v, 1) for v in vlines], "top/bottom:", round(top, 1), round(bot, 1))
print("check: the 0 degC line maps to %.1f degC" % (-50 + (Z0 - L1) / (R1 - L1) * 190.0))

red = (img[:, :, 0] > 110) & (img[:, :, 0] - img[:, :, 1] > 45) & (img[:, :, 0] - img[:, :, 2] > 45)


def pde(y_px):
    return 40.0 * (bot - y_px) / (bot - top)


def sample(x_px, exclude):
    ys = []
    for dx in range(-2, 3):
        col = int(round(x_px)) + dx
        for y in np.where(red[:, col])[0]:
            if top < y < bot and not exclude(pde(y)):
                ys.append(y)
    return pde(np.mean(ys)) if ys else float("nan")


print()
print("PDE vs temperature (left plot, median curve):")
for t in (-40, -20, 60, 125):
    x = L1 + (t + 50) / 190.0 * (R1 - L1)
    excl = (lambda p, t=t: (18.5 < p < 22.5) and (t < -2))
    print("  T = %5d degC   PDE = %5.1f %%" % (t, sample(x, excl)))

print()
print("PDE vs wavelength (right plot, median curve):")
for lam in (850, 865, 880, 895, 905, 910, 925, 940):
    x = L2 + (lam - 850) / 90.0 * (R2 - L2)
    excl = (lambda p, lam=lam: p > 28.0 and lam > 852)
    print("  lambda = %4d nm   PDE = %5.1f %%" % (lam, sample(x, excl)))
