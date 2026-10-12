"""Round 2, agent R2D_C7b: build the edit list for section C7b (from "## C7b." to "## C8.").

Reads the live report (read only), takes every "old" text from it (whole lines by number, checked against an expected
start, or literal fragments checked to occur exactly once), and writes edits/round2/R2D_C7b.json. The numbers in the
"new" texts come from r2d_c7b_numbers.py (same folder), which imports the installed model.

Run from anywhere:
    python r2d_c7b_build_edits.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]                       # .../scripts_archive/readability_2026-10-03
REPORT = HERE.parents[3] / "automotive_perception_report_2026-09-27.md"
OUT = WORK / "edits" / "round2" / "R2D_C7b.json"

TEXT = REPORT.read_text(encoding="utf-8")
L = TEXT.split("\n")
C7B = (TEXT.find("## C7b."), TEXT.find("## C8."))


def line(n, start):
    s = L[n - 1]
    assert s.startswith(start), (n, s[:90])
    return s


def block(n1, n2, start):
    s = "\n".join(L[n1 - 1:n2])
    assert s.startswith(start), (n1, s[:90])
    return s


EDITS, SKIPPED = [], []


def edit(finding, old, new, why):
    k = TEXT.count(old)
    assert k == 1, (finding, k, old[:80])
    a = TEXT.find(old)
    assert C7B[0] < a and a + len(old) < C7B[1], ("outside C7b", old[:80])
    EDITS.append({"id": f"R2D_C7b-{len(EDITS) + 1:03d}", "finding": finding, "old": old, "new": new, "why": why})


D1 = "Round 2 decision 1 (FMCW dwell T_int + 2 tau, ungated central case)"
D23 = "Round 2 decisions 2-3 (ToF 0.05 x 0.05 deg macro-pixel; n_req 21.7 with the x1.45 margin)"
D5 = "Round 2 decision 5 (single parity definition, section C7b subsection 5)"

# ---------------------------------------------------------------- short answer
edit(D23 + "; " + D1,
     "- **Per joule of emitted light, FMCW buys ≈3.2× fewer sampled points than 940 nm SPAD ToF. The reason is spatial, "
     "not temporal** (subsection 1). With the coherent efficiencies measured so far (0.057–0.168), the gap is 5–14× rather "
     "than 3.2× (subsection 1(c)).",
     "- **Per joule of useful light, FMCW buys ≈4.2× fewer sampled points than 940 nm SPAD ToF. The reason is spatial, "
     "not temporal** (subsection 1). Useful light is the light whose echo arrives inside the receiver's measurement "
     "windows; an ungated CW channel also emits during the round trips, which widens the gap to ≈5.3× per joule emitted "
     "(subsection 1(e)). With the coherent efficiencies measured so far (0.057–0.168), the gap is 6–19× rather than 4.2× "
     "(subsection 1(c)).",
     "ToF reference 72 nJ (0.303/0.0717 = 4.2); ungated FMCW emits 0.384 uJ (5.3x); measured-eta gaps 6.3-18.6x.")
edit(D23,
     "and still needs 120 photoelectrons per point against 25 counts for ToF (§C0 subsection 10.3).",
     "and still needs 120 photoelectrons per point against 21.7 counts for ToF (§C0 subsection 10.3).",
     "ToF n_req = 1.45 x 14.98 = 21.7.")
edit(D23,
     "against ≈93 nJ per ToF point (200 m, 10% target)",
     "against ≈72 nJ per ToF point (200 m, 10% target)",
     "ToF E_pt 71.7 nJ.")
edit(D23,
     "and about 160× the 93 nJ of a ToF point.",
     "and about 200× the 72 nJ of a ToF point.",
     "14.6 uJ / 72 nJ = 203.")
edit(D23,
     "it would need ≈15× more energy to stand out.",
     "it would need ≈13× more energy to stand out.",
     "5 sqrt(3,370) = 290 counts against 21.7: 13.4x (subsection 1(a)).")
edit(D1,
     "apart from the 12–35% it emits during the last $\\tau$ of each ramp, whose echo falls in the next ramp's discarded "
     "window.",
     "apart from the 12–35% it emits during the last $\\tau$ of each ramp (21% in the §C7a central case), whose echo "
     "falls in the next ramp's discarded window.",
     "Central case 2.67/12.67 = 21%.")
edit(D1,
     "A coherent channel costs ≈176 mW of receive power (four receivers of ≈44 mW) plus ≈200 mW of electrical power for "
     "its light (2026 central).",
     "A coherent channel costs ≈185 mW of receive power (four receivers of ≈46 mW) plus ≈200 mW of electrical power for "
     "its light (2026 central).",
     "E_rx 2.337 uJ over the 12.67 us dwell = 184 mW per channel (subsection 3).")
edit(D1,
     "but only 1.2× at 25 Mpts/s, where an ungated one can reach the allowance.",
     "but only 1.2× at 25 Mpts/s, where the ungated §C7a central transmitter, at 9.6 W, exceeds it.",
     "Central case is ungated: 7.58 W x 1.267 = 9.6 W > 9.1 W.")
edit(D5,
     "- **Parity with ToF needs three things at once** (subsection 5):",
     "- **Parity with ToF, defined as ≥15 Mpts/s in ≤15 W at 200 m and 10%, needs three things at once** (subsection 5):",
     "State the single parity definition where the conditions are listed.")
edit("round1_skipped [08_C7b] report #6 (channel count); " + D5,
     "a coherent receiver chip with ≥150 channels of four receivers each, at ≈8–13 mW per channel",
     "a coherent receiver chip with 115–190 channels of four receivers each (460–760 receivers), at ≈8–13 mW per "
     "channel",
     "One channel requirement throughout: 140-190 ungated, 115 gated (subsection 5).")
edit(D5 + "; " + D1 + "; " + D23,
     line(4934, "  - Without the efficient laser or the lower energy per point, a 15 Mp"),
     "  - With all three, a 15 Mpts/s sensor whose transmitter stays on through the round trips draws ≈14 W at 15 mW "
     "per channel, just inside the target; channels brighter than ≈22 mW stay inside it only if the transmitter is "
     "gated. That is "
     "still 1.8× the electrical energy per point of the 2026 SPAD ToF reference, which needs 9.2 W at 15 Mpts/s. Without "
     "the efficient laser or the lower energy per point, the sensor stays near 23.5 W; without the low-power receiver, "
     "near 48 W. Today's central case, at 15 Mpts/s and 200 m, is ≈76.5 W.",
     "Parity table recomputed on the ungated basis (subsection 5): 14.0 / 23.5-23.7 / 47.6 / 76.5 W; ToF 9.2 W.")

# ---------------------------------------------------------------- subsection 1
edit(D23 + "; " + D1,
     "A 940 nm SPAD time-of-flight sensor needs ≈93 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, "
     "about 3.2× more. The gap comes from how much of the echo each receiver can collect, not from pulsed versus "
     "continuous light.",
     "A 940 nm SPAD time-of-flight sensor needs ≈72 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, "
     "about 4.2× more. The gap comes from how much of the echo each receiver can collect, not from pulsed versus "
     "continuous light, which adds only the light an ungated CW channel emits during the round trips: 1.27× the useful "
     "energy in the §C7a central case (item (e)).",
     "ToF 72 nJ; ratio 4.2; ungated factor 12.67/10.")
edit(D23 + "; " + D1,
     block(4949, 4950, "  - SPAD ToF: $93\\ {\\rm nJ}"),
     "  - SPAD ToF: $72\\ {\\rm nJ}\\times15\\times10^{6}\\ {\\rm s^{-1}}=1.1$ W;\n"
     "  - FMCW: $0.30\\ \\mu{\\rm J}\\times15\\times10^{6}\\ {\\rm s^{-1}}=4.5$ W of useful light, and 1.27 times as "
     "much, 5.7 W, from a transmitter that also emits during the round trips (item (e)).",
     "72 nJ x 15e6 = 1.08 W; 4.5 W x 1.267 = 5.7 W emitted.")
edit(D23,
     line(4960, "  - **In the §C7a model:** a macro-pixel"),
     "  - **In the §C7a model:** a macro-pixel (a group of SPADs read out as one pixel, here 3×3 SPADs viewing a "
     "0.05° × 0.05° field) in bright sun counts $r_{\\rm bg}=1.83\\times10^{8}$ s⁻¹. That is half the fully sunlit case "
     "of §C6(d), $2.965\\times10^{8}$ s⁻¹ at a photon detection efficiency (PDE) of 0.3, scaled to the model's PDE of "
     "0.37: $2.965\\times10^{8}\\times(0.37/0.3)/2=1.83\\times10^{8}$ s⁻¹. It listens for the 20.8 µs column time per "
     "point (≈10 shots of ≈2 µs, §C6). Each of its nine SPADs counts $r=1.83\\times10^{8}/9=2.03\\times10^{7}$ s⁻¹. With "
     "the dead time $\\tau_d=6$ ns this gives $r\\tau_d=0.122$, so each SPAD is dead (unable to count) for "
     "$1-e^{-0.122}=11.5\\%$ of that time (Eq. (82), paralyzable form), and the macro-pixel is live for a fraction 0.885 "
     "of it. That gives "
     "$1.83\\times10^{8}\\times20.8\\times10^{-6}\\times0.885\\approx3{,}370$ background events per point. (§C7a(c) counts "
     "≈3,390 because it adds the 21.7 signal counts.)",
     "0.05 x 0.05 deg pixel halves r_bg; dead fraction, live fraction and events recomputed with substitutions.")
edit(D23,
     line(4961, "  - **Per bin:** these events are spread"),
     "  - **Per bin:** these events are spread over the ≈2,080 histogram bins of 1 ns in each shot's 2.08 µs listening "
     "window (≈300 m of range), so there are $3{,}370/2{,}080\\approx1.62$ counts per bin. Eq. (98), with the 0.885 live "
     "fraction, gives the same: $1.83\\times10^{8}\\times10^{-9}\\times10\\times0.885=1.62$. So the model's 21.7 signal "
     "counts in one bin stand out clearly: the detection threshold is 12 counts (§C0 subsection 10.3).",
     "b = 1.62; Poisson tail 1.1e-6 at 11 and 1.5e-7 at 12 counts against 5e-7 per bin, so threshold 12.")
edit(D23,
     line(4962, "  - **The same energy spread evenly in time,**"),
     "  - **The same energy spread evenly in time,** as with CW light, would have to stand out against all ≈3,370 "
     "background events. Their random (Poisson) fluctuation is $\\sqrt{3{,}370}\\approx58$ counts. At 5 standard "
     "deviations that takes $5\\sqrt{3{,}370}\\approx290$ counts: $290/21.7\\approx13$ times the energy per point, before "
     "any requirement on ranging precision.",
     "sqrt(3,370) = 58; 5 x 58 = 290; 290/21.7 = 13.4.")
edit(D23,
     "some 35× the SPAD's 25 counts.",
     "some 41× the SPAD's 21.7 counts.",
     "890/21.7 = 41.")
edit(D1,
     "or 0.006 photons in a 10 µs dwell.",
     "or 0.006 photons in the 10 µs that one point integrates ($T_{\\rm int}$, subsection 2(b)).",
     "The dwell is 12.67 us; the 10 us is the integration time (650 /s x 10 us = 0.0065).")
edit(D23,
     "The model uses 120, a ×1.36 margin, close to the ×1.45 that takes ToF from 17.3 to 25 counts.",
     "The model uses 120, a ×1.36 margin, close to the ×1.45 that takes ToF from the ideal 15.0 to 21.7 counts.",
     "Ideal requirement at b = 1.62 is 14.98 counts; 21.7/14.98 = 1.45.")
edit(D1,
     "**(c) Result: points per joule of emitted light, 200 m, 10% target**",
     "**(c) Result: points per joule of light, 200 m, 10% target**",
     "The FMCW rows count the useful light; the emitted light of an ungated channel is given in the notes.")
edit(D23,
     "a coherent sample needs 120 photoelectrons against 25 counts (§C0 subsection 10.3);",
     "a coherent sample needs 120 photoelectrons against 21.7 counts (§C0 subsection 10.3);",
     "ToF n_req 21.7.")
edit(D23,
     "| 940 nm SPAD or SiPM dToF, scanned or line-flash, 25 mm lens | 491 mm² (whole lens) | 25 counts | 0.145 | 93 nJ | "
     "$1.1\\times10^{7}$ |",
     "| 940 nm SPAD or SiPM dToF, scanned or line-flash, 25 mm lens | 491 mm² (whole lens) | 21.7 counts | 0.164 | "
     "72 nJ | $1.4\\times10^{7}$ |",
     "n_req 21.7, eta 0.164, E_pt 71.7 nJ, 1/E = 1.4e7 per J.")
edit(D23,
     "Worked example (SPAD row): $25\\times2.11\\times10^{-19}\\times1.26\\times10^{5}/(0.1\\times4.91\\times10^{-4}\\times0.145)"
     "=9.3\\times10^{-8}$ J.",
     "Worked example (SPAD row): $21.7\\times2.11\\times10^{-19}\\times1.26\\times10^{5}/(0.1\\times4.91\\times10^{-4}\\times"
     "0.164)=7.2\\times10^{-8}$ J.",
     "5.77e-13 / 8.05e-6 = 7.2e-8 J.")
edit(D23,
     "  - ToF: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction 0.784 (6 ns paralyzable "
     "dead time, §C7a(a));",
     "  - ToF: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction 0.885 (6 ns paralyzable "
     "dead time, (a) and §C7a(a)), i.e. $0.5\\times0.37\\times0.885=0.164$;",
     "Live fraction 0.885 at the halved background.")
edit(D23,
     "for example $1/(9.3\\times10^{-8}\\ {\\rm J})=1.1\\times10^{7}$ points per joule.",
     "for example $1/(7.2\\times10^{-8}\\ {\\rm J})=1.4\\times10^{7}$ points per joule.",
     "1/7.2e-8 = 1.39e7.")
edit(D23 + "; " + D1,
     "so FMCW buys 5–7× (discrete fibre chain) or ≈14× (integrated array) fewer points per optical joule than SPAD "
     "ToF, instead of ≈3.2×.",
     "so FMCW buys $4.23\\times0.25/0.168=6.3$ to $4.23\\times0.25/0.112=9.4$ times (discrete fibre chain) or "
     "$4.23\\times0.25/0.057=18.6$ times (integrated array) fewer points per optical joule than SPAD ToF, instead of "
     "≈4.2×. Here 4.23 is the unrounded ratio of Eq. (104), $0.303\\ \\mu{\\rm J}/71.7\\ {\\rm nJ}$.\n"
     "- **Useful and emitted light:** the FMCW rows count the light whose echo arrives inside the useful windows. "
     "An ungated CW transmitter also emits during the round trips (item (e)), 1.27 times as much in the §C7a central "
     "case: 0.384 µJ per sample, or $1/(3.84\\times10^{-7}\\ {\\rm J})=2.6\\times10^{6}$ samples per emitted joule.",
     "4.23 x (1.49, 2.23, 4.39) = 6.3, 9.4, 18.6; emitted 0.303 x 12.67/10 = 0.384 uJ.")
edit(D23,
     "Why FMCW buys ≈3.2× fewer sampled points per joule than SPAD ToF.** Let $E_{\\rm FMCW}$ be the optical energy per "
     "FMCW sample (0.30 µJ) and $E_{\\rm ToF}$ the optical energy per SPAD ToF point (93 nJ)",
     "Why FMCW buys ≈4.2× fewer sampled points per joule than SPAD ToF.** Let $E_{\\rm FMCW}$ be the optical energy per "
     "FMCW sample (0.30 µJ) and $E_{\\rm ToF}$ the optical energy per SPAD ToF point (72 nJ)",
     "Ratio 4.2 with the 72 nJ ToF point.")
edit(D23,
     "\\times\\underbrace{\\frac{120}{25}}_{\\rm detection}\\times\\underbrace{\\frac{940}{1{,}550}}_{\\rm photon\\ energy}"
     "\\times\\underbrace{\\frac{0.145}{0.25}}_{\\rm efficiency}=1.93\\times4.8\\times0.607\\times0.580\\approx3.25. "
     "\\tag{104}",
     "\\times\\underbrace{\\frac{120}{21.7}}_{\\rm detection}\\times\\underbrace{\\frac{940}{1{,}550}}_{\\rm photon\\ energy}"
     "\\times\\underbrace{\\frac{0.164}{0.25}}_{\\rm efficiency}=1.93\\times5.53\\times0.606\\times0.656\\approx4.2. "
     "\\tag{104}",
     "1.93 x 5.53 x 0.606 x 0.656 = 4.24 (model 0.3034/0.0717 = 4.23); 940/1550 = 0.606.")
edit(D23,
     line(5033, "- **Detection statistics (4.8×):**"),
     "- **Detection statistics (5.5×):** the four looks need 120 photoelectrons and ToF 21.7 counts; for the ideal "
     "requirements the ratio is 5.9 ($88.5/15.0$, §C0 subsection 10.3). Of the ideal 5.9, ×1.46 is the coherent "
     "receiver's one photoelectron of shot noise in each of the ≈2,450 FFT bins it searches (15.0 → 21.9), ×1.79 is "
     "finding the peak in both ramps (21.9 → 39.1), and ×2.26 is speckle fading with four looks (39.1 → 88.5): "
     "$1.46\\times1.79\\times2.26=5.9$.",
     "120/21.7 = 5.53; 88.5/14.98 = 5.9; 21.9/15.0 = 1.46.")
edit(D23,
     "- **Efficiency (0.58×):** the FMCW model's $\\eta=0.25$ is higher than the ToF model's 0.145,",
     "- **Efficiency (0.66×):** the FMCW model's $\\eta=0.25$ is higher than the ToF model's 0.164,",
     "0.164/0.25 = 0.66.")
edit(D23,
     "- **Per fully covered cell the gap is ≈160×** ($14.6\\ \\mu{\\rm J}/93\\ {\\rm nJ}$).",
     "- **Per fully covered cell the gap is ≈200×** ($14.6\\ \\mu{\\rm J}/72\\ {\\rm nJ}=203$).",
     "14.6 uJ / 72 nJ = 203.")
edit(D1,
     "  - At 16–30 mW per channel, a share $2\\tau/T_{\\rm dwell}$ of 12–35% of the transmitted energy is emitted during "
     "the dead time and wasted (subsection 2 table).",
     "  - At 16–30 mW per channel, a share $2\\tau/T_{\\rm dwell}$ of 12–35% of the transmitted energy is emitted during "
     "the dead time and wasted (subsection 2 table).\n"
     "  - The §C7a central case is ungated: $E_{\\rm pt}=0.303$ µJ at $P_{\\rm ch}=30$ mW gives $T_{\\rm int}=10$ µs and "
     "$T_{\\rm dwell}=12.67$ µs, so each point costs $0.303\\times12.67/10=0.384$ µJ of emitted light, 21% of it wasted. "
     "Per joule emitted, FMCW therefore buys $0.384/0.072\\approx5.3$ times fewer points than SPAD ToF, against the 4.2 "
     "of Eq. (104) for the useful light.",
     "Decision 1: emitted energy E_pt T_dwell/T_int in the central case.")
edit(D23,
     "The same SPAD receiver needs only $93\\ {\\rm nJ}\\times(10/200)^2=0.23$ nJ per point at 10 m",
     "The same SPAD receiver needs only $72\\ {\\rm nJ}\\times(10/200)^2=0.18$ nJ per point at 10 m",
     "72 x 0.0025 = 0.18 nJ.")
edit(D23,
     "and SPAD ToF $93\\ {\\rm nJ}\\times(300/200)^2=0.21$ µJ per point, so the ratio of Eq. (104) falls from 3.2 at "
     "200 m to $0.45/0.21=2.1$ at 300 m [E].",
     "and SPAD ToF $72\\ {\\rm nJ}\\times(300/200)^2=0.16$ µJ per point, so the ratio of Eq. (104) falls from 4.2 at "
     "200 m to $0.45/0.16=2.8$ at 300 m [E].",
     "72 x 2.25 = 162 nJ; 0.45/0.16 = 2.8.")

# ---------------------------------------------------------------- subsection 2
edit(D1,
     "Then $T_{\\rm dwell}=10+2.67=12.7$ µs and $\\dot N_{\\rm ch}=1/12.7\\ \\mu{\\rm s}=79$ kpts/s.",
     "Then $T_{\\rm dwell}=10+2.67=12.7$ µs and $\\dot N_{\\rm ch}=1/12.7\\ \\mu{\\rm s}=79$ kpts/s. This is the §C7a "
     "central case, whose 10 µs of integration are its two 5 µs useful windows.",
     "Tie Eq. (107) to the model's single dwell definition.")
edit("round1_skipped [08_C7b] consistency flag (Eq. (109) vs Eq. (94)); round1_skipped [08_C7b] report #1 (search "
     "range); " + D1,
     "  - At 300 m (the §C7a case, with the same $T_u=5$ µs), it is $5\\times300/0.15+2{,}260=10{,}000+2{,}260\\approx"
     "12{,}300$.",
     "  - At 300 m (the §C7a case, with the same $T_u=5$ µs), it is $5\\times300/0.15+2{,}260=10{,}000+2{,}260\\approx"
     "12{,}300$. This is the count of §C7a's Eq. (94): Eq. (109) becomes Eq. (94) when $R$ is the far end of the range "
     "searched, $R_{\\max}=300$ m, and the chirp duration $T$ of Eq. (94) is read as the useful window $T_u$, since only "
     "the useful windows are digitized. The §C7a model digitizes this whole 0–300 m search for its 200 m design point; "
     "a sensor that searched only to 200 m would need the 8,900 samples above.",
     "Cross-reference Eq. (109) to Eq. (94) and state once which range a 200 m sensor digitizes.")
edit(D23,
     "the same SPAD ToF model needs $0.21\\ \\mu{\\rm J}\\times10^{7}\\ {\\rm s^{-1}}=2.1$ W of useful light with a fixed "
     "25 mm lens, against FMCW's 4.5 W, a ratio of 2.1 rather than the 3.2 of 200 m.",
     "the same SPAD ToF model needs $0.16\\ \\mu{\\rm J}\\times10^{7}\\ {\\rm s^{-1}}=1.6$ W of useful light with a fixed "
     "25 mm lens, against FMCW's 4.5 W, a ratio of 2.8 rather than the 4.2 of 200 m.",
     "ToF 0.16 uJ at 300 m; 4.5/1.6 = 2.8.")
edit(D1,
     "so at 25 Mpts/s it can exceed the allowance [E].",
     "so at 25 Mpts/s it can exceed the allowance. The upper values, at 30 mW per channel, are the ungated §C7a central "
     "case [E].",
     "The model's central case is the ungated 30 mW one (3.84 / 9.61 W).")
edit(D23,
     "  - SPAD ToF emits 0.93 W at 10 Mpts/s and 2.3 W at 25 Mpts/s, 9.3 nJ per shot and point.",
     "  - SPAD ToF emits 0.72 W at 10 Mpts/s and 1.8 W at 25 Mpts/s, 7.2 nJ per shot and point.",
     "72 nJ x 1e7 = 0.72 W, x 2.5e7 = 1.8 W; 72/10 shots = 7.2 nJ.")
edit(D1,
     "at 25 Mpts/s an ungated FMCW transmitter reaches the allowance.",
     "at 25 Mpts/s the ungated §C7a central transmitter exceeds it (9.6 against 9.1 W).",
     "7.58 W x 1.267 = 9.6 W.")
edit(D23,
     "would need 0.84 µJ per point at 600 m and 8.4 W at 10 Mpts/s, far beyond its average-power limits.",
     "would need 0.65 µJ per point at 600 m and 6.5 W at 10 Mpts/s, far beyond its small-source average limit of "
     "≈0.24–0.28 W.",
     "72 nJ x 9 = 0.65 uJ; x 1e7 = 6.5 W (23-27x the small-source limit).")
edit(D23,
     "the gated floor of ≈49 W is still ≈3.5× the ≈14 W of the SPAD ToF sensor at the same range and rate.",
     "the gated floor of ≈49 W is still $49.4/11.7\\approx4.2$ times the ≈11.7 W of the SPAD ToF sensor at the same "
     "range and rate.",
     "49.4/11.7 = 4.2.")
edit(D23,
     "For ToF, $93\\ {\\rm nJ}\\times(600/200)^2=0.84$ µJ.",
     "For ToF, $72\\ {\\rm nJ}\\times(600/200)^2=0.65$ µJ, and $0.65\\ \\mu{\\rm J}\\times10^{7}\\ {\\rm s^{-1}}=6.5$ W.",
     "Substitution for the 600 m ToF figures.")
edit(D23,
     "and ≈70 nJ of SPAD-SoC receive electronics (§C7a(c)): $3\\ {\\rm W}+10^{7}\\ {\\rm s^{-1}}\\times(93\\ {\\rm nJ}"
     "\\times2.25/0.20+70\\ {\\rm nJ})=3+11.2=14.2$ W.",
     "and ≈57 nJ of SPAD-SoC receive electronics (§C7a(c)): $3\\ {\\rm W}+10^{7}\\ {\\rm s^{-1}}\\times(72\\ {\\rm nJ}"
     "\\times2.25/0.20+57\\ {\\rm nJ})=3+8.7=11.7$ W.",
     "810 + 57 = 867 nJ per point; 3 + 8.67 = 11.7 W.")

# ---------------------------------------------------------------- subsection 3
edit(D1 + "; " + D23,
     "each with four receivers and drawing ≈376 mW of electrical power (receivers plus its share of the laser), against "
     "≈26 mW per ToF channel.",
     "each with four receivers and drawing ≈385 mW of electrical power (receivers plus its share of the laser), against "
     "≈20 mW per ToF channel.",
     "185 + 200 mW against 2.7 + 17.2 mW.")
edit("round1_skipped [08_C7b] report #1 (dwell definitions, column name, 4 us case); round1_skipped [08_C7b] report #6; "
     + D1,
     block(5332, 5343, "The table applies Eq. (121) to four point rates at three dwells."),
     "The table applies Eq. (121) to four point rates at two dwells, both with the 2.67 µs of round trips at 200 m: the "
     "§C7a central dwell, 10 µs of integration (30 mW at 0.30 µJ), and a short one, 4 µs of integration.\n"
     "\n"
     "| Target point rate | Channels at 6.67 µs dwell (4 µs integration + $2\\tau$) | Channels at 12.67 µs dwell "
     "(10 µs integration + $2\\tau$; §C7a central) |\n"
     "|---|---|---|\n"
     "| 2 Mpts/s (Aeries-class) | 13 | 25 |\n"
     "| 10 Mpts/s | 67 | 127 |\n"
     "| 15 Mpts/s (the parity point rate) | 100 | 190 |\n"
     "| 41 Mpts/s (RoboSense EM4, ToF) | 273 | 519 |\n"
     "\n"
     "*How the table is computed* [E]:\n"
     "- $N_{\\rm ch}=\\dot N\\,T_{\\rm dwell}$ (Eq. (121)), with $T_{\\rm dwell}=T_{\\rm int}+2\\tau$ (Eq. (107)); for "
     "example $41\\times10^{6}\\times6.67\\times10^{-6}=273$ and $41\\times10^{6}\\times12.67\\times10^{-6}=519$.\n"
     "- A 4 µs integration time is close to the lower practical end at 200 m. It means $T_u=2$ µs per ramp and "
     "$T_c=T_u+\\tau=3.33$ µs. The sampling rate is then $f_s\\approx1.9$ GS/s for a search to 200 m (subsection 2(c) "
     "table), or ≈2.7 GS/s for the 0–300 m search of the §C7a model (§C7a(d)), and each channel needs "
     "$P_{\\rm ch}=E_{\\rm pt}/T_{\\rm int}=0.30\\ \\mu{\\rm J}/4\\ \\mu{\\rm s}\\approx76$ mW (38 mW at 0.15 µJ).",
     "One dwell definition: the 10 us column was the integration time; the short case is 4 us + 2 tau.")
edit(D23,
     block(5349, 5351, "- **Power per ToF channel.**"),
     "- **Power per ToF channel.** At the §C7a central values (≈57 nJ of receive electronics and ≈0.36 µJ of laser "
     "electrical energy per ToF point):\n"
     "  - receive: $15\\times10^{6}\\times57\\ {\\rm nJ}=0.855$ W, i.e. $0.855\\ {\\rm W}/312=2.7$ mW per macro-pixel;\n"
     "  - laser: $15\\times10^{6}\\times0.36\\ \\mu{\\rm J}=5.4$ W, i.e. ≈17 mW per macro-pixel.",
     "ToF electronics 57 nJ and laser 358 nJ per point.")
edit(D1,
     block(5354, 5355, "  - receive: $15\\times10^{6}\\times2.23"),
     "  - receive: $15\\times10^{6}\\times2.34\\ \\mu{\\rm J}=35.1$ W, i.e. ≈185 mW per channel, ≈46 mW for each of its "
     "four receivers (2.34 µJ is the §C7a receiver energy per point, $E_{\\rm rx}$ below);\n"
     "  - light: each channel transmits 30 mW continuously, round trips included, i.e. $0.030/0.15=200$ mW of electrical "
     "power at 15% wall-plug efficiency.",
     "E_rx with the analog power over the 12.67 us dwell; 35.1 W / 190 = 185 mW.")
edit(D1 + "; " + D23,
     "- **So the per-channel electrical power is ≈376 mW for FMCW against ≈26 mW for ToF, ≈15× more.**",
     "- **So the per-channel electrical power is ≈385 mW for FMCW (185 + 200 mW) against ≈20 mW for ToF (2.7 + 17 mW), "
     "≈19× more.**",
     "384.7/19.97 = 19.3.")
edit(D1,
     "The transmitted power is larger by the dead-time factor, e.g. $190\\times30\\ {\\rm mW}=5.7$ W.",
     "The power an ungated transmitter emits is larger by the dead-time factor $T_{\\rm dwell}/T_{\\rm int}$, e.g. "
     "$190\\times30\\ {\\rm mW}=5.7$ W in the §C7a central case.",
     "Name the factor and the case.")
edit("round1_skipped [08_C7b] report #1 (E_rx with T_dwell; search range); " + D1 + "; " + D23,
     block(5363, 5364, "  - The §C7a 2026 central value, at 300 m with the model's 10 µs dwell"),
     "  - The §C7a 2026 central value digitizes the 0–300 m search and keeps the analog front end on for the whole "
     "12.67 µs dwell, round trips included (Eq. (96) with $T_{\\rm dwell}$ from Eq. (107)): "
     "$E_{\\rm rx}=4\\times(12{,}265\\times37.3\\ {\\rm pJ}+10\\ {\\rm mW}\\times12.67\\ \\mu{\\rm s})=4\\times(0.457+0.127)"
     "\\approx2.34$ µJ per point, for four receivers. In each, the first term is the samples: 12,265 per point (the "
     "≈12,300 of Eq. (109) at $R=300$ m, taken in the two 5 µs useful windows) times ≈37.3 pJ each, the §C7a figure for "
     "an 8-ENOB ADC at 50 fJ per conversion step plus the FFT. The second term is the ≈10 mW per receiver that §C7a "
     "assumes for the TIA, bias and drivers, running for the whole dwell. A sensor that searched only to 200 m would "
     "digitize 8,900 samples per receiver (subsection 2(c)) and need $4\\times(8{,}900\\times37.3\\ {\\rm pJ}+0.127\\ "
     "\\mu{\\rm J})=4\\times(0.332+0.127)\\approx1.84$ µJ.\n"
     "  - At 15 Mpts/s that is $15\\times10^{6}\\times2.34\\times10^{-6}=35.1$ W of receiver electronics, about 4.3 times "
     "a whole 520-line ToF unit ($35.1/8.2=4.3$; ≈8.2 W at 12.5 Mpts/s in the §C7a model: $3\\ {\\rm W}+12.5\\times"
     "10^{6}\\ {\\rm s^{-1}}\\times0.415\\ \\mu{\\rm J}$).",
     "E_rx = 2.337 uJ (model); 35.1 W against 8.19 W.")

# ---------------------------------------------------------------- subsection 5
edit(D5 + "; " + D1 + "; " + D23,
     line(5445, "This subsection asks what FMCW must improve, and by how much, to match"),
     "This subsection asks what FMCW must improve, and by how much, to match ToF's point rate per watt. Three "
     "improvements must land together: a cheap, low-power multichannel coherent receiver, more efficient CW lasers and "
     "amplifiers, and a lower optical energy per point. With all three, a 15 Mpts/s sensor whose transmitter stays on "
     "through the round trips, as in the §C7a model, draws ≈14 W with 15 mW channels, just inside the 15 W target "
     "(below); with 30 mW channels it draws 16 W unless the transmitter is gated, which brings it to 12 W. Without the "
     "efficient laser, or without the lower energy per point, it stays near 23.5 W; without the low-power receiver it "
     "stays near 48 W. A receiver at 0.30 µJ per point, 8× better than today's but 3× short of the goal, gives 17 W. "
     "Even at parity FMCW spends 1.8× the electrical energy per point of the 2026 SPAD ToF reference, which needs only "
     "9.2 W at 15 Mpts/s.",
     "Headline numbers of the ungated parity table and the ToF reference.")
edit(D5 + "; " + D1 + "; " + D23,
     block(5447, 5451, "**The target.** Parity (§C7a) means"),
     "**The target.** Parity, in this report, means ≥15 Mpts/s in ≤15 W at 200 m and 10% (§C7a subsection 5 summarizes "
     "the conditions derived here). The 2026 SPAD ToF reference of §C7a, at 0.415 µJ of electrical energy per point, "
     "meets it with room to spare: $3\\ {\\rm W}+15\\times10^{6}\\ {\\rm s^{-1}}\\times0.415\\ \\mu{\\rm J}=9.2$ W. Sensor "
     "power is overhead plus point rate times electrical energy per point:\n"
     "$$P=P_{\\rm oh}+\\dot N\\left(\\frac{E_{\\rm pt}}{\\eta_{\\rm wp}}\\,\\frac{T_{\\rm dwell}}{T_{\\rm int}}+E_{\\rm rx}"
     "\\right), \\tag{122}$$\n"
     "where $P$ is the sensor's electrical power and $P_{\\rm oh}$ the fixed overhead that does not scale with point "
     "rate. $\\dot N$ is the point rate, $E_{\\rm pt}$ the optical energy per point and $\\eta_{\\rm wp}$ the laser and "
     "amplifier wall-plug efficiency (light out per electrical power in). $T_{\\rm dwell}/T_{\\rm int}=1+2\\tau P_{\\rm ch}"
     "/E_{\\rm pt}$ (Eq. (107)) is the factor by which an ungated CW transmitter emits more than the useful energy: "
     "$12.67/10=1.27$ at the §C7a dwell, and 1 for a transmitter switched off during the last $\\tau$ of each ramp. The "
     "first term in the bracket is therefore the laser's electrical energy per point. $E_{\\rm rx}$ is the receiver's "
     "electrical energy per point (samples, TIA and bias over the whole dwell; subsection 3). With $P_{\\rm oh}=3$ W, "
     "parity needs\n"
     "$$\\frac{E_{\\rm pt}}{\\eta_{\\rm wp}}\\,\\frac{T_{\\rm dwell}}{T_{\\rm int}}+E_{\\rm rx}\\le\\frac{15-3\\ {\\rm W}}"
     "{15\\times10^{6}\\ {\\rm s^{-1}}}=0.8\\ \\mu{\\rm J}. \\tag{123}$$\n"
     "In words: after the overhead, each point may cost at most 0.8 µJ of electricity, for its light and its receiver "
     "together, i.e. $0.8/0.415=1.9$ times what the ToF reference spends per point. Eq. (122) is Eq. (118) of "
     "subsection 2(h) with its useful and dead-time light combined in the factor $T_{\\rm dwell}/T_{\\rm int}$, the "
     "per-channel receiver terms folded into $E_{\\rm rx}$ (Eq. (96)) and no coherent loss ($E'=E_{\\rm pt}$), which "
     "holds to within 1 dB for a laser of ≲27 kHz at 200 m (≲55 kHz keeps the loss within 3 dB at 300 m; Eq. (115) and "
     "its table). Subsection 2(h) evaluated Eq. (118) at 10 Mpts/s and 300 m, whereas this subsection evaluates "
     "Eq. (122) at 15 Mpts/s and 200 m, so the ≈68 W there and the ≈76.5 W below are different cases.",
     "Single parity definition; Eqs. (122)-(123) on the ungated basis (tags kept); ToF reference 9.2 W; linewidth "
     "condition from Eq. (115).")
edit(D1,
     "and the 2026 central case at 15 Mpts/s rises from ≈67 W to ≈82–104 W, or to ≈170 W. For example, at "
     "$\\eta=0.112$ the optical energy is $0.303\\ \\mu{\\rm J}\\times0.25/0.112=0.68$ µJ, and Eq. (122) gives "
     "$3+15\\times(0.68/0.15+2.23)=104$ W.",
     "and the 2026 central case at 15 Mpts/s rises from ≈76.5 W to ≈95–124 W, or to ≈207 W. For example, at "
     "$\\eta=0.112$ the optical energy is $0.303\\ \\mu{\\rm J}\\times0.25/0.112=0.68$ µJ, or 0.86 µJ as emitted "
     "($\\times1.267$), and Eq. (122) gives $3+15\\times(0.86/0.15+2.34)=124$ W.",
     "Measured-efficiency cases on the ungated basis: 95.2 / 123.9 / 206.6 W.")
edit("round1_skipped [08_C7b] report #29 (2032 row); round1_skipped [08_C7b] report #6; " + D5 + "; " + D1 + "; " + D23,
     block(5457, 5484, "The table evaluates Eq. (122) for the central, optimistic and parity cases."),
     "The table evaluates Eq. (122) for the 2026 SPAD ToF reference and for the central, optimistic and parity FMCW "
     "cases. Every FMCW row is ungated at the §C7a dwell, 10 µs of integration plus the 2.67 µs of round trips at "
     "200 m (Eq. (107)): each channel carries $E_{\\rm pt}/10\\ \\mu{\\rm s}$ (30 mW at 0.303 µJ, 15 mW at 0.15 µJ), "
     "emits 1.267 times $E_{\\rm pt}$, and 15 Mpts/s needs 190 channels.\n"
     "\n"
     "| Case | $E_{\\rm pt}$ | Emitted per point | $\\eta_{\\rm wp}$ | Laser electrical | $E_{\\rm rx}$ | Total per point "
     "| Total ÷ 0.415 µJ (2026 ToF) | $P$ at 15 Mpts/s |\n"
     "|---|---|---|---|---|---|---|---|---|\n"
     "| 2026 SPAD ToF reference (§C7a) | 0.0717 µJ | 0.0717 µJ (pulsed) | 20% | 0.358 µJ | 0.057 µJ | 0.415 µJ | 1 | "
     "$3+15\\times0.415=9.2$ W |\n"
     "| 2026 FMCW central (§C7a) | 0.303 µJ | 0.384 µJ | 15% | 2.563 µJ | 2.337 µJ | 4.900 µJ | 11.8 | "
     "$3+15\\times4.900=76.5$ W |\n"
     "| Better steering only (no other change) | 0.303 µJ | 0.384 µJ | 15% | 2.563 µJ | 2.337 µJ | 4.900 µJ | 11.8 | "
     "76.5 W |\n"
     "| 2032 optimistic (§C7a) | 0.190 µJ | 0.240 µJ | 22% | 1.092 µJ | 0.646 µJ | 1.738 µJ | 4.2 | 29.1 W |\n"
     "| All three win conditions | 0.150 µJ | 0.190 µJ | 30% | 0.633 µJ | 0.100 µJ | 0.733 µJ | 1.8 | "
     "**14.0 W (parity)** |\n"
     "| Two of three: $\\eta_{\\rm wp}$ stays at 15% | 0.150 µJ | 0.190 µJ | 15% | 1.267 µJ | 0.100 µJ | 1.367 µJ | 3.3 | "
     "23.5 W |\n"
     "| Receiver only partly improved: $E_{\\rm rx}$ at 0.30 µJ | 0.150 µJ | 0.190 µJ | 30% | 0.633 µJ | 0.300 µJ | "
     "0.933 µJ | 2.2 | 17.0 W |\n"
     "| Two of three: $E_{\\rm rx}$ stays at today's 2.337 µJ | 0.150 µJ | 0.190 µJ | 30% | 0.633 µJ | 2.337 µJ | "
     "2.970 µJ | 7.2 | 47.6 W |\n"
     "| Two of three: $E_{\\rm pt}$ stays at 0.303 µJ | 0.303 µJ | 0.384 µJ | 30% | 1.281 µJ | 0.100 µJ | 1.381 µJ | 3.3 | "
     "23.7 W |\n"
     "\n"
     "*How the table is computed* [E], row by row from Eq. (122) with $P_{\\rm oh}=3$ W and $\\dot N=15\\times10^{6}$ "
     "s⁻¹:\n"
     "- *Worked row* (\"all three\"): at 15 mW per channel the integration takes $T_{\\rm int}=0.15\\ \\mu{\\rm J}/0.015\\ "
     "{\\rm W}=10$ µs and the dwell $T_{\\rm dwell}=10+2.67=12.67$ µs, so the channel emits $0.150\\times12.67/10=0.190$ µJ "
     "per point. The laser term is $0.190/0.30=0.633$ µJ; adding 0.100 µJ gives 0.733 µJ; $3\\ {\\rm W}+15\\times10^{6}"
     "\\times0.733\\times10^{-6}\\ {\\rm J}=3+11.0=14.0$ W.\n"
     "- *2026 central:* $0.3034\\times12.67/10=0.3844$ µJ emitted, $0.3844/0.15=2.563$ µJ for the laser and "
     "$E_{\\rm rx}=2.337$ µJ (subsection 3), so $2.563+2.337=4.900$ µJ.\n"
     "- *2032 optimistic,* with the §C7a 2032 inputs (0.190 µJ, 22%, 10.07 pJ per sample, 3 mW of analog power per "
     "receiver): $0.1897\\times12.67/10=0.2403$ µJ emitted, $0.2403/0.22=1.092$ µJ for the laser, and "
     "$E_{\\rm rx}=4\\times(12{,}265\\times10.07\\ {\\rm pJ}+3\\ {\\rm mW}\\times12.67\\ \\mu{\\rm s})=4\\times(0.1235+0.0380)"
     "=0.646$ µJ. Against §C7a's 2032 ToF (0.280 µJ per point) its ratio is $1.738/0.280=6.2$ rather than "
     "4.2.\n"
     "- *ToF reference:* the §C7a central budget, 71.67 nJ of light (the 72 nJ of subsection 1), $71.67/0.20=358$ nJ "
     "for the laser and 57 nJ for the SPAD-SoC (§C7a(c)). A pulsed laser emits nothing while it waits for the echo.\n"
     "- *Ratio column:* each total divided by the ToF reference's 0.415 µJ, e.g. $0.733/0.415=1.8$.\n"
     "\n"
     "**Brighter channels need a gated transmitter** [E]. More power per channel at the same 0.15 µJ shortens the dwell "
     "and cuts the channel count, but an ungated transmitter then wastes a larger share of its light (Eq. (107)):\n"
     "- **At 30 mW per channel:** $T_{\\rm int}=0.15\\ \\mu{\\rm J}/0.03\\ {\\rm W}=5$ µs and $T_{\\rm dwell}=7.67$ µs, so "
     "15 Mpts/s needs only $15\\times10^{6}\\times7.67\\times10^{-6}=115$ channels.\n"
     "  - Ungated, each point emits $0.15\\times7.67/5=0.230$ µJ, and the total is $0.230/0.30+0.10=0.867$ µJ, i.e. "
     "$3+15\\times0.867=16.0$ W, above the target.\n"
     "  - Switched off during the last $\\tau$ of each ramp (subsection 2(i), item 2), the transmitter emits only "
     "$E_{\\rm pt}$: $0.15/0.30+0.10=0.60$ µJ, i.e. $3+15\\times0.60=12.0$ W, at any power per channel.\n"
     "- **The ungated ceiling:** Eq. (123) with $\\eta_{\\rm wp}=0.30$ and $E_{\\rm rx}=0.10$ µJ allows "
     "$T_{\\rm dwell}/T_{\\rm int}\\le(0.8-0.10)\\times0.30/0.15=1.40$, i.e. $2\\tau P_{\\rm ch}/E_{\\rm pt}\\le0.40$, so "
     "$P_{\\rm ch}\\le0.40\\times0.15\\ \\mu{\\rm J}/2.67\\ \\mu{\\rm s}=22.5$ mW. Then $T_{\\rm int}=0.15\\ \\mu{\\rm J}"
     "/22.5\\ {\\rm mW}=6.67$ µs, and 15 Mpts/s needs $15\\times10^{6}\\times(6.67+2.67)\\times10^{-6}=140$ channels.\n"
     "- Parity therefore also forces a choice between many dim channels (140–190 at 15–22.5 mW, ungated) and fewer "
     "bright ones behind a transmitter switched off during the last $\\tau$ of each ramp (115 at 30 mW).\n"
     "\n"
     "**Do the three conditions still reach parity?** Yes, but narrowly [E].\n"
     "- Ungated, as in the §C7a model, the \"all three\" case draws 14.0 W at 15 Mpts/s, 1 W inside the target, and "
     "only while each channel carries ≤22.5 mW.\n"
     "- The receiver condition is the tightest: with the other two met, Eq. (123) leaves $0.8-0.633=0.17$ µJ per point "
     "for the receiver, 14× below today's 2.34 µJ.\n"
     "- Parity in this sense is not equality with ToF. The parity case still spends $0.733/0.415=1.8$ times the "
     "electrical energy per point of the 2026 SPAD ToF reference, which delivers the same 15 Mpts/s in 9.2 W. Matching "
     "that reference point for point would need, even with a gated transmitter, $\\eta_{\\rm wp}=0.30$ and a 0.10 µJ "
     "receiver, an optical energy of $(0.415-0.10)\\times0.30=0.095$ µJ per point. By Eq. (97) that is a receive "
     "efficiency near $0.25\\times0.303/0.095=0.80$, far above the 0.5 that the parity case already assumes.\n"
     "\n"
     "**The per-channel budget at parity** follows from these numbers:\n"
     "- 140–190 channels (560–760 receivers) at ≈15–22.5 mW of optical power each with an ungated transmitter, or "
     "115 channels (460 receivers) at 30 mW with a gated one;\n"
     "- ≈8–13 mW of receive power per channel, i.e. ≈2–3 mW for each of its four receivers, including ≈1 GS/s ADCs and "
     "FFT. This comes from dividing the receiver power $E_{\\rm rx}\\dot N=0.10\\ \\mu{\\rm J}\\times15\\times10^{6}\\ "
     "{\\rm s^{-1}}=1.5$ W by the channel count $N_{\\rm ch}$: 7.9, 10.7 or 13.0 mW for 190, 140 or 115 channels, and "
     "2.0, 2.7 or 3.3 mW per receiver. Today's §C7a receiver draws ≈46 mW ($2.337\\ \\mu{\\rm J}/12.67\\ \\mu{\\rm s}/4$), "
     "14–23× more.",
     "Parity table recomputed on the ungated basis with the ToF reference row and ratio column; 2032 row 1.092 + "
     "0.646 = 1.738 uJ; brighter channels and gating; plain statement; per-channel budget.")

# ---------------------------------------------------------------- subsections 6 and 7
edit("round1_skipped [08_C7b] report #6 (channel count)",
     "with ≥150–256 channels of four LO-matched receivers each, 600–1,000 receivers in all. Each receiver runs at "
     "≈2–3 mW including ADC and FFT (subsection 5), for a few cents of silicon.",
     "with 115–190 channels of four LO-matched receivers each, 460–760 receivers in all (140–190 channels with an "
     "ungated transmitter, 115 with a gated one; subsection 5). Each receiver runs at ≈2–3 mW including ADC and FFT "
     "(subsection 5), for a few cents of silicon.",
     "One channel requirement, from subsection 5.")
edit("round1_skipped [08_C7b] report #6 (signpost)",
     "   - Signpost: a published chip with ≥256 receivers at ≤5 mW each. §C10.7's looser signpost, ≥256 channels within "
     "≈10 W, marks the first step.",
     "   - Signpost: a published chip with ≥256 receivers (64 channels) at ≤5 mW each, a third to a half of the parity "
     "count ($64/190=0.34$ to $64/115=0.56$) at about twice the parity power per receiver (5 mW against 2–3 mW). "
     "§C10.7's signpost, ≥256 "
     "channels within ≈10 W (≈10 mW per receiver if each channel has four: $10\\ {\\rm W}/1{,}024$), asks for more "
     "channels at a higher power per receiver.",
     "State both signposts in the same units as the parity requirement.")
edit("round1_skipped [08_C7b] report #6 (item 2); " + D1,
     "for SOAs or lasers delivering $P_{\\rm opt}=E_{\\rm pt}\\dot N\\approx2$–4 W of light across ≥100 channels on SiN "
     "or III-V.",
     "for SOAs or lasers delivering ≈2.3–2.9 W of light across 115–190 channels on SiN or III-V: at the parity point, "
     "$E_{\\rm pt}\\dot N=0.15\\ \\mu{\\rm J}\\times15\\times10^{6}\\ {\\rm s^{-1}}=2.25$ W of useful light, and "
     "$190\\times15\\ {\\rm mW}=2.85$ W as emitted by an ungated transmitter.",
     "Light at the parity point, useful and ungated.")
edit("round1_skipped [08_C7b] report #6 (subsection 7 row)",
     "| A published coherent receiver chip with ≥256 simultaneous receivers including ADC and FFT at ≤5 mW per receiver |",
     "| A published coherent receiver chip with ≥256 simultaneous receivers (64 channels) including ADC and FFT at ≤5 mW "
     "per receiver |",
     "Receivers and channels named together.")
edit(D5,
     "| FMCW parity on point rate per watt (as in §C7a) |",
     "| FMCW parity on point rate per watt (≥15 Mpts/s in ≤15 W at 200 m and 10%, subsection 5) |",
     "Point to the single parity definition.")

# ---------------------------------------------------------------- skipped: decisions and cross-section quotes
SKIPPED += [
    {"finding": D5 + " (target against the ToF reference)", "kind": "needs_decision",
     "location": "§C7b subsection 5, '**The target.** Parity, in this report, means ≥15 Mpts/s in ≤15 W at 200 m and "
                 "10%'",
     "detail": "The definition is kept as decided. With the ToF reference at 0.415 µJ per point (9.2 W at 15 Mpts/s), "
               "the 15 W target allows FMCW 0.8/0.415 = 1.9× ToF's electrical energy per point after the overhead "
               "(it was 0.8/0.536 = 1.5×). The edits say so plainly. If parity should instead mean equality with the "
               "ToF model, Eq. (123)'s budget becomes 0.415 µJ per point: the three conditions do not reach it (0.733 "
               "µJ ungated at 15 mW, 0.60 µJ gated), and matching it would need, with gating, eta_wp 0.30 and a 0.10 "
               "µJ receiver, E_pt ≈ 0.095 µJ (receive efficiency ≈0.8). Author to decide whether to keep 15 W."},
    {"finding": D5 + " (probability)", "kind": "needs_decision",
     "location": "§C7b subsection 7 table, '| FMCW parity on point rate per watt (…) | 2032 | ≈3–7% |'",
     "detail": "The ≈3–7% (also in §C7a subsection 6) was judged when the parity case had 3 W of margin (12 W). On the "
               "ungated basis it has 1 W (14.0 W) and holds only with ≤22.5 mW channels or a gated transmitter. The "
               "probability is the author's judgement and is left unchanged; revisit if wanted. If §C7a subsection 6 "
               "loses its probability table when it becomes a pointer (decision 5), the subsection 7 heading "
               "'(my judgement; the §C7a table stands)' and 'They complement the §C7a probability table and do not "
               "replace it' need the matching change."},
    {"finding": "cross-section quote of §C7b subsection 5 (parity conditions)", "kind": "cross_section",
     "location": "§0 executive summary, 'Better beam steering would not change this (§C7b).' bullet",
     "detail": "Old: 'Parity would need three things together: a coherent receiver chip with ≥150 channels of four "
               "receivers each, at ≈2–3 mW per receiver, a CW light source with ≥30% wall-plug efficiency at 105 °C, "
               "and ≈0.15 µJ of optical energy per point.' New: 'Parity (≥15 Mpts/s in ≤15 W at 200 m and 10%, §C7b "
               "subsection 5) would need three things together: a coherent receiver chip with 115–190 channels of four "
               "receivers each, at ≈2–3 mW per receiver, a CW light source with ≥30% wall-plug efficiency at 105 °C, "
               "and ≈0.15 µJ of optical energy per point. Even then an ungated sensor draws ≈14 W at 15 Mpts/s, 1.8× "
               "the electrical energy per point of 2026 SPAD ToF (9.2 W).'"},
    {"finding": "cross-section quote of the §C7b ratio", "kind": "cross_section",
     "location": "§C0 Main results, '**Equal apertures, constant gap** (10.5).'",
     "detail": "Old: 'Against the fixed 25 mm ToF lens of §C7a the factor is 3.1 at 200 m (10.5), the ≈3.2× used in "
               "§C7a, §C7b and §C10.' New: 'Against the fixed 25 mm ToF lens of §C7a the factor is 4.1 at 200 m (10.5), "
               "the ≈4.2× used in §C7a, §C7b and §C10.' (link_budget ratio 4.08; §C7b Eq. (104) 4.2.)"},
    {"finding": "cross-section quote of the §C7b ToF energy", "kind": "cross_section",
     "location": "§C0 subsection 10.6, '**SPAD ToF at 940 nm with a 25 mm lens** needs 96 nJ per point'",
     "detail": "Old: 'Without the 0.15 dB of clear-air loss this is the ≈93 nJ of §C7b subsection 1.' New: 'Without the "
               "0.15 dB of clear-air loss this is the ≈72 nJ of §C7b subsection 1.' (74.2 nJ x 10^(-0.015) = 71.7 nJ.)"},
    {"finding": "cross-section quote of §C7b Eq. (98)", "kind": "cross_section",
     "location": "§C0 subsection 10.3, 'Eq. (98) of §C7b, multiplied by the live fraction'",
     "detail": "Old: '$b=r_{\\rm bg}\\,\\Delta t_{\\rm bin}\\,N_{\\rm shots}\\,(1-f_{\\rm dead})=3.66\\times10^{8}\\times10^{-9}"
               "\\times10\\times0.784=2.87$.' New: '$b=r_{\\rm bg}\\,\\Delta t_{\\rm bin}\\,N_{\\rm shots}\\,(1-f_{\\rm dead})"
               "=1.83\\times10^{8}\\times10^{-9}\\times10\\times0.885=1.62$.' (as §C7b subsection 1(a))"},
    {"finding": "cross-section quote of the §C7b event count", "kind": "cross_section",
     "location": "§C5a 'What the numbers mean physically', dark-count bullet",
     "detail": "Old: '(≈5,970 in the central case of §C7b subsection 1, built from the rates of §C6(d))' New: '(≈3,370 in "
               "the central case of §C7b subsection 1, built from the rates of §C6(d))' "
               "(1.83e8 x 20.8e-6 x 0.885 = 3,370)."},
    {"finding": "cross-section quote of the §C7b ratio", "kind": "cross_section",
     "location": "§F6 '**My view.**' paragraph",
     "detail": "Old: 'at 200 m FMCW needs ≈3.2× more optical energy per point than 940 nm time-of-flight (ToF) lidar' "
               "New: 'at 200 m FMCW needs ≈4.2× more optical energy per point than 940 nm time-of-flight (ToF) lidar'"},
    {"finding": "cross-section quote of the §C7b factor split", "kind": "cross_section",
     "location": "§C7a subsection 2(a), 'FMCW therefore needs ≈3.2× more optical energy per point than ToF'",
     "detail": "Proposed, matching Eq. (104): 'FMCW therefore needs ≈4.2× more optical energy per point than ToF (0.30 "
               "µJ against 72 nJ). The ≈4.2× ratio splits into four factors:' … 'detection statistics (5.5×), 120 "
               "required photoelectrons against 21.7 counts: …' … 'efficiency (0.66×), ToF's 0.164, which includes the "
               "SPADs' dead time in bright sun, against FMCW's 0.25.' (collection 1.9× and photon energy 0.61× "
               "unchanged)."},
    {"finding": "cross-section wording, decision 1 (ungated central case)", "kind": "cross_section",
     "location": "§C4c, '**1,550 nm CW (FMCW) can emit several watts when scanned**' bullet",
     "detail": "Old: 'but an ungated transmitter, which also emits during the round trips, sends 8.6–9.6 W at 25 Mpts/s "
               "and reaches it (§C7a(b); §C7b subsection 2(i)).' New: 'but an ungated transmitter, which also emits "
               "during the round trips, sends 8.6–9.6 W at 25 Mpts/s; the §C7a central case, ungated at 30 mW per "
               "channel, sends $7.58\\ {\\rm W}\\times12.67/10=9.6$ W and exceeds it (§C7a(b); §C7b subsection 2(i)).' "
               "This matches §C7b subsection 2(i), which states that the central case exceeds the allowance."},
    {"finding": "cross-section, decision 5", "kind": "cross_section",
     "location": "§C7a subsection 6 table, parity row",
     "detail": "Old: '| FMCW matching 2026 SPAD ToF on point rate per watt (≥15 Mpts/s in ≤15 W at 200–300 m, 10%) | "
               "2032 | ≈3–7% |' New: '| FMCW matching 2026 SPAD ToF on point rate per watt (≥15 Mpts/s in ≤15 W at "
               "200 m, 10%; §C7b subsection 5) | 2032 | ≈3–7% |'. §C7a subsection 5 should quote the ungated parity "
               "case as ≈14 W at 15 mW per channel (16 W at 30 mW unless gated, 12 W gated), 140–190 channels "
               "ungated or 115 gated, ≈8–13 mW of receive power per channel."},
]

# ---------------------------------------------------------------- overlap check and output
spans = sorted((TEXT.find(e["old"]), TEXT.find(e["old"]) + len(e["old"]), e["id"]) for e in EDITS)
for (a0, a1, ai), (b0, b1, bi) in zip(spans, spans[1:]):
    assert b0 >= a1, ("overlap", ai, bi)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8") as f:
    json.dump({"block": "R2D_C7b", "edits": EDITS, "skipped": SKIPPED}, f, ensure_ascii=False, indent=1)
kinds = {}
for s in SKIPPED:
    kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
print(f"{len(EDITS)} edits, {len(SKIPPED)} skipped {kinds} -> {OUT.name}")
