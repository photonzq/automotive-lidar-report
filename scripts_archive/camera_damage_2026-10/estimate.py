"""Arithmetic of the camera-damage estimate in §C4c subsection 1 ("How likely is damage in practice").

Model: a lidar pulse of energy E_p leaves as a beam of diameter d0 with full divergence theta_b; a camera with
entrance pupil D at range R collects eta = (D / (d0 + theta_b R))^2 of it (1 within R1 = (D - d0) / theta_b) and
focuses it on a spot of diameter ds, so the fluence per pulse is F = eta E_p / (pi ds^2 / 4).
Damage is possible out to R_max = (D sqrt(E_p / (F_th pi ds^2 / 4)) - d0) / theta_b, given the pulse count of the
measurement behind F_th (Bi et al., Fig. 4: 4 ns pulses at 50-100 kHz for 50 ms, i.e. 2,500-5,000 pulses).
Pulses per frame on one camera: (theta_b + D/R)^2 / (dtheta_h dtheta_v) for the Falcon K1 sample spacings.
Usage: python estimate.py
"""
import math

LAM = 1.55e-6                      # m
D0, THB = 2e-3, 1e-3               # beam diameter at the window (m), full divergence (rad)
DS = 20e-6                         # focal spot diameter on the sensor (m)
F_TH = 0.026                       # J/cm^2: lowest of Bi et al.'s 4 ns thresholds at 50-100 kHz (26-31, Fig. 4)
N_PULSES = 2500                    # pulses in Bi et al.'s 50 kHz, 50 ms runs (their minimum, p. 4716)
SPACINGS = {"ROI 0.09 x 0.08 deg": (0.09, 0.08), "outside 0.18 x 0.24 deg": (0.18, 0.24)}
FRAMES = 10                        # frames/s


def area_cm2(ds):
    return math.pi * (ds * 100) ** 2 / 4


def eta(D, R):
    return min(1.0, (D / (D0 + THB * R)) ** 2)


def r_max(D, Ep, Fth=F_TH, ds=DS):
    return (D * math.sqrt(Ep / (Fth * area_cm2(ds))) - D0) / THB


def per_frame(D, R):
    w = math.degrees(THB + D / R)
    return w, [w * w / (a * b) for a, b in SPACINGS.values()]


def minutes_for(n_per_frame):
    return N_PULSES / (n_per_frame * FRAMES) / 60


A = area_cm2(DS)
print(f"spot area for {DS*1e6:.0f} um: {A:.3e} cm^2")

# beam from the patent geometry: 200 um pitch and 1 deg spacing; SMF mode-field diameter 10.4 um
fc = 200e-6 / 0.0175
w0 = 5.2e-6
half = LAM / (math.pi * w0)
print(f"collimator f_c = {fc*1e3:.1f} mm; mode half-angle = {half:.3f} rad; beam = {2*half*fc*1e3:.2f} mm; "
      f"divergence = {2*w0/fc*1e3:.2f} mrad; 0.08 deg = {math.radians(0.08)*1e3:.2f} mrad")
for N in (1.8, 2.8):
    print(f"Airy diameter 2.44 lambda N at f/{N}: {2.44*LAM*N*1e6:.1f} um")
print(f"image of the beam cross-section d0 f/R, f = 14 mm, R = 1 m: {D0*14e-3/1.0*1e6:.0f} um")

# pulse energy from a 2 W source
print(f"Lumispot: 1.4 kW x 3 ns = {1.4e3*3e-9*1e6:.1f} uJ; 2 W / 500 kHz = {2/5e5*1e6:.1f} uJ; "
      f"2 W / 900 kHz = {2/9e5*1e6:.2f} uJ")

# Bi et al.: peak and average irradiance at threshold; pulse counts of the runs
for F, tau in ((0.017, 4e-9), (0.025, 4e-9), (0.037, 10e-9), (0.043, 10e-9)):
    print(f"peak irradiance {F*1e3:.0f} mJ/cm^2 / {tau*1e9:.0f} ns = {F/tau/1e6:.2f} MW/cm^2")
print(f"average irradiance at 20 mJ/cm^2 x 400 kHz = {0.020*4e5/1e3:.1f} kW/cm^2; peak at 4 ns = {0.020/4e-9/1e6:.1f} MW/cm^2")
print(f"pulses in 50 ms: 50 kHz {50e3*0.05:.0f}, 100 kHz {100e3*0.05:.0f}, 400 kHz {400e3*0.05:.0f}; "
      f"spacing 50 kHz {1/50e3*1e6:.0f} us, 100 kHz {1/100e3*1e6:.0f} us")

# close-up: phone telephoto, 14 mm f/2.8, at 1 m
D = 14e-3 / 2.8
f20, f28 = 2e-6 / A, 2e-6 / area_cm2(28e-6)
print(f"telephoto R1 = {(D-D0)/THB:.1f} m; F(20 um) = {f20:.3f} J/cm^2 ({f20/F_TH:.1f} x F_th); "
      f"F(28 um) = {f28:.3f} J/cm^2 ({f28/F_TH:.1f} x F_th)")
w, n = per_frame(D, 1.0)
print(f"telephoto at 1 m: window {w:.3f} deg; {n[0]:.2f} and {n[1]:.2f} pulses/frame; "
      f"{n[1]*FRAMES:.0f}-{n[0]*FRAMES:.0f} /s; {N_PULSES} pulses in {N_PULSES/(n[0]*FRAMES):.0f}-{N_PULSES/(n[1]*FRAMES):.0f} s")
print(f"average power on the spot: 2 uJ x 160 /s = {2e-6*160*1e3:.2f} mW = {2e-6*160/A/1e3:.3f} kW/cm^2")

# table: R1, R_max at the measured threshold, and the time a fixed camera at R_max needs for 2,500 pulses
s2 = math.sqrt(2e-6 / (F_TH * A))
print(f"sqrt(2 uJ / (F_th x A)) = {s2:.2f}; telephoto R_max = ({s2:.2f} x 5 - 2) mm / 1 mrad = {(s2*5-2):.1f} m")
cams = [("phone main 6.3 mm f/1.8", 6.3e-3, 1.8), ("phone telephoto 14 mm f/2.8", 14e-3, 2.8),
        ("camera lens 50 mm f/4", 50e-3, 4.0), ("telephoto lens 200 mm f/2.8", 200e-3, 2.8),
        ("car front 6 mm f/1.8", 6e-3, 1.8), ("car fisheye 1.2 mm f/2", 1.2e-3, 2.0)]
for name, f, N in cams:
    D = f / N
    r1 = (D - D0) / THB
    rs = " / ".join(f"{r_max(D, Ep):.1f}" for Ep in (1e-6, 2e-6, 10e-6))
    R = r_max(D, 2e-6)
    w, n = per_frame(D, R)
    print(f"{name:28s} D = {D*1e3:5.2f} mm  R1 = {r1:6.1f} m  R_max (1/2/10 uJ) = {rs} m  "
          f"at R_max(2 uJ): window {(THB + D/R)*1e3:.2f} mrad, {n[1]:.3f}-{n[0]:.3f}/frame, "
          f"{N_PULSES} pulses in {minutes_for(n[0]):.1f}-{minutes_for(n[1]):.1f} min")

# cameras on other cars
for label, D, R, Ep in (("front camera 3.3 mm at 5 m, 2 uJ", 3.3e-3, 5.0, 2e-6),
                        ("front camera 3.3 mm at 5 m, 10 uJ", 3.3e-3, 5.0, 10e-6),
                        ("fisheye 0.6 mm at 4.5 m, 2 uJ", 0.6e-3, 4.5, 2e-6)):
    e = eta(D, R)
    w, n = per_frame(D, R)
    F = e * Ep / A
    print(f"{label:34s} eta = {e:.4f}  F = {F*1e3:.1f} mJ/cm^2 ({F/F_TH:.1f} x F_th)  "
          f"{n[1]:.2f}-{n[0]:.2f}/frame; {N_PULSES} pulses in {minutes_for(n[0]):.1f}-{minutes_for(n[1]):.1f} min")
print(f"fisheye at the window: {(0.6/2)**2*2e-6/A*1e3:.1f} mJ/cm^2")

# 905/940 nm pulses
for Ep in (10e-9, 100e-9):
    print(f"905 nm {Ep*1e9:.0f} nJ whole pulse in 20 um: {Ep/A*1e3:.1f} mJ/cm^2; behind OD 2.5: {Ep/A/10**2.5*1e3:.2f} mJ/cm^2")
