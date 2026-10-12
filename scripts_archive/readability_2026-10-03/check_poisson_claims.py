"""Check the photon-counting numbers that the Round 1 edits add to Section C0 subsection 10.3 and 10.5.

The model (Section C0 subsection 10.3): 2,000 range bins of 1 ns per ramp, at most 1e-3 false points per point,
so a per-bin false-alarm probability p = 1e-3 / 2,000 = 5e-7. The threshold n_th is the smallest count whose
Poisson tail P(N >= n_th | b) is at most p, and the signal s needed is the one for which
P(N >= n_th | s + b) = 0.9. b = r_bg * dt_bin * N_shots * live_fraction.
Claims checked:
- paralyzable dead time (live 0.784): b = 2.87, n_th = 15, s = 17.26 (s + b = 20.13);
- non-paralyzable dead time (dead 0.196): b = 2.94, n_th = 16, s = 18.4;
- 5, 10, 20 shots per point (b = 1.43, 2.87, 5.73): s = 14.0, 17.3, 22.5.
Usage: python check_poisson_claims.py
"""
from scipy.optimize import brentq
from scipy.stats import poisson

P_BIN = 1e-3 / 2000
R_BG, DT = 3.66e8, 1e-9


def tail(n, mu):
    return poisson.sf(n - 1, mu)  # P(N >= n)


def threshold(b):
    n = 1
    while tail(n, b) > P_BIN:
        n += 1
    return n


def signal_needed(b):
    n = threshold(b)
    return n, brentq(lambda s: tail(n, s + b) - 0.9, 0.0, 200.0)


for label, live, shots in [("paralyzable, 10 shots", 0.784, 10), ("non-paralyzable, 10 shots", 1 - 0.244 / 1.244, 10),
                           ("paralyzable, 5 shots", 0.784, 5), ("paralyzable, 20 shots", 0.784, 20)]:
    b = R_BG * DT * shots * live
    n, s = signal_needed(b)
    print(f"{label:28s} b = {b:.3f}  n_th = {n}  tail(n_th-1) = {tail(n - 1, b):.2e}  tail(n_th) = {tail(n, b):.2e}"
          f"  s = {s:.2f}  s + b = {s + b:.2f}")
