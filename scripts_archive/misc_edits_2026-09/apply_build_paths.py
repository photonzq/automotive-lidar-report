from pathlib import Path

here = Path(__file__).resolve().parent
snap = here.parent / "rewrite" / "report_after_rewrite.md"
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes()
assert raw == snap.read_bytes(), "report changed since the rewrite was written"
s = raw.decode("utf-8")
missing = []


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        missing.append((n, old[:80]))
        return
    s = s.replace(old, new)


# 1. reading guide: where the figure scripts are, and the self-contained PDF
anchor = "\n\n**Method.** Web research drew on primary filings"
rep(anchor,
    "\n\n**Figures, their scripts and the self-contained PDF.**\n"
    "- Every figure is drawn by a Python script in the report folder's `build/figures/` subfolder, named next to the figure. "
    "Each script writes its figure (as PNG and PDF) and a `…_tables.txt` file with the numbers behind it into "
    "`automotive_perception_report_figures/`.\n"
    "- The PDF edition is self-contained. It embeds, as file attachments, every figure script, their one input data file "
    "(`lidar_equity_prices_weekly.csv`), the tables the scripts print, and the tools that build the PDF "
    "(`build/build_pdf.py`, `build/check_pdf.py`, `build/report.css` and a `build/README.md` that explains them). "
    "Open the PDF viewer's attachments panel to see them all, or click the paperclip in the left margin beside a figure "
    "to open the script that drew it.\n"
    "- To reproduce a figure, run its script with Python 3, NumPy and Matplotlib (and SciPy for `link_budget_scaling.py`). "
    "Run inside the report folder, a script writes into `automotive_perception_report_figures/`; run anywhere else, for "
    "example after extracting it from the PDF, it writes next to itself. The equity script needs its CSV in the same folder."
    + anchor)

# 2. script paths moved from automotive_perception_report_figures/ to build/figures/
for name in ["link_budget_scaling", "lidar_equity_hype_cycle", "wavelength_eye_safety_background", "ge_coherent_receiver",
             "fmcw_tof_system_budget", "coherent_mode_coverage", "nuscenes_matching_localization",
             "truck_long_range_sensing"]:
    rep(f"`automotive_perception_report_figures/{name}.py`", f"`build/figures/{name}.py`")
rep("script and tables in `automotive_perception_report_figures/mechanical_scanning_limits.py` and "
    "`mechanical_scanning_limits_tables.txt`",
    "script `build/figures/mechanical_scanning_limits.py`, tables in "
    "`automotive_perception_report_figures/mechanical_scanning_limits_tables.txt`")
rep("downloaded 27 Sep 2026 and stored in `lidar_equity_prices_weekly.csv`",
    "downloaded 27 Sep 2026 and stored in `build/figures/lidar_equity_prices_weekly.csv`")
rep("The code is `build/figures/coherent_mode_coverage.py`, stored with this note;",
    "The code is `build/figures/coherent_mode_coverage.py`, stored with the report;")

print("missing", missing)
assert not missing
assert "automotive_perception_report_figures/" + "link_budget_scaling.py" not in s
left = [ln for ln in s.split("\n") if "automotive_perception_report_figures/" in ln and ".py" in ln]
print("lines still naming a .py under the figures folder:", len(left))
for ln in left:
    print("   ", ln[:160])
assert "\t" not in s and "\r\n" not in s
assert rp.read_bytes() == raw, "report changed while editing"
rp.write_bytes(s.encode("utf-8"))
(here.parent / "rewrite" / "report_after_buildpaths.md").write_bytes(s.encode("utf-8"))
print("ok", len(s.encode("utf-8")))
