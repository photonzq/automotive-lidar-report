"""Coherent reception (single-mode, monostatic) vs direct-detection ToF:
spatial modes, mode-equivalent aperture and the sampling mesh at the target.

Companion to section C10.3a/C10.3b of automotive_perception_report_2026-09-27.md.

Model assumptions (see the note for discussion):
- Diffuse (Lambertian), depolarizing, extended target in the beam; speckle-averaged powers.
- Coherent receiver: monostatic, single spatial mode, single polarization, Gaussian
  mode with waist w0 = 0.45 D inside a hard aperture of diameter D (0.9 x radius),
  collimated (range-agnostic) beam.  Truncation efficiency applied on transmit and
  receive.
- Received coherent power: P_rx = eta*rho*P_tx * lambda^2 / (2 pi^2 w(R)^2) * T^2.
  The mode-equivalent *collecting area* is A_coh = T^2 lambda^2 R^2 / (2 pi w(R)^2).
  It differs from the effective beam area *at the target*, pi*w(R)^2, in
  Piggott et al., arXiv 2502.09736. The factor 1/2 selects one polarization.
- ToF receiver: hard aperture, polarization-insensitive multimode detector whose pixel
  field of view equals one mesh cell (pixels tile the field).
- Mode (speckle) counts from Goodman's integrated-speckle formula
  M = A^2 / Integral[ K_ap(d) |mu(d)|^2 d^2d ], with |mu|^2 from van Cittert-Zernike.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle


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


def export_figure(fig: plt.Figure, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".png"), dpi=600)
    fig.savefig(stem.with_suffix(".pdf"))
    plt.close(fig)


# ---------------------------------------------------------------- physics
LAM_COH = 1550e-9  # m
LAM_TOF = 940e-9  # m: the 940 nm SPAD ToF model of sections C0 subsection 10 and C7a
DEG = np.pi / 180
W0_OVER_D = 0.45  # Gaussian waist / hard-aperture diameter
TRUNC = 1 - np.exp(-2 * (0.5 / W0_OVER_D) ** 2)  # one-way truncation efficiency
FOV_SR = (120 * DEG) * (25 * DEG)
FRAME_HZ = 10.0


def w0_of(D):
    return W0_OVER_D * D


def spot_radius(R, D, lam=LAM_COH):
    """1/e^2 intensity radius of a collimated Gaussian beam at range R."""
    w0 = w0_of(D)
    zr = np.pi * w0**2 / lam
    return w0 * np.sqrt(1 + (R / zr) ** 2)


def a_coh(R, D, lam=LAM_COH):
    """Effective collecting area of a monostatic single-mode receiver (m^2)."""
    w = spot_radius(R, D, lam)
    return TRUNC**2 * lam**2 * R**2 / (2 * np.pi * w**2)


def a_coh_ceiling(R, lam=LAM_COH):
    """Best possible collimated single-mode area at range R (confocal waist, no truncation)."""
    return lam * R / 4


def mesh_pitch_from_rate(rate_pts_s, fov_sr=FOV_SR, frame_hz=FRAME_HZ):
    """Square mesh pitch (rad) for a given point rate over the field."""
    return np.sqrt(fov_sr * frame_hz / rate_pts_s)


def coverage(R, D, theta, lam=LAM_COH):
    """Nominal 1/e^2 spot-area / square-cell-area, capped at one.

    This is an area bookkeeping fraction, not gap-free geometric coverage or
    a probability of detecting a target between sample centres.
    """
    return np.minimum(1.0, np.pi * spot_radius(R, D, lam) ** 2 / (R * theta) ** 2)


def a_full_coverage(theta, lam=LAM_COH):
    """Mode-equivalent collecting area when pi*w^2 equals one square-cell area."""
    return TRUNC**2 * lam**2 / (2 * theta**2)


def aperture_overlap(d, a):
    """Autocorrelation (overlap area) of a circular aperture of radius a at shift d."""
    u = np.clip(d / (2 * a), 0, 1)
    return 2 * a**2 * (np.arccos(u) - u * np.sqrt(1 - u**2))


def goodman_M_gaussian_spot(D, w_t_over_R, lam):
    """Speckle degrees of freedom across a circular aperture, Gaussian spot of radius w_t."""
    a = D / 2
    d = np.linspace(0, 2 * a, 20001)
    mu2 = np.exp(-(np.pi**2) * (w_t_over_R**2) * d**2 / lam**2)
    integral = np.trapezoid(aperture_overlap(d, a) * mu2 * 2 * np.pi * d, d)
    return (np.pi * a**2) ** 2 / integral


def goodman_M_square_cell(D, theta, lam, n=1601):
    """Speckle degrees of freedom across a circular aperture, uniform square cell theta x theta."""
    a = D / 2
    x = np.linspace(-2 * a, 2 * a, n)
    dx = x[1] - x[0]
    X, Y = np.meshgrid(x, x)
    mu2 = np.sinc(theta * X / lam) ** 2 * np.sinc(theta * Y / lam) ** 2
    K = aperture_overlap(np.hypot(X, Y), a)
    integral = np.sum(K * mu2) * dx * dx
    return (np.pi * a**2) ** 2 / integral


def eq_diam_mm(area_m2):
    return 2 * np.sqrt(area_m2 / np.pi) * 1e3


def circle_touch_probability(width, height, pitch, radius):
    """Grid-offset fraction for a circular contour touching a rectangle.

    The rectangle starts at the origin. A square sampling lattice is shifted
    uniformly over one pitch in each axis. Integrate over horizontal offset;
    the accepted vertical offset length is the rectangle height dilated by
    the circular contour at that horizontal distance.
    """
    x = np.linspace(0.0, pitch, 20001)
    dx = np.where(x <= width, 0.0, np.minimum(x - width, pitch - x))
    dy = np.sqrt(np.maximum(0.0, radius**2 - dx**2))
    accepted_y = np.where(dx <= radius, np.minimum(pitch, height + 2 * dy), 0.0)
    return np.trapezoid(accepted_y, x) / pitch**2


# ---------------------------------------------------------------- tables
def print_tables():
    print("Truncation efficiency (one way):", round(TRUNC, 3))
    print("\n=== Table 1: speckle / spatial modes per sample (Goodman) ===")
    D_tof = 25e-3
    for th_deg in [0.1, 0.05, 0.025]:
        th = th_deg * DEG
        m_tof = goodman_M_square_cell(D_tof, th, LAM_TOF)
        simple = (np.pi * D_tof**2 / 4) * th**2 / LAM_TOF**2
        print(f"ToF 25 mm, {LAM_TOF*1e9:.0f} nm, pixel {th_deg} deg: M_Goodman = {m_tof:.0f} "
              f"(simple A*Omega/lambda^2 = {simple:.0f})")
    for D in [20e-3, 10e-3]:
        for th_deg in [0.05, 0.1]:
            th = th_deg * DEG
            wt = th / np.sqrt(np.pi)  # pi w^2 = cell area -> w/R
            m = goodman_M_gaussian_spot(D, wt, LAM_COH)
            print(f"Coherent {D*1e3:.0f} mm aperture, 1550 nm, 1/e2 spot area matched to {th_deg} deg cell: speckles across aperture M = {m:.0f}")
    for D in [20e-3]:
        for R in [100, 200]:
            wt = spot_radius(R, D) / R
            print(f"Coherent {D*1e3:.0f} mm, own (matched) spot at {R} m: M = {goodman_M_gaussian_spot(D, wt, LAM_COH):.2f}")

    print("\n=== Table 2: 20 mm coherent aperture on a 0.05 deg mesh ===")
    D = 20e-3
    th = 0.05 * DEG
    a_hard = np.pi * D**2 / 4
    print("R [m] | spot 1/e2 dia [cm] | mesh pitch [cm] | nominal 1/e2 area fraction | A_coh [mm2] (eq dia mm) | hard/A_coh | A_area-matched [mm2] (eq dia) | hard/A_matched")
    for R in [50, 100, 150, 200, 250, 300]:
        s = 2 * spot_radius(R, D) * 100
        p = R * th * 100
        c = coverage(R, D, th)
        ac = a_coh(R, D)
        af = a_full_coverage(th)
        print(f"{R:4d} | {s:5.1f} | {p:5.1f} | {c*100:5.1f}% | {ac*1e6:6.1f} ({eq_diam_mm(ac):4.1f}) | {a_hard/ac:5.1f} | {af*1e6:5.2f} ({eq_diam_mm(af):4.2f}) | {a_hard/af:5.0f} ({10*np.log10(a_hard/af):4.1f} dB)")
    print("ToF 25 mm hard area:", round(np.pi * 0.025**2 / 4 * 1e6, 0), "mm2; ideal pixels tile the field")
    print("Ceiling lambda*R/4 at 100/200/300 m [mm2]:", [round(a_coh_ceiling(R) * 1e6, 1) for R in (100, 200, 300)])
    print("Identity A_coh*nominal spot-area fraction below saturation at 0.05 deg [mm2]:", round(a_full_coverage(th) * 1e6, 2))

    print("\n=== Table 2b: geometric overlap fraction for small objects, 20 mm coherent, 0.05 deg mesh ===")
    print("(centre = spot centre inside object; any = 1/e^2 spot touches object; ToF fill = fraction of one pixel)")
    for R in [100, 200, 250]:
        p = R * th
        d = 2 * spot_radius(R, D)
        for (wo, ho) in [(0.10, 0.10), (0.20, 0.15)]:
            pc = min(1, wo / p) * min(1, ho / p)
            pa = circle_touch_probability(wo, ho, p, d / 2)
            fill = min(1, wo / p) * min(1, ho / p)
            print(f"R {R} m, {wo*100:.0f}x{ho*100:.0f} cm: centre {pc:.2f}, any {pa:.2f}; ToF best-case fill {fill:.2f}")

    print("\n=== Table 3: point rate -> mesh (120 x 25 deg, 10 Hz) ===")
    for rate in [0.4e6, 1e6, 5e6, 12e6, 25e6, 40e6]:
        p = mesh_pitch_from_rate(rate)
        print(f"{rate/1e6:5.1f} Mpts/s: pitch {p/DEG:.3f} deg; spacing {p*100*100:.1f} cm @100 m, {p*200*100:.1f} cm @200 m;"
              f" 20 mm coherent nominal 1/e2 area fraction @200 m {coverage(200, 20e-3, p)*100:.2f}%")


# ---------------------------------------------------------------- figure 1: mesh at the front
SCENE = {
    "car": (0.10, 0.15, 1.80, 1.50),  # x, y, w, h (m): rear of a car
    "debris_small": (2.25, 0.00, 0.10, 0.10),  # 10 x 10 cm
    "debris_large": (2.60, 0.00, 0.20, 0.15),  # 20 x 15 cm
}
WINDOW = (-0.05, 3.00, -0.10, 1.92)


def rect_overlap(x0, y0, w0, h0, x1, y1, w1, h1):
    dx = max(0.0, min(x0 + w0, x1 + w1) - max(x0, x1))
    dy = max(0.0, min(y0 + h0, y1 + h1) - max(y0, y1))
    return dx * dy


def fill_fraction(cx, cy, p):
    """Fraction of a p x p cell centred at (cx, cy) covered by scene objects."""
    x0, y0 = cx - p / 2, cy - p / 2
    return min(1.0, sum(rect_overlap(x0, y0, p, p, *r) for r in SCENE.values()) / p**2)


def spot_overlap_fraction(cx, cy, w):
    """Geometric overlap of an equal-area square proxy, not Gaussian return power."""
    s = np.sqrt(np.pi) * w
    return min(1.0, sum(rect_overlap(cx - s / 2, cy - s / 2, s, s, *r) for r in SCENE.values()) / s**2)


LABELS = {  # text, anchor position (m)
    "car": ("car rear 1.8 × 1.5 m", (0.10, 1.70)),
    "debris_small": ("10 × 10 cm", (1.98, 0.20)),
    "debris_large": ("20 × 15 cm", (2.42, 0.38)),
}


def draw_scene(ax, label=False):
    for name, (x, y, w, h) in SCENE.items():
        ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=COLORS["neutral"], linewidth=0.9, zorder=3))
        if label:
            text, (tx, ty) = LABELS[name]
            ax.text(tx, ty, text, color=COLORS["text"], zorder=4)
    ax.axhline(0.0, color=COLORS["annotation"], linewidth=0.6, zorder=1)
    ax.set_xlim(WINDOW[0], WINDOW[1])
    ax.set_ylim(WINDOW[2], WINDOW[3])
    ax.set_aspect("equal")


def cell_centres(p):
    xs = np.arange(WINDOW[0] - p, WINDOW[1] + p, p) + p / 2
    ys = np.arange(WINDOW[2] - p, WINDOW[3] + p, p) + p / 2
    return xs, ys


def figure_mesh(out_dir: Path):
    theta = 0.05 * DEG
    D_coh, D_tof = 20e-3, 25e-3
    fig, axes = plt.subplots(2, 3, figsize=(8.6, 4.4), constrained_layout=True)
    for row, R in enumerate([100, 200]):
        p = R * theta
        w = spot_radius(R, D_coh)
        xs, ys = cell_centres(p)
        # (a) coherent, native Gaussian beam: nominal 1/e^2 contours
        ax = axes[row, 0]
        for cx in xs:
            for cy in ys:
                f = spot_overlap_fraction(cx, cy, w)
                ax.add_patch(Circle((cx, cy), w, facecolor=COLORS["warm_accent"] if f > 0 else COLORS["primary"],
                                    edgecolor="none", alpha=0.25 + 0.7 * f if f > 0 else 0.45, zorder=2))
        draw_scene(ax, label=True)
        ax.set_title(f"Coherent, 20 mm, native spot ({2*w*100:.1f} cm)\n"
                     f"$R$ = {R} m, mesh {p*100:.1f} cm; 1/$e^2$ area/cell {coverage(R, D_coh, theta)*100:.1f}%")
        # (b) coherent, mode widened until nominal spot area equals cell area
        ax = axes[row, 1]
        wt = p / np.sqrt(np.pi)
        af = a_full_coverage(theta)
        for cx in xs:
            for cy in ys:
                f = fill_fraction(cx, cy, p)
                ax.add_patch(Circle((cx, cy), wt, facecolor=COLORS["purple_accent"], alpha=0.08 + 0.6 * f,
                                    edgecolor=COLORS["purple_accent"], linewidth=0.2, zorder=2))
        draw_scene(ax)
        ax.set_title(f"Coherent, 1/$e^2$ spot area = cell area\n"
                     f"mode area {eq_diam_mm(af):.1f} mm eq.; "
                     f"{np.pi*D_coh**2/4/af:.0f}$\\times$ below 20 mm hard area")
        # (c) ToF pixels integrating the whole cell
        ax = axes[row, 2]
        for cx in xs:
            for cy in ys:
                f = fill_fraction(cx, cy, p)
                ax.add_patch(Rectangle((cx - p / 2, cy - p / 2), p, p, facecolor=COLORS["cool_accent"],
                                       alpha=0.06 + 0.7 * f, edgecolor=COLORS["cool_accent"], linewidth=0.2, zorder=2))
        draw_scene(ax)
        ax.set_title(f"ToF, 25 mm, pixels tile each cell\n"
                     f"shading = fraction of pixel filled (relative signal)")
    for ax in axes.flat:
        ax.set_xlabel("Horizontal position at target (m)")
        ax.set_ylabel("Height (m)")
    export_figure(fig, out_dir / "coherent_mode_coverage_mesh")


# ---------------------------------------------------------------- figure 2: scaling curves
def figure_scaling(out_dir: Path):
    R = np.linspace(10, 400, 400)
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 4.3), constrained_layout=True)
    below = dict(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, handlelength=2.2, columnspacing=1.0)
    apertures = [5e-3, 10e-3, 20e-3, 30e-3]
    colors = [COLORS["teal_accent"], COLORS["purple_accent"], COLORS["primary"], COLORS["brown_accent"]]

    # (a) spot diameter vs mesh spacing
    ax = axes[0]
    for D, c in zip(apertures, colors):
        ax.plot(R, 2 * spot_radius(R, D) * 100, color=c, lw=LW, label=f"Coherent spot, $D$ = {D*1e3:.0f} mm")
    for th_deg, c in zip([0.1, 0.05, 0.025], [COLORS["neutral"], COLORS["grey_accent"], COLORS["annotation"]]):
        ax.plot(R, R * th_deg * DEG * 100, color=c, lw=LW, ls=DASH, label=f"Mesh pitch {th_deg}°")
    ax.set_yscale("log")
    ax.set_xlabel("Range, $R$ (m)")
    ax.set_ylabel("Size at target (cm)")
    ax.set_title("(a) Coherent spot (1/$e^2$ diameter) vs mesh pitch")
    ax.legend(**below)

    # (b) effective collecting area vs range
    ax = axes[1]
    for D, c in zip(apertures, colors):
        ax.plot(R, a_coh(R, D) * 1e6, color=c, lw=LW, label=f"Coherent, native spot, $D$ = {D*1e3:.0f} mm")
    ax.plot(R, a_coh_ceiling(R) * 1e6, color=COLORS["neutral"], lw=LW, ls=DASH, label=r"Single-mode ceiling $\lambda R/4$")
    for th_deg, ls in [(0.05, DASH), (0.025, ":")]:
        ax.axhline(a_full_coverage(th_deg * DEG) * 1e6, color=COLORS["warm_accent"], lw=LW, ls=ls,
                   label=f"Coherent, area-matched, {th_deg}° mesh")
    ax.axhline(np.pi * 0.025**2 / 4 * 1e6, color=COLORS["cool_accent"], lw=LW, label="ToF, 25 mm, tiled pixels")
    ax.set_yscale("log")
    ax.set_ylim(0.5, 2000)
    ax.set_xlabel("Range, $R$ (m)")
    ax.set_ylabel("Effective collecting area (mm$^2$)")
    ax.set_title("(b) Usable aperture per sample")
    ax.legend(**below)

    # (c) trade at 200 m on a 0.05 deg mesh: vary the coherent aperture
    ax = axes[2]
    Rt, th = 200.0, 0.05 * DEG
    D_scan = np.geomspace(0.5e-3, 40e-3, 400)
    cov = coverage(Rt, D_scan, th)
    ac = a_coh(Rt, D_scan)
    ax.plot(cov * 100, ac * 1e6, color=COLORS["primary"], lw=LW, label="Coherent, vary aperture $D$")
    cgrid = np.geomspace(0.1, 100, 50)
    ax.plot(cgrid, a_full_coverage(th) * 1e6 / (cgrid / 100), color=COLORS["neutral"], lw=LW, ls=DASH,
            label=r"Model identity: $A_\mathrm{mode}\,c = \frac{T^2}{2}(\lambda/\theta)^2$")
    for Dm in [2e-3, 5e-3, 20e-3]:
        ax.plot(coverage(Rt, Dm, th) * 100, a_coh(Rt, Dm) * 1e6, "o", color=COLORS["warm_accent"], ms=4)
        ax.annotate(f"{Dm*1e3:.0f} mm", (coverage(Rt, Dm, th) * 100, a_coh(Rt, Dm) * 1e6), textcoords="offset points",
                    xytext=(5, 4), color=COLORS["text"])
    ax.plot(100, np.pi * 0.025**2 / 4 * 1e6, "s", color=COLORS["cool_accent"], ms=5, label="ToF, 25 mm")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Nominal 1/$e^2$ spot area / cell, $c$ (%)")
    ax.set_ylabel("Effective collecting area (mm$^2$)")
    ax.set_title("(c) Trade at 200 m, 0.05° mesh")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=1, handlelength=2.2)
    export_figure(fig, out_dir / "coherent_mode_coverage_scaling")


if __name__ == "__main__":
    configure_plot_style()
    out = OUT_DIR
    print_tables()
    figure_mesh(out)
    figure_scaling(out)
    print("\nFigures written to", out)
