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
    "id _231119_4_12",
    "__input__ X",
    "__output__ A A_not B B_not Y"
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
wire Clock
    path
        88  100 v   -e0 18
        88  90  h   18
    colour
        808000  ffff00
wire A
    path
        c0  0   h   40
        e0  0   v  -30 -c8 f8   20
        18  -10 h   18
    colour
        008000  00ff00
wire A_not
    path
        c0  20  h   40
        e0  20  v   20  -b8 28  8
    colour
        008000  00ff00
wire B
    path
        c0  70  h   40
        e0  70  v   -20 -c0 -30 10
        20  50  v   68  18
    colour
        008080  00ffff
wire B_not
    path
        c0  90  h   40
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
    __in0__ A
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
    __in1__ B
    __out__ X_and_B
and zu_2
    rect
        30  80  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ A_not
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
    __in0__ A
    __in1__ B
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
"""

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(r"python D:\Sseu\Tryingssiuh\Ssianxmuh\_231025_DigitalLogic\web\modules\_231027_Interpret.py")
