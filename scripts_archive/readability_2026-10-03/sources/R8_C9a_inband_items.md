# Round 4 follow-up items: R8_C9a_inband (a source item that a Round 2 agent skipped)

## R8_C9a_inband-01

- **Where:** §C9a, "Check of the §C9 numbers", item 2, the bullet that begins "*In-band share* $f_{\rm band}$, the share of foreign units that my receive filter passes: 0.5–0.9."
- **Claim:** 9xx-nm units are ≈94–96% of Chinese installations (§C2), "but this report does not quantify their 905/940 nm split, so the range assumes my band holds half to most of them."
- **Needed:**
  1. The emission wavelength of each high-volume lidar installed in Chinese passenger cars in 2025 and H1 2026: at least Hesai ATX and AT128, the RoboSense M-platform units (M1, M1P, MX, M3) and EM4 or E-series, Huawei's 96- and 192-line units, Seyond Falcon and Robin, Zvision, Livox and any other unit with more than about 2% of installations. Take each wavelength from the product's datasheet, user manual, type-approval or homologation filing, or launch release; say which.
  2. The unit share of each product, from the installation data the report already uses (§B1 and §C2: ResearchInChina and Gasgoo supplier totals, with any per-product split the report or those sources give). Where a supplier ships products at two wavelengths, find the split or bound it.
  3. The resulting 905 nm / 940 nm / 1,550 nm shares of 2025 and H1 2026 installations, with the arithmetic shown.
  4. $f_{\rm band}$ for a victim at 905 nm and for one at 940 nm, given the receive filters the report assumes (10 nm at 940 nm, §C6(d) and §C4c; 20–40 nm at 905 nm, §C6(d)). Check whether any 905 nm filter in use is wide enough to pass 940 nm sources, or the reverse.
  5. Which wavelength §C9's "my" unit (a §C6-class SPAD-SoC scanner) should be taken at, as the report describes it.
- **Dependent numbers** (recompute them and say where else they are quoted; grep the report): in the same item 2, $F=f_{\rm ov}f_{\rm band}f_{\rm sd}$ ranges over 0.0625–0.54, and $1-(1-F\,p_1)^{n}$ with $p_1=4.17\times10^{-3}$ gives "about 0.08–3.5% of points carrying at least one foreign shot before rejection today ($n=3$ with $F=0.0625$, $n=16$ with $F=0.54$) and 0.26–6.5% later ($n=10$ and 30)". The item 2 heading quotes "today's 1.2–6.5% as much as the later 4–12%".
