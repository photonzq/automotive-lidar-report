from pathlib import Path

fp = Path(r"<report folder>\build\figures\link_budget_scaling.py")
s = fp.read_text(encoding="utf-8")

old_b = '''    for x0, x1, txt in ((0.05, 0.2, "thick\\nfog"), (0.2, 1.0, "fog"), (1.0, 4.0, "thin fog,\\nhaze"),
                        (4.0, 23.0, "light haze,\\nclear")):'''
new_b = '''    # fog is visibility below 1 km: thick fog 50-200 m, moderate to light fog 200 m - 1 km (international visibility code)
    for x0, x1, txt in ((0.05, 0.2, "thick\\nfog"), (0.2, 1.0, "fog"), (1.0, 10.0, "mist,\\nhaze"), (10.0, 23.0, "clear")):'''
assert s.count(old_b) == 1, ("fog labels", s.count(old_b))
s = s.replace(old_b, new_b)

old_c = '''    ax_c.axvspan(10, 50, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, zorder=0, label="_nolegend_")
    for x0, x1, txt in ((1.0, 2.5, "light"), (2.5, 10.0, "moderate"), (10.0, 50.0, "heavy"), (50.0, 150.0, "violent")):'''
new_c = '''    # rain classes of MANOBS and the AMS glossary (0.1 and 0.3 in/h), violent above 50 mm/h; WMO has no agreed definition
    ax_c.axvspan(7.6, 50, color=COLORS["highlight"], alpha=HIGHLIGHT_ALPHA, lw=0, zorder=0, label="_nolegend_")
    for x0, x1, txt in ((1.0, 2.5, "light"), (2.5, 7.6, "moderate"), (7.6, 50.0, "heavy"), (50.0, 150.0, "violent")):'''
assert s.count(old_c) == 1, ("rain labels", s.count(old_c))
s = s.replace(old_c, new_c)

fp.write_bytes(s.encode("utf-8"))
print("patched", len(s))
