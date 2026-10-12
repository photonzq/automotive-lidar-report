## A7. "Starlight" cameras: low-light CMOS, active near-infrared and photon counting

This section asks whether a camera that images reflected light could do thermal's job at night. The candidates are a low-light ("starlight") CMOS camera; a near-infrared (NIR) camera with its own invisible lamps; a gated camera, which records only the light of its own laser pulses that returns from a chosen range; a short-wave infrared (SWIR) camera; an image intensifier; and the photon-counting sensors now aimed at cars, SPAD (single-photon avalanche diode) arrays and quanta image sensors (QIS). Unlike a thermal camera (§A3, item 1), all of them can sit behind the windshield. All but the active ones depend on the light already in the scene. The section counts that light pixel by pixel (§A7.1), asks what each kind of noise costs (§A7.2), turns the result into detection ranges for a dark-clothed pedestrian (§A7.3), reviews the low-light (§A7.4), active (§A7.5) and photon-counting (§A7.6) products, and compares them with thermal (§A7.7).

**Short answer.**
- **Passive cameras are limited by photons, not by sensor technology.** Beyond the low beam's cutoff a dark-clothed pedestrian is lit only by the glare-limited part of the beam (350 cd, §A6.1) and by the night sky. A 3 µm automotive CMOS pixel then collects about 0.1–1 photoelectron per 30 ms frame from that pedestrian at 50–150 m, and below 0.01 on a moonless night without headlights. Below about 0.05 lux on a dark target, i.e. beyond about 85 m in the glare-limited zone, even the best automotive CMOS pixel is limited by its own read noise.
- **Photon counting removes read noise but adds no photons.** At equal pixel area and sensitivity, a single frame of a photon-counting pixel reaches an SNR of 1 at 1.00 detected photon, against 1.28 photoelectrons for a CMOS pixel with 0.6 electrons of read noise. The advantage grows only when an image is built from many readouts that each carry well under one photoelectron, as in short-exposure bursts (3–10× in SNR). Dark counts cap it as the chip warms: at 60 °C the cap is about 1.8×. For the pedestrian, photon counting stretches an ideal detector's range by about 20–35% and a pixel-level image's by about 12–14% [E].
- **Thermal works in another regime.** A thermal pixel sees the same pedestrian with an SNR of $\Delta T/{\rm NETD}\approx20$–100 in any light, one to two orders of magnitude above the best reflected-light camera beyond the low beam. Its limits are resolution, contrast (clothing, hot nights) and its exposed window (§A3), not photons.
- **Active near-infrared adds photons, and it was sold.** Toyota (2002) and Mercedes (2005) lit the road with invisible NIR lamps. In Mercedes's tests drivers recognized dark-clothed dummies at 160 m instead of 70 m with bi-xenon low beams, and in 2010 more than half of S-Class buyers ordered the option [P]. Mercedes nevertheless added a thermal camera in 2013 and has not offered night vision since the 2021 S-Class, and Lexus dropped the feature after the 2013 GS for lack of buyers [T]. Gated imaging (BrightWay) adds rejection of fog backscatter but has no named car programme.
- **Automotive SPAD cameras are announced, not shipping.** Canon's 2.1-megapixel automotive SPAD sensor (VLSI 2025) targets mass production in 2031 [T]. AUMOVIO presented SPAD imaging at AutoSens Europe 2026, but the only source for an AUMOVIO SPAD camera at A-sample stage is a social-media post by the chief executive of its software partner, Ubicept [U]. These sensors' near-term selling points in cars are dynamic range (156 dB in one shot) and immunity to flickering LED lights as much as low light.

### A7.1 The night photon budget

This subsection counts the photoelectrons that a camera pixel collects from a pedestrian at night, using two equations and two checks against measured sensors. The light that reaches the sensor depends on the target's luminance. For a Lambertian (perfectly diffuse) target, the illuminance of its image on the sensor is

$$E_{\rm img}=\frac{\tau_o\,\rho\,E_s}{4F_\#^2} \tag{9013}$$

where $E_{\rm img}$ is the illuminance on the sensor in lux, $E_s$ the scene illuminance falling on the target in lux, $\rho$ the target's diffuse reflectance (0 to 1), $F_\#$ the lens's f-number (focal length divided by aperture diameter) and $\tau_o$ the transmission of the lens and windshield together. Eq. (9013) combines the target's luminance, $L=\rho E_s/\pi$ (Eq. (9)), with the standard camera relation $E_{\rm img}=\pi\tau_oL/(4F_\#^2)$ for a distant object near the lens axis; the fall-off of illuminance toward the edge of the field is neglected. One pixel then collects

$$\bar n=S_v\,E_{\rm img}\,A_{\rm pix}\,t_{\rm exp},\qquad S_v=\bar\eta\,\Phi_{\rm lx} \tag{9014}$$

photoelectrons per readout, where $A_{\rm pix}$ is the pixel's area in µm², $t_{\rm exp}$ the exposure time in seconds and $S_v$ the pixel's luminous sensitivity, in photoelectrons per lux-second per µm² of pixel.
- $S_v$ is the product of two factors. $\Phi_{\rm lx}$ is the number of photons per second that fall on 1 µm² at an illuminance of 1 lux. It depends on the light's spectrum: $4.10\times10^{3}$ for green light at 555 nm, the eye's peak, and $1.09\times10^{4}$ for a 5,500 K white source counted from 400 to 700 nm, because broadband light carries more photons per lux than light at the peak of the eye's sensitivity [E]. $\bar\eta$ is the pixel's quantum efficiency (the share of incident photons that become photoelectrons) averaged over that spectrum.
- **Sensitivities used** [I]. OmniVision computed $S_v$ from measured quantum efficiency for its 2.1 µm automotive pixel, under D65 daylight with an infrared-cut filter at 650 nm: $16.4\times10^{3}$ photoelectrons per lux-second for the green pixel of an RGGB array and $30.3\times10^{3}$ for the clear pixel of an RCCB array (Funatsu et al., IS&T Electronic Imaging 2022). RGGB is the common red–green–green–blue colour-filter pattern; RCCB replaces the two green filters with clear (unfiltered) pixels. Per µm² these are $S_v=3{,}720$ (green) and $6{,}870$ (clear), which imply average quantum efficiencies over 400–650 nm of 0.40 and 0.74 [E]. The clear pixel collects 1.85 times the green pixel's light.
- **First check** [E]. OmniVision's 2.8 µm pixel of 2019 measured 24,600 photoelectrons per lux-second at 530 nm [I]. One lux at 530 nm delivers $4.50\times10^{3}$ photons per µm² per second, i.e. $3.53\times10^{4}$ on the pixel's 7.84 µm². The measurement therefore implies a quantum efficiency of $24{,}600/35{,}300=0.70$ at the green peak, as expected for a modern pixel.
- **Second check** [E]. Sony defines its low-light index SNR1s as the scene illuminance at which the green pixel's signal equals its noise, for an 18% grey chart lit by a 3,200 K lamp, an f/1.4 lens and a 1/60 s exposure, and gives 0.17 lux for its 2.9 µm IMX585 [P]. Eq. (9013) gives $E_{\rm img}=0.18\times0.17/(4\times1.4^2)=3.9\times10^{-3}$ lux. With the green sensitivity scaled by 0.85 for the redder lamp, Eq. (9014) gives $\bar n=3{,}160\times3.9\times10^{-3}\times8.41\times(1/60)\approx1.7$ photoelectrons, an SNR of 1.2 with 0.6 electrons of read noise (Eq. (9015) below). The model reproduces Sony's index to within about 20%.

The reference camera has $\tau_o=0.8$ (0.9 for the lens and 0.9 for the windshield [E]), $F_\#=1.6$ and $t_{\rm exp}=30$ ms, the longest exposure a 30 frames-per-second camera allows. The pedestrian wears dark ($\rho=0.05$) or light ($\rho=0.5$) clothing, as in §A6.1. The table gives the photoelectrons collected per pixel per frame from dark clothing; light clothing gives ten times more.

| Scene illuminance on the pedestrian | $E_s$ (lux) | 3 µm green pixel | 3 µm clear pixel | 2.1 µm clear pixel | 6.39 µm SPAD pixel |
|---|---|---|---|---|---|
| Low-beam hotspot (the IIHS 5 lux criterion, §A6.1) | 5 | 19.6 | 36.2 | 17.8 | 164 |
| Glare-limited zone of the low beam (350 cd) at 50 m | 0.14 | 0.55 | 1.02 | 0.50 | 4.6 |
| Full moon, upper end of typical summer values | 0.1 | 0.39 | 0.72 | 0.36 | 3.3 |
| Glare-limited zone at 100 m | 0.035 | 0.14 | 0.25 | 0.12 | 1.15 |
| Half moon at the zenith (maximum) | 0.025 | 0.10 | 0.18 | 0.09 | 0.82 |
| Glare-limited zone at 150 m | 0.016 | 0.06 | 0.11 | 0.06 | 0.51 |
| Moonless rural night, clear sky | 0.001 | 0.004 | 0.007 | 0.004 | 0.033 |

*How the numbers are derived* [E]:
- Each entry is Eq. (9014) with Eq. (9013). For the 3 µm clear pixel in the glare-limited zone at 100 m: $E_s=350/100^2=0.035$ lux (Eq. (8)); $E_{\rm img}=0.8\times0.05\times0.035/(4\times1.6^2)=1.37\times10^{-4}$ lux; and $\bar n=6{,}870\times1.37\times10^{-4}\times9\times0.030\approx0.25$.
- The SPAD column is the 6.39 µm pixel of Canon's 3.2-megapixel sensor (§A7.6), given the clear pixel's sensitivity, so that it differs from the CMOS pixel only in area, $(6.39/3)^2=4.5$ times larger, and in noise (§A7.2). The 2.1 µm column is the pixel of today's 8-megapixel front cameras.
- The night illuminances come from a review of measurements (Hänel et al. 2018) [I]: a natural starlit sky gives 0.6–0.9 mlux, a clear rural sky without moon 0.7–3 mlux, a half moon at most 25 mlux, a typical summer full moon 50–100 mlux, and a full moon at the zenith at most 320 mlux. Skyglow from artificial light raises clear suburban skies to 2–45 mlux and clear urban skies to 7–65 mlux, and overcast urban skies to 30–550 mlux; street lighting gives 2–30 lux [I].
- Euro NCAP's illustrative scale for its low-light tests (moonless night 0.002 lux, starry sky 0.03 lux, full moon 0.25–1 lux) sits several times above these measurements [P]. FMVSS 127's dark tests allow at most 0.2 lux of ambient light (§A4).

**Where read noise starts to bind.** The read noise $\sigma_r$ of a CMOS pixel, in electrons rms, adds a variance $\sigma_r^2$ to every readout, and below a signal of $\bar n=\sigma_r^2$ that variance exceeds the signal's own shot noise. For $\sigma_r=0.6$ electrons (§A7.2), $\sigma_r^2=0.36$.
- The 3 µm clear pixel collects $0.25/0.035=7.25$ photoelectrons per lux of scene illuminance on dark clothing. It reaches 0.36 at $E_s=0.36/7.25\approx0.050$ lux on dark clothing and at 0.005 lux on light clothing [E].
- In the glare-limited zone, 0.050 lux is reached at $R=\sqrt{350/0.050}\approx84$ m (Eq. (8)). Beyond about 85 m, therefore, a dark-clothed pedestrian lit only by the low beam sits in the read-noise-limited regime even of a 3 µm pixel. A 2.1 µm pixel collects half as much light and reaches the boundary at 0.10 lux, i.e. at 59 m.
- This is the regime in which photon counting can help (§A7.2).

**Canon's 0.002 lux in photons.** Canon's 3.2-megapixel SPAD sensor produced monochrome video at 0.002 lux with an f/1.2 lens and a 1/30 s exposure, and Canon describes subjects as identifiable at 0.0003 lux [P]. By Eqs. (9013)–(9014), with $\tau_o=0.9$, 0.002 lux on a scene of 20–50% reflectance gives 0.6–1.5 detected photons per pixel per frame, and 0.0003 lux gives 0.09–0.22 [E]. The image is usable at well under one photon per pixel because the sensor adds no read noise and a viewer averages over many pixels. The photons themselves come from the large pixel and the fast lens.

![Photoelectrons per pixel per frame versus scene illuminance for a CMOS and a SPAD pixel, with noise floors and night illuminance levels](automotive_perception_report_figures/night_photon_budget.png)

*Figure A7.1.* Photoelectrons per pixel per 30 ms frame (Eq. (9014)) versus the scene illuminance on the target. The data curves are a 3 µm clear CMOS pixel on dark ($\rho=0.05$, solid blue) and light ($\rho=0.5$, dashed blue) clothing, and a 6.39 µm SPAD pixel of the same sensitivity on dark clothing (solid red), with $F_\#=1.6$ and $\tau_o=0.8$.
- *Shaded bands:* a moonless rural sky (0.6–3 mlux) and a full moon (50–320 mlux) (Hänel et al. 2018). *Vertical dashed lines:* the low beam's glare-limited zone (350 cd) at 150 m and 50 m, and the 5 lux hotspot criterion (§A6.1).
- *Horizontal lines:* the CMOS pixel's noise floor per readout at 60 °C, read-noise variance plus dark electrons (grey, dashed), and the SPAD pixel's dark counts per frame at 60 °C (red, dashed) and 25 °C (red, dash-dotted) (§A7.2).
- Where a data curve lies below its sensor's noise floor, one frame of one pixel cannot show the target; a detector must then add up many pixels or frames (Eq. (9016)).

### A7.2 Noise: what photon counting removes and what it does not

This subsection compares the noise of an integrating CMOS pixel with that of a photon-counting pixel, and finds that photon counting gains most where each readout carries much less than one photoelectron and least at high chip temperature. An integrating pixel accumulates photoelectrons during the exposure and reads them out once through an amplifier, which adds read noise. A photon-counting pixel registers each detected photon as a digital event, so its readout adds no noise. A SPAD does this with an avalanche; a QIS does it with an amplifier quiet enough to resolve single electrons (§A7.6). The signal-to-noise ratio (SNR) of one readout is

$$\text{SNR}_1=\begin{cases}\dfrac{\bar n}{\sqrt{\bar n+\bar n_d+\sigma_r^2}} & \text{integrating pixel,}\\[8pt] \dfrac{\bar n}{\sqrt{\bar n+\bar n_{dc}}} & \text{photon-counting pixel,}\end{cases} \tag{9015}$$

where $\bar n$ is the mean signal in photoelectrons (or detected photons), $\bar n_d$ the mean number of dark electrons of the integrating pixel (charge generated thermally, whose shot noise has variance $\bar n_d$), $\bar n_{dc}$ the mean number of dark counts of the counting pixel (avalanches that fire without a photon), and $\sigma_r$ the read noise in electrons rms. Fixed-pattern noise and afterpulsing (spurious avalanches that follow a real one) are left out.
- **Single-frame threshold.** For SNR = 1, the integrating pixel needs $\bar n=\tfrac12\big(1+\sqrt{1+4(\sigma_r^2+\bar n_d)}\big)$. For $\sigma_r=0.6$ electrons and no dark charge that is 1.28 photoelectrons, while the photon-counting pixel without dark counts needs 1.00.
- **The read noise used.** Three measurements support $\sigma_r=0.6$ electrons: Sony's automotive IMX490, 0.54 electrons rms in an EMVA 1288 test of a LUCID camera [P]; OmniVision's 2.8 µm split pixel, 0.83 electrons (IISW 2019) [I]; and onsemi's 2.1 µm, 8.3-megapixel automotive sensor (IISW 2023), which reaches SNR = 1 at about 1.3 photoelectrons from 60 to 80 °C, i.e. a noise floor of about 0.6 electrons [I; E, read from the paper's Figure 3]. EMVA 1288 is the machine-vision industry's standard for measuring camera noise and sensitivity.

**Adding up readouts.** A pedestrian covers many pixels, and a detector can add them up. For a uniform target on a black background, the sum of $M$ independent readouts of equal mean signal has

$$\text{SNR}_M=\sqrt{M}\;\text{SNR}_1 \tag{9016}$$

because the signal grows as $M$ and the noise as $\sqrt{M}$. The same holds for $M$ frames of one pixel if the target does not move. The Rose criterion of visual detection asks for an SNR of about 5 over the target's area; it is applied to $\text{SNR}_M$ in §A7.3.

**The photon-counting gain.** At equal pixel area and sensitivity, the ratio of the two SNRs of Eq. (9015) is

$$G=\frac{\text{SNR}_1^{\rm count}}{\text{SNR}_1^{\rm int}}=\sqrt{\frac{\bar n+\bar n_d+\sigma_r^2}{\bar n+\bar n_{dc}}} \tag{9017}$$

and by Eq. (9016) the ratio is the same for any number of readouts added up. Two limits follow.
- **Large signals** ($\bar n\gg\sigma_r^2$): $G\to1$. Photon counting brings nothing in daylight or in the low-beam hotspot.
- **Small signals** ($\bar n\to0$): $G\to\sqrt{(\sigma_r^2+\bar n_d)/\bar n_{dc}}$. The gain is capped by the counting pixel's own dark counts.

The table gives $G$ for two pixels of the same 3 µm size and sensitivity, with $\sigma_r=0.6$ electrons and 30 ms readouts.

| Signal per readout $\bar n$ | No dark signal | Chip at 25 °C | Chip at 60 °C | Chip at 85 °C |
|---|---|---|---|---|
| 1 | 1.17 | 1.16 | 1.17 | 1.64 |
| 0.36 ($=\sigma_r^2$) | 1.41 | 1.40 | 1.35 | 1.82 |
| 0.1 | 2.14 | 2.04 | 1.60 | 1.94 |
| 0.03 | 3.61 | 3.07 | 1.75 | 1.97 |
| 0.01 | 6.08 | 4.14 | 1.81 | 1.99 |
| Small-signal cap | — | 5.5 | 1.85 | 1.99 |

*How the numbers are derived* [E]: each entry is Eq. (9017) with the dark signals per 30 ms readout from the dark-signal table below: $\bar n_d=0.005$ and $\bar n_{dc}=0.012$ at 25 °C, 0.27 and 0.19 at 60 °C, and 4.8 and 1.3 at 85 °C. For $\bar n=0.1$ at 60 °C, $G=\sqrt{(0.1+0.27+0.36)/(0.1+0.19)}=\sqrt{0.73/0.29}\approx1.6$. The 85 °C column is the least certain, because it extrapolates the two doubling temperatures of Eq. (9019) furthest; it rises above the 60 °C column only because the CMOS dark current is taken to double faster (every 6 °C) than the SPAD's dark counts (every 7–12 °C).

**Bursts of short frames.** The case for photon counting is strongest when one exposure is split into many short ones. Splitting an exposure that collects $N$ photoelectrons into $K$ readouts leaves the signal unchanged but adds $K$ read noises. Without dark signal, Eq. (9017) becomes

$$G_K=\sqrt{\frac{N+K\sigma_r^2}{N}}=\sqrt{1+\frac{K\sigma_r^2}{N}} \tag{9018}$$

where $N$ is the total signal per pixel and $K$ the number of readouts.
- For $N=1$ photoelectron per pixel over 30 ms, splitting into $K=30$ frames of 1 ms gives $G_{30}=\sqrt{1+30\times0.36/1}\approx3.4$; for $N=0.1$ it gives 10.4 [E].
- Short frames freeze motion, and a photon-counting camera can decide after capture how to combine them, for example by shifting each frame to follow a moving object before adding it. This is the basis of Ubicept's processing (§A7.6) and helps Canon's sensor handle very high dynamic range.
- The long-range night problem does not need bursts. A pedestrian 3 m to the side of the path, 100 m ahead of a car at 100 km/h, moves across the image at $3\times27.8/100^2\approx8.3$ mrad/s, i.e. 0.25 mrad in 30 ms, about one pixel of the reference camera of §A7.3 (0.27 mrad) [E].

**Temperature.** Both kinds of dark signal grow roughly exponentially with chip temperature:

$$D(T)=D(T_0)\,2^{(T-T_0)/T_2} \tag{9019}$$

where $D$ is the dark rate (electrons or counts per second), $T$ the chip temperature, $T_0$ a reference temperature and $T_2$ the temperature rise that doubles the rate.
- **CMOS.** McGrath et al. (IISW 2017) report that the dark current of modern pixels at 60 °C doubles about every 6 °C, against 11 °C historically [I].
- **SPADs.** ST measured 8.6, 810 and 6,923 dark counts per second at −20, 60 and 80 °C in a 10.17 µm pixel at 2.5 V excess bias, a doubling every 7 °C at high temperature [I]. Panasonic's 6 µm avalanche pixel rose from 21 counts per second at room temperature to 10,000 at a chip temperature of 105 °C, a doubling about every 9 °C [I].

The table gives the resulting dark signal per 30 ms readout.

| Chip temperature | CMOS, 3 µm (electrons) | SPAD, 6.39 µm, Canon-class (counts) | SPAD scaled to 3 µm (counts) |
|---|---|---|---|
| 25 °C | 0.001–0.02 | 0.05 | 0.01 |
| 60 °C | 0.05–0.9 | 0.4–1.7 | 0.09–0.38 |
| 85 °C | 1–16 | 1.7–21 | 0.4–4.5 |
| 105 °C | 10–160 | 5–150 (Panasonic's 6 µm pixel, measured: 300) | 1.2–33 |

*How the numbers are derived* [E]:
- **CMOS:** dark-current densities at 60 °C of 0.2, 1.0 and 3.3 electrons per second per µm², times 9 µm² and 0.030 s, scaled with $T_2=6$ °C. The 3.3 is OmniVision's 2.8 µm photodiode, 25.6 electrons per second at 60 °C (IISW 2019) [I], and Gigajot's quanta image sensor measured 1.35 at 60 °C (Scientific Reports 2022) [I]. The 0.2 is inferred from onsemi's SNR = 1 points, which barely move between 60 and 100 °C (IISW 2023) [E]. The middle value, 1.0, is used in the gain table above and in §A7.3.
- **SPAD:** Canon's 1.8 counts per second at 25 °C for its 6.39 µm pixel (IEDM 2021, as tabulated by Sony at the 2024 International SPAD Sensor Workshop) [I], scaled with $T_2=12$ °C (a slow case) and 7 °C (ST's measured value). The gain table and §A7.3 use the geometric mean of the two.
- **Per unit area** at 60 °C, measured SPAD dark rates (ST 7.8, Sony's 6 µm pixel 8.3 and 10 µm pixel 2.2 counts per second per µm²) [I] span the same range as CMOS dark current (0.2–3.3 electrons per second per µm²), with Canon's pixel at the low end (0.3–1.4, extrapolated).

At 25 °C the photon-counting pixel's dark counts are negligible, and its gain on the weakest signals reaches 4–6. At 60 °C, a common specification temperature for automotive image sensors, the dark signals of both pixels are comparable to the CMOS read-noise variance, and the gain is capped near 1.8. AEC-Q100 Grade 2 image sensors such as the IMX490 are rated to 105 °C ambient [P]; how warm a windshield camera's chip runs at night, without the sun's load, has not been published (Appendix 1).

### A7.3 What a low-light camera sees of a pedestrian

This subsection turns Eqs. (9013)–(9017) into detection ranges for the case that matters for automatic emergency braking (AEB) at night: a dark-clothed pedestrian on an unlit road, lit only by the glare-limited part of the low beam. It uses two bounds. The *ideal bound* adds up all of the pedestrian's pixels and asks for the Rose criterion, $\text{SNR}_M\ge5$ (Eq. (9016)). Real detectors, which need shape and texture, require more. The *pixel-level bound* asks every pixel for $\text{SNR}_1\ge1$, a frame in which the pedestrian can be seen pixel by pixel.
- **Visible camera:** 3 µm clear pixels, 1,920 columns over a 30° horizontal field. Its instantaneous field of view (IFOV, the angle seen by one pixel) is $\pi/6/1{,}920=0.273$ mrad, which takes an 11 mm focal length and, at f/1.6, a 6.9 mm aperture. The exposure is 30 ms and the chip is at 60 °C (dark signals from the table in §A7.2). The photon-counting pixel has the same area and sensitivity.
- **Scene:** the pedestrian of §A3 and §A5 (1.7 × 0.5 m, 0.85 m²) in dark clothing ($\rho=0.05$), on a black background, lit by 350 cd from the glare-limited zone (Eq. (8)) plus 1 mlux of moonless sky.
- **Thermal camera, for comparison:** 640 × 512 pixels over 24° (IFOV 0.654 mrad), with a noise-equivalent temperature difference (NETD, the temperature difference that gives an SNR of 1 in one pixel and frame) below 50 mK, as specified for Teledyne FLIR's automotive development kit [P]. Per pixel its SNR is

$$\text{SNR}_{\rm th}=\frac{\Delta T}{\rm NETD} \tag{9020}$$

  where $\Delta T$ is the difference in apparent temperature between the pedestrian and the background. Clothing shields body heat, so for a clothed pedestrian $\Delta T$ is a few kelvin: in cold weather clothing can hide all but the head and hands (Bertozzi et al., IEEE IV 2003) [I], and on hot nights the difference can vanish (§A3, item 5). $\Delta T=1$–5 K is assumed here [E].

The table gives the SNR of each camera on this pedestrian, moonless sky, chip at 60 °C.

| Range | $E_s$ (lux) | Visible pixels on the pedestrian | $\bar n$ per clear pixel | $\text{SNR}_1$, CMOS / counting | $\text{SNR}_M$, CMOS / counting | Thermal pixels on the pedestrian | $\text{SNR}_M$, thermal, $\Delta T=1$–5 K |
|---|---|---|---|---|---|---|---|
| 50 m | 0.141 | 4,572 | 1.02 | 0.80 / 0.93 | 54 / 63 | 794 | 560–2,800 |
| 75 m | 0.063 | 2,032 | 0.46 | 0.44 / 0.57 | 20 / 26 | 353 | 380–1,900 |
| 100 m | 0.036 | 1,143 | 0.26 | 0.28 / 0.39 | 9.3 / 13 | 198 | 280–1,400 |
| 150 m | 0.017 | 508 | 0.12 | 0.14 / 0.22 | 3.1 / 4.9 | 88 | 190–940 |
| 200 m | 0.010 | 286 | 0.07 | 0.08 / 0.14 | 1.4 / 2.4 | 50 | 140–700 |

*How the numbers are derived* [E]:
- Pixels on the pedestrian: $M=0.85/(R\cdot\text{IFOV})^2$, e.g. $0.85/(100\times2.73\times10^{-4})^2\approx1{,}143$ at 100 m.
- $\bar n$ from Eq. (9014) as in the photon table of §A7.1, with the 1 mlux of sky light added to $E_s$; $\text{SNR}_1$ from Eq. (9015) with $\bar n_d=0.27$ and $\bar n_{dc}=0.19$; $\text{SNR}_M$ from Eq. (9016). At 100 m, $\text{SNR}_1=0.26/\sqrt{0.26+0.27+0.36}\approx0.28$ and $\text{SNR}_M=\sqrt{1{,}143}\times0.28\approx9.3$.
- Thermal: $M=0.85/(100\times6.54\times10^{-4})^2\approx198$ at 100 m, and $\text{SNR}_M=\sqrt{198}\times(1\ {\rm K}/0.05\ {\rm K})\approx280$.
- The ranges at which the bounds are just met follow from the same equations on a 0.1 m grid of ranges. Ideal bound ($\text{SNR}_M=5$): CMOS 126 m and photon counting 149 m at 60 °C; 136 m and 182 m at 25 °C. Pixel-level bound ($\text{SNR}_1=1$): CMOS 42 m and photon counting 47 m at 60 °C; 44 m and 50 m at 25 °C.

**What the table shows** [E]:
- **An ideal detector loses the pedestrian at 125–180 m.** Even adding up all of a dark-clothed pedestrian's pixels against a black background, it loses the pedestrian beyond about 126 m with CMOS and 149 m with photon counting at 60 °C (136 m and 182 m at 25 °C).
- **Real classifiers work nearer the pixel-level bound.** A classifier needs the pedestrian's shape and texture, which puts it nearer the pixel-level bound of 42–50 m. That is inside the stopping distance at 80–100 km/h (69–98 m, Eq. (11)), and it matches the measured weakness of camera AEB on unlit roads (§A4, IIHS 2022; §A6.5).
- **Photon counting stretches both bounds only modestly.** It extends the ideal bound by 18–34% and the pixel-level bound by 12–14%; neither reaches past the stopping distance at the pixel level.
- **Moonlight helps less than it seems.** It raises the signal per pixel (0.72 photoelectrons at 0.1 lux, §A7.1) but lights the background as well, so the contrast of dark clothing against grass or asphalt falls, and the black-background bound no longer applies.
- **Thermal's SNR is far higher.** On the same pedestrian at 100 m, the thermal camera's SNR (280–1,400) is 20–150 times the visible camera's ideal-bound SNR (9–13). Thermal's range is set by resolution, its 1.5-pixel detection ceiling being 940 m for this camera (Eq. (2)), and by contrast and weather, not by photons.

### A7.4 Passive low-light CMOS today

This subsection describes what is sold as a low-light ("starlight") CMOS camera, in security and in cars. These sensors already have sub-electron read noise, clear or near-infrared-enhanced pixels and high dynamic range. The photon table of §A7.1 therefore describes them already.
- **"Starlight" comes from security cameras.** Sony's STARVIS family (STARVIS, STARVIS 2, STARVIS 3) is defined by a sensitivity of at least 2,000 mV per µm² (colour, 706 cd/m² light source, f/5.6, 1 s accumulation equivalent) [P].
  - Its SNR1s index (§A7.1) is 0.17 lux for the 2.9 µm IMX585 and IMX664 colour sensors and 0.10–0.11 lux for their monochrome versions. It is 0.29–0.31 lux for the 2.0 µm IMX678 and 0.53–0.79 lux for 1.45 µm sensors [P].
  - Security-camera makers quote "minimum illumination" far lower, for example 0.0003 lux in colour at f/1.0 for Hikvision's DarkFighterS [P]. As Axis points out, no standard defines how such minimum-illumination figures are measured [P], so they cannot be compared with each other or with SNR1s.
- **Automotive sensors.**
  - Sony's IMX490 (5.4 megapixels, 3.0 µm) delivers 120 dB of dynamic range together with LED-flicker mitigation (a long-exposure readout that never misses the on-phase of pulsed LED lights) and is qualified to AEC-Q100 Grade 2 [P]. LUCID's EMVA 1288 test gives it 0.54 electrons of dark noise [P].
  - onsemi's 8.3-megapixel, 2.1 µm family (IISW 2023) offers 110 dB in a single exposure and 150 dB with two [I]. It reaches SNR = 1 at about 1.3 photoelectrons from 60 to 80 °C, about 1.7 at 100 °C and about 6 at 125 °C, where dark-signal non-uniformity at the floating diffusion (the pixel's charge-to-voltage node) takes over from read noise [I; E, read from the graph].
  - OmniVision's OX08B40 (8.3 megapixels, 2.1 µm) claims 140 dB with flicker mitigation [P].
  - The 8-megapixel front cameras now standard in ADAS use 2.1 µm pixels, half the area of a 3 µm pixel (the 2.1 µm column of the photon table).
- **Clear-pixel colour filters.** Replacing the green filters with clear ones raises the light collected by 1.85 times. In OmniVision's analysis it lowers the illuminance at which the luminance SNR reaches 10, under its test conditions, from 48 lux (RGGB) to 19 lux (RCCB) [I]. The cost is colour: the hue angle separating a yellow from a red traffic light collapses from 29° with RGGB to 1.8° with RCCB. RYYCy, with yellow instead of green filters, collects 1.31 times the green pixel's light and keeps 3.6° [I]. OmniVision proposes shifting the red filter's edge to restore the separation [I].
- **Near-infrared-enhanced pixels.** OmniVision's Nyxel pixels use thicker silicon, a scattering layer that lengthens the photons' path, and deep-trench isolation between pixels. For Nyxel 2 OmniVision claims a quantum efficiency of 70% at 850 nm and 50% at 940 nm on a 2.9 µm pixel (2020) [P]. These gains matter only with NIR illumination or without an infrared-cut filter. White-LED headlamps emit almost no light beyond 750 nm [E].

### A7.5 Active illumination: near-infrared lamps, gated imaging, SWIR and image intensifiers

This subsection covers the cameras that bring their own light, or amplify the scene's light before it is detected. Active systems escape the photon table of §A7.1 because their lamps are invisible, so the glare cap of §A6.1 does not limit them; eye safety and lamp power do.

**Near-infrared lamps with a silicon camera: shipped and dropped.**
- **Toyota.** Toyota fitted the first system in 2002 (Land Cruiser Cygnus; Lexus LX470) and added pedestrian detection on the Crown Hybrid in Feb 2008 [P].
- **Mercedes.** Night View Assist (S-Class W221, 2005) used two infrared high-beam lamps and an NIR camera behind the windshield [P].
  - In the developers' tests, drivers recognized dummies in light clothing beyond 200 m, about 40 m earlier than with bi-xenon low beams, and dummies in dark clothing at 160 m against 70 m [P, Deutscher Zukunftspreis 2006].
  - Pedestrian detection followed in 2009 and a spotlight function, which flashes the headlights at a detected pedestrian, in Dec 2010. Daimler then said that more than half of S-Class buyers worldwide ordered the system [P].
  - For the 2013 S-Class (W222), Night View Assist Plus was supplemented by a thermal camera, which also detects animals [P]. The 2021 S-Class (W223) does not offer night vision (§A1).
- **Lexus.** Lexus dropped Night View after the 2013 GS because few buyers chose it [T, AutoGuide, Sep 2013].
- **Cost and range.** In 2006 an NIR system cost carmakers about \$300 against more than \$1,200 for a thermal one, and the NIR systems of the S-Class and LX470 offered 150–200 m of viewing distance [T, IEEE Spectrum, Mar 2006, quoting Siemens VDO].
- **Why it works.** An NIR high beam puts high-beam-like illuminance on the pedestrian without dazzling anyone, so the camera works with the photon budget of the hotspot rather than of the glare-limited zone (§A7.1) [E].

**Gated imaging.**
- **The system.** BrightWay Vision's system (Grauer 2014) uses a gated CMOS sensor of 1,280 × 960 pixels whose exposure gates (0.5–2 µs) are synchronized to laser pulses at 800–860 nm. The average optical power is below 5 W, and the sensor's NIR quantum efficiency is above 50% [I].
- **Why gating helps in fog.** The camera records only light that returns within a chosen time window, i.e. from a chosen slice of range, so backscatter from fog, rain or snow nearer than that slice is rejected. Grauer computes 10–1,000 times less backscatter than with continuous illumination from haze to light fog, and shows a pedestrian at 50–120 m in falling snow at night [I].
- **Independent test.** In Daimler's fog-chamber benchmark the BrightWay camera outperformed a standard passive CMOS camera in fog (Bijelic, Gruber and Ritter, arXiv:1912.03238) [I].
- **Status.** BrightWay says its system is in serial production without naming a carmaker [P]. No car programme is public (Appendix 1).

**Short-wave infrared.**
- **TriEye's sensor.** TriEye's TES200 ("Raven") has 1,236 × 960 global-shutter pixels at 7 µm, sensitive from 700 to 1,650 nm, with a quantum efficiency of 60% at 1,245 nm and above 50% from 850 to 1,450 nm, at 500 mW [P].
- **Its dark current rules out passive night imaging.** The dark current is 100 pA per pixel at 25 °C [P], i.e. $10^{-10}/1.6\times10^{-19}=6.2\times10^{8}$ electrons per second, which fills the 440,000-electron full well in about 0.7 ms [E]. The sensor therefore works only with short exposures under its own illumination, and TriEye's SEDAR platform pairs it with Coherent's 1,375 nm edge-emitting laser (Jun 2023) [P].
- **Passive SWIR at night.** On moonless nights the sky's nightglow is about ten times brighter in the SWIR than in the visible. Even so, the SWIR sensors available in Europe performed worse than visible cameras at equal f-number, exposure and frame rate, and would need at least a tenfold improvement (Adomeit and Krieg, Fraunhofer IOSB, SPIE 2015) [I].
- **Fog.** SWIR did not improve pedestrian detection in fog; its authors judged thermal imagers the most effective option (Bertozzi et al., ICIAP 2013) [I].
- **Industry ties.** TriEye's automotive links are Porsche as an investor, an evaluation by Denso (Jul 2020) and a collaboration with Hitachi Astemo (Jan 2022); no series programme is public [P, TriEye news page].

**Image intensifiers.**
- **How they work.** Military night-vision tubes multiply the photoelectrons from a photocathode in a microchannel plate before a phosphor screen turns them back into light. A Gen 3 gallium-arsenide photocathode reaches about 30% quantum efficiency at 370–920 nm, with a luminous gain of $4\times10^{4}$ (Hamamatsu V7090U-71) [P].
- **Use in a camera.** The phosphor image must be relayed to a CMOS sensor, or the photocathode built directly over one (electron-bombarded CMOS), so an intensified camera is a vacuum tube plus a camera.
- **Export controls.** Tubes are export-controlled: US ECCN 6A002.a.2 covers tubes with a microchannel-plate pitch of 12 µm or less and a gallium-arsenide or high-sensitivity multialkali photocathode, and goggles with Gen 3 or better tubes fall under USML Category XII [P].
- **Cars.** No production car has used one.

### A7.6 Photon-counting cameras: SPAD and QIS

This subsection reviews the photon-counting sensors and companies behind the automotive claims, and the limits that are specific to SPAD imagers.

**Canon.**
- **3.2-megapixel SPAD sensor** (Morimoto et al., IEDM 2021): 2,072 × 1,548 pixels at 6.39 µm, back-illuminated and 3D-stacked (90 nm). Its breakdown voltage is 30 V and its excess bias (the bias above breakdown) 2.5 V. Peak photon detection efficiency (PDE, the share of arriving photons that are counted) is 69.4%, and 24.4% at 940 nm. Dark count rate (DCR) is 1.8 counts per second at 25 °C and timing jitter 100 ps [I]. Canon showed monochrome video at 0.002 lux; that is 0.6–1.5 detected photons per pixel per frame (§A7.1).
- **Products.** Canon sells two security cameras with these sensors. The MS-500 (sold from Aug 2023) gives 0.001 lux minimum illumination in colour night mode at f/1.4 equivalent, 1/30 s and maximum gain, without adding frames together; it draws up to 23.7 W and weighs 2.2 kg [P]. The MS-510 (announced Apr 2026) has a new sensor with higher NIR sensitivity and reaches 0.0006 lux under the same conditions [P]; its estimated US retail price is \$22,800 [T].
- **2.1-megapixel automotive HDR sensor** (Ota et al., VLSI 2025): a 2/3-inch, 3D-stacked, back-illuminated sensor with 156 dB of dynamic range in one shot, which the abstract describes as being "for automotive applications" [P].
  - **Weighted photon counting.** In each time window the pixel measures how long the first photon takes to arrive and estimates from it how many photons arrive over the whole period, so in bright light it fires only a fraction of the avalanches that a counting pixel would and does not saturate [P].
  - **Power.** Canon's release says this cuts the power per pixel by roughly 75%, against a sensor whose dynamic range it raises about fivefold (Canon's ISSCC 2022 sensor: 143 dB, 0.37 W at about 1 megapixel [I]); at Canon's briefing a manager put the saving at about half [P/T]. Absolute power, pixel pitch, temperature range and AEC-Q status are not published (Appendix 1).
  - **Demonstrations.** Canon shows pedestrians detected 120 m ahead at 0.1 lux with a 25 mm f/1.4 lens, without giving exposure or reflectance [P]. The sensor keeps sampling through the frame, so it records Japanese traffic lights, which switch off four times per frame, as half on [T].
  - **Production.** Canon "aims to start mass production" [P], and Japanese trade press reported 2031 as the target for mass production [T, kuruma-news, Jun 2025].

**Other SPAD imagers.**
- **Sony.** All of Sony's SPAD products are depth sensors; its photon-counting image sensors remain research. One is 748 × 448 pixels at 3.36 µm, 120 dB and 104 mW at 60 frames per second (VLSI 2023); another is a 3.06 µm pixel with 57% PDE (Sensors 2023) [I].
- **Panasonic.** A 1,200 × 900-pixel sensor of 6 µm vertical avalanche photodiodes, aimed at time-of-flight, passed 1,000 h at 125 °C (2024) [I].
- **PolarisIC (北极芯微, China).** Its PCM7200 (Sep 2026) has 2,080 × 1,568 pixels at 8 µm in a 3D-stacked, back-illuminated design, runs at 1,000 frames per second at full resolution and claims up to 150 dB of dynamic range; PolarisIC shows images taken at about 0.001 lux indoors and on a moonless night with a 50 mm f/1.4 lens [P]. No automotive qualification is stated.
- **Pi Imaging (a ZEISS company).** It sells scientific SPAD cameras, for example the SPAD Alpha with 1,024 × 1,024 pixels [P].

**Quanta image sensors.**
- **What they are.** A QIS counts photoelectrons without avalanche gain, with an amplifier quiet enough to tell 0, 1 and 2 electrons apart.
- **Gigajot.** Its 163-megapixel sensor (Scientific Reports 2022) reaches 0.35 electrons rms of read noise at room temperature, 1.64 electrons per second of dark current per 1.1 µm pixel at 60 °C and a peak quantum efficiency of 87%, but only 10–20% in the NIR; it draws 3.86 W [I].
- **Why it matters here.** With $\sigma_r=0.35$ electrons, $\sigma_r^2=0.12$, a third of the CMOS value used above, so a QIS gets much of a SPAD's gain in Eq. (9017) without avalanche power or a 20–30 V bias [E]. No automotive QIS has been announced.

**AUMOVIO and Ubicept.**
- **AUMOVIO** (Continental's automotive business since Sep 2025). Its Stefan Christmann presented "Cameras That Count – Single Photon Avalanche Diodes Reaching Automotive Imaging" at AutoSens Europe on 24 Sep 2026 [P, agenda]. No abstract, slides or AUMOVIO statement is public.
  - The claim that AUMOVIO has a SPAD camera at A-sample stage, the first functional prototypes of an automotive development, comes only from a LinkedIn post by Ubicept's chief executive [U]. No sensor supplier or carmaker is named.
  - At the same show Ubicept demonstrated AUMOVIO's "Far Sensing" camera running Ubicept's processing, but no source says that camera uses a SPAD [P].
- **Ubicept** (a 2021 spin-off of MIT and the University of Wisconsin–Madison; \$8 M seed round in 2023). It sells processing for SPAD cameras and for CMOS cameras with raw output, and a SPAD evaluation kit with a 1-megapixel sensor from an unnamed partner. It claims 0.05 lux and 140–160 dB with SPAD sensors [P]. It demonstrated Canon's 1-megapixel SPAD at CES 2026 [P].
- **Analysts.** Yole's principal analyst described SPAD cameras as limited to niche applications, with adoption in industrial, automotive and consumer markets held back by pixel size and by the processing load of their data (Jan 2025) [T].

**Limits specific to SPAD imagers.**
- **Power in daylight.** Every avalanche draws a charge $Q$ from the bias supply. An array of $N_{\rm px}$ pixels, each firing at rate $r$, therefore draws

$$P=N_{\rm px}\,Q\,(V_{bd}+V_{ex})\,r,\qquad r\le\frac{1}{e\,\tau_d} \tag{9021}$$

  where $V_{bd}$ is the breakdown voltage, $V_{ex}$ the excess bias, $\tau_d$ the dead time after each avalanche, and $1/(e\,\tau_d)$ the highest count rate of a paralyzable pixel (one whose dead time restarts with every photon that arrives during it), reached at an arrival rate of $1/\tau_d$; $e$ is Euler's number.
  - **The count ceiling, checked.** ST's 10.17 µm pixel confirms the ceiling. Its dead time of 4.3 ns gives $1/(e\times4.3\times10^{-9})\approx86$ million counts per second, against a measured maximum count rate of 85 million [I].
  - **Energy per avalanche.** ST measured 68 fC per avalanche at $V_{bd}=18.6$ V and $V_{ex}=2.5$ V, i.e. $68\times10^{-15}\times21.1\approx1.4$ pJ [I].
  - **Daylight.** In 100 klux daylight a 6.39 µm pixel facing a scene of 20% reflectance receives $4.4\times10^{8}$ photons per second (Eqs. (9013)–(9014)). That is above the ceiling of $6.1\times10^{7}$ for a 6 ns dead time, so a free-running 2.1-megapixel array would fire at the ceiling and draw $2.1\times10^{6}\times1.4\times10^{-12}\times6.1\times10^{7}\approx185$ W [E]. Canon's ISSCC 2022 abstract puts megapixel-scale passive recharging at "tens of watts" in bright light [I].
  - **Staying within 1 W.** The 2.1-megapixel array may then fire at most $1/(2.1\times10^{6}\times1.4\times10^{-12})\approx3.3\times10^{5}$ times per pixel per second. That is 0.5% of the ceiling and 1/1,300 of the daylight arrivals [E]. This is why automotive SPAD imagers count only the first photon of each sub-frame and infer the flux from its timing (Canon), recharge on a clock, or switch a pixel off once it has counted enough.
- **Dark counts and temperature.** They cap the low-light gain at automotive temperatures (§A7.2).
- **Pixel size.** Because a SPAD's guard ring and isolation do not shrink with the pixel, fill factor and detection probability fall as the pitch shrinks; for the device configuration that Morimoto and Charbon analysed, detection probability reaches zero at a pitch of about 10 µm unless process and design rules change (Sensors 2021) [I]. Canon's 6.39 µm "charge-focusing" pixel avoids this and claims a 100% fill factor [P]. Automotive CMOS pixels are 2.1–3 µm, so a SPAD camera of equal resolution needs a sensor and lens about 2–3 times larger in each dimension (at fixed field of view and f-number, aperture scales with pixel pitch, §A4) [E].
- **Export controls.** US ECCN 6A002.a.3.g controls focal-plane arrays of more than 32 elements that peak at 400–900 nm and are specially designed or modified to achieve "charge multiplication" (gain by impact ionization), with a radiant sensitivity above 10 mA/W beyond 760 nm [P]. No classification of a SPAD image sensor under it has been published (Appendix 1). A QIS has no charge multiplication [E].

### A7.7 Against thermal

This subsection sets all the routes side by side. In short, reflected-light cameras that rely on the scene's own light cannot close the low beam's night gap, active ones can, and thermal does not need light at all.

| Route | What it senses | Behind the windshield? | What limits it at night | Status in cars (2026) |
|---|---|---|---|---|
| Thermal (8–14 µm microbolometer) | Emitted heat | No: grille window of germanium or chalcogenide (§A3) | Resolution; contrast through clothing and on hot nights; window wetting (§A3, §A5) | Factory option since 2000; an AEB input on the Zeekr 9X (§A1, §A4) |
| Low-light CMOS | Reflected visible light | Yes | Photons and read noise: about 0.1–1 photoelectron per pixel per frame on dark clothing beyond the low beam (§A7.1) | Every ADAS camera; high dynamic range and flicker mitigation, no night-specific product |
| NIR lamps + silicon camera | Light reflected from its own invisible lamps | Yes | Lamp power, eye safety, fog backscatter | Toyota from 2002; Lexus until the 2013 GS; Mercedes 2005–2020 (thermal added in 2013) |
| Gated NIR | Light from its own laser pulses, in a range slice | Yes | Laser power, eye safety | Serial production claimed; no named car |
| Active SWIR | Light from its own 1,375 nm laser | Not established for coated windshields [U] | Dark current (needs short, illuminated exposures) | Evaluations only |
| Image intensifier | Reflected light, amplified | Yes | Cost, export controls, analog output | None |
| SPAD camera | Reflected light, counted | Yes | Same photons as CMOS; dark counts at temperature; daylight power; pixel size | Canon targets 2031 [T]; AUMOVIO talk; A-sample claim [U] |
| QIS | Reflected light, counted without avalanche | Yes | Same photons as CMOS; NIR efficiency; power at high pixel counts | No automotive product |

**What this means** [E]:
1. **The deciding quantity is photons, not detector technology.** A passive camera, photon-counting or not, sees a dark-clothed pedestrian beyond the low beam with a few tenths of a photoelectron per pixel per frame. Photon counting stretches an ideal detector's range by about a fifth to a third and a pixel-level image's by about an eighth (§A7.3). Neither brings dark-clothed pedestrians on unlit roads reliably within stopping distance at highway speed.
2. **What works adds light or does without it.** NIR lamps and gated lasers add invisible light; high beams and ADB add visible light where traffic allows (§A6.3); thermal needs no light. Of these, ADB and thermal are in production in 2026.
3. **SPAD cameras answer a different question first.** Their automotive case rests on dynamic range (156 dB in one shot), flicker immunity and motion handling by burst processing, i.e. on mixed-light and daytime problems as much as on darkness. With first-photon readout their daylight power can be managed, but no price, power or temperature figure has been published for an automotive part.
4. **For the sensor debate.** A low-light camera is not a substitute for thermal on an unlit road. It competes with better headlights, and complements them, rather than with thermal.

Sources: https://arxiv.org/abs/1709.09558 (Hänel et al. 2018, night illuminance) ; https://doi.org/10.2352/EI.2022.34.16.AVM-215 (Funatsu et al. 2022, CFA sensitivities) ; https://imagesensors.org/Past%20Workshops/2019%20Workshop/2019%20Papers/R32.pdf (OmniVision split pixel, IISW 2019) ; https://imagesensors.org/Past%20Workshops/2023%20Workshop/2023%20Papers/R42.pdf (onsemi 8.3 MP, IISW 2023) ; https://imagesensors.org/Past%20Workshops/2017%20Workshop/2017%20Papers/R07.pdf (McGrath et al., dark current, IISW 2017) ; https://thinklucid.com/product/triton-5-mp-imx490/ (IMX490 EMVA 1288 data) ; https://www.sony-semicon.com/en/products/is/security/security.html (STARVIS and SNR1s) ; https://whitepapers.axis.com/en-us/lightfinder (minimum-illumination figures) ; https://www.hikvision.com/ca-en/core-technologies/low-light-imaging/darkfighters/ (DarkFighterS) ; https://www.ovt.com/technologies/nyxel-technology/ (Nyxel) ; https://cdn.euroncap.com/cars/assets/ca_101_testing_at_low_ambient_light_conditions_v10_f491a0d293.pdf (Euro NCAP CA-101) ; https://www.deutscher-zukunftspreis.de/en/team-3-2006 (Mercedes Night View tests) ; http://web.archive.org/web/20160304034809/http://media.daimler.com/dcmedia/0-921-1549267-1-1597008-1-0-0-0-0-0-0-0-0-1-0-0-0-0-0.html (2013 S-Class thermal camera) ; https://www.toyota-global.com/company/history_of_toyota/75years/data/automotive_business/products_technology/technology_development/electronics_parts/index.html (Toyota Night View) ; https://www.autoguide.com/auto-news/2013/09/lexus-drops-night-vision-tech.html (Lexus) ; https://spectrum.ieee.org/safer-driving-in-the-dead-of-night-2650250122 (NIR and FIR costs) ; https://doi.org/10.1515/aot-2014-0001 (Grauer 2014, gated imaging) ; https://arxiv.org/abs/1912.03238 (Daimler fog-chamber benchmark) ; https://trieye.tech/wp-content/uploads/2024/08/Raven-TES200-Product-Overview.pdf (TriEye TES200) ; https://www.coherent.com/news/press-releases/coherent-and-trieye-demo-laser-illuminated-shortwave-infrared-imaging-system (TriEye SEDAR) ; https://trieye.tech/news/ (TriEye partners) ; https://doi.org/10.1117/12.2193738 (Adomeit and Krieg 2015) ; https://www.ce.unipr.it/people/bertozzi/pap/cr/iciap2013.pedSWIR.pdf (Bertozzi et al. 2013, SWIR in fog) ; https://www.ce.unipr.it/people/bertozzi/pap/cr/iv2003-ir-vw.pdf (Bertozzi et al. 2003, pedestrians in thermal images) ; https://www.hamamatsu.com/us/en/product/type/V7090U-71/index.html (Gen 3 tube) ; https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-774/appendix-Supplement%20No.%201%20to%20Part%20774 (ECCN 6A002) ; https://global.canon/en/news/2021/20211215.html (Canon 3.2 MP SPAD) ; https://imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R01.1.pdf (SPAD pixel comparison table) ; https://canon.jp/biz/product/camera/nvs/high-sensitivity-camera/ms500/spec (MS-500) ; https://canon.jp/biz/product/camera/nvs/high-sensitivity-camera/ms510/spec (MS-510) ; https://prtimes.jp/main/html/rd/p/000001189.000013980.html (MS-510 release) ; https://www.newsshooter.com/2026/04/15/canon-announces-1-inch-spad-sensor-ms-510-extreme-low-light-multi-purpose-camera/ (MS-510 price) ; https://global.canon/en/news/2025/20250612.html (Canon automotive HDR SPAD) ; https://archive.vlsisymposium.org/25web/wp-content/uploads/VLSI2025_Advanceprogram0611.pdf (VLSI 2025 paper C27-1) ; https://kuruma-news.jp/post/916461 (Canon briefing and 2031 target) ; https://imagesensors.org/Past%20Workshops/2023%20Workshop/2023%20Papers/R82.pdf (ST SPAD pixel, IISW 2023) ; https://www.mdpi.com/1424-8220/24/16/5414 (Panasonic VAPD at 125 °C) ; https://www.polarisic.com/news/detail/index252.html (PolarisIC PCM7200) ; https://doi.org/10.1038/s41598-022-17952-z (Gigajot 163 MP QIS) ; https://auto-sens.com/session/aseur26/cameras-that-count-single-photon-avalanche-diodes-reaching-automotive-imaging/ (AUMOVIO talk) ; https://auto-sens.com/blog/cutting-edge-technologies-on-display/ (Ubicept and AUMOVIO demo) ; https://www.ubicept.com/products/evaluation (Ubicept evaluation kit) ; https://interestingengineering.com/ces-2025/machine-vision-spad-sensor-dark (Yole on SPAD cameras) ; https://www.mdpi.com/1424-8220/21/10/3447 (SPAD pixel scaling) ; https://platformselect.autonomoustuff.com/wp-content/uploads/2019/05/flir-adk-datasheet-whitelabel.pdf (FLIR ADK)
