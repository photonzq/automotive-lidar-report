# Addendum: Primary Source Verification of Open Items in Automotive Perception Report
## Source checks, citations and findings (as of 27 September 2026)

---

### Method and Sources
This addendum addresses some of the open items from **Appendix 1** of [`automotive_perception_report_2026-09-27.md`](automotive_perception_report_2026-09-27.md). Each claim below was checked against **primary legal registers, official gazettes, USPTO patent texts and technical press reports**. The report was revised after this addendum; where the two differ, the report takes precedence, and the notes below say where.

---

## 1. Headlight Photometric Regulations: Statutory Texts

### 1.1 UN Regulation No. 48 (Vehicle Installation Standard)
* **Official Registry:** *Official Journal of the European Union*, **OJ L 347, 30.9.2021, pp. 1–117** (incorporating the 07 series of amendments) and **OJ L 265, 30.9.2016, pp. 125–242** (06 series). Also codified across UNECE contracting parties and UK retained law (*Regulation (EU) 2015/208 Annex XII*).
* **Text of Paragraph 6.1.9 ("Other requirements"):**
  > **"6.1.9.1. The aggregate maximum intensity of the main-beam headlamps which can be switched on simultaneously shall not exceed 430 000 cd, which corresponds to a reference value of 100."**
  >
  > **"6.1.9.2. This maximum intensity shall be obtained by adding together the individual reference marks which are indicated on the several headlamps. The reference mark '10' shall be given to each of the headlamps marked 'HR'."**

### 1.2 UN Regulation No. 149 (Component Approval Standard)
* **Official Registry:** *Official Journal of the European Union*, **OJ L 347, 30.9.2021, pp. 173–296** (Regulation (EU) 2021/1720, replacing former separate regulations UN R98, R112, and R123).
* **Paragraph 3.3.2.4 (Marking of Driving Beams), paraphrased:**
  > Each headlamp approved under this regulation for driving-beam emissions must bear a reference mark indicating its maximum luminous intensity:
  > $$\text{Reference Mark} \in \{7.5,\ 10,\ 12.5,\ 17.5,\ 20,\ 25,\ 27.5,\ 30,\ 37.5,\ 40,\ 45,\ 50\}$$
* **Table 13 / Part B Limits:**
  * For a standard automotive Class B driving beam, the maximum luminous intensity $I_{\max}$ per individual lamp assembly is capped at a reference mark of **50**.
  * By statutory definition, $1\ \text{reference unit} \equiv 4,300\ \text{cd}$:
    $$I_{\max,\text{lamp}} \le 50 \times 4,300\ \text{cd} = \mathbf{215,000\ \text{cd}}$$
  * A symmetrical pair of two reference-50 headlamps on a passenger vehicle yields:
    $$2 \times 215,000\ \text{cd} = \mathbf{430,000\ \text{cd}}\quad (\sum \text{Reference Marks} = 100)$$

### 1.3 Comparison with US FMVSS 108
* **US Regulation:** 49 CFR § 571.108 (Federal Motor Vehicle Safety Standard No. 108, Table XVIII).
* **Upper Beam Limit:** Capped at **75,000 cd per lamp at test point H-V** ($150,000\ \text{cd}$ total per vehicle).
* **Finding:** Global/European UN-compliant driving beams legally provide up to **$2.87\times$** the luminous intensity ($430,000\ \text{cd}$ vs $150,000\ \text{cd}$) of US FMVSS 108 high beams.

---

## 2. Laser Safety: IEC 60825-1:2014 Calculations

* **Standard Authority:** International Electrotechnical Commission, **IEC 60825-1:2014 (Edition 3.0)**, *Safety of laser products – Part 1: Equipment classification and requirements*.

### 2.1 Table 9: Wavelength Correction Factor $C_4$
* For the ocular hazard band $700\ \text{nm} \le \lambda \le 1050\ \text{nm}$, Table 9 specifies:
  $$C_4 = 10^{0.002(\lambda - 700)}$$
* **Exact Calculations:**
  * **905 nm:**
    $$C_4 = 10^{0.002(905 - 700)} = 10^{0.41} = \mathbf{2.57039578...}$$
  * **940 nm:**
    $$C_4 = 10^{0.002(940 - 700)} = 10^{0.48} = \mathbf{3.01995172...}$$
  * **Ratio:**
    $$\frac{C_4(940\ \text{nm})}{C_4(905\ \text{nm})} = \frac{3.019952}{2.570396} = \mathbf{1.174898} \implies \mathbf{+17.49\%}$$

### 2.2 Table 3 & Table 4: Class 1 Accessible Emission Limits (AEL)
* **Single-Pulse AEL ($t = 10^{-9}\ \text{s}$ to $1.8 \times 10^{-5}\ \text{s}$, measured through 7 mm pupil aperture):**
  $$\text{AEL}_{\text{single}} = 2 \times 10^{-7} C_4\ \text{J}$$
  * **905 nm:** $2 \times 10^{-7} \times 2.5704\ \text{J} = \mathbf{0.5141\ \mu\text{J}}$
  * **940 nm:** $2 \times 10^{-7} \times 3.0199\ \text{J} = \mathbf{0.6040\ \mu\text{J}}$
  * **1550 nm (Table 4, corneal thermal absorption regime):** $\text{AEL}_{\text{single}} = \mathbf{8.0\ \text{mJ}}$ ($8,000\ \mu\text{J}$).
  * *Note:* the 905/940 nm single-pulse expression $2 \times 10^{-7} C_4$ J is that of IEC 60825-1:2007 (Table 3), not a 2014 AEL; the report does not use this nanosecond-pulse comparison (report, Appendix 1).
* **Continuous / Long-Exposure Average Power Limit ($t > 10\ \text{s}$):**
  * At 905 nm (Table 3): $\text{AEL}_{\text{power}} = 3.9 \times 10^{-4} C_4\ \text{W} = \mathbf{1.002\ \text{mW}}$
  * At 1550 nm (Table 4): Flat limit of $\mathbf{10.0\ \text{mW}}$ ($9.98\times$ average power increase).
* **Usable Eye-Safe Photon Flux Ratio:**
  $$\frac{\Phi_{1550}}{\Phi_{905}} = \left(\frac{P_{1550}}{P_{905}}\right) \times \left(\frac{\lambda_{1550}}{\lambda_{905}}\right) = 9.98 \times \left(\frac{1550}{905}\right) = 9.98 \times 1.7127 = \mathbf{17.09\times}$$
  * **Note:** This agrees with Luminar’s Form 10-K figure ("17× eye-safe photon flux") for the long-exposure average-power limits of IEC 60825-1:2014 Tables 3 and 4; with the unrounded 9.6 mW limit the ratio is 16.4× (report, Part B).

---

## 3. Robotaxi Sensor Suites: Primary Pages

### 3.1 Waymo Sensor Hardware & Primary Patent Excerpts
* **Patent Document:** **US Patent No. 9,368,936 B1** (*Laser Diode Firing System*, Google LLC / Waymo; Inventors: Samuel William Lenius, Pierre-Yves Droz; Issued: June 14, 2016; Application 14/132,219).
  * **Source:** full text on Google Patents (`patents.google.com/patent/US9368936B1/en`).
  * **Text from the specification (col. 5, ll. 38–41; col. 17, ll. 44–46):**
    > *"In one example, the laser diode emits pulses of infrared light with a wavelength of about 905 nm. The transistor can be a Gallium nitride field effect transistor (FET), for example."*
    > 
    > *"In one example, the laser diode is configured to emit a pulse of light in the infrared spectrum with a wavelength of about 905 nanometers."*
* **Patent Application Note:** **US Patent Application No. 2026/0189798 A1** (*LiDAR-Guided Dynamic Camera Exposure Control*, Waymo LLC; Inventors: Colin Braley, Chase Salsbury, Po-Chao Huang).
  * **Caution:** This application appears in patent aggregators (Patentlyze, Justia inventor records) as a 2026 publication, but its Google Patents page could not be retrieved. Colin Braley's granted calibration patents (e.g., **US Patent No. 10,943,367 B1**, *Calibration of detection system to vehicle*) are available on Google Patents; citations to application '798 rest on aggregator abstracts, not on the full specification.
* **Waymo 6th-Generation Driver Sensor Count:**
  * **Primary Source:** Satish Jeyachandran (VP of Engineering, Waymo), official release: *Meet the 6th-generation Waymo Driver: Optimized for costs, designed to handle more weather, and coming to riders faster than before* (August 19, 2024).
  * **Sensor configuration:**
    * **13 cameras** (reduced from 29 on the 5th generation)
    * **4 lidars** (reduced from 5 on the 5th generation; in-house designs; the wavelength is not public, report Appendix 1)
    * **6 radars**
    * External Audio Receivers (EARs) array

### 3.2 Zoox Purpose-Built Robotaxi Sensor Suite
* **Source:** *Forbes* (Alan Ohnsman: *Amazon's Zoox Is On Track To Be Waymo's Biggest Robotaxi Rival*; *Waymo Finally Gets Robotaxi Competition As Amazon's Zoox Launches In Las Vegas*). Not confirmed by Zoox or Hesai filings: Zoox filed its sensor layout with NHTSA as confidential appendices, and the 2026 exemption grant lists sensor types only (report, Appendix 1).
* **Sensor counts as reported by *Forbes*:**
  * **8 lidars (Hesai supplies Zoox):** which models, and where the eight sit, are not established (report, Appendix 1). One description has **four corner sensor pods**, each with:
    1. One horizontally mounted surround lidar.
    2. One downward-pitched near-field lidar targeting curbs, tires, and road blind spots.
  * **18 Digital Cameras:** Overlapping 360° coverage.
  * **10 Radar Units:** High-frequency perimeter coverage.
  * **4 Long-Wave Infrared (LWIR) Thermal Cameras:** reportedly one per corner pod, used to detect pedestrians and animals in darkness, fog and steam.
  * **8 Microphones:** For acoustic emergency vehicle identification.

---

## 4. OEM L3 Programs and Commercial History

### 4.1 Ford Level 3 Strategy & Latitude AI
* **Source:** Doug Field (then Chief EV, Digital and Design Officer, Ford Motor Company), at CES 2026 and in a Reuters interview (Jan 2026).
* **Reported facts:**
  1. **Lidar included:** Field said that Ford's 2028 Level 3 "eyes-off" system **is planned to include lidar**; the supplier, count and configuration are undisclosed, and lidar does not appear in Ford's SEC filings for 2025–26 (report, Appendix 1).
  2. **Latitude AI:** Wholly owned subsidiary established in March 2023 with ~550 former engineers from Argo AI. Latitude AI is developing Ford’s proprietary automated driving stack.
  3. **Universal EV (UEV) Platform:** The L3 system will debut on Ford's low-cost Universal EV architecture, starting with a midsize electric pickup truck targeting a $30,000 base MSRP (planned: hands-free L2 in 2027, eyes-off L3 software in 2028).
  4. **Executive transition:** on 15 Apr 2026 Ford announced a reorganization and Doug Field's departure the following month (report, Appendix 2).

### 4.2 Cadillac DeVille Night Vision Commercial Sales
* **Source:** *Automotive News*, 15 Nov 2004 ("Cadillac drops night-vision option"), as reproduced by *Automotive News Europe* and *Autoweek*; not checked against GM's unit records (report, Appendix 1).
* **Hardware:** Raytheon Commercial Infrared uncooled ferroelectric barium strontium titanate (BST) bolometer (8–14 µm LWIR) paired with a windshield HUD.
* **Option Price:** $2,250 (MY2000).
* **Reported uptake:**
  * **MY 2000 (Launch):** **~7,000 units** (Cadillac had forecasted only ~2,000 units).
  * **MY 2001–2003:** volumes declined each year; no source gives the reasons.
  * **MY 2004:** Dropped to **~600 units**.
  * **MY 2005:** **145 units** ordered prior to cancellation.
* **Discontinuation:** GM terminated the program in September 2004; the feature was omitted from the 2006 Cadillac DTS platform.

---

## 5. Advanced Lidar Specifications & Teardowns

### 5.1 Huawei 896-Line Image-Grade Lidar
* **Primary Release:** Huawei Harmony Intelligent Mobility Alliance (HIMA) Spring Technical Conference, March 4, 2026; Securities Times (*STCN*).
* **Technical Architecture:**
  * **Name:** Huawei 896-Line "Dual-Optical-Path" Image-Grade Lidar (双光路图像级激光雷达).
  * **Structure:** "One Body, Dual Focal" (一体双焦) architecture in a single housing:
    1. *Wide-Angle Receiving Channel:* 120° Horizontal FOV for peripheral scene understanding.
    2. *Telephoto Receiving Channel:* 30° Horizontal FOV for long-range central cone object discrimination.
  * **Wavelength and detector:** not disclosed by Huawei; claims of 905 nm and two HiSilicon SPAD dies extrapolate from other Huawei products (report §C5 and Appendix 1).
  * **Huawei-stated performance:** detects a 14 cm obstacle at **120 meters** (Huawei: night detection range for a 10% target up from 42 m to **122 meters**, +190% against the 192-line model).
  * **Production Deployments:** Standard on Maextro S800 (尊界 S800), Aito M9 flagship, and Avatr 12/07 series.

### 5.2 Hesai Picasso 5th-Generation SPAD-SoC
* **Primary Release:** Hesai Technology Day, April 17, 2026.
* **Technical Architecture:**
  * Monolithic "6D" perception SPAD-SoC integrating on-chip native RGB-D color and spatial coordinates.
  * **Photon Detection Efficiency (PDE):** **$>40\%$** (wavelength not stated; foundry, node, pitch and stacking undisclosed, report §C5).
  * **Channel Density:** 2,160 detection channels per die.
  * **Multi-Die Packaging:** The 4,320-line Hesai ETX pairs **two Picasso chips side-by-side**, consistent with the reticle-limit analysis in §C6 ($26 \times 33\ \text{mm}$ exposure field); Hesai has not stated its reason.

### 5.3 Merchant Fleet Lidar Suppliers
* **May Mobility:** in 2023 **Aeva** announced May as an exclusive production customer for long-range lidar, and **Ouster** announced OS1 and Alpha Prime supply; neither has mentioned May since 2023, and May names no suppliers for its end-2025 Sienna (report, Appendix 1).
* **Plus (PlusAI):** **Aeva** (2021, long-range FMCW for autonomous heavy trucks), **Ouster** (2021, digital short-range lidar) and a 2023 **Luminar** arrangement (a *PlusDrive* exclusivity agreement plus a separate \$10 M investment). For its 2025–26 trucks the truck makers that integrate PlusAI's software choose the lidars, and none names a vendor (report, Appendix 1).
* **InnovizTwo:** 905 nm; the detector type is not disclosed. Its production datasheet qualifies the detector as a discrete optoelectronic part (AEC-Q101/Q102), separately from its ASIC, which points to a SiPM or APD array rather than a SPAD-SoC; onsemi's SiPM partnership concerns InnovizOne (report, Appendix 1).
* **Valeo SCALA 3:** a 2024 Valeo engineering presentation shows a **SPAD receiver** for the SCALA 3 platform, with 12.9 million points/s at 20 fps; the variants and production detector are not otherwise documented (report, Appendix 1).

---

## 6. Corporate SEC Filings & Commercial Restructurings

### 6.1 Luminar Technologies, Inc. (SEC Form 8-K, Item 2.01)
* **Official Registry:** SEC EDGAR CIK **0001758057**, Current Report on Form 8-K (Accession No. 0001140361-26-003737).
* **Filing Date / Transaction Closing:** February 2026; Bankruptcy Court Section 363 approval.
* **Disclosures and asset sales:**
  1. **Sale of Luminar Semiconductor, Inc. (LSI):**
     * *Purchaser:* **Quantum Computing Inc.** ("Quantum").
     * *Terms:* Completed **February 2, 2026** ("LSI Closing Date"). Luminar transferred 100% of issued and outstanding shares of LSI for **$110 million in cash consideration** (with $11 million held in a 12-month post-closing indemnity escrow).
     * *Covenants:* Luminar entered a 3-year non-compete with LSI and 3-year non-solicitation of LSI employees/customers, with mutual IP cross-licenses.
  2. **Sale of Core LiDAR Business Assets:**
     * *Purchaser:* **MicroVision, Inc.** ("MicroVision").
     * *Transaction:* Following a Section 363 bankruptcy auction concluded on January 26, 2026, MicroVision's $33 million cash bid was designated the highest and best bid (Quantum was named back-up bidder).
     * *Closing:* Transaction completed on **February 3, 2026** for **$33.0 million cash** plus assumed liabilities.
     * *Termination Fee:* On February 4, 2026, Luminar paid Quantum a $660,000 break-up fee and $500,000 expense reimbursement.

### 6.2 Hesai Group Audited Annual Report (SEC Form 20-F / 6-K)
* **Official Registry:** SEC EDGAR CIK **0001861737**, Form 20-F (Accession No. 0001104659-26-048025); the Hong Kong annual report was furnished the same day on Form 6-K (No. 0001104659-26-048075).
* **Audited FY2025 Financial & Operational Metrics:**
  * **Total LiDAR Shipments:** **1,620,406 units** (+222.9% YoY from 501,889), comprising:
    * *ADAS LiDARs:* **1,381,133 units** (85.23% of total volume)
    * *Robotics / Autonomous Mobility LiDARs:* **239,273 units** (14.77% of total volume)
  * **Net Revenues:** **RMB 3,027.6 million** ($432.9 million), up from RMB 2,077.2 million in FY2024.
  * **Gross Margin:** **41.8%** (Gross Profit: RMB 1,265.1 million / $180.9 million). Hesai attributes the slight decline from 42.6% in 2024 mainly to lower revenue from high-margin non-recurring engineering services and a higher share of ADAS products.
  * **Cash reserve:** RMB 7,511.0 million as of December 31, 2025, against RMB 3,204.8 million a year earlier (annual report); the balance sheet shows cash of RMB 1,663.5 million and short-term investments of RMB 3,091.9 million.
* **Geographic Revenue Disaggregation (20-F Note 18; Hong Kong annual report, p. 136):**
  * *Chinese Mainland:* **RMB 2,354.7 million (77.78%)** (up from RMB 1,542.8M in 2024).
  * *North America:* **RMB 451.7 million (14.92%)** (up +60.8% YoY from RMB 280.9M in 2024).
  * *Europe:* **RMB 140.0 million (4.62%)**.
  * *Other Regions:* **RMB 81.2 million (2.68%)**.
* **Supply-Chain & Supplier Concentration (Hong Kong annual report, Report of the Directors, p. 33):**
  * *Largest Single Supplier:* Accounted for **4.6%** of total purchases in FY2025.
  * *Top Five Suppliers Combined:* Accounted for **20.5%** of total purchases in FY2025.

### 6.3 Mobileye Global Inc. FMCW LiDAR Termination (SEC Form 10-Q)
* **Official Registry:** SEC EDGAR CIK **0001910139**, Form 10-Q for the Period Ended September 28, 2024 (Accession No. 0001410578-24-001734, Note 1).
* **Disclosure of programme termination (Note 1; the numbering of the three factors is added here):**
  > *"On September 9, 2024, the Company announced the winding down of the Lidar R&D Unit by the end of 2024 and the cessation of internal development of next-generation frequency modulated continuous wave (FMCW) lidars for use in autonomous and highly automated driving systems. The decision was based on a variety of factors, including:*
  > 1. *substantial progress on the Company's EyeQ™6-based computer vision perception,*
  > 2. *increased clarity on the performance of the Company's internally developed imaging radar, and*
  > 3. *continued better-than-expected cost reductions in third-party time-of-flight lidar units."*
* **Restructuring Terms:** Reduction in workforce of ~90 employees worldwide; $4.6 million in termination charges; termination of the Intel LiDAR Product Collaboration Agreement as of October 2, 2024 (Note 7).

---

## 7. Judicial Decisions & Federal Agency Investigations

### 7.1 D.C. Circuit Court of Appeals: *Hesai Technology Co. v. Department of Defense*
* **Official Citation:** U.S. Court of Appeals for the District of Columbia Circuit, **Case No. 25-5256** (Argued March 2026, Decided August 18, 2026; *Opinion by Circuit Judge Garcia*, joined by Circuit Judge Pillard and Senior Circuit Judge Edwards).
* **Appeal From:** U.S. District Court for the District of Columbia (No. 1:24-cv-01381, Friedman, J., reported at *792 F. Supp. 3d 22*).
* **Judicial Holding:**
  * **Reversed** the District Court's grant of summary judgment in favor of DoD on Fifth Amendment procedural due process grounds.
  * **Constitutional Protected Interest:** The Court ruled that Section 1260H listing carries direct, concrete statutory harms—including the mandatory procurement bar under NDAA Section 805 (Pub. L. 118-31 § 805, 10 U.S.C. note), DHS funding bans (Pub. L. 118-47 § 536), and Department of Energy restrictions—triggering constitutional due process protections.
  * **Procedural Defect:** The court held that DoD violated the Due Process Clause by not giving Hesai notice of the unclassified evidence on which the designation rested, or a meaningful opportunity to rebut it before designation.
  * **Not Harmless Error:** The Court held the lack of process was not harmless, rejecting DoD's arguments.
  * **Remedy (Remand Without Vacatur):** Consistent with D.C. Circuit national security precedents (*NCRI*, 251 F.3d 192, 209; *PMOI*, 613 F.3d 220, 230–31), the Court **remanded the matter to the Secretary of Defense without vacating the underlying listing**, leaving Hesai on the 1260H list while DoD conducts administrative remand proceedings.

### 7.2 NHTSA ODI Engineering Analysis EA26002 on Tesla Vision
* **Official Registry:** U.S. Department of Transportation, National Highway Traffic Safety Administration (NHTSA), Office of Defects Investigation (ODI), **Engineering Analysis EA26002**.
* **Opening Date:** March 18, 2026.
* **Scope & Subject Vehicle Population:** an estimated 3,203,754 Model S, X, 3 and Y vehicles and Cybertrucks (MY 2016–2026) equipped with Full Self-Driving (Supervised) / FSD hardware (HW3 and HW4); the analysis upgraded preliminary evaluation PE24031 (report §E12.2).
* **Investigative Trigger:** Multiple severe collisions occurring while FSD was actively engaged in reduced roadway visibility conditions (sun glare, fog, blowing airborne dust, and severe weather), including a fatal pedestrian collision in Rimrock, Arizona.
* **Information request EA26002-01 (2 Jul 2026):**
  * ODI's information request asks Tesla for internal engineering evaluations, safety-margin trade studies and simulation records from the removal of radar hardware.
  * It requests supporting material around an internal document titled "Radar Saves Us" (report §E12.2).

---

## 8. Federal Regulatory & Trade Mandates

### 8.1 FMVSS No. 127: PAEB Darkness Requirements
* **Statutory Codification:** 49 CFR Part 571.127 (Federal Motor Vehicle Safety Standard No. 127, *Automatic emergency braking systems for light vehicles*, Final Rule published at **89 FR 39686**, May 9, 2024, Docket No. NHTSA-2023-0012).
* **Mandatory Collision Avoidance Parameters (§ 571.127 S5.2):**
  * *Speed Range:* Operational from **10 km/h (6.2 mph) to 73 km/h (45.3 mph)**.
  * *Performance Requirement (§ 571.127 S5.2.3):* The vehicle must provide forward collision warning and automatically apply service brakes such that the subject vehicle **does not collide** with the pedestrian test mannequin (complete avoidance, not merely speed mitigation).
* **Darkness Test Conditions (§ 571.127 S6.1.3 & S6.3.12):**
  * *Ambient Illumination:* Surface illumination must be **$\le 0.2\text{ lux}$** (simulating unlit rural/suburban nighttime).
  * *Headlamp Modes (§ 571.127 S6.3.12(b)):* Darkness testing is conducted **separately with the vehicle's lower beams active** and with upper beams active.
  * *Significance for Perception:* The darkness tests run at up to 65 km/h (40.4 mph; Table 2 to S8.1.1). Passing them with **lower beams** under 0.2 lux requires pedestrian detection and trajectory forecasting at ranges that may exceed low-beam reach (about 40–60 m), which may favour active illumination (lidar) and thermal sensing.
* **Compliance Schedule (§ 571.127 S5(a)):**
  * Mandatory for all light vehicles manufactured on or after **September 1, 2029** (extended from original proposed 2027 date in the NPRM). Small-volume manufacturers receive until September 1, 2030. In Mar 2026 DOT said it was preparing a proposal to extend compliance by two years; the binding date remains 1 Sep 2029 unless a later rule changes it (report §A4).

### 8.2 US Commerce Department BIS Connected Vehicles Final Rule
* **Statutory Codification:** 15 CFR Part 791 (Bureau of Industry and Security, *Securing the Information and Communications Technology and Services Supply Chain: Connected Vehicles*, Final Rule published at **90 FR 5360**, January 16, 2025; Effective March 17, 2025).
* **Prohibition Phasing by Model Year:**
  1. *Covered Software (VCS or ADS software with a PRC/Russian nexus):* Prohibitions take effect for **Model Year (MY) 2027**.
  2. *VCS Hardware (Vehicle Connectivity Systems Hardware):* Prohibitions take effect for **Model Year (MY) 2030** (or January 1, 2029 for units without model year).
* **Explicit Administrative Finding on LiDAR Hardware (90 FR 5360):**
  * BIS excluded LiDAR from the definition of VCS hardware (90 FR 5391) and said it may consider LiDAR in a separate rulemaking or investigation.
  * BIS concluded (90 FR 5364): *"Based on a number of comments to the proposed rule, BIS recognizes a national security risk posed by LiDAR, but it concludes that focusing this regulation on VCS hardware and software systems, which ultimately enable the external communication of end-point sensors, is an appropriate scope at this time."*
  * Consequently, pure endpoint LiDAR hardware is not banned under 15 CFR Part 791 unless it integrates prohibited PRC automated driving software or connects directly to external communications hardware.

---

## 9. Critical Minerals & Upstream Chokepoints (USGS MCS 2026)

* **Standard Authority:** U.S. Geological Survey, *Mineral Commodity Summaries 2026* (Published February 2026, U.S. Department of the Interior).

### 9.1 Gallium (GaAs / GaN Optoelectronics & VCSELs)
* **Primary production:** Zero domestic primary recovery in the US since 1987; **US net import reliance: 100%**.
* **Global Output Share:** China accounted for **98.9%** (rounded to 99% in USGS text) of worldwide primary low-purity gallium production (839,000 kg out of 848,000 kg in 2024; estimated 900,000 kg in 2025).
* **Production Capacity:** China controls 1,600,000 kg of capacity out of 1,700,000 kg worldwide (**94.1%**).
* **Trade Actions & Pricing:** Following China's August 2023 export licensing and December 2024 total export ban to the US, the average unit import value surged 32% in 2025 to **$580/kg** (from $439/kg in 2024 and $365/kg in 2023). China instituted a temporary 1-year suspension of the US ban in November 2025.

### 9.2 Germanium (LWIR Optics, Thermal Lenses & Multi-Junction Diodes)
* **Supply Shock & Price Explosion:**
  * China banned all germanium exports to the US in December 2024.
  * China's metal exports through September 2025 collapsed to 7,520 kg (down from 18,787 kg and 36,656 kg in the same periods of 2024 and 2023).
  * Direct US imports of germanium metal plunged **67%** in 2025 to 7,000 kg.
  * **Price Trajectory:** European 99.999% germanium metal price skyrocketed from $1,392/kg (2023) to $1,991/kg (2024) to an average of **$4,100/kg in 2025**, reaching **$5,380/kg** in October 2025 (from $3,150/kg in January).
  * *Optics Substitution:* USGS notes that **chalcogenide glass** has been used as a substitute for germanium metal in infrared applications.

### 9.3 Indium (InP Lasers, Photodetectors & Coherent Optical Engines)
* **Refinery Production Concentration:** Global refinery production of 1,100 metric tons in 2025e; **US net import reliance: 100%**.
* **Global Output Share:** China produced **760 metric tons (69.1% / ~70%)**, followed by Republic of Korea (180 t / 16.4%), Japan (65 t / 5.9%), and Canada (40 t / 3.6%).
* **Trade Restrictions:** In February 2025, China's Ministry of Commerce subjected indium to new export restrictions; Asian Metal reports that exports of unwrought indium plunged 72% YoY from September 2024 to September 2025.

---

## 10. Sensor Datasheets & Silicon Architecture

### 10.1 Seyond (Innovusion) Architecture Matrix
* **Source:** Seyond datasheets and specifications (V2.2.0, Dec 2024 / 2025).
* **Parameters:**
  * **Falcon K2 (Long-Range Roof Lidar):**
    * *Wavelength:* **1550 nm** fiber laser (Class 1, IEC 60825-1:2014).
    * *Range:* 500 m maximum; **250 m at 10% Lambertian reflectivity** (under 100 klx sunlight, POD > 90%).
    * *Field of View:* $120^\circ \times 25^\circ$ non-ROI; $120^\circ \times 9.6^\circ$ dynamic ROI.
    * *Angular Resolution:* $0.1^\circ \times 0.15^\circ$ (outer) / $0.1^\circ \times 0.1^\circ$ (central ROI).
    * *Points per Second:* 1,370,000 pts/s (single return) / 2,740,000 pts/s (dual return).
    * *Power / Form Factor:* 20 W; $58.9 \times 228 \times 149.6\text{ mm}$; 1.7 kg.
  * **Robin E / Robin E1X (Behind-Windshield / Cabin Lidar):**
    * *Wavelength:* **940 nm** diode laser (Class 1, IEC 60825-1).
    * *Range:* 1 m to 250 m (**200 m at 10% reflectivity**).
    * *Resolution:* $0.1^\circ \times 0.1^\circ$.
    * *Power Consumption:* **6 W** (convection cooling, behind-windshield capable).
    * *Form Factor:* $30 \times 106 \times 101\text{ mm}$.
  * **Robin W (Perimeter / Blind-Spot Lidar):**
    * *Wavelength:* **905 nm** diode laser (Class 1, IEC 60825-1).
    * *Range:* 0.1 m to 150 m (**70 m at 10% reflectivity**).
    * *Field of View:* $120^\circ \times 70^\circ$.
    * *Resolution:* Up to $0.15^\circ \times 0.36^\circ$.

### 10.2 Sony Semiconductor SPAD-SoC Evolution (IMX459 vs IMX479)
* **Sources:** Sony Semiconductor Solutions Corporation releases (Sept 6, 2021 & June 10, 2025).
* **Technical Comparison:**

| Specification Parameter | Sony IMX459 (Generation 1, 2021/22) | Sony IMX479 (Generation 2, 2025) |
|---|---|---|
| **Optical Format / Image Size** | 1/2.9-type ($6.25\text{ mm}$ diagonal) | **1-type ($15.8\text{ mm}$ diagonal)** |
| **Die Dimensions** | $15.65 \times 15.35\text{ mm}$ BGA | **$12.2\text{ mm}\ (\text{H}) \times 20.0\text{ mm}\ (\text{V})$ chip size** |
| **Effective SPAD Pixels** | $597 \times 168$ (~100,000 pixels) | **$105 \times 1,568$ (~164,000 pixels)** |
| **Dedicated Vertical dToF Pixels** | Pixel-summed block | **520 vertical dToF line channels** |
| **Recommended Wavelength** | **905 nm** | **940 nm** |
| **Photon Detection Efficiency (PDE)** | **24%** (at 905 nm) | **37%** (at 940 nm) |
| **Distance Precision at 300 m** | 15–30 cm | **Minimum 5 cm equivalent** |
| **Fabrication Architecture** | 3D stacked BSI SPAD + Cu-Cu logic | 3D stacked BSI SPAD + Cu-Cu logic |

* **Architectural Takeaway:** Sony’s migration from IMX459 (905 nm, 24% PDE) to IMX479 (940 nm, 37% PDE, 520 vertical channels) is consistent with a shift toward **940 nm SPAD arrays**, which have lower solar background, a +17.5% higher IEC Class 1 limit and high silicon PDE.

---

## 11. Alternative Readings: Evidence and Physics

This section sets out six alternative readings of points in [`automotive_perception_report_2026-09-27.md`](automotive_perception_report_2026-09-27.md), with the literature, physics and regulations behind each. Where a reading describes the report, the report's own wording governs.

---

### 11.1 FMCW LiDAR: Instantaneous Doppler Kinematics in Class 8 Autonomous Trucking
* **Point examined:** The report (§C7, §C10, §F6) projects a small passenger-car role for FMCW (0.1%–0.5% of units by 2030), citing Mobileye's wind-down and falling dToF prices; §F6 rates FMCW "decisive" for heavy trucks.
* **Kinematic & Physics Counter-Evidence:**
  * **Radial Velocity Measurement:** Frequency-modulated continuous-wave (FMCW) coherent detection extracts the radial velocity $v_r$ of every returned point **instantaneously within a single chirp** ($\tau \approx 5\text{ to }20\ \mu\text{s}$) via the Doppler frequency shift:
    $$v_r = \frac{\Delta f_{\text{Doppler}} \cdot \lambda}{2}$$
  * **The dToF Tracking Latency Penalty:** Direct time-of-flight (dToF) returns only range ($r$). To establish target velocity, a dToF perception stack must cluster point returns across multiple consecutive frames:
    $$v_{\text{dToF}} = \frac{r(t_k) - r(t_{k-1})}{\Delta t_{\text{frame}}}$$
    At standard 10–20 Hz frame rates ($\Delta t_{\text{frame}} = 50–100\text{ ms}$), achieving acceptable Kalman filter false-alarm rejection requires observing an obstacle across **2 to 4 frames (100–300 ms latency)** before initiating safety-critical braking.
  * **Heavy Trucking Braking Arithmetic:**
    * Operating parameters for a loaded Class 8 combination tractor-trailer: Gross Vehicle Weight Rating (GVWR) of **80,000 lbs (36,287 kg)** cruising at **70 mph (31.3 m/s)** on a highway.
    * Maximum pneumatic brake deceleration: $a \approx 0.55g = 5.39\ \text{m/s}^2$.
    * Pure braking distance: $d_{\text{brake}} = \frac{v^2}{2a} = \frac{(31.3)^2}{2 \times 5.39} \approx \mathbf{90.9\text{ meters}}$.
    * Air-brake pneumatic lag + mechanical latch time: $\approx 0.50\text{ s}$ ($\implies 15.65\text{ m}$).
    * **Latency Savings:** An FMCW sensor can remove most of the assumed 200 ms multi-frame velocity-estimation delay:
      $$\Delta d_{\text{stopping}} = v \times \Delta t_{\text{latency}} = 31.3\ \text{m/s} \times 0.20\ \text{s} = \mathbf{6.26\text{ meters}}$$
    * A 6.26 m reduction is about 6–7% of the stopping distance computed above.
* **Commercial milestones (May 2026 and Dec 2025):**
  1. *Daimler Truck North America & Torc Robotics:* On **May 6, 2026** Aeva announced that it had delivered initial **Atlas 4D LiDAR C-samples** to Daimler Truck North America and Torc Robotics for Level 4 Freightliner Cascadia trucks, as their exclusive long-range lidar supplier; on its earnings call the same day it called the sensor production-intent and gave a 2027 target launch.
  2. *Top European Passenger OEM:* On **December 3, 2025** Aeva announced that it had become the exclusive Tier-1 lidar supplier for a "Global Top 10" OEM's vehicle platform outside China (Atlas Ultra 4D LiDAR, Level 3, start of production targeted in 2028); a July 2025 release names **LG Innotek** as manufacturer of the Atlas Ultra. Aeva's 10-K (Mar 2026) says no definitive volume production agreement had been signed (report, Appendix 1).
* **Finding:** FMCW is priced out of sub-$30,000 passenger cars today, but its per-point velocity may still justify the cost in autonomous heavy freight and premium L3 eyes-off systems.

---

### 11.2 Silicon Bandgap Physics ($E_g = 1.124\text{ eV}$) and 1550 nm Foundry Incompatibility
* **Point examined:** §G3 of the report examines the statement *"Luminar failed on program economics, not optics"*, and Part B concludes that sensor performance was not the main factor.
* **Solid-State Physics Counter-Evidence:**
  * **Silicon Absorption Cutoff:** The bandgap of crystalline silicon at room temperature ($T = 300\text{ K}$) is $E_g \approx 1.124\text{ eV}$. The fundamental long-wavelength absorption cutoff $\lambda_c$ is determined by:
    $$\lambda_c = \frac{h c}{E_g} = \frac{1.2398\ \mu\text{m}\cdot\text{eV}}{1.124\ \text{eV}} = \mathbf{1.103\ \mu\text{m}} = \mathbf{1,103\text{ nm}}$$
  * **Optical Transparency at 1550 nm:** Photons at $\lambda = 1550\text{ nm}$ possess an energy of $h\nu = 0.800\text{ eV} < E_g$. Silicon is transparent at 1550 nm; photons pass through the lattice without exciting interband electron-hole pairs (extinction coefficient $k \approx 0$).
  * **Detector material:** A 1550 nm receiver cannot use a silicon absorber. It needs III-V compound semiconductor alloys (or Ge-on-Si), primarily Indium Gallium Arsenide ($\text{In}_{0.53}\text{Ga}_{0.47}\text{As}$) lattice-matched to Indium Phosphide ($\text{InP}$) substrates ($E_g \approx 0.74\text{ eV}$, $\lambda_c \approx 1680\text{ nm}$).
  * **Wafer Scale Disparity:**
    * Commercial InP wafers are standard at **3-inch (76 mm)** and **4-inch (100 mm)** diameters (slowly piloting 6-inch / 150 mm).
    * Automotive silicon CMOS foundries (TSMC, UMC, Sony, SMIC) fabricate on **12-inch (300 mm)** wafers.
    * The surface area ratio per wafer is:
      $$\frac{A_{300\text{mm}}}{A_{100\text{mm}}} = \left(\frac{300}{100}\right)^2 = \mathbf{9.0\times}$$
    * A 300 mm silicon line yields nearly an order of magnitude more dies per wafer, draws on a much larger, already amortised manufacturing base, and exhibits defect densities ($D_0$) two orders of magnitude lower than InP/InGaAs.
  * **Discrete Optical Assembly:** 1550 nm pulsed sources commonly use Erbium-Doped Fiber Amplifiers (EDFAs) pumped by 980 nm laser diodes, fiber coils, and fused splitters, which require active mechanical fiber alignment. By contrast, 905/940 nm systems integrate planar surface-emitting VCSELs directly bonded to silicon SPAD-SoCs.
* **Finding:** Optics and economics are coupled: choosing 1550 nm ruled out silicon CMOS detectors and raised Luminar’s costs relative to 905/940 nm designs.

---

### 11.3 Sensor Fusion Epistemic Conflict (Phantom Braking) vs. Dynamic Ego-Motion Baselines
* **Point examined:** §E1–§E8 argue from triangulation geometry that camera-only depth error grows as $Z^2$, and model fused failure probability as a product ($P_{\text{fail}} = P_{\text{cam}} \times P_{\text{lidar}}$) for independent channels (§E5).
* **Information Theory & Automotive Safety Counter-Evidence:**
  * **Dynamic Ego-Motion Baseline Expansion:**
    * Classical binocular stereo depth error is given by:
      $$\delta Z = \frac{Z^2}{b \cdot f} \delta d$$
      where $b$ is the physical baseline between cameras (typically $b \approx 0.25\text{ m}$ in a windshield housing), $f$ is focal length, and $\delta d$ is pixel disparity error. At $Z = 150\text{ m}$, static disparity is fractions of a subpixel.
    * However, modern end-to-end vision models (e.g. Tesla FSD V12/V13, Wayve) do not operate as static stereo pairs; they ingest continuous multi-frame temporal video buffers.
    * A vehicle moving at highway speed ($v = 25\text{ m/s}$ / 56 mph) spans an ego-motion distance over a 500 ms window of:
      $$b_{\text{dynamic}} = v \cdot \Delta t = 25\text{ m/s} \times 0.50\text{ s} = \mathbf{12.5\text{ meters}}$$
    * This represents a **$50\times$ baseline expansion** over the physical windshield camera mount ($12.5\text{ m}$ vs $0.25\text{ m}$), converting monocular temporal tracking into high-parallax structure-from-motion and reducing the $Z^2$ depth error for objects away from the direction of travel.
  * **The Epistemic Dilemma of Multi-Sensor Fusion:**
    * Classical independent probability multiplication ($P(A \cap B) = P(A)P(B)$) holds only for independent false negatives, but does not address **false positive generation (Type I errors)**.
    * Physical radar and lidar sensors frequently return spurious high-amplitude reflections from non-hazardous road infrastructure (overhead steel gantries, bridge expansion joints, manhole covers, metallic trash bags, steam plumes).
    * When a high-resolution camera perceives an unobstructed road but a radar/lidar reports an obstacle, the fusion layer faces a trade-off:
      1. *Prioritize Lidar/Radar:* Trigger emergency braking. This reduces false negatives but can cause **phantom braking**, a hazard for following vehicles on highways.
      2. *Prioritize Camera / Gate the Lidar/Radar:* Suppress the alert. This avoids phantom braking but gives up the sensor's safety redundancy.
    * **Regulatory Evidence:** NHTSA opened **Preliminary Evaluation PE22-002** on 16 Feb 2022 into unexpected brake activation on MY2021–2022 Tesla Model 3 and Model Y (416,000 vehicles at opening, 695,000 at closing). It closed the evaluation on 29 Jun 2026 without a recall and made no causal finding; its closing summary notes that some complaint and field data aligned with Tesla's mid-2021 transition from radar-vision fusion to vision-only. (EA24003 is an unrelated Dodge Journey investigation.)
* **Finding:** Multimodal sensor fusion is not automatically safer: disagreements between sensors must be arbitrated, and poor arbitration can cause false braking.

---

### 11.4 Semiconductor Defect Yield vs. Lithography Reticle Limits
* **Point examined:** §C6 and §C8 cite the lithography exposure field ($26 \times 33\text{ mm} = 858\text{ mm}^2$) as a physical limit that forces multi-die packaging (such as Hesai's ETX pairing two Picasso chips).
* **Semiconductor Manufacturing Yield Analysis:**
  * **Yield Modeling:** Integrated circuit yield is governed by Poisson’s model $Y = e^{-A \cdot D_0}$ or Murphy’s model:
    $$Y = \left(\frac{1 - e^{-A \cdot D_0}}{A \cdot D_0}\right)^2$$
    where $A$ is active die area and $D_0$ is defect density per unit area.
  * **Automotive 3D BSI SPAD Process Metrics:**
    * In a specialized 3D-stacked BSI CMOS process incorporating deep trench isolation (DTI) and high-voltage SPAD junctions, defect densities of $D_0 \approx 0.06\text{ to }0.10\text{ defects/cm}^2$ are assumed here.
    * For **Sony IMX479** ($A = 12.2 \times 20.0\text{ mm} = 2.44\text{ cm}^2$):
      $$A \cdot D_0 = 2.44 \times 0.08 = 0.1952 \implies Y_{\text{Murphy}} \approx \mathbf{82.6\%}$$
    * For a full-reticle monolithic die ($A = 26 \times 33\text{ mm} = 8.58\text{ cm}^2$):
      $$A \cdot D_0 = 8.58 \times 0.08 = 0.6864 \implies Y_{\text{Murphy}} \approx \mathbf{50.7\%}$$
  * **Automotive AEC-Q100 Grade 2 Reliability:** For automotive safety applications, dies must satisfy zero-defect gate oxide integrity and withstand severe thermal cycling ($-40^\circ\text{C}$ to $+105^\circ\text{C}$). Across an $858\text{ mm}^2$ die, thermo-mechanical coefficient of thermal expansion (CTE) mismatches and Cu-Cu wafer bonding micro-voids can raise field failure rates.
  * **Optical Packaging Bounds:** In a roof-mounted automotive sensor blister, the physical focal length $f$ and entrance pupil diameter $D_{\text{lens}}$ are constrained by package height (<45 mm). Off-axis aberrations (coma, astigmatism, Petzval field curvature) scale rapidly with image circle diameter:
    $$\Delta_{\text{aberration}} \propto \left(\frac{y}{f}\right)^2$$
    where $y$ is the semi-diagonal image height.
* **Finding:** Hesai’s division of the Picasso architecture into dual 2,160-line dies for the ETX, and Sony’s sizing of the IMX479 at $244\text{ mm}^2$, may reflect **wafer yield, thermal stress and optical aberration limits** as well as the exposure-field limit; neither company has stated its reasons.

---

### 11.5 NHTSA FMVSS 127 Low-Beam Stopping Distance vs. Thermal Night Vision
* **Point examined:** §A3 and §F1 project that thermal night vision stays below 0.5% of global production unless night-AEB testing forces it, and that ADB narrows but does not close the night gap (§A6.5).
* **Statutory Analysis & Stopping Distance Formulation:**
  * **Codified Mandate:** 49 CFR § 571.127 (FMVSS No. 127, 89 FR 39686):
    * *Section S5.2:* Mandates **complete collision avoidance** (zero impact with pedestrian test mannequin) in the S8 tests; the system must operate up to **73 km/h (45.3 mph)**, and the darkness tests run at up to 65 km/h (40.4 mph).
    * *Section S6.3.12(b):* Darkness testing is conducted **with the vehicle's lower beams active, and separately with its upper beams active**.
    * *ADB:* the regulatory text does not mention adaptive driving beams; the preamble (89 FR 39751) declines commenters' requests to test with ADB active, since NHTSA does not require ADB.
  * **Stopping Distance Mechanics at 45.3 mph ($v = 20.11\text{ m/s}$), the upper operating speed of S5.2.2:**
    * *Braking Deceleration on Dry Asphalt ($a = 0.70g = 6.867\text{ m/s}^2$):*
      $$d_{\text{brake}} = \frac{v^2}{2a} = \frac{(20.11)^2}{2 \times 6.867} = \mathbf{29.45\text{ meters}}$$
    * *Total System Latency ($\tau_{\text{system}}$):* Perception confirmation window ($300\text{ ms}$) + path verification & false-positive gating ($300\text{ ms}$) + electro-hydraulic brake-by-wire pressure build-up ($150\text{ ms}$) = **$750\text{ ms} = 0.75\text{ s}$**.
    * *Latency Distance Traveled:*
      $$d_{\text{latency}} = v \cdot \tau_{\text{system}} = 20.11\text{ m/s} \times 0.75\text{ s} = \mathbf{15.08\text{ meters}}$$
    * *Minimum Required Detection Range (Dry Road):*
      $$d_{\text{total,dry}} = d_{\text{brake}} + d_{\text{latency}} = 29.45 + 15.08 = \mathbf{44.53\text{ meters}}$$
    * *Minimum Required Detection Range (Wet Asphalt, $a = 0.50g = 4.905\text{ m/s}^2$):*
      $$d_{\text{total,wet}} = \frac{(20.11)^2}{2 \times 4.905} + (20.11 \times 1.0\text{ s}) = 41.23 + 20.11 = \mathbf{61.34\text{ meters}}$$
    * *Note:* the darkness tests run at up to 65 km/h ($v = 18.06$ m/s); with the same assumptions this gives about 37 m (dry) and 51 m (wet).
  * **The Photometric Photodiode Barrier:**
    * Under UN R48 / FMVSS 108 low-beam cutoff requirements, illuminance on a pedestrian at 55–65 meters wearing low-reflectance clothing ($\rho \approx 0.05$) drops to **$<0.5\text{ lux}$**.
    * Reflected target photon flux into a 5 mm camera aperture falls below the shot-noise floor of automotive CMOS image sensors, preventing the high-confidence ($>99.9\%$) classification required to initiate maximum emergency braking.
  * **Passive LWIR Advantage:**
    * Uncooled microbolometers operating in the Long-Wave Infrared band (**8–14 µm**) detect blackbody thermal photon emission from human skin/clothing ($T \approx 310\text{ K}$) at **150 to 200+ meters**, requiring **zero lux of external illumination**.
* **Finding:** FMVSS 127’s low-beam darkness tests may create a perception bottleneck for visible-light cameras at the test speeds (up to 65 km/h). If camera-only platforms fail the low-beam compliance threshold before the **September 1, 2029 deadline**, thermal cameras (or active lidar) could become necessary for compliance.

---

### 11.6 Domestic Chinese Component Substitution: Automotive AEC-Q101 GaN and AEC-Q102 VCSELs
* **Point examined:** §C5 and §D1 state that Chinese lidar makers still depend on Western suppliers for some laser diodes (ams OSRAM) and GaN FET drivers (EPC).
* **Component qualification evidence:**
  1. **Automotive Multi-Junction VCSELs (Everbright Photonics / 长光华芯):**
     * On **March 31, 2023** Suzhou Everbright Photonics announced that its automotive lidar chip, a VCSEL-array light source, passed **AEC-Q102** qualification (as reported by DRAMX/TrendForce; the company's original post was not found).
     * Operates a 6-inch epitaxy and wafer-fab IDM (Integrated Device Manufacturer) line. A multi-junction design, 905/940 nm wavelengths, a $130^\circ\text{C}$ junction rating and 6,000 V ESD protection could not be confirmed.
  2. **Automotive GaN Laser Driver FETs (Innoscience / 英诺赛科):**
     * Innoscience reports **AEC-Q101** qualification for its 100 V gallium nitride HEMTs **INN100W135A-Q** and **INN100W800A-Q** (release of 30 Oct 2024), which it describes as optimized for lidar, DC-DC converters and Class D audio.
     * Its single-channel lidar evaluation board reaches a **1.5 ns pulse width** at a **74.93 A** peak current (a board demonstration, not a datasheet specification).
     * Operates 8-inch GaN-on-silicon wafer fabs in Zhuhai and Suzhou.
  3. **Foundry Image Sensor / SPAD Lines:**
     * **SMIC (Semiconductor Manufacturing International Corporation)** and **Silan Micro (士兰微)** are possible domestic foundries for BSI CIS (Back-Illuminated CMOS Image Sensor) and SPAD processes; none is publicly named for an in-house lidar SPAD-SoC (report, Appendix 1).
* **Finding:** Chinese LiDAR Tier-1s (Hesai, RoboSense, Seyond) have domestic sources for some discrete GaN FETs and emitter diodes. The remaining dependence on Western suppliers appears to lie in **EDA design software (Synopsys, Cadence)** and advanced precision optical test equipment.

---

## 12. Summary of Items and Their Status

| # | Item | Source | Value or finding | Status |
|---|---|---|---|:---:|
| 1 | **UN R48 Driving Beam Cap** | *Official Journal of the EU*, OJ L 347, 30.9.2021, p. 33 (§6.1.9.1) | **430,000 cd** ($\sum \text{Reference Marks} \le 100$) | Source cited |
| 2 | **UN R149 Lamp Limit** | *Official Journal of the EU*, OJ L 347, 30.9.2021, p. 182 (§3.3.2.4) | Max Reference Mark 50 per lamp ($215,000\ \text{cd}$) | Source cited |
| 3 | **IEC 60825-1 $C_4$ Ratio** | IEC 60825-1:2014, Edition 3.0, Table 9 | $10^{0.48} / 10^{0.41} = 3.01995 / 2.57040 = \mathbf{+17.49\%}$ | Calculation |
| 4 | **IEC 60825-1 Flux Ratio** | IEC 60825-1:2014, Tables 3, 4 | $(10\ \text{mW} / 1.002\ \text{mW}) \times (1550 / 905) = \mathbf{17.09\times}$ | Calculation (long-exposure limits) |
| 5 | **Waymo Patent Wavelength** | USPTO Patent No. 9,368,936 B1, Col. 5 and 17 | **905 nm** diode laser with GaN FET driver | Source cited |
| 6 | **Waymo 6th-Gen Sensors** | S. Jeyachandran Official Blog (Aug 19, 2024) | **13 cameras, 4 lidars, 6 radars** | Company statement |
| 7 | **Zoox Sensor Complement** | *Forbes* (A. Ohnsman) | **8 Hesai lidars, 18 cameras, 10 radars, 4 LWIR thermal** | Trade press; not confirmed by Zoox (report, Appendix 1) |
| 8 | **Ford L3 & Latitude AI** | D. Field (CES 2026; Reuters, Jan 2026); Ford, 2 Mar 2023 | **Lidar planned for 2028 L3; Latitude AI (~550 former Argo staff)** | Source cited |
| 9 | **Cadillac Night Vision** | *Automotive News*, Nov 15, 2004 | **7,000 (2000) $\to$ 600 (2004) $\to$ 145 (2005)** | Trade press; not checked against GM records |
| 10 | **Huawei 896-Line Specs** | Huawei HIMA Release; *STCN* (Mar 4, 2026) | **Dual-optical-path (120°/30°), 14 cm @ 120 m (Huawei)** | Company statement |
| 11 | **Hesai Picasso Architecture** | Hesai Tech Day (Apr 17, 2026) | **PDE >40%, 2,160 ch/die, 2 dies in ETX** | Company statement |
| 12 | **Luminar LSI Sale** | SEC Form 8-K (CIK 0001758057), Item 2.01 | **$110.0M cash** to Quantum Computing Inc. (Feb 2, 2026) | Source cited |
| 13 | **Luminar LiDAR Assets Sale** | SEC Form 8-K (CIK 0001758057), Item 2.01 | **$33.0M cash** to MicroVision at auction (Feb 3, 2026) | Source cited |
| 14 | **Hesai FY2025 Shipments** | SEC Form 20-F (CIK 0001861737) | **1,620,406 units** (1,381,133 ADAS + 239,273 Robotics) | Source cited |
| 15 | **Hesai FY2025 Financials** | SEC Form 20-F; HK annual report, p. 136 | **RMB 3,027.6M rev; 41.8% GM; NA rev RMB 451.7M (14.9%)** | Source cited |
| 16 | **Hesai Supplier Concentration** | HK annual report (Form 6-K), p. 33 | **Largest: 4.6%; Top Five: 20.5% of total purchases** | Source cited |
| 17 | **Mobileye FMCW Wind-Down** | SEC Form 10-Q (CIK 0001910139), Note 1 | **Sept 9, 2024 closure; EyeQ6 + radar + lower-cost third-party ToF lidar** | Source cited |
| 18 | **D.C. Cir. Hesai v. DoD** | D.C. Cir. Docket No. 25-5256 (Aug 18, 2026) | **Reversed on Due Process; Remanded without vacatur** | Source cited |
| 19 | **NHTSA EA26002 (Tesla)** | NHTSA ODI Investigation EA26002 | **3.2M vehicles; information request includes "Radar Saves Us" document** | Source cited |
| 20 | **FMVSS 127 Darkness Rules** | 49 CFR § 571.127 (89 FR 39686) | **Darkness PAEB tests up to 65 km/h @ $\le 0.2\text{ lux}$, lower and upper beams separately; Sept 1, 2029** | Source cited |
| 21 | **US BIS Connected Vehicles** | 15 CFR Part 791 (90 FR 5360) | **ADS softw. MY2027; VCS hardw. MY2030; LiDAR not banned** | Source cited |
| 22 | **USGS Gallium / Germanium** | USGS Mineral Commodity Summaries 2026 | **Ga: China 98.9% (99%); Ge: EU price $4,100/kg avg ($5,380 in Oct 2025)** | Source cited |
| 23 | **Seyond Wavelength Matrix** | Seyond Official Datasheets (V2.2.0) | **Falcon K2: 1550 nm; Robin E1X: 940 nm; Robin W: 905 nm** | Company datasheets |
| 24 | **Sony SPAD IMX459 / 479** | Sony Semiconductor Press Releases | **IMX459: 905nm/24% PDE; IMX479: 940nm/37% PDE/520 lines** | Company releases |
| 25 | **Aeva Daimler C-Samples** | Aeva Official Release (May 6, 2026) | **Initial Atlas C-samples delivered for Cascadia L4 (production-intent, 2027 target per the earnings call)** | Company statement |
| 26 | **Aeva European OEM L3** | Aeva Official Release (Dec 3, 2025) | **Exclusive Tier-1 supplier for a Top-10 OEM platform (Atlas Ultra, SOP target 2028)** | Company statement; no definitive volume agreement per Aeva's 10-K |
| 27 | **Silicon Bandgap Cutoff** | Solid-State Physics / $hc/E_g$ at 300K | **$\lambda_c = 1,103\text{ nm}$; 1550 nm transparent in Si, needs InGaAs or Ge-on-Si** | Calculation |
| 28 | **NHTSA Phantom Braking** | NHTSA ODI PE22-002 (closed 29 Jun 2026) | **Unexpected braking, MY2021–22 Model 3/Y; closed without recall; no causal finding** | Source cited |
| 29 | **Everbright AEC-Q102 VCSEL**| Everbright announcement (Mar 31, 2023), via DRAMX/TrendForce| **AEC-Q102 automotive qualification for LiDAR VCSEL arrays** | Trade press |
| 30 | **Innoscience AEC-Q101 GaN** | Innoscience release (Oct 30, 2024) and lidar page | **AEC-Q101 for two 100 V GaN HEMTs; evaluation board: 1.5 ns pulse, 74.93 A** | Company statement |



