"""Round 3 (structural moves the author approved on 2026-10-04: "All moves, with equation renumbering").

Writes edits/round3/R3b_moves.json, one edit list for six moves and the cross-references that follow them:
  M1  §C0 subsection 9: the product and chip survey moves to a new §C1a (after §C1); a pointer and a source subset stay.
  M2  §C0 10.7: "How strong returns fail in ToF lidars" and "Tests and evidence" move to a new subsection of §C4b.
  M3  §C7b: items 2(h)-(i) become subsection 3a (after the channel tax), "Summary of the dwell" then follows item (g),
      the expanded P_elec of item (h) becomes a numbered display (review 08 #34), the short answer is cut to nine
      bullets (review 08 #15), and every "2(h)"/"2(i)" reference in the report follows.
  M4  §C5: the Fastree3D timeline and assessment move to §C3a subsection 2; three sentences stay in §C5.
  M5  §C5a: the AS-DT1 versus imaging-radar comparison moves to §E2; a pointer stays.
  M6  §C10.3a/b: the identity Eq. (147) is derived where §C10.3a first uses it (item 4); §C10.3b points back.
Moved text is cut from the live report by unique anchors and re-inserted verbatim, apart from the listed reference
fixes (each applied exactly as often as asserted). The new display equation carries the temporary tag 990, which
renumber_equations.py replaces. The report is only read.
Usage: python round3_build_moves.py
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
OUT = HERE / "edits" / "round3" / "R3b_moves.json"
T = REPORT.read_text(encoding="utf-8")
edits = []


def once(s):
    k = T.count(s)
    assert k == 1, (k, s[:90])
    return s


def span(start, end):
    """Text from the start of `start` up to (not including) `end`; both anchors unique, end after start."""
    a = T.index(once(start))
    b = T.index(once(end))
    assert b > a, (start[:60], end[:60])
    return T[a:b]


def fix(text, old, new, n=1):
    k = text.count(old)
    assert k == n, (k, n, old[:80])
    return text.replace(old, new)


def add(eid, finding, old, new, why):
    once(old)
    edits.append({"id": f"R3b_moves-{eid}", "finding": finding, "old": old, "new": new, "why": why})


# ---------------------------------------------------------------- M1: §C0 subsection 9 -> §C1a
F1 = "02_C0_parts1-9 report #20 (move the survey of §C0 subsection 9)"
add("M1-01", F1,
    "### 9. Amplitude-modulated (phase) ranging: ToF cameras, surveying rangers and what counts as lidar",
    "### 9. Amplitude-modulated (phase) ranging",
    "The product survey and 'what counts as lidar' move to §C1a; the subsection keeps the principle.")
add("M1-02", F1,
    "It also explains why the same physics gives millimetre precision at hundreds of metres in a surveying scanner "
    "but only about 10 m in a camera, and where the boundary of \"lidar\" is drawn.",
    "It also explains why the same physics gives millimetre precision at hundreds of metres in a surveying scanner "
    "but only about 10 m in a camera. The products themselves, the chips inside them and where the boundary of "
    "\"lidar\" is drawn are surveyed in §C1a.",
    "The opening names where the moved material now is.")
m1a = span("**One principle, three kinds of product.**", "**Same physics, different photon budgets** [E].")
add("M1-03", F1, m1a,
    "**Products.** Surveying rangefinders (electronic distance meters, EDMs), phase-based laser scanners and iToF "
    "cameras all use this principle. §C1a compares them, describes the two pixel architectures of ToF chips (iToF "
    "and dToF) and sets out where usage draws the line of \"lidar\".\n\n",
    "One-line pointer in place of the product table, its term note and derivation.")
SRC1 = T[T.index(once("Sources: https://www.ti.com/lit/ug/sbau219d/sbau219d.pdf ; https://thinklucid.com")):]
SRC1 = SRC1[:SRC1.index("\n")]
m1b_full = span("**iToF and dToF chips: two pixel architectures.**", SRC1) + SRC1
m1b = m1b_full[:-len(SRC1)]
src_kept = ("Sources: https://www.ti.com/lit/ug/sbau219d/sbau219d.pdf ; "
            "https://www.eenewseurope.com/en/time-of-flight-depth-image-sensor-has-0-5-megapixels/ ; "
            "https://www.imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R06.1.pdf ; "
            "https://geo3d.hr/sites/default/files/2018-06/Z+F%20IMAGER%205016_Datasheet.pdf ; "
            "https://www.zofre.de/en/laser-scanners/3d-laser-scanner ; "
            "https://www.slac.stanford.edu/econf/C8907312/papers/013.PDF")
for u in src_kept[len("Sources: "):].split(" ; "):
    assert u in SRC1, u
add("M1-04", F1, m1b_full, src_kept,
    "The chip, maker, 'line is blurring' and 'what counts as lidar' blocks and the companion pointer move to "
    "§C1a; the sources the remaining text cites (TI, ST VD55H1, Z+F, Mekometer) stay.")
moved1 = fix(m1a + m1b, "SPAD jitter and TDC step (subsection 1).", "SPAD jitter and TDC step (§C0 subsection 1).")
moved1 = fix(moved1, "the pulse repetition frequency of subsection 1", "the pulse repetition frequency of §C0 subsection 1")
c1a = ("## C1a. Phase ranging in products: ToF cameras, surveying rangers, ToF chips and what counts as lidar\n\n"
       "This section surveys the products and chips built on the amplitude-modulated (phase) ranging of §C0 "
       "subsection 9 (Eq. (28)): the three kinds of product that use it, the two pixel architectures of ToF chips, "
       "makers that build both, and where usage draws the line of \"lidar\". The conclusion of §C0 subsection 9 "
       "carries over: phase ranging (indirect ToF, iToF) suits the cabin, while exterior automotive sensing uses "
       "pulsed dToF or FMCW.\n\n" + moved1 + SRC1 + "\n\n")
add("M1-05", F1, "## C2. Market share by technology", c1a + "## C2. Market share by technology",
    "New §C1a after the taxonomy, holding the moved blocks verbatim (two 'subsection 1' references made explicit) "
    "and the full original source line.")
add("M1-06", F1 + "; pointer follows the move",
    "hold about two-thirds of ToF-sensor revenue [MR] (§C0 subsection 9).",
    "hold about two-thirds of ToF-sensor revenue [MR] (§B8; physics in §C0 subsection 9 and §C1a).",
    "The revenue figure is in §B8 (Mordor Intelligence); 'flash lidars in the physical sense' is in §C1a.")
add("M1-07", F1 + "; pointer follows the move",
    "Physically, ToF cameras are flash iToF lidars (§C0 subsection 9):",
    "Physically, ToF cameras are flash iToF lidars (§C1a):",
    "'What counts as lidar' moved to §C1a (Part B line outside the protected set of the parallel Part B pass; reported to that pass).")

# ---------------------------------------------------------------- M2: §C0 10.7 survey -> §C4b
F2 = "03_C0_part10 report #24 (move the strong-return survey of 10.7)"
m2 = span("**How strong returns fail in ToF lidars** (each item is documented in the sources listed):",
          "**What coherent detection changes.**")
add("M2-01", F2, m2,
    "**How strong returns fail in ToF lidars, and how it is tested.** Range walk, blooming, ghosting and blinding "
    "in ToF receivers, and the standards, open benchmarks and vendor fixes that address them, are surveyed in "
    "§C4b.\n\n",
    "Pointer in place of the survey; 10.7 keeps the span analysis, the coherent comparison and 'What this means'.")
moved2 = fix(m2, "satisfies $\\varepsilon\\,\\mathcal{D}<1$. That is $10\\log_{10}\\varepsilon<-74$ dB for the ToF "
             "design and a sign at 5 m,",
             "satisfies $\\varepsilon\\,\\mathcal{D}<1$, with $\\mathcal{D}$ the span of Eq. (52). That is "
             "$10\\log_{10}\\varepsilon<-74$ dB for the 25 mm SPAD ToF design of §C0 subsection 10.6 and a sign at "
             "5 m (§C0 subsection 10.7 table),")
moved2 = fix(moved2, "(each item is documented in the sources listed):",
             "(each item is documented in the sources listed at the end of this subsection):")
src2 = ("Sources: https://arxiv.org/abs/2605.24753 (Gump et al., CVPR 2026, glare in SPAD lidar) ; "
        "https://arxiv.org/html/2512.05932v1 (Dudzik et al. 2025, blooming simulation) ; "
        "https://ouster.com/insights/blog/new-lidar-firmware-v112 (Ouster firmware 1.12, retroreflector range bias and blooming) ; "
        "https://ouster.com/insights/blog/improved-3-1-firmware (Ouster firmware 3.1) ; "
        "https://patents.google.com/patent/US20250189670A1/en (Ouster, pile-up and matched filters) ; "
        "https://www.imeko.org/publications/tc4-2014/IMEKO-TC4-2014-292.pdf (Kurtti et al. 2014, walk and receiver linearity) ; "
        "https://www.semanticscholar.org/paper/A-Wide-Dynamic-Range-CMOS-Laser-Radar-Receiver-With-Kurtti-Nissinen/cfae82db5979654436ddef2520d36a17fec57dc3 (Kurtti et al. 2017, walk compensation) ; "
        "https://patents.google.com/patent/US7969558B2/en (Velodyne, one laser at a time) ; "
        "https://patents.google.com/patent/US11536845B2/en (Waymo, window ghosts) ; "
        "https://patents.google.com/patent/US12560716B2/en (SiPM blind zone after the window reflection) ; "
        "https://www.hesaitech.com/cn/news/1298 (GB/T 45500-2025 test items) ; "
        "https://user.guancha.cn/main/content?id=1435473 (GB/T 45500-2025, secondary summary) ; "
        "https://iss.rs/en/project/show/iso:proj:84347 (ISO/FDIS 13228) ; "
        "https://www.persival.de/post/quantifying-lidar-sensor-performance-through-din-sae-spec-91471-testing-methods (DIN SAE SPEC 91471) ; "
        "https://www.spiedigitallibrary.org/journals/optical-engineering/volume-62/issue-3/031211/Toward-open-benchmark-tests-for-automotive-lidars-year-1/10.1117/1.OE.62.3.031211.full (SPIE/SAE benchmark, year 1) ; "
        "https://www.spiedigitallibrary.org/journals/optical-engineering/volume-63/issue-8/085102/Toward-standardized-testing-of-automotive-lidars-year-two-results/10.1117/1.OE.63.8.085102.full (SPIE/SAE benchmark, year 2) ; "
        "https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=956735 (NIST 2024) ; "
        "https://www.robosense.ai/en/tech-show-55 (RoboSense M1) ; "
        "https://www.prnewswire.com/news-releases/hesai-showcases-next-gen-high-performance-lidars-at-iaa-mobility-2025-mass-production-expected-in-2026-302549128.html (Hesai ETX)")
src10 = T[T.index("Sources: https://doi.org/10.1364/AO.5.001588 (Siegman 1966)"):]
src10 = src10[:src10.index("\n")]
for u in src2[len("Sources: "):].split(" ; "):
    assert u.split(" (")[0] in src10, u
c4b = ("### Strong returns in ToF receivers: failure modes and tests\n\n"
       "§C0 subsection 10.7 sizes the span of return strengths a receiver must handle: for a 25 mm SPAD ToF design "
       "sized to reach 200 m on a 10% target, 56–82 dB of optical span from its weakest detectable return to a white "
       "target at 0.3–1 m or a retroreflective sign at 2–30 m (Eq. (52)). This subsection collects how ToF "
       "receivers fail when a return exceeds what they can span, and how standards, benchmarks and vendors test for "
       "it.\n\n" + moved2 + src2 + "\n\n")
add("M2-02", F2, "\n### Other dimensions\n", "\n" + c4b + "### Other dimensions\n",
    "New §C4b subsection after the dynamic-range trade, holding the survey verbatim (criterion tied to Eq. (52)) "
    "with the sources it cites, copied from the §C0 subsection 10 source line, which keeps them.")

# ---------------------------------------------------------------- M3: §C7b reorder, P_elec display, short answer
F3 = "08_C7b report #14 (items (h)-(i) become subsection 3a)"
m3 = span("**(h) What limits a 10 Mpts/s sensor at 300 m: the light itself.**", "**Summary of the dwell.**")
add("M3-01", F3, m3, "", "Items (h) and (i) move to subsection 3a; 'Summary of the dwell' now follows item (g).")
moved3 = fix(m3, "**(h) What limits a 10 Mpts/s sensor at 300 m: the light itself.**",
             "**(a) What limits a 10 Mpts/s sensor at 300 m: the light itself.**")
moved3 = fix(moved3, "**(i) What the 1,550 nm eye-safety allowance buys:", "**(b) What the 1,550 nm eye-safety allowance buys:")
moved3 = fix(moved3, "(item (g))", "(subsection 2(g))", n=moved3.count("(item (g))"))
moved3 = fix(moved3, "(item (c))", "(subsection 2(c))", n=moved3.count("(item (c))"))
moved3 = fix(moved3, "unless the transmitter is gated (item (i)).", "unless the transmitter is gated (item (b)).")
moved3 = fix(moved3, "Item (h) shows that this pays only", "Item (a) shows that this pays only")
assert "item (g)" not in moved3 and "(h)" not in moved3 and "(i)" not in moved3.replace("(i) ", "")
# review 08 #34: the expanded P_elec as a numbered two-line display
p_old = ("Substituting $N_{\\rm ch}$ and $N_{\\rm samp}$ splits $P_{\\rm elec}$ into three parts. The part independent of "
         "$P_{\\rm ch}$ is $\\dot N[E'/\\eta_{\\rm wp}+5N_L(R/\\Delta R)e_s+2\\tau N_LP_{\\rm an}]+P_{\\rm oh}$. The dead-time "
         "light, $2\\tau\\dot NP_{\\rm ch}/\\eta_{\\rm wp}$, grows with $P_{\\rm ch}$. The analog power and the Doppler share "
         "of the samples, $\\dot NE'N_L(P_{\\rm an}+2.5f_De_s)/P_{\\rm ch}$, fall as $1/P_{\\rm ch}$.")
p_new = ("Substituting $N_{\\rm ch}$ and $N_{\\rm samp}$ splits $P_{\\rm elec}$ into three parts:\n\n"
         "$$\\begin{aligned}P_{\\rm elec}&=\\underbrace{\\dot N\\left[\\dfrac{E'}{\\eta_{\\rm wp}}+5N_L\\,\\dfrac{R}{\\Delta R}\\,e_s"
         "+2\\tau N_LP_{\\rm an}\\right]+P_{\\rm oh}}_{\\rm independent\\ of\\ P_{\\rm ch}}\\\\ &\\quad+\\underbrace{\\dfrac{2\\tau\\,"
         "\\dot NP_{\\rm ch}}{\\eta_{\\rm wp}}}_{\\rm grows\\ with\\ P_{\\rm ch}}+\\underbrace{\\dfrac{\\dot NE'N_L\\,(P_{\\rm an}"
         "+2.5f_De_s)}{P_{\\rm ch}}}_{\\rm falls\\ as\\ 1/P_{\\rm ch}} .\\end{aligned} \\tag{990}$$\n\n"
         "  The first part is fixed by the point rate and the photons per point. The dead-time light grows with "
         "$P_{\\rm ch}$, while the analog power and the Doppler share of the samples fall as $1/P_{\\rm ch}$.")
moved3 = fix(moved3, p_old, p_new)
c3a = ("### 3a. Sensor power at 10 Mpts/s and 300 m, and the 1,550 nm eye-safety ceiling\n\n"
       "This subsection adds up a whole FMCW sensor's electrical power from the dwell (subsection 2) and the channel "
       "count (Eq. (121)), and asks whether the 1,550 nm eye-safety allowance relaxes it.\n\n" + moved3)
add("M3-02", F3, "### 4. What beam steering can and cannot do for FMCW",
    c3a + "### 4. What beam steering can and cannot do for FMCW",
    "Subsection 3a after the channel tax (order 1, 2 + summary, 3, 3a, 4-7); items relabelled (a)-(b) and their "
    "internal references made explicit.")
add("M3-03", F3,
    "Items (h) and (i) then add up the electrical power of a whole sensor at 10 Mpts/s and 300 m and ask what the "
    "1,550 nm eye-safety allowance buys.",
    "Subsection 3a then adds up the electrical power of a whole sensor at 10 Mpts/s and 300 m and asks what the "
    "1,550 nm eye-safety allowance buys.",
    "The subsection 2 preview follows the move.")
REFS3 = [
    ("§C7b subsection 2(i) puts numbers on it for the two designs of §C7a.",
     "§C7b subsection 3a(b) puts numbers on it for the two designs of §C7a."),
    ("would emit only the 7.6 W of useful light and stay within it (§C7a(b); §C7b subsection 2(i)).",
     "would emit only the 7.6 W of useful light and stay within it (§C7a(b); §C7b subsection 3a(b))."),
    ("would exceed the allowance for this field (§C7b subsection 2(i)).",
     "would exceed the allowance for this field (§C7b subsection 3a(b))."),
    ("Eye safety allows ≈9.1 W of scanned light over a 120° × 25° field at 1,550 nm (§C7b subsection 2(i)).",
     "Eye safety allows ≈9.1 W of scanned light over a 120° × 25° field at 1,550 nm (§C7b subsection 3a(b))."),
    ("$2\\tau/T_{\\rm dwell}=2.67/12.67=21\\%$ of what the ungated laser emits (§C7b subsection 2(i)).",
     "$2\\tau/T_{\\rm dwell}=2.67/12.67=21\\%$ of what the ungated laser emits (§C7b subsection 3a(b))."),
    ("takes ≈9 W more (§C7b subsection 2(h)).", "takes ≈9 W more (§C7b subsection 3a(a))."),
    ("the optimum is already ≈30–40 mW per channel (§C7b subsection 2(h)).",
     "the optimum is already ≈30–40 mW per channel (§C7b subsection 3a(a))."),
    ("Eq. (122) is Eq. (118) of subsection 2(h) with", "Eq. (122) is Eq. (118) of subsection 3a(a) with"),
    ("Subsection 2(h) evaluated Eq. (118) at 10 Mpts/s and 300 m,", "Subsection 3a(a) evaluated Eq. (118) at 10 Mpts/s and 300 m,"),
    ("(subsection 2(i), item 2)", "(subsection 3a(b), item 2)"),
    ("FMCW transmit budgets of §C7b 2(i)", "FMCW transmit budgets of §C7b 3a(b)"),
    ("§C7b subsections 1(f) and 2(i))", "§C7b subsections 1(f) and 3a(b))"),
]
for i, (o, n) in enumerate(REFS3, 1):
    add(f"M3-R{i:02d}", F3 + "; references follow the move", o, n, "Reference to items (h)/(i) of subsection 2.")
F3b = "08_C7b report #15 (cut the short answer to about eight bullets)"
sa_old = span("**Short answer** [E unless tagged].", "### 1. How many points one joule of light buys, by architecture")
sa_new = (
    "**Short answer** [E unless tagged].\n"
    "- **Per joule of useful light, FMCW buys ≈4.2× fewer sampled points than 940 nm SPAD ToF, and the reason is "
    "spatial, not temporal** (subsection 1). A coherent receiver collects one spatial mode and one polarization of "
    "the echo, ≤65 mm² at 200 m for any collimated beam, and a single speckle that fades, whereas a direct-detection "
    "pixel sums the ≈491 mm² of a 25 mm lens and hundreds of speckles. An ungated CW channel, which also emits "
    "during the round trips, widens the gap to ≈5.3× per joule emitted, and the coherent efficiencies measured so "
    "far (0.057–0.168) widen it to 6–19× (subsection 1(c)).\n"
    "- **Per covered cell the gap is ≈200×** (subsection 1(d)). One FMCW sample, ≈0.30 µJ against ≈72 nJ per ToF "
    "point at 200 m on a 10% target, covers only ≈2% of a 0.05° × 0.05° cell, so covering the cell takes ≈15 µJ "
    "(48 samples).\n"
    "- **Pulsing matters for direct detection, not for coherent detection** (subsection 1(a) and (e)). ToF must "
    "pulse so that sunlight competes with the signal only inside a 1 ns bin; spread evenly in time, the same echo "
    "would need ≈13× more energy. In FMCW the local oscillator (LO) already rejects sunlight, so continuous-wave "
    "(CW) light costs no photons, apart from the 12–35% emitted during the last $\\tau$ of each ramp (21% in the "
    "§C7a central case), whose echo falls in a discarded window.\n"
    "- **What CW light costs is hardware: the channel tax** (subsections 2–3). A CW channel carries only tens of "
    "milliwatts, so it must dwell $E_{\\rm pt}/P_{\\rm ch}+2\\tau$ on each point, and 15 Mpts/s needs ≈190 "
    "channels, each a transmit beam with four complete coherent receivers drawing ≈385 mW against ≈20 mW for a "
    "SPAD-SoC macro-pixel.\n"
    "- **Neither a better beam steerer nor a faster laser removes the tax** (subsections 2(g) and 4). Mirrors "
    "already move each beam as fast as one channel can use, faster scanning adds scanner-induced Doppler and "
    "receive walk-off (§C7), and at ≤30 mW per channel photons, not the laser's chirp rate or tuning range, set "
    "each ramp's useful window (7.5–14 µs at 300 m).\n"
    "- **At the sensor level most of the power is light** (subsection 3a(a)). A 10 Mpts/s sensor at 300 m draws "
    "≈68 W, ≈30 W of it to make the useful light, which no split among channels reduces; a 100 kHz laser raises "
    "the total to ≈160 W.\n"
    "- **The 1,550 nm eye-safety allowance buys range, not watts per point** (subsection 3a(b)). It allows ≈9.1 W "
    "of scanned light over a 120° × 25° field, enough for ≈470–600 m of eye-safe reach at 10 Mpts/s, but the "
    "ungated §C7a central transmitter exceeds it at 25 Mpts/s (9.6 W).\n"
    "- **Parity with ToF, ≥15 Mpts/s in ≤15 W at 200 m and 10%, needs three things at once** (subsection 5): a "
    "coherent receiver chip at ≈2–3 mW per receiver for 115–190 channels of four receivers, CW lasers and "
    "amplifiers at ≥30% wall-plug efficiency at 105 °C, and ≈0.15 µJ of light per point. With all three an "
    "ungated sensor draws ≈14 W at 15 Mpts/s, still 1.8× the electrical energy per point of the 2026 SPAD ToF "
    "reference (9.2 W); today's central case draws ≈76.5 W.\n"
    "- **FMCW can win a market, but not the point-rate race.** Its market is buyers who pay for velocity on every "
    "point and for immunity to sunlight and other lidars at long range: trucks and highway L3. (L3 is SAE "
    "driving-automation Level 3: the car drives itself in a defined domain, and the driver takes over on request.) "
    "Through 2028 that market is thousands of units a year, against millions for ToF (§B4).\n\n")
add("M3-04", F3b, sa_old, sa_new,
    "Nine bullets, each with its key number and pointer; the floor, sweep and ADC numbers stay in 2(g), the "
    "eta_coh formula in 2(e) and 3a(a), and the 185 + 200 mW per channel in subsection 3.")
# the numbers the cut short answer no longer carries are all in the body
for s in ("7.5–14 µs", "1.14–1.27 GHz", "=35$ mW with 1 GS/s converters", "Per fully covered cell the gap is ≈200×",
          "≈385 mW of electrical power", "≈20 mW per ToF channel", "≈160 W"):
    assert s in T, s

# ---------------------------------------------------------------- M4: Fastree3D history -> §C3a
F4 = "06_C5_C5a_C6 report #29 (move the Fastree3D history to §C3a)"
m4 = span("**Fastree3D: the European SPAD lineage now inside Hesai.**", "**Foundry check.**")
add("M4-01", F4, m4,
    "**Fastree3D: the European SPAD lineage now inside Hesai.** Part of Hesai's SPAD IP (intellectual property, "
    "here mainly patents) comes from Fastree3D, a spin-off of EPFL (the Swiss federal technology institute in "
    "Lausanne) and TU Delft (Delft University of Technology) that Hesai bought on 15 December 2023 for \\$7.67 M "
    "[P]; Hesai says it had also researched SPADs itself since 2016. Hesai booked the acquired patent rights at "
    "RMB 59.35 M (≈\\$8.4 M) [P]. No public evidence yet shows Fastree3D circuits in a shipping chip, as distinct "
    "from its patents in Hesai's 4th-generation platform; §C3a, subsection 2, traces the company's history and asks "
    "whether the deal was a success.\n\n",
    "Three facts stay in §C5 (price, patent value, no circuits in a shipping chip), with a pointer.")
moved4 = fix(m4, "**Fastree3D: the European SPAD lineage now inside Hesai.** Part of Hesai's SPAD IP (intellectual "
             "property, here mainly patents) comes from this spin-off of EPFL (the Swiss federal technology institute "
             "in Lausanne) and TU Delft (Delft University of Technology), bought in late 2023; Hesai says it had also "
             "researched SPADs itself since 2016.",
             "**Fastree3D: a European SPAD exit to a Chinese buyer.** Fastree3D, a spin-off of EPFL (the Swiss "
             "federal technology institute in Lausanne) and TU Delft (Delft University of Technology), is the SPAD "
             "company that Hesai bought, patents included, in late 2023 (§C5); Hesai says it had also researched "
             "SPADs itself since 2016.")
moved4 = fix(moved4, "It mirrors the wider pattern described in §B3, §C3a and §G2,",
             "It mirrors the wider pattern described above and in §B3 and §G2,")
add("M4-02", F4, "### 3. The technology bets: what each company staked, and what the pattern shows",
    moved4 + "### 3. The technology bets: what each company staked, and what the pattern shows",
    "The timeline, its term list and the assessment, after 'Where the IP went' in §C3a subsection 2.")

# ---------------------------------------------------------------- M5: AS-DT1 against imaging radar -> §E2
F5 = "06_C5_C5a_C6 report #29 (move the radar comparison to §E2)"
m5 = span("**Against imaging radar** (§E2).", "**What a real lidar adds** (range-weighted point rate, §C3b).")
add("M5-01", F5, m5,
    "**Against imaging radar.** A sparse 576-point lidar such as the AS-DT1 invites comparison with an imaging "
    "radar, which also reports a few hundred to a few thousand angular cells; §E2 compares the two and finds that "
    "they do different jobs.\n\n",
    "Pointer; the 'Points cost range' result stays in §C5a.")
moved5 = fix(m5, "**Against imaging radar** (§E2). A sparse 576-point lidar invites comparison",
             "**A sparse SPAD lidar against an imaging radar** (§C5a). Sony's AS-DT1, a 576-point SPAD lidar for "
             "drones and autonomous mobile robots (AMRs), invites comparison")
moved5 = fix(moved5, "a precise multipoint ranger for drones and AMRs,", "a precise multipoint ranger for drones and AMRs,")
add("M5-02", F5, "## E2a. Sideline: the automotive mmWave radar market, deployments and prices",
    moved5 + "## E2a. Sideline: the automotive mmWave radar market, deployments and prices",
    "The comparison and its six bullets at the end of §E2, after the radar physics.")

# ---------------------------------------------------------------- M6: §C10.3a/b, the identity where it is first used
F6 = "10_C10_part2 report #17 (untangle §C10.3a/§C10.3b)"
id_old = ("The relation follows from Eq. (142) with the hard area $A_{\\rm rx}$ replaced by the mode-equivalent area "
          "$A_{\\rm mode}$, combined with the antenna theorem in the form the Gaussian model gives it, "
          "$A_{\\rm mode}\\,\\Omega_{\\rm footprint}=\\tfrac{t^2}{2}\\lambda^2$ (Eq. (147) of §C10.3b, since one sample's "
          "footprint fraction is $\\Omega_{\\rm footprint}/\\Omega_{\\rm cell}$); an ideal single mode without truncation "
          "or polarization loss would have $\\lambda^2$.")
id_new = ("**The mode-area–footprint identity.** Multiplying the mode-equivalent area of Eq. (33) (§C0 subsection "
          "10.2), $A_{\\rm mode}=t^2\\lambda^2R^2/(2\\pi w^2)$, by one sample's nominal footprint fraction "
          "$f_{\\rm fp}=\\pi w^2/(R\\theta_{\\rm cell})^2$, where $\\theta_{\\rm cell}$ is the mesh pitch (rad), cancels "
          "both the beam radius $w$ and the range $R$:\n\n"
          "$$A_{\\rm mode}\\,f_{\\rm fp}=\\frac{t^2}{2}\\left(\\frac{\\lambda}{\\theta_{\\rm cell}}\\right)^2 \\tag{147}$$\n\n"
          "with $t^2=0.84$ the round-trip truncation factor, ½ the single-polarization factor and $\\lambda$ the "
          "wavelength. This is the antenna theorem in the form the Gaussian model gives it, "
          "$A_{\\rm mode}\\,\\Omega_{\\rm footprint}=\\tfrac{t^2}{2}\\lambda^2$, since one sample's footprint fraction is "
          "$\\Omega_{\\rm footprint}/\\Omega_{\\rm cell}$; an ideal single mode without truncation or polarization loss "
          "would have $\\lambda^2$. A design can therefore buy collecting area (photons per sample) only by giving up "
          "footprint fraction (coverage), and vice versa; only the mesh pitch and the wavelength move the product "
          "(§C10.3b, Result 2, evaluates it).\n\n"
          "Eq. (144) follows from Eq. (142) with the hard area $A_{\\rm rx}$ replaced by the mode-equivalent area "
          "$A_{\\rm mode}$ and combined with Eq. (147).")
add("M6-01", F6, id_old, id_new,
    "The identity is derived where §C10.3a first uses it, from §C0 Eq. (33), so no equation is cited before it appears.")
b_old = span("- **Photons and coverage trade one for one.** Let $f_{\\rm fp}$ be the nominal 1/e² footprint fraction",
             "  | Mesh pitch | $A_{\\rm mode}\\,f_{\\rm fp}$ |")
assert "\\tag{147}" in b_old and b_old.endswith("moves the product:\n\n"), b_old[-60:]
add("M6-02", F6, b_old,
    "- **Photons and coverage trade one for one.** By the identity of Eq. (147) (§C10.3a, item 4), "
    "$A_{\\rm mode}f_{\\rm fp}=\\tfrac{t^2}{2}(\\lambda/\\theta_{\\rm cell})^2$, a design can buy collecting area only "
    "by giving up footprint fraction; only the mesh pitch (and the wavelength) moves the product:\n\n",
    "§C10.3b now evaluates the identity rather than deriving it.")
add("M6-03", F6,
    " The 30-photoelectron column is the §C7a four-look design value: 30 per look, a 1.36× margin over the ideal 22 "
    "per look (88.5 in total). By Eq. (145) below, four modes at 30 each have the coverage bound of one mode at 30.",
    " The 30-photoelectron column is the §C7a four-look design value: 30 per look, a 1.36× margin over the ideal 22 "
    "per look (88.5 in total).",
    "The Eq. (145) statement moves after Eq. (145).")
add("M6-04", F6,
    "where $n_\\Sigma=N_{\\rm mode}\\,n_{\\rm mode}$ is the photoelectron count summed over the $N_{\\rm mode}$ selected "
    "modes and $K$ is the single-mode budget constant of Eq. (144).",
    "where $n_\\Sigma=N_{\\rm mode}\\,n_{\\rm mode}$ is the photoelectron count summed over the $N_{\\rm mode}$ selected "
    "modes and $K$ is the single-mode budget constant of Eq. (144). Four modes at 30 photoelectrons each, as in the "
    "§C7a four-look design, therefore have the coverage bound of one mode at 30 (the 30-photoelectron column of the "
    "table above).",
    "Placed after the equation it uses.")
REFS6 = [
    ("the Gaussian model of §C10.3b gives the second relation (its Eq. (147) with a footprint fraction of one)",
     "the Gaussian model gives the second relation (Eq. (147) of §C10.3a, item 4, with a footprint fraction of one)"),
    ("[E: the bound is the identity Eq. (147), derived in §C10.3b,", "[E: the bound is the identity Eq. (147), derived in item 4,"),
    ("mode-area–footprint identity as an OPA,** Eq. (147) of §C10.3b:", "mode-area–footprint identity as an OPA,** Eq. (147) of §C10.3a:"),
    ("as $A_{\\rm mode}f_{\\rm fp}=$ const requires (Eq. (147), §C10.3b).", "as $A_{\\rm mode}f_{\\rm fp}=$ const requires (Eq. (147), §C10.3a)."),
]
for i, (o, n) in enumerate(REFS6, 1):
    add(f"M6-R{i:02d}", F6 + "; references follow the move", o, n, "Eq. (147) is now derived in §C10.3a, item 4.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"block": "R3b_moves", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(len(edits), "edits written to", OUT.name)
