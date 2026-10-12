"""Classify USAspending.gov lidar transactions and tabulate obligations by fiscal year.

Purpose
    Reads the prime-transaction CSVs written by usasp_lidar_download.py (contracts from
    FPDS, assistance from FABS), keeps transactions whose own description or the award's
    base description contains a lidar term, and classifies each one:
      sbir_status  : SBIR/STTR Phase I/II (FPDS research codes SR1, SR2, ST1, ST2, or SBIR/STTR
                     wording in assistance descriptions), Phase III (SR3, ST3), or non-SBIR
      kind         : contracts -> rd (product/service code starting with A), data (architect-
                     engineering, mapping, surveying, aerial photography: C2xx, R404, T0xx),
                     equipment (numeric product codes), services (other letters);
                     assistance -> research (science, engineering, defence-research listings),
                     data (USGS National Map / geologic mapping / data-collection listings,
                     FEMA mapping), transport (DOT listings), other
      lidar_core   : lidar term in the first 200 characters of the base description, or two or
                     more mentions in the combined text (passing mentions are not core)
      coherent     : FMCW, coherent, Doppler or heterodyne wording
      integrated   : optical phased array, photonic integrated, silicon photonics, chip-scale
    Obligations are summed by the fiscal year of each transaction's action date.

    Known false positives removed: personal or product names that contain "ladar"
    (Ladarius, Ladarrian, Ladarola, the drug ladarixin, and the ophthalmic LADARVision and
    LADARWave systems).

Inputs
    data_dir : folder holding Contracts_PrimeTransactions_*.csv and Assistance_PrimeTransactions_*.csv
    out_dir  : folder for result CSVs
Outputs
    usasp_lidar_transactions.csv, usasp_lidar_by_fy.csv, usasp_lidar_agency_fy.csv,
    usasp_lidar_top_recipients.csv, usasp_lidar_phase3.csv, usasp_lidar_sbir_fy2026.csv

Usage:
    python usasp_lidar_analysis.py <data_dir> <out_dir>
"""
import glob
import os
import re
import sys

import pandas as pd

TERM = r"l[ai]dar|laser[\s-]+radar"
FALSE = r"ladarixin|ladarius|ladarrian|ladarola|ladarvision|ladarwave"
COH = r"FMCW|frequency[\s-]modulated|coherent|doppler|heterodyne|homodyne"
PIC = r"optical phased array|phased[\s-]array|photonic integrated|integrated photonic|silicon photonic|chip[\s-]scale|on[\s-]a[\s-]chip|\bPIC\b"


def agency_short(row):
    ag = str(row["awarding_agency_name"]).upper()
    sub = str(row["awarding_sub_agency_name"]).upper()
    if "DEFENSE" in ag or "WAR" in ag:
        for k, v in (("ARMY", "DoD-Army"), ("NAVY", "DoD-Navy"), ("AIR FORCE", "DoD-Air Force"),
                     ("ADVANCED RESEARCH PROJECTS", "DoD-DARPA"), ("MISSILE DEFENSE", "DoD-MDA"),
                     ("SPECIAL OPERATIONS", "DoD-SOCOM"), ("GEOSPATIAL", "DoD-NGA"),
                     ("LOGISTICS", "DoD-DLA"), ("SPACE DEVELOPMENT", "DoD-SDA")):
            if k in sub:
                return v
        return "DoD-other"
    for k, v in (("AERONAUTICS", "NASA"), ("ENERGY", "DOE"), ("SCIENCE FOUNDATION", "NSF"),
                 ("TRANSPORTATION", "DOT"), ("HOMELAND", "DHS"), ("AGRICULTURE", "USDA"),
                 ("INTERIOR", "DOI"), ("COMMERCE", "DOC"), ("ENVIRONMENTAL PROTECTION", "EPA")):
        if k in ag:
            if v == "DOI":
                return "DOI-USGS" if "GEOLOGICAL" in sub else "DOI-other"
            if v == "DOC":
                return "DOC-NOAA" if "OCEANIC" in sub else ("DOC-NIST" if "STANDARDS" in sub else "DOC-other")
            if v == "USDA":
                return "USDA-Forest Service" if "FOREST" in sub else "USDA-other"
            if v == "DHS":
                return "DHS-FEMA" if "EMERGENCY" in sub else "DHS-other"
            return v
    return "other"


def kind_contract(psc, text):
    psc = str(psc).upper()
    if psc.startswith("A"):
        return "rd"
    if psc.startswith("C2") or psc in ("R404", "R408") or psc.startswith("T0") or psc.startswith("B5"):
        return "data"
    if psc[:1].isdigit():
        return "equipment"
    if re.search(r"acqui\w* (?:of )?(?:new )?l[ai]dar|l[ai]dar (?:data )?(?:acquisition|collection|survey|mapping)|3DEP|topobath", text, re.I):
        return "data"
    return "services"


def kind_assist(cfda, text):
    cf = str(cfda)
    if cf in ("15.817", "15.810", "15.808", "15.073", "97.045", "97.039", "97.047", "10.902", "11.457"):
        return "data"
    if cf.startswith("20."):
        return "transport"
    if cf.startswith(("47.", "43.", "12.", "81.", "11.4", "11.6", "10.310", "10.200")):
        return "research"
    if re.search(r"acqui\w* (?:of )?l[ai]dar|l[ai]dar (?:data )?(?:acquisition|collection)|3DEP", text, re.I):
        return "data"
    return "other"


def load(data_dir):
    c = pd.read_csv(glob.glob(os.path.join(data_dir, "Contracts_PrimeTransactions*.csv"))[0], dtype=str, low_memory=False)
    a = pd.read_csv(glob.glob(os.path.join(data_dir, "Assistance_PrimeTransactions*.csv"))[0], dtype=str, low_memory=False)
    c["src"], a["src"] = "contract", "assistance"
    c["award_id"] = c["award_id_piid"]
    a["award_id"] = a["award_id_fain"]
    keep = ["src", "award_id", "action_date", "action_date_fiscal_year", "federal_action_obligation",
            "awarding_agency_name", "awarding_sub_agency_name", "recipient_name", "transaction_description",
            "prime_award_base_transaction_description"]
    c2 = c[keep + ["product_or_service_code", "product_or_service_code_description", "research_code", "research",
                   "parent_award_id_piid"]].copy()
    a2 = a[keep + ["cfda_number", "cfda_title", "assistance_type_description"]].copy()
    return pd.concat([c2, a2], ignore_index=True)


def main(data_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    d = load(data_dir)
    d["ob"] = pd.to_numeric(d["federal_action_obligation"], errors="coerce").fillna(0.0)
    d["fy"] = pd.to_numeric(d["action_date_fiscal_year"], errors="coerce")
    base = d["prime_award_base_transaction_description"].fillna("")
    text = d["transaction_description"].fillna("") + " || " + base
    clean = text.str.replace(FALSE, " ", case=False, regex=True)
    d["hit"] = clean.str.contains(TERM, case=False, regex=True)
    d = d[d["hit"]].copy()
    clean = clean[d.index]
    base = base[d.index]
    d["n_terms"] = clean.str.count("(?i)" + TERM)
    d["lidar_core"] = base.str[:200].str.contains(TERM, case=False, regex=True) | (d["n_terms"] >= 2)
    rc = d["research_code"].fillna("").str.upper()
    sb_text = clean.str.contains(r"\bSBIR\b|\bSTTR\b|SMALL BUSINESS INNOVATION|SMALL BUSINESS TECHNOLOGY TRANSFER", case=False, regex=True)
    d["sbir_status"] = "non-SBIR"
    d.loc[rc.isin(["SR1", "SR2", "ST1", "ST2"]) | ((d["src"] == "assistance") & sb_text), "sbir_status"] = "SBIR/STTR I-II"
    d.loc[(d["src"] == "contract") & ~rc.isin(["SR1", "SR2", "ST1", "ST2", "SR3", "ST3"]) & sb_text
          & clean.str.contains(r"PHASE I\b|PHASE II\b|PHASE 1\b|PHASE 2\b", case=False, regex=True), "sbir_status"] = "SBIR/STTR I-II"
    d.loc[rc.isin(["SR3", "ST3"]), "sbir_status"] = "Phase III"
    d["kind"] = [kind_contract(p, t) if s == "contract" else kind_assist(cf, t)
                 for s, p, cf, t in zip(d["src"], d["product_or_service_code"], d["cfda_number"], clean)]
    d["coherent"] = clean.str.contains(COH, case=False, regex=True)
    d["integrated"] = clean.str.contains(PIC, case=False, regex=True)
    d["agency"] = d.apply(agency_short, axis=1)
    d.to_csv(os.path.join(out_dir, "usasp_lidar_transactions.csv"), index=False)

    fy = d[d["fy"].between(2008, 2026)]

    def col(mask, name):
        g = fy[mask].groupby("fy")["ob"].sum() / 1e6
        g.name = name
        return g

    ns = fy["sbir_status"] == "non-SBIR"
    tab = pd.concat([
        col(fy["ob"].notna(), "all_$M"),
        col(fy["sbir_status"] == "SBIR/STTR I-II", "sbir12_$M"),
        col(fy["sbir_status"] == "Phase III", "phase3_$M"),
        col(ns, "nonsbir_$M"),
        col(ns & fy["lidar_core"], "nonsbir_core_$M"),
        col(ns & (fy["src"] == "contract") & (fy["kind"] == "rd"), "nonsbir_contract_rd_$M"),
        col(ns & (fy["src"] == "contract") & (fy["kind"] == "rd") & fy["lidar_core"], "nonsbir_contract_rd_core_$M"),
        col(ns & (fy["kind"] == "data"), "data_acq_$M"),
        col(ns & (fy["kind"] == "equipment"), "equipment_$M"),
        col(ns & (fy["src"] == "contract") & (fy["kind"] == "services"), "other_services_$M"),
        col(ns & (fy["src"] == "assistance") & (fy["kind"] == "research"), "assist_research_$M"),
        col(ns & (fy["src"] == "assistance") & (fy["kind"] == "research") & fy["lidar_core"], "assist_research_core_$M"),
        col(ns & (fy["src"] == "assistance") & (fy["kind"] == "transport"), "assist_transport_$M"),
        col(ns & fy["coherent"] & fy["lidar_core"], "nonsbir_coherent_core_$M"),
        col(ns & fy["integrated"] & fy["lidar_core"], "nonsbir_integrated_core_$M"),
        fy.groupby("fy").size().rename("n_transactions"),
        fy.groupby("fy")["award_id"].nunique().rename("n_awards"),
        fy[fy["src"] == "assistance"].groupby("fy")["transaction_description"].apply(lambda s: s.fillna("").str.len().median()).rename("assist_desc_median_chars"),
    ], axis=1).fillna(0)
    tab.index = tab.index.astype(int)
    tab.to_csv(os.path.join(out_dir, "usasp_lidar_by_fy.csv"))
    ag = fy[ns & fy["lidar_core"]].pivot_table(index="agency", columns="fy", values="ob", aggfunc="sum", fill_value=0) / 1e6
    ag.to_csv(os.path.join(out_dir, "usasp_lidar_agency_fy.csv"))
    rows = []
    for lab, lo, hi in (("FY2008-2026", 2008, 2026), ("FY2020-2026", 2020, 2026)):
        x = fy[ns & fy["lidar_core"] & fy["fy"].between(lo, hi)]
        g = x.groupby("recipient_name").agg(usd=("ob", "sum"), n=("award_id", "nunique"),
                                            agencies=("agency", lambda s: ";".join(s.value_counts().index[:3])),
                                            kinds=("kind", lambda s: ";".join(s.value_counts().index[:2])))
        g = g.sort_values("usd", ascending=False).head(25)
        g["period"] = lab
        rows.append(g.reset_index())
    pd.concat(rows).to_csv(os.path.join(out_dir, "usasp_lidar_top_recipients.csv"), index=False)
    p3 = d[d["sbir_status"] == "Phase III"].groupby(["award_id", "recipient_name", "agency"]).agg(
        usd=("ob", "sum"), first=("action_date", "min"), last=("action_date", "max"),
        desc=("prime_award_base_transaction_description", "first")).sort_values("usd", ascending=False)
    p3.to_csv(os.path.join(out_dir, "usasp_lidar_phase3.csv"))
    s26 = d[(d["fy"] == 2026) & (d["sbir_status"] == "SBIR/STTR I-II")]
    s26[["award_id", "action_date", "agency", "recipient_name", "research", "ob", "transaction_description"]].to_csv(
        os.path.join(out_dir, "usasp_lidar_sbir_fy2026.csv"), index=False)
    with pd.option_context("display.width", 250, "display.max_columns", 40, "display.max_colwidth", 90):
        print(tab.round(1))
        print(ag.round(1))
        print(pd.concat(rows).to_string())
        print(p3.head(30).to_string())
        print(p3.groupby(level="agency")["usd"].sum() / 1e6)
        print("Phase III total $M", round(p3["usd"].sum() / 1e6, 1), "awards", len(p3))
        print(s26[["award_id", "action_date", "agency", "recipient_name", "research", "ob"]].to_string())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
