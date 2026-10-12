# Scripts archive

Working scripts behind the edits and numbers in `automotive_perception_report_2026-09-27.md`.

- Paths that pointed to temporary working folders are now relative to this folder. Scripts that read or write the live report still use its absolute path.
- Report snapshots and downloaded data are not kept here.
- The build scripts and the installed figure models live in `../build/`.
- Section and equation numbers in this index are those of the report when each script ran. §C0 was restructured on 12 Oct 2026; the table in the section on `c0_restructure_2026-10/` maps its old subsections to the new ones.

Status:
- **current**: still the source of numbers in the report.
- **historical**: one-off, already applied or used.
- **superseded**: an intermediate copy replaced by a later version.

## Self-consistent re-baseline of the FMCW vs SPAD-ToF comparison (§C0, §C7a, §C7b), `rebase/`

| File | Purpose | Status |
|---|---|---|
| `rebase/apply_rebase.py` | Applies `edits.py` and `s103_new.md` (133 anchored edits plus the new §C0 10.3 with one new equation) to the live report. The write is hash-guarded. Snapshot equation numbers are mapped to the live file by matching equation bodies, then all equations are renumbered. | historical |
| `rebase/edits.py` | Edit pairs for the re-baseline: line, exact-line, substring and block replacements written against the 12:04 snapshot. | historical |
| `rebase/s103_new.md` | New text of §C0 10.3 (detection statistics). | historical |
| `rebase/apply_fix2.py` | Follow-up write: the `P_{FA,{\rm pt}}` notation fix, evidence-tag style, and the measured-efficiency caveat in §C7a and §C7b. | historical |
| `rebase/apply_dt.py` | Applies `edits_dt.py` (SPAD detection efficiency and 6 ns dead time, 67 edits). It uses the same machinery as `apply_rebase.py`, whose docstring it inherits. | historical |
| `rebase/edits_dt.py` | Edit pairs for the detection-efficiency and dead-time pass. | historical |
| `rebase/apply_par.py` | Applies `edits_par.py` (paralyzable dead-time model plus the new §C7b 2(i) eye-safety part, 106 edits). Same machinery as `apply_rebase.py`. | historical |
| `rebase/edits_par.py` | Edit pairs for the paralyzable-model and eye-safety pass. | historical |
| `rebase/check_refs.py` | Read-only check: equation tags are sequential, no reference dangles, and key anchors are present. | current |
| `rebase/patch_lbs.py` | Patches `build/figures/link_budget_scaling.py` with the per-point detection rule, the two-ramp FMCW statistics (Figure C0.10b) and the four-look reading of the FMCW case. | historical (installed) |
| `rebase/power_c7b.py` | §C7b 2(h) with $N_L$ receivers per channel, plus assorted re-baseline numbers. | historical |
| `rebase/stats103.py` | Detection statistics for §C0 10.3, with the per-point rule for both receivers. | historical |
| `rebase/sym_split.py` | Two-stage FMCW detection with a symmetric per-bin false-alarm split $p_1=p_2$. | historical |
| `rebase/NEXT_STEPS.md` | Working note on the order of the re-baseline writes around a parallel editing pass. | historical |
| `rebase/lbs/link_budget_scaling.py` | Test copy of the patched link-budget figure script. | superseded |
| `rebase/lbs/link_budget_scaling_peer1156.py` | The 11:56 copy from the parallel editing pass, used to test `patch_lbs.py`. | superseded |

## SPAD dead time and the 1,550 nm eye-safety allowance (§C7b 2(i)), `deadtime/`

| File | Purpose | Status |
|---|---|---|
| `deadtime/tof_paralyzable.py` | ToF numbers with the paralyzable dead-time model: live fraction $e^{-r\tau}$, where $r$ is the count rate and $\tau$ the dead time. | current |
| `deadtime/eyesafety.py` | Eye-safety headroom at 1,550 nm against the model's needs, and the gated-transmitter channel power (§C7b 2(i)). | current |
| `deadtime/lbs/base.py`, `deadtime/lbs2/base.py` | Copies of the link-budget figure script before each patch. | superseded |
| `deadtime/lbs/link_budget_scaling.py`, `deadtime/lbs2/link_budget_scaling.py` | The same script after each patch; the installed version is in `../build/figures/`. | superseded |

## FMCW detection statistics and the FMCW/ToF system power model, `fmcw/`

| File | Purpose | Status |
|---|---|---|
| `fmcw/apply_fmcw.py` | Hash-guarded write of the FMCW block of §C7b subsection 2, from item (d) to the summary, taken from `c7b_block.md`. | historical |
| `fmcw/c7b_block.md` | Text of that block. | historical |
| `fmcw/detect_stats.py` | Photoelectrons needed for detection: SPAD ToF (Poisson) against coherent FMCW (FFT bin), including the up/down ramp split and the number of bins searched. | historical |
| `fmcw/options200.py` | Two-ramp FMCW detection: photoelectrons for $P_D=0.9$ at 200 and 300 m against ramp time and number of looks, with the per-stage false-alarm split optimized. | historical |
| `fmcw/pairsum.py` | Statistic summed over $L$ looks × 2 ramps of $\lvert s+n\rvert^2$, with fading common to both ramps within a look. | historical |
| `fmcw/bg_algo.py` | Background counts per 1 ns bin per point against scene reflectance. | historical |
| `fmcw/l8.py` | Sensor power at 15 Mpts/s and 200 m with $L$ receivers per channel. | historical |
| `fmcw/model/patch_model.py` | Builds the patched system-budget model (four looks, harmonized background, paralyzable dead time) from `fmcw_tof_system_budget_orig.py`. | historical (installed in `../build/figures/`) |
| `fmcw/model/fmcw_tof_system_budget_orig.py` | The system-budget model before patching. | superseded |
| `fmcw/model/fmcw_tof_system_budget.py` | Copy of the patched model. | superseded |
| `fmcw/model/lab/try_labels.py` | Trial placements of the product labels (ATX, ETX) on the model's figure. | superseded |
| `fmcw/model/lab/`, `run/`, `run2/`, `run3/` `fmcw_tof_system_budget.py` | Intermediate runs of the model. | superseded |

## Public-funding section (§C3a), `funding/`

| File | Purpose | Status |
|---|---|---|
| `funding/apply_funding.py` | Hash-guarded write of the public-funding block (§C3a) and the §C5 Fastree3D timeline. | historical |
| `funding/fix_block.py` | Text fixes to `public_money_c3a.md` before it was applied, such as the consortium-share list. | historical |
| `funding/public_money_c3a.md` | Text of §C3a. | historical |

## Data-gathering helpers for the landscape and funding research

| File | Purpose | Status |
|---|---|---|
| `search/fetchq.py` | Paged downloader for the CORDIS search API; JSON pages are cached. | historical |
| `search/runall.py` | Runs the CORDIS queries (lidar, FMCW, OPA, SPAD, ranging, microcomb, ...) through `fetchq.py`. | historical |
| `search/classify.py` | Normalizes CORDIS hits (calls, programmes, funding scheme, organizations) and classifies the scheme. | historical |
| `search/relevance.py` | Tags the normalized hits by keyword: lidar, FMCW, OPA, ToF, SPAD, ranging, 3-D, beam steering, comb, automotive. | historical |
| `names/names.py` | CORDIS project search by organization or person name, using `classify.py`. | historical |
| `summ.py` | Prints a CORDIS project summary for given project IDs (dates, cost, EU contribution, keywords, organizations), downloading the JSON if missing. | historical |
| `summ2.py` | Prints the calls, topics and funding scheme of given CORDIS project IDs. | historical |
| `agent3/summ.py` | The same summary for a helper agent's cached CORDIS files. | historical |
| `xv/parse.py` | Prints project details from saved CORDIS search-result files. | historical |
| `lidarfund/extract.py` | Extracts the main post text and dates from saved news pages. | historical |
| `lidarfund/extract2.py` | Variant for pages with an `<article>` element; also lists image alt texts. | historical |

## Thermal-camera export controls (note of 2026-10-02), `export_controls/`

| File | Purpose | Status |
|---|---|---|
| `export_controls/fetch_thermal_export_rules.py` | Downloads the EAR parts as of a fixed date (eCFR) and China's MOFCOM drone-payload notices. It extracts ECCNs 6A002, 6A003 and 6A993, §§734.4, 740.20, 742.6, 743.3, 744.9, 744.21 and 746.8, Country Groups A:1, A:5 and A:6, and the NS2/RS1/RS2 country-chart columns. | current |
| `export_controls/apply_a3_export_fix.py` | Hash-guarded replacement of the thermal export-control bullet in §A3 item 6 (car exit Note 3.c, ECCN 6A993.a), applied 2026-10-03. | historical |
| `export_controls/apply_d7_controls.py` | Hash-guarded edit of §D7 "Policy and controls": the China catalogue's any-one-of reading and pulse-width caveat, the exact 6A008.j.2 wording, and a bullet on laser-emitter controls (6A005/6A995 margins, the 1,555/1,570 nm edges, the tunable grey zone), applied 2026-10-03. | historical |
| `export_controls/apply_d2_row.py` | Hash-guarded edit of the §D2 timeline row for the Dec 2023 technology catalogue (any one of six thresholds; pulse-width caveat), applied 2026-10-03. | historical |
| `export_controls/laser_lidar_rules.py` | Laser and lidar controls (note of 2026-10-03). It extracts ECCNs 6A005, 6A995, 6A008 and 6A998, the Part 772 laser definitions, and the 6A995 line of Supp. 2 to Part 744. It checks the Wassenaar 2025 1,555/1,570 nm lines and the 6.A.5.c.3 Note, then prints the average-power margins of typical lidar emitters against the nearest 6A005 threshold. | current |

## Readability review of the scientific sections (2026-10-03), `readability_2026-10-03/`

| File | Purpose | Status |
|---|---|---|
| `readability_2026-10-03/reports/*.md` | The eleven block reports: at most 40 findings each, with exact quotes and proposed rewrites, for §A3–§A6 and §E2–§E5, §C0 subsections 1–9 and 10, §C4–§C4c, §C4d with §C8–§C9, §C5–§C6, §C7–§C7a with §F6, §C7b, both halves of §C10, and §E9–§E12. | current (most findings open) |
| `readability_2026-10-03/collect_reviews.py` | Copied each review agent's final report into `reports/`; archived as a stub, since the working logs it read are not included. | historical |
| `readability_2026-10-03/apply_readability_high.py` | Hash-guarded batch of 59 exact-substring edits fixing the clear-cut high-severity findings, applied 2026-10-03 (report sha256 after: 9c6d35ce…). | historical |
| `readability_2026-10-03/build_review_file.py` | Builds `../automotive_perception_report_readability_review_2026-10-03.md`: the applied edits, the open cross-section problems, the eleven block reports and the five follow-ups. | current |
| `readability_2026-10-03/reports/*_followup.md` | Follow-up cross-checks by five reviewers (§C0 parts 1–9 and 10, §C4–§C4c, both halves of §C10), run against the report after both edit batches; new findings only. | current (open) |
| `readability_2026-10-03/collect_followups.py` | Copied each reviewer's follow-up report into `reports/<label>_followup.md`; archived as a stub, since the working logs it read are not included. | historical |
| `readability_2026-10-03/fix_spec.md`, `round2_spec.md` | The rules for the edit agents: Round 1 (edit-list format, report-wide symbol scheme) and Round 2 (the author's model decisions of 2026-10-05, every old → new number, the sections per agent). | historical |
| `readability_2026-10-03/edits/*.json`, `edits/round2/*.json`, `edits/round3/*.json` | The applied edit lists of Rounds 1–3: exact `old`/`new` pairs, each with its finding and reason, plus the items each agent skipped. `*.json.bak` hold a list before my amendments. `edits/round3/round3_renumber_map.txt` maps every old equation number to the new one. | historical (applied 2026-10-05; report sha256 after Round 3: 51d60fa2…) |
| `readability_2026-10-03/validate_edits.py` | Checks edit lists against the live report without writing: each `old` occurs once, no overlaps, `$` parity, versioning words, texmath-safe `\rm`. | current |
| `readability_2026-10-03/merge_apply.py` | Merges edit lists and applies them as one hash-guarded batch, with the same checks plus protected spans (§D8, Appendix 1), the tag count and glued bold headings; `--dry --out=<copy>` writes the merged text to a scratch copy instead. | current |
| `readability_2026-10-03/show_edit_diffs.py`, `show_edit_raw.py` | Word-level diff of every edit for a read-through; raw `old`/`new` text of chosen edits. | current |
| `readability_2026-10-03/amend_round1_lists.py`, `amend_round2_lists.py` | The amendments made to agents' edits after the read-through, each with its reason; idempotent. | historical |
| `readability_2026-10-03/build_cross_section_edits.py` | Builds `edits/12_cross_section.json`, the cross-section items of Round 1. | historical |
| `readability_2026-10-03/collect_skipped.py`, `round1_skipped_items.md` | Collects the items the Round 1 agents skipped, grouped by kind (model, structural, decision, source, cross-section). | current (the needs_decision items are open) |
| `readability_2026-10-03/split_needs_source.py` | Writes the needs_source items of each group to `sources/<group>_items.md` for the Round 4 research agents. | historical |
| `readability_2026-10-03/grep_context.py`, `find_literal.py` | Regex matches with context; literal strings with their full lines, for copying exact `old` text. | current |
| `readability_2026-10-03/check_poisson_claims.py`, `check_poisson_claims_round2.py` | Recompute the photon-counting numbers of §C0 subsections 10.3–10.5 (Round 1, then the 0.05° × 0.05° pixel of Round 2). | historical |
| `readability_2026-10-03/round2_tof_pixel_variants.py`, `round2_c10_3_power_table.py` | Round 2 numbers: the ToF model at 0.1° × 0.05° against 0.05° × 0.05°, and the §C10.3 power table on the report-wide conventions. | historical |
| `readability_2026-10-03/round2/scripts/` (with `INDEX.md`) | The Round 2 agents' scripts (R2A–R2F): the numbers each section quotes, the edit-list builders and their checks; `R2F_C9_fetch_sources.py` downloads the three §C9a sources (no identity sent). | historical |
| `readability_2026-10-03/grep_stale_numbers.py`, `check_skipped_coverage.py` | After a dry merge: every retired Round 2 number left in the text; whether each skipped cross-section item is covered by another list. | current |
| `readability_2026-10-03/post_merge_symbol_check.py` | Lists remaining uses of symbols that the report-wide scheme replaces (all zero after Round 1). | current |
| `readability_2026-10-03/round3_build_moves.py`, `round3_build_eqdups.py`, `round3_fix_pelec_labels.py` | Round 3: the six moves (§C0 subsection 9 → §C1a, the 10.7 survey → §C4b, §C7b 2(h)–(i) → 3a with the short-answer cut and the P_elec display, Fastree3D → §C3a, the AS-DT1 radar comparison → §E2, the identity Eq. (140) into §C10.3a) and the fourteen merged duplicate displays. | historical (applied) |
| `readability_2026-10-03/renumber_equations.py` | Renumbers `\tag{N}` in document order and remaps every equation reference; `--redirect OLD=KEPT` for merged tags, `--allow-reorder` after a move, `--file=<copy>` for dry runs. | current |
| `readability_2026-10-03/check_eq_sections.py`, `check_eq_directions.py` | After moves: references that name a section other than the equation's, and "Eq. (N) below/above" that point the wrong way (both zero after Round 3). | current |
| `readability_2026-10-03/render_eq_pages.py` | Renders the PDF pages holding given equation numbers, to check how displays typeset. | current |
| `readability_2026-10-03/sources/` | Round 4 source research: `research_spec.md` (the rules: primary sources, no e-mail address in any request, scripts archived), `<group>_items.md`, the agents' `<group>_findings.md`, and their scripts in `sources/scripts/` with `INDEX.md`. | historical (applied); `R8_C9a_inband_items.md` is open (its research pass ended before writing anything) |
| `readability_2026-10-03/round4_build_from_findings.py`, `round4_amendments.py` | Round 4: turn a research agent's `sources/<group>_findings.md` into `edits/round4/R4_<group>.json`, with my amendments after the read-through (`AMEND`, each with its reason) and the Appendix 2 group of items that name none (`APPX_GROUPS`). Refuses to overwrite an applied list without `--force`. | historical (applied) |
| `readability_2026-10-03/round4_r1_appendix.py`, `round4_r2_appendix.py`, `round4_r5_appendix.py` | Round 4: the Appendix 2 lines of the groups whose findings list sources without a group, placed by hand by the section they support. | historical (applied) |
| `readability_2026-10-03/round4_reconstruct_before.py`, `round4_check_list_reproduces.py` | Rebuild the report text before an applied list and check that the list reproduces the recorded hash (used once, after an applied list had been rebuilt by mistake). | historical |
| `readability_2026-10-03/edits/round4/*.json`, `edits/round5/*.json` | The applied lists of Round 4 (`R4_<group>` per research group, their Appendix 2 lists, and my own `R4x_mine` to `R4x_mine4`) and Round 5 (`R5a_panasonic`). | historical (applied 2026-10-05; report sha256 after Round 5: 4992caf4…) |
| `readability_2026-10-03/check_round2_survival.py` | Checks that every Round 2 edit survives in the current report (renumbered with the Round 3 map) and attributes each later change to the Round 3 or 4 edit that made it. | current |
| `readability_2026-10-03/round5_build_decisions.py` | Round 5b: the author's decisions on the open readability items (2026-10-05) as one edit per changed line, so that no edits overlap. Covers "programme" outside URLs, quotations and official names, "(§X subsection N)", the N_ADC/n_req/P_D/p/x_th/N_m/T_c/T_u/PRF_ch notation, Falcon K1, the Moore Photonics deletion and nine content fixes. Lines in Part B, §D8 and Appendix 1 go to `edits/round5/R5b_for_peer.json`, applied in a separate pass. | historical (applied; report sha256 after: 2a68627599c1) |
| `../build/figures/link_budget_scaling.py` (change of 2026-10-05) | The fixed extra-loss list uses the water film's exact 1.88 dB in place of 1.9 dB; tables rerun: 111 m (best aperture) and 61 m (25 mm), as §C0 10.6 now says. | current |
| `readability_2026-10-03/round5_panasonic_photons.py`, `round5_build_r2_leftovers.py` | Round 5: the photons per pixel per pulse of Panasonic's flash sensor (Hirose et al. 2018) from Eq. (55), for the two fields of view, and the edit list for that row of §C0 subsection 10.8. | historical (applied) |

## Gap-filling write and §D8 (2026-10-03), `gapfill_2026-10/`

| File | Purpose | Status |
|---|---|---|
| `gapfill_2026-10/apply_gapfill.py` | Applies `edits_gapfill.py` to the live report. The write is hash-guarded: snapshot equation numbers are mapped by equation body, every match must be unique, and the script runs hygiene checks (odd `$`, table pipe counts, versioning words). Applied 2026-10-03 (report sha256 after: 453a99a7…). | historical |
| `gapfill_2026-10/edits_gapfill.py` | The 78 anchored edits: corrections from the research round (Sony ISSCC 2021 facts, silicon absorption, Brosens, ISO 16750-3:2023, Falcon K1, ATX, robotics, delivery vans and robots, JV suppliers, exports, failed companies, EU and German grants, Analog Photonics subawards, Hesai Thailand), the new §D8 on EU and US public research funding, and the rewritten Appendix 1. | historical |
| `gapfill_2026-10/fix_caption_dollar.py` | Follow-up, hash-guarded: the §D8 table caption reads "(nominal US dollars)" (report sha256 after: ba47777d…). | historical |
| `gapfill_2026-10/edits_gapfill2.py` | Second batch, 54 edits, applied with `apply_gapfill.py --edits edits_gapfill2`: clean-up of escaped quotes left by the first batch; §C4d scanner rates (Falcon five-facet polygon and four beams, InnovizOne four lasers, M1 teardown, Cepton patent frequencies) and the Figure C4d caption; headlights (AAA 2019); export controls and NHTSA EA26002 status; Tesla fleet; §B8 vacuums, industrial lidar and ToF parts; Pointcloud, Fastree3D, Oryx, TetraVue, LeddarTech, Baraja and OURS facts; Hesai Thailand land; §D3 FY2026 NDAA §162 and two §D6 calendar rows; the §D8 non-SBIR US channels; Appendix 1 as a whole again (report sha256 after: a43e05d7…). | historical |
| `gapfill_2026-10/edits_gapfill3.py` | Third batch, 23 edits: §D8 EU numbers after the corrected CORDIS search rule, the EU defence paragraph (EDF and POINTER, EIC, Chips JU, ESA, Photonics21), and the §D8 items of Appendix 1 (report sha256 after: 551411dc…). | historical |
| `gapfill_2026-10/fix_blank_line.py` | Follow-up, hash-guarded: the blank line before "US: how the count was made" in §D8 (report sha256 after: fedff6f5…). | historical |
| `gapfill_2026-10/edits_b8_integration.py` | Builds 9 old→new pairs (2026-10-04) that work the two §B8 note bullets ("Verification of dToF", "Scope of the 80% estimate") into the robot-vacuum row, the terms list and the Camsense list, drop the trade-report consistency check now that the prospectus gives the figure, and align the Appendix 1 robot-vacuum item. Facts checked against the LDROBOT prospectus, application proof and interim results, the Camsense prospectus and IDC's 2025 cleaning-robot figures; page numbers are in the docstring. Writes the pairs as JSON plus a dry-run copy; it does not write the report. | current |
| `gapfill_2026-10/b8_integration_edits.json` | The 9 pairs, applied in a separate pass (each "old" unique in report sha256 fedff6f5…; applied alone they give 6ec93640…). | current |
| `gapfill_2026-10/b8_locate_terms.py`, `b8_locate_terms2.py`, `b8_render_pages.py` | Find the cited pages of the LDROBOT and Camsense filings by text search, then render them at 160 dpi for reading; also trace LDROBOT's 2024 dToF figure to its application proof. | historical |
| `gapfill_2026-10/edits_partB_definitive.py` with `partB_definitive_texts.py` | Builds 43 old→new pairs (5 Oct 2026) that turn Part B's reviewer-voice hedges ("not verified", "was found", "in this review", "Treat … as", "not checked") into definitive statements, fix three such phrases in §D3, and move what stays unknown into Appendix 1 (new "Parking and near-field sensing" group; Zoox, May/PlusAI, delivery vans and robots, Zeekr blind-spot items). Facts come from the three research folders below; the texts module names the sources per block. Writes the pairs as JSON plus a dry-run copy; it does not write the report. | current |
| `gapfill_2026-10/partB_definitive_edits.json` | The 43 pairs (each "old" unique in report sha256 4992caf4…). The separate pass that was to apply them closed first, and at the author's choice they were applied directly on 2026-10-05 with `apply_json_pairs.py` (report sha256 after: c0e80c3a…, identical to the tested dry-run copy). | historical |
| `gapfill_2026-10/apply_json_pairs.py` | Applies a JSON list of {"id", "old", "new"} pairs to the report: checks the expected hash, requires every "old" to occur once, saves a copy of the previous version, and re-hashes just before writing. | current |
| `gapfill_2026-10/partB_research/vehicles/`, `parking/`, `rules_japan/` | The research agents' scripts for those pairs: URL fetchers with a generic User-Agent, PDF grep/render (160 dpi), HTML-to-text, Autohome sensor-row extraction, eCFR XML to text, and a regulations.gov docket downloader that uses the public `DEMO_KEY` placeholder. Raw downloads were kept outside the report folder. | historical |
| `gapfill_2026-10/followups_texts.py` and `followups_edits.json` | The readability review's follow-ups for these sections, chosen by the author on 2026-10-05, as 10 pairs built with `edits_partB_definitive.py --texts followups_texts --name followups`. They repoint Appendix 1's Fastree3D pointer to §C3a subsection 2; give the §B8 VL53L5 macro-pixel wording; add an Appendix 1 entry for the Wood et al. [U] figures; name each §B1 figure's provider (ResearchInChina 1.529 M and 3.21 M; Gasgoo's 21 May 2026 article for 2.756 M main lidars and >985k in Q1 2026); and turn §B4a's duplicate stopping-distance display (Eq. (14)) into a pointer to Eq. (11). Applied 2026-10-05 after the readability review's 19 R5b edits for these sections ("programme", "(§X subsection N)"): 2a686275… → fbba4eea… → 4d1c63f3…. Then `../readability_2026-10-03/renumber_equations.py` (175 → 174 tags) gave 078a6dc6…, and one more "Programmes" heading fix gave 7d73cf79…. check_refs, check_eq_sections and check_eq_directions were clean. | historical |
| `../build/figures/mechanical_scanning_limits.py` (edited in place, not archived here) | Figure C4d data changed with the second batch: Falcon K1 as a five-facet, four-beam polygon (54,720°/s), InnovizOne with four lasers (640 sweeps/s), M1 one beam per module. The pre-edit copy was kept outside the report folder. | current (installed) |

## Research round on the Appendix 1 gaps (2026-10-03), `gaps_*/`

Each folder holds one research agent's scripts; raw downloads were kept outside the report folder. Every script has a docstring with its purpose and usage.

| Folder | Files | What they produced |
|---|---|---|
| `gaps_specs/` | `sony/digitize_isscc2021_pde.py`; `common/doi_meta.py`, `common/fetch_text.py`, `common/ieee_meta.py` (does not get past the IEEE Xplore bot check; kept as a record), `common/hkex_docs.py`, `common/pdf_keyword_pages.py`, `common/download_render.py`, `common/edgar_fts.py`, `common/openalex_search.py`; `fmcw_rx/soa_wpe_105c_estimate.py`; `INDEX.md` | Sony ISSCC 2021 PDE curves against temperature and wavelength (§C5a); DOI metadata for the closed-access Sony and Yonsei papers; Hesai, RoboSense and XMC prospectus searches (foundry evidence); the SOA wall-plug-efficiency estimate at 105 °C (Appendix 1) |
| `gaps_scanners_regulation/` | `astm_g173_lidar_bands.py`, `si_absorption_905_940.py`, `brosens_constant_check.py`, `nhtsa_investigation_docket.py`, `scanner_rate_arithmetic.py`; `INDEX.txt` | AM1.5G values at 905, 940 and 1,550 nm (match §C4c); silicon absorption at 905 and 940 nm (§C4); the cantilever-strip check of the Brosens constant (§C4d); the Falcon, M1 and InnovizOne sweep-rate arithmetic (§C4d); the EA26002 docket status |
| `gaps_funding/` | `ap_usaspending_awards.py`, `ap_subaward_detail.py`, `ap_subaward_table.py` (Analog Photonics prime awards and the 31 subaward records); `foekat_search.py`, `povos_totals.py` (German federal funding catalogue, POV.OS); `aeva_oem/`, `hesai_thailand/`, `eic_fund/` (helpers: SEC filings and call transcripts, HKEX filings, EIC Fund portfolio and Data Hub, Belgian accounts); `fastree3d_filing_grep.py`, `fastree3d_wayback_pages.py`, `aramis_search.py`, `snf_grep.py`, `eic_fund_portfolio_check.py`, `browser_extraction_snippets.js` (the page-console snippets used where sites block scripts) | §C3a subawards, grant rows and Pointcloud; §C5 Fastree3D deal and team; §D4 Thailand plant; Appendix 1 funding items |
| `gaps_companies/` | `item1_2_patent_assignment_scan.py` (patent assignments), `item4_fetch_pages.py`, `item4_baidu_search.py` (光勺 and 映讯芯光), `item5a_gpatents_*.py`, `item5b_fetch_uspto.py`, `item5b_ocr_pdf.py`, `item5b_winocr.ps1` (Strobe, OURS and Baraja patents), `uspto_assignment_search.py` | TetraVue, LeddarTech, Insight LiDAR, peak values, failed-company technology bets (§C3a) |
| `gaps_programs/` | `cars_*.py` (EDGAR and HKEX searches on Rivian, GM, Ford and RoboSense), `china_*.py` (JV suppliers), `robotaxi_*.py`, `trucks_*.py`, `exports_lidar_estimate.py` (the channel-by-channel export estimate of §B5), `exports_eu_rdw_model_counts.py` (Dutch registrations), `exports_eu_rdw_counts.py` (superseded first version), `exports_fetch_helper.py`, `takerate_sgo_mercedes.py` (NHTSA crash files for Mercedes), `robotaxi_zoox_federal_register.py`, `trucks_fmcsa_safer.py` (FMCSA carrier registrations) | §B2 note 6, §B5, §B6 notes, Appendix 1 supplier, take-rate and trucking items |
| `gaps_robotics/` | `hkex_fetch.py`, `robotics_lidar_asp.py` (robotics revenue per unit), `call_transcript_grep.py`, `vans_fetch_pages.py`, `delivx_sec_fetch.py` (reads its SEC User-Agent from the `SEC_UA` environment variable), `delivx_web_fetch.py`, `vacind_prospectus_extract.py` (LDROBOT, Camsense and Vanjee filings), `asdt1_sony_pages.py` (Sony AS-DT1 pages) | §B4a vans and delivery robots; §B8 robotics units, revenue, split by robot type, robot vacuums and industrial lidar |

## Western public research funding (§D8), `renew_eu/` and `renew_us/`

| File | Purpose | Status |
|---|---|---|
| `renew_eu/build_corpus.py` | Builds the project table (84,787 FP7, H2020 and Horizon Europe projects) from the CORDIS bulk JSON files. | current |
| `renew_eu/classify_trends.py` | Search, relevance score, hardware/use role, coherent and photonic-integrated flags, and the trend tables of §D8. The corrected version (word-bounded exclusions; ToF and depth terms count only with an active-ranging word) produced the §D8 numbers of the third batch. | current |
| `renew_eu/edf_factsheets.py` | European Defence Fund topic and factsheet sweep for lidar mentions (POINTER and the 2021–2024 topics in §D8). | unfinished |
| `renew_eu/period_summary.py` | Window sums, rate ratios and binomial tests, programme shares, and the hand-read 2023–2026 set. | current |
| `renew_eu/wp_topics.py` | Parses the Horizon Europe work-programme PDFs into a topic table with budgets and keyword counts. | current |
| `renew_eu/ft_search.py` | Funding & Tenders portal search. | unfinished |
| `renew_eu/README.md` | Folder index. | current |
| `renew_us/sbir_lidar_trends.py` | Lidar SBIR/STTR awards by fiscal year, agency, application and recipient from SBIR.gov's bulk award file (the 1 Oct 2026 file at the `mod_awarddatapublic` address). It produces the §D8 US tables. | current |
| `renew_us/sbir_candidate_rules_draft.py` | First version of the selection rules. | superseded |
| `renew_us/usasp_lidar_download.py`, `renew_us/usasp_lidar_analysis.py` | USAspending transactions naming lidar, FY2008–FY2026, with SBIR and Phase III flags (the §D8 non-SBIR table). | current |
| `renew_us/nsf_lidar_awards.py`, `renew_us/nasa_techport_lidar.py`, `renew_us/civil_3dep_table.py` | NSF awards, NASA TechPort projects and the USGS 3DEP spending table (§D8). | current |
| `renew_us/dod_darpa_jbook_scan.py` | Lidar mentions and programme lines in DARPA's budget justification books (SWEEPER, MOABB, LUMOS). | current |
| `renew_us/policy_grep_pdfs.py`, `renew_us/policy_signals_table.py`, `renew_us/renew_us_period_summaries.py` | NDAA, House report and Federal Register checks (§D3, §D6, §D8) and the period averages. | current |
| `renew_us/README.md` | Folder index. | current |

## Link budget, margin, dynamic range and benchmark (§C0 subsection 10), `c0_link_budget_2026-09/`

Scripts and edit inputs from late September 2026, archived on 9 Oct 2026. Paths into the original working folders appear as `<scratch>` and `<downloads>`, and paths into the report, reference and notes folders as `<report folder>`, `<refs folder>` and `<notes folder>`.

| File | Purpose | Status |
|---|---|---|
| `c0_10_restructured.md`, `apply_c0_10.py` | New text of §C0 subsection 10 (parts 10.1–10.7 at the time) and its hash-guarded write with global equation renumbering. | historical |
| `margin_block.py`, `patch_labels.py`, `link_budget_scaling_before_fix.py` | Margin, fog and rain block (Figure C0.10d) spliced into `build/figures/link_budget_scaling.py`, the class-label fix, and the script before the splice. | historical (installed) |
| `fmcw_near_field_weather.py`, `fmcw_margin_tradeoff.py` | Collimated coherent near field checked against the classic hard-target equation; margins, dark targets and fog for FMCW and ToF designs; the aperture-versus-energy trade. | current |
| `dynamic_range_model.py`, `c0_10_7_dynamic_range.md`, `apply_c0_10_7.py`, `verify_c0_10_7.py` | Dynamic range each design must handle (Eqs. of 10.7), the text of 10.7 and its write. | current / historical |
| `benchmark_real_lidars.py`, `benchmark_fullpapers.py`, `benchmark_final.py`, `c0_10_8_benchmark.md`, `apply_c0_10_8.py` | Model against Waymo, Pointcloud, indie, Wang et al., Sony, Toshiba, Toyota, Panasonic and product claims (10.8), its text and write. | current / historical |
| `check_eq_numbers.py`, `pts_per_joule.py`, `apd_check.py`, `arch_c0.md`, `c0_10.md`, `figblock.py` | Equation-number checks, the points-per-joule arithmetic of §C7b, the linear-APD check and earlier drafts. | historical |

## Chinese FMCW update (§D7), `d7_china_fmcw_2026-09/`

| File | Purpose | Status |
|---|---|---|
| `apply_d7.py` | §D7: RoboSense/SUSTech papers, long-range Chinese demonstrations, new firms, 2025–26 news. | historical |
| `apply_d7_hesai.py` | §D7: Hesai's in-house FMCW programme (2020 STAR prospectus, patents, 4DLidarOpen) and the RoboSense inventor wording. | historical |
| `scan_star_prospectus.py`, `scan_cn_pdfs.py`, `render_jilin.py`, `render_refs.py`, `find_pages.py`, `find_vis_code.py`, `scan_supp.py`, `verify_d7_pdf.py` | Page location and rendering in the sources (Hesai's draft prospectus, Jilin papers, Nature source data) and the PDF check after the write. | historical |

## Whole-report reader-considerate rewrite (Sep 2026), `rewrite_2026-09/`

| File | Purpose | Status |
|---|---|---|
| `REWRITE_BRIEF.md` | Brief given to the chunk rewriters (definitions next to use, global equation numbers, full sentences). | historical |
| `chunks.json`, `equation_labels.json` | Chunk boundaries and temporary equation labels. | historical |
| `check_chunk.py`, `merge_and_number.py`, `make_test_tagged.py`, `apply_fixes.py` | Per-chunk checker (numbers, URLs, tags, tables, banned words), merge with global `\tag` numbering, test tagging and the post-merge fixes. | historical |

## Other report edits of Sep 2026, `misc_edits_2026-09/`

| File | Purpose | Status |
|---|---|---|
| `apply_*.py` with their `.md` inputs (`c7b*.md`, `coherent_c3a.md`, `fom_c3b.md`, `meet_b8.md`, `modcost_b8.md`, `phone2lidar_c5a.md`, `trucking_b4.md`) | Section writes of that period: §C7b versions, A_mode definition, AS-DT1 fix, audits, iToF, phone-to-lidar, trucking and other fills. | historical |
| `make_build_folder.py`, `patch_fig_scripts.py`, `pep8_helper_spacing.py` | Creation of `build/`, the figure scripts' output folder, and PEP 8 spacing of the helper that sets it. | historical |
| `render_pages.py`, `verify_final_pdf.py`, `verify_peer_write.py`, `time_save.py`, `find_rm.py` | PDF rendering and post-write checks. | historical |

## Low-light ("starlight") night vision (§A7) and Fortsense (§C4b, §C5), `starlight_2026-10/`

The numbers of §A7 and its Figure A7.1 come from `build/figures/night_photon_budget.py`, which is stored with the report and embedded in the PDF; its printed tables are in `automotive_perception_report_figures/night_photon_budget_tables.txt`. The files below are the working and edit scripts of that round (9 Oct 2026).

| File | Purpose | Status |
|---|---|---|
| `photon_budget_night.py` | First version of the night photon budget (photons per lux, photoelectrons per pixel, read-noise boundary, SPAD count ceiling and daylight power), with a Gaussian green-channel model. | superseded by `build/figures/night_photon_budget.py`, which calibrates the CMOS sensitivities to OmniVision's published values |
| `a7_section.md` | Text of §A7 as inserted, with placeholder equation tags 9013–9021 (renumbered to (13)–(21) on insertion). | historical |
| `apply_a7_fortsense.py` | Hash-guarded insertion of §A7 and of the Fortsense additions (§B7.1, §B8 consumer path, §C0 subsection 10.7 pointer, §C4b, §C5 table row and paragraph, foundry check, §D chokepoint table, Appendix 1), plus the guide, executive-summary, Part A introduction and §A1 Mercedes edits. Followed by `readability_2026-10-03/renumber_equations.py --allow-reorder`. | historical |
| `apply_a7_codenote.py`, `apply_a7_fixes.py`, `apply_a7_wording.py` | The code pointer under Figure A7.1; two corrections after the PDF check (O-Film's FL6031 lidar with two-dimensional addressing; the image-intensifier row); and wording aligned with the sources (Mercedes test phrasing, LED-flicker gloss, USML XII(c)). | historical |
| `verify_claims.py`, `render_key_pdfs.py` | Checks of vendor claims against the downloaded pages, and renders of the Xintong announcement and the Tower–Fortsense press release. | historical |
| `extract_agent_results.py` | Recovered finished research agents' reports from a working log; archived as a stub, since the log is not included. | historical |
| `agents/spadimaging_*.py`, `agents/fortsense_*.py`, `agents/lowlight_*.py` | Helper scripts of the three research agents (SPAD imaging, Fortsense, low-light CMOS and active imaging): HTML-to-text, PDF rendering and cropping, Fortsense news and patent downloads. Their downloads stayed in the working folder. | historical |

## Publication on GitHub (2026-10-10), `publish_2026-10/`

The report folder, except `refs/`, is published as a repository with a web version (`index.html`, served by GitHub Pages) and the PDF. The report opens with an AI-use disclaimer; it has no "read in full" remarks or pointers to `refs/`, and the paywalled press articles in Appendix 2 link to their publishers.

| File | Purpose | Status |
|---|---|---|
| `add_disclaimer.py` | Hash-guarded insertion of the disclaimer as a fenced div after the subtitle; `build/build_pdf.py` places it on the title page. | historical |
| `publish_texts.py`, `publish_edits.json` | Seven edits applied with `../gapfill_2026-10/edits_partB_definitive.py --texts publish_texts --name publish`: no "read in full" remarks, no `refs/` pointers, DOI links for the ISSCC 2021 and *Nature* 2026 papers, and the Appendix 2 heading "Press articles (paywalled)". | historical |
| `add_press_links.py`, `press_links.json` | Links 28 of the 45 press titles in Appendix 2 to the publishers' pages (found by search and checked by title and date; three are medium-confidence matches whose author, date and facts agree). The other titles stay as plain citations. | historical |
| `make_web_html.py` | Turns the print HTML kept by `build/build_pdf.py` (`KEEP_HTML=1`) into `index.html`: figures linked from `automotive_perception_report_figures/` instead of embedded, a screen-only stylesheet with screen-sized headings, a floating link back to the contents, and a link to the PDF under the disclaimer. Source links are made clickable in the build (`autolink_bare_uris` in `build/build_pdf.py`). | current |
| `link_audit.py` | Read-only check of the links in `index.html`: kinds of link, relative links to unpublished files, anchors without a target, malformed URLs and URLs left as plain text. | current |

## Neutral-tone revision and source checks (2026-10-10 and 11), `tone_2026-10/`

Before publication every published file was reviewed for non-neutral wording (loaded or emotive words, unattributed judgements of people, companies and countries, national framing, scare quotes and rhetorical headings, promotional or unhedged certainty, opinion stated as fact). The author chose which kinds to change: nationality and geopolitical framing; scare quotes, promise framing and "claims"; unhedged certainty, investment vocabulary and spec-sheet pejoratives. Metaphors of death, war, hype and contest were kept. All factual inconsistencies the review found were corrected, after checking the sources (Luminar's 8-K of 14 May 2025, Hesai's FY2024 results, MOFCOM Announcements No. 57 and No. 70 of 2025, Momenta's 2021 Mpilot configurations, NHTSA PE22-002, the FMVSS 127 and connected-vehicle rules, and the filings and releases behind the addendum). The addendum was reconciled with the report, which takes precedence, and its summary table now gives each item's real status. The edits were applied as hash-guarded exact-substring pairs: 411 in the report, 151 in the addendum, 70 in the earlier draft, 25 in the readability review and 5 in the reading list. Equation tags, equation references and section references were checked after the edit. In this archive, local paths are replaced by placeholders, downloaded source files are referred to by descriptive names, and three scripts that read working logs not kept here are archived as stubs.

The decision lists and the generated pairs are not archived here: they quote the removed text, including local paths, so they are kept with the author's unpublished records.

| File | Purpose | Status |
|---|---|---|
| `check_quotes.py` | Parses the review tables and finds every quoted span in the report, so each finding carries current line numbers. | historical |
| `show_lines.py` | Prints selected report lines with their numbers. | current |
| `build_review_doc.py` | Assembles the consolidated review from the per-part tables, with current line numbers and pattern tags. | historical |
| `build_candidates.py` | Turns the reviewed findings and a decision file into edit pairs and shows each in context; reports any pair whose text is not unique. | historical |
| `simulate_apply.py` | Applies a pair list to a copy of a file, in order, keeping line endings, and reports any pair that fails. | current |
| `validate_report.py` | Compares an edited report with the original: equation tags, equation and section references, `$` parity and spacing on changed lines, changed headings. | current |
| `apply_pairs.py` | Applies a pair list to a file: expected hash, unique matches, a backup first and a re-hash just before writing. | current |
| `research/html2txt_grep.py`, `research/fr_page_locator.py`, `research/render_pdf_pages.py` | Source-check helpers: keyword-in-context search of saved HTML, Federal Register page numbers for matches, and PDF pages rendered to PNG with their text. | historical |

## Restructured physics chapter (§C0, 2026-10-12), `c0_restructure_2026-10/`

§C0 was reorganized as a textbook chapter in six parts, following the measurement chain: measuring one point (1.1–1.4), from points to images (2.1), how much light comes back (3.1–3.3), how much light is needed (4.1–4.3), range and its limits and robustness (5.1–5.5), and testing the model (6.1–6.2), with a closing table of where each relation is used. Every table, derivation and number was carried over from the previous text by exact copy between anchors; the new text is the connective prose, the merged passages (one photon budget, one set of detection statistics under the per-point rule, one treatment of weather) and the renumbered references. The duplicate single-speckle law was merged (old Eq. (35) into Eq. (46)), equations were renumbered in document order, and Figures C0.10a–d became Figures C0.1–C0.4. The old subsections map to the new ones as follows:

| Old (before 12 Oct 2026) | New |
|---|---|
| 1. Pulsed direct time of flight | 1.1 (timing); 3.1 (photon budget of one pulse); 5.2 (range scaling) |
| 2. FMCW coherent ranging | 1.3 |
| 3. Beams, pixels and sampling | 2.1 |
| 4. Velocity | 1.4 |
| 5. Eye safety and sunlight | 4.2 (solar background); 5.3 (eye safety) |
| 6. Detector gain and excess noise | 4.1 |
| 7. Detection and false alarms | 4.3 |
| 8. Weather | 3.3 (extinction); 5.4 (reach in fog and rain) |
| 9. Amplitude-modulated (phase) ranging | 1.2 |
| 10.1 Model, assumptions and symbols | assumptions at the start of 3; symbols in 3.1–3.3 |
| 10.2 Link loss | 3.1 (direct), 3.2 (coherent) |
| 10.3 Detection statistics | 4.2 (background of the model), 4.3 |
| 10.4 Detection level and maximum range | 5.1 |
| 10.5 Range scaling | 5.2 |
| 10.6 Margin at short range | 5.4 |
| 10.7 Dynamic range | 5.5 |
| 10.8 Benchmark | 6.1 |
| 10.9 What the model leaves out | 6.2 |

| File | Purpose | Status |
|---|---|---|
| `c0_lib.py` | Assembler: a plan of new text and exact copies of old lines between anchors, with counted replacements, table-column removal and indentation changes. | historical |
| `c0_plan_a.py`, `c0_plan_b.py`, `c0_plan_c.py` | The plan of the new §C0: opening and parts 1–2; parts 3–4; parts 5–6 and the closing table. | historical |
| `c0_build.py` | Builds a working copy: assembles §C0, lists the old lines not carried over, remaps the 110 references to §C0 subsections elsewhere in the report (with per-line overrides where an old subsection split), updates the reader's guide, renames the figures and checks every internal reference. | historical |
| `make_renumber_copy.py` | Points a copy of `readability_2026-10-03/renumber_equations.py` at the working copy; it was run with `--allow-reorder --redirect 35=46`. | historical |
| `check_c0.py` | Checks the new §C0: unbalanced `$`, doubled spaces, untagged displays, the tag range and the heading list. | historical |
| `c0_install.py` | Installs the working copy into the report (hash-guarded) and updates the files that refer to §C0. | historical |
