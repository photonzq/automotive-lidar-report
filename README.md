# Automotive Night Vision, Lidar and the Sensor Debate

Technology routes, markets, supply chain, geopolitics and outlook.

- **Read online:** https://photonzq.github.io/automotive-lidar-report/
- **PDF:** [automotive_perception_report_2026-09-27.pdf](automotive_perception_report_2026-09-27.pdf) (about 40 MB; the scripts that draw the figures are attached inside the PDF)
- **Side note, *Short-Wave Infrared Image Sensors*:** https://photonzq.github.io/automotive-lidar-report/swir_image_sensor_survey.html and [swir_image_sensor_survey_2026-10-29.pdf](swir_image_sensor_survey_2026-10-29.pdf). It surveys SWIR cameras, explains why they are unlikely to matter for cars at this stage, and checks the detectivity reported in one recent paper.

This report was created with AI assistance. It may contain errors: each statement carries an evidence tag and, where possible, a source, so check those before relying on a figure.

## What is in this repository

| Path | Contents |
|---|---|
| `index.html` | The web version of the report; its figures load from `automotive_perception_report_figures/` |
| `automotive_perception_report_2026-09-27.md` | The source text (Markdown with LaTeX maths) |
| `automotive_perception_report_2026-09-27.pdf` | The compiled PDF |
| `automotive_perception_report_figures/` | The figures (PNG and PDF) and the numbers behind them (`*_tables.txt`) |
| `swir_image_sensor_survey_2026-10-29.md`, `swir_image_sensor_survey_2026-10-29.pdf`, `swir_image_sensor_survey.html` | The SWIR side note: source text, PDF and web version |
| `build/` | The build script (Markdown → HTML → PDF), its stylesheet and checks, and the figure scripts in `build/figures/` |
| `scripts_archive/` | Scripts used to research, check and edit the report, indexed in `scripts_archive/README.md` |
| `automotive_perception_report_addendum_2026-09-27.md`, `automotive_perception_report_reading_list_2026-09-28.md`, `automotive_perception_report_readability_review_2026-10-03.md`, `automotive_perception_report_2026-09-27.pre-audit.md` | An addendum, a reading list, a readability review of the scientific parts, and an earlier draft |

The paywalled press articles the report cites are not included; Appendix 2 lists them with links to the publishers' pages.

## Building

`build/build_pdf.py` turns the Markdown into HTML with pandoc (MathML for the equations), prints it to PDF with headless Chrome and attaches the figure scripts with PyMuPDF; `KEEP_HTML=1` also keeps the HTML, from which `scripts_archive/publish_2026-10/make_web_html.py` makes `index.html`. Given `swir_image_sensor_survey_2026-10-29.md` as an argument, both scripts build the side note instead, into `swir_image_sensor_survey_2026-10-29.pdf` and `swir_image_sensor_survey.html`; build the report first, because the side note's links to the report's sections take their targets from `index.html`. `build/build_pdf.py` runs `pandoc` and `chrome` from the PATH; set `PANDOC` and `CHROME` to use other executables. Each figure script in `build/figures/` runs on its own with Python 3, NumPy and Matplotlib.

## Licence

CC0 1.0 Universal (public-domain dedication); see [LICENSE](LICENSE).
