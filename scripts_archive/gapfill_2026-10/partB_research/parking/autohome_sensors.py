"""Extract perception-sensor rows from saved Autohome (汽车之家) config pages.

Usage:
    python autohome_sensors.py <config_page.html> [<config_page.html> ...]
    python autohome_sensors.py --all <config_page.html>   # dump every row name

The script reads the JSON objects that the page embeds as
`var config = {...};` (parameters) and `var option = {...};` (equipment),
removes the font-obfuscation <span> tags from names, and prints, per trim
(specid), the rows that matter for parking/near-field sensing:
超声波雷达数量, 毫米波雷达数量, 激光雷达数量, 激光雷达品牌, 激光雷达型号,
激光雷达线数, 摄像头 rows, 自动泊车/泊车 rows.

Notes:
- Autohome replaces some characters in row names with <span class='hs_kw..'>
  glyph placeholders; those characters are dropped here, so a name such as
  "激光雷达型<span ..>" prints as "激光雷达型". Matching uses substrings.
- A trim that lacks a row shows "-" or nothing in Autohome's own table.
"""
import json
import re
import sys

KEYS = ["超声波", "毫米波雷达", "激光雷达", "摄像头", "泊车", "车型"]


def load_json_var(text, var):
    m = re.search(r"var\s+" + var + r"\s*=\s*", text)
    if not m:
        return None
    start = m.end()
    dec = json.JSONDecoder()
    obj, _ = dec.raw_decode(text[start:])
    return obj


def clean(s):
    return re.sub(r"<[^>]+>", "", s or "")


def rows_from(obj, kind):
    out = []
    if not obj:
        return out
    res = obj.get("result", {})
    groups = res.get("paramtypeitems" if kind == "param" else "configtypeitems", [])
    for g in groups:
        items = g.get("paramitems" if kind == "param" else "configitems", [])
        for it in items:
            name = clean(it.get("name", ""))
            vals = {}
            for v in it.get("valueitems", []):
                sid = v.get("specid")
                val = clean(v.get("value", ""))
                subs = v.get("sublist") or []
                if subs:
                    val = (val + " " if val else "") + "; ".join(
                        clean(s.get("subname", "")) for s in subs)
                vals[sid] = val.strip()
            out.append((name, vals))
    return out


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = argv[1:]
    dump_all = False
    if args and args[0] == "--all":
        dump_all = True
        args = args[1:]
    if not args:
        print(__doc__)
        return 1
    for path in args:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        title = re.search(r"<title>([^<]*)</title>", text)
        print("=" * 80)
        print(path, "|", title.group(1) if title else "")
        rows = rows_from(load_json_var(text, "config"), "param") + \
            rows_from(load_json_var(text, "option"), "config")
        # trim names
        names = {}
        for name, vals in rows:
            if name.startswith("车型"):
                names = vals
                break
        for sid, nm in names.items():
            print(f"  specid {sid}: {nm}")
        for name, vals in rows:
            if dump_all or any(k in name for k in KEYS):
                cells = " | ".join(f"{sid}:{v}" for sid, v in vals.items())
                print(f"  {name}: {cells}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
