# EU lidar funding trend, FP7 to Horizon Europe (renew_eu)

Scripts behind the CORDIS trend tables, the work-programme topic review and the defence-funding sweep of Oct 2026. Run them in the order below; each takes its input and output folders as arguments.

| File | Purpose | Status |
|---|---|---|
| `build_corpus.py` | Normalizes the CORDIS bulk JSON downloads (FP7, H2020, Horizon Europe; 84,787 projects) into one table. | current |
| `classify_trends.py` | Finds lidar-relevant projects by regex on title, objective and keywords; classifies relevance, role (hardware vs use), application, coherent/photonic-integrated/SPAD flags and programme type; writes the trend CSVs. Time-of-flight and depth terms count only with an active-ranging word, and the exclusion list uses word boundaries so that "electronic" no longer matches "electron". | current |
| `period_summary.py` | Sums by framework period and programme type; applies the manual 2023–2026 reading listed in the script. | current |
| `wp_topics.py` | Parses the Horizon Europe work-programme PDFs (Clusters 3–6, Research Infrastructures, 2021–2027) into a topic table with budgets and keyword counts. | current |
| `ft_search.py` | Pages through the Funding & Tenders portal search API for a free-text query (public portal key, no login). | current |
| `edf_factsheets.py` | Downloads the European Defence Fund project factsheets linked from the yearly results pages, validates the PDF header, paces requests, and greps them for lidar and laser-sensing terms. The Oct 2026 sweep was stopped before completion. | unfinished |
