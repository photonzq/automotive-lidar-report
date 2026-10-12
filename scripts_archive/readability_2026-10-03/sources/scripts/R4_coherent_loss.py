"""Coherent-loss check for item R4_C7-C7b_F6-07 (and -02/-08 context).

Evaluates the report's Eq. (109) (numbered (113) before the report's equations
were renumbered on 5 Oct 2026),
    sigma^2 = integral_{1/T_u}^{inf} S_nu(f) * 4 sin^2(pi f tau) / f^2 df,
and Eq. (110) (formerly (114)), eta_coh = exp(-sigma^2), for frequency-noise spectra read off
published figures, and compares the result with the report's shortcut of
inserting a linewidth into eta = exp(-2 pi dnu tau) as if it were Lorentzian.

Spectra (one-sided frequency-noise PSD S_nu in Hz^2/Hz), each a white floor
plus a power law, read by eye from the rendered figures:
  EDBR_S : Siddharth et al., arXiv:2408.01743v1, Fig. 3(d): white floor with
           pi*S0 = 2.8 kHz (S0 = 891), thermal-charge-carrier line through
           1e6 at 1 kHz and ~1e2 at 2.5 MHz (slope -1.18).
  EDBR_B : Bianconi et al., Nat. Commun. 16, 6739 (2025), Fig. 1(c), blue:
           floor ~1.2e3, ~1e4 at 100 kHz, ~2e3 at 1 MHz (slope ~ -1.25 above
           the floor, anchored at 1e4 at 100 kHz).
  SIL_B  : same figure, red: floor ~2, ~15 at 100 kHz, ~100 at 10 kHz.
  DFB_B  : same figure, green: floor ~2e5 above ~200 kHz (for reference).
These are approximations of digitised curves, good to a factor of ~1.5 in S.

Usage:  python R4_coherent_loss.py
No inputs, no network access; prints a table to stdout.
"""
import math

import numpy as np
from scipy import integrate

C = 299_792_458.0


def spectra():
    return {
        "EDBR_S (Siddharth Fig.3d)": lambda f: 891.0 + 1e6 * (f / 1e3) ** -1.18,
        "EDBR_B (Bianconi Fig.1c)": lambda f: 1.2e3 + 1e4 * (f / 1e5) ** -1.25,
        "SIL_B  (Bianconi Fig.1c)": lambda f: 2.0 + 15.0 * (f / 1e5) ** -0.85,
        "DFB_B  (Bianconi Fig.1c)": lambda f: 2.0e5 + 2.0e5 * (f / 2e5) ** -1.3,
    }


def sigma2(S, tau, T_u, f_max=1e10):
    """Phase variance of Eq. (113), integrated on a log grid (lower limit 1/T_u)."""
    f_lo = 1.0 / T_u
    g = lambda lf: (S(math.exp(lf)) * 4.0 * math.sin(math.pi * math.exp(lf) * tau) ** 2
                    / math.exp(lf) ** 2) * math.exp(lf)
    # split the log range so the oscillating tail is resolved
    edges = np.linspace(math.log(f_lo), math.log(f_max), 400)
    total = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        val, _ = integrate.quad(g, a, b, limit=200)
        total += val
    return total


def main():
    print("Eq. (113)-(114) with measured spectra vs Lorentzian shortcut\n")
    cases = [(300.0, 7.5e-6), (300.0, 2.25e-6), (300.0, 16e-6), (200.0, 7.5e-6)]
    lorentz = {"EDBR": 378e3, "SIL": 42e3, "DFB": 802e3}
    for R, T_u in cases:
        tau = 2 * R / C
        print(f"R = {R:.0f} m, tau = {tau * 1e6:.3f} us, T_u = {T_u * 1e6:.2f} us "
              f"(lower limit 1/T_u = {1 / T_u / 1e3:.0f} kHz)")
        for name, S in spectra().items():
            s2 = sigma2(S, tau, T_u)
            eta = math.exp(-s2)
            print(f"   {name:28s} sigma^2 = {s2:8.4f}  eta = {eta:.3f}  "
                  f"loss = {-10 * math.log10(eta):6.2f} dB")
        for key, dnu in lorentz.items():
            s2 = 2 * math.pi * dnu * tau
            print(f"   shortcut, {key} {dnu / 1e3:5.0f} kHz as Lorentzian: "
                  f"2 pi dnu tau = {s2:6.3f}, loss = {10 * s2 / math.log(10):6.2f} dB")
        # white floors alone, for reference
        for key, dnu in (("EDBR intrinsic 2.8 kHz", 2.8e3), ("SIL intrinsic 3 Hz", 3.0)):
            s2 = 2 * math.pi * dnu * tau
            print(f"   white floor only, {key}: loss = {10 * s2 / math.log(10):7.4f} dB")
        print()


if __name__ == "__main__":
    main()
