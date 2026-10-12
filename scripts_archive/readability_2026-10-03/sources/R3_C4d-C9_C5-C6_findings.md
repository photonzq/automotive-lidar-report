# Round 4 source findings: R3_C4d-C9_C5-C6

Read on 5 Oct 2026. Every `old` string below was copied from the report as of sha 51d60fa27199 (after the move of the Fastree3D timeline to §C3a and the equation renumbering) and checked again against sha 4e2afc5d7428; each occurs exactly once (check script `scripts/R3_check_old_strings.py`).

---

## R3_C4d-C9_C5-C6-01

- **Question:** How many lidars were fitted in China before 2024, and what source supports the ≈350 M car fleet behind the 2% fleet share?
- **Answer:**
  - **Before 2024 the volumes were small.** The report's 2024 and 2025 totals (1.529 M and 3.21 M) are ResearchInChina's (佐思汽研) series: 152.9万 (1.529 M) units in 2024, +245.4%, on 6.0% of new cars [MR]. Its 2023 total follows as $152.9/(1+2.454)=44.3$万 units; its chart puts 2022 near 13.7万 and labels 2021 at 0.91万 (chart values, not printed) [MR/E]. GGAI (高工智能汽车研究院) counts factory-standard lidars on passenger cars sold in China (exports and imports excluded) and also the cars that carry them:

    | Year | Units | Cars | Units per car [E] |
    |---|---|---|---|
    | 2021 | ≈0.79万 [E] | ≈0.41万 [E] | — |
    | 2022 | 12.99万 (+1,544%) | 11.18万 (+2,627%) | $12.99/11.18=1.16$ |
    | 2023 | 57.09万 (+341%) | 44.03万 | $57.09/44.03=1.30$ |
    | 2024 | "over 150万" | 137.37万 (+212%) | ≈1.1 |
    | 2025 | 324.84万 (+112%; 11.15% of new cars) | 256.28万 (+86.5%) | $324.84/256.28=1.27$ |

    The 2021 values follow from the 2022 growth rates: $12.99/16.443=0.79$万 units and $11.18/27.268=0.41$万 cars [E]. All of GGAI's ratios lie at or below the bottom of the 1.3–1.6 units per car assumed in §F2.
  - **Stock of lidar cars.** GGAI's car counts sum to $0.41+11.18+44.03+137.37+256.28=449.3$万, i.e. about 4.5 M at end-2025 [E]. Adding the report's assumed 4–5 M units for 2026 at 1.27 units per car adds $4/1.27=3.15$ to $5/1.27=3.94$ M cars, so the stock is about $4.49+3.15=7.6$ M to $4.49+3.94=8.4$ M at end-2026 [E]. GGAI's own forecast of more than 4.4 M lidar cars in 2026 would give about 8.9 M [MR].
  - **Fleet.** The Ministry of Public Security counts automobiles (汽车, including trucks and buses): 3.53亿 (353 M) at end-2024, which is the report's ≈350 M; 3.66亿 (366 M) at end-2025; and 3.71亿 (371 M) at 30 June 2026 [P]. New-energy vehicles were 31.40 M, 43.97 M and 48.97 M at the same dates. The MPS releases give no passenger-car subtotal; the National Bureau of Statistics, using MPS data, gives 366.11 M civil automobiles at end-2025, of which 6.81 M three-wheelers and low-speed trucks and 197.73 M sedans [P].
  - **Share.** $7.6/371=2.0\%$ to $8.4/371=2.3\%$ of the mid-2026 automobile fleet: about 2%, as the report says, but on a sourced denominator [E].
  - **Related (outside this item):** in §B1, the 3.21 M for 2025 is ResearchInChina's, while the 2.756 M main lidars and the 985k for Q1 2026 appear to be Gasgoo's (盖世汽车研究院), whose own 2025 total is 3.386 M; GGAI's is 3.248 M. One sentence should not mix the providers (not edited here).
- **Source:**
  - GGAI (高工智能汽车研究院), on its own Sohu account: "「微报告」激光雷达前装'成色'", 6 Mar 2023 (2022 data), https://www.sohu.com/a/650045051_121136454 ; 2023 data, 23 Apr 2024, https://www.sohu.com/a/773626453_121136454 ; 2024 data, 17 Mar 2025, https://www.sohu.com/a/872160040_121136454 . 2025 units, relayed 17 Mar 2026, https://news.qq.com/rain/a/20260317A0627W00 ; 2025 cars, relayed 7 May 2026, https://k.sina.com.cn/article_7857141524_1d452771401902a7gg.html . Page texts read.
  - ResearchInChina (佐思汽研, posting as 佐思产研), "激光雷达研究：性能提升、成本下沉、应用拓展，迎接爆发增长", eefocus, 26 Mar 2025, https://www.eefocus.com/article/1819136.html — text read; its 2022–2024 chart read for 2022.
  - Ministry of Public Security statistics, as published by gov.cn and Xinhua: "全国机动车保有量达4.53亿辆 驾驶人达5.42亿人", 18 Jan 2025 (source line: MPS website), https://www.gov.cn/lianbo/bumen/202501/content_6999762.htm ; "2025年全国机动车达4.69亿辆 驾驶人达5.59亿人", 26 Jan 2026 (Xinhua), https://www.gov.cn/lianbo/202601/content_7056115.htm ; "2026年上半年全国机动车达4.76亿辆 驾驶人达5.67亿人…", 14 Jul 2026 (source: MPS Traffic Management Bureau), https://www.news.cn/politics/20260714/6dc71608fee14901a0b25a9351078267/c.html — texts read. The MPS's own pages refused automated requests.
  - National Bureau of Statistics, "中华人民共和国2025年国民经济和社会发展统计公报", 28 Feb 2026, https://www.stats.gov.cn/sj/zxfbhjd/202602/t20260228_1962662.html — vehicle paragraph read.
- **Evidence tag:** [MR] for the installation series; [P] for the MPS fleet (and NBS); [E] for the sums and ratios.
- **Confidence:** high for the fleet and for GGAI's printed 2022–2025 figures; medium for 2021 and the chart-read ResearchInChina 2022 value.
- **Proposed edit:**
  - `old`:
    ```text
    About 3.2–3.3 M lidar units were installed in 2025 (3.21 M in §B1; ≈3.32 M per NE Times in §B7.1), at roughly 1.3–1.6 units per car (§F2). Lidar cars are therefore probably only a few percent of China's car fleet in 2026 [E]: 2025's installations correspond to $3.21\ {\rm M}/1.6\approx2.0$ M to $3.32\ {\rm M}/1.3\approx2.6$ M lidar cars. Adding 2024 (1.53 M units, §B1) and 2026 (985k units in Q1, §B1, and an assumed 4–5 M for the whole year) gives $1.53+3.21+4\approx8.7$ M to $1.53+3.32+5\approx9.9$ M units installed in 2024–2026, i.e. $8.7/1.6\approx5.5$ M to $9.9/1.3\approx7.6$ M lidar cars. Installations before 2024, not quantified here, add to this, so the stock is roughly 6–8 M lidar cars by end-2026. That is about 2% ($7\ {\rm M}/350\ {\rm M}$) of a Chinese car fleet assumed at ≈350 M [U].
    ```
  - `new`:
    ```text
    About 3.2–3.3 M lidar units were installed in 2025 (3.21 M in §B1; ≈3.32 M per NE Times in §B7.1). GGAI (高工智能汽车研究院), which counts cars as well as units, puts 2025 at 3.25 M units on 2.56 M new cars, i.e. $324.84/256.28\approx1.27$ units per car, below the 1.3–1.6 assumed in §F2 [MR/E]. Earlier years add little: GGAI counts 0.11 M lidar cars in 2022 and 0.44 M in 2023 (0.13 M and 0.57 M units), about 4,000 in 2021 and 1.37 M in 2024 [MR/E], so about $0.004+0.112+0.440+1.374+2.563\approx4.5$ M lidar cars were on China's roads at end-2025 [E]. Adding 2026 (985k units in Q1, §B1, and an assumed 4–5 M for the whole year) at 1.27 units per car gives $4.5+4/1.27\approx7.6$ M to $4.5+5/1.27\approx8.4$ M lidar cars by end-2026 [E]. That is about 2% ($7.6/371\approx2.0\%$ to $8.4/371\approx2.3\%$) of the 371 M automobiles registered in China at 30 June 2026, a count that includes trucks and buses [P, Ministry of Public Security], so lidar cars remain only a few percent of the fleet [E].
    ```
- **Appendix 2 entry:**
  - `- GGAI (高工智能汽车研究院), passenger-car lidar fitment in cars and units, 2022–2025: https://www.sohu.com/a/650045051_121136454 ; https://www.sohu.com/a/773626453_121136454 ; https://www.sohu.com/a/872160040_121136454 ; https://news.qq.com/rain/a/20260317A0627W00 ; https://k.sina.com.cn/article_7857141524_1d452771401902a7gg.html`
  - `- ResearchInChina (佐思汽研), 2022–2024 lidar installations (1.529 M in 2024, 6.0%): https://www.eefocus.com/article/1819136.html`
  - `- Ministry of Public Security, vehicle fleet at end-2024, end-2025 and 30 Jun 2026 (via gov.cn and Xinhua): https://www.gov.cn/lianbo/bumen/202501/content_6999762.htm ; https://www.gov.cn/lianbo/202601/content_7056115.htm ; https://www.news.cn/politics/20260714/6dc71608fee14901a0b25a9351078267/c.html`

---

## R3_C4d-C9_C5-C6-02

- **Question:** Is there a source for the 25 mW/π upper end of thermo-optic silicon phase-shifter power, and hence for the 25 W total for 1,000 elements?
- **Answer:** Yes. Harris *et al.* (2014) measured a compact thermo-optic phase shifter (a doped-silicon resistive heater, current flowing across a ridge waveguide) made in a standard CMOS silicon-on-insulator process with oxide cladding and two metal layers. It is 61.6 µm long and needs $P_\pi=24.77\pm0.43$ mW, with $V_\pi=4.36$ V, a −3 dB modulation bandwidth of $130.0\pm5.59$ kHz (time constant $\tau=2.69$ µs) and an insertion loss of $0.23\pm0.13$ dB over 21 devices on an 8-inch wafer. Their Table I compares earlier thermo-optic shifters: 0.49 mW/π for a 1,000 µm TiN heater with air cladding ($\tau=144$ µs), 10.6–20 mW/π for Ti and NiSi heaters, and 46–235 mW/π for long metal heaters in oxide. The speed–power product is similar for the fast and the slow device ($P_\pi\tau=66.9$ against 70.5 mW·µs), which is the trade the report describes. So about 25 mW/π is what a fast, compact, oxide-clad heater without thermal isolation needs; it is a sound upper end for the report's range (older long metal heaters exceed it). The total follows as $N\times P_\pi$ at a mean phase of about $\pi$: $1{,}000\times24.77\ {\rm mW}=24.8\ {\rm W}\approx25$ W [E]. The same paper shows a shifter shorter than the report's "about 100–200 µm", so the edit widens that range to about 60–200 µm.
- **Source:** N. C. Harris, Y. Ma, J. Mower, T. Baehr-Jones, D. Englund, M. Hochberg and C. Galland, "Efficient, compact and low loss thermo-optic phase shifter in silicon", *Optics Express* 22(9), 10487–10493 (2014), https://doi.org/10.1364/OE.22.010487 (open access). Read in full as the arXiv version, https://arxiv.org/abs/1410.3616 (v1, 14 Oct 2014): abstract and introduction on p. 1, Table I on p. 2.
- **Evidence tag:** [I]
- **Confidence:** high — a peer-reviewed measurement over 21 devices, read in the paper's own table.
- **Proposed edit:**
  - `old`:
    ```text
    are short (about 100–200 µm) but draw about 0.1–25 mW per $\pi$ of phase shift each. Heaters with trenches or undercuts reach 0.14 mW/π but respond in 200–300 µs, while the thermal shifters of MIT's 50-element array need 13 mW/π (§C10.2b); the 25 mW/π upper end is unverified [U].
    ```
  - `new`:
    ```text
    are short (about 60–200 µm) but draw about 0.1–25 mW per $\pi$ of phase shift each. Heaters with trenches or undercuts reach 0.14 mW/π but respond in 200–300 µs, while the thermal shifters of MIT's 50-element array need 13 mW/π (§C10.2b). The upper end is a compact, fast heater without thermal isolation: a 61.6 µm doped-silicon heater in a standard oxide-clad CMOS process needs 24.77 mW/π at a 130 kHz modulation bandwidth [I, Harris *et al.*, *Opt. Express* 22, 10487 (2014)].
    ```
- **Appendix 2 entry:** `- Harris *et al.*, compact thermo-optic Si phase shifter (61.6 µm, 24.77 mW/π, 130 kHz), *Opt. Express* 22, 10487 (2014): https://doi.org/10.1364/OE.22.010487 (open access; arXiv: https://arxiv.org/abs/1410.3616)` (group: *OPA devices, reviews and receive-side analysis*).

---

## R3_C4d-C9_C5-C6-03

- **Question:** In the InnovizOne series-production datasheet, which of the 60 m and 75 m ranges outside the ROI is native and which uses pixel summation?
- **Answer:** 60 m is native and 75 m uses pixel summation. Both are 10%-reflectivity ranges outside the 20° × 8° region of interest, in the datasheet's "Eagle" configuration (115° × 15° field, 15 frames/s, 160 scanned lines, 250 m maximum range). The full table: inside the ROI 110 m native (0.1° × 0.1°) and 140 m with summation (0.2° × 0.2°) at 10%, and 180 m and 230 m at 50%; outside the ROI 60 m native and 75 m with summation at 10%, and 120 m and 155 m at 50%. The "Falcon" configuration (115° × 25°, 10 frames/s, 256 lines, 190 m maximum, no ROI) gives 80 m native and 100 m with summation at 10%. Note 1 defines long-range detection as 20 klux ambient light with 90% true positives and a 5% false-alarm rate per pixel; note 2 says pixel summation mode increases detection range.
- **Source:** Innoviz Technologies, "InnovizOne — Series Production Unit, Automotive-Grade LiDAR" datasheet, © 2023 (PDF metadata and file name dated 18 Apr 2023), p. 2, "Optical performance" table and notes 1–2; full 4-page PDF read (distributor-hosted copy): https://levelfivesupplies.com/wp-content/uploads/2023/08/InnovizOne-Series-Production-Datasheet-18.04.2023.pdf
- **Evidence tag:** [P]
- **Confidence:** high — read directly from the datasheet's table.
- **Proposed edit:**
  - `old`:
    ```text
    InnovizOne: native 10% range 110 m inside its 20° × 8° ROI (140 m with pixel summation), 60/75 m outside, at 20 klx [P]
    ```
  - `new`:
    ```text
    InnovizOne (Eagle configuration): native 10% range 110 m inside its 20° × 8° ROI (140 m with pixel summation) and 60 m native (75 m with summation) outside it, at 20 klx with detection defined as 90% true positives and 5% false alarms per pixel [P]
    ```
- **Appendix 2 entry:** `- InnovizOne series-production datasheet (Apr 2023; Eagle and Falcon configurations, native and pixel-summation ranges at 20 klx): https://levelfivesupplies.com/wp-content/uploads/2023/08/InnovizOne-Series-Production-Datasheet-18.04.2023.pdf` (group: *Additional verification sources*, next to the InnovizTwo entries).

---

## R3_C4d-C9_C5-C6-04

- **Question:** How do the ATX's "17 SiPM dies × 4 channels" (68) and its "64 physical channels" reconcile?
- **Answer:** No public source supports "× 4 channels", so the 68 should not stand. What the public record shows:
  - **17 SiPM dies.** A May 2025 Chinese trade article, relaying a teardown of the mass-produced ATX, reports 17 SiPM chip modules stacked on the receiver board (and 16 on the AT128, one per transmitter module) [T]. It gives no channel count per die.
  - **64 physical channels.** NE Times' 26-teardown summary (Dec 2025) says the ATX halved the AT128's physical transmit–receive channels from 128 to 64 and reached a higher "equivalent" line count by system design (it cites Hesai patent CN119199894A) [T].
  - **Hesai's own manual agrees with 64.** The ATX_S01 user manual (A07, May 2026) lists 116 output channels: channels 1–64 are "normal channels" and 65–116 "super-resolution channels" [P].
  - **Nothing shows four channels per die.** The TechInsights partial teardown published by Electronics360 (29 Aug 2025) lists the main- and motor-board ICs but no SiPM count. A close-up of the ATX receiver in the NE Times article shows each SiPM die with one undivided microcell array and four bond pads, of which two are wire-bonded (the other two show only probe marks), which does not by itself show four channels.
  - Arithmetic: $17\times4=68\neq64$, while $64/17=3.8$ is not an integer. A split such as $16\times4=64$ receiving channels plus one die with another role would close the count, but nothing public shows it [U]. The die-level report (TechInsights DDT-2505-806) is paywalled; its product page returns "Page not found".
  - **Variant caveat (see also item 11).** These counts describe the ATX in series production since Q1 2025. The 256-line, 3.84 Mpts/s, 230 m figures on Hesai's product page are the "flagship configuration" of the ATX version Hesai announced on 24 Nov 2025 with its Fermi C500 controller, for delivery from April 2026 [P]; Hesai's footnote says production parameters may differ by customization. Its physical channel count is not public.
- **Source:**
  - 快科技 (MyDrivers), "揭秘禾赛激光雷达第四代芯片架构" (author cici), 23 May 2025, https://news.mydrivers.com/1/1049/1049493.htm — full text read: "17个SiPM小芯片模组" on the ATX PCBA; 16 on the AT128.
  - NE Times (NE时代), 雪岭飞花, "雪岭 · 26款激光雷达拆机分析——总结和展望", updated 22 Dec 2025, https://www.ne-time.cn/web/article/37421 — full text read, Hesai section ("收发物理通道减少了一半（从128个降至64个）") and the ATX receiver close-up in the detector section (image file read).
  - Hesai, *ATX_S01 Hybrid Solid-State Lidar User Manual*, doc version A07-en-260520, §1.3 "Channel distribution" (printed p. 12, Figure 4 and its note) and §1.4 "Specifications" (printed p. 13), https://www.hesaitech.com/wp-content/uploads/2026/05/ATX_S01_User_Manual_A07-en-260520.pdf — full PDF, pages rendered and read.
  - Hesai, "禾赛重磅发布自研RISC-V激光雷达主控芯片费米C500，256线ATX升级焕新", 24 Nov 2025, https://www.hesaitech.com/cn/news/1384 — full text read (ATX mass production from Q1 2025, nearly 1 M delivered; 256-line flagship configuration, 0.08° × 0.05°, 230 m at 10%, 3.84 M points/s; deliveries from April 2026; footnote 7).
  - TechInsights, "TechInsights Teardown: Hesai ATX Lidar", Electronics360, 29 Aug 2025, https://electronics360.globalspec.com/article/22673/techinsights-teardown-hesai-atx-lidar — full page read; no SiPM count.
  - Not accessible: TechInsights DDT-2505-806 (paywalled).
- **Evidence tag:** [T] for the 17 dies and the 64 physical channels; [P] for the 64 + 52 channel split; [U] for any die-to-channel mapping.
- **Confidence:** medium — two independent trade sources and Hesai's manual agree on 64, but the die-level mapping sits behind a paywall.
- **Proposed edit** (three cells carry the 17 × 4 figure; the §C5 cell and the §C4b "64 physical channels" sentence are under item 11):
  - Edit 1, §C8.1 table, SiPM row:
    - `old`:
      ```text
      ATX: **17 SiPM dies × 4 channels** [T]
      ```
    - `new`:
      ```text
      ATX: **17 SiPM dies** [T, teardown relayed by MyDrivers] for **64 physical channels** [T, NE Times]; how the channels map onto the dies is not public [U]
      ```
  - Edit 2, §C4b architecture table, "Examples" row:
    - `old`:
      ```text
      **ATX (17 SiPM dies × 4 channels)**
      ```
    - `new`:
      ```text
      **ATX (17 SiPM dies, 64 physical channels)**
      ```
  - Edit 3, §D1 dependency table, SiPM row:
    - `old`:
      ```text
      **ATX: 17 SiPM dies × 4 channels, vendor not public** (in paywalled TechInsights DDT-2505-806)
      ```
    - `new`:
      ```text
      **ATX: 17 SiPM dies for 64 physical channels, vendor not public** (die-level detail in paywalled TechInsights DDT-2505-806)
      ```
- **Appendix 2 entry:**
  - `- NE Times, 26-teardown summary (ATX: 64 physical channels, half the AT128's 128): https://www.ne-time.cn/web/article/37421` — the URL is already listed as "NE Times, 26-teardown summary"; if kept as is, write "none".
  - `- Hesai ATX_S01 user manual A07 (20 May 2026; 116 channels = 64 normal + 52 super-resolution; 1-D rotating mirror; 10 Hz): https://www.hesaitech.com/wp-content/uploads/2026/05/ATX_S01_User_Manual_A07-en-260520.pdf`
  - `- Hesai, Fermi C500 and 256-line ATX (24 Nov 2025; flagship configuration, deliveries from April 2026): https://www.hesaitech.com/cn/news/1384`
  - `- TechInsights, partial ATX teardown (Electronics360, 29 Aug 2025): https://electronics360.globalspec.com/article/22673/techinsights-teardown-hesai-atx-lidar`
  - The MyDrivers summary is already listed ("Hesai ATX teardown summary (MyDrivers)"): none.

---

## R3_C4d-C9_C5-C6-05

- **Question:** What date does the ATX S01 user manual A07 carry?
- **Answer:** 20 May 2026. The cover reads "Doc version: A07-en-260520" (year-month-day), the PDF was created on 29 May 2026, and it is filed under Hesai's uploads for May 2026. The manual has no revision-history table and nothing in it says February 2026, so "Feb 2026" is a slip; May 2026 matches §C3b, the §E9 sources and Appendix 1. The quoted wording checks out: "Scanning method: 1-D rotating mirror (hybrid solid-state)" and "Frame rate: 10 Hz" (§1.4, printed p. 13); "each mirror surface" (point-rate note, printed p. 15); and a parity flag whose even frames sweep "in the direction of increasing azimuth" and odd frames back (printed p. 53).
- **Source:** Hesai, *ATX_S01 Hybrid Solid-State Lidar User Manual*, Classification C0 (Public), doc version A07-en-260520: cover (PDF p. 1), §1.4 (printed p. 13), §1.4 point-rate note (printed p. 15), §3.1 point-cloud packet tail (printed p. 53); full 97-page PDF read where cited: https://www.hesaitech.com/wp-content/uploads/2026/05/ATX_S01_User_Manual_A07-en-260520.pdf
- **Evidence tag:** [P]
- **Confidence:** high — the document version string is printed on the cover.
- **Proposed edit:**
  - `old`:
    ```text
    The Feb 2026 manual calls it a "1-D rotating mirror (hybrid solid-state)", refers to more than one mirror surface and lists 10 Hz [P, manual A07].
    ```
  - `new`:
    ```text
    The ATX S01 user manual (A07, May 2026, §E9) calls it a "1-D rotating mirror (hybrid solid-state)", refers to more than one mirror surface and lists 10 Hz [P].
    ```
- **Appendix 2 entry:** `- Hesai ATX_S01 user manual A07 (20 May 2026; 116 channels = 64 normal + 52 super-resolution; 1-D rotating mirror; 10 Hz): https://www.hesaitech.com/wp-content/uploads/2026/05/ATX_S01_User_Manual_A07-en-260520.pdf` (same entry as item 04; add once).

---

## R3_C4d-C9_C5-C6-06

- **Question:** What frame rate does RoboSense specify for the M1, and what does it change in subsection 2(a), panel (d) and the 0.3–0.94 kHz range?
- **Answer:** The series-production M1 runs at **10 Hz**. RoboSense's RS-LiDAR-M1 User Guide (rev. 1.7, 3 Dec 2021) gives a frame rate of 10 Hz, about 750,000 points/s in single-return mode (1,500,000 dual), 120° × 25° and an average angular resolution of 0.2° × 0.2°. The M1 Plus store page also gives 10 Hz, with 787,500 points/s. The 15 Hz comes from RoboSense's launch release of 2 Jan 2020 for the pre-series M1 (which also gives the 125 laser beams): it says the frame rate "is increased to 15Hz". RoboSense's GAZE release of 29 Jun 2021 treats 10 Hz as the normal rate: GAZE raises it "from 10Hz to 20Hz (or higher)" for traffic-jam driving and, on the highway, raises the ROI's vertical resolution from 0.2° to 0.1°.
  - Points per line at 10 Hz: M1, $750{,}000/(125\times10)=600$, i.e. $120°/600=0.20°$, matching the 0.2° average horizontal resolution; M1 Plus, $787{,}500/(125\times10)=630$, i.e. $0.19°$ [E].
  - Eq. (69) with $N_{\rm lines}=125$, $f_{\rm frame}=10$ Hz and $N_{\rm par}=1$ per module: $S=125\times10/1=1{,}250$ sweeps/s, so $f_{\rm mirror}=S/2=625$ Hz $\approx0.63$ kHz [E].
  - Against a one-axis unit's 10 sweeps/s: $1{,}250/10=125$ [E]. The range of resonant fast-axis frequencies for the products in subsection 3 becomes 0.30–0.63 kHz (InnovizOne 0.30–0.32 kHz).
  - The 1.2–1.3 kHz rating of the module mirror [I] gives $2\times1{,}200=2{,}400$ to $2\times1{,}300=2{,}600$ sweeps/s, i.e. 125 lines at $2{,}400/125=19.2$ to $2{,}600/125=20.8$ frames/s: it matches the 20 Hz GAZE mode, $125\times20/2=1{,}250$ Hz. At 10 Hz the same mirror would sweep each line about twice, room for the ROI densification that GAZE describes [E].
  - The figure script `build/figures/mechanical_scanning_limits.py` (line 142) holds the M1 marker as `("M1 (1 beam per module, teardown)", 125, 15, 1)`; panel (d) needs 10 in place of 15, which moves the marker to 1,250 sweeps/s (not edited here; outside the sources folder).
- **Source:**
  - RoboSense, *RS-LiDAR-M1 User Guide*, Executive Standard Q/RS 001-2021, revision history p. I (rev. 1.7, 2021-12-03) and Table 1 "Product Specifications", p. 1 (PDF p. 4), https://cdn.robosense.cn/20211220200638_20760.pdf — PDF pages rendered and read.
  - RoboSense, "RoboSense 125-laser beam solid-state LiDAR: RS-LiDAR-M1 is officially on sale priced at \$1,898", 2 Jan 2020, as posted by its PR agency: http://www.thomas-pr.com/robosense/robosensem1releaseces2020.html — full text read.
  - RoboSense, "RoboSense Unveils The Smart 'GAZE' Function Of Its RS-LiDAR-M1", Business Wire, 29 Jun 2021, https://www.businesswire.com/news/home/20210629005665/en/ — full text read.
  - RoboSense store, M1 Plus product page (specification table: 10 Hz; 787,500 pts/s single return), https://store.robosense.ai/products/m1-plus — read 5 Oct 2026.
- **Evidence tag:** [P]
- **Confidence:** high — RoboSense's own user guide and product page state 10 Hz, and the arithmetic closes on the published point rates.
- **Proposed edit** (four sentences use the 15 Hz figure):
  - Edit 1, §C4d 2(a):
    - `old`:
      ```text
      RoboSense M1 (125 lines at 15 Hz [P]): each of its five modules carries one laser (a teardown confirms one laser per module [I]) and scans every line of its own horizontal tile, so that $N_{\rm par}=1$ per tile in Eq. (69), the mirror makes $S=125\times15/1=1{,}875$ sweeps/s, a resonant fast axis near $f_{\rm mirror}=S/2=0.94$ kHz.
      ```
    - `new`:
      ```text
      RoboSense M1 (125 lines at 10 Hz [P, user guide]; RoboSense's January 2020 launch release gave 15 Hz for the pre-series unit): each of its five modules carries one laser (a teardown confirms one laser per module [I]) and scans every line of its own horizontal tile, so that $N_{\rm par}=1$ per tile in Eq. (69), the mirror makes $S=125\times10/1=1{,}250$ sweeps/s, a resonant fast axis near $f_{\rm mirror}=S/2=0.63$ kHz. The point rate fits: $750{,}000/(125\times10)=600$ points per line, one every 0.2° over 120° [P/E].
      ```
  - Edit 2, §C4d introduction:
    - `old`:
      ```text
      1,875 sweeps/s for the RoboSense M1
      ```
    - `new`:
      ```text
      1,250 sweeps/s for the RoboSense M1
      ```
  - Edit 3, §C4d 2(a), last bullet:
    - `old`:
      ```text
      $1{,}875/10\approx190$ for the M1
      ```
    - `new`:
      ```text
      $1{,}250/10=125$ for the M1
      ```
  - Edit 4, §C4d subsection 3:
    - `old`:
      ```text
      which gives 0.3–0.94 kHz for the products above. For the M1 that is 0.94 kHz, while the maker of its module mirror rates the fast axis at 1.2–1.3 kHz [I].
      ```
    - `new`:
      ```text
      which gives 0.30–0.63 kHz for the products above. For the M1 that is 0.63 kHz at its 10 Hz frame rate, about half the 1.2–1.3 kHz at which the maker of its module mirror rates the fast axis [I]; that rating matches the 20 Hz to which the M1's GAZE function can switch ($125\times20/2=1{,}250$ Hz) [P/E].
      ```
- **Appendix 2 entry:**
  - `- RoboSense RS-LiDAR-M1 user guide (rev. 1.7, Dec 2021; 10 Hz, ≈750,000 pts/s): https://cdn.robosense.cn/20211220200638_20760.pdf`
  - `- RoboSense M1 launch release (2 Jan 2020; 125 beams, 15 Hz for the pre-series unit): http://www.thomas-pr.com/robosense/robosensem1releaseces2020.html`
  - `- RoboSense GAZE release (29 Jun 2021; 10 Hz to 20 Hz, ROI 0.2° to 0.1°): https://www.businesswire.com/news/home/20210629005665/en/`
  - The M1 Plus store page is already in the §C4d sources line but not in Appendix 2: `- RoboSense M1 Plus store page (10 Hz; 787,500 pts/s): https://store.robosense.ai/products/m1-plus`

---

## R3_C4d-C9_C5-C6-07

(The Fastree3D timeline and its assessment now sit in §C3a, subsection 2; their wording is unchanged.)

- **Question:** What is the nominal value of Fastree3D's shares, what did each loan-to-equity conversion create, and which exchange rate turns the \$7.67 M price into francs?
- **Answer:**
  - **Nominal value.** Every capital entry and SOGC notice gives registered shares ("actions nominatives") of CHF 1, with transfer restrictions; the CHF 429,444 of capital is 429,444 shares [P]. The [U] on "CHF 1 nominal" can go.
  - **The six conversions** (each a capital increase paid "par compensation de créances", by setting off claims against the company), with the price per share as claims divided by shares issued [P; E arithmetic]:

    | Statutes (decision) | SOGC notice (date, ID) | Claims set off, CHF | Shares issued | Price per share, CHF |
    |---|---|---|---|---|
    | 24 Oct 2014 | 5 Nov 2014, 1805463 | 170,000 | 34,000 | $170{,}000/34{,}000=5.00$ |
    | 20 Nov 2015 | 8 Dec 2015, 2526843 | 82,000 | 16,400 | $82{,}000/16{,}400=5.00$ |
    | 18 Nov 2016 | 6 Dec 2016, 3204661 | 400,086 | 14,818 | $400{,}086/14{,}818=27.00$ |
    | 13 Apr 2018 | 14 May 2018, 4227035 | 875,204 | 19,891 | $875{,}204/19{,}891=44.00$ |
    | 23 Aug 2019 | 4 Sep 2019, 1004709189 | 697,344 | 14,528 | $697{,}344/14{,}528=48.00$ |
    | 20 Aug 2020 | 8 Sep 2020, 1004974438 | 1,236,202 | 41,450 | $1{,}236{,}202/41{,}450=29.82$ |
    | **Total** | | **3,460,836** | **141,087** | |

  - **Why the row did not close.** (a) The conversions created only 141,087 of the $429{,}444-100{,}000=329{,}444$ shares added from 2014 to 2020, i.e. 43%, so "mostly through six conversions" is wrong. The other shares came from rights exercised under the conditional capital created on 1 Jul 2013 (32,170 in Oct 2014, 11,189 in Nov 2016, 18,326 in Jun 2018 and 9,479 in Aug 2020: 71,164 in all) and from ordinary or authorised increases with no set-off stated, i.e. paid otherwise, at prices not published (43,463 in Mar 2015, 25,500 in Nov 2016, 10,417 in Jun 2018 and 37,813 in Aug 2020: 117,193). Check: $141{,}087+71{,}164+117{,}193=329{,}444$ [E]. (b) The ≈CHF 3.3 M in the report comes from the cantonal extract's table of "montant libéré par compensation de créances", which lists CHF 34,000 for the 2014 step, the nominal value of the 34,000 shares; the SOGC notice itself gives CHF 170,000 of claims. With it the six conversions total CHF 3.46 M. (c) The two earliest conversions, at CHF 5, were missing from the list of implied prices; the four the report gives (27, 44, 48, ≈29.8) are exact.
  - **Exchange rate.** The 20-F's \$7.67 M is its convenience translation of RMB 54.45 M at the year-end rate: $54.45/7.0999=7.67$, and RMB 7.0999 per dollar is the H.10 rate of 29 Dec 2023 [P; E]. At the H.10 rate for the closing date, 15 Dec 2023 (CHF 0.8688 per dollar), the price is $7.67\ {\rm M}\times0.8688=6.66$ M, i.e. about CHF 6.7 M as the report says; converting the RMB amount at that day's rates gives $54.45\ {\rm M}/7.1179\times0.8688=6.65$ M [P; E]. At the 29 Dec rate (CHF 0.8405) it would be CHF 6.45 M; the Swiss National Bank's December 2023 average (CHF 0.86603 per dollar) gives CHF 6.64 M. Per share: $6.66\times10^{6}/429{,}444=15.5$ CHF, below every conversion from 2016 to 2020 (CHF 27–48) but three times the CHF 5 of 2014–15 [E].
- **Source:**
  - Canton of Vaud, commercial register extract for Fastree3D SA (CHE-291.330.490, register no. 2013/10822), state of 5 Oct 2026, read in full with struck entries shown ("Afficher les radiations"): capital, statutes, addresses, set-off and journal tables: https://prestations.vd.ch/pub/101266/extract?lang=FR&companyOfsUid=CHE-291.330.490
  - SOGC (FOSC/SHAB) notices for Fastree3D SA: 12 Jul 2013 (ID 974895), 5 Nov 2014 (1805463), 18 Mar 2015 (2049783) and 8 Dec 2015 (2526843), read as the archive's one-page PDFs (e.g. https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID=1805463); 11 Jul 2016 to 12 Mar 2024 read as the publication texts in the federal Zefix record (ehraid 1146596): https://www.zefix.admin.ch/ZefixREST/api/v1/firm/1146596.json
  - Board of Governors of the Federal Reserve System, H.10 releases of 18 Dec 2023 (rates for 11–15 Dec) and 2 Jan 2024 (25–29 Dec): https://www.federalreserve.gov/releases/h10/20231218/ ; https://www.federalreserve.gov/releases/h10/20240102/
  - Swiss National Bank data portal, cube devkum (monthly average and end of month, December 2023): https://data.snb.ch/api/cube/devkum/data/csv/en?fromDate=2023-12&toDate=2023-12
- **Evidence tag:** [P]
- **Confidence:** high — every step is printed in the official notices, and the shares add up to the registered capital.
- **Proposed edit:**
  - Edit 1, §C3a subsection 2, timeline row 2013–2020:
    - `old`:
      ```text
      | 2013–2020 | **Capital, from the Vaud commercial register:** CHF 100 k at founding (statutes 1 Jul 2013, seat Ecublens; board Charbon, Florin and André Borowski, whose 2011 SPAD-imager patents the company later held), rising to **CHF 429,444** by Aug 2020, mostly through six conversions of loans into shares totalling ≈CHF 3.3 M. Implied conversion prices: ≈CHF 27 per share (2016), ≈44 (2018), 48 (2019) and ≈29.8 (Aug 2020, a down-round) | [P, register; E arithmetic] |
      ```
    - `new`:
      ```text
      | 2013–2020 | **Capital, from the Vaud commercial register and its SOGC notices:** CHF 100,000 in 100,000 registered shares of CHF 1 at founding (statutes 1 Jul 2013, seat Ecublens; board Charbon, Florin and André Borowski, whose 2011 SPAD-imager patents the company later held), rising to **CHF 429,444, i.e. 429,444 shares,** by Aug 2020. Six conversions of loans into shares turned CHF 3.46 M of claims into 141,087 shares: 34,000 at CHF 5 (Oct 2014), 16,400 at CHF 5 (Nov 2015), 14,818 at CHF 27 (Nov 2016), 19,891 at CHF 44 (Apr 2018), 14,528 at CHF 48 (Aug 2019) and 41,450 at ≈CHF 29.8 (Aug 2020, a down-round). The other 188,357 new shares came from rights exercised under the conditional capital (71,164) and from increases with no set-off stated (117,193), at prices not published | [P, register and SOGC; E arithmetic] |
      ```
  - Edit 2, same table, "Total funding" row:
    - `old`:
      ```text
      largely as convertible loans (≈CHF 3.3 M converted by 2020 [P, register])
      ```
    - `new`:
      ```text
      largely as convertible loans (≈CHF 3.46 M of claims converted by 2020 [P, register and SOGC])
      ```
  - Edit 3, "Was it a success?", per-share bullet:
    - `old`:
      ```text
      The \$7.67 M price is about CHF 6.7 M. Taking the CHF 429,444 of capital as 429,444 shares of CHF 1 nominal [U], that is $6.7\times10^{6}/429{,}444\approx15.6$ CHF per share, below every 2016–20 conversion price (CHF 27–48).
      ```
    - `new`:
      ```text
      The \$7.67 M price is about CHF 6.7 M: $7.67\ {\rm M}\times0.8688\ {\rm CHF/\$}=6.66$ M at the Federal Reserve's H.10 rate for the closing date, 15 Dec 2023 [P, H.10; E]. The CHF 429,444 of capital is 429,444 registered shares of CHF 1 [P, register], so that is $6.66\times10^{6}/429{,}444\approx15.5$ CHF per share, below every conversion price from 2016 to 2020 (CHF 27–48) but three times the CHF 5 of the 2014–15 conversions [E].
      ```
- **Appendix 2 entry:**
  - The Vaud register extract is listed already: none.
  - `- SOGC (FOSC) notices for Fastree3D SA, 2013–2024 (founding 12 Jul 2013; six set-offs of claims, 2014–20; addresses 2017 and 2024): https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID=974895 ; full texts from 2016 in the Zefix record: https://www.zefix.admin.ch/ZefixREST/api/v1/firm/1146596.json`
  - `- Federal Reserve H.10, daily rates 11–15 Dec 2023 (CHF 0.8688, CNY 7.1179 per US$ on 15 Dec) and 25–29 Dec 2023: https://www.federalreserve.gov/releases/h10/20231218/ ; https://www.federalreserve.gov/releases/h10/20240102/`

---

## R3_C4d-C9_C5-C6-08

- **Question:** In the IMX560-AAMV flyer, is the 6 Mcps dark-count maximum the worst SPAD or a slip, and what does "at 99% accumulation" mean for the 15 ns dead time?
- **Answer:**
  - **Dark count rate.** The flyer's "Sensor Characteristics" table gives a typical "(3.5 k)" and a maximum "6 M" cps, and its Remarks column says "Average per SPAD" for every row. The maximum is therefore an upper limit on the average over the array, not the worst SPAD. Only values in parentheses are "for reference only", so the typical 3.5 kcps is a reference value while the 6 Mcps maximum is a stated limit. The ratio is $6\times10^{6}/3.5\times10^{3}\approx1{,}700$. The same entries appear in the 2024 Ver. 1.0 and the 2026 Ver. 1.1 of the flyer, which makes a one-off misprint unlikely; the flyer states no temperature, so the limit may cover the hot end of the operating range, but that is a reading, not a statement [E/U].
  - **Dead time.** The flyer defines dead time as the SPAD's output pulse width and gives two figures, both averaged per SPAD: "Pulse width, accumulation 99 %" with 15 ns typical and 20 ns maximum (both in parentheses, reference only), and "Pulse width, most frequent" with 9 ns typical and 11.5 ns maximum. "Accumulation 99 %" reads as the cumulative (accumulated) distribution of pulse widths reaching 99%, i.e. the width that 99% of pulses do not exceed, while "most frequent" is the mode of the distribution [E]. The 9 ns modal value is the one to set against the 6 ns of the ISSCC 2021 development chip.
  - Other entries in the same table: breakdown voltage −24.5 to −17 V (−22.5 V typical); PDE 10% minimum, 24% typical (wavelength not stated); 1 GHz TDC with 2,024 bins; ranging modes of 192, 96 or 48 pixels (3 × N, 6 × N, 12 × N SPADs) to 150–303 m.
- **Source:** Sony Semiconductor Solutions, "IMX560-AAMV: Diagonal 6.25 mm (Type 1/2.9) SPAD ToF Depth Sensor with Signal-amplifying Pixels", flyer Ver. 1.1, © 2024, 2026 (PDF created 22 Apr 2026), p. 2, "Sensor Characteristics" table and note; full 3-page PDF read (table region re-rendered at 300 dpi): https://www.sony-semicon.com/files/62/flyer_industry/IMX560-AAMV_Flyer.pdf . Ver. 1.0 (© 2024) checked in the HTML rendering hosted by the distributor portal Sekorm (2 pages; identical table): https://en.sekorm.com/doc/577474321.html
- **Evidence tag:** [P] for the values and their "average per SPAD" basis; [E] for the reading of "accumulation 99 %"; [U] for why the maximum is so loose.
- **Confidence:** high for what the flyer states; medium for the interpretation of the 6 Mcps limit.
- **Proposed edit** (the dead-time bullet may also carry the 15 ns / 6 ns reconciliation edit; if that edit has been applied first, keep its wording and add only the definitions):
  - Edit 1:
    - `old`:
      ```text
      dark count rate (DCR, the rate of spurious counts in total darkness, caused by thermally generated and tunnelling carriers) **3.5 kcps typical, 6 Mcps maximum, per SPAD** (kcps and Mcps are thousands and millions of counts per second; temperature not stated; values marked "reference");
      ```
    - `new`:
      ```text
      dark count rate (DCR, the rate of spurious counts in total darkness, caused by thermally generated and tunnelling carriers) **3.5 kcps typical and 6 Mcps maximum, both as the average over the SPADs** (kcps and Mcps are thousands and millions of counts per second; temperature not stated). Only the typical value is marked "for reference only". The maximum, about $6\times10^{6}/3.5\times10^{3}\approx1{,}700$ times the typical value and the same in the 2024 and 2026 versions of the flyer, is a loose limit on the array average rather than the worst SPAD [P; reading E];
      ```
  - Edit 2:
    - `old`:
      ```text
      dead time 15 ns typical at 99% accumulation, longer than the 6 ns measured on the ISSCC 2021 development chip behind IMX459 (specification table above), possibly because of a different definition or operating point [U];
      ```
    - `new`:
      ```text
      dead time, defined as the width of the SPAD's output pulse and again averaged over the SPADs, given two ways: 15 ns typical (20 ns maximum) for the width that 99% of pulses do not exceed (the flyer's "accumulation 99 %"), and 9 ns typical (11.5 ns maximum) for the most frequent width [P; reading of "accumulation" E]. The most frequent width is the one to compare with the 6 ns measured on the ISSCC 2021 development chip behind IMX459 (specification table above); the remaining 3 ns may reflect a different definition or operating point [U];
      ```
- **Appendix 2 entry:** `- Sony IMX560-AAMV flyer Ver. 1.1 (Apr 2026; DCR and dead time "average per SPAD"): https://www.sony-semicon.com/files/62/flyer_industry/IMX560-AAMV_Flyer.pdf` (group: *Technology routes and SPAD*; the URL is in the §C5a sources line but not in Appendix 2).

---

## R3_C4d-C9_C5-C6-09

- **Question:** Does the AS-DT1 spec sheet offer a 30 m range at both 30 fps and 15 fps, and how many mode settings are there?
- **Answer:** There are **five** mode settings, not four, and 30 m exists at both frame rates. The spec sheet's tables: 20M, 0.3–20 m at 30 fps; 30MSTD, 0.3–30 m at 30 fps; 30M15F, 0.3–30 m at 15 fps; 30M30F, 0.3–30 m at 30 fps; 40M, 0.3–40 m at 15 fps. Sony's User's Guide explains them: 30MSTD is "the standard range", 576 points at up to 30 fps; 30M15F lowers the frame rate to 15 fps and adds ToF measurements per point for outdoor use; 30M30F keeps 30 fps for outdoor use by adding measurements per point while reducing the points to 288; 20M gives better accuracy below 5 m; 40M (576 points, 15 fps) lengthens the maximum ToF measurement time. The distributor's specification table gives the grids: 24 × 24 for all modes except 30M30F (24 × 12). The 288-point mode is the binning trade of the report's "Points cost range" paragraph, used by Sony itself.
- **Source:**
  - Sony, AS-DT1 spec sheet (PDF created 5 Feb 2026, modified 29 Apr 2026; distributor Aegis Electronic Group), p. 1 "Distance measurement" tables of range and frame rate per mode; pp. 1–3 accuracy and precision tables; full 4 pages of data read: https://aegis-elec.com/mwdownloads/download/link/id/7568
  - Sony Corporation, *AS-DT1 LiDAR Depth Sensor User's Guide*, marked "Tentative", © 2025 (PDF created 14 Oct 2025, modified 14 Jan 2026), "Distance Measurement Range" (p. 21), "Ranging Performance" (p. 22) and "Specifications" (p. 27); pages rendered and read: https://aegis-elec.com/mwdownloads/download/link/id/7523
  - Aegis Electronic Group, AS-DT1 product page, specification table ("576 dots (288 dots with 30M30F mode)"; mode table with dots per mode): https://aegis-elec.com/sony-as-dt1-lidar-depth-sensor.html — HTML read.
- **Evidence tag:** [P]
- **Confidence:** high — two Sony documents and the distributor's table agree.
- **Proposed edit:**
  - `old`:
    ```text
    four mode settings: 20 m and 30 m at 30 fps, and 30 m and 40 m at 15 fps [P, spec sheet]
    ```
  - `new`:
    ```text
    five mode settings: 20 m at 30 fps; 30 m at 30 fps (the standard mode), at 15 fps, and at 30 fps with 288 points; and 40 m at 15 fps [P, spec sheet and user's guide]
    ```
- **Appendix 2 entry:**
  - `- Sony AS-DT1 spec sheet (Feb–Apr 2026, via Aegis Electronic Group; five modes): https://aegis-elec.com/mwdownloads/download/link/id/7568` (the URL is in the §C5a sources line but not in Appendix 2)
  - `- Sony AS-DT1 User's Guide (tentative, Oct 2025–Jan 2026; mode descriptions; 1,000 lx indoor and 40,000 lx outdoor test conditions): https://aegis-elec.com/mwdownloads/download/link/id/7523`
- **Related observations (outside this item; optional edits for the editor):**
  - The User's Guide states the test illuminance that the report calls unstated: indoor results at 1,000 lux and outdoor results at 40,000 lux (p. 22). Sony's own brochure (Apr 2025) gives 20 m outdoors "on a clear summer day (assuming 100,000 lux)" at 50% reflectivity and 15 fps, while the User's Guide's main specifications give 40 m outdoors in the 40M mode at 50% reflectivity; the two outdoor figures refer to different ambient levels.
    - `old`:
      ```text
      In its 40 m mode the sheet also tabulates outdoor figures out to 40 m, with the ambient level unstated.
      ```
    - `new`:
      ```text
      In its 40 m mode the sheet also tabulates outdoor figures out to 40 m; Sony's user's guide gives the test conditions as 1,000 lx indoors and 40,000 lx outdoors [P].
      ```
  - The qualification cell's "operating 0–40 °C" is the guaranteed-performance range; the spec sheet and User's Guide give operation from −5 to +45 °C and storage from −30 to +60 °C.
    - `old`:
      ```text
      Industrial (drones, AMRs, service robots); Class 1 under IEC 60825-1:2014; operating 0–40 °C [P]
      ```
    - `new`:
      ```text
      Industrial (drones, AMRs, service robots); Class 1 under IEC 60825-1:2014; performance guaranteed at 0–40 °C, operation from −5 to +45 °C [P]
      ```

---

## R3_C4d-C9_C5-C6-10

- **Question:** Where does a Hesai "V-series" chip label appear, and do Hesai's own documents use it?
- **Answer:** The label comes from Hesai itself, as version numbers of its ASIC roadmap, so "no such name exists" is too strong. Hesai's F-1/A prospectus (filed 2 Feb 2023) says it produces "v1.0 and v1.5 ASICs" in volume, is developing "v2.0 and v3.0 ASICs" (the FT120 "is expected to carry our v3.0 ASICs") and plans "v4.0 ASICs" for future AT and FT products. A Hesai slide (data as of 31 May 2023), reproduced in ResearchInChina's *Automotive LiDAR Industry Report, 2023*, labels its chip generations V1.0 (2017–20, XT series), V2.0 (2018–22, AT128), V3.0 (2019–23, FT120) and V4.0 (2020–26, next-generation products); the report's text relays this as "V1.0, V1.5, V2.0, and V3.0 LiDAR chip architectures" with V4.0 in development. These are version numbers, not a product line called "V-series". Hesai's later releases speak of generations: the ATX (22 Apr 2024) uses the "4th-generation technology platform"; the Fermi C500 controller (24 Nov 2025) completes the in-house fourth-generation chip platform (it is a part of that generation, not a generation of its own); and Picasso (Apr 2026) is the fifth-generation SPAD-SoC. The fourth step of the 2023 numbering, V4.0, therefore corresponds to what Hesai later calls its fourth-generation platform [E].
- **Source:**
  - Hesai Group, Form F-1/A (amendment to the registration statement), filed 2 Feb 2023, "Business" and "Product Roadmap" sections, https://www.sec.gov/Archives/edgar/data/1861737/000110465923009861/tm2120356-22_f1a.htm — passages read in the filing (EDGAR index dated 2023-02-02).
  - ResearchInChina, *Automotive LiDAR Industry Report, 2023* (Oct 2023), free excerpt p. 6 "Hesai LiDAR", text and the reproduced Hesai slide "Hesai's platform-based self-developed chips" (source line "Hesai Technology"): http://www.researchinchina.com/UpLoads/ArticleFreePartPath/20231103150900.pdf — page rendered and read.
  - Hesai, "Hesai Launches New Ultra-Wide FOV, Long-Range ATX Lidar", 22 Apr 2024, https://www.hesaitech.com/hesai-launches-new-ultra-wide-fov-long-range-atx-lidar/ — full text read.
  - Hesai, Fermi C500 release, 24 Nov 2025, https://www.hesaitech.com/cn/news/1384 — full text read ("补齐了禾赛第四代芯片平台全栈自研的最后一块拼图").
- **Evidence tag:** [P] for Hesai's numbering and generations; [MR] for the ResearchInChina relay; [E] for matching V4.0 to the fourth generation.
- **Confidence:** high — Hesai's own filing and slide use the numbering.
- **Proposed edit:**
  - `old`:
    ```text
    **No Hesai "V-series" chip name exists**; the generations are the 4th-gen ASIC, Fermi C500 and Picasso
    ```
  - `new`:
    ```text
    Hesai's 2023 prospectus and a 2023 Hesai slide number its in-house ASICs v1.0, v1.5, V2.0, V3.0 and a planned V4.0 [P], relayed as "V1.0 ... V4.0" chip architectures by ResearchInChina (Oct 2023) [MR]; these are version numbers, not a chip family. Its later releases name the 4th-generation platform (ATX, 2024–25), whose Fermi C500 controller (Nov 2025) completes it, and the 5th-generation Picasso SPAD-SoC [P]
    ```
- **Appendix 2 entry:**
  - `- Hesai F-1/A (2 Feb 2023; v1.0/v1.5 ASICs in production, v2.0/v3.0 in development, v4.0 planned): https://www.sec.gov/Archives/edgar/data/1861737/000110465923009861/tm2120356-22_f1a.htm`
  - `- ResearchInChina, Automotive LiDAR Industry Report 2023, free excerpt (Hesai V1.0–V4.0 chip slide, p. 6): http://www.researchinchina.com/UpLoads/ArticleFreePartPath/20231103150900.pdf`
  - `- Hesai ATX launch (22 Apr 2024; 4th-generation platform): https://www.hesaitech.com/hesai-launches-new-ultra-wide-fov-long-range-atx-lidar/`

---

## R3_C4d-C9_C5-C6-11

- **Question:** What die and channel counts should the §C5 table give for the ATX, and how should the other places be aligned?
- **Answer:** The public record gives 17 SiPM dies [T] and 64 physical channels [T]; Hesai's ATX_S01 manual lists 116 output channels, of which channels 1–64 are "normal" and 65–116 "super-resolution" [P]. No public source gives four channels per die (details and sources under item 04). Two further points matter for aligning the text:
  - The ATX_S01 configuration specifies 116 channels, 200 m at 10%, 120° × 18.3° with a 120° × 8.8° ROI, 0.08° horizontal and 0.1° (ROI) to 0.2° vertical resolution, and $1{,}500\times116\times10=1.74\times10^{6}$ points/s at 10 Hz [P]. The 256 channels, 230 m and 3.84 Mpts/s of Hesai's product page are the flagship configuration of the version announced on 24 Nov 2025 for delivery from April 2026 [P]. The report's "ATX 256 [P], whose laser-addressed lines share 64 physical receive channels" therefore mixes two versions: the 64 is documented only for the 2025 configuration.
  - With 64 physical channels, the S01 configuration's 1.74 Mpts/s is $1.74\times10^{6}/64\approx27$ kpts/s per receive channel; the 60 kpts/s in §C4d 2(b) holds only if the 256-line version also keeps 64 channels, which is not public [E/U].
  - How the 52 super-resolution channels are formed is not described by Hesai; NE Times points to patent CN119199894A [T]. The phrase "by laser addressing" has no source and is left out below.
- **Source:** As item 04: Hesai ATX_S01 manual A07 (§1.3, printed p. 12, Figure 4; §1.4, printed p. 13; point-rate note, printed p. 15); Hesai Fermi C500 release of 24 Nov 2025; Hesai ATX product page, "256 (Highest Supported Channels)", https://www.hesaitech.com/product/atx/ (read 5 Oct 2026); NE Times 26-teardown summary (22 Dec 2025); MyDrivers (23 May 2025); TechInsights via Electronics360 (29 Aug 2025). TechInsights DDT-2505-806 not accessible (paywall).
- **Evidence tag:** [T] for 17 dies and 64 physical channels; [P] for the 116 = 64 + 52 split and for the two configurations; [E/U] for per-channel rates of the 256-line version.
- **Confidence:** medium — the counts are consistent across sources, but the die-to-channel mapping and the 256-line version's physical channels are not public.
- **Proposed edit:**
  - Edit 1, §C5 table:
    - `old`:
      ```text
      | Hesai ATX | SiPM (17 dies / 64 channels), TI, 3peak and Infineon parts [I] |
      ```
    - `new`:
      ```text
      | Hesai ATX | SiPM: 17 dies [T] for 64 physical channels [T], which Hesai's ATX_S01 manual lists as 64 "normal" plus 52 "super-resolution" output channels [P]; TI, 3peak and Infineon parts [I] |
      ```
  - Edit 2, §C4b "Other dimensions" table:
    - `old`:
      ```text
      The ATX uses 64 physical channels and multiplies effective lines by laser addressing
      ```
    - `new`:
      ```text
      The ATX uses 64 physical channels [T]; its ATX_S01 configuration outputs 116 channels, 64 "normal" and 52 "super-resolution", by a scheme Hesai has not described [P]
      ```
  - Edit 3 (related), §C4d subsection 1 table, one-axis row:
    - `old`:
      ```text
      AT128 128 channels, ATX 256 [P], whose laser-addressed lines share 64 physical receive channels (§C4b)
      ```
    - `new`:
      ```text
      AT128 128 channels; ATX 116 in its ATX_S01 configuration (64 "normal" and 52 "super-resolution" channels on 64 physical receive channels, §C4b) and 256 in the flagship configuration of the version delivered from April 2026 [P]
      ```
  - Edit 4 (related), §C4d 2(b):
    - `old`:
      ```text
      The ATX's 256 lines share 64 physical receive channels (§C4b), so each receive channel handles $3.84\times10^{6}/64=60$ kpts/s, still about a tenth of the limit.
      ```
    - `new`:
      ```text
      The ATX_S01 configuration spreads $1.74\times10^{6}$ pts/s over 64 physical receive channels (§C4b), $1.74\times10^{6}/64\approx27$ kpts/s each; if the 256-line version kept 64 channels, each would handle $3.84\times10^{6}/64=60$ kpts/s, still about a tenth of the limit [P/T/E].
      ```
- **Appendix 2 entry:** as item 04 (ATX_S01 manual; Fermi C500 release; TechInsights partial teardown). The Hesai ATX product page is already listed for §C3b ("Hesai ATX product page" is in the §C4d sources line); add `- Hesai ATX product page ("256 (Highest Supported Channels)", 230 m, 3.84 Mpts/s, 8 W): https://www.hesaitech.com/product/atx/` only if it is not already in Appendix 2.

---

## R3_C4d-C9_C5-C6-12

(The rows concerned now sit in §C3a, subsection 2; their wording is unchanged.)

- **Question:** When was Fastree3D SA founded and registered, where were its seat and address in 2013, and how did the address change later?
- **Answer:**
  - **Founding.** Statutes dated 1 Jul 2013; entered in the Vaud daily register on 9 Jul 2013 (no. 10822); published as a new company in SOGC No 133 of 12 Jul 2013 [P]. Capital CHF 100,000 in 100,000 registered shares of CHF 1; board Charbon (president), Florin (secretary) and Borowski.
  - **Seat and address.** The legal seat has always been Ecublens (VD). The 2013 address was "Parc Scientifique EPFL, PSE-C, 1015 Lausanne", the EPFL science park, which EPFL renamed EPFL Innovation Park in 2014 [P]. From 13 Apr 2017 (SOGC 20 Apr 2017) the address was chemin de la Dent d'Oche 1 B, 1024 Ecublens; from 7 Mar 2024 (SOGC 12 Mar 2024, statutes of 29 Feb 2024) it is EPFL Innovation Park, Bâtiment E, 1015 Lausanne [P]. So in 2024 the address returned to the park after seven years in Ecublens.
  - **The other dates.** The company's own page calls it a "2014 EPFL/TU-Delft spin-off" based in Lausanne and Delft [P]; it does not say what the 2014 refers to, but it is not the year of incorporation (the timeline's Venture Kick award is also of 2014). Hesai's Hong Kong listing document (accountants' report, Sep 2025) lists Fastree3D SA as "September 2013, Switzerland", capital CHF 429,444 [P], two months after the register's dates; the report's 2025-annual-report citation carries the same month. The register is the legal record, so the timeline should date the founding to July 2013 and attribute "Sep 2013" to Hesai.
- **Source:**
  - SOGC No 133, 12 Jul 2013, "Nouvelles inscriptions", Fastree3D SA (ID 974895, daily register no. 10822 of 9 Jul 2013), one-page PDF read: https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID=974895
  - SOGC notices of 20 Apr 2017 (ID 3476973, address in Ecublens) and 12 Mar 2024 (ID 1005983841, address at the EPFL Innovation Park), read in the Zefix record: https://www.zefix.admin.ch/ZefixREST/api/v1/firm/1146596.json
  - Canton of Vaud, register extract with struck entries shown (address table: refs 1, 8, 15; statutes table): https://prestations.vd.ch/pub/101266/extract?lang=FR&companyOfsUid=CHE-291.330.490
  - EPFL, "EPFL: fostering innovation for 25 years", 29 Aug 2018 ("renamed EPFL Innovation Park in 2014"): https://actu.epfl.ch/news/epfl-fostering-innovation-for-25-years
  - Fastree3D, "About us" (live page read 5 Oct 2026): https://www.fastree3d.com/about-us/
  - Hesai Group, Hong Kong listing document, Appendix I, Accountants' Report, 16 Sep 2025, subsidiary table p. 17 (text located and read): https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0916/11842018/sehk25083100407.pdf . Hesai's 2025 annual report itself could not be re-read here (the SEC copy is served only as a download).
- **Evidence tag:** [P]
- **Confidence:** high — the dates and addresses are printed in the official notices.
- **Proposed edit:**
  - Edit 1, §C3a subsection 2, timeline row "Sep 2013 / 2014":
    - `old`:
      ```text
      | Sep 2013 / 2014 | Fastree3D SA incorporated in Lausanne (EPFL Innovation Park; office in Delft) as an **EPFL + TU Delft spin-off**. Florin is CEO, Charbon CSO, Lucio Carrara CTO. It starts with more than 15 patents from about 20 years of academic work | [P, company "About"; T] |
      ```
    - `new`:
      ```text
      | Jul 2013 | Fastree3D SA founded: statutes of 1 Jul 2013, entered in the Vaud register on 9 Jul 2013 and published on 12 Jul 2013, with its legal seat in Ecublens and its address in the EPFL science park (Parc Scientifique EPFL, PSE-C, 1015 Lausanne), renamed EPFL Innovation Park in 2014. The company calls itself a 2014 **EPFL + TU Delft spin-off**, with an office in Delft. Florin is CEO, Charbon CSO, Lucio Carrara CTO. It starts with more than 15 patents from about 20 years of academic work | [P, register and SOGC; EPFL; company "About"; T] |
      ```
  - Edit 2, row "15 Dec 2023":
    - `old`:
      ```text
      Its 2025 annual report lists **Fastree3D SA** (Switzerland, Sep 2013, capital CHF 429,444) as a 100% subsidiary for "Development of LiDAR".
      ```
    - `new`:
      ```text
      Its 2025 annual report lists **Fastree3D SA** (Switzerland, capital CHF 429,444) as a 100% subsidiary for "Development of LiDAR"; Hesai dates it to September 2013, also in its Hong Kong listing document, two months after the July 2013 of the commercial register.
      ```
  - Edit 3, row "Jan–Mar 2024":
    - `old`:
      ```text
      and the registered address moves to the EPFL Innovation Park (the legal seat stays Ecublens)
      ```
    - `new`:
      ```text
      and the registered address returns to the EPFL Innovation Park (Building E, 1015 Lausanne) after seven years at an Ecublens street address (the legal seat stays Ecublens)
      ```
- **Appendix 2 entry:**
  - `- EPFL, the science park renamed EPFL Innovation Park in 2014 (29 Aug 2018): https://actu.epfl.ch/news/epfl-fostering-innovation-for-25-years`
  - `- Hesai Hong Kong listing document, accountants' report (Sep 2025; subsidiary table, Fastree3D SA "September 2013"): https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0916/11842018/sehk25083100407.pdf`
  - The SOGC entry is given under item 07; the Vaud register and the Fastree3D "About us" page are listed already: none.

---

## R3_C4d-C9_C5-C6-13

- **Question:** What vertical field does RoboSense give for the EM4, and how does it relate to IMX479's 120° × 26°?
- **Answer:** RoboSense's EM4 page gives **120° × 27°** in both its English and Chinese versions (the Chinese page labels it "更大垂向FOV", a larger vertical field), for the EM4 platform, which is offered with up to 2,160 lines (41.04 M points/s; 300 m at 10%, 600 m maximum); the page's performance images are of "the 520-beam version". 27° is right for the product. The 120° × 26° is not a chip property: Sony's IMX479 release gives 520 dToF pixels and 0.05° vertical resolution but no field, and the 120° horizontal by 26° vertical comes from the JSSC 2026 paper's abstract, which describes Sony's own lidar system with 0.05° steps in both axes. The receiver lens sets the field: 520 pixels at 0.05° span $520\times0.05°=26°$, while 27° over 520 lines needs $27°/520=0.052°$ per line, a focal length about 4% shorter [E]. 27° over 1,080 lines gives $27°/1{,}080=0.025°$, the EM4's finest vertical step reported by Chinese media [T]. The $R^2\cdot{\rm FOV}$ entry is unaffected: $300^2\times120\times27=2.9\times10^{8}$, against $2.8\times10^{8}$ with 26° [E].
- **Source:**
  - RoboSense, EM4 product page, English https://www.robosense.ai/en/IncrementalComponents/EM4 and Chinese https://www.robosense.ai/IncrementalComponents/EM4 — read 5 Oct 2026 (rendered pages). The EM4 brochure (7 Jan 2025) sits behind a form asking for name, phone, email and a CAPTCHA and was not downloaded.
  - Sony Semiconductor Solutions, IMX479 release, 10 Jun 2025, "Key Specifications", https://www.sony-semicon.com/en/news/2025/2025061001.html — full text read.
  - T. Yui *et al.*, "A 25-Mpts/s Back-Illuminated Stacked SPAD Direct Time-of-Flight Depth Sensor With Equivalent Time Sampling and Pixel-Level Threshold Control for Automotive LiDAR", *IEEE J. Solid-State Circuits* 61(4), 1308–1318 (published 18 Feb 2026), https://doi.org/10.1109/JSSC.2026.3663598 — abstract read on IEEE Xplore (full text paywalled).
  - Sina/QQ coverage of the EM4 platform (520/720/1,080/2,160-line versions; 0.050° × 0.025° finest), seen as search-result extracts only, e.g. https://www.sohu.com/a/993845757_211762 [T].
- **Evidence tag:** [P] for 120° × 27°; [I] for the origin of 120° × 26°; [E] for the lens arithmetic.
- **Confidence:** high — RoboSense's own pages and Sony's abstract were read directly.
- **Proposed edit:**
  - Edit 1, §C6 table:
    - `old`:
      ```text
      | RoboSense EM4 (1 scan axis) | 120°×27° |
      ```
    - `new`:
      ```text
      | RoboSense EM4 (1 scan axis) | 120°×27° [P]; the lens, not the IMX479-class chip, sets this field (Sony's 120° × 26° is its own test system at 0.05°) |
      ```
  - Edit 2 (related), §C5a specification table, IMX479 throughput cell:
    - `old`:
      ```text
      over 120° × 26° |
      ```
    - `new`:
      ```text
      over 120° × 26°, the field of Sony's own lidar system at 0.05° in both axes rather than a property of the chip [I, JSSC 2026 abstract] |
      ```
- **Appendix 2 entry:** none for the RoboSense EM4 page and the IMX479 release (both listed). Add `- Yui *et al.*, Sony 25-Mpts/s SPAD dToF sensor, *IEEE JSSC* 61(4), 1308 (2026), abstract (120° × 26° at 0.05°): https://doi.org/10.1109/JSSC.2026.3663598` only if the DOI is not already in Appendix 2 (it is in the §C5a sources line).
