import os, re

d = r"C:\Dev\MTC\Công Cuộc Bị 999 Em Gái Chinh Phục"

problems = [
    'Chương 192 ta và ngươi có con....txt',
    'Chương 250 Vô tình thu mĩ hay là....txt',
    'Chương 316 Người con gái đó ở....txt',
    'Chương 333 Tỉnh lại và....txt',
    'Chương 344 Thành công hay...txt',
    'Chương 368 Dâm hoa gây chuyện...txt',
    'Chương 416 Cầm và Cầm giả .txt',
    'Chương 531 Ra khơi và... vào bụng cá..txt',
    'Chương 551 Qua hay là...txt',
    'Chương 614 Thua định Hay là.....txt',
    'Chương 770 Chế định kế hoạch xin lỗi .txt',
    'Chương 97 Phút nguy hiểm và đầy.....txt',
]

for f in problems:
    name = f[:-4]  # strip .txt
    # Remove trailing dots and spaces
    clean = name.rstrip('. ')
    newf = clean + '.txt'
    if newf != f:
        old = os.path.join(d, f)
        new = os.path.join(d, newf)
        if os.path.exists(old):
            if os.path.exists(new):
                print(f"CONFLICT: {f} -> {newf} (target exists!)")
            else:
                os.rename(old, new)
                print(f"RENAMED: {f} -> {newf}")
        else:
            print(f"NOT FOUND: {f}")
