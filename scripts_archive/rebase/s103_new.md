#### 10.3 How much light is needed: detection statistics (Figure C0.10b)

A detection is a decision made in one range bin (ToF) or one frequency bin (FMCW): the signal there must cross a threshold that noise alone crosses only rarely. This part finds how many signal photoelectrons per point, on average, make that decision succeed with a given probability, with both receivers held to the same rule.

**The detection rule.** A point must be detected with probability $P_D=0.9$, and noise may produce at most $P_{FA,\rm pt}=10^{-3}$ false points per point, counted over the whole range the receiver searches (0–300 m here).
- **Why per point, not per bin.** The two receivers search different numbers of cells. A ToF histogram has 2,000 time bins over 300 m, while an FMCW receiver searches ≈2,450 frequency bins in one chirp ramp and a further window in the other. A common per-bin false-alarm probability would give them different false-point rates. Subsection 7 uses the same per-point budget.
- **What it allows.** At 10 Mpts/s, $10^{-3}$ per point is $10^{4}$ false points per second before any filtering; products remove most of them with neighbour-consistency checks (subsection 7).
- **Per-bin probability.** The per-bin false-alarm probability $p$ then follows from the number of bins each receiver searches.

*Photon counting (SPAD histogram).* A pixel that sums hundreds of speckles sees a non-fading signal, so signal and background counts are Poisson.
- **Rule:** the histogram has $N_{\rm bins}=2{,}000$ bins of 1 ns over 0–300 m, so each bin may false-alarm with probability $p=P_{FA,\rm pt}/N_{\rm bins}=5\times10^{-7}$. With background mean $b$ per bin, the threshold $n_{\rm th}$ is the smallest count with $P(N\ge n_{\rm th}\mid b)\le p$. Here $P(N\ge n\mid\mu)$ is the probability that a Poisson count $N$ of mean $\mu$ is at least $n$, and $s$ is the mean signal count in the echo's bin. Then
$$P_D=P(N\ge n_{\rm th}\mid s+b)=\frac{\gamma(n_{\rm th},\,s+b)}{\Gamma(n_{\rm th})}. \tag{36}$$
  The special functions are:
  - $\Gamma(n)=\int_0^\infty u^{n-1}e^{-u}\,du$, the gamma function, which equals $(n-1)!$ for a whole number $n$;
  - $\gamma(n,x)=\int_0^x u^{n-1}e^{-u}\,du$, the lower incomplete gamma function, the same integral stopped at $x$;
  - their ratio $\gamma(n,x)/\Gamma(n)$, the regularized lower incomplete gamma function, which rises from 0 to 1 as $x$ grows. It equals the Poisson tail $P(N\ge n\mid x)$, which is why it appears here.
- **Night, $b=0.01$:** $P(N\ge2\mid0.01)=5.0\times10^{-5}$ is too high and $P(N\ge3\mid0.01)=1.7\times10^{-7}$ passes, so $n_{\rm th}=3$.
- **Bright sun, $b=2.94$:** $P(N\ge15\mid2.94)=5.2\times10^{-7}$ just fails and $P(N\ge16\mid2.94)=9.5\times10^{-8}$ passes, so $n_{\rm th}=16$.
- **Where $b=2.94$ comes from** [E]. It is the bright-sun background of the §C7a ToF model, built from the equations of §C6(d):
  - Eq. (76) gives $r_{\rm bg}=5.93\times10^{8}$ counts per second per macro-pixel for a fully sunlit scene of reflectance 0.9, at 940 nm behind a 10 nm filter and at PDE 0.3. The same SPADs count background and signal, so at the model's PDE of 0.37 the rate is $5.93\times10^{8}\times0.37/0.3=7.31\times10^{8}$ s⁻¹.
  - The central case takes half of that, $r_{\rm bg}=3.66\times10^{8}$ s⁻¹: a sunlit scene of reflectance ≈0.45, or a pixel whose view is only half filled by bright surfaces. The full value is the model's high case.
  - Eq. (77) gives the dead fraction. Each of the nine SPADs counts $r=3.66\times10^{8}/9=4.06\times10^{7}$ s⁻¹, so $r\tau_d=0.244$ for $\tau_d=6$ ns, and $f_{\rm dead}=0.244/1.244=0.196$.
  - Eq. (93) of §C7b, multiplied by the live fraction $1-f_{\rm dead}$, gives the counts in one 1 ns bin summed over the $N_{\rm shots}=10$ shots of a point: $b=r_{\rm bg}\,t_{\rm bin}\,N_{\rm shots}\,(1-f_{\rm dead})=3.66\times10^{8}\times10^{-9}\times10\times0.804=2.94$.
  - Over the 20.8 µs a point listens, the same rate gives $3.66\times10^{8}\times20.8\times10^{-6}\times0.804\approx6{,}120$ background events, the event count of the §C7a electronics budget.

*Coherent detection in one frequency bin (FMCW building blocks).* After the FFT, the power in one frequency bin is compared with a threshold.
- **Normalization:** the noise (LO shot noise) is set to unit mean, so noise-only power in a bin is exponential and exceeds a threshold $x$ with probability $e^{-x}$. A per-bin false-alarm probability $p$ therefore sets the threshold $x_{\rm th}=-\ln p$. In a shot-noise-limited receiver the mean signal-to-noise ratio equals $\bar n$ (subsection 2), so $\bar n$ is also the signal power in these units.
- **This noise is quantum, not background.** It is the shot noise of heterodyne detection: every FFT bin searched carries about one photoelectron of it, whereas a ToF bin at night holds 0.01 background counts.
- **Steady, non-fading target:**
$$P_D=Q_1\!\left(\sqrt{2\bar n},\sqrt{2x_{\rm th}}\right), \tag{37}$$
  where $Q_1(u,v)$ is Marcum's Q function: the probability that the envelope of a steady tone of amplitude $u$ plus Gaussian noise (unit variance per quadrature) exceeds a threshold $v$. The factors of 2 convert the unit-mean power scale into that amplitude scale.
- **One speckle** (Rayleigh amplitude, exponential intensity; Swerling I, Eq. (27) of subsection 7 with $\overline{\rm SNR}=\bar n$):
$$P_D=p^{1/(1+\bar n)} . \tag{38}$$
- **$N_{\rm sp}$ independent speckles summed incoherently** (polarization, wavelength or spatial diversity; each is one *look*, taken by its own coherent receiver), with $\bar n$ split equally among them:
  - the noise-only sum is Gamma-distributed, so the threshold $x_{N_{\rm sp}}$ solves $Q(N_{\rm sp},x_{N_{\rm sp}})=p$, where $Q(n,x)=1-\gamma(n,x)/\Gamma(n)$ is the regularized upper incomplete gamma function, the probability that a sum of $n$ independent unit-mean exponential variables exceeds $x$;
  - each speckle's power, signal plus noise, is then exponential with mean $1+\bar n/N_{\rm sp}$, so
$$P_D=Q\!\left(N_{\rm sp},\,\frac{x_{N_{\rm sp}}}{1+\bar n/N_{\rm sp}}\right). \tag{39}$$

*An FMCW point: both ramps, over the whole range.* Eqs. (37)–(39) put all the photons in one bin. An FMCW point needs more, because a triangular chirp measures it with an up-ramp and a down-ramp (subsection 2): range and radial velocity follow only when the echo's peak is found in both, at $f_{\rm up}=f_b-f_D$ and $f_{\rm down}=f_b+f_D$.
- **The photons are split.** Each ramp collects half of the point's photoelectrons, $\bar n/2$.
- **The fading is common.** Target and beam do not change within the ≈10 µs of the two ramps, so both see the same speckle and only their noise is independent. A fade therefore removes the peak from both ramps at once; it does not average out between them.
- **Two searches.** The up-ramp peak must be found among all $N_b$ bins the beat can occupy, and the down-ramp peak within the window of $N_w$ bins around it that the velocity range allows. For the §C7a chirp (1 GHz over 5 µs up and 5 µs down, so 200 kHz bins; 300 m; ±70 m/s):
  - $N_b=(f_{b,\max}+f_{D,\max})\,T_u=2{,}450$, where $T_u=5$ µs is one ramp, $f_{b,\max}=400$ MHz the range beat at 300 m and $f_{D,\max}=90$ MHz the Doppler shift at 70 m/s. Equivalently $N_b=R_{\max}/\Delta R+f_{D,\max}T_u=2{,}000+450$; Eq. (89) of §C7a samples these bins five times over, $N_{\rm samp}=5N_b\approx12{,}300$.
  - $N_w=4f_{D,\max}T_u=1{,}800$: the down-ramp peak sits $2f_D$ from the up-ramp peak, and $2f_D$ spans ±180 MHz.
- **False points and detection.** A false point needs noise to cross the threshold in the up-ramp search (probability $p_1$ per bin) and again in the down-ramp window ($p_2$ per bin). The false-point rate and the detection probability are then
$$P_{FA,\rm pt}\approx N_b\,p_1\,N_w\,p_2,\qquad P_D=\int_0^\infty\left[Q_{N_{\rm sp}}\!\left(\sqrt{\bar nS/N_{\rm sp}},\,\sqrt{2x}\right)\right]^2\frac{S^{N_{\rm sp}-1}e^{-S}}{\Gamma(N_{\rm sp})}\,dS . \tag{9001}$$
  - **Thresholds.** Splitting the budget evenly gives $p_1=p_2=p=\sqrt{P_{FA,\rm pt}/(N_bN_w)}=\sqrt{10^{-3}/(2{,}450\times1{,}800)}=1.5\times10^{-5}$; the best uneven split changes the results by less than 0.1%. The threshold $x$ in each ramp solves $Q(N_{\rm sp},x)=p$, as in Eq. (39): $x=-\ln p=11.1$ for one look and 18.2 for four.
  - **Symbols.** $S$ is the speckle power gain summed over the $N_{\rm sp}$ looks, each look's gain being exponential with unit mean; the sum is Gamma-distributed with the density shown, which for one look is $e^{-S}$. Each ramp then holds a signal power $\bar nS/(2N_{\rm sp})$ spread over its $N_{\rm sp}$ looks. $Q_M(a,b)$ is the generalized Marcum Q function: the probability that the summed power of $M$ bins of unit-mean noise, carrying a total signal power $a^2/2$, exceeds $b^2/2$. For $M=1$ it is the $Q_1$ of Eq. (37).
  - **Reading.** The square is the two ramps' independent noise, and the integral averages over their common fading. A steady target does not fade, so for it $P_D=[Q_1(\sqrt{\bar n},\sqrt{2x})]^2$ with $x=-\ln p$.

The table gives both receivers' requirements under this rule. In the FMCW rows, $\bar n$ is the total over both ramps and all looks.

| Receiver statistics | $\bar n$ for $P_D=0.5$ | $\bar n$ for $P_D=0.9$ | $P_D$ at $\bar n=25$ | $P_D$ at $\bar n=120$ |
|---|---|---|---|---|
| Photon counting, night ($b=0.01$, $n_{\rm th}=3$) | 2.7 | 5.3 | 1.00 | 1.00 |
| Photon counting, bright sun ($b=2.94$, $n_{\rm th}=16$) | 12.7 | 18.4 | 0.99 | 1.00 |
| FMCW, steady target | 26.6 | 39.1 | 0.43 | 1.00 |
| FMCW, 4 looks summed | 39.0 | 88.5 | 0.22 | 0.96 |
| FMCW, 2 looks summed | 36.2 | 120 | 0.32 | 0.90 |
| FMCW, 1 look | 38.2 | 259 | 0.35 | 0.80 |

*How the numbers are derived* [E]:
- **Method:** each entry solves the matching $P_D$ expression numerically (script): Eq. (36) for photon counting, with $\bar n=s$, and Eq. (9001) for the FMCW rows, with the thresholds above.
- **Worked check, bright sun:** $s=18.4$ puts the total mean at $s+b=21.3$, and a Poisson count of mean 21.3 reaches 16 with probability 0.90.
- **Worked check, one look:** in Eq. (9001) the common fade dominates. Both ramps cross their thresholds roughly when the speckle gain exceeds $2x/\bar n$, which for one look happens with probability $e^{-2x/\bar n}$. Setting that to 0.9 gives $\bar n\approx2\times11.1/0.105=211$; the noise in each ramp raises the exact value to 259.
- **More looks:** eight looks need 82.4 photoelectrons. The requirement approaches the steady target's 39.1 only slowly as the number of looks grows.

![Detection probability versus mean signal photoelectrons for photon counting and coherent detection](automotive_perception_report_figures/link_budget_detection_statistics.png)

*Figure C0.10b.* Detection probability versus mean signal photoelectrons per point, with at most $10^{-3}$ false points per point over a 0–300 m search.
- Solid: photon counting at night and in bright sun (2,000 bins, Eq. (36)). Dashed: FMCW with the echo's peak found in both chirp ramps (Eq. (9001)), for a steady target, four summed looks and one look.
- Dots and numbers mark $P_D=0.9$. The dotted verticals are the photoelectron counts used in the §C7a model: 25 for ToF and 120 for FMCW (four looks).

**Reading Figure C0.10b** [E]:
- **ToF:** the model's 25 counts are 1.36× the 18.4 that an ideal counter needs in bright sun. The margin covers a return spread over two or three bins, dead time and pile-up (§C6). In the model's high case, a fully sunlit scene of reflectance 0.9 ($b=4.92$, $n_{\rm th}=20$), the ideal counter needs 21.0.
- **FMCW:** the model's 120 photoelectrons over four looks carry the same 1.36× margin over the ideal 88.5. They give $P_D=0.96$ with four looks, 0.90 with two and 0.80 with one.
- **Waymo's figure is a one-ramp figure.** Waymo's 50 photoelectrons for 90% detection with four averaged speckles at $10^{-6}$ per bin [P] matches one ramp searched in full, which needs 47.3 by the rule here. Requiring the peak in both ramps raises this to 88.5.
- **Where FMCW's extra photons go** (four looks, 88.5 against the counter's 18.4 in bright sun):
  - *the noise floor, ×1.2:* even a steady target in one fully searched ramp needs 21.9, more than the counter in bright sun. Each of the 2,450 bins carries one photoelectron of shot noise, and the threshold must clear the largest of them; the counter's threshold only has to clear the Poisson tail of 2.94 counts;
  - *both ramps, ×1.8:* splitting the photons and passing two thresholds raises the steady target to 39.1;
  - *fading, ×2.3:* four looks raise it to 88.5. One look would raise it to 259, ×6.6.
- **Curve shapes:** photon counting has the steepest curves. Once the mean clears the threshold, a non-fading Poisson signal almost always crosses it. Speckle fading makes the coherent curves shallow: the median ($P_D=0.5$) is 36–39 photoelectrons with one, two or four looks, but reaching 90% costs up to 7× the median.

**Is the FFT the limit? Nearly** [E; detection theory I]. For a tone of unknown frequency and phase in white noise, the peak of the FFT power spectrum (the periodogram) is the maximum-likelihood, or generalized likelihood-ratio, detector (S. M. Kay, *Fundamentals of Statistical Signal Processing*, Vol. II, 1998). No algorithm extracts more from one ramp without prior information. Two costs remain:
- **Straddle (scalloping) loss.** A beat that falls between FFT bins loses signal: 1.1 dB on average and 3.9 dB at worst with a rectangular window, and 0.3 and 0.9 dB with twofold zero padding. This belongs to the 1.36× implementation margin.
- **The search.** The threshold rises with the logarithm of the number of cells searched. A joint search, neighbour checks or a tracking window lower the requirement by 8–33%, for both receivers:

| Search (FMCW: four looks; ToF: bright sun) | FMCW $\bar n$ for $P_D=0.9$ | ToF $s$ for $P_D=0.9$ |
|---|---|---|
| Full search (the rule above) | 88.5 | 18.4 |
| Joint search over all $N_bN_w=4.4\times10^{6}$ up–down pairs, summing both ramps | 77.8 | — |
| $10^{-2}$ false points per point, pruned by neighbour checks | 81.6 | 16.0 |
| Tracking window of 20 bins per ramp around a predicted return | 59.6 | 14.8 |
| Known cell (no search; the ideal bound) | 32.2 | 11.3 |

- **What the table shows.** The joint search is the optimal detector for an unknown range and velocity, and the two-stage search of Eq. (9001) needs only 14% more. Even a known cell needs 32.2 photoelectrons with four looks (13.8 for a steady target, 77.1 for one look), well above the counter's 11.3. Fading and heterodyne shot noise are physics, not algorithm. The model therefore uses the full search for both receivers and treats these gains as sensitivities.

**What this means for the comparison** [E]. Under one rule, a SPAD ToF receiver in bright sun needs 18–25 counts per point, and an FMCW receiver 88–120 photoelectrons with four looks (259 with one). The coherent receiver's freedom from background does not lower its photon requirement: even a steady coherent target needs more (39.1) than an ideal counter in bright sun (18.4), and speckle fading adds to that. 10.4 turns the model's counts, 25 for SPAD ToF and 120 for FMCW (30 in each of four looks), into detection levels.
