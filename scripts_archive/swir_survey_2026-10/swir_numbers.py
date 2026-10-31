"""Numbers for the SWIR image-sensor supplement (detectivity check of Li et al., Nature 2026,
measurement-chain estimates, and dark leakage of SWIR absorbers versus temperature).
All inputs are typed in below with their sources; nothing is read from disk. Usage: swir_numbers.py"""
import cmath
import math

kB = 1.380649e-23   # J/K
q = 1.602176634e-19  # C
HC_UM = 1.23984198   # h*c/q in um*V
T = 298.0            # K, temperature stated for the benchmark measurement (Peer Review File p. 118)
FOURKT = 4 * kB * T
VT = kB * T / q


def resp(eqe, lam_um):
    """Responsivity in A/W from external quantum efficiency and wavelength in um."""
    return eqe * lam_um / HC_UM


def johnson(r_ohm):
    """One-sided Johnson-noise current density in A/Hz^0.5."""
    return math.sqrt(FOURKT / r_ohm)


print(f"T = {T} K, 4kT = {FOURKT:.4e} J, kT/q = {VT * 1e3:.3f} mV")

# A. PbS diode of Li et al. (1 mm^2)
A_PBS = 0.01                       # cm^2 (Supp. Fig. 19a legend)
R_PBS = resp(0.484, 2.5)           # EQE 48.4 % at 2,500 nm (SI p. 34; Source Data Fig. 3e)
I_N_REP = 2.19e-13                 # A/Hz^0.5 at 1 kHz, zero bias (SI p. 34)
J_M01 = 123.0e-6                   # A/cm^2 at -0.1 V (Peer Review File p. 28)
print("\nA. PbS")
print(f"  R(2.5 um) = {R_PBS:.4f} A/W; reported D* = {R_PBS * math.sqrt(A_PBS) / I_N_REP:.3e} Jones")
r0a_chord = 0.1 / J_M01
r0_chord = r0a_chord / A_PBS
fl_chord = johnson(r0_chord)
print(f"  chord R0A = {r0a_chord:.1f} ohm cm^2, R0 = {r0_chord / 1e3:.2f} kohm, floor = {fl_chord:.3e}, "
      f"floor/reported = {fl_chord / I_N_REP:.3f}, D*max = {R_PBS * math.sqrt(A_PBS) / fl_chord:.3e}")
print(f"  headline check: R*sqrt(R0A/4kT) = {R_PBS * math.sqrt(r0a_chord / FOURKT):.3e}")
n = 1.2
RSH_A = 1240.0                     # ohm cm^2, Supp. Table 10
for j0 in (3.0e-5, 3.5e-5, 4.0e-5, 3.6e-4):
    r0a = 1.0 / (q * j0 / (n * kB * T) + 1.0 / RSH_A)
    fl = johnson(r0a / A_PBS)
    print(f"  fit J0 = {j0:.1e} A/cm^2, n = 1.2, RshA = 1240: R0A = {r0a:.1f}, R0 = {r0a / A_PBS / 1e3:.1f} kohm, "
          f"floor = {fl:.3e}, ratio = {fl / I_N_REP:.2f}, D* = {R_PBS * math.sqrt(A_PBS) / fl:.3e}")
j_pred = 3.6e-4 * (1 - math.exp(-0.1 / (n * VT))) + 0.1 / RSH_A
print(f"  Table 10 values predict J(-0.1 V) = {j_pred * 1e6:.0f} uA/cm^2 against 123.0 measured "
      f"(x{j_pred / J_M01:.2f})")
print(f"  Table 10 shunt alone at -0.8 V: {0.8 / RSH_A * 1e3:.3f} mA/cm^2 against ~0.29 measured "
      f"(x{0.8 / RSH_A / 2.9e-4:.1f})")
# route used in the text: the diode component drawn in Supp. Fig. 20b (plateau 3-4e4 nA/cm^2, n = 1.2),
# the rest of the measured -0.1 V current bounded by its chord (sublinear branch)
for j0 in (3.0e-5, 4.0e-5):
    r0a_d = n * VT / j0
    j_d = j0 * (1 - math.exp(-0.1 / (n * VT)))
    r_rest = 0.1 / (J_M01 - j_d)
    r0a = 1.0 / (1.0 / r0a_d + 1.0 / r_rest)
    fl = johnson(r0a / A_PBS)
    print(f"  diode part J0 = {j0:.0e}: R0A_d = {r0a_d:.0f}, rest chord = {r_rest:.0f}, R0A <= {r0a:.0f} ohm cm^2, "
          f"floor >= {fl:.3e} (x{fl / I_N_REP:.2f}), D* <= {R_PBS * math.sqrt(A_PBS) / fl:.3e}")
j0_all = J_M01 / (1 - math.exp(-0.1 / (n * VT)))
r0a_all = n * VT / j0_all
print(f"  all of J(-0.1 V) as n = 1.2 diode current: R0A = {r0a_all:.0f}, floor = {johnson(r0a_all / A_PBS):.3e} "
      f"(x{johnson(r0a_all / A_PBS) / I_N_REP:.2f})")
line = 1.0e-14
print(f"  Supp. Fig. 19a 'thermal noise' line {line:.1e} A/Hz^0.5 -> R = {FOURKT / line**2:.3e} ohm, "
      f"R*A = {FOURKT / line**2 * A_PBS:.3e} ohm cm^2, x{FOURKT / line**2 * A_PBS / r0a_chord:.0f} the chord R0A")
print(f"  what dark current gives sqrt(2qI) = reported: I = {I_N_REP**2 / (2 * q) * 1e9:.0f} nA")
for i_amp in (60e-15, 100e-15):
    dev_only = math.sqrt(I_N_REP**2 - i_amp**2)
    print(f"  reported total minus SR570 noise {i_amp * 1e15:.0f} fA: {dev_only:.3e} -> floor/device = {fl_chord / dev_only:.2f}")
print(f"  R0A needed for the reported noise to equal the floor: {FOURKT / I_N_REP**2 * A_PBS:.0f} ohm cm^2 "
      f"(x{FOURKT / I_N_REP**2 * A_PBS / r0a_chord:.2f} the chord)")
# Source Data Fig. 3b first curve (not the published panel): slope at 0 V
g = (1.79520e-6 + 2.13393e-6) / 0.02
g2 = (3.40307e-6 + 4.50404e-6) / 0.04
print(f"  Source Data Fig. 3b curve 1: dJ/dV = {g:.4e} (+-10 mV), {g2:.4e} (+-20 mV) -> R0A = {1 / g:.0f}, {1 / g2:.0f} ohm cm^2;"
      f" floor = {johnson(1 / g / A_PBS):.3e}; D*max = {R_PBS * math.sqrt(A_PBS) / johnson(1 / g / A_PBS):.3e}")

# B. residual bias: ideal-diode shot noise plus shunt Johnson noise, fit split
print("\nB. noise floor versus a residual bias (ideal-diode shot noise + shunt Johnson noise)")
for j0 in (3.5e-5,):
    i0 = j0 * A_PBS
    gsh = A_PBS / RSH_A
    for v in (0.0, 1e-3, -1e-3, -1e-2, -0.1):
        s = 2 * q * i0 * (math.exp(q * v / (kB * T)) + 1) + FOURKT * gsh
        print(f"  J0 {j0:.1e}, V = {v * 1e3:+.0f} mV: floor = {math.sqrt(s):.3e} A/Hz^0.5")
    print(f"  all-shunt bound (any bias): {fl_chord:.3e}")
    for v_os in (0.25e-3, 1e-3, 2e-3):
        print(f"  offset {v_os * 1e3:.2f} mV drives {v_os / r0_chord * 1e9:.1f}-{v_os / (r0a_chord * 0.58 / A_PBS) * 1e9:.1f} nA "
              f"(R0 {r0_chord / 1e3:.0f} to {0.58 * r0_chord / 1e3:.0f} kohm)")

# C. Extended InGaAs reference, Hamamatsu G12183-003K
print("\nC. G12183-003K")
A_ING = math.pi * 0.015**2
print(f"  area = {A_ING:.4e} cm^2 ({A_ING * 100:.4f} mm^2), sqrt = {math.sqrt(A_ING):.5f} cm")
for rsh in (2e4, 1e5):
    print(f"  Rsh {rsh / 1e3:.0f} kohm: R0A = {rsh * A_ING:.1f} ohm cm^2, floor = {johnson(rsh):.3e}, "
          f"D*_th(1.3 A/W) = {1.3 * math.sqrt(A_ING) / johnson(rsh):.3e}, J0 = kT/(qR0A) = {VT / (rsh * A_ING) * 1e6:.0f} uA/cm^2")
r_ing = resp(0.593, 2.5)
print(f"  authors' EQE 59.3 % at 2.5 um -> R = {r_ing:.4f} A/W")
print(f"  round 1: D* (A = 0.09 mm^2) = {r_ing * math.sqrt(9e-4) / 2.09e-13:.4e}; with true area = "
      f"{r_ing * math.sqrt(A_ING) / 2.09e-13:.4e}; Rsh equivalent of 2.09e-13: {FOURKT / 2.09e-13**2 / 1e3:.0f} kohm")
i_meas = 153.7e-6 * 9e-4
i0 = i_meas / (1 - math.exp(-0.1 / VT))
print(f"  current at -0.1 V = {i_meas * 1e9:.1f} nA (J x stated area); chord R = {0.1 / i_meas / 1e3:.0f} kohm, floor >= "
      f"{johnson(0.1 / i_meas):.3e}; diffusion-limited R0 = {VT / i0 / 1e3:.0f} kohm, floor = {johnson(VT / i0):.3e}, "
      f"R0A = {VT / i0 * A_ING:.0f} ohm cm^2")
for r0a in (70.7, VT / i0 * A_ING):
    print(f"  D*_th at 2.5 um (R = {r_ing:.3f}) with R0A = {r0a:.1f}: {r_ing * math.sqrt(r0a / FOURKT):.3e}")
print(f"  round 2: D* 9.52e10 with true area and same R implies i_n = {r_ing * math.sqrt(A_ING) / 9.52e10:.3e}")
print(f"  round1/round2 = {r_ing * math.sqrt(9e-4) / 2.09e-13 / 9.52e10:.3f}; area part = {math.sqrt(9e-4 / A_ING):.4f}")

# D. measurement chain (SR570 at 1e-8 A/V; AD743 in High BW, AD546 in Low Noise)
print("\nD. SR570 chain at 1 kHz")
f = 1e3
w = 2 * math.pi * f
C_PBS = 3.0e-9                     # F at 0 V, Supp. Fig. 18b
ZIN = 1e4                          # ohm, DC input impedance at 1e-7 and 1e-8 A/V (SR570 Table 1)
I_AMP = {"HighBW": 100e-15, "LowNoise": 60e-15}
EN = {"HighBW": 3.2e-9, "LowNoise": 35e-9}   # AD743 / AD546 at 1 kHz
F3 = {"HighBW": 2e3, "LowNoise": 200.0}
cases = [("PbS chord", r0_chord, C_PBS), ("PbS fit", 1.0 / (q * 3.5e-5 / (n * kB * T) + 1 / RSH_A) / A_PBS, C_PBS),
         ("InGaAs typ", 1e5, 50e-12), ("InGaAs diff", VT / i0, 50e-12)]
print(f"  PbS R0C corner (chord): {1 / (2 * math.pi * r0_chord * C_PBS):.0f} Hz")
for name, r0, c in cases:
    ys = 1 / r0 + 1j * w * c
    div = abs(1 / (1 + ZIN * ys))
    dev = johnson(r0)
    for mode in ("HighBW", "LowNoise"):
        h = 1 / math.sqrt(1 + (f / F3[mode]) ** 2)
        en_term = EN[mode] * abs(ys)
        tot = h * math.sqrt((dev * div) ** 2 + (en_term * div) ** 2 + I_AMP[mode] ** 2)
        print(f"  {name:12s} R0 = {r0 / 1e3:6.1f} k, |Ys| = {abs(ys):.3e} S, divider = {div:.3f}, dev = {dev:.3e}, "
              f"{mode:8s}: |H| = {h:.3f}, e_n|Ys| = {en_term:.3e}, expected reading = {tot:.3e}")

print("  network model (input resistors R132-R135 are physical, per the manual's front-end description):")
print("  i_read = |H| sqrt(4kT Re[1/(Rin+Zs)] + e_n^2/|Rin+Zs|^2 + i_amp^2), Zs = R0/(1+j w R0 C)")
for name, r0, c in cases:
    zs = r0 / (1 + 1j * w * r0 * c)
    zt = ZIN + zs
    eq_noise = math.sqrt(FOURKT * (1 / zt).real)
    for mode in ("HighBW", "LowNoise"):
        h = 1 / math.sqrt(1 + (f / F3[mode]) ** 2)
        en_t = EN[mode] / abs(zt)
        tot = h * math.sqrt(eq_noise**2 + en_t**2 + I_AMP[mode] ** 2)
        print(f"  {name:12s} Zs = {zs.real / 1e3:.1f}{zs.imag / 1e3:+.1f}j k, |Rin+Zs| = {abs(zt) / 1e3:.1f} k, "
              f"Re[1/(Rin+Zs)] = {(1 / zt).real:.4e} S, equilibrium noise = {eq_noise:.3e} (diode alone {johnson(r0):.3e}), "
              f"{mode:8s}: e_n/|Rin+Zs| = {en_t:.3e}, expected reading = {tot:.3e}")
e_r = math.sqrt(FOURKT * ZIN)
print(f"  Johnson noise of a physical 10 kohm input resistor: {e_r:.3e} V/Hz^0.5")
for name, r0, c in cases[:2]:
    ys = 1 / r0 + 1j * w * c
    print(f"  {name}: |Zs| at 1 kHz = {1 / abs(ys) / 1e3:.1f} kohm ({1e8 * abs(ys):.0f}x below the 100 Mohm the manual asks for);"
          f" resistor-noise current = {e_r * abs(ys) / abs(1 + ZIN * ys):.3e}")

# E. dark leakage of SWIR absorbers versus temperature
print("\nE. leakage versus temperature")
A3 = math.pi * 0.015**2
r25 = 1e9
r_m40, r_100 = 5.5e11, 7.6e5      # G12180-003A, read from the datasheet plot (p. 5)
dec_per_k = math.log10(r_m40 / r_100) / 140
print(f"  G12180-003A: {dec_per_k:.4f} decades/K, halving every {math.log10(2) / dec_per_k:.2f} K")
for tc, r in ((25, r25), (85, r25 * 10 ** (-dec_per_k * 60)), (100, r_100), (105, r25 * 10 ** (-dec_per_k * 80))):
    tk = tc + 273.15
    r0a = r * A3
    j0 = (kB * tk / q) / r0a
    print(f"  {tc:4d} C: R0 = {r:.3e} ohm, R0A = {r0a:.3e} ohm cm^2, J0 = {j0:.3e} A/cm^2")
h183 = 35 / math.log2(10)
print(f"  G12183: 25 C -> -10 C x10 over 35 K: halving every {h183:.1f} K; -10 -> -20 C x2 over 10 K")
for tc in (85, 105):
    fac = 2 ** ((tc - 25) / h183)
    r0a = 1e5 * A3 / fac
    print(f"  G12183 at {tc} C (extrapolated): R0 = {1e5 / fac:.0f} ohm, J0 = {(kB * (tc + 273.15) / q) / r0a * 1e3:.1f} mA/cm^2")
print("  diffusion-limited halving interval of R0 (R0 ~ T^-2 exp(Eg/kT)):")
for eg in (0.75, 0.80):
    for tk in (300.0, 373.0):
        slope = 2 / tk + eg / (8.617333e-5 * tk**2)
        print(f"    Eg {eg} eV at {tk:.0f} K: {math.log(2) / slope:.1f} K")

# F. dark electrons per millisecond per pixel
print("\nF. dark electrons per ms")
for name, j, p_um in (("std InGaAs 25 C", 3.63e-8, 5), ("std InGaAs 25 C", 3.63e-8, 15), ("std InGaAs 100 C", 6.0e-5, 5),
                      ("std InGaAs 100 C", 6.0e-5, 15), ("Ge TES200 25 C", 204e-6, 7), ("PbS -0.1 V 25 C", 123e-6, 15)):
    a = (p_um * 1e-4) ** 2
    print(f"  {name:18s} {p_um:2d} um: {j * a / q * 1e-3:.3e} e-/ms")
print(f"  PbS 15 um pixel, 2 ms at -0.1 V: {123e-6 * (15e-4) ** 2 * 2e-3 / q:.3e} e-")
print(f"  TES200: 100 pA per (7 um)^2 = {1e-10 / (7e-4) ** 2 * 1e6:.0f} uA/cm^2")
print(f"  shot noise of 1.23 uA at -0.1 V: {math.sqrt(2 * q * 1.23e-6):.3e} A/Hz^0.5")
