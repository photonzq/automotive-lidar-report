# Round 1 fix specification (2026-10-04)

The author has decided to apply the open findings of the readability review. Round 1 covers the sentence-level and within-block fixes, the follow-up findings and the report-wide symbol scheme. Later rounds (done centrally, not by you) cover the model recomputations, the moves between sections with equation renumbering, and new sources.

## Files

- Live report (read only for you): `<report folder>\automotive_perception_report_2026-09-27.md`. It has changed since the review, so copy every "old" text from the live file, not from a review report.
- Findings for your block: `scripts_archive\readability_2026-10-03\reports\<label>.md`, plus `<label>_followup.md` if present.
- Your output: `scripts_archive\readability_2026-10-03\edits\<label>.json`. This is the only file you may create.
- Validator: `python scripts_archive\readability_2026-10-03\validate_edits.py scripts_archive\readability_2026-10-03\edits\<label>.json`. Use `python`, and run it from the report folder. It must print OK before you finish.

## Hard rules

- Never modify the report or any other existing file. Do not run the build scripts. Do not use web or network tools. Do not start helper agents.
- Edit only text inside your block (between the headings given in your task). Findings that need a change outside your block go to `skipped` with kind `cross_section`, quoting the exact text and the proposed fix.
- Never write placeholders such as "[author: …]", "[state …]", "[source]" or "[confirm]" into the report text. If a fix needs a fact you do not have, put it in `skipped`.
- Never write any personal email address or contact detail into anything.

## What to apply

Apply every finding in your reports (all severities), including the follow-up findings, that can be fixed from the report itself. The fixes are:
- rewrites for clarity;
- splitting long sentences;
- defining symbols and acronyms at first use in the section;
- adding missing derivation steps, with the substitution shown;
- fixing arithmetic, units and rounding;
- fixing cross-references (§ and Eq. pointers);
- evidence tags following the legend: [P] primary; [I] independent, including academic papers; [T] trade press; [E] own estimate; [U] unverified; [MR] market research such as Yole or ResearchInChina; [S] secondary, such as Wikipedia or a search extract; [D]/[NT]/[R] deployability;
- table lead-in sentences;
- removing repetition inside your block;
- the symbol scheme below, inside your block.

Skip a finding whose fix has already been made in the live text: list it as `already_fixed`.

House style:
- Full sentences, not telegraphic notes.
- Every estimate shows equation, inputs, substitution and result.
- Symbols are defined next to their use.
- Math uses `$…$` and `$$…$$`, never `\(` or `\[`. In subscripts, `\rm` must come right after `{`: write `P_{FA,{\rm pt}}`.
- Currency is written `\$`.
- No versioning words ("added", "corrected", "updated", "revised", "now", "new" describing edits).
- At most three bullet levels.
- Keep every existing `\tag{N}` as it is. Do not add or remove display equations; Round 3 handles numbering.

## Excluded from Round 1 (list in `skipped` with the kind shown)

- `model_round2`:
  - anything that changes the FMCW dwell definition, channel counts, receiver energy $E_{\rm rx}$, sensor power totals or the FMCW/ToF ratios in §C7a, §C7b or §F6;
  - the ToF wavelength or efficiency basis, and the $\eta$ convention numbers, in §C10.2–§C10.3b;
  - the §C9a interference model and its rates.
  
  Wording fixes elsewhere in those subsections are fine.
- `structural`:
  - moving material between sections or subsections (the §C0 subsection 9 and 10.7 survey material, §C7b 2(h)–(i), §C5 Fastree3D history, §C10.3a/§C10.3b order, §E2 radar-market sideline);
  - merging duplicated equations;
  - shortening the §C7b short answer by moving its detail elsewhere.
- `needs_source`: a fix that needs an outside fact or source. Give the claim, its location and what is needed.
- `needs_decision`: a fix that needs an author decision not covered here.

## Symbol scheme (apply inside your block, in equations and text)

| Quantity | Symbol to use | Replaces |
|---|---|---|
| Optical energy emitted toward one point (or sample) | $E_{\rm pt}$ | $E_{\rm tx}$ (§C0 subsection 10), $E_{\rm opt}$ (§C7a, §C7b), $E_{\rm pulse}$ when it means per point (§C10.2, §E9), $E_{\rm point}$ (§E11.3), $E_s$ (§C10.3) |
| Energy of one laser pulse (one shot) | $E_{\rm p}$ | — |
| Detected signal photons per point (summed over its shots) | $N_s$ | — |
| Detected signal photons per pulse | $N_{s,1}$ | $N_s$ where it means one pulse (§C0 Eq. (23) and its uses) |
| Signal photons in the LO's spatial mode (before detection) | $N_{\rm mode}$, with $\bar n=\eta N_{\rm mode}$ detected | $N_s$ in §C0 subsection 2 |
| Photoelectrons a detection needs | $n_{\rm req}$ | $N_s$ in §C3b Eq. (62) |
| Maximum detection range | $R_{\max}$ | — |
| Unambiguous range | $R_{\rm amb}$ | $R_{\max}$ where it means unambiguous range |
| Half-width of a BEV grid | $R_{\rm grid}$ | $R_{\max}$ in §E11 Eq. (167) |
| Solid angle | $\Omega$ (only for solid angle) | — |
| Optical scan rate (angular speed of the beam) | $\dot\theta$ (rad/s or °/s) | $\Omega$ as a scan rate (§C0 subsection 2, §C4d Eq. (71), §C7 Eqs. (86)–(87), §C7b Eqs. (116)–(117)), $\omega$ in §C10.3a |
| Mechanical mirror or polygon rate | $\dot\theta_{\rm m}$ ($=\dot\theta/2$ for a reflective mirror) | $\omega$ in §C7 (e.g. Eq. (88)) |
| Electrical (noise) bandwidth | $\Delta f$ | — |
| Scanner-induced frequency spread | $\Delta f_{\rm scan}$ | $\Delta f$ as a spread |
| FMCW beat bandwidth | $\Delta f_{\rm beat}$ | $\Delta f$ as a beat bandwidth |
| Shared efficiency (optics × detector, × mixing for coherent) | $\eta$, excluding polarization and mode/truncation factors (those sit in $A_{\rm mode}$ through $t^2/2$, as in §C0 subsection 10.1) | — (the §C10 number changes are Round 2) |
| Laser wall-plug efficiency | $\eta_{\rm wp}$ | $\eta_{\rm WPE}$ |
| Fixed sensor overhead power | $P_{\rm oh}$ | $P_0$ |
| APD multiplication gain | $M$ | — |
| Link margin | $\mathcal{M}$, $\mathcal{M}_0$ | $M(R)$, $M_0$ (§C0 subsection 10.6) |
| Marcum function | $Q_N(a,b)$, with $N$ the number of summed looks | $Q_M$ |
| Sweep rate (sweeps/s) | $S$ | — |
| Summed speckle gain | $G$ | $S$ in §C0 Eq. (40) |
| Lidar ratio | $S_{\rm L}$ | $S$ in §C0 subsection 10.6 |
| Beamwidth (FWHM) in §C10 | $\theta_{\rm B}$ | $\theta$ where it means beamwidth |
| Cell angular pitch | $\theta_{\rm cell}$ | $\theta$ where it means the cell |
| Angular spacing of points | $\delta\theta$ | $\Delta\theta_h$, $\theta_{\rm step}$, $\Delta\theta$ as a point spacing |
| Braking deceleration | $a_{\rm b}$ | $a$ in §E2 Eq. (159), §E6 Eq. (162), §E12 Eq. (170), §F6 Eq. (184) |
| Round-trip delay | $\tau=2R/c$ | $\Delta t$ as a delay (§C0 subsection 1) |
| Histogram bin width | $\Delta t_{\rm bin}$ | $\Delta t$ as a bin width |
| Time to contact (§E12) | $t_{\rm c}$ | $\tau$ there |
| Mirror resonance (§C4d) | $f_{\rm mirror}$ | bare $f$ for the mirror frequency |

- Ionization ratio $k$: define it as the ionization coefficient of the weaker-ionizing carrier divided by that of the stronger one (hole/electron in Si; electron/hole in InP).
- Shared inputs:
  - The pedestrian is 0.5 m × 1.7 m everywhere; recompute pixel and point counts that used 1.8 m.
  - The truck stopping distance is 257 m ($v=29.2$ m/s, $t_{\rm r}=1.5$ s, $a_{\rm b}=2.0$ m/s²).
  - Keep the 0.7 $g$ firm stop of §A6 and the 5–6 m/s² of §E2 apart, and say why they differ: a firm dry-road stop against the UN R157 planning value.

## Output format

```json
{
  "block": "<label>",
  "edits": [
    {"id": "<label>-001", "finding": "report #12 (or follow-up #3, or symbol scheme)", "old": "<exact current text>", "new": "<replacement>", "why": "<one line>"}
  ],
  "skipped": [
    {"finding": "report #7", "kind": "needs_source|needs_decision|structural|model_round2|cross_section|already_fixed", "location": "<heading and short quote>", "detail": "<what is needed, or the proposed cross-section fix with exact text>"}
  ]
}
```

- Make each "old" the smallest span that is unique in the whole report and contains the change.
- Edits must not overlap. Merge nearby changes into one edit.
- Write the JSON with Python (`json.dump(..., ensure_ascii=False, indent=1)`). Run the validator, fix every problem it reports and re-run until it prints OK.
- Final report: the counts (edits and skipped, by kind) and the validator's last line. Do not paste the edits.
