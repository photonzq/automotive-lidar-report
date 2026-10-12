"""Texts for edits_partB_definitive.py (5 Oct 2026).

Each entry is (id, unique start of the report line, change):
  - ("sub", old_fragment, new_fragment): replace one fragment inside that line;
  - a string: the new full line;
  - None: delete the line;
  - a list of strings: keep the line and insert these lines after it.
"""

HESAI_Q2 = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0818/2026081800396.pdf"

EDITS = [
    # §B1
    ("b1-hesai-revenue-per-unit", "- **Hesai revenue per unit.** Revenue per unit is quarterly revenue",
     ("sub", "The Q2 2026 revenue and unit inputs behind the RMB 1.37k figure are not reproduced in this report.",
      "In Q2 2026 Hesai's net revenues were RMB 860.8 M on 628,275 lidars shipped, so revenue per unit was "
      "$860.8\\text{ M}/628{,}275\\approx\\text{RMB }1{,}370$ "
      f"[P, [Q2 2026 results]({HESAI_Q2}); E].")),
    # §B4
    ("b4-aurora-count", "  - **Aurora:** FirstLight FMCW plus short-range units.",
     ("sub", "Hesai is reported as the near-range supplier. No count was found for the 2025–26 hardware [P/T].",
      "Hesai is reported as the near-range supplier [P/T]. Aurora has published no lidar count for its 2025–26 "
      "hardware (Appendix 1).")),
    ("b4-waabi-split", "| **Waabi / Volvo** | None |",
     ("sub", "[P, via Aurora's letter; the split between Aurora and Waabi is unclear]",
      "[P, via Aurora's letter, which does not split the trucks between Aurora and Waabi]")),
    # §B5
    ("b5-short-answer", "**Short answer.** Outside China, both passenger-car lidar and OEM thermal night vision",
     ("sub", "appear to be **well below 1% of new vehicles**; their precise ranking is unresolved. Lidar may dip "
             "below thermal in 2026, but the report has no complete installation series for either.",
      "are **well below 1% of new vehicles** [E]. Neither has a complete published installation series, so "
      "their exact order is unknown, and lidar may dip below thermal in 2026.")),
    # §B6
    ("b6-no-lidar-models", "- **No lidar on current China models:** BMW iX3 LWB",
     ("sub", "VW's Xpeng-based ID. UNYX 08. Honda and Hyundai are not established.",
      "VW's Xpeng-based ID. UNYX 08, and Beijing Hyundai's IONIQ V [S]. Honda's China models are covered in "
      "Appendix 1.")),
    ("b6-program-orders", "  2. **The potential volume paradox.**",
     ("sub", "These are program orders, not verified delivered units.",
      "These are program orders, not delivered units.")),
    # §B7
    ("b7-denominator", "**The denominator matters.** Parking beeps,",
     ("sub", "This report has no verified global installation series or matched system-price series for parking "
             "lidar, so I do not assign it a market-size number.",
      "Parking lidar has no published global installation series or matched system-price series, so it gets "
      "no market-size number (Appendix 1).")),
    ("b7-product-hypotheses", "A lower-cost, shorter-range lidar could still make sense",
     ("sub", "not verified adoption forecasts.", "not adoption forecasts.")),
    # §B7.1
    ("b71-how-to-read", "**How to read the numbers.** The figures below are indicative.",
     ("sub", "There is still no audited global parking-sensor installation or price series here.",
      "No audited global series of parking-sensor installations or prices is published.")),
    ("b71-apa-series", "- **Automated-parking features:** [ResearchInChina]",
     ("sub", "APA definitions and coverage differ, so this does not establish a comparable jump from 8.2% to 30%.",
      "APA definitions and coverage differ between the two sources, so 8.2% (2023) and 30% (H1 2025) are not "
      "a like-for-like series.")),
    ("b71-bosch-fitment", "  - The Tier 1s (suppliers selling complete sensors directly to carmakers)",
     ("sub", "it is a fitment list, not confirmed original-equipment (OE, factory-fitted) supply.",
      "a fitment list shows which cars a replacement part fits, not who supplied the factory-fitted "
      "(original-equipment, OE) sensors.")),
    ("b71-valeo-nomination", "- **Ultrasound remains in new programmes:**",
     ("sub", "this one is current, but it is not confirmed delivered volume.",
      "this one is current, and it records an award, not delivered volume.")),
    ("b71-lateral-sampling", "- **Lateral sampling.** A single wide acoustic beam",
     ("sub", "does not establish metric depth accuracy or coverage at the bumper.",
      "does not by itself give metric depth accuracy or coverage at the bumper.")),
    ("b71-ftx-note", "5. **FTX.** [Hesai calls Li Auto L9 Livis",
     ("sub", "FTX installations by model/trim are not disclosed here.",
      "Hesai does not disclose FTX installations by model or trim.")),
    ("b71-tracker-trend", "- **Chinese blind-spot lidar is visible, but much smaller",
     ("sub", "Treat the direction as tentative, not a reconciled trend.",
      "Because the two trackers count differently, the fall from about 16% to 11% is not a reconciled trend.")),
    # §B8
    ("b81-industrial-size", "These points reinforce the caution above: humanoid lidar demand",
     ("sub", "No credible industrial-lidar or safety-scanner market size was found.",
      "Industrial lidar and safety scanners have no credible published market size (Appendix 1).")),
] + [
    # §B7.1 parking: research of 5 Oct 2026 (Aumovio, Aptiv, Rivian, Li Auto, Hesai and RoboSense documents)
    ("b71-rivian-li-auto", "- **Radar replacing ultrasound:** at Rivian's",
     ("sub", "[Rivian reported R2 deliveries beginning in Q2 2026](https://www.sec.gov/Archives/edgar/data/1874178/"
             "000187417826000053/ex-9922q26rivianearnings.htm) [P]. This is a more concrete deployment path than a "
             "supplier reference design, though no public component teardown or matched parking-performance study "
             "was found.",
      "[Rivian reported R2 deliveries from 9 June 2026](https://www.sec.gov/Archives/edgar/data/1874178/"
      "000187417826000053/ex-9922q26rivianearnings.htm) [P], and the June 2026 "
      "[R2 owner's guide](https://documents.cdn.ifixit.com/vx2RolDBvXboBYLs.pdf) shows no ultrasonic sensors and "
      "gives radar-and-camera parking warnings up to 1.45 m front and rear and 0.75 m at the sides [P]. Li Auto's "
      "new L9 (15 May 2026) is the second case: it [replaces its 12 ultrasonic sensors with UWB (ultra-wideband) "
      "near-field radar](https://www.lixiang.com/news/159.html) [P]. These are deployments in production cars, "
      "not supplier reference designs; no component teardown or matched parking-performance study of either has "
      "been published.")),
    ("b71-conti-aptiv", "  - [Continental's Radar Vision Parking]",
     "  - [Continental's Radar Vision Parking](https://www.continental.com/en/press/press-releases/20231116-radar-"
     "vision-parking/), now an Aumovio product, was shown at CES 2024 and 2025 as a surround-radar-plus-camera "
     "substitute for ultrasound [P]. No customer, award or production start for it has been announced, and "
     "Aumovio's production parking system, [Xelve Park](https://www.aumovio.com/en/solutions/driver-assistance/"
     "automated-assisted-driving/xelve-a-scalable-adas-and-ad-system-setup.html), uses cameras and ultrasonic "
     "sensors [P]. [Aptiv's PULSE](https://www.aptiv.com/docs/default-source/ces-2026/2026-aptiv-ces-"
     "knowbeforeyougo.pdf) puts a surround-view camera and a 76–81 GHz ultra-short-range radar in one "
     "camera-sized housing; Aptiv says one unit front and one rear can replace a 12-sensor ultrasonic system [P]. "
     "PULSE is at A-sample stage, with production targeted for 2027 [I, [Frost & Sullivan](https://www.frost.com/"
     "wp-content/uploads/2025/10/Aptiv-Final-Report.pdf)], and its only announced customer is a warehouse-robot "
     "maker [P]."),
    ("b71-table-near-field", "| Near-field limit |",
     ("sub", "Minimum valid range is not stated in the cited FTX/E1R product summaries; verify on the installed vehicle",
      "RoboSense E1R: 0.1 m blind area; automotive E1: ground blind area ≤15 cm [P]. Hesai gives no minimum range "
      "for FTX, though it does for other models (QT128: 0.05 m) [P]; FT120's 0.1 m comes from a withdrawn Hesai "
      "page [T]")),
    ("b71-radar-reuse", "- **Radar's case is re-use.**",
     ("sub", "It is not established that every existing corner radar can be upgraded in software to replace "
             "ultrasonic sensors.",
      "Both production cases use radars built for the near field, Rivian's dual-mode corner radars and Li Auto's "
      "UWB units, and Aptiv's PULSE adds a dedicated ultra-short-range radar [P]; none relies on a software update "
      "to an ordinary corner radar [E].")),
    ("b71-e1-specs", "6. **E1R.**",
     ("sub", "The automotive E1's specifications are not tabulated here.",
      "The automotive E1 is specified at 120° × 90°, 30 m at 10% and 10–30 Hz, without a published point rate "
      "[P, [product page](https://www.robosense.ai/en/rslidar/E1)]; RoboSense names Baidu's next-generation "
      "Apollo Go robotaxi as an E1 design win [P].")),
    ("b71-no-lidar-replacement", "  - No OEM or supplier statement that lidar replaces ultrasound",
     "  - No carmaker or lidar supplier has announced lidar as a replacement for ultrasonic sensors. Blind-spot "
     "lidar sits alongside 12–15 ultrasonic sensors on the Zeekr 9X, Aito M9, Maextro S800, NIO ES8 and Xiaomi "
     "SkyNomad N90 Max [T, Autohome configurations]. The new Li Auto L9 dropped its ultrasonic sensors for UWB "
     "radar, not lidar: its Ultra trim, which has no blind-spot lidar, has no ultrasonic sensors either [P/T]."),
    ("b71-judgement-low-end", "- **Low-end parking assistance is likely",
     ("sub", "Radar re-use now has at least one announced vehicle deployment (Rivian R2); lidar has no verified "
             "high-volume ultrasound-replacement programme in this review.",
      "Radar has replaced ultrasound in two production cars, the Rivian R2 and the 2026 Li Auto L9 (UWB); no "
      "carmaker has replaced ultrasound with lidar.")),
    ("b71-what-would-change", "- **What would change this:** several high-volume radar-for-ultrasound",
     ("sub", "The Rivian R2 announcement is one radar data point, without a published matched miss-rate comparison.",
      "The Rivian R2 and the Li Auto L9 are two radar data points, neither with a published matched miss-rate "
      "comparison.")),
    # §B4a and §D3: US rules and Japanese delivery robots (research of 5 Oct 2026; 90 FR 5360, P.L. 118-159,
    # P.L. 119-60, FCC DA 26-786, 85 FR 7826, Panasonic's 2020 filing to the National Police Agency)
    ("b4a-japan-row", "| | Japan: Panasonic Hakobo, ZMP DeliRo, Rakuten |",
     "| | Japan: Panasonic Hakobo, ZMP DeliRo, Rakuten | Small: since Jan 2025 one Panasonic operator has run "
     "10 Hakobo robots at once across Fujisawa, Kadoma and Saga under a special road-use permit; the certified "
     "ratio for ordinary operation is one operator to four robots, as for DeliRo [P] | Hakobo: 3D and 2D lidar "
     "plus remote-operation cameras ([Panasonic's 2020 filing](https://www.npa.go.jp/bureau/traffic/council/"
     "mobility/1210-4.pdf) to the National Police Agency) [P]. DeliRo (ZMP, now ROBO-HI): cameras and \"laser "
     "sensors\" for 360° sensing [P] |"),
    ("b4a-us-rules", "- **Exports carry Chinese lidar.**",
     "- **Exports carry Chinese lidar.** Chinese vans sold abroad fit RoboSense or Hesai units. In the US the "
     "barrier is the van, not its lidar. The Commerce Department's [connected-vehicle rule]"
     "(https://www.govinfo.gov/content/pkg/FR-2025-01-16/pdf/2025-00592.pdf) (15 CFR 791 subpart D, §D3) covers "
     "road vehicles of up to 10,000 lb gross vehicle weight; for vans in that class it bars China-controlled "
     "makers such as Neolix or Zelos, from model year 2027, from selling them in the US or running a commercial "
     "driverless service with them, and bars any importer from selling vans that run Chinese driving software "
     "[P]. The rule exempts lidar as automotive sensing and excludes sidewalk delivery robots [P]. Since "
     "28 Jul 2026, however, foreign-made autonomous mobile robots are on the FCC's Covered List, which blocks "
     "equipment authorization for new models, delivery robots included [P, FCC DA 26-786; I for delivery "
     "robots]. The Pentagon's lidar bans reach only what the Defense Department buys and operates (§D3), and a "
     "van without manual controls also needs an NHTSA exemption from the federal safety standards, as Nuro's R2 "
     "received in 2020 [P, 85 FR 7826]."),
    ("d3-805-components", "  - from **30 Jun 2027**, it may not buy goods",
     ("sub", "reportedly with an exemption for components of end items.",
      "with an exemption for components written into the act (§805(a)(3)(C)) [P].")),
    ("d3-civilian-restriction", "- A civilian restriction would need S.4429",
     ("sub", "and no BIS sensor proposal has been found (§D6 dates).",
      "and BIS has published no sensor proposal; its 2025 rule left lidar to possible separate rulemaking "
      "(§D6 dates) [P].")),
    ("d3-s4429-status", "  - *Status:* the bill **passed Senate Commerce",
     ("sub", "No floor vote or NDAA attachment was found by late Sep 2026.",
      "It had no floor vote by 5 Oct 2026, and the House-passed FY2027 NDAA carries no lidar provision [P].")),
    ("appx1-delivery-vans", "- **China's delivery vans (§B4a).**",
     ("sub", "; and whether GB 44721-2026, which applies to vehicles with L3 or L4 systems from 1 Jul 2027, will "
             "bind vans that run under municipal pilot rules.",
      "; whether GB 44721-2026, which applies to vehicles with L3 or L4 systems from 1 Jul 2027, will bind vans "
      "that run under municipal pilot rules; and, for the US, whether any van exceeds the 10,000 lb limit of the "
      "connected-vehicle rule and whether BIS counts a driverless delivery service as a \"commercial service\" "
      "under 15 CFR 791.304 (its examples are robotaxi and rideshare).")),
    ("appx1-delivery-robots", "- **Delivery robots outside China (§B4a, subsection 4).**",
     ("sub", "; and Japan's parcel volume for fiscal 2025 (fiscal 2024: 5.03 B, MLIT, Japan's transport ministry). "
             "They would size this market outside China.",
      "; Japan's parcel volume for fiscal 2025 (fiscal 2024: 5.03 B, MLIT, Japan's transport ministry); and "
      "whether today's Hakobo still carries its 2020 pair of 3D and 2D lidar, and which lidar DeliRo uses. The "
      "first three would size this market outside China.")),
    # §B2, §B4, §B7.1: vehicle facts (research of 5 Oct 2026: Zoox NHTSA docket NHTSA-2025-0523 and Hesai F-1/A;
    # May Mobility's Sep 2026 investor deck; Ouster, Aeva and Luminar releases and filings; PlusAI's 2026
    # prospectus; Mercedes S-Class press kit of 30 Jan 2026; Zeekr 9X launch reports)
    ("b2-sclass", "5. **Mercedes next L3.**",
     ("sub", "**Customer 2026/27 S-Class cars appear to carry no lidar in any market**; the roof-lidar cars shown are "
             "robotaxi prototypes [T].",
      "**The facelifted S-Class (premiere 29 Jan 2026) has no lidar and no DRIVE PILOT in any market**: every car "
      "carries 10 cameras, 5 radars and 12 ultrasonic sensors for the Level 2++ MB.DRIVE ASSIST PRO "
      "[P, [press kit](https://media.mercedes-benz.com/en/press-kit/71dc2a9c-34c7-47e0-a264-d39d89b85d4c/article/"
      "8e671658-cf56-45c3-8ba7-15e997dee179)]. The roof-lidar S-Class cars shown are robotaxi prototypes [T].")),
    ("b4-zoox", "- **Zoox:** about 100 robotaxis",
     "- **Zoox:** about 100 robotaxis; Hesai supplies lidar, and Hesai's 2023 prospectus names Zoox as a customer "
     "for its flagship Pandar series [P]. Zoox's exemption filings with NHTSA (the US National Highway Traffic "
     "Safety Administration) list the sensor types (lidar, radar, cameras, thermal cameras and microphones) in four "
     "corner pods, the drive module and the A-pillars, but file the sensor layout and per-sensor coverage as "
     "confidential business information [P, [petition](https://downloads.regulations.gov/NHTSA-2025-0523-0002/"
     "attachment_3.pdf)]. The only public count is a 2025 *Forbes* report: **8 lidars, 18 cameras, 10 radars, "
     "4 thermal cameras and 8 microphones** [T]. Zoox has offered paid rides in Las Vegas since 10 Aug 2026 and "
     "holds an NHTSA exemption for up to 2,500 vehicles per year."),
    ("b4-may", "- **May Mobility** selected Aeva",
     "- **May Mobility**'s Toyota Sienna, as configured at the end of 2025, carries a primary roof lidar, a "
     "forward lidar and secondary lidars at the front fender and rear, all off the shelf; May's 2026 "
     "[investor deck](https://www.sec.gov/Archives/edgar/data/2111542/000121390026100367/ea030470201ex99-2.htm) "
     "names no suppliers [P]. The supplier record dates from 2023: Ouster then supplied four OS1 short/mid-range "
     "units and one Alpha Prime long-range unit per vehicle, with more than 1,000 sensors committed through 2024, "
     "and Aeva became May's **exclusive production supplier of long-range lidar**, with volume commitments "
     "through 2028 and Aeries II ramping from 2025 [P]. Neither company's later filings mention May (Appendix 1)."),
    ("b4-plus", "- **Plus** announced agreements with Ouster",
     "- **Plus** signed lidar agreements with Ouster (Feb 2021: a customer agreement with an initial order of "
     "2,000 sensors), Aeva (Nov 2021: a multi-year supply agreement for long-range FMCW lidar, shown with Aeries II "
     "in 2023) and Luminar [P]. The Luminar arrangement had two parts: in Jun 2023 Luminar became the exclusive "
     "mid- to long-range lidar for *PlusDrive*, and in Aug 2023 it made a separate \\$10 M investment in Plus (a "
     "SAFE, a simple agreement for future equity), paid in Luminar shares [P]. None is disclosed as a binding "
     "volume contract; PlusAI's 2026 prospectus says the truck makers buy the sensors, and Luminar sold its lidar "
     "business to MicroVision in Feb 2026 [P]."),
    ("b4-dated-wins", "- Treat these as dated program wins",
     ("sub", "Treat these as dated program wins, not an additive sensor list [P].",
      "These are dated programme wins, not an additive sensor list [P].")),
    ("b4-botauto-row", "| **Bot Auto** |",
     ("sub", "Scaling not disclosed | Not checked |", "Scaling not disclosed | Not disclosed (Appendix 1) |")),
    ("b4-plusai-row", "| **PlusAI** | None found |",
     "| **PlusAI** | None | SPAC merger with Churchill Capital IX terminated 20 Apr 2026, citing market conditions; "
     "a new SPAC deal with Texas Ventures Acquisition III followed in Sep 2026 [P] | OEM-built trucks around 2027 "
     "[U] | Chosen and bought by the truck makers (TRATON, IVECO, Hyundai); none names a vendor for its 2025–26 "
     "trucks [P] |"),
    ("b71-zeekr", "  - [Zeekr says the 9X H9 has five lidars]",
     "  - [Zeekr says the 9X H9 has five lidars](https://www.zeekrgroup.com/news/202507091) [P]: a custom "
     "RoboSense 520-line main lidar ([RoboSense via tgbus](https://tech.tgbus.com/news/234712)) and four "
     "blind-spot lidars of Zeekr's own design, **alongside 12 ultrasonic sensors**, 5 4D radars and 13 cameras "
     "([launch report](https://finance.sina.com.cn/tech/discovery/2025-09-29/doc-infseqec8172233.shtml)) [T]. "
     "The NE Times 'Zeekr' blind-spot count above is therefore of Zeekr's in-house units; at four per car its "
     "17,568 units correspond to about 4,400 9X H9 cars if all went into that model "
     "[E: $17{,}568/4\\approx4{,}390$]. Zeekr has not published the blind-spot units' detailed specifications "
     "(Appendix 1)."),
    ("appx1-zoox", "- **Zoox:** the exact count from an OEM specification is missing.",
     "- **Zoox:** no primary source gives lidar counts or models. Zoox filed its sensor layout and per-sensor "
     "coverage with NHTSA as confidential appendices, and the 2026 exemption grant lists sensor types only [P]; "
     "*Forbes*'s 8 lidars, 18 cameras, 10 radars, 4 thermal cameras and 8 microphones is the count used in §F4 "
     "[T]. Unknown: which Hesai model or models the robotaxi carries, and where the eight lidars sit."),
    ("appx1-gatik-may-plusai", "- **Gatik, Avride, May and PlusAI:**",
     "- **Gatik, Avride, May and PlusAI:** the current vehicle-level supplier mixes of Gatik and Avride are unknown "
     "(Avride's Ioniq 5 robotaxis carry 13 cameras plus lidar and radar [T]). May's end-2025 Sienna carries roof, "
     "forward, fender and rear lidars, but May names no suppliers, and neither Aeva nor Ouster has mentioned May "
     "since 2023 [P]; the maker of each unit and the next-generation vehicle's suite are unknown. PlusAI designs "
     "no sensors: the truck makers that integrate its software (TRATON, IVECO, Hyundai) choose and buy the lidars, "
     "and none names a vendor for its 2025–26 trucks [P]. Its 2023 Luminar arrangement combined a *PlusDrive* "
     "exclusivity agreement with a separate \\$10 M investment [P]."),
    ("appx1-zeekr-blind-spot", "- **Mechanical scanners (§C4d).**",
     ["- **Zeekr 9X blind-spot lidar (§B7.1).** The four near-field units are Zeekr's own design [T]. Unknown: "
      "their field of view, range, minimum range, point rate and chip suppliers; one trade article gives "
      "150° × 112° and 15 m, with Fushi SPAD receivers and Ruixi VCSEL emitters [U]."]),
    ("appx1-parking", "- **Chinese-brand lidar exports outside China.**",
     ["", "**Parking and near-field sensing**",
      "- **Parking sensors (§B7).** Unknown: a global installation series and matched system prices for parking "
      "lidar; Hesai's FTX minimum range (no Hesai document gives it, and a trade page's 0.05 m is unconfirmed "
      "[U]); the automotive E1's point rate and passenger-car programmes; PULSE's automotive customer and start of "
      "production (the 2027 target is Frost & Sullivan's); whether any of Aumovio's awarded parking projects is "
      "radar-only; the supplier and minimum distance of the R2's corner radars; who supplies the L9's UWB radar; "
      "and a matched miss-rate comparison of radar, UWB or lidar against ultrasound. These decide whether lidar "
      "ever takes the parking function from ultrasound (§B7.1)."]),
]
