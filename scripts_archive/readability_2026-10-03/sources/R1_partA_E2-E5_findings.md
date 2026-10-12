# Round 4 source findings: R1_partA_E2-E5

Report checked: `automotive_perception_report_2026-09-27.md`, sha256 prefix b2dd35a90bdb. Every `old` string below was copied from that version and occurs exactly once in it (checked with `scripts/R1A_check_old_strings.py`: 28 blocks, all 1×). Section names follow that version (the radar-market sideline is §E2a).

## R1_partA_E2-E5-01

- **Question:** Which IIHS work gave the "superior to advanced with high beams, to basic with low beams" result, on which vehicles, in which year, against which "superior" condition, and how large was the "small IIHS track sample"?
- **Answer:** The grades come from IIHS research track tests, not from its official night ratings (which began in Aug 2022). IIHS put eight small SUVs from eight makers through its standard daylight vehicle-to-pedestrian test in full darkness on its covered track, each once with high beams and once with low beams, and scored them with the daylight rating system. The vehicles were the 2019 Subaru Forester, 2019 Volvo XC40, 2020 Honda CR-V, 2020 Hyundai Venue, 2021 Chevrolet Trailblazer, 2021 Ford Bronco Sport, 2021 Toyota C-HR and 2022 Volkswagen Taos. Excluding the radar-only Taos, performance generally fell enough to move vehicles from superior (their daylight grade) to advanced with high beams and to basic with low beams. The Taos scored about the same in the dark, but it was also the worst daytime performer. The sample size is therefore eight vehicles (the C-HR was tested with both good and poor headlights). On headlights, IIHS found no clear association: the two worst low-beam performers (CR-V, XC40) had good-rated headlights, and the C-HR beat all the others on low beams even with poor headlights.
- **Source:** IIHS, "Pedestrian crash avoidance systems cut crashes — but not in the dark", news release, 3 Feb 2022, section "Nighttime track tests". https://www.iihs.org/news/detail/pedestrian-crash-avoidance-systems-cut-crashes--but-not-in-the-dark . Full text read (saved HTML). The official night-test release of 30 Aug 2022 (https://www.iihs.org/news/detail/few-vehicles-excel-in-new-nighttime-test-of-pedestrian-autobrake) was also read; it does not contain these grades.
- **Evidence tag:** [I] (IIHS's own independent track tests).
- **Confidence:** high — the release states the sample, the beams and the grade changes explicitly.
- **Proposed edit:**
  - `old`:
    ```text
    - **Camera AEB is also headlight-limited.** IIHS night pedestrian-AEB ratings fell from superior to advanced with high beams, and to basic with low beams (§E6). Superior, advanced and basic are IIHS rating grades, in descending order.
    ```
  - `new`:
    ```text
    - **Camera AEB is also headlight-limited.** In IIHS research track tests of eight small SUVs (model years 2019–2022), each run in full darkness once with high beams and once with low beams and scored with IIHS's daylight pedestrian-AEB rating system, performance generally fell from superior to advanced with high beams and from superior to basic with low beams; only the radar-only Volkswagen Taos scored about as well as in daylight, and it was also the worst daytime performer [I, IIHS, 3 Feb 2022]. Superior, advanced and basic are IIHS rating grades, in descending order.
    ```
  - `old`:
    ```text
    - The cited small IIHS track sample did not establish that better-rated headlights alone predict better night AEB results.
    ```
  - `new`:
    ```text
    - In that eight-vehicle sample, better-rated headlights did not go with better night scores: the two worst low-beam performers, the Honda CR-V and Volvo XC40, had good-rated headlights, and the Toyota C-HR outperformed all the others on low beams even with poor-rated headlights [I, IIHS, 3 Feb 2022].
    ```
- **Appendix 2 entry:** none (listed as "IIHS, pedestrian AEB at night").

## R1_partA_E2-E5-02

- **Question:** To which product does ResearchInChina's "below \$100" expectation refer?
- **Answer:** The source does not say. Its summary gives the basic-imaging-radar price fall (RMB 500–1,000 in early 2024 to RMB 200–400 in 2025, 1/5–1/10 of a lidar), then a separate sentence saying that with chip-process optimization (it names NXP's S32R47 processor and Milliverse's 8T8R MVRA188 chip) and scale "the cost is expected to drop below \$100". The sentence names no radar class. The Chinese original by the same firm (佐思汽研) also says 100美元, i.e. US dollars, not yuan, so it is not a mistranslation of RMB 100. Because the basic imaging radar already costs about \$28–56, the figure cannot describe that product as written, and the source gives nothing to attach it to another one. The clause should go.
- **Source:** ResearchInChina, *Automotive 4D Radar Industry Research Report, 2025* (Dec 2025, 260 pp.), public summary, http://www.researchinchina.com/Htmls/Report/2025/78124.html (summary read in full; the same text is on the Research and Markets page already in the §E2a source list). Chinese summary: 佐思汽研, "4D毫米波雷达研究：从'可选'变'刚需'", https://www.smartautoclub.com/p/109685/ (read in full). The GlobeNewswire release in the §E2a list carries no price text.
- **Evidence tag:** [MR].
- **Confidence:** high — both language versions were read and neither names the product.
- **Proposed edit:**
  - `old`:
    ```text
    The same source puts this radar at 1/5–1/10 of a lidar's price and expects it to fall below \$100 [MR, ResearchInChina; not independently corroborated].
    ```
  - `new`:
    ```text
    The same source puts this radar at 1/5–1/10 of a lidar's price [MR, ResearchInChina; not independently corroborated].
    ```
- **Appendix 2 entry:** ResearchInChina, Automotive 4D Radar Industry Research Report 2025, summary (basic-imaging-radar prices, installations): http://www.researchinchina.com/Htmls/Report/2025/78124.html

## R1_partA_E2-E5-03

- **Question:** What sign convention does IIHS use for the measured factory aims, and how should the range be written?
- **Answer:** IIHS counts downward aim as negative. Its rationale gives the angle from a 69 cm lamp down to the 25 cm sensor at 100 m as −0.25°, and the SAE-recommended aim for lamps above 90 cm as −0.38° (both downward). Figure 1 plots both lamps of 21 vehicles (seven 2015 models, three vehicles each, full tank and 77 kg driver ballast): the values run from about −0.54° (2015 Toyota Prius V, right lamp) to about +0.39° (2015 Jeep Cherokee, left lamp), and most are negative. So the range is about 0.5° below to 0.4° above the horizontal. All lamps below 90 cm were within SAE J599's 0 ± 0.76°.
- **Source:** IIHS, *Rationale and Supporting Work for Headlight Test and Rating Protocol*, Aug 2015, pp. 1–2 and Figure 1. https://www.iihs.org/media/9b0f599a-7a50-4bc4-b8d2-1cf6b52a128a/VSGFZg/Ratings/Protocols/current/headlight_rationale_supporting_work.pdf . Full text read (all 12 pages rendered; Figure 1 read at 300 dpi).
- **Evidence tag:** [I].
- **Confidence:** high — the sign convention is fixed by two worked angles in the same text.
- **Proposed edit:**
  - `old`:
    ```text
    - IIHS measured factory aims on new cars between about −0.5° and +0.4° [I].
    ```
  - `new`:
    ```text
    - IIHS measured the factory aim of both headlamps on 21 new 2015-model vehicles (three of each of seven models) and found aims between about 0.5° below and 0.4° above the horizontal, most of them below it [I].
    ```
- **Appendix 2 entry:** none (listed as "IIHS headlight rating rationale").

## R1_partA_E2-E5-04

- **Question:** What is an ADB transition zone, which rule or practice gives "about 4°", and what does the 1° rule mean for the beam?
- **Answer:**
  - Definition: FMVSS 108 S3 defines the transition zone as the portion of an adaptive driving beam between an area of reduced intensity and an area of unreduced intensity. SAE J3069 (MAR2021) defines it as the area where the unreduced intensity transitions to the non-glare zone, without giving a width.
  - US rule: S9.4.1.6.4.5 permits a transition zone "not to exceed 1.0 degree in either the horizontal or vertical direction"; inside it the lower- and upper-beam test points do not apply, except the upper-beam maximum at H–V. Beyond it the full upper-beam photometry (Table XVIII) applies, so within 1° of the shadow's edge the beam must already be back at high-beam level (for example 5,000 cd at 1U 3L for a UB2 lamp in NHTSA's worked example).
  - "About 4°" is industry practice, not a rule. NHTSA's final rule found no transition-zone width in UN R48 or R123 (only aiming tolerances of ±0.5°, and ±1° horizontally in R123). In the petitions, SAE, Stanley, Valeo, the Alliance, Toyota, Volkswagen and TSEI asked NHTSA to allow 4°; Valeo's intensity scan showed that reaching full upper-beam intensity takes at least 4°, Koito showed its ADB systems use about 4°, and petitioners said most ADB systems sold elsewhere would fail the 1° rule. NHTSA denied all petitions on 30 Dec 2024, noting that at 50 m a 4° zone is 3.5 m wide and could cover a whole adjacent lane.
  - Geometry [E]: the zone width at distance $R$ is $w=R\tan\theta$; at $R=50$ m, $50\times\tan1^\circ\approx0.87$ m and $50\times\tan4^\circ\approx3.50$ m (NHTSA's 3.5 m).
- **Source:** 49 CFR 571.108, S3 (definition) and S9.4.1.6.4.5, CFR 2025 edition, p. 411, https://www.govinfo.gov/link/cfr/49/571?link-type=pdf&sectionnum=108&year=mostrecent (pages rendered). NHTSA ADB final rule, 87 FR 9916 (22 Feb 2022), Section VIII.D.5, p. 9987, and Appendix B worked example, https://www.govinfo.gov/content/pkg/FR-2022-02-22/pdf/2022-02451.pdf (pages rendered). NHTSA denial of petitions for reconsideration, 89 FR 106365–106374 (30 Dec 2024), Section E "Transition Zone", pp. 106371–106372, https://www.govinfo.gov/content/pkg/FR-2024-12-30/html/2024-31141.htm (full text read).
- **Evidence tag:** [P].
- **Confidence:** high — definition, width and the 4° petitions are all stated in the regulator's own documents.
- **Proposed edit:**
  - `old`:
    ```text
        - It requires a 1° transition zone, against about 4° elsewhere.
    ```
  - `new`:
    ```text
        - Its transition zone, the part of the adaptive beam between a dimmed area and full high beam, may be no wider than 1° horizontally or vertically, and full high-beam photometry applies beyond it (FMVSS 108 S9.4.1.6.4.5) [P]. UN R48, UN R123 and SAE J3069 set no width for this zone; petitioners asked NHTSA for 4°, and Valeo and Koito showed ADB beams that need about 4° to reach full intensity. At 50 m a 1° zone is about 0.9 m wide and a 4° zone about 3.5 m ($50\times\tan1^\circ\approx0.87$ m; $50\times\tan4^\circ\approx3.50$ m), enough to cover an adjacent lane, which is why NHTSA kept 1° [P, NHTSA, 30 Dec 2024].
    ```
  - `old`:
    ```text
    ADB also needs a camera to detect lamps at hundreds of metres, with some latency and transition zones.
    ```
  - `new`:
    ```text
    ADB also needs a camera to detect lamps at hundreds of metres, with some latency, and each shadow is bordered by transition zones that are not lit to full high-beam level (§A6.3).
    ```
- **Appendix 2 entry:** FMVSS 108 codified text, S3 and S9.4.1.6.4.5 (ADB transition zone at most 1.0°): https://www.govinfo.gov/link/cfr/49/571?link-type=pdf&sectionnum=108&year=mostrecent (the final rule and the Dec 2024 denial are already listed).

## R1_partA_E2-E5-05

- **Question:** Which Cruise incident discarded correct lidar data, what did the lidar show, and what is the Cummings reference?
- **Answer:** The 23 Mar 2023 San Francisco collision with an articulated Muni bus, not the Oct 2023 pedestrian-dragging crash. A driverless Cruise car followed the bus as it pulled out of a stop into its lane; the rear section then hid the front section and the bus slowed. The software kept predicting the bus's motion from the hidden front section, concluded it was still moving forward and braked too late, rear-ending it. Cruise filed a voluntary recall of the software on 300 vehicles (versions from 12 Jan 2023; fixed 25 Mar 2023). Cummings, citing Cruise's explanation, writes that "the model rejected the lidar data that correctly detected the bus", i.e. the lidar placed the bus's rear section where it actually was, but the prediction model's estimate overrode it.
- **Source:** Cruise LLC, Part 573 Safety Recall Report 23E-029, submitted 3 Apr 2023, pp. 1–4, https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23E029-4270.PDF (full text read; it does not mention lidar). M. L. Cummings, "What Self-Driving Cars Tell Us About AI Risks", *IEEE Spectrum*, 30 Jul 2023, https://spectrum.ieee.org/self-driving-cars-2662494269 (article read).
- **Evidence tag:** [P] for the incident and recall; [T] for the lidar statement (a magazine article by an academic, relaying Cruise's account).
- **Confidence:** medium — the lidar detail rests on Cummings's account of Cruise's explanation, not on a Cruise document.
- **Proposed edit:**
  - `old`:
    ```text
    - **Cruise (GM's robotaxi subsidiary), 2023:** its system discarded correct lidar data (Cummings).
    ```
  - `new`:
    ```text
    - **Cruise (GM's robotaxi subsidiary), 23 Mar 2023:** a driverless Cruise car ran into the back of an articulated San Francisco Muni bus that had pulled out of a stop ahead of it and then slowed. The software predicted the bus's motion from its front section, which the rear section had hidden, concluded that the bus was still moving and braked too late; Cruise recalled the software of 300 vehicles [P, Cruise recall report 23E-029]. Cummings reports that "the model rejected the lidar data that correctly detected the bus" [T, Cummings, *IEEE Spectrum*, 30 Jul 2023].
    ```
- **Appendix 2 entry:**
  - Cruise Part 573 Safety Recall Report 23E-029 (articulated-bus collision, 23 Mar 2023): https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23E029-4270.PDF
  - Cummings, "What Self-Driving Cars Tell Us About AI Risks", *IEEE Spectrum* (30 Jul 2023): https://spectrum.ieee.org/self-driving-cars-2662494269

## R1_partA_E2-E5-06

- **Question:** Which LET-3D-AP values support "camera error is almost purely depth"?
- **Answer:** Table II (vehicle class, 10% longitudinal tolerance, Waymo's 80-segment camera-only test set):

  | Range | BEVFormer 3D AP | BEVFormer LET-3D-AP | PointPillars 3D AP | PointPillars LET-3D-AP |
  |---|---|---|---|---|
  | 0–30 m | 79.7 | 89.7 | 88.2 | 88.5 |
  | 30–50 m | 47.2 | 80.6 | 76.4 | 78.5 |
  | >50 m | 20.5 | 50.1 | 58.4 | 66.2 |
  | All vehicles | 50.7 | 82.9 | 78.6 | 80.7 |

  Within 50 m the tolerance lifts the camera to or slightly above the lidar, so its error there is almost entirely longitudinal. Beyond 50 m it rises only to 50.1, below the lidar's 58.4 even without tolerance, so at long range the camera's errors are not all depth errors within 10% of range. The paper also reports mean longitudinal affinity (mLA) for BEVFormer of 0.839, 0.850 and 0.776 in the three bands, which it reads as depth error roughly proportional to range.
- **Source:** W.-C. Hung, V. Casser, H. Kretzschmar, J.-J. Hwang, D. Anguelov (Waymo), "LET-3D-AP: Longitudinal Error Tolerant 3D Average Precision for Camera-Only 3D Detection", arXiv:2206.07705v2, 3 May 2024, Table II and Section V.D. https://arxiv.org/abs/2206.07705 . Full text read (all 8 pages rendered).
- **Evidence tag:** [I].
- **Confidence:** high — values read from the table image.
- **Proposed edit:**
  - `old`:
    ```text
    - With a 10% longitudinal tolerance, i.e. when a detection may be off in range (along the line of sight) by up to 10% of the distance, the camera's AP rises to about the lidar's: **camera error is almost purely depth**, and it grows with range [I]. The camera finds the objects; it misjudges how far away they are.
    ```
  - `new`:
    ```text
    - With a 10% longitudinal tolerance, i.e. when a detection may be off in range (along the line of sight) by up to 10% of the distance, the camera's vehicle AP (LET-3D-AP) rises to 89.7 at 0–30 m and 80.6 at 30–50 m, level with or slightly above the lidar's 88.5 and 78.5 under the same tolerance, and to 82.9 against 80.7 over all ranges [I]. Within 50 m, then, **camera error is almost purely depth**: the camera finds the objects but misjudges how far away they are. Beyond 50 m the tolerance lifts the camera only from 20.5 to 50.1, against the lidar's 66.2 (58.4 without tolerance), so at long range the camera also misses objects or places them off by more than 10% of their range [I].
    ```
- **Appendix 2 entry:** none (listed as "LET-3D-AP (Waymo)").

## R1_partA_E2-E5-07

- **Question:** Did any fatal crash attributable to the Waymo system occur within the 271 M rider-only miles to Jun 2026?
- **Answer:** No fatal crash has been attributed to the Waymo Driver. NHTSA's Standing General Order data hold three Waymo reports with a fatality up to the latest file (reports submitted to Aug 2026):
  - San Francisco, 19 Jan 2025, 18:07: the unoccupied Waymo was stopped in a queue when an SUV travelling at an extreme speed hit the car behind it, starting a chain collision; one person and a dog died. San Francisco police and Waymo said the Waymo was not responsible.
  - Tempe, 14 Sep 2025, 01:21: the empty Waymo was slowing with its turn signal on to yield to a pedestrian when a motorcyclist hit its rear; the rider fell into the next lane and was struck by a passing car that left the scene, and died.
  - Dallas, 7 Aug 2026, 23:31: a pedestrian walking in the opposite lanes was struck by an SUV and thrown into the slowing Waymo; police said no one was at fault. This one falls after Jun 2026.

  Two deaths therefore occurred in crashes involving Waymo vehicles within the period, neither caused by the system.
- **Source:** NHTSA, Standing General Order 2021-01 ADS incident reports: current file https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADS.csv (reports Jun 2025–Aug 2026; report IDs 30270-11713 Tempe, 30270-16196 Dallas) and archive https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Incident_Reports_ADS.csv (Jul 2021–Jun 2025; report 30270-9724 San Francisco), narratives read; filtered with `scripts/R1A_sgo_waymo_fatal.py`. Police and fault statements: NBC Bay Area, 20 Jan 2025 (San Francisco); azfamily.com, 14 Sep 2025 (Tempe); NBC DFW and B. Templeton, *Forbes*, 10 Aug 2026 (Dallas; "Waymo's 3rd 'involved' fatality").
- **Evidence tag:** [P] (the operator's reports to the regulator); [T] for the police statements.
- **Confidence:** high for the count of fatal reports; medium for fault, which rests on police statements relayed by the press.
- **Proposed edit:**
  - `old`:
    ```text
    Waymo's system was modified along the way (the recalls listed in §E1). Nor do they establish safety across all operating domains.
    ```
  - `new`:
    ```text
    Waymo's system was modified along the way (the recalls listed in §E1). Nor do they establish safety across all operating domains. No fatal crash in those miles has been attributed to the Waymo Driver: of the two fatal crashes Waymo reported to NHTSA before Jul 2026, one in San Francisco on 19 Jan 2025 began when a speeding car hit traffic queued behind a stopped, unoccupied Waymo, and in the other, in Tempe on 14 Sep 2025, a motorcyclist hit the back of a Waymo that was slowing to yield to a pedestrian and was then struck by a hit-and-run car [P, NHTSA Standing General Order reports]. A third, in Dallas on 7 Aug 2026, falls after these miles [P].
    ```
- **Appendix 2 entry:** NHTSA Standing General Order crash reports, ADS incidents (current file and 2021–2025 archive): https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADS.csv ; https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Incident_Reports_ADS.csv

## R1_partA_E2-E5-08

- **Question:** Which lidar does the Dual Radar dataset use, and what is its angular grid?
- **Answer:** A RoboSense RS-Ruby Lite (paper Table 2: 0.05 m range resolution, 0.2° azimuth and 0.2° elevation resolution, 230 m, 360° × 40°, 10 fps). RoboSense's manual gives 80 channels spread non-uniformly over −25° to +15° (vertical resolution "at least 0.1°"), azimuth resolution 0.2° at 10 Hz, and about 1.44 M points per second (single return). The grid is therefore $(360/0.2)\times80=1{,}800\times80=144{,}000$ angular cells per frame, matching $1.44\times10^6/10=144{,}000$ points per frame. The paper's Table 4 gives 74,386 / 116,096 / 133,538 lidar points per frame (minimum / average / maximum), so the average frame fills $116{,}096/144{,}000\approx81\%$ of the cells. (The 0.2° elevation figure in Table 2 cannot be a uniform grid: 40°/0.2° would be 200 lines, not 80.)
- **Source:** X. Zhang et al., "Dual Radar: A Multi-modal Dataset with Dual 4D Radar for Autonomous Driving", *Scientific Data* 12, 439 (2025), Tables 2 and 4; open-access full text via Europe PMC (PMC11907064), https://pmc.ncbi.nlm.nih.gov/articles/PMC11907064/ (full-text XML read; nature.com served a bot-check page, which was not bypassed). RoboSense, *RS-Ruby Lite Users' Manual*, Table 1 "Product Parameters", p. 3 (distributor-hosted copy), https://cdn.robotshop.com/media/u/utr/rb-utr-07/pdf/robosense-rs-rubylite-laser-rangefinder-230-m-user-guide.pdf (page rendered).
- **Evidence tag:** [P] (dataset paper and maker's manual); [E] for the cell count.
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
    That is of the same order as the ≈110,000–120,000 points per frame that the dataset's own lidar records, whose grid is not given here; directions with no return, such as the sky, also lower a lidar's point count [E].
    ```
  - `new`:
    ```text
    That is of the same order as the 116,096 points per frame, on average (74,386–133,538), that the dataset's own lidar records [P, Zhang et al., *Sci. Data* 2025, Table 4]. That lidar is a RoboSense RS-Ruby Lite, with 80 channels spread non-uniformly over a 40° vertical field (−25° to +15°) and 0.2° azimuth steps at the dataset's 10 Hz frame rate, so its own grid has $(360/0.2)\times80=1{,}800\times80=144{,}000$ angular cells per frame, matching its rated 1.44 M points per second at 10 Hz [P, RoboSense manual]. The average frame fills about 81% of those cells ($116{,}096/144{,}000\approx0.81$), because directions with no return, such as the sky, lower a lidar's point count [E].
    ```
- **Appendix 2 entry:**
  - Zhang et al., Dual Radar dataset, *Sci. Data* 12, 439 (2025), Tables 2 and 4 (open access): https://pmc.ncbi.nlm.nih.gov/articles/PMC11907064/
  - RoboSense RS-Ruby Lite users' manual, Table 1 (80 channels, 0.2° at 10 Hz, 1.44 M points/s): https://cdn.robotshop.com/media/u/utr/rb-utr-07/pdf/robosense-rs-rubylite-laser-rangefinder-230-m-user-guide.pdf

## R1_partA_E2-E5-09

- **Question:** What does Magna say about its fifth-generation thermal camera's size, and what pixel pitches do Raytron and Guide offer?
- **Answer:**
  - Magna: the sentence misreads the source. Magna's camera is "roughly the size of a golf ball"; sugar-cube size is a stated aim, not a property of the fifth generation, which was "targeted to debut late 2025". Magna's 2025 award post describes the system (thermal camera plus convolutional neural network) but gives no size.
  - Raytron: it released an 8 µm 1920×1080 vanadium-oxide uncooled detector in 2021 and "the world's first 6 μm 640 × 512 uncooled infrared detector" in 2024 (CIOE, Sep 2024); it also says its automotive products reached volume on BYD, Geely and other carmakers' models in 2025.
  - Guide: its 640×512 detector page lists 12 µm parts only, but its CIOE 2024 news presents the FLEXB608 camera core with 640×512 pixels at 8 µm.
  - So pixel pitch has reached 8 µm at both makers and 6 µm at Raytron. No source was found for "cheaper"; it is marked [U] in the edit.
- **Source:** Magna, R. Seoane, "Magna Tech Spotlight – Thermal Sensing System", blog, 23 May 2024, https://www.magna.com/stories/blog/2024/magna-tech-spotlight--thermal-sensing-system (read; already in Appendix 2). Magna, "Magna's Innovations Recognized at PACE Pilot Awards", 16 Apr 2025 (read). Raytron, "About us", https://en.raytrontek.com/about/about-us.htm (read; milestone list). Raytron, CIOE 2024 release on 6 µm sensors, PR Newswire, 27 Sep 2024, https://www.prnewswire.com/news-releases/thermal-imaging-manufacturer-raytron-brings-latest-6m-infrared-sensors-and-other-solutions-at-cioe-2024-302261058.html (read). Guide Infrared, "Guide Infrared Cutting-Edge Products Showcased at Shenzhen CIOE2024", https://www.guide-infrared.com/companynews/217.html (as indexed; the FLEXB608 figures were read in the search index, not on the page), and 640×512 detector page https://www.guide-infrared.com/uncooled-ir-detectors/163.html (read).
- **Evidence tag:** [P] (makers' own pages and releases); [U] for "cheaper".
- **Confidence:** high for Magna and Raytron; medium for Guide's 8 µm core (read from the index, not the page).
- **Proposed edit:**
  - `old`:
    ```text
    Magna's fifth generation (late 2025) shrinks the camera from golf-ball to sugar-cube size.
    ```
  - `new`:
    ```text
    Magna's thermal camera is roughly the size of a golf ball; its fifth generation was targeted to debut in late 2025, and Magna aims eventually at sugar-cube size [P, Magna, May 2024].
    ```
  - `old`:
    ```text
    Chinese makers such as Raytron and Guide (Wuhan Guide Infrared) offer cheaper sensors and optics, and pixel pitch has fallen to 8 µm.
    ```
  - `new`:
    ```text
    Chinese makers such as Raytron and Guide (Wuhan Guide Infrared) offer cheaper sensors and optics [U], and pixel pitch has fallen to 8 µm and below: Raytron released an 8 µm 1920×1080 detector in 2021 and a 6 µm 640×512 detector in 2024, and Guide shows an 8 µm 640×512 camera core [P].
    ```
- **Appendix 2 entry:**
  - Raytron, company milestones (8 µm 1920×1080 detector, 2021; 6 µm 640×512 detector, 2024): https://en.raytrontek.com/about/about-us.htm
  - Guide Infrared, CIOE 2024 products (FLEXB608, 640×512 at 8 µm): https://www.guide-infrared.com/companynews/217.html
  - (Magna's 2024 blog is already listed; its label can read "Magna thermal sensing (golf-ball size; fifth generation targeted for late 2025)".)

## R1_partA_E2-E5-10

### (a) §A3 "unlit rural roads and highways"

- **Question:** Where do US night pedestrian deaths occur: on unlit rural roads and highways?
- **Answer:** Only partly. In 2024, 7,080 pedestrians were killed; 76.0% died in the dark. By FARS light condition, 2,376 (33.6%) died in the dark on roads without lighting and 2,842 (40.1%) in the dark where there was lighting (2.3% dark, lighting unknown). Of the 2,376 unlit-road deaths, 69.9% were in urban areas and 29.2% in rural areas; by road class, 55.9% were on arterials other than freeways, 22.3% on interstates and freeways, and 21.2% on collectors and local roads. 2023 gives the same picture (35.2% unlit; of those 70.8% urban, 22.0% interstates and freeways). So unlit roads matter (a third of all pedestrian deaths, and the condition where pedestrian AEB showed no benefit, §A4), but most unlit-road deaths are on urban arterials, not on rural roads or highways.
- **Source:** NHTSA, *Traffic Safety Facts: Pedestrians, 2024 Data* (DOT HS 813 818), key findings and Figure 1 (76% dark, 84% urban, 7,080 killed), https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813818 (pages located, text read). FARS 2024 and 2023 national CSV files, https://static.nhtsa.gov/nhtsa/downloads/FARS/2024/National/FARS2024NationalCSV.zip (person.csv PER_TYP = 5, INJ_SEV = 4; accident.csv LGT_COND, RUR_URB, FUNC_SYS), tabulated with `scripts/R1A_fars_ped_light.py`; the script's 7,080 total matches NHTSA's.
- **Evidence tag:** [I] (government statistics); [E] for the tabulation.
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
    - Thermal is therefore valuable on unlit rural roads and highways, where many night pedestrian deaths occur.
    ```
  - `new`:
    ```text
    - Thermal is therefore most valuable where roads are unlit at night. In 2024, 2,376 of the 7,080 US pedestrian deaths (34%) happened in the dark on roads without lighting; most of these (70%) were in urban areas, mainly on arterial roads (56%), and fewer on rural roads (29%) or on interstates and freeways (22%) [I, NHTSA FARS 2024; E].
    ```
- **Appendix 2 entry:** NHTSA, Traffic Safety Facts: Pedestrians, 2024 Data (DOT HS 813 818): https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813818 ; FARS 2024 national data files: https://static.nhtsa.gov/nhtsa/downloads/FARS/2024/National/FARS2024NationalCSV.zip

### (b) §A3 Cadillac's reason for dropping the option

- **Question:** Did Cadillac cite limited usefulness in urban and suburban driving when it dropped Night Vision?
- **Answer:** Not in the source. The article reports that Cadillac dropped the passive (thermal) Night Vision option from the 2005 DeVille in September 2004 and would not offer it again; take-up fell from about 7,000 cars in model year 2000 (against 2,000 expected) to 600 in 2004, and 145 at \$2,250 on 2005 models. Cadillac's marketing director said only that any future system would be active (near-infrared). The reason given is the writer's, not Cadillac's: the systems' usefulness "has been questioned, and word-of-mouth evidently has not helped". It also notes that the thermal picture turns "a fuzzy gray" when it is warm outside (the crossover of §A3, item 5). No other source with an urban/suburban reason was found.
- **Source:** J. Meiners, "Cadillac drops Night Vision on DeVille, no new system planned", *Automotive News Europe*, 15 Nov 2004, republished by *Autoweek*, https://www.autoweek.com/news/a2091756/cadillac-drops-night-vision-deville-no-new-system-planned/ (full text read; already in Appendix 2).
- **Evidence tag:** [T].
- **Confidence:** high that the urban/suburban reason is not in this source.
- **Proposed edit:**
  - `old`:
    ```text
    Cadillac cited limited usefulness in urban and suburban driving when it dropped the option.
    ```
  - `new`:
    ```text
    When Cadillac dropped the option from the 2005 DeVille, take-up had fallen from about 7,000 cars in model year 2000 to 600 in 2004, and the trade press noted that the systems' usefulness had been questioned [T, *Automotive News Europe*, 15 Nov 2004].
    ```
- **Appendix 2 entry:** none (listed under "Additional verification sources").

### (c) §A3 option price

- **Question:** What did thermal night-vision options cost?
- **Answer:** In the US, Cadillac's passive Night Vision was a \$2,250 option on 2005 DeVilles, and BMW Night Vision (thermal, from 2005) cost "around US\$2500" in 2006. A fan blog citing Audi's configurator gives \$2,300 for the 2011 A8's Night Vision Assistant, but no Audi document was reached, so it is not used. The 2004 article adds that passive (thermal) systems cost about twice as much as active near-infrared ones, which supports "expensive" without isolating the optics. "\$2–3k" is therefore right; the sourced range is about \$2,250–2,500.
- **Source:** *Automotive News Europe*, 15 Nov 2004 (as in (b)). New Atlas, "BMW incorporates thermal imaging into newly available Night Vision driver assistance system", 23 Aug 2006, https://newatlas.com/bmw-incorporates-thermal-imaging-into-newly-available-night-vision-driver-assistance-system/6044/ (read).
- **Evidence tag:** [T].
- **Confidence:** medium — two trade-press prices, no maker price lists.
- **Proposed edit:**
  - `old`:
    ```text
    - The option cost \$2–3k, with expensive optics.
    ```
  - `new`:
    ```text
    - The option cost about \$2,250–2,500 in the US (Cadillac \$2,250 on the 2005 DeVille; BMW about \$2,500 in 2006), and passive thermal systems cost about twice as much as active near-infrared ones [T, *Automotive News Europe*, 15 Nov 2004; New Atlas, 23 Aug 2006].
    ```
- **Appendix 2 entry:** New Atlas, BMW Night Vision (about US\$2,500 option, 2006): https://newatlas.com/bmw-incorporates-thermal-imaging-into-newly-available-night-vision-driver-assistance-system/6044/

### (d) §A4 the Alliance's appeal and the abeyance

- **Question:** Which court holds the FMVSS 127 challenge, and is it still in abeyance?
- **Answer:** The Alliance for Automotive Innovation petitioned the US Court of Appeals for the D.C. Circuit for review on 17 Jan 2025 (*Alliance for Automotive Innovation v. DOT*, No. 25-1026). DOT moved on 24 Feb 2025, unopposed, to hold the case in abeyance while it reviewed the rule, and the court granted this four days later. DOT has since filed status reports ("awaiting decision of agency", Sep 2025 to Aug 2026). The Alliance moved to lift the abeyance on 7 May 2026; on 13 Aug 2026 a per curiam order (Judges Katsas, Rao and Childs) denied the motion and kept the case in abeyance pending further order, directing motions to govern future proceedings within 45 days; DOT filed one on 28 Sep 2026.
- **Source:** D.C. Circuit docket No. 25-1026, entries of 17 Jan 2025, 7 May 2026, 5 Aug 2026, 13 Aug 2026 and 28 Sep 2026, via the CourtListener RECAP archive, https://www.courtlistener.com/docket/69556046/alliance-for-automotive-innovation-v-dot/ (entry texts read through its search API). Nelson Mullins, "The Road Ahead for FMVSS 127", 22 Apr 2026 (already in Appendix 2), for the 24 and 28 Feb 2025 abeyance dates.
- **Evidence tag:** [P] (court record); [T] for the abeyance-grant date.
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
      - The Alliance (the Alliance for Automotive Innovation, the main US carmakers' trade group) appealed; the case is held in abeyance (paused by the court).
    ```
  - `new`:
    ```text
      - The Alliance (the Alliance for Automotive Innovation, the main US carmakers' trade group) petitioned the D.C. Circuit for review on 17 Jan 2025 (*Alliance for Automotive Innovation v. DOT*, No. 25-1026). At DOT's request the court has held the case in abeyance (paused it) since Feb 2025, and on 13 Aug 2026 it denied the Alliance's motion to lift the abeyance [P, D.C. Cir. docket; T, Nelson Mullins, Apr 2026].
    ```
- **Appendix 2 entry:** D.C. Circuit, *Alliance for Automotive Innovation v. DOT*, No. 25-1026 (FMVSS 127 petition; abeyance orders), RECAP docket: https://www.courtlistener.com/docket/69556046/alliance-for-automotive-innovation-v-dot/

### (e) §A4 Chinese germanium exports

- **Question:** Where do the Jan–Sep export figures come from?
- **Answer:** USGS: China's reported exports of germanium metal for the year through September fell to 7,520 kg in 2025 from 18,787 kg in 2024 and 36,656 kg in 2023; 2025 exports went mostly to Russia (28%), Belgium (26%), Germany (26%) and Japan (18%). The report's figures match.
- **Source:** USGS, *Mineral Commodity Summaries 2026*, "Germanium", Feb 2026, p. 2 (Events, Trends, and Issues), https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-germanium.pdf (both pages rendered and read).
- **Evidence tag:** [I].
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
    - Chinese Ge metal exports in Jan–Sep fell from 36,656 kg (2023) to 18,787 kg (2024) to 7,520 kg (2025).
    ```
  - `new`:
    ```text
    - Chinese Ge metal exports in Jan–Sep fell from 36,656 kg (2023) to 18,787 kg (2024) to 7,520 kg (2025) [I, USGS MCS 2026].
    ```
- **Appendix 2 entry:** none (listed as "USGS germanium 2026").

### (f) §A4 export permits for germanium

- **Question:** What export regime applies to Chinese germanium, and what supports "Chinese thermal makers buy optics domestically"?
- **Answer:** China introduced export licensing for germanium in August 2023 (MOFCOM Announcement No. 23 of 2023, effective 1 Aug 2023) and banned germanium exports to the United States in December 2024 (MOFCOM Announcement No. 46 of 2024). On 9 Nov 2025 China suspended the US ban (Article 2 of Announcement No. 46) until 27 Nov 2026; the licensing requirement itself was not suspended. No source was found on where Chinese thermal makers buy their optics; the defensible point is the logical one that a maker inside China needs no export licence for domestic supply.
- **Source:** USGS, *Mineral Commodity Summaries 2026*, "Germanium", p. 2 (licensing from Aug 2023; US ban Dec 2024), https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-germanium.pdf . Pillsbury, "China Suspends Export Controls on Certain Critical Minerals and Related Items", 13 Nov 2025 (already in Appendix 2), for the suspension dates.
- **Evidence tag:** [I] (USGS); [T] (law-firm note); [E] for the consequence.
- **Confidence:** high for the regime; the domestic-sourcing statement is reworded as an inference.
- **Proposed edit:**
  - `old`:
    ```text
    - Chinese thermal makers buy optics domestically; Western ones face permit friction, because China requires export permits for germanium.
    ```
  - `new`:
    ```text
    - China has required export licences for germanium since August 2023 and banned germanium exports to the United States in December 2024 [I, USGS MCS 2026]; the US ban is suspended from 9 Nov 2025 to 27 Nov 2026 [T, Pillsbury, Nov 2025]. A thermal-camera maker outside China that buys Chinese germanium or lenses therefore depends on licensed shipments, whereas a Chinese maker buying at home does not [E].
    ```
- **Appendix 2 entry:** none (USGS and Pillsbury are listed).

### (g) §A6.1 the low-beam "hotspot"

- **Question:** What supports "typically tens of thousands of cd" just below the cutoff?
- **Answer:** UN R149 sets the order of magnitude. For a class B passing beam (the usual European asymmetric low beam), points 50R (1.72° R, 0.86° D) and 75R (1.15° R, 0.57° D), just below the cutoff on the kerb side, need at least 10,100 cd (Table 8; R112 §6.2.4 has the same minimums). For the class C passing beam of an adaptive front-lighting system the maximum intensity must lie between 16,900 and 44,100 cd (Table 9, line 18), and a class D beam may reach 43,800 cd right of V–V (Table 8). The hotspot of a compliant low beam is therefore between about 10,000 and 44,000 cd, consistent with the report's 20,000 cd "typical" and 40,000 cd "strong" rows.
- **Source:** UN Regulation No 149, official text incorporating Supplement 3 (OJ L 347, 30.9.2021), Table 8 (p. L 347/199) and Table 9 (pp. L 347/203–204), https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:42021X1720 (pages rendered). UN Regulation No 112 (OJ L 250, 22.8.2014), §6.2.4 tables (pp. L 250/79–80), https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=uriserv:OJ.L_.2014.250.01.0067.01.ENG (pages rendered).
- **Evidence tag:** [P].
- **Confidence:** high for the regulatory bounds; "typically" is the report's reading of them.
- **Proposed edit:**
  - `old`:
    ```text
    - Just below the cutoff sits the "hotspot", the brightest part of the beam, typically tens of thousands of cd.
    ```
  - `new`:
    ```text
    - Just below the cutoff sits the "hotspot", the brightest part of the beam, typically tens of thousands of cd: UN R149 requires a class B passing beam to deliver at least 10,100 cd at points 50R and 75R, just below the cutoff on the kerb side (Table 8), and puts the maximum of an adaptive class C passing beam between 16,900 and 44,100 cd (Table 9) [P].
    ```
- **Appendix 2 entry:** UN R112, 2014 official text, §6.2.4 passing-beam table (B50L at most 350 cd; 50R and 75R at least 10,100 cd for class B): https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=uriserv:OJ.L_.2014.250.01.0067.01.ENG (R149 is listed).

### (h) §A6.3 ADB in Europe and China since about 2013

- **Question:** What supports "widespread since about 2013 (Audi Matrix LED, Mercedes Multibeam …)"?
- **Answer:** Audi announced on 1 Jul 2013 that its Matrix LED headlights would debut on the new A8, on the market at the end of 2013: each headlight has 25 high-beam LEDs, and the system blanks out the light that would fall on oncoming and preceding vehicles while keeping full high beam elsewhere. Mercedes-Benz first used Multibeam LED headlamps, with 24 individually controlled LEDs per lamp, on the new CLS in 2014. Matrix ADB was thus on sale in Europe from late 2013. "Widespread" and the Chinese makers were not checked; the edit keeps them as the report's own statement without a tag.
- **Source:** Audi AG press release "Leading the way in lighting technology: The new Audi Matrix LED headlights", 1 Jul 2013, republished by Automotive World, https://www.automotiveworld.com/news/leading-the-way-in-lighting-technology-the-new-audi-matrix-led-headlights/ (read). Autocar Professional, "Mercedes-Benz debuts multi-beam LED headlamp tech in new CLS", 17 Jun 2014, https://www.autocarpro.in/news-international/mercedes-benz-debuts-multi-beam-led-headlamp-tech-cls-5835 (read; the Daimler media page failed on a TLS error).
- **Evidence tag:** [P] (Audi release); [T] (Mercedes, via trade press).
- **Confidence:** high for the dates.
- **Proposed edit:**
  - `old`:
    ```text
      - **Europe and China:** widespread since about 2013 (Audi Matrix LED, Mercedes Multibeam and Digital Light, BMW Selective Beam, and many Chinese makers).
    ```
  - `new`:
    ```text
      - **Europe and China:** on sale since late 2013, when Audi's Matrix LED headlights, with 25 individually switched high-beam LEDs per lamp, arrived on the A8 [P, Audi, Jul 2013]; Mercedes followed with Multibeam LED on the CLS in 2014 [T], and Mercedes Digital Light, BMW Selective Beam and many Chinese makers' systems came later.
    ```
- **Appendix 2 entry:**
  - Audi, Matrix LED headlights (A8, end of 2013; 25 LEDs per lamp): https://www.automotiveworld.com/news/leading-the-way-in-lighting-technology-the-new-audi-matrix-led-headlights/
  - Autocar Professional, Mercedes Multibeam LED on the CLS (2014): https://www.autocarpro.in/news-international/mercedes-benz-debuts-multi-beam-led-headlamp-tech-cls-5835

## R1_partA_E2-E5-11

- **Question:** What do UN R112 and R149 themselves say about B50L?
- **Answer:** For conventional asymmetric passing beams, B50L (0.57° U, 3.43° L) has a maximum of 350 cd and no minimum: R112 §6.2.4 (class A and class B) and R149 Table 8 (classes A, B and D). The 50–350 cd range exists only for adaptive front-lighting systems: R149 Table 9 gives B50L 50–350 cd for class C and class V passing beams, with footnote 4 requiring each side's contribution to be at least 50 cd, and 50–625 cd for classes E and W (790 cd in class W bending mode). The *Scientific Reports* range, given for R123 (the AFS regulation that R149 absorbed), matches the class C row. The text should give both figures and cite the regulations.
- **Source:** UN R112, OJ L 250, 22.8.2014, §6.2.4, p. L 250/79 (rendered). UN R149, OJ L 347, 30.9.2021, Table 8, p. L 347/199, and Table 9 with notes, pp. L 347/203–204 (rendered). URLs as in item 10(g).
- **Evidence tag:** [P].
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
    Example: the ECE glare point B50L must stay within 50–350 cd [S, via *Scientific Reports* 2026, which gives it for ECE R123].
    ```
  - `new`:
    ```text
    Example: at the ECE glare point B50L a conventional class A or B passing beam may send at most 350 cd, with no minimum (UN R112 §6.2.4; UN R149 Table 8), and the class C passing beam of an adaptive front-lighting system (AFS) must stay within 50–350 cd (UN R149 Table 9) [P].
    ```
- **Appendix 2 entry:** UN R112 line as in item 10(g); R149 is listed. The *Scientific Reports* 2026 entry can stay or go.

## R1_partA_E2-E5-12

- **Question:** Which LightPath BlackDiamond grade is germanium-free?
- **Answer:** BD6, an arsenic selenide ($\mathrm{As_{40}Se_{60}}$) chalcogenide glass made in Orlando, Florida. BD-2 is 28% germanium, 12% antimony and 60% selenium (equivalent to AMTIR-3 and IG5). The reviewer is right. USGS separately confirms that chalcogenide glass has been used as a substitute for germanium metal in infrared applications, which supports the sentence's [I, USGS] tag.
- **Source:** LightPath Technologies, *Black Diamond BD6 Infrared Chalcogenide Glass* datasheet (2023), p. 1, https://refractiveindex.info/download/data/2023/50415_Lightpath_BD6_Datasheet.pdf ; LightPath, *BD-2 Glass Datasheet* (rev. 5/13), "Composition" table, https://refractiveindex.info/download/data/2013/BD-2.pdf (both are LightPath documents re-hosted by refractiveindex.info; pages rendered). USGS MCS 2026, "Germanium", p. 2, Substitutes.
- **Evidence tag:** [P] (maker's datasheets); [I] (USGS) for the substitute statement.
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
    - Chalcogenide glass (infrared-transmitting glass based on sulphur, selenium or tellurium; e.g. LightPath "BlackDiamond", Ge-free) is **one demonstrated substitute** in infrared optics, not a universal replacement for every thermal-camera lens design [I, USGS].
    ```
  - `new`:
    ```text
    - Chalcogenide glass (infrared-transmitting glass based on sulphur, selenium or tellurium) is **one demonstrated substitute** in infrared optics, not a universal replacement for every thermal-camera lens design [I, USGS]. Not every chalcogenide glass is germanium-free: LightPath's BlackDiamond BD6 is an arsenic selenide ($\mathrm{As_{40}Se_{60}}$) with no germanium, whereas its BD-2 grade is 28% germanium [P, LightPath datasheets].
    ```
- **Appendix 2 entry:** LightPath BlackDiamond BD6 datasheet ($\mathrm{As_{40}Se_{60}}$, germanium-free) and BD-2 datasheet (28% Ge): https://refractiveindex.info/download/data/2023/50415_Lightpath_BD6_Datasheet.pdf ; https://refractiveindex.info/download/data/2013/BD-2.pdf

## R1_partA_E2-E5-13

- **Question:** Does IIHS use 5 lux for low beams and 3 lux for high beams?
- **Answer:** No. IIHS uses 5 lux for both beams: the v3 protocol (Jul 2018, still current) says the average 5 lux distance is used for each low- and high-beam test, and its Table 4 gives a "Min. 5 lux distance for no demerits" for both (for example 100 m right edge straightaway on low beam, 150 m on high beam). The 3 lux figure is from the 2015 rationale, which calls 3 lux probably the most common single value for the visibility distance of low-contrast objects (citing CIE 188 and UMTRI reports) and explains that 5 lux was chosen because it can be measured more accurately in moving tests and correlates with the 3 lux distance. The report's sentence is right in substance; it can say "for low and high beams alike" and attribute the 3 lux statement precisely.
- **Source:** IIHS, *Headlight Test and Rating Protocol (Version III)*, Jul 2018, pp. 6 and 9 (Visibility Metric; Overall Assessment; Table 4), https://www.iihs.org/media/0e823704-32d1-4500-b095-15d064d824a7/ZJciYw/ (all 14 pages rendered). IIHS rationale (Aug 2015), p. 4, "Visibility Metric" (URL as in item 03). IIHS's protocol page lists Version III as current.
- **Evidence tag:** [P] (IIHS's own protocol).
- **Confidence:** high.
- **Proposed edit:**
  - `old`:
    ```text
    IIHS (the US Insurance Institute for Highway Safety) scores visibility as the distance at which 5 lux reaches a point 25 cm above the lane edge; 3 lux is a common criterion for low-contrast objects [P, IIHS].
    ```
  - `new`:
    ```text
    IIHS (the US Insurance Institute for Highway Safety) scores visibility, for low and high beams alike, as the distance at which 5 lux reaches a point 25 cm above the lane edge. Its rationale calls 3 lux probably the most common single criterion for the visibility of low-contrast objects, and chose 5 lux because it can be measured more accurately in moving tests and tracks the 3 lux distance [P, IIHS].
    ```
- **Appendix 2 entry:** none (protocol v3 and rationale are listed).

## R1_partA_E2-E5-14

- **Question:** Is 45.3 mph FMVSS 127's own conversion of 73 km/h?
- **Answer:** Yes. S5.2.1 (forward collision warning) and S5.2.2 (automatic emergency braking) for pedestrians both read "greater than 10 km/h (6.2 mph) and less than 73 km/h (45.3 mph)". The standard truncates 45.36 mph; 45.3 should stay.
- **Source:** 49 CFR 571.127, S5.2.1–S5.2.2, CFR 2025 edition (Title 49, vol. 6), p. 659, https://www.govinfo.gov/link/cfr/49/571?link-type=pdf&sectionnum=127&year=mostrecent (page rendered).
- **Evidence tag:** [P].
- **Confidence:** high.
- **Proposed edit:** optional, to show the lower bound and the clause numbers:
  - `old`:
    ```text
      - The pedestrian warning/braking system must operate below **73 km/h** (45.3 mph).
    ```
  - `new`:
    ```text
      - The pedestrian warning/braking system must operate at any forward speed above 10 km/h and below **73 km/h** (6.2 and 45.3 mph in the standard's own conversions; S5.2.1–S5.2.2).
    ```
- **Appendix 2 entry:** none (the codified FMVSS 127 text is listed).

## R1_partA_E2-E5-15

- **Question:** Which Wood et al. study gave each figure (40%/5% recognition, 59 → 94 m, 3.5×, 0 m)?
- **Answer:**
  - 5% and 0 m: Wood, Tyrrell & Carberry (2005), *Human Factors* 47(3):644–653. Ten young and ten older drivers on a closed road circuit; four clothing and two beam conditions, with and without glare. Drivers recognized only 5% of pedestrians in the hardest condition (low beams, black clothing, glare). Without glare, mean recognition distances ranged from 0.0 m (older drivers, low beam, black clothing) to 220 m (younger drivers, high beam, retroreflective "biomotion" markings).
  - The earlier conference version, Wood, Tyrrell & Carberry, "Pedestrian visibility at night: effects of pedestrian clothing, driver age, and headlamp beam setting" (TRB 82nd Annual Meeting, Washington DC, 2003; submitted 1 Aug 2002; TRB Pedestrian Committee outstanding-paper award), reports in its abstract that drivers identified 61% of pedestrians with glare and 76% without, only 5% of darkly clad pedestrians with glare, a mean of 76.5 m for the primary pedestrian (13 m for dark clothing, up to 50× more for biomotion), and older drivers at 58% of the younger drivers' distances.
  - 40% (dark clothing, low beam, no glare), 59 → 94 m and 3.5×: not found in either abstract. A search-engine summary attributes "59 m to 94 m" to this research group, but the passage could not be read. The full texts were not reachable: the 2005 paper is paywalled (SAGE), its QUT author copy and the TRB paper's ResearchGate and QUT copies returned HTTP 403/404, CORE's copies returned 403, and the archived TRB copy (web.archive.org snapshot of ltrc.lsu.edu, 13 Sep 2012) returned HTTP 429 on every attempt.
- **Source:** Wood JM, Tyrrell RA, Carberry TP, "Limitations in drivers' ability to recognize pedestrians at night", *Human Factors* 47(3):644–653 (2005), doi:10.1518/001872005774859980, PubMed abstract (PMID 16435703; read). TRB 2003 paper: abstract as indexed by Semantic Scholar (corpus ID 1549870) and the search engines; full text not read.
- **Evidence tag:** [I] for 5% and 0 m; [U] for 40%, 59 → 94 m and 3.5×.
- **Confidence:** high for the 5% and 0 m attributions; low for the others.
- **Searched:** PubMed/E-utilities (abstract), Semantic Scholar API, CORE API, Europe PMC (the 2014, 2017 and 2020 Wood papers are not open access), QUT ePrints (records 8301 and 29994), ResearchGate, academia.edu, TRID, the Wayback Machine, and web searches for "59 m" "94 m", "3.5 times", "just under 60 m … over 90 m" and the 40% figure.
- **Proposed edit:**
  - `old`:
    ```text
    (Wood et al., §A6.1) [I]
    ```
  - `new`:
    ```text
    (Wood, Tyrrell & Carberry 2005; §A6.1) [I]
    ```
  - `old`:
    ```text
    - Measurement agrees: in a closed-road study, dark-clad pedestrians under low beams were recognized on only about 40% of trials without glare and about 5% with glare (Wood et al.) [I].
    ```
  - `new`:
    ```text
    - Measurement agrees: in a closed-road study, drivers using low beams against oncoming glare recognized only 5% of black-clad pedestrians (Wood, Tyrrell & Carberry 2005) [I], against about 40% without glare [U].
    ```
  - `old`:
    ```text
    - **Measured:** switching from low to high beam raised mean pedestrian recognition distance from 59 m to 94 m, and by up to 3.5× for dark clothing (Wood/Tyrrell studies) [I].
    ```
  - `new`:
    ```text
    - **Measured:** switching from low to high beam raised mean pedestrian recognition distance from 59 m to 94 m, and by up to 3.5× for dark clothing (Wood, Tyrrell & Carberry 2003 and 2005) [U].
    ```
  - `old`:
    ```text
    - **Human factors.** Reaction time, attention and age: in Wood et al., older drivers under low beam failed to recognize black-clad pedestrians at all (mean recognition distance 0 m) [I].
    ```
  - `new`:
    ```text
    - **Human factors.** Reaction time, attention and age: in Wood, Tyrrell & Carberry (2005), older drivers under low beam failed to recognize black-clad pedestrians at all, even without glare (mean recognition distance 0.0 m) [I].
    ```
- **Appendix 2 entry:** relabel the second Wood line as "Wood, Tyrrell & Carberry 2003, 'Pedestrian visibility at night: effects of pedestrian clothing, driver age, and headlamp beam setting', TRB 82nd Annual Meeting (author copy): https://www.researchgate.net/publication/228414781_Pedestrian_visibility_at_night_Effects_of_pedestrian_clothing_driver_age_and_headlamp_beam_setting". Appendix 1, "Unknown:" list: "the 40% no-glare recognition rate, 59 → 94 m and 3.5× attributed to Wood, Tyrrell & Carberry (2003, 2005); full texts not checked".
