"""Photon budget of a camera pixel at night, for Part A section A7 ("starlight" night vision).

All numbers are engineering estimates [E] for a Lambertian target imaged on axis.

Chain of equations (numbered as in the report section):
  image-plane illuminance      E_img = tau_o * rho * E_s / (4 N^2)
  photoelectrons / pixel/frame  n_pe = eta * Phi_lx * E_img * A_pix * t_int
  pixel SNR, integrating CMOS   SNR = n / sqrt(n + i_d t + sigma_r^2)
  pixel SNR, photon counting    SNR = n / sqrt(n + DCR t)          (no read noise)
  read-noise boundary           n_pe = sigma_r^2  ->  E_s*
  SPAD avalanche energy         E_av = C (V_bd + V_ex) V_ex
  SPAD array power at the paralyzable count ceiling  P = N_px * E_av / (e tau_d)

Phi_lx (photons per second per m^2 per lux) depends on the light's spectrum; it is computed here for a
monochromatic 555 nm source and for black bodies, with the CIE photopic curve from the multi-lobe fit of
Wyman, Sloan and Shirley (JCGT 2013).
"""
import numpy as np

H, C = 6.62607015e-34, 2.99792458e8
KM = 683.0  # lm/W at 555 nm


def g(x, mu, s1, s2):
    return np.exp(-0.5 * ((x - mu) / np.where(x < mu, s1, s2)) ** 2)


def ybar(lam_nm):
    """CIE 1931 photopic luminosity function V(lambda), Wyman-Sloan-Shirley multi-lobe fit."""
    return 0.821 * g(lam_nm, 568.8, 46.9, 40.5) + 0.286 * g(lam_nm, 530.9, 16.3, 31.1)


def planck(lam_m, T):
    return 2 * H * C**2 / lam_m**5 / np.expm1(H * C / (lam_m * 1.380649e-23 * T))


def phi_per_lux(T=None, band=(400, 700)):
    """Photon flux per lux (s^-1 m^-2 lx^-1) counted in `band` (nm), for a black body at T or 555 nm if T is None."""
    if T is None:
        return 1.0 / KM / (H * C / 555e-9)
    lam = np.linspace(360, 1100, 7401)  # nm
    s = planck(lam * 1e-9, T)  # arbitrary scale
    lux = KM * np.trapezoid(ybar(lam) * s, lam)  # per unit of s
    m = (lam >= band[0]) & (lam <= band[1])
    photons = np.trapezoid((s * lam * 1e-9 / (H * C))[m], lam[m])
    return photons / lux


print("Photon flux per lux, Phi_lx (photons s^-1 m^-2 lx^-1):")
PHI = {
    "555 nm monochromatic": phi_per_lux(None),
    "5,500 K black body, photons 400-700 nm": phi_per_lux(5500, (400, 700)),
    "2,856 K (CIE A, halogen), photons 400-700 nm": phi_per_lux(2856, (400, 700)),
    "2,856 K (CIE A, halogen), photons 400-1,000 nm": phi_per_lux(2856, (400, 1000)),
}
for k, v in PHI.items():
    print(f"  {k:48s} {v:.2e}  ({v / PHI['555 nm monochromatic']:.2f} x the 555 nm value)")

# ---------------------------------------------------------------- optics and sensors
TAU_O = 0.8   # lens x windshield transmission (assumed 0.9 x 0.9)
N_F = 1.6     # f-number
T_INT = 0.030  # s, exposure per frame (30 fps, motion-limited)
PHI_BB = PHI["5,500 K black body, photons 400-700 nm"]  # white light, visible band
SENSORS = {
    # name: (pixel pitch m, efficiency, read noise e-, dark rate e-/s or counts/s)
    "CMOS 3.0 um, RGGB colour pixel": (3.0e-6, 0.25, 1.5, 20.0),
    "CMOS 3.0 um, clear pixel (RCCC)": (3.0e-6, 0.60, 1.5, 20.0),
    "SPAD 6.39 um (Canon-class)": (6.39e-6, 0.50, 0.0, 30.0),
}


def e_img(E_s, rho):
    return TAU_O * rho * E_s / (4 * N_F**2)


def n_pe(E_s, rho, pitch, eta, t=T_INT, phi=PHI_BB):
    return eta * phi * e_img(E_s, rho) * pitch**2 * t


SCENES = [("low-beam hotspot, 5 lux (Sec. A6.1)", 5.0), ("glare-limited zone at 50 m, 0.14 lux", 0.14),
          ("full moon, about 0.1 lux", 0.1), ("quarter moon, about 0.01 lux", 0.01), ("starlight, about 0.001 lux", 0.001)]
print(f"\nPhotoelectrons per pixel per {T_INT * 1e3:.0f} ms frame, f/{N_F}, tau_o = {TAU_O}, white light "
      f"(Phi_lx = {PHI_BB:.2e}); target rho = 0.05 (dark clothing) / 0.5 (light clothing):")
for name, E in SCENES:
    row = []
    for s, (p, eta, sr, dk) in SENSORS.items():
        nd, nl = n_pe(E, 0.05, p, eta), n_pe(E, 0.5, p, eta)
        snr_d = nd / np.sqrt(nd + dk * T_INT + sr**2)
        row.append(f"{s.split(',')[0][:9]}{'(clear)' if 'clear' in s else ('(RGGB)' if 'RGGB' in s else '')}: "
                   f"{nd:.3g}/{nl:.3g} e (SNR_dark {snr_d:.2f})")
    print(f"  {name:42s} | " + " | ".join(row))

# per unit sensor area (same optics): photoelectrons per (3 um)^2 of sensor
print("\nSame optics, per (3.0 um)^2 of sensor area, dark target at 0.01 lux:")
for s, (p, eta, sr, dk) in SENSORS.items():
    n_area = n_pe(0.01, 0.05, 3.0e-6, eta)
    # SPAD: (3 um)^2 of area is (3/6.39)^2 of one pixel; aggregate counts are noiseless, dark counts scale with area
    print(f"  {s:34s} n = {n_area:.3f} e; read noise per readout {sr} e")

# ---------------------------------------------------------------- read-noise boundary
print("\nScene illuminance E_s* at which n_pe = sigma_r^2 (CMOS becomes read-noise limited below it):")
for s, (p, eta, sr, dk) in SENSORS.items():
    if sr == 0:
        continue
    for rho in (0.05, 0.5):
        Es = sr**2 / n_pe(1.0, rho, p, eta)
        print(f"  {s:34s} rho = {rho}: E_s* = {Es:.2f} lux")

# ---------------------------------------------------------------- headlight glare zone versus distance
print("\nIlluminance from the glare-limited zone of a low beam (350 cd), E = I/R^2:")
for R in (20, 30, 50, 80, 100):
    print(f"  R = {R:3d} m: {350 / R**2:.3f} lux")

# ---------------------------------------------------------------- SPAD in daylight: count ceiling and power
E_DAY, RHO_DAY = 1.0e5, 0.2
phi_day = PHI["5,500 K black body, photons 400-700 nm"]
eimg = e_img(E_DAY, RHO_DAY)
p_spad, pde = 6.39e-6, 0.50
rate_attempt = pde * phi_day * eimg * p_spad**2
tau_d = 6e-9
r_max = 1.0 / (np.e * tau_d)
print(f"\nDaylight: scene {E_DAY:.0e} lux, rho {RHO_DAY}: image plane {eimg:.0f} lux, photon flux "
      f"{phi_day * eimg:.2e} s^-1 m^-2; a {p_spad * 1e6:.2f} um pixel would detect {rate_attempt:.2e} s^-1 "
      f"against a paralyzable ceiling 1/(e tau_d) = {r_max:.2e} s^-1 (tau_d = 6 ns)")
for Cd, Vex, Vbd in ((10e-15, 2.0, 15.0), (20e-15, 3.0, 20.0), (40e-15, 4.0, 25.0)):
    Eav = Cd * (Vbd + Vex) * Vex
    for npx in (2.1e6, 3.2e6):
        P = npx * Eav * r_max
        print(f"  C = {Cd * 1e15:.0f} fF, V_ex = {Vex} V, V_bd = {Vbd} V: E_av = {Eav * 1e12:.2f} pJ; "
              f"{npx / 1e6:.1f} MP at the count ceiling -> {P:.1f} W; with 75% fewer detections {0.25 * P:.1f} W")
for frac in (1e-3, 1e-2):
    print(f"  to stay near 1 W at 2.1 MP and 0.5 pJ, the mean detection rate per pixel must be <= "
          f"{1.0 / (2.1e6 * 0.5e-12):.2e} s^-1 (= {1.0 / (2.1e6 * 0.5e-12) / r_max:.4f} of the ceiling)")
    break

# measured avalanche charge (ST 10.17 um 3D BSI SPAD, IISW 2023: 68 fC at V_ex 2.5 V, V_bd 18.6 V) and Canon's bias
q_st = 68e-15
E_st = q_st * (18.6 + 2.5)
print(f"\nST SPAD: E_av = Q (V_bd + V_ex) = 68 fC x 21.1 V = {E_st * 1e12:.2f} pJ")
for Cd in (10e-15, 20e-15):
    E_canon = Cd * 2.5 * (30.0 + 2.5)
    print(f"Canon bias (V_bd 30 V, V_ex 2.5 V), C = {Cd * 1e15:.0f} fF: E_av = {E_canon * 1e12:.2f} pJ; "
          f"2.1 MP at the 6 ns ceiling -> {2.1e6 * E_canon * r_max:.0f} W")

# ---------------------------------------------------------------- dark counts versus temperature
print("\nSPAD dark counts per 30 ms frame, Canon-class pixel (1.8 cps at 25 C), doubling every 7 or 12 K:")
for T in (25, 40, 60, 85, 105, 125):
    lo = 1.8 * 2 ** ((T - 25) / 12.0)
    hi = 1.8 * 2 ** ((T - 25) / 7.0)
    print(f"  chip {T:3d} C: {lo:9.1f} - {hi:11.1f} cps  -> {lo * T_INT:8.3f} - {hi * T_INT:9.2f} counts/frame")
print("Panasonic VAPD check: 21 cps (room temperature) -> 10,000 cps at a 105 C chip = x"
      f"{10000 / 21:.0f}, i.e. a doubling every {80 / np.log2(10000 / 21):.1f} K over 80 K")
print("ST check: 810 -> 6,923 cps from 60 to 80 C = doubling every "
      f"{20 / np.log2(6923 / 810):.1f} K; ams: 14 -> 270 cps from 25 to 75 C = doubling every {50 / np.log2(270 / 14):.1f} K")

# ---------------------------------------------------------------- photon-counting gain at equal pixel area
print("\nSNR gain of photon counting over an integrating pixel of the same area and efficiency,")
print("G = sqrt((n + d_cmos + sigma_r^2) / (n + d_spad)), dark clear-pixel signal n from the table above:")
for name, E in SCENES[1:]:
    n = n_pe(E, 0.05, 3.0e-6, 0.60)
    for d_spad_cps, label in ((0.0, "no dark counts"), (1.8 * 2 ** (15 / 7.0) * (3.0 / 6.39) ** 2, "chip 40 C"),
                              (1.8 * 2 ** (35 / 7.0) * (3.0 / 6.39) ** 2, "chip 60 C")):
        d_spad = d_spad_cps * T_INT
        G = np.sqrt((n + 0.0 + 1.5**2) / (n + d_spad))
        print(f"  {name:40s} n = {n:6.3f}: G = {G:5.2f} ({label}, SPAD dark {d_spad:.3f}/frame per (3 um)^2)")
