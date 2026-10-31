# Short-Wave Infrared Image Sensors
## A side note to *Automotive Night Vision, Lidar and the Sensor Debate*: technologies, a detectivity check, and the automotive case

::: {.disclaimer}
**Disclaimer.** This side note was prepared with significant AI assistance. It may contain errors: each statement carries an evidence tag and, where possible, a source, so check those before relying on a figure.
:::

---

### A side note, and its verdict for cars

This is a side note to the report *Automotive Night Vision, Lidar and the Sensor Debate* (https://photonzq.github.io/automotive-lidar-report/). It reflects sources available in October 2026, and it changes none of that report's conclusions. Its verdict is that short-wave infrared (SWIR) cameras are unlikely to matter for automotive perception at this stage, that is, in the vehicle programmes now being developed. Four findings support the verdict.

1. **A SWIR camera offers a car little that it cannot already buy.** At night the scene gives off little SWIR light of its own, so the camera needs its own illuminator, and fog scatters SWIR light about as strongly as visible light (§S1.1, §S1.2).
   - As a night-vision sensor it therefore competes with thermal cameras, which need no illumination and are already fitted to series cars (main report §A1). In the fog tests of Bertozzi et al., SWIR did not improve pedestrian detection, and the authors judged thermal imagers the most effective option. A 2025 chamber study shows one fog scene in which SWIR images revealed a person and a car that an RGB camera missed, but it compared SWIR with visible light, not with thermal imaging (§S1.2).
   - As an active imager it competes with gated near-infrared cameras, which use silicon, and with lidar (§S4).
2. **Each route that could become cheap enough fails an automotive requirement today.**
   - Germanium on silicon leaks about 200 µA cm⁻² at room temperature (§S3.2).
   - The PbS quantum-dot product reaches only about 10% quantum efficiency at 1,550 nm, and the exemption list of the End-of-Life Vehicles Directive, as it stood at the end of 2020, has no entry for lead in infrared detectors (§S3.3, §S3.6).
   - Lead-free InAs dots leak about 10⁴ times more than PbS dots of almost the same band gap (§S3.3).
   - InGaAs gives the best images, but its processed InP costs 10–100 times as much as silicon per mm², before the cost of joining it to the readout chip (§S3.1).
3. **No sensor has been shown to work in a hot car.** No thin-film sensor has published its dark current at the 85–105 °C at which an automotive sensor must still work, and even standard InGaAs leaks about 1,700 times more at 100 °C than at 25 °C (§S1.3). How much light windshields pass at 1.3–1.6 µm, and what other cars' 1,550 nm lidars do to SWIR pixels, are also unknown (§S4, §S5).
4. **No carmaker has committed.** No SWIR camera is in a series-production car. TriEye, the one supplier with an automotive-oriented SWIR product, lists Porsche as an investor, an evaluation by Denso and a collaboration with Hitachi Astemo, but no series programme is public (§S3.2; main report §A7.5).

The verdict would change if a sensor made in a silicon fab published usable dark current and quantum efficiency at 105 °C, if lead-free dots matched the leakage of PbS dots or lead in infrared detectors gained an automotive exemption, or if a carmaker sourced a gated SWIR camera such as TriEye's. It concerns cameras only: SWIR photodiodes and avalanche detectors in the receivers of 1,550 nm lidars are a separate matter, treated in the main report (§C4b, §C4c).

The rest of this side note gives the evidence. Its longest part, §S2, checks the detectivity that Li et al. (*Nature* 2026) report for a PbS photodiode grown on its readout chip; that check bears on SWIR detectors in general rather than on cars.

### How to read this side note

This side note surveys short-wave infrared (SWIR) image sensors, the cameras that detect light between the absorption edge of silicon near 1.1 µm and about 2.5 µm, with the use in cars weighted most. The main report treats SWIR where it meets lidar and night vision, and those passages are not repeated here: TriEye's germanium sensor, gated SWIR imaging, passive SWIR at night and SWIR in fog (§A7.5); the economics of InGaAs (§C4c subsection 3); germanium-on-silicon photodiodes and SPADs (§C4c subsection 4); water and fog (§C4c subsection 5); and camera damage by 1,550 nm lidar (§C4c subsection 1). Section numbers here start with S to keep them apart from those of the main report.

It has a survey part and a check of one paper. §S1 sets out what an automotive SWIR camera has to do and the physics behind it. §S2 tests the detectivity that Li et al. (*Nature* 2026) report for a PbS photodiode grown directly on its readout chip, against the paper's figures, its Supplementary Information, its Source Data, its Peer Review File and the instruments the authors used, and §S2.8 sets out how such a diode can be measured. §S3 surveys the sensor routes and, in §S3.6, how the European rules on lead apply to them; §S4 gives the automotive outlook, and §S5 lists what deserves a deeper look. Five papers behind §S3 were read in full, the HgTe review except its reference list: the quantum-dot sensors of imec (Chu et al., *Sensors* 2025), Sony (Enoki et al., IEDM 2024) and SWIR Vision Systems (Gregory et al., Proc. SPIE 2022), the megapixel HgTe imager of Luo et al. (*APL Photonics* 2023) and the HgTe review of Sergeeva et al. (*Adv. Funct. Mater.* 2024). Elsewhere the survey is a first pass: unless a statement cites a page or a figure, it rests on datasheets, press releases, abstracts or search extracts, and the tags say which.

**Evidence tags** follow the main report. A tag in square brackets after a statement says what kind of source supports it, and text after the tag inside the brackets gives the arithmetic or names the source.

| Tag | Meaning |
|---|---|
| **[P]** | Primary document: datasheet, manual, press release, patent or company filing. A company claim is *primary* but not *independent*. |
| **[I]** | Independent: peer-reviewed paper, conference paper, test body. |
| **[T]** | Trade press. |
| **[E]** | Own estimate or calculation; assumptions are stated. |
| **[U]** | Unverified; a lead, not a fact. |
| **[S]** | Secondary: a value read from a search-result extract or a review table rather than the original source. |

Equations are numbered within this side note. Page numbers of the Supplementary Information of Li et al. are its printed page numbers; page numbers of its Peer Review File are PDF pages.

---

## S0. Main findings

1. **The detectivity of Li et al. is overstated by a factor of at least 2, and most likely by about 2.6.** At zero bias and in the dark a photodiode is in thermal equilibrium, so its noise current cannot fall below the Johnson noise of its zero-bias resistance. The dark current that the authors report for the same 1 mm² diode, 123.0 µA cm⁻² at −0.1 V, puts that floor at no less than 4.5×10⁻¹³ A Hz⁻¹ᐟ², twice the 2.19×10⁻¹³ A Hz⁻¹ᐟ² on which the 4.4×10¹¹ Jones rests. The diode can therefore reach at most 2.2×10¹¹ Jones at 2.5 µm, and 1.6–1.7×10¹¹ Jones once the diode current that the authors' own fit draws is included (§S2.3). Neither an offset voltage in the instruments, the frequency of the measurement nor the device area can close the gap (§S2.4). Detailed balance gives the same verdict independently: the reported noise would need the PbS film to emit light with an external radiative efficiency of at least 12%, 17 times what its own dark current requires (§S2.3).
2. **The noise measurement cannot be checked as described.** At the stated gain of 10⁸ V/A, the SR570 current preamplifier has a bandwidth of 200 Hz in its default Low Noise mode and 2 kHz in High Bandwidth mode, and a physical 10 kΩ input resistor. Its manual specifies these figures for a 100 pF source and asks for a source impedance above 100 MΩ at that gain, while the PbS diode presents about 3 nF and 50–80 kΩ. The instrument's own noise at that range is 60–100 fA Hz⁻¹ᐟ², not the 5 fA Hz⁻¹ᐟ² the rebuttal cites, and it is included in the reported total, so it cannot be what makes the reading too low. The paper gives no settings and no calibration with a known noise source of the diode's impedance. Its decomposition of the noise into shot, generation–recombination and 1/f terms assumes a dark current that does not flow at zero bias, and it omits the thermal term that should dominate (§S2.5). §S2.8 sets out a measurement that avoids these problems.
3. **The InGaAs benchmark moved during review while the PbS number did not.** In the first rebuttal the authors measured a commercial 2.6 µm-cut-off InGaAs photodiode at 1.7×10¹¹ Jones, almost twice its datasheet typical, and called this good agreement. In the second rebuttal the same type measured 9.5×10¹⁰ Jones, which does agree with the datasheet. The corrected PbS value is about twice that InGaAs value at 2.5 µm, not 4.7 times (§S2.6).
4. **What holds in the paper is the materials and integration result.** A PbS photodiode grown from water at room temperature on a CMOS readout chip has an external quantum efficiency above 40% from 0.7 to 2.6 µm and makes a working 640 × 512 imager with reasonable uniformity and sharpness. For cars the 2.85 µm cut-off is the wrong choice: it adds no signal at the 1.3–1.6 µm wavelengths that cars use and costs about three orders of magnitude in zero-bias resistance against standard InGaAs (§S1.3, §S2.7).
5. **Heat, not wavelength, is the automotive SWIR problem.** The zero-bias resistance of a standard InGaAs photodiode halves every ≈7 K. At 100 °C such a diode leaks ≈60 µA cm⁻², the level that germanium on silicon (TriEye, ≈200 µA cm⁻²) and bulk PbS (≈120 µA cm⁻² at −0.1 V) show at room temperature. Every uncooled SWIR camera in a hot car therefore has to integrate briefly under its own illumination (§S1.3).
6. **Among the thin films, PbS quantum dots leak like InGaAs, while lead-free InAs dots leak about 10⁴ times more.**
   - SWIR Vision Systems' PbS dots leak about 5 nA cm⁻² at 25 °C on 15 µm pixels, the level of an InGaAs pixel.
   - InAs dots of almost the same band gap leak 80–100 µA cm⁻² (imec, Sony), the level of germanium on silicon. The way that leakage scales with the band gap points to traps, not to the gap itself (§S1.3, §S3.3).
   - imec's InAs sensor reaches 4.8% EQE at 1,400 nm, and Sony has not yet shown a SWIR image from its InAs sensor.
7. **The commercial routes that suit cars are the ones made in silicon fabs.**
   - These are germanium on silicon (TriEye, made by Tower) and PbS quantum dots coated on CMOS readout wafers (SWIR Vision Systems, bought in July 2024 by onsemi, a supplier of automotive image sensors).
   - The PbS-dot product reaches only about 10% QE at 1,550 nm, against up to 45% claimed for prototypes, and its published reliability data are storage tests, not automotive qualification.
   - Sony's Cu–Cu-bonded InGaAs, with 3.45 µm pixels, gives the best image quality but carries the cost of InP. No SWIR camera is in a series-production car (§S3, §S4).
8. **Lead is a legal hurdle, not a material one.**
   - A VGA array of PbS holds about 0.4 mg of lead, but the PbS film is 87% lead by weight, against a limit of 0.1% per homogeneous material.
   - Cars fall under the End-of-Life Vehicles Directive rather than RoHS. Its exemption list (Annex II) has no entry for infrared detectors, so a PbS camera in a new car would need a new entry (§S3.6).
9. **Several system questions remain open, and each could decide the case.** One is how much light windshields pass at 1.3–1.6 µm. Another is whether SWIR helps in real fog: physics says hardly, while one 2025 chamber study shows a detection benefit. A third is whether 1,550 nm lidars dazzle or damage SWIR cameras, which absorb that light efficiently (§S5).

---

## S1. What an automotive SWIR camera has to do

### S1.1 The band is set by the light sources

At night the scene offers little SWIR light of its own, so a car's SWIR camera images light that the car itself or another car emits. The wavelengths in play are therefore those of the light sources: 1,550 nm for eye-safe pulsed and FMCW lidars, 1,375 nm for TriEye's laser in a solar water-absorption band, and 1,310 nm and 1,135 nm for laser diodes and VCSELs (main report §A7.5, §C4c). All lie below 1.65 µm.

- A standard In₀.₅₃Ga₀.₄₇As absorber, whose response ends near 1.7 µm, covers all of them [P, Hamamatsu G12180 datasheet, p. 1].
- Tensile-strained germanium on silicon covers them too: its direct-gap edge lies near 1,600–1,625 nm at room temperature (main report §C4c subsection 4) [I].
- PbS quantum dots sized for an absorption peak near 1.4 µm cover them as well, as in the sensors of §S3.3.
- Absorbers with a longer cut-off, extended InGaAs to 2.2–2.6 µm or bulk PbS to 2.85 µm, add no automotive signal but add thermal leakage, as §S1.3 quantifies.

**Germanium has a cold-start issue at 1,550 nm.** Its absorption edge moves to shorter wavelengths in the cold, and the main report estimates a loss of about 40% in responsivity at 1,550 nm at −40 °C. At 1,375 nm, TriEye's wavelength, the edge is far away (main report §C4c subsection 4) [I/E].

**Passive SWIR imaging is weak.** On moonless nights the nightglow is about ten times brighter in the SWIR than in the visible. Even so, the SWIR sensors that Fraunhofer IOSB tested in 2015 performed worse than visible cameras at equal f-number, exposure and frame rate (main report §A7.5) [I]. In a car, SWIR is therefore an active-imaging technology, with a lamp or a laser at a chosen wavelength.

### S1.2 Weather: haze yes, fog hardly

**Fog scatters the SWIR about as strongly as the visible.** Fog droplets are larger than both wavelengths, so their extinction is nearly independent of wavelength. Duthon et al. computed that light of 1,000–2,400 nm is about 10% *more* attenuated than visible light, and then only in very dense fog, and that extinction differs by less than 10% between 905 and 1,550 nm (main report §C4c subsection 5) [I].

**Haze and smoke do favour the SWIR.** Particles much smaller than the wavelength scatter with a cross-section that falls steeply with wavelength (as $\lambda^{-4}$ in the Rayleigh limit), so the advantage is real for them.

**Experiments in fog are mixed.** In Bertozzi et al. (2013), SWIR did not improve pedestrian detection in fog, and the authors judged thermal imagers the most effective option (main report §A7.5) [I]. A 2025 study on Cerema's fog-and-rain platform compared an InGaAs and a colloidal-quantum-dot SWIR camera with an RGB camera. It shows a fog example in which a person and a car were detected in the SWIR images but not in the RGB image (Mehra et al., ICCVW 2025) [S]. It is a detection study, not a transmission measurement, and §S5 lists it for a full reading.

**Water on the window costs more in the SWIR.** Liquid water absorbs 10.8–11.9 cm⁻¹ at 1,550 nm, so a 1 mm film on a window transmits 34% one way (main report §C4c subsection 5) [I/E]. A SWIR camera behind a wet window pays this, while a silicon camera at 905 nm loses less than 1%.

### S1.3 Heat sets the dark current, and the dark current sets the exposure

A SWIR photodiode leaks current from carriers that are thermally excited across its band gap or through defect levels inside it, so the leakage rises steeply with temperature. An automotive sensor has to work from −40 to +105 °C, the range used in main report §C4c subsection 6.

**How leakage is quantified.** Datasheets express the leakage of a photodiode by its shunt resistance $R_{\rm sh}$, measured at 10 mV reverse bias, which is in effect the zero-bias resistance $R_0$. Multiplying by the photosensitive area $A$ gives the resistance–area product $R_0A$, a figure of the material and process that does not depend on the size of the diode. For a diode whose dark current follows the diode law,

$$R_0A=\frac{n\,k_BT}{q\,J_0} \label{eq:swir-r0a}$$

Here $k_B$ is Boltzmann's constant, $T$ the absolute temperature, $q$ the electron charge, $J_0$ the saturation current density, and $n$ the ideality factor, which is 1 for diffusion current and up to 2 for generation–recombination current in the depletion region. With $n=1$, $J_0=k_BT/(qR_0A)$ is the leakage current density the diode carries once it is reverse-biased by more than a few $k_BT/q$. That is the number compared in the table.

| Absorber (cut-off) | Device | Measured at 25 °C | $R_0A$ | Leakage $J_0$ at 25 °C | Temperature dependence |
|---|---|---|---|---|---|
| Standard InGaAs (1.7 µm) | Hamamatsu G12180-003A, φ0.3 mm | $R_{\rm sh}$ 1 GΩ typ., 200 MΩ min. [P] | 7.1×10⁵ Ω cm² | 36 nA cm⁻² | $R_{\rm sh}$ halves every ≈7.2 K from −40 to 100 °C; ≈0.76 MΩ at 100 °C, i.e. ≈60 µA cm⁻² [P, plot; E] |
| Standard InGaAs pixel (1.7 µm) | Sony, 5 µm Cu–Cu-bonded pixel (Manda et al., IEDM 2019) | ≈2.5 nA cm⁻² [S: read by imec from the paper's graph] | — | — | Temperature of the value not given |
| Extended InGaAs (2.6 µm) | Hamamatsu G12183-003K, φ0.3 mm | $R_{\rm sh}$ 100 kΩ typ., 20 kΩ min. [P] | 71 Ω cm² | 0.36 mA cm⁻² | 1 MΩ at −10 °C and 2 MΩ at −20 °C (cooled versions), i.e. halving every ≈10 K [P; E] |
| Bulk PbS (2.85 µm) | Li et al., 1 mm² diode | 123.0 µA cm⁻² at −0.1 V [I] | ≤813 Ω cm² (§S2.3) | — | Not reported |
| Ge on Si (≈1.65 µm) | TriEye TES200, 7 µm pixel | 100 pA per pixel [P] | — | 204 µA cm⁻² (main report §A7.5) | Bulk leakage of foundry Ge photodiodes rises 30–40× from 25 to 125 °C (main report §C4c subsection 4) [I] |
| PbS quantum dots (≈1.65 µm) | SWIR Vision Systems Acuros, 15 µm pixel | ≈5 nA cm⁻² below 0.1 V reverse bias [P] | — | — | Not reported. Over more than 1,000 h of storage at 85 °C and 85% relative humidity, test diodes stayed within 76–104% of their initial dark current [P] |
| InAs quantum dots (≈1.35 and ≈1.6 µm) | imec, 768 × 512, 5 µm pixel, −3.2 V | 23.6 and 80 µA cm⁻² [I] | — | — | Measured at room temperature only |
| InAs quantum dots (≈1.6 µm) | Sony test diodes, 1,450 nm peak, −1.5 V | ≈100 µA cm⁻² [I, read by eye] | — | — | Not reported |

*How the numbers are derived* [E]:
- **Areas.** The φ0.3 mm diodes have $A=\pi(0.015\ {\rm cm})^2=7.07\times10^{-4}\ {\rm cm^2}$.
- **Standard InGaAs at 25 °C.** $R_0A=10^{9}\ \Omega\times7.07\times10^{-4}\ {\rm cm^2}=7.1\times10^{5}\ \Omega\,{\rm cm^2}$, and $J_0=0.02569\ {\rm V}/7.07\times10^{5}\ \Omega\,{\rm cm^2}=3.6\times10^{-8}\ {\rm A\,cm^{-2}}$ [P, G12180 datasheet p. 3].
- **Standard InGaAs versus temperature.** The datasheet's shunt-resistance plot runs straight on a logarithmic scale for the φ0.3 mm part, from ≈5.5×10¹¹ Ω at −40 °C to ≈7.6×10⁵ Ω at 100 °C [P, G12180 datasheet p. 5, read by eye]. That is $\log_{10}(5.5\times10^{11}/7.6\times10^{5})/140\ {\rm K}=0.042$ decades per kelvin, or a halving every $\log_{10}2/0.042=7.2$ K.
- **Standard InGaAs at 100 °C.** $R_0A=7.6\times10^{5}\times7.07\times10^{-4}=537\ \Omega\,{\rm cm^2}$ and $k_BT/q=32.2$ mV, so $J_0=0.0322/537=6.0\times10^{-5}\ {\rm A\,cm^{-2}}$. The same slope gives 14 µA cm⁻² at 85 °C and, extrapolated beyond the plot, 0.10 mA cm⁻² at 105 °C.
- **Diffusion theory.** A diffusion-limited $R_0$ varies as $T^{-2}e^{E_g/k_BT}$. For $E_g=0.75$–$0.80$ eV it halves every 6.3–6.7 K near 300 K and every 9.6–10.2 K near 373 K. The datasheet's average of 7.2 K over −40 to 100 °C lies in this range.
- **Extended InGaAs.** $R_0A=10^{5}\times7.07\times10^{-4}=71\ \Omega\,{\rm cm^2}$, so $J_0=0.02569/71=3.6\times10^{-4}\ {\rm A\,cm^{-2}}$ [P, G12183 datasheet p. 3]. A tenfold rise in $R_{\rm sh}$ from 25 to −10 °C is a halving every $35/\log_2 10=10.5$ K. Extrapolated with that slope, $J_0$ would reach ≈23 mA cm⁻² at 85 °C.
- **Germanium.** $10^{-10}\ {\rm A}/(7\times10^{-4}\ {\rm cm})^2=2.04\times10^{-4}\ {\rm A\,cm^{-2}}$.
- **Quantum dots.** SWIR Vision Systems gives about 5 nA cm⁻² at 25 °C for its 15 µm pixels and 200 µm test diodes, at a reverse bias below 0.1 V [P, Gregory et al., p. 2 and Table 2]. imec measures 23.6 and 80 µA cm⁻² on its 5 µm pixels at −3.2 V [I, Chu et al., Table 1]. Sony's 1,450 nm test diodes pass about 10⁻⁴ A cm⁻² at −1.5 V [I, Enoki et al., Fig. 10, read by eye].

**What sets the leakage of a thin film.** Thermodynamics gives every photodiode a floor under its dark saturation current. In equilibrium the diode absorbs the blackbody radiation of its surroundings, and every absorbed photon makes a carrier pair, so

$$J_0\ \ge\ J_{0,{\rm rad}}\ \ge\ q\int{\rm EQE}(\lambda)\,\Phi_{\rm bb}(\lambda,T)\,d\lambda,\qquad \Phi_{\rm bb}(\lambda,T)=\frac{2\pi c}{\lambda^{4}}\,\frac{1}{e^{hc/\lambda k_BT}-1} \label{eq:swir-radiative-floor}$$

Here $J_{0,{\rm rad}}$ is the radiative part of the saturation current, $\Phi_{\rm bb}$ the blackbody photon flux per unit wavelength into one face of the device, $h$ Planck's constant and $c$ the speed of light. The EQE stands in for the absorptance, which can only be larger. The ratio $J_{0,{\rm rad}}/J_0$ is the external radiative efficiency, the fraction of recombination that emits light, which is why the photoluminescence quantum yield of the dots enters their detectivity (Sergeeva et al., p. 5) [I]. At 298 K Eq. \eqref{eq:swir-radiative-floor} gives these floors from each device's own spectrum [E, `detailed_balance.py`]:
- 2.5 pA cm⁻² for SWIR Vision Systems' standard 1.5 µm sensor (Gregory et al., Fig. 1);
- 5.8 pA cm⁻² for its improved test diode (Fig. 3);
- 0.26 nA cm⁻² for its extended-SWIR camera, which responds to 2.1 µm (Fig. 2);
- 0.88 µA cm⁻² for Li et al.'s bulk PbS (Source Data, Fig. 3e; §S2.3).

Three conclusions follow.
- **The 1.5 µm PbS-dot diodes are plausible.** Their 5–8 nA cm⁻² sit 1.4–2×10³ times above their floors, which needs an external radiative efficiency of only 5–7×10⁻⁴.
- **The extended-SWIR figure is doubtful.** The same paper gives dark currents of about 5 nA cm⁻² for diodes that respond to 2.1 µm (p. 2). As $J_0$ that would need an external radiative efficiency of at least 5%, exceptional for PbS dots near 2 µm.
  - The paper gives neither the bias nor a J–V curve for that figure.
  - At a reverse bias of a few $k_BT/q$ or less, the net current is only a fraction of $J_0$, while the noise is still set by $J_0$.
- **Traps, not the gap, set the leakage of InAs dots.**
  - At almost the same band gap, Sony's InAs dots (1,450 nm peak, 0.86 eV) pass about 10⁴ times more current than SWIR Vision Systems' PbS dots (1,480 nm peak, 0.84 eV).
  - Between Sony's two InAs materials, with 940 and 1,450 nm peaks, the dark current at −1.5 V rises by about 5×10³ as the gap narrows by $\Delta E_g=0.46$ eV (Enoki et al., Fig. 10, read by eye).

Leakage generated through mid-gap traps scales as

$$\frac{J_{d,2}}{J_{d,1}}\approx e^{\Delta E_g/2k_BT} \label{eq:swir-gr-scaling}$$

where $J_{d,1}$ and $J_{d,2}$ are the dark currents of the wider-gap and the narrower-gap material. It gives $e^{0.46/0.0514}=8\times10^{3}$ at 298 K, against $e^{\Delta E_g/k_BT}=7\times10^{7}$ for diffusion across the full gap [E]. The InAs leakage therefore behaves like trap-mediated generation, a matter of material quality that chemistry may improve, not a limit set by the band gap.

**No thin film has published leakage at automotive temperatures.** If the leakage of PbS dots were thermally activated like that of standard InGaAs, halving every 7–10 K, then 5 nA cm⁻² at 25 °C would become $5\ {\rm nA\,cm^{-2}}\times2^{80/10}=1.3\ \mu{\rm A\,cm^{-2}}$ to $5\ {\rm nA\,cm^{-2}}\times2^{80/7.2}=11\ \mu{\rm A\,cm^{-2}}$ at 105 °C. That would still lie far below germanium at room temperature, but it is a condition, not a measurement: the sources read report storage tests only (§S3.3).

**What this means for a pixel.** A pixel of pitch $p$ (square, with full fill factor) integrating for a time $t$ collects

$$N_d=\frac{J\,p^2\,t}{q} \label{eq:swir-dark-electrons}$$

dark electrons. Per millisecond, Eq. \eqref{eq:swir-dark-electrons} gives these counts [E]:
- A standard InGaAs pixel collects 57 electrons at 25 °C and 9.4×10⁴ at 100 °C at 5 µm pitch, and 510 and 8.4×10⁵ at 15 µm.
- A TES200 germanium pixel at 25 °C collects 6.2×10⁵.
- A 15 µm PbS-dot pixel at 5 nA cm⁻² collects 70 electrons per ms at 25 °C.
- A 5 µm imec InAs pixel collects 3.7×10⁴ (1,200 nm stack) and 1.25×10⁵ (1,400 nm stack); the latter fills imec's 71.9 ke⁻ high-gain well in 0.58 ms.
- A 15 µm pixel of Li et al.'s PbS at −0.1 V collects 1.7×10⁶.

For example, $6.0\times10^{-5}\ {\rm A\,cm^{-2}}\times(15\times10^{-4}\ {\rm cm})^2\times10^{-3}\ {\rm s}/1.602\times10^{-19}\ {\rm C}=8.4\times10^{5}$.

A 15 µm InGaAs pixel at 100 °C would fill a 440,000-electron well in about 0.5 ms; 440,000 electrons is the TES200's full well (main report §A7.5). Standard InGaAs therefore buys about three orders of magnitude of margin at room temperature, and loses it in a hot car. Every uncooled SWIR route then has to integrate briefly under its own illumination, as TriEye does with gated exposures (main report §A7.5), or else cool the sensor.

The datasheet values are for discrete φ0.3 mm photodiodes. Pixels of 5–15 µm leak differently, through their edges and passivation, so measured array dark current at temperature is an item for §S5.

---

## S2. The PbS imager of Li et al. (*Nature* 2026): what holds and how far the detectivity is overstated

### S2.1 What the paper reports

Sen Li, Jing Liu, Liang Gao and colleagues in Jiang Tang's group (Wuhan National Laboratory for Optoelectronics) grow a PbS photodiode directly on a CMOS readout integrated circuit (ROIC) from an aqueous bath at room temperature, a process they call monolithic in situ integration (MISI). The paper is "Monolithically and in situ integrated PbS infrared imagers", *Nature*, doi:10.1038/s41586-026-11222-y, received 16 August 2025 and accepted 24 September 2026, here read as the accelerated article preview [I].

- **Material.** The film grows in a narrow pH window with millikelvin thermal and microscale vibrational stabilization. It is p-type at about 2×10¹⁵ cm⁻³, has a Hall mobility of 124 cm² V⁻¹ s⁻¹ and an optical band gap of about 0.45 eV (p. 5) [I].
- **Diode.** An Sb-doped n-type top layer makes an ITO/500 nm p-PbS/300 nm n-PbS/Al homojunction (p. 6).
  - The external quantum efficiency (EQE) exceeds 40% from 0.7 to 2.6 µm (Fig. 3e). In the Source Data it is 67.8% at 1,300 nm, 64.5% at 1,550 nm, 48.4% at 2,500 nm and 41.9% at 2,640 nm [I].
  - The 1 mm² diode has a −3 dB bandwidth of about 200 kHz (Fig. 3d) and a linear dynamic range above 120 dB (Fig. 3c).
  - Its headline is a specific detectivity of 4.4×10¹¹ Jones at 2.5 µm, "surpassing commercial InGaAs detectors" (abstract, p. 1; p. 7; Fig. 3f) [I].
- **Imager.** The 640 × 512 array at 15 µm pitch on a CMOS ROIC has these properties [I]:
  - an MTF50 of ≈34 (horizontal) and ≈30 (vertical) line pairs per mm (Fig. 4c);
  - a dynamic range of 62 dB (Fig. 4d) and a photoresponse non-uniformity (PRNU) of 5.05% (Fig. 4e);
  - images of objects at 80–600 °C without illumination (Fig. 4f).

  It images at −0.1 V bias with a fixed 2 ms integration time (Methods, p. 10). A 64 × 64 thin-film-transistor imager shows a PRNU of ≈1.41% after flat-field correction (Fig. 4g).

### S2.2 How the detectivity was obtained

The responsivity follows from the EQE $\eta$ at wavelength $\lambda$,

$$\mathcal{R}=\eta\,\frac{q\lambda}{hc}=\eta\,\frac{\lambda}{1.2398\ \mu{\rm m}}\ {\rm A\,W^{-1}} \label{eq:swir-responsivity}$$

where $h$ is Planck's constant and $c$ the speed of light. The Supplementary Information defines the specific detectivity as

$$D^{*}=\frac{\mathcal{R}\sqrt{A\,\Delta f}}{i_n} \label{eq:swir-dstar}$$

with $A$ the active area, $\Delta f=1$ Hz the electrical bandwidth and $i_n$ the measured noise current (SI Eq. S33, p. 34) [I].

The SI quotes a total noise below 2.19×10⁻¹³ A Hz⁻¹ᐟ² at 1 kHz which, with an EQE of 48.4% at 2,500 nm, gives 4.4×10¹¹ Jones (SI p. 34) [I]. Check [E]: Eq. \eqref{eq:swir-responsivity} gives $\mathcal{R}=0.484\times2.5/1.2398=0.976\ {\rm A\,W^{-1}}$, and with $A=1\ {\rm mm^2}=0.01\ {\rm cm^2}$ Eq. \eqref{eq:swir-dstar} gives $0.976\times0.1\ {\rm cm}/2.19\times10^{-13}=4.46\times10^{11}$ cm Hz¹ᐟ² W⁻¹. The whole D*(λ) curve of the PbS diode in Fig. 3f uses this single noise value: dividing $\mathcal{R}(\lambda)\sqrt{A}$ from the Source Data EQE by the Source Data D*(λ) gives 2.18×10⁻¹³ A Hz⁻¹ᐟ² at every wavelength from 1,300 to 2,700 nm [E].

The noise was taken at zero bias in the dark with an SR570 current preamplifier and an SR850 lock-in amplifier (Methods, p. 9; Peer Review File pp. 26–27) [I]. Measuring the noise, rather than assuming shot noise, is the right practice. The question is whether the measured value is physically possible for this diode.

### S2.3 The thermal floor at zero bias

**Result.** The dark current that the paper reports bounds the detectivity by

$$D^{*}\le\mathcal{R}\sqrt{\frac{|V|}{4k_BT\,|J(V)|}} \label{eq:swir-headline}$$

where $J(V)$ is the dark current density at a small reverse bias $V$. With the paper's numbers, $D^*\le0.976\times\sqrt{0.1/(1.646\times10^{-20}\times1.230\times10^{-4})}=2.2\times10^{11}$ Jones, half the reported 4.4×10¹¹ [E].

| Quantity | Symbol | Value | Source |
|---|---|---|---|
| Responsivity at 2.5 µm | $\mathcal{R}$ | 0.976 A W⁻¹ (EQE 48.4%) | SI p. 34; Source Data Fig. 3e |
| Bias of the dark-current point | $V$ | −0.1 V | Peer Review File p. 28 |
| Dark current density at −0.1 V | $J(V)$ | 123.0 µA cm⁻² | Peer Review File p. 28; consistent with Fig. 3b and Supp. Fig. 20b |
| Area | $A$ | 1 mm² | Supp. Fig. 19a legend |
| Temperature | $T$ | 298 K ($4k_BT=1.646\times10^{-20}$ J) | Peer Review File p. 118 (benchmark at 298 K) |
| Reported noise, 1 kHz, zero bias | $i_n$ | 2.19×10⁻¹³ A Hz⁻¹ᐟ² | SI p. 34 |

**Derivation.**
1. **The fluctuation–dissipation theorem fixes the noise.** At zero bias and in the dark a photodiode is a passive device in thermal equilibrium, and Nyquist's theorem fixes its short-circuit current noise. The one-sided power spectral density is

   $$S_I(f)=4k_BT\,{\rm Re}\,Y(f) \label{eq:swir-fdt}$$

   where $Y(f)$ is the device's small-signal admittance.
2. **At low frequency this is the Johnson noise of $R_0$.** There ${\rm Re}\,Y=1/R_0$, so the noise current density is

   $$i_{n,{\rm th}}=\sqrt{\frac{4k_BT}{R_0}} \label{eq:swir-johnson}$$

   In equilibrium this is not one noise term among several; it is the whole noise. For an ideal diode it equals the full shot noise of the two equal and opposite diffusion currents $I_0$ that cross the junction at zero bias: $4qI_0=4k_BT/R_0$ with $R_0=k_BT/(qI_0)$. Generation, recombination and trapping all enter through $R_0$ and through the frequency dependence of $Y$. A measured noise below Eq. \eqref{eq:swir-johnson} therefore means that the measurement, not the device, is wrong.
3. **The measured dark current bounds $R_0$.** The paper does not report $R_0$, but its dark current bounds it. In reverse bias the diode current saturates within a few $k_BT/q$, and leakage through a shunt grows at most linearly with $|V|$. Between 0 and −0.1 V the magnitude of the current therefore grows no faster than linearly with $|V|$, so the slope at the origin is at least the average slope over that interval:

   $$R_0A\le\frac{|V|}{|J(V)|} \label{eq:swir-chord}$$

   With 123.0 µA cm⁻² at −0.1 V, $R_0A\le0.1/1.230\times10^{-4}=813\ \Omega\,{\rm cm^2}$, so the 1 mm² diode has $R_0\le81.3$ kΩ. Eq. \eqref{eq:swir-johnson} then gives $i_{n,{\rm th}}\ge\sqrt{1.646\times10^{-20}/8.13\times10^{4}}=4.50\times10^{-13}$ A Hz⁻¹ᐟ², 2.05 times the reported noise [E].
4. **Substituting the floor into the detectivity.** Putting the floor in place of $i_n$ in Eq. \eqref{eq:swir-dstar} gives the most the diode can reach,

   $$D^{*}_{\max}=\frac{\mathcal{R}\sqrt{A}}{i_{n,{\rm th}}}=\mathcal{R}\sqrt{\frac{R_0A}{4k_BT}} \label{eq:swir-dstar-th}$$

   With Eq. \eqref{eq:swir-chord} this becomes Eq. \eqref{eq:swir-headline}: $0.976\times\sqrt{813/1.646\times10^{-20}}=2.17\times10^{11}$ Jones [E]. The units work out as follows. Ω cm² divided by J is cm² A⁻² s⁻¹, whose square root is cm Hz¹ᐟ² A⁻¹, and multiplied by A W⁻¹ this gives cm Hz¹ᐟ² W⁻¹, i.e. Jones.

**With the authors' own diode current, the floor is higher still.** The authors fit the dark current with a diode term, an ohmic shunt and a trap-assisted-tunnelling term (SI Eq. S34, p. 35). Supp. Fig. 20b draws the diode component of the MISI device with a reverse plateau of about 3–4×10⁴ nA cm⁻², with $n\approx1.2$ (p. 6; SI p. 35) [I]. Splitting the measured 123.0 µA cm⁻² into that diode current and a remainder, and bounding the remainder's resistance by its chord as in Eq. \eqref{eq:swir-chord}, gives

$$\frac{1}{R_0A}=\frac{q\,J_0}{n\,k_BT}+\frac{1}{R_{\rm rest}A} \label{eq:swir-r0a-split}$$

with $R_{\rm rest}A\le0.1\ {\rm V}/(J(V)-J_{\rm diode}(V))$. Two values bracket the result [E]:
- With $J_0=3\times10^{-5}\ {\rm A\,cm^{-2}}$, the diode term gives $n k_BT/(qJ_0)=0.0308/3\times10^{-5}=1{,}027\ \Omega\,{\rm cm^2}$. The diode carries $2.9\times10^{-5}\ {\rm A\,cm^{-2}}$ at −0.1 V, which leaves $9.4\times10^{-5}$ and $R_{\rm rest}A\le1{,}062\ \Omega\,{\rm cm^2}$, so $R_0A\le522\ \Omega\,{\rm cm^2}$.
- With $J_0=4\times10^{-5}$, the same steps give $R_0A\le466\ \Omega\,{\rm cm^2}$.

The floor is then 5.6–5.9×10⁻¹³ A Hz⁻¹ᐟ², 2.6–2.7 times the reported noise, and the detectivity is at most 1.6–1.7×10¹¹ Jones. If all of the −0.1 V current were diode current with $n=1.2$, $R_0A$ would be 241 Ω cm² and the floor 3.8 times the reported noise.

**Supp. Table 10 cannot be used as printed.** It gives $J_0=0.36$ mA cm⁻², $n=1.2$ and $R_{\rm sh}A=1.24$ kΩ cm² for the MISI devices (SI p. 49), and the main text repeats the $J_0$ (p. 7) [I]. These values contradict the measured current in two ways [E]:
- They predict $0.36\times(1-e^{-0.1/0.0308})+0.1/1.24=0.43$ mA cm⁻² at −0.1 V, 3.5 times the measured 0.123 mA cm⁻².
- The shunt alone would carry $0.8/1{,}240=0.65$ mA cm⁻² at −0.8 V, more than twice the ≈0.29 mA cm⁻² measured there (Fig. 3b; Supp. Fig. 20b).

The printed $J_0$ is also about ten times the diode plateau that Supp. Fig. 20b draws. Taken at face value the table would give $R_0A=80\ \Omega\,{\rm cm^2}$ and a floor 6.5 times the reported noise, but it evidently does not describe the measured diode, so this side note does not use it.

**The measured dark current itself is physical.** Two checks show that 123.0 µA cm⁻² is an allowed value for this absorber, so the conflict lies in the noise reading, not in the I–V.
- **Radiative floor.** With the paper's own EQE spectrum (Source Data, Fig. 3e), Eq. \eqref{eq:swir-radiative-floor} puts a floor of 0.88 µA cm⁻² under $J_0$ at 298 K, or 0.91 µA cm⁻² if the 0.3% EQE tail beyond 2.85 µm is counted [E, `detailed_balance.py`]. The measured current is about 140 times larger.
- **Empirical benchmark.** Rule 07, the empirical benchmark for the best HgCdTe diodes (Tennant et al., *J. Electron. Mater.* 2008), gives 180 µA cm⁻² at 298 K for a 2.7 µm cut-off, the wavelength where the PbS EQE has fallen to half [E, `rule07_check.py`]. The measured value sits at that benchmark, remarkable for a polycrystalline film but not forbidden.

**Detailed balance gives a second, independent bound on the noise.** Radiative recombination alone gives the diode a zero-bias conductance of $qJ_{0,{\rm rad}}/k_BT$ per unit area, and every other recombination channel adds to it. Writing $\eta_{\rm ext}\le1$ for the radiative share of the total, the external radiative efficiency,

$$R_0A=\eta_{\rm ext}\,\frac{k_BT}{q\,J_{0,{\rm rad}}} \label{eq:swir-r0a-radiative}$$

With $J_{0,{\rm rad}}\ge0.88\ \mu{\rm A\,cm^{-2}}$, $k_BT/(qJ_{0,{\rm rad}})\le0.0257\ {\rm V}/0.88\ \mu{\rm A\,cm^{-2}}=29{,}000\ \Omega\,{\rm cm^2}$ [E]. Two consequences follow.
- **The reported noise needs a very efficient emitter.** It needs $R_0A\ge3{,}430\ \Omega\,{\rm cm^2}$ (§S2.4), hence $\eta_{\rm ext}\ge3{,}430/29{,}000=12\%$.
- **The diode's own dark current needs far less.** The largest zero-bias conductance consistent with 123.0 µA cm⁻² at −0.1 V is that of an ideal diode, $J_0=123.0/(1-e^{-0.1/0.0257})=125.6\ \mu{\rm A\,cm^{-2}}$, which gives $R_0A\ge0.0257/125.6\times10^{-6}=204\ \Omega\,{\rm cm^2}$ and hence $\eta_{\rm ext}\ge0.7\%$ [E].

The reported noise would therefore require the PbS film to emit light 17 times more efficiently than its measured dark current requires.

### S2.4 How robust the floor is: offsets, bias, frequency and area

The zero-bias resistance is itself a measured quantity, and both the I–V and the noise measurement can carry small offsets. The bound of §S2.3 survives each of the following.

1. **Bias error in the I–V.** The dark current was recorded with an Agilent B1500A semiconductor analyser (Methods, p. 9) [I]. The bound uses the current at −0.1 V, where the 1 mm² diode passes 1.23 µA. It does not use the slope near 0 V, where currents are a few nanoamperes and offsets matter.
   - A bias error $\delta V$ changes the current at −0.1 V by at most the fraction $\delta V/0.1$ V, 1% per millivolt, for an ohmic branch, and by less for a saturating one.
   - For the reported noise to be physical, $R_0A$ would have to be at least $4k_BT\,A/i_n^2=1.646\times10^{-20}\times0.01/(2.19\times10^{-13})^2=3{,}430\ \Omega\,{\rm cm^2}$, 4.2 times the chord value [E]. That would need a current at −0.1 V 4.2 times smaller than measured, which no millivolt-level offset can produce.
2. **Residual bias during the noise measurement.** The SR570 holds its input at a virtual null set by its front-end operational amplifier [P, SR570 manual]. At 10⁸ V/A that amplifier is an AD743 in High Bandwidth mode and an AD546 in Low Noise mode [P, manual Appendix B, PDF p. 35]. The AD743 has an initial input offset of 0.25 mV typical and 1.0 mV maximum, and the AD546 of up to 1 mV [P, AD743 datasheet p. 2; AD546 datasheet p. 1]. Both offsets are nulled with trimmers at calibration (manual, PDF p. 29) [P].
   - **What sets the residual bias.** After calibration the op amps' datasheet offsets matter less than three other things: how well the trims have held, thermoelectric voltages at the contacts of the range relays in the input path (manual, PDF p. 26) [P; size U], and the bias-voltage source if it was switched on. That source sets −5 to +5 V in 12-bit steps of 1.22 mV (manual, PDF p. 16) [P].
   - **The output need not show it.** The instrument can also subtract an input offset current of 1 pA to 5 mA (manual, PDF pp. 8, 13) [P]. That nulls a DC current at the output, so a diode can sit at a small bias that the output does not show.
   - **Size of the effect.** A residual 0.25–2 mV across $R_0\approx47$–81 kΩ drives 3–40 nA through the diode [E].
   - The floor barely moves. For an ideal diode in parallel with a linear shunt, the noise at a bias $V$ is

     $$S_I(V)=2qI_0\left(e^{qV/k_BT}+1\right)+\frac{4k_BT}{R_{\rm sh}} \label{eq:swir-bias-floor}$$

     where $I_0$ is the diode's saturation current and $R_{\rm sh}$ the shunt resistance. With $J_0=3.5\times10^{-5}\ {\rm A\,cm^{-2}}$ and the remainder of §S2.3 as the shunt, Eq. \eqref{eq:swir-bias-floor} gives 5.98×10⁻¹³ A Hz⁻¹ᐟ² at 0 V, and 5.94 or 6.01×10⁻¹³ at −1 mV or +1 mV [E].
   - Even 100 mV of reverse bias, which halves the diode's share of the noise power, leaves 4.97×10⁻¹³ [E]. If all of the leakage were ohmic, the floor would be 4.50×10⁻¹³ at any bias. No small bias brings the floor down to the reported 2.19×10⁻¹³.
   - A residual bias does explain one feature of Supp. Fig. 19a. At true equilibrium the spectrum is $4k_BT\,{\rm Re}\,Y(f)$, which does not rise toward low frequency for any network of resistors and capacitors (item 3). The 1/f rise below ≈200 Hz that the paper fits as 1/f noise of the dark current therefore means either that current flowed, as a residual offset makes it do, or that the amplifier contributed the excess.
3. **Frequency.** The bound uses the DC resistance, but the noise was read at 1 kHz. There the diode's capacitance, about 3 nF at 0 V (Supp. Fig. 18b, SI p. 31), puts the corner $1/(2\pi R_0C)$ near 650 Hz [I/E]. A network of resistors and capacitors, the usual model of junction, traps and contacts, has an admittance of Foster form, $Y(j\omega)=G_0+j\omega C_\infty+\sum_i k_i\,j\omega/(j\omega+\sigma_i)$ with $k_i,\sigma_i>0$. Its real part, $G_0+\sum_i k_i\omega^2/(\omega^2+\sigma_i^2)$, is never below the DC conductance $G_0=1/R_0$. The floor at 1 kHz is therefore at least the DC floor.
4. **Area.** The comparison involves only currents, the measured noise current and the measured dark current $I=JA$ at −0.1 V. $R_0\le0.1\ {\rm V}/1.23\ \mu{\rm A}$ does not depend on the area assumed, so an error in the 1 mm² cannot reconcile them. The temperature matters little: ±5 K changes the floor by less than 1%.
5. **The only escape is a different diode.** The noise and the I–V would have to come from different diodes. The Source Data workbook for Fig. 3b holds a dark curve whose slope at 0 V gives $R_0A\approx5.1$ kΩ cm², and the reported noise would respect its floor of 1.8×10⁻¹³ A Hz⁻¹ᐟ² [E]. But that curve does not match the published panel, which shows ≈0.12 mA cm⁻² at −0.1 V where the workbook curve has 37.0 µA cm⁻² [I/E]. The authors themselves pair the 4.4×10¹¹ Jones with the 123.0 µA cm⁻² diode, measured "under identical conditions" with the InGaAs reference (Peer Review File p. 28; main text p. 6) [I].

### S2.5 The measurement chain

**What is described.** The Methods give the noise measurement one sentence: an SR570 low-noise current preamplifier "together with" an SR850 lock-in amplifier (p. 9) [I]. In the first rebuttal the authors describe the SR570 feeding the SR850 at a transimpedance of 10⁸ V/A. They put the instrument floor at about 5 fA Hz⁻¹ᐟ², set by the SR570, after Referee #1 had found a claimed floor below 1 fA Hz⁻¹ᐟ² unrealistic (Peer Review File pp. 1, 26) [I]. The rebuttal also says the details were added to the Methods and to a Supplementary Fig. S28 (p. 26). The published Methods hold only the sentence above, and the published SI ends at Supplementary Fig. 24.

**What the instrument does at that gain** [P, SR570 manual, Table 1, PDF p. 10; Appendix B, PDF p. 35]:
- **Bandwidth.** At 10⁻⁸ A/V (10⁸ V/A) the −3 dB bandwidth is 200 Hz in Low Noise mode, the instrument's default, and 2 kHz in High Bandwidth mode. A 1 kHz measurement therefore needs High Bandwidth mode.
- **Input impedance.** The DC input impedance is 10 kΩ at 10⁻⁷ and 10⁻⁸ A/V.
- **Front-end amplifier.** The front end is an AD546 (35 nV Hz⁻¹ᐟ² at 1 kHz [P, AD546 datasheet p. 2]) in Low Noise mode and an AD743 (3.2 nV Hz⁻¹ᐟ² at 1 kHz [P, AD743 datasheet p. 2]) in High Bandwidth mode.
- **Own noise.** The instrument's own noise is 60 fA Hz⁻¹ᐟ² (Low Noise) or 100 fA Hz⁻¹ᐟ² (High Bandwidth); the 5 fA figure belongs to the 10⁻¹⁰–10⁻¹² A/V ranges, whose bandwidth is 10–100 Hz.
  - The reported value is a total: the SI calls 2.19×10⁻¹³ A Hz⁻¹ᐟ² "the total measured noise current spectral density" (p. 34), and neither the SI nor the rebuttal describes subtracting the instrument's noise [I].
  - Because that noise adds in quadrature, subtracting 100 fA Hz⁻¹ᐟ² would leave $\sqrt{2.19^2-1.0^2}\times10^{-13}=1.95\times10^{-13}$ A Hz⁻¹ᐟ² for the diode, 2.3 times below its thermal floor [E].
  - The instrument's own noise therefore makes the reading too high, not too low; only an error in the chain's gain, response or normalization can make it too low.
- **Conditions of these figures.** The manual states that its figures hold for a 100 pF source capacitance and an infinite source resistance, and that "significantly higher values of source capacitance or finite source resistance can degrade these specifications". The PbS diode presents about 3 nF and 47–81 kΩ.
- **Source impedance.** For accurate measurements the manual asks for a source impedance above the inverse of the sensitivity, 100 MΩ at 10⁸ V/A (manual, PDF p. 11) [P]. At 1 kHz the PbS diode presents 37–44 kΩ, 2,300–2,700 times less [E].
- **The input resistor.** The 10 kΩ input impedance is a physical resistor. In the low-noise front end, resistors R132–R135, switched with the range by relays K103–K105, protect the amplifier's inputs and limit its noise gain due to input capacitance. Their values are chosen for an error below 0.1% in the output (manual, PDF p. 26) [P].
  - That holds for the high-impedance sources the manual has in mind, but with the PbS diode the resistor becomes part of the circuit being measured.
  - Its own Johnson noise, 12.8 nV Hz⁻¹ᐟ², is no longer negligible against the diode's [E].

**What the chain would read.** The amplifier's virtual null sees the diode's impedance $Z_s=R_0/(1+j\omega R_0C)$ in series with the input resistor $R_{\rm in}$. In equilibrium, Eq. \eqref{eq:swir-fdt} applied to that whole network gives its thermal noise current. The amplifier's voltage noise $e_n$ drives a further current $e_n/|R_{\rm in}+Z_s|$ through the network, and the instrument adds its own current noise $i_{\rm amp}$. The amplifier response $H(f)$ filters the sum:

$$i_{\rm read}=|H(f)|\sqrt{4k_BT\,{\rm Re}\frac{1}{R_{\rm in}+Z_s}+\frac{e_n^2}{|R_{\rm in}+Z_s|^2}+i_{\rm amp}^2} \label{eq:swir-chain}$$

Here $|H|=1/\sqrt{1+(f/f_{3\,{\rm dB}})^2}$, which assumes a single-pole response at the specified bandwidth. Eq. \eqref{eq:swir-chain} gives these expected readings at 1 kHz [E]:

| SR570 setting at 10⁸ V/A | $\lvert H\rvert$ at 1 kHz | $e_n/\lvert R_{\rm in}+Z_s\rvert$, PbS | Expected, PbS diode ($R_0$ 81 or 51 kΩ, 3 nF) | Expected, InGaAs diode ($R_0$ 100 or 182 kΩ, 50 pF) |
|---|---|---|---|---|
| High Bandwidth (AD743, 2 kHz) | 0.89 | 0.6–0.7×10⁻¹³ | 4.3–5.0×10⁻¹³ | 2.8–3.6×10⁻¹³ |
| Low Noise, default (AD546, 200 Hz) | 0.20 | 6.9–7.8×10⁻¹³ | 1.6–1.9×10⁻¹³ | 0.7–1.0×10⁻¹³ |
| *Reported* | | | 2.19–2.20×10⁻¹³ (both rounds) | 2.09×10⁻¹³ (first rebuttal); 3.3×10⁻¹³ implied by the second |

*How the numbers are derived* [E]:
- **PbS diode, network noise.** With $R_0=81.3$ kΩ and $C=3$ nF at 1 kHz, $\omega R_0C=1.53$, so $Z_s=24.3-37.2j$ kΩ, $R_{\rm in}+Z_s=34.3-37.2j$ kΩ and $|R_{\rm in}+Z_s|=50.6$ kΩ. Then ${\rm Re}[1/(R_{\rm in}+Z_s)]=34.3/50.6^2\ {\rm mS}=1.34\times10^{-5}$ S, and the network's thermal noise is $\sqrt{1.646\times10^{-20}\times1.34\times10^{-5}}=4.70\times10^{-13}$ A Hz⁻¹ᐟ².
- **The resistor does not lower it.** That is slightly more than the diode alone (4.50×10⁻¹³): at this frequency the resistor's own noise outweighs the current it diverts. With $R_0=51.5$ kΩ the network gives 5.49×10⁻¹³ against 5.65×10⁻¹³ for the diode alone.
- **Voltage-noise current.** It is $3.2\times10^{-9}/50.6\times10^{3}=6.3\times10^{-14}$ for the AD743 and $6.9\times10^{-13}$ for the AD546.
- **InGaAs diode.** At 1 kHz the 50 pF barely matters, and the network noise is that of $R_0+R_{\rm in}$: 3.9×10⁻¹³ for 100 kΩ and 2.9×10⁻¹³ for 182 kΩ. The 182 kΩ value is the diode's own −0.1 V current read as diffusion-limited (§S2.6).

Three conclusions follow.
- **In High Bandwidth mode the PbS reading is too low.** The mode a 1 kHz reading requires should have read the PbS diode at 4.3–5.0×10⁻¹³, 2.0–2.3 times the reported value. It should also have read the InGaAs diode at about the second-rebuttal value, not the first. The input resistor cannot explain a low reading, because it leaves the network's noise about as large as the diode's own.
- **No single setting fits both first-round readings.** In Low Noise mode the reading at 1 kHz is cut fivefold and is set by the AD546's voltage noise acting on the 3 nF source. That lands near the reported PbS value but puts the InGaAs reading 2–3 times below its first-round value. Either the chain's real response and loading differed from these specifications, or the settings differed between devices, and the paper does not say which.
- **The InGaAs diode cannot calibrate the chain for the PbS diode.** It presents 50 pF and 0.1–0.2 MΩ against 3 nF and 50–80 kΩ, so the same chain loads and filters the two differently.

**The noise decomposition does not apply at zero bias.** Supp. Fig. 19a decomposes the PbS spectrum with shot noise $\sqrt{2qI_d}$ (Eq. S30), a generation–recombination term with a "current gain" (Eq. S31) and a 1/f term proportional to $I_d^2$ (Eq. S32) (SI pp. 33–34) [I]. All three need a dark current $I_d$, and at zero bias the net current is zero.
- The main text's description of "a noise floor above 1 kHz approaching the shot-noise limit" (p. 6) applies the picture of a biased diode to an unbiased one.
- The curve labelled "thermal noise" lies near 1×10⁻¹⁴ A Hz⁻¹ᐟ². That is the Johnson noise of $1.646\times10^{-20}/(10^{-14})^2=1.6\times10^{8}\ \Omega$, an $R_0A$ of 1.6×10⁶ Ω cm², 2,000 times the bound of Eq. \eqref{eq:swir-chord} [E]. The decomposition therefore leaves out the one term that must dominate.
- The gentle fall above 2–3 kHz that it fits with a generation–recombination Lorentzian sits where the High Bandwidth response at 10⁸ V/A rolls off.
- The figure's axis and Eqs. S30–S32 are labelled "noise power spectral density" but are in A Hz⁻¹ᐟ², an amplitude density.

**What would settle it.** Three measurements would decide the question.
1. Measure, with the same settings, a metal-film resistor of 50–80 kΩ in parallel with about 3 nF in place of the diode, whose noise is known.
2. Measure the diode's admittance at 1 kHz with an LCR meter and compare its noise with $4k_BT\,{\rm Re}\,Y$.
3. Calibrate the chain's response at 1 kHz with the diode connected, by injecting a known AC current through a small capacitor at the input (§S2.8).

§S2.8 places these three checks in a fuller protocol.

**A sounder protocol is in use elsewhere.** Luo et al. quote 2.8×10¹⁰ Jones for an HgTe array and compute it from the signal-to-noise ratio of each pixel. They measure that ratio over 100 frames under illumination with a 5 ms integration, so read noise, dark-current noise and photon noise are all included, and the integration sets the bandwidth (Luo et al., Eq. 7 and Table I) [I]. Their figure corresponds to a signal-to-noise ratio of about 700 [E: ${\rm SNR}=D^{*}EA/\sqrt{A\,\Delta f}$ with irradiance $E=216\ \mu{\rm W\,cm^{-2}}$, pixel area $A=1.33\times10^{-6}\ {\rm cm^2}$ and $\Delta f=1/(2\times5\ {\rm ms})=100$ Hz gives $2.8\times10^{10}\times2.87\times10^{-10}/0.0115=700$].

**Zero bias at 1 kHz is also the most favourable operating point.** The imager runs at −0.1 V with 2 ms integration (Methods, p. 10). There the shot noise of the 1.23 µA dark current of a 1 mm² diode is $\sqrt{2q\times1.23\times10^{-6}}=6.3\times10^{-13}$ A Hz⁻¹ᐟ², and the 1/f noise below ≈200 Hz falls inside the ≈250 Hz noise bandwidth of a 2 ms integration [E]. The zero-bias, 1 kHz detectivity therefore does not describe the imager.

### S2.6 The InGaAs benchmark across the review rounds

Referee #1 asked for a commercial extended-SWIR InGaAs photodiode to be measured as a reference (Peer Review File p. 1) [I]. The authors measured a Hamamatsu G12183-003K, a φ0.3 mm, 2.6 µm-cut-off, uncooled diode, twice.

| | PbS diode (Li et al.) | G12183-003K |
|---|---|---|
| Photosensitive area | 1 mm² | 0.0707 mm² (φ0.3 mm, datasheet); 0.09 mm² used in the first rebuttal |
| Capacitance at 0 V | ≈3 nF (Supp. Fig. 18b) | 50 pF typ. (datasheet p. 3) |
| Dark current density at −0.1 V, authors | 123.0 µA cm⁻² | 153.7 µA cm⁻² |
| Zero-bias $R_0A$ | ≤813 Ω cm²; ≤466–522 with the authors' diode component | 71 Ω cm² (typical $R_{\rm sh}$ 100 kΩ); ≈129 Ω cm² (authors' current, diffusion-limited) |
| Thermal floor at 298 K | ≥4.5×10⁻¹³ (≥5.6–5.9×10⁻¹³) A Hz⁻¹ᐟ² | 4.1×10⁻¹³ (typical); 3.0×10⁻¹³ (authors' unit) A Hz⁻¹ᐟ² |
| Noise reported, 1 kHz, 0 V | 2.20×10⁻¹³ (first rebuttal); 2.19×10⁻¹³ (SI) | 2.09×10⁻¹³ (first rebuttal) |
| D* reported at 2.5 µm | 4.4×10¹¹ Jones, unchanged | 1.7×10¹¹ (first rebuttal); 9.5×10¹⁰ (second rebuttal, Fig. 3f) |
| D* allowed by the floor at 2.5 µm | ≤2.2×10¹¹ (≤1.6–1.7×10¹¹) Jones | 0.8–1.1×10¹¹ Jones (with the authors' EQE of 59.3%) |

- **First rebuttal (Peer Review File pp. 26–28).** The authors reported, "using the exact same measurement chain", these values: 2.09×10⁻¹³ (InGaAs) and 2.20×10⁻¹³ (PbS) A Hz⁻¹ᐟ² at 1 kHz, 153.7 and 123.0 µA cm⁻² at −0.1 V, EQE at 2,500 nm of 59.3% and 48.4%, and D* of 1.7×10¹¹ and 4.4×10¹¹ Jones. They wrote that the InGaAs value agrees well with the datasheet [I]. It does not.
  - The datasheet gives a typical D* of 9×10¹⁰ and a minimum of 3×10¹⁰ cm Hz¹ᐟ² W⁻¹, at the peak wavelength near 2.3 µm, where the responsivity peaks at about 1.3 A W⁻¹ (datasheet p. 3) [P]. 1.7×10¹¹ is 1.9 times the typical, at a wavelength past the peak.
  - The typical value is itself the Johnson-noise limit: Eq. \eqref{eq:swir-dstar-th} with $R_0A=71\ \Omega\,{\rm cm^2}$ and 1.3 A W⁻¹ gives $1.3\times\sqrt{71/1.646\times10^{-20}}=8.5\times10^{10}$ Jones [E].
  - The 2.09×10⁻¹³ reading is the Johnson noise of 377 kΩ, 3.8 times the typical shunt resistance. Read as diffusion-limited, the authors' own −0.1 V current of 138 nA gives $R_0=k_BT/(qI_0)=182$ kΩ and a floor of 3.0×10⁻¹³, which the reading also undercuts, by 1.44 times [E].
- **Equal noise at 14 times the area is not evidence of fewer defects.** The authors read the equal noise of the two diodes as evidence of fewer defects in the PbS (p. 27) [I]. Junction noise scales as $\sqrt{A/R_0A}$, so typical $R_0A$ values predict a PbS-to-InGaAs ratio of $\sqrt{14.1\times71/813}=1.1$. Equal noise is what the two diodes' resistances predict; what is wrong is that both readings sit below their thermal floors [E].
- **Second rebuttal (Peer Review File pp. 118–119).** Referee #1 asked for the measured InGaAs D* to be added to Fig. 3f. The authors measured the InGaAs at 298 K "with the actual photosensitive area" and found a peak of 9.52×10¹⁰ Jones near 2.5 µm, "in good agreement" with the datasheet's 9×10¹⁰ [I]. The Source Data of Fig. 3f give 9.75×10¹⁰ at 2,360 nm and 9.52×10¹⁰ at 2,500 nm [I].
  - The passage does not mention the earlier 1.7×10¹¹ or explain the change by a factor of 1.80. The area correction accounts for 1.13 of it. The remaining factor of 1.60 corresponds to a noise reading of 3.34×10⁻¹³ if the responsivity was unchanged [E].
  - The PbS value stayed at 4.4×10¹¹, with the same noise.
- **The final text keeps the older comparison.** It compares PbS with "uncooled 2.5-µm In0.83Ga0.17As detectors (about 1.7 × 10¹¹ Jones)", citing Arslan et al., *IEEE J. Quantum Electron.* 50, 957 (2014), a focal-plane-array paper (p. 7) [I]. Supp. Table 11 lists In₀.₈₃Ga₀.₁₇As at 2,650 nm with 2.5×10¹⁰ Jones (SI p. 50), so the paper carries two literature values for the same material, a factor of 7 apart. Whether Arslan et al.'s value is for an uncooled detector is an item for §S5.
- **The benchmark curve understates InGaAs below 2 µm.** In Fig. 3f the measured InGaAs curve is 2.24×10¹⁰ Jones at 1,550 nm, 4.3 times below its peak (Source Data) [I]. The datasheet responsivity at 1.55 µm, ≈0.74 A W⁻¹, is only 1.8 times below its ≈1.3 A W⁻¹ peak [P, datasheet p. 3, read by eye]. With a constant noise the D* curve should follow the responsivity, so the curve understates InGaAs by about 2.4 times at 1,550 nm [E].

### S2.7 Verdict, and what the device means for cars

**The detectivity is overstated.** For the diode to which the authors attribute it, the reported D* is overstated by at least 2.05 times, a bound that needs only the paper's own dark current and thermodynamics. With the diode current the authors' fit draws, the factor is 2.6–2.7. The physically allowed value is at most 2.2×10¹¹ Jones at 2.5 µm, 0 V and 298 K, and most likely 1.6–1.7×10¹¹. Detailed balance gives the same verdict independently: the reported noise would need the film to be an emitter with an external radiative efficiency of at least 12%, 17 times what its own dark current requires (§S2.3).

That is still a good value for a room-temperature photodiode with a 2.85 µm cut-off. Against the measured G12183-003K (9.5×10¹⁰ Jones at 2.5 µm, consistent with its datasheet) the PbS diode leads by 1.7–2.3 times rather than 4.7. That lead reflects an $R_0A$ several times higher than extended InGaAs's, at a lower responsivity. Against the 1.7×10¹¹ Jones the main text quotes for uncooled In₀.₈₃Ga₀.₁₇As, the corrected value is at parity, not 2.6 times ahead. It still matches or exceeds the other room-temperature points that Supp. Table 11 compiles at 2.5 µm (HgCdTe 1.0×10¹¹, HgTe quantum dots 6.5×10¹⁰); this side note did not check how those points were selected.

A commercial printed PbS photoconductor gives another reference point. trinamiX's Hertzstück single pixel is specified at 22 °C with 1×10¹¹ Jones typical and 0.8×10¹¹ minimum at its 2.7 µm peak, a 2.9 µm cut-off and a 200 µs time constant [P, datasheet]. At the nearby 2,640 nm the corrected PbS diode reaches 1.5–2.0×10¹¹ Jones, the reported 4.1×10¹¹ divided by 2.05–2.7. That is 1.5–2 times the photoconductor, a plausible margin for a photodiode at zero bias [E].

**What holds.** The paper's contribution does not rest on the detectivity. It is a quasi-single-crystalline PbS photodiode grown from water at room temperature directly on a CMOS ROIC, with an EQE above 40% from 0.7 to 2.6 µm and a working 640 × 512 imager. The low-intensity responsivity in the Fig. 3c data, 0.59–0.64 A W⁻¹ at 1,300 nm for a 1 mm² device, is broadly consistent with the 0.71 A W⁻¹ from the EQE [E]. Growing a lead salt directly on a finished readout chip is not new in itself (§S3.4); what is new is a room-temperature aqueous route to a PbS photodiode with a high SWIR EQE at 15 µm pitch.

**For cars.** This absorber suits the 2–2.8 µm band: extended-SWIR industrial sensing, and imaging of hot objects as in Fig. 4f. It does not suit the 1.3–1.6 µm band cars use.
- At −0.1 V a 15 µm pixel with the test diode's leakage collects 1.7×10⁶ dark electrons per millisecond, 3.5×10⁶ in the paper's 2 ms integration [E]. The paper gives neither the array's dark current nor the ROIC's full well; §S2.8 estimates what that leaves open.
- The paper does not measure the leakage at automotive temperatures either, and bulk PbS cannot be given a wider band gap.
- The same growth route would need a different absorber, for example quantum-confined PbS, to compete at automotive wavelengths.

### S2.8 How such a diode could be measured

Measuring the noise of a photodiode like this one is harder than it looks. At 1 mm² it presents 50–80 kΩ in parallel with 3 nF, while a general-purpose current preamplifier at its sensitive ranges is specified for sources above 100 MΩ and 100 pF (§S2.5), and such a preamplifier, the SR570 in particular, is the natural first choice in most laboratories [E]. The discrepancy of §S2.3–§S2.5 is therefore easy to fall into. Established practice in three communities shows how to avoid it.

**Emerging photodetectors.** A consensus statement by more than 50 academic and industrial groups, published in November 2025 after Li et al. had submitted their paper, sets out the practice (Pecunia et al., *Nat. Photon.* 19, 1178) [I].
- The noise power spectral density should be measured and corrected for the instrument's own noise (p. 1182).
- The preferred route to the NEP records that spectrum while a modulated optical signal of known rms power is applied; the power at which the signal line equals the noise is the NEP (p. 1183; Fig. 4b,c). Dividing a measured noise by a responsivity is accepted only if the responsivity was measured at powers approaching the NEP; otherwise the result is an apparent detectivity, $D_{\rm app}$ (p. 1183).
- A theoretical noise floor must include the thermal term $4k_BT/R$, with $R$ the differential resistance at the operating voltage (Eq. 5, p. 1183). $D^*$ should be quoted only after the noise has been shown to scale as $\sqrt{AB}$, for example on devices whose areas differ 5–10-fold (p. 1183; Supplementary Note 18, SI p. 51).

Its Supplementary Note 14 gives the instrument correction (SI pp. 46–47; Supplementary Fig. 6). The detector is replaced by a dummy, a resistor equal to its dark differential resistance in parallel with a capacitor equal to its dark capacitance, whose spectrum $S^{\rm ext}$ is recorded. The chain's transfer function $H(f)$ is measured by injecting a sinusoidal test current through a capacitor at the input, with the dummy in place. Injected at the node where the diode connects, the test current divides between the amplifier and the diode exactly as the diode's own noise current does, so $H(f)$ applies to that noise; the injecting impedance only has to be far above that of the node [E]. A capacitor suits this because it adds no thermal noise and passes no direct current, so it can stay connected while the noise is recorded without disturbing the bias. Driven at 1 V rms, 1 pF injects $2\pi fCV$, 63 pA at 10 Hz and 6.3 nA at 1 kHz, a current known as well as $C$ is measured [E, `measurement_budget.py`]. A resistor gives a current that is flat down to DC, but it adds $4k_BT/R$ and turns capacitive through its stray capacitance: 100 MΩ with 0.2 pF injects 3 dB more than $V/R$ at 8 kHz [E]. With $S^{\rm tot}$ the spectrum recorded with the detector connected, the detector's own spectrum is

$$S^{\rm PD}(f)=\frac{S^{\rm tot}(f)-S^{\rm ext}(f)}{|H(f)|^2}+\frac{4k_BT}{R_{\rm dark}} \label{eq:swir-dummy}$$

The supplement prints the last term with a minus sign (its Eq. S26). The subtraction also removes the dummy resistor's own thermal noise, so that term has to be added back [E]. At zero bias in the dark the diode is in equilibrium and a dummy with $R=R_0$ reproduces its noise, so the two spectra must agree.

**Infrared detectors.** Datasheets state the conditions with the number, as in $D^*(\lambda_p,1200,1)$: at the peak wavelength, with the light chopped at 1,200 Hz and the noise in a 1 Hz band (Hamamatsu P15409-901 datasheet, p. 1) [P]. For a photodiode at zero bias the noise is the Johnson noise of $R_0$, so $D^*$ follows from $R_0A$ through Eq. \eqref{eq:swir-dstar-th}; the typical $D^*$ of the G12183-003K is exactly that limit (§S2.6).

**Image sensors and cameras.** The EMVA 1288 standard characterizes a camera from its own output (Release 4.0 Linear, 2021) [P]. The photon transfer curve gives the system gain and the temporal dark noise in electrons (Eq. 15, p. 10). The SNR then depends only on the quantum efficiency and the dark noise, because the gain cancels (Eq. 21, p. 11), and the absolute sensitivity threshold, the photon number at which the SNR is 1, plays the role of the NEP (Eq. 26, p. 12). Dark current is measured from the dark signal against exposure time and reported at several temperatures (Eqs. 29–30 and §3.2, p. 12).

**A protocol for this diode** [E, `measurement_budget.py`]:
1. **Check the chain against thermodynamics first.** Measure the admittance $Y(f)$ of the same diode with an LCR meter, and require its zero-bias dark spectrum to equal $4k_BT\,{\rm Re}\,Y(f)$, Eq. \eqref{eq:swir-fdt}, or equivalently to match the spectrum of its dummy. A reading below that floor, as in §S2.3, flags the chain before any $D^*$ is computed.
2. **Choose the amplifier by the diode's impedance.** In a TIA with feedback resistor $R_f$, three terms add to the diode's noise: the resistor's Johnson noise $\sqrt{4k_BT/R_f}$, the op amp's current noise $i_n$, and its voltage noise $e_n$, which drives a current $e_n|Y|$ through everything at the input, $|Y|=|1/R_0+1/R_f+j2\pi f(C_s+C_f+C_{\rm in})|$ [E]. Here $C_s$ is the diode's capacitance, $C_f$ the feedback capacitor and $C_{\rm in}$ the op amp's input capacitance. Against the diode's thermal noise, the resistor costs $R_0/R_f$ of the noise power. The voltage noise is small only if $e_n$ is well below the diode's own Johnson voltage, $\sqrt{4k_BTR_0}=37$ nV Hz⁻¹ᐟ² for $R_0=81.3$ kΩ, divided by $|1+j2\pi fR_0C_s|$, which is 1.8 at 1 kHz [E, `measurement_budget.py`].
   - With $R_f=1$ MΩ the resistor costs 8% of the diode's noise power, which the dummy measurement removes. The op amp's bias and current noise do not matter here: the AD743's 150 pA bias puts 0.15 mV on the output, and its 6.9 fA Hz⁻¹ᐟ² is 0.3% of the resistor's noise power (AD743 datasheet, p. 2) [P].
   - Its voltage noise does matter. The AD743, the JFET-input amplifier that the SR570 itself uses (§S2.5), has 3.2 nV Hz⁻¹ᐟ² at 1 kHz and adds $7.4\times10^{-14}$ A Hz⁻¹ᐟ² there; the diode keeps about 90% of the total noise power from 10 Hz to 1 kHz. The electrometer-grade OPA928, with 18 nV Hz⁻¹ᐟ² at 100 Hz and 15 at 1 kHz (TI SBOSA77A, p. 4), adds $3.5\times10^{-13}$ at 1 kHz and leaves the diode 60%. The general-purpose CMOS LMC662, with 22 nV Hz⁻¹ᐟ² (TI SNOSC51D, p. 6), adds $5.1\times10^{-13}$, more than the diode's own noise, and leaves it 42%. The ADA4530-1 is in the same class as the OPA928, at 14 nV Hz⁻¹ᐟ² quoted for 10 kHz [S]. The femtoampere bias currents of these parts buy nothing at 1 MΩ.
   - The Johnson noise of $R_f$ is the largest excess term only while $e_n|Y|$ stays below it, which for the AD743 holds up to about 2 kHz. Above that, $e_n\,2\pi fC_s$ keeps growing, and at 10 kHz it exceeds the diode's own noise.
   - The choice reverses for a pixel-sized diode. At 15 µm the same $R_0A$ gives $R_0\approx3.6\times10^{8}$ Ω, about 0.7 pF and a thermal floor of 6.8 fA Hz⁻¹ᐟ². The AD743's current noise alone would double that floor, so an electrometer amplifier with $R_f\approx10$ GΩ is the right choice there; it turns the 277 pA dark current at −0.1 V into 2.8 V.
   - $R_f=1$ MΩ is set by the dark current. At −0.1 V the 1.23 µA becomes 1.23 V, whereas 10 MΩ would need a 12.3 V swing, more than ±9 V battery rails allow. At 0 V no dark current flows, and 10 MΩ cuts the resistor's share to 0.8%.
   - With 3 nF at the input, a feedback capacitor $C_f\approx\sqrt{C_s/(2\pi R_ff_{\rm GBW})}$ keeps the response flat and stable, where $f_{\rm GBW}$ is the op amp's gain–bandwidth product. For the AD743's 4.5 MHz (p. 2) that is 10 pF and a 16 kHz bandwidth at 1 MΩ, and 3.3 pF and 4.9 kHz at 10 MΩ.
   - The bias is applied to the non-inverting input from a battery-referenced divider behind a large RC filter, so the diode sits at the chosen voltage with no series resistor. The circuit runs on batteries in a shielded box.
   - The output goes to an FFT analyser or a digitizer, with the window and the equivalent noise bandwidth stated (Pecunia et al., Supplementary Note 15, SI p. 48).
3. **Measure the noise against bias.** At 0 V the spectrum must equal $4k_BT\,{\rm Re}\,Y$. As the reverse bias grows, the diode's share falls toward the full shot noise of its saturation current, Eq. \eqref{eq:swir-bias-floor}, while 1/f and generation–recombination noise grow with the current. The figure that matters for the camera is the noise at the imager's −0.1 V, over the ≈250 Hz noise bandwidth of a 2 ms integration (§S2.5).
4. **Read the NEP from the SNR at a known power.** With 1 MΩ the output noise is 0.47 µV Hz⁻¹ᐟ², and a 10 V swing holds 10 µA, about 10 µW at 2.5 µm. One range therefore covers seven decades above the NEP, which is about $4.6\times10^{-13}$ W Hz⁻¹ᐟ² at the thermal floor; a modulated signal of 46 pW rms on the 1 mm² diode gives an SNR of 100 in 1 Hz.
   - The optical power must be traceable: a blackbody of known temperature behind a known aperture, or a laser behind attenuators calibrated against a reference detector at higher power.
   - This diode's noise is large enough for one gain to carry both its noise and its signal. A detector whose noise is in the femtoampere range needs 10⁹ Ω or more to read that noise, and its signal then needs a lower gain. The ratio of the two gains must then be calibrated by injecting a known current, as for $H(f)$.
5. **Measure several areas, and repeat the I–V.** A 0.1 mm² diode with the same $R_0A$ presents 0.81 MΩ and 0.3 nF. Its floor, $1.4\times10^{-13}$ A Hz⁻¹ᐟ², is $\sqrt{10}$ times lower, and it is easier to read: a 10 MΩ feedback resistor adds 8% in noise power and the amplifier's voltage noise 0.3%. The pair tests the $\sqrt{A}$ scaling that $D^*$ assumes. Measuring the I–V before and after the noise checks that the diode did not drift in between (Pecunia et al., p. 1186).
6. **Cross-correlate if the amplifier noise is comparable.** Two amplifiers reading the same diode give a cross-spectrum whose average converges to the diode's own spectrum, even when each amplifier's background is larger (Rubiola and Vernotte, arXiv:1003.0113) [I]. For a low-impedance diode the simplest form reads the open-circuit voltage noise, $\sqrt{4k_BTR_0}=37$ nV Hz⁻¹ᐟ² below the 650 Hz corner for $R_0=81.3$ kΩ, with two voltage preamplifiers of a few nV Hz⁻¹ᐟ². The photovoltage read through the same preamplifiers gives the same NEP, because signal and noise both scale with the diode's impedance [E].

**For the imager, the SNR at a known irradiance is the test.** The camera's sensitivity follows from its per-pixel SNR at a known irradiance, measured as EMVA 1288 prescribes; Luo et al.'s per-pixel SNR (§S2.5) follows the same idea. Whether the readout limits Li et al.'s imager depends on numbers the paper does not give [E, `measurement_budget.py`]:
- If the pixels leak like the 1 mm² test diode, a 15 µm pixel collects $1.23\times10^{-4}\ {\rm A\,cm^{-2}}\times(15\ \mu{\rm m})^2\times2\ {\rm ms}/q=3.5\times10^{6}$ dark electrons in the 2 ms integration, with a shot noise of up to $\sqrt{3.5\times10^{6}}=1{,}860$ e⁻. The readout's own temporal noise adds to this in quadrature (EMVA 1288, Eq. 30), so it matters only if it approaches that level.
- With white noise alone the pixel would reach $1.6$–$2.0\times10^{11}$ Jones at 2.5 µm: $\mathcal{R}/\sqrt{2qJ}=0.976/\sqrt{2\times1.602\times10^{-19}\times1.23\times10^{-4}}=1.6\times10^{11}$ Jones for full shot noise of the dark current, and $2.0\times10^{11}$ with the noise model of §S2.4. That is close to the corrected zero-bias value (§S2.7).
- The well has to be sized for this dark charge, but that is a design choice rather than a limit. $3.5\times10^{6}$ electrons is 6.3 times the 550 ke⁻ largest well of SWIR Vision Systems' 15 µm readout (§S3.3), which this dark current would fill in 0.32 ms. That readout, however, serves dots that leak $2.5\times10^{4}$ times less (§S1.3), and its three gains already span 25–550 ke⁻.
- An analog well is the integration capacitance times its voltage swing, $Q_{\rm max}=C_{\rm int}\Delta V$, so the process's capacitance density and voltage set the limit. Lincoln Laboratory puts it below $2.5\times10^{7}$ electrons in a 30 µm pixel, for example with 0.8 pF at 5 V, the capacitor taking most of the pixel (Schultz et al. 2014, pp. 38–39) [I]. Scaled by area to a 15 µm pixel that is about $6\times10^{6}$ electrons, and imec's 5 µm pixel, which holds 782 ke⁻ in 108 fF (Chu et al., p. 6 and Table 1), scales to 0.97 pF and $7\times10^{6}$ electrons [E]. A readout for this diode is therefore feasible, and Li et al.'s must hold several million electrons unless its pixels leak less than the test diode.
- The price of the larger capacitor is conversion gain. The reset noise $\sqrt{k_BTC}/q$ is 400 e⁻ at 1 pF if correlated double sampling does not remove it, and the readout chain's voltage noise, referred to the pixel, grows in proportion to $C$: at 1 pF, 300 µV rms of chain noise would equal the dark shot noise. Below that, the deeper well costs little, because the dark shot noise dominates anyway [E].
- Long-wave infrared readouts meet the same problem with background current: a 300 K scene seen at f/2 fills a 25-million-electron well in about 0.3 ms. Digital pixels, which count charge packets of about 6,000 electrons in an in-pixel counter, remove the capacitor limit (Schultz et al., pp. 38–39) [I]. Subtracting most of the dark current in the pixel before integration, as TriEye's patents do (main report §A7.5), saves the well but not the shot noise.
- Fixed pattern would dominate the temporal noise. Every 1% of pixel-to-pixel spread in that leakage is 35,000 e⁻, 19 times the shot noise, and at −0.1 V each millivolt of spread in the bias that the input stage holds moves the leakage by 0.8–1%, almost all of it through the ohmic part [E]. The dark-frame correction and its stability with temperature therefore set the usable floor.
- The 62 dB that the paper quotes is read from images of a 36-step greyscale card, plotted as pixel level over 255 against exposure (Fig. 4d; p. 7). It is not the ratio of saturation to the noise floor that EMVA 1288 defines (Eq. 28), so it does not reveal the readout noise.

---

## S3. The sensor routes

### S3.1 InGaAs on InP

**How it works.** In₀.₅₃Ga₀.₄₇As grows lattice-matched on InP and absorbs to ≈1.7 µm. InP, with a 1.34 eV band gap, absorbs below 0.92 µm, so standard sensors start at about 0.9 µm, and visible-extended sensors respond from 0.4 µm [E; S]. The detector array is grown on InP and joined pixel by pixel to a silicon readout chip, traditionally with indium bumps; Sony's SenSWIR parts use Cu–Cu bonding [T; S]. Raising the indium fraction moves the cut-off to 2.2–2.6 µm at the price of lattice mismatch and dislocations, which is why extended InGaAs leaks about 10⁴ times more than standard InGaAs (§S1.3 table) [P/E].

**Products and pitch.**
- Sony's IMX990 and IMX991 (1.34 and 0.34 megapixels) use Cu–Cu bonding at 5 µm pitch [T, TechInsights].
- Sony's IMX992 and IMX993 (5.32 and 3.21 megapixels, 1/1.4-type and 1/1.8-type) reach 3.45 µm, which Sony calls the smallest pixel among InGaAs SWIR sensors. They respond from 0.4 to 1.7 µm and are aimed at industrial equipment [S, Sony press release, 28 Nov 2023].
- Sony's 5 µm Cu–Cu pixel of IEDM 2019 (Manda et al.) leaks about 2.5 nA cm⁻², as imec reads it from that paper's graph; the temperature of the value is not given [S, Chu et al., Table 2].
- Other InGaAs camera and array makers include Teledyne, Sensors Unlimited (Collins Aerospace), SCD, Lynred, Xenics and Hamamatsu [U].

**Cost.** Processed InP costs 10–100 times as much as silicon per mm², before the cost of hybridization (main report §C4c subsection 3) [I/E]. A 1.3-megapixel array at 5 µm pitch covers $1.3\times10^{6}\times(5\ \mu{\rm m})^2=33\ {\rm mm^2}$, i.e. about €33–330 of processed InP at 1–10 €/mm². The same area of stacked silicon costs about \$3 at the ≈\$0.1 per mm² of a Sony SPAD die (main report §C4c subsection 3) [E].

**Automotive status.** No InGaAs camera is in a series car. The one SWIR detector that reached vehicles was Argo AI's InGaAs/InP SPAD lidar, of which about 400 units were built before Argo closed in 2022 (main report §C4c subsection 3) [P].

### S3.2 Germanium on silicon

**How it works.** Germanium absorbs to about 1.6 µm through its direct gap, which the tensile strain of Ge on Si lowers, and it can be grown or bonded on silicon wafers in CMOS fabs. The 4.2% lattice mismatch brings dislocations that raise the leakage. TriEye's patents describe bonding single-crystal germanium-on-insulator to avoid them (main report §A7.5) [P]. Germanium is the leakiest route here at room temperature, 204 µA cm⁻² in TriEye's pixel, which TriEye handles with gated integration and dark-current subtraction inside each pixel (main report §A7.5) [P/E].

**Products.**
- TriEye's TES200 ("Raven") has 1,236 × 960 global-shutter pixels at 7 µm. It is sensitive from 700 to 1,650 nm, has a quantum efficiency of 60% at 1,245 nm, draws 500 mW and is made by Tower Semiconductor (main report §A7.5) [P].
- For ranging rather than imaging, Sony has shown a 400 × 300 Ge-SPAD direct-ToF sensor (ISSCC 2026), and Artilux makes Ge–Si SPADs (main report §C4c subsection 4) [P/I].
- Other germanium imagers are few.
  - NoblePeak Vision's TriWave (around 2010) had 744 × 576 pixels at 10 µm, with 44% quantum efficiency at 1.3 µm and a 5-electron noise floor. Its diodes leaked 25 fA per pixel at −45 °C at wafer probe, which is 25 nA cm⁻² [S; E].
  - Artilux and II-VI (now Coherent) showed a germanium–silicon 3D camera at 1,380 nm in 2022, in the same solar-blind band as TriEye's laser, without a published resolution [P].
  - STMicroelectronics and CEA-Leti stacked a 32 × 32 germanium-on-silicon SPAD array on 40 nm CMOS, with the germanium growth tuned to reduce dislocations (IISW 2023) [I].
  - No megapixel germanium imager other than TriEye's was found.

**Automotive status.**
- TriEye counts Porsche as an investor, an evaluation by Denso and a collaboration with Hitachi Astemo; no series programme is public.
- The TES200 was available in sample quantities in August 2025, and AM General showed TriEye's cameras on a special-operations vehicle in October 2025 (main report §A7.5) [P/T].

### S3.3 Colloidal quantum dots and other thin films

**How it works.** Semiconductor nanocrystals a few nanometres across absorb up to a wavelength set by their size. A film a few hundred nanometres thick is coated directly onto a finished CMOS readout wafer, so no hybridization is needed, and pixel pitch and cost follow silicon. Two limits come with the thin film.
- **Weak absorption.** Absorption coefficients are a few 10³ cm⁻¹, so a 200 nm HgTe film absorbs only about 10%, and resonant cavities that raise absorption 3–10 times are the usual remedy (Sergeeva et al., pp. 13–14) [I].
- **Thickness limited by transport.** Carriers hop between dots, so a thicker film collects less, and EQE falls when hopping slows in the cold (Luo et al., Fig. 3; Gregory et al., p. 3) [I; P].

**PbS quantum dots from SWIR Vision Systems (now onsemi).** The company's Acuros cameras use a PbS-dot photodiode with its excitonic peak near 1,500 nm on a 15 µm readout. The readout has three gains (full wells of 550, 110 and 25 ke⁻), a global shutter and 60 frames/s in HD (Gregory et al., p. 2) [P].
- **Leakage.** About 5 nA cm⁻² at 25 °C on 15 µm pixels, at a reverse bias below 0.1 V (p. 2; Table 2) [P]. That is the InGaAs level, and the radiative floor of Eq. \eqref{eq:swir-radiative-floor} shows it is physically plausible (§S1.3).
- **Quantum efficiency.**
  - The product reaches about 15% at the 1,480 nm excitonic peak and about 10% at 1,550 nm (Fig. 1, read by eye).
  - An improved test diode reaches about 42% at its peak and about 26% at 1,550 nm, with 8 nA cm⁻² of dark current (Fig. 3, read by eye).
  - The paper's outlook and Table 2 quote up to 45% at 1,550 nm, depending on the diode type, but no figure shows it.
- **Noise.** Total dark noise is 65–183 e⁻ at 30 °C and 16.6 ms, and the diode's dark current matters only beyond about 20 ms (p. 2; Table 1).
  - The table's dynamic range does not follow from its own entries in two modes: $20\log_{10}(25{,}000/65)=51.7$ dB in high gain, where 32 dB is printed, and 63 dB in medium gain, where 67 dB is printed [E].
- **Extended SWIR.** Cameras that respond to 2.1 µm are offered with dark currents of about 5 nA cm⁻²; §S1.3 explains why that figure cannot be $J_0$ without an exceptional radiative efficiency.
- **Speed.** A 0.2 mm test diode gave 1.0 ns rise and 2.8 ns fall (10–90%) on 3–5 ns Nd:YAG pulses. That beats the InGaAs reference photodiode beside it (2.5 and 5.8 ns), so the circuit or the laser likely set both (Fig. 5) [P; E].
  - The test wavelength is not stated; Nd:YAG lases at 1,064 nm.
  - Table 2's bandwidth above 350 MHz uses only the rise time; the 2.8 ns fall corresponds to about 120 MHz [E].
  - A single measurement showed the 0.94 ns delay of a 28 cm path change, with 16 averages (Figs. 6–7).
  - The diode has no gain, so as a lidar receiver it would be limited by amplifier noise, like a linear InGaAs PIN (main report §C4b).
- **Reliability.**
  - Test diodes stored at 85 °C and 85% relative humidity for more than 1,000 h kept their 1,550 nm QE within about 6% and their dark current within 76–104% of the initial values (Fig. 8).
  - HD sensors stored at 75 °C and 85% relative humidity drifted by about ±10–15% in response (Fig. 9).
  - Testing at 105 °C for automotive use had been started, with no data shown (p. 7).
  - These are storage tests. Automotive qualification under AEC-Q100 also requires biased humidity tests, high-temperature operating life and temperature cycling, none of which is reported, and no leakage is measured at an elevated operating temperature.
- **Ownership.** onsemi completed its purchase of SWIR Vision Systems in July 2024 and plans to combine the dots with its CMOS sensor manufacturing to lower the cost of SWIR sensors [S, onsemi release]. onsemi also makes automotive image sensors (main report §A7.4). The release does not name automotive use; the 2022 paper names automotive direct time-of-flight sensing as an opportunity (p. 1).

**PbS quantum dots from other makers.**
- **STMicroelectronics** presented a global-shutter sensor with 1.62 µm pixels at IEDM 2021 (Steckel et al.), with 60% quantum efficiency and 99.98% shutter efficiency at 1,400 nm, made on a 300 mm toolset [S]. imec recalculates its dark current as 0.3–0.51 µA cm⁻² (Chu et al., Table 2) [I]. ST planned samples for 2022, aimed at mobile devices; no product was found. The HgTe review lists ST as in development in its Table 2 but its text puts ST cameras on the market (Sergeeva et al., pp. 21 and 23) [I].
- **imec** showed 1.82 µm PbS-dot pixels on a 130 nm readout at IEDM 2020, with 18% EQE at 1,400 nm and a target of 50% [T].
- **Emberion** (Finland and UK) combines graphene with quantum dots on CMOS; its VS20 camera, shown in 2021, covers 400–2,000 nm, and it raised €6 M in January 2022 [T]. Its later status was not found.
- **Quantum Solutions** sells a PbS-dot array, **Qurv**, an ICFO spin-off, develops PbS–Ag₂Te cameras, and **QDI Systems** develops PbS arrays (Sergeeva et al., Table 2) [I].

**Lead-free InAs quantum dots.**
- **imec** (Chu et al., *Sensors* 2025) built 768 × 512 pixels at 5 µm on a 0.13 µm readout, a thin-film photodiode on a three-transistor pixel with dual conversion gain, collecting holes at −3.2 V (pp. 4–6; Table 1) [I].
  - The InAs stack, with a 200 nm film, reaches 28% EQE at 1,200 nm. The In(As,P) stack for 1,400 nm, with a 100 nm film, reaches 4.8% and stays flat at about 4.5% from 1,100 to 1,380 nm, so part of its shortfall is the thinner film (p. 4; Fig. 10).
  - The dark current is 23.6 and 80 µA cm⁻². Read noise is 52.2 e⁻ in high gain, full wells are 71.9 ke⁻ and 782 ke⁻, PRNU is 8.1% and 3.5%, and the dynamic range is 83.5 dB, $20\log_{10}(782{,}000/52.2)$, the low-gain well over the high-gain noise. Every figure is at room temperature (Table 1).
  - The 52.2 e⁻ is close to the reset (kTC) noise of the 20 fF node, $\sqrt{k_BTC}/q=57$ e⁻ at 300 K, although the paper credits its digital correlated double sampling with suppressing that noise [E].
  - The response flattens toward full well, falling to about 45% as the diode bias drops from 3.2 to 2 V (Fig. 8a).
  - The smoke demonstration (Fig. 11) is a bench-top box, consistent with small particles scattering less at 1.2 µm (§S1.2).
- **Sony** (Enoki et al., IEDM 2024, all eight authors at Sony Semiconductor Solutions) spin-coats InAs dots on readout wafers in an inert atmosphere at low temperature and patterns them by lithography and dry etching. Film thickness varies by about 2% and EQE by 8% across the wafer (Figs. 3–9) [I].
  - Dots with a 940 nm peak reach about 40% EQE at about 10 nA cm⁻² at 1 V.
  - Dots with a 1,450 nm peak reach 15% at −1.5 V, falling steadily toward zero bias, with about 10⁻⁴ A cm⁻² of dark current; at the test illumination the light current exceeds the dark current only 2–3 times (Fig. 10, read by eye).
  - The 10–90% response times are below 30 µs, but about 5–8% of the signal follows over roughly a millisecond, a source of image lag (Fig. 11).
  - The only image is taken through a 940 nm filter (Fig. 14). The paper gives no pixel pitch, array format or temperature data, and it aims at consumer devices, citing RoHS as the motive (p. 1).
- **What the two show together.** At the same band gap the InAs dots leak about 10⁴ times more than PbS dots, and the scaling with gap points to traps (§S1.3, Eq. \eqref{eq:swir-gr-scaling}). Lead-free dots therefore trade the regulatory problem of §S3.6 for leakage at the germanium level.

**Other lead-free dots.** Ag₂Te dots from ICFO and Qurv cover 350–1,600 nm in a photodiode with a claimed detectivity of about 10¹² Jones, a linear dynamic range above 118 dB and a bandwidth above 110 kHz, and were integrated with a CMOS readout as a proof of concept (Wang et al., *Nature Photonics* 2024) [T]. How their noise was measured has not been checked. Sony's comparison places them at about 30% EQE near 1,400 nm (Enoki et al., Fig. 13) [I].

**HgTe quantum dots.** HgTe is the only colloidal material that reaches the mid-wave infrared through interband transitions; in the SWIR it competes with PbS and with III–V dots (Sergeeva et al., p. 3) [I].
- **Performance.** Room-temperature SWIR HgTe photoconductors sit in the high 10¹⁰ Jones range, one to two orders below HgCdTe, InGaAs and InSb, and extended-SWIR photodiodes reach about 10¹¹ Jones (p. 17). Room-temperature SWIR arrays span 2.8×10¹⁰ to 2×10¹¹ Jones; the highest uses a trapping-mode photoconductor whose 175% EQE means gain (Table 1, p. 22).
- **The megapixel array.** Luo et al. (*APL Photonics* 2023) put an HgTe photoconductor on a CMOS readout as 1280 × 1024 pixels at 15 µm, with a resonant cavity formed by the chip's own pixel metal and passivation, a 2 µm cut-off and 2.5 V bias [I].
  - They report 0.23 A W⁻¹, 14.3% EQE, 5.04 µA cm⁻² of dark current and 2.8×10¹⁰ Jones (Table I), the detectivity computed from measured pixel signal-to-noise ratios (§S2.5).
  - The 600 °C blackbody irradiance of 216 µW cm⁻² is not stated as total or in-band, and only about 3% of that blackbody's power lies below 2 µm [E].
  - The 42 and 40 lp/mm read off an ISO-12233 chart (p. 7) exceed the 33.3 lp/mm Nyquist limit of a 15 µm pitch, $1/(2\times0.015\ {\rm mm})$, beyond which bar patterns alias [E].
  - The cavity is credited with tripling EQE by comparison with another group's array, while the authors' own cavity-free pixel from the same process reaches 12.4% against the array's 14.3% (Table I).
  - Cooling from 20 to −60 °C halves the response as hopping slows, while the dark current falls only 20–25% (Fig. 3); no data above room temperature are given.
  - The corresponding author is at Zhongxinrecheng, which the review lists as selling HgTe arrays and cameras; the paper declares no conflict of interest.
- **Industry.** The review counts PbS-dot cameras from SWIR Vision Systems, Emberion and Quantum Solutions as commercial and HgTe only from Zhongxinrecheng, with NIT, Sivananthan Labs and QDIR in development (Table 2, p. 23). It notes that the SWIR field sells only a few thousand cameras a year, which makes wafer-scale processing questionable at that volume, and it rates HgTe sensors at technology readiness 3–5 and manufacturing readiness 1–3 (pp. 21–24). An estimate it cites puts a quantum-dot array at €10–20 against €600 for an InGaAs array plus €600 for its lens (p. 20) [I].
- **For cars.** HgTe works in the 2–2.5 µm band, contains mercury and has no published data above room temperature, so it is not an automotive candidate.

### S3.4 Bulk lead-salt films

Chemical-bath PbS and PbSe photoconductors are decades old; Referee #1 of Li et al. cites literature from 2001–2008 (Peer Review File p. 1) [I]. Three precedents bracket Li et al.'s contribution.
- **trinamiX**, a BASF subsidiary, sells printed PbS and PbSe photoconductors as single pixels and as line arrays of up to 512 pixels. The PbS single pixel is specified at 22 °C with a 2.7 µm peak, a 2.9 µm cut-off, 1×10¹¹ Jones typical and 0.8×10¹¹ minimum, a 200 µs time constant and 0.3–3 MΩ of dark resistance. The datasheet forbids element temperatures above 70 °C, a warning for lead-salt films under automotive heat [P].
- **Zogg's group at ETH Zurich** grew PbTe photodiode arrays by molecular-beam epitaxy on finished CMOS readout chips: 96 × 128 pixels at 75 µm pitch with a cut-off near 5.5 µm, reported in 2003. Each threading dislocation acted as a shunt of about 1 GΩ [S].
- **NIT** (Spain) deposits PbSe from the vapour phase on 200 mm CMOS wafers for uncooled mid-wave arrays, starting with 80 × 80 pixels at 135 µm pitch in 2013 [S].

Li et al.'s contribution is therefore a photodiode rather than a photoconductor, grown from water at room temperature on a readout chip with controlled crystallinity and a high SWIR EQE (§S2). The authors also show a PbSe extension (Extended Data Fig. 9) [I]. Bulk lead salts have narrow gaps, about 0.45 eV for the PbS of Li et al., so they suit the extended SWIR and the mid-wave infrared, not automotive work at 1.3–1.6 µm (§S2.7).

### S3.5 Cooled, avalanche and photon-counting detectors

- **HgCdTe.** Its band gap can be tuned from the SWIR to the long-wave infrared, and Teledyne makes 320 × 256 SWIR arrays with about 85% peak QE and 99.9% operability [S]. Leonardo's SAPHIRA is a 320 × 256 electron-avalanche array at 24 µm pitch covering about 0.8–2.5 µm. Its gain can be set to several hundred, which makes the read noise sub-electron at frame rates of about 1 kHz, and it runs near 85 K [S].
- **Type-II quantum wells and superlattices.** Sumitomo Electric's InGaAs/GaAsSb quantum-well arrays on InP reach cut-offs of 2.35–2.5 µm, with dark current below 1 µA cm⁻² at 213 K, diffusion-limited and comparable to HgCdTe, in work from around 2017 [S]. Other extended-SWIR superlattices on InP exist, for example that of Liang et al. (*Appl. Phys. Lett.* 2024) [I, title-level].
- **InGaAs/InP SPAD arrays.**
  - At 300 K they show dark counts of 2.5×10³–6×10⁴ s⁻¹ µm⁻² and a ceiling of ≈10⁶ counts s⁻¹ set by afterpulsing. Argo AI used 512 × 2 arrays in its lidar, and Yildirim et al. (2026) gate a 96 × 96 array in nanoseconds (main report §C4c subsection 3) [I/P].
  - Fraunhofer HHI's 96 × 96 array at 25 µm pitch has SPADs of 15 µm diameter with a median dark count of 87 kcps at room temperature [S].
- **Low-noise linear APDs.** Phlux Technology, a Sheffield spin-out, sells InGaAs APDs of 30–200 µm diameter with 0.98 A W⁻¹ at 1,550 nm and gains up to 120, quoting excess-noise factors of 1.08 at a gain of 10 and 1.86 at 40 [T/S]. These lie below the floor of the standard theory (below).
- **Ge-on-Si SPADs.** These are covered in main report §C4c subsection 4 and in §S3.2.

McIntyre's local model of avalanche noise gives

$$F=kM+(1-k)\left(2-\frac{1}{M}\right) \label{eq:swir-mcintyre}$$

where $F$ is the excess-noise factor, $M$ the gain and $k$ the ratio of the hole to the electron ionization coefficient. Even with $k=0$, $F\ge2-1/M$, which is 1.90 at $M=10$ and 1.98 at $M=40$ [E]. Values below that floor are possible only where dead-space effects in a very thin multiplication region break the local model, as they do in HgCdTe electron APDs. The definition and measurement behind Phlux's figures therefore deserve a check (§S5).

None of these is a candidate for an automotive camera. In the SWIR, photon counting and avalanche gain are topics for lidar receivers, and cooled arrays are military, scientific and industrial products.

### S3.6 Lead, mercury and the law

PbS, PbSe and HgTe films put a restricted metal on the sensor. The quantity is tiny, but the European rules limit concentration, not mass, and for cars the governing law is the End-of-Life Vehicles (ELV) Directive rather than RoHS.

**Which law applies.** RoHS (Directive 2011/65/EU) does not apply to means of transport for persons or goods (Article 2(4)(f)) [P]. Vehicles fall under the ELV Directive (2000/53/EC). Its Article 4(2)(a) bans lead, mercury, cadmium and hexavalent chromium in vehicle materials and components unless an entry in Annex II allows them, and Annex II tolerates up to 0.1% lead by weight in each homogeneous material, the same limit as RoHS [P].

**Why a thin film does not escape.**
- **Inside the layer.** PbS is $207.2/(207.2+32.06)=86.6\%$ lead by weight, 866 times the limit, and dot films with ligands stay far above it [E].
- **Is the film its own material?** The Commission treats as homogeneous any material that cannot be separated mechanically, and it counts abrasion as mechanical [I, Danish EPA summary of the Commission's interpretation]. A deposited film can be ground off, so under the strict reading it is its own material.
- **Even averaged over the die.** Semiconductor material declarations list the die as one material, which is the most lenient reading. Averaged through the silicon beneath it, the lead fraction is

$$w_{\rm Pb}=\frac{t_f\,\rho_{\rm PbS}\,w_{\rm Pb,PbS}}{t_f\,\rho_{\rm PbS}+t_{\rm Si}\,\rho_{\rm Si}} \label{eq:swir-lead-fraction}$$

where $t_f$ and $t_{\rm Si}$ are the film and die thicknesses, $\rho_{\rm PbS}=7.6$ and $\rho_{\rm Si}=2.33$ g cm⁻³ the densities, and $w_{\rm Pb,PbS}=0.866$ the lead fraction of PbS. With assumed die thicknesses it gives [E, `lead_content.py`]:

| PbS film | 775 µm die | 300 µm die |
|---|---|---|
| 0.2 µm | 0.073% | 0.19% |
| 0.3 µm | 0.11% | 0.28% |
| 0.8 µm (Li et al.: 500 + 300 nm) | 0.29% | 0.75% |

For example, for 0.8 µm on 775 µm, $0.8\times7.6\times0.866/(0.8\times7.6+775\times2.33)=5.27/1812=0.29\%$. Laser Components, which makes PbS and PbSe detectors, likewise says the lead content of its detectors lies just above the threshold, which is why they fall under RoHS [P, FAQ, October 2022].

**The absolute amount is small.** Li et al.'s 640 × 512 array at 15 µm holds $73.7\ {\rm mm^2}\times0.8\ \mu{\rm m}\times7.6\ {\rm g\,cm^{-3}}\times0.866=0.39$ mg of lead [E]. A car's 12 V lead–acid battery, exempted by ELV Annex II entry 5(b), holds kilograms.

**Thin films have needed exemptions before.** Lead in the PZT dielectric of capacitors inside integrated circuits has its own entries, ELV Annex II 10(b) and RoHS Annex III 7(c)-IV [P; I, TÜV SÜD 2019]. Lead-salt infrared detectors rely on RoHS Annex IV entry 1c, which covers lead, cadmium and mercury in infrared light detectors [P].

**What is allowed today.**
- **Medical and industrial instruments.** Entry 1c applies only to these RoHS categories (8 and 9). Laser Components gave its expiry as July 2021 for medical use and July 2024 for industrial use (note, January 2020) [P].
  - Its 2022 FAQ says the reviewing institute recommended renewing the entry for seven years and that the old exemption stays valid until the Commission decides [P].
  - The Commission published a draft amending Annexes III and IV on 8 July 2026 [T]; its effect on entry 1c is an open item (§S5).
- **Consumer products.** Laser Components says coverage outside medical and industrial use ended in July 2018 and that an extension request was filed; no outcome was found [P].
- **Cars.** The ELV Annex II text checked here, the EU text as it stood at the end of 2020, has no entry for infrared detectors or photodetectors [P]. The nearest, 10(a), covers lead in glass or ceramic, a stretch for a semiconductor film. A PbS camera built into a new car would therefore need a new entry; amendments after 2020 were not checked.

**Can an exemption be had?**
- **The test.** RoHS grants an exemption when substitution is scientifically or technically impracticable or the substitutes are not reliable (Article 5(1)(a)), and the ELV Directive allows an entry where the use of the substance is unavoidable [P].
- **The evidence supports one today.** At 1,400–1,450 nm the lead-free dots give 4.8–15% EQE at 80–100 µA cm⁻², about 10⁴ times the leakage of PbS dots (§S3.3). Laser Components won its renewal on the same argument, that PbS and PbSe could not be replaced [P].
- **Entries end when substitutes arrive.** In the same review, PZT pyroelectric detectors were granted only six more years, with a recommendation to switch to LiTaO₃ [P].
- **Regulators have refused quantum dots before.** In May 2015 the European Parliament rejected, 618 votes to 33, an extension of the exemption for cadmium quantum dots in displays [T, Display Daily], and the display industry moved to cadmium-free InP dots (Sergeeva et al., p. 23) [I].

For an automotive programme, lead is therefore a programme risk rather than a physical one:
- no ELV entry exists, and obtaining one takes years of consultation and review;
- any entry would be time-limited, while vehicle programmes and their spare-part obligations run for a decade or more;
- every gain in InAs dots, now pursued by imec and Sony, gives regulators a substitute to point to.

Mercury in HgTe dots raises the same question, and Annex IV entry 1c covers it only for medical and industrial instruments.

---

## S4. Automotive outlook

**What SWIR can do for a car.** It can image actively under an eye-safe illuminator: TriEye's choice of 1,375 nm puts the laser where ground-level sunlight is about 2,500 times weaker than at 1,550 nm, and no erbium amplifier is needed or possible there (main report §A7.5). It can also see through haze and smoke better than visible light (§S1.2). The other side is that every SWIR camera sees the 1,550 nm light of other cars' lidars, which may dazzle it and whose damage threshold for SWIR sensors is unknown (§S5).

**What it does not do.** It gives no passive night vision worth having (§S1.1) and little help in fog (§S1.2). Its niche must beat three established competitors: near-infrared gated CMOS at 800–860 nm, which uses silicon (BrightWay, main report §A7.5); thermal cameras for passive night vision and fog (main report §A5, §A7.7); and lidar for range.

**How the routes rank for cars.**
1. **PbS quantum dots on CMOS** (SWIR Vision Systems, now onsemi) have the strongest case on paper.
   - They leak about 5 nA cm⁻² at 25 °C, the InGaAs level and about 4×10⁴ times less than germanium.
   - They are coated at wafer scale, their owner supplies automotive image sensors, and their published storage tests are the most extensive for any thin film (§S3.3).
   - Against them, the product reaches only about 10% QE at 1,550 nm, no leakage above room temperature is published, qualification has not been shown, and lead requires a new ELV entry (§S3.6).
2. **Germanium on silicon** (TriEye with Tower) is the only route with an automotive-oriented product and a gated active-imaging concept (SEDAR). Its weakness is room-temperature leakage of ≈200 µA cm⁻², which gating and in-pixel subtraction manage. No carmaker has announced it.
3. **InGaAs** gives the best images, but at 10–100 times the cost of silicon per mm², and its room-temperature advantage in leakage disappears by about 100 °C (§S1.3).
4. **Lead-free InAs quantum dots** (imec, Sony) avoid the lead problem but leak at the germanium level, about 10⁴ times more than PbS dots of the same gap, and reach 4.8–15% EQE near 1.4 µm. Sony has not yet shown a SWIR image (§S3.3).
5. **Extended-SWIR absorbers** (extended InGaAs, bulk PbS, HgTe dots) are in the wrong band for cars and leak 10³–10⁴ times more than standard InGaAs; HgTe adds mercury.
6. **Cooled, avalanche and photon-counting arrays** are not camera candidates.

**Barriers common to every route.** These are the dark current at 85–105 °C, which no thin-film sensor has published (§S1.3); the windshield's transmission at 1.3–1.6 µm; interference from and possible damage by other cars' 1,550 nm lidars; and automotive qualification. Lead and mercury add a regulatory barrier for the lead-salt and quantum-dot routes, including the one that ranks first on leakage (§S3.6). None of these is settled in the sources read for this survey (§S5).

**Verdict.** On this evidence, SWIR cameras are unlikely to matter for cars at this stage. The four findings behind that verdict are set out at the start of this side note.

---

## S5. What to dig into next

The list is ordered by how much each item could change the conclusions above.

1. **The noise measurement of Li et al.** Establish which diode the 2.19×10⁻¹³ A Hz⁻¹ᐟ² was measured on, and obtain its dark I–V near 0 V. Then establish the SR570's sensitivity, gain mode, filters, bias-voltage and offset-current settings and calibration state, and how the SR850's noise reading was normalized: the X-channel or the magnitude, the equivalent noise bandwidth of the time-constant filter, and one-sided or two-sided density. Errors of a factor of about 2 are easy to make in each. The decisive tests are the resistor calibration, the admittance measurement and the current injection of §S2.5, within the protocol of §S2.8.
2. **The rest of the Peer Review File.** Only the reviewer reports and the threads on noise and detectivity (pp. 1–2, 26–28, 118–119) were read for this side note. The rebuttals on materials, cost and stability remain unread.
3. **Arslan et al. 2014** (*IEEE J. Quantum Electron.* 50, 957). Check at what temperature and wavelength they report the ≈1.7×10¹¹ Jones that Li et al. call uncooled.
4. **The group's earlier detectivity practice.** Check whether Liu et al. (*Nat. Electron.* 2022), a PbS-dot imager quoted at 2.1×10¹² Jones in its preprint, and the group's other papers use the same SR570 chain and noise decomposition. Then check whether their detectivities pass the $4k_BT/R_0$ test and the bound of Eq. \eqref{eq:swir-r0a-radiative} against their own I–V and EQE data.
5. **Leakage at temperature.** No thin-film sensor has published leakage above room temperature. The data to obtain are:
   - SWIR Vision Systems' 105 °C results, begun by 2022, with dark current and QE measured at 85–105 °C rather than after storage;
   - the same for the InAs sensors of imec and Sony, and for TriEye's TES200 from a datasheet;
   - InGaAs arrays, from the Sony IMX990/992 datasheets, SCD and Teledyne;
   - Li et al.'s array dark current and readout full well.
6. **Sony's SWIR InAs imager.** Its pixel pitch, array format, a SWIR image and data versus temperature.
7. **The extended-SWIR dark current of SWIR Vision Systems.** The bias and J–V behind the quoted 5 nA cm⁻² for 2.1 µm diodes, to place it against the radiative floor of §S1.3.
8. **Windshields.** Find the transmission of standard laminated and solar-control (infrared-reflective) windshields from 1.0 to 1.7 µm. Patents by glass makers describe special zones for 905 and 1,550 nm lidars, which suggests ordinary glass is a problem.
9. **Fog and haze.** Read Mehra et al. (ICCVW 2025) in full, and find measured droplet spectra for Cerema's radiation and advection fogs and SWIR-versus-visible contrast measurements (for example Judd et al., SPIE 2019).
10. **Lidar dazzle and damage of SWIR sensors.** No data were found on what 1,550 nm lidar pulses do to InGaAs, germanium or quantum-dot pixels, which absorb that light efficiently, unlike the silicon sensors of main report §C4c subsection 1.
11. **Lead and mercury.** Establish whether anyone has applied for an ELV Annex II entry for lead in infrared detectors, what the July 2026 draft does to RoHS Annex IV entry 1c, and whether a consumer exemption exists. Check how vehicle rules outside the EU treat lead in sensors, and the status of mercury for HgTe.
12. **Company status.** Check onsemi's SWIR roadmap after the acquisition and ST's Quantum Film product status. Check Emberion after 2022, and Quantum Solutions, Qurv and QDI Systems. TriEye's 2026 status is already an open item of the main report.
13. **Cost and export controls.** Find SWIR camera module prices at volume. Check the export-control classification of InGaAs focal-plane arrays against quantum-dot sensors, which SWIR Vision Systems marketed as globally exportable [S].
14. **Uses that need the water bands.** SWIR may detect water and ice on the road through the absorption bands of water. No automotive product using them was checked.
15. **Claims in the wider survey.** Check the definition and measurement behind Phlux's excess-noise factors against Eq. \eqref{eq:swir-mcintyre}, the noise protocol behind the Ag₂Te dots' 10¹² Jones, and SWIR Vision Systems' 45% QE at 1,550 nm, which no figure shows.
16. **HgCdTe electron-APDs and extended-SWIR type-II superlattices.** Survey these only for completeness.

---

## Sources

**Li et al. and its supplementary files**
- Li, S., Liu, J., Gao, L. *et al.* Monolithically and in situ integrated PbS infrared imagers. *Nature* (2026), https://doi.org/10.1038/s41586-026-11222-y (pp. 1, 5–7, 9–10; Figs. 3 and 4)
- Supplementary Information: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-11222-y/MediaObjects/41586_2026_11222_MOESM1_ESM.pdf (pp. 31, 33–35, 49–50; Supp. Figs. 18–20; Supp. Tables 10 and 11; Eqs. S30–S34)
- Peer Review File: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-11222-y/MediaObjects/41586_2026_11222_MOESM2_ESM.pdf (PDF pp. 1–2, 26–28, 118–119)
- Source Data, Fig. 3: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-026-11222-y/MediaObjects/41586_2026_11222_MOESM4_ESM.xlsx (sheets Fig 3b, 3c, 3e, 3f)
- Arslan, Y. *et al.* 640 × 512 extended short wavelength infrared In0.83Ga0.17As focal plane array. *IEEE J. Quantum Electron.* 50, 957–964 (2014) (cited by Li et al. as ref. 44; not read)
- Liang, Y. *et al.* InP-based high-performance extended short wavelength p-B-n infrared photodetector with InGaAs/GaAsSb type-II superlattice absorption layer. *Appl. Phys. Lett.* 125, 141103 (2024) (cited by Li et al. as ref. 39; title only)

**Instruments and reference detectors**
- Stanford Research Systems, SR570 Low-Noise Current Preamplifier manual: https://www.thinksrs.com/downloads/pdfs/manuals/SR570m.pdf (Table 1, PDF p. 10; source-impedance rule, PDF p. 11; bias voltage, PDF p. 16; front-end circuit description, PDF p. 26; calibration trims, PDF p. 29; Appendix B, PDF p. 35)
- Analog Devices, AD743 datasheet, Rev. E: https://www.analog.com/media/en/technical-documentation/data-sheets/AD743.pdf (p. 2, specifications; p. 5, noise spectra)
- Texas Instruments, OPA928 datasheet, SBOSA77A (Apr. 2024): https://www.ti.com/lit/ds/symlink/opa928.pdf (pp. 4–5; Figs. 5-40 and 5-41, p. 16)
- Texas Instruments, LMC660/LMC662 datasheet, SNOSC51D (Feb. 2024): https://www.ti.com/lit/ds/symlink/lmc662.pdf (p. 6)
- ADA4530-1 voltage noise and bandwidth as listed by distributors, the datasheet not having been retrieved: https://www.digikey.com/en/products/detail/analog-devices-inc/ADA4530-1ARZ-R7/7404339
- Analog Devices, AD546 datasheet (obsolete part): https://www.analog.com/media/en/technical-documentation/data-sheets/AD546.pdf (pp. 1–2)
- Hamamatsu, InGaAs PIN photodiodes G12183 series, Cat. No. KIRD1119E06 (Mar. 2019), copy hosted by Farnell: https://www.farnell.com/datasheets/2822644.pdf (p. 3)
- Hamamatsu, InGaAs PIN photodiodes G12180 series, Cat. No. KIRD1121J12 (Jan. 2021, Japanese edition), copy hosted by Akizuki Denshi: https://akizukidenshi.com/goodsaffix/G12180-005A.pdf (p. 3 table; p. 5 shunt resistance versus temperature)

**Measurement practice (§S2.8)**
- Pecunia, V. *et al.* Guidelines for accurate evaluation of photodetectors based on emerging semiconductor technologies. *Nat. Photon.* 19, 1178–1188 (2025), https://doi.org/10.1038/s41566-025-01759-1 (pp. 1182–1183 and 1186; Fig. 4; Eq. 5); Supplementary Information, https://static-content.springer.com/esm/art%3A10.1038%2Fs41566-025-01759-1/MediaObjects/41566_2025_1759_MOESM1_ESM.pdf (Supplementary Notes 14, 15 and 18 and Supplementary Fig. 6, SI pp. 46–48 and 51)
- EMVA Standard 1288, Release 4.0 Linear (16 June 2021): https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf (pp. 10–12; Eqs. 15, 21, 26, 28, 29 and 30; §3.2)
- Hamamatsu, Type II superlattice infrared detector P15409-901, Cat. No. KIRD1137E04 (Jul. 2026): https://www.hamamatsu.com/content/dam/hamamatsu-photonics/sites/documents/99_SALES_LIBRARY/ssd/p15409-901_kird1137e.pdf (p. 1)
- Rubiola, E. & Vernotte, F. The cross-spectrum experimental method. arXiv:1003.0113 (2010), https://arxiv.org/abs/1003.0113 (abstract)
- Schultz, K. I. *et al.* Digital-pixel focal plane array technology. *Lincoln Laboratory Journal* 20(2), 36–51 (2014): https://archive.ll.mit.edu/publications/journal/pdf/vol20_no2/20_2_Schultz_v4a.pdf (pp. 38–39; Fig. 3)

**Sensor routes and companies**
- Sony, IMX992/IMX993 press release, 28 Nov 2023: https://sony.mediaroom.com/2023-11-28-Sony-Semiconductor-Solutions-to-Release-SWIR-Image-Sensor-for-Industrial-Applications-with-Industry-Leading-5-32-Effective-Megapixels
- TechInsights on the IMX990/IMX991: https://www.techinsights.com/blog/image-sensor/groundbreaking-senswir-image-sensors-sony-imx990-imx991
- STMicroelectronics blog on the IEDM 2021 sensor: https://blog.st.com/?p=43834 ; IMVE: https://www.imveurope.com/news/sts-quantum-dot-sensor-set-volume-swir-imaging
- imec, IEDM 2020 prototype: https://www.eenewseurope.com/en/quantum-dot-swir-sensor-has-sub-2µm-pixel-pitch ; https://techxplore.com/news/2021-01-thin-film-short-wave-infrared-image-sensor-sub-2m.html
- imec, lead-free InAs quantum dots (IEDM 2024): https://www.eenewseurope.com/en/first-swir-sensor-with-non-lead-quantum-dots ; https://imec-publications.be/entities/publication/a3b5b01c-7117-4462-bc60-094edbb0609a/full
- SWIR Vision Systems, Acuros datasheet: https://www.mouser.com/datasheet/3/101/1/Acuros4-Camera-Datasheet_0124.pdf ; Laser Focus World: https://www.laserfocusworld.com/detectors-imaging/article/14305806/swir-camera-features-a-global-snapshot-shutter-design ; IMVE: https://www.imveurope.com/news/quantum-dot-swir-compete-ingaas
- onsemi, acquisition of SWIR Vision Systems (Business Wire, Jul 2024): https://www.businesswire.com/news/home/20240702703913/en
- Emberion funding (EE Times Europe): https://www.eetimes.eu/?p=23356

**Quantum-dot and HgTe papers read in full**
- Chu, M. *et al.* Wide-dynamic-range lead-free SWIR image sensors based on InAs thin-film quantum-dot photodiodes. *Sensors* 25, 7345 (2025), https://doi.org/10.3390/s25237345 (pp. 3–6 and 9–11; Figs. 8–11; Tables 1 and 2)
- Enoki, O. *et al.* Pb-free colloidal InAs quantum dot image sensor for infrared. 2024 IEEE International Electron Devices Meeting, https://doi.org/10.1109/IEDM50854.2024.10873373 (p. 1; Figs. 3–14)
- Gregory, C. *et al.* SWIR colloidal quantum dot sensor bandwidth and thermal stability: progress and outlook. *Proc. SPIE* 12107, 1210705 (2022), https://doi.org/10.1117/12.2618320 (pp. 1–3 and 7; Figs. 1–9; Tables 1 and 2)
- Luo, Y. *et al.* Megapixel large-format colloidal quantum-dot infrared imagers with resonant-cavity enhanced photoresponse. *APL Photonics* 8, 056109 (2023), https://doi.org/10.1063/5.0145374 (p. 7; Eq. 7; Fig. 3; Table I)
- Sergeeva *et al.* The rise of HgTe colloidal quantum dots for infrared optoelectronics. *Adv. Funct. Mater.* 34, 2405307 (2024), https://doi.org/10.1002/adfm.202405307 (pp. 3, 5, 13–14, 17 and 20–24; Tables 1 and 2)

**Further detectors and benchmarks**
- trinamiX, Hertzstück PbS bare-chip single-pixel datasheet (distributor copy): https://shop.amstechnologies.com/media/d4/32/fe/1720718735/Hertzstueck-PbS-Bare-Chip-Single-Pixel-NIR-Detectors-trinamiX-Datasheet.pdf
- Zogg *et al.*, lead-chalcogenide-on-silicon arrays (review): https://publications.drdo.gov.in/ojs/index.php/dsj/article/view/2205
- NIT, monolithic VPD PbSe array: https://www.ama-science.org/proceedings/details/1633 ; https://www.photonicsonline.com/doc/new-mwir-uncooled-fpa-roic-infrared-technologies-competitive-price-0001
- NoblePeak Vision TriWave: https://medicalimaging.spiedigitallibrary.org/conference-proceedings-of-spie/7660/76603E/Single-photon-imaging-camera-development-for-night-vision/10.1117/12.852646.full
- Artilux and II-VI, 1,380 nm 3D camera: https://www.coherent.com/news/press-releases/ii-vi-incorporated-and-artilux-demonstrate-a-3d-camera-for-enhanced-user-experience-in-the-metaverse
- STMicroelectronics and CEA-Leti, Ge-on-Si SPAD array (IISW 2023): https://imagesensors.org/Past%20Workshops/2023%20Workshop/2023%20Papers/R85.pdf
- Wang, Y. *et al.* Silver telluride colloidal quantum dot infrared photodetectors and image sensors. *Nature Photonics* 18, 236–242 (2024); ICFO release: https://www.icfo.eu/news/2276/non-toxic-quantum-dots-pave-the-way-towards-cmos-shortwave-infrared-image-sensors-for-consumer-electronics-
- Liu, J. *et al.* A near-infrared colloidal quantum dot imager with monolithically integrated readout circuitry. *Nature Electronics* 5, 443–451 (2022), https://doi.org/10.1038/s41928-022-00779-x
- Manda, S. *et al.* High-definition visible-SWIR InGaAs image sensor using Cu–Cu bonding of III–V to silicon wafer. IEDM 2019, https://doi.org/10.1109/IEDM19573.2019.8993432 (not read; value as quoted by Chu *et al.*)
- Tennant, W. E. *et al.* MBE HgCdTe technology: a very general solution to IR detection, described by "Rule 07". *J. Electron. Mater.* 37, 1406–1410 (2008), https://doi.org/10.1007/s11664-008-0426-3
- Leonardo SAPHIRA: https://arxiv.org/pdf/1805.08419 ; https://arxiv.org/html/2409.04247v1
- Teledyne Judson, SWIR HgCdTe 320 × 256 arrays: https://proceedings.spiedigitallibrary.org/conference-proceedings-of-spie/10766/107660J/High-performance-SWIR-HgCdTe-320x256-30%c2%b5m-FPAs-at-Teledyne-Judson/10.1117/12.2501430.full
- Sumitomo Electric, InGaAs/GaAsSb quantum-well arrays: https://ebooks.spiedigitallibrary.org/conference-proceedings-of-spie/10111/1011115/InGaAs-GaAsSb-type-II-quantum-well-focal-plane-array-with/10.1117/12.2254566.full ; https://spie.org/Publications/Proceedings/Volume/10177
- Fraunhofer HHI, 96 × 96 InGaAs/InP SPAD array: https://nanophotonics.spiedigitallibrary.org/conference-proceedings-of-spie/13192/131920V/Room-temperature-96x96-InGaAsInP-SPAD-array-for-SWIR-imaging/10.1117/12.3033437.full
- Phlux Technology APDs: https://compoundsemiconductor.net/article/118841/Startup_Phlux_ships_1550nm_IR_sensors ; Sheffield AlGaAsSb APD work: https://eprints.whiterose.ac.uk/197832

**Regulation**
- RoHS Directive 2011/65/EU: https://eur-lex.europa.eu/eli/dir/2011/65/oj (Article 2(4)(f); Article 5(1)(a); Annex III entry 7(c)-IV; Annex IV entry 1c)
- End-of-Life Vehicles Directive 2000/53/EC: https://eur-lex.europa.eu/eli/dir/2000/53/oj (Article 4(2)); Annex II as it stood at the end of 2020: https://www.legislation.gov.uk/eudr/2000/53/annex/II (entries 5(b), 10(a), 10(b) and the concentration note)
- Laser Components, RoHS note on PbS and PbSe detectors (January 2020): https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/lc-lead-salt/rohs-directives-pbs-pbse.pdf ; FAQ (October 2022): https://www.lasercomponents.com/fileadmin/user_upload/home/Datasheets/lc-lead-salt/questions-rohs-for-pbx-detectors.pdf
- TÜV SÜD on the 2019 RoHS amendments: https://www.tuvsud.com/en-us/e-ssentials-newsletter/consumer-products-and-retail-essentials/e-ssentials-2-2019/eu-rohs-directive-amendments-for-lead-and-cadmium-published
- Danish EPA, homogeneous materials under RoHS: https://www2.mst.dk/udgiv/publications/2009/978-87-7052-987-7/html/kap01_eng.htm
- July 2026 draft amending RoHS Annexes III and IV (ChemLinked): https://chemical.chemlinked.com/news/chemical-news/european-commission-proposes-updates-to-rohs-exemptions-for-lead-and-cadmium-in-eee
- European Parliament vote on cadmium quantum dots (Display Daily): https://displaydaily.com/european-parliament-rejects-cadmium-qds/

**Weather**
- Mehra et al., "Would SWIR modality help for detection and segmentation in harsh weather?", ICCV 2025 Workshops: https://openaccess.thecvf.com/content/ICCV2025W/MIRA/papers/Mehra_Would_SWIR_modality_help_for_detection_and_segmentation_in_harsh_ICCVW_2025_paper.pdf
- Duthon et al. 2019, Bertozzi et al. 2013 and Adomeit and Krieg 2015: see the main report, §C4c subsection 5 and §A7.5.
