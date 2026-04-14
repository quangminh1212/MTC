import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

folder = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

bad_chapters = [215, 216, 238, 239, 250, 320, 327, 339, 376, 391]

for num in bad_chapters:
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
    
    lines = content.split('\n')
    
    print(f"=== Ch.{num} ===")
    # The chapter title is on line 2 (index 1)
    # The corrupted repeat is on line 4 (index 3) or wherever text starts
    # Show lines around the corruption
    for i, line in enumerate(lines[:10]):
        line_clean = line.rstrip('\r')
        # Show repr for non-standard chars
        has_unusual = False
        for ch in line_clean:
            code = ord(ch)
            if code > 0x7F and not (0xC0 <= code <= 0x024F or 0x0300 <= code <= 0x036F or 0x1E00 <= code <= 0x1EFF or code == 0x20AB):
                has_unusual = True
                break
        if has_unusual or i < 6:
            # Show with repr for unusual chars
            display = ''
            for ch in line_clean:
                code = ord(ch)
                if code < 0x20 and code not in (0x09,):
                    display += f'[U+{code:04X}]'
                elif code > 0x7F:
                    # Check if it's a valid Vietnamese char
                    if ch in 'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ–—…""''':
                        display += ch
                    else:
                        display += f'[U+{code:04X}:{ch}]'
                else:
                    display += ch
            print(f"  L{i+1}: {display[:150]}")
        else:
            print(f"  L{i+1}: {line_clean[:150]}")
    print()
