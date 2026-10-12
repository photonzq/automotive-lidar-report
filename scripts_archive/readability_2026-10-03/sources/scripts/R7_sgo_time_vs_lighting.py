"""R7 item 03: test whether Tesla's SGO 'Incident Time' fields are local time or UTC.

For each SGO archive record that has both a time and a 'Lighting' field, compute the solar
elevation at the recorded clock time read (a) as local civil time and (b) as UTC, for every
day of the recorded month (the public file gives only month and year). Compare with the
record's own Lighting field. Solar position: NOAA simplified algorithm (about 0.5 deg).
City coordinates are approximate town centres.
"""
import calendar
import math
from datetime import datetime, timedelta


def solar_elevation(dt_utc, lat, lon):
    """Solar elevation in degrees (NOAA general solar position equations)."""
    doy = dt_utc.timetuple().tm_yday
    hour = dt_utc.hour + dt_utc.minute / 60
    g = 2 * math.pi / 365 * (doy - 1 + (hour - 12) / 24)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                       - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
            - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
            - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    tst = hour * 60 + eqtime + 4 * lon          # true solar time, minutes (lon east +)
    ha = math.radians(tst / 4 - 180)
    la = math.radians(lat)
    cosz = math.sin(la) * math.sin(decl) + math.cos(la) * math.cos(decl) * math.cos(ha)
    return 90 - math.degrees(math.acos(max(-1, min(1, cosz))))


def utc_offset(tz, day):
    """Offset of local civil time from UTC in hours for the US zones needed here."""
    y = day.year
    # US DST: second Sunday in March to first Sunday in November
    mar = [d for d in range(8, 15) if calendar.weekday(y, 3, d) == 6][0]
    nov = [d for d in range(1, 8) if calendar.weekday(y, 11, d) == 6][0]
    dst = datetime(y, 3, mar, 2) <= day < datetime(y, 11, nov, 2)
    base = {"MST_noDST": -7, "PT": -8, "CT": -6, "ET": -5}[tz]
    if tz == "MST_noDST":
        return base
    return base + (1 if dst else 0)


records = [  # id, city, lat, lon (east +), tz, year, month, hh:mm, lighting field
    ("13781-8004", "Rimrock AZ", 34.65, -111.79, "MST_noDST", 2023, 11, "00:03", "Dawn / Dusk"),
    ("13781-7381", "Red Mills VA", 37.9, -78.5, "ET", 2024, 3, "19:19", "Daylight"),
    ("13781-7767", "Collinsville OH", 39.48, -84.60, "ET", 2024, 5, "10:16", "Dawn / Dusk"),
    ("13781-7964", "Fullerton CA", 33.87, -117.92, "PT", 2024, 6, "07:03", "Dark - Lighted"),
    ("13781-8977", "Issaquah WA", 47.53, -122.03, "PT", 2024, 10, "20:40", "Daylight"),
    ("13781-9267", "Stockton CA", 37.96, -121.29, "PT", 2024, 11, "11:30", "Dark - Lighted"),
]

for rid, city, lat, lon, tz, y, m, hm, light in records:
    hh, mm = map(int, hm.split(":"))
    ndays = calendar.monthrange(y, m)[1]
    loc_el, utc_el, loc_clock = [], [], []
    for d in range(1, ndays + 1):
        # (a) recorded time read as local civil time
        local = datetime(y, m, d, hh, mm)
        off = utc_offset(tz, local)
        loc_el.append(solar_elevation(local - timedelta(hours=off), lat, lon))
        # (b) recorded time read as UTC
        u = datetime(y, m, d, hh, mm)
        utc_el.append(solar_elevation(u, lat, lon))
        lc = u + timedelta(hours=utc_offset(tz, u))
        loc_clock.append(lc.strftime("%H:%M"))
    print(f"{rid} {city} {y}-{m:02d} time {hm}, lighting field '{light}':")
    print(f"   read as local time: sun elevation {min(loc_el):6.1f} to {max(loc_el):6.1f} deg over the month")
    print(f"   read as UTC (local {sorted(set(loc_clock))}): sun elevation "
          f"{min(utc_el):6.1f} to {max(utc_el):6.1f} deg")

# Rimrock specifically: 27 Nov 2023 17:03 MST = 28 Nov 2023 00:03 UTC
t = datetime(2023, 11, 28, 0, 3)
print(f"Rimrock 27 Nov 2023 17:03 MST (= {t:%d %b %Y %H:%M} UTC): sun elevation "
      f"{solar_elevation(t, 34.65, -111.79):.1f} deg")
for hhmm in ("17:00", "17:10", "17:20", "17:30"):
    h, mi = map(int, hhmm.split(":"))
    tt = datetime(2023, 11, 27, h, mi) + timedelta(hours=7)
    print(f"   {hhmm} MST: {solar_elevation(tt, 34.65, -111.79):5.1f} deg")
