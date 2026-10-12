"""Point every moved figure script's outputs at <report>/automotive_perception_report_figures.

Inside the report folder the scripts live in <report>/build/figures; run elsewhere (e.g. extracted from
the PDF's attachments) they fall back to writing next to themselves.
"""
from pathlib import Path

BFIG = Path(r"<report folder>\build\figures")
NL = "\n"
HELPER = NL.join([
    "",
    "",
    "def _output_dir() -> Path:",
    '    """Where figures and tables are written.',
    "",
    "    Inside the report folder this script lives in <report>/build/figures, and its outputs go to",
    "    <report>/automotive_perception_report_figures. Run anywhere else (for example after extracting it",
    "    from the PDF's attachments), it writes next to itself.",
    '    """',
    "    here = Path(__file__).resolve().parent",
    "    try:",
    '        figs = here.parents[1] / "automotive_perception_report_figures"',
    "    except IndexError:",
    "        return here",
    "    return figs if figs.is_dir() else here",
    "",
    "",
    "OUT_DIR = _output_dir()",
])

REPL = {
    "coherent_mode_coverage.py": [("    out = Path(__file__).resolve().parent", "    out = OUT_DIR")],
    "fmcw_tof_system_budget.py": [("    here = Path(__file__).resolve().parent", "    here = OUT_DIR")],
    "ge_coherent_receiver.py": [("    here = Path(__file__).resolve().parent", "    here = OUT_DIR")],
    "lidar_equity_hype_cycle.py": [
        ("    here = Path(__file__).resolve().parent" + NL + '    data = load(here / "lidar_equity_prices_weekly.csv")',
         "    here = OUT_DIR  # outputs" + NL
         + '    data = load(Path(__file__).resolve().parent / "lidar_equity_prices_weekly.csv")  # input sits next to the script'),
    ],
    "link_budget_scaling.py": [("    here = Path(__file__).resolve().parent", "    here = OUT_DIR")],
    "mechanical_scanning_limits.py": [("    here = Path(__file__).resolve().parent", "    here = OUT_DIR")],
    "nuscenes_matching_localization.py": [("    here = Path(__file__).resolve().parent", "    here = OUT_DIR")],
    "truck_long_range_sensing.py": [("    here = Path(__file__).resolve().parent", "    here = OUT_DIR")],
    "wavelength_eye_safety_background.py": [
        ('    Path(__file__).with_name("wavelength_eye_safety_background_tables.txt").write_text(',
         '    (OUT_DIR / "wavelength_eye_safety_background_tables.txt").write_text('),
    ],
}

BLANK2 = NL + NL
for name, reps in REPL.items():
    p = BFIG / name
    t = p.read_text(encoding="utf-8")
    if "OUT_DIR = _output_dir()" in t:
        print("already patched", name)
        continue
    for old, new in reps:
        assert t.count(old) == 1, (name, old[:50], t.count(old))
        t = t.replace(old, new)
    anchor = "from pathlib import Path" + NL
    assert t.count(anchor) == 1, (name, t.count(anchor))
    i = t.index(anchor)
    k = t.find(BLANK2, i)
    while True:
        nxt = t.find(BLANK2, k + 2)
        block = t[k + 2:nxt if nxt > 0 else len(t)]
        lines = block.split(NL)
        if block and all(l.startswith(("import ", "from ")) or not l.strip() for l in lines):
            k = nxt
            continue
        break
    t = t[:k] + HELPER + t[k:]
    p.write_text(t, encoding="utf-8", newline=NL)
    print("patched", name)
