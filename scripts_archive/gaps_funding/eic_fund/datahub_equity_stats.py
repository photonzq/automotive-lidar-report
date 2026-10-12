"""Equity-field statistics from the public EIC Data Hub files.

Reads raw/datahub_eic-data-core.json and raw/datahub_eic-data-extend.json
(see datahub_explore.py) and, for EIC Accelerator coordinator roles, tabulates
the per-role 'equity' object ({active, amount, consent}) against the project's
budget type (Blended finance / Grant only / Grant first / Equity only ...) and
against the EIC Fund portfolio list (eic_fund_portfolio.json). Prints the full
records for the two target projects (101218255 VoxelSensors SPAES and
190195250 Hybrid Lidar LiSSA 3D) and for the cut-off cohorts of 11 Jan 2023
and Oct 2024. Writes datahub_accelerator_roles.csv.

Run from the eic_fund folder:  python scripts/datahub_equity_stats.py
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

core = json.loads(Path("raw/datahub_eic-data-core.json").read_text(encoding="utf-8"))["content"]
ext = json.loads(Path("raw/datahub_eic-data-extend.json").read_text(encoding="utf-8"))["content"]
port = json.loads(Path("eic_fund_portfolio.json").read_text(encoding="utf-8"))

partners = {p["id"]: p for p in core["partners"]}
pext = {p["id"]: p for p in ext["partners"]}
projects = {p["id"]: p for p in core["projects"]}
prext = {p["id"]: p for p in ext["projects"]}

STOP = {"gmbh", "ltd", "limited", "ab", "bv", "b", "v", "sl", "sas", "sa", "oy", "aps", "nv",
        "srl", "ag", "as", "lda", "ad", "spa", "sarl", "inc", "the", "s", "l", "r"}


def norm(s):
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return " ".join(t for t in s.split() if t not in STOP)


port_norm = {norm(p["name"]): p["name"] for p in port}


def in_portfolio(name):
    n = norm(name)
    if n in port_norm:
        return port_norm[n]
    for pn, orig in port_norm.items():
        if len(n) > 5 and len(pn) > 5 and (n.startswith(pn) or pn.startswith(n)):
            return orig
    return ""


rows = []
for r in core["roles"]:
    pr = projects.get(r["project"], {})
    px = prext.get(r["project"], {})
    cat = px.get("cat", {})
    if cat.get("program") != "Accelerator" or r["role"] != "COORDINATOR":
        continue
    part = partners.get(r["partner"], {})
    rows.append({
        "project": r["project"], "acronym": pr.get("acronym"),
        "partner": r["partner"], "name": part.get("name", ""), "nuts": part.get("nuts", ""),
        "budget_type": (pr.get("budget") or {}).get("type"),
        "grant": (pr.get("budget") or {}).get("grant"),
        "jury": (pr.get("budget") or {}).get("jury"),
        "total": (pr.get("budget") or {}).get("total"),
        "ec_contrib": r["ec_contrib"], "status": r["status"],
        "eq_active": r["equity"]["active"], "eq_amount": r["equity"]["amount"],
        "eq_consent": r["equity"]["consent"],
        "badge_equity": (px.get("badges") or {}).get("equity"),
        "call": cat.get("call"), "cutoff": (px.get("history") or {}).get("call"),
        "start": (px.get("history") or {}).get("start"), "end": (px.get("history") or {}).get("end"),
        "in_eic_fund_portfolio": in_portfolio(part.get("name", "")),
    })

with open("datahub_accelerator_roles.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print("Accelerator coordinator roles:", len(rows))
print("\nbudget_type x (eq_active, consent, amount>0, badge_equity):")
tab = Counter((r["budget_type"], r["eq_active"], r["eq_consent"], (r["eq_amount"] or 0) > 0, r["badge_equity"]) for r in rows)
for k, v in sorted(tab.items(), key=lambda kv: (str(kv[0][0]), -kv[1])):
    print(f"  {str(k[0]):18s} active={str(k[1]):5s} consent={str(k[2]):5s} amount>0={str(k[3]):5s} badge={str(k[4]):5s} : {v}")

print("\nportfolio-listed vs eq_active (Accelerator coordinators):")
tab2 = Counter((bool(r["in_eic_fund_portfolio"]), r["eq_active"], (r["eq_amount"] or 0) > 0) for r in rows)
for k, v in sorted(tab2.items()):
    print(f"  listed={k[0]!s:5s} active={k[1]!s:5s} amount>0={k[2]!s:5s} : {v}")

print("\nby cut-off date (eq_active true / total, with amount>0, listed in portfolio):")
by = defaultdict(lambda: [0, 0, 0, 0])
for r in rows:
    k = r["cutoff"]
    by[k][0] += 1
    by[k][1] += bool(r["eq_active"])
    by[k][2] += (r["eq_amount"] or 0) > 0
    by[k][3] += bool(r["in_eic_fund_portfolio"])
for k in sorted(by, key=str):
    t, a, m, l = by[k]
    print(f"  {k}: total {t:3d} | eq_active {a:3d} | amount>0 {m:3d} | in EICF portfolio list {l:3d}")

for pid in (101218255, 190195250):
    print("\n=== target project", pid, "===")
    print(json.dumps(projects.get(pid), ensure_ascii=False))
    x = dict(prext.get(pid, {}))
    x.pop("abstract", None)
    print(json.dumps(x, ensure_ascii=False))
    for r in core["roles"]:
        if r["project"] == pid:
            print(json.dumps(r), partners.get(r["partner"]), pext.get(r["partner"]))

for cut in ("2023-01-11", "2024-10-03"):
    print(f"\n=== cohort cut-off {cut} ===")
    for r in sorted((r for r in rows if r["cutoff"] == cut), key=lambda r: (str(r["budget_type"]), r["name"])):
        print(f"  {str(r['budget_type']):16s} act={r['eq_active']!s:5s} amt={r['eq_amount']:>12,.0f} cons={r['eq_consent']!s:5s} "
              f"badge={r['badge_equity']!s:5s} st={str(r['status']):10s} listed={r['in_eic_fund_portfolio'][:22]:22s} {r['name']}")
