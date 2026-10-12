"""R7 item 03 (extension): are SGO 'Incident Time' values local time or UTC, by reporting entity?

For every record (latest version per Report ID) in the SGO ADAS archive CSV that has a time,
a US state and a definite Lighting value, compute the mid-month solar elevation at the state's
approximate centroid with the time read (a) as local civil time and (b) as UTC, and score
whether each reading agrees with the Lighting field. Tesla is compared with other entities.

Usage: python R7_sgo_utc_test_all.py <SGO-2021-01_Incident_Reports_ADAS.csv (archive)>
Approximations: state centroids; one dominant time zone per state; US DST rules.
"""
import calendar
import math
import sys
from datetime import datetime, timedelta

import pandas as pd

# state: (lat, lon east+, standard UTC offset, observes DST)
S = {
    "AL": (32.8, -86.8, -6, 1), "AZ": (34.3, -111.7, -7, 0), "AR": (34.9, -92.4, -6, 1),
    "CA": (36.8, -119.4, -8, 1), "CO": (39.0, -105.5, -7, 1), "CT": (41.6, -72.7, -5, 1),
    "DE": (39.0, -75.5, -5, 1), "DC": (38.9, -77.0, -5, 1), "FL": (28.6, -82.4, -5, 1),
    "GA": (32.7, -83.4, -5, 1), "ID": (44.4, -114.6, -7, 1), "IL": (40.0, -89.2, -6, 1),
    "IN": (39.9, -86.3, -5, 1), "IA": (42.1, -93.5, -6, 1), "KS": (38.5, -98.4, -6, 1),
    "KY": (37.5, -85.3, -5, 1), "LA": (31.1, -92.0, -6, 1), "ME": (45.4, -69.2, -5, 1),
    "MD": (39.0, -76.8, -5, 1), "MA": (42.3, -71.8, -5, 1), "MI": (44.3, -85.4, -5, 1),
    "MN": (46.3, -94.3, -6, 1), "MS": (32.7, -89.7, -6, 1), "MO": (38.4, -92.5, -6, 1),
    "MT": (47.0, -109.6, -7, 1), "NE": (41.5, -99.8, -6, 1), "NV": (39.3, -116.6, -8, 1),
    "NH": (43.7, -71.6, -5, 1), "NJ": (40.2, -74.7, -5, 1), "NM": (34.4, -106.1, -7, 1),
    "NY": (42.9, -75.5, -5, 1), "NC": (35.6, -79.4, -5, 1), "ND": (47.5, -100.5, -6, 1),
    "OH": (40.3, -82.8, -5, 1), "OK": (35.6, -97.5, -6, 1), "OR": (43.9, -120.6, -8, 1),
    "PA": (40.9, -77.8, -5, 1), "RI": (41.7, -71.5, -5, 1), "SC": (33.9, -80.9, -5, 1),
    "SD": (44.4, -100.2, -6, 1), "TN": (35.9, -86.4, -6, 1), "TX": (31.5, -99.3, -6, 1),
    "UT": (39.3, -111.7, -7, 1), "VT": (44.1, -72.7, -5, 1), "VA": (37.5, -78.9, -5, 1),
    "WA": (47.4, -120.5, -8, 1), "WV": (38.6, -80.6, -5, 1), "WI": (44.6, -89.9, -6, 1),
    "WY": (43.0, -107.6, -7, 1), "HI": (20.8, -156.3, -10, 0),
}
MON = {m.upper(): i for i, m in enumerate(calendar.month_abbr) if m}


def elev(dt_utc, lat, lon):
    doy = dt_utc.timetuple().tm_yday
    hour = dt_utc.hour + dt_utc.minute / 60
    g = 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                    - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    dec = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
           + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    ha = math.radians((hour * 60 + eqt + 4 * lon) / 4 - 180)
    la = math.radians(lat)
    c = math.sin(la) * math.sin(dec) + math.cos(la) * math.cos(dec) * math.cos(ha)
    return 90 - math.degrees(math.acos(max(-1.0, min(1.0, c))))


def dst(day):
    y = day.year
    mar = [d for d in range(8, 15) if calendar.weekday(y, 3, d) == 6][0]
    nov = [d for d in range(1, 8) if calendar.weekday(y, 11, d) == 6][0]
    return datetime(y, 3, mar, 2) <= day < datetime(y, 11, nov, 2)


def agrees(light, e):
    if light == "Daylight":
        return e > -1.0
    if light.startswith("Dark"):
        return e < -3.0
    if light.startswith("Dawn"):
        return -12.0 < e < 10.0
    return None


df = pd.read_csv(sys.argv[1], dtype=str, encoding="latin-1", low_memory=False)
df["v"] = pd.to_numeric(df["Report Version"], errors="coerce")
df = df.sort_values("v").groupby("Report ID", as_index=False).last()
ent_col = "Reporting Entity" if "Reporting Entity" in df.columns else "Make"
rows = []
for _, r in df.iterrows():
    t, st, light, dt = r.get("Incident Time (24:00)"), str(r.get("State")).strip(), r.get("Lighting"), r.get("Incident Date")
    if not isinstance(t, str) or ":" not in t or st not in S or not isinstance(light, str):
        continue
    if light not in ("Daylight", "Dawn / Dusk") and not light.startswith("Dark"):
        continue
    try:
        mon, yr = dt.split("-")
        y, m = int(yr), MON[mon.upper()]
    except Exception:
        continue
    hh, mm = map(int, t.split(":"))
    lat, lon, off, obs = S[st]
    day = datetime(y, m, 15, hh, mm)
    o = off + (1 if (obs and dst(day)) else 0)
    e_local = elev(day - timedelta(hours=o), lat, lon)
    e_utc = elev(day, lat, lon)
    rows.append((str(r[ent_col]).strip(), agrees(light, e_local), agrees(light, e_utc)))

res = pd.DataFrame(rows, columns=["entity", "local_ok", "utc_ok"])
res["group"] = res["entity"].where(res["entity"].str.contains("Tesla", case=False), "All other entities")
res.loc[res["entity"].str.contains("Tesla", case=False), "group"] = "Tesla"
summ = res.groupby("group").agg(n=("local_ok", "size"), local_agree=("local_ok", "mean"), utc_agree=("utc_ok", "mean"))
print(summ.to_string(float_format=lambda x: f"{x:.3f}"))
top = res[res.group != "Tesla"].groupby("entity").agg(n=("local_ok", "size"), local=("local_ok", "mean"),
                                                       utc=("utc_ok", "mean")).sort_values("n", ascending=False)
print("\nLargest other entities:")
print(top.head(8).to_string(float_format=lambda x: f"{x:.3f}"))
