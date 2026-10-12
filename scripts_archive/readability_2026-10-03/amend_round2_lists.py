"""Amend the "new" text of individual Round 2 edits after a read-through, before the merge.

Same mechanism as amend_round1_lists.py: each amendment names the edit list, the edit id, an exact substring of
that edit's "new" text (which must occur exactly once) and its replacement; a .bak copy of each list is kept the
first time. The reasons are given next to each amendment.
Usage: python amend_round2_lists.py
"""
import json
import shutil
from pathlib import Path

EDITS = Path(__file__).resolve().parent / "edits" / "round2"

AMEND = [
    # §C10.2 item 5 counts the OPA's optical loss separately (eta_OPA), so eta is the detector efficiency 0.8 with
    # ideal mixing (the item's original 0.4 = polarization 0.5 x QE 0.8, with polarization now in A_mode). The design
    # value 0.25 of §C0 10.1 already contains a free-space chain's optics loss and would count that loss twice.
    ("R2E_C10", "R2E_C10-003",
     "and $\\eta=0.25$, the coherent design efficiency of §C0 subsection 10.1 (optics × detector × mixing), with the OPA's own loss counted separately in $\\eta_{\\rm OPA}$.",
     "and $\\eta=0.8$, the detector's quantum efficiency with ideal mixing: the OPA's optical loss is counted separately in $\\eta_{\\rm OPA}$, so the design value 0.25 of §C0 subsection 10.1, which already contains a free-space chain's optics loss, would count it twice."),
    ("R2E_C10", "R2E_C10-004",
     "and $41\\times0.25=10.3$ after the efficiency.",
     "and $41\\times0.8=32.8$ after the efficiency."),
    ("R2E_C10", "R2E_C10-005",
     "about **6.5, 2.6 and 0.41 photons** are detected. The monostatic path applies each loss twice, so the factors $\\eta_{\\rm OPA}^2$ are $10^{-0.2}$, $10^{-0.6}$ and $10^{-1.4}$: $10.3\\times0.631=6.5$, $10.3\\times0.251\\approx2.58$ and $10.3\\times0.0398=0.41$.",
     "about **21, 8.2 and 1.3 photons** are detected. The monostatic path applies each loss twice, so the factors $\\eta_{\\rm OPA}^2$ are $10^{-0.2}$, $10^{-0.6}$ and $10^{-1.4}$: $32.8\\times0.631=20.7$, $32.8\\times0.251=8.23$ and $32.8\\times0.0398=1.31$."),
    # The amendments of R2E_C10-006 and -008 (eta = 0.8 with 60 beams) were taken over by the agent's own revision of
    # the list, which keeps eta = 0.8 and counts 92 beams at the dwell 5 us + 2 tau = 7.67 us (decision 1); they are
    # therefore no longer applied here.
    ("R2E_C10", "R2E_C10-007",
     "a waveguide platform that carries ≈9–100 W per beam:",
     "a waveguide platform that carries ≈3–31 W per beam:"),
    ("R2E_C10", "R2E_C10-007",
     "(the Si–SiN chip of §C10.2b takes 20 W in, against the 34–100 W per beam of single-mode looks);",
     "(the Si–SiN chip of §C10.2b takes 20 W in, against the 11–31 W per beam of looks that share one receive mode);"),
    ("R2E_C10", "R2E_C10-009",
     "That is 3–11× below the cell-filling link budget of §C10.2, item 5, Eq. (134), which needs 172–502 µJ for 88.5–259 photons at 3 dB one-way loss (5 µJ yields 2.58 detected photons there, so $5\\ \\mu{\\rm J}\\times88.5/2.58=172\\ \\mu{\\rm J}$ and $5\\ \\mu{\\rm J}\\times259/2.58=502\\ \\mu{\\rm J}$; $172/56=3.1$ and $502/44=11$).",
     "That sits at or just below the low end of the cell-filling link budget of §C10.2, item 5, Eq. (134): 54–157 µJ for 88.5–259 photons at 3 dB one-way loss (5 µJ yields 8.23 detected photons there, so $5\\ \\mu{\\rm J}\\times88.5/8.23=54\\ \\mu{\\rm J}$ and $5\\ \\mu{\\rm J}\\times259/8.23=157\\ \\mu{\\rm J}$)."),
    ("R2E_C10", "R2E_C10-061",
     "while carrying ≈9–100 W per beam (§C10.2, item 5)",
     "while carrying ≈3–31 W per beam (§C10.2, item 5)"),
    # The figure script now draws the ToF marker at the model's 21.7 counts (link_budget_scaling.py, n_tof).
    ("R2A_C0", "R2A_C0-025",
     "The dotted verticals sit at 25 and 120 photoelectrons, the two columns of the table above. The FMCW model uses 120 (four looks); the ToF model uses 21.7 (10.4), just left of the line marked \"ToF model\".",
     "The dotted verticals are the photoelectron counts used in the §C7a model: 21.7 for ToF (10.4) and 120 for FMCW (four looks)."),
    # Same rounding of the four factors as §C7b Eq. (104): 940/1550 = 0.606 and 0.164/0.25 = 0.656.
    ("R2C_C7-C7a", "R2C_C7-C7a-019",
     "$1.93\\times5.53\\times0.607\\times0.655=4.2$",
     "$1.93\\times5.53\\times0.606\\times0.656=4.2$"),
    # Eq. (96) is the receiver energy, which uses the dwell; the dwell itself is defined by Eq. (107).
    ("R2C_C7-C7a", "R2C_C7-C7a-031",
     "$T_{\\rm dwell}=12.67$ µs (Eq. (96); §C7b, Eq. (107))",
     "$T_{\\rm dwell}=12.67$ µs (the dwell of Eq. (96); §C7b, Eq. (107))"),
    # §C7b subsection 5: ungated channels up to 22.5 mW still reach 15 W, so only brighter ones need the gate.
    ("R2C_C7-C7a", "R2C_C7-C7a-046",
     "Brighter channels stay inside 15 W only with a gated transmitter:",
     "Channels brighter than ≈22 mW stay inside 15 W only with a gated transmitter:"),
    # One dwell vocabulary (decision 1): T_int is the integration time, the useful windows of the two ramps, as in
    # §C7a and §C7b; "chirp" is kept only where it means one ramp (the beat-frequency sentence of item 7).
    ("R2E2_C10_dwell", "R2E2_C10_dwell-001",
     "the chirp time $T_{\\rm int}$ of an up- and a down-ramp,",
     "the integration time $T_{\\rm int}$, the useful windows of an up- and a down-ramp,"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-001",
     "At 2–10 µs of chirp that is",
     "At 2–10 µs of integration that is"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-002",
     "at 2–10 µs of chirp. The number",
     "at 2–10 µs of integration. The number"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-002",
     "=152$ at 10 µs of chirp.",
     "=152$ at 10 µs of integration."),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-003",
     "If the chirp time is split into an up-ramp and a down-ramp, as the dwell above assumes, each ramp's chirp is half as long",
     "If the integration time is split into an up-ramp and a down-ramp, as the dwell above assumes, each ramp's useful window is half as long"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-004",
     "dwell for 10 µs of chirp)",
     "dwell for 10 µs of integration)"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-004",
     "Same with 2 µs of chirp (4.67 µs dwell)",
     "Same with 2 µs of integration (4.67 µs dwell)"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-005",
     "for 2 µs of chirp (",
     "for 2 µs of integration ("),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-007",
     "i.e. 2 µs or 10 µs of chirp)",
     "i.e. 2 µs or 10 µs of integration)"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-008",
     "dwell (10 µs of chirp) give",
     "dwell (10 µs of integration) give"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-009",
     "dwell (10 µs of chirp plus",
     "dwell (10 µs of integration plus"),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-009",
     "and only the 10 µs of chirp is integrated.",
     "and only the 10 µs of useful windows is integrated."),
    ("R2E2_C10_dwell", "R2E2_C10_dwell-011",
     "at 2–10 µs of chirp (§C10.2, item 7).",
     "at 2–10 µs of integration (§C10.2, item 7)."),
    ("R2E_C10", "R2E_C10-006",
     "at 5 µs of chirp and 3 dB",
     "at 5 µs of integration and 3 dB"),
    ("R2E_C10", "R2E_C10-006",
     "the 5 µs of chirp plus the round trips,",
     "the 5 µs of integration plus the two round trips,"),
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
    if k == 0 and new in hit[0]["new"]:
        print("already amended", eid)
        continue
    assert k == 1, (eid, old[:60], k)
    hit[0]["new"] = hit[0]["new"].replace(old, new)
    print("amended", eid)
for path, data in lists.values():
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("written", path.name)
