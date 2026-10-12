"""Round 4, group R5 (§C10 part 1): Appendix 2 lines for the sources its agent read, plus Zhang et al. (2022).

The R5 findings list their Appendix 2 sources as plain lines without a group, so this script places them by hand at
the end of the italic subgroup *OPA devices, reviews and receive-side analysis* of the §C10 group. Zhang et al.
(Opt. Express 2022) is added because my amendment of R5 item 04 cites it in §C10.2b; the RAY-L1 datasheet the agent
offered as optional is left out because the report never cites that laser. Lines whose URL Appendix 2 already holds
are left out. Writes edits/round4/R4_R5_appendix.json; the report is only read.
Usage: python round4_r5_appendix.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
T = REPORT.read_text(encoding="utf-8")
A = T[T.index("# Appendix 2 — Selected sources"):]
NEW = {
    "OPA devices, reviews and receive-side analysis": [
        "- Li Y. *et al.* (Jilin University), 128-channel SiN-on-SOI OPA, 140° field, 100 m FMCW ranging on a 90% scatter plate, *Photon. Res.* 9, 2511 (2021): https://opg.optica.org/prj/fulltext.cfm?uri=prj-9-12-2511",
        "- Zhang L. *et al.* (Jilin University and CIOMP), 64-channel SiN-on-SOI OPA, 109 m FMCW ranging on a 90% reflector with a lens in front of the chip, *Opt. Express* 30, 5008 (2022): https://opg.optica.org/oe/fulltext.cfm?uri=oe-30-4-5008",
        "- Prost *et al.* (imec), transparent peer review file (target material, 2026): https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-77490-4/MediaObjects/41467_2026_77490_MOESM2_ESM.pdf",
        "- Yang *et al.*, \"Phase coherence length in silicon photonic platform\", *Opt. Express* 23, 16890 (2015): https://opg.optica.org/oe/fulltext.cfm?uri=oe-23-13-16890",
        "- Rizzo *et al.*, fabrication-robust SOI devices (width sensitivity of Si strips), *Opt. Lett.* 48, 215 (2023), preprint: https://arxiv.org/abs/2205.11481",
        "- Fatemi, Khachaturian & Hajimiri, 128-element nonuniform sparse 2-D OPA, *IEEE JSSC* 54, 1200 (2019): https://ieeexplore.ieee.org/document/8649827",
        "- Wang Y. *et al.*, 160 × 160 MEMS 2D optical phased array, *Optica* 6, 557 (2019): https://opg.optica.org/optica/fulltext.cfm?uri=optica-6-5-557",
        "- Guglielmon *et al.* (Analog Photonics), \"Optical phased array super-cell beyond the reticle limit\", CLEO 2023, STh5C.5 (abstract): https://opg.optica.org/abstract.cfm?uri=CLEO_SI-2023-STh5C.5",
    ],
}
# group headings: bold lines and italic sublines of Appendix 2
heads = {(m.group(1) or m.group(2)).strip(): m.start()
         for m in re.finditer(r"(?m)^\*\*([^*]+)\*\*\s*$|^\*([^*]+)\*\s*$", A)}
edits = []
for g, lines in NEW.items():
    a = heads[g]
    b = min((p for p in heads.values() if p > a), default=len(A))
    body = A[a:b]
    last = [l for l in body.split("\n") if l.startswith("- ")][-1]
    assert T.count(last) == 1, (g, last[:60])
    add = [l for l in lines if re.findall(r"https?://\S+", l)[-1].rstrip(").,;") not in A]
    if add:
        edits.append({"id": f"R4_R5_appendix-{len(edits)+1:03d}", "finding": f"Round 4 source research, R5 Appendix 2 ({g})",
                      "old": last, "new": last + "\n" + "\n".join(add),
                      "why": "Sources read by the R5 research agent (sources/R5_C10_part1_findings.md), placed by "
                             "section; Zhang et al. (2022) read for my amendment of item 04."})
out = HERE / "edits" / "round4" / "R4_R5_appendix.json"
assert not out.exists(), "already written"
out.write_text(json.dumps({"block": "R4_R5_appendix", "edits": edits,
                           "skipped": [{"id": "R5-08 appendix", "why": "RAY-L1 datasheet: the report never cites RAY-L1"}]},
                          ensure_ascii=False, indent=1), encoding="utf-8")
print(len(edits), "edits written to", out.name, "|", sum(e["new"].count("\n") for e in edits), "lines added")
