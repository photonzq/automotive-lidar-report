## C7b. Can FMCW win? The binding constraint, what beam steering can and cannot do, and what would have to change

**Short answer** [E unless tagged].
- **FMCW is held back by the cost of each simultaneous measurement, not by beam steering.** Every point that an FMCW sensor measures at the same moment needs its own local-oscillator (LO)-matched coherent receiver: balanced photodiodes, a transimpedance amplifier (TIA), a GS/s analogue-to-digital converter (ADC) and an FFT. It also needs its own tens of milliwatts of continuous-wave (CW) laser light.
  - Each such channel can measure only about 0.05–0.25 million points per second at 200 m (subsection 1 derives this).
  - The point rate therefore grows only in proportion to the number of channels, and so do cost and power. This report calls that the *channel tax*.
  - A ToF lidar adds a line for a few cents of SPAD column and histogram memory, and reads a whole column from one laser pulse.
- **The dwell per point is set mainly by photons, because CW light cannot be concentrated in time.** A pulsed ToF laser puts its energy into a nanosecond pulse at tens to hundreds of watts. A CW channel's peak power *is* its average power, so the only way to deliver more energy to a point is to transmit for longer.
  - The round trip adds a fixed overhead on top.
  - Readout bandwidth and laser chirp quality make very short chirps expensive, but they are not the floor.
- **A better beam steerer cannot remove the channel tax.** Existing mirrors already move each beam as fast as, or faster than, one coherent channel can use. Faster scanning actively hurts FMCW (scanner-induced Doppler and walk-off, §C7). No steerer changes the single-mode collection rule, $A_{\rm mode}\Omega\approx\lambda^2$, that fixes FMCW's photons per point.
- **Parity with ToF needs three things at once** (subsection 4):
  - a coherent receiver chip with ≥150 channels at ≤10–20 mW each, ADC and FFT included (a coherent counterpart of the SPAD-SoC);
  - CW lasers and amplifiers at ≥30% wall-plug efficiency at 105 °C;
  - an optical energy per point near 0.15 µJ at 200 m on a 10% target, which needs multimode or diversity reception.
  - Missing any one of them leaves a 15 Mpts/s sensor at ≈15–20 W against a 15 W target; today's central case is ≈41 W.
- **FMCW can win a market, not the point-rate race.** Its market is buyers who pay for per-point velocity and immunity at long range: trucks and highway L3. Through 2028 that is thousands of units a year, against millions for ToF (§B4).

### 1. What sets the dwell of one FMCW point

**Notation.** An FMCW channel sweeps the optical frequency linearly over one "ramp" (chirp) of duration $T_c$ at chirp rate $\kappa$ (Hz/s). The echo from range $R$ returns after the round trip

$$\tau=\frac{2R}{c},\qquad \tau(200\ {\rm m})=\frac{2\times200\ {\rm m}}{3\times10^{8}\ {\rm m/s}}=1.33\ \mu{\rm s}.$$

The standard measurement uses an up-ramp and a down-ramp, because the pair separates range from Doppler (§C0 subsection 2). One point therefore takes $T_{\rm dwell}=2T_c$.

**(a) The round trip removes $\tau$ from every ramp.** The echo only produces a clean beat with the LO once it has arrived. During the first $\tau$ of each ramp, what returns is the tail of the previous ramp, which has the opposite slope and is discarded. The useful window per ramp is therefore

$$T_u=T_c-\tau .$$

Two consequences follow.
- **Resolution comes from the useful window only.** The frequency swept while the beat exists is $B_{\rm eff}=\kappa T_u$, and range resolution is $\Delta R=c/(2B_{\rm eff})$. Keeping $\Delta R=15$ cm needs $B_{\rm eff}=c/(2\Delta R)=3\times10^{8}/(2\times0.15)=1$ GHz within $T_u$. The total sweep is larger: $B_{\rm tot}=\kappa T_c=B_{\rm eff}\,T_c/T_u$. For $T_u=2$ µs, $T_c=3.33$ µs and $B_{\rm tot}=1\ {\rm GHz}\times3.33/2=1.67$ GHz.
- **There is a hard ceiling on point rate per channel.** Even with infinite laser power ($T_u\to0$), $T_{\rm dwell}\ge2\tau$. At 200 m that is 2.67 µs, i.e. at most $1/(2.67\ \mu{\rm s})\approx375$ kpts/s per channel.

**(b) The photon budget sets the rest, and it is the binding term.**
- **Energy needed.** A point needs an optical energy $E_{\rm opt}$ on the useful windows, large enough to collect the photoelectrons that survive speckle fading. §C7a(a) derives it from
  $$E_{\rm opt}=\frac{n_{\rm req}\,E_{\rm ph}\,\pi R^2}{\rho\,A_{\rm mode}\,\eta}.$$
  Here $E_{\rm ph}=hc/\lambda=1.28\times10^{-19}$ J at 1,550 nm; $n_{\rm req}=30$ photoelectrons; $\rho=0.1$; $A_{\rm mode}\approx64$ mm² (one coherent mode of a 20 mm monostatic Gaussian at 200 m, §C10.3b); and efficiency $\eta=0.25$. That gives
  $$E_{\rm opt}=\frac{30\times1.28\times10^{-19}\ {\rm J}\times\pi\times(200\ {\rm m})^2}{0.1\times64\times10^{-6}\ {\rm m^2}\times0.25}\approx3.0\times10^{-7}\ {\rm J}=0.30\ \mu{\rm J}.$$
  The optimistic parity case (subsection 4) halves this to 0.15 µJ.
- **Integration time.** A channel transmitting constant power $P_{\rm ch}$ must integrate for $T_{\rm int}=E_{\rm opt}/P_{\rm ch}$ of useful window, summed over both ramps: $2T_u=T_{\rm int}$. With $T_c=T_u+\tau$:
  $$\boxed{\,T_{\rm dwell}=2T_c=\frac{E_{\rm opt}}{P_{\rm ch}}+2\tau\,},\qquad \dot N_{\rm ch}=\frac{1}{T_{\rm dwell}}.$$
- **Worked example:** $E_{\rm opt}=0.30$ µJ and $P_{\rm ch}=30$ mW give $T_{\rm int}=0.30\times10^{-6}/0.030=10$ µs. Then $T_{\rm dwell}=10+2.67=12.7$ µs and $\dot N_{\rm ch}=1/12.7\ \mu{\rm s}=79$ kpts/s.
- **What limits $P_{\rm ch}$.** It cannot simply be raised:
  - *Heat.* CW sources plus semiconductor optical amplifiers (SOAs) run at ≈15–20% wall-plug efficiency, so each watt of light costs 4–6 W of heat (§C7a(b)).
  - *Waveguide power handling.* Silicon waveguides saturate near 16 mW through two-photon and free-carrier absorption (Pointcloud Methods, §C7a(b)); higher power needs SiN or III-V paths.
  - *Per-beam eye safety at 1,550 nm.* This is secondary; §C7a concludes that heat is the practical ceiling.
- **The share of the laser's energy wasted in the round-trip windows** is $2\tau/T_{\rm dwell}$. In the example, $2.67/12.7=21\%$.

| $P_{\rm ch}$ | $T_{\rm dwell}$ at 0.30 µJ | Per-channel rate | Wasted share | $T_{\rm dwell}$ at 0.15 µJ | Per-channel rate | Wasted share |
|---|---|---|---|---|---|---|
| 16 mW (silicon limit) | 21.4 µs | 47 kpts/s | 12% | 12.0 µs | 83 kpts/s | 22% |
| 30 mW | 12.7 µs | 79 kpts/s | 21% | 7.7 µs | 130 kpts/s | 35% |
| 100 mW | 5.7 µs | 176 kpts/s | 47% | 4.2 µs | 240 kpts/s | 64% |
| Unlimited | → 2.67 µs | → 375 kpts/s | → 100% | → 2.67 µs | → 375 kpts/s | → 100% |

*How the table is computed* [E]: $T_{\rm dwell}=E_{\rm opt}/P_{\rm ch}+2\tau$ with $2\tau=2.67$ µs at 200 m; rate $=1/T_{\rm dwell}$; wasted share $=2\tau/T_{\rm dwell}$. Example row (100 mW, 0.15 µJ): $0.15\ \mu{\rm J}/0.1\ {\rm W}=1.5$ µs, plus 2.67 µs, gives 4.17 µs. The rate is $1/4.17\ \mu{\rm s}=240$ kpts/s, and the wasted share is $2.67/4.17=64\%$.

At the powers realistic for integrated photonics (16–30 mW), the photon term is 2–7 times the round-trip term: $T_{\rm int}$/$2\tau$ = 3.5–7.0 at 0.30 µJ and 1.9–3.5 at 0.15 µJ. **The dwell is mostly a measure of how much CW light one channel can carry.**

**(c) Readout bandwidth makes short chirps expensive but does not forbid them.**
- **Beat frequency.** The largest beat, at maximum range and closing speed, is
  $$f_{b,\max}=\kappa\tau+f_D=\frac{B_{\rm eff}}{T_u}\,\tau+\frac{2v}{\lambda}.$$
  At 70 m/s and 1,550 nm, $f_D=2\times70/1.55\times10^{-6}=90$ MHz.
- **Sampling rate.** Sampling with ≈25% margin above Nyquist, $f_s\approx2.5\,f_{b,\max}$, at $R=200$ m and $B_{\rm eff}=1$ GHz:

| Useful window $T_u$ | Chirp $T_c=T_u+\tau$ | Total sweep $B_{\rm tot}$ | Range beat $B_{\rm eff}\tau/T_u$ | $f_{b,\max}$ with Doppler | Sampling rate $f_s$ |
|---|---|---|---|---|---|
| 10 µs | 11.3 µs | 1.13 GHz | 133 MHz | 223 MHz | 0.56 GS/s |
| 5 µs | 6.3 µs | 1.27 GHz | 267 MHz | 357 MHz | 0.89 GS/s |
| 2 µs | 3.3 µs | 1.67 GHz | 667 MHz | 757 MHz | 1.9 GS/s |
| 1 µs | 2.3 µs | 2.33 GHz | 1,333 MHz | 1,423 MHz | 3.6 GS/s |

  *Worked row* (5 µs): $1\ {\rm GHz}\times1.33\ \mu{\rm s}/5\ \mu{\rm s}=267$ MHz; plus 90 MHz gives 357 MHz; $\times2.5=0.89$ GS/s.
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
- **Consequence.** Once the FFT bin $1/T_u$ is narrower than the phase-noise spread $2\Delta\nu$, a longer window no longer sharpens the peak. So $T_u\gtrsim1/(2\Delta\nu)$ buys little: ≈5 µs for a 100 kHz laser. Long, photon-rich chirps need narrower lasers (§C7).

**(f) Scanning also caps the chirp from above.** The chirp must end before the beam sweeps across its own width, $T_c\lesssim\theta_b/\Omega$ (§C7). For $\theta_b=0.05°=8.7\times10^{-4}$ rad and a 5 µs chirp, $\Omega\lesssim8.7\times10^{-4}/5\times10^{-6}=175$ rad/s ≈ $10^4$ °/s. Target motion during a chirp is negligible: 50 m/s × 10 µs = 0.5 mm.

**Summary of the dwell.**
- At 200 m, with 16–30 mW per channel, the photon budget dominates: 8–21 µs per point, i.e. 47–130 kpts/s per channel.
- The round trip adds a fixed 2.67 µs and caps any channel at ≈375 kpts/s.
- Readout and laser make chirps below about 2 µs expensive.
- Linewidth and scanning cap useful chirps at about 5 µs (for a 100 kHz laser) and $\theta_b/\Omega$.

### 2. The channel tax: channels, power and receivers

**Channels.** Each coherent channel measures one point per dwell, so a sensor that must deliver $\dot N$ points per second needs
$$N_{\rm ch}=\dot N\,T_{\rm dwell}.$$
Example: 15 Mpts/s at a 12.7 µs dwell needs $15\times10^{6}\times12.7\times10^{-6}=190$ channels.

| Target point rate | Channels at 4 µs dwell | Channels at 10 µs dwell | Channels at the 30 mW / 0.30 µJ dwell (12.7 µs) |
|---|---|---|---|
| 2 Mpts/s (Aeries-class) | 8 | 20 | 25 |
| 10 Mpts/s | 40 | 100 | 127 |
| 15 Mpts/s (the parity case) | 60 | 150 | 190 |
| 41 Mpts/s (RoboSense EM4, ToF) | 164 | 410 | 520 |

*How the table is computed* [E]: $N_{\rm ch}=\dot N\,T_{\rm dwell}$; for example $41\times10^{6}\times4\times10^{-6}=164$. A 4 µs dwell is close to the lower practical end at 200 m: it implies $T_u=4/2-1.33=0.67$ µs per ramp, $f_s\approx5$ GS/s and ≈100 mW per channel at 0.15 µJ.

**Optical power.** Total optical power depends only on the energy per point, not on the dwell: $P_{\rm opt}=E_{\rm opt}\,\dot N$. At 15 Mpts/s this is $0.30\ \mu{\rm J}\times15\times10^{6}\ {\rm s^{-1}}=4.5$ W (2026 central), or 2.25 W at 0.15 µJ. Spreading it over $N_{\rm ch}$ channels gives $P_{\rm ch}=P_{\rm opt}/N_{\rm ch}$: $4.5\ {\rm W}/150=30$ mW.
- **Brighter channels do not save watts.** They shorten the dwell and the channel count, which saves receiver chains, but they do not lower watts per point. The round-trip waste of subsection 1(b) even raises the transmitted energy.

**Receiver power.** $P_{\rm rx}=\dot N\,E_{\rm rx}$. At the §C7a 2026 central ≈0.56 µJ per point (300 m, 12,300 samples at 37 pJ plus ≈10 mW of TIA and bias per channel), 15 Mpts/s needs $15\times10^{6}\times0.56\times10^{-6}=8.4$ W of receiver electronics. That is the same order as the whole of a 520-line ToF unit.

**ToF for contrast.** One more ToF line costs ≈30 µm of SPAD column (three 10 µm SPADs) plus a share of a time-to-digital converter and histogram. Its laser energy comes from high-peak pulses shared across lines in time (§C7a(e)).

**Published products** (vendor figures, at different ranges). Electrical energy per point is $E=P/\dot N$ [E from P]:

| Sensor | Architecture | Point rate $\dot N$ | Power $P$ | $E=P/\dot N$ | Range at 10% |
|---|---|---|---|---|---|
| Hesai ATX | ToF, one mechanical axis | 3.84 Mpts/s | 8 W | $8/3.84\times10^{6}=2.1$ µJ | 230 m |
| Hesai AT128 | ToF, one mechanical axis | 1.536 Mpts/s | 13.5 W | $13.5/1.536\times10^{6}=8.8$ µJ | 210 m |
| LuminWave F1 | FMCW, on-chip antennas | ≈1.5 Mpts/s (implied) | <45 W | $\lesssim45/1.5\times10^{6}=30$ µJ | 250 m |
| Analog Photonics FS-4S | FMCW, OPA | 0.09 / 0.4 Mpts/s | 35 W | $35/0.09\times10^{6}=390$ / $35/0.4\times10^{6}=88$ µJ | 200 m in a 20° × 10° ROI / 80 m over 60° × 14° |

**Pointcloud's research array**, the only coherent array with a published energy figure, reports ≈46 nJ *optical* per point at 65 m and 30% reflectivity, with coherent averaging [P]. Optical energy per point scales as $R^2/\rho$ (the $E_{\rm opt}$ formula above). Scaling to 200 m and 10% multiplies it by $(200/65)^2\times(0.30/0.10)=9.47\times3=28.4$, giving $46\ {\rm nJ}\times28.4\approx1.3$ µJ optical per point. That is ≈4.4× the §C7a central 0.30 µJ, before any electrical conversion [E].

### 3. What beam steering can and cannot do for FMCW

**Steering is not the rate limiter.**
- **What one channel can use.** At 200 m, one channel can use at most $1/T_{\rm dwell}$ beam positions per second: 47–240 k with realistic power, never more than 375 k (subsection 1).
- **What steerers supply.** A steerer supplies $\Omega/\theta_b$ positions per second per beam:
  - a Falcon-class polygon at 45,600 °/s with a 0.05° beam gives $45{,}600/0.05=912{,}000$;
  - a resonant MEMS mirror at 188,500 °/s peak gives $188{,}500/0.05=3.8\times10^{6}$ (§C7 table);
  - the AT128's mirror, by comparison, visits only $1{,}200\times10=12{,}000$ columns per second per channel.
- **So a faster steerer buys nothing in points per second per channel.**

**Faster scanning actively hurts above a threshold.** The chirp must end before the beam crosses its own width: $\Omega\lesssim\theta_b/T_c=175$ rad/s ≈ $10^4$ °/s for 0.05° and 5 µs (subsection 1(f)). Above this, scanner-induced Doppler spreads the beat over $\approx T_c\,\Omega D/\lambda$ FFT bins, and receive walk-off costs signal (§C7). Coherent designs therefore favour *slow* mechanical axes or step-and-stare.

**No steerer raises photons per point.**
- A single-mode coherent receiver collects $A_{\rm mode}\Omega_{\rm cell}\approx\lambda^2$, whatever steers the beam.
- For a 0.05° × 0.05° cell, $\Omega_{\rm cell}=(8.7\times10^{-4})^2=7.6\times10^{-7}$ sr. That gives $A_{\rm mode}\approx(1.55\times10^{-6})^2/7.6\times10^{-7}=3.2\times10^{-6}$ m², an equivalent collecting diameter of only ≈2 mm (§C7, §C10.3a).
- A larger steered aperture narrows each mode's angular acceptance, so the field then needs more samples or more channels. Only more *modes per sample*, i.e. more channels, raises collection. That returns to the channel tax.

**What a steerer can buy (secondary, but real).**
1. **Random access and foveation.** FMCW can spend its scarce samples on tracked objects. Worked example [E]:
   - A 120° × 25° field is 3,000 deg². Put 80% of 2 Mpts/s on the 5% of it (150 deg²) that holds tracked objects. The density there is $1.6\times10^{6}/150=10{,}700$ pts/deg²/s, about 2× a uniform 15 Mpts/s ToF ($15\times10^{6}/3{,}000=5{,}000$), with velocity on every point.
   - The remaining 95% of the field (2,850 deg²) then gets $0.4\times10^{6}/2{,}850=140$ pts/deg²/s, $5{,}000/140\approx36\times$ sparser than ToF. That is where an unexpected small obstacle must be *found* (§C10.6).
   - Foveation therefore helps tracking, not first detection.
2. **Step-and-stare without a moving mirror.** This removes scanner Doppler and walk-off, which allows longer chirps: more photons per point and fewer points per second.
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
  - **Wavelength and power.** It is designed at 737 nm and shown broadband over 450–750 nm; lidar-level CW power (15–30 mW or more per channel at 1,310/1,550 nm) was not tested. It is plausible on SiN [U] but undemonstrated.
  - **Environment.** Its Q needs high vacuum, and a PID loop tracks the resonance as it drifts. Its modes (1.3–7 kHz) sit near the automotive vibration band, which ISO 16750-3 extends to ≈2 kHz (§C4d). Die-level vacuum packaging, −40 to +105 °C drift and vibration coupling are open questions.
  - **Parallel beams.** Arrays are natural: 64 were built, and >1,000 under one 12 mm lens are projected. Each beam, though, still needs its own coherent receiver chain and optical power. The device *relocates* the channel tax rather than removing it.
- **Verdict:** an elegant chip-to-free-space scanner, strongest for visible displays and qubit control, as the paper demonstrates. For automotive FMCW it is [R], and it attacks neither of FMCW's binding costs.
- **The same test applies to any steerer**, including OPAs, LC metasurfaces and switched FPAs. A steerer helps FMCW only where it enables step-and-stare, random access or cheap parallel beams, and parallel beams help only if the receiver chain per beam becomes cheap.

### 4. The parity arithmetic: all three conditions must land together

**The target.** Parity (§C7a) means ≥15 Mpts/s in ≤15 W at 200 m and 10%. Sensor power is overhead plus point rate times electrical energy per point:
$$P=P_{\rm oh}+\dot N\left(\frac{E_{\rm opt}}{\eta_{\rm wp}}+E_{\rm rx}\right),$$
where $\eta_{\rm wp}$ is the laser and amplifier wall-plug efficiency. With $P_{\rm oh}=3$ W, parity needs
$$\frac{E_{\rm opt}}{\eta_{\rm wp}}+E_{\rm rx}\le\frac{15-3\ {\rm W}}{15\times10^{6}\ {\rm s^{-1}}}=0.8\ \mu{\rm J}.$$

| Case | $E_{\rm opt}$ | $\eta_{\rm wp}$ | Laser electrical $E_{\rm opt}/\eta_{\rm wp}$ | $E_{\rm rx}$ | Total per point | $P$ at 15 Mpts/s |
|---|---|---|---|---|---|---|
| 2026 central (§C7a) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.56 µJ | $3+15\times2.56=41$ W |
| Better steering only (no other change) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.56 µJ | 41 W |
| 2032 optimistic (§C7a) | 0.16 µJ | 22% | 0.73 µJ | 0.15 µJ | 0.88 µJ | 16 W (just over) |
| All three win conditions | 0.15 µJ | 30% | 0.50 µJ | 0.10 µJ | 0.60 µJ | **12 W (parity)** |
| Two of three: $\eta_{\rm wp}$ stays at 15% | 0.15 µJ | 15% | 1.0 µJ | 0.10 µJ | 1.1 µJ | 19.5 W |
| Two of three: $E_{\rm rx}$ at 0.30 µJ | 0.15 µJ | 30% | 0.50 µJ | 0.30 µJ | 0.80 µJ | 15 W (borderline) |
| Two of three: $E_{\rm opt}$ stays at 0.30 µJ | 0.30 µJ | 30% | 1.0 µJ | 0.10 µJ | 1.1 µJ | 19.5 W |

*Worked row* ("all three"): $0.15/0.30=0.50$ µJ; plus 0.10 µJ gives 0.60 µJ; $3\ {\rm W}+15\times10^{6}\times0.60\times10^{-6}\ {\rm J}=3+9=12$ W.

**The round-trip waste tightens this further** [E]. The table counts only the useful energy. A CW laser transmits for the whole dwell, so the transmitted energy per point is $E_{\rm opt}\,T_{\rm dwell}/T_{\rm int}$.
- In the "all three" case at 30 mW per channel: $T_{\rm int}=0.15\ \mu{\rm J}/0.03\ {\rm W}=5$ µs and $T_{\rm dwell}=7.67$ µs. The transmitted energy is $0.15\times7.67/5=0.23$ µJ, and the total becomes $0.23/0.30+0.10=0.87$ µJ, i.e. $3+15\times0.87=16$ W with 115 channels.
- At 15 mW per channel: $T_{\rm int}=10$ µs and $T_{\rm dwell}=12.7$ µs. The transmitted energy is 0.19 µJ, the total $0.19/0.30+0.10=0.73$ µJ, i.e. 14 W, but with $15\times10^{6}\times12.7\times10^{-6}=190$ channels.
- Parity therefore also forces a choice between wasted light (few bright channels) and many dim channels.

**The per-channel budget at parity** follows from these numbers:
- 115–190 channels;
- ≈15–30 mW of optical power each;
- ≈10–20 mW of receive power each, including a ≈1 GS/s ADC and FFT. From $E_{\rm rx}\,\dot N/N_{\rm ch}=0.10\ \mu{\rm J}\times15\times10^{6}/(115\ {\rm to}\ 190)=8$–13 mW.
- The only merchant FMCW SoC today, indie's Surya, offers four 1 GS/s ADC channels per chip, with power not published (§C7a).

### 5. What would have to change, ranked

1. **A coherent SPAD-SoC** [NT/R].
   - What it is: a stacked or monolithic electronic-photonic IC with ≥150–256 LO-matched channels, each at ≤10–20 mW including ADC and FFT (subsection 4), for a few cents of silicon per channel.
   - This is the single enabler that attacks the channel tax. Pointcloud's own paper names the missing piece: an ASIC to replace its RFSoC readout [P].
   - Signpost: a published chip with ≥256 channels within ≈10 W (§C10.7).
2. **Efficient CW light at temperature** [NT].
   - $\eta_{\rm wp}\ge30\%$ at 105 °C for SOAs or lasers delivering $P_{\rm opt}=E_{\rm opt}\dot N\approx2$–4 W of light across ≥100 channels on SiN or III-V.
   - A comb or multi-wavelength source can feed many channels from one laser, but it does not reduce the receiver count.
3. **More modes per sample** [R].
   - Diversity or multimode coherent reception that lowers $n_{\rm req}$ and restores coverage (the ≈2% footprint of §C10.3a).
   - It costs channels, so it presupposes item 1.
4. **A buyer for "fewer, richer points"** [D in trucks].
   - Driverless trucks and highway L3, where 250–400 m detection and instantaneous velocity pay (§F6).
   - A safety-case credit for instantaneous Doppler would widen this market.
5. **Energy storage instead of CW** [R].
   - The dwell–power link is specific to CW light. A pulsed coherent (pulse-compression) design fires chirped pulses from an energy-storing amplifier, which lets one channel deliver high energy in a short time. Pulsed coherent Doppler wind lidars do this with erbium-doped fibre amplifiers, whose excited-state lifetime is milliseconds.
   - SOAs cannot store energy (their carrier lifetime is nanoseconds), and fibre amplifiers are bulky and costly. For automotive this is research-stage.
6. **A ToF failure mode** [U].
   - Documented mutual interference at high penetration (§C9), or eye-safety and sunlight limits beyond 300 m at 905/940 nm.
   - None is documented today; ToF coding and randomization cope.

**What does not change the verdict:**
- faster or larger steering (subsection 3);
- more OPA elements (8,192 are already demonstrated, §C10.7);
- ultrafast chirps, which are bounded by detector and ADC bandwidth (subsection 1(c); §C7a(f));
- the 1,550 nm eye-safety allowance on its own, since heat, not eye safety, is the ceiling (§C7a(b)).

### 6. Probabilities (my judgement; the §C7a table stands)

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

Sources: https://doi.org/10.1038/s41586-025-10038-6 (copy: `refs/2026-03-12_Nature_Saha-et-al_Nanophotonic-waveguide-chip-to-world-beam-scanning.pdf`) ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12979198/ ; https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf ; https://luminwave.com.cn/long-distance-fmcw-series/ ; https://www.hesaitech.com/product/atx/ ; https://www.hesaitech.com/product/at128/ ; https://www.nature.com/articles/s41467-025-62027-y ; https://github.com/bmurmann/ADC-survey
