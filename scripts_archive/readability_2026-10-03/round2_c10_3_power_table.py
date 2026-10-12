"""Round 2b/2c: the §C10.3 power table on the report-wide conventions.

ToF: 940 nm SPAD model of §C0 subsection 10.3 and §C7a with the 0.05 x 0.05 deg macro-pixel: n_req = 21.7 detected
counts (x1.45 over the ideal 15.0), eta = optics 0.5 x PDE 0.37 x live fraction 0.885 = 0.164, 25 mm aperture.
Coherent: eta = 0.25 (optics x detector x mixing, excluding polarization and mode shape), whose single-polarization
and truncation factor t^2/2 = 0.419 sits in A_mode = (t^2/2) lambda^2 / Omega_cell (§C0 subsection 10.1, §C10.3b),
N_req = 10-30 detected photoelectrons per sample. Field 120 x 25 deg, 200 m, 10 % target, 10 Hz (Eq. (139)).
Usage: python round2_c10_3_power_table.py
"""
import numpy as np

H, C = 6.62607015e-34, 2.99792458e8
DEG = np.pi / 180
R, RHO, F_FRAME = 200.0, 0.10, 10.0
OMEGA_FOV = (120 * DEG) * (25 * DEG)
A_RX = np.pi * 0.0125 ** 2
T2_HALF = (1 - np.exp(-2 * (0.5 / 0.45) ** 2)) ** 2 / 2

lam_c, lam_t = 1550e-9, 940e-9
e_c, e_t = H * C / lam_c, H * C / lam_t
eta_c, eta_t = 0.25, 0.5 * 0.37 * np.exp(-1.83e8 / 9 * 6e-9)
n_t = 21.7
base = np.pi * R ** 2 * F_FRAME * OMEGA_FOV / RHO
p_coh = {n: n * e_c * base / (T2_HALF * lam_c ** 2 * eta_c) for n in (10, 30)}
print(f"t^2/2 = {T2_HALF:.3f}; eta_ToF = {eta_t:.4f}; Omega_FOV = {OMEGA_FOV:.3f} sr; pi R^2 f Omega/rho = {base:.3e}")
print(f"P_coh (N_req 10 / 30, eta 0.25, t^2/2 in A_mode): {p_coh[10]:.1f} / {p_coh[30]:.1f} W on every grid")
print(f"  for comparison, eta 0.112 (measured, Waymo chain) raises these by {0.25/0.112:.2f}x to "
      f"{p_coh[10]*0.25/0.112:.0f} / {p_coh[30]*0.25/0.112:.0f} W")
for cell in ((0.1, 0.1), (0.1, 0.05), (0.05, 0.05), (0.025, 0.025), (0.0125, 0.0125)):
    om = cell[0] * DEG * cell[1] * DEG
    p_t = n_t * e_t * base / (A_RX * om * eta_t)
    print(f"  {cell[0]}° x {cell[1]}°: Omega_cell {om:.3e} sr, P_ToF {p_t:.3f} W, ratio {p_coh[10]/p_t:.1f}-{p_coh[30]/p_t:.0f}x")
om01 = (0.1 * DEG) ** 2
p_t01 = n_t * e_t * base / (A_RX * om01 * eta_t)
for n in (10, 30):
    print(f"parity cell (N_req {n}): 0.1° / sqrt({p_coh[n]/p_t01:.0f}) = {0.1/np.sqrt(p_coh[n]/p_t01):.4f}°")
print(f"diffraction limit lambda/sqrt(A_rx) = {lam_t/np.sqrt(A_RX):.3e} rad = {lam_t/np.sqrt(A_RX)/DEG:.4f}°")
