"""Round 4, group R2 (§C0, §C4): Appendix 2 lines for the sources its agent read.

The R2 findings list their Appendix 2 sources as plain lines without a group, so this script places them by
hand at the end of the Appendix 2 group that covers the section they support. Lines whose URL Appendix 2
already holds are left out. Writes edits/round4/R4_R2_appendix.json; the report is only read.
Usage: python round4_r2_appendix.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
T = REPORT.read_text(encoding="utf-8")
A = T[T.index("# Appendix 2 — Selected sources"):]
NEW = {
    "Technology routes and SPAD": [
        "- Excelitas C30902EH Si APD datasheet ($k_{\\rm eff}=0.02$, gain 150): https://www.excelitas.com/file-download/download/public/91501?filename=C30902EH_Si_APD_Datasheet.pdf",
        "- Excelitas C30645/C30662 InGaAs APD datasheet (usable gain 10–20): https://www.excelitas.com/file-download/download/public/61766?filename=Excelitas_C30645_Series_InGaAs_APD_Datasheet.pdf",
        "- Campbell *et al.*, recent advances in APDs, *IEEE JSTQE* (2004): https://coldren.ece.ucsb.edu/sites/default/files/publications/campbelljstqejuly04.pdf",
        "- Martyniuk *et al.*, infrared APDs review, *Light Sci. Appl.* (2023): https://www.nature.com/articles/s41377-023-01259-3",
        "- Rae and Mellot (ST), 64-zone SPAD ranging device, ISSW 2018 slides: https://imagesensors.org/wp-content/uploads/2019/05/Bruce_Rae.pdf",
        "- Bonanno (Yole), smartphone laser-autofocus teardown and costing, ISSW 2024: https://www.imagesensors.org/Past%20Workshops/2024%20ISSW/Papers/R06.1.pdf",
        "- Seibersdorf Laboratories, white papers on IEC 60825-1:2014 (Class 3B cap above 1,310 nm) and on EN 60825-1 A11: https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/whitepaper_iec-60825-1.pdf ; https://www.seibersdorf-laboratories.at/fileadmin/user_upload/docs/le/las/publ/whitepaper_a11_to_en_60825-1.pdf",
        "- Duthon, Colomb and Bernardin, fog extinction against wavelength, *Appl. Sci.* (2019): https://www.mdpi.com/2076-3417/9/14/2843",
        "- Seyond Falcon K1 user manual V2.1.2 (30 W, 1.75 kg): https://www.seyond.com/wp-content/uploads/2024/12/Seyond-Falcon-K1-LiDAR_User-Manual_V2.1.2_EN_PublicRH_20240314.pdf",
        "- Seyond Falcon K3 product page (Chinese; 900 m maximum, 450 m at 10%, 20 W): https://www.seyond.cn/falcon-k3-2/",
        "- Beer *et al.*, Fraunhofer IMS SPAD lidar sensor (2% PDE at 905 nm), *Sensors* (2018): https://pmc.ncbi.nlm.nih.gov/articles/PMC6308528/",
        "- onsemi ArrayRDM-0112A20 (16% PDE at 905 nm): https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6325/ARRAYRDM-0112A20-QFN.pdf",
        "- onsemi J-Series SiPM datasheet: https://www.farnell.com/datasheets/2704145.pdf",
        "- Na *et al.*, review of germanium-silicon SPADs, Proc. SPIE 13448 (2025): https://arxiv.org/pdf/2605.07343",
        "- Na *et al.*, room-temperature Ge-Si SPAD (Artilux), *Nature* (2024): https://doi.org/10.1038/s41586-024-07076-x",
        "- Bian *et al.* (GlobalFoundries), Ge-on-Si PIN photodiodes, OFC 2025 Th3E.6: https://opg.optica.org/abstract.cfm?URI=OFC-2025-Th3E.6",
        "- Wang *et al.* (Fudan University, Zhangjiang Laboratory, Innolight), ultra-thin Ge photodiode, OFC 2025 M4K.2: https://opg.optica.org/abstract.cfm?uri=OFC-2025-M4K.2",
        "- Chen *et al.*, Ge p-i-n dark current, *J. Appl. Phys.* (2016), author copy: https://www.photonics.intec.ugent.be/download/pub_3746.pdf",
        "- Hale and Querry, optical constants of water (1973): https://doi.org/10.1364/AO.12.000555",
        "- Kou, Labrie and Chylek, refractive indices of water and ice (1993): https://doi.org/10.1364/AO.32.003531",
        "- KrASIA (36Kr), Seyond's SPAC listing and the 1,550 nm cost (Oct 2025): https://kr-asia.com/lidar-maker-seyond-pursues-spac-listing-after-losing-ground-to-rivals",
        "- Yole, Automotive LiDAR 2023 conference deck (wavelength and light-source shares): https://medias.yolegroup.com/uploads/2023/12/automotive-lidar_boulay_yole_intelligence_v2.pdf",
        "- RoboSense M3 at CES 2024 (940 nm, 50–70% cheaper than 1,550 nm): https://en.prnasia.com/releases/global/robosense-announces-new-m-platform-lidar-sensors-at-ces-2024-433294.shtml",
    ],
    "FMCW and beam steering": [
        "- Wang *et al.* (SUSTech and RoboSense), integrated FMCW photonic engine, *Moore and More* (2025): https://link.springer.com/article/10.1007/s44275-025-00030-7",
    ],
    "Supply chain and geopolitics": [
        "- BigGo Finance, InP substrate prices (Apr 2026): https://finance.biggo.com/news/xsiIxJ0Bh5an-7GhIww3",
        "- Reuters via MINING.COM, InP export controls and the 6-inch price (Jun 2026): https://www.mining.com/web/chinas-control-over-indium-phosphide-exports-threatens-ai-data-centre-rollout/",
    ],
    "Lidar market and Western programs": [
        "- Hesai, ATX \"best-selling long-range lidar in the ADAS segment\" and the Yole 43% share (May 2026): https://www.prnewswire.com/news-releases/hesai-secures-design-win-from-another-top-european-oem-adding-1-million-unit-order-302777712.html",
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
    if add:
        edits.append({"id": f"R4_R2_appendix-{len(edits)+1:03d}", "finding": f"Round 4 source research, R2 Appendix 2 ({g})",
                      "old": last, "new": last + "\n" + "\n".join(add),
                      "why": "Sources read by the R2 research agent (sources/R2_C0_C4_findings.md), placed by section."})
out = HERE / "edits" / "round4" / "R4_R2_appendix.json"
assert not out.exists(), "already written"
out.write_text(json.dumps({"block": "R4_R2_appendix", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(len(edits), "edits written to", out.name, "|", sum(e["new"].count("\n") for e in edits), "lines added")
