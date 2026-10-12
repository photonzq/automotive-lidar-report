#### 10.7 Dynamic range: strong returns, blooming and blinding

10.6 asked how much light a design has to spare for weak returns. The same excess light appears as a burden for strong ones. A receiver must detect the weakest return it is specified for and still range the strongest one correctly. In between it must stay linear, or at least saturate gracefully, recover quickly and not spill light into neighbouring pixels. This part sizes that span for the designs of 10.6, describes the failure modes documented for ToF receivers, and says what coherent detection changes and what it does not. The problem is well studied. Vendors publish firmware fixes for it, China's national lidar standard tests one of its artefacts, and open benchmarks have found it in production sensors.

**How large the span is.** Let the dynamic range a design must handle be the ratio of the link loss of the strongest return that must still be ranged correctly, $\mathcal{L}_{\max}$, to the detection level:
$$\mathcal{D}=\frac{\mathcal{L}_{\max}}{\mathcal{L}_{\rm det}},\qquad 10\log_{10}\mathcal{D}=10\log_{10}\frac{\rho_{\max}}{\rho_0}+M(R_{\min}) . \tag{907}$$
Here $\rho_{\max}$ is the effective reflectance of the strongest target, $R_{\min}$ the shortest range at which it must be measured, $\rho_0=10\%$ the reflectance the design is sized for, and $M$ the margin of Eq. (46). The second form holds because both link losses are proportional to reflectance (Eqs. (30) and (33)). In words: the span a receiver must handle is the reflectance span plus the short-range margin of 10.6. The excess light that protects direct detection against dirt and fog is the same excess light its receiver must survive, and FMCW has little of either.

**Retroreflectors as effective reflectances.** A retroreflector is specified by its coefficient of retroreflection $R_A$ (cd·lx⁻¹·m⁻²): the intensity it returns per unit illuminance and per unit area, in units of sr⁻¹. A Lambertian surface of reflectance $\rho$ returns $\rho/\pi$ in the same units, so the retroreflector acts like a Lambertian surface of reflectance
$$\rho_{\rm eq}=\pi R_A . \tag{908}$$
- **Road-sign sheeting.** White sheeting of ASTM D4956 Types I and III has $R_A=70$ and 250 at 0.2° observation and −4° entrance, i.e. $\rho_{\rm eq}\approx220$ and 790 [P]. New sheeting of EN 12899-1 class RA2 measured 414–769, i.e. $\rho_{\rm eq}=$ 1,300–2,400 [I].
- **Licence plates.** ISO 7591 specifies 30–45 at 0.2° observation, with a maximum of 250 [P].
- **These are floors for lidar.** They are measured in visible light at observation angles of 0.2–0.33°, while a monostatic lidar looks back at nearly 0°, where retroreflection is stronger.
- **Measured at a lidar wavelength.** In the 1,310 nm coherent array of Settembrini et al. (2026), a retroreflector at 7.2 m returned 31.8 dB more than a 50% Lambertian target [P]. By Eq. (908) that is $\rho_{\rm eq}=0.5\times10^{3.18}\approx760$, i.e. $R_A\approx240$, close to Type III sheeting.
- **Overall span.** Waymo puts real scenes at more than 50 dB of reflectance: a retroreflector can exceed 1,000× a Lambertian target, and a wet dark car can fall below 1% (Piggott et al. 2025) [P].
- **Value used below.** As in §C10.2, item 4, a bright sign is taken as $R_A=500$, i.e. $\rho_{\rm eq}=1{,}571$, 42.0 dB above a 10% target.

| Strongest return, relative to the weakest detectable return | SPAD ToF, 25 mm lens | FMCW, 22 mm (best for 200 m) | FMCW, 13 mm | FMCW, 7 mm |
|---|---|---|---|---|
| White 90% target at 1 m | 55.7 dB | 12.6 dB | 19.3 dB | 29.6 dB |
| White 90% target at 0.3 m | 66.2 dB | 12.6 dB | 19.3 dB | 29.6 dB |
| Retroreflective sign ($R_A=500$) at 30 m | 58.6 dB | 44.9 dB | 51.0 dB | 56.9 dB |
| Retroreflective sign at 5 m | 74.1 dB | 45.0 dB | 51.7 dB | 61.8 dB |
| Retroreflective sign at 2 m | 82.1 dB | 45.0 dB | 51.7 dB | 62.0 dB |

*How the numbers are derived* [E]: each design of 10.6 is sized to reach exactly 200 m on a 10% target, so its detection level equals its link loss there, and every entry is Eq. (907) with clear-air loss included.
- **ToF, sign at 5 m:** $10\log_{10}(1{,}571/0.1)=42.0$ dB, plus the margin $20\log_{10}(200/5)=32.0$ dB, plus 0.15 dB of clear-air loss at 200 m, gives 74.1 dB.
- **Best FMCW, sign at 5 m:** 42.0 dB plus $10\log_{10}[2/(1+(5/200)^2)]=3.0$ dB, i.e. 45.0 dB. Inside the Rayleigh range the value hardly depends on range.
- **Polarization.** The coherent entries treat the sign like a depolarizing target. A retroreflector largely preserves polarization, so a single-polarization receiver, or the co-polarized looks of the four-look receiver of 10.3, see it up to 3 dB stronger than the table. Summed over both polarizations, the table holds.

**Optical span and electrical span.** What the electronics must handle depends on how the receiver converts light into current:
$$20\log_{10}\frac{i_{\max}}{i_{\min}}=\begin{cases}2\times10\log_{10}\mathcal{D} & \text{direct detection, } i\propto P,\\[2pt] 10\log_{10}\mathcal{D} & \text{coherent detection, } i\propto\sqrt{P\,P_{\rm LO}} .\end{cases} \tag{909}$$
- **Direct detection.** A photocurrent proportional to optical power doubles the dB span. The ToF design's 74 dB for a sign at 5 m becomes 148 dB at the amplifier input.
- **Coherent detection.** The beat current is proportional to the optical field, the square root of power, so the span keeps its optical value (Piggott et al. 2025) [P]. The best FMCW design's 45 dB needs about 7.5 bits of an analog-to-digital converter (ADC) at 6 dB per bit.
- **Photons, ToF.** Per shot the SPAD design emits 7.6 nJ (its 76 nJ over ten shots). The sign at 5 m then returns about $3.5\times10^{8}$ photons, $6.5\times10^{7}$ of them detected, against 2.5 detected photons per shot from the weakest return the design must see [E].
- **Photons, FMCW.** The same sign sends about 49 nW into the best FMCW design's mode, against a local oscillator of about a milliwatt, so its photodiodes stay linear [E, 30 mW transmitted].

**What ToF receivers can span.**
- **SPADs:** a SPAD fires at most once per dead time. Sony's automotive SPAD has a 6 ns dead time and 3×3 SPADs per macro-pixel, so a macro-pixel registers at most nine counts per shot [P; §C6].
- **Linear amplifiers:**
  - TI's LMH32401 amplifier, at its 20 kΩ gain, has a 1.5 V output swing, so it is linear up to about 75 µA of input current, against 49 nA rms of noise [P].
    - That is a linear range of about 63 dB in current, which by Eq. (909) is only about 32 dB of optical span for a direct detector.
    - Beyond it, a clamp limits the input to 100 mA [P].
  - Maxim's MAX40660 recovers from a 100 mA overload in 2 ns [P].
- **The span of the returns is larger still.** Kurtti et al. put the span of automotive return amplitudes at up to 1:10⁵ in photocurrent, with inputs up to about 100 mA [I].
- ToF receivers are therefore designed to saturate gracefully rather than to stay linear over the full span.

**How strong returns fail in ToF lidars** (each item is documented in the sources listed):
1. **Range walk.** Strong echoes read too short.
   - *SPAD pile-up.* The first photons of a strong echo fire the SPADs, which are then dead for the rest of the pulse, so detections pile up on the leading edge. Ouster's firmware 1.12 fixed retroreflectors that appeared 20–40 cm too close [P]. An Ouster patent attributes errors of this size, about 37 cm on a licence plate, to a matched filter applied to a piled-up return [P].
   - *Linear receivers.* With a fixed threshold, a strong pulse crosses it earlier than a weak one. Kurtti et al. measured 2.5 ns of walk (37 cm) over inputs of 1 µA to 100 mA, from a receiver linear only to about 70 µA. Corrections that use the measured pulse width reached ±4 mm over a 1:10⁵ span [I].
2. **Blooming**, a halo of false points around a bright object, usually at its range.
   - *Glare inside the receiver.* In arrays that share one lens, light reflected between lens and sensor, and scattered in the optics, reaches neighbouring pixels. Gump et al. (CVPR 2026) model this as a glare spread function; on a commercial SPAD sensor they cut the depth error on a stop sign from 0.52 to 0.11 m RMS [I].
   - *The weak edge of the beam.* Even the faint outer part of the beam returns a detectable echo from a retroreflector, widening its outline by several degrees (Dudzik et al. 2025) [I].
   - *Crosstalk between channels.* Velodyne's patent fires one laser at a time partly to avoid retroreflector crosstalk [P].
   - *Criterion* [E]: a neighbouring pixel stays clean only if the fraction $\varepsilon$ of the bright return that reaches it satisfies $\varepsilon\,\mathcal{D}<1$. That is $\varepsilon<-74$ dB for the ToF design and a sign at 5 m, more suppression than lens and window scattering usually provide.
3. **Ghosting.** Copies of the bright object appear elsewhere.
   - Part of the beam reflected off the window leaves in another direction, and its echo is logged along the main beam (a Waymo patent) [P].
   - Strong echoes from beyond the maximum range land in the next listening window [P].
4. **Blinding.**
   - An overloaded amplifier stays blind until it recovers.
   - A SiPM saturated by the reflection from its own window leaves a blind zone of about 3 m after a 20 ns recovery (a patent) [P].
   - Ouster's firmware 3.1 fixed bright objects inside the minimum range deleting other objects [P].

**Tests and evidence.**
- **Standards:**
  - China's national standard GB/T 45500-2025 includes a pass/fail "high-reflectivity ghost" test on a board of Class V retroreflective sheeting, and a test for trailing points. Secondary summaries give the false-point limit as 0.1% or 1%, and none lists a blooming or dynamic-range test [P/T].
  - ISO/FDIS 13228 names ghost points in its scope [I]. DIN SAE SPEC 91471 includes a retroreflector among its targets [P].
- **Open benchmarks:**
  - The SPIE/SAE lidar benchmark tested 8 lidars in 2022 and 9 in 2023. It placed road signs beside a 10% "child" target: the signs sharply cut detection range and often merged the child with the sign. Results per vendor were not published [I].
  - NIST (2024) put retroreflectors in front of a 5.9% black panel. One SPAD lidar lost the points on half the panel [I].
- **Vendors market fixes** [P]:
  - RoboSense (M1, 2021) claims ghosting removed and a minimum range of 0.3 m on licence plates.
  - Hesai (ETX, 2025) claims 95% fewer false positives on highly reflective objects.

**What coherent detection changes.**
- **A smaller span, compressed again by field detection.** From the table and Eq. (909), the best FMCW design handles 45 dB where the ToF design faces 148 dB at its amplifier.
- **The time-domain signal stays small** [E].
  - Suppose the weakest return has a per-bin SNR of about 15 dB.
  - The sign is then about 60 dB above the noise in its FFT bin.
  - An FFT over 10 µs sampled at 1 GS/s gains about 40 dB, so before the FFT the sign's tone is only about 20 dB above the noise, which does not stress the ADC.
- **Spatial filtering** [E].
  - Stray light is detected only if it couples into the LO's single mode.
  - That mode accepts an étendue of about $\lambda^2$, against $A_{\rm rx}\Omega_{\rm px}=4.9\times10^{-4}\ {\rm m^2}\times(1.75\ {\rm mrad})^2=1.5\times10^{-9}$ m² sr for a 25 mm lens with a 0.1° pixel.
  - For diffuse glare this suppresses coupling by about $2.4\times10^{-12}/1.5\times10^{-9}$, i.e. −28 dB.
- **Evidence.**
  - Settembrini et al. (2026) saw no noticeable blooming from a retroreflector beside a 5% target at 7.2 m, although the retroreflector was 37.7 dB brighter [P].
  - Aeva describes its sensor as "inherently free from retroreflector blooming and ghosting" (2023); Mobileye, SiLC and Voyant make similar claims [P]. None has been tested independently.
- **What does not go away:**
  - *Beam sidelobes.* A retroreflector seen through the transmit beam's own angular sidelobes returns into the same mode, weighted by the two-way pattern. Sidelobes therefore matter for both architectures, as in the phased-array case of §C10.2, item 4.
  - *Clipping.* Strong beats that clip the ADC create harmonics and ghost tones; an Aeva patent uses frequency-domain gain control against them [P].
  - *Window sidelobes.* The FFT sidelobes of a strong beat can mask a weak one at a nearby beat frequency.
    - Harris (1978) tabulates highest sidelobes of −13 dB for a rectangular window, −43 dB for Hamming and −67 to −92 dB for Blackman–Harris windows, which have wider main lobes [I].
    - Waymo uses a Hann window (about −31 dB), which cost 1.8 dB of SNR (a factor of 0.667) in its measurement [P].
  - *Laser phase noise.* The skirt of the strong zero-range reflection from the window sets the minimum range of a monostatic FMCW lidar (Piggott et al. 2025) [P].
  - *Pairing ghosts.* With several targets in one beam, pairing up- and down-chirp peaks can create ghost points. Waymo proposes three or more chirps, or phase codes [P].

**What this means** [E]:
- **ToF.** Dynamic range is the flip side of its robust margin. The receiver cannot stay linear over 70–80 dB of optical span (140–160 dB electrical), so products rely on graceful saturation, walk correction, glare suppression and filtering. Standards now test some of the resulting artefacts.
- **FMCW.**
  - Its burden is 25–30 dB smaller for the large-aperture designs, and electrically halved.
  - Its remaining strong-return problems are spectral (sidelobes, harmonics, phase noise, pairing), handled by windowing and gain control.
  - The robust small-aperture designs of 10.6 give back part of this advantage (62 dB for 7 mm), because beyond their short Rayleigh range they collect like direct detection.
