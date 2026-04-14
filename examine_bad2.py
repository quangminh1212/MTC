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
        print(f"Ch.{num}: FILE NOT FOUND")
        continue
    
    path = os.path.join(folder, found)
    with open(path, 'rb') as f:
        raw = f.read()
    
    print(f"\n{'='*60}")
    print(f"Ch.{num}: {found}")
    print(f"File size: {len(raw)} bytes")
    
    # Show hex of first 200 bytes
    print(f"First 200 bytes hex:")
    for i in range(0, min(200, len(raw)), 32):
        hex_part = ' '.join(f'{b:02x}' for b in raw[i:i+32])
        print(f"  {i:4d}: {hex_part}")
    
    # Find all positions with suspicious bytes (non-standard)
    # Scan for bytes that form invalid or unusual UTF-8
    suspicious = []
    i = 0
    while i < len(raw):
        b = raw[i]
        if b < 0x80:
            i += 1
            continue
        # Multi-byte UTF-8
        if b >= 0xC0 and b < 0xE0:
            if i+1 < len(raw) and (raw[i+1] & 0xC0) == 0x80:
                codepoint = ((b & 0x1F) << 6) | (raw[i+1] & 0x3F)
                if codepoint < 0x80:  # overlong
                    suspicious.append((i, raw[i:i+2], f"overlong U+{codepoint:04X}"))
                elif 0x80 <= codepoint <= 0x9F:  # C1 controls
                    suspicious.append((i, raw[i:i+2], f"C1 control U+{codepoint:04X}"))
                i += 2
            else:
                suspicious.append((i, raw[i:i+1], f"invalid continuation"))
                i += 1
        elif b >= 0xE0 and b < 0xF0:
            if i+2 < len(raw) and (raw[i+1] & 0xC0) == 0x80 and (raw[i+2] & 0xC0) == 0x80:
                codepoint = ((b & 0x0F) << 12) | ((raw[i+1] & 0x3F) << 6) | (raw[i+2] & 0x3F)
                # Check for unusual Unicode blocks  
                if 0x0500 <= codepoint <= 0x06FF:  # Armenian, Arabic
                    suspicious.append((i, raw[i:i+3], f"unusual U+{codepoint:04X}"))
                i += 3
            else:
                suspicious.append((i, raw[i:i+1], f"invalid 3-byte"))
                i += 1
        elif b >= 0xF0:
            if i+3 < len(raw) and all((raw[i+j] & 0xC0) == 0x80 for j in range(1,4)):
                i += 4
            else:
                suspicious.append((i, raw[i:i+1], f"invalid 4-byte"))
                i += 1
        elif (b & 0xC0) == 0x80:
            # Continuation byte without start
            suspicious.append((i, raw[i:i+1], f"orphan continuation 0x{b:02X}"))
            i += 1
        else:
            suspicious.append((i, raw[i:i+1], f"invalid byte 0x{b:02X}"))
            i += 1
    
    if suspicious:
        print(f"Suspicious bytes ({len(suspicious)} found):")
        for pos, bts, desc in suspicious[:20]:
            ctx_start = max(0, pos-5)
            ctx_end = min(len(raw), pos+10)
            ctx_hex = ' '.join(f'{b:02x}' for b in raw[ctx_start:ctx_end])
            print(f"  pos {pos}: {desc} | context hex: {ctx_hex}")
    else:
        print("No suspicious bytes (valid UTF-8)")
    
    # Try decode as UTF-8 and show first line
    try:
        content = raw.decode('utf-8')
        if content.startswith('\ufeff'):
            content = content[1:]
        lines = content.split('\n')
        print(f"First line: {lines[0][:100]}")
        if len(lines) > 3:
            print(f"Line 4: {lines[3][:100]}")
    except:
        print("Cannot decode as UTF-8")
    
    print()
