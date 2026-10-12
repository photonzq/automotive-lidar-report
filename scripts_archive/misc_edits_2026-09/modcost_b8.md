**What a complete phone dToF module costs** [I, Bonanno (Yole), ISSW 2024: reverse costing with stated inputs]. A SPAD chip is only the receiver. A working module adds a VCSEL and its driver, transmit and receive optics with a bandpass filter, a PCB and housing, assembly, and a final test that scraps failing modules.

| | iPhone 15 Pro LiDAR (all-Sony dies) | ST VL53L5 (multizone) | ams TMF8821 (multizone) |
|---|---|---|---|
| **Estimated manufacturing cost** | **\$6.60** | **\$0.60** | **\$0.50** |
| **Emitter** | VCSEL with 112 independently addressed cavities (12,650 µm²), an 8 × 14 dot pattern | 5-cavity VCSEL (1,150 µm²) | 33-cavity VCSEL (5,400 µm²) |
| **Receiver** | 116 × 92 SPADs at 10.1 µm; 90 nm SPAD wafer on 28 nm logic | 14 × 10 macro-pixels; 40 nm | 34 × 18; 55 nm high-voltage CMOS |
| **Module volume** | 235 mm³ | 29 mm³ | 13 mm³ |

- **Where the iPhone module's cost goes** [E, from the paper's inputs]:
  - SPAD die ≈\$0.69 (≈12% before test yield);
  - VCSEL plus driver ASIC ≈\$1.22 (≈21%);
  - other parts (lenses, filter, PCB, housing) \$3.00 (≈51%);
  - assembly \$1.00 (≈17%).

  A 90% final-test yield brings the total to \$6.60. **The SPAD chip is about a tenth of the module.**
- **Cost is not price.** The paper notes that supplier margins "can more than double" effective costs. ST's complete VL53L8CX (8 × 8 zones, with VCSEL, SPAD array and diffractive optics in one package) sells for \$3.60 in 1,000-unit trays [T, via Hackster].
- **Why range is expensive** [E]. For an extended target, signal per pixel scales as $E\,A_{\rm rx}\,\rho/R^2$, and sunlight does not fall with range.
  - Holding SNR from 8 m to 40 m needs ≈$25\times$ more energy-times-aperture; to 200 m it needs ≈$625\times$.
  - That growth lands on the emitter (multi-junction VCSEL arrays at tens to hundreds of watts peak, GaN drivers) and on the optics, the parts that already dominate the phone module's cost. Class 1 limits also force scanning or zoned illumination (§C4c, §C6).
  - **A \$1–7 phone module cannot do a robotics lidar's 30–60 m in sunlight by swapping in a better chip.** The chip platform transfers (Sony's automotive SPADs grew from its phone SPAD, §C5a); the module economics do not.
