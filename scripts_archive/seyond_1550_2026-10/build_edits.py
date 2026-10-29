"""Additions of 2026-10-29: Seyond's 1,550 nm receiver (from Innovusion's patents), Seyond's Hong Kong listing, and
the 1,550 nm ToF units of Benewake and LeiShen.

Sources read for these edits:
- US 11,789,128 B2 (Innovusion, priority 1 Mar 2021), claims 1-26 and the description of Figs. 12-17;
- US 11,789,132 B2 (Innovusion, priority 9 Apr 2018), claims 1-25 and the description of Figs. 11-15;
- Benewake, Horn-X2 Pro datasheet BP-DS-62 A01 (24 Jun 2022), all three pages;
- LSLiDAR (LeiShen), LS series launch release (PR Newswire, 23 Aug 2022);
- Walkers (10 Dec 2025) and PEdaily (10 Dec 2025) on Seyond's listing.
Writes edits.json (the report's Part C and Appendix 2) and appendix1_pair.json (one Appendix 1 pair, applied with
that appendix's own batch). The report is only read.
Usage: python build_edits.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = HERE.parent.parent / "automotive_perception_report_2026-09-27.md"
T = REPORT.read_text(encoding="utf-8")
WHY = "Facts not yet in the report, checked against the sources listed in build_edits.py (2026-10-29)."


def edit(eid, old, new):
    assert T.count(old) == 1, (eid, T.count(old), old[:70])
    return {"id": eid, "finding": "Additions on Seyond's receiver and other 1,550 nm ToF makers", "old": old,
            "new": new, "why": WHY}


def appendix2_group_end(group):
    """The last list line of an Appendix 2 group (bold heading)."""
    a = T.index("# Appendix 2")
    m = re.search(r"(?m)^\*\*" + re.escape(group) + r"\*\*\s*$", T[a:])
    start = a + m.end()
    nxt = re.search(r"(?m)^\*\*[^*]+\*\*\s*$|^\*[^*]+\*\s*$|^#", T[start:])
    body = T[start:start + nxt.start()] if nxt else T[start:]
    return [l for l in body.split("\n") if l.startswith("- ")][-1]


edits = []

# §C3 company table: Seyond row (also K -> K1 in the range cell, as in the products cell) and the second-tier row
edits.append(edit(
    "S1-C3-seyond",
    "| 250 m (K), 300 m (K2), 450 m (K3); Robin E1X 200 m; Robin W 70 m (notes) | Main customer NIO; moving to 9xx for cost |",
    "| 250 m (K1), 300 m (K2), 450 m (K3); Robin E1X 200 m; Robin W 70 m (notes) | Main customer NIO; moving to 9xx for "
    "cost; listed on the Hong Kong main board on 10 Dec 2025 (02665.HK) through a merger with the SPAC TechStar "
    "Acquisition [T] |"))
edits.append(edit(
    "S2-C3-second-tier",
    "mostly 905; LeiShen and Benewake 1550",
    "mostly 905; LeiShen (LS series) and Benewake (Horn-X2 Pro) 1550 (§C4)"))

# §C4 "Where 1,550 nm survives": the Chinese 1,550 nm ToF units
edits.append(edit(
    "S3-C4-survives",
    "(AEye; MicroVision, which bought Luminar's lidar business, §C3a).",
    "(AEye; MicroVision, which bought Luminar's lidar business, §C3a). Two Chinese makers also sell 1,550 nm ToF units. "
    "Benewake's Horn-X2 Pro, built for roadside, railway, airport and shipping sensing rather than for vehicles, is a "
    "Class 1 unit specified at 300 m on a 10% target under 100 klx at 620 kpts/s, over 90° × 30° and at up to 35 W "
    "[P, datasheet BP-DS-62 A01, 2022]. LeiShen launched its LS series in August 2022 with an in-house fibre laser, "
    "claiming 250 m at 10% (500 m maximum) over 120° × 25° with 128 to 512 lines at 1.6–6.4 Mpts/s, for highway driver "
    "assistance at L3 and above; its release names no carmaker [P, company release]."))

# §C4b "Which lidars still use linear APDs": how Seyond builds its receiver, by its patents
L3850 = next(l for l in T.split("\n") if l.startswith("- **At 1,550 nm, all volume ToF lidars do.**"))
edits.append(edit(
    "S4-C4b-receiver",
    L3850,
    L3850 + "\n"
    "  - Innovusion, Seyond's name until 2024, patented a fibre-fed receiver that matches the Falcon's four-way fibre "
    "split (§C4d subsection 2(a)) [P, US 11,789,128 B2, priority 1 Mar 2021]. Four or more single-mode transmit fibres "
    "sit at a 100–400 µm pitch behind a collimating lens set into an opening of the collection lens, so the beams leave "
    "0.5–2.5° apart through the aperture that also collects their returns (claims 1, 14, 17, 18 and 21). At the image "
    "of each beam a multimode receive fibre, with a core of 50–1,000 µm, carries the return to its own detector "
    "assembly, where one lens collimates it through a small narrowband filter and a second lens focuses it onto an APD "
    "(claims 5, 10 and 11; Figs. 13–17). The fibre core thus sets each channel's field of view and its acceptance angle "
    "rejects stray light, and the four detectors can sit apart, clear of each other's optical and electrical "
    "crosstalk; the patent contrasts this with four APDs packed side by side in one focal plane (Fig. 12).\n"
    "  - A second Innovusion patent keeps the APDs in linear mode [P, US 11,789,132 B2, priority 9 Apr 2018]. The bias "
    "stays below a temperature-dependent avalanche threshold, set as the measured breakdown voltage times a fitted "
    "constant, using a temperature sensor, a look-up table and calibration sweeps at start-up or at intervals "
    "(claims 1–3, 7 and 8). Within each pulse period the bias rises, so that near returns see less gain than far ones "
    "(claims 12 and 13): the lidar counterpart of the sensitivity-time control by which a radar lowers its gain for "
    "near echoes.\n"
    "  - The patents leave the detector material open, but Seyond's 1,550 nm route uses InGaAs (§C4). Which of these "
    "designs the Falcon ships, and its APD supplier and readout chip, are not public; TechInsights sells a deep-dive "
    "teardown of the Falcon Kinetic (DDT-2208-806) whose public page names no parts."))

# Appendix 2: the sources
tech = appendix2_group_end("Technology routes and SPAD")
edits.append(edit("S5-A2-technology", tech, tech + "\n"
    "- Innovusion (Seyond), US 11,789,128 B2, fibre-based transmitter and receiver channels (priority 1 Mar 2021; "
    "claims 1–26, Figs. 12–17): https://patents.google.com/patent/US11789128B2/en\n"
    "- Innovusion (Seyond), US 11,789,132 B2, bias compensation for lidar APD receivers (priority 9 Apr 2018; "
    "claims 1–25): https://patents.google.com/patent/US11789132B2/en\n"
    "- TechInsights, deep-dive teardown DDT-2208-806 of the Innovusion Falcon Kinetic (product page; the report is "
    "paywalled): https://www.techinsights.com/products/ddt-2208-806\n"
    "- Benewake, Horn-X2 Pro datasheet BP-DS-62 A01 (24 Jun 2022; 1,550 nm, 300 m at 10% under 100 klx): "
    "https://en.benewake.com/uploadfiles/2024/05/20240509111033695.pdf\n"
    "- LSLiDAR (LeiShen), LS series 1,550 nm launch release (PR Newswire, 23 Aug 2022; syndicated copy): "
    "https://technode.global/prnasia/lslidars-image-grade-1550nm-lidar-ls-series-is-now-available-for-automotive-oems-taking-vehicle-safety-to-a-new-height/"))
market = appendix2_group_end("Lidar market and Western programmes")
edits.append(edit("S6-A2-market", market, market + "\n"
    "- Walkers, Seyond's listing on the Hong Kong main board through a de-SPAC merger with TechStar Acquisition "
    "(10 Dec 2025): https://www.walkersglobal.com/en/About-us/News/2025/12/Advising-Seyond-on-successful-HKEX-listing-through-de-SPAC-transaction-with-TechStar ; "
    "PEdaily (投资界), Seyond listed on 10 Dec 2025 as 02665.HK: https://news.pedaily.cn/20251210/119920.shtml"))

# Appendix 1 is edited in its own batch: one pair for it
appendix1 = [edit(
    "S7-A1-receive-front-ends",
    "Seyond Falcon and Aeva's sensors were not found,",
    "Seyond Falcon and Aeva's sensors were not found (for the Falcon, Innovusion's patents describe a fibre-fed APD "
    "receiver, §C4b, and TechInsights' paywalled teardown DDT-2208-806 of the Falcon Kinetic would name its parts),")]

for name, lst in (("edits.json", edits), ("appendix1_pair.json", appendix1)):
    out = HERE / name
    assert not out.exists() or "--force" in sys.argv, f"{name} exists; pass --force"
    out.write_text(json.dumps({"block": "seyond_1550_2026-10", "edits": lst, "skipped": []}, ensure_ascii=False,
                              indent=1), encoding="utf-8")
    print(name, len(lst), "edits")
