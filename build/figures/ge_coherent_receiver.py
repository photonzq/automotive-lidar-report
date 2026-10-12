"""Can a Ge-on-Si photodiode serve a coherent (FMCW) lidar receiver?

Companion to section C4c of automotive_perception_report_2026-09-27.md.
Order-of-magnitude engineering estimates [E].

(a) Shot-noise efficiency of a balanced Ge photodiode pair with a strong local
    oscillator (LO):
        eta_sn = I_LO / (I_LO + 2 I_d + I_th^2 / (2 q))
    I_LO   = responsivity x LO power delivered to the pair (both diodes together),
    I_d    = dark current per diode, scaled with temperature as
             I_d(T) = I_d(25 C) (T/T0)^3 exp[-(E_a/k)(1/T - 1/T0)],
    I_th   = input-referred TIA noise current density (A/sqrt(Hz)).
    eta_sn = 1 means LO-shot-noise-limited (the ideal coherent receiver).

(b) Position of the Ge direct-gap (Gamma) absorption edge versus temperature:
    Varshni form E_G(T) = 0.8893 - 6.842e-4 T^2 / (T + 398) eV for bulk Ge,
    shifted by a biaxial tensile-strain term (about -0.11 eV per 1 % strain) typical
    of Ge-on-Si.  The edge is where strong direct absorption begins; absorption
    does not stop abruptly there (indirect absorption and band tails remain), so
    this is a design-margin indicator, not a responsivity model.
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


Q = 1.602176634e-19
K_B_EV = 8.617333262e-5
HC_EV_NM = 1239.84198
T0 = 298.15


def dark_current(i_d25: float, t_c: np.ndarray, e_a: float) -> np.ndarray:
    t = np.asarray(t_c) + 273.15
    return i_d25 * (t / T0) ** 3 * np.exp(-(e_a / K_B_EV) * (1.0 / t - 1.0 / T0))


def shot_noise_efficiency(p_lo: np.ndarray, i_d: float, i_th: float, resp: float = 0.9) -> np.ndarray:
    i_lo = resp * p_lo
    return i_lo / (i_lo + 2.0 * i_d + i_th**2 / (2.0 * Q))


def ge_gamma_edge_nm(t_c: np.ndarray, strain_pct: float) -> np.ndarray:
    t = np.asarray(t_c) + 273.15
    e_bulk = 0.8893 - 6.842e-4 * t**2 / (t + 398.0)
    e = e_bulk - 0.11 * strain_pct
    return HC_EV_NM / e


def make_tables() -> str:
    lines = ["Dark current per diode vs temperature, starting from I_d(25 C) = 50 nA"]
    temps = np.array([-40, 25, 85, 105, 125])
    for e_a in (0.35, 0.50):
        vals = dark_current(50e-9, temps, e_a)
        lines.append(f"  E_a = {e_a:.2f} eV: " + ", ".join(f"{t:+d} C {v*1e6:.3g} uA" for t, v in zip(temps, vals)))
    lines.append(f"TIA noise 3 pA/rtHz is equivalent to a shot-noise current of {(3e-12)**2/(2*Q)*1e6:.1f} uA")
    lines.append("")
    lines.append("Shot-noise efficiency (balanced pair, R = 0.9 A/W, TIA 3 pA/rtHz)")
    for p_lo in (0.1e-3, 0.3e-3, 1e-3):
        row = f"  P_LO {p_lo*1e3:.1f} mW:"
        for t_c in (25, 105, 125):
            i_d = float(dark_current(50e-9, t_c, 0.50))
            row += f"  {t_c} C (I_d {i_d*1e6:.2g} uA) {shot_noise_efficiency(p_lo, i_d, 3e-12):.3f}"
        lines.append(row)
    lines.append("")
    lines.append("Ge direct-gap edge (nm) vs temperature")
    for s in (0.0, 0.20, 0.25):
        lines.append(f"  strain {s:.2f} %: " + ", ".join(
            f"{t:+d} C {float(ge_gamma_edge_nm(t, s)):.0f}" for t in temps))
    return "\n".join(lines)


def figure(out_stem: Path) -> None:
    configure_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.3), constrained_layout=True)

    ax = axes[0]
    p_lo = np.logspace(-5, -2, 200)
    cases = [
        ("25 °C, $I_d$ = 50 nA", float(dark_current(50e-9, 25, 0.5)), COLORS["primary"], "-"),
        ("105 °C", float(dark_current(50e-9, 105, 0.5)), COLORS["warm_accent"], "-"),
        ("125 °C", float(dark_current(50e-9, 125, 0.5)), COLORS["warm_accent"], DASH),
        ("125 °C, 10× leakier diode", float(dark_current(500e-9, 125, 0.5)), COLORS["purple_accent"], DASH),
    ]
    for lab, i_d, col, ls in cases:
        ax.plot(p_lo * 1e3, shot_noise_efficiency(p_lo, i_d, 3e-12), color=col, ls=ls, lw=LW, label=lab)
    ax.plot(p_lo * 1e3, shot_noise_efficiency(p_lo, 0.0, 10e-12), color=COLORS["grey_accent"], ls=":", lw=LW,
            label="no dark current, 10 pA Hz$^{-1/2}$ TIA")
    ax.axvspan(0.3, 1.0, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, linewidth=0, label="_nolegend_", zorder=0)
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(1e-2, 10)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("LO power on the balanced pair (mW)")
    ax.set_ylabel("Shot-noise efficiency $\\eta_{\\rm sn}$")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, columnspacing=1.0)
    ax.set_title("(a) Strong-LO receiver, TIA 3 pA Hz$^{-1/2}$", loc="left")

    ax = axes[1]
    t = np.linspace(-40, 125, 200)
    ax.axvspan(-40, 105, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, linewidth=0, label="_nolegend_", zorder=0)
    for s, col, ls in [(0.0, COLORS["grey_accent"], DASH), (0.20, COLORS["primary"], "-"), (0.25, COLORS["cool_accent"], "-")]:
        ax.plot(t, ge_gamma_edge_nm(t, s), color=col, ls=ls, lw=LW,
                label=("bulk Ge" if s == 0 else f"Ge-on-Si, {s:.2f}% tensile"))
    for wl, lab in [(1550, "1550 nm"), (1310, "1310 nm")]:
        ax.axhline(wl, color=COLORS["warm_accent"], lw=1.0, ls=":", label="_nolegend_")
        ax.text(120, wl + 6, lab, color=COLORS["warm_accent"], ha="right", va="bottom")
    ax.set_xlim(-45, 130)
    ax.set_ylim(1280, 1720)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Direct-gap absorption edge (nm)")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.1))
    ax.set_title("(b) Ge edge vs temperature (model)", loc="left")

    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    here = OUT_DIR
    text = make_tables()
    (here / "ge_coherent_receiver_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    figure(here / "ge_coherent_receiver")


if __name__ == "__main__":
    main()
