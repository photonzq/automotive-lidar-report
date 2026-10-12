"""Photoelectrons needed for detection: SPAD ToF (Poisson) vs coherent FMCW (FFT bin),
including FMCW's up/down ramp split and bins searched.  All statistics per point."""
import numpy as np
from scipy import stats, optimize, integrate, special

PD = 0.9


# ---------------- photon counting (SPAD histogram), non-fading Poisson
def tof_required(b, pfa_bin):
    n_th = 0
    while stats.poisson.sf(n_th - 1, b) > pfa_bin:      # P(N >= n_th | b)
        n_th += 1
    s = optimize.brentq(lambda s: stats.poisson.sf(n_th - 1, s + b) - PD, 1e-6, 500)
    return n_th, s


# ---------------- coherent, one FFT bin, noise-only power ~ Exp(1)
def pd_steady(n, x):            # Marcum Q1(sqrt(2n), sqrt(2x))
    return stats.ncx2.sf(2 * x, 2, 2 * n)


def pd_one_speckle(n, x):
    return np.exp(-x / (1 + n))


def thr_L(L, pfa):              # sum of L unit exponentials exceeds x with prob pfa
    return stats.gamma.isf(pfa, L)


def pd_L(n, L, x):              # L looks summed, total mean n split equally, fading iid per look
    return special.gammaincc(L, x / (1 + n / L))


def solve(f):
    return optimize.brentq(lambda n: f(n) - PD, 1e-3, 1e5)


# ---------------- two ramps, fading common to both ramps (same speckle), noise independent
def pd_pair_steady(nr, x1, x2):
    return pd_steady(nr, x1) * pd_steady(nr, x2)


def pd_pair_L(nr, L, x1, x2):
    # per ramp: sum of L looks; look powers (nr/L)*A_l, A_l ~ Exp(1) iid; S = sum A_l ~ Gamma(L,1)
    def integrand(S):
        lam = 2 * nr * S / L
        return (stats.ncx2.sf(2 * x1, 2 * L, lam) * stats.ncx2.sf(2 * x2, 2 * L, lam)
                * stats.gamma.pdf(S, L))
    val, _ = integrate.quad(integrand, 0, np.inf, limit=400)
    return val


# ================================================================ ToF
print("=== SPAD ToF, photon counting, P_D = 0.9")
for label, nbins, pfa_pt in [("report basis: 1e-6 per bin", 1, 1e-6),
                             ("300 m, 2,000 bins, 1e-3 false points per point", 2000, 1e-3)]:
    for b, cond in [(0.01, "night"), (2.2, "bright sun")]:
        n_th, s = tof_required(b, pfa_pt / nbins)
        print(f"  {label:48s} {cond:10s} b={b:<5} n_th={n_th:2d}  signal needed s={s:5.1f}")

# ================================================================ FMCW single look (all photons in one ramp)
print("\n=== Coherent, all photons in ONE ramp (report basis), P_D = 0.9")
for label, pfa_bin in [("1e-6 per bin (report)", 1e-6), ("1e-3/2,700 bins", 1e-3 / 2700)]:
    x = -np.log(pfa_bin)
    print(f"  {label:26s} x_th={x:5.2f}  steady={solve(lambda n: pd_steady(n, x)):6.1f}"
          f"  4-look={solve(lambda n: pd_L(n, 4, thr_L(4, pfa_bin))):6.1f}"
          f"  1-speckle={solve(lambda n: pd_one_speckle(n, x)):6.1f}")

# ================================================================ FMCW two ramps
R, dR, fD, Tu = 300.0, 0.15, 90e6, 7.5e-6
Nb = R / dR + fD * Tu                 # bins per ramp from 0 to f_b,max
Nwin = 2 * fD * Tu                    # down-ramp bins consistent with +-f_D,max around the up-ramp result
print(f"\nbins per ramp = {Nb:.0f}; confirmation window = {Nwin:.0f} bins")
pfa_pt = 1e-3

# (A) independent detection in each ramp, then pairing: 2*Nb bins searched
p = pfa_pt / (2 * Nb)
x = -np.log(p)
xL = thr_L(4, p)
nr_s = optimize.brentq(lambda n: pd_pair_steady(n, x, x) - PD, 1, 1e4)
nr_1 = optimize.brentq(lambda n: pd_pair_L(n, 1, x, x) - PD, 1, 1e5)
nr_4 = optimize.brentq(lambda n: pd_pair_L(n, 4, xL, xL) - PD, 1, 1e5)
print(f"(A) independent per-ramp thresholds, p_bin={p:.2e}, x_th={x:.2f}")
print(f"    per ramp: steady {nr_s:6.1f}, 4-look {nr_4:6.1f}, 1-speckle {nr_1:6.1f}  -> total x2")

# (B) two-stage: detect in up-ramp over Nb bins (p1), confirm in down-ramp over Nwin bins (p2),
#     false point ~ Nb*p1*Nwin*p2 = pfa_pt ; choose split to minimise photons
best = {}
for name, L in [("steady", 0), ("4-look", 4), ("1-speckle", 1)]:
    res = []
    for log_p1 in np.linspace(-9, -3, 25):
        p1 = 10 ** log_p1
        p2 = pfa_pt / (Nb * p1 * Nwin)
        if p2 >= 1:
            continue
        if L == 0:
            x1, x2 = -np.log(p1), -np.log(p2)
            f = lambda n: pd_pair_steady(n, x1, x2) - PD
        else:
            x1, x2 = thr_L(L, p1), thr_L(L, p2)
            f = lambda n, L=L, x1=x1, x2=x2: pd_pair_L(n, L, x1, x2) - PD
        nr = optimize.brentq(f, 1, 1e5)
        res.append((nr, p1, p2))
    best[name] = min(res)
    nr, p1, p2 = best[name]
    print(f"(B) two-stage {name:9s}: per ramp {nr:6.1f} (total {2*nr:6.1f}) at p1={p1:.1e}, p2={p2:.1e}")
