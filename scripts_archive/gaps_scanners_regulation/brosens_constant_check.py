"""Independent check of the constant in Brosens' dynamic-mirror-deformation formula.

Brosens' formula, as reproduced by Urey (Proc. SPIE 4773, 2002, Sec. 5) from
P. J. Brosens, Appl. Opt. 11, 2987-2989 (1972):

    delta_max = 0.217 * rho * f**2 * D**5 * theta_mech / (E * t**2)

with f the scan frequency (Hz), theta_mech the peak mechanical scan angle
(rad), D the mirror dimension perpendicular to the rotation axis, t the
thickness, rho the density, E Young's modulus; delta_max is the "deviation
from linearity" of the mirror cross-section at the scan extremes.

Model used here (an approximation, not Brosens' own derivation): a
rectangular mirror held along its rotation axis; each half (length a = D/2) is
a cantilever strip in cylindrical bending (flexural rigidity per unit width
E t^3 / (12 (1 - nu^2))) under the inertial load q(x) = rho t alpha x of the
peak angular acceleration alpha = (2 pi f)^2 theta_mech. The cantilever
deflection is w(x) = (q0 a^4 / EI) g(x/a), g(u) = u^2/6 - u^3/12 + u^5/120,
with q0 = rho t alpha a. The optically relevant distortion is the departure
from a straight line; two reference lines are evaluated:

* the chord through the axis and the mirror edges (Urey's figure draws
  delta_max this way, at about one third of the half-width from the axis);
* the least-squares line over the whole cross-section.

The script prints the resulting constant C in delta = C * rho f^2 D^5 theta /
(E t^2) for nu = 0 and for typical Poisson ratios, and evaluates the report's
worked example (silicon, 3 mm, 100 um, 1.5 kHz, 15 deg).
"""
import math

import numpy as np


def g(u):
    """Normalized cantilever deflection under a load rising linearly to the tip."""
    return u**2 / 6 - u**3 / 12 + u**5 / 120


def main():
    u = np.linspace(0.0, 1.0, 200001)
    w = g(u)
    # chord reference: straight line through the axis (u=0) and the edge (u=1)
    dev_chord = np.max(np.abs(w - g(1.0) * u))
    u_chord = u[np.argmax(np.abs(w - g(1.0) * u))]
    # least-squares line through the origin over the antisymmetric profile
    m = np.trapezoid(u * w, u) / np.trapezoid(u * u, u)
    dev_ls = np.max(np.abs(w - m * u))
    # convert: delta = dev * q0 a^4 / EI, q0 = rho t alpha a, EI = E t^3/(12(1-nu^2)),
    # a = D/2, alpha = 4 pi^2 f^2 theta  ->  C = dev * 12 * 4 pi^2 / 32 * (1 - nu^2)
    k = 12 * 4 * math.pi**2 / 32
    print(f"max deviation from chord at u = {u_chord:.3f} of the half-width; "
          f"dimensionless {dev_chord:.6f}; tip deflection {g(1.0):.6f}")
    print(f"least-squares-line deviation (dimensionless): {dev_ls:.6f}")
    print("Constant C in delta = C rho f^2 D^5 theta / (E t^2):")
    for nu in (0.0, 0.17, 0.20, 0.22, 0.25, 0.28, 0.30):
        print(f"  nu = {nu:.2f}: chord {dev_chord * k * (1 - nu**2):.4f};"
              f" least-squares line {dev_ls * k * (1 - nu**2):.4f}")
    # report's worked example with the published 0.217
    rho, E, f, D, t, th = 2330.0, 169e9, 1500.0, 3e-3, 100e-6, math.radians(15)
    d = 0.217 * rho * f**2 * D**5 * th / (E * t**2)
    print(f"Report example (0.217, Si, 3 mm, 100 um, 1.5 kHz, 15 deg): {d*1e9:.1f} nm;"
          f" 5 mm: {d*(5/3)**5*1e9:.0f} nm")
    # if the constant multiplied omega^2 instead of f^2 the result would be 4 pi^2 larger
    print(f"(If 0.217 multiplied omega^2 = (2 pi f)^2, the same case would be {d*4*math.pi**2*1e9:.0f} nm.)")


if __name__ == "__main__":
    main()
