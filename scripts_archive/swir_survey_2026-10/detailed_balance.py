"""Radiative (detailed-balance) floor of the dark saturation current of a photodiode from its own EQE spectrum.
J0 >= J0_rad >= q * integral( EQE(lambda) * Phi_bb(lambda, T) dlambda ), because the absorptance is at least the EQE
and the external radiative efficiency is at most 1. Phi_bb is the blackbody photon flux into a hemisphere through
one flat face (2 pi c / lambda^4 / (exp(hc / lambda k T) - 1)).
Usage: detailed_balance.py [<Source Data Fig. 3 workbook of Li et al. (.xlsx)>]
The SWIR Vision Systems spectra are typed in below, read by eye from Gregory et al., Proc. SPIE 12107, 1210705
(2022): Fig. 2 (eSWIR camera responsivity, A/W), Fig. 1 (standard sensor QE) and Fig. 3 (enhanced-QE test diode)."""
import math
import sys

H, C, KB, Q = 6.62607015e-34, 2.99792458e8, 1.380649e-23, 1.602176634e-19
T = 298.15


def phi_bb(lam_m):
    return 2 * math.pi * C / lam_m**4 / (math.exp(H * C / (lam_m * KB * T)) - 1.0)


def j0_rad(points):
    """points: list of (lambda_nm, EQE); trapezoid integral; returns A/cm^2."""
    s = 0.0
    for (l1, e1), (l2, e2) in zip(points, points[1:]):
        f1 = e1 * phi_bb(l1 * 1e-9)
        f2 = e2 * phi_bb(l2 * 1e-9)
        s += 0.5 * (f1 + f2) * (l2 - l1) * 1e-9
    return Q * s * 1e-4


# eSWIR camera responsivity (A/W) by eye, Fig. 2, 1,700-2,100 nm
eswir_r = [(1700, 0.028), (1720, 0.027), (1740, 0.025), (1760, 0.026), (1780, 0.029), (1800, 0.033),
           (1820, 0.040), (1840, 0.053), (1860, 0.071), (1880, 0.091), (1900, 0.097), (1920, 0.099),
           (1940, 0.082), (1960, 0.060), (1980, 0.039), (2000, 0.023), (2020, 0.013), (2040, 0.007),
           (2060, 0.004), (2080, 0.002), (2100, 0.0015)]
eswir = [(lam, r * 1239.84 / lam) for lam, r in eswir_r]
j = j0_rad(eswir)
print(f"eSWIR camera (to 2,100 nm, tail beyond set to zero): J0_rad >= {j:.3e} A/cm^2 = {j * 1e9:.2f} nA/cm^2")
tail = [(2100, eswir[-1][1]), (2120, eswir[-1][1] * 0.5), (2140, eswir[-1][1] * 0.25), (2160, eswir[-1][1] * 0.125)]
print(f"   with a halving tail per 20 nm beyond 2,100 nm: +{j0_rad(tail) * 1e9:.2f} nA/cm^2")
for jq in (5e-9, 10e-9):
    print(f"   quoted {jq * 1e9:.0f} nA/cm^2 would need ERE >= {j / jq:.2f} if it were J0")

# standard sensor QE by eye, Fig. 1
std = [(1400, 0.07), (1420, 0.10), (1440, 0.13), (1460, 0.145), (1480, 0.145), (1500, 0.14), (1520, 0.12),
       (1540, 0.10), (1560, 0.08), (1580, 0.06), (1600, 0.045), (1620, 0.03), (1640, 0.015), (1660, 0.005),
       (1680, 0.0), (1700, 0.0)]
j = j0_rad(std)
print(f"standard sensor: J0_rad >= {j:.3e} A/cm^2 ({j * 1e12:.1f} pA/cm^2); 5 nA/cm^2 -> ERE >= {j / 5e-9:.1e}")
enh = [(1500, 0.40), (1520, 0.37), (1540, 0.30), (1550, 0.26), (1560, 0.22), (1580, 0.14), (1600, 0.085),
       (1620, 0.05), (1640, 0.03), (1660, 0.015), (1680, 0.015), (1700, 0.02)]
j = j0_rad(enh)
print(f"enhanced-QE diode: J0_rad >= {j:.3e} A/cm^2 ({j * 1e12:.1f} pA/cm^2); 8 nA/cm^2 -> ERE >= {j / 8e-9:.1e}")

if len(sys.argv) > 1:
    import openpyxl
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
    rows = [r for r in wb["Fig 3e"].iter_rows(min_row=2, values_only=True) if r[0] is not None]
    li = [(float(a), max(0.0, float(b))) for a, b in rows[:]]
    j = j0_rad(li)
    print(f"Li et al. PbS (Source Data Fig. 3e, {li[0][0]:.0f}-{li[-1][0]:.0f} nm): J0_rad >= {j:.3e} A/cm^2 "
          f"= {j * 1e6:.2f} uA/cm^2; measured 123 uA/cm^2 at -0.1 V -> ERE <= ... J0_rad/J = {j / 123e-6:.3f}")
    print("   last EQE points:", li[-6:])
