"""§C0 subsection 10.8, Panasonic flash row: photons per pixel per pulse from Eq. (55) of the report, with the inputs
of Hirose et al., "A 250 m direct time-of-flight ranging system based on a synthesis of sub-ranging images and a
vertical avalanche photo-diodes (VAPD) CMOS image sensor", Sensors 18, 3642 (2018), doi:10.3390/s18113642:
  - 940 nm; four 300 W sources, 10 ns FWHM pulses (its photon estimate, Fig. 2, assumes 1.2 kW, 10 ns, a 20° field
    and a 10% target; its experiments use an f/1.4 lens and a 10° field);
  - 688 x 384 pixels of 11.2 µm (its Table 2).
Eq. (55) solved for the mean count with eta = 1 (photons arriving at a pixel through the lens, before the PDE, which
is what the paper's Fig. 2 plots): n = rho * E_px * A_rx / (pi * R^2 * E_ph), with the pulse spread evenly over the
pixels (illumination filling the camera's field) and the lens aperture D = f/1.4, f = (array width / 2) / tan(FOV/2).
Run: python round5_panasonic_photons.py   (no files read or written)
"""
import math

H, C = 6.62607015e-34, 2.99792458e8
lam, rho, R = 940e-9, 0.10, 100.0
e_ph = H * C / lam
e_pulse = 4 * 300.0 * 10e-9
pixels = 688 * 384
e_px = e_pulse / pixels
half_width = 688 * 11.2e-6 / 2
print(f"E_ph = {e_ph:.4g} J, pulse = {e_pulse * 1e6:.1f} uJ, pixels = {pixels}, E_px = {e_px * 1e12:.1f} pJ, "
      f"array width = {2 * half_width * 1e3:.2f} mm")
for fov in (20.0, 10.0):
    f = half_width / math.tan(math.radians(fov / 2))
    d = f / 1.4
    a = math.pi * d ** 2 / 4
    n = rho * e_px * a / (math.pi * R ** 2 * e_ph)
    print(f"FOV {fov:.0f} deg: f = {f * 1e3:.2f} mm, D = {d * 1e3:.2f} mm, A_rx = {a * 1e4:.3f} cm^2, "
          f"n(100 m) = {n:.3f}, n(250 m) = {n * (100 / 250) ** 2:.4f}; paper's Fig. 2 at 100 m (about 1.2) / n = {1.2 / n:.1f}")
