#### 10.8 Benchmark against published systems

The model of 10.2–10.4 predicts how much light a design collects and how much it needs. This part tests those predictions against published systems that state their power, their beam or aperture, and a measured range or SNR. It checks three things:
- **the geometry:** the flat near field and the far-field fall;
- **the absolute level:** photons collected against photons needed;
- **the efficiencies assumed in 10.4.**

Coherent systems publish enough to test all three. ToF systems rarely publish their receive aperture, so for them the test runs backwards: it asks what aperture and efficiency the model needs to reproduce the published range, and whether those are plausible.

**Coherent (FMCW) systems.**

| System | Published inputs | Model | Published result | Agreement |
|---|---|---|---|---|
| Waymo design point (Piggott et al. 2025, Table 1) | 1,550 nm; collimated beam, $w_0=10$ mm; 0.52 µJ per point over two chirps; 5% target at 250 m; lossless optics, QE 0.9; four speckle looks | Link loss −106.2 dB (Eqs. (33)–(34)); 49 photons per chirp; $P_D=0.895$ at $10^{-6}$ per bin with four looks (Eq. (39)) | −106.1 dB; 50 photons; $P_D=0.9$ | 0.1 dB |
| Waymo lab validation (same paper, App. A) | 1,550 nm; 1 GHz chirps of 8.3 µs; diffuse 84% target at 8 and 15 m; measured chain 0.403 (optics) × 0.549 (circulator and coupler) × 0.760 (QE) × 0.667 (Hann window) = 0.112 | Eq. (33) with the measured efficiency; flat inside $z_R$ | Matches their link equation, independent of range | Shape and level ✓; efficiency 0.112, not 0.25 |
| Pointcloud array (Settembrini et al. 2026) | 1,310 nm; 178 µW per pixel; 32 µs chirps (11.4 nJ per point); waist 1.31 mm at 11.1 m, measured with a camera; $\eta_p=0.23$; 0.95 A/W; noise 5.6 dB above the shot-noise limit | SNR 57.6 (in their convention, SNR = 2N) on the 50% target at 7.2 m | 74.7. SNR against distance on cardboard (4–22 m) follows their Gaussian-mode model to 17 m and exceeds it by 1–3 dB beyond | About 1 dB; shape ✓ |
| indie / MicroTech whitepaper (2023) | 1,550 nm; 200 mW; 12 mm aperture; $z_R\approx70$ m | Flat to $z_R$, then −1.8, −4.8 and −9.6 dB at 50, 100 and 200 m | Flat from 1 to 20 m, then −3.1, −8.1 and −16.1 dB | Plateau ✓; falls 1–6 dB faster beyond $z_R$ |
| Wang et al. 2025 (RoboSense and SUSTech) | 1,550 nm; 100 kHz laser; 7 mm waist diameter (56.8 mm at 200 m); 1.5 m board of 10%; four dual-polarization receivers; SNR ≥ 10 dB to 200 m; transmit power not published | 20 → 200 m: −16.0 dB of beam spreading and −3.3 dB of coherence loss, −19.3 dB in all | −15 to −15.5 dB | Falls 3–4 dB more gently; matches a 5 mm waist |

*How the numbers are derived* [E]:
- **Waymo design point.** $z_R=\pi(0.01)^2/1.55\times10^{-6}=203$ m, so $w(250)^2=2.52\,w_0^2$. Eq. (33) with $t^2=1$ and $\rho=0.05$ then gives $0.05\times(1.55\times10^{-6})^2/(2\pi^2\times10^{-4}\times2.52)=2.4\times10^{-11}$, i.e. −106.2 dB. That is $0.52\ \mu{\rm J}/1.28\times10^{-19}\ {\rm J}\times2.4\times10^{-11}=98$ photons per point, and at QE 0.9 about 44 photoelectrons per chirp: the ≈45 that Eq. (39) gives for $P_D=0.9$ with four looks at $10^{-6}$ per bin.
- **Pointcloud array.** The camera-measured beam has $w(7.2\ {\rm m})=1.31\ {\rm mm}\times\sqrt{1+(3.9/4.1)^2}=1.80$ mm.
  - With $\eta=\eta_p$, Eq. (33) gives $P_{\rm RX}/P_{\rm TX}=0.23\times0.5\times(1.31\ \mu{\rm m})^2/(2\pi^2\times(1.80\ {\rm mm})^2)=3.1\times10^{-9}$ for the 50% target.
  - In one 32 µs chirp that is $0.95\ {\rm A/W}\times178\ \mu{\rm W}\times3.1\times10^{-9}\times32\ \mu{\rm s}/q=104$ photoelectrons.
  - The measured amplifier noise leaves 28% of that SNR (their $\kappa=0.62$, i.e. $1/(1+1/\kappa^2)$), i.e. 28.8, or 57.6 in their convention, against 74.7 measured.
  - Their own form of the link equation has no polarization factor of ½, so it predicts twice as much; the data lie between the two.
- **Wang.** $z_R=\pi(3.5\ {\rm mm})^2/1.55\ \mu{\rm m}=24.8$ m.
  - Beam spreading from 20 to 200 m costs $10\log_{10}[(1+(200/24.8)^2)/(1+(20/24.8)^2)]=16.0$ dB.
  - The coherence factor $e^{-4\pi\Delta\nu R/c}$ in their own SNR formula, the same as $e^{-2\pi\Delta\nu\tau}$ of §C7b, adds 3.3 dB for $\Delta\nu=100$ kHz.
  - The measured fall of 15–15.5 dB fits a 5 mm waist ($z_R\approx50$ m), not the 3.5 mm stated; the paper does not allow the cause to be identified.
  - With transmit power unpublished, only an estimate is possible. Their 1–2 mW local oscillator makes the receiver shot-noise limited, so 10 dB at 200 m implies $P_{\rm TX}\eta\approx$ 5–11 mW, i.e. 18–36 mW transmitted at $\eta=0.3$.

**What the coherent comparison shows.**
- **Geometry.** The flat near field and the fall beyond $z_R$ appear in every measured data set. The distance of the 3 dB fall-off scales with the square of the waist, as Pointcloud's simulations with camera-measured waists confirm. At 200 m the measured fall lies within ±3–6 dB of the nominal-beam model: steeper for indie, gentler for Wang.
- **Detection statistics.** Waymo's design needs the same ≈45 photoelectrons for $P_D=0.9$ with four looks that Eq. (39) gives at $10^{-6}$ per bin. Pointcloud's measured detection probability against SNR follows the single-speckle law $\exp[-x_{\rm th}/(1+{\rm SNR})]$ of Eq. (38).
- **Efficiency.** It is the weakest input. The 0.25 of 10.4 lies above both measured chains, 0.112 for Waymo's fibre-optic bench and 0.057 effective for Pointcloud's integrated array, as 10.1 notes.

**Direct-detection ToF systems.** Eqs. (30) and (41) with $\bar n=n_{\rm req}$ give the product of efficiency and receive area that a published range requires:
$$\eta A_{\rm rx}=\frac{n_{\rm req}\,E_{\rm ph}\,\pi R^2}{\rho\,E_{\rm tx}} . \tag{911}$$
Here $E_{\rm tx}$ is the energy per point, $R$ the published range on a target of reflectance $\rho$, and $n_{\rm req}=25$ the model's bright-sun count (10.4). The model's own receiver, 0.145 × a 25 mm lens, has $\eta A_{\rm rx}=0.71$ cm².

| System | Published | Energy per point | Required $\eta A_{\rm rx}$ | Implied receiver |
|---|---|---|---|---|
| Sony, Kumagai et al. (ISSCC 2021) | 905 nm, 45 W × 4.5 ns pulses every 3.04 µs, each lighting a vertical line of 63 macro-pixels; 168×63 points at 20 fps; PDE 22%, 6 ns dead time; 150 m on 10% at 117 klux | ≈0.29 µJ (≈89 shots per point) | 0.14 cm² | 12–14 mm lens at optics 0.7–0.5: about f/1 for the 11.5 mm focal length implied by its 0.15° pixel ✓ |
| Toshiba, Yoshioka et al. (ISSCC 2018) | 905 nm, 50 mW, 240×96 points at 10 fps; 200 m on 10% at 70 klux (92.7% success); accumulates up to 9 neighbouring pixels | 217 nJ | 0.32 cm² (0.035 cm² with 9-pixel accumulation) | 20–28 mm at $\eta=$ 0.10–0.05 ✓ |
| Toyota, Niclass et al. (ISSCC 2013; numbers from Toshiba's comparison table) | 870 nm, 21 mW, 202×96 points at 10 fps; 100 m on 9% at 70 klux | 108 nJ | 0.18 cm² | 15–22 mm at $\eta=$ 0.10–0.05 ✓ |
| Panasonic flash, Hirose et al. (2018) | 940 nm, four 300 W sources, ≈10 ns pulses spread over 688×384 pixels; f/1.4 lens | 45 pJ per pixel per pulse | — | The model gives 0.13–0.53 photons per pixel per pulse at 100 m; the paper says below one beyond 100 m ✓ |

*How the numbers are derived* [E]:
- **Sony's energy per point is my reading of its timing diagram, which states no shots per point.**
  - The laser fires every 3.04 µs during 721.76 µs of each 761.6 µs slot, i.e. 237 shots per slot.
  - The mirror sweeps the 168 columns once per slot, with 63 slots per frame, so each column receives $237/168\times63\approx89$ shots.
  - Each 202 nJ pulse is shared by 63 macro-pixels, so a point receives $89\times202/63\approx290$ nJ.
- **Sony's lens.** Eq. (911) then asks for $25\times2.20\times10^{-19}\times\pi\times150^2/(0.1\times2.9\times10^{-7})=1.4\times10^{-5}$ m². With $\eta=$ 0.5–0.7 (optics) × 0.22 (PDE) × 0.784 (live fraction, §C6), that is a lens of 12–14 mm.
- **Toshiba and Toyota** publish laser power but not optics or PDE, so a range of $\eta$ is shown. Their $\eta A_{\rm rx}$ is 2–4× below the model's 0.71 cm², consistent with the lower PDE of 2013–2018 detectors.

**Products: what their claims imply.** No automotive product publishes both its laser energy and its receive aperture, so the model can only say what a claimed range requires [E]. For photon-counting scanners the inputs are the model's $n_{\rm req}=25$ and $\eta=0.145$ (a PDE of 37%), with 20–30 mm lenses; a lower PDE raises the energy in proportion.
- **Ouster OS2-128 Rev7** (SPAD receiver): 865 nm; 200 m on 10% at more than 90% detection probability in 100 klx, in its 1024 × 10 Hz mode (1.31 Mpts/s). It needs 70–158 nJ per point, i.e. 0.09–0.21 W average optical power.
- **Hesai AT128** (onsemi SiPM receiver, whose PDE is not public and is likely below 37%): 905 nm; 210 m on 10%; 1.54 Mpts/s. At the model's efficiency it needs 74–167 nJ, i.e. 0.11–0.26 W, and proportionally more at a lower PDE.
- **Analog Photonics FS-4S** (FMCW phased array; datasheet quoted in Pointcloud's peer-review file). It claims 200 m on 10% at 90 kpts/s in its region-of-interest mode, and 80 m at 400 kpts/s in its base mode, with a beam of at most 0.04° × 0.02° FWHM.
  - That beam means waists of only 0.83 × 1.66 mm, so 200 m lies deep in the far field, with a link loss of −117.6 dB.
  - It then needs 9 µJ per point at $\eta=0.25$, or 20 µJ at 0.112, i.e. 0.8–1.8 W of optical power.
  - In the far field range grows as the square root of energy per point. Its 4.4× more energy per point in the region-of-interest mode then predicts $80\times\sqrt{4.4}=170$ m, against the 200 m claimed.
- **Reflectance scaling in sunlight.**
  - Ouster quotes 200 m on 10% and 350 m on 80%, a ratio of 1.75. That fits $R\propto\rho^{1/4}$ (1.68), not $\rho^{1/2}$ (2.83).
  - In full sun the target's own sunlit radiance is the background, so a brighter target also raises the background, and range follows the background-limited law of subsection 1.
  - The model of 10.4 holds the background fixed, and so scales as $\rho^{1/2}$: it is optimistic for bright targets in full sun and pessimistic for dark ones.

**What the benchmark says** [E]:
- **The coherent link equation holds.** Eq. (33), with its flat near field, reproduces every coherent system whose beam and efficiency are published to within about 1–3 dB. At 200 m the far-field fall matches the nominal beam to within ±3–6 dB.
- **Efficiency is the weak input.** Measured coherent chains reach 0.057–0.17 against the 0.25 used in 10.4 (see 10.1).
- **ToF is consistent but not tested absolutely.** The model's figures match every published research sensor, given f/1-class lenses of 10–30 mm and PDEs of 5–22%. Because products publish neither laser energy nor aperture, the absolute ToF level cannot be tested against them.
- **Product claims imply undisclosed powers:**
  - about 0.1–0.3 W average optical power for 865–905 nm photon-counting scanners;
  - 0.8–1.8 W for a small-aperture FMCW phased array at 200 m;
  - and, for SPAD sensors in full sun, range scaling with reflectance closer to $\rho^{1/4}$ than the $\rho^{1/2}$ the model assumes.
