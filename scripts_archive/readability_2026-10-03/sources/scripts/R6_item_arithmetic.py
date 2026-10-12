"""R6_C10_part2 items 04 and 08: arithmetic behind the proposed edits. No network access.

Item 04: zero-lidar-point shares in nuScenes at 50-80 m from Far3Det (Gupta et al., WACV 2023),
         appendix Table 11 (arXiv 2211.13858v1, p. 12).
Item 08: the ~6 dB coherent-vs-ToF gap of Piggott et al. (arXiv 2502.09736, Sec. 2.5, Fig. 5a)
         against the far-field factor of the report's Gaussian model (w0 = 0.45 D, t = 0.915).
"""
import math

# ---- item 04 -----------------------------------------------------------------------------
table11 = {  # 50-80 m: non-zero-point boxes, zero-point boxes, unoccluded zero-point boxes
    "train": (100123, 45050, 10430),
    "val": (21658, 10069, 2655),
}
for name, (nz, z, unocc) in table11.items():
    total = nz + z
    print(f"{name}: total {total}, zero share {z/total:.4f}, zero/non-zero {z/nz:.4f}, "
          f"unoccluded/total {unocc/total:.4f}, unoccluded/non-zero {unocc/nz:.4f}")

# ---- item 08 -----------------------------------------------------------------------------
db = lambda x: 10 * math.log10(x)
a, w0 = 15.0, 10.0                       # Piggott: 30 mm ToF lens (radius 15 mm), w0 = 10 mm
t_p = 1 - math.exp(-2 * (a / w0) ** 2)   # one-way transmission of that Gaussian through 30 mm
aperture = (a / w0) ** 2
print(f"Piggott: (a/w0)^2 = {aperture:.3f} ({db(aperture):.2f} dB); with polarization "
      f"{2*aperture:.2f} ({db(2*aperture):.2f} dB); clipping t = {t_p:.4f}")
r = 0.5 / 0.45                           # report model: aperture radius / waist
t = 1 - math.exp(-2 * r ** 2)            # one-way truncation, 0.915
shape = r ** 2 / t ** 2
print(f"Model: a/w0 = {r:.3f}, t = {t:.4f}, t^2 = {t*t:.4f}, mode shape and truncation "
      f"{shape:.3f} ({db(shape):.2f} dB); with polarization {2*shape:.3f} ({db(2*shape):.2f} dB)")
print(f"Gap between the two: {db(2*aperture) - db(2*shape):.2f} dB")
