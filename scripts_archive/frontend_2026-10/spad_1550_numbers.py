"""Numbers for "Why a SPAD is harder at 1,550 nm" (§C0 subsection 4.1) and the InGaAs/InP SPAD
array of Argo AI (§C4c subsection 3), Oct 2026.

Inputs: Ioffe NSM archive (band gaps, intrinsic carrier densities at 300 K); Itzler, ISSW 2024
(Argo 512 x 2 InGaAs/InP SPAD array, slides 10, 16, 17, 19, 22); Telesca et al., ISSW 2024, as
quoted in §C4c subsection 3; Sony SPAD dark counts as quoted there; Excelitas C30645/C30662
datasheet (Rev. 2024-04, p. 2); TI LMH32401 noise as quoted in §C0 subsection 5.5.
"""
from math import exp, log, pi

k_B = 8.617e-5  # Boltzmann constant, eV/K

# --- 1. Photon energy against band gaps ---
E_ph = 1239.84 / 1550  # eV
print(f"1. photon energy at 1,550 nm: {E_ph:.3f} eV; Si gap 1.12 eV, In0.53Ga0.47As 0.74 eV, Ge 0.661 eV")

# --- 2. Intrinsic carrier density at 300 K (Ioffe) ---
n_i = {"Si": 1.0e10, "InGaAs": 6.3e11, "Ge": 2.0e13}  # cm^-3
for m in ("InGaAs", "Ge"):
    r = n_i[m] / n_i["Si"]
    print(f"2. n_i({m})/n_i(Si) = {r:.0f}; squared (diffusion) = {r*r:.2g}")

# --- 3. Dark counts per area ---
a_10um = pi * 5.0**2  # um^2, 10 um active diameter (Argo: "<10 um", so per-area values are lower bounds)
for T, lo, hi in ((25, 25e3, 35e3), (40, 60e3, 75e3)):
    print(f"3. Argo array at {T} C: {lo/a_10um:.0f}-{hi/a_10um:.0f} counts/s/um^2 (at least), PDE ~20%")
si_60C = 2007 / 100.0  # Sony 10 um square pixel at 60 C
print(f"   Sony Si SPAD at 60 C: {si_60C:.0f} counts/s/um^2; ratio {25e3/a_10um/si_60C:.0f}-{35e3/a_10um/si_60C:.0f}")
print(f"   per pixel: 25 kHz / 2,007 Hz = {25e3/2007:.1f}")

# --- 4. Activation energy and temperature scaling ---
def e_act(r, t1, t2):  # ratio r = DCR(t2)/DCR(t1), t2 > t1, kelvin
    return k_B * log(r) / (1 / t1 - 1 / t2)

ea_argo = e_act(64e3 / 25e3, 298.15, 313.15)  # medians marked on slides 17 and 19
ea_tel = e_act(2e5 / 3.5e4, 275.0, 300.0)       # Telesca Fig. 5 at 3 V, as quoted in §C4c
print(f"4. E_a: Argo medians 25 -> 64 kHz (25 -> 40 C): {ea_argo:.3f} eV; Telesca 275 -> 300 K: {ea_tel:.3f} eV")
ea = 0.5
f10 = exp(ea / k_B * (1 / 298.15 - 1 / 308.15))
f85 = exp(ea / k_B * (1 / 298.15 - 1 / 358.15))
print(f"   at E_a = 0.5 eV: x{f10:.2f} per 10 K near 25 C; 85 C vs 25 C: x{f85:.0f}")
d85 = 25e3 * f85
print(f"   a 25 kHz pixel at 85 C: {d85/1e3:.0f} kHz; P(dark count in 1 us) = {1-exp(-d85*1e-6):.0%}")
print(f"   at 100 kHz: P(dark count in 1 us) = {1-exp(-1e5*1e-6):.1%}")

# --- 5. Linear InGaAs APD noise against a TIA ---
tia = 49e-9 / (250e6) ** 0.5
print(f"5. LMH32401: 49 nA rms over 250 MHz = {tia*1e12:.1f} pA/rtHz average; "
      f"Excelitas C30645/C30662 at M=10, 22 C: 0.2/0.7 pA/rtHz -> {tia*1e12/0.2:.0f}x/{tia*1e12/0.7:.1f}x below")

# --- 6. Argo pixel field of view and sampling ---
pix_v = 2e-3 / 6          # 6 pixels span 2 mrad (slide 10)
pix_h = (0.14 / 200) / 2  # two columns span ~14 cm at 200 m (slide 10)
omega_argo = pix_v * pix_h
omega_model = (0.05 * pi / 180) ** 2  # §C4c model macro-pixel, 0.05 x 0.05 deg
print(f"6. Argo pixel {pix_v*1e3:.2f} x {pix_h*1e3:.2f} mrad = {omega_argo:.2e} sr; model {omega_model:.2e} sr; "
      f"ratio {omega_model/omega_argo:.1f}")
need = 3.4e8 / 1e5
print(f"   §C4c 1,550 nm model pixel 3.4e8 counts/s against ~1e5: x{need:.0f} to find; pixel x{omega_model/omega_argo:.1f}, "
      f"PDE 0.30/0.20 = x1.5 -> x{omega_model/omega_argo*1.5:.0f}; remaining x{need/(omega_model/omega_argo*1.5):.0f}")
print(f"   samples per point: 12 pixels x 13 pulses = {12*13}; pulse period at 400 kHz = {1/400e3*1e6:.1f} us")
