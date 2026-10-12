**iToF and dToF chips: two pixel architectures.** Both are CMOS chips behind a lens, lit by a VCSEL. What differs is what the pixel does with a photon.
- **iToF: an analog lock-in integrator.** A linear-mode photodiode (pinned, CAPD or PMD) with gain 1 steers photoelectrons into two or more taps in step with the modulation. In Sony's CAPD pixel, an alternating drift field sends each electron to one of two junctions switched 180° apart [T, LUCID].
  - Four phase samples give $\varphi=\arctan[(Q_{90}-Q_{270})/(Q_0-Q_{180})]$.
  - Subtracting taps removes the *mean* ambient light but not its shot noise.
  - The time reference is the modulation clock; no single photon is ever timed.
- **dToF: a photon counter with a stopwatch.** A SPAD biased above breakdown turns one photon into a digital event. A time-to-digital converter (TDC) stamps it, and on-chip memory builds a histogram over hundreds to thousands of laser pulses.
  - $\sigma_R\approx(c/2)\,\sigma_t/\sqrt{N_s}$, with $\sigma_t$ set by pulse width, SPAD jitter and TDC step (subsection 1).
  - Ambient photons spread evenly over the histogram bins; only the few bins around the echo compete with it.

| | iToF sensor | dToF (SPAD) chip |
|---|---|---|
| **What the pixel stores** | Analog charge in 2–4 taps | Nothing analog: events go to TDCs or time-gated counters, then to histogram memory |
| **Circuitry per pixel** | Demodulation gates, storage nodes, reset and readout transistors | Quench and recharge, pulse shaping, a shared TDC, histogram SRAM and peak finding |
| **Pitch and resolution** | Small and dense: Sony IMX556 VGA at 10 µm (57% QE at 850 nm) [T]; ST VD55H1 0.54 MP at 4.6 µm [T]; 1 MP parts (ADI/Microsoft) | Coarse: iPhone 15 Pro LiDAR 116 × 92 SPADs at 10.1 µm; VL53L5 14 × 10 macro-pixels [I]; IMX611 140 × 170 at 28% PDE (940 nm) [P] |
| **Process** | An image-sensor process plus demodulation structures; ST's VD55H1 uses its 40 nm stacked back-illuminated wafers [T] | A SPAD junction (guard rings, low dark count, high-voltage bias) plus dense logic. Sony stacks a 90 nm SPAD wafer on 28 nm logic with 5 µm-pitch Cu–Cu hybrid bonds; ST uses monolithic 40 nm; ams 55 nm high-voltage CMOS [I, Bonanno 2024] |
| **Emitter** | Flood, modulated at 10–200 MHz with ≈50% duty; moderate peak power | ns pulses at high peak power and low duty, often as a dot pattern or addressable zones (the iPhone module's VCSEL has 112 individually addressed cavities) |
| **Raw output** | Four or more raw frames per depth frame → phase processing → dense depth and amplitude images | Photon events → on-chip histograms → one or several peaks per pixel or zone |
| **Ambiguity** | $c/2f_m$ (0.75 m at 200 MHz); fixed with a second frequency | $c/2f_{\rm rep}$; fixed with the repetition rate or pulse coding |
| **Sunlight** | Integrated into the wells continuously: shot noise and full-well saturation | Seen only in the bins near the echo; heavy flux causes pile-up through SPAD dead time |
| **Multiple echoes** (glass, rain, edges, corners) | One phasor per pixel: the depth is biased | Separate histogram peaks |
| **Power** | Clock distribution across the pixel array, plus the laser | Grows with photon count rate, so sunlight raises power as well as noise |

**Same makers, both architectures** (a comparison that controls for company and process):

| Maker | dToF (SPAD) | iToF (demodulating) |
|---|---|---|
| **ST** | VL53L5/L8: 8 × 8 zones, ≈4 m; a complete module with VCSEL and optics, \$3.60 in 1,000-unit trays [T] | VD55H1: 672 × 804 pixels, 200 MHz at >85% demodulation contrast (940 nm), ≈5 m at full resolution, 120 fps, <100 mW in some modes; sampling from Feb 2022 [T] |
| **Sony** | IMX611: 23,800 SPADs, 8 m specification point [P] | IMX556: VGA (307,200 pixels), 10 µm CAPD pixels [T] |

- **Resolution.** At a similar 5–8 m, the VD55H1 has ≈23× the IMX611's pixel count ($540{,}288/23{,}800$) and ≈8,400× an 8 × 8 ranger's zones [E].
- **Why dToF lags: memory, not optics.** A VGA dToF chip with full per-pixel histograms of 256 bins × 12 bits would need $307{,}200\times256\times12\approx0.94$ Gbit of on-chip memory [E]. dToF chips therefore share TDCs and memory across macro-pixels (4 × 4 SPADs on the VL53L5), histogram by zone, find peaks on the fly, and put the logic on a stacked wafer (§C6).
- **What dToF buys:** time gating against sunlight, separate multiple echoes, and a longer reach per joule.
- **ST's own precision claim follows the $1/f_m$ law.** ST says the VD55H1 gives "depth precision twice as good as typical 100 MHz modulated sensors" [T]: at equal phase noise, $c/(4\pi f_m)$ is 0.12 m/rad at 200 MHz against 0.24 m/rad at 100 MHz.

**The line is blurring.**
- **Pulsed ("hybrid") iToF** from Infineon/pmd and Opnous uses a short pulse and two or three gated taps, and reads the delay from the charge ratio. It keeps the dense analog pixel and gains some time gating.
- **SPAD-based iToF and gated photon counting** feed SPAD events into counters correlated with the modulation, at up to GHz rates in research.
- **The two underlying axes** are how the pixel detects (an integrating linear photodiode versus a counting Geiger-mode SPAD) and how it gets time (phase correlation versus time stamping). Commercial "iToF" and "dToF" are the two common combinations.
