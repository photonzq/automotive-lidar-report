# Round 2 specification: model harmonizations and the numbers that follow from them

Report (live, read-only for you): `<report folder>\automotive_perception_report_2026-09-27.md`. Its sha256 begins **189682c75e26**. The work folder is `<report folder>\scripts_archive\readability_2026-10-03\`.

**Your deliverable.** Write an edit list, `edits\round2\<label>.json`, in the format of Round 1 (`fix_spec.md`, "Output format"):

```
{"block": "<label>", "edits": [{"id", "finding", "old", "new", "why"}], "skipped": [{"finding", "kind", "location", "detail"}]}
```

Then run `validate_edits.py edits\round2\<label>.json` until it prints OK.

**Hard rules.**
- Never modify the report. Edit only inside your own sections (list at the end). Each `old` must occur exactly once in the live report, and no two of your edits may overlap.
- Follow the house rules of `fix_spec.md`:
  - every estimate shows its equation, inputs, substitution and result;
  - symbols follow the report-wide scheme (the table in `fix_spec.md`);
  - evidence tags; full sentences; math in `$...$`;
  - currency written `\$`;
  - `\rm` directly after `{` in subscripts (texmath);
  - no versioning words ("corrected", "updated", "revised", "now", "newly", "added") and no notes about editing.
- **Add no new `\tag{}`** and remove none: the 188 tags must stay sequential. Use inline math or rewrite existing displays in place, keeping their tags.
- **Stay off:** Part B (being rewritten in a separate pass), §D8 and Appendix 1.
- Compute every changed number. Copy no number from this spec into the report unless its derivation, with substitution, is in the report or in your edit. Where a sentence rests on a value that changes, rewrite the sentence so that it stays true.
- If a model change makes a conclusion change, say so plainly in the text. Do not keep a conclusion the numbers no longer support.
- Put any calculation script in `round2\scripts\`. Use sanitised paths and add one line per script to `round2\scripts\INDEX.md`. Interpreter: `python`.

## The author's decisions (2026-10-05), which this round implements

1. **FMCW dwell (ungated)**. One FMCW dwell definition is used report-wide: $T_{\rm dwell}=T_{\rm int}+2\tau$, the §C7b Eq. (107) form $E_{\rm pt}/P_{\rm ch}+2\tau$.
   - In the §C7a model, $T_{\rm int}=2\times5$ µs, the up- plus down-chirp, and $\tau=2R/c=1.33$ µs at the 200 m design range, so $T_{\rm dwell}=12.67$ µs.
   - The central case is ungated, so the laser also emits during the round trips: the emitted optical energy is $E_{\rm pt}\,T_{\rm dwell}/T_{\rm int}$.
   - ADC samples and their energy count the useful windows only, while the per-channel analog power runs for the whole $T_{\rm dwell}$. The raw ADC data counts the useful windows.
   - The per-channel CW power is $E_{\rm pt}/T_{\rm int}$, i.e. 30 mW in the central case, emitted for the whole dwell.
2. **ToF macro-pixel field 0.05° × 0.05°** (not 0.1° × 0.05°). This is the IMX479 grid, 2,400 × 520 over 120° × 26°, so $\Omega_{\rm pix}=(8.727\times10^{-4})^2=7.615\times10^{-7}$ sr. Every sunlight background rate per macro-pixel computed with 0.1° × 0.05° halves; dead fractions, live fractions, counts per bin and everything that follows are recomputed.
3. **ToF n_req keeps the ×1.45 implementation margin.**
   - With the new background, the ideal requirement of §C0 subsection 10.3 is 15.0 counts, so the model uses $n_{\rm req}=25\times15.0/17.26=21.7$.
   - Low and high cases scale alike: 17.4 / 21.7 / 30.4 for 2026; 17.6 / 22.1 / 26.5 for 2032.
4. **Sunlight convention.** Keep §C6(d)'s irradiances for the model. Label §C4c's per-pixel values as ASTM G173 ±10 nm band averages. Add one sentence linking the two: the band average, which is what a filter integrates, is about 1.5× lower at 940 nm than the near-point value the model uses, so the model is conservative for 940 nm ToF.
5. **FMCW parity follows §C7b subsection 5.**
   - §C7a subsections 5–6 become a short summary of, and pointer to, §C7b's three-condition definition at 200 m.
   - Drop "≥100 mW per channel", which §C7b subsection 2(h) shows is not the lever.
   - Restate the linewidth condition from Eq. (115): ≲27 kHz for 1 dB, ≲55 kHz for 3 dB at 300 m, as tabulated there.
6. **η convention (§C10).** η excludes polarization and mode shape. The single-polarization and truncation factor $t^2/2=0.419$ sits in $A_{\rm mode}=(t^2/2)\lambda^2/\Omega_{\rm cell}$, as in §C0 subsection 10.1 and §C10.3b.
   - Coherent: η = 0.25, the §C0 design value: optics × detector × mixing.
   - ToF: η = 0.5 × 0.37 × 0.885 = 0.164.
7. **ToF in §C10.3–3b is the 940 nm SPAD model** of §C0/§C7a, with $n_{\rm req}=21.7$ and η = 0.164, not 905 nm with 20 and 0.15.
8. **USAspending tag [P]**. Agent C3a edits only, which the merge handles. Ignore this item.

## Model outputs to use

These are the outputs of the installed scripts:
- `build/figures/fmcw_tof_system_budget.py`, tables in `automotive_perception_report_figures/fmcw_tof_system_budget_tables.txt`;
- `link_budget_scaling.py`;
- `wavelength_eye_safety_background.py`;
- `coherent_mode_coverage.py`;
- `scripts_archive/readability_2026-10-03/round2_c10_3_power_table.py` and `check_poisson_claims_round2.py`.

Read the tables files themselves for anything not listed here. In each row below, old → new.

**ToF background and detection** (§C0 10.3, §C6(d), §C7a):

| Quantity | 2026 | 2032 |
|---|---|---|
| Background r_bg, night / central / full sun (counts/s) | 0 / 3.66e8 / 7.31e8 → 0 / 1.83e8 / 3.66e8 | 4.45e8 → 2.22e8 (central) |
| Paralyzable dead fraction, central (r = r_bg/9 per SPAD, τ_d = 6 ns) | 21.6% → 11.5%, i.e. $r\tau_d$ 0.244 → 0.122 and live fraction 0.784 → 0.885 | 26% → 14% |
| Paralyzable dead fraction, full sun | 39% → 21.6% (live 0.784) | 45% → 26% |
| Counts per 1 ns bin over 10 shots ($b=r_{\rm bg}\,\Delta t_{\rm bin}N_{\rm shots}(1-f_{\rm dead})$), central | 2.87 → 1.62 | 3.31 → 1.92 |
| Counts per 1 ns bin, full sun | 4.49 → 2.87 | — |

Ideal counter for the central case (2,000 bins, 5e-7 per bin, 90 % detection):
- threshold 15 → 12 counts; the tail is 1.15e-6 at 11 counts and 1.54e-7 at 12;
- required signal 17.26 → 14.98 (s + b = 16.60); the P_D = 0.5 requirement 11.8 → 10.0;
- P_D at $\bar n=25$: 0.997 → 0.999.

Non-paralyzable alternative: live fraction 0.891, b = 1.63, threshold 12, ideal 14.97. The change is under 0.1 % (the earlier 18.4 against 17.3 no longer applies).

Shots per point 5 / 10 / 20: b = 0.81 / 1.62 / 3.24, thresholds 9 / 12 / 16, ideal 12.2 / 15.0 / 18.1 counts. That is about 20–23 % per factor of two (earlier 14.0 / 17.3 / 22.5).

Signal efficiency η: 0.5 × 0.37 × 0.784 = 0.145 → 0.5 × 0.37 × 0.885 = 0.164.

Events per point over the 20.8 µs listen: 5,968 background + 25 signal ≈ 5,990 → 3,369 + 21.7 ≈ 3,390. The Poisson spread of the background is $\sqrt{3{,}369}=58$.

**§C6(d) and §C4c per-pixel rates** (0.05° × 0.05°, 25 mm aperture, optics 0.5): every 0.1° × 0.05° value halves.
- §C6(d), 940 nm, 10 nm filter, ρ = 0.9, PDE 0.3: 5.93e8 → 2.965e8.
- §C6(d), 905 nm, 20 nm filter, ρ = 0.9: 2.2e9 → 1.1e9.
- Dead fractions, recomputed for each row ($r=r_{\rm bg}/9$, τ_d = 6 ns):
  - paralyzable $1-e^{-r\tau_d}$;
  - non-paralyzable $r\tau_d/(1+r\tau_d)$.
- §C4c table, ASTM band averages (`wavelength_eye_safety_background_tables.txt`):
  - 905 nm/0.24/20 nm 8.11e8;
  - 905 nm/40 nm 1.62e9;
  - 940 nm/0.37/10 nm 2.84e8;
  - 1,550 nm/0.30/10 nm 3.38e8;
  - 1,550 nm/0.80/10 nm 9.02e8.
- Count-rate headroom:
  - Si 3×3 at 940 nm: 0.53 of its 5.4e8 ceiling (was ≈1.05);
  - InGaAs: ≈340× its ≈1e6 ceiling at a 1 µs hold-off, ≈3,400× at 10 µs (was ≈700× and ≈7,000×).

**§C7a model** (energy per point at 200 m, 10 %, low / central / high, nJ; old → new):
- ToF 2026:
  - E_opt 58/93/167 → 51/72/113;
  - laser electrical 195/466/1111 → 169/358/756;
  - electronics 20/70/126 → 20/57/102;
  - total 215/536/1237 → 189/415/858.
- ToF 2032:
  - E_opt 48/81/131 → 42/61/86;
  - laser 137/323/653 → 121/246/428;
  - electronics 10/44/86 → 10/34/70;
  - total 147/368/739 → 131/280/497.
- FMCW 2026:
  - E_opt 152/303/885, unchanged useful light;
  - **emitted 192/384/1121** (new row: × T_dwell/T_int = 12.67/10);
  - laser electrical 759/2023/8850 → 961/2563/11212;
  - electronics 1264/2230/3773 → 1317/2337/3987;
  - total 2022/4253/12623 → 2278/4899/15199.
- FMCW 2032:
  - E_opt 121/190/364;
  - emitted 154/240/461;
  - laser 405/862/2428 → 513/1092/3075;
  - electronics 387/614/1241 → 408/646/1305;
  - total 791/1476/3668 → 920/1738/4380.
- Ratios, central:
  - FMCW/ToF electrical energy 7.9× → **11.8×** in 2026 (4.899/0.415), 4.0× → **6.2×** in 2032 (1.738/0.280);
  - useful optical energy 3.2× → **4.2×** (0.303/0.072); emitted (ungated) **5.3×** (0.384/0.072).
- Sensor power (3 W overhead + rate × E), W, at 1/2/5/10/25/40 Mpts/s:
  - ToF 2026 3.5/4.1/5.7/8.4/16.4/24.5 → 3.4/3.8/5.1/7.2/13.4/19.6;
  - ToF 2032 3.4/3.7/4.8/6.7/12.2/17.7 → 3.3/3.6/4.4/5.8/10.0/14.2;
  - FMCW 2026 7.3/11.5/24.3/45.5/109.3/173.1 → 7.9/12.8/27.5/52.0/125.5/199.0;
  - FMCW 2032 4.5/6.0/10.4/17.8/39.9/62.0 → 4.7/6.5/11.7/20.4/46.5/72.5.
  - At 15 Mpts/s: FMCW 2026 ≈67 W → $3+15\times4.899=76.5$ W; ToF 2026 $3+15\times0.415=9.2$ W.
- FMCW channels at 1/2/5/10/25/40 Mpts/s:
  - 10/20/50/100/250/400 → **13/25/63/127/317/507** at the 12.67 µs dwell;
  - the "4 µs" case becomes 4 µs integration + 2τ = 6.67 µs: 4/8/20/40/100/160 → 7/13/33/67/167/267;
  - receivers are ×4.
- Optical power at 10 / 25 Mpts/s: useful 3.03 / 7.59 W; **emitted 3.84 / 9.61 W**. SOA/laser heat 17.2 / 43.0 → 21.8 / 54.5 W.
- Raw ADC data is unchanged (4.91 Tb/s at 10 Mpts/s).
- ToF optical power at 25 Mpts/s: 2.33 → 1.80 W.

**Link budget, §C0 subsection 10** (`link_budget_scaling_tables.txt`):
- SPAD 940 nm design: n_req 25 → 21.7, η 0.145 → 0.164, L_det 94.4 → 95.5 dB.
- R_max at 0.1 µJ for D = 10/25/50 mm: 82/204/400 → 94/232/455 m.
- E needed by the 25 mm SPAD at 100/200/300/500 m: 23.7/96.5/220.8/634.3 → 18.2/74.2/169.7/487.7 nJ. The FMCW best-D energies are unchanged (150/303/458/778 nJ).
- Ratio of best-D FMCW to 25 mm SPAD: 6.33/3.14/2.08/1.23 → 8.24/4.08/2.70/1.59. Against a SPAD with the same D_opt: 2.47/2.45/2.43/2.39 → 3.21/3.18/3.16/3.11.
- The gap closes as 1/R and crosses 1 near $4.08\times200\approx820$ m (earlier ≈600 m).
- 10.6 designs:
  - the 25 mm SPAD design needs 96 → 74 nJ ("0.32×" → $74/303=0.24\times$);
  - "0.1 µJ … reaches 204 m, scaled by $(200/204)^2$" becomes "reaches 232 m, scaled by $(200/232)^2=0.743$";
  - margins and ranges of the 200 m-sized designs are unchanged, being geometry only.
- Figure C0.10b (detection statistics), bright-sun counting curve: b = 1.62, k = 12.

**§C10** (`round2_c10_3_power_table.py`, `coherent_mode_coverage.py`):
- Eq. (139) on the new conventions:
  - $P_{\rm coh}=N_{\rm req}E_{\rm ph}\pi R^2f_{\rm frame}\Omega_{\rm FOV}/(\rho\,(t^2/2)\lambda^2\eta)$ with η = 0.25 gives 58.5 / 175.5 W for N_req = 10 / 30 (was 20.4 / 184 W). With the measured η = 0.112, ×2.23.
  - P_ToF at 940 nm, n_req 21.7, η 0.164, 25 mm:
    - 0.1°×0.1° 0.215 W (ratio 272–816×);
    - 0.1°×0.05° 0.430 W (136–408×);
    - 0.05°×0.05° 0.860 W (68–204×);
    - 0.025° 3.44 W (17–51×);
    - 0.0125° 13.8 W (4.2–13×).
  - Parity cells: 0.0061°–0.0035°. Diffraction limit $\lambda/\sqrt{A_{\rm rx}}=0.0024^\circ$ at 940 nm.
- Speckle and fading cases scale with N_req: about 5.85 W per detected count, e.g. 88.5 → 518 W and 259 → 1,515 W. Recompute every case from its own N_req.
- ToF Goodman modes at 940 nm (25 mm): 0.1° 1,752 (simple 1,692); 0.05° **451** (simple **423**); 0.025° 118 (106). Earlier at 905 nm: 485 and 456 at 0.05°.
- Coherent counts are unchanged.

## Sections, by agent label (edit only inside your own)

- **R2A_C0:** §C0 only, from `## C0.` to `## C1.`.
- **R2B_C4-C6:** §C3b, §C4, §C4b, §C4c, §C4d, §C5, §C5a, §C6 and §C8.
- **R2C_C7-C7a:** §0 (executive summary), §C7, §C7a, §D7 (only sentences quoting the FMCW/ToF ratio or FMCW per-channel light), §F6, and §F/§G sentences quoting these model numbers.
- **R2D_C7b:** §C7b only.
- **R2E_C10:** §C10 to §C10.7 only.
- **R2F_C9:** §C9 and §C9a only. This is the interference model; see the separate brief.

Finish by listing in `skipped` anything outside your sections that quotes a number you changed, as kind `cross_section`, with its exact text and your proposed replacement. Report the counts only.
