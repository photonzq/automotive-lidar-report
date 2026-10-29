"""Addition of 2026-10-29 to §C4c subsection 4 ("Ge for direct detection is a different matter"): one bullet pointing
to the TriEye material of §A7.5, where linear-mode germanium photodiodes serve gated imaging.
Writes edits_pointer.json. The report is only read. Usage: python add_c4c_pointer.py [--force]
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = HERE.parent.parent / "automotive_perception_report_2026-09-27.md"
T = REPORT.read_text(encoding="utf-8")

hits = [l for l in T.split("\n") if l.startswith("- Sony's IEDM 2025 (International Electron Devices Meeting) 10 µm Ge-on-Si SPAD")]
assert len(hits) == 1, len(hits)
sony = hits[0]
assert T.count(sony) == 1
POINTER = ("- **Linear-mode Ge photodiodes do serve gated imaging.** TriEye's SWIR image sensor lives with a dark current of "
           "≈200 µA cm⁻² by integrating only during short gates synchronised to its own laser pulses and by subtracting "
           "the dark current inside each pixel (§A7.5).")
edits = [{"id": "P1-C4c-trieye-pointer", "finding": "Pointer from the Ge direct-detection paragraph to §A7.5",
          "old": sony, "new": sony + "\n" + POINTER,
          "why": "A pointer from §C4c subsection 4 to the TriEye material (2026-10-29)."}]

out = HERE / "edits_pointer.json"
assert not out.exists() or "--force" in sys.argv, f"{out.name} exists; pass --force"
out.write_bytes((json.dumps({"block": "trieye_2026-10/pointer", "edits": edits, "skipped": []}, ensure_ascii=False,
                            indent=1) + "\n").encode("utf-8"))
print(out.name, len(edits), "edits")
