"""Silicon absorption coefficient at 905 and 940 nm from two tabulations.

Inputs (both public):
1. Green 2008 (M. A. Green, "Self-consistent optical parameters of intrinsic
   silicon at 300 K including temperature coefficients", Sol. Energy Mater.
   Sol. Cells 92, 1305-1310 (2008), doi:10.1016/j.solmat.2008.06.009), as
   transcribed (n, k at 10 nm steps) in the CC0 refractiveindex.info database:
   https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/master/database/data/main/Si/nk/Green-2008.yml
   The absorption coefficient is alpha = 4 pi k / lambda.
2. Green & Keevers 1995 (Prog. Photovolt. 3, 189-192), tabulated alpha in
   cm^-1 on PVEducation (OpticalPropertiesOfSilicon.xlsx):
   https://www.pveducation.org/sites/default/files/PVCDROM/Appendices/OpticalPropertiesOfSilicon.xlsx

For 905 nm the tables have no entry, so alpha is interpolated linearly in
log(alpha) between 900 and 910 nm (absorption in this indirect-gap tail is
close to exponential in wavelength over 10 nm). The absorption length 1/alpha
and the single-pass absorbed fraction 1 - exp(-alpha d) for a few silicon
thicknesses d are printed.

Usage: python si_absorption_905_940.py [Green-2008.yml] [OpticalPropertiesOfSilicon.xlsx]
"""
import math
import sys


def read_green2008(path):
    """Return dict wavelength_nm -> alpha_cm from the refractiveindex.info YAML (n, k)."""
    out = {}
    in_data = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("data: |"):
                in_data = True
                continue
            if in_data:
                parts = line.split()
                if len(parts) != 3:
                    if out:
                        break
                    continue
                lam_um, _n, k = (float(p) for p in parts)
                lam_cm = lam_um * 1e-4
                out[round(lam_um * 1000)] = 4 * math.pi * k / lam_cm
    return out


def read_gk1995(path):
    """Return dict wavelength_nm -> alpha_cm from the PVEducation workbook."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.worksheets[0]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row and isinstance(row[0], (int, float)) and isinstance(row[1], (int, float)):
            out[int(row[0])] = float(row[1])
    return out


def loginterp(table, lam):
    """Log-linear interpolation of alpha between the bracketing 10 nm entries."""
    if lam in table:
        return table[lam]
    lo = (lam // 10) * 10
    hi = lo + 10
    t = (lam - lo) / 10.0
    return math.exp((1 - t) * math.log(table[lo]) + t * math.log(table[hi]))


def main():
    g08 = read_green2008(sys.argv[1] if len(sys.argv) > 1 else "Si_Green-2008_refractiveindexinfo.yml")
    gk95 = read_gk1995(sys.argv[2] if len(sys.argv) > 2 else "pveducation_OpticalPropertiesOfSilicon.xlsx")
    print("Tabulated alpha (cm^-1): lambda | Green 2008 (4 pi k / lambda) | Green & Keevers 1995")
    for lam in range(880, 961, 10):
        print(f"  {lam} nm | {g08[lam]:7.1f} | {gk95[lam]:7.1f}")
    print()
    for lam in (905, 940):
        for name, tab in (("Green 2008", g08), ("Green & Keevers 1995", gk95)):
            a = loginterp(tab, lam)
            L_um = 1e4 / a
            fr = ", ".join(f"{d} um: {1 - math.exp(-a * d * 1e-4):.1%}" for d in (3, 10, 30, 100))
            print(f"{lam} nm, {name}: alpha = {a:.0f} cm^-1, 1/alpha = {L_um:.1f} um; "
                  f"single-pass absorption {fr}")
    print()
    print("Report values for comparison: 905 nm 3.1e2 cm^-1 (32 um); 940 nm 1.8e2 cm^-1 (56 um)")


if __name__ == "__main__":
    main()
