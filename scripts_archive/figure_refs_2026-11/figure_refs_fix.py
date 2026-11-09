"""Bring the equation and §C0 subsection numbers quoted by hand in the figure scripts up to date.

- build/figures/night_photon_budget.py: the docstring's list of §A7 equations still carried the numbers (13)-(21) it
  had when §A7 was written; they are now (20)-(28), and the thermal SNR (27) comes before the SPAD power (28).
- build/figures/link_budget_scaling.py, fmcw_tof_system_budget.py and coherent_mode_coverage.py, and
  link_budget_scaling_tables.txt: references to §C0 subsections from before the 2026-10-12 restructure ("subsection
  10", "10.3", "10.4", "10.6", "8"), mapped by content with the old-to-new table of scripts_archive/README.md: the
  bright-sun background and live fraction -> 4.2; detection statistics, false-alarm rule and the 120 photoelectrons ->
  4.3; the 21.7-count detection level -> 4.3 and 5.1; margin at short range -> 5.4; the rain extinction law -> 3.3;
  the link-budget model as a whole -> 3.1-6.1.
Comments, docstrings and one printed header line change; no computed value changes, so no figure is redrawn.

Usage: figure_refs_fix.py <report folder> [--write]
Each anchor must occur the stated number of times; files keep their LF line endings. Without --write it only checks.
"""
import sys
from pathlib import Path

folder = Path(sys.argv[1])
write = "--write" in sys.argv[2:]
figs = folder / "build" / "figures"

EDITS = {
    figs / "link_budget_scaling.py": [
        ("Companion to section C0 subsection 10 of automotive_perception_report_2026-09-27.md.",
         "Companion to section C0 (subsections 3.1-6.1) of automotive_perception_report_2026-09-27.md.", 1),
        ("0.05 x 0.05 deg macro-pixel, section C0 subsection 10.3)",
         "0.05 x 0.05 deg macro-pixel, section C0 subsection 4.2)", 1),
        ("120 photoelectrons a point needs (section C0 subsection 10.3)",
         "120 photoelectrons a point needs (section C0 subsection 4.3)", 1),
        ("ToF bright-sun background per 1 ns bin (section C0 subsection 10.3)",
         "ToF bright-sun background per 1 ns bin (section C0 subsection 4.2)", 1),
        ("the ToF model's count (21.7, section C0 subsection 10.4)",
         "the ToF model's count (21.7, section C0 subsections 4.3 and 5.1)", 1),
        ("margin, fixed losses, fog and rain (C0 subsection 10.6)",
         "margin, fixed losses, fog and rain (C0 subsection 5.4)", 1),
        ("1.076 R^0.67 dB/km (subsection 8).",
         "1.076 R^0.67 dB/km (section C0 subsection 3.3).", 1),
        ('"Link budget tables (companion to C0 subsection 10) [E]",',
         '"Link budget tables (companion to C0 subsections 3.1-6.1) [E]",', 1),
    ],
    folder / "automotive_perception_report_figures" / "link_budget_scaling_tables.txt": [
        ("Link budget tables (companion to C0 subsection 10) [E]",
         "Link budget tables (companion to C0 subsections 3.1-6.1) [E]", 1),
    ],
    figs / "fmcw_tof_system_budget.py": [
        ("section C0 subsection 10.3", "section C0 subsection 4.3", 3),
    ],
    figs / "coherent_mode_coverage.py": [
        ("the 940 nm SPAD ToF model of sections C0 subsection 10 and C7a",
         "the 940 nm SPAD ToF model of section C0 (subsections 4.2-5.1) and section C7a", 1),
    ],
}

# night_photon_budget.py: renumber the docstring's equation list by content and put it in the report's order
NIGHT = figs / "night_photon_budget.py"
NEW_NUMBER = {  # old number in the docstring -> current number, by the equation each line describes
    13: 20,  # image-plane illuminance        eq:image-plane-illuminance
    14: 21,  # photoelectrons per readout     eq:night-photoelectrons-per-pixel
    15: 22,  # SNR per readout                eq:snr-one-readout
    16: 23,  # SNR over M readouts            eq:snr-summed-readouts
    17: 24,  # photon-counting gain           eq:photon-counting-gain
    18: 25,  # burst of K readouts            eq:burst-readout-gain
    19: 26,  # dark rate versus temperature   eq:dark-signal-temperature
    20: 28,  # SPAD power at the count ceiling eq:spad-array-avalanche-power
    21: 27,  # thermal SNR per pixel          eq:thermal-snr
}
KEYWORDS = {13: "image-plane illuminance", 14: "photoelectrons per readout", 15: "SNR per readout",
            16: "SNR over M readouts", 17: "photon-counting gain", 18: "burst of K readouts",
            19: "dark rate versus temperature", 20: "SPAD power at the count ceiling", 21: "thermal SNR per pixel"}


def load(path):
    """Scripts must be LF. A tables file keeps whatever line endings it has (the repo stores text as LF either
    way), since each replacement stays within one line."""
    text = path.read_bytes().decode("utf-8")
    if path.suffix == ".py":
        assert "\r" not in text, f"{path.name}: expected LF line endings"
    return text


out = {}
for path, pairs in EDITS.items():
    text = load(path)
    for old, new, count in pairs:
        n = text.count(old)
        assert n == count, f"{path.name}: {old[:60]!r} found {n} times, expected {count}"
        text = text.replace(old, new)
    out[path] = text

text = load(NIGHT)
lines = text.split("\n")
start = next(i for i, ln in enumerate(lines) if ln.startswith("  (13) image-plane illuminance"))
block = lines[start:start + 9]
renumbered = []
for k, ln in enumerate(block):
    old_n = 13 + k
    assert ln.startswith(f"  ({old_n}) {KEYWORDS[old_n]}"), f"unexpected docstring line: {ln!r}"
    renumbered.append((NEW_NUMBER[old_n], ln.replace(f"  ({old_n}) ", f"  ({NEW_NUMBER[old_n]}) ", 1)))
renumbered.sort()
lines[start:start + 9] = [ln for _, ln in renumbered]
out[NIGHT] = "\n".join(lines)

for path, text in out.items():
    print(f"{path.relative_to(folder)}: ok")
print("\n".join(ln for _, ln in renumbered))
if write:
    for path, text in out.items():
        path.write_bytes(text.encode("utf-8"))
    print("written")
else:
    print("check only (add --write to apply)")
