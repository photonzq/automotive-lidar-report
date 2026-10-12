"""Round 3 follow-up: the underbrace labels of the new P_elec display (now Eq. (116)) nested \\rm inside \\rm, which
the PDF build's {\\rm ...} conversion handles only one brace level deep. Writes edits/round3/R3e_pelec_labels.json
with labels that need no nesting (\\text{fixed}, \\propto P_ch, \\propto 1/P_ch); the text after the display explains
them. Usage: python round3_fix_pelec_labels.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIRS = [
    (r"_{\rm independent\ of\ P_{\rm ch}}", r"_{\text{fixed}}"),
    (r"_{\rm grows\ with\ P_{\rm ch}}", r"_{\propto\,P_{\rm ch}}"),
    (r"_{\rm falls\ as\ 1/P_{\rm ch}}", r"_{\propto\,1/P_{\rm ch}}"),
]
edits = [{"id": f"R3e_pelec_labels-{i:03d}", "finding": "08_C7b report #34 (P_elec display); build compatibility",
          "old": o, "new": n,
          "why": "The build converts {\\rm ...} only one brace level deep; labels without nested \\rm."}
         for i, (o, n) in enumerate(PAIRS, 1)]
out = HERE / "edits" / "round3" / "R3e_pelec_labels.json"
out.write_text(json.dumps({"block": "R3e_pelec_labels", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(len(edits), "edits written to", out.name)
