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
        "id mux_2_8\n"
        "__input__ S_0 I_0_0 I_0_1 I_0_2 I_0_3 I_0_4 I_0_5 I_0_6 I_0_7 I_1_0 I_1_1 I_1_2 I_1_3 I_1_4 I_1_5 I_1_6 I_1_7\n"
        "__output__ Y_0 Y_1 Y_2 Y_3 Y_4 Y_5 Y_6 Y_7\n"
        "\n"
    )
    for i in range(1):
        file.write(
            "wire S_{0:1x}\n"
            "    path\n"
            "        0   {1:}h   40  180 8\n"
            "        10  {1:}v   10  10\n"
            "        40  30  h   8\n"
            "        40  60  h   8\n"
            "        40  90  h   8\n"
            "        40  c0  h   8\n"
            "        40  f0  h   8\n"
            "        40  120 h   8\n"
            "        40  150 h   8\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded(i * 0x20),
            contrast_colour(0x80 - i * 0x10, "101", False),
        ))
    file.write("\n")
    for i in range(1):
        file.write(
            "wire S_r_{0:1x}\n"
            "    path\n"
            "        30  {1:}h   40  2f0 8\n"
            "        70  1b0 h   8\n"
            "        70  1e0 h   8\n"
            "        70  210 h   8\n"
            "        70  240 h   8\n"
            "        70  270 h   8\n"
            "        70  2a0 h   8\n"
            "        70  2d0 h   8\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded(i * 0x20 + 0x10),
            contrast_colour(0x80 - i * 0x10, "101", False)
        ))
    file.write("\n")
    for i in range(2):
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
                four_padded((1 - i) * 0x180 + (7 - j) * 0x30 + 0x40),
                contrast_colour(0x80 - (7 - j) * 0x8, "100", False),
                (1 - i) * 0x30 + 0x48
            ))
    file.write("\n")
    for i in range(2):
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
                four_padded((1 - i) * 0x180 + (7 - j) * 0x30 + 0x38),
                contrast_colour(0x80 - (7 - j) * 0x8, "010", False),
                four_padded((1 - i) * 0x30 + 0x68),
                j * 0x4 - (1 - i) * 0x30 + 0x44,
                four_padded((i - 1) * 0x170 - 0x8),
                four_padded((7 - j) * 0x4 + 0x10)
            ))
    for i in range(8):
        file.write(
            "wire Y_{0:1x}\n"
            "    path\n"
            "        f0  {2:}h   10\n"
            "    colour\n"
            "        {3:}\n"
        .format(
            i,
            None,
            four_padded((7 - i) * 0x30 + 0x38),
            contrast_colour(0x80 - (7 - j) * 0x8, "010", False)
        ))
    file.write("\n\n\n")
    for i in range(1):
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
            four_padded(i * 0x20 + 0x18)
        ))
    file.write("\n")
    for i in range(2):
        for j in range(8):
            file.write(
                "and zu_{0:1x}_{1:1x}\n"
                "    rect\n"
                "        {2:}{3:}20  20\n"
                "    orientation\n"
                "        3\n"
                "    colour\n"
                "        ffffff  808080\n"
                "    __in0__ {4:}\n"
                "    __in1__ I_{0:1x}_{1:1x}\n"
                "    __out__ Y_{0:1x}_{1:1x}\n"
            .format(
                i,
                j,
                four_padded((1 - i) * 0x30 + 0x48),
                four_padded((1 - i) * 0x180 + (7 - j) * 0x30 + 0x48),
                "S_0" if i else "S_r_0"
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
            "    __in_array__ Y_0_{0:1x} Y_1_{0:1x}\n"
            "    __out__ Y_{0:1x}\n"
        .format(
            i,
            four_padded(0xd0),
            four_padded((7 - i) * 0x30 + 0x48)
        ))

os.system(r"python D:\Sseu\Tryingssiuh\Ssianxmuh\_231025_DigitalLogic\web\modules\_231027_Interpret.py")
