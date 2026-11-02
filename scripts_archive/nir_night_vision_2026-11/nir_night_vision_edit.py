"""Explain why active near-infrared night vision did not spread (§A7.5), link §A3 item 1 to it, extend the §A7.7 table,
add the sources, and add the public-domain sentence to the report's disclaimer.
Usage: nir_night_vision_edit.py <report.md> <expected sha256 prefix> [--write]
Each (old, new) pair must match exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

HELD_BACK = (
    "- **What held them back.** The invisible beam dazzles no one, but the camera itself can be dazzled, and the "
    "systems met the same headwinds as thermal ones.\n"
    "  - *Glare in the image.* Bright oncoming lights drive the camera's pixels to saturation and make the image "
    "unclear. Ford's patent on the problem states that a pulsed laser illuminator, with a matching duty cycle and a "
    "band-pass filter, removes the effect of oncoming headlamps but not that of retroreflective road signs, and that "
    "the large flat sides of trucks, buses and vans also saturate the image. It also claims to keep a car's own "
    "illuminator from blinding the night-vision systems of oncoming cars, a problem that would grow with the number "
    "of equipped cars (US 7,195,379 B2, filed Jan 2005) [P].\n"
    "  - *Weather.* A continuous beam lights the fog, rain or snow in front of the car, and the backscatter veils the "
    "image; Grauer's comparison of gated with continuous illumination below quantifies it [I].\n"
    "  - *Detection distance.* In a 2004 University of Michigan study, drivers watching video recorded simultaneously "
    "from an NIR and a thermal system detected pedestrians farther away with the thermal image, in both a younger and "
    "an older group (Tsimhoni et al., UMTRI-2004-38) [S, abstract as indexed].\n"
    "  - *Display and value.* Like thermal systems, they show a video that the driver must look away from the road to "
    "see (§A3, item 4), and they help mainly on unlit roads (§A3, item 3).\n"
    "  - *Outcome.* Lexus dropped the option for lack of buyers, and Mercedes added a thermal camera in 2013, which "
    "also detects animals, before dropping night vision from the 2021 S-Class (above; §A1). Adaptive driving beams "
    "now put high-beam light on the road without dazzling others, the benefit that an NIR beam gave only to the "
    "camera, now delivered to the driver's own eyes (§A6.3) [E]."
)

WHY_WORKS = ("- **Why it works.** An NIR high beam puts high-beam-like illuminance on the pedestrian without dazzling "
             "anyone, so the camera works with the photon budget of the hotspot rather than of the glare-limited zone "
             "(§A7.1) [E].")

PAIRS = [
    # disclaimer: the existing text stays and the public-domain sentence is appended
    ("so check those before relying on a figure.\n:::",
     "so check those before relying on a figure. It is dedicated to the public domain under CC0 1.0; no copyright is "
     "reserved.\n:::"),
    # §A3 item 1
    ("- NIR systems (Mercedes, Toyota) avoided this because a silicon camera works through glass, at the price of "
     "losing thermal contrast.",
     "- Active near-infrared (NIR) systems (Mercedes, Toyota) avoided this: they light the road with invisible NIR "
     "lamps and film it with a silicon camera, which works through glass, at the price of losing thermal contrast "
     "(§A7.5)."),
    # §A7.5: new bullet after "Why it works"
    (WHY_WORKS, WHY_WORKS + "\n" + HELD_BACK),
    # §A7.7 table
    ("| NIR lamps + silicon camera | Light reflected from its own invisible lamps | Yes | Lamp power, eye safety, fog "
     "backscatter |",
     "| NIR lamps + silicon camera | Light reflected from its own invisible lamps | Yes | Lamp power, eye safety, fog "
     "backscatter, saturation by oncoming lights and retroreflective signs (§A7.5) |"),
    # §A7 sources line
    ("https://platformselect.autonomoustuff.com/wp-content/uploads/2019/05/flir-adk-datasheet-whitelabel.pdf (FLIR ADK)",
     "https://platformselect.autonomoustuff.com/wp-content/uploads/2019/05/flir-adk-datasheet-whitelabel.pdf (FLIR ADK) ; "
     "https://patents.google.com/patent/US7195379B2/en (Ford, US 7,195,379 B2, anti-blinding system for NIR night "
     "vision) ; https://deepblue.lib.umich.edu/handle/2027.42/55202 (Tsimhoni et al., UMTRI-2004-38, NIR and FIR "
     "pedestrian detection)"),
]
for old, new in PAIRS:
    n = text.count(old)
    assert n == 1, f"found {n} times: {old[:80]!r}"
    text = text.replace(old, new)
assert "\n\n\n" not in text
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
