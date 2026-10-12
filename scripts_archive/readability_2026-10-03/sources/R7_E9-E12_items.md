# Round 4 source items: R7_E9-E12

## R7_E9-E12-01 [11_E9-E12] report #4 (part)

- **Where:** §E11.1, 'What the tables show', finding 2: "and MEFormer 70.5, 3.6 above it"
- **What is needed:** The report does not say whether Grace-BEV retrained MEFormer or quoted its 70.5 / 72.7 from the MEFormer paper (as it does for MetaBEV). Needs Grace-BEV (arXiv 2605.30983), Table 1 notes. If quoted, add after the MEFormer figure: 'quoted, like MetaBEV's, from its own paper'; if retrained, add 'retrained by Grace-BEV'.

## R7_E9-E12-02 [11_E9-E12] report #7 (part)

- **Where:** §E11.1, finding 1: "above the BEVFusion-MIT camera + lidar baseline of the same table, which was trained on its full schedule"
- **What is needed:** The training schedule (epochs) of the BEVFusion-MIT baseline in Fusion4CA's Table I is not in the report (Fusion4CA itself: 6 epochs), so the text cannot say whether the +1.2 mAP compares runs of equal training. Needs Fusion4CA (arXiv 2603.05305), Table I and training setup; then replace 'which was trained on its full schedule' with 'which was trained for N epochs'.

## R7_E9-E12-03 [11_E9-E12] report #10

- **Where:** §E12.2, 'Reading the pattern': "SGO times can also be imprecise: the Rimrock record gives 00:03, while the ODI resume dates the fatal crash to 28 Nov 2023."
- **What is needed:** The date that SGO report 13781-8004 gives with its 00:03 time, and what in the ODI resume conflicts with it, are needed to make the imprecision visible; then add 'the time is therefore omitted from the table'. Needs the SGO archive record and the EA26002 resume.

## R7_E9-E12-04 [11_E9-E12] report #16

- **Where:** §E11.2(b): "with gaps under about 3% for modest density changes [I, arXiv 2503.15087; figures taken from the paper's summary and not re-read from its tables]"
- **What is needed:** Whether the 3% is mAP points or per cent of the dense-trained score, and which beam-count change counts as 'modest' (e.g. 128 to 64 beams). Needs the TU Graz paper's tables (arXiv 2503.15087).

## R7_E9-E12-05 [11_E9-E12] report #18 (part)

- **Where:** §E10.1 table, role 5, weaknesses: "6,000–8,000 of Ushr's ≈200,000 mapped highway miles"
- **What is needed:** Ushr is not identified anywhere in the report. Once confirmed from the WSJ article (11 Oct 2018) or another source, write 'of the ≈200,000 highway miles mapped by Ushr (the HD-map supplier for GM's Super Cruise)'.

## R7_E9-E12-06 [11_E9-E12] report #20 (part)

- **Where:** §E9, 'Measured anchor': "including about **325 W** for the two computers"
- **What is needed:** (1) What besides a constant electrical load the paper's range extrapolation contains, which would explain 5.6% and 12.2% (Round 1 adds the Eq. (165) check: ≈3.7% expected for ≈122 W); (2) which two computers make up the 325 W (the reviewer suggests the RTX 3060 machine and the laptop). Needs Brown et al., IEEE ITSC 2023, method section and component table.

## R7_E9-E12-07 [11_E9-E12] report #28 (part)

- **Where:** §E11.2(c), counter-examples: "Huawei's \"WA\" (world–action) route deliberately skips the language layer"
- **What is needed:** Whether Huawei's 'WA' route is the vehicle-side model of the WEWA architecture named in §E10.1 is not stated in the report. If confirmed, write: 'Huawei's WEWA architecture (§E10.1), whose vehicle-side "WA" (world–action) model deliberately skips the language layer and maps multimodal perception directly to actions [T]'. Round 1 expands ADS as Huawei's brand at its first use in §E10.1.

## R7_E9-E12-08 [11_E9-E12] report #32 (part)

- **Where:** §E11 source list: "[Lin et al., ASPLOS 2018](https://dl.acm.org/doi/10.1145/3173162.3173191)" and "[Huawei's Jin Yuzhi interview, KrASIA](https://kr-asia.com/nothing-is-free-huaweis-richard-jin-on-assisted-driving-and-the-path-to-level-4-autonomy)"
- **What is needed:** Neither is cited in the §E11 text. After checking the sources, attach each to the claim it supports (Lin et al. possibly to the compute-power or latency points of §E11.3; the KrASIA interview possibly to Huawei's 'WA' route in §E11.2(c)), or drop them from the list.

## R7_E9-E12-09 [11_E9-E12] consistency flag: Huawei ADS fleet size

- **Where:** §E11.2(a): "and **1.7 million** ADS vehicles by April 2026"
- **What is needed:** §E1 gives 'More than 2 M vehicles; 14.5 B km [P]' with no date. Date the §E1 figure or reconcile the two from Huawei's own releases (the §E1 change is outside this block).

## R7_E9-E12-10 [11_E9-E12] consistency flag: ambiguous parallel

- **Where:** §E12.1: "Light's Clarity (now John Deere) claimed 10 cm to 1 km [T]."
- **What is needed:** Say whether '10 cm to 1 km' is a depth span or an object size at a range, as NODAR's '10 cm object at 150 m' is. Needs The Robot Report article on Clarity.
