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

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(
        "id mux_4_8\n"
        "__input__ S_0 S_1 I_0_0 I_0_1 I_0_2 I_0_3 I_0_4 I_0_5 I_0_6 I_0_7 I_1_0 I_1_1 I_1_2 I_1_3 I_1_4 I_1_5 I_1_6 I_1_7 I_2_0 I_2_1 I_2_2 I_2_3 I_2_4 I_2_5 I_2_6 I_2_7 I_3_0 I_3_1 I_3_2 I_3_3 I_3_4 I_3_5 I_3_6 I_3_7\n"
        "__output__ Y_0 Y_1 Y_2 Y_3 Y_4 Y_5 Y_6 Y_7\n"
        "\n"
    )
    for i in range(2):
        file.write(
            "wire S_{0:1x}\n"
            "    path\n"
            "        0   {1:}h   {3:}\n"
            "        10  {1:}v   10  10\n"
            "        {4:}\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((1 - i) * 0x20),
            contrast_colour(0x80 - (1 - i) * 0x10, "101", False),
            *(s.format(four_padded((1 - i) * 0x20)) for s in (
                ("b8  20", "58  {0:}v   20"),
                ("78  40", "48  {0:}v   40")
            )[i])
        ))
    file.write("\n")
    for i in range(2):
        file.write(
            "wire S_r_{0:1x}\n"
            "    path\n"
            "        30  {1:}h   {3:}\n"
            "        {4:}\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((1 - i) * 0x20 + 0x10),
            contrast_colour(0x80 - (1 - i) * 0x10, "101", False),
            *(s.format(four_padded((1 - i) * 0x20 + 0x10)) for s in (
                ("b8  10", "88  {0:}v   10"),
                ("a8  30", "a8  {0:}v   30")
            )[i])
        ))
    file.write("\n")
    for i in range(4):
        file.write(
            "wire Sel_{0:1x}\n"
            "    path\n"
            "        {1:}60  v   {3:}8\n"
            "        {1:}{4:}h   8\n"
            "        {1:}{5:}h   8\n"
            "        {1:}{6:}h   8\n"
            "        {1:}{7:}h   8\n"
            "        {1:}{8:}h   8\n"
            "        {1:}{9:}h   8\n"
            "        {1:}{10:}h   8\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((3 - i) * 0x30 + 0x50),
            contrast_colour(0x80 - (3 - i) * 0x10, "101", False),
            four_padded((3 - i) * 0x180 + 0x168),
            four_padded((3 - i) * 0x180 + 0x78),
            four_padded((3 - i) * 0x180 + 0xa8),
            four_padded((3 - i) * 0x180 + 0xd8),
            four_padded((3 - i) * 0x180 + 0x108),
            four_padded((3 - i) * 0x180 + 0x138),
            four_padded((3 - i) * 0x180 + 0x168),
            four_padded((3 - i) * 0x180 + 0x198)
        ))
    file.write("\n")
    for i in range(4):
        for j in range(8):
            file.write(
                "wire I_{0:1x}_{1:1x}\n"
                "    path\n"
                "        0   {2:}h   {4:x}\n"
                "    colour\n"
                "        {3:}\n"
            .format(
                i,
                j,
                four_padded((3 - i) * 0x180 + (7 - j) * 0x30 + 0x88),
                contrast_colour(0x80 - (7 - j) * 0x8, "100", False),
                (3 - i) * 0x30 + 0x58
            ))
    file.write("\n")
    for i in range(4):
        for j in range(8):
            file.write(
                "wire Y_{0:1x}_{1:1x}\n"
                "    path\n"
                "        {4:}{2:}h   {7:}{6:}{5:x}\n"
                "    colour\n"
                "        {3:}\n"
            .format(
                i,
                j,
                four_padded((3 - i) * 0x180 + (7 - j) * 0x30 + 0x80),
                contrast_colour(0x80 - (7 - j) * 0x8, "010", False),
                four_padded((3 - i) * 0x30 + 0x78),
                j * 0x4 - (3 - i) * 0x30 + 0xa4,
                four_padded((i - 3) * 0x178 - 0xc),
                four_padded((7 - j) * 0x4 + 0x10)
            ))
    for i in range(8):
        file.write(
            "wire Y_{0:1x}\n"
            "    path\n"
            "        160  {2:}h   10\n"
            "    colour\n"
            "        {3:}\n"
        .format(
            i,
            None,
            four_padded((7 - i) * 0x30 + 0x80),
            contrast_colour(0x80 - (7 - j) * 0x8, "010", False)
        ))
    file.write("\n\n\n")
    for i in range(2):
        file.write(
            "not fe_{0:1x}\n"
            "    rect\n"
            "        20  {1:}10  10\n"
            "    orientation\n"
            "        3\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __in__ S_{0:1x}\n"
            "    __out__ S_r_{0:1x}\n"
        .format(
            i,
            four_padded((1 - i) * 0x20 + 0x18)
        ))
    file.write("\n")
    for i in range(4):
        file.write(
            "and zu_{0:1x}\n"
            "    rect\n"
            "        {1:}40  20  20\n"
            "    orientation\n"
            "        0\n"
            "    colour\n"
            "         ffffff  808080\n"
            "    __in0__ S{2:}_0\n"
            "    __in1__ S{3:}_1\n"
            "    __out__ Sel_{0:1x}\n"
        .format(
            i,
            four_padded((3 - i) * 0x30  + 0x40),
            *(
                ("_r", "_r"),
                ("", "_r"),
                ("_r", ""),
                ("", "")
            )[i]
        ))
    file.write("\n")
    for i in range(4):
        for j in range(8):
            file.write(
                "and zu_{0:1x}_{1:1x}\n"
                "    rect\n"
                "        {2:}{3:}20  20\n"
                "    orientation\n"
                "        3\n"
                "    colour\n"
                "        ffffff  808080\n"
                "    __in0__ Sel_{0:1x}\n"
                "    __in1__ I_{0:1x}_{1:1x}\n"
                "    __out__ Y_{0:1x}_{1:1x}\n"
            .format(
                i,
                j,
                four_padded((3 - i) * 0x30 + 0x58),
                four_padded((3 - i) * 0x180 + (7 - j) * 0x30 + 0x90)
            ))
    file.write("\n")
    for i in range(8):
        file.write(
            "or_array xo_{0:1x}\n"
            "    rect\n"
            "        {1:}{2:}20  20\n"
            "    orientation\n"
            "        3\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __in_array__ Y_0_{0:1x} Y_1_{0:1x} Y_2_{0:1x} Y_3_{0:1x}\n"
            "    __out__ Y_{0:1x}\n"
        .format(
            i,
            four_padded(0x140),
            four_padded((7 - i) * 0x30 + 0x90)
        ))

os.system(os.path.join(os.path.dirname(__file__), "Interpret.py"))
