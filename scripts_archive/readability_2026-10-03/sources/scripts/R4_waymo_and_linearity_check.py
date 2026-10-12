"""Arithmetic checks for items R4_C7-C7b_F6-01 and -02/-08.

(1) Waymo ADAS case (Piggott et al., arXiv:2502.09736, Table 1): reproduce the
    -106.1 dB worst-case link and 0.52 uJ per shot, and evaluate the report's
    Eq. (93) per chirp and per point (two chirps).
(2) Bianconi et al. (Nat. Commun. 16, 6739, 2025; SI Eq. 4) define the chirp
    nonlinearity sigma = RMS deviation from a least-squares line / excursion.
    For a parabolic bow, convert sigma to the report's Eq. (112) variables:
    the peak deviation from the chord, dnu_max, and the fractional
    peak-to-peak chirp-rate error eps = 8 dnu_max / B.

Usage:  python R4_waymo_and_linearity_check.py
No inputs, no network access; prints to stdout.
"""
import math

import numpy as np

C = 299_792_458.0
H = 6.62607015e-34
LAM = 1.55e-6
E_PH = H * C / LAM


def waymo():
    w0, R, rho = 10e-3, 250.0, 0.05
    zr = math.pi * w0 ** 2 / LAM
    w = w0 * math.sqrt(1 + (R / zr) ** 2)
    t_link = LAM ** 2 * rho / (2 * math.pi * math.pi * w ** 2)       # Waymo Eq. (15), A_eff = pi w^2
    a_mode_eq = LAM ** 2 * R ** 2 / (2 * math.pi * w ** 2)           # same link written as the report's A_mode
    e_shot = 2 * 50 * E_PH / t_link                                  # 2 chirps x 50 photons
    print("(1) Waymo ADAS case")
    print(f"    photon energy {E_PH:.4e} J; z_R {zr:.1f} m; w(250 m) {w * 1e3:.2f} mm")
    print(f"    link {10 * math.log10(t_link):.2f} dB (paper: -106.1 dB); "
          f"equivalent A_mode {a_mode_eq * 1e6:.1f} mm^2")
    print(f"    2 chirps x 50 photons -> {e_shot * 1e6:.3f} uJ per shot (paper 0.52 uJ); "
          f"x 1.2e7/s = {e_shot * 1.2e7:.2f} W (paper 6.2 W)")
    for loss_db in (3, 6):
        print(f"    with {loss_db} dB loss: {e_shot * 10 ** (loss_db / 10) * 1e6:.2f} uJ per point")
    print(f"    Waymo 10-20 W / 1.2e7 = {10 / 1.2e7 * 1e6:.2f}-{20 / 1.2e7 * 1e6:.2f} uJ per point")
    # report's Eq. (93) with its own A_mode = 74.5 mm^2 at 250 m
    a_mode = 74.5e-6
    for n, eta in ((50, 0.25), (100, 0.25), (100, 0.5), (90, 0.45), (90, 0.225)):
        e = n * E_PH * math.pi * R ** 2 / (rho * a_mode * eta)
        print(f"    Eq.(93): n = {n:3d}, eta = {eta:5.3f}, A_mode 74.5 mm^2 -> {e * 1e6:.2f} uJ")
    print()


def linearity():
    print("(2) Bianconi sigma_RMS -> report's Eq. (112) variables, parabolic bow")
    # numerical check of the analytic ratios on a parabola over [0, L]
    L, a = 1.0, 1.0
    t = np.linspace(0, L, 200001)
    f = a * t ** 2
    p = np.polyfit(t, f, 1)
    rms = np.sqrt(np.mean((f - np.polyval(p, t)) ** 2))
    chord = f - (f[-1] - f[0]) / L * t
    dnu_max = np.max(np.abs(chord))
    print(f"    dnu_max / dnu_rms = {dnu_max / rms:.4f} (analytic 3*sqrt(5)/2 = {1.5 * math.sqrt(5):.4f})")
    k_eps = 8 * dnu_max / rms
    print(f"    eps / sigma = 8 * dnu_max / dnu_rms = {k_eps:.3f} (analytic 12*sqrt(5) = {12 * math.sqrt(5):.3f})")
    B = 1e9
    tol_300 = C / (16 * 300.0)
    for name, sigma in (("SIL unpackaged 0.65%", 0.0065), ("E-DBR 1.5%", 0.015),
                        ("SIL packaged 0.08%", 0.0008)):
        d_rms = sigma * B
        d_max = 1.5 * math.sqrt(5) * d_rms
        eps = 12 * math.sqrt(5) * sigma
        print(f"    {name:22s}: dnu_rms {d_rms / 1e6:6.2f} MHz, dnu_max {d_max / 1e6:6.2f} MHz, "
              f"eps {eps:.4f}; x{d_max / tol_300:6.0f} the {tol_300 / 1e3:.1f} kHz tolerance "
              f"(eps/5e-4 = {eps / 5e-4:6.0f})")
    print("    reading the % as eps directly: 0.65% -> x13, 1.5% -> x30;"
          " as dnu_max/B: 6.5 and 15 MHz -> x104 and x240")
    # Siddharth et al. Fig. 3f: RMS 156.787 MHz over 10.4835 GHz
    print(f"    Siddharth Fig. 3f: 156.787 MHz / 10.4835 GHz = {156.787 / 10483.5 * 100:.3f}%")


if __name__ == "__main__":
    waymo()
    linearity()
