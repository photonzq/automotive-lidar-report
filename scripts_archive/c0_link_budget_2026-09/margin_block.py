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
    for x0, x1, txt in ((0.05, 0.2, "thick\nfog"), (0.2, 1.0, "fog"), (1.0, 4.0, "thin fog,\nhaze"),
                        (4.0, 23.0, "light haze,\nclear")):
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
    ax_c.axvspan(10, 50, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, zorder=0, label="_nolegend_")
    for x0, x1, txt in ((1.0, 2.5, "light"), (2.5, 10.0, "moderate"), (10.0, 50.0, "heavy"), (50.0, 150.0, "violent")):
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
