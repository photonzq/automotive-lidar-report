# Helper: strip HTML to text and print context windows around keywords.
# Usage: python extract_text.py file.html kw1 [kw2 ...] [--win N] [--all]
import re, html, sys
args = sys.argv[1:]
win = 500
if '--win' in args:
    i = args.index('--win'); win = int(args[i+1]); del args[i:i+2]
show_all = False
if '--all' in args:
    args.remove('--all'); show_all = True
fn, kws = args[0], args[1:]
s = open(fn, encoding='utf-8', errors='ignore').read()
t = re.sub(r'<script.*?</script>', ' ', s, flags=re.S | re.I)
t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S | re.I)
t = re.sub(r'<br\s*/?>', ' ', t, flags=re.I)
t = re.sub(r'<[^>]+>', ' ', t)
t = html.unescape(re.sub(r'\s+', ' ', t))
out = t.encode('ascii', 'replace').decode()
if show_all:
    print(out[:60000])
else:
    seen = []
    for k in kws:
        for m in re.finditer(re.escape(k), out, flags=re.I):
            a = max(0, m.start() - win); b = m.start() + win
            if any(abs(a - x) < win for x in seen):
                continue
            seen.append(a)
            print('[' + k + '] ...' + out[a:b] + '...')
            print('-----')
