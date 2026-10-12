"""R2 item 05 check: photoelectrons needed for P_D = 0.9 with n averaged speckles (Piggott et al. 2025).

Model (Piggott et al., arXiv:2502.09736, Sec. 3.2, Eqs. (28)-(34)): each acquisition's FFT-bin energy
is exponential with mean N+1 (N signal photoelectrons, 1 photoelectron of shot noise); summing n
independent speckle realisations gives a Gamma(n) variable. The threshold t sets P_FA per bin;
P_D = P(Gamma(n, scale=N+1) > t). The x-axis of their Fig. 8(b) is the total n*N.

Also converts Table 1's link numbers to received photons per shot and per chirp, and redoes the
report's Eq. (93) single-receiver energy with 45 photoelectrons instead of 50.
"""
from scipy.optimize import brentq
from scipy.stats import gamma

H, C = 6.62607015e-34, 2.99792458e8


def total_pe_for_pd(n, pfa=1e-6, pd=0.9):
    t = gamma.isf(pfa, a=n, scale=1.0)
    f = lambda N: gamma.sf(t, a=n, scale=N + 1.0) - pd
    N = brentq(f, 1e-6, 1e5)
    return n * N, t


for n in (1, 2, 4, 6, 8):
    tot, t = total_pe_for_pd(n)
    print(f"n={n}: threshold t={t:.2f}; total photoelectrons for P_D=0.9 at 1e-6: {tot:.1f}")

e_ph = H * C / 1550e-9
link = 10 ** (-106.1 / 10)
per_shot = 0.52e-6 * link / e_ph
print(f"E_ph(1550 nm) = {e_ph:.4e} J; received photons per 0.52 uJ shot = {per_shot:.1f}; per chirp = {per_shot/2:.1f}")
print(f"50 photons x QE 0.9 = {50*0.9:.1f} photoelectrons")

# Report Eq. (93) check (single receiver, A_mode = 74.5 mm^2, rho = 0.05, eta = 0.25, R = 250 m)
import math
for npe in (50, 45):
    E = npe * 1.28e-19 * math.pi * 250**2 / (0.05 * 7.45e-5 * 0.25)
    print(f"n_req={npe}: E_pt = {E*1e6:.3f} uJ (one receiver); /4 = {E/4*1e6:.3f} uJ")
