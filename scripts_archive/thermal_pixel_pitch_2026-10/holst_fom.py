"""Range figure of merit of Holst and Driggers (Opt. Eng. 51, 096401, 2012, Eq. 8) applied to thermal-camera pixel pitch.
Range = W sqrt(C_target)/V x FOM(F lambda/d) x D/lambda (their Eq. 10; high SNR, clear air, human observer on a
flat-panel display). Prints FOM and range ratios at fixed aperture and at fixed IFOV, plus a check of the
well-limited NETD of cooled photon detectors against their Figs. 11 and 14. Usage: holst_fom.py"""
import math

H, C, KB = 6.62607015e-34, 2.99792458e8, 1.380649e-23


def fom(x):
    """Holst and Driggers Eq. 8, x = F lambda / d, valid up to x = 4."""
    return (-0.0254 * x**6 + 0.2686 * x**5 - 0.9282 * x**4 + 1.1314 * x**3
            - 1.6296 * x**2 + 7.6343 * x)


print("== FOM(x)")
for x in (0.41, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
    print(f"  x={x:4.2f}: FOM={fom(x):6.3f}")
xs = [i / 1000 for i in range(0, 4001)]
xm = max(xs, key=fom)
print(f"  maximum of the fit on 0-4: FOM={fom(xm):.3f} at x={xm:.2f}")

LAM = 10.0  # um, the paper's average LWIR wavelength
print("== LWIR, F/1: fixed aperture (range ~ FOM) and fixed IFOV and F-number (range ~ FOM x d ~ FOM/x)")
ref = None
rows = []
for d in (17, 12, 10, 8, 6, 5):
    x = 1.0 * LAM / d
    rows.append((d, x, fom(x)))
f12 = fom(LAM / 12)
for d, x, fm in rows:
    same_ap = fm / f12
    same_ifov = (fm * d) / (f12 * 12)
    print(f"  d={d:2d} um: x={x:.3f}, FOM={fm:.3f}, range vs 12 um at same aperture {same_ap:.3f}, "
          f"at same IFOV {same_ifov:.3f}, % of max {100 * fm / fom(xm):.1f}")
print("  examples, IFOV 0.667 mrad at F/1: 12 um / 18 mm, 8 um / 12 mm, 6 um / 9 mm, 5 um / 7.5 mm")
for d, D in ((12, 18.0), (8, 12.0), (6, 9.0), (5, 7.5)):
    x = LAM / d
    print(f"    d={d} um, D={D} mm: FOM x D = {fom(x) * D:.1f} (12 um: {f12 * 18:.1f}) -> {fom(x) * D / (f12 * 18):.3f}")
print("  F/1.2 cases: 6 um x =", round(1.2 * LAM / 6, 3), "FOM", round(fom(1.2 * LAM / 6), 3),
      "| 12 um F/1.2 x =", round(1.2 * LAM / 12, 3))
print("  Airy diameter 2.44 lambda F at F/1:", 2.44 * LAM, "um; equals d at x = 1/2.44 =", round(1 / 2.44, 3))
print("  MWIR 2.5 um at F/1: x =", 4.0 / 2.5, "; 3 um at F/1.2: x =", round(1.2 * 4 / 3, 3),
      "; Table 1 F for d = 3 um at x = 2: 2*3/4 =", 2 * 3 / 4)


def photon_band(l1, l2, t, n=4000):
    s = 0.0
    dl = (l2 - l1) * 1e-6 / n
    for i in range(n):
        lam = l1 * 1e-6 + (i + 0.5) * dl
        s += 2 * math.pi * C / lam**4 / (math.exp(H * C / (lam * KB * t)) - 1.0) * dl
    return s


print("== Well-limited NETD = 1/(C sqrt(N_fill)) at 50% fill, for comparison with Figs. 11 and 14")
for band, (l1, l2) in (("LWIR 8-12 um", (8.0, 12.0)), ("MWIR 3.6-5.1 um (no CO2 notch)", (3.6, 5.1))):
    for tc in (-50, 0, 20, 70):
        t = tc + 273.15
        m0, m1 = photon_band(l1, l2, t - 0.5), photon_band(l1, l2, t + 0.5)
        c = (m1 - m0) / (0.5 * (m0 + m1))
        print(f"  {band}, {tc:+d} C: C = {100 * c:.2f} %/K; 12 Me- well (6 Me- fill) {1e3 / (c * math.sqrt(6e6)):.1f} mK, "
              f"6 Me- well (3 Me- fill) {1e3 / (c * math.sqrt(3e6)):.1f} mK")
