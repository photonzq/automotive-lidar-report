## Readability review of §C0, subsections 1–9 (lines 1494–1857)

**Coverage:** the whole block was read. Cross-references past line 7341 are 6 lines lower after an insertion in §D7 (the §E4 table at 7667 is now at about 7673). The content behind the "Used in" pointers (§C3b, §C4b, §C5, §E12) was checked only for the headings, and the vendor figures (Z+F, Leica, ST, Sony) were not checked against their sources.

### 1. Overall assessment
Each subsection opens with the question it answers and closes with what it means for the sensor, and most numbers show their substitution. I recomputed about 60 of them in memory, with no files written: Poisson tails, Albersheim, Swerling, the fog reaches, rain loss, the Cramér–Rao bound, coherent share, solid angles and photon counts. All match the stated rounding. Equations (23)–(28) are numbered in global sequence (Eqs. (1)–(188) checked). There are no \( \) or \[ \] delimiters and no versioning words, and currency uses \$.

The three main systemic problems:
- **Symbols drift between subsections.** $N_s$ has four meanings, and $R_{\max}$ means unambiguous range here but maximum detection range in subsection 10 and Part A. $\Delta f$, $\Omega$ and $\rho$ each carry two meanings, and one quantity often has several symbols.
- **Several prose conclusions disagree with the numbers next to them.** Examples: FMCW precision written as ≈1 cm where the relation gives 1.5 cm; the InGaAs excess-noise claim; "needs more" next to 88 < 130; the fog reach versus §E4; the worked cases of subsection 7 versus 10.3.
- **Subsection 9 is out of scope, and a few derivation steps are skipped elsewhere.** Subsection 9 (126 lines, five tables) has grown into a product and market survey inside a physics primer. The skipped steps are: the étendue relation, the Cramér–Rao bound to range, coherent share versus $L_c$, the APD gain optimum, and the required LO power.

### 2. Findings (most severe first)

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

### 3. Consistency flags to check elsewhere
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