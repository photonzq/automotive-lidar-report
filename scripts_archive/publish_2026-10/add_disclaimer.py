"""Insert the AI-use disclaimer the author asked for (10 Oct 2026) right after the report's subtitle, hash-guarded.

The disclaimer is a pandoc fenced div with class "disclaimer"; build/build_pdf.py moves it onto the title page,
between the subtitle and the contents.

Usage:
    python add_disclaimer.py --report <report.md> --expect <sha256 prefix> [--dry]
"""
import argparse
import hashlib
import sys
from pathlib import Path

TEXT = ("**Disclaimer.** This report was created with AI assistance. It may contain errors: each statement carries "
        "an evidence tag and, where possible, a source, so check those before relying on a figure.")

ap = argparse.ArgumentParser()
ap.add_argument("--report", required=True)
ap.add_argument("--expect", required=True)
ap.add_argument("--dry", action="store_true")
args = ap.parse_args()

RP = Path(args.report)
raw = RP.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
if not h0.startswith(args.expect):
    sys.exit(f"ABORT: report sha {h0[:12]} is not the expected {args.expect}")
L = raw.decode("utf-8").split("\n")
if any(l.startswith("::: {.disclaimer}") for l in L):
    sys.exit("ABORT: a disclaimer block is already present")
assert L[0].startswith("# Automotive Night Vision") and L[1].startswith("## Technology routes"), L[:2]
new = L[:2] + ["", "::: {.disclaimer}", TEXT, ":::"] + L[2:]
out = "\n".join(new).encode("utf-8")
print(f"{h0[:12]} -> {hashlib.sha256(out).hexdigest()[:12]}")
if args.dry:
    sys.exit(0)
if hashlib.sha256(RP.read_bytes()).hexdigest() != h0:
    sys.exit("ABORT: report changed during processing")
RP.write_bytes(out)
print("written")
