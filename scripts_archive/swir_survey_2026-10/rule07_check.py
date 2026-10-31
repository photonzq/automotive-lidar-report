"""Rule 07 dark-current benchmark (Tennant et al., J. Electron. Mater. 37, 1406 (2008)) at the cut-offs of the
SWIR absorbers discussed in the supplement, for comparison with measured leakage. Usage: rule07_check.py"""
import math

J0 = 8367.000019        # A/cm^2
PWR = 0.544071282
C = -1.162972237
LAM_SCALE = 0.200847413  # um
LAM_THR = 4.635136423    # um
K_EV = 8.617333262e-5    # eV/K


def rule07(lam_c_um, t_k):
    """Rule 07 dark current density in A/cm^2 for cut-off wavelength lam_c (um) and temperature T (K)."""
    if lam_c_um >= LAM_THR:
        lam_e = lam_c_um
    else:
        lam_e = lam_c_um / (1 - (LAM_SCALE / lam_c_um - LAM_SCALE / LAM_THR) ** PWR)
    return J0 * math.exp(C * (1.24 / lam_e) / (K_EV * t_k))


for lam in (1.7, 2.6, 2.7, 2.85):
    for t in (298.0, 373.0):
        j = rule07(lam, t)
        r0a = K_EV * t / j  # ohm cm^2, kT/(qJ)
        print(f"cut-off {lam:.2f} um, {t:.0f} K: Rule 07 J = {j:.3e} A/cm^2 ({j * 1e6:.1f} uA/cm^2), kT/(qJ) = {r0a:.3g} ohm cm^2")
print("measured: PbS (Li et al.) 123.0 uA/cm^2 at -0.1 V; G12183-003K 153.7 uA/cm^2 at -0.1 V (authors), "
      "363 uA/cm^2 equivalent from the typical 100 kohm; G12180-003A 0.036 uA/cm^2 equivalent")
