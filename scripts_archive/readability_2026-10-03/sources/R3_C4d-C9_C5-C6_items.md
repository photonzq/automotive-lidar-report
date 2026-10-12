# Round 4 source items: R3_C4d-C9_C5-C6

## R3_C4d-C9_C5-C6-01 [05_C4d_C8_C9] report #11 (pre-2024 units; fleet size)

- **Where:** §C9, 'Sales penetration is not fleet share': "earlier years" and "a Chinese car fleet assumed at ≈350 M"
- **What is needed:** The edit shows the 2024–2026 arithmetic (5.5–7.6 M lidar cars) and tags the fleet [U]. Closing the 6–8 M estimate needs China's lidar installations before 2024 (2022–2023) and a source for the ≈350 M car fleet.

## R3_C4d-C9_C5-C6-02 [05_C4d_C8_C9] report #17 (upper end)

- **Where:** §C8.2 item 3: "draw about 1–25 mW per $\pi$ of phase shift each"
- **What is needed:** The 25 mW/π upper end, and the 25 W total it gives, has no source in the report and stays tagged [U]; a citation for a high-power thermo-optic shifter would firm it or replace it with the 13 mW/π of §C10.2b.

## R3_C4d-C9_C5-C6-03 [05_C4d_C8_C9] report #33 (InnovizOne 60/75 m)

- **Where:** §C4d subsection 4 table, 2-D MEMS row: "60/75 m outside, at 20 klx [P]"
- **What is needed:** Which of 60 and 75 m is native and which uses pixel summation must be read from the InnovizOne series-production datasheet. If 60 m is native: "…(140 m with pixel summation) and 60 m native (75 m with summation) outside it, at 20 klx [P]".

## R3_C4d-C9_C5-C6-04 [05_C4d_C8_C9] consistency flag #8 (68 vs 64 channels)

- **Where:** §C8.1 table, SiPM row: "ATX: **17 SiPM dies × 4 channels** [T]" (also §C4b's family table and §C10.7) vs §C4b: "The ATX uses 64 physical channels"
- **What is needed:** 17 × 4 = 68 against 64. Reconciling them (for example spare or reference channels) needs the TechInsights teardown DDT-2505-806, which is paywalled.

## R3_C4d-C9_C5-C6-05 [05_C4d_C8_C9] consistency flag #14

- **Where:** §C4d subsection 1 table, one-axis row: "The Feb 2026 manual calls it a "1-D rotating mirror (hybrid solid-state)""
- **What is needed:** §C3b and the §E9 note date the ATX S01 manual A07 to May 2026, and the linked file name ends -260520. Confirm the manual's own date; if May 2026, write "The ATX S01 user manual (A07, May 2026, §E9) calls it…".

## R3_C4d-C9_C5-C6-06 [05_C4d_C8_C9] consistency flag #19

- **Where:** §C4d 2(a): "RoboSense M1 (125 lines at 15 Hz [P])"
- **What is needed:** 125 lines at 15 Hz with the 787,500 pts/s of 2(b) (an M1 Plus figure) implies 420 points per line (≈0.29° over 120°); at 10 Hz it would be 630 points (≈0.19°), $S=1{,}250$ sweeps/s and $f_{\rm mirror}=0.63$ kHz. Confirm the M1 frame rate from the RoboSense specification; panel (d) and the 0.3–0.94 kHz range depend on it.

## R3_C4d-C9_C5-C6-07 [06_C5_C5a_C6] report #7

- **Where:** §C5 Fastree3D timeline, row 2013–2020: "rising to **CHF 429,444** by Aug 2020, mostly through six conversions of loans into shares totalling ≈CHF 3.3 M"; and the 'Per share' bullet of "Was it a success?"
- **What is needed:** The edit shows the division and flags the CHF 1 nominal assumption [U]. Still needed from the Vaud commercial register (or SOGC notices): (1) the nominal value per share, to confirm that CHF 429,444 of capital is 429,444 shares; (2) all six loan-to-equity conversions with date, CHF converted and shares (or nominal capital) created. Only four implied prices are given, and at CHF 1 nominal, CHF 3.3 M converted at CHF 27–48 creates only ≈69k–122k shares against a 329,444 increase described as 'mostly through six conversions', so the row does not close; (3) the CHF/USD rate used to turn the \$7.67 M price into CHF 6.7 M (the figures imply ≈0.87 CHF per dollar, December 2023), so the conversion can be shown with its substitution.

## R3_C4d-C9_C5-C6-08 [06_C5_C5a_C6] report #24 (part) and §3 flag 4

- **Where:** §C5a, IMX560 list: "**3.5 kcps typical, 6 Mcps maximum, per SPAD**" and "dead time 15 ns typical at 99% accumulation"
- **What is needed:** Check the IMX560-AAMV flyer: whether the 6 Mcps maximum (1,700× the typical value) is the worst SPAD of the array or a kcps/Mcps slip, and what "at 99% accumulation" means; then gloss both. The 15 ns versus 6 ns reconciliation is applied as an edit.

## R3_C4d-C9_C5-C6-09 [06_C5_C5a_C6] report #32 (verification)

- **Where:** §C5a AS-DT1 table, Depth output: "four mode settings: 20 m and 30 m at 30 fps, and 30 m and 40 m at 15 fps [P, spec sheet]" (text after the edit)
- **What is needed:** The edit states the four settings that the existing sentence implies. Confirm against the AS-DT1 spec sheet that a 30 m range exists at both 30 fps and 15 fps; if not, correct the duplicated 30 m.

## R3_C4d-C9_C5-C6-10 [06_C5_C5a_C6] report #36 (V-series sentence)

- **Where:** §C5 table, Hesai FTX / ETX row: "**No Hesai "V-series" chip name exists**; the generations are the 4th-gen ASIC, Fermi C500 and Picasso"
- **What is needed:** The sentence rebuts a label the reader never sees, and the report does not say where "V-series" appears. Name the article or secondary source that uses it, then write that Hesai's own documents use no such name and that its generations are the 4th-gen ASIC, Fermi C500 and Picasso. The table lead-in and the column rename are applied as edits.

## R3_C4d-C9_C5-C6-11 [06_C5_C5a_C6] report §3 flag 2 (ATX channel count)

- **Where:** §C5 table: "| Hesai ATX | SiPM (17 dies / 64 channels), TI, 3peak and Infineon parts [I] |"
- **What is needed:** §C4b and two later tables give "17 SiPM dies × 4 channels" (= 68), while §C4b also says "The ATX uses 64 physical channels". Check the TechInsights ATX teardown (DDT-2505-806, paywalled) for the die and channel counts (for example 16 receiving dies × 4 = 64 plus one other die) and align all places.

## R3_C4d-C9_C5-C6-12 [06_C5_C5a_C6] report §3 flag 13 (Fastree3D founding and seat)

- **Where:** §C5 Fastree3D timeline: "| Sep 2013 / 2014 | Fastree3D SA incorporated in Lausanne (EPFL Innovation Park; office in Delft)"; "statutes 1 Jul 2013, seat Ecublens"; "**Fastree3D SA** (Switzerland, Sep 2013, capital CHF 429,444)"; "the registered address moves to the EPFL Innovation Park (the legal seat stays Ecublens)"
- **What is needed:** The founding date (statutes 1 Jul 2013, Sep 2013, and "/ 2014") and the 2013 address (EPFL Innovation Park versus seat Ecublens, with the address moving to the Innovation Park only in 2024) disagree. Check the Vaud register (statutes date versus registration date, and the 2013 address) and the company 'About' page, then make the three rows consistent.

## R3_C4d-C9_C5-C6-13 [06_C5_C5a_C6] report §3 flag 17 (EM4 field of view)

- **Where:** §C6 R²·FOV table: "| RoboSense EM4 (1 scan axis) | 120°×27° |", against IMX479's "over 120° × 26°" in the §C5a table
- **What is needed:** EM4-520 is 'most likely IMX479' (§C5), whose stated coverage is 120° × 26°, while the EM4 row (and §C10) use 27°. Confirm EM4's vertical field on RoboSense's product page; if 27° is right, add a short note that the lens, not the chip, sets the product's field.
