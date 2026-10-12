"""Estimate lidar-equipped Chinese-brand passenger cars sold outside China in 2025 (cars and lidar units).

Purpose
    Bottom-up, channel-by-channel estimate for report section B5 (row "Chinese-brand exports
    with lidar"). Each channel = cars sold outside China x share of those cars fitted with
    lidar x lidar units per fitted car. Low / central / high inputs are listed with their
    evidence tag: measured inputs carry [P], [I], [T] or [MR]; everything else is a judgement [E].
    Two totals are printed: (1) the plain sum of all lows / centrals / highs (extreme bounds,
    every input at the same extreme at once) and (2) a Monte Carlo P10/P50/P90 with independent
    triangular distributions per input (a more realistic spread; independence is itself an
    assumption).

Inputs
    None (all inputs are in the CHANNELS table below, with sources in the comments).
    Optional command-line argument: number of Monte Carlo draws (default 200000).

Outputs
    Printed table and totals.

Date: 2026-10-03
"""
import sys
import numpy as np

# name, volume (low, central, high), lidar share (low, central, high), units per fitted car
# (low, central, high), basis
CHANNELS = [
    ("NIO brand (Europe official, MENA official, Russia grey)",
     (1195, 1535, 2056), (1.0, 1.0, 1.0), (1, 1, 1),
     "Europe 5 core markets 1,129 [T, official registrations compiled]; Russia 66 [MR]; "
     "BE/PT and UAE/other markets judged 0-860 [E]. EU and UAE spec pages list one LiDAR [P]. "
     "Firefly (no lidar) excluded."),
    ("Lotus Eletre/Emeya (China-built) outside China",
     (1592, 1650, 1742), (0.20, 0.45, 0.70), (2, 3, 4),
     "Lifestyle deliveries 4,552 minus China deliveries 2,960 (less 0-150 sports cars in China) "
     "[P via results release]; UK Lidar Pack is a GBP 4,250 option [T]; 2 AT128 main units, "
     "up to 2 more wing units [T/S]; take rate unknown [E]."),
    ("Zeekr official overseas + Russia grey",
     (15811, 21811, 33811), (0.10, 0.25, 0.45), (1, 1, 1),
     "Russia 3,811 registrations [MR]; other overseas 12k/18k/30k judged from 15k cumulative "
     "overseas by Jan 2025 [T] and 2025 expansion [E] (NL alone 1,653 [I, RDW]). Global 7X page "
     "lists 1 LiDAR [P]; EU 7X page lists none and AU lidar 'not yet confirmed' [T]; 001/X/009 "
     "exports mostly pre-lidar versions [E]."),
    ("Li Auto (grey; official from Q4 2025)",
     (18088, 23088, 31088), (0.70, 0.85, 0.95), (1, 1, 1),
     "Russia 13,088 registrations [MR]; other destinations 5k/10k/18k [E] scaled from the CEO's "
     "~3,000/month (early 2024) and 30k+ in 2023 [T]. L-series lidar standard on all trims from "
     "the May 2025 refresh [T]; before that Max/Ultra only, >70% of L7/L8 buyers took AD Max [T]."),
    ("Aito/Seres (official ME + grey CIS)",
     (3380, 5380, 8380), (0.50, 0.70, 0.90), (1.0, 1.2, 1.5),
     "Russia 2,380 [MR]; other 1k/3k/6k [E]; M8/M9 standard lidar, M5/M7 on upper trims [E]."),
    ("Xiaomi (grey only)",
     (1000, 1410, 2000), (0.50, 0.70, 0.90), (1, 1, 1),
     "Russia 705 [MR]; Russia ~50% of SU7 parallel exports [S]; YU7 standard lidar, "
     "SU7 Pro/Max lidar [E]."),
    ("Lynk & Co 900 (Russia)",
     (1437, 1916, 2156), (0.90, 1.00, 1.00), (1, 1, 1),
     "Lynk & Co Russia 2,395, growth attributed to the 900 [MR]; 900 share 60/80/90% [E]; "
     "900 has a roof LiDAR as standard in China [T]; Russia-bound cars assumed China spec [E]."),
    ("Avatr (official Russia, SE Asia, ME)",
     (2261, 4261, 7261), (0.00, 0.20, 0.50), (1, 1.5, 2),
     "Russia 1,261 [MR]; other 1k/3k/6k [E]; export-trim lidar not verified [E]."),
    ("Denza + Yangwang (official + grey)",
     (1781, 3781, 6781), (0.05, 0.15, 0.35), (1, 2, 3),
     "Russia Denza 733 + Yangwang 48 [MR]; other 1k/3k/6k [E]; D9 exports mostly without "
     "lidar; Z9 GT/N9/U8 multi-lidar [E]."),
    ("BYD God's Eye A/B trims abroad",
     (0, 500, 3000), (1.0, 1.0, 1.0), (1, 1.2, 1.5),
     "Judgement only [E]; BYD exported ~1.01 M cars in 2025 [T], almost all non-lidar trims."),
    ("Xpeng lidar trims abroad (G9 etc.)",
     (0, 300, 1500), (1.0, 1.0, 1.0), (1, 2, 2),
     "Judgement only [E]; EU G9 pages (NL, DE) and the global G9 page list no LiDAR [P, absence]; "
     "NL registered 358 G9 and 1,042 G6 in 2025 [I, RDW]."),
    ("Other (Voyah, Hongqi, Hyptec, Exeed, Wey/Tank, HIMA brands, Leapmotor, IM/MG, Polestar 3 "
     "China-built, HiPhi, Onvo)",
     (300, 1500, 5000), (1.0, 1.0, 1.0), (1, 1.2, 1.5),
     "Judgement only [E]; e.g. Voyah 9,459 and Hongqi 10,002 Russian registrations [MR] are "
     "assumed almost entirely non-lidar."),
]


def deterministic():
    rows, tot_c, tot_u = [], np.zeros(3), np.zeros(3)
    for name, vol, share, upc, basis in CHANNELS:
        cars = np.array(vol, float) * np.array(share, float)
        units = cars * np.array(upc, float)
        tot_c += cars
        tot_u += units
        rows.append((name, vol, share, upc, cars, units, basis))
    return rows, tot_c, tot_u


def tri(rng, lo, mode, hi, n):
    if hi <= lo:
        return np.full(n, float(lo))
    mode = min(max(mode, lo), hi)
    return rng.triangular(lo, mode, hi, n)


def montecarlo(n):
    rng = np.random.default_rng(20261003)
    cars = np.zeros(n)
    units = np.zeros(n)
    for name, vol, share, upc, basis in CHANNELS:
        v = tri(rng, *vol, n)
        s = tri(rng, *share, n)
        u = tri(rng, *upc, n)
        cars += v * s
        units += v * s * u
    return np.percentile(cars, [10, 50, 90]), np.percentile(units, [10, 50, 90])


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    rows, tot_c, tot_u = deterministic()
    print("Chinese-brand lidar cars sold outside China, 2025 (low / central / high)\n")
    for name, vol, share, upc, cars, units, basis in rows:
        print(f"- {name}")
        print(f"    cars sold outside China {vol[0]:>6,} / {vol[1]:>6,} / {vol[2]:>6,}; "
              f"lidar share {share[0]:.2f} / {share[1]:.2f} / {share[2]:.2f}; "
              f"units per fitted car {upc[0]} / {upc[1]} / {upc[2]}")
        print(f"    lidar cars {cars[0]:>7,.0f} / {cars[1]:>7,.0f} / {cars[2]:>7,.0f}; "
              f"lidar units {units[0]:>7,.0f} / {units[1]:>7,.0f} / {units[2]:>7,.0f}")
        print(f"    basis: {basis}")
    print("\nSum of extremes (all inputs low / central / high together):")
    print(f"  lidar cars  {tot_c[0]:,.0f} / {tot_c[1]:,.0f} / {tot_c[2]:,.0f}")
    print(f"  lidar units {tot_u[0]:,.0f} / {tot_u[1]:,.0f} / {tot_u[2]:,.0f}")
    pc, pu = montecarlo(n)
    print(f"\nMonte Carlo ({n:,} draws, independent triangular inputs) P10 / P50 / P90:")
    print(f"  lidar cars  {pc[0]:,.0f} / {pc[1]:,.0f} / {pc[2]:,.0f}")
    print(f"  lidar units {pu[0]:,.0f} / {pu[1]:,.0f} / {pu[2]:,.0f}")
    # Share of the central estimate carried by measured-volume channels with judged shares
    li = [r for r in rows if r[0].startswith("Li Auto")][0][4][1]
    print(f"\nLi Auto share of central lidar cars: {li / tot_c[1]:.0%}")
    print("Report baseline (section B5): 15-60k cars, central 25-35k.")


if __name__ == "__main__":
    main()
