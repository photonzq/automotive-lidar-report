"""High-severity readability and consistency fixes from the 2026-10-03 review of the scientific sections. Hash-guarded.

Each edit replaces one exact passage that must occur exactly once in the current text, applied in order.
  python apply_readability_high.py --dry   # check every anchor and report; nothing is written
  python apply_readability_high.py         # write the live report (aborts if it changed after being read)
"""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")

EDITS = [
    # ---- §C0 subsections 1-9
    ("C0.7 per-point rule",
     r"""A full FMCW point needs more: under the per-point rule of subsection 10.3 ($10^{-3}$ false points over a 0–300 m search, with the echo's peak found in both chirp ramps), one look needs ≈259 and four summed looks ≈88.""",
     r"""A full FMCW point is held to the stricter per-point rule of §C0 subsection 10.3 (at most $10^{-3}$ false points over a 0–300 m search, with the echo's peak found in both chirp ramps). With one look it then needs ≈259 photoelectrons, twice the single-bin ≈130; four independent looks bring the total, summed over both ramps and all looks, down to ≈88."""),
    ("C0.1 R_amb table",
     r"""| Unambiguous range per channel | $R_{\max}=c/(2\,\text{PRF})$ |""",
     r"""| Unambiguous range per channel | $R_{\rm amb}=c/(2\,\text{PRF})$ |"""),
    ("C0.1 R_amb derivation",
     r"""- **Unambiguous range:** $R_{\max}=c/(2\,\text{PRF})=""",
     r"""- **Unambiguous range:** $R_{\rm amb}=c/(2\,\text{PRF})="""),
    ("C0.1 R_amb definition",
     r"""$3.0\times10^8/(2\times300\times10^3)=500$ m at 300 kHz.""",
     r"""$3.0\times10^8/(2\times300\times10^3)=500$ m at 300 kHz. $R_{\rm amb}$ is the farthest range whose echo returns before the next pulse leaves (subsection 9 uses the same symbol); elsewhere $R_{\max}$ means the maximum detection range."""),
    # ---- §C0 subsection 10
    ("C0.10 equal apertures",
     r"""When both receivers use the same aperture, sized optimally for the coherent beam at each range, FMCW needs about 2.5 times the energy per sample of SPAD ToF, whatever the range. This underlies the energy-per-point comparisons between ToF and FMCW in §C7a and §C10.""",
     r"""When each of the FMCW receiver's two apertures (its four looks are two polarizations on each of two spatial modes, §C7a) is as large as the ToF lens and sized optimally for the coherent beam at each range, FMCW needs about 2.5 times the energy per point of SPAD ToF, whatever the range. Against the fixed 25 mm ToF lens of §C7a the factor is 3.1 at 200 m (10.5), the ≈3.2× used in §C7a, §C7b and §C10."""),
    ("C0.10 sixteen times",
     r"""needs five times the energy of the best FMCW design, i.e. sixteen times ToF's.""",
     r"""needs five times the energy of the best FMCW design: 1.5 µJ per point against 303 nJ, or sixteen times the 96 nJ of the 25 mm ToF design. The best FMCW design already needs 3.2 times ToF's energy here, not 2.5 times, because the ToF lens (25 mm) is larger than FMCW's 22 mm optimum."""),
    ("C0.10 direct rises",
     r"""on these axes, falling 20 dB per decade of range for every lens.""",
     r"""on these axes, rising 20 dB per decade of range for every lens."""),
    ("C0.10 coherent rises",
     r"""- **Coherent detection is flat, then falls.** Each curve is level out to about its Rayleigh range (41, 257 and 1,026 m for 10, 25 and 50 mm) and falls 20 dB per decade beyond it, 4.7 dB below the direct-detection line of the same aperture.""",
     r"""- **Coherent detection is flat, then rises.** Each curve is level out to about its Rayleigh range (41, 257 and 1,026 m for 10, 25 and 50 mm) and rises 20 dB per decade beyond it, 4.7 dB above (worse than) the direct-detection line of the same aperture."""),
    ("C0.10 envelope",
     r"""It falls only 10 dB per decade ($1/R$), because the best aperture grows as $\sqrt R$.""",
     r"""Its loss rises only 10 dB per decade ($1/R$), because the best aperture grows as $\sqrt R$."""),
    ("C0.10 direct fraction",
     r"""- **Direct detection falls as $D^2/R^2$ at every range.**""",
     r"""- **Direct detection collects a fraction proportional to $D^2/R^2$ at every range.**"""),
    ("C0.10 coherent collection",
     r"""- **Coherent detection is flat, then falls.** With 0.3 µJ,""",
     r"""- **Coherent collection is flat, then falls** (its loss is flat, then rises). With 0.3 µJ,"""),
    ("C0.10 four looks formed",
     r"""(polarization, wavelength or spatial diversity; each is one *look*, taken by its own coherent receiver), with $\bar n$ split equally among them:""",
     r"""(polarization, wavelength or spatial diversity; each is one *look*, taken by its own coherent receiver. The model's four looks are two polarizations on each of two spatial modes, received through two equal apertures, so each collects the full $\mathcal{L}_{\rm coh}$ from the same transmitted energy, §C7a), with $\bar n$ split equally among them:"""),
    ("C0.10 efficiency wording",
     r"""**The FMCW value, 0.25, is a design value at the optimistic end of what has been measured.**""",
     r"""**The FMCW value, 0.25, is a design value about 1.5× above the best coherent chain measured so far.**"""),
    # ---- §C4
    ("C4 C4 gain",
     r"""That alone does not confer 17.49% more power in every scan or pulse regime, because other rules (pulse-train and average-power limits) may bind first.""",
     r"""Every Class 1 limit this report uses between 700 and 1,050 nm (single pulse, pulse train via $C_5$, and long-exposure average power; table in §C4c) contains $C_4$, so a 940 nm design may emit 17.5% more than an otherwise identical 905 nm design whichever rule binds. This is a gain in permitted emission, not in range or signal-to-noise ratio [E]."""),
    ("C4c InGaAs area",
     r"""An IMX479-sized 244 mm² focal plane (the 12.2 × 20.0 mm Sony SPAD chip of §C5a) would cost ≈\$250–2,500 in processed InGaAs at 1–10 €/mm² (244 mm² × 1–10 €/mm² = 244–2,440 €, taking €1 ≈ \$1), before hybridization to a silicon readout (bump-bonding the InGaAs detector chip, pixel by pixel, onto a silicon readout chip, a further cost). The Si SPAD equivalent is ≈\$17–44 (§C5a).""",
     r"""An InGaAs array with IMX479's active area (≈16.7 mm², 105 × 1,568 pixels at 10.08 µm pitch, §C6) would cost ≈\$17–170 in processed InGaAs at 1–10 €/mm² (16.7 mm² × 1–10 €/mm², taking €1 ≈ \$1) [E]. That comes on top of a silicon readout chip of roughly the size and cost of the ≈\$17–44 Si SPAD die (§C5a), and of hybridization (bump-bonding the InGaAs detector chip, pixel by pixel, onto that silicon readout chip). Per mm², processed InGaAs costs 10–100× the silicon."""),
    ("C4c 905 emitters",
     r"""- **905 nm** (EELs) is the incumbent for the Hesai AT/ATX and RoboSense M series.""",
     r"""- **905 nm** is the incumbent: VCSEL columns in the Hesai AT128/ATX and edge-emitting lasers (EELs) in the RoboSense M series (§C3)."""),
    ("C4c EEL drift",
     r"""EEL drift (the shift of the emission wavelength as the laser warms) forces wide filters, which admit more sunlight.""",
     r"""Where the source is an EEL, its drift (the shift of the emission wavelength as the laser warms) forces wide filters, which admit more sunlight."""),
    # ---- §C5, §C5a, §C6
    ("C5 bottom line",
     r"""**Bottom line.** Neither pattern establishes foundry identity, wafer provenance (where the wafers were made) or production yield (the share of chips that work).""",
     r"""**Bottom line.** Some Chinese "in-house" SPAD-SoCs are Sony parts (pattern (a)), made in Sony's own fabs. The others are distinct designs (pattern (b)), whose foundry, wafer provenance (where the wafers were made) and production yield (the share of chips that work) are all undisclosed."""),
    ("C5 relabeled",
     r"""- No public evidence shows Sony dies relabeled as in-house, or Sony pixel wafers bonded to Chinese logic wafers; Sony is not known to sell SPAD pixel wafers.""",
     r"""- No public evidence shows a Sony die marked or sold as the lidar maker's own design, as distinct from pattern (a), where marketing calls an unnamed Sony part a "SPAD-SoC". Nor is there evidence of Sony pixel wafers bonded to Chinese logic wafers; Sony is not known to sell SPAD pixel wafers."""),
    ("C5a Huawei lever",
     r"""Huawei's move to in-house SPAD-SoCs (D3/D5/Limera, §D1a) removes that lever.""",
     r"""Huawei's newer units with in-house SPAD-SoCs (§D1a) remove that lever for those products; the 192-line L306/D3, very likely built on Sony's IMX459 (§C5), still depends on it."""),
    ("C6 intro moving axis",
     r"""this is why every long-range "digital" (SPAD-based) lidar shipping or announced still keeps one moving axis""",
     r"""this is why every long-range lidar shipping or announced, SPAD-based ("digital") or SiPM-based, still keeps one moving axis"""),
    ("C6 per point",
     r"""The detected signal photons per shot are then""",
     r"""The detected signal photons per point, summed over all the shots that make up the point, are then"""),
    ("C6 per shot numbers",
     r"""Eq. (80) gives about 21 detected photons at PDE 24% and about 33 at PDE 37%.""",
     r"""Eq. (80) gives about 21 detected photons at PDE 24% and about 33 at PDE 37%, i.e. ≈2–3 per shot over the ≈10 shots of a point (Eq. (80) is §C0 Eq. (23) with $T_{\rm atm}=1$ and the energy per point in place of the pulse energy)."""),
    ("C6 thresholds",
     r"""This is conceptually what IMX479's pixel-level threshold control and RoboSense's multi-threshold TDC (time-to-digital converter) do [T/I].""",
     r"""RoboSense's multi-threshold TDC (time-to-digital converter) applies this idea [T/I]. IMX479's pixel-level threshold control is a different mechanism: it sets the comparator level at which a pulse counts as an avalanche, which keeps the dead time stable (§C5a)."""),
    ("C6 industry evidence",
     r"""every long-range "digital" (SPAD-based) product shipping or announced keeps one moving axis (Hesai ETX and ATX, RoboSense EM4 and Phoenix units, Huawei 896, Seyond Robin E2).""",
     r"""every long-range SPAD-SoC ("digital") product shipping or announced keeps one moving axis (Hesai ETX, RoboSense EM4 and Phoenix-based units, Seyond Robin E2). So do the SiPM-based Hesai ATX and the Huawei 896-line, whose detector type is undisclosed (§C5)."""),
    # ---- §C7a
    ("C7a vendors publish",
     r"""**No FMCW vendor publishes point rate, range and power for the same configuration.** That silence is itself informative, because those three numbers together are what the energy-per-point comparison needs.""",
     r"""**Only one FMCW vendor publishes point rate, range and power for the same configuration:** Analog Photonics, whose FS-4S datasheet gives 90 kpts/s at 200 m on a 10% target in a 20° × 10° region-of-interest mode at 35 W, i.e. ≈390 µJ per point [P] (§C0 subsection 10.8, §C3b). The automotive FMCW vendors do not, and that silence is itself informative, because those three numbers together are what the energy-per-point comparison needs."""),
    ("C7a efficiency wording",
     r"""The FMCW value, 0.25, is a design value at the optimistic end of what has been measured.""",
     r"""The FMCW value, 0.25, is a design value about 1.5× above the best coherent chain measured so far."""),
    ("C7a eye safety gated",
     r"""which FMCW's 3.0–7.6 W at 10–25 Mpts/s and 200 m fits within (§C7b subsection 2(i))""",
     r"""which FMCW's 3.0–7.6 W at 10–25 Mpts/s and 200 m fits within if its transmitter is gated during the round trips; ungated, it emits 3.5–9.6 W and can reach the allowance at 25 Mpts/s (§C7b subsection 2(i))"""),
    ("C7a Waymo DFB",
     r"""- **Parts.** Waymo's thermally chirped DFB with pre-distortion holds <100 kHz error over 1 GHz (nonlinearity $<10^{-4}$) [P]: enough at 200–250 m, marginal at 300 m by Eq. (112) [E].""",
     r"""- **Parts.** Waymo's thermally chirped DFB with pre-distortion holds its frequency error below 100 kHz over a 1 GHz sweep, a fractional error $\delta\nu/B<10^{-4}$ [P]. Eq. (112) allows a peak deviation of 94 kHz at 200 m, 75 kHz at 250 m and 62.5 kHz at 300 m: read as a peak-to-peak bound (±50 kHz) the figure meets 200–250 m and is marginal at 300 m, while as a peak deviation it is marginal already at 200 m [E]."""),
    ("C7a light alone",
     r"""At 10 Mpts/s and 300 m the light alone is ≈30 of ≈68 W of sensor power (§C7b subsection 2(h)).""",
     r"""At 10 Mpts/s and 300 m, producing the useful light alone takes ≈30 W of the sensor's ≈68 W electrical draw (4.5 W of optical power at 15% wall-plug efficiency), and light emitted during the round-trip dead time takes ≈9 W more (§C7b subsection 2(h))."""),
    # ---- §C7b
    ("C7b short gap",
     r"""The reason is spatial, not temporal** (subsection 1).""",
     r"""The reason is spatial, not temporal** (subsection 1). With the coherent efficiencies measured so far (0.057–0.168), the gap is 5–14× rather than 3.2× (subsection 1(c))."""),
    ("C7b short CW waste",
     r"""apart from the 12–35% it emits during the round-trip dead time, before any usable echo has returned.""",
     r"""apart from the 12–35% it emits during the last $\tau$ of each ramp, whose echo falls in the next ramp's discarded window."""),
    ("C7b short eye safety",
     r"""3× what FMCW needs at 10 Mpts/s and 200 m, but only 1.2× at 25 Mpts/s.""",
     r"""3× what a gated FMCW transmitter needs at 10 Mpts/s and 200 m, but only 1.2× at 25 Mpts/s, where an ungated one can reach the allowance."""),
    ("C7b short reach",
     r"""The headroom extends eye-safe reach towards ≈600 m at moderate point rates""",
     r"""The headroom extends eye-safe reach towards ≈470–600 m (ungated to gated) at moderate point rates"""),
    ("C7b short parity",
     r"""  - If any one of them is missing, a 15 Mpts/s sensor stays at ≈15–20 W against a 15 W target. Today's central case is ≈67 W.""",
     r"""  - Without the efficient laser or the lower energy per point, a 15 Mpts/s sensor stays near 19.5 W against a 15 W target; without the low-power receiver it stays near 44 W. Today's central case is ≈67 W."""),
    ("C7b efficiency wording",
     r"""The FMCW value, 0.25, is at the optimistic end of what has been measured:""",
     r"""The FMCW value, 0.25, is a design value about 1.5× above the best coherent chain measured so far:"""),
    ("C7b dead time placement",
     r"""- **Round-trip dead time.** A CW channel keeps transmitting during the first $\tau$ of each ramp, before any usable echo exists (subsection 2(a)).""",
     r"""- **Round-trip dead time.** The receiver discards the first $\tau$ of each ramp (subsection 2(a)). The light a CW channel sends during the last $\tau$ of each ramp returns in that discarded window of the next ramp and is wasted; the wasted transmission and the receiver's dead time each last $\tau$ per ramp, $2\tau$ per point."""),
    ("C7b Waymo DFB",
     r"""  - Waymo reports a pre-distorted DFB holding <100 kHz error over 1 GHz, i.e. $\varepsilon<10^{-4}$ [P] (§C7a(f)). By Eq. (112) that is enough at 200–250 m and marginal at 300 m; the exact margin depends on the shape of the error [E].""",
     r"""  - Waymo reports a pre-distorted DFB holding <100 kHz error over 1 GHz [P] (§C7a(f)), a fractional frequency error $\delta\nu/B_{\rm eff}<10^{-4}$. With the bow shape of Eq. (112) and $\delta\nu_{\max}=100$ kHz it would give $\varepsilon=8\times10^{-4}$, just outside the 94 kHz tolerance at 200 m. Read as a peak-to-peak bound (±50 kHz) it meets 200–250 m and is marginal at 300 m (62.5 kHz), so the margin depends on how the figure is defined and on the error's shape [E]."""),
    ("C7b 2(i) emission",
     r"""  - FMCW emits $\dot NE_{\rm opt}$: 3.0 W at 10 Mpts/s and 200 m, a third of the 9.1 W, and 7.6 W at 25 Mpts/s, 83% of it. At 300 m it needs 4.6 and 11.4 W; the latter exceeds the allowance for this field.""",
     r"""  - A gated FMCW transmitter (dark during the last $\tau$ of each ramp, item 2 below) emits $\dot NE_{\rm opt}$: 3.0 W at 10 Mpts/s and 200 m, a third of the 9.1 W, and 7.6 W at 25 Mpts/s, 83% of it. At 300 m it needs 4.6 and 11.4 W; the latter exceeds the allowance for this field. An ungated transmitter also emits during the round trips, 1.14–1.27 times as much at 16–30 mW per channel (Eq. (107)): 3.5–3.8 W at 10 Mpts/s and 8.6–9.6 W at 25 Mpts/s at 200 m, so at 25 Mpts/s it can exceed the allowance [E]."""),
    ("C7b 2(i) operating point",
     r"""  - At the 200 m operating point of this section neither design is limited by eye safety, so the per-watt comparison stands.""",
     r"""  - At the 200 m operating point of this section neither design is limited by eye safety at 10 Mpts/s, so the per-watt comparison stands; at 25 Mpts/s an ungated FMCW transmitter reaches the allowance."""),
    ("C7b 2(i) reach",
     r"""so that is ≈600 m of eye-safe reach on a 10% target.""",
     r"""so that is ≈600 m of eye-safe reach on a 10% target with a gated transmitter, or ≈470 m ungated at 30 mW per channel [E]."""),
    ("C7b 2(i) reach 25",
     r"""At 25 Mpts/s the headroom shrinks to 0.36 µJ per point, i.e. ≈240 m.""",
     r"""At 25 Mpts/s the headroom shrinks to 0.36 µJ per point, i.e. ≈240 m gated or ≈190 m ungated."""),
    ("C7b 5 parity text",
     r"""With all three, a 15 Mpts/s sensor reaches ≈12 W. With any two of the three, it stays at ≈15–20 W, above the 15 W target.""",
     r"""With all three, a 15 Mpts/s sensor reaches ≈12 W counting only the useful light, and 14–16 W once the light sent during the round trips is counted (below). Without the efficient laser, or without the lower energy per point, it stays near 19.5 W; without the low-power receiver it stays near 44 W. A receiver at 0.30 µJ per point, 7× better than today's but 3× short of the goal, lands at the 15 W target."""),
    ("C7b 5 parity table",
     r"""| Two of three: $E_{\rm rx}$ at 0.30 µJ | 0.15 µJ | 30% | 0.50 µJ | 0.30 µJ | 0.80 µJ | 15 W (borderline) |""",
     r"""| Receiver only partly improved: $E_{\rm rx}$ at 0.30 µJ | 0.15 µJ | 30% | 0.50 µJ | 0.30 µJ | 0.80 µJ | 15 W (borderline) |
| Two of three: $E_{\rm rx}$ stays at today's 2.23 µJ | 0.15 µJ | 30% | 0.50 µJ | 2.23 µJ | 2.73 µJ | 44 W |"""),
    # ---- §C10
    ("C10 camera-like",
     r"""4. Does the push to **2,000+ line, "camera-like" lidar** (2,000 or more rows of points in the vertical) create value?""",
     r"""4. Does the push to **"camera-like" lidar** create value? Here camera-like means about 0.025–0.03°, an 8 MP camera's pixel pitch over 120° (§C10.1); vendors' "2,000+ line" claims go further, since 2,000 rows over a 25° vertical field is a $25^\circ/2{,}000=0.0125^\circ$ pitch."""),
    ("C10 ToF aperture",
     r"""At fixed range, ToF's required power scales as $1/\Omega_{\rm cell}$ (§C10.3), where $\Omega_{\rm cell}$ is the solid angle of one angular sample, and its usable aperture shrinks at fixed f-number (focal length divided by aperture diameter). Ideal full-coverage coherent power does not grow as $1/\Omega_{\rm cell}$ (§C10.3; §C10.3a, item 7).""",
     r"""At fixed range and aperture, ToF's required power scales as $1/\Omega_{\rm cell}$ (§C10.3), where $\Omega_{\rm cell}$ is the solid angle of one angular sample. The aperture cannot grow to compensate: at a fixed f-number (focal length divided by aperture diameter) and macro-pixel size a finer pixel angle needs a larger lens, and a behind-glass module holds only about 25–30 mm, so the pixels must shrink instead (§C10.3a, item 7). Ideal full-coverage coherent power does not grow as $1/\Omega_{\rm cell}$ (§C10.3; §C10.3a, item 4)."""),
    ("C10.2 OPA watts",
     r"""  - several watts per beam at 5 µs dwell [E]: with ≤3 dB one-way loss, ≈9 W for four-look and ≈26 W for single-look detection, or ≈540–1,590 W for 60 beams at 12 Mpts/s.""",
     r"""  - about 9–26 W per beam at 5 µs dwell and 3 dB one-way loss [E], if the looks share one receive mode (wavelength or time diversity): ≈9 W for four-look and ≈26 W for single-look detection, or ≈540–1,590 W for 60 beams at 12 Mpts/s. With polarization or spatial diversity each look adds a receive mode, which cuts the four-look figure about 4×, to ≈2.3 W per beam (≈135 W for 60 beams)."""),
    ("C10.2 OPA 26.4",
     r"""259 need $259/9.8=26.5$ W""",
     r"""259 need $259/9.8=26.4$ W"""),
    ("C10.2 OPA 1590",
     r"""$60\times26.5=1{,}590$ W""",
     r"""$60\times26.4\approx1{,}590$ W"""),
    ("C10.3 headline",
     r"""At a fixed photon budget, gap-free single-mode coherent coverage of 120° × 25° to 200 m ideally needs 20–184 W, against 0.23–14.4 W for ToF at 0.1° to 0.0125° sampling.""",
     r"""For a 10% target at 200 m and 10 Hz, gap-free single-mode coherent coverage of 120° × 25° needs 20–184 W at a non-fading threshold of 10–30 detected photons, and about 180–1,590 W once speckle fading is counted under the report's per-point rule (caveat 4; §C10.2, item 5); ToF needs 0.23–14.4 W at 0.1° to 0.0125° sampling."""),
    ("C10.3 sunlight caveat",
     r"""- *No sunlight.* Solar background, which raises the ToF $N_{\rm req}$, is left out (caveat 4 below).""",
     r"""- *Sunlight.* For ToF, $N_{\rm req}=20$ already corresponds to bright sun (§C0 subsection 10.3: 17.3 counts for an ideal counter, 25 in the §C7a model); at night ≈5 counts suffice."""),
    ("C10.3 ToF inputs",
     r"""The assumed inputs are, for ToF: 905 nm, 25 mm aperture, $N_{\rm req}=20$, $\eta=0.15$.""",
     r"""The assumed inputs are, for ToF: 905 nm, 25 mm aperture, $N_{\rm req}=20$ [E: close to the bright-sun requirement of §C0 subsection 10.3] and $\eta=0.15$ [E: about the §C7a value, 0.145]."""),
    ("C10.3a channels",
     r"""- Matching the 1/e² beam area to all cells with a 20 mm coherent aperture would need about 2,400–12,000 parallel channels under these dwell assumptions ($1.2\times10^{8}$ slots divided by $5\times10^{4}$ or $10^{4}$ dwells per channel per frame, for 2 µs or 10 µs dwells).""",
     r"""- Covering the whole field with the native 1/e² spots of a 20 mm aperture (a nominal footprint fraction of one, not the widened "area-matched" spot of §C10.3b) would need about 2,400–12,000 parallel channels by this mode count ($1.2\times10^{8}$ slots divided by $5\times10^{4}$ or $10^{4}$ dwells per channel per frame, for 2 µs or 10 µs dwells). The footprint count of §C10.3b gives half that, ≈1,200–5,800, because one nominal footprint spans ≈2 hard-aperture modes at 200 m; this is also why the table shows ≈1% where §C10.3b's Result 2 shows 2.1%."""),
    ("C10.3b near field",
     r"""The aperture is larger than the confocal optimum there, so the target sits in the beam's near field. The simple expectation $N_{\rm sp}\approx1$ is therefore too optimistic.""",
     r"""At 100 m the 20 mm aperture is larger than the confocal optimum (≈16 mm), so the target sits in the beam's near field. At 200 m it is close to the optimum (≈22 mm), yet the hard aperture still spans about two coherence areas of the speckle, $A_{\rm rx}\pi w^2/(\lambda R)^2=314\ {\rm mm^2}/152\ {\rm mm^2}\approx2.1$, because the Gaussian launched with $w_0=0.45D$ does not fill it. The simple expectation $N_{\rm sp}\approx1$ is therefore too optimistic even at the optimum."""),
    # ---- Part E
    ("E2 lane",
     r"""is **wider than a lane**. The radar therefore cannot tell, from angle alone, which lane a distant object is in.""",
     r"""spans **one to two lane widths**. Two objects in adjacent lanes at the same range and speed therefore share one cell and cannot be separated by angle, although an isolated strong reflector can be located more finely (see "Ways past the ceiling" below)."""),
    ("E2 radar ratio",
     r"""That is about 45 radars for every lidar ($166/3.7\approx45$), against Yole's 3.7 M lidars for passenger-car programmes (§B1) [E].""",
     r"""That is about 100 radars for every passenger-car lidar shipped in the same year ($166/1.6\approx104$, against Yole's 1.6 M lidar units for 2024, §B1) [E]; Yole's 2025 radar volume is not given, so a 2025 ratio cannot be formed."""),
    ("E5 system target",
     r"""- The headline system target of $10^{-8}$/h needs $\beta$ well below $10^{-4}$ (or a lower $p$): at $\beta=10^{-4}$ the common-cause term alone is $10^{-8}$/h. That cannot be validated from subsystem data alone [E],""",
     r"""- A system target of $10^{-8}$/h (the order of the ISO 26262 ASIL D target for random hardware failures, which was not written for perception failures [U]) cannot be met at $p=10^{-4}$/h: the independent term alone, $[(1-\beta)p]^2\approx10^{-8}$/h, already uses the whole target, so the per-channel rate must fall as well. With $p=10^{-5}$/h, for example, the independent term drops to $10^{-10}$/h and $\beta\approx10^{-3}$ gives $10^{-3}\times10^{-5}+10^{-10}\approx1.0\times10^{-8}$/h [E]. Such a $\beta$ cannot be validated from subsystem data alone [E],"""),
    ("E10 MetaBEV",
     r"""  - MetaBEV (ICCV 2023) improved detection NDS (nuScenes detection score, 0–100) by **35.5 points** over vanilla (unmodified) BEVFusion when lidar was missing (to about 42.6 NDS, implying a ≈7.1 NDS baseline in MetaBEV's own comparison [E: $42.6-35.5=7.1$]; the §E11.1 table, from Grace-BEV, lists vanilla BEVFusion at 0.0 NDS without lidar), and kept **69.2 NDS** with cameras absent [I].""",
     r"""  - MetaBEV (ICCV 2023), a fusion detector built to tolerate a missing sensor, scores about 42.6 NDS (nuScenes detection score, 0–100) without lidar and **69.2 NDS** without cameras [I]. Its paper reports the no-lidar figure as **35.5 points** above unmodified BEVFusion, implying a baseline of ≈7.1 NDS [E: $42.6-35.5=7.1$]; Grace-BEV's retraining (§E11.1) puts unmodified BEVFusion at 0.0 NDS without lidar."""),
    ("E11 zero",
     r"""3. **The architectures are built around lidar, which is why the drop is exactly zero.**""",
     r"""3. **The architectures are built around lidar, which is why the no-lidar score falls to exactly zero.**"""),
]

raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
assert "\r\n" not in text, "report has CRLF line endings"
problems = []
for label, old, new in EDITS:
    n = text.count(old)
    if n != 1:
        problems.append(f"{label}: anchor found {n} times")
        continue
    low = new.lower()
    for word in ("corrected", "updated", "revised", " added", " now ", " new "):
        if word in low and word not in old.lower():
            problems.append(f"{label}: versioning word {word.strip()!r} in new text")
    # math delimiters: unescaped $ (currency is written \$); a fragment may be odd, but must match the anchor's parity
    if len(re.findall(r"(?<!\\)\$", new)) % 2 != len(re.findall(r"(?<!\\)\$", old)) % 2:
        problems.append(f"{label}: unbalanced $ in new text")
    text = text.replace(old, new)
out = text.encode("utf-8")
tags_before = raw.decode("utf-8").count("\\tag{")
tags_after = text.count("\\tag{")
print(f"{len(EDITS)} edits; report sha {h0[:12]}; size {len(raw)} -> {len(out)} bytes; tags {tags_before} -> {tags_after}")
if problems:
    print("PROBLEMS (nothing written):")
    for p in problems:
        print("  ", p)
    sys.exit(1)
if "--dry" in sys.argv:
    print("dry run OK; nothing written")
    sys.exit(0)
if hashlib.sha256(REPORT.read_bytes()).hexdigest() != h0:
    sys.exit("report changed after it was read; nothing written")
REPORT.write_bytes(out)
print("written; new sha", hashlib.sha256(out).hexdigest()[:12])
