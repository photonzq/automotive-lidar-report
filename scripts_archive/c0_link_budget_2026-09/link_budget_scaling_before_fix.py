"""Link budget of automotive lidar: loss versus range, the detection level, detection
statistics, and how maximum range scales with transmitted energy per point.

Companion to section C0 subsection 10 of automotive_perception_report_2026-09-27.md.
All outputs are engineering estimates [E] for an extended Lambertian target.

Model
-----
Link loss (fraction of the transmitted energy the receiver can use, before detector
efficiency), Lambertian target of reflectance rho filling the footprint, normal incidence,
two-way clear-air transmission T_atm^2 = exp(-2 alpha R):

  direct detection (lens of diameter D):   L_DD  = rho * A_rx * T^2 / (pi R^2),  A_rx = pi D^2 / 4
  coherent, monostatic Gaussian:           L_coh = rho * A_mode * T^2 / (pi R^2)
                                           A_mode = t^2 lambda^2 R^2 / (2 pi w(R)^2)
      w0 = 0.45 D (waist at the aperture, collimated), t = 1 - exp(-2 (D/2)^2 / w0^2)
      w(R)^2 = w0^2 [1 + (R / z_R)^2],  z_R = pi w0^2 / lambda
      (the factor 1/2 is the single polarization of the LO; same model as
      coherent_mode_coverage.py and fmcw_tof_system_budget.py)
  coherent, best collimated aperture at each range (w0^2 = lambda R / pi):
                                           L_env = rho t^2 lambda T^2 / (4 pi R)

Detection level: L_det = n_req * E_ph / (eta * E_tx); maximum range solves L(R) = L_det.

Detection statistics at a per-bin false-alarm probability P_FA:
  photon counting, Poisson background b per bin: threshold k = min{k : P(N >= k | b) <= P_FA},
      P_D = P(N >= k | s + b) = gammainc(k, s + b)
  coherent, steady target (square-law, one bin):  P_D = Q_1(sqrt(2 S), sqrt(-2 ln P_FA))
  coherent, one speckle (Rayleigh, Swerling I):   P_D = P_FA ** (1 / (1 + S))
  coherent, M speckles summed incoherently:       T_M = Qinv_gamma(M, P_FA),
      P_D = Q_gamma(M, T_M / (1 + S / M))           (S = total mean photoelectrons)
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, LogFormatterMathtext, NullFormatter
from scipy.optimize import brentq
from scipy.special import gammainc, gammaincc, gammainccinv
from scipy.stats import ncx2


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
HIGHLIGHT_ALPHA = 0.24
COLOR_CYCLE = [
    COLORS["primary"],
    COLORS["warm_accent"],
    COLORS["cool_accent"],
    COLORS["purple_accent"],
    COLORS["teal_accent"],
    COLORS["brown_accent"],
    COLORS["grey_accent"],
]
LW = 1.5
DASH = (0, (5, 2))
DASHDOT = (0, (5, 2, 1, 2))


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


# ---------------------------------------------------------------- physics
H = 6.62607015e-34
C = 2.99792458e8
RHO = 0.10
W0_OVER_D = 0.45
T_TRUNC = 1.0 - np.exp(-2.0 * (0.5 / W0_OVER_D) ** 2)  # power through the aperture, 0.915


def photon_energy(lam: float) -> float:
    return H * C / lam


def alpha_clear(lam: float, visibility_km: float = 23.0) -> float:
    """Kim model extinction (1/m), clear air: q = 1.3 for 6 km < V < 50 km."""
    q = 1.3
    return (3.912 / (visibility_km * 1e3)) * (lam / 550e-9) ** (-q)


def t_atm2(R, lam):
    return np.exp(-2.0 * alpha_clear(lam) * R)


def loss_dd(R, D, lam):
    a_rx = np.pi * D**2 / 4.0
    return RHO * a_rx * t_atm2(R, lam) / (np.pi * R**2)


def beam_radius(R, D, lam):
    w0 = W0_OVER_D * D
    z_r = np.pi * w0**2 / lam
    return w0 * np.sqrt(1.0 + (R / z_r) ** 2)


def a_mode(R, D, lam):
    w = beam_radius(R, D, lam)
    return T_TRUNC**2 * lam**2 * R**2 / (2.0 * np.pi * w**2)


def loss_coh(R, D, lam):
    return RHO * a_mode(R, D, lam) * t_atm2(R, lam) / (np.pi * R**2)


def loss_coh_envelope(R, lam):
    return RHO * T_TRUNC**2 * lam * t_atm2(R, lam) / (4.0 * np.pi * R)


def d_opt(R, lam):
    return np.sqrt(lam * R / np.pi) / W0_OVER_D


def kim_alpha(lam: float, visibility_km: float) -> float:
    """Kim model extinction coefficient (1/m) at wavelength lam for meteorological visibility V (km)."""
    v = visibility_km
    if v > 50:
        q = 1.6
    elif v > 6:
        q = 1.3
    elif v > 1:
        q = 0.16 * v + 0.34
    elif v > 0.5:
        q = v - 0.5
    else:
        q = 0.0
    return (3.912 / (v * 1e3)) * (lam / 550e-9) ** (-q)


def loss_dd_alpha(R, D, alpha, rho=RHO):
    """Direct-detection link loss with an explicit extinction coefficient alpha (1/m)."""
    return rho * (np.pi * D**2 / 4.0) * np.exp(-2.0 * alpha * R) / (np.pi * R**2)


def loss_coh_alpha(R, D, lam, alpha, rho=RHO):
    """Coherent (collimated monostatic) link loss with an explicit extinction coefficient alpha (1/m)."""
    return rho * a_mode(R, D, lam) * np.exp(-2.0 * alpha * R) / (np.pi * R**2)


# Receiver cases for the detection level L_det = n_req E_ph / (eta E_tx)
CASES = {
    "spad940": dict(label="SPAD dToF, 940 nm", lam=940e-9, n_req=25.0, eta=0.5 * 0.37, e_tx=0.10e-6),
    "apd1550": dict(label="Linear APD ToF, 1,550 nm", lam=1550e-9, n_req=890.0, eta=0.5 * 0.8, e_tx=2.0e-6),
    "fmcw1550": dict(label="FMCW, 1,550 nm", lam=1550e-9, n_req=30.0, eta=0.25, e_tx=0.30e-6),
}


def l_det(case: dict, e_tx: float | None = None) -> float:
    e = case["e_tx"] if e_tx is None else e_tx
    return case["n_req"] * photon_energy(case["lam"]) / (case["eta"] * e)


def r_max(loss_fn, target: float, r_lo: float = 0.1, r_hi: float = 5e4) -> float:
    """Largest range at which loss_fn(R) >= target (loss_fn decreasing in R)."""
    if loss_fn(r_lo) < target:
        return np.nan
    if loss_fn(r_hi) > target:
        return np.inf
    return brentq(lambda r: np.log(loss_fn(r)) - np.log(target), r_lo, r_hi, xtol=1e-6)


def db(x):
    return -10.0 * np.log10(x)  # loss in positive dB


# ---------------------------------------------------------------- detection statistics
P_FA = 1e-6


def pd_poisson(s, b, p_fa=P_FA):
    k = 1
    while gammainc(k, b) > p_fa:  # P(N >= k | b)
        k += 1
    return gammainc(k, s + b), k


def pd_steady(s, p_fa=P_FA):
    t = -np.log(p_fa)
    return ncx2.sf(2.0 * t, df=2, nc=2.0 * s)


def pd_swerling1(s, p_fa=P_FA):
    return p_fa ** (1.0 / (1.0 + s))


def pd_looks(s, m, p_fa=P_FA):
    t_m = gammainccinv(m, p_fa)
    return gammaincc(m, t_m / (1.0 + s / m))


def s_for_pd(fn, pd=0.9, lo=1e-3, hi=1e4):
    return brentq(lambda s: fn(s) - pd, lo, hi)


# ---------------------------------------------------------------- figures
APERTURES = [(10e-3, COLORS["teal_accent"]), (25e-3, COLORS["primary"]), (50e-3, COLORS["warm_accent"])]
LABEL_BOX = dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.9)
REF_LW = 0.8  # thin reference lines (detection levels, target ranges): annotations, not data


def log_range_axis(ax) -> None:
    ax.set_xscale("log")
    ax.set_xlim(10, 500)
    ax.xaxis.set_major_locator(FixedLocator([10, 20, 50, 100, 200, 500]))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Range, $R$ (m)")
    ax.axvspan(200, 300, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, zorder=0, label="_nolegend_")


def fig_loss(out_stem: Path, lines: list) -> None:
    R = np.logspace(np.log10(10.0), np.log10(500.0), 600)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7), sharey=True, constrained_layout=True)

    # (a) direct detection
    ax = axes[0]
    for D, col in APERTURES:
        ax.plot(R, db(loss_dd(R, D, 940e-9)), color=col, lw=LW, label=f"$D={D * 1e3:.0f}$ mm lens")
    for key, above in [("apd1550", True), ("spad940", False)]:
        cs = CASES[key]
        lvl = db(l_det(cs))
        ax.axhline(lvl, color=COLORS["neutral"], lw=REF_LW, ls=DASH, zorder=1)
        e_str = f"{cs['e_tx'] * 1e6:.1f}".rstrip("0").rstrip(".")
        short = "SPAD, 940 nm" if key == "spad940" else "Linear APD, 1,550 nm"
        ax.text(11, lvl + (0.6 if above else -0.6),
                f"{short}: $\\bar n={cs['n_req']:.0f}$, $E_{{\\rm tx}}={e_str}$ µJ",
                color=COLORS["neutral"], va="bottom" if above else "top", ha="left", zorder=3)
        rm = r_max(lambda r: loss_dd(r, 25e-3, cs["lam"]), l_det(cs))
        ax.plot([rm], [lvl], "o", ms=4, color=COLORS["primary"], zorder=5)
        xt = (rm * 0.72, lvl + 4.5) if above else (rm * 1.12, lvl - 4.5)
        ax.annotate(f"{rm:.0f} m", xy=(rm, lvl), xytext=xt,
                    color=COLORS["primary"], ha="right" if above else "left", va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color=COLORS["annotation"], lw=0.6))
        lines.append(f"(fig 1a) {cs['label']}: L_det = {lvl:.1f} dB; R_max = "
                     f"{r_max(lambda r: loss_dd(r, 10e-3, cs['lam']), l_det(cs)):.0f} / {rm:.0f} / "
                     f"{r_max(lambda r: loss_dd(r, 50e-3, cs['lam']), l_det(cs)):.0f} m for D = 10 / 25 / 50 mm")
    ax.text(0.97, 0.04, r"$\mathcal{L}_{\rm DD}=\rho D^{2}T_{\rm atm}^{2}/(4R^{2})$", transform=ax.transAxes,
            ha="right", va="bottom")
    ax.set_title("(a) Direct detection: the lens collects the whole cell", loc="left")
    ax.legend(loc="upper left", handlelength=2.2)
    log_range_axis(ax)

    # (b) coherent
    ax = axes[1]
    ax.plot(R, db(loss_dd(R, 25e-3, 1550e-9)), color=COLORS["grey_accent"], lw=LW, alpha=0.4,
            label="Direct detection, 25 mm (ref.)")
    for D, col in APERTURES:
        ax.plot(R, db(loss_coh(R, D, 1550e-9)), color=col, lw=LW, label=f"$D={D * 1e3:.0f}$ mm, 1,550 nm")
    ax.plot(R, db(loss_coh(R, 25e-3, 1310e-9)), color=COLORS["purple_accent"], lw=LW, ls=DASH,
            label="$D=25$ mm, 1,310 nm")
    ax.plot(R, db(loss_coh_envelope(R, 1550e-9)), color=COLORS["neutral"], lw=LW, ls=DASHDOT,
            label="Best collimated $D$ at each $R$")
    cs = CASES["fmcw1550"]
    lvl = db(l_det(cs))
    ax.axhline(lvl, color=COLORS["neutral"], lw=REF_LW, ls=DASH, zorder=1)
    ax.text(11, lvl + 0.6, f"{cs['label']}: $\\bar n={cs['n_req']:.0f}$, $E_{{\\rm tx}}=0.3$ µJ",
            color=COLORS["neutral"], va="bottom", ha="left", zorder=3)
    for D, col in APERTURES:
        rm = r_max(lambda r: loss_coh(r, D, 1550e-9), l_det(cs))
        lines.append(f"(fig 1b) FMCW 1550, D = {D * 1e3:.0f} mm: near-field plateau {db(loss_coh(1e-3, D, 1550e-9)):.1f} dB, "
                     f"z_R = {np.pi * (W0_OVER_D * D) ** 2 / 1550e-9:.0f} m, R_max = {rm:.0f} m")
        if np.isfinite(rm) and 10 < rm < 500:
            ax.plot([rm], [lvl], "o", ms=4, color=col, zorder=5)
            ax.annotate(f"{rm:.0f} m", xy=(rm, lvl), xytext=(rm * 1.1, lvl - 4.5), color=col, ha="left",
                        va="center", zorder=5,
                        arrowprops=dict(arrowstyle="-", color=COLORS["annotation"], lw=0.6))
    cs13 = dict(cs, lam=1310e-9)
    rm13 = r_max(lambda r: loss_coh(r, 25e-3, 1310e-9), l_det(cs13))
    lines.append(f"(fig 1b) FMCW 1310, D = 25 mm, same n, eta, E_tx: L_det = {db(l_det(cs13)):.2f} dB, "
                 f"plateau {db(loss_coh(1e-3, 25e-3, 1310e-9)):.2f} dB, R_max = {rm13} (nan = no detection at any range)")
    rm_env = r_max(lambda r: loss_coh_envelope(r, 1550e-9), l_det(cs))
    lines.append(f"(fig 1b) envelope 1550: R_max = {rm_env:.0f} m with D_opt = {d_opt(rm_env, 1550e-9) * 1e3:.1f} mm")
    ax.text(0.03, 0.96, r"$\mathcal{L}_{\rm coh}=\rho t^{2}\lambda^{2}T_{\rm atm}^{2}/(2\pi^{2}w(R)^{2})$",
            transform=ax.transAxes, ha="left", va="top")
    ax.set_title("(b) Coherent, collimated monostatic beam: one spatial mode", loc="left")
    ax.legend(loc="lower right", handlelength=2.2)
    log_range_axis(ax)

    axes[0].set_ylim(55, 122)
    axes[0].set_ylabel(r"Link loss, $-10\log_{10}\mathcal{L}$ (dB)")
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def fig_detection(out_stem: Path, lines: list) -> None:
    s = np.logspace(0, np.log10(400), 700)
    fig, ax = plt.subplots(figsize=(4.6, 3.4), constrained_layout=True)
    pd_n, k_n = pd_poisson(s, 0.01)
    pd_d, k_d = pd_poisson(s, 2.2)
    curves = [
        ("Counting, night, $b=0.01$", pd_n, COLORS["cool_accent"], "-", lambda x: pd_poisson(x, 0.01)[0]),
        ("Counting, bright sun, $b=2.2$", pd_d, COLORS["primary"], "-", lambda x: pd_poisson(x, 2.2)[0]),
        ("Coherent, steady target", pd_steady(s), COLORS["neutral"], DASH, pd_steady),
        ("Coherent, 4 speckles summed", pd_looks(s, 4), COLORS["purple_accent"], DASH, lambda x: pd_looks(x, 4)),
        ("Coherent, 1 speckle", pd_swerling1(s), COLORS["warm_accent"], DASH, pd_swerling1),
    ]
    lines.append(f"(fig 2) Poisson thresholds at P_FA = 1e-6 per bin: night k = {k_n}, bright sun (b = 2.2) k = {k_d}")
    for lab, pd, col, ls, fn in curves:
        ax.plot(s, pd, color=col, lw=LW, ls=ls, label=lab)
        s90 = s_for_pd(fn, 0.9)
        ax.plot([s90], [0.9], "o", ms=3.5, color=col, zorder=5)
        ax.text(s90 * 1.04, 0.875, f"{s90:.0f}", color=col, ha="left", va="top")
        lines.append(f"(fig 2) {lab}: n(P_D=0.5) = {s_for_pd(fn, 0.5):.1f}, n(P_D=0.9) = {s90:.1f}, "
                     f"P_D(25) = {fn(25.0):.3f}, P_D(30) = {fn(30.0):.3f}, P_D(50) = {fn(50.0):.3f}")
    ax.axhline(0.9, color=COLORS["annotation"], lw=REF_LW, ls=DASH, zorder=0)
    ax.text(1.1, 0.915, "$P_D=0.9$", color=COLORS["annotation"], va="bottom")
    for n_mark in (25, 30):
        ax.axvline(n_mark, color=COLORS["annotation"], lw=REF_LW, ls=":", zorder=0)
    ax.text(25 * 0.96, 0.02, "ToF\nmodel", color=COLORS["annotation"], ha="right", va="bottom")
    ax.text(30 * 1.04, 0.02, "FMCW\nmodel", color=COLORS["annotation"], ha="left", va="bottom")
    ax.set_xscale("log")
    ax.set_xlim(1, 400)
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 50, 100, 200]))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel(r"Mean signal photoelectrons per point, $\bar n$")
    ax.set_ylabel(r"Detection probability, $P_D$")
    ax.set_title(r"Detection at a false-alarm probability of $10^{-6}$ per range bin", loc="left")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.13), handlelength=2.2)
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def energy_axes(ax, title: str) -> None:
    for rr in (200, 300):
        ax.axhline(rr, color=COLORS["annotation"], lw=REF_LW, ls=":", zorder=0)
        ax.text(9.2, rr * 0.97, f"{rr} m", color=COLORS["annotation"], ha="right", va="top")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.01, 10)
    ax.set_ylim(10, 3000)
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_locator(FixedLocator([10, 30, 100, 300, 1000, 3000]))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel(r"Transmitted optical energy per point, $E_{\rm tx}$ (µJ)")
    top = ax.secondary_xaxis("top", functions=(lambda e: 1.0 / np.maximum(e, 1e-12),
                                               lambda n: 1.0 / np.maximum(n, 1e-12)))
    top.set_xlabel(r"Points per second per watt of light, $1/E_{\rm tx}$ (Mpts s$^{-1}$ W$^{-1}$)")
    top.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_title(title, loc="left")


def fig_scaling(out_stem: Path, lines: list) -> None:
    e_uj = np.logspace(-2, 1, 500)  # transmitted energy per point, µJ
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9), sharey=True, constrained_layout=True)
    spad, fm, apd = CASES["spad940"], CASES["fmcw1550"], CASES["apd1550"]

    ax = axes[0]
    for D, col in APERTURES:
        r = [r_max(lambda x: loss_dd(x, D, 940e-9), l_det(spad, e * 1e-6)) for e in e_uj]
        ax.plot(e_uj, r, color=col, lw=LW, label=f"SPAD 940 nm, $D={D * 1e3:.0f}$ mm")
    r = [r_max(lambda x: loss_dd(x, 25e-3, 1550e-9), l_det(apd, e * 1e-6)) for e in e_uj]
    ax.plot(e_uj, r, color=COLORS["brown_accent"], lw=LW, ls=DASH, label="Linear APD 1,550 nm, $D=25$ mm")
    ax.text(0.012, 1800, r"$R_{\max}\propto\sqrt{A\,E_{\rm tx}}$", ha="left", va="top")
    energy_axes(ax, "(a) Direct detection")
    ax.set_ylabel(r"Maximum range at 10% reflectance, $R_{\max}$ (m)")
    ax.legend(loc="lower right", handlelength=2.2)

    ax = axes[1]
    r = [r_max(lambda x: loss_dd(x, 25e-3, 940e-9), l_det(spad, e * 1e-6)) for e in e_uj]
    ax.plot(e_uj, r, color=COLORS["grey_accent"], lw=LW, alpha=0.4, label="SPAD 940 nm, 25 mm (ref.)")
    for D, col in APERTURES:
        r = np.array([r_max(lambda x: loss_coh(x, D, 1550e-9), l_det(fm, e * 1e-6)) for e in e_uj])
        ax.plot(e_uj, r, color=col, lw=LW, label=f"FMCW 1,550 nm, $D={D * 1e3:.0f}$ mm")
        e_min = fm["n_req"] * photon_energy(1550e-9) / (fm["eta"] * loss_coh(1e-3, D, 1550e-9))
        lines.append(f"(fig 3b) FMCW D = {D * 1e3:.0f} mm: minimum energy for any detection E_min = {e_min * 1e6:.3f} uJ")
    r = [r_max(lambda x: loss_coh_envelope(x, 1550e-9), l_det(fm, e * 1e-6)) for e in e_uj]
    ax.plot(e_uj, r, color=COLORS["neutral"], lw=LW, ls=DASHDOT, label="FMCW, best collimated $D$")
    ax.text(0.012, 1800, r"best $D$: $R_{\max}\propto E_{\rm tx}$", ha="left", va="top")
    energy_axes(ax, "(b) Coherent (FMCW), collimated monostatic beam")
    ax.legend(loc="lower right", handlelength=2.2)
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)

    for R0 in (100.0, 200.0, 300.0, 500.0):
        e_s = l_det(spad, 1.0) / loss_dd(R0, 25e-3, 940e-9)  # E such that L_det(E) = L(R0)
        e_a = l_det(apd, 1.0) / loss_dd(R0, 25e-3, 1550e-9)
        e_f = l_det(fm, 1.0) / loss_coh(R0, 25e-3, 1550e-9)
        e_f20 = l_det(fm, 1.0) / loss_coh(R0, 20e-3, 1550e-9)
        e_env = l_det(fm, 1.0) / loss_coh_envelope(R0, 1550e-9)
        e_s_dopt = l_det(spad, 1.0) / loss_dd(R0, d_opt(R0, 1550e-9), 940e-9)
        lines.append(f"(fig 3) E needed at {R0:.0f} m: SPAD 25 mm {e_s * 1e9:.1f} nJ; APD 25 mm {e_a * 1e9:.0f} nJ; "
                     f"FMCW 25 mm {e_f * 1e9:.0f} nJ; FMCW 20 mm {e_f20 * 1e9:.0f} nJ; FMCW best D "
                     f"({d_opt(R0, 1550e-9) * 1e3:.1f} mm) {e_env * 1e9:.0f} nJ; ratio best-D FMCW / SPAD 25 mm = "
                     f"{e_env / e_s:.2f}; SPAD with the same D_opt {e_s_dopt * 1e9:.1f} nJ, ratio {e_env / e_s_dopt:.2f}")


# ---------------------------------------------------------------- margin, fixed losses and fog (C0 subsection 10.6)
R_DESIGN = 200.0  # every design below reaches 200 m on a 10% target in clear air
MARGIN_DESIGNS = [
    # label, kind, aperture D (m), colour
    ("SPAD ToF 940 nm, 25 mm", "dd", 25e-3, COLORS["neutral"]),
    ("FMCW 1,550 nm, 25 mm", "coh", 25e-3, COLORS["primary"]),
    ("FMCW 1,550 nm, 22 mm (best for 200 m)", "coh", float(np.sqrt(1550e-9 * R_DESIGN / np.pi) / W0_OVER_D), COLORS["purple_accent"]),
    ("FMCW 1,550 nm, 13 mm", "coh", 13e-3, COLORS["teal_accent"]),
    ("FMCW 1,550 nm, 7 mm", "coh", 7e-3, COLORS["cool_accent"]),
]


def margin_design(kind: str, D: float) -> dict:
    """Energy per point that makes a design reach R_DESIGN at 10% in clear air, and its loss function."""
    if kind == "dd":
        case, lam = CASES["spad940"], 940e-9
        fn = lambda R, a, rho=RHO: loss_dd_alpha(R, D, a, rho)  # noqa: E731
    else:
        case, lam = CASES["fmcw1550"], 1550e-9
        fn = lambda R, a, rho=RHO: loss_coh_alpha(R, D, lam, a, rho)  # noqa: E731
    a_clear = kim_alpha(lam, 23.0)
    l_target = fn(R_DESIGN, a_clear)
    e_tx = case["n_req"] * photon_energy(lam) / (case["eta"] * l_target)
    return dict(fn=fn, lam=lam, l_det=l_target, e_tx=e_tx, a_clear=a_clear)


def range_or_zero(fn, target):
    r = r_max(fn, target)
    return 0.0 if not np.isfinite(r) else r


def fig_margin_weather(out_stem: Path, lines: list) -> None:
    x_db = np.linspace(0.0, 12.0, 241)  # extra fixed two-way loss (dB)
    vis = np.logspace(np.log10(0.05), np.log10(23.0), 260)  # visibility (km)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9), constrained_layout=True)

    lines.append(f"(fig 4) designs that reach {R_DESIGN:.0f} m at 10% in clear air:")
    for label, kind, D, col in MARGIN_DESIGNS:
        dz = margin_design(kind, D)
        fn, ld, a0 = dz["fn"], dz["l_det"], dz["a_clear"]
        e_str = f"{dz['e_tx'] * 1e9:.0f} nJ"
        r_x = [range_or_zero(lambda R: fn(R, a0), ld * 10 ** (x / 10)) for x in x_db]
        axes[0].plot(x_db, r_x, color=col, lw=LW, label=f"{label}, {e_str}")
        r_v = [range_or_zero(lambda R: fn(R, kim_alpha(dz["lam"], v)), ld) for v in vis]
        axes[1].plot(vis, np.maximum(r_v, 1e-3), color=col, lw=LW, label=f"{label}, {e_str}")
        margins = {R0: 10 * np.log10(fn(R0, a0) / ld) for R0 in (10.0, 20.0, 50.0, 100.0, 150.0)}
        darkest = RHO * ld / fn(0.5, a0)
        fixed = {x: range_or_zero(lambda R: fn(R, a0), ld * 10 ** (x / 10)) for x in (1, 2, 3, 6, 10)}
        fog = {v: range_or_zero(lambda R: fn(R, kim_alpha(dz["lam"], v)), ld) for v in (5, 2, 1, 0.5, 0.2, 0.1, 0.05)}
        lines.append(f"  {label}: D = {D * 1e3:.1f} mm, E_tx = {e_str}; margin "
                     + ", ".join(f"{R0:.0f} m {m:.1f} dB" for R0, m in margins.items())
                     + f"; darkest detectable {100 * darkest:.2f}%; range with extra loss "
                     + ", ".join(f"{x} dB {r:.0f} m" for x, r in fixed.items())
                     + "; fog reach " + ", ".join(f"V={v:g} km {r:.0f} m" for v, r in fog.items()))

    ax = axes[0]
    ax.axvline(1.9, color=COLORS["annotation"], lw=REF_LW, ls=":", zorder=0)
    ax.text(2.05, 214, "0.2 mm water film\n(1,550 nm only)", color=COLORS["annotation"], va="top", ha="left")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 220)
    ax.set_xlabel(r"Extra two-way loss, $X$ (dB)")
    ax.set_ylabel(r"Maximum range, $R_{\max}$ (m)")
    ax.set_title("(a) Fixed losses and dark targets", loc="left")
    top = ax.secondary_xaxis("top", functions=(lambda x: 10.0 * 10 ** (-np.asarray(x) / 10.0),
                                               lambda r: -10.0 * np.log10(np.maximum(np.asarray(r), 1e-9) / 10.0)))
    top.set_xticks([10, 5, 2, 1, 0.5])
    top.set_xticklabels(["10", "5", "2", "1", "0.5"])
    top.set_xlabel(r"Same as a clean window and a target of reflectance (%)")
    ax.legend(loc="upper right", handlelength=2.0)

    ax = axes[1]
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.05, 23)
    ax.set_ylim(2, 300)
    ax.xaxis.set_major_locator(FixedLocator([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_major_locator(FixedLocator([2, 5, 10, 20, 50, 100, 200]))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax.yaxis.set_minor_formatter(NullFormatter())
    for x0, x1, txt in ((0.05, 0.2, "dense fog"), (0.2, 1.0, "fog"), (1.0, 6.0, "haze"), (6.0, 23.0, "clear")):
        ax.axvspan(x0, x1, color=COLORS["highlight"] if txt in ("fog",) else "white",
                   alpha=HIGHLIGHT_ALPHA if txt == "fog" else 0.0, lw=0, zorder=0, label="_nolegend_")
        ax.text(np.sqrt(x0 * x1), 2.3, txt, color=COLORS["annotation"], ha="center", va="bottom")
    ax.set_xlabel(r"Meteorological visibility, $V$ (km)")
    ax.set_ylabel(r"Maximum range at 10% reflectance (m)")
    ax.set_title("(b) Fog (Kim model, single scattering)", loc="left")
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)

    # fog backscatter: per-bin clutter-to-target ratio, and the near-range fog return (lidar ratio 18 sr assumed)
    s_lidar, d_r = 18.0, 0.15
    for v in (0.2, 0.05):
        a = kim_alpha(1550e-9, v)
        beta = a / s_lidar
        a_rx = np.pi * 0.0125**2
        tgt_dd = RHO * a_rx / (np.pi * 50.0**2) * np.exp(-2 * a * 50.0)
        tgt_coh = loss_coh_alpha(50.0, 25e-3, 1550e-9, a)
        dd = {r: 10 * np.log10(beta * d_r * a_rx / r**2 * np.exp(-2 * a * r) / tgt_dd) for r in (2, 5, 10, 20)}
        coh = {}
        for r in (2, 5, 10, 20):
            w = beam_radius(r, 25e-3, 1550e-9)
            fog_bin = beta * d_r * (1550e-9) ** 2 * T_TRUNC**2 / (2 * np.pi * w**2) * np.exp(-2 * a * r)
            coh[r] = 10 * np.log10(fog_bin / tgt_coh)
        lines.append(f"(fig 4) fog V = {v * 1e3:.0f} m: alpha = {a * 1e3:.1f}/km, beta = alpha/18 sr = {beta:.2e} /m/sr; "
                     f"per-bin fog/target = pi*beta*dR/rho = {10 * np.log10(np.pi * beta * d_r / RHO):.1f} dB (both receivers); "
                     "fog in the bin at r vs a 10% target at 50 m: SPAD 25 mm "
                     + ", ".join(f"{r} m {x:+.1f} dB" for r, x in dd.items()) + "; FMCW 25 mm "
                     + ", ".join(f"{r} m {x:+.1f} dB" for r, x in coh.items()))


def main() -> None:
    configure_plot_style()
    here = OUT_DIR
    lines = [
        "Link budget tables (companion to C0 subsection 10) [E]",
        f"rho = {RHO}, w0 = {W0_OVER_D} D, truncation t = {T_TRUNC:.4f} (t^2 = {T_TRUNC ** 2:.4f}), P_FA = {P_FA:g} per bin",
    ]
    for lam in (905e-9, 940e-9, 1310e-9, 1550e-9):
        a = alpha_clear(lam)
        lines.append(f"clear air (V = 23 km) alpha({lam * 1e9:.0f} nm) = {a * 1e3:.4f} /km; two-way loss at 200 m = "
                     f"{4.343 * 2 * a * 200:.3f} dB, at 500 m = {4.343 * 2 * a * 500:.3f} dB; E_ph = {photon_energy(lam):.4e} J")
    for key, cs in CASES.items():
        lines.append(f"case {key}: n = {cs['n_req']}, eta = {cs['eta']:.3f}, E_tx = {cs['e_tx'] * 1e6:.2f} uJ, "
                     f"L_det = {l_det(cs):.3e} = {db(l_det(cs)):.2f} dB")
    for R0 in (10.0, 100.0, 200.0, 300.0, 500.0):
        parts = [f"R = {R0:.0f} m:"]
        for D in (10e-3, 25e-3, 50e-3):
            parts.append(f"DD{D * 1e3:.0f} {db(loss_dd(R0, D, 940e-9)):.1f} dB")
        for D in (10e-3, 20e-3, 25e-3, 50e-3):
            parts.append(f"coh{D * 1e3:.0f} {db(loss_coh(R0, D, 1550e-9)):.1f} dB (A_mode {a_mode(R0, D, 1550e-9) * 1e6:.1f} mm2)")
        parts.append(f"coh25@1310 {db(loss_coh(R0, 25e-3, 1310e-9)):.1f} dB")
        parts.append(f"env {db(loss_coh_envelope(R0, 1550e-9)):.1f} dB (D_opt {d_opt(R0, 1550e-9) * 1e3:.1f} mm)")
        lines.append("  ".join(parts))
    fig_loss(here / "link_budget_loss_vs_range", lines)
    fig_detection(here / "link_budget_detection_statistics", lines)
    fig_scaling(here / "link_budget_range_scaling", lines)
    fig_margin_weather(here / "link_budget_margin_weather", lines)
    (here / "link_budget_scaling_tables.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
