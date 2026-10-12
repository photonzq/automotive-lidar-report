"""Long-range sensing for a heavy truck at highway speed: what a camera, stereo pair,
lidar (ToF or FMCW) and radar can deliver at 150-400 m.

Companion to section E12 of automotive_perception_report_2026-09-27.md.
Order-of-magnitude engineering estimates [E].

Scenario: 80,000 lb truck at 105 km/h (29.2 m/s), stopping distance 166-257 m
(section F6); stalled passenger car 1.8 m wide, 1.5 m high, in lane.

Models:
- Decision time available if the hazard is first detected at range R:
      t_avail = (R - d_stop) / v.
- Mono camera, time to separate "stationary" from "moving with traffic" (25 m/s) from
  image expansion alone.  Image width w = W / (R * IFOV) pixels grows at
  w / TTC with TTC = R / v.  A linear fit over T seconds at f frames/s with per-frame
  edge noise sigma_w has slope noise sigma_w * sqrt(12 / (f T^3)).  T is solved for a
  5-sigma separation.  Daylight, clean tracking: an optimistic bound.
- Mono camera absolute range from the ground plane: dR = R^2 * dtheta / h (camera
  height h, pitch/road-grade uncertainty dtheta); from a size prior: dR = 0.1 R.
- Stereo: dR = R^2 * sigma_d * IFOV / B.
- Lidar: range noise ~5 cm; ToF velocity needs >= 2 frames at 10 Hz; FMCW gives radial
  velocity per point in one measurement (~10-20 us dwell, shown as one 0.1 s frame).
- Cross-range cell = beam or pixel angle x R.
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
HIGHLIGHT_ALPHA = 0.24
LW = 1.5
DASH = (0, (5, 2))


def configure_plot_style() -> None:
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


V = 105 / 3.6
D_STOP = (166.0, 257.0)  # Eq. (11), section A6.1: 29.2 m/s, t_r = 1.5 s, a_b = 3.5 and 2.0 m/s^2 (section F6)
CAR_W, CAR_H = 1.8, 1.5
LANE = 3.7


def t_avail(r, d_stop):
    return (r - d_stop) / V


def t_mono_decide(r, ifov, sigma_w=0.3, fps=36.0, v_lead=25.0, nsig=5.0):
    w = CAR_W / (r * ifov)
    d_slope = w * V / r - w * (V - v_lead) / r
    return (nsig * sigma_w / d_slope) ** (2.0 / 3.0) * (12.0 / fps) ** (1.0 / 3.0)


def mono_ground_err(r, dtheta, h=2.75):
    return r**2 * dtheta / h


def stereo_err(r, baseline=1.5, ifov=0.1e-3, sigma_d=0.2):
    return r**2 * sigma_d * ifov / baseline


def make_tables() -> str:
    rr = np.array([150.0, 200.0, 250.0, 300.0, 400.0])
    out = [f"Truck at {V:.1f} m/s; stopping distance {D_STOP[0]:.0f}-{D_STOP[1]:.0f} m",
           "Range (m):                         " + "  ".join(f"{r:>7.0f}" for r in rr)]
    rows = [
        ("t available, worst case (s)", t_avail(rr, D_STOP[1])),
        ("t available, best case (s)", t_avail(rr, D_STOP[0])),
        ("mono 0.25 mrad: px across car", CAR_W / (rr * 0.25e-3)),
        ("mono 0.45 mrad: px across car", CAR_W / (rr * 0.45e-3)),
        ("mono 0.25 mrad: t to decide (s)", t_mono_decide(rr, 0.25e-3)),
        ("mono 0.45 mrad: t to decide (s)", t_mono_decide(rr, 0.45e-3)),
        ("mono ground-plane err, 0.5 mrad", mono_ground_err(rr, 0.5e-3)),
        ("mono ground-plane err, 2 mrad", mono_ground_err(rr, 2e-3)),
        ("mono size-prior err (10%)", 0.1 * rr),
        ("stereo 1.5 m, 0.2 px err (m)", stereo_err(rr)),
        ("lidar 0.1 deg: points on car", (np.degrees(CAR_W / rr) / 0.1) * (np.degrees(CAR_H / rr) / 0.1)),
        ("lidar 0.05 deg: points on car", (np.degrees(CAR_W / rr) / 0.05) * (np.degrees(CAR_H / rr) / 0.05)),
        ("radar 1 deg cross-range cell (m)", np.radians(1.0) * rr),
        ("4D radar 0.5 deg cell (m)", np.radians(0.5) * rr),
    ]
    for name, vals in rows:
        out.append(f"{name:<34}" + "  ".join(f"{x:>7.2f}" for x in vals))
    out.append("ToF lidar velocity: ~0.7 m/s after 2 frames (0.2 s), ~0.2 m/s after 5 frames (0.4 s)")
    out.append("FMCW: radial velocity ~0.05-0.2 m/s per point in one measurement")
    return "\n".join(out)


def figure(out_stem: Path) -> None:
    configure_plot_style()
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.7), constrained_layout=True)
    r = np.linspace(150, 450, 300)

    ax = axes[0]
    ax.fill_between(r, t_avail(r, D_STOP[1]), t_avail(r, D_STOP[0]), color=COLORS["grey_accent"],
                    alpha=0.18, linewidth=0, label="time available")
    ax.axvspan(150, 250, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, linewidth=0,
               label="_nolegend_", zorder=0)
    ax.text(155, 7.3, "typical high-beam\nreach at night", color=COLORS["annotation"], va="top")
    ax.plot(r, t_mono_decide(r, 0.25e-3), color=COLORS["primary"], lw=LW,
            label="mono camera, 0.25 mrad (day)")
    ax.plot(r, t_mono_decide(r, 0.45e-3), color=COLORS["primary"], lw=LW, ls=DASH,
            label="mono camera, 0.45 mrad (day)")
    ax.plot(r, np.full_like(r, 0.2), color=COLORS["cool_accent"], lw=LW, label="ToF lidar, 2 frames")
    ax.plot(r, np.full_like(r, 0.1), color=COLORS["warm_accent"], lw=LW, ls=DASH, label="FMCW, 1 frame")
    ax.axhline(0, color=COLORS["axes"], lw=0.6)
    ax.set_xlim(150, 450)
    ax.set_ylim(-1, 8)
    ax.set_xlabel("First-detection range (m)")
    ax.set_ylabel("Time (s)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1)
    ax.set_title("(a) Time to decide vs time available", loc="left")

    ax = axes[1]
    ax.plot(r, mono_ground_err(r, 2e-3), color=COLORS["primary"], lw=LW, label="mono, ground plane, 2 mrad")
    ax.plot(r, mono_ground_err(r, 0.5e-3), color=COLORS["primary"], lw=LW, ls=DASH,
            label="mono, ground plane, 0.5 mrad")
    ax.plot(r, 0.1 * r, color=COLORS["purple_accent"], lw=LW, ls=DASH, label="mono, 10% size prior")
    ax.plot(r, stereo_err(r), color=COLORS["teal_accent"], lw=LW, label="stereo, 1.5 m baseline")
    ax.plot(r, np.full_like(r, 0.05), color=COLORS["cool_accent"], lw=LW, label="lidar (ToF or FMCW)")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(150, 450)
    ax.set_ylim(0.02, 300)
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Range uncertainty (m)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1)
    ax.set_title("(b) Absolute range error", loc="left")

    ax = axes[2]
    for ang, lab, col, ls in [(np.radians(2.0), "radar, 2°", COLORS["brown_accent"], "-"),
                              (np.radians(1.0), "radar, 1°", COLORS["brown_accent"], DASH),
                              (np.radians(0.5), "4D radar, 0.5°", COLORS["warm_accent"], DASH),
                              (np.radians(0.1), "lidar, 0.1°", COLORS["cool_accent"], "-"),
                              (0.25e-3, "camera pixel, 0.25 mrad", COLORS["primary"], "-")]:
        ax.plot(r, ang * r, color=col, lw=LW, ls=ls, label=lab)
    ax.axhline(LANE, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
    ax.text(300, LANE * 1.1, "lane width 3.7 m", color=COLORS["annotation"])
    ax.axhline(CAR_W, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
    ax.text(155, CAR_W * 0.62, "car width 1.8 m", color=COLORS["annotation"])
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(150, 450)
    ax.set_ylim(0.02, 30)
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Cross-range cell (m)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1)
    ax.set_title("(c) Placing a static return in-lane", loc="left")

    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    here = OUT_DIR
    text = make_tables()
    (here / "truck_long_range_sensing_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    figure(here / "truck_long_range_sensing")


if __name__ == "__main__":
    main()
