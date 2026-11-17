"""Print licence, author and pixel size of Wikimedia Commons files through the public API.

Usage: commons_check.py "File:Name1.jpg" "File:Name2.jpg" ...
"""
import json
import re
import sys

import requests

UA = {"User-Agent": "report-check/1.0 (research)"}
params = {
    "action": "query", "format": "json", "prop": "imageinfo", "iiprop": "size|extmetadata|url",
    "titles": "|".join(sys.argv[1:]),
}
r = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=UA, timeout=40)
for page in r.json()["query"]["pages"].values():
    title = page.get("title")
    info = (page.get("imageinfo") or [{}])[0]
    meta = info.get("extmetadata", {})
    lic = meta.get("LicenseShortName", {}).get("value")
    artist = re.sub(r"<[^>]+>", "", meta.get("Artist", {}).get("value", ""))
    print(json.dumps({"title": title, "w": info.get("width"), "h": info.get("height"), "licence": lic,
                      "author": artist.strip()[:80], "url": info.get("url")}, ensure_ascii=False))
