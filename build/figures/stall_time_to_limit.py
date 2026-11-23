"""How long a stalled lidar beam takes to reach the Class 1 limit, against its average power.

Companion to section C4c subsection 1a of automotive_perception_report_2026-09-27.md. Engineering estimates [E] built
on the Class 1 limits of IEC 60825-1:2014 as used in section C4c subsection 1. The script prints the numbers quoted in
the subsection with their checks, writes them to stall_time_to_limit_tables.txt and draws stall_time_to_limit.png /
.pdf (Figure C4c.1).

Relations (section C4c subsections 1 and 1a):
  905 nm, small source (C6 = 1), exposures from about 5 us to 10 s:
      limit E(t) = 7e-4 * C4 * t^0.75  J  through a 7 mm aperture,  C4 = 10^(0.002 (lambda - 700)) = 2.570
      beyond 10 s the limit is the power 3.9e-4 * C4 = 1.00 mW
      a stalled beam of average power P wholly inside the aperture reaches it after t = (7e-4 C4 / P)^4
  905 nm pulse-train rule: each pulse of energy E_p is allowed while E_p <= 7.7e-8 C4 J * C5(N), with
      C5 = max[0.4, (N / 600)^(-1/4)] for N > 600 pulses, so the limit comes after N = 600 (E_single / E_p)^4 pulses
  1,550 nm: radiant exposure 1e4 J m^-2 for exposures up to 10 s over a limiting aperture of diameter
      D = 1 mm (t <= 0.35 s), 1.5 t^0.375 mm (0.35 s < t < 10 s); beyond 10 s the irradiance 1e3 W m^-2 over 3.5 mm
      a stalled beam of average power P, of which a fraction eta(D) enters the aperture, reaches the limit when
      eta(D) P t = 1e4 J m^-2 * pi D^2 / 4  (7.85 mJ for D = 1 mm, so t = 7.85 mJ / (eta P) below 0.35 s)
  Gaussian beam of 1/e^2 diameter d_b centred on an aperture of diameter D: eta = 1 - exp(-2 D^2 / d_b^2)
  scanned beam past an aperture: t_pass = (D_a + d_b) / (omega R), omega = 2 pi f_rot

Inputs [P]:
  Velodyne, about 2 mW per beam (Laser Focus World, 25 Sep 2019, quoting Velodyne).
  Luminar, US 9,874,635 B1: 1 uJ pulses at 640 kHz in the example (0.64 W).
  FARO Focus3D X: 1,550 nm beam "below 500mW" (FARO's safety page).
  FMCW model of section C7a: 3.8 W emitted at 10 Mpts/s, ungated (section C4c subsection 1).
Assumptions [E]: a 3 mm Gaussian beam for the partial-beam case; a 20 kHz pulse rate for the 905 nm pulse-train
example; a head spinning at 10 Hz, a 3 mm beam and the 100 mm evaluation distance for the pass time; a stall leaves the
whole emitted power in one beam (an FMCW source split over n beams pointing in different directions gives n times the
time for each beam).
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
STEM = "stall_time_to_limit"

# ---------------------------------------------------------------- style (house guide)
FONT_SIZE = 8.0
COLORS = {
    "primary": "#385C9E",
    "neutral": "#4D4D4D",
    "warm_accent": "#9E403D",
    "cool_accent": "#477A57",
    "purple_accent": "#6B5B95",
    "grey_accent": "#6F6F6F",
    "annotation": "#767676",
    "text": "#272727",
    "axes": "#000000",
    "background": "#FFFFFF",
}


def configure_plot_style() -> None:
    plt.rcParams.update({
        "figure.facecolor": COLORS["background"], "axes.facecolor": COLORS["background"],
        "axes.edgecolor": COLORS["axes"], "axes.labelcolor": COLORS["text"], "text.color": COLORS["text"],
        "xtick.color": COLORS["axes"], "ytick.color": COLORS["axes"], "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "sans-serif"], "font.size": FONT_SIZE,
        "axes.labelsize": FONT_SIZE, "axes.titlesize": FONT_SIZE, "xtick.labelsize": FONT_SIZE,
        "ytick.labelsize": FONT_SIZE, "legend.fontsize": FONT_SIZE, "axes.linewidth": 0.8,
        "axes.spines.top": True, "axes.spines.right": True, "xtick.top": True, "ytick.right": True,
        "xtick.direction": "in", "ytick.direction": "in", "legend.frameon": False, "axes.grid": False,
        "text.usetex": False, "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True,
        "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.facecolor": "white", "savefig.bbox": "tight",
    })


# ---------------------------------------------------------------- limits (section C4c subsection 1)
C4_905 = 10 ** (0.002 * (905 - 700))          # 2.570
K_905 = 7e-4 * C4_905                         # J s^-0.75: limit 7e-4 C4 t^0.75 for about 5 us to 10 s
P_CW_905 = 3.9e-4 * C4_905                    # W, beyond 10 s
E_SINGLE_905 = 7.7e-8 * C4_905                # J, one ns pulse
H_1550 = 1e4                                  # J m^-2, exposures up to 10 s
E_CW_1550 = 1e3                               # W m^-2, beyond 10 s
D_CW_1550 = 3.5e-3                            # m
P_CW_1550 = E_CW_1550 * np.pi * D_CW_1550 ** 2 / 4    # 9.62 mW
T_SHORT, T_LONG = 0.35, 10.0                  # s

# ---------------------------------------------------------------- examples (section C4c subsection 1a)
P_VELODYNE = 2e-3                             # W per beam, 905 nm
P_LUMINAR = 1e-6 * 640e3                      # W, 1 uJ at 640 kHz
P_FARO = 0.5                                  # W, Focus3D X ("below 500mW")
P_FMCW = 3.8                                  # W, FMCW model of section C7a at 10 Mpts/s
D_BEAM = 3e-3                                 # m, 1/e^2 diameter of the partial-beam case
F_PULSE_905 = 20e3                            # Hz, pulse-train example


def aperture_1550(t: float) -> float:
    """Limiting aperture diameter (m) at 1,550 nm for an exposure of duration t (s)."""
    if t <= T_SHORT:
        return 1.0e-3
    if t < T_LONG:
        return 1.5e-3 * t ** 0.375
    return D_CW_1550


def eta_gauss(d_aperture: float, d_beam: float | None) -> float:
    """Fraction of a centred Gaussian beam (1/e^2 diameter d_beam) inside an aperture; 1 for the whole beam."""
    if d_beam is None:
        return 1.0
    return 1.0 - np.exp(-2.0 * d_aperture ** 2 / d_beam ** 2)


def t_stall_1550(p: float, d_beam: float | None = None) -> float:
    """Time (s) for a stalled 1,550 nm beam of average power p (W) to reach the Class 1 limit; inf if never."""
    def margin(t: float) -> float:
        d = aperture_1550(t)
        return eta_gauss(d, d_beam) * p * t - H_1550 * np.pi * d ** 2 / 4

    grid = np.logspace(-8, np.log10(T_LONG), 4000)
    over = [margin(t) >= 0 for t in grid]
    if any(over):
        i = over.index(True)
        if i == 0:
            return float(grid[0])
        lo, hi = float(grid[i - 1]), float(grid[i])
        for _ in range(80):
            mid = (lo * hi) ** 0.5
            lo, hi = (lo, mid) if margin(mid) >= 0 else (mid, hi)
        return hi
    return T_LONG if eta_gauss(D_CW_1550, d_beam) * p > P_CW_1550 else float("inf")


def t_stall_905(p: float) -> float:
    """Time (s) for a stalled 905 nm beam of average power p (W), wholly inside 7 mm, to reach the limit."""
    t = (K_905 / p) ** 4
    if t <= T_LONG:
        return t
    return T_LONG if p > P_CW_905 else float("inf")


def pulse_train_905(p: float, f_p: float) -> tuple[float, float]:
    """Pulses and time (s) after which the 905 nm pulse-train rule is exceeded by a stalled beam."""
    e_p = p / f_p
    n = 600.0 * (E_SINGLE_905 / e_p) ** 4
    return n, n / f_p


# ---------------------------------------------------------------- tables
POWERS = [1e-3, 1.5e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 0.1, 0.2, 0.5, 0.64, 1.0, 2.0, 3.8, 5.0, 10.0]


T_MIN_905 = 5e-6   # s; below this the t^0.75 law gives way to the single-pulse limit


def fmt_t(t: float) -> str:
    if not np.isfinite(t):
        return "never"
    return f"{t * 1e3:.3g} ms" if t < 1 else f"{t:.3g} s"


def fmt_t905(t: float) -> str:
    return "below 5 us" if t < T_MIN_905 else fmt_t(t)


def table_lines() -> list[str]:
    out = ["Time for a stalled beam to reach the Class 1 limit (no limit reached = never; at 905 nm, times below",
           "5 us fall outside the t^0.75 law and are governed by the single-pulse and pulse-train rules):",
           f"{'P (W)':>8}  {'905 nm, whole beam':>20}  {'1,550 nm, whole beam':>22}  {'1,550 nm, 3 mm beam':>21}"]
    for p in POWERS:
        out.append(f"{p:8.4g}  {fmt_t905(t_stall_905(p)):>20}  {fmt_t(t_stall_1550(p)):>22}  "
                   f"{fmt_t(t_stall_1550(p, D_BEAM)):>21}")
    n, t = pulse_train_905(P_VELODYNE, F_PULSE_905)
    out += ["",
            f"905 nm pulse-train rule at {P_VELODYNE * 1e3:.0f} mW and {F_PULSE_905 / 1e3:.0f} kHz: "
            f"{P_VELODYNE / F_PULSE_905 * 1e9:.0f} nJ per pulse, limit after {n:,.0f} pulses = {t:.3f} s",
            f"Stationary limits: 905 nm {P_CW_905 * 1e3:.3f} mW; 1,550 nm {P_CW_1550 * 1e3:.2f} mW "
            f"(a 3 mm beam needs {P_CW_1550 / eta_gauss(D_CW_1550, D_BEAM) * 1e3:.2f} mW)"]
    return out


# ---------------------------------------------------------------- checks of hand-quoted values
def check(name: str, value: float, reference: float, tol: float) -> str:
    err = value - reference
    verdict = "pass" if abs(err) <= tol else "FAIL"
    return (f"{name}: value {value:.6g}, reference {reference:.6g}, error {err:+.3g}, "
            f"tolerance {tol:.3g} -> {verdict}")


def checks() -> list[str]:
    omega = 2 * np.pi * 10.0
    t_pass = (7e-3 + 3e-3) / (omega * 0.1)
    eta1 = eta_gauss(1e-3, D_BEAM)
    n_pt, t_pt = pulse_train_905(P_VELODYNE, F_PULSE_905)
    return [
        check("C4 at 905 nm", C4_905, 2.57, 0.001),
        check("905 nm limit at 10 s as a power (mW; text 1.01)", K_905 * T_LONG ** 0.75 / T_LONG * 1e3, 1.01, 0.005),
        check("905 nm CW limit (mW; subsection 1: 1.00)", P_CW_905 * 1e3, 1.00, 0.005),
        check("1,550 nm limit through 1 mm (mJ; 7.85)", H_1550 * np.pi * (1e-3) ** 2 / 4 * 1e3, 7.85, 0.005),
        check("1,550 nm CW limit (mW; 9.6)", P_CW_1550 * 1e3, 9.6, 0.05),
        check("1,550 nm aperture at 0.35 s (mm; continuous with 1 mm)", 1.5 * T_SHORT ** 0.375, 1.0, 0.02),
        check("1,550 nm aperture at 10 s (mm; continuous with 3.5 mm)", 1.5 * T_LONG ** 0.375, 3.5, 0.06),
        check("fraction of a 3 mm beam in 1 mm (0.20)", eta1, 0.20, 0.005),
        check("pass time at 10 Hz, 100 mm (ms; 1.6)", t_pass * 1e3, 1.6, 0.05),
        check("rotation rate over the 5 rad/s tracking rule (13)", omega / 5, 13, 0.5),
        check("time share in the aperture (%; 1.6)", t_pass * 10.0 * 100, 1.6, 0.05),
        check("power share in the aperture (1/63)", 1 / (t_pass * 10.0), 63, 0.5),
        check("Luminar example power (W; 0.64)", P_LUMINAR, 0.64, 1e-9),
        check("Luminar over the stationary limit (67)", P_LUMINAR / P_CW_1550, 67, 1.0),
        check("FARO Focus3D X over the stationary limit (52)", P_FARO / P_CW_1550, 52, 0.5),
        check("Velodyne over the stationary limit (2)", P_VELODYNE / P_CW_905, 2, 0.05),
        check("Luminar, whole beam (ms; 12)", t_stall_1550(P_LUMINAR) * 1e3, 12, 0.5),
        check("Luminar, 3 mm beam (ms; 61)", t_stall_1550(P_LUMINAR, D_BEAM) * 1e3, 61, 1.0),
        check("FARO, whole beam (ms; 16)", t_stall_1550(P_FARO) * 1e3, 16, 0.5),
        check("FARO, 3 mm beam (ms; 79)", t_stall_1550(P_FARO, D_BEAM) * 1e3, 79, 1.0),
        check("FMCW, whole beam (ms; 2.1)", t_stall_1550(P_FMCW) * 1e3, 2.1, 0.05),
        check("FMCW, 3 mm beam (ms; 10)", t_stall_1550(P_FMCW, D_BEAM) * 1e3, 10, 0.5),
        check("Velodyne, time-integrated rule (s; 0.65)", t_stall_905(P_VELODYNE), 0.65, 0.01),
        check("Velodyne, pulse energy at 20 kHz (nJ; 100)", P_VELODYNE / F_PULSE_905 * 1e9, 100, 0.5),
        check("Velodyne, pulse-train rule pulses (9,200)", n_pt, 9200, 50),
        check("Velodyne, pulse-train rule time (s; 0.46)", t_pt, 0.46, 0.005),
        check("1,550 nm, a 3 mm beam never reaches the limit below (mW; about 10)",
              P_CW_1550 / eta_gauss(D_CW_1550, D_BEAM) * 1e3, 10, 0.5),
    ]


# ---------------------------------------------------------------- figure
def draw() -> plt.Figure:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(4.2, 3.24), constrained_layout=True)
    p = np.logspace(np.log10(5e-4), 1.0, 1200)

    def below_10s(values: np.ndarray) -> np.ndarray:
        """Hide the points where the limit is the long-exposure power (10 s and beyond) or never reached."""
        out = values.copy()
        out[~(out < T_LONG)] = np.nan
        return out

    t905 = below_10s(np.array([t_stall_905(x) for x in p]))
    t1550 = below_10s(np.array([t_stall_1550(x) for x in p]))
    t1550b = below_10s(np.array([t_stall_1550(x, D_BEAM) for x in p]))
    ax.axhline(0.1, color=COLORS["grey_accent"], linestyle=(0, (5, 2)), linewidth=0.8, zorder=0)
    ax.text(9.0, 0.125, "a check every 100 ms", color=COLORS["grey_accent"], ha="right", va="bottom",
            fontsize=FONT_SIZE)
    ax.plot(p, t905, color=COLORS["primary"], linewidth=1.5, label="905 nm, whole beam")
    ax.plot(p, t1550, color=COLORS["warm_accent"], linewidth=1.5, label="1,550 nm, whole beam")
    ax.plot(p, t1550b, color=COLORS["warm_accent"], linestyle=(0, (5, 2)), linewidth=1.5,
            label="1,550 nm, 3 mm beam")
    marks = [
        (P_VELODYNE, t_stall_905(P_VELODYNE), COLORS["primary"], "o"),
        (P_LUMINAR, t_stall_1550(P_LUMINAR), COLORS["warm_accent"], "s"),
        (P_LUMINAR, t_stall_1550(P_LUMINAR, D_BEAM), COLORS["warm_accent"], "s"),
        (P_FMCW, t_stall_1550(P_FMCW), COLORS["warm_accent"], "^"),
        (P_FMCW, t_stall_1550(P_FMCW, D_BEAM), COLORS["warm_accent"], "^"),
    ]
    for x, y, c, m in marks:
        ax.plot([x], [y], marker=m, markersize=4.5, markerfacecolor="white", markeredgecolor=c,
                markeredgewidth=1.2, linestyle="none", zorder=5)
    # labels sit in empty space (above 10 s on the left, below the solid 1,550 nm line on the right)
    ax.annotate("Velodyne, 2 mW per beam", xy=(P_VELODYNE, t_stall_905(P_VELODYNE)), xytext=(6.5e-4, 30.0),
                ha="left", va="center", fontsize=FONT_SIZE, color=COLORS["primary"],
                arrowprops=dict(arrowstyle="-", color=COLORS["annotation"], linewidth=0.6, shrinkB=3))
    ax.annotate("Luminar patent\nexample, 0.64 W", xy=(P_LUMINAR, t_stall_1550(P_LUMINAR)),
                xytext=(0.17, 1.3e-3), ha="center", va="center", fontsize=FONT_SIZE, color=COLORS["warm_accent"],
                arrowprops=dict(arrowstyle="-", color=COLORS["annotation"], linewidth=0.6, shrinkB=3))
    ax.annotate("FMCW model,\n3.8 W", xy=(P_FMCW, t_stall_1550(P_FMCW)), xytext=(3.2, 2.6e-4),
                ha="center", va="center", fontsize=FONT_SIZE, color=COLORS["warm_accent"],
                arrowprops=dict(arrowstyle="-", color=COLORS["annotation"], linewidth=0.6, shrinkB=3))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(5e-4, 10.0)
    ax.set_ylim(1e-4, 1e2)
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlabel(r"Average power of the stalled beam, $P$ (W)")
    ax.set_ylabel(r"Time to reach the Class 1 limit, $t_{\rm stall}$ (s)")
    ax.legend(loc="upper right", handlelength=2.6)
    return fig


def main() -> None:
    header = [
        "Time for a stalled lidar beam to reach the Class 1 limit (section C4c subsection 1a, Figure C4c.1) [E]",
        "905 nm: t = (7e-4 C4 / P)^4 within 10 s; 1,550 nm: eta(D) P t = 1e4 J m^-2 x pi D^2 / 4, D = 1 mm below 0.35 s",
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
