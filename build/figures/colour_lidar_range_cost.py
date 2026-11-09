"""Range cost of colour channels on a SPAD lidar chip.

Companion to section C5b of automotive_perception_report_2026-09-27.md. Engineering estimates [E]. The script prints
the numbers behind the section's range-cost table and their checks, writes them to colour_lidar_range_cost_tables.txt
and draws colour_lidar_range_cost.png / .pdf (Figure C5b.1).

Relations (section C5b), which apply the background-limited and signal-limited laws of section C0, subsection 5.2:
  range factor in full sun     R / R0 = (a / m) ** (1/4)
  range factor at night        R / R0 = a ** (1/2)
  background multiplier        m = 1 + kappa * (dl_c / dl_L) * (pde_c / pde_L) * (rho_c / rho_L)
  dead time (paralyzable)      live fraction l = exp(-m * x0), l0 = exp(-x0); full-sun factor (a * l / (m * l0)) ** (1/4)
where
  a       share of the ranging channel's collected echo light that still reaches ranging SPADs (it removes signal and
          in-band background alike: area given to colour pixels, an added absorbing layer);
  m       rise in the background that the ranging SPADs count per unit of a, from light outside the laser band;
  dl_c    width of the colour band that also reaches the ranging SPAD (nm); dl_L the pass band at the laser line (nm);
  pde_c   SPAD photon detection efficiency in the colour band; pde_L at the laser line;
  rho_c   scene reflectance in the colour band; rho_L at the laser line;
  kappa   solar photon flux per nm in the colour band over that at the laser line;
  x0      colour-free background count rate per SPAD times the dead time.

Inputs [E]: a 100 nm colour band (one of red, green or blue) beside a 20 nm laser filter; pde_c / pde_L of 1-2;
rho_c / rho_L of 0.3-1; kappa = 1 (a 5,800 K blackbody gives 1.13 between 550 and 865 nm; Rayleigh scattering, which
removes more green than near infrared, brings the ground value close to 1); x0 = 0.122, the value of section C0,
subsection 4.2 (2.03 x 10^7 counts/s per SPAD and a 6 ns dead time). Datasheet values are from Ouster's OS1 Rev8
datasheet v4.0 (pp. 1-3) and OS1 Rev7 datasheet v3.1 (pp. 1-2) [P].
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


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
STEM = "colour_lidar_range_cost"

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


# ---------------------------------------------------------------- inputs [E]
DL_C = 100.0   # nm, one colour band
DL_L = 20.0    # nm, pass band at the laser line
KAPPA = 1.0    # solar photon flux per nm, colour band over laser line
X0 = 0.122     # section C0 subsection 4.2: 2.03e7 counts/s per SPAD x 6 ns dead time


def range_factor_sun(a: float, m: float, live_ratio: float = 1.0) -> float:
    """Full-sun (background-limited) range relative to the receiver without colour."""
    return (a * live_ratio / m) ** 0.25


def range_factor_night(a: float) -> float:
    """Night (signal-limited) range relative to the receiver without colour."""
    return a ** 0.5


def background_multiplier(pde_ratio: float, rho_ratio: float, kappa: float = KAPPA) -> float:
    """m when one SPAD ranges through a dual-band filter (colour band plus laser line)."""
    return 1.0 + kappa * (DL_C / DL_L) * pde_ratio * rho_ratio


def live_fraction(m: float, x0: float = X0) -> float:
    """Live fraction of a paralyzable SPAD whose colour-free load x0 is raised m-fold."""
    return float(np.exp(-m * x0))


def planck_photon_ratio(lam1_nm: float, lam2_nm: float, temp_k: float = 5800.0) -> float:
    """Blackbody photon flux per nm at lam1 over that at lam2 (proportional to lam^-4 / (exp(c2 / lam T) - 1))."""
    c2 = 1.438777e-2  # m K, second radiation constant

    def per_nm(lam_nm: float) -> float:
        lam = lam_nm * 1e-9
        return lam ** -4 / np.expm1(c2 / (lam * temp_k))

    return float(per_nm(lam1_nm) / per_nm(lam2_nm))


M_LOW = background_multiplier(1.0, 0.3)          # 2.5
M_MID = background_multiplier(1.5, 2.0 / 3.0)    # 6.0
M_HIGH = background_multiplier(2.0, 1.0)         # 11
LIVE_MID = live_fraction(M_MID) / live_fraction(1.0)

# label in the figure, label in the table, a, m, live-fraction ratio
CASES = [
    ("Separate channels", "Separate ranging and colour channels, each with its own filter", 1.0, 1.0, 1.0),
    ("Added layer passing 90%", "An added layer passing 90% at the laser line", 0.9, 1.0, 1.0),
    ("Hybrid pixel, $a$ = 0.75", "Hybrid pixel, a quarter of the ranging area given to colour", 0.75, 1.0, 1.0),
    ("Hybrid pixel, $a$ = 0.5", "Hybrid pixel, half the ranging area given to colour", 0.5, 1.0, 1.0),
    ("Colour band in path, $m$ = 2.5", "One SPAD ranging through a colour filter, mildest case", 1.0, M_LOW, 1.0),
    ("Colour band in path, $m$ = 6.0", "The same, middle case", 1.0, M_MID, 1.0),
    ("Colour band in path, $m$ = 11", "The same, grey scene and visible-efficient SPAD", 1.0, M_HIGH, 1.0),
    ("$m$ = 6.0 with dead time", "The middle case with the dead time of the C0 model", 1.0, M_MID, LIVE_MID),
]


def check(name: str, value: float, reference: float, tol: float) -> str:
    """One plain check: value, reference, error and tolerance on one line."""
    err = value - reference
    verdict = "pass" if abs(err) <= tol else "FAIL"
    return (f"{name}: value {value:.6g}, reference {reference:.6g}, error {err:+.3g}, "
            f"tolerance {tol:.3g} -> {verdict}")


def checks() -> list[str]:
    """Hand values quoted in section C5b, recomputed one at a time."""
    alpha_865 = 290.0 * (290.0 / 183.0) ** (40.0 / 35.0)  # cm^-1, log-linear from 905 and 940 nm (section C4)
    dwell_1024_10 = 1.0 / (1024 * 10.0)                   # s, column dwell of the 1,024 x 10 Hz mode
    kappa_toa = planck_photon_ratio(550.0, 865.0)
    out = [
        check("0.75^(1/4)", 0.75 ** 0.25, 0.9306, 5e-5),
        check("0.75^(1/2)", 0.75 ** 0.5, 0.8660, 5e-5),
        check("6.0^(-1/4)", 6.0 ** -0.25, 0.6389, 5e-5),
        check("m, mildest case", M_LOW, 2.5, 1e-9),
        check("m, middle case", M_MID, 6.0, 1e-9),
        check("m, grey scene", M_HIGH, 11.0, 1e-9),
        check("live fraction at x0 = 0.122 (C0 model 0.885)", live_fraction(1.0), 0.885, 5e-4),
        check("live fraction at m = 6", live_fraction(M_MID), 0.481, 5e-4),
        check("dead-time factor (l / l0)^(1/4), m = 6", LIVE_MID ** 0.25, 0.8586, 5e-4),
        check("Planck photon flux per nm, 550 nm over 865 nm, 5,800 K", kappa_toa, 1.129, 1e-3),
        check("m = 6 range factor with kappa = 1.13 over kappa = 1",
              ((1.0 + kappa_toa * 5.0) / (1.0 + 5.0)) ** -0.25, 0.975, 1e-3),
        check("Si absorption coefficient at 865 nm (cm^-1)", alpha_865, 491.0, 1.0),
        check("single-pass absorption, d = 3 um", 1.0 - np.exp(-alpha_865 * 3e-4), 0.137, 1e-3),
        check("single-pass absorption, d = 5 um", 1.0 - np.exp(-alpha_865 * 5e-4), 0.217, 1e-3),
        check("OS1 reflectance exponent ln(170/90) / ln 8", np.log(170.0 / 90.0) / np.log(8.0), 0.306, 1e-3),
        check("colour dynamic range 20 log10(2e6 / 3) (dB)", 20.0 * np.log10(2e6 / 3.0), 116.48, 0.01),
        check("16-bit linear span 20 log10(2^16) (dB)", 20.0 * np.log10(2.0 ** 16), 96.33, 0.01),
        check("column rate 1,024 x 40 Hz (1/s)", 1024 * 40.0, 40960.0, 0.0),
        check("dual-return point rate 128 x 40,960 x 2 (1/s)", 128 * 40960 * 2.0, 10485760.0, 0.0),
        check("timing precision 2 sigma_R / c for 0.25 cm (ps)", 2 * 0.0025 / 2.99792458e8 * 1e12, 16.68, 0.01),
        check("counts per sample at 2 Mlx, scaled from 10 at 3 lx", 10.0 * 2e6 / 3.0, 6.67e6, 0.01e6),
        check("count rate per channel at 2 Mlx, 97.7 us dwell (1/s)", 10.0 * 2e6 / 3.0 / dwell_1024_10, 6.83e10, 0.01e10),
        check("colour count rate at 100 klx, 97.7 us dwell (1/s)", 10.0 * 1e5 / 3.0 / dwell_1024_10, 3.41e9, 0.01e9),
        check("fill range of a 30 cm object in a 44/128 deg row (m)", 0.30 / np.radians(44.0 / 128.0), 50.0, 0.1),
        check("time offset of 5 column steps at 10,240 /s (ms)", 5.0 / 10240.0 * 1e3, 0.488, 1e-3),
    ]
    return out


def table_lines() -> list[str]:
    lines = [f"{'Layout':66s} {'a':>5s} {'m':>6s} {'live':>6s} {'sun':>6s} {'night':>6s}"]
    for _, label, a, m, live in CASES:
        lines.append(f"{label:66s} {a:5.2f} {m:6.2f} {live:6.3f} {range_factor_sun(a, m, live):6.3f} "
                     f"{range_factor_night(a):6.3f}")
    return lines


def draw() -> plt.Figure:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(6.3, 3.4), constrained_layout=True)
    y = np.arange(len(CASES))
    h = 0.38
    sun = [range_factor_sun(a, m, live) for _, _, a, m, live in CASES]
    night = [range_factor_night(a) for _, _, a, _, _ in CASES]
    bars_sun = ax.barh(y - h / 2, sun, h, color=COLORS["warm_accent"], label="Full sun (background-limited)")
    bars_night = ax.barh(y + h / 2, night, h, color=COLORS["primary"], label="Night (signal-limited)")
    for bars, vals in ((bars_sun, sun), (bars_night, night)):
        for rect, v in zip(bars, vals):  # values inside the bar ends, clear of the dashed 1.0 line
            ax.text(v - 0.012, rect.get_y() + rect.get_height() / 2, f"{v:.2f}", ha="right", va="center",
                    fontsize=FONT_SIZE, color=COLORS["background"])
    ax.axvline(1.0, color=COLORS["neutral"], linewidth=0.8, linestyle=(0, (5, 2)), zorder=0, label="_nolegend_")
    ax.set_yticks(y, [c[0] for c in CASES])
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0.0, 1.16)
    ax.set_ylim(len(CASES) - 0.45, -0.55)
    ax.set_xlabel(r"Range relative to the same receiver without colour, $R/R_0$")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    return fig


def main() -> None:
    header = [
        "Range cost of colour channels on a SPAD lidar chip (section C5b, Figure C5b.1) [E]",
        f"Inputs: colour band {DL_C:.0f} nm, laser pass band {DL_L:.0f} nm, kappa {KAPPA:.2f}, x0 {X0:.3f}",
        "Full sun: R/R0 = (a * live / m)^(1/4); night: R/R0 = a^(1/2)",
        "",
    ]
    body = table_lines()
    chk = ["", "Checks (value, reference, error, tolerance):"] + checks()
    text = "\n".join(header + body + chk) + "\n"
    print(text)
    (OUT_DIR / f"{STEM}_tables.txt").write_bytes(text.encode("utf-8"))  # LF line endings on every platform
    fig = draw()
    fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
    fig.savefig(OUT_DIR / f"{STEM}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
