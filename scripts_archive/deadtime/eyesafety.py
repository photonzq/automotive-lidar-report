"""Eye-safety headroom at 1,550 nm vs the model's needs, and gated-transmitter channel power (section C7b 2(i))."""
import math
import numpy as np

P_AEL_1550 = 9.1          # W, Class 1 time-averaged, 120 x 25 deg raster at 10 Hz, evaluated at 100 mm (section C4c)
P_SMALL_940 = 1.18e-3 * 9140 / 38.5   # W, small-source average-power limit over the same raster at 940 nm
print(f"940 nm small-source raster average limit: {P_SMALL_940:.3f} W; 905 nm: {1.00e-3*9140/38.5:.3f} W")

E_fmcw = {200: 0.303e-6, 300: 0.455e-6}
for R, E in E_fmcw.items():
    for nd in (10e6, 25e6):
        print(f"FMCW {R} m, {nd/1e6:.0f} Mpts/s: P_opt {nd*E:.2f} W = {nd*E/P_AEL_1550*100:.0f}% of 9.1 W")
for nd in (10e6, 25e6):
    Emax = P_AEL_1550 / nd
    print(f"allowed E per point at {nd/1e6:.0f} Mpts/s: {Emax*1e6:.2f} uJ -> R ~ {200*Emax/0.303e-6:.0f} m (E ~ R, best aperture)")

E_tof200 = 93.3e-9
for R in (200, 300, 500, 600):
    E = E_tof200 * (R / 200) ** 2
    print(f"ToF {R} m: E_opt {E*1e9:.0f} nJ per point, {E*1e8:.0f} nJ per shot (10 shots); P_opt at 10 Mpts/s {E*1e7:.2f} W, at 25 {E*2.5e7:.2f} W")

# gated transmitter: dead-time light removed; (h) at 10 Mpts/s, 300 m, N_L = 4
NDOT, R_DR, TAU, ETA, P_AN, E_S, F_D, P0, NL, EP = 1e7, 2000, 2e-6, 0.15, 0.010, 37e-12, 90e6, 3.0, 4, 0.45e-6


def total(Pch, gated):
    Tu = EP / (2 * Pch)
    nch = NDOT * (EP / Pch + 2 * TAU)
    nsamp = 5 * R_DR + 5 * F_D * Tu
    dead = 0 if gated else 2 * TAU * NDOT * Pch / ETA
    return NDOT * EP / ETA + dead + nch * NL * P_AN + NDOT * NL * nsamp * E_S + P0, nch, 2.5 * (1e9 * TAU / Tu + F_D)


for P in (0.0352, 0.1, 0.3, 1.0):
    tg, nch, fs = total(P, True)
    tu, _, _ = total(P, False)
    print(f"P_ch {P*1e3:6.1f} mW: channels {nch:5.0f} ({4*nch:5.0f} receivers), f_s {fs/1e9:.2f} GS/s, total gated {tg:5.1f} W, ungated {tu:5.1f} W")
floor = NDOT * EP / ETA + 2 * TAU * NDOT * NL * P_AN + NDOT * NL * 5 * R_DR * E_S + P0
print(f"gated floor (P_ch -> inf): {floor:.1f} W")
# ToF at 300 m, 10 Mpts/s (paralyzable model central)
e_opt = E_tof200 * 2.25
tof300 = 3 + NDOT * (e_opt / 0.20 + 69.9e-9)
print(f"ToF 300 m, 10 Mpts/s: {tof300:.1f} W; FMCW optimum 68.2 W / ToF = {68.2/tof300:.1f}; gated floor / ToF = {floor/tof300:.1f}")
