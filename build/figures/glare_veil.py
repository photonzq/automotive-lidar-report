"""Veil from glare scattered by windshield dirt: how much it costs a camera and a lidar.

Companion to section E4.1 of automotive_perception_report_2026-09-27.md. Engineering estimates [E] built on measured
inputs. The script prints the numbers behind the section's tables and their checks, writes them to
glare_veil_tables.txt and draws glare_veil.png / .pdf (Figure E4.1).

Relations (section E4.1):
  veil luminance              L_v = E_perp * f(theta)            (Padmos and Alferdinck 1983, Eq. 7, report p. 10)
  contrast with the veil      C' = C * L_b / (L_b + L_v)
  veil from a bright surround L_v = sum_i Lbar_i * g_i,  g = integral of f over solid angle (their Eqs. 5-6)
  lidar background multiple   m = 1 + pi * f(theta) * E_perp / (rho_ref * E_ref);  range ratio m ** (-1/4)
  photon-limited image        signal-to-noise ratio of target against background falls by
                              sqrt(1 + 2 L_v / (L_b + L_t))
where
  f(theta)  scatter function of the glass (or the eye), veil luminance per unit illuminance on a plane perpendicular to
            the glare source, sr^-1 (cd m^-2 per lx); theta is the angle between glare source and viewing direction;
  E_perp    illuminance from the glare source on that plane (lx);
  L_b       luminance of the background the target is seen against (cd m^-2); C its contrast without the veil;
  rho_ref, E_ref  reflectance and illuminance of the scene a lidar's full-sun specification assumes (0.9, 100 klx).

Measured inputs [P]:
  windshields   Padmos and Alferdinck, TNO report IZF 1983 C-10: 25 cars in service, dry, as found: g(1,20) mean 0.035,
                85th percentile 0.057; g(20,50) 0.0058 / 0.0097; g(50,110) 0.0026 / 0.0045; f(40) 0.0019 / 0.0032
                (Table II, p. 30); nominal (85th-percentile) scatter function f = 6.6 theta^-1.73 for 1-9 deg and
                f = 44 theta^-2.6 for 9-110 deg (Eqs. 23a-b, p. 31); f = 115 g(1,20) theta^-1.73 for 1-9 deg (p. 31);
                new clean screen g(1,20) about 0.0010 (p. 33). Toet and Alferdinck, Proc. SPIE 8898, 88980I (2013):
                dirty screens follow the 44 theta^-2.6 model and scatter on average 14 times more than clean ones
                (p. 12); new clean fit f = 0.067 theta^-1.50, measured from 8 to 50 deg (Fig. 9, p. 13).
  eye           Stiles-Holladay f = 10 / theta^2 (the report's Eq. stiles-holladay-glare).
  daylight      Gillette, NBS BSS 152 (1983): E_DN = 127.5 klx * exp(-0.210 / sin h) (Eq. 3.11, p. 20; constants
                p. 23; annual-mean Earth-Sun distance). Kimball and Hand, Monthly Weather Review 50, 615 (1922):
                clear winter sky, skylight on a vertical surface facing away from the sun and on a horizontal
                surface, 257 and 683 foot-candles at 20 deg (Table 4, p. 618), about 170 and 375 foot-candles at 10 deg
                read by eye from Fig. 6 (p. 619).
  headlamps     FMVSS No. 108 Table XVIII (49 CFR 571.108, 10-1-25 edition, p. 479): upper beam UB1 minima 15,000 cd
                at H-3L and 5,000 cd at 1U-3L; maximum 75,000 cd at H-V (UB2, UB3).
  sun           angular diameter 1919 arcsec at 1 AU (NASA Sun fact sheet).
  sun position  Hagita and Mori, Asian Transport Studies 3, 205 (2014), Table 1, p. 212: in Chiba, 1,310.2 of the
                4,394.5 daylight hours a year have a solar zenith angle of 70-90 deg.
Assumptions [E]: road and ground reflectance 0.1; dark clothing 0.05 (as in section A6.1); an average windshield as
found is 0.6 times the 85th-percentile curve (Table II: 0.035/0.057 = 0.61, 0.0019/0.0032 = 0.59); a cleaned
windshield in service is 1/14 of it (Toet and Alferdinck); a halogen headlamp is a 3,200 K blackbody; the photometric
ratio of a low sun to full sun also holds in the lidar's band. The near-infrared correction is printed as a condition:
if clear air's extinction coefficient at 905 nm is 0.06 instead of the visible 0.210, a low sun is brighter at 905 nm,
relative to a sun overhead, by exp[(0.210 - 0.06)(1/sin h - 1)].
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogFormatterMathtext


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
STEM = "glare_veil"

# ---------------------------------------------------------------- style (house guide)
FONT_SIZE = 8.0
COLORS = {
    "primary": "#385C9E",
    "neutral": "#4D4D4D",
    "warm_accent": "#9E403D",
    "cool_accent": "#477A57",
    "purple_accent": "#6B5B95",
    "teal_accent": "#3F7F82",
    "brown_accent": "#7D5C46",
    "grey_accent": "#6F6F6F",
    "highlight": "#EED671",
    "annotation": "#767676",
    "text": "#272727",
    "axes": "#000000",
    "background": "#FFFFFF",
}
COLOR_CYCLE = [COLORS["primary"], COLORS["warm_accent"], COLORS["cool_accent"], COLORS["purple_accent"],
               COLORS["teal_accent"], COLORS["brown_accent"], COLORS["grey_accent"]]


def configure_plot_style() -> None:
    """Apply the project Matplotlib style without external LaTeX."""
    plt.rcParams.update(
        {
            "figure.facecolor": COLORS["background"],
            "axes.facecolor": COLORS["background"],
            "axes.edgecolor": COLORS["axes"],
            "axes.labelcolor": COLORS["text"],
            "text.color": COLORS["text"],
            "xtick.color": COLORS["axes"],
            "ytick.color": COLORS["axes"],
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"],
            "font.size": FONT_SIZE,
            "axes.labelsize": FONT_SIZE,
            "axes.titlesize": FONT_SIZE,
            "xtick.labelsize": FONT_SIZE,
            "ytick.labelsize": FONT_SIZE,
            "legend.fontsize": FONT_SIZE,
            "axes.linewidth": 0.8,
            "axes.prop_cycle": plt.cycler(color=COLOR_CYCLE),
            "axes.spines.top": True,
            "axes.spines.right": True,
            "xtick.top": True,
            "ytick.right": True,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "legend.frameon": False,
            "axes.grid": False,
            "text.usetex": False,
            "mathtext.fontset": "cm",
            "axes.formatter.use_mathtext": True,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
        }
    )


# ---------------------------------------------------------------- scatter functions f(theta), theta in degrees, sr^-1
AVG_FACTOR = 0.6       # average windshield as found, relative to the 85th-percentile curve (Table II)
CLEAN_DIVISOR = 14.0   # cleaned windshield in service (Toet and Alferdinck: dirty / clean = 14 on average)
G_NEW = 0.0010         # g(1,20) of a new, clean windshield (Padmos and Alferdinck, p. 33)


def f_dirty(theta):
    """85th-percentile windshield in service (Padmos and Alferdinck Eqs. 23a-b)."""
    t = np.asarray(theta, dtype=float)
    return np.where(t <= 9.0, 6.6 * t ** -1.73, 44.0 * t ** -2.6)


def f_average(theta):
    return AVG_FACTOR * f_dirty(theta)


def f_cleaned(theta):
    return f_dirty(theta) / CLEAN_DIVISOR


def f_new(theta):
    """New, clean windshield: 115 g(1,20) theta^-1.73 below 9 deg, Toet and Alferdinck's fit 0.067 theta^-1.5 above."""
    t = np.asarray(theta, dtype=float)
    return np.where(t <= 9.0, 115.0 * G_NEW * t ** -1.73, 0.067 * t ** -1.5)


def f_eye(theta):
    """Stiles-Holladay disability glare of the eye."""
    return 10.0 / np.asarray(theta, dtype=float) ** 2


GLASS = [
    ("New, clean windshield", "new, clean", f_new),
    ("Cleaned windshield in service", "cleaned in service", f_cleaned),
    ("Average windshield as found", "average as found", f_average),
    ("Dirty windshield (85th percentile)", "dirty", f_dirty),
]


def crossing(func, level: float, lo: float = 0.05, hi: float = 110.0) -> float:
    """Angle where a decreasing scatter function falls to `level` (bisection on log angle)."""
    a, b = np.log(lo), np.log(hi)
    if func(np.exp(a)) < level:
        return float("nan")
    if func(np.exp(b)) > level:
        return float("inf")
    for _ in range(200):
        m = 0.5 * (a + b)
        if func(np.exp(m)) > level:
            a = m
        else:
            b = m
    return float(np.exp(0.5 * (a + b)))


# ---------------------------------------------------------------- daylight [P] and scene [E]
FC = 10.7639             # lux per foot-candle
RHO_ROAD = 0.1           # road and ground reflectance
RHO_DARK = 0.05          # dark clothing (section A6.1)


def e_direct_normal(h_deg: float) -> float:
    """Clear-sky direct normal illuminance (lx), Gillette Eq. 3.11 with the annual-mean Earth-Sun distance."""
    return 127.5e3 * np.exp(-0.210 / np.sin(np.radians(h_deg)))


SKY = {  # solar altitude: (skylight on a vertical face turned away from the sun, skylight on the horizontal) in fc
    10.0: (170.0, 375.0),   # Kimball and Hand Fig. 6, read by eye
    20.0: (257.0, 683.0),   # Kimball and Hand Table 4, clear sky, winter
}


def low_sun(h_deg: float) -> dict:
    e_dn = e_direct_normal(h_deg)
    sky_v, sky_h = SKY[h_deg][0] * FC, SKY[h_deg][1] * FC
    e_h = e_dn * np.sin(np.radians(h_deg)) + sky_h                 # horizontal: sun plus sky
    e_shade = sky_v + 0.5 * RHO_ROAD * e_h                          # vertical face away from the sun: sky plus ground
    l_b = RHO_ROAD * e_h / np.pi                                    # road behind the target
    l_t = RHO_DARK * e_shade / np.pi                                # dark clothing, shaded side
    return dict(h=h_deg, e_dn=e_dn, sky_v=sky_v, sky_h=sky_h, e_h=e_h, e_shade=e_shade, k=e_shade / e_dn,
                l_b=l_b, l_t=l_t, c0=(l_t - l_b) / l_b, f_half=l_b / e_dn, f_target=l_t / e_dn)


SUN10, SUN20 = low_sun(10.0), low_sun(20.0)


def horizon_half_width(d_deg: float, h_deg: float) -> float:
    """Azimuth half-width (deg) over which a cone of angular radius d around a sun at altitude h covers the horizon
    (spherical law of cosines: cos d = cos h cos(azimuth difference) on the horizon)."""
    if not d_deg > h_deg:
        return float("nan")
    return float(np.degrees(np.arccos(np.cos(np.radians(d_deg)) / np.cos(np.radians(h_deg)))))


TAU_VIS = 0.210   # Gillette's extinction coefficient for visible light
TAU_NIR = 0.06    # a condition, not a measurement: clear air at 905 nm (Rayleigh scattering alone gives about 0.013)


def nir_factor(h_deg: float) -> float:
    """How much brighter a sun at altitude h is at 905 nm than photometry says, both relative to a sun overhead."""
    return float(np.exp((TAU_VIS - TAU_NIR) * (1.0 / np.sin(np.radians(h_deg)) - 1.0)))

# ---------------------------------------------------------------- oncoming high beams at night (section A6.1 geometry)
D_ONCOMING = 50.0                     # m
THETA_NIGHT = np.degrees(np.arctan(3.0 / 50.0))
E_HIGH = (2 * 5000.0 / D_ONCOMING ** 2, 2 * 15000.0 / D_ONCOMING ** 2)   # lx, two lamps at the FMVSS minima
E_LOW = 2 * 350.0 / D_ONCOMING ** 2                                        # lx, section A6.1 (two low beams)
E_PED = 5.0                                                                # lx on the pedestrian, low-beam hotspot
L_PED = RHO_DARK * E_PED / np.pi
L_ROAD_NIGHT = RHO_ROAD * E_PED / np.pi

# ---------------------------------------------------------------- lidar
RHO_REF, E_REF = 0.9, 100e3           # full-sun specification scene (section C0 subsection 4.2, high case)
X0_HIGH = 2 * 0.122                   # SPAD count rate x dead time for that scene (section C0 subsection 4.2)
SUN_DIAMETER = 1919.0 / 3600.0        # deg
PIXEL = 0.05                          # deg, macro-pixel of section C0 subsection 4.2
E_SUN_940 = 0.39                      # W m^-2 nm^-1, full sun at 940 nm (section C6(d))
B_NIGHT = 0.01                        # counts per bin, night case of section C0 subsection 4.3
B_HIGH = 3.66e8 * 1e-9 * 10 * np.exp(-X0_HIGH)   # counts per bin of the full-sun high case


def lidar_level(e_perp: float) -> float:
    """Scatter function at which the veil equals the full-sun specification scene."""
    return RHO_REF * E_REF / (np.pi * e_perp)


def lidar_range_ratio(theta: float, func, e_perp: float, with_scene: bool, dead_time: bool) -> float:
    """Range relative to the full-sun specification near the sun, background-limited (m^-1/4), optionally with the
    live fraction of a paralyzable SPAD (section C5b): (l(m) / (l(1) m))^(1/4)."""
    rv = np.pi * float(func(theta)) * e_perp / (RHO_REF * E_REF)
    m = rv + (1.0 if with_scene else 0.0)
    live = np.exp(-m * X0_HIGH) / np.exp(-X0_HIGH) if dead_time else 1.0
    return float((live / m) ** 0.25)


def ybar(lam_nm):
    """CIE 1931 y-bar (photopic V), multi-lobe fit of Wyman, Sloan and Shirley (2013)."""
    lam = np.asarray(lam_nm, dtype=float)

    def lobe(mu, s1, s2):
        s = np.where(lam < mu, s1, s2)
        return np.exp(-0.5 * ((lam - mu) / s) ** 2)

    return 0.821 * lobe(568.8, 46.9, 40.5) + 0.286 * lobe(530.9, 16.3, 31.1)


def blackbody_per_lux(lam_target_nm: float, temp_k: float) -> float:
    """Spectral irradiance at lam_target (W m^-2 nm^-1) per lux of a blackbody source of temperature temp_k."""
    c2 = 1.438777e-2
    lam = np.arange(360.0, 831.0, 0.5)
    shape = (lam * 1e-9) ** -5 / np.expm1(c2 / (lam * 1e-9 * temp_k))
    lux_per_unit = 683.0 * np.trapezoid(ybar(lam) * shape, lam)
    target = (lam_target_nm * 1e-9) ** -5 / np.expm1(c2 / (lam_target_nm * 1e-9 * temp_k))
    return float(target / lux_per_unit)


# window attenuation: light scattered beyond 1 deg, both passes (Table II sums)
G_AVG = 0.035 + 0.0058 + 0.0026
G_85 = 0.057 + 0.0097 + 0.0045
Z_R, R0 = 257.0, 200.0    # FMCW 25 mm design of section C0 subsection 5.4
ALPHA_1550 = 0.044        # /km, clear-air extinction at 1,550 nm (section C0 subsection 3.3)


def loss_db(g: float) -> float:
    return -20.0 * np.log10(1.0 - g)


def coherent_loss_db(r_m: float) -> float:
    """Collimated-beam link loss relative to the near field, with two-way clear-air loss (section C0)."""
    return 10.0 * np.log10(1.0 + (r_m / Z_R) ** 2) + 8.686 * ALPHA_1550 * r_m / 1000.0


def fmcw_range(x_db: float) -> float:
    """Range of the 25 mm FMCW design (sized to reach R0 in clear air) with an extra fixed loss x_db."""
    budget = coherent_loss_db(R0) - x_db
    if budget <= 0.0:
        return 0.0
    lo, hi = 0.0, R0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if coherent_loss_db(mid) <= budget else (lo, mid)
    return 0.5 * (lo + hi)


def poisson_tail(n: int, mean: float) -> float:
    """P(N >= n) for a Poisson count of the given mean."""
    k = np.arange(n)
    from math import factorial
    return float(1.0 - np.exp(-mean) * sum(mean ** int(i) / factorial(int(i)) for i in k))


P_FALSE = 1e-3 / 2450.0   # per-bin false-alarm limit of section C0 subsection 4.3


def night_threshold(b: float) -> int:
    n = 1
    while poisson_tail(n, b) > P_FALSE:
        n += 1
    return n


def signal_for_pd(n_th: int, b: float, pd: float = 0.9) -> float:
    lo, hi = 0.0, 50.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if poisson_tail(n_th, mid + b) < pd else (lo, mid)
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- tables
def table_lines() -> list[str]:
    out = []
    for s in (SUN10, SUN20):
        out.append(f"Low sun at {s['h']:.0f} deg: E_DN {s['e_dn']:.0f} lx; sky on the shaded face {s['sky_v']:.0f} lx; "
                   f"sky on the horizontal {s['sky_h']:.0f} lx; horizontal total {s['e_h']:.0f} lx; shaded face "
                   f"{s['e_shade']:.0f} lx (k = {s['k']:.3f}); road L_b {s['l_b']:.1f} cd/m2; dark clothing L_t "
                   f"{s['l_t']:.1f} cd/m2; contrast {s['c0']:.3f}; f at which the veil halves the contrast "
                   f"{s['f_half']:.5f}; f at which it equals the target {s['f_target']:.6f}; lidar level "
                   f"{lidar_level(s['e_dn']):.3f}")
    out.append("")
    out.append(f"{'Glass':38s} {'half@10':>8s} {'kept@10':>8s} {'half@20':>8s} {'kept@20':>8s} {'=tgt@10':>8s} "
               f"{'lidar@10':>9s} {'lidar@20':>9s}")
    rows = GLASS + [("Driver's eye (Stiles-Holladay)", "eye", f_eye)]
    for label, _, func in rows:
        kept10 = SUN10["l_b"] / (SUN10["l_b"] + SUN10["e_dn"] * float(func(10.0)))
        kept20 = SUN20["l_b"] / (SUN20["l_b"] + SUN20["e_dn"] * float(func(20.0)))
        lid10 = crossing(func, lidar_level(SUN10["e_dn"])) if func is not f_eye else float("nan")
        lid20 = crossing(func, lidar_level(SUN20["e_dn"])) if func is not f_eye else float("nan")
        out.append(f"{label:38s} {crossing(func, SUN10['f_half']):8.1f} {kept10:8.3f} "
                   f"{crossing(func, SUN20['f_half']):8.1f} {kept20:8.3f} {crossing(func, SUN10['f_target']):8.1f} "
                   f"{lid10:9.1f} {lid20:9.1f}")
    out.append("")
    out.append("Directly below the sun (theta = h): veil L_v (cd/m2) and L_v / (L_b - L_t); half-contrast zone across the "
               "horizon (+- deg of azimuth from the sun's); lidar background of the veil alone / full-sun scene")
    for s in (SUN10, SUN20):
        for label, _, func in rows:
            fv = float(func(s["h"]))
            lv = s["e_dn"] * fv
            hw = horizon_half_width(crossing(func, s["f_half"]), s["h"])
            lid = (f"; lidar {np.pi * fv * s['e_dn'] / (RHO_REF * E_REF):.4f}" if func is not f_eye else "")
            out.append(f"  sun {s['h']:.0f} deg, {label:36s} L_v {lv:6.0f}; / (L_b - L_t) {lv / (s['l_b'] - s['l_t']):5.2f}; "
                       f"across the horizon +-{hw:.1f}{lid}")
    out.append("")
    out.append(f"Night: two oncoming high beams at {D_ONCOMING:.0f} m, {THETA_NIGHT:.2f} deg off axis: "
               f"{E_HIGH[0]:.1f}-{E_HIGH[1]:.1f} lx (two low beams {E_LOW:.2f} lx, ratio "
               f"{E_HIGH[0] / E_LOW:.0f}-{E_HIGH[1] / E_LOW:.0f}); dark pedestrian at {E_PED:.0f} lx "
               f"{L_PED:.4f} cd/m2, road {L_ROAD_NIGHT:.4f} cd/m2")
    for label, _, func in rows:
        fv = float(func(THETA_NIGHT))
        lv = (E_HIGH[0] * fv, E_HIGH[1] * fv)
        kept = tuple(L_ROAD_NIGHT / (L_ROAD_NIGHT + x) for x in lv)
        snr = tuple(np.sqrt(1.0 + 2.0 * x / (L_ROAD_NIGHT + L_PED)) for x in lv)
        out.append(f"  {label:36s} f {fv:.4f}; veil {lv[0]:.3f}-{lv[1]:.3f} cd/m2; veil / pedestrian "
                   f"{lv[0] / L_PED:.1f}-{lv[1] / L_PED:.1f}; road contrast kept {kept[0]:.3f}-{kept[1]:.3f}; "
                   f"photon-limited SNR / {snr[0]:.2f}-{snr[1]:.2f}")
    out.append("")
    out.append("Lidar near a sun 10 deg high, dirty window (85th percentile), range / full-sun specification:")
    for th in (1.0, 2.0):
        r = [lidar_range_ratio(th, f_dirty, SUN10["e_dn"], ws, dt) for ws in (False, True) for dt in (False, True)]
        rv = np.pi * float(f_dirty(th)) * SUN10["e_dn"] / (RHO_REF * E_REF)
        out.append(f"  {th:.0f} deg: veil / full-sun scene {rv:.2f}; range {r[0]:.3f} (veil only) to {r[2]:.3f} "
                   f"(with a full-sun scene); with dead time {r[1]:.3f} to {r[3]:.3f}")
    n_disc = np.pi / 4 * (SUN_DIAMETER / PIXEL) ** 2
    out.append(f"  sun's disc {SUN_DIAMETER:.3f} deg covers {n_disc:.0f} pixels of {PIXEL} deg")
    nf = nir_factor(10.0)
    zones = "; ".join(f"{short} {crossing(func, lidar_level(SUN10['e_dn']) / nf):.1f} deg" for _, short, func in GLASS)
    below = "; ".join(f"{short} {nf * np.pi * float(func(10.0)) * SUN10['e_dn'] / (RHO_REF * E_REF):.3f}"
                      for _, short, func in GLASS)
    out.append(f"905 nm, if clear air's extinction coefficient is {TAU_NIR} (visible {TAU_VIS}): a sun 10 deg high is "
               f"x{nf:.2f} brighter, relative to a sun overhead, than photometry says (angles x{nf ** (1 / 1.73):.2f} "
               f"below 9 deg); lidar zone {zones}; road-level pixel below the sun {below}")
    per_lux = blackbody_per_lux(940.0, 3200.0)
    out.append(f"Halogen (3,200 K) at 940 nm: {per_lux:.3e} W m^-2 nm^-1 per lx")
    n0 = night_threshold(B_NIGHT)
    s0 = signal_for_pd(n0, B_NIGHT)
    out.append(f"  night case: b {B_NIGHT}, threshold {n0} counts, signal for P_D = 0.9: {s0:.2f}")
    for label, _, func in (GLASS[2], GLASS[3]):
        lv940 = np.array(E_HIGH) * per_lux * float(func(THETA_NIGHT))
        ratio = lv940 / (RHO_REF * E_SUN_940 / np.pi)
        b_add = ratio * B_HIGH
        n1 = night_threshold(B_NIGHT + b_add[1])
        s1 = signal_for_pd(n1, B_NIGHT + b_add[1])
        out.append(f"  {label:36s} veil / full-sun scene at 940 nm {ratio[0]:.2e}-{ratio[1]:.2e}; counts per bin "
                   f"{b_add[0]:.1e}-{b_add[1]:.1e} (night case {B_NIGHT}); at the upper end threshold {n1}, "
                   f"signal {s1:.2f}, night range x{np.sqrt(s0 / s1):.3f}")
    out.append("")
    for label, g in (("average as found", G_AVG), ("dirty (85th percentile)", G_85)):
        x = loss_db(g)
        out.append(f"Window {label}: scattered beyond 1 deg {g:.4f} per pass; two-way loss {x:.3f} dB; ToF range "
                   f"x{10 ** (-x / 20):.3f}; FMCW 25 mm {fmcw_range(x):.1f} m of {R0:.0f} m (x{fmcw_range(x) / R0:.3f})")
    frac = 1310.2 / 4394.5
    out.append(f"Sun 0-20 deg high: {frac:.3f} of daylight hours (Chiba); within +-25 deg of a random heading: "
               f"{frac * 50 / 360:.3f} of daylight driving")
    return out


# ---------------------------------------------------------------- checks of hand-quoted values
def check(name: str, value: float, reference: float, tol: float) -> str:
    err = value - reference
    verdict = "pass" if abs(err) <= tol else "FAIL"
    return (f"{name}: value {value:.6g}, reference {reference:.6g}, error {err:+.3g}, "
            f"tolerance {tol:.3g} -> {verdict}")


def checks() -> list[str]:
    s10, s20 = SUN10, SUN20
    eye_low_beam = E_LOW * float(f_eye(THETA_NIGHT))
    return [
        check("E_DN at 10 deg (lx)", s10["e_dn"], 38.0e3, 0.1e3),
        check("E_DN at 20 deg (lx)", s20["e_dn"], 69.0e3, 0.1e3),
        check("road luminance, sun 10 deg (cd/m2)", s10["l_b"], 339.0, 1.0),
        check("dark clothing, sun 10 deg (cd/m2)", s10["l_t"], 37.6, 0.2),
        check("shaded-face ratio k, sun 10 deg", s10["k"], 0.062, 0.001),
        check("road luminance, sun 20 deg (cd/m2)", s20["l_b"], 985.0, 2.0),
        check("dark clothing, sun 20 deg (cd/m2)", s20["l_t"], 68.8, 0.2),
        check("half-contrast level, sun 10 deg (sr^-1)", s10["f_half"], 0.00895, 0.00005),
        check("dirty windshield f(10 deg)", float(f_dirty(10.0)), 0.1105, 0.0002),
        check("dirty windshield f(40 deg) vs Table II 85th percentile 0.0032", float(f_dirty(40.0)), 0.0030, 0.0001),
        check("new clean, both models meet at 9 deg", float(115 * G_NEW * 9 ** -1.73), float(0.067 * 9 ** -1.5),
              0.0001),
        check("contrast halved within, average as found, sun 10 deg", crossing(f_average, s10["f_half"]), 21.6, 0.1),
        check("contrast halved within, dirty, sun 10 deg", crossing(f_dirty, s10["f_half"]), 26.3, 0.1),
        check("lidar level, sun 10 deg (sr^-1)", lidar_level(s10["e_dn"]), 0.754, 0.002),
        check("lidar zone, dirty, sun 10 deg", crossing(f_dirty, lidar_level(s10["e_dn"])), 3.50, 0.02),
        check("eye veil from two low beams (section A6.1: 0.24 cd/m2)", eye_low_beam, 0.24, 0.005),
        check("glare angle of section A6.1 (deg)", THETA_NIGHT, 3.43, 0.01),
        check("two-way loss, average window (dB)", loss_db(G_AVG), 0.385, 0.002),
        check("FMCW 25 mm range with 0.2 mm water film (section C0 5.4: 61 m)", fmcw_range(1.88), 61.0, 1.5),
        check("FMCW 25 mm blind beyond (section C0 5.4: 2.1 dB)", coherent_loss_db(R0), 2.1, 0.05),
        check("night threshold of section C0 4.3 (3 counts at b = 0.01)", night_threshold(B_NIGHT), 3, 0),
        check("night signal for P_D = 0.9 (section C0 4.3 table: 5.3)", signal_for_pd(3, B_NIGHT), 5.3, 0.05),
        check("daylight share of a sun 0-20 deg high (Chiba)", 1310.2 / 4394.5, 0.298, 0.001),
    ]


# ---------------------------------------------------------------- figure
def draw() -> plt.Figure:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(4.2, 3.24), constrained_layout=True)
    th = np.logspace(0.0, 2.0, 400)
    styles = [
        (f_new, COLORS["primary"], (0, (5, 2))),
        (f_cleaned, COLORS["primary"], "-"),
        (f_average, COLORS["warm_accent"], (0, (5, 2))),
        (f_dirty, COLORS["warm_accent"], "-"),
    ]
    for (label, _, _), (func, color, ls) in zip(GLASS, styles):
        t = th[th <= 50.0] if func is f_new else th
        ax.plot(t, func(t), color=color, linestyle=ls, linewidth=1.5, label=label)
    ax.plot(th, f_eye(th), color=COLORS["neutral"], linestyle=(0, (1, 1.5)), linewidth=1.5,
            label="Driver's eye (Stiles–Holladay)")
    half, lid = SUN10["f_half"], lidar_level(SUN10["e_dn"])
    ax.axhline(lid, color=COLORS["purple_accent"], linewidth=0.8, zorder=0)
    ax.text(92.0, lid * 1.35, "Lidar: veil equals a sunlit white scene", color=COLORS["purple_accent"],
            ha="right", va="bottom", fontsize=FONT_SIZE)
    # the camera's label sits in the empty band above its line, right of the curves, with an arrow down to the line
    ax.axhline(half, color=COLORS["cool_accent"], linewidth=0.8, zorder=0)
    ax.text(92.0, 0.036, "Camera: veil halves\nthe road's contrast", color=COLORS["cool_accent"], ha="right",
            va="bottom", fontsize=FONT_SIZE, linespacing=1.1)
    ax.annotate("", xy=(72.0, half * 1.08), xytext=(72.0, 0.033),
                arrowprops=dict(arrowstyle="->", color=COLORS["cool_accent"], linewidth=0.8))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1.0, 100.0)
    ax.set_ylim(1e-5, 30.0)
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlabel(r"Angle from the glare source, $\theta$ (degrees)")
    ax.set_ylabel(r"Veil per lux of glare, $f(\theta)$ (sr$^{-1}$)")
    ax.legend(loc="lower left", handlelength=2.6)
    return fig


def main() -> None:
    header = [
        "Veil from glare scattered by windshield dirt (section E4.1, Figure E4.1) [E]",
        "L_v = E_perp f(theta); contrast kept L_b / (L_b + L_v); lidar background multiple 1 + pi f E_perp / (0.9 x 100 klx)",
        "",
    ]
    text = "\n".join(header + table_lines() + ["", "Checks (value, reference, error, tolerance):"] + checks()) + "\n"
    print(text)
    (OUT_DIR / f"{STEM}_tables.txt").write_bytes(text.encode("utf-8"))  # LF line endings on every platform
    fig = draw()
    fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
    fig.savefig(OUT_DIR / f"{STEM}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
