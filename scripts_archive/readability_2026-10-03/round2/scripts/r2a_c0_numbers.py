"""Round 2, agent R2A_C0: every number of §C0 that depends on the ToF background, n_req, eta, the link-budget
designs or the FMCW dwell, recomputed on the decisions of 2026-10-05 (0.05 x 0.05 deg macro-pixel, x1.45 margin,
FMCW dwell T_int + 2 tau). Prints each quantity with its inputs; writes nothing.

Usage: python r2a_c0_numbers.py
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import poisson

H, C = 6.62607015e-34, 2.99792458e8
EPH = {lam: H * C / (lam * 1e-9) for lam in (865, 870, 905, 940, 1550)}
RHO = 0.1
A25 = np.pi * 0.0125 ** 2
ALPHA = {940: 0.0847e-3, 1550: 0.0442e-3}  # clear-air extinction (1/m), Kim model V = 23 km (tables file)
T2T = 0.9153 ** 2  # truncation t^2


def head(t):
    print(f"\n=== {t}")


def threshold(b, p):
    n = 1
    while poisson.sf(n - 1, b) > p:  # P(N >= n | b)
        n += 1
    return n


def s_for(b, p, pd=0.9):
    n = threshold(b, p)
    return n, brentq(lambda s: poisson.sf(n - 1, s + b) - pd, 0.0, 400.0)


# ------------------------------------------------------------------ pixel and sunlight
head("macro-pixel solid angle and the subsection 5 example (905 nm, 20 nm, rho 0.9, PDE 0.3)")
th = np.deg2rad(0.05)
om = th ** 2
print(f"0.05 deg = {th:.4e} rad; Omega = {om:.4e} sr (0.1 x 0.05 deg: {np.deg2rad(0.1) * th:.4e} sr)")
flux905 = 0.75 / EPH[905]
r905 = flux905 * 20 * (0.9 / np.pi) * om * A25 * 0.5 * 0.3
print(f"E/Eph = {flux905:.4e}; r_bg(905, 0.05x0.05) = {r905:.4e} /s;  with the rounded 3.4e18 and 7.62e-7: "
      f"{3.4e18 * 20 * (0.9 / np.pi) * 7.62e-7 * 4.91e-4 * 0.5 * 0.3:.4e}")

head("§C6(d) 940 nm background and the model's central case")
r_pde03 = 2.965e8  # §C6(d), 940 nm, 10 nm filter, rho 0.9, PDE 0.3, 0.05 x 0.05 deg
r_full = r_pde03 * 0.37 / 0.3
r_c = r_full / 2
print(f"full sun at PDE 0.37: {r_full:.4e} /s; central (half): {r_c:.4e} /s")
for lab, r in (("central", 1.83e8), ("central exact", r_c), ("high (full sun)", 3.66e8)):
    x = r / 9 * 6e-9
    live = np.exp(-x)
    b = r * 1e-9 * 10 * live
    print(f"{lab:16s} r/9 = {r / 9:.4e} /s, r tau = {x:.4f}, live = {live:.4f}, f_dead = {1 - live:.4f}, b = {b:.4f}")
x = 1.83e8 / 9 * 6e-9
live_np = 1 / (1 + x)
b_np = 1.83e8 * 1e-9 * 10 * live_np
print(f"non-paralyzable: dead {x / (1 + x):.4f}, live {live_np:.4f}, b = {b_np:.4f}, "
      f"n_th = {threshold(b_np, 5e-7)}, ideal = {s_for(b_np, 5e-7)[1]:.3f}")
eta = 0.5 * 0.37 * np.exp(-x)
print(f"eta = 0.5 x 0.37 x {np.exp(-x):.4f} = {eta:.4f}; non-paralyzable eta = {0.5 * 0.37 * live_np:.4f} "
      f"(ratio {live_np / np.exp(-x):.4f})")
ev = 1.83e8 * 20.8e-6 * np.exp(-x)
print(f"events in 20.8 us: {ev:.1f} (+21.7 signal = {ev + 21.7:.0f}); exact r: {r_c * 20.8e-6 * np.exp(-r_c / 9 * 6e-9):.1f}")

# ------------------------------------------------------------------ detection statistics
head("ideal counter, 2,000 bins (p = 5e-7), 90 % detection")
B = 1.62
p = 5e-7
n_th = threshold(B, p)
print(f"b = {B}: P(N>=11) = {poisson.sf(10, B):.3e}, P(N>=12) = {poisson.sf(11, B):.3e}, n_th = {n_th}")
n, s90 = s_for(B, p)
n, s50 = s_for(B, p, 0.5)
print(f"s(0.9) = {s90:.3f} (s+b = {s90 + B:.3f}); s(0.5) = {s50:.3f}; P_D(25) = {poisson.sf(n_th - 1, 25 + B):.4f}; "
      f"P_D(120) = {poisson.sf(n_th - 1, 120 + B):.6f}; P(N>=12 | 16.60) = {poisson.sf(11, 16.60):.4f}")
for b in (2.87, 4.49):
    print(f"b = {b}: n_th = {threshold(b, p)}, ideal = {s_for(b, p)[1]:.3f}, P(N>=n_th-1) = {poisson.sf(threshold(b, p) - 2, b):.2e}, "
          f"P(N>=n_th) = {poisson.sf(threshold(b, p) - 1, b):.2e}")
margin = 25 / 17.26
print(f"margin 25/17.26 = {margin:.4f}; n_req = margin x {s90:.3f} = {margin * s90:.3f}; 1.45 x 14.98 = {1.45 * 14.98:.3f}")

head("subsection 7 worked cases (1,000 bins, b = 1 and 0.01) -- model independent check")
for b, pp in ((1.0, 1e-6), (0.01, 1e-6), (1.0, 1e-9)):
    nt = threshold(b, pp)
    print(f"b = {b}, p = {pp:g}: n_th = {nt}, P(N>=n_th-1) = {poisson.sf(nt - 2, b):.2e}, P(N>=n_th) = {poisson.sf(nt - 1, b):.2e}, "
          f"s = {s_for(b, pp)[1]:.2f} (s+b = {s_for(b, pp)[1] + b:.2f})")
print(f"b = 1.62 with 2,000 bins: s = {s90:.2f} (vs b = 1 with 1,000 bins: {s_for(1.0, 1e-6)[1]:.2f})")

head("shots per point (b scales with shots) and the two-bin spread")
for shots in (5, 10, 20):
    b = 1.83e8 * 1e-9 * shots * np.exp(-x)
    nt, s = s_for(b, p)
    print(f"{shots:2d} shots: b = {b:.3f}, n_th = {nt}, ideal = {s:.2f}")
s5, s10, s20 = (s_for(1.83e8 * 1e-9 * k * np.exp(-x), p)[1] for k in (5, 10, 20))
print(f"per factor of two: {s10 / s5:.3f} (10 vs 5 shots), {s20 / s10:.3f} (20 vs 10 shots)")
b2 = 2 * 1.62
print(f"two bins summed: 2b = {b2:.2f}, n_th = {threshold(b2, p)}, ideal = {s_for(b2, p)[1]:.2f}, "
      f"ratio to one bin = {s_for(b2, p)[1] / s90:.3f}; rest of the 1.45 margin = {margin / (s_for(b2, p)[1] / s90):.3f}")
b2o = 2 * 2.87
print(f"(old check) b = 2.87 two bins: 2b = {b2o}, ideal = {s_for(b2o, p)[1]:.2f}, ratio {s_for(b2o, p)[1] / s_for(2.87, p)[1]:.3f}")

head("search table, ToF column (bright sun)")
for lab, pp in (("full search", 5e-7), ("1e-2 false points/pt", 1e-2 / 2000), ("tracking 20 bins", 1e-3 / 20),
                ("known cell", 1e-3)):
    nt_o, so = s_for(2.87, pp)
    nt_n, sn = s_for(1.62, pp)
    print(f"{lab:22s} p = {pp:.1e}: b 2.87 -> n_th {nt_o}, s {so:.2f};   b 1.62 -> n_th {nt_n}, s {sn:.2f} "
          f"({(1 - sn / s90) * 100:.1f} % below full)")
for lab, v in (("joint", 77.8), ("1e-2", 81.6), ("tracking", 59.6)):
    print(f"FMCW {lab}: {(1 - v / 88.5) * 100:.1f} % below 88.5")

head("where FMCW's extra photons go (four looks)")
print(f"noise floor 21.9/{s90:.2f} = {21.9 / s90:.3f}; both ramps 39.1/21.9 = {39.1 / 21.9:.3f}; fading 88.5/39.1 = "
      f"{88.5 / 39.1:.3f}; one look 259/39.1 = {259 / 39.1:.2f}; total 88.5/{s90:.2f} = {88.5 / s90:.2f}")

# ------------------------------------------------------------------ link budget
head("detection levels (Eq. (41))")
nr, et = 21.7, 0.164
for eph in (2.11e-19, 2.113e-19, EPH[940]):
    L = nr * eph / (et * 1e-7)
    print(f"E_ph {eph:.4e}: L_det = {L:.4e} = {-10 * np.log10(L):.2f} dB")
L_spad = nr * EPH[940] / (0.5 * 0.37 * np.exp(-x) * 1e-7)
L_apd = 890 * EPH[1550] / (0.4 * 2e-6)
print(f"exact eta: L_spad = {L_spad:.4e} ({-10 * np.log10(L_spad):.2f} dB); L_apd = {L_apd:.4e}; ratio {L_spad / L_apd:.3f}, "
      f"sqrt {np.sqrt(L_spad / L_apd):.3f}")
for D in (0.010, 0.025, 0.050):
    r0 = D / 2 * np.sqrt(RHO / 2.80e-10)
    ra = brentq(lambda R: RHO * D ** 2 / (4 * R ** 2) * np.exp(-2 * ALPHA[940] * R) - L_spad, 1, 5000)
    print(f"D = {D * 1e3:.0f} mm: no air {r0:.1f} m (with 2.80e-10), clear air {ra:.1f} m")
need_apd = 890 * 1.28e-19 / 0.40
need_spad = 21.7 * 2.11e-19 / 0.164
print(f"APD/SPAD per-point need (rounded inputs) = {need_apd:.4e}/{need_spad:.4e} = {need_apd / need_spad:.3f}; "
      f"margin 20/{need_apd / need_spad:.2f} = {20 / (need_apd / need_spad):.3f}, sqrt = {np.sqrt(20 / (need_apd / need_spad)):.3f}")

head("Eq. (45), equal apertures")
f1 = (30 * 1.28e-19 / 0.25) / (21.7 * 2.11e-19 / 0.164)
g = 1 / (T2T * 0.45 ** 2)
print(f"first factor = {30 * 1.28e-19 / 0.25:.4e}/{21.7 * 2.11e-19 / 0.164:.4e} = {f1:.4f}; 1/(t^2 0.45^2) = {g:.3f}; "
      f"product = {f1 * g:.3f};  0.55 x 5.9 = {0.55 * 5.9:.3f}")

head("best-D FMCW against the 25 mm SPAD, with clear air (crossing)")


def e_spad(R):  # 25 mm SPAD, energy to reach R (J)
    return L_spad * 1e-7 / (RHO * A25 / (np.pi * R ** 2) * np.exp(-2 * ALPHA[940] * R))


def e_fmcw_best(R):  # best collimated aperture, Eq. (35), per look n = 30, eta 0.25
    L_env = RHO * T2T * 1550e-9 / (4 * np.pi * R) * np.exp(-2 * ALPHA[1550] * R)
    return 30 * EPH[1550] / (0.25 * L_env)


for R in (100, 200, 300, 500):
    print(f"R = {R}: SPAD {e_spad(R) * 1e9:.1f} nJ, FMCW best {e_fmcw_best(R) * 1e9:.1f} nJ, ratio {e_fmcw_best(R) / e_spad(R):.3f}")
Rx = brentq(lambda R: e_fmcw_best(R) - e_spad(R), 300, 3000)
print(f"crossing with clear air: R = {Rx:.0f} m, E = {e_spad(Rx) * 1e6:.3f} uJ; 1/R law from 200 m: {4.08 * 200:.0f} m; "
      f"from 500 m: {1.59 * 500:.0f} m")

head("10.6 and 10.7")
print(f"0.1 uJ x (200/232)^2 = {100 * (200 / 232) ** 2:.2f} nJ; 74/303 = {74 / 303:.3f}; 1,522/74 = {1522 / 74:.2f}; "
      f"303/74 = {303 / 74:.3f}; 74.2/10^(0.147/10) = {74.2 / 10 ** (0.0147):.1f} nJ")
ep = 7.4e-9
nph = ep / 2.11e-19
frac = 1571 * 4.91e-4 / (np.pi * 5 ** 2)
print(f"per shot 7.4 nJ: {nph:.4e} photons; fraction {frac:.4e}; collected {nph * frac:.4e}; detected (0.164) "
      f"{nph * frac * 0.164:.4e}; weakest per shot 21.7/10 = 2.17; ratio {nph * frac * 0.164 / 2.17:.3e} = "
      f"{10 * np.log10(nph * frac * 0.164 / 2.17):.1f} dB")
et_pix = 4.91e-4 * 7.62e-7
print(f"A Omega (25 mm, 0.05 x 0.05 deg) = {et_pix:.4e} m2 sr; lambda^2 = {1.55e-6 ** 2:.4e}; ratio {1.55e-6 ** 2 / et_pix:.3e} "
      f"= {10 * np.log10(1.55e-6 ** 2 / et_pix):.1f} dB;  (0.1 deg square: {4.9e-4 * 1.75e-3 ** 2:.3e}, "
      f"{10 * np.log10(2.4e-12 / (4.9e-4 * 1.75e-3 ** 2)):.1f} dB)")

head("FMCW dwell")
tau = 2 * 200 / 3.0e8
print(f"tau(200 m) = {tau * 1e6:.3f} us; T_dwell = 10 + 2 tau = {(10e-6 + 2 * tau) * 1e6:.2f} us; rate {1 / (10e-6 + 2 * tau):.0f} /s;"
      f" emitted 0.30 x {(10e-6 + 2 * tau) / 10e-6:.3f} = {0.30 * (10e-6 + 2 * tau) / 10e-6:.3f} uJ; 10 us ramps: T_int = "
      f"2 x (10 - {tau * 1e6:.2f}) = {2 * (10e-6 - tau) * 1e6:.2f} us")

# ------------------------------------------------------------------ 10.8
head("10.8 ToF benchmark, Eq. (55) with n_req 21.7")
print(f"model eta A = 0.164 x 4.91 cm2 = {0.164 * 4.91:.3f} cm2")
sony = 21.7 * 2.20e-19 * np.pi * 150 ** 2 / (0.1 * 2.85e-7)
print(f"Sony: {sony:.4e} m2")
for opt in (0.5, 0.7):
    e = opt * 0.22 * 0.885
    print(f"  optics {opt}: eta {e:.4f}, A {sony / e:.4e} m2, D {2 * np.sqrt(sony / e / np.pi) * 1e3:.2f} mm, f/# at 11.5 mm "
          f"{11.5 / (2 * np.sqrt(sony / e / np.pi) * 1e3):.2f}")
tosh = 21.7 * EPH[905] * np.pi * 200 ** 2 / (0.1 * 217e-9)
toyo = 21.7 * EPH[870] * np.pi * 100 ** 2 / (0.09 * 108e-9)
for lab, v in (("Toshiba", tosh), ("Toyota", toyo)):
    print(f"{lab}: eta A = {v * 1e4:.4f} cm2 (/9 = {v * 1e4 / 9:.4f}); D at eta 0.10 {2 * np.sqrt(v / 0.10 / np.pi) * 1e3:.1f} mm, "
          f"0.05 {2 * np.sqrt(v / 0.05 / np.pi) * 1e3:.1f} mm; model/this = {0.164 * 4.909e-4 / v:.2f}")
for lab, lam, R, rate in (("Ouster OS2", 865, 200, 1.31e6), ("Hesai AT128", 905, 210, 1.54e6)):
    for D in (0.030, 0.020):
        A = np.pi * (D / 2) ** 2
        e = 21.7 * EPH[lam] * np.pi * R ** 2 / (RHO * 0.164 * A)
        print(f"{lab} D {D * 1e3:.0f} mm: {e * 1e9:.1f} nJ, {e * rate:.3f} W")
