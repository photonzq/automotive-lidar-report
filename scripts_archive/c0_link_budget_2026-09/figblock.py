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
        ax.text(11, lvl + (0.6 if above else -0.6),
                f"{cs['label']}: $\\bar n={cs['n_req']:.0f}$, $E_{{\\rm tx}}={e_str}$ µJ",
                color=COLORS["neutral"], va="bottom" if above else "top", ha="left", bbox=LABEL_BOX, zorder=3)
        rm = r_max(lambda r: loss_dd(r, 25e-3, cs["lam"]), l_det(cs))
        ax.plot([rm], [lvl], "o", ms=4, color=COLORS["primary"], zorder=5)
        ax.annotate(f"{rm:.0f} m", xy=(rm, lvl), xytext=(rm * 1.12, lvl + (4.5 if above else -4.5)),
                    color=COLORS["primary"], ha="left", va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color=COLORS["annotation"], lw=0.6))
        lines.append(f"(fig 1a) {cs['label']}: L_det = {lvl:.1f} dB; R_max = "
                     f"{r_max(lambda r: loss_dd(r, 10e-3, cs['lam']), l_det(cs)):.0f} / {rm:.0f} / "
                     f"{r_max(lambda r: loss_dd(r, 50e-3, cs['lam']), l_det(cs)):.0f} m for D = 10 / 25 / 50 mm")
    ax.text(0.97, 0.04, r"$\mathcal{L}_{\rm DD}=\rho D^{2}T^{2}/(4R^{2})$", transform=ax.transAxes,
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
            color=COLORS["neutral"], va="bottom", ha="left", bbox=LABEL_BOX, zorder=3)
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
    ax.text(0.03, 0.96, r"$\mathcal{L}_{\rm coh}=\rho t^{2}\lambda^{2}T^{2}/(2\pi^{2}w(R)^{2})$",
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
