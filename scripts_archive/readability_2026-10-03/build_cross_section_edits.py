"""Build edits/12_cross_section.json: the cross-section items that the Round 1 block agents listed as 'skipped:
cross_section', plus the leftover old symbols that post_merge_symbol_check.py found after the Round 1 merge.

Every "old" is an exact substring of the live report and must occur exactly once; span edits rewrite one passage
(found by its unique start and end strings) and replace a symbol only inside it. The decisions taken here:
- truck stopping distance 166-257 m everywhere: Eq. (170) with v = 29.2 m/s, t_r = 1.5 s gives 43.8 + 121.8 = 165.6 m
  for 3.5 m/s^2 and 257.0 m for 2.0 m/s^2, so 166 m pairs with the 257 m already used (§F6 uses 166 after Round 1);
- E_opt in §C0 subsection 10.6 (the best design's energy per point) becomes E_best, since E_opt elsewhere was the
  old name of the optical energy per point;
- display equations split with aligned use \\dfrac (and \\displaystyle for the integral), because MathML table cells
  are set in text style and the fractions otherwise print small.
Usage: python build_cross_section_edits.py   (then validate_edits.py edits/12_cross_section.json)
"""
import json
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
OUT = Path(__file__).resolve().parent / "edits" / "12_cross_section.json"
text = REPORT.read_text(encoding="utf-8")
edits = []


def add(eid, old, new, why):
    assert text.count(old) == 1, (eid, text.count(old), old[:80])
    edits.append({"id": eid, "finding": "cross_section", "old": old, "new": new, "why": why})


def span(eid, start, end, pairs, why, extra=()):
    """Rewrite the passage from `start` to the end of `end`, replacing each (a, b) in pairs everywhere inside it."""
    a = text.find(start)
    assert a >= 0 and text.count(start) == 1, (eid, "start", text.count(start))
    b = text.find(end, a)
    assert b > a, (eid, "end")
    b += len(end)
    old = text[a:b]
    new = old
    for x, y in pairs:
        assert x in new, (eid, x)
        new = new.replace(x, y)
    for x, y in extra:
        assert new.count(x) == 1, (eid, "extra", x[:60], new.count(x))
        new = new.replace(x, y)
    for x, _ in pairs:
        assert x not in new, (eid, "left over", x)
    add(eid, old, new, why)


# ---- truck stopping distance 166-257 m (§E6, §E12, §F7) and Eq. (162) with a_b ----
add("X01", "brakes at constant deceleration $a$ (m/s²) stops within",
    "brakes at constant braking deceleration $a_{\\rm b}$ (m/s²) stops within",
    "Braking deceleration is a_b report-wide; Eq. (170) points to Eq. (162).")
add("X02", "$$d=v\\,t_{\\rm r}+\\frac{v^2}{2a} \\tag{162}$$", "$$d=v\\,t_{\\rm r}+\\frac{v^2}{2a_{\\rm b}} \\tag{162}$$",
    "Same symbol as Eqs. (11), (159), (170) and (184).")
add("X03", "Stopping takes about 165–255 m, so perception", "Stopping takes about 166–257 m, so perception",
    "Eq. (162) with 29.2 m/s, 1.5 s and 3.5 or 2.0 m/s² gives 165.6 and 257.0 m.")
add("X04", "- *Truck (165–255 m).*", "- *Truck (166–257 m).*", "As X03.")
add("X05", "$29.2\\times1.5+29.2^2/(2\\times3.5)\\approx165$ m", "$29.2\\times1.5+29.2^2/(2\\times3.5)\\approx166$ m",
    "43.8 + 121.8 = 165.6 m.")
add("X06", "needs 165–257 m to stop", "needs 166–257 m to stop", "As X03.")
add("X07", "against the truck's 165–257 m ($165/83\\approx2.0$, $257/83\\approx3.1$)",
    "against the truck's 166–257 m ($166/83\\approx2.0$, $257/83\\approx3.1$)", "As X03.")
add("X08", "is 165–257 m, from Eq. (170)", "is 166–257 m, from Eq. (170)", "As X03.")
add("X09", "(best case, 165 m)", "(best case, 166 m)", "As X03.")
add("X10", "stopping distance 165–257 m, stalled", "stopping distance 166–257 m, stalled", "As X03.")
add("X11", "$(300-165)/29.2\\approx4.6$", "$(300-166)/29.2\\approx4.6$", "134/29.2 = 4.59.")
add("X12", "| 4.9 to 8.1 s |", "| 4.9 to 8.0 s |", "(400 − 166)/29.2 = 8.01 s.")
add("X13", "$(250-165)/29.2\\approx2.9$", "$(250-166)/29.2\\approx2.9$", "84/29.2 = 2.88.")
add("X14", "$(150-165)/29.2\\approx-0.5$", "$(150-166)/29.2\\approx-0.5$", "−16/29.2 = −0.55.")
add("X15", "(165–255 m stopping distances,", "(166–257 m stopping distances,", "As X03.")

# ---- §E12 subsection pointer, §E2 Eq. (153) angle symbols ----
add("X16", "(§E12, subsection 3, item 5)", "(§E12.3, item 5)", "§E12's subsections are now numbered E12.1–E12.4.")
add("X17", "appears at an angle $\\theta$ below the horizon, the *depression angle*, with",
    "appears at an angle $\\alpha$ below the horizon, the *depression angle*, with",
    "delta-theta is the lidar point spacing in §E2 (scheme); the depression angle is alpha, as in §E12.")
add("X18", "$$Z=\\frac{h}{\\tan\\theta},\\qquad \\frac{\\partial Z}{\\partial\\theta}\\approx-\\frac{Z^2}{h},\\qquad \\lvert\\delta Z\\rvert\\approx\\frac{Z^2}{h}\\,\\delta\\theta \\tag{153}$$",
    "$$Z=\\frac{h}{\\tan\\alpha},\\qquad \\frac{\\partial Z}{\\partial\\alpha}\\approx-\\frac{Z^2}{h},\\qquad \\lvert\\delta Z\\rvert\\approx\\frac{Z^2}{h}\\,\\delta\\alpha \\tag{153}$$",
    "As X17.")
add("X19", "the small-angle form $Z\\approx h/\\theta$, and $\\delta\\theta$ (rad) is an error in the assumed camera pitch",
    "the small-angle form $Z\\approx h/\\alpha$, and $\\delta\\alpha$ (rad) is an error in the assumed camera pitch", "As X17.")
add("X20", "$Z^2\\delta\\theta/h=200^2\\times1.745\\times10^{-3}/1.5\\approx47$ m",
    "$Z^2\\delta\\alpha/h=200^2\\times1.745\\times10^{-3}/1.5\\approx47$ m", "As X17.")
add("X21", "with $R$ for $Z$, $h_{\\rm cam}$ for $h$ and $\\delta\\alpha$ for $\\delta\\theta$.",
    "with $R$ for $Z$ and $h_{\\rm cam}$ for $h$.", "§E2 now writes delta-alpha too.")

# ---- tags and pointers (Part A/B, §C3b, §C4b, §C5, §C0) ----
add("X22", "**\\$3.56–3.8 B** [T].", "**\\$3.56–3.8 B** [MR, Yole via optics.org].",
    "Yole estimates are [MR] in the legend; Appendix 2 lists optics.org as the relay.")
add("X23", "**Global (Yole)** [T]", "**Global (Yole)** [MR, via optics.org and Hesai]", "As X22.")
add("X24", "so the return falls as $1/R^4$ (§E12). For such targets",
    "so the return falls as $1/R^4$ (§E11.3, Eq. (169)). For such targets",
    "§E11.3 derives the 1/R^4 law; §E12 does not state it.")
add("X25", "Ranging precision is cm-class in both |",
    "Ranging precision is cm-class in both, against the ideal ≈0.3 cm of $\\sigma_R\\approx(c/2)\\sigma_t/\\sqrt{N_s}$ for 100 ps and 20 photons (§C0 subsection 1) |",
    "Ties the measured class to the §C0 relation.")
add("X26", "narrow ROIs and figures mixed from different variants.",
    "narrow ROIs and figures mixed from different variants. A second echo is reported separately only if it lies at least about $c\\,\\tau_p/2$ behind the first, with $\\tau_p$ the pulse length: 0.75 m for a 5 ns pulse (§C0 subsection 1).",
    "Applies the two-target resolution of §C0 subsection 1 to dual returns.")
add("X27", "| 5 ns → 0.75 m; 1 ns → 15 cm | — |", "| 5 ns → 0.75 m; 1 ns → 15 cm | §C3b |",
    "§C3b now applies the relation (X26).")
add("X28", "and \"297 ps bins\" is the width of the timing histogram's bins.",
    "and \"297 ps bins\" is the width of the timing histogram's bins, $c\\,\\Delta t_{\\rm bin}/2=4.5$ cm of range per bin (§C0 subsection 1).",
    "Gives the range per bin with the §C0 relation.")
add("X29", "$N_{\\rm points}R^2$ is roughly constant (§C5a).",
    "$N_{\\rm points}R^2$ is roughly constant (§C0 subsection 1; §C5a applies it to the AS-DT1).",
    "The scaling is derived in §C0 subsection 1; §C5a applies it.")
add("X30", "as points are added (§C5a).", "as points are added (§C0 subsection 1; §C5a applies it to the AS-DT1).", "As X29.")
add("X31", "120° × 25.4°, 0.1° × 0.2°, 13.5 W [P]", "120° × 25.4°, 0.1° × ≈0.2° (25.4°/128 = 0.198°), 13.5 W [P]",
    "128 rows of 0.2° would span 25.6°, not 25.4°.")
add("X32", "range noise ≈5 cm.",
    "range noise ≈5 cm, an assumed value [E] above the ideal ≈0.3 cm of §C0 subsection 1 and the 2–4 cm measured outdoors for the AS-DT1 (§C5a).",
    "States the basis of the assumed lidar range noise.")
add("X33", "and $f_{\\rm frame}$ is the frame rate (complete fields per second, in Hz or fps).",
    "and $f_{\\rm frame}$ is the frame rate (complete fields per second, in Hz or fps). Eq. (61) is the points-per-frame relation of §C0 subsection 3, times the frame rate.",
    "Links Eq. (61) to its §C0 source.")
add("X34", "places points $R\\,\\delta\\theta$ apart at range $R$,",
    "places points $R\\,\\delta\\theta$ apart at range $R$ (the point-spacing relation of §C0 subsection 3),", "Pointer to §C0.")
add("X35", "than its cross-range cell,\n", "than its cross-range cell, the footprint relation $R\\theta$ of §C0 subsection 3:\n", "Pointer to §C0.")

# ---- fog reach: §E4 table and reading, §C0 subsection 8 ----
add("X36", "| Reach ≈ 0.6–1 V, plus near clutter |", "| Reach ≈ 0.5–0.7 V at 20–50 m visibility (§C0 subsection 8), plus near clutter |",
    "The §C0 model gives 0.52 V at 50 m and 0.69 V at 20 m visibility; 1 V needs about 4 m.")
add("X37", "For the lidar's 0.6–1 V in dense fog, compare the measured ≈0.6 V of §A5, item 3 and the model of §C0 subsection 8, which gives about 0.5–0.7 V at 20–50 m visibility but only 0.13–0.3 V in lighter fog (200–1,000 m visibility).",
    "The lidar's 0.5–0.7 V in dense fog is the model of §C0 subsection 8 and agrees with the ≈0.6 V measured in §A5, item 3; in lighter fog (200–1,000 m visibility) the same model gives only 0.13–0.3 V.",
    "Matches the corrected table cell (X36).")
add("X38", "The \"≈0.6–1 V\" of §E4 therefore applies only below about 30 m visibility, and reach equals V only near 4 m visibility,",
    "A reach of 0.6 V therefore needs visibility below about 30 m, and reach equals V only near 4 m visibility,",
    "§E4 now quotes the model's 0.5–0.7 V (X36).")
add("X39", "| 1,000 m (light fog; $q_{\\rm K}=0.5$) |", "| 1,000 m (fog, at the haze boundary; $q_{\\rm K}=0.5$) |",
    "Same visibility classes as Figure C0.10d and its caption.")
add("X40", "| 50 m (dense fog) |", "| 50 m (thick fog) |", "As X39.")
add("X41", "| 20 m (very dense fog) |", "| 20 m (very thick fog) |", "As X39.")

# ---- §C3b Eq. (62) in the scheme's symbols, with the live fraction ----
add("X42", "If the sensor emits average optical power $P$ and shares it among $\\dot N$ points per second, each point gets energy $P/\\dot N$, and the number of signal photoelectrons detected per point is\n\n  $$N_s=\\frac{P}{\\dot N\\,E_{\\rm ph}}\\cdot\\frac{\\rho\\,A_{\\rm rx}}{\\pi R^2}\\,\\eta_{\\rm opt}\\,\\eta_{\\rm det}\\quad\\Longrightarrow\\quad \\dot N R^2=\\frac{P\\,\\rho\\,A_{\\rm rx}\\,\\eta_{\\rm opt}\\,\\eta_{\\rm det}}{\\pi\\,E_{\\rm ph}\\,N_s} \\tag{62}$$\n\n  where $N_s$ is the number of signal photoelectrons a point needs to be detected,",
    "This is §C0 Eq. (23) in clear air, with the energy per point in place of the pulse energy. A sensor that emits average optical power $P$ and shares it among $\\dot N$ points per second gives each point $E_{\\rm pt}=P/\\dot N$, and a point then yields $N_s=(E_{\\rm pt}/E_{\\rm ph})\\,\\rho A_{\\rm rx}/(\\pi R^2)\\,\\eta_{\\rm opt}\\,{\\rm PDE}$ detected signal photoelectrons (§C6, Eq. (80)). Setting $N_s$ equal to the number a detection needs, $n_{\\rm req}$ (§C0 subsection 10), gives\n\n  $$\\dot N R^2=\\frac{P\\,\\rho\\,A_{\\rm rx}\\,\\eta_{\\rm opt}\\,{\\rm PDE}}{\\pi\\,E_{\\rm ph}\\,n_{\\rm req}} \\tag{62}$$\n\n  where $n_{\\rm req}$ is the number of signal photoelectrons a point needs to be detected,",
    "Symbol scheme (E_pt, n_req, PDE as in §C0 and §C6); points to Eq. (23).")
add("X43", "$\\eta_{\\rm opt}$ the optics transmission and $\\eta_{\\rm det}$ the detector's photon detection efficiency. Everything",
    "$\\eta_{\\rm opt}$ the optics transmission and PDE the detector's photon detection efficiency; for a SPAD in sunlight the effective PDE also carries the dead-time live fraction (0.784 in the bright sun of §C0 subsection 10.3). Everything",
    "As X42, plus the dead-time caveat.")

# ---- §C4b: per-pulse photons N_{s,1}; hedged paralyzable model; 8-77% ----
span("X44", "**Saturation.** Let a channel have $N_c$ SPAD cells", "so 20 and 100 photons look almost the same.",
     [("$\\bar n$", "$N_{s,1}$"), ("\\bar n/N_c", "N_{s,1}/N_c"), ("$\\bar n\\ll N_c$", "$N_{s,1}\\ll N_c$"),
      ("$\\bar n\\gg N_c$", "$N_{s,1}\\gg N_c$"), ("N_{\\rm fired}\\approx\\bar n", "N_{\\rm fired}\\approx N_{s,1}"),
      ("$\\bar n=", "$N_{s,1}=")],
     "Detected photons per pulse are N_{s,1} in the scheme (n-bar is the coherent per-point count of §C0 subsection 10).",
     extra=[("if no cell had already fired (photons after PDE).", "if no cell had already fired (photons after PDE; the $N_{s,1}$ of §C0 Eq. (23))."),
            ("detected photons in a pulse:", "detected photons in a pulse, close to the ≈22 that §C0 Eq. (23) gives for a 10% target at 200 m with a 25 mm lens and 100 nJ:")])
add("X45", "can be dead **9–77% of the time** in bright sun (§C6(d)), and pile-up distorts its histogram. A passively recharged SPAD such as Sony's is paralyzable: a photon that arrives while it recovers restarts the recovery (§C5a),",
    "can be dead **8–77% of the time** in bright sun (§C6(d) and (d′)), and pile-up distorts its histogram. A passively recharged SPAD, as Sony's ISSCC 2021 chip appears to be (§C5a), is paralyzable: a photon that arrives while it recovers restarts the recovery,",
    "§C6(d′) row 1 is now 1.32e8 s^-1 (from 5.93e8); paralyzable behaviour is hedged as in §C5a.")
add("X46", "those cases run from $r=1.35\\times10^{8}/9=1.5\\times10^{7}\\ {\\rm s^{-1}}$ (940 nm, 20 nm filter, 10% scene), giving $1-e^{-0.09}\\approx9\\%$,",
    "those cases run from $r=1.32\\times10^{8}/9=1.46\\times10^{7}\\ {\\rm s^{-1}}$ (940 nm, 20 nm filter, 10% scene), giving $1-e^{-0.088}\\approx8\\%$,",
    "1.32e8/9 = 1.46e7; x 6 ns = 0.088.")
add("X47", "of the time, 8–59% (§C6(d)).", "of the time, 8–59% (§C6(d) and (d′)).", "As X45.")
add("X48", "Its passive recharge behaves paralyzably: a SPAD is live only if",
    "The model treats its SPADs as paralyzable [E], as passive recharge would make them, although the IMX459 press release says active recharge (§C5a): a SPAD is live only if",
    "Same hedge as §C5a and §C0 subsection 10.3.")

# ---- Part B/G/C3a/F2/C10.4/D7/C6 consistency ----
add("X49", "The stated rationale for 1550 nm was about 17× the eye-safe photon flux of 905 nm (derived in §C4 from the IEC 60825-1 laser-safety standard's long-exposure limits).",
    "The stated rationale for 1550 nm was about 16–17× the eye-safe photon flux of 905 nm (16.4× from the 9.6 mW long-exposure limit, 17.1× from its rounded 10 mW table entry; derived in §C4 from the IEC 60825-1 laser-safety standard).",
    "Matches §C4 item 1.")
add("X50", "its market value briefly exceeded roughly \\$10 B in late 2020 [U]",
    "its market value reached ≈\\$13.5 B at the peak close of \\$41.80 on 8 Dec 2020 [E, §C3a]",
    "§C3a computes the peak value from shares outstanding and the closing price.")
add("X51", "Against the ≈4×10⁴× gain at 1,550 nm (§C4c), it means",
    "Against the ≈4×10⁴× gain at 1,550 nm (§C4c, a 2014-edition figure, so the comparison mixes editions), it means",
    "The ≈4× above is from the 2007 edition.")
add("X52", "(NEVs: battery-electric and plug-in hybrid cars)", "(NEVs: battery-electric, plug-in hybrid and range-extended cars)",
    "Same NEV definition as §B1 and §C9.")
add("X53", "MicroVision bought the assets for about \\$2.2 M [P, MicroVision 10-Q].",
    "MicroVision bought the assets for \\$0.4 M plus a \\$1.8 M operating advance, about \\$2.2 M in all (§C3a) [P, MicroVision 10-Q].",
    "Matches §C3a and §C5.")
add("X54", "plus ≈50–100 mW of light.", "plus ≈30 mW of light per channel at 200 m, more at longer range (§C7a subsection 2(e)).",
    "Matches the central 30 mW of §C7a(e).")
add("X55", "At 20–30% wall-plug efficiency the laser alone draws $P_{\\rm opt}/\\eta_{\\rm wp}$, from $2.5/0.3\\approx8$ W to $7.5/0.2\\approx38$ W,",
    "At 15–30% wall-plug efficiency, the range of the §C7a model, the laser alone draws $P_{\\rm opt}/\\eta_{\\rm wp}$, from $2.5/0.3\\approx8$ W to $7.5/0.15=50$ W,",
    "Same wall-plug range as §C7a.")

# ---- Analog Photonics, OPA history (§C3a, §C7, §C10.7) ----
add("X56", "| ≈\\$45 M of US federal contracts and grants, mostly DARPA and ONR; SBIR only ≈\\$4.3 M [I] | No automotive programme; two unnamed Tier 1 JDAs (2018, 2020) [P]; defence FSOC and lasers (below; §C10.2b) |",
    "| ≈\\$45 M of US federal prime contracts and grants (≈\\$79 M with \\$34.2 M of subawards, mainly from AIM Photonics), mostly DARPA and ONR; SBIR only ≈\\$4.3 M [I] | No automotive production award found; two unnamed Tier 1 JDAs (2018, 2020) and on-car tests (2019) claimed [P]; defence FSOC and lasers (below; §C10.2b) |",
    "Matches the subaward analysis below and §C10.2b.")
add("X57", "The company does not live on SBIRs; it lives on large DARPA and ONR contracts.",
    "The company does not live on SBIRs; it lives on large DARPA and ONR prime contracts and on subawards, mainly from AIM Photonics.",
    "AIM Photonics provides \\$19.9 M of the \\$34.2 M of subawards.")
add("X58", "Its public milestones stop in 2021 [P].",
    "Its published milestone timeline stops in 2021 [P]; a 2023 company-authored IEEE Spectrum article promised automotive samples in 2025, and none were found (§C10.2b).",
    "Matches §C10.2b.")
add("X59", "(OPA with electro-optic phase shifters, 1.5 µm pitch, about 60°)",
    "(OPA with electro-optic phase shifters; its ≈60° phase-steered field implies a pitch of about 1.5 µm [E])",
    "The 512-element device of §C10.2b is 1.65 µm and 56°; 1.5 µm follows from lambda/(2 sin 30°).")
add("X60", "  - Voyant and Pointcloud: switched FPAs;",
    "  - Voyant: one on-chip axis plus a slow mirror (Carbon) and a switched FPA (Helium); Pointcloud: a switched FPA;",
    "Carbon pairs an on-chip steered axis with a slow mirror (§B8, §C8).")
add("X61", "- The only OPA product that shipped was Quanergy's S3-2, at 5–20 m [P, datasheet], and Quanergy went bankrupt [P, SEC 8-K] (§C10.2b).",
    "- The only fully solid-state OPA product that shipped was Quanergy's S3-2, at 5–20 m [P, datasheet], and Quanergy went bankrupt [P, SEC 8-K] (§C10.2b); Voyant's Carbon, which pairs one on-chip steered axis with a slow mirror, ships for industrial use (§B8).",
    "§C8 counts Carbon as an OPA-plus-mirror hybrid that ships.")
add("X62", "- Analog Photonics is the one serious OPA-lidar developer still publishing datasheets,",
    "- Analog Photonics is the one serious developer of two-axis non-mechanical OPA lidar still publishing datasheets,", "As X61.")

# ---- §C10 ----
add("X64", "about 0.9 mm at 0.1° and 1550 nm (§C7).",
    "about 0.9 mm at 0.1° and 1550 nm ($\\lambda/\\theta_{\\rm beam}$, before the truncation and single-polarization factor $t^2/2$ of §C10.3b, which gives an equivalent diameter of ≈0.65 mm, 0.33 mm²; §C7).",
    "0.419 x (0.888 mm)^2 = 0.33 mm^2, i.e. 0.65 mm across.")
add("X65", "**unlikely this decade**", "**unlikely by 2032**", "§C10.7 uses 'by 2032'.")
add("X66", "so $t^2=0.837$.", "so $t^2=0.838$.", "t = 0.9154, t^2 = 0.838, as in §C0 subsection 10.2.")
add("X68", "covers about 2% of a 0.05° cell at 200 m (§C10.3a).", "covers about 2% of a 0.05° cell at 200 m (§C10.3b, Result 2).",
    "The 2.1% is computed in §C10.3b, Result 2.")
add("X69", "still covers only ≈2% of its cell (§C10.3a).", "still covers only ≈2% of its cell (§C10.3b, Result 2).", "As X68.")
add("X70", "rather than ≈2% of it (§C10.3a),", "rather than ≈2% of it (§C10.3b, Result 2),", "As X68.")
add("X71", "=0.030$ m² (§C10.3a).", "=0.030$ m² (§C10.3b, Result 2).", "As X68.")
add("X72", "of a 0.05° cell per collimated sample (§C10.3a).", "of a 0.05° cell per collimated sample (§C10.3b, Result 2).", "As X68.")

# per-aperture speckle count N_spk in §C10.3a-b (N_sp stays the number of summed looks, as in §C0 subsection 10)
a = text.find("$$N_{\\rm sp}\\sim\\frac{A_{\\rm rx}\\,\\Omega_{\\rm spot}}{\\lambda^2} \\tag{143}$$")
b = text.find("**Result 2:", a)
para0 = text.rfind("\n", 0, a)
old = text[para0 + 1:b]
assert text.count(old) == 1
new = old.replace("N_{\\rm sp}", "N_{\\rm spk}")
anchor = "The exact coupling depends on illumination and pupil shape."
assert new.count(anchor) == 1
new = new.replace(anchor, anchor + " A single-mode receiver still fades like one look, however many speckles fall across its aperture.")
# X63 lies inside this passage: the §C10.3a item 7 caveat title contradicted the table beneath it (14 -> 29 -> 57 mm)
x63 = "- **Finer resolution shrinks ToF's usable aperture.**"
assert new.count(x63) == 1
new = new.replace(x63, "- **Finer resolution needs a larger ToF aperture than a module can hold.**")
# X67 also lies inside it (§C10.3b, What was computed): §C0 subsection 10.2 derives the 0.45, it is not a free choice
x67 = "the ratio 0.45 is a model choice, the same as in §C0 subsection 10.2."
assert new.count(x67) == 1
new = new.replace(x67, "the ratio 0.45 is the far-field optimum derived in §C0 subsection 10.2.")
edits.append({"id": "X73", "finding": "cross_section", "old": old, "new": new,
              "why": "N_sp is the number of summed looks in §C0 subsection 10 and §C10.2; the per-aperture speckle count gets its "
                     "own symbol. Also (X63) the item 7 caveat title now matches its table, where the aperture grows."})
# ---- §C7b background events: 3.66e8 x 20.8 us x 0.784 = 5,968 ----
add("X74", "would have to stand out against all 5,960 events. The random (Poisson) fluctuation of 5,960 counts is $\\sqrt{5{,}960}\\approx77$. At 5 standard deviations that takes $5\\sqrt{5{,}960}\\approx390$ counts",
    "would have to stand out against all 5,970 events. The random (Poisson) fluctuation of 5,970 counts is $\\sqrt{5{,}970}\\approx77$. At 5 standard deviations that takes $5\\sqrt{5{,}970}\\approx390$ counts",
    "3.66e8 s^-1 x 20.8 us x 0.784 = 5,968.")

# ---- leftover old symbols: E_opt (§C0 10.6), theta_step (§B7.1), Eq. (14) ----
span("X75", "The best aperture has $u=1$, so relative to its energy per point $E_{\\rm opt}$", "$E_{\\rm pt}/E_{\\rm opt}\\approx\\tfrac12\\,10^{\\mathcal{M}_0/20}$",
     [("E_{\\rm opt}", "E_{\\rm best}")], "E_opt was the old name of the optical energy per point; here it is the best design's energy.")
span("X76", "Two adjacent rays separated by an angular step $\\theta_{\\rm step}$", "$$s = R\\tan\\theta_{\\rm step} \\tag{17}$$",
     [("\\theta_{\\rm step}", "\\delta\\theta")], "Angular spacing of points is delta-theta (scheme).")
add("X77", "$$d = v\\,t_r + \\frac{v^2}{2a} \\tag{14}$$\n\n  where $d$ is the stopping distance (m), $v$ the initial speed (m/s; km/h divided by 3.6), $t_r$ the reaction time before braking begins (s), and $a$ the braking deceleration (m/s²).",
    "$$d = v\\,t_{\\rm r} + \\frac{v^2}{2a_{\\rm b}} \\tag{14}$$\n\n  where $d$ is the stopping distance (m), $v$ the initial speed (m/s; km/h divided by 3.6), $t_{\\rm r}$ the reaction time before braking begins (s), and $a_{\\rm b}$ the braking deceleration (m/s²).",
    "Same symbols as Eqs. (11), (162), (170) and (184).")
add("X78", "The stopping distance of Eq. (14), $d=v\\,t_r+v^2/(2a)$,", "The stopping distance of Eq. (14), $d=v\\,t_{\\rm r}+v^2/(2a_{\\rm b})$,", "As X77.")
add("X79", "Eq. (14), with $v$ the speed, $t_r$ the reaction time and $a$ the deceleration;",
    "Eq. (14), with $v$ the speed, $t_{\\rm r}$ the reaction time and $a_{\\rm b}$ the deceleration;", "As X77.")

# ---- display equations split with aligned: full-size fractions ----
for eid, tag in (("X80", "\\tag{40}$$"), ("X81", "\\tag{46}$$"), ("X82", "\\tag{139}$$")):
    end = text.find(tag)
    start = text.rfind("$$\\begin{aligned}", 0, end)
    assert 0 <= start and end - start < 1200, eid
    old = text[start:end + len(tag)]
    new = old.replace("\\frac{", "\\dfrac{").replace("\\int_0^\\infty", "\\displaystyle\\int_0^\\infty")
    assert new != old
    edits.append({"id": eid, "finding": "cross_section (rendering)", "old": old, "new": new,
                  "why": "MathML table cells are set in text style; dfrac and displaystyle keep full-size fractions and integral."})

OUT.write_text(json.dumps({"block": "12_cross_section", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(edits), "edits written to", OUT.name)
