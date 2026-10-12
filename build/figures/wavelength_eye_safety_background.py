"""Wavelength selection for automotive lidar: Class 1 limits, solar background per
pixel, and detector count-rate headroom.

Companion to section C4c of automotive_perception_report_2026-09-27.md.
Engineering estimates [E] built from tabulated inputs:
- ICNIRP 2013 exposure limits (IEC 60825-1:2014 Class 1 = ICNIRP limit x aperture
  area for 400-1400 nm; small source, C6 = 1), T_i = 5 us for 700-1050 nm;
  C5 = (N/600)^-0.25 with floor 0.4 for pulses shorter than T_i (400-1400 nm only).
- Above 1400 nm: 1 kW m^-2 over a 3.5 mm aperture for long exposures (9.6 mW);
  10 kJ m^-2 over a 1 mm aperture for single pulses shorter than 0.35 s (7.85 mJ).
- ASTM G173-03 global-tilt spectral irradiance, +-10 nm band averages.
A real Class 1 classification must also treat scan failure, the most hazardous
position, Condition 1 and platform motion (IEC TS 60825-19:2024).
"""

from pathlib import Path

import numpy as np


def _output_dir() -> Path:
    """Where figures and tables are written.

    Inside the report folder this script lives in <report>/build/figures, and its outputs go to
    <report>/automotive_perception_report_figures. Run anywhere else (for example after extracting it
    from the PDF's attachments), it writes next to itself.
    """
    here = Path(__file__).resolve().parent
    try:
        figs = here.parents[1] / "automotive_perception_report_figures"
    except IndexError:
        return here
    return figs if figs.is_dir() else here


OUT_DIR = _output_dir()

H = 6.62607015e-34
C = 2.99792458e8
A7 = np.pi * (3.5e-3) ** 2  # 7 mm aperture area, m^2

C4 = {905: 10 ** (0.002 * (905 - 700)), 940: 10 ** (0.002 * (940 - 700))}
G173_BAND = {905: 0.693, 940: 0.303, 1550: 0.270}  # W m^-2 nm^-1, global tilt, +-10 nm


def photons_per_joule(lam_nm: float) -> float:
    return lam_nm * 1e-9 / (H * C)


def c5(n: float) -> float:
    return 1.0 if n <= 600 else max(0.4, (n / 600.0) ** -0.25)


def nir_single_pulse(lam: int) -> float:
    """Class 1 single-pulse AEL, 1 ns <= t < T_i, 700-1050 nm (J)."""
    return 7.7e-8 * C4[lam]


def nir_cw(lam: int) -> float:
    return 3.9e-4 * C4[lam]


def stationary_pulse_limit(lam: int, prf: float, t2: float = 10.0) -> float:
    """Max energy per pulse for a stationary beam fully inside the aperture (J)."""
    if lam == 1550:
        return min(7.85e-3, 9.6e-3 / prf)
    n = prf * t2
    rule1_3 = nir_single_pulse(lam) * c5(n)
    rule2 = nir_cw(lam) / prf
    return min(rule1_3, rule2)


def solar_counts(lam: int, pde: float, filt_nm: float, rho: float = 0.9,
                 d_ap: float = 25e-3, pix_deg=(0.05, 0.05), optics: float = 0.5) -> float:
    """Background counts/s for one receive pixel viewing a sunlit Lambertian scene."""
    phot = G173_BAND[lam] * photons_per_joule(lam)  # photons s^-1 m^-2 nm^-1
    radiance = rho * phot / np.pi  # photons s^-1 m^-2 sr^-1 nm^-1
    area = np.pi * (d_ap / 2) ** 2
    omega = np.radians(pix_deg[0]) * np.radians(pix_deg[1])
    return radiance * filt_nm * area * omega * optics * pde


def main() -> None:
    out = []
    out.append("Class 1 building blocks (small source, IEC 60825-1:2014 via ICNIRP 2013) [E]")
    for lam in (905, 940):
        out.append(f"  {lam} nm: C4 = {C4[lam]:.4f}; single pulse {nir_single_pulse(lam)*1e9:.0f} nJ "
                   f"({nir_single_pulse(lam)*0.4*1e9:.0f} nJ at the C5 floor); CW {nir_cw(lam)*1e3:.2f} mW")
    out.append("  1550 nm: single pulse (<0.35 s, 1 mm aperture) 7.85 mJ; CW (3.5 mm aperture) 9.6 mW")
    out.append(f"  940/905 C4 ratio: {C4[940]/C4[905]:.4f}")
    out.append("")
    out.append("Photons per joule relative to 905 nm: "
               + ", ".join(f"{lam} nm {photons_per_joule(lam)/photons_per_joule(905):.3f}" for lam in (940, 1550)))
    out.append(f"CW ratio 1550/905: power {9.6e-3/nir_cw(905):.1f}x, photons "
               f"{9.6e-3/nir_cw(905)*photons_per_joule(1550)/photons_per_joule(905):.1f}x")
    out.append("")
    out.append("Stationary beam, short pulses: max energy per pulse (nJ) and 1550/905 ratio")
    for prf in (1e3, 1e4, 1e5, 1e6):
        e905, e940, e1550 = (stationary_pulse_limit(l, prf) for l in (905, 940, 1550))
        out.append(f"  {prf/1e3:>6.0f} kHz: 905 {e905*1e9:8.1f}  940 {e940*1e9:8.1f}  1550 {e1550*1e9:10.1f}"
                   f"  ratio {e1550/e905:6.0f}x")
    out.append("")
    out.append("Solar background per receive pixel (25 mm aperture, 0.05 x 0.05 deg, rho 0.9, optics 0.5) [E]")
    cases = [(905, 0.24, 20), (905, 0.24, 40), (940, 0.37, 10), (1550, 0.30, 10), (1550, 0.80, 10)]
    for lam, pde, filt in cases:
        n = solar_counts(lam, pde, filt)
        out.append(f"  {lam} nm, efficiency {pde:.2f}, {filt:.0f} nm filter: {n:.2e} counts/s")
    out.append("")
    out.append("Count-rate headroom: background / maximum sustainable detector count rate")
    si_max = 60e6 * 9  # 3x3 Si SPAD macro-pixel, 60 Mcps per SPAD (Sony ISSCC 2021)
    ingaas_max = 1e6  # InGaAs/InP SPAD, ~1 Mcps max with 1-10 us hold-off (Telesca 2024)
    n940 = solar_counts(940, 0.37, 10)
    n1550 = solar_counts(1550, 0.30, 10)
    out.append(f"  Si SPAD 3x3 at 940 nm: {n940:.2e} / {si_max:.1e} = {n940/si_max:.2f}")
    out.append(f"  InGaAs SPAD pixel at 1550 nm: {n1550:.2e} / {ingaas_max:.0e} = {n1550/ingaas_max:.0f}")
    text = "\n".join(out)
    (OUT_DIR / "wavelength_eye_safety_background_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
