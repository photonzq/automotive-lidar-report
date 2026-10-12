"""Install the restructured §C0 into the report (hash-guarded) and update the files that refer to it (12 Oct 2026).

Usage: python c0_install.py <report folder> <working copy> <expected report sha256 prefix>
Every replacement must match exactly the stated number of times; each file is re-hashed just before it is written.
"""
import hashlib
import sys
from pathlib import Path

root, work, expect = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]

MAP_TABLE = """
| Old (before 12 Oct 2026) | New |
|---|---|
| 1. Pulsed direct time of flight | 1.1 (timing); 3.1 (photon budget of one pulse); 5.2 (range scaling) |
| 2. FMCW coherent ranging | 1.3 |
| 3. Beams, pixels and sampling | 2.1 |
| 4. Velocity | 1.4 |
| 5. Eye safety and sunlight | 4.2 (solar background); 5.3 (eye safety) |
| 6. Detector gain and excess noise | 4.1 |
| 7. Detection and false alarms | 4.3 |
| 8. Weather | 3.3 (extinction); 5.4 (reach in fog and rain) |
| 9. Amplitude-modulated (phase) ranging | 1.2 |
| 10.1 Model, assumptions and symbols | assumptions at the start of 3; symbols in 3.1–3.3 |
| 10.2 Link loss | 3.1 (direct), 3.2 (coherent) |
| 10.3 Detection statistics | 4.2 (background of the model), 4.3 |
| 10.4 Detection level and maximum range | 5.1 |
| 10.5 Range scaling | 5.2 |
| 10.6 Margin at short range | 5.4 |
| 10.7 Dynamic range | 5.5 |
| 10.8 Benchmark | 6.1 |
| 10.9 What the model leaves out | 6.2 |
"""

ARCHIVE_SECTION = """
## Restructured physics chapter (§C0, 2026-10-12), `c0_restructure_2026-10/`

§C0 was reorganized as a textbook chapter in six parts, following the measurement chain: measuring one point (1.1–1.4), from points to images (2.1), how much light comes back (3.1–3.3), how much light is needed (4.1–4.3), range and its limits and robustness (5.1–5.5), and testing the model (6.1–6.2), with a closing table of where each relation is used. Every table, derivation and number was carried over from the previous text by exact copy between anchors; the new text is the connective prose, the merged passages (one photon budget, one set of detection statistics under the per-point rule, one treatment of weather) and the renumbered references. The duplicate single-speckle law was merged (old Eq. (35) into Eq. (46)), equations were renumbered in document order, and Figures C0.10a–d became Figures C0.1–C0.4. The old subsections map to the new ones as follows:
""" + MAP_TABLE + """
| File | Purpose | Status |
|---|---|---|
| `c0_lib.py` | Assembler: a plan of new text and exact copies of old lines between anchors, with counted replacements, table-column removal and indentation changes. | historical |
| `c0_plan_a.py`, `c0_plan_b.py`, `c0_plan_c.py` | The plan of the new §C0: opening and parts 1–2; parts 3–4; parts 5–6 and the closing table. | historical |
| `c0_build.py` | Builds a working copy: assembles §C0, lists the old lines not carried over, remaps the 110 references to §C0 subsections elsewhere in the report (with per-line overrides where an old subsection split), updates the reader's guide, renames the figures and checks every internal reference. | historical |
| `make_renumber_copy.py` | Points a copy of `readability_2026-10-03/renumber_equations.py` at the working copy; it was run with `--allow-reorder --redirect 35=46`. | historical |
| `check_c0.py` | Checks the new §C0: unbalanced `$`, doubled spaces, untagged displays, the tag range and the heading list. | historical |
| `c0_install.py` | Installs the working copy into the report (hash-guarded) and updates the files that refer to §C0. | historical |
"""

EDITS = {
    "build/README.md": [
        ("Figures C0.10a–d, §C0 subsections 10.2 (a), 10.3 (b), 10.5 (c) and 10.6 (d)",
         "Figures C0.1–C0.4: C0.1 in §C0 subsections 3.2 and 5.1, C0.2 in 4.3, C0.3 in 5.2 and C0.4 in 5.4", 1),
        ('"§C0 subsection 10", "§C0 subsection 10.3"', '"§C0 subsection 4", "§C0 subsection 4.3"', 1),
    ],
    "build/check_pdf.py": [('"C0. Physics primer"', '"C0. Physics of lidar ranging"', 1)],
    "build/figures/link_budget_scaling.py": [("drawn in Figure C0.10d", "drawn in Figure C0.4", 1)],
    "automotive_perception_report_reading_list_2026-09-28.md": [("§C0 subsection 9", "§C0 subsection 1.2", 3)],
    "automotive_perception_report_readability_review_2026-10-03.md": [
        ("# Readability review of the scientific sections, 2026-10-03\n",
         "# Readability review of the scientific sections, 2026-10-03\n\n"
         "*Section, subsection and equation numbers below are those of the report as reviewed. §C0 was restructured on "
         "12 Oct 2026; `scripts_archive/README.md` maps its old subsections to the new ones.*\n", 1),
    ],
    "scripts_archive/README.md": [
        ("- The build scripts and the installed figure models live in `../build/`.\n",
         "- The build scripts and the installed figure models live in `../build/`.\n"
         "- Section and equation numbers in this index are those of the report when each script ran. §C0 was restructured "
         "on 12 Oct 2026; the table in the section on `c0_restructure_2026-10/` maps its old subsections to the new ones.\n", 1),
        ("a screen-only stylesheet, and a link to the PDF under the disclaimer. | current |",
         "a screen-only stylesheet with screen-sized headings, a floating link back to the contents, and a link to the PDF "
         "under the disclaimer. Source links are made clickable in the build (`autolink_bare_uris` in `build/build_pdf.py`). | current |\n"
         "| `link_audit.py` | Read-only check of the links in `index.html`: kinds of link, relative links to unpublished files, "
         "anchors without a target, malformed URLs and URLs left as plain text. | current |", 1),
    ],
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


report = root / "automotive_perception_report_2026-09-27.md"
raw = report.read_bytes()
assert sha(raw).startswith(expect), f"report sha {sha(raw)[:12]} is not {expect}; nothing written"
new_report = work.read_bytes()

plans = []
for rel, subs in EDITS.items():
    f = root / rel
    b = f.read_bytes()
    t = b.decode("utf-8")
    nl = "\r\n" if "\r\n" in t else "\n"
    for old, new, n in subs:
        old2, new2 = old.replace("\n", nl), new.replace("\n", nl)
        assert t.count(old2) == n, f"{rel}: {old[:60]!r} occurs {t.count(old2)}x, expected {n}"
        t = t.replace(old2, new2)
    if rel == "scripts_archive/README.md":
        t = t.rstrip("\r\n") + nl + ARCHIVE_SECTION.replace("\n", nl)
    plans.append((f, b, t.encode("utf-8")))

if sha(report.read_bytes()) != sha(raw):
    sys.exit("report changed meanwhile; nothing written")
report.write_bytes(new_report)
print(f"report installed: {sha(raw)[:12]} -> {sha(new_report)[:12]}")
for f, b, out in plans:
    if sha(f.read_bytes()) != sha(b):
        sys.exit(f"{f.name} changed meanwhile; stopped")
    f.write_bytes(out)
    print(f"edited {f.relative_to(root)}")
