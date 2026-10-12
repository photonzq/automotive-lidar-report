"""My amendments to the Round 4 research agents' proposed edits, read by round4_build_from_findings.py.

AMEND[edit id] = list of (exact substring of the agent's "new" text, replacement), each with its reason.
APPX_GROUPS[item id] = the Appendix 2 group for an item whose findings name none (chosen by the section the source
supports).
"""
APPX_GROUPS = {
    "R3_C4d-C9_C5-C6-01": "Lidar market and Western programs",
    "R3_C4d-C9_C5-C6-04": "Technology routes and SPAD",
    "R3_C4d-C9_C5-C6-05": "Technology routes and SPAD",
    "R3_C4d-C9_C5-C6-06": "Technology routes and SPAD",
    "R3_C4d-C9_C5-C6-07": "Fastree3D history (§C3a subsection 2; §C5)",
    "R3_C4d-C9_C5-C6-09": "Technology routes and SPAD",
    "R3_C4d-C9_C5-C6-10": "Technology routes and SPAD",
    "R3_C4d-C9_C5-C6-11": "Technology routes and SPAD",
    "R3_C4d-C9_C5-C6-12": "Fastree3D history (§C3a subsection 2; §C5)",
    "R3_C4d-C9_C5-C6-13": "Technology routes and SPAD",
}
AMEND = {
    # R7 item 03: state which rate is which for the other companies, as for Tesla.
    "R4_R7_E9-E12-03a": [
        ("whereas for the 217 such reports from all other companies the figures are 50% and 93% "
         "[E: mid-month solar elevation at each state's centre].",
         "whereas the 217 such reports from all other companies agree with local time (93%) and not with UTC (50%) "
         "[E: mid-month solar elevation at each state's centre]."),
    ],
    # R1 item 07: the attribution of fault rests on police statements relayed by the press, not on the SGO reports.
    "R4_R1_partA_E2-E5-07": [
        ("No fatal crash in those miles has been attributed to the Waymo Driver:",
         "No fatal crash in those miles has been attributed to the Waymo Driver [T, police statements relayed by "
         "NBC Bay Area and azfamily.com]:"),
    ],
    # R1 item 10(a): keep the urban/rural split and the road-type split apart.
    "R4_R1_partA_E2-E5-10a": [
        ("most of these (70%) were in urban areas, mainly on arterial roads (56%), and fewer on rural roads (29%) or on "
         "interstates and freeways (22%) [I, NHTSA FARS 2024; E].",
         "70% of these were in urban areas and 29% in rural areas, and by road type 56% were on arterials other than "
         "freeways, 22% on interstates and freeways and 21% on collectors and local roads [I, NHTSA FARS 2024; E]."),
    ],
    # R5 item 02(a): state the conclusion the simulation supports (peak to highest floor point against the measured
    # 3-6 dB), and say what the bracketed simulation covered.
    "R4_R5_C10_part1-02a": [
        ("and the floor's highest points lie 5–6 dB above that mean [E: 120 random emitters over 6 mm seen through a "
         "0.13° Gaussian response give 11 dB to the mean floor and 4–6.5 dB to its highest point].",
         "and the floor's highest points lie about 5–6 dB above that mean, so only about 4–6.5 dB below the observed "
         "peak, close to the measured 3–6 dB [E: 20 layouts of 120 random emitters over 6 mm with exact amplitudes, "
         "seen through a 0.13° Gaussian response, give 11 dB from the observed peak to the mean floor and 4–6.5 dB to "
         "the floor's highest point]."),
    ],
    # R5 item 04(a): Jilin University and CIOMP's 64-channel OPA reached 109 m on a 90% reflector behind a lens
    # (Zhang et al., Opt. Express 30, 5008 (2022), p. 5016, read; already in the section D7 table), so the 2021 device
    # is not the only 100 m result. Li et al. also used the OPA as the receiver with a collimator transmitting
    # (their Figs. 7b and 8d), so "the other side of the link" replaces "as receiver".
    "R4_R5_C10_part1-04a": [
        ("100 m has been shown only on a 90% scatter plate, by Jilin University's 128-channel OPA (Li *et al.*, "
         "*Photon. Res.* 2021), with the path folded by a mirror beyond 50 m and a fibre collimator as receiver [P]; "
         "that is ≈33 m at 10% under $R^2$ scaling.",
         "100 m has been shown only on 90% targets over mirror-folded paths: by Jilin University's 128-channel OPA "
         "(Li *et al.*, *Photon. Res.* 2021), with a fibre collimator on the other side of the link [P], and, at 109 m, "
         "by the 64-channel OPA of Jilin University and the Changchun Institute of Optics, Fine Mechanics and Physics "
         "(CIOMP), with a bulk lens in front of the chip (36 m without it; Zhang *et al.*, *Opt. Express* 2022, §D7) "
         "[P]. 100 m on a 90% target is ≈33 m at 10% under $R^2$ scaling."),
    ],
    "R4_R5_C10_part1-04b": [
        ("by Jilin University's 128-channel OPA in 2021 (§C10.2b)",
         "by Jilin University's OPAs in 2021 and 2022 (§C10.2b; §D7)"),
    ],
    # R5 item 04(d): the 1.8 µW is the maximum static power of one shifter (Li et al., p. 2512), and the OPA served as
    # either end of the link (Figs. 7b, 8d).
    "R4_R5_C10_part1-04d": [
        ("PN shifters ≤1.8 µW static;", "PN shifters ≤1.8 µW static each;"),
        ("(path folded by a mirror beyond 50 m; OPA transmit, fibre-collimator receive)",
         "(path folded by a mirror beyond 50 m; the OPA at one end of the link, a fibre collimator at the other)"),
    ],
    # R5 item 06: "largest reported" cannot be proven; say it is the largest this search found.
    "R4_R5_C10_part1-06": [
        ("The largest integrated 2D phased arrays reported with a phase control per element are far smaller:",
         "The largest integrated 2D phased arrays with a phase control per element found for this report are far "
         "smaller:"),
    ],
    # R5 item 08(b): the SR-1S sheet itself lists the beam spot, so it is not borrowed from the FS-4S sheet.
    "R4_R5_C10_part1-08b": [
        ("beam ≤0.04° × 0.02° FWHM (as on the FS-4S sheet)", "beam ≤0.04° × 0.02° FWHM (as for the FS-4S)"),
    ],
    # R5 item 09(a): the report writes I/Q (section C7a table).
    "R4_R5_C10_part1-09a": [
        ("OPA-B1 an I-Q coherent receiver [P]", "OPA-B1 an I/Q coherent receiver [P]"),
    ],
}
