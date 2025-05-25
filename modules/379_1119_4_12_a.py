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
    "id _231119_4_12_a",
    "__input__ X Reset",
    "__output__ A_async A_not_async B_async B_not_async Y"
))

content = "\n".join(lines)
content += """
wire X
    path
        0   0   h   30
        10  0   v   e8  20
        10  30  h   20
        10  78  h   20
    colour
        800000  ff0000
    __signal__ true
wire Clock
    path
        88  100 v   -e0 18
        88  90  h   18
    colour
        808000  ffff00
wire Reset
    path
        0   120 h   e0
        d0  120 v   -f0 40
        d0  60  h   40
    colour
        804000  ff8000
    __signal__ true
wire Reset_not
    path
        f0  120 h   10  -130    18
        100 a0  h   18
    colour
        804000  ff8000
wire A
    path
        c0  0   h   58
    colour
        008000  00ff00
wire A_async
    path
        130 -8  h   40
        150 -8  v  -28 -138 f8   20
        18  -10 h   18
    colour
        008000  00ff00
wire A_not
    path
        c0  20  h   50
    colour
        008000  00ff00
wire A_not_async
    path
        130 28  h   40
        150 28  v   18  -128    28  8
    colour
        008000  00ff00
wire B
    path
        c0  70  h   50
    colour
        008080  00ffff
wire B_async
    path
        130 68  h   40
        150 68  v   -18 -130 -30 10
        20  50  v   68  18
    colour
        008080  00ffff
wire B_not
    path
        c0  90  h   58
    colour
        008080  00ffff
wire B_not_async
    path
        130 98  h   40
    colour
        008080  00ffff
wire X_and_A
    path
        50  -8  h   18
    colour
        808080  ffffff
wire X_and_B
    path
        50  28  h   8   -20 10
    colour
        808080  ffffff
wire X_and__A_or_B
    path
        80  0   h   20
    colour
        808080  ffffff
wire X_and_not_A
    path
        50  70  h   50
    colour
        808080  ffffff
wire A_or_B
    path
        50  c0  h   10
    colour
        808080  ffffff
wire X_not
    path
        40  e8  h   18  -18 8
    colour
        800000  ff0000
wire Y
    path
        80  c8  h   80
    colour
        800080  ff00ff

module timer_0
    module_id
        timer
    rect
        80  100 10  10
    colour
        ffff00  808000
    __input__
    __output__ Clock
module trigger_A
    module_id
        trigger_d
    rect
        a0  -10 20  40
    colour
        ffffff  808080
    __input__ Clock X_and__A_or_B
    __output__ A A_not
module trigger_B
    module_id
        trigger_d
    rect
        a0  60  20  40
    colour
        ffffff  808080
    __input__ Clock X_and_not_A
    __output__ B B_not

and zu_0
    rect
        30  8   20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ A_async
    __in1__ X
    __out__ X_and_A
and zu_1
    rect
        30  38  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ X
    __in1__ B_async
    __out__ X_and_B
and zu_2
    rect
        30  80  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ A_not_async
    __in1__ X
    __out__ X_and_not_A
and zu_3
    rect
        60  d8  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ A_or_B
    __in1__ X_not
    __out__ Y
or xo_0
    rect
        60  10  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ X_and_A
    __in1__ X_and_B
    __out__ X_and__A_or_B
or xo_1
    rect
        30  d0  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ A_async
    __in1__ B_async
    __out__ A_or_B
not fe_0
    rect
        30  f0  10  10
    orientation
        3
    colour
        ffffff  808080
    __in__ X
    __out__ X_not
and zu_4
    rect
        110 38  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ A_not
    __in1__ Reset
    __out__ A_not_async
and zu_5
    rect
        110 78  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ Reset
    __in1__ B
    __out__ B_async
or xo_2
    rect
        110 8   20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ Reset_not
    __in1__ A
    __out__ A_async
or xo_3
    rect
        110 a8  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ B_not
    __in1__ Reset_not
    __out__ B_not_async
not fe_1
    rect
        e0  128 10  10
    orientation
        3
    colour
        ffffff  808080
    __in__ Reset
    __out__ Reset_not
"""

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(os.path.join(os.path.dirname(__file__), "Interpret.py"))
