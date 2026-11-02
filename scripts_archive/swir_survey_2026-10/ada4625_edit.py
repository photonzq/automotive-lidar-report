"""Add the ADA4625-1 to §S2.8 step 2 of the SWIR side note from its datasheet (Rev. C): a table row, the criteria's
datasheet support, the recommendation (ADA4625-1 first, OPA828 for bandwidth), the crossover and 10 MOhm figures,
the feedback-capacitor bullet (datasheet Eqs. 8-9, phase margin) and its Sources entry. The numbers are printed by
opamp_candidates.py. Usage: ada4625_edit.py <side note .md> <expected sha256 prefix> [--write]
Each anchor must match exactly once and the starting hash must match; writes LF line endings. Special characters are
written as @NAME@ placeholders so that they get the same code points as the rest of the note."""
import hashlib
import sys
from pathlib import Path

note, expected = Path(sys.argv[1]), sys.argv[2]
raw = note.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"side note changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

CHARS = {"@HZ@": "Hz⁻¹ᐟ²", "@OHM@": "Ω", "@DEG@": "°", "@MINUS@": "−",
         "@PM@": "±", "@EN@": "–"}


def u(s):
    for k, v in CHARS.items():
        s = s.replace(k, v)
    assert "@" not in s, s
    return s


def once(anchor):
    n = text.count(anchor)
    assert n == 1, f"found {n} times: {anchor[:80]!r}"
    return text.index(anchor)


def replace(old, new):
    global text
    once(old)
    text = text.replace(old, u(new))


def replace_lines(start_anchor, end_anchor, new):
    """Replace from start_anchor to the end of the line that holds end_anchor."""
    global text
    i = once(start_anchor)
    j = once(end_anchor)
    assert j > i
    k = text.index("\n", j) + 1
    text = text[:i] + u(new) + text[k:]


replace("the criterion excludes bipolar inputs.",
        "the criterion excludes bipolar inputs. The ADA4625-1 datasheet makes the same point for a wideband photodiode "
        "amplifier: with a FET input the op amp's current noise is negligible, and the output noise is dominated by its "
        "voltage noise and the feedback resistor's thermal noise (Rev. C, p. 28) [P].")

replace("| 6.9 | 4.5 | 90 / 91 / 90% | 15 / 4.9 |\n",
        "| 6.9 | 4.5 | 90 / 91 / 90% | 15 / 4.9 |\n"
        "   | ADA4625-1 | JFET, rail-to-rail output; datasheet revised Oct. 2026 | 5.5 / 3.6 / 3.3 | 4.5 | "
        "18 at a gain of 100 | 90 / 91 / 90% | 31 / 9.8 |\n")

replace("AD743 Rev. E, p. 2; OPA828 SBOS671D, p. 5;",
        "AD743 Rev. E, p. 2; ADA4625-1 Rev. C, pp. 3@EN@4, at @PM@18 V; OPA828 SBOS671D, p. 5;")

replace("The status of the TI parts is from TI's product pages [P].",
        "The status of the TI parts is from TI's product pages; for the ADA4625-1 the table gives the date of its latest "
        "datasheet revision (Rev. C, p. 2) [P].")

replace_lines(
    "   - **Recommendation.** All three JFET-input parts in production", "carry the 12.3 V at",
    "   - **Recommendation.** All four JFET-input parts in production meet the criteria from 10 Hz to 1 kHz, and with "
    "any of them the diode keeps 87@EN@91% of the noise power, within 3 percentage points of the AD743.\n"
    "     - The ADA4625-1 is the first choice. Its voltage noise equals the AD743's at 10 and 100 Hz and is "
    "0.1 nV @HZ@ higher at 1 kHz, so the diode keeps the same 90@EN@91% of the noise power, and its gain@EN@bandwidth "
    "product is four times the AD743's. Its output is rail-to-rail: on @PM@18 V it swings to within about 0.3 V of "
    "either rail into 2 k@OHM@ (Rev. C, pp. 1 and 3), so on @PM@15 V rails it lets 10 M@OHM@ carry the 12.3 V at "
    "@MINUS@0.1 V.\n"
    "     - The OPA828 is the choice when bandwidth matters more. Its 45 MHz gives 49 kHz with 3 nF at 1 M@OHM@, "
    "against 31 kHz for the ADA4625-1, while its 7.5 and 4.8 nV @HZ@ at 10 and 100 Hz cost the diode up to "
    "2 percentage points of the noise power.\n"
    "     - The OPA827 and OPA140 also meet the criteria, but neither is quieter than the ADA4625-1 or faster than the "
    "OPA828.\n")

replace_lines("     - Analog Devices' ADA4625-1, quoted at", "could not be checked against its datasheet [S].", "")

replace("up to about 1.5 kHz for the OPA828 and 2 kHz for the AD743.",
        "up to about 1.9 kHz for the ADA4625-1, 2 kHz for the AD743 and 1.5 kHz for the OPA828.")

replace("and with the OPA828 the diode keeps 95% of the noise power at 1 kHz.",
        "and the diode keeps 97% of the noise power at 1 kHz with the ADA4625-1 and 95% with the OPA828.")

i = once("keeps the response flat and stable, where")
j = once("and 3.3 pF and 4.9 kHz.") + len("and 3.3 pF and 4.9 kHz.")
assert j > i
text = text[:i] + u(
    r"keeps the amplifier stable, where $f_{\rm GBW}$ is the op amp's gain@EN@bandwidth product. This value and the "
    r"bandwidth above are Eqs. 8 and 9 of the ADA4625-1 datasheet with $C_s$ as the input capacitance; they leave "
    r"about 45@DEG@ of phase margin and some overshoot, which a larger $C_f$, set on the bench, reduces at some cost in "
    r"bandwidth (Rev. C, pp. 28@EN@29) [P]. For the ADA4625-1's 18 MHz they give 5.2 pF and a 31 kHz bandwidth at "
    r"1 M@OHM@, and 1.6 pF and 9.8 kHz at 10 M@OHM@; for the OPA828's 45 MHz, 3.3 pF and 49 kHz, and 1.0 pF and "
    r"15 kHz; for the AD743's 4.5 MHz, 10 pF and 15 kHz, and 3.3 pF and 4.9 kHz.") + text[j:]

replace("- ADA4625-1 noise and bandwidth as quoted in search extracts, the datasheet not having been retrieved: "
        "https://www.analog.com/en/products/ada4625-1.html",
        "- Analog Devices, ADA4625-1/ADA4625-2 datasheet, Rev. C (Oct. 2026); product page "
        "https://www.analog.com/en/products/ada4625-1.html (pp. 1@EN@4; Eqs. 8@EN@9 and the noise sources of a photodiode "
        "amplifier, p. 28; Figs. 99@EN@101, p. 29)")

new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    note.write_bytes(new)
    print("written")
