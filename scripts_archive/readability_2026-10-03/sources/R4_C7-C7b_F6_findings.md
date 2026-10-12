# Round 4 source findings: R4_C7-C7b_F6

Read on 5 Oct 2026 against the report at sha 51d60fa27199 and re-checked at sha 803514977999, the version current at the final check (equations renumbered: the chirp tolerance is Eq. (108), the phase variance Eq. (109), the coherent fraction Eq. (110), the linewidth requirement Eq. (111)). Every `old` string below occurs exactly once in the sha 803514977999 file, and no two `old` strings overlap (12 strings; check script `scripts/R4_check_old_strings.py`). Line numbers are given only as a guide; none of the anchor lines moved between the two versions.

Scripts used: `scripts/R4_pdf_tools.py` (fetch and render), `scripts/R4_jats_to_text.py`, `scripts/R4_html_to_text.py`, `scripts/R4_coherent_loss.py` (Eq. (109)–(110) with measured spectra), `scripts/R4_waymo_and_linearity_check.py` (Waymo Table 1 and nonlinearity conversions), `scripts/R4_check_old_strings.py`.

Two edits depend on each other: the item-04 edit of §C7a(f) spells out E-DBR at its first use (line ≈4843), and the item-02 edit (line ≈4847) then writes "TFLN E-DBR lasers" without a second expansion. TFLN is already spelled out at line ≈4668.

---

## R4_C7-C7b_F6-01

- **Question:** In Piggott et al. (2025), what produces Waymo's four averaged speckles: one aperture over time or over wavelength, or several receivers?
- **Answer:** One receiver, over time. The paper's receiver is a monostatic, single-mode heterodyne receiver; a coherent lidar "can only detect light in a single optical mode per balanced detector" (§2, p. 3). In §3.2 (pp. 11–12) the photoelectrons needed for high detection probability are reduced by combining $n$ independent speckle realizations, obtained by scanning the beam across the scene so that the carrier amplitude decorrelates over successive acquisitions. The energies are added incoherently, "for example by summing the frequency spectra of several FMCW lidar acquisitions" (Fig. 8 caption): $A_i=\sum_{j=1}^{n}E_i^{(j)}$, which is Erlang-distributed, so $P_D=F_{\rm Erlang}(t;n,N+1)$ and $P_{FA}=F_{\rm Erlang}(t;n,1)$ (Eqs. (31)–(34)). The x-axis of Fig. 8(b) is $n\times N$, the total over the $n$ acquisitions. Wavelength or polarization diversity and multiple receivers are not mentioned anywhere in the paper. Table 1 (ADAS case, p. 13) lists "Number of averaged speckles 4" and "Photons per detection 50", so the 50 is the total over four successive acquisitions through one receiver. The report's one-receiver check is therefore the like-for-like reading, and the 0.34 µJ four-receiver case describes the §C7a design, not Waymo's.
  - *Second finding (edit 01b).* Table 1 also lists "Chirps per point 2", and its ideal 0.52 µJ per shot pays for two detections of 50 photons through the worst-case link of −106.1 dB: $E_{\rm shot}=2\times50\times E_{\rm ph}/T_{\rm link}$ with $E_{\rm ph}=1.28\times10^{-19}$ J and $T_{\rm link}=10^{-10.61}=2.45\times10^{-11}$, so $E_{\rm shot}=1.28\times10^{-17}/2.45\times10^{-11}=5.2\times10^{-7}$ J $=0.52$ µJ, and $0.52\ \mu{\rm J}\times1.2\times10^{7}\ {\rm s^{-1}}=6.2$ W. Reproduced independently: $w_0=10$ mm, $z_R=\pi w_0^2/\lambda=202.7$ m, $w(250\ {\rm m})=15.9$ mm, $T_{\rm link}=\lambda^2R/(2\pi\cdot\pi w^2)=-106.2$ dB, $E_{\rm shot}=0.53$ µJ. Waymo's "at least 10–20 W" adds 3–6 dB of system loss (pp. 13–14). The report's check evaluates 50 photoelectrons, one chirp's worth, and compares it with Waymo's per-point energy for two chirps. For two chirps Eq. (93) gives $100\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=2.70$ µJ at $\eta=0.25$, which is $2.70/1.67=1.6$ to $2.70/0.83=3.3$ times Waymo's 0.83–1.67 µJ, and 1.35 µJ at $\eta=0.5$, the efficiency of Waymo's 3 dB case. Waymo's per-point budget of 100 photons (≈90 photoelectrons at its 90% quantum efficiency) also sits close to the report's 88.5 photoelectrons for a peak in both ramps (§C0 subsection 10.3). A small wording point, not edited: Table 1 says 50 *photons* per detection, i.e. 45 photoelectrons at 90% quantum efficiency, which is the 44.9 the report itself derives at Waymo's $10^{-6}$ per bin (§C0, line ≈2018).
- **Source:** A. Y. Piggott, C. Y. Jiang, J. Lam, B. Gassend and S. Verghese (Waymo LLC), "Coherent lidar for ride-hailing autonomous vehicles", arXiv:2502.09736v1, 13 Feb 2025 (presented at SPIE Photonics West 2025), https://arxiv.org/abs/2502.09736. Full text read (20 pages rendered): §2 p. 3; §3.2 pp. 11–12 with Eqs. (23)–(34) and Fig. 8; §4.1 Table 1 p. 13; p. 14 for the 10–20 W.
- **Evidence tag:** [P] (Waymo's own paper)
- **Confidence:** high — the mechanism is stated explicitly and is the only one the paper describes; Table 1 was reproduced to 0.1 dB.
- **Proposed edit (01, the item):**
  - `old`:
    ```text
    The check uses one receiver's $A_{\rm mode}$, so it assumes that all 50 photoelectrons, and all four of Waymo's speckles, arrive through one receiver. With four separate receivers, as in the §C7a design, the same 50 photoelectrons would need $1.35/4\approx0.34$ µJ, below Waymo's range, so the agreement holds only if Waymo's four speckles come from within one receiver.
    ```
  - `new`:
    ```text
    One receiver is the right basis for the check, because Waymo takes all four speckles through one single-mode receiver: it sums the FFT spectra of successive acquisitions, between which the scanning beam has moved enough to decorrelate the speckle, and its 50 is the total over the four acquisitions [P, Piggott et al. 2025, §3.2 and Fig. 8(b)]. The §C7a design takes its four looks through four receivers at once instead, which divides the energy for the same 50 photoelectrons by four, to $1.35/4\approx0.34$ µJ.
    ```
- **Proposed edit (01b, second finding; independent of 01):**
  - `old`:
    ```text
    Eq. (93) for one receiver with $A_{\rm mode}=74.5$ mm² (a 20 mm aperture at 250 m) and $\eta=0.25$ gives $50\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=1.35$ µJ, inside that range.
    ```
  - `new`:
    ```text
    Eq. (93) for one receiver with $A_{\rm mode}=74.5$ mm² (a 20 mm aperture at 250 m) and $\eta=0.25$ gives $50\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=1.35$ µJ for one ramp. Waymo's energy per point pays for two chirps of 50 photons each: its ideal 0.52 µJ is $2\times50\times1.28\times10^{-19}\ {\rm J}/(2.45\times10^{-11})$, through a −106.1 dB worst-case link [P, Piggott et al. 2025, Table 1]. The like-for-like value is therefore $2\times1.35=2.7$ µJ at $\eta=0.25$, 1.6–3.3× Waymo's range, or 1.35 µJ at $\eta=0.5$, the efficiency of Waymo's 3 dB case, which lies inside it [E].
    ```
- **Appendix 2 entry:** none (Piggott et al. is listed under *OPA, FPA, LC metasurface and resolution value*).

---

## R4_C7-C7b_F6-02

- **Question:** Do Bianconi et al. (2025) define "nonlinearity" as a peak or an RMS frequency deviation over the sweep, or as a chirp-rate error?
- **Answer:** As an RMS frequency deviation, normalized to the sweep excursion. The main text defines a 1% non-linearity as "the normalized RMS deviation from the linear chirp". The Supplementary Information makes it exact (§1, Eq. (4)): for a chirp $f_{LO}(t)=at^2+bt+f_0$ over one ramp $0\le t\le T/2$, the straight ramp is the RMS (least-squares) fit, of slope $\beta=b+aT/2$ and offset $f_0=aT^2/24$, and
  $$\sigma_{RMS}=\frac{\sqrt{\frac{1}{T/2}\int_0^{T/2}\left(at^2+(b-\beta)t+f_0\right)^2dt}}{BW}=\frac{1}{6\sqrt5}\,\frac{a}{\beta}\,\frac{T}{2},$$
  with $BW=\beta T/2$ the total excursion of a symmetric triangle. So $\sigma=\delta\nu_{\rm rms}/B$: neither a chirp-rate error nor a peak deviation. Table 1 lists, under "Linewidth (1 ms)" and "Non-linearity": DFB (InP/InGaAs) 802 kHz and 1.8%; E-DBR (lithium niobate) 378 kHz and 1.5%; SIL (silicon nitride) 42 kHz and 0.65%. An Author Correction (9 Apr 2026) restored a factor of 6 in Eq. (1) and SI Eqs. (4) and (16); the versions read here are the corrected ones, and the definition is unchanged.
  - *Where the two values come from.* The 1.5% is the E-DBR laser of Siddharth et al.: Fig. 3(f) of their preprint gives an RMS deviation of 156.787 MHz over a 10.4835 GHz excursion (1.4956%) for the slowest triangle, 1.6131% over 9.97 GHz and 2.3118% over 9.30 GHz at 1 MHz. The 0.65% is the self-injection-locked laser of Voloshin et al.: Fig. 4(a), an unpackaged 1.5 GHz-FSR chip on carbon tape, 100 V peak to peak, 10 kHz triangle, $B=500$ MHz. Packaged on a glass submount, the same design reached 0.08% over $B=210$ MHz without linearization (Fig. 4(b)).
  - *Conversion to the report's Eq. (108).* For a parabolic bow over a ramp of length $L$, the peak deviation from the chord is $\delta\nu_{\max}=aL^2/4$ and the RMS deviation from the least-squares line is $\delta\nu_{\rm rms}=aL^2/(6\sqrt5)$, so $\delta\nu_{\max}/\delta\nu_{\rm rms}=6\sqrt5/4=3\sqrt5/2=3.354$ (checked numerically). The fractional peak-to-peak chirp-rate error is $\varepsilon=8\delta\nu_{\max}/B=12\sqrt5\,\sigma=26.8\,\sigma$. Assuming the same fractions over a 1 GHz sweep:
    - SIL, unpackaged, $\sigma=0.0065$: $\delta\nu_{\rm rms}=6.5$ MHz, $\delta\nu_{\max}=3.354\times6.5=21.8$ MHz, $\varepsilon=26.8\times0.0065=0.174$; against $c/(16R)=62.5$ kHz at 300 m, $21.8/0.0625=349\times$ (and $0.174/5\times10^{-4}=349\times$);
    - E-DBR, $\sigma=0.015$: 15 MHz, 50.3 MHz, $\varepsilon=0.40$; $805\times$;
    - SIL, packaged, $\sigma=0.0008$: 0.8 MHz, 2.68 MHz, $\varepsilon=0.021$; $43\times$.
    The report's current readings, 100–240× (as peak deviations) and 13–30× (as chirp-rate errors), both understate the gap.
  - *Tag.* The report cites Bianconi et al. as [P]; under its legend an academic paper is [I]. The same applies to "[P, Bianconi et al.]" in the next bullet (line ≈4849, very fast chirps), which is outside this item and is not edited here.
- **Source:** S. Bianconi (EPFL), P. Ribes-Pleguezuelo (ESA ESTEC) and F. Silvestri (TNO), "Requirements for next-generation integrated photonic FMCW LiDAR sources", *Nat. Commun.* 16, 6739 (2025), published 22 Jul 2025, https://doi.org/10.1038/s41467-025-62027-y; Author Correction, 9 Apr 2026, https://doi.org/10.1038/s41467-026-71867-1. Read: full text (Europe PMC JATS XML, PMC12283932), Fig. 1 image, Table 1, and the Supplementary Information PDF (8 pp., corrected version), pp. 2–5. Original papers, read as preprints: A. Siddharth *et al.*, "Ultrafast tunable photonic integrated Pockels extended-DBR laser", arXiv:2408.01743v1 (3 Aug 2024), published in *Nat. Photonics* 19, 709–717 (2025), pp. 4–5 and Fig. 3; A. Voloshin *et al.*, "Monolithic piezoelectrically tunable hybrid integrated laser with sub-fiber laser coherence", arXiv:2411.19264v1 (28 Nov 2024), published in *Optica* 12 (2025), pp. 6–7 and Fig. 4.
- **Evidence tag:** [I]
- **Confidence:** high — the definition is given in words in the paper and as an equation in its Supplementary Information.
- **Proposed edit (also answers item 08; depends on the E-DBR expansion in the item-04 edit):**
  - `old`:
    ```text
    Integrated alternatives are SiN self-injection-locked lasers (42 kHz, 0.65% nonlinearity) and thin-film lithium niobate (TFLN) E-DBR lasers (378 kHz, 1.5%) [P, Bianconi et al. 2025]. Read as peak frequency deviations over a 1 GHz sweep, the reading applied to Waymo's figure above, those nonlinearities are 6.5 and 15 MHz, ≈100–240× the 62.5 kHz that Eq. (108) allows at 300 m. Read as fractional chirp-rate errors, they are still 13–30× above the $5\times10^{-4}$ that 15 cm at 300 m tolerates. Either way they need pre-distortion or resampling [E].
    ```
  - `new`:
    ```text
    Integrated alternatives are SiN self-injection-locked lasers (42 kHz linewidth over 1 ms, 0.65% nonlinearity) and TFLN E-DBR lasers (378 kHz over 1 ms, 1.5%) [I, Bianconi et al. 2025]. Bianconi et al. define the nonlinearity $\sigma$ as the RMS deviation of the laser frequency from a least-squares straight ramp, divided by the sweep excursion $B$ [I, Bianconi et al. 2025, Supplementary Eq. (4)]. The 0.65% belongs to an unpackaged self-injection-locked chip swept over 500 MHz, which reached 0.08% over 210 MHz once packaged [I, Voloshin et al. 2025]; the 1.5% was measured over a 10.5 GHz sweep [I, Siddharth et al. 2025]. For the parabolic bow of Eq. (108) the peak deviation from the chord is $3\sqrt5/2\approx3.35$ times the RMS deviation, so $\delta\nu_{\max}=3.35\,\sigma B$ and $\varepsilon=8\delta\nu_{\max}/B=12\sqrt5\,\sigma\approx27\sigma$. If the same fractions hold over a 1 GHz sweep, 0.65% and 1.5% give $\delta\nu_{\max}\approx22$ and 50 MHz, or $\varepsilon\approx0.17$ and 0.40: about 350× and 800× the 62.5 kHz (equivalently the $5\times10^{-4}$) that Eq. (108) allows for 15 cm at 300 m. The packaged 0.08% is still about 43× too large. They need pre-distortion or resampling [E].
    ```
- **Appendix 2 entry:** three lines (group *FMCW and beam steering*):
  - `- Bianconi, Ribes-Pleguezuelo & Silvestri, requirements for integrated FMCW lidar laser sources (1 ms linewidths, RMS chirp nonlinearity), *Nat. Commun.* 16, 6739 (2025), with Author Correction (2026): https://doi.org/10.1038/s41467-025-62027-y`
  - `- Siddharth et al., Pockels extended-DBR (E-DBR) laser on thin-film LN, *Nat. Photonics* 19, 709 (2025) (preprint): https://arxiv.org/abs/2408.01743`
  - `- Voloshin et al., piezo-tunable SiN self-injection-locked laser (3 Hz intrinsic linewidth), *Optica* (2025) (preprint): https://arxiv.org/abs/2411.19264`

---

## R4_C7-C7b_F6-03

- **Question:** What are the sources for five untagged statements in §C7 *Commercial status*: Honda's investment in SiLC; Aeva's automated Jabil line of about 100k units per year and the 2027 Daimler launch; LightIC's use of Tower Semiconductor; LuminWave's "Raptor" engine and its July 2025 nomination?
- **Answer:** All five have primary sources.
  - *SiLC–Honda.* Honda Xcelerator Ventures announced "a strategic investment in SiLC Technologies Inc." on 10 Sep 2024; SiLC's own release of the same day says it "has received an investment from Honda". The amount is not disclosed.
  - *Aeva–Jabil.* On its Q4 2025 call (26 Feb 2026) Aeva said it had completed the buildup of its automated final-assembly line, "which we expect to enable systems annual capacity to reach 100,000". On its Q2 2026 call (12 Aug 2026) it said it had "begun manufacturing at our fully automated assembly line at Jabil North America". So "about 100k units per year" is an expected capacity, stated by Aeva, of the line at Jabil. Separately, on 16 Jul 2025 Aeva said it "plans to increase its production capacity to up to 200,000 LiDAR units annually" in North America. (§D5, line ≈7249, places the Jabil line in the US; Aeva says only "North America". No edit proposed there.)
  - *Daimler 2027.* The Aeva–Daimler Truck release of 9 Jan 2024 gives "Aeva's start of production by 2026 and Daimler Truck's production ramping up by 2027", and quotes Daimler Truck's Joanna Buttler as on track to offer autonomous trucks in the U.S. "by 2027". The C-sample release of 6 May 2026 confirms the program "advances towards series production" but gives no year.
  - *LightIC–Tower.* Tower Semiconductor and LightIC announced on 5 Jan 2026 a collaboration "leveraging Tower's mature silicon photonics platform to support LightIC's" FMCW products, "including the Lark" long-range automotive lidar. LightIC's CEO is quoted as using Tower's silicon-photonics process for qualification and long-term production.
  - *LuminWave.* The Raptor release (10 Sep 2024) describes a single chip on an "internationally leading" III-V/silicon heterogeneous platform, with an on-chip chirped laser of more than 10 GHz FM bandwidth and 8–16 FMCW receive channels, and names the "LuminWave Raptor" product line. The nomination release (8 Jul 2025) announces a formal nomination by an unnamed leading commercial-vehicle customer for a new-generation L2+ series-production program; the body names no product, customer or SOP and does not say FMCW (FMCW appears only in the site menu). The report's wording is correct.
- **Source:**
  - Honda Xcelerator Ventures, "Honda Xcelerator Ventures is excited to announce our new partnership with SiLC Technologies", 10 Sep 2024, https://xcelerator.hondainnovations.com/honda-xcelerator-ventures-is-excited-to-announce-our-new-partnership-with-silc-technologies/ (full page read); SiLC Technologies, "SiLC Technologies Receives Investment from Honda to Advance AI Vision Capabilities", Business Wire, 10 Sep 2024 (read in the full relay at https://www.theautochannel.com/news/2024/09/10/1427811-silc-technologies-receives-investment-from-honda-to-advance-ai-vision.html).
  - Aeva Q4 2025 earnings call, 26 Feb 2026, transcript (Motley Fool), https://www.fool.com/earnings/call-transcripts/2026/02/26/aeva-aeva-q4-2025-earnings-call-transcript/; Aeva Q2 2026 earnings call, 12 Aug 2026, transcript, https://www.fool.com/earnings/call-transcripts/2026/08/12/aeva-aeva-q2-2026-earnings-call-transcript/; Aeva, "Aeva to Accelerate Scaled Production of 4D LiDAR for Autonomous Trucks in Collaboration with Daimler Truck North America", 16 Jul 2025, https://www.aeva.com/press/aeva-to-accelerate-scaled-production-of-4d-lidar-for-autonomous-trucks-in-collaboration-with-daimler-truck-north-america/ (all read in full).
  - Aeva and Daimler Truck, "Daimler Truck and Torc Robotics Select Aeva to Supply Advanced 4D LiDAR Technology for Series-Production Autonomous Trucks", 9 Jan 2024, https://www.aeva.com/press/daimler-truck-and-torc-robotics-select-aeva-to-supply-advanced-4d-lidar-technology-for-series-production-autonomous-trucks/; Aeva, C-sample release, 6 May 2026, https://www.aeva.com/press/aeva-delivers-atlas-c-samples-to-daimler-truck-for-autonomous-truck-production-program/ (both read in full).
  - Tower Semiconductor, "Tower Semiconductor Partners with LightIC to Expand Silicon Photonics Beyond AI Infrastructure into Physical AI and Automotive", 5 Jan 2026, https://towersemi.com/2026/01/05/01052026/ (read in full).
  - LuminWave (洛微科技), Raptor release, 10 Sep 2024, https://luminwave.com.cn/fully-integrated-silicon-optical-chip/; nomination release, 8 Jul 2025, https://luminwave.com.cn/heavy-duty-truck-autonomous-driving-project/ (both read in full, in Chinese).
- **Evidence tag:** [P] for all five (the Aeva call statements are the company's own words, read in a third-party transcript)
- **Confidence:** high for SiLC, LightIC, LuminWave and the Daimler 2027 plan; medium-high for the 100k figure, which is a stated expectation and links the call's "automated final assembly line" to the Jabil line named on the next call.
- **Proposed edits:**
  - (a) SiLC, line ≈4526. `old`:
    ```text
    claims more than 1 km for its Eyeonic Vista [P/T] (§B8); Honda has invested in it.
    ```
    `new`:
    ```text
    claims more than 1 km for its Eyeonic Vista [P/T] (§B8). Honda invested in it through its venture arm, Honda Xcelerator Ventures, in September 2024, for an undisclosed amount [P].
    ```
  - (b) Aeva, line ≈4516. `old`:
    ```text
    has an automated line at the contract manufacturer Jabil with a capacity of about 100k units per year, and the Daimler launch is planned for 2027.
    ```
    `new`:
    ```text
    began production in 2026 on a fully automated final-assembly line at the contract manufacturer Jabil in North America, which it expects to reach 100,000 systems a year [P, Aeva earnings calls of 26 Feb and 12 Aug 2026], and the program plans Daimler Truck's production ramp for 2027 [P, Aeva–Daimler Truck release, 9 Jan 2024].
    ```
  - (c) LightIC, line ≈4528. `old`:
    ```text
    builds its Lark lidar on silicon photonics made by the foundry Tower Semiconductor, with what it calls
    ```
    `new`:
    ```text
    builds its Lark lidar on the silicon-photonics foundry platform of Tower Semiconductor [P, Tower Semiconductor, 5 Jan 2026], with what it calls
    ```
  - (d) LuminWave, line ≈4530. `old`:
    ```text
    with more than 10 GHz of FM bandwidth, i.e. optical frequency sweep. Its July 2025 heavy-truck nomination (selection for a truck program) names no product, customer or start of production, and does not say FMCW (§D7).
    ```
    `new`:
    ```text
    with more than 10 GHz of FM bandwidth, i.e. optical frequency sweep [P, LuminWave, 10 Sep 2024]. Its heavy-truck nomination of 8 July 2025 (selection for a truck program) names no product, customer or start of production, and does not say FMCW [P, LuminWave, 8 Jul 2025] (§D7).
    ```
- **Appendix 2 entry:** (group *FMCW and beam steering*; the Raptor page is already listed as "LuminWave integrated chip")
  - `- Honda Xcelerator Ventures, investment in SiLC (10 Sep 2024): https://xcelerator.hondainnovations.com/honda-xcelerator-ventures-is-excited-to-announce-our-new-partnership-with-silc-technologies/`
  - `- Aeva Q4 2025 earnings call, automated final-assembly line for 100,000 systems a year (transcript, 26 Feb 2026): https://www.fool.com/earnings/call-transcripts/2026/02/26/aeva-aeva-q4-2025-earnings-call-transcript/`
  - `- Aeva Q2 2026 earnings call, production started on the Jabil North America line (transcript, 12 Aug 2026): https://www.fool.com/earnings/call-transcripts/2026/08/12/aeva-aeva-q2-2026-earnings-call-transcript/`
  - `- Aeva–Daimler Truck series-production selection, Daimler ramp by 2027 (9 Jan 2024): https://www.aeva.com/press/daimler-truck-and-torc-robotics-select-aeva-to-supply-advanced-4d-lidar-technology-for-series-production-autonomous-trucks/`
  - `- Tower Semiconductor–LightIC silicon-photonics collaboration (5 Jan 2026): https://towersemi.com/2026/01/05/01052026/`
  - `- LuminWave heavy-truck L2+ series nomination (8 Jul 2025): https://luminwave.com.cn/heavy-duty-truck-autonomous-driving-project/`

---

## R4_C7-C7b_F6-04

- **Question:** Is there a datasheet or survey source for "Commercial distributed-feedback lasers (DFBs) reach tens of kHz"?
- **Answer:** Yes, for narrow-linewidth grades; standard DFBs are far broader.
  - AeroDIODE's 1550LD-5-SM/PM-II (≥20 mW CW) and 1550LD-6-SM/PM-II (≥40 mW CW), single-frequency DFBs in 14-pin butterfly packages, are both specified at a spectral width (FWHM) of "< 50" kHz typical, with the footnote "Phase noise method - 1 MHz", i.e. derived from the frequency noise at 1 MHz offset; case operating range −20 to 60 °C.
  - Waymo writes that "several vendors provide distributed-feedback (DFBs) lasers with linewidths in the low tens of kHz" (Piggott et al. 2025, p. 13).
  - For contrast, the "state-of-the-art commercial DFB" that Bianconi et al. measured shows 802 kHz over 1 ms (Table 1), with a white frequency-noise floor near $2\times10^{5}$ Hz²/Hz above about 200 kHz in their Fig. 1(c), i.e. a Lorentzian width of about $\pi\times2\times10^{5}\approx0.6$ MHz. Through the report's Eq. (109) that spectrum costs ≈31 dB at 300 m ($T_u=7.5$ µs, `scripts/R4_coherent_loss.py`). The tens-of-kHz figure therefore applies to selected narrow-linewidth parts, not to DFBs in general.
  - The phase-noise-at-1 MHz convention is the right one for Eq. (110): Eq. (109) weights Fourier frequencies from $1/T_u\approx0.1$ MHz to a few MHz.
  - *The integrated lasers in the same bullet (item 07).* Bianconi's 42 kHz and 378 kHz are linewidths over 1 ms, obtained by integrating the frequency noise above the β-separation line down to the integration time (Siddharth et al., Methods C; Bianconi Fig. 1(c), where the shaded areas end near 0.8 kHz, 60 kHz and 700 kHz for the SIL, E-DBR and DFB). They are set by noise below about 60 kHz, which Eq. (109) leaves out. The intrinsic linewidths are 3 Hz for the SIL laser (Voloshin et al., Fig. 2(a)) and 2.8 kHz for the E-DBR laser (Siddharth et al.: 800 Hz²/Hz at 2 MHz, $\pi S_0=2.8$ kHz). Inserting the measured spectra in Eq. (109), with $\tau=2R/c=2.0$ µs at 300 m and the lower limit $1/T_u$:
    - E-DBR, spectrum of Siddharth Fig. 3(d), $S_\nu(f)=891+10^{6}(f/1\ {\rm kHz})^{-1.18}$ Hz²/Hz: $\sigma^2=0.049$, $\eta_{\rm coh}=e^{-0.049}=0.952$, a loss of 0.21 dB at $T_u=7.5$ µs; 0.46 dB at $T_u=16$ µs;
    - E-DBR, spectrum of Bianconi Fig. 1(c), $S_\nu(f)=1.2\times10^{3}+10^{4}(f/100\ {\rm kHz})^{-1.25}$ Hz²/Hz: 0.40 dB at 7.5 µs; 0.93 dB at 16 µs;
    - SIL, Bianconi Fig. 1(c), $S_\nu(f)=2+15(f/100\ {\rm kHz})^{-0.85}$ Hz²/Hz: $\sigma^2=2\times10^{-4}$, below 0.01 dB;
    - the white floors alone, $2\pi\Delta\nu\tau$: $2\pi\times2.8\times10^{3}\times2.0\times10^{-6}=0.035$, i.e. 0.15 dB for the E-DBR laser, and $3.8\times10^{-5}$ for the SIL laser.
    The report's shortcut inserts the 1 ms values as Lorentzian widths: $2\pi\times378\times10^{3}\times2.0\times10^{-6}=4.75$, i.e. 21 dB, and $2\pi\times42\times10^{3}\times2.0\times10^{-6}=0.53$, i.e. 2.3 dB. The spectra were read by eye from the published figures (good to a factor of about 1.5 in $S_\nu$), so the measured-spectrum losses are 0.2–0.4 dB (E-DBR) and below 0.01 dB (SIL) to that accuracy.
- **Source:** AeroDIODE, "1550 nm laser diode – DFB, Model 5: Special Narrow Bandwidth version with >20 mW", reference 1550LD-5-SM/PM-II, datasheet PN_A75, rev. 04/26, p. 1 (specification table and footnote), and "Model 6 … >40 mW", reference 1550LD-6-SM/PM-II, datasheet PN_A79, rev. 04/26, p. 1; both 2-page PDFs read in full, hosted by the distributor Laser Diode Source: https://shop.laserdiodesource.com/wp-content/uploads/2025/04/1550-nm-laser-diode-Model-5-20-mW-Datasheet.pdf and https://shop.laserdiodesource.com/wp-content/uploads/2025/04/1550-nm-laser-diode-Model-6-40-mW-Datasheet.pdf (AeroDIODE's own site refused automated requests). Piggott et al. 2025 (item 01), p. 13. Bianconi et al. 2025 (item 02), Table 1 and Fig. 1(c). Siddharth et al. (arXiv:2408.01743v1), p. 4, Fig. 3(d) and Methods C. Voloshin et al. (arXiv:2411.19264v1), pp. 3–4 and Fig. 2(a).
- **Evidence tag:** [P] for the DFB claim (manufacturer datasheets and Waymo); [I] for the laser papers; [E] for the loss calculation
- **Confidence:** high for the datasheet figure and the 1 ms definitions; medium for the loss values, which rest on spectra read from figures (the conclusion, under 1 dB against 21 dB, is robust to that).
- **Proposed edit (also carries item 07's E-DBR expansion at its first use):**
  - `old`:
    ```text
    Commercial distributed-feedback lasers (DFBs) reach tens of kHz. At 300 m the SiN self-injection-locked laser below (42 kHz) loses 2.3 dB and the TFLN E-DBR laser (378 kHz) 21 dB [E].
    ```
  - `new`:
    ```text
    Narrow-linewidth grades of commercial distributed-feedback lasers (DFBs) reach tens of kHz: AeroDIODE specifies its 20 mW and 40 mW 1550 nm butterfly DFBs at <50 kHz, measured by the phase-noise method at 1 MHz [P, AeroDIODE datasheets PN_A75 and PN_A79, 2026], and Waymo notes that several vendors offer DFBs with linewidths in the low tens of kHz [P, Piggott et al. 2025]. A standard commercial DFB measured by Bianconi et al. showed 802 kHz over 1 ms [I]. The integrated lasers below are quoted with linewidths over 1 ms, which slow frequency noise dominates. The SiN self-injection-locked laser (42 kHz over 1 ms) has a 3 Hz intrinsic linewidth [I, Voloshin et al. 2025], and the TFLN extended distributed Bragg reflector (E-DBR) laser (378 kHz over 1 ms) one of 2.8 kHz [I, Siddharth et al. 2025]. Taken as Lorentzian widths in Eq. (110), the 1 ms values would cost 2.3 dB and 21 dB at 300 m, but the lasers' measured frequency-noise spectra in Eq. (109) give less than 0.01 dB and about 0.2–0.4 dB (up to ≈0.9 dB for a 16 µs useful window) [E].
    ```
- **Appendix 2 entry:** (group *FMCW and beam steering*)
  - `- AeroDIODE 1550LD-5/-6 narrow-linewidth DFB datasheets (<50 kHz by the phase-noise method at 1 MHz; PN_A75, PN_A79, rev. 04/26): https://shop.laserdiodesource.com/wp-content/uploads/2025/04/1550-nm-laser-diode-Model-5-20-mW-Datasheet.pdf ; https://shop.laserdiodesource.com/wp-content/uploads/2025/04/1550-nm-laser-diode-Model-6-40-mW-Datasheet.pdf`

---

## R4_C7-C7b_F6-05

- **Question:** What dated source fixes the start of the "192 → 520 → 896 → 2,160 → 4,320 lines in five years" race?
- **Answer:** The product race is much shorter than five years. The first 192-line Chinese automotive lidar was Huawei's D3, launched on 26 Dec 2023 (the Aito M9 launch; the M9 and Luxeed S7 were its first cars). The 4,320 end is Hesai's next-generation ETX, shown at its Technology Open Day on 17 Apr 2026 "with 1,080, 2,160, and up to 4,320 channels". That is $2026.29-2023.98\approx2.3$ years. Counted instead from Sony's IMX459 (announced 6 Sep 2021, samples planned for March 2022), whose 3×3 ToF unit gives the report's 192 lines [E, §C5a], the span is about 4.6 years; but the sentence speaks of the Chinese race, i.e. products. Sony's release gives 597 × 168 effective pixels and the 3×3 unit, not a line count.
- **Source:** 汽车之心 (Autobit), 安富建, "这匹'黑马'拿下激光雷达销冠，一点也不意外", 21 Jun 2024, https://www.autobit.xyz/news/3986.html (also on Autohome 车家号): states that Huawei released its 192-line lidar on 26 Dec 2023 and names it D3 (read in full, in Chinese). CnEVPost, "Huawei-backed Aito officially launches M9 SUV…", 26 Dec 2023, https://cnevpost.com/2023/12/26/huawei-backed-aito-officially-launches-m9/ (launch date). Hesai, "Hesai Unveils Picasso 6D Full-Color SPAD-SoC, Next-Gen ETX…", 20 Apr 2026, https://www.hesaitech.com/hesai-unveils-picasso-6d-full-color-spad-soc-next-gen-etx-and-innovations-in-spatial-intelligence-and-physical-ai/ (read in full). Sony Semiconductor Solutions, IMX459 release, 6 Sep 2021, https://www.sony-semicon.com/en/news/2021/2021090601.html (read in full).
- **Evidence tag:** [T] for the D3 launch date; [P] for Hesai's 4,320 channels
- **Confidence:** medium-high — the D3 date comes from trade press (no Huawei primary page found), but it matches the M9 launch and the April 2024 sales ramp the same article reports.
- **Proposed edit:**
  - `old`:
    ```text
    This is why the Chinese race went 192 → 520 → 896 → 2,160 → 4,320 lines in five years.
    ```
  - `new`:
    ```text
    This is why the Chinese race went 192 → 520 → 896 → 2,160 → 4,320 lines in under two and a half years, from Huawei's 192-line D3, launched on 26 Dec 2023 [T], to Hesai's ETX with up to 4,320 channels, shown on 17 Apr 2026 [P].
    ```
- **Appendix 2 entry:** (group *Technology routes and SPAD*; Hesai's release is already listed as "Hesai Picasso / ETX")
  - `- 汽车之心 (Autobit), Huawei 192-line lidar D3 launched 26 Dec 2023 (21 Jun 2024): https://www.autobit.xyz/news/3986.html`

---

## R4_C7-C7b_F6-06

- **Question:** What are the sources for "about 25 driverless trucks in mid-2026" and for the \$80 M annualized revenue?
- **Answer:** No primary source gives a mid-2026 count of 25; the primary documents give a fleet history and a target instead.
  - Q4 2025 letter (11 Feb 2026): "We expanded driverless operations to 10 trucks in December", and Aurora then reduced that fleet in early 2026 to prepare its second-generation fleet.
  - Q1 2026 letter (6 May 2026) and investor-day release (23 Sep 2026): no current count.
  - Q2 2026 letter (29 Jul 2026): the second-generation fleet on International LT trucks was launched "last week", and Aurora expects "20-25 second-generation driverless trucks in operation by the end of the third quarter". The report's 25 is the top of this target, not a mid-2026 count; §B4 already reports it as a target.
  - CNBC (22 Sep 2026): "With 20 driverless trucks currently on the road" — the trade report the report cites.
  - The \$80 M: the Q2 2026 letter expects Aurora to exit 2026 with more than 200 driverless trucks, which "translates to an approximately \$80 million revenue run-rate for our TaaS business"; the Q4 2025 and Q1 2026 letters say the same. It is a year-end run-rate for Transportation as a Service, not a forecast of annual revenue; 2026 revenue guidance is \$14–16 M. Per truck, $80\times10^{6}/200=4\times10^{5}$ \$ a year.
- **Source:** Aurora Innovation, Fourth Quarter 2025 Shareholder Letter, 11 Feb 2026, SEC 8-K exhibit, https://www.sec.gov/Archives/edgar/data/1828108/000182810826000014/finalaurora25q4sharehold.htm; First Quarter 2026 letter, 6 May 2026, https://www.sec.gov/Archives/edgar/data/0001828108/000182810826000050/aurora26q1shareholderlet.htm; Second Quarter 2026 letter, 29 Jul 2026, https://www.sec.gov/Archives/edgar/data/0001828108/000182810826000075/aurora26q2shareholderlet.htm; investor-day release, 23 Sep 2026, https://www.sec.gov/Archives/edgar/data/0001828108/000182810826000082/businesswire-aurora2026ana.htm. All four read in full through Aurora's investor-relations copies of the same filings (ir.aurora.tech; SEC refuses requests that do not declare an email address). P. LeBeau, "Autonomous trucking company Aurora looks to accelerate toward profitability", CNBC, 22 Sep 2026, https://www.cnbc.com/2026/09/22/aurora-autonomous-semi-ride.html (read in full).
- **Evidence tag:** [P] for the fleet history, the target and the run-rate; [T] for CNBC's count
- **Confidence:** high — quoted from the filings; the only judgement is that "about 25" was taken from the end-Q3 target.
- **Proposed edit:**
  - `old`:
    ```text
    Aurora had about 25 driverless trucks in mid-2026 across all generations (no count in the investor-day release below; one trade report says about 20 [T, single source]). It targets 200 by year-end 2026 [P], for about \$80 M annualized revenue.
    ```
  - `new`:
    ```text
    Aurora ran 10 driverless trucks in December 2025 and reduced that fleet in early 2026 to prepare a second-generation fleet [P, Q4 2025 shareholder letter]. It launched that fleet in late July 2026 and expected 20–25 second-generation driverless trucks by the end of September [P, Q2 2026 shareholder letter]; CNBC reported 20 on the road on 22 Sep 2026 [T]. It targets more than 200 by year-end 2026, which it says translates to a revenue run-rate of about \$80 M a year for its Transportation-as-a-Service business [P, Q2 2026 shareholder letter].
    ```
- **Appendix 2 entry:** (group *Robotaxi and trucks*; the Q2 2026 letter is already listed)
  - `- Aurora Q4 2025 shareholder letter, 10 driverless trucks in December 2025 (8-K, 11 Feb 2026): https://www.sec.gov/Archives/edgar/data/1828108/000182810826000014/finalaurora25q4sharehold.htm`
  - `- CNBC, Aurora driverless ride and fleet of 20 trucks (22 Sep 2026): https://www.cnbc.com/2026/09/22/aurora-autonomous-semi-ride.html`

---

## R4_C7-C7b_F6-07

- **Question:** What does "E-DBR" stand for in Bianconi et al. (2025), so that it can be spelled out at first use?
- **Answer:** "Extended distributed Bragg reflector": Bianconi et al. describe an external-cavity integrated laser "based on extended distributed Bragg reflector (E-DBR) in lithium niobate", and Table 1's footnote reads "E-DBR extended distributed Bragg reflector laser". Siddharth et al., who built the laser, use the same expansion in their abstract; the device is an InP reflective SOA butt-coupled to a 7.25 mm Bragg grating with gold electrodes on 400 nm X-cut thin-film LiNbO₃ (LNOI), tuned by the Pockels effect. The first use in the report is §C7a(f), line ≈4843 (TFLN is spelled out earlier, at line ≈4668), so the expansion is written there, inside the item-04 edit of the same bullet.
  - *Related finding (edits 07b).* The 378 kHz that the report uses is a linewidth over 1 ms, not a Lorentzian width (see item 04): with the laser's measured spectra, Eq. (109) gives about 0.2–0.4 dB at 300 m, not 21 dB, so "unusable at 300 m" in §C7b 2(e) does not hold for this laser. The same applies to the 42 kHz self-injection-locked laser in the line above it (below 0.01 dB rather than 2.3 dB). The edits keep the Lorentzian arithmetic as a reading of the 1 ms numbers and add what the measured noise gives. The generic "42 kHz laser" in §C7b 3a (line ≈5347) is a sensitivity case not tied to that laser and needs no change.
- **Source:** Bianconi et al. 2025 (item 02), Fig. 1 caption and Table 1 footnote; Siddharth et al., arXiv:2408.01743v1, abstract, Fig. 1 and §II (pp. 1–3); spectra as in item 04.
- **Evidence tag:** [I]
- **Confidence:** high — the expansion appears verbatim in both papers.
- **Proposed edit (07, expansion):** included in the item-04 edit (line ≈4843): "the TFLN extended distributed Bragg reflector (E-DBR) laser".
- **Proposed edits (07b, related finding):**
  - (a) line ≈5184. `old`:
    ```text
    42 kHz (SiN self-injection-locked laser): 0.528, $\eta_{\rm coh}=0.59$ (−2.3 dB), energy ×1.7;
    ```
    `new`:
    ```text
    42 kHz, taken as a Lorentzian width (the SiN self-injection-locked laser's linewidth over 1 ms; its measured frequency noise gives less than 0.01 dB, §C7a(f)): 0.528, $\eta_{\rm coh}=0.59$ (−2.3 dB), energy ×1.7;
    ```
  - (b) line ≈5186. `old`:
    ```text
    378 kHz (TFLN E-DBR laser): 4.75, $\eta_{\rm coh}=0.0087$ (−21 dB), energy ×116: unusable at 300 m.
    ```
    `new`:
    ```text
    378 kHz, taken as a Lorentzian width (the TFLN E-DBR laser's linewidth over 1 ms): 4.75, $\eta_{\rm coh}=0.0087$ (−21 dB), energy ×116. The laser itself does far better: its measured frequency noise, a 2.8 kHz white floor plus slower thermal noise, gives about 0.2–0.4 dB at 300 m through Eq. (109) (§C7a(f)) [E].
    ```
- **Appendix 2 entry:** none beyond item 02's three lines.

---

## R4_C7-C7b_F6-08

- **Question:** Are the 0.65% and 1.5% fractional chirp-rate errors $\varepsilon$ or frequency deviations $\delta\nu/B$, and how much worse are they under Eq. (108) if they are deviations?
- **Answer:** Neither as the report reads them: they are RMS frequency deviations divided by the sweep excursion, $\sigma=\delta\nu_{\rm rms}/B$ (item 02). Under the report's parabolic bow, $\delta\nu_{\max}=(3\sqrt5/2)\,\sigma B=3.35\,\sigma B$, and Eq. (108) in chirp-rate form gives $\varepsilon=8\delta\nu_{\max}/B=12\sqrt5\,\sigma=26.8\,\sigma$, not $8\sigma$. Relative to reading the percentages as $\varepsilon$, they are therefore about 27× worse, and relative to reading them as peak deviations $\delta\nu_{\max}/B$, 3.35× worse. Substituting at $B=1$ GHz and 300 m: 0.65% → $\varepsilon=26.8\times0.0065=0.174$, i.e. $0.174/(5\times10^{-4})=349\times$ the tolerance; 1.5% → $\varepsilon=0.40$, $805\times$; the packaged SIL's 0.08% → $\varepsilon=0.021$, $43\times$. The same ratios follow from $\delta\nu_{\max}$ against $c/(16R)=62.5$ kHz (21.8, 50.3 and 2.68 MHz). These assume the measured fractions carry over to a 1 GHz sweep; they were measured over 500 MHz (SIL, unpackaged), 210 MHz (SIL, packaged) and 10.5 GHz (E-DBR).
- **Source:** as item 02 (Bianconi et al. 2025, Supplementary Eq. (4); Voloshin et al., Fig. 4; Siddharth et al., Fig. 3(f)); arithmetic in `scripts/R4_waymo_and_linearity_check.py`.
- **Evidence tag:** [I] for the definition; [E] for the conversion
- **Confidence:** high for the definition and the bow conversion; medium for applying the fractions to a 1 GHz sweep.
- **Proposed edit:** the item-02 edit (one combined edit of the same sentences).
- **Appendix 2 entry:** none beyond item 02.
