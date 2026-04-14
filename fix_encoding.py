#!/usr/bin/env python3
"""Fix encoding issues (garbled prefix + mojibake) in chapter files."""
import os
import re

DIR = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

# All Vietnamese diacritical characters (67 lowercase + 67 uppercase)
VIET_STR = ("àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"
            "ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ")
VIET = set(VIET_STR)
SAFE_PUNCT = set(".,!?;:-'\"()[]{}…–—\u201c\u201d\u2018\u2019\u00b0")


def build_mojibake_table():
    """Build mapping: mojibake string -> correct Vietnamese char."""
    table = {}
    for c in VIET_STR:
        try:
            moji = c.encode('utf-8').decode('latin-1')
            table[moji] = c
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
    return sorted(table.items(), key=lambda x: len(x[0]), reverse=True)


MOJI_TABLE = build_mojibake_table()


def fix_mojibake(text):
    """Replace all Vietnamese mojibake sequences with correct characters."""
    for moji, correct in MOJI_TABLE:
        text = text.replace(moji, correct)
    return text


def is_text_char(c):
    """Is this character expected in normal Vietnamese prose?"""
    if c in VIET:
        return True
    if c.isascii() and (c.isalnum() or c.isspace()):
        return True
    if c in SAFE_PUNCT:
        return True
    return False


def has_encoding_issues(line):
    """Check if a line has encoding issues."""
    s = line.strip()
    if not s:
        return False
    # Mojibake sequences
    for moji, _ in MOJI_TABLE:
        if moji in s:
            return True
    # C1 control characters (0x80-0x9F)
    if any(0x80 <= ord(c) <= 0x9F for c in s):
        return True
    # Low control characters (except \n \r \t)
    if any(ord(c) < 0x20 and c not in '\n\r\t' for c in s):
        return True
    # Non-Vietnamese non-ASCII garbled chars (>= 2)
    garbled = sum(1 for c in s if not is_text_char(c))
    if garbled >= 2:
        return True
    return False


def find_content_start(line):
    """
    Find where readable Vietnamese text starts after a garbled prefix.
    Returns (mojibake_fixed_line, start_index) or (mojibake_fixed_line, None).
    """
    fixed = fix_mojibake(line)

    # Find the rightmost non-text character (= end of garbled prefix)
    last_garbled = -1
    for i, c in enumerate(fixed):
        if not is_text_char(c):
            last_garbled = i

    if last_garbled == -1:
        return fixed, 0  # Line is fully clean after mojibake fix

    # Scan forward from last_garbled+1 to find proper word start
    pos = last_garbled + 1
    while pos < len(fixed) - 2:
        c = fixed[pos]
        if c.isdigit():
            break  # Numbers can start content
        if c in VIET or (c.isascii() and c.isalpha()):
            nxt = fixed[pos + 1] if pos + 1 < len(fixed) else ''
            if nxt.isalpha() or nxt in VIET or nxt.isspace():
                break  # Proper word start (letter followed by letter/space)
        pos += 1

    if pos >= len(fixed) - 5:
        return fixed, None  # Not enough content remaining

    return fixed, pos


def main():
    fixed_count = 0
    log = []

    for fname in sorted(os.listdir(DIR)):
        if not fname.endswith('.txt'):
            continue
        fpath = os.path.join(DIR, fname)
        if not os.path.isfile(fpath):
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Detect and normalize line endings
        has_crlf = '\r\n' in content
        content = content.replace('\r\n', '\n')
        lines = content.split('\n')

        if len(lines) < 5:
            continue

        l5 = lines[4]
        l6 = lines[5] if len(lines) > 5 else ""

        if not has_encoding_issues(l5) and not has_encoding_issues(l6):
            continue

        # === File needs fixing ===
        l2 = lines[1]
        title_match = re.match(r'Chương\s+\d+:\s*(.+)', l2)
        has_title = bool(title_match and title_match.group(1).strip())

        if has_title:
            # Pattern A: garbled title duplicate — delete garbled line(s)
            deleted = 0
            while (deleted < 3 and len(lines) > 4 and
                   lines[4].strip() and has_encoding_issues(lines[4])):
                lines.pop(4)
                deleted += 1
            log.append(f"[A] {fname}: deleted {deleted} garbled title line(s)")

        else:
            # No title — Pattern B (prefix+content) or C (pure garbage)
            if has_encoding_issues(l5):
                fixed_line, start = find_content_start(l5)
                if start is not None:
                    cleaned = fixed_line[start:]
                    lines[4] = cleaned
                    preview = cleaned[:50].replace('\n', ' ')
                    log.append(f"[B] {fname}: strip {start} chars -> '{preview}...'")
                else:
                    lines.pop(4)
                    log.append(f"[C] {fname}: deleted pure garbage L5")
            elif has_encoding_issues(l6):
                fixed_line, start = find_content_start(l6)
                if start is not None:
                    lines[5] = fixed_line[start:]
                    log.append(f"[B*] {fname}: fixed L6")
                else:
                    lines.pop(5)
                    log.append(f"[C*] {fname}: deleted garbage L6")

        # Write back with original line ending style
        result = '\n'.join(lines)
        if has_crlf:
            result = result.replace('\n', '\r\n')
        with open(fpath, 'w', encoding='utf-8', newline='') as f:
            f.write(result)

        fixed_count += 1

    print(f"\nFixed {fixed_count} files:\n")
    for entry in log:
        print(f"  {entry}")


if __name__ == '__main__':
    main()
