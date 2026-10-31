"""Why microbolometers need a vacuum package, and how tight it must be (order-of-magnitude estimates).
Prints: leg conductance of a 12 um pixel from its time constant and heat capacity; gas conductance at 1 atm
(continuum, across the quarter-wave cavity) and in the free-molecular regime; the pressure at which gas adds 10% to
the leg conductance; the mean free path; and the leak-rate budget that keeps a sealed cavity below 1 Pa for 10 years.
Usage: bolometer_vacuum.py"""
import math

KB = 1.380649e-23
T = 300.0
d = 12e-6                    # pixel pitch, m (membrane area taken as d^2)
A = d * d
t_mem = 200e-9               # membrane thickness (SiN + thermistor), m, assumed
cv = 2.5e6                   # volumetric heat capacity, J m^-3 K^-1, assumed (SiN-like)
C = A * t_mem * cv
for tau in (7e-3, 12e-3):
    print(f"C = {C:.2e} J/K; tau = {tau * 1e3:.0f} ms -> G_leg = C/tau = {C / tau * 1e9:.1f} nW/K")
G_legs = (C / 7e-3, C / 12e-3)   # the stiffer and the softer legs

gap = 2.5e-6                 # quarter-wave cavity for ~10 um
k_air = 0.026                # W m^-1 K^-1
G_cont = k_air * A / gap
for G_leg in G_legs:
    print(f"1 atm, continuum, bottom face only: G_gas = {G_cont * 1e6:.2f} uW/K = {G_cont / G_leg:.0f} x G_leg "
          f"({G_leg * 1e9:.1f} nW/K)")

m = 29 * 1.66054e-27
flux_per_pa = 1 / math.sqrt(2 * math.pi * m * KB * T)       # molecules m^-2 s^-1 Pa^-1
gamma = 1.4
h_per_pa = (gamma + 1) / (2 * (gamma - 1)) * KB * flux_per_pa  # W m^-2 K^-1 Pa^-1, full accommodation
G_fm_per_pa = 2 * h_per_pa * A                                 # both faces
for G_leg in G_legs:
    p10 = 0.1 * G_leg / G_fm_per_pa
    print(f"free-molecular: h = {h_per_pa:.2f} W m^-2 K^-1 per Pa; G_gas = {G_fm_per_pa * 1e9:.3f} nW/K per Pa; "
          f"10% of G_leg ({G_leg * 1e9:.1f} nW/K) at p = {p10:.1f} Pa = {p10 / 100:.3f} mbar = {p10 / 0.1333:.0f} mTorr")
lam_1pa = KB * T / (math.sqrt(2) * math.pi * (3.7e-10) ** 2 * 1.0)
print(f"mean free path at 1 Pa: {lam_1pa * 1e3:.1f} mm (>> {gap * 1e6:.1f} um gap); mean free path equals the gap at about "
      f"{KB * T / (math.sqrt(2) * math.pi * (3.7e-10) ** 2 * gap):.0f} Pa (free-molecular below)")

yr10 = 10 * 3.156e7
for name, vol in (("wafer-level cap over a VGA 12 um array, 0.2 mm deep", 7.68e-3 * 6.14e-3 * 0.2e-3),
                  ("die-level ceramic package, about 1 cm^3", 1e-6),
                  ("pixel-level cavity, 12 x 12 x 2.5 um", 12e-6 * 12e-6 * 2.5e-6)):
    q = 1.0 * vol / yr10   # Pa m^3/s for a 1 Pa rise in 10 years
    print(f"{name}: V = {vol:.2e} m^3; leak budget for +1 Pa in 10 yr = {q:.1e} Pa m^3/s = {q * 10:.1e} mbar L/s")
