# Round 4 source items: R5_C10_part1

## R5_C10_part1-01 [09_C10_part1] report #9 (part)

- **Where:** §C10.2b finding 7, 'Optical energy per point for OPA lidars is 1,360–1,700 nJ' and the next bullet, '…from 35 m to 200 m at 10% gives ≈44–56 µJ per point'
- **What is needed:** Device, range and reflectance behind the 1,360 nJ value in Pointcloud's comparison table. If it was not measured at 35 m on 10%, scale it from its own range and reflectance in the ≈44–56 µJ step and the 530–670 W that follows.

## R5_C10_part1-02 [09_C10_part1] report #11 (part)

- **Where:** §C10.2b finding 2, 'DTU's 120-element array spread over 6 mm has a *simulated* main-lobe fraction of 0.8%'
- **What is needed:** To state the $N/N_{\rm spot}$ prediction for this array, the DTU paper's geometry is needed: 1D or 2D layout over the 6 × 5 mm aperture, element pattern and the field used in the 0.8% simulation. The camera explanation of the 3–6 dB floor is applied as an edit.

## R5_C10_part1-03 [09_C10_part1] report #20

- **Where:** §C10.1 sparse array, 'A Monte Carlo check with random sparse arrays gave **8.5%** main-lobe power for $N=128$ and $N_{\rm spot}\approx1{,}140$'
- **What is needed:** Inputs of the Monte Carlo run: aperture length, placement rule, the steering range that sets $N_{\rm spot}$ (≈1,140 and ≈1,720) and the number of trials. The $N/N_{\rm spot}=15\%$ for $N=256$ is applied as an edit.

## R5_C10_part1-04 [09_C10_part1] report #26

- **Where:** §C10.2b finding 7, '35 m at 10% (8,192 elements), about 50 m (9,216), 22 m (Jilin), 20 m (imec). 100 m has been shown only on a 90% target [S].' (also the summary, 'Measured reality check')
- **What is needed:** Reflectance for the 50 m (9,216), 22 m (Jilin) and 20 m (imec) results, and the device and year of the 100 m result on a 90% target (≈33 m at 10%), which should also be added to the device table.

## R5_C10_part1-05 [09_C10_part1] report #27 (part)

- **Where:** §C10.2b finding 3, 'about 12 rad per nm of width error per mm of Si path … about 1.6–4 mm [I]'
- **What is needed:** The [I] tag names no source. Give the paper for the 12 rad/nm/mm sensitivity and the 1.6–4 mm phase-coherence length, and use that paper's own definition of the coherence length if it differs from the gloss in the edit.

## R5_C10_part1-06 [09_C10_part1] report #33 (part)

- **Where:** §C10.2 item 2, 'Published 2D arrays are orders of magnitude smaller [U].'
- **What is needed:** Element count and source of the largest published 2D phase-controlled array, to replace the [U] claim with a number and a [P]/[I] tag.

## R5_C10_part1-07 [09_C10_part1] follow-up #3

- **Where:** §C10 summary 'If the quoted widths are FWHM…'; §C10.2b 'if the datasheet widths are FWHM'; §C10.3 footprint table '≈8%, if the datasheet widths are FWHM'; outside the block §C0 subsection 10.8, 'with a beam of at most 0.04° × 0.02° FWHM.'
- **What is needed:** Check the FS-4S datasheet. If it states FWHM, write 'Beam ≤0.04° × 0.02° FWHM' in the §C10.2b products table and drop the three conditionals (2.8% as a FWHM ellipse, ≈8% at 1/e²). If it does not, change §C0 subsection 10.8 to 'with a beam of at most 0.04° × 0.02° (width convention not stated)'.

## R5_C10_part1-08 [09_C10_part1] follow-up #5 (part)

- **Where:** §C10.2b products table, FS-4S row 'C+L band' and SR-1S row
- **What is needed:** State which laser each datasheet names (RAY-H1 or another source). The derivation for both lasers is applied as an edit.

## R5_C10_part1-09 [09_C10_part1] follow-up #8

- **Where:** Appendix 2, 'Analog Photonics FS-4S / SR-1S / RAY-H1 / FSOC-B1 datasheets (2025):' followed by three URLs only
- **What is needed:** Add the FSOC-B1 datasheet URL with its revision and date, or drop 'FSOC-B1' from that entry. Until then the §C10.2b FSOC-B1 row and the loss mention in finding 4 carry [U] (applied as edits).

## R5_C10_part1-10 [09_C10_part1] follow-up #12 (part)

- **Where:** §C10.2b device table, 'Analog Photonics "super-cell" (CLEO 2023) [I, abstract] | >49,152 over **four reticles**'
- **What is needed:** Whether the abstract gives exactly 49,152 elements (24 × 2,048) or more. Finding 1 was aligned with the table's '>49,152'; if the count is exact, change both to '49,152'.
