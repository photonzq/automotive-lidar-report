"""New section C3d (what teardowns and the makers' own disclosures show inside commercial lidars), its pointers, an
Appendix 1 item, a wider Appendix 2 group with the source report of each teardown image, and a correction in D1.

Each fact was read at its source:
- Yole SystemPlus: "What's in the box?" articles on the Hesai AT128 (19 Aug 2024; 128 Lumentum five-junction VCSEL
  dies of 0.17 mm2 in 16 bands of 8; EBOM: 72% of the components from US suppliers and 11% Chinese, largely Hesai's
  20 ASICs; by cost the Xilinx processor 33% and the ASICs 21%), on Chinese lidars (Dec 2023; Falcon: 1,550 nm seed,
  940 nm pump, about 6 m of erbium-doped fibre, 28 W, 1.9 times the M1, BOM 1.7 times; M1: five laser and SiPM
  modules) and on automotive lidars (Dec 2023; manufacturing cost 1.6 times SCALA Gen. 1 for Gen. 2 and 2.7 times for
  the M1; Continental's flash the only commercialized fully solid-state unit, under 50 m); the SCALA Gen. 1/Gen. 2
  article (Sep 2022; 780 and 890 components, electronic cores of about $70 and $110); the H800 article (3 May 2023);
  the AT128 teardown image; the teardown-track pages with their codes and dates; the Feb 2024 list of lidar tracks;
  a catalogue search for FMCW (no product).
- TechInsights: product-page summaries (AT128, Huawei 192-line L306, HFL110, Iris, Robin E1X and the product pages
  of the Falcon Kinetic, M1, Huawei 96-line L106, H800, OS1-64 and SCALA Gen. 2) and the partial teardowns on
  Electronics360 (Hesai ATX, Continental HFL110, Huawei 96-line, Valeo SCALA Gen. 2, Ouster OS1-64, Velodyne H800,
  Velodyne VLP-16, Innovusion Falcon Kinetic, LeiShen); the cost sums come from build/figures/teardown_component_costs.py.
- System Plus Consulting summaries: SCALA Gen. 1 (PR Newswire, 2019) and Livox Horizon (Embedded Computing Design,
  2020). CITIC Securities' teardown of five lidars (Sep 2022, Tencent News repost); NE Times' summary of 26 lidar
  teardowns (Dec 2025); the Huawei 96-line teardown with 55 photographs (Sohu repost).
- FMCW makers: Aurora's posts (2026 photonic engine; 2021 Sen Lin interview; 2020 wavelength), Aeva's 10-K for 2025
  (Item 1), its 2025 investor deck (slides 63 and 67, rendered) and the Aeries II release (1 Feb 2022), SiLC as
  relayed by Robotics 24/7, Baraja's 2023 blog, Voyant's products page, Scantinel's Oct 2024 white paper (pp. 6-8,
  rendered) and Mobileye's CES 2021 page.
- Wikimedia Commons licences, authors and sizes from the Commons API.

Usage: teardown_section_edit.py <report.md> <expected sha256 prefix> [--write]
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

# ---------------------------------------------------------------- reading guide, Part C overview and intro
TOC_ANCHOR = ("  - mechanical beam steering in numbers: scanner speed limits, vibration qualification, designs and what "
              "shipped (§C4d);\n")
TOC_ADD = ("  - what teardowns show inside shipped lidars (lasers, detectors, scanners, processors and where the cost "
           "sits) and what FMCW makers have shown of their own hardware (§C3d);\n")
PARTC_OLD = "company routes and the investment cycle, wavelength choice, receivers,"
PARTC_NEW = "company routes and the investment cycle, what teardowns show inside shipped lidars, wavelength choice, receivers,"
INTRO_OLD = "the companies behind them (§C1–§C3c), why 905/940 nm silicon receivers"
INTRO_NEW = ("the companies behind them (§C1–§C3c), what teardowns show inside the shipped hardware (§C3d), why "
             "905/940 nm silicon receivers")

# ---------------------------------------------------------------- the new section, before C4
C4_HEAD = "## C4. Why 905/940 nm with silicon receivers and one mechanical axis won\n"
C3D = r"""## C3d. Inside commercial lidars: teardowns and the makers' own disclosures

This section asks what the published teardowns of commercial lidars show inside them: which lasers, detectors, scanners and processors actually shipped, and where the cost of a unit sits. A teardown is an analysis in which a firm takes a product apart, identifies its parts and estimates what they cost. It is the one independent look at the hardware, where a specification sheet is the maker's own claim (§C3b). The findings are the hardware behind the argument of §C4, and the reports and images linked here are the best public views of it, for example for slides.

**Short answer.**
- **At 1,550 nm the laser is a fibre amplifier chain.** Seyond's Falcon and Luminar's Iris carry their light in optical fibre from a seeded, pumped fibre laser, and in the one 1,550 nm unit with a published component list, a LeiShen lidar, the fibre-laser parts make up three-quarters of the listed cost (subsections 1 and 4).
- **At 905/940 nm the designs converged.** Emitters went from one or a few edge-emitting lasers to arrays of VCSELs (vertical-cavity surface-emitting lasers), detectors went from linear avalanche photodiodes (APDs) to SiPMs (silicon photomultipliers) and stacked SPAD (single-photon avalanche diode) arrays, and most forward-looking units scan one axis mechanically, usually with a rotating mirror (subsections 2 and 5).
- **No FMCW lidar has been torn down.** What is known of the inside of FMCW (frequency-modulated continuous-wave, coherent) lidars is what their makers have published, and every maker that describes its source uses a semiconductor laser and a semiconductor optical amplifier (SOA) on or beside a photonic chip, not a fibre laser (subsection 3).
- **The laser, optics, mirrors and housing cost more than the electronics** in six of the seven published component lists; the Valeo SCALA 2, with its large processor, is the exception (subsection 4).

**Where the evidence comes from.**
- **Yole SystemPlus** (formerly System Plus Consulting, part of Yole Group) sells teardown tracks (teardown photographs, block diagram, parts data and assembly) and reverse-costing reports. Its product pages carry no summary, but its free "What's in the box?" articles summarize the findings and show annotated teardown images [I].
- **TechInsights** sells "Deep Dive Teardown" reports, each with a one-paragraph public summary. Partial teardowns appear as sponsored articles on Electronics360, with board photographs, the chips found and the ten components with the highest estimated cost [I]. The "price" each article prints, for example \$4,847 for the Hesai ATX against the ≈\$200 reported for that unit (§C3c), is not explained there and is not used here.
- **Chinese teardowns.** CITIC Securities took five lidars apart for a Sep 2022 research report [I]. The engineer 雪岭飞花 ("Xueling") has published teardowns of 26 lidars, summarized by NE Times in Dec 2025 [T]; his teardown of a Huawei 96-line unit, with 55 photographs, is cited directly [I].
- The full reports are paywalled, so the facts below come from their public parts. The last column of each table links the reports, and Appendix 2 lists them with the teardown images and freely licensed photographs. Facts from a teardown are tagged [I], from NE Times' summary [T], and from a maker's description of its own hardware [P]. Appendix 1 lists the lidars for which no public teardown was found.

*Terms used in the tables.* An FPGA (field-programmable gate array) is a reconfigurable logic chip, and an ASIC (application-specific integrated circuit) a custom chip. An SoC (system on chip) combines processor cores with other functions; an MPSoC has several processor cores. LPDDR4 is low-power memory. A TIA (transimpedance amplifier) turns a detector's current into a voltage, an ADC (analog-to-digital converter) digitizes it, and a DSP (digital signal processor) extracts range and velocity. A VCO is a voltage-controlled oscillator. A GaN FET or a MOSFET is a fast transistor switch that delivers a laser's current pulse. A MEMS mirror is a micro-electro-mechanical mirror; a galvanometer mirror is turned by a small motor; a polygon is a rotating mirror with several facets. A MOPA (master-oscillator power amplifier) amplifies a low-power seed laser. III–V semiconductors such as InP (indium phosphide) are the compounds in which lasers and SOAs are made. A bill of materials (BOM; EBOM for the electronics) lists a product's parts with their cost. Class 1 is the lowest hazard class of the laser-safety standard IEC 60825-1 (§C4).

### 1. 1,550 nm time-of-flight lidars: fibre lasers inside

Three 1,550 nm units have public teardown findings, and all three use a fibre laser.

| Lidar (vehicle) | Laser and scanner | Detector and electronics | Power and cost | Teardown reports |
|---|---|---|---|---|
| **Seyond (Innovusion) Falcon** (NIO ET7) | A 1,550 nm seed fibre laser coupled with a 940 nm pump and about 6 m of erbium-doped fibre [I, Yole]. The output is split one to four; a rotating polygon scans horizontally and a galvanometer mirror vertically, four lines at a time [I, CITIC], and the polygon has five facets (§C4d subsection 2). Yole's cutaway labels a prism, a diffuser, a mirror and the coiled fibre [I] | Detector not named in the public summaries; Innovusion's patents describe a fibre-fed APD receiver (§C4b). Xilinx XAZU4EV processor, a higher-priced part than the RoboSense M1's XAZU2EG [I, Yole]. The Falcon Kinetic has a Xilinx UltraScale+ MPSoC with 2 GB of LPDDR4 and a detector board with Texas Instruments (TI) amplifiers [I, TechInsights] | 28 W, 1.9 times the 15 W of the RoboSense M1; a bill of materials about 1.7 times the M1's, mainly from costly, hard-to-source parts [I, Yole]. Falcon Kinetic manufacturing cost \$520.75, 53% of it modules, discretes and connectors (subsection 4) [I/E] | [Yole SPTA23244](https://www.yolegroup.com/product/teardown-track/innovusion-falcon-lidar-for-nio-et7-/) (Sep 2023); [TechInsights DDT-2208-806](https://www.techinsights.com/products/ddt-2208-806); [Electronics360](https://electronics360.globalspec.com/article/19252/techinsights-teardown-innovusion-falcon-kinetic) |
| **Luminar Iris** (Volvo EX90) | Light carried in optical fibres from two fibre-laser tips emitting at 1,550 nm; a rotating scan mirror plus a mechanical adjustment in the vertical, an architecture TechInsights likens to the Falcon Kinetic's [I, TechInsights] | A custom receiver ASIC from Black Forest Engineering, a Luminar company; a Xilinx FPGA; automotive Ethernet [I, TechInsights] | Not in the public summary | [TechInsights DDT-2306-807](https://www.techinsights.com/products/ddt-2306-807); [summary](https://www.techinsights.com/blog/deep-dive-teardown-luminar-technologies-iris-lidar-70-0034-00102203a15650-automotive) |
| **LeiShen**, model not named (released Aug 2022) | The three costliest listed parts are a fibre-optic cable (\$174.78), two laser-diode modules (\$142.90) and a fibre-coupled laser (\$56.31); the optical board carries a thermoelectric-cooler controller and a GaN/MOSFET driver [I, TechInsights]. These are the parts of a fibre MOPA: a fibre-coupled seed, pump diodes and fibre [E] | Xilinx Artix-7 FPGA; an Analog Devices wideband synthesizer with VCO and a 12-bit ADC [I, TechInsights] | Fibre-laser parts \$373.99 of the \$497.17 listed, 75% (subsection 4) [E] | [Electronics360](https://electronics360.globalspec.com/article/19675/techinsights-teardown-leishen-lidar-system) (2 Jun 2023) |

- **Which LeiShen unit.** TechInsights names neither the model nor the wavelength. The unit's release month, Aug 2022, is the month in which LeiShen launched its 1,550 nm LS series with an in-house fibre laser (§C4), so it is probably an LS-series unit [E].
- **Seed and amplifier gain.** CITIC puts the seed of a 1,550 nm lidar at a few milliwatts, amplified in fibre to a peak power of the order of 1 kW, against the order of 100 W for a 905 nm laser diode, so that one fibre laser can be split into several beams (the Falcon's four), where 905 nm designs use one laser per beam (the M1's five, the AT128's 128 below) [I, CITIC]. From a seed of 1–5 mW to 1 kW is a peak-power gain of $10\log_{10}(1{,}000/0.005)=53$ dB to $10\log_{10}(1{,}000/0.001)=60$ dB [E]. Such a gain is normally split between stages, so that amplified spontaneous emission (ASE) does not build up in one long high-gain stage, and the patents show that split: a pre-amplifier and a booster, with an ASE filter between them in Luminar's (§C4). A commercial 1,550 nm pulsed fibre laser for lidar is specified at 1.4 kW peak (§C4c subsection 1).
- **The 940 nm pump.** Plain erbium-doped silica absorbs only weakly at 940 nm, away from its 980 nm band, while 915–940 nm multimode diodes are the usual pumps of cladding-pumped erbium–ytterbium co-doped fibre, in which ytterbium absorbs the pump and passes the energy to erbium. The Falcon's gain fibre is therefore probably Er/Yb co-doped, which the public summaries do not state; Luminar's patent plots the cross-sections of erbium–ytterbium fibre beside those of erbium fibre (Figs. 17–18, §C4) [E].

### 2. 905/940 nm and flash lidars

The rotating-mirror and prism units come first, then the MEMS, wedge-prism and oscillating-mirror designs, the spinning units and the one flash unit. All are pulsed time of flight.

| Lidar (vehicle) | Laser | Detector | Scanner | Electronics, power and cost | Teardown reports |
|---|---|---|---|---|---|
| **Valeo SCALA Gen. 1** (Audi A8, 2017) | One pulsed edge-emitting laser from Laser Components, with three stacked active layers, rated 75 W, in a can package [I, System Plus] | A three-element silicon APD array from First Sensor, on the same board as the laser [I, System Plus] | A rotating mirror, with separate emitting and receiving lenses [I, System Plus] | 780 components; electronic core ≈\$70 [I, Yole] | [System Plus, 2019](https://www.prnewswire.com/news-releases/valeo-scala-laser-scanner-bill-of-material-bom-and-manufacturing-cost-report-2019-the-worlds-first-automotive-grade-lidar-sensor-for-automated-and-autonomous-driving-300851922.html); [Yole SPT20024](https://www.yolegroup.com/product/teardown-track/valeo-scala-lidar/) (May 2020) |
| **Valeo SCALA Gen. 2** (Honda Legend, Mercedes S-Class) | Not named in the public summaries | A Hamamatsu photosensor with front-end IC (\$11.92) [I, TechInsights] | A rotating mirror (§C3c) | Xilinx Zynq UltraScale+ SoC (\$52.73, the costliest listed part) and 2 × 2 GB of LPDDR4; a heated plastic window filter (\$11.08) [I, TechInsights]. 890 components; electronic core ≈\$110; manufacturing cost 1.6 times Gen. 1's [I, Yole] | [Yole SPTA22142](https://www.yolegroup.com/product/teardown-track/valeo-scala-gen-2-lidar/) (Jan 2022); [TechInsights DDT-2205-811](https://www.techinsights.com/products/ddt-2205-811); [Electronics360](https://electronics360.globalspec.com/article/18818/techinsights-teardown-valeo-lidar-scala-gen-2-laser-rangefinder) |
| **Hesai AT128** (Li Auto L9) | 128 Lumentum VCSEL dies of 0.17 mm² each, with five junctions (stacked emission zones), in 16 bands of 8; Yole calls it the first long-range lidar with VCSELs [I, Yole] | One avalanche detector per channel, 128 in all [I, TechInsights]; SiPMs (§C5) | A rotating mirror [I, Yole] | One Xilinx processor makes up 33% of the electronic bill of materials by cost, and Hesai's 20 ASICs 21% [I, Yole]; 18 W [P, via Yole] | [Yole SPTA24290](https://www.yolegroup.com/product/teardown-track/hesai-at128-lidar-for-liauto-l9/) (Jan 2024); [Yole article](https://www.yolegroup.com/strategy-insights/whats-in-the-box-hesai-at128-lidar-for-li-auto-l9-at-a-glance/) (Aug 2024); [TechInsights](https://www.techinsights.com/node/52820) |
| **Hesai ATX** (2025) | A VCSEL array of unknown make, the costliest listed part (\$9.72) [I, TechInsights] | SiPMs [T, NE Times], for 64 physical channels (§C5) | A one-dimensional oscillating mirror, the first in the series [T, NE Times]; TechInsights lists a transmitter and a receiver mirror [I] | Efinix Ti60 FPGA (\$3.91), an Infineon 32-bit microcontroller, and Hesai's own differential ADC driver and analog switch [I, TechInsights]; the ten listed parts total \$51.14 (subsection 4) [E] | TechInsights DDT-2505-806; [Electronics360](https://electronics360.globalspec.com/article/22673/techinsights-teardown-hesai-atx-lidar) |
| **Huawei 96-line** (D2, 2020; Avatr 11 and others) | Eight 905 nm edge-emitting lasers on two transmitter boards; a beam splitter divides the eight beams into 96, and a prism sets their angles [I, Xueling] | A Sony SPAD depth sensor [I, TechInsights; Xueling] | A rotating mirror with four facets [I, Xueling]; the four mirrors are the costliest listed part (\$76.36) [I, TechInsights] | Unit L106: two Lattice FPGAs and a HiSilicon 8K camera SoC [I, TechInsights]; the unit Xueling opened: a TI TDA4-family processor and an FPGA [I]. A heated infrared window filter (\$58.23) [I, TechInsights] | [TechInsights DDT-2305-817](https://www.techinsights.com/products/ddt-2305-817); [Electronics360](https://electronics360.globalspec.com/article/20215/techinsights-teardown-huawei-96-line-lidar); [Xueling, 55 photographs](https://www.sohu.com/a/770979130_468661) |
| **Huawei 192-line** (D3, unit L306; AITO M9) | Four 905 nm emitters [I, TechInsights], reported as VCSEL line arrays (§C3) | One SPAD sensor of 189 × 600 pixels, the physical array of Sony's IMX459 design (§C5) [I, TechInsights] | A four-sided rotating prism with a magnetic position encoder [I, TechInsights] | A complete redesign of the L106 that shares some major chips with it; aluminium-alloy enclosures, glass lenses and filters, and mechanical parts much costlier than average [I, TechInsights] | [TechInsights](https://www.techinsights.com/node/57516); [Yole SPTA24344](https://www.yolegroup.com/product/teardown-track/huawei-192-line-lidar-for-luxeed-s7--aito-m9/) (Oct 2024) |
| **RoboSense M1** (Xpeng G9 and others) | Five 905 nm lasers, one per optical module [I, Yole] | One SiPM per module [I, Yole], made by Hamamatsu [I, CITIC] | One two-axis MEMS mirror above the five modules, whose alignment is the main difficulty in assembly [I, Yole]; a 7 mm mirror (§C4d) | Xilinx XAZU2EG [I, Yole]; a Xilinx SoC and an STMicroelectronics microcontroller [I, TechInsights]. 15 W; manufacturing cost 2.7 times SCALA Gen. 1's [I, Yole] | [Yole SPTA21068](https://www.yolegroup.com/product/teardown-track/robosense-rs-lidar-m1-lidar-sample-version/) (sample, Jan 2021); [Yole SPTA24314](https://www.yolegroup.com/product/teardown-track/robosense-m2-lidar--for-chery-exceed-es/) (M2, Mar 2024); [TechInsights DDT-2104-835](https://www.techinsights.com/products/ddt-2104-835) |
| **Livox** (DJI): Horizon; HAP (Xpeng P5); Mid-360 | Horizon: a Hamamatsu pulsed laser [I, System Plus] | Horizon: a custom Hamamatsu die of six APDs behind a 905 nm narrow band-pass filter [I, System Plus]; Mid-360: a custom Hamamatsu APD [T, NE Times] | HAP: two rotating wedge prisms [I, CITIC]; Mid-360: a double prism, with laser and detector fixed [T, NE Times] | Mid-360: GaN laser switches and TI TIAs (§D1a) | [System Plus, 2020](https://www.embedded-computing.com/hardware/yole-and-system-plus-consulting-investigate-the-lidar-industry-and-its-disruptive-technologies); [Yole SPT20041](https://www.yolegroup.com/product/teardown-track/livox-horizon-lidar/) (Horizon, Jul 2020); [Yole SPTA22189](https://www.yolegroup.com/product/teardown-track/livox-hap-t1-lidar/) (HAP, Sep 2022) |
| **Velodyne Velarray H800** | Long range: eight edge-emitting lasers in a 14.1 × 8.9 × 2.05 mm micro-lidar array, each EPC2715 GaN driver pulsing two of them; short range (0.1–20 m): four ams OSRAM five-junction 905 nm VCSEL dies, made by Vixar, behind a diffractive element that projects a dot pattern [I, Yole] | Eight silicon APDs in the same array, behind a MEMS beam splitter, shared by both illuminators [I, Yole] | A dual-axis oscillating mirror, the first in an automotive lidar [I, Yole] | Xilinx Artix-7 FPGA; the eight lasers are the costliest listed part (\$26.15) [I, TechInsights]; marketed at \$500 [I, Yole] | [Yole SPR23728](https://www.yolegroup.com/product/report/velodyne-short-and-long-range-lidar-with-vcsel-and-eel/); [Yole SPTA23214](https://www.yolegroup.com/product/teardown-track/velodyne-velarray-h800-lidar/) (Jan 2023); [Yole article](https://www.yolegroup.com/strategy-insights/velodynes-h800-lidar-a-noteworthy-progress-in-integration-practices-based-on-vcsel-and-laser-technologies/) (May 2023); [TechInsights DDT-2210-805](https://www.techinsights.com/products/ddt-2210-805); [Electronics360](https://electronics360.globalspec.com/article/19744/techinsights-teardown-velodyne-velarray-h800-lidar) |
| **Velodyne VLP-16** (Puck, 2016) | 16 channels, not described in the public summary | Not described | The head spins | Two Intel Cyclone III FPGAs; total manufacturing cost \$247.48 [I, TechInsights] | [Electronics360](https://electronics360.globalspec.com/article/16089/teardown-velodyne-lidar-puck-vlp-16-sensor) |
| **Ouster OS1-64** | One VCSEL array (\$10.46) [I, TechInsights] | One SPAD array (\$7.23) [I, TechInsights] | The head spins (§C4d) | A Xilinx Artix-7 FPGA on the rotor board and a Xilinx Zynq SoC on the main board; a Peltier module (\$7.53) [I, TechInsights] | [TechInsights DDT-2104-837](https://www.techinsights.com/products/ddt-2104-837); [Electronics360](https://electronics360.globalspec.com/article/17802/techinsights-teardown-ouster-os1-64-lidar-sensor) |
| **Continental HFL110** (Toyota Mirai 2; flash) | A 1,064 nm, Class 1 laser module, the costliest listed part (\$150.53) [I, TechInsights] | Continental's own 32 × 128 SPAD array (\$30.20) [I, TechInsights] | None: a stationary optical element spreads the light over 120° × 30°, to 50 m [I, TechInsights]; the only commercialized fully solid-state automotive lidar [I, Yole] | AMD (Xilinx) Artix-7 FPGA [I, TechInsights] | [Yole SPTA23218](https://www.yolegroup.com/product/teardown-track/continental-hfl110-3d-flash-lidar-for-toyota-mirai-2/) (Mar 2023); [TechInsights](https://www.techinsights.com/node/54392); [Electronics360](https://electronics360.globalspec.com/article/20837/techinsights-teardown-continental-3d-flash-lidar) |

- **Two disagreements, given as found.** For the AT128, TechInsights' summary also says that the unit has 32 laser transmitters and receivers while keeping the channel count of LeiShen's CH128X1, against Yole's 128 separate VCSEL dies, which Yole's photograph shows on a board with four identical driver-like packages; the paid reports would show whether 32 counts drivers or channels [I/E]. For the Huawei 96-line, the two units taken apart carry different processors (table); they may be different production versions [E].
- **What Yole's AT128 shares count.** 72% of the components came from US suppliers, mainly Lumentum and TI, and 11% from Chinese ones, largely Hesai's 20 ASICs [I]. These are shares of the components, not of their value, since by cost Hesai's ASICs alone come to 21% [I/E] (§D1).
- **Seyond's Robin E1X**, a 940 nm unit, has also been torn down by TechInsights; the public summary gives only its specification (120° × 20°, up to 96 lines, 6 W typical, 470 g) [I].

### 3. FMCW lidars: what the makers have shown

No physical teardown of an FMCW or other coherent lidar has been published. Yole's catalogue returns no product for "FMCW", and the TechInsights lidar teardowns found are all of time-of-flight units [I]. What is known of the inside comes from the makers, who have shown more than most teardown summaries do: die photographs, open packages and descriptions of their photonic chips [P].

| Maker (product) | What is inside, by the maker's account | Pictures published | Sources |
|---|---|---|---|
| **Aurora** (FirstLight; from Blackmore and OURS) | A "photonic engine": one multi-chip module that generates, amplifies, modulates, transmits and detects the light, with III–V lasers and Aurora's own optical amplifiers, low-loss silicon-nitride waveguides, custom photodiodes 25% more sensitive than the foundry's library device, and micro-lenses actively aligned between the chips during assembly. Its first FMCW systems were built from discrete fibre components, lasers and transceivers [P]. It works around 1,550 nm [P, 2020] | The packaged engine, and the engine emitting through its window on a test board (2026) | [Aurora, 2026](https://aurora.tech/newsroom/inside-auroras-photonic-engine-engineering-lidar-for-automotive-scale); [Aurora, 2021](https://aurora.tech/newsroom/meet-sen-lin-auroras-silicon-photonics-director-and); [Aurora, 2020](https://aurora.tech/newsroom/fmcw-lidar-the-self-driving-game-changer) |
| **Aeva** (Aeries II, Atlas) | Its own semiconductor laser, made in a III–V process already used for telecom parts, without fibre; low-cost photodetectors integrated on the silicon-photonics chip instead of SPADs or APDs; a custom DSP ASIC [P, 10-K for 2025, Item 1]. Its investor deck shows the laser, the SOA, the laser-driver and TIA ASIC and the silicon-photonics die, assembled into one "CoreVision" module that holds all the optical parts, and names TSMC and Tower for the chips, Fabrinet for optical assembly and Jabil for final assembly [P, slides 63 and 67]. Aeries II (Feb 2022) was its first design with no fibre optics [P]. Aeva does not publish its wavelength | Micrographs of the four dies and the module (deck slide 63) | [10-K](https://www.sec.gov/Archives/edgar/data/1789029/000119312526116518/aeva-20251231.htm); [investor deck, 2025](https://investors.aeva.com/static-files/10710a84-7fef-4c7d-ae1e-274e4da96583); [Aeries II release](https://www.aeva.com/press/aeva-introduces-aeries-ii-the-worlds-first-4d-lidar-with-camera-level-resolution/) |
| **SiLC** (Eyeonic) | One silicon-photonics chip carrying lasers, amplifiers, detectors and passive devices; the lasers are made by a partner fab in Japan; 1,550 nm [P, relayed by Robotics 24/7, Dec 2021] | An open-lid photograph of the fibre-less sensor (2021) | [Robotics 24/7](https://www.robotics247.com/article/silc_releases_chip_integrated_eyeonic_lidar_sensor/manufacturing); [photograph](https://silc.com/wp-content/uploads/2021/12/SiLC_Fiberless_Eyeonic_in_Human_Hand.jpg) |
| **Baraja** (Spectrum HD) | A 3 × 3.5 cm hermetic, temperature-controlled sub-assembly holding an InP laser chip, a silicon-photonics homodyne receiver chip and silicon TIAs with micro-optics; a separately packaged SOA with its own thermoelectric cooler, which Baraja calls 50–80 times smaller and lower in power than the fibre amplifiers of 1,550 nm lidars, its own first generation included; a silica chip for dispersion and steering; a bought-in automotive SoC instead of its own ASIC [P] | The sub-assembly open and sealed, and the packaged SOA (2023) | [Baraja, 2023](https://www.baraja.com/en/blog/power-of-integration) |
| **Voyant** (Carbon) | Beam steering on the chip in one axis: a photonic array of surface-emitting antennas behind a fixed lens, 128 pixels with 8 beams active at a time and pixel times down to 8 µs; a moving mirror scans the other axis [P] | Renders and a board photograph | [Voyant](https://voyantphotonics.com/products/) |
| **Scantinel** (assets to MicroVision, §C3a) | A hybrid III–V-on-silicon tunable laser with narrow linewidth, chirped by modulating its wavelength directly; hybrid-integrated arrays of SOAs on the silicon photonics; a chip from a standard CMOS foundry that runs several FMCW channels in parallel along one solid-state axis behind a collimating lens, with the other axis scanned separately [P, white paper, pp. 6–8] | Bare-die photographs | [White paper, Oct 2024](https://scantinel.com/wp-content/uploads/2024/11/Scantinel_Whitepaper_202410.pdf) |
| **Mobileye / Intel** (ended Sep 2024, never sold) | A silicon-photonics chip from Intel's New Mexico fab with active and passive laser elements on it and 184 vertical lines, which optics then move [P] | The chip on its carrier board (credited to Intel, 2021) | [Mobileye, Jan 2021](https://www.mobileye.com/news/ces-2021-mobileye-avs-on-move/) |

- **Voyant's point rate.** Eight beams at 8 µs per pixel give $8/(8\times10^{-6}\ {\rm s})=1.0\times10^{6}$ points per second, within about 2% of its stated 977,000 [E].
- **Semiconductor amplifiers instead of fibre.** Every coherent maker that describes its source has replaced the fibre laser and erbium amplifier with a semiconductor laser and an SOA on or beside a silicon-photonics chip: Aurora, Aeva, Baraja and Scantinel name an SOA, and SiLC puts amplifiers on its chip [P]. Aurora's first systems and Baraja's first generation used fibre, and both makers have left it [P]. The pulsed lidars of subsection 1 have not taken this step, for a physical reason [E]. An excited erbium ion lives for about 10 ms, so a fibre amplifier stores pump energy between pulses and releases it in kilowatt pulses a few nanoseconds long. The carriers in an SOA recombine within about a nanosecond, so an SOA amplifies the continuous light of an FMCW lidar well but cannot build kilowatt pulses.
- **Shared suppliers.** Fabrinet assembles Aeva's optics and builds Aurora's second hardware generation (Appendix 1), and Tower makes chips for Aeva and for LightIC (§C7, §D7) [P].

### 4. Where the cost sits

TechInsights' Electronics360 articles list, for seven of the units above, the ten components with the highest estimated cost, or nine for the SCALA 2 [I]. Grouped by function, the lists show which parts dominate each design (Figure C3d and the table below) [E]. They are not complete bills of materials, so the shares are shares of the listed lines.

::::: capside
![Share of the listed components' estimated cost by function for seven lidars](automotive_perception_report_figures/teardown_component_costs.png)

::: capbody
*Figure C3d.* Share of the estimated cost of the components TechInsights lists for each lidar, by function; the dollar figure under each name is the sum of the listed lines.
- Ten lines per lidar (nine for the Valeo SCALA 2), from TechInsights' partial teardowns on Electronics360 [I].
- *Laser source* includes the LeiShen unit's fibre and fibre-coupled parts and the H800's GaN laser drivers; *mirrors* are the Huawei unit's four rotating-mirror facets and the ATX's transmitter and receiver mirrors.
- Segments under 11% carry no label; the table below gives every value.
- *Script:* `build/figures/teardown_component_costs.py` [E].

:::
:::::

**Listed cost by function** (US\$) [I/E]:

| Lidar | Laser source | Detector | Mirrors | Lenses, filters, windows | Processors, memory | Housing, frames | Boards, cables, other | Listed total |
|---|---|---|---|---|---|---|---|---|
| LeiShen fibre-laser unit | 373.99 | — | — | 55.41 | 14.76 | 26.05 | 26.96 | 497.17 |
| Continental HFL110 (flash) | 150.53 | 30.20 | — | 52.79 | 9.00 | 19.36 | 4.16 | 266.04 |
| Huawei 96-line | — | — | 76.36 | 66.79 | 43.07 | 67.55 | 10.98 | 264.75 |
| Valeo SCALA 2 (nine lines) | — | 11.92 | — | 21.07 | 68.95 | 19.33 | 31.54 | 152.81 |
| Velodyne Velarray H800 | 36.06 | — | — | 17.81 | 15.15 | 32.25 | 6.41 | 107.68 |
| Ouster OS1-64 | 10.46 | 7.23 | — | 12.98 | 29.99 | 17.22 | 7.53 | 85.41 |
| Hesai ATX | 9.72 | — | 7.36 | 8.24 | 8.90 | 12.30 | 4.62 | 51.14 |

A dash means that no part of that function is among the listed lines.

*How the numbers are derived* [E]:
- Each cell sums the listed lines of one function; the figure script prints every line with the function assigned to it. The LeiShen unit's laser source is $174.78+142.90+56.31=373.99$ dollars, and $373.99/497.17=0.75$ of its list; the HFL110's laser module is $150.53/266.04=0.57$ of its list, and the ATX's VCSEL array $9.72/51.14=0.19$.
- The Huawei 96-line's mirrors, optics and housing come to $(76.36+66.79+67.55)/264.75=210.70/264.75=0.80$ of its list, and the ATX's to $(7.36+8.24+12.30)/51.14=27.90/51.14=0.55$. The SCALA 2's processor and memory come to $68.95/152.81=0.45$; the Ouster's, $29.99/85.41=0.35$, are level with its optics and housing, $(12.98+17.22)/85.41=0.35$.
- For the Falcon Kinetic, TechInsights gives the manufacturing cost by category instead: \$276.36 of modules, discretes and connectors, \$129.61 of non-electronic parts, \$84.90 of integrated circuits, and $14.53+6.75+5.64+2.96=29.88$ dollars of substrates, component insertion, assembly and test, \$520.75 in all. The first category, which would hold the laser modules, is $276.36/520.75=0.53$ [I/E]. The VLP-16's total manufacturing cost is \$247.48 [I].

**What the cost lists show** [E]:
- Where the laser is a single costly module, it dominates the list: 75% for the 1,550 nm fibre chain and 57% for the 1,064 nm flash laser. A 905 nm VCSEL array costs \$9.72 in the ATX and \$10.46 in the OS1-64, and the H800's eight edge emitters with their GaN drivers \$36.06.
- Where the laser is cheap, optics, mirrors and housing take the largest share (80% for the Huawei 96-line, 55% for the ATX), and two units list a heated window filter (Huawei 96-line, SCALA 2).
- Processors and memory lead only in the SCALA 2 (45%), whose Zynq UltraScale+ (\$52.73) is the costliest chip in any of the seven lists; the ATX's FPGA costs \$3.91.
- The listed totals fall from \$497 for the fibre unit to \$51 for the ATX, a unit reported at about \$200 (§C3c).

### 5. What the teardowns add up to [E]

1. **Pulsed time of flight at 1,550 nm means a fibre laser,** because an erbium amplifier stores pump energy between pulses and releases it as kilowatt peaks, which a semiconductor amplifier cannot do (subsections 1 and 3). The fibre chain accounts for the Falcon's 28 W against the M1's 15 W and for three-quarters of the LeiShen unit's listed cost; this is the hardware behind the cost and power argument of §C4.
2. **At 905/940 nm the number of emitters rose as the price fell:** one three-layer edge emitter (SCALA Gen. 1), five (M1), eight (Huawei 96-line and the H800's long range), then 128 VCSEL dies (AT128) and a \$9.72 VCSEL array (ATX).
3. **Detectors moved from linear APDs to photon counting:** a three-element APD array (SCALA Gen. 1) and a six-APD die (Livox Horizon); SiPMs (M1, AT128, ATX); and SPAD arrays: Ouster's, Sony's in the Huawei 96- and 192-line units, and Continental's own 32 × 128 (§C4b, §C5).
4. **One mechanical axis won the forward lidar:** rotating mirrors or prisms in the SCALA, AT128 and Huawei units, and a polygon with a galvanometer mirror at 1,550 nm. The alternatives are the M1's MEMS mirror, the oscillating mirrors of the ATX and the H800, Livox's wedge prisms, and flash below 50 m (HFL110) (§C4, §C4d).
5. **Processing moved from bought FPGAs towards the makers' own chips:** Xilinx parts in most units, Lattice in the Huawei 96-line and Efinix in the ATX, beside Hesai's 20 ASICs in the AT128, Luminar's receiver ASIC and Continental's own SPAD array (§D1a).
6. **The coherent makers left fibre** for semiconductor lasers and SOAs on photonic chips, a step that pulsed 1,550 nm lidars cannot take without giving up their kilowatt pulses (subsection 3).

Sources: https://www.yolegroup.com/yole-group-actuality/collection-of-lidar-teardowns-from-our-automotive-track/ ; https://www.yolegroup.com/strategy-insights/whats-in-the-box-chinese-automotive-lidars-at-a-glance/ ; https://www.edge-ai-vision.com/2023/12/whats-in-the-box-chinese-automotive-lidars-at-a-glance/ ; https://www.edge-ai-vision.com/2023/12/whats-in-the-box-automotive-lidars-at-a-glance/ ; https://www.edge-ai-vision.com/2022/09/first-and-second-generation-valeo-scala-lidars-the-technology-gap-revealed/ ; https://www.yolegroup.com/strategy-insights/whats-in-the-box-hesai-at128-lidar-for-li-auto-l9-at-a-glance/ ; https://www.yolegroup.com/strategy-insights/velodynes-h800-lidar-a-noteworthy-progress-in-integration-practices-based-on-vcsel-and-laser-technologies/ ; https://www.yolegroup.com/search-results/?search-term=FMCW ; https://www.prnewswire.com/news-releases/valeo-scala-laser-scanner-bill-of-material-bom-and-manufacturing-cost-report-2019-the-worlds-first-automotive-grade-lidar-sensor-for-automated-and-autonomous-driving-300851922.html (System Plus Consulting, Valeo SCALA) ; https://www.embedded-computing.com/hardware/yole-and-system-plus-consulting-investigate-the-lidar-industry-and-its-disruptive-technologies (System Plus Consulting, Livox Horizon) ; https://news.qq.com/rain/a/20220927A04DTZ00 (CITIC Securities, teardown of five lidars) ; https://www.ne-time.cn/web/article/37421 (NE Times, Xueling's 26 teardowns) ; https://www.sohu.com/a/770979130_468661 (Xueling, Huawei 96-line) ; https://www.techinsights.com/node/52820 ; https://www.techinsights.com/node/57516 ; https://www.techinsights.com/node/54392 ; https://www.techinsights.com/blog/deep-dive-teardown-luminar-technologies-iris-lidar-70-0034-00102203a15650-automotive ; https://www.techinsights.com/blog/summary-seyond-robin-e1x-lp-lidar080-ba-lidar-deep-dive-teardown ; https://www.techinsights.com/products/ddt-2306-807 ; https://www.techinsights.com/products/ddt-2208-806 ; https://www.techinsights.com/products/ddt-2104-835 ; https://www.techinsights.com/products/ddt-2305-817 ; https://www.techinsights.com/products/ddt-2205-811 ; https://www.techinsights.com/products/ddt-2104-837 ; https://www.techinsights.com/products/ddt-2210-805 ; https://electronics360.globalspec.com/article/19252/techinsights-teardown-innovusion-falcon-kinetic ; https://electronics360.globalspec.com/article/19675/techinsights-teardown-leishen-lidar-system ; https://electronics360.globalspec.com/article/18818/techinsights-teardown-valeo-lidar-scala-gen-2-laser-rangefinder ; https://electronics360.globalspec.com/article/22673/techinsights-teardown-hesai-atx-lidar ; https://electronics360.globalspec.com/article/20215/techinsights-teardown-huawei-96-line-lidar ; https://electronics360.globalspec.com/article/19744/techinsights-teardown-velodyne-velarray-h800-lidar ; https://electronics360.globalspec.com/article/16089/teardown-velodyne-lidar-puck-vlp-16-sensor ; https://electronics360.globalspec.com/article/17802/techinsights-teardown-ouster-os1-64-lidar-sensor ; https://electronics360.globalspec.com/article/20837/techinsights-teardown-continental-3d-flash-lidar ; https://aurora.tech/newsroom/inside-auroras-photonic-engine-engineering-lidar-for-automotive-scale ; https://aurora.tech/newsroom/meet-sen-lin-auroras-silicon-photonics-director-and ; https://aurora.tech/newsroom/fmcw-lidar-the-self-driving-game-changer ; https://www.sec.gov/Archives/edgar/data/1789029/000119312526116518/aeva-20251231.htm ; https://investors.aeva.com/static-files/10710a84-7fef-4c7d-ae1e-274e4da96583 ; https://www.aeva.com/press/aeva-introduces-aeries-ii-the-worlds-first-4d-lidar-with-camera-level-resolution/ ; https://www.robotics247.com/article/silc_releases_chip_integrated_eyeonic_lidar_sensor/manufacturing ; https://www.baraja.com/en/blog/power-of-integration ; https://voyantphotonics.com/products/ ; https://scantinel.com/wp-content/uploads/2024/11/Scantinel_Whitepaper_202410.pdf ; https://www.mobileye.com/news/ces-2021-mobileye-avs-on-move/
"""

# ---------------------------------------------------------------- C4 bullet, D1 wording
C4_BULLET_OLD = "Appendix 2 lists photographs of both lidars, the teardown images and these patent figures.\n"
C4_BULLET_NEW = ("§C3d sets these findings beside the other published teardowns, and Appendix 2 lists photographs of both "
                 "lidars, the teardown images and these patent figures.\n")
D1_OLD = ("  - **72% of component value came from US companies and 11% from Chinese ones**, and the Chinese share was "
          "almost entirely Hesai's own ASICs (application-specific integrated circuits, i.e. custom chips) [I].\n")
D1_NEW = ("  - **72% of the components came from US companies and 11% from Chinese ones**, and the Chinese share was "
          "largely Hesai's own ASICs (application-specific integrated circuits, i.e. custom chips) [I]. These shares "
          "count components rather than value: by cost, Hesai's ASICs alone came to 21% [I/E] (§C3d).\n")

# ---------------------------------------------------------------- Appendix 1
APPX1_ANCHOR = "- **Zeekr 9X blind-spot lidar (§B7.1).**"
APPX1_ADD = ("- **Teardowns (§C3d).** No public teardown was found of the Valeo SCALA 3, the InnovizOne or InnovizTwo, "
             "Cepton's Vista, RoboSense's M3, Ouster's OS2, Hesai's Pandar64 or any FMCW lidar, and nothing public "
             "shows the inside of Luminar's Iris beyond TechInsights' summary. Two counts disagree: the AT128's "
             "transmit channels (128 VCSEL dies by Yole, 32 transmitters and receivers by TechInsights) and the "
             "processors of the two Huawei 96-line units taken apart. Unknown: the model and wavelength of the "
             "LeiShen fibre-laser unit, the Falcon's detector, whether the Falcon's gain fibre is "
             "erbium–ytterbium co-doped, and the maker of the ATX's VCSEL array. The paid reports listed in §C3d "
             "would settle most of these.\n")

# ---------------------------------------------------------------- Appendix 2: the group written for §C4, widened
YOLE_IMG = "https://medias.yolegroup.com/uploads/2023/12/img-automotive-teardown-tracks_lidar-innovusion-and-robosense_"
OLD_HEAD = "**1,550 nm fibre-laser lidars: teardowns, patents and photographs (§C4)**\n"
OLD_YOLE_ARTICLE = (
    "- Yole SystemPlus, What's in the box? Chinese automotive LiDARs at a glance (19 Dec 2023; Seyond's Falcon: seed "
    "fibre laser, 940 nm pump and about 6 m of erbium-doped fibre, 28 W): "
    "https://www.yolegroup.com/strategy-insights/whats-in-the-box-chinese-automotive-lidars-at-a-glance/\n")
OLD_FALCON_IMG = (
    "- Yole SystemPlus, teardown image of Seyond's Falcon: the closed unit, the opened unit with its coiled fibre, and a "
    "labelled cutaway (3,482 × 2,250 px; © Yole SystemPlus 2023): " + YOLE_IMG + "2-1_ysp_november_2023.jpg\n")
OLD_COMPARE_IMG = (
    "- Yole SystemPlus, comparison of Seyond's Falcon and RoboSense's M1 (wavelength, power, field of view; © Yole "
    "SystemPlus 2023): " + YOLE_IMG + "1-3_ysp_november_2023.jpg\n")
OLD_TI_IRIS = (
    "- TechInsights, Deep Dive Teardown of the Luminar Technologies Iris LiDAR (summary: fibre-delivered light, two "
    "fibre-laser tips at 1,550 nm): https://www.techinsights.com/ja/node/53479\n")
KEEP = (
    "- Luminar Technologies, US 9,812,838 B2, Pulsed laser for lidar system (2017; seed and two amplifiers, abstract; "
    "one laser feeding several sensor heads through fibres, Figs. 5–7, sheet 4; double-pass fibre amplifier, Fig. 16, "
    "sheet 9; Er and Er/Yb cross-sections, Figs. 17–18, sheet 10): https://patents.google.com/patent/US9812838B2\n"
    "- Innovusion, US 11,614,521 B2, LiDAR scanner with pivot prism and mirror (2023; seed, pumps, pre-amplifier and "
    "booster, FIG. 4, sheet 4): https://patents.google.com/patent/US11614521B2\n"
    "- Wikimedia Commons, the Luminar lidar on the roof of a Volvo EX90, two photographs (CC0, 4,080 × 3,072 px): "
    "https://commons.wikimedia.org/wiki/File:Volvo_EX90_LiDAR_by_Luminar.jpg ; "
    "https://commons.wikimedia.org/wiki/File:Volvo_EX90_LiDAR_developed_by_Luminar.jpg\n"
    "- Wikimedia Commons, NIO ET7 with its roof lidar pod, IAA Mobility 2023 (Matti Blume, CC BY-SA 4.0, 4,608 × "
    "3,072 px): https://commons.wikimedia.org/wiki/File:Nio_ET7%2C_IAA_Mobility_2023%2C_Munich_%28P1110356%29.jpg\n"
    "- Seyond, Falcon K product page (1,550 nm, Class 1; 500 m, 250 m at 10%; more than 250,000 Falcon K1 delivered): "
    "https://seyond.com/products/falcon-k/\n")
APPX2_OLD = OLD_HEAD + OLD_YOLE_ARTICLE + OLD_FALCON_IMG + OLD_COMPARE_IMG + OLD_TI_IRIS + KEEP

YT = "https://www.yolegroup.com/product/teardown-track/"
E360 = "https://electronics360.globalspec.com/article/"
TI = "https://www.techinsights.com/"
CW = "https://commons.wikimedia.org/wiki/File:"
APPX2_NEW = (
    "**Teardowns of commercial lidars: reports, teardown images and photographs (§C3d, §C4)**\n"
    "\n*Overviews.*\n"
    "- Yole SystemPlus, LiDAR teardowns from the Automotive System Tracks (8 Feb 2024; its list of automotive lidar "
    "teardown tracks): https://www.yolegroup.com/yole-group-actuality/collection-of-lidar-teardowns-from-our-automotive-track/\n"
    "- Yole SystemPlus, What's in the box? Automotive LiDARs at a glance (Dec 2023; SCALA Gen. 1 as the cost "
    "reference, 1.6 times for Gen. 2 and 2.7 times for the RoboSense M1; Continental's flash lidar the only "
    "commercialized fully solid-state unit, under 50 m), reprint: "
    "https://www.edge-ai-vision.com/2023/12/whats-in-the-box-automotive-lidars-at-a-glance/\n"
    "- Yole SystemPlus, What's in the box? Chinese automotive LiDARs at a glance (19 Dec 2023; Seyond's Falcon: seed "
    "fibre laser, 940 nm pump and about 6 m of erbium-doped fibre, 28 W; RoboSense's M1: five laser and SiPM modules "
    "under one MEMS mirror): https://www.yolegroup.com/strategy-insights/whats-in-the-box-chinese-automotive-lidars-at-a-glance/ ; "
    "reprint: https://www.edge-ai-vision.com/2023/12/whats-in-the-box-chinese-automotive-lidars-at-a-glance/\n"
    "- CITIC Securities, 激光雷达产业深度研究：从拆解五款激光雷达看智能驾驶投资机遇 (a teardown of five lidars: LeiShen "
    "C16 and CH32, Seyond Falcon, RoboSense M1, Livox HAP; Sep 2022), Tencent News repost: "
    "https://news.qq.com/rain/a/20220927A04DTZ00\n"
    "- NE Times, 雪岭 · 26款激光雷达拆机分析——总结和展望 (summary of 雪岭飞花's teardowns of 26 lidars, Dec 2025): "
    "https://www.ne-time.cn/web/article/37421\n"
    "\n*1,550 nm fibre-laser lidars.*\n"
    "- Yole SystemPlus teardown track, Innovusion Falcon LiDAR for Nio ET7 (SPTA23244, Sep 2023), the source of the "
    "two Falcon images below: " + YT + "innovusion-falcon-lidar-for-nio-et7-/\n"
    "- Teardown image of Seyond's Falcon from that track: the closed unit, the opened unit with its coiled fibre, and "
    "a labelled cutaway (3,482 × 2,250 px; © Yole SystemPlus 2023): " + YOLE_IMG + "2-1_ysp_november_2023.jpg\n"
    "- Comparison of Seyond's Falcon and RoboSense's M1 from Yole SystemPlus's Falcon and M1 tracks (wavelength, "
    "power, field of view, processor; © Yole SystemPlus 2023): " + YOLE_IMG + "1-3_ysp_november_2023.jpg\n"
    "- TechInsights, Deep Dive Teardown of the Innovusion Falcon Kinetic NIO ET7 LIDAR (DDT-2208-806): "
    + TI + "products/ddt-2208-806 ; its partial teardown on Electronics360 (10 Feb 2023; boards and the "
    "manufacturing cost by category): " + E360 + "19252/techinsights-teardown-innovusion-falcon-kinetic\n"
    "- TechInsights, Deep Dive Teardown of the Luminar Technologies Iris LiDAR (DDT-2306-807; fibre-delivered light, "
    "two fibre-laser tips at 1,550 nm, a receiver ASIC from Black Forest Engineering): "
    + TI + "blog/deep-dive-teardown-luminar-technologies-iris-lidar-70-0034-00102203a15650-automotive ; "
    + TI + "products/ddt-2306-807\n"
    "- TechInsights Teardown: LeiShen lidar system (Electronics360, 2 Jun 2023; a fibre-optic cable, two laser-diode "
    "modules and a fibre-coupled laser among the listed parts): " + E360 + "19675/techinsights-teardown-leishen-lidar-system\n"
    + KEEP +
    "\n*905/940 nm and flash lidars.*\n"
    "- Valeo SCALA Gen. 1: System Plus Consulting report summary (PR Newswire, 2019; Laser Components laser, First "
    "Sensor APD array): https://www.prnewswire.com/news-releases/valeo-scala-laser-scanner-bill-of-material-bom-and-"
    "manufacturing-cost-report-2019-the-worlds-first-automotive-grade-lidar-sensor-for-automated-and-autonomous-"
    "driving-300851922.html ; Yole SystemPlus teardown track Valeo Scala LIDAR (SPT20024, May 2020): "
    + YT + "valeo-scala-lidar/\n"
    "- Valeo SCALA Gen. 1 and 2: Yole SystemPlus, First and Second Generation Valeo Scala LiDARs: the Technology Gap "
    "Revealed (Sep 2022; 780 and 890 components, electronic cores of ≈\\$70 and ≈\\$110; disassembly and board "
    "images), reprint: https://www.edge-ai-vision.com/2022/09/first-and-second-generation-valeo-scala-lidars-the-"
    "technology-gap-revealed/\n"
    "- Valeo SCALA Gen. 2: Yole SystemPlus teardown track (SPTA22142, Jan 2022): " + YT + "valeo-scala-gen-2-lidar/ ; "
    "TechInsights DDT-2205-811: " + TI + "products/ddt-2205-811 ; Electronics360 (28 Oct 2022): "
    + E360 + "18818/techinsights-teardown-valeo-lidar-scala-gen-2-laser-rangefinder\n"
    "- Hesai AT128: Yole SystemPlus, What's in the box? Hesai AT128 LiDAR for Li Auto L9 at a glance (19 Aug 2024): "
    "https://www.yolegroup.com/strategy-insights/whats-in-the-box-hesai-at128-lidar-for-li-auto-l9-at-a-glance/ ; "
    "teardown image from Yole SystemPlus's AT128 track (the unit, the opened housing and the transmitter board with "
    "its 128 VCSEL dies; 2,560 × 1,654 px; © Yole SystemPlus 2024): "
    "https://medias.yolegroup.com/uploads/2024/08/image-hesai-lidar-teardown-ysp_july2024-scaled.jpg ; teardown "
    "track (SPTA24290, Jan 2024): " + YT + "hesai-at128-lidar-for-liauto-l9/ ; TechInsights summary: "
    + TI + "node/52820\n"
    "- Hesai ATX: TechInsights partial teardown on Electronics360 (29 Aug 2025): "
    + E360 + "22673/techinsights-teardown-hesai-atx-lidar\n"
    "- Huawei 96-line: TechInsights DDT-2305-817 (unit L106): " + TI + "products/ddt-2305-817 ; Electronics360 "
    "(10 Nov 2023; receiver board with the Sony SPAD sensor): " + E360 + "20215/techinsights-teardown-huawei-96-line-lidar ; "
    "雪岭飞花's teardown with 55 photographs (Sohu repost): https://www.sohu.com/a/770979130_468661\n"
    "- Huawei 192-line: TechInsights summary (unit L306): " + TI + "node/57516 ; Yole SystemPlus teardown track "
    "(SPTA24344, Oct 2024): " + YT + "huawei-192-line-lidar-for-luxeed-s7--aito-m9/\n"
    "- RoboSense M1: Yole SystemPlus teardown tracks RS-LIDAR-M1 (sample version; SPTA21068, Jan 2021): "
    + YT + "robosense-rs-lidar-m1-lidar-sample-version/ and M2 for the Chery Exceed ES (SPTA24314, Mar 2024): "
    + YT + "robosense-m2-lidar--for-chery-exceed-es/ ; teardown image (the unit, its five optical modules and the MEMS "
    "mirror module; 2,048 × 1,323 px; © Yole SystemPlus 2023): " + YOLE_IMG + "3_ysp_november_2023-2048x1323.jpg ; "
    "TechInsights DDT-2104-835: " + TI + "products/ddt-2104-835\n"
    "- Livox: System Plus Consulting on the Hamamatsu laser and photodiode in the Horizon (Embedded Computing Design, "
    "2020): https://www.embedded-computing.com/hardware/yole-and-system-plus-consulting-investigate-the-lidar-"
    "industry-and-its-disruptive-technologies ; Yole SystemPlus teardown tracks Horizon (SPT20041, Jul 2020): "
    + YT + "livox-horizon-lidar/ and HAP (SPTA22189, Sep 2022): " + YT + "livox-hap-t1-lidar/\n"
    "- Velodyne Velarray H800: Yole SystemPlus, Velodyne's H800 LiDAR (3 May 2023): "
    "https://www.yolegroup.com/strategy-insights/velodynes-h800-lidar-a-noteworthy-progress-in-integration-"
    "practices-based-on-vcsel-and-laser-technologies/ ; report Velodyne Short and Long Range Lidar with VCSEL and EEL "
    "(SPR23728): https://www.yolegroup.com/product/report/velodyne-short-and-long-range-lidar-with-vcsel-and-eel/ ; "
    "teardown track (SPTA23214, Jan 2023): " + YT + "velodyne-velarray-h800-lidar/ ; teardown image (the opened "
    "H800, with small views of the LeiShen CH128X1 and Continental HFL110; 2,048 × 1,323 px; © Yole SystemPlus "
    "2023): https://medias.yolegroup.com/uploads/2023/07/img-automotive-teardown-tracks_solid-state-lidar_ysp_"
    "july2023-2048x1323.jpg ; TechInsights DDT-2210-805: " + TI + "products/ddt-2210-805 ; Electronics360 "
    "(30 Jun 2023): " + E360 + "19744/techinsights-teardown-velodyne-velarray-h800-lidar\n"
    "- Velodyne VLP-16: Electronics360 (14 Dec 2020): " + E360 + "16089/teardown-velodyne-lidar-puck-vlp-16-sensor\n"
    "- Ouster OS1-64: TechInsights DDT-2104-837: " + TI + "products/ddt-2104-837 ; Electronics360 (25 Feb 2022): "
    + E360 + "17802/techinsights-teardown-ouster-os1-64-lidar-sensor\n"
    "- Continental HFL110: TechInsights summary: " + TI + "node/54392 ; Electronics360 (15 Mar 2024): "
    + E360 + "20837/techinsights-teardown-continental-3d-flash-lidar ; Yole SystemPlus teardown track (SPTA23218, "
    "Mar 2023): " + YT + "continental-hfl110-3d-flash-lidar-for-toyota-mirai-2/\n"
    "- Seyond Robin E1X: TechInsights summary: " + TI + "blog/summary-seyond-robin-e1x-lp-lidar080-ba-lidar-deep-dive-teardown\n"
    "- Wikimedia Commons, freely licensed exterior photographs: Livox Mid-40, Horizon and Tele-15 (Dllu, CC BY-SA "
    "4.0, 4,929 × 3,696 px): " + CW + "Livox_Mid-40%2C_Livox_Horizon%2C_and_Livox_Tele-15.jpg ; a Velodyne HDL-64E "
    "on a car roof (Steve Jurvetson, CC BY 2.0, 4,587 × 3,321 px): " + CW + "Velodyne_High-Def_LIDAR.jpg ; "
    "Velodyne's product family (APJarvis, CC BY-SA 4.0, 5,184 × 3,240 px): "
    + CW + "Velodyne_ProductFamily_BlueLens_32GreenLens.png ; the Velodyne Velarray H800, Velabit and M1600 "
    "(APJarvis, CC BY-SA 4.0, 2,500 × 1,875 px): " + CW + "Velodyne_Lidar_Velarray_H800_Velabit_Velarray_M1600_"
    "Sensor_Family.jpg ; an Ibeo lidar sensor in a car (Lidar.HH, CC BY-SA 4.0, 1,280 × 960 px): "
    + CW + "Ibeo_LiDAR-Sensor_in_Car.jpg\n"
    "\n*FMCW lidars: the makers' own material.*\n"
    "- Aurora, Inside Aurora's Photonic Engine: Engineering Lidar for Automotive Scale (2026; photographs of the "
    "packaged engine): https://aurora.tech/newsroom/inside-auroras-photonic-engine-engineering-lidar-for-automotive-scale ; "
    "Aurora Voices with Sen Lin (2021; from discrete fibre components to silicon photonics): "
    "https://aurora.tech/newsroom/meet-sen-lin-auroras-silicon-photonics-director-and\n"
    "- Aeva, Form 10-K for 2025 (Item 1: transmitter, detector, DSP ASIC): "
    "https://www.sec.gov/Archives/edgar/data/1789029/000119312526116518/aeva-20251231.htm ; Aeva Day and Q2 2025 "
    "results deck (slide 63: micrographs of the laser, SOA, laser-driver and TIA ASIC and silicon-photonics die, and "
    "the CoreVision module; slide 67: manufacturing partners): "
    "https://investors.aeva.com/static-files/10710a84-7fef-4c7d-ae1e-274e4da96583 ; Aeries II release (1 Feb 2022): "
    "https://www.aeva.com/press/aeva-introduces-aeries-ii-the-worlds-first-4d-lidar-with-camera-level-resolution/\n"
    "- SiLC: Robotics 24/7 on the Eyeonic sensor (Dec 2021): "
    "https://www.robotics247.com/article/silc_releases_chip_integrated_eyeonic_lidar_sensor/manufacturing ; open-lid "
    "photograph of the fibre-less Eyeonic sensor (© SiLC): "
    "https://silc.com/wp-content/uploads/2021/12/SiLC_Fiberless_Eyeonic_in_Human_Hand.jpg\n"
    "- Baraja, Which chip are they talking about? (2023; photographs of the optical sub-assembly, open and sealed, and "
    "of the packaged SOA): https://www.baraja.com/en/blog/power-of-integration\n"
    "- Voyant, products page (Carbon): https://voyantphotonics.com/products/\n"
    "- Scantinel, Technology Overview white paper, Issue 02 (Oct 2024; pp. 6–8): "
    "https://scantinel.com/wp-content/uploads/2024/11/Scantinel_Whitepaper_202410.pdf\n"
    "- Mobileye, CES 2021 (the Intel FMCW chip; photographs credited to Intel): "
    "https://www.mobileye.com/news/ces-2021-mobileye-avs-on-move/\n"
    "- Yole Group, catalogue search for FMCW (no product): https://www.yolegroup.com/search-results/?search-term=FMCW\n"
)

EDITS = [
    (TOC_ANCHOR, TOC_ANCHOR + TOC_ADD),
    (PARTC_OLD, PARTC_NEW),
    (INTRO_OLD, INTRO_NEW),
    (C4_HEAD, C3D + "\n" + C4_HEAD),
    (C4_BULLET_OLD, C4_BULLET_NEW),
    (D1_OLD, D1_NEW),
    (APPX1_ANCHOR, APPX1_ADD + APPX1_ANCHOR),
    (APPX2_OLD, APPX2_NEW),
]
new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
