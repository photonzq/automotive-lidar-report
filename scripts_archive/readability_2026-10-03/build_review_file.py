"""Assemble the readability review of the scientific sections (2026-10-03) into one Markdown file in the report folder.

Reads the eleven block reports in ./reports and the edit labels of apply_readability_high.py (parsed as text, not run).
Usage: python build_review_file.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "automotive_perception_report_readability_review_2026-10-03.md"
BLOCKS = {
    "01_A3-A6_E2-E5": "§A3–§A6 (thermal and headlight physics) and §E2–§E5 (camera, radar and lidar physics; benchmarks; weather; safety arithmetic)",
    "02_C0_parts1-9": "§C0 subsections 1–9 (physics primer)",
    "03_C0_part10": "§C0 subsection 10 (link budget, detection statistics, range scaling)",
    "04_C4_C4b_C4c": "§C4, §C4b, §C4c (wavelength, SiPM vs SPAD, eye safety, sunlight, InGaAs, Ge)",
    "05_C4d_C8_C9": "§C4d (mechanical steering), §C8 (chip size and reticle), §C9 (interference)",
    "06_C5_C5a_C6": "§C5, §C5a, §C6 (SPAD-SoC receivers)",
    "07_C7_C7a_F6": "§C7, §C7a (FMCW maturity) and §F6",
    "08_C7b": "§C7b (can FMCW win?)",
    "09_C10_part1": "§C10 introduction to §C10.3 (optical phased arrays, photon arithmetic)",
    "10_C10_part2": "§C10.3a–§C10.7 (mode counting, FPAs, LC metasurface, camera-like resolution, verdict)",
    "11_E9-E12": "§E9–§E12 (perception power, heterogeneous sensors, learned stacks, camera-only trucking)",
}

labels = re.findall(r'^    \("([^"]+)",\s*$', (HERE / "apply_readability_high.py").read_text(encoding="utf-8"), re.M)

CROSS = """## Cross-section problems still open

The block reviewers worked separately, so the same problem often appears in several reports. These are the ones that need one decision for the whole report; none of them was changed in the 2026-10-03 batch except where noted.

**1. One symbol, several meanings (or one quantity, several symbols).**
- $R_{\\max}$: the unambiguous range in §C0 subsection 1 is now $R_{\\rm amb}$; §E11 Eq. (167) still uses $R_{\\max}$ for the half-width of a BEV grid.
- $N_s$: detected photons per range estimate, per pulse (Eq. (23)), accumulated histogram counts, and photons before detection (§C0 subsection 2); §C6 Eq. (80) now says per point.
- Energy per point: $E_{\\rm tx}$ (§C0 Eq. (42)), $E_{\\rm pt}$ (§C6, §F5), $E_{\\rm pulse}$ (§C10.2, §E9), $E_{\\rm point}$ (§E11 Eq. (169)), $E_s$ (§C10.3), $E_{\\rm opt}$ (§C7a, §C7b).
- $\\Omega$ is a solid angle (§C0 subsection 3, Eq. (24), §C6) and a scan rate (§C0 subsection 2, Eq. (86), Eq. (116)); $\\omega$ is the mechanical rate in §C7 but the optical rate in §C10.3a.
- $\\Delta f$: electrical bandwidth (Eqs. (26), (100)), scanner-induced spread (§C0 subsection 2, Eq. (86)) and beat bandwidth (§C7b).
- $\\eta$ includes the polarization factor in §C10.2 and §C10.3 but excludes it in §C0 subsection 10.1 and §C10.3a Eq. (144); this also leaves the §C10.3 and §C10.3a power figures (184 W) on different bases.
- Also: $\\eta_{\\rm wp}$ vs $\\eta_{\\rm WPE}$ and $P_{\\rm oh}$ vs $P_0$ (§C7b); $M$ (APD gain, $M^2$, margin, Marcum index); $S$ (sweep rate, speckle gain, lidar ratio); $\\theta$ (beamwidth, emission angle, cell width) in §C10; $a$ (aim angle, deceleration) in Parts A and E; $\\Delta t$ (round-trip delay, bin width); the ionization ratio $k$ is worded hole/electron in §C0 Eq. (25) and §C4, which is inverted for InP.

**2. The same relation under several equation numbers.** Stopping distance: Eq. (11) = (162) = (170) = (184), quoted as 255 m in some places and 257 m in others. Also Eq. (93) = (97); Eq. (85) = (186); Eqs. (33)–(35) = (101)–(103) = (146); Eq. (24) ≈ (67) ≈ (81)/(83); Eq. (65) = (82); Eq. (177) = (153); Eq. (178) = (150). The coherence-length condition is cited as "§C7, Eq. (185)", but Eq. (185) is in §F6.

**3. The FMCW dwell and channel model.** The dwell is defined three ways: $T_{\\rm up}+T_{\\rm down}$ (§C0, §C7), 10 µs without the round trip (§C7a Eq. (96)), and $E_{\\rm opt}/P_{\\rm ch}+2\\tau$ (§C7b Eq. (107)). As a result 10 Mpts/s needs 100 channels in §C7a and 127 in §C7b, and the receiver energy computed for the 0–300 m search is applied to the 200 m case. The parity chip is sized in channels in some places and receivers in others (≥150 channels; 115–190; ≥256 receivers; §C10.7's ≥256 channels), and §C7a lists five parity conditions where §C7b lists three.

**4. Interference (§C9, §C9a).** The ghost estimate switches from "up to nine counts per foreign shot" to one count per shot, from 0.33 ns to 1 ns bins and from 1.25 to 2.5 Mpt frames; the $10^{-3}$ fraction for facing scanners has no derivation; $n$ = 10–30 interferers is never tied to today's 3–16.

**5. Shared inputs that differ between Parts A, C and E.** Pedestrian 0.5 × 1.8 m vs 0.5 × 1.7 m; braking 0.7 $g$ vs 5–6 m/s²; low-beam reach 50–80 vs 50–100 m; dark-clothing reflectance 0.1, 0.05–0.1 or 5%; fog reach "0.6–1 V" in §E4 vs 0.52–0.69 V in the §C0 model, with fog classes defined three ways and $q_{\\rm K}$ in clear air 1.6 vs 1.3; solar background for the same case $1.6\\times10^9$ vs $2.2\\times10^9$ s⁻¹ (905 nm, 20 nm), $5.7\\times10^8$ vs $7.31\\times10^8$, $5.9\\times10^8$ vs $6.1\\times10^8$; the §C0 subsection 7 worked cases use 1,000 bins and $b=1$ where subsection 10.3 uses 2,000 bins and $b=2.87$.

**6. Product facts that disagree between sections.** Hesai ATX channels (64, 68 or 256); "2,160 channels per die"; IMX479 0.20 vs 0.16 MP; dead time 6 vs 15 ns for "the same array"; whether a Huawei 192-line teardown exists; Kim's interference fraction ($6\\times10^{-6}$ vs $2.6\\times10^{-5}$); Falcon K1 vs K2 ROI; HDL-64E point rate; BEVFusion-MIT at 68.5 vs 66.9 mAP and CenterPoint at 59.6 vs 56.3 mAP (different retrainings compared directly).

**7. Evidence tags.** Yole and ResearchInChina are tagged [P] or [T] instead of [MR]; Wikipedia [T] instead of [S]; several academic papers [P] instead of [I]; non-standard tags ("[T, snippet]", "[E from P]", "[P, search]"); and the untagged claims listed in each block report.

**8. Cross-reference slips.** Local "§2(a)" references in §C7a; "§A5.3"; "§E6" for IIHS night-AEB ratings that §E6 does not contain; "§C6" for the silicon-area multiplier (§C8.3); "§C10.3" for Pointcloud's DFB (§C10.4); "§C10.7" for the 8,192-element OPA (§C7, §C10.2b); "§C6(e)" for on-chip data reduction (§C5a).

**9. Structure.** §C0 subsection 9 (126 lines) and §C0 subsection 10.7 carry survey material that buries the primer's relations; §C7b items 2(h)–(i) depend on the channel model of subsection 3 but come before it; §C10.3a and §C10.3b are interleaved, with forward references; the §C5 Fastree3D history interrupts §C5's answer; the §C7b short answer runs to 33 lines; many tables lack an introducing sentence.

**10. High-severity items not applied because they need a source, a model decision or the author's judgement.** §A6 IIHS night-AEB ratings (no source); §E2 radar price "below \\$100" (unclear referent; tag [MR]); §C4b ATX channel mapping; §C5 Fastree3D share arithmetic; §C9a ghost-rate model and the §C9 $10^{-3}$ figure; §E10/§E11 MetaBEV and MEFormer like-for-like comparison; §C7b dwell definition and parity sizing; §C10.3a efficiency bookkeeping; §E11 grid symbol; §E9 energy symbol; §C10.3a fraction-column bases.
"""

parts = [
    "# Readability review of the scientific sections, 2026-10-03",
    "",
    "**Scope.** Eleven reviewers each read one block of the scientific sections of `automotive_perception_report_2026-09-27.md` "
    "(about 1 MB, ≈62% of the report) against the house style: derivations shown as equation, inputs, substitution and result; "
    "symbols and acronyms defined where used; full sentences and readable structure; arithmetic spot-checks; cross-section consistency; "
    "evidence tags and conventions. Each block report lists at most 40 findings, most severe first, with an exact quote and a proposed rewrite. "
    "They read the report at sha256 dfe616eb…/c39153b3…; line numbers in the block reports refer to that text.",
    "",
    "**Applied on 2026-10-03** (report sha256 after the batch: 9c6d35ce…). "
    f"{len(labels)} exact-substring edits from `scripts_archive/readability_2026-10-03/apply_readability_high.py`, "
    "covering the high-severity findings that were clear-cut and outside the lines being edited in parallel:",
    "",
]
parts += [f"- {lab}" for lab in labels]
parts += ["", "**Applied on 2026-10-04 and 2026-10-05**, as hash-guarded batches of exact-substring edits (the lists are in "
          "`scripts_archive/readability_2026-10-03/edits/`): Round 1, the block findings (905 edits) and a cross-section pass "
          "(80); Round 2, the model harmonizations the author decided on 2026-10-05 (311); Round 3, the moves and the merged "
          "duplicate equations, with every equation renumbered (175 tags; map in `edits/round3/round3_renumber_map.txt`); "
          "Round 4, source research for the items that needed a source (seven groups, in `sources/`); Round 5, the source "
          "items that Round 2 had skipped, and the author's decisions on the needs_decision items of "
          "`round1_skipped_items.md` and `edits/round2/*.json` (`edits/round5/R5b_decisions.json`; the lines in Part B, "
          "§D8 and Appendix 1 were applied in a separate batch, `R5b_for_peer.json`). The block reports below stay as the "
          "record of the findings; their line and equation numbers refer to the text of 2026-10-03. Still open is the "
          "905/940 nm split of §C9a (`sources/R8_C9a_inband_items.md`).", "",
          "Five blocks (§C0 parts 1–9 and 10, §C4–§C4c, both halves "
          "of §C10) also have follow-up cross-checks, run after both edit batches; they add findings such as the "
          "unsourced Falcon K 30 W, the misplaced §E12 pointer for the $1/R^4$ law (it is §E11.3, Eq. (169)), the 905 vs 940 nm "
          "ToF efficiency basis in §C10.3–§C10.3b, and Analog Photonics' funding stated three ways.", "",
          CROSS, "", "## Block reports", ""]
def demote(text):
    return re.sub(r"^(#{1,3}) ", lambda m: "#" * (len(m.group(1)) + 2) + " ", text.strip(), flags=re.M)


for key, title in BLOCKS.items():
    parts += [f"### {title}", "", demote((HERE / "reports" / f"{key}.md").read_text(encoding="utf-8")), ""]
    follow = HERE / "reports" / f"{key}_followup.md"
    if follow.exists():
        parts += [f"#### Follow-up cross-checks for this block (second pass, 2026-10-03; new findings only, "
                  "against the report after both edit batches)", "",
                  demote(follow.read_text(encoding="utf-8")), ""]
OUT.write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
print("wrote", OUT, f"({OUT.stat().st_size:,} bytes; {len(labels)} applied edits listed)")
