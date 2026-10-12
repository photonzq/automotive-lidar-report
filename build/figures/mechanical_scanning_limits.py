"""Mechanical beam steering for automotive lidar: vibration band, scan walk-off,
mirror dynamic deformation, and how channel parallelism sets mechanical speed.

Companion to section C4d of automotive_perception_report_2026-09-27.md.
Engineering estimates [E] built from these inputs:
- ISO 16750-3:2012 Test IV (passenger car, sprung masses): random PSD
  30 (m/s^2)^2/Hz at 10 Hz, 0.2 at 400 Hz and 1000 Hz; 27.1 m/s^2 rms;
  8 h per plane (public iTeh preview of the standard).
- Walk-off during the round trip: d_theta = 2 R omega / c.
  Scanner angular speeds: 360 deg spin at 10 Hz; Hesai AT128 3-facet mirror at
  200 rpm (optical speed = 2 x mechanical); Seyond Falcon K1 five-facet polygon
  with four beams (teardown): 1520 lines/s / (4 x 5) = 76 rev/s, optical
  speed 2 x 360 deg x 76 = 54,720 deg/s;
  resonant MEMS peak speed pi * f * (peak-to-peak optical angle).
- Brosens dynamic deformation of a sinusoidally scanned mirror:
  delta = 0.217 rho f^2 D^5 theta_mech / (E t^2), silicon rho = 2330 kg/m^3,
  E = 169 GPa, theta_mech = 0.26 rad (15 deg).
- Required fast-axis sweep rate S = N_lines * F / N_parallel.
No product data are altered; product markers use published line counts, frame
rates and channel counts, with assumptions stated in the tables file.
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
C_LIGHT = 2.99792458e8


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


# ---------------------------------------------------------------- inputs
PSD_F = np.array([10.0, 400.0, 1000.0])
PSD_S = np.array([30.0, 0.2, 0.2])


def iso_test_iv_psd(f: np.ndarray) -> np.ndarray:
    """ISO 16750-3:2012 Test IV PSD, log-log interpolation, zero outside 10-1000 Hz."""
    f = np.asarray(f, float)
    out = np.exp(np.interp(np.log(f), np.log(PSD_F), np.log(PSD_S)))
    out[(f < 10) | (f > 1000)] = np.nan
    return out


def brosens_nm(d_m, f_hz, t_m, theta=0.26, rho=2330.0, e_mod=169e9):
    return 0.217 * rho * f_hz**2 * d_m**5 * theta / (e_mod * t_m**2) * 1e9


SCANNERS = [
    # label, optical angular speed (deg/s), colour, linestyle
    ("360° spin, 10 Hz", 3600.0, COLORS["cool_accent"], "-"),
    ("AT128 mirror, 200 rpm", 2 * 200 / 60 * 360, COLORS["teal_accent"], DASH),
    ("Polygon, Falcon K1 (5 facets, 4 beams)", 2 * 360.0 * 1520 / (4 * 5),
     COLORS["brown_accent"], "-"),
    ("Resonant MEMS, 1 kHz, ±30°", np.degrees(np.pi * 1000 * np.radians(60)),
     COLORS["primary"], "-"),
    ("Resonant 1D MEMS, 1.5 kHz, 180°", np.degrees(np.pi * 1500 * np.radians(180)),
     COLORS["warm_accent"], "-"),
]

PRODUCTS = [
    # label, lines per frame, frame rate, parallel channels along lines
    ("HDL-64E", 64, 10, 64),
    ("AT128", 128, 10, 128),
    ("ATX", 256, 10, 256),
    ("Falcon K1 (4 beams, teardown)", 152, 10, 4),
    # 10 Hz per the RS-LiDAR-M1 user guide (rev. 1.7, 2021); 15 Hz was the January 2020 pre-series launch figure
    ("M1 (1 beam per module, teardown)", 125, 10, 1),
    ("InnovizOne 256 lines (4 lasers, company statement)", 256, 10, 4),
]


def make_tables() -> str:
    lines = ["ISO 16750-3:2012 Test IV PSD, (m/s^2)^2/Hz"]
    for f in (20, 50, 100, 136, 200, 300, 400, 1000):
        lines.append(f"  {f:5d} Hz: {float(iso_test_iv_psd(np.array([f]))[0]):.3f}")
    fg = np.logspace(1, 3, 4000)
    s = iso_test_iv_psd(fg)
    ms_total = np.trapezoid(s, fg)
    ms_400 = np.trapezoid(s[fg <= 400], fg[fg <= 400])
    lines.append(f"  rms = {np.sqrt(ms_total):.1f} m/s^2; share of mean square below 400 Hz = {ms_400 / ms_total:.0%}")
    lines.append("Walk-off 2 R omega / c (deg)")
    for lab, w, _, _ in SCANNERS:
        vals = ", ".join(f"{r} m: {w * 2 * r / C_LIGHT:.4f}" for r in (150, 200, 250))
        lines.append(f"  {lab} ({w:,.0f} deg/s): {vals}")
    lines.append("Brosens deformation (nm), theta_mech = 0.26 rad, silicon")
    for d in (2e-3, 3e-3, 5e-3, 10e-3):
        vals = ", ".join(
            f"{f / 1e3:.1f} kHz/{t * 1e6:.0f} um: {brosens_nm(d, f, t):.0f}"
            for f in (1000, 1500) for t in (100e-6, 250e-6))
        lines.append(f"  D = {d * 1e3:.0f} mm: {vals}")
    lines.append("Required fast-axis sweeps per second S = N_lines * F / N_parallel")
    for lab, n, fr, par in PRODUCTS:
        lines.append(f"  {lab}: {n} x {fr} / {par} = {n * fr / par:.0f}")
    return "\n".join(lines)


def figure(out_stem: Path) -> None:
    configure_plot_style()
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 6.48), constrained_layout=True)

    # (a) vibration band and resonances
    ax = axes[0, 0]
    f = np.logspace(1, np.log10(1000), 400)
    ax.plot(f, iso_test_iv_psd(f), color=COLORS["neutral"], lw=LW,
            label="ISO 16750-3 Test IV (body)")
    ax.axvspan(1000, 3000, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA,
               linewidth=0, label="_nolegend_", zorder=0)
    ax.text(1040, 22, "above the\nprofile", color=COLORS["text"])
    marks = [
        (136, "EM 2-D slow\naxis, 136 Hz", COLORS["warm_accent"], 7.0, "left"),
        (300, "quasi-static\n5–6 mm,\n300–\n350 Hz", COLORS["purple_accent"], 1.3, "left"),
        (800, ">0.8 kHz\nguideline", COLORS["primary"], 0.055, "right"),
        (1500, "1.5 kHz\nresonant\n1-D", COLORS["teal_accent"], 0.45, "left"),
    ]
    for x, lab, col, ytxt, ha in marks:
        ax.axvline(x, color=col, lw=1.0, ls=DASH, label="_nolegend_")
        xt = x * 1.07 if ha == "left" else x / 1.07
        ax.text(xt, ytxt, lab, color=col, ha=ha)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(10, 3000)
    ax.set_ylim(0.03, 60)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(r"Acceleration PSD ((m s$^{-2}$)$^2$ Hz$^{-1}$)")
    ax.legend(loc="lower left")
    ax.set_title("(a) Road-vibration band vs mirror resonances", loc="left")

    # (b) walk-off vs range
    ax = axes[0, 1]
    r = np.linspace(1, 300, 300)
    for lab, w, col, ls in SCANNERS:
        ax.plot(r, w * 2 * r / C_LIGHT, color=col, lw=LW, ls=ls, label=lab)
    for pix, txt, fy in ((0.1, "0.1° pixel", 1.12), (0.05, "0.05° pixel", 1 / 1.6)):
        ax.axhline(pix, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
        ax.text(235, pix * fy, txt, color=COLORS["annotation"])
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(0, 300)
    ax.set_ylim(1e-5, 3)
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Scan walk-off during round trip (deg)")
    ax.legend(loc="lower right")
    ax.set_title("(b) Coaxial receive: how far the scanner moves", loc="left")

    # (c) Brosens deformation vs diameter
    ax = axes[1, 0]
    d = np.linspace(1e-3, 12e-3, 300)
    for fhz, t, col, ls in ((500, 100e-6, COLORS["cool_accent"], "-"),
                            (1000, 100e-6, COLORS["primary"], "-"),
                            (1500, 100e-6, COLORS["warm_accent"], "-"),
                            (1500, 250e-6, COLORS["warm_accent"], DASH)):
        ax.plot(d * 1e3, brosens_nm(d, fhz, t), color=col, lw=LW, ls=ls,
                label=f"{fhz / 1e3:.1f} kHz, t = {t * 1e6:.0f} µm")
    ax.axhline(90.5, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
    ax.text(1.2, 110, r"$\lambda/10$ at 905 nm", color=COLORS["annotation"])
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(1, 12)
    ax.set_ylim(0.1, 1e5)
    ax.set_xlabel("Mirror diameter, D (mm)")
    ax.set_ylabel(r"Dynamic deformation, $\delta$ (nm)")
    ax.legend(loc="lower right")
    ax.set_title(r"(c) Brosens deformation, Si, $\theta_{\rm mech}$ = 15°", loc="left")

    # (d) sweeps per second vs parallel channels
    ax = axes[1, 1]
    npar = np.logspace(0, np.log10(300), 200)
    for nl, fr, col, ls in ((128, 10, COLORS["neutral"], "-"),
                            (256, 10, COLORS["neutral"], DASH)):
        ax.plot(npar, nl * fr / npar, color=col, lw=LW, ls=ls,
                label=f"{nl} lines at {fr} Hz")
    ax.axhspan(625, 3000, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA,
               linewidth=0, label="_nolegend_", zorder=0)
    ax.text(40, 900, "kHz-class resonant\nmirror needed", color=COLORS["text"])
    pcols = [COLORS["cool_accent"], COLORS["teal_accent"], COLORS["teal_accent"],
             COLORS["brown_accent"], COLORS["primary"], COLORS["purple_accent"]]
    place = [  # x factor, y factor, horizontal alignment
        (1 / 1.2, 0.72, "right"), (1.0, 0.52, "center"), (1.0, 0.52, "center"),
        (1.2, 1.0, "left"), (1.2, 0.72, "left"), (1.2, 1.12, "left")]
    for (lab, n, fr, par), col, (dx, dy, ha) in zip(PRODUCTS, pcols, place):
        s = n * fr / par
        ax.plot(par, s, marker="o", ms=4, color=col, ls="none", label="_nolegend_")
        ax.text(par * dx, s * dy, lab.split(" (")[0], color=col, ha=ha)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(0.7, 400)
    ax.set_ylim(3, 1e4)
    ax.set_xlabel("Parallel channels along the slow axis")
    ax.set_ylabel(r"Fast-axis sweeps per second (s$^{-1}$)")
    ax.legend(loc="upper right")
    ax.set_title("(d) Parallel channels set the mechanical speed", loc="left")

    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    here = OUT_DIR
    text = make_tables()
    (here / "mechanical_scanning_limits_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    figure(here / "mechanical_scanning_limits")


if __name__ == "__main__":
    main()
