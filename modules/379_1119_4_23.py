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
lines.extend(())

content = "\n".join(lines)
content += """id _231119_4_23
__input__ X
__output__ Y

wire X
    path
        0   0   h   20
    colour
        800000  ff0000
wire X_not
    path
        20  0   h   10
    colour
        800000  ff0000
wire Clock
    path
        0   28  h   60
    colour
        808000  ffff00
wire F
    path
        80  0   h   20
        90  0   v   40  -70 -30 10
    colour
        008000  00ff00
wire Y
    path
        50  8   h   10
    colour
        008000  00ff00

module timer_0
    module_id
        timer
    rect
        -10 20  10  10
    colour
        ffff00  808000
    __input__
    __output__ Clock
module trigger_0
    module_id
        trigger_d
    rect
        60  -8  20  40
    colour
        ffffff  808080
    __input__ Clock Y
    __output__ F null

not fe_0
    rect
        10  8   10  10
    orientation
        3
    colour
        ffffff  808080
    __in__ X
    __out__ X_not
xor zixo_0
    rect
        30  18  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ X_not
    __in1__ F
    __out__ Y
"""

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(os.path.join(os.path.dirname(__file__), "Interpret.py"))
