"""Round 2: photon-counting numbers of §C0 subsection 10.3-10.4 with the 0.05 x 0.05 deg macro-pixel.

Central bright-sun background 1.83e8 counts/s per macro-pixel (nine SPADs, 6 ns dead time), 1 ns bins,
2,000 bins, at most 1e-3 false points per point (5e-7 per bin), 90 % detection; 10 shots per point unless stated.
Usage: python check_poisson_claims_round2.py
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import poisson

P_BIN = 1e-3 / 2000
R_BG, DT, TAU = 1.83e8, 1e-9, 6e-9


def need(b):
    n = 1
    while poisson.sf(n - 1, b) > P_BIN:
        n += 1
    s90 = brentq(lambda s: poisson.sf(n - 1, s + b) - 0.9, 0.0, 300.0)
    s50 = brentq(lambda s: poisson.sf(n - 1, s + b) - 0.5, 0.0, 300.0)
    return n, s90, s50


x = R_BG / 9 * TAU
for label, live, shots in [("paralyzable, 10 shots", np.exp(-x), 10), ("non-paralyzable, 10 shots", 1 / (1 + x), 10),
                           ("paralyzable, 5 shots", np.exp(-x), 5), ("paralyzable, 20 shots", np.exp(-x), 20)]:
    b = R_BG * DT * shots * live
    n, s90, s50 = need(b)
    print(f"{label:28s} r tau = {x:.4f}, live {live:.4f}, b = {b:.3f}, n_th = {n}, tail(n_th-1) = {poisson.sf(n - 2, b):.2e}, "
          f"tail(n_th) = {poisson.sf(n - 1, b):.2e}, s(0.9) = {s90:.2f} (s+b {s90 + b:.2f}), s(0.5) = {s50:.2f}")
print(f"events per point in 20.8 us: {R_BG * 20.8e-6 * np.exp(-x):.0f} background + 21.7 signal")
print(f"Poisson spread of the background events: sqrt = {np.sqrt(R_BG * 20.8e-6 * np.exp(-x)):.1f}")
