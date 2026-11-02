"""Op-amp candidates for a 1 MOhm TIA reading the 1 mm^2 PbS diode of the SWIR side note (§S2.8).
Criterion: the op amp's voltage-noise current e_n|Y| should not exceed the feedback resistor's Johnson noise, and its
current noise should stay below a third of it; |Y| = |1/R0 + 1/Rf + j 2 pi f (Cs + Cf + Cin)|.
Datasheet values (typical, 25 C): AD743 Rev. E p. 2; OPA828 SBOS671D p. 5; OPA827 SBOS376I p. 6 (10 and 100 Hz read by
eye from Fig. 1, p. 8); OPA140 SBOS498F p. 7; OPA1656 SBOS901C p. 6. Usage: opamp_candidates.py"""
import math

KB, T = 1.380649e-23, 298.0
FOURKT = 4 * KB * T
R0, CS = 81.3e3, 3e-9             # chord bound on R0 and zero-bias capacitance of the 1 mm^2 diode (§S2.3, §S2.4)
CF = 10e-12

# name: (e_n by frequency [V/rtHz], i_n [A/rtHz], GBW [Hz], C_in [F], status)
PARTS = {
    "AD743":   ({10: 5.5e-9, 100: 3.6e-9, 1e3: 3.2e-9}, 6.9e-15, 4.5e6, 20e-12, "not recommended for new designs"),
    "OPA828":  ({10: 7.5e-9, 100: 4.8e-9, 1e3: 4.0e-9}, 1.2e-15, 45e6, 9e-12, "active"),
    "OPA827":  ({10: 9e-9, 100: 5e-9, 1e3: 4.0e-9}, 2.2e-15, 22e6, 9e-12, "active (10, 100 Hz by eye)"),
    "OPA140":  ({10: 8.0e-9, 100: 5.8e-9, 1e3: 5.1e-9}, 0.8e-15, 11e6, 10e-12, "active, rail-to-rail output"),
    "OPA1656": ({100: 11.8e-9, 1e3: 4.3e-9}, 6e-15, 53e6, 9.1e-12, "active, CMOS input; GBW at G = 100"),
}
# the loop of a TIA with 3 nF at the input crosses near a noise gain of Cs/Cf ~ 300, so the gain-bandwidth product
# quoted at high gain is the relevant one where a part lists two (OPA1656: 53 MHz at G = 100, 20 MHz at G = 1)


def y_in(f, rf, c_in):
    return abs(1 / R0 + 1 / rf + 2j * math.pi * f * (CS + CF + c_in))


i_floor = math.sqrt(FOURKT / R0)
for rf in (1e6, 10e6):
    i_rf = math.sqrt(FOURKT / rf)
    print(f"Rf = {rf / 1e6:.0f} MOhm: Johnson noise {i_rf * 1e15:.0f} fA/rtHz ({FOURKT / rf / i_floor ** 2 * 100:.1f}% of the diode floor "
          f"{i_floor * 1e15:.0f} fA/rtHz in power)")
    print("  largest e_n meeting e_n|Y| <= Rf noise: " + ", ".join(
        f"{f:.0f} Hz {i_rf / y_in(f, rf, 9e-12) * 1e9:.1f} nV" for f in (10, 100, 1e3, 3e3, 1e4)))
rf = 1e6
i_rf = math.sqrt(FOURKT / rf)
print(f"current-noise limit (a third of the 1 MOhm noise): {i_rf / 3 * 1e15:.0f} fA/rtHz")
for name, (en_tab, i_n, gbw, c_in, status) in PARTS.items():
    cells = []
    for f, en in en_tab.items():
        i_en = en * y_in(f, rf, c_in)
        share = i_floor ** 2 / (i_floor ** 2 + i_rf ** 2 + i_en ** 2 + i_n ** 2)
        cells.append(f"{f:.0f} Hz: {en * 1e9:.1f} nV -> {i_en * 1e15:.0f} fA ({i_en / i_rf:.2f} x Rf), diode {share * 100:.0f}%")
    en1k = en_tab[1e3]
    y_eq = i_rf / en1k
    f_x = math.sqrt(max(y_eq ** 2 - (1 / R0 + 1 / rf) ** 2, 0)) / (2 * math.pi * (CS + CF + c_in))
    bw1 = math.sqrt(gbw / (2 * math.pi * 1e6 * (CS + c_in)))
    bw10 = math.sqrt(gbw / (2 * math.pi * 1e7 * (CS + c_in)))
    print(f"{name} ({status}): i_n {i_n * 1e15:.1f} fA; " + "; ".join(cells))
    print(f"    e_n|Y| reaches the 1 MOhm noise near {f_x / 1e3:.1f} kHz; bandwidth with 3 nF: {bw1 / 1e3:.0f} kHz at 1 MOhm, "
          f"{bw10 / 1e3:.1f} kHz at 10 MOhm (GBW {gbw / 1e6:.1f} MHz); feedback capacitor "
          f"{math.sqrt(CS / (2 * math.pi * 1e6 * gbw)) * 1e12:.1f} pF at 1 MOhm, {math.sqrt(CS / (2 * math.pi * 1e7 * gbw)) * 1e12:.2f} pF at 10 MOhm")
    i_rf10 = math.sqrt(FOURKT / 1e7)
    i_en10 = en1k * y_in(1e3, 1e7, c_in)
    print(f"    with 10 MOhm at 0 V and 1 kHz: e_n|Y| {i_en10 * 1e15:.0f} fA against 41 fA from the resistor; diode keeps "
          f"{i_floor ** 2 / (i_floor ** 2 + i_rf10 ** 2 + i_en10 ** 2 + i_n ** 2) * 100:.1f}%")
