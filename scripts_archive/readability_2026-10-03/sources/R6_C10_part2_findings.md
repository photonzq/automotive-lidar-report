# Round 4 source findings: R6_C10_part2

Read on 5 Oct 2026, against the report file whose SHA-256 begins 51d60fa27199; re-checked against the later version whose SHA-256 begins 803514977999. Every `old` string below occurs exactly once in both versions (check script `scripts/R6_check_old_strings.py`). Line numbers are a guide only. Equation numbers in the `new` strings follow the current numbering: the mode-area–footprint identity is Eq. (140) in §C10.3a item 4, and the mode-equivalent area is Eq. (33) of §C0.

---

## R6_C10_part2-01

- **Question:** What nominal footprint fraction does Pointcloud's coherent FPA actually have, so that the quoted mode-equivalent diameter (≈6 mm) follows from a source, and why does the quoted 23° × 14° field exceed $352\times176\times0.061^\circ$?
- **Answer:** The ≈2% is not in the paper; it was an assumption. The paper gives the following, and the footprint fraction follows from it.
  - **Which beam was measured.** The only measured beam is behind a 25 mm test lens (VS-2514H1-SWIR) "in a focusing configuration at around 11–12 m". With the on-chip microlens it has a 1/e² waist $w_0=1.31$ mm located 11.1 m from the FPA and a Rayleigh range $z_R=4.1$ m; without the microlens, 1.53 mm at 12.5 m and $z_R=5.6$ m. The camera measurement spans 10–16 m (Methods, "System imaging properties"; Extended Data Fig. 2c). The 65 m building scene used the 50 mm lens, for which no beam size is published. The SNR-versus-distance check on cardboard (≈3.5–21.5 m, Extended Data Fig. 4c) also uses the 25 mm lens's beam.
  - **Address pitch** $\theta_{\rm cell}=2\tan^{-1}(p/2f)$ with pixel pitch $p=53$ µm: 0.1215° ($2.12\times10^{-3}$ rad) for $f=25$ mm (measured minimum 0.11°), and 0.0607° ($1.06\times10^{-3}$ rad) for $f=50$ mm (measured 0.06°) (Extended Data Fig. 3d).
  - **Why the field exceeds pixels × pitch.** The measured 50 mm-lens field is 23.11° × 13.55° (theory 23.40° × 13.73°; 44.44° × 26.65° for 25 mm). It exceeds $352\times176\times0.0607^\circ=21.4^\circ\times10.7^\circ$ because the active area includes "the spaces between pixel blocks that are used for electronic and photonic routing", which the paper gives as the cause of the gaps in its point clouds. From $\mathrm{FOV}=2\tan^{-1}(s/2f)$ the theoretical field implies an array of $s=20.7\ {\rm mm}\times12.0$ mm (Extended Data Fig. 2a spans about ±10.4 mm × ±6 mm), against $18.7\times9.3$ mm of pixels alone. The pixel addresses cover 73% of the field ($21.4\times10.7/(23.11\times13.55)$). The 23° × 14° field in the report is therefore right, but a per-address bound should use the pitch, not field ÷ pixel count (which spreads the gaps over the cells).
  - **Derivation.** Beam radius $w(R)=w_0\sqrt{1+[(R-R_w)/z_R]^2}$ with $w_0=1.31$ mm, $R_w=11.1$ m and $z_R=4.1$ m; check $\pi w_0^2/\lambda=\pi(1.31\ {\rm mm})^2/1.31\ \mu{\rm m}=4.115$ m. Footprint fraction $f_{\rm fp}=\pi w^2/(R\theta_{\rm cell})^2$. Mode-equivalent area from the report's Eq. (33) with $t=1$, as §C0 subsection 10.8 does for this array: $A_{\rm mode}=\lambda^2R^2/(2\pi w^2)$, so that $A_{\rm mode}f_{\rm fp}=\tfrac12(\lambda/\theta_{\rm cell})^2=0.191$ mm² on the 25 mm grid.

    | Range | $w$ | Cell ($R\theta_{\rm cell}$, 25 mm lens) | $f_{\rm fp}$ | $A_{\rm mode}$ (equivalent diameter) |
    |---|---|---|---|---|
    | 4 m | 2.62 mm | 8.5 mm | 30% | 0.64 mm² (0.90 mm) |
    | 7.2 m | 1.81 mm | 15.3 mm | 4.4% | 4.3 mm² (2.35 mm) |
    | 11.1 m (waist) | 1.31 mm | 23.5 mm | 0.97% | 19.6 mm² (5.0 mm) |
    | 12.6 m (minimum $f_{\rm fp}$) | 1.39 mm | 26.7 mm | 0.86% | 22.3 mm² (5.3 mm) |
    | 22 m | 3.72 mm | 46.6 mm | 2.0% | 9.6 mm² (3.5 mm) |
    | 65 m (extrapolated beyond the measured 10–16 m) | 17.3 mm | 137.8 mm | 4.9% | 3.9 mm² (2.2 mm) |

    Worked at 11.1 m: $f_{\rm fp}=\pi(1.31\ {\rm mm})^2/(11.1\ {\rm m}\times2.12\times10^{-3})^2=5.39\ {\rm mm^2}/(23.5\ {\rm mm})^2=0.97\%$, and $A_{\rm mode}=(1.31\ \mu{\rm m}\times11.1\ {\rm m})^2/[2\pi(1.31\ {\rm mm})^2]=19.6$ mm², an equivalent diameter $2\sqrt{19.6/\pi}=5.0$ mm.
  - **The reviewer's 4% and 20%.** They are reproduced (3.9% at 11.1 m, 19.7% at 65 m) only by putting the 25 mm-lens beam on the 50 mm-lens grid, a combination that was not measured. $A_{\rm mode}$ itself does not depend on the grid.
  - **Where the ≈6 mm came from.** It follows from Eq. (140) at the assumed $f_{\rm fp}=0.02$ on the 0.061° grid: $0.64/0.02=32$ mm², or 6.4 mm (pitch-based), and $0.45/0.02=23$ mm², or 5.4 mm (field-based). On the measured beam's own grid, $f_{\rm fp}=2\%$ occurs at 22 m and gives 3.5 mm. The largest $A_{\rm mode}$ the measured beam reaches is 22 mm² (5.3 mm), near 12.6 m.
  - **Full-coverage bound** ($f_{\rm fp}=1$). For the 50 mm lens it is $\tfrac{t^2}{2}(\lambda/\theta_{\rm cell})^2=0.42\times(1.31\ \mu{\rm m}/1.06\times10^{-3})^2=0.64$ mm², or 0.90 mm; with the ½ factor alone it is 0.76 mm² (0.99 mm). Spread over the measured 23.11° × 13.55° field it is 0.47 mm² (0.77 mm). For the 25 mm lens it is 0.16 mm² (0.45 mm).
- **Source:** F. F. Settembrini, A. C. Gungor, A. Forrer, S. A. Fortune *et al.* (Pointcloud GmbH), "A large-scale coherent 4D imaging sensor", *Nature* 651, 364–370 (2026), https://doi.org/10.1038/s41586-026-10183-6 (open access).
  - Main text and Methods read in full from the Europe PMC full-text XML of PMC12979198 ("System imaging properties", "SNR model"). The nature.com and PMC pages served bot challenges and were not used.
  - Extended Data Figs 2 (a, c), 3 (d) and 4 (c) and Extended Data Table 1 read as the publisher's figure images on static-content.springer.com (MediaObjects 41586_2026_10183_Fig6_ESM, Fig7_ESM, Fig8_ESM and Tab1_ESM).
  - Calculation: `scripts/R6_pointcloud_footprint.py`.
- **Evidence tag:** [P] for the measured beam, pitches and fields; [E] for the footprint fractions and mode areas derived from them.
- **Confidence:** high for the measured inputs and the arithmetic; medium for anything stated about the 50 mm configuration, because no beam was published for that lens.
- **Proposed edit:** the same figure appears in three places, and all three need the edit.
  - (a) §C10.3a, item 5, bite (b), Pointcloud bullet. `old`:
    ```text
    Pointcloud's 61,952-pixel focal-plane array (FPA, §C10.4) could fill its field only with a mode-equivalent collecting diameter of ≈0.8 mm. At an assumed nominal footprint fraction of ≈2%, the identity allows ≈6 mm. [E: the bound is the identity Eq. (140), derived in item 4, with $f_{\rm fp}\le1$ and a cell solid angle $\theta_{\rm cell}^2=\Omega_{\rm FOV}/N_{\rm cell}$, where $N_{\rm cell}=61{,}952$ is the number of pixels and $\Omega_{\rm FOV}$ the 23° × 14° field: $A_{\rm mode}\lesssim\tfrac{t^2}{2}N_{\rm cell}\lambda^2/\Omega_{\rm FOV}=0.42\times61{,}952\times(1.31\ \mu{\rm m})^2/[(23^\circ\times14^\circ)(\pi/180)^2]=0.42\times61{,}952\times1.72\times10^{-12}/0.098=0.45$ mm². That is an equivalent diameter $2\sqrt{A_{\rm mode}/\pi}=0.76$ mm; at $f_{\rm fp}=0.02$ it becomes $0.45/0.02=23$ mm², or 5.4 mm. Using the 0.061° address pitch $\theta_{\rm cell}$ instead of the quoted field, $\tfrac{t^2}{2}(\lambda/\theta_{\rm cell})^2=0.64$ mm², gives 0.9 mm and 6.4 mm.]
    ```
    `new`:
    ```text
    Pointcloud's 61,952-pixel focal-plane array (FPA, §C10.4) could fill its field only with a mode-equivalent collecting diameter of ≈0.9 mm behind its 50 mm lens. The one beam its authors measured, behind a 25 mm test lens focused at 11.1 m [P, Settembrini et al. 2026, Methods and Extended Data Fig. 2c], has a nominal 1/e² footprint fraction of ≈1% at that focus and ≈2% at 22 m on that lens's 0.12° address grid, and hence a mode-equivalent collecting diameter of ≈5 mm and ≈3.5 mm. [E: the full-coverage bound is the identity Eq. (140), derived in item 4, with $f_{\rm fp}\le1$. For the 0.061° address pitch of the 50 mm lens, $\theta_{\rm cell}=53\ \mu{\rm m}/50\ {\rm mm}=1.06\times10^{-3}$ rad, it gives $A_{\rm mode}\lesssim\tfrac{t^2}{2}(\lambda/\theta_{\rm cell})^2=0.42\times(1.31\ \mu{\rm m}/1.06\times10^{-3})^2=0.64$ mm², an equivalent diameter $2\sqrt{A_{\rm mode}/\pi}=0.9$ mm. Spreading the $N_{\rm cell}=61{,}952$ cells over the measured 23.1° × 13.6° field instead, $\theta_{\rm cell}^2=\Omega_{\rm FOV}/N_{\rm cell}$, gives 0.47 mm² (0.77 mm), because that field includes the routing gaps between pixel blocks: 352 × 176 pixels at 0.061° span only 21.4° × 10.7°. The measured beam has $w(R)=w_0\sqrt{1+[(R-11.1\ {\rm m})/z_R]^2}$ with $w_0=1.31$ mm and $z_R=4.1$ m. On the 25 mm lens's pitch, $\theta_{\rm cell}=53\ \mu{\rm m}/25\ {\rm mm}=2.12\times10^{-3}$ rad, its footprint fraction $f_{\rm fp}=\pi w^2/(R\theta_{\rm cell})^2$ is $5.39\ {\rm mm^2}/(23.5\ {\rm mm})^2=1.0\%$ at 11.1 m and, with $w=3.72$ mm, $43.5\ {\rm mm^2}/(46.6\ {\rm mm})^2=2.0\%$ at 22 m. Eq. (33) of §C0 with $t=1$, as in §C0 subsection 10.8, gives $A_{\rm mode}=\lambda^2R^2/(2\pi w^2)=19.6$ mm² (5.0 mm) at 11.1 m and 9.6 mm² (3.5 mm) at 22 m; each times its $f_{\rm fp}$ is $\tfrac12(\lambda/\theta_{\rm cell})^2=0.19$ mm², as Eq. (140) requires.]
    ```
  - (b) §C10.4 table, Pointcloud row, "Beam / address" cell. `old`:
    ```text
    0.06° *address spacing* (53 µm ÷ 50 mm). The beam is much narrower (mode-equivalent collecting diameter ≈6 mm at an assumed ≈2% nominal footprint fraction; §C10.3a, item 5)
    ```
    `new`:
    ```text
    0.06° *address spacing* (53 µm ÷ 50 mm). The beam is much narrower: the one measured, behind a 25 mm test lens, has a nominal 1/e² footprint fraction of ≈1–2% of that lens's 0.12° cells at 11–22 m and a mode-equivalent collecting diameter of ≈3.5–5 mm (§C10.3a, item 5)
    ```
  - (c) §C10 summary of verdicts, FPA bullet. `old`:
    ```text
    For Pointcloud's coherent FPA (*Nature* 2026, 1.31 µm), covering its whole field would leave an $A_{\rm mode}$ equal to that of a lens under 1 mm across; at an assumed ≈2% nominal footprint fraction (defined below), it would get ≈6 mm (§C10.3a, item 5).
    ```
    `new`:
    ```text
    For Pointcloud's coherent FPA (*Nature* 2026, 1.31 µm), covering its whole field would leave an $A_{\rm mode}$ equal to that of a lens under 1 mm across; the one beam its authors measured has a nominal footprint fraction (defined below) of only ≈1–2% at 11–22 m and gets ≈3.5–5 mm (§C10.3a, item 5).
    ```
- **Appendix 2 entry:** none (Settembrini *et al.* is listed; the extended data belong to that article).

---

## R6_C10_part2-02

- **Question:** Which Voyant chip has "just over 5,000 antennas", and is it Helium's production chip?
- **Answer:** The figure comes from a blog post of 14 February 2023 by Peter Stern, "Science Fiction to Forklifts in < 2 Years". It was written nearly three years before Helium was announced (17 December 2025) and does not name it.
  - **What the post describes.** A two-dimensional array of monostatic optical antennas, taped out alongside the first Carbon design. The chips arrived in summer 2022 and were tested in early 2023.
  - **Its three statements.** The demonstration used a small part of the chip, "a 4 x 80 antenna sub-array". The "first generation production version has just over 5000 antennas". Voyant's interface accepts almost any scan pattern at a 30 Hz update rate.
  - **What the figure belongs to.** The 5,000 antennas are the planned first production version of Voyant's 2D on-chip-steered FPA as of February 2023, the line that became Helium. They are not a figure for Helium as announced, which Voyant's 17 December 2025 release gives as an FPA architecture "spanning from 12,000 pixels to over 100,000 pixels". Carbon is the other line: one on-chip axis plus a slow mirror.
  - **Outside this item.** The 17 December 2025 release names a first prototype at CES 2026 and an early-access programme, but gives no production date. The "production 2027" in the same report sentence therefore needs its own source.
- **Source:**
  - P. Stern, "Science Fiction to Forklifts in < 2 Years", Voyant Photonics blog, 14 Feb 2023, https://voyantphotonics.com/news/448/ (full post read).
  - Voyant Photonics, "Voyant Photonics Introduces Industry's First Fully Solid-State 4D FMCW LiDAR…", 17 Dec 2025, https://voyantphotonics.com/news/1075/ (full release read).
  - All 30 posts linked from Voyant's news index were scanned, and this is the only one with the figure: `scripts/R6_voyant_blog_scan.py`.
- **Evidence tag:** [P]
- **Confidence:** high — read directly in the dated company post.
- **Proposed edit:**
  - `old`:
    ```text
    A company blog says the production chip has just over 5,000 antennas, and that the demonstration used a 4 × 80 sub-array at 30 Hz.
    ```
  - `new`:
    ```text
    A February 2023 company blog, written before Helium was named, says that the first-generation production version of its 2D monostatic antenna array would have just over 5,000 antennas, and that its demonstration used a 4 × 80 sub-array of the first 2D chip, at a scan-pattern rate of 30 Hz [P].
    ```
- **Appendix 2 entry:** `- Voyant blog, "Science Fiction to Forklifts in < 2 Years" (P. Stern, Feb 2023; 2D monostatic antenna array, 4 × 80 demonstration, production version of just over 5,000 antennas): https://voyantphotonics.com/news/448/` (group: *Focal-plane arrays and FMCW products*, next to the Voyant Helium announcement).

---

## R6_C10_part2-03

- **Question:** Where does Goodman give the integrated-speckle formula used for the mode counts?
- **Answer:** In J. W. Goodman, *Speckle Phenomena in Optics: Theory and Applications* (Roberts & Company, Englewood, CO, 2007): §4.6, "Statistics of Integrated and Blurred Speckle" (p. 105), and within it §4.6.1, "Mean and Variance of Integrated Speckle" (p. 106).
  - **What the section gives.** The number of degrees of freedom $M$ of speckle integrated over an aperture: the squared area of the aperture divided by the integral of the aperture autocorrelation times $|\mu_A|^2$. For a uniformly weighted aperture this is the report's $N_{\rm spk}=A_{\rm rx}^2/\!\int K_{\rm ap}|\mu|^2\,d^2\Delta$, which `build/figures/coherent_mode_coverage.py` implements (header lines 18–19; functions `goodman_M_gaussian_spot` and `goodman_M_square_cell`).
  - **Its optical-radar origin.** The same count of speckle correlation cells intercepted by a receiving aperture goes back to Goodman's 1965 optical-radar paper, which tied radar performance to it.
  - **Second edition.** SPIE Press, 2020 (DOI 10.1117/3.2548484, ISBN 9781510631496); its section numbers were not checked.
  - **Not verified.** I could not read the book's text: it is paywalled, and the publisher's free sample, Google Books search and the Optica and MDPI pages that restate the formula are behind bot protection. The section and pages are confirmed from the contents listing, so no equation number is given.
- **Source:**
  - Book contents read from the library record "Goodman J.W. Speckle phenomena in optics: theory and applications. Englewood: Roberts & Co., 2007. xvi, 387 p., ISBN 0-9747077-9-1", https://www.prometeus.nsc.ru/acquisitions/12-04-10/cont16f.ssi
  - Second edition from its Crossref record.
  - The 1965 paper as a listing and abstract only: J. W. Goodman, "Some effects of target-induced scintillation on optical radar performance", *Proc. IEEE* 53(11), 1688–1700 (1965), https://ieeexplore.ieee.org/document/1446271/
- **Evidence tag:** [I]
- **Confidence:** medium — the section and pages are confirmed and the formula is Goodman's standard aperture-integration result, but the equation was not read in the book itself.
- **Proposed edit:**
  - `old`:
    ```text
    **Mode counts:** Goodman's integrated-speckle formula, $N_{\rm spk}=A_{\rm rx}^2\big/\!\int K_{\rm ap}(\Delta)\,|\mu(\Delta)|^2\,d^2\Delta$, where $A_{\rm rx}$ is the aperture area
    ```
  - `new`:
    ```text
    **Mode counts:** Goodman's integrated-speckle formula for the degrees of freedom of speckle integrated over a uniformly weighted aperture [I, J. W. Goodman, *Speckle Phenomena in Optics*, 2007, §4.6.1], $N_{\rm spk}=A_{\rm rx}^2\big/\!\int K_{\rm ap}(\Delta)\,|\mu(\Delta)|^2\,d^2\Delta$, where $A_{\rm rx}$ is the aperture area
    ```
- **Appendix 2 entry:** `- Goodman, *Speckle Phenomena in Optics: Theory and Applications* (Roberts & Company, 2007), §4.6.1, mean and variance of integrated speckle (degrees of freedom of an aperture-integrated speckle field); second edition, SPIE Press 2020: https://doi.org/10.1117/3.2548484` (group: *OPA devices, reviews and receive-side analysis*).

---

## R6_C10_part2-04

- **Question:** Which papers give the FSD per-range vehicle AP on Argoverse 2 and the nuScenes zero-lidar-point share beyond 50 m, and do the numbers hold?
- **Answer:**
  - **FSD on Argoverse 2.** The source is Khoche *et al.*, IEEE IV 2024, Table III, "AP comparison (Vehicle class only)".
    - FSD* (FSD re-trained by the authors, with class-balanced sampling for six epochs) scores 89.0 / 61.7 / 29.2 / 13.9 / 3.6 at 0–50 / 50–100 / 100–150 / 150–200 / 200–250 m, and 71.5 over 0–250 m.
    - FSD* with multimodal virtual points (MVP) reaches 23.2 at 150–200 m.
    - The original authors' FSD scores 88.9 / 59.7 / 26.8 / 12.1 / 2.6.
    - The report's numbers match FSD* exactly. Argoverse 2 AP averages precision over 0.5, 1, 2 and 4 m centre-distance match thresholds (the paper's Eq. 3), not over IoU, which the surrounding text otherwise introduces.
  - **nuScenes zero-point share.** Gupta *et al.* (Far3Det, WACV 2023) say in the abstract and introduction that "almost 50%" of objects beyond 50 m contain zero lidar points. Their own appendix Table 11 (nuScenes, 50–80 m) does not support "half" as a share of objects:
    - training set: 45,050 zero-point boxes of $100{,}123+45{,}050=145{,}173$, i.e. 31.0%;
    - validation set: 10,069 of $21{,}658+10{,}069=31{,}727$, i.e. 31.7%.
    - The headline matches the ratio of zero-point boxes to boxes *with* points: $45{,}050/100{,}123=45.0\%$ (46.5% for validation). The same denominator gives the table caption's "≥10%" for unoccluded zero-point boxes ($10{,}430/100{,}123=10.4\%$; it is 7.2% of all boxes).
    - Over all of 0–80 m, main-text Table 1 gives 15.6% of annotations with zero points in the current sweep, and 10.0% once ten sweeps are accumulated.
    - So "about a third of objects at 50–80 m" is the defensible reading.
- **Source:**
  - A. Khoche, L. Pereira Sánchez, N. Batool, S. Sharif Mansouri and P. Jensfelt (KTH, Scania, Stockholm University), "Towards Long-Range 3D Object Detection for Autonomous Vehicles", *2024 IEEE Intelligent Vehicles Symposium (IV)*, IEEE Xplore 10588513. Read in full as arXiv 2310.04800v2 (20 May 2024); Table III on p. 5, metric Eqs. (2)–(3).
  - S. Gupta, J. Kanjani, M. Li, F. Ferroni, J. Hays, D. Ramanan and S. Kong (CMU, Argo AI, Georgia Tech, Texas A&M), "Far3Det: Towards Far-Field 3D Detection", *WACV 2023*, pp. 692–701. Read in full as arXiv 2211.13858v1: abstract and §1 on p. 1, §3.2 on p. 4, Table 1 on p. 5, appendix Tables 9 and 11 on pp. 11–12. The CVF open-access main paper was checked for the same "almost 50%" wording.
  - Arithmetic: `scripts/R6_item_arithmetic.py`.
- **Evidence tag:** [I]
- **Confidence:** high — both read in their own tables.
- **Proposed edit:**
  - (a) `old`:
    ```text
    On Argoverse 2 the vehicle AP of FSD (a fully sparse 3D detector, unrelated to Tesla's FSD software) falls from **89.0 to 61.7, 29.2, 13.9 and 3.6** across 0–50 / 50–100 / 100–150 / 150–200 / 200–250 m. Adding camera virtual points (extra 3D points generated from the camera image) lifts 150–200 m to 23.2.
    ```
    `new`:
    ```text
    On Argoverse 2 the vehicle AP of FSD (a fully sparse 3D detector, unrelated to Tesla's FSD software), averaged over 0.5–4 m centre-distance match thresholds, falls from **89.0 to 61.7, 29.2, 13.9 and 3.6** across 0–50 / 50–100 / 100–150 / 150–200 / 200–250 m. Adding camera virtual points (extra 3D points generated from the camera image) lifts 150–200 m to 23.2 (Khoche et al., IEEE IV 2024, Table III).
    ```
  - (b) `old`:
    ```text
    In nuScenes (32 beams), about **half of all objects beyond 50 m have zero lidar points**.
    ```
    `new`:
    ```text
    In nuScenes (32 beams), about **a third of the annotated objects at 50–80 m have zero lidar points**: 45,050 of 145,173 training boxes and 10,069 of 31,727 validation boxes (Gupta et al., Far3Det, WACV 2023, appendix Table 11). The paper's headline "almost 50%" matches the ratio of zero-point boxes to boxes with points ($45{,}050/100{,}123=45\%$).
    ```
- **Appendix 2 entry:** none (both are listed under *Resolution value, regulations and datasets*).

---

## R6_C10_part2-05

- **Question:** Is Rogers *et al.* (*Nature* 2021) company-authored, which would keep the [P] tag?
- **Answer:** Yes; [P] stays, as for Settembrini *et al.* (2026).
  - **Authors.** 7 of the 12 authors are at Pointcloud Inc. (San Francisco), including both equal-contribution first authors (C. Rogers, A. Y. Piggott) and the corresponding author (R. Nicolaescu). Four are at the Optoelectronics Research Centre, University of Southampton (D. J. Thomson, F. Meng, X. Chen, G. T. Reed), and one at Opris Consulting (I. E. Opris).
  - **Competing interests.** All authors except F.M. and X.C. declare that they are shareholders of Pointcloud Inc.
  - **Pointcloud's own record.** Settembrini *et al.* (2026) list the paper as their own "Prev. work" in Extended Data Table 1.
  - The edit adds the affiliation so that the tag's basis is visible.
  - **Other checks in the same paper.** The 3.1 mm precision at 75 m is on a 30%-reflectance target with 4 mW at the aperture, at 42% detection probability; the paper also reports 1.8 mm at 17 m on an 85% target. The 24× signal gain from the transmit microlens array is confirmed.
  - **Adjacent finding, outside this item.** The §C10.4 bullet "The design was bistatic, with separate transmit and receive apertures (16 transmit, 512 receive)" does not match the paper. Two identical chips serve as transmitter (a 1 × 16 switch tree with 16 gratings) and receiver (32 × 16 pixels), but they share one output lens of 25 mm physical aperture through a polarizing beamsplitter and a Faraday rotator (Methods, "Optical setup"; Extended Data Fig. 3). An optional second edit is given below.
- **Source:** C. Rogers, A. Y. Piggott, D. J. Thomson, R. F. Wiser, I. E. Opris, S. A. Fortune, A. J. Compston, A. Gondarenko, F. Meng, X. Chen, G. T. Reed and R. Nicolaescu, "A universal 3D imaging sensor on a silicon photonics platform", *Nature* 590, 256–261 (2021), https://doi.org/10.1038/s41586-021-03259-y.
  - Read in full as arXiv 2008.02411v3 (11 Nov 2020): affiliations on p. 1; competing interests and contributions on p. 7; Methods "Optical setup" on p. 10; Extended Data Fig. 3 on p. 16.
  - Affiliations of the published version confirmed from its Europe PMC / PubMed record (PMID 33568821).
- **Evidence tag:** [P]
- **Confidence:** high
- **Proposed edit:**
  - `old`:
    ```text
    | Rogers et al. (*Nature* 2021) [P] |
    ```
  - `new`:
    ```text
    | Rogers et al. (Pointcloud Inc. with the University of Southampton, *Nature* 2021) [P] |
    ```
  - Optional, for the adjacent finding. `old`:
    ```text
    The design was bistatic, with separate transmit and receive apertures (16 transmit, 512 receive).
    ```
    `new`:
    ```text
    The design was bistatic at the chip level: a 16-grating transmit chip and a 512-pixel receive chip, combined by a polarizing beamsplitter and a Faraday rotator behind one output lens of 25 mm aperture [P].
    ```
- **Appendix 2 entry:** none (listed).

---

## R6_C10_part2-06

- **Question:** Who said that Mobileye's PIC channels are "moved through optics", and where?
- **Answer:** Mobileye's CEO, Amnon Shashua, in his CES 2021 "Under the Hood" talk.
  - **Where it is recorded.** Mobileye's own live blog of the talk, in its 10:55 a.m. entry: he showed a photonic integrated circuit with "184 vertical lines", and said those lines are "moved through optics".
  - **Context in the same entry.** Intel can put active and passive laser elements on one chip, which he called a significant advantage for building these lidars.
  - The cancellation in September 2024 stays as tagged in §B3.
- **Source:** Mobileye, "CES 2021: Under the Hood with Prof. Amnon Shashua (Replay & Live Blog)", published 12 Jan 2021 UTC (page metadata), https://www.mobileye.com/news/ces-2021-under-the-hood-with-prof-amnon-shashua/ (full page read).
- **Evidence tag:** [P]
- **Confidence:** high
- **Proposed edit:**
  - `old`:
    ```text
    Mobileye/Intel: parallel PIC (photonic integrated circuit) channels "moved through optics", in an in-house FMCW programme cancelled in 2024 (§B3) [P/T];
    ```
  - `new`:
    ```text
    Mobileye/Intel: parallel PIC (photonic integrated circuit) channels, "184 vertical lines" that its CEO said are "moved through optics" (CES 2021) [P], in an in-house FMCW programme cancelled in 2024 (§B3) [P/T];
    ```
- **Appendix 2 entry:** `- Mobileye, CES 2021 "Under the Hood" live blog (Shashua: FMCW lidar PIC with 184 vertical lines scanned by optics): https://www.mobileye.com/news/ces-2021-under-the-hood-with-prof-amnon-shashua/` (group: **FMCW and beam steering**, next to "Mobileye ends lidar development").

---

## R6_C10_part2-07

- **Question:** What sources show Voyant (August 2026) and 国科光芯 (September 2026) moving into data-centre optical switching?
- **Answer:**
  - **Voyant: yes, optical circuit switching (OCS).** A technical white paper by co-founder and CTO Steven Miller, dated August 2026 and posted on 31 August 2026, says the switch fabric Voyant developed for its FMCW lidar "is now being pointed at" OCS.
    - Its conclusion says Voyant is deploying the same core switching fabric into datacenter optical circuit switching.
    - It names Voyant, Salience Labs and iPronics as developers of on-chip silicon-photonics OCS, and says Lumotive is developing OCS with its LCM. That last point supports the Lumotive bullet two lines above in the report.
  - **国科光芯: not switching, but data-centre optical interconnect.** Its B+ round of several hundred million yuan was announced on 3 September 2026. It was led by the Sichuan science-and-technology innovation investment group, with Hangzhou Kaitai Capital and the Shandong science-and-technology innovation group following.
    - The proceeds are mainly for: next-generation 400 Gb/s-per-lane silicon-photonics chips; 1.6T/3.2T silicon-photonic detector chips; 3.2T/6.4T NPO/CPO (near- and co-packaged optics); OIO chiplets; expansion of its datacom subsidiary (brand 星汉光子); and an overseas delivery centre.
    - The reports add that it has developed 400G/800G/1.6T datacom silicon-photonics chips, lidar and chip-integrated OCT products.
    - None of the four reports read mentions optical switching for the company. The only "光交换" (optical switching) hit is an MIIT policy paragraph in a Cailian sector article.
- **Source:**
  - S. Miller, "Silicon Photonics Switching: Empowering AI in the Physical and Virtual World", Voyant Photonics technical white paper, Aug 2026, 14 pp., read in full (§1 p. 2, §5.2 p. 12, §6 p. 14): https://voyantphotonics.com/wp-content/uploads/2026/08/Silicon-Photonics-Switching-Empowering-AI-Physical-Virtual-World-Voyant-Photonics.pdf; posting at https://voyantphotonics.com/news/1111/ (31 Aug 2026).
  - 瑞财经 (王敏), Tencent News, 3 Sep 2026: https://news.qq.com/rain/a/20260903A09R9000
  - 人民财讯 via 同花顺, 3 Sep 2026: https://news.10jqka.com.cn/20260903/c679562317.shtml
  - 界面新闻 via 东方财富: https://finance.eastmoney.com/a/202609033863967450.html
  - 科创板日报 sector piece: https://www.chinastarmarket.cn/detail/2473562
  - All four Guoke reports were read; they carry identical wording, evidently one company release. The company's own website is a JavaScript-only page and showed no release.
- **Evidence tag:** [P] for Voyant; [T] for 国科光芯.
- **Confidence:** high for Voyant; medium-high for 国科光芯 (trade-press relays of one release).
- **Proposed edit:**
  - `old`:
    ```text
    Voyant (August 2026) and 国科光芯 (Guoke Guangxin, a Haining-based maker of SiN OPA chips, §D7; September 2026) are also moving into data-centre optical switching.
    ```
  - `new`:
    ```text
    Voyant is pointing its lidar switch fabric at data-centre optical circuit switching, in a white paper by its CTO (August 2026) [P]. 国科光芯 (Guoke Guangxin, a Haining-based maker of SiN OPA chips, §D7) raised a B+ round of several hundred million yuan in September 2026 mainly for data-centre optical interconnect: 400 Gb/s-per-lane silicon-photonics chips, 1.6T and 3.2T detector chips, near- and co-packaged optics (NPO/CPO) and OIO chiplets, and to expand its datacom subsidiary 星汉光子 [T].
    ```
- **Appendix 2 entry:**
  - `- Voyant, "Silicon Photonics Switching" white paper (S. Miller, Aug 2026; lidar switch fabric aimed at datacenter optical circuit switching): https://voyantphotonics.com/wp-content/uploads/2026/08/Silicon-Photonics-Switching-Empowering-AI-Physical-Virtual-World-Voyant-Photonics.pdf` (group: *Focal-plane arrays and FMCW products*).
  - `- 国科光芯 B+ round and use of proceeds (瑞财经 via Tencent News, 3 Sep 2026): https://news.qq.com/rain/a/20260903A09R9000` (group: **Supply chain and geopolitics**, with the §D7 sources).

---

## R6_C10_part2-08

- **Question:** Why is Piggott *et al.*'s ≈6 dB coherent-versus-ToF gap larger than the 4.7 dB far-field factor of the report's model?
- **Answer:** The two figures size the comparison aperture differently. Polarization costs 3 dB in both.
  - **Piggott's comparison.** In §2.5 and Fig. 5(a), Piggott *et al.* compare a monostatic coherent lidar using a collimated Gaussian beam ($w_0=10$ mm) with a ToF lidar whose 30 mm lens is "just large enough to avoid significant clipping" of that Gaussian.
  - **Piggott's breakdown.** Beyond the Rayleigh range the coherent link is about 6 dB lower: 3 dB because it detects one polarization, and about 3 dB because the coherent receiver collects mostly from the centre of the Gaussian while the ToF lens is larger.
  - **Derivation of Piggott's 6 dB.** Their Eq. (15) with $A_{\rm eff}=\pi w^2$ and $w\to\lambda R/(\pi w_0)$ gives a far-field coherent equivalent collecting area of $\pi w_0^2/2$. The ToF lens area is $\pi a^2$ with $a=15$ mm. Their ratio is $2(a/w_0)^2=2\times2.25=4.5$, i.e. 3.0 + 3.5 = 6.5 dB ("approximately 6 dB"). The 30 mm lens barely clips the beam: $t=1-e^{-2\times1.5^2}=0.989$.
  - **The report's model.** Its Gaussian fills its own hard aperture more fully: $w_0=0.45D$, an aperture radius of $1.11w_0$ against Piggott's $1.5w_0$. In exchange it pays the truncation $t^2=0.838$. Its ratio is $2(0.5/0.45)^2/t^2=2\times1.473=2.95$, i.e. 3.0 + 1.7 = 4.7 dB.
  - **The difference.** The 1.84 dB gap comes entirely from the aperture-to-waist ratio chosen for the comparison, not from different physics.
  - **Consistency elsewhere.** §C7a's "(3 dB polarization, 3 dB aperture)" for the same figure agrees with this breakdown.
- **Source:** A. Y. Piggott, C. Y. Jiang, J. Lam, B. Gassend and S. Verghese (Waymo LLC), "Coherent lidar for ride-hailing autonomous vehicles", arXiv 2502.09736v1 (13 Feb 2025), also in Proc. SPIE *High-Power Diode Laser Technology XXIII* (2025). Read in full: §2.3, Eqs. (14)–(15) on p. 6; §2.5 and Fig. 5(a) on p. 8. Arithmetic: `scripts/R6_item_arithmetic.py`.
- **Evidence tag:** [P] for Piggott *et al.*'s breakdown; [E] for the comparison with the model.
- **Confidence:** high
- **Proposed edit:**
  - `old`:
    ```text
    Piggott et al. (Waymo) put coherent detection about 6 dB behind ToF at equal aperture, from polarization and mode weighting [P]; the far-field factor of item 2 in this model is 2.9×, or 4.7 dB.
    ```
  - `new`:
    ```text
    Piggott et al. (Waymo) put coherent detection about 6 dB behind ToF at long range: 3 dB for the single polarization and ≈3 dB because their 30 mm ToF lens, sized not to clip the coherent beam's Gaussian wings ($w_0=10$ mm), has $(15/10)^2=2.25$ times the coherent mode's far-field collecting area $\pi w_0^2$ before polarization [P, §2.5, Fig. 5(a)]. The far-field factor of item 2 in this model is 2.9×, or 4.7 dB, because its Gaussian fills the hard aperture more fully ($w_0=0.45D$, an aperture radius of $1.11w_0$ against $1.5w_0$) and pays 1.47× (1.7 dB) for mode shape and truncation instead of 2.25× (3.5 dB); the polarization factor is the same [E].
    ```
- **Appendix 2 entry:** none (listed).

---

## R6_C10_part2-09

- **Question:** Are Namuga's Stella-2 and Stella-180 the same product?
- **Answer:** No.
  - **Stella-2.** Namuga's first solid-state lidar, co-developed with Lumotive around its LCM.
    - It was first shown at the Embedded Vision Summit in May 2025: 120° × 90° field, 30 m typical and 80 m maximum range, below 15 W, MIPI interface.
    - It was launched at CES 2026. The November 2025 release lists 15–80 Hz programmable scanning, up to 100 m in its HDR mode (no reflectivity stated) and below 15 W.
    - Namuga reports first Stella-2 samples supplied at CES 2026 to a North American e-commerce partner.
  - **Stella-180 is a separate wide-angle model.** Namuga's April 2026 brochure lists two models, both 256 × 192 points at 30 Hz with a 72 m maximum range:
    - Stella 120: 120° × 90° field, 0.47° resolution, 40 m on a 10% target at 100 klux;
    - Stella 180: 185° × 110° field, 0.7° resolution, 30 m on a 10% target at 100 klux.
  - **Lumotive's account.** Its 9 April 2026 release says Namuga "recently showcased its Stella-180 prototype", with OEM samples targeted for later in 2026. It is built on Lumotive's LM10 and Adaps ADS6311 platform (180° × up to 140°, up to 50 m, 30 fps), which matches §F5.
  - **Not stated [U].** Whether Stella 120 is a renamed Stella-2: it has the same 120° × 90° field but different range and frame-rate figures.
- **Source:**
  - Namuga, "NAMUGA and Lumotive Demo Stella-2 at CES 2026", 24 Nov 2025: https://namuga.com/eng/invest/news_view.php?v_seqno=307
  - Lumotive release on Namuga's site, "NAMUGA Unveils Stella-2: Compact, Solid-State Lidar Powered by Lumotive, at Embedded Vision Summit", 26 May 2025: https://namuga.com/eng/invest/news_view.php?v_seqno=254
  - Namuga release relayed by the Edge AI and Vision Alliance, "NAMUGA Successfully Concludes CES Participation, official Launch of Next-Generation 3D LiDAR Sensor 'Stella-2'", 22 Jan 2026: https://www.edge-ai-vision.com/2026/01/namuga-successfully-concludes-ces-participation-official-launch-of-next-generation-3d-lidar-sensor-stella-2/
  - Namuga, "STELLA – Wide Range Solid-State LiDAR" brochure (PDF dated 30 Apr 2026), p. 1 table: https://namuga.com/down/NAMUGA_ProductIntro.pdf
  - Lumotive, "Lumotive's LCM Optical Semiconductor Platform Enables First Solid-State 180° dTOF LiDAR at 30 FPS", 9 Apr 2026: https://lumotive.com/press-releases/lumotives-lcm-optical-semiconductor-platform-enables-first-solid-state-180-dtof-lidar-at-30-fps/
  - All read in full.
- **Evidence tag:** [P]
- **Confidence:** high that the two products differ; low on whether Stella 120 continues Stella-2.
- **Proposed edit:**
  - `old`:
    ```text
    **Namuga Stella-2 (CES 2026):** ≤100 m, 15–80 Hz, below 15 W.
    ```
  - `new`:
    ```text
    **Namuga Stella-2** (first shown in May 2025, launched at CES 2026): ≤100 m in its HDR mode (reflectivity not stated), 15–80 Hz, below 15 W; the May 2025 release gave a 120° × 90° field and 30 m typical, 80 m maximum range [P]. It is not the Stella-180 of §F5: Namuga's April 2026 brochure lists a separate wide-angle pair, Stella 120 (120° × 90°) and Stella 180 (185° × 110°), both 256 × 192 points at 30 Hz, 72 m maximum range and 40 m or 30 m on a 10% target in 100 klux [P].
    ```
- **Appendix 2 entry:** `- Namuga Stella-2 releases (debut May 2025; CES 2026, Nov 2025) and Stella 120/180 brochure (Apr 2026): https://namuga.com/eng/invest/news_view.php?v_seqno=254 ; https://namuga.com/eng/invest/news_view.php?v_seqno=307 ; https://namuga.com/down/NAMUGA_ProductIntro.pdf` (group: *Lumotive LC metasurface*).
