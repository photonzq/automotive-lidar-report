from pathlib import Path

here = Path(__file__).parent
src = (here / "fmcw_tof_system_budget_orig.py").read_text(encoding="utf-8")


def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (old[:70], src.count(old))
    src = src.replace(old, new)


# ---- docstring
rep('''   - FMCW: A_eff = mode-equivalent collecting area of a 20 mm monostatic,
     collimated Gaussian (w0 = 0.45 D, truncation on Tx and Rx, one polarization),
     identical to coherent_mode_coverage.py; eta = common optical x detector x
     mixing efficiency *excluding* the mode/polarization factor already in A_mode.''',
'''   - FMCW: four receive looks per point (both polarizations x two spatial modes),
     each with its own coherent receiver, so A_eff = 4 x A_mode, where A_mode is the
     mode-equivalent collecting area of one polarization of a 20 mm monostatic,
     collimated Gaussian (w0 = 0.45 D, truncation on Tx and Rx), identical to
     coherent_mode_coverage.py; eta = common optical x detector x mixing efficiency
     *excluding* the mode/polarization factor already in A_mode.
   - n_req is set by detection statistics, with the same rule for both receivers: 90 %
     detection per point at 1e-3 false points per point, over the full range search.
     ToF (Poisson, bright-sun background of 2.87 counts per 1 ns bin) ideally needs
     17.3 counts; the central 25 is a x1.45 implementation margin.  FMCW (4 speckle
     looks, peak found in both the up- and the down-ramp, two-stage search) ideally
     needs 88.5 photoelectrons; a x1.36 margin gives 120, i.e. 30 per look (report
     section C0 subsection 10.3).''')
rep('''   - ToF (SPAD-SoC): event-driven.  Energy = fixed per-point overhead + (signal +
     background events) x energy per event (avalanche recharge + TDC/histogram).''',
'''   - ToF (SPAD-SoC): event-driven.  Energy = fixed per-point overhead + (signal +
     background events) x energy per event (avalanche recharge + TDC/histogram).
     Background: the background-rate equation of section C6(d) gives 5.93e8 counts/s
     per macro-pixel for a rho = 0.9 sunlit scene at PDE 0.3; it scales with PDE, and
     the central case takes half of the rho = 0.9 value.  The dead fraction follows the
     dead-time equation of section C6(d) (nine SPADs, 6 ns dead time, the state of the
     art: Sony IMX479 "approx. 6 ns", 3x3 SPADs per macro-pixel) at each background
     level.  Sony's passive recharge behaves paralyzably (its 60 Mcps count-rate
     ceiling is 1/(e tau)), so a SPAD is live only if no photon arrived in the last
     tau: live fraction exp(-r tau), with r the per-SPAD photon-detection rate.  The
     dead time removes signal photons as well as background, so the signal efficiency
     is optics x PDE x live fraction.
   - FMCW: each of the four looks digitizes and transforms its own beat, so the
     receiver electronics per point are four times those of one coherent receiver.''')

# ---- ToF scenarios: background from PDE, dead fraction computed
rep('''        e_fixed=(20e-9, 40e-9, 60e-9),
        bg_rate=(0.0, 3e8, 6e8),  # background counts/s per macro-pixel (night..bright)
        t_listen=20.8e-6, dead_frac=0.29, e_event=(4e-12, 5e-12, 7e-12),''',
'''        e_fixed=(20e-9, 40e-9, 60e-9),
        scene=(0.0, 0.5, 1.0),  # background as a share of the rho = 0.9 full-sun case
        t_listen=20.8e-6, e_event=(4e-12, 5e-12, 7e-12),''')
rep('''        e_fixed=(10e-9, 20e-9, 35e-9),
        bg_rate=(0.0, 3e8, 6e8),
        t_listen=20.8e-6, dead_frac=0.29, e_event=(2.5e-12, 3.5e-12, 5e-12),''',
'''        e_fixed=(10e-9, 20e-9, 35e-9),
        scene=(0.0, 0.5, 1.0),
        t_listen=20.8e-6, e_event=(2.5e-12, 3.5e-12, 5e-12),''')

# ---- FMCW scenarios
rep('''        lam=1550e-9, eta=(0.40, 0.25, 0.12), n_req=(20, 30, 45),
        wpe=(0.20, 0.15, 0.10),''',
'''        # Calibration check: evaluated for Waymo's own receiver (one look, 50 photons,
        # 250 m, 5 %), eta = 0.25 gives 1.35 uJ per point, inside their 0.83-1.67 uJ.
        lam=1550e-9, eta=(0.40, 0.25, 0.12), looks=4, n_req=(96, 120, 168),
        wpe=(0.20, 0.15, 0.10),''')
rep('''        lam=1550e-9, eta=(0.50, 0.40, 0.25), n_req=(20, 25, 30),
        wpe=(0.30, 0.22, 0.15),''',
'''        lam=1550e-9, eta=(0.50, 0.40, 0.25), looks=4, n_req=(96, 120, 144),
        wpe=(0.30, 0.22, 0.15),''')
rep('''P_OVERHEAD = 3.0  # W: scanner motor, system SoC, heaters, power conversion (both types)''',
'''P_OVERHEAD = 3.0  # W: scanner motor, system SoC, heaters, power conversion (both types)
BG_PER_PDE = 5.93e8 / 0.3  # counts/s per unit PDE, rho = 0.9 full-sun scene, section C6(d)
N_SPAD, TAU_DEAD = 9, 6e-9  # 3x3 macro-pixel and SPAD dead time (s), section C6(d)


def tof_background(s: dict, k: int) -> tuple:
    """Background count rate, dead fraction and background counts per 1 ns bin."""
    r_bg = BG_PER_PDE * s["pde"] * s["scene"][k]
    x = r_bg / N_SPAD * TAU_DEAD
    f_dead = 1 - np.exp(-x)  # paralyzable (passive recharge): live only if no photon in the last tau
    b_bin = r_bg * 1e-9 * 10 * (1 - f_dead)  # 10 shots of ~2 us accumulated per point
    return r_bg, f_dead, b_bin''')
rep('''    e_opt = s["n_req"][k] * photon_energy(s["lam"]) * np.pi * R_TARGET**2 / (
        RHO * a * s["optics"] * s["pde"]
    )
    e_laser = e_opt / s["wpe"][k]
    n_events = s["bg_rate"][k] * s["t_listen"] * (1 - s["dead_frac"]) + s["n_req"][k]
    e_elec = s["e_fixed"][k] + n_events * s["e_event"][k]
    return dict(e_opt=e_opt, e_laser=e_laser, e_elec=e_elec, e_total=e_laser + e_elec,
                n_events=n_events)''',
'''    r_bg, f_dead, b_bin = tof_background(s, k)
    # the dead time blinds a SPAD to signal photons as well as to sunlight: the signal
    # efficiency is optics x PDE x live fraction (1 - f_dead)
    e_opt = s["n_req"][k] * photon_energy(s["lam"]) * np.pi * R_TARGET**2 / (
        RHO * a * s["optics"] * s["pde"] * (1 - f_dead)
    )
    e_laser = e_opt / s["wpe"][k]
    n_events = r_bg * s["t_listen"] * (1 - f_dead) + s["n_req"][k]
    e_elec = s["e_fixed"][k] + n_events * s["e_event"][k]
    return dict(e_opt=e_opt, e_laser=e_laser, e_elec=e_elec, e_total=e_laser + e_elec,
                n_events=n_events, r_bg=r_bg, f_dead=f_dead, b_bin=b_bin)''')
rep('''    e_opt = s["n_req"][k] * photon_energy(s["lam"]) * np.pi * R_TARGET**2 / (
        RHO * a_mode * s["eta"][k]
    )
    e_laser = e_opt / s["wpe"][k]
    d = fmcw_digitization(s)
    e_sample = s["adc_fom"][k] * 2 ** s["enob"] + s["dsp_ops"] * s["e_op"][k]
    e_elec = d["n_samples"] * e_sample + s["p_analog"][k] * d["t_dwell"]''',
'''    e_opt = s["n_req"][k] * photon_energy(s["lam"]) * np.pi * R_TARGET**2 / (
        RHO * s["looks"] * a_mode * s["eta"][k]
    )
    e_laser = e_opt / s["wpe"][k]
    d = fmcw_digitization(s)
    e_sample = s["adc_fom"][k] * 2 ** s["enob"] + s["dsp_ops"] * s["e_op"][k]
    # each look has its own receiver: samples and analog power per point x looks
    e_elec = s["looks"] * (d["n_samples"] * e_sample + s["p_analog"][k] * d["t_dwell"])''')

# ---- tables
rep('''    lines.append(f"FMCW 20 mm monostatic Gaussian at {R_TARGET:.0f} m: A_mode = {a_mode*1e6:.1f} mm^2, "
                 f"spot radius w = {w*1e3:.1f} mm, 0.05 deg cell = {cell*1e3:.0f} mm, "
                 f"nominal 1/e^2 footprint fraction = {np.pi*w**2/cell**2*100:.1f} %")''',
'''    looks = FMCW["2026"]["looks"]
    lines.append(f"FMCW 20 mm monostatic Gaussian at {R_TARGET:.0f} m: A_mode = {a_mode*1e6:.1f} mm^2 per look, "
                 f"A_eff = {looks} looks x A_mode = {looks*a_mode*1e6:.0f} mm^2, "
                 f"spot radius w = {w*1e3:.1f} mm, 0.05 deg cell = {cell*1e3:.0f} mm, "
                 f"nominal 1/e^2 footprint fraction = {np.pi*w**2/cell**2*100:.1f} %")
    for yr in ("2026", "2032"):
        s = TOF[yr]
        bg = [tof_background(s, k) for k in range(3)]
        lines.append(f"ToF {yr} background (night / central / bright): r_bg = "
                     + " / ".join(f"{x[0]:.3g}" for x in bg) + " counts/s; dead fraction "
                     + " / ".join(f"{x[1]*100:.0f} %" for x in bg) + "; counts per 1 ns bin "
                     + " / ".join(f"{x[2]:.2f}" for x in bg))''')
rep('''    for yr in ("2026", "2032"):
        r = results[("FMCW", yr)]
        lines.append(f"  {yr}: energy per sample (ADC + DSP) = "
                     + " / ".join(f"{x['e_sample']*1e12:.0f}" for x in r) + " pJ")''',
'''    for yr in ("2026", "2032"):
        r = results[("FMCW", yr)]
        lines.append(f"  {yr}: energy per sample (ADC + DSP) = "
                     + " / ".join(f"{x['e_sample']*1e12:.0f}" for x in r) + " pJ; "
                     + f"{FMCW[yr]['looks']} receivers per point")''')
rep('''    lines.append("FMCW parallel channels and raw ADC data (10-bit samples), 2026 chirp")
    for rate in rates:
        n_ch = rate * d["t_dwell"]
        lines.append(f"  {rate/1e6:>4.0f} Mpts/s: {n_ch:>5.0f} channels at 10 us dwell ({rate*4e-6:>4.0f} at 4 us); "
                     f"raw data {n_ch*d['f_s']*10/1e12:.2f} Tb/s; "''',
'''    looks = FMCW["2026"]["looks"]
    lines.append(f"FMCW parallel channels (transmit beams, {looks} coherent receivers each) and raw ADC data "
                 "(10-bit samples, all receivers), 2026 chirp")
    for rate in rates:
        n_ch = rate * d["t_dwell"]
        lines.append(f"  {rate/1e6:>4.0f} Mpts/s: {n_ch:>5.0f} channels at 10 us dwell ({rate*4e-6:>4.0f} at 4 us), "
                     f"{looks*n_ch:.0f} receivers; "
                     f"raw data {looks*n_ch*d['f_s']*10/1e12:.2f} Tb/s; "''')
rep('''    lines.append(f"ToF 2026 central: events per point {tof['n_events']:.0f} (bright-sun background), "
                 f"optical power at 25 Mpts/s = {25e6*tof['e_opt']:.2f} W")''',
'''    lines.append(f"ToF 2026 central: events per point {tof['n_events']:.0f} (bright-sun background, "
                 f"dead fraction {tof['f_dead']*100:.0f} %, {tof['b_bin']:.2f} counts per bin), "
                 f"optical power at 25 Mpts/s = {25e6*tof['e_opt']:.2f} W")''')

# ---- figure (c) note and label
rep('''    note = ["raw 10-bit ADC data, 10 µs dwell:"]
    for r_mark in (2e6, 10e6, 25e6):
        n_ch = r_mark * 10e-6
        ax.plot(r_mark, n_ch, "o", color=COLORS["warm_accent"], ms=3.5, label="_nolegend_")
        note.append(f"{r_mark/1e6:.0f} Mpts/s: {n_ch:.0f} ch, {n_ch*f_s*10/1e12:.2g} Tb/s")''',
'''    looks = FMCW["2026"]["looks"]
    note = [f"{looks} receivers per channel;", "raw 10-bit ADC data, 10 µs dwell:"]
    for r_mark in (2e6, 10e6, 25e6):
        n_ch = r_mark * 10e-6
        ax.plot(r_mark, n_ch, "o", color=COLORS["warm_accent"], ms=3.5, label="_nolegend_")
        note.append(f"{r_mark/1e6:.0f} Mpts/s: {n_ch:.0f} ch, {looks*n_ch*f_s*10/1e12:.2g} Tb/s")''')
rep('''    ax.set_ylabel("Parallel coherent channels")''', '''    ax.set_ylabel("Parallel coherent channels (beams)")''')

# ---- label placement: no label crosses a curve (product ranges are listed in the caption)
rep('''    ax.text(6.2e5, 26.5, "typical 8–25 W envelope", color=COLORS["annotation"], va="bottom")''',
'''    ax.text(6.2e5, 26.5, "typical 8–25 W", color=COLORS["annotation"], va="bottom")''')
rep('''        (3.84e6, 8.0, "ATX, 230 m", COLORS["primary"], "s", (-52, 4)),
        (15.0e6, 13.0, "ETX, 300 m", COLORS["primary"], "s", (-14, -15)),
        (1.5e6, 45.0, "LuminWave F1, 250 m", COLORS["warm_accent"], "^", (-30, 7)),
    ]
    for x_p, y_p, lab, col, mk, off in products:
        ax.plot(x_p, y_p, mk, color=col, mfc="white", mew=1.2, ms=5, label="_nolegend_", zorder=5)
        ax.annotate(lab, (x_p, y_p), xytext=off, textcoords="offset points", color=col)''',
'''        (3.84e6, 8.0, "ATX", COLORS["primary"], "s", (6, 0), "left", "center"),
        (15.0e6, 13.0, "ETX", COLORS["primary"], "s", (0, 5), "center", "bottom"),
        (1.5e6, 45.0, "LuminWave F1", COLORS["warm_accent"], "^", (0, 5), "center", "bottom"),
    ]
    for x_p, y_p, lab, col, mk, off, ha, va in products:
        ax.plot(x_p, y_p, mk, color=col, mfc="white", mew=1.2, ms=5, label="_nolegend_", zorder=5)
        ax.annotate(lab, (x_p, y_p), xytext=off, textcoords="offset points", color=col,
                    ha=ha, va=va)''')
rep('''    ax.set_ylim(1, 3000)''', '''    ax.set_ylim(1, 1e4)''')
rep('''    ax.text(6e5, 2200, "\\n".join(note), color=COLORS["annotation"], va="top")''',
    '''    ax.text(6e5, 7000, "\\n".join(note), color=COLORS["annotation"], va="top")''')

(here / "fmcw_tof_system_budget.py").write_text(src, encoding="utf-8")
print("patched")
