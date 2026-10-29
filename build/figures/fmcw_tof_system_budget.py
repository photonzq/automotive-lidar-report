"""FMCW (coherent) vs direct-detection ToF lidar: energy per point, digitization
load, parallel-channel count and sensor power versus point rate.

Companion to section C7a of automotive_perception_report_2026-09-27.md.
All outputs are order-of-magnitude engineering estimates [E], not product data.

Model (see the note for the reasoning and for what each parameter stands for):

1. Optical energy per point, extended Lambertian target that fills the sample:
       E_opt = n_req * E_ph * pi R^2 / (rho * A_eff * eta)
   - ToF: A_eff = hard receive aperture (25 mm), eta = optics (0.5) x SPAD PDE.
     The pixel integrates the whole cell (many speckle modes), section C10.3a.
   - FMCW: four receive looks per point (both polarizations x two spatial modes),
     each with its own coherent receiver, so A_eff = 4 x A_mode, where A_mode is the
     mode-equivalent collecting area of one polarization of a 20 mm monostatic,
     collimated Gaussian (w0 = 0.45 D, truncation on Tx and Rx), identical to
     coherent_mode_coverage.py; eta = common optical x detector x mixing efficiency
     *excluding* the mode/polarization factor already in A_mode.
   - n_req is set by detection statistics, with the same rule for both receivers: 90 %
     detection per point at 1e-3 false points per point, over the full range search.
     ToF (Poisson, central bright-sun background of 1.62 counts per 1 ns bin) ideally
     needs 15.0 counts; n_req keeps the x1.45 implementation margin of the central case
     (21.7 counts in 2026), with the low and high cases scaled alike.  FMCW (4 speckle
     looks, peak found in both the up- and the down-ramp, two-stage search) ideally
     needs 88.5 photoelectrons; a x1.36 margin gives 120, i.e. 30 per look (report
     section C0 subsection 10.3).
     The FMCW sample is sparse: its 1/e^2 footprint covers about 2 % of a 0.05 deg
     grid cell at 200 m.  The comparison is per *sample*, not per equal coverage.
2. Laser electrical energy = E_opt / wall-plug efficiency (source + driver/SOA).
3. Receiver electronics per point:
   - FMCW: samples per point N_s = f_s * T_int, with f_s set by the maximum
     beat plus Doppler frequency and T_int the useful integration time (the up and
     down chirps, 2 x 5 us); energy per sample = ADC (Walden FOM x 2^ENOB)
     + FFT/peak DSP (ops per sample x energy per op); plus a continuous per-channel
     analog power (TIA, LO/bias, drivers) x T_dwell.  N_s is set by the
     time-bandwidth product ~ 5 R_max / dR (2.5 x the beat frequency over the up and
     down chirps), independent of how many photons return.
   - FMCW dwell (report section C7b, Eq. (115)): T_dwell = T_int + 2 tau, where
     tau = 2 R / c is the round trip at the 200 m design range.  Each ramp starts
     with tau of discarded beat, so a channel stays on a point 2 tau longer than it
     integrates.  The central case is ungated: the laser keeps emitting during the
     round trips, so the emitted optical energy is E_opt x T_dwell / T_int.
   - ToF (SPAD-SoC): event-driven.  Energy = fixed per-point overhead + (signal +
     background events) x energy per event (avalanche recharge + TDC/histogram).
     Background: the background-rate equation of section C6(d) gives 2.97e8 counts/s
     per 0.05 x 0.05 deg macro-pixel (the IMX479 grid, 2,400 x 520 over 120 x 26 deg)
     for a rho = 0.9 sunlit scene at PDE 0.3; it scales with PDE, and
     the central case takes half of the rho = 0.9 value.  The dead fraction follows the
     dead-time equation of section C6(d) (nine SPADs, 6 ns dead time, the state of the
     art: Sony IMX479 "approx. 6 ns", 3x3 SPADs per macro-pixel) at each background
     level.  Sony's passive recharge behaves paralyzably (its 60 Mcps count-rate
     ceiling is 1/(e tau)), so a SPAD is live only if no photon arrived in the last
     tau: live fraction exp(-r tau), with r the per-SPAD photon-detection rate.  The
     dead time removes signal photons as well as background, so the signal efficiency
     is optics x PDE x live fraction.
   - FMCW: each of the four looks digitizes and transforms its own beat, so the
     receiver electronics per point are four times those of one coherent receiver.
4. Sensor power = P_overhead + point_rate * E_point_electrical.
5. FMCW parallel channels = point_rate * T_dwell (each channel measures one point
   per dwell, round trips included); raw ADC data = point_rate * samples per point
   * receivers * bits, counting the useful windows only, as the ADC energy does (an ADC
   left running through the round trips would stream T_dwell / T_int times more).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogFormatterMathtext
from scipy.optimize import brentq
from scipy.stats import poisson


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


# ---------------------------------------------------------------- constants
H = 6.62607015e-34
C = 2.99792458e8
R_TARGET = 200.0  # m
RHO = 0.10  # Lambertian reflectance


def photon_energy(lam: float) -> float:
    return H * C / lam


def a_mode_monostatic(R: float, D: float = 20e-3, lam: float = 1550e-9) -> float:
    """Mode-equivalent collecting area, same model as coherent_mode_coverage.py."""
    w0 = 0.45 * D
    trunc = 1.0 - np.exp(-2.0 * (0.5 / 0.45) ** 2)
    z_r = np.pi * w0**2 / lam
    w = w0 * np.sqrt(1.0 + (R / z_r) ** 2)
    return trunc**2 * lam**2 * R**2 / (2.0 * np.pi * w**2), w


# ---------------------------------------------------------------- scenarios
# Each parameter has (low-energy, central, high-energy) values where a range is used.
TOF = {
    "2026": dict(
        lam=940e-9, aperture_d=25e-3, optics=0.5, pde=0.37,
        # implementation margins over the ideal requirement in the central background
        # (the earlier 20 / 25 / 35 counts over the ideal 17.26 at 2.87 counts per bin)
        margin=(20 / 17.26, 25 / 17.26, 35 / 17.26), wpe=(0.30, 0.20, 0.15),
        # clocking, SRAM histograms, DSP, MIPI per point.  Calibration: Sony's IMX459
        # development chip drew 1,192 mW (ISSCC 2021); a 1-2 W IMX479-class chip at
        # 25 Mpts/s is 40-80 nJ per point including events.
        e_fixed=(20e-9, 40e-9, 60e-9),
        scene=(0.0, 0.5, 1.0),  # background as a share of the rho = 0.9 full-sun case
        t_listen=20.8e-6, e_event=(4e-12, 5e-12, 7e-12),
    ),
    "2032": dict(
        lam=940e-9, aperture_d=25e-3, optics=0.5, pde=0.45,
        # the earlier 20 / 25 / 30 counts over the ideal 17.99 at 3.31 counts per bin
        margin=(20 / 17.99, 25 / 17.99, 30 / 17.99), wpe=(0.35, 0.25, 0.20),
        e_fixed=(10e-9, 20e-9, 35e-9),
        scene=(0.0, 0.5, 1.0),
        t_listen=20.8e-6, e_event=(2.5e-12, 3.5e-12, 5e-12),
    ),
}
FMCW = {
    "2026": dict(
        # eta calibrated so that E_opt matches Piggott et al. (Waymo, arXiv 2502.09736)
        # "realistic" 10-20 W optical for 12 Mpts/s at 250 m / 5 % / 50 photons, scaled
        # to 200 m / 10 % / 30 photons (0.16-0.32 uJ).  wpe: Aeva SOA >20 % at <=50 C.
        # Calibration check: evaluated for Waymo's own receiver (one look, 50 photons,
        # 250 m, 5 %), eta = 0.25 gives 1.35 uJ per point, inside their 0.83-1.67 uJ.
        lam=1550e-9, eta=(0.40, 0.25, 0.12), looks=4, n_req=(96, 120, 168),
        wpe=(0.20, 0.15, 0.10),
        r_max=300.0, bandwidth=1e9, t_chirp=5e-6, v_max=70.0,
        adc_fom=(30e-15, 50e-15, 100e-15), enob=8,
        dsp_ops=70.0, e_op=(0.2e-12, 0.35e-12, 0.5e-12),
        p_analog=(5e-3, 10e-3, 20e-3),  # TIA + LO/bias + drivers per channel
    ),
    "2032": dict(
        lam=1550e-9, eta=(0.50, 0.40, 0.25), looks=4, n_req=(96, 120, 144),
        wpe=(0.30, 0.22, 0.15),
        r_max=300.0, bandwidth=1e9, t_chirp=5e-6, v_max=70.0,
        adc_fom=(8e-15, 12e-15, 25e-15), enob=8,
        dsp_ops=70.0, e_op=(0.06e-12, 0.1e-12, 0.2e-12),
        p_analog=(2e-3, 3e-3, 6e-3),
    ),
}
P_OVERHEAD = 3.0  # W: scanner motor, system SoC, heaters, power conversion (both types)
BG_PER_PDE = 2.965e8 / 0.3  # counts/s per unit PDE, rho = 0.9 full-sun scene, 0.05 x 0.05 deg pixel, section C6(d)
N_SPAD, TAU_DEAD = 9, 6e-9  # 3x3 macro-pixel and SPAD dead time (s), section C6(d)
P_FA_BIN = 1e-3 / 2000  # section C0 subsection 10.3: 1e-3 false points per point over 2,000 bins of 1 ns


def n_ideal(b: float) -> float:
    """Ideal photon-counting requirement (section C0 subsection 10.3): with Poisson background b per bin, the
    threshold is the smallest count whose tail is at most P_FA_BIN, and 90 % detection fixes the signal."""
    n = 1
    while poisson.sf(n - 1, b) > P_FA_BIN:
        n += 1
    return brentq(lambda s: poisson.sf(n - 1, s + b) - 0.9, 0.0, 300.0)


def tof_n_req(s: dict, k: int) -> float:
    """Required signal counts: the case's margin times the ideal requirement in the central background."""
    return s["margin"][k] * n_ideal(tof_background(s, 1)[2])


def tof_background(s: dict, k: int) -> tuple:
    """Background count rate, dead fraction and background counts per 1 ns bin."""
    r_bg = BG_PER_PDE * s["pde"] * s["scene"][k]
    x = r_bg / N_SPAD * TAU_DEAD
    f_dead = 1 - np.exp(-x)  # paralyzable (passive recharge): live only if no photon in the last tau
    b_bin = r_bg * 1e-9 * 10 * (1 - f_dead)  # 10 shots of ~2 us accumulated per point
    return r_bg, f_dead, b_bin


def tof_energy(s: dict, k: int) -> dict:
    a = np.pi * (s["aperture_d"] / 2) ** 2
    r_bg, f_dead, b_bin = tof_background(s, k)
    # the dead time blinds a SPAD to signal photons as well as to sunlight: the signal
    # efficiency is optics x PDE x live fraction (1 - f_dead)
    n_req = tof_n_req(s, k)
    e_opt = n_req * photon_energy(s["lam"]) * np.pi * R_TARGET**2 / (
        RHO * a * s["optics"] * s["pde"] * (1 - f_dead)
    )
    e_laser = e_opt / s["wpe"][k]
    n_events = r_bg * s["t_listen"] * (1 - f_dead) + n_req
    e_elec = s["e_fixed"][k] + n_events * s["e_event"][k]
    return dict(e_opt=e_opt, e_emit=e_opt, e_laser=e_laser, e_elec=e_elec, e_total=e_laser + e_elec,
                n_events=n_events, r_bg=r_bg, f_dead=f_dead, b_bin=b_bin, n_req=n_req)


def fmcw_digitization(s: dict) -> dict:
    f_beat = 2 * s["bandwidth"] * s["r_max"] / (C * s["t_chirp"])
    f_dopp = 2 * s["v_max"] / s["lam"]
    f_s = 1.25 * 2 * (f_beat + f_dopp)  # real sampling with 25 % margin
    t_int = 2 * s["t_chirp"]  # useful integration: up + down chirp
    tau = 2 * R_TARGET / C  # round trip at the design range, discarded at the start of each ramp
    t_dwell = t_int + 2 * tau  # section C7b, Eq. (115)
    n_samples = f_s * t_int  # only the useful windows are digitized
    return dict(f_beat=f_beat, f_dopp=f_dopp, f_s=f_s, t_dwell=t_dwell, t_int=t_int, tau=tau,
                n_samples=n_samples, range_res=C / (2 * s["bandwidth"]),
                bins=s["r_max"] / (C / (2 * s["bandwidth"])),
                v_res=s["lam"] / (2 * s["t_chirp"]))


def fmcw_energy(s: dict, k: int) -> dict:
    a_mode, _ = a_mode_monostatic(R_TARGET, lam=s["lam"])
    e_opt = s["n_req"][k] * photon_energy(s["lam"]) * np.pi * R_TARGET**2 / (
        RHO * s["looks"] * a_mode * s["eta"][k]
    )
    d = fmcw_digitization(s)
    e_emit = e_opt * d["t_dwell"] / d["t_int"]  # ungated: the laser also emits during the round trips
    e_laser = e_emit / s["wpe"][k]
    e_sample = s["adc_fom"][k] * 2 ** s["enob"] + s["dsp_ops"] * s["e_op"][k]
    # each look has its own receiver: samples and analog power per point x looks
    e_elec = s["looks"] * (d["n_samples"] * e_sample + s["p_analog"][k] * d["t_dwell"])
    return dict(e_opt=e_opt, e_emit=e_emit, e_laser=e_laser, e_elec=e_elec, e_total=e_laser + e_elec,
                e_sample=e_sample, **d)


def sensor_power(point_rate: np.ndarray, e_point: float) -> np.ndarray:
    return P_OVERHEAD + point_rate * e_point


# ---------------------------------------------------------------- tables
def fmt(x: float, unit: str = "") -> str:
    return f"{x:.3g}{unit}"


def make_tables() -> str:
    lines = []
    a_mode, w = a_mode_monostatic(R_TARGET)
    cell = R_TARGET * np.radians(0.05)
    looks = FMCW["2026"]["looks"]
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
                     + " / ".join(f"{x[2]:.2f}" for x in bg))
    lines.append("")
    lines.append("Energy per point at 200 m, 10 % (low / central / high) [E]")
    lines.append(f"{'case':<12}{'E_opt (nJ)':>22}{'emitted (nJ)':>24}{'laser elec (nJ)':>24}{'electronics (nJ)':>24}{'total (nJ)':>22}")
    results = {}
    for name, scen, fn in [("ToF", TOF, tof_energy), ("FMCW", FMCW, fmcw_energy)]:
        for yr, s in scen.items():
            r = [fn(s, k) for k in range(3)]
            results[(name, yr)] = r
            row = f"{name+' '+yr:<12}"
            for key in ("e_opt", "e_emit", "e_laser", "e_elec", "e_total"):
                row += f"{' / '.join(f'{x[key]*1e9:.0f}' for x in r):>24}"
            lines.append(row)
    lines.append("")
    d = fmcw_digitization(FMCW["2026"])
    lines.append("FMCW digitization load (2026 central chirp): "
                 f"R_max 300 m, B 1 GHz (dR {d['range_res']*100:.0f} cm, {d['bins']:.0f} range bins), "
                 f"T_chirp 5 us up + 5 us down, v_max 70 m/s; round trip tau = {d['tau']*1e6:.2f} us at 200 m, "
                 f"dwell = {d['t_int']*1e6:.0f} us + 2 tau = {d['t_dwell']*1e6:.2f} us")
    lines.append(f"  beat {d['f_beat']/1e6:.0f} MHz + Doppler {d['f_dopp']/1e6:.0f} MHz -> f_s = {d['f_s']/1e9:.2f} GS/s real, "
                 f"{d['n_samples']:.0f} samples per point, velocity resolution {d['v_res']:.2f} m/s")
    for yr in ("2026", "2032"):
        r = results[("FMCW", yr)]
        lines.append(f"  {yr}: energy per sample (ADC + DSP) = "
                     + " / ".join(f"{x['e_sample']*1e12:.0f}" for x in r) + " pJ; "
                     + f"{FMCW[yr]['looks']} receivers per point")
    lines.append("")
    lines.append("Chirp design space (R_max, B, T_chirp): beat, f_s, samples per point")
    for r_max, bw, t in [(200, 0.5e9, 4e-6), (250, 1e9, 10e-6), (300, 1e9, 5e-6), (300, 2e9, 5e-6)]:
        s = dict(FMCW["2026"], r_max=r_max, bandwidth=bw, t_chirp=t)
        dd = fmcw_digitization(s)
        lines.append(f"  {r_max:.0f} m, {bw/1e9:.1f} GHz, {t*1e6:.0f} us: f_b {dd['f_beat']/1e6:.0f} MHz, "
                     f"f_s {dd['f_s']/1e9:.2f} GS/s, N_s {dd['n_samples']:.0f}, bins {dd['bins']:.0f}")
    lines.append("")
    lines.append("Sensor power (W) = 3 W overhead + rate x E_point (central values)")
    rates = [1e6, 2e6, 5e6, 10e6, 25e6, 40e6]
    lines.append(f"{'case':<12}" + "".join(f"{r/1e6:>9.0f} M" for r in rates))
    for key, r in results.items():
        e = r[1]["e_total"]
        lines.append(f"{key[0]+' '+key[1]:<12}" + "".join(f"{sensor_power(np.array(x), e):>10.1f}" for x in rates))
    lines.append("")
    looks = FMCW["2026"]["looks"]
    lines.append(f"FMCW parallel channels (transmit beams, {looks} coherent receivers each) and raw ADC data "
                 "(10-bit samples, all receivers), 2026 chirp")
    for rate in rates:
        n_ch = rate * d["t_dwell"]
        lines.append(f"  {rate/1e6:>4.0f} Mpts/s: {n_ch:>5.0f} channels at {d['t_dwell']*1e6:.1f} us dwell "
                     f"({rate*(4e-6 + 2*d['tau']):>4.0f} at 4 us integration), "
                     f"{looks*n_ch:.0f} receivers; "
                     f"raw data {looks*rate*d['n_samples']*10/1e12:.2f} Tb/s; "
                     f"optical power {rate*results[('FMCW','2026')][1]['e_emit']:.2f} W emitted "
                     f"({rate*results[('FMCW','2026')][1]['e_opt']:.2f} W useful; "
                     f"SOA/laser heat {rate*(results[('FMCW','2026')][1]['e_laser']-results[('FMCW','2026')][1]['e_emit']):.1f} W)")
    lines.append("")
    tof = results[("ToF", "2026")][1]
    lines.append(f"ToF 2026 central: events per point {tof['n_events']:.0f} (bright-sun background, "
                 f"dead fraction {tof['f_dead']*100:.1f} %, {tof['b_bin']:.2f} counts per bin; ideal requirement "
                 f"{n_ideal(tof['b_bin']):.2f} counts, n_req {tof['n_req']:.1f}, signal efficiency "
                 f"{TOF['2026']['optics']*TOF['2026']['pde']*(1-tof['f_dead']):.4f}), "
                 f"optical power at 25 Mpts/s = {25e6*tof['e_opt']:.2f} W")
    for yr in ("2026", "2032"):
        lines.append(f"ToF {yr} n_req (low / central / high) = "
                     + " / ".join(f"{tof_n_req(TOF[yr], k):.1f}" for k in range(3)))
    return "\n".join(lines), results


# ---------------------------------------------------------------- figure
def figure(results: dict, out_stem: Path) -> None:
    configure_plot_style()
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.7), constrained_layout=True)

    # (a) sensor power vs point rate
    ax = axes[0]
    rate = np.logspace(5.7, 7.7, 200)
    styles = {
        ("ToF", "2026"): (COLORS["primary"], "-", "ToF 940 nm, 2026"),
        ("ToF", "2032"): (COLORS["primary"], DASH, "ToF, 2032 projection"),
        ("FMCW", "2026"): (COLORS["warm_accent"], "-", "FMCW 1550 nm, 2026"),
        ("FMCW", "2032"): (COLORS["warm_accent"], DASH, "FMCW, 2032 projection"),
    }
    ax.axhspan(8, 25, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, linewidth=0,
               label="_nolegend_", zorder=0)
    ax.text(6.2e5, 26.5, "typical 8–25 W", color=COLORS["annotation"], va="bottom")
    for key, (col, ls, lab) in styles.items():
        r = results[key]
        ax.plot(rate, sensor_power(rate, r[1]["e_total"]), color=col, ls=ls, lw=LW, label=lab)
        if key[1] == "2026":
            ax.fill_between(rate, sensor_power(rate, r[0]["e_total"]),
                            sensor_power(rate, r[2]["e_total"]), color=col, alpha=0.15,
                            linewidth=0, label="_nolegend_")
    # Published products (range at 10 % differs from the 200 m model; see labels)
    products = [
        (3.84e6, 8.0, "ATX", COLORS["primary"], "s", (6, 0), "left", "center"),
        (15.0e6, 13.0, "ETX", COLORS["primary"], "s", (0, 5), "center", "bottom"),
        (1.5e6, 45.0, "LuminWave F1", COLORS["warm_accent"], "^", (0, 5), "center", "bottom"),
    ]
    for x_p, y_p, lab, col, mk, off, ha, va in products:
        ax.plot(x_p, y_p, mk, color=col, mfc="white", mew=1.2, ms=5, label="_nolegend_", zorder=5)
        ax.annotate(lab, (x_p, y_p), xytext=off, textcoords="offset points", color=col,
                    ha=ha, va=va)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(5e5, 5e7)
    # the top limit leaves the legend above the 2032 FMCW curve
    ax.set_ylim(3, 1000)
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlabel("Point rate (points s$^{-1}$)")
    ax.set_ylabel("Sensor electrical power (W)")
    ax.legend(loc="upper left", handlelength=2.2)
    ax.set_title("(a) Power vs point rate, 200 m at 10%", loc="left")

    # (b) energy per point breakdown
    ax = axes[1]
    order = [("ToF", "2026"), ("ToF", "2032"), ("FMCW", "2026"), ("FMCW", "2032")]
    labels = ["ToF\n2026", "ToF\n2032", "FMCW\n2026", "FMCW\n2032"]
    x = np.arange(len(order))
    opt = np.array([results[k][1]["e_emit"] for k in order]) * 1e9
    loss = np.array([results[k][1]["e_laser"] - results[k][1]["e_emit"] for k in order]) * 1e9
    elec = np.array([results[k][1]["e_elec"] for k in order]) * 1e9
    ax.bar(x, opt, 0.6, color=COLORS["primary"], label="emitted optical energy")
    ax.bar(x, loss, 0.6, bottom=opt, color=COLORS["grey_accent"], label="laser/SOA/driver loss")
    ax.bar(x, elec, 0.6, bottom=opt + loss, color=COLORS["warm_accent"], label="receiver electronics")
    for xi, tot in zip(x, opt + loss + elec):
        ax.text(xi, tot * 1.03, f"{tot/1000:.2f} µJ", ha="center", va="bottom")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Electrical energy per point (nJ)")
    # headroom above the tallest bar keeps its total label clear of the legend
    ax.set_ylim(0, 7600)
    ax.legend(loc="upper left")
    ax.set_title("(b) Energy per point (central)", loc="left")

    # (c) FMCW channel count vs point rate
    ax = axes[2]
    rate2 = np.logspace(5.7, 7.7, 100)
    dd = fmcw_digitization(FMCW["2026"])
    two_tau = 2 * dd["tau"]
    for t_int, col, ls in [(4e-6, COLORS["cool_accent"], DASH), (10e-6, COLORS["warm_accent"], "-"),
                           (20e-6, COLORS["purple_accent"], DASH)]:
        ax.plot(rate2, rate2 * (t_int + two_tau), color=col, ls=ls, lw=LW,
                label=f"{(t_int + two_tau)*1e6:.1f} µs dwell ({t_int*1e6:.0f} µs + 2τ)")
    f_s = dd["f_s"]
    looks = FMCW["2026"]["looks"]
    note = [f"{looks} receivers per channel;", f"raw 10-bit ADC data, {dd['t_dwell']*1e6:.1f} µs dwell:"]
    for r_mark in (2e6, 10e6, 25e6):
        n_ch = r_mark * dd["t_dwell"]
        ax.plot(r_mark, n_ch, "o", color=COLORS["warm_accent"], ms=3.5, label="_nolegend_")
        note.append(f"{r_mark/1e6:.0f} Mpts/s: {n_ch:.0f} ch, {looks*r_mark*dd['n_samples']*10/1e12:.2g} Tb/s")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(5e5, 5e7)
    ax.set_ylim(1, 1e4)
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlabel("Point rate (points s$^{-1}$)")
    ax.set_ylabel("Parallel coherent channels (beams)")
    ax.text(6e5, 7000, "\n".join(note), color=COLORS["annotation"], va="top")
    ax.legend(loc="lower right")
    ax.set_title("(c) FMCW channels, raw ADC data", loc="left")

    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    here = OUT_DIR
    text, results = make_tables()
    (here / "fmcw_tof_system_budget_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    figure(results, here / "fmcw_tof_system_budget")


if __name__ == "__main__":
    main()
