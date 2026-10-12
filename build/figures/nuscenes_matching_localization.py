"""How much of a camera-only detector's nuScenes deficit is a localization penalty?

Companion to section E11.1 of automotive_perception_report_2026-09-27.md.
Illustrative estimate [E].

nuScenes detection mAP counts a prediction as a true positive when its BEV centre lies
within t of the ground-truth centre, and averages AP over t = 0.5, 1, 2, 4 m.  Here the
only error is localization: a range (depth) error ~ N(0, (k R)^2 + floor^2) plus a small
lateral error, for objects spread uniformly over 5-50 m.  The mean match rate over the
four thresholds is an upper bound on the AP ratio that localization alone permits,
assuming detection and classification are otherwise perfect.
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
THRESHOLDS = (0.5, 1.0, 2.0, 4.0)
OBSERVED_RATIO = 41.6 / 59.6  # BEVFormer (camera) / CenterPoint (lidar), BEVFusion Table I


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


RNG = np.random.default_rng(0)
R = RNG.uniform(5.0, 50.0, 200_000)
UNIT_Z = RNG.standard_normal(R.size)
UNIT_X = RNG.standard_normal(R.size)


def match_rates(k: float, floor: float = 0.1, lateral: float = 0.15) -> np.ndarray:
    ez = UNIT_Z * np.sqrt((k * R) ** 2 + floor**2)
    ex = UNIT_X * lateral
    e = np.hypot(ez, ex)
    return np.array([np.mean(e < t) for t in THRESHOLDS])


def main() -> None:
    here = OUT_DIR
    ks = np.linspace(0.0, 0.08, 81)
    table = np.array([match_rates(k) for k in ks])
    mean = table.mean(axis=1)
    k_obs = float(np.interp(OBSERVED_RATIO, mean[::-1], ks[::-1]))

    lines = ["Depth error (% of range) | match rate at 0.5 / 1 / 2 / 4 m | mean"]
    for k in (0.0, 0.02, 0.04, 0.06, 0.08):
        m = match_rates(k)
        lines.append(f"  {k*100:4.0f}% | " + " / ".join(f"{x:.2f}" for x in m) + f" | {m.mean():.2f}")
    lines.append(f"Observed camera/lidar mAP ratio {OBSERVED_RATIO:.2f} corresponds to a depth error of "
                 f"about {k_obs*100:.1f}% of range in this model")
    text = "\n".join(lines)
    (here / "nuscenes_matching_localization_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)

    configure_plot_style()
    fig, ax = plt.subplots(figsize=(4.2, 3.24), constrained_layout=True)
    cols = [COLORS["warm_accent"], COLORS["purple_accent"], COLORS["teal_accent"], COLORS["cool_accent"]]
    for j, (t, c) in enumerate(zip(THRESHOLDS, cols)):
        ax.plot(ks * 100, table[:, j], color=c, lw=LW, ls=DASH, label=f"match within {t:g} m")
    ax.plot(ks * 100, mean, color=COLORS["primary"], lw=LW, label="mean over thresholds (AP bound)")
    ax.axhline(OBSERVED_RATIO, color=COLORS["annotation"], lw=1.0, ls=":",
               label=f"observed camera/lidar mAP ratio, {OBSERVED_RATIO:.2f}")
    ax.plot(k_obs * 100, OBSERVED_RATIO, "o", color=COLORS["primary"], ms=4, label="_nolegend_")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Camera depth error, $\\sigma_z/R$ (%)")
    ax.set_ylabel("Fraction of objects matched")
    ax.legend(loc="lower left")
    ax.set_title("nuScenes centre-distance matching, objects at 5–50 m", loc="left")
    stem = here / "nuscenes_matching_localization"
    fig.savefig(stem.with_suffix(".png"), dpi=600)
    fig.savefig(stem.with_suffix(".pdf"))
    plt.close(fig)


if __name__ == "__main__":
    main()
