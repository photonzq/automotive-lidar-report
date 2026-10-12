"""Dynamic range each design must handle: strongest return / weakest detectable return (dB).

Designs as in C0 subsection 10.6 (each reaches 200 m on a 10% target in clear air, so the weakest
detectable return is exactly the detection level). The strongest returns are a white Lambertian target
and a retroreflective sign at short range. A retroreflector of coefficient R_A (cd lx^-1 m^-2) returns
R_A per sr per unit irradiance per unit area, like a Lambertian surface of reflectance rho_eq = pi R_A.
Both receivers collect the target's radiance (direct detection over its lens, the coherent receiver
through its single mode), so rho_eq enters both link losses the same way, provided the retroreflected
cone (tenths of a degree) is wider than the receiver's acceptance.
"""
import importlib.util
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location(
    "lb", r"<report folder>\build\figures\link_budget_scaling.py")
lb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lb)

R0 = lb.R_DESIGN
cases = [("white 90% Lambertian at 1 m", 0.9, 1.0), ("white 90% at 0.3 m", 0.9, 0.3),
         ("10% target at 10 m", 0.1, 10.0),
         ("retro sign R_A=500 at 30 m", np.pi * 500, 30.0), ("retro sign R_A=500 at 10 m", np.pi * 500, 10.0),
         ("retro sign R_A=500 at 5 m", np.pi * 500, 5.0), ("retro sign R_A=500 at 2 m", np.pi * 500, 2.0)]
print(f"rho_eq of R_A = 500: {np.pi * 500:.0f} ({10 * np.log10(np.pi * 500 / 0.1):.1f} dB above a 10% Lambertian)")
header = f"{'design':42s}" + "".join(f"{c[0][:26]:>28s}" for c in cases)
print(header)
for label, kind, D, _, _ in lb.MARGIN_DESIGNS:
    dz = lb.margin_design(kind, D)
    fn, ld, a0 = dz["fn"], dz["l_det"], dz["a_clear"]
    row = [10 * np.log10(fn(R, a0, rho) / ld) for _, rho, R in cases]
    print(f"{lb.plain(label):42s}" + "".join(f"{x:28.1f}" for x in row))

# peak received power for the strongest case, and what it means for the detector
print()
spad = lb.margin_design("dd", 25e-3)
E_shot = spad["e_tx"] / 10  # the model's 10 shots per point
P_peak = E_shot / 3e-9  # 3 ns pulse
L_retro5 = spad["fn"](5.0, spad["a_clear"], np.pi * 500)
print(f"SPAD design: {E_shot * 1e9:.1f} nJ per shot, peak {P_peak:.2f} W for a 3 ns pulse; retro at 5 m returns "
      f"{P_peak * L_retro5 * 1e3:.1f} mW peak = {P_peak * L_retro5 * 3e-9 / lb.photon_energy(940e-9):.2e} photons per shot "
      f"({P_peak * L_retro5 * 3e-9 / lb.photon_energy(940e-9) * 0.185:.2e} detected); weakest (10% at 200 m) "
      f"{P_peak * spad['l_det'] * 3e-9 / lb.photon_energy(940e-9) * 0.185:.2f} detected photons per shot")
fm = lb.margin_design("coh", lb.MARGIN_DESIGNS[2][2])
P_cw = 30e-3
L_r5 = fm["fn"](5.0, fm["a_clear"], np.pi * 500)
print(f"FMCW best aperture: CW {P_cw * 1e3:.0f} mW; retro at 5 m returns {P_cw * L_r5 * 1e9:.1f} nW into the LO mode, "
      f"weakest {P_cw * fm['l_det'] * 1e12:.2f} pW; against an LO of ~1 mW the photodiodes stay linear")
