import os, unicodedata

d = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"
files = [f for f in os.listdir(d) if f.endswith('.txt')]
problems = []

for f in sorted(files):
    issues = []
    name = f[:-4]
    # Control chars
    for i, ch in enumerate(f):
        c = ord(ch)
        if c < 0x20:
            issues.append(f"CTRL U+{c:04X} @{i}")
        elif c == 0x7F:
            issues.append(f"DEL @{i}")
        elif c > 0xFFFF:
            issues.append(f"HIGH U+{c:04X} @{i}")
    # Trailing dot/space
    if name.endswith(' ') or name.endswith('.'):
        issues.append("TRAILING")
    # Special chars
    for ch in '<>|?*':
        if ch in f:
            issues.append(f"SPECIAL({ch})")
    # NFC
    nfc = unicodedata.normalize('NFC', f)
    if nfc != f:
        issues.append("NOT_NFC")
    if issues:
        problems.append((f, issues))

print(f"Scanned {len(files)} files")
if problems:
    print(f"Found {len(problems)} problematic files:")
    for fname, iss in problems:
        print(f"  {repr(fname)}: {', '.join(iss)}")
else:
    print("No problematic filenames found. All filenames are git-safe.")
