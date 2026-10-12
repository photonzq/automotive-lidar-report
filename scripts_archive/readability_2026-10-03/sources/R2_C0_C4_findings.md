# Round 4 source findings: R2_C0_C4

Report checked: `automotive_perception_report_2026-09-27.md`. The strings were copied from the version with sha256 prefix 51d60fa27199. They were re-checked against b2dd35a90bdb, written by a concurrent editing pass while this file was being drafted, and the one edit whose text had moved (item 05, "Check against Waymo") was rebased on it. All 34 search strings below occur exactly once in b2dd35a90bdb and in the later 4e2afc5d7428 (script `sources/scripts/R2_check_old_strings.py`). Line numbers are given only as a reading aid.

PDFs were read by rendering pages to PNG at 160–200 dpi; `get_text()` was used only to locate pages.

---

## R2_C0_C4-01

- **Question:** What textbook or review values support $k\approx0.02$ (Si), $k\approx0.4$–0.5 (InGaAs/InP) and the practical gains of ≈50–200 (Si) and ≈10–20 (InGaAs) in the §C0 subsection 6 table and in §C4 item 2?
- **Answer:**
  - **Silicon.** Excelitas gives $k_{\rm eff}=0.02$ for its C30902 reach-through Si APD and a recommended operating gain of 150. The review by Martyniuk et al. puts the best commercial Si APDs at $k=0.01$–0.06, with gains of 20–400 across Si APDs. PerkinElmer's (now Excelitas) APD guide tabulates $k=0.02$, typical $M=150$ and $F=4.9$ for reach-through Si.
  - **InGaAs/InP.** Campbell et al. state that commercial InP/InGaAs APDs typically have $0.4\le k\le0.5$; Martyniuk et al. give $k=0.4$–0.5 for InP multiplication regions. Excelitas lists a maximum usable gain of 10 (minimum) to 20 (typical) for its C30645/C30662 InGaAs APDs; Martyniuk et al. give 10–40; the PerkinElmer guide tabulates $k=0.45$, $M=10$, $F=5.5$.
  - **Consistency check** with McIntyre's formula, Eq. (25) of the report, $F(M)=kM+(1-k)(2-1/M)$:
    - Si, $k=0.02$, $M=150$: $F=0.02\times150+0.98\times(2-1/150)=3.00+1.95=4.95$, the guide's 4.9.
    - InGaAs, $k=0.45$, $M=10$: $F=0.45\times10+0.55\times(2-0.1)=4.50+1.05=5.55$, the guide's 5.5 and the report's own table entry.
  - The report's ranges sit inside the sourced ones: 50–200 within 20–400 (typical 150) for Si, and 10–20 matching Excelitas's 10–20 usable gain for InGaAs.
  - The guide's prose says Si APDs "have k = 0.22", which contradicts its own Table 1 (0.02); the table value is the consistent one, as the $F$ check shows.
- **Source:**
  - Excelitas Technologies, *C30902EH and C30921EH Avalanche Photodiodes* datasheet, Rev. 2022.02, p. 3, Table 4 (recommended gain 150) and Note 3 ($k_{\rm eff}=0.02$). https://www.excelitas.com/file-download/download/public/91501?filename=C30902EH_Si_APD_Datasheet.pdf (full text).
  - Excelitas Technologies, *C30645 and C30662 Series, Large area InGaAs Avalanche Photodiodes* datasheet, Rev. 2024-04, p. 2, Tables 1–2 ("Maximum Useable Gain (M)": 10 minimum, 20 typical). https://www.excelitas.com/file-download/download/public/61766?filename=Excelitas_C30645_Series_InGaAs_APD_Datasheet.pdf (full text).
  - J. C. Campbell et al., "Recent Advances in Avalanche Photodiodes", *IEEE J. Sel. Top. Quantum Electron.* 10(4), 777–787 (2004), p. 3 (text beside Fig. 4). Author-group copy: https://coldren.ece.ucsb.edu/sites/default/files/publications/campbelljstqejuly04.pdf (full text).
  - P. Martyniuk et al., "Infrared avalanche photodiodes from bulk to 2D materials", *Light: Science & Applications* 12, 212 (2023), pp. 9–10 and Table 3. https://www.nature.com/articles/s41377-023-01259-3 (full text, open access).
  - PerkinElmer Optoelectronics, *Avalanche Photodiodes: A User's Guide* (2003), p. 6, Table 1, and p. 2. Copy hosted by UC Irvine: https://www.chem.uci.edu/~unicorn/243/papers/AvalanchePD.pdf (full text; the old Excelitas URL now redirects to a product page).
- **Evidence tag:** [P] for the datasheet values; [I] for the two reviews.
- **Confidence:** high; two independent reviews and the manufacturer's datasheets agree, and the tabulated $F$ values reproduce McIntyre's formula.
- **Proposed edit:** three changes (two table rows and the §C4 sentence).
  - `old` (§C0 subsection 6 table, L1690):
```text
| Silicon APD (905/940 nm) | ≈0.02 [U] | 2.9 at $M=50$; 4.0 at $M=100$ | ≈50–200 [U] |
```
  - `new`:
```text
| Silicon APD (905/940 nm) | ≈0.02 [P, Excelitas C30902EH datasheet; I: 0.01–0.06 for the best commercial Si APDs, Martyniuk et al. 2023] | 2.9 at $M=50$; 4.0 at $M=100$ | ≈50–200 [P: 150 recommended for the C30902EH; I: 20–400 across Si APDs, Martyniuk et al. 2023, Table 3] |
```
  - `old` (L1691):
```text
| InGaAs/InP APD (1,550 nm) | ≈0.4–0.5 [U] (§C4) | 5.5 at $M=10$; 10 at $M=20$ | ≈10–20 [U] (§C4) |
```
  - `new`:
```text
| InGaAs/InP APD (1,550 nm) | ≈0.4–0.5 [I, Campbell et al. 2004; Martyniuk et al. 2023] (§C4) | 5.5 at $M=10$; 10 at $M=20$ | ≈10–20 [P: maximum usable gain 10 minimum and 20 typical, Excelitas C30645/C30662 datasheet; I: 10–40, Martyniuk et al. 2023] (§C4) |
```
  - `old` (§C4 item 2, L3335):
```text
is $k\approx0.4$–0.5, against about 0.02 for Si. A large $k$ makes the avalanche noisy, which limits useful linear gain to about 10–20.
```
  - `new`:
```text
is $k\approx0.4$–0.5 [I, Campbell et al. 2004], against about 0.02 for Si [P, Excelitas C30902EH datasheet]. A large $k$ makes the avalanche noisy, which limits useful linear gain to about 10–20 [P, Excelitas C30645/C30662 datasheet].
```
- **Appendix 2 entry:**
  - Excelitas C30902EH Si APD datasheet ($k_{\rm eff}=0.02$, gain 150): https://www.excelitas.com/file-download/download/public/91501?filename=C30902EH_Si_APD_Datasheet.pdf
  - Excelitas C30645/C30662 InGaAs APD datasheet (usable gain 10–20): https://www.excelitas.com/file-download/download/public/61766?filename=Excelitas_C30645_Series_InGaAs_APD_Datasheet.pdf
  - Campbell et al., recent advances in APDs, *IEEE JSTQE* (2004): https://coldren.ece.ucsb.edu/sites/default/files/publications/campbelljstqejuly04.pdf
  - Martyniuk et al., infrared APDs review, *Light Sci. Appl.* (2023): https://www.nature.com/articles/s41377-023-01259-3

---

## R2_C0_C4-02

- **Question:** How are the VL53L5's 14 × 10 macro-pixels of 4 × 4 SPADs binned into its 8 × 8 output zones?
- **Answer:**
  - ST's own description of the device (Rae and Mellot, ISSW 2018, slides 5 and 11–14):
    - the array is 14 × 10 macro-pixels, each of 16 SPADs (4 × 4), with 40% fill factor behind microlenses;
    - it is deliberately oversized, so the active region can be placed to absorb build tolerances, and zone position moves "with macro-pixel resolution";
    - 16 parallel histogram channels read the array;
    - the default mode gives 4 × 4 ranging zones, each aggregating 2 × 2 macro-pixels (64 SPADs), plus an 8 × 8 signal map at one macro-pixel per cell;
    - the device is "capable of 64 zones at 15fps for both signal and distance".
  - Reconciliation [E]:
    - An 8 × 8 output uses an 8 × 8 block of macro-pixels (64 of the 140), one macro-pixel of 4 × 4 SPADs per zone; the 4 × 4 output uses the same block at 2 × 2 macro-pixels per zone.
    - With 16 histogram channels, 64 ranging zones need four groups of 16, consistent with 15 fps for 64 zones.
    - Bonanno's statement that zones are formed of "4 or more macro-pixels" fits the 4 × 4 mode only: 64 zones of at least 4 macro-pixels would need at least $64\times4=256$ macro-pixels, more than the 140 on the die.
  - Bonanno (2024, Table 1) confirms the die: 140 macro-pixels (14 × 10), 54 µm pitch per 4 × 4 macro-pixel, SPADs sharing a cathode and addressed by their anodes.
  - ST's datasheet could not be opened (st.com timed out); the frame-rate split between the two modes is therefore taken from ST's ISSW slides, not the datasheet.
- **Source:**
  - B. Rae and P. Mellot (STMicroelectronics), "A SPAD-Based, Direct Time-of-Flight, 64 Zone, 15fps, Parallel Ranging Device Based on 40nm CMOS SPAD Technology", International SPAD Sensor Workshop 2018, slides dated 27 Feb 2018, slides 5, 9, 11, 12 and 14. https://imagesensors.org/wp-content/uploads/2019/05/Bruce_Rae.pdf (full slide deck).
  - Bonanno (Yole), "Physical and Cost Comparison of Smartphone Laser Autofocus Solutions", ISSW 2024, p. 2 (§III.B) and p. 3, Table 1. https://www.imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R06.1.pdf (full text).
- **Evidence tag:** [P] for ST's architecture; [I] for the teardown; [E] for the mapping arithmetic.
- **Confidence:** medium-high; ST's slides describe the 2018 device that Bonanno's teardown matches (same 14 × 10 × 16 array), but the product datasheet was not read.
- **Proposed edit:**
  - `old` (§C1a chip table, L2485):
```text
VL53L5 14 × 10 macro-pixels [I]
```
  - `new`:
```text
VL53L5 14 × 10 macro-pixels of 4 × 4 SPADs, an oversized array from which an 8 × 8 block forms the 64 zones, one macro-pixel each, or 4 × 4 zones of 2 × 2 macro-pixels [I, Bonanno 2024; P, Rae and Mellot 2018]
```
  - `old` (optional, §B8 receiver note, L1406):
```text
(the VL53L5's 14 × 10)
```
  - `new`:
```text
(the VL53L5's 14 × 10 macro-pixels of 4 × 4 SPADs, of which an 8 × 8 block is read out as its zones [P, Rae and Mellot 2018])
```
- **Appendix 2 entry:**
  - Rae and Mellot (ST), 64-zone SPAD ranging device, ISSW 2018 slides: https://imagesensors.org/wp-content/uploads/2019/05/Bruce_Rae.pdf
  - Bonanno (Yole), smartphone laser-autofocus teardown and costing, ISSW 2024: https://www.imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R06.1.pdf

---

## R2_C0_C4-03

- **Question:** Do the 37.7 dB (retroreflector against the 5% target) and the 31.8 dB (against the 50% target) in Settembrini et al. (2026) come from different measurements or ranges?
- **Answer:**
  - Both come from the same single-acquisition row ($N_{\rm avg}=1$) of Extended Data Table 2, all targets at 7.2 m. The measured SNRs are 113,715 (retroreflector), 74.7 (50%), 31.2 (10%) and 19.4 (5%).
  - The two figures are ratios of these SNRs [E]:
    - $10\log_{10}(113{,}715/19.4)=10\log_{10}5{,}862=37.7$ dB;
    - $10\log_{10}(113{,}715/74.7)=10\log_{10}1{,}522=31.8$ dB.
  - Their 5.9 dB difference, $10\log_{10}(74.7/19.4)=5.9$ dB, is the measured SNR gap between the 50% and 5% targets, not the 10 dB of the reflectance ratio.
  - Why the gap is smaller (Methods, "LiDAR measurements"): the paper averages the target amplitude over all captures but excludes false returns that gave an incorrect distance. A weak target therefore keeps mostly its strong speckles. The 5% target was detected in only 17.0% of single acquisitions (50% target: 74.5%), so its averaged SNR is biased upward [E].
  - The gap widens toward 10 dB as detection improves. At $N_{\rm avg}=4$ the ratios are $10\log_{10}(433{,}565/41.7)=40.2$ dB and $10\log_{10}(433{,}565/264)=32.2$ dB, 8.0 dB apart, with 67.7% detection of the 5% target.
  - In reflectance terms the retroreflector is ≈42 dB above a 5% Lambertian return [E: 31.8 dB + $10\log_{10}(0.5/0.05)$ = 31.8 + 10.0 = 41.8 dB], taking the better-detected 50% target as reference.
  - The Peer Review File (MOESM1) gives no dB figure for the retroreflector, so both report values are derived from Extended Data Table 2.
  - Consequence for 10.7 "Measured at a lidar wavelength" [E]: $\rho_{\rm eq}$ depends on the reference target, 760 from the 50% target ($0.5\times113{,}715/74.7$) but 290–360 from the 5% and 10% targets. The 760 is the least biased value.
- **Source:** F. F. Settembrini, A. C. Gungor, A. Forrer, S. A. Fortune et al., "A large-scale coherent 4D imaging sensor", *Nature* (2026), doi:10.1038/s41586-026-10183-6.
  - Extended Data Table 2 ("Calibrated targets"): https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-10183-6/MediaObjects/41586_2026_10183_Tab2_ESM.jpg
  - Methods, "LiDAR measurements" section.
  - Read in full via the Europe PMC JATS text of PMC12979198, plus the Extended Data Table 2 image and the Peer Review File (MOESM1).
- **Evidence tag:** [P] (developers' own measurement) and [E] for the ratios.
- **Confidence:** high; the two dB values reproduce exactly from one table row.
- **Proposed edit:**
  - `old` (10.7, "What coherent detection changes", Evidence, L2320):
```text
saw no noticeable blooming from a retroreflector beside a 5% target at 7.2 m, although the retroreflector was 37.7 dB brighter [P].
```
  - `new`:
```text
saw no noticeable blooming from a retroreflector beside a 5% target at 7.2 m, although the retroreflector's measured SNR exceeded that target's by 37.7 dB in the same single acquisition [P, Extended Data Table 2; E: $10\log_{10}(113{,}715/19.4)=37.7$ dB]. The 31.8 dB of "Measured at a lidar wavelength" comes from the same row ($10\log_{10}(113{,}715/74.7)=31.8$ dB against the 50% target). The two differ by 5.9 dB rather than the 10 dB of the reflectance ratio because the paper averages SNR only over returns that gave the correct distance, which favours the strongest speckles of the 5% target, detected in only 17% of acquisitions [P, Methods; E]. Scaled by reflectance from the 50% target, the retroreflector is ≈42 dB above a 5% Lambertian return [E: $31.8+10.0=41.8$ dB].
```
  - `old` (consequential, §C7 status list, L4629):
```text
saw no noticeable blooming beside a retroreflector 37.7 dB brighter than a 5% target [P] (§C0 subsection 10.7).
```
  - `new`:
```text
saw no noticeable blooming beside a retroreflector whose measured SNR was 37.7 dB above that of a 5% target, ≈42 dB in reflectance terms [P/E] (§C0 subsection 10.7).
```
- **Appendix 2 entry:** none (Settembrini et al. 2026 is listed; Extended Data Table 2 belongs to the same article).

---

## R2_C0_C4-04

- **Question:** What integration time $T$ of one measurement (chirp duration) do Wang et al. (2025) use, and what transmitted power follows at $\eta=0.25$?
- **Answer:**
  - The experiment uses an FM triangular wave with a period of 36 µs and a 4.1 GHz modulation bandwidth, from a 100 kHz-linewidth laser (p. 8).
  - The paper's Eq. (1) writes the range beat as $f_R=(2R_{\max}/c)(2B/T)$, with $T$ the modulation period, so each ramp sweeps $B$ in $T/2$.
    - Check of their own example: $R_{\max}=250$ m, $B=5$ GHz, $T=36$ µs give $(500/3\times10^8)\times(10^{10}/36\times10^{-6})=463$ MHz, the 463 MHz they quote.
    - One up- or down-ramp, the span of one beat measurement, therefore lasts $T_{\rm ramp}=36/2=18$ µs.
  - Transmitted power [E], from the report's estimate $\eta P_{\rm tx}T\approx2\times10^{-7}$ J for an SNR of 10 at 200 m:
    - $T=18$ µs: $\eta P_{\rm tx}=2\times10^{-7}\ {\rm J}/(18\times10^{-6}\ {\rm s})=11$ mW, so $P_{\rm tx}=11/0.25=44$ mW.
    - If both ramps of a period were integrated ($T=36$ µs): $\eta P_{\rm tx}=5.6$ mW and $P_{\rm tx}=22$ mW.
  - The paper does not state the EDFA output or the power sent to the target (pp. 8–9), so "transmit power not published" in the 10.8 table stands. Its 1–2 mW LO per balanced photodiode (p. 8) is as the report states.
- **Source:** J. Wang et al. (SUSTech and RoboSense), "Integrated multi-functional silicon photonic engine for long-range FMCW laser ranging", *Moore and More* 2, 12 (2025), doi:10.1007/s44275-025-00030-7.
  - p. 2, Eq. (1) and the 463 MHz example;
  - p. 8, experimental setup (36 µs, 4.1 GHz, LO 1–2 mW);
  - p. 9, Fig. 7.
  - Full text read (open-access PDF from link.springer.com).
- **Evidence tag:** [P] for the period and sweep; [E] for the power.
- **Confidence:** high for $T$; medium for the power, which inherits the report's link-budget assumptions.
- **Proposed edit:**
  - `old` (10.8, "How the numbers are derived", Wang, L2369):
```text
For an assumed $T$ of 18–40 µs [E] that is $\eta P_{\rm tx}\approx$ 5–11 mW, i.e. 20–44 mW transmitted at the report's $\eta=0.25$.
```
  - `new`:
```text
The paper's triangular modulation has a period of 36 µs and a sweep of 4.1 GHz, and its beat frequency $(2R/c)(2B/T)$ puts each ramp at half the period [P], so one measurement integrates $T=18$ µs. Then $\eta P_{\rm tx}=2\times10^{-7}\ {\rm J}/18\ \mu{\rm s}\approx11$ mW, i.e. about 44 mW transmitted at the report's $\eta=0.25$, or 22 mW if both ramps of a period were integrated [E].
```
- **Appendix 2 entry:** Wang et al. (SUSTech and RoboSense), integrated FMCW photonic engine, *Moore and More* (2025): https://link.springer.com/article/10.1007/s44275-025-00030-7

---

## R2_C0_C4-05

- **Question:** Are Waymo's 50 (Piggott et al. 2025, Table 1) photons or photoelectrons?
- **Answer:**
  - They are photons. Table 1 lists "Photons per detection 50" beside a photodiode quantum efficiency of 90%. Section 3.2 and Fig. 8 work in photoelectrons and assume a shot-noise-limited receiver.
  - Three checks agree:
    - **QE conversion:** 50 photons × 0.9 = 45 photoelectrons.
    - **Their detection model** (Eqs. (31)–(34), an Erlang/Gamma sum of $n$ exponential speckle looks): $n=4$ at $P_{FA}=10^{-6}$ needs a threshold of $t=21.35$, and $P_D=0.9$ then needs $nN=44.9$ photoelectrons in total. The 4-speckle curve of Fig. 8(b) crosses 0.9 near 45 [E, script].
    - **Their link budget:** 0.52 µJ per shot at −106.1 dB gives $0.52\times10^{-6}\times10^{-10.61}/(1.282\times10^{-19}\ {\rm J})=99.6$ photons per shot, 49.8 per chirp at two chirps per point [E].
  - So 50 photons per chirp (detection) are 45 photoelectrons, which match the report's 44.9 at $10^{-6}$ per bin. The 10.8 table cell ("50 photons") is right; 10.3, §C7a(a) and §C7b subsection 2 should say 50 photons, i.e. 45 photoelectrons.
  - The "10–30 photoelectrons give only ≈50%" in §C7a(a) is Piggott's single-speckle statement (Fig. 8(a)), spanning false-alarm probabilities from $10^{-3}$ to $10^{-9}$.
  - In the §C7a "Check against Waymo" bullet, 45 photoelectrons give $E_{\rm pt}=1.21$ µJ per ramp at $\eta=0.25$ and 2.43 µJ for two ramps, 1.5–2.9× Waymo's 0.83–1.67 µJ. At Waymo's 3 dB case including its QE ($\eta=0.45$), two ramps need 1.35 µJ, inside the range; four receivers need 0.30 µJ per ramp. The bullet's conclusions therefore stand with slightly smaller numbers [E].
- **Source:** A. Y. Piggott et al. (Waymo), arXiv:2502.09736 (2025): p. 11 (§3.2), p. 12 (Fig. 8, Eqs. (31)–(34)), p. 13 (Table 1), p. 14 (§4.1). https://arxiv.org/pdf/2502.09736 (full text).
- **Evidence tag:** [P].
- **Confidence:** high; the table, the paper's own statistics and its link budget all give 50 photons = 45 photoelectrons.
- **Proposed edit:** four sentences, all with the same correction.
  - `old` (§C0 10.3, "Reading Figure C0.10b", L2018):
```text
Waymo's 50 photoelectrons for 90% detection with four averaged speckles at $10^{-6}$ per bin [P] matches one ramp searched in full,
```
  - `new`:
```text
Waymo's 50 photons per detection, 45 photoelectrons at its quantum efficiency of 0.9, for 90% detection with four averaged speckles at $10^{-6}$ per bin [P] match one ramp searched in full,
```
  - `old` (§C7a(a), L4764):
```text
Waymo's analysis uses **50 photoelectrons for 90% detection** with four averaged speckles at a $10^{-6}$ false-alarm probability per frequency bin, and finds that 10–30 photoelectrons give only ≈50% [P]. Waymo's 50 requires the peak in one ramp only:
```
  - `new`:
```text
Waymo's analysis uses **50 photons (45 photoelectrons at a quantum efficiency of 0.9) for 90% detection** with four averaged speckles at a $10^{-6}$ false-alarm probability per frequency bin, and finds that with a single speckle 10–30 photoelectrons give only ≈50%, depending on the false-alarm probability [P]. Waymo's 45 photoelectrons require the peak in one ramp only:
```
  - The §C7a(a) "Check against Waymo" bullet (L4767) was rewritten by a concurrent editing pass while this file was drafted. The five edits below are rebased on its current wording and recomputed with 45 photoelectrons [E, script]:
    - one ramp at $\eta=0.25$: $45\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=1.21$ µJ, two ramps 2.43 µJ, i.e. $2.43/1.67=1.5$ to $2.43/0.83=2.9$ times Waymo's 0.83–1.67 µJ;
    - at Waymo's 3 dB case, $\eta=0.5\times0.9=0.45$ including its quantum efficiency: two ramps 1.35 µJ, inside the range. This is the bullet's existing 1.35 µJ, which it reached with 50 at $\eta=0.5$; the numbers agree because 50 photons at 0.5 equal 45 photoelectrons at 0.45;
    - four receivers at once: $1.21/4=0.30$ µJ.
  - `old` (§C7a(a), "Check against Waymo", L4767):
```text
(12 Mpts/s, 250 m, 5%, 50 photoelectrons, 90% detection)
```
  - `new`:
```text
(12 Mpts/s, 250 m, 5%, 50 photons or 45 photoelectrons at a quantum efficiency of 0.9, 90% detection)
```
  - `old`:
```text
gives $50\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=1.35$ µJ for one ramp.
```
  - `new`:
```text
gives $45\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=1.21$ µJ for one ramp.
```
  - `old`:
```text
The like-for-like value is therefore $2\times1.35=2.7$ µJ at $\eta=0.25$, 1.6–3.3× Waymo's range, or 1.35 µJ at $\eta=0.5$, the efficiency of Waymo's 3 dB case, which lies inside it [E].
```
  - `new`:
```text
The like-for-like value is therefore $2\times1.21=2.4$ µJ at $\eta=0.25$, 1.5–2.9× Waymo's range, or 1.35 µJ at $\eta=0.45$, the efficiency of Waymo's 3 dB case including its quantum efficiency of 0.9, which lies inside it [E].
```
  - `old`:
```text
and its 50 is the total over the four acquisitions
```
  - `new`:
```text
and its 50 photons, 45 photoelectrons, are the total over the four acquisitions
```
  - `old`:
```text
which divides the energy for the same 50 photoelectrons by four, to $1.35/4\approx0.34$ µJ.
```
  - `new`:
```text
which divides the energy for the same 45 photoelectrons by four, to $1.21/4\approx0.30$ µJ.
```
  - `old` (§C7b subsection 2, "Counts needed", L4984):
```text
Waymo's 50 photoelectrons with four averaged speckles [P] is the corresponding one-ramp figure (≈47 by the same rule).
```
  - `new`:
```text
Waymo's 50 photons per detection with four averaged speckles, 45 photoelectrons at its quantum efficiency of 0.9 [P], are the corresponding one-ramp figure (≈47 by the same rule).
```
- **Appendix 2 entry:** none (Piggott et al. 2025 is listed).

---

## R2_C0_C4-06

- **Question:** What IEC 60825-1:2014 rule makes the Class 3B level the binding cap at 1,310 nm?
- **Answer:**
  - **The factor.** IEC 60825-1:2014 Table 9 defines the retinal factor $C_7$ as:
    - 1 over 700–1,150 nm;
    - $10^{0.018(\lambda-1150)}$ over 1,150–1,200 nm;
    - $8+10^{0.04(\lambda-1250)}$ over 1,200–1,400 nm.
  - The 2007 edition held $C_7$ at 8 over 1,200–1,400 nm. With $C_4=5$ over 1,050–1,400 nm (same table), the small-source Class 1 limit for long exposures is $3.9\times10^{-4}C_4C_7$ W. At 1,310 nm [E]:
    - $C_7=8+10^{0.04\times(1310-1250)}=8+10^{2.4}=8+251=259$;
    - AEL $=3.9\times10^{-4}\times5\times259=0.505$ W.
  - **The cap.** The Class 3B AEL over 1,050–1,400 nm is 0.5 W for emission longer than 0.25 s (Table 8). Seibersdorf's white paper on the 2014 edition states two things:
    - for Classes 1, 1M and 3R the accessible emission is limited to the Class 3B AEL over 1,250–1,400 nm, i.e. 0.5 W for CW;
    - for small sources the retinal Class 1 AEL reaches 0.5 W at 1,310 nm, so above 1,310 nm the Class 3B AEL is the limiting factor.
  - At 1,310 nm the two are equal to within 1% (0.505 against 0.5 W), so the cap binds from there on.
  - **Europe.** EN 60825-1:2014/A11:2021 adds a third, corneal limit derived from the skin MPE: 0.1 W for exposures of 0.35 s or more, through a 1 mm aperture growing to 3.5 mm at 10 s and beyond. It was introduced because the 500 mW Class 3B limit does not protect the cornea for small beams approaching 1,400 nm. In Europe, A11 is therefore the tighter limit at 1,310 nm for beams that fit the aperture.
  - Schulmeister's ILSC 2013 paper on the draft edition gives the same $C_7=259$ at 1,310 nm and the same Class 3B cap.
- **Source:**
  - K. Schulmeister, "The new edition of the international laser product safety standard IEC 60825-1", White paper, Seibersdorf Laboratories, Version 1d, 26 May 2017, p. 9. Live copy: https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/whitepaper_iec-60825-1.pdf (full text; same document as the archived v1d link in §C4c).
  - Seibersdorf Laboratories, *White Paper: A11 to EN 60825-1* (© 2022), §4, pp. 10–12. Live copy: https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/whitepaper_a11_to_en_60825-1.pdf (full text).
  - TCVN 12670-1:2020 (identical adoption of IEC 60825-1:2014), Table 9 ($C_4$, $C_7$) and Table 8 (Class 3B AEL), accessible text (link already in Appendix 2). The bodies of Tables 3–4 are not reproduced on that page, so the cap itself is taken from the Seibersdorf white paper.
  - K. Schulmeister, "The upcoming new editions of IEC 60825-1 and ANSI Z136.1", ILSC 2013, p. 5: https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/2013_ilsc_the_upcoming_new_editions_iec60825-1_ansi_z136-1_schulmeister.pdf (full text).
- **Evidence tag:** [P] for the standard's factors and Class 3B AEL; [I] for the Seibersdorf statement of the cap.
- **Confidence:** high; the standard's factors and the white paper give the same crossover at 1,310 nm.
- **Proposed edit:**
  - `old` (§C4c subsection 4, cold-caveat bullet, L3700):
```text
where eye safety is set by the Class 3B cap and, in Europe, by the A11 corneal limit for 1,250–1,400 nm (subsection 1); or bond InGaAs photodiodes to the PIC.
```
  - `new`:
```text
where the retinal factor $C_7=8+10^{0.04(\lambda-1250)}=259$ (with $C_4=5$) makes the small-source Class 1 retinal limit for long exposures $3.9\times10^{-4}C_4C_7=0.51$ W, so lenient that the binding limits become the 0.5 W cap at the Class 3B level, which IEC 60825-1:2014 imposes on Class 1 over 1,250–1,400 nm [P, Tables 8 and 9 via TCVN 12670-1:2020; I, Seibersdorf], and, in Europe, the A11 corneal limit for 1,250–1,400 nm, 0.1 W for exposures of 0.35 s or more [I, Seibersdorf] (subsection 1); or bond InGaAs photodiodes to the PIC.
```
- **Appendix 2 entry:** Seibersdorf Laboratories, white papers on IEC 60825-1:2014 (Class 3B cap above 1,310 nm) and on EN 60825-1 A11 (live copies): https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/whitepaper_iec-60825-1.pdf ; https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/whitepaper_a11_to_en_60825-1.pdf

---

## R2_C0_C4-07

- **Question:** Which figures behind the InP substrate prices conflict, and can they be attributed?
- **Answer:**
  - **Origin.** The series appears in BigGo Finance (25 Apr 2026), citing only "market data":
    - 2″ optical-communication-grade substrates rose from \$800 (early 2025) to \$2,300–2,500 (Apr 2026), with urgent spot orders above \$3,000;
    - "high-end" 6″ substrates rose from \$1,400 to \$5,000.
  - **The conflict** is inside that article. Its headline says prices "nearly double in a year", while its text says they are "nearly tripling" and gives a gain of "nearly 200%" for the 2″ wafer. The figures support the text: $2{,}300/800=2.9$ to $2{,}500/800=3.1$, i.e. +188% to +213% [E].
  - **The 6″ figure** is independently reported by Reuters (via MINING.COM, 11 Jun 2026): the average 6-inch InP wafer price "surged 250% to \$5,000" since China's export restrictions, implying a start near $5{,}000/3.5=\$1{,}430$ [E], consistent with \$1,400. The report's "(Jun 2026)" for 6″ matches the Reuters date.
  - **A second tension** [E]: in early 2025, a 6″ wafer (9× the area) at \$1,400 against a 2″ at \$800 implies 6″ substrate about 5× cheaper per mm² ($0.077$ against $0.39$ \$/mm²). The two figures may refer to different grades ("optical-communication-grade" 2″ against "high-end" 6″); neither source explains it.
- **Source:**
  - BigGo Finance editorial, "AI Computing Power Ignites 'Gold Material' Indium Phosphide: Prices Nearly Double in a Year, Supply-Demand Gap Exceeds 70%", 25 Apr 2026. https://finance.biggo.com/news/xsiIxJ0Bh5an-7GhIww3 (full text). Chinese reposts of the same series exist (Eastmoney, Huxiu); none names an original source.
  - Reuters, republished by MINING.COM, "China's control over indium phosphide exports threatens AI data centre rollout", 11 Jun 2026. https://www.mining.com/web/chinas-control-over-indium-phosphide-exports-threatens-ai-data-centre-rollout/ (full text read with a plain HTTP request; the fetch tool was refused).
- **Evidence tag:** [T].
- **Confidence:** medium; the numbers trace to an unattributed finance-site article, with the 6″ figure confirmed by Reuters.
- **Proposed edit:**
  - `old` (§C4c subsection 3 cost table, tag cell, L3621):
```text
| [T, unattributed; internally inconsistent] |
```
  - `new`:
```text
| [T: BigGo Finance, 25 Apr 2026, citing unnamed "market data"; its headline says prices "nearly double" in a year while its text has the 2″ price nearly tripling; the 6″ rise of 250% to \$5,000 also in Reuters, 11 Jun 2026] |
```
- **Appendix 2 entry:**
  - BigGo Finance, InP substrate prices (Apr 2026): https://finance.biggo.com/news/xsiIxJ0Bh5an-7GhIww3
  - Reuters via MINING.COM, InP export controls and the 6-inch price (Jun 2026): https://www.mining.com/web/chinas-control-over-indium-phosphide-exports-threatens-ai-data-centre-rollout/

---

## R2_C0_C4-08

- **Question:** In Duthon et al. (2019), which band is ≈10% worse in very dense advection fog?
- **Answer:**
  - It is the longer-wavelength band, 1,000–2,400 nm, which includes 1,550 nm. The paper says that 350–1,000 nm (which includes 905 nm) behaves the same in fog "regardless of fog density or type". Above 1,000 nm, for very dense fogs ($V<30$ m) and particularly advection fogs, fog has an impact about 10% higher for 1,000–2,400 nm than for visible wavelengths (400–800 nm). For light radiation fog ($V>100$ m) the impact above 1,000 nm is equal or lower.
  - The conclusion gives 905 and 1,550 nm "close extinction coefficients (systematically, a ratio between 1.0 and 1.1)" and a difference below 10%.
  - Fig. 9 (e.g. $V=15$–40 m) shows extinction rising from 905 toward 1,550 nm in dense fog.
  - The rewrite proposed in the item list ("905 nm ≈10% worse than 1,550 nm") would therefore reverse the finding: if either band is worse, it is 1,550 nm.
- **Source:** P. Duthon, M. Colomb and F. Bernardin, "Light Transmission in Fog: The Influence of Wavelength on the Extinction Coefficient", *Applied Sciences* 9(14), 2843 (2019), doi:10.3390/app9142843: §4 (p. 15), Fig. 9 (p. 14), §5 Discussion (p. 16), conclusions (p. 17). Full text (CC BY) from MDPI's file host: https://mdpi-res.com/d_attachment/applsci/applsci-09-02843/article_deploy/applsci-09-02843.pdf
- **Evidence tag:** [I].
- **Confidence:** high; the paper states the band and the condition explicitly.
- **Proposed edit:**
  - `old` (§C4c subsection 5 table, Fog row, L3716):
```text
| Fog | Extinction differs by <10% between 905 and 1,550 nm; near-IR ≈10% worse only in very dense advection fog (<30 m visibility) | [I, Duthon et al. 2019] |
```
  - `new`:
```text
| Fog | Extinction differs by <10% between 905 and 1,550 nm (a ratio of 1.0–1.1); light of 1,000–2,400 nm, including 1,550 nm, is ≈10% more attenuated than visible light, which 905 nm matches, only in very dense fog (<30 m visibility), especially advection fog | [I, Duthon et al. 2019] |
```
- **Appendix 2 entry:** Duthon, Colomb and Bernardin, fog extinction against wavelength, *Appl. Sci.* (2019): https://www.mdpi.com/2076-3417/9/14/2843

---

## R2_C0_C4-09

- **Question:** Is there a Seyond source for the Falcon K's 30 W?
- **Answer:**
  - Yes. The Falcon K1 user manual's specification table lists "Power: 12V/30W" (printed p. 9).
  - §3.2.1 states a consumption of about 30 W in regular operation and a peak of about 50 W at activation, lasting under a second (printed p. 31).
  - The same manual gives 1.75 kg, 900,000 points/s, 250 m at 10% under 100 klx with >90% detection, and 500 m maximum.
  - The §C4d "1.75 kg, 20–30 W" (K1 30 W, K2 20 W) therefore stands, as do §0 and §E11's "6–20 W".
  - Seyond's Chinese K3 page also gives 20 W for the Falcon K3 (item 13).
- **Source:** Seyond, *Falcon K1 LiDAR User Manual*, V2.1.2 (file dated 14 Mar 2024), Table 1 "Specifications" (printed p. 9, PDF p. 10) and §3.2.1 "Power description" (printed p. 31, PDF p. 32). https://www.seyond.com/wp-content/uploads/2024/12/Seyond-Falcon-K1-LiDAR_User-Manual_V2.1.2_EN_PublicRH_20240314.pdf (full text).
- **Evidence tag:** [P].
- **Confidence:** high; the manufacturer's manual states it twice.
- **Proposed edit:**
  - `old` (§C4 item 3, L3340):
```text
Seyond's Falcon K drew 30 W [U],
```
  - `new`:
```text
Seyond's Falcon K1 draws about 30 W in regular operation and about 50 W for under a second at start-up [P, user manual],
```
- **Appendix 2 entry:** Seyond Falcon K1 user manual V2.1.2 (30 W, 1.75 kg): https://www.seyond.com/wp-content/uploads/2024/12/Seyond-Falcon-K1-LiDAR_User-Manual_V2.1.2_EN_PublicRH_20240314.pdf

---

## R2_C0_C4-10

- **Question:** What source supports "front-side-illuminated SPADs reached only 2–5% PDE at 9xx nm", and how does it square with §C4b's "historically about 5–10% (front-side)" for SiPMs?
- **Answer:**
  - **SPADs.** Villa et al. (2021, Table 1) list photon detection probability at 905 nm for lidar SPAD arrays:
    - 2% for Beer et al. (2018, Fraunhofer IMS, 350 nm CMOS, fill factor 5.3%);
    - 5% for Zhang et al. (2019, 180 nm CMOS, fill factor 28%);
    - 7.5% and 5% for two early BSI designs (45/65 nm and 90/40 nm);
    - 22% for Sony's 2021 BSI chip.
  - Villa et al. define $\rm PDE=PDP\cdot FF$ (p. 15), so these are active-area values.
  - Beer et al. confirm theirs in the original: SPADs with a PDE of 2% at 905 nm in pixels of 5.32% fill factor.
  - Per pixel [E]:
    - Beer: $0.02\times0.0532=0.1\%$;
    - Zhang: $0.05\times0.28=1.4\%$.
  - The 2–5% is therefore right as a per-SPAD figure at 905 nm, and pixel-level PDE was lower still. Early BSI alone did not lift it (5–7.5%); light trapping and thick silicon did (Sony's 22–24%).
  - **SiPMs** are front-side devices too, but made in processes that set their own NIR response:
    - onsemi's blue-optimized J-Series falls to ≈2% at 900 nm at 6 V overvoltage (datasheet Fig. 1);
    - its NIR-enhanced automotive ArrayRDM-0112A20 is specified at 16% at 905 nm.
  - The §C4b "5–10%" lies inside that sourced 2–16% span, so the two statements do not conflict. The §C4b cell can be tied to the datasheet values, as in the optional edit.
- **Source:**
  - F. Villa et al., "SPADs and SiPMs Arrays for Long-Range High-Speed Light Detection and Ranging (LiDAR)", *Sensors* 21, 3839 (2021), Table 1 (p. 13) and p. 15. https://www.mdpi.com/1424-8220/21/11/3839 (full text; PDF from mdpi-res.com).
  - M. Beer, J. F. Haase, J. Ruskowski, R. Kokozinski, "Background Light Rejection in SPAD-Based LiDAR Sensors by Adaptive Photon Coincidence Detection", *Sensors* 18, 4338 (2018), §4. Full text via Europe PMC (PMC6308528); the MDPI PDF is served truncated.
  - onsemi, *J-Series SiPM Sensors* datasheet (MICROJ-SERIES/D, Rev. 5, Nov 2018), p. 3, Fig. 1. Distributor copy: https://www.farnell.com/datasheets/2704145.pdf (onsemi's own URL refused the request).
  - onsemi, *ARRAYRDM-0112A20-QFN* product overview (2024), "PDE of 16% at 905 nm". Copy: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6325/ARRAYRDM-0112A20-QFN.pdf
- **Evidence tag:** [I] (Beer et al., original) and [S] (Zhang et al. via Villa's review table); [P] for the onsemi datasheets.
- **Confidence:** high for the 2% (original); medium for the 5% (review table, original JSSC paper paywalled and not read).
- **Proposed edit:**
  - `old` (§C4 item 2, L3332):
```text
reached only 2–5% PDE at 9xx nm [U].
```
  - `new`:
```text
reached only 2–5% at 905 nm, counted over the SPAD's active area: 2% in Fraunhofer IMS's 0.35 µm lidar sensor and 5% in a 180 nm flash-lidar chip from EPFL and TU Delft, before pixel fill factors of 5% and 28% [I, Beer et al. 2018; S, Villa et al. 2021, Table 1].
```
  - `old` (optional reconciliation, §C4b "Other dimensions" table, SiPM PDE cell, L3457):
```text
Historically about 5–10% (front-side); NIR-enhanced automotive SiPMs are reported in the mid-to-high teens [U].
```
  - `new`:
```text
Front-side, and set by the process: about 2% at 900 nm for a blue-optimized SiPM (onsemi J-Series, 6 V overvoltage) against 16% at 905 nm for onsemi's NIR-enhanced automotive ArrayRDM-0112A20 [P, datasheets].
```
- **Appendix 2 entry:**
  - Beer et al., Fraunhofer IMS SPAD lidar sensor (2% PDE at 905 nm), *Sensors* (2018): https://pmc.ncbi.nlm.nih.gov/articles/PMC6308528/
  - onsemi ArrayRDM-0112A20 (16% PDE at 905 nm): https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6325/ARRAYRDM-0112A20-QFN.pdf
  - onsemi J-Series SiPM datasheet: https://www.farnell.com/datasheets/2704145.pdf
  - Villa et al. 2021 is already listed.

---

## R2_C0_C4-11

- **Question:** Which links are missing from the §C4c Sources line, and are the unlabelled ones what the report assumes?
- **Answer:**

| Report item | Finding | Link |
|---|---|---|
| GlobalFoundries Ge photodiode, OFC 2025 | Bian et al. (GlobalFoundries, with Ranovus), OFC 2025 Th3E.6: ~60 GHz, 0.95 A/W (O-band), <30 nA, −36 dB ORL | https://opg.optica.org/abstract.cfm?URI=OFC-2025-Th3E.6 |
| Chen et al., JAP 2016 | It is the unlabelled pub_3746: H. Chen et al. (imec and Ghent University), "Dark current analysis in high-speed germanium p-i-n waveguide photodetectors", *J. Appl. Phys.* 119, 213105 (2016), author copy | https://www.photonics.intec.ugent.be/download/pub_3746.pdf ; doi:10.1063/1.4953147 |
| Hale & Querry | G. M. Hale and M. R. Querry, *Appl. Opt.* 12, 555 (1973) | https://doi.org/10.1364/AO.12.000555 |
| Kou | L. Kou, D. Labrie and P. Chylek, *Appl. Opt.* 32, 3531 (1993) | https://doi.org/10.1364/AO.32.003531 |
| Artilux Ge-on-Si SPAD | N. Na et al., "Room temperature operation of germanium–silicon single-photon avalanche diode", *Nature* 627, 295 (2024). The report's 19 kcps/µm² and 12% at 1,310 nm are relayed in the Na et al. review (next row) | https://doi.org/10.1038/s41586-024-07076-x |
| arXiv 2605.07343 (assumed Fudan/Zhangjiang/Innolight) | **Not that paper.** It is N. Na (Artilux), E. Chen, G. S. Buller, R. H. Hadfield and R. A. Soref, "Review of germanium-silicon single-photon avalanche diodes", Proc. SPIE 13448, 1344808 (2025). It is the source of the Artilux values (p. 7) and of Vines et al.'s 38% at 125 K (p. 6) | https://arxiv.org/pdf/2605.07343 |
| Fudan / Zhangjiang Lab / Innolight, ultra-thin Ge | X. Wang (Fudan University and Zhangjiang Laboratory) et al., with Innolight Technology Research Institute co-authors, "100 GHz Ultra-thin Germanium Photodetector with 1.05 A/W Responsivity at 1550 nm", OFC 2025 M4K.2. Abstract: up to 100 GHz, >0.8 A/W in the C-band, <20 nA | https://opg.optica.org/abstract.cfm?uri=OFC-2025-M4K.2 |
| Rogers et al., *Nature* 2021 | arXiv 2008.02411 is confirmed as its preprint ("A universal 3D imaging sensor on a silicon photonics platform") | https://arxiv.org/pdf/2008.02411 |
| Hamamatsu G8931-20 price [T] | Only a search extract of an Indian distributor listing (₹60,500 per unit, ≈\$700 at ₹86–88 per dollar) was found; the page refused repeated requests (HTTP 429). No source for the ≈\$113 Si APD price was found | https://www.indiamart.com/proddetail/hamamatsu-ingaas-apd-23931342712.html |
| SiLC "germanium detectors" [T] | Embedded.com: laser, SOA, "germanium detectors" and optical circuits integrated on SiLC's chip (SiLC's own Business Wire release of 7 Dec 2021 refused the request) | https://www.embedded.com/chip-integrated-fmcw-lidar-sensors-deliver-coherent-3d-vision/ |
| s41467-019-08830-w | Confirmed: P. Vines et al., "High performance planar germanium-on-silicon single-photon avalanche diode detectors", *Nat. Commun.* 10, 1086 (2019) | as in the report |
| PMC12113715 | Confirmed: J. Liu et al., "Low Temperature Characteristics of Ge-on-Si Waveguide Photodetectors: A Combined Simulation and Experimental Study", *Micromachines* 16, 542 (2025) | as in the report |
| arXiv 2112.08936 | Confirmed as a survey relaying Wojtanowski: Y. Zhang, A. Carballo, H. Yang and K. Takeda, *ISPRS J. Photogramm. Remote Sens.* 196, 146 (2023). p. 37 relays that 905 nm reaches twice as far as 1,550 nm at 25 mm/h | as in the report |
| photonics.intec.ugent.be pub_3746 | Chen et al., JAP 2016 (see above) | as in the report |
| IEC webstore 62424 | "IEC 60825:2026 SER", the IEC 60825 series bundle published 10 Jul 2026. It lists IEC 60825-1:2014 as the current Part 1 and contains TS 60825-13:2026, TS 60825-19:2024 and TS 60825-20:2025 | as in the report |

- **Source:** the publisher pages and PDFs in the table. Titles and authors come from arXiv abstract pages, Europe PMC, Crossref (queried with no email or mailto parameter), Optica abstract pages and the documents themselves. Full text was read for the Na et al. review, the Zhang et al. survey, the Chen et al. author copy and the IEC series page.
- **Evidence tag:** [P] (IEC page, OFC papers' own abstracts); [I] (journal papers); [T] (Embedded.com); [S] (the G8931-20 price, search extract only).
- **Confidence:** high for the identifications; low for the G8931-20 price pair.
- **Proposed edit:** five label edits on the §C4c Sources line (L3732), one appended list of links, and one tag change for the price sentence.
  - `old`:
```text
https://webstore.iec.ch/en/publication/62424 ;
```
  - `new`:
```text
https://webstore.iec.ch/en/publication/62424 (IEC 60825:2026 series, listing IEC 60825-1:2014 as the current Part 1 and TS 60825-13:2026) ;
```
  - `old`:
```text
https://www.nature.com/articles/s41467-019-08830-w ;
```
  - `new`:
```text
https://www.nature.com/articles/s41467-019-08830-w (Vines et al., Nature Communications 2019) ;
```
  - `old`:
```text
https://arxiv.org/pdf/2605.07343 ;
```
  - `new`:
```text
https://arxiv.org/pdf/2605.07343 (Na et al., review of germanium-silicon SPADs, Proc. SPIE 13448, 2025, for the Artilux and Vines et al. devices) ;
```
  - `old`:
```text
https://www.photonics.intec.ugent.be/download/pub_3746.pdf ;
```
  - `new`:
```text
https://www.photonics.intec.ugent.be/download/pub_3746.pdf (Chen et al., Journal of Applied Physics 2016, author copy) ;
```
  - `old`:
```text
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12113715/ ; https://arxiv.org/pdf/2008.02411 ;
```
  - `new`:
```text
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12113715/ (Liu et al., Micromachines 2025) ; https://arxiv.org/pdf/2008.02411 (Rogers et al., Nature 2021, preprint) ;
```
  - `old` (the last entry of the line):
```text
https://arxiv.org/pdf/2112.08936
```
  - `new`:
```text
https://arxiv.org/pdf/2112.08936 (Zhang et al., adverse-weather survey, ISPRS 2023, relaying Wojtanowski et al. 2014) ; https://opg.optica.org/abstract.cfm?URI=OFC-2025-Th3E.6 (GlobalFoundries Ge photodiode, OFC 2025) ; https://opg.optica.org/abstract.cfm?uri=OFC-2025-M4K.2 (Fudan University, Zhangjiang Laboratory and Innolight ultra-thin Ge photodiode, OFC 2025) ; https://doi.org/10.1364/AO.12.000555 (Hale and Querry 1973) ; https://doi.org/10.1364/AO.32.003531 (Kou, Labrie and Chylek 1993) ; https://doi.org/10.1038/s41586-024-07076-x (Na et al., Artilux room-temperature Ge-Si SPAD, Nature 2024) ; https://www.embedded.com/chip-integrated-fmcw-lidar-sensors-deliver-coherent-3d-vision/ (SiLC germanium detectors, trade press) ; https://www.indiamart.com/proddetail/hamamatsu-ingaas-apd-23931342712.html (G8931-20 distributor listing)
```
  - `old` (§C4c subsection 3, price sentence):
```text
a Hamamatsu G8931-20 InGaAs APD sells for ≈\$700 against ≈\$113 for a comparable Si APD [T].
```
  - `new`:
```text
a Hamamatsu G8931-20 InGaAs APD sells for ≈\$700 (₹60,500 in an Indian distributor listing [S, search extract]) against ≈\$113 for a comparable Si APD [U].
```
- **Appendix 2 entry:**
  - Na et al., review of germanium-silicon SPADs, Proc. SPIE 13448 (2025): https://arxiv.org/pdf/2605.07343
  - Na et al., room-temperature Ge-Si SPAD (Artilux), *Nature* (2024): https://doi.org/10.1038/s41586-024-07076-x
  - Bian et al. (GlobalFoundries), Ge-on-Si PIN photodiodes, OFC 2025 Th3E.6: https://opg.optica.org/abstract.cfm?URI=OFC-2025-Th3E.6
  - Wang et al. (Fudan University, Zhangjiang Laboratory, Innolight), ultra-thin Ge photodiode, OFC 2025 M4K.2: https://opg.optica.org/abstract.cfm?uri=OFC-2025-M4K.2
  - Chen et al., Ge p-i-n dark current, *J. Appl. Phys.* (2016), author copy: https://www.photonics.intec.ugent.be/download/pub_3746.pdf
  - Hale and Querry, optical constants of water (1973): https://doi.org/10.1364/AO.12.000555
  - Kou, Labrie and Chylek, refractive indices of water and ice (1993): https://doi.org/10.1364/AO.32.003531

---

## R2_C0_C4-12

- **Question:** What URLs support §C4 item 7 (the KrASIA summary, the Yole view and the RoboSense M3 pitch), and does each source say what the report attributes to it?
- **Answer:**
  - **KrASIA.** The article is a translation of a 36Kr piece by Song Wanxin, published on KrASIA on 22 Oct 2025.
    - It says Seyond's 1,550 nm route "is two to three times more expensive" than the 905 nm technology of Hesai and RoboSense.
    - The article discusses Seyond's prospectus (revenue concentration, unit prices), but it gives the 2–3× as its own statement, not as a prospectus figure. "Summarising Seyond's prospectus" therefore over-attributes it.
  - **Yole.** Yole's *Automotive LiDAR 2025* report page could not be read (the site returns an empty bot-protection response), so the report's wording is not verifiable there.
    - Yole's readable *Automotive LiDAR 2023* conference deck (P. Boulay, 3–5 Oct 2023), slide 26, says fibre-laser penetration "is linked to one LiDAR player" and is not expected to last "due to its high cost".
    - Slide 13 of the same deck counts 1,550 nm in 8% of 144 passenger-car design wins against 89% for 905 nm.
  - **RoboSense.** RoboSense's own CES 2024 release (9 Jan 2024) says the M3 (940 nm) "costs 50-70% less" than 1,550 nm lidar, is 50% smaller and draws >30% less power, with 300 m at 10%.
  - The Sources line below also carries the K1 manual (item 09), the K3 page (item 13) and the detector sources of items 01 and 10, all of which support §C4 text.
- **Source:**
  - Song Wanxin (36Kr), "LiDAR maker Seyond pursues SPAC listing after losing ground to rivals", KrASIA, 22 Oct 2025, paragraphs 3 and 7. https://kr-asia.com/lidar-maker-seyond-pursues-spac-listing-after-losing-ground-to-rivals (full text).
  - P. Boulay (Yole Intelligence), "Automotive LIDAR Market: Competitive Dynamics, Technology Evolution, and Revenue Trends", Automotive LiDAR conference, 3–5 Oct 2023, slides 13 and 26. https://medias.yolegroup.com/uploads/2023/12/automotive-lidar_boulay_yole_intelligence_v2.pdf (full deck).
  - RoboSense, "RoboSense Announces New M Platform LiDAR Sensors at CES 2024", Detroit, 9 Jan 2024. https://en.prnasia.com/releases/global/robosense-announces-new-m-platform-lidar-sensors-at-ces-2024-433294.shtml (full text).
- **Evidence tag:** [T] (KrASIA); [MR] (Yole); [P] (RoboSense).
- **Confidence:** high that each source says what is quoted; the Yole 2025 wording remains unverified.
- **Proposed edit:**
  - `old` (§C4 item 7, L3354):
```text
- KrASIA, summarising Seyond's prospectus: the InGaAs route costs **2–3×** as much as 905 nm [T].
```
  - `new`:
```text
- KrASIA, in a 36Kr article of 22 Oct 2025 on Seyond's listing prospectus, puts the InGaAs route at **2–3×** the cost of 905 nm; the article gives the figure as its own, not as a prospectus figure [T].
```
  - `old` (L3355):
```text
- Yole: 1,550 nm cost is hard to reconcile with OEM (carmaker) targets [MR/S].
```
  - `new`:
```text
- Yole ties fibre-laser (1,550 nm) penetration to one lidar maker and does not expect it to last because of its high cost; 1,550 nm accounted for 8% of passenger-car lidar design wins since 2018, against 89% for 905 nm [MR, Yole Automotive LiDAR 2023 conference, slides 13 and 26].
```
  - `old` (a new Sources line at the end of §C4, after the "Where 1,550 nm survives" paragraph, L3358):
```text
Separately, 1,550 nm is the natural band for FMCW (frequency-modulated continuous-wave, coherent) lidar (§C4c subsection 6).
```
  - `new`:
```text
Separately, 1,550 nm is the natural band for FMCW (frequency-modulated continuous-wave, coherent) lidar (§C4c subsection 6).

Sources: https://kr-asia.com/lidar-maker-seyond-pursues-spac-listing-after-losing-ground-to-rivals (KrASIA, 36Kr article on Seyond, 22 Oct 2025) ; https://medias.yolegroup.com/uploads/2023/12/automotive-lidar_boulay_yole_intelligence_v2.pdf (Yole, Automotive LiDAR 2023 conference) ; https://en.prnasia.com/releases/global/robosense-announces-new-m-platform-lidar-sensors-at-ces-2024-433294.shtml (RoboSense M3 at CES 2024) ; https://www.seyond.com/wp-content/uploads/2024/12/Seyond-Falcon-K1-LiDAR_User-Manual_V2.1.2_EN_PublicRH_20240314.pdf (Seyond Falcon K1 user manual) ; https://www.seyond.cn/falcon-k3-2/ (Seyond Falcon K3 product page) ; https://www.excelitas.com/file-download/download/public/91501?filename=C30902EH_Si_APD_Datasheet.pdf (Excelitas C30902EH Si APD) ; https://www.excelitas.com/file-download/download/public/61766?filename=Excelitas_C30645_Series_InGaAs_APD_Datasheet.pdf (Excelitas C30645/C30662 InGaAs APD) ; https://coldren.ece.ucsb.edu/sites/default/files/publications/campbelljstqejuly04.pdf (Campbell et al., IEEE JSTQE 2004) ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6308528/ (Beer et al., Sensors 2018) ; https://www.mdpi.com/1424-8220/21/11/3839 (Villa et al., Sensors 2021)
```
- **Appendix 2 entry:**
  - KrASIA (36Kr), Seyond's SPAC listing and the 1,550 nm cost (Oct 2025): https://kr-asia.com/lidar-maker-seyond-pursues-spac-listing-after-losing-ground-to-rivals
  - Yole, Automotive LiDAR 2023 conference deck (wavelength and light-source shares): https://medias.yolegroup.com/uploads/2023/12/automotive-lidar_boulay_yole_intelligence_v2.pdf
  - RoboSense M3 at CES 2024 (940 nm, 50–70% cheaper than 1,550 nm): https://en.prnasia.com/releases/global/robosense-announces-new-m-platform-lidar-sensors-at-ces-2024-433294.shtml

---

## R2_C0_C4-13

- **Question:** Is there a Seyond source for the Falcon K3's 450 m at 10%?
- **Answer:**
  - Yes. Seyond's Chinese product page calls the 猎鹰K3 (Falcon K3) its third-generation ultra-long-range lidar, with a detection range of "最远900m (450m@10%)", i.e. 900 m maximum and 450 m at 10%.
  - Its other specifications: 120° × 20° field of view; 0.05° × 0.04° ROI resolution; 500 lines; 1,550 nm, Class 1; 20 W; detection of 20 × 30 cm objects at 250 m; 50% smaller than the second generation.
  - The page states no ambient-light condition or detection probability for the 450 m.
  - Seyond's English Falcon K page lists only the K/K1 (250 m at 10%).
  - The report's "at NIO" placement of the K3 was not checked here; Seyond's Gasgoo award declaration (25 Jul 2026) names NIO's NT2.0 and NT3.0 platforms for the Falcon family without naming the K3.
- **Source:** Seyond (图达通), "猎鹰K3 第三代超远距激光雷达" product page, https://www.seyond.cn/falcon-k3-2/ (full page read, footer © 2025; accessed 5 Oct 2026).
- **Evidence tag:** [P].
- **Confidence:** high for the figure; its test conditions are unstated.
- **Proposed edit:**
  - `old` (§C4, "Where 1,550 nm survives", L3358):
```text
at NIO (Seyond Falcon K3, 450 m at 10%, §C3)
```
  - `new`:
```text
at NIO (Seyond Falcon K3, 450 m at 10% and 900 m maximum, conditions unstated [P, product page], §C3)
```
- **Appendix 2 entry:** Seyond Falcon K3 product page (Chinese; 900 m maximum, 450 m at 10%, 20 W): https://www.seyond.cn/falcon-k3-2/

---

## R2_C0_C4-14

- **Question:** Is there a source for the Hesai ATX being the best-selling long-range lidar?
- **Answer:**
  - Hesai itself makes the claim. Its release of 20 May 2026 calls the ATX "currently the best-selling long-range lidar in the ADAS segment", with over 1 million units delivered and an order backlog above 6 million.
  - The same release cites Yole for Hesai's company-level rank: No. 1 in long-range ADAS lidar shipments in 2025, with 43%.
  - No independent model-level ranking was found. Huawei's more than one million lidars shipped by July 2025 (§E11.2) are cumulative across several models, so they neither confirm nor refute a per-model rank.
- **Source:** Hesai Group, "Hesai Secures Design Win from Another Top European OEM, Adding 1 Million-Unit Order", PR Newswire, Stuttgart, 20 May 2026, paragraphs on ATX and Yole. https://www.prnewswire.com/news-releases/hesai-secures-design-win-from-another-top-european-oem-adding-1-million-unit-order-302777712.html (full text).
- **Evidence tag:** [P] (company claim; not independent).
- **Confidence:** high that Hesai claims it; low that it is independently established.
- **Proposed edit:**
  - `old` (§C4b "Where each wins", L3471):
```text
**Hesai's ATX, by its delivery count the best-selling long-range lidar [U], uses SiPM** (more than 1 M delivered, §C3; ≈\$200 [T], §C3c).
```
  - `new`:
```text
**Hesai's ATX, the best-selling long-range ADAS lidar by Hesai's own account [P], uses SiPM** (more than 1 M delivered, §C3; ≈\$200 [T], §C3c). No independent model-level ranking was found; Huawei's more than 1 M lidars by July 2025 span several models (§E11.2).
```
- **Appendix 2 entry:** Hesai, ATX "best-selling long-range lidar in the ADAS segment" and the Yole 43% share (May 2026): https://www.prnewswire.com/news-releases/hesai-secures-design-win-from-another-top-european-oem-adding-1-million-unit-order-302777712.html

---

## Access notes

- **Bot protection, not bypassed.** Springer's client challenge cleared with ordinary cookie handling (the open-access PDF); no challenge was solved.
- **Refused or rate-limited** (the item was answered from other copies): MDPI page HTML (used mdpi-res.com and Europe PMC), Yole's report pages (empty bot-protection reply), Business Wire (403), IndiaMART (429), st.com (timeout), SCMP (403).
- **Wayback Machine** returned 429 during this session; live Seibersdorf copies were used instead.
- **Privacy.** No email address was sent in any request.
