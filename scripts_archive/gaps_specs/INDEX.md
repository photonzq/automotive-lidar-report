# gaps_specs scripts (Appendix 1, sensor and chip specifications)

All scripts read their output folder from the `GAPS_SPECS_RAW` environment variable (default: the current folder). None sends contact details to any service.

| File | Purpose | Status |
|---|---|---|
| `sony/digitize_isscc2021_pde.py` | Digitizes the PDE-vs-temperature and PDE-vs-wavelength curves of Sony ISSCC 2021 paper 7.3 (Fig. 7.3.4). Set `ISSCC21_PDF` to the paper. | current |
| `fmcw_rx/soa_wpe_105c_estimate.py` | [E] scaling of InP laser/SOA wall-plug efficiency to 105 degC from the hottest published anchors (1310 nm: 20 % at 75 degC; 1550 nm: 20 % at 50 degC) with characteristic temperatures T0/T1. | current |
| `common/hkex_docs.py` | Lists and downloads HKEXnews filings (prospectuses, annual reports) by stock code; used for Hesai (2525) and RoboSense (2498). | current |
| `common/pdf_keyword_pages.py` | Finds pages of long PDFs by regular expression and renders them to PNG for reading. | current |
| `common/download_render.py` | Downloads an open PDF and renders pages to PNG (certificate verification kept on). | current |
| `common/edgar_fts.py` | SEC EDGAR full-text search by CIK and phrase (generic User-Agent, no contact details). | current |
| `common/openalex_search.py` | OpenAlex work search with abstracts rebuilt from the inverted index. | current |
| `common/doi_meta.py` | Crossref and OpenAlex metadata, abstract and open-access status for DOIs. | current |
| `common/fetch_text.py` | Saves public web pages and prints their text, optionally around keywords. | current |
| `common/ieee_meta.py` | Attempted to read IEEE Xplore's public metadata block; Xplore answers scripted requests with a bot challenge, so it returns nothing. Kept only as a record. | non-working |
