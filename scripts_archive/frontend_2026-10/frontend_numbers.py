"""Numbers for the receive front-end subsection of §C4b (Oct 2026).

Every input is a datasheet typical value or a figure quoted in the report; the
source of each is given next to it. Prints each result used in the text.
"""
from math import pi, sqrt

q = 1.602e-19  # elementary charge, C

# --- 1. Supply power per channel, from datasheet typical supply currents ---
parts = {
    # name: (supply current A, supply voltage V, channels sharing it)
    "OPA855 (SBOS622D p7, 5 V)": (17.8e-3, 5.0, 1),
    "OPA856 (SBOS623 p6, 5 V)": (17.2e-3, 5.0, 1),
    "LMH32401 (SBOS965D p1, 3.3 V)": (30e-3, 3.3, 1),
    "MAX40660 active (Rev 6 p4, 3.3 V)": (41e-3, 3.3, 1),
    "MAX40660 standby (Rev 6 p4, 3.3 V)": (8e-3, 3.3, 1),
}
print("1. Power per channel")
per_ch = {}
for name, (i, v, n) in parts.items():
    p = i * v / n
    per_ch[name] = p
    print(f"   {name}: {p*1e3:.1f} mW")
ltc = 0.200 / 4  # LTC6561: 200 mW for 4 channels (Rev C p1)
print(f"   LTC6561 (Rev C p1): {ltc*1e3:.0f} mW per input")

# --- 2. 128 always-on channels against whole-lidar power ---
print("2. 128 channels, always on")
for name in ("OPA855 (SBOS622D p7, 5 V)", "LMH32401 (SBOS965D p1, 3.3 V)",
             "MAX40660 active (Rev 6 p4, 3.3 V)"):
    tot = 128 * per_ch[name]
    print(f"   {name}: {tot:.1f} W = {tot/13.5:.2f} x AT128 (13.5 W), "
          f"{tot/8:.2f} x ATX (8 W)")

# --- 3. Op-amp TIA bandwidth for a Butterworth response ---
# f_3dB ~ sqrt(GBW / (2 pi R_F C_T)); C_T = photodiode + common-mode + differential input C
def f3db(gbw, rf, ct):
    return sqrt(gbw / (2 * pi * rf * ct))

def cf_butterworth(gbw, rf, ct):
    # from 2*zeta/w0 = R_F C_F + 1/w_A with zeta = 1/sqrt(2), w0 = 2 pi f3db
    w0 = 2 * pi * f3db(gbw, rf, ct)
    wa = 2 * pi * gbw
    return (sqrt(2) / w0 - 1 / wa) / rf

gbw855 = 8e9
c_amp = 0.6e-12 + 0.2e-12  # OPA855 common-mode + differential input capacitance
print("3. OPA855 TIA bandwidth")
for label, rf, cpd in (("APD 1 pF, R_F 10 kOhm", 10e3, 1e-12),
                       ("datasheet check: 10 pF, R_F 12 kOhm", 12e3, 10e-12),
                       ("SiPM channel 20 pF, R_F 10 kOhm", 10e3, 20e-12),
                       ("SiPM channel 20 pF, R_F 1 kOhm", 1e3, 20e-12)):
    ct = cpd + c_amp
    print(f"   {label}: C_T = {ct*1e12:.1f} pF, f_3dB = {f3db(gbw855, rf, ct)/1e6:.0f} MHz, "
          f"C_F = {cf_butterworth(gbw855, rf, ct)*1e12:.3f} pF")
ct_apd = 1e-12 + c_amp
print(f"   high-frequency noise gain 1 + C_T/C_F (1 pF APD, 10 kOhm): "
      f"{1 + ct_apd / cf_butterworth(gbw855, 10e3, ct_apd):.1f}")
k_B, T = 1.380649e-23, 300.0
print(f"   R_F thermal noise: 10 kOhm {sqrt(4*k_B*T/10e3)*1e12:.2f} pA/rtHz, "
      f"1 kOhm {sqrt(4*k_B*T/1e3)*1e12:.2f} pA/rtHz")

# --- 4. One photoelectron against amplifier noise ---
t_p = 4e-9          # pulse length, as in §C7b subsection 1
i_noise = 49e-9     # LMH32401 at 20 kOhm, integrated to 250 MHz (SBOS965D p7)
print("4. One photoelectron, spread over 4 ns, against 49 nA rms")
for label, gain in (("Si APD, M = 100", 100), ("InGaAs APD, M = 10", 10),
                    ("SiPM, G = 1.1e6", 1.1e6)):
    i1 = gain * q / t_p
    print(f"   {label}: {i1*1e9:.3g} nA = {i1/i_noise:.3g} sigma")
print(f"   SiPM-to-APD charge ratio: {1.1e6/100:.0f} to {1.1e6/10:.0f}")

# --- 5. Overload ---
print("5. Overload")
print(f"   10 kOhm x 100 mA = {10e3*0.1:.0f} V; OPA855 half swing 1.5 V -> "
      f"{10e3*0.1/1.5:.0f} x overdrive (datasheet recovery spec is at 2 x)")
print(f"   LMH32401 linear range at 20 kOhm: {1.5/20e3*1e6:.0f} uA; "
      f"100 mA is {0.1/(1.5/20e3):.0f} x that")

# --- 6. Coherent: voltage noise times input capacitance ---
e_n, f = 1.0e-9, 280e6  # 1 nV/rtHz amplifier, at Rogers et al.'s 280 MHz bandwidth
print("6. e_n * 2 pi f C_T at 280 MHz, e_n = 1 nV/rtHz")
for c in (0.5e-12, 1.5e-15):
    print(f"   C_T = {c*1e15:.1f} fF: {2*pi*f*c*e_n*1e12:.4f} pA/rtHz")
print(f"   Rogers et al. receiver chip: 250 mW / 8 outputs = {250/8:.1f} mW per output")

# --- 7. Hesai fourth-generation ASIC board ---
print("7. Hesai: 24.6e9 samples/s on one 512-channel board")
print(f"   average per channel {24.6e9/512/1e6:.0f} MS/s; channels at 1 GS/s: {24.6e9/1e9:.1f}; "
      f"at 0.5 GS/s: {24.6e9/0.5e9:.1f}")
