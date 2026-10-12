"""Edit list for the October 2026 gap-filling round (applied by apply_gapfill.py).

Each entry is one of
  ("L", prefix, new)            replace the unique line starting with prefix
  ("S", prefix, old, new)       replace old (once) inside the unique line starting with prefix
  ("A", prefix, text)           insert text after the unique line starting with prefix
  ("I", prefix, text)           insert text before the unique line starting with prefix
  ("B", start, end, text)       replace lines [start, end) (end line kept)
Written against the report as of 3 Oct 2026 (sha256 c39153b37984...).
Findings come from the research round of 3 Oct 2026 (folders gaps_* and renew_* in this archive).
"""

E = []

# ---------------------------------------------------------------- front matter
E.append(("S", "- **Supply chain and geopolitics:**",
          "Chinese FMCW development (§D7).",
          "Chinese FMCW development (§D7); EU and US public research funding for lidar (§D8)."))
E.append(("S", "   - **My bottom-up estimate** (built up program by program",
          r"about 45–140k passenger-car lidars were fitted to cars sold outside China in 2025. That is about 0.1–0.2% of non-China production ($4.5\times10^{4}/6\times10^{7}\approx0.08\%$ and $1.4\times10^{5}/6\times10^{7}\approx0.23\%$ of an assumed 60 M non-China light vehicles, rounded)",
          r"about 50–155k passenger-car lidars were fitted to cars sold outside China in 2025. That is about 0.1–0.3% of non-China production ($5.0\times10^{4}/6\times10^{7}\approx0.08\%$ and $1.55\times10^{5}/6\times10^{7}\approx0.26\%$ of an assumed 60 M non-China light vehicles, rounded)"))
E.append(("S", "   - **The hype–bust cycle (§C3a).**",
          "Their SPAC-era valuations (Quanergy",
          r"Their SPAC-era valuations, the implied equity values at the \$10 deal price (Quanergy"))
E.append(("S", "     - Sony's research pixels reached 51% at 905 nm (2025)",
          "Sony's research pixels reached 51% at 905 nm (2025)",
          "Sony's research pixels reached 42.5% at 940 nm (2025)"))

# ---------------------------------------------------------------- §B2 programmes
E.append(("S", "| **Rivian R2 Gen 3** | 1 forward lidar",
          "RoboSense reported, **Rivian denies it** [T]",
          "RoboSense reported; Rivian's denial addressed a different RoboSense customer (note 6) [T/E]"))
E.append(("S", "| **Aeva: top-10 European OEM, L3** |",
          "SOP 2028; OEM unnamed [P]",
          "SOP 2028, running into the mid-2030s; OEM unnamed. Aeva's FY2025 10-K calls it a selection, with no definitive volume production agreement signed [P]"))
E.append(("S", "6. **Rivian.** EV (eletric-vehicles.com)",
          "reported RoboSense as the lidar supplier, which Rivian denies.",
          "reported RoboSense as the lidar supplier, which Rivian denies. The denial answered RoboSense's description of \"a leading global manufacturer of SUVs and trucks\", which RoboSense's 9M 2025 results place among its wins in the Chinese domestic market (most likely Great Wall Motor), so it does not exclude RoboSense [P/E]. RoboSense separately reports unnamed North American wins: an electric-pickup start-up brand, for its EM4 of more than 500 beams, and a repeat exclusive win of more than 500,000 lidars at an EV maker that began deliveries in 2021. The first fits Rivian and the second Lucid most closely [P/E]."))

# ---------------------------------------------------------------- §B4a vans and robots
E.append(("S", "- **National standard:** GB 44721-2026",
          "No source found says whether low-speed delivery vans fall under the standard [U].",
          "It applies to vehicles fitted with L3 or L4 systems, and not to automated parking [P, SAMR record; T, CNR citing MIIT]. The vans reach roads through municipal pilot rules, so the standard would bind them only if they entered national type approval as N-category vehicles [E]; no published text addresses low-speed vans [U]."))
E.append(("A", "| Zelos Z5 (Jun 2024) |",
          "| Zelos Z5-2026 | 2 semi-solid-state lidars (supplier not named) | 2 radars, 12 ultrasonic sensors, 8 cameras | China.com, Jul 2025 [T] |\n"
          "| Zelos E6 | 2 Seyond Lingque W, front and rear | — | Seyond, 5 Jun 2025 [P] |\n"
          "| Zelos Z20 light truck (with Yutong) | 4 lidars (models not stated) | — | QbitAI, Aug 2026 [T] |"))
E.append(("S", "- **Reconciling them.** Both can be true",
          "Neither company publishes delivery-van units.",
          "Neither company publishes delivery-van units. Hesai's 200,000-unit Zelos award is a nomination for 2026 and later models, not shipments [T]; RoboSense guides 100,000–150,000 delivery-vehicle lidars for 2026 [T, results call]; and trade press puts van lidar prices at RMB 1,000–1,500, down more than 60% from early 2024 [T, OFweek]."))
E.append(("L", "- **Lidars per van:** 1 (Cainiao GT Pro, Neolix X3) to 4",
          "- **Lidars per van:** 1 (Cainiao GT Pro, Neolix X3) to 4 (Zelos Z5 of 2024, Zelos Z20). The market leader is cutting content: two lidars on the Z5-2026 and on the E6 [T/P], and Zelos describes its map-free L4 system as vision-led, with lidar as an aid [T]. The suppliers give two to four (RoboSense) and two to six (Hesai) lidars per van [T, results calls]."))
E.append(("S", "- **Installed base:** $47{,}000 \\times (1\\text{–}4)",
          "**50–190k lidars** in Q1 2026,",
          r"**50–190k lidars** in Q1 2026 (≈70–150k when split by operator: $25{,}000\times(2\text{–}4)+17{,}000\times(1\text{–}2)+5{,}000\times(1\text{–}4)=72\text{–}154$k for ≈25,000 Zelos, ≈17,000 Neolix and ≈5,000 other vans),"))
E.append(("L", "| | Serve Robotics (US; Uber Eats) |",
          r"| | Serve Robotics (US; Uber Eats) | More than 2,000 robots at end-2025, in 20 cities across six metro areas; 2026 revenue guidance cut to \$9–10 M (6 Aug 2026) [P] | **Yes: Ouster**, one per robot: an OS1 on the second generation and a single REV7 on the third, under a multi-year supply agreement [P] |"))
E.append(("S", "| | Cartken; Coco (formerly Kiwibot) |",
          "| **No.** Cartken is camera-first, \"without costly LiDAR\" [P] |",
          "| **Cartken: no**, camera-first, \"without costly LiDAR\" [P]. **Coco: some.** RoboSense's FY2025 results list Coco Robotics among its delivery customers for digital lidar [P] |"))

# ---------------------------------------------------------------- §B5 exports
E.append(("L", "| Chinese-brand exports with lidar (2025) |",
          "| Chinese-brand exports with lidar (2025) | **about 20–75k, central about 40k** (about 20–95k lidar units) [E, low confidence] | Li Auto's grey exports and, from Q4 2025, official exports to Russia, Central Asia and the Middle East are about half; official lidar exports of other brands are small (note 2) |"))
E.append(("L", "| **Total passenger-car lidar outside China (2025)** |",
          "| **Total passenger-car lidar outside China (2025)** | **about 50–155k** [E] | About **0.08–0.26%** of an assumed 60 M non-China light vehicles (note 3) |"))
E.append(("L", "2. **Chinese-brand exports.** NIO's overseas sales",
          r"2. **Chinese-brand exports.** The estimate works channel by channel: cars sold outside China, times the share fitted with lidar, times lidars per fitted car [E]. Measured inputs are Russian 2025 registrations of Li Auto 13,088, Zeekr 3,811, Lynk & Co 2,395, Aito 2,380, Avatr 1,261, Denza 733, Xiaomi 705 and NIO 66 [MR, Autostat data via a republisher]; NIO's 1,129 registrations in five European markets [T], every one with lidar [P]; Lotus's 1,592 Eletre and Emeya deliveries outside China (4,552 less 2,960 in China), on which lidar is an option [P/T]; and Dutch registrations (Zeekr 7X 892, 001 415, X 346; Li Auto 0) [I, RDW open data]. Li Auto, whose L series has carried lidar on every trim since its May 2025 refresh [T], is about half of the central value. Most of its volume is **\"parallel exports\"**, zero-mileage cars shipped by independent traders rather than the carmaker to Russia, Central Asia and the Middle East; Li Auto has sold officially in several of these markets since Q4 2025 [S]. Zeekr's lidar trims are a fraction of its ≈20k overseas sales (its EU 7X page mentions no lidar [P]), Xpeng exports are mostly vision-only (cameras, no lidar), and BYD's God's Eye trims are rare abroad [E]. Fitment shares other than those of NIO, Li Auto and the Lynk & Co 900 are judgements. From 1 Jan 2026, exporting a car registered for 180 days or less needs the carmaker's after-sales confirmation [P, MOFCOM], which curbs the trader channel, so 2026 is probably lower, at very roughly 15–50k [E, very low confidence]."))
E.append(("S", "- **Rows 1 and 2** are judgements over the programmes",
          "- **Rows 1 and 2** are judgements over the programmes and channels listed in their basis columns and in notes 1–2, not sums of disclosed counts; the only firm input is Volvo's 16,311 EX90s built in 2025.",
          r"- **Row 1** is a judgement over the programmes listed in note 1, not a sum of disclosed counts; its only firm input is Volvo's 16,311 EX90s built in 2025. **Row 2** sums twelve export channels. Channel $i$ contributes $V_is_i$ lidar cars and $V_is_iu_i$ lidar units, where $V_i$ is the number of cars it sold outside China, $s_i$ the share fitted with lidar and $u_i$ the lidars per fitted car. The low, central and high totals add all the low, central and high inputs: 19.6k, 37.7k and 75.0k lidar cars, carrying 19.9k, 41.7k and 96.3k lidars. Li Auto's central term is $23{,}088\times0.85\times1\approx19.6$k. A Monte Carlo draw with independent inputs gives a far narrower band (36.8–46.2k cars between the 10th and 90th percentiles), but the channel errors are correlated, so the sums are quoted."))
E.append(("S", "- **Total and share.** The total adds rows 1 and 2:",
          r"The total adds rows 1 and 2: $30+15=45\text{k}$ and $80+60=140\text{k}$. As a share of an assumed 60 M light vehicles sold outside China, that is $4.5\times10^{4}/(6\times10^{7})\approx0.08\%$ to $1.4\times10^{5}/(6\times10^{7})\approx0.23\%$.",
          r"The total adds rows 1 and 2: $30+20=50\text{k}$ and $80+75=155\text{k}$. As a share of an assumed 60 M light vehicles sold outside China, that is $5.0\times10^{4}/(6\times10^{7})\approx0.08\%$ to $1.55\times10^{5}/(6\times10^{7})\approx0.26\%$."))
E.append(("S", "3. **Total.** The share is rounded elsewhere",
          "The share is rounded elsewhere in the report to 0.1–0.2%.",
          "The share is rounded elsewhere in the report to 0.1–0.3%."))

# ---------------------------------------------------------------- §B6 JV suppliers
E.append(("S", "| **Toyota** (GAC-Toyota) | bZ7 |",
          "Roof lidar in launch coverage [T]; supplier not named; Hesai likely but unconfirmed [U] (note 2)",
          "Roof lidar in launch coverage [T]; **Hesai** design win, lidar model not named [P] (note 2)"))
E.append(("S", "| **Toyota** (FAW-Toyota) | Unnamed new NEVs |",
          "order of >1 M units (Dec 2025) plus another 500k (Jun 2026) [T, citing RoboSense]",
          "orders of nearly 1 M units (Dec 2025) and more than 500k (Jun 2026) [P, RoboSense titles; T]"))
E.append(("S", "| **VW** (SAIC-VW) | ID. ERA 9X",
          "supplier not named [T]; RoboSense likely [U] (note 4)",
          "**RoboSense** [T, relaying RoboSense]; EMX likely [E] (note 4)"))
E.append(("L", "2. **bZ7.** Hesai announced an ATX win",
          "2. **bZ7.** Hesai's Q2 2026 results name it: following the bZ3X, Hesai \"secured another design win for the bZ7 model\" at GAC Toyota [P]. The lidar model is not named; the ATX is likely, given Hesai's Aug 2025 ATX win for a new-energy model of \"a joint venture of Toyota based in China\" [E]. The win was announced after the bZ7's 29 Mar 2026 launch, so whether every car built since launch carries Hesai is unconfirmed."))
E.append(("L", "4. **ID. ERA 9X.** RoboSense's 192-beam EMX",
          "4. **ID. ERA 9X.** RoboSense is the supplier: a financial wire relaying RoboSense calls the ID. ERA 9X the first production model under the SAIC-VW–RoboSense partnership of Apr 2025, with RoboSense lidar standard on every trim [T]. RoboSense's 192-beam EMX had been chosen by \"a China-based joint venture vehicle brand of the largest Europe OEM\" (Apr 2025) [P], so the EMX is the likely unit [E]. FAW-VW's ID. AURA T6 (Sep 2026) carries RoboSense's 192-line lidar on both lidar trims [T]. RoboSense reports orders of more than 500,000 lidars from several China JV brands of the largest European car group, with models from 2026 [P, 9M 2025 results]."))
E.append(("L", "5. **Unnamed European OEM.** The order came from",
          "5. **Unnamed European OEM.** The order came from \"another top-tier European automaker\" (20 May 2026). Hesai's Q2 2026 results report \"a major global design win with Volkswagen, covering multiple vehicle models under its China joint ventures\" [P], so the OEM is almost certainly VW Group [E]; the results do not restate the order's size or the ATX. VW's 192-line units are RoboSense's (note 4), so VW's China JVs buy from both Chinese leaders, and which models take Hesai units is undisclosed."))
E.append(("S", "- **Orders without named models:**",
          "FAW-Toyota (RoboSense, ≈1.5 M units: >1 M in Dec 2025 plus 500k in Jun 2026)",
          "FAW-Toyota (RoboSense, ≈1.5 M units: nearly 1 M in Dec 2025 plus more than 500k in Jun 2026)"))
E.append(("S", "- **Orders without named models:**",
          "an unnamed European OEM's JV brands (Hesai ATX, >1 M)",
          "an unnamed European OEM's JV brands, almost certainly VW Group's (Hesai ATX, >1 M; note 5)"))

# ---------------------------------------------------------------- §B8 robotics
E.append(("S", "| **Hesai** | 239,273 (2024: 45,503) |",
          "None by segment (single reporting segment).",
          r"None by application. One reporting segment until Q1 2026; from Q2 2026 a Lidar segment (ADAS and robotics combined, RMB 815.9 M in Q2) and a Strategic Growth Initiatives segment (actuators and the Kosmo spatial-data platform, RMB 44.9 M) [P]. Market researcher CIC puts its 2024 robotics-lidar revenue at ≈\$90 M, 16.2% of that market [MR, in Hesai's Hong Kong prospectus]."))
E.append(("S", "| **RoboSense** | 303,000 | 185,500 |",
          "Robotics was \"close to half\" of H1 2026 product revenue (RMB 958 M) and the main source of product gross profit, per management (results call) [T].",
          "Robotics and other products earned RMB 709.8 M in 2025 (RMB 198.5 M in 2024), 39.1% of product revenue, at ≈RMB 2,300 a unit and a 39.7% gross margin [P]. Its 2026 filings no longer split product revenue, but robotics was \"nearly half\" of H1 2026 product revenue (RMB 958 M) and \"a primary source\" of product gross profit [P, H1 2026 results announcement]."))
E.append(("L", "  - Robotics therefore outsold ADAS only in Q1.",
          "  - Robotics therefore outsold ADAS only in Q1. RoboSense attributes this to mower lidars, which ship mainly in Q1 and Q4, ahead of the mowing season, leaving Q2 with \"very little contribution from lawnmowers\" [T, Q1 2026 results call]."))
E.append(("S", "- **Implied RoboSense robotics revenue per unit.**",
          "If \"close to half\" means",
          "If \"nearly half\" means"))
E.append(("A", "- **Implied RoboSense robotics revenue per unit.**",
          r"- **By robot type.** Neither company reports units by robot type in its filings, but both managements have given rounded splits on results calls [T, call transcripts, which are machine-made and contain errors]:"
          "\n"
          r"  - RoboSense said about 200,000 of its 303,000 robotics lidars in 2025 went into robot lawn mowers ($200/303\approx66\%$), put its share of mower lidar at about 70%, and guided 800,000–1,000,000 robotics lidars for 2026: 450,000–600,000 for mowers, 100,000–150,000 for delivery vehicles at two to four lidars each, and about 150,000 for industrial safety, cleaning and other robots [T]."
          "\n"
          r"  - Hesai said its JT series had shipped more than 200,000 units by end-2025, mainly to the mower brands Dreame, MOVA and Nexlawn, and that humanoid and quadruped lidars would reach five-digit annual volumes only in 2026. Most of its 2026 robotics volume, guided at more than 500,000 units, is mower lidar, and lidar mowers are 1–2% of the ≈20 M mowers sold each year [T]."
          "\n"
          r"  - Mowers therefore took roughly 350–400k of the two leaders' ≈542k robotics lidars in 2025, about two-thirds to three-quarters [E: RoboSense ≈200k plus Hesai ≈150–200k, i.e. most of its >200k JT units less fewer than 10k humanoid and quadruped units; $350/542\approx65\%$ and $400/542\approx74\%$]. That agrees with Hesai's 1–2% of 20 M, i.e. 200–400k lidar mowers. If both 200k figures hold, RoboSense had about half of the two leaders' mower lidars, not 70% [E]."))
E.append(("S", "| **Robot lawn mowers** |",
          "but gives no mower count [P]",
          "and put its 2025 mower lidars at about 200,000 on a results call [P/T]"))
E.append(("S", "| **Sidewalk delivery robots** (§B4a, subsection 4) |",
          "Serve: Ouster digital lidar under a multi-year agreement [P]. Avride: lidar to about 60 m [P]. Starship, Cartken, Coco and Woowa's Dilly carry no lidar product;",
          "Serve: one Ouster lidar per robot under a multi-year agreement [P]. Avride: lidar to about 60 m [P]. RoboSense lists Coco Robotics among its digital-lidar customers [P]. Starship, Cartken and Woowa's Dilly carry no lidar product;"))
E.append(("S", "| **Sidewalk delivery robots** (§B4a, subsection 4) |",
          "Serve about 2,000 robots;",
          "Serve more than 2,000 robots;"))

# ---------------------------------------------------------------- §C3a failed bets and public money
E.append(("S", "| **Insight LiDAR** (and parent Insight Photonic Solutions) | Colorado |",
          r"Chapter 11 filed 6 Jun 2024; liabilities \$10–50 M. A third amended plan was filed 24 Sep 2026, so the case is still open [P] | No sale found |",
          r"Chapter 11 filed 6 Jun 2024 by Insight Photonic Solutions and Insight Lidar (Bankr. D. Colo. 24-13141 and 24-13142), with estimated assets of \$1–10 M against liabilities of \$10–50 M [P]. Debtor-in-possession (DIP) financing, a court-approved loan that ranks ahead of existing debts, was denied in Nov 2024, and the US Trustee, the Justice Department office that supervises bankruptcy cases, moved in Jun 2025 to dismiss the case or convert it to liquidation. A disclosure statement was approved in Jun 2026 and an amended plan filed on 24 Sep 2026; the plan was unconfirmed in Oct 2026 [P, docket] | No sale motion on the docket [P] |"))
E.append(("S", "| **Aeva** | FMCW on silicon photonics (wavelength not officially stated; ≈1,550 nm assumed, §C3) | SPAC Mar 2021",
          r"SPAC Mar 2021 at ≈\$2.1 B implied [T]. Peak ≈\$4.1 B implied in Feb 2021, before the merger closed [E: weekly close \$19.50 pre-split $\times$ ≈210 M pro-forma shares; ≈\$4.6 B at the \$21.83 intraday high of 9 Feb 2021, T].",
          r"SPAC Mar 2021; the ≈\$2.1 B announced in Nov 2020 is an implied pro-forma equity value at the \$10 deal price, with an enterprise value of \$1.8 B [P]. Peak ≈\$4.2 B implied, before the merger closed [E: 211.4 M post-merger shares [P] × \$20.00, the highest close of the SPAC's shares on 10 Feb 2021, before the 1:5 reverse split [T]; ≈\$4.6 B at the \$21.835 intraday high of 9 Feb 2021 [T]]. After closing, the highest market value was ≈\$3.4 B on the first trading day, 15 Mar 2021 [E: 211.4 M × \$16.16 [T]]."))
E.append(("S", "| **Hybrid Lidar Systems AG** (Lower Saxony) |",
          "EIC Fund equity unconfirmed |",
          "No EIC Fund investment is public: the company is not on the EIC Fund's list of invested companies, and the 2023 press described the seven-figure equity only as a prospect [P/T]. Such silence is common: only 5 of the 17 companies selected for blended finance at the Jan 2023 cut-off appear on that list [E] |"))
E.append(("S", "| **VoxelSensors** (Brussels) |",
          "the NOVA coordination action €95,563 |",
          "the NOVA coordination action €95,563. No EIC Fund investment is public: VoxelSensors is not on the EIC Fund's list of invested companies, and its audited 2025 accounts show paid-in equity unchanged at €10.04 M through 2025, with convertible loans of €2.29 M (spring 2025) and €5 M (Jan 2026) from unnamed lenders [P] |"))
E.append(("S", "| **Scantinel** (Ulm) | ECSEL *Energy ECS*",
          "German co-funding for Energy ECS €331,398; Invest BW €989,780 (2021); an FMCW lidar project \"POVOS\" €740,474 from 2023, funder not identified [all T].",
          "German co-funding for Energy ECS €331,398 and Invest BW €989,780 (2021) [T]. €740,474 for an FMCW lidar sub-project in POV.OS (\"Professional Operating Vehicles Operating System\"), a joint project of the federal economics ministry (BMWK, today BMWE) administered by Projektträger TÜV Rheinland, which builds an open hardware and software platform for driverless farm, warehouse and mining machines (Jan 2023 – Mar 2026; 14 funded partners, among them AGCO, Bosch, Elektrobit, indurad and the University of Erlangen-Nürnberg; ≈€8.8 M of federal money) [P, federal funding catalogue; T for Scantinel's share]. Scantinel's sub-project is absent from the catalogue after its insolvency, so the amount actually paid is unknown [U]."))
E.append(("L", "- **Subawards:** reported subawards add roughly",
          r"- **Subawards, checked award by award** [I, USAspending; E for the bounds]. USAspending lists 31 subaward records naming Analog Photonics as sub-recipient, filed by six prime recipients under 11 prime awards between Nov 2013 and Jun 2026, totalling **\$34.2 M**. Prime recipients report subawards in FSRS (the federal subaward reporting system) and, since Mar 2025, in SAM.gov (the System for Award Management), and USAspending republishes them. The money comes from:"
          "\n"
          r"  - **AIM Photonics, \$19.9 M** (2016–2026): the American Institute for Manufacturing Integrated Photonics, the US integrated-photonics manufacturing institute, run by the Research Foundation for SUNY under Air Force cooperative agreements. Most of it pays for building and maintaining AIM's process design kit (PDK, the library of verified components a foundry gives chip designers), plus a quantum-dot laser project, a data-centre photonics challenge and two free-space-communication OPA projects, one with Lockheed Martin;"
          "\n"
          r"  - **NCMS, \$8.9 M** (2022–2025): the National Center for Manufacturing Sciences, for \"Integrated Photonics for Sustained Operations\" under a DoD maintenance-technology programme;"
          "\n"
          r"  - **Draper, \$2.3 M** (2020–2025): technical support under Navy Strategic Systems Programs contracts;"
          "\n"
          r"  - **DARPA via other primes, \$3.1 M**: UC Santa Barbara (PIPES, \$2.1 M), Rockwell Collins (DiSARMER, \$0.9 M) and Teledyne (MOABB, \$0.1 M)."
          "\n"
          r"  - About \$2.1 M of it (6%) concerns optical phased arrays, all for free-space communication or MOABB; none of it is automotive lidar [E]. The records read as separate funding actions; if every record that repeats an earlier description were instead a restated total, the sum would be \$28.3 M [E]. With the \$45.2 M of prime obligations, federal money to the company comes to $45.2+34.2\approx79$ (\$ M) over 2013–2026 [E]."))
E.append(("I", "Sources: https://cordis.europa.eu/project/id/947154 ;",
          "Whether EU and US research money as a whole is returning to lidar is counted programme by programme in §D8.\n\n"))
E.append(("S", "| **Luminar** | 1,550 nm fibre laser, InGaAs APD, two-axis mirror |",
          r"≈\$7.8 B market value at the first-day close of \$22.98 (3 Dec 2020) [T];",
          r"≈\$7.4 B market value at the first-day close of \$22.98 (3 Dec 2020) and ≈\$13.5 B at the peak close of \$41.80 (8 Dec 2020) [E: 323.9 M Class A and Class B shares at closing [P] × closing price [T]; prices before the 1-for-15 reverse split of 20 Nov 2024];"))
E.append(("S", "| **LeddarTech** (Québec) |",
          "after a bridge-loan default it made an assignment into bankruptcy under Canada's *Bankruptcy and Insolvency Act* on 18 Jun 2025.",
          r"after a bridge-loan default it made an assignment into bankruptcy under Canada's *Bankruptcy and Insolvency Act*, filed on 19 Jun 2025 (the company's release says 18 Jun), with Raymond Chabot Inc. as trustee [P]. Its sworn statement of affairs listed ≈\$1.8 M of assets, almost all cash, against ≈\$145.9 M of liabilities, \$138.9 M of them secured; the largest creditors were Investissement Québec (≈\$53.2 M) and the Desjardins group (≈\$40.3 M) [P; sums E; amounts presumably in Canadian dollars]."))
E.append(("S", "| **LeddarTech** (Québec) |",
          "No going-concern buyer; assets went to the bankruptcy trustee, and no IP sale was found [U]",
          r"No going-concern buyer. The holding company's subsidiaries and IP were listed at a nominal \$1, \"value undetermined\", and pledged to the secured lenders [P]. The patents (112 granted of more than 190 filed [T]) belong to the operating subsidiary, LeddarTech Inc. [P]; no sale of them or of the LeddarVision software was found [U]"))
E.append(("L", "| **TetraVue** | Pockels-cell flash lidar |",
          r"| **TetraVue** | Pockels-cell flash lidar | \$10 M Series A (2017) [T]; Robert Bosch Venture Capital took a minority stake, not control [P]. The original California corporation merged into a Delaware corporation of the same name on 17 Oct 2017 [P, via OpenCorporates]. That company filed for Chapter 7 liquidation, US court-supervised liquidation in which a trustee sells the assets and the business does not continue, on 26 Feb 2020 (Bankr. S.D. Cal. No. 20-00979). The court approved a sale of assets free and clear of liens on 17 Jul 2020, and the case closed on 21 Mar 2023 [P, docket]. Its California registration was forfeited on 28 Dec 2021 [P, via OpenCorporates] | Patents to **nLIGHT, Inc.**, a US maker of semiconductor and fibre lasers, assigned by the Chapter 7 trustee with effect from 24 Aug 2020; price not public [P, USPTO assignment records] | [Bosch](https://www.bosch-presse.de/pressportal/de/en/robert-bosch-venture-capital-invests-in-tetravue-89600.html); [docket](https://www.courtlistener.com/docket/16895668/tetravue-inc-a-delaware-corporation/); [assignment](https://patents.google.com/patent/US11209664B2/en) |"))
E.append(("S", "| **Strobe** (to GM/Cruise 2017; lidar fate undisclosed) |",
          "Wavelength, detector and steering undisclosed |",
          "A Strobe-era international application (filed Oct 2016; granted to GM as US 11,442,149 B2 and 11,675,078 B2) describes one laser and one detector behind a two-axis MEMS (micro-electro-mechanical) mirror used monostatically, prefers the 1,530–1,560 nm telecom C-band, and gives 1–100 GHz chirps and 333,000 points/s at 50 mW [P, patent]; a 2019 Cruise filing again claims a two-dimensional MEMS mirror [P, patent]. The patents show what was developed, not what shipped |"))
E.append(("S", "| **OURS Technology** (to Aurora 2021, \\$40.8 M) |",
          "Steering mechanism and wavelength undisclosed |",
          "Its patent titles trace the steering bet: an OPA using grating lobes (2017), then a switchable array of coherent pixels forming a focal-plane array (FPA) behind a lens (2019), then FMCW solid-state beam steering and optical-antenna arrays (2020–22) [P, patent titles; claims not reviewed]. No OURS document found states the wavelength; Aurora describes FirstLight as working around 1,550 nm [P] |"))
E.append(("S", "| **Baraja** (75% of staff cut 2023; IP for sale since Aug 2025) |",
          "**Spectrum-Scan:** a tunable laser into prism-like optics, steering by **wavelength** with no moving parts on at least one axis; RMCW ranging with interference rejection, and per-point Doppler from the HD25 (2022) [P]",
          "**Spectrum-Scan:** a C-band (1,550 ± 20 nm) telecom tunable laser of the sampled-grating distributed-Bragg-reflector (SG-DBR) type, which hops between wavelengths in tens of ns over ≈35 nm, steers the vertical fast axis by **wavelength** through prism-like dispersive optics with no moving parts, over up to 37° [P, white paper 2021]. The horizontal slow axis is mechanical: the 2021 white paper describes a continuously rotating diffractive optical element (DOE) of <100 g steering 120°, while a 2021–22 patent application claims counter-rotating Risley prisms [P; the patent is a claim, not a shipped design]. The first sensors ranged by random-modulation CW (RMCW) correlation on an avalanche photodiode (APD) with interference rejection; the Spectrum HD line (announced Nov 2021) brought homodyne detection for per-point Doppler and on-chip fast-axis steering, and its slow-axis mechanism is not stated [P/U]"))
E.append(("S", "| **Baraja** (75% of staff cut 2023; IP for sale since Aug 2025) |",
          "A laser that is fast, widely and mode-hop-free tunable *and* narrow enough in linewidth for coherent detection,",
          "A laser that can be addressed quickly and repeatably across a wide tuning range (the SG-DBR hops between wavelengths by design) and, for the homodyne HD, narrow enough in linewidth for coherent detection,"))
E.append(("S", "| **Scantinel** (insolvent 2025; assets to MicroVision) |",
          "an IMEC-made PIC with **parallel FMCW channels in a solid-state fast axis** [P] |",
          "an IMEC-made PIC with **parallel FMCW channels in a solid-state fast axis** [P]; a 2022 trade summary gives 256 channels on the PIC [S]. The laser, its tuning range and the point rate are not disclosed [U] |"))
E.append(("S", "| **Ibeo** (insolvent 2022; to MicroVision) |",
          "an **addressable ams VCSEL array** with a SPAD receiver [P/U] |",
          "an **addressable ams VCSEL array** with a SPAD receiver [P/U]. ams calls its VCSEL a \"core component\" and co-developed the emitter, driver and optics; who designed and made the SPAD receiver chip is not disclosed [S/U] |"))
E.append(("S", "| **TetraVue** (fate unknown) |",
          "| **TetraVue** (fate unknown) |",
          "| **TetraVue** (Chapter 7, 2020; patents to nLIGHT) |"))
E.append(("S", "| **TetraVue** (Chapter 7, 2020; patents to nLIGHT) |",
          "| Nothing independent found | Not found |",
          "| Nothing independent found | None found; the Chapter 7 petition and schedules are not freely available [U] |"))
E.append(("L", "  - **光勺:** a ¥5 M angel round",
          "  - **光勺 (北京光勺科技有限公司):** a phase-coded coherent lidar start-up founded in Jan 2019 that reported a ¥5 M angel round (a first outside investment, from individuals or small funds) in early 2019 [T]. It showed a road-test demo at CES 2020 and planned sales for Q3–Q4 2020 [T], and in Mar 2022 said it had reached small-batch readiness at end-2021 [T]. Nothing dated after Mar 2022 was found, and its web domain had lapsed by Oct 2024 [I]; registry aggregators still show the company as existing (存续) [S]."))
E.append(("L", "  - **映讯芯光:** ≈30 staff in 2022; no news since.",
          "  - **映讯芯光 (珠海映讯芯光科技有限公司):** not dormant. A supplier of FMCW lasers and silicon-photonic optical engines founded in Aug 2021, with 40 insured employees, it raised a Pre-A round of just under ¥100 M led by 深创投 (Shenzhen Capital Group), reported from 30 Dec 2025 [T]. The round is aimed mainly at co-packaged optics and data-centre uses, and FMCW lidar is one of eight target markets [P/T]."))
E.append(("S", "1. **Survivorship.** The worst outcomes",
          r"Luminar went from ≈\$7.8 B on its first trading day to cancellation",
          r"Luminar went from ≈\$13.5 B at its 8 Dec 2020 close to cancellation"))
E.append(("S", "| 2021 | Aeva peak,",
          r"Aeva peak, ≈\$4.1 B implied (Feb)",
          r"Aeva peak, ≈\$4.2 B implied (Feb)"))

# ---------------------------------------------------------------- §C3b, §C4, §C4d
E.append(("S", "| **Hesai ATX** (ToF) | 230 m at 10%, 3.84 Mpts/s, 8 W |",
          "the ATX S01 user manual gives 10 W typical (§E9)",
          "the ATX S01 user manual (A07, May 2026) gives 10 W typical, 355 g and 1.74 M points/s single return (§E9), so the headline 3.84 Mpts/s and 8 W may describe another variant or return mode [P/U]"))
E.append(("L", "- **Silicon absorption:** the absorption coefficient is",
          r"- **Silicon absorption:** the absorption coefficient is $\alpha\approx2.9\times10^2$ cm⁻¹ at 905 nm ($1/\alpha\approx35$ µm) and $1.83\times10^2$ cm⁻¹ at 940 nm ($1/\alpha\approx55$ µm) [I, Green 2008; the 905 nm value interpolated between the 900 and 910 nm entries]. Here $1/\alpha$ is the absorption length, the depth over which the light falls to $1/e$, so a thin silicon detector lets most 9xx-nm photons pass unabsorbed: a 10 µm absorbing layer captures $1-e^{-\alpha d}=25\%$ of them at 905 nm and 17% at 940 nm in one pass, where $d$ is the layer thickness [E]."))
E.append(("L", "- Seyond Falcon K1: its manual gives **1,520",
          r"- Seyond Falcon K1: its manual gives **1,520 \"vertical scanning lines\" per second** at 10 frames/s, configurable from 5 to 20 frames/s [P]. That is 152 lines per frame, close to the 144 implied by the manual's resolution table ($4.8°/0.08°=60$ lines inside the region of interest and $(25°-4.8°)/0.24°\approx84$ outside) [E]. A \"vertical scanning line\" is therefore one horizontal sweep per beam, and the polygon makes $1{,}520/N_{\rm beam}$ facet sweeps per second, where $N_{\rm beam}$ is the number of beams [E]. With four beams (§C4; the manual does not confirm the count) that is $1{,}520/4=380$ sweeps/s. Neither the facet count nor the speed is published: four beams on a four-facet polygon would need $1{,}520/(4\times4)=95$ rev/s (5,700 rpm), and on a five-facet polygon 76 rev/s (4,560 rpm) [E]."))
E.append(("S", "  [P, as quoted from the IEEE conference paper",
          "[P, as quoted from the IEEE conference paper \"Dynamic deformation of scanning mirrors\"; Brosens' 1972 original was not read]",
          "[I, as reproduced with its variable definitions by Urey (Proc. SPIE 4773, 2002) from P. J. Brosens, *Appl. Opt.* 11, 2987 (1972); the 1972 original is paywalled and was not read]"))
E.append(("S", "  [I, as reproduced with its variable definitions by Urey",
          "The coefficient 0.217 comes from Brosens' plate-bending analysis and is not derived here.",
          r"Here $f$ is in hertz, not the angular frequency $2\pi f$; $D$ is strictly the width across the rotation axis, and $\delta_{\max}$ the largest departure of the bent cross-section from the chord through the axis and the edges. A cantilever-strip estimate reproduces the coefficient [E]: each half of a mirror held along its axis, bent by the inertial load of the peak angular acceleration $(2\pi f)^2\theta_{\rm mech}$, gives $\delta_{\max}=0.226\,(1-\nu^2)\rho_{\rm m}f^2D^5\theta_{\rm mech}/(E\,t_{\rm m}^2)$, where $\nu$ is Poisson's ratio. That equals 0.217 for $\nu=0.2$, and 0.208–0.215 for silicon ($\nu=0.22$–0.28), within 1–4%."))
E.append(("L", "  - The current edition is ISO 16750-3:2023, whose profiles were not checked [U].",
          "  - The current edition, ISO 16750-3:2023, splits the body test by component size. Test IV covers small and lightweight devices under test (DUTs) on passenger-car sprung masses (§4.1.8), and Test XIV, taken from ISO 19453-3:2018, covers large and heavy DUTs on hybrid-electric and fully electric cars (§4.1.10) [P, official preview]. Its foreword says the vibration profiles were changed \"where necessary due to extended datasets of and experience from vehicle measurements\". The 2023 breakpoints and the mass threshold between the two classes are not in the public preview, so the 2012 profile is used here, and placing a 0.36–1.75 kg lidar in the small class is an assumption [U]."))

# ---------------------------------------------------------------- §C5a Sony
E.append(("S", "| Dead time | ≈6 ns (at 85 °C) |",
          "| Dead time | ≈6 ns (at 85 °C) |",
          "| Dead time | 6 ns at room temperature in the ISSCC 2021 development chip [P]; \"TBD\" on Sony's product page [P] |"))
E.append(("L", "- **Measured** [T, Sony figures]:",
          "- **Measured** [P, ISSCC 2021 paper 7.3, read in full; curve values E]:"))
E.append(("L", "  - PDE 22% at 905 nm; **14% at −40 °C**",
          "  - PDE 22% at 905 nm, the peak of the median curve near 60 °C (≈19% at 25 °C); **14% at −40 °C** and ≈17% at 125 °C. Against wavelength it falls from 29% at 850 nm to 21% at 905 nm and ≈15% at 940 nm (the paper's PDE figure, digitized) [P; E];"))
E.append(("L", "  - response 5–7 ns over temperature; maximum count rate 60 Mcps; power 1,192 mW;",
          "  - dead time 6 ns at room temperature, with passive quenching and recharge; jitter 300 ps; dark count rate 2,007 cps; afterpulsing 0.1% (4.9% at −40 °C); maximum count rate 60 Mcps, reached at 200 µW/cm²; power 1,192 mW on a 6.9 × 7.8 mm die;"))
E.append(("L", "  - with a MEMS scanner (a micro-electro-mechanical mirror): 150 m on a 10% target",
          "  - with a MEMS scanner (a micro-electro-mechanical mirror), 905 nm pulses of 4.5 ns at 45 W peak, and 168 × 63 points at 20 fps: 150 m on a 10% target and 200 m on a 95% target under 117 klx."))
E.append(("L", "- **The cold-temperature PDE drop is real.**",
          r"- **The cold-temperature PDE drop is real.** 14% at −40 °C against the 22% peak means $1-14/22=36\%$ fewer photons; against the ≈19.3% read off the curve at 25 °C it is $1-14/19.3=27\%$ fewer [E]."))
E.append(("S", "  - So the cold loss costs about **20% of range**",
          r"($1-\sqrt{17/22}=0.12$).",
          r"($1-\sqrt{17/22}=0.12$). Against the ≈19.3% at 25 °C the cold loss is ≈15% of range ($1-\sqrt{14/19.3}=0.15$) [E]."))
E.append(("S", "- **The PDE ladder.** Products went from 24% at 905 nm",
          "Sony's 2025 research pixel reached **51% at 905 nm and 42.5% at 940 nm** with a metal reflector (a mirror under the pixel that sends unabsorbed light back through the silicon) [I, VLSI 2025 T1-2]; at 905 nm that is $51/24=2.1$ times IMX459. Sony's research is therefore at least level with the 45% claimed for RoboSense's 2026 chip.",
          r"Sony's 2025 research pixel reached **42.5% at 940 nm** through doping design: a triggering probability of 92.9% at 3 V excess bias and a charge-collection efficiency of 98.8%, which leaves $0.425/(0.929\times0.988)=0.46$ for fill factor times absorption [P, VLSI 2025 T1-2 abstract; E]. A 905 nm figure and a metal reflector are not in the abstract or the programme entry [U]. At 940 nm that is $42.5/37\approx1.15$ times IMX479 and $42.5/15.3\approx2.8$ times the ISSCC 2021 chip, so Sony's research is roughly level with the 45% claimed for RoboSense's 2026 chip."))
E.append(("S", "2. **A peer-reviewed PDE roadmap that products follow",
          "51% at 905 nm was reached in 2025 research.",
          "42.5% at 940 nm was reached in 2025 research."))

# ---------------------------------------------------------------- Part D
E.append(("S", "Part D asks where the parts of an automotive lidar come from,",
          ", and the state of Chinese FMCW lidar (§D7).",
          ", the state of Chinese FMCW lidar (§D7), and whether EU and US public research money is returning to lidar (§D8)."))
E.append(("S", "  - **Thailand \"Galileo\" plant** (Bangkok),",
          "**Thailand \"Galileo\" plant** (Bangkok), intended to supply",
          r"**Thailand \"Galileo\" plant**, run by Hesai (Thailand) Limited (incorporated Jun 2023). Hesai's releases say \"Bangkok\" [P], while Thailand's Board of Investment (BOI) granted promotion for a THB 1.5 B (≈\$46 M) lidar project at Rojana Industrial Park in Phra Nakhon Si Ayutthaya, about 60 km north of Bangkok (Feb 2026) [T, relaying a government statement]. Hesai's filings show a leased 20,990 m² factory, under renovation in Apr 2026, plus about 25,600 m² of owned land, and RMB 77 M (≈\$11 M) of long-lived assets in Thailand by Jun 2026, about a quarter of the BOI project value [P/E]. No plant capacity has been published. The plant is intended to supply"))

D8 = r"""
## D8. Western public research funding: is it returning to lidar?

This section asks whether public research money in the European Union (EU) and the United States has turned back towards lidar since the collapse of many Western lidar companies (§C3a) and China's rise to dominance in automotive lidar (§D2–§D7). It counts every lidar project in the two databases that can be searched project by project: CORDIS for EU research grants, and SBIR.gov for the US small-business research programmes. It then reads the EU work programmes, the documents that define each funding call, for topics that name lidar. **The answer is flat interest, not renewal.** In both regions lidar's share of research money is no higher in 2023–2026 than in the late 2010s, and neither has a programme that targets lidar as such. The growth that exists is narrow and starts from small bases: coherent (FMCW) lidar and lidar on photonic integrated circuits (PICs) in the EU, each about five to six times more frequent per project than under the previous framework programme, and photonic-integrated and space-landing lidar in US small-business awards. This matters because public money is one of the few levers that could rebuild a Western lidar supply base (§D5, §G2). The record shows both governments paying for photonics infrastructure and enabling components, while the 2024–2026 measures against Chinese lidar (§D3) restrict purchases rather than fund suppliers. Company-level grants are in §C3a; defence budgets outside the two databases are not counted (end of section).

**Terms.**
- *CORDIS* is the European Commission's public database of the research and innovation projects it funds. *FP7* was the EU's Seventh Framework Programme for research (2007–2013), *Horizon 2020* (H2020) its successor (2014–2020), and *Horizon Europe* the current programme (2021–2027).
- Within them, the *European Research Council* (ERC) funds individual investigators; the *Marie Skłodowska-Curie Actions* (MSCA) fund researcher training, including doctoral networks; and the *European Innovation Council* (EIC) funds early research (Pathfinder), prototype validation (Transition) and start-ups (Accelerator). *Joint undertakings* (JUs) are EU–industry funding bodies, among them ECSEL, KDT and the Chips JU for electronics. *Research and innovation actions* (RIAs) and *innovation actions* (IAs) are collaborative grants awarded under the *topics* of a work programme.
- *SBIR* and *STTR* (Small Business Innovation Research and Small Business Technology Transfer) are US programmes that reserve part of federal agencies' research budgets for small firms. Phase I awards test feasibility and Phase II awards fund development; Phase III work is paid from other budgets.

**EU: how the count was made** [E unless tagged]
- *Data.* The CORDIS open-data files for FP7 (content of 23 Dec 2024), H2020 and Horizon Europe (content of 28 Aug 2026): 84,787 projects, each counted once by its grant number [P].
- *Search.* Titles, objectives and keywords were searched for lidar, ladar and laser radar; airborne, terrestrial and mobile laser scanning; laser altimetry and ceilometers; time-of-flight (ToF) depth cameras and 3D sensing; and laser rangefinders, optical ranging and comb-based distance measurement.
- *Relevance.* Each project scores $s=3t+2k+\min(m,5)$, where $t=1$ if a search term is in the title (otherwise 0), $k=1$ if one is in the keywords, and $m$ is the number of matches in the objective. A project is *lidar-relevant* if $s\ge2$. The 145 projects with $s=1$ mention lidar once in passing and are left out, because counting their full budgets would attribute large multi-sensor consortia to lidar.
- *Role and flags.* A relevant project counts as *hardware* when a sentence naming lidar also names a component (laser, detector, scanner, chip or instrument) with a development verb; otherwise it uses lidar data or bought sensors. *Coherent* marks FMCW, coherent or heterodyne detection and comb-based ranging. *Photonic-integrated* marks optical phased arrays (OPAs), PICs and silicon or silicon-nitride photonics, in a project that also names lidar or ranging.
- *Money* is the maximum EU contribution to the whole project, whatever share of it concerns lidar; JU national co-funding is excluded.
- *Rates.* Counts are divided by all projects starting in the same year: $r=1000\,N_{\rm L}/N_{\rm A}$, where $N_{\rm L}$ is the number of lidar-relevant projects starting in a year and $N_{\rm A}$ the number of all CORDIS projects starting that year. CORDIS lists a project only after its grant is signed, so start year 2025 is close to complete and 2026 is provisional; the rate removes the part of that lag that affects all programmes alike.
- *Check.* Of the 199 projects that CORDIS's own full-text search returns for "lidar", 178 are in the set. The other 21 mention lidar only in attached reports, among them atmospheric research-infrastructure projects, so atmospheric counts are low [P/E]. ToF depth-sensing projects that never name lidar are also undercounted.

**EU research projects relevant to lidar, by start year** (CORDIS; € M is the EU contribution in millions of euros; 2026 provisional) [P counts; E classification]

| Start year | All projects | Lidar-relevant: n (€ M) | Per 1,000 projects | Hardware: n (€ M) | Coherent: n (€ M) | Photonic-integrated: n (€ M) |
|---|---|---|---|---|---|---|
| 2007 | 169 | 0 | 0.00 | 0 | 0 | 0 |
| 2008 | 2,833 | 2 (2.37) | 0.71 | 1 (2.21) | 0 | 0 |
| 2009 | 2,901 | 2 (4.76) | 0.69 | 0 | 0 | 0 |
| 2010 | 3,602 | 3 (0.75) | 0.83 | 1 (0.50) | 0 | 0 |
| 2011 | 3,967 | 4 (2.31) | 1.01 | 3 (2.21) | 0 | 0 |
| 2012 | 4,332 | 5 (9.13) | 1.15 | 4 (8.92) | 0 | 0 |
| 2013 | 4,576 | 2 (2.20) | 0.44 | 1 (0.20) | 0 | 0 |
| 2014 | 3,320 | 1 (0.20) | 0.30 | 1 (0.20) | 1 (0.20) | 0 |
| 2015 | 5,040 | 7 (11.46) | 1.39 | 5 (4.26) | 0 | 0 |
| 2016 | 4,957 | 10 (32.74) | 2.02 | 4 (5.67) | 0 | 0 |
| 2017 | 4,975 | 4 (6.23) | 0.80 | 2 (0.37) | 0 | 0 |
| 2018 | 5,067 | 10 (24.22) | 1.97 | 6 (20.78) | 0 | 0 |
| 2019 | 5,562 | 15 (53.67) | 2.70 | 7 (30.59) | 0 | 2 (22.15) |
| 2020 | 4,507 | 17 (68.08) | 3.77 | 9 (31.32) | 1 (1.71) | 2 (6.26) |
| 2021 | 4,330 | 9 (16.99) | 2.08 | 5 (7.84) | 2 (4.66) | 2 (4.66) |
| 2022 | 4,278 | 7 (23.18) | 1.64 | 4 (12.34) | 1 (5.00) | 2 (7.48) |
| 2023 | 5,144 | 14 (53.07) | 2.72 | 9 (36.47) | 3 (9.76) | 6 (24.89) |
| 2024 | 4,959 | 10 (23.91) | 2.02 | 5 (12.75) | 2 (3.49) | 2 (5.50) |
| 2025 | 4,468 | 10 (34.63) | 2.24 | 6 (6.93) | 2 (1.27) | 3 (26.17) |
| 2026 | 4,750 | 10 (12.77) | 2.11 | 5 (2.72) | 0 | 1 (2.50) |

*How the numbers are derived* [E]: for 2023, $N_{\rm L}=14$ of $N_{\rm A}=5{,}144$ projects, so $r=1000\times14/5{,}144=2.72$ per thousand. The 14 projects hold €53.07 M of the €14,991 M granted to all projects starting in 2023, a share of $53.07/14{,}991=0.35\%$. Most of the 2019 photonic-integrated money is VIZTA, an ECSEL project led by STMicroelectronics (€21.1 M) whose lidar work is SPAD- and MEMS-based (§C3a), so the rule's flag is doubtful there.

**EU projects by programme period** [E]

| Start years | All projects | Lidar-relevant: n (€ M) | Per 1,000 | Share of EU money | Hardware: n (€ M) | Coherent: n (€ M) | Photonic-integrated: n (€ M) |
|---|---|---|---|---|---|---|---|
| 2007–2013 (FP7) | 22,380 | 18 (21.5) | 0.80 | 0.05% | 10 (14.0) | 0 | 0 |
| 2014–2020 (H2020) | 33,428 | 64 (196.6) | 1.91 | 0.31% | 34 (93.2) | 2 (1.9) | 4 (28.4) |
| 2021–2026 (Horizon Europe) | 27,929 | 60 (164.6) | 2.15 | 0.23% | 34 (79.1) | 10 (24.2) | 16 (71.2) |
| Rate ratio, 2021–2026 to 2014–2020 | | ×1.12 ($P=0.29$) | | | ×1.20 ($P=0.27$) | ×6.0 ($P=0.009$) | ×4.8 ($P=0.002$) |

*How the numbers are derived* [E]: the rate ratio for coherent lidar is $(10/27{,}929)/(2/33{,}428)=6.0$. If both windows had the same rate per project, each of the 12 coherent projects would fall in 2021–2026 with probability $q=27{,}929/(33{,}428+27{,}929)=0.455$, that window's share of all projects. The probability that 10 or more of the 12 land there is $P=\sum_{k=10}^{12}\binom{12}{k}q^{k}(1-q)^{12-k}\approx0.009$. The same one-sided binomial test gives $P\approx0.002$ for photonic-integrated lidar (16 of 20), but $P\approx0.29$ for all lidar-relevant projects (60 of 124) and $P\approx0.27$ for hardware (34 of 68), differences that chance explains easily. The money shares divide lidar-relevant EU money by all EU project money in the window: $164.6/71{,}692=0.23\%$ for 2021–2026, against $196.6/63{,}320=0.31\%$ for 2014–2020. FP7 records have no keyword field, which lowers FP7 scores, so part of the rise from FP7 to H2020 may be an artefact.

Reading the titles and objectives of the 2023–2026 projects removes two that are not lidar (a camera-only 3D perception system and a radar antenna). It also adds to both technology sets RETINA, an FMCW lidar on an indium-phosphide (InP) chip, and STARLight, a Chips JU silicon-photonics pilot with an FMCW lidar use case. With that reading, 2021–2026 holds 12 coherent projects (€55.3 M) and 17 photonic-integrated ones (€77.4 M); STARLight is €24.9 M of each, although Steerlight's lidar work inside it receives €0.46 M (§C3a) [P/E].

**Where the EU projects come from** [E]. Collaborative RIAs and IAs carry half of Horizon Europe's lidar-relevant money (€85.8 M of €164.6 M), the electronics JUs a fifth (€35.0 M, almost all of it STARLight), the EIC 14% (€22.5 M), and ERC and MSCA grants 12% between them. Collaborative lidar starts rose from 1 in 2021 to 10 in 2023, with the first Horizon Europe photonics and Earth-observation calls, then fell to 4, 2 and 0 in 2024–2026 (2026 provisional), while €150,000 ERC Proof of Concept grants and MSCA grants supply most of the rest. Automotive lidar-hardware starts were concentrated in 2023 (RETINA, CoRaLi-DAR, PARALIA, NiteLiDAR and LiSSA 3D); there was one in 2024 (6G-EWOC) and none clearly automotive in 2025–2026.

**What the EU work programmes ask for** [P; topic counts E]
- **Lidar is rarely named, and never as a target in its own right.** Across the work programmes of Clusters 3 to 6 and Research Infrastructures, lidar appears in 0 of 632 topics in 2021–2022, 4 of 568 in 2023–2024, 2 of 253 in 2025 and 0 of 327 in 2026–2027.
  - The one hardware topic is HORIZON-CL4-2025-04-DIGITAL-EMERGING-01, an IA of the Photonics Partnership, the EU's co-programmed partnership with the photonics industry platform Photonics21: €25.0 M in total, €4–6 M per project, taking sensors from TRL 3 to 7 (TRL, the technology readiness level, runs from 1 for a principle observed to 9 for a system proven in operation). Proposals must combine at least two sensing modalities, one of them photonic, from a list that opens with "3D sensing and imaging such as LIDAR" and continues with optical coherence tomography, fibre, gas, bio- and particle sensing. Lidar is therefore one optional example, not a requirement.
  - The other five name lidar as a sensor or a data source: border and maritime surveillance (HORIZON-CL3-2024-BM-01-02, €6.0 M); Copernicus, the EU Earth-observation programme, for the atmosphere (HORIZON-CL4-2023-SPACE-01-31, €8.6 M) and emergency management (-SPACE-01-32, €3.0 M); biodiversity monitoring (HORIZON-CL6-2024-BIODIV-01-2, €16.0 M); and a data platform for CCAM, connected, cooperative and automated mobility (HORIZON-CL5-2026-01-D6-06, about €4 M).
- **The topics that produced most coherent and photonic-integrated projects did not name lidar.** "Advanced multi-sensing systems" (HORIZON-CL4-2022-DIGITAL-EMERGING-01-03, €48 M) funded the radar–lidar projects CoRaLi-DAR and PARALIA; "Pervasive photonics" (HORIZON-CL4-2023-DIGITAL-EMERGING-01-51, €18 M) funded INPHOMIR; and "Advanced imaging and sensing" (-01-57, €20 M), which names autonomous vehicles and robots, funded RETINA. The 2026–2027 programme has no Photonics Partnership sensing topic.
- **The CCAM partnership funds perception as software and validation, not as sensors.** Its perception topics (2021, €15 M; 2024, €10 M; 2026, €8 M; and generative AI for perception, 2026, €13 M) do not name lidar.
- **Sovereignty language grows but stays generic.** The 2025 sensor topic asks projects to keep intellectual property and production means within the EU; the 2027 integrated-photonic-devices topic (HORIZON-CL4-2027-05-DIGITAL-EMERGING-03, €25 M) warns against dependence on a non-EU source; and a 2026 CCAM topic (HORIZON-CL5-2026-10-D6-02, €4 M) maps dependencies in automated-mobility supply chains and critical components. No topic names Chinese lidar. The only lidar money with an explicit sovereignty label is in space: the 2024 topic on European non-dependence in space technologies (HORIZON-CL4-2024-SPACE-01-73, €20.1 M) funds two lidar laser sources at ONERA, the French aerospace research centre: SIROCO (€3.07 M), a laser "with EU supply chain", and HALLOA (€2.74 M), a hybrid amplifier laser for lidar.

**The Chips Act's photonics money** [P unless tagged]
- *PIXEurope*, the Chips JU pilot line for advanced PICs, is coordinated by ICFO (the Institute of Photonic Sciences, Barcelona) with 20 partners in 11 countries. A pilot line under the European Chips Act is a shared pre-production facility that outside users can book. Its Horizon Europe grant is **€88.0 M** (101213727; Jun 2025 – May 2030), within a total of about €380–400 M [P/T]. It runs silicon, silicon-nitride, InP, thin-film lithium-niobate and silicon-carbide platforms; partner infrastructure opens to users from Nov 2026, and full capacity is planned for May 2028. Lidar is not among its named target applications; it appears only in the platform descriptions of imec and CEA-Leti, two of its partners.
- Two Chips JU projects carry FMCW lidar: STARLight (101194170, €24.9 M; 300 mm silicon photonics led by STMicroelectronics, with Steerlight's lidar as one use case, §C3a) and NEHIL (101194363, €1.50 M; imec Netherlands; a neuromorphic, heterogeneously integrated FMCW lidar from a joint call with Korea).
- The 2025 Chips JU automotive focus topics concern computing, not sensing: a RISC-V automotive hardware platform and heterogeneous integration for automotive computing [S].
- PIXEurope's EU grant alone exceeds all photonic-integrated lidar projects of 2021–2026 combined (€88.0 M against €71–77 M) [E]. The Chips Act is the largest public lever on European integrated photonics, but its effect on lidar is indirect.

**EU lidar-hardware projects started in 2023–2026** (CORDIS [P]; purpose from title and objective [E])

| CORDIS ID | Project | Coordinator (country) | EU € | Scheme | Purpose |
|---|---|---|---|---|---|
| 101194170 | STARLight | STMicroelectronics (FR) | 24,895,618 | Chips JU IA (2024) | 300 mm silicon photonics; Steerlight FMCW lidar use case |
| 101135529 | RETINA | AIMEN (ES) | 6,186,272 | IA, Photonics Partnership (2023) | FMCW lidar on an InP PIC, plus snapshot spectral imagers |
| 101120651 | Next-2Digits | NTUA (EL) | 5,134,570 | RIA, 2D-materials devices (2022) | 2D-material sensors; an Ommatidia lidar for drone mapping |
| 101135749 | INPHOMIR | G.E.M. Elettronica (IT) | 4,999,638 | RIA, Photonics Partnership (2023) | InP photonic building blocks for longer-wave infrared, with coherent sensing |
| 101092834 | CoRaLi-DAR | Silicon Austria Labs (AT) | 4,997,148 | RIA, Photonics Partnership (2022) | Co-integrated radar and lidar |
| 101093013 | PARALIA | Aristotle Univ. Thessaloniki (EL) | 4,995,910 | RIA, Photonics Partnership (2022) | Photonic multi-beam beamforming for radar–lidar fusion |
| 101312043 | BlueOcean | DTU (DK) | 4,122,170 | MSCA doctoral network | Photonic marine instruments, lidar among them |
| 101139182 | 6G-EWOC | UPC (ES) | 3,999,339 | SNS JU RIA | Optical 6G network with a connected-lidar prototype |
| 101189542 | SIROCO | ONERA (FR) | 3,071,641 | RIA, space non-dependence (2024) | Robust lidar laser source with an EU supply chain |
| 101086317 | EULIAA | Fraunhofer (DE) | 2,995,165 | IA, Cluster 6 observation | European lidar array for atmospheric climate monitoring |
| 101120353 | NiteLiDAR | DTU (DK) | 2,799,029 | MSCA doctoral network | Photonic and electronic integrated circuits for lidar |
| 101189970 | HALLOA | ONERA (FR) | 2,735,879 | RIA, space non-dependence (2024) | Hybrid amplifier laser for lidar |
| 101170019 | HyperSense | Lund University (SE) | 2,597,500 | ERC Consolidator | Hyperspectral Scheimpflug lidars |
| 101291179 | PI-MOLL | EPFL (CH) | 2,499,999 | EIC Transition (2025 call) | Integrated mode-locked laser; lidar among its applications |
| 190195250 | LiSSA 3D | Hybrid Lidar Systems (DE) | 2,400,260 | EIC Accelerator (2023) | Automotive and industrial lidar (§C3a) |
| 101160873 | OWL | Ocean Visuals (NO) | 2,212,272 | EIC Accelerator (2023) | Fluorescence lidar for submerged oil |
| 101125625 | HIGHRES | ULB (BE) | 1,987,369 | ERC Consolidator | Dual-comb spectroscopy and ranging |
| 101137084 | FORTE | Thales (FR) | 1,966,219 | EIC Transition (2023) | Frequency-agile lasers for FMCW lidar and fibre sensing |
| 101194363 | NEHIL | imec Netherlands (NL) | 1,499,968 | Chips JU RIA, joint call with Korea | Neuromorphic, heterogeneously integrated FMCW lidar |
| 101298573 | AQUADETECT | COFAC (PT) | 1,287,570 | MSCA staff exchange | Avalanche detectors for aquatic lidar |
| 101222367 | SPIDAR | Aalto University (FI) | 1,120,175 | EIC Pathfinder Challenge (2024, space) | GaAs photonic-chip FMCW lidar for space-debris mapping |

In this table, AIMEN is a Spanish technology centre, NTUA the National Technical University of Athens, DTU the Technical University of Denmark, UPC the Polytechnic University of Catalonia, ULB the Université libre de Bruxelles, COFAC the Portuguese cooperative behind Lusófona University, and GaAs gallium arsenide.

**US: how the count was made** [E unless tagged]
- *Data.* SBIR.gov, run by the Small Business Administration, publishes every SBIR/STTR award with its title, abstract, agency, phase and amount. This section uses the file dated 1 Oct 2026, with 219,649 awards through fiscal year (FY) 2026 [P]; a copy at SBIR.gov's older download address, dated 1 Jan 2026, stops at FY2023 and cannot show recent years [P]. The award year is the federal fiscal year, October to September [P, SBIR.gov data dictionary].
- *Money* is each award's full value, booked in its award year, so the series measures commitments rather than yearly spending, in nominal dollars.
- *Completeness.* FY2025 is incomplete for some agencies (no Department of Agriculture awards; 216 Department of Energy awards against 554 in FY2024), but the Department of Defense (DoD) and NASA, which provide 90% of lidar money, look complete [P/E]. FY2026 holds only 303 awards so far and is left out.
- *Selection.* An award *matches* if its title or abstract mentions lidar or ladar in any spelling, "laser radar", "light (or laser) detection and ranging" or "laser altimeter". It is *core* if the title carries the term or the text carries it at least twice, which drops passing mentions such as "cameras, radar and lidar"; core is the series used below. "Ladar" must be counted, because DoD used it for laser radar into the 2010s: SBIR.gov's own search for "lidar" alone returns 41 awards for FY2005 and 103 for FY2019 [P], whereas the match set, which includes ladar, has 91 and 102. A lidar-only search would show a doubling that did not happen.
- *Flags* within core: *coherent* (FMCW, heterodyne, homodyne, coherent or Doppler lidar), *photonic-integrated* (OPAs, PICs, silicon or silicon-nitride photonics, lidar on a chip) and *single-photon* (SPADs, Geiger-mode detection, photon counting). The rules were not checked award by award, and 285 awards that mention laser rangefinders, Geiger-mode arrays, OPAs or depth sensing without a lidar term are excluded.

**US lidar SBIR/STTR awards, annual averages by period** (nominal \$) [P, SBIR.gov; E, selection and arithmetic]

| Fiscal years | All SBIR/STTR (\$ B/yr) | Core awards/yr | Core \$ M/yr | Core share | Coherent: awards/yr (\$ M/yr) | Photonic-integrated: awards/yr (\$ M/yr) | Single-photon: awards/yr (\$ M/yr) |
|---|---|---|---|---|---|---|---|
| 2005–09 | 2.32 | 60.8 | 20.6 | 0.89% | 7.4 (2.1) | 0.6 (0.32) | 4.6 (2.0) |
| 2010–14 | 2.33 | 55.8 | 22.3 | 0.96% | 7.0 (2.7) | 1.0 (0.24) | 5.2 (2.3) |
| 2015–19 | 3.01 | 49.8 | 17.8 | 0.59% | 6.0 (1.8) | 0.6 (0.07) | 4.2 (1.6) |
| 2020–22 | 4.09 | 60.7 | 28.1 | 0.69% | 5.3 (2.1) | 2.3 (0.73) | 3.3 (1.5) |
| 2023–25 | 4.57 | 40.3 | 23.1 | 0.51% | 3.3 (1.5) | 3.0 (1.28) | 1.7 (1.1) |

*How the numbers are derived* [E]: each cell is a mean over the fiscal years of the period. For FY2023–25 the core money is $(17.4+25.3+26.7)/3=23.1$ (\$ M per year) and the programme's $(4.72+4.91+4.09)/3=4.57$ (\$ B per year), so lidar's share is $23.1/4{,}570=0.51\%$; for FY2015–19 it is $17.8/3{,}010=0.59\%$.

**Core lidar SBIR/STTR money by agency, \$ M per year** [P; E]

| Agency | FY2005–09 | FY2010–14 | FY2015–19 | FY2020–22 | FY2023–25 | Share of FY2005–25 |
|---|---|---|---|---|---|---|
| Air Force | 4.59 | 6.02 | 5.43 | 5.43 | 7.29 | 25.9% |
| Navy | 2.83 | 4.47 | 1.87 | 7.23 | 4.35 | 17.6% |
| Army | 3.30 | 2.15 | 1.78 | 2.12 | 0.41 | 9.6% |
| Missile Defense Agency | 3.09 | 0.94 | 0.38 | 1.47 | 0 | 5.8% |
| DARPA (Defense Advanced Research Projects Agency) | 0.61 | 0.63 | 0.39 | 1.21 | 1.19 | 3.4% |
| Other DoD | 0.87 | 0.91 | 0.04 | 1.42 | 1.65 | 4.0% |
| NASA | 3.98 | 5.23 | 6.34 | 4.64 | 5.47 | 23.6% |
| Department of Energy | 1.05 | 1.53 | 0.81 | 1.97 | 1.47 | 6.0% |
| National Science Foundation | 0.08 | 0.15 | 0.66 | 1.52 | 0.73 | 2.4% |
| Other civil agencies | 0.23 | 0.24 | 0.14 | 1.06 | 0.55 | 1.7% |
| **Total** | **20.6** | **22.3** | **17.8** | **28.1** | **23.1** | **\$457 M** |

**What the US series shows** [E unless tagged]
- **Flat in real terms.** Core lidar money averaged \$23.1 M a year in FY2023–25 against \$17.8 M in FY2015–19, a nominal rise of 30% ($23.1/17.8\approx1.30$). US consumer prices rose by about 28% between 2017 and 2024 [U], so in 2024 dollars the two periods are nearly equal ($17.8\times1.28\approx22.8$).
- **A falling share.** The whole programme grew by 52% over the same interval ($4.57/3.01\approx1.52$), so lidar's share fell from 0.59% to 0.51%. It was highest, 0.96%, in FY2010–14.
- **Fewer, larger awards.** Core awards fell from 49.8 to 40.3 a year, while the average core Phase II award grew from \$0.87 M to \$1.28 M.
- **No automotive boom.** FY2015–19, the years of the automotive lidar boom, are the low point of the series. Awards whose text points to cars or ground vehicles drew about \$1.0 M a year then and \$1.9 M a year in FY2023–25, by a keyword classification that was not reviewed. The boom was financed privately (§C3a).
- **Defence and space, not cars.** DoD provides two-thirds of the money and the Air Force alone a quarter; Army lidar awards have nearly disappeared, and the Missile Defense Agency's ladar-seeker work of the 2000s has ended. NASA provides another quarter. The largest recipients over FY2005–25 are specialist defence and remote-sensing firms: Areté Associates (\$28.3 M), Fibertek (\$25.1 M), Advanced Scientific Concepts (\$21.2 M), Physical Sciences Inc. (\$21.1 M) and Voxtel (\$20.5 M) [P]. None of the automotive lidar companies of §C3a is among the top 25.
- **Growth from small bases.** Photonic-integrated lidar rose from 0.6 awards and \$0.07 M a year in FY2015–19 to 3.0 awards and \$1.28 M a year in FY2023–25. The whole subset for FY2005–25, \$9.2 M, is smaller than DARPA's single MOABB contract with Analog Photonics (\$26.6 M, §C3a), so integrated lidar is funded through DARPA contracts rather than SBIR. Space and landing lidar doubled, from \$1.9 M to \$4.0 M a year, with Astrobotic Technology (\$5.9 M) and Psionic (\$2.2 M) among the largest FY2020–25 recipients [P].
- **Decline in coherent and single-photon awards.** Coherent lidar fell from six awards a year to 3.3, and single-photon lidar from about four to 1.7. SBIR shows no FMCW revival.
- **Lidar as an input.** Matches that mention lidar only in passing, mostly as one sensor in autonomy, inspection or digital-twin projects, grew from \$15.7 M to \$23.3 M a year, faster than lidar as a research subject.

**Reading** [E]
- **No renewal in volume on either side of the Atlantic.** EU lidar projects have held at about two per thousand since Horizon 2020, with a falling share of EU money (0.31% to 0.23%). US small-business lidar money is flat in real terms and a falling share of a growing programme (0.59% to 0.51%). Neither shows a 2024–2026 rise in response to China's lead in automotive lidar.
- **Renewal in technology, not volume.** Both record growth in chip-scale lidar: coherent and photonic-integrated projects in the EU (five- to sixfold per project and statistically significant, but from 2 and 4 projects), and photonic-integrated awards in US SBIR (from \$0.07 M to \$1.28 M a year). In the EU it comes from general photonics, EIC and training programmes, and in the US from DARPA rather than SBIR. That fits the reading of §C7a–§C7b that FMCW's open problems are chip-level.
- **Sovereignty is a label, not a lidar budget.** EU texts invoke strategic autonomy without targeting lidar, and the only sovereignty-labelled EU lidar money is €5.8 M for two space laser sources. The US measures of 2024–2026 (§D3) protect DoD purchasing from Chinese suppliers but fund no US lidar base. The large photonics programmes on both sides, PIXEurope and AIM Photonics (the US integrated-photonics manufacturing institute, §C3a), are generic infrastructure.
- **What could change this reading.** Defence money outside the two databases: the European Defence Fund (EDF), which is not in CORDIS (XenomatiX and VoxelSensors report EDF participation, §C3a), DARPA and other DoD programme lines, NASA missions, the European Space Agency (ESA) and national programmes. Counter-drone and military sensing are the most plausible sources of a Western uptick, and they are open items (Appendix 1).

Sources: https://cordis.europa.eu/data/cordis-HORIZONprojects-json.zip ; https://cordis.europa.eu/data/cordis-h2020projects-json.zip ; https://cordis.europa.eu/data/cordis-fp7projects-json.zip ; https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2025/wp-7-digital-industry-and-space_horizon-2025_en.pdf ; https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2025/wp-8-climate-energy-and-mobility_horizon-2025_en.pdf ; https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2023-2024/wp-7-digital-industry-and-space_horizon-2023-2024_en.pdf ; https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-7-digital-industry-and-space_horizon-2026-2027_en.pdf ; https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-8-climate-energy-and-mobility_horizon-2026-2027_en.pdf ; https://cordis.europa.eu/project/id/101213727 ; https://pixeurope.eu/ ; https://www.imec-int.com/en/press/europes-bid-leadership-photonic-chips-begins-barcelona ; https://cordis.europa.eu/project/id/101194170 ; https://cordis.europa.eu/project/id/101194363 ; https://cordis.europa.eu/project/id/101189542 ; https://cordis.europa.eu/project/id/101189970 ; https://cordis.europa.eu/project/id/101222367 ; https://cordis.europa.eu/project/id/101135529 ; https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv"""

E.append(("A", "Sources: https://en.lightic.tech/lark.html ;", D8))

# ---------------------------------------------------------------- Appendix 1
APPENDIX1 = r"""**Companies and failed technology bets**
- **TetraVue's sale and LeddarTech's IP.** TetraVue was liquidated under Chapter 7 in 2020 and its patents were assigned to nLIGHT (§C3a), but the sale price, and whether anything besides the patents was sold, are in paid court documents (the sale motion and the trustee's final report). What happened to LeddarTech's patents (112 granted) and its LeddarVision software after the Jun 2025 bankruptcy is unknown: the IP was pledged to the secured lenders, and no sale or transfer has been found. Both gaps leave the record of failed Western lidar companies in §C3a incomplete.
- **Peak market prices.** The share counts behind Aeva's and Luminar's peak values are from filings, but the peak prices come from market-data services, and Luminar's \$47.80 intraday high only from a search summary (§C3a, §G2).
- **光勺's registry record.** 映讯芯光 is an operating laser and optical-engine supplier (§C3a). 光勺 shows as existing in registry aggregators but has no dated news after Mar 2022; its record in China's official enterprise register and both firms' patents are unchecked. This bears on how thin the Chinese FMCW base is (§D7).
- **What the failed companies bet on.** Parts of the failed companies' technology bets are undisclosed (§C3a, subsection 3): which designs Strobe's and OURS's shipped hardware used (patents show a two-axis MEMS mirror at 1,530–1,560 nm for Strobe, and steering that moved from an OPA to a focal-plane array for OURS, whose wavelength no document states); the slow-axis mechanism of Baraja's Spectrum HD (its 2021 white paper describes a rotating diffractive element, a later patent application counter-rotating prisms) and the outcome of Baraja's 2025 IP sale; Scantinel's channel count (256 in one trade summary, not confirmed by a primary source), laser and tuning range; Bosch's architecture; and Ibeo's SPAD supplier. Without them, §C3a cannot say which technical choices, if any, contributed to each failure.
- **Insight LiDAR and Oryx.** The stated reason for Insight LiDAR's Chapter 11 filing is in the first-day declaration and the disclosure statements, which are paid court documents (D. Colo. 24-13141); the petition itself gives none, and the case was still open in Oct 2026. Whether Oryx tried to sell itself before closing is reported only in a search summary. Both bear on why the coherent and novel-steering start-ups failed (§C3a).
- **Pointcloud.** Its Tier 1 customer (a supplier that sells directly to carmakers) is known only from the company's own roadmap slide (a "first major Tier 1 commercial contract win" in Q1 2022), and Swiss public funding before 2023 has not been searched in ARAMIS, the federal register of research projects, or in the grant database of the SNSF (the Swiss National Science Foundation). They matter for how much commercial pull and public money this coherent developer had (§C3a).
- **European funding and exits.** No EIC Fund investment in VoxelSensors or Hybrid Lidar is public (§C3a), but German stock-corporation shareholders are not published and VoxelSensors' 2026 financing is unannounced, so neither can be excluded. How much of Scantinel's €740,474 POV.OS grant was paid before its insolvency is unknown. Fastree3D's exit terms per share (preferences, i.e. which investors are paid first, and earn-outs, i.e. payments that depend on later results) and whether its staff joined Hesai are also unknown. The last point matters for how much SPAD know-how Hesai acquired (§C5).
- **Hesai's Thailand plant.** Its capacity, jobs and Board of Investment terms are unpublished, and how the leased "Galileo" factory relates to the BOI-promoted project at Rojana Industrial Park, Ayutthaya, is undisclosed (§D4). Production is guided for "early 2027". The plant is central to the "Hesai-in-Mercedes template" for supplying Europe, and to whether an ownership-based US ban would reach it (§F3, §D5).
- **Aeva's European OEM.** No source names it. Aeva describes it as a "global Top 10" European OEM that already has a limited L3 system with ToF lidar on the road, and its 10-K (Mar 2026) says no definitive volume production agreement had been signed [P]. Hesai's May 2026 Mercedes L3 contract for Europe and China makes Mercedes unlikely though not impossible, and BMW fits the descriptors [E, low confidence]. Knowing it would show how large the first passenger-car FMCW program could be (§F3, §F6).

**Robotics, industrial and consumer markets**
- **Robot lidar by type.** Neither leading supplier reports lidar units by robot type in its filings. The split in §B8 (about two-thirds to three-quarters of the two leaders' 2025 robotics lidars in mowers) rests on management remarks on results calls; humanoid, AMR (autonomous mobile robot), cleaning-robot and robotaxi units are not reported.
- **Robotics revenue.** RoboSense disclosed robotics-and-other revenue for 2025 (RMB 709.8 M) and for each 2025 quarter, but for 2026 only that robotics was "nearly half" of product revenue. Hesai has never disclosed robotics revenue; the only figure is a market-research estimate of ≈\$90 M for 2024 in its Hong Kong prospectus. The value of robotics to the two leaders in 2026 can therefore be bounded but not measured (§B8).
- **China's delivery vans (§B4a).** Lidars per van are known for the main models (one to four; two on the current Zelos lines) [P/T]. Unknown: van lidar units by supplier (Hesai's 200,000-unit Zelos award is a nomination, not shipments); vehicles per remote operator; a collision rate per kilometre (only distances are published: Zelos 160 M km by Jul 2026, Neolix more than 100 M km by Mar 2026); and whether GB 44721-2026, which applies to vehicles with L3 or L4 systems from 1 Jul 2027, will bind vans that run under municipal pilot rules. These set the lidar volume the vans add (§F4 leaves it out) and test the supervision economics that §G7.5 contrasts with robotaxis.
- **Delivery robots outside China (§B4a, subsection 4).** Serve's one Ouster lidar per robot is confirmed [P]. Unknown: Gatik's current lidar supplier (a search summary names Luminar and Hesai [S]); Japan's count of notified delivery robots (no national tally found); and Japan's parcel volume for fiscal 2025 (fiscal 2024: 5.03 B, MLIT, Japan's transport ministry). They would size this market outside China.
- **ToF camera and sensor shares (§B8).** Supplier shares from a primary or independent source are missing; only market-research figures exist. The positions of the leading depth-sensor suppliers therefore rest on market-research estimates.
- **ToF and robotics-lidar prices (§B8).** Unknown: volume prices for ST's VD55H1 and Sony's IMX611 (time-of-flight sensor chips), and robotics-lidar prices by robot type, which neither Hesai nor RoboSense discloses. Revenue per unit bounds them: RoboSense's robotics lidars brought in ≈RMB 2,300 each in 2025 and ≈RMB 1,570 in Q4 2025, a quarter dominated by mower shipments [P/E]. Prices are needed to turn robotics unit counts into market value.
- **Sony AS-DT1 (§C5a).** Unknown: which SPAD sensor it uses; its price and typical power (the spec sheet gives only a 2.5 W maximum); the ambient conditions behind the spec sheet's outdoor figures to 40 m; and the IMX611's maximum histogram window (the span of arrival times its timing histogram records, which limits range). They decide how Sony's compact lidar compares with Chinese robotics units.
- **Robot vacuums.** Unknown: the share of robot vacuums with lidar navigation (AVC retail data, available by subscription); Slamtec and 3irobotix volumes; whether LDROBOT's 720k counts only dToF units. These determine how many lidar-type sensors this large consumer market really uses (§B8).
- **Foreign-brand lidar in China (§B6).** Known: VW's 192-line units are RoboSense's [T]; the Toyota bZ7 is a Hesai design win [P]; and Hesai's unnamed European OEM is almost certainly VW Group, which Hesai's Q2 2026 results name for a China-JV design win [P/E]. Unknown: lidar-trim shares of sales for any JV model whose lidar is optional (one unsourced post claims that 82% of FAW-VW ID. AURA T6 pre-orders chose a lidar version [U]); the suppliers for the Nissan N7 (RoboSense likely) and Buick Electra E7 (Hesai likely); and whether Honda and Hyundai China models offer lidar. These would show whether Western brands follow Chinese buyers to lidar (§F8, signpost 8).
- **Industrial-lidar market size.** A credible industrial-lidar and safety-scanner market size is missing. Market-research figures for safety laser scanners range from ≈\$0.32 B to ≈\$0.57 B (2025) [MR], and SICK (FY2025 sales €1.85 B [T]) reports no product split. CIC, in Hesai's Hong Kong prospectus, puts lidar revenue outside passenger-car ADAS (robots, robotaxis and industrial 3D lidar) at ≈\$0.6 B for 2024, excluding safety laser scanners [MR]. The spread limits any estimate of lidar's industrial market (§B8).

**Passenger-car take rates and exports**
- **Take-rate data.** The take rates (share of buyers choosing the option) of Mercedes Drive Pilot and BMW Personal Pilot were never published, and Lucid DreamDrive Pro's are unknown. Cadillac's historical night-vision figures (§A1) rest on the contemporaneous *Automotive News Europe* report, not on GM's underlying unit records. Take rates are the missing evidence behind §F3's 1–3% call and §G7.6's treatment of L3 as an option.
- **Chinese-brand lidar exports outside China.** A channel-by-channel estimate gives about 20–75k lidar cars in 2025 (central about 40k), half of them Li Auto (§B5). Still unknown: the brand and trim mix of China's 2025 zero-mileage exports, official overseas volumes by model for Zeekr, Aito, Avatr and Denza, the lidar fitment and take rate of export trims, and 2026 registrations outside Europe. This remains the largest uncertainty in §B5, and one reason §F3's 2026 trough call has low confidence.

**Undisclosed suppliers and sensor counts**

These gaps matter for two reasons. The Western pipeline in §F3 and the robotaxi and truck counts in §F4 multiply vehicles by lidars per vehicle. And a program's supplier decides whether a US ban on Chinese lidar would touch it (§F3, swing factor 1).
- **Rivian:** the supplier is unconfirmed. The R2's third-generation platform carries one front-facing long-range lidar [P], and RoboSense's Hong Kong results report an unnamed North American electric-pickup start-up among its design wins, which fits Rivian [P/E]. Rivian's Mar 2026 denial answered a different RoboSense customer description, one RoboSense places in the Chinese domestic market, so it does not exclude RoboSense (§B2, note 6) [E].
- **GM:** the vendor is undisclosed. GM's launch image shows one forward-facing lidar in a pod at the top centre of the windshield [P]; whether flush-mounted units also exist cannot be judged from the images.
- **Nissan:** one roof lidar is confirmed for next-generation ProPILOT, with 11 cameras and 5 radars [P]. Japanese trade press identifies the Sep 2025 prototypes' lidar as a Luminar unit [T], and Nissan entities appear on the service list of Luminar's Chapter 11 case [P]; Luminar's lidar business passed to MicroVision in Feb 2026. The production supplier for FY2027 is unknown.
- **Lucid–Nuro–Uber robotaxi (Gravity):** a reporter counted eight lidars (four long-range, four short-range) and 16 cameras on the CES 2026 show car [T]; the companies decline to confirm a count, and the suppliers are not disclosed. Nuro's own solid-state lidar sits in the front apron [T].
- **Ford:** the L3 lidar supplier, count and production configuration are unknown. The lidar plan itself is confirmed by a Field interview, and lidar does not appear in Ford's SEC filings for 2025–26 [P].
- **Zoox:** the exact count from an OEM specification is missing. A direct journalistic report gives 8 lidars, 18 cameras, 10 radar, 4 thermal and 8 microphones, the lidar count used in §F4. Zoox's NHTSA exemption petition and its voluntary safety self-assessment are the documents most likely to settle it.
- **Aurora:** the current (2025–26) lidar count per truck is not in the releases or filings found. Its second hardware generation, built by Fabrinet, entered service on 22 Jul 2026 with a FirstLight lidar detecting objects at 1,000 m, and a third generation built by Aumovio follows in H2 2027 [P]; the filings list lidars among single-source parts but give no count, and that Hesai supplies near-range units rests on trade reports, not filings. It feeds the truck and FMCW unit estimates in §F4 and §F5.
- **Autonomous trucking (§B4):** PACCAR-built trucks in Aurora's network still carried an observer in May 2026, and PACCAR's chief executive said in Jul 2026 that it had no plans to take the driver out [T]; their number is undisclosed. Kodiak's sixth-generation truck carried four lidars in two mirror-mounted sensor pods, and its filings place single-source suppliers in China, the EU and Mexico without naming a lidar maker [T/P]. Gatik's fleet size and the lidar suites of Gatik, Waabi and Bot Auto are unknown.
- **Gatik, Avride, May and PlusAI:** the current vehicle-level supplier mixes of Gatik, Avride and May Mobility are unknown. PlusAI designs no sensors: the truck makers that integrate its software (TRATON, IVECO, Hyundai) choose the lidars, and its 2023 Luminar agreement was an equity investment, not a supply contract [P].
- **Mercedes S-Class robotaxi (Abu Dhabi, with Momenta and Lumo):** it uses "LiDAR, radar and cameras" [T/S]; the count and supplier are not disclosed. Hesai's Mercedes L3 win is a different programme.

**Sensor and chip specifications**
- **Hesai Picasso:** the wavelength at which its PDE (photon detection efficiency) is quoted, its pixel pitch and its process node are unknown. They decide how its SPAD-SoC compares with Sony's parts (§C5).
- **Huawei 896-line:** its wavelength, emitter, detector and scanner are unknown; only media claims exist, some of low credibility. Its technology route therefore cannot be placed with confidence (§C3).
- **Foundries:** none is publicly named for any Chinese SPAD-SoC, which leaves open whether a foundry chokepoint exists (§C5, §D6, §F8 signpost 7). The ATX SiPM vendor is in the paywalled TechInsights DDT-2505-806.
- **Sony IMX479:** its power is not given in the press release, the product page, the VLSI 2025 and JSSC 2026 abstracts or the trade-press interview with its lead designer; the only published Sony figure is 1,192 mW for the ISSCC 2021 development chip (§C5a). Without it, Sony's newest automotive SPAD sensor cannot be compared on power with the Chinese in-house chips (§C5).
- **Hesai ATX figures.** The ATX S01 user manual (A07, May 2026) gives 10 W, 355 g and 1.74 M points/s single return, while the product page used in §C3b gives 8 W and 3.84 Mpts/s; which variant or return mode each set describes is unreconciled (§C3b, §E9).
- **Aeva sensor wattage:** it is not in Aeva releases or the distributor datasheet, which states passive cooling. Power is one input to the FMCW-versus-ToF comparison (§C7a).
- **Sony and Yonsei papers:** Sony's ISSCC 2021 paper 7.3 is read in full (§C5a). The VLSI 2025 T1-2 and C27-2 papers, the JSSC 2026 paper and Yonsei's VLSI 2025 T5-4 are closed access and were read only as abstracts. The T1-2 full text would show whether a 905 nm figure or a reflector accompanies its 42.5% at 940 nm, and the JSSC paper probably holds the IMX479's power.
- **Coherent and other long-range units.** Unknown: Aeva and Aurora gen-2 points/s, power and production scanners (Aurora states "around the 1550nm wavelength band"; only patent evidence exists for the scanners, §C3); Valeo SCALA 3 variants and detector (Valeo's page gives no wavelength or detector; SCALA 3 Platform is documented as SPAD); the InnovizTwo detector (filings say only "high sensitivity detector", with 2D MEMS mirrors at ≈905 nm); and Waymo's lidar wavelength (a Waymo patent describes a 1,550 nm fibre laser for a long-range steerable unit; nothing ties a wavelength to a shipping product). These gaps limit the route-by-route comparisons of §C3 and §C4.
- **FMCW (§C7b):** the channel count and per-channel receive power of the next coherent FPA (focal-plane array) or column chip are unknown, and no SOA (semiconductor optical amplifier) wall-plug efficiency at 105 °C has been published. Both set how many FMCW channels fit a sensor's power budget.
- **Mechanical scanners (§C4d).** Unknown: Seyond Falcon's facet count, polygon rpm, galvo frequency and beam count (patents and a teardown summary indicate a polygon on the horizontal axis and a galvo, a single oscillating mirror, on the vertical; the manual gives 1,520 scan lines per second, configurable from 5 to 20 frames/s); the ATX mirror's facet count and speed (its manual gives 10 Hz, a mirror turning about the vertical axis and a sweep direction that alternates each frame); RoboSense M1's SiPM vendor and beams per module (Livox describes HAP as a rotating-mirror design, not Risley prisms [P]); InnovizOne/Two mirror architecture and beam count; Cepton MMT's frequency and qualification data; the breakpoints of the ISO 16750-3:2023 body profiles (Test IV for small and Test XIV for large devices; China's adoption of the standard, still in drafting, will publish them); and Brosens' 1972 original (the constant is checked against Urey's reproduction and a cantilever-strip derivation). These set the scanner speed and vibration limits computed in §C4d.

**Regulation, standards and investigations**
- **China's export controls:** it is unknown whether the Ga/Ge/Sb (gallium, germanium, antimony) suspension is extended past 27 Nov 2026. The US says the wider truce runs to 10 Jan 2027, but no MOFCOM (China's Ministry of Commerce) notice on Announcement 72 was found. A lapse would hit Western laser substrates and germanium optics (§D2, §F8 signpost 4).
- **NHTSA EA26002:** the outcome is unknown. The investigation is open, and Tesla's reply to the Jul 2026 information request is not public. It bears on confidence in Tesla's camera-only design (§F7, §F8 signpost 1).
- **Headlight regulation figures (§A6):** these are resolved for the UN R48 summed reference-value limit of 100 (nominally 430,000 cd) and the UN R149 215,000 cd individual maximum. The exact measured aggregate interpretation depends on the R48 amendment series and rounded reference marks. A matched, vehicle-level comparison of actual EU and US beam patterns remains open; it would turn the regulatory limits into a measured difference between the two markets.
- **IEC 60825-1 (the laser eye-safety standard):** the $C_4$ wavelength coefficient and the conditional long-exposure comparison are checked; the AM1.5G values (the standard solar spectrum, used for sunlight background) match the official ASTM G173-03 file, and the silicon absorption values follow Green 2008. A nanosecond-pulse comparison that mixed editions of the standard is not used. Product-specific Class 1 calculations cannot be made from public documents: the Hesai ATX S01 and Seyond Falcon K1 manuals state the class but not the pulse energy, pulse duration, repetition rate or exit-beam size. All [E] calculations are order-of-magnitude, with stated assumptions.

**Public research funding (§D8)**
- **Channels not counted.** On the EU side, the European Defence Fund, ESA, national programmes, the EIC challenge texts and the Chips JU work-programme texts were not reviewed; on the US side, DARPA and other DoD programme lines, NASA missions, DOE, NSF and Phase III awards were not counted. Defence and counter-drone sensing are the most plausible sources of a Western uptick, so the "flat" reading of §D8 holds only for civil research grants and US small-business awards.
- **Search coverage.** The EU count undercounts ToF depth-sensing projects that never name lidar and atmospheric projects that name it only in attached reports; the US count excludes 285 awards that mention rangefinders, Geiger-mode arrays, OPAs or depth sensing without a lidar term. Neither selection was checked award by award.

**Contested or second-hand figures**
- **Tesla's active unsupervised fleet size** is uncertain. Registrations (546 in Texas on 26 Sep 2026) are an upper bound; crowdsourced counts suggest ≈300 active across Texas and Florida [U]. The number matters for §F7's calls on Tesla's fleet.
- **Yole's technology split** (rotating mirror 66% and MEMS 32% of 2024E passenger-car volumes, where 2024E is Yole's estimate for 2024; 905/940 nm ≈90%) comes from search extracts of the page for Yole's *LiDAR for Automotive 2024*, not from the full report; the 2025 edition may revise it. It is a reference point for the technology shares in §C2 and §F5.

"""
E.append(("B", "**Companies and failed technology bets**", "# Appendix 2 — Selected sources", APPENDIX1))
