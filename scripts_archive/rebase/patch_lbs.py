"""Patch build/figures/link_budget_scaling.py: per-point detection rule, two-ramp FMCW statistics
(Figure C0.10b), and the four-look reading of the FMCW detection case.

Usage: python patch_lbs.py <path to link_budget_scaling.py> <output path>
"""
import sys
from pathlib import Path

src_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
src = src_path.read_text(encoding="utf-8")


def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, (old[:80], n)
    src = src.replace(old, new)


# ---- docstring
rep('''Detection statistics at a per-bin false-alarm probability P_FA:
  photon counting, Poisson background b per bin: threshold k = min{k : P(N >= k | b) <= P_FA},
      P_D = P(N >= k | s + b) = gammainc(k, s + b)
  coherent, steady target (square-law, one bin):  P_D = Q_1(sqrt(2 S), sqrt(-2 ln P_FA))
  coherent, one speckle (Rayleigh, Swerling I):   P_D = P_FA ** (1 / (1 + S))
  coherent, M speckles summed incoherently:       T_M = Qinv_gamma(M, P_FA),
      P_D = Q_gamma(M, T_M / (1 + S / M))           (S = total mean photoelectrons)
''',
'''Detection statistics (fig 2), one rule for both receivers: P_D = 0.9 per point with at most
P_FA_PT = 1e-3 false points per point over the whole 0-300 m search.
  photon counting, 2,000 bins of 1 ns, Poisson background b per bin: per-bin budget p = P_FA_PT / 2000,
      threshold k = min{k : P(N >= k | b) <= p},  P_D = P(N >= k | s + b) = gammainc(k, s + b)
  FMCW, peak found in both the up- and the down-ramp: the n photoelectrons split equally between
      the ramps, speckle common to both ramps, M looks summed incoherently in each ramp.  The
      up-ramp search covers N_B = 2,450 bins (400 MHz range beat + 90 MHz Doppler at 200 kHz) and
      the down-ramp window N_W = 1,800 bins (+-180 MHz); per-bin budget p = sqrt(P_FA_PT / (N_B N_W)).
      threshold x: Q_gamma(M, x) = p;  P_D = int [Q_M(sqrt(n S / M), sqrt(2 x))]^2 Gamma(S; M, 1) dS
      (steady target: P_D = Q_1(sqrt(n), sqrt(2 x))^2 with x = -ln p)
''')

# ---- the FMCW detection case is read per look
rep('''    "fmcw1550": dict(label="FMCW, 1,550 nm", lam=1550e-9, n_req=30.0, eta=0.25, e_tx=0.30e-6),''',
'''    # FMCW: four looks (two polarizations x two spatial modes), each collecting A_mode; the
    # 120 photoelectrons a point needs (section C0 subsection 10.3) are 30 per look, so the
    # detection level of one look, with n_req = 30, is that of the whole receiver.
    "fmcw1550": dict(label="FMCW, per look", lam=1550e-9, n_req=30.0, eta=0.25, e_tx=0.30e-6),''')

# ---- detection statistics
rep('''# ---------------------------------------------------------------- detection statistics
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
''',
'''# ---------------------------------------------------------------- detection statistics
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
''')
rep('''from scipy.optimize import brentq
from scipy.special import gammainc, gammaincc, gammainccinv
from scipy.stats import ncx2''',
'''from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gammainc, gammainccinv
from scipy.stats import gamma as gamma_dist
from scipy.stats import ncx2''')

# ---- figure C0.10b
old_start = src.index("def fig_detection(out_stem: Path, lines: list) -> None:")
old_end = src.index("def energy_axes(ax, title: str) -> None:")
new_fig = '''def fig_detection(out_stem: Path, lines: list) -> None:
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
    ax.text(25 * 1.04, 0.02, "ToF\\nmodel", color=COLORS["annotation"], ha="left", va="bottom")
    ax.text(120 * 1.04, 0.02, "FMCW\\nmodel", color=COLORS["annotation"], ha="left", va="bottom")
    ax.set_xscale("log")
    ax.set_xlim(1, 400)
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_locator(FixedLocator([1, 2, 5, 10, 20, 50, 100, 200]))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel(r"Mean signal photoelectrons per point, $\\bar n$")
    ax.set_ylabel(r"Detection probability, $P_D$")
    ax.set_title(r"Detection with $\\leq10^{-3}$ false points per point (0–300 m)", loc="left")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.15), handlelength=2.2, frameon=True,
              facecolor="white", edgecolor="none", framealpha=0.9)
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


'''
src = src[:old_start] + new_fig + src[old_end:]

# ---- table header
rep('''P_FA = {P_FA:g} per bin",''',
    '''{P_FA_PT:g} false points per point",''')

out_path.write_text(src, encoding="utf-8")
print("patched", out_path)
