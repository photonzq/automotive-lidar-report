"""Section C9/C9a lidar-to-lidar interference model (Round 2, block R2F_C9).

Computes every number used in the rebuilt C9/C9a text:
  1. Kim et al. (IEMEK J. 12(1):43, 2017) measured fractions from their Tables 3-4,
     and the Eq. (127) prediction for their SICK LMS-511 geometry (their Table 1).
  2. Eq. (127) collision fractions for today's 3-16 and the later 10-30 units.
  3. The traffic reduction factor F = f_ov * f_band * f_sd and the reduced fractions.
  4. Eq. (128): ghosts per point, per frame and per second under 2-of-10 and 3-of-10
     shot-recurrence rules, with the one-unit "visit" term and the two-unit term,
     plus a Monte Carlo check of the visit term.
  5. The direct-view chain for two facing C6-class scanners, and the GB/T 45500 test case.

Inputs come from the report (C6, C9) and from the two sources named above
(SICK LMS511 datasheet; Kim et al. 2017). No files are read or written.
Run: <anaconda python> R2F_C9_interference_model.py
"""
import math
import numpy as np

c = 299_792_458.0

print("=== 1. Kim et al. 2017 measured fractions (Tables 3-4) ===")
# Table 4: occurrences of consecutive interference in the same line, by run length 1..17
table4 = {
    "side-by-side #1": [36593, 1467, 409, 150, 74, 43, 25, 12, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    "side-by-side #2": [218340, 3181, 810, 344, 151, 108, 73, 51, 1, 2, 1, 0, 1, 0, 0, 1, 1],
    "face-to-face": [28042, 1908, 522, 222, 123, 58, 37, 35, 3, 0, 1, 0, 0, 0, 1, 0, 0],
    "back-to-back a": [4416, 136, 1] + [0] * 14,
    "back-to-back b": [4500, 152, 16, 4, 1] + [0] * 12,
}
scanned = {  # Table 3, interference evaluation step, 24 h
    "side-by-side #1": 1_384_560_000, "side-by-side #2": 1_384_560_000,
    "face-to-face": 1_384_560_000, "back-to-back a": 779_760_000, "back-to-back b": 779_760_000,
}
for k, runs in table4.items():
    pts = sum((i + 1) * n for i, n in enumerate(runs))
    print(f"{k:16s} interfered points {pts:7d}  fraction {pts / scanned[k]:.3e}")

print("\n=== Kim geometry: Eq. (127) prediction ===")
prf, f_rot, step = 36_000.0, 25.0, 0.25          # Kim Table 1
print("steps per 360 deg:", prf / f_rot, " x step =", prf / f_rot * step, "deg")
div_deg = 11e-3 * 180 / math.pi                    # 11 mrad
T_kim = 2 * 80.0 / c                               # 80 m range
print(f"divergence {div_deg:.3f} deg, listen window {T_kim*1e6:.4f} us")
r_lo, r_hi = prf * div_deg / 360, prf * 2 * div_deg / 360
p_lo, p_hi = r_lo * T_kim, r_hi * T_kim
print(f"r_f = {r_lo:.1f} - {r_hi:.1f} /s ; p1 = {p_lo:.3e} - {p_hi:.3e}; central {0.5*(p_lo+p_hi):.3e}")
print(f"check 25 Hz x 0.63/0.25 = {f_rot*div_deg/step:.1f} /s")

print("\n=== 2. Eq. (127) for the C6-class foreign unit ===")
Ndot_f = 2.5e8                 # spot-shots/s
Om_hit, Om_f = 0.0025, 3120.0  # deg^2
r_f = Ndot_f * Om_hit / Om_f
T_listen = 1 / 48_000          # 20.83 us column
p1 = r_f * T_listen
print(f"r_f = {r_f:.2f} /s, T_listen = {T_listen*1e6:.3f} us, p1 = {p1:.4e} (200 x 20.8 us = {200*20.8e-6:.3e})")
ratio = p1 / (0.5 * (p_lo + p_hi))
print(f"p1 / Kim central = {ratio:.1f}; rescaled 2.6e-5 -> {2.6e-5*ratio:.2e}, 3e-4 -> {3e-4*ratio:.2e}")
for n in (3, 16, 10, 30):
    print(f"n={n:2d}: P>=1 = {100*(1-(1-p1)**n):.2f} %  (with 4.2e-3: {100*(1-(1-4.2e-3)**n):.2f} %)")
p_small = 2e7 * 0.01 / 3120 * T_listen
print(f"small unit: {2e7*0.01/3120:.1f} /s, p = {p_small:.4e}")
for n in (3, 16, 10, 30):
    print(f"  n={n:2d}: {100*(1-(1-p_small)**n):.2f} %")

print("\n=== 3. Traffic reduction factor ===")
F_lo, F_hi = 0.25 * 0.5 * 0.5, 0.6 * 0.9 * 1.0
print(f"F = {F_lo:.4f} - {F_hi:.3f}")
for n, F in ((3, F_lo), (16, F_hi), (10, F_lo), (30, F_hi)):
    print(f"  n={n:2d}, F={F:.4f}: {100*(1-(1-F*p1)**n):.3f} %")

print("\n=== 4. Ghost model, Eq. (128) ===")
N = 10                      # shots per point
tau = 2 * 0.05 / c          # 5 cm bin, s
T_w = 2e-6                  # per-shot span (300 m)
T_d = 0.6e-6                # dither range (+-0.3 us)
print(f"tau_bin = {tau*1e9:.4f} ns, bins in span {T_w/tau:.0f}, bins in dither {T_d/tau:.0f}")
frame_pts = 2400 * 520
pts_per_s = frame_pts * 20
print("frame points", frame_pts, " points/s", pts_per_s)
# visit statistics: offset of the 10-shot foreign column relative to my 10-shot window,
# uniform over 20 equal intervals of one shot period; k = shots inside my window
ks = [10] + [k for k in range(1, 10) for _ in (0, 1)] + [0]
assert len(ks) == 20
Ek = np.mean(ks)
E2 = np.mean([math.comb(k, 2) for k in ks])
E3 = np.mean([math.comb(k, 3) for k in ks])
P_v = 2 * T_listen / 0.05      # 2 x 20.83 us / 50 ms
print(f"P_v = {P_v:.4e}, E[k] = {Ek}, E[C(k,2)] = {E2}, E[C(k,3)] = {E3}, P(k>=2|overlap) = {np.mean([k>=2 for k in ks])}")
c2, c3 = E2 / Ek, E3 / Ek
print(f"c2 = {c2:.3f} pairs per foreign shot, c3 = {c3:.3f} triples per foreign shot; P_v*E[k] = {P_v*Ek:.4e}")
cases = {"today n=3": 3, "today n=16": 16, "later n=10": 10, "later n=30": 30}
print("Eq. (128) as written in the report: visit term c2*kbar*tau/T_d with T_d/tau = 1,800, "
      "plus two-unit term kbar^2/2 * tau/T_w with T_w/tau = 6,000 (an upper bound; the")
print("simulation below shows that about 78% of cross pairs fall on different shots, not 100%).")
for name, n in cases.items():
    kb = n * p1
    t1 = c2 * kb / 1800
    t2 = kb**2 / 2 / 6000
    pg = t1 + t2
    p3 = c3 * kb / 1800**2
    print(f"{name:11s} kbar={kb:.4f}  visit term {t1:.3e}  two-unit term {t2:.3e}  ratio {t1/t2:.0f}  "
          f"total {pg:.3e} -> {pg*frame_pts:.1f}/frame {pg*pts_per_s:.0f}/s ; "
          f"3-of-10 {p3:.3e} -> {p3*frame_pts:.3f}/frame {p3*pts_per_s:.2f}/s ; "
          f"two-unit term alone {t2*frame_pts:.3f}/frame {t2*pts_per_s:.2f}/s")
print(f"budget share at the top of the range: {c2*30*p1/1800/1e-3:.2f} of 1e-3 per point")
print(f"no dither: P_v x P(k>=2) = {P_v*0.85:.3e} per unit; n=3..30 -> "
      f"{100*3*P_v*0.85:.2f} - {100*30*P_v*0.85:.2f} %")

print("\n--- 4b. Bright sun: background-supplied recurrences ---")
# bright-sun (central) background of C0 subsection 10.3 after Round 2: r_bg = 1.83e8 /s, live fraction 0.885
b_shot = 1.83e8 * 0.3333e-9 * 0.885          # counts per 0.333 ns bin per shot
print(f"background per 0.333 ns bin per shot: {b_shot:.4f}")
print(f"lone burst finds >=1 background count on one of 9 other shots: {1-math.exp(-9*b_shot):.3f}")
p1c = 1 - math.exp(-b_shot) * (1 + b_shot)                     # >=2 counts
p2c = 1 - math.exp(-b_shot) * (1 + b_shot + b_shot**2 / 2)     # >=3 counts
print(f"background >=2 counts per bin per shot {p1c:.3e} (approx b^2/2 e^-b = {b_shot**2/2*math.exp(-b_shot):.3e}); "
      f">=3 counts {p2c:.3e}")
kb = 30 * p1
visit2 = c2 * kb / 1800
for name, q in (("two-count test", p1c), ("three-count test", p2c)):
    lone_2of10 = kb * 9 * q
    lone_3of10 = kb * math.comb(9, 2) * q**2
    pair_plus_bg = visit2 * 8 * q
    print(f"{name}: 2-of-10 lone-burst leak {lone_2of10:.3e}/point (visit term {visit2:.3e}); "
          f"3-of-10 lone {lone_3of10:.3e} + pair+bg {pair_plus_bg:.3e} = {lone_3of10+pair_plus_bg:.3e}/point "
          f"-> {(lone_3of10+pair_plus_bg)*frame_pts:.1f}/frame")
    print(f"   per-foreign-shot factors: 9q = {9*q:.3e}, C(9,2)q^2 = {math.comb(9,2)*q**2:.3e}, 8q = {8*q:.3e}")
from math import comb
for lam in (2.1, 2.17, 3.3):
    pge2 = 1 - math.exp(-lam) * (1 + lam)
    pge3 = 1 - math.exp(-lam) * (1 + lam + lam**2 / 2)
    det = lambda p, m: sum(comb(10, i) * p**i * (1 - p)**(10 - i) for i in range(m, 11))
    print(f"signal {lam}/shot: P(>=2 counts) {pge2:.3f} -> 2-of-10 {det(pge2,2):.4f}, 3-of-10 {det(pge2,3):.4f}; "
          f"P(>=3) {pge3:.3f} -> 2-of-10 {det(pge3,2):.4f}, 3-of-10 {det(pge3,3):.4f}")

print("\n--- Monte Carlo check of the visit term (one foreign unit, my +-0.3 us dither) ---")
rng = np.random.default_rng(1)
PRI = 20.8333e-6 / N
M, CHUNKS = 500_000, 20
hits2 = hits3 = 0
tot_pairs = 0
j = np.arange(N)
for _ in range(CHUNKS):
    t0 = rng.uniform(-N * PRI, N * PRI, M)          # visit start relative to my first shot
    # foreign shot j arrives at t0 + j*PRI (common path delay absorbed in t0)
    arr = t0[:, None] + j[None, :] * PRI            # M x N
    my_shot = np.floor(arr / PRI).astype(int)        # index of my shot it falls in
    inside = (my_shot >= 0) & (my_shot < N)
    base = arr - my_shot * PRI                        # offset in that shot's period
    dith = rng.uniform(-0.3e-6, 0.3e-6, (M, N))       # my dither, per my shot
    # my shot i fires at i*PRI + d_i; the arrival in shot i's histogram is base - d_i
    d_my = np.take_along_axis(dith, np.clip(my_shot, 0, N - 1), axis=1)
    off = base - d_my + 1e-6                          # keep positive
    b = np.floor(off / tau).astype(np.int64)
    b[~inside] = -1 - np.arange(N)[None, :].repeat(M, 0)[~inside]  # unique dummies
    bs = np.sort(b, axis=1)
    same = (bs[:, 1:] == bs[:, :-1]) & (bs[:, 1:] >= 0)
    # 2-of-10: any repeated bin; 3-of-10: any bin appearing 3 times
    hits2 += np.count_nonzero(same.any(axis=1))
    trip = same[:, 1:] & same[:, :-1]
    hits3 += np.count_nonzero(trip.any(axis=1))
    k_in = inside.sum(axis=1)
    tot_pairs += (k_in * (k_in - 1) // 2).sum()
MT = M * CHUNKS
print(f"MC ({MT:,} overlapping visits): mean pairs {tot_pairs/MT:.3f} (analytic {E2}); "
      f"P(2-of-10 ghost | overlap) {hits2/MT:.4e} (analytic {E2*tau/T_d:.4e}); "
      f"P(3-of-10 | overlap) {hits3/MT:.2e} from {hits3} events (analytic {E3*(tau/T_d)**2:.2e})")

print("\n--- Monte Carlo check of the two-unit term (two independent overlapping visits) ---")
M2 = 2_000_000
tA = rng.uniform(-N * PRI, N * PRI, M2)
tB = rng.uniform(-N * PRI, N * PRI, M2)
phaseB = rng.uniform(0, PRI, M2)        # unit B's firing phase is unrelated to unit A's
dith = rng.uniform(-0.3e-6, 0.3e-6, (M2, N))
bins = []
shots = []
for t, ph in ((tA, 0.0), (tB, phaseB)):
    arr = (t + ph)[:, None] + j[None, :] * PRI
    ms = np.floor(arr / PRI).astype(int)
    ins = (ms >= 0) & (ms < N)
    d_my = np.take_along_axis(dith, np.clip(ms, 0, N - 1), axis=1)
    bb = np.floor((arr - ms * PRI - d_my + 1e-6) / tau).astype(np.int64)
    bb[~ins] = -10**9
    bins.append(bb)
    shots.append(np.where(ins, ms, -1))
cross = np.zeros(M2, dtype=bool)
npairs = np.zeros(M2)
for a in range(N):
    for bidx in range(N):
        ok = (bins[0][:, a] >= 0) & (bins[1][:, bidx] >= 0)
        npairs += ok
        cross |= ok & (bins[0][:, a] == bins[1][:, bidx]) & (shots[0][:, a] != shots[1][:, bidx])
print(f"mean cross pairs {npairs.mean():.2f}; P(cross pair shares a bin on different shots) {cross.mean():.3e}; "
      f"analytic {npairs.mean()*(1-1/N)*tau/T_w:.3e}")

print("\n=== 5. Direct-view chain, two facing C6-class units ===")
th = 0.05 * math.pi / 180
print(f"column width at 30 m: {th*30*1e3:.1f} mm ; 25 mm at 30 m subtends {25e-3/30*180/math.pi:.4f} deg")
for a in (2, 4):
    print(f"aligned overlap probability ({a}/2400) = {a/2400:.2e}")
for mf in (1, 2):
    pe = (50 + mf) / 2400
    print(f"m_f={mf}: localized event prob {pe:.4f}, points/event {50*mf} ({50*mf/frame_pts:.2e}), "
          f"average {pe*50*mf:.2f} pts/frame = {pe*50*mf/frame_pts:.2e}; column-wide {520*mf} ({520*mf/frame_pts:.2e})")
print("GB/T test distances:")
for d in (2.0, 1.0, 0.5):
    mf = 1 + 25e-3 / (th * d)
    print(f"  d={d} m: m_f={mf:.1f}; column-wide {520*mf:.0f} pts = {100*520*mf/frame_pts:.2f} %; "
          f"localized {50*mf:.0f} pts = {100*50*mf/frame_pts:.3f} %")
print("Robinson-like spacing 1-3 m:")
for d in (1.0, 3.0):
    mf = 1 + 25e-3 / (th * d)
    print(f"  d={d} m: m_f={mf:.1f}, localized {50*mf:.0f} points per crossing")
