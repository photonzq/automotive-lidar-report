All four checks are finished, using the report file only. Line numbers are approximate; find each item by its heading or quote. Where an unlabelled URL is matched to a paper, the match rests on its venue or ID; the paper was not opened.

**Item 3, in one line:** the Luminar figures in §C4 and §C4c (\$110 M and \$33 M, February 2026, MicroVision as buyer of the lidar business) agree with §C3a. Only the wording in finding 6 needs fixing.

## New findings

1. **Line** ≈3295, §C4 item 3 "Source, power and heat" — **E/B** — **medium**
   - **Quote:** "Falcon K drew 30 W and K2 20 W, against about 6–10 W for 9xx-nm units (Robin E1X, Hesai ATX)."
   - **Problem:**
     - The 30 W has no source or tag anywhere in the report.
     - Everything else in the sentence is sourced elsewhere: the K2's 20 W in the §C3 notes ("The Falcon K2 datasheet gives 500 m maximum range and 20 W") and §E9 ("Seyond Falcon K2, 1550 nm lidar | **20 W** [P]"). Robin E1X 6 W is in the §C3 notes [P]; ATX 8 W [P], 10 W typical in its manual, is in §E9.
     - §C4d cites the 30 W back to §C4 ("1.75 kg, 20–30 W and fibre-laser cost (§C4)"), so the reference is circular.
     - §C3c says "One lidar is rated 6–20 W" (citing §E9), so the report's own sourced range has no 30 W unit.
   - **Proposed rewrite:** "Seyond's Falcon K2 is specified at 20 W [P, datasheet; §C3], against about 6–10 W for 9xx-nm units (Seyond Robin E1X 6 W [P], §C3; Hesai ATX 8 W, 10 W typical in its manual [P], §E9)."
     - Keep the Falcon K1's 30 W only with a source and tag.
     - Otherwise drop it, and change §C4d's "20–30 W" to "20 W (K2 datasheet [P])".

2. **Line** ≈3287, §C4 item 2 "Detectors" — **E** — **medium**
   - **Quote:** "Front-side SPADs reached only 2–5% PDE."
   - **Problem:**
     - There is no tag, source, wavelength or year, and nothing elsewhere in the report supports the figure.
     - The nearest figures read as if they conflict with it. §C4b gives "Historically about 5–10% (front-side)" for SiPMs, tagged [U]. §C0 subsection 10.8 fits published research sensors with "PDEs of 5–22%".
   - **Proposed rewrite:** "Front-side-illuminated SPADs (light entering through the wiring side) reached only about 2–5% PDE at 905/940 nm [U]."
     - Add a source if one exists.
     - If none does, write "single-digit PDE [U]" and reconcile it with §C4b's 5–10% for front-side SiPMs.

3. **Line** ≈3649, §C4c Sources line — **E** — **medium** (missing citations)
   - **Quote:** "Sources: https://webstore.iec.ch/en/publication/3587 ;"
   - **Problem:** Checking each paper the block cites against this line:
     - **Telesca et al., ISSW 2024:** probably present, as the unlabelled ISSW 2024 paper R02.1.
     - **Vines et al.:** probably the unlabelled `s41467-019-08830-w`. The block gives no venue or year, so the match cannot be confirmed from the text.
     - **Liu et al., *Micromachines* 2025:** probably the unlabelled `PMC12113715`.
     - **Rogers et al., *Nature* 2021:** there is no Nature link in this line; it appears only in Appendix 2. The unlabelled `arXiv 2008.02411` may be its preprint.
     - **GlobalFoundries, OFC 2025:** missing. The only OFC link is `OFC-2014-Th5C.1`, the 2014 demonstration.
     - **Wojtanowski 2014:** missing, deliberately ("original not read"). The survey that relays it is presumably the unlabelled `arXiv 2112.08936`.
     - **Also missing:**
       - Chen et al., *JAP* 2016 (no link anywhere in the report);
       - Hale & Querry and Kou (only Segelstein's data file is listed);
       - Artilux's Ge-on-Si SPAD;
       - Fudan / Zhangjiang Lab / Innolight (cannot be identified; `arXiv 2605.07343` is unlabelled);
       - the Hamamatsu G8931-20 price [T];
       - SiLC's "germanium detectors" [T].
     - The Sony IEDM 2025 Ge SPAD is covered by the "§C5a" pointer, since §C5a's Sources line carries IEDM 2025 DOIs.
   - **Proposed fix:** Add links for the GlobalFoundries OFC 2025 paper, Chen et al. *JAP* 2016, Hale & Querry, Kou, Artilux, the Fudan/Innolight paper and Rogers et al. (Nature). Tag any that cannot be linked as [U].

4. **Line** ≈3649, §C4c Sources line — **E** — **low** (unlabelled URLs)
   - **Quote:** "https://arxiv.org/pdf/2008.02411 ;"
   - **Problem:** The line is 33 bare URLs, so a reader cannot match a citation in the text to a link. §C0's Sources lines already label two of these same URLs: `s44275-025-00030-7` is "(Wang et al., SUSTech and RoboSense, Moore and More 2025)" and the jsaprev link is "(Sony automotive SPAD)".
   - **Proposed rewrite:** Use the §C0 format, "URL (Author, venue year)". For example:
     - "…/R02.1.pdf (Telesca et al., ISSW 2024)";
     - "…/s41467-019-08830-w (Vines et al., confirm)";
     - "…/PMC12113715/ (Liu et al., Micromachines 2025)";
     - "https://doi.org/10.1007/s44275-025-00030-7 (Wang et al., SUSTech and RoboSense, Moore and More 2025)";
     - "…/2023_230402/_pdf (Sony automotive SPAD)";
     - "https://arxiv.org/pdf/2112.08936 (survey relaying Wojtanowski et al. 2014)".

5. **Line** ≈3309, end of §C4 and §C4b — **E** — **medium**
   - **Quote:** "KrASIA, summarising Seyond's prospectus: the InGaAs route costs **2–3×** as much as 905 nm [T]."
   - **Problem:**
     - Neither §C4 nor §C4b ends with a Sources line.
     - That leaves these claims with no links: the KrASIA summary of Seyond's prospectus, the Yole view, the RoboSense M3 "50–70% cheaper" pitch [P], the NE Times ≈200-line cost crossover, and the power figures.
     - §G3 cites the 2–3× back to §C4 ("KrASIA's summary of Seyond's prospectus, §C4"). Every KrASIA link in the report is about another topic, so this claim has no URL anywhere.
   - **Proposed fix:** Add Sources lines at the end of §C4 and §C4b with the KrASIA article and/or Seyond's prospectus, the Yole release, the RoboSense M3 announcement, the NE Times teardown and the Seyond and Hesai datasheets. Alternatively, point each claim to the section that already carries its source, e.g. "(Falcon K2 datasheet, §C3)".

6. **Line** ≈3549, §C4c subsection 3, "Luminar's semiconductor unit" bullet — **D** — **low**
   - **Quote:** "was sold for **\$110 M** in Feb 2026, separately from its **\$33 M** lidar business [P, 10-K]."
   - **Problem:**
     - The facts match §C3a: \$110.0 M to Quantum Computing Inc. on 2 Feb 2026, and the lidar business for \$33.0 M plus \$0.2 M cure costs to MicroVision on 3 Feb 2026 [P]. The unit's contents also match §C3a's "Black Forest Engineering receivers and readout ICs … and an InP laser/photodiode unit".
     - But neither buyer is named, and "its \$33 M lidar business" reads as a valuation rather than a sale.
   - **Proposed rewrite:** "**Luminar's semiconductor unit** (InGaAs design, ROIC, lasers) was sold to Quantum Computing Inc. for **\$110 M** on 2 Feb 2026, and its lidar business separately to MicroVision for **\$33 M** (plus \$0.2 M cure costs) on 3 Feb 2026 [P, 10-K; §C3a]."

## Consistency flags (new)

- **Falcon naming:**
  - "Falcon K" is used in §C3 ("Falcon K/K2/K3 (1550)"), §C3b ("| **Seyond Falcon K / K2** (1,550 nm ToF)") and §C4 item 3.
  - "Falcon K1" is used in §C0 subsection 7 ("Seyond's Falcon K1 uses") and three times in §C4d: "Seyond Falcon K1: its manual gives", "heavier (Falcon K1 1.75 kg [P])" and "(Falcon K1 250 m, K3 450 m)".
  - Pick one name.
- **§C4d subsection 4, polygon-plus-galvo row:** "1.75 kg, 20–30 W and fibre-laser cost (§C4)" relies on §C4's unsourced 30 W.
- **§C3c table:** "One lidar is rated 6–20 W" (citing §E9) excludes the §C4 figure of 30 W.
- **§G3:** "(KrASIA's summary of Seyond's prospectus, §C4)" points back to §C4, which has no link.
- **§G2 "Cheap exits":** "its market value briefly exceeded roughly \$10 B in late 2020 [U]" conflicts with §C3a's computed "≈\$13.5 B at the peak close of \$41.80 (8 Dec 2020)". Use the §C3a figure.
- **§B3 note 1:** "about 17× the eye-safe photon flux of 905 nm (derived in §C4 …)" is a third place that depends on §C4's 17.1, while §C4c gives 16.4 (earlier finding 9). Carry whichever wording is chosen into §B3 as well.