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

Detection statistics (fig 2), one rule for both receivers: P_D = 0.9 per point with at most
P_FA_PT = 1e-3 false points per point over the whole 0-300 m search.
  photon counting, 2,000 bins of 1 ns, Poisson background b per bin: per-bin budget p = P_FA_PT / 2000,
      threshold k = min{k : P(N >= k | b) <= p},  P_D = P(N >= k | s + b) = gammainc(k, s + b)
  FMCW, peak found in both the up- and the down-ramp: the n photoelectrons split equally between
      the ramps, speckle common to both ramps, M looks summed incoherently in each ramp.  The
      up-ramp search covers N_B = 2,450 bins (400 MHz range beat + 90 MHz Doppler at 200 kHz) and
      the down-ramp window N_W = 1,800 bins (+-180 MHz); per-bin budget p = sqrt(P_FA_PT / (N_B N_W)).
      threshold x: Q_gamma(M, x) = p;  P_D = int [Q_M(sqrt(n S / M), sqrt(2 x))]^2 Gamma(S; M, 1) dS
      (steady target: P_D = Q_1(sqrt(n), sqrt(2 x))^2 with x = -ln p)

Margin and weather (fig 4): every design gets just enough energy per point to reach 200 m on a 10%
target in clear air, then meets
  a fixed extra two-way loss X (dirty or wet window, darker target: X = 10 log10(0.1 / rho)),
  fog and haze (Kim model extinction alpha(V, lambda), both ways),
  rain (Carbonneau law, 1.076 R_r^0.67 dB/km, both ways; wavelength-independent),
  heavy rain plus a water film on the window (9.4 dB per mm round trip at 1,550 nm; neglected at 940 nm).
It also tabulates the fog backscatter clutter (lidar ratio 18 sr) for direct and coherent detection.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, LogFormatterMathtext, NullFormatter
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammainc, gammainccinv
from scipy.stats import gamma as gamma_dist
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
    # FMCW: four looks (two polarizations x two spatial modes), each collecting A_mode; the
    # 120 photoelectrons a point needs (section C0 subsection 10.3) are 30 per look, so the
    # detection level of one look, with n_req = 30, is that of the whole receiver.
    "fmcw1550": dict(label="FMCW, per look", lam=1550e-9, n_req=30.0, eta=0.25, e_tx=0.30e-6),
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
    with np.errstate(divide="ignore"):  # exp(-2 alpha R) underflows at r_hi in dense fog
        return brentq(lambda r: np.log(loss_fn(r)) - np.log(target), r_lo, r_hi, xtol=1e-6)


def db(x):
    return -10.0 * np.log10(x)  # loss in positive dB


# ---------------------------------------------------------------- detection statistics
P_FA_PT = 1e-3  # false points per point, over the whole 0-300 m search (both receivers)
N_BINS_TOF = 2000  # 1 ns histogram bins over 0-300 m
N_B, N_W = 2450, 1800  # FMCW up-ramp search bins and down-ramp window bins (200 kHz bins)
P_FA = P_FA_PT / N_BINS_TOF  # per-bin false-alarm probability of the ToF histogram
P_RAMP = np.sqrt(P_FA_PT / (N_B * N_W))  # per-bin false-alarm probability in each FMCW ramp
B_SUN = 2.94  # ToF bright-sun background per 1 ns bin (section C0 subsection 10.3)


def pd_poisson(s, b, p_fa=P_FA):
    k = 1
    while gammainc(k, b) > p_fa:  # P(N >= k | b)
        k += 1
    return gammainc(k, s + b), k


def pd_two_ramp(n, m=0, p=P_RAMP):
    """FMCW point detected in both ramps: n photoelectrons in total, split equally between the
    ramps; m looks summed incoherently per ramp (m = 0: steady target); speckle common to both."""
    n = np.atleast_1d(np.asarray(n, dtype=float))
    if m == 0:
        return ncx2.sf(2.0 * (-np.log(p)), df=2, nc=n) ** 2
    x = gammainccinv(m, p)
    out = [quad(lambda g: ncx2.sf(2.0 * x, df=2 * m, nc=nn * g / m) ** 2 * gamma_dist.pdf(g, m),
                0.0, np.inf, limit=400)[0] for nn in n]
    return np.array(out)


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
    s = np.logspace(0, np.log10(400), 300)
    fig, ax = plt.subplots(figsize=(4.6, 3.4), constrained_layout=True)
    pd_n, k_n = pd_poisson(s, 0.01)
    pd_d, k_d = pd_poisson(s, B_SUN)
    curves = [
        ("Counting, night", pd_n, COLORS["cool_accent"], "-", lambda x: pd_poisson(x, 0.01)[0]),
        ("Counting, bright sun", pd_d, COLORS["primary"], "-", lambda x: pd_poisson(x, B_SUN)[0]),
        ("FMCW, steady", pd_two_ramp(s, 0), COLORS["neutral"], DASH, lambda x: pd_two_ramp(x, 0)[0]),
        ("FMCW, 4 looks", pd_two_ramp(s, 4), COLORS["purple_accent"], DASH, lambda x: pd_two_ramp(x, 4)[0]),
        ("FMCW, 1 look", pd_two_ramp(s, 1), COLORS["warm_accent"], DASH, lambda x: pd_two_ramp(x, 1)[0]),
    ]
    lines.append(f"(fig 2) per-point rule: {P_FA_PT:g} false points per point; ToF p = {P_FA:.1e} per bin over "
                 f"{N_BINS_TOF} bins, thresholds night k = {k_n}, bright sun (b = {B_SUN}) k = {k_d}; FMCW "
                 f"p = {P_RAMP:.2e} per bin per ramp over N_B = {N_B} and N_W = {N_W}, thresholds x = "
                 f"{-np.log(P_RAMP):.2f} (1 look), {gammainccinv(4, P_RAMP):.2f} (4 looks)")
    for lab, pd, col, ls, fn in curves:
        ax.plot(s, pd, color=col, lw=LW, ls=ls, label=lab)
        s90 = s_for_pd(fn, 0.9)
        ax.plot([s90], [0.9], "o", ms=3.5, color=col, zorder=5)
        ax.text(s90 * 1.04, 0.875, f"{s90:.1f}" if s90 < 100 else f"{s90:.0f}", color=col, ha="left", va="top")
        lines.append(f"(fig 2) {lab}: n(P_D=0.5) = {s_for_pd(fn, 0.5):.1f}, n(P_D=0.9) = {s90:.1f}, "
                     f"P_D(25) = {fn(25.0):.3f}, P_D(120) = {fn(120.0):.3f}")
    for m in (2, 8):
        fn = lambda x, m=m: pd_two_ramp(x, m)[0]
        lines.append(f"(fig 2) FMCW, {m} looks summed (not plotted): n(P_D=0.5) = {s_for_pd(fn, 0.5):.1f}, "
                     f"n(P_D=0.9) = {s_for_pd(fn, 0.9):.1f}, P_D(120) = {fn(120.0):.3f}")
    ax.axhline(0.9, color=COLORS["annotation"], lw=REF_LW, ls=DASH, zorder=0)
    ax.text(1.1, 0.915, "$P_D=0.9$", color=COLORS["annotation"], va="bottom")
    for n_mark in (25, 120):  # stop below the P_D = 0.9 labels
        ax.axvline(n_mark, ymax=0.8, color=COLORS["annotation"], lw=REF_LW, ls=":", zorder=0)
    ax.text(25 * 1.04, 0.02, "ToF\nmodel", color=COLORS["annotation"], ha="left", va="bottom")
    ax.text(120 * 1.04, 0.02, "FMCW\nmodel", color=COLORS["annotation"], ha="left", va="bottom")
    ax.set_xscale("log")
    ax.set_xlim(1, 400)
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 50, 100, 200]))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel(r"Mean signal photoelectrons per point, $\bar n$")
    ax.set_ylabel(r"Detection probability, $P_D$")
    ax.set_title(r"Detection with $\leq10^{-3}$ false points per point (0–300 m)", loc="left")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.15), handlelength=2.2, frameon=True,
              facecolor="white", edgecolor="none", framealpha=0.9)
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


# ---------------------------------------------------------------- margin, fixed losses, fog and rain (C0 subsection 10.6)
R_DESIGN = 200.0  # every design below reaches 200 m on a 10% target in clear air
TOF_STYLE = dict(color=COLORS["warm_accent"], ls=DASH, zorder=4)  # ToF: the reference, warm and dashed, drawn on top
MARGIN_DESIGNS = [
    # label, kind, aperture D (m), colour, drawn in Figure C0.10d (the others are table rows only)
    ("SPAD ToF, 940 nm, $D=25$ mm lens", "dd", 25e-3, COLORS["warm_accent"], True),
    ("FMCW, 1,550 nm, $D=25$ mm", "coh", 25e-3, COLORS["primary"], True),
    ("FMCW, $D=22$ mm (best for 200 m)", "coh", float(np.sqrt(1550e-9 * R_DESIGN / np.pi) / W0_OVER_D),
     COLORS["purple_accent"], True),
    ("FMCW, $D=16$ mm", "coh", 16e-3, None, False),
    ("FMCW, $D=13$ mm", "coh", 13e-3, COLORS["teal_accent"], True),
    ("FMCW, $D=10$ mm", "coh", 10e-3, None, False),
    ("FMCW, $D=7$ mm", "coh", 7e-3, COLORS["cool_accent"], True),
]
S_LIDAR = 18.0  # fog lidar ratio alpha/beta (sr), typical of water droplets [E]
BIN_M = 0.15  # range bin: 1 ns of ToF, or c/2B for a 1 GHz FMCW chirp
FILM_DB_PER_MM = 9.4  # two-way loss of a water film on the window at 1,550 nm (report section C4c)
# At 940 nm liquid water absorbs tens of times more weakly, so the film is neglected for the ToF design.
RAIN_FOR_FILM = 25.0  # mm/h ("heavy" rain) for panel (d)


def rain_alpha(rate_mm_h: float) -> float:
    """Rain extinction (1/m) from the Carbonneau free-space-optics law, 1.076 R^0.67 dB/km (subsection 8)."""
    gamma_db_per_km = 1.076 * rate_mm_h**0.67
    return gamma_db_per_km / (10.0 * np.log10(np.e)) / 1e3


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
    film = 0.0 if kind == "dd" else FILM_DB_PER_MM
    return dict(fn=fn, lam=lam, l_det=l_target, e_tx=e_tx, a_clear=a_clear, film_db_per_mm=film)


def range_or_zero(fn, target):
    r = r_max(fn, target)
    return 0.0 if not np.isfinite(r) else r


def reach(dz: dict, alpha_extra: float = 0.0, x_db: float = 0.0, a_base: float | None = None) -> float:
    """Maximum range of a design with extra extinction alpha_extra (1/m) and an extra fixed loss x_db (dB)."""
    a = (dz["a_clear"] if a_base is None else a_base) + alpha_extra
    return range_or_zero(lambda R: dz["fn"](R, a), dz["l_det"] * 10 ** (x_db / 10))


def plain(label: str) -> str:
    return label.replace("$D=", "D = ").replace("$", "")


def fog_bin_ratio(kind: str, D: float, r: float, r_t: float, alpha: float) -> float:
    """Fog return in the range bin at r, relative to the echo of a 10% target at r_t (same design, same fog).

    Fog slab: backscatter beta*dR per sr; Lambertian target: rho/pi per sr. Both are collected through the
    receiver's geometry at their own range: A_rx/r^2 for direct detection (full overlap assumed), and
    A_mode(r)/r^2 = t^2 lambda^2 / (2 pi w(r)^2) for the coherent receiver. Spherical droplets keep the
    polarization, so all of the fog return is in the LO's polarization, while the model's depolarizing target
    puts only half of its return there: the coherent ratio carries an extra factor 2."""
    beta = alpha / S_LIDAR
    if kind == "dd":
        geom, pol = (r_t / r) ** 2, 1.0
    else:
        geom, pol = (beam_radius(r_t, D, 1550e-9) / beam_radius(r, D, 1550e-9)) ** 2, 2.0
    return pol * np.pi * beta * BIN_M / RHO * geom * np.exp(2.0 * alpha * (r_t - r))


def style_for(kind: str, col: str) -> dict:
    return dict(TOF_STYLE) if kind == "dd" else dict(color=col, ls="-", zorder=3)


def range_axis_linear(ax) -> None:
    ax.set_ylim(0, 220)
    ax.yaxis.set_major_locator(FixedLocator([0, 50, 100, 150, 200]))
    ax.set_ylabel(r"Maximum range at 10% reflectance, $R_{\max}$ (m)")


def fig_margin_weather(out_stem: Path, lines: list) -> None:
    x_db = np.linspace(0.0, 12.0, 241)  # extra fixed two-way loss (dB)
    vis = np.logspace(np.log10(0.05), np.log10(23.0), 260)  # visibility (km)
    rain = np.logspace(0.0, np.log10(150.0), 200)  # rain rate (mm/h)
    film = np.linspace(0.0, 0.5, 201)  # water film on the window (mm)
    fig, axs = plt.subplots(2, 2, figsize=(8.4, 7.3), constrained_layout=True)
    ax_a, ax_b, ax_c, ax_d = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]

    lines.append(f"(fig 4) designs that reach {R_DESIGN:.0f} m at 10% in clear air (rows marked * are drawn):")
    e_best = margin_design("coh", MARGIN_DESIGNS[2][2])["e_tx"]
    for label, kind, D, col, drawn in MARGIN_DESIGNS:
        dz = margin_design(kind, D)
        fn, ld, a0 = dz["fn"], dz["l_det"], dz["a_clear"]
        e_str = f"{dz['e_tx'] * 1e9:,.0f} nJ"
        if drawn:
            st = style_for(kind, col)
            ax_a.plot(x_db, [reach(dz, x_db=x) for x in x_db], lw=LW, label=f"{label}: {e_str} per point", **st)
            r_v = [reach(dz, a_base=kim_alpha(dz["lam"], v)) for v in vis]
            ax_b.plot(vis, np.maximum(r_v, 1e-3), lw=LW, label="_nolegend_", **st)
            ax_c.plot(rain, [reach(dz, alpha_extra=rain_alpha(rr)) for rr in rain], lw=LW, label="_nolegend_", **st)
            ax_d.plot(film, [reach(dz, alpha_extra=rain_alpha(RAIN_FOR_FILM), x_db=dz["film_db_per_mm"] * f)
                             for f in film], lw=LW, label="_nolegend_", **st)
        margins = {R0: 10 * np.log10(fn(R0, a0) / ld) for R0 in (10.0, 20.0, 50.0, 100.0, 150.0)}
        darkest = RHO * ld / fn(0.5, a0)
        fixed = {x: reach(dz, x_db=x) for x in (1, 1.9, 2, 3, 6, 10)}
        fog = {v: reach(dz, a_base=kim_alpha(dz["lam"], v)) for v in (5, 2, 1, 0.5, 0.2, 0.1, 0.05)}
        if kind == "coh":
            z_r = np.pi * (W0_OVER_D * D) ** 2 / 1550e-9
            u = z_r / R_DESIGN
            extra = (f"z_R = {z_r:.0f} m, u = z_R/R0 = {u:.3f}, plateau margin 10log10(1+1/u^2) = "
                     f"{10 * np.log10(1 + 1 / u**2):.2f} dB, energy vs best aperture (u+1/u)/2 = {(u + 1 / u) / 2:.3f} "
                     f"(script ratio {dz['e_tx'] / e_best:.3f}); ")
        else:
            extra = f"darkest at 10 m {100 * RHO * ld / fn(10.0, a0):.3f}%; "
        lines.append(f"  {'*' if drawn else ' '} {plain(label)}: D = {D * 1e3:.1f} mm, E_tx = {e_str}; {extra}margin "
                     + ", ".join(f"{R0:.0f} m {m:.1f} dB" for R0, m in margins.items())
                     + f"; darkest detectable (any range) {100 * darkest:.2f}%; range with extra loss "
                     + ", ".join(f"{x:g} dB {r:.0f} m" for x, r in fixed.items())
                     + "; fog reach " + ", ".join(f"V={v:g} km {r:.0f} m" for v, r in fog.items()))
        rain_clean = {rr: reach(dz, alpha_extra=rain_alpha(rr)) for rr in (5.0, 25.0, 100.0)}
        rain_wet = {(rr, f): reach(dz, alpha_extra=rain_alpha(rr), x_db=dz["film_db_per_mm"] * f)
                    for rr in (5.0, 25.0, 100.0) for f in (0.1, 0.2)}
        lines.append(f"      rain, clean window: " + ", ".join(f"{rr:g} mm/h {r:.0f} m" for rr, r in rain_clean.items())
                     + "; with a water film: " + ", ".join(f"{rr:g} mm/h + {f:g} mm {r:.0f} m"
                                                           for (rr, f), r in rain_wet.items()))

    # (a) fixed extra loss
    ax_a.axvline(1.9, color=COLORS["annotation"], lw=REF_LW, ls=":", zorder=0)
    ax_a.text(2.1, 214, "0.2 mm water film on the window\n(1,550 nm; negligible at 940 nm)", color=COLORS["annotation"],
              va="top", ha="left")
    ax_a.set_xlim(0, 12)
    range_axis_linear(ax_a)
    ax_a.set_xlabel(r"Extra two-way loss, $X$ (dB)")
    ax_a.set_title("(a) A fixed extra loss: dirty window, darker target", loc="left")
    top = ax_a.secondary_xaxis("top", functions=(lambda x: 10.0 * 10 ** (-np.asarray(x) / 10.0),
                                                 lambda r: -10.0 * np.log10(np.maximum(np.asarray(r), 1e-9) / 10.0)))
    top.set_xticks([10, 5, 2, 1])
    top.set_xticklabels(["10", "5", "2", "1"])
    top.set_xlabel(r"Same loss as a darker target behind a clean window: reflectance $\rho$ (%)")

    # (b) fog
    ax_b.set_xscale("log")
    ax_b.set_yscale("log")
    ax_b.set_xlim(0.05, 23)
    ax_b.set_ylim(2, 300)
    ax_b.xaxis.set_major_locator(FixedLocator([0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]))
    ax_b.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax_b.xaxis.set_minor_formatter(NullFormatter())
    ax_b.yaxis.set_major_locator(FixedLocator([2, 5, 10, 20, 50, 100, 200]))
    ax_b.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax_b.yaxis.set_minor_formatter(NullFormatter())
    ax_b.axvspan(0.2, 1.0, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, zorder=0, label="_nolegend_")
    # fog is visibility below 1 km: thick fog 50-200 m, moderate to light fog 200 m - 1 km (international visibility code)
    for x0, x1, txt in ((0.05, 0.2, "thick\nfog"), (0.2, 1.0, "fog"), (1.0, 10.0, "mist,\nhaze"), (10.0, 23.0, "clear")):
        ax_b.text(np.sqrt(x0 * x1), 2.25, txt, color=COLORS["annotation"], ha="center", va="bottom")
    ax_b.set_xlabel(r"Meteorological visibility, $V$ (km)")
    ax_b.set_ylabel(r"Maximum range at 10% reflectance, $R_{\max}$ (m)")
    ax_b.set_title("(b) Fog and haze: two-way extinction (Kim model)", loc="left")

    # (c) rain, clean window
    ax_c.set_xscale("log")
    ax_c.set_xlim(1, 150)
    ax_c.xaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 50, 100]))
    ax_c.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
    ax_c.xaxis.set_minor_formatter(NullFormatter())
    range_axis_linear(ax_c)
    # rain classes of MANOBS and the AMS glossary (0.1 and 0.3 in/h), violent above 50 mm/h; WMO has no agreed definition
    ax_c.axvspan(7.6, 50, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, zorder=0, label="_nolegend_")
    for x0, x1, txt in ((1.0, 2.5, "light"), (2.5, 7.6, "moderate"), (7.6, 50.0, "heavy"), (50.0, 150.0, "violent")):
        ax_c.text(np.sqrt(x0 * x1), 6, txt, color=COLORS["annotation"], ha="center", va="bottom")
    ax_c.set_xlabel(r"Rain rate, $R_r$ (mm/h)")
    ax_c.set_title("(c) Rain, clean window: 1.076 $R_r^{0.67}$ dB/km", loc="left")

    # (d) heavy rain with a water film on the window
    ax_d.set_xlim(0, 0.5)
    range_axis_linear(ax_d)
    for f0 in (0.1, 0.2):
        ax_d.axvline(f0, color=COLORS["annotation"], lw=REF_LW, ls=":", zorder=0)
        ax_d.text(f0 + 0.006, 214, f"{f0:g} mm", color=COLORS["annotation"], va="top", ha="left")
    ax_d.set_xlabel("Water film on the window (mm)")
    ax_d.set_title(f"(d) Heavy rain ({RAIN_FOR_FILM:.0f} mm/h) and a wet window", loc="left")
    top = ax_d.secondary_xaxis("top", functions=(lambda f: FILM_DB_PER_MM * np.asarray(f),
                                                 lambda x: np.asarray(x) / FILM_DB_PER_MM))
    top.set_xticks([0, 1, 2, 3, 4])
    top.set_xlabel("Two-way film loss at 1,550 nm (dB)")

    handles, labels = ax_a.get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside lower center", ncol=3, handlelength=2.6, columnspacing=1.6,
               title=f"Each design's energy per point is set so that it reaches {R_DESIGN:.0f} m on a 10% target "
                     "in clear air")
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)

    # rain: two-way loss per 100 m for the table
    lines.append("(fig 4) rain (Carbonneau): " + ", ".join(
        f"{rr:g} mm/h {1.076 * rr**0.67:.1f} dB/km, two-way at 100 m {2 * 0.1 * 1.076 * rr**0.67:.2f} dB"
        for rr in (2.5, 5.0, 10.0, 25.0, 50.0, 100.0)))
    # fog backscatter: per-bin clutter-to-target ratio at the target's own range, and the near-range fog return
    for v, r_t in ((0.2, 50.0), (0.05, 20.0)):
        a = kim_alpha(1550e-9, v)
        beta = a / S_LIDAR
        parts = []
        for label, kind, D, _, _ in (MARGIN_DESIGNS[0], MARGIN_DESIGNS[6], MARGIN_DESIGNS[4], MARGIN_DESIGNS[1]):
            dz = margin_design(kind, D)
            r_reach = reach(dz, a_base=kim_alpha(dz["lam"], v))
            vals = ", ".join(f"{r:g} m {10 * np.log10(fog_bin_ratio(kind, D, r, r_t, a)):+.1f} dB" for r in (2, 5, 10, 20)
                             if r < r_t)
            parts.append(f"{plain(label)} (reach {r_reach:.0f} m): {vals}")
        lines.append(f"(fig 4) fog V = {v * 1e3:.0f} m: alpha = {a * 1e3:.1f}/km (q = 0, same at 940 nm), "
                     f"beta = alpha/{S_LIDAR:.0f} sr = {beta:.2e} /m/sr; per-bin fog/target at the target's own range "
                     f"= pi*beta*dR/rho = {10 * np.log10(np.pi * beta * BIN_M / RHO):.1f} dB (direct detection), "
                     f"2*pi*beta*dR/rho = {10 * np.log10(2 * np.pi * beta * BIN_M / RHO):.1f} dB (coherent); "
                     f"fog in the bin at r vs a 10% target at {r_t:.0f} m: " + "; ".join(parts))
    # the fog summed over all bins between 20 m and a 50 m target, V = 200 m (direct detection)
    a = kim_alpha(1550e-9, 0.2)
    r_grid = np.arange(20.0, 50.0, BIN_M)
    total = sum(fog_bin_ratio("dd", 25e-3, r, 50.0, a) for r in r_grid)
    lines.append(f"(fig 4) V = 200 m, SPAD 25 mm: fog summed over the {len(r_grid)} bins from 20 to 50 m = "
                 f"{total:.1f} x the echo of a 10% target at 50 m")


def main() -> None:
    configure_plot_style()
    here = OUT_DIR
    lines = [
        "Link budget tables (companion to C0 subsection 10) [E]",
        f"rho = {RHO}, w0 = {W0_OVER_D} D, truncation t = {T_TRUNC:.4f} (t^2 = {T_TRUNC ** 2:.4f}), {P_FA_PT:g} false points per point",
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
