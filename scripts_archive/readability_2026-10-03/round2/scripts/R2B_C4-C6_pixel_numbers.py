"""Round 2, sections C3b-C6 and C8: numbers that follow from the 0.05 x 0.05 deg ToF macro-pixel.

Recomputes, from the report's own equations, every per-pixel sunlight rate, dead and live fraction,
coincidence rate and quoted ratio that changes in sections C3b, C4, C4b, C4c, C4d, C5a and C6 when the
macro-pixel field is 0.05 x 0.05 deg (the IMX479 grid, 2,400 x 520 over 120 x 26 deg) instead of
0.1 x 0.05 deg.
- C6(d): Eq. (81) with the model's irradiances (0.75 W m^-2 nm^-1 at 905 nm, 0.39 at 940 nm, the midpoints of
  the exact and +-10 nm ASTM G173 values), 25 mm aperture, optics 0.5, PDE 0.3, rho 0.9; Eq. (82) dead fractions
  with nine SPADs and 6 ns.
- C6(d'): Eq. (84) accidental coincidences, nine SPADs, 1 ns window.
- C4c subsection 2: Eq. (67) with the +-10 nm band averages (photon fluxes of the C4c table), and the
  count-rate headroom of subsection 3.
- C6(f): column avalanche power, 520 macro-pixels, 1.6-3.9 pJ per avalanche.
- C4b: SiPM microcell dead fraction (1,000 cells, 30 ns) and the 3x3 macro-pixel range.
- C5a: background events per point over the 20.8 us listen; C4d: FMCW/ToF energy ratio from the model tables.
Usage: python R2B_C4-C6_pixel_numbers.py
"""
import numpy as np
from math import comb

H, C = 6.62607015e-34, 2.99792458e8
DEG = np.pi / 180
A_RX = np.pi * 0.0125 ** 2
OPT, PDE, RHO, TAU = 0.5, 0.3, 0.9, 6e-9
OM_NEW = (0.05 * DEG) ** 2
OM_OLD = (0.1 * DEG) * (0.05 * DEG)


def eph(lam_nm):
    return H * C / (lam_nm * 1e-9)


def r_bg81(e_sun, lam_nm, dlam, om, pde=PDE, rho=RHO):
    """Eq. (81): background counts/s per macro-pixel."""
    return e_sun * dlam / eph(lam_nm) * rho / np.pi * om * A_RX * OPT * pde


def dead(r_mp, tau=TAU, n=9):
    x = r_mp / n * tau
    return x, 1 - np.exp(-x), x / (1 + x)


print(f"Omega_pix new {OM_NEW:.4e} sr (8.727e-4 rad squared), old {OM_OLD:.4e} sr; A_rx {A_RX:.4e} m^2")
print(f"E_ph 905 {eph(905):.4e} J, 940 {eph(940):.4e} J, 1550 {eph(1550):.4e} J")
print(f"photon flux at 0.75 W/m2/nm, 905 nm: {0.75/eph(905):.4e}; at 0.39, 940 nm: {0.39/eph(940):.4e}")

print("\n--- C6(d) table (model irradiances, PDE 0.3, rho 0.9) ---")
rows = {"905/20": (0.75, 905, 20), "905/40": (0.75, 905, 40), "940/10": (0.39, 940, 10)}
rb = {}
for k, (e, lam, dl) in rows.items():
    new, old = r_bg81(e, lam, dl, OM_NEW), r_bg81(e, lam, dl, OM_OLD)
    rb[k] = new
    x, fp, fn = dead(new)
    xo, fpo, fno = dead(old)
    print(f"{k}: r_bg {old:.4e} -> {new:.4e}; r per SPAD {new/9:.4e}; r tau {xo:.4f} -> {x:.4f}; "
          f"paralyzable {fpo:.4f} -> {fp:.4f}; non-paralyzable {fno:.4f} -> {fn:.4f}")
print(f"check with rounded inputs, 905/20: {3.4e18*20*(0.9/np.pi)*7.62e-7*4.91e-4*0.5*0.3:.4e}")
print(f"check with rounded inputs, 940/10: {1.85e18*10*(0.9/np.pi)*7.62e-7*4.91e-4*0.5*0.3:.4e}")
print(f"band averages alone (0.693, 0.303) would be lower by {1-0.693/0.75:.3f} and {1-0.303/0.39:.3f}")
print(f"model irradiance / band average: 905 {0.75/0.693:.3f}, 940 {0.39/0.303:.3f}; exact / band average 940 {0.472/0.303:.3f}")

print("\n--- C6(d) 'In the ToF energy model' (PDE 0.37) ---")
full = rb["940/10"] * 0.37 / 0.3
for lab, r in (("full sun", full), ("central (half)", full / 2)):
    x, fp, fn = dead(r)
    print(f"{lab}: r_bg {r:.4e}; r tau {x:.5f}; dead {fp:.4f}; live {1-fp:.4f}; recorded {r*(1-fp):.4e}")
live_c = 1 - dead(full / 2)[1]
print(f"signal efficiency 0.5 x 0.37 x {live_c:.4f} = {0.5*0.37*live_c:.4f}")

print("\n--- C6(d') coincidence table (N = 9, tau_c = 1 ns) ---")
r1 = rb["940/10"] * 2 * (0.1 / 0.9)
for lab, r_mp in (("940/20, rho 0.1", r1), ("940/10, rho 0.9", rb["940/10"]), ("905/20, rho 0.9", rb["905/20"])):
    r = r_mp / 9
    acc = {n: comb(9, n) * n * r ** n * 1e-9 ** (n - 1) for n in (2, 3, 4)}
    print(f"{lab}: r_bg {r_mp:.4e}, r {r:.4e}, r tau_c {r*1e-9:.4f}; singles {r_mp:.3e}; "
          + "; ".join(f"{n}-fold {acc[n]:.3e} (x{r_mp/acc[n]:.1f})" for n in (2, 3, 4)))
r = 1.22e8
print(f"905 row from rounded r = 1.22e8: 2-fold {72*r**2*1e-9:.4e}, 3-fold {252*r**3*1e-18:.4e}, 4-fold {504*r**4*1e-27:.4e}")
r = 7.32e6
print(f"row 1 from rounded r = 7.32e6: 2-fold {72*r**2*1e-9:.4e}, 3-fold {252*r**3*1e-18:.4e}, 4-fold {504*r**4*1e-27:.4e}")
r = 3.29e7
print(f"row 2 from rounded r = 3.29e7: 2-fold {72*r**2*1e-9:.4e}, 3-fold {252*r**3*1e-18:.4e}, 4-fold {504*r**4*1e-27:.4e}")

print("\n--- C6(d') active recharge at 940/10 (r per SPAD = r_bg/9) ---")
r = rb["940/10"] / 9
for t in (3e-9, 6e-9, 20e-9):
    x = r * t
    print(f"tau {t*1e9:.0f} ns: r tau {x:.4f}; paralyzable {1-np.exp(-x):.4f}; non-paralyzable {x/(1+x):.4f}")

print("\n--- C6(f) column avalanche power (520 macro-pixels) ---")
for lab, r in (("central", full / 2), ("full sun", full)):
    rec = r * (1 - dead(r)[1])
    print(f"{lab}: recorded {rec:.4e}/s per macro-pixel; P = {520*rec*1.6e-12:.4f} W at 1.6 pJ, {520*rec*3.9e-12:.4f} W at 3.9 pJ")
print(f"energy per avalanche: 20 fF {20e-15*3.3*23.8*1e12:.3f} pJ, 50 fF {50e-15*3.3*23.8*1e12:.3f} pJ")

print("\n--- C4b ---")
x = rb["905/20"] / 1000 * 30e-9
print(f"SiPM cell at 905/20: {rb['905/20']/1000:.4e}/s; r tau {x:.4f}; dead {1-np.exp(-x):.4f}")
for lab, r_mp in (("940/20 rho 0.1", r1), ("905/20 rho 0.9", rb["905/20"]), ("905/40 rho 0.9", rb["905/40"])):
    x, fp, fn = dead(r_mp)
    print(f"{lab}: r {r_mp/9:.4e}, r tau {x:.4f}, paralyzable {fp:.4f}, non-paralyzable {fn:.4f}")

print("\n--- C4c subsection 2 (Eq. (67), band-average photon fluxes) and subsection 3 ---")
phi = {905: 0.693 * 905e-9 / (H * C), 940: 0.303 * 940e-9 / (H * C), 1550: 0.270 * 1550e-9 / (H * C)}
for lam, eff, dl in ((905, 0.24, 20), (905, 0.24, 40), (940, 0.37, 10), (1550, 0.30, 10), (1550, 0.80, 10)):
    L = RHO * phi[lam] / np.pi
    print(f"{lam} nm, {eff}, {dl} nm: L {L:.4e}; r_bg {L*dl*A_RX*OM_NEW*OPT*eff:.4e} (old {L*dl*A_RX*OM_OLD*OPT*eff:.4e})")
print(f"worked 940 with rounded inputs: {4.11e17*10*4.91e-4*7.62e-7*0.5*0.37:.4e}")
print(f"905 rounded: {0.9*3.16e18/np.pi*20*4.91e-4*7.62e-7*0.5*0.24:.4e}; 1550 rounded: {0.9*2.1e18/np.pi*10*4.91e-4*7.62e-7*0.5*0.30:.4e}")
r1550 = RHO * phi[1550] / np.pi * 10 * A_RX * OM_NEW * OPT * 0.30
r940 = RHO * phi[940] / np.pi * 10 * A_RX * OM_NEW * OPT * 0.37
print(f"InGaAs headroom: {r1550/1e6:.0f}x at 1e6, {r1550/1e5:.0f}x at 1e5; Si 3x3: {r940/5.4e8:.3f} (band), {full/5.4e8:.3f} (C6(d) at PDE 0.37)")

print("\n--- C4c subsection 1: FMCW emitted power (C7a model, ungated) ---")
tau_rt = 2 * 200 / C
t_dwell = 10e-6 + 2 * tau_rt
f = t_dwell / 10e-6
print(f"tau {tau_rt*1e6:.4f} us; T_dwell {t_dwell*1e6:.3f} us; factor {f:.4f}; emitted at 10/25 Mpts/s: {3.03*f:.3f} / {7.58*f:.3f} W")

print("\n--- C5a and C4d ---")
r = full / 2
print(f"background events per point: {r*20.8e-6*live_c:.0f} (r_bg {r:.4e} x 20.8 us x {live_c:.4f}); "
      f"with rounded 1.83e8 x 20.8 us x 0.885: {1.83e8*20.8e-6*0.885:.0f}")
print(f"FMCW/ToF electrical energy, 2026 central: 4.899/0.415 = {4.899/0.415:.2f}; 2032: 1.738/0.280 = {1.738/0.280:.2f}")
print(f"C5a dead fraction at 940/10, PDE 0.3: {dead(rb['940/10'])[2]:.4f}-{dead(rb['940/10'])[1]:.4f}")
