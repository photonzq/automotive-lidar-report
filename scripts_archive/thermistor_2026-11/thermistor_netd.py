"""Numbers for the §A4 block "The thermistor: where the NETD comes from, and VOx against a-Si".
Computes the 8-14 um blackbody contrast dM/dT, the power a 12 um pixel behind an F/1 lens absorbs per kelvin of scene
temperature, the thermal-fluctuation NETD floor for the membrane of the vacuum-packaging block, the TCR of an activated
thermistor from its activation energy, and the conductivity ratio of VOx and boron-doped a-Si at similar TCR.
Inputs: Honeywell US 6,322,670 B2, Fig. 2 (ln R = 1.8069 + 2600.6/T; rho = 0.43 ohm cm at 20 C); Moreno et al.,
IntechOpen (2012), p. 27, Table 1 (activation energies; a-Si:H,B 5e-3 S/cm); C = 7e-11 J/K and tau = 7-12 ms as in the
vacuum-packaging block (bolometer_vacuum.py). Usage: thermistor_netd.py"""
import math

H, C0, KB, QE = 6.62607015e-34, 2.99792458e8, 1.380649e-23, 1.602176634e-19


def dm_dt(t, lam1=8e-6, lam2=14e-6, n=20000):
    """Derivative of the in-band blackbody exitance with temperature, W m^-2 K^-1 (midpoint rule)."""
    s, dl = 0.0, (lam2 - lam1) / n
    for i in range(n):
        lam = lam1 + (i + 0.5) * dl
        x = H * C0 / (lam * KB * t)
        m = 2 * math.pi * H * C0 ** 2 / lam ** 5 / math.expm1(x)      # spectral exitance, W m^-3
        s += m * x * math.exp(x) / math.expm1(x) / t * dl              # its temperature derivative
    return s


for t in (295.0, 300.0):
    print(f"dM/dT (8-14 um) at {t:.0f} K: {dm_dt(t):.3f} W m^-2 K^-1 = {dm_dt(t) * 1e-4:.3e} W cm^-2 K^-1")

T, A, F = 300.0, (12e-6) ** 2, 1.0
dpdt = A * dm_dt(T) / (4 * F ** 2 + 1)                                  # per unit tau0 * eta * beta
print(f"12 um pixel at F/1: {dpdt:.3e} W per kelvin of scene temperature (tau0 * eta * beta = 1)")
CTH = 7e-11
print(f"rms pixel temperature fluctuation sqrt(k T^2 / C) = {math.sqrt(KB * T ** 2 / CTH) * 1e3:.3f} mK")
for tau in (7e-3, 12e-3):
    g = CTH / tau
    nep = math.sqrt(KB * T ** 2 * g / tau)    # thermal-fluctuation NEP over the 1/(4 tau) noise bandwidth of the pixel
    print(f"tau = {tau * 1e3:.0f} ms: G = {g * 1e9:.1f} nW/K, NEP_TF = {nep:.2e} W, NETD_TF = {nep / dpdt * 1e3:.1f} mK")

B = 2600.6
print(f"Honeywell Fig. 2: E_a = k_B x {B} K = {KB * B / QE:.3f} eV; TCR(293.15 K) = {-B / 293.15 ** 2 * 100:.2f} %/K")
for name, ea in (("VOx, Moreno Table 1", 0.16), ("a-Si:H,B, Moreno Table 1", 0.22), ("intrinsic a-Si:H, 0.8 eV", 0.8)):
    print(f"{name}: E_a = {ea} eV -> TCR(300 K) = {-ea * QE / (KB * 300.0 ** 2) * 100:.2f} %/K")
print(f"metal with rho proportional to T: TCR = 1/T = {100 / 293.15:.2f} %/K at 293 K")
print(f"conductivity at similar TCR: VOx {1 / 0.43:.2f} S/cm against a-Si:H,B 5e-3 S/cm, ratio {1 / 0.43 / 5e-3:.0f}")
print(f"1/f-limited NETD at fixed tau, film thickness and material scales as 1/d: 12 -> 8 um costs {12 / 8:.2f}x")
