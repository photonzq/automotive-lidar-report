### From phone SPAD to lidar: IMX611, the AS-DT1 and the automotive parts

**Short answer.** The IMX611's SPADs are lidar-grade, with the same 10.08 µm pitch and stacked process as the automotive IMX459/479. A lidar built on it is limited by the photon budget, collection area, histogram depth and qualification, not by the SPAD. Sony has built exactly this: the AS-DT1, a 40 m sensor that keeps only 576 points.

| | IMX611 (phone receiver chip) | AS-DT1 (Sony industrial lidar module) | IMX459 / IMX479 (automotive receiver chips) |
|---|---|---|---|
| **SPADs** | 140 × 170 (23,800) at 10.08 µm; ≈2.4 mm² array, 2.2 mm diagonal [P] | Sensor model not disclosed | 597 × 168 / 105 × 1,568 at 10.08 µm; ≈10 / ≈16.7 mm² active (tables above) |
| **Depth output** | On-chip "distance signal processing" [P] | 576 points (24 × 24); horizontal field "30° or more"; 30 fps, or 15 fps in maximum-range mode [P/T] | 192 / 520 lines with a one-axis scanner |
| **Wavelength, PDE** | 940 nm, 28% | 940 nm | 905 nm, 24% / 940 nm, 37% |
| **Range** | 8 m specification point, indoors [P] | 40 m indoors and 20 m outdoors at 50% reflectivity. Accuracy at 10 m "±5 cm" on Sony's page (some press reports give ±5 mm); distance resolution ≈2–2.5 cm; outdoor operation to 100 klx [P/T] | 300 m claims |
| **Power** | 110 mW sensor, 160 mW system at 8 m [P] | ≈350 mW for the module [T] | ≈1.2 W (IMX459 development chip) |
| **Qualification** | Consumer | Industrial: drones, AMRs, service robots | AEC-Q100 Grade 2, ASIL-B(D) |
| **Price** | ¥1,000 sample | Not published; availability Spring 2026 [T] | ¥15,000 / ¥35,000 samples |

**Where the 576 points may come from.** 24 × 24 = 576 resembles the 576-dot pattern reported for Apple's 2020 LiDAR, a 64-emitter VCSEL behind a 3 × 3 diffractive splitter [U]. Whether the AS-DT1 uses an IMX611-class sensor is not disclosed [U]. The estimates below assume an IMX611-class array, to show the mechanism [E].

**Points cost range.** At fixed laser energy per frame $E$, each point receives $E/N_{\rm points}$, whether the light is flooded, projected as dots or scanned. When the signal limits range, $R\propto\sqrt{E/N_{\rm points}}$, so $N_{\rm points}R^2$ is roughly constant. Anchored on Sony's 40 m (indoors, 50%, 15 fps):

| Grouping on a 140 × 170 array | Depth points | Points/s at 15 fps | Indoor range at 50% [E] |
|---|---|---|---|
| ≈6 × 7 SPADs per point (AS-DT1) | 576 | 8,640 | 40 m (Sony) |
| 3 × 3, Sony's minimum dToF pixel on the IMX479 | ≈2,576 | ≈38,600 | ≈19 m |
| One SPAD per point | 23,800 | 357,000 | ≈6 m, near the IMX611's 8 m phone point |

- **The native array is not a real alternative.** At 10 Hz it would give ≈0.24 Mpts/s, like a Livox Mid-360, but only at phone range. A single SPAD is also not a usable depth pixel (dead time, too few photons), which is why Sony's automotive parts start at 3 × 3.
- **Outdoors, binning helps less.** When sunlight limits range, a larger macro-pixel also collects more background, and range grows only as $N_{\rm points}^{-1/4}$, unless the chip reads only the SPADs a dot falls on.
- **The AS-DT1 at 10% reflectivity outdoors** would reach ≈9–13 m [E]: its 20 m at 50%, scaled as $\rho^{1/2}$ to $\rho^{1/4}$.

**Why about 6 × 6 SPADs per point** [E]:
1. **Range.** Sony itself groups 6 × 6 for the IMX459's 300 m mode (3 × 3 gives its 192 lines). Dividing the IMX611's array into 24 × 24 gives $140/24\times170/24\approx6\times7$, the same long-range grouping.
2. **Sunlight and dead time.** At 100 klx each SPAD counts background at a high rate and is blind for several to 15 ns after each count (IMX560: 15 ns typical). Several SPADs per point avoid blinding and allow coincidence detection.
3. **Parallax.** A dot's image shifts on the sensor by $\Delta x=f\,b/R$. With $f\approx3.2$ mm (30° across 1.71 mm) and an assumed 10 mm baseline, the shift is 64 µm (≈6 SPADs) at 0.5 m, 16 µm at 2 m and 3 µm at 10 m. Each dot needs a strip about 6 SPADs long just to be caught at close range.
4. **Histogram memory.** 40 m needs a 267 ns window, or ≈2,000 bins at 2 cm.
   - At 12 bits per bin, 576 points need ≈14 Mbit; 23,800 points would need ≈570 Mbit.
   - At an assumed ≈0.13 µm² per 28 nm SRAM bit-cell, even 14 Mbit is ≈1.7 mm², comparable to the whole 2.4 mm² pixel array.
   - Real chips use coarse-then-fine histogramming [U].

**Against imaging radar** (§E2):
- **Matched window.** Over ≈30° × 30°, the AS-DT1's 576 points (≈1.25° pitch, 24 lines) compare with a high-end radar's ≈450–1,800 cells.
- **Fill and footprint.** Nearly every lidar point is a valid return from a diffuse surface, and its narrow beamlet fixes the angle; most radar cells are empty or clutter (a car gives ≈3–10 points).
- **Range precision is similar,** a few centimetres for both.
- **The radar covers far more:** ±60° to 200–300 m, with Doppler and weather robustness.
- **Both miss thin objects** that fall between samples.
- **What the AS-DT1 is:** a precise multipoint ranger for drones and AMRs, competing with ultrasonics, stereo and ToF cameras. Phones densify the same kind of sparse depth by fusing it with the RGB camera.

**What a real lidar adds** (range-weighted point rate, §C3b). A Mid-360 delivers about 300× the AS-DT1's points/s × $R^2$, and an AT128 or ATX about 10⁵×. That margin comes from:
- **watts of laser:** 6.5–13.5 W against ≈0.35 W for the whole AS-DT1;
- **scanning,** which shortens the dwell per direction against sunlight and relaxes Class 1 with a moving beam;
- **collection area:** the IMX459/479 arrays are 4–7× the IMX611's, and shaped as lines for one-axis scanners;
- **deeper histograms** (300 m needs a 2 µs window) and automotive qualification.

**Sony's phone SPAD becomes an automotive lidar sensor by changing everything around the pixel, not the pixel.**

Sources: https://www.sony-semicon.com/en/news/2023/2023030601.html ; https://www.image-sensing-solutions.eu/AS-DT1_feature.html ; https://pro.sony/ue_US/products/lidar/as-dt1 ; https://www.cnx-software.com/2025/04/23/sony-as-dt1-tiny-industrial-lidar-depth-sensor-can-operate-under-bright-conditions-up-to-100000-lux/ ; http://image-sensors-world.blogspot.com/2025/04/sony-releases-spad-based-depth-sensor.html
