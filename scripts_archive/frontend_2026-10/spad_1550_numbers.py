"""Numbers for "Why a SPAD is harder at 1,550 nm" (§C0 subsection 4.1) and the InGaAs/InP SPAD
array of Argo AI (§C4c subsection 3), Oct 2026.

Inputs: Ioffe NSM archive (band gaps, intrinsic carrier densities at 300 K); Itzler, ISSW 2024
(Argo 512 x 2 InGaAs/InP SPAD array, slides 10, 16, 17, 19, 22); Telesca et al., ISSW 2024, as
quoted in §C4c subsection 3; Sony SPAD dark counts as quoted there; Excelitas C30645/C30662
datasheet (Rev. 2024-04, p. 2); TI LMH32401 noise as quoted in §C0 subsection 5.5.
"""
from math import exp, log, pi, sqrt

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

# --- 7. Dark generation per area from linear APD datasheets: silicon against InGaAs, and against the Argo SPAD ---
# Quantity common to both modes: dark carriers entering the multiplication region per s per um^2.
# Excelitas's model (C30902EH datasheet Rev. 2022.02, Notes 2 and 3, p. 3): the dark current i_D = i_DS + i_DB*M
# has an unmultiplied surface part i_DS and a multiplied bulk part i_DB, and the dark noise is
# i_N = sqrt(2q (i_DS + i_DB*M^2*F)). Two datasheet numbers (i_D, i_N) then give both parts:
#   i_DB = (i_N^2/(2q) - i_D) / (M^2 F - M),   i_DS = i_D - i_DB*M.
# i_DB/q is the rate of dark carriers entering the multiplication region.
# SPAD: DCR / (P_t A), with P_t the avalanche trigger probability; PDE = absorption x P_t, so P_t >= PDE.
q = 1.602e-19


def mcintyre(k, m):
    return k * m + (1 - k) * (2 - 1 / m)


def split(i_d, i_n, m, f):
    i_db = (i_n**2 / (2 * q) - i_d) / (m**2 * f - m)
    return i_db, i_d - i_db * m


# Silicon: C30902EH (Table 2 p. 2: 0.5 mm useful diameter; Table 4 p. 3: 22 C, M = 150, i_D 7 nA typ,
# i_N 0.1 pA/rtHz typ; Note 3: k_eff = 0.02)
M_si = 150.0
F_si = mcintyre(0.02, M_si)
idb_si, ids_si = split(7e-9, 0.1e-12, M_si, F_si)
a_si = pi * 250.0**2
g_si = idb_si / q / a_si
print(f"7. Silicon C30902EH (22 C, M = 150, F = {F_si:.2f}): i_DB = {idb_si*1e12:.3f} pA, i_DS = {ids_si*1e9:.2f} nA "
      f"({ids_si/7e-9:.1%} of i_D unmultiplied); bulk {idb_si/q:.2e}/s over {a_si:.0f} um^2 = {g_si:.1f} /s/um^2")
n_s = (2 * q * ids_si) ** 0.5
n_b = (2 * q * idb_si * M_si**2 * F_si) ** 0.5
print(f"   noise parts: surface {n_s*1e12:.3f}, bulk {n_b*1e12:.3f} pA/rtHz (total {(n_s**2+n_b**2)**0.5*1e12:.3f})")
for i_n in (0.095e-12, 0.105e-12):
    print(f"   i_N {i_n*1e12:.3f} pA/rtHz -> {split(7e-9, i_n, M_si, F_si)[0]/q/a_si:.1f} /s/um^2")
print(f"   max values (10 nA, 0.25 pA/rtHz): {split(10e-9, 0.25e-12, M_si, F_si)[0]/q/a_si:.0f} /s/um^2")
print(f"   Fig. 8 bound: (7.1 - 6.3) nA over gain 12 -> 100: i_DB <= {(7.1-6.3)*1e-9/(100-12)*1e12:.1f} pA")

# InGaAs: C30645/C30662 (Rev. 2024-04, Tables 1 and 2 p. 2; 22 C, M = 10): i_D typ (A), i_N typ (A/rtHz), diameter (um)
M = 10.0
apds = {
    "C30645 (80 um)": (2.5e-9, 0.2e-12, 80.0),
    "C30645-7 (80 um, low noise)": (1.0e-9, 0.1e-12, 80.0),
    "C30662 (200 um)": (13e-9, 0.7e-12, 200.0),
    "C30662-7 (200 um, low noise)": (7.5e-9, 0.35e-12, 200.0),
}
lin = {}
for k in (0.40, 0.45, 0.50):
    F = mcintyre(k, M)
    vals = []
    for name, (i_d, i_n, dia) in apds.items():
        area = pi * (dia / 2) ** 2
        i_db, i_ds = split(i_d, i_n, M, F)
        capped = i_ds < 0  # noise spec above what the whole dark current could produce: take all of it as multiplied
        if capped:
            i_db = i_d / M
        g = i_db / q / area
        vals.append(g)
        if k == 0.45:
            print(f"   {name} (k 0.45, F {F:.2f}): i_DB {i_db*1e9:.3f} nA = {i_db*M/i_d:.0%} of i_D multiplied"
                  f"{' (capped: all multiplied)' if capped else ''}; {g:.2e} /s/um^2")
    lin[k] = vals
    print(f"   k = {k:.2f}: InGaAs bulk {min(vals):.2e}-{max(vals):.2e} /s/um^2; ratio to Si {min(vals)/g_si:.2e}-{max(vals)/g_si:.2e}")
L = lin[0.45]
print(f"   area scaling 200/80 um: typ {13/2.5:.1f}x, low-noise {7.5/1.0:.1f}x; area {6.25:.2f}x, perimeter {2.5:.1f}x")
F_mc = mcintyre(0.45, M)
print(f"   unmultiplied alternative for the C30645: sqrt(2 q I_d) = {(2*q*2.5e-9)**0.5*1e12:.3f} pA/rtHz (spec 0.2)")

a10 = pi * 5.0**2
spad_lo, spad_hi = 25e3 / a10, 35e3 / (0.2 * a10)  # counts per area (P_t = 1) to primary at P_t = PDE = 0.2
print(f"   Argo SPAD pixel (25 C, 10 um diameter): {25e3/a10:.0f}-{35e3/a10:.0f} counts/s/um^2; "
      f"primary {spad_lo:.0f}-{spad_hi:.0f} /s/um^2 (P_t between 1 and 0.2); ratio to Si {spad_lo/g_si:.0f}-{spad_hi/g_si:.0f}")
print(f"   ratio InGaAs linear/Argo: {min(L)/spad_hi:.0f} to {max(L)/spad_lo:.0f}")
req_hi, req_lo = 1e5 / a10, 1e5 / (0.2 * a10)  # 10 um pixel at <= 100 kHz, P_t = 1 and 0.2
print(f"   requirement, 10 um pixel at <= 100 kHz: primary <= {req_hi:.0f} (P_t 1) to {req_lo:.0f} (P_t 0.2) /s/um^2; "
      f"InGaAs linear APDs {min(L)/req_lo:.0f}-{max(L)/req_hi:.0f}x above; Si {req_hi/g_si:.0f}-{req_lo/g_si:.0f}x below")
for p in (min(L), max(L), g_si):
    n_prim = p * a10
    lo, hi = 0.2 * n_prim, n_prim
    print(f"   10 um SPAD with {p:.3g} /s/um^2: {n_prim:.3g} primary/s -> {lo:.3g}-{hi:.3g} counts/s; "
          f"P(count in 1 us) {1-exp(-lo*1e-6):.1%}-{1-exp(-hi*1e-6):.1%}")
i_prim = spad_hi * pi * 40.0**2 * q
print(f"   converse: Argo-grade generation ({spad_hi:.0f} /s/um^2) over an 80 um APD: i_DB = {i_prim*1e12:.2f} pA, "
      f"noise {(2*q*i_prim*M**2*F_mc)**0.5*1e12:.3f} pA/rtHz at M = 10")
print(f"   22 -> 25 C at E_a = 0.5 eV: x{exp(0.5/k_B*(1/295.15-1/298.15)):.2f}")
print(f"   Telesca SPAD at 300 K, 3-11 V excess bias: 2.5e3-6e4 counts/s/um^2 -> InGaAs linear APDs "
      f"{min(L)/6e4:.1f}-{max(L)/6e4:.1f}x the 11 V value")

# --- 8. Why op-amp TIAs are rare in lidar, and the APD as mixer (§C4b, §C1a, §C0 subsection 1.2) ---
c = 2.998e8
print("8. Overload: OPA855 3 Vpp total swing (SBOS622D p. 1) at R_F = 10 kOhm")
lin_max = 3.0 / 10e3
print(f"   linear up to {lin_max*1e3:.1f} mA even with the whole swing in one direction; "
      f"100 mA is {0.1/lin_max:.0f}x that; i R_F = {0.1*10e3:.0f} V")
for t, what in ((2e-9, "MAX40660 from 100 mA"), (3e-9, "OPA855, 2x overdrive"), (4e-9, "LMH32401 pulse extension, 10 mA"),
                (12e-9, "LTC6561 from 1 mA"), (20e-9, "SiPM window-reflection patent")):
    print(f"   recovery {t*1e9:.0f} ns ({what}): range blanked c t/2 = {c*t/2:.2f} m")
print(f"   sunlight DC: 10 uA x 10 kOhm = {10e-6*10e3:.2f} V of swing")
print(f"   R_F thermal noise sqrt(4kT/R): 10 kOhm {sqrt(4*1.380649e-23*300/10e3)*1e12:.2f}, "
      f"1 MOhm {sqrt(4*1.380649e-23*300/1e6)*1e12:.2f} pA/rtHz")
print("   APD as mixer: time stretch f_m/f_IF")
f_m, f_if = 200e6, 10e3
tau = 2 * 1e-3 / c
phi = 2 * pi * f_m * tau
print(f"   1 mm of range: delay {tau*1e12:.2f} ps; phase at {f_m/1e6:.0f} MHz {phi:.2e} rad = {phi*180/pi:.3f} deg; "
      f"IF shift at {f_if/1e3:.0f} kHz {phi/(2*pi*f_if)*1e6:.3f} us; stretch {f_m/f_if:.0e}")
print(f"   OPT3101: c/(2 x 10 MHz) = {c/(2*10e6):.1f} m unambiguous range")
