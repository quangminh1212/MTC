import os

dir_path = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"
uo_pats = ['\u00c6\u00b0', '\u00c6\u00a1']
dbl_pats = ['\u00c3\u00a1','\u00c3\u00a0','\u00c3\u00a3','\u00c3\u00a2','\u00c3\u00a9','\u00c3\u00a8','\u00c3\u00aa','\u00c3\u00ad','\u00c3\u00ac','\u00c3\u00b3','\u00c3\u00b2','\u00c3\u00b5','\u00c3\u00b4','\u00c3\u00ba','\u00c3\u00b9','\u00c3\u00bd']
c1_range = set(range(0x80, 0xa0))
ctrl_bad = set(range(0, 32)) - {9, 10, 13}

results = {}
for f in sorted(os.listdir(dir_path)):
    if not f.endswith('.txt'):
        continue
    fpath = os.path.join(dir_path, f)
    if not os.path.isfile(fpath):
        continue
    try:
        text = open(fpath, 'r', encoding='utf-8').read()
    except:
        continue

    issues = []
    if any(p in text for p in uo_pats):
        issues.append('UO')
    if any(p in text for p in dbl_pats):
        issues.append('DBL')
    if any(ord(c) in c1_range for c in text):
        issues.append('C1')
    if any(ord(c) in ctrl_bad for c in text):
        issues.append('CTRL')

    if issues:
        lines = text.split('\n')
        l2 = lines[1] if len(lines) > 1 else '<NO L2>'
        l5 = lines[4] if len(lines) > 4 else '<NO L5>'
        l6 = lines[5] if len(lines) > 5 else '<NO L6>'
        results[f] = (issues, l2, l5, l6)

for f in sorted(results):
    iss, l2, l5, l6 = results[f]
    tag = " ".join(iss)
    print(f"=== {f} [{tag}] ===")
    print(f"  L2: {repr(l2[:120])}")
    print(f"  L5: {repr(l5[:120])}")
    print(f"  L6: {repr(l6[:80])}")
    print()
