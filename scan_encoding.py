import os

dir_path = r'C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục'
issues = []

for fname in sorted(os.listdir(dir_path)):
    if not fname.endswith('.txt'):
        continue
    fpath = os.path.join(dir_path, fname)
    
    if not os.path.isfile(fpath):
        issues.append((fname, ['FILE_NOT_FOUND']))
        continue
    
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    file_issues = []
    
    if len(raw) == 0:
        file_issues.append('EMPTY')
    
    if b'\x00' in raw:
        file_issues.append('NULL_BYTES')
    
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        file_issues.append('NOT_UTF8')
        issues.append((fname, file_issues))
        continue
    
    if '\ufffd' in content:
        file_issues.append('REPLACEMENT_CHAR')
    
    # Mojibake: double-encoded Vietnamese UTF-8
    mojibake_2char = [
        '\u00c3\u00a1', '\u00c3\u00a0', '\u00c3\u00a3', '\u00c3\u00a2',
        '\u00c3\u00a9', '\u00c3\u00a8', '\u00c3\u00aa', '\u00c3\u00b3',
        '\u00c3\u00b2', '\u00c3\u00b5', '\u00c3\u00b4', '\u00c3\u00ad',
        '\u00c3\u00ac', '\u00c3\u00ba', '\u00c3\u00b9', '\u00c3\u00bd',
    ]
    for pat in mojibake_2char:
        if pat in content:
            file_issues.append('MOJIBAKE_DOUBLE_ENC')
            break
    
    if '\u00c4\u0091' in content or '\u00c4\u0090' in content:
        if 'MOJIBAKE_DOUBLE_ENC' not in file_issues:
            file_issues.append('MOJIBAKE_D')
    if '\u00c6\u00b0' in content or '\u00c6\u00a1' in content:
        if 'MOJIBAKE_DOUBLE_ENC' not in file_issues:
            file_issues.append('MOJIBAKE_UO')
    
    if '\u00e2\u0080' in content:
        file_issues.append('MOJIBAKE_QUOTES')
    
    for ch in content:
        cp = ord(ch)
        if cp < 32 and cp not in (9, 10, 13):
            file_issues.append('CONTROL_CHAR_U+{:04X}'.format(cp))
            break
        if 0x80 <= cp <= 0x9F and cp != 0x85:
            file_issues.append('C1_CTRL_U+{:04X}'.format(cp))
            break
    
    if file_issues:
        issues.append((fname, file_issues))

total = len([f for f in os.listdir(dir_path) if f.endswith('.txt')])
print('Scanned {} files'.format(total))
print('Files with issues: {}'.format(len(issues)))
for fname, fi in issues:
    print('  [{}] {}'.format(' | '.join(fi), fname))
