"""Texts for the follow-ups the readability review flagged on 5 Oct 2026 (applied with edits_partB_definitive.py
--texts followups_texts --name followups). The author chose all of them on 5 Oct 2026.

  - Appendix 1: the Fastree3D purchase pointer moves from §C5 to §C3a subsection 2, where the history now lives.
  - §B8: the VL53L5 macro-pixel note gets the wording §C0 already uses (Rae and Mellot, ISSW 2018).
  - Appendix 1: an open item for the Wood et al. headlight figures that §A6 tags [U] (Round 4 research, R1).
  - §B1: each installation figure names its provider. ResearchInChina gives 1.529 M (2024, 6.0%) and 3.21 M
    (2025); Gasgoo (盖世汽车研究院, article of 21 May 2026, https://m.gasgoo.com/news/70458750.html) gives
    2.756 M main lidars in 2025 (Hesai 1.143 M) and more than 985k lidars in Q1 2026 with the supplier shares.
  - §B4a: the duplicated stopping-distance display Eq. (14) becomes a pointer to Eq. (11) (§A6.1); the
    equations after it are renumbered afterwards with ../readability_2026-10-03/renumber_equations.py.

Entries are (id, unique start of the report line, change); see partB_definitive_texts.py for the forms, plus
{"block": k, "text": ...}, which replaces the line and the k-1 lines after it.
"""

GASGOO = "https://m.gasgoo.com/news/70458750.html"
RIC_2024 = "https://www.eefocus.com/article/1819136.html"

EDITS = [
    ("appx1-fastree3d-pointer", "- **European funding and exits.**",
     ("sub", "with no earn-out, later payment or goodwill (§C5);",
      "with no earn-out, later payment or goodwill (§C3a subsection 2);")),
    ("b8-vl53l5-macropixel", "In the receiver row, a *macro-pixel* is",
     ("sub", "(the VL53L5's 14 × 10)",
      "(the VL53L5's 14 × 10 macro-pixels of 4 × 4 SPADs, of which an 8 × 8 block is read out as its zones "
      "[P, Rae and Mellot 2018])")),
    ("appx1-wood", "- **Yole's technology split**",
     ["- **Wood et al. headlight figures (§A6).** The 2005 *Human Factors* abstract confirms 5% recognition of "
      "black-clad pedestrians under low beams with glare and a mean recognition distance of 0.0 m for older "
      "drivers [I]. Unknown: whether the full texts of Wood, Tyrrell & Carberry (2003, 2005) contain the 40% "
      "recognition rate without glare, the 59 → 94 m gain from low to high beam and the 3.5× for dark clothing "
      "that §A6 cites [U]."]),
    ("b1-header", "**China installations** [T].",
     ("sub", "**China installations** [T].", "**China installations** [MR/T].")),
    ("b1-2024", "- In 2024 China installed 1.529 M lidars",
     ("sub", "a penetration of 6.0%.",
      f"a penetration of 6.0% [MR, [ResearchInChina]({RIC_2024})].")),
    ("b1-2025", "- In 2025 installations reached **3.21 M** units in total",
     ("sub", "- In 2025 installations reached **3.21 M** units in total, of which 2.756 M were main lidars.",
      "- In 2025 installations reached **3.21 M** units in total [MR, ResearchInChina]. Gasgoo, which counts main "
      "lidars separately, puts 2025 at 2.756 M main units, 1.143 M of them Hesai's "
      f"[T, [Gasgoo, 21 May 2026]({GASGOO})].")),
    ("b1-q1-2026", "- In Q1 2026 (the first quarter) 985k were installed.",
     "- In Q1 2026 (the first quarter) more than 985k lidars were installed, by Gasgoo's count, with Hesai at "
     "34.9%, Huawei 32.3%, Seyond 16.8% and RoboSense 11.0% [T, Gasgoo]."),
    ("b4a-eq14-merge", "- **Stopping distance scales with speed squared.**",
     {"block": 5,
      "text": "- **Stopping distance scales with speed squared.** A vehicle that reacts and then brakes at a "
              "constant rate stops within the distance of Eq. (11) (§A6.1), "
              "$d=v\\,t_{\\rm r}+v^2/(2a_{\\rm b})$, where $d$ is the stopping distance (m), $v$ the initial "
              "speed (m/s; km/h divided by 3.6), $t_{\\rm r}$ the reaction time before braking begins (s), and "
              "$a_{\\rm b}$ the braking deceleration (m/s²). The first term is the distance covered while "
              "reacting, the second the braking distance. The equation assumes a level road and constant "
              "deceleration. Here the reaction time is taken as 1 s and the deceleration as 5 m/s²; both are "
              "assumed round values."}),
    ("b4a-eq14-ref1", "**The sensing need scales with speed squared.**",
     ("sub", "The stopping distance of Eq. (14),", "The stopping distance of Eq. (11) (§A6.1),")),
    ("b4a-eq14-ref2", "- **Stopping distance** is reaction distance plus braking distance",
     ("sub", "braking distance, Eq. (14), with", "braking distance, Eq. (11), with")),
]
