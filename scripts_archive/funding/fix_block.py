from pathlib import Path
p = Path(__file__).parent / "public_money_c3a.md"
t = p.read_text(encoding="utf-8")

old_x = ("Consortium shares: <br>– RETINA (101135529): FMCW lidar on an InP chip, beam-steered by a tilted grating-coupler array; "
         "XenomatiX supplies the ADAS collision-detection use case. €502,988. <br>– PhotoGeNIC (101069490): XenomatiX builds an automotive "
         "lidar demonstrator with germanium-substrate VCSELs. €424,063. <br>– ECSEL AutoDrive €226,787 and NewControl €299,955. "
         "<br>– KDT Cynergy4MIE €323,741 and DistriMuSe €530,119. <br>– European Defence Fund GENIUS and PRECISE; shares not found")
new_x = ("Consortium shares: RETINA (101135529; FMCW lidar on an InP chip, beam-steered by a tilted grating-coupler array; XenomatiX "
         "supplies the ADAS collision-detection use case) €502,988; PhotoGeNIC (101069490; XenomatiX builds an automotive lidar "
         "demonstrator with germanium-substrate VCSELs) €424,063; ECSEL AutoDrive €226,787 and NewControl €299,955; KDT Cynergy4MIE "
         "€323,741 and DistriMuSe €530,119; European Defence Fund GENIUS and PRECISE (shares not found)")
assert t.count(old_x) == 1
t = t.replace(old_x, new_x)
t = t.replace(" <br>– ", " ").replace(": <br>– ", ": ").replace(" <br>", " ").replace("<br>", " ")
assert "<br>" not in t
p.write_text(t, encoding="utf-8")

# checks
lines = t.split("\n")
cur = None
for i, l in enumerate(lines):
    if l.startswith("|"):
        n = l.count("|") - l.count("\\|")
        if cur is None:
            cur = n
        elif n != cur:
            print("MISMATCH", i + 1, n, cur, l[:80])
    else:
        cur = None
bad = [(i + 1, l[:60]) for i, l in enumerate(lines) for j, c in enumerate(l) if c == "$" and (j == 0 or l[j - 1] != "\\")]
print("unescaped $:", bad[:5])
print("double spaces:", sum(l.count("  ") for l in lines if l.startswith("|")))
print("ok", len(t))
