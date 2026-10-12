"""Third (final) edit list of the October 2026 gap-filling round: §D8 EU numbers after the EU agent's
corrected search rule (time-of-flight and depth terms now count only with an active-ranging word),
the EU defence paragraph (EDF, POINTER, EIC, Chips JU, ESA, Photonics21), and the §D8 items of
Appendix 1. Applied by apply_gapfill.py with --edits edits_gapfill3, written against the report
as of 3 Oct 2026 12:12 (sha256 2ae128bb20ff...).
"""
E = []

# ---------------------------------------------------------------- method bullets
E.append(("S", "- *Search.* Titles, objectives and keywords were searched for lidar,",
          "time-of-flight (ToF) depth cameras and 3D sensing;",
          "time-of-flight (ToF) depth cameras and 3D or depth sensing, counted only when the text also names ToF, lidar, single-photon detection, ranging or a rangefinder, so that stereo and structured-light cameras are not counted as lidar;"))
E.append(("S", "- *Relevance.* Each project scores",
          "The 145 projects with $s=1$",
          "The 138 projects with $s=1$"))
E.append(("S", "- *Check.* Of the 199 projects that CORDIS's own full-text search returns",
          "ToF depth-sensing projects that never name lidar are also undercounted.",
          "Depth-sensing projects that name neither lidar nor any ranging term are not counted."))

# ---------------------------------------------------------------- table rows (by start year and by period)
ROWS = [
    ("| 2010 | 3,602 | 3 (0.75) | 0.83 | 1 (0.50) | 0 | 0 |", "| 2010 | 3,602 | 4 (4.32) | 1.11 | 2 (4.07) | 0 | 0 |"),
    ("| 2012 | 4,332 | 5 (9.13) | 1.15 | 4 (8.92) | 0 | 0 |", "| 2012 | 4,332 | 4 (7.79) | 0.92 | 3 (7.58) | 0 | 0 |"),
    ("| 2017 | 4,975 | 4 (6.23) | 0.80 | 2 (0.37) | 0 | 0 |", "| 2017 | 4,975 | 3 (2.24) | 0.60 | 2 (0.37) | 0 | 0 |"),
    ("| 2018 | 5,067 | 10 (24.22) | 1.97 | 6 (20.78) | 0 | 0 |", "| 2018 | 5,067 | 9 (23.17) | 1.78 | 6 (20.78) | 0 | 0 |"),
    ("| 2020 | 4,507 | 17 (68.08) | 3.77 | 9 (31.32) | 1 (1.71) | 2 (6.26) |", "| 2020 | 4,507 | 15 (64.05) | 3.33 | 7 (27.29) | 1 (1.71) | 2 (6.26) |"),
    ("| 2023 | 5,144 | 14 (53.07) | 2.72 | 9 (36.47) | 3 (9.76) | 6 (24.89) |", "| 2023 | 5,144 | 13 (50.57) | 2.53 | 9 (36.47) | 3 (9.76) | 6 (24.89) |"),
    ("| 2007–2013 (FP7) | 22,380 | 18 (21.5) | 0.80 | 0.05% | 10 (14.0) | 0 | 0 |", "| 2007–2013 (FP7) | 22,380 | 18 (23.7) | 0.80 | 0.06% | 10 (16.3) | 0 | 0 |"),
    ("| 2014–2020 (H2020) | 33,428 | 64 (196.6) | 1.91 | 0.31% | 34 (93.2) | 2 (1.9) | 4 (28.4) |", "| 2014–2020 (H2020) | 33,428 | 60 (187.5) | 1.79 | 0.30% | 32 (89.2) | 2 (1.9) | 4 (28.4) |"),
    ("| 2021–2026 (Horizon Europe) | 27,929 | 60 (164.6) | 2.15 | 0.23% | 34 (79.1) | 10 (24.2) | 16 (71.2) |", "| 2021–2026 (Horizon Europe) | 27,929 | 59 (162.1) | 2.11 | 0.23% | 34 (79.1) | 10 (24.2) | 16 (71.2) |"),
    ("| Rate ratio, 2021–2026 to 2014–2020 | | ×1.12 ($P=0.29$) | | | ×1.20 ($P=0.27$) | ×6.0 ($P=0.009$) | ×4.8 ($P=0.002$) |", "| Rate ratio, 2021–2026 to 2014–2020 | | ×1.18 ($P=0.21$) | | | ×1.27 ($P=0.20$) | ×6.0 ($P=0.009$) | ×4.8 ($P=0.002$) |"),
]
for old, new in ROWS:
    E.append(("X", old, new))

# ---------------------------------------------------------------- derivations and prose
E.append(("S", "*How the numbers are derived* [E]: for 2023, $N_{\\rm L}=14$",
          r"for 2023, $N_{\rm L}=14$ of $N_{\rm A}=5{,}144$ projects, so $r=1000\times14/5{,}144=2.72$ per thousand. The 14 projects hold €53.07 M of the €14,991 M granted to all projects starting in 2023, a share of $53.07/14{,}991=0.35\%$.",
          r"for 2023, $N_{\rm L}=13$ of $N_{\rm A}=5{,}144$ projects, so $r=1000\times13/5{,}144=2.53$ per thousand. The 13 projects hold €50.57 M of the €14,991 M granted to all projects starting in 2023, a share of $50.57/14{,}991=0.34\%$."))
E.append(("S", "*How the numbers are derived* [E]: the rate ratio for coherent lidar",
          r"but $P\approx0.29$ for all lidar-relevant projects (60 of 124) and $P\approx0.27$ for hardware (34 of 68), differences that chance explains easily. The money shares divide lidar-relevant EU money by all EU project money in the window: $164.6/71{,}692=0.23\%$ for 2021–2026, against $196.6/63{,}320=0.31\%$ for 2014–2020.",
          r"but $P\approx0.21$ for all lidar-relevant projects (59 of 119) and $P\approx0.20$ for hardware (34 of 66), differences that chance explains easily. The money shares divide lidar-relevant EU money by all EU project money in the window: $162.1/71{,}692=0.23\%$ for 2021–2026, against $187.5/63{,}320=0.30\%$ for 2014–2020."))
E.append(("S", "**Where the EU projects come from** [E].",
          "(€85.8 M of €164.6 M), the electronics JUs a fifth (€35.0 M, almost all of it STARLight), the EIC 14% (€22.5 M),",
          "(€85.8 M of €162.1 M), the electronics JUs a fifth (€35.0 M, almost all of it STARLight), the EIC 12% (€20.0 M),"))

# ---------------------------------------------------------------- EU defence paragraph
DEFENCE = r"""**EU defence funding: where lidar is named as a sovereign capability** [P unless tagged]. The European Defence Fund (EDF), the EU's defence research and development fund, is not recorded in CORDIS, so its topic texts for 2021, 2023 and 2024, its 2024 award decision and its 2026–2027 multiannual perspective were read separately.
- **POINTER is its first lidar-centred grant.** It came from the 2024 call for consortia of small firms and research organisations (EDF-2024-LS-RA-SMERO-NT), with a maximum grant of €3.99 M, and runs from Feb 2026 to Jul 2029 under the European Defence Agency. Optagon Photonics (Greece) coordinates, with Fraunhofer, PHIX, EVOELECTRONICS and CogniSensus. It builds an FMCW lidar on photonic integrated circuits, with optical phased arrays among its keywords, for surveillance and counter-drone use. It switches in under 1 ms between detection at up to 1,000 m over 30° × 25° and tracking at 1,000 frames/s with 3 cm range and 0.1° angular resolution. Its stated aim is "the first supply chain for defense-grade coherent LIDAR products in Europe". The grant is about 0.4% of the ≈€1.1 B EDF 2024 call ($3.99/1{,}100\approx0.004$) [P; S for the call budget; E].
- **Elsewhere lidar is one named option among many sensors.** EDF topics name quantum lidar (2021), non-line-of-sight imaging built on photon counting and round-trip timing (2021), active lidar against explosive ordnance (2023), and, in 2024, a small uncrewed aircraft that should carry radar and lidar, drone-navigation payloads and structural modelling from lidar data. The 2024 topics funded ten projects worth €82.6 M in which lidar is one option, among them PRECISE, where XenomatiX is a partner (§C3a) [P; E for the sum].
- **Plans.** The EDF's 2026–2027 multiannual perspective cites POINTER as its lidar line and lists radar, lidar and electronic-warfare demonstrators among its expected sensor outcomes [P]. Counter-drone money is far larger: the EDF 2025 call awarded €1.07 B to 57 projects with a counter-drone emphasis [T], and the European Defence Industry Programme (EDIP, 2026–2027) funds counter-drone procurement [S]. In these, lidar competes with radar, infrared and radio-frequency sensing rather than being named. The EIC's 2026 programme adds STEP Scale Up Defence, €200 M of equity in tickets of €10–30 M for defence domains including counter-drone and optronic systems [P].
- **Other EU signals.** No Chips JU topic of 2024–2026 names lidar; the nearest is a 2026 photonics innovation action (€20 M) for wafer-scale SiN, InP and GaAs processes, packaging and demonstrators in sectors including mobility and defence [P]. Among the EIC challenges of 2021–2026, lidar appears only as an application in the 2023 chip-scale frequency-comb challenge and the 2024 "smart edge" challenge, neither of which funded a lidar project [P]. ESA continues its science and weather lidars: EarthCARE's 355 nm lidar has been in orbit since May 2024, the methane lidar MERLIN is due in 2029, and Aeolus-2 was authorised on 29 Jun 2026 for a 2034 launch [P/S]. The photonics industry's 2025 position paper for the next framework programme asks for a ring-fenced €2 B photonics programme, and places multi-channel lidars with software-defined waveforms, optical phased arrays, tunable lasers and coherent receivers under a defence challenge "for sovereignty" [P, Photonics21].
"""
E.append(("I", "**US: how the count was made** [E unless tagged]", DEFENCE))

# ---------------------------------------------------------------- reading bullets
E.append(("S", "- **No renewal in volume on either side of the Atlantic.**",
          "with a falling share of EU money (0.31% to 0.23%).",
          "with a falling share of EU money (0.30% to 0.23%)."))
E.append(("L", "- **Sovereignty is a label, not a lidar budget.**",
          "- **Sovereignty is a label, not a lidar budget.** EU civil research texts invoke strategic autonomy without targeting lidar; the sovereignty-labelled EU lidar money is €5.8 M for two space laser sources and €4.0 M for one defence project, POINTER. The US measures of 2024–2026 (§D3) extend DoD's ban on Chinese lidar to contractors at every tier and ask DoD for an industrial-base assessment, but fund no US lidar base. The large photonics programmes on both sides, PIXEurope and AIM Photonics (the US integrated-photonics manufacturing institute, §C3a), are generic infrastructure.\n"
          "- **A defence reframing, with little money.** In 2024–2026 the framing in Europe moves towards defence: the EDF funds its first lidar-centred grant, its 2026–2027 plan names lidar among its sensor demonstrators, and the photonics industry files coherent, photonic-integrated lidar under defence sovereignty. The money aimed at lidar itself remains a few million euros a year."))
E.append(("L", "- **What could change this reading.**",
          "- **What could change this reading.** Defence money that this count reaches only in part: the EDF's 2025–2026 work programmes and most of its project factsheets were not read, and the research lines in the US Army, Navy and Air Force budget books could not be downloaded; classified programmes, national programmes and IPCEIs (Important Projects of Common European Interest) are outside the count. Counter-drone and military sensing are the most plausible sources of a larger Western uptick (Appendix 1)."))
E.append(("S", "Sources: https://cordis.europa.eu/data/cordis-HORIZONprojects-json.zip",
          "; https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv",
          "; https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv ; https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/projects-details/44181033/101224064/EDF ; https://defence-industry-space.ec.europa.eu/system/files/2025-10/EDF-2024%20Adopted%20Award%20Decision%20-%20C(2025)%206378%20EN.pdf ; https://defence-industry-space.ec.europa.eu/document/download/7a84b97c-5258-40a7-ac8e-460bcd87bbb7_en?filename=EDF+Indicative+Multiannual+Perspective+2026-2027.pdf ; https://eic.ec.europa.eu/document/download/52598755-1351-4b54-b46b-e2682d0a3aec_en?filename=EIC-Work-Programme-2026.pdf ; https://ec.europa.eu/info/funding-tenders/opportunities/data/topicDetails/horizon-ju-chips-2026-ft2-ia.json ; https://www.esa.int/Applications/Observing_the_Earth/Meteorological_missions/Authorisation_paves_the_way_for_Aeolus-2_wind_mission ; https://www.photonics21.org/download/ppp-services/photonics-downloads/Photonics21_Position_Paper_Investing_in_Light_The_Vision_to_Secure_Europes_Competitiveness_in_the_Global_Tech_Race_0.pdf"))

# ---------------------------------------------------------------- Appendix 1, §D8 items
E.append(("L", "- **Channels not counted.** EU: the European Defence Fund, ESA,",
          "- **Channels not counted.** EU: the EDF's 2025–2026 work programmes, most of its project factsheets and the amounts of its 2021 and 2023 lidar-related projects were not read; national programmes and IPCEIs are outside the count; and EU policy documents (Recommendation 2023/2113 on critical technologies, the Automotive Action Plan COM(2025) 95, the Cybersecurity Act revision) were not checked for lidar. US: the research lines in the Army, Navy and Air Force budget books (their sites blocked downloading), DIU, classified work and subawards are not counted, and NASA's TechPort gives project counts but no amounts. Defence and counter-drone sensing are the most plausible sources of a larger Western uptick, so the \"flat\" reading of §D8 holds for civil research grants, SBIR and the traced federal and EDF channels."))
E.append(("S", "- **Search coverage.** The EU count undercounts ToF depth-sensing projects that never name lidar",
          "The EU count undercounts ToF depth-sensing projects that never name lidar and atmospheric projects that name it only in attached reports;",
          "The EU count leaves out depth-sensing projects that name neither lidar nor any ranging term, and undercounts atmospheric projects that name lidar only in attached reports;"))
