r"""Paralyzable dead time (Sony passive recharge: live fraction exp(-r tau)) and the 1,550 nm
eye-safety allowance.  Written against report_after_dt.md (current numbering)."""

E = []

# =============================================================== executive summary
E.append(("S", "     - At 200 m and 10% reflectivity, the modelled electrical energy per point is ≈4.3 µJ",
          r"against ≈0.53 µJ for 940 nm SPAD ToF, whose SPADs lose ≈20% of the signal to their 6 ns dead time in bright sun. That is ≈8×, since $4.25/0.525\approx8.1$",
          r"against ≈0.54 µJ for 940 nm SPAD ToF, whose SPADs lose ≈22% of the signal to their 6 ns dead time in bright sun. That is ≈8×, since $4.25/0.536\approx7.9$"))
E.append(("S", "     - There are three causes. The first is coherent collection with speckle fading.",
          "against ≈18 counts for SPAD ToF in bright sun", "against ≈17 counts for SPAD ToF in bright sun"))
E.append(("S", "     - **Better beam steering would not change this (§C7b).**",
          "and ≈0.15 µJ of optical energy per point.",
          "and ≈0.15 µJ of optical energy per point. The 1,550 nm eye-safety allowance (≈9 W of scanned light over a 120° × 25° field) buys FMCW range at moderate point rates and brighter channels, not fewer watts per point."))

# =============================================================== §C0 10.3
E.append(("X", r"- **Bright sun, $b=2.94$:** $P(N\ge15\mid2.94)=5.2\times10^{-7}$ just fails and $P(N\ge16\mid2.94)=9.5\times10^{-8}$ passes, so $n_{\rm th}=16$.",
          r"- **Bright sun, $b=2.87$:** $P(N\ge14\mid2.87)=2.0\times10^{-6}$ fails and $P(N\ge15\mid2.87)=3.8\times10^{-7}$ passes, so $n_{\rm th}=15$."))
E.append(("S", "- **Where $b=2.94$ comes from** [E].", "- **Where $b=2.94$ comes from** [E].", "- **Where $b=2.87$ comes from** [E]."))
E.append(("L", "  - Eq. (81) gives the dead fraction. Each of the nine SPADs counts",
          r"  - Eq. (81) gives the dead fraction. Sony's passively recharged SPADs behave paralyzably (§C5a): a SPAD is live only if no photon arrived during the last $\tau_d$. Each of the nine SPADs counts $r=3.66\times10^{8}/9=4.06\times10^{7}$ s⁻¹, so $r\tau_d=0.244$ for $\tau_d=6$ ns, the live fraction is $e^{-0.244}=0.784$ and $f_{\rm dead}=0.216$."))
E.append(("S", "  - Eq. (97) of §C7b, multiplied by the live fraction $1-f_{\\rm dead}$",
          r"=3.66\times10^{8}\times10^{-9}\times10\times0.804=2.94$.", r"=3.66\times10^{8}\times10^{-9}\times10\times0.784=2.87$."))
E.append(("S", "  - Over the 20.8 µs a point listens, the same rate gives",
          r"$3.66\times10^{8}\times20.8\times10^{-6}\times0.804\approx6{,}120$ background events",
          r"$3.66\times10^{8}\times20.8\times10^{-6}\times0.784\approx5{,}960$ background events"))
E.append(("S", "  - The dead time blinds the SPADs to signal photons as well:",
          r"only the live fraction 0.804 of the echo can be counted, so the §C7a model multiplies the SPAD's signal efficiency by it, $0.5\times0.37\times0.804=0.149$.",
          r"only the live fraction 0.784 of the echo can be counted, so the §C7a model multiplies the SPAD's signal efficiency by it, $0.5\times0.37\times0.784=0.145$."))
E.append(("X", r"| Photon counting, bright sun ($b=2.94$, $n_{\rm th}=16$) | 12.7 | 18.4 | 0.99 | 1.00 |",
          r"| Photon counting, bright sun ($b=2.87$, $n_{\rm th}=15$) | 11.8 | 17.3 | 1.00 | 1.00 |"))
E.append(("X", r"- **Worked check, bright sun:** $s=18.4$ puts the total mean at $s+b=21.3$, and a Poisson count of mean 21.3 reaches 16 with probability 0.90.",
          r"- **Worked check, bright sun:** $s=17.3$ puts the total mean at $s+b=20.1$, and a Poisson count of mean 20.1 reaches 15 with probability 0.90."))
E.append(("L", "- **ToF:** the model's 25 counts are 1.36× the 18.4 that an ideal counter needs in bright sun.",
          r"- **ToF:** the model's 25 counts are 1.45× the 17.3 that an ideal counter needs in bright sun. The dead time is not part of this margin, because it is counted in the SPAD's efficiency (the live fraction above, §C7a(a)). The margin covers a return spread over about two bins, which needs 22.5 counts summed over both (×1.30), and pile-up distortion (§C6). In the model's high case, a fully sunlit scene of reflectance 0.9 ($b=4.49$, $n_{\rm th}=19$), the ideal counter needs 20.3."))
E.append(("S", "- **FMCW:** the model's 120 photoelectrons over four looks", "carry the same 1.36× margin over the ideal 88.5.",
          "carry a 1.36× margin over the ideal 88.5, close to ToF's 1.45×."))
E.append(("S", "- **Where FMCW's extra photons go**", "88.5 against the counter's 18.4 in bright sun", "88.5 against the counter's 17.3 in bright sun"))
E.append(("S", "  - *the noise floor, ×1.2:*", "  - *the noise floor, ×1.2:*", "  - *the noise floor, ×1.3:*"))
E.append(("S", "  - *the noise floor, ×1.3:*", "the Poisson tail of 2.94 counts;", "the Poisson tail of 2.87 counts;"))
E.append(("S", "- **The search.** The threshold rises with the logarithm", "lower the requirement by 8–33%", "lower the requirement by 7–33%"))
E.append(("X", "| Full search (the rule above) | 88.5 | 18.4 |", "| Full search (the rule above) | 88.5 | 17.3 |"))
E.append(("S", "| $10^{-2}$ false points per point, pruned by neighbour checks |", "| 81.6 | 16.0 |", "| 81.6 | 16.1 |"))
E.append(("S", "| Tracking window of 20 bins per ramp around a predicted return |", "| 59.6 | 14.8 |", "| 59.6 | 13.7 |"))
E.append(("S", "**What this means for the comparison** [E]. Under one rule,", "needs 18–25 counts per point", "needs 17–25 counts per point"))
E.append(("S", "**What this means for the comparison** [E]. Under one rule,", "an ideal counter in bright sun (18.4)", "an ideal counter in bright sun (17.3)"))

# =============================================================== §C0 10.4
E.append(("S", "| SPAD dToF, bright sun | 940 nm | 25 |", "| 25 | 0.149 |", "| 25 | 0.145 |"))
E.append(("S", "| SPAD dToF, bright sun | 940 nm | 25 |", "| 94.5 dB |", "| 94.4 dB |"))
E.append(("S", "  - SPAD: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction",
          "live fraction 0.804 (6 ns dead time, 10.3);", "live fraction 0.784 (6 ns paralyzable dead time, 10.3);"))
E.append(("S", "- **Worked (SPAD),** from Eq. (41):",
          r"$25\times2.11\times10^{-19}/(0.149\times10^{-7})=3.55\times10^{-10}$, and $-10\log_{10}(3.55\times10^{-10})=94.5$ dB.",
          r"$25\times2.11\times10^{-19}/(0.145\times10^{-7})=3.64\times10^{-10}$, and $-10\log_{10}(3.64\times10^{-10})=94.4$ dB."))
E.append(("L", "  - SPAD case, $D=25$ mm:",
          r"  - SPAD case, $D=25$ mm: $0.0125\times\sqrt{0.1/3.64\times10^{-10}}=207$ m, or 204 m with clear air. The 10 and 50 mm lenses reach 82 and 400 m."))
E.append(("L", "  - The APD case reaches 326 m with 25 mm.",
          r"  - The APD case reaches 326 m with 25 mm. Its per-point need $n_{\rm req}E_{\rm ph}/\eta$ is 7.8× the SPAD's, but its 20× larger energy leaves a 2.6× margin, i.e. $\sqrt{2.6}=1.6\times$ the range."))

# =============================================================== §C0 10.5
E.append(("S", "$$\\frac{E_{\\rm FMCW}}{E_{\\rm SPAD}}=", r"=0.43\times\frac{1}{t^2(0.45)^2}=0.43\times5.9=2.6 .",
          r"=0.42\times\frac{1}{t^2(0.45)^2}=0.42\times5.9=2.5 ."))
E.append(("L", "  - The first factor is $(30\\times1.28",
          r"  - The first factor is $(30\times1.28\times10^{-19}/0.25)/(25\times2.11\times10^{-19}/0.145)=1.54\times10^{-17}/3.64\times10^{-17}=0.42$."))
E.append(("X", "  - With clear-air loss the ratio is 2.5 at 100–500 m.", "  - With clear-air loss the ratio is 2.4 at 100–500 m."))
E.append(("S", "- **Against a fixed 25 mm SPAD receiver**,", "6.5× at 100 m, 3.2× at 200 m, 2.1× at 300 m and 1.3× at 500 m.",
          "6.3× at 100 m, 3.1× at 200 m, 2.1× at 300 m and 1.2× at 500 m."))
E.append(("L", "- **Linear APD against SPAD with the same lens:**",
          r"- **Linear APD against SPAD with the same lens:** $(890\times1.28\times10^{-19}/0.40)/(25\times2.11\times10^{-19}/0.145)=7.8$. That is almost eight times the energy per point at every range, which the 1,550 nm eye-safety limits can pay for at low point rates (§C4c)."))

# =============================================================== §C0 10.6, 10.7, 10.8
E.append(("L", "- **SPAD ToF at 940 nm with a 25 mm lens** needs 94 nJ per point",
          r"- **SPAD ToF at 940 nm with a 25 mm lens** needs 96 nJ per point: the 0.1 µJ of 10.4, which reaches 204 m, scaled by $(200/204)^2=0.96$. Without the 0.15 dB of clear-air loss this is the ≈93 nJ of §C7b subsection 1."))
E.append(("S", "| SPAD ToF, 940 nm, 25 mm lens | — |", "| 94 nJ (0.31×) |", "| 96 nJ (0.32×) |"))
E.append(("S", "  - A 7 mm aperture matches ToF's tolerance of dark targets and fog.", "sixteen times ToF's 94 nJ.", "sixteen times ToF's 96 nJ."))
E.append(("S", "- **Photons, ToF.** Per shot the SPAD design emits 9.4 nJ (its 94 nJ over ten shots).",
          r"Per shot the SPAD design emits 9.4 nJ (its 94 nJ over ten shots). The sign at 5 m then returns about $4.3\times10^{8}$ photons,",
          r"Per shot the SPAD design emits 9.6 nJ (its 96 nJ over ten shots). The sign at 5 m then returns about $4.4\times10^{8}$ photons,"))
E.append(("S", "- **Eye safety** caps $E_{\\rm tx}$ per direction and per unit time (subsection 5, §C4c).",
          "It would appear as a wavelength-dependent vertical limit in Figure C0.10c.",
          "It would appear as a wavelength-dependent vertical limit in Figure C0.10c. §C7b subsection 2(i) puts numbers on it for the two designs of §C7a."))

# =============================================================== §C4c
E.append(("S", "- **1,550 nm CW (FMCW) can emit several watts when scanned**",
          "heat and wall-plug efficiency (optical output power per unit of electrical input power) are (§C7a).",
          "heat and wall-plug efficiency (optical output power per unit of electrical input power) are (§C7a). The §C7a model's FMCW needs 3.0 W at 10 Mpts/s and 7.6 W at 25 Mpts/s at 200 m; at 300 m and 25 Mpts/s its 11 W would exceed the allowance for this field (§C7b subsection 2(i))."))

# =============================================================== SiPM passage (dead time)
E.append(("L", "- A 3×3 SPAD macro-pixel with the same field can be dead **8–59% of the time** in bright sun (§C6(d))",
          "- A 3×3 SPAD macro-pixel with the same field can be dead **9–77% of the time** in bright sun (§C6(d)), and pile-up distorts its histogram. A passively recharged SPAD such as Sony's is paralyzable: a photon that arrives while it recovers restarts the recovery (§C5a), so the SPAD is live only if no photon arrived during the last dead time. Counting at rate $r$, it is dead a fraction"))
E.append(("X", r"  $$f_{\rm dead}=\frac{r\,\tau_d}{1+r\,\tau_d} \tag{64}$$", r"  $$f_{\rm dead}=1-e^{-r\,\tau_d} \tag{64}$$"))
E.append(("S", "  of the time, where $r$ is the per-SPAD count rate (s⁻¹) and $\\tau_d$ the dead time (s).",
          r"giving $0.09/1.09\approx8\%$, to $r=2.2\times10^{9}/9\approx2.4\times10^{8}\ {\rm s^{-1}}$ (905 nm, 20 nm filter, 90% scene), giving $1.47/2.47\approx59\%$ by Eq. (64).",
          r"giving $1-e^{-0.09}\approx9\%$, to $r=2.2\times10^{9}/9\approx2.4\times10^{8}\ {\rm s^{-1}}$ (905 nm, 20 nm filter, 90% scene), giving $1-e^{-1.47}\approx77\%$ by Eq. (64). An actively recharged, non-paralyzable SPAD would be dead $r\tau_d/(1+r\tau_d)$ of the time, 8–59% (§C6(d))."))

# =============================================================== §C6(d)
E.append(("X", "| 905 nm, 20 nm filter, ρ = 0.9 scene | about 2.2×10⁹ | **59%** |", "| 905 nm, 20 nm filter, ρ = 0.9 scene | about 2.2×10⁹ | **77%** |"))
E.append(("X", "| 905 nm, 40 nm filter (EEL-type) | about 4.4×10⁹ | 75% |", "| 905 nm, 40 nm filter (EEL-type) | about 4.4×10⁹ | 95% |"))
E.append(("X", "| 940 nm, 10 nm filter (VCSEL-type) | about 6×10⁸ | 29% |", "| 940 nm, 10 nm filter (VCSEL-type) | about 6×10⁸ | 33% |"))
E.append(("L", "- **Dead fraction.** This assumes that each of the nine SPADs of the 3×3 macro-pixel sees the per-SPAD background rate",
          r"- **Dead fraction.** This assumes that each of the nine SPADs of the 3×3 macro-pixel sees the per-SPAD background rate $r=r_{\rm bg}/9$ (s⁻¹). Sony's passively recharged SPADs behave paralyzably (§C5a): a photon that arrives while the SPAD recovers restarts its recovery, so the SPAD is live only if no photon arrived during the last $\tau_d$, which happens with probability $e^{-r\tau_d}$. An actively recharged SPAD is non-paralyzable: such a photon is simply lost, the SPAD records counts at the rate $r/(1+r\tau_d)$ and is dead for $\tau_d$ after each. The fraction of time a SPAD is dead is therefore"))
E.append(("X", r"  $$f_{\rm dead}=\frac{r\tau_d}{1+r\tau_d} \tag{81}$$",
          r"  $$f_{\rm dead}=1-e^{-r\tau_d}\ \ \text{(paralyzable)},\qquad f_{\rm dead}=\frac{r\tau_d}{1+r\tau_d}\ \ \text{(non-paralyzable)} \tag{81}$$"))
E.append(("L", "  with $\\tau_d=6$ ns. For 905 nm, 20 nm:",
          r"  with $\tau_d=6$ ns. The table uses the paralyzable form. For 905 nm, 20 nm: $r=2.2\times10^{9}/9=2.4\times10^{8}$ s⁻¹, $r\tau_d=1.47$ and $1-e^{-1.47}=77\%$. The 40 nm case gives $r\tau_d=2.9$ and 95%; the 940 nm case gives $r\tau_d=0.40$ and 33%. Non-paralyzable SPADs would be dead 59%, 75% and 29% of the time."))
E.append(("L", "- **In the ToF energy model.** The §C7a model and the detection statistics of §C0 subsection 10.3",
          r"- **In the ToF energy model.** The §C7a model and the detection statistics of §C0 subsection 10.3 apply Eq. (80) and the paralyzable form of Eq. (81) at the model's PDE of 0.37, because the same SPADs count signal and background. The 940 nm, 10 nm case then gives $7.31\times10^{8}$ s⁻¹ and a 39% dead fraction for the fully sunlit $\rho_{\rm scene}=0.9$ scene ($r\tau_d=0.49$), and $3.66\times10^{8}$ s⁻¹ and 22% for the model's central case of half that background. The same live fraction multiplies the signal, because a SPAD that is dead when the echo arrives misses it; the §C7a model therefore uses a signal efficiency of $0.5\times0.37\times0.784=0.145$ in bright sun."))
E.append(("S", "- In a bright sunlit scene, SNR (signal-to-noise ratio) per bin is not the problem.",
          "they skew histograms and cut effective PDE by up to half,",
          "they skew histograms and cut effective PDE by a third at 940 nm behind a 10 nm filter and by three-quarters or more at 905 nm behind 20–40 nm filters,"))
E.append(("L", "- **Shorter dead time (active recharge).**",
          r"- **Shorter dead time (active recharge).** An active recharge circuit resets the SPAD quickly after each avalanche instead of letting it recover through a resistor, and makes it non-paralyzable (Eq. (81), right-hand form). In the bright 940 nm/10 nm case ($r=6.1\times10^{8}/9=6.8\times10^{7}$ s⁻¹ per SPAD) a passively recharged SPAD with Sony's 6 ns is dead $1-e^{-0.41}=34\%$ of the time. With active recharge it is dead 29% at 6 ns ($0.41/1.41$), 17% at 3 ns ($0.20/1.20$) and 58% at 20 ns ($r\tau_d=1.36$, and $1.36/2.36=0.58$). The trade-off is more afterpulsing: carriers trapped during one avalanche are released after a fast reset and trigger a false count."))

# =============================================================== §C7a
E.append(("S", "  - The model below gives about **8×** more electrical energy per point than 940 nm SPAD ToF",
          r"($4.25/0.525\approx8.1$). This narrows to about **4×** in an optimistic 2032 projection ($1.48/0.357\approx4.1$;",
          r"($4.25/0.536\approx7.9$). This narrows to about **4×** in an optimistic 2032 projection ($1.48/0.368\approx4.0$;"))
E.append(("X", "**(a) Optical energy per point: ≈91 nJ for ToF against ≈0.30 µJ for FMCW.**",
          "**(a) Optical energy per point: ≈93 nJ for ToF against ≈0.30 µJ for FMCW.**"))
E.append(("S", "- **SPAD dead time 6 ns**, the state of the art:",
          "In bright sun each SPAD is dead 19.6% of the time (§C0 subsection 10.3), and a SPAD that is dead when the echo arrives misses it, so the live fraction 0.804 multiplies the signal efficiency as well as the background.",
          "Its passive recharge behaves paralyzably, since the 60 Mcps ceiling equals $1/(e\\tau_d)$ (§C5a): a SPAD is live only if no photon arrived in the last 6 ns. In bright sun each SPAD is therefore dead 21.6% of the time (§C0 subsection 10.3), and a SPAD that is dead when the echo arrives misses it, so the live fraction 0.784 multiplies the signal efficiency as well as the background."))
E.append(("S", "- **ToF:** $A_{\\rm eff}=A_{\\rm rx}$ is the whole 25 mm receive aperture (491 mm²)",
          "an ideal counter needs 18.4 in the model's bright sun", "an ideal counter needs 17.3 in the model's bright sun"))
E.append(("S", "- **ToF:** $A_{\\rm eff}=A_{\\rm rx}$ is the whole 25 mm receive aperture (491 mm²)",
          r"the bright-sun live fraction of 0.804 the result is **≈91 nJ** (58–152). With $n_{\rm req}=25$ (central), $E_{\rm ph}=2.11\times10^{-19}$ J, $\pi R^2=\pi\times200^2=1.26\times10^{5}$ m², $\rho=0.1$ and $\eta=0.5\times0.37\times0.804=0.149$ (optics transmission × PDE × live fraction): $E_{\rm opt}=25\times2.11\times10^{-19}\times1.26\times10^{5}/(0.1\times4.91\times10^{-4}\times0.149)=6.64\times10^{-13}/(7.30\times10^{-6})\approx9.1\times10^{-8}$ J. The low case is night (20 counts, no dead time, $\eta=0.185$): 58 nJ. The high case is the fully sunlit scene (35 counts, live fraction 0.672, $\eta=0.124$): 152 nJ.",
          r"the bright-sun live fraction of 0.784 the result is **≈93 nJ** (58–167). With $n_{\rm req}=25$ (central), $E_{\rm ph}=2.11\times10^{-19}$ J, $\pi R^2=\pi\times200^2=1.26\times10^{5}$ m², $\rho=0.1$ and $\eta=0.5\times0.37\times0.784=0.145$ (optics transmission × PDE × live fraction): $E_{\rm opt}=25\times2.11\times10^{-19}\times1.26\times10^{5}/(0.1\times4.91\times10^{-4}\times0.145)=6.64\times10^{-13}/(7.12\times10^{-6})\approx9.3\times10^{-8}$ J. The low case is night (20 counts, no dead time, $\eta=0.185$): 58 nJ. The high case is the fully sunlit scene (35 counts, live fraction 0.614, $\eta=0.114$): 167 nJ."))
E.append(("S", "  - Single-mode returns fade, so detection needs more signal, and an FMCW point must show its peak",
          "The model uses $n_{\\rm req}=120$, 30 per look: the same ×1.36 implementation margin that takes ToF from 18.4 to 25 counts.",
          "The model uses $n_{\\rm req}=120$, 30 per look: a ×1.36 implementation margin, close to the ×1.45 that takes ToF from 17.3 to 25 counts."))
E.append(("X", "FMCW therefore needs ≈3.3× more optical energy per point than ToF (0.30 µJ against 91 nJ). The ≈3.3× ratio splits into four factors:",
          "FMCW therefore needs ≈3.2× more optical energy per point than ToF (0.30 µJ against 93 nJ). The ≈3.2× ratio splits into four factors:"))
E.append(("X", "- efficiency (0.60×), ToF's 0.149, which includes the SPADs' dead time in bright sun, against FMCW's 0.25.",
          "- efficiency (0.58×), ToF's 0.145, which includes the SPADs' dead time in bright sun, against FMCW's 0.25."))
E.append(("S", "**(b) Laser wall-plug efficiency and power handling.**",
          "and everything not emitted becomes heat.",
          "and everything not emitted becomes heat. Eye safety allows ≈9 W of scanned light over a 120° × 25° field at 1,550 nm, which FMCW's 3.0–7.6 W at 10–25 Mpts/s and 200 m fits within (§C7b subsection 2(i))."))
E.append(("L", "- **ToF is event-driven.** A SPAD-SoC",
r"""- **ToF is event-driven.** A SPAD-SoC (a SPAD array stacked on its own processing chip) spends energy per avalanche and histogram increment (a few pJ each; ≈5,990 events per point in bright sun), plus fixed clocking and readout. Calibrated to Sony's 1.19 W development chip (§C5a), that is **≈70 nJ per point** (20–126). Its histogram also has ≈2,000 bins, but they are *counted* sparsely, not *sampled and transformed* densely. The event count is background count rate × listening time × live fraction + signal counts, $r_{\rm bg}\,t_{\rm listen}\,(1-f_{\rm dead})+n_{\rm req}$: $3.66\times10^{8}\ {\rm s^{-1}}\times20.8\ \mu{\rm s}\times0.784+25\approx5{,}990$. This takes a background count rate $r_{\rm bg}=3.66\times10^{8}$ s⁻¹ per macro-pixel, half the fully sunlit 940 nm case of §C6(d) (Eq. (80)) evaluated at the model's PDE of 0.37; a listening time $t_{\rm listen}=20.8$ µs per point (a model input, equal to one column period of a 520-line sensor at 25 Mpts/s); the live fraction 0.784 that the paralyzable form of Eq. (81) gives at this rate (the SPADs are recharging and blind 21.6% of the time); and $n_{\rm req}=25$ signal counts. §C0 subsection 10.3 derives the same background as 2.87 counts per 1 ns bin. At 5 pJ per event plus a fixed 40 nJ per point, $E=40\ {\rm nJ}+5{,}990\times5\ {\rm pJ}=70$ nJ. The fixed term follows the calibration: 1–2 W for an IMX479-class chip at 25 Mpts/s is 40–80 nJ per point including events (Sony's 1.19 W divided by $25\times10^{6}$ s⁻¹ is 48 nJ). The range runs from 20 nJ (night: 20 nJ fixed, 4 pJ per event) to $60\ {\rm nJ}+(7.31\times10^{8}\times20.8\ \mu{\rm s}\times0.614+35)\times7\ {\rm pJ}=126$ nJ (the fully sunlit scene, live fraction 0.614)."""))
E.append(("S", "- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m",
          r"The ToF unit is $3\ {\rm W}+1.25\times10^{7}\times0.525\ \mu{\rm J}\approx9.6$ W.",
          r"The ToF unit is $3\ {\rm W}+1.25\times10^{7}\times0.536\ \mu{\rm J}\approx9.7$ W."))
E.append(("X", "| Counts or photoelectrons needed per point (ideal; model) | 18.4; 25 | 88.5; 120 (four looks) | 18.4; 25 | 88.5; 120 |",
          "| Counts or photoelectrons needed per point (ideal; model) | 17.3; 25 | 88.5; 120 (four looks) | 18.0; 25 | 88.5; 120 |"))
E.append(("X", "| Optical energy per point | 91 nJ | 0.30 µJ | 78 nJ | 0.19 µJ |", "| Optical energy per point | 93 nJ | 0.30 µJ | 81 nJ | 0.19 µJ |"))
E.append(("X", "| Laser/SOA electrical energy | 0.45 µJ | 2.0 µJ | 0.31 µJ | 0.86 µJ |", "| Laser/SOA electrical energy | 0.47 µJ | 2.0 µJ | 0.32 µJ | 0.86 µJ |"))
E.append(("X", "| Receiver electronics | 0.07 µJ | 2.2 µJ (four receivers) | 0.045 µJ | 0.61 µJ |",
          "| Receiver electronics | 0.07 µJ | 2.2 µJ (four receivers) | 0.044 µJ | 0.61 µJ |"))
E.append(("X", "| **Total per point** | **0.53 µJ** | **4.25 µJ** | **0.36 µJ** | **1.48 µJ** |",
          "| **Total per point** | **0.54 µJ** | **4.25 µJ** | **0.37 µJ** | **1.48 µJ** |"))
E.append(("X", "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 8.3 W | 46 W | 6.6 W | 18 W |",
          "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 8.4 W | 46 W | 6.7 W | 18 W |"))
E.append(("S", "- All entries are the central cases of the companion script. **Optical energy** uses",
          r"ToF 2026 is 91 nJ and FMCW 2026 0.30 µJ (worked in §2(a)). ToF 2032 raises PDE from 0.37 to 0.45, which also raises the sunlight counted and the dead fraction (22.9%, live fraction 0.771), giving $91\times(0.37\times0.804)/(0.45\times0.771)=78$ nJ;",
          r"ToF 2026 is 93 nJ and FMCW 2026 0.30 µJ (worked in §2(a)). ToF 2032 raises PDE from 0.37 to 0.45, which also raises the sunlight counted and the dead fraction (25.7%, live fraction 0.743), giving $93\times(0.37\times0.784)/(0.45\times0.743)=81$ nJ;"))
E.append(("S", "- All entries are the central cases of the companion script. **Optical energy** uses",
          "The counts row gives the ideal requirement of §C0 subsection 10.3 and the model's value, 1.36× higher for both receivers.",
          "The counts row gives the ideal requirement of §C0 subsection 10.3 and the model's value, 1.45× (ToF 2026) and 1.36× (FMCW) higher."))
E.append(("S", "- **Laser/SOA electrical energy** is $E_{\\rm opt}/\\eta_{\\rm wp}$", r"$91\ {\rm nJ}/0.20=0.45$ µJ", r"$93\ {\rm nJ}/0.20=0.47$ µJ"))
E.append(("S", "- **Laser/SOA electrical energy** is $E_{\\rm opt}/\\eta_{\\rm wp}$", r"$78\ {\rm nJ}/0.25=0.31$ µJ", r"$81\ {\rm nJ}/0.25=0.32$ µJ"))
E.append(("S", "- **Receiver electronics:** ToF is a fixed 40 nJ (2026) or 20 nJ (2032) plus",
          "≈6,140 or ≈7,160 events at 5 or 3.5 pJ, giving 71 and 45 nJ", "≈5,990 or ≈6,900 events at 5 or 3.5 pJ, giving 70 and 44 nJ"))
E.append(("S", "- **Sensor power** is $3\\ {\\rm W}+\\dot N E_{\\rm total}$",
          r"ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.525\times10^{-6}=8.3$ W.",
          r"ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.536\times10^{-6}=8.4$ W."))

# =============================================================== §C7b short answer and subsection 1
E.append(("S", "- **Per joule of emitted light, FMCW buys ≈3.3× fewer sampled points than 940 nm SPAD ToF.",
          "FMCW buys ≈3.3× fewer sampled points", "FMCW buys ≈3.2× fewer sampled points"))
E.append(("S", "  - The result is ≈0.30 µJ per FMCW sample against ≈91 nJ per ToF point", "against ≈91 nJ per ToF point", "against ≈93 nJ per ToF point"))
E.append(("S", "  - ToF must pulse so that sunlight competes with the signal only inside a 1 ns timing bin.",
          "it would need ≈16× more energy to stand out.", "it would need ≈15× more energy to stand out."))
E.append(("S", "  - Laser linewidth enters through $\\eta_{\\rm coh}=e^{-2\\pi\\Delta\\nu\\cdot2R/c}$:",
          "with a 100 kHz laser the same sensor needs ≈160 W.",
          "with a 100 kHz laser the same sensor needs ≈160 W.\n"
          "- **The 1,550 nm eye-safety allowance buys range, not watts per point** (subsection 2(i)). Class 1 at 1,550 nm allows ≈9 W of scanned light over a 120° × 25° field: 3× what FMCW needs at 10 Mpts/s and 200 m, but only 1.2× at 25 Mpts/s.\n"
          "  - The headroom extends eye-safe reach towards ≈600 m at moderate point rates, where 940 nm ToF runs into its own limits, and it permits brighter channels, which pay if the transmitter is gated off while its echo would be wasted.\n"
          "  - It does not lower FMCW's energy per point: the photons a point needs are set by collection and detection statistics."))
E.append(("S", "This subsection asks how much emitted light each lidar architecture needs to measure one point at 200 m",
          "A 940 nm SPAD time-of-flight sensor needs ≈91 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, about 3.3× more.",
          "A 940 nm SPAD time-of-flight sensor needs ≈93 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, about 3.2× more."))
E.append(("X", r"  - SPAD ToF: $91\ {\rm nJ}\times15\times10^{6}\ {\rm s^{-1}}=1.4$ W;", r"  - SPAD ToF: $93\ {\rm nJ}\times15\times10^{6}\ {\rm s^{-1}}=1.4$ W;"))
E.append(("S", "  - **In the §C7a model:** a macro-pixel (a group of SPADs read out as one pixel) in bright sun counts",
          r"It is dead (unable to count) for 19.6% of that time (Eq. (81)), so it is live for a fraction 0.804 of it. That gives $3.66\times10^{8}\times20.8\times10^{-6}\times0.804\approx6{,}120$ background events per point.",
          r"It is dead (unable to count) for 21.6% of that time (Eq. (81), paralyzable form), so it is live for a fraction 0.784 of it. That gives $3.66\times10^{8}\times20.8\times10^{-6}\times0.784\approx5{,}960$ background events per point."))
E.append(("L", "  - **Per bin:** these events are spread over the ≈2,080 histogram bins of 1 ns",
          r"  - **Per bin:** these events are spread over the ≈2,080 histogram bins of 1 ns in each shot's 2.08 µs listening window (≈300 m of range), so there are $5{,}960/2{,}080\approx2.87$ counts per bin. Eq. (97), with the 0.784 live fraction, gives the same: $3.66\times10^{8}\times10^{-9}\times10\times0.784=2.87$. So ≈25 signal counts in one bin stand out clearly: the detection threshold is 15 counts (§C0 subsection 10.3)."))
E.append(("L", "  - **The same energy spread evenly in time,** as with CW light, would have to stand out against all 6,120 events.",
          r"  - **The same energy spread evenly in time,** as with CW light, would have to stand out against all 5,960 events. The random (Poisson) fluctuation of 5,960 counts is $\sqrt{5{,}960}\approx77$. At 5 standard deviations that takes $5\sqrt{5{,}960}\approx390$ counts: ≈15× more energy per point, before any requirement on ranging precision."))
E.append(("S", "- **Counts needed.** One mode means one speckle.", "The model uses 120, the same ×1.36 margin that takes ToF from 18.4 to 25 counts.",
          "The model uses 120, a ×1.36 margin, close to the ×1.45 that takes ToF from 17.3 to 25 counts."))
E.append(("S", "| 940 nm SPAD or SiPM dToF, scanned or line-flash, 25 mm lens |", "| 25 counts | 0.149 | 91 nJ |", "| 25 counts | 0.145 | 93 nJ |"))
E.append(("S", "- **Energy column:** Eq. (96),", r"(0.1\times4.91\times10^{-4}\times0.149)=9.1\times10^{-8}$ J.", r"(0.1\times4.91\times10^{-4}\times0.145)=9.3\times10^{-8}$ J."))
E.append(("S", "  - ToF: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction",
          "live fraction 0.804 (6 ns dead time, §C7a(a));", "live fraction 0.784 (6 ns paralyzable dead time, §C7a(a));"))
E.append(("S", "- **Last column:** $1/E_{\\rm opt}$;", r"$1/(9.1\times10^{-8}\ {\rm J})=1.1\times10^{7}$", r"$1/(9.3\times10^{-8}\ {\rm J})=1.1\times10^{7}$"))
E.append(("S", "- **The FMCW efficiency is a design value.**",
          "so FMCW buys 5–7.5× (discrete fibre chain) or ≈15× (integrated array) fewer points per optical joule than SPAD ToF, instead of ≈3.3×.",
          "so FMCW buys 5–7× (discrete fibre chain) or ≈14× (integrated array) fewer points per optical joule than SPAD ToF, instead of ≈3.2×."))
E.append(("S", "**(d) Why FMCW buys ≈3.3× fewer sampled points per joule than SPAD ToF.**",
          "**(d) Why FMCW buys ≈3.3× fewer sampled points per joule than SPAD ToF.**",
          "**(d) Why FMCW buys ≈3.2× fewer sampled points per joule than SPAD ToF.**"))
E.append(("S", "**(d) Why FMCW buys ≈3.2× fewer sampled points per joule than SPAD ToF.**",
          "the optical energy per SPAD ToF point (91 nJ)", "the optical energy per SPAD ToF point (93 nJ)"))
E.append(("S", "$$\\frac{E_{\\rm FMCW}}{E_{\\rm ToF}}=\\underbrace{\\frac{491}{255}}_{\\rm collection}",
          r"\underbrace{\frac{0.149}{0.25}}_{\rm efficiency}=1.93\times4.8\times0.607\times0.596\approx3.3.",
          r"\underbrace{\frac{0.145}{0.25}}_{\rm efficiency}=1.93\times4.8\times0.607\times0.580\approx3.25."))
E.append(("S", "- **Detection statistics (4.8×):**",
          "the ideal requirements have the same ratio ($88.5/18.4=4.8$, §C0 subsection 10.3). Of this, ×2.3 is speckle fading with four looks, ×1.8 is finding the peak in both ramps, and ×1.2 is",
          "for the ideal requirements the ratio is 5.1 ($88.5/17.3$, §C0 subsection 10.3). Of this, ×2.3 is speckle fading with four looks, ×1.8 is finding the peak in both ramps, and ×1.3 is"))
E.append(("X", "- **Efficiency (0.60×):** the FMCW model's $\\eta=0.25$ is higher than the ToF model's 0.149, the SPADs' optics × PDE × live fraction in bright sun, which also helps FMCW.",
          "- **Efficiency (0.58×):** the FMCW model's $\\eta=0.25$ is higher than the ToF model's 0.145, the SPADs' optics × PDE × live fraction in bright sun, which also helps FMCW."))
E.append(("X", r"- **Per fully covered cell the gap is ≈160×** ($14.6\ \mu{\rm J}/91\ {\rm nJ}$).", r"- **Per fully covered cell the gap is ≈160×** ($14.6\ \mu{\rm J}/93\ {\rm nJ}$)."))
E.append(("S", "- **Direct detection:** from Eq. (96) with a fixed lens,", r"$91\ {\rm nJ}\times(10/200)^2=0.23$ nJ", r"$93\ {\rm nJ}\times(10/200)^2=0.23$ nJ"))

# =============================================================== §C7b subsection 2 (h) and the new (i)
E.append(("S", "- **More power per channel:** nothing, or worse.",
          "because 17 W more dead-time light outweighs the saving in receivers.",
          "because 17 W more dead-time light outweighs the saving in receivers, unless the transmitter is gated (item (i))."))
E.append(("S", "- **Against ToF, FMCW's photon handicap shrinks with range.**",
          r"$91\ {\rm nJ}\times(300/200)^2\times10^{7}=2.0$ W of useful light at 300 m with a fixed 25 mm lens. The FMCW-to-ToF photon ratio therefore falls from $0.30/0.091=3.3$ at 200 m to $4.5/2.0=2.2$ at 300 m,",
          r"$93\ {\rm nJ}\times(300/200)^2\times10^{7}=2.1$ W of useful light at 300 m with a fixed 25 mm lens. The FMCW-to-ToF photon ratio therefore falls from $0.30/0.093=3.2$ at 200 m to $4.5/2.1=2.1$ at 300 m,"))
E.append(("X", "**Summary of the dwell.**",
r"""**(i) What the 1,550 nm eye-safety allowance buys: range and brighter channels, not fewer watts per point.** Class 1 eye safety caps how much light a lidar may emit, and at 1,550 nm the cap is far higher than at 905/940 nm (§C4c). The allowance does not lower the energy a point needs, which subsection 1 derives from collection and detection statistics; it raises the ceiling that energy must stay under.
- **The ceilings** [E; §C4c, for the same 120° × 25° field scanned at 10 Hz and evaluated 100 mm from the sensor]:
  - *1,550 nm:* the cornea limits the time-averaged irradiance to 1 kW m⁻², so a scanned CW beam may emit ≈9.1 W. What counts is the average power that reaches the eye over the exposure time. It is set by how often and how long the beam crosses the pupil, i.e. by the field and the scan, not by the chirp.
  - *905/940 nm:* the retina limits each pulse to ≈80–230 nJ and the time average to ≈0.24–0.28 W for a small, collimated source. This is why SPAD ToF splits each point into ≈10 weak shots. Production units still emit watts, because a VCSEL array behind a line-forming lens is an extended source, whose apparent size raises the limits by the factor $C_6$ (up to ≈67×).
- **How much of it the two designs use** [E]:
  - FMCW emits $\dot NE_{\rm opt}$: 3.0 W at 10 Mpts/s and 200 m, a third of the 9.1 W, and 7.6 W at 25 Mpts/s, 83% of it. At 300 m it needs 4.6 and 11.4 W; the latter exceeds the allowance for this field.
  - SPAD ToF emits 0.93 W at 10 Mpts/s and 2.3 W at 25 Mpts/s, 9.3 nJ per shot and point. That is within the per-pulse limits but above the small-source average, so it relies on the extended-source relief that production units use.
  - At the 200 m operating point of this section neither design is limited by eye safety, so the per-watt comparison stands.
- **What the headroom buys FMCW:**
  1. *Range at moderate point rates.* At 10 Mpts/s the allowance covers 0.91 µJ per point, 3× the 200 m need. With an aperture matched to each range the energy grows only as $R$ (subsection 1(f)), so that is ≈600 m of eye-safe reach on a 10% target. SPAD ToF, whose energy grows as $R^2$, would need 0.84 µJ per point at 600 m and 8.4 W at 10 Mpts/s, far beyond its average-power limits. At 25 Mpts/s the headroom shrinks to 0.36 µJ per point, i.e. ≈240 m.
  2. *Brighter channels.* The limit applies to the sensor's total emission, not to each beam, so channels may carry 100 mW or more. Item (h) shows that this pays only if the transmitter is dark while its echo would be discarded: the dead-time light otherwise grows with $P_{\rm ch}$. A transmit SOA gated off during the last $\tau$ of each ramp, whose echo would arrive in the next ramp's discarded window, removes that term [E]. At 10 Mpts/s and 300 m the sensor then falls from ≈68 W to ≈59 W at the same 35 mW per channel, and to ≈53 W at 100 mW per channel (85 channels, 340 receivers, ≥2.5 GS/s converters). As $P_{\rm ch}\to\infty$ it approaches ≈49 W: the useful light, the range samples and the overhead.
  3. *One dwell per point.* FMCW need not split a point into many weak shots, so it has no multi-shot accumulation to manage.
- **What it does not buy: fewer watts per point.** At 300 m and 10 Mpts/s the gated floor of ≈49 W is still ≈3.5× the ≈14 W of the SPAD ToF sensor at the same range and rate. The allowance helps FMCW most where ToF meets its own eye-safety limits, at long range and high point rate, which is FMCW's truck niche; it does not close the per-watt gap at 200 m.

*How the numbers are derived* [E]:
- **Use of the allowance:** $\dot NE_{\rm opt}$ with the §C7a energies, e.g. $2.5\times10^{7}\times0.303\ \mu{\rm J}=7.6$ W; at 300 m, $0.45$ µJ gives $2.5\times10^{7}\times0.455\ \mu{\rm J}=11.4$ W against 9.1 W.
- **Reach:** $9.1\ {\rm W}/10^{7}\ {\rm s^{-1}}=0.91$ µJ per point, and $200\ {\rm m}\times0.91/0.30=600$ m with $E_{\rm opt}\propto R$. For ToF, $93\ {\rm nJ}\times(600/200)^2=0.84$ µJ.
- **Gated transmitter:** Eq. (117) without its dead-time term. At 100 mW, $10^{7}\times0.45\ \mu{\rm J}/0.15=30$ W of useful light, 85 channels × 4 receivers × 10 mW = 3.4 W of analog power, $10^{7}\times4\times(10{,}000+5\times9\times10^{7}\times2.25\times10^{-6})\times37\ {\rm pJ}=16.3$ W of ADC and FFT, and 3 W of overhead: 52.7 W. The floor is $30+14.8+1.6+3=49.4$ W.
- **ToF at 300 m:** $3\ {\rm W}+10^{7}\times(93\ {\rm nJ}\times2.25/0.20+70\ {\rm nJ})=14.2$ W.

**Summary of the dwell.**"""))

# =============================================================== §C7b subsection 3
E.append(("S", "This subsection turns the dwell of subsection 2 into the number of parallel coherent channels",
          "against ≈25 mW per ToF channel.", "against ≈26 mW per ToF channel."))
E.append(("S", "- **Power per ToF channel.** At the §C7a central values", "and ≈0.45 µJ of laser electrical energy per ToF point",
          "and ≈0.47 µJ of laser electrical energy per ToF point"))
E.append(("X", r"  - receive: $15\times10^{6}\times71\ {\rm nJ}=1.07$ W, i.e. $1.07\ {\rm W}/312=3.4$ mW per macro-pixel;",
          r"  - receive: $15\times10^{6}\times70\ {\rm nJ}=1.05$ W, i.e. $1.05\ {\rm W}/312=3.4$ mW per macro-pixel;"))
E.append(("X", r"  - laser: $15\times10^{6}\times0.45\ \mu{\rm J}=6.8$ W, i.e. ≈22 mW per macro-pixel.",
          r"  - laser: $15\times10^{6}\times0.47\ \mu{\rm J}=7.0$ W, i.e. ≈22 mW per macro-pixel."))
E.append(("X", "- **So the per-channel electrical power is ≈376 mW for FMCW against ≈25 mW for ToF, ≈15× more.** The FMCW channel is also far larger and costlier.",
          "- **So the per-channel electrical power is ≈376 mW for FMCW against ≈26 mW for ToF, ≈15× more.** The FMCW channel is also far larger and costlier."))
E.append(("S", "  - At 15 Mpts/s that is $15\\times10^{6}\\times2.23\\times10^{-6}=33.4$ W of receiver electronics",
          "about 3.5 times a whole 520-line ToF unit (≈9.6 W in the §C7a model).",
          "about 3.4 times a whole 520-line ToF unit (≈9.7 W in the §C7a model)."))

# =============================================================== §C10
E.append(("S", "- **Speckle and polarization favour ToF.** Single-mode detection fades", "and ≈18 in bright sun", "and ≈17 in bright sun"))
