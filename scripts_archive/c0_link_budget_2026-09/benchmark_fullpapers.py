"""Benchmark checks from the full papers the author supplied (Wang 2025, Sony ISSCC 2021, Settembrini 2026 + PRF)."""
import numpy as np

H, C = 6.62607015e-34, 2.99792458e8
eph = lambda lam: H * C / lam  # noqa: E731
db = lambda x: 10 * np.log10(x)  # noqa: E731

# ---- Wang et al. 2025 (Moore and More 2:12): 7 mm waist diameter, 100 kHz laser, 10% board, Fig. 7c/7d
lam, w0, dnu = 1550e-9, 3.5e-3, 100e3
zr = np.pi * w0**2 / lam
R = np.array([20, 40, 60, 80, 100, 120, 140, 160, 180, 200.0])
geo = -db(1 + (R / zr) ** 2)
coh = db(np.exp(-4 * np.pi * dnu * R / C))  # their Eq. 2 factor, same as e^{-2 pi dnu tau}
model = geo + coh
snr_ch1 = np.array([25, 23, 20, 18.5, 17, 16, 15, 13, 11, 10.0])  # read from Fig. 7d (CH1 squares)
pk_ch1 = np.array([-29.5, -32, -34, -37, -38, -39.5, -40, -42, -43, -45.0])  # Fig. 7c peaks (dBm)
print(f"Wang: z_R = {zr:.1f} m; coherence loss at 200 m = {-coh[-1]:.2f} dB (paper: 3.6 dB)")
print(" R(m)  model rel.20m  SNR_CH1 rel.  peak rel.")
for r, m, s, p in zip(R, model - model[0], snr_ch1 - snr_ch1[0], pk_ch1 - pk_ch1[0]):
    print(f" {r:4.0f}   {m:+6.1f}        {s:+6.1f}       {p:+6.1f}")
# which waist would fit the 20->200 m drop of ~15.5 dB?
for w in (3.5e-3, 4.0e-3, 4.5e-3, 5.0e-3):
    z = np.pi * w**2 / lam
    drop = db((1 + (200 / z) ** 2) / (1 + (20 / z) ** 2)) + (coh[0] - coh[-1])
    print(f"   w0 = {w * 1e3:.1f} mm: z_R = {z:.0f} m, model 20->200 m drop = {drop:.1f} dB")
L200 = 0.1 * lam**2 / (2 * np.pi**2 * w0**2 * (1 + (200 / zr) ** 2))
for conv, N in (("SNR = N", 10.0), ("SNR = 2N", 5.0)):
    ptx_eta = N * eph(lam) / (18e-6 * L200 * np.exp(-4 * np.pi * dnu * 200 / C))
    print(f"   implied P_tx*eta for 10 dB at 200 m ({conv}): {ptx_eta * 1e3:.1f} mW "
          f"(P_tx {ptx_eta / 0.3 * 1e3:.0f} mW at eta 0.3); L(200 m) = {db(L200):.1f} dB")

# ---- Sony ISSCC 2021: 905 nm, 45 W peak, 4.5 ns, shot period 3.04 us, slots 721.76/761.6 us, 63 slots/frame
Ep = 45 * 4.5e-9
shots_slot = 721.76e-6 / 3.04e-6
shots_col = shots_slot / 168 * 63  # MEMS sweeps the 168 columns once per slot, 63 slots per frame
E_pt = Ep / 63 * shots_col  # each pulse lights a vertical line of 63 macro-pixels
Pavg = Ep / 3.04e-6 * (721.76 / 761.6)
print(f"\nSony: pulse {Ep * 1e9:.0f} nJ; average {Pavg * 1e3:.0f} mW; {shots_slot:.0f} shots/slot -> {shots_col:.0f} "
      f"shots per point per frame; E per point = {E_pt * 1e9:.0f} nJ (points/s {168 * 63 * 20:,}; "
      f"check {Pavg / (168 * 63 * 20) * 1e9:.0f} nJ)")
eta = 0.5 * 0.22 * 0.804
for nreq in (25.0, 18.4):
    etaA = nreq * eph(905e-9) * np.pi * 150.0**2 / (0.1 * E_pt)
    for eo in (0.5, 0.7):
        A = etaA / (eo * 0.22 * 0.804)
        D = 2 * np.sqrt(A / np.pi)
        print(f"   n_req {nreq}: eta*A = {etaA * 1e4:.3f} cm2; optics {eo}: A = {A * 1e4:.2f} cm2, D = {D * 1e3:.1f} mm, "
              f"f/{11.46e-3 / D:.2f} for the 0.15-degree 30 um macro-pixel (f = 11.5 mm)")

# ---- Analog Photonics FS-4S datasheet (via the Nature peer review file): 200 m @10%, 90 kpts/s, <=0.04 x 0.02 deg FWHM
th = np.deg2rad(np.array([0.04, 0.02])) / 1.177  # 1/e2 half-angle from FWHM full angle
wx, wy = lam / (np.pi * th)
zx, zy = np.pi * wx**2 / lam, np.pi * wy**2 / lam
Rt = 200.0
wwx = wx**2 * (1 + (Rt / zx) ** 2)
wwy = wy**2 * (1 + (Rt / zy) ** 2)
L = 0.1 * lam**2 / (2 * np.pi**2 * np.sqrt(wwx * wwy))
print(f"\nFS-4S: w0 = {wx * 1e3:.2f} x {wy * 1e3:.2f} mm (z_R {zx:.1f} / {zy:.1f} m); L(200 m, 10%) = {db(L):.1f} dB")
for eta_, n in ((0.25, 30.0), (0.112, 30.0), (0.25, 120.0 / 4)):
    E = n * eph(lam) / (eta_ * L)
    print(f"   eta {eta_}, n {n}: E per point {E * 1e6:.1f} uJ -> {E * 90e3:.2f} W average at 90 kpts/s")
