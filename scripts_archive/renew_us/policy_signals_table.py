"""US federal policy signals on lidar, 2024-2026: a sourced table.

Purpose
    Writes the policy signals found for the US federal lidar-funding question (statutes,
    committee report language, rules and notices, executive orders, programme events), each
    with date, instrument, what it says about lidar, status, source URL and evidence tag
    (P primary, T trade press, S search summary, U unverified). Items already covered in the
    report's section D3 are marked "in D3" and are listed only where this work verified or
    extended them. Wording was read from rendered pages of the primary PDFs.

Inputs
    out_dir : output folder
Outputs
    policy_signals.csv

Usage:
    python policy_signals_table.py <out_dir>
"""
import csv
import os
import sys

ROWS = [
    ("2024-12-23", "FY2025 NDAA, P.L. 118-159, sec. 164 (138 Stat. 1818-1819)",
     "DoD may not operate or contract for covered lidar, or systems using it, from 30 Jun 2026; covered "
     "countries China, Iran, North Korea, Russia; Hesai named; exemption for intelligence, EW and testing; "
     "case-by-case waiver; defines lidar", "enacted (in D3; verified)",
     "https://www.govinfo.gov/content/pkg/PLAW-118publ159/pdf/PLAW-118publ159.pdf", "P"),
    ("2025-12-18", "FY2026 NDAA, P.L. 119-60, sec. 162 (139 Stat. 768-769)",
     "Amends sec. 164: covered lidar now defined by covered company, or software developed in, or "
     "connectivity/data storage located in, a covered country; DoD must publish a list of covered lidar "
     "companies in the Federal Register, assess contractor risk, consult contractors, and implement a "
     "mitigation strategy for contractors and subcontractors at any tier by 1 Jun 2027",
     "enacted (not in D3)", "https://www.govinfo.gov/content/pkg/PLAW-119publ60/pdf/PLAW-119publ60.pdf", "P"),
    ("2026-06-15", "H. Rept. 119-698 (HASC report on H.R. 8800, FY2027 NDAA), p. 71",
     "Item of special interest 'Advanced LIDAR Integration for Defense Systems': Air Force with Army to brief "
     "HASC by 1 Dec 2026 on lidar RDT&E, platform integration, transition, domestic industrial base and supply "
     "chain, and AFRL Rome's role", "report language (House-passed bill 22 Jul 2026 has no lidar section)",
     "https://rules.house.gov/sites/evo-subsites/republicans-rules.house.gov/files/documents/h-rept-119-698-fy27-ndaa-report-as-filed.pdf", "P"),
    ("2026", "H.R. 8800 (engrossed) and S. 4784 (SASC-reported), FY2027 NDAA bill texts",
     "no lidar term in either text", "bills pending",
     "https://www.govinfo.gov/content/pkg/BILLS-119hr8800eh/pdf/BILLS-119hr8800eh.pdf", "P"),
    ("2025-01-03", "BIS ICTS ANPRM, Unmanned Aircraft Systems, 90 FR (FR Doc. 2024-30209)",
     "Scope includes flight-control exteroceptive sensors; asks where UAS hardware such as lidar sensors is "
     "designed and made", "ANPRM; no proposed rule found",
     "https://www.govinfo.gov/content/pkg/FR-2025-01-03/html/2024-30209.htm", "P"),
    ("2025-06-06", "EO 14307 Unleashing American Drone Dominance; EO 14305 Restoring American Airspace Sovereignty",
     "Domestic drone industrial base and counter-UAS detection, tracking and identification; lidar and sensors "
     "not named", "executive orders",
     "https://www.govinfo.gov/content/pkg/FR-2025-06-11/pdf/2025-10814.pdf", "P"),
    ("2025-12-22", "FCC Covered List: foreign-produced UAS and UAS critical components (DA 25-1086)",
     "Critical components listed include cameras, gimbals, navigation systems, flight controllers; lidar not "
     "named in summaries", "in force; exemptions added Jan 2026",
     "https://www.hklaw.com/en/insights/publications/2025/12/fcc-adds-all-foreign-made-drones", "T"),
    ("2025-11-03", "Letter, Chairs Moolenaar, Mast, Crawford, Garbarino to Commerce Secretary",
     "Asks Commerce ICTS office to investigate adversary products in critical industries (connected cars, "
     "drones, solar named in release); letter text not read", "letter",
     "https://chinaselectcommittee.house.gov/media/press-releases/chairmen-moolenaar-mast-garbarino-and-crawford-ask-commerce-department-to-investigate-ccp-tied-tech-threats", "P"),
    ("2025-05", "Letter, Sen. Rick Scott and Rep. Moolenaar to SEC Chairman",
     "Calls for delisting of CCP-linked companies including Hesai", "letter",
     "https://www.rickscott.senate.gov/2025/5/sen-rick-scott-and-rep-moolenaar-lead-letter-to-sec-chairman-calling-for-delisting-of-ccp-linked-companies-on-u-s-stock-exchanges", "S"),
    ("2024-09-12", "Securing Infrastructure from Adversaries Act (Rep. Dusty Johnson, 118th Congress)",
     "Would bar DOT procurement, contracts and grants involving adversary lidar from 30 Jun 2026",
     "introduced, lapsed (House companion of the DOT ban in D3)",
     "https://dustyjohnson.house.gov/media/press-releases/johnson-legislation-protects-us-infrastructure-china", "P"),
    ("2025-09-30 to 2026-04-13", "SBIR/STTR authority lapse; S. 3971 Small Business Innovation and Economic Security Act",
     "Programmes lapsed 1 Oct 2025; reauthorized to 30 Sep 2031 when signed 13 Apr 2026 (Senate 3 Mar, House "
     "17 Mar 2026)", "enacted",
     "https://legacy.sba.gov/article/2026/04/13/administrator-loeffler-applauds-sbir-sttr-reauthorization", "P"),
    ("2024-02-22", "NASA Navigation Doppler Lidar on Intuitive Machines IM-1",
     "FMCW Doppler lidar used in the landing navigation; valid data beyond preflight range; NASA TM 2025",
     "flown", "https://ntrs.nasa.gov/citations/20250010290", "P"),
    ("search", "State laws restricting Chinese lidar", "none enacted found (searches 2026-10-03)", "none found",
     "", "S"),
    ("search", "Federal programme funding a domestic lidar industrial base",
     "none found; FY2026 NDAA sec. 162 is a risk-mitigation strategy, not funding; HASC FY2027 report asks for "
     "an industrial-base assessment briefing", "none found", "", "E"),
]


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "policy_signals.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "instrument", "lidar_content", "status", "url", "tag"])
        w.writerows(ROWS)
    print(len(ROWS), "rows written")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
