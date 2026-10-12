from pathlib import Path
here = Path(__file__).parent
src = (here.parent / "fmcw_tof_system_budget.py").read_text(encoding="utf-8")


def rep(old, new):
    global src
    assert src.count(old) == 1, old[:60]
    src = src.replace(old, new)


rep('''        (3.84e6, 8.0, "ATX, 230 m", COLORS["primary"], "s", (-52, 4)),
        (15.0e6, 13.0, "ETX, 300 m", COLORS["primary"], "s", (-14, -15)),
        (1.5e6, 45.0, "LuminWave F1, 250 m", COLORS["warm_accent"], "^", (-30, 7)),
    ]
    for x_p, y_p, lab, col, mk, off in products:
        ax.plot(x_p, y_p, mk, color=col, mfc="white", mew=1.2, ms=5, label="_nolegend_", zorder=5)
        ax.annotate(lab, (x_p, y_p), xytext=off, textcoords="offset points", color=col)''',
'''        (3.84e6, 8.0, "ATX", COLORS["primary"], "s", (0, -6), "center", "top"),
        (15.0e6, 13.0, "ETX", COLORS["primary"], "s", (0, 5), "center", "bottom"),
        (1.5e6, 45.0, "LuminWave F1", COLORS["warm_accent"], "^", (0, 5), "center", "bottom"),
    ]
    for x_p, y_p, lab, col, mk, off, ha, va in products:
        ax.plot(x_p, y_p, mk, color=col, mfc="white", mew=1.2, ms=5, label="_nolegend_", zorder=5)
        ax.annotate(lab, (x_p, y_p), xytext=off, textcoords="offset points", color=col,
                    ha=ha, va=va)''')
rep('''    ax.set_ylim(1, 3000)''', '''    ax.set_ylim(1, 1e4)''')
rep('''    ax.text(6e5, 2200, "\\n".join(note), color=COLORS["annotation"], va="top")''',
    '''    ax.text(6e5, 7000, "\\n".join(note), color=COLORS["annotation"], va="top")''')
src = src.replace('OUT_DIR = _output_dir()', 'OUT_DIR = Path(__file__).resolve().parent')
(here / "fmcw_tof_system_budget.py").write_text(src, encoding="utf-8")
print("ok")
