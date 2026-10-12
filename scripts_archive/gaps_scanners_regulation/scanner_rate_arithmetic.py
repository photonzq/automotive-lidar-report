"""Scanner-rate arithmetic for Seyond Falcon, InnovizOne and RoboSense M1.

All results are engineering estimates built from published inputs:

Seyond Falcon K1
  * 1,520 "vertical scanning lines" per second at 10 frames/s (Falcon K1
    user manual V2.1.2, specification table).
  * four beams from a fibre source split one-to-four, and a five-facet
    ("pentagon") polygon, per a hands-on teardown (Tencent News / 智驾最前沿,
    29 Nov 2022, "万字与你拆解5款车载激光雷达").
  * 120 deg horizontal field (manual).
  Each facet sweep writes one line per beam, so
      rev/s = lines_per_s / (beams * facets).
  A mirror turning by phi deflects the reflected beam by 2*phi, so one facet
  of an N-facet polygon can sweep at most 2*360/N deg (optical); the usable
  fraction is field / (720/N). Walk-off is 2*R*Omega/c (report Eq. (71)).

InnovizOne
  * four lasers and four silicon detectors for 256 lines (CEO remarks in the
    SEC Form 425 transcript of 17 Mar 2021); 256 lines at 10 frames/s or 160
    at 15 (datasheet); 2.8 M native points/s; 250 m maximum range.
  Sweeps/s = lines * frame_rate / beams (report Eq. (69)); a bidirectional
  resonant axis needs f = S/2. Per-laser pulse rate is compared with the
  unambiguous-range limit c/(2 R_max) (report Eq. (70)).

RoboSense M1
  * five transceiver modules with one laser each (same teardown); 125 lines
  at 15 frames/s; the MEMS supplier's quoted fast-axis band 1.2-1.3 kHz.
"""
C = 2.998e8  # speed of light, m/s


def falcon(lines_per_s=1520.0, beams=4, facets=5, field_deg=120.0, frame_hz=10.0):
    """Polygon speed, optical angular speed, duty and walk-off for the Falcon."""
    rev_s = lines_per_s / (beams * facets)
    omega_opt = 2 * 360.0 * rev_s                      # deg/s, reflection doubles
    max_sweep = 2 * 360.0 / facets                     # deg per facet (optical)
    duty = field_deg / max_sweep
    print(f"Falcon: {rev_s:.1f} rev/s = {rev_s*60:.0f} rpm; optical speed {omega_opt:,.0f} deg/s;"
          f" max optical sweep per facet {max_sweep:.0f} deg -> duty {duty:.2f} for {field_deg:.0f} deg")
    print(f"        lines per frame {lines_per_s/frame_hz:.0f}; facet period {1e3/(rev_s*facets):.2f} ms;"
          f" galvo sweep rate = frame rate {frame_hz:.0f} Hz (assumed one vertical sweep per frame)")
    for r in (200.0, 250.0):
        print(f"        walk-off at {r:.0f} m: {2*r*omega_opt/C:.3f} deg")
    for n in (4, 6):
        print(f"        (for comparison, {n} facets: {lines_per_s/(beams*n)*60:.0f} rpm,"
              f" max sweep {720/n:.0f} deg)")


def innoviz_one(beams=4, pts=2.8e6, r_max=250.0):
    """Sweep rate and per-laser pulse rate for InnovizOne with four lasers."""
    for lines, fr in ((256, 10), (160, 15)):
        s = lines * fr / beams
        print(f"InnovizOne {lines} lines @ {fr} Hz, {beams} beams: S = {s:.0f} sweeps/s,"
              f" resonant f = S/2 = {s/2:.0f} Hz")
    per_laser = pts / beams
    limit = C / (2 * r_max)
    print(f"           {pts/1e6:.1f} M pts/s / {beams} = {per_laser/1e3:.0f} kHz per laser vs"
          f" {limit/1e3:.0f} kHz unambiguous limit at {r_max:.0f} m"
          f" -> {'more than one point per pulse needed' if per_laser > limit else 'within limit'}")


def robosense_m1(lines=125, fr=15.0, f_fast=(1.2e3, 1.3e3)):
    """Sweep rate of the M1 with one beam per module, against the quoted fast-axis band."""
    s = lines * fr
    print(f"RoboSense M1: S = {s:.0f} sweeps/s -> f = {s/2:.0f} Hz needed (one beam per module)")
    for f in f_fast:
        print(f"           at {f/1e3:.2f} kHz the mirror makes {2*f/fr:.0f} sweeps per frame;"
              f" {lines} lines use {lines/(2*f/fr):.0%} of them")


if __name__ == "__main__":
    falcon()
    innoviz_one()
    robosense_m1()
