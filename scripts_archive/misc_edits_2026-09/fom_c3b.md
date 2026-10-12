**Range-weighted point rate** [E]. Point rate alone misleads, because binning, ROI modes and dot patterns trade points against range.
- **The metric.** Points/s × (range at 10%)² tracks the photon budget a sensor delivers, since at fixed energy per frame $N_{\rm points}R^2$ is roughly constant (§C5a).
- **The caveat.** Conditions differ between spec sheets (sunlight, detection probability), so the table is order-of-magnitude only.

| Sensor | Points/s | Range at 10% | Points/s × R² (m²/s) | Power | Per watt |
|---|---|---|---|---|---|
| Sony AS-DT1 (576 points, 15 fps) | 8,640 | ≈11 m outdoors [E, from 20 m at 50%] | ≈1 × 10⁶ | ≈0.35 W (module) | ≈3 × 10⁶ |
| The same array at native grouping, same budget | ≈0.24–0.36 M | ≈2–4 m outdoors | ≈1–4 × 10⁶ | Same | Same |
| Livox Mid-360 | 200,000 | 40 m (100 klx) | 3.2 × 10⁸ | 6.5 W average | ≈5 × 10⁷ |
| Hesai JT128 | 1,152,000 | 40 m | 1.8 × 10⁹ | Not listed | — |
| Ouster OS1 Rev8 (1,024 × 10 Hz mode, single return) | 1,310,720 | 90 m (100 klx) | 1.1 × 10¹⁰ | Not taken here | — |
| Hesai AT128 | 1,536,000 | 210 m | 6.8 × 10¹⁰ | 13.5 W | ≈5 × 10⁹ |
| Hesai ATX | 3,840,000 | 230 m | 2.0 × 10¹¹ | 8 W (10 W typical in the user manual, §E9) | ≈2–2.5 × 10¹⁰ |

- **Binned and native are the same product.** Both AS-DT1 rows sit at ≈10⁶ m²/s: the 24 × 24 grouping redistributes the budget, it does not waste it.
- **The spread is five orders of magnitude.** Above the AS-DT1: ≈300× for a Mid-360, ≈10⁴× for an OS1, ≈10⁵× for an AT128 or ATX. Per watt the gap is ≈16× (Mid-360) to ≈10³–10⁴× (AT128, ATX). The rest comes from collection area, scanning and emitter efficiency (§C5a).
- **What the number omits.** It weights range but says nothing about angular resolution, small-object detection or velocity. Read it alongside the triplet check.
