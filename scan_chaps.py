import os, re, sys

folder = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"
files = []
for fn in os.listdir(folder):
    if fn.endswith('.txt'):
        m = re.match(r'Chương (\d+)', fn)
        if m:
            num = int(m.group(1))
            if 201 <= num <= 400:
                files.append((num, fn))

files.sort()
print(f"Total files in range 201-400: {len(files)}")

bad_files = []
for num, fn in files:
    path = os.path.join(folder, fn)
    try:
        with open(path, 'rb') as f:
            raw = f.read()
        
        # Try to decode as UTF-8
        try:
            content = raw.decode('utf-8')
        except UnicodeDecodeError as e:
            bad_files.append((num, fn, f"UTF-8 decode error: {e}"))
            continue
        
        # Strip BOM
        if content.startswith('\ufeff'):
            content = content[1:]
        
        issues = []
        
        # Check for control characters (except \r \n \t)
        for i, ch in enumerate(content):
            code = ord(ch)
            if code < 0x20 and code not in (0x09, 0x0A, 0x0D):
                issues.append(f"control char U+{code:04X} at pos {i}")
                break
        
        # Check for characters in U+0080-U+009F range (C1 controls, shouldn't appear)
        for i, ch in enumerate(content):
            code = ord(ch)
            if 0x80 <= code <= 0x9F:
                snippet = content[max(0,i-15):i+15].replace('\n','\\n')
                issues.append(f"C1 control U+{code:04X} at pos {i}: [{snippet}]")
                break
        
        # Check for mojibake patterns typical of double-encoding
        mojibake_patterns = [
            (r'Ã[\u0080-\u00BF]', 'double-encoded UTF-8'),
            (r'Ä[\u0082\u0083\u0090\u0091\u00A8\u00A9]', 'possible double-encoded Vietnamese'),
            (r'Æ°', 'double-encoded ư'),
            (r'á»[\u0080-\u00BF]', 'double-encoded Vietnamese'),
        ]
        for pat, desc in mojibake_patterns:
            m2 = re.search(pat, content)
            if m2:
                pos = m2.start()
                snippet = content[max(0,pos-10):pos+20].replace('\n','\\n')
                issues.append(f"{desc} at pos {pos}: [{snippet}]")
        
        # Check for unusual characters that indicate corruption
        # Characters like Ü Ý (when not part of Vietnamese), Þ ß ð ñ ÿ etc.
        # Vietnamese uses: Ý ý but in specific contexts
        corruption_chars = []
        for i, ch in enumerate(content):
            code = ord(ch)
            # Chars that are suspicious in Vietnamese text
            if ch in 'ÜÞßðñÿþ':
                ctx = content[max(0,i-10):i+10].replace('\n','\\n')
                corruption_chars.append(f"U+{code:04X}('{ch}') at pos {i}: [{ctx}]")
            # Check for non-BMP or unusual blocks
            if 0x0600 <= code <= 0x06FF:  # Arabic block
                ctx = content[max(0,i-10):i+10].replace('\n','\\n')
                corruption_chars.append(f"Arabic U+{code:04X} at pos {i}: [{ctx}]")
            if 0x0500 <= code <= 0x058F:  # Armenian
                ctx = content[max(0,i-10):i+10].replace('\n','\\n')
                corruption_chars.append(f"Armenian U+{code:04X} at pos {i}: [{ctx}]")
            if 0xFB00 <= code <= 0xFDFF:  # Alphabetic presentation
                ctx = content[max(0,i-10):i+10].replace('\n','\\n')
                corruption_chars.append(f"Presentation U+{code:04X} at pos {i}: [{ctx}]")
            if 0x0300 <= code <= 0x036F and i > 0:
                # Combining diacritical - check if previous char is ASCII
                prev = ord(content[i-1])
                if prev < 0x41 or (prev > 0x5A and prev < 0x61) or prev > 0x7A:
                    pass  # might be ok
        
        if corruption_chars:
            issues.extend(corruption_chars[:3])  # limit output
        
        # Check first line specifically - chapter titles often get corrupted
        first_line = content.split('\n')[0] if content else ''
        if re.search(r'[Z]{1}[^a-zA-Z\s]|ýNg|ChưýNg', first_line):
            issues.append(f"Corrupted chapter title: [{first_line[:80]}]")
        
        if issues:
            bad_files.append((num, fn, "; ".join(issues[:5])))
            
    except Exception as e:
        bad_files.append((num, fn, f"ERROR: {e}"))

if bad_files:
    print(f"\nFiles with issues ({len(bad_files)}):")
    for num, fn, issue in bad_files:
        print(f"  Ch.{num}: {issue}")
        print(f"    File: {fn}")
else:
    print("\nNo issues found in any file.")
