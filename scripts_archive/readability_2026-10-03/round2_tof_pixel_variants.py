"""Round 2: effect of the ToF macro-pixel field (0.1 x 0.05 deg against 0.05 x 0.05 deg) on the §C7a ToF model.

Reproduces the background, dead-time and energy equations of build/figures/fmcw_tof_system_budget.py for the
2026 and 2032 ToF cases, and the ideal photon-counting requirement of §C0 subsection 10.3 (2,000 bins, at most
1e-3 false points per point, i.e. 5e-7 per bin, 90 % detection). Two ways of setting n_req are compared:
(A) keep the model's n_req triplets (20, 25, 35) / (20, 25, 30); (B) scale them by the change of the ideal
requirement in the central case, which keeps the stated x1.45 implementation margin.
Usage: python round2_tof_pixel_variants.py
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import poisson

H, C = 6.62607015e-34, 2.99792458e8
R, RHO, A = 200.0, 0.10, np.pi * 0.0125 ** 2
P_BIN = 1e-3 / 2000
TOF = {"2026": dict(pde=0.37, n_req=(20, 25, 35), wpe=(0.30, 0.20, 0.15), e_fixed=(20e-9, 40e-9, 60e-9),
                    e_event=(4e-12, 5e-12, 7e-12)),
       "2032": dict(pde=0.45, n_req=(20, 25, 30), wpe=(0.35, 0.25, 0.20), e_fixed=(10e-9, 20e-9, 35e-9),
                    e_event=(2.5e-12, 3.5e-12, 5e-12))}
SCENE, T_LISTEN, E_PH, OPTICS = (0.0, 0.5, 1.0), 20.8e-6, H * C / 940e-9, 0.5


def ideal(b):
    n = 1
    while poisson.sf(n - 1, b) > P_BIN:
        n += 1
    return brentq(lambda s: poisson.sf(n - 1, s + b) - 0.9, 0.0, 300.0), n


def model(bg_per_pde, year, k, n_scale=1.0):
    s = TOF[year]
    r_bg = bg_per_pde * s["pde"] * SCENE[k]
    f_dead = 1 - np.exp(-r_bg / 9 * 6e-9)
    b = r_bg * 1e-9 * 10 * (1 - f_dead)
    n_req = s["n_req"][k] * n_scale
    eta = OPTICS * s["pde"] * (1 - f_dead)
    e_opt = n_req * E_PH * np.pi * R ** 2 / (RHO * A * eta)
    n_ev = r_bg * T_LISTEN * (1 - f_dead) + n_req
    e_el = s["e_fixed"][k] + n_ev * s["e_event"][k]
    e_tot = e_opt / s["wpe"][k] + e_el
    return dict(r_bg=r_bg, f_dead=f_dead, live=1 - f_dead, b=b, eta=eta, n_req=n_req, e_opt=e_opt, n_ev=n_ev,
                e_el=e_el, e_tot=e_tot)


OLD, NEW = 5.93e8 / 0.3, 2.965e8 / 0.3  # counts/s per unit PDE for a rho = 0.9 full-sun scene, §C6(d)
for year in ("2026", "2032"):
    o, n = model(OLD, year, 1), model(NEW, year, 1)
    i_o, i_n = ideal(o["b"]), ideal(n["b"])
    scale = i_n[0] / i_o[0]
    nb = model(NEW, year, 1, n_scale=scale)
    print(f"--- ToF {year}, central (scene 0.5)")
    print(f"  r_bg {o['r_bg']:.3g} -> {n['r_bg']:.3g} /s; live {o['live']:.3f} -> {n['live']:.3f}; eta {o['eta']:.4f} -> {n['eta']:.4f}")
    print(f"  b per 1 ns bin {o['b']:.3f} -> {n['b']:.3f}; ideal {i_o[0]:.2f} (n_th {i_o[1]}) -> {i_n[0]:.2f} (n_th {i_n[1]}); scale {scale:.3f}")
    for lab, m in (("old", o), ("new A (n_req kept)", n), ("new B (margin kept)", nb)):
        print(f"  {lab:22s} n_req {m['n_req']:.1f}  E_opt {m['e_opt']*1e9:6.1f} nJ  events {m['n_ev']:6.0f}  "
              f"E_el {m['e_el']*1e9:5.1f} nJ  total {m['e_tot']*1e9:6.1f} nJ")
    for k, lab in ((0, "low (night)"), (2, "high (full sun)")):
        o2, n2 = model(OLD, year, k), model(NEW, year, k)
        print(f"  {lab}: r_bg {o2['r_bg']:.3g} -> {n2['r_bg']:.3g}; live {o2['live']:.3f} -> {n2['live']:.3f}; "
              f"b {o2['b']:.2f} -> {n2['b']:.2f}; total (A) {o2['e_tot']*1e9:.0f} -> {n2['e_tot']*1e9:.0f} nJ")
