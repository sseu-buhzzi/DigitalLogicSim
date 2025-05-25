import json
import os
import sys

def dl_compile(file_path):
    with open(file_path, "r") as file:
        lines = ["endmodule"] + [line for line in file.read().split("\n")[ : : -1] if line and not line.startswith("//")]

    module_json = {"id": None, "content": {}}
    indent_stack = []
    try:
        while True:
            line = lines.pop()
            parts = line.split()
            indent_stack.append(line.find(parts[0]))
            if len(indent_stack) != 1 and indent_stack[-1] == indent_stack[-2]:
                indent_stack.pop()
            if parts[0] == "id":
                module_json["id"] = parts[1]
            elif parts[0] in ("__input__", "__output__"):
                module_json[parts[0]] = parts[1 : ]
            elif parts[0] == "endmodule":
                break
            else:
                element_id = parts[1]
                element = {}
                if parts[0] == "wire":
                    element["__signal__"] = False
                elif parts[0] == "module":
                    element["__input__"] = None
                    element["__output__"] = None
                elif parts[0] in ("buffer", "not"):
                    element["__in__"] = None
                    element["__out__"] = None
                elif parts[0].endswith("_array"):
                    element["__in_array__"] = None
                    element["__out__"] = None
                else:
                    element["__in0__"] = None
                    element["__in1__"] = None
                    element["__out__"] = None
                element["type"] = parts[0]
                while True:
                    line = lines.pop()
                    parts = line.split()
                    indent_stack.append(line.find(parts[0]))
                    if indent_stack[-1] == indent_stack[-2]:
                        indent_stack.pop()
                    elif indent_stack[-1] < indent_stack[-2]:
                        indent_stack.pop()
                        indent_stack.pop()
                        lines.append(line)
                        break
                    if parts[0] == "__volitale__":
                        element["__volitale__"] = parts[1].lower() in ("1", "true")
                    elif parts[0] == "__delay__":
                        element["__delay__"] = int(parts[1], 16)
                    elif parts[0] in ("__signal__", "__in__", "__in0__", "__in1__", "__out__"):
                        element[parts[0]] = parts[1]
                    elif parts[0].endswith("_array__"):
                        element[parts[0]] = parts[1 : ]
                    elif parts[0] == "__input__":
                        element["__input__"] = [True if wire.lower() in ("1", "true") else False if wire.lower() in ("0", "false") else wire for wire in parts[1 : ]]
                    elif parts[0] == "__output__":
                        element["__output__"] = [None if wire.lower() in ("*", "null") else wire for wire in parts[1 : ]]
                    elif parts[0] == "path":
                        element["path"] = []
                        while True:
                            line = lines.pop()
                            parts = line.split()
                            indent_stack.append(line.find(parts[0]))
                            if indent_stack[-1] == indent_stack[-2]:
                                indent_stack.pop()
                            elif indent_stack[-1] < indent_stack[-2]:
                                indent_stack.pop()
                                indent_stack.pop()
                                lines.append(line)
                                break
                            path = {}
                            path["x"] = int(parts[0], 16)
                            path["y"] = int(parts[1], 16)
                            path["is_horizontal"] = parts[2] == "h"
                            path["turn"] = [int(part, 16) for part in parts[3 : ]]
                            element["path"].append(path)
                    elif parts[0] == "colour":
                        line = lines.pop()
                        parts = line.split()
                        element["stroke"] = "#" + parts[0]
                        element["active_stroke" if element["type"] == "wire" else "fill"] = "#" + parts[1]
                    elif parts[0] == "rect":
                        line = lines.pop()
                        parts = line.split()
                        element["x"] = int(parts[0], 16)
                        element["y"] = int(parts[1], 16)
                        element["width"] = int(parts[2], 16)
                        element["height"] = int(parts[3], 16)
                    elif parts[0] == "orientation":
                        line = lines.pop()
                        parts = line.split()
                        element["orientation"] = int(parts[0])
                    elif parts[0] == "module_id":
                        line = lines.pop()
                        parts = line.split()
                        element["module_id"] = parts[0]
                module_json["content"][element_id] = element
    except Exception as e:
        print(line)
        print(indent_stack)
        print(e)

    with open(file_path[ : -2] + "json", "w") as file:
        json.dump(module_json, file, indent = 4)
        file.write("\n")

dir = "D:\\Sseu\\Tryingssiuh\\Ssianxmuh\\_231025_DigitalLogic\\web\\modules"
name = sys.argv[1] if len(sys.argv) > 1 else "Timer"
if len(sys.argv) == 1:
    for name in filter(lambda name: name.endswith(".dl"), os.listdir(dir)):
        dl_compile(os.path.join(dir, name))
else:
    dl_compile(os.path.join(dir, sys.argv[1] + ".dl"))
