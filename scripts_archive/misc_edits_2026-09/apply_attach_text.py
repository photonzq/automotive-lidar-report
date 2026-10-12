from pathlib import Path

here = Path(__file__).resolve().parent
snap = here.parent / "rewrite" / "report_after_buildpaths.md"
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == snap.read_bytes(), "report changed since last write"
s = raw.decode("utf-8")
missing = []


def rep(old, new):
    global s
    if s.count(old) != 1:
        missing.append((s.count(old), old[:80]))
        return
    s = s.replace(old, new)


rep("**Figures, their scripts and the self-contained PDF.**", "**Figures and their code.**")
rep("- The PDF edition is self-contained. It embeds, as file attachments, every figure script, their one input data file "
    "(`lidar_equity_prices_weekly.csv`), the tables the scripts print, and the tools that build the PDF "
    "(`build/build_pdf.py`, `build/check_pdf.py`, `build/report.css` and a `build/README.md` that explains them). "
    "Open the PDF viewer's attachments panel to see them all, or click the paperclip in the left margin beside a figure "
    "to open the script that drew it.",
    "- The PDF edition carries the code for its figures: it embeds every figure script, and the one input data file they "
    "need (`lidar_equity_prices_weekly.csv`), as file attachments. Open the PDF viewer's attachments panel to see them "
    "all, or click the paperclip in the left margin beside a figure to open the script that drew it.")
print("missing", missing)
assert not missing
assert rp.read_bytes() == raw
rp.write_bytes(s.encode("utf-8"))
(here.parent / "rewrite" / "report_after_attachtext.md").write_bytes(s.encode("utf-8"))
print("ok", len(s.encode("utf-8")))
