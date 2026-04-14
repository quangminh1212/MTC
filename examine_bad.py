import os, re, sys

folder = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

# Files with issues to examine
bad_chapters = [215, 216, 238, 239, 250, 320, 327, 339, 376, 391]

for num in bad_chapters:
    # Find the file
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
    
    # Show raw hex around suspicious areas
    # Find positions with non-UTF8 or suspicious bytes
    # Show first 300 bytes as hex dump for analysis
    print(f"\nFirst 300 bytes hex:")
    for i in range(0, min(300, len(raw)), 32):
        hex_part = ' '.join(f'{b:02x}' for b in raw[i:i+32])
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in raw[i:i+32])
        print(f"  {i:4d}: {hex_part}")
        print(f"        {ascii_part}")
    
    # Try to identify the encoding
    # Check if it might be Latin-1 encoded Vietnamese (common mojibake)
    try:
        text_utf8 = raw.decode('utf-8')
        # Check if it looks right
        print(f"\nUTF-8 decode OK, first 200 chars:")
        print(f"  {text_utf8[:200]}")
    except UnicodeDecodeError as e:
        print(f"\nUTF-8 decode FAILED: {e}")
        # Try Latin-1
        text_latin1 = raw.decode('latin-1')
        print(f"Latin-1 first 200 chars:")
        print(f"  {text_latin1[:200]}")
        
        # Check if double-decoding helps
        try:
            fixed = raw.decode('latin-1').encode('latin-1').decode('utf-8')
            print(f"\nRe-encoded as UTF-8 first 200 chars:")
            print(f"  {fixed[:200]}")
        except:
            pass
    
    print()
