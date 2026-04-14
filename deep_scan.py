import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

folder = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

# Vietnamese chars set
VN_CHARS = set('ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ')
PUNCT_CHARS = set('–—…""''·×÷°±²³µ¹º¼½¾')

real_bad = [238, 250, 320, 339, 376, 391]

for num in real_bad:
    found = None
    for fn in os.listdir(folder):
        m = re.match(r'Chương (\d+)', fn)
        if m and int(m.group(1)) == num:
            found = fn
            break
    
    if not found:
        continue
    
    path = os.path.join(folder, found)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('\ufeff'):
        content = content[1:]
    
    print(f"=== Ch.{num}: {found} ===")
    
    # Find ALL non-Vietnamese non-ASCII characters
    issues = []
    lines = content.split('\n')
    for line_idx, line in enumerate(lines):
        line_clean = line.rstrip('\r')
        for col, ch in enumerate(line_clean):
            code = ord(ch)
            if code > 0x7F:
                if ch not in VN_CHARS and ch not in PUNCT_CHARS:
                    # Get context
                    ctx_start = max(0, col - 10)
                    ctx_end = min(len(line_clean), col + 10)
                    ctx = line_clean[ctx_start:ctx_end]
                    issues.append((line_idx + 1, col, code, ch, ctx))
    
    if issues:
        print(f"  Found {len(issues)} suspicious chars:")
        for ln, col, code, ch, ctx in issues:
            print(f"  L{ln} col{col}: U+{code:04X} ('{ch}') context: [{ctx}]")
    else:
        print("  No issues found")
    print()
