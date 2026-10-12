r"""Re-baseline edits for the automotive perception report, written against the 12:04 snapshot
(report_peer_1204.md) with its equation numbers.  Each entry is one of
  ("L", line_prefix, new_line)            replace the unique line that starts with line_prefix
  ("X", exact_line, new_line)             replace the unique line equal to exact_line
  ("S", line_prefix, old_sub, new_sub)    replace old_sub (once) inside the unique line with that prefix
  ("B", start_prefix, end_prefix, text)   replace lines [start, end) with text (end line kept)
Equation references use the snapshot numbering; 9001 is the one new equation (in 10.3).
"""
from pathlib import Path

HERE = Path(__file__).parent
S103 = (HERE / "s103_new.md").read_text(encoding="utf-8").rstrip("\n") + "\n"

E = []

# =============================================================== executive summary
E.append(("L", "     - At 200 m and 10% reflectivity, the modelled electrical energy per point is ≈2.6 µJ",
r"""     - At 200 m and 10% reflectivity, the modelled electrical energy per point is ≈4.3 µJ for FMCW against ≈0.44 µJ for 940 nm SPAD ToF. That is ≈10×, since $4.25/0.436\approx9.8$ (≈5× in an optimistic 2032 case). Both receivers are held to one detection rule: 90% detection per point with at most $10^{-3}$ false points per point over the whole range searched (§C0 subsection 10.3). Each FMCW sample also covers only ≈2% of a 0.05° cell, because its beam footprint is much smaller than the angular cell it stands for."""))
E.append(("L", "     - There are three causes. The first is single-mode collection with speckle fading",
r"""     - There are three causes. The first is coherent collection with speckle fading. A coherent receiver accepts one spatial mode in one polarization, and the randomly bright or dark speckle it sees makes detection costly: even with four receivers per point (two polarizations × two spatial modes) and the echo's peak required in both chirp ramps, ≈88 photoelectrons are needed for 90% detection, against ≈18 counts for SPAD ToF in bright sun (the model uses 120 and 25). The second is the wall-plug efficiency (optical output per unit of electrical input) of the semiconductor optical amplifier (SOA), ≈20% at ≤50 °C. The third is dense digitization: ≈12,000 ADC (analogue-to-digital converter) samples per receiver per point, whatever the photon count. At 10 Mpts/s (million points per second) that means ≈100 channels with 400 receivers and ≈4.9 Tb/s of raw ADC data."""))
E.append(("S", "     - Series production in trucks or L3 by 2030 is plausible", "(≈5–10%)", "(≈3–7%)"))
E.append(("S", "     - **Better beam steering would not change this (§C7b).**",
          "each simultaneous coherent sample needs its own receiver chain and tens of mW of CW light",
          "each simultaneous coherent sample needs its own receiver chains (four in the §C7a design) and tens of mW of CW light"))
E.append(("S", "     - **Better beam steering would not change this (§C7b).**",
          "a ≥150-channel coherent receiver chip at ≤10–20 mW per channel",
          "a coherent receiver chip with ≥150 channels of four receivers each, at ≈2–3 mW per receiver"))

# =============================================================== §C0 subsections 2 and 7
E.append(("S", "| Shot-noise-limited SNR |",
          "A few photons suffice in principle; speckle fading raises the practical need to ≈45–130 (§C10.3a)",
          "A few photons suffice in principle; speckle fading, the search over thousands of bins and a peak needed in both chirp ramps raise the practical need to ≈90 (four looks) to ≈260 (one look) per point (subsection 10.3)"))
E.append(("L", "  - In a shot-noise-limited coherent receiver SNR ≈ detected photons, so this matches",
r"""  - In a shot-noise-limited coherent receiver SNR ≈ detected photons, so a single look needs ≈130 photoelectrons at $10^{-6}$ per bin. A full FMCW point needs more: under the per-point rule of subsection 10.3 ($10^{-3}$ false points over a 0–300 m search, with the echo's peak found in both chirp ramps), one look needs ≈259 and four summed looks ≈88. Polarization, wavelength or spatial diversity recovers much of the fading penalty. Subsection 10.3 plots these cases against photon counting (Figure C0.10b)."""))

# =============================================================== §C0 subsection 10.3 (whole part)
E.append(("B", "#### 10.3 How much light is needed: detection statistics (Figure C0.10b)",
          "#### 10.4 Where they meet: the detection level and the maximum range (Figure C0.10a)",
          S103 + "\n"))

# =============================================================== §C0 subsection 10.4
E.append(("S", "| FMCW | 1,550 nm | 30 | 0.25 |", "| FMCW | 1,550 nm | 30 | 0.25 |",
          "| FMCW, per look (four looks) | 1,550 nm | 30 of the 120 | 0.25 |"))
E.append(("X", "  - FMCW: the §C7a(a) efficiency.",
r"""  - FMCW: the §C7a(a) efficiency, and 30 photoelectrons per look. The four-look receiver needs 120 in total (10.3), and each look collects the link loss $\mathcal{L}_{\rm coh}$ of Eq. (33), so its detection level is that of one look with $n_{\rm req}=30$."""))
E.append(("S", "- **Worked (FMCW):** $30\\times1.28", "- **Worked (FMCW):**", "- **Worked (FMCW, per look):**"))
E.append(("L", "  - Requiring $P_D=0.9$ with four speckles ($n_{\\rm req}=45$, 10.3)",
r"""  - An extra 1.8 dB, for example 45 instead of 30 photoelectrons per look ($10\log_{10}(45/30)=1.8$ dB) or a receiver at two-thirds of the shot-noise limit, cuts the 25 mm range to **54 m**."""))

# =============================================================== §C0 subsection 10.5
E.append(("S", "Solve $\\mathcal{L}(R_{\\max})=\\mathcal{L}_{\\rm det}(E_{\\rm tx})$", "buys in range.",
          r"buys in range. For FMCW, $n_{\rm req}$ is the 30 photoelectrons of one look (10.4): each of the four looks collects $\mathcal{L}_{\rm coh}$ and needs a quarter of the 120, so the energies and ranges below hold for the whole receiver."))
E.append(("S", "- **Equal apertures, constant gap.**", "At $D=D_{\\rm opt}(R)$, the ratio",
          r"At $D=D_{\rm opt}(R)$, with each FMCW aperture as large as the ToF lens, the ratio"))
E.append(("S", "  - The subscripts c and d mark the coherent and direct-detection cases:",
          "$n_{\\rm c}$ and $n_{\\rm d}$ are their values of $n_{\\rm req}$",
          r"$n_{\rm c}=30$ (per look) and $n_{\rm d}=25$ are their values of $n_{\rm req}$"))

# =============================================================== §C3a, technology table
E.append(("S", "| **Mobileye / Intel** (ended Sep 2024) |",
          "(FMCW ≈2.6 µJ vs ToF ≈0.43 µJ per point at 200 m, §C7a)",
          "(FMCW ≈4.3 µJ vs ToF ≈0.44 µJ per point at 200 m, §C7a)"))
E.append(("S", "| **Coherent (FMCW) scanners** | Aurora's driverless trucks", "energy per point ≈6× that of SPAD ToF (§C7a)",
          "energy per point ≈10× that of SPAD ToF (§C7a)"))

# =============================================================== §C6(d)
E.append(("S", "  with $\\tau_d=6$ ns. For 905 nm, 20 nm:", "the 940 nm case gives $r\\tau_d=0.40$ and 29%.",
r"""the 940 nm case gives $r\tau_d=0.40$ and 29%.
- **In the ToF energy model.** The §C7a model and the detection statistics of §C0 subsection 10.3 apply Eqs. (76) and (77) at the model's PDE of 0.37, because the same SPADs count signal and background. The 940 nm, 10 nm case then gives $7.31\times10^{8}$ s⁻¹ and a 33% dead fraction for the fully sunlit $\rho_{\rm scene}=0.9$ scene ($r\tau_d=0.49$), and $3.66\times10^{8}$ s⁻¹ and 20% for the model's central case of half that background."""))

# =============================================================== §C7a
E.append(("L", "  - The model below gives about **6×** more electrical energy per point than 940 nm SPAD ToF",
r"""  - The model below gives about **10×** more electrical energy per point than 940 nm SPAD ToF in 2026 ($4.25/0.436\approx9.8$). This narrows to about **5×** in an optimistic 2032 projection ($1.48/0.286\approx5.2$; totals from the §3 table). Both receivers are held to the same detection rule (§C0 subsection 10.3)."""))
E.append(("S", "- *(a)* Modelled sensor electrical power (3 W overhead", "Bands span the low/high parameter sets.",
          "Bands span the low/high parameter sets, and the yellow band marks the 8–25 W typical of automotive lidars."))
E.append(("X", r"- *(c)* Parallel coherent channels needed ($\dot N\times T_{\rm dwell}$, point rate times dwell per point) and the raw ADC data they produce at 10 bits per sample.",
          r"- *(c)* Parallel coherent channels (transmit beams) needed ($\dot N\times T_{\rm dwell}$, point rate times dwell per point) and the raw ADC data they produce at 10 bits per sample, counting the four receivers of each channel."))
E.append(("S", "This subsection computes the energy one point costs, stage by stage, for both lidar types.",
          "FMCW pays more at every stage: single-mode collection and fading raise the optical energy, continuous-wave (CW) amplification limits wall-plug efficiency (electrical-to-optical conversion efficiency), and dense digitization dominates the receiver.",
          "FMCW pays more at every stage: single-mode collection and detection statistics (speckle fading, and a peak needed in both chirp ramps) raise the optical energy, continuous-wave (CW) amplification limits wall-plug efficiency (electrical-to-optical conversion efficiency), and dense digitization in four receivers per point dominates the receiver."))
E.append(("L", "- **FMCW receiver: one polarization and one spatial mode.**",
r"""- **FMCW receiver: four looks per point.** Each coherent receiver collects only the light that matches its LO in polarization and spatial mode. The central design gives every beam four such receivers, one per polarization on each of two spatial modes (for example two receive apertures side by side), so each point is seen in four independent speckles, four *looks*."""))
E.append(("L", "- **Rayleigh speckle.** Each single-mode FMCW measurement sees one speckle",
r"""- **Rayleigh speckle.** Each look sees one speckle, whose intensity is exponentially distributed (Rayleigh amplitude), so detection needs extra signal margin against fades; summing the four looks narrows the spread but does not remove it. The ToF pixel sums hundreds of speckles and does not fade.
- **One detection rule for both receivers:** 90% detection per point with at most $10^{-3}$ false points per point over the whole 0–300 m search (§C0 subsection 10.3)."""))
E.append(("L", "- **20 mm monostatic aperture** for FMCW,",
r"""- **20 mm apertures** for FMCW: each spatial mode is received through a 20 mm aperture in the mode of a Gaussian beam, one of them the monostatic aperture that also transmits; the ToF receiver uses one 25 mm aperture."""))
E.append(("L", "- **FMCW efficiency $\\eta=0.25$**, calibrated to Waymo's estimate",
r"""- **FMCW efficiency $\eta=0.25$**, checked against Waymo's estimate (details below) rather than built up from component data."""))
E.append(("S", "- **ToF:** $A_{\\rm eff}=A_{\\rm rx}$ is the whole 25 mm receive aperture (491 mm²)",
          "and ≈20–35 counts suffice (§C6(c)).",
          "and ≈20–35 counts suffice (§C6(c); an ideal counter needs 18.4 in the model's bright sun, §C0 subsection 10.3)."))
E.append(("B", "  - One polarization and one spatial mode: here $A_{\\rm eff}=A_{\\rm mode}$",
          "FMCW therefore needs ≈4× more optical energy per point than ToF (0.30 µJ against 73 nJ).",
r"""  - Each look collects one polarization in one spatial mode, so its effective area is $A_{\rm mode}$, the mode-equivalent collecting area. It is the area that, placed in the Lambertian fraction $\rho A_{\rm mode}/(\pi R^2)$, gives the power actually coupled into the polarization and spatial mode that the LO selects. It is the antenna-theorem quantity of Eq. (85) in §C7, for a mode set by a 20 mm aperture rather than by a 0.1° cell. $A_{\rm mode}\approx64$ mm² for a 20 mm monostatic Gaussian at 200 m (§C10.3b; derived in §C0 subsection 10.2), which already includes the polarization and mode-shape factors. Piggott et al. (Waymo) put one mode at **≈6 dB below ToF** (3 dB polarization, 3 dB aperture) [P]. The four looks together give $A_{\rm eff}=4A_{\rm mode}=255$ mm².
  - Single-mode returns fade, so detection needs more signal, and an FMCW point must show its peak in both the up- and the down-ramp of its chirp. Under the report's detection rule four looks need **≈88 photoelectrons** in total for 90% detection, and one look ≈259 (§C0 subsection 10.3). The model uses $n_{\rm req}=120$, 30 per look: the same ×1.36 implementation margin that takes ToF from 18.4 to 25 counts. Waymo's analysis uses **50 photoelectrons for 90% detection** with four averaged speckles at a $10^{-6}$ false-alarm probability, and finds that 10–30 photoelectrons give only ≈50% [P]; 50 is the one-ramp figure (47 by the same rule).
  - For FMCW, $\eta$ is the product of optical transmission, detector quantum efficiency and heterodyne mixing efficiency. It excludes the mode and polarization factor, which $A_{\rm mode}$ already contains.
  - Result: **≈0.30 µJ** (0.15–0.88) for 120 photoelectrons over four looks. With $A_{\rm eff}=4\times63.7=255$ mm², $E_{\rm ph}=1.28\times10^{-19}$ J at 1,550 nm and $\eta=0.25$, Eq. (88) gives $E_{\rm opt}=120\times1.28\times10^{-19}\times1.26\times10^{5}/(0.1\times2.55\times10^{-4}\times0.25)=1.93\times10^{-12}/(6.37\times10^{-6})\approx3.0\times10^{-7}$ J. The low case uses 96 photoelectrons and $\eta=0.40$ (0.15 µJ), the high case 168 and $\eta=0.12$ (0.88 µJ).
  - **Check against Waymo.** Waymo's "realistic" 10–20 W optical for their ADAS (advanced driver-assistance) case (12 Mpts/s, 250 m, 5%, 50 photoelectrons, 90% detection) is 10–20 W divided by $12\times10^{6}$ points/s, i.e. 0.83–1.67 µJ per point. Eq. (88) for one receiver with $A_{\rm mode}=74.5$ mm² (a 20 mm aperture at 250 m) and $\eta=0.25$ gives $50\times1.28\times10^{-19}\times\pi\times250^2/(0.05\times7.45\times10^{-5}\times0.25)=1.35$ µJ, inside that range.

"""))
E.append(("B", "FMCW therefore needs ≈4× more optical energy per point than ToF (0.30 µJ against 73 nJ).",
          "§C7b subsection 1 derives each factor.",
r"""FMCW therefore needs ≈4× more optical energy per point than ToF (0.30 µJ against 73 nJ). The ≈4× ratio splits into four factors:
- collection (1.9×), the ToF aperture area over the four looks' $A_{\rm eff}$ (491 mm² against 255 mm²);
- detection statistics (4.8×), 120 required photoelectrons against 25 counts: speckle fading, a peak needed in both chirp ramps, and one photoelectron of shot noise in every FFT bin searched (§C0 subsection 10.3);
- photon energy (0.61×), because a 1,550 nm photon carries less energy than a 940 nm one ($1.28/2.11$);
- efficiency (0.74×), ToF's 0.185 against FMCW's 0.25.

"""))
E.append(("B", "- The analog front end adds ≈10 mW per channel for the transimpedance amplifier (TIA)",
          "- Waymo's analysis reaches the same scale from the other direction:",
r"""- The analog front end adds ≈10 mW per receiver for the transimpedance amplifier (TIA), bias and drivers, drawn for the whole dwell. Each of the $N_L=4$ receivers of a point (one per look) digitizes and transforms its own beat, so the receiver electronics energy per point is

  $$E_{\rm rx}=N_L\left(N_{\rm samp}\,e_s+P_{\rm an}\,T_{\rm dwell}\right) \tag{91}$$

  where $E_{\rm rx}$ is the receiver electronics energy per point, $N_L$ the number of receivers (looks) per point, $P_{\rm an}$ the analog power per receiver and $T_{\rm dwell}=2T=10$ µs the dwell per point. This gives **≈2.2 µJ per point** (1.3–3.8): $E_{\rm rx}=4\times(12{,}300\times37.3\ {\rm pJ}+10\ {\rm mW}\times10\ \mu{\rm s})=4\times(0.46+0.10)=2.23$ µJ. The low and high cases are $4\times(12{,}300\times22\ {\rm pJ}+5\ {\rm mW}\times10\ \mu{\rm s})=1.3$ µJ and $4\times(12{,}300\times61\ {\rm pJ}+20\ {\rm mW}\times10\ \mu{\rm s})=3.8$ µJ.
"""))
E.append(("S", "- Waymo's analysis reaches the same scale from the other direction:",
          r"The model's own count is $12\times10^{6}\ {\rm s^{-1}}\times12{,}300\times70\approx1.0\times10^{13}$ operations/s.",
          r"The model's count for one receiver per point is the same, $12\times10^{6}\ {\rm s^{-1}}\times12{,}300\times70\approx1.0\times10^{13}$ operations/s; with four receivers per point it is $\approx4\times10^{13}$."))
E.append(("L", "- **ToF is event-driven.** A SPAD-SoC",
r"""- **ToF is event-driven.** A SPAD-SoC (a SPAD array stacked on its own processing chip) spends energy per avalanche and histogram increment (a few pJ each; ≈6,140 events per point in bright sun), plus fixed clocking and readout. Calibrated to Sony's 1.19 W development chip (§C5a), that is **≈70 nJ per point** (20–130). Its histogram also has ≈2,000 bins, but they are *counted* sparsely, not *sampled and transformed* densely. The event count is background count rate × listening time × live fraction + signal counts, $r_{\rm bg}\,t_{\rm listen}\,(1-f_{\rm dead})+n_{\rm req}$: $3.66\times10^{8}\ {\rm s^{-1}}\times20.8\ \mu{\rm s}\times(1-0.196)+25\approx6{,}140$. This takes a background count rate $r_{\rm bg}=3.66\times10^{8}$ s⁻¹ per macro-pixel, half the fully sunlit 940 nm case of §C6(d) (Eq. (76)) evaluated at the model's PDE of 0.37; a listening time $t_{\rm listen}=20.8$ µs per point (a model input, equal to one column period of a 520-line sensor at 25 Mpts/s); the dead fraction $f_{\rm dead}=19.6\%$ that Eq. (77) gives at this rate, the share of time the SPADs are recharging and blind; and $n_{\rm req}=25$ signal counts. §C0 subsection 10.3 derives the same background as 2.94 counts per 1 ns bin. At 5 pJ per event plus a fixed 40 nJ per point, $E=40\ {\rm nJ}+6{,}140\times5\ {\rm pJ}=71$ nJ. The fixed term follows the calibration: 1–2 W for an IMX479-class chip at 25 Mpts/s is 40–80 nJ per point including events (Sony's 1.19 W divided by $25\times10^{6}$ s⁻¹ is 48 nJ). The range runs from 20 nJ (night: 20 nJ fixed, 4 pJ per event) to $60\ {\rm nJ}+(7.31\times10^{8}\times20.8\ \mu{\rm s}\times(1-0.328)+35)\times7\ {\rm pJ}=132$ nJ (the fully sunlit scene, with a 32.8% dead fraction)."""))
E.append(("S", "- The 10 µs dwell is the 5 µs up-chirp plus the 5 µs down-chirp of (c).",
          "10 Mpts/s needs **100**, and 25 Mpts/s needs 250.",
          "10 Mpts/s needs **100**, and 25 Mpts/s needs 250. With four receivers per channel these are 80, 400 and 1,000 receivers."))
E.append(("S", "- Raw ADC output at 10 bits per sample is **0.25, 1.2 and 3.1 Tb/s** respectively",
          r"**0.25, 1.2 and 3.1 Tb/s** respectively: $N_{\rm ch}\times f_s\times10$ bits, e.g. $100\times1.23\times10^{9}\ {\rm s^{-1}}\times10=1.2\times10^{12}$ b/s at 10 Mpts/s.",
          r"**0.98, 4.9 and 12 Tb/s** respectively: $N_LN_{\rm ch}\times f_s\times10$ bits with $N_L=4$ receivers per channel, e.g. $4\times100\times1.23\times10^{9}\ {\rm s^{-1}}\times10=4.9\times10^{12}$ b/s at 10 Mpts/s."))
E.append(("S", "- Today's merchant FMCW SoC, indie's **iND83301 \"Surya\"**",
          r"A 10 Mpts/s sensor would need roughly **30 such devices** [E]. The aggregate sample rate is $\dot N N_{\rm samp}=10^{7}\ {\rm s^{-1}}\times12{,}300\approx1.2\times10^{11}$ samples/s, against $4\times1$ GS/s per device, so $123/4\approx31$ devices. Counting one ADC per channel gives $100/4=25$, but each 1 GS/s converter is then below the 1.23 GS/s a channel needs, and the 8 × 500 MS/s mode (12–13 devices) is far too slow per channel.",
          r"A 10 Mpts/s sensor would need roughly **120 such devices** [E]. The aggregate sample rate is $\dot N N_LN_{\rm samp}=10^{7}\ {\rm s^{-1}}\times4\times12{,}300\approx4.9\times10^{11}$ samples/s, against $4\times1$ GS/s per device, so $490/4\approx123$ devices. Counting one ADC per receiver gives $400/4=100$, but each 1 GS/s converter is then below the 1.23 GS/s a receiver needs, and the 8 × 500 MS/s mode (50 devices) is far too slow per receiver."))
E.append(("L", "- **FMCW:** every *simultaneous* line needs an LO tap",
r"""- **FMCW:** every *simultaneous* line needs four receivers (one per look), each with an LO tap, a 90° hybrid (an optical mixer that yields in-phase and quadrature beats) or balanced Ge photodiode pair, a TIA, a GS/s ADC and an FFT pipe, plus **≈50–100 mW of dedicated optical power**. The central model gives $E_{\rm opt}/T_{\rm dwell}=0.30\ \mu{\rm J}/10\ \mu{\rm s}=30$ mW per channel at 200 m; 50–100 mW corresponds to its high-energy case (0.88 µJ, 88 mW) or to 250–300 m, since the energy scales as $R^2$ ($30\times(250/200)^2=47$ mW and $30\times(300/200)^2=68$ mW). Lines beyond the channel count come from stepping the beam, which costs dwell."""))
E.append(("L", "- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m",
r"""- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m (12.5 Mpts/s) implies ≈125 channels (500 receivers) at 10 µs, ≈3.8 W optical, ≈21 W of laser heat and ≈28 W of receiver electronics under the central 2026 assumptions. That is about **56 W** in total, against ≈8–9 W for a 520-line ToF unit in the same model, and each FMCW sample still covers only ≈2% of its cell (§C10.3a). The arithmetic: $\dot N=520\times2{,}400\times10\ {\rm Hz}=1.25\times10^{7}$ pts/s; $N_{\rm ch}=1.25\times10^{7}\times10\ \mu{\rm s}=125$; optical power $1.25\times10^{7}\times0.30\ \mu{\rm J}=3.8$ W; laser heat, the laser's electrical energy per point minus the light it emits, $1.25\times10^{7}\times(2.02-0.30)\ \mu{\rm J}=21$ W; receivers $1.25\times10^{7}\times2.23\ \mu{\rm J}=27.9$ W. With the 3 W overhead, the total is $3\ {\rm W}+1.25\times10^{7}\times4.25\ \mu{\rm J}\approx56$ W. The ToF unit is $3\ {\rm W}+1.25\times10^{7}\times0.436\ \mu{\rm J}\approx8.5$ W."""))
E.append(("S", "- **What is missing** is not a part that does this on a bench",
          "the light alone is ≈30 of ≈46 W of sensor power", "the light alone is ≈30 of ≈68 W of sensor power"))
E.append(("S", "This table collects the budget of §2 for a 200 m, 10%-reflectance target.",
          "FMCW needs about 6× ToF's electrical energy per point in 2026 and about 3× in the optimistic 2032 case",
          "FMCW needs about 10× ToF's electrical energy per point in 2026 and about 5× in the optimistic 2032 case"))
E.append(("X", "| Optical energy per point | 73 nJ | 0.30 µJ | 60 nJ | 0.16 µJ |",
          "| Counts or photoelectrons needed per point (ideal; model) | 18.4; 25 | 88.5; 120 (four looks) | 18.4; 25 | 88.5; 120 |\n"
          "| Optical energy per point | 73 nJ | 0.30 µJ | 60 nJ | 0.19 µJ |"))
E.append(("X", "| Laser/SOA electrical energy | 0.37 µJ | 2.0 µJ | 0.24 µJ | 0.72 µJ |",
          "| Laser/SOA electrical energy | 0.37 µJ | 2.0 µJ | 0.24 µJ | 0.86 µJ |"))
E.append(("X", "| Receiver electronics | 0.06 µJ | 0.56 µJ | 0.04 µJ | 0.15 µJ |",
          "| Receiver electronics | 0.07 µJ | 2.2 µJ (four receivers) | 0.045 µJ | 0.61 µJ |"))
E.append(("X", "| **Total per point** | **0.43 µJ** | **2.6 µJ** | **0.28 µJ** | **0.87 µJ** |",
          "| **Total per point** | **0.44 µJ** | **4.25 µJ** | **0.29 µJ** | **1.48 µJ** |"))
E.append(("X", "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 7.3 W | 29 W | 5.8 W | 12 W |",
          "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 7.4 W | 46 W | 5.9 W | 18 W |"))
E.append(("X", "| Sensor power at 25 Mpts/s | 14 W | 68 W | 10 W | 25 W |",
          "| Sensor power at 25 Mpts/s | 14 W | 109 W | 10 W | 40 W |"))
E.append(("S", "- All entries are the central cases of the companion script. **Optical energy** uses",
          r"FMCW 2032 uses 25 photoelectrons and $\eta=0.40$, giving $0.30\times(25/30)\times(0.25/0.40)=0.16$ µJ.",
          r"FMCW 2032 keeps the four looks and the 120 photoelectrons, since detection statistics do not improve with technology, and raises $\eta$ to 0.40, giving $0.30\times0.25/0.40=0.19$ µJ. The counts row gives the ideal requirement of §C0 subsection 10.3 and the model's value, 1.36× higher for both receivers."))
E.append(("S", "- **Laser/SOA electrical energy** is $E_{\\rm opt}/\\eta_{\\rm wp}$",
          r"$0.16\ \mu{\rm J}/0.22=0.72$ µJ.", r"$0.19\ \mu{\rm J}/0.22=0.86$ µJ."))
E.append(("L", "- **Receiver electronics:** ToF is a fixed 40 nJ (2026) or 20 nJ (2032) plus",
r"""- **Receiver electronics:** ToF is a fixed 40 nJ (2026) or 20 nJ (2032) plus ≈6,140 or ≈7,160 events at 5 or 3.5 pJ, giving 71 and 45 nJ (§2(c)); the 2032 sensor counts more events because its higher PDE also detects more sunlight (Eq. (76)). FMCW is $N_L(N_{\rm samp}e_s+P_{\rm an}T_{\rm dwell})$ (Eq. (91)): $N_L=4$ receivers, each with $N_{\rm samp}$ samples per point times energy per sample $e_s$, plus analog power per receiver $P_{\rm an}$ times the dwell $T_{\rm dwell}$. That is 2.23 µJ in 2026 (§2(c)). In 2032 the model keeps 8 effective bits (ENOB = 8) at a FOM of 12 fJ/step and 70 DSP operations at 0.1 pJ each, so Eq. (90) gives $e_s=12\ {\rm fJ}\times2^{8}+70\times0.1\ {\rm pJ}=3.1+7=10.1$ pJ, and $4\times(12{,}300\times10.1\ {\rm pJ}+3\ {\rm mW}\times10\ \mu{\rm s})=4\times(0.12+0.03)=0.61$ µJ."""))
E.append(("S", "- **Total per point** is the laser row plus the receiver row", "e.g. FMCW 2026: $2.02+0.56=2.6$ µJ.",
          "e.g. FMCW 2026: $2.02+2.23=4.25$ µJ."))
E.append(("S", "- **Sensor power** is $3\\ {\\rm W}+\\dot N E_{\\rm total}$",
          r"e.g. FMCW 2026 at 10 Mpts/s: $3+10^{7}\times2.58\times10^{-6}=28.8\approx29$ W, and at 25 Mpts/s $3+2.5\times10^{7}\times2.58\times10^{-6}=67.5\approx68$ W; ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.428\times10^{-6}=7.3$ W.",
          r"e.g. FMCW 2026 at 10 Mpts/s: $3+10^{7}\times4.25\times10^{-6}=45.5\approx46$ W, and at 25 Mpts/s $3+2.5\times10^{7}\times4.25\times10^{-6}=109$ W; ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.436\times10^{-6}=7.4$ W."))
E.append(("L", "The 2032 FMCW column assumes efficiency $\\eta=0.4$ and 22% wall-plug;",
r"""The 2032 FMCW column assumes efficiency $\eta=0.4$ and 22% wall-plug; ADCs at 12 fJ/step (still at 8 ENOB), FFTs at 0.1 pJ/op and 3 mW of analog per receiver; and the same four looks and 120 photoelectrons as in 2026. These are optimistic but not exotic. The residual ≈5× gap comes from detection statistics and single-mode collection, SOA wall-plug efficiency, and dense digitization in four receivers per point."""))
E.append(("L", "2. A stacked or monolithic electronic-photonic receiver at **≤10–20 mW per channel**",
          "2. A stacked or monolithic electronic-photonic receiver at **≈8–13 mW per channel**, i.e. ≈2–3 mW for each of its four receivers, including 1 GS/s ADCs and FFT (§C7b subsection 5)."))
E.append(("S", "| FMCW matching 2026 SPAD ToF on point rate per watt", "| 2032 | ≈5–10% |", "| 2032 | ≈3–7% |"))

# =============================================================== §C7b short answer
E.append(("L", "  - A coherent receiver, by contrast, uses only one spatial mode and one polarization of the echo.",
r"""  - A coherent receiver, by contrast, uses only one spatial mode and one polarization of the echo. For any collimated beam, that gives an effective collecting area of ≤65 mm² at 200 m, and a single speckle whose brightness fades at random. The §C7a design therefore gives each beam four receivers (two polarizations on each of two spatial modes), 255 mm² in all, and still needs 120 photoelectrons per point against 25 counts for ToF (§C0 subsection 10.3)."""))
E.append(("L", "  - Each channel is a complete coherent receiver matched to the LO.",
r"""  - Each channel is a transmit beam with four complete coherent receivers matched to the LO. Each receiver has balanced photodiodes, a transimpedance amplifier (TIA), a GS/s analogue-to-digital converter (ADC) and a fast-Fourier-transform (FFT) processor, and the channel is fed by its own CW light. It measures only ≈0.05–0.25 Mpts/s at 200 m."""))
E.append(("S", "  - A SPAD-SoC (a SPAD array stacked on its own processing chip, a system-on-chip) also runs hundreds of pixels",
          "A coherent channel costs ≈44 mW of receive power plus ≈200 mW of electrical power for its light (2026 central).",
          "A coherent channel costs ≈176 mW of receive power (four receivers of ≈44 mW) plus ≈200 mW of electrical power for its light (2026 central)."))
E.append(("L", "- **At the sensor level, most of the power is the light itself** (subsection 2(h)).",
r"""- **At the sensor level, most of the power is light** (subsection 2(h)). For 10 Mpts/s at 300 m, ≈30 of ≈68 W is the useful optical energy per point divided by the CW laser's wall-plug efficiency, $\dot NE_{\rm opt}/(\eta_{\rm coh}\eta_{\rm WPE})$, and ≈9 W more is light emitted during the round-trip dead time; the four receivers per beam take most of the rest (≈26 W)."""))
E.append(("S", "  - Laser linewidth enters through $\\eta_{\\rm coh}=e^{-2\\pi\\Delta\\nu\\cdot2R/c}$:",
          "with a 100 kHz laser the same sensor needs ≈130 W.", "with a 100 kHz laser the same sensor needs ≈160 W."))
E.append(("L", "  - a coherent receiver chip with ≥150 channels at ≤10–20 mW each, ADC and FFT included",
          "  - a coherent receiver chip with ≥150 channels of four receivers each, at ≈8–13 mW per channel (≈2–3 mW per receiver), ADC and FFT included (a coherent counterpart of the SPAD-SoC);"))
E.append(("L", "  - an optical energy per point near 0.15 µJ at 200 m on a 10% target, which needs multimode or diversity reception.",
          "  - an optical energy per point near 0.15 µJ at 200 m on a 10% target, which needs a receive efficiency near 0.5, or more looks per point, each with its own receiver."))
E.append(("S", "  - If any one of them is missing, a 15 Mpts/s sensor stays at ≈15–20 W against a 15 W target.",
          "Today's central case is ≈41 W.", "Today's central case is ≈67 W."))

E.append(("S", "  - ToF must pulse so that sunlight competes with the signal only inside a 1 ns timing bin.",
          "it would need ≈13× more energy to stand out.", "it would need ≈16× more energy to stand out."))

# =============================================================== §C7b subsection 1
E.append(("L", "  - **In the §C7a model:** a macro-pixel (a group of SPADs read out as one pixel) in bright sun counts",
r"""  - **In the §C7a model:** a macro-pixel (a group of SPADs read out as one pixel) in bright sun counts $r_{\rm bg}=3.66\times10^{8}$ s⁻¹, half the fully sunlit case of §C6(d) at the model's PDE of 0.37. It listens for the 20.8 µs column time per point (≈10 shots of ≈2 µs, §C6). It is dead (unable to count) for 19.6% of that time (Eq. (77)), so it is live for a fraction 0.804 of it. That gives $3.66\times10^{8}\times20.8\times10^{-6}\times0.804\approx6{,}120$ background events per point."""))
E.append(("L", "  - **Per bin:** these events are spread over the ≈2,000 histogram bins of 1 ns",
r"""  - **Per bin:** these events are spread over the ≈2,080 histogram bins of 1 ns in each shot's 2.08 µs listening window (≈300 m of range), so there are $6{,}120/2{,}080\approx2.94$ counts per bin. Eq. (93), with the 0.804 live fraction, gives the same: $3.66\times10^{8}\times10^{-9}\times10\times0.804=2.94$. So ≈25 signal counts in one bin stand out clearly: the detection threshold is 16 counts (§C0 subsection 10.3)."""))
E.append(("L", "  - **The same energy spread evenly in time,** as with CW light, would have to stand out against all 4,430 events.",
r"""  - **The same energy spread evenly in time,** as with CW light, would have to stand out against all 6,120 events. The random (Poisson) fluctuation of 6,120 counts is $\sqrt{6{,}120}\approx78$. At 5 standard deviations that takes $5\sqrt{6{,}120}\approx390$ counts: ≈16× more energy per point, before any requirement on ranging precision."""))
E.append(("L", "- **Counts needed.** One mode means one speckle.",
r"""- **Counts needed.** One mode means one speckle. A single speckle's intensity is exponentially distributed (its field amplitude follows Rayleigh statistics), so many looks are much dimmer than the mean. Averaging $N_{\rm sp}$ independent speckles narrows this spread; a direct-detection pixel averages hundreds, while each coherent receiver sees one. The §C7a design therefore gives each beam four receivers, one per polarization on each of two spatial modes, and sums their powers: four looks. Under the report's detection rule (90% per point, at most $10^{-3}$ false points per point over the full search) and with the peak required in both the up- and the down-ramp, four looks need ≈88 photoelectrons in total and one look ≈259 (§C0 subsection 10.3). The model uses 120, the same ×1.36 margin that takes ToF from 18.4 to 25 counts. Waymo's 50 photoelectrons with four averaged speckles [P] is the corresponding one-ramp figure (≈47 by the same rule). These counts assume a receiver at the LO shot-noise limit, i.e. thermal and dark-current noise neglected. At 105–125 °C this holds only approximately: §C4c gives 82–94% of the shot-noise limit for Ge at 125 °C."""))
E.append(("X", r"- for the coherent rows, one polarization and one spatial mode, both already inside $A_{\rm mode}$ (Eq. (96)), and a depolarizing target;",
          r"- for the coherent rows, four looks per sample (two polarizations × two spatial modes), each with its own $A_{\rm mode}$ (Eq. (96)), and a depolarizing target;"))
E.append(("X", "- speckle: direct-detection pixels average hundreds of speckles, while a coherent sample sees one exponentially fading speckle, which is why it needs 30 rather than 25 photoelectrons;",
          "- speckle and search: direct-detection pixels average hundreds of speckles, while each coherent look sees one exponentially fading speckle; with four looks, and the peak required in both ramps, a coherent sample needs 120 photoelectrons against 25 counts (§C0 subsection 10.3);"))
E.append(("X", r"| 1,550 nm FMCW, collimated 20 mm monostatic beam, per sample | 64 mm² (one mode) | 30 | 0.25 | 0.30 µJ | $3.3\times10^{6}$ |",
          r"| 1,550 nm FMCW, collimated 20 mm monostatic beam, four looks, per sample | 255 mm² (4 × 64 mm²) | 120 | 0.25 | 0.30 µJ | $3.3\times10^{6}$ |"))
E.append(("X", r"| FMCW with the beam widened, or 48 samples tiled, to cover a whole 0.05° cell | 1.3 mm² | 30 | 0.25 | ≈15 µJ | $6.8\times10^{4}$ |",
          r"| FMCW with the beam widened, or 48 samples tiled, to cover a whole 0.05° cell | 5.3 mm² (4 × 1.3 mm²) | 120 | 0.25 | ≈15 µJ | $6.8\times10^{4}$ |"))
E.append(("B", "**(d) Why FMCW buys ≈4× fewer sampled points per joule than SPAD ToF.**",
          "- **1,550 nm helps (0.61×):**",
r"""**(d) Why FMCW buys ≈4× fewer sampled points per joule than SPAD ToF.** Let $E_{\rm FMCW}$ be the optical energy per FMCW sample (0.30 µJ) and $E_{\rm ToF}$ the optical energy per SPAD ToF point (73 nJ), both from Eq. (92). Their ratio splits term by term; each factor is the ratio of one term of that equation, FMCW over ToF, or its inverse:
$$\frac{E_{\rm FMCW}}{E_{\rm ToF}}=\underbrace{\frac{491}{255}}_{\rm collection}\times\underbrace{\frac{120}{25}}_{\rm detection}\times\underbrace{\frac{940}{1{,}550}}_{\rm photon\ energy}\times\underbrace{\frac{0.185}{0.25}}_{\rm efficiency}=1.93\times4.8\times0.61\times0.74=4.15. \tag{99}$$
The collection factor is the ratio of effective areas in mm², the detection factor the ratio of required photoelectrons, the photon-energy factor the wavelength ratio (since $E_{\rm ph}=hc/\lambda$), and the efficiency factor the ratio of the two $\eta$ values.
- **Collection (1.9×):**
  - 1.56× of this comes from the model's larger ToF lens ($(25/20)^2$).
  - 1.23× compares the four looks' 255 mm² with the full area of one 20 mm aperture, $\pi(10\ {\rm mm})^2=314$ mm². Each look alone collects only $A_{\rm mode}=64$ mm², 4.9× less than that area ($314/64$), because it takes one polarization, in the Gaussian mode shape, of a 20 mm beam that has spread at 200 m; Waymo puts this single-mode penalty at ≈6 dB [P]. Two polarizations on each of two spatial modes recover a factor of four.
- **Detection statistics (4.8×):** the four looks need 120 photoelectrons and ToF 25 counts; the ideal requirements have the same ratio ($88.5/18.4=4.8$, §C0 subsection 10.3). Of this, ×2.3 is speckle fading with four looks, ×1.8 is finding the peak in both ramps, and ×1.2 is the coherent receiver's one photoelectron of shot noise in each of the ≈2,450 FFT bins it searches.
"""))

# =============================================================== §C7b subsection 2
E.append(("S", "  - A faster ADC simply runs for a shorter time.",
          r"At that energy the receiver spends $8{,}900\times37\ {\rm pJ}\approx0.33$ µJ per point at 200 m, and $12{,}300\times37\ {\rm pJ}\approx0.45$ µJ at 300 m, before TIA and bias power.",
          r"At that energy each receiver spends $8{,}900\times37\ {\rm pJ}\approx0.33$ µJ per point at 200 m, and $12{,}300\times37\ {\rm pJ}\approx0.45$ µJ at 300 m, before TIA and bias power; the four receivers of the §C7a design spend four times as much, 1.3 and 1.8 µJ."))
E.append(("S", "**(h) What limits a 10 Mpts/s sensor at 300 m: the light itself.**",
          "(laser wall-plug efficiency, per-channel analog power, per-sample ADC and FFT energy)",
          "(laser wall-plug efficiency, per-receiver analog power, per-sample ADC and FFT energy, four receivers per channel)"))
E.append(("S", "$$P_{\\rm elec}=\\underbrace{\\frac{\\dot N E'}{\\eta_{\\rm WPE}}}_{\\rm useful\\ light}",
          r"\underbrace{N_{\rm ch}P_{\rm an}}_{\rm analog}+\underbrace{\dot N N_{\rm samp}e_s}_{\rm ADC\ and\ FFT}",
          r"\underbrace{N_{\rm ch}N_LP_{\rm an}}_{\rm analog}+\underbrace{\dot N N_LN_{\rm samp}e_s}_{\rm ADC\ and\ FFT}"))
E.append(("S", "Here $\\dot N$ is the point rate; $\\eta_{\\rm WPE}$ the wall-plug efficiency of the CW laser",
          r"$P_{\rm an}$ the analog power per channel (TIA, bias and drivers, ≈10 mW);",
          r"$P_{\rm an}$ the analog power per receiver (TIA, bias and drivers, ≈10 mW); $N_L=4$ the receivers (looks) per channel;"))
E.append(("S", "- **Only the channel terms depend on $P_{\\rm ch}$.**",
          r"$P_{\rm elec}=\dot N[E'/\eta_{\rm WPE}+5(R/\Delta R)e_s+2\tau P_{\rm an}]+2\tau\dot NP_{\rm ch}/\eta_{\rm WPE}+\dot NE'(P_{\rm an}+2.5f_De_s)/P_{\rm ch}+P_0$",
          r"$P_{\rm elec}=\dot N[E'/\eta_{\rm WPE}+5N_L(R/\Delta R)e_s+2\tau N_LP_{\rm an}]+2\tau\dot NP_{\rm ch}/\eta_{\rm WPE}+\dot NE'N_L(P_{\rm an}+2.5f_De_s)/P_{\rm ch}+P_0$"))
E.append(("X", r"$$P_{\rm ch}^{*}=\sqrt{\frac{\eta_{\rm WPE}\,E'\,(P_{\rm an}+2.5f_De_s)}{2\tau}}, \tag{114}$$",
          r"$$P_{\rm ch}^{*}=\sqrt{\frac{\eta_{\rm WPE}\,E'\,N_L\,(P_{\rm an}+2.5f_De_s)}{2\tau}}, \tag{114}$$"))
E.append(("X", r"$$P_{\rm elec,min}=\dot N\left[\frac{E'}{\eta_{\rm WPE}}+5\,\frac{R}{\Delta R}\,e_s+2\tau P_{\rm an}+2\sqrt{\frac{2\tau\,E'\,(P_{\rm an}+2.5f_De_s)}{\eta_{\rm WPE}}}\,\right]+P_0 . \tag{115}$$",
          r"$$P_{\rm elec,min}=\dot N\left[\frac{E'}{\eta_{\rm WPE}}+5N_L\,\frac{R}{\Delta R}\,e_s+2\tau N_LP_{\rm an}+2\sqrt{\frac{2\tau\,E'\,N_L\,(P_{\rm an}+2.5f_De_s)}{\eta_{\rm WPE}}}\,\right]+P_0 . \tag{115}$$"))
E.append(("S", "  - $P_{\\rm an}+2.5f_De_s=10\\ {\\rm mW}+", "=10+8.3=18.3$ mW.", "=10+8.3=18.3$ mW per receiver."))
E.append(("L", "  - Eq. (114): $P_{\\rm ch}^{*}=\\sqrt{0.15",
r"""  - Eq. (114): $P_{\rm ch}^{*}=\sqrt{0.15\times0.45\times10^{-6}\times4\times0.0183/(4\times10^{-6})}=35.2$ mW, at the ≈35 mW where 1 GS/s converters start to bind (item (g)). Then $T_u=0.45\ \mu{\rm J}/(2\times35.2\ {\rm mW})=6.4$ µs, $T_c=8.4$ µs, $B_{\rm tot}=1.31$ GHz, $\kappa=1.6\times10^{14}$ Hz/s, $f_s=2.5\times(313+90)\ {\rm MHz}=1.01$ GS/s and $N_{\rm ch}=10^{7}\times(12.8+4.0)\ \mu{\rm s}=168$ channels, i.e. 672 receivers."""))
E.append(("L", "  - Eq. (115): useful light $10^{7}\\times0.45",
r"""  - Eq. (115): useful light $10^{7}\times0.45\ \mu{\rm J}/0.15=30$ W; range samples $10^{7}\times5\times2{,}000\times4\times37\ {\rm pJ}=14.8$ W; fixed analog share $10^{7}\times4\ \mu{\rm s}\times4\times10\ {\rm mW}=1.6$ W; the two channel terms $2\times9.4=18.8$ W, where $2\tau\dot NP_{\rm ch}^{*}/\eta_{\rm WPE}=4\times10^{-6}\times10^{7}\times0.0352/0.15=9.4$ W; overhead 3 W. **Total ≈68 W, of which ≈44% is the useful light and ≈38% the receivers.**"""))
E.append(("X", "| $P_{\\rm ch}$ | Channels | $T_u$ | $B_{\\rm tot}$ | $f_s$ | Useful light | Dead-time light | Analog | ADC and FFT | Total |",
          "| $P_{\\rm ch}$ | Channels (receivers) | $T_u$ | $B_{\\rm tot}$ | $f_s$ | Useful light | Dead-time light | Analog | ADC and FFT | Total |"))
E.append(("X", "| 16 mW | 321 | 14.1 µs | 1.14 GHz | 0.58 GS/s | 30.0 W | 4.3 W | 3.2 W | 6.0 W | 46.5 W |",
          "| 16 mW | 321 (1,285) | 14.1 µs | 1.14 GHz | 0.58 GS/s | 30.0 W | 4.3 W | 12.8 W | 24.2 W | 74.3 W |"))
E.append(("X", "| 17.6 mW (optimum) | 296 | 12.8 µs | 1.16 GHz | 0.62 GS/s | 30.0 W | 4.7 W | 3.0 W | 5.8 W | 46.5 W |",
          "| 30 mW | 190 (760) | 7.5 µs | 1.27 GHz | 0.89 GS/s | 30.0 W | 8.0 W | 7.6 W | 19.8 W | 68.4 W |"))
E.append(("X", "| 30 mW | 190 | 7.5 µs | 1.27 GHz | 0.89 GS/s | 30.0 W | 8.0 W | 1.9 W | 5.0 W | 47.9 W |",
          "| 35.2 mW (optimum) | 168 (672) | 6.4 µs | 1.31 GHz | 1.01 GS/s | 30.0 W | 9.4 W | 6.7 W | 19.1 W | 68.2 W |"))
E.append(("X", "| 100 mW (needs ≥2.5 GS/s ADCs) | 85 | 2.25 µs | 1.89 GHz | 2.45 GS/s | 30.0 W | 26.7 W | 0.9 W | 4.1 W | 64.6 W |",
          "| 100 mW (needs ≥2.5 GS/s ADCs) | 85 (340) | 2.25 µs | 1.89 GHz | 2.45 GS/s | 30.0 W | 26.7 W | 3.4 W | 16.3 W | 79.4 W |"))
E.append(("L", "- Analog $N_{\\rm ch}\\times10$ mW; ADC and FFT",
          r"- Analog $N_{\rm ch}\times4\times10$ mW; ADC and FFT $\dot N\times4\times(10{,}000+5f_DT_u)\times37$ pJ: at 30 mW, $10^{7}\times4\times(10{,}000+3{,}375)\times37\ {\rm pJ}=19.8$ W."))
E.append(("S", "- **Photons per point, $E'$:**", r"saves $15+9.4\times(1-1/\sqrt2)=17.7$ W.",
          r"saves $15+18.8\times(1-1/\sqrt2)=20.5$ W."))
E.append(("L", "- **Laser linewidth, through $\\eta_{\\rm coh}$:** at 300 m a 10 kHz laser",
r"""- **Laser linewidth, through $\eta_{\rm coh}$:** at 300 m a 10 kHz laser ($E'=0.51$ µJ) gives ≈73 W, a 42 kHz laser ($E'=0.76$ µJ) ≈95 W and a 100 kHz laser ($E'=1.58$ µJ) ≈160 W, against ≈68 W with no coherent loss. Worked (100 kHz): useful light $10^{7}\times1.58\ \mu{\rm J}/0.15=105$ W, channel terms $2\times10^{7}\times\sqrt{4\times10^{-6}\times1.58\times10^{-6}\times4\times0.0183/0.15}=35.2$ W, plus $14.8+1.6+3$ W."""))
E.append(("S", "- **Wall-plug efficiency:** doubling $\\eta_{\\rm WPE}$ to 0.30", "saves the same ≈18 W as halving",
          "saves the same ≈20 W as halving"))
E.append(("L", "- **Channel electronics:** halving $P_{\\rm an}$ and $e_s$ together saves",
          r"- **Channel electronics:** halving $P_{\rm an}$ and $e_s$ together saves ≈13.7 W: 7.4 W of range samples, 0.8 W of fixed analog power, and $18.8\times(1-1/\sqrt2)=5.5$ W of channel terms."))
E.append(("L", "- **More power per channel:** nothing, or worse.",
          "- **More power per channel:** nothing, or worse. The optimum is ≈30–40 mW; 100 mW per channel costs ≈11 W more, because 17 W more dead-time light outweighs the saving in receivers."))
E.append(("S", "- **The useful light itself is large and expensive.**",
          "≈5.2 W as emitted at the optimum, and each watt costs ≈7 W of electrical power at 15% wall-plug efficiency. That light and its heat are the binding problem.",
          "≈5.9 W as emitted at the optimum, and each watt costs ≈7 W of electrical power at 15% wall-plug efficiency. That light and its heat are the largest problem; the four receivers per beam are the second (≈26 W)."))
E.append(("L", "- **The levers are fewer photons per point and cheaper photons:**",
          r"- **The levers are fewer photons per point, cheaper photons and cheaper receivers:** a smaller $E'$ (collection per look, coherence), a higher $\eta_{\rm WPE}$ and less power per receiver. Chirp speed, tuning range and beam steering are not the limits at these channel powers."))

# =============================================================== §C7b subsection 3
E.append(("S", "This subsection turns the dwell of subsection 2 into the number of parallel coherent channels",
          "At 15 Mpts/s the answer is ≈190 channels, each drawing ≈245 mW of electrical power (receiver plus its share of the laser), against ≈21 mW per ToF channel. This matters because each coherent channel is a complete receiver fed by its own light,",
          "At 15 Mpts/s the answer is ≈190 channels, each with four receivers and drawing ≈376 mW of electrical power (receivers plus its share of the laser), against ≈21 mW per ToF channel. This matters because each coherent channel is four complete receivers fed by its own light,"))
E.append(("S", "- \"Aeries-class\" refers to Aeva's Aeries FMCW sensors;",
          "the 41 Mpts/s row is a ToF sensor, shown for scale.",
          "the 41 Mpts/s row is a ToF sensor, shown for scale.\n- In the §C7a design each channel carries four receivers, so the receiver count is four times these figures."))
E.append(("S", "- **Power per ToF channel.** At the §C7a central values", "(≈60 nJ of receive electronics",
          "(≈70 nJ of receive electronics"))
E.append(("L", "  - receive: $15\\times10^{6}\\times60\\ {\\rm nJ}=0.9$ W",
          r"  - receive: $15\times10^{6}\times71\ {\rm nJ}=1.07$ W, i.e. $1.07\ {\rm W}/312=3.4$ mW per macro-pixel;"))
E.append(("L", "  - receive: $15\\times10^{6}\\times0.56\\ \\mu{\\rm J}=8.4$ W",
          r"  - receive: $15\times10^{6}\times2.23\ \mu{\rm J}=33.4$ W, i.e. ≈176 mW per channel, ≈44 mW for each of its four receivers (2.23 µJ is the §C7a receiver energy per point, $E_{\rm rx}$ below);"))
E.append(("X", "  - Each channel is an LO tap, a balanced photodiode pair, a TIA, a GS/s ADC and an FFT pipe.",
          "  - Each channel is four receivers, each an LO tap, a balanced photodiode pair, a TIA, a GS/s ADC and an FFT pipe."))
E.append(("L", "- **So the per-channel electrical power is ≈245 mW for FMCW against ≈21 mW for ToF, ≈12× more.**",
          "- **So the per-channel electrical power is ≈376 mW for FMCW against ≈21 mW for ToF, ≈18× more.** The FMCW channel is also far larger and costlier."))
E.append(("L", "  - The §C7a 2026 central value, at 300 m with the model's 10 µs dwell, is $E_{\\rm rx}=12{,}300",
r"""  - The §C7a 2026 central value, at 300 m with the model's 10 µs dwell, is $E_{\rm rx}=4\times(12{,}300\times37\ {\rm pJ}+10\ {\rm mW}\times10\ \mu{\rm s})=4\times(0.46+0.10)\approx2.23$ µJ per point, for four receivers. In each, the first term is the samples: 12,300 per point at 300 m (Eq. (104)) times ≈37 pJ each, the §C7a figure for an 8-ENOB ADC at 50 fJ per conversion step plus the FFT. The second term is the ≈10 mW per receiver that §C7a assumes for the TIA, bias and drivers, running for the 10 µs dwell."""))
E.append(("L", "  - At 15 Mpts/s that is $15\\times10^{6}\\times0.56\\times10^{-6}=8.4$ W of receiver electronics",
          r"  - At 15 Mpts/s that is $15\times10^{6}\times2.23\times10^{-6}=33.4$ W of receiver electronics, about four times a whole 520-line ToF unit (≈8.5 W in the §C7a model)."))

# =============================================================== §C7b subsection 4
E.append(("X", "- at most ≈65 mm² per sample for any collimated beam at 200 m (Eq. (98));",
          "- at most ≈65 mm² per look for any collimated beam at 200 m (Eq. (98)), ≈260 mm² for the four looks of the §C7a design;"))
E.append(("S", "A steerer changes where the footprint goes, not how large it must be.",
          "Only more *modes per sample*, i.e. more channels, raises the collection per cell",
          "Only more *modes per sample*, i.e. more receivers, raises the collection per cell"))

# =============================================================== §C7b subsection 5
E.append(("L", "**Reaching $E_{\\rm opt}\\approx0.15$ µJ** means improving the terms of Eq. (92)",
r"""**Reaching $E_{\rm opt}\approx0.15$ µJ** means improving the terms of Eq. (92) without changing the geometry. The photoelectrons needed are fixed by detection statistics (120 for four looks, §C0 subsection 10.3), so the efficiency must carry most of it: raising $\eta$ from 0.25 to 0.40 gives $0.30\times0.25/0.40=0.19$ µJ, the §C7a 2032 case, and $\eta=0.50$ gives 0.15 µJ. The alternative is more looks per sample, each collecting its own $A_{\rm mode}$: eight looks ideally need ≈82 photoelectrons, ≈112 with the same margin, spread over twice the area, which gives $0.30\times(112/120)\times(4/8)=0.14$ µJ at the price of eight receivers per beam. A better detector than the full FFT search helps less: a joint search over both ramps saves 12% (§C0 subsection 10.3)."""))
E.append(("X", "| 2026 central (§C7a) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.56 µJ | $3+15\\times2.56=41$ W |",
          "| 2026 central (§C7a) | 0.30 µJ | 15% | 2.0 µJ | 2.23 µJ | 4.25 µJ | $3+15\\times4.25=67$ W |"))
E.append(("X", "| Better steering only (no other change) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.56 µJ | 41 W |",
          "| Better steering only (no other change) | 0.30 µJ | 15% | 2.0 µJ | 2.23 µJ | 4.25 µJ | 67 W |"))
E.append(("X", "| 2032 optimistic (§C7a) | 0.16 µJ | 22% | 0.73 µJ | 0.15 µJ | 0.88 µJ | 16 W (just over) |",
          "| 2032 optimistic (§C7a) | 0.19 µJ | 22% | 0.86 µJ | 0.61 µJ | 1.48 µJ | 25 W |"))
E.append(("L", "- ≈8–13 mW of receive power each, including a ≈1 GS/s ADC and FFT.",
          r"- ≈8–13 mW of receive power each, i.e. ≈2–3 mW for each of its four receivers, including ≈1 GS/s ADCs and FFT. This comes from dividing the receiver power $E_{\rm rx}\dot N$ by the channel count $N_{\rm ch}$, $E_{\rm rx}\dot N/N_{\rm ch}=0.10\ \mu{\rm J}\times15\times10^{6}/(115\ {\rm to}\ 190)$, and then by four. Today's §C7a receiver draws ≈44 mW, 13–22× more."))

# =============================================================== §C7b subsection 6
E.append(("L", "   - What it is: a stacked or monolithic electronic-photonic IC",
          "   - What it is: a stacked or monolithic electronic-photonic IC (photonics and electronics on one chip, or on separate chips bonded on top of each other) with ≥150–256 channels of four LO-matched receivers each, 600–1,000 receivers in all. Each receiver runs at ≈2–3 mW including ADC and FFT (subsection 5), for a few cents of silicon."))
E.append(("X", "   - Signpost: a published chip with ≥256 channels within ≈10 W (§C10.7).",
          "   - Signpost: a published chip with ≥256 receivers at ≤5 mW each. §C10.7's looser signpost, ≥256 channels within ≈10 W, marks the first step."))
E.append(("L", "   - Diversity or multimode coherent reception that lowers $n_{\\rm req}$ and restores coverage.",
          "   - Diversity or multimode coherent reception beyond the four looks already assumed. Each further look collects its own $A_{\\rm mode}$, so eight looks would roughly halve the optical energy per point (subsection 5), and many modes per sample would restore coverage, which subsection 1(b) caps at ≈2% of a 0.05° cell per collimated sample (§C10.3a)."))
E.append(("X", "   - Each extra mode needs its own coherent receiver, so this costs channels and presupposes item 1.",
          "   - Each extra mode needs its own coherent receiver, so this costs receivers and presupposes item 1."))

# =============================================================== §C7b subsection 7
E.append(("X", "| A published coherent receiver chip with ≥256 simultaneous channels including ADC and FFT at ≤20 mW per channel | 2030 | ≈25–35% |",
          "| A published coherent receiver chip with ≥256 simultaneous receivers including ADC and FFT at ≤5 mW per receiver | 2030 | ≈20–30% |"))
E.append(("X", "| The same class of chip in a qualified automotive product | 2032 | ≈10–15% |",
          "| The same class of chip in a qualified automotive product | 2032 | ≈8–12% |"))
E.append(("X", "| FMCW parity on point rate per watt (as in §C7a) | 2032 | ≈5–10% |",
          "| FMCW parity on point rate per watt (as in §C7a) | 2032 | ≈3–7% |"))

# =============================================================== §C10
E.append(("S", "  - A non-fading return needs about 21 [E: for a constant signal the detection probability is the Marcum function",
          "exceeds a normalized threshold $b$.",
          "exceeds a normalized threshold $b$.\n  - These are single-bin figures at $10^{-6}$ per bin. The report's per-point rule (§C0 subsection 10.3: at most $10^{-3}$ false points per point over a 0–300 m search, with the echo's peak found in both chirp ramps) raises them to ≈259 for one look, 120 for two, ≈88 for four and ≈82 for eight looks, and ≈39 for a non-fading return. The power figures below use these per-point values."))
E.append(("L", "  - several watts per beam at 5 µs dwell [E]: with ≤3 dB one-way loss",
r"""  - several watts per beam at 5 µs dwell [E]: with ≤3 dB one-way loss, ≈9 W for four-look and ≈26 W for single-look detection, or ≈540–1,590 W for 60 beams at 12 Mpts/s. At 3 dB one-way loss, 1 W for 5 µs yields 9.8 detected photons, so 88.5 photons need $88.5/9.8=9.0$ W and 259 need $259/9.8=26.5$ W; 12 Mpts/s at 5 µs dwell needs $12\times10^{6}\ {\rm s^{-1}}\times5\ \mu{\rm s}=60$ beams, hence $60\times9.0=540$ W to $60\times26.5=1{,}590$ W. Si trunks (the input waveguides that carry the full power before it is split among elements) are limited by two-photon absorption, a nonlinear loss that grows with intensity (§C8.2); SiN handles watts;"""))
E.append(("S", "- Current integrated OPAs do not combine these (open verification items in Appendix 1).",
          "would need hundreds of watts of optical power,", "would need 0.5–1.6 kW of optical power,"))
E.append(("S", "   - Scaling the measured energy per point as $R^2$",
          r"That agrees with the cell-filling link budget of §C10.2, item 5, Eq. (129): 23–66 µJ for 45–130 photons at 3 dB one-way loss (5 µJ yields 9.8 detected photons there, so $5\ \mu{\rm J}\times45/9.8=23\ \mu{\rm J}$ and $5\ \mu{\rm J}\times130/9.8=66\ \mu{\rm J}$).",
          r"That sits at the low end of the cell-filling link budget of §C10.2, item 5, Eq. (129): 45–132 µJ for 88.5–259 photons at 3 dB one-way loss (5 µJ yields 9.8 detected photons there, so $5\ \mu{\rm J}\times88.5/9.8=45\ \mu{\rm J}$ and $5\ \mu{\rm J}\times259/9.8=132\ \mu{\rm J}$)."))
E.append(("L", "   - **Speckle.** $N_{\\rm req}=10$–30 is roughly the non-fading regime",
r"""   - **Speckle.** $N_{\rm req}=10$–30 is at or below the non-fading requirement: ≈21 detected photons for $P_d=0.9$ at $P_{\rm fa}=10^{-6}$ in one bin, and ≈39 under the report's per-point rule, which searches 0–300 m and needs the peak in both chirp ramps (§C0 subsection 10.3). A single-mode fading return needs about 88 photons in total with four-look diversity, or about 259 with one look, under that rule (§C10.2, item 5). If the looks share one mode's collection (wavelength or time diversity), that raises the coherent requirement to about **180–1,590 W** ($P_{\rm coh}\propto N_{\rm req}/\eta$ from Eq. (134): 88.5 photons at $\eta=0.3$ give $20.4\times88.5/10=181$ W, and 259 photons at $\eta=0.1$ give $20.4\times(259/10)\times3=1{,}590$ W). Looks that each add a mode (polarization or spatial diversity, as in §C7a) collect four times as much, which brings the four-look case back to ≈45 W at $\eta=0.3$."""))
E.append(("X", "| Laser power | Ideal upper bound on nominal footprint fraction at 30 photons per mode | Ideal upper bound at 130 photons per mode |",
          "| Laser power | Ideal upper bound on nominal footprint fraction at 30 photons per mode | Ideal upper bound at 259 photons per mode |"))
E.append(("X", "| 1 W | 0.5% | 0.13% |", "| 1 W | 0.5% | 0.06% |"))
E.append(("X", "| 5 W | 2.7% | 0.6% |", "| 5 W | 2.7% | 0.3% |"))
E.append(("X", "| 20 W | 11% | 2.5% |", "| 20 W | 11% | 1.3% |"))
E.append(("X", "| 100 W | 54% | 13% |", "| 100 W | 54% | 6.3% |"))
E.append(("X", "| ≈200 W | 100% | 25% |", "| ≈200 W | 100% | 13% |"))
E.append(("S", "*How the numbers are derived* [E]: the bound is $f_{\\rm fp}=KP/n_{\\rm mode}$",
          r"For 20 W, $0.163\times20/30=11\%$ at 30 photons and $0.163\times20/130=2.5\%$ at 130 photons. Full coverage at 30 photons needs $P=30/0.163=184$ W, the ≈200 W row, where 130 photons give $0.163\times200/130=25\%$.",
          r"For 20 W, $0.163\times20/30=11\%$ at 30 photons and $0.163\times20/259=1.3\%$ at 259 photons. Full coverage at 30 photons needs $P=30/0.163=184$ W, the ≈200 W row, where 259 photons give $0.163\times200/259=13\%$."))
E.append(("L", "- The 130-photon column approximates a single-look speckle requirement",
r"""- The 259-photon column is the single-look requirement for 90% detection under the report's per-point rule: at most $10^{-3}$ false points per point over a 0–300 m search, with the echo's peak found in both chirp ramps (§C0 subsection 10.3; §C10.2, item 5). A *look* is one independent speckle realization; with several looks the receiver sums returns whose speckle is uncorrelated, which reduces fading. The 30-photon column is the §C7a four-look receiver: 120 photoelectrons summed over four modes (88.5 ideally, 22 per look), which by Eq. (140) has the coverage bound of a single mode at 30 photons."""))
E.append(("L", "- **Speckle and polarization favour ToF.** Single-mode detection fades",
r"""- **Speckle and polarization favour ToF.** Single-mode detection fades (exponential single-speckle statistics). Under the report's detection rule it needs ≈88 photoelectrons with four looks and ≈259 with one for reliable detection, against ≈5 counts for SPAD ToF at night and ≈18 in bright sun (§C0 subsection 10.3). Piggott et al. put coherent detection about 6 dB behind ToF at equal aperture, from polarization and mode weighting."""))

# =============================================================== §D and §F6
E.append(("L", "   - §C7a shows that FMCW costs ≈6× the electrical energy per point.",
          "   - §C7a shows that FMCW costs ≈10× the electrical energy per point. Each extra simultaneous line also costs coherent receiver chains (four in the §C7a design; each a mixer with the local laser copy, a balanced detector and a fast ADC, the analog-to-digital converter) plus ≈50–100 mW of light."))
E.append(("S", "- **Speckle diversity on chip.** Single-mode coherent detection sees Rayleigh fading.",
          "which raises detection probability without extra laser power.",
          "which raises detection probability without extra laser power. The §C7a model already assumes four looks per point (two polarizations × two spatial modes), and each look needs its own receiver, so the research value lies in cheap on-chip diversity (§C0 subsection 10.3, §C7b subsection 3)."))
