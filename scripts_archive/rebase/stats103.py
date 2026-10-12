"""Detection statistics for section C0 subsection 10.3, per-point rule for both receivers.

Rule: P_D = 0.9 per point with at most 1e-3 false points per point, over the full search.
ToF: 2,000 bins of 1 ns (0-300 m).  FMCW: 1 GHz over 5 us up + 5 us down, 200 kHz bins,
up-ramp search N_b = 2,450 bins (400 MHz range + 90 MHz Doppler), down-ramp window N_w = 1,800
bins (+-180 MHz = 2 x (+-90 MHz) Doppler, +-70 m/s).  Photons split equally between ramps;
speckle common to both ramps; L looks summed incoherently in each ramp.
"""
import numpy as np
from scipy import stats, optimize, integrate, special

PD = 0.9
PFA_PT = 1e-3
N_TOF = 2000
N_B, N_W = 2450, 1800


# ------------------------------------------------------------------ photon counting
def tof_threshold(b, p_bin):
    k = 0
    while stats.poisson.sf(k - 1, b) > p_bin:
        k += 1
    return k


def tof_pd(s, b, k):
    return stats.poisson.sf(k - 1, s + b)


def tof_need(b, p_bin, pd=PD):
    k = tof_threshold(b, p_bin)
    return k, optimize.brentq(lambda s: tof_pd(s, b, k) - pd, 1e-6, 1e4)


# ------------------------------------------------------------------ coherent, one ramp
def thr(L, p):
    return -np.log(p) if L == 0 else stats.gamma.isf(p, L)


def pd_ramp_given_S(nr, L, x, S):
    """P(per-ramp statistic > x) for a ramp with mean signal nr, speckle realization S."""
    if L == 0:
        return stats.ncx2.sf(2 * x, 2, 2 * nr)
    return stats.ncx2.sf(2 * x, 2 * L, 2 * nr * S / L)


def pd_pair(n_tot, L, x1, x2):
    nr = n_tot / 2
    if L == 0:
        return pd_ramp_given_S(nr, 0, x1, 1) * pd_ramp_given_S(nr, 0, x2, 1)
    g = lambda S: pd_ramp_given_S(nr, L, x1, S) * pd_ramp_given_S(nr, L, x2, S) * stats.gamma.pdf(S, L)
    return integrate.quad(g, 0, np.inf, limit=400)[0]


def two_stage(L, nb=N_B, nw=N_W, pfa_pt=PFA_PT, pd=PD):
    best = None
    for lp1 in np.linspace(-9, -2.5, 53):
        p1 = 10 ** lp1
        p2 = pfa_pt / (nb * p1 * nw)
        if p2 >= 0.5:
            continue
        x1, x2 = thr(L, p1), thr(L, p2)
        n = optimize.brentq(lambda n: pd_pair(n, L, x1, x2) - pd, 0.5, 1e5)
        if best is None or n < best[0]:
            best = (n, p1, p2, x1, x2)
    return best


def one_ramp(L, n_bins, pfa_pt=PFA_PT, pd=PD):
    """All photons in one ramp (range-only or known velocity), for comparison."""
    x = thr(L, pfa_pt / n_bins)
    if L == 0:
        f = lambda n: stats.ncx2.sf(2 * x, 2, 2 * n) - pd
    else:
        f = lambda n: special.gammaincc(L, x / (1 + n / L)) - pd
    return optimize.brentq(f, 0.1, 1e5)


def pair_sum(L, n_hyp=N_B * N_W, pfa_pt=PFA_PT, pd=PD):
    """Joint search: sum both ramps' powers for every (up, down) pair."""
    p = pfa_pt / n_hyp
    if L == 0:
        x = stats.gamma.isf(p, 2)
        f = lambda n: stats.ncx2.sf(2 * x, 4, 2 * n) - pd
    else:
        x = stats.gamma.isf(p, 2 * L)
        def f(n):
            g = lambda S: stats.ncx2.sf(2 * x, 4 * L, 2 * n * S / L) * stats.gamma.pdf(S, L)
            return integrate.quad(g, 0, np.inf, limit=400)[0] - pd
    return optimize.brentq(f, 0.5, 1e5)


if __name__ == "__main__":
    print("=== ToF photon counting, 2,000 bins, 1e-3 false points per point (p_bin = 5e-7)")
    p_bin = PFA_PT / N_TOF
    for b, lab in [(0.01, "night"), (2.13, "sun, old 6e8 x 0.71 / 2"), (2.94, "bright sun, central"),
                   (4.92, "bright sun, rho 0.9 scene")]:
        k, s90 = tof_need(b, p_bin)
        _, s50 = tof_need(b, p_bin, 0.5)
        print(f"  {lab:28s} b={b:5.2f}  n_th={k:2d}  P(N>=n_th|b)={stats.poisson.sf(k-1,b):.2e}  "
              f"P(N>=n_th-1|b)={stats.poisson.sf(k-2,b):.2e}  s50={s50:5.1f} s90={s90:5.1f}  "
              f"P_D(25)={tof_pd(25,b,k):.3f}  P_D(120)={tof_pd(120,b,k):.3f}")
    for b in (0.01, 2.94):
        for pb, lab in [(1e-3 / 20, "20-bin tracking window"), (1e-2 / N_TOF, "relaxed 1e-2/pt"),
                        (1e-3, "known bin")]:
            k, s90 = tof_need(b, pb)
            print(f"  b={b:5.2f} {lab:24s} n_th={k:2d} s90={s90:5.1f}")

    print(f"\n=== FMCW, both ramps, two-stage, N_b={N_B}, N_w={N_W}")
    res = {}
    for name, L in [("steady", 0), ("8 looks", 8), ("4 looks", 4), ("2 looks", 2), ("1 look", 1)]:
        n, p1, p2, x1, x2 = two_stage(L)
        res[name] = (L, n, x1, x2)
        n50 = optimize.brentq(lambda m: pd_pair(m, L, x1, x2) - 0.5, 0.5, 1e5)
        print(f"  {name:8s} n90={n:6.1f} (per ramp {n/2:5.1f})  p1={p1:.1e} p2={p2:.1e} x1={x1:5.2f} x2={x2:5.2f}  "
              f"n50={n50:6.1f}  P_D(25)={pd_pair(25,L,x1,x2):.3f}  P_D(120)={pd_pair(120,L,x1,x2):.3f}  "
              f"P_D(88)={pd_pair(88,L,x1,x2):.3f}")
    print("\n  sensitivities (total photoelectrons, both ramps):")
    for name, L in [("steady", 0), ("4 looks", 4), ("1 look", 1)]:
        trk = two_stage(L, nb=20, nw=20)[0]
        rel = two_stage(L, pfa_pt=1e-2)[0]
        ps = pair_sum(L)
        print(f"  {name:8s} full {res[name][1]:6.1f} | pair-sum {ps:6.1f} | relaxed 1e-2/pt {rel:6.1f} | "
              f"tracking 20x20 bins {trk:6.1f} | one ramp full-search (range only) {one_ramp(L, N_B):6.1f}")
    for Tu, R in [(10e-6, 300.0), (10e-6, 200.0), (5e-6, 200.0)]:
        nb = R / 0.15 + 90e6 * Tu
        nw = 4 * 90e6 * Tu
        print(f"  check R={R:.0f} m, T_u={Tu*1e6:.0f} us: N_b={nb:.0f}, N_w={nw:.0f}: 4 looks {two_stage(4, nb, nw)[0]:.1f}, "
              f"1 look {two_stage(1, nb, nw)[0]:.1f}, steady {two_stage(0, nb, nw)[0]:.1f}")

    # FFT straddle (scalloping) loss, rectangular window, offset uniform over a bin
    d = np.linspace(-0.5, 0.5, 200001)
    g = np.sinc(d) ** 2
    d2 = np.linspace(-0.25, 0.25, 200001)
    g2 = np.sinc(d2) ** 2
    print(f"\nFFT straddle, rect window: mean {10*np.log10(g.mean()):.2f} dB, worst {10*np.log10(g.min()):.2f} dB;"
          f" 2x zero padding: mean {10*np.log10(g2.mean()):.2f} dB, worst {10*np.log10(g2.min()):.2f} dB")
    # background for the ToF central case
    r_bg = 5.93e8 / 0.3 * 0.37 * 0.5
    x = r_bg / 9 * 6e-9
    fd = x / (1 + x)
    print(f"ToF central background: r_bg = {r_bg:.3e}/s, x = {x:.4f}, f_dead = {fd:.4f}, "
          f"b = {r_bg*1e-9*10*(1-fd):.3f}, events over 20.8 us = {r_bg*20.8e-6*(1-fd):.0f}")
