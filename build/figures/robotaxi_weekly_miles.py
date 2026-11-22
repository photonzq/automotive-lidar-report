"""Robotaxi miles against Waymo's: the published totals of ten fleets, and the weekly rates that two dated totals allow.

Companion to section F7 (after Call 1) of automotive_perception_report_2026-09-27.md. The script converts the published
figures to miles, derives the weekly rates and the ratios to Waymo quoted in the section's table, prints them with
checks of the values quoted in the text, writes them to robotaxi_weekly_miles_tables.txt and draws
robotaxi_weekly_miles.png / .pdf (Figure F7.1: (a) published totals, (b) miles per week).

Inputs, as published (each operator counts something different):
  Waymo [P]: 271.3 M rider-only miles through June 2026 (Safety Impact hub, https://waymo.com/safety/impact/ ; still
      the latest figure on 21 Nov 2026); more than 220 M fully autonomous miles through the end of March 2026 and more
      than 4 M miles a week in late June (blog, 24 Jun 2026, https://waymo.com/blog/shorts/safetydata-june26/ ); more
      than 300 M fully autonomous miles by 28 Oct 2026 (Alphabet Q3 2026 call, CEO remarks,
      https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/ ).
  Baidu Apollo Go [P]: more than 300 M autonomous km, including more than 190 M km fully driverless, "to date" in the
      Q4 2025 release of 26 Feb 2026
      ( https://www.sec.gov/Archives/edgar/data/1329099/000119312526076505/d117608dex991.htm ); more than 350 M km,
      including more than 240 M km fully driverless, "to date" in the Q2 2026 release of 18 Aug 2026
      ( https://www.sec.gov/Archives/edgar/data/1329099/000119312526355431/d112854dex991.htm ); about 34 M autonomous km
      in Q3 2026 and more than 390 M km by 31 Oct 2026, with no driverless split (Q3 2026 release of 16 Nov 2026,
      https://www.sec.gov/Archives/edgar/data/1329099/000119312526462286/d767848dex991.htm ).
  Pony.ai [P]: more than 100 M km in autonomous operation, including more than 40 M km fully driverless (Pony.ai and
      Verne, PR Newswire, 10 Sep 2026,
      https://www.prnewswire.com/news-releases/ponyai-and-verne-kick-off-fully-driverless-robotaxi-test-rides-in-zagreb-302874840.html ).
  WeRide [P]: more than 55,000,000 km of L4 driving on public roads, all products, no driverless split (company
      website, read 21 Nov 2026, https://weride.ai/products ). Its Q3 2026 release gives no mileage.
  Zoox [T]: close to 2 M autonomous miles on 24 Mar 2026 (company statement quoted by TechCrunch,
      https://techcrunch.com/2026/03/24/zoox-brings-its-robotaxis-to-austin-and-miami/ ) and 3 M miles on 12 Aug 2026
      (Zoox's vice president for system design, quoted by Axios,
      https://www.axios.com/2026/08/12/zoox-robotaxi-safety-framework ). Both are rounded.
  Motional [P]: more than 2 M autonomous miles across several platform generations, no driverless split (Voluntary
      Safety Self-Assessment 2026, section 2.2,
      https://motional.com/sites/default/files/inline-files/Motional_Voluntary_Safety_Self-Assessment_2026.pdf ).
  May Mobility [P]: more than 600,000 commercial autonomous rides across 1.1 M miles in the US and Japan, three
      driver-out deployments (PR Newswire, 12 Nov 2026,
      https://www.prnewswire.com/news-releases/may-mobility-plans-to-bring-autonomous-volkswagen-id-buzz-vehicles-to-global-robotaxi-platforms-302936992.html ).
  Tesla: nearly 2 M cumulative unsupervised Robotaxi miles by 30 Sep 2026, eight times the end-June total ("grew
      eightfold quarter over quarter") [P] (Q3 2026 update,
      https://www.sec.gov/Archives/edgar/data/1318605/000162828026066738/exhibit9914.htm ); 1 M announced on 3 Sep 2026
      [T] (https://electrek.co/2026/09/03/tesla-announces-1-million-unsupervised-miles-driven-by-robotaxi/ ).
  Cruise [T]: crossed 4 M driverless miles on 10 Aug 2023, driving more than 1 M driverless miles a month (its chief
      executive, 11 Aug 2023, quoted by GM Authority,
      https://gmauthority.com/blog/2023/08/gms-cruise-racks-up-4-million-driverless-miles/ ); driverless service
      suspended in Oct 2023.
  Aurora (trucks) [P]: more than 500k driverless miles from May 2025 to late Sep 2026 (section B4 of the report).

Derivations [E]: a rate is the difference of two dated totals divided by the weeks between them; kilometres are
converted at 1.609344 km per mile; Waymo's Q2 2026 rate is the reference for every weekly ratio, and its June 2026
rider-only total the reference for every ratio of driverless totals.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import LogFormatterMathtext, NullFormatter


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
STEM = "robotaxi_weekly_miles"

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
PALE_PRIMARY = "#7891B8"  # second node of the house's muted classic colormap
ENDED = "#A9A9A9"  # a service that has stopped
COLOR_CYCLE = [COLORS["primary"], COLORS["warm_accent"], COLORS["cool_accent"], COLORS["purple_accent"],
               COLORS["teal_accent"], COLORS["brown_accent"], COLORS["grey_accent"]]
DRIVERLESS = COLORS["primary"]
ALL_AUTONOMOUS = PALE_PRIMARY
CAMERA_ONLY = COLORS["warm_accent"]


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


# ---------------------------------------------------------------- published inputs
KM_PER_MILE = 1.609344
WEEK = 7.0  # days
MONTH_WEEKS = 365.25 / 12.0 / WEEK

WAYMO_RO_MAR = 220.0e6  # more than 220 M through the end of March 2026 (a lower bound)
WAYMO_RO_JUN = 271.3e6  # through June 2026
Q2_DAYS = 91  # 1 Apr to 30 Jun 2026

BAIDU_KM_FEB, BAIDU_DL_KM_FEB = 300.0e6, 190.0e6  # more than, to 26 Feb 2026
BAIDU_KM_AUG, BAIDU_DL_KM_AUG = 350.0e6, 240.0e6  # more than, to 18 Aug 2026
BAIDU_FEB_AUG_DAYS = 173  # 26 Feb to 18 Aug 2026
BAIDU_KM_Q3 = 34.0e6
BAIDU_KM_OCT = 390.0e6  # more than, to 31 Oct 2026
Q3_DAYS = 92  # 1 Jul to 30 Sep 2026

PONY_KM, PONY_DL_KM = 100.0e6, 40.0e6  # more than, to 10 Sep 2026
WERIDE_KM = 55.0e6  # more than, all L4 products (website, read 21 Nov 2026)

ZOOX_MAR = 2.0e6  # close to 2 M on 24 Mar 2026
ZOOX_AUG = 3.0e6  # 3 M on 12 Aug 2026
ZOOX_DAYS = 141  # 24 Mar to 12 Aug 2026

MOTIONAL = 2.0e6  # more than, all autonomous miles (2026)
MAY = 1.1e6  # commercial autonomous rides, 12 Nov 2026

TESLA_SEP = 2.0e6  # nearly 2 M by 30 Sep 2026
TESLA_GROWTH_Q3 = 8.0  # cumulative miles grew eightfold quarter over quarter
TESLA_1M = 1.0e6  # announced on 3 Sep 2026
TESLA_SEP_DAYS = 27  # 3 Sep to 30 Sep 2026

CRUISE = 4.0e6  # driverless, 10 Aug 2023
CRUISE_PER_MONTH = 1.0e6  # more than, Aug 2023

AURORA_MILES = 0.5e6  # more than 500k driverless miles, May 2025 to late Sep 2026
AURORA_WEEKS = 73.0  # 1 May 2025 to 23 Sep 2026 is 510 days


def mi(km: float) -> float:
    return km / KM_PER_MILE


# ---------------------------------------------------------------- derived values [E]
waymo_q2_miles = WAYMO_RO_JUN - WAYMO_RO_MAR
waymo_week = waymo_q2_miles / (Q2_DAYS / WEEK)

baidu_dl_aug = mi(BAIDU_DL_KM_AUG)
baidu_all_oct = mi(BAIDU_KM_OCT)
baidu_feb_aug_weeks = BAIDU_FEB_AUG_DAYS / WEEK
baidu_dl_week = mi(BAIDU_DL_KM_AUG - BAIDU_DL_KM_FEB) / baidu_feb_aug_weeks
baidu_all_week_feb_aug = mi(BAIDU_KM_AUG - BAIDU_KM_FEB) / baidu_feb_aug_weeks
baidu_q3_miles = mi(BAIDU_KM_Q3)
baidu_week = baidu_q3_miles / (Q3_DAYS / WEEK)
baidu_year = baidu_week * 52.0

pony_dl = mi(PONY_DL_KM)
pony_all = mi(PONY_KM)
werides_all = mi(WERIDE_KM)

zoox_week = (ZOOX_AUG - ZOOX_MAR) / (ZOOX_DAYS / WEEK)

tesla_jun = TESLA_SEP / TESLA_GROWTH_Q3
tesla_q3_miles = TESLA_SEP - tesla_jun
tesla_q3_week = tesla_q3_miles / (Q3_DAYS / WEEK)
tesla_q3_year = tesla_q3_week * 52.0
tesla_sep_week = (TESLA_SEP - TESLA_1M) / (TESLA_SEP_DAYS / WEEK)  # an upper bound: "nearly" 2 M

cruise_week = CRUISE_PER_MONTH / MONTH_WEEKS
aurora_week = AURORA_MILES / AURORA_WEEKS

lidar_without_baidu = waymo_week + zoox_week
share_without_baidu = lidar_without_baidu / (lidar_without_baidu + tesla_sep_week)
share_with_baidu_dl = (lidar_without_baidu + baidu_dl_week) / (lidar_without_baidu + baidu_dl_week + tesla_sep_week)
share_with_baidu_all = (lidar_without_baidu + baidu_week) / (lidar_without_baidu + baidu_week + tesla_sep_week)

# Panel (a), top to bottom: (label, driverless or unsupervised total, all-autonomous total, colour of the first)
TOTALS = [
    ("Waymo, Jun 2026", WAYMO_RO_JUN, None, DRIVERLESS),
    ("Baidu Apollo Go, Aug/Oct 2026", baidu_dl_aug, baidu_all_oct, DRIVERLESS),
    ("Pony.ai, Sep 2026", pony_dl, pony_all, DRIVERLESS),
    ("WeRide, Nov 2026", None, werides_all, DRIVERLESS),
    ("Cruise, Aug 2023 (stopped)", CRUISE, None, ENDED),
    ("Zoox, Aug 2026", ZOOX_AUG, None, DRIVERLESS),
    ("Motional, 2026", None, MOTIONAL, DRIVERLESS),
    ("Tesla, Sep 2026", TESLA_SEP, None, CAMERA_ONLY),
    ("May Mobility, Nov 2026", None, MAY, DRIVERLESS),
    ("Aurora trucks, Sep 2026", AURORA_MILES, None, DRIVERLESS),
]

# Panel (b), top to bottom: (label, rate, all-autonomous rate or None, colour, prefix of the value)
RATES = [
    ("Waymo, Q2 2026", waymo_week, None, DRIVERLESS, ""),
    ("Baidu Apollo Go, 2026", baidu_dl_week, baidu_week, DRIVERLESS, ""),
    ("Tesla, Sep 2026", tesla_sep_week, None, CAMERA_ONLY, "≤"),
    ("Cruise, Aug 2023", cruise_week, None, ENDED, ">"),
    ("Tesla, Q3 2026", tesla_q3_week, None, CAMERA_ONLY, ""),
    ("Zoox, Mar–Aug 2026", zoox_week, None, DRIVERLESS, ""),
]


def table_lines() -> list[str]:
    def m(x: float) -> str:
        return f"{x / 1e6:.4g} M"

    return [
        "Totals and rates behind the section F7 table (miles; weekly ratio = rate / Waymo's Q2 2026 rate; total ratio =",
        "driverless total / Waymo's 271.3 M rider-only miles to June 2026)",
        f"Waymo: Q2 2026 rider-only miles {m(waymo_q2_miles)} over {Q2_DAYS / WEEK:.2f} weeks -> {m(waymo_week)} a week",
        f"Baidu: driverless {m(baidu_dl_aug)} (Aug 2026), total ratio {baidu_dl_aug / WAYMO_RO_JUN:.3f}; all autonomous "
        f"{m(baidu_all_oct)} (Oct 2026); driverless Feb-Aug {m(mi(BAIDU_DL_KM_AUG - BAIDU_DL_KM_FEB))} over "
        f"{baidu_feb_aug_weeks:.2f} weeks -> {m(baidu_dl_week)} a week, ratio {baidu_dl_week / waymo_week:.3f} "
        f"(all autonomous Feb-Aug {m(baidu_all_week_feb_aug)} a week); Q3 all autonomous {m(baidu_q3_miles)} -> "
        f"{m(baidu_week)} a week, ratio {baidu_week / waymo_week:.3f}, {m(baidu_year)} a year",
        f"Pony.ai: driverless {m(pony_dl)}, total ratio {pony_dl / WAYMO_RO_JUN:.4f}; all autonomous {m(pony_all)}",
        f"WeRide: all L4 products {m(werides_all)}",
        f"Zoox: {m(ZOOX_AUG - ZOOX_MAR)} over {ZOOX_DAYS / WEEK:.2f} weeks -> {m(zoox_week)} a week, ratio "
        f"{zoox_week / waymo_week:.4f}; total ratio {ZOOX_AUG / WAYMO_RO_JUN:.4f}",
        f"Motional: {m(MOTIONAL)} all autonomous; May Mobility: {m(MAY)} commercial autonomous rides",
        f"Tesla: end-June {m(tesla_jun)}; Q3 {m(tesla_q3_miles)} -> {m(tesla_q3_week)} a week, ratio "
        f"{tesla_q3_week / waymo_week:.4f}, {m(tesla_q3_year)} a year; September at most {m(tesla_sep_week)} a week, "
        f"ratio {tesla_sep_week / waymo_week:.4f}; total ratio {TESLA_SEP / WAYMO_RO_JUN:.4f}",
        f"Cruise: {m(CRUISE)} driverless, total ratio {CRUISE / WAYMO_RO_JUN:.4f}; pace {m(cruise_week)} a week, "
        f"ratio {cruise_week / waymo_week:.4f}",
        f"Aurora trucks: {m(AURORA_MILES)} over {AURORA_WEEKS:.0f} weeks -> {m(aurora_week)} a week",
        f"Lidar-based share against Tesla's September pace: Waymo + Zoox {share_without_baidu:.3f}; with Baidu's "
        f"driverless rate {share_with_baidu_dl:.3f}; with all of Baidu's Q3 kilometres {share_with_baidu_all:.3f}",
    ]


# ---------------------------------------------------------------- checks of hand-quoted values
def check(name: str, value: float, reference: float, tol: float) -> str:
    err = value - reference
    verdict = "pass" if abs(err) <= tol else "FAIL"
    return (f"{name}: value {value:.6g}, reference {reference:.6g}, error {err:+.3g}, "
            f"tolerance {tol:.3g} -> {verdict}")


def checks() -> list[str]:
    return [
        check("Waymo Q2 2026 miles (M)", waymo_q2_miles / 1e6, 51.3, 0.05),
        check("Waymo miles a week (M)", waymo_week / 1e6, 3.95, 0.005),
        check("Baidu driverless total, Aug 2026 (M miles)", baidu_dl_aug / 1e6, 149.0, 0.5),
        check("Baidu driverless total against Waymo's", baidu_dl_aug / WAYMO_RO_JUN, 0.55, 0.005),
        check("Baidu all-autonomous total, Oct 2026 (M miles)", baidu_all_oct / 1e6, 242.0, 0.5),
        check("Baidu driverless growth, Feb-Aug (M miles)", mi(BAIDU_DL_KM_AUG - BAIDU_DL_KM_FEB) / 1e6, 31.1, 0.05),
        check("Baidu Feb-Aug weeks", baidu_feb_aug_weeks, 24.7, 0.05),
        check("Baidu driverless miles a week (M)", baidu_dl_week / 1e6, 1.26, 0.005),
        check("Baidu driverless rate against Waymo", baidu_dl_week / waymo_week, 0.32, 0.005),
        check("Baidu Q3 2026 miles (M)", baidu_q3_miles / 1e6, 21.1, 0.05),
        check("Q3 2026 weeks", Q3_DAYS / WEEK, 13.1, 0.05),
        check("Baidu all-autonomous miles a week, Q3 (M)", baidu_week / 1e6, 1.61, 0.005),
        check("Baidu all-autonomous rate against Waymo", baidu_week / waymo_week, 0.41, 0.005),
        check("Baidu miles a year at the Q3 rate (M)", baidu_year / 1e6, 84.0, 0.5),
        check("Pony.ai driverless miles (M)", pony_dl / 1e6, 24.9, 0.05),
        check("Pony.ai all-autonomous miles (M)", pony_all / 1e6, 62.1, 0.05),
        check("Pony.ai driverless total against Waymo's", pony_dl / WAYMO_RO_JUN, 0.092, 0.0005),
        check("WeRide all-product miles (M)", werides_all / 1e6, 34.2, 0.05),
        check("Zoox weeks", ZOOX_DAYS / WEEK, 20.1, 0.05),
        check("Zoox miles a week (M)", zoox_week / 1e6, 0.050, 0.0005),
        check("Zoox rate against Waymo", zoox_week / waymo_week, 0.013, 0.0005),
        check("Zoox total against Waymo's", ZOOX_AUG / WAYMO_RO_JUN, 0.011, 0.0005),
        check("Tesla end-June total (M)", tesla_jun / 1e6, 0.25, 0.0005),
        check("Tesla Q3 2026 miles (M)", tesla_q3_miles / 1e6, 1.75, 0.0005),
        check("Tesla Q3 miles a week (M)", tesla_q3_week / 1e6, 0.133, 0.0005),
        check("Tesla Q3 rate against Waymo", tesla_q3_week / waymo_week, 0.034, 0.0005),
        check("Tesla Q3 miles a year (M)", tesla_q3_year / 1e6, 6.9, 0.05),
        check("Tesla September weeks", TESLA_SEP_DAYS / WEEK, 3.86, 0.005),
        check("Tesla September miles a week, upper bound (M)", tesla_sep_week / 1e6, 0.259, 0.0005),
        check("Tesla September rate against Waymo", tesla_sep_week / waymo_week, 0.066, 0.0005),
        check("Tesla total against Waymo's", TESLA_SEP / WAYMO_RO_JUN, 0.0074, 0.00005),
        check("Weeks in a month", MONTH_WEEKS, 4.35, 0.005),
        check("Cruise miles a week, Aug 2023 (M)", cruise_week / 1e6, 0.230, 0.0005),
        check("Cruise rate against Waymo", cruise_week / waymo_week, 0.058, 0.0005),
        check("Cruise total against Waymo's", CRUISE / WAYMO_RO_JUN, 0.015, 0.0005),
        check("Aurora miles a week (M)", aurora_week / 1e6, 0.007, 0.0005),
        check("Aurora total against Waymo's", AURORA_MILES / WAYMO_RO_JUN, 0.0018, 0.00005),
        check("Waymo + Zoox + Baidu driverless miles a week (M)", (lidar_without_baidu + baidu_dl_week) / 1e6, 5.26,
              0.01),
        check("Waymo + Zoox miles a week (M)", lidar_without_baidu / 1e6, 4.0, 0.005),
        check("Lidar-based share, Waymo + Zoox", share_without_baidu, 0.94, 0.005),
        check("Lidar-based share with Baidu's driverless rate", share_with_baidu_dl, 0.95, 0.005),
        check("Lidar-based share with all of Baidu's Q3 kilometres", share_with_baidu_all, 0.96, 0.005),
    ]


# ---------------------------------------------------------------- figure
def fmt_m(x: float) -> str:
    """Millions of miles: three significant figures from 10 M up, two below."""
    v = x / 1e6
    return (f"{v:.0f}" if v >= 100 else f"{v:.1f}" if v >= 10 else f"{v:#.2g}".rstrip(".")) + " M"


def draw() -> plt.Figure:
    configure_plot_style()
    fig, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(4.2, 6.0), constrained_layout=True,
                                     gridspec_kw={"height_ratios": [len(TOTALS), len(RATES) + 0.6]})
    height = 0.64

    # (a) published totals
    for row, (label, primary, everything, color) in enumerate(TOTALS):
        if everything is not None:
            ax_a.barh(row, everything, height=height, color=ALL_AUTONOMOUS, edgecolor="white", linewidth=0.5)
        if primary is not None:
            ax_a.barh(row, primary, height=height, color=color, edgecolor="white", linewidth=0.5)
        parts = [fmt_m(v) for v in (primary, everything) if v is not None]
        right = max(v for v in (primary, everything) if v is not None)
        ax_a.text(right * 1.15, row, " / ".join(parts), ha="left", va="center", fontsize=FONT_SIZE)
    ax_a.set_yticks(range(len(TOTALS)))
    ax_a.set_yticklabels([t[0] for t in TOTALS])
    ax_a.set_ylim(len(TOTALS) - 0.5, -0.5)
    ax_a.set_xlim(1e5, 1e10)
    ax_a.set_xlabel("Published total (miles)")
    ax_a.set_title("(a) Published totals", loc="left")

    # (b) miles per week
    for row, (label, rate, everything, color, prefix) in enumerate(RATES):
        if everything is not None:
            ax_b.barh(row, everything, height=height, color=ALL_AUTONOMOUS, edgecolor="white", linewidth=0.5)
        ax_b.barh(row, rate, height=height, color=color, edgecolor="white", linewidth=0.5)
        ratio = rate / waymo_week
        if row == 0:
            note = f"{rate / 1e6:.2f} M (1)"
        elif everything is not None:
            note = f"{rate / 1e6:.2f}–{everything / 1e6:.2f} M ({ratio:.2g}–{everything / waymo_week:.2g})"
        else:
            value = f"{rate / 1e6:#.2g}" if rate < 1e5 else f"{rate / 1e6:.3g}"
            note = f"{prefix}{value} M ({ratio:.2g})"
        right = everything if everything is not None else rate
        ax_b.text(right * 1.15, row, note, ha="left", va="center", fontsize=FONT_SIZE)
    ax_b.set_yticks(range(len(RATES)))
    ax_b.set_yticklabels([r[0] for r in RATES])
    ax_b.set_ylim(len(RATES) - 0.5, -0.5)
    ax_b.set_xlim(1e4, 1e9)
    ax_b.set_xlabel("Miles per week")
    ax_b.set_title("(b) Miles per week (fraction of Waymo's)", loc="left")

    for ax in (ax_a, ax_b):
        ax.tick_params(axis="y", length=0)
        ax.set_xscale("log")
        ax.xaxis.set_major_formatter(LogFormatterMathtext())
        ax.xaxis.set_minor_formatter(NullFormatter())

    handles = [
        Patch(facecolor=DRIVERLESS, edgecolor="white", label="Driverless, lidar-based"),
        Patch(facecolor=ALL_AUTONOMOUS, edgecolor="white", label="All autonomous, incl. safety operators"),
        Patch(facecolor=CAMERA_ONLY, edgecolor="white", label="Unsupervised, camera-only"),
        Patch(facecolor=ENDED, edgecolor="white", label="Driverless, service stopped"),
    ]
    ax_b.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.30, -0.28), ncol=2, handlelength=1.2,
                columnspacing=1.0, handletextpad=0.5)
    return fig


def main() -> None:
    header = [
        "Robotaxi miles against Waymo's: published totals and weekly rates (section F7, Figure F7.1) [E]",
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
