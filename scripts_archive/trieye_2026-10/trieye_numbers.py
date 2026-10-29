"""Numbers for the TriEye bullets of §A7.5: ASTM G173-03 sunlight at the wavelengths TriEye's patents and products use,
the dark charge a gated Ge pixel collects, and the depth slice of a gate.

Sunlight: reads the ASTM G173-03 reference spectra (``astmg173.zip`` from the National Laboratory of the Rockies,
formerly NREL, https://www.nlr.gov/media/docs/libraries/grid/zip/astmg173.zip ; the same file as
gaps_scanners_regulation/astm_g173_lidar_bands.py) and prints the global-tilt +/-10 nm band average (trapezoidal
integral over [lambda-10, lambda+10] divided by 20 nm) at 1,135 (LITEON's VCSEL), 1,320, 1,340, 1,375, 1,440 and
1,550 nm.
Usage: python trieye_numbers.py [path/to/astmg173.zip]   (default: astmg173.zip in the current folder)
"""
import io
import sys
import zipfile

import numpy as np

Q = 1.602176634e-19        # electron charge, C
C = 2.99792458e8           # speed of light, m/s


def load(path):
    with zipfile.ZipFile(path) as z:
        text = z.read("ASTMG173.csv").decode("latin-1")
    rows = []
    for line in io.StringIO(text):
        parts = line.strip().split(",")
        try:
            rows.append([float(p) for p in parts[:4]])
        except ValueError:
            continue
    a = np.array(rows)
    return a[:, 0], a[:, 2]    # wavelength (nm), global tilt (W m^-2 nm^-1)


def band(wl, e, lam, half=10.0):
    m = (wl >= lam - half) & (wl <= lam + half)
    return np.trapezoid(e[m], wl[m]) / (2 * half)


path = sys.argv[1] if len(sys.argv) > 1 else "astmg173.zip"
wl, gt = load(path)
ref = band(wl, gt, 1550)
for lam in (1135, 1320, 1340, 1375, 1440, 1550):
    b = band(wl, gt, lam)
    exact = gt[np.argmin(abs(wl - lam))]
    b2 = band(wl, gt, lam, half=2.0)
    print(f"{lam} nm: global tilt +/-10 nm average {b:.3e} W m^-2 nm^-1 = {b/ref:.2e} x the 1,550 nm value; "
          f"+/-2 nm average {b2:.3e}; tabulated at {lam} nm: {exact:.3e}")

# dark charge of a TES200 pixel (100 pA at 25 C, 7 um pitch) and the dark current density it implies
i_d, pitch = 100e-12, 7e-4                       # A, cm
print(f"dark current density {i_d/pitch**2*1e6:.0f} uA/cm^2 (pixel area {pitch**2:.2e} cm^2)")
for t in (100e-9, 1e-6):
    print(f"dark electrons in a {t*1e9:.0f} ns gate: {i_d*t/Q:.1f}")
frame = 1 / 30
print(f"dark electrons in a 1/30 s frame of continuous integration: {i_d*frame/Q:.3g} "
      f"(= {i_d*frame/Q/4.4e5:.0f} full wells of 440,000 e-)")
for n in (100, 1000, 10000):
    print(f"{n} gates of 100 ns: {n*i_d*100e-9/Q:.3g} dark electrons, duty {n*100e-9/frame:.2e} of a 1/30 s frame")

# depth slice of a gate: 2 * depth = c * gate
for t in (100e-9, 1e-6):
    print(f"gate {t*1e9:.0f} ns -> depth slice c t / 2 = {C*t/2:.1f} m")
