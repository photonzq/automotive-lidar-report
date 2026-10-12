"""Round 3: replace the fourteen duplicated display equations by references to the equation they restate.

Writes edits/round3/R3c_eq_dups.json. Each duplicate display becomes an inline formula with a reference to the
kept equation; references whose wording would turn wrong under the renumbering redirect ("below", the section
named) are rewritten here, and the plain "Eq. (N)" references are left to renumber_equations.py --redirect:
  162, 170, 184 -> 11 (stopping distance; Eq. (11) also takes the report-wide t_{\\rm r})
  97 -> 93, 101 -> 33, 102 -> 34, 103 -> 35, 146 -> 33, 140 -> 33, 135 -> 38, 177 -> 153, 178 -> 150,
  186 -> 85, 185 -> 56.
The report is only read. Usage: python round3_build_eqdups.py
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
OUT = HERE / "edits" / "round3" / "R3c_eq_dups.json"
T = REPORT.read_text(encoding="utf-8")
edits = []
FIND = "consistency flags (duplicated display equations; Round 3 merge)"


def add(eid, old, new, why, finding=FIND):
    assert T.count(old) == 1, (eid, T.count(old), old[:80])
    edits.append({"id": f"R3c_eq_dups-{eid}", "finding": finding, "old": old, "new": new, "why": why})


# --- stopping distance: Eq. (11) is kept; t_r -> t_{\rm r} as everywhere else in the report
add("11a", "$$d_{\\rm stop}=v\\,t_r+\\frac{v^2}{2a_{\\rm b}} \\tag{11}$$",
    "$$d_{\\rm stop}=v\\,t_{\\rm r}+\\frac{v^2}{2a_{\\rm b}} \\tag{11}$$", "Report-wide symbol t_{\\rm r}.")
add("11b", "$v$ the speed in m/s, $t_r=1.5$ s the perception–reaction time",
    "$v$ the speed in m/s, $t_{\\rm r}=1.5$ s the perception–reaction time", "Report-wide symbol t_{\\rm r}.")
add("11c", "$v\\,t_r+v^2/(2a_{\\rm b})=d_{\\rm reach}$", "$v\\,t_{\\rm r}+v^2/(2a_{\\rm b})=d_{\\rm reach}$",
    "Report-wide symbol t_{\\rm r}.")
add("11d", "$v=a_{\\rm b}\\left[\\sqrt{t_r^2+2d_{\\rm reach}/a_{\\rm b}}-t_r\\right]$, with $t_r=1.5$ s",
    "$v=a_{\\rm b}\\left[\\sqrt{t_{\\rm r}^2+2d_{\\rm reach}/a_{\\rm b}}-t_{\\rm r}\\right]$, with $t_{\\rm r}=1.5$ s",
    "Report-wide symbol t_{\\rm r}.")
add("162", "stops within\n\n  $$d=v\\,t_{\\rm r}+\\frac{v^2}{2a_{\\rm b}} \\tag{162}$$\n\n  The first term",
    "stops within $d=v\\,t_{\\rm r}+v^2/(2a_{\\rm b})$, the stopping distance of Eq. (11) (§A6.1). The first term",
    "Eq. (162) restates Eq. (11).")
add("170", ", as in Eq. (162) of §E6 (written there with $d$ for $d_{\\rm stop}$):\n\n"
           "  $$d_{\\rm stop}=v\\,t_{\\rm r}+\\frac{v^2}{2a_{\\rm b}} \\tag{170}$$\n\n"
           "  where $v$ is the initial speed (m/s), $t_{\\rm r}$ the reaction time (s) and $a_{\\rm b}$ the constant "
           "braking deceleration (m/s²). Eq. (170) gives",
    ", $d_{\\rm stop}=v\\,t_{\\rm r}+v^2/(2a_{\\rm b})$ (Eq. (11), §A6.1), where $v$ is the initial speed (m/s), "
    "$t_{\\rm r}$ the reaction time (s) and $a_{\\rm b}$ the constant braking deceleration (m/s²). It gives",
    "Eq. (170) restates Eq. (11).")
add("184", "The stopping range is reproduced by the standard reaction-plus-braking distance\n\n"
           "$$d=v\\,t_{\\rm r}+\\frac{v^2}{2a_{\\rm b}} \\tag{184}$$\n\nwhere $d$ is the stopping distance (m),",
    "The stopping range is reproduced by the standard reaction-plus-braking distance "
    "$d=v\\,t_{\\rm r}+v^2/(2a_{\\rm b})$ of Eq. (11) (§A6.1), where $d$ is the stopping distance (m),",
    "Eq. (184) restates Eq. (11).")
# --- §F6 coherence length and beat frequency
add("185", "allows about 160 kHz at 300 m but marks the edge of detectability, not a design point:\n\n"
           "  $$L_c=\\frac{c}{\\pi\\,\\Delta\\nu}\\;\\ge\\;2R \\quad\\Longrightarrow\\quad \\Delta\\nu\\lesssim\\frac{c}{2\\pi R} \\tag{185}$$\n\n"
           "  Here $L_c$ is the coherence length (m), $c$ the speed of light, $\\Delta\\nu$ the laser linewidth (full "
           "width at half maximum, Hz), assuming a Lorentzian line shape, and $R$ the range, so $2R=600$ m at 300 m. "
           "Eq. (185) gives $\\Delta\\nu\\lesssim3\\times10^{8}/(\\pi\\times600)\\approx1.6\\times10^{5}$ Hz (§C0 subsection 2).",
    "allows about 160 kHz at 300 m but marks the edge of detectability, not a design point. With the coherence "
    "length $L_c=c/(\\pi\\Delta\\nu)$ of Eq. (56) (§C3a), the rule $L_c\\ge2R$ gives $\\Delta\\nu\\lesssim c/(2\\pi R)$, "
    "where $c$ is the speed of light, $\\Delta\\nu$ the laser linewidth (full width at half maximum, Hz), assuming a "
    "Lorentzian line shape, and $R$ the range; at 300 m, $2R=600$ m and "
    "$\\Delta\\nu\\lesssim3\\times10^{8}/(\\pi\\times600)\\approx1.6\\times10^{5}$ Hz (§C0 subsection 2).",
    "Eq. (185) is the coherence length of Eq. (56) with the condition L_c >= 2R.")
add("185r", "$L_c=c/(\\pi\\Delta\\nu)\\ge2R$ (§C7; §F6, Eq. (185))",
    "$L_c=c/(\\pi\\Delta\\nu)\\ge2R$ (§C7; Eq. (56) of §C3a, and §F6)",
    "The redirect would name §F6 for an equation now in §C3a.")
add("186", "using the beat-frequency relation of §C0 subsection 2:\n\n  $$f_b=\\frac{2BR}{cT} \\tag{186}$$\n\n"
           "  where $f_b$ is the beat frequency",
    "using the beat-frequency relation $f_b=2BR/(cT)$ of Eq. (85) (§C7; §C0 subsection 2), where $f_b$ is the beat "
    "frequency", "Eq. (186) restates Eq. (85).")
add("186b", "For a 1 GHz sweep in 10 µs, Eq. (186) gives 200 MHz at 300 m.",
    "For a 1 GHz sweep in 10 µs, it gives 200 MHz at 300 m.", "Follows the merged display.")
# --- §C7b: the energy per point and the coherent collection area
add("97", "- The optical energy that must be sent out per point is therefore\n"
          "$$E_{\\rm pt}=\\frac{n_{\\rm req}\\,E_{\\rm ph}\\,\\pi R^2}{\\rho\\,A_{\\rm eff}\\,\\eta},\\qquad "
          "E_{\\rm ph}=\\frac{hc}{\\lambda}, \\tag{97}$$\n"
          "where $E_{\\rm ph}$ is the energy of one photon, $h$ Planck's constant, $c$ the speed of light and $\\lambda$ "
          "the wavelength. One joule of light therefore buys $1/E_{\\rm pt}$ points. Eq. (97) is Eq. (93) of §C7a.",
    "- The optical energy that must be sent out per point is therefore Eq. (93) of §C7a, "
    "$E_{\\rm pt}=n_{\\rm req}E_{\\rm ph}\\pi R^2/(\\rho A_{\\rm eff}\\eta)$, where $E_{\\rm ph}=hc/\\lambda$ is the energy "
    "of one photon, $h$ Planck's constant, $c$ the speed of light and $\\lambda$ the wavelength. One joule of light "
    "therefore buys $1/E_{\\rm pt}$ points.",
    "Eq. (97) restates Eq. (93).")
add("101", "The §C10.3b model (Eq. (146)), with truncation factor $t$ and one polarization, gives\n"
           "$$A_{\\rm mode}=\\frac{t^2\\,\\lambda^2R^2}{2\\pi w^2}. \\tag{101}$$\n",
    "The mode-equivalent area of Eq. (33) (§C0 subsection 10.2; §C10.3b evaluates it), with truncation factor $t$ "
    "and one polarization, is $A_{\\rm mode}=t^2\\lambda^2R^2/(2\\pi w^2)$.\n",
    "Eq. (101) restates Eq. (33).")
add("102r", "spreads, by Eq. (102) below, to $w(200\\ {\\rm m})=14.2$ mm.",
    "spreads, by Eq. (34) (§C0 subsection 10.2), to $w(200\\ {\\rm m})=14.2$ mm.",
    "The redirect would keep 'below' for an equation that now precedes.")
add("102", "    - A collimated Gaussian beam of starting radius $w_0$ spreads with range as\n"
           "$$w^2=w_0^2+\\left(\\frac{\\lambda R}{\\pi w_0}\\right)^2 . \\tag{102}$$\n",
    "    - A collimated Gaussian beam of starting radius $w_0$ spreads with range as "
    "$w^2=w_0^2+(\\lambda R/\\pi w_0)^2$, Eq. (34) written out with the Rayleigh range $z_R=\\pi w_0^2/\\lambda$.\n",
    "Eq. (102) restates Eq. (34).")
add("103", "    - Inserting that minimum into Eq. (101) gives the ceiling\n"
           "$$A_{\\rm mode}\\le\\frac{t^2\\lambda R}{4}=65\\ {\\rm mm^2}\\ \\text{at 200 m}. \\tag{103}$$\n",
    "    - Inserting that minimum into Eq. (33) gives the ceiling $A_{\\rm mode}\\le t^2\\lambda R/4=65$ mm² at 200 m, "
    "the collecting-area form of the best-aperture envelope of Eq. (35).\n",
    "Eq. (103) restates Eq. (35) as an area.")
add("101r", "§C7b (Eq. (101)) and §C10.3b (Eq. (146)) restate it, and the report's scripts use it throughout.",
    "§C7b (subsection 1(b)) and §C10.3b use it, and so do the report's scripts.",
    "The restatements are merged into Eq. (33).")
# --- §C10: Eqs. (135), (140), (146)
add("135", "and $\\bar n$ the mean number of detected signal photons,\n\n"
           "  $$P_{\\rm fa}=e^{-\\gamma_{\\rm th}},\\qquad P_d=e^{-\\gamma_{\\rm th}/(1+\\bar n)}\\quad\\Rightarrow\\quad "
           "\\bar n=\\frac{\\ln P_{\\rm fa}}{\\ln P_d}-1 \\tag{135}$$\n\n  so $\\bar n=13.8/0.105-1\\approx130$,",
    "and $\\bar n$ the mean number of detected signal photons, $P_{\\rm fa}=e^{-\\gamma_{\\rm th}}$ and "
    "$P_d=e^{-\\gamma_{\\rm th}/(1+\\bar n)}$, the single-speckle detection law of Eq. (38) (§C0 subsection 10.3) with "
    "$p=P_{\\rm fa}$. Hence $\\bar n=\\ln P_{\\rm fa}/\\ln P_d-1=13.8/0.105-1\\approx130$,",
    "Eq. (135) restates Eq. (38).")
add("140", "Piggott et al. give the speckle-averaged received power (their Eq. 15) as\n\n"
           "  $$\\langle P_{\\rm RX}\\rangle=\\frac{\\lambda^2\\eta\\rho P_{\\rm TX}}{2\\pi A_{\\rm beam}} \\tag{140}$$\n\n"
           "  where $\\langle\\cdot\\rangle$ denotes",
    "Piggott et al. give the speckle-averaged received power (their Eq. 15) as "
    "$\\langle P_{\\rm RX}\\rangle=\\lambda^2\\eta\\rho P_{\\rm TX}/(2\\pi A_{\\rm beam})$, the link loss of Eq. (33) "
    "(§C0 subsection 10.2) with $A_{\\rm beam}=\\pi w(R)^2$ and no truncation ($t=1$), where $\\langle\\cdot\\rangle$ "
    "denotes", "Eq. (140) restates Eq. (33).")
add("146", "In this model it is\n\n$$A_{\\rm mode}(R)=\\frac{t^2\\,\\lambda^2R^2}{2\\pi\\,w(R)^2} \\tag{146}$$\n\nwhere $t$",
    "In this model it is Eq. (33) of §C0 subsection 10.2, $A_{\\rm mode}(R)=t^2\\lambda^2R^2/[2\\pi\\,w(R)^2]$, where $t$",
    "Eq. (146) restates Eq. (33).")
add("146b", " Eq. (146) restates §C0 Eq. (33).", "", "Said in the merged sentence.")
add("146r1", "Then Eq. (146) of §C10.3b (§C0 Eq. (33) restated) gives", "Then Eq. (33) of §C0 gives",
    "The redirect would name §C10.3b.")
add("146r2", "written below as a mode-equivalent collecting area $A_{\\rm mode}$, Eq. (146).",
    "written as a mode-equivalent collecting area $A_{\\rm mode}$ (Eq. (33) of §C0, quoted below).",
    "The redirect would keep 'below' for Eq. (33).")
# --- §E12.3: the mono and stereo range errors
add("177", "then shifts the inferred range by\n\n$$\\delta R\\approx\\frac{R^{2}\\,\\delta\\alpha}{h_{\\rm cam}} \\tag{177}$$\n\n"
           "with $h_{\\rm cam}=2.75$ m",
    "then shifts the inferred range by $\\delta R\\approx R^{2}\\,\\delta\\alpha/h_{\\rm cam}$ (Eq. (153) of §E2, with "
    "$R$ for $Z$ and $h_{\\rm cam}$ for $h$). Here $h_{\\rm cam}=2.75$ m",
    "Eq. (177) restates Eq. (153).")
add("177b", " Eq. (177) is Eq. (153) of §E2 with $R$ for $Z$ and $h_{\\rm cam}$ for $h$.", "",
    "Said in the merged sentence.")
add("178", "gives\n\n$$\\delta R=\\frac{R^{2}\\,\\sigma_d\\,{\\rm IFOV}_{\\rm st}}{b_{\\rm st}} \\tag{178}$$\n\n"
           "with ${\\rm IFOV}_{\\rm st}=0.1$ mrad",
    "gives $\\delta R=R^{2}\\,\\sigma_d\\,{\\rm IFOV}_{\\rm st}/b_{\\rm st}$, Eq. (150) of §E2 with $R$ for $Z$, "
    "$\\delta R$ for $\\sigma_Z$, $f=1/{\\rm IFOV}_{\\rm st}$ pixels per radian and $b=b_{\\rm st}$. Here "
    "${\\rm IFOV}_{\\rm st}=0.1$ mrad",
    "Eq. (178) restates Eq. (150).")
add("178b", " Eq. (178) is Eq. (150) of §E2 with $R$ for $Z$, $\\delta R$ for $\\sigma_Z$, $f=1/{\\rm IFOV}_{\\rm st}$ "
            "pixels per radian and $b=b_{\\rm st}$; §E2's wide-baseline case",
    " §E2's wide-baseline case", "Said in the merged sentence.")
add("178r", "Both Eq. (177) and Eq. (178) grow as $R^2$", "Both errors grow as $R^2$",
    "The two equations are now §E2's.")
add("178r2", "(Eq. (178) below)", "(Eq. (150), §E2)", "The redirect would keep 'below' for an equation in §E2.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"block": "R3c_eq_dups", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(len(edits), "edits written to", OUT.name)
