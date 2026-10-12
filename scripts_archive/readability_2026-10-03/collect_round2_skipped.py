"""List the items the Round 2 agents skipped as needs_decision or needs_source, for the author's decision list.

Usage: python collect_round2_skipped.py [kind ...]   (default kinds: needs_decision needs_source)
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
kinds = sys.argv[1:] or ["needs_decision", "needs_source"]
for p in sorted((Path(__file__).resolve().parent / "edits" / "round2").glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, list):
        continue
    for s in data.get("skipped", []):
        if s.get("kind") in kinds:
            print(f"[{p.stem}] {s.get('kind')} | {s.get('finding', '')[:110]}\n  @ {s.get('location', '')[:200]}\n"
                  f"  {s.get('detail', '')[:600]}\n")
