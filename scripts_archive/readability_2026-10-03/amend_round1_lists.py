"""Amend the "new" text of individual Round 1 edits after a read-through, before the merge.

Each amendment names the edit list, the edit id, an exact substring of that edit's "new" text (which must occur
exactly once) and its replacement. The edit lists are rewritten in place (a .bak copy of each is kept the first
time). The reasons are given next to each amendment.
Usage: python amend_round1_lists.py
"""
import json
import shutil
from pathlib import Path

EDITS = Path(__file__).resolve().parent / "edits"

AMEND = [
    # Thermal cameras at or below 9 Hz are still listed (ECCN 6A993.a); only the stricter entry needs > 9 Hz.
    ("01_A3-A6_E2-E5", "01_A3-A6_E2-E5-005",
     "and is export-controlled if it runs faster than 9 Hz. Its Export Control Classification Number (ECCN) is then 6A003.b.4.b;",
     "and falls under the stricter of two export-control entries if it runs faster than 9 Hz: its Export Control Classification Number (ECCN) is then 6A003.b.4.b;"),
    # No second-person address in the report.
    ("01_A3-A6_E2-E5", "01_A3-A6_E2-E5-018",
     "to an eye adapted to the road lit by your own low beam,",
     "to an eye adapted to the road lit by the driver's own low beam,"),
    # Walk-off keeps the symbol of Eq. (71) (§C4d) and Eq. (141) (§C10); delta-theta (lower case) is the point spacing.
    ("02_C0_parts1-9", "02_C0_parts1-9-023", "*Walk-off*, $\\theta_{\\rm wo}=2R\\dot\\theta/c$:",
     "*Walk-off*, $\\Delta\\theta=2R\\dot\\theta/c$:"),
    ("02_C0_parts1-9", "02_C0_parts1-9-023", "at an angle $\\theta_{\\rm wo}$ away from the LO's direction.",
     "at an angle $\\Delta\\theta$ away from the LO's direction."),
    ("02_C0_parts1-9", "02_C0_parts1-9-023", "gives $\\theta_{\\rm wo}=2\\times200\\times796",
     "gives $\\Delta\\theta=2\\times200\\times796"),
    # The trade-off sentence mixed the fixed-point-rate and fixed-frame-rate cases.
    ("02_C0_parts1-9", "02_C0_parts1-9-028",
     "so at a fixed point rate it quarters the frame rate or needs four times the channels.",
     "so it either quarters the frame rate at a fixed point rate or, at a fixed frame rate, needs four times the point rate, for example four times the channels."),
    # e^{2.391} = 10.93, so 3,721 x 10.93 = 4.07e4 (1.7% above 4.0e4); 61 m is the rounded root (60.8 m).
    ("02_C0_parts1-9", "02_C0_parts1-9-046",
     "=3{,}721\\times10.9=4.06\\times10^4$ m², within 1.5% of $(200\\ {\\rm m})^2=4.0\\times10^4$ m², as required.",
     "=3{,}721\\times10.93=4.07\\times10^4$ m², within 2% of $(200\\ {\\rm m})^2=4.0\\times10^4$ m², as required (61 m is the root rounded from 60.8 m)."),
    # Same tag as §C4c, where the original paper was not read (legend: relayed by a secondary source = [S]).
    ("02_C0_parts1-9", "02_C0_parts1-9-048", "[I, Wojtanowski 2014 via survey]",
     "[S, Wojtanowski et al. 2014, relayed by a survey]"),
    # 10.8-11.9 cm^-1 over 1 mm transmits e^-1.08 to e^-1.19, i.e. 34% to 30%.
    ("04_C4_C4b_C4c", "04_C4_C4b_C4c-012", "(it transmits 34%)", "(it transmits 30–34%)"),
    # §C7a(b) and §C7b 2(i): only a gated transmitter stays within 9.1 W at 25 Mpts/s; ungated it emits 8.6-9.6 W.
    ("04_C4_C4b_C4c", "04_C4_C4b_C4c-045",
     "At 200 m, eye safety therefore does not limit FMCW point rate up to 25 Mpts/s: the §C7a model's FMCW needs 3.0 W at 10 Mpts/s and 7.6 W at 25 Mpts/s, within the 9.1 W allowance, and heat and wall-plug efficiency (optical output power per unit of electrical input power) bind first (§C7a).",
     "At 200 m, eye safety therefore binds FMCW point rate only near 25 Mpts/s: the §C7a model's FMCW needs 3.0 W of useful light at 10 Mpts/s and 7.6 W at 25 Mpts/s, within the 9.1 W allowance, but an ungated transmitter, which also emits during the round trips, sends 8.6–9.6 W at 25 Mpts/s and reaches it (§C7a(b); §C7b subsection 2(i)). Below that, heat and wall-plug efficiency (optical output power per unit of electrical input power) bind first (§C7a)."),
    # Keep the residual risks in the short answer; the reviewer only asked to stop repeating the judgement.
    ("05_C4d_C8_C9", "05_C4d_C8_C9-065",
     "In short, foreign pulses are common before rejection, and the receiver's rejection logic decides whether they become false points; the judgement below gives the detail.",
     "In short, foreign pulses are common in dense traffic, and the receiver's rejection logic decides whether they become false points. The residual risks are identical units firing in step, saturation when one lidar looks straight into another, and products without that logic; the judgement below gives the detail."),
    # The per-point background count is in §C7b subsection 1 (3.66e8 x 20.8 us x 0.784 = 5,968, i.e. about 5,970).
    ("06_C5_C5a_C6", "06_C5_C5a_C6-013", "(≈5,960 in the central case of §C0 subsection 10.3, built from the rates of §C6(d))",
     "(≈5,970 in the central case of §C7b subsection 1, built from the rates of §C6(d))"),
    # Same symbol as §C4, where alpha_Si separates silicon absorption from other alphas.
    ("06_C5_C5a_C6", "06_C5_C5a_C6-014", "(absorption length $1/\\alpha\\approx35$ µm",
     "(absorption length $1/\\alpha_{\\rm Si}\\approx35$ µm"),
    # §D7 says LightIC calls it a "custom SoC" whose description matches indie's chip; say so without implying a fact.
    ("07_C7_C7a_F6", "07_C7_C7a_F6-009",
     "with a custom system-on-chip (SoC) that matches indie Semiconductor's iND83301 \"Surya\" (§D7).",
     "with what it calls a \"custom\" system-on-chip (SoC), whose description matches indie Semiconductor's iND83301 \"Surya\" (§D7)."),
    # The two edges are those of the beam's footprint on the mirror, moving along the mirror normal.
    ("07_C7_C7a_F6", "07_C7_C7a_F6-016", "the difference between the velocities of the footprint's two edges along the beam.",
     "the difference between the normal velocities of the two edges of the beam's footprint on the mirror."),
    # Same value in both places (8.6e-3 x 2.4e-12 x 0.008 x 0.5 = 8.3e-17 W).
    ("08_C7b", "08_C7b-022", "\\times0.008\\times0.5\\approx8\\times10^{-17}$ W.",
     "\\times0.008\\times0.5\\approx8.3\\times10^{-17}$ W."),
    # The 2% is an assumption with no source (§C10.3a item 5 and §C10.4 now say so); same wording here.
    ("09_C10_part1", "09_C10_part1-004",
     "at the ≈2% nominal footprint fraction it actually uses (defined below), it gets ≈6 mm (§C10.3a, item 5).",
     "at an assumed ≈2% nominal footprint fraction (defined below), it would get ≈6 mm (§C10.3a, item 5)."),
    # The consistency check is the report's own calculation.
    ("11_E9-E12", "11_E9-E12-002", "and they should not be rescaled to other loads.",
     "and they should not be rescaled to other loads [E]."),
]

lists = {}
for name, eid, old, new in AMEND:
    if name not in lists:
        path = EDITS / f"{name}.json"
        bak = path.with_suffix(".json.bak")
        if not bak.exists():
            shutil.copyfile(path, bak)
        lists[name] = (path, json.loads(path.read_text(encoding="utf-8")))
    data = lists[name][1]
    edits = data if isinstance(data, list) else data["edits"]
    hit = [e for e in edits if e["id"] == eid]
    assert len(hit) == 1, (eid, len(hit))
    k = hit[0]["new"].count(old)
    assert k == 1, (eid, old[:60], k)
    hit[0]["new"] = hit[0]["new"].replace(old, new)
    print("amended", eid)
for path, data in lists.values():
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("written", path.name)
