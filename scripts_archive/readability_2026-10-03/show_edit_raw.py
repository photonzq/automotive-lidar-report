"""Print the raw "old" and "new" text of selected edits, to prepare exact-substring amendments.

Usage: python show_edit_raw.py edits/<list>.json <id suffix> [<id suffix> ...]
An id suffix such as -005 matches the edit whose id ends with it.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
edits = data if isinstance(data, list) else data["edits"]
for suffix in sys.argv[2:]:
    for e in edits:
        if e["id"].endswith(suffix):
            print(f"===== {e['id']}\n--- OLD:\n{e['old']}\n--- NEW:\n{e['new']}\n")
