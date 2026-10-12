# Round 4 source findings: R7_E9-E12

Items from `R7_E9-E12_items.md` (block 11_E9-E12 of the readability review). Every `old` string below is copied verbatim from `automotive_perception_report_2026-09-27.md` at SHA-256 prefix 51d60fa27199 (the version with the §E12 equations merged and all equations renumbered), and the count check at the end confirms that each occurs exactly once in that version. Edits marked *optional* go beyond the item's literal request but fix something the research turned up in the same sentence or table. Scripts are in `sources/scripts/` (prefix `R7_`), each with a line in `sources/scripts/INDEX.md`.

---

## R7_E9-E12-01

- **Question:** Did Grace-BEV retrain MEFormer for its Table 1, or quote MEFormer's 70.5 mAP / 72.7 NDS from the MEFormer paper, as it does for MetaBEV?
- **Answer:** Grace-BEV retrained it. Its §5.1 says it re-implemented and trained "all baseline methods in a unified experimental setting, except MetaBEV", which it quotes from the original paper "due to the lack of public code". The Table 1 caption uses † for "results cited directly from the original paper". Only the MetaBEV row carries †; the MEFormer [5] row does not (checked on a 300 dpi render of the table).
  - MEFormer's own paper gives a different, higher figure, which corroborates the retraining: 71.5 mAP and 73.9 NDS on nuScenes val (Cha *et al.*, Table 1). Grace-BEV's run is therefore 1.0 mAP and 1.2 NDS lower ($71.5-70.5=1.0$; $73.9-72.7=1.2$). By contrast, the MetaBEV row in Grace-BEV (68.0 / 71.5) matches MetaBEV's own numbers exactly, which also appear in MEFormer's Table 1.
  - A point for the editor: MEFormer is built on CMT (Grace-BEV lists 86.6 M + 0.3 M parameters, against 40.8 M for BEVFusion-MIT). Its architecture-matched baseline in the same table is therefore CMT at 69.7 mAP, which MEFormer exceeds by 0.8. Its margin of 3.6 mAP over BEVFusion-MIT combines the robustness design with a larger base detector. The proposed edit leaves the report's comparison in place.
- **Source:**
  - Zhang H., Wang Y., Wang H., Li Z., Zuo Z., "Can BEV Perception Gracefully Degrade under Sensor Failures?", arXiv 2605.30983 v1 (PDF dated 1 Jun 2026), https://arxiv.org/abs/2605.30983. Read: §5.1 "Architecture and Baselines" (p. 6) and Table 1 with its caption (p. 5), full text, rendered pages.
  - Cha J., Joo M., Park J., Lee S., Kim I., Kim H. J., "Robust Multimodal 3D Object Detection via Modality-Agnostic Decoding and Proximity-based Modality Ensemble" (MEFormer), arXiv 2407.19156 (Aug 2024 version), https://arxiv.org/abs/2407.19156. Read: Table 1 (p. 6), full text, rendered page.
- **Evidence tag:** [I]
- **Confidence:** High. The paper says so explicitly, and MEFormer's own differing score corroborates it.
- **Proposed edit:**
  - `old`:
```
and MEFormer 70.5, 3.6 above it ($70.5-66.9=3.6$).
```
  - `new`:
```
and MEFormer 70.5, 3.6 above it ($70.5-66.9=3.6$). Grace-BEV retrained MEFormer in the same unified setting as its baseline; MEFormer's own paper reports 71.5 [I, Cha et al., arXiv 2407.19156, Table 1].
```
- **Appendix 2 entry:** under *Chip-size limits, interference and fusion (§C8, §C9, §E10)*:
  - `- Zhang *et al.*, Grace-BEV, BEV detection under sensor failures (arXiv 2605.30983, 2026): https://arxiv.org/abs/2605.30983`
  - `- Cha *et al.*, MEFormer, modality-agnostic decoding and modality ensemble (arXiv 2407.19156): https://arxiv.org/abs/2407.19156`

---

## R7_E9-E12-02

- **Question:** For how many epochs was the BEVFusion-MIT camera + lidar baseline (68.5 mAP) in Fusion4CA's Table I trained, and does the +1.2 mAP compare runs of equal training?
- **Answer:**
  - **What Fusion4CA says.** The baseline is "fully trained for 20 epochs" (abstract). Fig. 1 labels the three runs "BEVFusion-6ep" (64.7 mAP / 69.4 NDS), "BEVFusion-20ep" (68.5 / 71.4) and "Fusion4CA-6ep" (69.7 / 72.1). Its caption says Fusion4CA beats BEVFusion "by 5% mAP at six epochs" and its "20-epoch counterpart by 1.2% mAP". The note to Table I reads "our method only trained for 6 epochs, while others are fully trained". The 6-epoch BEVFusion run is Table II, Order 01 (64.7 mAP, 69.4 NDS). Fusion4CA itself trains for 6 epochs, at batch size 6 and initial learning rate 2e-4 on two RTX 4090 GPUs, "based on the BEVFusion codebase" (§IV-A). So, on Fusion4CA's own account, +1.2 mAP compares 6 epochs with 20, and +5.0 mAP compares 6 with 6 ($69.7-64.7=5.0$).
  - **What BEVFusion's released code says.** The global default is `max_epochs: 20` (`configs/default.yaml`); the lidar-only detector uses it. The camera + lidar configuration (`configs/nuscenes/det/transfusion/secfpn/camera+lidar/default.yaml`) sets `max_epochs: 6` and `lr: 2.0e-4`. The README's training command for the fused model starts from the released lidar-only checkpoint (`--load_from pretrained/lidar-only-det.pth`). The README lists 68.52 mAP / 71.38 NDS for that fused model and 64.68 / 69.28 for the lidar-only TransFusion-L baseline, the 64.7 / 69.3 lidar-only row of Fusion4CA's Table I.
  - **Consequence.** The published 68.5 mAP is the product of 20 lidar-only epochs followed by 6 camera + lidar epochs, with the same learning rate and number of epochs that Fusion4CA reports for itself. Fusion4CA does not say whether its 6 epochs also start from the lidar-only checkpoint. So whether the +1.2 mAP compares equal camera + lidar schedules cannot be settled from the paper. If Fusion4CA follows the codebase's recipe, the schedules are equal and "6 versus 20 epochs" overstates the difference. Fusion4CA's own 6-epoch BEVFusion run (64.7 mAP) falls short of the published 6-epoch fine-tune (68.5) for reasons the paper does not give (batch size 6 against the 8-GPU recipe is one candidate).
- **Source:**
  - Luo K., Chen X., Xiao Y., Wang H., "Fusion4CA: Boosting 3D Object Detection via Comprehensive Image Exploitation", arXiv 2603.05305 v1 (5 Mar 2026), https://arxiv.org/abs/2603.05305. Read: abstract (p. 1), Fig. 1 and caption (p. 2, radar chart zoomed at 400 dpi), §IV-A implementation details, Table I with its note and Table II (p. 5). Full text, rendered pages.
  - MIT HAN Lab, BEVFusion official repository, https://github.com/mit-han-lab/bevfusion. Read: `README.md` (results table and training commands), `configs/default.yaml` (`max_epochs: 20`) and `configs/nuscenes/det/transfusion/secfpn/camera+lidar/default.yaml` (`max_epochs: 6`, `lr: 2.0e-4`). Raw files read on 5 Oct 2026.
- **Evidence tag:** [I] for Fusion4CA; [P] for the BEVFusion repository (the authors' own release).
- **Confidence:** High for the stated schedules; medium for whether the comparison is schedule-matched, because Fusion4CA does not state its initialization.
- **Proposed edit:**
  - `old`:
```
which was trained on its full schedule ($69.7-68.5=1.2$).
```
  - `new`:
```
which Fusion4CA describes as fully trained for 20 epochs ($69.7-68.5=1.2$); Fusion4CA's own 6-epoch BEVFusion run scores 64.7 mAP (its Table II and Fig. 1). In BEVFusion's released code, however, the 20 epochs train the lidar-only detector, and the camera + lidar model is then trained from that checkpoint for 6 epochs, the number Fusion4CA reports for itself [P, BEVFusion repository]. Fusion4CA does not state its starting checkpoint, so the +1.2 mAP may compare equal camera + lidar schedules.
```
- **Appendix 2 entry:** under *Chip-size limits, interference and fusion (§C8, §C9, §E10)*:
  - `- Luo *et al.*, Fusion4CA, camera auxiliary supervision for BEVFusion (arXiv 2603.05305, 2026): https://arxiv.org/abs/2603.05305`
  - `- BEVFusion (MIT) released code and training configurations (20-epoch lidar-only stage, 6-epoch camera + lidar stage): https://github.com/mit-han-lab/bevfusion`

---

## R7_E9-E12-03

- **Question:** What date does SGO report 13781-8004 give with its 00:03 time, and what in the ODI resume conflicts with it?
- **Answer:**
  - **The SGO record.** In the public 2021–25 archive, report 13781-8004 has two versions. Both give the date only as month and year, "NOV-2023" (the public file gives no day), and the time "00:03".
    - Version 1 (submitted JUN-2024): roadway, lighting and weather all "Unknown"; narrative "Review in progress".
    - Version 2 (submitted JUL-2024): "Highway / Freeway", "Traffic Incident", lighting **"Dawn / Dusk"**, weather "Clear", pedestrian struck, fatality, 55 mph.
    - Both versions: notice received JUN-2024 from a complaint or claim.
  - **The ODI resume.** It gives no time. It dates the crash to "November 28, 2023", in the sentence saying Tesla began its update on 28 Jun 2024, "the day after Tesla submitted the SGO report".
  - **The conflict.** The two documents do not contradict each other directly. The conflict lies between the 00:03 time on one side, and on the other the record's own lighting field ("Dawn / Dusk") and the Arizona Department of Public Safety, which placed the crash "on Nov. 27 just after 5 p.m. on Interstate 17" (AP via CBS News). At Rimrock at 00:03 local time the sun is 69–77° below the horizon on every night of November 2023.
  - **The explanation: Tesla files SGO times in UTC.** Arizona keeps UTC−7 all year. A crash at 17:03 on 27 Nov is therefore 00:03 UTC on 28 Nov, which gives both the SGO time and the ODI date, with the sun 1.9° above the horizon (low sun, consistent with "Dawn / Dusk" and with the glare named in the resume). Three checks:
    - The six Tesla archive records in the report's table that carry both a time and a lighting field all agree with their lighting only when the time is read as UTC. Read as local time, five contradict it outright: Collinsville, May, 10:16, "Dawn / Dusk", sun +40°; Fullerton, June, 07:03, "Dark - Lighted", sun +14°; Issaquah, October, 20:40, "Daylight", sun −20° or lower; Stockton, November, 11:30, "Dark - Lighted", sun +30° or higher; Rimrock as above. The sixth (Red Mills) is borderline.
    - Across the whole archive, the lighting field agrees with the time read as UTC for 97.3% of the 1,563 Tesla reports that give a time, a US state and a definite lighting value, against 49.0% (about chance) read as local time. For the 217 such reports from all other entities the result reverses: 92.6% local and 50.2% UTC. Subaru (51 reports, 98% local), GM (49, 88%) and Ford (20, 85%) report local time. Method: solar elevation in mid-month at each state's approximate centre, one time zone per state.
    - The current (post-2025) file has no lighting field, so its Tesla times cannot be tested this way. The same convention is assumed.
  - **Consequences for the §E12.2 table.** Read as local time, the filed times shown in the table become 14:19 or 15:19 (Red Mills, March 2024, depending on whether the day fell before or after the DST change), 00:03 (Fullerton), 13:40 (Issaquah), 22:23 on the previous day (Barrington), 16:36 or 17:36 on the previous day (Sunol), and 16:49 (Bentonville). Times not shown in the table convert to 06:16 (Collinsville, dawn), 03:30 or 04:30 (Stockton), 07:53 (Seattle, about sunrise), 08:09 (Kansas City) and 09:50 (Claremore). The text's "several at night or dawn" still holds in local time (Fullerton, Stockton and Barrington at night; Collinsville and Seattle at dawn), and three more crashes fall at or near dusk (Rimrock, Sunol, Bentonville).
- **Source:**
  - NHTSA, Standing General Order 2021-01, ADAS incident reports, 2021–25 archive CSV, https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Incident_Reports_ADAS.csv (downloaded 5 Oct 2026; 4,027 rows, 137 columns); rows for Report ID 13781-8004, versions 1 and 2, fields Incident Date, Incident Time (24:00), Lighting, Weather, Roadway, Report Submission Date, Notice Received Date. Current file: https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADAS.csv (2,313 rows, 116 columns, no lighting field).
  - NHTSA ODI, "ODI Resume, EA26002" (opened 18 Mar 2026), https://static.nhtsa.gov/odi/inv/2026/INOA-EA26002-10023.pdf, p. 2, summary paragraph 3. Full text, both pages rendered.
  - CBS News / Associated Press, "Tesla's 'Full Self-Driving' system faces probe after pedestrian death", updated 18 Oct 2024, https://www.cbsnews.com/news/tesla-fsd-self-driving-autopilot-elon-musk/, quoting an Arizona Department of Public Safety statement. Read as relayed (the same AP text is carried by LEX 18).
  - Own calculations: `sources/scripts/R7_sgo_record_lookup.py`, `R7_sgo_time_vs_lighting.py`, `R7_sgo_utc_test_all.py`, `R7_misc_snippets.py` (`utc2local`).
- **Evidence tag:** [P] for the SGO fields and the ODI resume; [T] for the DPS time and date relayed by AP; [E] for the UTC finding and the conversions.
- **Confidence:** High. The fields were read directly, and the UTC convention holds for 97% of 1,563 Tesla reports against 49% for local time.
- **Proposed edit (a), the sentence:**
  - `old`:
```
SGO times can also be imprecise: the Rimrock record gives 00:03, while the ODI resume dates the fatal crash to 28 Nov 2023.
```
  - `new`:
```
Tesla files its SGO times in UTC (coordinated universal time), not local time: in the 2021–25 archive, the lighting field of 97% of the 1,563 Tesla reports that give a time and a lighting condition agrees with that time read as UTC, against 49% read as local time, whereas for the 217 such reports from all other companies the figures are 50% and 93% [E: mid-month solar elevation at each state's centre]. The Rimrock record (13781-8004) shows the effect. It gives only the month, November 2023, with 00:03 and the lighting "Dawn / Dusk"; the ODI resume dates the fatal crash to 28 Nov 2023, and the Arizona Department of Public Safety placed it just after 5 p.m. on 27 Nov [P; T, AP via CBS News, 18 Oct 2024]. Both fit a crash at 17:03 on 27 Nov, because Arizona keeps UTC−7 all year and 17:03 there is 00:03 UTC on 28 Nov [E]. The time is therefore omitted from the table, and the other times shown are as filed; in local time they are 14:19 or 15:19 (Red Mills), 00:03 (Fullerton), 13:40 (Issaquah), 22:23 the previous evening (Barrington), 16:36 or 17:36 the previous afternoon (Sunol) and 16:49 (Bentonville) [E].
```
- **Proposed edit (b), the table header** (so that a reader of the table alone does not take the times as local):
  - `old`:
```
| SGO report | Date, place | Road | Weather field | Struck | Tesla speed | Injury |
```
  - `new`:
```
| SGO report | Date, place (time as filed, in UTC) | Road | Weather field | Struck | Tesla speed | Injury |
```
- **Proposed edit (c), optional** (the next bullet, so that it matches the local times):
  - `old`:
```
several at night or dawn, some in fog.
```
  - `new`:
```
several at night, dawn or dusk in local time, some in fog.
```
- **Appendix 2 entry:** under *Camera-only vs multimodal*:
  - `- AP via CBS News, Rimrock fatal crash, Arizona DPS date and time (18 Oct 2024): https://www.cbsnews.com/news/tesla-fsd-self-driving-autopilot-elon-musk/`
  - `- NHTSA SGO ADAS incident reports, 2021–25 archive (time, lighting and weather fields): https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Incident_Reports_ADAS.csv`

---

## R7_E9-E12-04

- **Question:** In the TU Graz beam-density study, is the "under about 3%" in mAP points or in per cent of a reference score, and which beam-count change counts as "modest"?
- **Answer:**
  - **Definition.** The paper's metric is the domain gap of its Eq. (1), $DG=100\,(AP_{T\to T}-AP_{S\to T})/AP_{T\to T}$. Here $AP_{S\to T}$ is the 3D AP of a detector trained on source data $S$ and tested on target data $T$, and $AP_{T\to T}$ is the AP of the same detector trained on the target itself. The gap is therefore a percentage of the target-trained score, not mAP points, and not a percentage of the dense-trained score: the reference is whichever density the target has.
  - **Where the 3% comes from.** The sentence on p. 8 reads "the domain gap increases by only 3% or less when doubling or halving beam density", in the high-IoU (0.7) experiments. It describes the inference-gap experiment of Table 7: PV-RCNN++, vehicle class, detectors trained on the private Rooftop (32-beam) and Truck (128-beam) data and tested on the public Zenseact data resampled to 32, 64 and 128 beams.
    - The 3% is a change in that relative gap, i.e. percentage points of $DG$, not the size of the gap. The gaps themselves are large (16–67% at 0.7 IoU) because other domain shifts are present.
    - Doubling (32-beam-trained, tested on 64 beams): $DG$ 55.0 → 58.0, +3.0 points. Halving (128-beam-trained, tested on 64 beams): 16.3 → 19.0, +2.7 points. A fourfold change raises it by about 12 points (55.0 → 67.4; 16.3 → 28.6).
    - So "modest" means a factor of two, for example 128 to 64 beams.
    - Cross-check: Table 7's gaps follow from Eq. (1) and the target-trained AP of Table 11, e.g. $(68.7-57.6)/68.7=16.2\%$ for Truck128 on ZOD128 (16.3% in Table 7).
  - **The "training on denser data generalized better" part** holds for detection scored at the loose 0.4 IoU. Training-gap Table 8 at 0.4 IoU: on the 32-beam Rooftop target 13.1% / 11.1% / 9.2% for 32-, 64- and 128-beam training, and on the 128-beam Truck target 28.0% / 23.7% / 20.5%. At 0.7 IoU, denser training widened the gap on the sparse Rooftop target (38.4% → 45.8%).
  - **The isolated density-resampling experiment** (Table 6, Zenseact only) has small gaps: at 0.4 IoU between −0.9% and 3.0% for every change, including fourfold; at 0.7 IoU up to 9.4%.
- **Source:** Griesbacher C., Fruhwirth-Reisinger C. (TU Graz), "An Investigation of Beam Density on LiDAR Object Detection Performance", 28th Computer Vision Winter Workshop, Graz, 12–14 Feb 2025; arXiv 2503.15087 v1 (19 Mar 2025), https://arxiv.org/abs/2503.15087. Read: §5.1 and Eq. (1) (p. 6), Tables 5–6 (p. 7), Tables 7–8 and §5.5 text (p. 8), Table 1 (p. 3), Tables 10–12 (p. 13). Full text, all 13 pages rendered.
- **Evidence tag:** [I]
- **Confidence:** High; the definition, the sentence and the tables were read and cross-checked.
- **Proposed edit:**
  - `old`:
```
The TU Graz beam-density study (2025) found that training on *denser* data generalized better across 32–128 beams, with gaps under about 3% for modest density changes [I, arXiv 2503.15087; figures taken from the paper's summary and not re-read from its tables].
```
  - `new`:
```
The TU Graz beam-density study (2025) found that training on *denser* data generalized better across 32–128 beams when detection is scored at the loose 0.4 IoU threshold (§C10.6(i)), and that halving or doubling the beam count at test time (for example from 128 to 64 beams, or from 32 to 64) widened the domain gap by at most about 3 percentage points at the strict 0.7 threshold, against about 12 points for a fourfold change [I, arXiv 2503.15087, Eq. (1), Tables 7–8]. The domain gap is the shortfall in vehicle AP (PV-RCNN++) expressed as a percentage of the AP of the same detector trained on the target data, so the 3 points are a change in a relative gap, not mAP points.
```
- **Appendix 2 entry:** none (listed under *Resolution value, regulations and datasets* as "Griesbacher & Fruhwirth-Reisinger, beam density study").

---

## R7_E9-E12-05

- **Question:** Who is Ushr, and does the WSJ article (11 Oct 2018) or another source confirm that it supplies the HD map for GM's Super Cruise?
- **Answer:**
  - **The WSJ article.** "Ushr makes the Super Cruise system's maps", says Christopher Thibodeau, Ushr's senior vice president and general manager, describing terabytes of map data "boiled down to a few hundred megabytes of relevant route information". The figures in the report's cell are confirmed: Ushr's database covered "about 200,000 miles of controlled-access highways in North America", and 6,000–8,000 miles of it changed each year ($6{,}000/200{,}000=3\%$, $8{,}000/200{,}000=4\%$).
  - **Ushr's own release** (Detroit, 18 Oct 2017) says its precision HD map platform "has been implemented in the new Cadillac Super Cruise" hands-free highway feature. It says Ushr mapped every mile of limited-access highway in the US and Canada with lidar, to under four inches, and would supply frequent updates to GM.
  - Ushr was later acquired by Japan's Dynamic Map Platform (2019), which is background and not needed in the text.
- **Source:**
  - Christopher Mims, "The Key to Autonomous Driving? An Impossibly Perfect Map", *The Wall Street Journal*, 11 Oct 2018. Printout supplied by the report's owner (`refs/2018-10-11_WSJ_The-Key-to-Autonomous-Driving-An-Impossibly-Perfect-Map.pdf`), pp. 2, 3 and 5. Full text, rendered pages.
  - Ushr Inc., "Ushr Powers HD Map Data for Cadillac Super Cruise", press release, PR Newswire, 18 Oct 2017, https://www.prnewswire.com/news-releases/ushr-powers-hd-map-data-for-cadillac-super-cruise-300538822.html (full text of the release).
- **Evidence tag:** [P] for Ushr's release; [T] for the WSJ.
- **Confidence:** High; two independent texts agree.
- **Proposed edit:**
  - `old`:
```
maps age (in 2018, 6,000–8,000 of Ushr's ≈200,000 mapped highway miles, 3–4%, changed each year)
```
  - `new`:
```
maps age (in 2018, 6,000–8,000 of the ≈200,000 highway miles mapped by Ushr, the HD-map supplier for GM's Super Cruise [P, Ushr, 18 Oct 2017], 3–4%, changed each year)
```
- **Appendix 2 entry:** under *Software, data and ADAS validation*:
  - `- Ushr, lidar-built HD map implemented in Cadillac Super Cruise (18 Oct 2017): https://www.prnewswire.com/news-releases/ushr-powers-hd-map-data-for-cadillac-super-cruise-300538822.html`

---

## R7_E9-E12-06

- **Question:** (1) What, besides a constant electrical load, does Brown *et al.*'s range extrapolation contain that could explain 5.6% and 12.2%? (2) Which two computers make up the 325 W?
- **Answer:**
  - **(2) The two computers.** Table IV gives "Actual [W]" (measured, averaged over the combined UDDS/HWFET cycle) of **125 W for the Nuvo-8108GC XL** and **200 W for the HP Omen laptop**: $125+200=325$ W. The Nuvo is the computer "equipped with a 12GB RTX 3060 GPU" (§II-A; the HP Omen laptop runs "separate fusion and path planning algorithms for redundancy").
    - The reviewer's reading is therefore right. Note a coincidence that could mislead: the Nuvo's *theoretical* rating in the same table is also 325 W.
    - Table IV lists per-unit values; its totals, 765.4 W theoretical and 446.7 W actual, are reproduced only when the Table I quantities are applied (6 Basler cameras, 2 Aptiv radars, 2 GNSS receivers, 2 LAN switches).
    - Sensing and instrumentation alone come to $446.7-325=121.7$ W, the report's ≈122 W.
  - **(1) What the range figures contain.** The paper does not compute its range losses from the Table IV loads.
    - Each configuration was driven once on the dynamometer over one combined UDDS + HWFET cycle (17.71 mi, 2,149 s), starting at 95% state of charge. The drop in state of charge was obtained by integrating the battery current (its Eq. (1)), because the CAN-reported state of charge had only 0.5% resolution.
    - Table III gives the drops: 10.36% for the bare car, 11.05% with sensing, 11.9% with sensing and compute. It then gives the range "if the UDDS/HWFET combined drive cycle was iterated until the battery depletes": 127.5, 120.4 and 112.0 mi, hence −5.6% and −12.2%.
    - The two percentages therefore include everything else that differed between the three runs: conversion losses from the high-voltage battery to the 12 V bus, which the paper notes is charged from the high-voltage battery; any recharge of the 12 V battery; and run-to-run scatter in dynamometer road load and charge integration.
    - The paper reports no repeat runs or uncertainties. Its own validation against Argonne's dynamometer data for the same car and cycle differed by 1.64 points of final charge (Table II), and it calls a 3% charge error over a cycle "reasonable". Both exceed the 0.69- and 0.85-point increments behind 5.6% and 12.2%.
  - **Size of the discrepancy.** Kia specifies a 27 kWh (360 V) pack. With it [E; script `R7_brown_itsc2023_check.py`]:
    - Baseline draw: $0.1036\times27\ {\rm kWh}/0.597\ {\rm h}\approx4.69$ kW mean battery power, i.e. 9.8 kWh/100 km at the cycle's mean 47.7 km/h.
    - Sensing increment: $0.0069\times27/0.597\approx0.31$ kW (≈310 W), against 122 W tabulated.
    - Compute increment: $0.0085\times27/0.597\approx0.38$ kW (≈380 W), against 325 W tabulated.
    - Through the report's Eq. (158) (fractional loss $x/(e_0+x)$; numbered 165 before the equations were renumbered), an equivalent constant load is $\Delta P=P_0\,L/(1-L)$, with $P_0$ the baseline mean battery power and $L$ the fractional loss. Substituting $L=0.056$ and $L=0.122$ gives $4.69\times0.056/0.944\approx0.28$ kW and $4.69\times0.122/0.878\approx0.65$ kW, about 2.3× and 1.5× the tabulated 122 W and 447 W.
    - Conversely, the tabulated loads would give only $0.122/(4.69+0.122)\approx2.5\%$ and $0.447/(4.69+0.447)\approx8.7\%$.
    - The extrapolation is also not exactly inverse to the measured drops. Pure $1/\Delta{\rm SoC}$ scaling gives $1-10.36/11.05=6.2\%$ and $1-10.36/11.9=12.9\%$, and the three ranges imply slightly different usable windows (74.6, 75.1 and 75.3 points of charge). The paper does not describe that step.
  - **Bottom line.** The report's caution not to rescale the percentages is right. The specific reason is that the percentages are single-run battery-side measurements whose increments correspond to about 310 W and 380 W, not to the 122 W and 325 W measured at the components.
  - **Side observation.** The report's link to the paper on files.wmich.edu returned "AccessDenied" (HTTP 403) on 5 Oct 2026. The accepted manuscript is on OSTI (optional edit (c)).
- **Source:**
  - Brown N. E., Motallebiaraghi F., Fanas Rojas J., Ayantayo S., Meyer R., Asher Z. D. (Western Michigan University), Ekti A. R., Wang C. (ORNL), Goberville N. A. (Argonne), Feinberg B. (Sandia), "Evaluation of Autonomous Vehicle Sensing and Compute Load on a Chassis Dynamometer", 2023 IEEE 26th International Conference on Intelligent Transportation Systems (ITSC), doi:10.1109/ITSC57777.2023.10422013. Read: accepted manuscript at OSTI (record 2311313), https://www.osti.gov/servlets/purl/2311313, all 7 pages rendered, with §II-A–E, Tables I–IV (Tables III–IV zoomed at 300 dpi), Fig. 5 and §IV.
  - Kia Motors America, "2015 Soul EV Overview", https://www.kiamedia.com/us/en/media/pressreleases/9382/2015-soul-ev-overview (27 kWh, 360 V, 192-cell pack).
- **Evidence tag:** [I] for the paper; [P] for Kia's pack size; [E] for the implied loads.
- **Confidence:** High for the computers and for how the percentages were obtained; medium for the implied loads, which assume the nominal 27 kWh in the paper's charge integration (the paper takes capacity in Ah from Kia's specifications but does not print it).
- **Proposed edit (a), the computers:**
  - `old`:
```
including about **325 W** for the two computers.
```
  - `new`:
```
including about **325 W** for the two computers, the Nuvo-8108GC XL that carries the RTX 3060 (125 W) and the HP Omen laptop (200 W).
```
- **Proposed edit (b), what the percentages contain:**
  - `old`:
```
The two percentages are therefore not consistent with constant loads of the tabulated sizes, and they should not be rescaled to other loads [E].
```
  - `new`:
```
The two percentages are therefore not consistent with constant loads of the tabulated sizes, and they should not be rescaled to other loads [E]. The paper does not derive them from those loads. Each is extrapolated from one measured drop in battery state of charge over a single 17.71-mile cycle started at 95% charge (10.36% for the bare car, 11.05% with sensing and 11.9% with sensing and compute, its Table III), with the cycle repeated until the battery is depleted, so each includes everything else that differed between the three runs; the paper reports no repeat runs or uncertainties [I]. With the 27 kWh pack that Kia specifies [P], the extra 0.69 and 0.85 points of charge correspond to average battery-side draws of about 310 W and 380 W, against the tabulated 122 W and 325 W [E: $0.0069\times27\ {\rm kWh}/0.597\ {\rm h}\approx0.31$ kW and $0.0085\times27/0.597\approx0.38$ kW, with $2{,}149\ {\rm s}=0.597$ h]. The extrapolation is also not exactly inverse to the charge drops, which alone would give losses of 6.2% and 12.9% ($1-10.36/11.05$ and $1-10.36/11.9$).
```
- **Proposed edit (c), optional (dead link in the §E9 source line):**
  - `old`:
```
[Brown *et al.*, IEEE ITSC 2023 paper](https://files.wmich.edu/s3fs-public/attachments/u56/2023/IEEE_ITSC_2023__Evaluation_of_Autonomous_Vehicle_Sensing_and_Compute_Load_on_a_Chassis_Dynamometer.pdf)
```
  - `new`:
```
[Brown *et al.*, IEEE ITSC 2023 paper, accepted manuscript at OSTI](https://www.osti.gov/servlets/purl/2311313)
```
- **Appendix 2 entry:** under *Software, data and ADAS validation* (or a power group, if one is created):
  - `- Brown *et al.*, AV sensing and compute load on a chassis dynamometer, IEEE ITSC 2023 (OSTI accepted manuscript): https://www.osti.gov/servlets/purl/2311313`
  - `- Kia, 2015 Soul EV overview (27 kWh, 360 V pack): https://www.kiamedia.com/us/en/media/pressreleases/9382/2015-soul-ev-overview`

---

## R7_E9-E12-07

- **Question:** Is Huawei's "WA" route the vehicle-side model of the WEWA architecture named in §E10.1?
- **Answer:** Yes.
  - **Huawei's own pages.** The ADS product page shows "WEWA 2.0" with "Cloud: World Engine" and "Vehicle: World Action Model"; the Chinese page reads "云端：世界引擎" and "车端：世界行为模型". Huawei's release for its 23 Apr 2026 technology conference says that ADS 5 uses the WEWA 2.0 architecture, with the world model "located in the cloud" (位于云端) and a "vehicle-side world action model" (车端世界行为模型). WEWA 1.0 was introduced with ADS 4 in April 2025.
  - **The language layer.** In the KrASIA interview (translated from 36Kr, 12 Sep 2025), Jin Yuzhi, CEO of Huawei's Intelligent Automotive Solution BU, says "WA removes the language layer and directly turns perception into control". The article adds that WA turns visual, auditory and tactile data into driving actions "without converting everything into language first", and that Huawei built "its WEWA (world engine, world action) model" on this framework for ADS 4.0.
- **Source:**
  - Huawei Intelligent Automotive Solution, "HUAWEI ADS" product page, https://auto.huawei.com/en/ads, and Chinese page https://auto.huawei.com/cn/ads (WEWA 2.0 section), read 5 Oct 2026.
  - Huawei, "2026 华为乾崑技术大会在京举行" (23 Apr 2026), https://auto.huawei.com/cn/news/2026/2026-04-23-jishu (full text).
  - Fan Shuqi for 36Kr, "'Nothing is free': Huawei's Richard Jin on assisted driving and the path to Level 4 autonomy", KrASIA, 12 Sep 2025, https://kr-asia.com/nothing-is-free-huaweis-richard-jin-on-assisted-driving-and-the-path-to-level-4-autonomy (full text, read from the page source).
- **Evidence tag:** [P] for the architecture split; [T] for the language-layer statement, which is an executive interview relayed by trade press.
- **Confidence:** High; Huawei's own pages and its executive agree.
- **Proposed edit:**
  - `old`:
```
Huawei's "WA" (world–action) route deliberately skips the language layer and maps multimodal perception directly to actions [T].
```
  - `new`:
```
Huawei's WEWA architecture (§E10.1) pairs a cloud "world engine" (WE) with a vehicle-side "world action" (WA) model [P, Huawei ADS page], and the WA model deliberately skips the language layer, mapping multimodal perception directly to actions [T, KrASIA, Sep 2025].
```
- **Appendix 2 entry:** under *Chip-size limits, interference and fusion (§C8, §C9, §E10)*:
  - `- Huawei ADS page, WEWA cloud world engine and vehicle-side world action model: https://auto.huawei.com/en/ads`
  - The KrASIA interview line is given under item 08.

---

## R7_E9-E12-08

- **Question:** Which claims in §E11 do Lin *et al.* (ASPLOS 2018) and the KrASIA interview with Huawei's Jin Yuzhi support, given that neither is cited in the text?
- **Answer:**
  - **Lin *et al.*** support two §E11.3 points.
    - **(i) The 100 ms latency in the Synthesis.** §2.4.1 sets the performance constraint that the system process traffic conditions "within a latency of 100 ms at a frequency of at least once every 100 ms". §2.4.2 adds that this must hold for tail latency (99th to 99.99th percentile), not the mean.
    - **(ii) Compute power and range.** §2.4.5 and Fig. 2 estimate, for a Chevrolet Bolt, that a computing engine of one CPU and three GPUs at full utilization cuts driving range by 6%. The entire system cuts it by 11.5% once storage (about 8 W per 3 TB) and cooling are added. The cooling assumes an air conditioner with a coefficient of performance of 1.3, so "a 100 W system imposes 77 W cooling overhead". Fig. 2 bars: about 0.9 kW and 1.8 kW for that engine alone and in aggregate. This also gives §E9 an independent figure for the cooling term it tells readers to count.
    - The latency attachment is the natural one; the range sentence is optional.
  - **The KrASIA interview** supports §E11.2(c), Huawei's WA route skipping the language layer (item 07). It also supports the July 2025 figures in §E11.2(a): "As of July, one million vehicles had been equipped with Qiankun", lidar shipments "exceeded one million units", and assisted-driving mileage reached 4 billion km (item 09).
  - Both sources should stay in the §E11 source list, now with in-text tags pointing to them.
- **Source:**
  - Lin S.-C., Zhang Y., Hsu C.-H., Skach M., Haque M. E., Tang L., Mars J. (University of Michigan), "The Architectural Implications of Autonomous Driving: Constraints and Acceleration", ASPLOS '18, 24–28 Mar 2018, pp. 751–766, doi:10.1145/3173162.3173191. Read: §2.4.1–2.4.5 and Fig. 2 (pp. 4–6) of the camera-ready PDF. ACM lists the paper as free to read but blocked scripted downloads; the identical camera-ready copy with the ACM rights block was read from a university course page, https://people.computing.clemson.edu/~jmarty/projects/lowLatencyNetworking/papers/EmergingApplicationSystems/AutonomousVehicles/AutonomousCarConstraints.pdf. Rendered pages.
  - KrASIA interview as in item 07 (full text).
- **Evidence tag:** [I] for Lin *et al.*; [T] for KrASIA.
- **Confidence:** High; both sources were read in full and the attachments match their content.
- **Proposed edit (a), Lin *et al.* on latency:**
  - `old`:
```
At 36 m/s (about 130 km/h), 100 ms of end-to-end latency is $36\times0.1=3.6$ m.
```
  - `new`:
```
At 36 m/s (about 130 km/h), 100 ms of end-to-end latency is $36\times0.1=3.6$ m; 100 ms is the processing budget Lin et al. set for an autonomous-driving system, to be met at 10 or more frames per second and judged on tail latency, the 99th or 99.99th percentile of processing time [I, Lin et al., ASPLOS 2018, §2.4].
```
- **Proposed edit (b), optional, Lin *et al.* on compute power and range** (end of the §E11.3 compute-power bullet):
  - `old`:
```
so the slower the car, the more of that energy is spent per kilometre driven.
```
  - `new`:
```
so the slower the car, the more of that energy is spent per kilometre driven. Lin et al. estimate for a Chevrolet Bolt that a computer with one CPU and three GPUs at full load cuts range by about 6%, and the whole system by about 11.5% once storage and the air conditioning that removes its heat are counted (about 77 W of cooling per 100 W of load) [I, Lin et al., ASPLOS 2018, Fig. 2].
```
- **KrASIA:** attached by the edits of items 07 and 09(a); no separate edit.
- **Appendix 2 entry:** under *Software, data and ADAS validation*:
  - `- Lin *et al.*, architectural implications of autonomous driving (100 ms tail-latency budget; compute, storage and cooling cost in range), ASPLOS 2018: https://dl.acm.org/doi/10.1145/3173162.3173191`
  - `- KrASIA (36Kr), interview with Huawei's Jin Yuzhi on WA and Level 4 (12 Sep 2025): https://kr-asia.com/nothing-is-free-huaweis-richard-jin-on-assisted-driving-and-the-path-to-level-4-autonomy`

---

## R7_E9-E12-09

- **Question:** How do §E1's undated "More than 2 M vehicles; 14.5 B km [P]" and §E11.2(a)'s "1.7 million ADS vehicles by April 2026" fit together, according to Huawei's own releases?
- **Answer:** The two figures belong to different dates and do not conflict. Huawei's dated figures, all for vehicles fitted with Qiankun ADS (including the lidar-free ADS SE tier) and cumulative assisted-driving distance:

  | Date | Vehicles fitted | Cumulative assisted driving | Source |
  |---|---|---|---|
  | July 2025 | 1 million | 4 B km; lidar shipments above 1 million | Jin Yuzhi, KrASIA/36Kr, 12 Sep 2025 [T] |
  | 19–23 Apr 2026 | more than 1.7 million | more than 10 B km by 19 Apr | Huawei release, 23 Apr 2026 [P] |
  | end of Apr 2026 | — | 10.47 B km | Huawei April safety report [P] |
  | 16 Jul 2026 | more than 1.9 million (2 million forecast for end-August) | more than 12.8 B km | Huawei media-day release [P] |
  | end of Jul 2026 | — | 13.41 B km | Huawei July safety report [P] |
  | end of Aug 2026 | — | 14.71 B km | Huawei August safety report, published 4 Sep [P] |
  | 8 Sep 2026 | more than 2 million (with HarmonySpace cockpits and app users) | 14.9 B km (15.0 B km in another report of the same day) | Jin Yuzhi's post, relayed by Tencent News and others [T] |

  - §E1's "more than 2 M vehicles" is therefore the 8 Sep 2026 figure.
  - Its "14.5 B km" matches no dated Huawei figure found. It lies between 14.1 B km (17 Aug, trade press) and 14.71 B km (end-August, Huawei), so it is probably a reading of Huawei's live counter in late August. The end-August 14.7 B km from Huawei's own monthly report is the citable, dated number. By 2 Oct 2026 the counter was reported above 16 B km.
  - §E11.2(a)'s 1.7 million (April 2026) is confirmed by Huawei's own release.
- **Source:**
  - Huawei, "2026 华为乾崑技术大会在京举行", 23 Apr 2026, https://auto.huawei.com/cn/news/2026/2026-04-23-jishu: "整车搭载量已突破 170 万辆", and assisted-driving mileage above 10 B km as of 19 Apr.
  - Huawei, "2026 华为乾崑媒体日在深圳开幕", 16 Jul 2026, https://auto.huawei.com/cn/news/2026/2026-7-16-media-open-day: "总搭载量已突破 190 万台", above 12.8 B km, and the 2-million forecast.
  - Huawei, monthly safety reports, https://auto.huawei.com/cn/ads/safety-and-data-report/202604 (104.7 亿公里), /202607 (134.1 亿公里) and /202608 (147.1 亿公里); full text of each page.
  - Tencent News, "靳玉志宣布：华为乾崑智驾/鸿蒙座舱搭载量突破200万", 8 Sep 2026, https://news.qq.com/rain/a/20260908A05SBC00 (149 亿公里); 21st Century Business Herald via Tencent News, 8 Sep 2026, https://news.qq.com/rain/a/20260908A0DUN600 (150 亿公里).
  - KrASIA interview as in item 07.
- **Evidence tag:** [P] for Huawei's releases and reports; [T] for the 8 Sep milestone as relayed by press, and for KrASIA.
- **Confidence:** High for the dated figures; low only for the origin of the "14.5 B km", which could not be matched.
- **Proposed edit (a), §E11.2(a), in this block:**
  - `old`:
```
by July 2025, and **1.7 million** ADS vehicles by April 2026.
```
  - `new`:
```
by July 2025 [T, KrASIA, Sep 2025], **1.7 million** ADS vehicles by April 2026 [P, Huawei, 23 Apr 2026] and more than 2 million by 8 Sep 2026 (§E1) [T, Tencent News, 8 Sep 2026].
```
- **Proposed edit (b), §E1 table, outside this block** (for the editor of §E1):
  - `old`:
```
More than 2 M vehicles; 14.5 B km [P]
```
  - `new`:
```
More than 2 M vehicles (8 Sep 2026) [T]; 14.7 B km of assisted driving to end-Aug 2026 [P]
```
- **Appendix 2 entry:** under *Lidar market and Western programs* (or *Chip-size limits, interference and fusion*):
  - `- Huawei, 2026 Qiankun technology conference (more than 1.7 M ADS vehicles; 10 B km by 19 Apr 2026): https://auto.huawei.com/cn/news/2026/2026-04-23-jishu`
  - `- Huawei, August 2026 safety report (14.71 B km of assisted driving): https://auto.huawei.com/cn/ads/safety-and-data-report/202608`
  - `- Tencent News, Jin Yuzhi announces more than 2 M ADS installations (8 Sep 2026): https://news.qq.com/rain/a/20260908A05SBC00`

---

## R7_E9-E12-10

- **Question:** Is Light's "10 cm to 1 km" for Clarity a span of distances or an object size at a range, like NODAR's "10 cm object at 150 m"?
- **Answer:**
  - **A span of distances.** The Robot Report's launch article says Light claimed Clarity "is able to see any 3D structures in the road from 10 cm to 1 km (3.9 in. to 0.62 mi.) away". The same article quotes Light's CEO, Dave Grannan: "The best lidar today has a range of 250 meters, not 1,000 meters." The 2022 Deere article repeats it as seeing "3D structures at a range from 10 cm to 1000 m".
  - **The parallel with NODAR therefore misleads.** NODAR's "10 cm object at 150 m" is an object size at a stated range; Light's figure is a minimum and maximum working distance with no object size attached.
  - **The parenthesis "(now John Deere)" is loose.** Deere acquired "numerous patents and other intellectual property from Light" and hired a team of its employees in May 2022, and later clarified that it did not acquire all of Light. The proposed text says so without the word "now".
- **Source:**
  - Eugene Demaitre, "Clarity multicamera perception platform for vehicles launched by Light", *The Robot Report*, 27 Oct 2020, https://www.therobotreport.com/clarity-perception-platform-autonomous-vehicles-light-launches/ (full text).
  - "John Deere acquires Light's camera-based perception platform", *The Robot Report*, 19 May 2022, https://www.therobotreport.com/john-deere-acquires-light-camera-based-perception-platform/ (full text).
- **Evidence tag:** [T]
- **Confidence:** High; the wording is explicit in both articles.
- **Proposed edit:**
  - `old`:
```
Light's Clarity (now John Deere) claimed 10 cm to 1 km [T].
```
  - `new`:
```
Light's Clarity, whose patents and part of whose team John Deere acquired in 2022, claimed to see any 3D structure in the road at distances from 10 cm to 1 km, a span of range rather than an object size [T, The Robot Report, 27 Oct 2020 and 19 May 2022].
```
- **Appendix 2 entry:** under *Camera-only vs multimodal*:
  - `- The Robot Report, Light's Clarity launch (10 cm to 1 km depth range claim, 27 Oct 2020): https://www.therobotreport.com/clarity-perception-platform-autonomous-vehicles-light-launches/`
  - `- The Robot Report, John Deere acquires Light's perception patents and team (19 May 2022): https://www.therobotreport.com/john-deere-acquires-light-camera-based-perception-platform/`

---

## Check of the `old` strings

Run with `sources/scripts/R7_check_old_strings.py` against the report at SHA-256 prefix 51d60fa27199. All 16 `old` strings occur exactly once.

| Item | Edit | Location in the report | Count |
|---|---|---|---:|
| 01 | MEFormer retrained | §E11.1, finding 2 | 1 |
| 02 | Fusion4CA baseline schedule | §E11.1, finding 1 | 1 |
| 03 (a) | Rimrock time, UTC convention | §E12.2, "Reading the pattern", first bullet | 1 |
| 03 (b) | table header | §E12.2, SGO table | 1 |
| 03 (c) | night, dawn or dusk (optional) | §E12.2, "Reading the pattern", second bullet | 1 |
| 04 | TU Graz domain gap | §E11.2(b) | 1 |
| 05 | Ushr identified | §E10.1 table, role 5 | 1 |
| 06 (a) | the two computers | §E9, "Measured anchor", Power bullet | 1 |
| 06 (b) | what the percentages contain | §E9, Power bullet, last sentence | 1 |
| 06 (c) | dead WMU link (optional) | §E9, source line | 1 |
| 07 | WEWA and WA | §E11.2(c), counter-examples | 1 |
| 08 (a) | Lin *et al.*, latency | §E11.3, Synthesis | 1 |
| 08 (b) | Lin *et al.*, range (optional) | §E11.3, point 4, compute-power bullet | 1 |
| 09 (a) | Huawei fleet dates | §E11.2(a) | 1 |
| 09 (b) | §E1 cell (outside this block) | §E1 table, Huawei row | 1 |
| 10 | Clarity range span | §E12.1 | 1 |

In this version the range-loss formula of §E9 is Eq. (158), not Eq. (165); none of the `new` strings cite an equation number, and the Answer of item 06 uses the current number. No `old` string had moved, disappeared, or already carried its source.
