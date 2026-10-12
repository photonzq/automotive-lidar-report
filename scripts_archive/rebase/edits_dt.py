r"""SPAD dead time on the signal: the bright-sun live fraction 0.804 (6 ns, state of the art)
multiplies the SPAD signal efficiency, 0.5 x 0.37 x 0.804 = 0.149.  Written against the current
report (report_after_fix2.md numbering)."""

E = []

# =============================================================== executive summary
E.append(("S", "     - At 200 m and 10% reflectivity, the modelled electrical energy per point is ≈4.3 µJ",
          r"against ≈0.44 µJ for 940 nm SPAD ToF. That is ≈10×, since $4.25/0.436\approx9.8$ (≈5× in an optimistic 2032 case).",
          r"against ≈0.53 µJ for 940 nm SPAD ToF, whose SPADs lose ≈20% of the signal to their 6 ns dead time in bright sun. That is ≈8×, since $4.25/0.525\approx8.1$ (≈4× in an optimistic 2032 case)."))

# =============================================================== §C0 subsection 10 intro
E.append(("S", "- **Equal apertures, constant gap** (10.5).", "FMCW needs about three times the energy per sample of SPAD ToF",
          "FMCW needs about 2.5 times the energy per sample of SPAD ToF"))
E.append(("S", "- **A smaller aperture buys the margin back with energy** (10.6).", "i.e. twenty times ToF's.", "i.e. sixteen times ToF's."))

# =============================================================== §C0 10.3
E.append(("S", "  - Over the 20.8 µs a point listens, the same rate gives", "the event count of the §C7a electronics budget.",
r"""the event count of the §C7a electronics budget.
  - The dead time blinds the SPADs to signal photons as well: only the live fraction 0.804 of the echo can be counted, so the §C7a model multiplies the SPAD's signal efficiency by it, $0.5\times0.37\times0.804=0.149$."""))
E.append(("S", "- **ToF:** the model's 25 counts are 1.36× the 18.4 that an ideal counter needs in bright sun.",
          "The margin covers a return spread over two or three bins, dead time and pile-up (§C6).",
          "The dead time is not part of this margin, because it is counted in the SPAD's efficiency (the live fraction above, §C7a(a)). The margin covers a return spread over about two bins, which needs 22.3 counts summed over both (×1.21), and pile-up distortion (§C6)."))

# =============================================================== §C0 10.4
E.append(("X", r"| SPAD dToF, bright sun | 940 nm | 25 | 0.185 | 0.1 µJ (e.g. ≈10 shots of 10 nJ) | $2.9\times10^{-10}$ | 95.4 dB |",
          r"| SPAD dToF, bright sun | 940 nm | 25 | 0.149 | 0.1 µJ (e.g. ≈10 shots of 10 nJ) | $3.6\times10^{-10}$ | 94.5 dB |"))
E.append(("X", "  - SPAD: optics 0.5 × photon detection efficiency 0.37;",
          "  - SPAD: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction 0.804 (6 ns dead time, 10.3);"))
E.append(("S", "- **Worked (SPAD),** from Eq. (41):",
          r"$25\times2.11\times10^{-19}/(0.185\times10^{-7})=2.86\times10^{-10}$, and $-10\log_{10}(2.86\times10^{-10})=95.4$ dB.",
          r"$25\times2.11\times10^{-19}/(0.149\times10^{-7})=3.55\times10^{-10}$, and $-10\log_{10}(3.55\times10^{-10})=94.5$ dB."))
E.append(("L", "  - SPAD case, $D=25$ mm:",
          r"  - SPAD case, $D=25$ mm: $0.0125\times\sqrt{0.1/3.55\times10^{-10}}=210$ m, or 206 m with clear air. The 10 and 50 mm lenses reach 83 and 405 m."))
E.append(("L", "  - The APD case reaches 326 m with 25 mm.",
          r"  - The APD case reaches 326 m with 25 mm. Its per-point need $n_{\rm req}E_{\rm ph}/\eta$ is 8× the SPAD's, but its 20× larger energy leaves a 2.5× margin, i.e. $\sqrt{2.5}=1.6\times$ the range."))

# =============================================================== §C0 10.5
E.append(("S", "$$\\frac{E_{\\rm FMCW}}{E_{\\rm SPAD}}=",
          r"=0.54\times\frac{1}{t^2(0.45)^2}=0.54\times5.9=3.2 .", r"=0.43\times\frac{1}{t^2(0.45)^2}=0.43\times5.9=2.6 ."))
E.append(("L", "  - The first factor is $(30\\times1.28",
          r"  - The first factor is $(30\times1.28\times10^{-19}/0.25)/(25\times2.11\times10^{-19}/0.149)=1.54\times10^{-17}/3.54\times10^{-17}=0.43$."))
E.append(("X", "  - With clear-air loss the ratio is 3.1 at 100–500 m.", "  - With clear-air loss the ratio is 2.5 at 100–500 m."))
E.append(("S", "- **Against a fixed 25 mm SPAD receiver**,", "8.1× at 100 m, 4.0× at 200 m, 2.6× at 300 m and 1.6× at 500 m.",
          "6.5× at 100 m, 3.2× at 200 m, 2.1× at 300 m and 1.3× at 500 m."))
E.append(("L", "- **Linear APD against SPAD with the same lens:**",
          r"- **Linear APD against SPAD with the same lens:** $(890\times1.28\times10^{-19}/0.40)/(25\times2.11\times10^{-19}/0.149)=8.0$. That is eight times the energy per point at every range, which the 1,550 nm eye-safety limits can pay for at low point rates (§C4c)."))

# =============================================================== §C0 10.6 and 10.7
E.append(("L", "- **SPAD ToF at 940 nm with a 25 mm lens** needs 76 nJ per point",
          r"- **SPAD ToF at 940 nm with a 25 mm lens** needs 94 nJ per point: the 0.1 µJ of 10.4, which reaches 206 m, scaled by $(200/206)^2=0.94$. Without the 0.15 dB of clear-air loss this is the ≈91 nJ of §C7b subsection 1."))
E.append(("S", "| SPAD ToF, 940 nm, 25 mm lens | — |", "| 76 nJ (0.25×) |", "| 94 nJ (0.31×) |"))
E.append(("S", "- **In fog** (below 500 m visibility)", "at twenty times its energy.", "at sixteen times its energy."))
E.append(("S", "  - A 7 mm aperture matches ToF's tolerance of dark targets and fog.", "twenty times ToF's 76 nJ.", "sixteen times ToF's 94 nJ."))
E.append(("S", "- **Photons, ToF.** Per shot the SPAD design emits 7.6 nJ (its 76 nJ over ten shots).",
          r"Per shot the SPAD design emits 7.6 nJ (its 76 nJ over ten shots). The sign at 5 m then returns about $3.5\times10^{8}$ photons, $6.5\times10^{7}$ of them detected,",
          r"Per shot the SPAD design emits 9.4 nJ (its 94 nJ over ten shots). The sign at 5 m then returns about $4.3\times10^{8}$ photons, $6.4\times10^{7}$ of them detected,"))

# =============================================================== §C3a and technology table
E.append(("S", "| **Mobileye / Intel** (ended Sep 2024) |", "(FMCW ≈4.3 µJ vs ToF ≈0.44 µJ per point at 200 m, §C7a)",
          "(FMCW ≈4.3 µJ vs ToF ≈0.53 µJ per point at 200 m, §C7a)"))
E.append(("S", "| **Coherent (FMCW) scanners** | Aurora's driverless trucks", "energy per point ≈10× that of SPAD ToF (§C7a)",
          "energy per point ≈8× that of SPAD ToF (§C7a)"))

# =============================================================== §C6(d)
E.append(("S", "- **In the ToF energy model.** The §C7a model and the detection statistics of §C0 subsection 10.3",
          "and 20% for the model's central case of half that background.",
          r"and 20% for the model's central case of half that background. The same live fraction multiplies the signal, because a SPAD that is dead when the echo arrives misses it; the §C7a model therefore uses a signal efficiency of $0.5\times0.37\times0.804=0.149$ in bright sun."))

# =============================================================== §C7a
E.append(("S", "  - The model below gives about **10×** more electrical energy per point than 940 nm SPAD ToF",
          r"about **10×** more electrical energy per point than 940 nm SPAD ToF in 2026 ($4.25/0.436\approx9.8$). This narrows to about **5×** in an optimistic 2032 projection ($1.48/0.286\approx5.2$; totals from the §3 table).",
          r"about **8×** more electrical energy per point than 940 nm SPAD ToF in 2026 ($4.25/0.525\approx8.1$). This narrows to about **4×** in an optimistic 2032 projection ($1.48/0.357\approx4.1$; totals from the §3 table)."))
E.append(("S", "  - The model below gives about **8×** more electrical energy per point than 940 nm SPAD ToF",
          "the 2026 gap is ≈12–15× for a discrete fibre chain and ≈25× for an integrated array.",
          "the 2026 gap is ≈10–13× for a discrete fibre chain and ≈21× for an integrated array."))
E.append(("X", "**(a) Optical energy per point: ≈73 nJ for ToF against ≈0.30 µJ for FMCW.**",
          "**(a) Optical energy per point: ≈91 nJ for ToF against ≈0.30 µJ for FMCW.**"))
E.append(("S", "- **Shot-noise-limited LO.** The coherent receiver is limited by the LO's shot noise",
          "so the FMCW optical energy would rise somewhat when hot.",
          "so the FMCW optical energy would rise somewhat when hot.\n"
          "- **SPAD dead time 6 ns**, the state of the art: Sony's IMX479 specifies \"approx. 6 ns\" with 3×3 SPADs per macro-pixel, and its IMX459 predecessor measured 6 ns, a 60 Mcps count-rate ceiling and 0.1% afterpulsing [P]. In bright sun each SPAD is dead 19.6% of the time (§C0 subsection 10.3), and a SPAD that is dead when the echo arrives misses it, so the live fraction 0.804 multiplies the signal efficiency as well as the background."))
E.append(("S", "- **ToF:** $A_{\\rm eff}=A_{\\rm rx}$ is the whole 25 mm receive aperture (491 mm²)",
          r"At 940 nm and 37% PDE (photon detection efficiency of the SPAD) the result is **≈73 nJ** (58–102). With $n_{\rm req}=25$ (central), $E_{\rm ph}=2.11\times10^{-19}$ J, $\pi R^2=\pi\times200^2=1.26\times10^{5}$ m², $\rho=0.1$ and $\eta=0.5\times0.37=0.185$ (optics transmission 0.5 × PDE): $E_{\rm opt}=25\times2.11\times10^{-19}\times1.26\times10^{5}/(0.1\times4.91\times10^{-4}\times0.185)=6.64\times10^{-13}/(9.08\times10^{-6})\approx7.3\times10^{-8}$ J. The energy scales linearly with $n_{\rm req}$: 20 counts give 58 nJ and 35 give 102 nJ.",
          r"At 940 nm, 37% PDE (photon detection efficiency of the SPAD) and the bright-sun live fraction of 0.804 the result is **≈91 nJ** (58–152). With $n_{\rm req}=25$ (central), $E_{\rm ph}=2.11\times10^{-19}$ J, $\pi R^2=\pi\times200^2=1.26\times10^{5}$ m², $\rho=0.1$ and $\eta=0.5\times0.37\times0.804=0.149$ (optics transmission × PDE × live fraction): $E_{\rm opt}=25\times2.11\times10^{-19}\times1.26\times10^{5}/(0.1\times4.91\times10^{-4}\times0.149)=6.64\times10^{-13}/(7.30\times10^{-6})\approx9.1\times10^{-8}$ J. The low case is night (20 counts, no dead time, $\eta=0.185$): 58 nJ. The high case is the fully sunlit scene (35 counts, live fraction 0.672, $\eta=0.124$): 152 nJ."))
E.append(("S", "  - **Measured efficiencies are lower.**", "(12–15× ToF), or to ≈11 µJ (≈25×).", "(10–13× ToF), or to ≈11 µJ (≈21×)."))
E.append(("X", "FMCW therefore needs ≈4× more optical energy per point than ToF (0.30 µJ against 73 nJ). The ≈4× ratio splits into four factors:",
          "FMCW therefore needs ≈3.3× more optical energy per point than ToF (0.30 µJ against 91 nJ). The ≈3.3× ratio splits into four factors:"))
E.append(("X", "- efficiency (0.74×), ToF's 0.185 against FMCW's 0.25.",
          "- efficiency (0.60×), ToF's 0.149, which includes the SPADs' dead time in bright sun, against FMCW's 0.25."))
E.append(("S", "- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m", "against ≈8–9 W for a 520-line ToF unit",
          "against ≈10 W for a 520-line ToF unit"))
E.append(("S", "- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m",
          r"The ToF unit is $3\ {\rm W}+1.25\times10^{7}\times0.436\ \mu{\rm J}\approx8.5$ W.",
          r"The ToF unit is $3\ {\rm W}+1.25\times10^{7}\times0.525\ \mu{\rm J}\approx9.6$ W."))
E.append(("S", "This table collects the budget of §2 for a 200 m, 10%-reflectance target.",
          "FMCW needs about 10× ToF's electrical energy per point in 2026 and about 5× in the optimistic 2032 case",
          "FMCW needs about 8× ToF's electrical energy per point in 2026 and about 4× in the optimistic 2032 case"))
E.append(("X", "| Optical energy per point | 73 nJ | 0.30 µJ | 60 nJ | 0.19 µJ |", "| Optical energy per point | 91 nJ | 0.30 µJ | 78 nJ | 0.19 µJ |"))
E.append(("X", "| Laser/SOA electrical energy | 0.37 µJ | 2.0 µJ | 0.24 µJ | 0.86 µJ |", "| Laser/SOA electrical energy | 0.45 µJ | 2.0 µJ | 0.31 µJ | 0.86 µJ |"))
E.append(("X", "| **Total per point** | **0.44 µJ** | **4.25 µJ** | **0.29 µJ** | **1.48 µJ** |",
          "| **Total per point** | **0.53 µJ** | **4.25 µJ** | **0.36 µJ** | **1.48 µJ** |"))
E.append(("X", "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 7.4 W | 46 W | 5.9 W | 18 W |",
          "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 8.3 W | 46 W | 6.6 W | 18 W |"))
E.append(("X", "| Sensor power at 25 Mpts/s | 14 W | 109 W | 10 W | 40 W |", "| Sensor power at 25 Mpts/s | 16 W | 109 W | 12 W | 40 W |"))
E.append(("S", "- All entries are the central cases of the companion script. **Optical energy** uses",
          r"ToF 2026 is 73 nJ and FMCW 2026 0.30 µJ (worked in §2(a)). ToF 2032 raises PDE from 0.37 to 0.45, giving $73\times0.37/0.45=60$ nJ;",
          r"ToF 2026 is 91 nJ and FMCW 2026 0.30 µJ (worked in §2(a)). ToF 2032 raises PDE from 0.37 to 0.45, which also raises the sunlight counted and the dead fraction (22.9%, live fraction 0.771), giving $91\times(0.37\times0.804)/(0.45\times0.771)=78$ nJ;"))
E.append(("S", "- **Laser/SOA electrical energy** is $E_{\\rm opt}/\\eta_{\\rm wp}$",
          r"$73\ {\rm nJ}/0.20=0.37$ µJ", r"$91\ {\rm nJ}/0.20=0.45$ µJ"))
E.append(("S", "- **Laser/SOA electrical energy** is $E_{\\rm opt}/\\eta_{\\rm wp}$",
          r"$60\ {\rm nJ}/0.25=0.24$ µJ", r"$78\ {\rm nJ}/0.25=0.31$ µJ"))
E.append(("S", "- **Sensor power** is $3\\ {\\rm W}+\\dot N E_{\\rm total}$",
          r"ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.436\times10^{-6}=7.4$ W.",
          r"ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.525\times10^{-6}=8.3$ W."))
E.append(("S", "The 2032 FMCW column assumes efficiency $\\eta=0.4$ and 22% wall-plug;", "The residual ≈5× gap", "The residual ≈4× gap"))
E.append(("S", "Sources: https://arxiv.org/pdf/2502.09736 ; https://www.nature.com/articles/s41586-026-10183-6 ; https://arxiv.org/pdf/2008.02411",
          "https://optics.org/news/yole-trims-automotive-lidar-expectations-as-prices-drop",
          "https://optics.org/news/yole-trims-automotive-lidar-expectations-as-prices-drop ; https://www.sony-semicon.com/en/products/is/automotive/tof.html ; https://doi.org/10.11470/jsaprev.230402"))

# =============================================================== §C7b
E.append(("S", "- **Per joule of emitted light, FMCW buys ≈4× fewer sampled points than 940 nm SPAD ToF.",
          "FMCW buys ≈4× fewer sampled points", "FMCW buys ≈3.3× fewer sampled points"))
E.append(("L", "  - The result is ≈0.30 µJ per FMCW sample against ≈73 nJ per ToF point",
          "  - The result is ≈0.30 µJ per FMCW sample against ≈91 nJ per ToF point (200 m, 10% target). One FMCW sample covers only a small part of a 0.05° angular cell. To cover the whole cell, FMCW needs ≈15 µJ, about 160× more."))
E.append(("S", "This subsection asks how much emitted light each lidar architecture needs to measure one point at 200 m",
          "A 940 nm SPAD time-of-flight sensor needs ≈73 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, about 4× more.",
          "A 940 nm SPAD time-of-flight sensor needs ≈91 nJ per point; a 1,550 nm FMCW sensor needs ≈0.30 µJ per sample, about 3.3× more."))
E.append(("X", r"  - SPAD ToF: $73\ {\rm nJ}\times15\times10^{6}\ {\rm s^{-1}}=1.1$ W;",
          r"  - SPAD ToF: $91\ {\rm nJ}\times15\times10^{6}\ {\rm s^{-1}}=1.4$ W;"))
E.append(("X", r"| 940 nm SPAD or SiPM dToF, scanned or line-flash, 25 mm lens | 491 mm² (whole lens) | 25 counts | 0.185 | 73 nJ | $1.4\times10^{7}$ |",
          r"| 940 nm SPAD or SiPM dToF, scanned or line-flash, 25 mm lens | 491 mm² (whole lens) | 25 counts | 0.149 | 91 nJ | $1.1\times10^{7}$ |"))
E.append(("S", "- **Energy column:** Eq. (96),", r"(0.1\times4.91\times10^{-4}\times0.185)=7.3\times10^{-8}$ J.",
          r"(0.1\times4.91\times10^{-4}\times0.149)=9.1\times10^{-8}$ J."))
E.append(("X", "  - ToF: optics 0.5 × photon detection efficiency 0.37;",
          "  - ToF: optics 0.5 × photon detection efficiency 0.37 × the bright-sun live fraction 0.804 (6 ns dead time, §C7a(a));"))
E.append(("S", "- **Last column:** $1/E_{\\rm opt}$;", r"$1/(7.3\times10^{-8}\ {\rm J})=1.4\times10^{7}$", r"$1/(9.1\times10^{-8}\ {\rm J})=1.1\times10^{7}$"))
E.append(("S", "- **The FMCW efficiency is a design value.**",
          "so FMCW buys 6–9× (discrete fibre chain) or ≈18× (integrated array) fewer points per optical joule than SPAD ToF, instead of ≈4×.",
          "so FMCW buys 5–7.5× (discrete fibre chain) or ≈15× (integrated array) fewer points per optical joule than SPAD ToF, instead of ≈3.3×."))
E.append(("S", "**(d) Why FMCW buys ≈4× fewer sampled points per joule than SPAD ToF.**",
          "**(d) Why FMCW buys ≈4× fewer sampled points per joule than SPAD ToF.**",
          "**(d) Why FMCW buys ≈3.3× fewer sampled points per joule than SPAD ToF.**"))
E.append(("S", "**(d) Why FMCW buys ≈3.3× fewer sampled points per joule than SPAD ToF.**",
          "the optical energy per SPAD ToF point (73 nJ)", "the optical energy per SPAD ToF point (91 nJ)"))
E.append(("S", "$$\\frac{E_{\\rm FMCW}}{E_{\\rm ToF}}=\\underbrace{\\frac{491}{255}}_{\\rm collection}",
          r"\underbrace{\frac{0.185}{0.25}}_{\rm efficiency}=1.93\times4.8\times0.61\times0.74=4.15.",
          r"\underbrace{\frac{0.149}{0.25}}_{\rm efficiency}=1.93\times4.8\times0.607\times0.596\approx3.3."))
E.append(("X", "- **Efficiency (0.74×):** the FMCW model's $\\eta=0.25$ is higher than the ToF model's 0.185, which also helps FMCW.",
          "- **Efficiency (0.60×):** the FMCW model's $\\eta=0.25$ is higher than the ToF model's 0.149, the SPADs' optics × PDE × live fraction in bright sun, which also helps FMCW."))
E.append(("X", r"- **Per fully covered cell the gap is ≈200×** ($14.6\ \mu{\rm J}/73\ {\rm nJ}$).",
          r"- **Per fully covered cell the gap is ≈160×** ($14.6\ \mu{\rm J}/91\ {\rm nJ}$)."))
E.append(("S", "- **Direct detection:** from Eq. (96) with a fixed lens,", r"$73\ {\rm nJ}\times(10/200)^2=0.18$ nJ per point at 10 m",
          r"$91\ {\rm nJ}\times(10/200)^2=0.23$ nJ per point at 10 m"))
E.append(("S", "- **Against ToF, FMCW's photon handicap shrinks with range.**",
          r"$73\ {\rm nJ}\times(300/200)^2\times10^{7}=1.6$ W of useful light at 300 m with a fixed 25 mm lens. The FMCW-to-ToF photon ratio therefore falls from $0.30/0.073=4.1$ at 200 m to $4.5/1.6=2.7$ at 300 m,",
          r"$91\ {\rm nJ}\times(300/200)^2\times10^{7}=2.0$ W of useful light at 300 m with a fixed 25 mm lens. The FMCW-to-ToF photon ratio therefore falls from $0.30/0.091=3.3$ at 200 m to $4.5/2.0=2.2$ at 300 m,"))
E.append(("S", "This subsection turns the dwell of subsection 2 into the number of parallel coherent channels",
          "against ≈21 mW per ToF channel.", "against ≈25 mW per ToF channel."))
E.append(("S", "- **Power per ToF channel.** At the §C7a central values", "and ≈0.37 µJ of laser electrical energy per ToF point",
          "and ≈0.45 µJ of laser electrical energy per ToF point"))
E.append(("X", r"  - laser: $15\times10^{6}\times0.37\ \mu{\rm J}=5.6$ W, i.e. ≈18 mW per macro-pixel.",
          r"  - laser: $15\times10^{6}\times0.45\ \mu{\rm J}=6.8$ W, i.e. ≈22 mW per macro-pixel."))
E.append(("X", "- **So the per-channel electrical power is ≈376 mW for FMCW against ≈21 mW for ToF, ≈18× more.** The FMCW channel is also far larger and costlier.",
          "- **So the per-channel electrical power is ≈376 mW for FMCW against ≈25 mW for ToF, ≈15× more.** The FMCW channel is also far larger and costlier."))
E.append(("S", "  - At 15 Mpts/s that is $15\\times10^{6}\\times2.23\\times10^{-6}=33.4$ W of receiver electronics",
          "about four times a whole 520-line ToF unit (≈8.5 W in the §C7a model).",
          "about 3.5 times a whole 520-line ToF unit (≈9.6 W in the §C7a model)."))

# =============================================================== §D
E.append(("S", "   - §C7a shows that FMCW costs ≈10× the electrical energy per point.", "FMCW costs ≈10× the electrical energy per point.",
          "FMCW costs ≈8× the electrical energy per point."))
