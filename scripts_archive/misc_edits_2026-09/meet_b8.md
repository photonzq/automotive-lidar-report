**Where ToF cameras and robotics lidars meet** [E unless tagged].
- **Not in cars.** iToF does not compete with automotive lidar. A \$200 forward lidar such as the Hesai ATX (§C3c) must see ≈200 m in sunlight, which §C0 subsection 9 rules out for flood-lit iToF. Its rivals are cameras, 4D radar (§E2) and lidar-free trims.
- **At the robotics end.** Chinese robotics lidars also sell at about \$200 at volume: RoboSense's robotics revenue per unit is ≈RMB 1.5–1.7k (above), about \$210–240.

**The low-end ladder.** Costs and prices are not comparable, and single-unit retail prices run several times above OEM volume prices.

| Item | What it is | Principle | Useful range | Price or cost | Tag |
|---|---|---|---|---|---|
| ams TMF8821 / ST VL53L5 | Complete multizone module | SPAD dToF | ≈4 m | \$0.50 / \$0.60 manufacturing cost | [I] |
| ST VL53L8CX | Complete module, 8 × 8 zones | SPAD dToF | ≈4 m | \$3.60 in 1,000-unit trays | [T] |
| iPhone 15 Pro LiDAR | Complete dot-pattern module | SPAD dToF | ≈5 m | \$6.60 manufacturing cost | [I] |
| Sony IMX611 | Receiver chip only | SPAD dToF | 8 m specification point | ¥1,000 sample | [P] |
| ST VD55H1 | Receiver chip only | iToF, 0.54 MP | ≈5 m at full resolution | Not found | [T] |
| Arducam ToF camera | Complete camera | iToF, 940 nm | A few metres | \$29.99 (Kickstarter) | [T] |
| Orbbec Femto Bolt | Complete camera | iToF, 1 MP (Microsoft pixel) | "Optimized for indoor" | Not found | [T] |
| Robot-vacuum laser distance sensor (Camsense) | Complete spinning sensor | Mostly triangulation, with a rising dToF share | ≈8 m indoors | ASP RMB 43 (≈\$6) | [T] |
| Unitree L1 / L2 | Complete lidar | Spinning dToF | Tens of metres [U] | From \$249 / \$419 | [P] |
| Livox Mid-360 | Complete lidar | Non-repetitive-scan dToF | 40 m at 10% | ≈\$480–550 (resellers) | [T] |
| Hesai JT16 / JT128 | Complete lidar | Spinning dome dToF | JT128: 40 m at 10% | ≈\$745 / ≈\$1,120 single unit | [T] |
| RoboSense E1R | Complete lidar | Flash-type SPAD dToF (electronic scan) | 30 m at 10% | \$999 retail | [P] |
| Chinese robotics lidar at volume | — | dToF | — | ≈\$210–240 revenue per unit (RoboSense robotics) | [E] |

**By application:**

| Application | Need | What wins in 2026 | Is iToF the rival? |
|---|---|---|---|
| **Robot vacuums** | Indoors, <8 m, a 2D map | ≈\$6 spinning laser distance sensors; camera SLAM at the low end; structured light or ToF for front obstacles | Only for front obstacles |
| **Indoor AMRs and warehouses** | Safety-rated 2D scanning, 3D obstacles near the floor, SLAM in large halls | Certified 2D safety scanners; ToF or stereo cameras for obstacles; 3D lidar (Mid-360, JT128) for mapping | Yes, for obstacles within a few metres |
| **Humanoids** | 360° navigation plus close-range manipulation | Lidar domes for navigation (JT128, Mid-360); stereo or ToF cameras for the hands (Unitree G1: Mid-360 plus RealSense D435i) | Complementary |
| **Robot mowers** | Outdoors, full sun, 20–100 m | Lidar (E1R, JT16) versus RTK plus vision versus vision-only (Husqvarna AI Vision; Lymow, NexLawn) [T] | No: sunlight excludes iToF, and the rival is camera AI |
| **Sidewalk delivery robots** | Outdoors, ≈1–10 m at walking pace | Starship: ToF cameras and radar; Serve and Avride: lidar (§B4a, subsection 4) | Yes |
| **Car exterior** | 200 m forward; parking at 0–5 m | dToF or FMCW against camera plus radar; for parking, ultrasonics and cameras against FTX/E1-class units (§B7) | No |

**Verdict** [E]:
- **iToF caps lidar prices from below, not the automotive lidar.** In robotics it is one of several cheaper depth options, and it wins mostly indoors within a few metres.
- **Camera AI is the biggest rival to low-end lidar:** stereo or learned monocular depth in camera-SLAM vacuums, vision-only mowers and camera-first delivery robots.
- **Consumer SPAD dToF is a narrower threat than it looks.** Sony's and ST's parts share lidar's physics (time gating, multiple echoes), but their module economics stop near 10 m.
  - Beyond that, the emitter and optics must grow roughly as $R^2$ (above). That is where lidar makers carry their automotive VCSEL and driver volume.
  - Consumer dToF therefore threatens lidar only in short-range indoor slots, where lidar is weak anyway.
- **Where Hesai and RoboSense are safe, and where they are not.** Robotics demand holds where range, sunlight or 360° coverage matter: mowers, outdoor delivery and humanoid navigation. The quarter-to-quarter volatility above shows how quickly a customer can switch to vision.
