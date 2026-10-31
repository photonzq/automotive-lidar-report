"""Check the Fig. 3 Source Data of Li et al. (Nature 2026, doi:10.1038/s41586-026-11222-y).
Usage: source_data_check.py <Source Data Fig. 3 workbook (.xlsx)>
Prints the dark and light J-V near zero bias, the zero-bias slope (R0*A), J at -0.1 V,
the EQE at selected wavelengths, the D* curves of Fig. 3f, and the noise implied by D*(lambda)."""
import math
import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)


def cols(sheet, first_row=2):
    rows = [r for r in wb[sheet].iter_rows(min_row=first_row, values_only=True)]
    return list(zip(*rows))


# Fig. 3b: two (V, J) column pairs
c = cols("Fig 3b")
pairs = {"pair1": (c[0], c[1]), "pair2": (c[2], c[3])}
for name, (v, j) in pairs.items():
    data = [(float(a), float(b)) for a, b in zip(v, j) if a is not None and b is not None]
    print(f"== Fig 3b {name}: {len(data)} points, V from {data[0][0]} to {data[-1][0]}")
    for vv, jj in data:
        if abs(vv) <= 0.12 + 1e-9 or abs(vv + 0.75) < 1e-6 or abs(vv + 0.5) < 1e-6 or abs(vv + 1) < 1e-6:
            print(f"   V={vv:+.3f}  J={jj:.4e}")
    jmin = min(data, key=lambda t: abs(t[1]))
    print(f"   min |J| at V={jmin[0]:+.3f} (J={jmin[1]:.3e})")
    near = [(vv, jj) for vv, jj in data if abs(vv) <= 0.0201]
    if len(near) >= 3:
        # signed J is not stored (magnitudes); use symmetric points around 0 to get the slope of |J|
        print("   points used for the zero-bias slope:", near)

# Fig. 3e: EQE
v = cols("Fig 3e")
eqe = {int(round(float(a))): float(b) for a, b in zip(v[0], v[1]) if a is not None}
for lam in (1300, 1550, 2000, 2500, 2640, 2700):
    if lam in eqe:
        print(f"EQE({lam} nm) = {eqe[lam]:.4f}  R = {eqe[lam] * lam / 1239.84:.4f} A/W")

# Fig. 3f: literature, ours, extended-SWIR InGaAs
f = cols("Fig 3f")
ours = [(float(a), float(b)) for a, b in zip(f[2], f[3]) if a is not None and b is not None]
ing = [(float(a), float(b)) for a, b in zip(f[4], f[5]) if a is not None and b is not None]
lit = [(float(a), float(b)) for a, b in zip(f[0], f[1]) if a is not None and b is not None]
print("literature points:", lit)
pk = max(ing, key=lambda t: t[1])
print(f"InGaAs curve: {len(ing)} points, {ing[0][0]}-{ing[-1][0]} nm, peak {pk[1]:.3e} at {pk[0]} nm")
for lam, d in ing:
    if int(lam) in (1550, 2000, 2300, 2400, 2450, 2500, 2550, 2600):
        print(f"   InGaAs D*({lam:.0f}) = {d:.3e}")
pk = max(ours, key=lambda t: t[1])
print(f"PbS curve: {len(ours)} points, {ours[0][0]}-{ours[-1][0]} nm, peak {pk[1]:.3e} at {pk[0]} nm")
area = 0.01  # cm^2, 1 mm^2 device
for lam, d in ours:
    li = int(round(lam))
    if li in (1300, 1550, 2000, 2500, 2640, 2700) and li in eqe:
        r = eqe[li] * li / 1239.84
        print(f"   PbS D*({li}) = {d:.3e}; with EQE {eqe[li]:.3f}, implied i_n = R*sqrt(A)/D* = {r * math.sqrt(area) / d:.3e} A/Hz^0.5")

# Fig. 3c: photocurrent vs intensity
c3 = cols("Fig 3c")
for a, b in zip(c3[0], c3[1]):
    if a is None:
        continue
    print(f"Fig 3c: I={float(a):.2e} W/cm2, photocurrent column={float(b):.3e}; R if column is A and area 1 mm2: {float(b) / (float(a) * area):.3f} A/W")
