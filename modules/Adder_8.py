#!/usr/bin/env python3
import os

def four_padded(numb: int):
    s = "{:x}".format(numb)
    return s.ljust((len(s) // 4 + 1) * 4, " ")

def contrast_colour(base: int, rgb_format: str, light_first: bool):
    d = max(min(base, 0x80), 0x0)
    dr = 0x80 - d
    l = min(d * 0x2, 0xff)
    lr = 0x100 - d * 0x2
    rgb_format = rgb_format.replace("0", "_").replace("1", "^")
    d_part = rgb_format.replace("_", "{:02x}".format(dr)).replace("^", "{:02x}".format(d))
    l_part = rgb_format.replace("_", "{:02x}".format(lr)).replace("^", "{:02x}".format(l))
    return ("{0:}  {1:}" if light_first else "{1:}  {0:}").format(l_part, d_part)

lines = []
configs = {}
lines.extend((
    "id adder_8",
    "__input__ A_0 A_1 A_2 A_3 A_4 A_5 A_6 A_7 B_0 B_1 B_2 B_3 B_4 B_5 B_6 B_7 CI",
    "__output__ S_0 S_1 S_2 S_3 S_4 S_5 S_6 S_7 CO",
    ""
))

for i in range(8):
    yb = (7 - i) * 0x80 + 0x70
    lines.extend((
        f"wire A_{i:1x}",
        "    path",
        f"        0   {four_padded(yb)}h   40",
        f"        20  {four_padded(yb)}v   -10",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '100', False)}",
        ""
    ))
    lines.extend((
        f"wire B_{i:1x}",
        "    path",
        f"        10  {four_padded(yb + 0x10)}h   30",
        f"        30  {four_padded(yb + 0x10)}v   -20",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '110', False)}",
        ""
    ))
    lines.extend((
        f"wire Y_{i:1x}",
        "    path",
        f"        60  {four_padded(yb + 0x8)}h   38",
        f"        70  {four_padded(yb + 0x8)}v   -10",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '010', False)}",
        ""
    ))
    lines.extend((
        f"wire C_{i:1x}_0",
        "    path",
        f"        28  {four_padded(yb - 0x30)}v   -8  40  -10",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '101', False)}",
        ""
    ))
    lines.extend((
        f"wire C_{i:1x}_1",
        "    path",
        f"        78  {four_padded(yb - 0x28)}v   -20",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '101', False)}",
        ""
    ))
    if i == 0:
        configs["CI"] = len(lines)
    lines.extend((
        f"wire C_{i - 1:1x}",
        "    path",
        f"        70  {four_padded(yb + 0x20)}v   -8  28",
        f"        80  {four_padded(yb + 0x18)}v   -20",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '101', False)}",
        ""
    ))
    lines.extend((
        f"wire S_{i:1x}",
        "    path",
        f"        b8  {four_padded(yb + 0x10)}h   10",
        "    colour",
        f"        {contrast_colour(0x80 - (3 - i) * 0x8, '010', False)}",
        ""
    ))

lines.extend((
    "wire C_7",
    "    path",
    "        70  10  v   -10",
    "    colour",
    f"        {contrast_colour(0x80, '101', False)}",
    ""
))

for i in range(8):
    yb = (7 - i) * 0x80 + 0x70
    lines.extend((
        f"xor zixo_{i:1x}_0",
        "    rect",
        f"        40  {four_padded(yb + 0x18)}20  20",
        "    orientation",
        "        3",
        "    colour",
        "        ffffff  808080",
        f"    __in0__ A_{i:1x}",
        f"    __in1__ B_{i:1x}",
        f"    __out__ Y_{i:1x}"
        ""
    ))
    lines.extend((
        f"xor zixo_{i:1x}_1",
        "    rect",
        f"        98  {four_padded(yb + 0x20)}20  20",
        "    orientation",
        "        3",
        "    colour",
        "        ffffff  808080",
        f"    __in0__ Y_{i:1x}",
        f"    __in1__ C_{i - 1:1x}",
        f"    __out__ S_{i:1x}"
        ""
    ))
    lines.extend((
        f"and zu_{i:1x}_0",
        "    rect",
        f"        38  {four_padded(yb - 0x10)}20  20",
        "    orientation",
        "        2",
        "    colour",
        "        ffffff  808080",
        f"    __in0__ A_{i:1x}",
        f"    __in1__ B_{i:1x}",
        f"    __out__ C_{i:1x}_0"
        ""
    ))
    lines.extend((
        f"and zu_{i:1x}_1",
        "    rect",
        f"        88  {four_padded(yb - 0x8)}20  20",
        "    orientation",
        "        2",
        "    colour",
        "        ffffff  808080",
        f"    __in0__ Y_{i:1x}",
        f"    __in1__ C_{i - 1:1x}",
        f"    __out__ C_{i:1x}_1"
        ""
    ))
    lines.extend((
        f"or xo_{i:1x}",
        "    rect",
        f"        80  {four_padded(yb - 0x40)}20  20",
        "    orientation",
        "        2",
        "    colour",
        "        ffffff  808080",
        f"    __in0__ C_{i:1x}_0",
        f"    __in1__ C_{i:1x}_1",
        f"    __out__ C_{i:1x}"
        ""
    ))

ci_path_0: str = lines[configs["CI"] + 2]
ci_path_0_start_y = int(ci_path_0.split()[1], 0x10)
ci_path_0_extend_y = int(ci_path_0.split()[3], 0x10)
lines[configs["CI"] + 2] = ci_path_0.replace(four_padded(ci_path_0_start_y), four_padded(ci_path_0_start_y + 0x10)).replace(four_padded(ci_path_0_extend_y), four_padded(ci_path_0_extend_y - 0x10))

content = "\n".join(lines)
content = content.replace("C_-1", "CI").replace("C_7", "CO")

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(os.path.join(os.path.dirname(__file__), "Interpret.py"))
