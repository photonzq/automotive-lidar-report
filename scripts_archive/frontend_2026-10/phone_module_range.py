"""Numbers for "Why a better chip does not close the gap" (Part B, consumer electronics, after "Why range is
expensive"; Eqs. (31)-(35), 2026-10-29).

Sunlit range, Eq. (34): R ~ eta^(1/4) (E/Omega_FOV)^(1/2) (G/t)^(1/4), with G = A_rx * Omega_pix the pixel
etendue and, Eq. (35), G = (pi/4) (p/F#)^2 for a pixel of pitch p behind a lens of f-number F#.
Without sunlight, Eq. (31) at a fixed count gives R ~ (eta G)^(1/2).
"""
from math import pi, radians, tan

print("R^2 factors from 8 m:", {r: round((r / 8) ** 2, 1) for r in (30, 40, 60, 200)})
print("8 m -> 40 m in sunlight: product eta (E/Omega)^2 G/t must grow by 5^4 =", 5 ** 4)

# Chip: PDE 28% (Sony IMX611 at 940 nm, consumer table) -> 45% (RoboSense 3rd-gen SPAD, §C4b) -> 100%
for pde in (0.45, 1.00):
    g = pde / 0.28
    print(f"PDE 28% -> {pde:.0%}: eta x{g:.2f}; sunlit range x{g ** 0.25:.3f}; range without sunlight x{g ** 0.5:.3f}")

# Receiver: assumed phone-class receiver, 10.1 um SPADs, 170 pixels across a 60 deg field, f/1.5
p, n_pix, fov, fnum = 10.1e-6, 170, 60.0, 1.5
f = n_pix * p / (2 * tan(radians(fov / 2)))
d = f / fnum
print(f"phone receiver: f = {f * 1e3:.3f} mm, D = {d * 1e3:.3f} mm, pixel angle p/f = {p / f * 180 / pi:.3f} deg")
print(f"x25: D = {25 * d * 1e3:.1f} mm, f = {25 * f * 1e3:.1f} mm")
vol = pi * (25 * d / 2 * 1e3) ** 2 * (25 * f * 1e3)
print(f"lens-to-sensor cylinder {vol:,.0f} mm3 = {vol / 235:.0f} x the 235 mm3 iPhone LiDAR module")
w, h = 140 * 10.08e-3, 170 * 10.08e-3
print(f"IMX611 array {w:.2f} x {h:.2f} mm; x25: {25 * w:.1f} x {25 * h:.1f} mm (full frame 36 x 24 mm)")

g_phone = pi / 4 * (p / fnum) ** 2
a_rx, om = pi * 12.5e-3 ** 2, radians(0.05) ** 2      # 25 mm aperture, 0.05 deg macro-pixel (§C0 subsection 4.2)
g_model = a_rx * om
print(f"G phone SPAD = {g_phone:.3e} m2 sr; G model = {a_rx:.3e} x {om:.3e} = {g_model:.3e} m2 sr; "
      f"ratio {g_model / g_phone:.2f}; fourth root {(g_model / g_phone) ** 0.25:.2f}")
print(f"lens area ratio (25/{d * 1e3:.2f})^2 = {(25e-3 / d) ** 2:.0f}; pixel solid-angle ratio "
      f"({p / f * 180 / pi:.3f}/0.05)^2 = {(p / f * 180 / pi / 0.05) ** 2:.1f}")

# Products
print(f"VL53L9 6.0 m -> 40 m: (40/6)^2 = {(40 / 6) ** 2:.1f} (energy per sr), (40/6)^4 = {(40 / 6) ** 4:.0f} (etendue)")
print(f"iPhone LiDAR module (Bonanno 2024 via the report): (1.22+3.00)/5.91 = {(1.22 + 3.00) / 5.91:.3f}; "
      f"SPAD die 0.69/5.91 = {0.69 / 5.91:.3f}")
