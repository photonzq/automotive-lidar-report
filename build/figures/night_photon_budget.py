"""Night photon budget of a camera pixel: low-light CMOS, photon counting (SPAD) and thermal.

Companion to section A7 of automotive_perception_report_2026-09-27.md. Engineering estimates [E] for a
Lambertian target imaged on axis. The script prints the numbers behind the section's tables, writes them
to night_photon_budget_tables.txt and draws night_photon_budget.png / .pdf.

Equations (numbered as in the report):
  (13) image-plane illuminance          E_img = tau_o * rho * E_s / (4 F^2)
  (14) photoelectrons per readout        n = S_v * E_img * A_pix * t,   S_v = eta * Phi_lx
  (15) SNR per readout                   integrating: n / sqrt(n + n_d + sigma_r^2); counting: n / sqrt(n + n_dc)
  (16) SNR over M readouts               SNR_M = sqrt(M) * SNR_1      (uniform target on a black background)
  (17) photon-counting gain              G = sqrt((n + n_d + sigma_r^2) / (n + n_dc))
  (18) burst of K readouts, total N      G_K = sqrt((N + K sigma_r^2) / N)      (no dark signal)
  (19) dark rate versus temperature      D(T) = D(T0) * 2**((T - T0) / T_2)
  (20) SPAD power at the count ceiling   P = N_px * Q (V_bd + V_ex) * r,   r <= 1 / (e tau_d)
  (21) thermal SNR per pixel             SNR_th = dT / NETD

S_v is a pixel's luminous sensitivity per unit area (photoelectrons per lux-second per um^2 at the sensor).
The CMOS values are OmniVision's, computed from measured quantum efficiency for a 2.1 um automotive pixel
under D65 light with a 650 nm infrared-cut filter (Funatsu et al., IS&T Electronic Imaging 2022, Table 2):
16.4k e-/(lx s) for the green pixel of an RGGB array and 30.3k e-/(lx s) for the clear pixel of RCCB/RCCG.
The SPAD is given the clear pixel's sensitivity, so that it differs from the CMOS pixel only in area and
noise. Phi_lx (photons per second per m^2 per lux) is computed for the calibration checks, for a
monochromatic line and for black bodies, with the CIE 1931 photopic curve V(lambda) from the multi-lobe fit
of Wyman, Sloan and Shirley (JCGT 2013).

Inputs and their sources are listed next to each constant: [I] independent measurement or paper, [P]
company document, [E] assumption or estimate.
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


# ---------------------------------------------------------------- photometry (calibration checks)
H, C, KB = 6.62607015e-34, 2.99792458e8, 1.380649e-23
KM = 683.0  # lm/W at 555 nm


def _lobe(x, mu, s1, s2):
    return np.exp(-0.5 * ((x - mu) / np.where(x < mu, s1, s2)) ** 2)


def vbar(lam_nm):
    """CIE 1931 photopic luminosity function V(lambda), multi-lobe fit of Wyman, Sloan and Shirley (2013)."""
    return 0.821 * _lobe(lam_nm, 568.8, 46.9, 40.5) + 0.286 * _lobe(lam_nm, 530.9, 16.3, 31.1)


LAM = np.linspace(360.0, 1100.0, 7401)  # nm


def planck(lam_nm, temp):
    lam = lam_nm * 1e-9
    return 2 * H * C**2 / lam**5 / np.expm1(H * C / (lam * KB * temp))


def photon_spectrum_per_lux(temp):
    """Photon spectral flux (s^-1 m^-2 nm^-1) of a black body at `temp`, scaled to 1 lux."""
    s = planck(LAM, temp)
    lux = KM * np.trapezoid(vbar(LAM) * s, LAM)
    return s / lux * LAM * 1e-9 / (H * C)


def phi_lx_line(lam_nm):
    """Photons s^-1 m^-2 per lux for a monochromatic line."""
    return 1.0 / (KM * float(vbar(np.array([lam_nm]))[0])) / (H * C / (lam_nm * 1e-9))


def phi_lx_bb(temp, lo=400.0, hi=700.0):
    """Photons s^-1 m^-2 per lux for a black body at `temp`, counted from lo to hi (nm)."""
    band = (LAM >= lo) & (LAM <= hi)
    return np.trapezoid(photon_spectrum_per_lux(temp)[band], LAM[band])


def green_qe(lam_nm, peak=0.70, centre=530.0, sigma=40.0):
    """Simple model of the green channel of an RGGB pixel: Gaussian, peak QE 0.70 at 530 nm, FWHM 94 nm [E]."""
    return peak * np.exp(-0.5 * ((lam_nm - centre) / sigma) ** 2)


def s_v_green_model(temp):
    """Luminous sensitivity per um^2 of the model green channel for a black body, 400-700 nm."""
    band = (LAM >= 400.0) & (LAM <= 700.0)
    n = photon_spectrum_per_lux(temp)
    return np.trapezoid((green_qe(LAM) * n)[band], LAM[band]) * 1e-12


# ---------------------------------------------------------------- optics, sensors, scene
TAU_O = 0.8     # lens x windshield transmission, 0.9 x 0.9 [E]
F_NUM = 1.6     # f-number of the camera lens [E]
T_INT = 0.030   # s, exposure per frame at 30 frames/s [E]
S_V_GREEN = 16.4e3 / 2.1**2  # e- per (lx s um^2): RGGB green, Funatsu et al. 2022, Table 2 [I]
S_V_CLEAR = 30.3e3 / 2.1**2  # e- per (lx s um^2): RCCB/RCCG clear, same source [I]
S_V_SPAD = S_V_CLEAR         # monochrome SPAD given the clear pixel's sensitivity [E]
SIGMA_R = 0.6   # e- rms, CMOS read noise: IMX490 0.54 (LUCID EMVA 1288), OmniVision 0.83 (IISW 2019),
                # onsemi 8.3 MP SNR=1 at about 1.3 e- for 60-80 C (IISW 2023, Fig. 3) [I]
P_CMOS = 3.0e-6   # m, automotive CMOS pixel (IMX490, OX03C10 class) [P]
P_SPAD = 6.39e-6  # m, Canon 3.2 MP SPAD (IEDM 2021) [P]
RHO_DARK, RHO_LIGHT = 0.05, 0.5  # diffuse reflectance of dark and light clothing, as in section A6.1 [E]

# dark rates: CMOS dark current density at 60 C (e- s^-1 um^-2) and SPAD dark count rate
DC60_LOW, DC60_MID, DC60_HIGH = 0.2, 1.0, 3.3
# 0.2: inferred from onsemi's SNR=1 points (IISW 2023); 1.35: Gigajot QIS at 60 C (Sci. Rep. 2022) [I];
# 3.3: OmniVision 2.8 um large photodiode, 25.6 e-/s at 60 C (IISW 2019) [I]; doubling every 6 C (McGrath,
# IISW 2017) [I]
T2_CMOS = 6.0
DCR25_CANON = 1.8  # counts/s per 6.39 um pixel at 25 C (Canon IEDM 2021, via the ISSW 2024 R01.1 table) [I]
T2_SPAD = (12.0, 7.0)  # K per doubling: 12 K a slow case [E]; ST 7 K at high temperature (IISW 2023) [I]


def e_img(e_s, rho, tau=TAU_O, f_num=F_NUM):
    """Eq. (13): image-plane illuminance (lux) of a Lambertian target of reflectance rho at scene illuminance e_s."""
    return tau * rho * e_s / (4.0 * f_num**2)


def n_pe(e_s, rho, pitch, s_v, t=T_INT, tau=TAU_O, f_num=F_NUM):
    """Eq. (14): photoelectrons (or detected photons) per pixel per readout."""
    return s_v * e_img(e_s, rho, tau, f_num) * (pitch * 1e6) ** 2 * t


def snr_int(n, n_d, sig=SIGMA_R):
    return n / np.sqrt(n + n_d + sig**2)


def snr_cnt(n, n_dc):
    return n / np.sqrt(n + n_dc)


def gain(n, n_d, n_dc, sig=SIGMA_R):
    """Eq. (17)."""
    return np.sqrt((n + n_d + sig**2) / (n + n_dc))


def cmos_dark(temp, density60=DC60_MID, pitch=P_CMOS, t=T_INT):
    """Dark electrons per readout of a CMOS pixel, Eq. (19) with 6 C doubling."""
    return density60 * (pitch * 1e6) ** 2 * 2 ** ((temp - 60.0) / T2_CMOS) * t


def spad_dark(temp, t2, pitch=P_SPAD, t=T_INT):
    """Dark counts per readout of a Canon-class SPAD pixel, scaled by area, Eq. (19)."""
    return DCR25_CANON * (pitch / P_SPAD) ** 2 * 2 ** ((temp - 25.0) / t2) * t


def spad_dark_mid(temp, pitch=P_CMOS):
    """Geometric mean of the 12 K and 7 K cases."""
    return np.sqrt(spad_dark(temp, T2_SPAD[0], pitch) * spad_dark(temp, T2_SPAD[1], pitch))


def n_required(snr, var_floor):
    """Signal per readout that gives `snr` when the noise variance is n + var_floor."""
    return snr**2 / 2.0 + np.sqrt(snr**4 / 4.0 + snr**2 * var_floor)


# scenes: name, scene illuminance on the target (lux)
SCENES = [
    ("Low-beam hotspot (IIHS 5 lux criterion, section A6.1)", 5.0),
    ("Glare-limited zone at 50 m, 350 cd (Eq. (8))", 350.0 / 50.0**2),
    ("Full moon, typical summer upper value", 0.1),
    ("Glare-limited zone at 100 m, 350 cd", 350.0 / 100.0**2),
    ("Half moon at zenith, maximum", 0.025),
    ("Glare-limited zone at 150 m, 350 cd", 350.0 / 150.0**2),
    ("Moonless rural sky, clear", 0.001),
]

# reference cameras for the pedestrian example
PED_AREA = 1.7 * 0.5   # m^2, pedestrian silhouette used throughout the report
IFOV_VIS = np.radians(30.0) / 1920  # 3.0 um pixels, 1920 columns over 30 degrees [E]
IFOV_TH = np.radians(24.0) / 640    # 640 x 512 thermal core, 24 degree lens (FLIR ADK option) [P]
NETD = 0.050  # K, FLIR ADK "<50 mK" [P]
ROSE_K = 5.0  # aggregate SNR needed to detect a uniform target (Rose criterion) [E]


def ranges(amb, temp, rr):
    """Ranges at which the dark pedestrian reaches the Rose criterion and a per-pixel SNR of 1."""
    es = 350.0 / rr**2 + amb
    m = PED_AREA / (rr * IFOV_VIS) ** 2
    n = n_pe(es, RHO_DARK, P_CMOS, S_V_CLEAR)
    nd, ndc = cmos_dark(temp), spad_dark_mid(temp)
    s1c, s1p = snr_int(n, nd), snr_cnt(n, ndc)
    pick = lambda ok: rr[ok].max() if ok.any() else float("nan")  # noqa: E731
    return (pick(np.sqrt(m) * s1c >= ROSE_K), pick(np.sqrt(m) * s1p >= ROSE_K), pick(s1c >= 1.0), pick(s1p >= 1.0))


def tables() -> str:
    out = []
    w = out.append
    w("== Photon flux per lux, Phi_lx (photons s^-1 m^-2 lx^-1)")
    w(f"  555 nm line                                  {phi_lx_line(555.0):.3e}")
    w(f"  530 nm line                                  {phi_lx_line(530.0):.3e}")
    for temp in (3200.0, 5500.0, 6504.0):
        w(f"  black body {temp:6.0f} K, 400-700 nm / 400-650 nm   {phi_lx_bb(temp):.3e} / "
          f"{phi_lx_bb(temp, 400.0, 650.0):.3e}")
    w("")
    w("== Luminous sensitivity S_v (e- per lx s um^2) and the efficiencies it implies")
    for name, s_v in (("RGGB green", S_V_GREEN), ("RCCB clear", S_V_CLEAR)):
        eta = s_v / (phi_lx_bb(6504.0, 400.0, 650.0) * 1e-12)
        w(f"  {name}: S_v = {s_v:6.0f}; implied photon-weighted efficiency over 400-650 nm (D65): {eta:.2f}")
    w(f"  clear / green = {S_V_CLEAR / S_V_GREEN:.2f}")
    w(f"  Gaussian green model (peak 0.70 at 530 nm, FWHM 94 nm), 400-700 nm: S_v = {s_v_green_model(5500.0):.0f}"
      f" at 5500 K, {s_v_green_model(3200.0):.0f} at 3200 K (ratio {s_v_green_model(3200.0) / s_v_green_model(5500.0):.2f})")
    w("")
    w("== Calibration checks of Eq. (14)")
    ph = phi_lx_line(530.0) * (2.8e-6) ** 2
    w(f"  OmniVision 2.8 um pixel at 530 nm: {ph:.0f} photons per lx s on the pixel; measured 24,600 e- per lx s"
      f" -> implied QE {24600.0 / ph:.2f}; per um^2: {24600.0 / 2.8**2:.0f} e- per lx s")
    s_v_3200 = S_V_GREEN * s_v_green_model(3200.0) / s_v_green_model(5500.0)
    n_sony = n_pe(0.17, 0.18, 2.9e-6, s_v_3200, t=1.0 / 60.0, tau=1.0, f_num=1.4)
    w(f"  Sony SNR1s conditions (3200 K, 18% grey, F1.4, 1/60 s, no lens loss), 2.9 um G pixel, S_v scaled to "
      f"3200 K = {s_v_3200:.0f}: at IMX585's 0.17 lx, n = {n_sony:.2f} e-; SNR with sigma_r 0.6 = "
      f"{snr_int(n_sony, 0.0):.2f}")
    for rho in (0.2, 0.5):
        nc = n_pe(0.002, rho, P_SPAD, S_V_SPAD, t=1.0 / 30.0, tau=0.9, f_num=1.2)
        w(f"  Canon 0.002 lux, f/1.2, 1/30 s, tau 0.9, rho {rho}: {nc:.2f} detected photons per 6.39 um pixel per"
          f" frame; at 0.0003 lux: {nc * 0.15:.3f}")
    w("")
    w(f"== Table: photoelectrons per pixel per {T_INT * 1e3:.0f} ms frame, f/{F_NUM}, tau_o {TAU_O}, rho = {RHO_DARK}"
      f" (x10 for rho = {RHO_LIGHT})")
    w(f"  {'scene':58s} {'E_s (lux)':>10s} {'G 3um':>8s} {'C 3um':>8s} {'C 2.1um':>8s} {'SPAD 6.39':>10s}")
    for name, es in SCENES:
        w(f"  {name:58s} {es:10.4f} {n_pe(es, RHO_DARK, P_CMOS, S_V_GREEN):8.3f} "
          f"{n_pe(es, RHO_DARK, P_CMOS, S_V_CLEAR):8.3f} {n_pe(es, RHO_DARK, 2.1e-6, S_V_CLEAR):8.3f} "
          f"{n_pe(es, RHO_DARK, P_SPAD, S_V_SPAD):10.3f}")
    w("")
    w("== Read-noise boundary: scene illuminance at which n = sigma_r^2 = 0.36 e-")
    for rho in (RHO_DARK, RHO_LIGHT):
        w(f"  rho = {rho}: clear 3 um {SIGMA_R**2 / n_pe(1.0, rho, P_CMOS, S_V_CLEAR):.3f} lux; green 3 um "
          f"{SIGMA_R**2 / n_pe(1.0, rho, P_CMOS, S_V_GREEN):.3f} lux; clear 2.1 um "
          f"{SIGMA_R**2 / n_pe(1.0, rho, 2.1e-6, S_V_CLEAR):.3f} lux")
    w("  as a range in the glare-limited zone (350 cd), rho = 0.05, clear 3 um: R* = "
      f"{np.sqrt(350.0 * n_pe(1.0, RHO_DARK, P_CMOS, S_V_CLEAR) / SIGMA_R**2):.0f} m")
    w("")
    w("== SNR = 1 thresholds per readout (signal needed, e-)")
    for sig in (0.54, 0.6, 0.83):
        w(f"  integrating, sigma_r = {sig} e-, no dark: n = {n_required(1.0, sig**2):.2f}")
    w("  photon counting, no dark counts: n = 1.00")
    w("")
    w("== Dark signal per 30 ms readout versus chip temperature")
    w(f"  {'T (C)':>6s} {'CMOS 3um low/mid/high (e-)':>30s} {'SPAD 6.39um 12K/7K':>22s} {'SPAD at 3um 12K/7K':>20s}")
    for temp in (25.0, 40.0, 60.0, 85.0, 105.0):
        c = [cmos_dark(temp, d) for d in (DC60_LOW, DC60_MID, DC60_HIGH)]
        s = [spad_dark(temp, t2) for t2 in T2_SPAD]
        s3 = [spad_dark(temp, t2, pitch=P_CMOS) for t2 in T2_SPAD]
        w(f"  {temp:6.0f} {c[0]:9.3f} {c[1]:9.3f} {c[2]:9.2f}   {s[0]:9.3f} {s[1]:9.2f}   {s3[0]:8.3f} {s3[1]:8.3f}")
    w("  checks: Panasonic 6 um VAPD 21 cps (room) -> 10,000 cps at 105 C chip (300 counts per 30 ms), i.e. a "
      f"doubling every {80.0 / np.log2(10000.0 / 21.0):.1f} K; ST 810 -> 6,923 cps from 60 to 80 C, every "
      f"{20.0 / np.log2(6923.0 / 810.0):.1f} K")
    w("  dark rate per um^2 at 60 C: CMOS 0.2-3.3 e-/s; SPADs: ST 10.17 um "
      f"{810.0 / 10.17**2:.1f}, Sony 10/6 um {220.0 / 100.0:.1f}/{300.0 / 36.0:.1f}, Canon extrapolated "
      f"{spad_dark(60.0, 12.0, t=1.0) / 6.39**2:.2f}-{spad_dark(60.0, 7.0, t=1.0) / 6.39**2:.2f} counts/s")
    w("")
    w("== Photon-counting gain G at equal pixel area (3 um) and sensitivity, Eq. (17)")
    w(f"  {'n per readout':>14s} {'no dark':>8s} {'25 C':>8s} {'60 C':>8s} {'85 C':>8s}")
    for n in (1.0, 0.36, 0.1, 0.03, 0.01):
        row = [gain(n, 0.0, 0.0)] + [gain(n, cmos_dark(t), spad_dark_mid(t)) for t in (25.0, 60.0, 85.0)]
        w(f"  {n:14.2f} " + " ".join(f"{g:8.2f}" for g in row))
    for temp in (25.0, 60.0, 85.0):
        nd, ndc = cmos_dark(temp), spad_dark_mid(temp)
        w(f"  {temp:.0f} C: CMOS dark {nd:.3f} e-, SPAD dark {ndc:.3f} (geometric mean of 12 K and 7 K);"
          f" small-signal cap sqrt((sigma^2 + n_d)/n_dc) = {np.sqrt((SIGMA_R**2 + nd) / ndc):.2f}")
    w("")
    w("== Burst of K readouts with the same total signal N, Eq. (18), no dark")
    for big_n in (0.1, 1.0, 10.0):
        w(f"  N = {big_n:5.1f} e-: " + "  ".join(
            f"K={k:3d}: G={np.sqrt((big_n + k * SIGMA_R**2) / big_n):5.2f}" for k in (1, 10, 30, 100)))
    w("")
    w("== Pedestrian lit by the glare-limited zone (350 cd) plus ambient, dark clothing, chip 60 C")
    w(f"  visible camera: 3.0 um, IFOV {IFOV_VIS * 1e3:.3f} mrad (f = {P_CMOS / IFOV_VIS * 1e3:.1f} mm, aperture "
      f"{P_CMOS / IFOV_VIS / F_NUM * 1e3:.1f} mm); thermal: IFOV {IFOV_TH * 1e3:.3f} mrad, NETD {NETD * 1e3:.0f} mK")
    w(f"  {'R (m)':>6s} {'E_s (lux)':>9s} {'px on ped':>9s} {'n clear':>8s} {'SNR_1 CMOS':>10s} {'SNR_1 cnt':>9s}"
      f" {'SNR_M CMOS':>10s} {'SNR_M cnt':>9s} {'th px':>6s} {'SNR_M th dT=1/5K':>17s}")
    for amb_name, amb in (("moonless", 0.001), ("full moon", 0.1)):
        w(f"  ambient: {amb_name} ({amb} lux)")
        for r in (50.0, 75.0, 100.0, 150.0, 200.0):
            es = 350.0 / r**2 + amb
            m = PED_AREA / (r * IFOV_VIS) ** 2
            n = n_pe(es, RHO_DARK, P_CMOS, S_V_CLEAR)
            s1c, s1p = snr_int(n, cmos_dark(60.0)), snr_cnt(n, spad_dark_mid(60.0))
            mt = PED_AREA / (r * IFOV_TH) ** 2
            s_t = [np.sqrt(mt) * dt / NETD for dt in (1.0, 5.0)]
            w(f"  {r:6.0f} {es:9.4f} {m:9.0f} {n:8.3f} {s1c:10.2f} {s1p:9.2f} {np.sqrt(m) * s1c:10.1f}"
              f" {np.sqrt(m) * s1p:9.1f} {mt:6.0f} {s_t[0]:8.0f}/{s_t[1]:.0f}")
    rr = np.linspace(10.0, 600.0, 5901)
    for amb_name, amb in (("moonless", 0.001), ("full moon", 0.1)):
        for temp in (25.0, 60.0):
            r_c, r_p, q_c, q_p = ranges(amb, temp, rr)
            w(f"  {amb_name}, chip {temp:.0f} C: Rose (SNR_M >= {ROSE_K:.0f}) CMOS {r_c:.0f} m, photon counting "
              f"{r_p:.0f} m;  per-pixel SNR >= 1: CMOS {q_c:.0f} m, photon counting {q_p:.0f} m")
    w("  thermal: Johnson detection ceiling 0.92/(1.5 IFOV) = "
      f"{0.92 / (1.5 * IFOV_TH):.0f} m; per-pixel SNR dT/NETD = {1.0 / NETD:.0f}-{5.0 / NETD:.0f} for dT = 1-5 K")
    w("")
    w("== SPAD in daylight: count ceiling and avalanche power, Eq. (20)")
    e_day, rho_day = 1.0e5, 0.2
    rate = S_V_SPAD * e_img(e_day, rho_day) * (P_SPAD * 1e6) ** 2
    w(f"  100 klux, rho 0.2: image plane {e_img(e_day, rho_day):.0f} lux; a 6.39 um pixel would detect"
      f" {rate:.2e} photons/s")
    for tau_d in (4.3e-9, 6.0e-9):
        w(f"  dead time {tau_d * 1e9:.1f} ns: paralyzable ceiling 1/(e tau_d) = {1.0 / (np.e * tau_d):.3e} /s")
    w("  ST check: 4.3 ns dead time, measured maximum count rate 85 Mcps (IISW 2023)")
    q_st, v_st = 68e-15, 18.6 + 2.5
    e_av = q_st * v_st
    w(f"  ST avalanche energy Q (V_bd + V_ex) = 68 fC x {v_st:.1f} V = {e_av * 1e12:.2f} pJ")
    for q_c in (25e-15, 50e-15):
        w(f"  Canon bias 30 + 2.5 V, Q = {q_c * 1e15:.0f} fC: {q_c * 32.5 * 1e12:.2f} pJ")
    for npx in (2.1e6, 3.2e6):
        w(f"  {npx / 1e6:.1f} MP at the 6 ns ceiling, {e_av * 1e12:.2f} pJ: {npx * e_av / (np.e * 6.0e-9):.0f} W")
    r1w = 1.0 / (2.1e6 * e_av)
    w(f"  1 W budget at 2.1 MP and {e_av * 1e12:.2f} pJ: <= {r1w:.2e} detections/s per pixel = "
      f"{r1w * np.e * 6.0e-9 * 100:.2f}% of the 6 ns ceiling; daylight arrivals exceed it by "
      f"{rate / r1w:.0f}x")
    return "\n".join(out)


def figure(out_stem: Path) -> None:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(4.2, 3.24), constrained_layout=True)
    es = np.logspace(-4, 1, 400)
    for x0, x1, lab in ((6e-4, 3e-3, "moonless"), (0.05, 0.32, "full moon")):
        ax.axvspan(x0, x1, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, label="_nolegend_", zorder=0)
        ax.text(np.sqrt(x0 * x1), 8e1, lab, ha="center", va="top", color=COLORS["text"])
    for x, lab in ((350.0 / 150.0**2, "150 m"), (350.0 / 50.0**2, "50 m"), (5.0, "5 lux")):
        ax.axvline(x, color=COLORS["annotation"], lw=0.8, ls=DASH, label="_nolegend_", zorder=0)
        ax.text(x * 1.12, 1.5e-4, lab, rotation=90, va="bottom", color=COLORS["annotation"])
    ax.plot(es, n_pe(es, RHO_DARK, P_CMOS, S_V_CLEAR), color=COLORS["primary"], lw=LW,
            label=r"3 µm clear CMOS pixel, dark clothing ($\rho=0.05$)")
    ax.plot(es, n_pe(es, RHO_LIGHT, P_CMOS, S_V_CLEAR), color=COLORS["primary"], lw=LW, ls=DASH,
            label=r"3 µm clear CMOS pixel, light clothing ($\rho=0.5$)")
    ax.plot(es, n_pe(es, RHO_DARK, P_SPAD, S_V_SPAD), color=COLORS["warm_accent"], lw=LW,
            label=r"6.39 µm SPAD pixel, dark clothing ($\rho=0.05$)")
    # noise floors per readout, drawn thinner than the data curves (reference lines)
    ax.axhline(SIGMA_R**2 + cmos_dark(60.0), color=COLORS["neutral"], lw=1.0, ls=DASH,
               label=r"CMOS noise floor $\sigma_r^2+\bar n_d$, 3 µm, 60 °C")
    ax.axhline(spad_dark_mid(60.0, pitch=P_SPAD), color=COLORS["warm_accent"], lw=1.0, ls=DASH,
               label="SPAD dark counts, 6.39 µm, 60 °C")
    ax.axhline(spad_dark(25.0, 12.0), color=COLORS["warm_accent"], lw=1.0, ls=(0, (5, 2, 1, 2)),
               label="SPAD dark counts, 6.39 µm, 25 °C")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(1e-4, 10.0)
    ax.set_ylim(1e-4, 1e2)
    ax.set_xlabel("Scene illuminance on the target (lux)")
    ax.set_ylabel("Photoelectrons per pixel per 30 ms frame")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=1)
    fig.savefig(out_stem.with_suffix(".png"), dpi=600)
    fig.savefig(out_stem.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    text = tables()
    (OUT_DIR / "night_photon_budget_tables.txt").write_text(text + "\n", encoding="utf-8")
    print(text)
    figure(OUT_DIR / "night_photon_budget")


if __name__ == "__main__":
    main()
