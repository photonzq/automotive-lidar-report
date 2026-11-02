"""Replace the op-amp bullets of §S2.8 step 2 in the SWIR side note with explicit criteria, a table of current
JFET- and CMOS-input candidates (the AD743 for reference) and a recommendation, and add their datasheets to Sources.
Usage: opamp_edit.py <side note .md> <expected sha256 prefix> [--write]
Each (old, new) pair must match exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

note, expected = Path(sys.argv[1]), sys.argv[2]
raw = note.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"side note changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

OLD_BULLETS = """   - With $R_f=1$ MΩ the resistor costs 8% of the diode's noise power, which the dummy measurement removes. The op amp's bias and current noise do not matter here: the AD743's 150 pA bias puts 0.15 mV on the output, and its 6.9 fA Hz⁻¹ᐟ² is 0.3% of the resistor's noise power (AD743 datasheet, p. 2) [P].
   - Its voltage noise does matter. The AD743, the JFET-input amplifier that the SR570 itself uses (§S2.5), has 3.2 nV Hz⁻¹ᐟ² at 1 kHz and adds $7.4\\times10^{-14}$ A Hz⁻¹ᐟ² there; the diode keeps about 90% of the total noise power from 10 Hz to 1 kHz. The electrometer-grade OPA928, with 18 nV Hz⁻¹ᐟ² at 100 Hz and 15 at 1 kHz (TI SBOSA77A, p. 4), adds $3.5\\times10^{-13}$ at 1 kHz and leaves the diode 60%. The general-purpose CMOS LMC662, with 22 nV Hz⁻¹ᐟ² (TI SNOSC51D, p. 6), adds $5.1\\times10^{-13}$, more than the diode's own noise, and leaves it 42%. The ADA4530-1 is in the same class as the OPA928, at 14 nV Hz⁻¹ᐟ² quoted for 10 kHz [S]. The femtoampere bias currents of these parts buy nothing at 1 MΩ.
   - The Johnson noise of $R_f$ is the largest excess term only while $e_n|Y|$ stays below it, which for the AD743 holds up to about 2 kHz. Above that, $e_n\\,2\\pi fC_s$ keeps growing, and at 10 kHz it exceeds the diode's own noise.
   - The choice reverses for a pixel-sized diode. At 15 µm the same $R_0A$ gives $R_0\\approx3.6\\times10^{8}$ Ω, about 0.7 pF and a thermal floor of 6.8 fA Hz⁻¹ᐟ². The AD743's current noise alone would double that floor, so an electrometer amplifier with $R_f\\approx10$ GΩ is the right choice there; it turns the 277 pA dark current at −0.1 V into 2.8 V.
   - $R_f=1$ MΩ is set by the dark current. At −0.1 V the 1.23 µA becomes 1.23 V, whereas 10 MΩ would need a 12.3 V swing, more than ±9 V battery rails allow. At 0 V no dark current flows, and 10 MΩ cuts the resistor's share to 0.8%.
   - With 3 nF at the input, a feedback capacitor $C_f\\approx\\sqrt{C_s/(2\\pi R_ff_{\\rm GBW})}$ keeps the response flat and stable, where $f_{\\rm GBW}$ is the op amp's gain–bandwidth product. For the AD743's 4.5 MHz (p. 2) that is 10 pF and a 16 kHz bandwidth at 1 MΩ, and 3.3 pF and 4.9 kHz at 10 MΩ."""

NEW_BULLETS = """   - **Criteria at $R_f=1$ MΩ** [E, `opamp_candidates.py`]. The resistor costs 8% of the diode's noise power, which the dummy measurement removes, and the op amp should add no more than the resistor does.
     - *Voltage noise decides.* The current $e_n|Y|$ should not exceed the resistor's 128 fA Hz⁻¹ᐟ², which allows $e_n$ up to 9.5 nV Hz⁻¹ᐟ² at 10–100 Hz and 5.5 nV Hz⁻¹ᐟ² at 1 kHz, and only 2.2 nV Hz⁻¹ᐟ² at 3 kHz, where $C_s$ takes over. The imager integrates over a noise bandwidth of about 250 Hz (§S2.5), so the voltage noise at 10–100 Hz, and with it the 1/f corner, counts as much as the value at 1 kHz.
     - *Current noise hardly matters.* It should stay below a third of the resistor's noise, 43 fA Hz⁻¹ᐟ², which every FET-input part in the table meets by a factor of 6 or more; the criterion excludes bipolar inputs.
     - *Bias current does not matter.* The AD743's 150 pA puts 0.15 mV on the output (AD743 datasheet, p. 2) [P].
     - *The gain–bandwidth product sets the bandwidth* with 3 nF at the input, $f_{\\rm BW}\\approx\\sqrt{f_{\\rm GBW}/(2\\pi R_fC_s)}$.
     - *The part should be in production.* The AD743 that the SR570 uses (§S2.5) is listed by Analog Devices as not recommended for new designs [S].

   | Op amp | Input; status | $e_n$ at 10 Hz / 100 Hz / 1 kHz (nV Hz⁻¹ᐟ²) | $i_n$ at 1 kHz (fA Hz⁻¹ᐟ²) | Gain–bandwidth (MHz) | Diode's share of the noise power at 10 Hz / 100 Hz / 1 kHz | Bandwidth with 3 nF at 1 MΩ / 10 MΩ (kHz) |
   |---|---|---|---|---|---|---|
   | AD743 | JFET; not recommended for new designs | 5.5 / 3.6 / 3.2 | 6.9 | 4.5 | 90 / 91 / 90% | 15 / 4.9 |
   | OPA828 | JFET; active | 7.5 / 4.8 / 4.0 | 1.2 | 45 | 88 / 91 / 89% | 49 / 15 |
   | OPA827 | JFET; active | ≈9 / ≈5 / 4.0 | 2.2 | 22 | 87 / 91 / 89% | 34 / 11 |
   | OPA140 | JFET, rail-to-rail output; active | 8.0 / 5.8 / 5.1 | 0.8 | 11 | 88 / 90 / 87% | 24 / 7.6 |
   | OPA1656 | CMOS; active | – / 11.8 / 4.3 | 6 | 53 at a gain of 100 | – / 83 / 88% | 53 / 17 |

   Typical values at 25 °C from the datasheets: AD743 Rev. E, p. 2; OPA828 SBOS671D, p. 5; OPA827 SBOS376I, p. 6, with its 10 and 100 Hz values read by eye from Fig. 1 on p. 8; OPA140 SBOS498F, p. 7; OPA1656 SBOS901C, p. 6 [P]. The status of the TI parts is from TI's product pages [P]. The shares and bandwidths are for $R_0=81.3$ kΩ, $C_s=3$ nF and $R_f=1$ or 10 MΩ [E, `opamp_candidates.py`].
   - **Recommendation.** All three JFET-input parts in production meet the criteria from 10 Hz to 1 kHz, and with any of them the diode keeps 87–91% of the noise power, within 3 percentage points of the AD743.
     - The OPA828 is the first choice. Of the three it has the lowest voltage noise at 10–100 Hz, specified in its table rather than read from a curve, and the widest bandwidth with 3 nF.
     - The OPA140 is the alternative when a rail-to-rail output is wanted. Its output reaches within 0.2 V of the rails (SBOS498F, p. 7), so on ±15 V rails it lets 10 MΩ carry the 12.3 V at −0.1 V.
     - The CMOS-input OPA1656 is quieter above a few kilohertz, 2.9 nV Hz⁻¹ᐟ² at 10 kHz, but its 1/f noise, 11.8 nV Hz⁻¹ᐟ² at 100 Hz, fails the criterion in the band the imager uses.
     - Analog Devices' ADA4625-1, quoted at 3.3 nV Hz⁻¹ᐟ² at 1 kHz with an 18 MHz gain–bandwidth product, belongs in the same group, but its low-frequency noise could not be checked against its datasheet [S].
   - **Electrometer-grade and general-purpose CMOS parts fail on voltage noise.** The OPA928, with 18 nV Hz⁻¹ᐟ² at 100 Hz and 15 at 1 kHz (TI SBOSA77A, p. 4), leaves the diode 73% and 60% of the noise power. The LMC662, with 22 nV Hz⁻¹ᐟ² (TI SNOSC51D, p. 6), adds more than the diode's own noise at 1 kHz and leaves it 42%. The ADA4530-1 is in the same class as the OPA928, at 14 nV Hz⁻¹ᐟ² quoted for 10 kHz [S]. Their femtoampere bias currents buy nothing at 1 MΩ.
   - The Johnson noise of $R_f$ is the largest excess term only while $e_n|Y|$ stays below it: up to about 1.5 kHz for the OPA828 and 2 kHz for the AD743. Above that, $e_n\\,2\\pi fC_s$ keeps growing, and at 10 kHz it exceeds the diode's own noise.
   - The choice reverses for a pixel-sized diode. At 15 µm the same $R_0A$ gives $R_0\\approx3.6\\times10^{8}$ Ω, about 0.7 pF and a thermal floor of 6.8 fA Hz⁻¹ᐟ². The AD743's 6.9 fA Hz⁻¹ᐟ² of current noise alone would double that floor, so an electrometer amplifier with $R_f\\approx10$ GΩ is the right choice there; it turns the 277 pA dark current at −0.1 V into 2.8 V.
   - $R_f=1$ MΩ is set by the dark current. At −0.1 V the 1.23 µA becomes 1.23 V, whereas 10 MΩ would need a 12.3 V swing, more than ±9 V battery rails allow. At 0 V no dark current flows, and 10 MΩ cuts the resistor's share to 0.8%. The op amp's voltage noise is then the larger excess term, and with the OPA828 the diode keeps 95% of the noise power at 1 kHz.
   - With 3 nF at the input, a feedback capacitor $C_f\\approx\\sqrt{C_s/(2\\pi R_ff_{\\rm GBW})}$ keeps the response flat and stable, where $f_{\\rm GBW}$ is the op amp's gain–bandwidth product. For the OPA828's 45 MHz that is 3.3 pF and a 49 kHz bandwidth at 1 MΩ, and 1.0 pF and 15 kHz at 10 MΩ; for the AD743's 4.5 MHz it is 10 pF and 15 kHz, and 3.3 pF and 4.9 kHz."""

OLD_SRC = "- Texas Instruments, LMC660/LMC662 datasheet, SNOSC51D (Feb. 2024): https://www.ti.com/lit/ds/symlink/lmc662.pdf (p. 6)"
NEW_SRC = (OLD_SRC + "\n"
           "- Texas Instruments, OPA828 datasheet, SBOS671D (Dec. 2022): https://www.ti.com/lit/ds/symlink/opa828.pdf (p. 5; Fig. 6-1, p. 8)\n"
           "- Texas Instruments, OPA827 datasheet, SBOS376I (Jul. 2016): https://www.ti.com/lit/ds/symlink/opa827.pdf (p. 6; Fig. 1, p. 8)\n"
           "- Texas Instruments, OPA140 datasheet, SBOS498F (Mar. 2023): https://www.ti.com/lit/ds/symlink/opa140.pdf (p. 7)\n"
           "- Texas Instruments, OPA1656 datasheet, SBOS901C (Sep. 2022): https://www.ti.com/lit/ds/symlink/opa1656.pdf (p. 6; Fig. 6-1, p. 8)\n"
           "- Product status: TI product pages, all listed as active: https://www.ti.com/product/OPA828 ; https://www.ti.com/product/OPA827 ; "
           "https://www.ti.com/product/OPA140 ; https://www.ti.com/product/OPA1656 . Analog Devices, AD743 (not recommended for new "
           "designs, as quoted in search extracts): https://www.analog.com/en/products/ad743.html\n"
           "- ADA4625-1 noise and bandwidth as quoted in search extracts, the datasheet not having been retrieved: "
           "https://www.analog.com/en/products/ada4625-1.html")

for old, new in ((OLD_BULLETS, NEW_BULLETS), (OLD_SRC, NEW_SRC)):
    n = text.count(old)
    assert n == 1, f"found {n} times: {old[:80]!r}"
    text = text.replace(old, new)
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    note.write_bytes(new)
    print("written")
