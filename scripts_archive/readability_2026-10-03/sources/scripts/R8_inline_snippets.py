"""R8_C9a_inband: one-off snippets run inline during the research, collected
for the archive. Generic User-Agent, no email, no key; paths are arguments or
relative to a scratch folder <scratch>.

1. split_tall_image(path, step): cut a tall chart image (NE Times charts are
   944 x 2957 px) into 1,000-px strips for reading.
2. robosense_pages(out_dir): save RoboSense's per-product resource pages and
   product pages (English and Chinese sites) and print any line that mentions a
   wavelength. The download lists sit behind a contact form, which was not
   filled in.
3. sec_attempt(url): the SEC EDGAR full-text request that was refused (HTTP 403)
   because no contact address was sent; none was added.
"""
import re
import sys
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def split_tall_image(path, step=1000):
    from PIL import Image
    im = Image.open(path)
    w, h = im.size
    for i, y in enumerate(range(0, h, step)):
        im.crop((0, y, w, min(h, y + step))).save(path.rsplit(".", 1)[0] + f"_part{i}.png")
    return w, h


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def robosense_pages(out_dir):
    pages = [f"https://www.robosense.ai/en/resources-{n}" for n in
             (11, 20, 64, 81, 89, 99, 111, 117, 143, 160, 161, 181, 184, 188, 191)]
    for site in ("https://www.robosense.ai/en/", "https://www.robosense.cn/"):
        for p in ("rslidar/EMX", "rslidar/EM4", "rslidar/E1", "rslidar/MX", "rslidar/M1P",
                  "rslidar/E1R", "IncrementalComponents/EMX", "IncrementalComponents/MX"):
            pages.append(site + p)
    for url in pages:
        try:
            html = _get(url)
        except Exception as e:  # noqa: BLE001
            print(url, "ERR", e)
            continue
        fn = out_dir + "/" + re.sub(r"[^A-Za-z0-9]+", "_", url)[-60:] + ".html"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(html)
        txt = re.sub(r"<[^>]+>", "\n", re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S))
        hits = [l.strip() for l in txt.split("\n") if re.search(r"\d\s?nm\b|[Ww]avelength|波长", l)]
        print(url, len(html), "bytes;", "wavelength lines:", hits[:3] if hits else "none")


def sec_attempt(url):
    try:
        _get(url)
    except urllib.error.HTTPError as e:
        print("refused:", e.code)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd = sys.argv[1]
    if cmd == "split":
        print(split_tall_image(sys.argv[2]))
    elif cmd == "robosense":
        robosense_pages(sys.argv[2])
    elif cmd == "sec":
        sec_attempt(sys.argv[2])
