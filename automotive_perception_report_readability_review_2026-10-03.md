# Readability review of the scientific sections, 2026-10-03

**Scope.** Eleven reviewers each read one block of the scientific sections of `automotive_perception_report_2026-09-27.md` (about 1 MB, ≈62% of the report) against the house style: derivations shown as equation, inputs, substitution and result; symbols and acronyms defined where used; full sentences and readable structure; arithmetic spot-checks; cross-section consistency; evidence tags and conventions. Each block report lists at most 40 findings, most severe first, with an exact quote and a proposed rewrite. They read the report at sha256 dfe616eb…/c39153b3…; line numbers in the block reports refer to that text.

**Applied on 2026-10-03** (report sha256 after the batch: 9c6d35ce…). 59 exact-substring edits from `scripts_archive/readability_2026-10-03/apply_readability_high.py`, covering the high-severity findings that were clear-cut and outside the lines being edited in parallel:

- C0.7 per-point rule
- C0.1 R_amb table
- C0.1 R_amb derivation
- C0.1 R_amb definition
- C0.10 equal apertures
- C0.10 sixteen times
- C0.10 direct rises
- C0.10 coherent rises
- C0.10 envelope
- C0.10 direct fraction
- C0.10 coherent collection
- C0.10 four looks formed
- C0.10 efficiency wording
- C4 C4 gain
- C4c InGaAs area
- C4c 905 emitters
- C4c EEL drift
- C5 bottom line
- C5 relabeled
- C5a Huawei lever
- C6 intro moving axis
- C6 per point
- C6 per shot numbers
- C6 thresholds
- C6 industry evidence
- C7a vendors publish
- C7a efficiency wording
- C7a eye safety gated
- C7a Waymo DFB
- C7a light alone
- C7b short gap
- C7b short CW waste
- C7b short eye safety
- C7b short reach
- C7b short parity
- C7b efficiency wording
- C7b dead time placement
- C7b Waymo DFB
- C7b 2(i) emission
- C7b 2(i) operating point
- C7b 2(i) reach
- C7b 2(i) reach 25
- C7b 5 parity text
- C7b 5 parity table
- C10 camera-like
- C10 ToF aperture
- C10.2 OPA watts
- C10.2 OPA 26.4
- C10.2 OPA 1590
- C10.3 headline
- C10.3 sunlight caveat
- C10.3 ToF inputs
- C10.3a channels
- C10.3b near field
- E2 lane
- E2 radar ratio
- E5 system target
- E10 MetaBEV
- E11 zero

**Applied on 2026-10-04 and 2026-10-05**, as hash-guarded batches of exact-substring edits (the lists are in `scripts_archive/readability_2026-10-03/edits/`): Round 1, the block findings (905 edits) and a cross-section pass (80); Round 2, the model harmonizations the author decided on 2026-10-05 (311); Round 3, the moves and the merged duplicate equations, with every equation renumbered (175 tags; map in `edits/round3/round3_renumber_map.txt`); Round 4, source research for the items that needed a source (seven groups, in `sources/`); Round 5, the source items that Round 2 had skipped, and the author's decisions on the needs_decision items of `round1_skipped_items.md` and `edits/round2/*.json` (`edits/round5/R5b_decisions.json`; the lines in Part B, §D8 and Appendix 1 were applied in a separate batch, `R5b_for_peer.json`). The block reports below stay as the record of the findings; their line and equation numbers refer to the text of 2026-10-03. Still open is the 905/940 nm split of §C9a (`sources/R8_C9a_inband_items.md`).

Five blocks (§C0 parts 1–9 and 10, §C4–§C4c, both halves of §C10) also have follow-up cross-checks, run after both edit batches; they add findings such as the unsourced Falcon K 30 W, the misplaced §E12 pointer for the $1/R^4$ law (it is §E11.3, Eq. (169)), the 905 vs 940 nm ToF efficiency basis in §C10.3–§C10.3b, and Analog Photonics' funding stated three ways.

## Cross-section problems still open

The block reviewers worked separately, so the same problem often appears in several reports. These are the ones that need one decision for the whole report; none of them was changed in the 2026-10-03 batch except where noted.

**1. One symbol, several meanings (or one quantity, several symbols).**
- $R_{\max}$: the unambiguous range in §C0 subsection 1 is now $R_{\rm amb}$; §E11 Eq. (167) still uses $R_{\max}$ for the half-width of a BEV grid.
- $N_s$: detected photons per range estimate, per pulse (Eq. (23)), accumulated histogram counts, and photons before detection (§C0 subsection 2); §C6 Eq. (80) now says per point.
- Energy per point: $E_{\rm tx}$ (§C0 Eq. (42)), $E_{\rm pt}$ (§C6, §F5), $E_{\rm pulse}$ (§C10.2, §E9), $E_{\rm point}$ (§E11 Eq. (169)), $E_s$ (§C10.3), $E_{\rm opt}$ (§C7a, §C7b).
- $\Omega$ is a solid angle (§C0 subsection 3, Eq. (24), §C6) and a scan rate (§C0 subsection 2, Eq. (86), Eq. (116)); $\omega$ is the mechanical rate in §C7 but the optical rate in §C10.3a.
- $\Delta f$: electrical bandwidth (Eqs. (26), (100)), scanner-induced spread (§C0 subsection 2, Eq. (86)) and beat bandwidth (§C7b).
- $\eta$ includes the polarization factor in §C10.2 and §C10.3 but excludes it in §C0 subsection 10.1 and §C10.3a Eq. (144); this also leaves the §C10.3 and §C10.3a power figures (184 W) on different bases.
- Also: $\eta_{\rm wp}$ vs $\eta_{\rm WPE}$ and $P_{\rm oh}$ vs $P_0$ (§C7b); $M$ (APD gain, $M^2$, margin, Marcum index); $S$ (sweep rate, speckle gain, lidar ratio); $\theta$ (beamwidth, emission angle, cell width) in §C10; $a$ (aim angle, deceleration) in Parts A and E; $\Delta t$ (round-trip delay, bin width); the ionization ratio $k$ is worded hole/electron in §C0 Eq. (25) and §C4, which is inverted for InP.

**2. The same relation under several equation numbers.** Stopping distance: Eq. (11) = (162) = (170) = (184), quoted as 255 m in some places and 257 m in others. Also Eq. (93) = (97); Eq. (85) = (186); Eqs. (33)–(35) = (101)–(103) = (146); Eq. (24) ≈ (67) ≈ (81)/(83); Eq. (65) = (82); Eq. (177) = (153); Eq. (178) = (150). The coherence-length condition is cited as "§C7, Eq. (185)", but Eq. (185) is in §F6.

**3. The FMCW dwell and channel model.** The dwell is defined three ways: $T_{\rm up}+T_{\rm down}$ (§C0, §C7), 10 µs without the round trip (§C7a Eq. (96)), and $E_{\rm opt}/P_{\rm ch}+2\tau$ (§C7b Eq. (107)). As a result 10 Mpts/s needs 100 channels in §C7a and 127 in §C7b, and the receiver energy computed for the 0–300 m search is applied to the 200 m case. The parity chip is sized in channels in some places and receivers in others (≥150 channels; 115–190; ≥256 receivers; §C10.7's ≥256 channels), and §C7a lists five parity conditions where §C7b lists three.

**4. Interference (§C9, §C9a).** The ghost estimate switches from "up to nine counts per foreign shot" to one count per shot, from 0.33 ns to 1 ns bins and from 1.25 to 2.5 Mpt frames; the $10^{-3}$ fraction for facing scanners has no derivation; $n$ = 10–30 interferers is never tied to today's 3–16.

**5. Shared inputs that differ between Parts A, C and E.** Pedestrian 0.5 × 1.8 m vs 0.5 × 1.7 m; braking 0.7 $g$ vs 5–6 m/s²; low-beam reach 50–80 vs 50–100 m; dark-clothing reflectance 0.1, 0.05–0.1 or 5%; fog reach "0.6–1 V" in §E4 vs 0.52–0.69 V in the §C0 model, with fog classes defined three ways and $q_{\rm K}$ in clear air 1.6 vs 1.3; solar background for the same case $1.6\times10^9$ vs $2.2\times10^9$ s⁻¹ (905 nm, 20 nm), $5.7\times10^8$ vs $7.31\times10^8$, $5.9\times10^8$ vs $6.1\times10^8$; the §C0 subsection 7 worked cases use 1,000 bins and $b=1$ where subsection 10.3 uses 2,000 bins and $b=2.87$.

**6. Product facts that disagree between sections.** Hesai ATX channels (64, 68 or 256); "2,160 channels per die"; IMX479 0.20 vs 0.16 MP; dead time 6 vs 15 ns for "the same array"; whether a Huawei 192-line teardown exists; Kim's interference fraction ($6\times10^{-6}$ vs $2.6\times10^{-5}$); Falcon K1 vs K2 ROI; HDL-64E point rate; BEVFusion-MIT at 68.5 vs 66.9 mAP and CenterPoint at 59.6 vs 56.3 mAP (different retrainings compared directly).

**7. Evidence tags.** Yole and ResearchInChina are tagged [P] or [T] instead of [MR]; Wikipedia [T] instead of [S]; several academic papers [P] instead of [I]; non-standard tags ("[T, snippet]", "[E from P]", "[P, search]"); and the untagged claims listed in each block report.

**8. Cross-reference slips.** Local "§2(a)" references in §C7a; "§A5.3"; "§E6" for IIHS night-AEB ratings that §E6 does not contain; "§C6" for the silicon-area multiplier (§C8.3); "§C10.3" for Pointcloud's DFB (§C10.4); "§C10.7" for the 8,192-element OPA (§C7, §C10.2b); "§C6(e)" for on-chip data reduction (§C5a).

**9. Structure.** §C0 subsection 9 (126 lines) and §C0 subsection 10.7 carry survey material that buries the primer's relations; §C7b items 2(h)–(i) depend on the channel model of subsection 3 but come before it; §C10.3a and §C10.3b are interleaved, with forward references; the §C5 Fastree3D history interrupts §C5's answer; the §C7b short answer runs to 33 lines; many tables lack an introducing sentence.

**10. High-severity items not applied because they need a source, a model decision or the author's judgement.** §A6 IIHS night-AEB ratings (no source); §E2 radar price "below \$100" (unclear referent; tag [MR]); §C4b ATX channel mapping; §C5 Fastree3D share arithmetic; §C9a ghost-rate model and the §C9 $10^{-3}$ figure; §E10/§E11 MetaBEV and MEFormer like-for-like comparison; §C7b dwell definition and parity sizing; §C10.3a efficiency bookkeeping; §E11 grid symbol; §E9 energy symbol; §C10.3a fraction-column bases.


## Block reports

### §A3–§A6 (thermal and headlight physics) and §E2–§E5 (camera, radar and lidar physics; benchmarks; weather; safety arithmetic)

#### Readability review: §A3–§A6 and §E2–§E5

**Coverage.** Both ranges were read in full: lines 252–534 and §E2–§E5 (lines 7417–7722, 6 lines lower after an insertion in §D7). Every line number below is the later one.

##### 1. Overall assessment

- **What reads well.** Each section opens with its question and answer. Almost every estimate shows its equation, inputs and substitution. I recomputed about 120 substitutions and found only one small arithmetic slip (line 7545).
- **Problem 1: shared inputs and symbols drift between Parts A, C and E.**
  - The pedestrian is 1.8 m tall in Part A and 1.7 m in Part E.
  - Braking deceleration is 0.7 g in §A6 and 5–6 m/s² in §E2.
  - Dark-clothing reflectance $\rho$ is 0.1, 0.05–0.1 or 5% depending on the section.
  - Lidar reach in fog is 0.6 V in §A5 and 0.6–1 V in §E4. Low-beam reach is 50–80 m in two places and 50–100 m in another.
  - $N_{\rm px}$ and $a$ each mean two different things.
  - Some pointers are broken: §E6 at line 523, "§A5.3", and "under the lines table".
- **Problem 2: some conclusions go beyond, or contradict, the numbers beside them.** Examples are the $10^{-8}$/h target (line 7716), radar lane assignment (7464), the 45:1 radar-to-lidar ratio that mixes two years (7596), the "below \$100" radar price (7629) and the high-beam behaviour explanation (493).
- **Problem 3: evidence tags and house style slip in the market and regulation passages.**
  - Yole and ResearchInChina are tagged [P] or [T] instead of [MR].
  - Many factual bullets have no tag: lines 284–285, 294–295, 306–309, 324, 327, 382, 498–499, 7646–7648, 7661–7663 and 7720–7721.
  - Some bullets are telegraphic notes or single sentences of 50–60 words: 296, 314–315, 454, 7554.
  - Three tables have no sentence introducing them: 397, 7524, 7707.

##### 2. Findings (most severe first)

1. **Line** 7716 — **Category** B/A — **Severity** high
   - **Quote:** "The headline system target of $10^{-8}$/h needs $\beta$ well below $10^{-4}$ (or a lower $p$)"
   - **Problem:** No "headline system target" is introduced anywhere, so the reader cannot tell whose target this is. The logic is also wrong. With $p=10^{-4}$/h the independent term $[(1-\beta)p]^2\approx10^{-8}$/h already equals the whole target, so no $\beta>0$ meets it; the table's $\beta=10^{-4}$ row gives $2\times10^{-8}$. A lower $p$ is required, not an alternative.
   - **Proposed rewrite:** "- Suppose the system target is $10^{-8}$/h [name its source; if it is the ISO 26262 random-hardware-failure target for ASIL D, say so and note that it was not written for perception failures]. With $p=10^{-4}$/h the independent term alone, $[(1-\beta)p]^2\approx10^{-8}$/h, already uses the whole target, so no $\beta>0$ meets it and the per-channel rate must fall as well. With $p=10^{-5}$/h, for example, the independent term drops to $10^{-10}$/h and $\beta\approx10^{-3}$ gives $10^{-3}\times10^{-5}+10^{-10}\approx1.0\times10^{-8}$/h [E]. Such a $\beta$ cannot be validated from subsystem data alone [E], because testing each channel separately says nothing about how often they fail together."

2. **Line** 523 — **Category** A — **Severity** high
   - **Quote:** "IIHS night pedestrian-AEB ratings fell from superior to advanced with high beams, and to basic with low beams (§E6)."
   - **Problem:** §E6 has no IIHS night-AEB ratings, and no other section gives these grades. The claim therefore has no source, and it does not say which vehicle, which test year, or what condition earned "superior". Line 525 ("The cited small IIHS track sample…") refers to a citation that does not exist either.
   - **Proposed rewrite:** "**Camera AEB is also headlight-limited.** In IIHS's night pedestrian-AEB tests of [vehicle(s), year], [the system] rated superior [in the reference condition] scored advanced when tested with high beams and basic with low beams [I, source]. Superior, advanced and basic are IIHS rating grades, in descending order." At line 525, write "That IIHS track sample of [n] vehicles…" and add a tag.

3. **Line** 7596 — **Category** B — **Severity** high
   - **Quote:** "That is about 45 radars for every lidar ($166/3.7\approx45$), against Yole's 3.7 M lidars for passenger-car programmes (§B1) [E]."
   - **Problem:** The 166 M radars are 2024 shipments, but §B1's 3.7 M lidars are 2025 units; §B1 gives 1.6 M for 2024. The ratio divides one year by the next and understates the same-year ratio by more than 2×.
   - **Proposed rewrite:** "That is about 100 radars for every passenger-car lidar shipped in the same year ($166/1.6\approx104$, against Yole's 1.6 M lidar units for 2024, §B1) [E]; Yole's 2025 radar volume is not given, so a 2025 ratio cannot be formed."

4. **Line** 7629 — **Category** A/B/E — **Severity** high
   - **Quote:** "The same source puts it at 1/5–1/10 of a lidar's price and expects it to fall below \$100"
   - **Problem:** "It" is the basic radar that the same sentence has just priced at \$28–56, so "fall below \$100" reads as a contradiction. The tag also breaks house style: ResearchInChina is [MR] in the tag table (line 82), and Chinese prices are written in ¥ (line 57), not RMB.
   - **Proposed rewrite:** "**China, 4D "basic imaging radar":** fell from ¥500–1,000 in early 2024 to ¥200–400 in 2025, about \$28–56 at an assumed ¥7.1 per dollar (200 ÷ 7.1 ≈ 28 and 400 ÷ 7.1 ≈ 56), as dual-chip cascades replaced quad-chip designs. The same source puts this radar at 1/5–1/10 of a lidar's price and expects [name the product the \$100 refers to] to fall below \$100 [MR, ResearchInChina; not independently corroborated]."

5. **Line** 7464 — **Category** A — **Severity** high
   - **Quote:** "The radar therefore cannot tell, from angle alone, which lane a distant object is in."
   - **Problem:** Line 7547 says an isolated scatterer can be located to about 1/14 of a beam at 20 dB, which is about 0.25 m at 200 m and enough to assign a lane. What a 1° cell cannot do is separate two objects in adjacent lanes. Also, "4D" is used before it is defined (line 7468), and at 200 m a 3.5 m cell is about one lane wide, not "wider than a lane".
   - **Proposed rewrite:** "- The best 4D radars (which also measure elevation and radial velocity; see below) reach about 0.5–1°. A cell of angular width $\Delta\theta$ is $R\,\Delta\theta$ wide at range $R$, so a 1° cell spans $200\times0.01745\approx3.5$ m at 200 m and $400\times0.01745\approx7.0$ m at 400 m, one to two lane widths. Two objects in adjacent lanes at the same range and speed therefore share one cell and cannot be separated by angle, although an isolated strong reflector can be located more finely (see "Ways past the ceiling" below)."

6. **Line** 7466 — **Category** B — **Severity** medium
   - **Quote:** "or about 28 points on a pedestrian at 200 m at 0.05°"
   - **Problem:** §A5 (lines 334 and 338) uses a 0.5 × 1.8 m pedestrian and gets about 30 points for the same case; §E2 uses 0.5 × 1.7 m (from §C10.6(a)) and gets 28. A reader comparing the two sections sees two answers to one calculation.
   - **Proposed rewrite:** Use one size throughout the report. For example: "or about 30 points on a 0.5 m × 1.8 m pedestrian at 200 m at 0.05° (the size used in §A3 and §A5) … covers $(0.5/0.175)\times(1.8/0.175)\approx2.9\times10.3\approx30$ cells". Alternatively, change lines 268 and 334–339 to 1.7 m.

7. **Line** 367 — **Category** B/A — **Severity** medium
   - **Quote:** "so the 50–100 m figures below are representative, not a universal limit."
   - **Problem:** Lines 283 and 454 give the usable low-beam reach as 50–80 m. The 50–100 m figure is where the cutoff meets the road (line 376), so the short answer blends two different quantities.
   - **Proposed rewrite:** "so the figures below (the cutoff meets the road 50–100 m ahead, depending on aim, and the usable reach for dark targets is about 50–80 m) are representative, not a universal limit."

8. **Line** 7598 — **Category** A — **Severity** medium
   - **Quote:** "Elevation-capable "4D" radars were about 40% of 2024 shipments."
   - **Problem:** 40% of 166 M is about 66 M "4D" radars in 2024, yet line 7603 gives 2.74 M 4D radars in Chinese cars in 2024. The gap comes from different definitions and from shipments versus installations, but the text never says so.
   - **Proposed rewrite:** Add: "Under Yole's broad definition (any radar capable of elevation estimation) that is about 66 M units ($0.40\times166$ M); the 2.74 M Chinese 4D installations for 2024 below use a narrower definition and count installations, not shipments, so the two must not be compared [E]."

9. **Line** 7585 — **Category** B — **Severity** medium
   - **Quote:** "braking alone takes $v^2/(2a)=36.1^2/(2\times6)\approx109$ m at 6 m/s² and $36.1^2/(2\times5)\approx130$ m at 5 m/s²"
   - **Problem:** §A6.1 (Eq. (11)) brakes at 0.7 g = 6.87 m/s², which gives about 95 m at 130 km/h; §E2 uses 5–6 m/s² and does not say why (the 5 m/s² comes from UN R157, stated only in §C10.6(g)). The symbol $a$ is also the headlamp aim angle in Eqs. (6), (7) and (12), while Eq. (11) uses $a_{\rm b}$.
   - **Proposed rewrite:** "…braking alone takes $36.1^2/(2\times6)\approx109$ m at 6 m/s² and $36.1^2/(2\times5)\approx130$ m at the 5 m/s² that UN R157 assumes (§C10.6(g)). Both are gentler than the 0.7 $g$ (6.87 m/s²) firm dry-road stop of §A6.1, Eq. (11), which would give about 95 m, because [state the reason]." Rename $a$ to $a_{\rm b}$ in Eq. (159) and in §E6's Eq. (162).

10. **Line** 464 — **Category** A — **Severity** medium
    - **Quote:** "the cutoff crosses 25 cm at $(0.65-0.25)/\tan0.25^\circ\approx92$ m [E]."
    - **Problem:** The number 0.25 means two things in one expression: a height of 0.25 m and an angle of 0.25°. No units are given, and "its 25 cm sensor" is IIHS's light meter, not the car's sensor. Line 463, "between about −0.5° and +0.4°", has no stated sign convention, while the table at line 397 counts downward aim as positive.
    - **Proposed rewrite:** "- IIHS notes that a 0.25° downward aim already drops the cutoff below its light meter, mounted 25 cm above the road, beyond 100 m. With the 0.65 m lamp height above, Eq. (7) gives a cutoff height at 100 m of $0.65\ {\rm m}-100\ {\rm m}\times\tan0.25^\circ\approx0.21$ m, and the cutoff falls to the meter's 0.25 m height at $(0.65\ {\rm m}-0.25\ {\rm m})/\tan0.25^\circ\approx92$ m [E]." Line 463: "between about 0.5° below and 0.4° above the horizontal [I]" (check IIHS's sign convention first).

11. **Line** 404 — **Category** A — **Severity** medium
    - **Quote:** "Beyond $d$, a standing pedestrian's whole body lies above the cutoff and is lit only by the glare-limited part of the beam."
    - **Problem:** Line 383 says ECE beams raise the cutoff on the kerb side "to reach farther on your own side". But Eqs. (6)–(7) and the table treat the cutoff as one flat line, and line 454 then uses that table for the reach on the driver's own side. The reader cannot tell which part of the cutoff the table describes.
    - **Proposed rewrite:** Insert after line 393: "Eqs. (6)–(7) and the table below describe the flat, oncoming-side part of the cutoff. On the kerb side the 15° rise lifts the cutoff, so for a pedestrian at the road edge the reach is set mainly by the hotspot's intensity (Eq. (8) and the photometry table) rather than by this geometry." At line 404, write "a standing pedestrian in the flat part of the pattern".

12. **Line** 454 — **Category** A/D — **Severity** medium
    - **Quote:** "Setting Eq. (11) equal to the reach $d_{\rm reach}$, i.e. $v\,t_r+v^2/(2a_{\rm b})=d_{\rm reach}$, with $t_r=1.5$ s and $a_{\rm b}=0.7g$, and solving for $v$,"
    - **Problem:** This is a 55-word sentence with a dangling participle, and it skips the step of solving the quadratic, so the reader cannot reproduce 64, 77 and 88 km/h. The bullet is four sentences long.
    - **Proposed rewrite:** "Setting Eq. (11) equal to a reach $d_{\rm reach}$ and solving the quadratic for the speed gives $v=a_{\rm b}\left[\sqrt{t_r^2+2d_{\rm reach}/a_{\rm b}}-t_r\right]$, with $t_r=1.5$ s and $a_{\rm b}=6.87$ m/s². For $d_{\rm reach}=50$ m, $v=6.87\times(\sqrt{2.25+14.56}-1.5)\approx17.9$ m/s $\approx64$ km/h; 65 m gives about 77 km/h and 80 m about 88 km/h [E]." Make this a separate bullet.

13. **Line** 475 — **Category** A — **Severity** medium
    - **Quote:** "these are associations after statistical adjustment, not a controlled estimate of ADB's effect."
    - **Problem:** §A6.2 is about gains within the low-beam limit, and the IIHS evidence concerns headlight ratings, not ADB (which line 499 says became legal in the US only in 2022). Naming ADB here confuses which feature the caveat is about.
    - **Proposed rewrite:** "these are associations after statistical adjustment, not a controlled estimate of what better low beams alone achieve."

14. **Line** 493 — **Category** A — **Severity** medium
    - **Quote:** "So the binding constraint is **behavioural and social** (drivers dip their lights to avoid dazzling others), not photometric."
    - **Problem:** The explanation in brackets contradicts the data just quoted: high beams were used only 25.4% of the time on unlit rural roads with nobody to dazzle.
    - **Proposed rewrite:** "So the binding constraint is **behavioural**, not photometric: drivers leave high beams off even with no one to dazzle (25.4% use on empty unlit rural roads), as well as dipping them for other traffic."

15. **Line** 500 — **Category** D — **Severity** medium
    - **Quote:** "It requires a 1° transition zone, against about 4° elsewhere."
    - **Problem:** "Transition zone" is never defined, here or at line 511, and "elsewhere" is vague, so the reader cannot see why 1° is the stricter rule.
    - **Proposed rewrite:** "It allows only a 1° transition zone ([definition]), against about 4° in [UN R149 / SAE J3069 / other markets], which [consequence for the beam]." At line 511, add "(transition zones, see §A6.3)".

16. **Line** 372 — **Category** A — **Severity** medium
    - **Quote:** "Lever 2 has a large photometric opportunity, meaning that a great deal of extra light could reach the road, because drivers underuse high beams."
    - **Problem:** "Lever 2" (lines 368–370, and again at line 475) means "high-beam light more of the time". §A6.3 reuses the numbers 1–3 for different items (lines 496–505), where 2 is ADB, so a reader there will take "lever 2" to mean ADB.
    - **Proposed rewrite:** Label the levers (a) better low beam, (b) more high-beam time, (c) light aimed at detected hazards. Then write "Lever (b) has a large photometric opportunity…", change line 475 to "lever (b)", and make §A6.3's numbered list a bullet list.

17. **Line** 296 — **Category** C/D — **Severity** medium
    - **Quote:** "are dual-use controlled, i.e. export-controlled because they also have military uses, when they run faster than 9 Hz (US export classification ECCN 6A003.b.4.b;"
    - **Problem:** This one bullet holds five sentences, the first about 55 words long with nested brackets. ECCN is never expanded, "releases" is jargon, and the bullet never says why export control helped keep thermal niche.
    - **Proposed rewrite:** "- **Export controls.** In the US, a thermal camera built on an uncooled microbolometer (the usual thermal sensor: an array of tiny resistors warmed by the absorbed infrared) is a controlled dual-use item, one with military as well as civil uses, if it runs faster than 9 Hz [P]. Its Export Control Classification Number (ECCN) is then 6A003.b.4.b; the bare detector array is ECCN 6A002.a.3.f at any frame rate.
      - Note 3.c to 6A003.b.4.b exempts cameras specially designed for civilian passenger vehicles under 4,500 kg gross vehicle weight, mounted solely to assist the driver and built to stop working when removed from their vehicle. These fall under ECCN 6A993.a, controlled for anti-terrorism reasons only, at any frame rate.
      - Teledyne FLIR, for example, classifies its Tura (640 × 512 pixels, up to 60 Hz) as 6A993.a with its vehicle-authentication lock and as 6A003.b.4.b without it [P].
      - An automotive thermal camera therefore needs this lock, an extra design and validation item that a visible camera does not need, to avoid the stricter control [E]."

18. **Line** 340 — **Category** A — **Severity** medium
    - **Quote:** "Thermal may offer stronger contrast between a pedestrian and a dark road, but classification is **not trivial**:"
    - **Problem:** The item is headed "Samples on target", and the section intro sets lidar's "few points" against thermal, yet no thermal pixel count is given, even though Eq. (1) already supplies one.
    - **Proposed rewrite:** Insert before this bullet: "- For comparison, the 320×240 thermal camera of §A3 (IFOV 1.31 mrad, Eq. (1)) has a pixel footprint of $100\times1.31\times10^{-3}\approx0.13$ m at 100 m. By the same area count as Eq. (4), the pedestrian covers about $0.9/0.131^2\approx52$ pixels at 100 m and $0.9/0.262^2\approx13$ at 200 m [E], and a 640×512 sensor over the same 24° field quadruples these counts. Even a low-resolution thermal camera therefore samples the pedestrian more densely than a 0.1° lidar (30 and 7 points)."

19. **Line** 331 — **Category** A — **Severity** medium
    - **Quote:** "Lidar samples a distant pedestrian with only a few points and loses range on dark clothing, while thermal does not see colour at all."
    - **Problem:** Read literally, "does not see colour at all" sounds like a weakness of thermal. The intended point (line 350) is that thermal is unaffected by clothing colour.
    - **Proposed rewrite:** "Lidar samples a distant pedestrian with only a few points and loses range on dark clothing, whereas thermal is insensitive to clothing colour, because it senses emitted heat rather than reflected light."

20. **Line** 356 — **Category** A — **Severity** medium
    - **Quote:** "At 10 µm, $x=2\pi\times2/10\approx1.3$, well below the extinction peak."
    - **Problem:** The 905 nm case gets a value ($Q_\text{ext}\approx2$) but the 10 µm case does not, and nothing links $Q_\text{ext}$ to the $\alpha$ of line 353, so the "real advantage" at line 357 is never quantified. My own Mie check gives $Q_\text{ext}\approx0.26$ (10 µm, $r=2$ µm), about 2.25 (905 nm) and about 2.5 (10 µm, $r=10$ µm); to be checked with an independent calculation.
    - **Proposed rewrite:** "At 10 µm, $x=2\pi\times2/10\approx1.3$, well below the extinction peak, and a Mie calculation for water ($m\approx1.22+0.05i$) gives $Q_\text{ext}\approx0.26$, roughly an eighth of the ≈2 at 905 nm [E]. A fog of $N_{\rm d}$ droplets per cubic metre has $\alpha=N_{\rm d}\,\pi r^2Q_\text{ext}$, so the same fine-droplet fog removes power about eight times more slowly at 10 µm. For $r=10$ µm, $x\approx6.3$ and $Q_\text{ext}\approx2.5$ at 10 µm, and the advantage disappears [E]."

21. **Line** 358 — **Category** C/B — **Severity** medium
    - **Quote:** "**A water film** on the thermal window is opaque: the absorption length at 10 µm is about 10–20 µm."
    - **Problem:** The whole derivation (about 70 words of maths) sits inside the [E: …] tag, after the definitions. Its result, about 9–18 µm (16 µm at 10 µm), does not match the 10–20 µm stated first.
    - **Proposed rewrite:** "- **A water film** on the thermal window is opaque. Liquid water's complex refractive index is $n+i\kappa$; its imaginary part, the extinction index $\kappa$, sets the intensity absorption coefficient $\alpha_{\rm w}=4\pi\kappa/\lambda$, and $1/\alpha_{\rm w}$ is the absorption length, the depth over which the intensity falls by a factor $e$. With the tabulated $\kappa\approx0.05$ at 10 µm, $1/\alpha_{\rm w}=\lambda/(4\pi\kappa)=10^{-5}\ {\rm m}/(4\pi\times0.05)\approx16$ µm, and about 9–18 µm across 9–11 µm, where $\kappa\approx0.04$–0.1 [E]. A 50 µm film therefore transmits only about $e^{-50/16}\approx4\%$."

22. **Line** 7554 — **Category** D — **Severity** medium
    - **Quote:** "That matches a 2014 16-line lidar vertically, is 2–3× coarser horizontally (0.4–0.5° steps against the VLP-16's 0.2°), and has 25–200 times fewer cells"
    - **Problem:** This is the section's key result, delivered in one 60-word sentence with four claims, two bracketed calculations, and a trailing clause about strong reflectors that is a separate point.
    - **Proposed rewrite:** "**Bottom line.** A practical imaging radar offers roughly 10–20 lines with 0.4–0.5° horizontal steps, about 3,000–6,000 angular cells, and only strong reflectors return within those cells. Vertically that matches a 2014 16-line lidar; horizontally it is 2–3× coarser (0.4–0.5° steps against the VLP-16's 0.2°). In total it has 25–200 times fewer cells than current automotive lidar: $150{,}000/6{,}000=25$ for the AT128 against the practical ceiling, and $600{,}000/3{,}000=200$ for the ATX against a Mobileye-class radar."

23. **Line** 7547 — **Category** D — **Severity** medium
    - **Quote:** "*Super-resolution* locates an isolated bright scatterer to about beamwidth ÷ $\sqrt{2\,{\rm SNR}}$, where SNR is that scatterer's signal-to-noise power ratio."
    - **Problem:** In radar usage, "super-resolution" means separating two targets inside one beam. What is described here is the precision of locating one target, so a specialist will stumble and a generalist may overrate radar.
    - **Proposed rewrite:** "*Sub-beamwidth angle estimation* (sometimes loosely called super-resolution) locates an isolated bright scatterer … It sharpens *where* a single point is, but it does not separate two scatterers inside one beam, split a dense surface into pixels, or create returns from panels that reflect the signal away."

24. **Line** 7705 — **Category** A — **Severity** medium
    - **Quote:** "that last assumption is what lets the square of a per-hour probability be read again as a per-hour figure."
    - **Problem:** Few readers will be able to parse this, yet it is the model's key assumption. What it means is that the second term counts both channels failing in the same hour, so it depends on how long a failure goes unnoticed.
    - **Proposed rewrite:** "The model assumes two identical channels and $p\ll1$. Its second term is the probability that both channels fail independently within the same hour, so it treats a failed channel as staying failed, unnoticed, for the rest of that hour; if failures are detected and the car reaches a safe state sooner, that term shrinks in proportion to the time a failure goes unnoticed."

25. **Line** 7721 — **Category** A/E — **Severity** medium
    - **Quote:** "**Cruise (GM's robotaxi subsidiary), 2023:** its system discarded correct lidar data (Cummings)."
    - **Problem:** The incident is not identified, "Cummings" has no year or title and is missing from Appendix 2, and the bullet has no tag. The Uber bullet (line 7720) also has no tag, and "design failed" is vague.
    - **Proposed rewrite:** "**Cruise (GM's robotaxi subsidiary), 2023:** in [date and one-clause description of the incident], its software discarded lidar returns that correctly showed [what] [I, Cummings (year), title]." Add the reference to Appendix 2. At line 7720, add [I] and say what the design failure was.

26. **Line** 7659 — **Category** A — **Severity** medium
    - **Quote:** "by up to 10% of the distance, the camera matches: **camera error is almost purely depth**"
    - **Problem:** It is unclear what the camera matches (the lidar's AP? in which distance band?), and no numbers support "almost purely".
    - **Proposed rewrite:** "…by up to 10% of the distance, the camera's AP rises to about the lidar's ([values or distance bands]) [I]: **camera error is almost purely depth**, and it grows with range."

27. **Line** 7683 — **Category** A — **Severity** medium
    - **Quote:** "The answers are that miles alone cannot prove a fatality rate, and redundancy helps only if channels fail independently."
    - **Problem:** This overstates the section's own result: Eq. (160) shows that 275 M failure-free miles do bound the rate. Line 7697 then says Waymo's miles do not meet RAND's premise without saying why, and gives no pointer to §E1 for the 271 M figure.
    - **Proposed rewrite:** "The answers are that road miles can bound a fatality rate only after hundreds of millions of failure-free miles on one system version, and that redundancy helps only if channels fail independently." Line 7697: "Waymo's 271 M cumulative rider-only miles (to Jun 2026, §E1) are near that number, but they were driven by successive software versions and [fatal-crash status], so they do not meet RAND's single-system, failure-free premise…"

28. **Line** 7641 — **Category** A — **Severity** low
    - **Quote:** "It weights mAP by one half and averages it with five error measures (translation, size, orientation, velocity and attribute), each converted to a 0–1 score."
    - **Problem:** "Weights by one half and averages it with" is ambiguous, and the 3-point NDS gap is the section's headline number.
    - **Proposed rewrite:** "It is $\text{NDS}=\tfrac{1}{10}\left[5\,\text{mAP}+\sum_{k=1}^{5}\left(1-\min(1,\text{mTP}_k)\right)\right]$, reported ×100: half the weight on mAP (0–1) and a tenth on each of five true-positive error measures $\text{mTP}_k$ (translation, size, orientation, velocity and attribute), each turned into a 0–1 score."

29. **Line** 7595 — **Category** E — **Severity** low
    - **Quote:** "**Scale and suppliers** [P, Yole press release, 12 Nov 2025, unless tagged]:"
    - **Problem:** The tag table (line 82) puts Yole and ResearchInChina estimates under [MR]. This line tags Yole [P], §A2 (248) and §B1 (541) tag it [T], and lines 7602 and 7629 tag ResearchInChina [T].
    - **Proposed rewrite:** "[MR, Yole press release, 12 Nov 2025, unless tagged]". Also use "[MR, ResearchInChina, Dec 2025]" at line 7602 and align lines 248 and 541.

30. **Line** 7591 — **Category** C — **Severity** low
    - **Quote:** "This sideline leaves the physics for the market: how many automotive radars ship, who makes them, which carmakers fit how many, and what they cost."
    - **Problem:** A 45-line market digression sits inside §E2 "Physics", and the §E2 intro does not mention it, so readers who navigate by headings will miss it.
    - **Proposed rewrite:** Make it its own subsection ("§E2a. Automotive radar market, deployments and prices") or move it to Part B. Add to the §E2 intro: "A sideline at the end gives radar volumes, suppliers and prices for comparison with the lidar market of Part B."

31. **Line** 7449 — **Category** D — **Severity** low
    - **Quote:** "about 35 µrad of relative orientation between the two cameras must stay stable across a flexing body (NODAR's core IP, i.e. intellectual property;"
    - **Problem:** The number comes three sentences before its derivation, a nested company aside interrupts the physics, the NODAR claim has no tag, and "That is the 0.25 px…" has an unclear antecedent.
    - **Proposed rewrite:** "- Wide baselines move the problem to calibration. A relative rotation of the two cameras shifts every disparity directly, so it eats into the same error budget as matching noise. For the 3840 px / 30° camera one pixel subtends $1/f=1/7{,}166$ rad $\approx140$ µrad (its IFOV, the instantaneous field of view of a single pixel), so the 0.25 px budget is $0.25\times140\approx35$ µrad: the cameras' relative orientation must stay stable to about 35 µrad while the body flexes. Holding it there is the core intellectual property claimed by NODAR, a wide-baseline stereo company [P]."

32. **Line** 7483 — **Category** A — **Severity** low
    - **Quote:** "consistent with the ≈110,000–120,000 lidar points per frame in the same dataset [E]."
    - **Problem:** The text does not say whether the 0.1° × 0.2° grid is the dataset's own lidar. Also, 110–120k points against 150k cells is the same order of magnitude rather than "consistent".
    - **Proposed rewrite:** "of the same order as the ≈110,000–120,000 points per frame of the dataset's lidar ([model and its angular grid]); the shortfall is presumably directions with no return, such as sky [E]."

33. **Line** 7587 — **Category** B — **Severity** low
    - **Quote:** "at 150 m a 0.1° lidar (0.1° $=1.745\times10^{-3}$ rad) puts about 26 cm per pixel on the car"
    - **Problem:** The point is about elevation, but the lidars elsewhere in this section step 0.2° vertically (lines 7483, 7486, 7533), which gives 52 cm at 150 m. "Pixel" also mixes camera and lidar terms.
    - **Proposed rewrite:** "at 150 m a lidar with 0.1–0.2° vertical steps puts a scan line every 26–52 cm on the car ($150\times1.745\times10^{-3}\approx0.26$ m; $150\times3.49\times10^{-3}\approx0.52$ m), enough to separate it from both the gantry, about 4 m higher, and the road."

34. **Line** 7462 — **Category** A — **Severity** low
    - **Quote:** "(see the tapering note under the lines table below)"
    - **Problem:** The tapering note (line 7508) comes before the lines table, not under it.
    - **Proposed rewrite:** "(see the tapering note after Eq. (156) below)"

35. **Line** 526 — **Category** A — **Severity** low
    - **Quote:** "(though lidar, like cameras, degrades in fog, §A5.3)"
    - **Problem:** There is no §A5.3; item 3 is a numbered paragraph, and elsewhere the report writes "§A3, item 6" (line 315).
    - **Proposed rewrite:** "(though lidar, like cameras, degrades in fog; §A5, item 3)"

36. **Line** 7545 — **Category** B — **Severity** low
    - **Quote:** "$(450/1.95)\times(100/1.95)\approx231\times51\approx11{,}900$"
    - **Problem:** $231\times51=11{,}781$, and the unrounded product is about 11,830.
    - **Proposed rewrite:** "$(450/1.95)\times(100/1.95)\approx231\times51\approx11{,}800$"

37. **Line** 7717 — **Category** A — **Severity** low
    - **Quote:** "Different physics lowers $\beta$, because a condition that blinds one sensor leaves the other working:"
    - **Problem:** Line 7701 lists a shared software bug and a mounting fault as common causes, and different sensing physics removes neither.
    - **Proposed rewrite:** "Different physics lowers the environmental part of $\beta$, because a condition that blinds one sensor leaves the other working: camera vs radar for weather, camera vs lidar for darkness and geometry. Shared software, fusion logic, power and mounting remain common causes that sensor diversity does not remove."

38. **Line** 428 — **Category** D/A — **Severity** low
    - **Quote:** "has $L=\rho E/\pi\approx0.08$–0.16 cd/m² ($0.05\times5/\pi\approx0.08$ and $0.1\times5/\pi\approx0.16$), which is mesopic vision."
    - **Problem:** A luminance is not "vision". Without the numerical range, neither this value nor line 429's "effectively invisible" for 0.002–0.004 cd/m² is tied to a threshold.
    - **Proposed rewrite:** "…which lies in the mesopic range (roughly 0.005–5 cd/m²), the twilight regime in which…". At line 429: "…cd/m², below the lower edge of that range and, against a road lit by your own low beam, effectively invisible."

39. **Line** 314 — **Category** E/D — **Severity** low
    - **Quote:** "Zeekr 9X (Raytron); Valeo + Teledyne FLIR ASIL-B ("leading global OEM", late 2023; ASIL-B is the second of the four ISO 26262 safety-integrity levels);"
    - **Problem:** This is a telegraphic note with nested brackets and no evidence tags; OEM is not expanded, and "second" is ambiguous. Line 315 ("Raytron, Guide, 8 µm pixels.") has the same problem.
    - **Proposed rewrite:** "- **Thermal as an AEB input rather than a display.** The Zeekr 9X uses a Raytron thermal camera as an AEB input [tag]. In late 2023 Valeo and Teledyne FLIR won a contract to supply an ASIL-B thermal camera (ASIL-B is the second-lowest of the four ISO 26262 levels) to a "leading global OEM", an unnamed carmaker [P]. Magna's fifth generation (late 2025) shrinks the camera from golf-ball to sugar-cube size [P]." Line 315: "Raytron and Guide (Wuhan Guide Infrared) offer 8 µm-pixel sensors [tag]."

40. **Line** 257 — **Category** A — **Severity** low
    - **Quote:** "Silica absorbs strongly near 9–10 µm, because the Si–O bonds of glass vibrate at those frequencies and soak up the radiation (Si–O vibrational absorption)."
    - **Problem:** The heading claims glass is opaque across 8–14 µm, but the explanation covers only 9–10 µm, and the bracket repeats the clause before it.
    - **Proposed rewrite:** "Silica-based glass absorbs throughout 8–14 µm: the Si–O stretching vibration absorbs near 9–10 µm, the Si–O–Si bending vibration near 12.5 µm, and multiphonon absorption fills the gaps, so a windshield several millimetres thick transmits essentially nothing in this band."

##### 3. Consistency flags to check elsewhere

- **$N_{\rm px}$ has two meanings.** In Eq. (2) (line 274) it is the pixels across the target; in Eq. (151) (line 7437) it is the pixels across the field, which Eq. (1) calls $N_{\rm col}$. The field of view is also written two ways: $\text{FOV}_{\rm h}$ (Eq. 1) and HFOV (Eq. 151).
- **f-number and IFOV notation.** The f-number is $N$ at line 317 but $F_\#$ in §C0 (line 1604). The pixel angle is "IFOV" in Parts A and E but $\theta_{\rm pix}$ in §C0.
- **$a$ has two meanings.** It is the aim angle in Eqs. (6), (7) and (12), and the deceleration in Eq. (159) and §E6 Eq. (162) (≈ line 7737). Eq. (11) uses $a_{\rm b}$ for the deceleration.
- **Lidar angular step.** It is $\theta$ in Eq. (4) (line 336) but $\Delta\theta$ in §E2 (line 7466).
- **Other reused symbols (each defined locally, listed for awareness only).** $n$ is cycles (269), refractive index (358), antennas in "$n$T$m$R" (7604) and miles (Eq. 160). $d$ is the cutoff distance (Eq. 6) and the disparity (Eq. 150). $D$ is a lens aperture (317) and an antenna aperture (Eq. 154). $f$ is in metres at 316 and in pixels in Eq. 150.
- **Pedestrian size.** 0.5 × 1.8 m at lines 268 and 334–339; 0.5 × 1.7 m at line 7466 and in the §C10.6(a) table (line 6653).
- **Dark-clothing reflectance.** 0.1 at line 348 (lidar), 0.05–0.1 at line 428 and about 5% at line 513 (visible). State the wavelength in each place.
- **Braking deceleration.** 0.7 g (6.87 m/s²) at lines 282, 441 and 452; 5–6 m/s² at line 7585, §C10.6(g) (line 6704) and §E6 (≈7740).
- **Lidar reach in fog and the definition of $V$.** "About 0.6× V" at line 359; "0.6–1 V" in the §E4 table (line 7673); 0.13–0.69 V in the §C0 model (lines 1713–1716, and line 1723 says §E4's figure describes the dense end). $V$ is defined three ways: line 359, line 7669, and line 1708 (2% or 5% contrast). Point §E4 to §A5 and §C0.
- **Low-beam reach.** 50–80 m at lines 283 and 454; 50–100 m at line 367 (finding 7).
- **Radar-to-lidar ratio.** Line 7596 against the §B1 table (lines 546–547: 1.6 M lidars in 2024, 3.7 M in 2025); finding 3.
- **Evidence tags.**
  - Yole is tagged [T] at lines 248 and 541 and [P] at line 7595; ResearchInChina is tagged [T] at 7602 and 7629. The tag table (line 82) says [MR].
  - The B50L regulatory limit is tagged [T] at line 381; the regulation itself is a primary source ([P]).
  - "[P, via IIHS]" at line 462 matches the tag table's [S].
  - An IIHS analysis is tagged [T] at line 517, while IIHS studies are [I] elsewhere.
- **Currency.** "RMB" at line 7629, but line 57 sets ¥ for Chinese prices, and line 245 uses ¥.
- **Metric names and scales.** "3D AP" at lines 7554, 7640 and 7651, but "AP3D" at 7674 and 7679. Scores are on 0–100 in most places but 0–1 for Argoverse (line 7661). Line 7679 says the normal-weather value is "in brackets"; the table puts it in parentheses, and the "x / y" pairs (snow / sleet) are not explained.
- **Spelling.** "Center-distance" (7645) against "centre" elsewhere; "leveling" (368, 465, 472); "programs" (308, 7407–7408) against "programmes" (533, 7596).
- **Citations.**
  - Wood et al. appears without a year at lines 283, 439 and 516, and as "Wood/Tyrrell studies" (plural) at line 488. Appendix 2 lists only Wood, Tyrrell & Carberry 2005 (≈ line 9401); confirm which study gave each figure (40%/5%, 59→94 m, 3.5×, 0 m).
  - "Cummings" (line 7721) is not in Appendix 2.
- **Pointers to add.** Line 7697 should point to §E1 for Waymo's 271 M miles (§E1 gives 271.3 M to Jun 2026, ≈ line 7394), and line 7698 to §E1 for Tesla's 1 M miles. Line 461 ("same $Z^2/h$ geometry as monocular camera depth") and §E2 Eq. (153) should point to each other. Eq. (5) and line 349 could point to §C0 Eq. (23) and its $1/R^4$ small-target result (line 1548).
- **Equation numbering.** (1)–(12) and (150)–(161) are unique and in sequence. If finding 9 changes Eq. (159), update its citation in §E6 Eq. (162).
- **To verify (outside readability).**
  - Line 326: as far as I know, LightPath's BD2 contains germanium and the germanium-free grade is BD6; name the grade.
  - Line 410: IIHS may use 5 lux for low beams and 3 lux for high beams, rather than 3 lux "for low-contrast objects"; check the IIHS protocol.
  - Line 305: 73 km/h is 45.36 mph; keep 45.3 only if it is the rule's own conversion. That line also says "under lower beams", while the speed list covers all night runs.

### §C0 subsections 1–9 (physics primer)

#### Readability review of §C0, subsections 1–9 (lines 1494–1857)

**Coverage:** the whole block was read. Cross-references past line 7341 are 6 lines lower after an insertion in §D7 (the §E4 table at 7667 is now at about 7673). The content behind the "Used in" pointers (§C3b, §C4b, §C5, §E12) was checked only for the headings, and the vendor figures (Z+F, Leica, ST, Sony) were not checked against their sources.

##### 1. Overall assessment
Each subsection opens with the question it answers and closes with what it means for the sensor, and most numbers show their substitution. I recomputed about 60 of them in memory, with no files written: Poisson tails, Albersheim, Swerling, the fog reaches, rain loss, the Cramér–Rao bound, coherent share, solid angles and photon counts. All match the stated rounding. Equations (23)–(28) are numbered in global sequence (Eqs. (1)–(188) checked). There are no \( \) or \[ \] delimiters and no versioning words, and currency uses \$.

The three main systemic problems:
- **Symbols drift between subsections.** $N_s$ has four meanings, and $R_{\max}$ means unambiguous range here but maximum detection range in subsection 10 and Part A. $\Delta f$, $\Omega$ and $\rho$ each carry two meanings, and one quantity often has several symbols.
- **Several prose conclusions disagree with the numbers next to them.** Examples: FMCW precision written as ≈1 cm where the relation gives 1.5 cm; the InGaAs excess-noise claim; "needs more" next to 88 < 130; the fog reach versus §E4; the worked cases of subsection 7 versus 10.3.
- **Subsection 9 is out of scope, and a few derivation steps are skipped elsewhere.** Subsection 9 (126 lines, five tables) has grown into a product and market survey inside a physics primer. The skipped steps are: the étendue relation, the Cramér–Rao bound to range, coherent share versus $L_c$, the APD gain optimum, and the required LO power.

##### 2. Findings (most severe first)

**1. Line 1701 — A/B — high**
- **Quote:** "A full FMCW point needs more: under the per-point rule of subsection 10.3 ($10^{-3}$ false points over a 0–300 m search"
- **Problem:** The sentence says a full point "needs more" than the single-bin ≈130, then gives ≈88 for four looks, which is less. The ≈88 is a total over both ramps and all looks (10.3 table), and the sentence does not say so.
- **Proposed rewrite:** "A full FMCW point is held to the stricter per-point rule of §C0 subsection 10.3: at most $10^{-3}$ false points over a 0–300 m search, with the echo's peak found in both chirp ramps. With one look it then needs ≈259 photoelectrons, twice the single-bin 130. Summing four independent looks brings the total, over both ramps and all looks, down to ≈88, because diversity removes most of the fading penalty."

**2. Line 1564 (also 1506, 1534, 1549, 1578) — A — high**
- **Quote:** "$N_s$: the number of signal photons in the LO's spatial mode during the chirp, and $\eta$ the overall detection efficiency"
- **Problem:** $N_s$ has four meanings:
  - detected photons per range estimate (1506);
  - detected photons per pulse (Eq. (23));
  - accumulated histogram counts (1549);
  - here, photons before detection, so that SNR $\approx\eta N_s$.

  The ToF "≈22 photons" and FMCW's $N_s$ are therefore not comparable. Subsection 7 calls the detected quantity $s$, and subsection 10 calls it $\bar n$.
- **Proposed rewrite:**
  - Subsection 2: "- $N_{\rm mode}$: the number of signal photons arriving in the LO's spatial mode during one ramp, and $\eta$ the overall detection efficiency, so that $\bar n=\eta N_{\rm mode}$ is the number of signal photoelectrons (the $\bar n$ of subsection 10)." Table row: "With a strong LO, $\text{SNR}\approx\bar n=\eta N_{\rm mode}$".
  - Subsection 1: write Eq. (23) for $N_{s,1}$ (detected signal photons per pulse) and add "$N_s=N_{\rm pulse}N_{s,1}$ accumulated over the $N_{\rm pulse}$ pulses of one estimate".
  - Subsection 7: add "($s$ is the $N_s$ of subsection 1 and the $\bar n$ of subsection 10)".

**3. Line 1516 (and 1526) — A — high**
- **Quote:** "Unambiguous range per channel | $R_{\max}=c/(2\,\text{PRF})$"
- **Problem:** $R_{\max}$ is the maximum detection range in subsection 10 ("$\mathcal{L}(R_{\max})=\mathcal{L}_{\rm det}$", line 1865; line 2128) and in Part A Eq. (5), and the 300 m search window at line 2038. Subsection 9 already calls this quantity $R_{\rm amb}$. The relation also uses PRF where the symbol list defines $\text{PRF}_{\rm ch}$, and $R$, $\Delta R$ and $\sigma_R$ are missing from the symbol list.
- **Proposed rewrite:**
  - Table row: "| Unambiguous range per channel | $R_{\rm amb}=c/(2\,\text{PRF}_{\rm ch})$ | 750 kHz ↔ 200 m; 300 kHz ↔ 500 m | §C4d |", with the derivation changed to match.
  - Add to the symbols: "- $R$ is the range (m), $\Delta R$ the two-target range resolution (m), $\sigma_R$ the rms error of one range estimate (m), and $R_{\rm amb}$ the unambiguous range (m), the farthest range whose echo returns before the next pulse leaves (subsection 9 uses the same symbol)."

**4. Line 1680 — B — medium**
- **Quote:** "whereas InGaAs/InP reaches the same excess noise at a gain of about 10"
- **Problem:** With $k=0.45$, Eq. (25) gives $F=3$ at $M\approx4.5$ and $F=4$ at $M\approx6.6$. The table itself shows $F=5.5$ at $M=10$, so the sentence understates the InGaAs penalty.
- **Proposed rewrite:** "Silicon's small $k$ keeps $F$ near 3–4 even at a gain of 100, whereas InGaAs/InP with $k=0.45$ already reaches $F=4$ at $M\approx7$ and $F=5.5$ at $M=10$ [E: solving $0.45M+0.55(2-1/M)=4$ gives $M=6.6$]."

**5. Line 1665 — A — medium**
- **Quote:** "$k$ is the ratio of the hole to the electron ionization coefficient, i.e. how readily holes, rather than electrons, trigger further ionization"
- **Problem:** This is right for silicon, where electrons start the avalanche. In InGaAs/InP, holes start it in InP and ionize more readily, so $k\approx0.4$–0.5 is the electron-to-hole ratio. Eq. (25) is introduced "for electron-initiated multiplication" yet applied to InP. §C4 (line 3273) has the same wording.
- **Proposed rewrite:** "$k$ is the ionization coefficient of the carrier that does not start the avalanche divided by that of the carrier that does: holes over electrons ($\beta/\alpha$) in silicon, where electrons start it, and electrons over holes ($\alpha/\beta$) in InGaAs/InP, where holes start it in the InP layer. Eq. (25) holds in both cases with this $k$; a small $k$ means an avalanche driven by one carrier type, which is quieter." Also replace "for electron-initiated multiplication" with "for multiplication started by the more strongly ionizing carrier".

**6. Line 1570 (derivation 1583) — B/A — medium**
- **Quote:** "15 cm resolution at 20 dB SNR → ≈1 cm"
- **Problem:** The relation in the same row gives $15/\sqrt{100}=1.5$ cm, and ≈1 cm appears only as a compromise in the derivation. The step from the frequency bound to range is skipped, and "Cramér–Rao bound" is not explained.
- **Proposed rewrite:**
  - Table cell: "15 cm resolution at 20 dB SNR → 1.5 cm by this relation; 0.6–0.8 cm at the Cramér–Rao bound".
  - Derivation: "The Cramér–Rao bound (the smallest rms error any unbiased estimator can reach) for a tone's frequency is $\sigma_f=a/(T\sqrt{\rm SNR})$, with $a=\sqrt6/(2\pi)\approx0.39$ (complex I/Q samples) or $\sqrt{12}/(2\pi)\approx0.55$ (real samples). A beat error $\sigma_f$ is a range error $\sigma_R=c\,\sigma_f/(2\kappa)=a\,\Delta R/\sqrt{\rm SNR}$, i.e. $0.39\times1.5=0.59$ cm to $0.55\times1.5=0.83$ cm."

**7. Line 1578 — A — medium**
- **Quote:** "raise the practical need to ≈90 (four looks) to ≈260 (one look) per point (subsection 10.3)"
- **Problem:** The row's $N_s$ counts photons before detection during one ramp. The ≈90 and ≈260 are photoelectrons summed over both ramps and all looks, and no unit is given.
- **Proposed rewrite:** "A few signal photoelectrons per ramp suffice in principle. Speckle fading, the search over thousands of bins and a peak needed in both chirp ramps raise the practical need to ≈90 photoelectrons per point, summed over both ramps, with four looks, and to ≈260 with one look (§C0 subsection 10.3)".

**8. Line 1687 (to 1690; also 1686) — B — medium**
- **Quote:** "Worked cases for 1,000 bins and at most $10^{-3}$ false points per measurement, i.e. $10^{-6}$ per bin [E]:"
- **Problem:** Line 2000 says "Subsection 7 uses the same per-point budget", but 10.3 differs:
  - it uses 2,000 bins of 1 ns ($p=5\times10^{-7}$) and the bright-sun $b=2.87$;
  - here the bin width is unstated and the daylight $b=1$ has no source;
  - the per-bin probability is called $P_{FA}$ here but $p$ in 10.3.

  With 2,000 bins the first two thresholds stay at 10 and 3, but the third case becomes 13 counts ($s\approx17$). Line 1686 also says $P_D$ "depends on how many range cells are tested". In fact only the threshold does.
- **Proposed rewrite:** "Worked cases for $N_{\rm bins}=1{,}000$ bins (2 ns each over 0–300 m) and at most $P_{FA,{\rm pt}}=10^{-3}$ false points per point, i.e. $p=10^{-6}$ per bin [E]. The daylight $b=1$ is illustrative; §C0 subsection 10.3 uses 2,000 bins of 1 ns and the bright-sun $b=2.87$ of the §C7a model, which raises the daylight requirement from ≈13 to ≈17 counts:" Use $p$ and $P_{FA,{\rm pt}}$ throughout. At 1686 write: "and the threshold needed for a given false-point rate depends on how many range cells are tested."

**9. Line 1723 — B — medium**
- **Quote:** so the "≈0.6–1 V" of §E4 describes the dense end.
- **Problem:** The table gives 0.52 V at 50 m visibility and 0.69 V at 20 m. With $q_{\rm K}=0$ the reach is $R=200\ {\rm m}\times e^{-\alpha R}$, so 0.6 V needs $V\approx32$ m and 1 V needs $V\approx4$ m. The next sentence (44 words) also packs two ideas.
- **Proposed rewrite:** "**Reach relative to visibility rises as fog thickens:** about 0.5–0.7 V for visibilities of 20–50 m in this model. §E4's '≈0.6–1 V' therefore applies only below about 30 m visibility; reach equals V only near 4 m visibility, where $\alpha R=3.912$ [E]. The ratio rises because at a shorter reach the $1/R^2$ spreading loss is smaller, so the lidar can afford a larger fog optical depth $\alpha R$. Below 500 m visibility, where $\alpha=3.912/V$, reach divided by visibility is that optical depth divided by 3.912."

**10. Line 1709 (table 1711–1713) — A/E — medium**
- **Quote:** "Fog therefore attenuates 905 and 1,550 nm about equally [T, free-space-optics literature]"
- **Problem:** This holds only below 500 m visibility. The 1 km row ($q_{\rm K}=0.5$) is computed at 905 nm, which is stated only in the derivation, and is 2.33 /km at 1,550 nm (24% lower). [T] does not fit peer-reviewed work.
- **Proposed rewrite:** "Dense fog (visibility below 500 m, where $q_{\rm K}=0$) therefore attenuates 905 and 1,550 nm about equally [S, free-space-optics literature], consistent with the <10% difference measured by Duthon et al. (§C4c). In light fog the model still favours 1,550 nm slightly: at 1 km visibility $\alpha=3.05$ /km at 905 nm against 2.33 /km at 1,550 nm." Change the table header to "$\alpha$ at 905 nm".

**11. Line 1575 (derivation 1588) — A — medium**
- **Quote:** "100 kHz: $L_c\approx950$ m, yet only 28% of the beat stays coherent at 300 m (43% at 200 m)"
- **Problem:** The "yet" raises a puzzle the reader cannot resolve here, because the link between the two relations is never stated.
- **Proposed rewrite:**
  - Table cell: "100 kHz: $L_c\approx950$ m, but $\eta_{\rm coh}=e^{-4R/L_c}$ is only 28% at 300 m (43% at 200 m)".
  - Add to the derivation: "The two relations are linked by $\eta_{\rm coh}=e^{-2\pi\Delta\nu(2R/c)}=e^{-4R/L_c}$, so the coherent share falls to $1/e$ already at $R=L_c/4\approx240$ m; the rule $L_c\ge2R$ keeps only $e^{-2}=14\%$ (§C7b subsection 2(e)). Here $2.0\times10^{-6}$ s and $1.33\times10^{-6}$ s are the round-trip delays $2R/c$ at 300 and 200 m."

**12. Lines 1547, 1578, 1591, 1701 — A — medium**
- **Quote:** "per point (subsection 10.3) | §C7, §C10.3a"
- **Problem:** C0's "subsection 10.3" (detection statistics) and the main-text §C10.3/§C10.3a (photon arithmetic for optical phased arrays) have near-identical labels and appear side by side here. The rest of the report writes "§C0 subsection 10.3".
- **Proposed rewrite:** Write "§C0 subsection 10.3" at 1578 and twice at 1701. At the first mention (1547), write "§C10.3a (one spatial mode versus an integrating pixel)".

**13. Lines 1635–1636 — A/C — medium**
- **Quote:** "measures each point's radial velocity from its Doppler shift, with the resolution in subsection 2."
- **Problem:** The claim "noisier and slower" compares ToF's rms precision (0.42 m/s) with FMCW's resolution (7.8 cm/s), which are different measures. The 3 cm precision is untagged and is ten times subsection 1's 0.3 cm, unexplained.
- **Proposed rewrite:**
  - FMCW bullet: "- **FMCW** measures each point's radial velocity from its Doppler shift in one look. Its resolution is $\Delta v=\lambda/(2T)=7.8$ cm/s for a 10 µs ramp (subsection 2), and its precision is finer, of order $\Delta v/\sqrt{\rm SNR}\approx0.8$ cm/s at 20 dB [E]."
  - ToF bullet: "At an assumed range precision of 3 cm [E], ten times the ideal 0.3 cm of subsection 1 to allow for amplitude walk and background, … ≈0.4 m/s from two frames, about fifty times FMCW's single-look precision".

**14. Lines 1645–1655 — A/E — medium**
- **Quote:** "The proportionality absorbs the conversion from collected power to photon rate, a factor $1/E_{\rm ph}=\lambda/(hc)$."
- **Problem:** The one missing factor is named, so Eq. (24) can be the equality of §C6 Eq. (81); as written it duplicates Eq. (83). Its $\rho$ is the scene reflectance (0.9 in §C6), not the target's 0.1 in Eq. (23). The subsection has no worked number.
- **Proposed rewrite:** "$$r_{\rm bg}=\frac{E_\odot(\lambda)\,\Delta\lambda}{E_{\rm ph}}\,\frac{\rho_{\rm scene}}{\pi}\,\Omega_{\rm pix}\,A_{\rm rx}\,\eta_{\rm opt}\,\text{PDE} \tag{24}$$" Define $\rho_{\rm scene}$ as "the reflectance of the sunlit scene in the pixel's view, not the target reflectance $\rho$ of Eq. (23)". Add: "*Example* [E, inputs of §C6]: at 905 nm, $E_\odot/E_{\rm ph}=0.75/(2.20\times10^{-19})=3.4\times10^{18}$ photons s⁻¹ m⁻² nm⁻¹. With 20 nm, $\rho_{\rm scene}=0.9$, $\Omega_{\rm pix}=1.52\times10^{-6}$ sr, $A_{\rm rx}=4.91\times10^{-4}$ m², $\eta_{\rm opt}=0.5$ and PDE 0.3: $r_{\rm bg}=3.4\times10^{18}\times20\times(0.9/\pi)\times1.52\times10^{-6}\times4.91\times10^{-4}\times0.5\times0.3\approx2.2\times10^9$ counts/s."

**15. Line 1670 — A — medium**
- **Quote:** "The useful gain therefore ends where $F$ starts to climb."
- **Problem:** $F$ climbs from $M=1$, so this marks no point. The optimum is where the multiplied shot noise reaches the amplifier noise.
- **Proposed rewrite:** "The best gain is reached roughly where the multiplied shot noise $2qI_{\rm ph}M^2F(M)\,\Delta f$ of Eq. (26) grows to match the amplifier noise. Because $F\approx kM$ at high gain, a material with large $k$ reaches that point at a much lower $M$. Substituting the $k$ of each material into Eq. (25) gives:"

**16. Line 1682 — A/D — medium**
- **Quote:** "which for Ge photodiodes takes about 0.3–1 mW of LO (§C4c)"
- **Problem:** The required LO power is set by the TIA noise and the margin wanted, not by the diode being Ge. §C4c gives:
  - parity at 28 µA of LO photocurrent (≈30 µW) with a 3 pA Hz⁻¹ᐟ² TIA;
  - 82–94% of the shot-noise limit at 0.3–1 mW;
  - parity at 5 µW in Rogers et al.

  The sentence is also 41 words long, and PIN is not expanded.
- **Proposed rewrite:** "A balanced pair of PIN photodiodes (ordinary p–i–n diodes with unity gain, whose outputs are subtracted to cancel the LO's intensity noise) becomes shot-noise-limited once the LO's shot noise exceeds the TIA's input noise. With a 3 pA Hz⁻¹ᐟ² TIA, parity needs about 30 µW of LO, and 0.3–1 mW keeps a balanced Ge pair at 82–94% of the limit even at 125 °C; an integrated low-capacitance TIA reached parity at 5 µW (§C4c)."

**17. Line 1619 — A — medium**
- **Quote:** "At a fixed f-number, a smaller pixel pitch at the same pixel angle therefore means a smaller aperture"
- **Problem:** The "therefore" skips $D\,\theta_{\rm pix}=p/F_\#$, and the numbers column says only "§C6 worked example".
- **Proposed rewrite:** "$A\,\Omega$ is conserved through passive optics. With $\theta_{\rm pix}=p/f$ and $D=f/F_\#$, a pixel fixes $D\,\theta_{\rm pix}=p/F_\#$. At a fixed f-number a smaller pitch at the same pixel angle therefore means a smaller aperture, and a smaller pixel angle at the same pitch a larger one." Numbers column: "$p/F_\#=30\ {\rm µm}/1.2=25$ µm; at 0.88 mrad, $D=25\ {\rm µm}/0.88\ {\rm mrad}=28$ mm".

**18. Line 1788 — A/B — medium**
- **Quote:** "Why can one scanner reach 365 m with millimetre noise while a ToF camera stops near 10 m?"
- **Problem:** 365 m is the Z+F's ambiguity interval. Its millimetre-level noise is specified at 50–100 m.
- **Proposed rewrite:** "Why can a phase scanner range to 365 m, with 0.3–3.7 mm noise at 50–100 m, while a ToF camera stops near 10 m?"

**19. Line 1852 — A — medium**
- **Quote:** "Lidar statistics exclude ToF cameras and sensors, including Hesai's and RoboSense's reported units and Yole's lidar figures."
- **Problem:** The "including" clause attaches to "ToF cameras and sensors", so it reads as if Hesai's and RoboSense's units are ToF cameras.
- **Proposed rewrite:** "Lidar statistics, including Hesai's and RoboSense's reported unit counts and Yole's lidar figures, exclude ToF cameras and ToF sensors."

**20. Lines 1731–1856 — C — medium**
- **Quote:** "### 9. Amplitude-modulated (phase) ranging: ToF cameras, surveying rangers and what counts as lidar"
- **Problem:** At 126 lines and five tables, this is longer than subsections 1–3 combined. It moves beyond basic relations into products, chip architectures, maker tables and counting conventions, which buries Eq. (28) and the photon-budget comparison.
- **Proposed rewrite:** Keep in C0 the principle, Eq. (28), the $f_m$ table, the three-difference photon-budget comparison and a short "why long range uses pulses". Move these blocks to §B8 or §C1, leaving a one-line pointer:
  - "One principle, three kinds of product" and its table;
  - "iToF and dToF chips" and both of its tables;
  - "Same makers";
  - "The line is blurring";
  - "What counts as lidar", including "Counting".

  Retitle the subsection "9. Amplitude-modulated (phase) ranging".

**21. Line 1799 — A — medium**
- **Quote:** "Its precision is set by pulse width and jitter rather than range, and a histogram separates multiple returns."
- **Problem:** By subsection 1, $\sigma_R\propto1/\sqrt{N_s}$ with $N_s\propto1/R^2$, so precision does depend on range. The intended contrast is that iToF's $f_m$ fixes both precision and ambiguity. "Where long range goes" is an opaque lead-in.
- **Proposed rewrite:** "**Why long-range sensing uses pulses.** Pulsed dToF (subsection 1) gates out ambient light the way a scanner's short dwell does. Its precision is set by pulse width and timing jitter, averaged over the detected photons, not by a modulation frequency that also fixes the ambiguity range; and a histogram separates multiple returns."

**22. Lines 1547–1549 — C/A — medium**
- **Quote:** "the signal-to-noise ratio is SNR $\approx N_s/\sqrt{N_b}\propto(A_{\rm rx}/R^2)/\sqrt{A_{\rm rx}}=\sqrt{A_{\rm rx}}/R^2$"
- **Problem:** This uses the background-limited SNR two bullets before $N_s/\sqrt{N_s+N_b}$ is defined. "Far less range" is not quantified, and the point that $N_b\propto\rho$ for a sunlit target (used at line 2467) is missing.
- **Proposed rewrite:** Move the "Photon-counting SNR" bullet ahead of "Scaling", and end Scaling with: "In daylight, doubling the lens diameter (4× the area) therefore buys ×$4^{1/4}=1.41$ in range instead of ×2 at night. When the sunlit target itself supplies the background, $N_b\propto\rho$ too, and range scales as $\rho^{1/4}$ rather than $\rho^{1/2}$ (§C0 subsection 10.8)."

**23. Line 1545 — A/B — medium**
- **Quote:** "of the order of the Class 1 single-pulse limit, §C4c"
- **Problem:** The 905 nm limits are 198 nJ for an isolated pulse but 79 nJ per pulse in long trains, and the example accumulates several pulses per point. The reader cannot tell whether 100 nJ is eye-safe.
- **Proposed rewrite:** "($4.6\times10^{11}$ photons; between the 905 nm Class 1 limits of 198 nJ for an isolated pulse and 79 nJ per pulse in long trains, subsection 5 and §C4c)".

**24. Line 1729 — A/E — medium**
- **Quote:** "lidar 3D detection fell from 52.3 to 29.7 AP (average precision, a 0–100 score of object-detection accuracy) while radar held 44.5 (§E4)"
- **Problem:** "Held" implies no change, but §E4 gives radar 49.9 → 44.5. There is no evidence tag.
- **Proposed rewrite:** "…lidar-only 3D detection fell from 52.3 to 29.7 AP (average precision, a 0–100 score of object-detection accuracy), while radar-only detection fell only from 49.9 to 44.5 (§E4)", plus the evidence tag used in §E4.

**25. Lines 1592–1594 (with 1667) — A — medium**
- **Quote:** "*Scanner-induced Doppler*, $\Delta f\approx\Omega D/\lambda$: the moving mirror spreads the return's optical frequency by about $\Delta f$."
- **Problem:** Three symbols clash:
  - $\Delta f$ is the electrical bandwidth in Eq. (26);
  - $\Omega$ is a solid angle in subsections 3, 5 and 9;
  - $\Delta\theta$ is the point spacing in subsection 3.

  Neither error is given a number.
- **Proposed rewrite:** "*Scanner-induced Doppler*, $\Delta f_{\rm scan}\approx\Omega D/\lambda$ (Eq. (86) of §C7): the moving mirror spreads the return's optical frequency by about $\Delta f_{\rm scan}$. A polygon sweeping 45,600°/s (796 rad/s) with a 5 mm beam gives $796\times5\times10^{-3}/(1.55\times10^{-6})=2.6$ MHz, about 26 FFT bins of a 10 µs chirp (§C7)." Also write the walk-off as $\theta_{\rm wo}=2R\Omega/c$.

**26. Line 1558 (with 1563, 1573, 1577) — A — medium**
- **Quote:** "the measured beat frequencies during the rising (up) and falling (down) segments of a triangular chirp, which last $T_{\rm up}$ and $T_{\rm down}$"
- **Problem:** $T_{\rm up}=T_{\rm down}=T$ is never stated, and $T_{\rm dwell}$ has no unit. The round-trip delay at each ramp start is silently dropped, though §C7b uses $2(T_u+\tau)$. "Segment", "ramp" and "chirp" all name the same thing.
- **Proposed rewrite:** "…during the rising (up) and falling (down) ramps of a triangular chirp; each ramp lasts $T$, so $T_{\rm up}=T_{\rm down}=T$;" and "$T_{\rm dwell}$: the time spent per point (s), $\approx2T$ when the round-trip delay is small next to $T$ (§C7b keeps it: $T_{\rm dwell}=2(T_u+\tau)$)". Use "ramp" throughout.

**27. Lines 1790–1792 — D/A — medium**
- **Quote:** "Take a scanner at 10 mW average that dwells 7.3 µs per point (the inverse of Z+F's 136,719 pts/s) with a matched field of view"
- **Problem:** The sentence runs to 51 words with nested parentheses, and $\Omega$ is used before it is defined. The value "1.17" serves as both sr and sr·s/J, and the scanner figure has no unit. Because $T_{\rm exp}$ cancels, the comparison is simpler than it looks.
- **Proposed rewrite:** "Take a scanner at 10 mW average power that dwells 7.3 µs per point, the inverse of Z+F's 136,719 pts/s: $10^{-2}\ {\rm W}\times7.3\times10^{-6}\ {\rm s}=73$ nJ per point. Its detector sees a matched 0.6 mrad full angle (twice the Z+F beam's 0.3 mrad half-angle), a solid angle $\Omega=\pi\times(0.3\times10^{-3})^2\approx2.8\times10^{-7}$ sr, where $\Omega$ is the solid angle one detector or pixel sees." Then add: "$T_{\rm exp}$ cancels, so each figure is field solid angle over laser power: $1.17\ {\rm sr}/1\ {\rm W}$ against $2.83\times10^{-7}\ {\rm sr}/0.01\ {\rm W}=2.83\times10^{-5}$ sr·s/J, a ratio of $4.1\times10^4$."

**28. Line 1496 — A/C — low**
- **Quote:** the "Used in" column of each table points to those sections
- **Problem:** Only the tables in subsections 1–3 have that column.
- **Proposed rewrite:** "Later sections apply them without re-deriving them. The "Used in" column of the tables in subsections 1–3, and § pointers in the text of subsections 4–9, show where."

**29. Line 1600 (with 1630) — C — low**
- **Quote:** "Together they explain why resolution, range and scan speed cannot all be improved at once."
- **Problem:** The subsection promises this trade-off but never states it.
- **Proposed rewrite:** Append to 1630: "Taken together: halving the point spacing on both axes quadruples the points per frame, so at a fixed point rate it quarters the frame rate or needs four times the channels; and at a fixed pitch and f-number a finer pixel angle needs a longer focal length and a larger aperture, hence larger optics and a larger sensor for the same field (§C6)."

**30. Line 1709 — A — low**
- **Quote:** "it falls from 1.6 in clear air to 0 below 500 m visibility"
- **Problem:** 10.1 (line 1912) calls 23 km visibility with $q_{\rm K}=1.3$ "clear air".
- **Proposed rewrite:** "it is 1.6 above 50 km visibility, 1.3 for 6–50 km (the 'clear air' of subsection 10.1), and falls to 0 below 500 m visibility".

**31. Line 1744 (with 1752) — A — low**
- **Quote:** "TI's ToF design guide gives $\sigma_R\propto c\sqrt{n_e+n_T^2}/(n_m f_m C_d)$ [P, TI SBAU219D]."
- **Problem:** The scaling is not tied to Eq. (28), the assumed 0.02 rad is unexplained, and TI is not expanded.
- **Proposed rewrite:** "Texas Instruments' ToF design guide gives … [P, TI SBAU219D], i.e. by Eq. (28) a phase noise $\sigma_\varphi\propto\sqrt{n_e+n_T^2}/(C_d\,n_m)$." At 1752: "…an assumed phase noise of 0.02 rad [E], a phase signal-to-noise ratio of 50."

**32. Line 1768 (with 1769, 1771) — C/A — low**
- **Quote:** "Phase ranging is the oldest optical ranging method."
- **Problem:** Optical triangulation rangefinders are older. The heading promises three kinds of product but the bullets give history, "invented it" is ambiguous, and the table has no introducing sentence.
- **Proposed rewrite:** "Phase ranging was the first electronic distance-measurement method [S]. Erik Bergstrand built the Geodimeter in 1947…" Before the table, add: "The table compares the three kinds of product that use it today: surveying rangefinders (EDMs), phase-based laser scanners and iToF cameras."

**33. Line 1777 — A — low**
- **Quote:** Leica: "200 million waves" for millimetres, lower frequencies for metres [S]
- **Problem:** The quoted phrase has no unit, so the reader cannot tell what frequency it means.
- **Proposed rewrite:** "Leica: a fine-ranging frequency its FAQ calls '200 million waves' (per second, i.e. about 200 MHz [U]) for millimetres, lower frequencies for metres [S]".

**34. Line 1659 (also 1517, 1574, 1642, 1725, 1733, 1815, 1832) — D — low**
- **Quote:** "either by a controlled avalanche (a linear APD) or by a runaway one (a Geiger-mode SPAD)"
- **Problem:** APD and SPAD are used before they are expanded. The same applies to iToF, I/Q, IEC, ITU-R, SRAM, fps, AGA and TI, and "AT128" appears without its maker.
- **Proposed rewrite:** "either by a controlled avalanche (a linear avalanche photodiode, APD) or by a runaway one (a single-photon avalanche diode, SPAD, in Geiger mode)". Likewise use "in-phase/quadrature (I/Q)", "IEC (International Electrotechnical Commission)", "ITU-R (the International Telecommunication Union's radiocommunication sector)", "histogram SRAM (static on-chip memory)", "120 frames/s" and "Hesai AT128".

**35. Lines 1569, 1572, 1820 — E — low**
- **Quote:** "the FFT bin $1/T$ maps to $c/2B$"
- **Problem:** $c/2B$, $cf_D/2\kappa$, $c/2f_m$ and $c/2f_{\rm rep}$ read literally as $(c/2)B$. Units drift: Mpts/s vs M pts/s vs points/s, fps vs frames/s, /km vs km⁻¹, photo-electron vs photoelectron.
- **Proposed rewrite:** Write $c/(2B)$, $c f_D/(2\kappa)$, $c/(2f_m)$ and $c/(2\,\text{PRF})$. Standardize on Mpts/s, frames/s, /km and photoelectron.

**36. Line 1769 (also 1642, 1674–1675, 1709, 1725) — E — low**
- **Quote:** "AGA commercialized it in 1953 [T, Wikipedia]."
- **Problem:** The evidence tags are inconsistent:
  - Wikipedia and peer-reviewed work are tagged [T], and the rain law [T/E];
  - the Class 1 limits and the $k$ values have no tag;
  - practical gain is "[U]" for silicon but "(§C4)" for InGaAs.
- **Proposed rewrite:**
  - Use "[S, Wikipedia]", "[S, free-space-optics literature]" and "[P, ITU-R P.1814; E for the 200 m losses]".
  - Add "[P, IEC 60825-1:2014; §C4c]" after the Class 1 limits.
  - Add a source tag after "≈0.02" and "≈0.4–0.5".
  - Use the same tag form for both practical-gain entries.

**37. Line 1716 (with 1721) — B — low**
- **Quote:** "| 20 m (very dense fog) | 196 /km | 85 dB | ≈14 m | 0.69 |"
- **Problem:** The ratio uses 13.7 m, so a reader dividing 14 by 20 gets 0.70. The check "$3{,}721\times10.9\approx4.0\times10^4$" is actually $4.06\times10^4$.
- **Proposed rewrite:** "| 20 m (very dense fog) | 196 /km | 85 dB | ≈13.7 m | 0.69 |" and "$3{,}721\times10.9=4.06\times10^4\approx(200\ {\rm m})^2$, within 1.5%".

**38. Line 1628 — A — low**
- **Quote:** "A bidirectional resonant mirror would then run at $f_{\rm mirror}=S/2$, i.e. 5 Hz or 640 Hz."
- **Problem:** No resonant mirror runs at 5 Hz; the AT128 uses one polygon facet per frame (§C4d).
- **Proposed rewrite:** "With 128 channels, 10 sweeps/s is one polygon facet per frame or a slow galvanometer (§C4d); with one channel, a bidirectional resonant mirror would run at $f_{\rm mirror}=S/2=640$ Hz."

**39. Line 1826 (also 1503, 1608, 1739) — D — low**
- **Quote:** "The dToF entry $c/2f_{\rm rep}$ is the same rule for pulses, with $f_{\rm rep}$ the laser's pulse repetition rate (the PRF of subsection 1)."
- **Problem:** Single quantities carry several names:
  - repetition rate: PRF and $f_{\rm rep}$;
  - parallel channels: $N_{\rm ch}$ and $N_{\rm par}$;
  - round-trip delay: $\Delta t$ and $\tau$;
  - unambiguous range: "unambiguous", "ambiguity range" and "ambiguity interval".
- **Proposed rewrite:** "The dToF entry $c/(2\,\text{PRF})$ is the same rule for pulses (subsection 1)." Use $\tau=2R/c$ in subsection 1 too, note "$N_{\rm par}$ ($=N_{\rm ch}$ when each channel draws its own line)", and call $R_{\rm amb}$ the "unambiguous range" throughout.

**40. Line 1529 (with 1544) — D — low**
- **Quote:** "**Link budget for an extended Lambertian target** (one that fills the beam, such as a road surface or a car body)."
- **Problem:** Lines 1500 and 1889 call this the "photon budget", and "Link budget" is subsection 10's title. Eq. (23) also silently assumes the field of view covers the lit spot.
- **Proposed rewrite:** "**Photon budget for an extended Lambertian target** (…)." At 1544: "Eq. (23) assumes a Lambertian target at normal incidence that fills the beam, and a receiver whose field of view covers the whole lit spot."

##### 3. Consistency flags to check elsewhere
- **$R_{\max}$:** unambiguous range at 1516, but maximum detection range in Part A Eq. (5) (line 347), §C4d Eq. (70) (line 3682), C0 lines 1865 and 2128, and the search window at 2038.
- **§E4 fog reach:** the §E4 table (line 7667, now about 7673) gives "Reach ≈ 0.6–1 V". C0's model gives 0.52 V at 50 m and 0.69 V at 20 m visibility; 1 V needs about 4 m visibility.
- **Subsection 7 versus 10.3:** line 2000 says "Subsection 7 uses the same per-point budget", but 10.3 uses 2,000 bins and $b=2.87$ (lines 2005, 2012) against 1,000 bins and $b=1$ at 1687.
- **InP $k$:** C0 line 1665 and §C4 line 3273 both define $k$ as the hole-to-electron ratio, which is inverted for InP.
- **$\Delta f$:** scan spread in C0 line 1594 and §C7 Eq. (86) (line 4495); electrical or IF bandwidth in Eq. (26) and lines 4370, 4900–4910 and 5829.
- **$\Omega$:** scan rate at 1592, §C7 line 4493 and §C7b Eq. (116); solid angle at 1610, Eq. (24), 1790–1792, §C6 Eq. (81) and 10.2 line 1939.
- **$\rho$ versus $\rho_{\rm scene}$:** C0 Eq. (24) against §C6 Eqs. (81)/(83). Eq. (24) duplicates Eq. (83) and is never referenced anywhere.
- **LO power:** C0 line 1682 ("0.3–1 mW for Ge") against §C4c line 3575 (≈30 µW at parity) and line 3592 (5 µW).
- **Rain:** C0 line 1725 says the loss "barely depends" on wavelength; the §C4c table (line 3617) says 905 nm reaches ≈2× farther at 25 mm/h.
- **$q_{\rm K}$ in clear air:** 1.6 at line 1709 against 1.3 at 10.1 line 1912.
- **Chirp parameters:** C0 uses $B=1$ GHz and $T=10$ µs (matching §C7 Eq. (85)), but §C7a and 10.3 use 5 µs ramps, ±70 m/s and $f_b=400$ MHz at 300 m. C0's dwell omits the $\tau$ that §C7b line 5138 includes. State that C0's numbers are illustrative.
- **Symbol names:** $\text{PRF}_{\rm ch}$ and $f_{\rm rep}$ (C0) against $f_p$ (§C4d Eq. (70)); $f_{\rm mirror}$ (C0) against $f$ (§C4d Eq. (69)ff.).
- **VL53L5 resolution:** "8 × 8 zones" (1832, 1835), "14 × 10 macro-pixels" (1816 and §B8 line 1389) and "4 × 4 SPADs" (1836). Say how the macro-pixels are binned into the 8 × 8 output zones.
- **Duplicate relation:** Eq. (23) restates Part A's Eq. (5) in photon form; 10.2 line 1934 cross-references Eq. (23) but not Eq. (5).
- **Reference style:** the rest of the report writes "§C0 subsection 10.3" (e.g. lines 4302 and 4614), but C0 writes a bare "subsection 10.3" next to "§C10.3a". "(§B4a, subsection 4)" at 1852 should read "§B4a subsection 4".

#### Follow-up cross-checks for this block (second pass, 2026-10-03; new findings only, against the report after both edit batches)

#### Check of §C0's "Used in" pointers to §C3b, §C4b, §C5 and §E12 (new findings only)

**What I read:**
- the current §C0 tables in subsections 1–3;
- §C3b, §C4b, §C5 and §E12 in full;
- the §E11.3 passage that holds Eq. (169).

**What I searched** across the file: every use of $c\,\tau_p/2$, $\sigma_t/\sqrt{N_s}$ and $1/R^4$, and every "§C0" back-reference. Vendor figures were not checked.

Lines in Part E moved by +6 during the review, so find each item by its quote; the line numbers below are the later ones.

##### 1. Overall assessment
Five pointers in the "Used in" column of §C0 subsections 1–3 point at these four sections. Only two of them hold up:
- **§C3b uses points per frame** as Eq. (61).
- **§E12 uses the footprint $R\theta$** in Eqs. (179) and (180).

In both, the numbers agree with §C0 (the AT128 grid; 0.35 m and 0.175 m at 200 m). The notation differs, though, and neither section refers back to §C0. In fact none of the four sections ever cites §C0.

Three pointers are wrong:
- **§C3b never uses two-target resolution.**
- **§C4b never uses the single-target precision relation.**
- **§C5 only states the 297 ps bin width** and never converts it to range.

The $1/R^4$ law for small targets is credited to §E12 in three places, but it is derived in §E11.3, Eq. (169). §C3b's Eq. (62) restates §C0 Eq. (23) without citing it, and within one equation its $N_s$ means first the photons detected, then the photons a detection needs. §C4b's $\bar n$ is the quantity §C0 calls $N_s$.

##### 2. Findings (most severe first)

**1. Line 3119–3123 (§C3b, Eq. (62)) — A — medium**
- **Quote:** "where $N_s$ is the number of signal photoelectrons a point needs to be detected"
- **Problem:** Eq. (62) re-derives §C0 Eq. (23) without citing it. §C6's Eq. (80), by contrast, says it "is §C0 Eq. (23) with $T_{\rm atm}=1$". Eq. (62) also changes symbols:
  - PDE becomes $\eta_{\rm det}$.
  - $N_s$ is introduced as "detected per point", then redefined after the ⟹ as the number a detection *needs*. §C0 subsection 10 calls that $n_{\rm req}$.
- **Proposed rewrite:** Replace the sentence that runs from "If the sensor emits average optical power $P$…" through the "where" list with:

  "This is §C0 Eq. (23) with the energy per point, $P/\dot N$ for an average optical power $P$ shared among $\dot N$ points per second, in place of the pulse energy, and clear air. A point then yields $N_s=\frac{P}{\dot N E_{\rm ph}}\frac{\rho A_{\rm rx}}{\pi R^2}\eta_{\rm opt}\,\text{PDE}$ detected photoelectrons. Setting $N_s$ equal to the number a detection needs, $n_{\rm req}$ (§C0 subsection 10), gives
  $$\dot N R^2=\frac{P\,\rho\,A_{\rm rx}\,\eta_{\rm opt}\,\text{PDE}}{\pi\,E_{\rm ph}\,n_{\rm req}} \tag{62}$$
  where $n_{\rm req}$ is the number of signal photoelectrons a point needs to be detected, … and PDE the detector's photon detection efficiency."

**2. Line 1558 (also 2492 and 3125) — A — medium**
- **Quote:** "A target smaller than the beam (debris, a tyre) intercepts a fraction of it that falls as $1/R^2$, so its return falls as $1/R^4$ (§E12)."
- **Problem:** §E12 never mentions $1/R^4$ or how the signal from a small target falls with range. Its small-debris item (point 5 of subsection 3) counts pixels and lidar points only. The derivation is in §E11.3, Eq. (169): "$R\propto E_{\rm point}^{1/4}$ (target smaller than the footprint)". The same wrong pointer appears in §C0 10.9 ("(subsection 1; §E12)") and in §C3b ("so the return falls as $1/R^4$ (§E12)").
- **Proposed rewrite:**
  - Change "(§E12)" to "(§E11.3, Eq. (169))" in all three places.
  - Optionally, so that §E12 also earns the pointer, append to its point 5: "Each such point is also weak: an object of size $s$ smaller than the beam footprint $R\theta_b$ returns about $(s/R\theta_b)^2$ of an extended target's signal, so its return falls as $1/R^4$ (§C0 subsection 1; Eq. (169))."

**3. Line 1525 (row), with §C4b line 3377 — A — medium**
- **Quote:** "Single-target precision | $\sigma_R\approx(c/2)\,\sigma_t/\sqrt{N_s}$: timing spread $\sigma_t$ (pulse, detector jitter, TDC) averaged over $N_s$ detected signal photons"
- **Problem:** §C4b never uses this relation; its only precision statement is "Ranging precision is cm-class in both". No section outside §C0 (subsections 1 and 9) applies it. §C4b does, however, show why the $\sqrt{N_s}$ gain needs care. A 3×3 macro-pixel fires only ≈8 of its 9 cells for 20 photons (Eq. (64)), so the 20 photons of §C0's example cannot all be time-stamped in one shot.
- **Proposed rewrite:**
  - Change the row's "Used in" to "subsection 9; measured precisions in §C5a".
  - After "…reduces their scatter by that factor." add: "The gain assumes every detected photon is time-stamped independently. A 3×3 SPAD macro-pixel registers at most nine photons per shot, and only ≈8 of 20 (§C4b, Eq. (64)), so $N_s=20$ must be accumulated over several shots."
  - In §C4b's Timing row write: "Ranging precision is cm-class in both, against the ideal ≈0.3 cm of $\sigma_R\approx(c/2)\sigma_t/\sqrt{N_s}$ for 100 ps and 20 photons (§C0 subsection 1)".

**4. Line 1523 — A — medium**
- **Quote:** "Two-target range resolution | $\Delta R\approx c\,\tau_p/2$ for pulse length $\tau_p$ | 5 ns → 0.75 m; 1 ns → 15 cm | §C3b"
- **Problem:** §C3b never mentions pulse length or two-target separation, and no section outside §C0 applies $c\,\tau_p/2$. The only analogue is the acoustic $c_{\rm s}\tau/2$ in §B7.1. The relation would naturally belong in §C3b's dual-return discussion.
- **Proposed rewrite:** Either set "Used in" to "—", or make the pointer true. To do that, add after §C3b's "dual-return rates (two echoes reported per laser shot, which doubles the point count without more shots)": "A second echo is reported separately only if it lies at least about $c\,\tau_p/2$ behind the first, 0.75 m for a 5 ns pulse (§C0 subsection 1)."

**5. Line 1524, with §C5 line 3891 — A — medium**
- **Quote:** "Histogram quantization | $c\,\Delta t_{\rm bin}/2$ | 297 ps bins (Adaps ADS6311) → 4.5 cm | §C5"
- **Problem:** §C5 only defines "297 ps bins" as "the width of the timing histogram's bins" and never converts it to range. The dependency runs the other way: §C0 borrows §C5's number. §C5 tags that number [P]; the §C0 row carries no tag. §C5 also has a second applicable case it never converts: the IMX479's 3 GHz equivalent-time sampling.
- **Proposed rewrite:**
  - §C0 row: "| Histogram quantization | $c\,\Delta t_{\rm bin}/2$ | 297 ps bins (Adaps ADS6311 [P]) → 4.5 cm; 3 GHz equivalent-time sampling (Sony IMX479) → 333 ps → 5.0 cm | examples from §C5 |".
  - §C5: "…and "297 ps bins" is the width of the timing histogram's bins, $c\,\Delta t_{\rm bin}/2=4.5$ cm of range per bin (§C0 subsection 1)."

**6. Line 3343–3349 (§C4b, Eq. (64)) — A — medium**
- **Quote:** "Example [E] of Eq. (64), with $\bar n=20$ detected photons in a pulse:"
- **Problem:** §C4b's $\bar n$ (photons detected per pulse per channel, after PDE) is §C0's $N_s$ of Eq. (23). Meanwhile §C0 10.1 uses $\bar n$ for photoelectrons per *point*, summed over shots. The example's 20 photons is essentially §C0's ≈22-photon worked case, but the link is not made.
- **Proposed rewrite:** In §C4b write "$\bar n_1$ the mean number of photons the channel would detect in one pulse if no cell were already fired (photons after PDE; the $N_s$ of §C0 Eq. (23))". Then: "Example [E] of Eq. (64), with $\bar n_1=20$ detected photons in a pulse, close to the ≈22 that §C0 Eq. (23) gives for a 10% target at 200 m with a 25 mm lens and 100 nJ:" Use $\bar n_1$ throughout the saturation passage.

**7. Line 1506 — C — medium**
- **Quote:** "Later sections apply them without re-deriving them; the "Used in" column of each table points to those sections."
- **Problem:** Two of the pointed-to sections re-derive the relation with their own equation numbers: §C3b in Eqs. (61) and (62), §E12 in Eqs. (172), (179) and (180). None of §C3b, §C4b, §C5 or §E12 cites §C0, so the links run one way only.
- **Proposed rewrite:**
  - Change the §C0 sentence to: "Later sections apply them, some restating them in their own notation and numbering; the "Used in" column points to those sections."
  - Add back-references:
    - §C3b after Eq. (61): "(the points-per-frame relation of §C0 subsection 3, times the frame rate)";
    - §C3b at Eq. (62): see finding 1;
    - §E12 after Eqs. (179) and (180): "(the relation $R\theta$ of §C0 subsection 3)";
    - §C4b and §C5: see findings 3 and 5.

**8. Line 3047 (§C3b, Eq. (61)) — D — medium**
- **Quote:** "$$\dot N=N_{\rm col}\,N_{\rm row}\,f_{\rm frame}=\frac{\Theta_H}{\delta\theta_H}\cdot\frac{\Theta_V}{\delta\theta_V}\cdot f_{\rm frame} \tag{61}$$"
- **Problem:** The angular point spacing has four notations: §C0 uses $\Theta_h$ and $\Delta\theta_h$ with no units; §C3b uses $\Theta_H$ and $\delta\theta_H$ in degrees; §E12 uses $\theta_{\rm step}$ in Eq. (179); §E11.3 uses $\Delta\theta$. The §C0 row is unnumbered, while §C3b numbers the same relation.
- **Proposed rewrite:** Adopt §C3b's numbered notation in §C0 subsection 3:
  - Symbol list: "$\Theta_H$, $\Theta_V$ are the horizontal and vertical fields of view, and $\delta\theta_H$, $\delta\theta_V$ the angular spacing of points along each (degrees)".
  - Table row: "| Points per frame | $(\Theta_H/\delta\theta_H)(\Theta_V/\delta\theta_V)$; times $f_{\rm frame}$ this is the point rate, Eq. (61) | … | §C3b (Eq. (61)) |".
  - Use $\delta\theta$ for $\theta_{\rm step}$ in §E12 and for $\Delta\theta$ in §E11.3.

**9. Line 1626 — D/A — low**
- **Quote:** "Footprint at range | $R\,\theta$ | 0.1° at 200 m → 35 cm; 0.05° → 17 cm | §E12"
- **Problem:** §E12 applies $R\theta$ to a lidar's angular grid step ("places points $R\,\theta_{\rm step}$ apart", Eq. (179)) and to a radar's cross-range cell (Eq. (180)), not to a beam footprint. §E11.3 uses it for point spacing too. The numbers match: 0.35 m and 0.175 m at 200 m in §E12's debris item.
- **Proposed rewrite:** "| Footprint or point spacing at range | $R\,\theta$, for a beam, a pixel or an angular step $\theta$ | 0.1° at 200 m → 35 cm; 0.05° → 17 cm | §E11.3, §E12 (Eqs. (179), (180)) |". Extend the symbol line to "…covers at range $R$, or the spacing of points for an angular step $\theta$".

**10. Line 1627 — B — low**
- **Quote:** "120°/0.1° × 25°/0.2° = 150,000; at 10 Hz, 1.5 Mpts/s"
- **Problem:** This looks like the AT128 but does not match §C3b's AT128 entry: 120° × 25.4°, $1{,}200\times128\times10=1.536$ M. Subsection 1's point-rate row uses the exact 1.536 M. A reader following the pointer finds 153,600 points per frame, not 150,000.
- **Proposed rewrite:** "1,200 × 128 = 153,600 points per frame (the Hesai AT128 grid, 0.1° × ≈0.2° over 120° × 25.4°, §C3b); at 10 Hz, 1.536 Mpts/s, the point rate of subsection 1". Update the derivation to match.

**11. Line 3118 (§C3b) — A — low**
- **Quote:** "since at fixed energy per frame $N_{\rm points}R^2$ is roughly constant (§C5a)"
- **Problem:** This scaling is the "Scaling" bullet of §C0 subsection 1 ($R\propto\sqrt{E_pA_{\rm rx}\rho}$). The same applies to the $A_{\rm rx}^{1/4}$ statement in the next bullet, also credited to §C5a. §C5a applies these relations; it does not derive them.
- **Proposed rewrite:** "(§C0 subsection 1; §C5a applies it to the AS-DT1)" in both places.

**12. Line 1702 — A — low**
- **Quote:** "InnovizOne's range table uses 90% true positives and a 5% false-alarm rate *per pixel* at 20 klx"
- **Problem:** Subsection 7 sends the reader to §C3b for detection definitions, but §C3b documents InnovizTwo's terms: "90% true / 1% false positives per pixel at 100 klx". InnovizOne's figures appear nowhere else in the report.
- **Proposed rewrite:** "InnovizOne's range table uses 90% true positives and a 5% false-alarm rate *per pixel* at 20 klx [P], and InnovizTwo's datasheet 90% true and 1% false positives per pixel at 100 klx (§C3b); Seyond's Falcon K1 uses >90% detection probability at 100 klx [P]."

**13. Line 3358 (§C4b) — E — low**
- **Quote:** "$$f_{\rm dead}=1-e^{-r\,\tau_d} \tag{65}$$"
- **Problem:** The same paralyzable dead fraction appears again as §C6 Eq. (82), so the two dead-time sections behind §C0's pointer "(§C4b, §C6)" number one relation twice.
- **Proposed rewrite:** Keep Eq. (65), which avoids renumbering. Introduce §C6's Eq. (82) as: "The paralyzable form repeats Eq. (65) of §C4b; the non-paralyzable form is new:"

##### 3. Consistency flags to check elsewhere
- **Assumed lidar range precision differs by section:**
  - §C0 subsection 1: ≈0.3 cm (ideal);
  - §C0 subsection 4: 3 cm;
  - §C4b: "cm-class";
  - §E12: "range noise ≈5 cm";
  - §C5a: AS-DT1 at 20–40 mm outdoors, and IMX459 at "15 cm precision in 6×6 mode".

  State which value each section assumes and why.
- **Energy per point has five symbols:**
  - $E_p$, per pulse (§C0 Eq. (23));
  - $E_{\rm tx}$ (§C0 10.1);
  - $E_{\rm pt}$ (§C6 Eq. (80));
  - $E_{\rm point}$ (§E11.3 Eq. (169) and §C0 subsection 9);
  - $P/\dot N$ (§C3b Eq. (62)).
- **The PDE symbol differs:** PDE in §C0 and §C6, $\eta_{\rm det}$ in §C3b.
- **$\tau$ has several meanings:**
  - round-trip delay: $\Delta t$ in §C0 subsection 1, but $\tau$ in §C0 subsection 2 and in §B8's "$R=c\,\tau/2$";
  - pulse length: $\tau_p$ (§C0 subsection 1);
  - time to contact: $\tau$ (§E12 Eq. (173)).
- **The Lambertian collection argument ("a fraction $\rho A_{\rm rx}/(\pi R^2)$") is written out four times:** Part A Eq. (5), §C0 subsection 1, §C3b ("Why the weight is $R^2$") and §C0 10.2. Only 10.2 and §C6 cite Eq. (23).
- **§C3b's AT128 entry is internally slightly off:** 128 rows × 0.2° = 25.6° against the stated 25.4° field.

### §C0 subsection 10 (link budget, detection statistics, range scaling)

**Coverage.** The whole block (lines 1858–2490) was read line by line, with all four figure PNGs and the §C0 subsections 1, 2, 3 and 5–8 that set up its symbols. Almost every substitution was recomputed, including the 10.3 detection tables (via the Marcum Q and gamma functions), the margin, fog, rain and dynamic-range tables and the benchmark arithmetic. Cross-references were only partly checked (see §3, item 15).

#### 1. Overall assessment

The argument is well built. It runs model, then light returned, then light needed, then where they cross, then scaling, margin, dynamic range, benchmark and limits. Each part opens with the question it answers, and the arithmetic is very clean: the 10.3 tables and the 10.6 rain table reproduce exactly, and only a few small rounding slips remain.

The three systemic problems:
- **"Link loss" names a fraction.** $\mathcal{L}$ is a fraction of the light, but the prose says the "loss falls" or "grows" in both senses. "Falling" even contradicts Figure C0.10a, where the loss axis rises with range.
- **Model assumptions behind the headline ratios are hidden.** The four looks are two polarizations on two apertures (§C7a), and the ToF lens is 25 mm against FMCW's 22 mm optimum. Without these, a reader cannot reconcile the 2.5×, 3.2× and 16× claims.
- **Symbols and terms drift.** S, M and γ each carry several meanings; "per sample" alternates with "per point", "photons" with "photoelectrons", and "fog" with "haze"; and the sign of dB losses changes.

The order of the sub-subsections works. I would make only three moves: put the $w_0=0.45D$ derivation before it is used, optionally move 10.8 directly after 10.4, and move 10.7's evidence survey out of the primer.

#### 2. Findings (most severe first)

1. **Line** 1989 (also 1990, 1992, 2121) — **A** — **high**
   - **Quote:** "on these axes, falling 20 dB per decade of range for every lens"
   - **Problem:** Figure C0.10a plots $-10\log_{10}\mathcal{L}$ upward, so these lines rise. The same applies at 1990 ("falls 20 dB per decade beyond it, 4.7 dB below the direct-detection line", where the curve is actually 4.7 dB above it), 1992 ("falls only 10 dB per decade") and 2121 ("flat, then falls"). The text contradicts the figure it reads.
   - **Proposed rewrite:**
     - 1989: "on these axes, rising 20 dB per decade of range for every lens."
     - 1990: "**Coherent detection is flat, then rises.** Each curve is level out to about its Rayleigh range (41, 257 and 1,026 m for 10, 25 and 50 mm) and rises 20 dB per decade beyond it, 4.7 dB above (worse than) the direct-detection line of the same aperture."
     - 1992: "Its loss rises only 10 dB per decade ($1/R$) …"
     - 2121: the same "flat, then rises" heading.

2. **Line** 2286 (systemic; also 2287, 2101, 2118, 2209) — **A** — **high**
   - **Quote:** "where its loss falls as $1/R^2$ like direct detection"
   - **Problem:** $\mathcal{L}$ is a transmitted fraction, where larger means more light, but it is called a loss. The next bullet, at 2287, says "the loss grows with range" for the same direction of change, using the opposite verb. Further cases: "'Largest loss' means the smallest usable fraction" (2101), "Fog multiplies the link loss" (2209) and "Direct detection falls as $D^2/R^2$" (2118).
   - **Proposed rewrite:** Either rename $\mathcal{L}$ the "link fraction" throughout and keep "link loss" for its dB value only, starting at 1928: "**Definition of the link fraction.** The link fraction $\mathcal{L}$ is the fraction … Its value in dB, $-10\log_{10}\mathcal{L}$, is the link loss: a larger number of dB means less light." Or keep the name and use verbs only for the dB loss. In either case:
     - 2286: "where its collected fraction falls as $1/R^2$ (its loss rises 20 dB per decade), as for direct detection."
     - 2287: "in fog, whose extinction adds a loss that grows with range."

3. **Line** 1885 — **A/B** — **high**
   - **Quote:** "needs five times the energy of the best FMCW design, i.e. sixteen times ToF's"
   - **Problem:** The bullet just above (1883) says FMCW needs about 2.5× ToF's energy, so the reader computes 5 × 2.5 = 12.5, not 16. The 16 holds because the best FMCW design needs 303 nJ against the 25 mm ToF design's 96 nJ, which is 3.2×.
   - **Proposed rewrite:** "…needs five times the energy of the best FMCW design: 1.5 µJ per point against 303 nJ, or sixteen times the 96 nJ of the 25 mm ToF design. The best FMCW design already needs 3.2 times ToF's energy here, not 2.5 times, because the ToF lens (25 mm) is larger than FMCW's 22 mm optimum."

4. **Line** 1883 — **A** — **high**
   - **Quote:** "This underlies the energy-per-point comparisons between ToF and FMCW in §C7a and §C10."
   - **Problem:** §C7a (line 4699) and §C7b (Eq. (104)) use about 3.2×, not 2.5×. Also, "When both receivers use the same aperture" hides that the four-look FMCW receiver uses two apertures (§C7a, 4668 and 4673).
   - **Proposed rewrite:** "**Equal apertures, constant gap** (10.5). When each of the FMCW receiver's two apertures (its four looks are two polarizations on each of two spatial modes, §C7a) is as large as the ToF lens and sized optimally for the coherent beam at each range, FMCW needs about 2.5 times the energy per point of SPAD ToF, whatever the range. Against the fixed 25 mm ToF lens of §C7a the factor is 3.1 at 200 m, the ≈3.2× used in §C7a, §C7b and §C10."

5. **Line** 2029 (also 2107, 2113, 2134) — **A** — **high**
   - **Quote:** "(polarization, wavelength or spatial diversity; each is one *look*, taken by its own coherent receiver), with $\bar n$ split equally among them"
   - **Problem:** The block never says how the model's four looks are formed. Yet 10.4 lets every look collect the full $\mathcal{L}_{\rm coh}$ from the full $E_{\rm tx}$. A reader cannot tell why the energy is not split four ways; with wavelength diversity it would be.
   - **Proposed rewrite:** After the 10.3 table add: "**How the model's four looks are formed.** They are two polarizations on each of two spatial modes, received through two apertures of the same diameter side by side, one of which also transmits (§C7a). Each look therefore collects the full $\mathcal{L}_{\rm coh}$ of Eq. (33) from the same transmitted energy. Wavelength diversity would instead split $E_{\rm tx}$ between looks."

6. **Line** 1882 (also 2118) — **A** — **medium**
   - **Quote:** "Direct detection loses signal as $D^2/R^2$ at every range"
   - **Problem:** Read literally, the signal loss grows with $D$. What scales as $D^2/R^2$ is the collected fraction.
   - **Proposed rewrite:** "**Direct detection collects a fraction proportional to $D^2/R^2$ at every range** (10.2). A coherent (FMCW) receiver collects only the light in one spatial mode, so its collected fraction is flat out to the beam's Rayleigh range and falls beyond it." Use the same wording at 2118.

7. **Line** 2330 (also 1886, 2374) — **A** — **medium**
   - **Quote:** "The ToF design's 74 dB for a sign at 5 m becomes 148 dB at the amplifier input."
   - **Problem:** The ToF design is a SPAD photon counter, with no linear amplifier. Eq. (54) doubling applies to APD or PIN receivers. The same issue appears at 1886 ("twice that in its electronics") and 2374 ("148 dB at its amplifier"). "Field detection" is also first used at 1886 without being explained.
   - **Proposed rewrite:**
     - 2330: "In a linear (APD or PIN) receiver a photocurrent proportional to optical power doubles the dB span: a linear receiver facing the ToF design's 74 dB for a sign at 5 m would see 148 dB at its amplifier input. The SPAD design has no linear amplifier; its limit is the count ceiling below."
     - 1886: "…must span 56–82 dB of optical signal; a linear ToF receiver would see twice that in dB at its amplifier. The best FMCW design must span about 45 dB, and because its beat current is proportional to the optical field, the electrical span stays 45 dB."

8. **Line** 2399 (also 2397) — **B** — **medium**
   - **Quote:** "Its burden is 25–30 dB smaller for the large-aperture designs, and electrically halved."
   - **Problem:** The table gives 29 dB (sign at 5 m), 37 dB (sign at 2 m), 43 dB (white target at 1 m) and 14 dB (sign at 30 m). "Electrically halved" is ambiguous. Line 2397's "70–80 dB of optical span" disagrees with the 56–82 dB in the table and in 1886.
   - **Proposed rewrite:**
     - 2399: "For a retroreflective sign at 2–5 m its optical span is 29–37 dB smaller than the ToF design's (45 against 74–82 dB). Electrically the gap is larger still (45 against 148–164 dB in a linear receiver), because field detection does not double the span."
     - 2397: "over 56–82 dB of optical span (112–164 dB electrical in a linear receiver)".

9. **Line** 2311 (also 2384) — **B** — **medium**
   - **Quote:** "By Eq. (53) that is $\rho_{\rm eq}=0.5\times10^{3.18}\approx760$, i.e. $R_A\approx240$, close to Type III sheeting."
   - **Problem:** This is a coherent, single-polarization measurement against a depolarizing reference. The block's own "Polarization" note (2326) says a retroreflector can appear up to 3 dB stronger in such a receiver, so $R_A$ could be as low as ≈120. Separately, 31.8 dB above a 50% target implies 41.8 dB above a 5% target at the same range, but 2384 says the retroreflector was 37.7 dB brighter than the 5% target.
   - **Proposed rewrite:** "By Eq. (53), treating the retroreflector as depolarizing like the reference, that is $\rho_{\rm eq}\approx760$, i.e. $R_A\approx240$. If it preserves polarization, it gains up to 3 dB in a single-polarization coherent receiver (see 'Polarization' below the table), and $R_A$ may be as low as ≈120." At 2384, say whether the 37.7 dB comes from a different measurement or range.

10. **Line** 2378 (also 2376) — **B** — **medium**
    - **Quote:** "An FFT over 10 µs sampled at 1 GS/s gains about 40 dB"
    - **Problem:** In 10.3 the §C7a chirp has 5 µs ramps, and §C7a samples at 2.5 × 490 MHz ≈ 1.2 GS/s. That gives about 6,100 samples and 37.9 dB of FFT gain. The "about 15 dB" weakest-return SNR at 2376 is not tied to the model, which gives 15 photoelectrons per look per ramp, i.e. 11.8 dB.
    - **Proposed rewrite:** "Take the weakest detectable return: 15 photoelectrons per look in each ramp (120 over four looks and two ramps), a per-bin SNR of 11.8 dB. The sign, 45 dB stronger, sits about 57 dB above the noise in its FFT bin. An FFT over one 5 µs ramp sampled at ≈1.2 GS/s (§C7a) has about 6,100 samples and gains about 38 dB, so before the FFT the sign's tone is only about 19 dB above the noise, which does not stress the ADC."

11. **Line** 2433 — **A** — **medium**
    - **Quote:** "so 10 dB at 200 m implies $P_{\rm TX}\eta\approx$ 5–11 mW, i.e. 18–36 mW transmitted at $\eta=0.3$."
    - **Problem:** The derivation is skipped: no equation, no integration time $T$, no link loss. It also uses $\eta=0.3$ where the rest of the report uses 0.25. My reconstruction: $\mathcal{L}_{\rm coh}(200\ {\rm m})=1.5\times10^{-11}$, times a coherence factor of 0.43, gives $\eta P_{\rm TX}T\approx2\times10^{-7}$ J, so 5–11 mW implies $T\approx$ 18–40 µs.
    - **Proposed rewrite:** "Shot-noise-limited, SNR $=\eta P_{\rm TX}T\,\mathcal{L}_{\rm coh}\,e^{-4\pi\Delta\nu R/c}/E_{\rm ph}$, where $T$ is the integration time per ramp. With $\mathcal{L}_{\rm coh}=1.5\times10^{-11}$ (Eq. (33), $w(200\ {\rm m})=28.4$ mm) and a coherence factor of 0.43, SNR = 10 needs $\eta P_{\rm TX}T\approx2\times10^{-7}$ J, i.e. $\eta P_{\rm TX}\approx$ 5–11 mW for $T=$ 18–40 µs [E; insert the paper's $T$]. At $\eta=0.25$ that is 20–44 mW transmitted."

12. **Line** 2474 — **B** — **medium**
    - **Quote:** "given f/1-class lenses of 10–30 mm and PDEs of 5–22%"
    - **Problem:** The 5–10% values (Toshiba, Toyota, 2447–2448) are overall efficiencies $\eta$, not photon detection efficiencies (PDEs).
    - **Proposed rewrite:** "given f/1-class lenses of 10–30 mm and overall receive efficiencies $\eta$ of 0.05–0.12 (Sony's PDE is 22%; Toshiba and Toyota publish none)".

13. **Line** 2416 (also 2072, 2423, 2437) — **B** — **medium**
    - **Quote:** "−106.1 dB; 50 photons; $P_D=0.9$"
    - **Problem:** Line 2072 and §C7a (4693) call Waymo's 50 "photoelectrons", while this table says "photons". The model side is also given three ways: 49 photons per chirp, 44 photoelectrons, and 47.3 (2072) against ≈45 (2423).
    - **Proposed rewrite:**
      - Model cell: "Link loss 106.2 dB; 44 photoelectrons per chirp (49 photons at QE 0.9); $P_D=0.895$ …"
      - Published cell: "106.1 dB; 50 photoelectrons; $P_D=0.9$". Check this against Piggott et al.; if the paper's 50 are photons, change 2072 and 4693 instead.
      - 2072: "…which needs 47.3 under this report's rule ($4\times10^{-7}$ per bin over 2,450 bins), and 44.9 at Waymo's own $10^{-6}$ per bin (10.8)."

14. **Line** 2463 (also 2416) — **E** — **medium**
    - **Quote:** "with a link loss of −117.6 dB"
    - **Problem:** 10.2 defines the dB loss as $-10\log_{10}\mathcal{L}$, which is positive (94.1 and 103.0 dB); 10.8 switches to negative values (−106.2 and −106.1 dB as well).
    - **Proposed rewrite:** "with a link loss of 117.6 dB", and "Link loss 106.2 dB" / "106.1 dB" in the table. The relative changes in the indie and Wang rows can stay as "falls of 1.8 dB" and so on.

15. **Line** 2482 (also 2486) — **A** — **medium**
    - **Quote:** "so its loss grows as $R^{-4}$ (subsection 1; §E12)"
    - **Problem:** The direction is wrong: the returned fraction falls as $R^{-4}$. Line 2486 also says non-Lambertian targets "lower $\mathcal{L}_{\rm coh}$", but retroreflectors raise it.
    - **Proposed rewrite:**
      - 2482: "so the fraction it returns falls as $1/R^4$ (40 dB per decade; subsection 1; §E12)."
      - 2486: "**Turbulence and misalignment** lower $\mathcal{L}_{\rm coh}$ further (Frehlich and Kavaya 1991) [I]; **non-Lambertian targets** change it either way."

16. **Line** 2130 — **A** — **medium**
    - **Quote:** "A bigger collimated aperture helps only beyond its own Rayleigh range; at 500 m the optimum is 35 mm."
    - **Problem:** This contradicts 1991. There, 25 mm beats 10 mm beyond 103 m, which is well inside 25 mm's 257 m Rayleigh range.
    - **Proposed rewrite:** "An aperture larger than $D_{\rm opt}(R)$ collects less at $R$ itself; it pays only at longer ranges, where it becomes the optimum: at 500 m the optimum is 35 mm."

17. **Line** 2147 — **A** — **medium**
    - **Quote:** "while the footprint's share of a fixed angular cell shrinks as $1/R$ (§C10.3a)"
    - **Problem:** Cryptic at its first appearance in the report's reading order.
    - **Proposed rewrite:** "Doubling the energy doubles the range, but only if the aperture grows as $\sqrt R$. The footprint area then grows only as $R$ ($w^2=2\lambda R/\pi$), while the area of a fixed angular resolution cell grows as $R^2$, so the beam covers a share of the cell that shrinks as $1/R$ (§C10.3a)."

18. **Line** 2246 — **A** — **medium**
    - **Quote:** "It is tied to the extinction by the lidar ratio $S=\alpha/\beta$, here 18 sr"
    - **Problem:** $S$ is already the summed speckle gain in Eq. (40) (2043) and the sweep rate in subsection 3 (1607).
    - **Proposed rewrite:** "…by the lidar ratio $S_{\rm L}=\alpha/\beta$, here 18 sr [E]; O'Connor et al. (2004) give 18.8 sr …". Alternatively, rename the speckle gain $G$.

19. **Line** 2174 — **A** — **medium**
    - **Quote:** "The margin $M(R)$ of a design at range $R$ is the extra loss, in dB, that it can absorb there and still detect the target"
    - **Problem:** $M$ is also the APD gain (Eqs. (25)–(26)), $M^2$ the beam quality (1897), and the generalized Marcum index "$Q_M$" (2043).
    - **Proposed rewrite:** Use $\mathcal{M}(R)$ and $\mathcal{M}_0$ in Eqs. (46)–(49) and (52) and in the text, and write the Marcum function as $Q_N(a,b)$ for $N$ bins, matching $Q_{N_{\rm sp}}$ in Eq. (40).

20. **Line** 2019 (also 2016, 2336) — **A** — **medium**
    - **Quote:** "so the §C7a model multiplies the SPAD's signal efficiency by it, $0.5\times0.37\times0.784=0.145$."
    - **Problem:** The 0.5 is unexplained until 2111. "The nine SPADs" (2016) appears before the 3×3 macro-pixel is introduced (2336). "At most nine counts per shot" (2336) should read per echo: a 2 µs shot allows many counts per SPAD.
    - **Proposed rewrite:**
      - 2019: "…by it: optics transmission 0.5 × PDE 0.37 × live fraction 0.784 = 0.145."
      - 2016: "Each of the macro-pixel's nine SPADs (a 3×3 group, §C5a) counts …"
      - 2336: "registers at most nine counts from one echo".

21. **Line** 2018 — **A** — **medium**
    - **Quote:** "Over the 20.8 µs a point listens, the same rate gives"
    - **Problem:** 20.8 µs is used without a source.
    - **Proposed rewrite:** "A macro-pixel listens 20.8 µs per point, one column period of the §C7a scan (about ten 2.08 µs shots; §C5a, §C7a). Over that time the same rate gives …"

22. **Line** 2225 — **D** — **medium**
    - **Quote:** "(below 500 m visibility), where extinction no longer depends on wavelength"
    - **Problem:** "Fog" is defined three ways. The text uses below 500 m. The caption (2280) and figure use fog for 0.2–1 km and thick fog for 50–200 m. Subsection 8 calls 1 km "light fog".
    - **Proposed rewrite:** "**Below 500 m visibility**, where the Kim exponent $q_{\rm K}$ is zero and extinction no longer depends on wavelength, the best-aperture FMCW design keeps …". Then align subsection 8's row labels with the caption's classes.

23. **Line** 2214 (also 2230, 2315, 2256/2263) — **E/C** — **medium**
    - **Quote:** "| Design | $V=5$ km | 2 km | 1 km | 500 m | 200 m | 100 m | 50 m |"
    - **Problem:** The fog, rain and dynamic-range tables have no introductory sentence. The clutter table is explained only after it (2263), and two of its columns are for designs that cannot see the 50 m target.
    - **Proposed rewrite:** Add before each table:
      - Fog: "The table gives each design's maximum range on a 10% target from Eq. (49), versus meteorological visibility $V$ (Kim model)."
      - Rain: "The table gives the maximum range in rain from Eq. (49) with $2\gamma_{\rm rain}R$, with a clean window and with a 0.1 or 0.2 mm water film (0.94 and 1.88 dB at 1,550 nm)."
      - Dynamic range: "The table evaluates Eq. (52) for the designs of 10.6, in dB above each design's weakest detectable return."
      - Clutter: move the first two sentences of 2263 above that table.

24. **Line** 2298 (whole of 10.7) — **C** — **medium**
    - **Quote:** "10.7 Dynamic range: strong returns, blooming and blinding"
    - **Problem:** About 100 lines mix a short derivation (Eqs. (52)–(54) and the span table) with a survey of datasheets, patents, firmware, standards and vendor claims. That survey is not primer material, and the key result ("What this means", 2396) comes last.
    - **Proposed rewrite:** Keep in §C0 the opening, Eqs. (52)–(54), the retroreflector bullets, the span table, "What ToF receivers can span" and a short "What coherent detection changes". Put "What this means" directly after the span table. Move "How strong returns fail in ToF lidars" and "Tests and evidence" to a receiver section (for example §C4b or §C3b) and leave a § pointer.

25. **Line** 2148 (also 1883, 2154) — **D** — **medium**
    - **Quote:** "the ratio of the energies per sample needed by FMCW and SPAD ToF does not depend on range"
    - **Problem:** $E_{\rm tx}$ is defined "per point" (1904); "per sample" appears only in these three places.
    - **Proposed rewrite:** "the ratio of the energies per point needed …". Make the same change at 1883 and 2154, or define once: "(one FMCW sample, an up–down chirp pair, is one point)".

26. **Line** 2127 — **B** — **low**
    - **Quote:** "cuts the 25 mm range to **54 m**"
    - **Problem:** For a factor of 1.5 (45/30) I get 53 m with clear-air loss and 56 m without; an exact +1.8 dB gives 47 m.
    - **Proposed rewrite:** "cuts the 25 mm range to **53 m** (56 m without clear-air loss)", after checking against the script.

27. **Line** 1973 — **C** — **low**
    - **Quote:** "Why the beam is launched with $w_0=0.45D$."
    - **Problem:** The paragraph comes after 0.45 and $t$ have already been used (1966, 1971).
    - **Proposed rewrite:** Move it to just before "In a monostatic system …" (1952).

28. **Line** 2034 — **A** — **low**
    - **Quote:** "at $f_{\rm up}=f_b-f_D$ and $f_{\rm down}=f_b+f_D$"
    - **Problem:** $f_b$ and $f_D$ are not defined at their first use in this subsection.
    - **Proposed rewrite:** Append ", where $f_b$ is the beat frequency set by range and $f_D$ the Doppler shift (subsection 2)."

29. **Line** 2038 — **C** — **low**
    - **Quote:** "Eq. (94) of §C7a samples these bins five times over, $N_{\rm samp}=5N_b\approx12{,}300$."
    - **Problem:** An unclear digression that the block never uses. It actually means 2.5 samples per bin in each ramp, over two ramps. Likewise, "Where b = 2.87 comes from" (2013–2019) repeats §C7b (4893–4894) at length.
    - **Proposed rewrite:** Delete the sentence, or replace it with "(§C7a's digitizer takes 2.5 samples per bin in each ramp, so its Eq. (94) counts $N_{\rm samp}=5N_b\approx12{,}250$ samples per point)". Shorten the background derivation to its result plus a pointer.

30. **Line** 2077 — **A** — **low**
    - **Quote:** "the median ($P_D=0.5$) is 36–39 photoelectrons with one, two or four looks"
    - **Problem:** The table's $P_D=0.5$ column does not change monotonically with the number of looks (38.2, 36.2, 39.0), and nothing explains why.
    - **Proposed rewrite:** Add: "At $P_D=0.5$ more looks do not help: summing the noise of four looks needs a higher threshold (18.2 against 11.1), which offsets their narrower fading."

31. **Line** 2272 — **A** — **low**
    - **Quote:** "so the fog adds a weak noise floor in the near-range bins and nothing at the target's frequency"
    - **Problem:** Eq. (50) gives −19.9 dB of fog in the target's own bin, so "nothing" is too strong.
    - **Proposed rewrite:** "…and, at the target's frequency, only the in-bin fog return of Eq. (50) (−19.9 dB at 200 m visibility)."

32. **Line** 2353 — **E** — **low**
    - **Quote:** "That is $\varepsilon<-74$ dB for the ToF design and a sign at 5 m, more suppression than lens and window scattering usually provide."
    - **Problem:** It mixes a linear $\varepsilon$ with dB, and the claim has no tag.
    - **Proposed rewrite:** "That is $10\log_{10}\varepsilon<-74$ dB … usually provide [U]", or cite a stray-light figure.

33. **Line** 2339 (rounding set) — **B** — **low**
    - **Quote:** "That is a linear range of about 63 dB in current"
    - **Problem:** $20\log_{10}(75\ \mu{\rm A}/49\ {\rm nA})=63.7$ dB. Other small slips:
      - 2456: the displayed $2.9\times10^{-7}$ gives $1.34\times10^{-5}$, not $1.4\times10^{-5}$.
      - 2059: 17.3 + 2.87 = 20.17, not 20.1.
      - 1976: $0.915^2=0.837$, not 0.838.
      - 2153: the ratio is 2.47 at 100 m.
      - 2115: as displayed, the substitution gives $5.12\times10^{-11}$.
    - **Proposed rewrite:**
      - 2339: "about 64 dB".
      - 2456: substitute $2.86\times10^{-7}$.
      - 2059: "$s=17.26$ … $s+b=20.13$".
      - 1976: "$t^2=0.9153^2$".
      - 2153: "2.4–2.5 at 100–500 m".

34. **Line** 2123 — **D** — **low**
    - **Quote:** "Its near field is $10\log_{10}(1310/1550)^2=-1.5$ dB weaker, at 102.4 dB"
    - **Problem:** A double negative.
    - **Proposed rewrite:** "Its near-field level is 1.5 dB weaker ($10\log_{10}(1310/1550)^2=-1.5$ dB), at 102.4 dB, …"

35. **Line** 2478 — **C** — **low**
    - **Quote:** "and, for SPAD sensors in full sun, range scaling with reflectance closer to $\rho^{1/4}$ than the $\rho^{1/2}$ the model assumes."
    - **Problem:** Filed under "imply undisclosed powers", but it is not about power.
    - **Proposed rewrite:** Make it its own bullet: "**Reflectance scaling.** For SPAD sensors in full sun, range scales with reflectance closer to $\rho^{1/4}$ than the model's $\rho^{1/2}$."

36. **Line** 2446 (convention slips) — **E** — **low**
    - **Quote:** "150 m on 10% at 117 klux"
    - **Problem:**
      - Units: "klux" (2446–2448) against "klx" (2460 and 1692).
      - Unexpanded acronyms: FWHM (2462), SUSTech (2420), CVPR (2350), FDIS (2365), WMO (2281), QE (2416).
      - Very wide display equations: Eqs. (40), (46), (51).
    - **Proposed rewrite:**
      - Units: "klx" throughout.
      - Acronyms: "full width at half maximum (FWHM)", "Southern University of Science and Technology (SUSTech)", "quantum efficiency (QE)", and so on.
      - Equations: split each into one relation per line, keeping the single global tag.

37. **Line** 2427 (10.8 notation) — **A** — **low**
    - **Quote:** "(their $\kappa=0.62$, i.e. $1/(1+1/\kappa^2)$)"
    - **Problem:**
      - $\kappa$ is undefined.
      - $P_{\rm RX}/P_{\rm TX}$ (2425) is new notation for $\eta\mathcal{L}$, and $q$ (2426) is not defined here.
      - "100 kHz laser" (2420) reads as a repetition rate.
      - "a 5 mm waist" (2420, 2432) is a radius, but the stated "7 mm waist diameter" is a diameter.
      - "32 µs chirps (11.4 nJ per point)" (2418) hides that there are two chirps per point.
      - The indie row (2419) says "Flat to $z_R$", then gives a −1.8 dB fall at 50 m, which is inside $z_R\approx70$ m.
    - **Proposed rewrite:** Define $\kappa$ in a phrase. Write $\eta\mathcal{L}$ and "$q$, the elementary charge". Use "a laser of 100 kHz linewidth", "a waist radius of 5 mm", "two 32 µs chirps per point (11.4 nJ)", and "falls by 1.8, 4.8 and 9.6 dB at 50, 100 and 200 m".

38. **Line** 1915 (evidence tags) — **E** — **low**
    - **Quote:** "Waymo's lab chain measured 0.112 end to end, or 0.168 without its Hann window (Piggott et al. 2025, App. A)"
    - **Problem:** Tags are missing or irregular:
      - This sentence has no [P]; the §C7a copy at 4697 has one.
      - 2461 "likely below 37%" has no tag.
      - 1898 and 2486 cite Frehlich and Kavaya without [I].
      - 2246 "18 sr" has no tag.
      - "[P/T]" (2364) and "[E, 30 mW transmitted]" (2333) are non-standard.
    - **Proposed rewrite:**
      - Add [P] after both citations here.
      - 2461: "likely below 37% [E]".
      - 1898 and 2486: [I].
      - 2246: "here 18 sr [E]".
      - 2333: "[E]", with "for 30 mW transmitted" moved into the sentence.

39. **Line** 2194 — **A** — **low**
    - **Quote:** "Plateau margins of 6.7, 9.7, 13.9 and 20.0 dB (apertures of 16, 13, 10 and 7 mm)"
    - **Problem:** The table's "Margin at 10 m" gives 13.8 and 19.1 dB (and 3.1 against $M_0=3.0$ dB), and the difference is unexplained.
    - **Proposed rewrite:** Add after the table: "The margin at 10 m is below $M_0$ for the 10 and 7 mm designs because 10 m is a sizeable fraction of their Rayleigh ranges (41 and 20 m); the table also includes clear-air extinction (≈0.08 dB)."

40. **Line** 1936 (also 1910) — **A** — **low**
    - **Quote:** "Clear air adds 0.15 dB, for 94.2 dB."
    - **Problem:** The wavelength is unstated: 0.15 dB is the 940 nm value. Likewise, 1910's 63 mm² is a 1,550 nm value.
    - **Proposed rewrite:** "Clear air at 940 nm adds 0.15 dB, for 94.2 dB." and "63 mm² at 1,550 nm against the 491 mm² of a 25 mm aperture at 200 m."

#### 3. Consistency flags to check elsewhere

1. **Energy ratio.** The block says 2.5× at 1883 and 3.1× at 200 m at 2154. §C7a line 4699 has "≈3.2× … 0.30 µJ against 93 nJ", and §C7b lines 4837 and 4960–4961 give Eq. (104) = 3.25.
2. **Four looks.** They are two polarizations × two spatial modes through two 20 mm apertures (§C7a 4668, 4673). The block (2029, 2107, 2113, 2134, 2148) never says so.
3. **Waymo's 50.** Called photoelectrons at 2072 and §C7a 4693, photons at 2416.
4. **Fog classes.**
   - Subsection 8 table (1713–1716): 1 km "light fog", 50 m "dense fog".
   - Caption 2280 and the figure: fog 0.2–1 km, thick fog 50–200 m, haze above 1 km.
   - Block text 2224–2225: fog below 500 m.
5. **Detection rule.** Subsection 7 (1687–1690) uses 1,000 bins and $10^{-6}$ per bin, so daylight needs $s\approx13$. 10.3 uses 2,000 bins and $5\times10^{-7}$ per bin, so bright sun needs 17.3. "Same per-point budget" (2000) is true, but readers will compare 13 with 17.3.
6. **Symbol reuse.**
   - $S$: 1607 and Eq. (69) at 3671 (sweep rate), 2043 (speckle gain), 2246 (lidar ratio).
   - $M$: 1661–1669 and Eqs. (99)–(100) at 4899–4902 (APD gain), 1897 ($M^2$), 2174 onward (margin), 2043 (Marcum index).
   - $\gamma$: 2009 (incomplete gamma), 1725 and 2228 ($\gamma_{\rm rain}$), Eq. (74) at 3770.
   - $p$: 1604 (pixel pitch) against 2002 onward (per-bin false-alarm probability).
   - $u$: 2008 against 2192; $x$: 2022 against 1973.
   - $R_A$ and $R_r$ against range $R$; $\mathcal{D}$ against $D$.
7. **Duplicated equations.** Eqs. (33)/(34)/(35) reappear as Eqs. (101)/(102)/(103) (4914–4923), and Eq. (55) as Eqs. (93)/(97) (4678, 4879). Consider cross-references instead of new numbers.
8. **Water film.** The film-only results at 2189 (110 m and 58 m) match $X=1.9$ dB, while the rain table (2230–2238) reproduces exactly with $X=0.94$ and 1.88 dB. At 1.88 dB the 25 mm film-only range would be 61 m (111 m for the best design).
9. **Line 2127 (54 m).** Recomputed as 53 m with clear air, 56 m without.
10. **Retroreflector contrast.** 2311 (31.8 dB above a 50% target) and 2384 (37.7 dB above a 5% target) both cite Settembrini et al. 2026 and disagree by 4 dB.
11. **ToF span.** 56–82 dB at 1886 and in the table (2317–2321), but 70–80 dB at 2397.
12. **Efficiency caveat repeated.** 0.057 / 0.112 / 0.168 appear at 1887, 1915, 2438 and 2473, and again at §C7a 4697 and §C7b 4958. The numbers are consistent; this is repetition only.
13. **Chirp examples.** Subsection 2 uses $T=10$ µs per segment (1566). 10.3 uses §C7a's 5 µs ramps. Line 2378's "10 µs" may come from the former.
14. **Figure–text mismatches.**
    - Figure C0.10a panel (a) title says "collects the whole cell"; 1932 says "whole spot".
    - The shaded 200–300 m band (1983) is unexplained.
    - Figure C0.10c has no "Reading Figure C0.10c" paragraph, unlike the other three figures.
15. **Cross-references checked and correct:**
    - Eq. (23) at 1531; Eq. (27) at 1695.
    - Eqs. (81)/(82) at 4293/4299, in §C6(d); Eq. (94) at 4721, in §C7a; Eq. (98) at 4891, in §C7b.
    - §C4c's 82–94% at 3585 and 9.4 dB/mm at 3615.
    - §C10.2 item 4, $R_A\approx500$, at 5848.
    - §C7a(a) at 4664; §C7b 1(a) at 4888; §C7b 2(i) at 5221.
    - The 20.8 µs listening time is consistent between §C5a (4014) and §C7a (4740), but 2018 cites neither.

    **Not checked:** the §C3b figure-of-merit text, the content of §C10.3a/b, §C5a's paralyzable statement and §E12.

#### Follow-up cross-checks for this block (second pass, 2026-10-03; new findings only, against the report after both edit batches)

All four cross-references are checked. Line numbers below may be off by a few lines (§E12's heading moved from 8451 to 8459 during the check), so locate by quote.

#### Results of the four checks

- **§E12 (item 4).** The pointer is wrong. §E12 never states the $R^{-4}$ small-object law; it is in §E11.3 (Eq. (169)). Finding 1.
- **§C3b (item 1).** Its Eq. (62) is subsection 10's Eq. (42) rearranged ($A_{\rm rx}=\pi D^2/4$, $\eta=\eta_{\rm opt}\eta_{\rm det}$, $N_s=n_{\rm req}$). But §C3b assumes signal-limited detection, and subsection 10 applies the relation in bright sun without that condition. Finding 2.
- **§C5a (item 3).** §C5a presents the paralyzable behaviour as an [E] inference about the development chip, notes a contrary press release, and adds "The product may differ from the development chip." Subsection 10 states it as fact. Finding 3.
- **§C10.3a/§C10.3b (item 2).** Both pointers are supported:
  - §C10.3b uses $t=0.915$ with $w_0=0.45D$ and the same monostatic link equation (63.7 mm² for 20 mm at 200 m; ceiling $\lambda R/4$; far-field loss about 3×, matching 10.2's 0.34).
  - §C10.3a item 3 gives the footprint fraction $2\lambda/(R\theta^2)\propto1/R$.
  - §C10.3a item 3 and §C10.3b Result 4 cover small objects being missed between samples.
  
  Its assumption list matches 10.1. But the two sections conflict with subsection 10 on efficiencies, on what the "optimum diameter" means, and on the symbol $N_{\rm sp}$ (flags a–c).

#### New findings

1. **Line** 2492 — **A** — **medium**
   - **Quote:** "so its loss grows as $R^{-4}$ (subsection 1; §E12). A narrow coherent beam is filled by smaller objects, but it must hit them (§C10.3a)."
   - **Problem:** §E12 contains no $R^{-4}$ law. The law and its consequence $R\propto E_{\rm point}^{1/4}$ are in §E11.3 ("For a target smaller than the footprint, it intercepts a share of the beam that also falls as $1/R^2$", Eq. (169)). §E12 (subsection 3, item 5) only counts pixels and points on small debris ("0–1 lidar points on the 0.1° grid … at 200–300 m"). That fits the second sentence, not the first.
   - **Proposed rewrite** (also covers earlier finding 15 on the same sentence): "- **Small objects.** An object smaller than the footprint intercepts a fraction of the light that falls as $1/R^2$, so the fraction it returns falls as $1/R^4$ and range grows only as $E_{\rm tx}^{1/4}$ (subsection 1; §E11.3, Eq. (169)). A narrow coherent beam is filled by smaller objects, but it must hit them (§C10.3a, item 3; §C10.3b, Result 4). At 200–300 m a 15–30 cm object gets at most about one point on a 0.1° grid, whatever the receiver (§E12, subsection 3, item 5)."

2. **Line** 2148 — **A** — **medium**
   - **Quote:** "is constant: this is the range-weighted point-rate figure of merit of §C3b."
   - **Problem:** §C3b's Eq. (62) is constant only under "signal-limited detection (a fixed number of detected signal photons per point suffices, whatever the background)". §C3b adds that the conserved product tends toward $\dot N R^4$ when sunlight limits. Subsection 10 applies the relation with the bright-sun $n_{\rm req}$ and drops that condition. In the 10.3 model the bright-sun requirement depends on how the energy per point is delivered. With 5, 10 and 20 shots per point ($b=1.43$, 2.87 and 5.73), the ideal counter needs 14.0, 17.3 and 22.5 counts. So $\dot N R^2$ moves by about 25% per factor of two in point rate.
   - **Proposed rewrite:** "So $\dot N R_{\max}^2=\rho\,\eta\,D^2P_{\rm opt}/(4n_{\rm req}E_{\rm ph})$ is constant as long as $n_{\rm req}$ is: this is Eq. (62), the range-weighted point-rate figure of merit of §C3b, which assumes signal-limited detection. In bright sun $n_{\rm req}$ grows with the background a point collects. If the energy per point is changed through the number of shots, the ideal counter of 10.3 needs 14.0, 17.3 and 22.5 counts for 5, 10 and 20 shots [E]. $\dot N R^2$ then shifts by about 25% per factor of two in point rate, part of the way toward the $\dot N R^4$ of sunlight-limited detection (§C3b)."

3. **Line** 2026 — **E/A** — **medium**
   - **Quote:** "Sony's passively recharged SPADs behave paralyzably (§C5a): a SPAD is live only if no photon arrived during the last $\tau_d$."
   - **Problem:** §C5a records "The ISSCC abstract says *passive* quenching and recharge; the IMX459 press release says *active* recharge [I/P]". It infers paralyzable behaviour from the 60 Mcps ceiling as [E] and adds "The product may differ from the development chip." Subsection 10 drops all three hedges. The numerical effect is small, but not zero. A non-paralyzable SPAD here would be dead 19.6% rather than 21.6% of the time (live fraction 0.804, $\eta=0.149$). $b$ would rise to 2.94, which lifts the threshold from 15 to 16 counts (18.4 needed instead of 17.3).
   - **Proposed rewrite:** "Eq. (82) gives the dead fraction. The model treats Sony's SPADs as paralyzable [E]: the development chip's measured 60 Mcps ceiling equals the $1/(e\tau_d)$ of a paralyzable counter with passive recharge, although the IMX459 press release says active recharge (§C5a). A paralyzable SPAD is live only if no photon arrived during the last $\tau_d$. Each of the macro-pixel's nine SPADs (a 3×3 group) counts … and $f_{\rm dead}=0.216$. A non-paralyzable SPAD would be dead 19.6% of the time instead, which raises $b$ to 2.94 and the threshold to 16 counts, and changes the energy per point by a few per cent."

4. **Line** 1968 — **A** — **low**
   - **Quote:** "written as an area; the report's scripts use it throughout (§C10.3b)."
   - **Problem:** §C10.3b documents only its own script, `coherent_mode_coverage.py`. It also restates the same relation as Eq. (146), and §C7b restates it as Eq. (101). The pointer neither supports "throughout" nor tells the reader that the later equation numbers are the same relation.
   - **Proposed rewrite:** "This is the monostatic link equation of Piggott et al. (Waymo) [P], written as an area. §C7b (Eq. (101)) and §C10.3b (Eq. (146)) restate it, and the report's scripts use it throughout."

5. **Line** 2157 — **A** — **low** (amends earlier finding 17)
   - **Quote:** "while the footprint's share of a fixed angular cell shrinks as $1/R$ (§C10.3a)."
   - **Problem:** The pointer is correct, but §C10.3a item 3 gives the explicit expression. Citing it makes the sentence self-contained.
   - **Proposed rewrite:** "…while the beam covers a share $\pi w^2/(R\theta)^2=2\lambda/(R\theta^2)$ of a cell of angular pitch $\theta$, which shrinks as $1/R$: 4.1% at 100 m for 0.05° (§C10.3a, item 3)."

#### New consistency flags

a. **Efficiencies (substantive).**
   - §C10.3a item 7 (~6350) uses ToF optics 0.5 × PDE 0.35 = 0.175, with no dead-time factor, giving 86 mm².
   - For FMCW it uses QE 0.8 × 1 dB each way ≈ 0.50, giving 14.5, 32 and 41 mm² at 100, 200 and 300 m, and concludes "about 2–6×".
   - Subsection 10 (10.1, 10.4, 10.8) and §C7a use 0.145 and 0.25, and call 0.25 "at the optimistic end" of measured chains (0.057–0.17).
   - With subsection 10's values the per-look ratio is about 3.5–10× (71 mm² against 7.2, 15.9 and 20.5 mm²). §C10.3a's FMCW efficiency is twice the report's own optimistic design value.

b. **"Optimum diameter" means two things.**
   - §C10.3a item 3's table and item 7 ("Confocal optimum (≈14 mm at 100 m, ≈22 mm at 250 m)") give the beam diameter $2w_0$, about 31 mm at 500 m.
   - §C0 10.2/10.4 and §C10.3b give the aperture $D_{\rm opt}=w_0/0.45$: about 16 mm at 100 m, 22 mm at 200 m, 35 mm at 500 m.
   - So "≈22 mm" is the 250 m optimum in one section and the 200 m optimum in the other.

c. **$N_{\rm sp}$ has two meanings.**
   - Subsection 10 (10.1 at ~1905, 10.3 at ~2039) uses it for the number of looks summed.
   - §C10.3a item 2 (~6170, "one coherent mixer uses of order $1/N_{\rm sp}$ of the aperture power") and §C10.3b Result 1 ("6.2 / 3.3" speckles for the matched 20 mm aperture) use it for speckle modes across one aperture.
   - A reader could take "3–6 speckles" as 3–6 looks, which would contradict 10.3's single-look fading. Use a separate symbol in §C10.3a/b, and say that a single-mode receiver still fades like one look.

d. **$t^2$ and the 0.45 ratio.** §C10.3b gives $t^2=0.837$ (~6437) and $t^2=0.84$ (~6453); subsection 10.2 uses 0.838. §C10.3b calls 0.45 "a model choice" (~6388), while §C0 10.2 derives it as the far-field optimum.

e. **One equation, three numbers.** Eq. (33) = Eq. (101) in §C7b = Eq. (146) in §C10.3b. The collimated ceiling $\lambda R/4$ is likewise restated in §C10.3b and as Eq. (103) in §C7b.

f. **Paralyzable claim stated without hedge elsewhere.** §C4b (~3356, "A passively recharged SPAD such as Sony's is paralyzable"), §C6(d) (the Eq. (82) text) and §C7a(a) (~4689, "Its passive recharge behaves paralyzably") all drop §C5a's hedge. Hedge them consistently with §C5a.

g. **The same wrong §E12 pointer appears in two more places.** Subsection 1 (~1558, "its return falls as $1/R^4$ (§E12)") and §C3b (~3125, "so the return falls as $1/R^4$ (§E12)") should point to §E11.3, Eq. (169).

h. **$N_s$ and $\eta$ notation differs across sections.**
   - $N_s$ is "signal photoelectrons a point needs" in §C3b's Eq. (62), "detected photons per pulse" in subsection 1's Eq. (23), and "photons in the LO's mode" in subsection 2.
   - §C3b's $\eta_{\rm opt}\eta_{\rm det}$ (with $\eta_{\rm det}$ = PDE) omits the dead-time live fraction that subsection 10's $\eta$ includes.

### §C4, §C4b, §C4c (wavelength, SiPM vs SPAD, eye safety, sunlight, InGaAs, Ge)

The whole block (lines 3254–3633, §C4, §C4b and §C4c) was read. Five cross-checks were not finished: the source for Falcon K's 30 W, the source for the 2–5% front-side SPAD PDE, the Telesca, Vines and Liu values against the original papers, the MicroVision details in §C3a, and the Sources URL list at line 3632.

#### 1. Overall assessment

Each section opens with its question and a short answer, and most estimates show the equation, inputs and substitution. Tables are followed by "Terms in the table" paragraphs, equations run (63)–(68) in order, there are no `\(`/`\[` delimiters, and currency is written `\$`. I recomputed about 60 substitutions and almost all are correct, so the problems are mostly about consistency and readability, not arithmetic. The three systemic problems are:
- **Key numbers and definitions disagree** within the block and with §C3, §C4d and §C6. Examples: the 17.5% $C_4$ caveat, the ATX channel count, "905 nm = EEL", the 244 vs 16.7 mm² InGaAs area, and the solar background rates.
- **§C4 re-derives what §C4c derives**, and the copies have drifted apart: 17.1 vs 16.4, 8 vs 7.85 mJ, 145 vs 125 K, 17.49% vs 17.5%.
- **Symbols are defined late, or reused with different meanings.** $\alpha$ has three meanings, "count rate" in Eq. (65) is wrong for a paralyzable SPAD, "time base" has two meanings, the sweep rate is written in words, and "§2" looks like a section reference. There are also several paragraph-length bullets and vague hedges.

#### 2. Findings (most severe first)

1. **Line** 3263 (with 3285 and 3432) — **A/B** — **high**
   - **Quote:** "That alone does not confer 17.49% more power in every scan or pulse regime, because other rules (pulse-train and average-power limits) may bind first."
   - **Problem:** In the report's own §C4c table, every near-IR limit scales by exactly 1.175: 198→233 nJ, 79→93 nJ and 1.00→1.18 mW. So the pulse-train and average-power rules cannot "bind first" and remove the gain. Line 3285 calls the gain "one simplified single-pulse calculation", and line 3432 says "it applies wherever $C_4$ enters". That is three different statements of one caveat.
   - **Proposed rewrite (3263):** "Every Class 1 limit this report uses between 700 and 1,050 nm (single pulse, pulse train via $C_5$, and long-exposure average power; table in §C4c) contains $C_4$, so a 940 nm design may emit 17.5% more than an otherwise identical 905 nm design whichever rule binds. This is a gain in permitted emission, not in range or signal-to-noise ratio [E]."
   - **Proposed rewrite (3285, last sentence):** "The 17.5% higher emission limit (item 1) is the only intrinsic eye-safety gain of 940 nm; the system-level advantage also depends on PDE, filter width and the emitters available."
   - If the author means a rule that does not scale with $C_4$, it should be named. Use 17.5%, 2.570 and 3.020 throughout, not 17.49%, 2.5704 and 3.0200.

2. **Line** 3528 — **B** — **high**
   - **Quote:** "An IMX479-sized 244 mm² focal plane (the 12.2 × 20.0 mm Sony SPAD chip of §C5a) would cost ≈\$250–2,500 in processed InGaAs"
   - **Problem:** In a hybrid sensor only the photosensitive array is made of InGaAs. §C6 (line 4231) puts IMX479's active array at ≈16.7 mm² inside the 244 mm² chip, so this overstates the InGaAs area about 15×. That inflates the "\$250–2,500 vs \$17–44" contrast and the verdict's "10–100× silicon" at line 3629.
   - **Proposed rewrite:** "**For arrays it matters a great deal.** An InGaAs array with IMX479's active area (≈16.7 mm², 105 × 1,568 pixels at 10.08 µm pitch, §C6) would cost ≈\$17–170 in processed InGaAs at 1–10 €/mm² ($16.7\ {\rm mm^2}\times1$–$10$ €/mm², taking €1 ≈ \$1) [E]. That comes on top of a silicon readout chip of roughly the size and cost of the ≈\$17–44 Si SPAD die (§C5a), and of hybridization (bump-bonding the two chips pixel by pixel). Per mm², processed InGaAs costs 10–100× the silicon."

3. **Line** 3627 (with 3388) — **B** — **high**
   - **Quote:** "**905 nm** (EELs) is the incumbent for the Hesai AT/ATX and RoboSense M series."
   - **Problem:**
     - §C3 (line 2530) lists Hesai AT/ATX as "905 | VCSEL + SiPM". §C3 (2531) and §C4 (3294) put RoboSense M3 at 940 nm.
     - So line 3388's definition ("'905 nm' here means … edge-emitting lasers") does not fit the best-selling 905 nm lidar, and the "EEL drift forces wide filters" argument does not apply to it.
   - **Proposed rewrite:** "**905 nm** is the incumbent: edge-emitting lasers in the RoboSense M1/MX and VCSEL columns in the Hesai AT128/ATX (§C3). It has higher silicon absorption than 940 nm but more sunlight. Where the source is an EEL, its drift … forces wide filters." At 3388: "…served mostly by multi-junction EELs and also by 905 nm VCSEL arrays (Hesai AT128/ATX, §C3)." If §C3 is the one that is wrong, correct §C3 instead.

4. **Line** 3358 (with 3314) — **B** — **high**
   - **Quote:** "The ATX uses 64 physical channels and multiplies effective lines by laser addressing"
   - **Problem:**
     - Line 3314 gives "17 SiPM dies × 4 channels", which is 68, not 64.
     - §C4d (3651, 3674) and §C3b (3040) call the ATX a 256-channel lidar.
     - "Channel" is the very unit §C4b defines (3316), yet the reader cannot tell whether the ATX has 64, 68 or 256.
   - **Proposed rewrite:** Change cell 3314 to "**ATX (17 SiPM dies, 64 receive channels [T])**", or explain how 17 × 4 gives 64. Change cell 3358 to "The ATX has 64 physical receive channels; laser addressing gives each four lines, which is how Hesai counts 256 channels (§C3b, §C4d)." If four lines per channel is not the real mapping, state the actual one.

5. **Line** 3343 — **A** — **medium**
   - **Quote:** "where $r$ is the per-SPAD count rate (s⁻¹) and $\tau_d$ the dead time (s)"
   - **Problem:** For a paralyzable SPAD, Eq. (65) needs the rate at which photons *would* trigger avalanches, not the recorded count rate, which is lower ($re^{-r\tau_d}$; §C5a line 4003 separates the two). "Counting at rate $r$" at line 3339 has the same slip.
   - **Proposed rewrite:** "Exposed to a rate $r$ of photons that would trigger avalanches, it is dead a fraction … where $r$ (s⁻¹) is that rate for one SPAD (photon arrival rate × PDE; the recorded count rate is lower, $re^{-r\tau_d}$, §C5a) and $\tau_d$ the dead time (s). Eq. (65) is the paralyzable form of Eq. (82) (§C6(d))."

6. **Line** 3470 — **A** — **medium**
   - **Quote:** "Eye safety is therefore not the binding limit on FMCW point rate; heat and wall-plug efficiency"
   - **Problem:** The next sentence says the model's 11 W at 300 m exceeds the 9.1 W allowance, which contradicts this.
   - **Proposed rewrite:** "At 200 m, eye safety therefore does not limit FMCW point rate up to 25 Mpts/s: the §C7a model needs 3.0 W at 10 Mpts/s and 7.6 W at 25 Mpts/s against the 9.1 W allowance, and heat and wall-plug efficiency (…) bind first (§C7a). At 300 m and 25 Mpts/s, however, the model's 11 W would exceed the allowance for this field (§C7b subsection 2(i))."

7. **Line** 3296 — **A** — **medium**
   - **Quote:** "and as the natural band for FMCW (frequency-modulated continuous-wave, coherent) lidar."
   - **Problem:** The paragraph is headed "Where 1,550 nm ToF survives", but FMCW is not ToF. "MicroVision ex-Luminar" is telegraphic, and "450 m at 10%" has no tag.
   - **Proposed rewrite:** "**Where 1,550 nm survives.** Pulsed time-of-flight (ToF) lidar at 1,550 nm survives where long range is worth its price: at NIO (Seyond Falcon K3, 450 m at 10% [P]), in trucks and off-road vehicles, and in defence and very long range (AEye; MicroVision, which bought Luminar's lidar business, §C3a). Separately, 1,550 nm is the natural band for FMCW (frequency-modulated continuous-wave, coherent) lidar (§C4c subsection 4)."

8. **Line** 3269 (with 3264 and 3287) — **A** — **medium**
   - **Quote:** "the absorption coefficient is $\alpha\approx3.1\times10^2$ cm⁻¹ at 905 nm ($1/\alpha\approx32$ µm)"
   - **Problem:** Within §C4, $\alpha$ is the apparent source angle (3264), then silicon's absorption coefficient (3269), then water's (3287).
   - **Proposed rewrite:**
     - Use $\alpha_{\rm Si}$ at 3269: "$\alpha_{\rm Si}\approx3.1\times10^2$ cm⁻¹ … ($1/\alpha_{\rm Si}\approx32$ µm)".
     - Use $\alpha_{\rm abs}$ at 3287, as §C4c subsection 5 does.
     - Optionally make "thin" concrete: "[E: an assumed 3 µm absorber captures $1-e^{-3/32}\approx9\%$ at 905 nm and $1-e^{-3/56}\approx5\%$ at 940 nm in one pass]".

9. **Line** 3264 — **B** — **medium**
   - **Quote:** "the tabular ratio is $(10/1.002)(1550/905)=9.98\times1.713\approx17.1$"
   - **Problem:** §C4c gives the same photon ratio as 16.4 (line 3454, from 9.6 mW), and treats 10 mW only as the "commonly quoted" table entry (3430). Here 10 mW is tagged [P/E]. Similarly, 3265 says 8 mJ where §C4c says 7.85 mJ.
   - **Proposed rewrite:** "Adjusted for photon energy, the ratio is ≈16–17: $(9.6/1.00)\times1.713=16.4$ from the 9.6 mW that 1 kW m⁻² gives over a 3.5 mm aperture, or $(10/1.002)\times1.713=17.1$ from the rounded 10 mW table entry (§C4c)."

10. **Line** 3455 (and table row 3446) — **B** — **medium**
    - **Quote:** "The ratio is $1{,}000/26.0=38.4$, which the table rounds to 39×; in photons it is $38.4\times1.713=66$ (67 from the rounded 39×)."
    - **Problem:** 38.4 rounds to 38, not 39, so the table's 39× and 67× are each one too high.
    - **Proposed rewrite:** "The ratio is $1{,}000/26.0=38.4$, shown as 38×; in photons it is $38.4\times1.713=66$." In the table row: "**38×** | 66× | IEEE Spectrum's "40 times more powerful" (the same ratio, rounded) [T]".

11. **Line** 3358 — **B** — **medium**
    - **Quote:** "Scales on chip, from 520 to 2,160 channels per die, because timing and histogramming sit under the pixels"
    - **Problem:** §C6 (4229) and §0 (159) call 520 and 2,160 effective line counts that may involve binning or interleaving, "not a single-die channel-count sequence". §C8 (5499) shows 2,160 rows of 3-SPAD macro-pixels would be ≈65 mm long.
    - **Proposed rewrite:** "Scales on chip: published effective line counts reach 520 (IMX479) and 2,160 per receiver chip, though the larger figures may involve binning or interleaving (§C6). Timing and histogramming sit under the pixels and data are compressed on chip; the limits are the reticle and memory (§C6)."

12. **Line** 3499 — **B/A** — **medium**
    - **Quote:** "| 905 nm, 24% efficiency, 20 nm filter | ≈1.6×10⁹ |"
    - **Problem:** §C4 item 4 (3284) and the verdict (3627) say a 905 nm EEL needs a ≈40 nm filter. The table silently gives 905 nm a 20 nm filter, which halves its background.
    - **Proposed rewrite:** Add a row "| 905 nm, 24%, 40 nm filter (EEL over −40 to +105 °C) | ≈3.2×10⁹ |". In the derivation, add: "The 20 nm row assumes a temperature-stabilised source or a 905 nm VCSEL; an EEL needs ≈40 nm (§C4 item 4), which doubles the count to $3.2\times10^{9}$ s⁻¹."

13. **Line** 3628 — **B** — **medium**
    - **Quote:** "($0.07\ {\rm nm/K}\times125\ {\rm K}=8.8$ nm over −40 to +85 °C)"
    - **Problem:** §C4 (3284) and §C6(d′) (4320) use −40 to +105 °C (145 K, ≈10 nm).
    - **Proposed rewrite:** "($0.07\ {\rm nm/K}\times145\ {\rm K}\approx10$ nm over −40 to +105 °C, §C4 item 4)".

14. **Line** 3457 — **A** — **medium**
    - **Quote:** "Over the $T_2=10$ s time base a pulse repetition frequency $f_p$ (in Hz) gives $N=10\ {\rm s}\times f_p$ pulses."
    - **Problem:** Line 3412 defines the "time base" as the exposure duration the classification assumes, and $T_2$ separately as the counting time (3422). Here $T_2$ is called the time base. Line 3265's "standard's reference time" is a third name for the same thing.
    - **Proposed rewrite:** "Over the counting time $T_2=10$ s, a pulse repetition frequency $f_p$ (the PRF, in Hz) gives $N=10\ {\rm s}\times f_p$ pulses." At 3265, write "within $T_2$ (10 s; §C4c)".

15. **Line** 3326 — **A** — **medium**
    - **Quote:** "A given cell then receives a Poisson-distributed number of photons with mean $\bar n/N_c$, and fires with probability $1-e^{-\bar n/N_c}$."
    - **Problem:** $\bar n$ and $N_c$ are used here but defined only after Eq. (64), at line 3330.
    - **Proposed rewrite:** Open the paragraph with: "**Saturation.** Let a channel have $N_c$ SPAD cells, and let $\bar n$ be the mean number of photons it would detect in one pulse if no cell had already fired (photons after PDE). Assume…". After Eq. (64), keep only the definition of $N_{\rm fired}$.

16. **Line** 3338 — **A/B** — **medium**
    - **Quote:** "So **dead-time blocking is negligible**."
    - **Problem:** No number supports "negligible", and SiPM microcells recover more slowly than the 6 ns used elsewhere.
    - **Proposed rewrite:** "So dead-time blocking is small [E: in the brightest §C6(d) case, $2.2\times10^{9}$ s⁻¹ over $N_c=1{,}000$ cells is $2.2\times10^{6}$ s⁻¹ per cell; with an assumed 30 ns microcell recovery a cell is dead $1-e^{-2.2\times10^{6}\times3\times10^{-8}}\approx6\%$ of the time, against 77% for a 3×3 macro-pixel]."

17. **Line** 3289 — **A/E** — **medium**
    - **Quote:** "The sweep rate is lines × frame rate ÷ parallel channels (§C4d), i.e. the number of mirror passes per second needed"
    - **Problem:** The formula is in words even though §C0 subsection 3 and Eq. (69) define it with symbols, and the sentence runs to about 70 words.
    - **Proposed rewrite:** "The required sweep rate is $S=N_{\rm lines}f_{\rm frame}/N_{\rm par}$ (Eq. (69), §C4d), where $N_{\rm lines}$ is the number of lines per frame, $f_{\rm frame}$ the frame rate (Hz) and $N_{\rm par}$ the number of lines drawn in parallel. With 128 lines, 128 channels and 10 Hz, $S=128\times10/128=10$ sweeps/s. One beam drawing an assumed 100–300 lines at 10 Hz needs $S=(100\ {\rm to}\ 300)\times10/1=1{,}000$–$3{,}000$ sweeps/s."

18. **Line** 3289 — **A** — **medium**
    - **Quote:** "optics cannot increase it, so a receiver that stares at the whole field at once must give up aperture."
    - **Problem:** The step that makes this true is missing: a detector of fixed area behind a lens of fixed f-number.
    - **Proposed rewrite:** "passive optics cannot increase it, and a detector of given area behind a lens of given f-number has a fixed étendue. A receiver that stares at the whole field at once (large solid angle) must therefore accept a small aperture (§C0 subsection 3, §C6)."

19. **Line** 3552 — **A** — **medium**
    - **Quote:** "A 1,550 nm pixel receives ≈7×10⁸ background counts/s in bright sun (§2 table)"
    - **Problem:** "§2" reads as a report section; §C2 is market share.
    - **Proposed rewrite:** "…in bright sun (subsection 2 table above)…".

20. **Line** 3600 — **A** — **medium**
    - **Quote:** "where eye safety is set by the Class 3B cap and, in Europe, A11"
    - **Problem:** Subsection 1 says automotive lidar must be Class 1 and never explains a Class 3B cap, so the reader cannot follow this.
    - **Proposed rewrite**, if this is the intended meaning: "There the retinal factor $C_7$ makes the Class 1 retinal limit so lenient that the binding limits become the cap at the Class 3B level and, in Europe, the A11 corneal limit for 1,250–1,400 nm (subsection 1)."

21. **Line** 3604 — **A** — **medium**
    - **Quote:** "Vines et al. needed 125 K for 38% at 1,310 nm, with 1,550 nm requiring ≈245 K for 1 µm-thick Ge [I]."
    - **Problem:** It does not say whether ≈245 K is a minimum or a maximum. Line 3597 implies it is a minimum.
    - **Proposed rewrite** (check the direction against the paper): "…; for 1 µm-thick Ge, detection at 1,550 nm needs operation at or above ≈245 K, because cooling moves the absorption edge below 1,550 nm [I]."

22. **Line** 3585 — **A** — **medium**
    - **Quote:** "the figure's deliberately pessimistic 125 °C dark current of 15.8 µA per diode (50 nA at 25 °C, 0.5 eV activation energy)"
    - **Problem:** 15.8 µA is not derived in the text; the scaling law appears only in the figure caption.
    - **Proposed rewrite:** Append "[E: $I_d(T)=I_d(T_0)(T/T_0)^3\exp[-(E_a/k_B)(1/T-1/T_0)]$, with $I_d(T_0)=50$ nA at $T_0=298.15$ K, $E_a=0.5$ eV and $k_B=8.617\times10^{-5}$ eV/K. At $T=398.15$ K, $(T/T_0)^3=2.38$ and $\exp[5{,}803\ {\rm K}\times(1/298.15-1/398.15)\ {\rm K^{-1}}]=e^{4.89}=133$, so $I_d\approx50\ {\rm nA}\times2.38\times133=15.8$ µA]".

23. **Line** 3600 — **D** — **medium**
    - **Quote:** "At −40 °C (233 K) a 1,550 nm receiver therefore loses a meaningful share of responsivity unless it compensates [E]"
    - **Problem:** "A meaningful share" is a vague hedge, and the previous bullet has the data to quantify it.
    - **Proposed rewrite:** "…loses roughly 40% of its responsivity unless it compensates [E: interpolating linearly between Liu et al.'s 0.87 A/W at room temperature (taken as 295 K) and 0.34 A/W at 200 K gives $0.34+0.53\times33/95\approx0.52$ A/W at 233 K]".

24. **Line** 3273 — **A** — **medium**
    - **Quote:** "The InP multiplier's ionization-coefficient ratio (the ratio of hole to electron impact-ionization rates) is $k\approx0.4$–0.5 (vs about 0.02 for Si)."
    - **Problem:** In InP, holes ionize more readily than electrons, so hole/electron is about 2–2.5; the 0.4–0.5 figure is electron/hole. §C0 Eq. (25) (line 1665) uses the same wording.
    - **Proposed rewrite:** "The InP multiplier's ionization-coefficient ratio $k$ (the weaker-ionizing carrier's impact-ionization coefficient over the stronger one's: electron/hole in InP, where holes start the avalanche; hole/electron in Si) is $k\approx0.4$–0.5, against about 0.02 for Si."

25. **Line** 3256 — **C** — **medium**
    - **Quote:** "the other six factors (detectors, sources, sunlight, water, scanning and cost) favour 905/940 nm with silicon (numbers in §C4c)"
    - **Problem:** §C4 says its numbers are in §C4c but re-derives most of them, and the copies have drifted:
      - $C_4$: 3263 vs 3436;
      - the 2007/2014 pulse limits and the 2.6 factor: 3265 vs 3411 and 3433;
      - the CW and photon ratios: 3264 vs 3454;
      - the photons-per-joule explanation: 3264, 3283, 3441 and 3492;
      - the ASTM solar numbers: 3283 vs 3480–3492;
      - water absorption: 3287 vs 3614–3620;
      - the 700× InGaAs SPAD overload: 3274, 3552 and 3629.
      Scanning numbers are in §C4d, not §C4c.
    - **Proposed restructuring:** Make §C4 a summary: one result sentence with its key number and a "§C4c subsection N" pointer per item, with the substitutions in items 1, 4 and 5 deleted. Keep the derivations only in §C4c, and define $E_{\rm ph}$ and the 1.713 factor once (3441). Change the pointer to "(numbers in §C4c, and for scanning §C4d)".

26. **Line** 3264 — **C** — **medium**
    - **Quote:** "**905 vs 1,550 nm, long exposure.** A small source is one whose apparent angular size seen from the eye is $\alpha\le1.5$ mrad (§C4c)"
    - **Problem:** The bullet is a ≈190-word paragraph. Limits, a photon conversion defined mid-sentence and three disclaimers bury the result.
    - **Proposed restructuring:** Split into three sub-bullets:
      - "the long-exposure limit is $3.9\times10^{-4}C_4C_7$ W at 905 nm ($C_7=1$), i.e. $3.9\times10^{-4}\times2.570=1.00$ mW, against ≈10 mW at 1,550 nm [P/E]";
      - "per joule 1,550 nm carries $1{,}550/905=1.713$ times the photons ($E_{\rm ph}=hc/\lambda$), so the photon ratio is ≈16–17, the scale of Luminar's '17×'";
      - "the two limits use different apertures (7 mm vs 3.5 mm), so the ratio is not a like-for-like comparison of transmitter output, scene photon flux, range or compliance."

27. **Line** 3265 — **E/A** — **medium**
    - **Quote:** "so dividing it by the 2007 near-IR entry is not a valid general comparison"
    - **Problem:** This and "should not be presented as IEC 60825-1:2014 results" read like a correction note. The reader has not been shown any such division.
    - **Proposed rewrite:** "**Pulses: the edition matters.** The 2007 edition's single-pulse limit, $2\times10^{-7}C_4$ J (0.514/0.604 µJ at 905/940 nm), was lowered in the 2014 edition to **198/233 nJ** per isolated small-source pulse, falling to **79/93 nJ** for long trains, because the per-pulse limit falls when many pulses enter the eye within $T_2=10$ s (§C4c). The 1,550 nm single-pulse limit (7.85 mJ, ≈8 mJ in the standard's table) applies to pulses up to 0.35 s; §C4c compares it with the 2014 values." At 3433, replace "should not be used (§C4)" with "was superseded in 2014".

28. **Line** 3468 — **A** — **medium**
    - **Quote:** "**905/940 nm ToF is capped at ≈10–100 nJ per pulse** (more for scanned beams, within the $C_5$ floor)."
    - **Problem:** The scanned raster gives 96/40 nJ, which is inside 10–100 nJ, not "more". "Within the $C_5$ floor" has no clear meaning.
    - **Proposed rewrite:** "**905/940 nm ToF is capped at ≈10–100 nJ per pulse**: ≈10 nJ for a stationary beam at ≥100 kHz, ≈40–96 nJ for the scanned raster of the table, and never more than the 198/233 nJ single-pulse limit."

29. **Line** 3570 (Ge photodiode table, 3566–3572) — **E/B** — **medium**
    - **Quote:** "| GlobalFoundries (O-band), OFC 2025 | 0.95 A/W | <30 nA | ≈60 GHz |"
    - **Problem:** An O-band device sits under the column "Responsivity at 1,550 nm". "Saturation 6.3 mA" is in the Bandwidth column. AIM, APSUNY and "PDs" are not expanded.
    - **Proposed rewrite:** Rename the column "Responsivity (1,550 nm unless stated)" and write "0.95 A/W (O-band, 1,310 nm)". Move "saturation photocurrent 6.3 mA" into a Notes column. Expand AIM and APSUNY, and write "18 PDs (photodiodes)".

30. **Line** 3592 — **A** — **medium**
    - **Quote:** "Rogers et al. (*Nature* 2021) reached shot-noise parity at **5 µW of LO per pixel**."
    - **Problem:** The text above derives parity at 28 µA (≈31 µW) and recommends 0.3–1 mW. The gap is never explained.
    - **Proposed rewrite:** Append "At 0.9 A/W, 5 µW gives 4.5 µA, which implies an amplifier input noise of $\sqrt{2q\times4.5\ \mu{\rm A}}\approx1.2$ pA Hz⁻¹ᐟ², about 2.5× quieter than the 3 pA Hz⁻¹ᐟ² assumed above [E]. The 0.3–1 mW used above buys margin with a discrete amplifier; it is not a physical minimum."

31. **Line** 3521 — **A** — **medium**
    - **Quote:** "[T, unattributed; internally inconsistent]"
    - **Problem:** The reader is not told what is inconsistent, so cannot tell which prices, or the per-mm² row derived from them, to trust.
    - **Proposed rewrite:** "[T, unattributed; its figures conflict: <name the conflict in one clause>; indicative only]".

32. **Line** 3373 — **E** — **medium**
    - **Quote:** "**The best-selling long-range lidar in the world, Hesai's ATX (more than 1 M delivered, under \$200), uses SiPM.**"
    - **Problem:** The rank, delivery count and price carry no tags.
    - **Proposed rewrite:** "**Hesai's ATX, by its delivery count the best-selling long-range lidar (more than 1 M delivered [P], ≈\$200 [T], §C3c), uses SiPM.**"

33. **Line** 3465 — **B** — **low**
    - **Quote:** "The ratios are $91\ {\rm µJ}/96\ {\rm nJ}\approx950$ and $18\ {\rm µJ}/40\ {\rm nJ}\approx460$."
    - **Problem:** As written, 18 µJ / 40 nJ is 450.
    - **Proposed rewrite:** "…and $18.3\ {\rm µJ}/39.6\ {\rm nJ}\approx460$ (unrounded: $9.14\ {\rm W}/500\ {\rm kHz}=18.3$ µJ; $0.4\times198/2=39.6$ nJ)."

34. **Line** 3464 — **A** — **low**
    - **Quote:** "With $C_5$ at its 0.4 floor each pair may carry 79 nJ, i.e. ≈40 nJ per pulse"
    - **Problem:** The pulse count that puts $C_5$ at its floor is not shown, and neither is the reason consecutive pulses both reach the aperture.
    - **Proposed rewrite:** Prepend: "Along a line, pulses land $209\ {\rm mm}/(5\times10^{5}\ {\rm s^{-1}}/1{,}280\ {\rm lines\,s^{-1}})=0.54$ mm apart at 100 mm, so consecutive pulses overlap the aperture. In $T_2$ the aperture receives $5\times1.09\times10^{4}=5.5\times10^{4}$ pulses, i.e. $2.7\times10^{4}$ pairs, and Eq. (66) gives $(2.7\times10^{4}/600)^{-1/4}=0.39$, below the floor, so $C_5=0.4$…".

35. **Line** 3488 (with 3484 and 3492) — **B** — **low**
    - **Quote:** "$1.44/3.16\approx0.46$, $1.44/2.10\approx0.68$ and $2.10/3.16\approx0.67$"
    - **Problem:** As shown, $1.44/2.10=0.69$ and $2.10/3.16=0.66$. Line 3492 computes 1.43×10¹⁸ but says "tabulated as 1.44×10¹⁸" without a reason.
    - **Proposed rewrite:** Show the 1,550 nm flux as $2.11\times10^{18}$ ($0.270\times7.80\times10^{18}=2.106\times10^{18}$) in the table and in 3492. All three ratios then reproduce: $1.44/2.11\approx0.68$, $2.11/3.16\approx0.67$. Add to 3492: "(the table averages $E_\lambda\lambda/hc$ nm by nm over the band, giving 1.44×10¹⁸)", if that is the reason.

36. **Line** 3284 — **B/D** — **low**
    - **Quote:** "allows 10–20 nm receive filters instead of about 40 nm, roughly halving background."
    - **Problem:** The same bullet then says a 20 nm filter halves and a 10 nm filter quarters the background.
    - **Proposed rewrite:** "…instead of about 40 nm, cutting background 2–4×."

37. **Line** 3526 — **B** — **low**
    - **Quote:** "processed InP is about 1.4–3.4 orders of magnitude (24× to 2,400×) dearer than 28 nm silicon, depending on volume"
    - **Problem:** The verdict (3629) says "10–100× silicon per mm²", against a different baseline and a different volume range.
    - **Proposed rewrite:** Add "(against the ≈\$0.1/mm² of a stacked Sony SPAD die, §C5a, the ratio at 1–10 €/mm² is 10–100×, the figure used in subsection 6)".

38. **Line** 3615 (water table, 3615–3617) — **D/E/A** — **low**
    - **Quote:** "a 0.1 mm film costs −0.47 dB one-way at 1,550 nm"
    - **Problem:**
      - "Costs −0.47 dB" is a double negative.
      - "Near-IR ≈10% worse" (fog row) does not say which band.
      - "[I, … via survey; original not read]" is [S] by the report's own tag legend.
    - **Proposed rewrite:**
      - "a 0.1 mm film costs 0.47 dB one way at 1,550 nm";
      - "905 nm ≈10% worse than 1,550 nm only in very dense advection fog (<30 m visibility)" (confirm the direction);
      - "[S, Wojtanowski et al. 2014, via a survey]".

39. **Line** 3552 — **A/B** — **low**
    - **Quote:** "about **700× the ≈10⁶ counts/s an InGaAs SPAD can sustain** with the hold-off its afterpulsing requires"
    - **Problem:** 1 Mcps corresponds to a 1 µs hold-off, which still leaves ≈8% afterpulsing (3548). Getting below 3% needs 10 µs, which gives a ceiling of ≈0.1 Mcps.
    - **Proposed rewrite:** "…can sustain with a 1 µs hold-off (which still leaves ≈8% afterpulsing; the 10 µs needed for <3% lowers the ceiling to ≈10⁵ counts/s, ≈7,000× below the sunlight rate)".

40. **Line** 3597 — **D** — **low**
    - **Quote:** "Germanium absorbs 1,550 nm light strongly only above the photon energy of its *direct band gap*, the "direct edge"."
    - **Problem:** The sentence mixes up wavelength and photon energy.
    - **Proposed rewrite:** "Germanium absorbs strongly only photons whose energy exceeds its *direct band gap*, the "direct edge"; in Ge-on-Si that edge lies just longward of 1,550 nm at room temperature."

**Polish not itemised above (exact quotes available if wanted):**
- 3258 vs 3423 give different physical reasons for $C_4$.
- 3411 and 3436 do not cite Eq. (63).
- 3422 says "for $C_5$ below", but Eq. (66) is above.
- 3302 says "During that dead time" before defining dead time; $V_{\rm bd}$ and $V_{\rm ex}$ are never used.
- 3348 says "10 µm pixels", but the 3×3 macro-pixel sets the 0.05° resolution.
- 3376 lists Huawei's 192-line unit under "500–2,000+ lines".
- 3278 has untagged Falcon power figures and nested parentheses.
- 3386 lists "four constraints", but there are five subsections.
- 3390 uses ICNIRP before expanding it.
- 3448's photon column says "×1.7" instead of 168×/21×/16.4×.
- 3437 is missing $C_4$ in the middle term.
- 3504 says Lambertian means "equally into all directions"; it means equal radiance.
- 3574 calls $2qI$ a "noise power".
- 3598 gives 0.85 vs 0.86 nm/K, and 1,600–1,625 vs 1,590 nm.
- 3604 uses PDP where the rest of the block uses PDE.
- 3530 does not explain "F-1"; 3532's "\$33 M lidar business" is ambiguous.
- 3359 (RoboSense 45%), 3363 (NE Times) and 3292–3293 (Yole tagged [S], not [MR]) need tags.
- The table at 3308 has no introductory sentence.

#### 3. Consistency flags to check elsewhere

- **ATX channels:** 3314 (17 × 4) and 3358 (64) vs §C4d 3651 and 3674 (256), §C3b 3040 (256), §C5 3870 ("17 dies / 64 channels") and §C8 5491 (17 × 4).
- **Emitter type:** §C3 2530 (Hesai AT/ATX at 905 nm, VCSEL) vs 3388 and 3627 (905 nm = EEL). RoboSense M3 is 940 nm at 2531 and 3294 vs "M series" at 905 nm in 3627.
- **Solar background for the same case:**
  - For 905 nm, 20 nm filter, ρ = 0.9: §C4c 3499 gives 1.6×10⁹ (PDE 0.24, 0.693 W m⁻² nm⁻¹); §C6(d) 4286/4296 gives 2.2×10⁹ (PDE 0.3, 0.75), and §C4b 3343 uses the latter.
  - For 940 nm, 10 nm filter, PDE 0.37: 5.7×10⁸ (3500) vs 7.31×10⁸ (§C6 4302).
  - With §C6's value, the "≈1× ceiling" at 3552 becomes ≈1.35×. One irradiance convention is needed.
- **"2,160 channels per die"** (3358) vs §C6 4229, §0 159 and §C8 5499.
- **"244 mm² focal plane"** (3528) vs the IMX479 active array of 16.7 mm² (§C6 4231).
- **Ionization ratio $k$:** the "hole to electron" wording at 3273 is also in §C0 1665 (Eq. (25)).
- **Background-rate equation:** Eq. (67) at 3506 duplicates Eq. (24) at 1645 and Eq. (81) at 4293 with different symbols ($E_\lambda$/$\Phi$ vs $E_\odot$, $\eta_{\rm det}$ vs PDE, $\rho$ vs $\rho_{\rm scene}$). Eq. (65) at 3341 duplicates Eq. (82) at 4299. Cross-reference and unify.
- **1,550 nm limits:** 10 mW [P/E] (3264) vs 9.6 mW "commonly quoted as 10 mW" (3430); 8 mJ (3265) vs 7.85 mJ (3430); photon ratio 17.1 (3264) vs 16.4 (3445, 3454).
- **Filter-drift temperature range:** −40 to +105 °C at 3284 and §C6(d′) 4320 vs −40 to +85 °C at 3628.
- **Solar ratios on different bases:** 3488 gives 940/905 = 0.46 and 1,550/905 = 0.67 in photons; §C6(d′) 4325 gives 0.44–0.58 and ≈0.35 in power. Both are right on their own basis, but each should be labelled "in photons" or "in power".
- **Mixed standard editions:** §C3a Eq. (57) at 2835 sets a 2007-edition ratio (1,064/905 ≈ 3.9) against the 2014-based "≈4×10⁴× at 1,550 nm (§C4c)". That conflicts with the caution at 3265.
- **Shot-noise symbol:** $i_n$ is a density (A Hz⁻¹ᐟ²) at 3574–3576, but $\langle i_n^2\rangle$ is a band-integrated mean square (A²) in §C0 Eq. (26).
- **Shots per point:** "≈10 low-energy shots per point" (3468) vs the Sony ISSCC sensor's ≈89 in §C0 10.8 (2446). It is consistent with §C6 4237 (≤10 at 300 m), but it needs its basis.
- **Luminar/MicroVision:** "MicroVision ex-Luminar" (3296) and "\$33 M lidar business" (3532) vs §C3 2537 ("lidar business sold to MicroVision for \$33 M").

#### Follow-up cross-checks for this block (second pass, 2026-10-03; new findings only, against the report after both edit batches)

All four checks are finished, using the report file only. Line numbers are approximate; find each item by its heading or quote. Where an unlabelled URL is matched to a paper, the match rests on its venue or ID; the paper was not opened.

**Item 3, in one line:** the Luminar figures in §C4 and §C4c (\$110 M and \$33 M, February 2026, MicroVision as buyer of the lidar business) agree with §C3a. Only the wording in finding 6 needs fixing.

#### New findings

1. **Line** ≈3295, §C4 item 3 "Source, power and heat" — **E/B** — **medium**
   - **Quote:** "Falcon K drew 30 W and K2 20 W, against about 6–10 W for 9xx-nm units (Robin E1X, Hesai ATX)."
   - **Problem:**
     - The 30 W has no source or tag anywhere in the report.
     - Everything else in the sentence is sourced elsewhere: the K2's 20 W in the §C3 notes ("The Falcon K2 datasheet gives 500 m maximum range and 20 W") and §E9 ("Seyond Falcon K2, 1550 nm lidar | **20 W** [P]"). Robin E1X 6 W is in the §C3 notes [P]; ATX 8 W [P], 10 W typical in its manual, is in §E9.
     - §C4d cites the 30 W back to §C4 ("1.75 kg, 20–30 W and fibre-laser cost (§C4)"), so the reference is circular.
     - §C3c says "One lidar is rated 6–20 W" (citing §E9), so the report's own sourced range has no 30 W unit.
   - **Proposed rewrite:** "Seyond's Falcon K2 is specified at 20 W [P, datasheet; §C3], against about 6–10 W for 9xx-nm units (Seyond Robin E1X 6 W [P], §C3; Hesai ATX 8 W, 10 W typical in its manual [P], §E9)."
     - Keep the Falcon K1's 30 W only with a source and tag.
     - Otherwise drop it, and change §C4d's "20–30 W" to "20 W (K2 datasheet [P])".

2. **Line** ≈3287, §C4 item 2 "Detectors" — **E** — **medium**
   - **Quote:** "Front-side SPADs reached only 2–5% PDE."
   - **Problem:**
     - There is no tag, source, wavelength or year, and nothing elsewhere in the report supports the figure.
     - The nearest figures read as if they conflict with it. §C4b gives "Historically about 5–10% (front-side)" for SiPMs, tagged [U]. §C0 subsection 10.8 fits published research sensors with "PDEs of 5–22%".
   - **Proposed rewrite:** "Front-side-illuminated SPADs (light entering through the wiring side) reached only about 2–5% PDE at 905/940 nm [U]."
     - Add a source if one exists.
     - If none does, write "single-digit PDE [U]" and reconcile it with §C4b's 5–10% for front-side SiPMs.

3. **Line** ≈3649, §C4c Sources line — **E** — **medium** (missing citations)
   - **Quote:** "Sources: https://webstore.iec.ch/en/publication/3587 ;"
   - **Problem:** Checking each paper the block cites against this line:
     - **Telesca et al., ISSW 2024:** probably present, as the unlabelled ISSW 2024 paper R02.1.
     - **Vines et al.:** probably the unlabelled `s41467-019-08830-w`. The block gives no venue or year, so the match cannot be confirmed from the text.
     - **Liu et al., *Micromachines* 2025:** probably the unlabelled `PMC12113715`.
     - **Rogers et al., *Nature* 2021:** there is no Nature link in this line; it appears only in Appendix 2. The unlabelled `arXiv 2008.02411` may be its preprint.
     - **GlobalFoundries, OFC 2025:** missing. The only OFC link is `OFC-2014-Th5C.1`, the 2014 demonstration.
     - **Wojtanowski 2014:** missing, deliberately ("original not read"). The survey that relays it is presumably the unlabelled `arXiv 2112.08936`.
     - **Also missing:**
       - Chen et al., *JAP* 2016 (no link anywhere in the report);
       - Hale & Querry and Kou (only Segelstein's data file is listed);
       - Artilux's Ge-on-Si SPAD;
       - Fudan / Zhangjiang Lab / Innolight (cannot be identified; `arXiv 2605.07343` is unlabelled);
       - the Hamamatsu G8931-20 price [T];
       - SiLC's "germanium detectors" [T].
     - The Sony IEDM 2025 Ge SPAD is covered by the "§C5a" pointer, since §C5a's Sources line carries IEDM 2025 DOIs.
   - **Proposed fix:** Add links for the GlobalFoundries OFC 2025 paper, Chen et al. *JAP* 2016, Hale & Querry, Kou, Artilux, the Fudan/Innolight paper and Rogers et al. (Nature). Tag any that cannot be linked as [U].

4. **Line** ≈3649, §C4c Sources line — **E** — **low** (unlabelled URLs)
   - **Quote:** "https://arxiv.org/pdf/2008.02411 ;"
   - **Problem:** The line is 33 bare URLs, so a reader cannot match a citation in the text to a link. §C0's Sources lines already label two of these same URLs: `s44275-025-00030-7` is "(Wang et al., SUSTech and RoboSense, Moore and More 2025)" and the jsaprev link is "(Sony automotive SPAD)".
   - **Proposed rewrite:** Use the §C0 format, "URL (Author, venue year)". For example:
     - "…/R02.1.pdf (Telesca et al., ISSW 2024)";
     - "…/s41467-019-08830-w (Vines et al., confirm)";
     - "…/PMC12113715/ (Liu et al., Micromachines 2025)";
     - "https://doi.org/10.1007/s44275-025-00030-7 (Wang et al., SUSTech and RoboSense, Moore and More 2025)";
     - "…/2023_230402/_pdf (Sony automotive SPAD)";
     - "https://arxiv.org/pdf/2112.08936 (survey relaying Wojtanowski et al. 2014)".

5. **Line** ≈3309, end of §C4 and §C4b — **E** — **medium**
   - **Quote:** "KrASIA, summarising Seyond's prospectus: the InGaAs route costs **2–3×** as much as 905 nm [T]."
   - **Problem:**
     - Neither §C4 nor §C4b ends with a Sources line.
     - That leaves these claims with no links: the KrASIA summary of Seyond's prospectus, the Yole view, the RoboSense M3 "50–70% cheaper" pitch [P], the NE Times ≈200-line cost crossover, and the power figures.
     - §G3 cites the 2–3× back to §C4 ("KrASIA's summary of Seyond's prospectus, §C4"). Every KrASIA link in the report is about another topic, so this claim has no URL anywhere.
   - **Proposed fix:** Add Sources lines at the end of §C4 and §C4b with the KrASIA article and/or Seyond's prospectus, the Yole release, the RoboSense M3 announcement, the NE Times teardown and the Seyond and Hesai datasheets. Alternatively, point each claim to the section that already carries its source, e.g. "(Falcon K2 datasheet, §C3)".

6. **Line** ≈3549, §C4c subsection 3, "Luminar's semiconductor unit" bullet — **D** — **low**
   - **Quote:** "was sold for **\$110 M** in Feb 2026, separately from its **\$33 M** lidar business [P, 10-K]."
   - **Problem:**
     - The facts match §C3a: \$110.0 M to Quantum Computing Inc. on 2 Feb 2026, and the lidar business for \$33.0 M plus \$0.2 M cure costs to MicroVision on 3 Feb 2026 [P]. The unit's contents also match §C3a's "Black Forest Engineering receivers and readout ICs … and an InP laser/photodiode unit".
     - But neither buyer is named, and "its \$33 M lidar business" reads as a valuation rather than a sale.
   - **Proposed rewrite:** "**Luminar's semiconductor unit** (InGaAs design, ROIC, lasers) was sold to Quantum Computing Inc. for **\$110 M** on 2 Feb 2026, and its lidar business separately to MicroVision for **\$33 M** (plus \$0.2 M cure costs) on 3 Feb 2026 [P, 10-K; §C3a]."

#### Consistency flags (new)

- **Falcon naming:**
  - "Falcon K" is used in §C3 ("Falcon K/K2/K3 (1550)"), §C3b ("| **Seyond Falcon K / K2** (1,550 nm ToF)") and §C4 item 3.
  - "Falcon K1" is used in §C0 subsection 7 ("Seyond's Falcon K1 uses") and three times in §C4d: "Seyond Falcon K1: its manual gives", "heavier (Falcon K1 1.75 kg [P])" and "(Falcon K1 250 m, K3 450 m)".
  - Pick one name.
- **§C4d subsection 4, polygon-plus-galvo row:** "1.75 kg, 20–30 W and fibre-laser cost (§C4)" relies on §C4's unsourced 30 W.
- **§C3c table:** "One lidar is rated 6–20 W" (citing §E9) excludes the §C4 figure of 30 W.
- **§G3:** "(KrASIA's summary of Seyond's prospectus, §C4)" points back to §C4, which has no link.
- **§G2 "Cheap exits":** "its market value briefly exceeded roughly \$10 B in late 2020 [U]" conflicts with §C3a's computed "≈\$13.5 B at the peak close of \$41.80 (8 Dec 2020)". Use the §C3a figure.
- **§B3 note 1:** "about 17× the eye-safe photon flux of 905 nm (derived in §C4 …)" is a third place that depends on §C4's 17.1, while §C4c gives 16.4 (earlier finding 9). Carry whichever wording is chosen into §B3 as well.

### §C4d (mechanical steering), §C8 (chip size and reticle), §C9 (interference)

#### Readability review: §C4d (lines 3634–3851) and §C8–§C9a (lines 5463–5732)

**Coverage:** both ranges of the block were read in full, together with the symbols and numbers it relies on in §C0, §C2, §C4, §C4b, §C6, §C7/§C7a, §C10.2b, §C10.3a and §C10.4. The two references past line 7341 are given with the +6 shift from an insertion in §D7.

##### 1. Overall assessment

The three sections are well organised. Each one opens with its question and its answer, symbols are defined next to their equations, and every display equation is tagged. Almost every substitution I recomputed is correct: Eqs. (69)–(75), the walk-off table, figures of merit (FoM), the Brosens deformation, the vibration-spectrum (PSD) integral, Miles' equation, the yield/cost table, the Eq. (126) lengths, and the Eq. (127) and (129) chains. I found no versioning language, no `\( \)` delimiters and no unescaped currency.

Three systemic problems:
- **The interference estimate changes its model between §C9 and §C9a.** §C9 says one foreign shot can add up to nine counts; §C9a counts each shot as one. Bin width goes from 0.33 ns to 1 ns, the frame from 1.25 Mpt to 2.5 Mpt, and $n$ = 10–30 is never linked to the 3–16 units §C9 says are in range today. Several inputs the conclusions rest on are stated without derivation: the 10⁻³ aligned-hit fraction, Kim's 60–125 shots/s, and the 0.1–0.5 reduction factor.
- **Some conclusions are not tied to the numbers beside them.** Examples: the 100–400 Hz slow-axis claim, low-voltage electro-optic OPAs "approaching" the reticle, the word "agree" in §C9a item 3, and the Yole 52–66% range.
- **Density and drift.** Many table cells run to several sentences, parentheticals nest, and the acronym lists in §C4d and §C8 are incomplete. Symbols and terms drift between sections ($f$ vs $f_{\rm mirror}$, PRF vs $f_p$, "GS/s" vs "100–400 MHz" digitizer, AT128 sweep 2,400 vs 1,200°/s).

##### 2. Findings (most severe first)

**1.** **Line** 5661 (and 5665) — **Category** A — **Severity** high
- **Quote:** "the Poisson probability of two foreign counts in a point is about $\bar n^2/2$, and the second then shares the first one's bin"
- **Problem:** Eq. (128) treats each foreign shot as one count. But §C9 (line 5608) says one foreign shot can put up to nine counts into one bin, so under the "2-count rule" of line 5665 a single foreign burst would already be declared a point. The text also slides from "foreign shots" (§C9) to "foreign counts", and $\bar n$ reads as the mean of $n$, the number of foreign lidars in Eq. (127).
- **Proposed rewrite:** "Let $\bar k=n\,p_1$ be the mean number of foreign *shots* per point, here 0.04–0.12 for $n=10$–30 (Eq. (127)); $\tau_{\rm bin}$ is the histogram bin width and $T_{\rm w}\approx2$ µs the per-shot histogram span. One foreign shot can fill a bin with up to nine counts (§C9), so a per-point count threshold does not reject it; what rejects it is the lack of recurrence across shots. With dither, foreign shots land uniformly and independently over the span, so the probability that two foreign shots of one point fall in the same bin is $$p_{\rm ghost}\approx\frac{\bar k^2}{2}\,\frac{\tau_{\rm bin}}{T_{\rm w}} \tag{128}$$ This is the ghost rate under a 2-of-10 shot-recurrence rule, in which a peak is accepted when it recurs in the same bin on two of the ten shots." In line 5665, replace "under a 2-count rule (a point is declared when two counts share one bin;" with "under that 2-of-10 rule (".

**2.** **Line** 5584 — **Category** A — **Severity** high
- **Quote:** "For two facing scanners they affect of order $10^{-3}$ of points per frame and saturate a few points."
- **Problem:** This figure has no derivation, inputs or tag. Yet §C9a item 5 benchmarks against it ("the right order, and possibly a few times low"), and line 5716 uses it to call the GB/T ≤0.1% limit "a lenient bar". It is also unclear whether it is per frame or per face-to-face event.
- **Proposed rewrite:** Replace it with an [E] chain that gives each value and its source:
  - the fraction of my points per frame whose pixel sees the foreign aperture;
  - times the probability that the foreign beam is aimed at my aperture during that point's 20.8 µs window;
  - times the number of pixels one saturating hit spreads over (for example Popko's ≈2.5°, about 50 × 50 pixels at 0.05°);
  - divided by the 1.25 M points per frame (§C6).

  State whether the result is per frame or per event. Then make line 5716 say explicitly whether a unit without mitigation would pass ≤0.1%.

**3.** **Line** 5665 — **Category** B — **Severity** medium
- **Quote:** "That is ≈1–9 ghosts per 2.5 Mpt frame under a 2-count rule (a point is declared when two counts share one bin"
- **Problem:** The §C6-class unit used throughout §C9 (25 Mpts/s, 20.8 µs per column) is 2,400 × 520 points at 20 fps (line 4236), so a frame is 1.25 Mpt. A 2.5 Mpt frame implies 10 Hz, which contradicts the 20.8 µs listening time.
- **Proposed rewrite:** "That is ≈0.5–4.5 ghosts per 1.25 Mpt frame, or ≈10–90 per second at 25 Mpts/s, under the 2-of-10 rule ($4\times10^{-7}\times1.25\times10^{6}=0.5$ and $3.6\times10^{-6}\times1.25\times10^{6}=4.5$), and negligible under 3-of-10 (a peak must recur in at least 3 of the 10 shots)."

**4.** **Line** 5661 — **Category** B — **Severity** medium
- **Quote:** "$\tau_{\rm bin}$ the histogram bin width (1 ns here) and $T_{\rm w}\approx2$ µs the per-shot histogram span"
- **Problem:** §C9 (line 5611) uses 5 cm bins (0.33 ns) and ±0.3 µs dither. §C9a switches to 1 ns without comment. With 0.33 ns bins, $\tau_{\rm bin}/T_{\rm w}=1.7\times10^{-4}$, and $p_{\rm ghost}$ falls threefold.
- **Proposed rewrite:** "$\tau_{\rm bin}$ the histogram bin width (0.33 ns, the 5 cm bins of §C9) and $T_{\rm w}\approx2$ µs the per-shot histogram span". Then recompute: $(0.04^2/2)\times1.7\times10^{-4}=1.3\times10^{-7}$ and $(0.12^2/2)\times1.7\times10^{-4}=1.2\times10^{-6}$. If 1 ns is intended, say why it differs from §C9.

**5.** **Line** 5666 — **Category** A — **Severity** medium
- **Quote:** "Post-rejection rates in modern units (10⁻⁵–10⁻³, or "negligible") agree."
- **Problem:** 10⁻⁵–10⁻³ is 3–2,500 times the 4×10⁻⁷–4×10⁻⁶ just derived, so "agree" is not what the numbers show. No source is given. The matching figures in §C9a (Hwang & Lee's preset 10⁻⁵, Liang's 0.11%) come from simulations, not modern units.
- **Proposed rewrite:** "Published post-rejection false-alarm rates, from $10^{-5}$ (Hwang & Lee, preset) to $1.1\times10^{-3}$ (Liang et al., 200 interferers), both simulated, lie above this random-coincidence floor. That suggests bursts, direct view or synchronized units set the residual rate, not random coincidences."

**6.** **Line** 5577 — **Category** A — **Severity** medium
- **Quote:** "from a few to perhaps 15 lidars today, depending on city and location; dozens later, as the fleet turns over."
- **Problem:** The result (line 5604) uses $n=$ 10–30 without saying which scenario that is. Today's count derived here is 3–16, and the text says "perhaps 15" against its own 16. So the claim "already at the percent level" is never shown with today's numbers.
- **Proposed rewrite:** "from about 3 to about 16 lidars today, depending on city and location, and dozens later as the fleet turns over." Start the Result bullet with: "With today's 3–16 fully overlapping §C6-class units, Eq. (127) gives 1.3–6.5% ($1-(1-4.2\times10^{-3})^{3}=1.3\%$, $1-(1-4.2\times10^{-3})^{16}=6.5\%$); with $n=$ 10–30, the later case, about 4–12%…"

**7.** **Line** 5657 — **Category** A — **Severity** medium
- **Quote:** "Applying the §C9 flux × window structure of Eq. (127) to Kim's SICK geometry (≈60–125 foreign shots/s per footprint, ≈0.53 µs window)"
- **Problem:** Neither input is derived or sourced: the scanner's shot rate, beam width and field are missing, and so is why the window is the 80 m round trip. The verdict "consistent" therefore cannot be checked. Line 5658's "Kim's central ≈4.9×10⁻⁵" is the model's prediction, but readers will take it for Kim's measurement.
- **Proposed rewrite:** After the parenthesis, add one sentence deriving 60–125 s⁻¹ from the LMS-511 shot rate × (beam width ÷ field), with sources, and say where the 80 m comes from. In line 5658, write "the model's central prediction for Kim's geometry, $\approx4.9\times10^{-5}$".

**8.** **Line** 5657 — **Category** B — **Severity** medium
- **Quote:** "Kim measured 2.6×10⁻⁵–1.7×10⁻⁴; Popko measured 2–3×10⁻⁴ scattered-only."
- **Problem:** The Measurements table (line 5636) gives Kim as 6×10⁻⁶–1.7×10⁻⁴. The check silently drops the lower arrangements, and the 85× rescaling inherits that choice.
- **Proposed rewrite:** "Kim measured 6×10⁻⁶–1.7×10⁻⁴ over all arrangements (2.6×10⁻⁵–1.7×10⁻⁴ for the arrangements comparable to this geometry, named); Popko measured 2–3×10⁻⁴ scattered-only." Alternatively, correct the table.

**9.** **Line** 5659 — **Category** A — **Severity** medium
- **Quote:** "which corresponds to a combined reduction factor of about 0.1–0.5 applied to the 4–12%"
- **Problem:** Three factors are named but only the overlap (≈¼) is quantified, so the "realistic 0.4–6%" is asserted, not derived. The text also switches to "one foreign count".
- **Proposed rewrite:** Give each factor a value range and tag, then multiply. For example (illustrative values to be replaced by the author's): overlap 0.25–0.6 (Popko's ≈¼ as the low end), in-band share 0.5–0.9 [E], spot-density factor 0.8–0.9 [E]; product $0.25\times0.5\times0.8=0.10$ to $0.6\times0.9\times0.9=0.49$. Hence "≈0.4–6% of points carry at least one foreign *shot* before rejection ($0.04\times0.1$, $0.12\times0.5$)."

**10.** **Line** 5585 — **Category** A — **Severity** medium
- **Quote:** "scattered by lens flare or the window onto other active pixels, each gets about 100× a normal return"
- **Problem:** "$10^{-5}$ of the directly received light" reads as the total scattered fraction. The 100× figure needs $10^{-5}$ to reach *each* pixel. "A normal return" is also undefined.
- **Proposed rewrite:** "Stray light is the larger risk. If lens flare or window scatter delivers even $10^{-5}$ of the directly received power to each of the other active pixels, each gets about 100× the return of a 10% Lambertian target at the same range ($10^{-5}\times10^{7}=10^{2}$)."

**11.** **Line** 5576 — **Category** A — **Severity** medium
- **Quote:** "Adding 2024 (1.53 M units, §B1), earlier years and 2026 (985k units in Q1, §B1), and assuming 4–5 M units for the whole of 2026"
- **Problem:** The pre-2024 units are not given, and the sum and the division by units per car are skipped, so 6–8 M cannot be reproduced. The ≈350 M fleet needs a tag or a source.
- **Proposed rewrite:** "Units installed through end-2026 are roughly $U_{<2024}+1.53+(3.21\text{–}3.32)+(4\text{–}5)$ M, with pre-2024 installations $U_{<2024}\approx0.5$–1 M [E] (substitute the figure actually used), i.e. 9.2–10.9 M units. At 1.3–1.6 units per car that is $9.2/1.6\approx5.8$ to $10.9/1.3\approx8.3$ M lidar cars, about 2% of a Chinese car fleet of ≈350 M [E] ($7/350=2\%$)."

**12.** **Line** 3820 — **Category** A — **Severity** medium
- **Quote:** "In practice that puts the resonance at 100–400 Hz, the most energetic part of the road spectrum."
- **Problem:** Mirrorcle's 2.0 mm quasi-static mirror at 1,300 Hz (line 3718) contradicts this. The reason the resonance cannot go higher (the FoM bound) is missing. Line 3763 ("exactly where a MEMS mirror's slow axis must resonate") inherits the overstatement.
- **Proposed rewrite:** "Raising that resonance needs stiffer springs, which cut the quasi-static angle for a given actuator (the FoM bound, Eq. (72)). Mirrors of 3 mm and more therefore sit at about 100–400 Hz (Hua's 5 mm at 136 Hz; Mirrorcle's 3–6.4 mm at 300–400 Hz), the most energetic part of the road spectrum. Only small mirrors escape it (Mirrorcle's 2 mm at 1.3 kHz), at the cost of the aperture of subsection 2(e)." In line 3763, write "…where the slow axis of a MEMS mirror of 3 mm or more resonates."

**13.** **Line** 3709 — **Category** A — **Severity** medium
- **Quote:** "That caps the chirp (the FMCW frequency sweep) at roughly the time the beam takes to cross its own width (§C7, scanner-induced Doppler)."
- **Problem:** The step from a frequency spread to a time limit is skipped. "Cross its own width" is ambiguous: it means the angular beamwidth, not the spot. No number is given.
- **Proposed rewrite:** "A spread $\Delta f\approx\Omega D/\lambda$ limits coherent integration to about $1/\Delta f=\lambda/(\Omega D)$. That is also the time the beam takes to sweep through one diffraction-limited beamwidth $\lambda/D$, and a longer chirp (the FMCW frequency sweep) is smeared. For a 5 mm beam at the Falcon polygon's 45,600°/s (796 rad/s), $\Delta f\approx2.6$ MHz and the chirp is capped near 0.39 µs (§C7, scanner-induced Doppler)."

**14.** **Line** 3669 — **Category** A — **Severity** medium
- **Quote:** "Consider a frame of $N_{\rm lines}$ lines (rows of points along the slow axis), repeated at the frame rate $f_{\rm frame}$ (Hz)"
- **Problem:** A line is drawn along the fast axis, and lines are stacked along the slow axis. As written, the definition inverts the geometry of Eq. (69) and §C0.3.
- **Proposed rewrite:** "Consider a frame of $N_{\rm lines}$ lines (rows of points, each drawn along the fast axis and stacked along the slow axis), repeated at the frame rate $f_{\rm frame}$ (Hz)"

**15.** **Line** 3688 — **Category** A — **Severity** medium
- **Quote:** "AT128 and ATX fire each channel at only 12–15 kHz (1.536 M pts/s over 128 channels and 3.84 M/256)."
- **Problem:** 12–15 kHz is a per-channel *point* rate. It equals the pulse rate only at one shot per point, an assumption 2(b) never states, while §C6 and §C9 assume ≈10 shots per point.
- **Proposed rewrite:** "AT128 and ATX measure only 12–15 kpts/s per channel (1.536 M pts/s over 128 channels and 3.84 M/256); even at several pulses per point their per-channel pulse rate stays far below Eq. (70)'s 600–750 kHz." Earlier in 2(b), after "minimum number of channels that must fire in parallel", add "(at one pulse per point; $k$ pulses per point multiply it by $k$)".

**16.** **Line** 3829 — **Category** A — **Severity** medium
- **Quote:** "≈54% of 2024 units weighted by supplier, and the basis of Yole's 52–66% rotating-mirror shares (§C2)"
- **Problem:** §C2 gives 66% for 2024 and 52% for Yole's ten-year outlook. The range "52–66%" merges a measured share with a forecast.
- **Proposed rewrite:** "≈54% of 2024 units weighted by supplier [E], against Yole's 66% for 2024 and 52% in its ten-year outlook (§C2)"

**17.** **Line** 5540 — **Category** B — **Severity** medium
- **Quote:** "draw about 1–25 mW per $\pi$ of phase shift each. The low end needs trenches or undercuts and responds more slowly (§C10.2b: 0.14 mW/π undercut"
- **Problem:** The low-end example (0.14 mW/π) is 7× below the stated range. §C10.2b tabulates 13 mW/π, not "about 20", for a standard thermal shifter. The 1–25 W total is a calculation but is tagged [U].
- **Proposed rewrite:** "draw about 0.1–25 mW per $\pi$ of phase shift each: undercut heaters reach 0.14 mW/π but respond in 200–300 µs, and standard heaters need about 13 mW/π (§C10.2b). With a mean phase of about $\pi$, 1,000 elements need roughly **0.1–25 W** of control power ($1{,}000\times0.14$–25 mW) [E]." Source the 20 mW/π figure if it is kept.

**18.** **Line** 5549 — **Category** A — **Severity** medium
- **Quote:** "Low-voltage EO OPAs are therefore among the few *transmitter* designs that genuinely approach the reticle."
- **Problem:** The area estimate (line 5547, 19–70%) uses the bipolar 8–20 mm lengths. The low-voltage cases the conclusion is about (16–24 mm and 27–40 mm) are never carried through.
- **Proposed rewrite:** "At 0–5 V (16–24 mm) the same 1,000 elements take $20\times16=320$ to $30\times24=720$ mm², 37–84% of a field; at 0–3 V (27–40 mm) they take $20\times27=540$ to $30\times40=1{,}200$ mm², 63–140%. Low-voltage EO OPAs are therefore among the few *transmitter* designs that approach or exceed the reticle."

**19.** **Line** 5536 — **Category** A — **Severity** medium
- **Quote:** "Shrinking the pitch shortens $f$ (30 → 5.7 mm) without the photon penalty it imposes on a SPAD staring array (§C6: 28.5 → 11.5 mm)."
- **Problem:** The §C6 pair is the f/1.2 entrance-aperture diameter when SPAD pitch falls from 10.08 to 4 µm (line 4420), not a focal length. Placed beside focal lengths, it reads as one.
- **Proposed rewrite:** "Shrinking the pitch shortens $f$ (30 → 5.7 mm) without a photon penalty. In a SPAD staring array the same shrink, from 10.08 to 4 µm SPAD pitch, cuts the f/1.2 entrance aperture from 28.5 to 11.5 mm, about six times less collecting area (§C6)."

**20.** **Line** 5537 — **Category** A — **Severity** medium
- **Quote:** "That is why Berkeley's array (a $f\approx5$ mm lens, since $55\ \mu{\rm m}/(0.6\times\pi/180)=5.3$ mm) samples at 0.6° with 0.05° beams"
- **Problem:** The step from "the mode must fill the pitch" to the 0.6°/0.05° ratio is missing.
- **Proposed rewrite:** "With $f=5.3$ mm ($55\ \mu{\rm m}/(0.6\times\pi/180)$), a 0.05° beam corresponds to a mode $f\theta=5.3\ {\rm mm}\times8.7\times10^{-4}\approx4.6$ µm wide in the focal plane, a twelfth of the 55 µm pitch. Berkeley's array therefore samples at 0.6° with 0.05° beams ($0.6/0.05=55/4.6=12$; §C10.4)."

**21.** **Line** 5489 — **Category** D — **Severity** medium
- **Quote:** "Above about 1k lines with 3-SPAD grouping, up to about 3k with 1-SPAD rows, at 10 µm pitch in a 33 mm field before periphery"
- **Problem:** "up to about 3k" reads as "bound up to 3k lines". The derivation uses 10.08 µm, and "3-SPAD" is §C6's "3-SPAD-high" (3×3) macro-pixel.
- **Proposed rewrite:** "Yes above about 1,090 lines with 3-SPAD-high (3×3) macro-pixels, or above about 3,270 lines with one-SPAD rows, at IMX479's 10.08 µm pitch in a 33 mm field before periphery; more lines fit at smaller pitch [E]"

**22.** **Line** 3814 — **Category** D — **Severity** medium
- **Quote:** "The line budget sets it ($f=S/2$ with $S$ from Eq. (69), 0.6–1.3 kHz for the products above"
- **Problem:** This is a ≈70-word sentence with nested parentheses. It introduces a new assumption (two beams per sweep, giving 0.6 kHz) that subsection 2(a) never uses.
- **Proposed rewrite:** "**A resonant fast axis cannot be placed at will.** The line budget sets it, $f=S/2$ with $S$ from Eq. (69): 0.94 kHz for the M1 and 1.2–1.3 kHz for InnovizOne with one beam per sweep. If two beams share each sweep in InnovizOne's 160-line, 15 Hz mode, $f=2{,}400/2/2=600$ Hz, so the products span 0.6–1.3 kHz. The frequency also drifts with temperature."

**23.** **Line** 3657 — **Category** B — **Severity** medium
- **Quote:** "Few: one to tens of coherent channels (Mobileye's ended design, 184), because each needs its own LO, balanced detector and GS/s digitizer (§C7a)"
- **Problem:** 184 is not "tens". §C3 (line 2543) and §C7a (line 4647) give 184 *lines*, not channels. LO is not expanded in §C4d.
- **Proposed rewrite:** "Few: one to tens of coherent channels (Mobileye's ended design claimed 184 lines, §C7a), because each channel needs its own local oscillator (LO), balanced detector and GS/s digitizer (§C7a)"

**24.** **Line** 3848 — **Category** A — **Severity** medium
- **Quote:** "The yellow band lies above the profile."
- **Problem:** "Above" reads as "higher PSD". In panel (a) the band actually marks frequencies above 1 kHz. Panel (d)'s shaded band is not described at all, and Mirrorcle's mirrors are 5–6.4 mm, not "5–6 mm".
- **Proposed rewrite:** "The shaded band marks frequencies above 1 kHz, where the Test IV profile has no energy." In (d), add "The shaded band marks sweep rates that need a kHz-class resonant mirror." Write "Mirrorcle's 300–350 Hz quasi-static 5–6.4 mm mirrors".

**25.** **Line** 3734 — **Category** A — **Severity** low
- **Quote:** "A 905 nm ToF beam 0.05–0.1° wide tolerates more, because deformation tilts reflected rays by roughly $10\,\delta_{\max}/D$ [E, order of magnitude]."
- **Problem:** The "because" clause does not explain why. The real reason is that the beam is far wider than its diffraction limit.
- **Proposed rewrite:** "A 905 nm ToF beam is 0.05–0.1° wide, several times the 0.01° diffraction limit of a 5 mm mirror ($\lambda/D=0.18$ mrad). What matters is therefore not wavefront error against $\lambda/10$ but whether deformation tilts reflected rays by a sizeable fraction of the beam width; that tilt is roughly $10\,\delta_{\max}/D$ [E, order of magnitude]."

**26.** **Line** 3801 — **Category** A — **Severity** low
- **Quote:** "95 rev/s is what the ≈380 sweeps/s of subsection 2(a) require from a four-facet polygon ($380/4=95$; the facet count is an assumption)"
- **Problem:** 380 was already 1,520/4, where the 4 is beams. Dividing by 4 again, now facets, looks like double counting.
- **Proposed rewrite:** "95 rev/s is what the ≈380 sweeps/s of subsection 2(a), already divided by the four beams, require from a polygon with an assumed four facets, one sweep per facet ($380/4=95$)"

**27.** **Line** 5578 — **Category** A — **Severity** low
- **Quote:** "The exception is near temperature extremes, because a laser's wavelength rises with temperature"
- **Problem:** The sentence computes 927 nm but never states the consequence.
- **Proposed rewrite:** "The exception is at temperature extremes, because a laser's wavelength rises with temperature. A 905 nm edge-emitting laser (EEL) drifts by 0.27 nm/K to about 927 nm at +105 °C ($905+0.27\ {\rm nm\,K^{-1}}\times80\ {\rm K}\approx927$ nm, from 905 nm at 25 °C). That is inside any receive filter centred at 940 nm and wider than about 26 nm ($2\times(940-927)$)."

**28.** **Line** 3834 — **Category** A — **Severity** low
- **Quote:** "energy per point ≈8× that of SPAD ToF (§C7a)"
- **Problem:** The ≈8× is *electrical* energy (4.25 vs 0.54 µJ). The optical ratio in §C7a(a) is ≈3× (0.30 µJ vs 93 nJ).
- **Proposed rewrite:** "electrical energy per point ≈8× that of SPAD ToF (§C7a)"

**29.** **Line** 3678 — **Category** B — **Severity** low
- **Quote:** "so the mirror runs 100–250× slower than a single-beam 2-D mirror (10 sweeps/s against 1,000–2,560"
- **Problem:** The substitution gives 256, not 250. The range 1,000–2,560 also differs from the 1,000–3,000 used at line 3636, in §5 item 1 and in §C4 item 6.
- **Proposed rewrite:** "so the mirror runs about 100–300× slower than a single-beam 2-D mirror (10 sweeps/s against 1,000–3,000; $1{,}875/10\approx190$ for the M1 and $2{,}560/10=256$ for InnovizOne"

**30.** **Line** 3732 — **Category** B — **Severity** low
- **Quote:** "six times $\lambda/10$ at 905 nm (90 nm; $547/90.5=6.0$)"
- **Problem:** 547 nm comes from the unrounded 42.5 nm, but the 3 mm case is printed as 43 nm, and 43 × 12.9 = 555.
- **Proposed rewrite:** "$12.9\times42.5\ {\rm nm}=547$ nm ≈ **0.55 µm**, six times $\lambda/10$ at 905 nm (90.5 nm; $547/90.5=6.0$)". Print the 3 mm result as "$4.25\times10^{-8}$ m, i.e. 42.5 nm".

**31.** **Line** 3772 — **Category** A — **Severity** low
- **Quote:** "where $\gamma$ is the slope on log–log axes."
- **Problem:** The log–log slope is $-\gamma$, not $\gamma$.
- **Proposed rewrite:** "where $-\gamma$ is the slope on log–log axes (the PSD falls as $f^{-\gamma}$)."

**32.** **Line** 3818 — **Category** D — **Severity** low
- **Quote:** "It used a multichannel horizontal line laser, a 10° × 11° field and up to 29 Hz."
- **Problem:** It does not say what is 29 Hz.
- **Proposed rewrite:** "It used a multichannel horizontal line laser, a 10° × 11° field and frame rates up to 29 Hz."

**33.** **Line** 3831 — **Category** D — **Severity** low
- **Quote:** "native 10% range 110 m inside its 20° × 8° ROI (140 m with pixel summation), 60/75 m outside, at 20 klx [P]"
- **Problem:** "60/75 m" does not say which figure is which. The same table also has unexplained shorthand: "Horizon" (line 3832) is not identified as a Livox model, "64-line equivalence" is undefined, "Atlas Ultra" (line 3834) is not attributed to Aeva, and "(company claims)" stands in for a tag.
- **Proposed rewrite:** If that is the mapping: "…(140 m with pixel summation) and 60 m native (75 m with summation) outside it, at 20 klx [P]". Line 3832: "Livox's Horizon covers 60% of its field in 100 ms; the Mid-40 matches a 64-line spinning lidar's coverage only after 0.5 s". Line 3834: "Aeva's Atlas Ultra 250 m on low-reflectivity targets [P, company claims]".

**34.** **Line** 3749 — **Category** A — **Severity** low
- **Quote:** "its signal-limited factor of 0.40 applied to the ≈200 m of a one-axis unit such as the AT128 gives roughly 80 m."
- **Problem:** The text picks the signal-limited factor (80 m) over the background-limited one (0.63, ≈126 m) without saying why.
- **Proposed rewrite:** "…gives roughly 80 m with the signal-limited factor (0.40) and ≈126 m with the background-limited one (0.63). If its receive field matches its 0.4° divergence, about 16× the solid angle of a 0.1° pixel, the extra background favours the lower figure."

**35.** **Line** 3694 — **Category** E — **Severity** low
- **Quote:** "This is the ToF counterpart of the coherent lag angle in §C10.3a (item 6)."
- **Problem:** §C4d uses ToF, FMCW, LO, SPAD and VCSEL without expansion or a § pointer (lines 3651, 3657, 3694). ROI appears in the walk-off table (line 3700) before its definition (line 3707). $\Omega$ in Eq. (71) has no units, although the table uses °/s and line 3709 uses rad/s.
- **Proposed rewrite:** "This is the time-of-flight (ToF) counterpart of the coherent lag angle in §C10.3a (item 6)." After Eq. (71), add "($\Omega$ in °/s gives $\Delta\theta$ in degrees, in rad/s gives radians)". Expand FMCW, LO, SPAD and VCSEL at first use or point to §C0.

**36.** **Line** 5465 — **Category** E — **Severity** low
- **Quote:** "only architectures with one on-chip cell per look direction hit this limit at automotive resolution: staring SPAD arrays and switched FMCW focal-plane arrays."
- **Problem:** The §C8 abbreviation list omits SPAD, SPAD-SoC, FMCW, SOA, CMOS, ASIC and étendue. "ALICE ITS3 upgrade; MOSS prototype" (line 5471) is unexplained.
- **Proposed rewrite:** Add to the list: "a SPAD is a single-photon avalanche diode, and a SPAD-SoC a SPAD array stacked on its timing and histogram logic (§C5); FMCW is frequency-modulated continuous-wave lidar; an SOA is a semiconductor optical amplifier; CMOS is the standard silicon chip process; an ASIC is an application-specific integrated circuit; étendue is aperture area times accepted solid angle (§C0.3)." At line 5471, write "(the ITS3 inner-tracker upgrade of CERN's ALICE experiment; MOSS, a monolithic stitched-sensor prototype)".

**37.** **Line** 5544 — **Category** E — **Severity** low
- **Quote:** "$$L_{2\pi}=\frac{2\,V_\pi L}{\Delta V}, \tag{126}$$"
- **Problem:** Eqs. (125) and (126) sit inside bullets but start at column 0. That ends the list in most renderers and strands the indented "where…" lines. §C4d and §C9 indent theirs correctly.
- **Proposed rewrite:** Indent Eq. (125) by 2 spaces and Eq. (126) by 4 spaces, matching their bullets' content.

**38.** **Line** 5509 — **Category** C — **Severity** low
- **Quote:** "The cost per good die then scales as $A/Y$ [E]."
- **Problem:** This repeats Eq. (124), one line earlier. Similar repetition elsewhere: §C8.3's opening paragraph restates its first two bullets and §C8's introduction, and §C9's introduction (line 5568) restates the "Judgement" paragraph (line 5570).
- **Proposed rewrite:** Delete this sentence. Fold §C8.3's opening into its first bullet. Cut §C9's introductory answer to one sentence and let "Judgement" carry the detail.

**39.** **Line** 5639 — **Category** E — **Severity** low
- **Quote:** "(≈5×10⁻⁴ of points; my inference from the stated frame format)"
- **Problem:** This is the author's own estimate without an [E] tag. The Measurements table has no introductory sentence. In the Sato row, "spanning 1.5–110 m of equivalent range" is unexplained.
- **Proposed rewrite:** "(≈5×10⁻⁴ of points [E], inferred from the stated frame format)". Before the table, add "The table lists published measurements of lidar-to-lidar interference: the setup and the interfered fraction found." In the Sato row, write "randomization windows equivalent to 1.5–110 m of range (10–730 ns)".

**40.** **Line** 3844 — **Category** D — **Severity** low
- **Quote:** "What could reverse this.** A large-aperture receive-side steerer"
- **Problem:** The item is a sentence fragment with no verb.
- **Proposed rewrite:** "**What could reverse this.** Two developments could: a large-aperture receive-side steerer (a device that steers the field of view of a large receiving aperture, §C6, §C10), or MEMS mirrors with FoM of order 10 at ≥5 mm and robust closed-loop control at car cost."

##### 3. Consistency flags to check elsewhere

1. **AT128 sweep speed.** §C4d (lines 3699, 3705) uses 2,400°/s optical (1,200°/s mechanical, doubled). §C10.3a item 6 (lines 6310, 6316) uses "column sweep 120° × 10 Hz ≈ 1,200°/s" for lag and smear. One of them needs a duty-factor note: the active sweep is 50% duty, against a frame average.
2. **Digitizer.** §C4d (lines 3657, 3659) says "GS/s digitizer (§C7a)". §C8.2 (line 5551) says "100–400 MHz digitizer (§C7)", and §C7 (line 4544) says "100–400 MHz ADC path". Harmonize to something like "a digitizer for a 100–400 MHz beat, sampling at up to ≈1 GS/s".
3. **Symbols.** §C0.3 (lines 1609, 1618) writes $f_{\rm mirror}=S/2$; §C4d writes $f=S/2$ (lines 3673–3677, 3814). §C0.1 (line 1516) writes PRF; Eq. (70) writes $f_p$. §C10.3a (line 6311) uses $\omega$ for what §C0, §C4d and §C7 call $\Omega$.
4. **Kim's measured fraction:** line 5636 (6×10⁻⁶ lower end) vs line 5657 (2.6×10⁻⁵).
5. **Frame size:** §C6 line 4236 (1.25 Mpt at 20 fps) vs §C9a line 5665 (2.5 Mpt). **Bin width:** §C9 line 5611 (0.33 ns) vs §C9a line 5661 (1 ns).
6. **Thermo-optic shifters:** §C8.2 line 5540 ("about 20 mW/π", attributed to §C10.2b) vs §C10.2b table, line 5906 (13 mW/π).
7. **HDL-64E point rate:** §C4d line 3650 (up to 2.2 M pts/s, S3 spec sheet) vs §C3c line 3188 (1.3 M points/s in the 2013 entry). Name the version.
8. **ATX receive channels:** §C8 line 5491 (17 SiPM dies × 4 = 68) vs §C4b line 3358 (64 physical channels) vs §C4d line 3651 (256 channels). Reconcile 68 vs 64, and say that 256 laser-addressed lines share fewer receive channels.
9. **Mobileye 184:** "channels" in §C4d line 3657 vs "lines" in §C3 line 2543 and §C7a line 4647.
10. **Hesai 2025 volume:** §C4d line 3829 cites 1.62 M; the §B1 company table gives 1,620,406 *including* 239,273 robotics units. For the one-axis row, the 1.38 M driver-assistance (ADAS) figure fits better.
11. **"Seyond now ships mostly 9xx-nm Robin units"** (line 3830). This is true for Q2 2026 (71%, §C2 line 2515), but in 2025 Falcon outsold Robin (194.7k vs 137.8k, §C2/§B1). State the period and the figure.
12. **Falcon ROI:** §C4d line 3830 (K1: 0.09° × 0.08° in a 40° × 4.8° window) and §C3b line 3051 vs §C10.6 line 6737 (K2: 0.06° × 0.06° in a 120° × 4.8° band). Check whether these are different models.
13. **Falcon line rate:** §C4d line 3675 (1,520 lines/s [P]) vs line 9246 after the +6 shift, formerly 9240 (TechInsights, 1,500 lines/s).
14. **ATX manual date:** line 3651 says "Feb 2026 manual … A07"; the §E9 source link at line 7854 after the shift, formerly 7848, is "…A07-en-260520", uploaded May 2026.
15. **FPA image at 0.05°:** §C8 line 5495 (55 µm, 120° × 26°: 132 × 29 mm) vs §C10.4 line 6526 (53 µm, 120° × 25°: 127 × 27 mm). §C8's own 0.1° case uses 120° × 25°. Use one field.
16. **Macro-pixel naming and pitch:** §C8 says "3-SPAD", "10 µm", "30 µm"; §C6 (lines 4235, 4246) says "3-SPAD-high", 10.08 µm, 30.24 µm; §C9 says "3×3 macro-pixel".
17. **ETX two chips:** §C8 line 5489 lists the two chips as a reticle escape route, but §C6(a) line 4247 says the two-chip choice "does not by itself prove a reticle limit".
18. **Cross-reference:** §C8.3 line 5563 points to §C6 for one-axis dominance; that argument is in §C4 item 6 and §C4d.
19. **M1 frame rate (arithmetic check, not externally verified):** 125 lines at 15 Hz (line 3676) with 787,500 pts/s (line 3687) implies 420 points per line, ≈0.29° over 120°. At 10 Hz it would be 630 points (≈0.19°), with $S=1{,}250$ sweeps/s and $f=0.63$ kHz. Worth rechecking, because panel (d) and the 0.6–1.3 kHz range both depend on it.
20. **NEV definition:** §C9 line 5575 ("battery-electric and plug-in hybrid") vs §B1 ("battery-electric, plug-in hybrid and range-extended").

### §C5, §C5a, §C6 (SPAD-SoC receivers)

#### 1. Overall assessment

The whole block, lines 3852–4431, was read. Two lines cited outside it, 8723 and 8874–8881, are 6 lines lower after an insertion in §D7.

**What reads well.** Each subsection opens with the question it answers. Almost every estimate shows its equation, inputs and substitution. I recomputed about 60 substitutions: die counts, costs, dead fractions, link budget, coincidence rates, filter shift, sizing and the figure-of-merit table. All are correct to rounding except those listed below.

**Three systemic problems:**
1. **Contradictions with §C5's own classification.** Later text calls Huawei's D3 in-house. It lists the SiPM-based ATX and the Huawei 896-line (detector undisclosed) as "digital" SPAD products. It describes IMX479's threshold control in two incompatible ways and disagrees on whether a teardown exists. The §C5 Bottom line also contradicts its own Foundry check.
2. **Notation drifts from §C0.** $\Delta t$, $N_s$ (per shot or per point), $\dot N$ vs $\dot N_{\rm pts}$, $E_{\rm pt}$ vs $E_{\rm tx}$, and $n$ vs $r$ all shift. The same relations are renumbered as Eqs. (78)–(80), (82) and (83).
3. **Unsourced inputs and digressions.** Several load-bearing inputs are neither derived nor sourced: the 0.1° pixel field, $6.1\times10^8$ s⁻¹, the avalanche rates, the 54 mm² die and the Fastree3D share count. Two long digressions (Fastree3D finance; AS-DT1 vs radar) bury the sections' answers.

#### 2. Findings (most severe first)

**1.** **Line** 4187 — **Category** B — **Severity** high
- **Quote:** "Huawei's move to in-house SPAD-SoCs (D3/D5/Limera, §D1a) removes that lever."
- **Problem:** §C5 (line 3863) and §C3 (lines 2532, 3044) put Sony's IMX459 array (189 × 600) in the Huawei 192-line "L306 / D3", which §C5 calls "Very likely Sony". §D1a (line 6917) names a Huawei SoC only in "D3P/Limera" and does not mention D5.
- **Proposed rewrite:** "Huawei's newer units with in-house SPAD-SoCs (D3P and Limera, §D1a) remove that lever for those products; the 192-line L306/D3, very likely built on Sony's IMX459 (§C5), still depends on it."

**2.** **Line** 3919 — **Category** A — **Severity** high
- **Quote:** "No public evidence shows Sony dies relabeled as in-house, or Sony pixel wafers bonded to Chinese logic wafers"
- **Problem:** Pattern (a) is "Sony parts under a generic label", and the EM4-520 row says "SPAD-SoC" there means Sony's chip. The reader cannot see how "relabeled as in-house" differs, so the sentence seems to deny pattern (a).
- **Proposed rewrite:** "No public evidence shows a Sony die marked or sold as the lidar maker's own design, as distinct from pattern (a), where marketing calls an unnamed Sony part a "SPAD-SoC". Nor is there evidence of Sony pixel wafers bonded to Chinese logic wafers; Sony is not known to sell SPAD pixel wafers."

**3.** **Line** 3916 — **Category** A — **Severity** high
- **Quote:** "Neither pattern establishes foundry identity, wafer provenance (where the wafers were made) or production yield (the share of chips that work)."
- **Problem:** This contradicts line 3912 ("made in Sony's own fabs"): for pattern (a) the fab is known. The Bottom line also opens with what is unknown instead of answering the section's question.
- **Proposed rewrite:** "**Bottom line.** Some Chinese "in-house" SPAD-SoCs are Sony parts (pattern (a)), made in Sony's own fabs. The others are distinct designs (pattern (b)), whose foundry, wafer provenance (where the wafers were made) and production yield (the share of chips that work) are all undisclosed."

**4.** **Line** 4424 — **Category** B — **Severity** high
- **Quote:** ""digital" (SPAD-based) product shipping or announced keeps one moving axis (Hesai ETX and ATX, RoboSense EM4 and Phoenix units, Huawei 896"
- **Problem:** The ATX uses SiPMs (§C5 line 3870; §C4b line 3373), the analog class that "digital" is meant to exclude. §C5 (line 3864) says the Huawei 896-line's detector type is undisclosed. The same claim opens §C6 (line 4195).
- **Proposed rewrite:** "**Industry evidence:** every long-range SPAD-SoC ("digital") product shipping or announced keeps one moving axis (Hesai ETX, RoboSense EM4 and Phoenix-based units, Seyond Robin E2). So do the SiPM-based Hesai ATX and the Huawei 896-line, whose detector type is undisclosed (§C5)." Adjust line 4195 to match.

**5.** **Line** 4261 — **Category** A — **Severity** high
- **Quote:** "The detected signal photons per shot are then"
- **Problem:** Eq. (80) is evaluated with $E_{\rm pt}$, the energy per point ("0.1 µJ per point", line 4266). Its result is therefore per point, summed over the ≈10 shots of a point (line 4237).
  - §C0 Eq. (23) uses the same $N_s$ per pulse, at 100 nJ per pulse.
  - Lesson 2 (line 4354) uses ≈2–5 photons per shot.
  - The reader cannot tell which unit the 21–33 photons are in.
- **Proposed rewrite:** "The detected signal photons per point, summed over all the shots that make up the point, are then". After Eq. (80), add: "This is §C0 Eq. (23) with $T_{\rm atm}=1$ and the energy per point $E_{\rm pt}$ in place of the pulse energy $E_p$. With ≈10 shots per point, 21–33 photons per point are ≈2–3 per shot."

**6.** **Line** 4355 — **Category** A — **Severity** high
- **Quote:** "This is conceptually what IMX479's pixel-level threshold control and RoboSense's multi-threshold TDC (time-to-digital converter) do [T/I]."
- **Problem:** §C5a (lines 3942, 3962) describes IMX479's threshold control differently. There it is the comparator level at which a pulse counts as an avalanche, used to keep the dead time stable. It is not an adaptive coincidence threshold $n_{\rm th}$.
- **Proposed rewrite:** "RoboSense's multi-threshold TDC (time-to-digital converter) applies this idea [T/I]. IMX479's pixel-level threshold control is a different mechanism: it sets the comparator level at which a pulse counts as an avalanche, which keeps the dead time stable (§C5a)."

**7.** **Line** 3905 (with 3884) — **Category** B — **Severity** high
- **Quote:** "About CHF 6.7 M over 429,444 shares is ≈CHF 15–16 per share, below every 2016–20 conversion price (CHF 27–48)."
- **Problem:** Equating CHF 429,444 of capital with 429,444 shares assumes CHF 1 nominal per share, which is never stated. On that basis the share count does not close:
  - CHF 3.3 M converted at CHF 27–48 creates only ≈70k–120k shares.
  - Yet capital rose by 329,444 "mostly through six conversions" (line 3884).
  - Only four of the six conversion prices are given.
  - The step from \$7.67 M to CHF 6.7 M is not shown.
- **Proposed rewrite:** In the line 3884 row, state the nominal value and list all six conversions (date, CHF converted, shares created). Here, write: "The \$7.67 M price is ≈CHF 6.7 M at ≈0.87 CHF per dollar (December 2023) [E]. Over 429,444 shares of CHF 1 nominal, that is $6.7\times10^{6}/429{,}444\approx15.6$ CHF per share, below every 2016–20 conversion price (CHF 27–48)."

**8.** **Line** 3974 — **Category** A — **Severity** medium
- **Quote:** "**Range per time bin** is $c\,\Delta t/2$, where $c$ is the speed of light and $\Delta t$ the bin width"
- **Problem:** §C0 (lines 1503–1504) defines $\Delta t$ as the round-trip delay and $\Delta t_{\rm bin}$ as the bin width. §C6 (line 4201) also uses $\Delta t$ as the delay.
- **Proposed rewrite:** "**Range per time bin** is $c\,\Delta t_{\rm bin}/2$ (§C0, subsection 1), where $c$ is the speed of light and $\Delta t_{\rm bin}$ the bin width; the factor 2 is there because the light travels out and back."

**9.** **Line** 4229 — **Category** A — **Severity** medium
- **Quote:** "Effective lines went from 128 to 520 to 2,160 per chip; a 4,320-line system uses two chips."
- **Problem:** No devices or years are named. "128" matches no SPAD-SoC: IMX459 (2021) gives 192 lines, and 128 is the SiPM-based AT128. The next bullet's "25–41 Mpts/s" is also unattributed; 41 Mpts/s is the 2,160-beam RoboSense EM4 (§C7a line 4658).
- **Proposed rewrite:** "Effective lines per chip went from 192 (Sony IMX459, 2021) to 520 (IMX479, 2025) to 2,160 (Hesai Picasso, 2026); the 4,320-line Hesai ETX uses two chips." Then: "Point rates reach 25 Mpts/s (IMX479, §C5a) to 41 Mpts/s (2,160-beam RoboSense EM4, §C7a)."

**10.** **Line** 4277 — **Category** B — **Severity** medium
- **Quote:** "a 25 mm receive aperture, a 0.1°×0.05° field per macro-pixel, PDE 0.3, about 6 ns dead time"
- **Problem:** The IMX479 check (line 4235) sizes a 3×3 macro-pixel at 0.05° per line, i.e. 0.05° × 0.05°. The 0.1° doubles $\Omega_{\rm pix}$, and with it $r_{\rm bg}$ and every dead fraction in (d), (d′), §C0 10.3 and §C7a. No reason is given.
- **Proposed rewrite:** "a 0.1° × 0.05° field per macro-pixel: 0.05° per line, as in the IMX479 check above, and 0.1° across the scan because [state reason] [E]". Alternatively, use 0.05° × 0.05° and halve the rates.

**11.** **Line** 4343 — **Category** B — **Severity** medium
- **Quote:** "940 nm, 10 nm filter, ρ = 0.9 ($6.1\times10^8$/s)"
- **Problem:** (d) derives ≈5.9×10⁸ s⁻¹ for this case (line 4296; §C0 line 2014 gives 5.93×10⁸) and a 33% dead fraction. (d′) uses 6.1×10⁸ instead, which gives 34% (line 4356) and also scales row 1. The 4-fold ratio is "58×" in the table but "about 57–58×" in line 4349; the exact value is 57×.
- **Proposed rewrite:** Use $5.9\times10^{8}$ s⁻¹ throughout (d′). Recomputed values:

  | Case | Per-SPAD $r$ (s⁻¹) | 2-fold | 3-fold | 4-fold |
  |---|---|---|---|---|
  | 940 nm, 10 nm, ρ = 0.9 | $6.6\times10^{7}$ | $3.1\times10^{8}$ | $7.2\times10^{7}$ (8×) | $9.5\times10^{6}$ (62×) |
  | Row 1 ($1.32\times10^{8}$ s⁻¹) | $1.46\times10^{7}$ | — | $7.9\times10^{5}$ (≈170×) | $2.3\times10^{4}$ |

  At line 4356 the dead fractions become: passive 33%; active 28% (6 ns), 17% (3 ns) and 57% (20 ns).

**12.** **Line** 4107 — **Category** A — **Severity** medium
- **Quote:** "**Why about 6 × 6 SPADs per point** [E]. Four separate constraints point to the same block size:"
- **Problem:** Only items 1 (≈6 × 7) and 3 (a strip of 5–9 SPADs) point to a size. Item 2 argues only for "several" SPADs, and item 4 only against one SPAD per point. The heading's 6 × 6 also differs from item 1's 6 × 7.
- **Proposed rewrite:** "**Why several SPADs per point, about 6 × 6 to 6 × 7** [E]. Four constraints favour blocks of several SPADs; the first and third point to roughly this size:"

**13.** **Lines** 3935 and 3937 — **Category** A — **Severity** medium
- **Quote:** "the page figure is probably the active macro-pixel count; extra rows may be monitor or margin rows [E]" / "3×3 (or 6×6) macro-pixels → **192 lines**"
- **Problem:** 1,560 is a SPAD count (three SPADs for each of 520 macro-pixels), not a macro-pixel count. The second cell implies 6 × 6 also gives 192 lines. Line 4108 says 6 × 6 is the 300 m mode, which gives about 96 lines.
- **Proposed rewrite:** "the page figure is probably the number of SPADs spanned by the 520 active macro-pixels along the long axis; the other 8 may be monitor or margin SPADs [E]" and "3×3 macro-pixels → **192 lines**; 6×6 (the 300 m mode) → about 96 lines [E]"

**14.** **Line** 3856 — **Category** A — **Severity** medium
- **Quote:** "so it is a first test for a Sony part (details in §C5a)."
- **Problem:** A step is missing. The reader is not told that Sony's parts bin to characteristic counts (192 and 520 lines), which is what makes line count a test.
- **Proposed rewrite:** ""Line count" in this class is the receiver's long-axis dToF pixel count after 3 × 3 binning (grouping 3 × 3 SPADs into one ranging pixel). Sony's two automotive parts bin to 192 and 520 lines, so a product with exactly one of these counts is a first suspect for a Sony part (details in §C5a)."

**15.** **Line** 3876 — **Category** B — **Severity** medium
- **Quote:** "Hesai's SPAD IP (intellectual property, here mainly patents) comes from this spin-off of EPFL"
- **Problem:** This overstates the case. Line 3894 says Hesai "had researched SPADs since 2016". Line 3895 credits Hesai with 920 patent applications, with SPAD/SiPM detectors the largest cluster.
- **Proposed rewrite:** "Part of Hesai's SPAD IP (intellectual property, here mainly patents) comes from this spin-off of EPFL (...) and TU Delft (...), bought in late 2023; Hesai says it had also researched SPADs itself since 2016."

**16.** **Line** 4061 — **Category** A — **Severity** medium
- **Quote:** "Sony has built exactly this: the AS-DT1, a 40 m sensor that keeps only 576 points."
- **Problem:** Line 4079 says the AS-DT1 is described only as using "a SPAD sensor" and that "whether it is IMX611-class is not disclosed [U]". "Exactly this" asserts what the text later calls unknown.
- **Proposed rewrite:** "Sony has built a product of this kind: the AS-DT1, a 40 m industrial module that reports only 576 points. Its SPAD sensor is not named; the estimates below assume an IMX611-class array [U]."

**17.** **Line** 4124 — **Category** A — **Severity** medium
- **Quote:** "By this measure a Livox Mid-360 delivers about 300× the AS-DT1's points/s × $R^2$, and a Hesai AT128 or ATX automotive lidar about 10⁵×."
- **Problem:** No inputs or substitution are shown (house style 1). The numbers exist in the §C3b table (lines 3115–3121) but are not cited.
- **Proposed rewrite:** "By this measure (§C3b table), a Livox Mid-360 delivers $3.2\times10^{8}$ m²/s. That is $3.2\times10^{8}/(1\times10^{6})\approx300$ times the AS-DT1's ≈$1\times10^{6}$ m²/s (8,640 pts/s at ≈11 m outdoors on a 10% target). A Hesai AT128 or ATX delivers $6.8\times10^{10}$–$2.0\times10^{11}$ m²/s, about $10^{5}$ times."

**18.** **Line** 4385 — **Category** A — **Severity** medium
- **Quote:** "The column figure corresponds to about $2.5\times10^{8}$ avalanches/s in each of 520 macro-pixels"
- **Problem:** Neither this rate nor the $10^{7}$ s⁻¹ per VGA pixel (line 4386) is derived or tied to (d). For paralyzable SPADs the avalanche rate is the recorded rate $r\,e^{-r\tau_d}$ (Eq. (76)), not the incident rate. The headline "0.2–0.55 W" (line 4384) also disagrees with the derived 0.21–0.51 W.
- **Proposed rewrite:** "The column figure assumes about $2.5\times10^{8}$ avalanches/s per macro-pixel, close to the $3.66\times10^{8}\times0.784=2.9\times10^{8}$ s⁻¹ recorded rate of the §C7a central case (§C0 subsection 10.3) [E]." Add a basis for the $10^{7}$ s⁻¹ VGA figure, and write "0.2–0.5 W" in line 4384.

**19.** **Lines** 4325 and 4367 — **Category** B — **Severity** medium
- **Quote:** "with about 0.45–0.55× the solar irradiance of 905 nm" / "The factor 3 is in solar irradiance ($0.27/0.82\approx0.33$)."
- **Problem:**
  - Line 4325 computes 0.44 and 0.58 but states 0.45–0.55.
  - Line 4367 mixes bases. Its factor 3 uses the exact 905 nm value (0.817), but its "0.67×" photon ratio uses the ±10 nm band average (0.693; §C4c line 3488).
  - On one consistent basis the ratios are 0.33× and 0.57× (exact wavelengths) or 0.39× and 0.67× (band averages).
- **Proposed rewrite:** "with about 0.44–0.58× the solar irradiance of 905 nm". For line 4367: "On the ±10 nm band averages of §C4c, 1,550 nm has $0.270/0.693=0.39$ of the 905 nm solar irradiance, ≈2.6× less, and 0.67× the photon flux, ≈1.5× less, because each 1,550 nm photon carries less energy (0.33× and 0.57× at the exact wavelengths)."

**20.** **Line** 4020 — **Category** B — **Severity** medium
- **Quote:** "Sony's research is therefore at least level with the 45% claimed for RoboSense's 2026 chip."
- **Problem:** RoboSense's 45% has no stated wavelength (line 3868). Sony's research pixel reaches 51% at 905 nm but only 42.5% at 940 nm. "At least level" therefore holds only if RoboSense's figure is at 905 nm.
- **Proposed rewrite:** "Sony's research is therefore comparable to the 45% claimed for RoboSense's 2026 chip, whose wavelength is not stated: ahead if that figure is at 905 nm, slightly behind if it is at 940 nm."

**21.** **Line** 4155 — **Category** A — **Severity** medium
- **Quote:** ""Line mode only" and a ≈6 ns dead time tie IMX479 to one-axis scanned architectures."
- **Problem:** Line mode explains why IMX479 needs a scanner; the text never says how the dead time does.
- **Proposed rewrite:** ""Line mode only" ties IMX479 to one-axis scanned architectures. Its ≈6 ns dead time also leaves each SPAD blind for a large share of the time in bright sun (33% at 940 nm behind a 10 nm filter, §C6(d))."

**22.** **Line** 4141 — **Category** B — **Severity** medium
- **Quote:** "Geometry match (189 × 600) plus Chinese "industry analysis" [T]; no public teardown"
- **Problem:** §C5 (line 3863) attributes the 189 × 600 array to TechInsights [I], and §C3 (line 2532) to a "TechInsights teardown". "No public teardown" contradicts both unless it means no public teardown names the part.
- **Proposed rewrite:** "TechInsights' teardown found the 189 × 600 array and says this "suggests" Sony [I] (§C5); Chinese "industry analysis" names IMX459 [T]; no public teardown names the part"

**23.** **Line** 3857 (and 3858) — **Category** E — **Severity** medium
- **Quote:** "(90 nm SPAD / 40 nm logic in the ISSCC 2021 design), PDE 24% at 905 nm. Binned: about **192** lines [P]."
- **Problem:**
  - The single [P] covers the 40 nm logic node, which §C5a (line 4000) says "appears only in trade press [T]".
  - Line 3858's [P] likewise covers 3 GHz sampling, which §C5a tags [I] because the papers do not name the part.
  - PDE is not expanded at its first use in §C5.
- **Proposed rewrite:** "(90 nm SPAD wafer [I]; 40 nm logic wafer per trade press [T]), PDE (photon detection efficiency, §C5a) 24% at 905 nm [P]. Binned: about **192** lines [P]." In line 3858, tag "3 GHz equivalent-time sampling [I, §C5a]".

**24.** **Lines** 3978–3979 — **Category** A — **Severity** medium
- **Quote:** "**3.5 kcps typical, 6 Mcps maximum, per SPAD**" / "dead time 15 ns typical at 99% accumulation;"
- **Problem:**
  - A 1,700× gap between typical and maximum needs explaining: either the worst "hot" SPAD of the array, or a kcps/Mcps typo.
  - "At 99% accumulation" is unexplained.
  - 15 ns for "the same 597 × 168 array" conflicts with the ≈6 ns used in line 3942, in Eq. (76) and throughout §C6, with no sentence reconciling them.
- **Proposed rewrite:** "3.5 kcps typical and 6 Mcps maximum per SPAD (the maximum presumably being the worst SPAD of the array; check the datasheet)". Then: "dead time 15 ns typical, measured at [explain "99% accumulation"]; this is longer than the ≈6 ns of the automotive development chip, probably because of a different definition or operating point [U]."

**25.** **Line** 4360 — **Category** A — **Severity** medium
- **Quote:** "Background forms a flat floor that averages down as $\sqrt{N_{\rm shots}}$"
- **Problem:** The background floor itself grows in proportion to $N_{\rm shots}$; what falls is its relative fluctuation, as $1/\sqrt{N_{\rm shots}}$. The bullet's first sentence is also 50 words long.
- **Proposed rewrite:** "**Multi-shot time-correlated single-photon counting (TCSPC) histograms** accumulate photon arrival times over many shots. Matched filtering correlates the histogram with the expected pulse shape. Constant-false-alarm-rate (CFAR) peak detection sets the threshold from the measured noise floor, so that false alarms stay at a fixed rate. The background forms a flat floor whose relative fluctuation falls as $1/\sqrt{N_{\rm shots}}$, so the signal-to-noise ratio of the return grows as $\sqrt{N_{\rm shots}}$. Here $N_{\rm shots}$ is the number of laser shots accumulated into one histogram."

**26.** **Line** 4390 — **Category** E — **Severity** medium
- **Quote:** "NE Times: SPAD-SoC beats SiPM above about 200 lines."
- **Problem:** Item (g) is three telegraphic notes with no evidence tags. "Monolithic Phoenix" (line 4391) contradicts its own gloss, "one stacked chip".
- **Proposed rewrite:**
  - "A NE Times analysis finds SPAD-SoC receivers cheaper than SiPM receivers above about 200 lines [T]."
  - "RoboSense claims about 50% lower cost for its Phoenix, which puts the SPAD array and processing on one stacked chip rather than separate parts [P]."
  - "The SPAD wafer stays on mature (older, cheaper) process nodes, while the logic wafer moves to finer nodes for SRAM and DSP [E]."

**27.** **Line** 4354 — **Category** A — **Severity** medium
- **Quote:** "A mean of $\bar n=5$ detected photons per shot gives $1-e^{-5}\times18.5=0.88$; a mean of 2 gives only $1-e^{-2}\times5=0.32$."
- **Problem:** $n_{\rm th}=3$ is only implied, and the lesson is not tied to the report's own link budget.
- **Proposed rewrite:** Append: "For $n_{\rm th}=3$ at 200 m on a 10% target, (c) gives ≈21–33 photons per point, i.e. $\bar n\approx2.1$–3.3 per shot over the ≈10 shots of a point, so a 3-fold requirement would detect only ≈35–64% of shots."

**28.** **Line** 3866 — **Category** B — **Severity** medium
- **Quote:** "TechInsights: 0.20 MP at 10.0 µm [I]"
- **Problem:** IMX479 has 105 × 1,568 = 164,640 SPADs, i.e. 0.16 MP (line 3971). The teardown figure is ≈20% higher, yet the row concludes "Most likely IMX479" without comment.
- **Proposed rewrite:** "TechInsights: 0.20 MP at 10.0 µm [I], against 0.16 MP active for IMX479; the difference may be dummy or margin pixels counted in the teardown [U]"

**29.** **Lines** 3876 and 4116 — **Category** C — **Severity** medium
- **Quote:** "**Fastree3D: the European SPAD lineage now inside Hesai.**" / "**Against imaging radar** (§E2)."
- **Problem:**
  - The Fastree3D timeline and assessment (lines 3876–3909) are about a third of §C5. They are mostly financing history and interrupt the answer between the product table and the Foundry check.
  - The AS-DT1 material in §C5a, and its radar comparison above all, is about an industrial module, not the automotive chips the section asks about.
- **Proposed rewrite:** Keep three sentences on Fastree3D in §C5: bought December 2023 for \$7.67 M; patents booked at RMB 59.35 M; no evidence of Fastree3D circuits in a shipping chip. Move the timeline and "Was it a success?" to §C3a with a pointer. Move the radar comparison (lines 4116–4122) to §B8 or §E2, and keep the "Points cost range" result in §C5a.

**30.** **Line** 4241 — **Category** C — **Severity** medium
- **Quote:** "Seven factors, (a) to (g), limit how far the approach can go."
- **Problem:** (c) is a worked link budget for (b), not a separate limit, and (d′) is a list of mitigations. The section opener (line 4195) speaks of "four limits".
- **Proposed rewrite:** "Six factors limit how far the approach can go: (a) die size; (b) photon budget, worked through in the link budget (c); (d) sunlight, with the mitigations of (d′); (e) histogram memory; (f) avalanche power; and (g) cost. Sunlight is the dominant daytime limit. For a wide-field staring receiver, the étendue discussion further below ranks four of them as binding."

**31.** **Line** 4033 — **Category** B — **Severity** medium
- **Quote:** "The smaller IMX459 (≈54 mm² logic die) is ≈\$3–9 in silicon."
- **Problem:** The 54 mm² input has no source or [E] tag; the specification table gives no IMX459 die size. "Logic die" is confusing because in a stacked chip both dies share one footprint.
- **Proposed rewrite:** "The smaller IMX459 (stacked die ≈54 mm² [source, or E with its basis]) is ≈\$3–9 in silicon."

**32.** **Line** 4066 — **Category** A — **Severity** medium
- **Quote:** "30 fps in the 20 m and 30 m modes, 15 fps in the 30 m and 40 m modes [P, spec sheet]"
- **Problem:** The 30 m mode appears at both frame rates, while line 4068 lists only three modes.
- **Proposed rewrite:** "four mode settings: 20 m and 30 m at 30 fps, and 30 m and 40 m at 15 fps [P, spec sheet]". If the sheet does not support this, correct the duplicated 30 m.

**33.** **Line** 4314 — **Category** C — **Severity** medium
- **Quote:** "This is Eq. (81) written as a proportionality."
- **Problem:** Several numbered equations restate earlier ones under new symbols:
  - Eq. (83) restates Eq. (81) and is never cited.
  - Eqs. (78)/(79) restate §C0 Eq. (42) and §C3b Eq. (62).
  - Eq. (80) restates §C0 Eq. (23).
  - Eq. (82)'s paralyzable form is §C4b Eq. (65).
  - The symbols change: $E_{\rm pt}$ vs $E_{\rm tx}$/$E_p$, $\dot N_{\rm pts}$ vs $\dot N$, and $n$ in Eq. (76) vs $r$ in Eq. (82).
- **Proposed rewrite:** Keep the numbers to avoid renumbering, but introduce each one as "§C0 Eq. (42) [or (23), or §C4b Eq. (65)] in this section's notation". Write Eq. (76) with $r$ (rate per SPAD), and say Eq. (83) is used in Layers 1–2.

**34.** **Line** 4297 — **Category** A — **Severity** medium
- **Quote:** "Sony's passively recharged SPADs behave paralyzably (§C5a)"
- **Problem:** §C5a (line 4001) presents passive vs active recharge as an unresolved discrepancy ("The product may differ"). Here it is stated as fact, and it drives every number in the table.
- **Proposed rewrite:** "Sony's SPADs, if passively recharged as the ISSCC 2021 chip appears to be (§C5a), behave paralyzably"

**35.** **Lines** 3999 and 4375 — **Category** A — **Severity** medium
- **Quote:** "150 m on a 10% target, and 200 m at 168 × 63 and 20 fps under 117 klx." / "Sony's ISSCC 2021 receiver gives 150 m @10% at 117 klx [P] (§C5a)."
- **Problem:**
  - "168 × 63" is unexplained, and the 200 m case gives no reflectance.
  - §C6 pairs 117 klx with the 150 m figure and tags it [P], where §C5a has [T, Sony figures].
  - "Response 5–7 ns" (line 3998) is undefined.
- **Proposed rewrite:** In §C5a: "150 m on a 10% target; and 200 m with 168 × 63 depth points per frame at 20 fps under 117 klx, reflectance not stated [T, Sony figures]." In §C6: "Sony's ISSCC 2021 receiver reaches 150 m on a 10% target and 200 m under 117 klx [T, Sony figures] (§C5a)." Define "response".

**36.** **Line** 3860 (and 3871) — **Category** C — **Severity** low
- **Quote:** "| Product | Verified | Inferred / unknown |" / "**No Hesai "V-series" chip name exists**"
- **Problem:**
  - No sentence introduces the table.
  - The "Verified" column holds marketing claims (EMX: "Marketed as a digital SPAD-SoC").
  - Two SiPM units are included without saying why.
  - The "V-series" sentence rebuts a claim the reader never sees.
- **Proposed rewrite:** Before the table: "The table lists, for each Chinese product, what teardowns or vendor documents establish about its receiver and what is only inferred; Hesai's two SiPM-based units are included for contrast." Rename the column "Documented (teardown or vendor)". Rewrite the V-series sentence to name where that label appears and that Hesai's documents do not use it.

**37.** **Line** 4176 — **Category** E — **Severity** low
- **Quote:** "Sony's 37% for IMX479 is a **product PDE** at ≈3 V excess bias."
- **Problem:** ≈3 V is not disclosed. It is inferred from the 3.3 V $V_{\rm EX}$ supply (line 3966).
- **Proposed rewrite:** "Sony's 37% for IMX479 is a **product PDE**, at ≈3 V excess bias if the 3.3 V $V_{\rm EX}$ supply is the excess bias (§C5a) [E]."

**38.** **Lines** 4119 and 4361 — **Category** E — **Severity** low
- **Quote:** "$\Delta R=c/2B$" / "[U: check the references]"
- **Problem:** $c/2B$ reads as $(c/2)B$; §C7a (line 4723) writes $c/(2B)$. "[U: check the references]" is an editor's note left in the prose, with a non-standard tag.
- **Proposed rewrite:** "$\Delta R=c/(2B)$"; and "[U]", or verify the Gupta et al. CVPR/ICCV 2019 citations and tag them [I].

**39.** **Line** 4068 — **Category** C — **Severity** low
- **Quote:** "Modes to 20, 30 and 40 m from 0.3 m. Press: 40 m indoors and 20 m outdoors at 50% reflectivity, to 100 klx [T]"
- **Problem:** The Range cell is a ≈100-word paragraph of accuracy, precision and output-step data.
- **Proposed rewrite:** Make the cell "20, 30 and 40 m modes from 0.3 m; 40 m indoors and 20 m outdoors at 50% [T]". Move the outdoor figures, accuracy, precision and output step into a bullet under "Reading the table".

**40.** **Line** 3908 (and 3905) — **Category** D — **Severity** low
- **Quote:** "World-class European SPAD and TDC know-how (the lineage from Canesta to Kinect, EPFL AQUA, TU Delft) could not reach automotive scale on about \$6 M"
- **Problem:** This is a 54-word sentence. Line 3905's 48-word sentence nests three parentheticals.
- **Proposed rewrite:** "**Reading.** World-class European SPAD and TDC know-how, from Canesta and Kinect to EPFL's AQUA lab and TU Delft, could not reach automotive scale on about \$6 M. It did not die, however: a Chinese maker with volume bought it as a going concern, a functioning company rather than a liquidation, at roughly the capital invested." For line 3905: "Liquidation preferences (terms that repay some investors first in a sale) or earn-outs (later payments that depend on performance) could change this split, but none is public [U]. Without them, money invested from 2016 lost value, while founders' shares bought at par and the earliest money gained."

#### 3. Consistency flags to check elsewhere

1. **Huawei D3.** §C3 (lines 2532, 3044) and §C5 (3863) treat it as very likely Sony. §C5a (4187) calls it in-house. §D1a (6917) names "D3P/Limera".
2. **Hesai ATX detector.** It is SiPM in §C5 (3870) and §C4b (3314, 3373), but listed as a "digital (SPAD-based)" product in §C6 (4195, 4424). The channel count also varies: "17 dies / 64 channels" (3870), "17 SiPM dies × 4 channels" (3314, which is 68) and "64 physical channels" (3358).
3. **Huawei 192-line teardown.** §C3 2532 says "TechInsights teardown"; §C5 3863 cites TechInsights [I]; §C5a 4141 says "no public teardown".
4. **Dead time of the "same array".** ≈6 ns appears in 3942, Eq. (76), §C6(d) and §C0 2016; 15 ns (IMX560) in 3979 and 4109.
5. **940 nm / 10 nm background.** $5.93\times10^8$ s⁻¹ in §C0 2014 and §C6(d) 4296, vs $6.1\times10^8$ in §C6(d′) 4343, 4347 and 4356. The dead fraction is 33% at 4288 but 34% at 4356.
6. **§C4b 3339 range.** It says "dead 9–77% of the time … (§C6(d))". §C6(d) gives 33/77/95% (22/39% in 4302); 9% only follows from (d′) row 1.
7. **Symbols vs §C0.** $\Delta t$ (§C0 1503 vs 3974). $N_s$ per pulse (Eq. (23)) vs per point (Eq. (80)). $R_{\max}$ means both unambiguous range (§C0 1516) and detection range (Eq. (42), Eq. (79)). The point-rate and energy symbols differ: $\dot N$/$E_{\rm tx}$ (§C0 2138), $\dot N$/$P$ (§C3b Eq. (62)), $N_{\rm points}$/$E_{\rm frame}$ (Eq. (78)), $\dot N_{\rm pts}$/$E_{\rm pt}$ (Eqs. (79)–(80)), and $N_{\rm pt}$ (Eq. (183), now line 8729).
8. **Same example twice.** §C0 1545 has 100 nJ "per pulse" → ≈22 photons at PDE 0.25; §C6(c) 4266 has 0.1 µJ "per point" → ≈21 at PDE 0.24.
9. **Per-point background pointer.** §C5a 4015 cites "≈10⁴ background counts per point (§C6(d))", but §C6(d) gives only rates. The per-point figure (5,960) is in §C0 2018 and §C7b 4894.
10. **Central-case halving.** The reason for "half that background" (4302) appears only in §C0 2015.
11. **Silicon absorption depth.** §C5a 4022 says "several micrometres of depth (§C4)"; §C4 3269 gives $1/\alpha\approx32$ µm (905 nm) and 56 µm (940 nm).
12. **Scantinel price.** \$0.4 M (§C5 3904; §C3a 2782, plus a \$1.8 M advance) vs "about \$2.2 M" (6556).
13. **Fastree3D founding and seat.** "Sep 2013 / 2014 … incorporated in Lausanne (EPFL Innovation Park…)" (3883); "statutes 1 Jul 2013, seat Ecublens" (3884); "Sep 2013" (3891); "the seat moves to the EPFL Innovation Park" in 2024 (3892).
14. **Adaps–RoboSense start.** "2019/2020–23" (3865) vs "from 2020 until early 2023" (3914).
15. **"Parts B and D" (3909).** The MicroVision consolidation is in §B3 (653–658), §C3a (2782) and §G2 (8874–8881, now about 8880–8887), not Part D.
16. **Class 1 pointer.** 4325 points to §C4 for the 1,550 vs 905 nm Class 1 comparison; that table is in §C4c (3441 onward).
17. **EM4 field of view.** 120° × 27° (4408; §C10 6102) vs IMX479's 120° × 26° (3945), although EM4-520 is "most likely IMX479".
18. **905 nm, 20 nm filter.** The (d) table row 4286 has no laser type, while (d′) Layer 1 says a 905 nm EEL needs 40–50 nm.
19. **Power envelope.** "6.5–13.5 W" (4125, matching §C3b) vs "8–13 W electrical envelopes" (4270).
20. **PDE roadmap claim (4151).** "Products follow within 2–4 years" is supported only by the two-year 2023→2025 example, which also compares a 6 µm research pixel with a 10 µm product.

### §C7, §C7a (FMCW maturity) and §F6

#### Readability review: §C7, §C7a and §F6

**Coverage.** The whole block was read:
- §C7, lines 4432–4607;
- §C7a, lines 4608–4831;
- §F6, now lines 8739–8785 after the +6 shift. I re-read it after the shift and the text is unchanged.

Line numbers for §C7 and §C7a are unaffected by the §D7 insertion. To check symbols and numbers, I read §C0 subsections 2, 3 and 10.1–10.3, §C6(c)–(d) and §C7b subsections 1–2.

##### 1. Overall assessment

Each subsection opens with the question it answers, and most estimates show the equation, the inputs and the substitution. I recomputed about 90 substitutions: the scanner-Doppler table, the polygon bias drift, the OPA counts, Eqs. (93)–(96), the 2026/2032 summary table, the learning curve and the §F6 stopping distances. Almost all of them hold, with a few small slips.

The three systemic problems are:
1. **Consistency with the rest of the report.** §C7a's claims and model drift from §C7b and other sections. Examples are the parity conditions, the Analog Photonics FS-4S counter-example to "no vendor publishes", two meanings of "nonlinearity", and the round-trip dead time that the 10 µs dwell ignores.
2. **Quantities a reader must guess when recomputing.** Examples are per-SPAD versus macro-pixel rate, "the light alone is ≈30 W", "per pass", why $A_{\rm mode}$ depends on range, an ambiguous "these", and mechanical versus optical scan rates.
3. **Form.** There are paragraph-length bullets, telegraphic note-style bullets in the commercial status, local "§2(a)" references, equations given new numbers when they already have one, and missing or nonstandard evidence tags.

##### 2. Findings (most severe first)

**1. Line 4636 — B — high**
- **Quote:** "No FMCW vendor publishes point rate, range and power for the same configuration."
- **Problem:** The report itself gives all three numbers for Analog Photonics' FS-4S: 0.09 Mpts/s, 200 m at 10% in a 20° × 10° ROI, at 35 W, i.e. ≈390 µJ per point (§C3b line 3058; §C7b subsection 3 table, line ≈5298). The LuminWave row of this same table also fills all three columns. The bold claim and the "silence is informative" argument built on it fail as written.
- **Proposed rewrite:** "**Only one FMCW vendor publishes point rate, range and power for the same configuration: Analog Photonics, whose FS-4S datasheet gives 0.09 Mpts/s at 200 m on a 10% target in a 20° × 10° ROI at 35 W, i.e. ≈390 µJ per point [P] (§C10.2b, §C7b subsection 3). Among automotive vendors LuminWave comes closest, but its point rate is only implied by line count and frame rate.**" Also add a table row: "| Analog Photonics FS-4S (OPA) | 0.09 M pts/s (ROI); 0.4 M (base) | 200 m at 10% in a 20° × 10° ROI; 80 m over 60° × 14° | 35 W | no automotive award found (author to tag) |".

**2. Line 4809 — B — high**
- **Quote:** "Parity needs all five conditions below. Items 1–3 are engineering, item 4 is physics-limited (§C10.3a) and item 5 is commercial."
- **Problem:** By the section's own model, conditions 1–2 still give $0.30/0.30+0.08$–$0.13\approx1.1$ µJ per point. That is ≈2× the 0.54 µJ of 2026 ToF, or ≈19–20 W at 15 Mpts/s. The missing item is §C7b's third condition, an optical energy of ≈0.15 µJ per point. §C7b's short answer also lists "three things at once", so the two sections disagree in both count and content.
- **Proposed rewrite:** Add: "6. An optical energy per point near 0.15 µJ at 200 m on a 10% target, i.e. a receive efficiency $\eta$ near 0.5, or more looks per point, each with its own receiver (§C7b subsection 5). Without it, conditions 1 and 2 give $0.30\ \mu{\rm J}/0.30+(8$–$13\ {\rm mW})\times10\ \mu{\rm s}\approx1.1$ µJ per point, about 2× the 0.54 µJ of 2026 ToF." Change the lead to "all six conditions", and add one sentence mapping them onto §C7b's three.

**3. Lines 4763–4764 — A — high**
- **Quote:** "holds <100 kHz error over 1 GHz (nonlinearity $<10^{-4}$) [P]: enough at 200–250 m, marginal at 300 m by Eq. (112)"
- **Problem:** Eq. (112) allows $\delta\nu_{\max}\le c/(16R)$, which is 94 kHz at 200 m and 75 kHz at 250 m. A 100 kHz error is "enough" there only if it is peak-to-peak (±50 kHz), and the text does not say so. The next bullet then reads the integrated lasers' "nonlinearity" as the fractional chirp-rate error $\varepsilon$ (13–30× over $5\times10^{-4}$). §C7b, however, defines $\varepsilon=8\delta\nu_{\max}/B_{\rm eff}$. Read the same way, Waymo's $10^{-4}$ would pass at 300 m with a 5× margin, which contradicts "marginal". One word is carrying two different quantities.
- **Proposed rewrite:** "Waymo's thermally chirped DFB with pre-distortion keeps its frequency error below 100 kHz over a 1 GHz sweep [P]. Taken as peak-to-peak ($\delta\nu_{\max}\approx50$ kHz), it meets Eq. (112) at 200 and 250 m (94 and 75 kHz) and is marginal at 300 m (62.5 kHz) [E]." For 4764: "Bianconi et al. report 0.65% and 1.5% nonlinearity [P]. As peak deviations over a 1 GHz sweep, these are 6.5 and 15 MHz, ≈100–240× the 62.5 kHz that Eq. (112) allows at 300 m. Read as fractional chirp-rate errors $\varepsilon$, they are still 13–30× above $5\times10^{-4}$. Either way they need pre-distortion or resampling [E]." State once which definition Bianconi et al. use.

**4. Line 4767 — A — high**
- **Quote:** "At 10 Mpts/s and 300 m the light alone is ≈30 of ≈68 W of sensor power (§C7b subsection 2(h))."
- **Problem:** Read literally, this is 30 W of light, about 3× the ≈9 W eye-safety allowance stated in (b). In fact 30 W is the laser's electrical draw for the useful light (4.5 W optical at 15% wall-plug efficiency). Another ≈9 W of electrical power goes into light emitted during the round-trip dead time.
- **Proposed rewrite:** "At 10 Mpts/s and 300 m, producing the useful light alone takes ≈30 W of the sensor's ≈68 W electrical draw (4.5 W of optical power at 15% wall-plug efficiency), and light emitted during the round-trip dead time takes ≈9 W more (§C7b subsection 2(h))."

**5. Line 4692 — A — medium**
- **Quote:** "It is the antenna-theorem quantity of Eq. (90) in §C7, for a mode set by a 20 mm aperture rather than by a 0.1° cell."
- **Problem:** Eq. (90) alone gives a mode area of the order of the 20 mm aperture itself, so a reader cannot get from it to 64 mm². The 64 mm² comes from the overlap result of §C0 Eq. (33), which also explains why it changes with range: 64 mm² at 200 m here, 74.5 mm² at 250 m in the Waymo check, with no explanation given. In the same bullet, "≈6 dB below ToF" does not match the model's own ratios: 6.9 dB below its own 314 mm² aperture and 8.9 dB below the 491 mm² ToF lens.
- **Proposed rewrite:** "It rests on the antenna theorem of Eq. (90) applied to a monostatic Gaussian beam: §C0 Eq. (33) gives $A_{\rm mode}=t^2\lambda^2R^2/(2\pi w^2)$, with $w$ the beam's 1/e² radius at the target and $t^2=0.84$. The 20 mm beam ($w_0=9$ mm, Rayleigh range ≈160 m) is still spreading at 200–250 m, so $A_{\rm mode}$ depends on range: ≈64 mm² at 200 m and 74.5 mm² at 250 m. Waymo puts one mode ≈6 dB below a direct-detection receiver of the same aperture [P]; here one mode is 4.9× (6.9 dB) below the 314 mm² of its own aperture."

**6. Line 4740 — B — medium**
- **Quote:** "the live fraction 0.784 that the paralyzable form of Eq. (82) gives at this rate (the SPADs are recharging and blind 21.6% of the time)"
- **Problem:**
  - At "this rate" of $3.66\times10^{8}$ s⁻¹ per macro-pixel, Eq. (82) gives $e^{-2.2}\approx0.11$. The value 0.784 needs the per-SPAD rate $r_{\rm bg}/9$.
  - "Half the fully sunlit case" is not explained.
  - The text says §C0 derives "2.87 counts per 1 ns bin" but omits the 10 shots per point that connect it to the rate.
- **Proposed rewrite:** "the live fraction 0.784 that the paralyzable form of Eq. (82) gives at the per-SPAD rate $r=r_{\rm bg}/9=4.07\times10^{7}$ s⁻¹ (nine SPADs per 3×3 macro-pixel): $e^{-r\tau_d}=e^{-0.244}=0.784$, so each SPAD is blind 21.6% of the time". After "half the fully sunlit case", add "(a scene of reflectance ≈0.45, or a pixel half filled by bright surfaces; §C0 subsection 10.3)". Replace the 2.87 sentence with "$3.66\times10^{8}\ {\rm s^{-1}}\times1\ {\rm ns}\times10\ {\rm shots}\times0.784=2.87$ counts per bin".

**7. Line 4672 — A — medium**
- **Quote:** "Its passive recharge behaves paralyzably, since the 60 Mcps ceiling equals $1/(e\tau_d)$ (§C5a)"
- **Problem:** $\tau_d$ and "Mcps" are undefined in §C7a, and the inference from the ceiling to paralyzable behaviour is not explained. "Therefore dead 21.6%" does not follow without the per-SPAD rate. "Bright sun" (the central case) and "fully sunlit" (the high case) are used throughout §C7a without definition.
- **Proposed rewrite:** "Its passive recharge behaves paralyzably: a paralyzable counter with dead time $\tau_d$ counts at most $1/(e\tau_d)=1/(2.718\times6\ {\rm ns})=61$ Mcps (million counts per second), matching the measured 60 Mcps ceiling (§C5a, Eq. (76)). In the model's central "bright sun" case, half the background of a fully sunlit scene of reflectance 0.9 (the high case, §C0 subsection 10.3), each SPAD counts $4.07\times10^{7}$ s⁻¹ and is therefore dead $1-e^{-0.244}=21.6\%$ of the time."

**8. Line 4696 — A — medium**
- **Quote:** "Eq. (93) for one receiver with $A_{\rm mode}=74.5$ mm² (a 20 mm aperture at 250 m) and $\eta=0.25$ gives"
- **Problem:** Waymo's 50 photoelectrons assume four averaged speckles, but the check uses one receiver's area. With the §C7a design's four receivers, the same inputs give ≈0.34 µJ, outside Waymo's 0.83–1.67 µJ. Whether the check passes therefore rests on a choice the text does not explain.
- **Proposed rewrite:** Add: "One receiver is used because Waymo's four speckles come from [author: the diversity mechanism, e.g. within one aperture]; with four separate receivers, the same 50 photoelectrons would need $1.35/4\approx0.34$ µJ."

**9. Line 4493 (and table header, line 4513) — A — medium**
- **Quote:** "The frequency spread per pass is then"
- **Problem:** The previous bullet says a monostatic scanner's two passes add. The text never says whether the received beat is broadened by $\Delta f$ or by ≈$2\Delta f$. The "FFT bins spread" column silently uses the per-pass value.
- **Proposed rewrite:** After Eq. (86), state in one sentence whether the round-trip broadening is ≈$\Delta f$ (the speckle-decorrelation picture, consistent with the Blackmore criterion below) or ≈$2\Delta f$. Then label the column to match, for example "Spread $\Delta f$ (per pass; used for the round trip)".

**10. Line 4534 (table row, line 4516) — A — medium**
- **Quote:** "It places the problem at mirror speeds above about 5 kdeg/s, with "little impact" below."
- **Problem:** "Mirror speed" reads as a mechanical rate, but the table enters 5,000°/s as the optical rate $\Omega$ (twice the mechanical rate). The table also pairs it with a 5 mm beam that Aeva did not state, and the row label "Aeva's stated threshold" makes both look sourced.
- **Proposed rewrite:** Append: "The table treats this as an optical scan rate and assumes a 5 mm beam [E]; if the patent means the mirror's mechanical rate, the optical rate is 10,000°/s and the spread doubles to 0.56 MHz." Relabel the row "Aeva's threshold read as optical rate; 5 mm beam assumed [E]".

**11. Line 4544 — A — medium**
- **Quote:** "each with its own 100–400 MHz ADC path: at a 10 µs dwell"
- **Problem:** "100–400 MHz" could be a beat bandwidth or a sample rate; §C7a samples a 400 MHz beat at 1.23 GS/s. The 10 µs dwell also silently means 5 µs chirps, half the 10 µs chirp of the example just above, so the beat at 300 m becomes 400 MHz, not 200 MHz.
- **Proposed rewrite:** "each digitizing 100–400 MHz of beat bandwidth (sampled at ≈2.5× the highest beat plus Doppler, ≈1.2 GS/s for 5 µs chirps at 300 m, §C7a(c)). At a 10 µs dwell, i.e. a 5 µs up-chirp plus a 5 µs down-chirp, whose beat at 300 m is 400 MHz rather than the 200 MHz of the 10 µs example above,"

**12. Line 4743 — A — medium**
- **Quote:** "A 4 µs dwell cuts these by a factor of 2.5, to 8, 40 and 100, but $f_s$ and ADC energy rise"
- **Problem:** "These" follows the receiver counts (80, 400 and 1,000), but 8, 40 and 100 are channel counts.
- **Proposed rewrite:** "A 4 µs dwell cuts the channel counts by a factor of 2.5, to 8, 40 and 100 channels (32, 160 and 400 receivers), but $f_s$ and ADC energy rise"

**13. Lines 4747–4750 — A — medium**
- **Quote:** "Waymo says this makes 360°, 10 Hz spinning "impractical for target ranges much above 100 m""
- **Problem:** Walk-off is filed under "bounds the minimum dwell", but it bounds the scan rate, not the dwell. The Waymo claim is not tied to the lag-versus-beam numbers that §C10.3a already has. The next bullet's real conclusion is left implicit: above ≈1.2 mm, the minimum dwell is longer than the maximum.
- **Proposed rewrite:** Use three bullets:
  - "**Physics bounds the minimum dwell:** one round trip, 1.67 µs at 250 m."
  - "**Walk-off bounds the scan rate.** For a 360°, 10 Hz spin ($\Omega=62.8$ rad/s) the lag $2R\Omega/c$ is 0.0024° at 100 m and 0.006° at 250 m, against a 0.0036° beam (§C10.3a), which is why Waymo calls it "impractical for target ranges much above 100 m" [P]."
  - Keep the maximum-dwell bullet and end it with: "For any wider beam the minimum dwell already exceeds the maximum, so no chirp length works without digital compensation (cf. §C7b subsection 2(g))."

**14. Line 4754 — A — medium**
- **Quote:** "plus **≈50–100 mW of dedicated optical power**. The central model gives"
- **Problem:** The bold lead number is the high case or a longer range, not the central 30 mW. §C7b subsection 2(h) puts the optimum at ≈30–40 mW per channel.
- **Proposed rewrite:** "plus its own CW optical power: **≈30 mW per channel** in the central model at 200 m ($0.30\ \mu{\rm J}/10\ \mu{\rm s}$), rising to ≈50–90 mW in the high-energy case (0.88 µJ, 88 mW) or at 250–300 m (47 and 68 mW, since the energy scales as $R^2$)."

**15. Lines 4761–4762 — A — medium**
- **Quote:** "The laser must sweep ≈1.1–1.9 GHz continuously and without mode hops, in ramps of ≈4–16 µs repeated as a 30–120 kHz triangle."
- **Problem:** Nothing says why the sweep exceeds the 1 GHz that 15 cm needs; the reason is the round-trip overhead of Eq. (110). The ranges also merge the ≤30 mW case with the 100 mW case, so "0.7–4.4×10¹⁴ Hz/s … at ≤30 mW" is wrong at its upper end.
- **Proposed rewrite:** "The laser must sweep more than the 1 GHz that 15 cm needs, because the first round trip $\tau=2R/c$ of each ramp yields no usable beat (Eq. (110)): 1.14–1.27 GHz in 9.5–16 µs ramps at ≤30 mW per channel, and 1.89 GHz in 4.25 µs ramps at 100 mW (§C7b subsection 2(g)), repeated as a 30–120 kHz triangle." In the next line, write "$0.7$–$1.3\times10^{14}$ Hz/s at ≤30 mW per channel ($4.4\times10^{14}$ Hz/s at 100 mW)".

**16. Line 4813 — B — medium**
- **Quote:** "Integrated sub-100 kHz lasers with ≤$10^{-4}$ chirp nonlinearity, qualified to automotive grade."
- **Problem:** Subsection (f) asks for ≤18–55 kHz for a 1–3 dB loss at 300 m; 100 kHz costs 5.5 dB, i.e. ×3.5 energy. Subsection (f) also calls a $10^{-4}$-class chirp marginal at 300 m. This parity condition is therefore looser than the section's own requirement.
- **Proposed rewrite:** "3. Integrated lasers with linewidth ≤55 kHz (≤3 dB coherent loss at 300 m; ≤83 kHz at 200 m, Eq. (115)) and a residual chirp error inside Eq. (112) (≤62.5 kHz at 300 m), qualified to automotive grade."

**17. Line 4614 (also lines 4786 and 4788) — E — medium**
- **Quote:** "With the lower FMCW efficiencies measured so far (§2(a)), the 2026 gap is ≈10–13× for a discrete fibre chain"
- **Problem:** Bare "§2(a)", "§3 table" and "(§2(c))" look like report-level sections and collide with "§C0 subsection 2". §C7b cites the same items as "§C7a(a)".
- **Proposed rewrite:** Use "(subsection 2(a) below)", "the subsection 3 table", "Eq. (93), subsection 2(a)" and "(subsection 2(c))". Adopt one report-wide form, for example "§C7a subsection 2(a)".

**18. Line 8758 — B — medium**
- **Quote:** "\$200 ToF lidar at 25–40 Mpts/s (million points per second)"
- **Problem:** No product in the report combines both:
  - ≈\$200 is Hesai's ATX, at 3.84 Mpts/s.
  - 41 Mpts/s is RoboSense's EM4, with no price given.
  - 45% PDE is RoboSense's claimed, unverified Phoenix chip (§C5).
  
  The same untagged performance bar appears at line 4606.
- **Proposed rewrite:** "ToF keeps raising the bar on price and performance: Hesai's ATX sells for ≈\$200 at 3.84 Mpts/s [P/T], RoboSense's 2,160-beam EM4 reaches 41 Mpts/s [P] (§C7a subsection 1), and SPAD photon detection efficiency (PDE, the probability that an arriving photon is detected) is 37% in the §C7a model, with 45% claimed for RoboSense's Phoenix [P, unverified] (§C5)."

**19. Line 8761 — B — medium**
- **Quote:** "the time one channel must stay on a point (about one chirp). Tens of parallel LO-matched channels on one PIC"
- **Problem:** Eq. (89) and §C7a set the dwell as an up-chirp plus a down-chirp, ≈10 µs. "Tens" of channels give only 2–4 Mpts/s, whereas §C7a(d) needs 100–250 channels for 10–25 Mpts/s.
- **Proposed rewrite:** "…one up-chirp plus one down-chirp (≈10 µs in §C7a; Eq. (89)). Hundreds of parallel LO-matched channels on one PIC (Voyant's Helium direction) would remove the dwell-time penalty: 10–25 Mpts/s needs 100–250 channels, i.e. 400–1,000 receivers (§C7a(d))."

**20. Line 8777 — A — medium**
- **Quote:** "So ADC (analog-to-digital converter) and DSP (digital signal processing) power per channel sets how many channels fit in a 10–15 W sensor power envelope."
- **Problem:** The conclusion is not tied to numbers the report already has. "10–15 W" conflicts with the "8–25 W" in Figure C7a. In the §C7a design, each channel digitizes with four receivers.
- **Proposed rewrite:** "ADC (analog-to-digital converter) and DSP (digital signal processing) energy therefore sets how many channels fit in a power envelope. In the §C7a central 2026 model, one channel's four receivers draw ≈0.22 W ($2.23\ \mu{\rm J}/10\ \mu{\rm s}$). After the 3 W overhead, a 10–15 W sensor therefore holds ≈30–55 channels even with free light (3–5.5 Mpts/s), and supports only ≈1.6–2.8 Mpts/s once the light is paid for [E]."

**21. Line 8767 — C — medium**
- **Quote:** "The coherence-length rule of thumb gives about $\Delta\nu\lesssim160$ kHz at 300 m, from the condition that the coherence length exceed the round trip:"
- **Problem:** The bullet leads with, and gives an equation number to, a bound that the report calls the edge of detectability rather than a design point. A skimming reader takes away 160 kHz instead of 18–55 kHz.
- **Proposed rewrite:** "The linewidth requirement comes from the coherent loss of Eqs. (114)–(115): holding it to 1–3 dB at 300 m needs $\Delta\nu\approx18$–55 kHz (§C7b subsection 2(e)). The coherence-length rule $L_c=c/(\pi\Delta\nu)\ge2R$ allows ≈160 kHz but keeps only $e^{-2}\approx14\%$ of the beat in the coherent peak (8.7 dB), so it marks the edge of detectability, not a design point."

**22. Lines 8747, 8769 and 8775 — E — medium**
- **Quote:** "$$f_b=\frac{2BR}{cT} \tag{186}$$"
- **Problem:** §F6 gives new numbers to relations that already have one:
  - Eq. (186) is Eq. (85).
  - Eq. (184) is the stopping distance, already Eq. (11), Eq. (162) and Eq. (170).
  - Eq. (185) restates the §C7 coherence condition, which has no number in §C7 although §C7b cites "§C7, Eq. (185)".
- **Proposed rewrite:** In §F6, cite "Eq. (85)" and "Eq. (11), §A6.1" instead of displaying the equations again. Number the coherence condition where §C7 first states it, and cite that number from §C7b and §F6.

**23. Line 4740 — C — medium**
- **Quote:** "The fixed term follows the calibration: 1–2 W for an IMX479-class chip at 25 Mpts/s is 40–80 nJ per point including events"
- **Problem:** The "ToF is event-driven" bullet is a ≈330-word paragraph that mixes the result, the inputs, the calibration and the low/high cases. This sentence calibrates the 70 nJ total, events included, not the 40 nJ fixed term it names.
- **Proposed rewrite:** Split it into sub-bullets: the result; the event count and its inputs; the energy, $40\ {\rm nJ}+5{,}990\times5\ {\rm pJ}=70$ nJ; the calibration ("The 70 nJ total sits inside the 40–80 nJ per point that a 1–2 W IMX479-class chip implies at 25 Mpts/s; Sony's 1.19 W gives 48 nJ"); and the low and high cases.

**24. Lines 4461–4466 — D — medium**
- **Quote:** "**SiLC:** Eyeonic line; 1 km claims; Honda investment."
- **Problem:** Several commercial bullets are telegraphic notes (also LightIC, "Moore Photonics: claims only.", LuminWave), and most have no evidence tag.
- **Proposed rewrite:** "**SiLC** sells its Eyeonic line for industrial inspection, claims ranges up to 1 km and has an investment from Honda [P]." "**LightIC** builds its Lark at Tower Semiconductor and uses indie Semiconductor's Surya system-on-chip (SoC) [P]." "**Moore Photonics** has published claims but no product data." (Author to confirm the tags.)

**25. Line 4606 (systemic) — E — medium**
- **Quote:** "The cost bar is about **\$300–500 for trucks and L3** and about **\$200 for passenger L2++**"
- **Problem:** Several claims carry no tag:
  - this cost bar, and "(40 Mpts/s, 45% … PDE)" after it;
  - "≈15–30% system wall-plug efficiency" (line 4710);
  - "DFBs reach tens of kHz" (line 4760);
  - the line-count race "in five years" (line 4753);
  - the cumulative volumes $10^7$ and $10^4$ (line 4799, needs [E]);
  - the Aurora Gen 2/Fabrinet, Aumovio, Jabil, Scantinel, Baraja and Quanergy bullets.
  
  Some tags are also nonstandard: "[P, search]" for a negative search (line 4802), "[T, snippet]" (line 4658), and "(a vendor claim)" with no tag (line 4564).
- **Proposed rewrite:** Write "… **\$200 for passenger L2++** [E]" (or give the source), and "(41 Mpts/s for RoboSense's EM4 [P], §C7a subsection 1; 45% PDE claimed for RoboSense's Phoenix [P, unverified], §C5)". Tag the other items listed. Use "[E, search]" or "[U]" for "none found".

**26. Line 4498 — B — low**
- **Quote:** "the velocity estimate blurs by $\approx\Omega D/2$, the rim speed of the illuminated mirror"
- **Problem:** $\Omega D/2=\omega D$ is the difference between the two edges' velocities along the beam. Each edge moves at half that.
- **Proposed rewrite:** "the velocity estimate blurs by $\approx\lambda\Delta f/2=\Omega D/2=\omega D$, the difference between the velocities of the footprint's two edges projected on the beam"

**27. Line 4531 — A — low**
- **Quote:** "A 1 kHz, ±15° MEMS mirror centred to 0.2 mm ($\bar s=0.2$ mm): up to ±0.57 m/s, oscillating at the scan frequency."
- **Problem:** ±15° is the mechanical amplitude, while the table's MEMS row says ±30° optical. The reader cannot tell this is the same mirror.
- **Proposed rewrite:** "A 1 kHz MEMS mirror swinging ±15° mechanically (±30° optical, the table's MEMS row), centred to 0.2 mm ($\bar s=0.2$ mm), shows a false velocity of up to ±0.57 m/s that oscillates at the scan frequency."

**28. Line 4537 — A — low**
- **Quote:** "This is the frequency-domain face of the walk-off (§C7a, §C10.3a), the lateral offset between where the beam points when the light returns"
- **Problem:** §C0 subsection 2 lists walk-off and scanner Doppler as two separate errors. Walk-off is an angle, $2R\Omega/c$, not a lateral offset, and the two effects are bounded by different times.
- **Proposed rewrite:** "Scanner-induced Doppler is the companion of walk-off (§C0 subsection 2, §C7a(d), §C10.3a). Both compare the angle the beam turns with its width $\lambda/D$: walk-off over the round trip $2R/c$, Doppler spreading over the chirp $T_c$ (Eq. (87))."

**29. Line 4554 — D — low**
- **Quote:** "Matching areas does not guarantee strong response at square-cell corners."
- **Problem:** The sentence is cryptic. The next sentence calls a 1 mm diameter an "area", and nothing links it to the 20 mm, 64 mm² design that §C7a uses.
- **Proposed rewrite:** "Matching the mode's solid angle to the cell's does not make its response uniform: a round, Gaussian-shaped mode responds weakly near the corners of a square cell." Then: "The 1 mm diameter (0.8 mm²) is an illustrative size for a mode that fills a 0.1° cell. §C7a takes the other branch: a 20 mm aperture with $A_{\rm mode}\approx64$ mm² whose beam covers ≈2% of a 0.05° cell (§C7b subsection 1(b))."

**30. Line 4693 — A — low**
- **Quote:** "with four averaged speckles at a $10^{-6}$ false-alarm probability, and finds that 10–30 photoelectrons give only ≈50% [P]; 50 is the one-ramp figure"
- **Problem:** Waymo's $10^{-6}$ is per bin, whereas the report's rule is per point. The comparison of 50 with 88 is too compressed to follow.
- **Proposed rewrite:** "…at a $10^{-6}$ false-alarm probability per frequency bin… [P]. Waymo's 50 requires the peak in one ramp only; the report's rule gives 47 for that case and 88.5 when the peak must appear in both ramps (§C0 subsection 10.3)."

**31. Line 4805 — B — low**
- **Quote:** "Mobileye (exited 2024), Insight LiDAR (bankruptcy 2024), Baraja (IP sale 2025) and Scantinel (insolvency 2025) [P/T]; details under §C7 Commercial status."
- **Problem:** Insight LiDAR is covered in §C3a, not in §C7 Commercial status. Quanergy's 2022 Chapter 11 is missing from a list headed "since 2022".
- **Proposed rewrite:** "Quanergy (Chapter 11, 2022), Mobileye (exited 2024), Insight LiDAR (Chapter 11, 2024), Baraja (IP sale 2025) and Scantinel (insolvency 2025) [P/T]; details under §C7 Commercial status and, for Insight LiDAR, §C3a."

**32. Line 8749 (and lead at line 8745) — B — low**
- **Quote:** "$29.2\times1.5+29.2^2/(2\times3.5)\approx44+122=165$ m and $44+29.2^2/(2\times2.0)\approx44+213=257$ m [E]"
- **Problem:** 44 + 122 = 166, not 165. The lead says "165–255 m" while the substitution gives 257 m.
- **Proposed rewrite:** Use $v=29.17$ m/s: "$43.8+121.5=165$ m and $43.8+212.7=256$ m [E]", and write "≈165–256 m" in the lead, in §E6 and in §E12.

**33. Line 4719 — A — low**
- **Quote:** "The model samples at $f_s\approx2.5(f_b+f_D)$, where $f_s$ is the ADC sample rate and $f_b$ is taken at the maximum range $R_{\max}$."
- **Problem:** The optical budget is set at 200 m but digitization at 300 m, and the text never says why.
- **Proposed rewrite:** Add: "The receiver must search the whole 0–300 m window even when the design target is at 200 m, so $R_{\max}=300$ m sets the digitization while 200 m sets the optical energy."

**34. Line 4567 — A — low**
- **Quote:** "In this simple array model the steering angle $\theta_{\rm s}$, measured from the array normal, stays free of grating lobes for"
- **Problem:** At $d=1.5$ µm a grating lobe always exists somewhere. Eq. (91) gives the field that stays free of grating lobes, not the absence of lobes.
- **Proposed rewrite:** "In this simple array model the field $\pm\arcsin(\lambda/2d)$ about the array normal is free of grating lobes: while the main beam steers to any $\theta_{\rm s}$ inside it, the nearest grating lobe stays outside (reaching the opposite edge when $\theta_{\rm s}$ reaches the edge), so"

**35. Line 4587 — B — low**
- **Quote:** "has a nearly **8 mm transmit aperture** ($8{,}192\times1\ \mu{\rm m}=8.2$ mm): near a centimeter, but below a conventional single field"
- **Problem:** 8.2 mm is just over 8 mm, not "nearly" 8 mm, and the field size is not given.
- **Proposed rewrite:** "has an **≈8.2 mm transmit aperture** ($8{,}192\times1\ \mu{\rm m}=8.2$ mm), well inside one ≈26 × 33 mm reticle field (§C6(a))"

**36. Line 4776 (also lines 4664 and 4709) — E — low**
- **Quote:** "| Optical energy per point | 93 nJ | 0.30 µJ | 81 nJ | 0.19 µJ |"
- **Problem:** Units are mixed within one row and within the (a) heading. "1550 nm" and "1,550 nm" alternate, even inside paragraph (b).
- **Proposed rewrite:** "| Optical energy per point (µJ) | 0.093 | 0.30 | 0.081 | 0.19 |"; heading "≈93 nJ for ToF against ≈300 nJ (0.30 µJ) for FMCW"; "1,550 nm" throughout (lines 4489, 4572, 4584, 4707, 4709).

**37. Line 4616 — D — low**
- **Quote:** "**Automotive product maturity: probably, in a narrower segment.**"
- **Problem:** Subsection 6 gives ≈50–60%, which is about even odds rather than "probably".
- **Proposed rewrite:** "**Automotive product maturity: about even odds by 2030 (≈50–60%, subsection 6), in a narrower segment.**"

**38. Line 4627 — C — low**
- **Quote:** "*Product markers* show published point rate and power."
- **Problem:** This bullet belongs to panel (a) but sits at the same level as (a)–(c). "(b) Central energy breakdown." does not say what is broken down. The ETX and LuminWave derivations appear three times (lines 4629–4630, 4652 and 4657).
- **Proposed rewrite:** Nest the product markers under (a). Say in (b) what the breakdown shows, as in the figure. Keep each derivation once, in the subsection 1 list, and point to it from the caption.

**39. Line 4445 — D — low**
- **Quote:** "An Aurora "observer" has nevertheless ridden in the cab since May 2025, when truck maker Paccar asked for a person back on board"
- **Problem:** This is a 43-word sentence with a nested clause. "About 25 driverless trucks" and "\$80 M annualized revenue" in the same bullet are untagged.
- **Proposed rewrite:** "Since May 2025, however, an Aurora "observer" has ridden in the cab: truck maker Paccar asked for a person back on board less than three weeks after the first driverless runs. Aurora still counts these as driverless miles [T, NYT, 17 Mar 2026]." Tag the truck count and the revenue target.

**40. Line 8750 (also line 8756) — D — low**
- **Quote:** "Any lidar places a static return in-lane and above the road surface."
- **Problem:**
  - "Places" reads as if the lidar puts the return there.
  - The L3 substitution stops at "≈54+95 m" without the result.
  - "therefore helps prediction" does not follow from a stopping distance.
  - L3/L4, SPAD, ToF, OPA and FFT are not expanded in §F6.
- **Proposed rewrite:** "Any lidar can locate a static return precisely enough to place it in the lane and above the road surface." For the L3 paragraph: "…$\approx54+95=149$ m. At that range a per-point velocity spares the tracker the frames it needs to estimate motion, which helps prediction and lowers latency." Expand the acronyms at first use in §F6.

##### 3. Consistency flags to check elsewhere

- **Eq. (185) location.** §C7b subsection 2(e) (line 5126) cites "§C7, Eq. (185)", but Eq. (185) is in §F6 (line 8769). The §C7 coherence condition (line 4481) has no number.
- **Stopping distance numbered four times:**
  - Eq. (11), §A6.1 (line 450);
  - Eq. (162), §E6 (now ≈7737);
  - Eq. (170), §E12 (now ≈8329);
  - Eq. (184), §F6 (line 8747).
  
  The truck value is 257 m in §F6 (line 8749) and §E6 (≈7741), but 255 m in the §F6 lead (line 8745) and §E12 (≈8339).
- **Same relation, two numbers:**
  - Eq. (93) = Eq. (97) (§C7b, line 4879).
  - Eq. (85) = Eq. (186).
  - Eq. (94) uses the full chirp $T$, while Eq. (109) uses $T_u=T_c-\tau$.
- **Round-trip dead time missing from §C7a.**
  - §C7a's 10 µs dwell at 30 mW (lines 4743 and 4754) counts all 0.30 µJ as useful. §C7b subsection 2(a)–(b) adds $2\tau$ (2.67 µs at 200 m, giving a 12.7 µs dwell and 12–35% wasted light).
  - As a result §C7b gives ≈190 channels at 15 Mpts/s (line 4847) where Eq. (89) at 10 µs gives 150.
  - Receive power per channel is ≈176 mW in §C7b versus $2.23\ \mu{\rm J}/10\ \mu{\rm s}=223$ mW in §C7a.
- **Parity conditions.** §C7a subsection 5 (lines 4809–4815) lists five conditions, with item 1 "≥100 mW per channel". §C7b's short answer (lines 4863–4867) lists three. §C7b subsection 2(h) (line 5213) puts the optimum at 30–40 mW and says 100 mW costs ≈11 W more unless the transmitter is gated.
- **Definition of $\varepsilon$.** §C7b defines $\varepsilon=8\delta\nu_{\max}/B_{\rm eff}$ (line 5083), then treats Waymo's 100 kHz over 1 GHz as $\varepsilon<10^{-4}$ (line 5087). §C7a (lines 4763–4764) inherits the inconsistency.
- **$\omega$ and $\Omega$.**
  - $\omega$ is the mechanical rate in §C7 (Eq. (88), lines 4529 and 4531) but the optical scan rate in §C10.3a item 6 (≈6313).
  - $\Omega$ is a solid angle in §C0 subsection 3 (line 1610) and in $\Omega_{\rm mode}$ of Eq. (90), but a scan rate in Eq. (86).
- **$N_{\rm samp}$.** It means ADC samples per point in Eqs. (94) and (96), but samples per frame in §C10.3a Eq. (144) (≈6232).
- **Other symbols:**
  - $\eta_{\rm wp}$ (§C7a) vs $\eta_{\rm WPE}$ (§C7b Eq. (118)).
  - $E_{\rm opt}$ vs $E_{\rm tx}$ (§C0 subsection 10.1, line 1904) vs $E_{\rm pt}$ (§C6 Eq. (80)).
  - $v$ (lines 4489 and 4719) vs $v_r$ (§C0 subsection 2; §F6 line 8777) for radial velocity; $v$ is also the vehicle speed in Eq. (184).
  - $T$ vs $T_c$ for the chirp duration.
- **FS-4S.** §C3b (line 3058), §C0 subsection 10.8 (line 2462) and the §C7b subsection 3 table (≈5298, 390/88 µJ) contradict §C7a line 4636.
- **"Long range" as an FMCW differentiator.** §F6 (line 8743) lists it, but in §C7a/§C7b FMCW needs ≈3.2× more optical energy per point at 200 m (2.1× at 300 m, line 5219). Its reach comes from the 1,550 nm eye-safety allowance (§C7b subsection 2(i)), which 1,550 nm ToF shares.
- **Power envelopes:**
  - "10–15 W" in §F6 (line 8777);
  - "8–25 W" in Figure C7a (line 4626);
  - "8–13 W" in §C6(c) (line 4270);
  - "≤15 W" in §C7a subsection 6 (line 4825).
- **Interference immunity.** §F6 says coherent detection "responds only to light that matches its own LO" (line 8763), while §C7 says "this is not absolute, since FMCW interference modes exist" (line 4563).
- **Repeated paragraph.** The measured efficiencies 0.112/0.168/0.057 appear three times: §C0 subsection 10.1 (line 1915), §C7a(a) (line 4697) and §C7b subsection 1(c) (≈4958).
- **Spelling and wording:**
  - "Insight Lidar" (line 4536) vs "Insight LiDAR" (line 4805; §C3a, line 2585).
  - $n_{\rm mode}$ is "signal photons" in §F6 (line 8761) but "signal photoelectrons" in §C10.3a.
- **45% PDE.** It is RoboSense's Phoenix claim, tagged [P, unverified] in §C5 (lines 3868 and 4159), but used untagged at line 4606 and in §F6 (line 8758).
- **Two Analog Photonics OPAs.** §C7 describes one at "1.5 µm pitch, about 60°" (line 4459) and one with "8,192 elements at 1 µm pitch" (line 4587; §C10.3a gives 8 × 5 mm, 100° × 17°). Say in §C7 that these are two different devices.
- **ToF emitter wall-plug efficiency.** §C7a gives "≈15–30%" (line 4710), §C6(c) gives "20–30%" (line 4270), and the model uses 20% (line 4787).

### §C7b (can FMCW win?)

The whole block, lines 4832–5462 (from "## C7b" through the Sources line before "## C8"), was read, with all of §C7a (4608–4831) and the specific lines in §C0, §C3a, §C6, §C10 and §F6 that it draws on. Lines cited after 7341 are 6 lines lower after an insertion in §D7 (Eq. (185): 8763 → ≈8769).

#### 1. Overall assessment

What reads well: nearly every estimate is derived in the text. I recomputed about 150 substitutions and almost all agree to rounding. Most subsections open with their question and answer, and every table has a "how computed" note. Three systemic problems:

1. **One quantity, several definitions.**
   - "Dwell" is 10 µs with no round trip in §C7a's $E_{\rm rx}$, but $E/P+2\tau$ in Eq. (107).
   - Wall-plug efficiency and the fixed overhead each have two symbols.
   - Two power models give near-identical totals (≈68 W and ≈67 W) for different cases.
   - The parity chip is sized in channels in some places and in receivers in others.
2. **The round-trip ("dead-time") light is handled inconsistently.**
   - It is placed at the wrong end of the ramp.
   - It is dropped from the eye-safety and parity headlines that it changes: an ungated sensor at 25 Mpts/s can exceed the 9.1 W allowance, and the parity case is 14–16 W, not 12 W.
   - Two stated conclusions also contradict the block's own numbers: the Waymo laser-linearity claim, and "any two of three → 15–20 W".
3. **Structure.**
   - The 33-line short answer leaves out the two caveats that move the headline most: the assumed coherent efficiency is above every measured value, and the 3.2× is per sample, not per cell.
   - Subsection 2 absorbs sensor power and eye safety (2(h)–(i)) before the channel model those items depend on.

#### 2. Findings (most severe first)

**1.** **Line** 5288 (also 5259, 5268, 5279) — **Category** A/B — **Severity** high
- **Quote:** "The §C7a 2026 central value, at 300 m with the model's 10 µs dwell, is"
- **Problem:** "Dwell" means two things.
  - In §C7a, Eq. (96) (line 4738) uses $T_{\rm dwell}=2T=10$ µs. That is the integration time with no round trip, and "300 m" there is the 0–300 m search window $R_{\max}$, not the target range.
  - Eq. (107) here defines $T_{\rm dwell}=E_{\rm opt}/P_{\rm ch}+2\tau=12.7$ µs.
  - Subsection 3 mixes the two. The table at 5259 puts a "10 µs dwell" column next to a "12.7 µs" one. The 200 m, 15 Mpts/s receiver power (5279, 5386) uses the 300 m / 10 µs $E_{\rm rx}$. "A 4 µs dwell" implies ≈5 GS/s here (5268) but ≈2.7 GS/s in §C7a (4743).
- **Proposed rewrite:** "The §C7a 2026 central value is $E_{\rm rx}=4\times(12{,}300\times37\ {\rm pJ}+10\ {\rm mW}\times10\ \mu{\rm s})\approx2.23$ µJ per point (Eq. (96)). It digitizes the whole 0–300 m search window ($R_{\max}=300$ m, 12,300 samples, Eq. (109)). It charges the analog power for §C7a's 10 µs, which is the integration time $T_{\rm int}$ of Eq. (107), not its dwell. With the 12.7 µs dwell of Eq. (107) the analog term is $10\ {\rm mW}\times12.7\ \mu{\rm s}=0.127$ µJ and $E_{\rm rx}\approx2.3$ µJ. A sensor that searches only to 200 m (8,900 samples) would need $4\times(8{,}900\times37\ {\rm pJ}+0.127\ \mu{\rm J})\approx1.8$ µJ [E]." Also rename the 5259 column to "Channels at 10 µs integration (§C7a, no round trip)".

**2.** **Line** 5087 (same claim in §C7a, 4763) — **Category** B — **Severity** high
- **Quote:** "Waymo reports a pre-distorted DFB holding <100 kHz error over 1 GHz, i.e. $\varepsilon<10^{-4}$ [P] (§C7a(f)). By Eq. (112) that is enough at 200–250 m"
- **Problem:**
  - Line 5083 defines $\varepsilon=8\delta\nu_{\max}/B_{\rm eff}$, so 100 kHz over 1 GHz is $\varepsilon=8\times10^{-4}$, not $10^{-4}$; the ratio 100 kHz / 1 GHz is $\delta\nu/B_{\rm eff}$.
  - In frequency terms Eq. (112) allows 94 kHz at 200 m, 75 kHz at 250 m and 62.5 kHz at 300 m (line 5082). A 100 kHz error therefore fails at 250 m by the section's own rule.
- **Proposed rewrite:** "Waymo reports a pre-distorted DFB holding <100 kHz error over 1 GHz [P] (§C7a(f)), a fractional frequency error $\delta\nu/B_{\rm eff}<10^{-4}$. If the error had the bow shape of Eq. (112), $\delta\nu_{\max}=100$ kHz would give $\varepsilon=8\times10^{-4}$. That is just outside the 94 kHz tolerance at 200 m and well outside the 62.5 kHz at 300 m. Whether it suffices at 200–250 m depends on the error's shape and on whether 100 kHz is a peak, peak-to-peak or rms figure [E]."

**3.** **Line** 5370 (also 4867; table row 5391) — **Category** B — **Severity** high
- **Quote:** "With any two of the three, it stays at ≈15–20 W, above the 15 W target."
- **Problem:**
  - The row "Two of three: $E_{\rm rx}$ at 0.30 µJ" keeps a receiver 7× better than today's 2.23 µJ, so it does not show the receiver condition missing.
  - With today's receiver and the other two conditions met, Eq. (122) gives $3+15\times(0.50+2.23)\approx44$ W. The receiver is the decisive condition, and the claim (repeated at 4867) understates its absence by about 3×.
  - 15 W is at the target, not above it.
- **Proposed rewrite:**
  - Add a row: "| Two of three: receiver stays at today's 2.23 µJ | 0.15 µJ | 30% | 0.50 µJ | 2.23 µJ | 2.73 µJ | 44 W |".
  - Relabel the row at 5391 "Receiver only partly improved (0.30 µJ)".
  - Write: "Without the efficient laser, or without the lower energy per point, a 15 Mpts/s sensor stays near 19.5 W. Without the low-power receiver it stays near 44 W. A receiver at 0.30 µJ per point, 7× better than today's but 3× short of the goal, lands exactly at the 15 W target." Make the same change at 4867.

**4.** **Line** 4973 (also 4844) — **Category** A — **Severity** high
- **Quote:** "A CW channel keeps transmitting during the first $\tau$ of each ramp, before any usable echo exists (subsection 2(a))."
- **Problem:**
  - Light sent during the first $\tau$ of a ramp returns during $[\tau,2\tau]$, inside that ramp's useful window, so it is used.
  - The wasted light is what is sent during the last $\tau$: its echo lands in the next ramp's discarded first $\tau$. That is exactly the light 2(i) gates off (5231: "gated off during the last $\tau$ of each ramp").
  - The energy count ($2\tau$ per point) is right, but this explanation contradicts the gating fix. Line 4844 has the same error ("…before any usable echo has returned").
- **Proposed rewrite:** "**Round-trip dead time.** The receiver discards the first $\tau$ of each ramp (subsection 2(a)). The light the channel sends during the last $\tau$ of each ramp returns in that discarded window of the next ramp and is wasted. The wasted transmission and the receiver's dead time both last $\tau$ per ramp, $2\tau$ per point." At 4844: "apart from the 12–35% it emits during the last $\tau$ of each ramp, whose echo falls in the next ramp's discarded window."

**5.** **Line** 5226 (also 4860, 5228, 5230, 5236–5237; §C7a 4709) — **Category** B — **Severity** high
- **Quote:** "FMCW emits $\dot NE_{\rm opt}$: 3.0 W at 10 Mpts/s and 200 m, a third of the 9.1 W, and 7.6 W at 25 Mpts/s"
- **Problem:**
  - Line 5285 states that an ungated channel transmits more than its useful light ("$190\times30\ {\rm mW}=5.7$ W" for 4.5 W useful), yet the eye-safety budget counts only $\dot NE_{\rm opt}$.
  - At 16–30 mW per channel, Eq. (107) adds a factor of 1.14–1.27, the same at every range because both terms scale with $R$. That gives 3.5–3.8 W at 10 Mpts/s and 8.7–9.6 W at 25 Mpts/s; the top of that range exceeds 9.1 W.
  - The ≈600 m reach (5230) becomes ≈470 m. The ≈240 m reach at 25 Mpts/s becomes ≈190 m, below this section's 200 m operating point, so line 5228 no longer holds at 25 Mpts/s.
- **Proposed rewrite:** "Counting the round-trip light (×1.14–1.27 at 16–30 mW per channel, Eq. (107)), an ungated FMCW sensor emits 3.5–3.8 W at 10 Mpts/s and 200 m, 38–42% of the 9.1 W. At 25 Mpts/s it emits 8.7–9.6 W, which can exceed the allowance. With a gated transmitter (item 2 below) the figures are $\dot NE_{\rm opt}$: 3.0 and 7.6 W [E]." Then recompute the reach in item 1 for both cases (ungated at 30 mW ≈470 m; gated ≈600 m) and qualify 5228.

**6.** **Line** 5418 (also 4864, 5406, 5416, 5420, 5449) — **Category** A — **Severity** high
- **Quote:** "Signpost: a published chip with ≥256 receivers at ≤5 mW each. §C10.7's looser signpost, ≥256 channels within ≈10 W, marks the first step."
- **Problem:** The required chip is sized differently in each place:
  - "≥150 channels" (4864);
  - "115–190 channels" (5406);
  - "≥150–256 channels … 600–1,000 receivers" (5416);
  - "≥100 channels" (5420);
  - signposts counted in receivers (5418, 5449: ≥256 receivers is 64 four-receiver channels);
  - §C10.7's signpost counted in channels (line 6810).

  A reader cannot tell which chip is required, or whether "looser" refers to count or to power.
- **Proposed rewrite:**
  - At first use, fix "a channel is one transmit beam with its four receivers".
  - Use one requirement throughout: "115–190 channels (460–760 receivers) at ≈2–3 mW per receiver, ADC and FFT included (subsection 5)".
  - Signpost: "a published chip with ≥256 receivers (64 channels) at ≤5 mW each: a third to a half of the parity count, at about twice the parity power per receiver. §C10.7's signpost, ≥256 channels within ≈10 W (≈10 mW per receiver if each channel has four), asks for more channels at a higher power per receiver."

**7.** **Line** 4958 (also 5380; short answer 4837–4841) — **Category** A — **Severity** high
- **Quote:** "The FMCW value, 0.25, is at the optimistic end of what has been measured: Waymo's lab chain measured 0.112 end to end"
- **Problem:**
  - 0.25 is above every measured value quoted in the same sentence (0.057–0.168). §C0 (line 2438) correctly says it "lies above both measured chains".
  - The short answer's 3.2× never says that with the measured efficiencies the gap is 5–14×.
- **Proposed rewrite:** "The FMCW value, 0.25, is a design value about 1.5× above the best coherent chain measured so far. Waymo's lab chain measured 0.112 end to end, or 0.168 without its Hann window [P]; Pointcloud's integrated array measured 0.057 [P] (§C0 subsection 10.1)." In the first short-answer bullet add: "With the coherent efficiencies measured so far (0.057–0.168), the gap is 5–14× rather than 3.2× (subsection 1(c))."

**8.** **Line** 5178 (Eqs. (118)–(120); 4857; Eqs. (122)–(123)) — **Category** A — **Severity** high
- **Quote:** "$\eta_{\rm WPE}$ the wall-plug efficiency of the CW laser with its amplifiers, the optical power out per electrical power in (≈0.15 in 2026, §C7a(b))"
- **Problem:**
  - The same efficiency is written $\eta_{\rm WPE}$ in Eqs. (118)–(120) and at 4857, but $\eta_{\rm wp}$ in Eqs. (122)–(123) and in §C7a (4709, 4787).
  - The 3 W overhead is $P_0$ in Eq. (118) and $P_{\rm oh}$ in Eq. (122).
  - Two power models are never related. Eq. (118) at 10 Mpts/s and 300 m gives ≈68 W; Eq. (122) at 15 Mpts/s and 200 m gives ≈67 W. The two totals appear ten lines apart in the short answer (4857, 4867) and read as one case.
- **Proposed rewrite:** Use $\eta_{\rm wp}$ and $P_{\rm oh}$ throughout. After Eq. (122) add: "Eq. (122) is Eq. (118) with the dead-time light left out and the channel terms folded into $E_{\rm rx}$ (Eq. (96)). Here it is evaluated at 15 Mpts/s and 200 m; subsection 2(h) evaluated Eq. (118) at 10 Mpts/s and 300 m, so the ≈67 W and ≈68 W totals are different cases." In the short answer, label each total with its case.

**9.** **Line** 5370 — **Category** A/C — **Severity** medium
- **Quote:** "With all three, a 15 Mpts/s sensor reaches ≈12 W."
- **Problem:** The opening headline counts useful light only. The same subsection (5396–5402) shows that the round-trip light lifts the "all three" case to 16 W at 30 mW per channel, or 14 W with 190 dim channels.
- **Proposed rewrite:** "With all three, a 15 Mpts/s sensor reaches ≈12 W counting only the useful light, and 14–16 W once the light sent during the round trips is counted. Parity therefore also needs either many dim channels (≈190 at 15 mW) or a transmitter switched off during the last $\tau$ of each ramp."

**10.** **Line** 4848 (also 5309) — **Category** B — **Severity** medium
- **Quote:** "It measures only ≈0.05–0.25 Mpts/s at 200 m."
- **Problem:** The upper end needs 100 mW per channel (table at 5026). The same list says a channel "can carry only tens of milliwatts" (4846), and subsection 2 calls 16–30 mW realistic, which gives 47–130 kpts/s (5242). Line 5309 repeats the range as "47–240 k with realistic power".
- **Proposed rewrite:** "It measures only ≈47–130 kpts/s at 200 m with 16–30 mW of light, and ≈240 kpts/s even at 100 mW (subsection 2 table)." At 5309: "That is 47–130 k at the realistic 16–30 mW, 176–240 k at 100 mW, and never more than 375 k (subsection 2)."

**11.** **Line** 4989 (also 5242–5243) — **Category** A — **Severity** medium
- **Quote:** "the photon budget dominates: 8–21 µs per point. The round trip adds a fixed 2.67 µs."
- **Problem:** 8–21 µs is already the whole dwell, round trip included (table rows at 5024–5025: 7.7–21.4 µs). Read in order, the text implies 10.7–23.7 µs. The summary at 5242–5243 repeats the wording.
- **Proposed rewrite:** "At 200 m with 16–30 mW per channel, emitting the photon budget takes 5–19 µs per point; the round trip adds a fixed 2.67 µs, for a dwell of 8–21 µs."

**12.** **Line** 4841 — **Category** A — **Severity** medium
- **Quote:** "To cover the whole cell, FMCW needs ≈15 µJ, about 160× more."
- **Problem:**
  - "More" than what? Right after a sentence about one FMCW sample, a reader can take 160× as relative to 0.30 µJ, where the true factor is 48×.
  - "Cell" is used here but defined only at 4926.
- **Proposed rewrite:** "A cell is one angular resolution element of the point cloud, here 0.05° × 0.05°. To cover a whole cell, FMCW needs ≈15 µJ: 48 samples, and about 160× the 93 nJ of a ToF point."

**13.** **Line** 5126 — **Category** A — **Severity** medium
- **Quote:** "$L_c=c/(\pi\Delta\nu)\ge2R$ (§C7, Eq. (185)), is the condition $2\pi\Delta\nu\tau\le2$."
- **Problem:** Eq. (185) is in §F6 (old line 8763, now ≈8769), not §C7, and §C7 does not state this rule. $L_c$ is first tagged as Eq. (56) in §C3a (2802) and defined in the §C0 subsection 2 table (1575).
- **Proposed rewrite:** "$L_c=c/(\pi\Delta\nu)\ge2R$ (§C0 subsection 2; Eq. (56)), where $L_c$ is the coherence length, is the condition $2\pi\Delta\nu\tau\le2$."

**14.** **Line** 5241 (structure of subsection 2) — **Category** C — **Severity** medium
- **Quote:** "**Summary of the dwell.**"
- **Problem:**
  - Items 2(h) (sensor power at 10 Mpts/s and 300 m) and 2(i) (the eye-safety allowance) are not about the dwell.
  - The subsection's opening (4989, "items (c)–(h)") does not preview them, and the dwell summary comes only after (i).
  - Item (h) uses $N_{\rm ch}$ from Eq. (121) and receiver ingredients that subsection 3 introduces later.
- **Proposed rewrite:**
  - Move "Summary of the dwell" to directly after item (g).
  - Make (h) and (i) a new subsection after the channel tax, "### 3a. Sensor power at 10 Mpts/s and 300 m, and the 1,550 nm eye-safety ceiling". Open it with: "This subsection adds up a whole FMCW sensor's electrical power from the dwell (subsection 2) and the channel count (Eq. (121)), and asks whether the 1,550 nm eye-safety allowance relaxes it."
  - Order: 1 → 2(a)–(g) + summary → 3 → 3a → 4 → 5 → 6 → 7.
  - Update the pointers "subsection 2(h)" (4857; §C7a 4757, 4767), "subsection 2(i)" (4860; §C7a 4709), "item (i)" (5213) and "Item (h)" (5231).

**15.** **Line** 4836 (short answer, 4836–4868) — **Category** C — **Severity** medium
- **Quote:** "**Short answer** [E unless tagged]."
- **Problem:**
  - It runs 33 lines: 10 top-level bullets and about 25 sub-bullets.
  - It carries derivation-level detail: the 35 mW ADC crossover, 1.1–1.3 GHz sweeps, the $\eta_{\rm coh}$ formula, and 176 mW + 200 mW per channel.
  - It leaves out two decisive caveats: the efficiency (finding 7), and which comparison to use (per sample vs per cell), which is buried at the end of 1(d) (4970).
- **Proposed rewrite:** Cut to about eight one-sentence bullets, each with one number and a pointer. For example, bullet 1: "Per joule of light, FMCW measures ≈3.2× fewer samples than 940 nm SPAD ToF at 200 m on a 10% target, or 5–14× with measured coherent efficiencies (subsection 1(c)). The per-sample figure suits objects larger than the sample spacing, such as cars. For objects smaller than a cell, such as debris, FMCW needs ≈160× ToF's energy (subsection 1(d))." Move the floor, sweep and ADC numbers into subsection 2.

**16.** **Line** 4981 (and 5219) — **Category** C — **Severity** medium
- **Quote:** "The required energy grows with range in both principles, but at different rates."
- **Problem:** The heading "Range dominates everything" is never tied to a result. The consequence appears only at the end of 2(h) (5219: the ratio falls from 3.2 to 2.1).
- **Proposed rewrite:** Add to (f): "**Consequence.** The ratio of Eq. (104) falls roughly as $1/R$, from 3.2 at 200 m to 2.1 at 300 m ($4.5\ {\rm W}/2.1\ {\rm W}$ at 10 Mpts/s). This assumes the coherent aperture is re-optimized for each range and the ToF lens stays at 25 mm [E]." Replace 5219 with a pointer to 1(f).

**17.** **Line** 5301 — **Category** A — **Severity** medium
- **Quote:** "Optical energy per point scales as $R^2/\rho$ (subsection 1). Scaling to 200 m and 10% multiplies it by"
- **Problem:**
  - Subsection 1(f) (4983) says coherent energy scales as $R$. $R^2$ holds only for direct detection, or for a fixed coherent aperture in its far field.
  - The comparison also crosses wavelengths without saying so: Pointcloud works at 1,310 nm (§C7a, 4648).
- **Proposed rewrite:** "Pointcloud's aperture is small and fixed, so at 65–200 m its beam is in the far field and $A_{\rm mode}$ (Eq. (101)) stops changing with range. The energy per point then scales as $R^2/\rho$ (Eq. (97)), not as the $R$ of subsection 1(f), which re-optimizes the aperture for each range. Scaling to 200 m and 10% multiplies it by $(200/65)^2\times(0.30/0.10)=28.4$. Pointcloud works at 1,310 nm, where a photon carries 1.18× the energy of a 1,550 nm one." The author should confirm the far-field point against §C10.4.

**18.** **Line** 5128 (also 5131, 5138, 5316, 5350) — **Category** A — **Severity** medium
- **Quote:** "The chirp must end before the beam sweeps across its own width (§C7):"
- **Problem:**
  - A point needs two ramps ($T_{\rm dwell}=2T_c$), but Eq. (116), the scan limit in Eq. (117), the ≈$10^4$ °/s figure and the ski-jump test (5350) all cap a single chirp.
  - The text never says whether a point's up- and down-ramp may fall on adjacent beam positions.
- **Proposed rewrite:** After Eq. (116) add: "Eq. (116) caps each ramp. The up- and down-ramp of one point are paired to separate range from Doppler. If both must see the same spot, the condition is $2T_c\lesssim\theta_b/\Omega$, which halves the allowed $\Omega$ (≈$5\times10^3$ °/s for 0.05° and 5 µs chirps)." Then state which condition items (g) and subsection 4 use.

**19.** **Line** 5239 — **Category** A — **Severity** medium
- **Quote:** "$3\ {\rm W}+10^{7}\times(93\ {\rm nJ}\times2.25/0.20+70\ {\rm nJ})=14.2$ W."
- **Problem:** Three inputs are undefined here:
  - 0.20 is the ToF laser wall-plug efficiency (§C7a 4787);
  - 70 nJ is the SPAD-SoC receive energy, introduced only later (5274);
  - 3 W is the overhead.

  The "≈3.5×" conclusion at 5233 rests on this line.
- **Proposed rewrite:** "**ToF at 300 m:** the 3 W overhead, plus per point the laser's electrical energy at the §C7a ToF wall-plug efficiency of 0.20 and ≈70 nJ of SPAD-SoC receive electronics (§C7a(c)): $3\ {\rm W}+10^{7}\ {\rm s^{-1}}\times(93\ {\rm nJ}\times2.25/0.20+70\ {\rm nJ})=3+11.2=14.2$ W [E]."

**20.** **Line** 4857 — **Category** A/D — **Severity** medium
- **Quote:** "≈30 of ≈68 W is the useful optical energy per point divided by the CW laser's wall-plug efficiency"
- **Problem:**
  - An energy per point divided by an efficiency is not a power.
  - $\eta_{\rm coh}$ appears before it is defined (4859).
  - The sentence is about 60 words long.
- **Proposed rewrite:** "For 10 Mpts/s at 300 m the sensor draws ≈68 W. About 30 W is the useful optical power divided by the laser's efficiencies, $\dot NE_{\rm opt}/(\eta_{\rm coh}\eta_{\rm wp})$, where $\eta_{\rm coh}$ is the share of beat power left in the FFT peak (≈1 for a narrow laser). About 9 W is light sent during the round trips, and about 26 W goes to the four receivers per beam."

**21.** **Line** 4910 (vs 4900) — **Category** A — **Severity** medium
- **Quote:** "A beat bandwidth $\Delta f=1$ GHz corresponds to an optical bandwidth"
- **Problem:** Ten lines apart, $\Delta f$ is first the 250 MHz TIA bandwidth (4900, Eq. (100)) and then the 1 GHz beat bandwidth.
- **Proposed rewrite:** "A beat bandwidth $\Delta f_{\rm beat}=1$ GHz corresponds to an optical bandwidth $\Delta\lambda=\lambda^2\Delta f_{\rm beat}/c=0.008$ nm." Optionally write $\Delta f_{\rm TIA}$ in Eqs. (99)–(100).

**22.** **Line** 5105 (vs 5096) — **Category** A — **Severity** medium
- **Quote:** "What does make long ramps harder is frequency noise slower than $1/T_u$ (flicker noise, drift) and chirp nonlinearity (Eq. (112))"
- **Problem:** Line 5096 says frequency noise slower than $1/T_u$ "is left out" and harmless. This line says the same noise makes long ramps harder.
- **Proposed rewrite:** "What does make long ramps harder is low-frequency noise (flicker, drift). As $T_u$ grows, the lower limit $1/T_u$ of Eq. (113) falls and lets more of that noise into $\sigma^2_{\Delta\phi}$. Chirp nonlinearity (Eq. (112)) also matters more for long ramps. Both are specified separately from the linewidth."

**23.** **Line** 5263 (vs 5009, 5208) — **Category** A — **Severity** medium
- **Quote:** "15 Mpts/s (the parity case)"
- **Problem:** "The parity case" means the 15 Mpts/s point rate here, but the 0.15 µJ energy per point at 5009 and 5208. The 5208 case is also at 10 Mpts/s and 300 m.
- **Proposed rewrite:** Write "15 Mpts/s (the parity point rate)" here, and "the 0.15 µJ parity energy (subsection 5)" at 5009 and 5208.

**24.** **Line** 4966 — **Category** B — **Severity** low
- **Quote:** "Of this, ×2.3 is speckle fading with four looks, ×1.8 is finding the peak in both ramps, and ×1.3 is"
- **Problem:** The three factors multiply to 5.4, not the 5.1 just stated. The §C0 steps (17.3 → 21.9 → 39.1 → 88.5, lines 2074–2076) give 1.27 × 1.79 × 2.26 = 5.1. "Of this" could mean the 4.8 or the 5.1.
- **Proposed rewrite:** "Of the ideal 5.1, ×1.27 is the coherent receiver's one photoelectron of shot noise in each of the ≈2,450 FFT bins it searches (17.3 → 21.9), ×1.79 is finding the peak in both ramps (→ 39.1), and ×2.26 is speckle fading with four looks (→ 88.5)."

**25.** **Line** 5125 (repetition) — **Category** C — **Severity** low
- **Quote:** "With a 100 kHz laser at 200 m, $\eta_{\rm coh}=e^{-0.84}=0.43$, so the central 0.30 µJ becomes $0.30/0.43=0.70$ µJ."
- **Problem:** This repeats 4979 nearly verbatim. Other near-verbatim repeats:
  - the efficiency paragraph: 4958 = 5380 (= §C7a 4697);
  - the dead-time share: 4975 ≈ 5018;
  - the scan limit: 5131 ≈ 5316;
  - $\tau=2R/c$ is defined three times (4846, 4973, Eq. (105)).
- **Proposed rewrite:** Keep one copy and point to it. At 5125: "The energies of subsection 1 leave this loss out; at 200 m a 100 kHz laser more than doubles them (subsection 1(e))." At 5380: "The efficiency is also the least certain input (subsection 1(c)). With measured chains the 2026 central case rises from ≈67 W to ≈82–104 W, or ≈170 W."

**26.** **Line** 4921 (also 4915, 4917) — **Category** A — **Severity** low
- **Quote:** "This is smallest, at $2\lambda R/\pi$, when $w_0=\sqrt{\lambda R/\pi}=9.9$ mm (a ≈22 mm aperture)."
- **Problem:**
  - "This" is $w^2$, not $w$; read as $w$, the units are wrong.
  - At 4915, "The ½" is invisible to the reader because it is inside the $2\pi$ of Eq. (101).
  - At 4917, the 14.2 mm uses Eq. (102) before Eq. (102) is given.
- **Proposed rewrite:** "$w^2$ is smallest, $w^2_{\min}=2\lambda R/\pi$, when $w_0=\sqrt{\lambda R/\pi}=9.9$ mm (a ≈22 mm aperture)." At 4915: "The factor 2 in the denominator of Eq. (101) is the ½ for the single polarization the LO accepts." At 4917: "spreads, by Eq. (102) below, to $w(200\ {\rm m})=14.2$ mm".

**27.** **Line** 4972 — **Category** A — **Severity** low
- **Quote:** "(An FMCW channel sweeps its frequency in "ramps", or chirps; one point uses an up-ramp and a down-ramp, subsection 2.)"
- **Problem:** Ramps are first used at 4927 and 4935 and are defined only here. The short answer's "$+2\tau$" (4846) also relies on the two ramps without saying so.
- **Proposed rewrite:** Move the definition into the first FMCW sentence (4834): "…sweeps the frequency of a continuous laser in linear 'ramps' (chirps), one up and one down per point…". At 4846 add: "($2\tau$ because each of the two ramps loses one round trip)".

**28.** **Line** 4903 — **Category** A/E — **Severity** low
- **Quote:** "This gives $n\approx890$ photoelectrons, some 35× the SPAD's 25 counts."
- **Problem:** The solve step for the quadratic is skipped.
- **Proposed rewrite:** "Squaring Eq. (100) gives $M^2I_s^2-49\,(2qM^2F\Delta f)\,I_s-49\,i_n^2=0$, whose positive root is $I_s=35.5$ nA. Then $n=I_st_p/q=35.5\ {\rm nA}\times4\ {\rm ns}/(1.60\times10^{-19}\ {\rm C})\approx890$ photoelectrons, some 35× the SPAD's 25 counts."

**29.** **Line** 5386 — **Category** B — **Severity** low
- **Quote:** "| 2026 central (§C7a) | 0.30 µJ | 15% | 2.0 µJ | 2.23 µJ | 4.25 µJ |"
- **Problem:** As printed, 2.0 + 2.23 = 4.23, not 4.25, and then $3+15\times4.23=66$ W. The 4.25 comes from $0.303/0.15=2.02$ (§C7a 4789).
- **Proposed rewrite:** Print 2.02 µJ in the laser column, and note "0.30 µJ is 0.303 µJ rounded".

**30.** **Line** 5231 — **Category** B — **Severity** low
- **Quote:** "As $P_{\rm ch}\to\infty$ it approaches ≈49 W: the useful light, the range samples and the overhead."
- **Problem:** The listed terms sum to 30 + 14.8 + 3 = 47.8 W. The 49.4 W derived at 5238 also includes 1.6 W of analog power during the round trips.
- **Proposed rewrite:** "…approaches ≈49 W: the useful light (30 W), the range samples (14.8 W), the analog power held during the round trips (1.6 W) and the overhead (3 W)."

**31.** **Line** 5083 (also 5104, 5166, 5324) — **Category** D/A — **Severity** low
- **Quote:** "It is the range-blur rule $\delta R\approx\varepsilon R$ with the blur held inside one resolution cell:"
- **Problem:**
  - "Cell" is the 0.05° angular cell elsewhere, but here and at 5104 and 5166 it means a $\Delta R$-wide range bin.
  - At 5324, $\Omega_{\rm cell}$ (a solid angle) sits next to $\Omega$, the scan rate (5310, 5316).
- **Proposed rewrite:** Write "range bin" at 5083, 5104 and 5166. At 5324: "divided by the cell's solid angle $\theta_{\rm cell}^2$ gives $\lambda^2/\theta_{\rm cell}^2=(1.55\times10^{-6})^2/(8.7\times10^{-4})^2=3.2$ mm²".

**32.** **Line** 5433 — **Category** D — **Severity** low
- **Quote:** "Documented mutual interference at high penetration (§C9), i.e. when many lidar-equipped cars share the road,"
- **Problem:** The bullet asserts "documented" interference, and the next bullet says "None is documented today". The conditional is missing.
- **Proposed rewrite:** "If mutual interference were documented at high penetration (§C9), i.e. when many lidar-equipped cars share the road, or if 905/940 nm ToF hit eye-safety and sunlight limits beyond 300 m. Neither is documented today; ToF coding and randomization cope."

**33.** **Line** 5413 (also 5056, 5425, 5432; missing tags) — **Category** E — **Severity** low
- **Quote:** "with the evidence status of each in brackets."
- **Problem:**
  - The brackets mix deployability tags with an evidence tag ([U], 5432) and a non-standard "[D in trucks]".
  - "[I/U]" (5056) does not say which claim is which.
  - Untagged claims include:
    - sunlight $E_\lambda\approx0.25$ W m⁻² nm⁻¹ (4909);
    - the Waymo and Pointcloud efficiencies (4958);
    - Siegman, Rye, Frehlich and Kavaya (4915); Richter et al. (5103);
    - "Pointcloud Methods" (5016);
    - $10^{15}$–$10^{16}$ Hz/s (5088);
    - the vendor rows of the product table (5293–5298);
    - EM4 and Aeries (5261–5264);
    - 45,600 °/s (5311);
    - "The only merchant FMCW SoC" (5409);
    - the wind-lidar EDFAs (5429).
- **Proposed rewrite:** "…with the deployability status of each in brackets ([D], [NT], [R]; §C7a)". Write "[D] (trucks only)" and "**A ToF failure mode** (hypothetical, none documented) [U]". Split 5056 into "[I, Murmann ADC survey]" and "[U]". Add [P]/[I]/[T] to the listed claims.

**34.** **Line** 5039 (also 5131, 5157, 5164, 5181, 5295–5298) — **Category** E/B — **Severity** low
- **Quote:** "$f_D=2\times70/1.55\times10^{-6}=90$ MHz."
- **Problem:**
  - As typed this evaluates to $9.0\times10^{-5}$; the denominator needs brackets. The same slip appears at 5131 ("$8.7\times10^{-4}/5\times10^{-6}$"), 5157 and 5164 ("$2{,}000/3.1\times10^{8}$"), and in the $E=P/\dot N$ column at 5295–5298.
  - Line 5181 is a very wide inline equation.
- **Proposed rewrite:** Write "$f_D=2\times70/(1.55\times10^{-6})=90$ MHz", "$8/(3.84\times10^{6})=2.1$ µJ", and so on. Make the expanded $P_{\rm elec}$ at 5181 a numbered display equation split over two lines.

**35.** **Line** 4944 (jargon) — **Category** D — **Severity** low
- **Quote:** "1,550 nm FMCW, collimated 20 mm monostatic beam, four looks, per sample"
- **Problem:** These terms are unexplained at first use in this section:
  - "monostatic" (explained only at 5355);
  - "PDE" (4893; expanded at 4952);
  - "Hann window" (4958);
  - "mode-hop-free" (5063);
  - "TFLN" and "E-DBR" (5124);
  - "the indie Surya class" (5163; explained at 5409);
  - "VCSEL" and "$C_6$" (5224);
  - "SRAM" (5277);
  - "FFT pipe" (5281);
  - "CMOS" (5338);
  - "qualified by the million" (5334).
- **Proposed rewrite:** Expand each at first use. Examples:
  - "monostatic (transmitting and receiving through one aperture)";
  - "PDE (photon detection efficiency)";
  - "Hann window (a taper applied before the FFT that cost Waymo 1.8 dB of signal, §C0 subsection 10.7)";
  - "mode-hop-free (no jumps between laser cavity modes)";
  - "TFLN (thin-film lithium niobate)", and spell out E-DBR;
  - "indie Semiconductor's Surya FMCW SoC";
  - "VCSEL (vertical-cavity surface-emitting laser)";
  - "the IEC 60825-1 extended-source factor $C_6$ (§C4c)";
  - "have passed automotive qualification and shipped in millions".

**36.** **Line** 5123 (pointer and number slips) — **Category** B/A — **Severity** low
- **Quote:** "100 kHz (Waymo's upper figure; Pointcloud's external DFB, §C10.3)"
- **Problem:**
  - Waymo's figure is "≲60–120 kHz" (§C7a 4759), so 100 kHz is not its upper end.
  - Pointcloud's DFB is in the §C10.4 table (6517), not §C10.3.
  - The 8,192-element OPA cited to "§C10.7" (5438) is in §C7 (4587) and §C10.2b (5908).
  - The same useful light is "4.5 W" at 5216 but "4.6 W" at 5226.
  - At 5236, "$0.45$ µJ gives …$0.455\ \mu{\rm J}$" uses two values in one clause.
- **Proposed rewrite:** "100 kHz (inside Waymo's 60–120 kHz range, §C7a(f); Pointcloud's external DFB, §C10.4)". Change "§C10.7" to "§C7, §C10.2b". Use 0.455 µJ (4.6 W, 11.4 W) or 0.45 µJ (4.5 W, 11.3 W) consistently.

**37.** **Line** 5313 (numbers without their inputs) — **Category** A — **Severity** low
- **Quote:** "visits only $1{,}200\times10=12{,}000$ columns per second per channel."
- **Problem:** Inputs are not named:
  - here, 1,200 columns per frame × 10 Hz;
  - "≈4×10⁴× a scanner's" (4947), which is §C0's sunlight per unit signal;
  - $T_u=5$ µs assumed at 300 m (5054);
  - 2 Mpts/s is an Aeries-class rate (5330);
  - the FMCW $\eta=0.25$ described as "optical × detector × mixing" (4954), whereas §C7a (4674) says it was checked against Waymo's estimate rather than built from component factors.
- **Proposed rewrite:**
  - "visits only $1{,}200$ columns per frame × 10 frames/s $=12{,}000$ columns per second per channel";
  - 4947: "background per unit signal ≈4×10⁴× a scanner's (§C0 subsection 9)";
  - 5054: "(with the same $T_u=5$ µs)";
  - 5330: "80% of an Aeries-class 2 Mpts/s";
  - 4954: "FMCW: 0.25, a design value checked against Waymo's estimate rather than built from component factors (§C7a(a))".

**38.** **Line** 4861 — **Category** D — **Severity** low
- **Quote:** "it permits brighter channels, which pay if the transmitter is gated off while its echo would be wasted."
- **Problem:** "Which pay if" is hard to parse.
- **Proposed rewrite:** "it also permits brighter channels, which save power only if each transmitter is switched off during the last $\tau$ of every ramp, when its echo would land in a discarded window (subsection 2(i))."

**39.** **Line** 5291 — **Category** A/C — **Severity** low
- **Quote:** "Electrical energy per point is the sensor's electrical power $P$ divided by its point rate, $E=P/\dot N$ [E from P]."
- **Problem:** A bare $E$ collides with $E_{\rm opt}$, $E'$, $E_{\rm ph}$ and $E_{\rm rx}$. "[E from P]" is not a house tag. The table has no takeaway.
- **Proposed rewrite:** "…divided by its point rate, $E_{\rm el}=P/\dot N$ [E, from [P] vendor figures]. The FMCW products spend 30–390 µJ per point against 2–9 µJ for the ToF products: an order of magnitude or more, though at different ranges and fields."

**40.** **Line** 5342 (ski-jump wording) — **Category** D — **Severity** low
- **Quote:** "68.6 M spots s⁻¹ mm⁻², ">50-fold" state-of-the-art MEMS mirrors,"
- **Problem:**
  - Words are missing ("that of").
  - "a ≈0.5–0.66 µm mode" (5339) does not say diameter or radius, while 5357 uses $w_0\approx0.3$ µm as a radius.
  - $w_0$ is reused from the 9 mm beam at 4917.
- **Proposed rewrite:** '68.6 M spots s⁻¹ mm⁻², ">50-fold" that of state-of-the-art MEMS mirrors,'. At 5339: "a mode ≈0.5–0.66 µm across (1/e² diameter)". At 5357: use $w_{\rm tip}\approx0.3$ µm.

#### 3. Consistency flags to check elsewhere

- **Dwell definitions differ by section.**
  - §C0 table (1577) and §C7 Eq. (89) (4540): $T_{\rm dwell}\approx T_{\rm up}+T_{\rm down}$.
  - §C7a Eq. (96) (4738): $2T=10$ µs, no round trip; Eq. (94) (4721) uses the whole chirp.
  - §C7b Eq. (107): $E_{\rm opt}/P_{\rm ch}+2\tau$.
  - Knock-on: 10 Mpts/s needs 100 channels in §C7a (4743) but 127 in §C7b (5262).
- **Symbols.**
  - Wall-plug efficiency: $\eta_{\rm wp}$ (§C7a 4709, 4787; Eq. (122)) vs $\eta_{\rm WPE}$ (Eqs. (118)–(120); 4857).
  - Overhead: unnamed 3 W (§C7a 4626, 4790) vs $P_0$ vs $P_{\rm oh}$.
- **Equations re-tagged.** Eq. (97) = Eq. (93) (4678). Eq. (101) = Eq. (146) (§C10.3b). Eq. (109) ≈ Eq. (94). Eq. (121) = Eq. (89) rearranged. Cite the earlier tag.
- **Range scaling of coherent energy.** §C7a(e) (4754) uses $R^2$ ("$30\times(250/200)^2=47$ mW"). §C7b 1(f) (4983) and the 300 m case ($E'=0.45$ µJ, 5146) use $R$. Line 5301 uses $R^2$.
- **Laser linearity.**
  - The Waymo DFB claim is the same in §C7a (4763) and §C7b (5087); finding 2 applies to both.
  - §C7a 4764 treats the SiN (0.65%) and TFLN (1.5%) "nonlinearities" as $\varepsilon$ directly. If those are $\delta\nu/B$ figures, the definition at 5083 makes them up to 8× worse.
- **Eye safety.** §C7a 4709 ("FMCW's 3.0–7.6 W … fits within") has the same dead-time omission as 5226.
- **Parity conditions disagree.**
  - §C7a §5 item 1 (4811) asks for "≥100 mW per channel"; §C7b gives 15–30 mW at parity (5407) and says more power per channel is not the lever (5213–5217).
  - §C7a item 3 (4813) asks for "sub-100 kHz" lasers, but §C7b shows 100 kHz costs ×2.3 energy at 200 m, and a 1 dB loss needs ≤27 kHz (5113).
  - §C7a lists five conditions; §C7b says three.
  - Parity is "200–300 m" in §C7a (4825) but "200 m" in §C7b (5372).
- **Totals for different cases sit side by side.**
  - ≈68 W (10 Mpts/s, 300 m: 4857, 5192, §C7a 4767);
  - ≈67 W (15 Mpts/s, 200 m: 4867, 5386);
  - 46 W (§C7a table, 4780: 10 Mpts/s, 200 m).

  Each is correct for its own case, but none is labelled together with the others.
- **Signposts.** §C10.7 (6810) asks for "≥256 simultaneous channels … within about 10 W"; §C7b 5418 and 5449 ask for "≥256 receivers at ≤5 mW". The channel requirement also varies: 4864 vs 5406 vs 5416 vs 5420.
- **Search range for the receiver energy.** §C7a's 12,300 samples are for the 0–300 m search (4670, 4724), but §C7b applies the resulting 2.23 µJ to the 200 m case (5279, 5386), while 2(c) gives 8,900 samples "at 200 m" (5053). State once which range a 200 m sensor digitizes.
- **Background events.** 4893 gives ≈5,960 (exactly 5,968; same as §C0 2018); §C7a 4740 gives ≈5,990, which adds the 25 signal counts. Say so where the two appear.
- **520-line ToF unit.** 5289 compares FMCW receivers at 15 Mpts/s with §C7a's 520-line ToF unit, which is at 12.5 Mpts/s (4755).
- **Efficiency wording.** "At the optimistic end of what has been measured" also appears in §C0 10.1 (1915) and §C7a (4697). §C0 2438 says it correctly ("lies above both measured chains"). Use one wording in all four places.

I found no versioning language in the block (the only "now", at 5072, is physical), no `\( \)` or `\[ \]` delimiters, and no currency amounts.

### §C10 introduction to §C10.3 (optical phased arrays, photon arithmetic)

### Review of §C10 intro, C10.1, C10.2, C10.2b and C10.3 (lines 5733–6111)

**Coverage.** The whole block, lines 5733–6111, was read. The cross-check of §C3a stopped at line 2625.

#### 1. Overall assessment

The block is easy to check. Almost every number has a "How the numbers are derived" list, and Eqs. (130)–(141) are numbered and cited correctly. I recomputed about 80 substitutions, including the speckle thresholds 130/61/45/42 and the Marcum value 20.8. Only rounding slips turned up.

Three problems run through the whole block:
- **Different assumptions for the same quantity.** The photon arithmetic in §C10.3 uses different conventions from §C10.2 and from the §C0 primer:
  - $\eta$ sometimes includes the polarization factor ½ and sometimes does not.
  - The coherent thresholds are 10–30 photons, against the report's own per-point rule of 39–259.
  - The ToF threshold of 20 is labelled "no sunlight", but it is already the bright-sun value.

  As a result, the §C10.3 headline (20–184 W) and the §C10.2 item 5 figure (0.5–1.6 kW) disagree by about 10× for the same coverage. The two are reconciled only in a caveat.
- **Key terms drift.**
  - "Camera-like" means 0.025° (about 1,000 rows) in one place and "2,000+ lines" in another.
  - $\theta$ stands for the beamwidth, the emission angle and the cell width.
  - "Fill", "coverage" and "nominal footprint fraction" are used for the same thing.
  - Summary bullets use terms before they are defined.
- **Structure.** Many bullets are really paragraphs with long bracketed derivations. The "seven findings" of §C10.2b do not map onto the "seven constraints" of §C10.2.

#### 2. Findings

1. **Line** 5991 — **A/B** — **high**
   - **Quote:** "At a fixed photon budget, gap-free single-mode coherent coverage of 120° × 25° to 200 m ideally needs 20–184 W, against 0.23–14.4 W for ToF"
   - **Problem:** The same coverage costs 0.5–1.6 kW in §C10.2, item 5 (line 5880) and 180–1,590 W in caveat 4 (line 6052). The headline uses $N_{\rm req}=10$–30, which is below even the report's non-fading per-point value of 39. It does not state the 10% target or the 10 Hz frame rate, and "at a fixed photon budget" is undefined.
   - **Proposed rewrite:** "For a 10% target at 200 m and 10 Hz, gap-free single-mode coherent coverage of 120° × 25° needs 20–184 W at a non-fading threshold of 10–30 detected photons, and about 180–1,590 W once speckle fading is counted under the report's per-point rule (caveat 4; §C10.2, item 5). ToF needs 0.23–14.4 W at 0.1° to 0.0125° sampling." In line 5998, replace "roughly those for a non-fading return" with "bracket the single-bin non-fading requirement (≈21) and lie below the per-point one (≈39)".

2. **Line** 5741 — **A** — **high**
   - **Quote:** "Does the push to **2,000+ line, "camera-like" lidar** (2,000 or more rows of points in the vertical) create value?"
   - **Problem:** §C10.1 defines camera-like as 0.025–0.03° (lines 5773 and 5780). Over a 25° field that gives 830–1,000 rows, not 2,000. 2,000 rows over 25° is a 0.0125° pitch. The reader cannot tell which pitch the verdicts refer to.
   - **Proposed rewrite:** "4. Does the push to **"camera-like" lidar** create value? Here camera-like means about 0.025–0.03°, an 8 MP camera's pixel pitch over 120° (§C10.1). Vendors' "2,000+ line" claims go further: 2,000 rows over a 25° vertical field is a $25^\circ/2{,}000=0.0125^\circ$ pitch." Add the same sentence after line 5780, pointing to the 0.0125° row of the §C10.3 table.

3. **Line** 5997 (also 5865, 6042, 6061) — **A** — **high**
   - **Quote:** "The values of $\eta$ below are assumed to include whatever polarization loss applies."
   - **Problem:** In Eqs. (134) and (137)–(139), $\eta$ includes the polarization factor ½ (item 5 uses $\eta=0.4$ = 0.5 × 0.8). Eq. (140) carries the ½ explicitly, and §C0 (line 1914) keeps "mode and polarization factors" out of $\eta$. So the same symbol differs by 2× within the block and against the primer. This also makes the "ideal" $A_{\rm mode}=3.2$ mm² look 2.4× larger than the 1.32 mm² that §C10.3b gives for the same cell. Line 6042's conditional leaves the reader unsure which factor applies to the table.
   - **Proposed rewrite:** Adopt §C0's convention: "As in §C0 (subsection 10.1), $\eta$ excludes polarization. The factors ½ and $t^2$ belong to $A_{\rm mode}$, so a cell-filling mode has $A_{\rm mode}=\tfrac{t^2}{2}\lambda^2/\Omega_{\rm cell}=1.32$ mm² at 0.05° (§C10.3b)." Then use $\eta=0.8$ in item 5. If the block's convention is kept instead, rename the symbol ($\eta'$) and replace line 6042 with: "Because $\eta$ here already includes polarization, only $t^2\approx0.84$ applies, raising the coherent powers by ≈19%."

4. **Line** 6021 (also 6002, 6049) — **B/A** — **high**
   - **Quote:** "The assumed inputs are, for ToF: 905 nm, 25 mm aperture, $N_{\rm req}=20$, $\eta=0.15$."
   - **Problem:** No source or reason is given for either input. Under the report's own rule (§C0 subsection 10.3, lines 2050–2051), an ideal counter needs 5.3 counts at night and 17.3 in bright sun, and the model uses 25. So 20 is already a bright-sun value. Yet line 6002 says solar background "is left out", and caveat 4 says sunlight would raise $N_{\rm req}$.
   - **Proposed rewrite:** "…$N_{\rm req}=20$ [E: close to the bright-sun requirement of §C0 subsection 10.3, 17.3 counts for an ideal counter at 940 nm and 25 in the §C7a model; 5.3 suffice at night] and $\eta=0.15$ [E: about the §C7a value, 0.5 × 0.37 × 0.784 = 0.145]." Change line 6002 to: "*Sunlight.* $N_{\rm req}=20$ already corresponds to bright sun; a fully sunlit scene of reflectance 0.9 raises the ideal requirement only to ≈20 (§C0 subsection 10.3)."

5. **Line** 5877 (also 5873) — **A** — **high**
   - **Quote:** "with ≤3 dB one-way loss, ≈9 W for four-look and ≈26 W for single-look detection, or ≈540–1,590 W for 60 beams at 12 Mpts/s."
   - **Problem:** "≈9 W for four-look" divides the four-look total of 88.5 photons by what one receive mode collects. That assumes the four looks share one mode (wavelength or time diversity). But line 5873 also lists polarization and spatial diversity, and §C10.3 caveat 4 (line 6052) says those "collect four times as much"; with them the figure would be ≈2.3 W per beam. Smaller issues: "several watts" understates 9–26 W, "≤3 dB" should be "at 3 dB", and the bullet also carries the separate Si/SiN power-handling point.
   - **Proposed rewrite:** "- about 9–26 W per beam at 5 µs dwell and 3 dB one-way loss [E], if the looks share one receive mode (wavelength or time diversity): 88.5 photons need $88.5/9.8=9.0$ W and 259 need $259/9.8=26.4$ W; 60 beams at 12 Mpts/s need 540–1,590 W. With polarization or spatial diversity each look adds a mode, which cuts the four-look figure about 4×, to ≈2.3 W per beam (≈135 W for 60 beams)." Move "Si trunks … SiN handles watts" into its own bullet. In line 5873 add: "Wavelength or time diversity splits one mode's photons, so the total counts; polarization or spatial diversity adds a mode per look, so the per-look figure counts (§C10.3, caveat 4)."

6. **Line** 5759 — **A** — **high**
   - **Quote:** "and its usable aperture shrinks at fixed f-number (focal length divided by aperture diameter)."
   - **Problem:** No mechanism is given. The relation the reader is sent to, $D=p_{\rm px}/(\theta F_\#)$ in §C10.3a item 7, makes the aperture *grow* as the pixel angle falls (14 → 29 → 57 mm). The real constraint is that the module caps the lens size. The pointer "§C10.3a, item 7" is also attached to the coherent sentence, but item 7 is about ToF.
   - **Proposed rewrite:** "At fixed range and aperture, ToF's required power scales as $1/\Omega_{\rm cell}$ (§C10.3, Eq. (139)). The aperture cannot grow to compensate: at a fixed f-number and macro-pixel size a finer pixel angle needs a larger lens, a behind-glass module holds only about 25–30 mm, so the pixels must shrink instead (§C10.3a, item 7). Ideal full-coverage coherent power does not grow as $1/\Omega_{\rm cell}$ (§C10.3, Eq. (139); §C10.3a, item 4)."

7. **Line** 6065 — **A** — **medium**
   - **Quote:** "It needs about 50 photons per detection, a −106 dB link (the ratio of received to transmitted power) and 0.52 µJ per shot"
   - **Problem:** Line 5868 says one fading look at the same $P_d$ and $P_{\rm fa}$ needs ≈130 photons. The text does not say that Waymo's 50 assumes four averaged speckles in one ramp (§C0, line 2072). Without that, the two figures look contradictory.
   - **Proposed rewrite:** "It needs about 50 detected photons with four averaged speckles searched in one chirp ramp [P] (close to the 45 for $L=4$ in §C10.2, item 5; the both-ramp per-point rule raises it to 88.5, §C0 subsection 10.3), a −106 dB link … and 0.52 µJ per shot at $1.2\times10^{7}$ shots/s."

8. **Line** 6045 — **A** — **medium**
   - **Quote:** "That is exactly how FMCW products position themselves: as long-range, narrower-field truck sensors (§C7, §F6)."
   - **Problem:** The $R^2\Omega$ table further down lists FMCW products with full 120° × 25–30° fields (LuminWave F1, LightIC Lark, Aeva Atlas), and line 6109 says they accept sparse coverage instead. Also, "is demanding" in the same item is a vague hedge for 20–184 W.
   - **Proposed rewrite:** "1. **In this fixed-threshold example, gap-free single-mode coverage of a full field to 200 m needs 20–184 W even before speckle (caveat 4).** … It must also narrow its field, lower its point rate or accept sparse footprints: some FMCW products are long-range, narrower-field truck sensors (§C7, §F6), while the scanned 120°-wide ones sample sparsely (see the $R^2\Omega$ table below)."

9. **Line** 5937 (also 5935) — **A** — **medium**
   - **Quote:** "a gap of one to two orders of magnitude, not a calibration detail."
   - **Problem:** The "gap" is not measured against anything. In line 5935, the 1,360 nJ value has no device or range, yet it is scaled from 35 m as if it were the 8,192-element result. The text does not say whether these are optical energies, and "Rogers et al." is not identified.
   - **Proposed rewrite:** "At 12 Mpts/s this is about 530–670 W of optical power (…), 15–19× the 35 W of the FS-4S and 66–84× the 8 W of the Hesai ATX: a gap of one to two orders of magnitude, not a calibration detail." In line 5935: "Optical energy per point … 1,360 nJ ([device, range, reflectance]) to 1,700 nJ (8,192 elements, 35 m at 10%) … 212 nJ for the 512-pixel coherent FPA of Rogers et al. (§C10.4)". If 1,360 nJ was not measured at 35 m, scale it from its own range.

10. **Line** 5945 — **B** — **medium**
    - **Quote:** "Funding is mostly government contracts and grants; amounts are not disclosed, so treat any figure with a grain of salt."
    - **Problem:** §C3a (lines 2617–2625) gives \$45.2 M of federal prime obligations [I], and line 4459 repeats ≈\$45 M. "Not disclosed" contradicts this, and "any figure" has nothing to refer to. The "Who they are" paragraph (line 5943) also duplicates the §C3a profile.
    - **Proposed rewrite:** "Funding is mostly US government contracts and grants: about \$45 M of federal prime obligations on USAspending, mainly DARPA and ONR (§C3a) [I]; private funding is not disclosed." Replace the history in line 5943 with "Company background is profiled in §C3a."

11. **Line** 5925 — **A** — **medium**
    - **Quote:** "DTU's 120-element array spread over 6 mm has a *simulated* main-lobe fraction of 0.8% and a *measured* floor only 3–6 dB below the peak."
    - **Problem:** The finding says these data "bear out" §C10.1, but shows no $N/N_{\rm spot}$ for this array. The measured 3–6 dB floor is also far above the $1/N\approx-21$ dB mean sidelobe that §C10.1's rule gives for $N\approx120$, and no reason is given.
    - **Proposed rewrite:** "…a *simulated* main-lobe fraction of 0.8%, the order of $N/N_{\rm spot}$ for that aperture [E: give $N_{\rm spot}$]. Its *measured* floor, only 3–6 dB below the peak, is far above the $1/N\approx-21$ dB mean of §C10.1 because [reason, e.g. the camera's 0.13° resolution sums many sidelobe spots]."

12. **Line** 5796 — **A** — **medium**
    - **Quote:** "the aperture length $D$ that gives the required beamwidth $\theta$ (full width at half maximum, FWHM, in radians)"
    - **Problem:** $\theta$ is the beamwidth in Eq. (130), the emission angle in Eqs. (131)–(132) only 25 lines later, the steering angle at line 5785, and the cell width at lines 6046 and 6064.
    - **Proposed rewrite:** Use $\theta_{\rm B}$ for the beamwidth in Eq. (130) and its derivation ($D=0.886\,\lambda/\theta_{\rm B}$), keep $\theta$ for the emission or steering angle, and write $\theta_{\rm cell}$ at lines 6046 and 6064.

13. **Line** 5837 — **A** — **medium**
    - **Quote:** "Differentiating the grating equation at fixed wavelength gives the angle drift $\Delta\theta$ for a temperature change $\Delta T$"
    - **Problem:** The grating equation and the grating period are never written, so neither Eq. (132) nor Eq. (131) can be followed.
    - **Proposed rewrite:** Before Eq. (131): "A grating of period $\Lambda$ emits at $\sin\theta=n_{\rm eff}-\lambda/\Lambda$. Differentiating with respect to $\lambda$, with $n_g=n_{\rm eff}-\lambda\,dn_{\rm eff}/d\lambda$, gives Eq. (131)." At line 5837: "At fixed wavelength, $\cos\theta\,\Delta\theta=\Delta n_{\rm eff}$, which gives…"

14. **Line** 5890 — **A** — **medium**
    - **Quote:** "0.2–1 GHz beat at 300 m, i.e. 0.4–2 GS/s (gigasamples per second) real sampling, doubled for up/down chirps, plus about ±0.1 GHz of Doppler."
    - **Problem:** It is unclear what doubles. It could be the sample count, the data volume, or the rate (splitting the dwell into two ramps doubles $f_b$ by Eq. (136)).
    - **Proposed rewrite:** "…a 0.2–1 GHz beat at 300 m for a single 10–2 µs ramp, i.e. 0.4–2 GS/s. If the dwell is split into an up-ramp and a down-ramp, each is half as long, so by Eq. (136) the beat and the sampling rate double, to 0.8–4 GS/s. Doppler adds about ±0.1 GHz."

15. **Line** 6051 (also 6052) — **B/D** — **medium**
    - **Quote:** "The choices of $N_{\rm req}$ and $\eta$ move the numbers by a few times but do not change the scaling."
    - **Problem:** The next bullet shows speckle moving the coherent power about 9× (20.4 → 181 W), not "a few times". In line 6052, the condition "If the looks share one mode's collection" is applied to the whole 180–1,590 W range, but 1,590 W is the single-look case.
    - **Proposed rewrite:** "The choice of $\eta$ moves the numbers by up to 3×, and speckle raises the coherent $N_{\rm req}$ about 9–26× (next bullet); neither changes the scaling with $\Omega_{\rm cell}$." In line 6052: "…rises to about **180 W** (four looks sharing one mode, $\eta=0.3$) to **1,590 W** (one look, $\eta=0.1$)…"

16. **Line** 6062 — **A** — **medium**
    - **Quote:** "**A larger useful aperture can buy photons at the cost of sparser angular sampling.**"
    - **Problem:** Waymo's example still samples every 0.05° cell. What it loses is coverage, as lines 5895 and 6015 say.
    - **Proposed rewrite:** "**A larger useful aperture can buy photons at the cost of coverage: the sampling pitch is unchanged, but narrow footprints leave gaps between samples.**"

17. **Line** 5782 (also 5747) — **A** — **medium**
    - **Quote:** "**A degrees-of-freedom rule links every steerer** [E; standard antenna theory]:"
    - **Problem:** Line 5784 then says that one control (mirror tilt, wavelength sweep) can address many directions. That contradicts "every steerer" and the summary rule at line 5747.
    - **Proposed rewrite:** "**A degrees-of-freedom rule links every steerer that sets its phase element by element** [E; standard antenna theory]:" At line 5747, add: "…; whole-aperture phase ramps (mirror tilt, wavelength sweep) escape this at a cost in dwell, bandwidth or loss (§C10.1)".

18. **Line** 5753 (also 5748) — **C/A** — **medium**
    - **Quote:** "Full nominal coverage needs $A_{\rm mode}\lesssim\tfrac{t^2}{2}N_{\rm cell}\lambda^2/\Omega_{\rm FOV}$, where $N_{\rm cell}$ is the number of FPA cells"
    - **Problem:** This summary bullet carries a five-symbol inequality. It uses "nominal coverage" and "fill" before "nominal footprint fraction" is defined at line 5760. It omits the 1.31 µm wavelength needed to reproduce "<1 mm". By contrast, line 5748 ("the second steering axis;") gives no reason at all.
    - **Proposed rewrite:** "For Pointcloud's coherent FPA (*Nature* 2026), covering its whole field would leave a mode-equivalent collecting area equal to a lens under 1 mm across; at the ≈2% nominal footprint fraction it actually uses (defined below), it gets ≈6 mm (§C10.3a, item 5)." Move the inequality to §C10.3a. Line 5748: "the second steering axis: phase control on both axes needs about $10^6$ shifters, and wavelength steering of 25° needs ≈160 nm of tuning on Si (§C10.2, item 2);"

19. **Line** 5900 — **C** — **medium**
    - **Quote:** "This subsection checks the seven constraints of §C10.2 against devices that have actually been built and measured."
    - **Problem:** The findings come in a different order (finding 5 checks constraint 2, finding 6 checks constraint 3). Finding 2 checks §C10.1, not §C10.2. Constraints 6 (receive étendue) and 7 (point rate) are never checked.
    - **Proposed rewrite:** Either reorder the findings in §C10.2's order, each opening with its pointer, and add lines for étendue and point rate (e.g. 28.6 kpts/s against 12 Mpts/s). Or write: "This subsection compares measured devices with §C10.1 and §C10.2; seven findings follow."

20. **Line** 5788 — **A** — **medium**
    - **Quote:** "A Monte Carlo check with random sparse arrays gave **8.5%** main-lobe power for $N=128$ and $N_{\rm spot}\approx1{,}140$"
    - **Problem:** The inputs are not given: aperture length, placement rule, the steering range that sets $N_{\rm spot}$, and the number of trials. The $N/N_{\rm spot}$ prediction is missing for $N=256$ (15%, against the 12% found).
    - **Proposed rewrite:** "A Monte Carlo check [E] placed $N$ elements at random over an aperture of [length], steered over [range] ($N_{\rm spot}\approx1{,}140$ for $N=128$, ≈1,720 for $N=256$), over [n] trials… For $N=256$ it gave 12% ($N/N_{\rm spot}=15\%$), −12.6 dB and −24 dB."

21. **Line** 6073 — **C/E** — **medium**
    - **Quote:** "| Analog Photonics FS-4S | about 3.6% (box convention; 2.8% as a FWHM ellipse; ≈8% at 1/e² if the datasheet widths are FWHM) |"
    - **Problem:** One column mixes three conventions, and Waymo's headline value uses a different one from the other rows. The FPSA values have no pointer to where they are derived.
    - **Proposed rewrite:** Use columns "| Design | Box (quoted widths) | FWHM ellipse | Gaussian 1/e² |":
      - FS-4S: 3.6% / 2.8% / ≈8% (if the widths are FWHM)
      - Berkeley FPSA (§C10.4): 0.7% / ≈0.55% / ≈1.6%
      - Waymo: — / 0.6% / 1.6–1.8%
      - ToF column receiver: pixels tile the field (≈100%)

22. **Line** 5787 — **A** — **low–medium**
    - **Quote:** "while the angle-averaged intensity scales as $N$ and spreads over $N_{\rm spot}$ spots. The main-lobe power fraction is therefore about $N/N_{\rm spot}$"
    - **Problem:** The step from intensities to a power fraction is skipped.
    - **Proposed rewrite:** "Normalize one element's intensity to 1. The main-lobe peak is $N^2$ and the angle-averaged intensity is $N$. The main lobe fills one of $N_{\rm spot}$ resolvable spots, so it carries $N^2/N_{\rm spot}$ of a total $N$ (in units of the steering range), a fraction $N/N_{\rm spot}$; the mean sidelobe level is $N/N^2=1/N$ of the peak."

23. **Line** 5784 (also 5885) — **A/E** — **low–medium**
    - **Quote:** "Examples are mirror tilt, a wavelength sweep through a dispersive grating, and row–column addressing (§C10.3a, item 5b)."
    - **Problem:** §C10.3a has no item 5b. The meaning is item 5, "bite" (b). Line 5885 uses "bite (a)", a coinage that is defined only later.
    - **Proposed rewrite:** "(§C10.3a, item 5, limit (b): the steering space–bandwidth product)" and "(§C10.3a, item 5, limit (a): receive modes per unit time)".

24. **Line** 5882 (also 5755) — **C** — **low–medium**
    - **Quote:** "**6. The OPA does not by itself solve the ToF receive problem.**"
    - **Problem:** "ToF receive problem" is never defined; the intro at line 5794 calls this constraint "receive étendue". Line 5755 also uses "the solid-state *receive* problem" before it is explained.
    - **Proposed rewrite:** "**6. Receive étendue: an OPA collects only one spatial mode.** A long-range ToF receiver needs a large multimode aperture looking along the beam; an OPA does not provide one." At line 5755, add "(collecting many spatial modes from the steered direction, §C10.2, item 6)".

25. **Line** 5854 — **D** — **low–medium**
    - **Quote:** "Measured one-way suppression of 10–19 dB (§C10.2b) gives only 20–38 dB two-way, 20–38 dB short of the 58 dB retroreflector case."
    - **Problem:** The repeated range reads like a typo, and the shortfall actually runs in the opposite order.
    - **Proposed rewrite:** "…gives only 20–38 dB two-way, leaving the 58 dB retroreflector case 38 dB short (10 dB devices) to 20 dB short (19 dB devices)."

26. **Line** 5934 (also 5763) — **A** — **low–medium**
    - **Quote:** "35 m at 10% (8,192 elements), about 50 m (9,216), 22 m (Jilin), 20 m (imec)."
    - **Problem:** The 50, 22 and 20 m results have no reflectance, so they cannot be compared with the 10% standard. The "100 m on a 90% target" result names no device and is not in the table.
    - **Proposed rewrite:** "35 m at 10% (8,192 elements), about 50 m at [ρ] (9,216), 22 m at [ρ] (Jilin), 20 m at [ρ] (imec). [Device, year] reached 100 m, but only on a 90% target (≈33 m at 10%) [S]." Add that device to the table.

27. **Line** 5929 — **D** — **low–medium**
    - **Quote:** "Correlated waveguide-width errors make uncalibrated phases effectively random: about 12 rad per nm of width error per mm of Si path"
    - **Problem:** "Correlated … random" reads as a contradiction. "Phase-coherence length" is undefined, and the [I] tag has no source.
    - **Proposed rewrite:** "Waveguide-width errors, correlated along each guide, accumulate about 12 rad per nm of width error per mm of Si path, so after a few millimetres the uncalibrated phases are effectively random. The Si phase-coherence length ([definition, e.g. the path over which the random phase reaches 1 rad rms]) is about 1.6–4 mm [I: source]."

28. **Line** 5828 — **B/D** — **low**
    - **Quote:** "narrow-linewidth (≲20–55 kHz at 300 m for a 1–3 dB coherent loss, §C7b subsection 2(e); Waymo designs to ≲60–120 kHz at 250 m, §C10.3)"
    - **Problem:** The cited §C7b table gives 18.3 kHz, not 20, at 1 dB. The parentheticals are nested, and the reader is not told why Waymo's limit is looser.
    - **Proposed rewrite:** "The laser must therefore be widely tunable, linearly chirped, cheap and narrow in linewidth at once. A 1–3 dB coherence loss at 300 m allows ≲18–55 kHz (§C7b, subsection 2(e)); Waymo's ≲60–120 kHz at 250 m accepts a 2.7–5.5 dB loss (§C7a(f))."

29. **Line** 5802 — **A** — **low**
    - **Quote:** "| Alias-free FOV (no grating lobe inside the FOV) | Max pitch $\lambda/(2\sin\tfrac{\rm FOV}{2})$ | 0.1°: aperture / elements | 0.05° | 0.025° |"
    - **Problem:** The headers do not say that 0.1/0.05/0.025° are FWHM beamwidths, while §C10.1 uses the same numbers as sampling pitches. No sentence introduces the table.
    - **Proposed rewrite:** Add "The table evaluates Eq. (130) for three fields and three beamwidths:" and use the header "Beamwidth 0.1°: aperture / elements".

30. **Line** 6004 (also 6009, 6019) — **A/D/E** — **low**
    - **Quote:** "the photons reaching a direct detector are approximately"
    - **Problem:** Eq. (137) includes $\eta$, so it counts *detected* photons. "Do not multiply by cell étendue again" (line 6009) reads as a note to self. Eq. (139) is very wide.
    - **Proposed rewrite:** "…the number of photons a direct-detection receiver detects is approximately". Line 6009: "The receiver's étendue adds no second factor: the lens collects light from the whole illuminated cell whatever its size." Split Eq. (139) over two lines in one aligned block under \tag{139}.

31. **Line** 6027 — **B** — **low**
    - **Quote:** "| 0.1° × 0.1° | 0.23 W | 87–800× |"
    - **Problem:** The other rows use the unrounded $P_{\rm ToF}$. Done the same way, 20.4/0.225 = 91 and 184/0.225 = 818.
    - **Proposed rewrite:** "| 0.1° × 0.1° | 0.23 W | 91–820× |". In line 6046: "$0.1^\circ/\sqrt{91}=0.010^\circ$ to $0.1^\circ/\sqrt{820}=0.0035^\circ$".

32. **Line** 5841 (also 5927, 5877) — **B** — **low**
    - **Quote:** "or about 25 cells at 0.05° ($1.3^\circ/0.05^\circ\approx26$);"
    - **Problem:** The prose and the arithmetic disagree. The same kind of slip appears in three more places:
      - Line 5927: "its peak is about 9 dB higher", against the computed 8.4 dB.
      - Line 5877: "$259/9.8=26.5$ W"; the quotient is 26.4.
      - Line 5841: "$\Delta\theta\approx1.6\times10^{-4}$ rad/K" is a per-kelvin rate written with the symbol for an angle.
    - **Proposed rewrite:** "about 26 cells (…$=26$)"; "about 8 dB higher"; "$259/9.8=26.4$ W"; "$\Delta\theta/\Delta T\approx1.6\times10^{-4}$ rad/K".

33. **Line** 5820 — **E** — **low**
    - **Quote:** "2D phase control for 2,400×500 spots would need about 1.2 M phase shifters. Published 2D arrays are orders of magnitude smaller."
    - **Problem:** The claim has no number or tag. Line 5821 puts [E] on a statement of common practice rather than on the estimate below it.
    - **Proposed rewrite:** "…the largest published 2D phase-controlled array has [N] elements [P: source]." Move the [E] tag to the Si/SiN tuning estimates.

34. **Line** 5975 (also 5939, 5945, 5746–5760) — **E** — **low**
    - **Quote:** "Per 2024 press reports, its target price is under \$200 [I]."
    - **Problem:**
      - Press reports should carry [T].
      - The CEO talk at line 5945 is a company statement but is tagged [I].
      - "rendered and read" at line 5939 is a working note.
      - The summary verdicts carry no [D]/[NT]/[R] deployability tags.
    - **Proposed rewrite:** "…under \$200 [T]."; "[P, company datasheets Rev A, June–July 2025; figures are vendor claims]"; add [D]/[R] to the verdict bullets.

35. **Line** 6092 (also 6090) — **B/D** — **low**
    - **Quote:** "Scanned coherent products claim $R^2\Omega$ comparable to scanned ToF, at higher power; solid-state coherent designs sit one to two orders of magnitude below."
    - **Problem:** Pointcloud's ≈140 m²·sr is ≈280× (2.4 orders) below the ATX. The heading says "range × field" for range squared times field.
    - **Proposed rewrite:** Heading "**Reality check: range² × field ($R^2\Omega$)…**". Sentence: "…solid-state coherent designs sit about 16–24× (FS-4S) to 280× (Pointcloud) below."

36. **Line** 6097 (also 5771, 5985) — **E** — **low**
    - **Quote:** "90k / 400k pts/s; 35 W"
    - **Problem:** The point-rate column mixes "Mpts/s", "k pts/s", "128 lines" (not a rate) and "not disclosed". §C10.1 writes "M/s", and line 5985 gives a rate as "1.5 MHz".
    - **Proposed rewrite:** "0.09 / 0.4 Mpts/s; 35 W"; for LuminWave "not disclosed (128 lines); <45 W"; "3 / 12 / 48 Mpts/s" in §C10.1; "1.5 Mpts/s (stated as 1.5 MHz)".

37. **Line** 5835 (also 5874) — **D** — **low**
    - **Quote:** "as the Strehl-type factor $e^{-\sigma^2}=e^{-0.09}=0.914$ predicts ($0.90\times0.914=0.82$)."
    - **Problem:** The Strehl factor is used before it is defined, and the Marcum function at line 5874 is used the same way.
    - **Proposed rewrite:** "The Strehl factor $e^{-\sigma^2}$ is the fraction of peak intensity kept when uncorrelated phase errors of rms $\sigma$ (rad) are present. For $\sigma=0.3$ rad it is $e^{-0.09}=0.914$, lowering the ideal 90% main-lobe share to $0.90\times0.914=82\%$, as the Monte Carlo finds." Reorder the Marcum sentence the same way.

38. **Line** 5875 (also 5735, 5758, 6004) — **D** — **low**
    - **Quote:** "The report's per-point rule (§C0 subsection 10.3: at most $10^{-3}$ false points per point over a 0–300 m search"
    - **Problem:** This sentence runs to about 55 words, most of it a parenthetical. Lines 5735 and 5758 have other sentences over 40 words, and the symbol list at line 6004 is packed into one long sentence.
    - **Proposed rewrite:** "The report's per-point rule is stricter: at most $10^{-3}$ false points per point over a 0–300 m search, with the peak found in both chirp ramps (§C0 subsection 10.3). It raises the requirements to ≈259 photons for one look, 120 for two, 88.5 for four, 82 for eight and 39 for a non-fading return." Turn the symbols at line 6004 into a bullet list.

39. **Line** 5860 — **D/C** — **low**
    - **Quote:** "The number of detected signal photons $N_s$ from one pulse is the number of transmitted photons"
    - **Problem:** The example is an FMCW chirp (1 W for 5 µs), not a pulse. Several things are named or defined more than once:
      - The same energy is $E_{\rm pulse}$ here, $E_s$ in Eq. (137) and $E_{\rm tx}$ in §C0.
      - Eq. (138) is Eq. (134) with $\eta_{\rm OPA}=1$, but the text does not say so.
      - $A_{\rm mode}$ is defined three times (lines 5753, 5864, 6010) and $R^2\Omega$ three times (5963, 6021, 6092).
    - **Proposed rewrite:** "…from one sample (one chirp or pulse)…", using $E_s$. At Eq. (138) add "(Eq. (134) with $\eta_{\rm OPA}=1$)". Replace the repeat definitions with pointers.

40. **Line** 6064 — **D** — **low**
    - **Quote:** "They differ by convention and are not inconsistent measurements of scene coverage."
    - **Problem:** The bullet contains a derivation of about 90 words in brackets, and the closing sentence is a double negative.
    - **Proposed rewrite:** Move the bracket into a "*How the numbers are derived* [E]" list. Replace the sentence with: "The two figures differ only in the contour convention; neither measures scene coverage."

#### 3. Consistency flags to check elsewhere

- **$\eta$ convention and values.**
  - In this block $\eta$ includes the polarization ½ (lines 5865, 5997). §C0 keeps it out of $\eta$ (line 1914).
  - Converted to §C0's convention, item 5's $\eta=0.4$ becomes 0.8, and §C10.3's 0.3–0.1 becomes 0.6–0.2.
  - §C0's design value is 0.25, described as "the optimistic end" (line 1915).
  - So item 5 and the §C10.3 best case are about 2.4–3.2× more optimistic than the primer.
- **"120 photoelectrons".** In this block (line 5875) 120 is the *two-look* ideal requirement. §C0 subsection 10.4 (line 2093), §C7a (line 2113) and §C7b (lines 4840, 4935) use 120 as the *four-look model* value (30 per look). Readers may conflate the two.
- **Detection notation.** §C0 writes $P_D$, $P_{FA,{\rm pt}}$, $x_{\rm th}$, $N_{\rm sp}$, $n_{\rm req}$ and $E_{\rm tx}$. This block writes $P_d$, $P_{\rm fa}$, $\gamma_{\rm th}$, $L$, $N_{\rm req}$ and $E_{\rm pulse}$/$E_s$. Eq. (135) restates §C0's Eq. (38), and Eq. (140) restates Eq. (33).
- **ToF model in §C10.3.** Here it is 905 nm, $N_{\rm req}=20$, $\eta=0.15$, "no sunlight". The §C0/§C7a model is 940 nm, needs 5.3 counts at night and 17.3 ideal / 25 model in bright sun, with $\eta=0.145$ including the live fraction (lines 2019, 2050–2051, 2070). The sunlight figures in §C0 are for 940 nm.
- **Linewidth.** Line 5828 gives "≲20–55 kHz"; the §C7b 2(e) table gives 18.3 and 55.2 kHz (lines 5113–5114). Waymo's 60–120 kHz equals a 2.7–5.5 dB loss (line 4759).
- **Wrong pointer into this block.** §C7b line 5123 says "Pointcloud's external DFB, §C10.3". That laser appears only in §C10.4 (line 6517).
- **Walk-off beam width.** Line 6085 uses "a 0.003° beam" ($w_0=10$ mm). §C10.3a (lines 6314–6317) uses 0.0036° for the same 250 m, 360°-spin case.
- **Analog Photonics.**
  - Funding: "not disclosed" at line 5945, against \$45.2 M in §C3a (lines 2617–2625) and §C7 (line 4459).
  - Pitch and field: the 512-element device is 1.65 µm and 56° here (line 5907), but §C7 says "1.5 µm pitch, about 60°" (lines 4459, 4571).
  - Steering range: line 5954 says "14–17° in AP's papers", while the table gives 15° and 17°. "AP" is never defined.
- **Resolvable spots.** "About 10⁴ resolvable spots" (line 5924) is 100°/0.01° in degrees at broadside. In sine space it is ≈8,100, which matches the N-element rule of §C10.1 and §C10.3a line 6300 (8,192 controls).
- **Lumotive range.** The summary gives "≈10–50 m (§C10.5)" at line 5755, but §C10.5 also lists Namuga Stella-2 at "≤100 m" (around line 6629).
- **Camera-like.** §C10.1 uses 0.025–0.03° (lines 5773, 5780). §C10.6 says "2,000+ line" and "thousands of lines" (lines 6640–6642), and its table goes down to 0.0125°.
- **§C10.3a item 7 (line 6344).** Its heading, "Finer resolution shrinks ToF's usable aperture", sits above a table in which the aperture grows (14 → 29 → 57 mm). That is the source of finding 6 and should be checked in that block.
- **Loss.** Finding 4 (line 5930) says research devices lose 10–14 dB one-way. The FSOC-B1 datasheet in this block (line 5956) gives ≤7.5 dB fibre-to-beam. That vendor figure deserves a mention.
- **Pointcloud wavelength.** §C10.3a and §C10.4 use 1.31 µm (lines 6301, 6517). The summary bound at line 5753 omits it; using 1.55 µm gives 0.9 mm rather than 0.76 mm.
- **$t^2$ label.** Line 5866 calls $t^2$ a "mode-shape and truncation factor". §C10.3b (lines 6370, 6384) defines $t$ as one-way truncation only, with $t^2$ for transmit plus receive.

#### Follow-up cross-checks for this block (second pass, 2026-10-03; new findings only, against the report after both edit batches)

### Analog Photonics cross-check: §C3a profile against §C10 and §C10.2b

**What was checked.** The report, located by heading and quote; line numbers may be off by a line. The §C3a profile (table row at line 2623, profile at lines 2627–2654) was compared with:
- §C10: summary, §C10.2 item 3, §C10.2b and the §C10.7 verdict.
- Other places that mention the company: §C0 subsection 10.8, §C3c, §C7, §C7a, §C7b, §C10.3a, §D8 and Appendix 2.

#### 1. Overall assessment

The core facts agree everywhere:
- Founded about 2012 by Michael Watts, with the company's own timeline starting at a 2016 DARPA MOABB award.
- Two unnamed Tier 1 joint development agreements, in 2018 and 2020.
- The 8,192-element, 1 µm-pitch array reached 35 m at 10%.
- The FS-4S datasheet claims are the same in eight places: 200 m at 10% only in a 20° × 10° ROI at 90 kpts/s, 80 m over 60° × 14° at 400 kpts/s, 35 W, 2025.

Three problems remain:
- **Funding is given three ways:** "not disclosed" in §C10.2b, "≈\$45 M of federal contracts and grants" in the §C3a table, and ≈\$79 M including subawards in the §C3a profile.
- **Datasheet claims are stated inconsistently:** the FS-4S beam convention, FSOC-B1 random access against the RAY-H1 retune time, and the FSOC-B1 datasheet has no source link.
- **§C10.7's verdict sentences contradict the report's own labelling** of Voyant Carbon as an OPA-plus-mirror hybrid.

#### 2. New findings

1. **Line** 6848 (§C10.7; also 6845, 6847) — **B** — **medium**
   - **Quote:** "Analog Photonics is the one serious OPA-lidar developer still publishing datasheets, and its automotive milestones have not materialized on the stated timeline."
   - **Problem:** §C8 (line 5512, "hybrid (OPA + slow mirror, e.g. Voyant Carbon)") and §C10.2 item 2 (line 5848, "the Voyant Carbon type of hybrid") call Carbon an OPA hybrid. Carbon ships at \$1,490 with a public spec sheet (line 1310). Yet §C10.7 files Voyant under "switched FPAs" (line 6845) and says "The only OPA product that shipped was Quanergy's S3-2" (line 6847). Either Carbon's on-chip axis is not an OPA, in which case §C8 and §C10.2 are wrong, or these §C10.7 sentences need a "fully solid-state" qualifier.
   - **Proposed rewrite:**
     - Line 6847: "- The only fully solid-state OPA product that shipped was Quanergy's S3-2, at 5–20 m, and Quanergy went bankrupt; Voyant's Carbon, which pairs one on-chip steered axis with a slow mirror, ships for industrial use (§B8)."
     - Line 6848: "- Analog Photonics is the one serious developer of two-axis non-mechanical OPA lidar still publishing datasheets, …"
     - Line 6845: "Voyant: one on-chip axis plus a mirror (Carbon) and a switched FPA (Helium); Pointcloud: a switched FPA;"
     - If Carbon's axis is not an OPA, change §C8 and §C10.2 item 2 instead.

2. **Line** 2623 (§C3a table; also 2637) — **B** — **medium**
   - **Quote:** "≈\$45 M of US federal contracts and grants, mostly DARPA and ONR; SBIR only ≈\$4.3 M [I]"
   - **Problem:** The profile right below gives \$45.2 M of prime obligations plus \$34.2 M of subawards, ≈\$79 M in total (line 2643). The table counts only the prime money but does not say so. Line 2637 ("it lives on large DARPA and ONR contracts") also leaves out the subawards, although AIM Photonics alone (\$19.9 M) exceeds all the listed ONR prime money. §C7 (line 4476) correctly says "federal prime awards". §C10.2b still says "amounts are not disclosed" (earlier finding 10, line 5963).
   - **Proposed rewrite:**
     - Table: "≈\$45 M of federal prime contracts and grants (≈\$79 M with \$34.2 M of subawards, mainly from AIM Photonics), mostly DARPA and ONR; SBIR only ≈\$4.3 M [I]".
     - Line 2637: "…it lives on large DARPA and ONR prime contracts and on subawards, mainly from AIM Photonics."
     - §C10.2b: "Funding is mostly US government money: \$45.2 M of federal prime obligations and \$34.2 M of subawards, ≈\$79 M over 2013–2026 (§C3a) [I]; no venture round was found."

3. **Line** 2472 (§C0 subsection 10.8; also 5778, 5995, 6091) — **B** — **medium**
   - **Quote:** "with a beam of at most 0.04° × 0.02° FWHM."
   - **Problem:** §C0 states that the FS-4S beam widths are FWHM. The §C10 summary, §C10.2b and the §C10.3 footprint table all say "if the datasheet widths are FWHM". The same datasheet claim is given as fact in one place and as an assumption in three others, and the ≈8% 1/e² footprint fraction depends on which is true.
   - **Proposed rewrite:** Check the datasheet.
     - If it states FWHM: write "Beam ≤0.04° × 0.02° FWHM" in §C10.2b and replace the three conditionals with firm values (2.8% as a FWHM ellipse, ≈8% at 1/e²).
     - If it does not: change §C0 to "with a beam of at most 0.04° × 0.02° (width convention not stated)".

4. **Line** 5974 (§C10.2b products table) — **A/B** — **low–medium**
   - **Quote:** "50° × 14°, 1 mrad beam, ≤7.5 dB fibre-to-beam loss at up to 400 mW in, <10 µs random access, <5 W"
   - **Problem:** The row calls FSOC-B1 "The same engine" as the lidar. In the FS-4S the second axis (14° there too) is wavelength-steered, and the RAY-H1 row says that axis "can be re-addressed only about every 300 µs". Random access in under 10 µs across 50° × 14° would need a laser retune 30× faster. The row does not say whether the 10 µs covers both axes.
   - **Proposed rewrite:** "…<10 µs random access (the datasheet does not say whether this covers the 14° axis or which laser it assumes) [U], <5 W". In the "What it shows" cell: "The same OPA engine sold for free-space optical links; if its 14° axis is wavelength-steered, <10 µs access needs a laser much faster than RAY-H1's <300 µs retune".

5. **Line** 5972 (§C10.2b, SR-1S row; also 5971) — **A/B** — **low–medium**
   - **Quote:** "The 70° wavelength-steered axis would need ≈1.17°/nm over RAY-H1's 60 nm"
   - **Problem:** The table never says which laser either module uses. The FS-4S is listed as "C+L band" (≈95 nm). Its 14° vertical field fits that band at the papers' 0.14°/nm, but would need 0.23°/nm with RAY-H1's 60 nm. The SR-1S check assumes 60 nm only.
   - **Proposed rewrite:** Add a derivation bullet: "FS-4S: 14° over the ≈95 nm C+L band is $14/95=0.147^\circ$/nm, consistent with the 8,192-element array's 0.14°/nm; over RAY-H1's 60 nm it would need $0.23^\circ$/nm, i.e. $(n_g-\sin\theta)/\cos\theta\approx6.3$, 1.5× a Si strip. SR-1S: 70° needs $1.17^\circ$/nm over 60 nm (factor ≈32) or $0.74^\circ$/nm over 95 nm (factor ≈20, 4.7× a Si strip); either is far beyond the papers." Also state which laser each datasheet names.

6. **Line** 5927 (§C10.2b device table) — **B** — **low–medium**
   - **Quote:** "| Analog Photonics, 9,216 (VLSI 2023) [I/S] | 9,216 | About 50° × 11° | 0.05° |"
   - **Problem:** A 50° alias-free field allows a pitch of at most $1.55/(2\sin25^\circ)=1.83$ µm. 9,216 elements at that pitch make a ≈17 mm aperture with a FWHM of $0.886\lambda/D\approx0.005^\circ$, ten times finer than the 0.05° listed. The row gives no pitch and no axis for the 0.05°. The 512-element row handles the same ambiguity with a note and [U].
   - **Proposed rewrite:** "| Analog Photonics, 9,216 (VLSI 2023) [I/S] | 9,216; pitch not reported | About 50° × 11° | 0.05° (axis not stated; a 9,216-element phase axis at the ≤1.8 µm pitch a 50° field allows would give ≈0.005°) [U] |".

7. **Line** 2646 (§C3a profile) — **A/B** — **low–medium**
   - **Quote:** "Its public milestones stop in 2021 [P]. The FS-4S datasheet (2025) is analysed in §C10.2b."
   - **Problem:** §C10.2b reports a 2023 company-authored IEEE Spectrum article promising automotive samples in 2025, plus 2025 datasheets and a 2025 CEO talk. "Public milestones stop in 2021" reads as contradicting this. The intended meaning is the company's achieved-milestone timeline.
   - **Proposed rewrite:** "Its published milestone timeline stops in 2021 [P]; a 2023 company-authored IEEE Spectrum article promised automotive samples in 2025, and none were found (§C10.2b). The FS-4S datasheet (2025) is analysed in §C10.2b."

8. **Line** 9672 (Appendix 2, under the heading "Analog Photonics datasheets and the Quanergy record") — **E** — **low–medium**
   - **Quote:** "Analog Photonics FS-4S / SR-1S / RAY-H1 / FSOC-B1 datasheets (2025):"
   - **Problem:** Four datasheets are named but only three URLs follow; there is no FSOC-B1 link. Its figures (≤7.5 dB loss, <10 µs access) cannot be traced. The §C10.2b tag "Rev A, June–July 2025" is also unverified for FSOC-B1.
   - **Proposed rewrite:** Add the FSOC-B1 URL with its revision and date. Otherwise drop "FSOC-B1" from this entry and tag the §C10.2b row [U].

9. **Line** 5961 (§C10.2b, "Who they are") — **B/E** — **low**
   - **Quote:** "Third-party databases give 2012 as the founding year; the company's own timeline begins with a 2016 award under DARPA's MOABB"
   - **Problem:**
     - §C3a shows federal money earlier than this: subawards from Nov 2013 and SBIR awards from 2015.
     - The founder is tagged [I] here but [P/S] in §C3a (line 2631).
     - The milestones in this paragraph carry no tag.
     - The paragraph omits the facts §C3a holds: funding, 26 employees, and the departure of Christopher Poulton, lead author of the 512- and 8,192-element papers this subsection relies on.
   - **Proposed rewrite:** "**Who they are.** Analog Photonics (Boston) was founded about 2012 by Michael Watts of MIT, who remains CEO [P/S]. Federal records show subawards from Nov 2013 and SBIR awards from 2015; the company's own timeline starts with its 2016 DARPA MOABB award (§C3a). Company milestones [P]: a Tier 1 joint development agreement (2018), on-car tests (2019), a second Tier 1 agreement (2020) and a narrow-linewidth FMCW laser (2021). Funding, size and the departure of the lead author of its OPA papers are covered in §C3a."

10. **Line** 2635 (§C3a; also §D8, lines 7574–7575) — **B/E** — **low**
    - **Quote:** "**\$3.97 M**, 2023–26 [I];"
    - **Problem:**
      - §D8 gives this ONR contract as "\$4.0 M over FY2023–25, is the only active integrated-photonics lidar contract found [P]". The years differ, and so does the tag ([I] vs [P]) for the same USAspending record.
      - Similarly, §C3a's MOABB award ("2016–2023") outlasts §D8's MOABB budget ("\$102 M over FY2016–21 and nothing from FY2022 [P]").
      - The reader is not told that one set of dates is the period of performance and the other is the fiscal years of obligation.
    - **Proposed rewrite:** In §C3a, "**\$3.97 M** obligated in FY2023–25, period of performance 2023–26 [I];" and "…**\$26.6 M**, period of performance 2016–2023 (MOABB's budget lines end in FY2021, §D8)". In §D8, "\$4.0 M obligated over FY2023–25 (performance to 2026, §C3a)". Use one tag for USAspending records throughout.

11. **Line** 2623 (§C3a table, status cell) — **D** — **low**
    - **Quote:** "No automotive programme; two unnamed Tier 1 JDAs (2018, 2020) [P]; defence FSOC and lasers (below; §C10.2b)"
    - **Problem:** "No automotive programme" reads as contradicting the Tier 1 joint development agreements in the same cell and the "on-car tests (2019)" in §C10.2b. What is missing is a production award.
    - **Proposed rewrite:** "No automotive production award found; two unnamed Tier 1 JDAs (2018, 2020) and on-car tests (2019) claimed [P]; defence FSOC and lasers (below; §C10.2b)".

12. **Line** 5942 (§C10.2b finding 1; also 5928) — **B** — **low**
    - **Quote:** "Multi-reticle stitching has been demonstrated (49,152 elements)."
    - **Problem:** The table row says ">49,152 over four reticles", tags the source as an abstract and reports no ranging. Finding 1 gives exactly 49,152 and calls it "demonstrated". 24 OPAs of 2,048 elements each would be exactly 49,152.
    - **Proposed rewrite:** "Multi-reticle stitching of 49,152 elements (24 coherently combined OPAs over four reticles) has been reported in a conference abstract [I], without ranging." Use the same count in the table.

#### 3. Earlier findings: status in the current text

**Resolved**
- **#1, coherent-power headline** (now line 6009). Minor residual: line 6016 still says $N_{\rm req}=10$–30 "are roughly those for a non-fading return".
- **#2, "camera-like" definition** (Q4, now line 5759).
- **#4, ToF inputs** (now lines 6020 and 6039). New residual: the caveat at line 6067, "Sunlight raises the ToF $N_{\rm req}$ (§C6(d)).", now contradicts line 6020. Suggested replacement: "Sunlight is already included in the ToF $N_{\rm req}$ (bright sun, §C0 subsection 10.3); a fully sunlit scene of reflectance 0.9 raises the ideal requirement only to ≈20 (§C6(d))."
- **#5, diversity assumption** (now line 5895). Line 5891 still groups polarization, wavelength and spatial diversity together, but line 5895 now explains the difference.
- **#6, ToF usable aperture** (now line 5777).
- **#32, in part:** "26.5" has been corrected to 26.4. "about 25 cells" (line 5859) and "about 9 dB higher" (line 5945) remain.

**Still open (quote text unchanged)**
- #3 ($\eta$ convention, line 6015), #7–#31 and #33–#40.
- This includes #10 (§C10.2b "amounts are not disclosed", line 5963), which new finding 2 extends.

#### 4. Consistency flags confirmed in this check

- §C7 (line 4476), "1.5 µm pitch, about 60°", against the 512-element device in §C10.2b (1.65 µm, 56°). Still unsourced. If 1.5 µm is inferred from the FS-4S's 60° field, mark it so, e.g. "a 60° phase-steered field implies a pitch of about 1.5 µm [E]".
- Line 5972, "14–17° in AP's papers", against the table's 15° and 17°. "AP" is still undefined.
- Optional: the headline at line 6009 could add the multi-mode case from caveat 4, "≈45 W with four receive modes".

### §C10.3a–§C10.7 (mode counting, FPAs, LC metasurface, camera-like resolution, verdict)

**Coverage:** the whole block, lines 6112–6838, was read line by line. The cross-reference checks were stopped before they were finished: the §C8.2 ADC pointer, §E11.2, §C6's staring-array text and where §C7a gets its 520-pixel and PDE inputs were not fully checked, and outside product facts were not checked.

#### 1. Overall assessment

The block is unusually checkable. I recomputed almost every substitution: Eqs. (142)–(148), the waist, speckle and footprint tables, Results 1–4, the mode–time budgets, scan lag, the LCM efficiency, dispersion and contact counts, stopping distances, debris sample counts and line counts. None has an arithmetic slip. Each subsection opens with its question and its answer.

The three systemic problems are:
- **The efficiency and area bookkeeping changes basis without saying so.** $\eta$ includes polarization loss in §C10.3 but excludes it in Eq. (144). Fractions, "far-field" areas and the chip-row areas switch between including and excluding polarization, truncation and losses. "Photons" and "photoelectrons" are used interchangeably, and $K$ is also used to mean $K/P$.
- **The same quantity is computed with several models that give different numbers, and they are never reconciled.** Examples: the confocal "optimum" aperture is taken as $2w_0$ in one place and $w_0/0.45$ in another; there are three overlap rules; the mode-count method gives ≈1% coverage where the footprint method gives 2.1%; and $\lambda^2/\Omega_{\rm cell}$ appears next to $\tfrac{t^2}{2}\lambda^2/\Omega_{\rm cell}$. One physical explanation is wrong: the target at 200 m is not in the near field.
- **Structure.** §C10.3a and §C10.3b are interleaved, with forward references to Eqs. (145)–(147). Core results and the "not a detection probability" disclaimer are repeated 3–9 times. Terms drift: "fill", "beam width" and "area-matched" each mean more than one thing.

#### 2. Findings (most severe first)

**1. Line 6238** — A — **high**
- **Quote:** "$\eta$ is the end-to-end efficiency, playing the role of $\eta_{\rm common}$ in item 1 (it excludes truncation and polarization);"
- **Problem:** The symbol and name are the same as in §C10.3, but the meaning differs. §C10.3 says "The values of $\eta$ below are assumed to include whatever polarization loss applies" (line 5997). Both places use $\eta=0.1$ and both arrive at 184 W (line 6258 and §C10.3), so the reader cannot tell whether 184 W includes the polarization loss. Item 1 also calls this same quantity $\eta_{\rm common}$, so one quantity has two symbols within 100 lines.
- **Proposed rewrite:** Use $\eta_{\rm common}$ in Eq. (144) and in its substitution, and write: "$\eta_{\rm common}$ is the shared efficiency of item 1 (optics and photoconversion). As there, it excludes truncation and polarization, which the Gaussian model puts into $A_{\rm mode}$. It therefore differs from the $\eta$ of Eq. (139) in §C10.3, which includes polarization. With $\eta_{\rm common}=0.1$, the 184 W below equals §C10.3's 184 W only numerically. Including §C10.3b's factor $t^2/2=0.42$ raises it to ≈440 W ($184/0.419$)."

**2. Line 6402** — A/B — **high**
- **Quote:** "The aperture is larger than the confocal optimum there, so the target sits in the beam's near field."
- **Problem:** This is true at 100 m but false at 200 m:
  - For the 20 mm beam, $z_R=164$ m, which is less than 200 m.
  - §C0 Eq. (35) gives $D_{\rm opt}=22$ mm at 200 m.
  - Result 2's $A_{\rm mode}=63.7$ mm² is 98% of the collimated ceiling $t^2\lambda R/4=64.9$ mm².

  $N_{\rm sp}>1$ even at the optimum for a different reason: the hard aperture spans about two coherence areas of the speckle, $A_{\rm rx}\pi w^2/(\lambda R)^2=314/152\approx2.1$.
- **Proposed rewrite:** "At 100 m the 20 mm aperture is larger than the confocal optimum (≈16 mm), so the target sits in the beam's near field. At 200 m it is close to the optimum (≈22 mm), yet the hard aperture still spans about two coherence areas of the speckle, $A_{\rm rx}\pi w^2/(\lambda R)^2=314\ {\rm mm^2}/152\ {\rm mm^2}\approx2.1$, because the Gaussian launched with $w_0=0.45D$ does not fill it. The simple expectation $N_{\rm sp}\approx1$ is therefore too optimistic even at the optimum."

**3. Line 6161** — B — **high**
- **Quote:** "| Coherent receiver with a cell-filling spot, 20 mm aperture | ≈22 cm | ≈1.8 mm | ≈106 (exact) | ≈1/100 |"
- **Problem:** The "Fraction the detector uses" column mixes two bases:
  - The monostatic row's ≈1/4 includes polarization, truncation and near-field loss.
  - This row's ≈1/100 is the spatial fraction $1/N_{\rm sp}$ only. On the monostatic row's basis it is 1/238, which is what §C10.3b reports for the same configuration ($314/1.32$).

  The $N_{\rm sp}$ column also mixes the simple count (ToF ≈460) with Goodman counts (106, labelled "exact"). Result 1 leaves the simple column blank ("—") for coherent rows, although line 6166 computes 100.
- **Proposed rewrite:**
  - This row's cell: "≈1/100 spatially; ≈1/240 of hard-aperture power with polarization and truncation (§C10.3b, Result 2)".
  - Monostatic cell: "≈1/4 of hard-aperture power (polarization, mode shape, truncation and near field included)".
  - Replace "(exact)" with "(numerical model)" and put all $N_{\rm sp}$ values on one basis.
  - Fill Result 1's simple column for the coherent rows: 100, 398, 25.

**4. Line 6292** — A/B — **high**
- **Quote:** "Matching the 1/e² beam area to all cells with a 20 mm coherent aperture would need about 2,400–12,000 parallel channels under these dwell assumptions"
- **Problem:**
  - **Term clash.** This sentence, and the table header "area-matched field sampling", read like §C10.3b's "area-matched cell" (the spot widened to fill one cell). Here the phrase actually means tiling the field with the native 20 mm spots ($f_{\rm fp}=1$).
  - **Factor-of-2 conflict.** For the same design (20 mm aperture, 128 channels × 10 µs), the table gives ≈1% coverage while Result 2 gives 2.1%. The footprint method gives ≈1,200–5,800 channels, not 2,400–12,000. The gap comes from the ≈2 hard-aperture modes per nominal footprint at 200 m, and the text never says so.
- **Proposed rewrite:** "Covering the whole field with the native 1/e² spots of a 20 mm aperture ($f_{\rm fp}=1$, not the widened 'area-matched' spot of §C10.3b) would need about 2,400–12,000 channels by this mode count. The footprint count of §C10.3b gives half that, ≈1,200–5,800 ($0.914\ {\rm sr}\times(200\ {\rm m})^2/6.32\ {\rm cm^2}=5.8\times10^{7}$ samples per frame, divided by $5\times10^{4}$ or $10^{4}$ dwells). The difference arises because one nominal footprint spans ≈2 hard-aperture modes at 200 m, which is also why the table shows ≈1% where Result 2 shows 2.1%." Rename the column to "Mode–time slots for full nominal coverage".

**5. Line 6218** — A — medium
- **Quote:** "each sample is treated as a hard square spot of side $s=R\times0.0036^\circ$ (the 250 m confocal 1/e² half-angle from the table above"
- **Problem:** For the same two objects the block gives three different coherent overlap values:
  - 0.93 / 0.28 here (the 250 m confocal radius used as the square's side, also at 150 m and 200 m);
  - 0.86 / 0.21 in Result 4 (centre-in-object rule);
  - 1.00 / 0.37 in Result 4 (1/e² circle touches the object).

  The mesh figure uses yet another rule ("equal-area square proxy"). No reason is given for using the radius as the side. §C10.6(g) then reuses 0.28 / 0.81.
- **Proposed rewrite:** Replace both coherent columns with Result 4's two named rules for the 20 mm beam. For 10 × 10 cm at 250 m that gives 0.21 and 0.37, and over five offsets $1-0.79^5=0.69$ and $1-0.63^5=0.90$. Alternatively, state once: "This table uses an intermediate rule between §C10.3b's centre-in-object and 1/e²-touch rules, and for simplicity uses the 250 m confocal beam at all three ranges." Make the figure caption name the same rule.

**6. Line 6338** — B — medium
- **Quote:** "The far-field-only figure takes the hard area with the single-polarization factor and the same QE and losses, $314\times0.5\times0.8\times0.63=79$ mm²."
- **Problem:** 79 mm² is not the model's far-field limit. Item 2 shows that in the far field the hard area exceeds $A_{\rm mode}$ by 2.9 (polarization × mode shape and truncation, 2 × 1.47), which gives ≈54 mm². The wrong label carries into line 6332 and line 6496 ("the ≈80 mm² of the far-field formula alone").
- **Proposed rewrite:** "A hard-area estimate with only the single-polarization factor gives $314\times0.5\times0.8\times0.63=79$ mm². The model's far-field limit also includes item 2's mode-shape and truncation factor 1.47, giving $79/1.47\approx54$ mm²." Change lines 6332 and 6496 to match.

**7. Line 6339** — B — medium
- **Quote:** "OPA or FPA chip: hard area times the single-polarization factor, before on-chip loss, $\pi(8\ {\rm mm})^2/4\times0.5=25$ mm² for 8 mm and 0.4 mm² for 1 mm."
- **Problem:** The column is headed "Efficiency-weighted aperture", but this row leaves out QE and the on-chip loss, so it cannot be compared with the ToF and FMCW rows. Applying QE 0.8 and 3–10 dB each way gives ≈0.2–5 mm² for 8 mm and ≈0.003–0.08 mm² for 1 mm. The "3–10 dB" is also below §C10.2b's measured 10–14 dB one-way for OPAs.
- **Proposed rewrite:** Table cell: "≈0.2–5 mm² for 8 mm and below 0.1 mm² for 1 mm, after QE 0.8 and 3–10 dB on-chip loss each way (measured OPAs: 10–14 dB, §C10.2b)". Note: "…times QE 0.8 and $10^{-0.6}$ to $10^{-2}$ for the round trip: 0.2–5 mm² (0.003–0.08 mm² for 1 mm)."

**8. Line 6509** — B — medium
- **Quote:** "$A_{\rm mode}=\lambda^2/\Omega_{\rm cell}$, with $\Omega_{\rm cell}$ the solid angle of one address cell, holds only for a cell-filling footprint."
- **Problem:** This contradicts the identity stated just before it. At $f_{\rm fp}=1$, Eq. (147) gives $\tfrac{t^2}{2}\lambda^2/\Omega_{\rm cell}$, which is 2.4× smaller (§C10.3b: 1.3 mm² against 3.2 mm²).
- **Proposed rewrite:** "For a cell-filling footprint ($f_{\rm fp}=1$), Eq. (147) gives $A_{\rm mode}=\tfrac{t^2}{2}\lambda^2/\Omega_{\rm cell}$, where $\Omega_{\rm cell}=\theta^2$ is the solid angle of one address cell. The ideal $\lambda^2/\Omega_{\rm cell}$ omits truncation and polarization."

**9. Line 6301** (also 6517) — A/B — medium
- **Quote:** "at the ≈2% fill it actually uses, it gets ≈6 mm."
- **Problem:**
  - The ≈2% has no source or derivation. §C10.4 (line 6517) cites §C10.3a for it, which is circular. The report's other "≈2%" belongs to the 20 mm collimated beam at 200 m, a different optical system.
  - "≈0.8 mm aperture" and "≈6 mm" are equivalent diameters of $A_{\rm mode}$, yet §C10.4 calls ≈6 mm a "lens-filled aperture". For a Gaussian beam the far-field equivalent diameter is about 0.58 of the physical aperture.
- **Proposed rewrite:** "…could fill its field only with a mode-equivalent collecting diameter of ≈0.8 mm. At a nominal footprint fraction of ≈2% [source or derivation needed], the identity allows ≈6 mm." In §C10.4: "(mode-equivalent collecting diameter ≈6 mm at an assumed ≈2% nominal footprint fraction; §C10.3a)".

**10. Line 6332** — B — medium
- **Quote:** "Confocal optimum (≈14 mm at 100 m, ≈22 mm at 250 m)"
- **Problem:** These are beam diameters $2w_0$ (item 3's table header is "Optimal $w_0$ (diameter)"), not aperture diameters. §C0 Eq. (35) defines $D_{\rm opt}=\sqrt{\lambda R/\pi}/0.45$, which gives 15.6 mm at 100 m, 22 mm at 200 m and 24.7 mm at 250 m. So "22 mm" means 200 m in §C0 and 250 m here. This mix-up also underlies finding 2.
- **Proposed rewrite:** "Confocal optimum ($D_{\rm opt}=\sqrt{\lambda R/\pi}/0.45$, §C0 Eq. (35): ≈16 mm at 100 m, ≈25 mm at 250 m)". In item 3's table, change the header to "Optimal $w_0$ (beam diameter $2w_0$)" and add the apertures $w_0/0.45$: 11, 16, 25 and 35 mm.

**11. Line 6166** (also 6426) — B — medium
- **Quote:** "matching the Goodman count of §C10.3b (3.0 at 250 m, 6.2 at 100 m)"
- **Problem:** Result 1, and the tables file behind it, give 6.2 at 100 m and 3.3 at 200 m. No 250 m value appears anywhere. Separately, line 6426 says "about 2–15%", but Result 2 runs from 1.6% to 15%.
- **Proposed rewrite:** "consistent with the Goodman counts of §C10.3b, Result 1 (6.2 at 100 m, 3.3 at 200 m)", or add a 250 m row to Result 1. At line 6426, write "about 1.6–15%".

**12. Line 6248** — A — medium
- **Quote:** "$K$ is about **0.16 photons per watt**"
- **Problem:** Eq. (144) defines $K$ as a photoelectron count times a fraction, so it is proportional to $P$. Here, and in the table note ("$K$ here taken as the per-watt value 0.163 W⁻¹"), the same symbol is used for $K/P$. "Photons" also replaces "photoelectrons".
- **Proposed rewrite:** "the per-watt budget constant $k\equiv K/P$ is about **0.16 photoelectrons per watt**". In the table note: "the bound is $f_{\rm fp}=kP/n_{\rm mode}$, capped at one".

**13. Line 6801** — B — medium
- **Quote:** "Only partly demonstrated (38–80 nm of tuning)"
- **Problem:** §C10.2b finding 5 gives 38–120 nm (the 8,192-element array used 1515–1635 nm). The source of "80 nm" is not given.
- **Proposed rewrite:** "Only partly demonstrated (38–120 nm in OPA demonstrations, §C10.2b; 60 nm in a narrow-linewidth chirped module, RAY-H1)".

**14. Line 6504** — A — medium
- **Quote:** "Selecting a pixel selects a direction ($\theta=x/f$, where $x$ is the pixel's distance from the lens axis"
- **Problem:** Here $\theta$ is a look direction. Two bullets later it is the address pitch (Eq. (147); and $f=p/\theta$ in the first cost).
  - Other symbols are also reused. $p$ means the pitch at the target, the FPA pixel pitch, the rail pitch and the LCoS pixel pitch.
  - $h$ means both Planck's constant (line 6133) and the mount height (§C10.6).
- **Proposed rewrite:** "Selecting a pixel selects a look direction $\phi=x/f$, where $x$ is the pixel's distance from the lens axis and $f$ the focal length. Neighbouring pixels at pitch $p$ are therefore $\theta=p/f$ apart (the address pitch)."

**15. Line 6360** — A — medium
- **Quote:** "The roughly 0.5–4% figures above are *inferred nominal footprint fractions* for particular design examples"
- **Problem:** No 0.5–4% range appears in §C10.3a; items 3–5 give 0.8–8%, 0.5–11% and ≈1–5%. The 0.5–4% range is the box/FWHM design table in §C10.3, which corresponds to 1.6–8% at 1/e².
- **Proposed rewrite:** "The footprint fractions in this subsection (0.5–11% for item 4's 1–20 W bounds, ≈1–5% for item 5's budgets) and the 0.5–4% box or FWHM values of the designs in §C10.3 (1.6–8% at 1/e²) are inferred nominal footprint fractions for particular design examples, not measured probabilities…"

**16. Line 6140** — A/D — medium
- **Quote:** "has about **16 photons incident** in this efficiency-weighted bookkeeping, before projection into its selected mode"
- **Problem:** $\eta_{\rm common}$ already includes photoconversion, so these 16 are photoelectron equivalents, not incident photons. Three lines later the same bookkeeping becomes "3.3 usable signal photoelectrons". The word changes again at lines 6248, 6250, 6264, 6293 and 6564.
- **Proposed rewrite:** "collects about **16 photoelectron equivalents** (aperture photons already multiplied by $\eta_{\rm common}\rho$), before projection into its selected mode". Add once: "Throughout §§C10.3a–b, photon counts per sample are detected photons, i.e. photoelectrons."

**17. Line 6365** — C — medium
- **Quote:** "This subsection replaces the order-of-magnitude estimates of §C10.3a with an explicit numerical model [E]."
- **Problem:** §C10.3a already quotes §C10.3b's results (lines 6143, 6159, 6164, 6167, 6171, 6261, 6293). It also cites equations before they appear: Eq. (145) at line 6260 (defined at 6268) and Eqs. (146)–(147) at lines 6293 and 6301 (defined at 6382 and 6433). "Replaces" also reads like edit history.
- **Proposed rewrite:** "This subsection gives the explicit numerical model [E] whose results §C10.3a quotes, and checks the order-of-magnitude scalings there." In item 5, cite "Eq. (33) of §C0 (restated as Eq. (146))". At line 6301, write "Eq. (147), derived in §C10.3b".

**18. Line 6221** — C — medium
- **Quote:** "These are **geometric overlap fractions, not detection probabilities**."
- **Problem:** Some form of this disclaimer appears about nine times (lines 6199, 6221, 6223, 6294, 6360, 6426, 6475–6477, 6492). Key results are also restated 3–7 times each: "1/4–1/11" (4×), "15–40 / 80 / 85 mm²" (4×) and "1.3 mm²" (7×).
- **Proposed rewrite:** Define once, in item 3: "**Nominal footprint and overlap fractions** are geometric bookkeeping. They ignore Gaussian tails, speckle, reflectance and threshold, and are not detection probabilities." Later passages should just say "nominal (item 3)". Cut "What the exact computation shows" down to its new numbers: 1.6 and 3.2 mm².

**19. Line 6531** — D — medium
- **Quote:** "**Fill factor.** Grating antennas are microns wide but pitches are tens of microns, so the far-field beams are much narrower than their spacing."
- **Problem:** "Fill" has four meanings in the block:
  - the footprint fraction (here, and "≈2% fill" at line 6301);
  - a detector's active area (6200);
  - an aperture's emitting area (6592);
  - an object's share of a pixel (Result 4).

  §C10.5 (line 6603) also uses "footprint fraction" for a one-axis quantity.
- **Proposed rewrite:** "**Nominal footprint fraction (beam fill).** Grating antennas are microns wide but pitches are tens of microns, so each far-field beam is much narrower than the address spacing; the beam-to-pitch ratio is roughly the emitter-to-pixel size ratio." Keep "fill factor" for active area only, and write "one-axis footprint fraction" in §C10.5.

**20. Line 6552** — A — medium
- **Quote:** "A company blog says the production chip has just over 5,000 antennas, and that the demonstration used a 4 × 80 sub-array at 30 Hz."
- **Problem:** The preceding sentence gives Helium "12k to >100k pixels". The reader cannot tell which product's production chip has 5,000 antennas.
- **Proposed rewrite:** "A company blog says that the first production [Helium/Carbon] chip has just over 5,000 antennas, fewer than the 12k–100k pixels quoted for Helium configurations, and that the demonstration used…"

**21. Line 6662** — D — medium
- **Quote:** "enough geometric overlap to register them, though below the ≈60–100 points per object, and the ≈0.075° pitch for a car, that learned detectors"
- **Problem:** This is a sentence of about 55 words with a split comparison, and it is hard to parse.
- **Proposed rewrite:** "At 200 m on a 0.1° grid, a car subtends ≈5×4 sample centres and a pedestrian ≈1.4×5: enough geometric overlap to register them. That is still below what learned (neural-network) detectors needed in the studies of (i): about 60–100 points per object, and a pitch of ≈0.075° for a car."

**22. Line 6260** — B — low
- **Quote:** "The 30-photon column is the §C7a four-look receiver: 120 photoelectrons summed over four modes (88.5 ideally, 22 per look)"
- **Problem:** The two columns are on different bases. 30 per look includes the 1.36× design margin; 259 is the ideal value with no margin. Eq. (145) is also used here before it is defined.
- **Proposed rewrite:** "The 30-photon column is the §C7a four-look design value: 30 per look, a 1.36× margin over the ideal 22 per look (88.5 in total). The 259-photon column is the ideal single-look value without margin. By Eq. (145) below, four modes at 30 have the coverage bound of one mode at 30."

**23. Line 6270** — A — low
- **Quote:** "where $n_{\rm selected\ modes}$ is the photoelectron count summed over all the selected modes and $K$ is the single-mode budget constant of Eq. (144)."
- **Problem:** $n_{\rm mode}$, $N_{\rm mode}$ and $n_{\rm selected\ modes}$ all appear within six lines and are easily confused.
- **Proposed rewrite:** "$$n_\Sigma\,f_{\rm fp}\sim N_{\rm mode}\,K \tag{145}$$ where $n_\Sigma=N_{\rm mode}\,n_{\rm mode}$ is the photoelectron count summed over the $N_{\rm mode}$ selected modes…"

**24. Line 6137** — A — low
- **Quote:** "and that the same aperture serves both comparisons."
- **Problem:** The example that follows uses two different apertures, 20 mm and 25 mm, so the meaning is unclear.
- **Proposed rewrite:** "…and that $A_{\rm rx}$ is the receive aperture of whichever receiver is evaluated (20 mm coherent and 25 mm ToF below)."

**25. Line 6605** — A — low
- **Quote:** "That is about 23% above the 10k steps/s ($1/100\ \mu{\rm s}$) a 100 µs device can deliver even at zero dwell"
- **Problem:** Twenty lines later, the LM10 + Adaps design claims "30 fps full frame" over 180° × 140°. At 0.39° steps that needs about 10.8–13.8k steps/s, and the text does not reconcile this with the ceiling.
- **Proposed rewrite:** Add after the Adaps bullet: "At 0.39° steps its 30 fps would need $140^\circ/0.39^\circ\times30\approx10.8$k steps/s, at or above the 100 µs ceiling, so it probably lights several rows per step [E]."

**26. Line 6770** — A — low
- **Quote:** "A fixed-aperture sparse design instead gains footprint fraction, not photons"
- **Problem:** Photons per sample fall in the same proportion as the footprint fraction rises. "Not photons" can be misread as "photons unchanged".
- **Proposed rewrite:** "A fixed-aperture sparse design instead gains footprint fraction and loses photons per sample in the same proportion, because $n_{\rm mode}f_{\rm fp}=K$ is fixed (Eq. (144), §C10.3a)."

**27. Line 6311** (also 6312) — D/E — low
- **Quote:** "(§C7, scanner-induced Doppler, where the scan rate is written $\Omega$)"
- **Problem:** The sentence is about 60 words long and states the $\Omega$ note twice. It does not warn that §C7 uses $\omega$ for the *mechanical* rate. The next bullet cites the walk-off "of §C10.3" instead of an equation number.
- **Proposed rewrite:** "…by $\approx\omega D/\lambda$ per pass (Eq. (86), §C7), where $\omega$ is the optical scan rate in rad/s and $D$ the beam diameter on the scanner. §C0, §C4d and §C7 write this rate $\Omega$, and §C7 uses $\omega$ for the mechanical rate." In the next bullet: "by the walk-off of Eq. (141), $\Delta\theta\approx2R\omega/c$".

**28. Line 6310** — A — low
- **Quote:** "roughly three narrow-beam widths ($0.012^\circ/0.0036^\circ=3.3$)"
- **Problem:** 0.0036° is the 1/e² half-angle, not a width. The same applies in the lag table ("a 0.0036° beam", "half a beam width").
- **Proposed rewrite:** "roughly three 1/e² beam radii, or 1.7 full 1/e² widths ($0.012^\circ/0.0072^\circ$)". Change the lag table header to "Compared with the 0.0036° 1/e² half-angle".

**29. Line 6774** — C — low
- **Quote:** "| Pitch | Coherent power ÷ ToF power |"
- **Problem:** The table omits 0.05°, the reference grid used throughout §§C10.3a–b. Its lead-in "far more power" also overstates the 1.4× lower end.
- **Proposed rewrite:** Add the row "| 0.05° | 23–200× |". Change the lead-in to "…needs 1.4–800× the power of the ToF example".

**30. Line 6809** — D — low
- **Quote:** "a laser that is tunable over ≥100–160 nm (or ≥60 nm paired with ≥0.3°/nm dispersion-engineered emitters, i.e. grating emitters designed to steer more degrees"
- **Problem:** This is an 80-word bullet with nested parentheses.
- **Proposed rewrite:** Split it into two bullets:
  - "a laser tunable over ≥100–160 nm, with ≤100 kHz linewidth and a linear chirp, at automotive cost and a few watts (RAY-H1 offers 60 nm and <40 kHz, but in a 19 W module);"
  - "or ≥60 nm with dispersion-engineered grating emitters steering ≥0.3°/nm, since $60\times0.3=18^\circ$ exceeds the ≈16° that 100 nm gives on plain Si ($100\times0.155$);"

**31. Line 6768** — D — low
- **Quote:** "at least three vertical returns on a 50×15 cm (W×H) object at 150–200 m (three returns at 200 m need a vertical pitch of ≤0.014°"
- **Problem:** Nested parentheses put a derivation inside the specification.
- **Proposed rewrite:** "…on a 50×15 cm (W×H) object at 150–200 m, 10% reflectivity, 100 klux and at least 10 Hz, with stated detection probability and false-alarm rate. Three returns at 200 m need ≤0.014° [E: $0.15/200=7.5\times10^{-4}$ rad $=0.043^\circ$, divided by 3]."

**32. Line 6173** — C — low
- **Quote:** "the Gaussian mode shape and truncation cost about 1.5×. Here $D$ is the aperture diameter (20 mm) and $w_0=0.45D$ the Gaussian beam's waist"
- **Problem:** This list item is really a paragraph. It redefines $D$, $w_0$ and $t$, and it points to §C10.3b for the 0.45 ratio, whose justification is in §C0 subsection 10.2.
- **Proposed rewrite:** Keep the bullet as "the mode shape and truncation cost 1.47× (derived below);". Move the derivation to an *How the numbers are derived* [E] note: "With $w_0=0.45D$ (§C0 subsection 10.2) and $t=0.915$, the far-field limit gives hard area ÷ $A_{\rm mode}=2(D/2)^2/(t^2w_0^2)=2\times1.47=2.9$."

**33. Lines 6114–6116** — A/D — low
- **Quote:** "The target is diffuse and extended (the Gaussian model of §C10.3b also covers the near field)."
- **Problem:** The parenthesis does not follow from the sentence it sits in. "Nominal footprint coverage" (line 6114) is used before it is defined.
- **Proposed rewrite:** "The target is diffuse and extended. The estimates below are mostly far-field; §C10.3b's Gaussian model also covers the near field." At line 6114: "…against nominal footprint coverage (the share of the field covered by the beam spots, item 4), …"

**34. Line 6342** — E — low
- **Quote:** "Piggott et al. put coherent detection about 6 dB behind ToF at equal aperture, from polarization and mode weighting."
- **Problem:** Several tags are missing or do not match the legend:
  - This sentence has no tag (§C7b tags the same claim [P]).
  - Also untagged: Waymo's 18 dB (6564); the point rates (6456, where Aeva Aeries II is not among the "cited" products); Mobileye and Quanergy (6825, 6829); the FSD and nuScenes figures (6726–6727, no citation); Goodman's formula (6375, no citation).
  - "(secondary)" appears in place of a tag (6739).
  - The legend files academic papers under [I] and secondary sources under [S], but Zhang et al. and Rogers et al. are tagged [P] and LM10 figures "[T, secondary sources]".
- **Proposed rewrite:** Append "[P]" here and add tags or sources at the other places. Use [I] for independent academic papers, keep [P] for company-authored ones, and use [S] as the legend defines it.

**35. Line 6122** — D — low
- **Quote:** "this $M^2$ is unrelated to an APD gain"
- **Problem:** Several acronyms are not expanded in their section: APD; CMOS and LCD (6580); QVGA (6625); SAE (6753, 6786); ONCE (6723); FSD (6726); NYCU (6549); ITHCA (6632); fps (6517).
- **Proposed rewrite:** "this $M^2$ is unrelated to the multiplication gain $M$ of an avalanche photodiode (APD)". Expand the others at first use.

**36. Line 6384** (also 6151, 6569) — A/E — low
- **Quote:** "the antenna theorem, derived in §C0 subsection 10.2"
- **Problem:** §C0 subsection 10.2 *states* the theorem (citing Siegman 1966) and derives $A_{\rm mode}$ from it. It does not derive the theorem itself or Eq. (143). Separately, "(§C6: the mechanical axis as a silicon-area multiplier)" points to the wrong section: the phrase and the argument are in §C8.3 (line 5563).
- **Proposed rewrite:** "the antenna theorem, stated with its source in §C0 subsection 10.2 (Siegman 1966)". At line 6569: "(§C6; §C8.3: …)".

**37. Line 6278** — C — low
- **Quote:** "Illustrative budgets (optical modes × scan slots):"
- **Problem:** Several tables are introduced only by a fragment or by definitions, not by a sentence saying what they show: here, and at 6155, 6184, 6248, 6511, 6731 and 6786.
- **Proposed rewrite:** "The table compares, for each system, the mode–time slots needed for full nominal coverage of 120° × 25° at 10 Hz with the slots its channels and dwells supply per frame." Add similar one-sentence leads to the others.

**38. Line 6703** — D — low
- **Quote:** "First seen at 200 m, it gives 19–25 frames."
- **Problem:** The frame rate is not stated.
- **Proposed rewrite:** "First seen at 200 m, it gives 19–25 frames at 10 Hz (39–50 at 20 Hz)."

**39. Line 6634** (also 6631) — D/C — low
- **Quote:** "Voyant (August 2026) and 国科光芯 (September 2026) are also moving into data-centre optical switching."
- **Problem:** The Chinese name has no transliteration or gloss. The judgement "where the money currently is" is informal and untagged. The "first 2D" LCM chip mentioned at line 6631 bears directly on the one-axis limit, but appears only among business signals.
- **Proposed rewrite:** "…and Guoke Guangxin (国科光芯; [one-line description])… Beam-steering and silicon-photonics IP is being redirected towards AI interconnect, which currently attracts more funding [E]." Add to Limits: "Lumotive showed a first 2D LCM chip in March 2026 [P]; its steering performance is unpublished."

**40. Line 6625** — B — low
- **Quote:** "against the stated ≈$5\times10^5$ [E]"
- **Problem:** The check gives a result 30% higher than the stated rate, and the text says nothing about the gap.
- **Proposed rewrite:** "…against the stated ≈$5\times10^5$, about 30% lower; the difference is unexplained [E]."

#### 3. Consistency flags to check elsewhere

1. **$\eta$ scope.** It includes polarization in §C10.3 (line 5997) and in §C10.2 item 5 (line 5865, $\eta=0.4$). It excludes polarization in §C0 subsection 10.1 (line 1914) and in §C10.3a Eq. (144) (line 6238). Both §C10.3 and §C10.3a give 184 W, and §C10.4 (line 6566) quotes "20–184 W".
2. **Confocal aperture.** §C0 Eq. (35) and line 1979 give $D_{\rm opt}=22$ mm at **200 m**. The block (6186, 6332) uses "≈22 mm" at **250 m**, because it quotes $2w_0$.
3. **"≈2% of a 0.05° cell (§C10.3a)"** at lines 4615, 4755, 4814 and 5423. The 2.1% figure is in §C10.3b Result 2 (and §C10.2 item 7), not in §C10.3a.
4. **Pointcloud ≈2% / ≈6 mm** (6301, 6517, and the §C10 summary at 5753) against §C0 subsection 10.8 (lines 2418, 2424), which gives a measured waist of 1.31 mm at 11.1 m ($z_R\approx4.1$ m). On the 0.061° grid that waist gives a nominal 1/e² footprint fraction of about 4% at 11 m and about 20% at 65 m (my estimate). The quoted field of 23° × 14° also differs from $352\times176\times0.061^\circ=21.5^\circ\times10.7^\circ$.
5. **LCM ranges and names.** The §C10 summary (5755) says "≈10–50 m", but §C10.5 lists Namuga at ≤100 m (6628) and X20 at >120 m. The product is "Namuga Stella-2" at 6628 and "Namuga Stella-180" in §F5 (line 8711).
6. **Tuning range.** §C10.2b (5931) says 38–120 nm; §C10.7 (6801) says 38–80 nm.
7. **LC switching threshold.** The §C10.5 verdict needs ≤21 µs (6637); the §C10.7 signpost says ≤25 µs at −40 °C (6811).
8. **Time horizon.** The §C10 summary (5746) says "this decade"; §C10.7 says "by 2032".
9. **Channel counts.** §C10.2 item 7 (5889) gives 24–120 channels and §C10.4 (6538) "tens to about a hundred", but the §C10.7 signpost (6810) asks for ≥256 without explanation.
10. **Overlap values.** §C10.6(g) (6706) uses 0.28 / 0.81; Result 4 (6468) gives 0.21 / 0.37 for the same object.
11. **Beam angle used for scan lag.** §C10.3 (6085) uses "0.003°" ($\lambda/\pi w_0$); §C10.3a (6316) uses "0.0036°" ($w(R)/R$).
12. **$\omega$.** §C7 (lines 4492–4493) uses $\omega$ for the mechanical rate; §C10 (Eq. (141), lines 6311–6312) uses it for the optical rate.
13. **ToF signal efficiency.** Item 7 (6331, 6337) uses 0.175; §C0 subsection 10.3 and §C7a (line 2019) use 0.145.
14. **Single-mode penalty.** Waymo's ≈6 dB is tagged [P] in §C7b (line 4965), while the model's own far-field factor is 2.9×, i.e. 4.7 dB (§C0, line 1966). The 6 vs 4.7 dB difference is not discussed anywhere.
15. **Duplicated equations.** Eq. (146) is Eq. (33) (line 1956), and §C10.3b's $w(R)$ is Eq. (34). Both are restated without a cross-reference.
16. **Tag legend** (lines 77–83) says academic papers are [I] and secondary sources are [S]. The block's [P] tags on academic papers and its "[T, secondary sources]" do not follow it.
17. **"Silicon-area multiplier".** §C10.4 (6569) attributes it to §C6; it is in §C8.3 (line 5563).

#### Follow-up cross-checks for this block (second pass, 2026-10-03; new findings only, against the report after both edit batches)

All four cross-reference checks are finished. Locate items by their quotes if the line numbers shift.

**What each check found**

1. **§C8.2 pointer (digitizer):** It resolves, but only to "a 100–400 MHz digitizer (§C7)". §C8.2 gives no converter numbers of its own, and its figure is on a different basis from §C10.2 and §C7a (finding 2).
2. **§E11.2:** The content matches what §C10.6(d) relies on: depth carried as an extra image channel, and "tokenizer" defined. But §E11.2 hedges the claim and tags it [E], while §C10.6(d) states it as fact (finding 9).
3. **§C6's staring-array text:** It exists under "The physics behind it: receive étendue and silicon area" and "What could break this". §C10 paraphrases it with a different formula, puts it more strongly than §C6 does, and in two places departs from §C6's sunlight and pixel-pitch text (findings 5–8, 10).
4. **§C7a's ToF inputs:** The 520 macro-pixels (IMX479: 520 lines × 0.05° = 26°, §C6), the 25 mm aperture and the 30 µm macro-pixel all match. The efficiency inputs do not. §C7a uses PDE 0.37 *at 940 nm* with a 0.784 live fraction (η = 0.145) and FMCW η = 0.25. §C10.3–C10.3b model ToF at 905 nm, and §C10.3a item 7 uses PDE 0.35 with no live fraction and FMCW at 0.504 (findings 1, 3, 4).

#### New findings (most severe first)

**1. Line 6349 (and 6356; repeated in §C10.3b "What the exact computation shows")** — B — **high**
- **Quote:** "≈85 mm² for 25 mm (optics ≈0.5 × PDE ≈0.35)"
- **Problem:** Item 7's efficiencies are on a different basis from the model the report builds in §C7a:
  - **ToF:** item 7 uses 0.5 × 0.35 = 0.175. §C7a uses "$\eta=0.5\times0.37\times0.784=0.145$ (optics transmission × PDE × live fraction)" in bright sun, or 0.185 at night. §C10.3 itself uses 0.15 "about the §C7a value".
  - **FMCW:** item 7 uses QE 0.8 × 1 dB each way = 0.504. §C7a's η = 0.25 also includes "heterodyne mixing efficiency", and the measured chains reach only 0.06–0.17.
  - **Effect:** on §C7a's efficiencies, ToF is 491 × 0.145 = 71 mm² and one FMCW look is (28.8–82.0) × 0.25 = 7.2–20.5 mm². That makes the ratio ≈3.5–10×, not the "2–6×" stated here and repeated in §C10.3b. §C7a's four-look design reaches 4 × 63.7 × 0.25 = 64 mm² at 200 m, about 1.1× below ToF.
- **Proposed rewrite:**
  - ToF cell: "≈70 mm² in bright sun, ≈90 mm² at night, for 25 mm (optics 0.5 × PDE 0.37 at 940 nm × live fraction 0.784, §C7a)".
  - FMCW cell: "≈7–20 mm² per look for 20 mm at 100–300 m, using §C7a's $\eta=0.25$ (optics, QE and heterodyne mixing; measured chains 0.06–0.17)".
  - Lead sentence: "On the §C7a efficiencies, a 25 mm scanned ToF receiver keeps about 3.5–10× the efficiency-weighted aperture of one mirror-scanned FMCW look, and about 1.1× that of §C7a's four looks at 200 m."
  - Update the "2–6×" in §C10.3b to match.

**2. Line 6556** — A/B — medium
- **Quote:** "a balanced detector and a digitizer (an analog-to-digital converter, ADC; §C8.2)"
- **Problem:** The pointer lands on §C8.2 item 4, "a 100–400 MHz digitizer (§C7)". That sends the reader on to §C7 and gives a figure that is ambiguous: it is a beat *bandwidth* (§C7: "100–400 MHz ADC path"), not a sample rate. Elsewhere §C10 relies on different digitizer figures:
  - §C10.2 item 7: "0.2–1 GHz beat at 300 m, i.e. 0.4–2 GS/s", using the 2× Nyquist rule and no Doppler;
  - §C7a(c): "$f_s\approx1.2$ GS/s" for 5 µs chirps, using the 2.5 × ($f_b+f_D$) rule.

  Also, the §C7a design needs four receivers per channel (one per look), each with its own balanced detector and GS/s ADC; this sentence implies one per pixel.
- **Proposed rewrite:** "Each *simultaneously* active coherent receiver needs local-oscillator (LO) power, a balanced detector and a GS/s-class analog-to-digital converter (ADC): ≈1.2 GS/s for 5 µs chirps to 300 m (§C7a(c)), or 0.4–2 GS/s for 10–2 µs chirps (§C10.2, item 7). The four-look design of §C7a needs four such receivers per channel." Separately, in §C8.2: "a digitizer for 100–400 MHz of beat signal (≈0.5–1.2 GS/s with Doppler and the 2.5× sampling rule of §C7a(c))".

**3. Line 6039 (§C10.3; also 6159, 6178, 6409 in §§C10.3a–b)** — B — medium
- **Quote:** "$\eta=0.15$ [E: about the §C7a value, 0.145]"
- **Problem:** §§C10.3–C10.3b model ToF at **905 nm** (E_ph = 2.19×10⁻¹⁹ J; $N_{\rm sp}\approx460$ at 0.905 µm) but take their efficiency from §C7a's **940 nm** IMX479 model (PDE 0.37, live fraction 0.784). The report's own 905 nm PDE data are lower: §C6 reports "22–24% at 905 nm (2021), 37% at 940 nm (2025)". §C6(d) also gives a 77% dead fraction at 905 nm behind a 20 nm filter in full sun, against 22–39% at 940 nm/10 nm. Item 7's "PDE ≈0.35" has the same mismatch.
- **Proposed rewrite (preferred):** move the ToF model to 940 nm: "for ToF: 940 nm (the wavelength of §C7a's PDE 0.37 and live fraction), 25 mm aperture, $N_{\rm req}=20$ and $\eta=0.15$ [E: about the §C7a value, 0.145]". Then use $E_{\rm ph}=2.11\times10^{-19}$ J in §C10.3, in item 1's ToF example and in item 5. Mode counts become $N_{\rm sp}\approx420$ at 0.05° (from 456) and $P_{\rm ToF}$ about 4% lower.
- **Alternative:** keep 905 nm and use a 905 nm PDE of 0.22–0.24 with §C6(d)'s 905 nm dead fraction. This raises $P_{\rm ToF}$ by roughly 1.5× or more in sun.

**4. Line 6300** — B — low
- **Quote:** "ToF: 25 mm aperture, 520 SPAD macro-pixels × ≈460 modes, 2,400 scan columns"
- **Problem:** The 520 count matches §C7a's 520-line, IMX479-based sensor (§C6: "520 lines × 0.05°"). But the ≈460 modes and §C10.3b's ToF model ("field of view equals one mesh cell") assume a 0.05° × 0.05° pixel. §C6(d)'s background model, which §C7a and §C0 subsection 10.3 (b = 2.87) build on, assumes "a 0.1°×0.05° field per macro-pixel":
  - If the 0.1° × 0.05° field is right, each pixel accepts ≈850–910 modes and adjacent columns overlap.
  - If 0.05° is right, the §C7a/§C0 background is 2× too high.

  Separately, 520 × 0.05° spans 26°, not the 25° field; this 4% excess is what makes "available" 5.7×10⁸ slightly exceed "required" 5.5×10⁸.
- **Proposed rewrite:** add a note to the derivation: "Each macro-pixel views 0.05° × 0.05° (IMX479 geometry, 520 × 0.05° = 26°, §C6), giving ≈460 modes at 905 nm (≈420 at 940 nm). §C6(d)'s background assumes a 0.1° × 0.05° field, which would double both the mode count and the background; the two should be reconciled." The fix itself (state the horizontal pixel field and why) belongs in §C6(d) and §C7a.

**5. Line 6321** — A — medium
- **Quote:** "has a finite étendue: detector area × NA², where NA is the numerical aperture of the receive optics. This is the §C6 staring-array penalty"
- **Problem:**
  - §C6 does not use this formula or the term "staring-array penalty". It frames the cost as a short focal length forced onto a fixed-size sensor: "staring over 120° … $D\approx3.8$ mm", against 28.5 mm for a 26° scanned column, i.e. "about **1.8% of the collecting area**" and "roughly **7.5× less range**". Those §C6 numbers are what the reader needs.
  - The étendue formula drops a factor π (≈ π × area × NA²).
  - "which ToF solves by scanning one axis" is firmer than §C6's "A mechanical one-axis scanner appears to be the cheapest proven optical multiplexer at current automotive volumes."
- **Proposed rewrite:** "A staring array (…) has a fixed étendue, about $\pi A_{\rm det}{\rm NA}^2$ for detector area $A_{\rm det}$ and receive numerical aperture NA, which a wide field spreads over many directions. §C6 ('The physics behind it: receive étendue and silicon area') quantifies it: IMX479's 15.8 mm array at f/1.2 gets a ≈28.5 mm aperture as a 26° scanned column but ≈3.8 mm staring over 120°, 1.8% of the collecting area and about 7.5× less range. A one-axis scanner avoids this by sharing a small detector across many time slots; §C6 judges it the cheapest proven way at current volumes."

**6. Line 6613** — A — medium
- **Quote:** "**Steering the receive path through a large aperture is exactly the solid-state capability that §C6 found missing**"
- **Problem:** This overstates §C6, which says: "This is **one attractive missing capability**, not the only route". §C6's alternatives are tiling, smaller SPAD pitch and coherent detection.
- **Proposed rewrite:** "**Steering the receive path through a large aperture is one attractive capability that §C6 found missing ('What could break this', item 3), not the only route**, and the LCM is the most mature candidate for it."

**7. Line 6361** — A — medium
- **Quote:** "signal and solar background both grow with aperture, so the signal-to-noise ratio (SNR) scales approximately as $\sqrt{A_{\rm rx}}$"
- **Problem:** §C6(d), which the report's ToF model uses, says the opposite about the mechanism: "In a bright sunlit scene, SNR (signal-to-noise ratio) per bin is not the problem. **Dead time and pile-up** are". In §C7a sunlight enters through the 0.784 live fraction and a higher Poisson threshold, not through √A scaling. As written, the caveat points the reader to a mechanism the report's numbers do not use.
- **Proposed rewrite:** "For SPAD ToF, bright sun mainly costs dead time and pile-up rather than per-bin SNR (§C6(d)): at 940 nm behind a 10 nm filter it cuts effective PDE by about a third in a fully sunlit scene (live fraction 0.784 in §C7a's central case), and a larger aperture collects proportionally more background. Only for a purely background-limited detector does SNR scale as $\sqrt{A_{\rm rx}}$. A narrowband LO receiver strongly rejects broadband sunlight (≈10³ photons/s in one mode, §C6(d′)), …"

**8. Line 6697** — A — medium
- **Quote:** "So **for small objects, more vertical lines cost silicon, not photons.**"
- **Problem:** This holds only if the receive aperture is kept, which the line does not say. Two passages show the alternatives:
  - §C10.3a item 7: with fixed 30 µm macro-pixels at f/1.2, 0.025° needs a ≈57 mm aperture, "which does not fit".
  - §C6: "smaller pixels do not preserve the photon budget automatically": at a fixed line pitch, shrinking the pixels shrinks the aperture "from about **28.5 to 11.5 mm**".

  The sentence carries §C10.6's explanation of the line race, yet reads as a contradiction of item 7's "erodes ToF's photon advantage".
- **Proposed rewrite:** "So **for small objects, more vertical lines cost silicon rather than photons, provided the receive aperture is kept**: the macro-pixel must shrink in step with the line pitch (smaller SPADs, §C6) or the optics must get faster. With fixed 30 µm macro-pixels at f/1.2, 0.025° would need ≈57 mm (§C10.3a, item 7). Extended-target range does fall, because energy per pixel drops (§C6(b))."

**9. Line 6701** — E/A — low
- **Quote:** "This is a genuine architectural motive, independent of detection range."
- **Problem:** §E11.2 hedges the same point and tags it as an estimate: "it may be one of the real motives behind "camera-like" lidar resolution (§C10.6) [E]". It also describes the mechanism more accurately: depth makes lidar "look like an extra image channel". A patch tokenizer pretrained on RGB has no weights for a depth channel, so "let lidar enter image-pretrained tokenizers" overstates.
- **Proposed rewrite:** "…simplify calibration and fusion, and present depth as an extra channel on the camera's pixel grid, a practical way to feed lidar into image-pretrained networks (§E11.2; a tokenizer is the input stage that cuts an image into patches, or 'tokens'). This is plausibly one real motive for camera-like resolution, independent of detection range [E]."

**10. Line 6352** — B — low
- **Quote:** "| Solid-state flash ToF | ≈3–5 mm | Staring étendue (bite c) | Small |"
- **Problem:** Every other row gives a number. §C6 supplies the input: ≈3.8 mm at f/1.2 for a 120° staring field.
- **Proposed rewrite:** "≈1.6 mm² ($\pi(1.9\ {\rm mm})^2\times0.145$; §C6: 1.8% of the 28.5 mm scanned-column aperture's area)".

#### New consistency flags

1. **§C6(d) pixel field** (line 4294, "0.1°×0.05° field per macro-pixel") against the 0.05° grids of §C7a (520 × 2,400) and §§C10.3a–b. §C0 subsection 10.3's b = 2.87 inherits the 0.1° field (see finding 4).
2. **Digitizer figures are on four different bases:**
   - §C8.2 (line 5569): "100–400 MHz digitizer (§C7)";
   - §C7 (line 4561): "100–400 MHz ADC path";
   - §C10.2 item 7 (line 5908): "0.4–2 GS/s" (2× rule, no Doppler);
   - §C7a(c) and §C7b: 2.5 × ($f_b+f_D$), ≈1.2 GS/s.
3. **Useful aperture per address:** §C8.2 item 2 (line 5553) says "about 0.9 mm at 0.1° and 1550 nm" ($\lambda/\theta$). §C10.3b's area-matched equivalent collecting diameter at 0.1° is ≈0.65 mm (0.33 mm², with $t^2/2$). Both are fine, but the bases differ and are not labelled.
4. **ToF wavelength:** 905 nm in §§C10.3–C10.3b; 940 nm in §C7a, §C0 subsection 10.3 and §C6(d)'s model case (see finding 3).
5. **Scanner wording:** §C6's own term is "the cheapest proven optical multiplexer" (line 4440). This refines earlier finding 36: §C10.4's "(§C6: the mechanical axis as a silicon-area multiplier)" should cite §C8.3, line 5581, or use §C6's wording.

### §E9–§E12 (perception power, heterogeneous sensors, learned stacks, camera-only trucking)

#### Readability review: §E9–§E12 (current lines 7832–8472)

**Coverage.** The whole block was read. Line numbers below include the +6 shift from an insertion in §D7. Every quote was checked against the report by exact-string search. Quotes are in code spans so the Markdown and LaTeX characters stay intact.

##### 1. Overall assessment

- **What reads well.** Each section, and most subsections, opens with its question and a short answer. The derivations are thorough and the arithmetic holds up. I recomputed every substitution and all are correct, except one: 255 m where Eq. (170) gives about 257 m. That includes the §E9 range table, the §E11.1 differences, the §E11.3 grid and data-rate figures, and every §E12 table entry. I also reproduced Eq. (166)'s 88%, 74% and 64% numerically, and the 4.8% value that matches the observed 0.70 ratio.
- **Problem 1: symbols drift.**
  - One quantity carries several symbols: $E_{\rm pulse}$, $E_{\rm point}$ and §C6's $E_{\rm pt}$; also $\Delta\theta$ and $\theta_{\rm step}$.
  - One symbol means several things: $R_{\max}$, IFOV, and $v$ (km/h in §E9, m/s later).
  - Equations are re-derived under new numbers: Eq. (170) = Eq. (162) = Eq. (184), Eq. (177) = Eq. (153), Eq. (178) = Eq. (150).
- **Problem 2: §E11.1 mixes sources.** It compares Fusion4CA, Grace-BEV, MetaBEV and BEVFusion numbers directly, even though the text itself says to compare rows only within one source. BEVFusion-MIT also appears with two different clean scores and no explanation.
- **Problem 3: repetition, and terms defined late or twice.** This runs across §E10–§E11: the missing-modality numbers, NAVSIM, the line-count history and the detection-range scaling each appear twice. NDS, mAP, BEV and "token" are each defined two or three times, and "token space" is given two conflicting meanings.

##### 2. Findings (most severe first)

**1. Line 8100 — A — high**
- **Quote:** `which is why the drop is exactly zero.`
- **Problem:** This says the drop is zero, which means nothing was lost. The intended point is the opposite: the no-lidar score falls to exactly zero (0.0 / 0.0 in the sensor-removal table).
- **Proposed rewrite:** "3. **The architectures are built around lidar, which is why the no-lidar score falls to exactly zero.**"

**2. Line 8185 — A — high**
- **Quote:** `where $R_{\max}$ is the perception range (the grid extends $\pm R_{\max}$ in each direction)`
- **Problem:** Elsewhere $R_{\max}$ is a lidar's maximum detection range: in §E9 of this block (line 7911), §C0 Eq. (42), §C6 Eq. (79) and §F5 Eq. (183). Here it is the half-width of a BEV grid, and Eq. (169) a few paragraphs later goes back to detection range.
- **Proposed rewrite:** "$$N_{\rm cell}=\left(\frac{2R_{\rm grid}}{\Delta_{\rm cell}}\right)^{2} \tag{167}$$ where $R_{\rm grid}$ is the perception range the grid covers (it extends $\pm R_{\rm grid}$ in each direction) and $\Delta_{\rm cell}$ is the side of one cell."

**3. Line 7911 — A — high**
- **Quote:** `Let $E_{\rm pulse}$ be the optical energy the lidar sends toward one independent point, and $R_{\max}$ the largest range`
- **Problem:** The same quantity has three symbols: $E_{\rm pulse}$ here, $E_{\rm point}$ in Eq. (169) (line 8223), and $E_{\rm pt}$ in §C6 Eq. (79), which both passages cite. Detection range is $R_{\max}$ here but $R$ in Eq. (169). "Independent point" is unexplained.
- **Proposed rewrite (§E9):** "Let $E_{\rm pt}$ be the optical energy the lidar sends toward one measured point (the symbol of §C6), and $R_{\max}$ the largest range at which a given target is still detected. … the extended-target model of §C6, Eq. (79), gives $R_{\max}\propto\sqrt{E_{\rm pt}}$."
- **Proposed rewrite (Eq. (169)):** "$$R_{\max}\propto\sqrt{E_{\rm pt}}\ \text{(beam-filling target)},\qquad R_{\max}\propto E_{\rm pt}^{1/4}\ \text{(target smaller than the footprint)} \tag{169}$$"

**4. Line 8077 — A/B — high**
- **Quote:** `keep or slightly beat clean accuracy *within Grace-BEV's own retraining* (BEVFusion-MIT baseline 66.9 mAP), while retaining a fallback.`
- **Problem:** Three issues:
  - MetaBEV's 68.0 is quoted from MetaBEV's own paper (see its table row label), so it is not "within Grace-BEV's own retraining".
  - MEFormer's +3.6 mAP is not "slightly".
  - The next sentence compares against BEVFusion's published 68.5, which line 8079 then forbids.
- **Proposed rewrite:** "Reliability-gated or mixture-of-experts designs keep or beat clean accuracy while retaining a fallback. In Grace-BEV's Table 1, against its retrained BEVFusion-MIT at 66.9 mAP, Grace-BEV scores 68.3 (+1.4) and MEFormer 70.5 (+3.6) [state whether MEFormer was retrained or quoted]; MetaBEV's 68.0 is quoted from its own paper and is not like-for-like." Then delete the "Against BEVFusion's published 68.5 mAP…" sentence, or label it as a cross-source comparison.

**5. Line 7955 — D — high**
- **Quote:** `MetaBEV (ICCV 2023) improved detection NDS (nuScenes detection score, 0–100) by **35.5 points** over vanilla (unmodified) BEVFusion when lidar was missing`
- **Problem:** This is one sentence of about 70 words with parentheses nested inside parentheses. It carries two no-lidar baselines (7.1 and 0.0 NDS), a derivation and a second result.
- **Proposed rewrite:** "MetaBEV (ICCV 2023), a fusion detector built to tolerate a missing sensor, scores about 42.6 NDS (nuScenes detection score, 0–100) without lidar and 69.2 NDS without cameras [I]. Its paper reports the no-lidar figure as 35.5 points above unmodified BEVFusion, implying a baseline of ≈7.1 NDS [E: $42.6-35.5=7.1$]; Grace-BEV's retraining (§E11.1) puts unmodified BEVFusion at 0.0 NDS."

**6. Line 8079 — A — medium**
- **Quote:** `Different papers retrain the same model to different baselines: Grace-BEV's CenterPoint is 56.3 mAP, against 59.6 in BEVFusion's Table I (§E11.3).`
- **Problem:** The more visible discrepancy is never explained. BEVFusion-MIT camera + lidar is 68.5 / 71.4 in the reference table (line 8043, Fusion4CA) but "Clean" 66.9 / 69.7 in the table right after it (line 8054, Grace-BEV).
- **Proposed rewrite:** "Different papers retrain the same model to different baselines: BEVFusion-MIT scores 68.5 mAP in Fusion4CA's Table I (BEVFusion's published value) but 66.9 in Grace-BEV's retraining, and CenterPoint 59.6 in BEVFusion's Table I but 56.3 in Grace-BEV's (§E11.3). Compare rows only within one source." Also add under the reference table: "Grace-BEV's retraining, used in the next table, scores 66.9 / 69.7."

**7. Line 8074 — A — medium**
- **Quote:** `Fusion4CA's extra camera supervision recovers about +1.2 mAP over the fully trained baseline ($69.7-68.5=1.2$)`
- **Problem:** "Fully trained baseline" is undefined. The "6 epochs" in the reference table (line 8044) is never connected to it, so the reader cannot tell whether the two runs had equal training.
- **Proposed rewrite:** "Fusion4CA's extra camera supervision, trained for 6 epochs, scores about +1.2 mAP above the BEVFusion-MIT baseline ($69.7-68.5=1.2$), which was trained for [state the schedule]."

**8. Line 8021 — A — medium**
- **Quote:** `*Late fusion* runs a separate *encoder* (the sub-network that turns raw input into features) for each modality and merges their high-level features near the output.`
- **Problem:** The two sections classify fusion differently:
  - §E10.1 (line 7939) uses early/mid fusion and places BEVFusion under early/mid.
  - §E11.1 uses early/late/BEV fusion, and its "late fusion" is §E10's "mid fusion".
  - The reader cannot tell whether Huang et al.'s theorem covers BEVFusion. In safety writing, "late fusion" also means merging object lists (role 3).
- **Proposed rewrite:** "*Late fusion*, in Huang et al.'s sense, runs a separate *encoder* … and merges their high-level features near the output; this is the 'mid fusion' of §E10.1. [State whether BEV fusion counts as such.] Merging finished object lists from separate stacks, as an independent safety channel does, is a different scheme (§E10.1, role 3)."

**9. Line 8429 — A — medium**
- **Quote:** `Low beams reach the road at ≈50–100 m and high beams at ≈150–250 m (§A6).`
- **Problem:** The night verdict is never tied to Eq. (171), although the table already has a 250 m column.
- **Proposed rewrite (append):** "If an unlit hazard is first seen at the high-beam limit, Eq. (171) leaves $t_{\rm avail}=(150-255)/29.2\approx-3.6$ s to $(250-165)/29.2\approx2.9$ s. At 150 m the truck cannot stop even in the best case, and at 250 m it cannot in the worst, before any of the 0.6–0.9 s needed to call 'stationary' is spent."

**10. Line 8325 — A — medium**
- **Quote:** `SGO times can also be imprecise: the Rimrock record gives 00:03, while the ODI resume dates the fatal crash to 28 Nov 2023.`
- **Problem:** This compares a clock time with a date, so the imprecision cannot be seen. The Rimrock table row (line 8309) also leaves out the time that other rows show.
- **Proposed rewrite:** "…the Rimrock record gives a time of 00:03 [on date …], whereas the ODI resume dates the fatal crash to 28 Nov 2023 [and describes …]; the time is therefore omitted from the table."

**11. Line 8329 — B/C — medium**
- **Quote:** `$$d_{\rm stop}=v\,t_{\rm r}+\frac{v^2}{2a} \tag{170}$$`
- **Problem:** This is Eq. (162) of §E6 (line 7737), and it appears again as Eq. (184) in §F6. With $v=29.2$ m/s, $t_{\rm r}=1.5$ s and $a=2.0$ m/s² it gives about 257 m (256.4 m with $105/3.6$). §E6 and §F6 both print 257 m, but this block uses 255 m at lines 8255, 8332, 8339, 8352 and 8376.
- **Proposed rewrite:** "The stopping distance is the reaction distance plus the braking distance (Eq. (162) of §E6, restated with $d_{\rm stop}$ for $d$): [equation]". Then use "165–257 m" throughout, or say once "(257 m, rounded to 255 m)". The 1.5 s figure at 300 m is unchanged.

**12. Line 8406 — A/B — medium**
- **Quote:** `with $h_{\rm cam}=2.75$ m and $\delta\theta$ = 0.5–2 mrad.`
- **Problem:** The 0.5–2 mrad is not justified. §E2 (line 7456) says braking pitch and road slope reach 0.1–0.5°, which is about 1.7–8.7 mrad.
- **Proposed rewrite:** "…and a residual pitch or grade error $\delta\theta$ = 0.5–2 mrad [E], assuming pitch and grade are estimated online to that accuracy; an uncompensated 0.1–0.5° (1.7–8.7 mrad) change (§E2) would give errors up to about 4× the 2 mrad column."

**13. Line 8354 — A — medium**
- **Quote:** `a 10% size prior (range inferred from an assumed car size known to ±10%)`
- **Problem:** This curve is plotted in Figure E12(b) but has no equation, no table row and no derivation.
- **Proposed rewrite (new derivation item):** "*Size prior.* Range can also be inferred from apparent width, $R=W/\varphi$; with $W$ known to ±10%, $\delta R/R=0.1$: ±25 m at 250 m, ±30 m at 300 m, ±40 m at 400 m, comparable to Eq. (177)."

**14. Line 8215 — A — medium**
- **Quote:** `Beyond about 0.05° at ranges under 150 m, most extra points fall into the same 0.1–0.2 m voxel`
- **Problem:** "Beyond 0.05°" reads as "coarser than 0.05°". The meaning is the opposite: steps finer than 0.05°.
- **Proposed rewrite:** "For angular steps finer than about 0.05°, at ranges under 150 m, neighbouring points lie less than 0.13 m apart, so most extra points fall into the same 0.1–0.2 m voxel: a 0.05° step ($0.873\times10^{-3}$ rad) spans only $150\times0.873\times10^{-3}\approx0.13$ m at 150 m (§C10.6(f))."

**15. Line 8241 — A — medium**
- **Quote:** `Balanced, reliability-gated training fixes most of it at modest cost.`
- **Problem:** This clashes with line 8017 ("Robust training restores only a partial no-lidar fallback.") and with finding 3. "It" is also ambiguous.
- **Proposed rewrite:** "Balanced, reliability-gated training removes the collapse at little or no cost in clean accuracy, but the no-lidar fallback (33–41 mAP) stays far below the fused score (68–71 mAP) (§E11.1, findings 2–3)."

**16. Line 8143 — A — medium**
- **Quote:** `with gaps under about 3% for modest density changes`
- **Problem:** It is unclear whether this means 3 mAP points or 3% of the score, and what counts as a "modest" density change.
- **Proposed rewrite:** "with accuracy gaps under about 3 [mAP points / per cent of the dense-trained score] when the beam count changes by [specify]".

**17. Line 8147 — A — medium**
- **Quote:** `the *token space* is the set of learned representations the pretrained model already understands`
- **Problem:** §E10.1 (line 7940) defines a *token space* as the scene represented as feature vectors. Here it means the model's learned vocabulary. "Token" is also defined a third time at line 7983.
- **Proposed rewrite:** "(A *token* is the unit of input a transformer processes, such as an image patch (§E10.1). A pretrained vision–language model has learned what image-patch tokens mean; lidar tokens fall outside that learned vocabulary. A *tokenizer* cuts raw input into tokens.)"

**18. Line 7936 — A/D — medium**
- **Quote:** `in 2018 Waymo and Mobileye-based cars also localized against stored maps, and with lidar, landmark matching places a car`
- **Problem:** It is unclear whether "with lidar" applies to Mobileye cars, whose maps are camera-built (§E8). The tense mixes 2018 with "places". "Ushr" in the same cell is never explained.
- **Proposed rewrite:** "In 2018 Waymo's cars and Mobileye-equipped cars also localized against stored maps; with lidar, matching landmarks to such a map was said to place a car "down to the centimeter" [T, WSJ, 11 Oct 2018]". In the weaknesses cell: "…of the ≈200,000 highway miles mapped by Ushr (the HD-map supplier for GM's Super Cruise; confirm from source)…".

**19. Line 8410 — A — medium**
- **Quote:** `$$\delta R=\frac{R^{2}\,\sigma_d\,{\rm IFOV}}{b_{\rm st}} \tag{178}$$`
- **Problem:** In Eq. (172) IFOV is the mono pixel (0.25–0.45 mrad); here it is the stereo telephoto pixel (0.1 mrad). The mono-versus-stereo comparison therefore changes two variables at once.
- **Proposed rewrite:** Use ${\rm IFOV}_{\rm st}$ in Eq. (178) and in caption (b), and add: "With the mono camera's 0.25–0.45 mrad pixels the stereo error at 300 m would be ≈3.0–5.4 m, still well below the ground-plane error."

**20. Line 7895 — B — medium**
- **Quote:** `their extrapolated range fell **5.6% with the added sensing/instrumentation powered and 12.2% with that system plus compute**`
- **Problem:** A reader applying Eq. (165) will be stuck. If 447 W gives 12.2%, then the non-compute load of $447-325\approx122$ W should give about 3.7%, not 5.6%. "The two computers" are also never identified in the equipment list.
- **Proposed rewrite (add):** "The two percentages are not proportional to the ≈122 W and 447 W loads, so the extrapolation includes more than a constant electrical load [state what]; the two computers are the RTX 3060 machine and the laptop [confirm]."

**21. Line 8402 — C — medium**
- **Quote:** `*Mono range error.* A single camera can estimate range from where the car's contact point with the road appears in the image.`
- **Problem:** Eq. (177) is §E2's Eq. (153), and Eq. (178) is §E2's Eq. (150), in new notation and without cross-references.
- **Proposed rewrite:** After Eq. (177): "This is Eq. (153) of §E2 with $R$ for $Z$ and $h_{\rm cam}$ for $h$." After Eq. (178): "This is Eq. (150) of §E2 with $f=1/{\rm IFOV}$ pixels per radian and $b=b_{\rm st}$."

**22. Line 8444 — A — medium**
- **Quote:** `The credible camera-first path for trucks would add wide-baseline stereo for range and radar or thermal (infrared) cameras for night and weather.`
- **Problem:** Point 4 (line 8430) shows a 1° radar cannot place a static return in-lane at 300 m. Stereo also shares the night limit.
- **Proposed rewrite:** "…wide-baseline stereo for daytime range and, for night and weather, thermal cameras or an imaging radar whose cross-range cell at 300 m is narrower than the lane (below ≈0.7°, since $3.7/300\approx0.012$ rad; point 4)."

**23. Line 8138 — A — medium**
- **Quote:** `Waymo's scaling study used **500,000 hours** of multimodal driving (§E8), so the leaders drive lidar-equipped fleets for $10^5$–$10^6$+ hours.`
- **Problem:** §E8 (line 7791) does not say "multimodal" and does not mention the "encoded scene representations" that line 8139 attributes to it. "Multimodal" followed by "not raw paired streams" reads as a contradiction. The inference has no [E] tag.
- **Proposed rewrite:** "…500,000 hours of driving logged by its lidar-equipped fleet [P, Baniodeh et al., 2025; §E8], so the leaders' lidar-equipped fleets log $10^5$–$10^6$+ hours [E]." Cite the paper directly in line 8139.

**24. Line 7960 — B — medium**
- **Quote:** `move from 128 to 192, then 520, then 896 lines and switch suppliers between model years`
- **Problem:** §E11.2 (line 8142) cites this passage but gives the sequence "…896 and then 2,160". Neither place has an evidence tag.
- **Proposed rewrite:** "move from 128 to 192, 520, 896 and 2,160 lines… [P/T; spec sheets in §C3b]", with the same sequence in §E11.2.

**25. Line 8255 — C — medium**
- **Quote:** `In short, supervised camera-only assistance (a human driver still monitors and takes over) is plausible, but driverless camera-only trucking faces open problems`
- **Problem:** The answer is buried at the end of the second paragraph.
- **Proposed rewrite:** Move this sentence directly after §E12's first sentence. Move the companion-script sentence (line 8257) into the figure caption.

**26. Line 7982 — D — low**
- **Quote:** `extra modalities complicate training and arbitration; data scale and a uniform fleet matter more; use lidar in training only.`
- **Problem:** All four perspectives (lines 7982–7985) are telegraphic. The imperative reads as the author's own advice rather than the camp's view.
- **Proposed rewrite:** "This camp argues that extra modalities complicate training and arbitration, that data scale and a uniform fleet matter more, and that lidar belongs in training only." Use the same pattern for items 2–4, and change "don't" to "do not".

**27. Line 7935 — A — low**
- **Quote:** `BEVDepth and BEVDistill (§E3, §E8) [I]`
- **Problem:** Neither §E3 nor §E8 mentions these two models.
- **Proposed rewrite:** "BEVDepth and BEVDistill [I] (the lidar-teacher method is explained in §E8)".

**28. Line 8152 — A — low**
- **Quote:** `Huawei's "WA" (world–action) route deliberately skips the language layer`
- **Problem:**
  - §E10.1 calls the same architecture "WEWA", and nothing links the two names.
  - "ADS" is first expanded only at line 8136.
  - §E8 (line 7789) uses "ADS" to mean "automated driving system".
- **Proposed rewrite:** "Huawei's WEWA architecture (§E10.1), whose vehicle-side "WA" (world–action) model [confirm] deliberately skips…". At first use in §E10.1: "Huawei ADS 4 (Huawei's branded driver-assistance system)".

**29. Line 7974 — D — low**
- **Quote:** `NAVSIM shows only 83.8 (camera) vs 84.0 (camera+lidar) PDMS, its 0–100 composite score of a planned trajectory.`
- **Problem:** NAVSIM and PDMS are explained only later (line 8127). "Ablation" (line 7976) is likewise used before it is defined.
- **Proposed rewrite:** "On NAVSIM, a planning benchmark built on logged real driving (§E3), camera-only and camera+lidar planners score 83.8 and 84.0 PDMS (PDM score, a 0–100 composite of safety, progress and comfort)." At line 7976: "matched ablation (removing one sensor and measuring what is lost; §E3)".

**30. Line 8412 — D — low**
- **Quote:** `Both Eq. (177) and Eq. (178) grow as $R^2$, because a fixed angular error produces a range error that grows with the square of distance.`
- **Problem:** The reasoning is circular.
- **Proposed rewrite:** "Both grow as $R^2$ because each reads range from an angle that shrinks as $1/R$ ($h_{\rm cam}/R$ or $b_{\rm st}/R$), so a fixed angular error $\delta\alpha$ gives $\delta R\approx R^2\delta\alpha/h_{\rm cam}$ or $R^2\delta\alpha/b_{\rm st}$."

**31. Line 8259 — E — low**
- **Quote:** `### 1. Promises versus delivery`
- **Problem:** §E10 and §E11 use "E10.1"-style subsection numbers. §E12 uses bare "1.–4.", "subsections 3 and 4" (line 8255), and "Figure E12." where §E11 has "Figure E11.1".
- **Proposed rewrite:** "### E12.1 Promises versus delivery" (likewise E12.2–E12.4), "(§E12.3, §E12.4)", "*Figure E12.1.*"

**32. Line 8463 — E — low**
- **Quote:** `Sources: https://static.nhtsa.gov/odi/inv/2026/INOA-EA26002-10023.pdf ;`
- **Problem:**
  - The sources are bare URLs, unlike the named links in §E9 and §E11.
  - Line 8265 tags Wikipedia as [T], although it is secondary.
  - §E11's list (line 8249) includes Lin et al. (ASPLOS 2018) and the Jin Yuzhi KrASIA interview, which are cited nowhere in the text.
- **Proposed rewrite:** "[NHTSA EA26002 resume](…); …". Change line 8265 to "[S, Wikipedia; T, TechCrunch 2017]". Attach Lin et al. and the KrASIA interview to the claims they support, or drop them.

**33. Line 7888 — E/A — low**
- **Quote:** `so the loss is 6.7 / 26.7 = 25% to 13.3 / 33.3 = 40%.`
- **Problem:** The math is not in $…$, and the step that gives $x$ is skipped.
- **Proposed rewrite:** "adds $x=100\times2/30\approx6.7$ to $100\times4/30\approx13.3$ kWh/100 km…, so the loss is $6.7/26.7=25\%$ to $13.3/33.3=40\%$."

**34. Line 8234 — A — low**
- **Quote:** `during it the vehicle travels $v\,t_{\rm lat}$, for speed $v$ and latency $t_{\rm lat}$.`
- **Problem:** $v$ is in km/h in Eq. (163) but in m/s here, and no units are given.
- **Proposed rewrite:** "…for speed $v$ (m/s) and latency $t_{\rm lat}$ (s)."

**35. Line 8149 — A — low**
- **Quote:** `Read the last claim against the eye-safety discussion in §C4: it is not an established automotive-compliance barrier.`
- **Problem:** Eye safety is covered in §C4c (line 3384), not §C4.
- **Proposed rewrite:** "…in §C4c (subsection 1, IEC 60825-1): …"

**36. Line 8008 — A — low**
- **Quote:** `Short answers (argued in full in §E11.4):`
- **Problem:** §E11.4 is a summary; the arguments themselves are in §E11.1–§E11.3.
- **Proposed rewrite:** "Short answers (argued in §E11.1–§E11.3 and drawn together in §E11.4):"

**37. Line 8115 — A — low**
- **Quote:** `close to what the front third of objects alone would give (±60° is 120° of 360°).`
- **Problem:** The step that supports "detected essentially nothing" is skipped.
- **Proposed rewrite (add):** "If objects were spread evenly in azimuth and the front third were detected at clean accuracy, the score would be $66.9\times120/360\approx22.3$ mAP; the observed 20.2 leaves essentially nothing for the other 240°."

**38. Line 8203 — A — low**
- **Quote:** `Most of that gain comes from BEVFusion's stronger lidar branch: against BEVFusion's own lidar-only version (64.7 mAP, §E11.1), cameras add only about +3.8 mAP.`
- **Problem:** "Most" is never quantified, and the 64.7 comes from Fusion4CA's table, not BEVFusion's.
- **Proposed rewrite:** "Most of that gain, $64.7-59.6=5.1$ of the 8.9 mAP, comes from BEVFusion's stronger lidar branch; cameras add the remaining ≈3.8 mAP ($68.5-64.7$; lidar-only figure from Fusion4CA's Table I)."

**39. Line 8095 — A — low**
- **Quote:** `Because everything except localization is assumed perfect, $\bar m$ is an upper bound on the camera-to-lidar AP ratio that localization alone allows.`
- **Problem:** Reading $\bar m$ as a ratio silently assumes that lidar matches every object.
- **Proposed rewrite:** "Because everything except localization is assumed perfect, and lidar's centimetre-level localization is taken to match every object ($\bar m\approx1$ for lidar), $\bar m$ is an upper bound…"

**40. Line 7933 — E/D — low**
- **Quote:** `Huawei ADS SE (no lidar) vs Pro/Max. BYD God's Eye C vs A/B`
- **Problem:** There are no evidence tags, and the reader is not told which God's Eye tiers carry lidar.
- **Proposed rewrite:** "Huawei ADS SE (no lidar) vs Pro/Max (with lidar); BYD God's Eye C (vision-only) vs A (three lidars) and B (one or two) (§E1) [T]".

##### 3. Consistency flags to check elsewhere

- **Stopping distance.** This block uses 165–255 m (lines 8255, 8332, 8339, 8352, 8376). §E6 quotes 165–255 m (7732) but derives about 257 m (7741). §F6 also derives 257 m (8749). The same equation appears three times as Eq. (162), Eq. (170) and Eq. (184).
- **Energy per point and maximum range.**
  - §C0 Eq. (42) uses $E_{\rm tx}$ (2137).
  - §C6 Eq. (79) uses $E_{\rm pt}$ (4251).
  - §C10.2 uses $E_{\rm pulse}$ (5862).
  - §F5 Eq. (183) uses $E_{\rm pt}$ (8729).
  - This block uses $E_{\rm pulse}$ (7911) and $E_{\rm point}$ (8223), and uses $R_{\max}$ for a grid half-width (8185).
- **Mono and stereo assumptions.** §E2 sets $h=1.5$ m with pitch/slope of 0.1–0.5° (7454–7456). For stereo it uses $b=1.2$ m, 140 µrad pixels and 0.25 px, giving 4.7 m at 400 m (7431). §E12 uses $h_{\rm cam}=2.75$ m, 0.5–2 mrad, $b_{\rm st}=1.5$ m, 0.1 mrad and 0.2 px, giving 2.1 m at 400 m. The two sets of assumptions are not cross-referenced.
- **Angular-step symbol.** §E2 and §E11.3 (8215) use $\Delta\theta$. §E12 (8414) uses $\theta_{\rm step}$, and uses $\delta\theta$ for pitch error.
- **Huawei ADS fleet size.** §E1 (7397) says "More than 2 M vehicles; 14.5 B km [P]". §E11.2 (8136) says "1.7 million ADS vehicles by April 2026 [T]". Both should be dated or reconciled.
- **"ADS" has two meanings.** §E8 (7789) uses it for "automated driving system"; §E10.1 and §E11.2 use it as Huawei's brand name.
- **128-line point rate.** §E11.3 (8213) says "2–3 Mpts/s". §C0 (1527) and §C3b (3041) give 1.536 Mpts/s for the AT128 in single-return mode. Say if 2–3 Mpts/s means dual return.
- **Multi-gigabit claim.** Line 8214 says a 2,160-line unit "needs a multi-gigabit link", but the polar-packet rate at line 8213 starts at 0.8 Gbit/s, which fits on 1000BASE-T1.
- **§C6(e) pointer.** §E10.2 (7966) points to §C6(e), which is "Histogram memory" (4377). The ≈98% on-chip data reduction is in §C5a (3858).
- **HD radar.** §E12 (8444) and §E1 (7393) say "unused"; §E2 (7617) says "reportedly unused [I/T]".
- **§E11.1 baselines and sources.**
  - BEVFusion-MIT clean is 68.5 / 71.4 at 8043 but 66.9 / 69.7 at 8054.
  - CenterPoint is 56.3 at 8046 but 59.6 at 8198.
  - The BEVFusion paper's Table I is used at 8081, 8097 and 8111 but is missing from the §E11.1 source line (8071); it appears only in the end list (8249).
- **Repeated content.**
  - Detection-range scaling: §E9 (7911) and §E11.3 (8223).
  - Missing-modality numbers: §E10.2 (7955), §E10.3 (7975) and §E11.1.
  - NAVSIM/PDMS definitions: §E3 (7663) and §E11.1 (8127).
  - NDS/mAP definitions: §E3, §E10.2 and §E11.1.
- **Figure labels.** "Figure E11.1" (8108) versus "Figure E12." (8351).
- **Ambiguous parallel.** "Light's Clarity … claimed 10 cm to 1 km" (8272) sits next to NODAR's "a 10 cm object at 150 m" (8271). The reader cannot tell whether Clarity's figure is a depth span or an object size at range.
- **Spelling.** "Naïvely" (7954) versus "naive" (7956, 8058, 8066, 8076).

