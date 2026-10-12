# Automotive Night Vision, Lidar and the Sensor Debate
## Technology routes, markets, supply chain, geopolitics and outlook: status as of 27 September 2026

*This is an earlier draft, kept for reference. Where it differs from the current report, the report takes precedence.*

---

### How to read this report

**Scope.** This report started from one question: did car makers ever sell thermal night vision as a factory option? It then widens to:

- lidar vs thermal;
- lidar outside China;
- FMCW and beam steering;
- company-by-company lidar technology routes;
- SPAD receiver chips;
- supply chain and geopolitics;
- whether camera-only or camera+radar driving can reach full autonomy.

It ends with explicit projections.

**Method.** Web research using primary filings (SEC, HKEX, NHTSA, NTSB, court opinions, government registers), company press releases, datasheets and manuals, teardown summaries (TechInsights, Yole/System Plus, NE Times), analyst releases (Yole, Gasgoo, ResearchInChina, IIHS, USGS) and trade press. Paywalled full reports were not accessible: Yole/TechInsights PDFs, Automotive News, Politico Pro, IEEE Xplore full texts.

**Evidence tags used in tables and bullets.**

| Tag | Meaning |
|---|---|
| **[P]** | Primary document: company filing, datasheet, press release or regulator record. A company claim is *primary* but not *independent*. |
| **[I]** | Independent: regulator finding, court, academic paper, test body, independent analyst, or a journalist's own count. |
| **[T]** | Trade press, or an analyst figure relayed by press. |
| **[E]** | My own estimate or calculation. Assumptions are stated. |
| **[U]** | Unverified. Treat as a lead, not a fact. |

Where sources conflict, both values are given.

**Amendment log.** 27 Sep 2026 (later the same day): added §A6 on headlights (what "better headlights" can and cannot do); updated the Rivian R2 lidar-supplier reporting (§B2, Appendix 1); added a Fastree3D history timeline (§C5); added the related sources. Then a **gap-filling pass**, ended early: updated take-rate data (Volvo, Mercedes, Cadillac), the estimate of Chinese-brand lidar exports, the thermal annual volume, supplier identities (GM, Nissan, Lucid, Ford, Aurora), specs (Hesai ETX and Picasso, Huawei 192- and 896-line, Seyond Robin E1X read directly from its datasheet), SPAD foundry status, Hesai ATX parts and the Hesai/RoboSense Southeast Asia plants. Items not covered are listed in Appendix 1. Finally, added **Part G**, which re-examines the report's strongest editorial judgements, and softened the overstated lines in §B2, §B3, §D6, §F2 and §F4 to match. Then **expanded the terse sections**: Part F projections (reasoning, assumptions and what would change each call), §D2 effects, §D5 and §D6. Added **§B6** on Western brands in China. Also added **§C4b**, comparing SiPM and SPAD-array receivers, and **§C6(d′)** on how sunlight blinding is mitigated. Two numbers were corrected in the process: FMCW's 2030 share (0.5–2% → 0.1–0.5% of units) and the AV-vs-passenger lidar value comparison (now "about equal in 2026–28", not "AV exceeds").

---

## 0. Executive summary

1. **Thermal night vision has been on sale from car makers since 2000, but has never been widely adopted.**
   - Cadillac pioneered it (DeVille, 2000–04). BMW, Audi, Porsche, VW, GM, Stellantis, Bentley and Rolls-Royce still offer it; Mercedes (near-infrared) and Lexus dropped out.
   - The dominant supplier (Magna, ex-Veoneer/Autoliv, about 98% share) reports **about 1.2 M systems on the road after roughly 20 years**. That is about **0.08% of cars built**.
   - China is now the growth market: 19k units in Jan–Sep 2025, up 385% year on year, but still about 0.1% of Chinese sales.
   - **Why it stayed niche:** glass is opaque in the thermal band, so the camera must sit exposed in the grille; resolution is low; the display is poorly placed for the driver; the option cost \$2–3k; and headlight automation (auto high beam, adaptive driving beam) plus camera AEB eroded part of the benefit.
   - **Headlights have a hard, glare-imposed ceiling on the low beam** (the cutoff reaches the road at about 50–100 m). The biggest improvement lever is getting high-beam-level light onto the road more of the time *without relying on the driver*: automatic switching and adaptive driving beam (ADB). ADB is common in Europe and China but effectively absent in the US (only Rivian certified as of 2025). See §A6.
2. **Lidar is eating thermal's "extra sensor" budget, especially in China.** China installed **3.21 M lidars in passenger cars in 2025** (about 18–21% penetration by year-end), roughly 100× the thermal volume.
   - Lidar covers many functions: highway and urban assisted driving, AEB, L3.
   - It is **not** a full substitute for thermal. Lidar gets only sparse points on small objects at range and cannot tell whether something is alive; thermal does better in haze. The top Chinese flagships (Yangwang U8L, Zeekr 9X) carry both.
3. **Outside China, lidar in passenger cars is roughly as niche as thermal. 2026 is a trough.**
   - **Western exits since late 2025:**
     - Volvo permanently shelved lidar functions on the EX90/ES90. The lidar was never activated for any feature, and Volvo is paying owners \$1.5–1.9k in compensation.
     - BMW dropped its €6k L3 option; its R&D chief said demand "was not at a stage where we could be profitable".
     - Mercedes paused Drive Pilot. The 2027 S-Class/EQS US releases list no lidar.
     - Stellantis shelved its L3 program.
     - Luminar filed Chapter 11 and its lidar business sold for **\$33 M**.
   - **My bottom-up estimate:** about 45–140k passenger-car lidars in cars sold outside China in 2025, about 0.1–0.2% of non-China production. That is the same order of magnitude as OEM thermal night vision (about 50–100k per year).
   - **Robotaxis and trucks outside China add about 30k lidars in 2026.** About half are Waymo's in-house units.
4. **A Western restart is scheduled for 2027–28, tied to eyes-off L3:**
   - Rivian R2 Gen 3 (from end-2026);
   - Nissan next-generation ProPILOT with Wayve (FY2027);
   - Mercedes' next L3 **with Hesai lidar built in Thailand**;
   - GM Escalade IQ eyes-off (2028);
   - an Aeva FMCW win at an unnamed top-10 European OEM (SOP 2028).
5. **The winning technology route is 905/940 nm pulsed direct ToF.** It uses silicon SiPM or SPAD receivers, multi-junction VCSEL (or EEL) line arrays, **one mechanical scan axis**, and solid-state flash units for blind spots.
   - **1550 nm** has shrunk to about 4–6% of Chinese units (Seyond/NIO) plus trucks and defense.
   - **FMCW** has **no passenger-car series production**. Its only commercial foothold is heavy trucks: Aurora (about 25 driverless trucks, targeting 200 by year-end 2026) and Aeva with Daimler Truck (2027).
   - **No optical phased array (OPA) is in series production.** Attrition has been heavy: Mobileye's FMCW, Scantinel, Baraja, Quanergy, Luminar.
6. **SPAD-SoC receivers have scaled fast along one axis.**
   - PDE went from 24% at 905 nm (Sony IMX459, 2021) to 37% at 940 nm (IMX479, 2025) to more than 40% (Hesai Picasso, 2026).
   - Channel counts went 128 → 520 → 2,160 → 4,320.
   - **Fully solid-state, long-range, wide-field lidar is blocked** by receiver étendue (aperture), silicon area, histogram memory and background-driven avalanche power. Shipping solid-state sensors cluster at $R_{10\%}^2\cdot\text{FOV}\approx10^7$ m²·deg², against about $10^8$ for one-axis-scanned units.
   - **The missing component is a large-aperture, non-mechanical receive-side beam steerer.** That problem sits squarely in beam-steering research.
7. **Chinese lidar makers' SPAD SoCs are a mix.** There is no evidence of relabeled Sony dies:
   - **open use of Sony parts** in products described as SPAD-SoCs: Huawei 96- and 192-line (IMX459 geometry), and very likely the RoboSense EM4-520 (IMX479);
   - **separate designs:** RoboSense E1 (9.8 µm pitch, no Sony match), Hesai's Fastree3D-derived chips, RoboSense Phoenix (28 nm, 2160×1900), Hesai Picasso, Adaps.
   - No foundry is publicly identified for any of them.
8. **Supply chain.**
   - In the 2022 Hesai AT128, **72% of component value was US-sourced**: a Lumentum VCSEL, an onsemi SiPM, and a Xilinx FPGA that alone was 33% of cost. Hesai now designs all seven core blocks in-house, and no single supplier exceeds 4.6% of its purchases.
   - **Remaining dependence on Western and Japanese suppliers:** Sony SPADs, FPGAs (being designed out), TI/Infineon analog parts, and latent foundry/EDA access.
   - **Inputs mainly sourced from China:** Ga (98%), Ge (77%), In (68%), GaAs/InP substrate export permits, and rare-earth magnets. Suspensions of China's controls expire on **10 and 27 Nov 2026**.
9. **Geopolitics.**
   - Hesai and RoboSense are on the US DoD 1260H list. DoD may not buy Chinese lidar from 30 Jun 2026.
   - The BIS connected-vehicle rule **excludes lidar**.
   - Pending bills would ban Chinese lidar in US vehicles: Connected Vehicle Security Act S.4429, which passed Senate Commerce unanimously on 22 Jul 2026, and the SAFE LiDAR Act.
   - Chinese lidar now pays about 37.5% Section 301 tariffs plus MFN duty.
   - Most merchant robotaxi and truck lidar in the US is Hesai.
10. **Camera-only vs multimodal.**
    - **Physics:** camera depth error grows as $Z^2$, radar angle is diffraction-limited, and lidar is sparse at range.
    - **Benchmarks:** camera-only is within about 3 NDS of lidar on short-range benchmarks, but far behind beyond 50 m (Waymo Open: 20.5 vs 58.4 AP).
    - **Weather:** in fog, lidar and cameras fail together; radar is the orthogonal channel.
    - **Outcome evidence at scale exists only for lidar-equipped L4.** Waymo: 271 M rider-only miles; the independent IIHS study found −68% crashes per mile. Tesla's roughly 1 M unsupervised miles cannot support statistical claims.
    - **Industry behaviour:** every announced production eyes-off or driverless program uses lidar, except Tesla (and Xpeng's robotaxi). Almost every Western L2++ product now ships **without** lidar.
11. **My headline projections** (details and confidence levels in §F):
    - China lidar reaches about 50–60% of new cars at ¥100k and above by 2030.
    - Western passenger-car lidar reaches about 1–3% of new cars by 2030, driven by eyes-off L3 and dependent on US policy toward Chinese suppliers.
    - 905/940 nm dToF holds about 85–92% of units in 2030; FMCW about 0.1–0.5% of units (≈20–100k, larger by value), mostly trucks and a few L3 programs.
    - Western brands face strong pressure to offer lidar **in China** (about 70% chance that most of their ¥150k+ NEV models offer it by 2028), and meet it with Chinese stacks. That makes them large lidar buyers for China-built cars while their home programs retreat (§B6).
    - OPA automotive series production before 2030: about 10–15% probability.
    - Thermal stays below 0.5% of global production unless night-AEB testing forces it.
    - Lidar-based fleets keep more than 85% of global driverless miles through 2028.

---

# Part A — Thermal night vision

## A1. OEM history

| Year | OEM / model | Type | Supplier / notes |
|---|---|---|---|
| 2000–04 | Cadillac DeVille | FIR (passive thermal) | Raytheon; grille camera; image on windshield HUD; **\$2,250 option**; reportedly about 7,000 buyers in MY2000 (Cadillac had expected about 2,000), falling to about 600 in MY2004 and 145 on 2005 models before it was dropped in Sep 2004 (Automotive News, 15 Nov 2004, via a forum repost; original paywalled) [T] |
| 2002 | Toyota Land Cruiser Cygnus / Lexus LX470 | Active near-IR (NIR) | First active system; HUD |
| 2004 | Honda Legend (Japan) | FIR | First with pedestrian detection |
| 2005 | BMW 7 Series (E65) | FIR | Autoliv with FLIR core; pedestrian detection 2008; animal detection and "Dynamic Light Spot" 2013 |
| 2005/06 | Mercedes S-Class W221 Night View Assist | Active NIR | Pedestrian detection 2009; spotlight 2011; animal detection 2013; **not offered on W223 (2021→)** |
| 2010 | Audi A8 (D4) Night Vision Assistant | FIR | Later flashes matrix-LED "marker lights" at pedestrians |
| 2016–20 | Cadillac CT6 | FIR | Autoliv; later Escalade and other Cadillacs |
| 2017–20 | DS 7; Peugeot 508, 3008, 5008 | FIR | The only real push below luxury pricing |
| various | Porsche (Cayenne, Panamera, Taycan), VW Touareg, Bentley, Rolls-Royce | FIR | Mostly Veoneer/Magna |
| 2025–26 | Fangchengbao Bao 8, Yangwang U8L, Zeekr 9X, M-Hero 817/917, HiPhi HL, Cadillac XT5 (China) | FIR | Mostly **Raytron** (about 74% China share, Jan–Sep 2025); Zeekr 9X claims the "world's first thermal AEB" (Raytron 640×512) |

## A2. Adoption numbers

- **Magna (2024):** more than **1.2 M systems on the road**, 40+ models, 13 automakers, about **98% share** [P].
  - Assume about 1.5 B light vehicles built worldwide since 2005 [E].
  - Penetration is then about $1.2\times10^6/1.5\times10^9\approx0.08\%$, roughly 1 car in 1,300 [E].
- **China:** 19,000 installs in Jan–Sep 2025, **+384.7% year on year** [T].
  - 90.5% were SUVs; the largest price band was ¥400–500k.
  - Raytron held 73.8% and Xuanyuan IDrive 15.5%.
  - The report projects 146,000 units per year by 2030 [T].
- **Yole:** automotive thermal camera revenue of about **\$285 M by 2030**, against automotive lidar at about **\$3.6–3.8 B** [T].
  - The whole thermal imaging market was more than \$7 B in 2024, and 60% of thermal sensors were Chinese-made [T]. Thermal's problem is not wafer scale.
- **Forecast inconsistent with unit volumes.** One market-research firm puts "automotive night vision" at \$3.5 B in 2025.
  - Even 100k systems at \$1,000 is \$0.1 B, so the figure is inconsistent with unit volumes [E].
  - Such figures should be checked against unit volumes.

## A3. Why it stayed niche: physics and engineering

**1. Glass is opaque in the thermal band (8–14 µm).**
- Silica absorbs strongly near 9–10 µm (Si–O vibrational absorption).
- The camera therefore sits in the grille or bumper behind a Ge, chalcogenide or ZnS window, with a heater and sometimes a washer, exposed to stone chips and crash damage.
- NIR systems (Mercedes, Toyota) avoided this because a silicon camera works through glass. The price was losing thermal contrast.
- The same rule applies to aftermarket thermal cameras mounted on the dashboard: behind the windshield they see nothing.

**2. Resolution.**
- Take a 320×240 sensor over a 24° field (typical of the aftermarket FLIR PathFindIR II, which listed at \$3,200 plus \$800 for detection):

$$\text{IFOV}=\frac{24^\circ\cdot\pi/180}{320}\approx1.31\ \text{mrad}$$

- A pedestrian has a characteristic size of about $d_c=\sqrt{1.8\times0.5}\approx0.95$ m.
- Johnson/NVESD criteria: detection needs about 0.75 cycles (about 1.5 px) across the target; recognition about 3 cycles (about 6 px).

$$R_\text{det}\approx\frac{0.95}{1.5\times1.31\times10^{-3}}\approx480\ \text{m},\qquad R_\text{rec}\approx\frac{0.95}{6\times1.31\times10^{-3}}\approx120\ \text{m}$$

- So a thermal camera sees a warm blob far away but only says "person" at about 100–120 m. Vendor claims match this: Yangwang U8L 120 m for moving objects and 300 m maximum.

**3. Where it helps.**
- At 100 km/h, stopping distance is about $27.8\times1.5+27.8^2/(2\times0.7g)\approx98$ m.
- The low beam's useful reach for dark, low-contrast targets is set by its glare cutoff: roughly 50–80 m on the driver's own side, much less on the oncoming side (§A6). In a closed-road study, pedestrians in dark clothing under low beams were recognized on only about 40% of trials without glare and about 5% with glare (Wood et al.) [I]. Thermal is therefore valuable on unlit rural roads and highways, where many night pedestrian deaths occur.
- It adds little in lit urban areas. Cadillac cited limited usefulness in urban and suburban driving when it dropped the option.

**4. The display is poorly placed.**
- A grey video in the cluster pulls the driver's eyes off the road.
- The industry moved to alert-only designs (spotlights, marker lights), which effectively turns the product into a detector.

**5. Thermal crossover.** On hot nights, pavement is near skin or clothing temperature and contrast collapses.

**6. Cost, validation and export controls.**
- The option cost \$2–3k, with expensive optics.
- It was a single-function sensor, and no ASIL-rated thermal camera existed until the Valeo + Teledyne FLIR ASIL-B program (first contract late 2023).
- Uncooled microbolometers above 9 Hz are dual-use controlled (ECCN 6A003.b.4.b). Vehicle-integrated cameras are decontrolled under Note 3.b.4.c if built into civilian passenger vehicles.

## A4. What could change it

**Regulation**
- **FMVSS 127** requires pedestrian AEB in darkness by **1 Sep 2029**.
  - The Alliance appealed; the case is held in abeyance.
  - **On 23 Mar 2026 DOT announced a rulemaking to extend compliance by two years (to about 2031)** [T, Nelson Mullins, Apr 2026].
- **Euro NCAP 2026 and C-NCAP 2027** expand night, rain and fog scenarios.
- **IIHS (2022):** pedestrian AEB cut pedestrian crashes by **27% in daylight, but had about zero effect on unlit roads at night** [I]. This leaves a real gap for some sensor to fill.

**Market and technology**
- **Thermal as an AEB input rather than a display:** Zeekr 9X (Raytron); Valeo + Teledyne FLIR ASIL-B ("leading global OEM", late 2023); Magna fifth generation (late 2025, shrinking from golf-ball to sugar-cube size).
- **Cheaper Chinese sensors and optics:** Raytron, Guide, 8 µm pixels.
  - At fixed IFOV and f-number, lens area scales as $p^2$.
  - Going from 17 µm to 8 µm pixels cuts it to about $(8/17)^2\approx0.22$ [E].

**Headwind: germanium**
- China holds 77% of refined Ge output [I, USGS MCS 2026].
- Chinese Ge metal exports in Jan–Sep fell from 36,656 kg (2023) to 18,787 kg (2024) to 7,520 kg (2025).
- European Ge prices rose from about \$3,150/kg to \$5,380/kg during 2025 [I, USGS].
- Chalcogenide glass (e.g. LightPath "BlackDiamond", Ge-free) is the escape route.
- Chinese thermal makers buy optics domestically. Western ones face permit friction.

## A5. Lidar vs thermal: complementary, not identical

**1. Samples on target.**
- At 0.1°×0.1° lidar sampling (1.75 mrad), a 0.5×1.8 m pedestrian gets about **30 points at 100 m and about 7 at 200 m**.
- At 0.05°, about 112 and 28 points [E].
- Thermal has a similar pixel count, but the person is usually the hottest object, so segmentation is trivial and it answers "is it alive?".

**2. Dark clothing.**
- Lidar returned power for an extended Lambertian target is $P_r\propto\rho A_rT^2/(\pi R^2)$, so $R_\text{max}\propto\sqrt{\rho}$.
- Going from white ($\rho\approx0.8$) to dark ($\rho\approx0.1$) cuts range to about $0.35\times$.
- Thermal ignores visible colour (it depends on temperature and emissivity).

**3. Fog.**
- Lidar pays extinction twice: $T^2=e^{-2\alpha R}$, versus thermal's one-way path. Lidar also gets near-field backscatter clutter.
- **Size parameter** $x=2\pi r/\lambda$:
  - at 905 nm, fine fog droplets ($r\approx2$ µm) give $x\approx14$ and $Q_\text{ext}\approx2$;
  - at 10 µm, $x\approx1.3$, well below the peak.
  - So **LWIR has a real advantage in haze and fine-droplet fog**, which **largely vanishes in thick fog with large droplets** ($r\gtrsim10$ µm) and in rain or snow.
- **Water film** on the thermal window is opaque: absorption length at 10 µm is about 10–20 µm.
- **Measured:** lidar reach collapses to about 0.6× meteorological visibility $V$ (below 25 m when $V<40$ m, Bijelic et al., IV 2018), and **1550 nm is not better than 905 nm in fog** (Kutila et al., ITSC 2018) [I].

## A6. Headlights: what "better headlights" can and cannot do

**Short answer.** The low beam has a hard, glare-imposed ceiling. "Better headlights" help in three ways:
1. getting real-world low beams closer to that ceiling (pattern, aim, leveling, curve lighting);
2. **delivering high-beam-level light more of the time without relying on the driver** (automatic high beam; adaptive driving beam, ADB);
3. aiming light at hazards that sensors have already detected (marking or spot lights).

Lever 2 is by far the largest, so "use the high beam more, automatically" is a fair one-line summary. Levers 1 and 3 are real but bounded.

### A6.1 Why the low beam has a hard limit

**Design goal.** Light the road without dazzling oncoming drivers. The low beam is therefore a sharp horizontal **cutoff** aimed slightly below horizontal.
- Above the cutoff, intensity is capped at a few hundred candela. Example: the ECE glare point B50L (the oncoming driver's eye at 50 m) must stay within 50–350 cd [T].
- Just below the cutoff sits the "hotspot", typically tens of thousands of cd.
- ECE beams raise the cutoff (a 15° kink) on the kerb side to reach farther on the driver's side. The oncoming side stays flat and low.

**Geometry** [E]. With mounting height $h$ and downward aim $a$, the cutoff reaches the road at

$$d=\frac{h}{\tan a}$$

For $h=0.65$ m:

| Downward aim | 0.25° | 0.38° | 0.57° (≈1% down) | 0.76° | 1.0° |
|---|---|---|---|---|---|
| Cutoff meets road at | 149 m | 98 m | 65 m | 49 m | 37 m |

- Beyond $d$, a standing pedestrian's whole body lies above the cutoff. At 100 m with a 0.57° aim, the cutoff line is 0.34 m **below** the road surface. The pedestrian is then lit only by the glare-limited part of the beam.

**Photometry** [E]. Illuminance falls as $E=I/R^2$. IIHS scores visibility as the distance at which 5 lux reaches a point 25 cm above the lane edge; 3 lux is a common criterion for low-contrast objects [P, IIHS].

| Intensity toward the target | 5 lux reached at | 3 lux reached at | 1 lux reached at |
|---|---|---|---|
| 350 cd (glare-limited zone) | 8 m | 11 m | 19 m |
| 20,000 cd (typical low-beam hotspot) | 63 m | 82 m | 141 m |
| 40,000 cd (strong hotspot) | 89 m | 115 m | 200 m |
| 150,000 cd (two US-max high beams) | 173 m | 224 m | 387 m |
| 430,000 cd (ECE-class high beam, [U]) | 293 m | 379 m | 656 m |

**Target luminance** [E]. A dark pedestrian ($\rho\approx0.05$–0.1) at 5 lux has $L=\rho E/\pi\approx0.08$–0.16 cd/m², which is mesopic vision. In the glare-limited zone (0.14 lux at 50 m), $L\approx0.002$–0.004 cd/m², effectively invisible.

**Oncoming glare makes it worse** [E].
- Two opposing low beams at 50 m put about 0.28 lux at the driver's eye, about 3.4° off-axis.
- Stiles–Holladay gives a veiling luminance of about $10E/\theta^2\approx0.24$ cd/m², **larger than the dark pedestrian's own luminance**.
- This matches measurement: in a closed-road study, dark-clad pedestrians under low beams were recognized on only about 40% of trials without glare and about 5% with glare (Wood et al.) [I].

**Stopping distance** (1.5 s reaction, 0.7 g) [E]:

| Speed | 50 km/h | 80 km/h | 100 km/h | 130 km/h |
|---|---|---|---|---|
| Stopping distance | 35 m | 69 m | 98 m | 149 m |

- The low beam's usable reach for low-contrast targets is about 50–80 m, set by cutoff geometry and glare. That is **shorter than stopping distance above roughly 70–80 km/h** ("overdriving the low beams").
- No amount of LED brightness fixes this. The constraint is the intensity allowed in the glare-sensitive angular region, not total lumens.

**Aim sensitivity.** This is the same $Z^2/h$ geometry as monocular camera depth.
- SAE J599 allows a vertical aim of 0 ± 0.76° (below 90 cm mounting height) [P, via IIHS].
- IIHS measured factory aims on new cars between about −0.5° and +0.4° [I].
- IIHS notes that a 0.25° downward aim already drops the cutoff below its 25 cm sensor beyond 100 m.
- So production aim, load, and pitch leveling are first-order variables, not details.

### A6.2 What improves within the low-beam limit

- **Pattern quality:** a sharper, flatter cutoff with more intensity just below it, and wider spread for road edges and curves (LED projectors, better optics).
- **Aim and leveling:** tighter factory aim; automatic and dynamic leveling for load and braking pitch.
- **Curve and bending light (AFS)** and cornering lamps.
- **Evidence:** against poor-rated headlights, IIHS "good" ratings are associated with:
  - a **19% lower nighttime single-vehicle crash rate**;
  - **23% fewer pedestrian crashes**;
  - **29% fewer driver-injury crashes**
  - (about 44,000 crashes, 187 vehicles) [I].
- **Caveat:** the IIHS rating also gives credit for automatic high-beam switching, so part of this benefit is lever 2.

### A6.3 The big lever: high-beam light, more of the time

**The high beam has no cutoff.**
- The US caps it at 75,000 cd per lamp at H-V [P, FMVSS 108].
- ECE permits more. The per-vehicle total was historically 225,000 cd, and later amendments reportedly allow about 430,000 cd [U; check the current UN R149/R112 text].
- BMW's laser boost claims about 600 m of high-beam range [P].
- High-beam reach comfortably exceeds stopping distance at highway speeds.
- **Measured:** switching from low to high beam raised mean pedestrian recognition distance from 59 m to 94 m, and up to 3.5× for dark clothing (Wood/Tyrrell studies) [I].

**Drivers seldom use it.**
- UMTRI naturalistic data: high beams were on for **3.1% of night driving distance**, and only **25.4%** even on unlit rural roads with no other traffic [I].
- Other studies find about 50% under ideal conditions [I, cited by IIHS].
- So the binding constraint is **behavioural and social** (glare to others), not photometric.

**The engineering answers are automation, not persuasion:**
1. **Automatic high-beam switching.** A camera detects other vehicles' lamps and toggles the beam. This removes the behavioural part.
2. **Adaptive driving beam (ADB, matrix or pixel "glare-free high beam").** It keeps high-beam intensity everywhere except dark "tunnels" around detected vehicles. This removes most of the glare constraint.
   - **Europe and China:** widespread since about 2013 (Audi Matrix LED, Mercedes Multibeam and Digital Light, BMW Selective Beam, and many Chinese makers).
   - **United States:** legalized by NHTSA in **Feb 2022** (FMVSS 108 amendment), but the vehicle-level track test is stricter than global practice.
     - It requires a 1° transition zone, against about 4° elsewhere.
     - Component minimums conflict with track-test maximums in right curves.
     - NHTSA **denied all 12 petitions for reconsideration** on 30 Dec 2024 [P].
     - As of 2025, **Rivian was the only automaker offering fully compliant ADB in the US** [T].
     - In practice, most US cars still switch between low and high beam.
3. **Sensor-directed marking or spot light.** Light is aimed at detected pedestrians or animals: BMW Dynamic Light Spot (with thermal), Audi marker lights, and pixel/DMD headlights that can also project lane markings.

### A6.4 Limits that remain even with perfect ADB

- **Traffic.** ADB carves light away near every other road user. A pedestrian beside or just behind an oncoming car can fall in or near the shadow, and dense traffic pushes ADB back toward low-beam behaviour. ADB also needs a camera to detect lamps at hundreds of metres, with some latency and transition zones.
- **Oncoming glare** still cuts the driver's contrast sensitivity (veiling luminance).
- **Target reflectance.** The pedestrian's own luminance is set by $\rho$ (dark clothing ≈ 5%).
- **Weather.** High beams are *worse* in fog and snow because of backscatter into the driver's eyes, and wet roads reflect light away specularly.
- **Photometry.** $E\propto1/R^2$, so doubling reach needs 4× intensity in that direction.
- **Human factors.** Reaction time, attention and age: in Wood et al., older drivers under low beam failed to recognize black-clad pedestrians at all (mean recognition distance 0 m) [I].
- **Glare complaints.** LED and SUV glare complaints are rising, although an IIHS analysis (2025) found crashes have not increased because of glare [T].

### A6.5 Why this matters for the sensor debate

- **Camera AEB is also headlight-limited.** IIHS night pedestrian-AEB ratings fell from superior to advanced with high beams, and to basic with low beams (§E6).
  - So auto high beam and ADB directly raise camera-AEB performance at night.
  - That is the sense in which headlights eroded part of thermal's (and lidar's) night value.
- **The ceiling is real, though.** Low-beam geometry (about 50–80 m for dark targets), shadowed zones in traffic, and fog leave a residual gap.
  - Lidar, radar and thermal do not depend on headlights at all.
  - That gap is exactly where FMVSS 127's dark low-beam test, Euro NCAP 2026 and C-NCAP 2027 apply pressure.
- **US-specific corollary.** With ADB effectively absent, US cars are more low-beam-limited than European or Chinese cars. That slightly strengthens the case for active or thermal night sensing in the US market.

---

# Part B — Lidar markets: China vs outside China

## B1. Global and China numbers

**Global (Yole)** [T]

| Year | Market | Units | Leaders / notes |
|---|---|---|---|
| 2023 | \$538 M | — | Hesai 37%, RoboSense 21%, Seyond 19%, Valeo 10% (revenue) |
| 2024 | \$859 M | 1.6 M | Hesai 33%, RoboSense 24%, Huawei 19%; Chinese suppliers **93%** of passenger cars; passenger-car sales more than 4× robotaxi |
| 2025 | **>\$1 B (+60%)** | **3.7 M passenger-car units** (about 3.1 M long-range ADAS) | Chinese suppliers **about 95%**; Hesai 43% of long-range ADAS volume |
| Forecast | \$3.56–3.8 B by 2030 (24–28% CAGR) | — | Yole had **cut** earlier forecasts (\$4.5 B by 2028 → \$3.6 B by 2029) because prices fell faster than expected |

- ASP (Yole 2024): China \$450–500 vs rest of world \$700–1,000.
- Implied 2025 blended ASP: about \$270 [E].
- Yole's 2024 robotaxi lidar market: \$166 M, with Hesai at 61% share [T].

**China installations** [T]
- 2024: 1.529 M (6.0% penetration).
- 2025: **3.21 M** in total, or 2.756 M main lidars; about **21% of NEVs**; 18.5% of new cars in Dec 2025; 21.4% in May 2026.
- Q1 2026: 985k (Hesai 34.9%, Huawei 32.3%, Seyond 16.8%, RoboSense 11.0%).
- 2025 by Gasgoo, including blind-spot units: Huawei 41.5%, Hesai 33.8%, RoboSense 17.0%, Seyond 7.7%.
- Lidar has reached about **¥80–90k cars**: Leapmotor A05 at ¥85,900; BYD Seagull God's Eye B at ¥90,900.
- BYD made lidar optional on **every model for ¥12,000** from May 2026.

**Company volumes** [P unless noted]

| Company | 2024 | 2025 | H1 2026 | Other |
|---|---|---|---|---|
| Hesai | 501,889 | **1,620,406** (ADAS 1,381,133; robotics 239,273) | 1.10 M | FY25 revenue RMB 3.03 B; gross margin 41.8%; first profit (RMB 436 M). 2026 target 3.0–3.5 M. Q2 2026 revenue per unit about RMB 1.37k (about \$200) [E] |
| RoboSense | 544,200 | about 912k (ADAS about 609k) | 719,200 | Q1 2026 ASP RMB 1,336 (−52% year on year) [T]; first quarterly profit Q4 2025 |
| Seyond | about 230k | 332.5k (Robin 137.8k) | 450.9k | NIO about 86–92% of revenue; Falcon (1550 nm) ASP about \$704 (2024) [T] |
| Huawei | n/d | 41.5% China share | n/d | Also 3–5 blind-spot units per flagship car |

## B2. Western passenger-car programs: status in September 2026

| OEM / program | Lidar (supplier) | Status | Stated reason / notes |
|---|---|---|---|
| **Volvo EX90 / ES90** | Luminar Iris, roof, standard from 2024 | **Lidar functions never activated.** Not standard from Apr 2026; contract terminated 14 Nov 2025; lidar functions **permanently discontinued** Jul 2026. Compensation: NOK 18k / SEK 16k / €1.5k / C\$2k / about \$1.5k in packages | Volvo cited "supply chain risk" and Luminar's failure to meet its obligations; cars safe "with or without a lidar" [P/T]. EX90 US sales 2025: 3,913 [P]. **Global EX90 production:** 1,806 (2024) + 16,311 (2025), about 18.1k in total, per Volvo data compiled by the Volvo Owners Club [I]. So roughly **15–20k EX90s carry lidar hardware** [E]. Luminar's filings say Volvo, which had once agreed to 1.1 M lifetime sensors, bought fewer than 10k. The two figures don't reconcile cleanly, possibly because of different cut-off dates [P/E] |
| **Polestar 3** | Luminar option | Dropped [T] | — |
| **Mercedes Drive Pilot (L3)** | Valeo SCALA 2 | **Paused Jan 2026.** 2027 S-Class/EQS US releases list 10 cameras, 5 radars, 12 ultrasonics, **no lidar** [P] | "Middling demand and high production costs"; also "the unit numbers do not match the system costs". The spokesperson said lidar was needed to compensate for camera limits in glare and low light [T]. **No uptake figure was ever published.** The one data point: in Apr 2024, 65 L3-equipped Mercedes were for sale in California and 1 had been sold (Fortune) [T]. Price was €5,950–9,000 in Europe or \$2,500 per year in the US |
| **Mercedes MB.DRIVE ASSIST PRO** (L2++) | none | CLA/C/GLA/S: 10 cameras, 5 radars, 12 ultrasonics; NVIDIA (Momenta in China) [P] | Cheaper, broader use |
| **Mercedes next L3** (≤130 km/h) | **Hesai** (Picasso family per optics.org), built in the Thailand plant | Confirmed supplier for Europe and China, May 2026. Model and SOP not disclosed; "within 2–3 years". Reuters (Mar 2025) reported an exclusive multi-year deal through 2030 [P/T] | Needs fully redundant steering, braking and power on top of the L2++ hardware. L4 planned for the next-generation S-Class from about 2028. **Customer 2026/27 S-Class cars appear to carry no lidar in any market**; the roof-lidar cars shown are robotaxi prototypes [T] |
| **BMW Personal Pilot L3** | Lidar (InnovizOne widely reported [U]) | **Dropped** with 7 Series facelift (Apr 2026); €6,000 (or €5,110) option | "Demand … was not at a stage where we could be profitable" (Joachim Post) [P]. iX3 L2 (€1,450) has no lidar |
| **Stellantis STLA AutoDrive L3** | Valeo SCALA 3 | **Shelved Aug 2025** [T] | Cost, technical hurdles, demand |
| **Audi A8** | Valeo SCALA 1 (2017) | L3 never activated [U] | — |
| **Honda Legend** | Valeo | 100 lease units (2021) [T] | — |
| **Lexus LS / Mirai Advanced Drive** | Denso | Japan, small volume [T] | — |
| **Lucid Air / Gravity** | 1 forward lidar on DreamDrive Pro: Gravity has 14 cameras, 1 lidar, 5 radars, 12 ultrasonics (NVIDIA blog) and the option costs \$6,750. **Supplier undisclosed by Lucid**; RoboSense (M1-class, 905 nm) reported for the Air [T] | In production; take-rate undisclosed | Lucid–Nuro–Uber robotaxi uses "solid-state lidar sensors" in the body and roof halo, count and supplier undisclosed. About 100 test vehicles; at least 20k over 6 years [P] |
| **Rivian R2 Gen 3** | 1 forward lidar, about 900 ft; **supplier undisclosed**. EV (eletric-vehicles.com) reported RoboSense as the supplier; **Rivian denies it** [T] | From end-2026. Launch R2s have no lidar and cannot be retrofitted [P/T] | Scaringe: "a really great sensor that can do things that cameras can't". In his view, all realistic options at low hundreds of dollars come from China. He told Reuters Rivian is weighing building lidar in the US with Chinese technology, possibly via a joint venture; the CFO later said there are "no plans today" to bring lidar in-house [T]. Lidar cars also serve as ground truth for camera training |
| **Nissan next-gen ProPILOT** (with Wayve) | **1 roof-mounted** next-gen lidar ("Ground Truth Perception"), plus 11 cameras and 5 radars; **supplier undisclosed**. The 2022 demo used **Luminar**, whose lidar business is now MicroVision's. MicroVision's CEO would not comment on individual customers and said "every Luminar customer is engaged with us" [P/T] | FY2027, Japan first [P] | Range at high speed and at night |
| **GM eyes-off, Escalade IQ** | lidar + radar + cameras; **supplier, count and placement undisclosed**. No published report names a vendor [P/T] | "As early as 2028"; more than 200 development vehicles [P] | "Better with multiple modes of sensing, period" (Sterling Anderson) [T] |
| **GM Super Cruise** | none onboard (lidar-mapped HD maps) | 1 B hands-free miles; about 750k equipped [P] | — |
| **Ford BlueCruise; 2028 eyes-off** | none today; **L3 sensors undisclosed**. Reports conflict on whether it will use lidar. One outlet's "in-house lidar development" claim is unverified; the only Ford in-house lidar found was Argo AI's, and Argo shut down in 2022 [T/U] | 1.2 M equipped [P] | NTSB (Mar 2026): stationary vehicles at night "likely outside the capabilities" [I] |
| **Aeva, top-10 European OEM, L3** | Aeva Atlas Ultra (**FMCW**) | SOP 2028; OEM unnamed [P] | Exclusive outside China |
| **Hesai, "another top European OEM"** | ATX, more than 1 M units, 10+ models | **China JV brands** (probably VW), so China-built [P] | — |

**The pattern.** Lidar in Western cars was tied to **eyes-off L3**. That feature was narrow in operation (60–95 km/h, daytime, dry, lead vehicle, specific roads), expensive (€5–6k or \$2.5k per year) and rarely bought. When L3 was cut, the lidar went with it. The retreat is **mainly commercial and regulatory, not a sensor-physics verdict**. It also suggests that carmakers do not see lidar as necessary for *supervised* L2++, where cameras and radar offer more visible features at lower cost [E] (§G4).

## B3. Western supplier health

| Company | Route | Status (Sep 2026) |
|---|---|---|
| **Luminar** | 1550 nm dToF, fiber laser, InGaAs, 2-axis mirror | Chapter 11 on 15 Dec 2025. Semiconductor unit to Quantum Computing Inc. (\$110 M); **lidar business to MicroVision (\$33 M)**; equity cancelled Apr 2026 [P]. Stated rationale was about 17× eye-safe photon flux. Its difficulties arose mainly from OEM program economics and the unmet obligations Volvo cited; its 1550 nm cost structure contributed; sensor performance was not the main factor [E] (§G3) |
| **Valeo SCALA** | 905 nm, rotating mirror | About 150–170k units since 2017; >€1 B SCALA 3 orders, but the Stellantis L3 was shelved and the Mercedes next-L3 went to Hesai [P/T] |
| **Innoviz** | 905 nm, MEMS | FY25 revenue \$55.1 M; FY26 guidance \$67–73 M; 9 InnovizTwo per VW ID. Buzz AD (Mobileye Drive, about 150k-unit program life claimed); Daimler Truck/Torc short-range; reverse split approved Sep 2026 [P] |
| **Ouster** (+Velodyne) | 865 nm, VCSEL + SPAD SoC, spinning | FY25 revenue \$169 M, more than 25k sensors; mostly industrial and infrastructure. Lost its arbitration with Hesai (paid about \$6.4 M in costs) [P] |
| **Aeva** | FMCW (silicon photonics) | FY25 revenue \$18.1 M; H1 2026 \$12.4 M; cash \$177.9 M; Daimler C-samples; LG Innotek stake of about 6% [P] |
| **MicroVision** | Acquired technologies: MEMS 905, Ibeo flash (MOVIA), Luminar 1550, Scantinel FMCW | Q1 2026 revenue \$0.9 M; cash about \$46 M; industrial and defense focus [P] |
| **Cepton → Koito** | 905 nm | Taken private Jan 2025; GM Ultra Cruise orders cancelled 2023 [P] |
| **AEye** | 1550 nm adaptive MEMS | FY25 revenue \$233k; defense [P] |
| **Tier-1 exits** | — | Bosch (2023); Continental HRL131 (2023; Aumovio now builds Aurora hardware); ZF via Ibeo insolvency (2022); Mobileye in-house FMCW (Sep 2024) [P/T] |

## B4. Robotaxis and trucks outside China

**Installed base (late Sep 2026)** [E, built from P/I counts]: about **27–40k lidars on about 6–7.5k vehicles**.
- **Waymo:** about 4,000 vehicles, with 5 lidars on the 5th generation and 4 on the 6th. **All in-house and captive.**
- **Tesla:** 0 lidars in production (about 476–546 registered in Texas; community trackers count about 85–200 active unsupervised vehicles in late Aug 2026; Tesla discloses no fleet number).
- **Zoox:** about 100 robotaxis; Hesai ("multiple" lidars in 4 corner pods, exact count undisclosed); paid Las Vegas rides from 10 Aug 2026; NHTSA exemption up to 2,500 per year.
- **Motional:** 109 vehicles; 4 Hesai + 1 Ouster.
- **Avride:** about 200 vehicles; 5 lidars each.
- **VW ID. Buzz AD / Mobileye:** 9 Innoviz each; about 500 vehicles targeted by end-2026.
- **Chinese operators abroad** (WeRide about 400 in the Middle East; Pony and Baidu in Doha, Zagreb, Dubai and Switzerland): Hesai or RoboSense.
- **Trucks:** only about 1–2.5k lidars in total.
  - **Aurora:** FirstLight FMCW plus short-range units; about 25 driverless trucks; 200 targeted by year-end. Its 2022 business update listed **9 lidars per truck**: 3 long-range and 2 mid-range in the main pod, plus 4 near-range. Hesai is reported as the near-range supplier. No count was found for the 2025–26 hardware [P/T].
  - **Kodiak:** 2 Luminar + 2 Hesai per truck.
  - **Torc/Daimler:** Aeva long-range + Innoviz short-range.

**Annual consumption 2026:** about **20–47k lidars, central estimate about 30k**, of which about half is Waymo's captive supply. The merchant market is only about **10–25k units**.
- A plan-based 2027 scenario gives about 70–225k, but historically AV ramps slip.
- **By value**, AV lidar outside China is a much larger share, because robotaxi and truck lidars cost several times more than \$200 ADAS units.

**Exposure.** Most merchant AV lidar in the US is **Hesai**: Zoox, Motional, Kodiak, Waabi and Aurora's short-range units.
- Hesai signed a **\$40 M order from an unnamed "leading U.S. robotaxi company"** as sole supplier, for delivery by end-2026. That is most likely Zoox [E].
- Idaho National Laboratory is probing Chinese lidar for security vulnerabilities (Aug 2026) [T].

## B5. How niche is lidar outside China? (estimate)

| Segment | Estimate | Basis |
|---|---|---|
| Non-Chinese-OEM passenger cars sold outside China with lidar (2025) | **about 30–80k** [E] | Volvo EX90 (about 16k built in 2025, lidar standard until the Luminar contract ended); Mercedes Drive Pilot (uptake undisclosed; "low demand"); BMW 7 Series L3 (undisclosed; BMW cited profitability); Lucid DreamDrive Pro (a few thousand); Lexus and Honda (hundreds); Valeo's historic average about 20k per year |
| Chinese-brand exports with lidar (2025) | **about 15–60k, central 25–35k** [E, low confidence] | Official exports of lidar trims are small: NIO overseas in the low thousands (every NIO has lidar); Zeekr lidar trims are a fraction of roughly 10–20k overseas sales; Aito and Denza in the hundreds to low thousands. Xpeng exports are mostly vision-only; BYD God's Eye A/B trims are rare abroad. **"Parallel exports"** of zero-mileage lidar models (Li Auto, Aito) to Russia, Central Asia and the Middle East may be the largest single channel and are invisible in company data |
| **Total passenger-car lidar outside China (2025)** | **about 45–140k** [E] | About **0.1–0.2%** of about 60 M non-China light vehicles. A top-down proxy (non-Chinese suppliers' 5–7% of 3.7 M) gives 185–260k and is probably an upper bound |
| 2026 | **likely lower** [E] | Volvo, BMW and Mercedes L3 exits; the restart comes in 2027–28 |
| Robotaxi and truck lidar outside China (2026) | about 20–47k (central 30k) [E] | §B4 |
| OEM thermal night vision, global | about 50–100k per year (mostly outside China) plus China about 25–30k (2025) [E] | FLIR/Veoneer/Magna cumulative milestones: more than 500k (Sep 2019), more than 700k (Jan 2020), "nearly 1 M" (Feb 2021), "over 1.2 M" (May 2024) [P]. That implies about **60–70k per year in 2021–24**. China's Jan–Sep 2025 figure was 19k |

**Conclusion.** Outside China, passenger-car lidar and OEM thermal night vision are both at about **0.1–0.3% of production**, and lidar may dip below thermal in 2026. In China, lidar is about 100× thermal. The claim "outside China, lidar is nearly as niche as thermal" holds on these numbers, with wide error bars on Chinese exports.

## B6. Western brands in China: pressure to adopt lidar

**Short answer.** Yes. The pressure is strong for any Western brand competing in Chinese NEVs above about ¥150k, and it is already being acted on, mostly by buying Chinese ADAS stacks and Chinese lidar. The result is a paradox: **Western brands are becoming some of the world's largest lidar buyers, but for China-built cars**, while their home-market lidar programs retreat (§B2).

**Market context** [T]:
- **VW** (FAW-VW + SAIC-VW) held **10.9% of China retail sales in 2025**, down from 12.2% in 2024. That put it third, behind BYD (14.7%) and Geely (about 11%).
  - In Jan–Feb 2026 VW was back at #1 with 13.9% as EV purchase-tax exemptions changed. Toyota (GAC + FAW joint ventures) was #3 at 7.8%.
  - VW's share was roughly 19–20% before about 2020 [U]. The decline since may be one reason the joint ventures now adopt Chinese technology widely [E].
  - VW's battery-EV deliveries in China fell 44% in 2025.
- **Joint-venture NEV penetration** rose from 16.5% to 25.1% (Jan–Jul 2026, Gasgoo), described as a breakthrough by a few brands rather than a collective reversal.

**Why the pressure exists:**
- Lidar is in about **21–25% of new NEVs**, available from about ¥80–90k, standard at Li Auto and Xiaomi, and a ¥12k option across BYD's range.
- Buyers compare urban NOA capability directly, and the lidar "hump" has become a visible technology and safety signal.
- China's rules raise the bar without naming sensors:
  - GB 47955 (mandatory L2 standard) takes effect Jan 2027;
  - GB 44721 (L3/L4 safety baseline) takes effect Jul 2027;
  - C-NCAP 2027 adds night, rain and fog scenarios.
- Chinese competitors refresh ADAS every 12–18 months. A joint-venture product without competitive assisted driving loses share quickly.

**How Western brands are responding** [T/P; supplier details as reported]:

| Brand / JV | Model(s) | Lidar | ADAS stack | Notes |
|---|---|---|---|---|
| **Toyota** (GAC-Toyota) | bZ3X | RoboSense on the lidar versions of the 520 Pro/Pro+; optional on the 610 Max | Momenta 5.0 | From ¥109,800. **Top-selling joint-venture NEV from Sep 2025 to Apr 2026**; 10,027 units in Apr 2026 |
| **Toyota** (GAC-Toyota) | bZ7 and new NEVs | Hesai ATX | — | Mass production 2026 |
| **Toyota** (FAW-Toyota) | NEV lineup | RoboSense (about 1–1.5 M-unit orders) | Momenta | — |
| **VW** (VW Anhui) | ID.UNYX higher version | Lidar (supplier not stated) | Carizon (VW–Horizon Robotics JV) | Described as the first lidar in the ID.UNYX line |
| **VW** (China JV brands) | 10+ models | **Hesai ATX, more than 1 M units** (a "top European OEM", most likely VW per Hesai's 6-K) | Mixed | Announced May 2026 |
| **VW** (with Xpeng) | ID.UNYX 07/08 ("Zhong 08") | Probably none [E]: Xpeng's stack is vision-only | Xpeng VLA 2.0, Turing chip | VW is hedging both routes |
| **Nissan** (Dongfeng-Nissan) | N7 and successors | RoboSense (about 1 M-unit order, Dec 2025) | Momenta | — |
| **GM** | Cadillac XT5 PHEV and VISTIQ (China) | Lidar; Hesai AT series reported for the VISTIQ | Momenta R7 | — |
| **Mazda** (Changan-Mazda) | EZ-60 | Lidar version | Changan platform | — |
| **Mercedes** | CLA (China) | Not standard on the L2++ system [T]; next L3 uses Hesai for China and Europe | Momenta (China) | — |
| **BMW** | iX3 long-wheelbase (China) | One lidar reported [U] | Momenta | — |
| **Audi** | SAIC Audi E5 and others | [U] | Huawei partnership | — |
| **Ford** | — | No lidar program found | — | Ford's China passenger presence is small, so pressure applies only if it competes in mainstream NEVs |

**My judgement:**
- **The pressure is strong, and the response is under way.** In the ¥150k+ NEV segment, lidar-equipped urban NOA is close to table stakes, and the joint ventures meet it through Chinese stacks (Momenta, Horizon/Carizon, Huawei, Xpeng) and Chinese lidar (RoboSense, Hesai). **Probability that by 2028 most Western-brand NEV models above ¥150k in China offer lidar, at least as an option: about 70%** [E].
- **It is not universal.** Vision-only stacks remain viable (VW's Xpeng-based models, BYD God's Eye C, Tesla), so lidar is "expected on upper trims" rather than mandatory. Western brands in cheaper segments, or with a small China presence like Ford, feel much less pressure.
- **Consequences:**
  1. **The volume paradox.** Western brands' largest lidar volumes are in China: Hesai's 1 M+ ATX order for a European OEM's joint ventures, and RoboSense's orders from the Toyota and Nissan joint ventures, which run into the millions. Their home-market programs, by contrast, were cut (§B2).
  2. **Two-track products.** China versions get Chinese ADAS and lidar; Western versions get cameras and radar with Western or NVIDIA software. Examples: Mercedes CLA (Momenta in China, NVIDIA in the US) and BMW iX3 (Momenta in China).
  3. **Know-how flows back.** China programs teach Western carmakers lidar integration at scale. Mercedes then picked Hesai for its next global L3, and China-built joint-venture EVs such as the bZ3X have been spotted testing in right-hand-drive form overseas [T]. That is a possible export route for lidar-equipped Western-brand cars.
  4. **Geopolitics splits the tracks.** US rules (Chinese ADS software banned from MY2027; a possible lidar ban, §F3) stop these China stacks moving into US models. Europe can take them (the "Hesai-in-Mercedes template", §F3).

---

# Part C — Technology routes and physics

## C1. Taxonomy

| Design axis | Options |
|---|---|
| **Detection** | Pulsed direct ToF (dToF; histogramming or threshold); indirect ToF (short range); **FMCW coherent** (range + radial velocity) |
| **Wavelength** | 850–865 nm (Ouster); **905 nm**; **940 nm** (sits in a water-vapour dip in the solar spectrum); **1550 nm** (fiber laser + InGaAs); 1064 nm (Continental HFL110) |
| **Emitter** | Multi-junction EEL (ams OSRAM SPL, 3→5 junctions); **multi-junction VCSEL line and 2D arrays** (addressable); Er-fiber MOPA (1550 nm); narrow-linewidth chirped laser + SOA (FMCW) |
| **Detector** | Si APD; **Si SiPM**; **Si SPAD-SoC** (BSI, Cu–Cu stacked, per-pixel TDC/sampling); InGaAs APD (1550 nm); coherent balanced photodiodes (FMCW) |
| **Scanning** | 360° mechanical spinning (robotaxi); **1D rotating or oscillating mirror + electronically addressed column** (dominant); polygon + galvo (Seyond 1550 nm); 2D MEMS (RoboSense M, Innoviz); **flash / electronic scanning** (addressable VCSEL × SPAD; blind spot); Risley prisms (Livox); OPA; liquid-crystal metasurface (Lumotive); wavelength steering (Baraja) |

## C2. Market share by technology

- **Yole, 2024 passenger cars:** rotating-mirror "hybrid solid-state" **66%**, MEMS **32%**; near-IR (905/940) **about 90%** of volume.
  - Yole's ten-year outlook: rotating mirror 52%, MEMS 6%, **flash 37%**.
  - These figures came from a search extract of Yole's page [S/T].
- **Derived China shares** [E]:
  - 1550 nm fell from about 12–13% of units (2024) to about 6% (2025) to about 4–5% (H1 2026).
  - Even Seyond shipped 71% 9xx-nm Robin units in Q2 2026 [T].
- **Scanner, 2024, weighted by supplier** [E]: one-axis mirror about 54% (Hesai + Huawei); 2D MEMS about 33% (RoboSense M); polygon + galvo about 13% (Seyond Falcon). MEMS is fading: RoboSense calls the MX its last MEMS generation and has moved to its SPAD-SoC "EM" line.
- **Detector** [T]:
  - SiPM: Hesai AT128, ATX, JT.
  - SPAD-SoC: Huawei D-series; RoboSense E and EM; Hesai ETX/Picasso and FTX; Seyond Robin E2.
  - InGaAs APD: Seyond Falcon.
  - NE Times: **SPAD-SoC wins on cost above about 200 lines; SiPM is cheaper below that.**
- **FMCW:** effectively 0% of passenger-car units. OPA: 0%.

## C3. Company route table (condensed)

| Company | Main automotive product(s) | Detection | λ | Emitter / detector | Scanning | Range @10% | Status / volume |
|---|---|---|---|---|---|---|---|
| **Hesai** (CN) | AT128 (2022), **ATX** (2025), ETX/Picasso (H2 2026), FTX (blind spot); OT/Pandar/XT/QT/JT (robotaxi, robotics) | dToF | 905 (FTX/QT: 940) | VCSEL + **SiPM** (AT/ATX); SPAD-SoC (ETX, FTX) | 1D mirror (3-facet rotating on AT128; oscillating on ATX); FTX electronic scan | 200–230 m (ATX). ETX: **400 m @10%** is the platform-wide headline (first used for the 800-channel ETX in 2025, no mode stated); **300 m @10%** is the only figure in the formal spec table (10 Hz, 120°×20°, 0.06°×0.055°/0.027°). Both are company claims | 1.62 M in 2025; ATX >1 M delivered, >6 M backlog; Mercedes L3; VW China JVs; Toyota JVs; NVIDIA Hyperion 10 |
| **RoboSense** (CN) | M1/M1P/MX (2D MEMS); **EM4/EMX** ("digital"); E1/E2 (flash); Phoenix/Peacock chips (2026) | dToF | 905 (M); **940** (M3, EM, likely E) | EEL + APD/SiPM (M); VCSEL + SPAD-SoC (EM, E) | 2D MEMS → **1D mirror** (EM); electronic scan (E) | 200 m (MX); EM4 300 m (basis unclear) | about 912k in 2025; ADAS backlog >9 M; FAW-Toyota, Dongfeng-Nissan |
| **Huawei** (CN) | 96/192/**896-line** (dual optical path), SL210 solid-state, Limera in-cabin | dToF | 192-line: **905 nm** (TechInsights teardown); 896-line undisclosed | 192-line: 4 emitters (VCSEL line arrays, reportedly from Vertilite) + **SPAD 189×600** (Sony IMX459 geometry) | 192-line: **4-facet rotating prism** with magnetic encoder, 120°×20°, ≤20 Hz, 180 m @10%, about 1.84 Mpts/s. 896-line: one transmitter, two receivers (wide about 120°, tele about 30° per media; about 600 + 300 "equivalent lines" per media, unverified) | 896: 14 cm object at 120 m (Huawei); 400 m in tele mode per media | #1 China share 2025 (41.5% incl. blind spot) |
| **Seyond** (CN/US) | Falcon K/K2/K3 (1550); Robin W/E1X/E2; Hummingbird D1 | dToF | **1550** / 905 (Robin W) and **940 (Robin E1X, per its datasheet)** | Er-fiber MOPA + InGaAs APD / VCSEL + SiPM or SPAD | **Polygon + galvo** / 1D / flash | 250 m (K2), 450 m (K3). Robin E1X: 200 m @10% (10 Hz), 300 m max, 120°×20°, 1200×96 points, 0.1°×0.2°, 6 W, 470 g, Class 1 | NIO-dependent; moving to 9xx for cost |
| Zvision, Tanway, Vanjee, Leishen, Benewake, Livox (CN) | various | dToF | mostly 905; Leishen and Benewake 1550 | — | MEMS / 1D mirror / prism | 150–300 m | Mostly robotics and industrial; Livox has in effect left automotive (Xpeng went lidar-free Nov 2024) |
| **Valeo** (FR) | SCALA 1/2/3 | dToF | 905 | EEL + Si APD [U] | 1D rotating mirror | 200 m low-reflectivity (SCALA 3) | About 150–170k in total |
| **Innoviz** (IL) | InnovizOne/Two/Three | dToF | 905 | — | 2D MEMS | about 250–300 m [U] | BMW (L3 ended), Mobileye Drive, Daimler Truck |
| **Luminar → MicroVision** (US) | Iris, Halo | dToF | **1550** | Fiber + InGaAs APD + ROIC | 2-axis macro-mirror | Halo 200 m | Liquidated; assets \$33 M |
| **Ouster** (US) | OS Rev7/Rev8 | dToF | 865 | VCSEL + CMOS SPAD SoC | spinning | 90 m (OS1), 200 m (OS2) | Industrial and robotaxi mapping |
| **Opsys** (IL) | ALTOS 70/150/300 | dToF | 905/940 | addressable VCSEL × addressable SPAD | **fully solid-state** | 55/100/200 m (FOV shrinks with range) | ITS / security |
| **Waymo** (US) | 5th/6th-gen in-house | presumed dToF | undisclosed | — | roof 360° + perimeter | >300 m (5th gen) | 4 lidars per 6th-gen vehicle; captive |
| **Aurora** (US) | FirstLight gen 1 → gen 2 → gen 3 | **FMCW** | about 1550 | III-V laser + custom SOAs on SiN photonic engine | undisclosed | about 1 km (gen 2, max, company claim) | About 25 driverless trucks; gen 2 kit built by Fabrinet; gen 3 with Aumovio 2027 |
| **Aeva** (US) | Aeries II, Atlas, Atlas Ultra | **FMCW** | not stated (1550 assumed) | SiPh "CoreVision" + X1 SoC | scanner (type undisclosed) | 250 m low-reflectivity (Atlas Ultra) | Daimler Truck (2027), EU OEM L3 (2028), Bendix L2+ |
| **Mobileye** (IL/US) | in-house FMCW (Intel SiPh, 184 lines) | FMCW | — | — | — | — | **Ended Sep 2024** (about 100 staff, about \$60 M R&D in 2024); now uses Innoviz |

## C4. Why 905/940 nm with silicon receivers and one mechanical axis won

**1. Eye safety: what 1550 nm really buys.** From IEC 60825-1:2014 Class 1 limits, not checked against the standard in this draft [U/E].
- **Single ns pulse:**
  - 905 nm: about $2\times10^{-7}C_4$ J, with $C_4=10^{0.002(\lambda-700)}=2.57$, so about **0.51 µJ**.
  - 940 nm: $C_4=3.02$, so about 0.60 µJ, i.e. **+17.5%**.
  - 1500–1800 nm: about **8 mJ**, roughly $10^4\times$. The repetitive-pulse correction $C_5=N^{-1/4}$ reduces this in practice.
- **Long-exposure average power:**
  - 905 nm: about $3.9\times10^{-4}C_4\approx1$ mW, before scanning and extended-source relaxations.
  - 1550 nm: about 10 mW, so about **10×**.
  - Multiplied by the photon-energy ratio (1550/905 ≈ 1.71), that gives **about 17× the photon flux**. Luminar's FY2024 10-K cites exactly "17×" [P].
  - The "40×" and "$10^4$–$10^6$×" figures in company materials use different bases.

**2. Detectors.**
- **Silicon absorption:** $\alpha\approx3.1\times10^2$ cm⁻¹ at 905 nm ($1/\alpha\approx32$ µm) and about $1.8\times10^2$ cm⁻¹ at 940 nm ($1/\alpha\approx56$ µm).
  - Front-side SPADs reached only 2–5% PDE.
  - **BSI + Cu–Cu stacking + light trapping** (textured surface, deep trench isolation, back reflector) raised this to **24% at 905 nm** (IMX459) and **37% at 940 nm** (IMX479) [P].
- **InGaAs/InP APDs:**
  - The InP multiplier's excess-noise factor is $k\approx0.4$–0.5 (vs about 0.02 for Si), which limits linear gain to about 10–20.
  - InGaAs SPAD arrays suffer from dark counts and afterpulsing, and have needed cooling [U].
  - InGaAs wafers are small and expensive.

**3. Source, power and heat.**
- A 1550 nm fiber MOPA (seed + EDFA + 940 nm pump, split 1→4) is expensive and hot. Falcon K drew 30 W and K2 20 W, against about 6–10 W for 9xx-nm units (Robin E1X, Hesai ATX).
- A four-way split source forces fast two-axis mechanical scanning.
- A **VCSEL column × SPAD column** gets 128 to more than 2,000 lines electronically with **one** scan axis.

**4. Solar background.**
- Direct solar spectral irradiance: about 0.25 W m⁻² nm⁻¹ at 1550 nm, about 0.7 at 905 nm, and about 0.3–0.45 at 940 nm (water-vapour dip) [U, approximate ASTM G173].
- **VCSEL wavelength drift** (about 0.07 nm/K, vs 0.25–0.3 nm/K for EELs) allows 10–20 nm receive filters instead of about 40 nm, roughly halving background.
- Hence the drift to **940 nm + VCSEL**.

**5. Liquid water penalises 1550 nm.** Absorption is about 10 cm⁻¹ at 1550 nm vs about 0.07 cm⁻¹ at 905 nm; a 1 mm water film absorbs about 63% at 1550 nm. That hurts wet windows and weakens claims that 1550 nm performs better in rain.

**6. Why one mechanical axis.**
- Semiconductor arrays scale cheaply along one axis (a VCSEL line and a SPAD column).
- A robust, cheap mirror covers the other (about 120° horizontal).
- That avoids MEMS aperture and FOV limits and the étendue penalty of fully staring receivers (§C6).

**7. Cost.**
- KrASIA, summarising Seyond's prospectus: the InGaAs route is **2–3× the cost** of 905 nm [T].
- Yole: 1550 nm cost is hard to reconcile with OEM targets [S].
- RoboSense M3 (940 nm) was pitched as 50–70% cheaper than 1550 nm competitors [P].

**Where 1550 nm ToF survives:** NIO (Seyond Falcon K3, 450 m @10%), trucks and off-road, defense and very long range (AEye; MicroVision ex-Luminar), and as the natural band for FMCW.

## C4b. SiPM vs SPAD-array (SPAD-SoC) receivers

Both receivers are built from the same element: a **SPAD**, i.e. a Geiger-mode avalanche photodiode biased above breakdown ($V_{\rm bd}$) by an excess bias $V_{\rm ex}$. Each detected photon triggers a binary avalanche, which must be quenched and recharged. During that dead time $\tau_d$ (a few to tens of ns) the cell is blind. The two architectures differ in **how many SPADs are combined per lidar channel, and whether the combining is analog or digital**.

### Architecture

| | **SiPM** (silicon photomultiplier, MPPC) | **SPAD array / SPAD-SoC** ("digital lidar") |
|---|---|---|
| Structure | Hundreds to thousands of microcells (about 10–75 µm each), each with a passive quench resistor, **all wired in parallel to one output** | Each SPAD (or a small macro-pixel such as 3×3) has **its own active quench/recharge and a digital output**, usually with a logic wafer bonded underneath |
| Output | **Analog current pulse** whose amplitude is roughly proportional to the number of cells fired (a multi-photon signal) | **Digital events → timestamps → on-chip histograms** (TDC or equivalent-time sampling, then DSP and compression) |
| Signal chain | External analog front end **per channel**: TIA, comparator or ADC, TDC; often an ASIC plus FPGA | Front end integrated **under each pixel** via 3D stacking; data leave as compressed point or echo data over MIPI |
| One lidar channel = | One SiPM element (for example one of the 12 in onsemi's 1×12 ArrayRDM) | One pixel or macro-pixel (for example Sony's 3×3-binned IMX479 pixel) |
| Examples | Hesai AT128 (onsemi SiPM) and **ATX (17 SiPM dies × 4 channels)**; InnovizOne (onsemi ArrayRDM-0112); Cepton; Seyond Robin E1X [T] | Sony IMX459/IMX479; RoboSense E1/EM4/Phoenix; Hesai FTX/Picasso; Huawei D-series; Ouster L3/L4; Adaps ADS6311 |

A SPAD-SoC **macro-pixel** of 3×3 SPADs with coincidence detection is effectively a tiny *digital SiPM*, and "digital SiPMs" (per-cell digital readout, summed output) also exist. The boundary blurs, but the scaling behaviour differs sharply.

### The core physics trade: per-channel dynamic range vs spatial resolution

**Saturation.** With $N_c$ cells per channel and $n$ photons detected within one dead time, the expected number of cells fired is

$$N_{\rm fired}=N_c\left(1-e^{-n/N_c}\right)$$

Example [E], with $n=20$ detected photons in a pulse:
- **SiPM channel** ($N_c=1000$): $N_{\rm fired}\approx19.8$. The response is essentially linear, so it can tell 20 photons from 100.
- **3×3 SPAD macro-pixel** ($N_c=9$): $N_{\rm fired}\approx8.0$. It is saturated, so 20 and 100 photons look almost the same.
- The SPAD-SoC compensates with **multi-shot histogramming** (several shots per point), **coincidence detection** and **pixel-level thresholds**. It works statistically, not in a single shot.

**Sunlight and pile-up.** For the same optics (field and aperture per channel), the background photon rate per channel is the same, but a SiPM spreads it over about $10^3$ cells.
- Per-cell background rate is about 1000× lower, so **dead-time blocking is negligible**.
- Sunlight instead appears as a DC background current plus shot noise on the analog signal, and a multi-photon threshold can sit above it.
- A 3×3 SPAD macro-pixel with the same field can be dead **8–59% of the time** in bright sun (§C6(d)), and pile-up distorts its histogram.
- **That is why SiPMs pair well with large-aperture, modest-channel-count scanned lidars.**

**Spatial resolution.**
- SiPM channels are large (hundreds of µm), so the lidar's angular resolution comes from **laser channel addressing and scanning**, not detector pixels.
- SPAD-SoCs have 10 µm pixels, so the **receiver pixels themselves set the angular resolution** (for example 0.05° vertical in IMX479). That enables "image-grade" 500–2,000+ line receivers.

### Other dimensions

| Dimension | SiPM | SPAD-SoC |
|---|---|---|
| **Channel-count scaling** | Limited by one analog path and ASIC input per channel: practical ranges are tens to about 128 physical channels. The ATX uses 64 physical channels and multiplies effective lines by laser addressing | Scales on chip: 520 → 2,160 channels per die, because timing and histogramming sit under the pixels and data are compressed on chip. Limits are the reticle and memory (§C6) |
| **PDE at 905/940 nm** | Historically about 5–10% (front-side); NIR-enhanced automotive SiPMs are in the mid-to-high teens [U]. Fill factor (30–80%) is set by cell size, trenches and quench resistors | 24% (IMX459, 905 nm), 37% (IMX479, 940 nm), 45% (RoboSense 3rd-gen SPAD) with BSI, stacking and light trapping. **Now ahead on PDE** |
| **Timing** | Good single-photon timing, but large capacitance slows pulses, and TIA noise adds jitter | Per-pixel TDC or equivalent-time sampling at ps resolution (IMX479: 3 GHz). Ranging precision is cm-class in both |
| **Bias and power** | Tens of volts of bias; front-end power per channel (TIA/ADC) scales with channel count | About 20+ V on the SPAD layer; **avalanche power scales with count rate** (§C6(f)) plus on-chip DSP power |
| **Bill of materials** | Cheap mature dies, but an **external front end, ADC and FPGA per channel** | **One stacked die (two wafers plus hybrid bonding) replaces** discrete front ends, ADCs and part of the DSP. Cost per channel falls with channel count |
| **Cost crossover** | Cheapest below about 200 lines (NE Times) | Cheaper above about 200 lines, and the natural choice for flash and e-scan units |
| **Supply chain** | onsemi (SensL), Hamamatsu, Broadcom, Ketek, FBK; Chinese in-house or startup SiPMs (Hesai claims in-house; Adaps) [T/U] | Sony (merchant); in-house Chinese (RoboSense, Hesai, Huawei/HiSilicon); Adaps, Fortsense, VisionICs; ST (Ouster) |

### Where each wins, and the trend

- **SiPM wins** for cost-optimized long-range scanned lidars with 64–128 physical channels. It gives single-shot multi-photon dynamic range, robustness to sunlight and retroreflectors, and a simple large-aperture design.
  - **Hesai's ATX, which Hesai calls the best-selling long-range lidar in the ADAS segment (more than 1 M delivered, under \$200), uses SiPM.**
  - Innoviz (MEMS) and Cepton also use SiPM.
- **SPAD-SoC wins** wherever resolution or integration matters:
  - "image-grade" main lidars with 500–2,000+ lines (RoboSense EM4 and Phoenix, Hesai ETX/Picasso, Huawei 192/896-line);
  - all flash and e-scan blind-spot units (FTX, E1, SL210), where a 2D pixel array is unavoidable;
  - on-chip RGB-D fusion (Picasso, Limera).
- **Trend** [E]:
  - Main lidars move from SiPM to SPAD-SoC as line counts pass about 200 and per-channel front-end cost becomes the bottleneck.
  - The share of SiPM in automotive units falls through 2030 but doesn't vanish. Cost-down 100–200-line units and some Western designs keep it.
  - The architectures also converge: SPAD-SoC macro-pixels with coincidence behave like small digital SiPMs, and SiPM front ends gain on-chip digitization.

## C5. SPAD-SoC receivers in Chinese lidars: design origin and foundries

**The line-count shortcut.** "Line count" in this class is the receiver's long-axis dToF pixel count after 3×3 binning.
- **Sony IMX459:** 597×168 SPADs, 10.08 µm pitch, BSI SPAD wafer Cu–Cu bonded to a logic wafer (90 nm SPAD / 40 nm logic in the ISSCC 2021 design), PDE 24% at 905 nm. Binned, this gives about **192** lines [P].
- **Sony IMX479:** 105×1,568 SPADs, 10.08 µm, **520 dToF pixels** at 0.05° vertical, PDE 37% at 940 nm, 3 GHz equivalent-time sampling, about 98% on-chip data reduction, 25 Mpts/s [P].

| Product | Verified | Inferred / unknown |
|---|---|---|
| Huawei 96-line | TechInsights: **Sony SPAD depth sensor** + 2 Lattice FPGAs [I] | — |
| Huawei 192-line (L306 / D3) | SPAD array **189×600** = the IMX459 geometry; TechInsights says this "suggests" Sony [I] | Very likely Sony |
| Huawei 896-line (Mar 2026) | Wide + telephoto receive paths, each with its own SPAD chip [P] | Vendor unknown; no teardown. One teardown write-up says HiSilicon has its own SPAD-SoC in the D3P and Limera (fab unknown) [T] |
| RoboSense E1/E1R | In-house SPAD-SoC, >250k px, Cu–Cu, AEC-Q102 [P]. TechInsights: **0.27 MP at 9.8 µm pitch**, stacked BSI [I] | **Matches no Sony catalogue part**, consistent with an independent design. Co-developed with Adaps (2019–23); **the two companies are now suing each other** |
| RoboSense EM4-520 | NE Times teardown: "uses Sony IMX479" [T]. TechInsights: 0.20 MP at 10.0 µm [I] | **Most likely IMX479.** The "SPAD-SoC" label here means Sony's stacked chip |
| RoboSense EMX (192-line) | Marketed as a digital SPAD-SoC | 192 lines = the IMX459 geometry; not teardown-verified |
| RoboSense Eocene "Phoenix" (2160×1900) / "Peacock" (640×480) | **28 nm logic**, SPAD PDE 45%, wafer-level hybrid bonding; mass production 2026 [P] | Foundry undisclosed. Candidates: TSMC, UMC, SMIC, XMC, Huali |
| Hesai AT128 | **onsemi SiPM** + Lumentum VCSEL + Xilinx FPGA [I, Yole teardown] | — |
| Hesai ATX | SiPM (17 dies / 64 channels), TI, 3peak and Infineon parts [I] | SiPM vendor not public; Hesai claims in-house detectors |
| Hesai FTX / ETX "Picasso" | Uses SPAD IP from its acquisition of **Fastree3D** (Swiss, EPFL). Picasso is a 5th-generation RGB+ToF SPAD-SoC, PDE >40% (**wavelength not stated**). **2,160 lines per chip; the 4,320-line ETX uses two chips** [P/T] | Foundry, node, pixel pitch and stacking undisclosed. One Chinese article says Adaps SPAD chips have orders from Hesai and RoboSense [T, single source]. **There is no Hesai "V-series" chip name**; generations are called 4th-gen ASIC, Fermi C500 and Picasso |
| Adaps ADS6311 | 256×192, 297 ps bins, Cu–Cu hybrid-bonded, AEC-Q102 [P] | Foundry unnamed; one commentator says domestic SPAD startups mostly use **Tower** (Israel) [T] |

**Fastree3D: the European SPAD lineage now inside Hesai.**

| When | Event | Source |
|---|---|---|
| 2000–2002 | Edoardo Charbon is chief architect at **Canesta**, which developed 3D CMOS time-of-flight image sensors. Microsoft bought Canesta in 2010 and used its technology in the later Kinect 3D camera | [I, Wikipedia bio] |
| 2002→ / 2008–2016 | Charbon joins the EPFL faculty (full professor 2015; heads the **AQUA** lab) and also holds the TU Delft Chair of VLSI Design (2008–2016). He is a pioneer of SPADs in standard CMOS, e.g. early 128×128 SPAD imagers with per-pixel TDCs | [I] |
| 2012 | Claude Florin (EPFL EE graduate; formerly at HP Labs/Philips and in early-stage VC) meets Charbon. **Bogdan Staszewski** (TU Delft; time-to-digital-converter and digital-PLL expert) joins as partner/advisor | [T, 2020 and 2021 interviews] |
| Sep 2013 / 2014 | Fastree3D SA incorporated in Lausanne (EPFL Innovation Park, with an office in Delft) as an **EPFL + TU Delft spin-off**. Florin is CEO, Charbon CSO, Lucio Carrara CTO. It starts with more than 15 patents from about 20 years of academic work | [P, company "About"; T] |
| 2014–2017 | Venture Kick stage-3 winner (2014); two EU Horizon 2020 projects, a Dutch STW project, Innosuisse/CTI grants; Top-15 Swiss startups (2016); European Photonics Venture Forum winner (2016, 2017) | [P] |
| ~2019–2021 | **Product concept:** fabless, "single-chip 2D + 3D flash lidar" for short range, on Si-CMOS SPADs with ps timing and low-cost NIR VCSELs; 1–15 MHz laser repetition. A 30° FOV / 30 m demonstrator, and a 40k-pixel / 60 m version in development (2021). About 10 staff in 2020 | [T, Laser Focus World 2021] |
| 2020 | Joint R&D reported with **Bosch and NXP**. Other profiles also list interest from Audi-VW, Qualcomm-Veoneer, ifm and Sick. **Series system-on-chip was targeted for 2022** but never reached independent production | [T] |
| Total funding | Only about **\$5.9 M** raised (A3 Angels, Basel Area Business & Innovation, Delft Enterprises and others), plus grants | [T, Crunchbase/Dealroom] |
| **Late 2023** | **Acquired by Hesai** (price undisclosed). Publicly disclosed on 27 Feb 2025, when Hesai said Fastree3D's SPAD patents underpin its 4th-generation platform and the FTX solid-state lidar (180°×140°, 30 m @10%, 492k pts/s). Hesai says it had researched SPADs since 2016 | [P, Hesai PR] |
| 2025 | Knowmade ranks Hesai the automotive-lidar IP leader among pure players: 920 applications in 558 families, with SPAD/SiPM detectors as its largest cluster | [T, Knowmade Nov 2025] |

**Why it matters** [E]:
- It is an example of **European SPAD and TDC know-how** (the Canesta→Kinect lineage, EPFL AQUA, TU Delft) that could not reach automotive scale on about \$6 M.
- It was absorbed by the Chinese lidar maker that had the volume to industrialize it. Fastree3D's IP is part of why Hesai's FTX and Picasso SPAD chips count as "separate designs" rather than Sony parts.
- It mirrors the wider pattern in Parts B and D: Western lidar IP consolidating into buyers with scale (Luminar→MicroVision, Scantinel→MicroVision, Ibeo→MicroVision), except that here the buyer was Chinese.

**Foundry check (gap-fill pass).** Across English and Chinese press releases, teardown summaries and litigation coverage, **no foundry is publicly named for any Chinese in-house lidar SPAD-SoC**: RoboSense E1 and Eocene (28 nm, wafer-level hybrid bonding), Hesai Picasso and FTX, Hesai Fermi C500, Adaps ADS6311 ("multiple foundries"), Huawei/HiSilicon.
- The only lidar receivers with a known fab are Sony's, made in Sony's own fabs.
- The claim that Chinese SPAD startups use Tower Semiconductor is **not verified**.
- On the RoboSense E1 lineage: joint development with Adaps ran from 2020 until early 2023, when it ended because pilot-run performance fell short. Adaps then taped out its own design (which became the ADS6311), and the two companies now sue each other [T].

**Bottom line.** Pattern (a) is **openly used Sony parts** in products described as SPAD-SoCs. Pattern (b) is **separate designs** ramping in 2026–27.
- No public evidence exists of Sony dies relabeled as in-house, or of Sony pixel wafers bonded to Chinese logic wafers.
- Sony is not known to sell SPAD pixel wafers.
- Foundry identities sit behind paywalled teardown die marks.

## C6. How far can SPAD-SoC receivers scale?

**Along the column axis they have scaled quickly.**
- PDE: 22–24% at 905 nm (2021) → 37% at 940 nm (2025) → more than 40% (2026).
- Channels: 128 → 520 → 2,160 → 4,320.
- Point rates: 25–41 Mpts/s.
- A column receiver uses only tens of mm² of pixel area. IMX479's pixel area is about 16.7 mm² [E].

**IMX479 is self-consistent** [E]:
- 1,568 × 10.08 µm = a 15.8 mm column.
- A 3×3 macro-pixel is 30.24 µm, so 0.05° per line needs $f\approx34.7$ mm, giving about 26° vertical.
- 120°/0.05° = 2,400 columns; at 20 fps that is 48k columns/s, or about 20.8 µs per column.
- At 300 m (2 µs round trip), that leaves at most about **10 shots per point** for histogramming.

**What limits further scaling**

**(a) Reticle** (about 26×33 mm):
- 2,160 lines fit on one die only at about **1 SPAD per line** (21.8 mm).
- With 3×3 binning, 2,160 lines would need a 65 mm column.
- 4,320 lines need pitch ≤7 µm, stitching, two dies, or interleaving. **Confirmed:** Hesai's Picasso supports 2,160 lines per chip, and the 4,320-line ETX uses **two chips** [T, Gasgoo/OFweek, Apr 2026]. That is consistent with this reticle argument.
- Single-SPAD channels collect 1/3–1/9 of a macro-pixel's photons and have far less dynamic range within one dead time.
- Huawei's **dual optical path** is an optical workaround: a telephoto receiver foveates the horizon band.

**(b) Photon budget:**
- At fixed average laser power, energy per point is $E=P/\dot N_{\rm pts}$, so for extended targets $R_{\max}\propto(P/\dot N_{\rm pts})^{1/2}$.
- Quadrupling the point count halves the 10%-target range, unless PDE, aperture or power rise.
- **Small-object detection improves:** signal-to-background scales as $1/\Omega_{\rm pix}$ once a target is sub-pixel. That is why vendors now quote "13×17 cm box at 150 m" metrics.
- Headline ranges are very probably quoted in binned or low-line modes [E].

**(c) Link budget example** [E], with a 25 mm aperture and 50% optics:
- At 200 m @10% and 0.1 µJ per point: about 21 detected photons at PDE 24%, about 33 at PDE 37%.
- At 25 Mpts/s with 0.1–0.3 µJ per point, average optical power is about 2.5–7.5 W. That strains 8–13 W electrical envelopes at 20–30% wall-plug efficiency.

**(d) Sunlight, dead time and pile-up (the dominant daytime limit)** [E]
- Assumptions: 25 mm aperture, 0.1°×0.05° field per macro-pixel, PDE 0.3, about 6 ns dead time.

| Case | Counts/s per macro-pixel | Fraction of time dead |
|---|---|---|
| 905 nm, 20 nm filter, ρ = 0.9 scene | about 2.2×10⁹ | **59%** |
| 905 nm, 40 nm filter (EEL-type) | about 4.4×10⁹ | 75% |
| 940 nm, 10 nm filter (VCSEL-type) | about 6×10⁸ | 29% |

- In a bright sunlit scene, SNR per bin is not the problem. **Dead time and pile-up** are: they skew histograms and cut effective PDE by up to half.
- Smaller pixels reduce background per pixel in proportion to solid angle, a genuine side benefit of the line-count race.

**(d′) How sunlight is mitigated: a layered toolbox** [E unless tagged]

The background rate per pixel scales as

$$B \propto E_{\odot}(\lambda)\,\Delta\lambda\;\frac{\rho_{\rm scene}}{\pi}\;\Omega_{\rm pix}\,A_{\rm ap}\,T_{\rm opt}\,\text{PDE}$$

Each mitigation attacks one factor, or changes how the detector responds to the remaining background. No single step is enough. Each gives roughly 2–100×, and they are stacked.

*Layer 1 — collect fewer background photons (optics)*
- **Narrow spectral filter ($\Delta\lambda$).** Background scales linearly with filter width, and the filter can be only as narrow as the laser's wavelength spread allows.
  - Over −40 to +105 °C (about 145 K), an EEL drifts about 0.25–0.3 nm/K, which is about 40 nm, so it needs a filter of about 40–50 nm.
  - A VCSEL drifts about 0.07 nm/K, about 10 nm, so it allows a 10–20 nm filter. That alone is a **2–4× background reduction**, and a main reason VCSELs displaced EELs.
- **Angle of incidence limits filter width, especially for wide-field receivers.** An interference filter blue-shifts as $\lambda(\theta)=\lambda_0\sqrt{1-(\sin\theta/n_{\rm eff})^2}$. With $n_{\rm eff}\approx1.8$ at 940 nm, the shift is about 4 nm at 10° but about **37 nm at 30°**.
  - Narrow filters must therefore sit in collimated or telecentric space, or the receiver's instantaneous field must be small.
  - A scanned column receiver can do that. A wide-FOV flash receiver cannot, which is another reason flash units are short-range.
- **Wavelength.** 940 nm sits in a water-vapour dip, with about 0.45–0.55× the solar irradiance of 905 nm. 1550 nm has about 0.35×, plus about 10× the eye-safe average power (§C4).
- **Small instantaneous field per pixel ($\Omega_{\rm pix}$).** Background scales with pixel solid angle.
  - Scanned receivers look only where the laser is pointing at that moment.
  - Addressable VCSEL "e-scan" systems enable only the SPAD zone matching the lit emitter zone.
  - Finer pixels from the line-count race help directly.
- **Baffles and hoods** against the sun directly in the FOV.

*Layer 2 — concentrate the signal in time*
- **Short, high-peak-power pulses.** Eye safety fixes the energy per pulse, not the peak power. Background per time bin scales with bin width, so shortening pulses (with bins to match) raises signal-to-background per bin roughly as $1/\tau_p$. Multi-junction EELs and VCSELs (3–5 junctions) give hundreds of watts peak in ns pulses.
- **Time gating.** SPADs are enabled only in a window around the expected return, so background photons arriving earlier don't leave the SPAD dead when the real return arrives. Gating also rejects near-field clutter, and "progressive gating" (EPFL) sweeps the window over range.

*Layer 3 — detection logic*
- **Coincidence detection.** A macro-pixel registers an event only if at least $k$ of its $N$ SPADs fire within a short window $\tau_c$. For uncorrelated background at per-SPAD rate $r$, the accidental $k$-fold rate is about $\binom{N}{k}\,k\,r^k\,\tau_c^{\,k-1}$. With $N=9$ and $\tau_c=1$ ns:

| Scene (3×3 macro-pixel background) | Per-SPAD $r$ | Singles | 2-fold | 3-fold | 4-fold |
|---|---|---|---|---|---|
| 940 nm, 20 nm filter, ρ = 0.1 ($1.35\times10^8$/s) | $1.5\times10^7$/s | $1.35\times10^8$ | $1.6\times10^7$ | $8.5\times10^5$ (**160×** lower) | $2.6\times10^4$ |
| 940 nm, 10 nm filter, ρ = 0.9 ($6.1\times10^8$/s) | $6.8\times10^7$/s | $6.1\times10^8$ | $3.3\times10^8$ | $7.9\times10^7$ (8×) | $1.1\times10^7$ (58×) |
| 905 nm, 20 nm filter, ρ = 0.9 ($2.2\times10^9$/s) | $2.4\times10^8$/s | $2.2\times10^9$ | no gain | no gain | no gain |

  - **Lesson 1:** coincidence works only once optics have made $r\tau_c\ll1$. In the brightest case ($r\tau_c\approx0.24$) it does almost nothing, so Layer 1 has to come first.
  - **Lesson 2:** coincidence costs sensitivity at long range. It needs at least $k$ signal photons within $\tau_c$. With a mean of 5 detected photons per shot, $P(\ge3)=0.88$; with a mean of 2, only $0.32$.
  - Hence **adaptive thresholds**: raise $k$ in bright sun, lower it in darkness and for weak far returns. This is conceptually what IMX479's pixel-level threshold control and RoboSense's multi-threshold TDC do [T/I]. Sony's ISSCC 2021 receiver demonstrated 150 m @10% at 117 klux [P].
- **Shorter dead time (active recharge).** The dead fraction of a non-paralyzable SPAD is $r\tau_d/(1+r\tau_d)$. In the bright 940 nm/10 nm case: 58% at 20 ns, 29% at 6 ns (Sony's quoted response), 17% at 3 ns. The trade-off is more afterpulsing.
- **More SPADs per channel.** Larger macro-pixels, up to the SiPM limit of hundreds of cells (§C4b), add parallel cells, so some are always armed when the return arrives. The price is resolution.

*Layer 4 — statistics and processing*
- **Multi-shot TCSPC histograms** with matched filtering and constant-false-alarm-rate peak detection. Background forms a flat floor that averages down as $\sqrt{N_{\rm shots}}$.
- **Pile-up correction.** Coates' correction (1968) reconstructs the true arrival histogram from the first-photon-biased one. Research methods go further: asynchronous or shifted gating, and deliberately attenuating flux to the optimal level (Gupta et al., CVPR 2019 / ICCV 2019) [U: check the references].
- **Point-level confidence and spatio-temporal filtering** drop low-confidence returns caused by sunlight noise.

*Layer 5 — system architecture*
- **Adaptive exposure within eye safety.** Concentrate energy on regions of interest, or trade point rate and frame rate for more energy per point in bright conditions. Hesai's AT128 prospectus describes ASIC-driven addressable laser channels with "dynamic exposure" [P].
- **SiPM receivers** tolerate sunlight better per channel, because background is spread over about $10^3$ cells (§C4b).
- **1550 nm ToF:** about 10× the eye-safe average power and about 3× less sunlight, at 2–3× the cost.
- **FMCW coherent detection is the fundamental fix.** Only light in the local oscillator's spatial mode and IF bandwidth mixes.
  - Example: a sunlit ρ = 0.5 surface at 1550 nm, in one spatial mode ($A\Omega\approx\lambda^2$) and a 200 MHz IF bandwidth ($\Delta\lambda\approx1.6$ pm), contributes only about $10^3$ photons/s.
  - That is 5–6 orders of magnitude below a ToF macro-pixel's $10^8$–$10^9$/s, and negligible against local-oscillator shot noise.
  - The price is FMCW's cost and point-rate penalties (§C7).

*How it shows up in specs.* Vendors quote range at a stated ambient level. Seyond Falcon K2: 250 m @10% at 100 klx, $P_d$ > 90% [P]; Sony ISSCC 2021: 150 m @10% at 117 klux [P]. **The sun directly in the field of view** still blinds affected columns for a moment. Systems blank or flag those regions and rely on other sensors meanwhile.

**(e) Histogram memory:**
- Full 300 m / 5 cm histograms are 6,000 bins × 10 bits = 60 kbit per pixel.
  - One 520-pixel column: about 31 Mbit.
  - A **staring 520k-pixel array: about 31 Gbit, which is impossible.**
- The answers are equivalent-time sampling plus compression (Sony, about 98%), partial histograms and peak tracking.
- **Manageable in a scanned column; prohibitive in a staring 2D array** without zone multiplexing.

**(f) Avalanche power:**
- Each avalanche costs about $C\,V_{\rm ex}(V_{\rm bd}+V_{\rm ex})\approx1.6$–3.9 pJ.
- A scanned column dissipates about 0.2–0.55 W in sunlight; a staring VGA SPAD array about **5–12 W**.
- So 2D arrays must enable only the illuminated zone.

**(g) Cost.**
- NE Times: SPAD-SoC beats SiPM above about 200 lines.
- RoboSense claims about 50% cost reduction for its monolithic Phoenix.
- The SPAD layer stays on mature nodes; the logic layer advances for SRAM and DSP.

**Can a fully solid-state 2D addressable VCSEL × SPAD "electronic scan" reach long range over a wide field?**

Shipping products, using the figure of merit $R_{10\%}^2\cdot\text{FOV}$ [P data, E figure of merit]:

| Product | FOV | Range @10% | $R^2\cdot$FOV (m²·deg²) |
|---|---|---|---|
| Hesai FTX-140 (solid-state) | 140°×105° | 30 m | 1.3×10⁷ |
| RoboSense E1 (solid-state) | 120°×90° | 30 m | 9.7×10⁶ |
| Seyond Hummingbird D1 (solid-state) | 140°×100° | 30 m | 1.26×10⁷ |
| **Opsys ALTOS 70 / 150 / 300** (same design, different optics) | 80°×22° / 45°×13° / 22.5°×6.5° | 55 / 100 / 200 m | **5.3 / 5.85 / 5.85 ×10⁶** (constant) |
| Hesai ATX (1 scan axis) | 120°×20° | 230 m | 1.3×10⁸ |
| Seyond Falcon K2 (1550 nm, 2-axis) | 120°×25° | 250 m | 1.9×10⁸ |
| RoboSense EM4 (1 scan axis) | 120°×27° | 300 m (basis unclear) | about 2.9×10⁸ |

- Opsys keeps $R^2\cdot$FOV constant to within about 10%. Scaled to 120°×25°, its photon budget would give **about 44 m @10%** [E].

**The physics behind it: receive étendue and silicon area** [E]
- Take IMX479's 15.8 mm array at f/1.2:
  - covering a 26° axis (scanned column): $f\approx34$ mm, aperture $D\approx28.5$ mm;
  - staring over 120°: $f\approx4.6$ mm, $D\approx3.8$ mm.
  - That is about **1.8% of the collecting area**, roughly **7.5× less range** for the same photons.
- Keeping 0.05° over 120°×26° with a staring array of 3×3×10 µm macro-pixels needs a **72.6×15.7 mm (about 1,141 mm²) SPAD array**. That is above the reticle and about 68× IMX479.
- The emitter is not the bottleneck: addressable VCSEL zones concentrate energy as well as a scanner does.
- **Binding constraints, in order:** (1) receive étendue and aperture; (2) silicon area; (3) histogram memory for parallel readout; (4) background avalanche power.
- **A mechanical one-axis scanner is the cheapest optical multiplexer.** It shares one small column across about 2,400 horizontal positions while keeping a large aperture.
- **Industry evidence:** every long-range "digital" product shipping or announced keeps one moving axis (Hesai ETX and ATX, RoboSense EM4 and Phoenix units, Huawei 896, Seyond Robin E2).

**What could break this** [E]:
1. Tiling narrow-field solid-state modules (about 20× ALTOS 300 to cover 120°×25°), which is a cost problem.
2. Smaller SPAD pitch (5 µm) with high NIR PDE on stitched or three-layer stacks.
3. **Non-mechanical steering of the receive path** feeding a small detector from a large aperture: OPA, LC metasurfaces (Lumotive), LC polarization gratings, or wavelength steering. **This is the missing component.**
4. Coherent (FMCW) detection, which removes the sunlight and pile-up problem but brings back 1550 nm and the same steering need.

## C7. FMCW and non-mechanical beam steering

### Commercial status

- **Passenger cars: zero series production.** Yole had said FMCW would not enter automotive "before 2028" [T]. The first passenger-car design win is **Aeva with an unnamed top-10 European OEM, L3, SOP 2028** (announced 3 Dec 2025) [P].
- **Trucks, the only foothold:**
  - **Aurora FirstLight:**
    - Driverless commercial service since 1 May 2025.
    - About 25 driverless trucks mid-2026 across all generations; 200 targeted by year-end 2026 (about \$80 M annualized revenue).
    - More than 500k driverless miles by Sep 2026.
    - Gen 2 claims **1,000 m detection**. Its photonic engine uses SiN waveguides, a III-V laser, custom SOAs and custom photodiodes, fiber-free, with the kit built by **Fabrinet**.
    - Gen 3 with Aumovio in 2027, "for tens of thousands of trucks".
    - Q2 2026: revenue \$2 M, net loss \$270 M, about \$1.2 B cash [P].
  - **Aeva:**
    - Exclusive long-range lidar for **Daimler Truck/Torc**: C-samples delivered May 2026; Jabil automated line of about 100k per year; Daimler launch 2027.
    - **Bendix** L2+ truck ADAS.
    - Atlas Ultra: 250 m on low-reflectivity targets, up to 150° horizontal FOV, ASIL-B(D).
    - Wavelength and scanner type not disclosed [P].
- **Attrition:**
  - **Mobileye** ended its Intel-SiPh FMCW program in Sep 2024. Reasons given: EyeQ6 vision progress, in-house imaging radar, and "better-than-expected cost reductions in third-party time-of-flight lidar" [P].
  - **Scantinel** went insolvent in Aug 2025; assets to MicroVision.
  - **Baraja** (wavelength steering) cut staff 75% in 2023; patents for sale in 2025.
  - **Quanergy** (OPA) filed Chapter 11 in 2022.
  - **Analog Photonics** (OPA with electro-optic phase shifters, 1.5 µm pitch, about 60°) has no production award found.
- **Pivots to industrial and security** (the route Yole predicted):
  - **SiLC:** Eyeonic line; 1 km claims; Honda investment.
  - **Voyant:** Carbon at \$1,490, 1-axis on-chip steering + slow mirror; Helium 2D solid-state FPA.
  - **LightIC:** Lark; Tower foundry; indie SoC.
- **China:**
  - **LuminWave:** III-V-on-Si fully integrated chip with >10 GHz FM bandwidth; heavy-truck nomination.
  - **Moore Photonics:** company claims; no independent data found.
  - **No FMCW product from Hesai, RoboSense or Huawei**, although Hesai holds FMCW, OPA and metasurface patents.
- **Non-mechanical steering in production:**
  - flash/SPAD solid-state units (blind spot);
  - **Lumotive** LCM in an industrial ToF sensor (Hokuyo YLM-10LX3, 2024; 180°×140° platform at ≤50 m, 2026).
  - No OPA or wavelength-steered scanner is in automotive series production.

### Physics constraints for FMCW [E]

**Coherence.** The round trip must sit within the coherence length. For a Lorentzian line, $L_c=c/(\pi\Delta\nu)$. At 300 m range (600 m round trip) this needs $\Delta\nu\lesssim c/(600\pi)\approx160$ kHz, before chirp-nonlinearity and phase-noise budgets.

**Beat frequency and ADC load.**

$$f_b=\frac{2BR}{cT}$$

For $B=1$ GHz (range resolution $c/2B=15$ cm), $T=10$ µs and $R=300$ m, $f_b\approx200$ MHz per channel.

**Doppler.** $f_D=2v/\lambda\approx1.29$ MHz per m/s at 1550 nm. At a 50 m/s closing speed that adds about 65 MHz, requiring up/down chirps or other disambiguation.

**Point rate.**
- Each point needs a dwell of about $T_{\rm up}+T_{\rm down}$ (several µs to tens of µs).
- So pts/s ≈ $M/T_{\rm dwell}$. Reaching 2–4 Mpts/s needs **tens of parallel coherent channels**, each with its own 100–400 MHz ADC path.
- Shorter chirps raise $f_b\propto1/T$.
- This **throughput problem** is why photonic integration (many LO-matched receivers on one PIC) is the whole game.

**Single-mode étendue (antenna theorem).**
- Coherent detection needs mode matching: $A_{\rm eff}\,\Omega\approx\lambda^2$.
- For a beam filling a 0.1° cell ($\Omega\approx3\times10^{-6}$ sr), $A_{\rm eff}\approx(1.55\ \mu\text{m})^2/3\times10^{-6}\approx8\times10^{-7}$ m², i.e. an aperture of about **1 mm**.
- Using a larger aperture narrows the beam, which then **under-fills** each angular cell (sparse sampling).
- Incoherent ToF has no such constraint: a large aperture plus a pixel-defined IFOV.
- Coherent shot-noise-limited gain has to compensate for the smaller collection area.

**Speckle.** Single-mode detection of rough targets gives Rayleigh-distributed amplitude with deep fades. Polarization, wavelength or spatial diversity is needed for high detection probability. Multimode ToF receivers average over many speckle cells.

**Benefits.**
- Per-point radial velocity (lower prediction latency);
- intrinsic rejection of sunlight and other lidars (only LO-matched light within the IF bandwidth mixes; not absolute — FMCW interference modes exist);
- no retroreflector blooming (a vendor claim).

**OPA arithmetic** [E]:
- The grating-lobe-free steering range is $\pm\arcsin(\lambda/2d)$. At $d=1.5$ µm that is about ±31° (Analog Photonics' "about 60°" matches).
- Element count for beamwidth $\theta$: $N\approx\lambda/(d\,\theta)$, about **590 elements for 0.1°** and about 1,200 for 0.05°, each with calibrated phase control.
- The orthogonal axis is usually wavelength-steered with grating emitters (about 0.1–0.2°/nm in Si), which needs tens of nm of tuning alongside the chirp.
- Receive-side OPA efficiency and aperture are the hard part.

### What would make FMCW or OPA matter

The single most valuable technical advance, for both ToF and FMCW, is a **large-aperture, low-loss, fast, non-mechanical steerer usable on receive**. Next come:
- **coherent focal-plane arrays** with many parallel LO-matched pixels (the Voyant Helium direction), which fix point rate;
- **integrated narrow-linewidth chirped lasers + SOAs** on SiN or TFLN at automotive cost;
- speckle diversity built into the PIC.

The cost bar is about **\$300–500 for trucks and L3** and about **\$200 for passenger L2++**, and SPAD ToF keeps raising the performance bar (40 Mpts/s, 45% PDE).

---

# Part D — Supply chain and geopolitics

## D1. Component dependency map (Chinese automotive lidar)

| Component | Western / JP suppliers | Chinese alternatives | Substitution status (2026) | Exposure |
|---|---|---|---|---|
| 905/940 nm multi-junction VCSEL arrays | Lumentum (AT128 era), ams OSRAM, Coherent, Trumpf | Hesai's own VCSEL fabbed at **立昂东芯 (Lion Dongxin)**; **纵慧芯光 Vertilite** (investors include Huawei Hubble, BYD, Xiaomi, DJI, Hesai, RoboSense); **长光华芯 Everbright**; 瑞识 | **Largely substituted** on newer platforms [P/T] | GaAs substrate/epi upstream |
| 905 nm multi-junction EEL | ams OSRAM SPL (RoboSense M1/M2/MX as of 2024) | Everbright, Raybow and others | Partial | ams OSRAM depends on China more: **Greater China was 40.8% of its 2025 revenue** [P] |
| GaAs / InP substrates, epi | Sumitomo, Freiberger, JX; AXT (US-listed, China fabs); IQE and others | Tongmei (AXT's China subsidiary), Vital, Yunnan Xinyao | China self-sufficient | **China export-licenses GaAs (since Aug 2023) and InP (since Feb 2025)**. AXT permit shortfalls cut InP revenue from \$13.1 M to \$8 M in Q4 2025. No permit needed for domestic sales [P/T] |
| 1550 nm fiber laser / InGaAs | Hamamatsu and others | 光库 Advanced Fiber Resources | Unclear | Niche |
| SPAD / SPAD-SoC | **Sony IMX459 / IMX479**; STMicro | RoboSense in-house; Hesai (Fastree3D); Adaps, Fortsense, VisionICs | **In transition** (§C5) | **The largest remaining foreign dependency** (Japan has no controls on these) |
| SiPM | onsemi (AT128; also InnovizOne's ArrayRDM-0112), Hamamatsu | Hesai claims an in-house receiver; Adaps | **ATX: 17 SiPM dies × 4 channels, vendor not public** (in paywalled TechInsights DDT-2505-806); no onsemi link found; in-house likely but unconfirmed | Moderate |
| FPGA / controller | **AMD/Xilinx** (the most common across 26 teardowns), Lattice (Huawei 96-line), **Efinix** (US; found in the ATX teardown together with an Infineon MCU and TI power ICs) | **Hesai Fermi C500** RISC-V SoC (SOP Apr 2026); RoboSense in-house; Huawei SoC | **Being designed out, 2025–27** | High only if the Entity List or FDPR were applied (they have not been) |
| MCU, analog, power | TI, Infineon (ATX), ST | 3peak and others | Mixed | Moderate |
| Motor drivers; magnets | MPS, TI drivers | NdFeB magnets and motors Chinese | Drivers still US | China's rare-earth leverage |
| Optics, filters, windows | Schott, Hoya, Viavi | Sunny, Crystal-Optech, Focuslight | Localized | Low |

**How localization progressed.**
- **Yole's teardown of the Hesai AT128 (Li Auto L9):**
  - 128 Lumentum 5-junction VCSELs, an onsemi SiPM and a Xilinx FPGA;
  - **Xilinx was 33% of component cost**;
  - **72% of component value came from US companies and 11% from Chinese ones**, the latter almost entirely Hesai's own ASICs [I].
- **By 2025–26:**
  - Hesai says it designs all **seven key components** (laser, detector, driver, AFE, ADC, DSP, controller) and has shipped 185–230 M in-house chips;
  - its **largest single supplier was 4.6% of 2025 purchases**, and the top five 20.5% [P].
- **Revenue exposure of Western suppliers:**
  - Lumentum: mainland China about 9.4% of FY2026 revenue, likely datacom-driven;
  - Coherent: about 11.7% in FY2025 [P, via search summaries];
  - neither breaks out lidar.

## D2. Chinese export controls

**Materials.** China holds 98% of primary Ga, 77% of refined Ge and 68% of refined In [I, USGS MCS 2026].

| Date | Chinese measure | Status (Sep 2026) |
|---|---|---|
| 1 Aug 2023 | Ga/Ge licensing (includes GaAs) | In force |
| 21 Dec 2023 | Technology export catalogue: **lidar system technology restricted** above extreme thresholds (e.g. >2 km range, <20 µrad resolution) | In force; automotive lidar falls below the thresholds |
| 3 Dec 2024 | Dual-use ban to US military end users; **Ga/Ge/Sb export ban to the US** | Ban **suspended to 27 Nov 2026** |
| 4 Feb 2025 | W, Te, Bi, Mo, **In** (includes InP) | In force |
| 4 Apr 2025 | Rare earths + magnets | In force (general licences to major magnet makers from Dec 2025) |
| 9 Oct 2025 | Extraterritorial 0.1% de minimis rare-earth rule, and more | **Suspended to 10 Nov 2026** |
| 6 Jan 2026 | Dual-use ban for Japanese military end use | In force |

**Effects.**
- **Licensing, rather than outright bans, is the main instrument.** Most measures require export licences, which can be granted slowly or selectively. That creates supply uncertainty rather than a hard stop.
  - The clearest evidence is at **AXT**, a US-listed maker of GaAs and InP substrates whose fabs are in China (Tongmei). InP permits came in below expectations in Q4 2025 and InP revenue fell from \$13.1 M to \$8 M; GaAs permits "came in light" in Q1 2026 [P/T].
  - Western VCSEL and EEL makers that rely on China-made substrates therefore face lead-time and allocation risk. Alternatives outside China exist (Freiberger in Germany; Sumitomo and JX in Japan), but capacity is limited and prices are higher.
- **Gallium** is the deepest dependency, since China produces about 98% of primary Ga. Western recovery (for example as a by-product of alumina refining) is only starting.
- **Rare earths and magnets.** Lidar polygon and spindle motors and voice-coil actuators use small NdFeB magnets.
  - The April 2025 controls caused real stoppages in carmaking: Ford idled its Chicago Explorer plant in May 2025, and Suzuki halted Swift production [T].
  - US imports of yttrium collapsed to 17 t (Apr–Dec 2025), against 333 t before the controls (CSIS) [T].
  - **For 1550 nm fiber lasers and EDFAs**, erbium and ytterbium dopants are also rare earths. Whether they were part of the suspended Oct 2025 package was not checked in this draft [U].
- **The asymmetry.** Chinese lidar makers buy magnets, III-V substrates and optics domestically without permits. Western lines in Thailand, Germany and the US do not have that advantage.
- **The Nov 2026 cliff.** If the suspensions lapse (10 Nov for the Oct 2025 rare-earth package, 27 Nov for the Ga/Ge/Sb ban to the US):
  - the extraterritorial 0.1% de minimis rare-earth rule would return, reaching products made *outside* China that contain Chinese-origin rare earths, including Western lidar assembled in Thailand;
  - the US-specific Ga/Ge/Sb ban would resume.
  - If instead they are extended as part of a trade arrangement, the status quo of permit friction continues.
- **Germanium** ties directly into thermal-camera optics (§A4). Chalcogenide glass and recycling are the Western mitigations.

## D3. US actions

**Timeline**
- **2023:** Ouster's ITC and Delaware case against Hesai ends in arbitration. The **final award (Sep 2025) gave Hesai about \$6.4 M in costs**; the case was dismissed without conditions [P].
- **Jan 2024:** Hesai added to the DoD **1260H** list. It was redesignated in Oct 2024 and DoD won in district court (Jul 2025).
  - **18 Aug 2026: the D.C. Circuit reversed on due process**, remanded **without vacatur**. Hesai stays on the list and was relisted in 2026 [I].
- **FY2025 NDAA §164:** DoD may not procure or operate Chinese lidar (Hesai named) **from 30 Jun 2026** [I].
- **16 Jan 2025, BIS connected-vehicle rule:** Chinese VCS/ADS software banned from MY2027 and hardware from MY2030. **Lidar is explicitly excluded** [I].
- **8–10 Jun 2026: RoboSense added to the 1260H list**; Hesai retained. The §805 ban on *products* of listed firms starts **30 Jun 2027** [I].
- **Tariffs:**
  - Lidar (HTS 9015.80.20) has carried a 25% Section 301 List 1 tariff since 2018.
  - IEEPA tariffs were struck down by the Supreme Court (20 Feb 2026).
  - A new 12.5% "forced-labour" §301 (24 Jul 2026) brings the aggregate to **about 37.5% plus MFN** [T/E].
- **Bills:**
  - **Connected Vehicle Security Act S.4429:** permanent ban on connected-vehicle hardware and software linked to a "foreign adversary" (the bill's term) plus a 15% ownership cap; **passed Senate Commerce unanimously on 22 Jul 2026**; Hesai cited as covered.
  - **SAFE LiDAR Act (H.R. 6576):** would ban purchases of lidar from "foreign adversary" countries (the bill's term) within 3 years.
  - **S.4000:** DOT procurement ban.
  - None enacted.
- **Idaho National Laboratory** testing of Chinese lidar (Aug 2026). Lawmakers raised cyber-risk concerns over Hesai's NVIDIA Hyperion role (Jul 2026) [T].
- **States:** Aurora's 10-K flags state bills conditioning the use of Chinese lidar in AVs; none enacted found [P].
- **Allies:** no EU, Japan or Korea bans found.

## D4. Chinese responses

- **Hesai:**
  - North America was **14.9% of 2025 revenue** (RMB 451.7 M), **up** despite the 1260H listing; Europe 4.6%.
  - **Thailand "Galileo" plant** (Bangkok; Mercedes L3 supply for Europe and China). At CES in Jan 2026 Hesai guided start of production for "early 2027". Its Q2 2026 release says it "operates in-house factories in China and Thailand", but **no volume production has been announced**, so it is most likely at setup or pilot stage [P/E].
  - HK dual listing Sep 2025 (about \$614 M net).
  - Capacity above 4 M per year in 2026 [P].
- **RoboSense:** first overseas plant in Southeast Asia (H2 2026), requested by customers because of tariff and US–China risk. Overseas revenue up 90%; 33 overseas design wins [P/T].
- **Upstream integration:** Hesai–Fastree3D; RoboSense's own SPAD and VCSEL; Huawei Hubble stakes in Vertilite, Everbright and VisionICs.
- **Limit of offshore plants:** they address tariffs, not "developed by" or ownership clauses like those in S.4429 or 1260H §805 [E].

## D5. Western lidar supply-chain resilience

**Where Western lidar is built:**
- **Thailand contract manufacturing is the hub:** Fabrinet (Innoviz, Ouster, Aeva, Aurora gen 2) and Benchmark (Ouster).
  - **Why Thailand:** Fabrinet's precision-optics and photonics assembly expertise (it also builds optical transceivers), non-China origin for US tariffs, and a location in a long-standing US treaty ally.
  - **The risk:** a single-country concentration still sits close to Chinese component supply chains.
- **Other sites:** Valeo Wemding (Germany), Jabil's automated Atlas line for Aeva (US, about 100k per year), Aumovio for Aurora gen 3 (New Braunfels, Texas, 2027), LG Innotek for Aeva's passenger-car Atlas Ultra (from about 2027), and Ouster's small San Francisco line for Buy-America units.

**Where it still depends on China:**
- Ga, Ge and In feedstock; GaAs and InP substrates (via AXT's China fabs, or scarcer non-China capacity); rare-earth magnets.
- Many optical parts: Chinese lens, filter and line-beam optics suppliers also ship to Western lidar makers. Focuslight reports a line-beam module for an unnamed foreign "AG" customer [T].
- I found no detailed China-sourcing disclosures in Western lidar 10-Ks.

**The scale gap:**
- All non-Chinese automotive lidar makers together ship **well under 5% of global units**.
- That means higher unit costs (Yole 2024 ASP: \$700–1,000 outside China vs \$450–500 in China), less learning-curve benefit, and thinner balance sheets (§B3, §G2).

**What buyers say:**
- Rivian's CEO said all realistic low-hundreds-of-dollars lidar options are Chinese.
- Rivian explored US production through Chinese-linked partnerships. Reuters reported it; the CFO later called the headline erroneous [T].
- This is the clearest buyer statement that US lidar would cost more without Chinese suppliers; the ASP gap in §B1 suggests about double.

## D6. Chokepoints, ranked (my judgement)

**Chinese makers' dependence on Western and Japanese inputs** (ordered by potential impact)
1. **Foundry and EDA access (latent, potentially the strongest).**
   - The new in-house SPAD-SoCs and ASICs (RoboSense Phoenix at 28 nm with hybrid bonding, Hesai Picasso and Fermi C500) must be fabbed somewhere, and **no foundry is publicly named** (§C5).
   - If any use TSMC, UMC or other non-Chinese fabs, or US-origin EDA tools (as almost all chip designers do), an Entity List designation or a Foreign Direct Product Rule extension could disrupt them.
   - **Why latent:** the US has used procurement bans (1260H, NDAA) against Chinese lidar, not export controls, and the Nov 2023 congressional request to consider Entity List action has not been acted on.
   - **Mitigation for China:** domestic fabs with 3D-stacking capability (XMC, Huali, SMIC) exist, but a switch would take one to two years of requalification [E].
2. **Sony SPADs (real today, uncontrolled).**
   - The 192-line (IMX459) and 520-line (IMX479) classes largely use Sony parts: Huawei 96/192-line, and very likely the RoboSense EM4-520.
   - Japan has no controls on them.
   - In-house replacements (Phoenix, Picasso, Adaps) reach mass production in 2026–27, so this lever weakens every quarter.
3. **FPGAs and US analog parts (being designed out).**
   - AMD/Xilinx and Lattice FPGAs appear widely in teardowns; the ATX also uses a US Efinix FPGA, plus TI power parts and an Infineon MCU.
   - Hesai's Fermi C500 RISC-V SoC and RoboSense's in-house processors are replacing FPGAs from 2025–27.
   - TI and ADI analog parts are easy to second-source from Chinese suppliers (for example 3peak).
4. **EELs and SiPMs (substitutable).**
   - ams OSRAM EELs (RoboSense M-series) and onsemi SiPMs (AT128) have Chinese alternatives: Everbright, Raybow and in-house designs.
   - ams OSRAM itself depends on China for 40.8% of its revenue, so the leverage partly runs the other way.
5. **VCSELs (already localized).** Hesai's VCSEL is fabbed at Lion Dongxin, and Vertilite and Everbright supply others. Lumentum was the AT128-era supplier.

**US demand leverage** is modest: North America was about 15% of Hesai's 2025 revenue, and bans so far cover DoD procurement only. It would become significant only if S.4429 or a similar civilian ban passes (§F3), and even then it would mostly hit robotaxi and truck fleets and a few Western OEM programs, not Chinese domestic volume.

**Western makers' dependence on Chinese inputs** (ordered by potential impact)
1. **Ga/Ge/In feedstock and GaAs/InP substrates.** Permit friction is already visible at AXT. Every Western VCSEL, EEL and InGaAs detector ultimately needs these, and non-China substrate capacity is limited.
2. **Rare-earth magnets.** They are small in lidar (motors, actuators), but the April 2025 controls showed they can stop car plants. The suspended extraterritorial rule would reach Western lidar assembled outside China.
3. **Germanium IR optics.** Mainly a thermal-camera exposure (§A4), mitigated by chalcogenide glass.
4. **The finished product itself.**
   - Chinese suppliers hold about 95% of global automotive lidar share.
   - Western carmakers (Mercedes, the VW, Toyota and Nissan joint ventures) buy Chinese lidar at scale (§B6).
   - The Western supplier base is thin: Luminar liquidated, Ibeo and Quanergy earlier (§G2).
   - In a severe decoupling, the West would lack capacity rather than technology.

**Dates to watch**
- **10 Nov and 27 Nov 2026:** Chinese suspensions expire.
- Hesai's DoD remand.
- Senate floor vote on S.4429.
- **30 Jun 2027:** DoD products ban.
- BIS commercial-vehicle rule.
- Hesai and RoboSense Southeast Asia plants.

---

# Part E — Can camera-only or camera+radar solve autonomous driving?

## E1. Positions and deployment scale

| Company | Sensor philosophy | Deployment scale (latest) | Key evidence |
|---|---|---|---|
| **Tesla** | Camera-only (8 cameras); radar removed 2021–22; HD radar on S/X unused | **FSD (Supervised):** about 12 B cumulative miles, 1.48 M subscriptions (Q2 2026) [P]. **Robotaxi:** unsupervised in 6 metros (TX, FL); Bay Area with safety drivers; **1 M unsupervised miles** (3 Sep 2026) [P]. 546 registered in Texas (26 Sep); active unsupervised fleet contested (Austin 7-day average of 8 per a tracker, vs "nearly 200" per Teslarati) [I/T]. Cybercab production started; NHTSA audit query AQ26002 | [P] 5.3 M miles per major collision vs 660k US average (method caveats: crashes counted if the system was active within 5 s of impact; younger fleet than the US average). [I] NHTSA **EA26002** on 3.2 M vehicles for reduced visibility, requesting an internal Tesla document titled **"Radar Saves Us"**; PE25012 (red lights); 17–22 robotaxi crash reports; \$243 M Benavides verdict. [I] **IIHS TSP+ 2026 Model Y; top performer in the Dongchedi 2025 test; AAA night test 4/5** |
| **Waymo** | 13 cameras + 4 lidar + 6 radar + audio (6th gen) | **271.3 M rider-only miles (to Jun 2026)**; about 4,000 vehicles; about 500k paid rides per week; 15 US metros | [P] −95% serious injury (about 3 observed vs about 58 expected), −82% injury, −93% pedestrian injury. **[I] IIHS: −68% crashes per mile** (Phoenix −76%, SF −35%, Austin +4% on a small sample). Recalls: school buses, floods, construction zones |
| **Mobileye** | Camera-first; eyes-off adds an independent radar+lidar channel ("True Redundancy") | SuperVision about 300k on road; Chauffeur has a front lidar; Drive uses Innoviz lidars; imaging radar SOP 2028 | Ended its FMCW program. Safety paper: joint MTBF of at least $180\,T_1T_2$ |
| **Xpeng** | Camera + radar, no lidar (since late 2024) | Whole consumer lineup; robotaxi employee testing (Jul 2026) | "The auto industry no longer needs" lidar (He Xiaopeng, May 2026) |
| **Huawei ADS** | Lidar + 4D radar (up to 4 lidars; 896-line); SE tier without lidar | More than 2 M vehicles; 14.5 B km [P] | L3 permit (Arcfox Alpha S) |
| **BYD God's Eye** | Tiered: A = 3 lidars, B = 1–2, C = vision-only; lidar ¥12k option on all models | 3.15 M assisted-driving cars (May 2026) | In-house 4D radar, 0.8° |
| **Li Auto / Xiaomi / NIO** | Lidar standard or near-standard (2025–26) | — | Fatal NOA crash of a Xiaomi SU7 Standard, the camera-only trim (Mar 2025); the sensor set's role is not established here |
| **GM / Ford / BMW / Mercedes** | L2 camera + radar; eyes-off plans with lidar (GM; Mercedes with Hesai); Ford L3 sensors undisclosed | Super Cruise 1 B miles; BlueCruise 1.2 M vehicles | NTSB on BlueCruise; IIHS safeguard ratings mostly Poor |
| **Rivian / Nissan–Wayve / NVIDIA** | Adding lidar (R2 Gen 3; ProPILOT; **Hyperion 10 = 14 cameras, 9 radars, 1 lidar**) | — | Wayve's London Mach-E has no lidar; its Nissan programs do |

**The factual pattern.**
- Only Tesla (and Xpeng) ship camera-only driving with no lidar tier.
- Almost everyone ships **no-lidar L2/L2++**: Huawei SE, BYD C, Mercedes CLA, BMW iX3, Mobileye SuperVision.
- **Every announced production eyes-off (L3) or driverless (L4) program uses lidar**, except Tesla and Xpeng's robotaxi. The contested case is Changan's SL03 L3 permit.

## E2. Physics

**Stereo depth error** $\sigma_Z\approx Z^2\sigma_d/(fB)$ [E]. Values are shown as $\sigma_d$ = 0.25 px / 0.5 px.

| Configuration | 100 m | 200 m | 400 m |
|---|---|---|---|
| ADAS stereo, B = 0.20 m, 1920 px / 50° | 6.1 m (6%) / 12.1 m | 24 m (12%) / 49 m | 97 m / 194 m |
| B = 0.35 m (EyeSight-class) | 3.5 m / 6.9 m | 13.9 m / 27.8 m | 56 m / 111 m |
| Wide baseline, B = 1.2 m, 3840 px / 30° | 0.29 m / 0.58 m | 1.2 m / 2.3 m | 4.7 m / 9.3 m |
| Human eyes, B = 0.065 m, 20″ stereoacuity | 15 m (15%) | 60 m (30%) | 239 m |

- Wide baselines move the problem to calibration: about 35 µrad of relative orientation must stay stable across a flexing body (NODAR's core IP).
- **Humans don't use stereo at driving ranges**, which matters for the "humans drive with two eyes" argument.

**Monocular ground-plane depth.** $Z=h/\tan\theta$, so $\partial Z/\partial\theta\approx-Z^2/h$.
- With $h=1.5$ m, a **0.1° pitch error moves an object at 200 m by about 61 m**. Braking pitch and road slope reach 0.1–0.5°.

**Radar is diffraction-limited.** $\theta\approx\lambda/D$ at 77 GHz ($\lambda=3.9$ mm):
- 1° needs a 0.22 m virtual aperture; **0.1° would need 2.2 m**.
- Best 4D radars are about 0.5–1°. At 200–400 m a 1° cell (3.5–7 m) is **wider than a lane**.

**Lidar** gives cm-level direct range but samples sparsely: 0.05–0.2°, about 28 points on a pedestrian at 200 m at 0.05°.

**In one line:** camera is weak in range, lidar in sampling density, radar in angle.

## E3. Benchmarks

**nuScenes test** (≤50 m, lenient center-distance matching):
- best camera-only NDS about **70.9** (RoPETR, 2025);
- lidar-only 73.9 (LION, 2024);
- fusion 77.0 (SparseLIF, 2024).
- The camera–lidar gap shrank from about 25 points (2020) to about 3 (2025). Camera mATE is still about 0.38 m vs 0.24 m for fusion [I].

**Waymo Open (2022 models), vehicle 3D AP by distance:**

| Distance | BEVFormer (camera) | PointPillars (lidar) |
|---|---|---|
| 0–30 m | 79.7 | 88.2 |
| 30–50 m | 47.2 | 76.4 |
| **>50 m** | **20.5** | **58.4** |

- With a 10% longitudinal tolerance the camera matches: **camera error is almost purely depth**, and it grows with range [I].

**Argoverse 2 (150 m):** camera Far3D 0.316 mAP vs lidar LION 0.415; camera translation error 1.5–1.7× worse.

**End-to-end planning (NAVSIM):** camera-only 83.8 vs camera+lidar 84.0 PDMS. The benchmark is non-reactive and dominated by common scenarios; it says nothing about the tail.

## E4. Weather: which sensor gives real diversity

| Condition | Camera | Lidar | Radar |
|---|---|---|---|
| Dense fog | Reach ≈ V | Reach ≈ 0.6–1 V, plus near clutter | Largely unaffected |
| Heavy snow / sleet (K-Radar AP3D) | occluded | 29.7 / 22.7 (vs 52.3 normal) | **44.5 / 41.5** (vs 49.9) |
| Night | Headlight-limited | Unaffected | Unaffected |
| Low sun / glare | Weak | Some sunlight noise | Unaffected |
| Stationary unusual objects | Prior-dependent | **Strong** (category-agnostic geometry) | Weak (elevation, clutter) |

**Key point.** Camera and lidar **share** a failure mode in fog. **Radar is the orthogonal weather channel. Lidar is the orthogonal channel for darkness, geometry and unusual stationary objects.**

## E5. Safety-engineering arithmetic

**RAND "Driving to Safety"** (2016):
- 275 M failure-free miles to show ≤1.09 fatalities per 100 M miles at 95% confidence;
- about 8.8 B miles to pin the fatality rate within ±20%;
- about 5 B miles to show a 20% improvement.
- Waymo is near 275 M rider-only miles. Tesla's 1 M unsupervised miles imply an expected 0.012 fatalities at human rates, so they are statistically uninformative [E].

**Redundancy needs independence.**
- With $p=10^{-4}$/h per channel and a β-factor common-cause model, $P_{\rm sys}\approx\beta p+((1-\beta)p)^2$:

| β | $P_{\rm sys}$ (per h) |
|---|---|
| 0.01 | about $10^{-6}$ |
| 0.001 | about $1.1\times10^{-7}$ |
| 0.0001 | about $2\times10^{-8}$ |

- The headline $10^{-8}$/h needs β ≤ about $10^{-4}$, which cannot be validated from subsystem data alone [E].
- Different physics lowers β: camera vs radar for weather, camera vs lidar for darkness and geometry.

**Having sensors is not the same as being safe.**
- **Uber, 2018:** lidar and radar detected the pedestrian **5.6 s before impact**, but classification, prediction and design failed (NTSB HAR-19/03).
- **Cruise, 2023:** its system discarded correct lidar data (Cummings).

## E6. My synthesis by operating domain

| Domain | Assessment |
|---|---|
| **L2++ supervised** (highway + urban) | Camera-only or camera+radar is adequate and proven at scale: the human covers the tail. Lidar's marginal value is mainly night and unusual-object AEB. **Camera+radar will dominate globally** (high confidence). |
| **L3 highway eyes-off** (≤130 km/h) | Needs reliable detection at about 150–200 m (stopping about 110–170 m) plus degraded-mode redundancy. Lidar, or at least 4D radar plus telephoto cameras, makes certification much easier. **Every approved or announced L3 so far uses lidar**; the contested case is Changan's SL03 L3 permit. |
| **L4 urban robotaxi** | Ranges are short (camera depth at 30–50 m is workable), but vulnerable road users, occlusion, night and rare objects dominate. Vision-only is **physically plausible but statistically unproven**. Multimodal is the only design with outcome evidence at scale. |
| **Trucking** (80,000 lb, 105 km/h) | Stopping takes about 165–255 m, so perception is needed at 250–400+ m. Physics favours **long-range lidar (ideally FMCW with Doppler) + imaging radar + telephoto or wide-baseline stereo** most strongly here. |

**My view.**
- Cameras can in principle carry most of the driving task. End-to-end learning plus fleet data has closed much of the short-range gap.
- But **physics limits long-range depth, and statistics limits proof**.
- At a \$200 lidar price, the cheapest route to a **certifiable** safety case is usually to add physically diverse sensing, rather than to accumulate the billions of miles needed to prove vision-only to the same confidence.
- The debate has moved from "can we afford lidar?" to "does lidar buy a certifiable capability worth its integration and validation cost?" For supervised L2++ the answer is often no; for eyes-off L3, L4 and trucks it is usually yes.

---

# Part F — Projections

Probabilities are my subjective estimates as of 27 Sep 2026. "Confidence" reflects how strongly the evidence supports each call.

## F1. Thermal night vision

**Call: 2030 base case of 200–400k OEM thermal systems per year, still below 0.5% of global production, with China more than half. Confidence: medium.**

**Where it starts** [E]:
- Magna: about 50–100k per year. Its cumulative milestones (more than 500k in 2019, "nearly 1 M" in 2021, "over 1.2 M" in 2024) imply about 60–70k per year in 2021–24.
- China: about 25–30k per year (19k in Jan–Sep 2025).
- Total: about 80–130k per year.

**Why it grows, but only slowly:**
- **China** is the growth engine. Raytron-class 640×512 modules at 8 µm pitch are getting cheaper, and thermal is moving from a display to an **AEB input** (Zeekr 9X). The industry report's projection of 146k in China by 2030 implies about 50% growth per year. I haven't adopted it: lidar already covers night obstacle detection in Chinese flagships, so thermal competes for the same budget line.
- **The West** grows mainly through Magna's 5th generation on the existing premium users (BMW, Audi, Porsche, GM/Cadillac, VW), plus a possible handful of thermal-fused AEB programs aimed at night pedestrian tests.

**Why it stays niche:**
- It is a single-function sensor that must sit exposed in the grille (§A3).
- Camera+radar AEB keeps improving at night, especially where ADB is legal (§A6).
- In China, lidar takes the "extra sensor" slot.

**Near-standard (more than 10% of new cars) in any major market by 2030: probability <10%.**

**Upside triggers**, each of which would raise that figure:
1. **Test protocols that camera+radar demonstrably fail.** FMVSS 127's darkness/low-beam pedestrian scenarios, Euro NCAP 2026 night VRU tests, and C-NCAP 2027 fog/rain scenarios. If a pedestrian beyond the low-beam cutoff with oncoming glare becomes a *rated* scenario, thermal-fused AEB becomes the cheapest pass.
2. **Module cost below about \$100–150 at automotive grade.** This would come from Chinese 8 µm detectors and chalcogenide optics.
3. **ASIL-B thermal AEB becoming a Chinese flagship standard feature** rather than a Zeekr-only differentiator.

**Downside risks:**
1. **FMVSS 127 slipping to about 2031.** DOT announced an extension rulemaking in Mar 2026 while the industry lawsuit is on hold, which removes the nearest US forcing function.
2. **HDR camera progress.** 140 dB sensors plus better ISP/AI keep shrinking the night gap.
3. **Lidar ubiquity in China**, which removes the need for a separate night sensor.
4. **Germanium supply shocks** that raise Western optics costs. Chinese makers buy optics domestically.
5. **Wider ADB adoption.** An easing of the strict US ADB rule would lift camera-AEB performance at night.

## F2. Lidar in China

**Call 1: 2026 installations of about 5–6 M (all mounting positions), about 25–30% of NEVs. Confidence: medium-high.**

**Basis:**
- 2025 was 3.21 M. Q1 2026 was about 985k, and May 2026 alone was 447k, so the run-rate is already about 5 M+ per year.
- Company guidance and run-rates agree:
  - Hesai targets 3.0–3.5 M units in 2026, including robotics.
  - RoboSense shipped 437k ADAS units in H1 2026.
  - Seyond shipped 451k in H1 2026.
  - Huawei holds roughly a third of the market.
- Penetration crossed 21% of new cars in May 2026.

**Call 2: by 2030, about 50–60% of new passenger cars at ¥100k and above carry at least one lidar; about 10–15 M units per year including blind-spot units; main-lidar ASP about \$120–170. Confidence: medium.**

**Why it keeps rising:**
- **Price has crossed the mass-market threshold.**
  - Main lidars cost about ¥800–1,300.
  - BYD offers lidar on every model for ¥12,000.
  - Leapmotor sells a lidar trim at ¥85,900, and the GAC-Toyota bZ3X one from ¥109,800.
  - Li Auto and Xiaomi now fit it as standard.
- **Regulation raises the bar without naming sensors.**
  - GB 47955 (the mandatory L2 standard, effective Jan 2027) adds track and road tests, driver-monitoring lockouts and NOA verification.
  - GB 44721 (L3/L4, effective Jul 2027) requires systems to be "at least as safe as a competent and attentive driver".
  - C-NCAP 2027 adds more night, rain and fog scenarios.
  - Lidar is the cheapest safety margin for passing these, and a visible marketing feature.
- **Multi-lidar configurations raise units per car.** The average is about 1.3–1.6 [E]; the Aito M9 carries 6 (1 main, 1 in-cabin, 4 solid-state).

**Why it could stall below 50%:**
- A strong vision-only camp: Xpeng, Tesla's supervised driving in China, BYD God's Eye C, and VW–Xpeng models.
- The price war squeezes bill-of-materials budgets on cars below ¥150k.
- MIIT's post-2025 restrictions on "smart driving" marketing reduce the feature race.
- If those forces dominate, penetration plateaus around 35–45%.

**ASP path.** Blended revenue per unit fell from about RMB 4.1k (Hesai, 2024) to about RMB 1.37k (Q2 2026). I assume price cuts slow to about 10–15% per year once main lidars reach about \$150, and that high-line "digital" units (1,080+ lines) partly offset the decline.

**Call 3, structure:**
- Hesai and Huawei lead long-range.
- RoboSense and Seyond face share and margin pressure but still grow in volume (§G4). Some suppliers may consolidate or shift toward robotics (lawn mowers, humanoids) and exports.
- The vision-only share holds at about 20–30% of the ADAS-equipped market.
- Regulation stays sensor-agnostic.
- Western joint-venture brands become some of the largest lidar buyers in China (§B6).

## F3. Lidar in Western passenger cars

**Call 1: 2026 is a trough, probably below 100k units in cars sold outside China. Confidence: low-medium.**

**Basis:**
- Volvo removed lidar as standard from Apr 2026 and later abandoned lidar functions entirely.
- BMW dropped Personal Pilot L3 with the Apr 2026 7 Series facelift.
- Mercedes paused Drive Pilot, and the 2027 S-Class/EQS list no lidar.
- Stellantis shelved its L3 in Aug 2025.
- **What remains:** Lucid's DreamDrive Pro, small Japanese volumes (Lexus, Honda) and Chinese-brand exports (§B5).

**Uncertainty:** Chinese-brand exports are unmeasured. That includes "parallel exports" of zero-mileage lidar cars to Russia, Central Asia and the Middle East.

**Call 2: a 2027–28 restart tied to eyes-off L3 and "L4-ready" platforms.**

| Program | Lidar | Timing | What could go wrong |
|---|---|---|---|
| Rivian R2 Gen 3 | 1 forward, supplier undisclosed | From end-2026 | Supplier geopolitics; the only realistic low-cost options are Chinese |
| Nissan next-gen ProPILOT (with Wayve) | 1 roof-mounted | FY2027, Japan first | Nissan's financial restructuring; supplier (possibly MicroVision via Luminar) unconfirmed |
| Mercedes next L3 (up to 130 km/h) | Hesai (Picasso family) | "Within 2–3 years" | L3 economics were the problem last time |
| GM Escalade IQ eyes-off | Undisclosed | "As early as 2028" | Low-volume flagship; timing already hedged |
| Aeva (FMCW) with an unnamed top-10 European OEM, L3 | Aeva Atlas Ultra | SOP 2028 | Same L3 economics; Aeva's balance sheet |
| Ford eyes-off BlueCruise | Undisclosed (lidar unclear) | 2028 | Its chief sponsor (Doug Field) left in May 2026 |
| NVIDIA Hyperion 10 "L4-ready" platforms (Mercedes, Stellantis, Lucid, Nissan) | 1 lidar in the reference design | 2027+ | Carmakers may de-content to cameras and radar for consumer versions |

**Call 3: by 2030, about 1–3% of Western new cars carry lidar (about 0.6–2 M units per year on about 60 M non-China light vehicles). Confidence: low-medium.**

**Why this range:**
- The low end assumes eyes-off L3 stays a premium option with 10–20% take rates on a few flagship lines.
- The high end assumes L3 becomes a mainstream highway option: Mercedes at 130 km/h, GM, the Hyperion-based platforms, Rivian's volume R2.
- It also assumes Western lidar ASPs fall toward \$300–500 even without Chinese suppliers.

**What would push it higher:**
- L3 regulation harmonizing, such as UN R157 at 130 km/h and US state frameworks.
- Insurers or regulators crediting lidar in ratings.
- Robotaxi-derived hardware trickling down.

**What would push it lower:**
- L2++ hands-free systems (BMW Motorway Assistant, MB.DRIVE ASSIST PRO, Super Cruise, FSD Supervised) satisfying most buyers at €1–4k.
- Another round of L3 cancellations.

**Swing factor 1, US policy. A civilian-vehicle ban on Chinese lidar enacted by end-2028: probability about 50–60%.**

**Why that high:**
- The political direction is consistent and bipartisan:
  - S.4429 (Connected Vehicle Security Act) passed Senate Commerce unanimously on 22 Jul 2026.
  - The SAFE LiDAR Act has House Select Committee backing.
  - Hesai and RoboSense are both on the DoD 1260H list, whose §805 *products* ban for DoD starts 30 Jun 2027.
  - Idaho National Laboratory is testing Chinese lidar for vulnerabilities.
- The most likely vehicle is a **future NDAA** (the FY2025 NDAA already carried the DoD lidar ban in §164) or a standalone bill after the Nov 2026 midterms.

**Why not higher:**
- US robotaxi and AV companies that rely on Hesai (Zoox, Motional, Kodiak, Waabi, Aurora's near-range units) are likely to seek exemptions or long phase-ins.
- Rivian and Lucid want low-cost lidar.
- A US–China trade arrangement could slow measures that count as sanctions.
- BIS deliberately **excluded lidar** from the Jan 2025 connected-vehicle rule, showing some agencies see it as lower-risk than connectivity or ADS software.

**If enacted:**
- Expect a phase-in by model year, similar to the connected-vehicle rule.
- An ownership test (like S.4429's 15% cap) would exclude Hesai's Thailand plant and US joint ventures built on Chinese lidar technology.
- Western lidar ASPs would stay about 2–3× Chinese levels.
- Non-Chinese suppliers that could gain orders: Innoviz, Valeo, Aeva, Ouster, MicroVision (ex-Luminar), LG Innotek, Koito/Cepton, possibly Aumovio.
- Rivian, Lucid and the robotaxi fleets would need to requalify suppliers.
- US lidar penetration would grow more slowly than Europe's.

**Swing factor 2, European policy. An EU-level ban on Chinese automotive lidar by 2028: probability about 15%.**

**Why low:**
- **No EU instrument is aimed at automotive components.** The EU's tools so far are tariffs (countervailing duties on Chinese battery EVs since Oct 2024) and horizontal cybersecurity rules that apply at type approval (UNECE R155/R156 on cybersecurity and software updates). I found no EU-level measure aimed at lidar.
- **European carmakers are the main buyers of Chinese lidar:** Mercedes' next L3 uses Hesai for Europe and China, and a "top European OEM" (probably VW) ordered more than 1 M Hesai ATX units for its China joint ventures. The industry would oppose a ban strongly.
- **Retaliation risk is high.** European carmakers depend heavily on China sales and on Chinese battery and rare-earth supply chains.

**Why not negligible:**
- A US ban would create transatlantic pressure to align.
- A security incident involving vehicle sensors, or results from the INL-type testing, could change the politics.
- The EU's economic-security agenda keeps "de-risking" critical technologies on the table.

**The more likely European outcome is "the Hesai-in-Mercedes template"**, which has four parts:
1. Chinese-designed lidar hardware;
2. made outside China (Hesai's Thailand plant);
3. integrated by a European carmaker under its own software and cybersecurity process (R155/R156);
4. supplied into both European and Chinese programs.

This lets European carmakers keep Chinese cost and performance while managing security and tariff exposure. Japan and Korea look similar: no restrictions, and Toyota and Nissan already buy Chinese lidar for their China joint ventures.

## F4. Robotaxi and truck lidar outside China

**Call 1: 2027 consumption of about 60–120k units. Confidence: low.**

**Basis, from company plans at 4–9 lidars per vehicle:**
- **Waymo:** 8–20k vehicles × 4. Its Mesa factory claims "tens of thousands" of vehicles per year at full capacity, and Hyundai Ioniq 5 deliveries start in Q4 2026.
- **Zoox:** 1–2.5k × about 6. Its NHTSA exemption is capped at 2,500 per year.
- **VW/Mobileye:** 1–5k × 9.
- **Nuro/Lucid/Uber:** about 1–6k × about 6.
- **Chinese operators abroad:** WeRide, Pony and Baidu in the Middle East and Europe.
- **Trucks:** Aurora's Roush line runs at about 1,000 per year from Oct 2026; Kodiak; Daimler/Torc from 2027.

The plan-based total is about 70–225k. I discount it because AV ramps have historically slipped: Tesla had stated a target of about 500 cars by end-2025 and had about 30 by tracker counts; Zoox had about 100 robotaxis, under an exemption capped at 2,500 a year.

**Call 2: 2030 consumption in two scenarios. Confidence: low.**
- **About 200–500k per year if scaling plans hold.** That needs Waymo at tens of thousands of vehicles per year, Uber's NVIDIA-platform fleet (target up to 100k vehicles from 2027), and VW/Mobileye and Zoox scaling on schedule.
- **About 100–200k per year if ramps keep slipping**, which is the historical pattern.

**Value vs units** (corrected when this section was expanded):
- Robotaxi and truck lidar costs more per unit: roof long-range units are several thousand dollars; perimeter units are hundreds [E].
- In 2026–28, AV lidar outside China (about \$40–120 M, including Waymo's captive units at cost) is **about the same size by value** as Western passenger-car lidar (about \$40–150 M).
- AV lidar pulls ahead if the Western L3 restart slips.
- The earlier claim that AV lidar would "exceed passenger-car lidar by value" was too confident.
- Waymo stays captive. **Hesai is the default merchant supplier for non-Waymo robotaxis** (long-range and 360° units), but it faces real competition in specific slots (Innoviz in Mobileye Drive, RoboSense for blind spots, Aeva and Aurora's FMCW for long-range truck lidar) and a concrete, dated US policy risk. See §G1.

## F5. Technology mix, 2030 (global automotive units)

**Denominator** [E]. Total automotive lidar in 2030 is about 11–18 M units per year: China 10–15 M (§F2), Western passenger cars 0.6–2 M (§F3), robotaxis and trucks 0.1–0.5 M (§F4). Robotics lidar is excluded.

| Route | 2030 unit share | Reasoning |
|---|---|---|
| 905/940 nm dToF (Si SiPM / SPAD-SoC) | **85–92%** | Every leading Chinese supplier is on this route. It rides silicon scaling (SPAD-SoCs, VCSEL arrays) and already sells at about \$200. **Within it:** long-range one-axis scanned units about 50%; short-range flash/e-scan units 30–40% (flagships add 2–4 blind-spot units per car, and robotaxis add perimeter units); MEMS below 5% (RoboSense calls the MX its last MEMS generation; Innoviz continues in Western and robotaxi niches). **940 nm gains share** thanks to narrower VCSEL filters and a +17.5% eye-safety allowance |
| 1550 nm ToF | 1–3% | Seyond Falcon (NIO), trucks (Seyond K24, Benewake, Leishen), MicroVision's ex-Luminar Iris/Halo, AEye in defense. It shrinks because of its 2–3× cost and higher power. **Upside:** a high-end L3 revival where eye-safe range (Seyond K3 at 450 m @10%) is a selling point |
| FMCW | **0.1–0.5%** (≈20–100k units); larger by value | **Revised down from 0.5–2%** after doing the arithmetic. Aurora (thousands of trucks per year × 1–3 FirstLight units), Daimler/Torc from 2027 (thousands), Bendix L2+ trucks, Aeva's European L3 from 2028 (a premium option: tens of thousands at most), LuminWave's Chinese truck programs. Reaching 1%+ needs FMCW on a mainstream passenger L3/L2++ platform |
| OPA in automotive series production by 2030 | probability **10–15%** | No series program exists, and OPA companies have suffered heavy attrition (Quanergy filed for Chapter 11 in 2022), and Analog Photonics has no announced production award. Not zero, because LuminWave claims a 2026 truck SOP for an on-chip-antenna FMCW design (unverified) and Voyant's 2D solid-state FMCW array targets industrial markets first. Hard problems remain: element count (about 600 for 0.1° at 1.5 µm pitch), phase calibration, receive efficiency and aperture |
| LC-metasurface (Lumotive-type) automotive short-range by 2030 | probability **20–25%** | Already in industrial production (Hokuyo YLM-10LX3); a 180°×140° ToF platform with Namuga is sampling in 2026, and short range (≤50 m) suits it. **Automotive risk:** liquid-crystal response slows sharply at −40 °C, and qualification from −40 to +105 °C is demanding |
| Fully solid-state long-range (≥200 m @10% over ≥100° H) in series by 2030 | probability **15–20%** | Blocked by receiver étendue and silicon area (§C6): solid-state sensors sit at $R^2\cdot$FOV about $10^7$ vs about $10^8$ for scanned units. It would need a large-aperture non-mechanical receive steerer, tiling of about 20 narrow-field modules (cost), or much smaller high-PDE SPADs on stitched or three-layer stacks |

**Further expectations:**
- **SPAD-SoC line counts saturate** around 2–4k lines. The reticle limits a single die (Picasso already needs two chips for 4,320 lines), and the photon budget makes extended-target range fall as $N^{-1/2}$ at fixed laser power.
- **Competition moves elsewhere:**
  - from "lines" to **small-object detection metrics** (for example a 13×17 cm box at 150 m);
  - to **RGB-D fusion on chip** (Hesai Picasso; Huawei Limera's coaxial lidar-camera);
  - to **behind-glass or in-cabin mounting** (Hesai ET25 and ETX; Huawei's in-cabin lidar);
  - and to **cost per car** as multi-lidar configurations spread.
- **Sony remains the merchant SPAD supplier** for non-Chinese and tier-2 Chinese makers. The top Chinese makers move to in-house chips (RoboSense Phoenix, Hesai Picasso) in 2026–27. Where those are fabbed is the open strategic question (§C5, §D6).

## F6. FMCW specifically

**My view.** FMCW's differentiators are per-point radial velocity, intrinsic rejection of sunlight and other lidars, and long range. How much each matters depends on the use case:
- **Heavy trucks (decisive).** An 80,000 lb truck at 105 km/h needs 165–255 m to stop, so perception at 250–400+ m matters. Instantaneous Doppler separates a stalled vehicle from road clutter at that range within a single frame. That is why both driverless-truck leaders chose FMCW for long range (Aurora in-house, Daimler/Torc with Aeva).
- **L3 at 130 km/h (useful).** Stopping takes about 150 m, so long-range velocity helps prediction and lowers latency. It is a real but not unique advantage; long-range ToF plus radar Doppler can cover much of it.
- **L2++ (nice to have).** \$200 ToF at 25–40 Mpts/s with SPAD PDE of 37–45% keeps raising the bar. The human remains the fallback, so FMCW's advantages don't pay for its cost.

**What would change this:**
1. **Coherent FPAs or massively parallel PIC receivers at about \$300–500.** FMCW's point rate is limited by dwell time per point per channel (about $M/T_{\rm dwell}$). Tens of parallel LO-matched channels on one PIC (Voyant's Helium direction) would remove the throughput penalty.
2. **A safety-case advantage from instantaneous Doppler at L3/L4.** For example, if regulators or insurers credit shorter perception latency, or if radar-lidar association errors show up as a failure mode in incident data.
3. **Mutual interference becoming measurable for ToF.** With about 20%+ penetration and several lidars per car in China, pulse collisions rise. ToF coding and randomization currently cope, but a documented failure mode would favour coherent detection.

**Research leverage points**, and why each matters:
- **Receive-side, large-aperture non-mechanical steering.** It benefits both ToF (it removes the étendue penalty of staring arrays, §C6) and FMCW (it removes mechanical scanning of a single-mode receiver).
- **Integrated narrow-linewidth, linear-chirp lasers with SOAs** (SiN, TFLN, III-V-on-Si). Coherence needs about $\Delta\nu\lesssim160$ kHz at 300 m, and chirp linearity drives range precision. Doing this at automotive cost is the core FMCW bill-of-materials problem.
- **Speckle diversity on chip.** Single-mode coherent detection sees Rayleigh fading. Polarization, wavelength or spatial diversity raises detection probability without extra laser power.
- **Low-power, high-rate coherent receiver ASICs.** Each channel digitizes 100–400 MHz of beat signal, so ADC and DSP power per channel sets how many channels fit in a 10–15 W envelope.

**What to watch, and why:**
- **Aurora's truck count against its 200-by-year-end target.** This is the first test of FMCW at fleet scale.
- **Aeva–Daimler 2027 launch.** The first truck-OEM series FMCW program.
- **Aeva's European OEM SOP in 2028.** The first passenger-car FMCW program.
- **LuminWave's truck SOP.** Whether Chinese FMCW reaches production.
- **Whether Hesai or RoboSense ever announce FMCW.** Hesai holds FMCW, OPA and metasurface patents; a product announcement would signal that the ToF leaders see a need.

## F7. Camera-only vs multimodal

**Call 1: lidar-based fleets keep more than 85% of global driverless miles through 2028. Probability about 80%.**
- **Waymo** alone drives about 4 M+ miles a week, roughly 200 M a year, and is growing. Baidu, Pony, WeRide and Zoox add to that.
- **Tesla** had about 1 M cumulative unsupervised miles by Sep 2026.
- Even at 10× growth per year, Tesla would reach only tens of millions of miles a year by 2028, against several hundred million for Waymo.
- **The main risk to this call** is Tesla scaling far faster than it has so far. For example, 10k+ concurrent unsupervised cars at about 30k miles per car per year would be about 300 M miles a year and could take 25–35% of the total.

**Call 2: Tesla operates thousands of unsupervised camera-only vehicles concurrently by end-2027. Probability about 50%.**
- **For:**
  - Cybercab production has started, with a claimed installed capacity above 125k per year.
  - Texas registrations reached about 546 by 26 Sep 2026.
  - Tesla has the capital and the manufacturing capacity.
- **Against:**
  - End-2025 fleet target: about 500 cars stated, against about 30 on trackers.
  - The active unsupervised fleet is only about 85–200 per trackers, with Austin's 7-day average at 8 on 22 Sep.
  - Open NHTSA probes: EA26002 on reduced visibility, including the "Radar Saves Us" document request; PE25012 on traffic violations; the Cybercab FMVSS audit.
- **Independent evidence that it is as safe as Waymo in a matched operating domain is unlikely before 2028.**
  - RAND-style arithmetic needs on the order of $10^8$ miles for injury-crash comparisons and billions for fatalities.
  - Tesla's unsupervised mileage is two orders of magnitude short, and crash narratives were redacted until May 2026.

**Call 3: no major jurisdiction mandates lidar by 2030. Probability about 90%.**
- FMVSS, UNECE and China's GB standards are all technology-neutral by tradition.
- The performance-based rules (FMVSS 127's darkness tests, UN R157/R171, China's GB 44721 "competent driver" baseline) will **indirectly favour multimodal sensing for eyes-off systems**, because lidar and radar are the cheapest way to pass night, glare and fog scenarios with margin.

**Call 4: more than 90% of driverless trucks use lidar plus radar through 2030. Confidence: high.**
- Every driverless truck program uses lidar: Aurora, Kodiak, Torc/Daimler, Waabi, PlusAI, Gatik, Bot Auto.
- The physics (165–255 m stopping distances, lane assignment at 300 m) leaves camera-only designs little room.

## F8. Key signposts (next 12–18 months)

| # | Signpost | Why it matters / what it would move |
|---|---|---|
| 1 | **NHTSA EA26002** (Tesla reduced visibility, including the "Radar Saves Us" document request) and the **Cybercab FMVSS audit** (answers due 30 Sep 2026) | A recall or finding that vision-only failed in glare, fog or dust would weaken the camera-only case (§F7 call 2) and strengthen multimodal. A clean closure would do the opposite |
| 2 | **Waymo's 1 M rides-per-week target**, and IIHS or insurer follow-up studies | Confirms whether lidar-based L4 keeps scaling with independently verified safety (§F7 call 1), and whether the Austin +4% anomaly in the IIHS data persists |
| 3 | **US Senate floor vote on S.4429**; the **Hesai 1260H remand**; the **30 Jun 2027** DoD products ban | Directly moves the US-ban probability (§F3 swing factor 1), Hesai's position with US robotaxis (§G1), and Western supplier prospects |
| 4 | **China's export-control suspensions expiring 10 and 27 Nov 2026** | A lapse would reinstate the Ga/Ge/Sb ban to the US and the extraterritorial rare-earth rule, affecting Western supplies of VCSEL/EEL substrates, magnets and germanium optics (§D2) |
| 5 | **The FMVSS 127 two-year extension rulemaking** | Sets when US night pedestrian-AEB tests bite: a key trigger for thermal (§F1) and a softer one for lidar |
| 6 | **Aurora reaching 200 driverless trucks**; the **Aeva–Daimler SOP**; the **Rivian R2 Gen 3 lidar supplier**; **GM's lidar supplier** | Tests of FMCW at fleet scale (§F6), and whether Western passenger-car lidar lands with Western or Chinese suppliers (§F3) |
| 7 | **Teardowns of mass-production RoboSense Phoenix and Hesai Picasso** (foundry, node, pitch) | Shows how far Chinese SPAD-SoCs are independent designs, and whether a foundry chokepoint exists (§C5, §D6) |
| 8 | **Lidar take rates on Western-brand China joint-venture models** (Toyota bZ series, VW ID.UNYX, Nissan, Buick/Cadillac) | Shows whether Western brands follow Chinese buyers to lidar, or can win with vision-only partners such as the Xpeng stack (§B6) |

---

# Part G — Editorial judgements, re-examined

Several conclusions in this report compress a lot of evidence into a short verdict. This part re-examines the strongest of them: what each one means, what supports it, what cuts against it, and what a fair statement is. Where a verdict turned out to be overstated, the main text has been softened and points here.

## G1. "Hesai is the default merchant lidar supplier for robotaxis and trucks"



**Meaning.** Excluding Waymo, which is captive and uses about half of all robotaxi and truck lidar outside China, Hesai is the default supplier. The main threat to it is policy, not a competitor.

**For:**
- About 61% of robotaxi lidar in 2024 (Yole).
- **Customers:** Zoox, Motional (exclusive short-range), Kodiak, Waabi, Aurora's near-range units, Baidu, Pony (4 AT128 per car), DiDi and Momenta.
- A \$40 M sole-supplier order from an unnamed "leading U.S. robotaxi company".
- Primary lidar partner for NVIDIA DRIVE Hyperion 10, the reference design behind Uber's plan for up to 100k vehicles.
- **Scale:** about 1.6 M units in 2025, a 41.8% gross margin, profitable, and more than 4 M units of capacity in 2026. Western merchant suppliers' prices are several times higher (§B1).

**Against:**
- **Innoviz won Mobileye Drive:** 9 lidars per VW ID. Buzz, with a claimed program life of about 150k units. It is the largest non-Chinese merchant AV win, and it is not Hesai.
- **RoboSense** took WeRide's Gen-8 robotaxi and claims about 90% of leading L4 fleets use its E-platform blind-spot units.
- **Long-range truck lidar is going to FMCW:** Aurora in-house, Aeva for Daimler/Torc (with Innoviz for short range).
- **Ouster** supplies Motional's long-range unit and May Mobility.
- **US policy risk is dated and concrete:**
  - the 1260H §805 *products* ban from 30 Jun 2027 (DoD procurement only);
  - S.4429 cleared Senate Commerce unanimously;
  - Idaho National Laboratory is testing Chinese lidar.
  - Zoox, Kodiak, Waabi and Aurora would all face requalification.

**Fair statement.** Hesai is the default for long-range and 360° robotaxi lidar outside Waymo. It is not dominant in blind-spot units, in Mobileye's ecosystem, or in long-range truck lidar, and its US position depends on policy. Confidence: medium on today's position, low on how long it lasts.

## G2. "The Western lidar base is thin"



**Meaning.** Most of the 2020–22 Western automotive lidar cohort has failed, sold cheaply, or become marginal, and its IP is consolidating into a few buyers.

**For:**
- **Failures:**
  - Quanergy: listed Feb 2022 at about \$1.4 B implied, Chapter 11 Dec 2022.
  - Ibeo: insolvent 2022.
  - Argo AI (Princeton Lightwave lidar): shut down 2022.
  - Scantinel: insolvent 2025.
  - Baraja: 75% layoffs, patents for sale.
- **Sales far below peak valuation:**
  - Luminar's lidar business sold for \$33 M; its market value briefly exceeded roughly \$10 B in late 2020 [U].
  - Velodyne merged with Ouster.
  - Cepton taken private by Koito at \$3.17 per share.
- **Tier-1 exits:** Bosch (2023), Continental HRL131 (2023), Mobileye's in-house FMCW (2024).
- **Small revenue or share-price pressure:** AEye \$233k (FY25); MicroVision about \$1 M per quarter; Innoviz approved a reverse split.
- **IP consolidation:** MicroVision took Ibeo, Luminar and Scantinel; Hesai took Fastree3D.

**Against:**
- **Real, growing survivors:**
  - Ouster: \$169 M in FY25, up about 50%, mostly industrial.
  - Valeo: >€1 B in SCALA orders.
  - Innoviz: guiding \$67–73 M for 2026.
  - Aeva: Daimler, a European OEM L3 program, and LG Innotek as an investor.
- Captive Western lidar is healthy: Waymo, and Aurora FirstLight.
- A US ban on Chinese lidar would create a protected market and could revive Western suppliers quickly.

**Root causes, my reading:**
- SPAC-era valuations assumed L4 by about 2025.
- Western lidar was tied to eyes-off L3 programs that were narrow, expensive, and then cancelled.
- OEM programs have long lead times and low volumes.
- Chinese prices collapsed to about \$200, backed by a 3 M+ unit home market.
- For 1550 nm players, the cost structure was higher from the start.

**Fair statement.** "A brutal shakeout: most of the 2020–22 cohort has failed, been sold cheaply, or become marginal, and IP is consolidating. The survivors are real but small (non-Chinese suppliers are about 5% of automotive units)." Confidence: high on the shakeout, medium on its permanence, since the policy wildcard remains.

## G3. "Luminar failed on program economics, not optics"

**For.** Luminar's bankruptcy disclosure centres on Volvo's volume collapse: 1.1 M lifetime sensors expected, fewer than 10 k bought, and a 90% cut in Sept 2025. It also cites debt and OEM software-integration delays. Volvo's lidar functions were never activated.

**Against:**
- Mercedes ended the Iris deal because Luminar "failed to meet ambitious requirements".
- Volvo cited Luminar's "failure to meet contractual obligations".
- Both customer statements concern delivery against requirements, alongside demand.
- The 1550 nm fiber-laser plus InGaAs route is itself an optics-driven cost structure, about 2–3× the 905 nm route.

**Fair statement.** Its difficulties arose mainly from program economics and unmet customer obligations; its 1550 nm cost structure contributed; sensor performance was not the main factor.

## G4. Other judgements

| Judgement (section) | Basis | What cuts against it | Assessment |
|---|---|---|---|
| RoboSense and Seyond "squeezed" (§F2) | Q1 2026 China share: Hesai 34.9%, Huawei 32.3%, Seyond 16.8%, RoboSense 11.0%. RoboSense ASP −52%, and robotics volume now exceeds ADAS. Seyond gross margin about 8%, NIO-dependent | Both are growing in volume. Seyond's Q2 2026 shipments surged. RoboSense has a >9 M backlog and Toyota/Nissan JV orders | Fair on margin and share pressure; not a decline in volume. The main text is softened |
| "2026 is a trough" for Western lidar (§0, §F3) | Volvo, BMW and Mercedes L3 exits; restart scheduled for 2027–28 | Unmeasured Chinese exports; Rivian ramp | Reasonable; low-medium confidence |
| "Commercial, not a sensor-physics verdict" (§B2) | OEMs cite demand, cost and profitability; Mercedes still says lidar compensates for camera limits | Lidar-free L2++ succeeding is itself a verdict that supervised driving doesn't need lidar | Half right. The main text now says both |
| "One-axis scanner is the cheapest optical multiplexer" (§C6) | $R_{10\%}^2\cdot$FOV: solid-state about $10^7$ vs scanned about $10^8$ m²·deg²; every long-range digital lidar keeps one moving axis | MEMS, flash, stitched and smaller-pitch SPADs keep improving | A statement about today's economics; a sound engineering judgement, not a law |
| "The missing component is large-aperture receive-side steering" (§C6) | Receiver étendue and silicon-area arithmetic | Alternatives: tiling, smaller-pitch high-PDE SPADs, coherent FPAs. The binding constraint may be cost, not physics | Defensible, but check it for bias: it favours beam-steering research. Treat it as one of several routes |
| "FMCW is nice-to-have for L2++" (§F6) | \$200 ToF at 40 Mpts/s; Mobileye's exit citing ToF cost-downs | Aeva's European L3 win; mutual interference may become measurable as Chinese penetration passes 20% with several lidars per car | Opinion. It would be wrong if interference or instantaneous Doppler becomes safety-case critical |

## G5. How these judgements should be read

Short verdicts are useful for thinking, but they hide uncertainty. Across this report the pattern is consistent:
- statements about the **present** (market shares, program exits, failures) are well supported;
- statements about **durability** (who keeps winning) depend mainly on **US policy** and on whether **eyes-off L3** returns in 2027–28;
- **engineering judgements** (one-axis scanning, receive-side steering, the value of FMCW) describe current economics and could change with a single device breakthrough.

---

# Appendix 1 — Open items and unverified points

**Resolved in the gap-fill pass**
- Seyond Robin E1X: **940 nm** (read from its datasheet).
- Hesai ETX: the 400 m vs 300 m discrepancy is explained as headline vs spec table.
- Picasso: 2,160 lines per chip; 4,320 lines uses two chips.
- Huawei 192-line: 905 nm, 4-facet prism, 189×600 SPAD.
- Volvo EX90 production: about 18.1k (2024–25).
- Cadillac night-vision take-rate: secondary figures refined.
- Thermal volume: rate implied by the FLIR/Magna milestones.
- Aurora 2022 lidar complement: 9 per truck.

**Still open**
- **Take-rate data:** Mercedes Drive Pilot and BMW Personal Pilot (never published); Lucid DreamDrive Pro; the Cadillac original article (Automotive News, paywalled).
- **Chinese-brand lidar exports outside China:** only an estimate exists (15–60k, low confidence), and parallel exports are unmeasured. This is still the largest uncertainty in §B5.
- **Undisclosed suppliers:**
  - Rivian (RoboSense reported by one outlet, denied by Rivian);
  - GM (count and vendor);
  - Nissan (1 roof lidar, vendor unknown; possibly MicroVision via Luminar, unconfirmed);
  - Lucid–Nuro robotaxi and Gravity;
  - Ford L3 sensors;
  - Zoox exact count;
  - Aurora's current (2025–26) count;
  - Gatik, May, Avride and PlusAI current suppliers.
- **Not covered in the gap-fill pass:**
  - Aeva's European OEM identity;
  - Mercedes S-Class robotaxi lidar;
  - Aeva and Aurora gen-2 wavelength, scanner and points/s;
  - Valeo SCALA 3 and InnovizTwo detector types;
  - Waymo lidar wavelength;
  - the Yole technology split.
- **Headlight regulation figures (§A6):** the current ECE/UN R149 cap on total main-beam intensity (225,000 cd historically; about 430,000 cd reportedly allowed now) was not researched and needs checking against the regulation text.
- **Hesai:** Picasso PDE wavelength, pitch and node; Thailand plant volume start (guided early 2027).
- **Huawei 896-line:** wavelength, emitter, detector and scanner (only media claims exist, some unsourced).
- **Foundries:** none publicly named for any Chinese SPAD-SoC. ATX SiPM vendor is in the paywalled TechInsights DDT-2505-806.
- **IEC 60825-1** figures (not covered in the gap-fill pass), silicon absorption and AM1.5G values are from standard tables and were not checked in this draft. All [E] calculations are order-of-magnitude, with stated assumptions.
- **Tesla:** active unsupervised fleet size is contested (a community tracker vs Teslarati).
- **Yole** technology split (rotating mirror 66% / MEMS 32% / 9xx about 90%) came from a search extract of a paywalled page.

# Appendix 2 — Selected sources

**Thermal night vision**
- Automotive night vision (overview): https://en.wikipedia.org/wiki/Automotive_night_vision
- Magna thermal sensing: https://www.magna.com/stories/blog/2024/magna-tech-spotlight--thermal-sensing-system
- China infrared night vision report 2025: https://finance.yahoo.com/news/china-global-automotive-infrared-night-114200997.html
- Raytron–Zeekr thermal AEB: https://www.prnewswire.co.uk/news-releases/raytron-partners-with-zeekr-to-launch-the-worlds-first-thermal-aeb-302614080.html
- Valeo–Teledyne FLIR: https://www.valeo.com/en/valeo-and-teledyne-flir-announce-agreement-and-first-contract-for-thermal-imaging-for-automotive-safety-systems/
- optics.org, thermal \$7 B / automotive \$285 M: https://optics.org/news/16/8/44
- IIHS, pedestrian AEB at night: https://www.iihs.org/news/detail/pedestrian-crash-avoidance-systems-cut-crashes--but-not-in-the-dark
- FMVSS 127 status (Nelson Mullins, Apr 2026): https://www.nelsonmullins.com/insights/blogs/driving-forward-developments-in-transportation-law-and-innovation/all/the-road-ahead-for-fmvss-127-whither-the-automatic-emergency-braking-mandate
- USGS germanium 2026: https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-germanium.pdf

**Lidar market and Western programs**
- Hesai/Yole 2025 shares: https://www.hesaitech.com/hesai-secures-no-1-in-long-range-adas-lidar-shipments-in-2025-by-yole-group/
- optics.org, Yole 2024: https://optics.org/news/16/7/2
- optics.org, Yole trims forecast: https://optics.org/news/15/6/25
- Gasgoo, "Is LiDAR no longer necessary?": https://autonews.gasgoo.com/articles/market-industry/is-lidar-no-longer-necessary-in-the-automotive-sector-2057737516554313729
- TechInsights, market consolidates on China: https://www.techinsights.com/blog/insight-automotive-lidar-market-consolidates-china
- Hesai FY2025 results: https://investor.hesaitech.com/news-releases/news-release-details/hesai-group-reports-fourth-quarter-and-full-year-2025-unaudited
- Hesai–Mercedes L3: https://www.hesaitech.com/hesai-announced-as-strategic-lidar-partner-and-confirmed-supplier-for-mercedes-benz-l3-enabled-models/
- Volvo drops lidar (Electrek, Jul 2026): https://electrek.co/2026/07/29/volvo-drops-lidar-ex90-es90-compensation/
- Luminar Chapter 11 / asset sales (8-K): https://www.sec.gov/Archives/edgar/data/1758057/000114036126003737/ef20064774_8k.htm
- Mercedes Drive Pilot paused (The Verge): https://www.theverge.com/transportation/860935/mercedes-drive-pilot-level-3-scrapped
- 2027 S-Class US release: https://media.mbusa.com/news/the-new-mercedes-benz-s-class-refined-in-every-detail
- BMW drops L3 (bmwblog): https://www.bmwblog.com/2026/03/17/bmw-explains-why-dropping-level-3-self-driving-tech/
- Stellantis shelves L3 (electrive): https://www.electrive.com/2025/08/29/stellantis-probably-stops-development-of-level-3-driver-assistance-system/
- GM eyes-off 2028: https://news.gm.com/home.detail.html/Pages/news/us/en/2025/oct/1022-AI-GM-launch-eyes-off-driving-conversational-AI.html
- Rivian Q2 2026 letter: https://www.sec.gov/Archives/edgar/data/0001874178/000187417826000053/ex-9922q26rivianearnings.htm
- Nissan–Wayve: https://wayve.ai/press/nissan-wayve-sign-definitive-agreements/
- Innoviz Q2 2026 (6-K): https://www.sec.gov/Archives/edgar/data/0001835654/000117891326003861/exhibit_99-1.htm

**Robotaxi and trucks**
- Waymo fleet data (TechCrunch, Sep 2026): https://techcrunch.com/2026/09/24/waymo-is-scaling-fast-heres-what-the-fleet-data-shows/
- Waymo 6th-gen driver: https://waymo.com/blog/2024/08/meet-the-6th-generation-waymo-driver/
- Hesai \$40 M US robotaxi order: https://www.hesaitech.com/hesai-signs-new-40-million-lidar-contract-with-leading-u-s-robotaxi-company/
- Aurora Q2 2026 letter: https://www.sec.gov/Archives/edgar/data/1828108/000182810826000075/aurora26q2shareholderlet.htm
- Kodiak Q2 2026: https://www.sec.gov/Archives/edgar/data/0001853138/000162828026054331/kodiakai-q2202663026xearni.htm
- Zoox paid service: https://techcrunch.com/2026/07/30/zoox-clears-final-federal-hurdle-to-launch-paid-robotaxi-service/

**FMCW and beam steering**
- Aeva European OEM win: https://www.aeva.com/press/aeva-wins-exclusive-global-production-contract-from-top-european-passenger-oem/
- Aeva–Daimler C-samples: https://www.aeva.com/press/aeva-delivers-atlas-c-samples-to-daimler-truck-for-autonomous-truck-production-program/
- Aurora photonic engine: https://aurora.tech/newsroom/inside-auroras-photonic-engine-engineering-lidar-for-automotive-scale
- Mobileye ends lidar development: https://ir.mobileye.com/news-releases/news-release-details/mobileye-end-internal-lidar-development
- Analog Photonics OPA (IEEE Spectrum): https://spectrum.ieee.org/lidar-on-a-chip
- Voyant Helium: https://www.businesswire.com/news/home/20251216762450/en/
- Lumotive–Hokuyo: https://lumotive.com/press-releases/lumotive-and-hokuyo-announce-commercial-release-of-worlds-first-3d-lidar-sensor-with-true-solid-state-beam-steering/
- LuminWave integrated chip: https://luminwave.com.cn/fully-integrated-silicon-optical-chip/
- Yole on FMCW timing: https://www.edge-ai-vision.com/2024/06/automotive-lidar-deployment-ramps-up-in-2024/

**Technology routes and SPAD**
- Sony IMX459: https://www.sony-semicon.com/en/news/2021/2021090601.html
- Sony IMX479: https://www.sony-semicon.com/en/news/2025/2025061001.html
- Kumagai et al., ISSCC 2021: doi:10.1109/ISSCC42613.2021.9365961
- Villa et al., *Sensors* 21, 3839 (2021): https://www.mdpi.com/1424-8220/21/11/3839
- NE Times, 26-teardown summary: https://www.ne-time.cn/web/article/37421
- TechInsights, Huawei 192-line: https://www.techinsights.com/blog/deep-dive-teardown-huawei-192-line-lidar-l306-lidar-sensor
- TechInsights, RoboSense E1: https://www.techinsights.com/blog/robosense-rs-lidar-e1-solid-state-blind-spot-lidar-standard-floorplan-analysis
- TechInsights, RoboSense EM4: https://www.techinsights.com/blog/robosense-em4-long-range-digital-lidar-device-essentials-plus
- EE Times / Yole, Hesai AT128 teardown: https://www.eetimes.com/whats-in-the-box-hesai-at128-lidar-for-li-auto-l9-at-a-glance/
- Hesai Picasso / ETX: https://www.hesaitech.com/hesai-unveils-picasso-6d-full-color-spad-soc-next-gen-etx-and-innovations-in-spatial-intelligence-and-physical-ai/
- RoboSense Eocene: https://www.robosense.ai/en/news-show-1978
- Opsys ALTOS: https://www.opsys-tech.com/altos-industrial-lidar
- Seyond Falcon K2 datasheet: https://www.seyond.cn/wp-content/uploads/2025/03/Seyond_Falcon-K2-LiDAR_Datasheet_EN_Public_V2.2.0.pdf

**Supply chain and geopolitics**
- Hesai 2025 Annual Report: https://www.sec.gov/Archives/edgar/data/0001861737/000110465926048075/tm2612222d1_ex99-1.pdf
- ams OSRAM 2025 report: https://ams-osram.com/documents/d/ams-osram/ams-osram-en-management-report-and-group-financial-statement-2025
- AXT permits (Semiconductor Today): https://www.semiconductor-today.com/news_items/2026/mar/axt-090326.shtml
- D.C. Circuit, Hesai v. DoD (No. 25-5256): https://media.cadc.uscourts.gov/opinions/docs/2026/08/25-5256-2188737.pdf
- DoD 1260H list (Jun 2026): https://media.defense.gov/2026/Jun/08/2003945537/-1/-1/1/ENTITIES-IDENTIFIED-AS-CHINESE-MILITARY-COMPANIES-OPERATING-IN-THE-UNITED-STATES-IN-ACCORDANCE-WITH-SECTION-1260H.PDF
- BIS connected-vehicle rule (Gibson Dunn): https://www.gibsondunn.com/bis-connected-vehicles-rule-effective-as-of-march-17-2025/
- SAFE LiDAR Act: https://chinaselectcommittee.house.gov/media/press-releases/moolenaar-cosponsors-the-safe-lidar-act
- Connected Vehicle Security Act advances: https://www.slotkin.senate.gov/2026/07/22/slotkin-moreno-bill-to-protect-national-economic-security-from-chinese-vehicles-advances-unanimously/
- China export-control suspensions (Pillsbury): https://www.pillsburylaw.com/en/news-and-insights/china-suspends-export-controls-certain-critical-minerals-related-items.html
- INL probes Chinese lidar: https://techcrunch.com/2026/08/21/us-government-lab-is-probing-chinese-lidar-for-security-vulnerabilities/

**Camera-only vs multimodal**
- Waymo Safety Impact: https://waymo.com/safety/impact/
- IIHS Waymo study (Jul 2026): https://www.iihs.org/news/detail/waymos-driverless-cars-crash-less-often-than-people
- NHTSA EA26002: https://static.nhtsa.gov/odi/inv/2026/INOA-EA26002-10023.pdf
- Tesla robotaxi fleet (Electrek, Sep 2026): https://electrek.co/2026/09/22/tesla-robotaxi-active-fleet-austin-crashes-8-vehicles/
- Tesla 1 M unsupervised miles: https://electrek.co/2026/09/03/tesla-announces-1-million-unsupervised-miles-driven-by-robotaxi/
- Koopman on Tesla safety data: https://philkoopman.substack.com/p/new-tesla-fsd-safety-data
- Mobileye safety architecture: https://static.mobileye.com/website/us/corporate/files/SDS_Safety_Architecture.pdf
- Xpeng "lidar no longer necessary": https://cnevpost.com/2026/05/21/xpeng-defends-pure-vision-strategy-says-lidar-no-longer-necessary/
- NVIDIA Hyperion 10: https://nvidianews.nvidia.com/news/nvidia-uber-robotaxi
- LET-3D-AP (Waymo): https://arxiv.org/abs/2206.07705
- Far3D: https://arxiv.org/abs/2308.09616
- Bijelic et al., lidar in fog: https://arxiv.org/abs/1912.03251
- K-Radar: https://arxiv.org/abs/2206.08171
- RAND RR-1478: https://www.rand.org/pubs/research_reports/RR1478.html
- NTSB HAR-19/03: https://www.ntsb.gov/investigations/AccidentReports/Reports/HAR1903.pdf
- RSS paper: https://arxiv.org/abs/1708.06374

**Headlights (§A6)**
- IIHS headlight rating rationale (aim tolerance, 5 lux metric, high-beam use): https://www.iihs.org/media/9b0f599a-7a50-4bc4-b8d2-1cf6b52a128a/VSGFZg/Ratings/Protocols/current/headlight_rationale_supporting_work.pdf
- IIHS headlight test protocol v3: https://www.iihs.org/media/0e823704-32d1-4500-b095-15d064d824a7/ZJciYw/
- IIHS, good headlight ratings linked to lower crash rates: https://www.iihs.org/news/detail/good-iihs-headlight-ratings-linked-to-lower-crash-rates
- UMTRI, real-world use of high-beam headlamps (Mefford et al.): https://deepblue.lib.umich.edu/handle/2027.42/58716
- Wood, Tyrrell & Carberry 2005, *Human Factors*: https://doi.org/10.1518/001872005774859980
- Pedestrian visibility at night (clothing, driver age, beam setting): https://www.researchgate.net/publication/228414781_Pedestrian_visibility_at_night_Effects_of_pedestrian_clothing_driver_age_and_headlamp_beam_setting
- NHTSA ADB final rule (Feb 2022): https://www.federalregister.gov/documents/2022/02/22/2022-02451/federal-motor-vehicle-safety-standards-lamps-reflective-devices-and-associated-equipment-adaptive
- NHTSA denial of ADB petitions (Dec 2024): https://www.govinfo.gov/content/pkg/FR-2024-12-30/html/2024-31141.htm
- Rivian the only US ADB (CarBuzz): https://carbuzz.com/only-car-brand-full-adaptive-driving-beam-headlights-america-rivian/
- FMVSS 108, 75,000 cd upper-beam maximum: https://www.federalregister.gov/documents/2009/08/24/E9-20258/federal-motor-vehicle-safety-standard-no-108-lamps-reflective-devices-and-associated-equipment
- ECE-R123 B50L 50–350 cd (Scientific Reports 2026): https://www.nature.com/articles/s41598-026-44526-0
- BMW Laserlight, 600 m high beam: https://www.press.bmwgroup.com/global/article/detail/T0165849EN/bmw-laser-light-goes-into-series-production-the-bmw-i8-is-the-first-production-vehicle-to-feature-the-innovative-light-technology?language=en
- IIHS on headlight glare and crashes (2025): https://www.repairerdrivennews.com/2025/10/20/iihs-study-says-crashes-havent-increased-due-to-headlight-glare/

**Western brands in China (§B6)**
- CarNewsChina, VW Group China sales 2025: https://carnewschina.com/2026/01/13/volkswagen-groups-sales-declined-by-8-y-o-y-in-china-as-the-top-selling-foreign-auto-brand-in-2025/
- Automotive World, VW loses share, falls behind Geely and BYD: https://www.automotiveworld.com/topics/oems/vw-loses-share-in-china-falls-behind-geely-and-byd/
- Autocar Pro (Reuters), Jan–Feb 2026 rankings: https://www.autocarpro.in/news/byd-falls-to-fourth-and-volkswagen-reclaims-top-spot-in-china-sales-reuters-reports-131650
- VW Group Annual Report 2025, deliveries: https://annualreport2025.volkswagen-group.com/group-management-report/business-development/deliveries.html
- CarNewsChina, Toyota bZ3X launch (RoboSense lidar, Momenta): https://carnewschina.com/2025/03/07/all-electric-toyota-bz3x-suv-launched-for-15100-usd-its-65-chinese/
- Electrek, bZ3X top-selling JV EV: https://electrek.co/2026/05/07/toyotas-15k-electric-suv-chinas-top-selling-joint-venture-ev-7-months/
- CnEVPost, Hesai to supply Toyota JV: https://cnevpost.com/2025/08/15/hesai-to-supply-lidars-toyota-china/
- CnEVPost, VW ID. UNYX 08 and the Xpeng partnership: https://cnevpost.com/2026/04/16/vw-launches-id-unyx-08-china-xpeng-partnership/
- Gasgoo, joint-venture NEVs gaining momentum (Sep 2026): https://autonews.gasgoo.com/articles/ev/joint-venture-nevs-are-gaining-momentum-in-china-2102381343702196225
- France 24, "joint venture in reverse": https://www.france24.com/en/live-news/20260427-joint-venture-in-reverse-foreign-carmakers-seek-edge-with-china-partners
- 36Kr, Chengdu Auto Show preview (JV lidar models): https://eu.36kr.com/en/p/3946674996336265

**Fastree3D history (§C5)**
- Hesai, Fastree3D acquisition / FTX (27 Feb 2025): https://www.hesaitech.com/hesai-strengthens-patent-portfolio-with-swiss-ip-acquisition-advancing-next-gen-solid-state-lidar-ftx-to-drive-robotics-revolution/
- Laser Focus World, founder interview (Oct 2021): https://www.laserfocusworld.com/executive-forum/article/14210746/founder-of-fastree3d-advances-flash-lidar-by-combining-a-fast-detector-with-readout-electronics-for-3d-imaging
- Fastree3D "About us": https://www.fastree3d.com/about-us/
- Inno-Forum Lausanne interview (Dec 2020): https://lausanne.inno-forum.org/innovator-of-the-month-interview-with-fastree3d/
- Venturelab profile: https://www.venturelab.swiss/Fastree3d
- Crunchbase: https://www.crunchbase.com/organization/fastree3d
- Edoardo Charbon (bio): https://en.wikipedia.org/wiki/Edoardo_Charbon
- Knowmade, Hesai lidar patent landscape (Nov 2025): https://www.knowmade.com/technology-news/semiconductor-news/sensing-imaging-news/from-competitor-to-leader-hesai-in-lidar-patent-landscape/

**Gap-fill pass (27 Sep 2026)**
- Seyond Robin E1X datasheet (940 nm): https://www.seyond.com/wp-content/uploads/2025/03/Robin-E1X-LiDAR-C-sample_Datasheet_EN_Public_V3.0.0-2.pdf
- Seyond Robin E1X user manual: https://www.seyond.com/wp-content/uploads/2025/03/Seyond-Robin-E1X_LiDAR_User-Manual_EN_V1.3.1_20250114.pdf
- Hesai ETX product page (300 m spec table): https://www.hesaitech.com/product/etx/
- Hesai ETX at IAA 2025 (400 m, 800 channels): https://www.hesaitech.com/hesai-showcases-next-gen-high-performance-lidars-at-iaa-mobility-2025-mass-production-expected-in-2026/
- Gasgoo, Picasso (2,160 lines per chip; 4,320 lines = 2 chips): https://autonews.gasgoo.com/articles/market-industry/hesai-unveils-picasso-spad-chip-lidar-enters-6d-full-color-era-2046161208086880257
- Huawei 896-line launch: https://auto.huawei.com/cn/news/2026/2026-3-4-lidar
- Sina (896-line wide/tele FOV): https://finance.sina.com.cn/cj/2026-03-06/doc-inhpzkwq2593695.shtml
- Sohu / 雪岭飞花, Huawei 192-line teardown notes: https://www.sohu.com/a/770979130_468661
- RoboSense Eocene PR (28 nm, hybrid bonding): https://www.prnewswire.com/news-releases/robosense-unveiled-eocene-spad-soc-architecture-and-chipsets-phoenix-and-peacock-ushering-the-lidar-industry-into-the-image-grade-era-of-high-definition-3d-perception-302748401.html
- RoboSense–Adaps litigation background: https://www.tmtpost.com/7820009.html
- Hesai ATX teardown summary (MyDrivers): https://news.mydrivers.com/1/1049/1049493.htm
- Nikkei Asia, RoboSense Southeast Asia plant: https://asia.nikkei.com/business/technology/chinese-lidar-maker-building-first-overseas-plant-in-southeast-asia
- Hesai CES 2026 capacity and Thailand plant: https://www.hesaitech.com/hesai-announces-plan-to-double-annual-lidar-production-capacity-at-ces-2026/
- Volvo EX90 production statistics (Volvo Owners Club): https://www.volvoclub.org.uk/history/ex90_stats_search.shtml
- Fortune, Mercedes Drive Pilot in California (Apr 2024): https://fortune.com/2024/04/18/mercedes-self-driving-autonomous-cars-california-nevada-level-3-drive-pilot
- JESMB, Drive Pilot unit numbers vs system cost: https://jesmb.de/31483/
- heise, BMW drops Level 3: https://www.heise.de/news/Autonomes-Fahren-BMW-streicht-Level-3-aus-7er-Reihe-11186428.html
- optics.org, Hesai–Mercedes Level 3: https://optics.org/news/hesai-sees-level-3-lidar-shift-with-mercedes-benz
- Teslarati, Tesla unsupervised fleet (Aug 2026): https://www.teslarati.com/tesla-surges-robotaxi-fleet-ahead-of-cybercab-launch-event/
- ChargePort robotaxi tracker: https://thechargeport.com/robotaxi-tracker
- Nissan next-gen ProPILOT (1 lidar): https://global.nissannews.com/en/releases/next-gen-propilot-technology
- Nikkei xTech, Nissan 2022 demo with Luminar: https://xtech.nikkei.com/atcl/nxt/column/18/01537/00353/
- MicroVision Q4 2025 call: https://www.fool.com/earnings/call-transcripts/2026/03/04/microvision-mvis-q4-2025-earnings-transcript/
- NVIDIA blog, Lucid Gravity sensor suite: https://blogs.nvidia.com/blog/lucid-gravity-suv-nvidia-drive/
- Aurora 2022 business update (9 lidars): https://www.sec.gov/Archives/edgar/data/1828108/000182810822000041/businessupdatepresentati.htm
- Reuters exclusive, Rivian lidar (via Investing.com): https://www.investing.com/news/stock-market-news/exclusiverivian-mulls-making-its-own-lidar-sensors-possibly-in-partnership-with-chinese-firms-4661573
- FLIR/Veoneer night-vision milestones: https://oem.flir.com/about/news/flir-technology-used-in-new-night-vision-system-from-veoneer/

**Rivian lidar supplier (update)**
- InsideEVs, Rivian may build its own lidar in the US: https://insideevs.com/news/795006/rivian-r2-lidar-us-build-ceo/
- EV, Rivian denies RoboSense is its R2 supplier: https://eletric-vehicles.com/rivian/rivian-denies-robosense-is-its-lidar-supplier-for-the-r2/
- EV, undisclosed supplier points to RoboSense: https://eletric-vehicles.com/rivian/rivians-undisclosed-self-driving-lidar-supplier-points-to-chinas-robosense/
- Rivian Forums (Reuters), "no plans today" for in-house lidar: https://www.rivianforums.com/forum/threads/rivian-has-no-plans-today-to-bring-lidar-development-in-house.59792/
