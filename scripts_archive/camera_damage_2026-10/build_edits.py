"""Additions of 2026-10-29: lidar damage to cameras (§C4c subsection 1), its 1,550 nm mechanism, single-shot against
cumulative damage, and an estimate of how likely damage is.

Sources read for these edits:
- Bi et al., Opt. Express 32(3), 4709-4719 (2024), all pages (Figs. 1-8, Tables 1-3);
- Theberge et al., Appl. Opt. 61(10), 2473-2482 (2022), all pages (Figs. 1-9, Tables 1-2);
- Westgate & James, Sensors 22(7), 2526 (2022), full text (Section 1, Section 3.3, Tables 1-3);
- Qian, Peng & Xu, Chinese Optics 18(2), 256-265 (2025), Figs. 8, 11, 14-16 and Table 3;
- Ars Technica (11 Jan 2019), ifanr (16 Feb 2023), HiEV via 36Kr (17 Mar 2023), The Drive (12 May 2025);
- Lumispot, 1550 nm pulse-mode fibre laser product page.
The arithmetic of the estimate is in estimate.py (same folder).
Writes edits.json (§C4c and Appendix 2) and appendix1_pair.json (one Appendix 1 pair, applied with that appendix's
own batch). The report is only read.
Usage: python build_edits.py [--force]
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = HERE.parent.parent / "automotive_perception_report_2026-09-27.md"
T = REPORT.read_text(encoding="utf-8")
WHY = "Lidar damage to cameras, checked against the sources listed in build_edits.py (2026-10-29)."


def edit(eid, old, new):
    assert T.count(old) == 1, (eid, T.count(old), old[:70])
    return {"id": eid, "finding": "Lidar damage to cameras: cases, mechanism and likelihood", "old": old, "new": new,
            "why": WHY}


def line_starting(prefix):
    hits = [l for l in T.split("\n") if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


def appendix2_group_end(group):
    """The last list line of an Appendix 2 group (bold heading)."""
    a = T.index("# Appendix 2")
    m = re.search(r"(?m)^\*\*" + re.escape(group) + r"\*\*\s*$", T[a:])
    start = a + m.end()
    nxt = re.search(r"(?m)^\*\*[^*]+\*\*\s*$|^\*[^*]+\*\s*$|^#", T[start:])
    body = T[start:start + nxt.start()] if nxt else T[start:]
    return [l for l in body.split("\n") if l.startswith("- ")][-1]


BLOCK = [
    r"",
    r"**Eye-safe is not camera-safe** [P/T/E]. Class 1 protects the eye; IEC 60825-1 sets no limit for camera sensors. Cameras have been reported damaged by 1,550 nm lidars in several publicised cases, all of them photos or videos taken of the lidar. Two laboratory studies show how light that silicon hardly absorbs can still destroy a silicon image sensor. The estimate at the end of this block, which separates single-shot from cumulative damage, finds damage likely for a phone filming a 1,550 nm lidar from a few metres, possible for a camera held in front of one for many minutes out to tens of metres, and unlikely in passing traffic.",
    r"",
    r"- **Reported cases** [T].",
    r"  - At CES 2019 the autonomous-vehicle engineer Jit Ray Chowdhury photographed a car carrying AEye's 1,550 nm lidars. Every later picture from his \$1,998 Sony camera showed two bright purple spots with horizontal and vertical lines running from them, even with the lens cap on. AEye's chief executive wrote to Ars Technica that cameras can be up to 1,000 times more sensitive to lasers than eyes and can occasionally suffer thermal damage to the focal-plane array; the company later said he had meant lasers in general, and it offered to buy a new camera. Blackmore, a maker of FMCW lidar, said that a video camera had filmed its sensor from about four feet for 45 minutes without damage [T, Ars Technica, 11 Jan 2019].",
    r"  - In Feb 2023 a widely shared video showed a phone filming the roof lidar of a NIO ES7, a 1,550 nm Falcon made by Innovusion (Seyond's name until 2024), until one horizontal and one vertical line stayed in the image [T, ifanr, 16 Feb 2023]. HiEV reported a similar ES7 video, taken while the car was parked with its lidar running, and night photos of a NIO ET5 under the Milky Way that showed two bright points that were not stars [T, HiEV via 36Kr, 17 Mar 2023].",
    r"  - In May 2025 a Reddit user's phone showed multicoloured specks after filming the roof lidar of a Volvo EX90, a Luminar Iris (§B2); the specks vanished when the phone switched to another lens, which has its own sensor. Volvo's support page says not to point a camera directly at the lidar, and Volvo told The Drive that close-ups are the problem and that filters or protective covers on the lens help [T, The Drive, 12 May 2025].",
    r"  - No laboratory analysis of these cameras was published, and no report of a camera on another vehicle damaged by a lidar was found. The damage patterns, bright spots and lines through them, match the laboratory results below.",
    r"- **Why a camera is more exposed than an eye** [P].",
    r"  - Above 1,400 nm, water in the cornea and lens absorbs the light before the eye can focus it (above), but a camera lens focuses it, so the 460–950 times larger pulses that Class 1 allows a scanned 1,550 nm raster (table above) reach a camera's sensor concentrated. The lens gathers the light over its whole aperture onto a spot a few pixels wide: Westgate & James put the ratio of irradiance at the pixel to irradiance at the lens at $10^6$ or more, for a 25.4 mm lens at f/8 and 532 nm (their Section 1).",
    r"  - Visible-light cameras block the near infrared with filters specified only to about 1,200 nm (optical density, OD, 2.5 from 700 to 1,200 nm in the colour camera of Théberge et al., p. 2474), and Bi et al. note that cameras lack a 1,550 nm filter (p. 4710).",
    r"- **How 1,550 nm light damages a silicon sensor** [P].",
    r"  - A 1,550 nm photon carries 0.80 eV, less than silicon's 1.12 eV band gap, so the photodiodes hardly respond; Bi et al. still saw the focused spot, which they attribute to impurity levels in the gap (p. 4712). The energy is absorbed instead by the colour-filter polymer above the pixels and by the wiring below them, whose absorption does not depend on the band gap.",
    r"  - Bi et al. (Hesai, which funded the work) focused 1,550 nm pulses of 4–10 ns at 50–800 kHz to a ≈30 µm spot on a Sony IMX415, a back-illuminated (BSI) colour sensor without an infrared filter (Table 2 and p. 4711). Damage grew from a point to a line and then to a cross through the spot (Fig. 2, p. 4712), the pattern of the CES and NIO cases. Focused-ion-beam cross-sections (Fig. 8, p. 4717) show the colour filter damaged first, under intact microlenses, at 25 mJ cm⁻² per pulse. At 50 mJ cm⁻² the microlenses and colour filter were ablated and the thin dielectric between the photodiodes and the metal wiring was broken, while the photodiodes showed no abnormal region. In the authors' sequence the colour filter absorbs first, boils and splashes off with the microlens above it (point damage); then the dielectric fails, and short or open circuits in the row and column lines give line and then cross damage (pp. 4716–4717). The same sites were damaged whether or not the sensor was powered, so the damage is optical, not electrical (p. 4716).",
    r"  - In a BSI sensor the wiring lies behind the silicon. Westgate & James attribute the robustness of their BSI sensor at 532 nm to the readout circuitry lying below the photosensitive layer: it needed about 10 times the fluence of front-illuminated sensors for line damage and about 100 times for complete failure (≈10³ against ≈10 J cm⁻²; their Section 3.3 and Table 3). At 1,550 nm that silicon is transparent, the light reaches the wiring, and Bi et al.'s cross-sections show the dielectric next to it failing, so back illumination loses the protection it gives in band [E].",
    r"  - With 4 ns pulses at 400 kHz for 50 ms, Bi et al. found point damage at 17–25 mJ cm⁻² per pulse, and with 10 ns pulses at 37–43 mJ cm⁻² (Fig. 6, p. 4715); line damage needed ≈9.5 mJ cm⁻² more on average (Fig. 7, p. 4716). The 10 ns pulses needed about twice the fluence at a similar peak irradiance, $37$–$43\ {\rm mJ\,cm^{-2}}/10\ {\rm ns}=3.7$–$4.3\ {\rm MW\,cm^{-2}}$ against $17$–$25\ {\rm mJ\,cm^{-2}}/4\ {\rm ns}=4.3$–$6.3\ {\rm MW\,cm^{-2}}$, which the authors read as damage driven by peak power (p. 4715). How the threshold depends on the number and spacing of the pulses is taken up under single-shot and cumulative damage below.",
    r"  - In band, single nanosecond pulses on another Sony BSI sensor (IMX178) need 29 mJ cm⁻² (532 nm) and 41 mJ cm⁻² (1,064 nm) for point damage, and 70 and 101 mJ cm⁻² for line damage (Qian et al., Table 3, p. 263). A few thousand 1,550 nm pulses on one spot therefore damage a sensor at per-pulse fluences similar to or below those of a single in-band pulse.",
    r"  - Théberge et al. (Defence Research and Development Canada) exposed four CCD and CMOS cameras, the colour one with its infrared filter removed, to 100 ms of continuous light at 532, 1,072 and 1,970 nm, and give the thresholds at the sensor surface (pp. 2474–2475; Table 2, p. 2480). At 1,970 nm, which silicon does not absorb either, the damage followed the in-band sequence. First a single pixel's response changed permanently by 50%, through damage to the colour filter or microlenses rather than to the silicon (200–510 kW cm⁻²; definition on p. 2475). Line or cross damage followed at 250–700 kW cm⁻², similar to the in-band values, which the authors tie to melting of the aluminium or aluminium–copper wiring; at 1,072 nm they measured 550–950 °C at the pixels in that range (Fig. 4, pp. 2476–2477; p. 2481). Colour sensors were damaged first because their filters absorb more than the clear microlenses of monochrome sensors (p. 2481). Out of band the camera gives no warning: in band the whole sensor saturates at 5–30 kW cm⁻², 2–3 orders of magnitude below damage, while at 1,970 nm saturation needs 200–540 kW cm⁻², close to the damage thresholds (p. 2481).",
    r"  - The pulses, not the average power, do the damage [E]. At Bi et al.'s 4 ns threshold at 400 kHz the average irradiance is only $20\ {\rm mJ\,cm^{-2}}\times4\times10^{5}\ {\rm s^{-1}}=8\ {\rm kW\,cm^{-2}}$, against the 150 kW cm⁻² to 1.5 MW cm⁻² at which continuous light permanently damaged all of Théberge et al.'s cameras (p. 2481), while the peak irradiance is $20\ {\rm mJ\,cm^{-2}}/4\ {\rm ns}=5\ {\rm MW\,cm^{-2}}$. A lidar's average power on a camera is smaller still (≈0.1 kW cm⁻² in the close-up case below), so its pulse energy is what matters.",
    r"",
    r"**How likely is damage in practice** [E]. A pulse of energy $E_{\rm p}$ leaves the lidar as a beam of diameter $d_0$ that spreads with full divergence $\theta_{\rm b}$, so at range $R$ it is $d_0+\theta_{\rm b}R$ wide. A camera lens whose entrance pupil (the aperture seen from the front) has diameter $D=f/N$, for focal length $f$ and f-number $N$, collects the fraction $\eta=[D/(d_0+\theta_{\rm b}R)]^2$ of the pulse, treating the beam as uniform, or all of it ($\eta=1$) within $R_1=(D-d_0)/\theta_{\rm b}$. It focuses that energy on a spot of diameter $d_{\rm s}$, so the fluence per pulse on the sensor is $F=\eta E_{\rm p}/(\pi d_{\rm s}^2/4)$. Setting $F$ equal to a damage threshold $F_{\rm th}$ gives the largest range at which damage is possible, $R_{\max}=\left[D\sqrt{E_{\rm p}/(F_{\rm th}\,\pi d_{\rm s}^2/4)}-d_0\right]/\theta_{\rm b}$.",
    r"",
    r"- **Inputs.**",
    r"  - $E_{\rm p}=2\ \mu{\rm J}$, with 1 and 10 µJ as bounds. A 1,550 nm fibre source sold for lidar gives 1.4 kW for 3 ns at 500 kHz with 2 W average power, i.e. $2\ {\rm W}/5\times10^{5}\ {\rm s^{-1}}=4\ \mu{\rm J}$ [P, Lumispot product page]; the same 2 W shared among the 900,000 points per second of Seyond's Falcon K1 (§C4d subsection 2) gives $2\ {\rm W}/9\times10^{5}\ {\rm s^{-1}}=2.2\ \mu{\rm J}$. The Class 1 ceiling for a scanned raster is 18–91 µJ (table above). No pulse energy for Seyond's or Luminar's lidars was found.",
    r"  - $d_0=2$ mm and $\theta_{\rm b}=1$ mrad. Innovusion's patent spaces single-mode transmit fibres 100–400 µm apart to send beams 0.5–2.5° apart (§C4b). Taking 200 µm and 1° from those ranges implies a collimating lens of focal length $f_{\rm c}\approx200\ \mu{\rm m}/0.0175\ {\rm rad}=11.4$ mm. The fibre's mode, $2w_0=10.4\ \mu{\rm m}$ across, spreads at a half-angle of $\lambda/(\pi w_0)=1.55\ \mu{\rm m}/(\pi\times5.2\ \mu{\rm m})=0.095$ rad, so the beam leaves $2\times0.095\times11.4\ {\rm mm}=2.2$ mm wide and diverges by $2w_0/f_{\rm c}=10.4\ \mu{\rm m}/11.4\ {\rm mm}=0.9$ mrad, finer than the Falcon's finest sample spacing of 0.08° (1.4 mrad).",
    r"  - $d_{\rm s}=20\ \mu{\rm m}$, so the spot area is $\pi(20\ \mu{\rm m})^2/4=3.1\times10^{-6}\ {\rm cm^2}$. That lies between the diffraction limit at 1.55 µm ($2.44\lambda N$: 6.8 µm at f/1.8 and 10.6 µm at f/2.8) and Bi et al.'s 30 µm test spot, allowing for lenses designed only for visible light. Close up, the spot is also the image of the beam's cross-section, $d_0f/R$: 28 µm for $f=14$ mm at 1 m.",
    r"  - Pulses per camera. While camera and lidar stand still, every pulse that enters the camera lands on the same spot of its sensor, because the lens maps every ray from the lidar's exit window onto the window's image (blurred if the camera is focused elsewhere); the scan decides only when a pulse arrives, not where it lands. A pulse enters when the beam axis passes within $(\theta_{\rm b}+D/R)/2$ of the camera in both axes, so a raster with sample spacings $\Delta\theta_{\rm h}\times\Delta\theta_{\rm v}$ delivers about $(\theta_{\rm b}+D/R)^2/(\Delta\theta_{\rm h}\Delta\theta_{\rm v})$ pulses per frame. For the Falcon K1 these spacings are 0.09° × 0.08° inside its region of interest and 0.18° × 0.24° outside it, at 10 frames/s (§C3b, §C4d). The pulses arrive in bursts: one to a few, microseconds apart, each time a beam sweeps across the camera, with the bursts milliseconds apart (successive scan lines and frames).",
    r"- **Single-shot or cumulative damage.** The threshold depends on how many pulses land on the same spot, and at 1,550 nm only the cumulative case has been measured.",
    r"  - Bi et al. irradiated each site with 2,500 to $2\times10^6$ pulses; with their shutter the threshold of a single pulse or a few pulses could not be measured (p. 4716). Their 4 ns threshold falls from 26–31 mJ cm⁻² with 2,500–5,000 pulses at 50–100 kHz (Fig. 4, p. 4714) to 17–25 mJ cm⁻² with $2\times10^4$ pulses at 400 kHz and to ≈10 mJ cm⁻² with $2\times10^6$ pulses (5 s at 400 kHz; Fig. 6, p. 4715). Two effects lower it (p. 4715). Heat accumulates when pulses arrive before the irradiated layer has cooled, which their simulation shows only above 100–200 kHz, i.e. for pulses less than 5–10 µs apart (Fig. 5). Incubation is damage left by earlier pulses that makes the site absorb later ones more strongly.",
    r"  - A lidar's bursts, milliseconds apart, let the spot cool between them, so heat accumulates over a few pulses at most; incubation, which counts pulses rather than their spacing, still acts. Westgate & James saw cumulative damage without heating, with pulses 100 ms apart: at low fluence five pulses only filled in the damage of the first, but at high fluence each further pulse enlarged it, and five pulses killed a BSI sensor at less than a tenth of the single-pulse fluence (358 against 4,110 J cm⁻²; their Section 3.3 and Table 3).",
    r"  - The measured case closest to a lidar is therefore Bi et al.'s lowest rate, at which neither the threshold nor the simulated heating changes with rate any longer: $F_{\rm th}=26$ mJ cm⁻², the lowest of the four sensors' 26–31 mJ cm⁻² at 50–100 kHz. It is a cumulative threshold, valid when about 2,500 pulses land on one spot, and it is the $F_{\rm th}$ used below.",
    r"  - A single pulse needs more, by a factor not measured at 1,550 nm. For comparison, a single nanosecond pulse in band needs 29–41 mJ cm⁻² for point damage and 70–101 mJ cm⁻² for line damage on a similar BSI sensor (Qian et al., above).",
    r"  - Two regimes follow. A camera that holds the lidar's image on one spot for minutes, such as a fixed camera or a phone on a tripod, is in the cumulative regime, and $F\ge26$ mJ cm⁻² marks possible damage. A handheld or moving camera spreads the pulses over its sensor and gives each spot only one or a few bursts. That is the single-shot regime, whose threshold is higher by the unmeasured factor.",
    r"- **Close-up.** A phone telephoto camera (14 mm, f/2.8, so $D=5$ mm) at 1 m collects whole pulses ($R_1=(5-2)\ {\rm mm}/1\ {\rm mrad}=3$ m), so $F=2\ \mu{\rm J}/3.1\times10^{-6}\ {\rm cm^2}=0.64\ {\rm J\,cm^{-2}}$, or 0.32 J cm⁻² on the 28 µm image spot: 12–25 times the cumulative threshold. Its acceptance window is $\theta_{\rm b}+D/R=1\ {\rm mrad}+5\ {\rm mm}/1\ {\rm m}=6$ mrad (0.34°), so it receives $0.34^2/(0.09\times0.08)=16$ pulses per frame inside the region of interest and $0.34^2/(0.18\times0.24)=2.7$ outside it, i.e. 27–160 pulses/s, and collects 2,500 pulses on one spot in $2{,}500/(160$–$27\ {\rm s^{-1}})=16$–$93$ s. Held steady, it reaches the cumulative regime within about a minute and a half, at more than ten times the threshold. The reported cases, handheld photos and short videos taken from close up, suggest that far fewer pulses suffice at such fluences.",
    r"- **Range in the cumulative regime.** With $E_{\rm p}=2\ \mu{\rm J}$, $\sqrt{E_{\rm p}/(F_{\rm th}\pi d_{\rm s}^2/4)}=\sqrt{2\times10^{-6}\ {\rm J}/(0.026\ {\rm J\,cm^{-2}}\times3.14\times10^{-6}\ {\rm cm^2})}=4.95$, so $R_{\max}=(4.95D-2\ {\rm mm})/1\ {\rm mrad}$; for the telephoto camera, $(4.95\times5-2)\ {\rm mm}/1\ {\rm mrad}=22.7$ m. At $R_{\max}$ the window of every camera in the table except the fisheye is about 1.2 mrad, so it receives 0.11–0.69 pulses per frame and needs 6–38 minutes, fixed in place, to collect 2,500 pulses.",
    r"",
    r"| Camera (focal length, f-number) | Entrance pupil $D$ | Whole pulse enters within $R_1$ | Cumulative damage out to $R_{\max}$ at 1 / 2 / 10 µJ |",
    r"|---|---|---|---|",
    r"| Phone main camera (6.3 mm, f/1.8) | 3.5 mm | 1.5 m | 10 / 15 / 37 m |",
    r"| Phone telephoto camera (14 mm, f/2.8) | 5.0 mm | 3.0 m | 16 / 23 / 53 m |",
    r"| Camera lens (50 mm, f/4) | 12.5 mm | 10.5 m | 42 / 60 / 136 m |",
    r"| Telephoto lens (200 mm, f/2.8) | 71 mm | 69 m | 250 / 350 / 790 m |",
    r"| Car front camera (6 mm, f/1.8) | 3.3 mm | 1.3 m | 10 / 15 / 35 m |",
    r"| Car reversing camera (1.2 mm fisheye, f/2) | 0.6 mm | never | 0.1 / 1.0 / 4.6 m |",
    r"",
    r"- $R_{\max}$ scales as $D\sqrt{E_{\rm p}/F_{\rm th}}/d_{\rm s}$: a 10 µm spot roughly doubles it, and a Gaussian beam centred on the pupil, which delivers up to twice the uniform beam's fluence, lengthens it by up to $\sqrt2$. Beyond the spread in the table, the ranges are uncertain by a factor of about two either way.",
    r"- **The single-shot regime has no measured threshold**, so its range can only be bounded. On the telephoto camera the fluence per pulse, $F=[5/(2+R)]^2\times0.64\ {\rm J\,cm^{-2}}$ with $R$ in metres, falls from 0.64 J cm⁻² at 3 m to 0.32, 0.11 and 0.033 J cm⁻² at 5, 10 and 20 m, i.e. 12, 4.3 and 1.3 times the cumulative threshold. A handheld camera at 10 m is therefore at risk only if one pulse damages the sensor at less than 4.3 times the cumulative threshold, and at 20 m only if it does so at less than 1.3 times; neither factor has been measured.",
    r"- **Cameras on other cars** have small pupils. A front camera ($D=3.3$ mm) facing a 1,550 nm lidar from 5 m collects $[3.3/(2+5)]^2=22\%$ of each pulse, i.e. $0.22\times2\ \mu{\rm J}/3.1\times10^{-6}\ {\rm cm^2}=0.14\ {\rm J\,cm^{-2}}$, 5.4 times the cumulative threshold, but receives only 0.2–1.3 pulses per frame. It therefore needs 3–20 minutes facing the lidar to collect 2,500 pulses, as when two cars stand nose to nose with both systems running. The reversing fisheye of the car in front, 4.5 m from a roof lidar, collects $[0.6/(2+4.5)]^2=0.85\%$, i.e. 5 mJ cm⁻², a fifth of the cumulative threshold. Car cameras are therefore at risk only within about 15 m of a running lidar that they face for many minutes.",
    r"- **905/940 nm lidars.** Eye safety caps their pulses at ≈10–100 nJ (above), 20–200 times below the 2 µJ assumed here. Even a whole 100 nJ pulse in a 20 µm spot gives $10^{-7}\ {\rm J}/3.1\times10^{-6}\ {\rm cm^2}=32\ {\rm mJ\,cm^{-2}}$, close to the in-band single-pulse threshold for a camera without an infrared-cut filter, and an OD 2.5 filter lowers it to 0.1 mJ cm⁻².",
    r"",
    r"**Verdict** [E]. Damage needs a running 1,550 nm pulsed lidar (in cars, mainly Seyond's Falcon on NIO models and Luminar's Iris on the Volvo EX90), a camera without a filter that blocks 1,550 nm, and a line of sight both ways, with the camera inside the lidar's field of view and the lidar inside the camera's frame. It then needs either a short distance or a long, fixed exposure. Within a few metres of the lidar every pulse is an order of magnitude above the cumulative threshold and a short video collects hundreds of pulses. Farther out, damage needs the cumulative regime: a camera held in front of the lidar for minutes to tens of minutes, out to 15–23 m for phone and car cameras and to hundreds of metres for a large telephoto lens (2 µJ pulses). Close-up photos and videos of the lidar meet these conditions, which is the case Volvo's warning addresses. Passing traffic rarely does: car cameras have pupils of a few millimetres or less, receive about one pulse per frame or fewer at traffic distances and move relative to the lidar, consistent with the absence of reported cases. The remedies are a filter that blocks 1,550 nm in front of the sensor, which Bi et al. propose (p. 4718), and, on the lidar side, lower pulse energy at the cost of range.",
]
NEW_BLOCK = "\n".join(BLOCK)

edits = []

# §C4c subsection 1: replace the one-line camera note with the block (the bullet list above it ends on the previous line)
ces = line_starting("- The CES 2019 camera-damage report")
edits.append(edit("K1-C4c-camera-damage", ces, NEW_BLOCK))

# Appendix 2: a new group at the end
last = appendix2_group_end("Adoption outside China (§G6)")
SOURCES = [
    r"",
    r"**Camera damage by lidar (§C4c)**",
    r"- Bi et al., Failure mechanisms of a silicon-based CMOS image sensor irradiated by a 1550 nm nanosecond laser, Optics Express 32(3), 4709–4719 (2024; Hesai; Sony IMX415; Figs. 2–8): https://doi.org/10.1364/OE.515728",
    r"- Théberge et al., Damage thresholds of silicon-based cameras for in-band and out-of-band laser expositions, Applied Optics 61(10), 2473–2482 (2022; continuous light at 532, 1,072 and 1,970 nm; Table 2): https://doi.org/10.1364/AO.450317",
    r"- Westgate & James, Visible-band nanosecond pulsed laser damage thresholds of silicon 2D imaging arrays, Sensors 22(7), 2526 (2022; optical gain, BSI robustness, five-pulse damage, Table 3): https://doi.org/10.3390/s22072526",
    r"- Qian, Peng & Xu, Damage mechanism of back-illuminated CMOS image sensor irradiated by pulsed laser, Chinese Optics 18(2), 256–265 (2025; Sony IMX178; single pulses; Table 3): https://doi.org/10.37188/CO.2024-0139",
    r"- Ars Technica, CES 2019 camera damaged by AEye's lidar, with AEye's and Blackmore's statements (11 Jan 2019): https://arstechnica.com/cars/2019/01/man-says-ces-lidars-laser-was-so-powerful-it-wrecked-his-1998-camera/",
    r"- ifanr, phone camera damaged filming the Falcon lidar of a NIO ES7 (16 Feb 2023): https://www.ifanr.com/1535696",
    r"- HiEV via 36Kr, further NIO phone-camera cases (17 Mar 2023): https://www.36kr.com/p/2175234507616520",
    r"- The Drive, Volvo EX90 lidar and phone cameras, with Volvo's statements (12 May 2025): https://www.thedrive.com/news/volvo-ex90s-lidar-sensor-will-fry-your-phones-camera",
    r"- Lumispot, 1550 nm pulse-mode fibre laser for lidar (1.4 kW, 3 ns, 500 kHz, 2 W): https://lumispot-tech.com/1550nm-pulsed-fiber-laser-product",
]
edits.append(edit("K2-A2-camera-damage", last, last + "\n" + "\n".join(SOURCES)))

# Appendix 1 is edited in its own batch. The item was first inserted after the IEC 60825-1 item by that batch
# (appendix1_pair.json, applied 2026-10-29); once it is in the report, only a wording pair is written.
A1_ITEM = (
    "- **Camera damage by lidar (§C4c subsection 1).** No laboratory analysis of the cameras in the reported cases was "
    "published. At 1,550 nm only cumulative thresholds have been measured (Bi et al., 2,500 to $2\\times10^6$ pulses "
    "per site); the single-pulse threshold, which governs handheld and moving cameras, is unknown. The pulse energies "
    "of Seyond's Falcon and Luminar's Iris are not public, the 1,550 nm transmission of the damaged phones' "
    "infrared-cut filters was not reported, and the estimate ignores any attenuation by the windshield in front of a "
    "car camera. The estimate's 2 µJ per pulse is therefore an assumption, and for the single-shot regime it can "
    "state only the threshold factor at which damage would begin at each distance, not a damage distance.")
iec = line_starting("- **IEC 60825-1 (the laser eye-safety standard):**")
applied = [l for l in T.split("\n") if l.startswith("- **Camera damage by lidar (§C4c subsection 1).**")]
if applied:
    a1_name = "appendix1_wording.json"
    appendix1 = [edit("K4-A1-camera-damage-wording", applied[0], A1_ITEM)] if applied[0] != A1_ITEM else []
else:
    a1_name = "appendix1_pair.json"
    appendix1 = [edit("K3-A1-camera-damage", iec, iec + "\n" + A1_ITEM)]

for name, lst in (("edits.json", edits), (a1_name, appendix1)):
    out = HERE / name
    assert not out.exists() or "--force" in sys.argv, f"{name} exists; pass --force"
    data = json.dumps({"block": "camera_damage_2026-10", "edits": lst, "skipped": []}, ensure_ascii=False, indent=1)
    out.write_bytes((data + "\n").encode("utf-8"))
    print(name, len(lst), "edits")
