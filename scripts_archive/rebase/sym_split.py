"""Two-stage FMCW detection with a symmetric per-bin false-alarm split p1 = p2."""
import numpy as np
from scipy import stats, optimize, integrate

PD, PFA_PT, N_B, N_W = 0.9, 1e-3, 2450, 1800
p = np.sqrt(PFA_PT / (N_B * N_W))


def thr(L):
    return -np.log(p) if L == 0 else stats.gamma.isf(p, L)


def pd_pair(n, L):
    x, nr = thr(L), n / 2
    if L == 0:
        return stats.ncx2.sf(2 * x, 2, 2 * nr) ** 2
    g = lambda S: stats.ncx2.sf(2 * x, 2 * L, 2 * nr * S / L) ** 2 * stats.gamma.pdf(S, L)
    return integrate.quad(g, 0, np.inf, limit=400)[0]


print(f"symmetric split: p = {p:.3e} per bin, x(L=1) = {thr(1):.2f}, x(L=4) = {thr(4):.2f}")
for L in (0, 8, 4, 2, 1):
    n90 = optimize.brentq(lambda n: pd_pair(n, L) - PD, 1, 1e4)
    n50 = optimize.brentq(lambda n: pd_pair(n, L) - 0.5, 1, 1e4)
    print(f"L={L}: n90 = {n90:6.1f}, n50 = {n50:5.1f}, P_D(25) = {pd_pair(25, L):.3f}, P_D(120) = {pd_pair(120, L):.3f}")
