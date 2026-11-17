"""Where the cost sits in seven lidars: TechInsights' published component lists, grouped by function.

Companion to section C3d of automotive_perception_report_2026-09-27.md. The script prints the per-function sums behind
the section's table and their checks, writes them to teardown_component_costs_tables.txt and draws
teardown_component_costs.png / .pdf (Figure C3d).

Inputs [I]: the "Major components" lists of TechInsights' partial teardowns, published on Electronics360. Each list
gives ten major components in descending order of estimated cost (nine for the Valeo SCALA 2), with the quantity; the
dollar figure is TechInsights' cost estimate for the line. The lists are not complete bills of materials.
  LeiShen lidar system (model and wavelength not named; released Aug 2022), 2 Jun 2023:
      https://electronics360.globalspec.com/article/19675/techinsights-teardown-leishen-lidar-system
  Continental 3D flash lidar HFL110 (1,064 nm), 15 Mar 2024:
      https://electronics360.globalspec.com/article/20837/techinsights-teardown-continental-3d-flash-lidar
  Huawei 96-line lidar, 10 Nov 2023:
      https://electronics360.globalspec.com/article/20215/techinsights-teardown-huawei-96-line-lidar
  Valeo SCALA Gen 2, 28 Oct 2022:
      https://electronics360.globalspec.com/article/18818/techinsights-teardown-valeo-lidar-scala-gen-2-laser-rangefinder
  Velodyne Velarray H800, 30 Jun 2023 (the list prints "Lens #2" twice; both lines are kept):
      https://electronics360.globalspec.com/article/19744/techinsights-teardown-velodyne-velarray-h800-lidar
  Ouster OS1-64, 25 Feb 2022 ("Pettier module" in the list is a Peltier module):
      https://electronics360.globalspec.com/article/17802/techinsights-teardown-ouster-os1-64-lidar-sensor
  Hesai ATX, 29 Aug 2025:
      https://electronics360.globalspec.com/article/22673/techinsights-teardown-hesai-atx-lidar
  Innovusion (Seyond) Falcon Kinetic, 10 Feb 2023, checked only: its article gives the manufacturing cost by category
  instead of a component list, so it is not drawn:
      https://electronics360.globalspec.com/article/19252/techinsights-teardown-innovusion-falcon-kinetic

Grouping [E]: each listed line is assigned to one function: the laser source (lasers, laser modules, the fibre and
fibre-coupled parts of the LeiShen unit, and the H800's GaN laser drivers); the detector; mirrors (the Huawei unit's
four rotating-mirror facets and the ATX's transmitter and receiver mirrors); lenses, filters and windows (heated
filters included); processors and memory; housing and frames (enclosures, covers, mounts); and everything else
(circuit boards, cables, connectors, the vendors' own power or converter subsystems, the H800's eight capacitors and
the Ouster's Peltier module, whose purpose the article does not state).
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


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
STEM = "teardown_component_costs"

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
COLOR_CYCLE = [COLORS["primary"], COLORS["warm_accent"], COLORS["cool_accent"], COLORS["purple_accent"],
               COLORS["teal_accent"], COLORS["brown_accent"], COLORS["grey_accent"]]


def configure_plot_style() -> None:
    """Apply the project Matplotlib style without external LaTeX."""
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


# ---------------------------------------------------------------- functions (order along each bar) and colours
CATEGORIES = [
    ("laser", "Laser source (fibre, drivers)", COLORS["warm_accent"]),
    ("detector", "Detector", COLORS["purple_accent"]),
    ("mirrors", "Mirrors", COLORS["teal_accent"]),
    ("optics", "Lenses, filters, windows", COLORS["primary"]),
    ("processing", "Processors, memory", COLORS["cool_accent"]),
    ("housing", "Housing, frames", COLORS["brown_accent"]),
    ("other", "Boards, cables, other", "#A9A9A9"),
]

# ---------------------------------------------------------------- the published lists: (line, US dollars, function)
LIDARS = [
    {
        "label": "LeiShen fibre-laser unit",
        "items": [
            ("Fiber optic cable", 174.78, "laser"),
            ("Laser diode module (x2)", 142.90, "laser"),
            ("Fiber coupled laser", 56.31, "laser"),
            ("Main glass filter", 34.48, "optics"),
            ("Power box subsystem (LeiShen)", 26.96, "other"),
            ("Artix-7 FPGA (Xilinx)", 14.76, "processing"),
            ("Bottom enclosure", 13.37, "housing"),
            ("Top enclosure", 12.68, "housing"),
            ("Lens 1", 10.55, "optics"),
            ("Lens 3", 10.38, "optics"),
        ],
    },
    {
        "label": "Continental HFL110 flash",
        "items": [
            ("Laser module", 150.53, "laser"),
            ("Glass filter (x2)", 36.19, "optics"),
            ("SPAD 32 x 128 array", 30.20, "detector"),
            ("Main enclosure", 12.79, "housing"),
            ("Artix-7 FPGA (AMD)", 9.00, "processing"),
            ("Bottom enclosure", 6.57, "housing"),
            ("Lens 1", 6.21, "optics"),
            ("Lens 4", 5.72, "optics"),
            ("Lens 2", 4.67, "optics"),
            ("Connector external power", 4.16, "other"),
        ],
    },
    {
        "label": "Huawei 96-line",
        "items": [
            ("Mirror (x4)", 76.36, "mirrors"),
            ("IR glass filter with heater", 58.23, "optics"),
            ("Bottom enclosure", 35.71, "housing"),
            ("8K UHD mobile camera SoC (HiSilicon)", 30.46, "processing"),
            ("Top enclosure", 15.69, "housing"),
            ("FPGA (Lattice, x2)", 12.61, "processing"),
            ("14-layer conventional FR4/HF board", 10.98, "other"),
            ("Glass filter (x2)", 8.56, "optics"),
            ("Main board internal cover", 8.12, "housing"),
            ("Optics mount", 8.03, "housing"),
        ],
    },
    {
        "label": "Valeo SCALA 2",
        "items": [
            ("Zynq UltraScale+ SoC (Xilinx)", 52.73, "processing"),
            ("Convert box subsystem (Valeo)", 19.66, "other"),
            ("Mounting frame", 19.33, "housing"),
            ("Multichip memory, 2 GB LPDDR4 (Micron, x2)", 16.22, "processing"),
            ("Photosensor with front-end IC (Hamamatsu)", 11.92, "detector"),
            ("Plastic filter with heater element", 11.08, "optics"),
            ("Rx lens", 9.99, "optics"),
            ("6-layer rigid flex (Valeo)", 5.96, "other"),
            ("Cable power DC", 5.92, "other"),
        ],
    },
    {
        "label": "Velodyne Velarray H800",
        "items": [
            ("Small active laser (x8)", 26.15, "laser"),
            ("Artix-7 FPGA (Xilinx)", 15.15, "processing"),
            ("Middle enclosure", 13.03, "housing"),
            ("GaN power FET (x4)", 9.91, "laser"),
            ("Front enclosure", 9.82, "housing"),
            ("Back enclosure", 9.40, "housing"),
            ("Small passive safety capacitor (x8)", 6.41, "other"),
            ("Lens #2", 6.14, "optics"),
            ("Lens #2 (listed twice)", 6.14, "optics"),
            ("Lens #1", 5.53, "optics"),
        ],
    },
    {
        "label": "Ouster OS1-64",
        "items": [
            ("Artix-7 FPGA (Xilinx)", 13.43, "processing"),
            ("Mounting base", 10.93, "housing"),
            ("Small active VCSEL array", 10.46, "laser"),
            ("Dual-core Arm and programmable-logic SoC (Xilinx)", 10.13, "processing"),
            ("Peltier module", 7.53, "other"),
            ("SPAD array", 7.23, "detector"),
            ("Lens #3 (x2)", 6.51, "optics"),
            ("Lens #2 (x2)", 6.47, "optics"),
            ("DDR3L SDRAM 512 MB (Micron, x2)", 6.43, "processing"),
            ("Bottom enclosure", 6.29, "housing"),
        ],
    },
    {
        "label": "Hesai ATX",
        "items": [
            ("VCSEL array (maker unknown)", 9.72, "laser"),
            ("Main frame", 8.12, "housing"),
            ("32-bit microcontroller with memory (Infineon)", 4.99, "processing"),
            ("10-layer build-up FR4/HF board", 4.62, "other"),
            ("Lens #2", 4.43, "optics"),
            ("Top cover", 4.18, "housing"),
            ("FPGA Ti60 (Efinix)", 3.91, "processing"),
            ("Lens #1", 3.81, "optics"),
            ("Transmitter mirror", 3.77, "mirrors"),
            ("Receiver mirror", 3.59, "mirrors"),
        ],
    },
]

# Falcon Kinetic: manufacturing cost by category (US dollars), as published
FALCON_KINETIC = {
    "Modules, discretes and connectors": 276.36,
    "Non-electronic parts": 129.61,
    "Integrated circuits": 84.90,
    "Substrates": 14.53,
    "Component insertion": 6.75,
    "Final assembly and test": 5.64,
    "Card test": 2.96,
}


def sums(lidar: dict) -> dict:
    """Dollar sum of the listed lines per function, plus the total."""
    out = {key: 0.0 for key, _, _ in CATEGORIES}
    for _, dollars, cat in lidar["items"]:
        out[cat] += dollars
    out["total"] = sum(out[key] for key, _, _ in CATEGORIES)
    return out


SUMS = {lidar["label"]: sums(lidar) for lidar in LIDARS}


def table_lines() -> list[str]:
    keys = [key for key, _, _ in CATEGORIES]
    head = "Lidar | " + " | ".join(keys) + " | total (US$)"
    lines = ["Per-function sums of the listed lines, US$ (share of the listed total)", head]
    for lidar in LIDARS:
        s = SUMS[lidar["label"]]
        cells = [f"{s[k]:.2f} ({100 * s[k] / s['total']:.1f}%)" for k in keys]
        lines.append(f"{lidar['label']} | " + " | ".join(cells) + f" | {s['total']:.2f}")
    lines += ["", "Lines and their assigned function:"]
    for lidar in LIDARS:
        lines.append(f"  {lidar['label']}:")
        for name, dollars, cat in lidar["items"]:
            lines.append(f"    {dollars:8.2f}  {cat:10s}  {name}")
    fk = sum(FALCON_KINETIC.values())
    lines += ["", f"Falcon Kinetic manufacturing cost by category (not drawn): total {fk:.2f}"]
    for name, dollars in FALCON_KINETIC.items():
        lines.append(f"    {dollars:8.2f}  ({100 * dollars / fk:.1f}%)  {name}")
    return lines


# ---------------------------------------------------------------- checks of hand-quoted values
def check(name: str, value: float, reference: float, tol: float) -> str:
    err = value - reference
    verdict = "pass" if abs(err) <= tol else "FAIL"
    return (f"{name}: value {value:.6g}, reference {reference:.6g}, error {err:+.3g}, "
            f"tolerance {tol:.3g} -> {verdict}")


def checks() -> list[str]:
    s = SUMS
    fk = sum(FALCON_KINETIC.values())
    leishen_fibre = s["LeiShen fibre-laser unit"]["laser"]
    huawei = s["Huawei 96-line"]
    return [
        check("LeiShen listed total", s["LeiShen fibre-laser unit"]["total"], 497.17, 0.005),
        check("HFL110 listed total", s["Continental HFL110 flash"]["total"], 266.04, 0.005),
        check("Huawei 96-line listed total", huawei["total"], 264.75, 0.005),
        check("SCALA 2 listed total (nine lines)", s["Valeo SCALA 2"]["total"], 152.81, 0.005),
        check("H800 listed total", s["Velodyne Velarray H800"]["total"], 107.68, 0.005),
        check("OS1-64 listed total", s["Ouster OS1-64"]["total"], 85.41, 0.005),
        check("ATX listed total", s["Hesai ATX"]["total"], 51.14, 0.005),
        check("LeiShen fibre-laser lines (US$)", leishen_fibre, 373.99, 0.005),
        check("LeiShen fibre-laser share", leishen_fibre / s["LeiShen fibre-laser unit"]["total"], 0.752, 0.0005),
        check("HFL110 laser-module share", 150.53 / s["Continental HFL110 flash"]["total"], 0.566, 0.0005),
        check("ATX VCSEL-array share", 9.72 / s["Hesai ATX"]["total"], 0.190, 0.0005),
        check("Huawei mirrors + optics + housing share",
              (huawei["mirrors"] + huawei["optics"] + huawei["housing"]) / huawei["total"], 0.796, 0.0005),
        check("SCALA 2 processor and memory share", s["Valeo SCALA 2"]["processing"] / s["Valeo SCALA 2"]["total"],
              0.451, 0.0005),
        check("Falcon Kinetic manufacturing cost (US$)", fk, 520.75, 0.005),
        check("Falcon Kinetic modules, discretes and connectors share", 276.36 / fk, 0.531, 0.0005),
    ]


# ---------------------------------------------------------------- figure
def draw() -> plt.Figure:
    configure_plot_style()
    fig, ax = plt.subplots(figsize=(4.2, 3.4), constrained_layout=True)
    height = 0.66
    for row, lidar in enumerate(LIDARS):
        s = SUMS[lidar["label"]]
        left = 0.0
        for key, _, color in CATEGORIES:
            width = 100.0 * s[key] / s["total"]
            if width <= 0.0:
                continue
            ax.barh(row, width, left=left, height=height, color=color, edgecolor="white", linewidth=0.5)
            if width >= 11.0:
                ax.text(left + width / 2.0, row, f"{width:.0f}%", ha="center", va="center", color="white",
                        fontsize=FONT_SIZE)
            left += width
    ax.set_yticks(range(len(LIDARS)))
    ax.set_yticklabels([f"{lidar['label']}\nUS\\${SUMS[lidar['label']]['total']:.0f} listed" for lidar in LIDARS],
                       linespacing=1.15)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(len(LIDARS) - 0.5, -0.5)
    ax.set_xlim(0.0, 100.0)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("Share of the listed components' estimated cost (%)")
    handles = [Patch(facecolor=color, edgecolor="white", label=label) for _, label, color in CATEGORIES]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.36, -0.13), ncol=2, handlelength=1.2,
              columnspacing=1.0, handletextpad=0.5)
    return fig


def main() -> None:
    header = [
        "Where the cost sits in seven lidars: TechInsights' published component lists, grouped by function "
        "(section C3d, Figure C3d) [I/E]",
        "",
    ]
    text = "\n".join(header + table_lines() + ["", "Checks (value, reference, error, tolerance):"] + checks()) + "\n"
    print(text)
    (OUT_DIR / f"{STEM}_tables.txt").write_bytes(text.encode("utf-8"))  # LF line endings on every platform
    fig = draw()
    fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
    fig.savefig(OUT_DIR / f"{STEM}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
