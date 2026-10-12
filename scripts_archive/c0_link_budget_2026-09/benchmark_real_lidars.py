"""Benchmark the C0 subsection 10 link-budget model against published lidar systems.

Every input below is from a primary source read for this check (see the SOURCES dict). The model is
the report's: direct detection  L = rho A_rx T^2/(pi R^2),  coherent  L = rho t^2 lambda^2 T^2/(2 pi^2 w(R)^2)
with the Gaussian w(R), and detection statistics of subsection 10.3.
"""
import numpy as np
from scipy.special import gammaincc, gammainccinv

H, C, Q = 6.62607015e-34, 2.99792458e8, 1.602176634e-19
eph = lambda lam: H * C / lam  # noqa: E731
db = lambda x: 10 * np.log10(x)  # noqa: E731


def w2(R, w0, lam, z_focus=0.0):
    zr = np.pi * w0**2 / lam
    return w0**2 * (1 + ((R - z_focus) / zr) ** 2), zr


def l_coh(R, w0, lam, rho, t2=1.0, z_focus=0.0):
    ww, _ = w2(R, w0, lam, z_focus)
    return rho * t2 * lam**2 / (2 * np.pi**2 * ww)


def pd_looks(n, m, pfa=1e-6):
    x = gammainccinv(m, pfa)
    return gammaincc(m, x / (1 + n / m))


print("=" * 100)
print("A. FMCW / coherent")
# 1. Waymo design point (Piggott et al. 2025, Table 1)
lam, w0, rho, R, E, qe = 1550e-9, 10e-3, 0.05, 250.0, 0.52e-6, 0.9
L = l_coh(R, w0, lam, rho)
ph_pt = E / eph(lam) * L
print(f"1 Waymo design: z_R = {np.pi * w0**2 / lam:.1f} m; L(250 m, 5%) = {db(L):.1f} dB (paper -106.1 dB); "
      f"photons per point {ph_pt:.0f}, per chirp {ph_pt / 2:.0f} (paper 50); photoelectrons per chirp "
      f"{qe * ph_pt / 2:.1f}; P_D with 4 looks at that count = {pd_looks(qe * ph_pt / 2, 4):.3f} (paper 0.90)")
# report pairing (eta, n_req) = (0.25, 30) vs Waymo's (0.9 lossless, 2 x 45)
print(f"  photon-equivalents per point: Waymo n/eta = {2 * 45 / 0.9:.0f}; report (old) 30/0.25 = {30 / 0.25:.0f}; "
      f"parallel re-baseline 120/(0.25 x 4 A_mode) = {120 / (0.25 * 4):.0f} per single-mode area")
# 2. Waymo lab validation (App. A): measured chain efficiency
eff = {"optics (BS, lens, mirror)": 0.403, "circulator + coupler": 0.549, "QE": 0.760, "Hann window": 0.667}
tot = np.prod(list(eff.values()))
print(f"2 Waymo lab: total {tot:.3f} ({db(tot):.1f} dB); without the window {tot / 0.667:.3f}; "
      f"vs report eta 0.25: {db(0.25 / tot):.1f} dB (with window), {db(0.25 / (tot / 0.667)):.1f} dB (without); "
      f"measured link 'independent of range' at 8 and 15 m (z_R of their beams not stated)")
# 3. Settembrini et al., Nature 651, 364 (2026): calibrated targets at 7.2 m, 25 mm lens, one acquisition
lam, w0, zf, P, T, eta_p, rpd, kappa = 1310e-9, 1.31e-3, 11.1, 178e-6, 32e-6, 0.23, 0.95, 0.62
pen = 1 / (1 + 1 / kappa**2)
ww, zr = w2(7.2, w0, lam, zf)
qe = rpd * H * C / (Q * lam)
for rho, snr_meas in ((0.5, 74.7), (0.1, 31.2), (0.05, 19.4)):
    prx_theirs = eta_p * (rho / np.pi) * P * lam**2 / (np.pi * ww)  # their Eq. 1 with rho(pi) = rho/pi
    n_theirs = rpd * prx_theirs * T / Q
    snr_theirs = 2 * n_theirs * pen  # their SNR = 2N, times the kappa penalty
    prx_ours = P * eta_p * l_coh(7.2, w0, lam, rho, 1.0, zf)  # report Eq. 33 with eta = eta_p
    n_ours = rpd * prx_ours * T / Q
    print(f"3 Settembrini {100 * rho:.0f}% @7.2 m: w(7.2) = {np.sqrt(ww) * 1e3:.2f} mm (z_R {zr:.1f} m, focus 11.1 m); "
          f"their model SNR(2N) = {snr_theirs:.1f}; report model N_eff = {n_ours * pen:.1f} (SNR=N) "
          f"= {2 * n_ours * pen:.1f} in their 2N units; measured {snr_meas} -> report model/measured "
          f"{db(2 * n_ours * pen / snr_meas):+.1f} dB")
print(f"  effective end-to-end efficiency eta_p x QE x noise penalty = {eta_p:.2f} x {qe:.2f} x {pen:.3f} = "
      f"{eta_p * qe * pen:.3f} ({db(0.25 / (eta_p * qe * pen)):.1f} dB below the report's 0.25); "
      f"retro/50% measured = {113715 / 74.7:.0f} ({db(113715 / 74.7):.1f} dB) -> rho_eq = {0.5 * 113715 / 74.7:.0f}, "
      f"R_A_eff = {0.5 * 113715 / 74.7 / np.pi:.0f} cd/lx/m2; retro/5% = {db(113715 / 19.4):.1f} dB, no blooming noticed")
# 4. indie / MicroTech whitepaper Fig. 6: 200 mW, 12 mm aperture, z_R ~ 70 m (values read off the plot)
zr = 70.0
w0 = np.sqrt(zr * 1550e-9 / np.pi)
read = {1: 42.5, 2: 42.0, 5: 42.3, 10: 42.8, 20: 43.5, 50: 39.5, 100: 34.5, 200: 26.5}
plateau = np.mean([read[r] for r in (1, 2, 5, 10, 20)])
print(f"4 indie Fig. 6: w0 for z_R = 70 m is {w0 * 1e3:.2f} mm (12 mm aperture); plateau {plateau:.1f} (plot units)")
for r in (50, 100, 200):
    model = -db(1 + (r / zr) ** 2)
    coh = db(np.exp(-2 * np.pi * 100e3 * 2 * r / C))
    print(f"   {r:3d} m: measured {read[r] - plateau:+.1f} dB, model {model:+.1f} dB, model + coherence loss of a "
          f"100 kHz laser {model + coh:+.1f} dB")
# 5. Wang et al. 2025 (Moore and More): 7 mm waist diameter, 10% board, SNR >= 10 dB at 200 m, 18 us ramps
w0 = 3.5e-3
ww, zr = w2(200.0, w0, 1550e-9)
L = l_coh(200.0, w0, 1550e-9, 0.1)
need = 10.0 / (18e-6 / eph(1550e-9) * L)  # P_tx * eta for N = 10 photoelectrons per ramp
print(f"5 Wang: z_R = {zr:.1f} m; beam diameter at 200 m {2 * np.sqrt(ww) * 1e3:.1f} mm (paper 56.8 mm); "
      f"L(200 m,10%) = {db(L):.1f} dB; SNR 10 dB (N=10 per 18 us ramp) needs P_tx*eta >= {need * 1e3:.1f} mW "
      f"(e.g. {need / 0.25 * 1e3:.0f} mW at eta 0.25, {need / 0.112 * 1e3:.0f} mW at 0.112); TX power not published")

print("=" * 100)
print("B. Direct-detection ToF (n_req = 25 counts per point unless stated)")


def implied_eta_area(n, lam, R, rho, E):
    return n * eph(lam) * np.pi * R**2 / (rho * E)  # eta * A_rx (m^2) needed


for name, P, px, fps, lam, R, rho in (("6 Toshiba ISSCC 2018 (SiPM, 70 klux)", 50e-3, 240 * 96, 10, 905e-9, 200.0, 0.10),
                                      ("7 Toyota ISSCC 2013 (SPAD, 70 klux)", 21e-3, 202 * 96, 10, 870e-9, 100.0, 0.09)):
    E = P / (px * fps)
    ea = implied_eta_area(25, lam, R, rho, E)
    ea9 = implied_eta_area(25 / 9, lam, R, rho, E)
    dia = lambda eta, a: 2 * np.sqrt(a / eta / np.pi) * 1e3  # noqa: E731
    print(f"{name}: E per point {E * 1e9:.0f} nJ; implied eta*A_rx = {ea * 1e4:.2f} cm2 "
          f"(D = {dia(0.05, ea):.0f} mm at eta 0.05, {dia(0.1, ea):.0f} mm at 0.10); with 9-pixel accumulation "
          f"{ea9 * 1e4:.3f} cm2 (D = {dia(0.05, ea9):.0f} mm at eta 0.05); report default 0.185 x 25 mm = "
          f"{0.185 * np.pi * 0.0125**2 * 1e4:.2f} cm2")
print("8 Toshiba vs Toyota: '1.4x longer range at the same laser power' -> x1.96 in eta*A_rx/n_req at fixed E per point")
# 9. Panasonic Hirose 2018: 1.2 kW x 10 ns = 12 uJ per pulse over 688 x 384 pixels, f/1.4 lens, 10% (their assumptions)
E_px = 1.2e3 * 10e-9 / (688 * 384)
for f_mm in (22.0, 44.0):
    D = f_mm / 1.4 * 1e-3
    ph100 = E_px / eph(940e-9) * 0.1 * D**2 / (4 * 100.0**2)
    print(f"9 Panasonic: {E_px * 1e12:.1f} pJ per pixel per pulse; with f = {f_mm:.0f} mm (D = {D * 1e3:.1f} mm) "
          f"photons per pixel per pulse at the lens at 100 m = {ph100:.2f} (paper: below 1 beyond 100 m)")
# 10. Products: what the report model says they must emit (25 mm lens, eta 0.185, n_req 25, clear air ignored)
print("10 Products (inverse check; power and aperture unpublished):")
for name, lam, R, rate in (("Ouster OS2-128 Rev7, 865 nm, 200 m @10%, >90% P_D, 100 klx", 865e-9, 200.0, 2.62e6),
                           ("Hesai AT128, 905 nm, 200 m @10% (180-210)", 905e-9, 200.0, 1.536e6),
                           ("Livox HAP, 905 nm, 150 m @10%, 100 klx", 905e-9, 150.0, 452e3)):
    for D in (0.020, 0.025, 0.030):
        E = 25 * eph(lam) * 4 * R**2 / (0.1 * 0.185 * D**2)
        print(f"   {name}: D = {D * 1e3:.0f} mm -> {E * 1e9:.0f} nJ per point, average optical {E * rate:.2f} W")
