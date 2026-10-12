# Build files for the automotive perception report

This folder holds everything needed to rebuild the report's PDF and every figure in it. The PDF carries the code for its figures: it embeds the figure scripts in `figures/` (and the one input data file they need) as attachments.

## Folder layout

| Path (relative to the report folder) | What it is |
|---|---|
| `automotive_perception_report_2026-09-27.md` | The report source: Markdown with LaTeX math. Display equations carry `\tag{N}`. |
| `automotive_perception_report_2026-09-27.pdf` | The built PDF. It embeds the figure scripts and `lidar_equity_prices_weekly.csv` as attachments. |
| `automotive_perception_report_figures/` | Figure outputs only: a PNG (used by the report) and a vector PDF for each figure, and a `…_tables.txt` file with the numbers each script prints. |
| `build/build_pdf.py` | Builds the PDF (see "How the PDF is built"). |
| `build/check_pdf.py` | Sanity checks on the built PDF. |
| `build/report.css` | Print stylesheet (A4, Arial). |
| `build/figures/` | One Python script per figure, plus `lidar_equity_prices_weekly.csv`, the input data of `lidar_equity_hype_cycle.py`. |

## Which script draws which figure

| Script (`build/figures/`) | Figure file(s) | Where in the report |
|---|---|---|
| `link_budget_scaling.py` | `link_budget_loss_vs_range.png`, `link_budget_detection_statistics.png`, `link_budget_range_scaling.png`, `link_budget_margin_weather.png` | Figures C0.1–C0.4: C0.1 in §C0 subsections 3.2 and 5.1, C0.2 in 4.3, C0.3 in 5.2 and C0.4 in 5.4 |
| `lidar_equity_hype_cycle.py` (reads `lidar_equity_prices_weekly.csv`) | `lidar_equity_hype_cycle.png` | Figure C3a, §C3a subsection 5 |
| `ge_coherent_receiver.py` | `ge_coherent_receiver.png` | Figure C4c, §C4c subsection 4 |
| `mechanical_scanning_limits.py` | `mechanical_scanning_limits.png` | Figure C4d, §C4d subsection 5 |
| `fmcw_tof_system_budget.py` | `fmcw_tof_system_budget.png` | Figure C7a, §C7a |
| `coherent_mode_coverage.py` | `coherent_mode_coverage_mesh.png`, `coherent_mode_coverage_scaling.png` | §C10.3b |
| `nuscenes_matching_localization.py` | `nuscenes_matching_localization.png` | Figure E11.1, §E11.1 |
| `truck_long_range_sensing.py` | `truck_long_range_sensing.png` | Figure E12, §E12 subsection 3 |
| `wavelength_eye_safety_background.py` | none (tables only) | the eye-safety and sunlight tables of §C4c |

## Requirements

- Python 3.10 or later (the figures were made with Python 3.13 from Anaconda).
- For the figure scripts: NumPy and Matplotlib; SciPy as well for `link_budget_scaling.py`. The plotting style (Arial, restrained palette) is written into each script, so no style file is needed.
- For the PDF: pandoc 3 (tested with 3.8), Google Chrome (run headless), and the Python packages `beautifulsoup4` and `pymupdf`. `build_pdf.py` runs `pandoc` and `chrome` from the PATH; set the environment variables `PANDOC` and `CHROME` to use other executables.

## How to rebuild

Run from the report folder:

```
python build/figures/link_budget_scaling.py    # redraw one figure; repeat for any other script
python build/build_pdf.py                      # rebuild the PDF (about 2 minutes)
python build/check_pdf.py                      # check the result
```

- **Where figure scripts write.** When a script sits in `build/figures/` inside the report folder, it writes its PNG, PDF and tables into `automotive_perception_report_figures/`. Anywhere else, for example after extraction from the PDF's attachments, it writes next to itself.
- **Input data.** `lidar_equity_hype_cycle.py` reads `lidar_equity_prices_weekly.csv` from its own folder, so keep the two together.
- **Determinism.** The only random draws are the Monte Carlo samples in `nuscenes_matching_localization.py`, which use a fixed seed (`default_rng(0)`). Rerunning any script therefore reproduces its figure and tables.

## How the PDF is built

`build_pdf.py` does the following:
1. It converts the Markdown to HTML with pandoc, rendering math as MathML and turning bare URLs into links.
2. It post-processes the HTML:
   - it turns each `\tag{N}` into a right-aligned equation number with an anchor;
   - it turns every "Eq. (N)" and every section reference ("§C7b", "§C0 subsection 4", "§C0 subsection 4.3") into an internal link;
   - it moves the table of contents after the title.
3. It prints the HTML to PDF with headless Chrome.
4. With PyMuPDF, it fixes the outline title and sets the metadata. It then embeds the figure scripts and the equity CSV as attachments, and adds a paperclip in the left margin beside each figure, holding the script that draws that figure.

Environment variables `REPORT_MD` and `REPORT_PDF` override the input and output paths for test builds. `KEEP_HTML=1` keeps the print HTML next to the PDF.

## Opening the attachments

- **Whole set:** open the PDF viewer's attachments panel (Adobe Acrobat and Reader, Firefox, SumatraPDF and most other viewers have one).
- **One figure:** click the paperclip beside that figure.
- **If a viewer refuses:** some viewers refuse to open `.py` attachments directly. Save them to disk first, then open them.
