"""Numbers of the slowdown paragraph of §C4c subsection 1a: at 1,550 nm a slower scan delivers the same energy per
0.35 s window as long as each window holds a pass, and a single pass reaches the limit only near standstill.

Relations (symbols as in the report):
- energy per pass through the aperture, an upper bound: E_pass = eta * P * (D_a + d_b) / (omega * R), where eta is
  the fraction of the beam power inside the aperture when the beam is centred on it;
- a 0.35 s window holds about 0.35 s * omega / (2 pi) passes, at least one while omega >= 2 pi / 0.35 s;
- the energy per window is then 0.35 s * eta * P * (D_a + d_b) / (2 pi R), whatever the speed;
- below that speed a window holds one pass, which reaches the limit of 10^4 J/m^2 over a 1 mm aperture (7.85 mJ,
  exposures up to 0.35 s) at omega_trip = eta * P * (D_a + d_b) / (R * 7.85 mJ).
Inputs: the 0.64 W of Luminar's patent example; a Gaussian beam 3 mm across (1/e^2 diameter), of which
eta = 1 - exp(-2 (0.5 mm / 1.5 mm)^2) = 0.20 enters the 1 mm aperture, so D_a + d_b = 4 mm; the whole-beam case
eta = 1 with D_a + d_b = 2 mm; R = 100 mm; a 10 Hz head, omega = 62.8 rad/s. The text substitutes eta = 0.20, and so
do the checks.

Usage: slowdown_check.py   (prints each value with its reference, error, tolerance and verdict)
"""
import math

E_LIM = 1e4 * math.pi * (0.5e-3) ** 2  # J: 10^4 J/m^2 over a 1 mm aperture, exposures up to 0.35 s
T_WIN = 0.35                           # s
R = 0.100                              # m
OMEGA_FULL = 2 * math.pi * 10.0        # rad/s, a 10 Hz head
P = 0.64                               # W, Luminar's patent example
ETA_3MM = 0.20                         # as substituted in the text
SPAN_3MM = 4e-3                        # m, D_a + d_b for a 3 mm beam and the 1 mm aperture
SPAN_WHOLE = 2e-3                      # m, D_a + d_b with the whole beam (at most 1 mm) in the aperture


def window_energy(eta: float, span: float) -> float:
    return T_WIN * eta * P * span / (2 * math.pi * R)


def omega_trip(eta: float, span: float) -> float:
    return eta * P * span / (R * E_LIM)


def check(name: str, value: float, reference: float, tol: float) -> str:
    err = value - reference
    verdict = "pass" if abs(err) <= tol else "FAIL"
    return (f"{name}: value {value:.6g}, reference {reference:.6g}, error {err:+.3g}, "
            f"tolerance {tol:.3g} -> {verdict}")


def checks() -> list[str]:
    omega_one = 2 * math.pi / T_WIN
    return [
        check("limit through 1 mm (mJ; 7.85)", E_LIM * 1e3, 7.85, 0.005),
        check("eta of a 3 mm beam in 1 mm, unrounded (0.20)", 1 - math.exp(-2 * (0.5 / 1.5) ** 2), 0.20, 0.005),
        check("speed for one pass per window (rad/s; 18)", omega_one, 18, 0.1),
        check("that speed as a share of 62.8 rad/s (%; 29)", 100 * omega_one / OMEGA_FULL, 29, 0.5),
        check("omega_trip, 3 mm beam (rad/s; 0.65)", omega_trip(ETA_3MM, SPAN_3MM), 0.65, 0.005),
        check("as a share of full speed (%; 1.0)", 100 * omega_trip(ETA_3MM, SPAN_3MM) / OMEGA_FULL, 1.0, 0.05),
        check("omega_trip, whole beam (rad/s; 1.6)", omega_trip(1.0, SPAN_WHOLE), 1.6, 0.05),
        check("as a share of full speed (%; 2.6)", 100 * omega_trip(1.0, SPAN_WHOLE) / OMEGA_FULL, 2.6, 0.05),
        check("window energy at full speed, 3 mm beam (mJ; 0.29)", window_energy(ETA_3MM, SPAN_3MM) * 1e3, 0.29, 0.005),
        check("margin, 3 mm beam (times; 27)", E_LIM / window_energy(ETA_3MM, SPAN_3MM), 27, 0.6),
        check("window energy at full speed, whole beam (mJ; 0.71)", window_energy(1.0, SPAN_WHOLE) * 1e3, 0.71, 0.005),
        check("margin, whole beam (times; 11)", E_LIM / window_energy(1.0, SPAN_WHOLE), 11, 0.5),
        check("pass energy at omega_trip equals the limit (mJ; 7.85)",
              ETA_3MM * P * SPAN_3MM / (omega_trip(ETA_3MM, SPAN_3MM) * R) * 1e3, 7.85, 0.005),
    ]


if __name__ == "__main__":
    for line in checks():
        print(line)
