"""Addition of 2026-10-29 to §A7.5 (short-wave infrared): how TriEye's germanium sensor and SEDAR work.

Sources read for these edits:
- US 10,978,600 B1 (TriEye, priority 24 Oct 2019), claims 1-22 and the full description;
- US 11,606,515 B2 (TriEye, same priority family), claims 1-20 and the passages on the Q-switched laser and on the
  dark-current compensation circuits (Figs. 12A-16B);
- US 11,063,079 B2 (TriEye, priority 9 Jan 2018) and US 11,271,028 B2 (TriEye, priority 12 Feb 2018), claims and
  full descriptions;
- Tower Semiconductor's release of 31 Aug 2023 (SEC Form 6-K);
- the Yole interview with TriEye (25 Mar 2023, reprinted by the Edge AI and Vision Alliance);
- ASTM G173-03; the numbers are printed by trieye_numbers.py (same folder).
Writes edits.json (§A7.5 and the §A7 Sources line) and appendix1_pair.json (one Appendix 1 pair, applied with that
appendix's own batch). The report is only read. Usage: python add_trieye.py [--force]
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = HERE.parent.parent / "automotive_perception_report_2026-09-27.md"
T = REPORT.read_text(encoding="utf-8")
WHY = "How TriEye's sensor and SEDAR work, and the company's status (2026-10-29)."


def edit(eid, old, new):
    assert T.count(old) == 1, (eid, T.count(old), old[:70])
    return {"id": eid, "finding": "How TriEye's germanium SWIR sensor and SEDAR work", "old": old, "new": new,
            "why": WHY}


def line_starting(prefix):
    hits = [l for l in T.split("\n") if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


BULLETS = [
    r"- **How the pixels are made.** Tower Semiconductor, which develops and manufactures the sensor, describes a 1.3-megapixel array of 7 µm pixels made of back-illuminated (BSI) germanium photodiodes on silicon, with a pixel-level electrical connection made in a wafer-stacking process [P, Tower Semiconductor, 31 Aug 2023]. TriEye's patents describe two routes to such pixels.",
    r"  - *Germanium-on-insulator* (US 11,271,028 B2, priority Feb 2018). The photodiodes are formed in the single-crystal germanium layer of a germanium-on-insulator wafer, which is bonded face down to the silicon readout wafer by hybrid bonding. The handle is then removed, and the buried oxide, a quarter-wave thick at 1.5 µm, stays as an anti-reflection coating that cuts the reflection from over 30% to a few percent (claims 1 and 8; Figs. 4A–4C) [P]. The patent's case for this route is that germanium grown directly on silicon carries dislocations from the 4.2% lattice mismatch, which raise the leakage, and that germanium grown on a finished readout chip must be grown cold [P].",
    r"  - *Pyramid concentrator* (US 11,063,079 B2, priority Jan 2018). Each 10–20 µm pixel funnels the light through a silicon pyramid, which is transparent in the SWIR, onto a germanium diode only about 1 µm across on its truncated top. Dark current scales with the volume of absorbing germanium, so the small diode cuts it (claims 1–4; Fig. 1) [P].",
    r"  - Which route the TES200 uses is not public; Tower's description, back-illuminated diodes joined pixel by pixel in a wafer stack, matches the bonded route [E].",
    r"- **The dark current to beat.** 100 pA per 7 µm pixel is $10^{-10}\ {\rm A}/(7\times10^{-4}\ {\rm cm})^2=204\ \mu{\rm A\,cm^{-2}}$ [E]. TriEye's patents put the dark current of germanium photodiodes typically near 50 µA cm⁻² and claim systems for dark currents above that value [P, US 10,978,600 B1, summary; US 11,606,515 B2, claim 1].",
    r"- **First remedy: gate the exposure.** The patents open the pixels only while the echo of a laser pulse can arrive, and stop integrating while the accumulated dark-current noise is still below the readout (kTC) noise, which does not grow with time [P, US 10,978,600 B1, claim 1; US 11,606,515 B2, claims 1 and 11]. A gate of duration $\Delta t$ admits light from a slice of depth $c\Delta t/2$, 15 m for the 100 ns gate the patent calls typical, and a frame may accumulate 1 to 10,000 pulses [P, US 10,978,600 B1]. In 100 ns a TES200 pixel collects $10^{-10}\ {\rm A}\times10^{-7}\ {\rm s}/1.602\times10^{-19}\ {\rm C}=62$ dark electrons. Continuous integration over a 1/30 s frame would collect $2.1\times10^{7}$, i.e. 47 full wells, while even 1,000 gates of 100 ns collect only $6.2\times10^{4}$ [E].",
    r"- **Second remedy: subtract the dark current in the pixel.** In US 11,606,515 B2, a voltage-controlled current source in each pixel feeds in a current equal and opposite to the dark current. An amplifier sets the common control voltage from reference pixels kept dark under the same bias, averaged over several of them because nominally identical germanium diodes can differ in dark current by a factor of 1.5–4 (Figs. 12A–16B) [P]. The subtraction keeps a small pixel capacitance from filling, but it cannot remove the shot noise of the dark current, so gating is still needed [E].",
    r"- **The light: a solar absorption band, and no amplifier.**",
    r"  - The patents choose the wavelength to match a solar absorption band, between 1.3 and 1.4 µm. They use passively Q-switched ceramic Nd:YAG lasers, with V³⁺:YAG or cobalt-doped saturable absorbers, at 1.32, 1.34 or 1.44 µm, delivering in their examples 10–100 mJ pulses at 10–50 Hz. The reason given is that the peak power eye safety allows for ≈100 ns pulses, ≈300 kW, is beyond laser diodes [P, US 11,606,515 B2; US 10,978,600 B1].",
    r"  - The products use laser diodes instead. Coherent supplied the 1,375 nm edge-emitting laser above (Jun 2023), and TriEye's interview with Yole calls the region around 1,380 nm solar-blind [T, Yole, 25 Mar 2023]. VCSEL partners followed: Vertilas at 1.3 µm (Apr 2024), then HLJ (Oct 2024) and LITEON (Aug 2025) at 1,135 nm [P, TriEye news page; T, Semiconductor Today, 22 Aug 2025].",
    r"  - In ASTM G173 the sunlight at ground level averaged over 1,365–1,385 nm is $1.1\times10^{-4}\ {\rm W\,m^{-2}\,nm^{-1}}$, about 2,500 times less than the $0.27\ {\rm W\,m^{-2}\,nm^{-1}}$ at 1,550 nm, and every tabulated value from 1,360 to 1,390 nm stays below about $10^{-3}\ {\rm W\,m^{-2}\,nm^{-1}}$, so a diode whose wavelength drifts with temperature keeps the benefit [E]. The Nd:YAG lines at 1.32, 1.34 and 1.44 µm get 1.05, 0.50 and 0.16 times the 1,550 nm value. Near 1,135 nm the water absorption comes in narrow lines: the value tabulated at exactly 1,135 nm is $0.015\ {\rm W\,m^{-2}\,nm^{-1}}$, but the average is 0.10 over ±2 nm and 0.17 over ±10 nm, 0.63 times the 1,550 nm value [E].",
    r"  - The bet has costs. 1,375 nm lies outside the erbium gain band near 1,530–1,565 nm, so the erbium-fibre amplifiers of 1,550 nm lidars (§C4) cannot be used, and the pulse energy must come from the laser diodes themselves [E]. The water vapour that removes the sunlight also absorbs the laser's own light along its path, by an amount not found (Appendix 1).",
    r"- **Depth from gated slices (SEDAR).** The patents combine several gated time slices, each covering a range of distances, into one image with depth, citing Gated2Depth (Gruber et al. 2019) [P, US 10,978,600 B1]. Their claims cover slices wider than 2 m, for example from 20, 40 and 60 m, and detection of a 1 m × 1 m target of 20% reflectivity beyond 50 m with an uncooled germanium receiver, and of vehicles and pedestrians at 50–150 m with the receiver above 30 °C [P, US 11,606,515 B2, claims 4 and 13–16]. TriEye describes SEDAR as a high-definition gated imager combined with a flash-lidar concept that gives depth at every pixel, with at least 5 million points per second and object detection beyond 200 m [T, Yole interview, 25 Mar 2023].",
]

dark = line_starting("- **Its dark current rules out passive night imaging.**")
edits = [edit("T1-A7.5-trieye", dark, dark + "\n" + "\n".join(BULLETS))]

# §A7.5 "Industry ties": TriEye's status
ties = line_starting("- **Industry ties.** TriEye's automotive links are")
STATUS = (
    r" TriEye is still active, though its press releases end in Oct 2024. Its news page lists the LITEON demonstrator, "
    r"in which the TES200 was available in sample quantities only [T, Semiconductor Today, 22 Aug 2025], and AM "
    r"General's MIMIC-V special-operations vehicle, shown at the US Army's AUSA exhibition on 13–15 Oct 2025 fitted with "
    r"TriEye's SWIR cameras for imaging and 3D depth [P, AM General, 10 Oct 2025]. The last funding disclosed is a \$74 M "
    r"round in Nov 2021, which brought the total to \$96 M and with which TriEye expected sales in 2022 [T, Calcalist, "
    r"10 Nov 2021]; no announcement from 2026 was found.")
edits.append(edit("T1b-A7.5-trieye-status", ties, ties + STATUS))

SOURCES = (
    " ; https://patents.google.com/patent/US10978600B1/en (TriEye, active SWIR imaging with germanium receivers, "
    "priority 24 Oct 2019)"
    " ; https://patents.google.com/patent/US11606515B2/en (TriEye, germanium receivers, Q-switched laser and in-pixel "
    "dark-current compensation)"
    " ; https://patents.google.com/patent/US11063079B2/en (TriEye, germanium-on-silicon pyramid focal-plane array, "
    "priority 9 Jan 2018)"
    " ; https://patents.google.com/patent/US11271028B2/en (TriEye, germanium-on-insulator focal-plane array, priority "
    "12 Feb 2018)"
    " ; https://www.sec.gov/Archives/edgar/data/928876/000117891323003038/zk2330246.htm (Tower Semiconductor and "
    "TriEye, 31 Aug 2023)"
    " ; https://www.edge-ai-vision.com/2023/03/a-swir-imaging-platform-for-automotive-and-beyond/ (Yole interview with "
    "TriEye, 25 Mar 2023)"
    " ; https://www.nlr.gov/grid/solar-resource/spectra-am1.5 (ASTM G173-03 reference spectra)"
    " ; https://semiconductor-today.com/news_items/2025/aug/trirye-liteon-220825.shtml (TriEye and LITEON, 1,135 nm "
    "VCSEL demonstrator, 22 Aug 2025)"
    " ; https://www.amgeneral.com/wp-content/uploads/2025/10/AM-General-Press-Release_AUSA-2025_Final.pdf (AM General "
    "at AUSA 2025, MIMIC-V with TriEye SWIR, 10 Oct 2025)"
    " ; https://www.calcalistech.com/ctech/articles/0,7340,L-3922225,00.html (TriEye's \\$74 M round, Calcalist, "
    "10 Nov 2021)")
anchor = "https://trieye.tech/news/ (TriEye partners)"
edits.append(edit("T2-A7-sources", anchor, anchor + SOURCES))

# Appendix 1 is edited in its own batch: one pair for it
gated = line_starting("- **Gated and SWIR imaging.**")
appendix1 = [edit(
    "T3-A1-trieye", gated,
    gated + "\n"
    "- **TriEye's sensor and illuminator (§A7.5).** Unknown: which patented pixel route the TES200 uses (Tower's "
    "description, back-illuminated diodes joined pixel by pixel in a wafer stack, fits the bonded "
    "germanium-on-insulator route); its read noise, which sets how many gates a frame can accumulate before the "
    "dark-current noise exceeds it; the pulse energy, duration and repetition rate of its UltraBlaze illuminator; how "
    "much water vapour absorbs 1,375 nm light over a 100–200 m path; SEDAR's depth accuracy; and any funding after the "
    "Nov 2021 round or any series programme, automotive or military.")]

for name, lst in (("edits.json", edits), ("appendix1_pair.json", appendix1)):
    out = HERE / name
    assert not out.exists() or "--force" in sys.argv, f"{name} exists; pass --force"
    data = json.dumps({"block": "trieye_2026-10", "edits": lst, "skipped": []}, ensure_ascii=False, indent=1)
    out.write_bytes((data + "\n").encode("utf-8"))
    print(name, len(lst), "edits")
