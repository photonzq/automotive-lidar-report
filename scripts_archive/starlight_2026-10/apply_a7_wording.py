"""Wording corrections in section A7 after re-reading the sources: the Mercedes test phrasing, the gloss on LED-flicker
mitigation, and the USML wording for intensified viewers. Hash-guarded.
Usage: python apply_a7_wording.py <expected sha prefix>
"""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
assert h0.startswith(sys.argv[1]), f"report changed: {h0[:12]}"
text = raw.decode("utf-8")
EDITS = [
    ("In Mercedes's tests drivers recognized dark-clothed dummies at 160 m instead of 70 m with bi-xenon low beams, "
     "and in 2010 more than half of S-Class buyers ordered the option [P].",
     "In Mercedes's tests, pedestrians in dark clothing were detected at 160 m instead of 70 m with bi-xenon low "
     "beams, and in 2010 more than half of S-Class buyers ordered the option [P]."),
    ("  - In the developers' tests, drivers recognized dummies in light clothing beyond 200 m, about 40 m earlier than "
     "with bi-xenon low beams, and dummies in dark clothing at 160 m against 70 m [P, Deutscher Zukunftspreis 2006].",
     "  - In the developers' tests, test drivers saw dummies in light clothing from beyond 200 m, about 40 m earlier "
     "than with bi-xenon low beams, and pedestrians in dark clothing were detected at 160 m against 70 m [P, Deutscher "
     "Zukunftspreis 2006]."),
    ("delivers 120 dB of dynamic range together with LED-flicker mitigation (a long-exposure readout that never misses "
     "the on-phase of pulsed LED lights)",
     "delivers 120 dB of dynamic range together with LED-flicker mitigation (imaging pulsed LED lights without the "
     "flicker that short exposures produce)"),
    ("and goggles with Gen 3 or better tubes fall under USML Category XII [P].",
     "and goggles and similar viewers with an autogated third-generation or later tube fall under USML Category "
     "XII(c) [P]."),
]
out = text
for old, new in EDITS:
    assert out.count(old) == 1, (out.count(old), old[:70])
    out = out.replace(old, new)
REPORT.write_bytes(out.encode("utf-8"))
print("written; sha", hashlib.sha256(out.encode("utf-8")).hexdigest()[:12])
