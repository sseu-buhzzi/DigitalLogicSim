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
content += """id _231119_4_29_a
__input__ Reset
__output__ Q_2

wire X
    path
        30  58  h   -30 -48 20
    colour
        800000  ff0000
wire Reset
    path
        0   -20 h   20
    colour
        804000  ff8000
wire Reset_not
    path
        30  -20 h   120 20  10
        50  -20 v   20  10
        d0  -20 v   20  10
    colour
        804000  ff8000
wire Clock
    path
        0   -10 h   118 40  10
        18  -10 v   40  10
        98  -10 v   40  10
    colour
        808000  ffff00
wire D_0
    path
        80  8   h   10  8   10
    colour
        008000  00ff00
wire D_1
    path
        100 8   h   10  8   10
    colour
        008000  00ff00
wire D_2
    path
        180 8   h   10  50  -150
        190 10  h   10
    colour
        008000  00ff00
wire Q_0
    path
        40  10  h   20
    colour
        008000  00ff00
wire Q_1
    path
        c0  10  h   20
    colour
        008000  00ff00
wire Q_2
    path
        140 10  h   20
    colour
        008000  00ff00

module timer_0
    module_id
        timer
    rect
        -10 -18 10  10
    colour
        ffff00  808000
    __input__
    __output__ Clock
module trigger_0
    module_id
        trigger_d
    rect
        20  0   20  40
    colour
        ffffff  808080
    __input__ Clock X
    __output__ Q_0 null
module trigger_1
    module_id
        trigger_d
    rect
        a0  0   20  40
    colour
        ffffff  808080
    __input__ Clock D_0
    __output__ Q_1 null
module trigger_2
    module_id
        trigger_d
    rect
        120 0   20  40
    colour
        ffffff  808080
    __input__ Clock D_1
    __output__ Q_2 null

not fe_0
    rect
        40  50  10  10
    orientation
        1
    colour
        ffffff  808080
    __in__ Q_2
    __out__ X
not fe_1
    rect
        20  -18 10  10
    orientation
        3
    colour
        ffffff  808080
    __in__ Reset
    __out__ Reset_not
and zu_0
    rect
        60  18  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ Reset_not
    __in1__ Q_0
    __out__ D_0
and zu_1
    rect
        e0  18  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ Reset_not
    __in1__ Q_1
    __out__ D_1
and zu_2
    rect
        160 18  20  20
    orientation
        3
    colour
        ffffff  808080
    __in0__ Reset_not
    __in1__ Q_2
    __out__ D_2
"""

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(r"python D:\Sseu\Tryingssiuh\Ssianxmuh\_231025_DigitalLogic\web\modules\_231027_Interpret.py")
