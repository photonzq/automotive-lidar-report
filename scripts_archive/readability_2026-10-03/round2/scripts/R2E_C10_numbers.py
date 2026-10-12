"""Round 2, agent R2E_C10: every number that sections C10.2-C10.7 recompute under decisions 6 and 7.

Decision 6: eta excludes polarization and mode shape; the factor t^2/2 = 0.419 sits in A_mode = (t^2/2) lambda^2 / Omega_cell.
            Coherent eta = 0.25 (optics x detector x mixing, the C0 design value); ToF eta = 0.5 x 0.37 x 0.885 = 0.164.
Decision 7: ToF in C10.3-C10.3b is the 940 nm SPAD model of C0/C7a, n_req = 21.7 (= 25 x 15.0 / 17.26), eta = 0.164.
Usage: python R2E_C10_numbers.py   (prints everything; writes nothing)
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import poisson

H, C = 6.62607015e-34, 2.99792458e8
DEG = np.pi / 180
LAM_C, LAM_T = 1550e-9, 940e-9
E_C, E_T = H * C / LAM_C, H * C / LAM_T
T = 1 - np.exp(-2 * (0.5 / 0.45) ** 2)          # one-way truncation, w0 = 0.45 D
T2H = T ** 2 / 2                                 # t^2/2
R, RHO, F = 200.0, 0.10, 10.0
OM_FOV = (120 * DEG) * (25 * DEG)
A25 = np.pi * 0.0125 ** 2
LIVE = np.exp(-1.83e8 / 9 * 6e-9)                 # paralyzable live fraction, central bright sun
ETA_T, ETA_C, N_T = 0.5 * 0.37 * LIVE, 0.25, 21.7   # n_req as quoted (25 x 15.0 / 17.26 = 21.73)
print(f"E_ph 1550 = {E_C:.4e} J, 940 = {E_T:.4e} J; t = {T:.4f}, t^2 = {T**2:.4f}, t^2/2 = {T2H:.4f}")
print(f"live = {LIVE:.4f}, eta_ToF = {ETA_T:.4f}, n_req ToF = {N_T} (25 x 15.0/17.26 = {25*15.0/17.26:.2f}, "
      f"1.45 x 15.0 = {1.45*15.0:.2f}); Omega_FOV = {OM_FOV:.4f} sr")
print(f"full-sun P_ToF factor (17.26/14.98) x (0.8851/0.7835) = {(17.26/14.98)*(0.8851/0.7835):.3f}")

print("\n--- C10.2 item 5: cell-filling 0.05 deg beam, 10 % at 200 m, 1 W for 5 us ---")
om05 = (0.05 * DEG) ** 2
a_ideal = LAM_C ** 2 / om05
a_mode = T2H * a_ideal
nph = 5e-6 / E_C
frac = RHO * a_mode / (np.pi * R ** 2)
n_mode = nph * frac
n_det = n_mode * ETA_C
print(f"lambda^2/Omega = {a_ideal*1e6:.3f} mm2; A_mode = {a_mode*1e6:.3f} mm2; photons {nph:.4e}; fraction {frac:.4e}")
print(f"photons in the mode {n_mode:.2f}; detected (eta 0.25) {n_det:.2f}")
for db in (1, 3, 7):
    g = 10 ** (-2 * db / 10)
    print(f"  {db} dB one way: eta_OPA^2 = {g:.4f}, detected {n_det*g:.3f}")
n3 = n_det * 10 ** (-0.6)
for nreq in (88.5, 259):
    print(f"  N_req {nreq}: {nreq/n3:.2f} W per beam; 60 beams {60*nreq/n3:.0f} W; energy per point {5e-6*nreq/n3*1e6:.1f} uJ")
print(f"  four looks, each its own mode: {88.5/4/n3:.2f} W per beam, 60 beams {60*88.5/4/n3:.0f} W")
print(f"  beams at 12 Mpts/s, 5 us: {12e6*5e-6:.0f}")
for e in (44, 56):
    print(f"  measured {e} uJ against 172-502 uJ: {5*88.5/n3/e:.2f}-{5*259/n3/e:.2f} x below")

print("\n--- C10.2 item 5 as merged: eta = 0.8 (QE, ideal mixing; OPA loss in eta_OPA), dwell = 5 us + 2 tau ---")
TAU2 = 2 * 2 * 200 / C                            # two round trips at 200 m (s)
n8 = n_mode * 0.8
n8_3 = n8 * 10 ** (-0.6)
dw5 = 5e-6 + TAU2
beams = 12e6 * dw5
print(f"2 tau(200 m) = {TAU2*1e6:.3f} us; detected {n8:.2f}; after 1/3/7 dB: {n8*10**-0.2:.2f}/{n8_3:.3f}/{n8*10**-1.4:.3f}")
for nreq in (88.5, 259):
    print(f"  N_req {nreq}: {nreq/n8_3:.2f} W per beam; cell-filling energy {5*nreq/n8_3:.1f} uJ; "
          f"60 beams {60*nreq/n8_3:.0f} W; at the {dw5*1e6:.2f} us dwell {beams:.1f} beams -> {beams*nreq/n8_3:.0f} W")
print(f"  own mode per look: {88.5/4/n8_3:.2f} W per beam, {beams*88.5/4/n8_3:.0f} W for {beams:.0f} beams")

print("\n--- decision 1 in C10.2 item 7 and C10.3a items 5-6 (T_dwell = T_int + 2 tau, 200 m) ---")
for tint in (2e-6, 10e-6):
    dw = tint + TAU2
    print(f"  T_int {tint*1e6:.0f} us: dwell {dw*1e6:.3f} us, {1/dw/1e6:.4f} Mpts/s per beam, channels at 12 Mpts/s {12e6*dw:.1f}, "
          f"dwells per frame {0.1/dw:.0f}, 128-channel slots {128*0.1/dw:.4e} ({128*0.1/dw/1.2e8*100:.3f} % of 1.2e8)")
    print(f"     mode-count channels {1.2e8/(0.1/dw):.0f}; footprint count {1.2e6/0.0208/(0.1/dw):.0f} (1.2e6/0.0208 = {1.2e6/0.0208:.4e})")
s128 = 128 * 0.1 / (10e-6 + TAU2)
mesh = np.sqrt(OM_FOV / s128)
print(f"  128 channels, 10 us chirp: {s128:.4e} samples, mesh {mesh:.4e} rad = {mesh/DEG:.4f} deg, {mesh*200*100:.1f} cm at 200 m, "
      f"area-matched radius {mesh*200*100/np.sqrt(np.pi):.2f} cm; footprint for these samples {2.08*s128/1.2e6:.3f} %")
w2 = 0.9e-3 * np.sqrt(1 + (200 / (np.pi * 0.9e-3 ** 2 / LAM_C)) ** 2)
print(f"  2 mm aperture spot radius at 200 m {w2*100:.2f} cm; A_mode {T**2*LAM_C**2*200**2/(2*np.pi*w2**2)*1e6:.3f} mm2")
print(f"  smear 1,200 deg/s x {(10e-6+TAU2)*1e6:.2f} us = {1200*(10e-6+TAU2):.4f} deg; /0.0036 = {1200*(10e-6+TAU2)/0.0036:.2f}; /0.0072 = {1200*(10e-6+TAU2)/0.0072:.2f}")

print("\n--- C10.3 Eq. (139) ---")
base = np.pi * R ** 2 * F * OM_FOV / RHO
pc = {n: n * E_C * base / (T2H * LAM_C ** 2 * ETA_C) for n in (10, 30, 39.1, 88.5, 259)}
print(f"base = {base:.4e}; per count {pc[10]/10:.3f} W")
for n, p in pc.items():
    print(f"  P_coh(N_req {n}) = {p:.1f} W; at eta 0.112: {p*0.25/0.112:.0f} W")
print(f"  four looks each with its own mode: {pc[88.5]/4:.1f} W")
print(f"  rounded-input substitution: {10*1.28e-19*1.15e7/(0.419*2.40e-12*0.25):.2f} W")
pt = {}
for cell in ((0.1, 0.1), (0.1, 0.05), (0.05, 0.05), (0.025, 0.025), (0.0125, 0.0125)):
    om = cell[0] * DEG * cell[1] * DEG
    pt[cell] = N_T * E_T * base / (A25 * om * ETA_T)
    print(f"  {cell}: Omega {om:.4e}, P_ToF {pt[cell]:.4f} W, ratio {pc[10]/pt[cell]:.1f}-{pc[30]/pt[cell]:.1f}")
print(f"  rounded-input ToF substitution: {21.7*2.11e-19*1.15e7/(4.91e-4*3.05e-6*0.164):.4f} W")
r01 = (pc[10] / pt[(0.1, 0.1)], pc[30] / pt[(0.1, 0.1)])
print(f"  parity: 0.1/sqrt({r01[0]:.0f}) = {0.1/np.sqrt(r01[0]):.4f} deg; 0.1/sqrt({r01[1]:.0f}) = {0.1/np.sqrt(r01[1]):.4f} deg")
print(f"  sqrt(A_rx) = {np.sqrt(A25)*1e3:.2f} mm; lambda/sqrt(A) = {LAM_T/np.sqrt(A25):.4e} rad = {LAM_T/np.sqrt(A25)/DEG:.5f} deg")

print("\n--- C0 subsection 10.3 checks (ideal counter, 2,000 bins, 5e-7 per bin, P_D 0.9) ---")
def need(b, pbin=1e-3 / 2000):
    n = 1
    while poisson.sf(n - 1, b) > pbin:
        n += 1
    return n, brentq(lambda s: poisson.sf(n - 1, s + b) - 0.9, 0, 300)
for lab, rbg in (("central", 1.83e8), ("full sun", 3.66e8)):
    x = rbg / 9 * 6e-9
    b = rbg * 1e-9 * 10 * np.exp(-x)
    n, s = need(b)
    print(f"  {lab}: r tau = {x:.4f}, live {np.exp(-x):.4f}, b = {b:.3f}, n_th = {n}, s90 = {s:.2f}; eta = {0.185*np.exp(-x):.4f}")

print("\n--- C6(d) dead fractions at the 0.05 x 0.05 deg pixel, PDE 0.3 ---")
for lab, rbg in (("940/10", 2.965e8), ("905/20", 1.1e9), ("905/40", 2.2e9)):
    x = rbg / 9 * 6e-9
    print(f"  {lab}: r = {rbg/9:.3e}, r tau = {x:.4f}, paralyzable {1-np.exp(-x):.3f}, non-paralyzable {x/(1+x):.3f}")

print("\n--- C10.3a item 1 (1 W, 1.2 M samples, 10 Hz, 200 m, eta 0.1) ---")
ept = 1.0 / (10 * 1.2e6)
for lab, e, a in (("coh 20 mm 1550", E_C, np.pi * 0.01 ** 2), ("ToF 25 mm 940", E_T, A25)):
    nph = ept / e
    print(f"  {lab}: photons {nph:.3e}, geometric {a/(np.pi*R**2):.3e}, x0.01 -> {nph*0.01*a/(np.pi*R**2):.2f}")
print(f"  aperture ratio {(20/25)**2:.2f}, photons per joule ratio 1550/940 = {1550/940:.3f}")

print("\n--- C10.3a item 2 table and item 5 slots (ToF at 940 nm) ---")
cell250 = 250 * 0.05 * DEG
print(f"  cell at 250 m {cell250*100:.2f} cm; speckle {LAM_T*250/cell250*1e3:.3f} mm; N_spk simple {A25*om05/LAM_T**2:.1f}")
req = A25 * OM_FOV / LAM_T ** 2
print(f"  required slots {req:.3e}; available 520 x 423 x 2400 = {520*423*2400:.3e}; ratio {520*423*2400/req:.3f}")

print("\n--- C10.3a item 4: K/P with t^2/2, eta 0.25 ---")
kp = T2H * ETA_C * RHO * LAM_C ** 2 / (np.pi * R ** 2 * F * OM_FOV * E_C)
print(f"  K/P = {kp:.4f} 1/W; rounded {0.419*0.25*0.1*2.40e-12/(1.26e5*10*0.914*1.28e-19):.4f}")
for p in (1, 5, 20, 100, 30 / kp):
    print(f"  {p:6.1f} W: 30 pe -> {min(1, kp*p/30)*100:.2f} %, 259 pe -> {kp*p/259*100:.2f} %")
kpm = kp * 0.112 / 0.25
print(f"  measured eta 0.112: K/P = {kpm:.4f}; 100 W at 30 pe -> {kpm*100/30*100:.1f} %")

print("\n--- C10.3a item 7: efficiency-weighted apertures ---")
tof = A25 * ETA_T * 1e6
print(f"  ToF 25 mm: {A25*1e6:.1f} x {ETA_T:.4f} = {tof:.1f} mm2; full sun eta {0.185*np.exp(-3.66e8/9*6e-9):.4f} -> {A25*1e6*0.185*np.exp(-3.66e8/9*6e-9):.1f} mm2")
am = {100: 28.8, 200: 63.7, 300: 82.0}
for r_, a in am.items():
    print(f"  FMCW 20 mm at {r_} m: {a} x 0.25 = {a*0.25:.2f} mm2; ToF/FMCW = {tof/(a*0.25):.2f}")
print(f"  four looks at 200 m: {4*63.7*0.25:.1f} mm2; ToF/that = {tof/(4*63.7*0.25):.2f}")
w0 = 0.45 * 0.020
aff = T ** 2 * np.pi * w0 ** 2 / 2 * 1e6
print(f"  far-field limit t^2 pi w0^2/2 = {aff:.1f} mm2 (hard/limit = {np.pi*0.01**2*1e6/aff:.2f}); x0.25 = {aff*0.25:.1f} mm2")
for d in (8e-3, 1e-3):
    hard = np.pi * d ** 2 / 4 * 1e6
    lim = T ** 2 * np.pi * (0.45 * d) ** 2 / 2 * 1e6
    print(f"  chip {d*1e3:.0f} mm: hard {hard:.3f}, far-field A_mode {lim:.3f}, x0.25 = {lim*0.25:.4f}, after 3-10 dB each way {lim*0.25*10**-0.6:.4f}-{lim*0.25*0.01:.5f} mm2")
for d in (3e-3, 3.8e-3, 5e-3):
    print(f"  flash {d*1e3:.1f} mm: {np.pi*(d/2)**2*1e6:.2f} mm2 x {ETA_T:.3f} = {np.pi*(d/2)**2*1e6*ETA_T:.2f} mm2")
