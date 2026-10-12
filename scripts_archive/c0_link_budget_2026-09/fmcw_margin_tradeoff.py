"""Designs that all reach 200 m at 10% in clear air: the price of short-range margin for FMCW."""
import importlib.util
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location(
    "nf", r"<scratch>\mech\fmcw_near_field_weather.py")
src = Path(spec.origin).read_text(encoding="utf-8")
ns = {}
exec(src.split("# ---- 1. classic check")[0], ns)  # load the functions only
L_dd, L_coh, kim_alpha, rmax, eph, RHO0 = ns["L_dd"], ns["L_coh"], ns["kim_alpha"], ns["rmax"], ns["eph"], ns["RHO0"]

R0 = 200.0
a940, a1550 = kim_alpha(940e-9, 23), kim_alpha(1550e-9, 23)
rows = []
# direct detection sized for 200 m
Ld = L_dd(R0, 25e-3, alpha=a940)
E_dd = 25 * eph(940e-9) / (0.185 * Ld)
rows.append(("SPAD 940 nm, 25 mm lens", E_dd, lambda r, a: L_dd(r, 25e-3, alpha=a), Ld, 940e-9))
for D in (25e-3, 22.1e-3, 16e-3, 13e-3, 10e-3, 7e-3):
    Ld = L_coh(R0, D, alpha=a1550)
    E = 30 * eph(1550e-9) / (0.25 * Ld)
    rows.append((f"FMCW 1550 nm, {D*1e3:.1f} mm", E, (lambda D: (lambda r, a: L_coh(r, D, alpha=a)))(D), Ld, 1550e-9))

print(f"{'design (all reach 200 m at 10%, clear air)':34s} {'E/pt':>8s} {'margin@10m':>10s} {'darkest':>8s} "
      f"{'R@3dB':>6s} {'R@6dB':>6s} {'R@V=1km':>8s} {'R@V=200m':>9s} {'R@V=50m':>8s}")
for name, E, fn, Ld, lam in rows:
    a = kim_alpha(lam, 23)
    m10 = 10 * np.log10(fn(10, a) / Ld)
    darkest = RHO0 * Ld / fn(0.5, a)
    r3 = rmax(lambda r: fn(r, a), Ld * 10 ** 0.3)
    r6 = rmax(lambda r: fn(r, a), Ld * 10 ** 0.6)
    fog = [rmax(lambda r: fn(r, kim_alpha(lam, v)), Ld) for v in (1, 0.2, 0.05)]
    print(f"{name:34s} {E*1e9:6.0f} nJ {m10:8.1f} dB {100*darkest:6.2f}% {r3:6.0f} {r6:6.0f} {fog[0]:8.0f} {fog[1]:9.0f} {fog[2]:8.0f}")
