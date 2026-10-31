"""Numbers for the question of how pixel pitch changes mid- and long-wave infrared focal-plane arrays.
Prints: F*lambda/d and the diffraction x pixel-aperture MTF at Nyquist for LWIR and MWIR cases; lens focal length,
aperture and field for 12 um VGA and 8 um SXGA modules; array die areas; the phonon-limited NETD scaling and its
F-number compensation; and 300 K background photon rates per pixel for cooled MWIR and LWIR photon detectors.
Usage: ir_pixel_pitch.py"""
import math

H, C, KB = 6.62607015e-34, 2.99792458e8, 1.380649e-23


def mtf_diff(nu_per_mm, lam_um, fnum):
    x = nu_per_mm * lam_um * 1e-3 * fnum
    if x >= 1:
        return 0.0
    return (2 / math.pi) * (math.acos(x) - x * math.sqrt(1 - x * x))


print("== Sampling against diffraction (monochromatic; 100% fill-factor pixel aperture)")
for band, lam, fnums, pitches in (("LWIR", 10.0, (1.0, 0.8), (17, 12, 10, 8, 5)),
                                  ("MWIR", 4.0, (2.0, 4.0), (15, 10, 8, 5))):
    for fn in fnums:
        for d in pitches:
            nyq = 1000.0 / (2 * d)            # cycles/mm
            md = mtf_diff(nyq, lam, fn)
            mp = 2 / math.pi                   # sinc at Nyquist
            print(f"  {band} {lam:.0f} um F/{fn:.1f} d={d:2d} um: F*lam/d={fn * lam / d:.2f}, Nyquist {nyq:.1f} cy/mm, "
                  f"cut-off {1000 / (lam * fn):.0f} cy/mm, MTF_diff {md:.3f}, x pixel {md * mp:.3f}")
print(f"  Airy diameter 2.44*lam*F: LWIR F/1 {2.44 * 10:.1f} um; MWIR F/2 {2.44 * 4 * 2:.1f} um, F/4 {2.44 * 4 * 4:.1f} um")

print("== Lenses and fields")
for name, n_h, d_um, f_mm in (("VGA 12 um, 18 mm", 640, 12, 18.0), ("SXGA 8 um, 12 mm", 1280, 8, 12.0),
                               ("SXGA 8 um, 18 mm", 1280, 8, 18.0), ("SXGA 8 um, 24 mm", 1280, 8, 24.0)):
    hfov = 2 * math.degrees(math.atan(n_h * d_um * 1e-3 / 2 / f_mm))
    print(f"  {name}: HFOV {hfov:.1f} deg, IFOV {d_um / f_mm:.3f} mrad, F/1 aperture {f_mm:.0f} mm")
f12 = 640 * 12e-3 / (2 * math.tan(math.radians(12)))
print(f"  VGA 12 um at 24 deg needs f = {f12:.2f} mm; same IFOV with 8 um pitch needs f = {f12 * 8 / 12:.2f} mm")
print(f"  aperture ratio 8/12 = {8 / 12:.3f}; area ratio {(8 / 12) ** 2:.3f}; volume ratio if all lens dimensions scale {(8 / 12) ** 3:.3f}")
ped = 0.5 / 200 * 1e3
print(f"  0.5 m pedestrian at 200 m = {ped:.2f} mrad = {ped / 0.667:.1f} px at 0.667 mrad, {ped / 0.333:.1f} px at 0.333 mrad")

print("== Array die areas (active array only)")
for nx, ny in ((640, 512), (1280, 1024), (1920, 1080)):
    for d in (12, 8):
        print(f"  {nx}x{ny} at {d} um: {nx * d * 1e-3:.2f} x {ny * d * 1e-3:.2f} mm = {nx * ny * (d * 1e-3) ** 2:.1f} mm^2")

print("== Microbolometer phonon-limited NETD at fixed thermal time constant and F-number: NETD ~ 1/d")
print(f"  12 -> 8 um: x{12 / 8:.2f}; 17 -> 12 um: x{17 / 12:.2f}")
for f_new in (0.8, 0.9):
    print(f"  F/1 -> F/{f_new}: (4F^2+1) ratio {(4 * f_new ** 2 + 1) / 5:.3f}")


def photon_exitance(l1_um, l2_um, t_k, n=4000):
    """pi * band-integrated photon radiance of a blackbody, photons s^-1 m^-2."""
    s = 0.0
    dl = (l2_um - l1_um) * 1e-6 / n
    for i in range(n):
        lam = (l1_um * 1e-6) + (i + 0.5) * dl
        s += 2 * math.pi * C / lam**4 / (math.exp(H * C / (lam * KB * t_k)) - 1.0) * dl
    return s


print("== 300 K background photon rate per pixel (extended scene, lens transmission 1, QE 0.7)")
for band, (l1, l2), fnums in (("MWIR 3.4-4.8 um", (3.4, 4.8), (2.0, 4.0)), ("MWIR 3.4-4.2 um", (3.4, 4.2), (2.0, 4.0)),
                              ("LWIR 8-10 um", (8.0, 10.0), (2.0,))):
    m = photon_exitance(l1, l2, 300.0)
    print(f"  {band}: photon exitance {m * 1e-4:.2e} cm^-2 s^-1")
    for fn in fnums:
        for d in (15, 10, 8, 5):
            rate = 0.7 * m / (4 * fn**2 + 1) * (d * 1e-6) ** 2
            print(f"    F/{fn:.0f}, {d:2d} um: {rate:.2e} e-/s = {rate * 1e-3:.2e} e-/ms")

print("== Thermal contrast C = (1/Phi) dPhi/dT at 300 K and the well-limited NETD = 1/(C sqrt(N_well))")
for band, (l1, l2) in (("MWIR 3.4-4.8 um", (3.4, 4.8)), ("MWIR 3.4-4.2 um", (3.4, 4.2)), ("LWIR 8-10 um", (8.0, 10.0))):
    m0, m1 = photon_exitance(l1, l2, 299.5), photon_exitance(l1, l2, 300.5)
    c_th = (m1 - m0) / (0.5 * (m0 + m1))
    out = ", ".join(f"{nw / 1e6:.1f} Me- -> {1e3 / (c_th * math.sqrt(nw)):.1f} mK" for nw in (0.5e6, 1e6, 4e6))
    print(f"  {band}: C = {100 * c_th:.2f} %/K; {out}")
