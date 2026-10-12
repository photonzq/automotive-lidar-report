"""Robotics-lidar revenue, units and revenue per unit for RoboSense and Hesai.

Purpose
-------
Reproduces the [E] arithmetic behind the robotics-lidar answers for Appendix 1
of the automotive perception report (items "Robot lidar by type",
"Robotics revenue" and "ToF and robotics-lidar prices").

All inputs are typed in from the companies' own filings (HKEX announcements and
interim/annual reports, Hesai's HKEX-filed quarterly releases and its HKEX
prospectus of 8 Sep 2025). Each constant carries its source in a comment.
Units are lidar units; money is RMB unless stated.

Usage
-----
    python robotics_lidar_asp.py
"""

# ---------------------------------------------------------------- RoboSense
# Product revenue split "For ADAS" / "For robotics and others" (RMB thousand)
# and units (approximate, as reported).
RS = {
    # Q1 2025 results (HKEX, 30 May 2025), MD&A p. 9
    "Q1 2025": dict(adas_rev=228_887, rob_rev=73_403, adas_u=96_700, rob_u=11_900),
    # H1 2025 interim results (HKEX, 21 Aug 2025), MD&A p. 10 (six months)
    "H1 2025": dict(adas_rev=500_320, rob_rev=220_706, adas_u=None, rob_u=None),
    # 9M 2025 results (HKEX, 25 Nov 2025), MD&A p. 10 (three months to Sep 30)
    "Q3 2025": dict(adas_rev=244_705, rob_rev=142_429, adas_u=150_100, rob_u=None),
    # FY2025 annual results (HKEX, 25 Mar 2026), pp. 2, 4, 10
    "FY2025": dict(adas_rev=1_105_914, rob_rev=709_841, adas_u=609_000, rob_u=303_000),
}
RS_Q4_2025_UNITS = dict(adas_u=238_400, rob_u=221_200)       # FY2025 results p. 2
RS_Q4_2025_ROB_REV = 346_700                                 # FY2025 results p. 4 (RMB 346.7 M)
RS_Q4_ROB_QOQ = 6.231                                        # +523.1% QoQ (factor 6.231), FY2025 results p. 4
# 2026: product revenue is no longer split by application.
RS_2026 = {
    "Q1 2026": dict(prod_rev=441_123, adas_u=144_800, rob_u=185_500),  # Q1 2026 results p. 8, p. 1
    "Q2 2026": dict(prod_rev=516_880, adas_u=291_800, rob_u=97_100),   # H1 2026 results pp. 2, 13
}
RS_H1_2026_PROD_REV = 958_003      # H1 2026 interim results p. 9
RS_H1_2026_ROB_SHARE = (0.45, 0.50)  # "nearly half" of product revenue (H1 2026 results p. 6) -> assumed band

# ---------------------------------------------------------------- Hesai
HS_UNITS = {  # robotics lidar shipments (HKEX/6-K quarterly releases)
    "2024": 45_503, "Q2 2025": 48_531, "Q3 2025": 60_639, "Q4 2025": 80_372,
    "FY2025": 239_273, "Q1 2026": 118_282, "Q2 2026": 142_371,
}
HS_TOTAL_UNITS = {"FY2025": 1_620_406, "Q2 2026": 628_275}
HS_LIDAR_PRODUCT_REV_2025 = 2_973_300      # RMB thousand, 2025 annual report MD&A p. 20
HS_LIDAR_SEGMENT_REV_Q2_2026 = 815_884     # RMB thousand, Q2 2026 release, segment table
HS_ROBOTICS_REV_2024_USD = 0.09e9          # HK prospectus p. 208 (CIC ranking table, 16.2% share)
RMB_PER_USD_REPORT = 7.1                   # conversion rate used throughout the report


def k(x):
    return x * 1_000


def main():
    print("RoboSense, robotics-and-others revenue per unit (RMB):")
    q1 = RS["Q1 2025"]
    print(f"  Q1 2025: {k(q1['rob_rev']) / q1['rob_u']:,.0f}  (filing: ~6,200)")
    q2_rev = RS["H1 2025"]["rob_rev"] - q1["rob_rev"]
    q2_units = RS_2026["Q2 2026"]["rob_u"] / 2.823          # Q2 2026 = +182.3% YoY
    print(f"  Q2 2025: revenue {q2_rev:,} k over ~{q2_units:,.0f} units -> {k(q2_rev) / q2_units:,.0f}")
    q3_units = RS_Q4_2025_UNITS["rob_u"] / RS_Q4_ROB_QOQ
    print(f"  Q3 2025: {k(RS['Q3 2025']['rob_rev']) / q3_units:,.0f}  (units ~{q3_units:,.0f}; filing: ~4,000)")
    print(f"  Q4 2025: {k(RS_Q4_2025_ROB_REV) / RS_Q4_2025_UNITS['rob_u']:,.0f}")
    fy = RS["FY2025"]
    print(f"  FY2025 : {k(fy['rob_rev']) / fy['rob_u']:,.0f}  (filing: ~2,300)")
    q4_adas_rev = fy["adas_rev"] - RS["H1 2025"]["adas_rev"] - RS["Q3 2025"]["adas_rev"]
    print(f"RoboSense ADAS revenue per unit Q4 2025: {k(q4_adas_rev) / RS_Q4_2025_UNITS['adas_u']:,.0f}")
    print(f"Check: quarterly robotics revenue sum = {q1['rob_rev'] + q2_rev + RS['Q3 2025']['rob_rev'] + RS_Q4_2025_ROB_REV:,} k "
          f"vs FY {fy['rob_rev']:,} k")

    for q, v in RS_2026.items():
        units = v["adas_u"] + v["rob_u"]
        print(f"RoboSense {q}: product revenue per unit {k(v['prod_rev']) / units:,.0f}")
    h1_units_rob = sum(v["rob_u"] for v in RS_2026.values())
    h1_units_adas = sum(v["adas_u"] for v in RS_2026.values())
    for s in RS_H1_2026_ROB_SHARE:
        rob = s * k(RS_H1_2026_PROD_REV)
        adas = k(RS_H1_2026_PROD_REV) - rob
        print(f"  H1 2026 at {s:.0%}: robotics {rob / 1e6:,.0f} M -> {rob / h1_units_rob:,.0f}/unit; "
              f"ADAS {adas / 1e6:,.0f} M -> {adas / h1_units_adas:,.0f}/unit")
    at_q4 = h1_units_rob * k(RS_Q4_2025_ROB_REV) / RS_Q4_2025_UNITS["rob_u"]
    print(f"  H1 2026 robotics units at the Q4 2025 rate: {at_q4 / 1e6:,.0f} M = "
          f"{at_q4 / k(RS_H1_2026_PROD_REV):.1%} of product revenue")

    print("\nHesai:")
    print(f"  2024 robotics revenue per unit: US${HS_ROBOTICS_REV_2024_USD / HS_UNITS['2024']:,.0f}")
    print(f"  2025 lidar product revenue per unit: RMB {k(HS_LIDAR_PRODUCT_REV_2025) / HS_TOTAL_UNITS['FY2025']:,.0f}")
    print(f"  Q2 2026 lidar-segment revenue per unit: RMB {k(HS_LIDAR_SEGMENT_REV_Q2_2026) / HS_TOTAL_UNITS['Q2 2026']:,.0f}"
          f" (= US${k(HS_LIDAR_SEGMENT_REV_Q2_2026) / HS_TOTAL_UNITS['Q2 2026'] / RMB_PER_USD_REPORT:,.0f} at {RMB_PER_USD_REPORT})")
    q12025 = HS_UNITS["Q1 2026"] / 2.37   # Q1 2026 = +137% YoY (rounded in the release)
    print(f"  Q1 2025 robotics units implied: ~{q12025:,.0f}; H1 2025 = {HS_UNITS['FY2025'] - HS_UNITS['Q3 2025'] - HS_UNITS['Q4 2025']:,}")


if __name__ == "__main__":
    main()
