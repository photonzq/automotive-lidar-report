"""FMCW near-field flattening: check against the classic coherent-lidar hard-target equation, and its
consequences for fixed losses, dark targets and fog. Same model and detection levels as link_budget_scaling.py."""
import numpy as np
from scipy.optimize import brentq

h, c = 6.62607015e-34, 2.99792458e8
T_TRUNC = 1 - np.exp(-2 * (0.5 / 0.45) ** 2)
RHO0 = 0.10


def eph(lam):
    return h * c / lam


def kim_alpha(lam, V_km):
    """Kim model extinction (1/m)."""
    if V_km > 50:
        q = 1.6
    elif V_km > 6:
        q = 1.3
    elif V_km > 1:
        q = 0.16 * V_km + 0.34
    elif V_km > 0.5:
        q = V_km - 0.5
    else:
        q = 0.0
    return (3.912 / (V_km * 1e3)) * (lam / 550e-9) ** (-q)


def L_dd(R, D, rho=RHO0, alpha=0.0):
    return rho * D**2 / (4 * R**2) * np.exp(-2 * alpha * R)


def L_coh(R, D, lam=1550e-9, rho=RHO0, alpha=0.0):
    w0 = 0.45 * D
    zr = np.pi * w0**2 / lam
    w2 = w0**2 * (1 + (R / zr) ** 2)
    return rho * T_TRUNC**2 * lam**2 / (2 * np.pi**2 * w2) * np.exp(-2 * alpha * R)


def L_det(n, lam, eta, E):
    return n * eph(lam) / (eta * E)


def rmax(fn, target, lo=0.05, hi=5e4):
    if fn(lo) < target:
        return 0.0
    if fn(hi) > target:
        return np.inf
    return brentq(lambda r: np.log(fn(r)) - np.log(target), lo, hi)


# ---- 1. classic check (Rye 1979; Frehlich & Kavaya 1991): collimated monostatic, uniform aperture D:
# P ∝ D^2 / {R^2 [1 + (pi D^2/(4 lambda R))^2]}  ->  flat for R << pi D^2/(4 lambda)
lam = 1550e-9
for D in (10e-3, 25e-3, 50e-3):
    Rt = np.pi * D**2 / (4 * lam)
    zr = np.pi * (0.45 * D) ** 2 / lam
    classic = [D**2 / (R**2 * (1 + (np.pi * D**2 / (4 * lam * R)) ** 2)) for R in (10, 100, 200, 500)]
    model = [L_coh(R, D) / RHO0 for R in (10, 100, 200, 500)]
    print(f"D={D*1e3:.0f} mm: classic transition piD^2/4lambda = {Rt:.0f} m, Gaussian z_R = {zr:.0f} m; "
          f"shape 10/100/200/500 m classic {[round(10*np.log10(x/classic[0]),1) for x in classic]} dB, "
          f"model {[round(10*np.log10(x/model[0]),1) for x in model]} dB")

# designs (clear-air detection levels as in the report)
SPAD = dict(n=25, lam=940e-9, eta=0.185, E=0.1e-6, D=25e-3)
FM = dict(n=30, lam=1550e-9, eta=0.25, E=0.3e-6)
Ld_spad = L_det(SPAD["n"], SPAD["lam"], SPAD["eta"], SPAD["E"])
Ld_fm = L_det(FM["n"], FM["lam"], FM["eta"], FM["E"])
a_clear940, a_clear1550 = kim_alpha(940e-9, 23), kim_alpha(1550e-9, 23)
R_dd = rmax(lambda r: L_dd(r, 25e-3, alpha=a_clear940), Ld_spad)
R_fm25 = rmax(lambda r: L_coh(r, 25e-3, alpha=a_clear1550), Ld_fm)
R_fm10 = rmax(lambda r: L_coh(r, 10e-3, alpha=a_clear1550), Ld_fm)
Dopt200 = np.sqrt(lam * 200 / np.pi) / 0.45
R_fmopt = rmax(lambda r: L_coh(r, Dopt200, alpha=a_clear1550), Ld_fm)
# DD with energy scaled so that its clear-air range equals the FMCW 25 mm design (apples to apples)
Ld_spad_m = L_dd(R_fm25, 25e-3, alpha=a_clear940)
E_match = SPAD["n"] * eph(940e-9) / (SPAD["eta"] * Ld_spad_m)
print(f"\nclear-air ranges: SPAD 25 mm {R_dd:.0f} m; FMCW 25 mm {R_fm25:.0f} m; FMCW 10 mm {R_fm10:.0f} m; "
      f"FMCW D_opt(200 m)={Dopt200*1e3:.1f} mm {R_fmopt:.0f} m; SPAD energy for {R_fm25:.0f} m = {E_match*1e9:.0f} nJ")

designs = [
    ("SPAD 940 nm, 25 mm, 0.1 uJ", lambda r, a: L_dd(r, 25e-3, alpha=a), Ld_spad, 940e-9),
    (f"SPAD 940 nm, 25 mm, {E_match*1e9:.0f} nJ (same clear range as FMCW 25 mm)", lambda r, a: L_dd(r, 25e-3, alpha=a), Ld_spad_m, 940e-9),
    ("FMCW 1550 nm, 25 mm, 0.3 uJ", lambda r, a: L_coh(r, 25e-3, alpha=a), Ld_fm, 1550e-9),
    ("FMCW 1550 nm, 22 mm (optimum for 200 m), 0.3 uJ", lambda r, a: L_coh(r, Dopt200, alpha=a), Ld_fm, 1550e-9),
    ("FMCW 1550 nm, 10 mm, 0.3 uJ", lambda r, a: L_coh(r, 10e-3, alpha=a), Ld_fm, 1550e-9),
]

# ---- 2. margin profile: how far above the detection level each design sits at short range
print("\nmargin above detection level (dB), clear air:")
for name, fn, Ld, lam_ in designs:
    a = kim_alpha(lam_, 23)
    print(f"  {name:60s}", "  ".join(f"{R:>3d} m: {10*np.log10(fn(R, a)/Ld):5.1f}" for R in (10, 20, 50, 100, 150)))

# ---- 3. fixed extra loss X (dirty or wet window, laser ageing): range vs X
print("\nrange (m) with an extra fixed two-way loss X, clear air:")
for name, fn, Ld, lam_ in designs:
    a = kim_alpha(lam_, 23)
    print(f"  {name:60s}", "  ".join(f"{X} dB: {rmax(lambda r: fn(r, a), Ld*10**(X/10)):4.0f}" for X in (0, 1, 2, 3, 6, 10)))

# ---- 4. reflectivity: darkest detectable target at any range, and range at 5% and 2%
print("\ndark targets (clear air):")
for name, fn, Ld, lam_ in designs:
    a = kim_alpha(lam_, 23)
    rho_min = RHO0 * Ld / fn(0.5, a)  # the best (shortest) range
    r5 = rmax(lambda r: fn(r, a) * 0.05 / RHO0, Ld)
    r2 = rmax(lambda r: fn(r, a) * 0.02 / RHO0, Ld)
    print(f"  {name:60s} darkest detectable (at ~0.5 m) {100*rho_min:5.2f}%; range at 5%: {r5:4.0f} m; at 2%: {r2:4.0f} m")

# ---- 5. fog: single-scattering reach vs visibility (Kim model)
print("\nreach (m) vs visibility, single scattering, 10% target:")
Vs = [23, 5, 2, 1, 0.5, 0.2, 0.1, 0.05]
print("  " + " " * 60, "  ".join(f"V={v:g} km" for v in Vs))
for name, fn, Ld, lam_ in designs:
    row = []
    for v in Vs:
        a = kim_alpha(lam_, v)
        row.append(f"{rmax(lambda r: fn(r, a), Ld):8.0f}")
    print(f"  {name:60s}", "  ".join(row))
print("  alpha 940/1550 (1/km):", [(v, round(kim_alpha(940e-9, v)*1e3, 2), round(kim_alpha(1550e-9, v)*1e3, 2)) for v in Vs])

# ---- 6. fog backscatter: per-bin clutter-to-target ratio and the near-range return
S_lidar = 18.0  # fog lidar ratio alpha/beta (sr), water droplets [typical value]
dR = 0.15
for v in (0.2, 0.05):
    a = kim_alpha(1550e-9, v)
    beta = a / S_lidar
    print(f"\nfog V={v*1e3:.0f} m: alpha={a*1e3:.1f}/km, beta={beta:.2e} /m/sr; per-bin fog/target at the same range "
          f"= pi*beta*dR/rho = {np.pi*beta*dR/RHO0:.3f} ({10*np.log10(np.pi*beta*dR/RHO0):.1f} dB), identical for both")
    # DD near-range fog return per 15 cm bin, relative to a 10% target at 50 m, for r = 2, 5, 10, 20 m (overlap = 1)
    A = np.pi * 0.0125**2
    tgt50 = RHO0 * A / (np.pi * 50**2) * np.exp(-2 * a * 50)
    dd = {r: beta * dR * A / r**2 * np.exp(-2 * a * r) / tgt50 for r in (2, 5, 10, 20)}
    # coherent: fog per bin = beta*dR*lambda^2*(t^2/2)/(pi w^2)*exp(-2 alpha r); target = (rho/pi)*... same geometry
    def coh_bin(r, D=25e-3):
        w0 = 0.45 * D
        zr = np.pi * w0**2 / 1550e-9
        w2 = w0**2 * (1 + (r / zr) ** 2)
        return beta * dR * (1550e-9) ** 2 * T_TRUNC**2 / (2 * np.pi * w2) * np.exp(-2 * a * r)
    tgt50c = L_coh(50, 25e-3, alpha=a)
    coh = {r: coh_bin(r) / tgt50c for r in (2, 5, 10, 20)}
    print("  fog return per bin at r, relative to a 10% target at 50 m:  DD",
          {r: f"{10*np.log10(x):+.1f} dB" for r, x in dd.items()}, "| FMCW 25 mm",
          {r: f"{10*np.log10(x):+.1f} dB" for r, x in coh.items()})
