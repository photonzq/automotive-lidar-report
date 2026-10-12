# Analog Photonics cross-check: §C3a profile against §C10 and §C10.2b

**What was checked.** The report, located by heading and quote; line numbers may be off by a line. The §C3a profile (table row at line 2623, profile at lines 2627–2654) was compared with:
- §C10: summary, §C10.2 item 3, §C10.2b and the §C10.7 verdict.
- Other places that mention the company: §C0 subsection 10.8, §C3c, §C7, §C7a, §C7b, §C10.3a, §D8 and Appendix 2.

## 1. Overall assessment

The core facts agree everywhere:
- Founded about 2012 by Michael Watts, with the company's own timeline starting at a 2016 DARPA MOABB award.
- Two unnamed Tier 1 joint development agreements, in 2018 and 2020.
- The 8,192-element, 1 µm-pitch array reached 35 m at 10%.
- The FS-4S datasheet claims are the same in eight places: 200 m at 10% only in a 20° × 10° ROI at 90 kpts/s, 80 m over 60° × 14° at 400 kpts/s, 35 W, 2025.

Three problems remain:
- **Funding is given three ways:** "not disclosed" in §C10.2b, "≈\$45 M of federal contracts and grants" in the §C3a table, and ≈\$79 M including subawards in the §C3a profile.
- **Datasheet claims are stated inconsistently:** the FS-4S beam convention, FSOC-B1 random access against the RAY-H1 retune time, and the FSOC-B1 datasheet has no source link.
- **§C10.7's verdict sentences contradict the report's own labelling** of Voyant Carbon as an OPA-plus-mirror hybrid.

## 2. New findings

1. **Line** 6848 (§C10.7; also 6845, 6847) — **B** — **medium**
   - **Quote:** "Analog Photonics is the one serious OPA-lidar developer still publishing datasheets, and its automotive milestones have not materialized on the stated timeline."
   - **Problem:** §C8 (line 5512, "hybrid (OPA + slow mirror, e.g. Voyant Carbon)") and §C10.2 item 2 (line 5848, "the Voyant Carbon type of hybrid") call Carbon an OPA hybrid. Carbon ships at \$1,490 with a public spec sheet (line 1310). Yet §C10.7 files Voyant under "switched FPAs" (line 6845) and says "The only OPA product that shipped was Quanergy's S3-2" (line 6847). Either Carbon's on-chip axis is not an OPA, in which case §C8 and §C10.2 are wrong, or these §C10.7 sentences need a "fully solid-state" qualifier.
   - **Proposed rewrite:**
     - Line 6847: "- The only fully solid-state OPA product that shipped was Quanergy's S3-2, at 5–20 m, and Quanergy went bankrupt; Voyant's Carbon, which pairs one on-chip steered axis with a slow mirror, ships for industrial use (§B8)."
     - Line 6848: "- Analog Photonics is the one serious developer of two-axis non-mechanical OPA lidar still publishing datasheets, …"
     - Line 6845: "Voyant: one on-chip axis plus a mirror (Carbon) and a switched FPA (Helium); Pointcloud: a switched FPA;"
     - If Carbon's axis is not an OPA, change §C8 and §C10.2 item 2 instead.

2. **Line** 2623 (§C3a table; also 2637) — **B** — **medium**
   - **Quote:** "≈\$45 M of US federal contracts and grants, mostly DARPA and ONR; SBIR only ≈\$4.3 M [I]"
   - **Problem:** The profile right below gives \$45.2 M of prime obligations plus \$34.2 M of subawards, ≈\$79 M in total (line 2643). The table counts only the prime money but does not say so. Line 2637 ("it lives on large DARPA and ONR contracts") also leaves out the subawards, although AIM Photonics alone (\$19.9 M) exceeds all the listed ONR prime money. §C7 (line 4476) correctly says "federal prime awards". §C10.2b still says "amounts are not disclosed" (earlier finding 10, line 5963).
   - **Proposed rewrite:**
     - Table: "≈\$45 M of federal prime contracts and grants (≈\$79 M with \$34.2 M of subawards, mainly from AIM Photonics), mostly DARPA and ONR; SBIR only ≈\$4.3 M [I]".
     - Line 2637: "…it lives on large DARPA and ONR prime contracts and on subawards, mainly from AIM Photonics."
     - §C10.2b: "Funding is mostly US government money: \$45.2 M of federal prime obligations and \$34.2 M of subawards, ≈\$79 M over 2013–2026 (§C3a) [I]; no venture round was found."

3. **Line** 2472 (§C0 subsection 10.8; also 5778, 5995, 6091) — **B** — **medium**
   - **Quote:** "with a beam of at most 0.04° × 0.02° FWHM."
   - **Problem:** §C0 states that the FS-4S beam widths are FWHM. The §C10 summary, §C10.2b and the §C10.3 footprint table all say "if the datasheet widths are FWHM". The same datasheet claim is given as fact in one place and as an assumption in three others, and the ≈8% 1/e² footprint fraction depends on which is true.
   - **Proposed rewrite:** Check the datasheet.
     - If it states FWHM: write "Beam ≤0.04° × 0.02° FWHM" in §C10.2b and replace the three conditionals with firm values (2.8% as a FWHM ellipse, ≈8% at 1/e²).
     - If it does not: change §C0 to "with a beam of at most 0.04° × 0.02° (width convention not stated)".

4. **Line** 5974 (§C10.2b products table) — **A/B** — **low–medium**
   - **Quote:** "50° × 14°, 1 mrad beam, ≤7.5 dB fibre-to-beam loss at up to 400 mW in, <10 µs random access, <5 W"
   - **Problem:** The row calls FSOC-B1 "The same engine" as the lidar. In the FS-4S the second axis (14° there too) is wavelength-steered, and the RAY-H1 row says that axis "can be re-addressed only about every 300 µs". Random access in under 10 µs across 50° × 14° would need a laser retune 30× faster. The row does not say whether the 10 µs covers both axes.
   - **Proposed rewrite:** "…<10 µs random access (the datasheet does not say whether this covers the 14° axis or which laser it assumes) [U], <5 W". In the "What it shows" cell: "The same OPA engine sold for free-space optical links; if its 14° axis is wavelength-steered, <10 µs access needs a laser much faster than RAY-H1's <300 µs retune".

5. **Line** 5972 (§C10.2b, SR-1S row; also 5971) — **A/B** — **low–medium**
   - **Quote:** "The 70° wavelength-steered axis would need ≈1.17°/nm over RAY-H1's 60 nm"
   - **Problem:** The table never says which laser either module uses. The FS-4S is listed as "C+L band" (≈95 nm). Its 14° vertical field fits that band at the papers' 0.14°/nm, but would need 0.23°/nm with RAY-H1's 60 nm. The SR-1S check assumes 60 nm only.
   - **Proposed rewrite:** Add a derivation bullet: "FS-4S: 14° over the ≈95 nm C+L band is $14/95=0.147^\circ$/nm, consistent with the 8,192-element array's 0.14°/nm; over RAY-H1's 60 nm it would need $0.23^\circ$/nm, i.e. $(n_g-\sin\theta)/\cos\theta\approx6.3$, 1.5× a Si strip. SR-1S: 70° needs $1.17^\circ$/nm over 60 nm (factor ≈32) or $0.74^\circ$/nm over 95 nm (factor ≈20, 4.7× a Si strip); either is far beyond the papers." Also state which laser each datasheet names.

6. **Line** 5927 (§C10.2b device table) — **B** — **low–medium**
   - **Quote:** "| Analog Photonics, 9,216 (VLSI 2023) [I/S] | 9,216 | About 50° × 11° | 0.05° |"
   - **Problem:** A 50° alias-free field allows a pitch of at most $1.55/(2\sin25^\circ)=1.83$ µm. 9,216 elements at that pitch make a ≈17 mm aperture with a FWHM of $0.886\lambda/D\approx0.005^\circ$, ten times finer than the 0.05° listed. The row gives no pitch and no axis for the 0.05°. The 512-element row handles the same ambiguity with a note and [U].
   - **Proposed rewrite:** "| Analog Photonics, 9,216 (VLSI 2023) [I/S] | 9,216; pitch not reported | About 50° × 11° | 0.05° (axis not stated; a 9,216-element phase axis at the ≤1.8 µm pitch a 50° field allows would give ≈0.005°) [U] |".

7. **Line** 2646 (§C3a profile) — **A/B** — **low–medium**
   - **Quote:** "Its public milestones stop in 2021 [P]. The FS-4S datasheet (2025) is analysed in §C10.2b."
   - **Problem:** §C10.2b reports a 2023 company-authored IEEE Spectrum article promising automotive samples in 2025, plus 2025 datasheets and a 2025 CEO talk. "Public milestones stop in 2021" reads as contradicting this. The intended meaning is the company's achieved-milestone timeline.
   - **Proposed rewrite:** "Its published milestone timeline stops in 2021 [P]; a 2023 company-authored IEEE Spectrum article promised automotive samples in 2025, and none were found (§C10.2b). The FS-4S datasheet (2025) is analysed in §C10.2b."

8. **Line** 9672 (Appendix 2, under the heading "Analog Photonics datasheets and the Quanergy record") — **E** — **low–medium**
   - **Quote:** "Analog Photonics FS-4S / SR-1S / RAY-H1 / FSOC-B1 datasheets (2025):"
   - **Problem:** Four datasheets are named but only three URLs follow; there is no FSOC-B1 link. Its figures (≤7.5 dB loss, <10 µs access) cannot be traced. The §C10.2b tag "Rev A, June–July 2025" is also unverified for FSOC-B1.
   - **Proposed rewrite:** Add the FSOC-B1 URL with its revision and date. Otherwise drop "FSOC-B1" from this entry and tag the §C10.2b row [U].

9. **Line** 5961 (§C10.2b, "Who they are") — **B/E** — **low**
   - **Quote:** "Third-party databases give 2012 as the founding year; the company's own timeline begins with a 2016 award under DARPA's MOABB"
   - **Problem:**
     - §C3a shows federal money earlier than this: subawards from Nov 2013 and SBIR awards from 2015.
     - The founder is tagged [I] here but [P/S] in §C3a (line 2631).
     - The milestones in this paragraph carry no tag.
     - The paragraph omits the facts §C3a holds: funding, 26 employees, and the departure of Christopher Poulton, lead author of the 512- and 8,192-element papers this subsection relies on.
   - **Proposed rewrite:** "**Who they are.** Analog Photonics (Boston) was founded about 2012 by Michael Watts of MIT, who remains CEO [P/S]. Federal records show subawards from Nov 2013 and SBIR awards from 2015; the company's own timeline starts with its 2016 DARPA MOABB award (§C3a). Company milestones [P]: a Tier 1 joint development agreement (2018), on-car tests (2019), a second Tier 1 agreement (2020) and a narrow-linewidth FMCW laser (2021). Funding, size and the departure of the lead author of its OPA papers are covered in §C3a."

10. **Line** 2635 (§C3a; also §D8, lines 7574–7575) — **B/E** — **low**
    - **Quote:** "**\$3.97 M**, 2023–26 [I];"
    - **Problem:**
      - §D8 gives this ONR contract as "\$4.0 M over FY2023–25, is the only active integrated-photonics lidar contract found [P]". The years differ, and so does the tag ([I] vs [P]) for the same USAspending record.
      - Similarly, §C3a's MOABB award ("2016–2023") outlasts §D8's MOABB budget ("\$102 M over FY2016–21 and nothing from FY2022 [P]").
      - The reader is not told that one set of dates is the period of performance and the other is the fiscal years of obligation.
    - **Proposed rewrite:** In §C3a, "**\$3.97 M** obligated in FY2023–25, period of performance 2023–26 [I];" and "…**\$26.6 M**, period of performance 2016–2023 (MOABB's budget lines end in FY2021, §D8)". In §D8, "\$4.0 M obligated over FY2023–25 (performance to 2026, §C3a)". Use one tag for USAspending records throughout.

11. **Line** 2623 (§C3a table, status cell) — **D** — **low**
    - **Quote:** "No automotive programme; two unnamed Tier 1 JDAs (2018, 2020) [P]; defence FSOC and lasers (below; §C10.2b)"
    - **Problem:** "No automotive programme" reads as contradicting the Tier 1 joint development agreements in the same cell and the "on-car tests (2019)" in §C10.2b. What is missing is a production award.
    - **Proposed rewrite:** "No automotive production award found; two unnamed Tier 1 JDAs (2018, 2020) and on-car tests (2019) claimed [P]; defence FSOC and lasers (below; §C10.2b)".

12. **Line** 5942 (§C10.2b finding 1; also 5928) — **B** — **low**
    - **Quote:** "Multi-reticle stitching has been demonstrated (49,152 elements)."
    - **Problem:** The table row says ">49,152 over four reticles", tags the source as an abstract and reports no ranging. Finding 1 gives exactly 49,152 and calls it "demonstrated". 24 OPAs of 2,048 elements each would be exactly 49,152.
    - **Proposed rewrite:** "Multi-reticle stitching of 49,152 elements (24 coherently combined OPAs over four reticles) has been reported in a conference abstract [I], without ranging." Use the same count in the table.

## 3. Earlier findings: status in the current text

**Resolved**
- **#1, coherent-power headline** (now line 6009). Minor residual: line 6016 still says $N_{\rm req}=10$–30 "are roughly those for a non-fading return".
- **#2, "camera-like" definition** (Q4, now line 5759).
- **#4, ToF inputs** (now lines 6020 and 6039). New residual: the caveat at line 6067, "Sunlight raises the ToF $N_{\rm req}$ (§C6(d)).", now contradicts line 6020. Suggested replacement: "Sunlight is already included in the ToF $N_{\rm req}$ (bright sun, §C0 subsection 10.3); a fully sunlit scene of reflectance 0.9 raises the ideal requirement only to ≈20 (§C6(d))."
- **#5, diversity assumption** (now line 5895). Line 5891 still groups polarization, wavelength and spatial diversity together, but line 5895 now explains the difference.
- **#6, ToF usable aperture** (now line 5777).
- **#32, in part:** "26.5" has been corrected to 26.4. "about 25 cells" (line 5859) and "about 9 dB higher" (line 5945) remain.

**Still open (quote text unchanged)**
- #3 ($\eta$ convention, line 6015), #7–#31 and #33–#40.
- This includes #10 (§C10.2b "amounts are not disclosed", line 5963), which new finding 2 extends.

## 4. Consistency flags confirmed in this check

- §C7 (line 4476), "1.5 µm pitch, about 60°", against the 512-element device in §C10.2b (1.65 µm, 56°). Still unsourced. If 1.5 µm is inferred from the FS-4S's 60° field, mark it so, e.g. "a 60° phase-steered field implies a pitch of about 1.5 µm [E]".
- Line 5972, "14–17° in AP's papers", against the table's 15° and 17°. "AP" is still undefined.
- Optional: the headline at line 6009 could add the multi-mode case from caveat 4, "≈45 W with four receive modes".