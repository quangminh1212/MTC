import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

folder = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

# These had matches deep in file - need to verify if false positive
check_chapters = {
    215: 5213,
    216: 4246,
    238: 2751,
    239: 3765,
    327: 5517
}

for num, approx_pos in check_chapters.items():
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
    
    # Check around the approximate position for suspicious chars
    start = max(0, approx_pos - 50)
    end = min(len(content), approx_pos + 50)
    snippet = content[start:end]
    
    print(f"=== Ch.{num} around pos {approx_pos} ===")
    display = ''
    for ch in snippet:
        code = ord(ch)
        if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
            display += f'[U+{code:04X}]'
        elif ch == '\n':
            display += '\\n'
        elif ch == '\r':
            display += ''
        elif code > 0x7F:
            if ch in 'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ–—…""''·':
                display += ch
            else:
                display += f'[U+{code:04X}:{ch}]'
        else:
            display += ch
    print(f"  {display}")
    print()
