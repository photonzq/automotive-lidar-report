"""NASA TechPort projects that involve lidar, by start year, programme, application and technology.

Purpose
    Downloads the public TechPort project listing (GET https://techport.nasa.gov/api/projects/search,
    which returns every project record with title, description, programme, dates and lead
    organization; about 21,000 records, 115 MB) unless a cached copy exists, keeps projects
    whose title or description mentions lidar terms, and classifies them [E]:
      programme   : SBIR/STTR; ESTO (Earth Science Technology Office: IIP, ACT, AIST, ...);
                    STMD technology programmes (Game Changing, Early Career, Early Stage,
                    Tipping Point, Flight Opportunities, Center Innovation Fund, ...); other
      application : earth_atmosphere (wind, aerosol, clouds, CO2, CH4, water vapour, DIAL);
                    earth_altimetry_vegetation; landing_navigation (descent, hazard detection,
                    Navigation Doppler Lidar, terrain-relative navigation); rendezvous_docking;
                    planetary_science; other
      technology  : coherent/FMCW/Doppler; photonic-integrated; single-photon/photon-counting
    TechPort exposes no award amounts in this listing, so the output is project counts.
    Personal fields (contacts, names, emails) are dropped and never written.

Inputs
    out_dir : folder for the cached dump (techport_all.json) and the results
Outputs
    techport_lidar_projects.csv, techport_lidar_by_year.csv (in out_dir)

Usage:
    python nasa_techport_lidar.py <out_dir>
"""
import json
import os
import re
import sys

import pandas as pd
import requests

URL = "https://techport.nasa.gov/api/projects/search?searchQuery=lidar"
TERM = re.compile(r"l[ai]dars?\b|laser[\s-]+radar|laser[\s-]+altimet|light detection and ranging", re.I)
APPS = [
    ("landing_navigation", r"landing|lander|descent|hazard detection|navigation doppler|\bNDL\b|terrain[\s-]relative|"
                           r"\bTRN\b|SPLICE|ALHAT|COBALT|touchdown"),
    ("rendezvous_docking", r"rendezvous|docking|proximity operations|satellite servicing|\bOSAM\b|capture"),
    ("earth_atmosphere", r"\bwind|aerosol|cloud|\bCO2\b|carbon dioxide|methane|\bCH4\b|water vapou?r|ozone|\bDIAL\b|"
                         r"differential absorption|boundary layer|atmospher|air quality|greenhouse|backscatter"),
    ("earth_altimetry_vegetation", r"altimet|topograph|vegetation|canopy|biomass|ice sheet|sea ice|ICESat|GEDI|"
                                   r"surface topography|elevation|bathymetr|snow"),
    ("planetary_science", r"mars|lunar|moon|europa|titan|asteroid|comet|venus|planetary"),
]
COH = r"coherent|FMCW|frequency[\s-]modulated|doppler|heterodyne|homodyne"
PIC = r"photonic integrated|integrated photonic|\bPIC\b|silicon photonic|optical phased array|chip[\s-]scale|on[\s-]chip"
SPC = r"single[\s-]photon|photon[\s-]counting|geiger|\bSPAD"


def prog_class(p):
    t = (p.get("title") or "") + " " + (p.get("acronym") or "")
    if re.search(r"SBIR|STTR|Small Business", t, re.I):
        return "SBIR/STTR"
    if re.search(r"Earth Science Technology|ESTO|Instrument Incubator|Advanced Component|AIST|In-Space Validation|"
                 r"Decadal Survey Incubation", t, re.I):
        return "ESTO/Earth science technology"
    if re.search(r"Game Changing|Early Career|Early Stage|Tipping Point|Flight Opportunities|Center Innovation|"
                 r"Technology Demonstration|Small Spacecraft|Lunar Surface Innovation|NIAC|Innovative Advanced|"
                 r"Announcement of Collaboration|Prizes|Space Technology Research", t, re.I):
        return "STMD technology"
    if re.search(r"Planetary|PICASSO|MatISSE|DALI|Lunar|Mars", t, re.I):
        return "SMD planetary instrument"
    if re.search(r"Internal|IRAD|Independent Research", t, re.I):
        return "Center internal R&D"
    return "other"


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fn = os.path.join(out_dir, "techport_all.json")
    if not os.path.exists(fn):
        r = requests.get(URL, headers={"User-Agent": "research-script/1.0"}, timeout=600)
        r.raise_for_status()
        open(fn, "wb").write(r.content)
    recs = json.load(open(fn, encoding="utf-8"))["results"]
    rows = []
    for p in recs:
        text = f"{p.get('title') or ''} {p.get('description') or ''} {p.get('benefits') or ''}"
        if not TERM.search(text):
            continue
        prog = p.get("program") or {}
        lead = p.get("leadOrganization") or {}
        app = "other"
        for name, pat in APPS:
            if re.search(pat, text, re.I):
                app = name
                break
        start = pd.to_datetime(p.get("startDate"), errors="coerce")
        rows.append({
            "projectId": p.get("projectId"), "title": p.get("title"),
            "program": prog.get("title"), "program_class": prog_class(prog),
            "lead_org": lead.get("organization_name"), "lead_org_type": lead.get("organization_type"),
            "start_year": start.year if pd.notna(start) else None, "status": p.get("status"),
            "trl_begin": p.get("trlBegin"), "trl_end": p.get("trlEnd"),
            "n_terms": len(TERM.findall(text)), "title_term": bool(TERM.search(p.get("title") or "")),
            "application": app,
            "coherent": bool(re.search(COH, text, re.I)),
            "integrated": bool(re.search(PIC, text, re.I)),
            "single_photon": bool(re.search(SPC, text, re.I)),
        })
    d = pd.DataFrame(rows)
    d["core"] = d["title_term"] | (d["n_terms"] >= 2)
    d.sort_values("start_year").to_csv(os.path.join(out_dir, "techport_lidar_projects.csv"), index=False)
    c = d[d["core"] & d["start_year"].between(2005, 2026)]
    t = pd.concat([
        c.groupby("start_year").size().rename("core_projects"),
        c.pivot_table(index="start_year", columns="program_class", values="projectId", aggfunc="count", fill_value=0),
        c.pivot_table(index="start_year", columns="application", values="projectId", aggfunc="count", fill_value=0).add_prefix("app_"),
        c[c["coherent"]].groupby("start_year").size().rename("coherent"),
        c[c["integrated"]].groupby("start_year").size().rename("integrated"),
        c[c["single_photon"]].groupby("start_year").size().rename("single_photon"),
    ], axis=1).fillna(0).astype(int)
    t.to_csv(os.path.join(out_dir, "techport_lidar_by_year.csv"))
    with pd.option_context("display.width", 250, "display.max_columns", 40):
        print(len(d), "lidar-mentioning projects;", int(d["core"].sum()), "core")
        print(t)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
