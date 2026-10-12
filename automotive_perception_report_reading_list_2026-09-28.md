# Reading list for the automotive perception report

Papers and documents that would strengthen `automotive_perception_report_2026-09-27.md`. Section 1 lists the paywalled items (with library access they can be fetched and added to `refs/`). Section 2 lists open-access items. Section 3 lists paywalled industry documents.

Bibliographic details were checked against Crossref, arXiv and the VLSI 2025 programme. Free full-text status comes from OpenAlex. ★ marks the priority items. Letters A–J give the topic:

| Letter | Topic |
|---|---|
| A | SPAD/SiPM dToF sensors |
| B | FMCW/coherent lidar |
| C | OPA and solid-state steering |
| D | Weather and eye safety |
| E | Mechanical and MEMS scanners |
| F | Interference and security |
| G | Automotive radar |
| H | iToF/AMCW |
| I | Camera vs lidar perception |
| J | Lidar systems reviews |

## 1. Paywalled papers worth obtaining

| # | Citation | DOI | Topic: why it matters | Report section |
|---|---|---|---|---|
| 1 | ★ O. Kumagai et al. (Sony), "7.3 A 189×600 back-illuminated stacked SPAD direct time-of-flight depth sensor for automotive LiDAR systems," ISSCC 2021, pp. 110–112 | 10.1109/ISSCC42613.2021.9365961 | A: baseline for Sony's automotive SPADs (IMX459) | §C5a |
| 2 | ★ T. Yui et al. (Sony), "A 25-Mpts/s back-illuminated stacked SPAD direct time-of-flight depth sensor with equivalent time sampling and pixel-level threshold control for automotive LiDAR," IEEE JSSC 61(4), 1308–1318, 2026 (conference version VLSI 2025 C27-2, 10.23919/VLSITechnologyandCir65189.2025.11075078) | 10.1109/JSSC.2026.3663598 | A: IMX479; would settle its power figure | §C5a, Appendix 1 |
| 3 | ★ S. Shimada et al. (Sony), "A back-illuminated 10 µm-pitch SPAD depth sensor with 42.5% PDE at 940 nm using an optimized doping design," VLSI 2025, T1-2 | 10.23919/VLSITechnologyandCir65189.2025.11075014 | A: 42.5% PDE at 940 nm; excess bias, DCR | §C5a |
| 4 | E. Park et al. (Yonsei, SK hynix), "Optimization of a 3.5 µm pitch 3D-stacked back-illuminated SPAD in 40 nm CIS technology: achieving 37% PDP at 940 nm," VLSI 2025, T5-4 | 10.23919/VLSITechnologyandCir65189.2025.11075016 | A: small-pitch foundry SPAD | §C5a |
| 5 | K. Yoshioka et al. (Toshiba), "A 20-ch TDC/ADC hybrid architecture LiDAR SoC for 240×96 pixel 200-m range imaging…," IEEE JSSC 53(11), 3026–3038, 2018 | 10.1109/JSSC.2018.2868315 | A: SiPM lidar SoC; SiPM vs SPAD | §C4b |
| 6 | C. Niclass et al. (Toyota CRDL), "A 0.18-µm CMOS SoC for a 100-m-range 10-frame/s 200×96-pixel time-of-flight depth sensor," IEEE JSSC 49(1), 315–330, 2014 | 10.1109/JSSC.2013.2284352 | A: coincidence detection in sunlight | §C6 |
| 7 | ★ E. Baumann et al. (NIST), "Speckle phase noise in coherent laser ranging: fundamental precision limitations," Opt. Lett. 39(16), 4776, 2014 | 10.1364/OL.39.004776 | B: the speckle limit on FMCW | §C7, §C10.3a |
| 8 | C. V. Poulton et al., "Coherent solid-state LIDAR with silicon photonic optical phased arrays," Opt. Lett. 42(20), 4091, 2017 | 10.1364/OL.42.004091 | B/C (already in `refs/`) | §C10.2b |
| 9 | B. Behroozpour, P. A. M. Sandborn, M. C. Wu, B. E. Boser, "Lidar system architectures and circuits," IEEE Commun. Mag. 55(10), 135–142, 2017 | 10.1109/MCOM.2017.1700030 | B/J: pulsed vs AMCW vs FMCW | §C0 |
| 10 | M. Prost et al. (imec), "Monolithically integrated silicon photonic biaxial FMCW LiDAR for scalable 3D sensing," OFC 2025 postdeadline Th4A.5 (DOI not retrieved) | opg.optica.org/abstract.cfm?uri=OFC-2025-Th4A.5 | B/C: OPA transmit plus coherent FPA receive on one chip | §C7b, §C10.4 |
| 11 | ★ J. Sun et al., "Large-scale nanophotonic phased array," Nature 493, 195–199, 2013 | 10.1038/nature11727 | C: 64×64 OPA demonstration | §C10 |
| 12 | C. V. Poulton et al., "Long-range LiDAR and free-space data communication with high-performance optical phased arrays," IEEE JSTQE 25(5), 2019; and "8192-element optical phased array with 100° steering range and flip-chip CMOS," CLEO 2020 JTh4A.3 | 10.1109/JSTQE.2019.2908555; 10.1364/CLEO_AT.2020.JTh4A.3 | C: Analog Photonics' state of the art | §C10.2b, §C3a |
| 13 | ★ C.-P. Hsu et al., "A review and perspective on optical phased array for automotive LiDAR," IEEE JSTQE 27(1), 2021 | 10.1109/JSTQE.2020.3022948 | C: automotive OPA review | §C10 |
| 14 | I. Kim et al., "Nanophotonics for light detection and ranging technology," Nat. Nanotechnol. 16, 508–524, 2021 | 10.1038/s41565-021-00895-3 | C/B: OPA, metasurface, FMCW review | §C10 |
| 15 | ★ M. Kutila et al., "Automotive LiDAR performance verification in fog and rain," ITSC 2018, 1695–1701 | 10.1109/ITSC.2018.8569624 | D: 905 vs 1,550 nm in a fog/rain chamber | §C0, §C4c |
| 16 | A. Frederiksen et al., "Eye safety for scanning laser projection systems," Biomed. Tech. 57(3), 2012 | 10.1515/bmt-2011-0088 | D: IEC 60825-1 for scanned beams | §C4c |
| 17 | P. J. Brosens, "Dynamic mirror distortions in optical scanning," Appl. Opt. 11(12), 2987, 1972 | 10.1364/AO.11.002987 | E: would check the Brosens constant (Appendix 1) | §C4d |
| 18 | S. T. S. Holmström, U. Baran, H. Urey, "MEMS laser scanners: a review," J. Microelectromech. Syst. 23(2), 259–275, 2014 | 10.1109/JMEMS.2013.2295470 | E: MEMS aperture–angle–frequency trade | §C4d |
| 19 | H. Shin et al., "Illusion and dazzle: adversarial optical channel exploits against lidars for automotive applications," CHES 2017, 445–467 | 10.1007/978-3-319-66787-4_22 | F: spoofing and saturation | §C9 |
| 20 | G. Kim, J. Eom, Y. Park, "An experiment of mutual interference between automotive LIDAR scanners," ITNG 2015, 680–685 | 10.1109/ITNG.2015.113 | F: early measured interference | §C9a |
| 21 | S. Alland et al., "Interference in automotive radar systems," IEEE SPM 36(5), 45–59, 2019 | 10.1109/MSP.2019.2908214 | F/G: radar interference review | §E2 |
| 22 | ★ F. Engels et al. (Continental), "Automotive radar signal processing: research directions and practical challenges," IEEE JSTSP 15(4), 865–878, 2021 | 10.1109/JSTSP.2021.3063666 | G: imaging-radar processing | §E2 |
| 23 | S. Sun, A. P. Petropulu, H. V. Poor, "MIMO radar for advanced driver-assistance systems and autonomous driving," IEEE SPM 37(4), 98–117, 2020 | 10.1109/MSP.2020.2978507 | G: virtual-array basis of 4D radar | §E2 |
| 24 | L. Fan et al., "4D mmWave radar for autonomous driving perception: a comprehensive survey," IEEE T-IV 9(4), 4606–4620, 2024 | 10.1109/TIV.2024.3380244 | G: 4D radar survey | §E2 |
| 25 | ★ I. Bilik (GM), "Comparative analysis of radar and lidar technologies for automotive applications," IEEE ITS Mag. 15(1), 244–269, 2023 | 10.1109/MITS.2022.3162886 | G/J: radar vs lidar | §E2, §E4 |
| 26 | ★ R. Lange, P. Seitz, "Solid-state time-of-flight range camera," IEEE JQE 37(3), 390–397, 2001 | 10.1109/3.910448 | H: early iToF range-camera paper | §C0 subsection 9 |
| 27 | C. S. Bamji et al. (Microsoft), "1Mpixel 65nm BSI 320MHz demodulated TOF image sensor with 3µm global shutter pixels and analog binning," ISSCC 2018, 94–96 | 10.1109/ISSCC.2018.8310200 | H: 320 MHz iToF | §C0 subsection 9, §B8 |
| 28 | ★ C. Bamji et al. (Microsoft), "A review of indirect time-of-flight technologies," IEEE TED 69(6), 2779–2793, 2022 | 10.1109/TED.2022.3145762 | H: iToF review | §C0 subsection 9 |
| 29 | P. F. McManamon, *LiDAR Technologies and Systems*, SPIE Press, 2019 | 10.1117/3.2518254 | J: link budgets and architectures | §C0 |
| 30 | R. Roriz, J. Cabral, T. Gomes, "Automotive LiDAR technology: a survey," IEEE T-ITS 23(7), 6282–6297, 2022 | 10.1109/TITS.2021.3086804 | J: commercial survey | §C1 |
| 31 | J. Hecht, "Lidar for self-driving cars," Opt. Photonics News 29(1), 26, 2018 (the web edition may be free) | 10.1364/OPN.29.1.000026 | J: industry overview | §C3c |
| 32 | Samsung, "A 1.2Mp 2.8 µm 4-tap iToF sensor with 42% QE at 940 nm," VLSI 2025, T5-5 | 10.23919/VLSITechnologyandCir65189.2025.11075065 | H: current iToF state of the art (nothing peer-reviewed found for ST's VD55H1) | §B8 |
| 33 | *Nature* News & Views on Pointcloud, "A silicon chip that enables the creation of 4D cameras," 2026 | nature.com/articles/d41586-026-00727-1 | B: independent commentary on the coherent FPA | §C7b, §C3a |

## 2. Open-access papers worth reading

These can be read directly. The priority ones are marked; several are already cited in the report.

| # | Citation | Open URL | Topic |
|---|---|---|---|
| 1 | ★ F. Villa et al., "SPADs and SiPMs arrays for long-range high-speed LiDAR," Sensors 21(11), 3839, 2021 | doi.org/10.3390/s21113839 | A |
| 2 | L. Mo et al., "A review of SPAD array chip design for direct time-of-flight LiDAR," Discover Nano 21, 2026 | doi.org/10.1186/s11671-026-04493-x | A |
| 3 | S. W. Hutchings et al., "A reconfigurable 3-D-stacked SPAD imager with in-pixel histogramming…," IEEE JSSC 54(11), 2019 | research.ed.ac.uk (green copy) | A |
| 4 | C. Zhang et al., "A 30-frames/s, 252×144 SPAD flash LiDAR with 1728 dual-clock 48.8-ps TDCs…," IEEE JSSC 54(4), 2019 | infoscience.epfl.ch/record/266775 | A |
| 5 | P. Padmanabhan et al., "A 256×128 3D-stacked (45nm) SPAD flash LiDAR with 7-level coincidence detection…," ISSCC 2021 7.4 | infoscience.epfl.ch/record/287364 | A |
| 6 | E. Charbon, "Single-photon imaging in complementary metal oxide semiconductor processes," Phil. Trans. R. Soc. A 372, 2014 | doi.org/10.1098/rsta.2013.0100 | A |
| 7 | F. Acerbi, S. Gundacker, "Understanding and simulating SiPMs," NIM A 926, 2019 | doi.org/10.1016/j.nima.2018.11.118 | A |
| 8 | K. Morimoto et al., "Megapixel time-gated SPAD image sensor for 2D and 3D imaging applications," Optica 7(4), 2020 | doi.org/10.1364/OPTICA.386574 | A |
| 9 | ★ C. Rogers et al., "A universal 3D imaging sensor on a silicon photonics platform," Nature 590, 2021 | arxiv.org/abs/2008.02411 | B |
| 10 | ★ J. Riemensberger et al., "Massively parallel coherent laser ranging using a soliton microcomb," Nature 581, 2020 | arxiv.org/abs/1912.11374 | B |
| 11 | A. Martin et al., "Photonic integrated circuit-based FMCW coherent LiDAR," JLT 36(19), 2018 | ieeexplore (free to read) | B |
| 12 | S. Bianconi et al., "Requirements for next-generation integrated photonic FMCW LiDAR sources," Nat. Commun. 16, 2025 | doi.org/10.1038/s41467-025-62027-y | B (cited in §C7a) |
| 13 | A. Lukashchuk et al., "Photonic-electronic integrated circuit-based coherent LiDAR engine," Nat. Commun. 15, 2024 | doi.org/10.1038/s41467-024-47478-z | B |
| 14 | R. Chen et al., "Breaking the temporal and frequency congestion of LiDAR by parallel chaos," Nat. Photon. 17, 2023 | doi.org/10.1038/s41566-023-01158-4 | B/F |
| 15 | Z. Wu et al., "Advancements in key parameters of FMCW LiDAR: a research review," Appl. Sci. 14(17), 2024 | doi.org/10.3390/app14177810 | B |
| 16 | ★ X. Zhang et al., "A large-scale microelectromechanical-systems-based silicon photonics LiDAR," Nature 603, 2022 | doi.org/10.1038/s41586-022-04415-8 | C |
| 17 | N. Li et al., "A progress review on solid-state LiDAR and nanophotonics-based LiDAR sensors," Laser Photonics Rev. 16, 2022 | doi.org/10.1002/lpor.202100511 | C |
| 18 | R. Juliano Martins et al., "Metasurface-enhanced light detection and ranging technology," Nat. Commun. 13, 2022 | doi.org/10.1038/s41467-022-33450-2 | C |
| 19 | M. Saha et al., "Nanophotonic waveguide chip-to-world beam scanning," Nature 651, 2026 | doi.org/10.1038/s41586-025-10038-6 | C (read in full; in `refs/`; §C7b) |
| 20 | ★ J. Wojtanowski et al., "Comparison of 905 nm and 1550 nm semiconductor laser rangefinders' performance deterioration due to adverse environmental conditions," Opto-Electron. Rev. 22(3), 2014 | doi.org/10.2478/s11772-014-0190-2 | D (cited second-hand in §C4c; now readable) |
| 21 | R. H. Rasshofer et al., "Influences of weather phenomena on automotive laser radar systems," Adv. Radio Sci. 9, 2011 | doi.org/10.5194/ars-9-49-2011 | D |
| 22 | ★ P. Duthon et al., "Light transmission in fog: the influence of wavelength on the extinction coefficient," Appl. Sci. 9(14), 2019 | doi.org/10.3390/app9142843 | D |
| 23 | M. Bijelic et al., "A benchmark for lidar sensors in fog," IEEE IV 2018 | arxiv.org/abs/1912.03251 | D |
| 24 | Y. Zhang et al., "Perception and sensing for autonomous vehicles under adverse weather conditions: a survey," ISPRS J. 196, 2023 | arxiv.org/abs/2112.08936 | D |
| 25 | ★ D. Wang, C. Watkins, H. Xie, "MEMS mirrors for LiDAR: a review," Micromachines 11(5), 2020 | doi.org/10.3390/mi11050456 | E (cited in §C4d) |
| 26 | ★ Y. Cao et al., "Adversarial sensor attack on LiDAR-based perception in autonomous driving," ACM CCS 2019 | arxiv.org/abs/1907.06826 | F |
| 27 | J. Petit et al., "Remote attacks on automated vehicles sensors," Black Hat Europe 2015 (white paper) | blackhat.com (PDF) | F |
| 28 | ★ C. Waldschmidt, J. Hasch, W. Menzel, "Automotive radar — from first efforts to future systems," IEEE J. Microwaves 1(1), 2021 | doi.org/10.1109/JMW.2020.3033616 | G |
| 29 | Z. Han et al., "4D millimeter-wave radar in autonomous driving: a survey," arXiv 2306.04242, 2023 | arxiv.org/abs/2306.04242 | G |
| 30 | A. Palffy et al., "Multi-class road user detection with 3+1D radar in the View-of-Delft dataset," IEEE RA-L 7(2), 2022 | TU Delft repository (cited in §E2) | G |
| 31 | D.-H. Paek et al., "K-Radar: 4D radar object detection…," NeurIPS 2022 Datasets and Benchmarks | arxiv.org/abs/2206.08171 | G |
| 32 | X. Zhang et al., "Dual Radar: a multi-modal dataset with dual 4D radar…," Sci. Data 12, 2025 | doi.org/10.1038/s41597-025-04698-2 | G (cited in §E2) |
| 33 | C. S. Bamji et al., "A 0.13 µm CMOS SoC for a 512×424 time-of-flight image sensor with multi-frequency photo-demodulation up to 130 MHz…," IEEE JSSC 50(1), 2015 | ieeexplore (free to read) | H |
| 34 | M. Hansard et al., *Time-of-Flight Cameras: Principles, Methods and Applications*, Springer, 2013 | inria.hal.science/hal-00725654 | H |
| 35 | R. Horaud et al., "An overview of depth cameras and range scanners based on time-of-flight technologies," MVA 27, 2016 | arxiv.org/abs/2012.06772 | H |
| 36 | ★ Y. Wang et al., "Pseudo-LiDAR from visual depth estimation," CVPR 2019 | arxiv.org/abs/1812.07179 | I |
| 37 | Z. Liu et al., "BEVFusion," ICRA 2023 | arxiv.org/abs/2205.13542 | I |
| 38 | D. Feng et al., "Deep multi-modal object detection and semantic segmentation for autonomous driving," IEEE T-ITS 22(3), 2021 | arxiv.org/abs/1902.07830 | I |
| 39 | ★ Y. Li, J. Ibanez-Guzman, "Lidar for autonomous driving: the principles, challenges, and trends…," IEEE SPM 37(4), 2020 | arxiv.org/abs/2004.08467 | J |
| 40 | ★ S. Royo, M. Ballesta-Garcia, "An overview of lidar imaging systems for autonomous vehicles," Appl. Sci. 9(19), 2019 | doi.org/10.3390/app9194093 | J |
| 41 | P. McManamon, "Review of ladar: a historic, yet emerging, sensor technology with rich phenomenology," Opt. Eng. 51(6), 2012 | doi.org/10.1117/1.OE.51.6.060901 | J |
| 42 | M. Bijelic et al., "Seeing through fog without seeing fog," CVPR 2020 | arxiv.org/abs/1902.08913 | D/I |

## 3. Paywalled industry documents that would close open items

| Document | Would settle | Report section |
|---|---|---|
| TechInsights DDT-2505-806 (Hesai ATX teardown) | ATX SiPM vendor, mirror facets | §D1, §C4d |
| TechInsights DDT-2208-806 / System Plus teardown of the Innovusion Falcon (NIO ET7) | Falcon polygon facets, rpm, galvo | §C4d |
| Yole, *LiDAR for Automotive 2024* and *Automotive LiDAR 2025* | Technology split by volume | Appendix 1 |
| Insight LiDAR / Insight Photonic Solutions Chapter 11 dockets, D. Colo. 24-13141/13142 (PACER) | Stated reason for the filing; plan recoveries | §C3a |
| Automotive News, "Ford to launch eyes-off driving system in 2028" (CES 2026) | Ford lidar plan | §B2 |
| Nikkei / Nikkan Kogyo on Pioneer's 3D-LiDAR exit (Feb 2022) | Exact dissolution date | §C3a |
| Reuters or Bloomberg on the 23 Sep 2026 extension of the US–China trade arrangement | Whether MOFCOM Announcement 72 is extended | §D2 |
| AVC (奥维云网) robot-vacuum navigation-type retail data | Share of vacuums with lidar | §B8 |
| Paid China monthly lidar-installation data by model and supplier (for example Gasgoo Auto Research) | Lidar-trim share of JV models; lidar on exported cars | §B5, §B6 |
