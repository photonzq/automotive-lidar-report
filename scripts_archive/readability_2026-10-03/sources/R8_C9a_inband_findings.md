# Round 4 source findings: R8_C9a_inband

Read on 5 Oct 2026. Every `old` string below was copied from the report as of sha 7d73cf7910b5 and checked against it; each occurs exactly once (check script `scripts/R8_check_old_strings.py`). The equation that item 2 cites is Eq. (123) in that version.

---

## R8_C9a_inband-01

- **Question:** What share of the lidars installed in Chinese passenger cars in 2025 and H1 2026 emits at 905 nm, 940 nm and 1,550 nm, and what does that make the in-band share $f_{\rm band}$ of §C9a item 2 for a 905 nm and for a 940 nm victim?

- **Answer:**

  **1. Wavelength and unit share of each product.** Shares are of all units installed in the period (main plus blind-spot). The 2025 column uses the Gasgoo supplier shares that §B1 quotes (Huawei 41.5%, Hesai 33.8%, RoboSense 17.0%, Seyond 7.7%) and splits each supplier as described in part 2. The H1 2026 column sums NE Times' monthly charts for Jan–Feb, Mar, Apr, May and Jun 2026, which give every supplier's main and blind-spot units (2,282,153 units in all). No other product reaches about 2% in either tracker.

  | Product (role) | Wavelength | Source of the wavelength | 2025 share | H1 2026 share |
  |---|---|---|---|---|
  | Hesai ATX and AT128/AT128P (main) | 905 nm | ATX user manual A12 (10 Sep 2026), §1.5 spec table, p. 14; AT128P user manual A02 (10 Jan 2026), §1.5, p. 13 [P] | 33.8% (Gasgoo counts all 1.143 M Hesai units as main lidars; ATX deliveries reached nearly 1 M by late Nov 2025 [T]) | 31.3% (714,902) |
  | Hesai FT120, FTX (blind-spot) | 940 nm | FT120 user manual F01 (10 Jan 2025), §1.5, p. 16; FTX_140 user manual F04, §1.4, p. 15; FTX_180 user manual F07, §1.4, p. 15 [P] | ≈0 | 1.3% (29,510) |
  | Huawei 192-line D3 (and D3P), 96-line D2 (main) | 905 nm | D3: TechInsights teardown of the L306 192-line unit from an AITO M9 [I]; D2: 905 nm EEL with SPAD in a published teardown [T]; D3P: no public source, taken as the D3 family | 24.1% ($41.5\%\times0.581$) | 4.1–10.5% (Huawei main units less the 896-line) |
  | Huawei 896-line, dual optical path (main) | not published | Huawei's launch release and ADS page give none [P]; NE Times: over 57% of Huawei's main units in May 2026 [T] | 0 (production from Mar 2026) | 3.7–10.1% (central 5.8%) |
  | Huawei Flash blind-spot unit, SL210 (blind-spot) | not published | Trade press gives 8 m at 10%, 120° × 90° and a HiSilicon SPAD, but no wavelength [T] | 17.4% (16.2% in NE Times) | 16.8% (382,424) |
  | RoboSense M platform: M1, M1P, M2, MX (main) | 905 nm | RS-LiDAR-M1 user guide, Table 1 [P]; M1 Plus on RoboSense's store [P]; MX "completely inherits" the M platform's "core optical path and optoelectronic devices" (RoboSense MX page) [P] | 6.2–17.0% | 0–15.6% |
  | RoboSense EM platform: EM4, EMX (main) | conflicting | EM4: "940nm VCSEL" in launch coverage of RoboSense's 7 Jan 2025 release (IT之家) and in NE Times' teardown summary [T], but 905 nm in two distributors' listings [S]; EMX: none from RoboSense, 905 nm in one retailer's listing [S] | 0–10.8% | 0–15.6% (RoboSense main 356,263 in all) |
  | RoboSense E1 (blind-spot) | 940 nm, reported | NE Times teardown summary [T] | ≈0 | 0.2% (4,347) |
  | Seyond Falcon K/K2/K3 (main) | 1,550 nm | the Falcon K1 manual and K2 datasheet that §C3 and §C4 cite [P] (not re-read here) | 4.5% | 4.7–6.4% |
  | Seyond Robin W, W1G (side units, two per NIO ES8) | 905 nm | Robin W1G datasheet [P]; ES8 carries one Falcon and two Robin W (MarkLines, 25 Aug 2025) [T] | 3.2% | 8.2% (186,504) |
  | Seyond Robin E1X (main) | 940 nm | Robin E1X C-sample datasheet V3.0.0 [P] | ≈0 (car SOP 2026: AION N60, Hyptec S600, new ONVO L60) | 0–1.7% (central 1.1%) |
  | Zeekr in-house blind-spot units (four per 9X H9 or 8X) | not published | the VCSEL supplier's release names the architecture only [P] | 0.5% (NE Times only) | 6.0% (137,112) |

  **2. Share arithmetic.** Let $s_\lambda$ be the share of installations at wavelength $\lambda$ and $s_U$ the share whose wavelength is not published or conflicting.
  - *2025, Gasgoo basis.* $s_{905}=s_{\rm He}+s_{\rm Hw}h+s_{\rm RS}(1-y)+s_{\rm Se}w$, where $s_{\rm He}=0.338$, $s_{\rm Hw}=0.415$, $s_{\rm RS}=0.170$ and $s_{\rm Se}=0.077$ are the Gasgoo shares; $h=746{,}198/1{,}284{,}905=0.581$ is the main-lidar fraction of Huawei's units (NE Times, the only tracker that splits them); $w=137.8/332.5=0.414$ is the Robin share of Seyond's 2025 shipments (§B1), taken as Robin W because Robin E1X reached cars only in 2026; and $y$ is the EM-platform share of RoboSense's units. $y$ lies between 0 and $(609{,}000-220{,}500)/609{,}000=0.638$, because all of RoboSense's ≈220,500 H1 2025 ADAS units (interim results, p. 1) predate EM4's Q3 2025 production and EMX's batch deliveries from 9 Sep 2025. Hesai's FT120 and FTX are taken as zero because Gasgoo's main-lidar count for Hesai, 114.3万, equals its all-unit count ($0.338\times3.386\ {\rm M}=1.144$ M).
    - $s_{905}=0.338+0.415\times0.581+0.170(1-y)+0.077\times0.414=0.781-0.170\,y$, i.e. 0.781 at $y=0$ and 0.672 at $y=0.638$.
    - $s_{940}$ (EM platform counted at 940 nm) $=0.170\,y=0$ to 0.108.
    - $s_{1550}=0.077\times(1-0.414)=0.045$.
    - $s_U=0.415\times(1-0.581)=0.174$ (Huawei's blind-spot units). The four terms sum to 1.000 at either end of $y$.
    - On NE Times' own 2025 shares (Huawei 38.7%, Hesai 32.0%, RoboSense 20.9%, Seyond 7.8%, Zeekr 0.5%) the same steps give $s_{905}=0.653$–0.787, $s_{940}=0$–0.134, $s_{1550}=0.046$ and $s_U=0.168$.
  - *H1 2026, NE Times basis*, $N=2{,}282{,}153$ units (monthly totals 602,419, 334,170, 371,534, 446,682 and 527,348):
    - Hesai main 714,902 (0.313, 905 nm); Hesai blind-spot 29,510 (0.013, 940 nm); RoboSense blind-spot 4,347 (0.002, 940 nm); Seyond blind-spot 186,504 (0.082, Robin W, 905 nm); Huawei blind-spot 382,424 (0.168, U); Zeekr 137,112 (0.060, U).
    - Huawei main 324,931 (0.142). The 896-line unit started in March and was over 57% of Huawei's main units in May, so it is bounded by $0.57\times(65{,}875+82{,}250)=84{,}431$ (none in Mar–Apr) and all Mar–Jun main units, 230,838, with a central $0.57\times230{,}838=131{,}578$. That leaves 94,093–240,500 D3/D3P units (0.041–0.105) at 905 nm.
    - RoboSense main 356,263 (0.156), split between the M platform (905 nm) and the EM platform (EM4 reported at 940 nm, EMX unpublished) in an undisclosed ratio $y$ between 0 and 1.
    - Seyond main 146,160 (0.064): Falcon plus Robin E1X. The main units not on the ES8 (main minus half the blind-spot units) were 7,573 in Jan–Feb, 5,541 in Mar, 9,373 in Apr, 14,943 in May and 15,478 in Jun; their excess over the Jan–Mar rate of 4,664 a month, 25,803 units, is taken as Robin E1X (central), with 0 and all 39,794 Apr–Jun non-ES8 units as bounds [E].
    - Result: documented 905 nm $s_{905}=0.313+0.082+(0.041\ {\rm to}\ 0.105)+0.156(1-y)=0.436$–0.656; documented or reported 940 nm $s_{940}=0.013+0.002+(0\ {\rm to}\ 0.017)+0.156\,y=0.015$–0.188; $s_{1550}=0.047$–0.064; $s_U=0.168+0.060+(0.037\ {\rm to}\ 0.101)=0.265$–0.329.
  - *Cross-check.* For Q1 2026 Gasgoo counts 940,656 units against NE Times' 936,589 (0.4% apart). By supplier, NE Times' counts are 0.99 of Gasgoo's for Seyond (155,950 against 158,008), 0.96 for Huawei (291,869 against 303,753), 0.89 for Hesai (292,143 against 328,246) and 1.28 for RoboSense (133,139 against 103,761); Gasgoo's "others" (46,888, 5.0%) is of the size of Zeekr's in-house units (63,488 in NE Times).

  **3. Wavelength shares.** 2025: 905 nm 67–78%, 940 nm 0–11%, 1,550 nm 4.5%, undisclosed 17% (Huawei's blind-spot units). H1 2026: 905 nm 44–66%, 940 nm 1.5–19%, 1,550 nm 4.7–6.4%, undisclosed 27–33% (Huawei's blind-spot and 896-line units, Zeekr's units). The 9xx share is thus 95.5% for 2025 and 94–95% for H1 2026 on an installation basis, inside §C2's ≈94–96%.

  **4. $f_{\rm band}$ and the filters.**
  - The receive filters the report assumes are 10 nm at 940 nm and 20–40 nm at 905 nm (§C6(d), §C4c). With the drift coefficients of §C9 and §C6(d′) (EEL 0.27 nm/K, VCSEL 0.07 nm/K, 25 °C nominal), over −40 to +105 °C a 905 nm EEL spans 887.5–926.6 nm, a 905 nm VCSEL 900.5–910.6 nm and a 940 nm VCSEL 935.5–945.6 nm.
  - *905 nm filter versus 940 nm sources.* A 40 nm EEL filter centred on 907 nm ends at 927 nm, 8.5 nm below a 940 nm VCSEL at −40 °C; it would need to be at least $2\times(935.5-907.0)=57$ nm wide to reach it (61 nm if centred on 905 nm). A 20 nm VCSEL-type filter ends at 915 nm, 20 nm short. No 905 nm filter in the report's range passes 940 nm sources; the widest EEL filter of §C6(d′), about 50 nm, would end about 3.5 nm short.
  - *940 nm filter versus 905 nm sources.* A 10 nm filter starts at 935 nm, 8.4 nm above a 905 nm EEL at +105 °C; reaching it needs a filter at least $2\times(940-926.6)=27$ nm wide (the ≈26 nm of §C9), and reaching a 905 nm VCSEL at +105 °C needs 59 nm. A wide-field flash receiver whose filter must accept large angles of incidence (37 nm blue shift at 30°, §C6(d′)) is the one case in which 905 nm light could enter a 940 nm receiver; the §C9 victim is a scanned column receiver, which can keep its filter narrow.
  - *Within the 905 nm band*, a 20 nm VCSEL-type filter (895–915 nm) holds a 905 nm EEL source only while that emitter is between about −12 °C and +62 °C, so hot RoboSense M-platform and Huawei D2 emitters drift out of it; the 905 nm values below count them as in-band and are upper ends in that respect.
  - $f_{\rm band}$ for a 940 nm victim equals $s_{940}$, plus $s_U$ if the undisclosed units are at 940 nm: 0–0.28 for 2025 and 0.015–0.52 for H1 2026, i.e. **about 0.01–0.5**.
  - $f_{\rm band}$ for a 905 nm victim equals $s_{905}$, plus $s_U$ if the undisclosed units are at 905 nm: 0.67–0.955 for 2025 and 0.44–0.92 for H1 2026, i.e. **about 0.44–0.95**.
  - *Main lidars only* (if blind-spot flash units, with 8–30 m at 10%, are judged too weak at distance to count as §C6-class interferers): 2025, 905 nm 78–94%, 940 nm 0–17%, 1,550 nm 5.7%; H1 2026 (1,542,256 main units), 905 nm 52–85%, 940 nm 0–26%, 896-line (undisclosed) 5.5–15%, 1,550 nm 6.9–9.5%.
  - *Installed base.* The fleet within 100 m also contains the ≈2.2 M units of 2022–2024 (0.13 M, 0.57 M and 1.529 M), about 28–29% of the ≈7.7–7.9 M units installed by mid-2026 [E]. Those years' volume products (AT128, M1/M1P, Huawei D2/D3, Falcon) were 905 nm or 1,550 nm, so weighting by the installed base would lower the 940 nm share and raise the 905 nm share.

  **5. The wavelength of §C9's "my" unit, as the report describes it.** The §C6-class unit is the Sony IMX479 grid of §C5a and §C6 (0.05° macro-pixels, 520 lines, 20.8 µs columns, 10 shots per point, 25 Mpts/s), a 940 nm sensor (37% PDE at 940 nm; the §C5a table's design-wavelength row gives 940 nm for the IMX479). Item 3's bright-sun test uses the background of §C0 subsection 10.3, $1.83\times10^{8}$ s⁻¹, which §C7a defines as half the fully sunlit 940 nm, 10 nm-filter case of §C6(d). As described, the victim is therefore a 940 nm receiver behind a 10 nm filter.

  **Dependent numbers** (item 2, Eq. (123) with $p_1=4.17\times10^{-3}$; $f_{\rm ov}=0.25$–0.6 and $f_{\rm sd}=0.5$–1 unchanged; script `scripts/R8_band_shares.py`):

  | Victim | $f_{\rm band}$ | $F$ | Today, $n=3$ to 16 | Later, $n=10$ to 30 |
  |---|---|---|---|---|
  | Report as it stands | 0.5–0.9 | $0.25\times0.5\times0.5=0.0625$ to $0.6\times0.9\times1=0.54$ | 0.078–3.54% | 0.260–6.54% |
  | 940 nm | 0.01–0.5 | $0.25\times0.01\times0.5=0.00125$ to $0.6\times0.5\times1=0.30$ | $1-(1-0.00125p_1)^3=0.0016\%$ to $1-(1-0.30p_1)^{16}=1.98\%$ | 0.0052–3.69% |
  | 905 nm | 0.44–0.95 | $0.25\times0.44\times0.5=0.055$ to $0.6\times0.95\times1=0.57$ | 0.069–3.74% | 0.229–6.89% |

  - The item 2 heading's "today's 1.2–6.5% as much as the later 4–12%" are the fully overlapping rates of §C9 ($F=1$); they do not change.
  - Item 3 quotes $F=0.0625$–0.54 once ("scales all of these down in proportion"); it changes with the choice below. Item 3's absolute ghost rates, and the Net-effect bullet's $1.1\times10^{-5}$, are for fully overlapping traffic and do not change.
  - Grep found no other quotation of $f_{\rm band}$, 0.0625, 0.54, 0.08–3.5% or 0.26–6.5% in the report.

  **Needs decision (author):**
  1. *Victim wavelength.* As the report describes it, the §C6-class victim is a 940 nm receiver (part 5), which gives $f_{\rm band}\approx0.01$–0.5 and $F=0.00125$–0.30 (Option A below). Taking a 905 nm victim, the band of most units in service, keeps item 2 close to its present numbers ($F=0.055$–0.57, Option B) but makes item 3's bright-sun test inconsistent: at 905 nm behind 20–40 nm filters the background is $1.1\times10^{9}/(2.965\times10^{8})=3.7$ to $2.2\times10^{9}/(2.965\times10^{8})=7.4$ times the 940 nm value of §C6(d), so item 3's sunlight numbers would have to be redone.
  2. *Population weighting.* The ranges use 2025–H1 2026 installations. Weighting by the installed base, by main lidars only, or by a projected later mix (FTX, Robin E1X and the EM platform are ramping) are model choices; part 4 gives the data for the first two.
  3. *Undisclosed units.* About 17% (2025) and 27–33% (H1 2026) of installations have no published wavelength, and they set the upper half of the 940 nm range. A Huawei SL210 or Zeekr blind-spot teardown with the laser line, or a RoboSense EM4/EMX datasheet (gated behind a contact form on robosense.ai, not filled in), would narrow it.

  **Related findings outside this item (not proposed as edits):**
  - §B7.1 quotes a blind-spot share near 11% for H1 2026, against about 16% in 2025. NE Times' own monthly charts for Jan–Jun 2026 sum to 739,897 blind-spot units of 2,282,153, i.e. 32.4% (Huawei 382,424, Seyond 186,504, Zeekr 137,112, Hesai 29,510, RoboSense 4,347), and NE Times' 2025 chart separates only Huawei's and Zeekr's blind-spot units, not Seyond's Robin W side units on the ES8. The OFweek page among §B7.1's sources gives main lidars as about 89% and blind-spot units as 11% of H1 2026 and names NE Times' research arm as its source, a split that NE Times' monthly charts do not support. The Sohu report that §B7.1 cites for its 11% (said to cite Gasgoo) was not read here, and no Gasgoo main and blind-spot split for H1 2026 was found.
  - §C2's 1,550 nm share of ≈6.1% for 2025 divides Seyond's Falcon *shipments* (194.7k) by China's *installations* (3.21 M). On an installation basis it is about 4.5% (Gasgoo, $0.077\times0.586$) or 4.6% (NE Times); the ≈94–96% 9xx share still holds.
  - The Huawei blind-spot unit's and the Huawei 896-line unit's wavelengths, and the EM4 conflict, could be listed in Appendix 1, beside its existing Huawei 896-line and Zeekr entries.

- **Source:**
  - Hesai, *ATX User Manual*, doc. A12-en-260910 (10 Sep 2026), §1.5 Specifications, p. 14 (PDF p. 18): https://www.hesaitech.com/wp-content/uploads/2026/09/ATX_User_Manual_A12-en-260910.pdf — full text; spec pages rendered.
  - Hesai, *AT128P User Manual*, A02-en-260110 (10 Jan 2026), §1.5, p. 13 (PDF p. 17): https://www.hesaitech.com/wp-content/uploads/2026/01/AT128P_User_Manual_A02-en-260110.pdf — full text; spec page rendered.
  - Hesai, *FT120 User Manual*, F01-en-250110 (10 Jan 2025), §1.5, p. 16 (PDF p. 20): https://www.hesaitech.com/wp-content/uploads/2025/02/FT120_User_Manual_F01-en-250110.pdf ; *FTX_140 User Manual*, F04-en-260910, §1.4, p. 15 (PDF p. 18): https://www.hesaitech.com/wp-content/uploads/2026/09/FTX_140_User_Manual_F04-en-260910.pdf ; *FTX_180 User Manual*, F07-en-260510, §1.4, p. 15 (PDF p. 18): https://www.hesaitech.com/wp-content/uploads/2026/05/FTX_180_User_Manual_F07-en-260510.pdf — full texts; spec pages rendered.
  - Hesai, Q4 and FY2025 results (24 Mar 2026; ADAS 1,381,133 units in 2025), SEC Form 6-K exhibit 99.1: https://www.sec.gov/Archives/edgar/data/1861737/000110465926033591/tm269592d1_ex99-1.htm — read through a fetch; the FY2025 20-F could not be read (SEC refuses requests that carry no contact address, and none was added).
  - Gasgoo community (盖世汽车社区), "禾赛科技连发三大核心成果，ATX焕新版在手订单已超400万台" (24 Nov 2025; ATX nearly 1 M delivered since Q1 2025; AT128 + ATX about 2 M): https://i.gasgoo.com/news/70437733.html — page text.
  - Seyond, *Robin W1G LiDAR Specifications* (datasheet, Jan 2025): https://www.seyond.com/wp-content/uploads/2025/01/Seyond-Robin-W-Datasheet.pdf ; *Robin E1X LiDAR C-sample Datasheet* V3.0.0: https://www.seyond.com/wp-content/uploads/2025/03/Robin-E1X-LiDAR-C-sample_Datasheet_EN_Public_V3.0.0-2.pdf — full texts; page 1 of each rendered.
  - MarkLines (Chinese), "图达通为蔚来ES8提供'1+2'激光雷达组合方案" (25 Aug 2025): https://www.marklines.com/cn/news/331619 — page text.
  - RoboSense, *RS-LiDAR-M1 User Guide* (Dec 2021), Table 1, p. 4: https://cdn.robosense.cn/20211220200638_20760.pdf — full text; page rendered. RoboSense store, M1 Plus: https://store.robosense.ai/products/m1-plus ; RoboSense, MX product page: https://www.robosense.ai/en/IncrementalComponents/MX — page texts. RoboSense, *EM4-F User Manual* V3.1.0 (Dec 2025; no wavelength in its spec table, p. 10), distributor-hosted copy: https://www.generationrobots.com/media/robosense-em4-user-guide.pdf — full text; pages rendered.
  - RoboSense, *Interim results announcement for the six months ended June 30, 2025* (HKEX, 21 Aug 2025), p. 1: https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0821/2025082101017.pdf — full text; page rendered.
  - IT之家, "全球首款 1080 线超长距数字化激光雷达，国产 RoboSense EM4 发布" (7 Jan 2025): https://www.ithome.com/0/822/958.htm — page text. 证券时报e公司 via Sina, "全球唯一可量产！数字化EM平台全线规模交付" (9 Sep 2025; EMX batch deliveries from 9 Sep): https://finance.sina.com.cn/roll/2025-09-09/doc-infpxfwc3399823.shtml — page text.
  - Generation Robots, RoboSense EM4 listing and brochure copy (905 nm; brochure dated 21 Nov 2025 in its title): https://www.generationrobots.com/en/404442-robosense-em4-lidar.html ; https://www.generationrobots.com/media/robosense-em4-brochure.pdf . LidarSeek, RS-EMX listing (905 nm): https://lidarseek.com/product/robosense-emx — page texts; the brochure rendered. Both are secondary relays.
  - TechInsights, "Deep Dive Teardown of the Huawei 192 Line LiDAR L306 LiDAR Sensor" (public summary; 905 nm, AITO M9): https://www.techinsights.com/blog/deep-dive-teardown-huawei-192-line-lidar-l306-lidar-sensor — summary page only.
  - Sohu, "55图分析：华为激光雷达详细拆解和系统方案" (12 Apr 2024; D2 at 905 nm with EEL and SPAD): https://www.sohu.com/a/770979130_468661 — page text.
  - 鑫椤智驾 via Tencent News, Huawei lidar customers and product matrix (18 Jul 2025; Flash blind-spot unit 8 m at 10%, 120° × 90°, HiSilicon SPAD): https://news.qq.com/rain/a/20250718A07UUR00 — page text.
  - Huawei Qiankun, 896-line launch (4 Mar 2026; no wavelength): https://auto.huawei.com/cn/news/2026/2026-3-4-lidar ; ADS sensing page: https://auto.huawei.com/cn/ads/advanced-intelligent-sensing — page texts.
  - Raysees (睿熙科技), Zeekr 9X solid-state lidar VCSEL release (9 Jul 2025; no wavelength): https://www.rayseasc.com/news/%E7%9D%BF%E7%86%99%E5%BF%AB%E8%AE%AF-vcsel%E8%8A%AF%E7%89%87%E8%B5%8B%E8%83%BD%E6%9E%81%E6%B0%AA9x%E5%85%A8%E5%9B%BA%E6%80%81%E6%BF%80%E5%85%89%E9%9B%B7%E8%BE%BE/ — page text.
  - NE Times (NE时代), 雪岭, "26款激光雷达拆机分析——总结和展望" (Dec 2025; EM4, E1 and Robin E1X named as 940 nm; EM4 uses the IMX479; EMX volume production in 2026): https://www.ne-time.cn/web/article/37421 — article text and figures read.
  - NE Times, monthly installation charts (domestic retail basis, main and blind-spot units per supplier; chart images read): 2025 full year, https://www.ne-time.cn/web/article/37913 ; Dec 2025, https://www.ne-time.cn/web/article/37780 ; Jan–Feb 2026, https://www.ne-time.cn/web/article/38392 ; Mar 2026, https://www.ne-time.cn/web/article/38640 ; Apr 2026, https://www.ne-time.cn/web/article/38884 ; May 2026, https://www.ne-time.cn/web/article/39098 ; Jun 2026, https://www.ne-time.cn/web/article/39279 . The chart images were fetched from the WeChat image host because img.ne-time.cn did not resolve here. The Apr 2026 chart's Zeekr line prints 108,031 blind-spot units beside a total of 27,996; the total is used.
  - Gasgoo (盖世汽车研究院), "2025主雷达装机量出炉，禾赛问鼎第一" (11 Feb 2026; 3.386 M units, 2.756 M main, Hesai 114.3万 main at 41.5%): https://auto.gasgoo.com/news/202602/11I70446522C601.shtml ; "2026年一季度ADAS供应商装机量排行榜" (13 May 2026; 940,656 units by supplier, others 46,888): https://i.gasgoo.com/news/70457578.html — page texts.
- **Evidence tag:** [P] for the Hesai, Seyond and RoboSense M-platform wavelengths and RoboSense's H1 2025 volumes; [I] for Huawei's 192-line unit; [T] for the installation counts (NE Times, Gasgoo), EM4 and E1 at 940 nm, Huawei D2, and the ES8 fit; [S] for the distributor listings of EM4 and EMX at 905 nm; [U] for Huawei's blind-spot and 896-line units and Zeekr's units; [E] for the shares, bounds and $F$.
- **Confidence:** medium overall: high for the documented wavelengths (manuals and datasheets) and for the 905 nm share being the majority; medium for the shares, which rest on two trade-press trackers that agree on the Q1 2026 total within 0.4% but differ by up to 28% for one supplier (RoboSense); low for the upper half of the 940 nm range, which is set by units whose wavelength is undisclosed.
- **Proposed edit:**
  - Edit 1, the $f_{\rm band}$ bullet (one version for either option):
  - `old`:
    ```text
    *In-band share* $f_{\rm band}$, the share of foreign units that my receive filter passes: 0.5–0.9. 9xx-nm units are ≈94–96% of Chinese installations (§C2), but this report does not quantify their 905/940 nm split, so the range assumes my band holds half to most of them.
    ```
  - `new`:
    ```text
    *In-band share* $f_{\rm band}$, the share of foreign units that my receive filter passes: 0.01–0.5 for a 940 nm receiver and 0.44–0.95 for a 905 nm one. 9xx-nm units are ≈94–96% of Chinese installations (§C2), and most of them emit at 905 nm: Hesai's ATX and AT128, Huawei's 192-line unit, RoboSense's M platform and Seyond's Robin W make up about 67–78% of 2025 installations and 44–66% of H1 2026's [P/I/T/E]. Units documented at 940 nm (Hesai's FT120 and FTX, Seyond's Robin E1X) or reported there (RoboSense's E1 and its EM platform, whose sources conflict) make up about 0–11% and 1.5–19% [P/T/E]. Huawei's blind-spot and 896-line units and Zeekr's blind-spot units, about 17% and 27–33%, have no published wavelength [U]. The low end of each range puts every unit of undisclosed or conflicting wavelength in the other band, and the high end puts it in the receiver's band. Neither band leaks into the other through the filters assumed here (10 nm at 940 nm, 20–40 nm at 905 nm, §C6(d)): over −40 to +105 °C each laser line stays at least about 8 nm outside the other band's passband (§C9).
    ```
  - Edit 2, the product $F$ and the fractions (choose Option A or Option B):
  - `old`:
    ```text
    The product is $F=f_{\rm ov}f_{\rm band}f_{\rm sd}=0.25\times0.5\times0.5=0.0625$ to $0.6\times0.9\times1=0.54$, and Popko's ≈¼ overlap alone sits inside that range. With $F\,p_1$ in place of $p_1$ in Eq. (123), $1-(1-F\,p_1)^{n}$ gives **about 0.08–3.5% of points carrying at least one foreign shot before rejection today** ($n=3$ with $F=0.0625$, $n=16$ with $F=0.54$) and 0.26–6.5% later ($n=10$ and 30). Counting only single-scatter paths is right (Kim's power analysis).
    ```
  - `new` (Option A, 940 nm victim):
    ```text
    For a 940 nm receiver, the band whose sunlight background item 3 uses (§C6(d)), the product is $F=f_{\rm ov}f_{\rm band}f_{\rm sd}=0.25\times0.01\times0.5=0.00125$ to $0.6\times0.5\times1=0.30$, and Popko's ≈¼ overlap alone sits inside that range. With $F\,p_1$ in place of $p_1$ in Eq. (123), $1-(1-F\,p_1)^{n}$ gives **about 0.002–2.0% of points carrying at least one foreign shot before rejection today** ($n=3$ with $F=0.00125$, $n=16$ with $F=0.30$) and 0.005–3.7% later ($n=10$ and 30). A 905 nm receiver would see $F=0.055$–0.57, 0.07–3.7% today and 0.23–6.9% later. Counting only single-scatter paths is right (Kim's power analysis).
    ```
  - `new` (Option B, 905 nm victim):
    ```text
    For a 905 nm receiver, the band of most units in service, the product is $F=f_{\rm ov}f_{\rm band}f_{\rm sd}=0.25\times0.44\times0.5=0.055$ to $0.6\times0.95\times1=0.57$, and Popko's ≈¼ overlap alone sits inside that range. With $F\,p_1$ in place of $p_1$ in Eq. (123), $1-(1-F\,p_1)^{n}$ gives **about 0.07–3.7% of points carrying at least one foreign shot before rejection today** ($n=3$ with $F=0.055$, $n=16$ with $F=0.57$) and 0.23–6.9% later ($n=10$ and 30). A 940 nm receiver would see $F=0.00125$–0.30, 0.002–2.0% today and 0.005–3.7% later. Counting only single-scatter paths is right (Kim's power analysis).
    ```
  - Edit 3, item 3's quotation of $F$ (take the option chosen in Edit 2):
  - `old`:
    ```text
    The traffic factor $F=0.0625$–0.54 of item 2 scales all of these down in proportion.
    ```
  - `new` (Option A):
    ```text
    The traffic factor $F=0.00125$–0.30 of item 2 scales all of these down in proportion.
    ```
  - `new` (Option B):
    ```text
    The traffic factor $F=0.055$–0.57 of item 2 scales all of these down in proportion.
    ```
  - Needs decision: Option A follows the report's own description of the victim (part 5); Option B would also require item 3's bright-sun test to be redone at 905 nm (Needs decision, point 1).
- **Appendix 2 entry:**
  - `- Hesai, ATX user manual A12 (10 Sep 2026; §1.5, wavelength 905 nm): https://www.hesaitech.com/wp-content/uploads/2026/09/ATX_User_Manual_A12-en-260910.pdf`
  - `- Hesai, AT128P user manual A02 (10 Jan 2026; §1.5, wavelength 905 nm): https://www.hesaitech.com/wp-content/uploads/2026/01/AT128P_User_Manual_A02-en-260110.pdf`
  - `- Hesai, FT120 user manual F01 (10 Jan 2025; §1.5, 940 nm) and FTX_140 / FTX_180 user manuals F04 / F07 (§1.4, 940 nm): https://www.hesaitech.com/wp-content/uploads/2025/02/FT120_User_Manual_F01-en-250110.pdf ; https://www.hesaitech.com/wp-content/uploads/2026/09/FTX_140_User_Manual_F04-en-260910.pdf ; https://www.hesaitech.com/wp-content/uploads/2026/05/FTX_180_User_Manual_F07-en-260510.pdf`
  - `- Seyond, Robin W1G datasheet (905 nm): https://www.seyond.com/wp-content/uploads/2025/01/Seyond-Robin-W-Datasheet.pdf ; MarkLines, NIO ES8 with one Falcon and two Robin W (25 Aug 2025): https://www.marklines.com/cn/news/331619`
  - `- RoboSense, MX page (inherits the M platform's optical path and optoelectronic devices): https://www.robosense.ai/en/IncrementalComponents/MX ; 2025 interim results (H1 2025 ADAS ≈220,500 units): https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0821/2025082101017.pdf`
  - `- RoboSense EM4 at 940 nm (IT之家 on the 7 Jan 2025 launch): https://www.ithome.com/0/822/958.htm ; at 905 nm (distributor listings): https://www.generationrobots.com/en/404442-robosense-em4-lidar.html ; EMX at 905 nm (retailer listing): https://lidarseek.com/product/robosense-emx ; EMX batch deliveries from 9 Sep 2025 (证券时报 via Sina): https://finance.sina.com.cn/roll/2025-09-09/doc-infpxfwc3399823.shtml`
  - `- Huawei Flash blind-spot lidar parameters, no wavelength (鑫椤智驾 via Tencent News, 18 Jul 2025): https://news.qq.com/rain/a/20250718A07UUR00`
  - `- NE Times monthly lidar installations by supplier, main and blind-spot (2025; Jan–Feb, Mar, Apr, May, Jun 2026): https://www.ne-time.cn/web/article/37913 ; https://www.ne-time.cn/web/article/38392 ; https://www.ne-time.cn/web/article/38640 ; https://www.ne-time.cn/web/article/38884 ; https://www.ne-time.cn/web/article/39098 ; https://www.ne-time.cn/web/article/39279`
  - `- Gasgoo, 2025 main-lidar installations (2.756 M of 3.386 M; Hesai 114.3万): https://auto.gasgoo.com/news/202602/11I70446522C601.shtml ; Q1 2026 ADAS supplier ranking: https://i.gasgoo.com/news/70457578.html`
  - none for the TechInsights Huawei 192-line teardown, the Sohu Huawei teardown notes, the NE Times 26-teardown summary, the RS-LiDAR-M1 user guide, the M1 Plus store page, the Robin E1X datasheet and the Huawei 896-line launch, which Appendix 2 already lists.
