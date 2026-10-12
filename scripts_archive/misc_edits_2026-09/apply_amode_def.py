from pathlib import Path
here = Path(__file__).resolve().parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = rp.read_bytes(); assert raw == (here / "report_after_c0_10.md").read_bytes(), "report changed since last snapshot"
s = raw.decode("utf-8"); missing = []


def rep(old, new):
    global s
    if s.count(old) != 1:
        missing.append((s.count(old), old[:90])); return
    s = s.replace(old, new, 1)


# 1. C0.10 variables list: define P_tx, P_het and A_mode in words
rep(r"""- $D$: diameter of the receive lens (direct detection), or of the shared transmit–receive aperture (monostatic coherent). $A_{\rm rx}=\pi D^2/4$.
""",
    r"""- $D$: diameter of the receive lens (direct detection), or of the shared transmit–receive aperture (monostatic coherent). $A_{\rm rx}=\pi D^2/4$.
- $P_{\rm tx}$: transmitted optical power. $P_{\rm het}$: the signal a coherent receiver collects in its local oscillator's (LO's) spatial mode and polarization, expressed as an equivalent optical power.
- $A_{\rm mode}$: the *mode-equivalent collecting area* of a coherent receiver (m²).
  - **Definition.** It is the area of an ideal direct-detection lens that would collect, from the same Lambertian target, the same signal power as the coherent receiver collects in its single LO mode. It takes the place of $A_{\rm rx}$ in the link budget: $P_{\rm het}=P_{\rm tx}\,\rho A_{\rm mode}/(\pi R^2)$ before atmospheric loss.
  - **Not a physical area.** It depends on the range and on the beam, and is usually much smaller than the aperture: 63 mm² against the 491 mm² of a 25 mm aperture at 200 m. Item (a) derives it.
""")

# 2. C7b 1(b): define A_mode itself before its ingredients
rep(r"""  - **Variables and derivation.** $\lambda$ is the wavelength,""",
    r"""  - **Variables and derivation.** $A_{\rm mode}$ is the mode-equivalent collecting area: the area of an ideal direct-detection lens that would collect the same signal from the same target as the coherent receiver collects in its single LO mode, so it replaces the lens area in the link budget. $\lambda$ is the wavelength,""")

print("missing", missing); assert not missing
assert "\t" not in s and "\r\n" not in s
assert rp.read_bytes() == raw, "report changed while editing"
rp.write_bytes(s.encode("utf-8")); (here / "report_after_amode_def.md").write_bytes(s.encode("utf-8"))
print("ok", len(s.encode("utf-8")))
