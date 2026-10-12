**(d) The chirp the laser must deliver: tuning range, ramp time and linearity. A cost, not the floor.** Three quantities specify the chirp: how far it sweeps, how long each ramp lasts, and how straight the sweep is. The chirp rate follows from the first two.
- **Tuning range.** The range resolution is set by the frequency swept *while the echo is present*, $B_{\rm eff}=c/(2\Delta R)$ (item (a)): 1 GHz for $\Delta R=15$ cm, 3 GHz for 5 cm. The laser must sweep further than that, because it keeps sweeping through the round trip $\tau$ at the start of each ramp, before any usable echo has arrived. The total continuous, mode-hop-free sweep per ramp is therefore

  $$B_{\rm tot}=\kappa\,T_c=B_{\rm eff}\,\frac{T_u+\tau}{T_u}=B_{\rm eff}\left(1+\frac{\tau}{T_u}\right), \tag{9001}$$

  where $\kappa=B_{\rm eff}/T_u$ is the chirp rate, $T_c=T_u+\tau$ the ramp duration (Eq. (95)) and $T_u$ the useful window.
  - The overhead cannot be avoided when one laser serves as both transmitter and LO. The echo that beats during the useful window $[\tau,T_c]$ was emitted during $[0,T_c-\tau]$, so the laser frequency must follow one straight line over the whole ramp $[0,T_c]$.
  - The overhead is small for long useful windows ($T_u\gg\tau$) and grows without bound as $T_u\to0$. At 300 m ($\tau=2.0$ µs, Eq. (94)) and 15 cm: $T_u=7.5$ µs gives $B_{\rm tot}=1\ {\rm GHz}\times(1+2/7.5)=1.27$ GHz, and $T_u=2.25$ µs gives $1\ {\rm GHz}\times(1+2/2.25)=1.89$ GHz.
- **Ramp time.** $T_c$ is not a free choice of the laser. It is $T_u+\tau$, and $T_u$ is set by how long the channel needs to collect its photons (item (g)). The laser then repeats the up–down triangle at a rate $1/(2T_c)$: 30–120 kHz in the cases of item (g).
- **Chirp rate** follows: $\kappa=B_{\rm eff}/T_u$, e.g. $1\ {\rm GHz}/7.5\ \mu{\rm s}=1.3\times10^{14}$ Hz/s, or $1\ {\rm GHz}/1\ \mu{\rm s}=10^{15}$ Hz/s. It is a derived number, not a requirement in its own right. What the laser must do is cover $B_{\rm tot}$ within $T_c$, linearly, ramp after ramp.
- **Linearity: an absolute frequency tolerance set by range alone.** Let $\delta\nu(t)$ be the laser frequency's deviation from the ideal straight ramp. The beat is the LO frequency now minus the frequency of the echo emitted $\tau$ earlier:

  $$f_b(t)=\nu(t)-\nu(t-\tau)\approx\kappa\tau+\tau\,\frac{d\,\delta\nu}{dt}, \tag{9002}$$

  which holds when $\delta\nu$ changes little within $\tau$. The beat therefore wanders by $\tau$ times the slope of the frequency error.
  - Take a smooth bow over the useful window, $\delta\nu(t)=\delta\nu_{\max}\,[1-(2t/T_u-1)^2]$ for $0\le t\le T_u$: zero at both ends and $\delta\nu_{\max}$ at the centre. Its slope runs from $+4\delta\nu_{\max}/T_u$ to $-4\delta\nu_{\max}/T_u$, so by Eq. (9002) the beat sweeps over $8\tau\,\delta\nu_{\max}/T_u$ during the window.
  - The FFT resolves frequencies in bins $1/T_u$ wide. The peak stays within one bin if $8\tau\,\delta\nu_{\max}/T_u\le1/T_u$, that is

  $$\delta\nu_{\max}\lesssim\frac{1}{8\tau}=\frac{c}{16R}. \tag{9003}$$

  - The tolerance depends on range only, not on the sweep bandwidth or the ramp time: $3\times10^{8}/(16\times300)=62.5$ kHz at 300 m and 94 kHz at 200 m.
  - As a fractional peak-to-peak error in the chirp rate the same condition reads $\varepsilon=8\delta\nu_{\max}/B_{\rm eff}\le1/(\tau B_{\rm eff})=\Delta R/R$, using $B_{\rm eff}\tau=R/\Delta R$ (Eq. (98)). That is $5\times10^{-4}$ for 15 cm at 300 m and $1.7\times10^{-4}$ for 5 cm. It is the range-blur rule $\delta R\approx\varepsilon R$ with the blur held inside one resolution cell: at 200 m, $\varepsilon=10^{-3}$ gives $\delta R\approx0.2$ m, more than the 15 cm cell, and $\varepsilon=10^{-4}$ gives 2 cm.
  - The tolerance applies to what remains after any correction. An auxiliary reference interferometer that measures the actual ramp, followed by resampling or digital correction of the beat, relaxes the laser requirement at the cost of one more optical and digital path per sensor.
- **Directly modulated DFB lasers** (distributed-feedback laser diodes, chirped by modulating their drive current) tune through two competing effects: fast carrier tuning and slower thermal tuning. The two cross over at roughly 1–10 MHz of modulation frequency [U].
  - A linear ramp of a few µs has harmonic content up to tens of MHz, so pre-distortion (shaping the drive current so that the optical chirp comes out linear) or feedback must stay accurate across that crossover. It gets harder as $T_c$ shrinks.
  - Waymo reports a pre-distorted DFB holding <100 kHz error over 1 GHz, i.e. $\varepsilon<10^{-4}$ [P] (§C7a(f)). By Eq. (9003) that is enough at 200–250 m and marginal at 300 m; the exact margin depends on the shape of the error [E].
- **Electro-optic chirping** (thin-film lithium niobate, single-sideband modulators) or an optical phase-locked loop (a feedback loop that locks the laser's frequency sweep to a reference) reaches $10^{15}$–$10^{16}$ Hz/s linearly. The laser's ability to chirp is therefore not the fundamental floor; it sets the cost of reaching short, linear chirps. Item (g) shows when that cost matters.

**(e) Laser linewidth sets a range-dependent loss, not a cap on the chirp length.**
- **Where the loss comes from.** The LO and the echo are the same laser at two instants $\tau$ apart. Their phase difference $\Delta\phi(t)=\phi(t)-\phi(t-\tau)$ therefore carries only the phase noise accumulated over $\tau$. Its variance is set by the laser's frequency-noise spectrum:

  $$\sigma^2_{\Delta\phi}\approx\int_{1/T_u}^{\infty}S_\nu(f)\,\frac{4\sin^2(\pi f\tau)}{f^2}\,df, \tag{9004}$$

  where $S_\nu(f)$ is the one-sided power spectral density of the laser's frequency fluctuations (Hz²/Hz) at Fourier frequency $f$, and $4\sin^2(\pi f\tau)/f^2$ is the filter of the delay $\tau$.
  - Frequency noise slower than about $1/T_u$ is left out: within one ramp it only shifts the beat's phase, or its frequency by $\tau\,d\delta\nu/dt$, which the FFT does not count as lost power [E].
  - For white frequency noise, $S_\nu=\Delta\nu/\pi$, where $\Delta\nu$ is the Lorentzian (intrinsic) linewidth. With $\int_0^\infty\sin^2(af)/f^2\,df=\pi a/2$ and $a=\pi\tau$, the integral gives $\sigma^2_{\Delta\phi}=(\Delta\nu/\pi)\times4\times\pi^2\tau/2=2\pi\Delta\nu\,\tau$ (slightly less with the $1/T_u$ lower limit).
  - So the specification that matters is the frequency-noise level at Fourier frequencies from about $1/T_u$ (≈0.1 MHz) to a few $1/\tau$ (MHz), not a linewidth measured over milliseconds.
- **What it costs.** With $\Delta\phi$ Gaussian, the beat splits into a sharp coherent tone that carries a fraction

  $$\eta_{\rm coh}\approx e^{-\sigma^2_{\Delta\phi}}=e^{-2\pi\Delta\nu\,\tau} \tag{99}$$

  of the beat power, and a pedestal that carries the rest (Richter et al., *IEEE J. Quantum Electron.* 22, 2070 (1986)).
  - In the regime of automotive lidar, $2\pi\Delta\nu\tau\lesssim1$, the pedestal spreads over roughly $\pm1/\tau$ around the tone (±0.5 MHz at 300 m), not over $2\Delta\nu$. That is about $\pm T_u/\tau$ FFT bins, i.e. $\pm T_u/\tau$ range cells, so it raises the floor near a strong return and can mask a weak target just behind it [E].
- **Why it does not cap the chirp.** The coherent tone is a true spectral line: its FFT peak keeps growing as $T_u$ lengthens, exactly as without phase noise. What linewidth removes is a fixed fraction of the signal, set by the range. It therefore enters the photon budget as a multiplier on the energy, $E_{\rm opt}\to E'=E_{\rm opt}/\eta_{\rm coh}$, not as a limit on $T_u$. What does make long ramps harder is frequency noise slower than $1/T_u$ (flicker noise, drift) and chirp nonlinearity (Eq. (9003)), which are specified separately.
- **Requirement.** Allowing the coherent share to fall to no less than $\eta_{\min}$ gives

  $$\Delta\nu\le\frac{\ln(1/\eta_{\min})}{2\pi\tau}=\frac{c\,\ln(1/\eta_{\min})}{4\pi R}. \tag{9005}$$

| Allowed coherent loss | $\eta_{\min}$ | Max linewidth at 200 m | at 250 m | at 300 m |
|---|---|---|---|---|
| 0.5 dB | 0.89 | 13.7 kHz | 11.0 kHz | 9.2 kHz |
| 1 dB | 0.79 | 27.5 kHz | 22.0 kHz | 18.3 kHz |
| 3 dB | 0.50 | 82.7 kHz | 66.2 kHz | 55.2 kHz |
| 4.3 dB ($e^{-1}$) | 0.37 | 119 kHz | 95.5 kHz | 79.6 kHz |
| 8.7 dB ($e^{-2}$, the rule $L_c\ge2R$) | 0.14 | 239 kHz | 191 kHz | 159 kHz |

*How the table is computed* [E]: Eq. (9005) with $2\pi\tau=2\pi\times2R/c$, which is $8.38\times10^{-6}$ s at 200 m, $1.05\times10^{-5}$ s at 250 m and $1.26\times10^{-5}$ s at 300 m. Worked cell (3 dB at 300 m): $\ln2/(1.26\times10^{-5}\ {\rm s})=0.693/1.26\times10^{-5}=55$ kHz. A loss of $L$ dB means $\eta_{\min}=10^{-L/10}$, so $\ln(1/\eta_{\min})=0.115$, 0.230, 0.693, 1 and 2 for the five rows.

- **Lasers against the requirement at 300 m** [E; linewidths as cited in §C7a(f)]. With $2\pi\tau=1.26\times10^{-5}$ s:
  - 10 kHz: $2\pi\Delta\nu\tau=0.126$, $\eta_{\rm coh}=0.88$ (−0.5 dB), energy ×1.13;
  - 42 kHz (SiN self-injection-locked laser): 0.528, $\eta_{\rm coh}=0.59$ (−2.3 dB), energy ×1.7;
  - 100 kHz (Waymo's upper figure; Pointcloud's external DFB, §C10.3): 1.26, $\eta_{\rm coh}=0.28$ (−5.5 dB), energy ×3.5;
  - 378 kHz (TFLN E-DBR laser): 4.75, $\eta_{\rm coh}=0.0087$ (−21 dB), energy ×116: unusable at 300 m.
- **The energies of subsection 1 leave this loss out.** With a 100 kHz laser at 200 m, $\eta_{\rm coh}=e^{-0.84}=0.43$, so the central 0.30 µJ becomes $0.30/0.43=0.70$ µJ.
- **The coherence-length rule of thumb,** $L_c=c/(\pi\Delta\nu)\ge2R$ (§C7, Eq. (165)), is the condition $2\pi\Delta\nu\tau\le2$. It keeps only $e^{-2}=14\%$ of the beat in the coherent peak: a limit of detectability, not a design point.

**(f) Scanning caps the chirp from above.** The chirp must end before the beam sweeps across its own width (§C7):
$$T_c\lesssim\frac{\theta_b}{\Omega}, \tag{100}$$
where $T_c$ is the chirp duration, $\theta_b$ the angular width of one beam (rad) and $\Omega$ the angular scan speed (rad/s).
- For $\theta_b=0.05°=8.7\times10^{-4}$ rad and a 5 µs chirp, $\Omega\lesssim8.7\times10^{-4}/5\times10^{-6}=175$ rad/s ≈ $10^4$ °/s.
- Target motion during a chirp is negligible: 50 m/s × 10 µs = 0.5 mm.

**(g) Which floor sets the useful window: photons, ADC, chirp rate or tuning range.** Items (a)–(f) combine into one rule. The useful window of each ramp must be long enough for four separate reasons, and the longest of the four wins:

$$T_u=\max\{T_{\rm ph},\,T_{\rm ADC},\,T_\kappa,\,T_B\}, \tag{9006}$$

subject to the scan limit $T_u+\tau\le\theta_b/\Omega$ (Eq. (100)). The dwell is then $T_{\rm dwell}=2(T_u+\tau)$. The four floors are:
1. **Photons,** $T_{\rm ph}=E'/(2P_{\rm ch})$. The two ramps together must collect the energy $E'=E_{\rm opt}/\eta_{\rm coh}$ (item (e)) at the channel's CW optical power $P_{\rm ch}$; this is Eq. (96) with the coherent loss included.
2. **ADC,** $T_{\rm ADC}=(R/\Delta R)/(f_{s,\max}/2.5-f_D)$. The largest beat, $\kappa\tau+f_D=(R/\Delta R)/T_u+f_D$ (Eq. (97), with $B_{\rm eff}\tau=R/\Delta R$), must fit a converter that samples at most at $f_{s,\max}$ under the 2.5× rule of item (c). Solving $2.5[(R/\Delta R)/T_u+f_D]\le f_{s,\max}$ for $T_u$ gives the floor.
3. **Laser chirp rate,** $T_\kappa=B_{\rm eff}/\kappa_{\max}$. A laser that cannot chirp faster than $\kappa_{\max}$ needs at least this long to sweep $B_{\rm eff}$.
4. **Laser tuning range,** $T_B=\tau B_{\rm eff}/(B_{\max}-B_{\rm eff})$. Solving $B_{\rm eff}(1+\tau/T_u)\le B_{\max}$ (Eq. (9001)) for $T_u$, where $B_{\max}$ is the laser's largest continuous, linear sweep at the required repetition rate. If $B_{\max}\le B_{\rm eff}$, the resolution cannot be reached at all.

**A better laser (a larger $\kappa_{\max}$ or $B_{\max}$) shortens the dwell only if $T_\kappa$ or $T_B$ is the largest floor. Otherwise it changes nothing.**

The table evaluates the floors at 300 m and 15 cm ($R/\Delta R=2{,}000$, $\tau=2.0$ µs, $f_D=90$ MHz at 70 m/s). It takes $E'=0.45$ µJ: the central 0.30 µJ at 200 m scaled in proportion to range for an aperture optimized at 300 m (subsection 1(f)), with a laser narrow enough to lose nothing to coherence ($\eta_{\rm coh}\approx1$).

| Floor | Setting | $T_u$ floor |
|---|---|---|
| Photons, $T_{\rm ph}$ | $P_{\rm ch}=16$ / 30 / 100 / 300 mW | 14.1 / 7.5 / 2.25 / 0.75 µs |
| ADC, $T_{\rm ADC}$ | $f_{s,\max}=1$ / 2 / 4 GS/s | 6.5 / 2.8 / 1.3 µs |
| Chirp rate, $T_\kappa$ | $\kappa_{\max}=10^{14}$ / $3\times10^{14}$ / $10^{15}$ / $10^{16}$ Hz/s | 10 / 3.3 / 1.0 / 0.1 µs |
| Tuning range, $T_B$ | $B_{\max}=1.2$ / 1.5 / 2 / 5 GHz | 10 / 4.0 / 2.0 / 0.5 µs |

*How the table is computed* [E]:
- $T_{\rm ph}=E'/(2P_{\rm ch})$: $0.45\ \mu{\rm J}/(2\times0.030\ {\rm W})=7.5$ µs; the other powers scale inversely.
- $T_{\rm ADC}$: at 1 GS/s, $f_{s,\max}/2.5-f_D=400-90=310$ MHz, so $2{,}000/3.1\times10^{8}\ {\rm s^{-1}}=6.45$ µs; at 2 GS/s, $2{,}000/7.1\times10^{8}=2.8$ µs; at 4 GS/s, $2{,}000/1.51\times10^{9}=1.3$ µs.
- $T_\kappa=B_{\rm eff}/\kappa_{\max}$: $10^{9}/10^{14}=10$ µs, and so on.
- $T_B=\tau B_{\rm eff}/(B_{\max}-B_{\rm eff})$: $2\ \mu{\rm s}\times1/(1.2-1)=10$ µs; $2\times1/0.5=4$ µs; $2\times1/1=2$ µs; $2\times1/4=0.5$ µs.

What the table shows [E]:
- **At ≤30 mW per channel, photons set the window: 7.5–14 µs.** The laser then needs only 1.14–1.27 GHz of sweep in ramps of 9.5–16 µs, a chirp rate of $0.7$–$1.3\times10^{14}$ Hz/s, with 0.14–0.27 GHz of headroom above $B_{\rm eff}$ (Eq. (9001)). A faster or wider-tuning laser shortens nothing, and even a 1 GS/s converter does not bind.
- **The ADC binds next, not the laser.** Photons stop setting the window once $T_{\rm ph}<T_{\rm ADC}$, i.e. above $P_{\rm ch}=E'/(2T_{\rm ADC})$. That is $0.45\ \mu{\rm J}/(2\times6.45\ \mu{\rm s})=35$ mW with 1 GS/s converters (the indie Surya class, §C7a(d)), 80 mW at 2 GS/s and 170 mW at 4 GS/s. Beyond that, more power per channel buys nothing unless the converters get faster too.
- **The laser binds only in photon-rich channels.** At 100 mW per channel with converters of ≥2.5 GS/s ($T_{\rm ADC}=2{,}000/9.1\times10^{8}=2.2$ µs), the window falls to $T_{\rm ph}=2.25$ µs. The laser must then sweep 1.89 GHz in 4.25 µs ($4.4\times10^{14}$ Hz/s). A DFB limited to $10^{14}$ Hz/s, or to a 1.2 GHz sweep, would stretch the window back to 10 µs.
- **A fast but narrow sweep limits resolution instead.** A laser with $B_{\max}=0.5$ GHz, like the 500 MHz excursion of the 12 PHz/s TFLN laser of §C7a(f), cannot reach 15 cm at all. With $T_u=7.5$ µs at 300 m it gives $B_{\rm eff}\le B_{\max}T_u/(T_u+\tau)=0.5\times7.5/9.5=0.39$ GHz, i.e. $\Delta R\ge3\times10^{8}/(2\times3.9\times10^{8})=0.38$ m.
- **Finer resolution is paid for in converters, not photons.** Halving $\Delta R$ doubles $B_{\rm eff}$, $B_{\rm tot}$, $\kappa$, the range beat and $T_{\rm ADC}$, and doubles the range samples per point, $5R/\Delta R$ (Eq. (98)). At 5 cm and 300 m, $T_{\rm ADC}=6{,}000/3.1\times10^{8}=19$ µs at 1 GS/s, so the converter, not photons, sets the window even at 16 mW. A surface that is deeper than $\Delta R$ within the beam footprint (a road at grazing incidence) also spreads its echo over several range cells, so finer resolution can lower the peak signal.
- **Splitting a dwell into several shorter chirp pairs never helps.** Each pair pays its own round trip, so $k$ pairs need $T_{\rm dwell}=E'/P_{\rm ch}+2k\tau$ for the same energy. Short, fast chirps pay only when photons are plentiful or when the scan forces them.
- **So a faster or wider-tuning laser helps in three cases only:**
  - photon-rich channels: ≳100 mW each at 300 m, or short range and bright targets, where $T_{\rm ph}$ falls below the laser floors;
  - fast scanning, when $\theta_b/\Omega$ (Eq. (100)) forces the ramp below the photon window. The shorter window then also needs more power per channel, $P_{\rm ch}\ge E'/[2(\theta_b/\Omega-\tau)]$. For a 0.05° beam at $10^4$ °/s ($\theta_b/\Omega=5$ µs) at 300 m, that is $0.45\ \mu{\rm J}/(2\times3\ \mu{\rm s})=75$ mW. At the polygon's 45,600°/s the crossing time, 1.1 µs, is shorter than the 2 µs round trip, and no chirp fits;
  - finer range resolution, which needs a wider $B_{\rm eff}$.
- **Linearity (Eq. (9003)) and linewidth (Eq. (9005)) always matter,** because they blur every point or multiply every point's energy.

**(h) What limits a 10 Mpts/s sensor at 300 m: the light itself.** Summing over all channels turns the dwell into power. With the ingredients of §C7a (laser wall-plug efficiency, per-channel analog power, per-sample ADC and FFT energy), the sensor's electrical power is

$$P_{\rm elec}=\underbrace{\frac{\dot N E'}{\eta_{\rm WPE}}}_{\rm useful\ light}+\underbrace{\frac{2\tau\,\dot N P_{\rm ch}}{\eta_{\rm WPE}}}_{\rm dead\text{-}time\ light}+\underbrace{N_{\rm ch}P_{\rm an}}_{\rm analog}+\underbrace{\dot N N_{\rm samp}e_s}_{\rm ADC\ and\ FFT}+P_0 . \tag{9007}$$

Here $\dot N$ is the point rate; $\eta_{\rm WPE}$ the wall-plug efficiency of the CW laser with its amplifiers, the optical power out per electrical power in (≈0.15 in 2026, §C7a(b)); $P_{\rm an}$ the analog power per channel (TIA, bias and drivers, ≈10 mW); $e_s$ the energy per ADC sample including the FFT (≈37 pJ, Eq. (84)); $P_0$ the fixed overhead (≈3 W); and $N_{\rm ch}=\dot N(E'/P_{\rm ch}+2\tau)$ the channel count (Eq. (101)). While photons set the window, $T_u=E'/(2P_{\rm ch})$ and $N_{\rm samp}=5R/\Delta R+5f_DT_u$ (Eq. (98)).

- **The useful-light term does not depend on how the light is split among channels.** It is the photon budget, $\dot N E'$ of useful optical power, divided by the laser efficiency. More power per channel reduces the number of channels, but it cannot reduce this term.
- **Only the channel terms depend on $P_{\rm ch}$.** Substituting $N_{\rm ch}$ and $N_{\rm samp}$ gives $P_{\rm elec}=\dot N[E'/\eta_{\rm WPE}+5(R/\Delta R)e_s+2\tau P_{\rm an}]+2\tau\dot NP_{\rm ch}/\eta_{\rm WPE}+\dot NE'(P_{\rm an}+2.5f_De_s)/P_{\rm ch}+P_0$. The dead-time light grows with $P_{\rm ch}$, while the analog power and the Doppler share of the samples fall as $1/P_{\rm ch}$. Setting the derivative with respect to $P_{\rm ch}$ to zero gives the optimum power per channel,

$$P_{\rm ch}^{*}=\sqrt{\frac{\eta_{\rm WPE}\,E'\,(P_{\rm an}+2.5f_De_s)}{2\tau}}, \tag{9008}$$

  at which the two $P_{\rm ch}$-dependent terms are equal, so the minimum power is

$$P_{\rm elec,min}=\dot N\left[\frac{E'}{\eta_{\rm WPE}}+5\,\frac{R}{\Delta R}\,e_s+2\tau P_{\rm an}+2\sqrt{\frac{2\tau\,E'\,(P_{\rm an}+2.5f_De_s)}{\eta_{\rm WPE}}}\,\right]+P_0 . \tag{9009}$$

- **Numbers for 10 Mpts/s at 300 m and 15 cm** [E], with $E'=0.45$ µJ, $\eta_{\rm WPE}=0.15$, $P_{\rm an}=10$ mW, $e_s=37$ pJ, $f_D=90$ MHz, $\tau=2.0$ µs and $P_0=3$ W:
  - $P_{\rm an}+2.5f_De_s=10\ {\rm mW}+2.5\times9\times10^{7}\ {\rm s^{-1}}\times37\times10^{-12}\ {\rm J}=10+8.3=18.3$ mW.
  - Eq. (9008): $P_{\rm ch}^{*}=\sqrt{0.15\times0.45\times10^{-6}\times0.0183/(4\times10^{-6})}=17.6$ mW, close to the 16 mW silicon limit. Then $T_u=0.45\ \mu{\rm J}/(2\times17.6\ {\rm mW})=12.8$ µs, $T_c=14.8$ µs, $B_{\rm tot}=1.16$ GHz, $\kappa=7.8\times10^{13}$ Hz/s, $f_s=2.5\times(156+90)\ {\rm MHz}=0.62$ GS/s and $N_{\rm ch}=10^{7}\times(25.6+4.0)\ \mu{\rm s}=296$.
  - Eq. (9009): useful light $10^{7}\times0.45\ \mu{\rm J}/0.15=30$ W; range samples $10^{7}\times5\times2{,}000\times37\ {\rm pJ}=3.7$ W; fixed analog share $10^{7}\times4\ \mu{\rm s}\times10\ {\rm mW}=0.4$ W; the two channel terms $2\times4.7=9.4$ W, where $2\tau\dot NP_{\rm ch}^{*}/\eta_{\rm WPE}=4\times10^{-6}\times10^{7}\times0.0176/0.15=4.7$ W; overhead 3 W. **Total ≈46 W, of which ≈65% is the useful light.**

| $P_{\rm ch}$ | Channels | $T_u$ | $B_{\rm tot}$ | $f_s$ | Useful light | Dead-time light | Analog | ADC and FFT | Total |
|---|---|---|---|---|---|---|---|---|---|
| 16 mW | 321 | 14.1 µs | 1.14 GHz | 0.58 GS/s | 30.0 W | 4.3 W | 3.2 W | 6.0 W | 46.5 W |
| 17.6 mW (optimum) | 296 | 12.8 µs | 1.16 GHz | 0.62 GS/s | 30.0 W | 4.7 W | 3.0 W | 5.8 W | 46.5 W |
| 30 mW | 190 | 7.5 µs | 1.27 GHz | 0.89 GS/s | 30.0 W | 8.0 W | 1.9 W | 5.0 W | 47.9 W |
| 100 mW (needs ≥2.5 GS/s ADCs) | 85 | 2.25 µs | 1.89 GHz | 2.45 GS/s | 30.0 W | 26.7 W | 0.9 W | 4.1 W | 64.6 W |

*How the table is computed* [E], Eq. (9007) term by term, each total including $P_0=3$ W:
- Channels $N_{\rm ch}=\dot N(E'/P_{\rm ch}+2\tau)$: at 30 mW, $10^{7}\times(15+4)\ \mu{\rm s}=190$.
- Dead-time light $2\tau\dot NP_{\rm ch}/\eta_{\rm WPE}$: at 30 mW, $4\times10^{-6}\times10^{7}\times0.030/0.15=8.0$ W.
- Analog $N_{\rm ch}\times10$ mW; ADC and FFT $\dot N(10{,}000+5f_DT_u)\times37$ pJ: at 30 mW, $10^{7}\times(10{,}000+3{,}375)\times37\ {\rm pJ}=4.95$ W.
- The 100 mW row keeps $e_s=37$ pJ, which flatters it: faster converters have a poorer figure of merit (item (c)).

**What moves the total** [E], from Eq. (9009):
- **Photons per point, $E'$:** it enters the dominant term linearly and the channel terms as a square root. Halving it (the parity case, subsection 5) saves $15+9.4\times(1-1/\sqrt2)=17.7$ W.
- **Laser linewidth, through $\eta_{\rm coh}$:** at 300 m a 10 kHz laser ($E'=0.51$ µJ) gives ≈51 W, a 42 kHz laser ($E'=0.76$ µJ) ≈70 W and a 100 kHz laser ($E'=1.58$ µJ) ≈130 W, against ≈46 W with no coherent loss. Worked (100 kHz): useful light $10^{7}\times1.58\ \mu{\rm J}/0.15=105$ W, channel terms $2\times10^{7}\times\sqrt{4\times10^{-6}\times1.58\times10^{-6}\times0.0183/0.15}=17.6$ W, plus $3.7+0.4+3$ W.
- **Wall-plug efficiency:** doubling $\eta_{\rm WPE}$ to 0.30 saves the same ≈18 W as halving $E'$, since both enter as $E'/\eta_{\rm WPE}$.
- **Channel electronics:** halving $P_{\rm an}$ and $e_s$ together saves ≈4.8 W: $1.85$ W of range samples, $0.2$ W of fixed analog power, and $9.4\times(1-1/\sqrt2)=2.75$ W of channel terms.
- **A faster or wider-tuning laser:** nothing, while photons set the window (item (g)).
- **More power per channel:** nothing, or worse. The optimum is ≈15–25 mW; 100 mW per channel costs ≈18 W more, all of it dead-time light.

**So is it just a matter of more optical power?** Partly, in the sense that matters.
- **The useful light itself is large and expensive.** FMCW needs $\dot N E'=10^{7}\times0.45\ \mu{\rm J}=4.5$ W of useful CW light for 10 Mpts/s at 300 m even with a perfect laser, ≈5.2 W as emitted at the optimum, and each watt costs ≈7 W of electrical power at 15% wall-plug efficiency. That light and its heat are the binding problem.
- **More power *per channel* is not the lever.** It only trades receivers against dead-time light, and past ≈35 mW it runs into the ADC floor (item (g)).
- **The levers are fewer photons per point and cheaper photons:** a smaller $E'$ (single-mode collection, speckle diversity, coherence) and a higher $\eta_{\rm WPE}$. Chirp speed, tuning range and beam steering are not the limits at these channel powers.
- **Against ToF, FMCW's photon handicap shrinks with range.** The same 940 nm SPAD ToF model needs $73\ {\rm nJ}\times(300/200)^2\times10^{7}=1.6$ W of useful light at 300 m with a fixed 25 mm lens. The FMCW-to-ToF photon ratio therefore falls from $0.30/0.073=4.1$ at 200 m to $4.5/1.6=2.7$ at 300 m, because coherent energy grows as $R$ and direct-detection energy as $R^2$ (subsection 1(f)).

**Summary of the dwell.**
- At 200 m, with 16–30 mW per channel, the photon budget dominates: 8–21 µs per point, i.e. 47–130 kpts/s per channel.
- The round trip adds a fixed 2.67 µs and caps any channel at ≈375 kpts/s.
- The useful window is the largest of four floors (Eq. (9006)): photons, ADC rate, laser chirp rate and laser tuning range. At ≤30 mW per channel photons win, so a faster or wider-tuning laser does not raise the point rate; the ADC binds next (above ≈35 mW per channel with 1 GS/s converters at 300 m).
- Scanning caps the ramp at $\theta_b/\Omega$ (Eq. (100)). Linewidth does not cap it but multiplies every point's energy by $1/\eta_{\rm coh}$ (Eq. (99)).
- In practice, then, one coherent channel at 200 m delivers at most ≈375 kpts/s, and far fewer at realistic power, so a sensor that needs millions of points per second must run many channels in parallel (subsection 3).
