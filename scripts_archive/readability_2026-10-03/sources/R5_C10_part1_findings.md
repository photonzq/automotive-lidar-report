# Round 4 source findings: R5_C10_part1

Report checked: `automotive_perception_report_2026-09-27.md`, sha256 prefix 2b959bd85367 (the version on disk when this file was checked on 5 Oct 2026; other editing passes were changing the report while it was written, from 51d60fa27199 onwards). Every `old` string below was copied verbatim from the report and occurs exactly once in that version (checked with `scripts/R6_check_old_strings.py` and `scripts/R4_check_old_strings.py`: 23 blocks, all 1×, no overlaps, no e-mail addresses, no versioning words in `new` blocks).

Scripts used (all in `scripts/`, one line each in `scripts/INDEX.md`): `R5_pdf_tools.py` (download, locate, render), `R5_sparse_array_mc.py` (items 02 and 03), `R5_mc_rerun_check.py` (item 03, the 20-trial block alone). Primary PDFs were rendered at 160 dpi and read as images; `get_text()` was used only to locate pages.

## R5_C10_part1-01

- **Question:** Which device, range and reflectance lie behind the 1,360 nJ in Pointcloud's comparison table, and what does that value scale to at 200 m on a 10% target?
- **Answer:** In Extended Data Table 1 of Settembrini *et al.* (*Nature* 2026) the 1,360 nJ belongs to the table's Ref. [19], which is Li, Y. *et al.*, "Wide-steering-angle high-resolution optical phased array", *Photonics Res.* 9, 2511–2518 (2021). That is Jilin University's 128-channel SiN-on-SOI OPA; the table row reads 128 ch, 140° × 19.3°, 0.05° × 0.05°, 100 m, 1,360 nJ, no transmit/receive integration, no CMOS integration. Li *et al.* measured FMCW range from 5 to 100 m on a 90% reflectivity scatter plate. Beyond 50 m the optical path was folded with a silver mirror. The fishbone-grating OPA transmitted and a fibre collimator received, with 26 dBm into the transmitter; at 100 m, 116 repeated measurements had a 3.38 cm absolute error. The value is therefore not a 35 m, 10% measurement.
  - The table's "energy" is per pulse or per up-and-down chirp pair (its Methods, "Performance comparison"). A consistency check [E]: 26 dBm is 398 mW; the paper's system insertion loss is 16.97 dB (fishbone) or 17.7 dB (chain), leaving 8.0 or 6.8 mW; the chirp is 3 GHz at 30 THz/s, i.e. 100 µs per ramp and 200 µs per up-and-down pair. Then $6.8\ {\rm mW}\times200\ \mu{\rm s}=1.35\ \mu{\rm J}$ and $8.0\ {\rm mW}\times200\ \mu{\rm s}=1.60\ \mu{\rm J}$; the table's 1,360 nJ matches the 17.7 dB case.
  - Scaling to 200 m at 10% with the return of an extended diffuse target proportional to $\rho/R^2$, the energy needed scales as $R^2/\rho$:
    - Li *et al.*: $E=1.36\ \mu{\rm J}\times(200/100)^2\times(0.9/0.1)=1.36\ \mu{\rm J}\times4\times9=49\ \mu{\rm J}$.
    - 8,192 elements (35 m, 10%): $E=1.7\ \mu{\rm J}\times(200/35)^2=1.7\ \mu{\rm J}\times32.65=55.5\approx56\ \mu{\rm J}$.
    - So the range is ≈49–56 µJ, not ≈44–56 µJ.
  - At 12 Mpts/s: $49\ \mu{\rm J}\times12\times10^{6}\ {\rm s^{-1}}=588\approx590$ W and $56\ \mu{\rm J}\times12\times10^{6}\ {\rm s^{-1}}=670$ W. Against the FS-4S's 35 W: $590/35=16.8\approx17$ and $670/35=19.1\approx19$. Against the Hesai ATX's 8 W: $590/8=74$ and $670/8=84$.
  - The comparison with the link budget still reads "at or just below the low end" of 54–157 µJ (49 is below 54, 56 is at it).
- **Source:**
  - Settembrini, F. F. *et al.* (Pointcloud), "A large-scale coherent 4D imaging sensor", *Nature* (2026), doi:10.1038/s41586-026-10183-6: Extended Data Table 1 "Comparison table" (PDF p. 16), reference list (PDF p. 6, ref. 19), Methods "Performance comparison" (PDF p. 9). Full PDF read (open access, nature.com).
  - Li, Y. *et al.*, *Photonics Res.* 9, 2511–2518 (2021), doi:10.1364/PRJ.437846: §3A (loss list: system insertion loss 17.7 dB chain, 16.97 dB fishbone), §3B "FMCW Ranging Performance" (90% scatter plate, 5–100 m, mirror fold beyond 50 m, 26 dBm, 30 THz/s, 3 GHz), Figs. 7–8. Full text read on Optica's open-access HTML page.
- **Evidence tag:** [S] for the 1,360 nJ (Pointcloud's table); [P] for the device's range, target and loss (the device paper itself, as the §C10.2b table tags device papers).
- **Confidence:** high — reference number, table row and the paper's ranging conditions agree, and the energy cross-check matches to 1%.
- **Proposed edit:**
  - `old`:
    ```text
    - Optical energy per point for OPA lidars is 1,360–1,700 nJ, the upper value being the 8,192-element array's at 35 m on a 10% target. Pointcloud's FPA uses 46 nJ (at 65 m and 30%), and the 512-pixel coherent receiver array of Rogers et al. (*Nature* 2021, §C10.4) 212 nJ. All four values come from Pointcloud's comparison table [S].
    ```
  - `new`:
    ```text
    - Optical energy per point for OPA lidars is 1,360–1,700 nJ in Pointcloud's comparison table [S]. The 1,360 nJ is that of Jilin University's 128-channel OPA (Li *et al.*, *Photon. Res.* 2021) at 100 m on a 90% target, and the 1,700 nJ that of the 8,192-element array at 35 m on a 10% target. The table counts energy per pulse or per up-and-down chirp pair, and Li *et al.*'s 26 dBm input, less its 17.7 dB system insertion loss, over $2\times100$ µs of chirp gives the same figure [E: $398\ {\rm mW}\times10^{-1.77}=6.8$ mW and $6.8\ {\rm mW}\times200\ \mu{\rm s}=1.35\ \mu{\rm J}$]. Pointcloud's FPA uses 46 nJ (at 65 m and 30%), and the 512-pixel coherent receiver array of Rogers et al. (*Nature* 2021, §C10.4) 212 nJ, from the same table [S].
    ```
  - `old`:
    ```text
    - Scaling the measured energy per point as $R^2$ (the return from an extended target falls as $1/R^2$) from 35 m to 200 m at 10% gives ≈44–56 µJ per point [E: $(200/35)^2=32.7$, and $1.36\ \mu{\rm J}\times32.7=44\ \mu{\rm J}$, $1.7\ \mu{\rm J}\times32.7=56\ \mu{\rm J}$].
    ```
  - `new`:
    ```text
    - Scaling each measured energy per point to 200 m at 10% as $R^2/\rho$ (the return from an extended diffuse target is proportional to $\rho/R^2$, with $\rho$ the reflectance) gives ≈49–56 µJ per point [E: $1.36\ \mu{\rm J}\times(200/100)^2\times(0.9/0.1)=1.36\ \mu{\rm J}\times36=49\ \mu{\rm J}$ and $1.7\ \mu{\rm J}\times(200/35)^2=1.7\ \mu{\rm J}\times32.7=56\ \mu{\rm J}$].
    ```
  - `old`:
    ```text
    - At 12 Mpts/s this is about 530–670 W of optical power ($44\ \mu{\rm J}\times12\times10^{6}\ {\rm s^{-1}}=530$ W, $56\ \mu{\rm J}\times12\times10^{6}\ {\rm s^{-1}}=670$ W). That is 15–19 times the 35 W that the whole FS-4S module draws and 66–84 times the 8 W of the Hesai ATX (table below)
    ```
  - `new`:
    ```text
    - At 12 Mpts/s this is about 590–670 W of optical power ($49\ \mu{\rm J}\times12\times10^{6}\ {\rm s^{-1}}=590$ W, $56\ \mu{\rm J}\times12\times10^{6}\ {\rm s^{-1}}=670$ W). That is 17–19 times the 35 W that the whole FS-4S module draws and 74–84 times the 8 W of the Hesai ATX (table below)
    ```
- **Appendix 2 entry:** - Li Y. *et al.*, 128-channel 140° SiN-on-SOI OPA with 100 m FMCW ranging on a 90% target, *Photon. Res.* 9, 2511 (2021): https://opg.optica.org/prj/fulltext.cfm?uri=prj-9-12-2511

## R5_C10_part1-02

- **Question:** What geometry, element pattern and field lie behind DTU's simulated 0.8% main-lobe fraction, what does $N/N_{\rm spot}$ predict for it, and does the camera explain the measured 3–6 dB floor?
- **Answer:**
  - **Geometry.** The array is one-dimensional along the phase-steered axis. It is a single aperiodic row of 120 shallow-etched grating emitters with a mean pitch of about 50 µm across 6 mm. Each grating is 5 mm long and steers the other axis by wavelength (13.7° over 1,480–1,572 nm). The "6 × 5 mm" aperture is therefore 6 mm of sparse array by 5 mm of grating length.
  - **Element pattern and field.** The simulated element factor of one grating (0.45 µm wide, 0.7 µm period, duty cycle 0.1, 10 nm etch) is nearly flat over ±80° (paper Fig. 2). The paper then sets the element factor aside and computes the array factor alone over the 180° field (Fig. 4b).
  - **Main-lobe power.** Its theory gives 13% for a 0.37 mm aperture and 13%/16.3 ≈ 0.8% for 6 mm (Fig. 3a, text).
  - **$N/N_{\rm spot}$ [E].** Both values match $N/N_{\rm spot}$ when spots are counted in angle with a flat pattern over ±90°: $N_{\rm spot}=\pi D/\lambda=\pi\times6\ {\rm mm}/1.55\ \mu{\rm m}=12{,}161$, close to the paper's "≈12,000 resolvable points in simulation". Then $N/N_{\rm spot}=120/12{,}161=0.99\%$, and about 90% of a uniform aperture's main lobe lies inside its first nulls, giving ≈0.9%. For 0.37 mm, $N_{\rm spot}=750$ and $N/N_{\rm spot}=16\%$, i.e. ≈13% after the same factors. Counting in sine space instead ($N_{\rm spot}=2D/\lambda=7{,}742$) would give 1.4%.
  - **Monte Carlo [E].** `R5_sparse_array_mc.py` (Part B) puts 120 random emitters over 6 mm and gets 0.88% with power uniform in angle and 1.38% uniform in $\sin\theta$.
  - **Measured floor.** The paper reports a measured GLSR (main lobe to highest "grating-lobe noise") of 3–6 dB, against 12.8 dB simulated. It attributes the difference to amplitude variation of its cascaded directional couplers [P].
  - **Camera effect [E].** The camera's 0.13° response is about 9 main-lobe widths ($\lambda/D=0.015^\circ$). It spreads the main lobe and reads its peak about 9.5–10 dB low, while it leaves the floor at its mean, $1/N$ of the true peak (−21 dB). The observed peak should then stand about 11 dB above the mean floor, and the floor's highest points about 5.6 dB above that mean.
  - **Simulation [E].** Part C of the same script (120 random emitters over 6 mm, Gaussian response of 0.13° FWHM, 20 layouts) gives 11.2 dB peak-to-mean-floor and 5.6 dB peak-to-highest-floor (range 4.2–6.4 dB) with perfect amplitudes. With 1 dB and 2 dB rms amplitude spread it gives 5.5 and 5.3 dB. So the camera alone accounts for most of the 3–6 dB.
  - **Current text.** Finding 2's last sentence says that because each pixel integrates many spots, "a pixel's floor therefore sits far above the per-spot mean". That inverts the mechanism: averaging leaves the floor at its mean, and it is the main-lobe peak that is diluted. The edit below states the mechanism, the paper's own attribution and the geometry.
- **Source:**
  - Qiu, H., Liu, Y., Meng, X., Guan, X., Ding, Y. & Hu, H., "Ultra-sparse aperiodic silicon optical phased array using high-performance thermo-optic phase shifter", *Laser Photonics Rev.* 18, 2301177 (2024), doi:10.1002/lpor.202301177. Read pp. 2–9 of the DTU Orbit peer-reviewed copy (the URL already in Appendix 2), full text: Fig. 1 (layout), Fig. 2 (element factor), Fig. 3a and text p. 4 (13% → 0.8%), Fig. 4 (12.8 dB GLSR), §3 p. 8 (3–6 dB measured GLSR and its attribution, 0.13° camera-limited beam, ≈12,000 simulated resolvable points, 13.7° wavelength axis).
  - Calculations: `scripts/R5_sparse_array_mc.py`, Parts B and C.
- **Evidence tag:** [P] for the device facts and the paper's attribution; [E] for $N/N_{\rm spot}$ and the camera calculation.
- **Confidence:** high for the geometry and the 0.8% convention (the paper's own 13% and 0.8% are both reproduced); medium for the camera estimate, because random layouts stand in for the paper's optimized ones and the camera response is modelled as Gaussian.
- **Proposed edit:**
  - `old`:
    ```text
    DTU's 120-element array spread over 6 mm has a *simulated* main-lobe fraction of 0.8%. Its *measured* floor, only 3–6 dB below the peak, was recorded with a camera of 0.13° resolution, whose pixels each integrate many sidelobe spots of width $\lambda/D$, with $D=6$ mm the aperture: $1.55\ \mu{\rm m}/6\ {\rm mm}=2.6\times10^{-4}$ rad $=0.015^\circ$, about $0.13/0.015\approx9$ spots per pixel along that axis. A pixel's floor therefore sits far above the per-spot mean of §C10.1, $1/N=1/120$, i.e. −21 dB [E].
    ```
  - `new`:
    ```text
    DTU's 120-element array is one aperiodic row of 120 grating emitters at a mean pitch of about 50 µm across 6 mm, each grating 5 mm long and steered by wavelength along the other axis, so it is sparse along one axis only [P]. Its *simulated* main-lobe fraction of 0.8% comes from the array factor alone, with a flat element pattern over the ±90° field, and it is what §C10.1 predicts: counting spots in angle as the paper does, $N_{\rm spot}=\pi D/\lambda=\pi\times6\ {\rm mm}/1.55\ \mu{\rm m}\approx12{,}200$ (the paper's ≈12,000 simulated resolvable points), so $N/N_{\rm spot}=120/12{,}200=1.0\%$, and random 120-element layouts give 0.9% [E]. Its *measured* floor, only 3–6 dB below the peak, is set mostly by the camera's 0.13° resolution, about 9 main-lobe widths ($\lambda/D=1.55\ \mu{\rm m}/6\ {\rm mm}=2.6\times10^{-4}$ rad $=0.015^\circ$, with $D=6$ mm the aperture). The camera spreads the main lobe over those 9 widths and reads its peak about 9.5 dB low ($10\log_{10}9$), while it averages the floor to its mean, $1/N=1/120$ of the true peak (−21 dB). The observed peak therefore stands only about 11 dB above the mean floor, and the floor's highest points lie 5–6 dB above that mean [E: 120 random emitters over 6 mm seen through a 0.13° Gaussian response give 11 dB to the mean floor and 4–6.5 dB to its highest point]. The paper itself attributes the gap from its simulated 12.8 dB to amplitude variation in its cascaded directional couplers [P].
    ```
  - `old`:
    ```text
    | DTU ultra-sparse 120 (LPR 2024) [P] | 120 over 6 × 5 mm | 162° |
    ```
  - `new`:
    ```text
    | DTU ultra-sparse 120 (LPR 2024) [P] | 120 in one aperiodic row, ≈50 µm mean pitch, across 6 mm; gratings 5 mm long | Phase 162° × wavelength 13.7° (1,480–1,572 nm) |
    ```
- **Appendix 2 entry:** none (Qiu *et al.*, *Laser Photonics Rev.* 2024, is listed).

## R5_C10_part1-03

- **Question:** What were the inputs of the sparse-array Monte Carlo behind 8.5% ($N=128$, $N_{\rm spot}\approx1{,}140$) and 12% ($N=256$, $N_{\rm spot}\approx1{,}720$)?
- **Answer:**
  - **Origin.** The run that first produced these numbers is not archived. They were already in the report snapshot of 28 Sep 2026, before the audit of that day. That audit re-implemented the check, and its script (the sparse-array block of `audit/agent7/mc.py` in that audit's scratch folder) fixes every input:
    - $N_{\rm spot}$ is an input, 1,140 for $N=128$ and 1,720 for $N=256$, with no other stated origin.
    - The aperture is $L=N_{\rm spot}\lambda/2$: $570\lambda=0.88$ mm and $860\lambda=1.33$ mm at 1.55 µm.
    - $N$ isotropic elements are placed independently and uniformly at random on $[0,L]$, with no minimum spacing.
    - The far field is sampled in $u=\sin\theta$ over all of visible space, $[-1,1]$, at $40N_{\rm spot}+1$ points, so that $N_{\rm spot}=2L/\lambda$ beamwidths fit in the range.
    - The main lobe is $|u|<\lambda/L$ (first nulls) and the sidelobes are the rest.
    - The run uses numpy `default_rng(1)` and 20 trials.
  - **Re-run [E].** `R5_mc_rerun_check.py` repeats that block and gives, for $N=128$: 9.3% main lobe (sd 0.6% over trials), peak sidelobe −11.7 dB, mean −21.1 dB. For $N=256$: 11.7% (sd 0.5%), −12.9 dB, −24.0 dB. A 200-trial run (`R5_sparse_array_mc.py`, Part A, seed 2) gives 9.2%, −11.5 dB, −21.0 dB and 11.8%, −13.0 dB, −24.0 dB.
  - **Analytic check.** With $E|AF|^2=N+N(N-1)\,{\rm sinc}^2(uL)$, the expected fraction is $[2N/L+0.903N(N-1)/L]/[2N+N(N-1)/L]=9.2\%$ and 11.8%, i.e. close to $0.90\,N/(N_{\rm spot}+N)$ (9.1% and 11.7%). The 0.90 is the share of the main lobe inside its first nulls, and $N_{\rm spot}+N$ appears because the main lobe's own power adds to the total.
  - **Comparison with the report.** The mean sidelobes (−21, −24 dB) and the 12% are reproduced. The 8.5% for $N=128$ is not: it lies about 1.3 single-trial standard deviations below the expectation. The peak sidelobes come out 0.4–0.5 dB lower than −11 and −12.6 dB.
  - **Dependent text.** The next bullet's "1.6 dB" improvement of the peak sidelobe becomes 1.5 dB (200 trials: $12.97-11.51=1.46$ dB); the mean improves by 3.0 dB as stated.
- **Source:** Report-internal calculation. Inputs taken from the 28 Sep 2026 audit script (file read in full). Results from `scripts/R5_mc_rerun_check.py` and `scripts/R5_sparse_array_mc.py` (Part A), run 5 Oct 2026.
- **Evidence tag:** [E].
- **Confidence:** high for the inputs and re-run values (reproducible, and matching the analytic expectation); the original 8.5% cannot be traced.
- **Proposed edit:**
  - `old`:
    ```text
    - A Monte Carlo check with random sparse arrays gave **8.5%** main-lobe power for $N=128$ and $N_{\rm spot}\approx1{,}140$ ($N/N_{\rm spot}=11\%$), with a peak sidelobe of −11 dB and a mean sidelobe of −21 dB. For $N=256$ and $N_{\rm spot}\approx1{,}720$ ($N/N_{\rm spot}=15\%$) it gave 12%, −12.6 dB and −24 dB.
    ```
  - `new`:
    ```text
    - A Monte Carlo check [E] placed $N$ isotropic elements independently and uniformly at random over an aperture $L=N_{\rm spot}\lambda/2$: $570\lambda=0.88$ mm for $N=128$ and $N_{\rm spot}=1{,}140$, and $860\lambda=1.33$ mm for $N=256$ and $N_{\rm spot}=1{,}720$, at 1.55 µm. It evaluated the far field over all of visible space, $\sin\theta$ from −1 to 1, which holds $N_{\rm spot}=2L/\lambda$ beamwidths, and counted the main lobe out to its first nulls, $|\sin\theta|<\lambda/L$. Over 200 trials it gave **9.2%** main-lobe power for $N=128$ ($N/N_{\rm spot}=11\%$), with a peak sidelobe of −11.5 dB and a mean sidelobe of −21 dB, and 11.8% ($N/N_{\rm spot}=15\%$), −13.0 dB and −24 dB for $N=256$. Both fractions match the expectation $0.90\,N/(N_{\rm spot}+N)$, 9.1% and 11.7%: 90% of the main lobe lies inside its first nulls, and the main lobe's own power adds to the total.
    ```
  - `old`:
    ```text
    As expected, they improve only weakly with $N$ (1.6 dB, against 3 dB for the mean).
    ```
  - `new`:
    ```text
    As expected, they improve only weakly with $N$ (1.5 dB, against 3 dB for the mean).
    ```
- **Appendix 2 entry:** none (internal calculation; scripts archived in `sources/scripts/`).

## R5_C10_part1-04

- **Question:** On what reflectance were the 50 m (9,216 elements), 22 m (Jilin) and 20 m (imec) results obtained, and which device reached 100 m on a 90% target?
- **Answer:**
  - **9,216 elements (Moss *et al.*, VLSI 2023).** The abstract states a ">50 meter coherent LiDAR engine" and gives no target or reflectance. The full two-page paper is paywalled and was not read. Pointcloud's table (50 m, no energy) and the npj review's Table 5 (aperture 6,000 × 15,667 µm, 0.05° × 0.05°) give no reflectance either. No source was found for the "55 m" in the device table. Reflectance: not stated [U].
  - **Jilin Vernier (Chen *et al.*, LPR 2024).** The 22.15 m is an indoor back wall seen through a folding mirror (preprint Fig. 3d–g; 25 dBm in, ≈11 dBm in the main beam). Neither the arXiv text (v1, the only version) nor the published abstract states the wall's reflectance. The npj review's Table 14 lists this result as "22 @ 10%" [S].
  - **imec (Prost *et al.*, Nat. Commun. 2026).** The 20 m result images a "T" logo target with a 35 mm f/1.4 lens and a 1,000 µs chirp. The paper gives no reflectance for it, and says only that its reflective target is "made of a material similar to that used in traffic signs". In the transparent peer-review file the authors state that their targets are commercial retroreflective traffic-sign tape, quoted at about 70% from the manufacturer's visible-band specification (not measured at 1,550 nm). They declined a reviewer's request for a 10% target, noting that the loss could in principle be made up with more power. So the 20 m is on a retroreflective target, not a diffuse 10% one [P].
  - **100 m on 90%.** Li, Y. *et al.* (Jilin University), *Photonics Res.* 9, 2511 (2021) (item 01): 128-channel SiN-on-SOI OPA, aperiodic 29.7 µm mean pitch, 4 × 3 mm aperture, 140° (chain) or 100° (fishbone) × 19.2–19.4° (1,350–1,630 nm). FMCW to 100 m on a 90% scatter plate, with the path mirror-folded beyond 50 m and a collimator receiver. Equivalent range at 10%: $100\ {\rm m}\times\sqrt{0.1/0.9}=33.3$ m. It is both the npj review's "100 @ 90%" (its ref. 25) and Pointcloud's Ref. [19].
- **Source:**
  - IEEE Xplore abstract of Moss *et al.*, 2023 IEEE Symp. VLSI Technology and Circuits, pp. 1–2, doi:10.23919/VLSITechnologyandCir57934.2023.10185161 (abstract read).
  - Chen, B. *et al.*, arXiv:2401.04335 v1 (full text read, pp. 1–8), and the *Laser Photonics Rev.* 18, 2301360 (2024) abstract via Crossref.
  - Prost, M. *et al.*, "Monolithically integrated silicon photonic biaxial FMCW LiDAR system", *Nat. Commun.* (published 4 Sep 2026), doi:10.1038/s41467-026-77490-4: published PDF p. 5 read (full text), and the Transparent Peer Review file (MOESM2) pp. 17 and 22 read.
  - Xu, W. *et al.*, *npj Nanophotonics* 2, 14 (2025), Table 14 (p. 24) and Table 5 (p. 13), full PDF read.
  - Li *et al.* 2021 as in item 01.
- **Evidence tag:** [U] (9,216 reflectance); [S] (Jilin 10%, review only); [P] (imec target type; Li *et al.* device and target).
- **Confidence:** high for imec and Li *et al.*; medium for Jilin (the 10% rests on the review alone); the 9,216 reflectance stays open.
- **Proposed edit:**
  - `old`:
    ```text
    - 35 m at 10% (8,192 elements), about 50 m (9,216), 22 m (Jilin), 20 m (imec). 100 m has been shown only on a 90% target [S].
    ```
  - `new`:
    ```text
    - 35 m at 10% (8,192 elements) [S]; more than 50 m for the 9,216-element array, reflectance not stated [I, abstract]; 22 m for Jilin's Vernier array, to an indoor wall whose reflectance the paper does not state (10% in the npj review [S]); and 20 m for imec, on a retroreflective traffic-sign-type target [P]. 100 m has been shown only on a 90% scatter plate, by Jilin University's 128-channel OPA (Li *et al.*, *Photon. Res.* 2021), with the path folded by a mirror beyond 50 m and a fibre collimator as receiver [P]; that is ≈33 m at 10% under $R^2$ scaling.
    ```
  - `old`:
    ```text
    100 m has been shown only on a 90% target, which is ≈33 m at 10% under $R^2$ scaling
    ```
  - `new`:
    ```text
    100 m has been shown only on a 90% target, by Jilin University's 128-channel OPA in 2021 (§C10.2b), which is ≈33 m at 10% under $R^2$ scaling
    ```
  - `old`:
    ```text
    <3.8 µs point-to-point | About 50–55 m coherent |
    ```
  - `new`:
    ```text
    <3.8 µs point-to-point | More than 50 m coherent [I, abstract]; reflectance not stated |
    ```
  - `old`:
    ```text
    | 25 dBm in, about 11 dBm in the main beam | FMCW 22 m |
    ```
  - `new`:
    ```text
    | 25 dBm in, about 11 dBm in the main beam | FMCW 22 m, to an indoor wall via a folding mirror; the paper states no reflectance, and the npj review lists 10% [S] |
    | Jilin 128-channel SiN-on-SOI (*Photon. Res.* 2021) [P] | 128, aperiodic, 29.7 µm mean pitch; 4 × 3 mm aperture | Phase 140° (chain gratings) or 100° (fishbone) × wavelength 19.2–19.4° (1,350–1,630 nm) | 0.021° × 0.1° (chain), 0.021° × 0.029° (fishbone) | System insertion loss 17.7 dB (chain) and 17.0 dB (fishbone); PN shifters ≤1.8 µW static; sidelobe suppression 10.3–10.6 dB at 0° | FMCW **100 m on a 90% scatter plate** (path folded by a mirror beyond 50 m; OPA transmit, fibre-collimator receive), 26 dBm in; 1,360 nJ per point [S]; ≈33 m at 10% under $R^2$ scaling |
    ```
  - `old`:
    ```text
    about 85% main-lobe power | FMCW 20 m |
    ```
  - `new`:
    ```text
    about 85% main-lobe power | FMCW 20 m, on a retroreflective traffic-sign-type target; no low-reflectance target was tested [P] |
    ```
- **Appendix 2 entry:**
  - - Li Y. *et al.* — as in item 01 (one line for both items).
  - - Prost *et al.* (imec), transparent peer review file (target material, 2026): https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-77490-4/MediaObjects/41467_2026_77490_MOESM2_ESM.pdf

## R5_C10_part1-05

- **Question:** Which papers support "about 12 rad per nm of width error per mm of Si path" and "a phase-coherence length of about 1.6–4 mm", and how do they define the coherence length?
- **Answer:**
  - **Phase sensitivity.** The phase per unit width error is $(2\pi/\lambda)(\partial n_{\rm eff}/\partial w)L$. For a 400 nm wide, 220 nm thick Si strip at 1,550 nm, Rizzo *et al.* simulate $\partial n_{\rm eff}/\partial w=3\times10^{-3}\ {\rm nm^{-1}}$. That gives $(2\pi/1.55\ \mu{\rm m})\times3\times10^{-3}\ {\rm nm^{-1}}\times1\ {\rm mm}=12.2$ rad per nm per mm, so the report's 12 rad holds for a 400 nm strip.
  - **Common 500 nm strip.** Yang *et al.*'s Table 1 gives $C_w=1.6\times10^{-3}\ {\rm nm^{-1}}$ (strip) and $1.2\times10^{-3}\ {\rm nm^{-1}}$ (rib), i.e. 6.5 and 4.9 rad/nm/mm. Rizzo *et al.*'s Fig. 1b gives ≈0.0016 at 500 nm as well.
  - **Coherence length.** Yang *et al.* measured 4.17 ± 0.42 mm for single-mode strip and 1.61 ± 0.12 mm for rib waveguides. They used 800 unbalanced Mach–Zehnder interferometers (five path differences, 50–1,044 µm) in 8 dies across one 6-inch, 220 nm SOI MPW wafer (BAE Systems, 248 nm lithography).
  - **Their definition.** $L_{\rm coh}$ is the length at which $\langle e^{i\Delta\phi}\rangle=e^{-1}$, with the random phase Gaussian. Its standard deviation is $(2L/L_{\rm coh})^{1/2}$ for a guide of length $L$, i.e. $\sqrt2$ rad at $L=L_{\rm coh}$ and 1 rad at $L_{\rm coh}/2$. This differs from the report's gloss ("no longer keep a predictable phase relation"), so the edit uses the paper's definition.
- **Source:**
  - Yang, Y., Ma, Y., Guan, H., Liu, Y., Danziger, S., Ocheltree, S., Bergman, K., Baehr-Jones, T. & Hochberg, M., "Phase coherence length in silicon photonic platform", *Opt. Express* 23(13), 16890–16902 (2015), doi:10.1364/OE.23.016890: abstract, §2.3 (definition), Table 1, §3. Full text read on Optica's open-access HTML page.
  - Rizzo, A. *et al.*, "Fabrication-robust silicon photonic devices in standard sub-micron silicon-on-insulator processes", *Opt. Lett.* 48(2), 215 (2023), doi:10.1364/OL.476873. Read via the arXiv preprint 2205.11481 (full text, p. 2 and Fig. 1 rendered).
- **Evidence tag:** [I].
- **Confidence:** high — both numbers are stated explicitly and the 12 rad/nm/mm follows from the 400 nm sensitivity in one line.
- **Proposed edit:**
  - `old`:
    ```text
    - Waveguide-width errors, correlated along each guide, accumulate phase at about 12 rad per nm of width error per mm of Si path, so after a few millimetres the uncalibrated phases are effectively random. The Si phase-coherence length, the guide length beyond which two nominally identical paths no longer keep a predictable phase relation, is about 1.6–4 mm [I].
    ```
  - `new`:
    ```text
    - Waveguide-width errors, correlated along each guide, accumulate a phase $(2\pi/\lambda)(\partial n_{\rm eff}/\partial w)$ per unit width error and length: about 12 rad per nm of width error per mm for a 400 nm wide Si strip ($\partial n_{\rm eff}/\partial w=3\times10^{-3}\ {\rm nm^{-1}}$ at 1,550 nm, Rizzo *et al.*, *Opt. Lett.* 2023) and about 6.5 rad for the common 500 nm strip ($1.6\times10^{-3}\ {\rm nm^{-1}}$, Yang *et al.*, *Opt. Express* 2015) [I; $(2\pi/1.55\ \mu{\rm m})\times3\times10^{-3}\ {\rm nm^{-1}}\times1\ {\rm mm}=12$ rad]. After a few millimetres the uncalibrated phases are therefore effectively random. Yang *et al.* measured the phase-coherence length of 220 nm SOI waveguides, the length $L_{\rm coh}$ at which the random phase reaches an rms of $\sqrt2$ rad (its rms is $\sqrt{2L/L_{\rm coh}}$ for a length $L$, so $\langle e^{i\Delta\phi}\rangle=e^{-1}$ at $L_{\rm coh}$), at 4.2 mm for strip and 1.6 mm for rib waveguides, from 800 Mach–Zehnder interferometers across one 6-inch foundry wafer [I].
    ```
- **Appendix 2 entry:**
  - - Yang *et al.*, "Phase coherence length in silicon photonic platform", *Opt. Express* 23, 16890 (2015): https://opg.optica.org/oe/fulltext.cfm?uri=oe-23-13-16890
  - - Rizzo *et al.*, fabrication-robust SOI devices (width sensitivity of Si strips), *Opt. Lett.* 48, 215 (2023), preprint: https://arxiv.org/abs/2205.11481

## R5_C10_part1-06

- **Question:** What is the element count of the largest published 2D phase-controlled array, and from what source?
- **Answer:**
  - **Waveguide-fed integrated 2D OPAs.** These stay at about $10^2$ elements with a phase control each. The largest found is Fatemi, Khachaturian & Hajimiri's nonuniform sparse 2-D OPA: 128 radiating elements, a 16°/0.8° grating-lobe-free field-to-beamwidth ratio (≥400 resolvable spots), and row–column drive cutting 144 drivers to 37. The earlier active 2D arrays are 8 × 8 = 64 (Sun *et al.*, *Nature* 2013; Abediasl & Hashemi 2015). Sun *et al.*'s 64 × 64 = 4,096 array was passive, with fixed phases. The npj review mentions only 8 × 8 active 2D arrays, and its large arrays (1,024, 8,192, 9,216) are one-dimensional along the phase axis.
  - **Free-space-fed MEMS 2D OPA.** Wang *et al.* report 160 × 160 = 25,600 independent MEMS-actuated grating phase shifters over 3.1 × 3.2 mm. Its beam is 0.042° × 0.031°, its field 6.6° × 4.4°, its response time 5.7 µs, with about 25,600 steerable spots.
  - **Ratios.** Against the report's $1.2\times10^{6}$: $1.2\times10^{6}/128=9{,}400$ (four orders of magnitude) and $1.2\times10^{6}/25{,}600=47$ (1.7 orders).
  - **LCOS.** Wang *et al.* also note that liquid-crystal-on-silicon modulators reach 8 million phase pixels but respond in milliseconds. Those are larger 2D phase arrays, so the edit names them.
- **Source:**
  - Fatemi, R., Khachaturian, A. & Hajimiri, A., "A nonuniform sparse 2-D large-FOV optical phased array with a low-power PWM drive", *IEEE J. Solid-State Circuits* 54(5), 1200–1215 (2019), doi:10.1109/JSSC.2019.2896767 (IEEE abstract read).
  - Wang, Y. *et al.*, "2D broadband beamsteering with large-scale MEMS optical phased array", *Optica* 6(5), 557–562 (2019), doi:10.1364/OPTICA.6.000557. Full text read (University of Arizona author copy; pp. 1–2 rendered: abstract, introduction, refs. 2, 14, 15, 20).
  - npj review (Xu *et al.* 2025), p. 18 and Table 5.
- **Evidence tag:** [I]; the LCOS figure [I, as cited by Wang *et al.*].
- **Confidence:** medium — a web and review search found nothing larger, but "largest" cannot be proven exhaustively.
- **Proposed edit:**
  - `old`:
    ```text
    Published 2D arrays are orders of magnitude smaller [U].
    ```
  - `new`:
    ```text
    The largest integrated 2D phased arrays reported with a phase control per element are far smaller: 128 emitters in a waveguide-fed silicon chip (Fatemi *et al.*, *IEEE JSSC* 2019) and 160 × 160 = 25,600 MEMS-actuated grating phase shifters in a free-space-fed chip with a 6.6° × 4.4° field (Wang *et al.*, *Optica* 2019) [I], about 9,400 and 47 times fewer ($1.2\times10^{6}/128$ and $1.2\times10^{6}/25{,}600$). Liquid-crystal-on-silicon modulators have millions of phase pixels but respond in milliseconds [I, as cited by Wang *et al.*].
    ```
- **Appendix 2 entry:**
  - - Fatemi, Khachaturian & Hajimiri, 128-element nonuniform sparse 2-D OPA, *IEEE JSSC* 54, 1200 (2019): https://ieeexplore.ieee.org/document/8649827
  - - Wang Y. *et al.*, 160 × 160 MEMS 2D optical phased array, *Optica* 6, 557 (2019): https://opg.optica.org/optica/fulltext.cfm?uri=optica-6-5-557

## R5_C10_part1-07

- **Question:** Does the FS-4S datasheet state that its ≤0.04° × 0.02° beam widths are FWHM?
- **Answer:** Yes. The FS-4S specification table reads "Beam Spot Size (H×V): ≤ 0.04° × 0.02° FWHM". It gives the sampling grid separately as "Angular Resolution (H×V): 0.15° × 0.15° (programmable)". So 2.8% (FWHM ellipse) and ≈8% (Gaussian 1/e²) are firm values, and the three conditionals go. §C0 subsection 10.8 already says FWHM and needs no change. The SR-1S datasheet lists the same "≤ 0.04° × 0.02° FWHM" beam spot, with a 0.4° × 0.4° angular resolution (see item 08).
- **Source:** Analog Photonics, "FS-4S LiDAR" product brochure, Rev A (file name; PDF created 2 July 2025), p. 1 specification table, https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf . Both pages rendered and read.
- **Evidence tag:** [P] (vendor claim).
- **Confidence:** high — explicit in the specification table.
- **Proposed edit:**
  - `old`:
    ```text
    Beam ≤0.04° × 0.02°, sampling grid 0.15° × 0.15°.
    ```
  - `new`:
    ```text
    Beam ≤0.04° × 0.02° FWHM, sampling grid 0.15° × 0.15°.
    ```
  - `old`:
    ```text
    If the quoted widths are FWHM, the nominal 1/e² footprint fraction (§C10.3b convention: the spot is bounded where intensity falls to $1/e^2$ of its peak) is about 1.6–8%.
    ```
  - `new`:
    ```text
    Taking the quoted widths as FWHM, as the FS-4S datasheet states for its beam, the nominal 1/e² footprint fraction (§C10.3b convention: the spot is bounded where intensity falls to $1/e^2$ of its peak) is about 1.6–8%.
    ```
  - `old`:
    ```text
    and ≈8% as a nominal 1/e² footprint fraction (§C10.3b convention) if the datasheet widths are FWHM.
    ```
  - `new`:
    ```text
    and ≈8% as a nominal 1/e² footprint fraction (§C10.3b convention), since the datasheet gives the widths as FWHM.
    ```
  - `old`:
    ```text
    | Analog Photonics FS-4S (§C10.2b) | ≈3.6% | ≈2.8% | ≈8%, if the datasheet widths are FWHM |
    ```
  - `new`:
    ```text
    | Analog Photonics FS-4S (§C10.2b) | ≈3.6% | ≈2.8% | ≈8% |
    ```
- **Appendix 2 entry:** none (the FS-4S datasheet is listed).

## R5_C10_part1-08

- **Question:** Which laser do the FS-4S and SR-1S datasheets name?
- **Answer:**
  - **FS-4S and SR-1S.** Neither names a laser model. Both list "Wavelength: C + L-Band" and, under applications and benefits, "Integrated tunable laser". Their block diagrams show a generic "Laser" block, and "RAY" appears nowhere in either file.
  - **RAY-H1.** A separate product: >25 dBm, "C + L-Band (2-Channel)", 60 nm tuning, <300 µs random access, <40 kHz linewidth, ≤1.5 GHz chirp, 19 W as a module (5 W gold-box only).
  - **RAY-L1.** A low-power sibling with the same tuning, linewidth and chirp specifications and >0 dBm.
  - **Consequence.** Both §C10.2b derivations (60 nm for RAY-H1, ≈95 nm for the full C+L band) are assumptions about which laser is inside. The SR-1S row also lacks its band and beam spot, and its "0.4° × 0.4°" is the datasheet's angular resolution (sampling grid), not the beam.
- **Source:**
  - Analog Photonics product brochures, all Rev A (file names), read in full (both pages rendered):
    - FS-4S (PDF created 2 July 2025): https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf
    - SR-1S (23 July 2025): https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-SR-1S-RevA.pdf
    - RAY-H1 (20 June 2025): https://www.analogphotonics.com/wp-content/uploads/2025/06/Laser-RAY-H1-RevA.pdf
    - RAY-L1 (19 June 2025): https://www.analogphotonics.com/wp-content/uploads/2025/06/Laser-RAY-L1-RevA.pdf
- **Evidence tag:** [P] (vendor claims).
- **Confidence:** high — read directly from the specification tables.
- **Proposed edit:**
  - `old`:
    ```text
    | **FS-4S** (long range) | C+L band, Class 1,
    ```
  - `new`:
    ```text
    | **FS-4S** (long range) | C+L band with an "integrated tunable laser" (no model named), Class 1,
    ```
  - `old`:
    ```text
    | **SR-1S** (short range) | 20 m at 10%, 150° × 70°, 0.4° × 0.4°, 660 kpts/s, 35 W | The 70° wavelength-steered axis would need ≈1.17°/nm over RAY-H1's 60 nm,
    ```
  - `new`:
    ```text
    | **SR-1S** (short range) | C+L band with an "integrated tunable laser" (no model named), 20 m at 10%, 150° × 70°, sampling grid 0.4° × 0.4°, beam ≤0.04° × 0.02° FWHM (as on the FS-4S sheet), 660 kpts/s, 35 W | The 70° wavelength-steered axis would need ≈1.17°/nm over a 60 nm sweep such as RAY-H1's,
    ```
- **Appendix 2 entry:** - Analog Photonics RAY-L1 laser datasheet (Rev A, June 2025): https://www.analogphotonics.com/wp-content/uploads/2025/06/Laser-RAY-L1-RevA.pdf (optional; the other three sheets are listed).

## R5_C10_part1-09

- **Question:** Is there an FSOC-B1 datasheet to cite, with revision and date?
- **Answer:**
  - **The datasheets.** The FSOC-B1 brochure is linked from the company's "Free Space Optical Communication" page at https://www.analogphotonics.com/wp-content/uploads/2025/06/FSOC-B1-RevA.pdf (Rev A in the file name; PDF created 20 June 2025). The page's own link, without "wp-content", returns 404. Its sister part OPA-B1, the "Optical Phased Array Beam Steerer", has a coherent receiver: https://www.analogphotonics.com/wp-content/uploads/2025/06/OPA-B1-RevA.pdf (Rev A; created 19 June 2025).
  - **Shared specifications.** Both specify C + L-band; 400 mW maximum input; optical power in the beam "≤ 7.5 dB IL from fiber input"; 1 mrad × 1 mrad beam; 50° × 14° field; "< 10 µs random access" point-to-point steering; < 5 W; a 7 × 6 × 1 cm PCB; availability "Immediate".
  - **Differences.** FSOC-B1 has a direct-detection (APD) receiver and OPA-B1 an I-Q coherent receiver. Both say "Customer-provided laser for C- and/or L-band". Their field-of-view figure labels the 14° axis "λ-Axis (Wavelength Steering)" and the 50° axis "θ-Axis (Phase Steering)".
  - **Consequence.** The report's conditional "If its 14° axis is wavelength-steered" is a fact, and the <10 µs figure can hold across that axis only with a laser about 30× faster than RAY-H1 ($300/10=30$). The row's figures all match, so its [U] and finding 4's [U] become [P] (vendor claim).
- **Source:** Analog Photonics, "FSOC-B1" and "OPA-B1" product brochures, Rev A, June 2025, p. 1 specification tables and p. 2 field-of-view figure (both files read in full, both pages rendered); company product pages https://www.analogphotonics.com/product/free-space-optical-communication/ and https://www.analogphotonics.com/product/optical-phased-array-beam-steerer/ (read 5 Oct 2026).
- **Evidence tag:** [P] (vendor claims).
- **Confidence:** high — every figure in the row was found in the datasheets.
- **Proposed edit:**
  - `old`:
    ```text
    | **FSOC-B1** / OPA-B1 steerer | 50° × 14°, 1 mrad beam, ≤7.5 dB fibre-to-beam loss at up to 400 mW in, <10 µs random access, <5 W [U] | The same OPA engine sold for free-space optical links. If its 14° axis is wavelength-steered, <10 µs access needs a laser that retunes about 30× faster than RAY-H1 (<300 µs) |
    ```
  - `new`:
    ```text
    | **FSOC-B1** / OPA-B1 steerer | 50° × 14° (phase-steered 50° axis, wavelength-steered 14° axis), 1 mrad × 1 mrad beam, ≤7.5 dB insertion loss from fibre input to beam at up to 400 mW in, <10 µs point-to-point random access, <5 W, customer-provided C/L-band laser; FSOC-B1 has a direct-detection receiver and OPA-B1 an I-Q coherent receiver [P] | The same OPA engine sold for free-space optical links. Because the 14° axis is wavelength-steered and the laser is the customer's, <10 µs access across that axis needs a laser that retunes about 30× faster than RAY-H1 (<300 µs) |
    ```
  - `old`:
    ```text
    (products table below; vendor claim [U])
    ```
  - `new`:
    ```text
    (products table below; vendor claim [P])
    ```
  - `old`:
    ```text
    - Analog Photonics FS-4S / SR-1S / RAY-H1 / FSOC-B1 datasheets (2025): https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf ; https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-SR-1S-RevA.pdf ; https://www.analogphotonics.com/wp-content/uploads/2025/06/Laser-RAY-H1-RevA.pdf
    ```
  - `new`:
    ```text
    - Analog Photonics FS-4S / SR-1S / RAY-H1 / FSOC-B1 / OPA-B1 datasheets (Rev A, June–July 2025): https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-FS-4S-RevA.pdf ; https://www.analogphotonics.com/wp-content/uploads/2025/07/LiDAR-SR-1S-RevA.pdf ; https://www.analogphotonics.com/wp-content/uploads/2025/06/Laser-RAY-H1-RevA.pdf ; https://www.analogphotonics.com/wp-content/uploads/2025/06/FSOC-B1-RevA.pdf ; https://www.analogphotonics.com/wp-content/uploads/2025/06/OPA-B1-RevA.pdf
    ```
- **Appendix 2 entry:** covered by the third edit above.

## R5_C10_part1-10

- **Question:** Does the CLEO 2023 abstract give exactly 49,152 elements or more?
- **Answer:** More. The abstract describes a super-cell "spanning four reticles and containing over 49,152 active elements". It enables "cross-reticle light routing between 24 OPAs" with coherent combination by intra- and inter-reticle IQ receivers. The table's ">49,152" and finding 1's "more than 49,152 elements" are correct as written, so no text edit is needed. The 24 × 2,048 = 49,152 product is not stated in the abstract. The source is missing from Appendix 2.
- **Source:** Guglielmon, J., Byrd, M. J., Moss, B. R., Tran, J., Millman, R. P., Watts, M. R. & Poulton, C. V., "Optical Phased Array Super-Cell Beyond the Reticle Limit", CLEO: Science and Innovations 2023, paper STh5C.5, doi:10.1364/CLEO_SI.2023.STh5C.5, https://opg.optica.org/abstract.cfm?uri=CLEO_SI-2023-STh5C.5 (abstract read; the summary is not hosted on the company site, whose paper list stops at 2021).
- **Evidence tag:** [I, abstract].
- **Confidence:** high — the wording "over 49,152" is explicit.
- **Proposed edit:** none (the current text already says ">49,152" and "more than 49,152").
- **Appendix 2 entry:** - Guglielmon *et al.* (Analog Photonics), "Optical phased array super-cell beyond the reticle limit", CLEO 2023, STh5C.5 (abstract): https://opg.optica.org/abstract.cfm?uri=CLEO_SI-2023-STh5C.5
