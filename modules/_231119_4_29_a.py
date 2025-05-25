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
__input__
__output__ Q_2

wire X
    path
        30  58  h   -30 -48 20
    colour
        800000  ff0000
wire Clock
    path
        0   -10 h   98  40  10
        18  -10 v   40  10
        58  -10 v   40  10
    colour
        808000  ffff00
wire Q_0
    path
        40  10  h   20
    colour
        008000  00ff00
wire Q_1
    path
        80  10  h   20
    colour
        008000  00ff00
wire Q_2
    path
        c0  10  h   20
        c8  10  v   48  -88
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
        60  0   20  40
    colour
        ffffff  808080
    __input__ Clock Q_0
    __output__ Q_1 null
module trigger_2
    module_id
        trigger_d
    rect
        a0  0   20  40
    colour
        ffffff  808080
    __input__ Clock Q_1
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
"""

with open(__file__[ : -2] + "dl", "w") as file:
    file.write(content)

os.system(r"python D:\Sseu\Tryingssiuh\Ssianxmuh\_231025_DigitalLogic\web\modules\_231027_Interpret.py")
