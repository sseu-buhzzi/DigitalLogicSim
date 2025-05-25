function build_sidebar() {
    while (window.sidebar.firstChild !== null) {
        window.sidebar.removeChild(window.sidebar.firstChild);
    }
    for (let title in window.sidebar_titles) {
        let sidebar_title = window.sidebar_titles[title];
        window.sidebar.appendChild(sidebar_title.element);
        if (sidebar_title.is_folded) {
            window.sidebar.appendChild(sidebar_title.hint);
        } else {
            for (let sidebar_item of sidebar_title.items) {
                window.sidebar.appendChild(sidebar_item);
            }
        }
    }
}

function add_module(proto_json) {
    let new_module = new LogicModule(proto_json);
    if (!(new_module.id in window.modules)) {
        window.modules_proto_json[new_module.id] = proto_json;
        window.modules[new_module.id] = new_module;
        window.sidebar_titles.modules.add_item(new_module.id, function() {
            window.set_main_module(new_module);
            window.build_sidebar();
        });
        window.set_main_module(new_module);
        window.build_sidebar();
    }
}

function set_main_module(main_module) {
    let prev_main_module = window.sidebar_titles.modules.items.find(item => item.className === "sidebar_item_selected") ?? null;
    if (prev_main_module !== null) {
        prev_main_module.className = "sidebar_item";
    }
    window.sidebar_titles.modules.items.find(item => item.innerText === main_module.id).className = "sidebar_item_selected";
    window.sidebar_titles.input.items = [];
    for (let input_indx = 0; input_indx !== main_module.__input__.length; ++input_indx) {
        let input = main_module.__input__[input_indx];
        window.sidebar_titles.input.add_item(main_module.input_ids[input_indx], function() {
            let should_activate = this.className === "sidebar_item";
            input.__signal__ = should_activate;
            this.className = should_activate ? "sidebar_item_selected" : "sidebar_item";
            window.main_module.update_deque.add(input);
        });
        if (input.__signal__) {
            window.sidebar_titles.input.items[window.sidebar_titles.input.items.length - 1].className = "sidebar_item_selected";
        }
    }
    window.main_module = main_module;
}

function add_module_init(local_path) {
    window.fetch(local_path).then(response => response.text()).then(text => window.add_module(text));
}

function add_module_graphic() {
    let input_element = window.document.createElement("input");
    input_element.type = "file";
    input_element.accept = ".json";
    input_element.addEventListener("change", function() {
        if (input_element.files.length !== 0) {
            let reader = new window.FileReader();
            reader.onload = () => window.add_module(reader.result);
            reader.readAsText(input_element.files[0]);
        }
    })
    input_element.click();
};

function set_main_module_graphic() {
    if (window.floating_window.style.display === "none") {
        window.floating_window.style.display = "block";
        let floating_input_saved_value = window.main_module?.id ?? "";
        window.floating_input.value = floating_input_saved_value;
        window.floating_button.addEventListener("mouseup", function() {
            let new_module = window.modules[window.floating_input.value] ?? null;
            if (new_module === null) {
                window.floating_input.value = floating_input_saved_value;
            } else {
                window.floating_input.value = new_module.id;
                window.floating_window.style.display = "none";
                window.set_main_module(new_module);
            }
        });
    } else {
        window.floating_window.style.display = "none";
    }
}

function render_view() {
    window.lineJoin = "round";
    window.context.lineWidth = 1;
    window.context.fillStyle = "#000000";
    window.context.fillRect(0, 0, window.view.width, window.view.height);
    window.context.save();
    window.context.translate(-window.viewport.x, -window.viewport.y);
    window.context.scale(window.viewport.zoom, window.viewport.zoom);
    window.context.beginPath();
    window.context.moveTo(-1024, 0);
    window.context.lineTo(1024, 0);
    window.context.moveTo(0, -1024);
    window.context.lineTo(0, 1024);
    window.context.strokeStyle = "#808080";
    window.context.stroke();
    if (window.main_module !== null) {
        for (let element of window.main_module.__wire__) {
            window.context.beginPath();
            for (let path of element.path) {
                let coord = [path.x, path.y];
                let is_horizontal = path.is_horizontal;
                window.context.moveTo(...coord);
                for (let turn_dist of path.turn) {
                    coord[is_horizontal ? 0 : 1] += turn_dist;
                    window.context.lineTo(...coord);
                    is_horizontal = !is_horizontal;
                }
            }
            window.context.fillStyle = window.context.strokeStyle = element.__signal__ ? element.active_stroke : element.stroke;
            window.context.lineWidth = element.__signal__ ? 3 : 2;
            window.context;
            window.context.stroke();
            for (let path of element.path) {
                window.context.beginPath();
                window.context.arc(path.x, path.y, window.context.lineWidth, 0, window.Math.PI * 2);
                window.context.fill();
            }
        }
        for (let element of window.main_module.__submodule__) {
            window.context.lineWidth = 2;
            window.context.beginPath();
            window.context.rect(element.x, element.y, element.width, element.height);
            window.context.strokeStyle = element.stroke;
            window.context.stroke();
            window.context.fillStyle = element.fill;
            window.context.fill();
            window.context.fillStyle = element.stroke;
            window.context.fillText(element.module_id, element.x + 1, element.y + element.height - 1);
        }
        for (let element of window.main_module.__gate__) {
            window.context.lineWidth = 2;
            window.context.save();
            window.context.translate(element.x, element.y);
            window.context.rotate(element.orientation * Math.PI * 0.5);
            window.context.beginPath();
            window.context.moveTo(0, 0);
            switch (element.type) {
                case "buffer": {
                    window.context.lineTo(element.width * 0.5, element.height);
                    window.context.lineTo(element.width, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    break;
                }
                case "not": {
                    window.context.lineTo(element.width * 0.5, element.height);
                    window.context.lineTo(element.width, 0);
                    window.context.closePath();
                    window.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                    window.context.strokeStyle = element.stroke;
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    break;
                }
                case "and": case "and_array": {
                    window.context.quadraticCurveTo(0, element.height, element.width * 0.5, element.height);
                    window.context.quadraticCurveTo(element.width, element.height, element.width, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    break;
                }
                case "or": case "or_array": {
                    window.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                    window.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                    window.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                    window.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    break;
                }
                case "xor": {
                    window.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                    window.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                    window.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                    window.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    window.context.beginPath();
                    window.context.moveTo(0, -element.height * 0.25);
                    window.context.quadraticCurveTo(0, 0, element.width * 0.5, 0);
                    window.context.quadraticCurveTo(element.width, 0, element.width, -element.height * 0.25);
                    window.context.stroke();
                    break;
                }
                case "nand": case "nand_array": {
                    window.context.quadraticCurveTo(0, element.height, element.width * 0.5, element.height);
                    window.context.quadraticCurveTo(element.width, element.height, element.width, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    break;
                }
                case "nor": case "nor_array": {
                    window.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                    window.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                    window.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                    window.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    break;
                }
                case "xnor": {
                    window.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                    window.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                    window.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                    window.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                    window.context.closePath();
                    window.context.strokeStyle = element.stroke;
                    window.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                    window.context.stroke();
                    window.context.fillStyle = element.fill;
                    window.context.fill();
                    window.context.beginPath();
                    window.context.moveTo(0, -element.height * 0.25);
                    window.context.quadraticCurveTo(0, 0, element.width * 0.5, 0);
                    window.context.quadraticCurveTo(element.width, 0, element.width, -element.height * 0.25);
                    window.context.stroke();
                    break;
                }
            }
            window.context.restore();
        }
    }
    window.context.restore();
};

class SidebarTitle {
    is_folded = true;
    items = [];
    element = window.document.createElement("div");
    hint = window.document.createElement("div");
    on_mouse_up = function() {
        this.is_folded = !this.is_folded;
        window.build_sidebar();
    }.bind(this);
    constructor(name, ...item_args) {
        this.element.className = "sidebar_title";
        this.element.innerText = name;
        this.element.addEventListener("mouseup", this.on_mouse_up);
        this.hint.className = "sidebar_hint";
        this.hint.innerText = "...";
        this.hint.addEventListener("mouseup", this.on_mouse_up);
        for (let name_and_listener of item_args) {
            this.add_item(...name_and_listener);
        }
    }
    add_item(name, listener) {
        let sidebar_item = window.document.createElement("div");
        sidebar_item.className = "sidebar_item";
        sidebar_item.innerText = name;
        sidebar_item.addEventListener("mouseup", listener);
        this.items.push(sidebar_item);
    }
}

const __TRUE__ = {__signal__: true};
const __FALSE__ = {__signal__: false};
var __NULL__ = {};
class LogicModule {
    __wire__ = [];
    __submodule__ = [];
    __gate__ = [];
    constructor(proto_json, update_deque) {
        let {__input__, __output__, id, content} = JSON.parse(proto_json);
        this.id = id;
        this.input_ids = __input__;
        this.__input__ = __input__.map(input => content[input]);
        this.__output__ = __output__.map(output => content[output]);
        this.update_deque = update_deque ?? new Set();
        for (let element_id in content) {
            let element = content[element_id];
            switch (element.type) {
                case "wire": {
                    element.__terminal__ = [];
                    this.__wire__.push(element);
                    break;
                }
                case "module": {
                    element.__module__ = new LogicModule(window.modules_proto_json[element.module_id], this.update_deque);
                    this.__submodule__.push(element);
                    break;
                }
                default: {
                    element.__delay__ = element.__delay__ ?? 0;
                    element.timeout_id = null;
                    this.__gate__.push(element);
                    break;
                }
            }
        }
        // this.__input__.forEach(input => input.__volitale__ = true);
        for (let element of this.__wire__) {
            element.__volitale__ = element.__volitale__ ?? false;
            if (element.__volitale__) {
                this.update_deque.add(element);
            }
        }
        for (let element of this.__gate__) {
            switch (element.type) {
                case "buffer": case "not": {
                    element.__in__ = content[element.__in__];
                    element.__in__.__terminal__.push(element);
                    element.__out__ = content[element.__out__];
                                                                if (element.__in__ === undefined) {
                                                                    throw "element.__in__ === undefined";
                                                                }
                                                                if (element.__out__ === undefined) {
                                                                    throw "element.__out__ === undefined";
                                                                }
                    break;
                }
                case "and": case "or": case "xor": case "nand": case "nor": case "xnor": {
                    element.__in0__ = content[element.__in0__];
                    element.__in0__.__terminal__.push(element);
                    element.__in1__ = content[element.__in1__];
                    element.__in1__.__terminal__.push(element);
                    element.__out__ = content[element.__out__];
                    break;
                }
                case "and_array": case "or_array": case "nand_array": case "nor_array": {
                    element.__in_array__ = element.__in_array__.map(function(input) {
                        input = content[input];
                        input.__terminal__.push(element);
                        return input;
                    });
                    element.__out__ = content[element.__out__];
                    break;
                }
            }
        }
        for (let element of this.__submodule__) {
            let submodule = element.__module__;
            for (let input_indx = 0; input_indx !== submodule.__input__.length; ++input_indx) {
                let input = element.__input__[input_indx];
                let buffer = {
                    __in__: input === true ? __TRUE__ : input === false ? __FALSE__ : content[input],
                    __out__: submodule.__input__[input_indx],
                    __delay__: 0,
                    timeout_id: null,
                    type: "buffer"
                };
                buffer.__in__?.__terminal__?.push(buffer);
                this.__gate__.push(buffer);
                                                                (function(buffer) {
                                                                    if ([buffer.__in__, buffer.__out__].includes(undefined)) {
                                                                        throw buffer;
                                                                    };
                                                                })(buffer);
            }
            for (let output_indx = 0; output_indx !== submodule.__output__.length; ++output_indx) {
                let output = element.__output__[output_indx];
                let buffer = {
                    __in__: submodule.__output__[output_indx],
                    __out__: output === null ? __NULL__ : content[output],
                    __delay__: 0,
                    timeout_id: null,
                    type: "buffer"
                };
                buffer.__in__.__terminal__.push(buffer);
                this.__gate__.push(buffer);

            }
        }
        for (let element_id in this.content) {
            let element = this.content[element_id];
            if (element.type !== "wire") {
                this.update(element);
            }
        }
    }
    update(element) {
        if (element.timeout_id === null) {
            element.timeout_id = window.setTimeout(function() {
                if (element.__out__ !== __NULL__) {
                    // let res;
                    switch (element.type) {
                        case "buffer": {
                            element.__out__.__signal__ = element.__in__.__signal__;
                            break;
                        }
                        case "not": {
                            element.__out__.__signal__ = !element.__in__.__signal__;
                            break;
                        }
                        case "and": {
                            element.__out__.__signal__ = element.__in0__.__signal__ && element.__in1__.__signal__;
                            break;
                        }
                        case "or": {
                            element.__out__.__signal__ = element.__in0__.__signal__ || element.__in1__.__signal__;
                            break;
                        }
                        case "xor": {
                            element.__out__.__signal__ = element.__in0__.__signal__ !== element.__in1__.__signal__;
                            break;
                        }
                        case "nand": {
                            element.__out__.__signal__ = !(element.__in0__.__signal__ && element.__in1__.__signal__);
                            break;
                        }
                        case "nor": {
                            element.__out__.__signal__ = !(element.__in0__.__signal__ || element.__in1__.__signal__);
                            break;
                        }
                        case "xnor": {
                            element.__out__.__signal__ = element.__in0__.__signal__ === element.__in1__.__signal__;
                            break;
                        }
                        case "and_array": {
                            element.__out__.__signal__ = true;
                            for (let input of element.__in_array__) {
                                if (!input.__signal__) {
                                    element.__out__.__signal__ = false;
                                    break;
                                }
                            }
                            break;
                        }
                        case "or_array": {
                            element.__out__.__signal__ = false;
                            for (let input of element.__in_array__) {
                                if (input.__signal__) {
                                    element.__out__.__signal__ = true;
                                    break;
                                }
                            }
                            break;
                        }
                        case "nand_array": {
                            element.__out__.__signal__ = false;
                            for (let input of element.__in_array__) {
                                if (!input.__signal__) {
                                    element.__out__.__signal__ = true;
                                    break;
                                }
                            }
                            break;
                        }
                        case "nor_array": {
                            element.__out__.__signal__ = true;
                            for (let input of element.__in_array__) {
                                if (input.__signal__) {
                                    element.__out__.__signal__ = false;
                                    break;
                                }
                            }
                            break;
                        }
                    }
                    // if (element.__out__.__signal__ !== res) {
                    //     element.__out__.__signal__ = res;
                    //     this.update_deque.add(element.__out__);
                    // }
                }
                element.timeout_id = null;
            }.bind(this), element.__delay__);
        }
    }
    update_all() {
        for (let element of this.__submodule__) {
            element.__module__.update_all();
        }
        for (let element of this.__gate__) {
            this.update(element);
        }
    }
    handle_update_deque() {
        // let deque = Array.from(this.update_deque);
        // let element = deque[Math.floor(Math.random() * deque.length)] ?? null;
        let element = this.update_deque.values().next().value ?? null;
        // let element = this.update_deque.shift();
        if (element !== null) {
            for (let terminal of element.__terminal__) {
                this.update(terminal);
            }
            this.update_deque.delete(element);
            if (element.__volitale__) {
                this.update_deque.add(element);
            }
        }
    }
}

window.sidebar = window.document.getElementById("sidebar");
window.floating_window = window.document.getElementById("floating_window");
window.floating_input = window.document.getElementById("floating_input");
window.floating_button = window.document.getElementById("floating_button");

window.sidebar_titles = {
    modules: new SidebarTitle("modules"),
    input: new SidebarTitle("input"),
    management: new SidebarTitle(
        "management",
        ["add_module_graphic", window.add_module_graphic],
        ["main_module", window.set_main_module_graphic]
    ),
    run: new SidebarTitle(
        "run_and_debug",
        ["run", null]
    ),
    tools: new SidebarTitle(
        "tools",
        ["select", null]
    )
}
window.build_sidebar();

window.view = window.document.getElementById("view");
window.context = window.view.getContext("2d");

window.viewport = {
    x: -256,
    y: -64,
    zoom: 1,
}
window.view.width = window.innerWidth;
window.view.height = window.innerHeight;
window.context.lineJoin = "round"
window.context.font = "8px Courier"

window.modules_proto_json = {};
window.modules = {};
window.main_module = null;

window.mouse = {
    x: 0,
    y: 0,
    is_pressed: false,
    dx: 0,
    dy: 0,
    move(x, y) {
        this.dx = x - this.x;
        this.dy = y - this.y;
        this.x = x;
        this.y = y;
    }
};
window.view.addEventListener("mousedown", function(event) {
    window.mouse.move(event.x, event.y);
    window.mouse.is_pressed = true;
});
window.document.addEventListener("mousemove", function(event) {
    window.mouse.move(event.x, event.y);
    if (window.mouse.is_pressed) {
        window.viewport.x -= window.mouse.dx;
        window.viewport.y -= window.mouse.dy;
    }
});
window.document.addEventListener("mouseup", function(event) {
    window.mouse.move(event.x, event.y);
    window.mouse.is_pressed = false;
});
window.view.addEventListener("wheel", function(event) {
    let new_zoom = window.viewport.zoom * (event.deltaY < 0 ? 1.0666666666666667 : 0.9375);
    let scale_offset = new_zoom / window.viewport.zoom;
    window.viewport.x = (event.x + window.viewport.x) * scale_offset - event.x;
    window.viewport.y = (event.y + window.viewport.y) * scale_offset - event.y;
    window.viewport.zoom = new_zoom;
});
window.addEventListener("resize", function() {
    window.view.width = window.innerWidth;
    window.view.height = window.innerHeight;
})

window.setTimeout(function() {
    local_paths = [
        // "./modules/FullAdder.json",
        // "./modules/Latch_d.json",
        // "./modules/Timer.json",
        // "./modules/_231102_TimerTest.json"
        // // "./modules/_231026_Adder.json",
        // // "./modules/_231026_Adder_8bit.json",
        // "./modules/Trigger_d.json",
        // "./modules/_231027_Register_32bit.json",
        "./modules/Latch_rs.json",
        "./modules/RAMCell.json",
        "./modules/RAMBitSlice_16.json",
        "./modules/Decoder_4_16.json",
        "./modules/Decoder_en_4_16.json",
        "./modules/RAM_256_8.json",
    ];
    function init_cbfunc() {
        if (local_paths.length !== 0) {
            window.add_module_init(local_paths.shift());
            window.setTimeout(init_cbfunc, 64);
        }
    }
    return init_cbfunc;
}(), 256);

window.setInterval(function() {
    if (window.main_module !== null) {
        window.main_module.update_all();
    }
}, 0);
window.setInterval(window.render_view, 64);
