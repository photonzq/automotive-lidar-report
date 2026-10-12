"""Round 4, group R1 (Part A, §E2–§E5): Appendix 2 lines for the sources its agent read.

The R1 findings list their Appendix 2 sources as plain lines without a group, so this script places them by
hand: each new line goes at the end of the Appendix 2 group that covers the section it supports, and the
second Wood line is relabelled with its authors and venue (R1 item 15). Lines whose URL Appendix 2 already holds
are left out. Writes edits/round4/R4_R1_appendix.json; the report is only read.
Usage: python round4_r1_appendix.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
T = REPORT.read_text(encoding="utf-8")
A = T[T.index("# Appendix 2 — Selected sources"):]
NEW = {
    "Thermal night vision": [
        "- NHTSA, Traffic Safety Facts: Pedestrians, 2024 Data (DOT HS 813 818; 7,080 deaths, 76% in the dark): https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813818",
        "- NHTSA FARS 2024 national data files (pedestrian deaths by light condition, area and road type): https://static.nhtsa.gov/nhtsa/downloads/FARS/2024/National/FARS2024NationalCSV.zip",
        "- New Atlas, BMW Night Vision with thermal imaging (about US\\$2,500 option, 23 Aug 2006): https://newatlas.com/bmw-incorporates-thermal-imaging-into-newly-available-night-vision-driver-assistance-system/6044/",
        "- D.C. Circuit, *Alliance for Automotive Innovation v. DOT*, No. 25-1026 (FMVSS 127 petition; abeyance orders), RECAP docket: https://www.courtlistener.com/docket/69556046/alliance-for-automotive-innovation-v-dot/",
        "- Raytron, company milestones (8 µm 1920×1080 detector, 2021; 6 µm 640×512 detector, 2024): https://en.raytrontek.com/about/about-us.htm",
        "- Guide Infrared, CIOE 2024 products (FLEXB608, 640×512 at 8 µm): https://www.guide-infrared.com/companynews/217.html",
        "- LightPath BlackDiamond BD6 datasheet ($\\mathrm{As_{40}Se_{60}}$, germanium-free) and BD-2 datasheet (28% Ge): https://refractiveindex.info/download/data/2023/50415_Lightpath_BD6_Datasheet.pdf ; https://refractiveindex.info/download/data/2013/BD-2.pdf",
    ],
    "Headlights (§A6)": [
        "- FMVSS 108 codified text, S3 and S9.4.1.6.4.5 (ADB transition zone at most 1.0°): https://www.govinfo.gov/link/cfr/49/571?link-type=pdf&sectionnum=108&year=mostrecent",
        "- UN R112, 2014 official text, §6.2.4 passing-beam table (B50L at most 350 cd; 50R and 75R at least 10,100 cd for class B): https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=uriserv:OJ.L_.2014.250.01.0067.01.ENG",
        "- Audi, Matrix LED headlights (A8, end of 2013; 25 high-beam LEDs per lamp; 1 Jul 2013): https://www.automotiveworld.com/news/leading-the-way-in-lighting-technology-the-new-audi-matrix-led-headlights/",
        "- Autocar Professional, Mercedes Multibeam LED headlamps on the CLS (17 Jun 2014): https://www.autocarpro.in/news-international/mercedes-benz-debuts-multi-beam-led-headlamp-tech-cls-5835",
    ],
    "Robotaxi and trucks": [
        "- Cruise Part 573 Safety Recall Report 23E-029 (articulated-bus collision, 23 Mar 2023): https://static.nhtsa.gov/odi/rcl/2023/RCLRPT-23E029-4270.PDF",
        "- Cummings, \"What Self-Driving Cars Tell Us About AI Risks\", *IEEE Spectrum* (30 Jul 2023): https://spectrum.ieee.org/self-driving-cars-2662494269",
        "- NHTSA Standing General Order crash reports, ADS incidents (current file and 2021–2025 archive): https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADS.csv ; https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Incident_Reports_ADS.csv",
    ],
    "Camera-only vs multimodal": [
        "- ResearchInChina, Automotive 4D Radar Industry Research Report 2025, summary (basic-imaging-radar prices, installations): http://www.researchinchina.com/Htmls/Report/2025/78124.html",
        "- Zhang *et al.*, Dual Radar dataset, *Sci. Data* 12, 439 (2025), Tables 2 and 4 (open access): https://pmc.ncbi.nlm.nih.gov/articles/PMC11907064/",
        "- RoboSense RS-Ruby Lite users' manual, Table 1 (80 channels, 0.2° at 10 Hz, 1.44 M points/s): https://cdn.robotshop.com/media/u/utr/rb-utr-07/pdf/robosense-rs-rubylite-laser-rangefinder-230-m-user-guide.pdf",
    ],
}
heads = {m.group(1).strip(): m.start() for m in re.finditer(r"(?m)^\*\*([^*]+)\*\*\s*$|^\*([^*]+)\*\s*$", A)
         if m.group(1)}
edits = []
for g, lines in NEW.items():
    a = heads[g]
    b = min((p for p in heads.values() if p > a), default=len(A))
    body = A[a:b]
    last = [l for l in body.split("\n") if l.startswith("- ")][-1]
    assert T.count(last) == 1, (g, last[:60])
    add = [l for l in lines if re.findall(r"https?://\S+", l)[-1].rstrip(").,;") not in A]
    edits.append({"id": f"R4_R1_appendix-{len(edits)+1:03d}", "finding": f"Round 4 source research, R1 Appendix 2 ({g})",
                  "old": last, "new": last + "\n" + "\n".join(add),
                  "why": "Sources read by the R1 research agent (sources/R1_partA_E2-E5_findings.md), placed by section."})
old_wood = ("- Pedestrian visibility at night (clothing, driver age, beam setting): "
            "https://www.researchgate.net/publication/228414781_Pedestrian_visibility_at_night_Effects_of_pedestrian_clothing_driver_age_and_headlamp_beam_setting")
assert T.count(old_wood) == 1
edits.append({"id": f"R4_R1_appendix-{len(edits)+1:03d}", "finding": "Round 4 source research, R1 item 15 (Wood line label)",
              "old": old_wood,
              "new": old_wood.replace("- Pedestrian visibility at night (clothing, driver age, beam setting):",
                                      "- Wood, Tyrrell & Carberry 2003, \"Pedestrian visibility at night: effects of pedestrian clothing, driver age, and headlamp beam setting\", TRB 82nd Annual Meeting (author copy):"),
              "why": "Names the study the text cites as Wood, Tyrrell & Carberry 2003."})
out = HERE / "edits" / "round4" / "R4_R1_appendix.json"
assert not out.exists(), "already written"
out.write_text(json.dumps({"block": "R4_R1_appendix", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(len(edits), "edits written to", out.name)
