"""§E4.1: glare through dirty glass for cameras and lidar, with its cross-references.

Inserts §E4.1 (the veil model, measured windshield scatter, a low sun and oncoming high beams for the camera, the
common cause with the driver, what lidar suffers, how often, and what carmakers do) before §E5, and updates the
executive summary's weather bullet, §A6.1, §C0 subsection 5.4, the §E4 table, §E12.2, Appendix 1 and Appendix 2.
Every number in the new text is printed by build/figures/glare_veil.py (glare_veil_tables.txt).

Usage: glare_veil_edit.py <report.md> <expected sha256 prefix> [--write]
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

EDITS = []

# ---------------------------------------------------------------- executive summary, weather bullet
EDITS.append((
    "    - **Weather.** In fog, lidar and cameras fail together, because fog droplets scatter both of their short "
    "optical wavelengths. Radar, at millimetre wavelengths, is the orthogonal channel, i.e. the one whose failures are "
    "largely independent.\n",
    "    - **Weather.** In fog, lidar and cameras fail together, because fog droplets scatter both of their short "
    "optical wavelengths. Radar, at millimetre wavelengths, is the orthogonal channel, i.e. the one whose failures are "
    "largely independent. Glare is a different case: a low sun or oncoming high beams veil a camera and the driver "
    "behind the same windshield, over a zone that dirt on the glass widens from 4–10° to 22–26° around a sun 10° high, "
    "while a lidar loses range only within a few degrees of the sun (§E4.1).\n",
))

# ---------------------------------------------------------------- §A6.1, after the Wood et al. bullet
EDITS.append((
    "- Measurement agrees: in a closed-road study, drivers using low beams against oncoming glare recognized only 5% of "
    "black-clad pedestrians (Wood, Tyrrell & Carberry 2005) [I], against about 40% without glare [U].\n",
    "- Measurement agrees: in a closed-road study, drivers using low beams against oncoming glare recognized only 5% of "
    "black-clad pedestrians (Wood, Tyrrell & Carberry 2005) [I], against about 40% without glare [U].\n"
    "- A camera behind the windshield sees the same veil, and dirt on the glass multiplies it; oncoming high beams put "
    "14–43 times more light on the glass than these low beams (§E4.1).\n",
))

# ---------------------------------------------------------------- §C0 subsection 5.4, window dirt
EDITS.append((
    "- **Dust, mud, salt or droplets on the window,** which scatter light out of the beam at every wavelength.\n",
    "- **Dust, mud, salt or droplets on the window,** which scatter light out of the beam at every wavelength. Dry "
    "windshields in service scatter 4–7% of the light that crosses them by more than 1°, which costs 0.4–0.6 dB "
    "two-way; water and heavy dirt cost more (§E4.1).\n",
))

# ---------------------------------------------------------------- §E4 table row
EDITS.append((
    "| Low sun / glare | Weak | Some sunlight noise | Unaffected |\n",
    "| Low sun / glare | Weak; worse through dirty glass (§E4.1) | Background noise within a few degrees of the sun "
    "(§E4.1) | Unaffected |\n",
))

# ---------------------------------------------------------------- §E4.1, before §E5
E41 = r"""### E4.1 Glare through dirty glass: how cameras are dazzled, and how much lidar is

The table above rates the camera "weak" in low sun and glare. This subsection works out how weak and why, because glare is a failure that the forward camera shares with the driver who supervises it, and one that dirt on the windshield multiplies. It then asks how much a lidar suffers from the same glare and the same dirt. The short answer [E]: dirt raises the light that a windshield scatters five- to fourteenfold over cleaned glass. With the sun 10° above the road ahead, it widens the zone in which a dark pedestrian loses half of its contrast to the camera from 4–10° around the sun (new or cleaned glass) to 22–26° (glass as found), and at night it lets oncoming high beams outshine a dark pedestrian 24–118 times. A lidar loses range only within a few degrees of the sun (2.6–5.3°, depending on dirt, sun height and wavelength), and through the same dirt its main cost is the window's loss of transmission: 4–7% of a time-of-flight lidar's range and 12–20% of a coherent design's.

**The veil.** Light from a bright source that the glass scatters forward reaches the camera from the direction of every object behind that patch of glass, as a luminous veil laid over the image. Padmos and Alferdinck (TNO, 1983) write the veil seen at an angle $\theta$ from the source as

$$L_{\rm v}(\theta)=E_\perp\,f(\theta) \label{eq:veil-luminance}$$

where $L_{\rm v}$ is the veiling luminance in cd/m², $E_\perp$ the illuminance in lux that the glare source produces on a plane square to its direction, and $f(\theta)$ the glass's scatter function in sr⁻¹, i.e. cd/m² of veil per lux of glare (their Eq. 7, report p. 10) [I]. For the eye, the Stiles–Holladay rule, Eq. \eqref{eq:stiles-holladay-glare}, is the same relation with $f=10/\theta^2$ ($\theta$ in degrees). The veil adds the same luminance to a target and to the background it is seen against, so a target of contrast $C=(L_{\rm t}-L_{\rm b})/L_{\rm b}$ keeps

$$C'=C\,\frac{L_{\rm b}}{L_{\rm b}+L_{\rm v}} \label{eq:veil-contrast}$$

where $L_{\rm t}$ and $L_{\rm b}$ are the luminances of target and background in cd/m². A veil as bright as the background halves the contrast. Three consequences follow [E]:
- **A wider dynamic range does not undo it.** The veil is light added to the optical image before it reaches the sensor, so the 110–156 dB of today's automotive image sensors (§A7.4, §A7.6) records it faithfully. Processing can subtract a smooth veil and stretch the contrast back, but not the veil's photon noise, nor a veil made uneven by spots, streaks and wiper arcs. In the low-sun case below, the veil through an average windshield is 8.4 times the difference between pedestrian and road, so an unevenness of 12% across the glass is as large as the pedestrian's whole contrast.
- **A uniformly bright surround veils little.** Light arriving from all directions with mean luminance $\bar L$ produces $L_{\rm v}=\bar L\,g$, where $g=\int f\,d\Omega$ is the fraction of the light that the glass scatters (their Eqs. 5–6). For an average windshield as found, $g$ summed over 1–110° is 0.043 (below), so a uniform daylight surround veils only about 4% of its own luminance. This explains why AAA's test with a bug-and-dirt pattern on the windshield changed nothing: a 2020 Buick Enclave detected its target 148.19 ft ahead with the clean windshield and 147.88 ft ahead with the dirty one at 35 mph (Fig. 52, p. 46), and the report states that no test was run with a low sun (pp. 30–31) [I]. Glare needs a concentrated source: a low sun or headlamps.
- **The camera's own lens adds its scatter to the windshield's.** No automotive camera's stray light has been published (Appendix 1), so the windshield's veil below is a lower bound for the camera's.

**What windshields scatter, measured.** Padmos and Alferdinck measured the windshields of 25 cars in service, dry and as found, in white light (Table II, p. 30) [I]. The fraction scattered between 1° and 20° from the source, $g(1,20)$, was 0.035 on average and 0.057 at the 85th percentile; between 20° and 50° it was 0.0058 and 0.0097, and between 50° and 110° it was 0.0026 and 0.0045. They fitted the 85th-percentile ("dirty") windshield with

$$f_{\rm dirty}(\theta)=\begin{cases}6.6\,\theta^{-1.73}, & 1^\circ\le\theta\le9^\circ,\\ 44\,\theta^{-2.6}, & 9^\circ\le\theta\le110^\circ,\end{cases} \label{eq:windscreen-scatter}$$

with $\theta$ in degrees and $f$ in sr⁻¹ (Eqs. 23a–b, p. 31), and noted that it is of the same order as the eye's own scatter. At 40° it gives $44\times40^{-2.6}=0.0030$ sr⁻¹, against the 0.0032 measured at the 85th percentile.

::: side
![Veil per lux of glare versus angle for windshields and the eye](automotive_perception_report_figures/glare_veil.png)

*Figure E4.1.* Veil per lux of glare, $f(\theta)$ of Eq. \eqref{eq:veil-luminance}, against the angle from the glare source, for four windshields and for the driver's eye (Eq. \eqref{eq:stiles-holladay-glare}).
- *Green line:* with a sun 10° high, glass whose curve lies above it halves the contrast of anything seen against the sunlit road ($f=0.0089$ sr⁻¹).
- *Purple line:* above it, the veil gives a lidar more background than a sunlit white scene, the condition of its full-sun specification ($f=0.75$ sr⁻¹).
- *Script:* `build/figures/glare_veil.py` [E].

:::

The four windshields of Figure E4.1 span the range from new to dirty [E]:
- *Dirty (85th percentile)* is Eq. \eqref{eq:windscreen-scatter}.
- *Average as found* is 0.6 times it, the ratio of the mean to the 85th percentile in Table II ($0.035/0.057=0.61$ for $g(1,20)$ and $0.0019/0.0032=0.59$ for the scatter at 40°).
- *Cleaned in service* is the dirty curve divided by 14, the average factor by which a dried road-salt film raised the scatter of 12 new and used windshields in Toet and Alferdinck's measurements (SPIE 8898, 2013, p. 12) [I]. Padmos and Alferdinck's windshields cleaned on both sides scattered $g(1,20)=0.0073$ (Table III, p. 32), 1.8 times this curve's $0.057/14=0.0041$, so cleaning in service may leave more scatter than the curve shows.
- *New, clean* follows $115\,g(1,20)\,\theta^{-1.73}$ with $g(1,20)=0.0010$ (p. 33) below 9°, and above 9° Toet and Alferdinck's fit to new, clean glass, $0.067\,\theta^{-1.50}$, measured from 8° to 50° (Fig. 9, p. 13); the two agree within 4% at 9°.

Dirt, wear and water each raise the scatter [I]:
- **Dirt dominates.** The average windshield as found scattered 4.8 times as much as the cleaned ones ($0.035/0.0073$), the 85th percentile 7.8 times ($0.057/0.0073$), and Toet and Alferdinck's road-salt film 14 times. Dirt on the inside scattered as much as dirt on the outside at small angles but fell off faster with angle ($\theta^{-3.04}$ against $\theta^{-2.42}$, Table III).
- **Wear adds a slow floor.** $g(1,20)$ of clean glass grew roughly linearly, from about 0.0010 new to about 0.012 after 120,000 km (p. 33).
- **Water is worst.** Imitation rain raised one car's $g(1,20)$ to 0.20 and condensation on the inside to 0.34, giving 2–3 and 4–5 times the dry veil (Fig. 6 and p. 37).

**A low sun ahead.** The daytime case is a sun 10° above the horizon straight ahead, behind a pedestrian in dark clothing who stands on the road with the shaded side toward the camera. Its inputs are measured clear-sky daylight and assumed reflectances [E]:
- *Direct sunlight.* Gillette's clear-sky formula gives the illuminance on a plane square to the sun as $E_\perp=127.5\ {\rm klx}\times e^{-0.210/\sin h}$, where $h$ is the sun's altitude (NBS BSS 152, Eq. 3.11, p. 20, constants p. 23) [I]. At $h=10^\circ$ it gives $127.5\times e^{-0.210/0.1736}=127.5\times e^{-1.209}=38.0$ klx, and at 20° it gives 69.0 klx.
- *Skylight.* Kimball and Hand's clear winter sky puts 683 foot-candles (7.35 klx) on a horizontal surface and 257 fc (2.77 klx) on a vertical surface facing away from a sun 20° high (Table 4, p. 618), and about 375 fc (4.04 klx) and 170 fc (1.83 klx) for a sun 10° high, read from their Fig. 6 (p. 619) [I].
- *Road.* With reflectance 0.1, the horizontal illuminance $38{,}000\times\sin10^\circ+4{,}040=10{,}640$ lx gives the road a luminance $L_{\rm b}=0.1\times10{,}640/\pi=339$ cd/m² by Eq. \eqref{eq:lambertian-luminance}.
- *Pedestrian.* Dark clothing of reflectance 0.05 (as in §A6.1), on a side lit by the sky and by the road, receives $E=1{,}830+\tfrac12\times0.1\times10{,}640=2{,}360$ lx, 6.2% of the direct sun. It has $L_{\rm t}=0.05\times2{,}360/\pi=37.6$ cd/m², and its contrast is $C=(37.6-339)/339=-0.89$.
- *Halving level.* By Eqs. \eqref{eq:veil-luminance} and \eqref{eq:veil-contrast}, the veil halves this contrast where $L_{\rm v}=L_{\rm b}$, i.e. where $f=L_{\rm b}/E_\perp=339/38{,}000=0.0089$ sr⁻¹ (the green line of Figure E4.1). An average windshield reaches it where $0.6\times44\,\theta^{-2.6}=0.0089$, i.e. at $\theta=(26.4/0.0089)^{1/2.6}=21.6^\circ$.

| Windshield | Contrast halved within (sun 10° / 20° high) | Contrast kept by a pedestrian beneath the sun (10° / 20°) | Veil brighter than the pedestrian within (10°) |
|---|---|---|---|
| New, clean | 4.4° / 3.3° | 81% / 95% | 16.6° |
| Cleaned in service | 9.5° / 7.5° | 53% / 92% | 22.2° |
| Average as found | 21.6° / 18.1° | 12% / 57% | 50.4° |
| Dirty (85th percentile) | 26.3° / 22.0° | 7.5% / 44% | 61.4° |
| Driver's eye (Stiles–Holladay), for comparison | 33.5° / 26.5° | 8.2% / 36% | 101° |

*How the numbers are derived* [E]: each angle solves $f(\theta)=L_{\rm b}/E_\perp$ (first column) or $f(\theta)=L_{\rm t}/E_\perp$ (last column) for the curves of Figure E4.1. The middle column is $L_{\rm b}/(L_{\rm b}+E_\perp f(h))$, Eq. \eqref{eq:veil-contrast} for a pedestrian at the angle $h$ below the sun. A sun 20° high gives $E_\perp=69.0$ klx, a road of 985 cd/m² and a pedestrian of 68.7 cd/m², so $f=0.0143$ sr⁻¹ halves the contrast. The script `build/figures/glare_veil.py` prints every entry.

*Reading the table* [E]:
- **Dirt turns a local problem into a wide one.** Through new or cleaned glass, the camera loses half of the contrast only within 4–10° of the sun; through glass as found, within 22–26°. For a sun 10° high that zone meets the road up to 19° (average) or 24° (dirty) to either side of the sun's direction, a sector 39–49° wide.
- **Beneath the sun, dirt decides.** A pedestrian standing on the road 10° below a sun 10° high keeps 81% of its contrast through new glass, 53% through cleaned glass, 12% through an average windshield and 7.5% through a dirty one. The driver's own eye keeps 8.2% before the windshield's veil is added.
- **A higher sun relieves it quickly.** A sun 20° high is 1.8 times brighter (69.0 against 38.0 klx), but a pedestrian beneath it is now 20° away, where the scatter is $2^{2.6}=6.1$ times weaker, and the road is brighter. An average windshield then keeps 57% of the contrast, and only dirty glass halves it, within 22°.
- **A sun visor does not help the camera.** It shades the driver's eye but not the windshield, which the sun lights from outside, so the veil still forms on the glass in front of driver and camera.

**Oncoming high beams at night.** At night the glare source is a pair of oncoming headlamps, and the targets are about 2,000 times darker than by day [E]:
- *Geometry, as in §A6.1.* The oncoming lamps are 50 m ahead and 3 m to the side, i.e. $\arctan(3/50)=3.43^\circ$ from the line of sight.
- *High beams.* FMVSS No. 108 requires a US upper beam to send at least 15,000 cd toward H-3L and 5,000 cd toward 1U-3L (Table XVIII, p. 479 of the 2025 edition) [P]. An eye or camera 3.43° to the left of the lamps and slightly above them lies between these points, so two lamps put $2\times5{,}000/50^2=4$ to $2\times15{,}000/50^2=12$ lx on the windshield, 14–43 times the 0.28 lx of two low beams at their B50L limit (§A6.1). The regulation sets only these minima there; its 75,000 cd maximum applies straight ahead.
- *Target.* The dark pedestrian of §A6.1, at 5 lx in the low-beam hotspot, has $L_{\rm t}=0.05\times5/\pi=0.080$ cd/m², against a road of $0.1\times5/\pi=0.16$ cd/m².

| Windshield | Veil from two high beams (cd/m²) | Veil ÷ pedestrian's luminance | Contrast kept | Photon-limited signal-to-noise ratio divided by |
|---|---|---|---|---|
| New, clean | 0.05–0.16 | 0.7–2.1 | 75–49% | 1.2–1.5 |
| Cleaned in service | 0.22–0.67 | 2.8–8.4 | 42–19% | 1.7–2.6 |
| Average as found | 1.9–5.6 | 24–71 | 7.8–2.8% | 4.1–6.9 |
| Dirty (85th percentile) | 3.1–9.4 | 39–118 | 4.8–1.7% | 5.2–8.9 |
| Driver's eye (Stiles–Holladay), for comparison | 3.4–10.2 | 43–128 | 4.5–1.5% | 5.4–9.3 |

*How the numbers are derived* [E]: the veil is Eq. \eqref{eq:veil-luminance} at 3.43° for 4–12 lx. Through an average windshield $f=0.6\times6.6\times3.43^{-1.73}=0.47$ sr⁻¹, so $L_{\rm v}=4\times0.47=1.9$ to $12\times0.47=5.6$ cd/m². The contrast kept is Eq. \eqref{eq:veil-contrast} against the road. The last column assumes that the camera finds the pedestrian by comparing its pixels with an equal area of road and that photon noise dominates, as it does at night. The signal then stays $L_{\rm b}-L_{\rm t}$ while the noise grows as $\sqrt{L_{\rm b}+L_{\rm t}+2L_{\rm v}}$, so the signal-to-noise ratio falls by $\sqrt{1+2L_{\rm v}/(L_{\rm b}+L_{\rm t})}$; for the average windshield at 4 lx, $\sqrt{1+2\times1.88/0.239}=4.1$.

*Reading the table* [E]:
- **Through clean glass, high beams add a veil about as bright as the pedestrian; through glass as found, they bury it.** The veil of an average windshield is 24–71 times the pedestrian's luminance, about as large as the eye's own glare.
- **Processing cannot restore what photon noise takes.** An average windshield divides the night camera's signal-to-noise ratio for this pedestrian by 4.1–6.9. To win it back, the camera would need $4.1^2=17$ to $6.9^2=48$ times more light, through longer exposures or a larger aperture.

**Camera and driver are dazzled together.** Glare is a common-cause failure [E]. The forward camera sits behind the same windshield as the driver, near the top of the wiped area, and looks along nearly the same line of sight, so the same low sun or high beams and the same dirt veil both at the same moment; the driver's eye then adds scatter of its own, as large as a dirty windshield's (Figure E4.1). In a supervised (L2) system the driver is the fallback for the situations the camera handles badly, so in glare the two channels that §E5 counts as redundant fail together. NHTSA's open investigation EA26002 concerns exactly this situation: FSD's failure to detect degraded visibility, glare included, and to warn the driver (§E12.2).

**What lidar suffers.** A lidar meets the same veil but pays in a different currency: the veil reaches its receiver as background light, which costs range rather than contrast (§C0 subsection 4.2) [E]. A lidar's full-sun range is quoted against a sunlit scene. The §C0 model's high case is a fully sunlit scene of reflectance $\rho_{\rm ref}=0.9$ (subsection 4.2), taken here to be lit by $E_{\rm ref}=100$ klx, the illuminance of vendors' full-sun specifications (§C3b). Such a scene has luminance $\rho_{\rm ref}E_{\rm ref}/\pi$, so a veil raises the background of a pixel that looks at it to

$$m=1+\frac{\pi\,f(\theta)\,E_\perp}{\rho_{\rm ref}\,E_{\rm ref}} \label{eq:veil-lidar-background}$$

times the specification's background, where the 1 stands for the sunlit scene itself. With background dominant, range scales as $m^{-1/4}$ (Eq. \eqref{eq:colour-range-factor} with $a=1$), and the SPAD's dead time costs more on top (§C5b). The equation assumes that a low sun is as much weaker than full sun at the lidar's wavelength as it is in visible light; the fourth bullet below corrects for the near infrared.
- **Only a narrow zone around the sun.** The veil outshines a sunlit white scene where $f>\rho_{\rm ref}E_{\rm ref}/(\pi E_\perp)=0.9\times100{,}000/(\pi\times38{,}000)=0.75$ sr⁻¹ for a sun 10° high (the purple line of Figure E4.1). That happens within 0.3° of the sun through new glass, 0.8° through cleaned glass, 2.6° through an average window and 3.5° through a dirty one; for a sun 20° high, where $f$ must exceed 0.41, within 0.5°, 1.1°, 3.7° and 4.9°.
- **Inside it, a time-of-flight lidar loses range.** At 2° from a sun 10° high, a dirty window's veil alone gives $\pi\times6.6\times2^{-1.73}\times38{,}000/90{,}000=2.6$ times the specification's background, so $m=3.6$ with a sunlit scene behind it, and the range falls to $3.6^{-1/4}=0.72$ of the full-sun specification (0.78 if the scene behind is dark). Paralyzable dead time, with the high case's $x_0=0.244$ (live fraction 0.784, §C0 subsection 4.2), lowers these to 0.62 and 0.71. At 1° from the sun the range falls to 0.57–0.58, or 0.33–0.36 with dead time.
- **Beneath the sun, glare costs the lidar nothing.** A pedestrian standing on the road under a sun 10° high is 10° from it, where even a dirty window's veil adds only $\pi\times0.11\times38{,}000/90{,}000=0.15$ of a sunlit white scene's background (0.09 through an average window), and the pedestrian's shaded side adds almost nothing. The lidar thus ranges that pedestrian against less background than its full-sun specification assumes, while the camera behind the same dirty glass keeps 7.5% of the contrast.
- **The near-infrared correction.** Clear air is more transparent in the near infrared, because Rayleigh scattering falls as $\lambda^{-4}$ and is about seven times weaker at 905 nm than at 555 nm. If clear air's extinction coefficient at 905 nm is 0.06 instead of the 0.210 of Gillette's formula, a sun 10° high is brighter at 905 nm, relative to a sun overhead, by $e^{(0.210-0.06)(1/\sin10^\circ-1)}=e^{0.71}=2.0$ times what photometry says. The zone then widens by $2.0^{1/1.73}=1.5$ times, to 3.9° (average) and 5.3° (dirty), and the background beneath the sun rises to 0.18–0.30 of the specification's, still below it. At 940 nm, water vapour absorbs more of a low sun's light along its longer path through the air (§C4c), which works the other way by an amount that depends on humidity.
- **The sun's disc** (0.533° across, NASA Sun fact sheet [P]) is imaged onto $\tfrac{\pi}{4}(0.533/0.05)^2=89$ macro-pixels of 0.05° (§C0 subsection 4.2), which see only the sun, dirt or no dirt.
- **Headlamps barely reach a lidar.** White LED headlamps emit almost nothing beyond about 780 nm: the spectrum of an ams OSRAM forward-lighting LED falls to about 1% of its peak at 750 nm and ends near 780 nm (KW H2L531.TE datasheet, p. 9) [P], so it adds no background at 905, 940 or 1,550 nm. A halogen lamp (up to 3,200 K, Philips H7 leaflet, p. 3 [P]) does emit in the band: treated as a 3,200 K blackbody, 12 lx of its light carries $12\times2.67\times10^{-5}=3.2\times10^{-4}$ W m⁻² nm⁻¹ at 940 nm. Through a dirty window this adds at most 0.0064 counts per 1 ns bin to the night background of 0.01 (§C0 subsection 4.3). That raises the detection threshold from 3 to 4 counts and the signal needed for 90% detection from 5.3 to 6.7 photoelectrons, which costs a factor $\sqrt{5.31/6.66}=0.89$ of the night range in the pixels near the lamps.
- **The window's transmission is the main cost of dirt.** A dirty window also scatters the lidar's own beam and its echo out of their narrow paths. Counting the light that a windshield scatters beyond 1° as lost on each pass (Table II summed over 1–110°: $g=0.043$ average and 0.071 dirty), the two-way loss is $X=-20\log_{10}(1-g)$: 0.39 dB for an average window and 0.64 dB for a dirty one. This is a lower bound, because light scattered by less than 1° but more than the beam's width is lost too. The background of a uniformly sunlit scene is not reduced, because the light scattered into a pixel replaces what is scattered out of it (the uniform-surround case above). By Eq. \eqref{eq:range-with-extra-loss}, a time-of-flight lidar keeps $10^{-0.39/20}=0.96$ to $10^{-0.64/20}=0.93$ of its range, losing 4–7%. The coherent 25 mm design of §C0 subsection 5.4, which reaches 200 m in clear air, reaches 177 m and 160 m (12% and 20% less, with clear-air extinction included as in that subsection). Coherent detection rejects sunlight, so for an FMCW lidar this loss is the whole cost of dirt.
- **The pulse's own echo from the window.** Dirt also scatters part of each outgoing pulse back into the receiver, as a return at almost zero range. With a dead time of 6 ns it can blind a SPAD for the first 0.9 m at most; how strongly it couples depends on the optical layout, which makers do not publish.
- **Where the lidar sits.** A roof lidar looks through its own window, which no wiper clears unless the car adds a washer; the scatter of lidar windows in service has not been measured (Appendix 1), and the estimates above assume that it equals a windshield's as found. Lidars behind the windshield, such as Hesai's in-cabin unit on the Cadillac VISTIQ (§B6) and the InnovizThree (§C3b), look through the same glass as the camera and share its dirt and its wipers.

**How often, and what carmakers do.**
- **A low sun ahead is common enough to matter.** In Chiba (35.6° N) the sun stands 0–20° high for 1,310 of the 4,395 daylight hours of a year, 29.8% (Hagita and Mori 2014, Table 1, p. 212) [I]. If it dazzles when within 25° of the heading (the halved-contrast zone of glass as found, above) and headings are spread evenly, $50/360$ of them qualify, so a low sun lies ahead for about $0.298\times50/360=4.1\%$ of daytime driving, before buildings and terrain hide it [E]. Drivers feel it: in Chiba's 57,814 daytime crashes in fine weather of 2007–2011, the rate with the sun 10–20° high and within 45° of the heading was about 30.5 crashes per 24 hours of fine weather, against 24–25 with the sun to the side or behind (Fig. 4, p. 213, read by eye) [I].
- **No public test isolates glare on a camera-based system.** AAA's dirty-windshield test excluded a low sun (above). ADAC's April 2026 test of six cars in fog projected a simulated low sun through a fog wall in one scenario but published only overall scores, from 92% for the Mercedes CLA down to 38% for the BYD Seal [I]. In 240 highway trials, a Duke University study found more hands-on-wheel alerts in low sun (4–20° high) for one car model and no relationship for the other (2022, p. 23) [I].
- **Carmakers' manuals name these conditions** [P]. Subaru's EyeSight manual lists strong light from the front, from the sun or from oncoming headlamps, and a windshield obscured by dirt, smears or light reflected off the dirt (pp. 9–10). Toyota's Safety Sense 3.0 manual (2026 Tacoma) warns against bright light shining into the front camera and against a dirty or fogged windshield. Tesla's Model 3 manual says that bright light from oncoming headlamps or direct sunlight interferes with the cameras, asks for the inside of the windshield in front of the camera enclosure to be cleaned periodically, and shows an alert when a hazy residue on the glass obstructs the camera.
- **Countermeasures address parts of the problem.** Toyota heats the windshield around the camera when it may be fogged, Tesla's manual describes a washer nozzle on the front bumper camera, Denso's camera hood blocks cabin light reflected by the inner windshield (US 10,272,849 B2), and soiling detectors such as Valeo's SoilingNet flag a dirty lens on surround-view cameras (arXiv:1905.01492) [P, I]. Nothing removes the veil of a dirty windshield in front of a low sun except cleaning it, which takes an average windshield's halved-contrast zone from 22° back to about 10°.

**What this means for the sensor comparison** [E]. Glare is a camera failure that the supervising driver shares, that windshield dirt multiplies, and that occurs in a few per cent of daytime driving and with every oncoming high beam. A lidar is not immune, but its exposure differs in kind: it loses range within a few degrees of the sun, not beneath it where the road is, and headlamps reach it only through the near-infrared tail of halogen lamps, and then slightly. Its own cost of dirt is the window's transmission, a few per cent of range for time of flight and up to a fifth for a coherent design. In glare, lidar plays the part that radar plays in fog: its failures are largely independent of the camera's.

"""
EDITS.append(("\n## E5. Safety-engineering arithmetic\n", "\n" + E41 + "## E5. Safety-engineering arithmetic\n"))

# ---------------------------------------------------------------- §E12.2
EDITS.append((
    "The degradation detection system is the software that is meant to recognize when the cameras' view is impaired "
    "(by glare, fog or dirt, for example) and to alert the driver.\n",
    "The degradation detection system is the software that is meant to recognize when the cameras' view is impaired "
    "(by glare, fog or dirt, for example) and to alert the driver. §E4.1 estimates how much glare and windshield dirt "
    "impair the camera's image.\n",
))

# ---------------------------------------------------------------- Appendix 1, end of "Sensor and chip specifications"
EDITS.append((
    "\n\n**Night vision beyond thermal (§A7)**\n",
    "\n- **Cameras in glare and dirty glass (§E4.1).** No production automotive camera's stray light (the scatter of "
    "its own lens against angle, with or without the windshield) has been published, and no public test isolates a "
    "camera system's response to a low sun or to high beams: AAA excluded a low sun, and ADAC published only overall "
    "scores. The windshield data are visible-light measurements of dry glass from 1983 (25 cars) and 2013 (12 "
    "windshields); none covers 905, 940 or 1,550 nm, wiper smear, or the film that interior plastics deposit on the "
    "inside of the glass. How often windshields and lidar windows are dirty in service, and how much lidar windows "
    "scatter, were not measured in any source found.\n\n**Night vision beyond thermal (§A7)**\n",
))

# ---------------------------------------------------------------- Appendix 2, a new group after the last item
APPX2 = """
**Glare and dirty glass (§E4.1)**
- Padmos & Alferdinck, Verblinding bij tunnelingangen III: de invloed van strooilicht van de autovoorruit (glare at tunnel entrances III: stray light from the windscreen), TNO report IZF 1983 C-10 (Eqs. 5–7 p. 10, Table II p. 30, Eqs. 23a–b p. 31, Table III p. 32, p. 33, Fig. 6 and p. 37): https://open.rijkswaterstaat.nl/publish/pages/38763/159778.pdf
- Toet & Alferdinck, Effects of high power illuminators on vision through windscreens and driving behavior, Proc. SPIE 8898, 88980I (2013; p. 12, Fig. 9 p. 13): https://doi.org/10.1117/12.2028224
- Gillette, A Daylighting Model for Building Energy Simulation, NBS Building Science Series 152 (1983; Eq. 3.11 p. 20, constants p. 23): https://doi.org/10.6028/NBS.BSS.152
- Kimball & Hand, Daylight illumination on horizontal, vertical, and sloping surfaces, Monthly Weather Review 50(12), 615–628 (1922; Table 4 p. 618, Fig. 6 p. 619): https://journals.ametsoc.org/view/journals/mwre/50/12/1520-0493_1922_50_615_diohva_2_0_co_2.pdf
- FMVSS No. 108, 49 CFR 571.108, 2025 edition, Table XVIII, upper-beam photometry (p. 479): https://www.govinfo.gov/content/pkg/CFR-2025-title49-vol6/pdf/CFR-2025-title49-vol6-sec571-108.pdf
- NASA, Sun fact sheet (apparent diameter 1,919 arcsec at 1 AU): https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
- ams OSRAM, KW H2L531.TE datasheet, relative spectral emission (p. 9): https://look.ams-osram.com/m/3bf1cbb8a87a401e/original/KW-H2L531-TE.pdf
- Philips, Vision H7 leaflet (colour temperature up to 3,200 K, p. 3): https://www.documents.philips.com/assets/20230914/90f6d5e046774aaea2e4b07d017ea191.pdf
- AAA, sensor performance degradation tests with a dirty windshield and simulated rain (2021; pp. 30–31, Fig. 52 p. 46): https://newsroom.aaa.com/wp-content/uploads/2021/10/E-1-Research-Report-Sensor-Performance-Degradation-FINAL-9-28-21.pdf
- ADAC, driver-assistance sensors in fog, with a simulated low sun (14 Apr 2026): https://presse.adac.de/meldungen/adac-ev/tests/sensoren-im-nebel.html
- Duke University, supplemental report on driver-assistance systems in highway trials (2022; p. 23): https://www.roadsafety.unc.edu/wp-content/uploads/2023/08/UNC-Duke-AV-supplemental-report.pdf
- Hagita & Mori, The Effect of Sun Glare on Traffic Accidents in Chiba Prefecture, Japan, Asian Transport Studies 3, 205–219 (2014; Table 1 p. 212, Fig. 4 p. 213): https://www.jstage.jst.go.jp/article/eastsats/3/2/3_205/_pdf
- Subaru, EyeSight owner's manual supplement (2024 Outback, pp. 9–10; a copy posted by an owner): https://komar.org/car/2024_subaru_outback/2024_subaru_manuals/Eyesight_MSA5M2414B_STIS.pdf
- Toyota, 2026 Tacoma owner's manual, Toyota Safety Sense 3.0: https://assets.sia.toyota.com/publications/en/om-x/OM04051U/topics/chapter4/ch04se050402.html
- Tesla, Model 3 owner's manual (US): limitations and warnings, https://www.tesla.com/ownersmanual/model3/en_us/GUID-E5FF5E84-6AAC-43E6-B7ED-EC1E9AEB17B7.html; cleaning, https://www.tesla.com/ownersmanual/model3/en_us/GUID-9A3F0F72-71F4-433D-B68B-0A472A9359DF.html; camera alerts, https://www.tesla.com/ownersmanual/model3/en_us/GUID-65384C1F-86F2-44E8-A8BC-8A12E7E00A40.html
- Denso, camera hood against reflections from the windshield, US 10,272,849 B2: https://patents.google.com/patent/US10272849B2
- Uřičář et al., SoilingNet: soiling detection on automotive surround-view cameras, arXiv:1905.01492 (ITSC 2019): https://arxiv.org/abs/1905.01492
"""
LUMISPOT = ("- Lumispot, 1550 nm pulse-mode fibre laser for lidar (1.4 kW, 3 ns, 500 kHz, 2 W): "
            "https://lumispot-tech.com/1550nm-pulsed-fiber-laser-product\n")
EDITS.append((LUMISPOT, LUMISPOT + APPX2))

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
print(f"length {len(text)} -> {len(new)} characters")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
