"""Write the Round 1 'needs_source' items of each group of edit lists to sources/<group>_items.md, numbered.

Each research agent of Round 4 gets one file. Groups follow the report blocks of the edit lists.
Usage: python split_needs_source.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GROUPS = {
    "R1_partA_E2-E5": ["01_A3-A6_E2-E5"],
    "R2_C0_C4": ["02_C0_parts1-9", "03_C0_part10", "04_C4_C4b_C4c"],
    "R3_C4d-C9_C5-C6": ["05_C4d_C8_C9", "06_C5_C5a_C6"],
    "R4_C7-C7b_F6": ["07_C7_C7a_F6", "08_C7b"],
    "R5_C10_part1": ["09_C10_part1"],
    "R6_C10_part2": ["10_C10_part2"],
    "R7_E9-E12": ["11_E9-E12"],
}
out_dir = HERE / "sources"
out_dir.mkdir(exist_ok=True)
for group, stems in GROUPS.items():
    lines = [f"# Round 4 source items: {group}", ""]
    n = 0
    for stem in stems:
        data = json.loads((HERE / "edits" / f"{stem}.json").read_text(encoding="utf-8"))
        for s in data.get("skipped", []):
            if s.get("kind") != "needs_source":
                continue
            n += 1
            lines += [f"## {group}-{n:02d} [{stem}] {s.get('finding', '')}", "",
                      f"- **Where:** {s.get('location', '')}", f"- **What is needed:** {s.get('detail', '')}", ""]
    (out_dir / f"{group}_items.md").write_text("\n".join(lines), encoding="utf-8")
    print(group, n)
