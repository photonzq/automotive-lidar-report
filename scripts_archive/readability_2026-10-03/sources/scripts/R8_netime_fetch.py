"""R8_C9a_inband: fetch an NE Times (ne-time.cn) article page with a generic
User-Agent (no email, no key), print its title and the text lines that carry
lidar numbers, and download its chart images. The page's img.ne-time.cn image
paths are WeChat image hashes; this host did not resolve here, so each image is
fetched from the WeChat image CDN (mmbiz.qpic.cn), trying the sz_mmbiz_png,
sz_mmbiz_jpg, mmbiz_png and mmbiz_jpg prefixes and keeping the first response
larger than 1 kB. Tall images are split into 1,000-px strips for reading.

Usage: python R8_netime_fetch.py <article_id> <out_dir>
"""
import os
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, referer=None):
    headers = {"User-Agent": UA}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    aid, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    html = fetch(f"https://www.ne-time.cn/web/article/{aid}").decode("utf-8", "replace")
    with open(os.path.join(out_dir, f"netime_{aid}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    print("TITLE:", m.group(1).strip() if m else "?")
    # article body is the part before the related-article list; keep lines with numbers
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    txt = re.sub(r"<[^>]+>", "\n", txt)
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    for l in lines[:60]:
        if re.search(r"激光雷达|颗|万|%|补盲|主雷达|线", l):
            print("TXT:", l[:400])
    hashes = re.findall(r"img\.ne-time\.cn/([A-Za-z0-9]{40,})\.jpg\?[^\"' ]*?wx_fmt=(png|jpeg|jpg|gif)", html)
    seen = set()
    k = 0
    for h, fmt in hashes:
        if h in seen:
            continue
        seen.add(h)
        k += 1
        ok = False
        for prefix in ("sz_mmbiz_png", "sz_mmbiz_jpg", "mmbiz_png", "mmbiz_jpg"):
            url = f"https://mmbiz.qpic.cn/{prefix}/{h}/640?wx_fmt={fmt}"
            try:
                data = fetch(url, referer="https://mp.weixin.qq.com/")
            except Exception as e:  # noqa: BLE001
                continue
            if len(data) > 1000:
                ext = "png" if data[:4] == b"\x89PNG" else "jpg"
                fn = os.path.join(out_dir, f"netime_{aid}_img{k}.{ext}")
                with open(fn, "wb") as f:
                    f.write(data)
                print(f"IMG{k}: {prefix} {len(data)} bytes -> {fn}")
                ok = True
                try:
                    from PIL import Image
                    im = Image.open(fn)
                    W, H = im.size
                    print(f"   size {W}x{H}")
                    if H > 1300:
                        for i, y in enumerate(range(0, H, 1000)):
                            im.crop((0, y, W, min(H, y + 1000))).save(fn.replace(f".{ext}", f"_part{i}.png"))
                except Exception as e:  # noqa: BLE001
                    print("   PIL error", e)
                break
        if not ok:
            print(f"IMG{k}: not retrieved ({h[:20]}...)")


if __name__ == "__main__":
    main()
