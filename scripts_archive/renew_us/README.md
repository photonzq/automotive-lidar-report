# renew_us: US federal lidar funding (SBIR/STTR backbone and other channels)

Scripts behind the US federal funding numbers (proposed §D8). Downloaded data are not kept here; each script takes its data and output folders as arguments.

Main data sources:
- **SBIR.gov award file with abstracts:** `https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv`, Last-Modified 1 Oct 2026, 394.8 MB, 219,649 awards, FY1983 to FY2026 to date. The older copy at `https://data.www.sbir.gov/awarddatapublic/award_data.csv`, Last-Modified 1 Jan 2026, stops at FY2023 and is not used.
- **USAspending.gov:** Advanced Search transaction download (`POST /api/v2/download/transactions/`) with the keywords lidar, ladar and "laser radar", FY2008 to FY2026.
- **NSF Award Search API:** `https://api.nsf.gov/services/v1/awards.json`.
- **NASA TechPort project listing:** `https://techport.nasa.gov/api/projects/search`.
- **DARPA RDT&E justification books** on `comptroller.war.gov`.
- **Statutes, bills and reports** on govinfo.gov and house.gov, and the USGS 3DEP chart.

| File | Purpose | Status |
|---|---|---|
| `sbir_lidar_trends.py` | Selects lidar-relevant SBIR/STTR awards FY2005-FY2026 by keyword (match and core sets), flags coherent, photonic-integrated and single-photon subsets, classifies application and agency, and writes year, agency, application, recipient and borderline-pool tables. | current |
| `sbir_candidate_rules_draft.py` | First pass at the candidate rules, including the conditional rules (FMCW, OPA, Geiger-mode, SPAD/ToF, comb ranging, DIAL and others) intended for manual review. Stopped as too slow. | superseded |
| `usasp_lidar_download.py` | Requests, polls and unpacks the USAspending transaction download for a keyword set and fiscal-year window. | current |
| `usasp_lidar_analysis.py` | Removes false positives, flags SBIR/STTR (FPDS research codes) and Phase III, and classifies each transaction as R&D, data acquisition, equipment, services, research grant or transport grant. Also flags coherent and integrated subsets, and writes FY, agency, recipient, Phase III and FY2026 SBIR tables. | current |
| `nsf_lidar_awards.py` | NSF awards mentioning lidar. Classified by division and text into hardware, atmospheric/space science, geoscience/mapping, robotics/vision, other and SBIR/STTR; tables by start FY and period, with a list of hardware awards. | current |
| `nasa_techport_lidar.py` | TechPort projects mentioning lidar, classified by programme, application (landing and navigation, Earth atmosphere, altimetry and vegetation, and others) and technology; counts by start year. | current |
| `dod_darpa_jbook_scan.py` | DARPA justification books FY2014-FY2027: lidar mention counts per book, plus the SWEEPER, DODOS, MOABB and LUMOS amounts read from rendered pages. | current |
| `policy_grep_pdfs.py` | Locates lidar wording in statute, bill, report and budget PDFs and renders the hit pages to PNG. | current |
| `civil_3dep_table.py` | USGS 3DEP expenditures FY2015-FY2024 by source, transcribed from the USGS chart. | current |
| `policy_signals_table.py` | The sourced table of 2024-2026 policy signals. | current |
| `renew_us_period_summaries.py` | Period averages across the USAspending, NSF and TechPort outputs, and the ESTO lidar project list. | current |
