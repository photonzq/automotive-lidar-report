"""Round 2, agent R2E_C10, second list: decision 1 of round2_spec.md (one FMCW dwell, T_dwell = T_int + 2 tau,
§C7b Eq. (107)) in sections C10-C10.7, outside the spans of the first list (R2E_C10.json, which carries the dwell in
§C10.2 item 5 itself).

At 200 m, 2 tau = 2 x 2 x 200 m / c = 2.67 us. Numbers from R2E_C10_numbers.py (section "decision 1").
Reads the live report (read only), cuts each "old" span by anchors, checks one occurrence inside C10 and no overlap
with this list or with R2E_C10.json, and writes edits/round2/R2E2_C10_dwell.json.
Usage: python R2E2_C10_dwell_build_edits.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / "automotive_perception_report_2026-09-27.md"
EDITS = ROOT / "scripts_archive" / "readability_2026-10-03" / "edits" / "round2"
OUT = EDITS / "R2E2_C10_dwell.json"
text = REPORT.read_text(encoding="utf-8")
lo, hi = text.index("## C10. Can optical phased arrays"), text.index("# Part D")
edits = []
D1 = "decision 1 (FMCW dwell T_int + 2 tau, §C7b Eq. (107))"


def span(start, end):
    assert text.count(start) == 1, ("start", start[:60], text.count(start))
    i = text.index(start)
    return text[i:text.index(end, i) + len(end)]


def rep(old, pairs):
    new = old
    for a, b in pairs:
        assert new.count(a) == 1, ("rep", a[:70], new.count(a))
        new = new.replace(a, b)
    return new


def add(finding, old, new, why):
    assert text.count(old) == 1, ("old", old[:70], text.count(old))
    i = text.index(old)
    assert lo <= i and i + len(old) <= hi, ("outside C10", old[:60])
    edits.append({"id": f"R2E2_C10_dwell-{len(edits) + 1:03d}", "finding": finding, "old": old, "new": new, "why": why})


# ---------------------------------------------------------------- §C10.2 item 7
old = span(r"**7. Point rate.** A single-beam FMCW OPA is limited to about $1/T_{\rm dwell}$", r"$1/2\ \mu{\rm s}=0.5$ Mpts/s).")
add(f"{D1}: §C10.2 item 7, single-beam point rate", old,
    r"**7. Point rate.** A single-beam FMCW OPA is limited to about $1/T_{\rm dwell}$, where the dwell $T_{\rm dwell}=T_{\rm int}+2\tau$ is how long the beam stays on one point (§C7b, Eq. (107)): the chirp time $T_{\rm int}$ of an up- and a down-ramp, plus the round trip $\tau=2R/c$ that opens each ramp before the echo arrives, $2\tau=2\times2\times200\ {\rm m}/(3\times10^{8}\ {\rm m\,s^{-1}})=2.67$ µs at 200 m. At 2–10 µs of chirp that is **0.079–0.21 Mpts/s** ($1/(10+2.67)\ \mu{\rm s}=1/12.67\ \mu{\rm s}=0.079$ Mpts/s and $1/(2+2.67)\ \mu{\rm s}=1/4.67\ \mu{\rm s}=0.21$ Mpts/s).",
    "Dwell = chirp + 2 tau; point rate 0.079-0.21 Mpts/s.")

old = span(r"- One sample per 0.05° cell over the full field (12 Mpts/s) would need **24–120 parallel coherent channels**", r"and 120 at 10 µs.")
add(f"{D1}: §C10.2 item 7, channel count", old,
    r"- One sample per 0.05° cell over the full field (12 Mpts/s) would need **56–152 parallel coherent channels** at 2–10 µs of chirp. The number of channels is the required point rate $\dot N$ times the dwell: $N_{\rm ch}=\dot N\,T_{\rm dwell}=12\times10^{6}\ {\rm s^{-1}}\times4.67\ \mu{\rm s}=56$, and $12\times10^{6}\ {\rm s^{-1}}\times12.67\ \mu{\rm s}=152$ at 10 µs of chirp.",
    "Channels = point rate x dwell at the dwell of Eq. (107).")

old = span(r"Shorter dwell (a shorter chirp) raises the beat frequency", r"each ramp is half as long")
add(f"{D1}: §C10.2 item 7, beat paragraph", old,
    rep(old, [("Shorter dwell (a shorter chirp) raises the beat frequency", "A shorter chirp raises the beat frequency"),
              ("If the dwell is split into an up-ramp and a down-ramp, each ramp is half as long",
               "If the chirp time is split into an up-ramp and a down-ramp, as the dwell above assumes, each ramp's chirp is half as long")]),
    "The beat depends on the chirp, not on the whole dwell.")

# ---------------------------------------------------------------- §C10.3a item 5
old = span("| Coherent, scanned monostatic: 20 mm aperture, 128 channels × (0.1 s ÷ 10 µs)", "| Same with 2 µs dwell | 1.2×10⁸ | 6.4×10⁶ | ≈5% |")
add(f"{D1}: §C10.3a item 5 table", old,
    "| Coherent, scanned monostatic: 20 mm aperture, 128 channels × (0.1 s ÷ 12.67 µs dwell for 10 µs of chirp) | 1.2×10⁸ | 1.0×10⁶ | ≈0.8% |\n| Same with 2 µs of chirp (4.67 µs dwell) | 1.2×10⁸ | 2.7×10⁶ | ≈2.3% |",
    "Slots per frame at the dwell of Eq. (107).")

old = span(r"coherent $128\times(0.1\ {\rm s}/10\ \mu{\rm s})=1.28\times10^{6}$", r"$0.1\ {\rm s}/2\ \mu{\rm s}=5\times10^{4}$ dwells).")
add(f"{D1}: §C10.3a item 5 derivation", old,
    r"coherent $128\times(0.1\ {\rm s}/12.67\ \mu{\rm s})=128\times7{,}890=1.01\times10^{6}$ (0.1 s is one frame at 10 Hz, and $12.67\ \mu{\rm s}=10\ \mu{\rm s}+2\tau$ is the dwell of §C7b, Eq. (107), with $2\tau=2.67$ µs at 200 m), or $128\times2.14\times10^{4}=2.74\times10^{6}$ for 2 µs of chirp ($0.1\ {\rm s}/4.67\ \mu{\rm s}=2.14\times10^{4}$ dwells).",
    "Substitutions for the table rows.")

add(f"{D1}: §C10.3a item 5 derivation",
    r"- Nominal footprint fraction, available over required: $1.28\times10^{6}/1.2\times10^{8}=1.1\%$ and $6.4\times10^{6}/1.2\times10^{8}=5.4\%$.",
    r"- Nominal footprint fraction, available over required: $1.01\times10^{6}/1.2\times10^{8}=0.84\%$ and $2.74\times10^{6}/1.2\times10^{8}=2.3\%$.",
    "Footprint fractions from the slots above.")

old = span(r"would need about 2,400–12,000 parallel channels by this mode count", r"this is also why the table shows ≈1% where §C10.3b's Result 2 shows 2.1%.")
add(f"{D1}: §C10.3a item 5, channels for full coverage", old,
    r"would need about 5,600–15,200 parallel channels by this mode count ($1.2\times10^{8}$ slots divided by $2.14\times10^{4}$ or $7{,}890$ dwells per channel per frame, for 4.67 µs or 12.67 µs dwells, i.e. 2 µs or 10 µs of chirp). The footprint count of §C10.3b gives about half that, ≈2,700–7,300: the $1.2\times10^{6}$ cells, divided by the 2.1% footprint fraction of one sample at 200 m (§C10.3b, Result 2; 2.08% unrounded), need $1.2\times10^{6}/0.0208=5.77\times10^{7}$ samples per frame, and $5.77\times10^{7}/2.14\times10^{4}=2{,}700$ and $5.77\times10^{7}/7{,}890=7{,}300$ channels. The factor of two arises because one nominal footprint spans ≈2 hard-aperture modes at 200 m. It is also why the table's ≈0.8% is half the 1.75% that §C10.3b's per-sample footprint gives for the same $1.01\times10^{6}$ samples per frame ($2.08\%\times1.01\times10^{6}/1.2\times10^{6}=1.75\%$).",
    "Channel counts at the dwell of Eq. (107); the comparison with Result 2 restated for the samples the channels supply.")

old = span(r"[E: 128 channels at 10 µs give $1.28\times10^{6}$ samples per frame, a 0.048° mesh.", r"slightly overfilling a 0.05° cell (17.5 cm).")
add(f"{D1}: §C10.3a item 5, area-matched alternative", old,
    r"[E: 128 channels at a 12.67 µs dwell (10 µs of chirp) give $1.01\times10^{6}$ samples per frame, a 0.054° mesh ($\sqrt{0.914\ {\rm sr}/1.01\times10^{6}}=9.5\times10^{-4}$ rad, 19 cm at 200 m). With aperture diameter $D=2$ mm, waist $w_0=0.9$ mm and Rayleigh range $z_R=\pi w_0^2/\lambda=1.6$ m, the 1/e² radius at 200 m is $w=11$ cm, slightly overfilling such a cell, whose area-matched radius is $19\ {\rm cm}/\sqrt{\pi}=10.7$ cm.",
    "Mesh from the samples at the dwell of Eq. (107); the 2 mm aperture still gives an area-matched spot.")

# ---------------------------------------------------------------- §C10.3a item 6
old = span(r"a 10 µs dwell moves the beam about $1{,}200^\circ/{\rm s}\times10\ \mu{\rm s}=0.012^\circ$", r"depend on the chirp and processing.")
add(f"{D1}: §C10.3a item 6, smear", old,
    r"a 12.67 µs dwell (10 µs of chirp plus $2\tau=2.67$ µs at 200 m, §C7b, Eq. (107)) moves the beam about $1{,}200^\circ/{\rm s}\times12.67\ \mu{\rm s}=0.015^\circ$: roughly four 1/e² beam radii of the 250 m confocal spot ($0.015^\circ/0.0036^\circ=4.2$), or 2.1 full 1/e² widths ($0.015^\circ/0.0072^\circ$). The swept geometric footprint is larger, but coherent integration and speckle decorrelation depend on the chirp and processing, and only the 10 µs of chirp is integrated.",
    "Smear over the whole dwell; integration over the chirp only.")

# ---------------------------------------------------------------- §C10.3a item 8, §C10.4, §C10.7
add(f"{D1}: §C10.3a item 8 (quotes item 5)",
    r"≈1–5% for item 5's channel budgets",
    r"≈0.8–2.3% for item 5's channel budgets",
    "From the item 5 table at the dwell of Eq. (107).")

add(f"{D1}: §C10.4 item 3 (quotes §C10.2 item 7)",
    r"The 12 Mpts/s case of §C10.2 would need tens to about a hundred parallel channels.",
    r"The 12 Mpts/s case of §C10.2 would need 56–152 parallel channels at 2–10 µs of chirp (§C10.2, item 7).",
    "Channel count of §C10.2 item 7 at the dwell of Eq. (107).")

add(f"{D1}: §C10.7 requirement 5 (quotes §C10.2 item 7)",
    r"| 5 | Tens of parallel coherent channels |",
    r"| 5 | 56–152 parallel coherent channels for one sample per 0.05° cell at 12 Mpts/s (§C10.2, item 7) |",
    "Channel count of §C10.2 item 7 at the dwell of Eq. (107).")

# ---------------------------------------------------------------- checks and output
first = json.loads((EDITS / "R2E_C10.json").read_text(encoding="utf-8"))["edits"]
spans = sorted((text.index(e["old"]), text.index(e["old"]) + len(e["old"]), e["id"]) for e in edits + first)
for (a0, a1, ai), (b0, b1, bi) in zip(spans, spans[1:]):
    assert b0 >= a1, ("overlap", ai, bi)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"block": "R2E2_C10_dwell", "edits": edits, "skipped": []}, f, ensure_ascii=False, indent=1)
print(f"{len(edits)} edits, 0 skipped -> {OUT.name}")
