import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

folder = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

fixes_applied = 0

def find_file(num):
    for fn in os.listdir(folder):
        m = re.match(r'Chương (\d+)', fn)
        if m and int(m.group(1)) == num:
            return os.path.join(folder, fn)
    return None

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('\ufeff'):
        content = content[1:]
    return content

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Fix Ch.238: L41 "Thá»§" -> "Thủ"
path = find_file(238)
if path:
    content = read_file(path)
    old = 'Thá»§'
    new = 'Thủ'
    if old in content:
        content = content.replace(old, new)
        write_file(path, content)
        fixes_applied += 1
        print(f"Ch.238: Fixed '{old}' -> '{new}'")
    else:
        print(f"Ch.238: Pattern not found")

# Fix Ch.250: L5 corrupted title
path = find_file(250)
if path:
    content = read_file(path)
    lines = content.split('\n')
    # L2 has the correct title: "Chương 250: Vô tình thu mĩ hay là..."
    title_line = lines[1].rstrip('\r')  # "Chương 250: Vô tình thu mĩ hay là..."
    # Extract title after "Chương NNN: "
    m = re.match(r'Chương \d+:\s*(.*)', title_line)
    if m:
        correct_title = m.group(1)
    else:
        correct_title = title_line
    
    old_line5 = lines[4].rstrip('\r')
    print(f"Ch.250: L5 was: [{old_line5}]")
    print(f"Ch.250: L5 fix: [{correct_title}]")
    lines[4] = correct_title + ('\r' if lines[4].endswith('\r') else '')
    content = '\n'.join(lines)
    write_file(path, content)
    fixes_applied += 1

# Fix Ch.320: L5-L6 corrupted title (spans 2 lines, should be 1 line)
path = find_file(320)
if path:
    content = read_file(path)
    lines = content.split('\n')
    title_line = lines[1].rstrip('\r')
    m = re.match(r'Chương \d+:\s*(.*)', title_line)
    if m:
        correct_title = m.group(1)
    else:
        correct_title = title_line
    
    old_l5 = lines[4].rstrip('\r')
    old_l6 = lines[5].rstrip('\r')
    print(f"Ch.320: L5 was: [{repr(old_l5)}]")
    print(f"Ch.320: L6 was: [{repr(old_l6)}]")
    print(f"Ch.320: Fix: merge L5+L6 into [{correct_title}]")
    
    # Replace L5 with correct title, remove L6 (the continuation of corruption)
    has_cr = lines[4].endswith('\r')
    lines[4] = correct_title + ('\r' if has_cr else '')
    # L6 had the rest of corrupted title, remove it
    del lines[5]
    content = '\n'.join(lines)
    write_file(path, content)
    fixes_applied += 1

# Fix Ch.339: L5 corrupted title
path = find_file(339)
if path:
    content = read_file(path)
    lines = content.split('\n')
    title_line = lines[1].rstrip('\r')
    m = re.match(r'Chương \d+:\s*(.*)', title_line)
    if m:
        correct_title = m.group(1)
    else:
        correct_title = title_line
    
    old_line5 = lines[4].rstrip('\r')
    print(f"Ch.339: L5 was: [{old_line5}]")
    print(f"Ch.339: L5 fix: [{correct_title}]")
    lines[4] = correct_title + ('\r' if lines[4].endswith('\r') else '')
    content = '\n'.join(lines)
    write_file(path, content)
    fixes_applied += 1

# Fix Ch.376: L5 corrupted title
path = find_file(376)
if path:
    content = read_file(path)
    lines = content.split('\n')
    title_line = lines[1].rstrip('\r')
    m = re.match(r'Chương \d+:\s*(.*)', title_line)
    if m:
        correct_title = m.group(1)
    else:
        correct_title = title_line
    
    old_line5 = lines[4].rstrip('\r')
    print(f"Ch.376: L5 was: [{old_line5}]")
    print(f"Ch.376: L5 fix: [{correct_title}]")
    lines[4] = correct_title + ('\r' if lines[4].endswith('\r') else '')
    content = '\n'.join(lines)
    write_file(path, content)
    fixes_applied += 1

# Fix Ch.391: L5 corrupted title
path = find_file(391)
if path:
    content = read_file(path)
    lines = content.split('\n')
    title_line = lines[1].rstrip('\r')
    m = re.match(r'Chương \d+:\s*(.*)', title_line)
    if m:
        correct_title = m.group(1)
    else:
        correct_title = title_line
    
    old_line5 = lines[4].rstrip('\r')
    print(f"Ch.391: L5 was: [{repr(old_line5)}]")
    print(f"Ch.391: L5 fix: [{correct_title}]")
    lines[4] = correct_title + ('\r' if lines[4].endswith('\r') else '')
    content = '\n'.join(lines)
    write_file(path, content)
    fixes_applied += 1

print(f"\nTotal fixes applied: {fixes_applied}")
