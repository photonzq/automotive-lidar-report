"""ASTM G173-03 solar spectral irradiance at lidar wavelengths.

Reads the ASTM G173-03 reference spectra (the CSV inside ``astmg173.zip``
published on the National Laboratory of the Rockies, formerly NREL, page
"Reference Air Mass 1.5 Spectra": https://www.nlr.gov/grid/solar-resource/spectra-am1.5 ,
file https://www.nlr.gov/media/docs/libraries/grid/zip/astmg173.zip ) and prints,
for 905, 940 and 1,550 nm:

* the tabulated value at exactly that wavelength (extraterrestrial, global tilt,
  direct + circumsolar), in W m^-2 nm^-1;
* the +/-10 nm average, computed two ways: (a) the arithmetic mean of the 21
  tabulated 1-nm values from lambda-10 to lambda+10 nm inclusive, and (b) the
  trapezoidal integral over [lambda-10, lambda+10] divided by 20 nm;
* the ground/extraterrestrial ratio of the band averages;
* the spectral photon flux of the global-tilt band average,
  Phi = E_lambda * lambda / (h c), in photons s^-1 m^-2 nm^-1;
* the neighbouring tabulated values 900-910 nm (the 905 nm feature).

Usage:  python astm_g173_lidar_bands.py [path/to/astmg173.zip or ASTMG173.csv]
Default input: ``astmg173.zip`` in the current folder.
"""
import io
import sys
import zipfile

import numpy as np

H = 6.62607015e-34  # Planck constant, J s
C = 2.99792458e8    # speed of light, m/s


def load(path):
    """Return (wavelength_nm, etr, global_tilt, direct) arrays from the ASTM file."""
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            text = z.read("ASTMG173.csv").decode("latin-1")
    else:
        with open(path, encoding="latin-1") as f:
            text = f.read()
    rows = []
    for line in text.splitlines()[2:]:
        parts = [p for p in line.split(",") if p.strip()]
        if len(parts) >= 4:
            rows.append([float(p) for p in parts[:4]])
    a = np.array(rows)
    return a[:, 0], a[:, 1], a[:, 2], a[:, 3]


def band(wl, y, lo, hi):
    """Arithmetic mean of tabulated samples in [lo, hi] and trapezoid mean."""
    m = (wl >= lo - 1e-9) & (wl <= hi + 1e-9)
    mean_samples = y[m].mean()
    trap = np.trapezoid(y[m], wl[m]) / (hi - lo)
    return mean_samples, trap, int(m.sum())


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "astmg173.zip"
    wl, etr, gt, dr = load(path)
    print(f"{len(wl)} rows, {wl[0]}-{wl[-1]} nm")
    # integrated global tilt as a sanity check (should be ~1000.4 W/m2)
    print(f"Integrated global tilt 280-4000 nm: {np.trapezoid(gt, wl):.1f} W/m2;"
          f" ETR: {np.trapezoid(etr, wl):.1f} W/m2; direct: {np.trapezoid(dr, wl):.1f} W/m2")
    print()
    hdr = ("lambda", "ETR", "GT exact", "DC exact", "GT mean21", "GT trap",
           "ETR mean21", "GT/ETR", "photons/(s m2 nm) GT mean21")
    print(" | ".join(hdr))
    out = {}
    for lam in (905.0, 940.0, 1550.0):
        i = int(np.argmin(np.abs(wl - lam)))
        gm, gtr, n = band(wl, gt, lam - 10, lam + 10)
        em, etrap, _ = band(wl, etr, lam - 10, lam + 10)
        dm, dtr, _ = band(wl, dr, lam - 10, lam + 10)
        phot = gm * lam * 1e-9 / (H * C)
        out[lam] = (gm, phot)
        print(f"{lam:.0f} | {etr[i]:.4f} | {gt[i]:.4f} | {dr[i]:.4f} | {gm:.4f} | {gtr:.4f} |"
              f" {em:.4f} | {gm/em:.3f} | {phot:.3e}  (n={n}; direct mean {dm:.4f};"
              f" ETR trap {etrap:.4f}; GT/ETR trap {gtr/etrap:.3f})")
    print()
    p905, p940, p1550 = out[905.0][1], out[940.0][1], out[1550.0][1]
    print(f"photon ratios (band means): 940/905 = {p940/p905:.3f}; 940/1550 = {p940/p1550:.3f};"
          f" 1550/905 = {p1550/p905:.3f}")
    print()
    print("Tabulated global tilt and ETR, 895-950 nm:")
    for lam in range(895, 951):
        i = int(np.argmin(np.abs(wl - lam)))
        print(f"  {wl[i]:.0f} nm: GT {gt[i]:.4f}  ETR {etr[i]:.4f}  DC {dr[i]:.4f}")
    print("Tabulated global tilt, 1540-1560 nm:")
    for lam in range(1540, 1561):
        i = int(np.argmin(np.abs(wl - lam)))
        print(f"  {wl[i]:.0f} nm: GT {gt[i]:.4f}  ETR {etr[i]:.4f}")


if __name__ == "__main__":
    main()
