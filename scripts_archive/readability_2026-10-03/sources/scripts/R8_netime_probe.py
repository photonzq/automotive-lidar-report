"""R8_C9a_inband: print the page titles of a range of NE Times (ne-time.cn)
article IDs, to locate the monthly lidar-installation articles; generic
User-Agent, no email, no key.

Usage: python R8_netime_probe.py <first_id> <last_id> [step]
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    a, b = int(sys.argv[1]), int(sys.argv[2])
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    for i in range(a, b + 1, step):
        try:
            req = urllib.request.Request(f"https://www.ne-time.cn/web/article/{i}",
                                         headers={"User-Agent": UA})
            html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
            m = re.search(r"<title>(.*?)</title>", html, re.S)
            t = m.group(1).strip() if m else "?"
        except Exception as e:  # noqa: BLE001
            t = f"ERR {e}"
        print(i, t)


if __name__ == "__main__":
    main()
