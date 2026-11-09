"""Add §C5b (colour lidar: Ouster's L-series SPAD chips, the colour products of Ouster, Hesai, RoboSense and Huawei,
and what colour channels cost in range) before §C6. Point to it from the scope list, §C0's relation table, §C3, §C4b,
§C5, §C10.6, §E10.4, §E11.2 and §F5, and add two Appendix 1 items. Also list the new figure script in build/README.md
and update the equation number that build/figures/fmcw_tof_system_budget.py quotes by hand: the two new equations of
§C5b move eq:fmcw-dwell from (122) to (124).

Usage: colour_lidar_edit.py <report folder> <expected report sha256 prefix> [--write]
Each report anchor must match exactly once, the figure script's quote exactly twice, and the starting hash must
match. Inserted text is normalised to the report's code points (micro sign U+00B5, straight quotes). Files keep
their LF line endings. Without --write the script only checks.
"""
import hashlib
import sys
from pathlib import Path

folder, expected = Path(sys.argv[1]), sys.argv[2]
write = "--write" in sys.argv[3:]
report = folder / "automotive_perception_report_2026-09-27.md"
readme = folder / "build" / "README.md"
fmcw = folder / "build" / "figures" / "fmcw_tof_system_budget.py"


def load(path):
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    assert "\r" not in text, f"{path.name}: expected LF line endings"
    return raw, text


def normalise(s):
    """Use the report's code points: micro sign, straight quotes."""
    return (s.replace("μ", "µ").replace("‘", "'").replace("’", "'")
            .replace("“", '"').replace("”", '"'))


raw, text = load(report)
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"

C5B = r"""## C5b. Colour lidar: colour channels on the SPAD chip, and what they cost in range

In 2026 two makers of SPAD-SoC lidars put colour sensing on the ranging chip: Ouster's Rev8 sensors and Hesai's Picasso chip give every point a colour (red, green and blue, RGB) as well as a range. This applies the SPAD-SoC's integration advantage (§C4b) to camera–lidar fusion, and it bears on the pixel-aligned RGB-D argument of §C10.6 and §E11.2. The colour channels share the focal plane, the optics and sometimes the spectral pass band with the ranging channels, and depending on the layout that sharing can cost range in sunlight. This subsection describes the chips that Ouster's colour runs on, what "colour lidar" denotes, how the products differ, and what colour costs in range.

### Ouster's L-series SPAD chips

**The architecture has not changed since 2018.** An array of 865 nm VCSELs (vertical-cavity surface-emitting lasers) fires through one lens. The echoes return through a second lens onto a single CMOS chip that holds both the SPADs and the logic that turns photon arrival times into ranges, and the head spins. Each channel has its own aperture, collimating micro-lens and filter in front of its detector, which Ouster's patents describe as one or more SPADs counting photons [P, US 10,739,189 B2]. In 2018 Ouster credited the OS1-64's chip with counting more than $10^{12}$ photons per second into on-chip memory, with more than 100 GMAC/s (billion multiply–accumulate operations per second) of logic in more than ten million transistors. It put the efficiency of the SPADs of the time at 2–5%, against 20–30% at 850 nm for the newest ones [P, quoted by Image Sensors World].

| Chip | Introduced | Public information |
|---|---|---|
| First generation | 2018 (OS1-64) | More than $10^{12}$ photons/s, more than 100 GMAC/s, more than $10^{7}$ transistors [P] |
| L2X | Oct 2021 | 128-channel SPAD array [P, Form 10-K for 2021]; about twice the previous chip's data rate at similar size and power [P] |
| L3 | 2022 (Rev7) | Stacked and back-illuminated, made by STMicroelectronics, 10 µm SPAD pitch [I, TechInsights]; about 125 M transistors and 21.47 GMACS; up to about $10^{13}$ photons/s and ten times the photon sensitivity [T] |
| L4 and L4 Max | May 2026 (Rev8) | 128 or 256 channels; up to $2\times10^{13}$ photons/s; 42.94 GMACs; a 40 kHz measurement rate; 22.4 Gb/s off the chip; up to 10.4 Mpts/s; Fujifilm colour filters on the chip [P]. Foundry, process node and pitch are not published |
| Chronos | Announced Mar 2022 | Chip for the solid-state DF series, with tape-out planned for late 2022 [S]; DF never shipped (§C3b) |

**TechInsights' teardown of the L3 is the most detailed independent source.** It identifies the L3 as a stacked, back-illuminated direct-ToF SPAD sensor made by STMicroelectronics with a 10 µm pixel pitch. It lists hybrid bonding, a quench resistor inside the die, double deep-trench isolation, a finger capacitor and a diffraction grating, and it ranks the chip as a direct competitor of Sony's IMX459 [I]. Ouster called the L3 the first back-illuminated chip in lidar [T], but Sony had announced its stacked, back-illuminated IMX459 for automotive lidar in September 2021 (§C5a).

**These structures answer silicon's weak absorption at 865 nm.** A log-linear extrapolation of the Green 2008 values used in §C4 (absorption lengths of 35 µm at 905 nm and 55 µm at 940 nm) gives an absorption coefficient $\alpha_{\rm Si}\approx4.9\times10^2$ cm⁻¹ at 865 nm, an absorption length $1/\alpha_{\rm Si}\approx20$ µm [E]. The sensitive layer of a back-illuminated SPAD is a few micrometres thick, so a single pass absorbs the fraction $1-e^{-\alpha_{\rm Si}d}$, where $d$ is the layer thickness: $1-e^{-0.147}=14\%$ for $d=3$ µm and $1-e^{-0.245}=22\%$ for $d=5$ µm [E].
- The grating sends the light into steep angles and the trenches act as side mirrors, so photons cross the thin layer several times.
- The trenches also keep avalanche glow, the light that hot carriers emit in a firing SPAD, from triggering its neighbours.
- Hybrid bonding puts the logic on a second wafer under the SPADs, which is how the L3 holds about 125 M transistors.
- The same recipe raised Sony's PDE from the 2–5% of front-illuminated SPADs to 24% at 905 nm (§C4), and it is consistent with the step from Ouster's 2018 efficiencies to its claimed tenfold sensitivity gain for the L3 [E].

**What Ouster's chip figures mean** [E]:
- *The 40 kHz measurement rate is the column rate.* With $N_{\rm col}$ columns per revolution and a rotation rate $f_{\rm rot}$, the column rate is $f_{\rm col}=N_{\rm col}f_{\rm rot}$. The Rev8 OS1's fastest modes, 1,024 × 40 Hz, 2,048 × 20 Hz and 4,096 × 10 Hz, all give $f_{\rm col}=40{,}960$ s⁻¹ (datasheet v4.0, p. 3). With $N_{\rm ch}=128$ channels and $N_{\rm ret}=2$ returns, $N_{\rm ch}f_{\rm col}N_{\rm ret}=128\times40{,}960\times2=10{,}485{,}760$ points/s: the datasheet's maximum (p. 2) and the dual-return figure of §C3b.
- *The picosecond timing is that of a histogram centroid.* The best range precision, $\sigma_R=0.25$ cm at one standard deviation (p. 2), corresponds to a timing precision $\sigma_t=2\sigma_R/c=2\times2.5\times10^{-3}\ {\rm m}/(3.00\times10^{8}\ {\rm m/s})=16.7$ ps, and the 0.1 cm range step to 6.7 ps. These are precisions of a centroid estimated from many photons, not of one detection.
- *The photon figure is a capacity rating.* Spread over 128 channels, $2\times10^{13}$ photons/s is $1.6\times10^{11}$ s⁻¹ per channel. A SPAD with dead time $\tau_d$ counts at most $1/\tau_d$, i.e. $10^{8}$–$10^{9}$ s⁻¹ for $\tau_d$ = 10–1 ns, so the figure implies hundreds to thousands of SPADs per channel, or a counting basis that Ouster does not state.
- *The GMAC figures are not comparable across generations.* The 2018 chip was already credited with more than 100 GMAC/s, against 21.47 GMACS for the L3 and 42.94 for the L4.

### What "colour lidar" denotes

The term means that each 3D point carries a colour as well as its range and its infrared return strength. Four constructions are sold or described under it:
1. **Software colouring.** A separate camera is calibrated to the lidar and its pixels are projected onto the points, as mapping systems have long done. The colour suffers from parallax at depth edges (a point on a sign takes the colour of the wall behind it), from calibration drift with heat and vibration, and from the timing difference between a camera exposure and a scan.
2. **A lidar and a camera in one housing** (RoboSense's Active Camera, below). The two are synchronised in hardware and calibrated at the factory. They still look through two lenses, so parallax remains, but the user no longer calibrates.
3. **Colour on the ranging chip, behind the ranging lens.** Colour-filtered photon-counting channels sit on the lidar's own receiver chip, so colour and range are registered by construction, without parallax or extrinsic calibration. Ouster calls this native colour, and Hesai calls it 6D full colour (XYZ plus RGB).
4. **Active multi-wavelength lidar.** The laser itself carries several wavelengths, so colour works in darkness. This is a research and airborne-survey technique, not offered for cars or robots [U].

In constructions 1–3 the colour is passive: it comes from daylight or street lighting reflected by the scene, not from the 865–905 nm laser.

### The products compared

| Product | Where the colour is measured | Optics shared with ranging | Published colour specifications | Status |
|---|---|---|---|---|
| Ouster Rev8 (L4, L4 Max) | Colour-filtered SPAD channels on the ranging chip, with Fujifilm organic filter materials [P] | One lens and one aperture plane [P] | 116 dB dynamic range; 3 lux at SNR 10 dB; 2,000,000 lux maximum; sensitivity metamerism index (SMI) 80; 16 bits per channel [P] | Launched 4 May 2026, with datasheets [P] |
| Hesai Picasso (ETX) | RGB sensing and ToF ranging on one SPAD-SoC [P]; a 2026 patent shows an RGB SPAD array beside a filtered depth array [T] | Not stated | None | Mass production planned for H2 2026; the ETX was in customer validation in Aug 2026 [P] |
| RoboSense Active Camera (AC1, AC2) | A separate RGB camera (two on the AC2) beside a solid-state dToF lidar, synchronised in hardware [S] | No: two lenses | Camera resolution (1,600 × 1,400 on the AC2) [S] | Sold for robots |
| Huawei Limera | A coaxial lidar–camera unit with a Huawei SoC (§C3, §D1a, §F5) | One optical axis, separate detectors [U] | None found | In-cabin product |

**Ouster's colour.** Ouster's release with Fujifilm (19 May 2026) says that the colour comes from Fujifilm's organic colour-filter materials, built into the L4 silicon from the prototype stage. These belong to Fujifilm's Wave Control Mosaic family, which supplies the colour filters of CMOS image sensors. Colour and depth are captured and processed on one ASIC behind shared optics, with shared timing and calibration [P]. Ouster's patent US 10,739,189 B2 (priority Aug 2018) shows how a spinning sensor can do this [P]:
- each row of the receiver chip holds one ranging channel and several ambient-light channels with different filters, behind one bulk lens and one aperture plane;
- as the head turns, every channel of the row sees each direction in turn (Fig. 33B shows green, yellow, orange and red channels followed by the ranging channel), so the samples of one direction are taken at slightly different times;
- registration is exact when the angular pitch of the channels is a whole multiple of the angular step;
- the ambient channels are SPADs whose counters run for a shutter interval, while the ranging channel has timing circuits;
- variants include a hybrid pixel, with a near-infrared centre and a visible rim, and a second chip laid over the first.

Ouster has not said which layout Rev8 uses [U].

**What the Rev8 colour figures imply** (OS1 datasheet v4.0, p. 3) [E]:
- *The dynamic range is the ratio of the two illuminance limits:* $20\log_{10}(2\times10^{6}\ {\rm lx}/3\ {\rm lx})=116.5$ dB. Ouster's launch blog quotes 1 lux to 2 million lux [P], which would be 126 dB, so its 1 lux is at a lower, unstated SNR.
- *The floor is about ten photons.* For shot-noise-limited counting ${\rm SNR}=\sqrt N$, with $N$ the counts in one colour sample, so 10 dB ($\sqrt N=10^{10/20}=3.16$) means $N\approx10$, and more if dark counts matter. For scale, 3.4 lux is the dark limit of civil twilight, a full moon gives 0.05–0.3 lux and public areas with dark surroundings are lit to 20–50 lux [S, Wikipedia's illuminance table]. The colour therefore fails under moonlight alone and works under street lighting; on a car it would also work within the reach of the headlamps, and signal and brake lamps are bright emitters.
- *The top of the range cannot come from linear photon counting.* Scaling the floor gives $10\times(2\times10^{6}/3)=6.7\times10^{6}$ counts per sample. In the 97.7 µs column dwell of the 1,024 × 10 Hz mode, $1/(1{,}024\times10\ {\rm Hz})$, that is $6.8\times10^{10}$ s⁻¹, about 700 times the $10^{8}$ s⁻¹ ceiling of a SPAD with a 10 ns dead time. Ouster attributes its HDR to hardware without saying how. Dead-time-corrected estimation, which recovered a $10^{6}{:}1$ range in one exposure with a free-running SPAD [I, Ingle, Velten and Gupta, CVPR 2019], shortened gates or attenuated sub-pixels would each do. Sixteen linear bits span only $20\log_{10}2^{16}=96.3$ dB, so the output code must be non-linear or floating point.
- *The colour accuracy is camera-grade.* DxOMark gives SMI values of 75–85 for DSLRs [I]. With the commonly quoted form ${\rm SMI}=100-5.5\,\overline{\Delta E^*_{ab}}$ [S], where $\overline{\Delta E^*_{ab}}$ is the mean CIELAB colour error over the ColorChecker patches after the best colour matrix, an SMI of 80 is a mean error of $(100-80)/5.5=3.6$.
- *The time offset is negligible.* In the patent's row layout, a colour channel $k$ column steps from the ranging channel samples the same direction $\Delta t=k/f_{\rm col}$ earlier or later. At 1,024 × 10 Hz with $k=5$ (an assumed value), $\Delta t=5/(10{,}240\ {\rm s^{-1}})=0.49$ ms, in which an object closing at 30 m/s moves $30\times0.49\times10^{-3}=1.5$ cm.
- *The colour image has the lidar's resolution.* The OS1 has $44^\circ/128=0.34^\circ$ per row, while an 8 MP camera spanning 120° has $120^\circ/3{,}840=0.031^\circ$ per pixel, eleven times finer. Ouster's megapixel colour is the OS1 Max at 4,096 columns, $256\times4{,}096=1{,}048{,}576$ points per frame. If each colour sample integrates for one column dwell, 24–98 µs, it collects light for between a thousandth and a hundredth of a camera exposure of 10–30 ms; the lidar makes up for it with a larger aperture and coarser samples.

**Hesai's Picasso.** Hesai showed Picasso at its Technology Open Day on 17 Apr 2026 as a fifth-generation SPAD-SoC that combines RGB sensing with ToF ranging on one chip, so that each point carries colour natively, with a PDE above 40% at an unstated wavelength [P]. The first product, the ETX, comes with 1,080, 2,160 or 4,320 channels (two chips for 4,320) and is claimed to reach 600 m, 400 m on 10% and a 15 × 25 cm block at 150 m; Hesai calls its published point clouds prototype results [P]. Its chief scientist described image and depth functions fused so that every pixel measures both [T, Gasgoo], while a 2026 Hesai patent shows separate depth and RGB SPAD arrays (Appendix 1) [T]; which layout ships is not public. The principle is Ouster's, on a different platform: a long-range, forward-looking car lidar with thousands of detector channels rather than a spinning sensor with 128–256. If its colour followed the ETX's finest sampling, 0.06° × 0.027° (§C3b), it would rival an 8 MP camera's 0.031°, finer vertically and half as fine horizontally [E]. Hesai has published no colour SNR, dynamic range or colour accuracy.

### What colour costs in range

In full sun, the condition in which lidar range is quoted (§C3b), a SPAD channel's range is set by the solar background it collects (§C0, subsections 4.2 and 5.2). Colour costs range when it takes echo light away from the ranging SPADs or lets more background in.

**The range factor.** Let $R_0$ be the range of a receiver without colour and $R$ its range with colour, on the same target with the same laser. Two quantities describe what colour changes:
- the share $a$ of the ranging channel's collected echo light that still reaches ranging SPADs, which captures any loss that removes signal and in-band background alike, such as area given to colour pixels or an added absorbing layer;
- the factor $m$ by which the background that the ranging SPADs count per unit of $a$ rises, from light outside the laser band.

In full sun the sunlit target fills the channel's view, so the background does not depend on range, and the SNR of §C0 subsection 4.2 reduces to $N_s/\sqrt{N_b}$ with $N_s\propto a/R^2$ and $N_b\propto a\,m$; holding it fixed gives $a/R^2\propto\sqrt{a\,m}$. At night $N_b\to0$, detection needs a fixed $N_s$, and $R^2\propto a$. Hence

$$\frac{R}{R_0}=\left(\frac{a}{m}\right)^{1/4}\ \text{in full sun},\qquad \frac{R}{R_0}=a^{1/2}\ \text{at night}. \label{eq:colour-range-factor}$$

These are the background-limited and signal-limited laws of §C0 subsection 5.2. The full-sun law fits Ouster's own specifications: the OS1's 170 m on 80% and 90 m on 10% give $R\propto\rho^{0.31}$, since $\ln(170/90)/\ln8=0.31$, close to the $\rho^{1/4}$ of background-limited detection, as the OS2's figures do (§C0 subsection 6.1) [E].

**Ranging through a colour filter.** If one SPAD both ranges and senses colour, its filter must pass the laser line and a colour band. That takes a dual-band filter: an organic colour filter alone passes the whole near infrared, so the pixel would lose its colour. The background then gains the colour band. Summing Eq. \eqref{eq:solar-background-rate} over the two pass bands gives

$$m=1+\kappa_\odot\,\frac{\Delta\lambda_{\rm c}}{\Delta\lambda_{\rm L}}\,\frac{{\rm PDE}_{\rm c}}{{\rm PDE}_{\rm L}}\,\frac{\rho_{\rm c}}{\rho_{\rm L}}, \label{eq:colour-background-multiplier}$$

where:
- $\Delta\lambda_{\rm L}$ is the pass band at the laser line and $\Delta\lambda_{\rm c}$ the width of the colour band (nm);
- ${\rm PDE}_{\rm c}$ and ${\rm PDE}_{\rm L}$ are the SPAD's photon detection efficiencies in the colour band and at the laser line;
- $\rho_{\rm c}$ and $\rho_{\rm L}$ are the scene's reflectances in the two bands;
- $\kappa_\odot$ is the solar photon flux per nanometre in the colour band divided by that at the laser line. For a 5,800 K blackbody it is 1.13 between 550 and 865 nm; Rayleigh scattering, which removes more green than near infrared, brings it close to 1 at the ground. The calculation below uses $\kappa_\odot=1$; 1.13 would change the range factors by less than 3% [E].

*Inputs* [E]: a 100 nm colour band (one of red, green or blue) beside a 20 nm laser filter; ${\rm PDE}_{\rm c}/{\rm PDE}_{\rm L}$ of 1–2 (a stacked, back-illuminated SPAD can be about twice as efficient in the visible as in the near infrared, as the 81% peak PDP at 675 nm against 39% at 940 nm of the SK hynix device in §C5a shows); and $\rho_{\rm c}/\rho_{\rm L}$ of 0.3–1 (vegetation is several times brighter in the near infrared, while grey surfaces are about flat). They give $m=1+5\times1\times0.3=2.5$ for the mildest case, $m=1+5\times1.5\times0.67=6.0$ for a middle case and $m=1+5\times2\times1=11$ for a grey scene with a visible-efficient SPAD.

**Dead time adds to the cost.** The extra background also keeps the SPADs dead for longer. For paralyzable SPADs the live fraction is $\ell=e^{-m x_0}$, where $x_0$ is the colour-free background rate per SPAD times the dead time. Because $\ell$ multiplies both counts, the full-sun factor becomes $(a\,\ell/(m\,\ell_0))^{1/4}$, with $\ell_0=e^{-x_0}$. With the §C0 model's $x_0=0.122$ (subsection 4.2) and $m=6$, $\ell$ falls from 0.885 to $e^{-0.732}=0.481$, which multiplies the range by a further $(0.481/0.885)^{1/4}=0.86$ [E].

| Layout | $a$ | $m$ | Full sun | Night |
|---|---|---|---|---|
| Separate ranging and colour channels, each with its own filter (Ouster's patent; Hesai's patent) | 1 | 1 | 1.00 | 1.00 |
| An added layer passing 90% at the laser line | 0.9 | 1 | 0.97 | 0.95 |
| Hybrid pixel, a quarter of the ranging area given to colour | 0.75 | 1 | 0.93 | 0.87 |
| Hybrid pixel, half of the ranging area given to colour | 0.5 | 1 | 0.84 | 0.71 |
| One SPAD ranging through a colour filter, mildest case | 1 | 2.5 | 0.80 | 1.00 |
| The same, middle case | 1 | 6.0 | 0.64 | 1.00 |
| The same, grey scene and visible-efficient SPAD | 1 | 11 | 0.55 | 1.00 |
| The middle case with the dead time of the §C0 model | 1 | 6.0 | 0.55 | 1.00 |

*Range relative to the same receiver without colour, from Eq. \eqref{eq:colour-range-factor}* [E]. Worked: $0.75^{1/4}=0.93$ and $0.75^{1/2}=0.87$; $6.0^{-1/4}=0.64$; $0.64\times0.86=0.55$.

![Range of a SPAD ranging channel with colour channels, relative to the same receiver without colour](automotive_perception_report_figures/colour_lidar_range_cost.png)

*Figure C5b.1.* Range relative to the same receiver without colour, for the layouts of the table above, in full sun (background-limited) and at night (signal-limited), from Eq. \eqref{eq:colour-range-factor}. Separate channels cost nothing. Area given to colour costs its fourth root in sun and its square root at night. A colour band in the ranging path costs only in sun, as $m^{-1/4}$, and dead time adds to that cost. The script `build/figures/colour_lidar_range_cost.py` draws the figure and writes the table and its checks to `colour_lidar_range_cost_tables.txt`.

**What the evidence shows.** Ouster's OS1 kept its range across the change. Its Rev7 datasheet (v3.1, p. 1) and its Rev8 datasheet (v4.0, p. 1) give the same 90 m on 10% and 170 m on 80%, at more than 90% detection probability in 100 klx and in the 1,024 × 10 Hz mode. The Rev8's range precision and accuracy are twice as good: 0.25–1.5 cm and ±1.25 cm against 0.5–3 cm and ±2.5 cm (p. 2 of each) [P]. Its vertical field widened from 42.4° ± 1.0° to 44.0° [P], which suggests new optics [E]. Whatever the colour channels cost, the L4 generation absorbed it within the published range [E]. Hesai quotes the same 400 m on 10% for the colour ETX as for the 2025 ETX, whose formal specification table gives 300 m (§C3); neither figure has been tested independently. How much Picasso pays depends on its layout: separate arrays, as in its 2026 patent, would cost almost nothing, while depth pixels ranging through colour filters would lose 20–45% of the sunlit range (table) [E].

**What keeps the cost near zero** [E]:
- *Separate channels with their own filters.* Per-channel filters behind collimating micro-lenses, as in Ouster's patent, let the ranging channel keep a narrow interference filter at near-normal incidence while the colour channels take broad colour filters [P].
- *An infrared cut on the colour channels.* Organic RGB filter materials pass the near infrared, which is why cameras carry an infrared-cut filter. Without one the colour channels would count solar infrared and the sensor's own 865 nm echoes, which at night would tint the colours.
- *Chromatic focus.* The bulk lens must focus 400–700 nm and 865 nm onto the same aperture plane; the patent corrects the colour channels' focus with their own micro-optics [P]. A lens that blurred the 865 nm spot instead would need a ranging aperture $g$ times larger in area, which raises $m$ by $g$ and costs a factor $g^{-1/4}$ in sun.
- *Isolation from the colour SPADs.* In full sun the colour SPADs count fast. Scaling the 3 lux floor to 100 klx gives $10\times10^{5}/3=3.3\times10^{5}$ counts in a 97.7 µs dwell, $3.4\times10^{9}$ s⁻¹ if counted linearly, against the $1.8\times10^{8}$–$3.7\times10^{8}$ s⁻¹ background of the §C0 model's ranging macro-pixel. Their avalanche glow and electrical coupling must be kept away from the ranging SPADs; trench isolation like the L3's serves that purpose.

**The colour channels' own reach.** Passive colour does not fade with distance on a surface that fills a channel's view; it fades on a small object as the object's share of the view shrinks. An object of size $s$ fills a channel of angular size $\theta$ out to $R=s/\theta$: $0.30\ {\rm m}/6.0\ {\rm mrad}=50$ m for a 30 cm object in an OS1 row of $44^\circ/128=0.344^\circ$. Beyond that its colour mixes with the background in proportion to the area it covers, although a bright lamp can still tint a pixel it only partly fills [E]. The colour filters do not shorten this reach; they give each colour channel about a third of the visible photons, which sets the low-light floor above [E].

Sources: https://data.ouster.io/downloads/datasheets/datasheet-rev8-v4p0-os1.pdf (Ouster OS1 Rev8 datasheet v4.0, pp. 1–3) ; https://data.ouster.io/downloads/datasheets/datasheet-rev7-v3p1-os1.pdf (Ouster OS1 Rev7 datasheet v3.1, pp. 1–2) ; https://ouster.com/insights/blog/introducing-rev8-os-family (Ouster, Rev8 launch) ; https://www.businesswire.com/news/home/20260519339385/en/ (Ouster and Fujifilm, 19 May 2026) ; https://www.businesswire.com/news/home/20211028005360/en/Ouster-Doubles-Digital-Lidar-Processing-Power-With-New-L2X-Chip (L2X) ; https://www.businesswire.com/news/home/20220310005630/en (Chronos) ; https://www.sec.gov/Archives/edgar/data/1816581/000162828022004256/oust-20211231.htm (Ouster Form 10-K for 2021) ; https://patents.google.com/patent/US10739189B2/en (US 10,739,189 B2) ; https://image-sensors-world.blogspot.com/2020/08/ouster-releases-details-of-its-spad.html (Ouster's 2018 article, quoted) ; https://www.techinsights.com/blog/stmicroelectronics-ouster-l3-chip-third-generation-direct-time-flight-cmos-image-sensor-device ; https://www.techinsights.com/blog/stmicroelectronics-ouster-os1-lidar-spad-array-sensor-l3-chip-process-flow-analysis (TechInsights on the L3) ; https://lidarmag.com/?p=13260 ; https://powermotiontech.com/sensors-software/article/21252991/advanced-chip-technology-enhances-lidar-sensor-capabilities (the L3 in the trade press) ; https://www.hesaitech.com/hesai-unveils-picasso-6d-full-color-spad-soc-next-gen-etx-and-innovations-in-spatial-intelligence-and-physical-ai/ (Hesai, Picasso and ETX) ; https://autonews.gasgoo.com/articles/ICV/is-the-future-of-lidar-not-price-cutting-but-6d-full-color-2046126963415048193 (Gasgoo on Hesai's open day) ; https://www.robosense.ai/en/rslidar/AC2 ; https://store.robosense.ai/ja/products/ac1 (RoboSense Active Camera) ; https://www.dxomark.com/glossary/color-depth/ (DxOMark on the SMI) ; https://www.strollswithmydog.com/phone-camera-color-accuracy/ (the SMI formula as quoted) ; https://arxiv.org/abs/1902.10190 (Ingle, Velten and Gupta, CVPR 2019) ; https://en.wikipedia.org/wiki/Lux (illuminance table)"""

PAIRS = [
    # scope list
    ("including an in-depth read of Sony's automotive parts (§C5a);",
     "including an in-depth read of Sony's automotive parts (§C5a) and of colour channels on the ranging chip, with "
     "their cost in range (§C5b);"),
    # §C0 relation table
    (r"| Solar background per pixel, Eq. \eqref{eq:solar-background-rate} (4.2) | §C4c, §C6 (Eq. "
     r"\eqref{eq:macro-pixel-background-rate}) |",
     r"| Solar background per pixel, Eq. \eqref{eq:solar-background-rate} (4.2) | §C4c, §C5b (Eq. "
     r"\eqref{eq:colour-background-multiplier}), §C6 (Eq. \eqref{eq:macro-pixel-background-rate}) |"),
    ("| Detection efficiency, dead time, pile-up, afterpulsing and crosstalk (4.1, 4.2) | §C4b, §C5a, §C6 |",
     "| Detection efficiency, dead time, pile-up, afterpulsing and crosstalk (4.1, 4.2) | §C4b, §C5a, §C5b, §C6 |"),
    # §C3 route table
    ("| **Ouster** (US) | OS Rev7/Rev8 | dToF | 865 | VCSEL + CMOS SPAD-SoC | spinning |",
     "| **Ouster** (US) | OS Rev7/Rev8 | dToF | 865 | VCSEL + CMOS SPAD-SoC (the L3 made by ST [I]; colour channels "
     "on the chip from Rev8, §C5b) | spinning |"),
    # §C4b supply-chain row
    ("Adaps, Fortsense, VisionICs; ST (Ouster); SolidVue (Korea) |",
     "Adaps, Fortsense, VisionICs; ST (Ouster's L3 [I], §C5b); SolidVue (Korea) |"),
    # §C4b bullet
    ("  - on-chip RGB-D fusion, i.e. colour and depth from one chip (Picasso, Limera).",
     "  - on-chip RGB-D fusion, i.e. colour and depth from one sensor: from the ranging chip itself in Hesai's "
     "Picasso and Ouster's Rev8 (§C5b), or from a coaxial lidar–camera in Huawei's Limera (§F5)."),
    # §C5 Picasso row
    ("**2,160 lines per chip; the 4,320-line ETX uses two chips** [P/T] |",
     "**2,160 lines per chip; the 4,320-line ETX uses two chips** [P/T]; colour channels and their range cost: "
     "§C5b |"),
    # the new subsection, before §C6
    ("\n\n## C6. How far can SPAD-SoC receivers scale?",
     "\n\n" + C5B + "\n\n## C6. How far can SPAD-SoC receivers scale?"),
    # §C10.6 (d)
    ("Lidar samples matched to camera pixels (Hesai Picasso, Huawei Limera; §F5)",
     "Lidar samples matched to camera pixels (Hesai Picasso, Ouster Rev8, Huawei Limera; §C5b, §F5)"),
    # §E10.4
    ("such as Hesai Picasso and Huawei Limera, §F5)",
     "such as Hesai Picasso, Ouster's Rev8 and Huawei Limera; §C5b, §F5)"),
    # §E11.2
    ("  - **Pixel-aligned RGB-D sensors** (Hesai Picasso, Huawei Limera; §F5)",
     "  - **Pixel-aligned RGB-D sensors** (Hesai Picasso, Ouster Rev8, Huawei Limera; §C5b, §F5)"),
    # §F5
    ("(a colour image plus depth from one sensor; Hesai Picasso; Huawei Limera's coaxial lidar-camera);",
     "(a colour image plus depth from one sensor; Hesai Picasso and Ouster's Rev8, §C5b; Huawei Limera's coaxial "
     "lidar-camera);"),
    # Appendix 1
    ("The PDE wavelength, pixel pitch and process node are unknown; they decide how its SPAD-SoC compares with Sony's "
     "parts (§C5).",
     "The PDE wavelength, pixel pitch and process node are unknown; they decide how its SPAD-SoC compares with Sony's "
     "parts (§C5). Its colour performance (SNR, dynamic range, colour accuracy) is not published either, nor is "
     "whether its depth pixels range through colour filters, which would cost range in sunlight (§C5b).\n"
     "- **Ouster L4 and L4 Max:** the foundry, process node, SPAD pitch, PDE and dead time are not published "
     "(TechInsights found the L3 made by STMicroelectronics), nor is the colour layout of Rev8: a row of separate "
     "channels or a hybrid pixel. The layout decides what the colour channels cost in range (§C5b)."),
]

new = text
for old, rep in PAIRS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:80]!r}"
    new = new.replace(old, normalise(rep), 1)
assert "\r" not in new

# build/README.md: the new figure script
_, readme_text = load(readme)
row_old = "| `mechanical_scanning_limits.py` | `mechanical_scanning_limits.png` | Figure C4d, §C4d subsection 5 |"
row_new = row_old + "\n| `colour_lidar_range_cost.py` | `colour_lidar_range_cost.png` | Figure C5b.1, §C5b |"
assert readme_text.count(row_old) == 1 and "colour_lidar_range_cost.py" not in readme_text
readme_new = readme_text.replace(row_old, row_new, 1)

# build/figures/fmcw_tof_system_budget.py: the quoted number of eq:fmcw-dwell
_, fmcw_text = load(fmcw)
assert fmcw_text.count("Eq. (122)") == 2 and "Eq. (124)" not in fmcw_text
fmcw_new = fmcw_text.replace("Eq. (122)", "Eq. (124)")

print(f"report: {len(PAIRS)} replacements, {len(text):,} -> {len(new):,} characters")
print(f"report sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if write:
    report.write_bytes(new.encode("utf-8"))
    readme.write_bytes(readme_new.encode("utf-8"))
    fmcw.write_bytes(fmcw_new.encode("utf-8"))
    print("written: report, build/README.md, build/figures/fmcw_tof_system_budget.py")
else:
    print("check only (add --write to apply)")
