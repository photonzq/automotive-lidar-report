"""Round 2, agent R2A_C0: build edits/round2/R2A_C0.json (edits inside §C0 only) and check every "old" against the
live report (exactly one occurrence, no overlaps). The numbers in the "new" texts come from r2a_c0_numbers.py and
from the tables files of link_budget_scaling.py and fmcw_tof_system_budget.py. Writes only the JSON file.

Usage: python r2a_c0_build_edits.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPORT = HERE.parents[4] / "automotive_perception_report_2026-09-27.md"
OUT = HERE.parents[2] / "edits" / "round2" / "R2A_C0.json"
LABEL = "R2A_C0"

E = []  # (finding, old, new, why)


def ed(finding, old, new, why):
    E.append((finding, old, new, why))


# ------------------------------------------------------------------ subsection 2: FMCW dwell (decision 1)
ed("decision 1 (FMCW dwell)",
   r"""$T_{\rm dwell}$: the time spent per point (s), $2T$ for one up- and one down-ramp, and $N_{\rm ch}$ the number of parallel coherent channels. Only the last $T-\tau$ of each ramp yields a clean beat, because the echo arrives $\tau$ after the ramp starts; §C7b subsection 2(g) writes the same dwell as $T_{\rm dwell}=2(T_u+\tau)$, with $T_u=T-\tau$ the useful part of each ramp;""",
   r"""$T_{\rm dwell}$: the time spent per point (s), and $N_{\rm ch}$ the number of parallel coherent channels. Only the last $T_u=T-\tau$ of each ramp, its useful part, yields a clean beat, because the echo arrives $\tau$ after the ramp starts. A point therefore integrates for $T_{\rm int}=2T_u$ over its up- and down-ramp, and its dwell is $T_{\rm dwell}=T_{\rm int}+2\tau=2T$. This is the dwell of §C7b subsection 2(b), Eq. (107), written there as $E_{\rm pt}/P_{\rm ch}+2\tau$, with $E_{\rm pt}$ the optical energy a point needs and $P_{\rm ch}$ the channel's constant optical power; the report uses it throughout. The §C7a model integrates $T_{\rm int}=2\times5$ µs, so at its 200 m design range ($\tau=1.33$ µs) its dwell is $T_{\rm dwell}=10+2\times1.33=12.67$ µs;""",
   "One dwell definition report-wide, T_dwell = T_int + 2 tau (Eq. (107)), with the 12.67 µs of the §C7a model.")
ed("decision 1 (FMCW dwell)",
   r"""| Dwell and point rate | One point per channel per up–down ramp pair, $T_{\rm dwell}=2T$, so $\dot N\approx N_{\rm ch}/T_{\rm dwell}$ | 20 µs dwell → 50 kpts/s per channel | §C7, §C7a |""",
   r"""| Dwell and point rate | One point per channel per up–down ramp pair, $T_{\rm dwell}=T_{\rm int}+2\tau=2T$, so $\dot N\approx N_{\rm ch}/T_{\rm dwell}$ | 20 µs dwell → 50 kpts/s per channel; the §C7a model's 12.67 µs → 79 kpts/s | §C7, §C7a, §C7b |""",
   "Table row states the report-wide dwell and the model's 12.67 µs (1/12.67 µs = 79 kpts/s).")
ed("decision 1 (FMCW dwell)",
   r"""the §C7a model and §C0 subsection 10.3 use 5 µs ramps:""",
   r"""the §C7a model and §C0 subsection 10.3 integrate 5 µs in each ramp ($T_{\rm int}=10$ µs):""",
   "In the model 5 µs is the integration window of each ramp, not the ramp.")
ed("decision 1 (FMCW dwell)",
   r"""**Dwell:** $T_{\rm dwell}=2T=2\times10\ \mu{\rm s}=20\ \mu{\rm s}$, so one channel delivers $1/(20\times10^{-6}\ {\rm s})=5\times10^4$ pts/s.""",
   r"""**Dwell:** $T_{\rm dwell}=2T=2\times10\ \mu{\rm s}=20\ \mu{\rm s}$, of which $T_{\rm int}=2\times(10-1.33)\ \mu{\rm s}=17.3\ \mu{\rm s}$ integrates signal from 200 m, so one channel delivers $1/(20\times10^{-6}\ {\rm s})=5\times10^4$ pts/s. The §C7a model's dwell, $T_{\rm dwell}=10+2\times1.33=12.67$ µs, gives $1/(12.67\times10^{-6}\ {\rm s})=7.9\times10^4$ pts/s per channel.""",
   "Derivation of the dwell numbers on the T_int + 2 tau definition.")

# ------------------------------------------------------------------ subsection 5: macro-pixel (decision 2)
ed("decision 2 (0.05° × 0.05° macro-pixel)",
   r"""With a 20 nm filter, $\rho_{\rm scene}=0.9$, a 0.1° × 0.05° pixel ($\Omega_{\rm pix}=1.52\times10^{-6}$ sr), a 25 mm aperture ($A_{\rm rx}=4.91\times10^{-4}$ m²), $\eta_{\rm opt}=0.5$ and PDE 0.3, $r_{\rm bg}=3.4\times10^{18}\times20\times(0.9/\pi)\times1.52\times10^{-6}\times4.91\times10^{-4}\times0.5\times0.3\approx2.2\times10^9$ counts/s.""",
   r"""With a 20 nm filter, $\rho_{\rm scene}=0.9$, a 0.05° × 0.05° macro-pixel ($0.05^\circ=8.73\times10^{-4}$ rad, so $\Omega_{\rm pix}=(8.73\times10^{-4})^2=7.62\times10^{-7}$ sr; the 2,400 × 520 grid of Sony's IMX479 over 120° × 26°, §C5a), a 25 mm aperture ($A_{\rm rx}=4.91\times10^{-4}$ m²), $\eta_{\rm opt}=0.5$ and PDE 0.3, $r_{\rm bg}=3.4\times10^{18}\times20\times(0.9/\pi)\times7.62\times10^{-7}\times4.91\times10^{-4}\times0.5\times0.3\approx1.1\times10^9$ counts/s.""",
   "Macro-pixel field 0.05° × 0.05° (IMX479 grid) halves the per-pixel background: 1.1e9 counts/s.")

# ------------------------------------------------------------------ subsection 7
ed("decision 2/3 (background and n_req)",
   r"""§C0 subsection 10.3 uses 2,000 bins of 1 ns and the bright-sun $b=2.87$ of the §C7a model, which raises the daylight requirement from ≈13 to ≈17 counts:""",
   r"""§C0 subsection 10.3 uses 2,000 bins of 1 ns and the bright-sun $b=1.62$ of the §C7a model, which raises the daylight requirement from ≈13 to ≈15 counts:""",
   "Pointer to 10.3 follows the new background (b = 1.62, ideal 14.98 counts); the b = 1 worked cases are model independent and kept.")

# ------------------------------------------------------------------ subsection 10, main results
ed("decision 3/6 (n_req, eta) and 1 (ungated)",
   r"""FMCW needs about 2.5 times the energy per point of SPAD ToF, whatever the range. Against the fixed 25 mm ToF lens of §C7a the factor is 3.1 at 200 m (10.5), the ≈3.2× used in §C7a, §C7b and §C10.""",
   r"""FMCW needs about 3.2 times the energy per point of SPAD ToF, whatever the range. Against the fixed 25 mm ToF lens of §C7a the factor is 4.1 at 200 m (10.5), close to the ≈4.2× of §C7a ($0.303/0.072$ µJ, for a 20 mm FMCW beam and without clear-air loss). An ungated FMCW transmitter also emits during the two round trips of each point, 1.27 times its useful light at 200 m (10.1), so in emitted light §C7a's ratio is 5.3× ($0.384/0.072$).""",
   "Eq. (45) gives 3.2 with n_req 21.7 and eta 0.164; the fixed-lens ratio is 303/74.2 = 4.08; ungated emission adds 12.67/10.")
ed("decision 3/6 (n_req, eta)",
   r"""or sixteen times the 96 nJ of the 25 mm ToF design. The best FMCW design already needs 3.2 times ToF's energy here, not 2.5 times, because the ToF lens (25 mm) is larger than FMCW's 22 mm optimum.""",
   r"""or about twenty times the 74 nJ of the 25 mm ToF design ($1{,}522/74=20.6$). The best FMCW design already needs 4.1 times ToF's energy here ($303/74$), not 3.2 times, because the ToF lens (25 mm) is larger than FMCW's 22 mm optimum.""",
   "The 25 mm SPAD design needs 74 nJ at 200 m (tables file), so the multiples become 20.6 and 4.1.")

# ------------------------------------------------------------------ 10.1 symbols
ed("decision 1 (ungated emission); decision 6 (eta)",
   r"""- $E_{\rm pt}$: optical energy transmitted toward one point, summed over all shots of a point (ToF) or over the up–down chirp pair (FMCW).""",
   r"""- $E_{\rm pt}$: optical energy transmitted toward one point, summed over all shots of a point (ToF) or over the integration time $T_{\rm int}$ of the up–down chirp pair (FMCW; subsection 2), i.e. $E_{\rm pt}=P_{\rm ch}T_{\rm int}$ for a channel of constant optical power $P_{\rm ch}$. An ungated FMCW transmitter also emits during the two round trips, $E_{\rm pt}T_{\rm dwell}/T_{\rm int}$ in all: for the §C7a central case at 200 m, 30 mW for $T_{\rm dwell}=12.67$ µs, i.e. $0.30\ \mu{\rm J}\times12.67/10=0.38$ µJ. The link budget counts only $E_{\rm pt}$, the light that falls within the integration windows.""",
   "Defines the FMCW energy per point on the dwell convention and states the ungated emission.")
ed("decision 6 (eta convention)",
   r"""- $\eta$: end-to-end efficiency from photons at the aperture to signal photoelectrons: optics × detector, and for coherent detection also × mixing.""",
   r"""- $\eta$: end-to-end efficiency from photons at the aperture to signal photoelectrons: optics × detector, and for coherent detection also × mixing. For a SPAD in sunlight the detector term includes the dead-time live fraction: $\eta=0.5\times0.37\times0.885=0.164$ in the bright sun of 10.3.""",
   "States the ToF value of eta on the report-wide convention.")

# ------------------------------------------------------------------ 10.3 detection statistics
ed("decision 2/3 (background and n_req)",
   r"""The 2,000 bins and the 2.87 background counts per bin of the §C7a model raise this to 17.3 here.""",
   r"""The 2,000 bins and the 1.62 background counts per bin of the §C7a model raise this to 15.0 here.""",
   "New background per bin and ideal requirement.")
ed("decision 2 (background)",
   r"""- **Bright sun, $b=2.87$:** $P(N\ge14\mid2.87)=2.0\times10^{-6}$ fails and $P(N\ge15\mid2.87)=3.8\times10^{-7}$ passes, so $n_{\rm th}=15$.""",
   r"""- **Bright sun, $b=1.62$:** $P(N\ge11\mid1.62)=1.15\times10^{-6}$ fails and $P(N\ge12\mid1.62)=1.54\times10^{-7}$ passes, so $n_{\rm th}=12$.""",
   "Poisson tails at b = 1.62 against p = 5e-7: threshold 12.")
ed("decision 2 (background)",
   r"""- **Where $b=2.87$ comes from** [E].""",
   r"""- **Where $b=1.62$ comes from** [E].""",
   "Heading of the derivation follows the new value.")
ed("decision 2 (0.05° × 0.05° macro-pixel)",
   r"""Eq. (81) gives $r_{\rm bg}=5.93\times10^{8}$ counts per second per macro-pixel for a fully sunlit scene of reflectance 0.9, at 940 nm behind a 10 nm filter and at PDE 0.3. The same SPADs count background and signal, so at the model's PDE of 0.37 the rate is $5.93\times10^{8}\times0.37/0.3=7.31\times10^{8}$ s⁻¹.""",
   r"""Eq. (81) gives $r_{\rm bg}=2.97\times10^{8}$ counts per second per macro-pixel for a fully sunlit scene of reflectance 0.9, at 940 nm behind a 10 nm filter and at PDE 0.3. The macro-pixel sees 0.05° × 0.05° ($\Omega_{\rm pix}=7.62\times10^{-7}$ sr, the IMX479 grid of subsection 5), and §C6(d) takes $E_\odot\approx0.39$ W m⁻² nm⁻¹ at 940 nm, so with $E_{\rm ph}=2.11\times10^{-19}$ J and the 25 mm aperture Eq. (81) reads $(0.39/2.11\times10^{-19})\times10\times(0.9/\pi)\times7.62\times10^{-7}\times4.91\times10^{-4}\times0.5\times0.3=2.97\times10^{8}$ s⁻¹. The same SPADs count background and signal, so at the model's PDE of 0.37 the rate is $2.97\times10^{8}\times0.37/0.3=3.66\times10^{8}$ s⁻¹.""",
   "Background of the 0.05° × 0.05° macro-pixel, with the Eq. (81) substitution shown.")
ed("decision 2 (background)",
   r"""The central case takes half of that, $r_{\rm bg}=3.66\times10^{8}$ s⁻¹: a sunlit scene of reflectance ≈0.45""",
   r"""The central case takes half of that, $r_{\rm bg}=1.83\times10^{8}$ s⁻¹: a sunlit scene of reflectance ≈0.45""",
   "Central case is half of 3.66e8.")
ed("decision 2 (dead and live fractions)",
   r"""Each of the macro-pixel's nine SPADs (a 3×3 group, §C5a) counts $r=3.66\times10^{8}/9=4.06\times10^{7}$ s⁻¹, so $r\tau_d=0.244$ for $\tau_d=6$ ns, the live fraction is $e^{-0.244}=0.784$ and $f_{\rm dead}=0.216$. A non-paralyzable SPAD would instead be dead a fraction $0.244/1.244=0.196$ of the time (the other form of Eq. (82)). That would raise $b$ to 2.94 and the threshold to 16 counts, so an ideal counter would need 18.4 signal counts rather than 17.3, and the energy per point would change by a few per cent.""",
   r"""Each of the macro-pixel's nine SPADs (a 3×3 group, §C5a) counts $r=1.83\times10^{8}/9=2.03\times10^{7}$ s⁻¹, so $r\tau_d=0.122$ for $\tau_d=6$ ns, the live fraction is $e^{-0.122}=0.885$ and $f_{\rm dead}=0.115$. A non-paralyzable SPAD would instead be dead a fraction $0.122/1.122=0.109$ of the time (the other form of Eq. (82)), i.e. live 0.891. That would raise $b$ only to $1.83\times10^{8}\times10^{-9}\times10\times0.891=1.63$ and leave the threshold at 12 counts, so an ideal counter would need 14.97 signal counts rather than 14.98. Its larger live fraction would lower the energy per point by under 1% ($0.885/0.891=0.993$).""",
   "Dead and live fractions at r = 2.03e7 /s; the paralyzable choice now matters by under 1 %, not a few per cent.")
ed("decision 2 (counts per bin)",
   r"""$b=r_{\rm bg}\,\Delta t_{\rm bin}\,N_{\rm shots}\,(1-f_{\rm dead})=3.66\times10^{8}\times10^{-9}\times10\times0.784=2.87$.""",
   r"""$b=r_{\rm bg}\,\Delta t_{\rm bin}\,N_{\rm shots}\,(1-f_{\rm dead})=1.83\times10^{8}\times10^{-9}\times10\times0.885=1.62$.""",
   "Counts per 1 ns bin over 10 shots.")
ed("decision 2/3 (events per point)",
   r"""Over those 20.8 µs the same rate gives $3.66\times10^{8}\times20.8\times10^{-6}\times0.784\approx5{,}960$ background events, the event count of the §C7a electronics budget.""",
   r"""Over those 20.8 µs the same rate gives $1.83\times10^{8}\times20.8\times10^{-6}\times0.885\approx3{,}370$ background events; with the 21.7 signal counts of 10.4 that is ≈3,390 events per point, the event count of the §C7a electronics budget.""",
   "Events per point over the 20.8 µs listen.")
ed("decision 6 (eta)",
   r"""only the live fraction 0.784 of the echo can be counted, so the §C7a model multiplies the SPAD's signal efficiency by it: optics transmission 0.5 × PDE 0.37 × live fraction 0.784, i.e. $0.5\times0.37\times0.784=0.145$.""",
   r"""only the live fraction 0.885 of the echo can be counted, so the §C7a model multiplies the SPAD's signal efficiency by it: optics transmission 0.5 × PDE 0.37 × live fraction 0.885, i.e. $0.5\times0.37\times0.885=0.164$.""",
   "Signal efficiency 0.164.")
ed("decision 1 (FMCW dwell)",
   r"""Target and beam do not change within the ≈10 µs of the two ramps, so both see the same speckle""",
   r"""Target and beam do not change within the 12.67 µs dwell of the two ramps (10 µs of integration plus the two 1.33 µs round trips at 200 m, subsection 2), so both see the same speckle""",
   "Time span of the two ramps on the report-wide dwell.")
ed("decision 1 (FMCW dwell)",
   r"""For the §C7a chirp (1 GHz over 5 µs up and 5 µs down, so 200 kHz bins; 300 m; ±70 m/s):""",
   r"""For the §C7a chirp (1 GHz swept over the 5 µs useful window of each ramp, up and down, so 200 kHz bins; 300 m; ±70 m/s):""",
   "The 5 µs are the useful windows.")
ed("decision 1 (FMCW dwell)",
   r"""where $T_u=5$ µs is one ramp,""",
   r"""where $T_u=5$ µs is the useful window of one ramp,""",
   "Same clarification for T_u.")
ed("decision 2/3 (detection table)",
   r"""| Photon counting, bright sun ($b=2.87$, $n_{\rm th}=15$) | 11.8 | 17.3 | 1.00 | 1.00 |""",
   r"""| Photon counting, bright sun ($b=1.62$, $n_{\rm th}=12$) | 10.0 | 15.0 | 1.00 | 1.00 |""",
   "Ideal counter at b = 1.62: 10.0 (P_D 0.5) and 15.0 (P_D 0.9); P_D(25) = 0.999.")
ed("decision 2/3 (worked check)",
   r"""- **Worked check, bright sun:** $s=17.26$ puts the total mean at $s+b=17.26+2.87=20.13$, and a Poisson count of mean 20.13 reaches 15 with probability 0.90.""",
   r"""- **Worked check, bright sun:** $s=14.98$ puts the total mean at $s+b=14.98+1.62=16.60$, and a Poisson count of mean 16.60 reaches 12 with probability 0.90.""",
   "Worked check at the new threshold.")
ed("decision 3 (reading of Figure C0.10b)",
   r"""The dotted verticals are the photoelectron counts used in the §C7a model: 25 for ToF and 120 for FMCW (four looks).""",
   r"""The dotted verticals sit at 25 and 120 photoelectrons, the two columns of the table above. The FMCW model uses 120 (four looks); the ToF model uses 21.7 (10.4), just left of the line marked "ToF model".""",
   "Caption stays true for the figure as drawn (its ToF marker is at 25) and gives the model's 21.7.")
ed("decision 3 (n_req margin)",
   r"""- **ToF:** the model's 25 counts are 1.45× the 17.3 that an ideal counter needs in bright sun. The dead time is not part of this margin, because it is counted in the SPAD's efficiency (the live fraction above, §C7a(a)). The margin covers a return spread over about two bins, which needs 22.5 counts summed over both (×1.30), and pile-up distortion (§C6). In the model's high case, a fully sunlit scene of reflectance 0.9 ($b=4.49$, $n_{\rm th}=19$), the ideal counter needs 20.3.""",
   r"""- **ToF:** the model's 21.7 counts keep a ×1.45 implementation margin over the 15.0 that an ideal counter needs in bright sun ($n_{\rm req}=1.45\times14.98=21.7$). The dead time is not part of this margin, because it is counted in the SPAD's efficiency (the live fraction above, §C7a(a)). The margin covers a return spread over about two bins, which needs 18.1 counts summed over both (×1.21: the two bins hold $2b=3.24$ background counts, which raises the threshold to 16), and leaves ×1.20 for pile-up distortion (§C6) and other implementation losses. In the model's high case, a fully sunlit scene of reflectance 0.9 ($r_{\rm bg}=3.66\times10^{8}$ s⁻¹, live fraction 0.784, $b=2.87$, $n_{\rm th}=15$), the ideal counter needs 17.3.""",
   "n_req = 1.45 x 14.98 = 21.7; two-bin case 18.05 (x1.21); high case b = 2.87, ideal 17.26.")
ed("decision 2/3 (FMCW against the counter)",
   r"""- **Where FMCW's extra photons go** (four looks, 88.5 against the counter's 17.3 in bright sun):""",
   r"""- **Where FMCW's extra photons go** (four looks, 88.5 against the counter's 15.0 in bright sun):""",
   "Counter requirement 15.0.")
ed("decision 2/3 (FMCW against the counter)",
   r"""*the noise floor, ×1.3:* even a steady target in one fully searched ramp needs 21.9, more than the counter in bright sun. Each of the 2,450 bins carries one photoelectron of shot noise, and the threshold must clear the largest of them; the counter's threshold only has to clear the Poisson tail of 2.87 counts;""",
   r"""*the noise floor, ×1.5:* even a steady target in one fully searched ramp needs 21.9, 1.46 times the counter in bright sun ($21.9/15.0$). Each of the 2,450 bins carries one photoelectron of shot noise, and the threshold must clear the largest of them; the counter's threshold only has to clear the Poisson tail of 1.62 counts;""",
   "Noise-floor factor 21.9/14.98 = 1.46.")
ed("decision 2/3 (search table)",
   r"""A joint search, neighbour checks or a tracking window lower the requirement by 7–33%, for both receivers:""",
   r"""A joint search, neighbour checks or a tracking window lower the requirement by 8–33%, for both receivers:""",
   "ToF savings are 8 % and 24 %, FMCW 8–33 %.")
ed("decision 2/3 (search table)",
   r"""| Full search (the rule above) | 88.5 | 17.3 |""",
   r"""| Full search (the rule above) | 88.5 | 15.0 |""",
   "ToF full search at b = 1.62.")
ed("decision 2/3 (search table)",
   r"""| $10^{-2}$ false points per point, pruned by neighbour checks | 81.6 | 16.1 |""",
   r"""| $10^{-2}$ false points per point, pruned by neighbour checks | 81.6 | 13.8 |""",
   "p = 5e-6: threshold 11, s = 13.79.")
ed("decision 2/3 (search table)",
   r"""| Tracking window of 20 bins per ramp around a predicted return | 59.6 | 13.7 |""",
   r"""| Tracking window of 20 bins per ramp around a predicted return | 59.6 | 11.4 |""",
   "p = 5e-5: threshold 9, s = 11.37.")
ed("decision 2/3 (search table)",
   r"""| Known cell (no search; the ideal bound) | 32.2 | 11.3 |""",
   r"""| Known cell (no search; the ideal bound) | 32.2 | 10.2 |""",
   "p = 1e-3: threshold 8, s = 10.15.")
ed("decision 2/3 (search table)",
   r"""well above the counter's 11.3.""",
   r"""well above the counter's 10.2.""",
   "Known-cell counter value.")
ed("decision 3 (comparison)",
   r"""Under one rule, a SPAD ToF receiver in bright sun needs 17–25 counts per point, and an FMCW receiver 88–120 photoelectrons with four looks (259 with one). The coherent receiver's freedom from background does not lower its photon requirement: even a steady coherent target needs more (39.1) than an ideal counter in bright sun (17.3), and speckle fading adds to that. 10.4 turns the model's counts, 25 for SPAD ToF and 120 for FMCW (30 in each of four looks), into detection levels.""",
   r"""Under one rule, a SPAD ToF receiver in bright sun needs 15–22 counts per point (the ideal 15.0 and the model's 21.7), and an FMCW receiver 88–120 photoelectrons with four looks (259 with one). The coherent receiver's freedom from background does not lower its photon requirement: even a steady coherent target needs more (39.1) than an ideal counter in bright sun (15.0), and speckle fading adds to that. 10.4 turns the model's counts, 21.7 for SPAD ToF and 120 for FMCW (30 in each of four looks), into detection levels.""",
   "ToF counts 15.0 ideal and 21.7 model.")

# ------------------------------------------------------------------ 10.4 detection levels
ed("decision 3/6 (detection level)",
   r"""| SPAD dToF, bright sun | 940 nm | 25 | 0.145 | 0.1 µJ (e.g. ≈10 shots of 10 nJ) | $3.6\times10^{-10}$ | 94.4 dB |""",
   r"""| SPAD dToF, bright sun | 940 nm | 21.7 | 0.164 | 0.1 µJ (e.g. ≈10 shots of 10 nJ) | $2.8\times10^{-10}$ | 95.5 dB |""",
   "L_det = 21.7 x 2.11e-19 / (0.164 x 1e-7) = 2.79e-10, 95.5 dB (tables: 2.800e-10).")
ed("decision 1 (FMCW dwell)",
   r"""0.3 µJ (30 mW × 10 µs)""",
   r"""0.3 µJ (30 mW × 10 µs of integration)""",
   "The 10 µs is the integration time, not the dwell.")
ed("decision 3/6 (inputs)",
   r"""SPAD: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction 0.784 (6 ns dead time, modelled as paralyzable, 10.3);""",
   r"""SPAD: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction 0.885 (6 ns dead time, modelled as paralyzable, 10.3), i.e. $\eta=0.164$, and $n_{\rm req}=21.7$, the ×1.45 margin over the ideal 15.0 counts (10.3);""",
   "Inputs of the SPAD row.")
ed("decision 3/6 (worked SPAD level)",
   r"""$25\times2.11\times10^{-19}/(0.145\times10^{-7})=3.64\times10^{-10}$, and $-10\log_{10}(3.64\times10^{-10})=94.4$ dB.""",
   r"""$21.7\times2.11\times10^{-19}/(0.164\times10^{-7})=2.79\times10^{-10}$, and $-10\log_{10}(2.79\times10^{-10})=95.5$ dB.""",
   "Worked detection level.")
ed("decision 3/6 (reading of Figure C0.10a)",
   r"""SPAD case, $D=25$ mm: $0.0125\times\sqrt{0.1/3.64\times10^{-10}}=207$ m, or 204 m with clear air. The 10 and 50 mm lenses reach 82 and 400 m.""",
   r"""SPAD case, $D=25$ mm: $0.0125\times\sqrt{0.1/2.79\times10^{-10}}=237$ m, or 232 m with clear air. The 10 and 50 mm lenses reach 94 and 455 m.""",
   "Crossings of the new SPAD level (tables: 94 / 232 / 455 m).")
ed("decision 3/6 (APD against SPAD)",
   r"""Its per-point need $n_{\rm req}E_{\rm ph}/\eta$ is 7.8× the SPAD's, but its 20× larger energy leaves a 2.6× margin, i.e. $\sqrt{2.6}=1.6\times$ the range.""",
   r"""Its per-point need $n_{\rm req}E_{\rm ph}/\eta$ is 10.2× the SPAD's (10.5), but its 20× larger energy leaves a $20/10.2=1.96\times$ margin, i.e. $\sqrt{1.96}=1.40\times$ the range.""",
   "APD/SPAD need ratio 10.2; 232 m x 1.40 = 325 m, against 326 m with less clear-air loss at 1,550 nm.")

# ------------------------------------------------------------------ 10.5 range scaling
ed("decision 2/3 (shots per point)",
   r"""the ideal counter of 10.3 needs 14.0, 17.3 and 22.5 counts for 5, 10 and 20 shots ($b=1.43$, 2.87 and 5.73) [E]. The product $\dot N R_{\max}^2$ then shifts by about 25% per factor of two in point rate,""",
   r"""the ideal counter of 10.3 needs 12.2, 15.0 and 18.1 counts for 5, 10 and 20 shots ($b=0.81$, 1.62 and 3.24; thresholds 9, 12 and 16) [E]. The product $\dot N R_{\max}^2$ then shifts by about 21–23% per factor of two in point rate ($15.0/12.2=1.23$ and $18.1/15.0=1.21$),""",
   "Shots-per-point sensitivity at the new background.")
ed("decision 3/6 (Eq. (45))",
   r"""=0.42\times\frac{1}{t^2(0.45)^2}=0.42\times5.9=2.5 . \tag{45}$$""",
   r"""=0.55\times\frac{1}{t^2(0.45)^2}=0.55\times5.9=3.2 . \tag{45}$$""",
   "Eq. (45) rewritten in place with the new first factor; tag kept.")
ed("decision 3 (n_d)",
   r"""and $n_{\rm d}=25$ are their values of $n_{\rm req}$""",
   r"""and $n_{\rm d}=21.7$ are their values of $n_{\rm req}$""",
   "n_req of the SPAD.")
ed("decision 3/6 (first factor of Eq. (45))",
   r"""The first factor is $(30\times1.28\times10^{-19}/0.25)/(25\times2.11\times10^{-19}/0.145)=1.54\times10^{-17}/3.64\times10^{-17}=0.42$.""",
   r"""The first factor is $(30\times1.28\times10^{-19}/0.25)/(21.7\times2.11\times10^{-19}/0.164)=1.54\times10^{-17}/2.79\times10^{-17}=0.55$.""",
   "First factor 0.55.")
ed("decision 3/6 (ratio with clear air)",
   r"""With clear-air loss the ratio is 2.4–2.5 (2.47 at 100 m, 2.39 at 500 m),""",
   r"""With clear-air loss the ratio is 3.1–3.2 (3.21 at 100 m, 3.11 at 500 m),""",
   "Tables: SPAD with the same D_opt, 3.21 / 3.18 / 3.16 / 3.11.")
ed("decision 3/6 (fixed 25 mm SPAD)",
   r"""6.3× at 100 m, 3.1× at 200 m, 2.1× at 300 m and 1.2× at 500 m.""",
   r"""8.2× at 100 m, 4.1× at 200 m, 2.7× at 300 m and 1.6× at 500 m (150, 303, 458 and 778 nJ against 18.2, 74.2, 169.7 and 487.7 nJ, with clear air).""",
   "Tables: ratio best-D FMCW / SPAD 25 mm, 8.24 / 4.08 / 2.70 / 1.59.")
ed("decision 3/6 (APD against SPAD)",
   r"""$(890\times1.28\times10^{-19}/0.40)/(25\times2.11\times10^{-19}/0.145)=7.8$. That is almost eight times the energy per point at every range,""",
   r"""$(890\times1.28\times10^{-19}/0.40)/(21.7\times2.11\times10^{-19}/0.164)=2.85\times10^{-16}/2.79\times10^{-17}=10.2$. That is about ten times the energy per point at every range,""",
   "APD/SPAD energy ratio 10.2.")
ed("decision 3/6 (reading of Figure C0.10c)",
   r"""The linear APD with a 25 mm lens runs just below the 10 mm SPAD, because with the same lens it needs 7.8 times the SPAD's energy (10.5), slightly more than the factor $2.5^2=6.25$ between the 10 and 25 mm SPAD lenses.""",
   r"""The linear APD with a 25 mm lens runs below the 10 mm SPAD, because with the same lens it needs 10.2 times the SPAD's energy (10.5), more than the factor $2.5^2=6.25$ between the 10 and 25 mm SPAD lenses; at equal energy it reaches $\sqrt{6.25/10.2}=0.78$ of the 10 mm SPAD's range.""",
   "Reading of panel (a) with the ratio 10.2.")
ed("decision 3/6 (reading of Figure C0.10c)",
   r"""the FMCW energy gap closes as $1/R$ (10.5), from 3.1× at 200 m to 1.2× at 500 m, so the two lines cross at about $500\times1.2=600$ m, near 1 µJ per point.""",
   r"""the FMCW energy gap closes as $1/R$ (10.5), from 4.1× at 200 m to 1.6× at 500 m, so the two lines cross near 780 m, at about 1.2 µJ per point [E: the $1/R$ law alone gives $500\times1.59\approx800$ m; clear air, which costs more at 940 nm than at 1,550 nm, brings the crossing in to ≈780 m].""",
   "Crossing of panel (b) solved with clear air: 780 m at 1.24 µJ.")

# ------------------------------------------------------------------ 10.6 designs
ed("decision 3/6 (10.6 designs)",
   r"""needs 96 nJ per point: the 0.1 µJ of 10.4, which reaches 204 m, scaled by $(200/204)^2=0.96$. Without the 0.15 dB of clear-air loss this is the ≈93 nJ of §C7b subsection 1.""",
   r"""needs 74 nJ per point: the 0.1 µJ of 10.4, which reaches 232 m, scaled by $(200/232)^2=0.743$. Without the 0.15 dB of clear-air loss this is the ≈72 nJ of §C7a subsection 2(a) and §C7b subsection 1 ($74.2\ {\rm nJ}/10^{0.15/10}=71.7$ nJ).""",
   "25 mm SPAD design energy 74 nJ (tables: 74.2 nJ).")
ed("decision 1 (ungated emission)",
   r"""needs 303 nJ. This is close to the ≈0.30 µJ of §C7b subsection 1, which uses a 20 mm beam and no atmospheric loss.""",
   r"""needs 303 nJ in its integration windows; ungated, it emits $303\times12.67/10=384$ nJ (10.1). This is close to the ≈0.30 µJ of §C7b subsection 1, which uses a 20 mm beam and no atmospheric loss.""",
   "States the emitted energy of the ungated transmitter.")
ed("decision 3/6 (10.6 table)",
   r"""| SPAD ToF, 940 nm, 25 mm lens | — | 96 nJ (0.32×) |""",
   r"""| SPAD ToF, 940 nm, 25 mm lens | — | 74 nJ (0.24×) |""",
   "74/303 = 0.24.")
ed("decision 3/6 (10.6 fog)",
   r"""The 7 mm design matches ToF to within 2 m, at sixteen times its energy.""",
   r"""The 7 mm design matches ToF to within 2 m, at about twenty times its energy ($1{,}522/74=20.6$).""",
   "1,522/74 = 20.6.")
ed("decision 3/6 (10.6 design)",
   r"""It needs 5.0× the best FMCW energy, i.e. 1.5 µJ per point, sixteen times ToF's 96 nJ.""",
   r"""It needs 5.0× the best FMCW energy, i.e. 1.5 µJ per point, about twenty times ToF's 74 nJ.""",
   "1,522/74 = 20.6.")

# ------------------------------------------------------------------ 10.7 dynamic range
ed("decision 3/6 (photons per shot)",
   r"""- **Photons, ToF.** Per shot the SPAD design emits 9.6 nJ (its 96 nJ over ten shots). The sign at 5 m then returns about $4.4\times10^{8}$ photons, $6.4\times10^{7}$ of them detected, against 2.5 detected photons per shot from the weakest return the design must see [E].""",
   r"""- **Photons, ToF.** Per shot the SPAD design emits 7.4 nJ (its 74 nJ over ten shots), i.e. $7.4\times10^{-9}/2.11\times10^{-19}=3.5\times10^{10}$ photons. The sign at 5 m returns a fraction $\rho_{\rm eq}A_{\rm rx}/(\pi R^2)=1{,}571\times4.91\times10^{-4}/(\pi\times5^2)=9.8\times10^{-3}$ of them to the lens, about $3.4\times10^{8}$ photons, of which $\eta=0.164$, i.e. $5.6\times10^{7}$, are detected. The weakest return the design must see gives $n_{\rm req}/N_{\rm shots}=21.7/10=2.2$ detected photons per shot [E].""",
   "Photon numbers of the 74 nJ design, with the substitution; ratio 2.6e7 = 74 dB as in the table.")
ed("decision 2 (macro-pixel étendue)",
   r"""That mode accepts an étendue of about $\lambda^2$, against $A_{\rm rx}\Omega_{\rm px}=4.9\times10^{-4}\ {\rm m^2}\times(1.75\ {\rm mrad})^2=1.5\times10^{-9}$ m² sr for a 25 mm lens with a 0.1° pixel.""",
   r"""That mode accepts an étendue of about $\lambda^2=2.40\times10^{-12}$ m² sr, against $A_{\rm rx}\Omega_{\rm pix}=4.91\times10^{-4}\ {\rm m^2}\times7.62\times10^{-7}\ {\rm sr}=3.74\times10^{-10}$ m² sr for the 25 mm lens with the model's 0.05° × 0.05° macro-pixel (subsection 5).""",
   "Compares against the model's macro-pixel field.")
ed("decision 2 (macro-pixel étendue)",
   r"""For diffuse glare this suppresses coupling by about $2.4\times10^{-12}/1.5\times10^{-9}$, i.e. −28 dB.""",
   r"""For diffuse glare this suppresses coupling by about $2.40\times10^{-12}/3.74\times10^{-10}=6.4\times10^{-3}$, i.e. −22 dB.""",
   "Suppression with the 0.05° × 0.05° macro-pixel.")

# ------------------------------------------------------------------ 10.8 benchmark
ed("decision 3/6 (Eq. (55) inputs)",
   r"""and $n_{\rm req}=25$ the model's bright-sun count (10.4). The model's own receiver, 0.145 × a 25 mm lens, has $\eta A_{\rm rx}=0.71$ cm².""",
   r"""and $n_{\rm req}=21.7$ the model's bright-sun count (10.4). The model's own receiver, 0.164 × a 25 mm lens, has $\eta A_{\rm rx}=0.164\times4.91\ {\rm cm^2}=0.81$ cm².""",
   "Model receiver eta A = 0.81 cm2.")
ed("decision 3/6 (Sony row)",
   r"""| 0.14 cm² | 12–14 mm lens at optics 0.7–0.5:""",
   r"""| 0.12 cm² | 10.5–12.4 mm lens at optics 0.7–0.5:""",
   "Eq. (55) with n_req 21.7: 1.18e-5 m2; eta 0.136-0.097.")
ed("decision 3/6 (Toshiba row)",
   r"""| 0.32 cm² (0.035 cm² with 9-pixel accumulation) | 20–28 mm at $\eta=$ 0.10–0.05 ✓ |""",
   r"""| 0.28 cm² (0.031 cm² with 9-pixel accumulation) | 19–27 mm at $\eta=$ 0.10–0.05 ✓ |""",
   "Eq. (55) with n_req 21.7: 2.76e-5 m2.")
ed("decision 3/6 (Toyota row)",
   r"""| 0.18 cm² | 15–22 mm at $\eta=$ 0.10–0.05 ✓ |""",
   r"""| 0.16 cm² | 14–20 mm at $\eta=$ 0.10–0.05 ✓ |""",
   "Eq. (55) with n_req 21.7: 1.60e-5 m2.")
ed("decision 3/6 (Sony lens)",
   r"""Eq. (55) then asks for $25\times2.20\times10^{-19}\times\pi\times150^2/(0.1\times2.85\times10^{-7})=1.36\times10^{-5}$ m². With $\eta=$ 0.5–0.7 (optics) × 0.22 (PDE) × 0.784 (live fraction, §C6), that is a lens of 12–14 mm.""",
   r"""Eq. (55) then asks for $21.7\times2.20\times10^{-19}\times\pi\times150^2/(0.1\times2.85\times10^{-7})=1.18\times10^{-5}$ m². With $\eta=$ 0.5–0.7 (optics) × 0.22 (PDE) × 0.885 (live fraction, 10.3), i.e. 0.097–0.136, that is a lens of 10.5–12.4 mm ($D=2\sqrt{A_{\rm rx}/\pi}$ with $A_{\rm rx}=1.18\times10^{-5}\ {\rm m^2}/\eta$).""",
   "Sony lens 10.5-12.4 mm, still about f/1 for 11.5 mm.")
ed("decision 3/6 (Toshiba and Toyota)",
   r"""Their $\eta A_{\rm rx}$ is 2–4× below the model's 0.71 cm², consistent with the lower PDE of 2013–2018 detectors.""",
   r"""Eq. (55) gives $21.7\times2.20\times10^{-19}\times\pi\times200^2/(0.1\times2.17\times10^{-7})=2.76\times10^{-5}$ m² for Toshiba and $21.7\times2.28\times10^{-19}\times\pi\times100^2/(0.09\times1.08\times10^{-7})=1.60\times10^{-5}$ m² for Toyota. Their $\eta A_{\rm rx}$ is 3–5× below the model's 0.81 cm² ($0.81/0.28=2.9$ and $0.81/0.16=5.1$), consistent with the lower PDE of 2013–2018 detectors.""",
   "Substitutions shown; ratios 2.9 and 5.1.")
ed("decision 3/6 (product inputs)",
   r"""the inputs are the model's $n_{\rm req}=25$ and $\eta=0.145$ (a PDE of 37%)""",
   r"""the inputs are the model's $n_{\rm req}=21.7$ and $\eta=0.164$ (a PDE of 37%)""",
   "Model inputs.")
ed("decision 3/6 (Ouster)",
   r"""It needs 70–158 nJ per point, i.e. 0.09–0.21 W average optical power.""",
   r"""It needs 54–122 nJ per point, i.e. 0.07–0.16 W average optical power [E: Eq. (55) solved for the energy, $E_{\rm pt}=21.7\times2.30\times10^{-19}\times\pi\times200^2/(0.1\times0.164\times A_{\rm rx})$, with $A_{\rm rx}=7.07$ cm² (30 mm) to 3.14 cm² (20 mm), times 1.31 Mpts/s].""",
   "Ouster energies with the substitution.")
ed("decision 3/6 (Hesai)",
   r"""At the model's efficiency it needs 74–167 nJ, i.e. 0.11–0.26 W, and proportionally more at a lower PDE.""",
   r"""At the model's efficiency it needs 57–128 nJ, i.e. 0.09–0.20 W at 1.54 Mpts/s, and proportionally more at a lower PDE [E: as for Ouster, with $E_{\rm ph}=2.20\times10^{-19}$ J and $R=210$ m].""",
   "Hesai energies.")
ed("decision 3/6 (benchmark summary)",
   r"""overall receive efficiencies $\eta$ of 0.05–0.12""",
   r"""overall receive efficiencies $\eta$ of 0.05–0.14""",
   "Sony's eta is 0.097-0.136 with the 0.885 live fraction.")
ed("decision 3/6 (benchmark summary)",
   r"""about 0.1–0.3 W average optical power for 865–905 nm photon-counting scanners;""",
   r"""about 0.07–0.2 W average optical power for 865–905 nm photon-counting scanners;""",
   "Ouster 0.07-0.16 W, Hesai 0.09-0.20 W.")

# ------------------------------------------------------------------ skipped
S = []


def sk(finding, kind, location, detail):
    S.append(dict(finding=finding, kind=kind, location=location, detail=detail))


sk("[03_C0_part10] follow-up flag a (model_round2 list)", "cross_section",
   "§C10.3a item 7 (R2E_C10): 'ToF optics 0.5 × PDE 0.35 = 0.175, and FMCW QE 0.8 × 1 dB each way ≈ 0.50, concluding \"about 2–6×\"'",
   "Lies in §C10.3a, outside §C0, so not edited here. On the Round 2 efficiencies the reviewer's numbers become: ToF eta A_rx = 0.164 × 491 mm² = 80.5 mm² (0.5 × 0.37 × 0.885); one FMCW look 0.25 × A_mode = 7.2, 15.9 and 20.5 mm² at 100, 200 and 300 m (20 mm beam, A_mode 28.8, 63.7 and 82.0 mm²), a ratio of 80.5/20.5 = 3.9 to 80.5/7.2 = 11 (about 4–11×); §C7a's four looks reach 4 × 15.9 = 64 mm² at 200 m, 80.5/64 = 1.26× below ToF.")
sk("Figure C0.10b and C0.10a labels", "cross_section",
   "build/figures/link_budget_scaling.py, fig_detection: 'for n_mark in (25, 120)' and the text 'ToF\\nmodel' at 25; fig_loss level label f\"$n_{{\\\\rm req}}={cs['n_req']:.0f}$\"",
   "The detection-statistics figure still draws its 'ToF model' marker at 25 photoelectrons, while the model uses 21.7; Figure C0.10a prints the SPAD level as n_req = 22 (21.7 formatted with .0f). Proposed: n_mark = (21.7, 120), and format the SPAD label with one decimal; then rebuild. After the rebuild the §C0 caption sentence set by edit R2A_C0 (Figure C0.10b) can read: 'The dotted verticals are the photoelectron counts used in the §C7a model: 21.7 for ToF and 120 for FMCW (four looks).'")
sk("decision 4 (sunlight convention), ratio", "needs_decision",
   "round2_spec.md decision 4 and the linking sentence for §C4c/§C6 (R2B_C4-C6)",
   "The spec's 'about 1.5× lower' does not match the model's own irradiance: §C6(d) uses 0.39 W m⁻² nm⁻¹ at 940 nm, the midpoint of the near-point 0.472 and the ±10 nm band average 0.303, so the band average is 0.39/0.303 = 1.29× lower than the model's value (per pixel at PDE 0.37: 3.66e8 against 2.84e8 counts/s, 1.29×). 1.56× is the ratio of the near-point value 0.472 to the band average. §C0 subsection 10.3 therefore states the 0.39 W m⁻² nm⁻¹ input and no ratio; the linking sentence should say ≈1.3× unless the model is meant to use 0.472.")
sk("10.8 Panasonic row", "needs_source",
   "§C0 subsection 10.8 table, Panasonic flash: 'The model gives 0.13–0.53 photons per pixel per pulse at 100 m; the paper says below one beyond 100 m ✓'",
   "The report does not state the lens diameter, reflectance or efficiency behind 0.13–0.53, so it cannot be told whether it uses the model's eta. Left unchanged. If it uses the old eta = 0.145, the range becomes 0.164/0.145 = 1.13 times higher, ≈0.15–0.60, and the conclusion (below one beyond 100 m) holds either way.")

CS = [
    ("§0 executive summary (R2C_C7-C7a)",
     "whose SPADs lose ≈22% of the signal to their 6 ns dead time in bright sun",
     "whose SPADs lose ≈11.5% of the signal to their 6 ns dead time in bright sun (live fraction 0.885, §C0 subsection 10.3)"),
    ("§C3b 'Why the weight is R^2' (R2B_C4-C6)",
     "(0.784 in the bright sun of §C0 subsection 10.3)",
     "(0.885 in the bright sun of §C0 subsection 10.3)"),
    ("§C5a dark counts (R2B_C4-C6)",
     "(≈5,970 in the central case of §C7b subsection 1, built from the rates of §C6(d))",
     "(≈3,370 in the central case of §C7b subsection 1, built from the rates of §C6(d): $1.83\\times10^{8}\\times20.8\\times10^{-6}\\times0.885$)"),
    ("§C6(d) 'In the ToF energy model' (R2B_C4-C6)",
     "The 940 nm, 10 nm case then gives $7.31\\times10^{8}$ s⁻¹ and a 39% dead fraction for the fully sunlit $\\rho_{\\rm scene}=0.9$ scene ($r\\tau_d=0.49$), and $3.66\\times10^{8}$ s⁻¹ and 22% for the model's central case",
     "The 940 nm, 10 nm case then gives $3.66\\times10^{8}$ s⁻¹ and a 22% dead fraction for the fully sunlit $\\rho_{\\rm scene}=0.9$ scene ($r\\tau_d=0.244$), and $1.83\\times10^{8}$ s⁻¹ and 11.5% ($r\\tau_d=0.122$) for the model's central case; in the same bullet '$0.5\\times0.37\\times0.784=0.145$ in bright sun' → '$0.5\\times0.37\\times0.885=0.164$ in bright sun'"),
    ("§C7a(a) SPAD dead time (R2C_C7-C7a)",
     "each of the nine SPADs of a macro-pixel counts $r=3.66\\times10^{8}/9=4.06\\times10^{7}$ s⁻¹, so $r\\tau_d=0.244$ and each SPAD is dead a fraction $1-e^{-0.244}=21.6\\%$ of the time (Eq. (82)). A SPAD that is dead when the echo arrives misses it, so the live fraction 0.784 multiplies",
     "each of the nine SPADs of a macro-pixel counts $r=1.83\\times10^{8}/9=2.03\\times10^{7}$ s⁻¹, so $r\\tau_d=0.122$ and each SPAD is dead a fraction $1-e^{-0.122}=11.5\\%$ of the time (Eq. (82)). A SPAD that is dead when the echo arrives misses it, so the live fraction 0.885 multiplies"),
    ("§C7a(a) ToF energy (R2C_C7-C7a)",
     "an ideal counter needs 17.3 in the model's bright sun, §C0 subsection 10.3). At 940 nm, 37% PDE (photon detection efficiency of the SPAD) and the bright-sun live fraction of 0.784 the result is **≈93 nJ** (58–167). With $n_{\\rm req}=25$ (central)",
     "an ideal counter needs 15.0 in the model's bright sun, §C0 subsection 10.3). At 940 nm, 37% PDE (photon detection efficiency of the SPAD) and the bright-sun live fraction of 0.885 the result is **≈72 nJ** (51–113). With $n_{\\rm req}=21.7$ (central); in the substitution that follows, $\\eta=0.5\\times0.37\\times0.885=0.164$ and $E_{\\rm pt}=21.7\\times2.11\\times10^{-19}\\times1.26\\times10^{5}/(0.1\\times4.91\\times10^{-4}\\times0.164)=5.77\\times10^{-13}/(8.05\\times10^{-6})\\approx7.2\\times10^{-8}$ J; low case 17.4 counts, eta 0.185: 51 nJ; high case 30.4 counts, live fraction 0.784, eta 0.145: 113 nJ"),
    ("§C7a(a) FMCW counts (R2C_C7-C7a)",
     "close to the ×1.45 that takes ToF from 17.3 to 25 counts. Waymo's analysis",
     "close to the ×1.45 that takes ToF from 15.0 to 21.7 counts. Waymo's analysis"),
    ("§C7a(a) factor list (R2C_C7-C7a)",
     "- detection statistics (4.8×), 120 required photoelectrons against 25 counts:",
     "- detection statistics (5.5×), 120 required photoelectrons against 21.7 counts:"),
    ("§C7a(c) electronics inputs (R2C_C7-C7a)",
     "the background count rate $r_{\\rm bg}=3.66\\times10^{8}$ s⁻¹ per macro-pixel",
     "the background count rate $r_{\\rm bg}=1.83\\times10^{8}$ s⁻¹ per 0.05° × 0.05° macro-pixel"),
    ("§C7a(c) cross-check (R2C_C7-C7a)",
     "$b=r_{\\rm bg}\\,\\Delta t_{\\rm bin}\\,N_{\\rm shots}\\,(1-f_{\\rm dead})=3.66\\times10^{8}\\ {\\rm s^{-1}}\\times1\\ {\\rm ns}\\times10\\times0.784=2.87$",
     "$b=r_{\\rm bg}\\,\\Delta t_{\\rm bin}\\,N_{\\rm shots}\\,(1-f_{\\rm dead})=1.83\\times10^{8}\\ {\\rm s^{-1}}\\times1\\ {\\rm ns}\\times10\\times0.885=1.62$"),
    ("§C7b opening (R2D_C7b)",
     "still needs 120 photoelectrons per point against 25 counts for ToF (§C0 subsection 10.3)",
     "still needs 120 photoelectrons per point against 21.7 counts for ToF (§C0 subsection 10.3)"),
    ("§C7b subsection 1 'Per bin' (R2D_C7b)",
     "so there are $5{,}960/2{,}080\\approx2.87$ counts per bin. Eq. (98), with the 0.784 live fraction, gives the same: $3.66\\times10^{8}\\times10^{-9}\\times10\\times0.784=2.87$. So ≈25 signal counts in one bin stand out clearly: the detection threshold is 15 counts (§C0 subsection 10.3).",
     "so there are $3{,}370/2{,}080\\approx1.62$ counts per bin. Eq. (98), with the 0.885 live fraction, gives the same: $1.83\\times10^{8}\\times10^{-9}\\times10\\times0.885=1.62$. So ≈22 signal counts in one bin stand out clearly: the detection threshold is 12 counts (§C0 subsection 10.3)."),
    ("§C7b subsection 1(b) counts needed (R2D_C7b)",
     "The model uses 120, a ×1.36 margin, close to the ×1.45 that takes ToF from 17.3 to 25 counts.",
     "The model uses 120, a ×1.36 margin, close to the ×1.45 that takes ToF from 15.0 to 21.7 counts."),
    ("§C7b subsection 1 speckle and search (R2D_C7b)",
     "a coherent sample needs 120 photoelectrons against 25 counts (§C0 subsection 10.3);",
     "a coherent sample needs 120 photoelectrons against 21.7 counts (§C0 subsection 10.3);"),
    ("§C7b subsection 1(d) detection statistics (R2D_C7b)",
     "- **Detection statistics (4.8×):** the four looks need 120 photoelectrons and ToF 25 counts; for the ideal requirements the ratio is 5.1 ($88.5/17.3$, §C0 subsection 10.3). Of the ideal 5.1, ×1.27 is the coherent receiver's one photoelectron of shot noise in each of the ≈2,450 FFT bins it searches (17.3 → 21.9), ×1.79 is finding the peak in both ramps (21.9 → 39.1), and ×2.26 is speckle fading with four looks (39.1 → 88.5): $1.27\\times1.79\\times2.26=5.1$.",
     "- **Detection statistics (5.5×):** the four looks need 120 photoelectrons and ToF 21.7 counts; for the ideal requirements the ratio is 5.9 ($88.5/15.0$, §C0 subsection 10.3). Of the ideal 5.9, ×1.46 is the coherent receiver's one photoelectron of shot noise in each of the ≈2,450 FFT bins it searches (15.0 → 21.9), ×1.79 is finding the peak in both ramps (21.9 → 39.1), and ×2.26 is speckle fading with four looks (39.1 → 88.5): $1.46\\times1.79\\times2.26=5.9$."),
    ("§C7b subsection 1 ToF energy 93 nJ and ratio 3.2× (R2D_C7b)",
     "'≈0.30 µJ per FMCW sample against ≈93 nJ per ToF point' and 'about 160× the 93 nJ of a ToF point' (1(a)); 'A 940 nm SPAD time-of-flight sensor needs ≈93 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, about 3.2× more.' (opening); table row '| 25 counts | 0.145 | 93 nJ | $1.1\\times10^{7}$ |'; '(d) Why FMCW buys ≈3.2× fewer sampled points per joule than SPAD ToF' and '(93 nJ)'",
     "§C0 subsection 10.6 now points to '≈72 nJ of §C7a subsection 2(a) and §C7b subsection 1' (74.2 nJ with clear air). On the §C7a model: 93 → 72 nJ; 3.2× → 4.2× (0.303/0.072); 15 µJ/93 nJ ≈ 160× → 15 µJ/72 nJ ≈ 210×; table row 21.7 counts, 0.164, 72 nJ, $1/(72\\times10^{-9}\\ {\\rm J})=1.4\\times10^{7}$ points per joule."),
    ("§C10.3 Sunlight assumption (R2E_C10)",
     "(§C0 subsection 10.3: 17.3 counts for an ideal counter, 25 in the §C7a model)",
     "(§C0 subsection 10.3: 15.0 counts for an ideal counter, 21.7 in the §C7a model)"),
    ("§C10.3 caveats (R2E_C10)",
     "a fully sunlit scene of reflectance 0.9 raises the ideal requirement only to ≈20 (§C0 subsection 10.3;",
     "a fully sunlit scene of reflectance 0.9 raises the ideal requirement only to ≈17 (§C0 subsection 10.3;"),
    ("§C10.3a item 7 caveat (R2E_C10)",
     "against ≈5 counts for SPAD ToF at night and ≈17 in bright sun (§C0 subsection 10.3)",
     "against ≈5 counts for SPAD ToF at night and ≈15 in bright sun (§C0 subsection 10.3)"),
    ("§C10.3 inputs (R2E_C10)",
     "$N_{\\rm req}=20$ [E: close to the bright-sun requirement of §C0 subsection 10.3] and $\\eta=0.15$ [E: about the §C7a value, 0.145]",
     "Decision 7: 940 nm with $N_{\\rm req}=21.7$ [E: the §C7a model, ×1.45 over the ideal 15.0 of §C0 subsection 10.3] and $\\eta=0.164$ [E: $0.5\\times0.37\\times0.885$, §C0 subsection 10.3]"),
    ("§F6 'My view' (R2C_C7-C7a)",
     "at 200 m FMCW needs ≈3.2× more optical energy per point than 940 nm time-of-flight (ToF) lidar",
     "at 200 m FMCW needs ≈4.2× more useful optical energy per point (≈5.3× emitted by an ungated transmitter; §C7a) than 940 nm time-of-flight (ToF) lidar"),
]

# ------------------------------------------------------------------ checks and output
text = REPORT.read_text(encoding="utf-8")
c0_start, c0_end = text.index("\n## C0."), text.index("\n## C1.")
problems, spans = [], []
for i, (f, old, new, why) in enumerate(E, 1):
    k = text.count(old)
    if k != 1:
        problems.append(f"edit {i}: old occurs {k} times: {old[:80]!r}")
        continue
    s = text.index(old)
    if not (c0_start < s and s + len(old) < c0_end):
        problems.append(f"edit {i}: outside §C0")
    if "\\tag{" in old or "\\tag{" in new:
        if old.count("\\tag{") != new.count("\\tag{"):
            problems.append(f"edit {i}: tag count changed")
    spans.append((s, s + len(old), i))
spans.sort()
for (a0, a1, ai), (b0, b1, bi) in zip(spans, spans[1:]):
    if b0 < a1:
        problems.append(f"overlap {ai} / {bi}")
for loc, old, new in CS:
    if old.startswith("'") or old.startswith("Decision"):
        continue
    if old not in text:
        problems.append(f"cross-section text not found: {old[:80]!r}")
for p in problems:
    print("PROBLEM", p)
if problems:
    sys.exit(1)

for loc, old, new in CS:
    sk("cross-section quote of a §C0 number changed in this round", "cross_section", loc,
       f"Exact text: {old} → proposed: {new}")

data = {"block": LABEL,
        "edits": [dict(id=f"{LABEL}-{i:03d}", finding=f, old=o, new=n, why=w) for i, (f, o, n, w) in enumerate(E, 1)],
        "skipped": S}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
kinds = {}
for s in S:
    kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
print(f"{len(E)} edits, {len(S)} skipped {kinds}; written {OUT.name}")
