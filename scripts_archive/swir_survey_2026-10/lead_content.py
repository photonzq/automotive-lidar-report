"""Lead content of a PbS photodiode film on a silicon readout die, for the RoHS/ELV question.
Prints the lead mass fraction of PbS, the lead mass in a 640 x 512, 15 um array with Li et al.'s
0.8 um PbS (500 nm p-PbS + 300 nm n-PbS), and the lead fraction averaged through film plus silicon
under the film for several film and die thicknesses (the most lenient reading of "homogeneous material").
Usage: lead_content.py"""
M_PB, M_S = 207.2, 32.06          # g/mol
RHO_PBS, RHO_SI = 7.60, 2.33      # g/cm^3
W_PB = M_PB / (M_PB + M_S)
print(f"lead mass fraction of PbS: {W_PB:.3f} ({W_PB / 0.001:.0f} times the 0.1 % limit)")

area_mm2 = (640 * 0.015) * (512 * 0.015)
t_film_um = 0.8
vol_cm3 = area_mm2 * 1e-2 * t_film_um * 1e-4
m_pbs_g = vol_cm3 * RHO_PBS
print(f"array area {area_mm2:.1f} mm^2; PbS {m_pbs_g * 1e3:.3f} mg; lead {m_pbs_g * W_PB * 1e3:.3f} mg")

for t_f in (0.2, 0.3, 0.8):
    for t_si in (775.0, 300.0):
        pb = t_f * RHO_PBS * W_PB
        tot = t_f * RHO_PBS + t_si * RHO_SI
        print(f"film {t_f:.1f} um on {t_si:.0f} um Si: lead {100 * pb / tot:.3f} wt% of film + silicon")
