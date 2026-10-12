# Round 4 source items: R2_C0_C4

## R2_C0_C4-01 [02_C0_parts1-9] report #36 (k values have no source tag)

- **Where:** §C0 subsection 6 table: «≈0.02» (silicon) and «≈0.4–0.5» (InGaAs/InP), and the practical gains «≈50–200» and «≈10–20»
- **What is needed:** No source for these values is cited anywhere in the report (§C4 states the InP value without a tag), so this list tags them [U]. A textbook or review reference for $k$ and practical APD gain would let them be tagged [I].

## R2_C0_C4-02 [02_C0_parts1-9] consistency flag (VL53L5 resolution)

- **Where:** §C0 subsection 9: «VL53L5 14 × 10 macro-pixels [I]» (chip table), «VL53L5/L8: 8 × 8 zones» (makers table), «4 × 4 SPADs on the VL53L5»; also §B8
- **What is needed:** The three descriptions are not reconciled: how the 14 × 10 macro-pixels (of 4 × 4 SPADs) are binned into the 8 × 8 output zones needs a source (ST datasheet or a teardown).

## R2_C0_C4-03 [03_C0_part10] report #9 (second part); report §3 flag 10

- **Where:** 10.7, What coherent detection changes, Evidence: "although the retroreflector was 37.7 dB brighter [P]"
- **What is needed:** Settembrini et al. (2026): state whether the 37.7 dB (retroreflector against the 5% target at 7.2 m) and the 31.8 dB in 'Measured at a lidar wavelength' (against the 50% target) come from different measurements or ranges. As written they disagree by 4 dB: 31.8 dB above a 50% target is 41.8 dB above a 5% target.

## R2_C0_C4-04 [03_C0_part10] report #11 (part)

- **Where:** 10.8, How the numbers are derived, Wang: "For an assumed $T$ of 18–40 µs [E]"
- **What is needed:** Wang et al. 2025: the integration time T of one measurement (chirp duration). The edit shows the estimate (an SNR of 10 at 200 m needs eta*P_tx*T of about 2e-7 J) and states the 18-40 µs that reproduces the 5-11 mW previously quoted; if the paper gives T, use eta*P_tx = 2e-7 J / T and redo the transmitted power at eta = 0.25.

## R2_C0_C4-05 [03_C0_part10] report #13 (unit of Waymo's 50); report §3 flag 3

- **Where:** 10.8 coherent table, Waymo design point, published cell: "50 photons; $P_D=0.9$"; 10.3: "Waymo's 50 photoelectrons for 90% detection"; §C7a(a): "Waymo's analysis uses **50 photoelectrons for 90% detection**"
- **What is needed:** Check Piggott et al. 2025 (Table 1 and the detection discussion): are Waymo's 50 photons or photoelectrons? The model gives 49 photons per chirp, i.e. 44 photoelectrons at QE 0.9, against 44.9 needed at 1e-6 per bin with four looks, which fits '50 photons' better. If they are photons, change 10.3 and §C7a(a) to '50 photons (45 photoelectrons at QE 0.9)'; if photoelectrons, change this cell to '50 photoelectrons'.

## R2_C0_C4-06 [04_C4_C4b_C4c] report #20

- **Where:** §C4c subsection 4, cold caveat bullet: 'where eye safety is set by the Class 3B cap'
- **What is needed:** The report never explains a Class 3B cap at 1,310 nm. Needs the IEC 60825-1:2014 rule (C7 over 1,150–1,400 nm and the Class 3B ceiling) before writing: 'There the retinal factor C7 makes the Class 1 retinal limit so lenient that the binding limits become the cap at the Class 3B level and, in Europe, the A11 corneal limit for 1,250–1,400 nm (subsection 1).' The A11 part is applied.

## R2_C0_C4-07 [04_C4_C4b_C4c] report #31

- **Where:** §C4c subsection 3 cost table, InP substrate price row: '[T, unattributed; internally inconsistent]'
- **What is needed:** The report does not say which figures conflict (2″ $800 → $2,300–2,500; 6″ $1,400 → $5,000). Name the conflict from the source in one clause, or re-source the prices.

## R2_C0_C4-08 [04_C4_C4b_C4c] report #38 (fog row)

- **Where:** §C4c subsection 5 table, Fog row: 'near-IR ≈10% worse only in very dense advection fog (<30 m visibility)'
- **What is needed:** Confirm against Duthon et al. 2019 which band is worse before rewriting as '905 nm ≈10% worse than 1,550 nm only in very dense advection fog (<30 m visibility)'.

## R2_C0_C4-09 [04_C4_C4b_C4c] follow-up #1; report polish (3278)

- **Where:** §C4 item 3: 'Seyond's Falcon K drew 30 W [U]'
- **What is needed:** No source for 30 W anywhere in the report; tagged [U] meanwhile. Needs a Falcon K/K1 datasheet or manual figure. If none: drop it, and in §C4d change '1.75 kg, 20–30 W and fibre-laser cost (§C4)' to '1.75 kg, 20 W (Falcon K2 datasheet [P], §E9) and fibre-laser cost (§C4)'; §0 and §E11 ('6–20 W') then stand.

## R2_C0_C4-10 [04_C4_C4b_C4c] follow-up #2

- **Where:** §C4 item 2: 'Front-side-illuminated SPADs … reached only 2–5% PDE at 9xx nm [U]'
- **What is needed:** No source anywhere in the report; tagged [U] meanwhile. Add a source, or write 'single-digit PDE [U]' and reconcile with §C4b's 'Historically about 5–10% (front-side)' for SiPMs.

## R2_C0_C4-11 [04_C4_C4b_C4c] follow-up #3

- **Where:** §C4c Sources line ('Sources: https://webstore.iec.ch/en/publication/3587 ; …')
- **What is needed:** Links missing for: GlobalFoundries Ge photodiode, OFC 2025; Chen et al., JAP 2016; Hale & Querry; Kou; Artilux Ge-on-Si SPAD; Fudan/Zhangjiang Lab/Innolight (perhaps arXiv 2605.07343); Rogers et al., Nature 2021 (perhaps arXiv 2008.02411); Hamamatsu G8931-20 price [T]; SiLC 'germanium detectors' [T]. Confirm before labelling: s41467-019-08830-w (Vines et al.?), PMC12113715 (Liu et al., Micromachines 2025?), arXiv 2112.08936 (survey relaying Wojtanowski?), photonics.intec.ugent.be pub_3746, IEC webstore 62424.

## R2_C0_C4-12 [04_C4_C4b_C4c] follow-up #5

- **Where:** End of §C4 and §C4b (no Sources line); §C4 item 7 'KrASIA, summarising Seyond's prospectus: the InGaAs route costs 2–3× as much as 905 nm [T]'
- **What is needed:** No URL anywhere for the KrASIA summary (§G3 points back to §C4), the Yole view [MR/S] or the RoboSense M3 '50–70% cheaper' pitch [P]. Add a Sources line to §C4 with these. Pointers to §C2, §C3, §C3b and §E9 are applied for NE Times and the power figures.

## R2_C0_C4-13 [04_C4_C4b_C4c] report #7 (K3 range)

- **Where:** §C4 'Where 1,550 nm survives': 'Seyond Falcon K3, 450 m at 10%, §C3'
- **What is needed:** The 450 m at 10% has no source or tag anywhere (§C3, §C4d, §F). A Seyond source would allow [P].

## R2_C0_C4-14 [04_C4_C4b_C4c] report #32 (rank)

- **Where:** §C4b 'Where each wins': 'Hesai's ATX, by its delivery count the best-selling long-range lidar [U]'
- **What is needed:** Tagged [U]. Huawei also reports more than 1 M lidars shipped by July 2025 (Part E, [T]). Source the rank, or soften to 'one of the best-selling long-range lidars'.
