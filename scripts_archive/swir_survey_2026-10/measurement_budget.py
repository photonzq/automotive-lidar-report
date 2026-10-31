"""Numbers for §S2.8 of the SWIR side note: what a dedicated measurement of the PbS diode of Li et al. would see.
Prints the thermal floor and RC corner of the 1 mm^2 diode for both bounds on R0, the noise added by a JFET-input TIA
(feedback resistor, op-amp voltage noise on the diode's admittance), the output levels that let one gain range carry both
noise and signal, the open-circuit voltage noise, the same budget for a 0.1 mm^2 diode, and the dark charge, shot noise,
well filling and shot-limited detectivity of a 15 um pixel at the imager's -0.1 V and 2 ms.
All inputs are typed in with their sources (side note §S2.3-§S2.5, §S3.3; AD743 datasheet p. 2). Usage: measurement_budget.py"""
import math

Q = 1.602176634e-19
KB = 1.380649e-23
T = 298.0
FOURKT = 4 * KB * T                  # 1.646e-20 J
R_RESP = 0.976                       # A/W at 2.5 um (EQE 48.4%, §S2.2)
J_m01 = 1.230e-4                     # A/cm^2 at -0.1 V, 1 mm^2 diode (§S2.3)
C_1MM2 = 3e-9                        # F at 0 V (Supp. Fig. 18b, §S2.4)
EN_AD743 = 3.2e-9                    # V/sqrt(Hz) at 1 kHz (AD743 datasheet p. 2)
F = 1e3                              # Hz, the frequency of the reported noise


def admittance(r0, c, f):
    return math.hypot(1 / r0, 2 * math.pi * f * c)


print("1 mm^2 diode")
for r0 in (81.3e3, 51.5e3):          # chord bound and bound with the authors' diode component (§S2.3)
    i_th = math.sqrt(FOURKT / r0)
    fc = 1 / (2 * math.pi * r0 * C_1MM2)
    y = admittance(r0, C_1MM2, F)
    i_en = EN_AD743 * y
    print(f"  R0 = {r0 / 1e3:.1f} kOhm: floor {i_th:.3g} A/rtHz, corner {fc:.0f} Hz, |Y(1 kHz)| = {y:.3g} S, "
          f"e_n|Y| = {i_en:.2g} A/rtHz ({(i_en / i_th) ** 2 * 100:.1f}% of the floor in power), "
          f"open-circuit voltage noise below the corner {math.sqrt(FOURKT * r0) * 1e9:.1f} nV/rtHz")
i_th = math.sqrt(FOURKT / 81.3e3)
for rf in (1e6, 10e6, 100e6):
    i_rf = math.sqrt(FOURKT / rf)
    print(f"  Rf = {rf / 1e6:.0f} MOhm: Johnson noise {i_rf:.3g} A/rtHz ({(i_rf / i_th) ** 2 * 100:.1f}% of the 81.3 kOhm floor in power); "
          f"-0.1 V dark current {J_m01 * 0.01 * 1e6:.2f} uA gives {J_m01 * 0.01 * rf:.2f} V at the output")
rf, cf = 1e6, 10e-12
y = admittance(81.3e3, C_1MM2, F)
total = math.sqrt(i_th ** 2 + FOURKT / rf + (EN_AD743 * y) ** 2)
print(f"  1 MOhm TIA with the AD743 at 1 kHz: total {total:.3g} A/rtHz, diode share {i_th ** 2 / total ** 2 * 100:.1f}% of the power; "
      f"output noise {total * rf * 1e6:.2f} uV/rtHz; bandwidth with {cf * 1e12:.0f} pF: {1 / (2 * math.pi * rf * cf) / 1e3:.0f} kHz")
nep = i_th / R_RESP
print(f"  NEP at the thermal floor: {nep:.2g} W/rtHz at 2.5 um; signal for SNR = 100 in 1 Hz: {100 * nep * 1e12:.0f} pW rms, "
      f"photocurrent {100 * i_th * 1e12:.0f} pA, {100 * i_th * rf * 1e6:.0f} uV at 1 MOhm")
print(f"  10 V swing at 1 MOhm holds {10 / rf * 1e6:.0f} uA = {10 / rf / R_RESP * 1e6:.0f} uW at 2.5 um; "
      f"range from the NEP: {math.log10(10 / rf / R_RESP / nep):.1f} decades")

print("0.1 mm^2 diode (same R0*A, C and leakage per area)")
r0s, cs = 813e3, 0.3e-9
i_ths = math.sqrt(FOURKT / r0s)
ys = admittance(r0s, cs, F)
for rf in (10e6, 100e6):
    print(f"  Rf = {rf / 1e6:.0f} MOhm: {(FOURKT / rf) / i_ths ** 2 * 100:.1f}% of the floor in power; "
          f"-0.1 V current {J_m01 * 0.001 * 1e9:.0f} nA gives {J_m01 * 0.001 * rf:.2f} V")
print(f"  floor {i_ths:.3g} A/rtHz ({i_th / i_ths:.2f} times below the 1 mm^2 diode), corner {1 / (2 * math.pi * r0s * cs):.0f} Hz, "
      f"e_n|Y| = {EN_AD743 * ys:.2g} A/rtHz ({(EN_AD743 * ys / i_ths) ** 2 * 100:.2f}% in power)")

print("15 um pixel at -0.1 V, 2 ms (test-diode leakage)")
a_pix = (15e-4) ** 2                 # cm^2
n_dark = J_m01 * a_pix * 2e-3 / Q
print(f"  dark charge {n_dark:.3g} e-, full shot noise {math.sqrt(n_dark):.0f} e-; 1% leakage spread = {0.01 * n_dark:.3g} e- "
      f"= {0.01 * n_dark / math.sqrt(n_dark):.0f} x the shot noise")
print(f"  time to fill a 550 ke- well: {550e3 / (J_m01 * a_pix / Q) * 1e3:.2f} ms; dark charge / 550 ke- = {n_dark / 550e3:.1f}")
d_shot = R_RESP / math.sqrt(2 * Q * J_m01)
d_model = R_RESP * math.sqrt(0.01) / 4.97e-13      # §S2.4: 4.97e-13 A/rtHz at -0.1 V for 1 mm^2
print(f"  white-noise D* at -0.1 V: {d_shot:.3g} Jones (full shot noise of the dark current) to {d_model:.3g} Jones (§S2.4 model)")

print("Well depth of a 15 um pixel")
print(f"  dark-current ratio, bulk PbS at -0.1 V / PbS dots (5 nA/cm^2, §S1.3): {J_m01 / 5e-9:.3g}")
ll_well, ll_pitch = 25e6, 30.0                       # Schultz et al., Lincoln Lab. J. 20(2), 2014, p. 38: <25 Me- at 30 um
print(f"  Lincoln Laboratory's 25 Me- at 30 um scaled by area to 15 um: {ll_well * (15 / ll_pitch) ** 2:.3g} e-; "
      f"checks: 5 V x 0.8 pF = {5 * 0.8e-12 / Q:.3g} e-, 2.2 V x 1.85 pF = {2.2 * 1.85e-12 / Q:.3g} e-")
imec_well, imec_c, imec_pitch = 782e3, 108e-15, 5.0  # Chu et al., Sensors 2025, Table 1 and p. 6 (low-gain node)
swing = imec_well * Q / imec_c
c15 = imec_c * (15 / imec_pitch) ** 2
print(f"  imec 5 um pixel: swing {swing:.2f} V; same capacitance per area over a 15 um pixel: {c15 * 1e12:.2f} pF, "
      f"well {c15 * swing / Q:.3g} e-")
for c in (88e-15 / 1.6, 1e-12):                      # 550 ke- at ~1.6 V (~55 fF), and 1 pF
    print(f"  C = {c * 1e15:.0f} fF: reset (kTC) noise {math.sqrt(KB * T * c) / Q:.0f} e-; chain noise that equals the "
          f"1,860 e- dark shot noise: {math.sqrt(n_dark) * Q / c * 1e6:.0f} uV rms")
# bias sensitivity of the dark current at -0.1 V: ohmic part scales with V, saturated diode part barely
j0, ut, n_id = 3.5e-5, KB * T / Q, 1.2
j_diode = j0 * (1 - math.exp(-0.1 / (n_id * ut)))
j_ohm = J_m01 - j_diode
d_ohm = 1 / 0.1                                      # (dI/I)/dV for an ohmic branch at 0.1 V, per volt
d_diode = math.exp(-0.1 / (n_id * ut)) / (1 - math.exp(-0.1 / (n_id * ut))) / (n_id * ut)
mix = (j_ohm * d_ohm + j_diode * d_diode) / J_m01
print(f"  dark-current change per mV of held bias at -0.1 V: ohmic {d_ohm * 1e-3 * 100:.1f}%, saturated diode "
      f"{d_diode * 1e-3 * 100:.2f}%, with the authors' diode component ({j_diode * 1e6:.0f} uA/cm^2) {mix * 1e-3 * 100:.2f}%")
print("Op-amp classes for the 1 mm^2 diode in a 1 MOhm TIA (R0 = 81.3 kOhm, Cs = 3 nF, Cf = 10 pF)")
# datasheet values: AD743 Rev. E p. 2 (e_n at 10 Hz/100 Hz/1 kHz/10 kHz, i_n at 1 kHz, C_in ~20 pF);
# OPA928 SBOSA77A p. 4 (e_n at 100 Hz and 1 kHz) with ~6 pF input; LMC662 SNOSC51D p. 6 (e_n, i_n at 1 kHz)
amps = {
    "AD743 (JFET)": ({10: 5.5e-9, 100: 3.6e-9, 1e3: 3.2e-9, 1e4: 2.9e-9}, 6.9e-15, 20e-12),
    "OPA928 (electrometer)": ({100: 18e-9, 1e3: 15e-9}, 0.07e-15, 6e-12),
    "LMC662 (CMOS)": ({1e3: 22e-9}, 4e-15, 5e-12),
}
r0, rf, cs, cf = 81.3e3, 1e6, 3e-9, 10e-12
i_floor = math.sqrt(FOURKT / r0)
i_rf = math.sqrt(FOURKT / rf)
print(f"  diode floor {i_floor:.3g}; Rf noise {i_rf:.3g} A/rtHz ({FOURKT / rf / i_floor ** 2 * 100:.1f}% of the floor in power); "
      f"diode Johnson voltage sqrt(4kTR0) = {math.sqrt(FOURKT * r0) * 1e9:.1f} nV/rtHz, "
      f"|1 + j w R0 Cs| at 1 kHz = {abs(1 + 2j * math.pi * 1e3 * r0 * cs):.2f}")
for name, (en_tab, i_n, c_in) in amps.items():
    for f_, en in en_tab.items():
        y = abs(1 / r0 + 1 / rf + 2j * math.pi * f_ * (cs + cf + c_in))
        i_en = en * y
        tot2 = i_floor ** 2 + i_rf ** 2 + i_en ** 2 + i_n ** 2
        print(f"  {name:22s} {f_:>7.0f} Hz: e_n {en * 1e9:4.1f} nV -> e_n|Y| {i_en:.3g} A/rtHz; "
              f"diode share of the total power {i_floor ** 2 / tot2 * 100:.1f}%")
# frequency where the AD743's e_n|Y| equals the 1 MOhm Johnson noise
y_eq = i_rf / 3.2e-9
f_eq = math.sqrt(max(y_eq ** 2 - (1 / r0 + 1 / rf) ** 2, 0)) / (2 * math.pi * (cs + cf + 20e-12))
print(f"  AD743 e_n|Y| equals the 1 MOhm noise near {f_eq:.0f} Hz; bias 150 pA x 1 MOhm = {150e-12 * rf * 1e3:.2f} mV; "
      f"i_n 6.9 fA = {(6.9e-15 / i_rf) ** 2 * 100:.1f}% of the Rf noise power")
print(f"  stable feedback capacitor sqrt(Cs/(2 pi Rf GBW)) for 4.5 MHz: {math.sqrt(cs / (2 * math.pi * 1e6 * 4.5e6)) * 1e12:.1f} pF at 1 MOhm, "
      f"{math.sqrt(cs / (2 * math.pi * 1e7 * 4.5e6)) * 1e12:.1f} pF at 10 MOhm; bandwidths "
      f"{1 / (2 * math.pi * 1e6 * 10.3e-12) / 1e3:.1f} kHz and {1 / (2 * math.pi * 1e7 * 3.26e-12) / 1e3:.1f} kHz")

print("A single 15 um pixel as the device (R0A <= 813 Ohm cm^2, C scaled by area)")
r_px = 813 / a_pix
c_px = 3e-9 * a_pix / 0.01
fl_px = math.sqrt(FOURKT / r_px)
print(f"  R0 {r_px:.3g} Ohm, C {c_px * 1e12:.2f} pF, floor {fl_px:.3g} A/rtHz, dark current at -0.1 V {J_m01 * a_pix * 1e12:.0f} pA")
print(f"  AD743 i_n 6.9 fA = {(6.9e-15 / fl_px) ** 2 * 100:.0f}% of that floor in power; Rf = 10 GOhm adds "
      f"{FOURKT / 1e10 / fl_px ** 2 * 100:.1f}% and carries {J_m01 * a_pix * 1e10:.2f} V at -0.1 V")

print("Test-current injection")
for c in (1e-12, 10e-12):
    print(f"  {c * 1e12:.0f} pF driven at 1 V rms: {2 * math.pi * 10 * c * 1e12:.2f} pA at 10 Hz, {2 * math.pi * 100 * c * 1e12:.1f} pA at 100 Hz, "
          f"{2 * math.pi * 1e3 * c * 1e12:.0f} pA at 1 kHz (SNR {2 * math.pi * 1e3 * c / i_floor:.0f} in a 1 Hz bin against the 1 mm^2 floor)")
for r, cp in ((100e6, 0.2e-12), (10e6, 0.2e-12)):
    print(f"  {r / 1e6:.0f} MOhm with {cp * 1e12:.1f} pF stray: noise {math.sqrt(FOURKT / r):.3g} A/rtHz "
          f"({FOURKT / r / i_floor ** 2 * 100:.1f}% of the floor), current up 3 dB at {1 / (2 * math.pi * r * cp) / 1e3:.0f} kHz")

# injection efficiency of a direct-injection input at the pixel's dark current (weak inversion, slope factor 1.3)
r_pix = 813 / a_pix                                  # ohm, chord bound on R0 per pixel
i_pix = J_m01 * a_pix
gm = i_pix / (1.3 * ut)
for gain in (1, 100):
    rin = 1 / (gm * gain)
    print(f"  {'DI' if gain == 1 else 'BDI, A = 100'}: input resistance {rin / 1e6:.3g} MOhm against R0 {r_pix / 1e6:.0f} MOhm, "
          f"injection efficiency {r_pix / (r_pix + rin) * 100:.1f}%")
