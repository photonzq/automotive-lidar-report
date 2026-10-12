## C7b. Can FMCW win? The binding constraint, what beam steering can and cannot do, and what would have to change

**Short answer** [E unless tagged].
- **Per joule of emitted light, FMCW buys ≈4× fewer sampled points than 940 nm SPAD ToF. The reason is spatial, not temporal** (subsection 1).
  - In every architecture, the average optical power a sensor needs is its energy per point times its point rate, $P_{\rm opt}=E_{\rm opt}\dot N$. A ToF pulse's high peak power therefore buys no extra points by itself.
  - What differs is how much of the echo the receiver can use. A direct-detection pixel sums everything its lens collects from the cell: ≈491 mm² for a 25 mm lens, with hundreds of speckles averaged. A coherent receiver uses one spatial mode and one polarization: ≤65 mm² at 200 m for any collimated beam, with one fading speckle.
  - Result: ≈0.30 µJ per FMCW sample against ≈73 nJ per ToF point. To cover a whole 0.05° cell, FMCW needs ≈15 µJ, about 200× more.
- **The time format of the light matters for direct detection, not for coherent detection.**
  - ToF must pulse so that sunlight competes with the signal only inside a 1 ns timing bin. Spread evenly in time, the same echo would need ≈13× more energy.
  - The local oscillator (LO) already rejects sunlight, so CW light costs FMCW no photons, apart from the 12–35% it emits during the round-trip dead time.
- **What CW light does cost is hardware: the channel tax** (subsections 2–3).
  - A CW channel can carry only tens of milliwatts, so it must dwell $E_{\rm opt}/P_{\rm ch}+2\tau$ on each point. The simultaneous channels a sensor needs are therefore $N_{\rm ch}=P_{\rm opt}/P_{\rm ch}+2\tau\dot N$: ≈190 at 15 Mpts/s.
  - Each channel is an LO-matched coherent receiver: balanced photodiodes, a transimpedance amplifier (TIA), a GS/s analogue-to-digital converter (ADC) and an FFT, fed by its own CW light. It measures only ≈0.05–0.25 Mpts/s at 200 m.
  - A SPAD-SoC also runs hundreds of pixels in parallel, but each costs a few cents and ≈3 mW of receive power. A coherent channel costs ≈44 mW of receive power plus ≈200 mW of electrical power for its light (2026 central).
- **A better beam steerer cannot remove the channel tax** (subsection 4).
  - Existing mirrors already move each beam as fast as, or faster than, one coherent channel can use.
  - Faster scanning actively hurts FMCW (scanner-induced Doppler and walk-off, §C7).
  - No steerer changes the single-mode collection rule that fixes FMCW's photons per point.
- **Parity with ToF needs three things at once** (subsection 5):
  - a coherent receiver chip with ≥150 channels at ≤10–20 mW each, ADC and FFT included (a coherent counterpart of the SPAD-SoC);
  - CW lasers and amplifiers at ≥30% wall-plug efficiency at 105 °C;
  - an optical energy per point near 0.15 µJ at 200 m on a 10% target, which needs multimode or diversity reception.
  - Missing any one of them leaves a 15 Mpts/s sensor at ≈15–20 W against a 15 W target; today's central case is ≈41 W.
- **FMCW can win a market, not the point-rate race.** Its market is buyers who pay for per-point velocity and immunity at long range: trucks and highway L3. Through 2028 that is thousands of units a year, against millions for ToF (§B4).

### 1. How many points one joule of light buys, by architecture

**One equation covers every architecture.** A point is measured when the receiver collects enough signal photoelectrons, $n_{\rm req}$, to pass its detection threshold.
- For a Lambertian target of reflectance $\rho$ that fills the sample, a fraction $\rho A_{\rm eff}/(\pi R^2)$ of the transmitted light reaches the receiver's effective collecting area $A_{\rm eff}$.
- A fraction $\eta$ of the arriving photons becomes photoelectrons.
- The optical energy that must be sent out per point is therefore
$$E_{\rm opt}=\frac{n_{\rm req}\,E_{\rm ph}\,\pi R^2}{\rho\,A_{\rm eff}\,\eta},\qquad E_{\rm ph}=\frac{hc}{\lambda},$$
and one joule of light buys $1/E_{\rm opt}$ points.
- The sensor's average optical power is $P_{\rm opt}=E_{\rm opt}\dot N$, whatever the time format of the light. At 15 Mpts/s:
  - SPAD ToF: $73\ {\rm nJ}\times15\times10^{6}\ {\rm s^{-1}}=1.1$ W;
  - FMCW: $0.30\ \mu{\rm J}\times15\times10^{6}\ {\rm s^{-1}}=4.5$ W.
- A ToF pulse of a few hundred nJ at ≈100 W peak simply delivers its share of that average, either by lighting a line of pixels at once or as one of several shots accumulated per point.

**The architecture enters through $A_{\rm eff}$, $n_{\rm req}$ and $\eta$.** How the light is distributed in time, and how it is distributed over the target, enter through *different* terms for the two detection principles.

**(a) Direct detection (SPAD, SiPM or APD ToF): the lens collects everything, and timing sets how many counts are needed.**
- **Collection.** The pixel sums all the light its lens gathers from its cell. $A_{\rm eff}$ is therefore the lens area, however the transmitted light is spread over the cell: for a 25 mm lens, $A_{\rm eff}=\pi(12.5\ {\rm mm})^2=491$ mm². The pixel accepts hundreds of speckle modes at once (§C10.3a), so the echo does not fade.
- **Counts needed, and why pulses matter here.** Sunlight reflected by the target reaches the pixel along with the signal. A direct detector can separate the two only by *when* photons arrive. So the only competition for the signal is the background that falls in the signal's own time bin,
$$\bar n_{\rm bg,bin}=B\,t_{\rm bin}\,N_{\rm shots},$$
where $B$ is the background count rate, $t_{\rm bin}$ the bin width and $N_{\rm shots}$ the number of shots accumulated per point.
  - **In the §C7a model:** a macro-pixel in bright sun counts $B=3\times10^{8}$ s⁻¹. It listens for the 20.8 µs column time per point (≈10 shots of ≈2 µs, §C6) with 29% dead time. That gives $3\times10^{8}\times20.8\times10^{-6}\times0.71\approx4{,}430$ background events per point.
  - **Per bin:** spread over the ≈2,000 histogram bins of 1 ns (≈300 m of range), that is $4{,}430/2{,}000\approx2.2$ counts per bin. The formula gives the same: $3\times10^{8}\times10^{-9}\times10\times0.71=2.1$. So ≈25 signal counts in one bin stand out clearly.
  - **The same energy spread evenly in time,** as with CW light, would have to stand out against all 4,430 events. At 5 standard deviations that takes $5\sqrt{4{,}430}\approx330$ counts: ≈13× more energy per point, before any requirement on ranging precision.
  - This is why direct-detection lidars pulse. It is also why AMCW ToF cameras stay short-range outdoors (§C0 subsection 9), and why flash designs, which accumulate many weak shots per point (raising $N_{\rm shots}$), lose range in sunlight.
- **Amplifier noise (linear-mode APDs).** A linear APD with a TIA adds electronic noise to every shot, so its threshold is set shot by shot. Splitting the energy across shots then costs sensitivity. Illustrative 1,550 nm case [E], with assumed parameters:
  - **Assumptions:** APD gain $M=10$; ionization ratio $k=0.45$, so excess noise factor $F=kM+(1-k)(2-1/M)=5.5$; TIA noise $2\ {\rm pA/\sqrt{Hz}}$ over 250 MHz ($i_n=32$ nA rms); a 4 ns pulse; a single-shot signal-to-noise ratio of 7.
  - **Solve** $M I_s=7\sqrt{2qM^2F I_s B+i_n^2}$ for the primary signal current $I_s=nq/t_p$. This gives $n\approx890$ photoelectrons, some 35× the SPAD's 25 counts.
  - **Result:** with quantum efficiency 0.8 and optics 0.5, $E_{\rm opt}\approx0.73$ µJ at 200 m and 10%. It is 0.6–0.9 µJ for TIA noise of 1.5–3 pA/√Hz.
  - 1,550 nm ToF sensors make up for this with larger apertures and the µJ-class pulses that 1,550 nm eye-safety limits allow (§C4c), not with more points per joule.

**(b) Coherent detection (FMCW, or pulsed coherent): the LO removes the background, and the spot size sets the collection.**
- **Background.** The receiver responds only to light in the LO's spatial mode and polarization, within the beat bandwidth. Worked number:
  - Sunlight at 1,550 nm (≈0.25 W m⁻² nm⁻¹) on a 10% target gives radiance $L=\rho E_\lambda/\pi\approx8\times10^{-3}$ W m⁻² sr⁻¹ nm⁻¹.
  - One mode has étendue $\lambda^2=2.4\times10^{-12}$ m² sr. A 1 GHz beat bandwidth is $\Delta\lambda=\lambda^2\Delta f/c=0.008$ nm. One polarization halves the total.
  - Collected sunlight: $8\times10^{-3}\times2.4\times10^{-12}\times0.008\times0.5\approx8\times10^{-17}$ W, i.e. ≈600 photons per second, or 0.006 photons in a 10 µs dwell. The LO's own shot noise is equivalent to about one photon in *every* FFT bin.
  - **So coherent detection gains nothing from concentrating light in time.** CW costs it no photons per point, apart from the dead time in (e).
- **Collection: one mode, and it depends on where the light lands.** A single-mode receiver collects the target's radiance times $\lambda^2$. The smaller the illuminated spot, the higher the radiance, so the collecting area is set by the beam footprint, not by the lens. For a Gaussian beam of radius $w$ at the target, the §C10.3b model (truncation factor $t$, one polarization) gives
$$A_{\rm mode}=\frac{t^2\,\lambda^2R^2}{2\pi w^2}.$$
  - **A collimated 20 mm aperture** ($w_0=9$ mm, $t^2=0.84$) spreads to $w(200\ {\rm m})=14.2$ mm. Then $A_{\rm mode}=0.84\times(1.55\times10^{-6})^2\times200^2/(2\pi\times0.0142^2)=64$ mm², about 1/8 of the ToF lens area.
  - **A bigger collimated aperture does not help.**
    - $w^2=w_0^2+(\lambda R/\pi w_0)^2$ is smallest, at $2\lambda R/\pi$, when $w_0=\sqrt{\lambda R/\pi}=9.9$ mm (a ≈22 mm aperture).
    - The ceiling is therefore $A_{\rm mode}\le t^2\lambda R/4=65$ mm² at 200 m. A 40 mm collimated aperture gives 36 mm², and an 80 mm one gives 10 mm², because their beams are wider at 200 m.
    - Only focusing on the target range raises the ceiling, and only near that range.
  - **The price is coverage.** The 14 mm beam's footprint, $\pi w^2=6.3\times10^{-4}$ m², is 2.1% of a 0.05° cell at 200 m, whose area is $(8.7\times10^{-4}\times200\ {\rm m})^2=0.030$ m² (§C10.3a). Widening the beam to fill the cell cuts $A_{\rm mode}$ by the same factor of 48, to 1.3 mm². Covering the cell costs ≈15 µJ either way, as one wide sample or as 48 narrow ones of 0.30 µJ.
- **Counts needed.** One mode means one speckle, whose intensity fades with exponential (Rayleigh) statistics. Detecting it with 90% probability therefore needs a higher mean signal than a pixel that averages hundreds of speckles: 30 photoelectrons in the §C7a model, and 50 in Waymo's analysis with four averaged speckles [P].

**(c) Result: points per joule of emitted light, 200 m, 10% target** [E; §C7a parameters unless stated]

| Architecture | Effective collecting area | Photoelectrons needed | $\eta$ | Optical energy per point | Points per optical joule |
|---|---|---|---|---|---|
| 940 nm SPAD or SiPM dToF, scanned or line-flash, 25 mm lens | 491 mm² (whole lens) | 25 counts | 0.185 | 73 nJ | $1.4\times10^{7}$ |
| 1,550 nm pulsed ToF, linear InGaAs APD, same lens (illustrative, (a)) | 491 mm² | ≈890 | 0.40 | ≈0.73 µJ | $1.4\times10^{6}$ |
| 1,550 nm FMCW, collimated 20 mm monostatic beam, per sample | 64 mm² (one mode) | 30 | 0.25 | 0.30 µJ | $3.3\times10^{6}$ |
| FMCW at the parity target (subsection 5) | — | — | — | 0.15 µJ | $6.7\times10^{6}$ |
| FMCW with the beam widened, or 48 samples tiled, to cover a whole 0.05° cell | 1.3 mm² | 30 | 0.25 | ≈15 µJ | $6.8\times10^{4}$ |
| AMCW (iToF) camera outdoors at long range | whole lens | set by sunlight integrated over the exposure, ≈4×10⁴× a scanner's (§C0 subsection 9) | — | not viable | — |

*How the numbers are derived* [E]:
- **Energy column:** $E_{\rm opt}=n_{\rm req}E_{\rm ph}\pi R^2/(\rho A_{\rm eff}\eta)$, with $\pi R^2=1.26\times10^{5}$ m², $\rho=0.1$, and $E_{\rm ph}=2.11\times10^{-19}$ J at 940 nm or $1.28\times10^{-19}$ J at 1,550 nm. Worked example (SPAD row): $25\times2.11\times10^{-19}\times1.26\times10^{5}/(0.1\times4.91\times10^{-4}\times0.185)=7.3\times10^{-8}$ J.
- **$\eta$:**
  - ToF: optics 0.5 × photon detection efficiency 0.37;
  - APD: optics 0.5 × quantum efficiency 0.8;
  - FMCW: the §C7a common optical × detector × mixing efficiency (the mode and polarization factors are in $A_{\rm mode}$).
- **Last column:** $1/E_{\rm opt}$; for example $1/(7.3\times10^{-8}\ {\rm J})=1.4\times10^{7}$ points per joule.
- **Full-cell FMCW row:** $0.30\ \mu{\rm J}\times64/1.32=14.6$ µJ.

**(d) Why FMCW buys ≈4× fewer sampled points per joule than SPAD ToF.** The ratio of the two energies splits term by term:
$$\frac{E_{\rm FMCW}}{E_{\rm ToF}}=\underbrace{\frac{491}{64}}_{\rm collection}\times\underbrace{\frac{30}{25}}_{\rm fading}\times\underbrace{\frac{940}{1{,}550}}_{\rm photon\ energy}\times\underbrace{\frac{0.185}{0.25}}_{\rm efficiency}=7.7\times1.2\times0.61\times0.74=4.15.$$
- **Collection (7.7×):**
  - 1.56× of this comes from the model's larger ToF lens ($(25/20)^2$).
  - 4.9× comes from single-mode reception: one polarization, the Gaussian mode shape, and near-field spreading of a 20 mm beam at 200 m ($314\ {\rm mm^2}/64\ {\rm mm^2}=4.9$). Waymo puts this penalty at ≈6 dB [P].
- **1,550 nm helps (0.61×):** each 1,550 nm photon carries only 0.61× the energy of a 940 nm one, so a joule contains more of them.
- **Per fully covered cell the gap is ≈200×** ($14.6\ \mu{\rm J}/73\ {\rm nJ}$).
- **Which figure to use:** the per-sample figure is the fair one for objects larger than the sample spacing, such as cars. The per-cell figure applies to objects smaller than a cell, such as debris (§C10.3a).

**(e) What CW light does cost FMCW in photons.** Two things, both modest at today's channel powers:
- **Round-trip dead time.** A CW channel keeps transmitting during the first $\tau$ of each ramp, before any usable echo exists (subsection 2(a)).
  - The transmitted energy per point is $E_{\rm opt}T_{\rm dwell}/T_{\rm int}$. At 16–30 mW per channel, a share $2\tau/T_{\rm dwell}$ of 12–35% of it is emitted during the dead time and wasted (subsection 2 table).
  - A pulsed laser stays dark while it waits.
- **Coherence cap.** A ramp can integrate coherently for at most $T_u\approx1/(2\Delta\nu)$ (subsection 2(e)), so one ramp can collect at most $P_{\rm ch}/(2\Delta\nu)$ of energy.
  - At 30 mW and 100 kHz linewidth that is $0.03\ {\rm W}/(2\times10^{5}\ {\rm Hz})=0.15$ µJ, or 0.30 µJ per up–down pair: exactly the central requirement.
  - At the 16 mW silicon limit it is 0.16 µJ per pair. Reaching 0.30 µJ then needs a narrower laser, or several chirp pairs averaged incoherently, which add up less efficiently than one coherent integration.

**(f) Range dominates everything.**
- **Direct detection:** $E_{\rm opt}\propto R^2/\rho$. The same SPAD receiver needs only $73\ {\rm nJ}\times(10/200)^2=0.18$ nJ per point at 10 m, i.e. 400× more points per joule. This is why phone dToF modules and ToF cameras deliver many points for milliwatts (§B8, §C0 subsection 9).
- **Coherent:** for a collimated beam at its optimum aperture, $A_{\rm mode}\propto R$, so $E_{\rm opt}\propto R$. The footprint's share of a fixed angular cell, however, falls as $1/R$.

**(g) What the pulse format does change: occupancy, not photons.** A channel is busy for as long as it takes to deliver $E_{\rm opt}$ at its peak power, plus the round trip. That sets how many channels must run in parallel (subsections 2–3). It does not set how many joules the scene needs.

### 2. What sets the dwell of one FMCW point

**Notation.** An FMCW channel sweeps the optical frequency linearly over one "ramp" (chirp) of duration $T_c$ at chirp rate $\kappa$ (Hz/s). The echo from range $R$ returns after the round trip

$$\tau=\frac{2R}{c},\qquad \tau(200\ {\rm m})=\frac{2\times200\ {\rm m}}{3\times10^{8}\ {\rm m/s}}=1.33\ \mu{\rm s}.$$

The standard measurement uses an up-ramp and a down-ramp, because the pair separates range from Doppler (§C0 subsection 2). One point therefore takes $T_{\rm dwell}=2T_c$.

**(a) The round trip removes $\tau$ from every ramp.** The echo produces a clean beat with the LO only once it has arrived. During the first $\tau$ of each ramp, what returns is the tail of the previous ramp, which has the opposite slope and is discarded. The useful window per ramp is therefore

$$T_u=T_c-\tau .$$

Two consequences follow.
- **Resolution comes from the useful window only.**
  - The frequency swept while the beat exists is $B_{\rm eff}=\kappa T_u$, and range resolution is $\Delta R=c/(2B_{\rm eff})$.
  - Keeping $\Delta R=15$ cm needs $B_{\rm eff}=c/(2\Delta R)=3\times10^{8}/(2\times0.15)=1$ GHz within $T_u$.
  - The total sweep is larger: $B_{\rm tot}=\kappa T_c=B_{\rm eff}\,T_c/T_u$. For $T_u=2$ µs, $T_c=3.33$ µs and $B_{\rm tot}=1\ {\rm GHz}\times3.33/2=1.67$ GHz.
- **There is a hard ceiling on point rate per channel.** Even with infinite laser power ($T_u\to0$), $T_{\rm dwell}\ge2\tau$. At 200 m that is 2.67 µs, i.e. at most $1/(2.67\ \mu{\rm s})\approx375$ kpts/s per channel.

**(b) The photon budget sets the rest, and it is the binding term.**
- **Energy needed.** Subsection 1 gives $E_{\rm opt}=0.30$ µJ per point at 200 m and 10% for the central 2026 case, and 0.15 µJ in the optimistic parity case (subsection 5).
- **Integration time.** A channel transmitting a constant power $P_{\rm ch}$ must integrate for $T_{\rm int}=E_{\rm opt}/P_{\rm ch}$ of useful window, summed over both ramps: $2T_u=T_{\rm int}$. With $T_c=T_u+\tau$:
  $$\boxed{\,T_{\rm dwell}=2T_c=\frac{E_{\rm opt}}{P_{\rm ch}}+2\tau\,},\qquad \dot N_{\rm ch}=\frac{1}{T_{\rm dwell}}.$$
- **Worked example:** $E_{\rm opt}=0.30$ µJ and $P_{\rm ch}=30$ mW give $T_{\rm int}=0.30\times10^{-6}/0.030=10$ µs. Then $T_{\rm dwell}=10+2.67=12.7$ µs and $\dot N_{\rm ch}=1/12.7\ \mu{\rm s}=79$ kpts/s.
- **What limits $P_{\rm ch}$.** It cannot simply be raised:
  - *Heat.* CW sources plus semiconductor optical amplifiers (SOAs) run at ≈15–20% wall-plug efficiency, so each watt of light costs 4–6 W of heat (§C7a(b)).
  - *Waveguide power handling.* Silicon waveguides saturate near 16 mW through two-photon and free-carrier absorption (Pointcloud Methods, §C7a(b)); higher power needs SiN or III-V paths.
  - *Per-beam eye safety at 1,550 nm.* This is secondary; §C7a concludes that heat is the practical ceiling.
- **The share of the laser's energy emitted during the round-trip windows** is $2\tau/T_{\rm dwell}$, and it is wasted (subsection 1(e)). In the example, $2.67/12.7=21\%$.

| $P_{\rm ch}$ | $T_{\rm dwell}$ at 0.30 µJ | Per-channel rate | Wasted share | $T_{\rm dwell}$ at 0.15 µJ | Per-channel rate | Wasted share |
|---|---|---|---|---|---|---|
| 16 mW (silicon limit) | 21.4 µs | 47 kpts/s | 12% | 12.0 µs | 83 kpts/s | 22% |
| 30 mW | 12.7 µs | 79 kpts/s | 21% | 7.7 µs | 130 kpts/s | 35% |
| 100 mW | 5.7 µs | 176 kpts/s | 47% | 4.2 µs | 240 kpts/s | 64% |
| Unlimited | → 2.67 µs | → 375 kpts/s | → 100% | → 2.67 µs | → 375 kpts/s | → 100% |

*How the table is computed* [E]:
- $T_{\rm dwell}=E_{\rm opt}/P_{\rm ch}+2\tau$, with $2\tau=2.67$ µs at 200 m.
- Rate $=1/T_{\rm dwell}$; wasted share $=2\tau/T_{\rm dwell}$.
- Example row (100 mW, 0.15 µJ): $0.15\ \mu{\rm J}/0.1\ {\rm W}=1.5$ µs, plus 2.67 µs, gives 4.17 µs. The rate is $1/4.17\ \mu{\rm s}=240$ kpts/s, and the wasted share is $2.67/4.17=64\%$.

**At the powers realistic for integrated photonics (16–30 mW), the photon term is 2–7 times the round-trip term.** The ratio $T_{\rm int}/2\tau$ is 3.5–7.0 at 0.30 µJ and 1.9–3.5 at 0.15 µJ. So the dwell mostly measures how much CW light one channel can carry.

**(c) Readout bandwidth makes short chirps expensive but does not forbid them.**
- **Beat frequency.** The largest beat, at maximum range and closing speed, is
  $$f_{b,\max}=\kappa\tau+f_D=\frac{B_{\rm eff}}{T_u}\,\tau+\frac{2v}{\lambda}.$$
  At 70 m/s and 1,550 nm, $f_D=2\times70/1.55\times10^{-6}=90$ MHz.
- **Sampling rate.** Sampling at 2.5× the maximum beat frequency (Nyquist plus ≈25% margin), $f_s\approx2.5\,f_{b,\max}$, at $R=200$ m and $B_{\rm eff}=1$ GHz:

| Useful window $T_u$ | Chirp $T_c=T_u+\tau$ | Total sweep $B_{\rm tot}$ | Range beat $B_{\rm eff}\tau/T_u$ | $f_{b,\max}$ with Doppler | Sampling rate $f_s$ |
|---|---|---|---|---|---|
| 10 µs | 11.3 µs | 1.13 GHz | 133 MHz | 223 MHz | 0.56 GS/s |
| 5 µs | 6.3 µs | 1.27 GHz | 267 MHz | 357 MHz | 0.89 GS/s |
| 2 µs | 3.3 µs | 1.67 GHz | 667 MHz | 757 MHz | 1.9 GS/s |
| 1 µs | 2.3 µs | 2.33 GHz | 1,333 MHz | 1,423 MHz | 3.6 GS/s |

  *Worked row* (5 µs): $1\ {\rm GHz}\times1.33\ \mu{\rm s}/5\ \mu{\rm s}=267$ MHz; adding 90 MHz gives 357 MHz; $\times2.5=0.89$ GS/s.
- **Samples per point barely depend on the chirp length.** Sampling both useful windows gives
  $$N_s=f_s\times2T_u=5B_{\rm eff}\tau+5f_DT_u=5\frac{R}{\Delta R}+5f_DT_u ,$$
  using $B_{\rm eff}\tau=(c/2\Delta R)(2R/c)=R/\Delta R$.
  - At 200 m and 15 cm with $T_u=5$ µs: $N_s=5\times200/0.15+5\times90\times10^{6}\times5\times10^{-6}=6{,}670+2{,}260\approx8{,}900$ samples per point.
  - At 300 m (the §C7a case), it is $10{,}000+2{,}260\approx12{,}300$.
  - A faster ADC simply runs for a shorter time. At the §C7a central ≈37 pJ per sample (ADC plus FFT), the receiver spends $8{,}900\times37\ {\rm pJ}\approx0.33$ µJ per point at 200 m, and $12{,}300\times37\ {\rm pJ}\approx0.45$ µJ at 300 m, before TIA and bias power.
- **Why short chirps are still costly in practice** [I/U]:
  - ADC energy per conversion step worsens above about 1 GS/s (the Murmann ADC survey trend).
  - Wider-band TIAs add noise and power.
  - All of this is replicated in every channel.
  - So the readout makes $T_u$ below about 2 µs (≥1.9 GS/s per channel at 200 m) expensive at scale, but it is not a physical floor.

**(d) The laser's chirp speed and linearity: a cost, not the floor.**
- **Chirp rate required:** $\kappa=B_{\rm eff}/T_u$, e.g. $1\ {\rm GHz}/5\ \mu{\rm s}=2\times10^{14}$ Hz/s, or $10^{15}$ Hz/s at 1 µs.
- **Linearity sets range blur.** Because $f_b=\kappa\tau\propto R$, a fractional chirp non-linearity $\varepsilon$ smears the beat by $\approx\varepsilon f_b$ and the range by $\delta R\approx\varepsilon R$. At 200 m, $\varepsilon=10^{-3}$ gives $\delta R\approx0.2$ m, larger than the 15 cm resolution; $\varepsilon=10^{-4}$ gives 2 cm.
- **Directly modulated DFB lasers** tune through two competing effects, fast carrier tuning and slower thermal tuning, which cross over at roughly 1–10 MHz of modulation frequency [U].
  - A linear ramp of a few µs has harmonic content up to tens of MHz, so pre-distortion or feedback must stay accurate across that crossover. It gets harder as $T_c$ shrinks.
  - Waymo reports a pre-distorted DFB holding <100 kHz error over 1 GHz, i.e. $\varepsilon<10^{-4}$ [P] (§C7a(f)).
- **Electro-optic chirping** (thin-film lithium niobate, single-sideband modulators) or an optical phase-locked loop reaches $10^{15}$–$10^{16}$ Hz/s linearly. The laser's ability to chirp is therefore not the fundamental floor; it sets the cost of reaching short, linear chirps.

**(e) Laser linewidth caps the *useful* chirp length from above.**
- **Coherent peak fraction.** The beat between the echo and the LO carries the laser's phase noise accumulated over the delay $\tau$. For a Lorentzian linewidth $\Delta\nu$, the phase difference has variance $2\pi\Delta\nu\tau$. The fraction of beat power that stays in a coherent peak is therefore
  $$F_{\rm coh}\approx e^{-2\pi\Delta\nu\,\tau}.$$
  The rest spreads over ≈$2\Delta\nu$.
- **Examples at 200 m:**
  - a 100 kHz laser gives $2\pi\times10^{5}\times1.33\times10^{-6}=0.84$ and $F_{\rm coh}=e^{-0.84}=0.43$: workable;
  - a 1 MHz laser gives $e^{-8.4}=2\times10^{-4}$: the coherent peak is gone.
- **Consequence.** Once the FFT bin $1/T_u$ is narrower than the phase-noise spread $2\Delta\nu$, a longer window no longer sharpens the peak. So $T_u\gtrsim1/(2\Delta\nu)$ buys little: ≈5 µs for a 100 kHz laser. Long, photon-rich chirps need narrower lasers (§C7; subsection 1(e)).

**(f) Scanning also caps the chirp from above.** The chirp must end before the beam sweeps across its own width, $T_c\lesssim\theta_b/\Omega$ (§C7).
- For $\theta_b=0.05°=8.7\times10^{-4}$ rad and a 5 µs chirp, $\Omega\lesssim8.7\times10^{-4}/5\times10^{-6}=175$ rad/s ≈ $10^4$ °/s.
- Target motion during a chirp is negligible: 50 m/s × 10 µs = 0.5 mm.

**Summary of the dwell.**
- At 200 m, with 16–30 mW per channel, the photon budget dominates: 8–21 µs per point, i.e. 47–130 kpts/s per channel.
- The round trip adds a fixed 2.67 µs and caps any channel at ≈375 kpts/s.
- Readout and laser make chirps below about 2 µs expensive.
- Linewidth and scanning cap useful chirps at about 5 µs (for a 100 kHz laser) and at $\theta_b/\Omega$.

### 3. The channel tax: channels, power and receivers

**Channels follow from average power.** Each coherent channel measures one point per dwell, so a sensor that must deliver $\dot N$ points per second needs
$$N_{\rm ch}=\dot N\,T_{\rm dwell}=\dot N\left(\frac{E_{\rm opt}}{P_{\rm ch}}+2\tau\right)=\frac{P_{\rm opt}}{P_{\rm ch}}+2\tau\dot N .$$
- The first term is the scene's average optical power (subsection 1) divided by the power one channel can carry. The second is the round-trip occupancy.
- Example: 15 Mpts/s at 0.30 µJ and 30 mW gives $4.5\ {\rm W}/0.03\ {\rm W}+2\times1.33\times10^{-6}\times15\times10^{6}=150+40=190$ channels. That equals $15\times10^{6}\times12.7\times10^{-6}$.
- **The watts are fixed by the scene; the channel count is fixed by the channel.** The scene needs only its average optical power, in any architecture. FMCW's problem is that this power must be split into CW channels of ≤30 mW, each with its own LO-matched receiver.

| Target point rate | Channels at 4 µs dwell | Channels at 10 µs dwell | Channels at the 30 mW / 0.30 µJ dwell (12.7 µs) |
|---|---|---|---|
| 2 Mpts/s (Aeries-class) | 8 | 20 | 25 |
| 10 Mpts/s | 40 | 100 | 127 |
| 15 Mpts/s (the parity case) | 60 | 150 | 190 |
| 41 Mpts/s (RoboSense EM4, ToF) | 164 | 410 | 520 |

*How the table is computed* [E]:
- $N_{\rm ch}=\dot N\,T_{\rm dwell}$; for example $41\times10^{6}\times4\times10^{-6}=164$.
- A 4 µs dwell is close to the lower practical end at 200 m. It implies $T_u=4/2-1.33=0.67$ µs per ramp, $f_s\approx5$ GS/s and ≈100 mW per channel at 0.15 µJ.

**ToF also runs hundreds of receive channels. The difference is what each one costs.**
- **ToF channel count.** A SPAD macro-pixel is occupied for its listening time, the 20.8 µs column time per point of the §C6/§C7a model (≈10 shots). So 15 Mpts/s keeps $15\times10^{6}\times20.8\times10^{-6}=312$ macro-pixels listening at once, for example one 312-pixel column.
- **Power per ToF channel.** At the §C7a central values:
  - receive: $15\times10^{6}\times60\ {\rm nJ}=0.9$ W, i.e. $0.9\ {\rm W}/312=2.9$ mW per macro-pixel;
  - laser: $15\times10^{6}\times0.37\ \mu{\rm J}=5.6$ W, i.e. ≈18 mW per macro-pixel.
  - Each macro-pixel is ≈30 µm of SPAD column plus a share of a time-to-digital converter and histogram SRAM: a few cents of silicon (§C7a(e)).
- **Power per FMCW channel.** With 190 channels:
  - receive: $15\times10^{6}\times0.56\ \mu{\rm J}=8.4$ W, i.e. ≈44 mW per channel;
  - light: each channel transmits 30 mW continuously, i.e. $0.030/0.15=200$ mW of electrical power at 15% wall-plug.
  - Each channel is an LO tap, a balanced photodiode pair, a TIA, a GS/s ADC and an FFT pipe.
- **So the per-channel electrical power is ≈245 mW for FMCW against ≈21 mW for ToF, ≈12× more.** The FMCW channel is also far larger and costlier.

**Optical and receiver power.**
- **Optical power** depends only on the energy per point, not on the dwell: $P_{\rm opt}=E_{\rm opt}\dot N=4.5$ W at 0.30 µJ, or 2.25 W at 0.15 µJ. The transmitted power is larger by the dead-time factor, e.g. $190\times30\ {\rm mW}=5.7$ W.
- **Brighter channels do not save watts.** They shorten the dwell and cut the channel count, which saves receiver chains, but they do not lower the watts per point. The round-trip waste even raises the transmitted energy (subsection 2 table).
- **Receiver power** is $P_{\rm rx}=\dot N E_{\rm rx}$.
  - The §C7a 2026 central value, at 300 m with the model's 10 µs dwell, is $E_{\rm rx}=12{,}300\times37\ {\rm pJ}+10\ {\rm mW}\times10\ \mu{\rm s}=0.46+0.10\approx0.56$ µJ per point (samples, plus TIA and bias).
  - At 15 Mpts/s that is $15\times10^{6}\times0.56\times10^{-6}=8.4$ W of receiver electronics, the same order as a whole 520-line ToF unit.

**Published products** (vendor figures, at different ranges). Electrical energy per point is $E=P/\dot N$ [E from P]:

| Sensor | Architecture | Point rate $\dot N$ | Power $P$ | $E=P/\dot N$ | Range at 10% |
|---|---|---|---|---|---|
| Hesai ATX | ToF, one mechanical axis | 3.84 Mpts/s | 8 W | $8/3.84\times10^{6}=2.1$ µJ | 230 m |
| Hesai AT128 | ToF, one mechanical axis | 1.536 Mpts/s | 13.5 W | $13.5/1.536\times10^{6}=8.8$ µJ | 210 m |
| LuminWave F1 | FMCW, on-chip antennas | ≈1.5 Mpts/s (implied) | <45 W | $\lesssim45/1.5\times10^{6}=30$ µJ | 250 m |
| Analog Photonics FS-4S | FMCW, OPA | 0.09 / 0.4 Mpts/s | 35 W | $35/0.09\times10^{6}=390$ / $35/0.4\times10^{6}=88$ µJ | 200 m in a 20° × 10° ROI / 80 m over 60° × 14° |

**Pointcloud's research array** is the only coherent array with a published energy figure. It reports ≈46 nJ *optical* per point at 65 m and 30% reflectivity, with coherent averaging [P].
- Optical energy per point scales as $R^2/\rho$ (subsection 1). Scaling to 200 m and 10% multiplies it by $(200/65)^2\times(0.30/0.10)=9.47\times3=28.4$.
- That gives $46\ {\rm nJ}\times28.4\approx1.3$ µJ optical per point: ≈4.4× the §C7a central 0.30 µJ, before any electrical conversion [E].

### 4. What beam steering can and cannot do for FMCW

**Steering is not the rate limiter.**
- **What one channel can use.** At 200 m, one channel can use at most $1/T_{\rm dwell}$ beam positions per second: 47–240 k with realistic power, never more than 375 k (subsection 2).
- **What steerers supply.** A steerer supplies $\Omega/\theta_b$ positions per second per beam:
  - a Falcon-class polygon at 45,600 °/s with a 0.05° beam gives $45{,}600/0.05=912{,}000$;
  - a resonant MEMS mirror at 188,500 °/s peak gives $188{,}500/0.05=3.8\times10^{6}$ (§C7 table);
  - the AT128's mirror, by comparison, visits only $1{,}200\times10=12{,}000$ columns per second per channel.
- **So a faster steerer buys nothing in points per second per channel.**

**Faster scanning actively hurts above a threshold.** The chirp must end before the beam crosses its own width: $\Omega\lesssim\theta_b/T_c=175$ rad/s ≈ $10^4$ °/s for 0.05° and 5 µs (subsection 2(f)). Above this, two things happen (§C7):
- scanner-induced Doppler spreads the beat over $\approx T_c\,\Omega D/\lambda$ FFT bins;
- receive walk-off costs signal.

Coherent designs therefore favour *slow* mechanical axes or step-and-stare.

**No steerer raises photons per point.** The coherent collecting area is set by the beam footprint at the target (subsection 1(b)):
- at most ≈65 mm² per sample for any collimated beam at 200 m;
- 1.3 mm² if the beam is widened to fill a 0.05° cell (equivalently $\lambda^2/\Omega_{\rm cell}=(1.55\times10^{-6})^2/(8.7\times10^{-4})^2=3.2$ mm² before the mode and polarization factors).

A steerer changes where the footprint goes, not how large it must be. A larger steered aperture only narrows each mode's angular acceptance, so the field then needs more samples or more channels. Only more *modes per sample*, i.e. more channels, raises the collection per cell, and that returns to the channel tax.

**What a steerer can buy (secondary, but real).**
1. **Random access and foveation.** FMCW can spend its scarce samples on tracked objects. Worked example [E]:
   - A 120° × 25° field is 3,000 deg². Put 80% of 2 Mpts/s on the 5% of it (150 deg²) that holds tracked objects. The density there is $1.6\times10^{6}/150=10{,}700$ pts/deg²/s, about 2× a uniform 15 Mpts/s ToF ($15\times10^{6}/3{,}000=5{,}000$), with velocity on every point.
   - The remaining 95% of the field (2,850 deg²) then gets $0.4\times10^{6}/2{,}850=140$ pts/deg²/s, $5{,}000/140\approx36\times$ sparser than ToF. That is where an unexpected small obstacle must be *found* (§C10.6).
   - Foveation therefore helps tracking, not first detection.
2. **Step-and-stare without a moving mirror.** This removes scanner Doppler and walk-off, which allows longer chirps. The trade is more photons per point for fewer points per second.
3. **Solid-state packaging and reliability.** This matters less than it once seemed, because motor-driven one-axis mirrors have qualified by the million (§C4d).

**Case study: the "photonic ski-jump"** [P: M. Saha, Y. H. Wen, A. S. Greenspon, M. Zimmermann et al. (MITRE, MIT, Sandia and others), "Nanophotonic waveguide chip-to-world beam scanning", *Nature* 651, 356–362 (12 Mar 2026), open access; read in full; copy in `refs/`].
- **What it is:** a 400 × 300 nm SiN waveguide on a ≈2 µm-thick AlN piezoelectric cantilever that curls ≈90° out of the chip plane, within <0.1 mm². It is made in a 200 mm CMOS foundry.
  - It emits a ≈0.5–0.66 µm mode (divergence half-angles 41° × 53°) and scans it resonantly at 1 kHz to >100 kHz.
  - Its quality factor is Q ≈ 10,000 in high vacuum against ≈5 at atmospheric pressure.
  - It is driven at 1–10 Vpp in vacuum and holds a DC position with ≈10 nW.
- **Its figure of merit:** 68.6 M spots s⁻¹ mm⁻², ">50-fold" state-of-the-art MEMS mirrors, "sufficient for one million pixels at 100 Hz from an approximately 1.5 mm diameter footprint". (Check: $68.6\times10^{6}\times\pi(0.75\ {\rm mm})^2=1.2\times10^{8}$ spots/s against $10^{6}\times100=10^{8}$ needed.)
- **Demonstrations:**
  - full-colour Lissajous image projection at 7–36 Hz;
  - addressing of silicon-vacancy qubits;
  - a 64-device array with <2% curvature spread;
  - a projected >1 gigaspot at kHz rates from <5 cm, given a further 10× in figure of merit.
- **Limitations the authors state:** vacuum packaging, no true random access, a curved scan trajectory, and possible nonlinearity or thermal loading at higher optical power.
- **Tested against lidar needs** [E]:
  - **Dwell per spot.** In a resonant raster at frequency $f$ with $N$ resolvable spots per line and two lines per period, the time on each spot is $t_{\rm spot}=1/(2fN)$. A 5 µs chirp per spot therefore allows at most $N_{\max}=1/(2fT_c)$.
    - At the lowest ≈1.3 kHz mode: $1/(2\times1{,}300\times5\times10^{-6})=77$ spots per line.
    - At the ≈4.9 kHz lateral mode: $1/(2\times4{,}900\times5\times10^{-6})=20$.
    - A 0.05°-class lidar needs ≈2,400 columns over 120°.
    - Off resonance the motion is small (≈29 µm of DC tip travel for ±50 V). Slowing the device to FMCW dwell times therefore sacrifices most of its range of motion.
  - **Monostatic receive.** In a focal-plane scanner, the echo images back onto the tip position at the moment of emission. Meanwhile the tip has moved $\Delta x=v\tau$, with peak speed $v=2\pi fA$.
    - With $A\approx50$ µm and $f\approx5$ kHz: $v=2\pi\times5{,}000\times50\times10^{-6}=1.6$ m/s.
    - Power coupling between two identical Gaussian modes offset by $\Delta x$ is $\eta=e^{-(\Delta x/w_0)^2}$, with mode radius $w_0\approx0.3$ µm.
    - At 20 m ($\tau=133$ ns): $\Delta x=0.21$ µm and $\eta=e^{-0.49}$, i.e. −2.1 dB.
    - At 50 m: $\Delta x=0.52$ µm and $\eta=e^{-3.0}$, i.e. −13 dB.
    - At 200 m: $\Delta x=2.1$ µm and $\eta=e^{-49}$, i.e. nothing.
    - It therefore needs a separate or lag-offset receive path (compare Aeva's lag-angle receive waveguides, §C3) or a much slower scan.
  - **Wavelength and power.** It is designed at 737 nm and shown broadband over 450–750 nm. Lidar-level CW power (15–30 mW or more per channel at 1,310/1,550 nm) was not tested; it is plausible on SiN [U] but undemonstrated.
  - **Environment.** Its Q needs high vacuum, and a PID loop tracks the resonance as it drifts. Its modes (1.3–7 kHz) sit near the automotive vibration band, which ISO 16750-3 extends to ≈2 kHz (§C4d). Die-level vacuum packaging, −40 to +105 °C drift and vibration coupling are open questions.
  - **Parallel beams.** Arrays are natural: 64 were built, and >1,000 under one 12 mm lens are projected. Each beam, though, still needs its own coherent receiver chain and optical power. The device *relocates* the channel tax rather than removing it.
- **Verdict:** an elegant chip-to-free-space scanner, strongest for visible displays and qubit control, as the paper demonstrates. For automotive FMCW it is [R], and it attacks neither of FMCW's binding costs.
- **The same test applies to any steerer**, including OPAs, LC metasurfaces and switched FPAs. A steerer helps FMCW only where it enables step-and-stare, random access or cheap parallel beams, and parallel beams help only if the receiver chain per beam becomes cheap.

### 5. The parity arithmetic: all three conditions must land together

**The target.** Parity (§C7a) means ≥15 Mpts/s in ≤15 W at 200 m and 10%. Sensor power is overhead plus point rate times electrical energy per point:
$$P=P_{\rm oh}+\dot N\left(\frac{E_{\rm opt}}{\eta_{\rm wp}}+E_{\rm rx}\right),$$
where $\eta_{\rm wp}$ is the laser and amplifier wall-plug efficiency. With $P_{\rm oh}=3$ W, parity needs
$$\frac{E_{\rm opt}}{\eta_{\rm wp}}+E_{\rm rx}\le\frac{15-3\ {\rm W}}{15\times10^{6}\ {\rm s^{-1}}}=0.8\ \mu{\rm J}.$$

**Reaching $E_{\rm opt}\approx0.15$ µJ** means improving the terms of subsection 1 without changing the geometry. For example, raising $\eta$ from 0.25 to 0.40 and lowering $n_{\rm req}$ from 30 to 25 (speckle diversity) gives $0.30\times(0.25/0.40)\times(25/30)=0.16$ µJ, the §C7a 2032 case. Going lower needs more modes per sample.

| Case | $E_{\rm opt}$ | $\eta_{\rm wp}$ | Laser electrical $E_{\rm opt}/\eta_{\rm wp}$ | $E_{\rm rx}$ | Total per point | $P$ at 15 Mpts/s |
|---|---|---|---|---|---|---|
| 2026 central (§C7a) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.56 µJ | $3+15\times2.56=41$ W |
| Better steering only (no other change) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.56 µJ | 41 W |
| 2032 optimistic (§C7a) | 0.16 µJ | 22% | 0.73 µJ | 0.15 µJ | 0.88 µJ | 16 W (just over) |
| All three win conditions | 0.15 µJ | 30% | 0.50 µJ | 0.10 µJ | 0.60 µJ | **12 W (parity)** |
| Two of three: $\eta_{\rm wp}$ stays at 15% | 0.15 µJ | 15% | 1.0 µJ | 0.10 µJ | 1.1 µJ | 19.5 W |
| Two of three: $E_{\rm rx}$ at 0.30 µJ | 0.15 µJ | 30% | 0.50 µJ | 0.30 µJ | 0.80 µJ | 15 W (borderline) |
| Two of three: $E_{\rm opt}$ stays at 0.30 µJ | 0.30 µJ | 30% | 1.0 µJ | 0.10 µJ | 1.1 µJ | 19.5 W |

*Worked row* ("all three"): $0.15/0.30=0.50$ µJ; adding 0.10 µJ gives 0.60 µJ; $3\ {\rm W}+15\times10^{6}\times0.60\times10^{-6}\ {\rm J}=3+9=12$ W.

**The round-trip waste tightens this further** [E]. The table counts only the useful energy. A CW laser transmits for the whole dwell, so the transmitted energy per point is $E_{\rm opt}\,T_{\rm dwell}/T_{\rm int}$ (subsection 1(e)).
- **At 30 mW per channel** ("all three" case): $T_{\rm int}=0.15\ \mu{\rm J}/0.03\ {\rm W}=5$ µs and $T_{\rm dwell}=7.67$ µs.
  - Transmitted energy: $0.15\times7.67/5=0.23$ µJ.
  - Total: $0.23/0.30+0.10=0.87$ µJ, i.e. $3+15\times0.87=16$ W, with 115 channels.
- **At 15 mW per channel:** $T_{\rm int}=10$ µs and $T_{\rm dwell}=12.7$ µs.
  - Transmitted energy: 0.19 µJ.
  - Total: $0.19/0.30+0.10=0.73$ µJ, i.e. 14 W, but with $15\times10^{6}\times12.7\times10^{-6}=190$ channels.
- Parity therefore also forces a choice between wasted light (few bright channels) and many dim channels.

**The per-channel budget at parity** follows from these numbers:
- 115–190 channels;
- ≈15–30 mW of optical power each;
- ≈8–13 mW of receive power each, including a ≈1 GS/s ADC and FFT. This comes from $E_{\rm rx}\dot N/N_{\rm ch}=0.10\ \mu{\rm J}\times15\times10^{6}/(115\ {\rm to}\ 190)$.
- The only merchant FMCW SoC today, indie's Surya, offers four 1 GS/s ADC channels per chip, with power not published (§C7a).

### 6. What would have to change, ranked

1. **A coherent SPAD-SoC** [NT/R].
   - What it is: a stacked or monolithic electronic-photonic IC with ≥150–256 LO-matched channels, each at ≤10–20 mW including ADC and FFT (subsection 5), for a few cents of silicon per channel.
   - This is the single enabler that attacks the channel tax. Pointcloud's own paper names the missing piece: an ASIC to replace its RFSoC readout [P].
   - Signpost: a published chip with ≥256 channels within ≈10 W (§C10.7).
2. **Efficient CW light at temperature** [NT].
   - $\eta_{\rm wp}\ge30\%$ at 105 °C for SOAs or lasers delivering $P_{\rm opt}=E_{\rm opt}\dot N\approx2$–4 W of light across ≥100 channels on SiN or III-V.
   - A comb or multi-wavelength source can feed many channels from one laser, but it does not reduce the receiver count.
3. **More modes per sample** [R].
   - Diversity or multimode coherent reception that lowers $n_{\rm req}$ and restores coverage, which subsection 1(b) caps at ≈2% of a 0.05° cell per collimated sample (§C10.3a).
   - It costs channels, so it presupposes item 1.
4. **A buyer for "fewer, richer points"** [D in trucks].
   - Driverless trucks and highway L3, where 250–400 m detection and instantaneous velocity pay (§F6).
   - A safety-case credit for instantaneous Doppler would widen this market.
5. **Energy storage instead of CW** [R].
   - The dwell–power link is specific to CW light. A pulsed coherent (pulse-compression) design fires chirped pulses from an energy-storing amplifier, so one channel delivers its energy in a short time. Pulsed coherent Doppler wind lidars do this with erbium-doped fibre amplifiers, whose excited-state lifetime is milliseconds.
   - This cuts the occupancy term $E_{\rm opt}/P_{\rm ch}$, and so the channel count. It does not cut the photons per point, which subsection 1 shows are set by single-mode collection.
   - SOAs cannot store energy (their carrier lifetime is nanoseconds), and fibre amplifiers are bulky and costly. For automotive this is research-stage.
6. **A ToF failure mode** [U].
   - Documented mutual interference at high penetration (§C9), or eye-safety and sunlight limits beyond 300 m at 905/940 nm.
   - None is documented today; ToF coding and randomization cope.

**What does not change the verdict:**
- faster or larger steering (subsection 4);
- more OPA elements (8,192 are already demonstrated, §C10.7);
- ultrafast chirps, which are bounded by detector and ADC bandwidth (subsection 2(c); §C7a(f));
- the 1,550 nm eye-safety allowance on its own, since heat, not eye safety, is the ceiling (§C7a(b)).

### 7. Probabilities (my judgement; the §C7a table stands)

| Outcome | By | Probability |
|---|---|---|
| A better beam steerer alone, with channel costs unchanged, brings FMCW to ToF parity on point rate per watt | 2032 | **<2%** |
| A published coherent receiver chip with ≥256 simultaneous channels including ADC and FFT at ≤20 mW per channel | 2030 | ≈25–35% |
| The same class of chip in a qualified automotive product | 2032 | ≈10–15% |
| FMCW parity on point rate per watt (as in §C7a) | 2032 | ≈5–10% |
| FMCW automotive volume above 1% of lidar units | 2028 | <5%. Truck and L3 demand is a few thousand to ≈20k units (§B4) against >4 M ToF planned by Hesai alone in 2026 |

**Signposts to watch:**
- channel count and per-channel power in the next coherent FPA or column chip, from Pointcloud, Voyant, Aeva or imec;
- a published SOA wall-plug efficiency at 105 °C;
- Aeva–Daimler 2027 volumes and Aurora's FirstLight count per truck;
- whether Aeva's 2028 L3 programme specifies point rate and power together;
- any Hesai or RoboSense coherent product.

Sources: https://doi.org/10.1038/s41586-025-10038-6 (copy: `refs/2026-03-12_Nature_Saha-et-al_Nanophotonic-waveguide-chip-to-world-beam-scanning.pdf`) ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12979198/ ; https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf ; https://luminwave.com.cn/long-distance-fmcw-series/ ; https://www.hesaitech.com/product/atx/ ; https://www.hesaitech.com/product/at128/ ; https://www.nature.com/articles/s41467-025-62027-y ; https://github.com/bmurmann/ADC-survey ; https://arxiv.org/pdf/2502.09736
