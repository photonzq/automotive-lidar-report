# Re-baseline: what is ready and what to do after the parallel edit is done

Ready (validated 14:40 against the 12:04 snapshot `../fmcw/report_peer_1204.md`, sha e79a9269e98e):
- `edits.py` (133 anchored edits) + `s103_new.md` (new §C0 10.3), applied by `apply_rebase.py`
  (maps snapshot equation numbers to the live file by equation body; one new equation -> global renumber).
- `patch_lbs.py`: patches build/figures/link_budget_scaling.py (fig_detection two-ramp, CASES label "FMCW, per look").
  Tested on `lbs/link_budget_scaling_peer1156.py` (copy of 11:56 from the parallel edit); non-detection tables identical.
- `../fmcw/model/fmcw_tof_system_budget.py`: patched system-budget model (4 looks, harmonized background,
  label layout); regenerate with `../fmcw/model/patch_model.py` from `fmcw_tof_system_budget_orig.py`.

After "done" (in order):
1. Re-read the parallel edit's list of places quoting old numbers; add edits for any new text. Diff the live file vs snapshot.
2. `python apply_rebase.py --dry`, review, then `python apply_rebase.py` (hash-guarded).
3. Check build/figures/fmcw_tof_system_budget.py still equals `../fmcw/model/fmcw_tof_system_budget_orig.py`,
   then copy the patched model over it. Run `patch_lbs.py build/figures/link_budget_scaling.py <same>` on the live copy.
4. Run both scripts from build/figures (outputs go to automotive_perception_report_figures/).
5. `python build/build_pdf.py` then `python build/check_pdf.py`; render and view pages of §C0 10.3, Fig C0.10b,
   §C7a (Fig C7a, table), §C7b (d), (h), subsection 5 table.
6. Identity check of the md, the PDF text and metadata, and the scripts.
7. Notify the parallel edit: what changed, where, new equation (40) and renumbering, figure changes; ask for a re-read.
8. Final summary to the author, incl. judgement changes: parity 2032 5–10% -> 3–7% (exec summary, §C7a, §C7b),
   receiver-chip signpost (>=256 receivers at <=5 mW, 20–30%; qualified 8–12%).
