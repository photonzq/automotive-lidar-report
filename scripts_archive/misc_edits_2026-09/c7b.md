## C7b. Can FMCW win? The binding constraint, what beam steering can and cannot do, and what would have to change

**Short answer** [E unless tagged].
- **The binding constraint is not steering but the channel tax.** Every *simultaneous* FMCW sample needs its own local-oscillator (LO)-matched coherent receiver chain (balanced photodiodes, TIA, GS/s ADC, FFT) and its own tens of mW of CW optical power. Each channel then delivers only ≈0.1–0.25 Mpts/s at 200 m, because the dwell cannot be shorter than the chirp pair.
  - ToF adds a line for a few cents of SPAD and histogram, and shares one laser pulse across a whole column.
  - FMCW's point rate scales linearly with channels, and so do its cost and power.
- **A better beam steerer cannot remove this.** Existing mechanics already steer each channel 10–100× faster than a 200 m coherent measurement can use. Faster scanning *hurts* FMCW, through scanner-induced Doppler and walk-off (§C7). No steerer changes the single-mode collection ($A_{\rm mode}\Omega\approx\lambda^2$) that sets FMCW's photons per point.
- **Parity needs three things at once:**
  - a coherent receive channel at ≤10–20 mW with its ADC and FFT, at ≥150 channels per chip: a "coherent SPAD-SoC";
  - CW sources and amplifiers at ≥30% wall-plug efficiency at 105 °C;
  - optical energy per point near 0.15 µJ at 200 m and 10%, which needs multimode or diversity reception.
  - Missing any one leaves FMCW at ≈15–20 W for 15 Mpts/s against a ≤15 W target (table below). Today's central case is ≈41 W.
- **Where FMCW can win is a market, not a race:** buyers who pay for per-point velocity and immunity at long range, i.e. trucks and highway L3. That market is thousands of units a year through 2028, against millions for ToF (§B4).

### 1. Why point rate is expensive: the channel tax

**Dwell per channel.** An up/down chirp pair must outlast the round trip ($2R/c$ = 1.33 µs at 200 m) with margin for the beat to form. Practical dwells are 4–10 µs (§C7a), which gives **≈0.1–0.25 Mpts/s per coherent channel** at 200 m. Pointcloud's *Nature* 2026 array uses 32 µs up plus 32 µs down per pixel [P]. Channel count is therefore the multiplier:

| Target point rate | Channels at 4 µs dwell | Channels at 10 µs dwell |
|---|---|---|
| 2 Mpts/s (Aeries-class) | 8 | 20 |
| 10 Mpts/s | 40 | 100 |
| 15 Mpts/s (the parity case below) | 60 | 150 |
| 41 Mpts/s (RoboSense EM4, ToF) | 165 | 410 |

**What each channel costs** at the 2026 central values of §C7a:
- ≈30–75 mW of CW optical power at 10–15 Mpts/s (≈15–30 mW in the parity case). Silicon waveguides saturate near 16 mW (§C7a(b)), so SiN or III-V routing is needed.
- A receiver chain costing ≈0.56 µJ per point, dominated by ≈12,000 ADC samples and the FFT per 300 m-class point.
- No time sharing: the chain works whether or not photons return.
- Contrast ToF: one more line costs ≈30 µm of SPAD column plus a share of a TDC and histogram, and the laser energy is shared across lines in time (§C7a(e)).

**Published products show the gap in electrical energy per point** (vendor numbers, different ranges) [E from P]:

| Sensor | Architecture | Point rate | Power | Electrical energy per point | Range at 10% |
|---|---|---|---|---|---|
| Hesai ATX | ToF, one mechanical axis | 3.84 Mpts/s | 8 W | ≈2.1 µJ | 230 m |
| Hesai AT128 | ToF, one mechanical axis | 1.54 Mpts/s | 13.5 W | ≈8.8 µJ | 210 m |
| LuminWave F1 | FMCW, on-chip antennas | ≈1.5 Mpts/s (implied) | <45 W | ≲30 µJ | 250 m |
| Analog Photonics FS-4S | FMCW, OPA | 0.09 / 0.4 Mpts/s | 35 W | ≈390 / 88 µJ | 200 m in a 20° × 10° ROI / 80 m over 60° × 14° |

The only coherent research array with a published energy figure, Pointcloud's, reports ≈46 nJ *optical* per point at 65 m and 30% reflectivity with coherent averaging [P]. Scaled to 200 m and 10% ($\times(200/65)^2\times3$), that is ≈1.3 µJ optical per point, about 4× the §C7a FMCW central value, before any electrical conversion [E].

### 2. What beam steering can and cannot do for FMCW

**It is not the rate limiter.**
- One channel at 200 m can use at most ≈0.1–0.25 M beam positions per second.
- Galvos and polygons already supply 10⁵–10⁶ positions per second per beam; the AT128's mirror, for comparison, visits 1,200 columns per frame at 10 Hz.
- A faster steerer therefore buys nothing in points per second per channel.

**Faster scanning is actively harmful above a threshold** (§C7). A chirp must end before the beam sweeps across its own width, $\Omega\lesssim\theta_b/T_c$. At $\theta_b=0.05°$ and $T_c=5$ µs that is ≈10⁴ °/s. Above it, scanner-induced Doppler spreads the beat and receive walk-off costs signal. Coherent designs therefore favour *slow* mechanical axes, or step-and-stare.

**It cannot raise photons per point.**
- A single-mode coherent receiver collects $A_{\rm mode}\Omega\approx\lambda^2$ per channel, whatever steers the beam (§C7, §C10.3a).
- A larger steered aperture narrows each mode's angle, so the field then needs more samples or more channels. Only more *modes per sample*, which means more channels, raises collection. That returns to the channel tax.

**What a steerer can buy (secondary, but real):**
1. **Random access and foveation.** FMCW can spend its scarce samples on tracked objects.
   - Worked example [E]: 2 Mpts/s with 80% of samples on the 5% of a 120° × 25° field that holds tracked objects gives ≈10,700 pts/deg²/s on those objects, about 2× a uniform 15 Mpts/s ToF (≈5,000), and with velocity.
   - The remaining 95% of the field then gets ≈140 pts/deg²/s, 36× sparser than ToF. That is where an unexpected small obstacle has to be *found* (§C10.6).
   - Foveation therefore helps tracking, not first detection.
2. **Step-and-stare without a moving mirror.** This removes scanner Doppler and walk-off and allows longer chirps: more photons per point, fewer points per second.
3. **Solid-state packaging and reliability.** This matters less than it once seemed, because motor-driven one-axis mirrors have qualified by the million (§C4d).

**Case study: the "photonic ski-jump"** [P: M. Saha, Y. H. Wen, A. S. Greenspon, M. Zimmermann et al. (MITRE, MIT, Sandia and others), "Nanophotonic waveguide chip-to-world beam scanning", *Nature* 651, 356–362 (12 Mar 2026), open access; read in full, copy in `refs/`].
- **What it is:**
  - A 400 × 300 nm SiN waveguide on a ≈2 µm-thick AlN piezoelectric cantilever that curls ≈90° out of the chip plane, within <0.1 mm².
  - Made in a 200 mm CMOS foundry.
  - Emits a ≈0.5–0.66 µm mode (divergence half-angles 41° × 53°) and scans it resonantly at 1 kHz to >100 kHz.
  - Q ≈ 10,000 in high vacuum against ≈5 at atmospheric pressure.
  - Drive of 1–10 Vpp in vacuum; ≈10 nW DC hold power.
- **Its figure of merit:** 68.6 M spots s⁻¹ mm⁻², ">50-fold" state-of-the-art MEMS mirrors, "sufficient for one million pixels at 100 Hz from an approximately 1.5 mm diameter footprint".
- **Demonstrations:**
  - full-colour Lissajous image projection at 7–36 Hz;
  - addressing of silicon-vacancy qubits;
  - a 64-device array with <2% curvature spread;
  - a projected >1 gigaspot at kHz rates from <5 cm, given a further 10× in figure of merit.
- **Limitations the authors state:** vacuum packaging, no true random access, a curved scan trajectory, and possible nonlinearity or thermal loading at higher optical power.
- **Tested against lidar needs** [E]:

| Requirement for a 200 m coherent channel | Ski-jump as published | Consequence |
|---|---|---|
| Dwell of 4–10 µs per resolved position | Resonant raster. At the lowest ≈1.3 kHz mode, one 5 µs chirp per spot allows only $1/(2fT)\approx77$ spots per line (≈20 at the ≈4.9 kHz mode). Off-resonance travel is small (≈29 µm of DC tip travel for ±50 V) | Used point by point at lidar resolution, it would be far too fast. Slowed, it loses most of its range of motion |
| Monostatic receive: the tip must not move more than a fraction of the mode during the round trip | Tip speed ≈2πfA ≈ 1.6 m/s at A ≈ 50 µm and 5 kHz. It moves ≈2.1 µm in 1.33 µs (200 m), against a ≈0.3 µm mode radius | Coupling $\propto e^{-(\Delta x/w_0)^2}$: ≈−2 dB at 20 m, ≈−13 dB at 50 m, nil at 200 m. It needs a separate or lag-offset receive path (compare Aeva's lag-angle receive waveguides, §C3) or a much slower scan |
| 1,310/1,550 nm at 15–30 mW or more of CW per channel | Designed at 737 nm; broadband 450–750 nm shown; lidar-level optical power not tested | Plausible on SiN [U], but undemonstrated |
| Automotive environment: −40 to +105 °C, ISO 16750-3 vibration to ≈2 kHz (§C4d) | Needs high vacuum for its Q; resonance tracked by a PID loop; modes at 1.3–7 kHz | Die-level vacuum packaging, thermal drift and vibration coupling are open |
| Many parallel channels | Arrays are natural: 64 built; >1,000 under one 12 mm lens projected | Gives many beams, but each still needs its own coherent receiver chain and optical power. It *relocates* the channel tax rather than removing it |

  - **Verdict:** an elegant chip-to-free-space scanner, strongest for visible displays and qubit control, as the paper demonstrates [D/R there]. For automotive FMCW it is [R], and it attacks neither of FMCW's binding costs.
- **The same test applies to any steerer, including OPAs, LC metasurfaces and switched FPAs.** It helps FMCW only where it enables step-and-stare, random access or cheap parallel beams. And parallel beams help only if the receiver chain per beam becomes cheap.

### 3. The parity arithmetic: all three conditions must land together

Parity (§C7a) means ≥15 Mpts/s in ≤15 W at 200 m and 10%. After 3 W of overhead, that leaves ≤0.8 µJ of electrical energy per point [E]:

| Case | Optical per point | Laser wall-plug | Laser electrical | Receiver | Total per point | Power at 15 Mpts/s |
|---|---|---|---|---|---|---|
| 2026 central (§C7a) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.6 µJ | ≈41 W |
| Better steering only (no other change) | 0.30 µJ | 15% | 2.0 µJ | 0.56 µJ | 2.6 µJ | ≈41 W |
| 2032 optimistic (§C7a) | 0.16 µJ | 22% | 0.73 µJ | 0.15 µJ | 0.87 µJ | ≈16 W (just over) |
| All three win conditions | 0.15 µJ | 30% | 0.50 µJ | 0.10 µJ | 0.60 µJ | **≈12 W (parity)** |
| Two of three: wall-plug stays at 15% | 0.15 µJ | 15% | 1.0 µJ | 0.10 µJ | 1.1 µJ | ≈20 W |
| Two of three: receiver at 0.30 µJ | 0.15 µJ | 30% | 0.50 µJ | 0.30 µJ | 0.80 µJ | ≈15 W (borderline) |
| Two of three: optical stays at 0.30 µJ | 0.30 µJ | 30% | 1.0 µJ | 0.10 µJ | 1.1 µJ | ≈20 W |

At parity, per channel, the budget is 75–150 channels at 5–10 µs dwell, with ≈15–30 mW of optical power each and **≈10–20 mW of receive power each, including a ≈1 GS/s ADC and FFT**. The only merchant FMCW SoC today, indie's Surya, offers four 1 GS/s ADC channels per chip, with power not published (§C7a).

### 4. What would have to change, ranked

1. **A coherent SPAD-SoC** [NT/R].
   - What it is: a stacked or monolithic electronic-photonic IC with ≥150–256 LO-matched channels, each at ≤10–20 mW including ADC and FFT, and a few cents of silicon.
   - This is the single enabler that attacks the channel tax. Pointcloud's own paper names the missing piece: an ASIC to replace its RFSoC readout [P].
   - Signpost: a published chip at ≥256 channels within ≈10 W (§C10.7).
2. **Efficient CW light at temperature** [NT].
   - ≥30% wall-plug efficiency at 105 °C for SOAs or lasers delivering ≥2–4 W of optical power across ≥100 channels on SiN or III-V.
   - A comb or multi-wavelength source can feed many channels from one laser, but it does not reduce the receiver count.
3. **More modes per sample** [R].
   - Diversity or multimode coherent reception that restores coverage (the ≈2% footprint of §C10.3a) and cuts fading margins.
   - It costs channels, so it presupposes item 1.
4. **A buyer for "fewer, richer points"** [D in trucks].
   - Driverless trucks and highway L3, where 250–400 m detection and instantaneous velocity pay (§F6).
   - A safety-case credit for instantaneous Doppler would widen this market.
5. **A ToF failure mode** [U].
   - Documented mutual interference at high penetration (§C9), or eye-safety and sunlight limits beyond 300 m at 905/940 nm.
   - None is documented today; ToF coding and randomization cope.

**What does not change the verdict:**
- faster or larger steering;
- more OPA elements (8,192 are already demonstrated, §C10.7);
- ultrafast chirps, which are bounded by detector bandwidth (§C7a(f));
- the 1,550 nm eye-safety allowance on its own, since heat, not eye safety, is the ceiling (§C7a(b)).

### 5. Probabilities (my judgement; the §C7a table stands)

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

Sources: https://doi.org/10.1038/s41586-025-10038-6 (copy: `refs/2026-03-12_Nature_Saha-et-al_Nanophotonic-waveguide-chip-to-world-beam-scanning.pdf`) ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12979198/ ; https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf ; https://luminwave.com.cn/long-distance-fmcw-series/ ; https://www.hesaitech.com/product/atx/ ; https://www.hesaitech.com/product/at128/
