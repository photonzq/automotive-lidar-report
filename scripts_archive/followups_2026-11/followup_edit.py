"""Clear air in §C0 (wording, citations, the 940 nm caveat) and Figure C3a's caption beside the figure.

1. §C0 subsection 5.4 said that its margin and range equations neglect clear-air extinction, "which changes the
   margins by at most 0.15 dB here", yet the ranges it quotes include that extinction (link_budget_scaling.py solves
   them numerically). The text now gives the clear-air term, says which numbers include it, and shows how strongly it
   matters near a coherent design's cliff.
2. §C0 subsection 3.3's clear-air coefficients now cite Kim, McArthur and Korevaar (2001) at equation and table
   precision (Eq. 10; 23 km is the "clear" row of their Table 4), carry their substitutions, and state that the model
   covers scattering only, so at 940 nm, inside a water-vapour band, the loss is a lower bound. Appendix 1 gets an
   item on that absorption; §C0's source list names the equation and table.
3. Figure C3a: image and caption side by side in a fenced div `capside` (image 60 % wide, caption block `capbody`
   beside it, kept on one page), replacing the class `tall`; the style block gains the rules.

Usage: followup_edit.py <report.md> <expected sha256 prefix> [--write]
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

EDITS = [
    # ---- §C0 subsection 3.3: fog bullet, equation reference
    (r"therefore attenuates 905 and 1,550 nm about equally [I, Kim, McArthur and Korevaar 2001], consistent with",
     r"therefore attenuates 905 and 1,550 nm about equally [I, Kim, McArthur and Korevaar 2001, Eq. 10], consistent "
     r"with"),
    # ---- §C0 subsection 3.3: clear-air bullet
    (r"- **Clear air.** With the clear-air exponent $q_{\rm K}=1.3$ (visibility 23 km), the Kim model gives "
     r"$\alpha=0.085$ /km at 940 nm and 0.044 /km at 1,550 nm, so the two-way transmission $T_{\rm atm}^2$ costs only "
     r"0.15 and 0.08 dB at 200 m.",
     r"- **Clear air.** Kim, McArthur and Korevaar's model, $\alpha=(3.91/V)(\lambda/550\ {\rm nm})^{-q_{\rm K}}$ with "
     r"$q_{\rm K}=1.3$ for visibilities of 6–50 km [I, Kim et al. 2001, Eq. 10], gives at the 23 km visibility that "
     r"their Table 4 classes as clear $\alpha=(3.912/23\ {\rm km})\times(940/550)^{-1.3}=0.170\times0.498=0.085$ /km "
     r"at 940 nm and $0.170\times(1{,}550/550)^{-1.3}=0.044$ /km at 1,550 nm (their Table 4 lists 0.2 dB/km at "
     r"1,550 nm for this visibility; $4.343\times0.044=0.19$ dB/km). The two-way transmission $T_{\rm atm}^2$ then "
     r"costs $8.686\times0.085\times0.2=0.15$ dB at 200 m at 940 nm and $8.686\times0.044\times0.2=0.08$ dB at "
     r"1,550 nm [E]. The model covers scattering only: Kim et al. leave absorption out because free-space links use "
     r"wavelengths inside atmospheric transmission windows (their section 3). 940 nm lies in a water-vapour "
     r"absorption band (§C4c), so there the 0.15 dB is a lower bound; how much the water vapour adds depends on the "
     r"laser's line and on the humidity and is not computed here (Appendix 1)."),
    # ---- §C0 source list: equation and table
    (r"https://doi.org/10.1117/12.417512 (Kim, McArthur and Korevaar 2001, fog model and visibility classes)",
     r"https://doi.org/10.1117/12.417512 (Kim, McArthur and Korevaar 2001: fog model, Eq. 10; visibility classes, "
     r"Table 4)"),
    # ---- §C0 subsection 5.4: the clear-air term
    (r"Both neglect clear-air extinction, which changes the margins by at most 0.15 dB here.",
     r"Both leave out clear-air extinction. At a shorter range $R$ the light crosses less air than at $R_0$, so a "
     r"design sized to reach $R_0$ through clear air has a margin larger by $8.686\,\alpha\,(R_0-R)$ dB, where "
     r"$\alpha$ is the clear-air extinction coefficient of subsection 3.3 (0.085 /km at 940 nm and 0.044 /km at "
     r"1,550 nm) and $8.686=20/\ln10$ counts both passes. That is at most $8.686\times0.085\times0.2=0.15$ dB here. "
     r"The margins, ranges and tables below include this term; `build/figures/link_budget_scaling.py` finds each "
     r"range numerically."),
    (r"A target is still detected wherever $\mathcal{M}(R)\ge X$. Solving Eq. \eqref{eq:link-margin} for the range "
     r"gives the maximum range with the extra loss:",
     r"A target is still detected wherever $\mathcal{M}(R)\ge X$. Without the clear-air term, solving Eq. "
     r"\eqref{eq:link-margin} for the range gives the maximum range with the extra loss in closed form:"),
    (r"The 25 mm design reaches 61 m behind the film and nothing beyond 2.1 dB.",
     r"The 25 mm design reaches 61 m behind the film and nothing beyond 2.1 dB. These ranges include the clear-air "
     r"term, and near the cliff they depend on it strongly, because the margin there changes slowly with range. The "
     r"term lifts the best-aperture design's plateau from 3.01 to $3.01+8.686\times0.044\times0.2=3.09$ dB, which "
     r"moves its range at $X=3$ dB from the 9.7 m of Eq. \eqref{eq:range-with-extra-loss} to 27 m; without the term "
     r"the same equation gives 109 m and 52 m behind the film for the two designs."),
    # ---- Appendix 1: water-vapour absorption at 940 nm, after the glare item
    ("were not measured in any source found.\n\n**Night vision beyond thermal (§A7)**\n",
     "were not measured in any source found.\n"
     "- **Water-vapour absorption at 940 nm (§C0 subsection 3.3).** The clear-air and fog losses of §C0 come from Kim "
     "et al.'s scattering model, which leaves out molecular absorption. At 940 nm, inside a water-vapour band, the "
     "extra loss over a 200 m path depends on the laser's line, its drift with temperature and the humidity; it was "
     "not computed here. Line-by-line absorption data (for example HITRAN) would give it.\n"
     "\n**Night vision beyond thermal (§A7)**\n"),
    # ---- style block: the capside layout
    ("img, table, .eqn, h1, h2, h3, h4, div.pair, div.narrow { clear: both; }\n</style>",
     "div.capside { display: flex; align-items: flex-start; gap: 1.4em; margin: 0.6em 0; break-inside: avoid; }\n"
     "div.capside > p:first-child { flex: 0 0 60%; margin: 0; }\n"
     "div.capside > p:first-child img { width: 100%; margin: 0; }\n"
     "div.capside > div.capbody { flex: 1 1 0; min-width: 0; }\n"
     "div.capside div.capbody p { margin: 0 0 0.3em 0; }\n"
     "@media screen and (max-width: 700px) { div.capside { display: block; } }\n"
     "img, table, .eqn, h1, h2, h3, h4, div.pair, div.narrow, div.capside { clear: both; }\n</style>"),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)

# ---- Figure C3a: wrap the image and its whole caption block
IMG = ("![Listed lidar companies: share price relative to listing, and drawdown from prior peak]"
       "(automotive_perception_report_figures/lidar_equity_hype_cycle.png){.tall}\n")
END = "Their outcomes are in the tables above.\n"
assert new.count(IMG) == 1, "C3a image line"
start = new.index(IMG)
stop = new.index(END, start) + len(END)
block = new[start:stop]
lines = block.split("\n")[:-1]
assert lines[1] == "" and lines[2] == "*Figure C3a.*", lines[:3]
assert all(ln.startswith("- ") for ln in lines[3:]) and len(lines) == 8, len(lines)
wrapped = ("::::: capside\n" + IMG.replace("{.tall}", "") + "\n::: capbody\n" + "\n".join(lines[2:]) + "\n\n:::\n"
           ":::::\n")
new = new[:start] + wrapped + new[stop:]
assert new.count("{.tall}") == 0

assert "\r" not in new
print(f"{len(EDITS) + 1} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
