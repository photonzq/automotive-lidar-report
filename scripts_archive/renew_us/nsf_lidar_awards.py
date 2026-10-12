"""NSF awards that mention lidar, from the public NSF Award Search API, classified by purpose.

Purpose
    Pages through https://api.nsf.gov/services/v1/awards.json for a set of lidar-related
    keywords (25 records per page, offset counted from 1), de-duplicates by award id,
    keeps only awards whose title or abstract really contains a lidar term, flags NSF
    SBIR/STTR awards (also in the SBIR.gov file, so excluded from non-SBIR totals), and
    assigns each award one class, by NSF division first and keyword rules second
    [classification is approximate]:
      sbir_sttr     NSF SBIR/STTR (Technology, Innovation and Partnerships/IIP)
      hardware      building or improving lidar instruments or lidar components
      atmos_space   atmospheric, middle/upper-atmosphere or space science using lidar
      geo_eco_map   geoscience, ecology, glaciology, archaeology, hazards or mapping with lidar data
      robotics_cv   robotics, autonomous vehicles, computer vision, point-cloud computing
      other         education, infrastructure and anything else
    Technology flags (coherent/FMCW, photonic-integrated, single-photon) are set on all classes.
    No personal data (investigator names, emails, phones) are requested or stored.

Inputs
    out_dir : directory for the raw JSON pages and the result CSVs
Outputs
    <out_dir>/nsf_raw/*.json, nsf_lidar_awards.csv, nsf_lidar_by_fy.csv,
    nsf_lidar_by_period_class.csv, nsf_lidar_hardware_list.csv (all in <out_dir>)

Usage:
    python nsf_lidar_awards.py <out_dir>
"""
import json
import os
import re
import sys
import time

import pandas as pd
import requests

API = "https://api.nsf.gov/services/v1/awards.json"
FIELDS = ("id,title,agency,awardeeName,awardeeStateCode,startDate,expDate,date,estimatedTotalAmt,"
          "fundsObligatedAmt,fundProgramName,primaryProgram,dirAbbr,divAbbr,transType,cfdaNumber,abstractText")
KEYWORDS = ["lidar", "ladar", '"laser radar"', '"Doppler lidar"', '"coherent lidar"', "FMCW",
            '"optical phased array"', '"single-photon lidar"', '"flash lidar"', '"laser altimeter"']
TERM = re.compile(r"l[ai]dars?\b|laser[\s-]+radar|light detection and ranging|laser[\s-]+altimet", re.I)


def fetch(out_dir):
    raw = os.path.join(out_dir, "nsf_raw")
    os.makedirs(raw, exist_ok=True)
    recs = {}
    for kw in KEYWORDS:
        off = 1
        while True:
            fn = os.path.join(raw, re.sub(r"\W+", "_", kw).strip("_") + f"_{off}.json")
            if os.path.exists(fn):
                d = json.load(open(fn, encoding="utf-8"))
            else:
                r = requests.get(API, params={"keyword": kw, "printFields": FIELDS, "offset": off, "rpp": 25},
                                 headers={"User-Agent": "research-script/1.0"}, timeout=120)
                r.raise_for_status()
                d = r.json()
                json.dump(d, open(fn, "w", encoding="utf-8"))
                time.sleep(0.5)
            aw = d.get("response", {}).get("award", [])
            for a in aw:
                a.setdefault("_kw", kw)
                recs.setdefault(a["id"], a)
            meta = d.get("response", {}).get("metadata", {})
            total = int(meta.get("totalCount", 0) or 0)
            off += 25
            if not aw or off > total:
                print(kw, "total", total)
                break
    return pd.DataFrame(list(recs.values()))


def fy_of(datestr):
    d = pd.to_datetime(datestr, format="%m/%d/%Y", errors="coerce")
    return d.year + (d.month >= 10) if pd.notna(d) else None


ATMOS_T = (r"atmospher|mesosph|thermosph|stratosph|ionosph|geospace|aurora|airglow|gravity wave|aerosol|"
           r"boundary layer|King Air|sodium|\bNa\b|\bFe\b|iron|potassium|Rayleigh|Raman|Doppler lidar|wind|"
           r"cloud|precipitation|convecti|turbulen|tropical|Monin|SPARC|MAPNet|water vapou?r|ozone|meteor")
GEO_T = (r"OpenTopography|NCALM|Airborne Laser Mapping|topograph|hazard|landslide|fault|earthquake|glacier|"
         r"ice sheet|snow|forest|canopy|vegetation|ecolog|biomass|archaeolog|river|coastal|bathymetr|volcan|"
         r"elevation|terrain|watershed|permafrost|wetland|reef|habitat|tree")
HW_T = (r"MRI|instrument|develop\w* (?:a|an|the|of)?\s*\w*\s*l[ai]dar|l[ai]dar (?:system|transmitter|receiver|"
        r"instrument|technolog|chip|sensor design)|laser|detector|photonic|phased[\s-]array|beam steer|metasurface|"
        r"FMCW|frequency[\s-]modulated|single[\s-]photon|avalanche|frequency comb|VCSEL|modulator")
ROBO_T = r"robot|autonomous|vehicle|self-driving|computer vision|point cloud|perception|SLAM|drone|UAV|aerial robot"


def classify(row):
    """Division first, then text; approximate [E]."""
    if row["sbir"]:
        return "sbir_sttr"
    title = str(row.get("title", ""))
    text = f"{title} {row.get('abstractText', '')}"
    div = str(row.get("divAbbr", ""))
    if re.search(r"\bMRI\b|Major Research Instrumentation", title) and re.search(r"l[ai]dar", text, re.I):
        return "hardware"
    if div == "AGS":
        return "atmos_space"
    if div in ("GCP", "OPP", "GEO", "RISE"):
        if re.search(ATMOS_T, title, re.I):
            return "atmos_space"
        return "geo_eco_map" if re.search(GEO_T, text, re.I) else "atmos_space"
    if div in ("EAR", "DEB", "DBI", "IOS", "EF", "BCS", "OCE", "ICER", "SMA", "SES"):
        return "geo_eco_map"
    if div in ("ECCS", "DMR", "PHY", "CBET", "CHE", "AST", "EEC", "OIA", "CCF"):
        if re.search(HW_T, text, re.I) and not re.search(r"mmWave|millimet|wireless|communication", title, re.I):
            return "hardware"
    if re.search(ROBO_T, text, re.I) and div in ("CMMI", "CNS", "IIS", "CCF", "OAC", "ECCS", "ITE", "TI", "EEC", "CPIS"):
        return "robotics_cv"
    if div == "CMMI" and re.search(GEO_T, text, re.I):
        return "geo_eco_map"
    if re.search(ATMOS_T, title, re.I):
        return "atmos_space"
    if re.search(GEO_T, title, re.I):
        return "geo_eco_map"
    return "other"


def main(out_dir):
    df = fetch(out_dir)
    df["text"] = df["title"].fillna("") + " " + df["abstractText"].fillna("")
    df = df[df["text"].str.contains(TERM)].copy()
    df["n_terms"] = df["text"].str.count(TERM)
    prog = df["fundProgramName"].fillna("").astype(str) + " " + df["primaryProgram"].fillna("").astype(str)
    df["sbir"] = df["title"].str.contains(r"\b(?:SBIR|STTR)\b", case=False, regex=True) | prog.str.contains(
        r"SBIR|STTR|SMALL BUSINESS", case=False, regex=True)
    df["klass"] = df.apply(classify, axis=1)
    df["fmcw_coherent"] = df["text"].str.contains(r"FMCW|frequency[\s-]modulated continuous|coherent (?:lidar|detection|doppler)|heterodyne", case=False, regex=True)
    df["photonic_integrated"] = df["text"].str.contains(r"optical phased array|photonic integrated|integrated photonic|silicon photonic|silicon nitride|on[\s-]chip|chip[\s-]scale", case=False, regex=True)
    df["single_photon"] = df["text"].str.contains(r"single[\s-]photon|photon[\s-]counting|SPAD|geiger", case=False, regex=True)
    df["start_fy"] = df["startDate"].map(fy_of)
    for c in ("fundsObligatedAmt", "estimatedTotalAmt"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    keep = ["id", "title", "awardeeName", "awardeeStateCode", "startDate", "expDate", "start_fy", "transType",
            "dirAbbr", "divAbbr", "fundProgramName", "fundsObligatedAmt", "estimatedTotalAmt", "n_terms", "sbir",
            "klass", "fmcw_coherent", "photonic_integrated", "single_photon"]
    df[keep].sort_values("start_fy").to_csv(os.path.join(out_dir, "nsf_lidar_awards.csv"), index=False)
    d = df[df["start_fy"].between(2005, 2026)]
    t = d.pivot_table(index="start_fy", columns="klass", values="fundsObligatedAmt", aggfunc=["size", "sum"], fill_value=0)
    t.columns = [f"{a}_{b}" for a, b in t.columns]
    ns = d[~d["sbir"]]
    t["nonsbir_n"] = ns.groupby("start_fy").size()
    t["nonsbir_oblig"] = ns.groupby("start_fy")["fundsObligatedAmt"].sum()
    t["nonsbir_esttotal"] = ns.groupby("start_fy")["estimatedTotalAmt"].sum()
    for f in ("fmcw_coherent", "photonic_integrated", "single_photon"):
        x = ns[ns[f]]
        t[f + "_n"] = x.groupby("start_fy").size()
        t[f + "_oblig"] = x.groupby("start_fy")["fundsObligatedAmt"].sum()
    t = t.fillna(0)
    t.to_csv(os.path.join(out_dir, "nsf_lidar_by_fy.csv"))
    def period(y):
        for lo, hi, lab in ((2005, 2009, "2005-09"), (2010, 2014, "2010-14"), (2015, 2019, "2015-19"),
                            (2020, 2022, "2020-22"), (2023, 2025, "2023-25")):
            if lo <= y <= hi:
                return lab
        return "2026 (partial)"

    d = d.assign(period=d["start_fy"].map(period))
    pt = d.pivot_table(index="klass", columns="period", values="fundsObligatedAmt", aggfunc=["size", "sum"], fill_value=0)
    pt.to_csv(os.path.join(out_dir, "nsf_lidar_by_period_class.csv"))
    hw = d[(d["klass"] == "hardware") | d["fmcw_coherent"] | d["photonic_integrated"]]
    hw = hw[~hw["sbir"]].sort_values("start_fy")
    hw[["id", "start_fy", "klass", "divAbbr", "fundsObligatedAmt", "awardeeName", "title", "fmcw_coherent",
        "photonic_integrated", "single_photon"]].to_csv(os.path.join(out_dir, "nsf_lidar_hardware_list.csv"), index=False)
    with pd.option_context("display.width", 250, "display.max_columns", 40, "display.max_colwidth", 100):
        print(t.round(0))
        print(pt)
        big = ns.sort_values("fundsObligatedAmt", ascending=False).head(40)
        print(big[["id", "start_fy", "klass", "fundsObligatedAmt", "awardeeName", "title"]].to_string())
        print(hw[["id", "start_fy", "klass", "divAbbr", "fundsObligatedAmt", "awardeeName", "title"]].to_string())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
