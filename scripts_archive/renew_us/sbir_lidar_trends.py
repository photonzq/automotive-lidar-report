"""Lidar-relevant SBIR/STTR awards by fiscal year, from SBIR.gov's bulk award file.

Purpose
    Selects lidar-relevant SBIR/STTR awards (FY2005-FY2026) from the SBIR.gov award
    database with abstracts, flags subsets (FMCW/coherent, photonic-integrated,
    single-photon/Geiger-mode), assigns an application class and an agency/branch
    label by keyword rules, and writes year, agency, application and recipient tables.

Selection rule (automatic, not manually reviewed)
    "match"  : title or abstract contains lidar/ladar in any spelling or compound
               (regex l[ai]dar, case-insensitive), "laser radar", "light/laser
               detection and ranging", or "laser altimeter/altimetry".
    "core"   : a match whose title carries the term, or whose title+abstract carry
               two or more mentions. Single passing mentions in the abstract only
               ("cameras, radar and lidar") are kept in the match set but not in core.
    Conditional terms (FMCW without lidar, optical phased array without lidar,
    Geiger-mode, SPAD/ToF with depth, frequency comb with ranging, laser
    rangefinder) are counted separately as an unreviewed borderline pool.

Inputs
    <data_dir>/award_data_current.csv : SBIR.gov award file with abstracts
        (https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv).
Outputs (in <out_dir>)
    sbir_lidar_awards.csv            award-level matches with flags and classes
    sbir_lidar_by_year.csv           counts and dollars by award (fiscal) year
    sbir_lidar_by_agency.csv         core set by agency/branch and period
    sbir_lidar_by_application.csv    core set by application class and period
    sbir_lidar_top_recipients.csv    top firms by core dollars, two periods
    sbir_lidar_borderline_pool.csv   conditional-term awards without a lidar term

Usage:
    python sbir_lidar_trends.py <data_dir> <out_dir>
"""
import os
import re
import sys

import pandas as pd

YEARS = range(2005, 2027)


def norm_company(x):
    x = re.sub(r"[^A-Z0-9 &]", " ", str(x).upper())
    x = re.sub(r"\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LP|PLLC|DBA.*)\b", " ", x)
    return re.sub(r"\s+", " ", x).strip()


def agency_label(row):
    ag, br = row["Agency"], row["Branch"]
    if ag == "Department of Defense":
        m = {"Air Force": "DoD-Air Force", "Navy": "DoD-Navy", "Army": "DoD-Army",
             "Defense Advanced Research Projects Agency": "DoD-DARPA",
             "Missile Defense Agency": "DoD-MDA", "Special Operations Command": "DoD-SOCOM",
             "Office of the Secretary of Defense": "DoD-OSD",
             "National Geospatial-Intelligence Agency": "DoD-NGA",
             "Space Development Agency": "DoD-SDA"}
        return m.get(br, "DoD-other")
    if ag == "Department of Commerce":
        return {"National Oceanic and Atmospheric Administration": "DOC-NOAA",
                "National Institute of Standards and Technology": "DOC-NIST"}.get(br, "DOC-other")
    m = {"National Aeronautics and Space Administration": "NASA", "Department of Energy": "DOE",
         "National Science Foundation": "NSF", "Department of Transportation": "DOT",
         "Department of Homeland Security": "DHS", "Department of Agriculture": "USDA",
         "Department of Health and Human Services": "HHS", "Environmental Protection Agency": "EPA"}
    return m.get(ag, "other")


APPS = [  # first match wins; keyword classification, not reviewed
    ("atmospheric", r"wind|aerosol|atmospher|(?<!point )(?<!point-)clouds?\b|differential absorption|\bDIAL\b|"
                    r"water vapou?r|ozone|\bCO2\b|carbon dioxide|methane|greenhouse|boundary layer|turbulen|"
                    r"air quality|meteorolog|weather"),
    ("space/planetary", r"planetary|lunar|\bmoon\b|\bmars\b|asteroid|comet|lander|landing|descent|rendezvous|"
                        r"docking|spacecraft|on-orbit|satellite servicing|cubesat|smallsat"),
    ("automotive/ground vehicles", r"automotive|autonomous (?:car|vehicle|driving)|self-driving|\bADAS\b|"
                                   r"ground vehicle|\bUGV|unmanned ground|convoy|traffic|highway|\bcars?\b"),
    ("defence/ISR/targeting/C-UAS", r"target|\bISR\b|surveillance|reconnaissance|missile|seeker|munition|"
                                    r"weapon|counter-?(?:UAS|drone|sUAS)|battlefield|warfighter|soldier|combat|"
                                    r"threat|interceptor|kill vehicle|camouflage|foliage|obscur|\bATR\b"),
    ("mapping/bathymetry/forestry", r"bathymetr|mapping|topograph|terrain|forest|vegetation|canopy|survey|"
                                    r"geospatial|elevation|coastal|shoreline|underwater|seafloor|hydrograph|"
                                    r"agricultur|\bcrops?\b"),
    ("robotics/industrial", r"robot|industrial|manufactur|inspection|warehouse|factory|metrology|construction|"
                            r"\bUAVs?\b|drone|unmanned aerial|navigation"),
]

FLAG_FMCW = (r"FMCW|frequency[\s-]modulated[\s-]continuous|coherent[\s-]+(?:lidar|ladar|detection|receiver|doppler|"
             r"laser[\s-]+radar)|heterodyne|homodyne|doppler[\s-]+(?:lidar|ladar)|chirped[\s-]+(?:lidar|ladar|laser)")
FLAG_PIC = (r"optical[\s-]+phased[\s-]+arrays?|photonic[\s-]+phased[\s-]+array|photonic[\s-]+integrated|"
            r"integrated[\s-]+photonic|silicon[\s-]+photonic|silicon[\s-]+nitride|\bPICs?\b|"
            r"l[ai]dar[\s-]+on[\s-]+(?:a[\s-]+)?chip|chip[\s-]+scale[\s-]+l[ai]dar|photonic[\s-]+chip")
FLAG_SPC = r"single[\s-]photon|photon[\s-]counting|geiger|\bSPADs?\b|GM-?APD"


def main(data_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    c = pd.read_csv(os.path.join(data_dir, "award_data_current.csv"), dtype=str,
                    keep_default_na=False, encoding="utf-8")
    c["AY"] = pd.to_numeric(c["Award Year"], errors="coerce")
    c["amt"] = pd.to_numeric(c["Award Amount"].str.replace(",", ""), errors="coerce").fillna(0.0)
    s = c[c["AY"].between(min(YEARS), max(YEARS))].copy()
    T = s["Award Title"].fillna("")
    A = s["Abstract"].fillna("")
    txt = T + " || " + A
    strong = r"l[ai]dar|laser[\s-]+radar|light detection and ranging|laser detection and ranging|laser[\s-]+altimet"
    s["n_terms"] = txt.str.count("(?i)" + strong)
    s["title_term"] = T.str.contains(strong, case=False, regex=True)
    s["match"] = s["n_terms"] > 0
    s["core"] = s["match"] & (s["title_term"] | (s["n_terms"] >= 2))
    s["fmcw_coherent"] = txt.str.contains(FLAG_FMCW, case=False, regex=True)
    s["photonic_integrated"] = txt.str.contains(FLAG_PIC, case=False, regex=True)
    s["single_photon"] = txt.str.contains(FLAG_SPC, case=False, regex=True)
    app = pd.Series("other", index=s.index)
    done = pd.Series(False, index=s.index)
    for name, pat in APPS:
        hit = txt.str.contains(pat, case=False, regex=True) & ~done
        app[hit] = name
        done |= hit
    s["application"] = app
    s["agency_label"] = s.apply(agency_label, axis=1)
    s["phase2b_text"] = txt.str.contains(r"phase\s*II[\s-]?B\b|phase\s*IIb|phase\s*2b|sequential phase II|"
                                         r"phase II enhancement", case=False, regex=True)
    s["company_norm"] = s["Company"].map(norm_company)

    # borderline pool: conditional terms without any strong term
    cond = {
        "fmcw_optical": txt.str.contains(r"\bFMCW\b", case=False) & txt.str.contains(r"laser|optical|photonic", case=False),
        "optical_phased_array": txt.str.contains(r"optical[\s-]+phased[\s-]+array", case=False),
        "geiger_mode": txt.str.contains(r"geiger[\s-]mode", case=False),
        "spad_or_tof_depth": txt.str.contains(r"\bSPADs?\b|single[\s-]photon[\s-]avalanche|time[\s-]of[\s-]flight", case=False)
                             & txt.str.contains(r"depth|3[\s-]?D\b|\brang(?:e|ing)\b", case=False)
                             & ~txt.str.contains(r"mass[\s-]spectr|TOF[\s-]?MS|\bSIMS\b|neutron|positron|\bPET\b|ultrason", case=False),
        "comb_ranging": txt.str.contains(r"frequency[\s-]combs?|microcombs?|dual[\s-]comb", case=False)
                        & txt.str.contains(r"\brang(?:e|ing)\b|distance", case=False),
        "laser_rangefinder": txt.str.contains(r"laser[\s-]+rang(?:ing|efind|e[\s-]+find)", case=False),
    }
    bp = pd.DataFrame(cond)
    bp = bp[~s["match"]]
    bp = bp[bp.any(axis=1)]
    pool = s.loc[bp.index, ["Award Year", "Company", "Award Title", "Agency", "Branch", "Phase", "Program", "amt"]].join(bp)
    pool.to_csv(os.path.join(out_dir, "sbir_lidar_borderline_pool.csv"), index=False)

    m = s[s["match"]]
    cols = ["Award Year", "AY", "Agency", "Branch", "agency_label", "Phase", "Program", "Company", "company_norm",
            "Award Title", "amt", "Contract", "Agency Tracking Number", "Topic Code", "Proposal Award Date",
            "n_terms", "title_term", "core", "fmcw_coherent", "photonic_integrated", "single_photon",
            "application", "phase2b_text"]
    m[cols].to_csv(os.path.join(out_dir, "sbir_lidar_awards.csv"), index=False)

    # year table
    tot = s.groupby("AY").agg(all_sbir_n=("amt", "size"), all_sbir_usd=("amt", "sum"))
    out = [tot]

    def block(df, tag):
        g = df.groupby("AY").agg(n=("amt", "size"), usd=("amt", "sum"))
        g.columns = [f"{tag}_n", f"{tag}_usd"]
        return g

    core = s[s["core"]]
    out.append(block(m, "match"))
    out.append(block(core, "core"))
    out.append(block(core[core["Phase"] == "Phase I"], "core_ph1"))
    out.append(block(core[core["Phase"] == "Phase II"], "core_ph2"))
    out.append(block(core[core["Program"] == "STTR"], "core_sttr"))
    out.append(block(core[core["fmcw_coherent"]], "core_fmcw"))
    out.append(block(core[core["photonic_integrated"]], "core_pic"))
    out.append(block(core[core["single_photon"]], "core_spc"))
    out.append(block(core[core["agency_label"].str.startswith("DoD")], "core_dod"))
    out.append(block(core[core["agency_label"] == "NASA"], "core_nasa"))
    y = pd.concat(out, axis=1).fillna(0)
    y["core_share_of_sbir_usd_pct"] = 100 * y["core_usd"] / y["all_sbir_usd"]
    y.index.name = "award_year"
    y.to_csv(os.path.join(out_dir, "sbir_lidar_by_year.csv"))

    def period(ay):
        if 2005 <= ay <= 2009:
            return "2005-09"
        if 2010 <= ay <= 2014:
            return "2010-14"
        if 2015 <= ay <= 2019:
            return "2015-19"
        if 2020 <= ay <= 2022:
            return "2020-22"
        if 2023 <= ay <= 2025:
            return "2023-25"
        return "2026 (partial)"

    core = core.assign(period=core["AY"].map(period))
    ag = core.pivot_table(index="agency_label", columns="period", values="amt", aggfunc=["size", "sum"], fill_value=0)
    ag.to_csv(os.path.join(out_dir, "sbir_lidar_by_agency.csv"))
    ap = core.pivot_table(index="application", columns="period", values="amt", aggfunc=["size", "sum"], fill_value=0)
    ap.to_csv(os.path.join(out_dir, "sbir_lidar_by_application.csv"))

    rows = []
    for lab, lo, hi in (("2005-2025", 2005, 2025), ("2020-2025", 2020, 2025)):
        d = core[core["AY"].between(lo, hi)]
        g = d.groupby("company_norm").agg(n=("amt", "size"), usd=("amt", "sum"),
                                          name=("Company", "first")).sort_values("usd", ascending=False).head(25)
        g["period"] = lab
        rows.append(g.reset_index())
    pd.concat(rows).to_csv(os.path.join(out_dir, "sbir_lidar_top_recipients.csv"), index=False)

    with pd.option_context("display.width", 250, "display.max_columns", 40):
        print(y[["all_sbir_usd", "match_n", "match_usd", "core_n", "core_usd", "core_ph1_n", "core_ph2_n",
                 "core_ph2_usd", "core_fmcw_n", "core_fmcw_usd", "core_pic_n", "core_pic_usd", "core_spc_n",
                 "core_spc_usd", "core_dod_usd", "core_nasa_usd", "core_share_of_sbir_usd_pct"]].round(0))
        print(ag)
        print(ap)
        print(pd.concat(rows).to_string())
        print("borderline pool size:", len(pool), pool[list(cond)].sum().to_dict())
        print("phase II-B text flags in core:", int(core["phase2b_text"].sum()))
        print("core Phase II awards above 1.5 M USD:", int(((core["Phase"] == "Phase II") & (core["amt"] > 1.5e6)).sum()))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
