"""R6_C10_part2-01: nominal 1/e^2 footprint fraction and mode-equivalent area of the
Pointcloud coherent FPA (Settembrini et al., Nature 2026), from the paper's own numbers.

Inputs (Methods, 'System imaging properties'; Extended Data Figs 2c and 3d):
  wavelength 1.31 um; pixel pitch 53 um; 352 x 176 pixels;
  beam measured behind the f = 25 mm test lens: waist 1.31 mm at 11.1 m, z_R = 4.1 m;
  measured fields: 44.44 x 26.65 deg (f = 25 mm), 23.11 x 13.55 deg (f = 50 mm).
Model (report Eqs. (146)-(147)):
  w(R)   = w0 * sqrt(1 + ((R - z_w)/z_R)^2)
  f_fp   = pi w^2 / (R theta_cell)^2,   theta_cell = 2 atan(p / 2f)
  A_mode = t^2 lambda^2 R^2 / (2 pi w^2)   (t = 1 for a measured beam; t^2 = 0.838 model value)
  identity: A_mode * f_fp = (t^2/2) (lambda/theta_cell)^2
No network access; prints tables only.
"""
import math

lam = 1.31e-6
p = 53e-6
N = 352 * 176
w0, zw, zR = 1.31e-3, 11.1, 4.1
t2_model = 0.838

print(f"z_R from w0: pi w0^2/lambda = {math.pi * w0**2 / lam:.3f} m (paper: 4.1 m)")


def theta(f):
    return 2 * math.atan(p / (2 * f))


def w(R):
    return w0 * math.sqrt(1 + ((R - zw) / zR) ** 2)


def ffp(R, th):
    return math.pi * w(R) ** 2 / (R * th) ** 2


def amode(R, t2=1.0):
    return t2 * lam**2 * R**2 / (2 * math.pi * w(R) ** 2)


def deq(a):
    return 2 * math.sqrt(a / math.pi)


for f in (25e-3, 50e-3):
    th = theta(f)
    print(f"\nlens f = {f*1e3:.0f} mm: theta_cell = {th:.4e} rad = {math.degrees(th):.4f} deg")
    print("  pixels x pitch span: {:.2f} x {:.2f} deg".format(
        352 * math.degrees(th), 176 * math.degrees(th)))
    full_half = 0.5 * (lam / th) ** 2
    print(f"  full coverage (f_fp=1): (1/2)(lam/theta)^2 = {full_half*1e6:.3f} mm^2 "
          f"(d = {deq(full_half)*1e3:.2f} mm); with t^2/2: {t2_model*full_half*1e6:.3f} mm^2 "
          f"(d = {deq(t2_model*full_half)*1e3:.2f} mm)")
    print("   R (m)   w (mm)  cell (mm)  f_fp (%)  A_mode t=1 (mm^2, d mm)  identity check")
    for R in (4.0, 7.2, 11.1, 12.6, 16.0, 22.0, 27.1, 65.0):
        a = amode(R)
        print(f"  {R:5.1f}  {w(R)*1e3:7.2f}  {R*th*1e3:8.2f}  {100*ffp(R, th):7.2f}"
              f"   {a*1e6:7.2f} ({deq(a)*1e3:4.2f})   {a*ffp(R, th)*1e6:.4f} vs {full_half*1e6:.4f}")

# minimum footprint fraction along the range (same for any lens, scaled by 1/theta^2)
Rs = [x / 100 for x in range(200, 7000)]
Rmin = min(Rs, key=lambda R: ffp(R, theta(25e-3)))
print(f"\nminimum f_fp at R = {Rmin:.2f} m: {100*ffp(Rmin, theta(25e-3)):.2f}% (f=25 mm), "
      f"{100*ffp(Rmin, theta(50e-3)):.2f}% (f=50 mm grid)")

# field-based cell solid angle, as in the report's bracket, with the measured fields
for f, (H, V) in ((25e-3, (44.44, 26.65)), (50e-3, (23.11, 13.55)), (50e-3, (23.0, 14.0))):
    om = math.radians(H) * math.radians(V)
    a = t2_model / 2 * N * lam**2 / om
    print(f"\nfield-based bound, f = {f*1e3:.0f} mm, field {H} x {V} deg: Omega = {om:.4f} sr, "
          f"(t^2/2) N lam^2/Omega = {a*1e6:.3f} mm^2, d = {deq(a)*1e3:.2f} mm; "
          f"share of field covered by pixel addresses = "
          f"{(352*math.degrees(theta(f)))*(176*math.degrees(theta(f)))/(H*V):.2f}")

# the report's assumed 2% on the 50 mm grid
th50 = theta(50e-3)
for t2, lab in ((1.0, "1/2"), (t2_model, "t^2/2")):
    a = t2 / 2 * (lam / th50) ** 2 / 0.02
    print(f"\nassumed f_fp = 2% on the 0.061 deg grid, {lab}: A_mode = {a*1e6:.1f} mm^2, d = {deq(a)*1e3:.2f} mm")

# chip size implied by the theoretical fields, FOV = 2 atan(s / 2f)
for f, (H, V) in ((25e-3, (44.27, 26.61)), (50e-3, (23.40, 13.73))):
    sx = 2 * f * math.tan(math.radians(H / 2))
    sy = 2 * f * math.tan(math.radians(V / 2))
    print(f"\nchip size from theoretical field, f = {f*1e3:.0f} mm: {sx*1e3:.2f} x {sy*1e3:.2f} mm "
          f"(pixels alone: {352*p*1e3:.2f} x {176*p*1e3:.2f} mm)")
