"""Round 5b: the author's decisions on the open readability items (2026-10-05), as one edit list for my sections and
one list of pairs for the lines of the parallel Part B pass.

Decisions: the author asked for the recommendations to be applied (after the list of 2026-10-05),
and answered the Part B pass's questions the same way: "(§X subsection N)" with no comma; "programme", keeping
"program" for software and quoted official names. Kept as they are (no edit): the 15 W parity target, the ≈3–7%
parity probability and the two-term §C9a interference model.
Two departures from the recommendations, for reasons stated in the edits: the §C10.3a mode count is renamed N_m, not M
(§C10.3a already uses M² and the APD gain M); the §C6(f) staring pixel is stated at f/2.4, the f-number that gives the
10⁷ s⁻¹ used (f/2 gives 1.4×10⁷).
Each changed line becomes one edit whose old text is the whole line, so no two edits overlap. Lines in Part B, §D8 and
Appendix 1 belong to the Part B pass: their pairs go to edits/round5/R5b_for_peer.json, which that pass applies.
Writes edits/round5/R5b_decisions.json and edits/round5/R5b_for_peer.json; the report is only read.
Usage: python round5_build_decisions.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
T = REPORT.read_text(encoding="utf-8")
L = T.split("\n")
NEW = list(L)
WHY = {}


def heading_index(prefix):
    hits = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]


def section(prefix):
    """Line range of the section whose heading starts with prefix, up to the next heading of the same or higher level."""
    a = heading_index(prefix)
    level = len(prefix) - len(prefix.lstrip("#"))
    b = next((j for j in range(a + 1, len(L)) if re.match(r"#{1,%d} " % level, L[j])), len(L))
    return range(a, b)


def owner(i):
    part = sec = None
    for j in range(i, -1, -1):
        if sec is None and L[j].startswith("## "):
            sec = L[j]
        if L[j].startswith("# "):
            part = L[j]
            break
    if part and (part.startswith("# Part B") or part.startswith("# Appendix 1")):
        return "peer"
    return "peer" if sec and sec.startswith("## D8.") else "mine"


def once(old, new, why):
    """Replace a substring that occurs exactly once in the report (and still once in its line)."""
    assert T.count(old) == 1, (why, T.count(old), old[:70])
    i = next(k for k, l in enumerate(L) if old in l)
    assert NEW[i].count(old) == 1, (why, old[:70])
    NEW[i] = NEW[i].replace(old, new)
    WHY.setdefault(i, []).append(why)


def in_lines(old, new, lines, why, expect):
    n = 0
    for i in lines:
        k = NEW[i].count(old)
        if k:
            NEW[i] = NEW[i].replace(old, new)
            WHY.setdefault(i, []).append(why)
            n += k
    assert n == expect, (why, n, expect)


C7, C7A, C7B = section("## C7. "), section("## C7a. "), section("## C7b. ")
C10_3A = section("### C10.3a")

# 1. Power envelopes: say which applies where
once("and the yellow band marks the 8–25 W typical of automotive lidars.",
     "and the yellow band marks the 8–25 W typical of shipping automotive lidars; the parity target of §C7b "
     "subsection 5 is ≤15 W.", "power envelope: Figure C7a band against the parity target")
once("sets how many channels fit in a 10–15 W sensor power envelope.",
     "sets how many channels fit in a sensor drawing 10–15 W, whose upper end is the ≤15 W of the parity target "
     "(§C7b subsection 5).", "power envelope: §F6 sizing range")

# 2. §C6(f): basis of the 10^7 avalanches/s of a staring VGA pixel
once(r"$3.1\times10^{5}\times10^{7}\ {\rm s^{-1}}\times1.6\ {\rm pJ}=4.9$ W, and 12 W at 3.9 pJ.",
     r"$3.1\times10^{5}\times10^{7}\ {\rm s^{-1}}\times1.6\ {\rm pJ}=4.9$ W, and 12 W at 3.9 pJ. The $10^{7}$ is the "
     r"recorded rate of a staring 10 µm single-SPAD pixel behind an f/2.4 lens in the fully sunlit scene of (d). A pixel "
     r"collects background in proportion to its étendue $\pi p^2/(4N^2)$, with $p$ the pixel pitch and $N$ the "
     r"f-number: $\pi\times(10\ \mu{\rm m})^2/(4\times2.4^2)=1.36\times10^{-11}$ m² sr, i.e. 0.036 of the "
     r"$7.62\times10^{-7}\ {\rm sr}\times4.91\times10^{-4}\ {\rm m^2}=3.74\times10^{-10}$ m² sr of the macro-pixel in (d). "
     r"That gives $2.965\times10^{8}\times0.036=1.08\times10^{7}$ s⁻¹ incident (940 nm, 10 nm filter, reflectance 0.9, "
     r"PDE 0.3) and, with 6 ns of paralyzable dead time, $1.08\times10^{7}\times e^{-0.065}=1.0\times10^{7}$ s⁻¹ "
     r"recorded. At f/2 the recorded rate is $1.4\times10^{7}$ s⁻¹; an f/1.2 lens, with four times the étendue of "
     r"f/2.4, gives $3.3\times10^{7}$ s⁻¹ and about 3.3 times the power [E].", "§C6(f) VGA pixel basis (f/2.4)")

# 3. FS-4S deployability tag in the §C7a subsection 1 table
once("| No production award found (§C7 Commercial status) |", "| [R]: no production award found (§C7 Commercial status) |",
     "FS-4S deployability tag [R]")

# 4. §C8.1 switched FPA: one field and pitch for the 0.05° case
once("At §C7's specification (0.05° over 120°×26°, 55 µm pitch) ≈132×29 mm.",
     "At 0.05° over the same 120°×25° and 53 µm ≈127×26.5 mm (2,400×500 addresses, as in §C10.4); §C7's 2,400×520 "
     "grid at Berkeley's 55 µm pitch gives ≈132×29 mm.", "§C8.1 FPA: 120°×25° at 53 µm, as §C10.4")

# 5. §C10.7 signposts
once("- LC metasurfaces switching in ≤25 µs at −40 °C;",
     "- LC metasurfaces switching in ≤21 µs per step at −40 °C, the 0.05°, 20 fps requirement of §C10.5;",
     "§C10.7 signpost: LC switching from §C10.5")
once("- a coherent FPA or column with ≥256 simultaneous channels on an ASIC (application-specific integrated circuit) "
     "within about 10 W;",
     "- a coherent FPA or column with ≥256 simultaneous receivers (64 channels of four looks, the milestone of §C7b "
     "subsection 7) on an ASIC (application-specific integrated circuit) within about 10 W;",
     "§C10.7 signpost: receiver count as §C7b subsection 7")

# 6. Falcon naming: K1 for the first-generation Falcon
once("Falcon K/K2/K3 (1550)", "Falcon K1/K2/K3 (1550)", "Falcon K1 naming")
once("Seyond's 1,550 nm Falcon K (§C3, §C3b)", "Seyond's 1,550 nm Falcon K1 (§C3, §C3b)", "Falcon K1 naming")
once("**Seyond Falcon K / K2** (1,550 nm ToF) | 500 m max; 250 m (K) / 300 m (K2) at 10%",
     "**Seyond Falcon K1 / K2** (1,550 nm ToF) | 500 m max; 250 m (K1) / 300 m (K2) at 10%", "Falcon K1 naming")
once("- **Seyond Falcon K / K2:**", "- **Seyond Falcon K1 / K2:**", "Falcon K1 naming")

# 7. §E11.3: the 128-line point rate
once("A 2–3 Mpts/s 128-line unit produces about 0.2–0.4 Gbit/s. Compact polar sensor packets (≈4–6 bytes per return) "
     "give about 0.8–1.9 and 0.06–0.14 Gbit/s respectively [E].",
     "A 128-line unit such as the Hesai AT128, at 1.54 Mpts/s with single returns (§C3b) and twice that with dual "
     "returns, produces about 0.15–0.39 Gbit/s. Compact polar sensor packets (≈4–6 bytes per return) give about 0.8–1.9 "
     "and 0.05–0.15 Gbit/s respectively [E].", "§E11.3 128-line rate: AT128 single to dual return")
once(r"$2\times10^{6}\times12\times8\approx0.19$ Gbit/s, and $3\times10^{6}\times6\times8\approx0.14$ Gbit/s.",
     r"$1.54\times10^{6}\times12\times8\approx0.15$ Gbit/s, $3.07\times10^{6}\times16\times8\approx0.39$ Gbit/s, and "
     r"$3.07\times10^{6}\times6\times8\approx0.15$ Gbit/s.", "§E11.3 128-line rate: AT128 single to dual return")

# 8. §C0 10.6: the water film at its exact 1.88 dB (link_budget_scaling.py rerun: 111 m and 61 m)
once("The best-aperture design reaches 110 m behind a 0.2 mm water film ($X=1.9$ dB)",
     "The best-aperture design reaches 111 m behind a 0.2 mm water film ($X=1.88$ dB)", "water film 1.88 dB")
once("The 25 mm design reaches 58 m behind the film", "The 25 mm design reaches 61 m behind the film", "water film 1.88 dB")

# 9. §E11.1: how far Huang et al.'s theorem reaches
once("it too merges learned features, so it is mid fusion in §E10.1's terms.",
     "it too merges learned features, so it is mid fusion in §E10.1's terms. Huang et al.'s theorem is proved for their "
     "late-fusion networks, in which the merged features feed the output directly; it carries over to BEV fusion, which "
     "processes the merged features further, only by analogy, and §E11.1 checks the effect empirically for camera–lidar "
     "detectors.", "§E11.1 Huang et al. and BEV fusion: by analogy")

# 10. §C0 10.8: the efficiency caveat as a pointer to 10.1
once("- **Efficiency.** It is the weakest input. The 0.25 of 10.4 lies above both measured chains, 0.112 for Waymo's "
     "fibre-optic bench and 0.057 effective for Pointcloud's integrated array, as 10.1 notes.",
     "- **Efficiency.** It is the weakest input: the 0.25 of 10.4 lies above both measured chains (10.1).",
     "§C0 10.8 efficiency caveat as pointer")

# 11. Chirp duration T_c (§C7, §C0 subsection 2, §F6) and useful window T_u (§C7a)
once("swept in a time $T$ returns from a target", "swept in a time $T_c$ returns from a target", "T_c in §C7")
once(r"$$f_b=\frac{2BR}{cT} \tag{85}$$", r"$$f_b=\frac{2BR}{cT_c} \tag{85}$$", "T_c in §C7")
once("$T=10$ µs and $R=300$ m, Eq. (85) gives", "$T_c=10$ µs and $R=300$ m, Eq. (85) gives", "T_c in §C7")
once("Let $T_c$ be the chirp duration, the same quantity as $T$ in Eq. (85), over which",
     "Let $T_c$ be the chirp duration of Eq. (85), over which", "T_c in §C7")
once(r"where $\kappa=B/T$ is the chirp rate in Hz/s", r"where $\kappa=B/T_c$ is the chirp rate in Hz/s", "T_c in §C7")
once(r"With chirp rate $\kappa=B/T=10^{9}/10^{-5}=10^{14}$ Hz/s", r"With chirp rate $\kappa=B/T_c=10^{9}/10^{-5}=10^{14}$ Hz/s",
     "T_c in §C7")
once(r"$f_b\propto1/T$ by Eq. (85)", r"$f_b\propto1/T_c$ by Eq. (85)", "T_c in §C7")
once(r"$B=1$ GHz and $T=10$ µs, so that $\kappa=B/T=10^{14}$ Hz/s. These are illustrative values, as in §C7 Eq. (85);",
     r"$B=1$ GHz and $T_c=10$ µs, so that $\kappa=B/T_c=10^{14}$ Hz/s. These are illustrative values, as in §C7 Eq. (85);",
     "T_c in §C0 subsection 2")
once("using the beat-frequency relation $f_b=2BR/(cT)$ of Eq. (85)", "using the beat-frequency relation $f_b=2BR/(cT_c)$ of Eq. (85)",
     "T_c in §F6")
once("$T$ the chirp duration (s)", "$T_c$ the chirp duration (s)", "T_c in §F6")
once("The beat frequency is $f_b=2BR/(cT)$ (Eq. (85)), with $R$ the range, $T$ the useful window of one chirp ramp and $B$ "
     "the bandwidth swept in it.",
     "The beat frequency is $f_b=2BR/(cT_u)$, Eq. (85) with the useful window $T_u$ of one chirp ramp in place of the "
     "chirp duration, where $R$ is the range and $B$ the bandwidth swept in the useful window.", "T_u in §C7a")
once(r"the ramp itself lasts $T+\tau$", r"the ramp itself lasts $T_u+\tau$", "T_u in §C7a")
once(r"$T_{\rm int}=2T$ in all", r"$T_{\rm int}=2T_u$ in all", "T_u in §C7a")
once(r"$N_{\rm samp}=f_s\times2T$, which gives", r"$N_{\rm samp}=f_s\times2T_u$, which gives", "T_u in §C7a")
once(r"5\,f_D\,T \tag{94}", r"5\,f_D\,T_u \tag{94}", "T_u in §C7a")
once(r"$f_bT=2BR_{\max}/c=R_{\max}/\Delta R$ at maximum range. Eq. (94) is Eq. (105) of §C7b with $R=R_{\max}$ and $T_u=T$.",
     r"$f_bT_u=2BR_{\max}/c=R_{\max}/\Delta R$ at maximum range. Eq. (94) is Eq. (105) of §C7b with $R=R_{\max}$.",
     "T_u in §C7a")
once(r"$N_{\rm samp}=f_s\times2T=1.23", r"$N_{\rm samp}=f_s\times2T_u=1.23", "T_u in §C7a")
once(r"because $f_bT=R_{\max}/\Delta R$:", r"because $f_bT_u=R_{\max}/\Delta R$:", "T_u in §C7a")
once(r"$T_{\rm dwell}=2T+2\tau=10+2.67=12.67$ µs", r"$T_{\rm dwell}=2T_u+2\tau=10+2.67=12.67$ µs", "T_u in §C7a")
once(r"With chirp rate $\kappa=B/T$ (Hz/s), the beat frequency", r"With chirp rate $\kappa=B/T_u$ (Hz/s), the beat frequency",
     "T_u in §C7a")

# 12. ADC samples per point N_ADC (§C0 10.3, §C7a, §C7b); N_samp stays the samples per frame of §C10
assert T.count(r"N_{\rm ADC}") == 0
C0_LINE = [next(i for i, l in enumerate(L) if "so its Eq. (94) counts $N_{\\rm samp}=5N_b" in l)]
in_lines(r"N_{\rm samp}", r"N_{\rm ADC}", C0_LINE + list(C7A) + list(C7B), "N_ADC for ADC samples per point", 16)

# 13. §C10 detection notation as in §C0 subsection 10.3 (P_D, per-bin p, x_th, n_req)
once(r"For a detection probability $P_d=0.9$ at a false-alarm probability $P_{\rm fa}=10^{-6}$,",
     r"For a detection probability $P_D=0.9$ at a per-bin false-alarm probability $p=10^{-6}$,", "§C10 detection notation")
once(r"With the detection threshold $\gamma_{\rm th}$ expressed in units of the mean noise power, and $\bar n$ the mean number "
     r"of detected signal photons, $P_{\rm fa}=e^{-\gamma_{\rm th}}$ and $P_d=e^{-\gamma_{\rm th}/(1+\bar n)}$, the "
     r"single-speckle detection law of Eq. (38) (§C0 subsection 10.3) with $p=P_{\rm fa}$. Hence "
     r"$\bar n=\ln P_{\rm fa}/\ln P_d-1=13.8/0.105-1\approx130$,",
     r"With the detection threshold $x_{\rm th}$ expressed in units of the mean noise power, and $\bar n$ the mean number "
     r"of detected signal photons, $p=e^{-x_{\rm th}}$ and $P_D=e^{-x_{\rm th}/(1+\bar n)}$, the single-speckle detection "
     r"law of Eq. (38) (§C0 subsection 10.3). Hence $\bar n=\ln p/\ln P_D-1=13.8/0.105-1\approx130$,",
     "§C10 detection notation")
once(r"$b=\sqrt{2\gamma_{\rm th}}$ and $\gamma_{\rm th}=\ln10^{6}=13.8$", r"$b=\sqrt{2x_{\rm th}}$ and $x_{\rm th}=\ln10^{6}=13.8$",
     "§C10 detection notation")
once(r"≈21 detected photons for $P_d=0.9$ at $P_{\rm fa}=10^{-6}$ in one bin", r"≈21 detected photons for $P_D=0.9$ at $p=10^{-6}$ in one bin",
     "§C10 detection notation")
once(r"a detection probability $P_d=0.9$ and a false-alarm rate of $10^{-6}$ per bin",
     r"a detection probability $P_D=0.9$ and a false-alarm probability $p=10^{-6}$ per bin", "§C10 detection notation")
once(r"$N_{\rm req}$ is the number of detected photons (photoelectrons) required per sample, the $n_{\rm req}$ of §C0 subsection 10.1.",
     r"$N_{\rm req}$ is the number of detected photons (photoelectrons) required per sample, as in §C0 subsection 10.1.",
     "§C10 detection notation")
in_lines(r"N_{\rm req}", r"n_{\rm req}", range(len(L)), "§C10 detection notation: n_req", 17)

# 14. §C10.3a: the number of spatial modes received per sample
in_lines(r"N_{\rm mode}", r"N_{\rm m}", C10_3A, "§C10.3a mode count N_m (N_mode is §C0's photons in the LO mode)", 6)

# 15. §C4d Eq. (70): the per-channel pulse rate as in §C0 subsection 1
once(r"$$f_p\le\frac{c}{2R_{\max}} \tag{70}$$", r"$$\text{PRF}_{\rm ch}\le\frac{c}{2R_{\max}} \tag{70}$$", "PRF_ch in §C4d")
once("where $f_p$ is the channel's pulse repetition frequency (PRF),",
     r"where $\text{PRF}_{\rm ch}$ is the channel's pulse repetition frequency,", "PRF_ch in §C4d")

# 16. Moore Photonics is LightIC (摩尔芯光; www.lightic.tech title, read 2026-10-05), listed above it in §C7
MOORE = "  - **Moore Photonics** has published claims but no product data."
assert L.count(MOORE) == 1
moore_i = L.index(MOORE)

# 17. "programme", keeping "program" in URLs, link targets, quotations and official names
URL = re.compile(r"https?://\S+")
LINK = re.compile(r"\]\([^)]*\)")  # applied after URL, which may itself hold parentheses, e.g. "AEye+(LIDR)+…"
KEEP = {"Navy Strategic Systems Programs"}
for i, l in enumerate(L):
    if i == moore_i:
        continue
    masked = URL.sub(lambda m: "\0" * len(m.group(0)), NEW[i])
    masked = LINK.sub(lambda m: "\0" * len(m.group(0)), masked)
    for name in KEEP:
        masked = masked.replace(name, "\0" * len(name))
    out, last, n = [], 0, 0
    for m in re.finditer(r"\b(P|p)rogram(s?)\b", masked):
        s = m.start()
        before = masked[:s]
        if before.count('"') % 2 == 1:
            continue  # inside a quotation
        if m.group(1) == "P" and not NEW[i].lstrip().startswith("|"):
            continue  # capitalized outside a table header: an official name
        out.append(NEW[i][last:s] + m.group(1) + "rogramme" + m.group(2))
        last, n = m.end(), n + 1
    if n:
        NEW[i] = "".join(out) + NEW[i][last:]
        WHY.setdefault(i, []).append("programme (not in URLs, quotations or official names)")

# 18. reference form "(§X subsection N)", no comma
for i in range(len(L)):
    s, n = re.subn(r"(§[A-Z][0-9A-Za-z.]*), (subsection )", r"\1 \2", NEW[i])
    if n:
        NEW[i] = s
        WHY.setdefault(i, []).append("reference form §X subsection N")

mine, peer = [], []
changed = [i for i in sorted(WHY) if NEW[i] != L[i]]
runs = []  # maximal runs of consecutive changed lines
for i in changed:
    if runs and runs[-1][1] == i - 1:
        runs[-1][1] = i
    else:
        runs.append([i, i])
spans = []
for a, b in runs:
    lo, hi = a, b
    # a line that is not unique (a repeated table header) takes unchanged neighbours along until the text is unique
    while T.count("\n".join(L[lo:hi + 1])) != 1:
        lo, hi = (lo - 1, hi) if (hi - lo) % 2 == 0 and lo > 0 else (lo, hi + 1)
    if spans and lo <= spans[-1][1] + 1:  # touches the previous edit: merge the two
        spans[-1][1] = max(spans[-1][1], hi)
    else:
        spans.append([lo, hi])
for lo, hi in spans:
    a = next(i for i in range(lo, hi + 1) if i in changed)
    b = max(i for i in range(lo, hi + 1) if i in changed)
    reasons = list(dict.fromkeys(r for i in range(a, b + 1) for r in WHY.get(i, [])))
    e = {"id": f"R5b-L{a + 1}" + (f"-{b + 1}" if b > a else ""), "finding": "; ".join(reasons),
         "old": "\n".join(L[lo:hi + 1]), "new": "\n".join(NEW[lo:hi + 1]),
         "why": "Author's decision of 2026-10-05 (see round5_build_decisions.py)."}
    owners = {owner(i) for i in range(a, b + 1)}
    assert len(owners) == 1, ("run crosses an ownership boundary", a + 1, b + 1)
    (peer if owners == {"peer"} else mine).append(e)
    assert owners == {"mine"} or set(reasons) <= {"programme (not in URLs, quotations or official names)",
                                                  "reference form §X subsection N"}, (a + 1, reasons)
assert owner(moore_i) == "mine"
mine.append({"id": f"R5b-L{moore_i + 1}", "finding": "Moore Photonics is LightIC (摩尔芯光), listed above it in §C7",
             "old": MOORE + "\n", "new": "",
             "why": "§D7 and LightIC's own site (www.lightic.tech, title 摩尔芯光) give one company; the LightIC bullet of "
                    "the same list describes its Lark lidar."})
for name, lst in (("R5b_decisions", mine), ("R5b_for_peer", peer)):
    out = HERE / "edits" / "round5" / f"{name}.json"
    assert not out.exists() or "--force" in sys.argv, f"{out.name} exists; pass --force"
    out.write_text(json.dumps({"block": name, "edits": lst, "skipped": []}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{name}: {len(lst)} line edits")
