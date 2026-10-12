"""Listed lidar companies, 2020-2026: split-adjusted share price relative to listing.

Companion to section C3a of automotive_perception_report_2026-09-27.md.
Data: weekly split-adjusted closes from Yahoo Finance's public chart endpoint, saved in
lidar_equity_prices_weekly.csv (downloaded 27 Sep 2026).  Delisted or reassigned
tickers (Luminar LAZR, Velodyne VLDR, Quanergy QNGY, Cepton CPTN, LeddarTech LDTC) are
not served by that endpoint; their peak and terminal values are tabulated in the note
from filings and press sources instead.

Reference price (= 1 on the plot):
- SPAC listings (Aeva, Ouster, Innoviz, AEye): the first weekly close of the SPAC shell,
  about $10 before any later reverse split; the adjusted series already folds the splits in.
- IPOs (Hesai, RoboSense): the first weekly close after listing.
- MicroVision: first weekly close of January 2020 (listed since 1996).
"""

import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter


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


SERIES = [
    # ticker, label, colour, linestyle, reference start (None = first point)
    ("AEVA", "Aeva (FMCW; de-SPAC 2021)", COLORS["warm_accent"], "-", None),
    ("OUST", "Ouster (de-SPAC 2021; merged Velodyne 2023)", COLORS["primary"], "-", None),
    ("INVZ", "Innoviz (de-SPAC 2021)", COLORS["purple_accent"], "-", None),
    ("LIDR", "AEye (de-SPAC 2021)", COLORS["brown_accent"], "-", None),
    ("MVIS", "MicroVision (from Jan 2020)", COLORS["grey_accent"], DASH, date(2020, 1, 1)),
    ("HSAI", "Hesai (Nasdaq IPO 2023)", COLORS["cool_accent"], "-", None),
    ("2498.HK", "RoboSense (HKEX IPO 2024)", COLORS["teal_accent"], "-", None),
]


def load(path: Path) -> dict:
    data = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["ticker"]].append((date.fromisoformat(row["week"]), float(row["adjclose"])))
    return data


# Dated Aeva catalysts marked on panel (a) [T, company releases and press; see note §C3a]
AEVA_EVENTS = [
    (date(2025, 5, 13), "strategic equity deal, $9.26/share (LG Innotek named 29 Jul)"),
    (date(2025, 12, 3), "exclusive L3 award, top-10 European OEM"),
    (date(2026, 1, 15), "NVIDIA Hyperion reference lidar; SOA for AI data centres"),
    (date(2026, 5, 6), "Atlas C-samples to Daimler Truck"),
    (date(2026, 8, 5), "Optical Connectivity business, hyperscaler JDA, $115 M offering"),
]


def main() -> None:
    here = OUT_DIR  # outputs
    data = load(Path(__file__).resolve().parent / "lidar_equity_prices_weekly.csv")  # input sits next to the script
    configure_plot_style()
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(7.0, 7.2), constrained_layout=True,
                                  gridspec_kw={"height_ratios": [1.25, 1.0]})
    ax.axvspan(date(2020, 8, 1), date(2021, 12, 31), color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA,
               linewidth=0, label="_nolegend_", zorder=0)
    ax.text(date(2020, 9, 1), 45, "SPAC wave", color=COLORS["annotation"], va="top")
    lines = []
    series_xy = {}
    for tic, lab, col, ls, start in SERIES:
        pts = [(d, p) for d, p in data[tic] if start is None or d >= start]
        if not pts:
            continue
        d0, p0 = pts[0]
        xs = [d for d, _ in pts]
        prices = np.array([p for _, p in pts])
        ys = prices / p0
        series_xy[tic] = (xs, ys)
        ax.plot(xs, ys, color=col, lw=LW, ls=ls, label=lab)
        drawdown = prices / np.maximum.accumulate(prices)
        ax2.plot(xs, drawdown, color=col, lw=LW, ls=ls, label="_nolegend_")
        lines.append(f"{tic}: reference {d0} {p0:.4g}; peak x{ys.max():.2f}; latest x{ys[-1]:.3f} ({xs[-1]}); "
                     f"deepest drawdown {drawdown.min():.4f}; latest vs running peak {drawdown[-1]:.3f}")
    ax.axhline(1.0, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
    xs_a, ys_a = series_xy["AEVA"]
    note = ["Aeva catalysts:"]
    for k, (d, lab) in enumerate(AEVA_EVENTS, start=1):
        i = int(np.argmin([abs((x - d).days) for x in xs_a]))
        ax.plot(xs_a[i], ys_a[i], "o", ms=7, mfc="white", mec=COLORS["warm_accent"], mew=1.2, zorder=6,
                label="_nolegend_")
        ax.text(xs_a[i], ys_a[i], str(k), ha="center", va="center", color=COLORS["warm_accent"],
                fontsize=6.5, zorder=7)
        note.append(f"{k}  {lab} ({d:%b %Y})")
    ax2.text(date(2020, 1, 20), 0.0013, "\n".join(note), color=COLORS["text"], va="bottom", ha="left")
    events = [
        # date, label, label height, horizontal alignment relative to the event line
        (date(2022, 12, 13), "Quanergy Ch. 11 ", 45, "right"),
        (date(2023, 2, 10), " Velodyne–Ouster merger", 18, "left"),
        (date(2024, 9, 9), " Mobileye ends FMCW", 45, "left"),
        (date(2025, 12, 15), "Luminar Ch. 11 ", 18, "right"),
    ]
    for d, lab, y, ha in events:
        ax.axvline(d, color=COLORS["annotation"], lw=0.8, ls=DASH, label="_nolegend_")
        ax.text(d, y, lab, va="center", ha=ha, color=COLORS["annotation"])
    ax.set_yscale("log")
    ax.set_ylim(0.001, 80)
    ticks = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
    ax.yaxis.set_major_locator(FixedLocator(ticks))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}×"))
    ax.set_xlim(date(2020, 1, 1), date(2026, 10, 1))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylabel("Split-adjusted price ÷ listing price")
    ax.set_title("(a) Share price relative to listing (weekly, log scale)", loc="left")
    ax2.set_yscale("log")
    ax2.set_ylim(0.001, 1.3)
    ax2.yaxis.set_major_locator(FixedLocator([0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1]))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}×"))
    ax2.set_xlim(date(2020, 1, 1), date(2026, 10, 1))
    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax2.set_ylabel("Price ÷ running peak (drawdown)")
    ax2.set_title("(b) Drawdown from each company's prior peak", loc="left")
    ax2.axhline(0.1, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
    ax2.text(date(2020, 2, 1), 0.105, "−90%", color=COLORS["annotation"], va="bottom")
    ax2.axhline(0.01, color=COLORS["annotation"], lw=1.0, ls=":", label="_nolegend_")
    ax2.text(date(2020, 2, 1), 0.0105, "−99%", color=COLORS["annotation"], va="bottom")
    fig.legend(*ax.get_legend_handles_labels(), loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=2)
    fig.savefig(here / "lidar_equity_hype_cycle.png", dpi=600)
    fig.savefig(here / "lidar_equity_hype_cycle.pdf")
    plt.close(fig)
    (here / "lidar_equity_hype_cycle_tables.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
