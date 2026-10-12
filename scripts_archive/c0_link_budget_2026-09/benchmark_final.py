"""Final numbers for C0 subsection 10.8 (benchmark), with the report's current SPAD efficiency (live fraction 0.784)."""
import numpy as np

H, C, Q = 6.62607015e-34, 2.99792458e8, 1.602176634e-19
eph = lambda lam: H * C / lam  # noqa: E731
db = lambda x: 10 * np.log10(x)  # noqa: E731
LIVE = 0.784
ETA_SPAD = 0.5 * 0.37 * LIVE
print(f"report SPAD eta = {ETA_SPAD:.3f}")

# ToF inverse check: eta*A_rx = n E_ph pi R^2 / (rho E)
def eta_area(n, lam, R, rho, E):
    return n * eph(lam) * np.pi * R**2 / (rho * E)

# Sony ISSCC 2021
E_sony = 45 * 4.5e-9 / 63 * (721.76e-6 / 3.04e-6) / 168 * 63
ea = eta_area(25, 905e-9, 150.0, 0.1, E_sony)
print(f"Sony: E per point {E_sony * 1e9:.0f} nJ; eta*A = {ea * 1e4:.3f} cm2")
for eo in (0.5, 0.7):
    A = ea / (eo * 0.22 * LIVE)
    D = 2 * np.sqrt(A / np.pi)
    print(f"   optics {eo}: D = {D * 1e3:.1f} mm, f/{11.46e-3 / D:.2f}")
for name, P, px, fps, lam, R, rho in (("Toshiba", 50e-3, 240 * 96, 10, 905e-9, 200.0, 0.10),
                                      ("Toyota", 21e-3, 202 * 96, 10, 870e-9, 100.0, 0.09)):
    E = P / (px * fps)
    ea = eta_area(25, lam, R, rho, E)
    d = lambda eta: 2 * np.sqrt(ea / eta / np.pi) * 1e3  # noqa: E731
    print(f"{name}: E {E * 1e9:.0f} nJ; eta*A {ea * 1e4:.2f} cm2 (9-pixel: {ea / 9 * 1e4:.3f}); "
          f"D {d(0.10):.0f}-{d(0.05):.0f} mm at eta 0.10-0.05")
print(f"report default eta*A (25 mm): {ETA_SPAD * np.pi * 0.0125**2 * 1e4:.2f} cm2")

# Products with the report's SPAD model (n_req 25, eta 0.145)
for name, lam, R, rate in (("Ouster OS2-128 Rev7 (1024 x 10 Hz)", 865e-9, 200.0, 1024 * 10 * 128),
                           ("Hesai AT128", 905e-9, 210.0, 1.536e6),
                           ("Livox HAP", 905e-9, 150.0, 452e3)):
    out = []
    for D in (0.020, 0.030):
        E = 25 * eph(lam) * 4 * R**2 / (0.1 * ETA_SPAD * D**2)
        out.append(f"D {D * 1e3:.0f} mm: {E * 1e9:.0f} nJ, {E * rate:.2f} W")
    print(f"{name} ({rate:,.0f} pts/s): " + "; ".join(out))
# reflectance scaling in sunlight: Ouster 200 m @10%, 350 m @80%
for name, r1, p1, r2, p2 in (("Ouster OS2", 200, 0.10, 350, 0.80), ("Sony", 150, 0.10, 200, 0.95)):
    print(f"{name}: range ratio {r2 / r1:.2f} for reflectance x{p2 / p1:.1f}: exponent {np.log(r2 / r1) / np.log(p2 / p1):.2f} "
          f"(signal-limited 0.50 -> {(p2 / p1) ** 0.5:.2f}; background-limited 0.25 -> {(p2 / p1) ** 0.25:.2f})")

# FMCW: Waymo, Pointcloud, indie, Wang, FS-4S (as before)
lam = 1550e-9
w0 = 10e-3
zr = np.pi * w0**2 / lam
L = 0.05 * lam**2 / (2 * np.pi**2 * w0**2 * (1 + (250 / zr) ** 2))
print(f"Waymo: z_R {zr:.1f} m, L {db(L):.1f} dB, photons/point {0.52e-6 / eph(lam) * L:.0f}")
lam13, w0p, zf, P, T = 1310e-9, 1.31e-3, 11.1, 178e-6, 32e-6
zrp = np.pi * w0p**2 / lam13
ww = w0p**2 * (1 + ((7.2 - zf) / zrp) ** 2)
prx = 0.23 * 0.5 * lam13**2 / (2 * np.pi**2 * ww)
n = 0.95 * P * prx * T / Q
pen = 1 / (1 + 1 / 0.62**2)
print(f"Pointcloud: w(7.2) {np.sqrt(ww) * 1e3:.2f} mm; P_RX/P_TX {prx:.2e}; N {n:.0f}; N_eff {n * pen:.1f}; 2N units {2 * n * pen:.1f} "
      f"vs 74.7 -> {db(2 * n * pen / 74.7):+.1f} dB; eff eta {0.23 * 0.95 * H * C / (Q * lam13) * pen:.3f}")
