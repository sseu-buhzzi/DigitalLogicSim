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
        "id _231106_functional\n"
        "__input__ D_0 D_1 D_2 D_3 D_4 D_5 D_6 D_7 Addr_D_0 Addr_D_1 Addr_A_0 Addr_A_1 Addr_B_0 Addr_B_1 Write OpSel_ones OpSel_revr OpSel_cin DataSel\n"
        "__output__\n"
        "\n"
    )
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    for i in reversed(range(8)):
        i = 7 - i
        file.write(
            "wire DI_{0:1x}\n"
            "    path\n"
            "        138 {1:}h   {2:}30  {3:x}\n"
            "        {4:}{1:}v   30  {3:x}\n"
            "        {5:}{1:}v   30  {3:x}\n"
            "        {6:}{1:}v   30  {3:x}\n"
            "    colour\n"
            "        {7:}\n"
        .format(
            i,
            four_padded(0x6c - i * 0x4),
            four_padded(7 - i - 0xf8),
            0x10 + i - 7,
            four_padded((7 - i) + 0x80),
            four_padded((7 - i) + 0xc0),
            four_padded((7 - i) + 0x100),
            contrast_colour(i * 0x8 + 0x48, "100", False)
        ))
    file.write("\n")
    for i in range(2):
        file.write(
            "wire Addr_D_{0:1x}\n"
            "    path\n"
            "        0   {1:}h   10\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((2 - i) * 0x8),
            contrast_colour(i * 0x20 + 0x60, "101", False)
        ))
    file.write("\n")
    for i in range(4):
        file.write(
            "wire RegSel_{0:1x}\n"
            "    path\n"
            "        20  {1:}h   {2:}{3:x}\n"
            "    colour\n"
            "        {4:}\n"
        .format(
            i,
            four_padded(0x18 - i * 0x8),
            four_padded(0xf0 - i * 0x40),
            i * 0x8 + 0x10,
            contrast_colour(i * 0x10 + 0x50, "101", False)
        ))
    file.write(
        "\n"
        "wire Write\n"
        "    path\n"
        "        0   30  h   10\n"
        "    colour\n"
        "        804000  ff8000\n"
        "\n"
        "wire Clock\n"
        "    path\n"
        "        0   40  h   10\n"
        "    colour\n"
        "        804000  ff8000\n"
        "\n"
        "wire Write_sync\n"
        "    path\n"
        "        30  38  h   10  -18 e0 8\n"
        "        60  20  v   8\n"
        "        a0  20  v   8\n"
        "        e0  20  v   8\n"
        "    colour\n"
        "        804000  ff8000\n"
        "\n"
    )
    for i in range(4):
        file.write(
            "wire RegSel_W_{0:1x}\n"
            "    path\n"
            "        {1:}48  v   30\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded(0x118 - i * 0x40),
            contrast_colour(i * 0x10 + 0x50, "101", False)
        ))
    file.write("\n")
    for i in range(4):
        for j in range(8):
            file.write(
                "wire DO_{0:1x}_{1:1x}\n"
                "    path\n"
                "        {2:}{5:}h   {3:}{9}{8:x}\n"
                "        {6:}{7:}h   {8:x}\n"
                "    colour\n"
                "        {4:}\n"
            .format(
                i,
                j,
                four_padded((3 - i) * 0x40 + 0x60),
                four_padded(0x10 - j),
                contrast_colour(j * 0x8 + 0x58, "110", False),
                four_padded(0x9c - j * 0x4),
                four_padded((3 - i) * 0x40 + (7 - j) + 0x68),
                four_padded((3 - i) * 0x28 + (7 - j) * 0x4 + 0xc0),
                i * 0x40 + j + 0x8,
                four_padded((3 - i) * 0x28 + 0xf8)
            ))
    file.write("\n")
    for i in range(8):
        file.write(
            "wire A_{0:1x}\n"
            "    path\n"
            "        150 {1:}h   {3:}{4:}{5:x}\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((7 - i) * 0x4 + 0xc0),
            contrast_colour(0x80 - (7 - i) * 0x8, "010", False),
            four_padded(i * 0x4 + 0xa0),
            four_padded((7 - i) * 0x2c + 0xb8),
            (7 - i) * 0x4 + 0xc
        ))
    file.write("\n")
    for i in range(2):
        file.write(
            "wire Addr_A_{0:1x}\n"
            "    path\n"
            "        0   {1:}h   {2:}{3:x}\n"
            "    colour\n"
            "        {4:}\n"
        .format(
            i,
            four_padded(0xb0 - i * 0x8),
            four_padded(0x148 - i * 0x8),
            i * 0x8 + 0x8,
            contrast_colour(i * 0x20 + 0x60, "101", False)
        ))
    file.write("\n")
    for i in range(8):
        file.write(
            "wire B_{0:1x}\n"
            "    path\n"
            "        150 {1:}h   {3:}{4:}{5:x}\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((7 - i) * 0x4 + 0x178),
            contrast_colour(0x80 - (7 - i) * 0x8, "011", False),
            four_padded(i * 0x4 + 0x10),
            four_padded((7 - i) * 0x2c + 0x20),
            (7 - i) * 0x4 + 0x1c
        ))
    file.write("\n")
    for i in range(2):
        file.write(
            "wire Addr_B_{0:1x}\n"
            "    path\n"
            "        0   {1:}h   {2:}{3:x}\n"
            "    colour\n"
            "        {4:}\n"
        .format(
            i,
            four_padded(0x168 - i * 0x8),
            four_padded(0x148 - i * 0x8),
            i * 0x8 + 0x8,
            contrast_colour(i * 0x20 + 0x60, "101", False)
        ))
    file.write(
        "\n"
        "wire OpSel_ones\n"
        "    path\n"
        "        188 300 v   -178    10\n"
        "        188 1b8 h   10\n"
        "        188 1e8 h   10\n"
        "        188 218 h   10\n"
        "        188 248 h   10\n"
        "        188 278 h   10\n"
        "        188 2a8 h   10\n"
        "        188 2d8 h   10\n"
        "    colour\n"
        "        {0:}\n"
        "\n"
        "wire OpSel_revr\n"
        "    path\n"
        "        1b8 300 v   -180    10\n"
        "        1b8 1b0 h   10\n"
        "        1b8 1e0 h   10\n"
        "        1b8 210 h   10\n"
        "        1b8 240 h   10\n"
        "        1b8 270 h   10\n"
        "        1b8 2a0 h   10\n"
        "        1b8 2d0 h   10\n"
        "    colour\n"
        "        {0:}\n"
        "\n"
        "wire OpSel_cin\n"
        "    path\n"
        "        228 300 v -20\n"
        "    colour\n"
        "        {0:}\n"
        "\n"
        "wire DataSel\n"
        "    path\n"
        "        140 0   v   48\n"
        "    colour\n"
        "        {0:}\n"
        "\n"
    .format(
        contrast_colour(0x80, "101", False)
    ))
    for i in range(8):
        file.write(
            "wire B_OpSel_ones_{0:1x}\n"
            "    path\n"
            "        1b0 {1:}h   18\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((7 - i) * 0x30 + 0x190),
            contrast_colour(i * 0x8 + 0x48, "011", False)
        ))
    file.write("\n")
    for i in range(8):
        file.write(
            "wire B_OpSel_revr_{0:1x}\n"
            "    path\n"
            "        1e8 {1:}h   30\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((7 - i) * 0x30 + 0x188),
            contrast_colour(i * 0x8 + 0x48, "011", False)
        ))
    file.write("\n")
    for i in range(8):
        file.write(
            "wire F_{0:1x}\n"
            "    path\n"
            "        238 {1:}h   {3:}{4:}{5:x}\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((7 - i) * 0x30 + 0x178),
            contrast_colour(i * 0x8 + 0x48, "010", False),
            four_padded((7 - i) * 0x4 + 0x10),
            four_padded(-(7 - i) * 0x2c - 0x100),
            -(7 - i) * 0x4 - 0x100
        ))
    file.write("\n")
    for i in range(8):
        file.write(
            "wire D_{0:1x}\n"
            "    path\n"
            "        200 {1:}h   -b8\n"
            "    colour\n"
            "        {2:}\n"
        .format(
            i,
            four_padded((7 - i) * 0x4 + 0x50),
            contrast_colour(i * 0x8 + 0x48, "100", False)
        ))
    file.write("\n")
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    file.write(
        "\n\n\n"
        "module decoder_d\n"
        "    module_id\n"
        "        decoder_2_4\n"
        "    rect\n"
        "        10  -4  10  20\n"
        "    colour\n"
        "        ffffff  808080\n"
        "    __input__ Addr_D_0 Addr_D_1\n"
        "    __output__ RegSel_0 RegSel_1 RegSel_2 RegSel_3\n"
    )
    for i in range(4):
        file.write(
            "module reg_{0:1x}\n"
            "    module_id\n"
            "        reg_8\n"
            "    rect\n"
            "        {1:}78  10  28\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __input__ RegSel_W_{0:1x} DI_0 DI_1 DI_2 DI_3 DI_4 DI_5 DI_6 DI_7\n"
            "    __output__ DO_{0:1x}_0 DO_{0:1x}_1 DO_{0:1x}_2 DO_{0:1x}_3 DO_{0:1x}_4 DO_{0:1x}_5 DO_{0:1x}_6 DO_{0:1x}_7\n"
        .format(
            i,
            four_padded(0x110 - i * 0x40),
            contrast_colour(i * 0x10 + 0x50, "101", False)
        ))
    file.write("\n")
    for i in range(2):
        file.write(
            "module mux_{0:}\n"
            "    module_id\n"
            "        mux_4_8\n"
            "    rect\n"
            "        138 {2:}18  a0\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __input__ Addr_{1:}_0 Addr_{1:}_1 DO_0_0 DO_0_1 DO_0_2 DO_0_3 DO_0_4 DO_0_5 DO_0_6 DO_0_7 DO_1_0 DO_1_1 DO_1_2 DO_1_3 DO_1_4 DO_1_5 DO_1_6 DO_1_7 DO_2_0 DO_2_1 DO_2_2 DO_2_3 DO_2_4 DO_2_5 DO_2_6 DO_2_7 DO_3_0 DO_3_1 DO_3_2 DO_3_3 DO_3_4 DO_3_5 DO_3_6 DO_3_7\n"
            "    __output__ {1:}_0 {1:}_1 {1:}_2 {1:}_3 {1:}_4 {1:}_5 {1:}_6 {1:}_7\n"
        .format(
            ("a", "b")[i],
            ("A", "B")[i],
            four_padded(i * 0xb8 + 0xb8)
        ))
    file.write(
        "\n"
        "module adder\n"
        "    module_id\n"
        "        adder_8\n"
        "    rect\n"
        "        218 170 20  170\n"
        "    colour\n"
        "        ffffff  808080\n"
        "    __input__ A_0 A_1 A_2 A_3 A_4 A_5 A_6 A_7 B_OpSel_revr_0 B_OpSel_revr_1 B_OpSel_revr_2 B_OpSel_revr_3 B_OpSel_revr_4 B_OpSel_revr_5 B_OpSel_revr_6 B_OpSel_revr_7 OpSel_cin\n"
        "    __output__ F_0 F_1 F_2 F_3 F_4 F_5 F_6 F_7 null\n"
        "\n"
        "module mux_data\n"
        "    module_id\n"
        "        mux_2_8\n"
        "    rect\n"
        "        138 48 10  50\n"
        "    colour\n"
        "        ffffff  808080\n"
        "    __input__ DataSel D_0 D_1 D_2 D_3 D_4 D_5 D_6 D_7 F_0 F_1 F_2 F_3 F_4 F_5 F_6 F_7\n"
        "    __output__ DI_0 DI_1 DI_2 DI_3 DI_4 DI_5 DI_6 DI_7 null\n"
        "\n"
        "module timer_0\n"
        "    module_id\n"
        "        timer\n"
        "    rect\n"
        "        -10 38  10  10\n"
        "    colour\n"
        "        ffffff  808080\n"
        "    __input__\n"
        "    __output__ Clock\n"
        "\n"
    )
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    # ________________________________________________________________
    file.write("\n\n\n")
    for i in range(4):
        file.write(
            "and zu_regsel_{0:1x}\n"
            "    rect\n"
            "        {1:}28  20  20\n"
            "    orientation\n"
            "        0\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __in0__ RegSel_{0:1x}\n"
            "    __in1__ Write_sync\n"
            "    __out__ RegSel_W_{0:1x}\n"
        .format(
            i,
            four_padded(0x108 - i * 0x40),
            contrast_colour(i * 0x10 + 0x50, "101", False)
        ))
    for i in range(8):
        file.write(
            "or xo_OpSel_{0:1x}\n"
            "    rect\n"
            "        190 {1:}20  20\n"
            "    orientation\n"
            "        3\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __in0__ B_{0:1x}\n"
            "    __in1__ OpSel_ones\n"
            "    __out__ B_OpSel_ones_{0:1x}\n"
        .format(
            i,
            four_padded((7 - i) * 0x30 + 0x1a0),
            contrast_colour(i * 0x10 + 0x50, "101", False)
        ))
    for i in range(8):
        file.write(
            "xor zixo_OpSel_{0:1x}\n"
            "    rect\n"
            "        1c8 {1:}20  20\n"
            "    orientation\n"
            "        3\n"
            "    colour\n"
            "        ffffff  808080\n"
            "    __in0__ B_OpSel_ones_{0:1x}\n"
            "    __in1__ OpSel_revr\n"
            "    __out__ B_OpSel_revr_{0:1x}\n"
        .format(
            i,
            four_padded((7 - i) * 0x30 + 0x198),
            contrast_colour(i * 0x10 + 0x50, "101", False)
        ))
    file.write(
        "and zu_Write_sync\n"
        "    rect\n"
        "        10  48  20  20\n"
        "    orientation\n"
        "        3\n"
        "    colour\n"
        "        ffffff  808080\n"
        "    __in0__ Write\n"
        "    __in1__ Clock\n"
        "    __out__ Write_sync\n"
    )

with open(__file__[ : -2] + "dl", "r") as file:
    content = file.read()
lines = content.split("\n")



content = "\n".join(lines)
with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(os.path.join(os.path.dirname(__file__), "Interpret.py"))
