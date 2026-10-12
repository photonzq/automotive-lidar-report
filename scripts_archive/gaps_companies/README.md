# Scripts for the company open items (Appendix 1), `gaps_companies/`

Working scripts behind the 2026-10-03 research on the open company items in Appendix 1 (TetraVue, LeddarTech, peak market values, Chinese FMCW start-ups, technology bets, Insight LiDAR, Oryx). Downloaded raw data are not kept here.

| File | Purpose | Status |
|---|---|---|
| `uspto_assignment_search.py` | Searches the public USPTO Assignment Center by assignor or assignee name, patent number or reel/frame, and lists the patents in each recorded assignment. Source of the TetraVue (trustee to nLIGHT), LeddarTech (security interests only) and Baraja (no transfer out) assignment findings. | current |
| `item1_2_patent_assignment_scan.py` | Lists a company's patents and their assignment events from Google Patents pages. Full runs were blocked by rate limiting; superseded by `uspto_assignment_search.py`. | superseded |
| `item4_fetch_pages.py`, `item4_baidu_search.py` | Fetch and search pages for the registry status of 光勺 and 映讯芯光. | historical |
| `item5a_gpatents_fetch.py`, `item5a_gpatents_query.py` | Download Google Patents pages and run patent searches (Strobe, OURS). | historical |
| `item5b_fetch_uspto.py` | Downloads US patent and application PDFs from the USPTO print service and greps them. Also used for the OURS full texts. | current |
| `item5b_ocr_pdf.py`, `item5b_winocr.ps1` | Render image-only PDFs and OCR them with the Windows OCR engine. Also used for the OURS patents and the TetraVue assignment deeds. | current |
