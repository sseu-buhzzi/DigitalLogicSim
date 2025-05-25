class SidebarTitle {
    is_folded = true;
    items = [];
    element = document.createElement("div");
    hint = document.createElement("div");
    on_mouse_up = function() {
        this.is_folded = !this.is_folded;
        user_interface.build_sidebar();
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
        let sidebar_item = document.createElement("div");
        sidebar_item.className = "sidebar_item";
        sidebar_item.innerText = name;
        sidebar_item.addEventListener("mouseup", listener);
        this.items.push(sidebar_item);
    }
}

class LogicModule {
    __wire__ = [];
    __submodule__ = [];
    __gate__ = [];
    constructor(proto_json, supmodule) {
        let {__input__, __output__, id, content} = JSON.parse(proto_json);
        this.id = id;
        this.input_ids = __input__;
        this.__input__ = __input__.map(input => content[input]);
        this.__output__ = __output__.map(output => content[output]);
        this.update_deque = supmodule?.update_deque ?? new Set();
        this.__TRUE__ = supmodule?.__TRUE__ ?? {__signal__: true};
        this.__FALSE__ = supmodule?.__FALSE__ ?? {__signal__: false};
        this.__NULL__ = supmodule?.__NULL__ ?? {};
        for (let element_id in content) {
            let element = content[element_id];
            switch (element.type) {
                case "wire": {
                    element.__terminal__ = [];
                    this.__wire__.push(element);
                    break;
                }
                case "module": {
                    element.__module__ = new LogicModule(user_interface.modules_proto_json[element.module_id], this.update_deque);
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
                    __in__: input === true ? this.__TRUE__ : input === false ? this.__FALSE__ : content[input],
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
                    __out__: output === null ? this.__NULL__ : content[output],
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
            element.timeout_id = setTimeout(function() {
                if (element.__out__ !== this.__NULL__) {
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
        // console.time("__submodule__");
        for (let element of this.__submodule__) {
            element.__module__.update_all();
        }
        // console.timeEnd("__submodule__");
        // console.time("__gate__");
        for (let element of this.__gate__) {
            this.update(element);
        }
        // console.timeEnd("__gate__");
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

class UserInterface {
    build_sidebar() {
        while (this.sidebar.firstChild !== null) {
            this.sidebar.removeChild(this.sidebar.firstChild);
        }
        for (let title in this.sidebar_titles) {
            let sidebar_title = this.sidebar_titles[title];
            this.sidebar.appendChild(sidebar_title.element);
            if (sidebar_title.is_folded) {
                this.sidebar.appendChild(sidebar_title.hint);
            } else {
                for (let sidebar_item of sidebar_title.items) {
                    this.sidebar.appendChild(sidebar_item);
                }
            }
        }
    }
    add_module(proto_json) {
        let new_module = new LogicModule(proto_json);
        if (!(new_module.id in this.modules)) {
            this.modules_proto_json[new_module.id] = proto_json;
            this.modules[new_module.id] = new_module;
            this.sidebar_titles.modules.add_item(new_module.id, function() {
                this.set_main_module(new_module);
                this.build_sidebar();
            }.bind(this));
            this.set_main_module(new_module);
            this.build_sidebar();
        }
    }
    set_main_module(curr_main_module) {
        let prev_main_module = this.sidebar_titles.modules.items.find(item => item.className === "sidebar_item_selected") ?? null;
        if (prev_main_module !== null) {
            prev_main_module.className = "sidebar_item";
        }
        this.sidebar_titles.modules.items.find(item => item.innerText === curr_main_module.id).className = "sidebar_item_selected";
        this.sidebar_titles.input.items = [];
        for (let input_indx = 0; input_indx !== curr_main_module.__input__.length; ++input_indx) {
            let input = curr_main_module.__input__[input_indx];
            this.sidebar_titles.input.add_item(curr_main_module.input_ids[input_indx], function() {
                let should_activate = this.className === "sidebar_item";
                input.__signal__ = should_activate;
                this.className = should_activate ? "sidebar_item_selected" : "sidebar_item";
                curr_main_module.update_deque.add(input);
            });
            if (input.__signal__) {
                this.sidebar_titles.input.items[this.sidebar_titles.input.items.length - 1].className = "sidebar_item_selected";
            }
        }
        this.main_module = curr_main_module;
    }
    add_module_init(local_path) {
        fetch(local_path).then(response => response.text()).then(text => this.add_module(text));
    }
    add_module_graphic() {
        let input_element = document.createElement("input");
        input_element.type = "file";
        input_element.accept = ".json";
        input_element.addEventListener("change", function() {
            if (input_element.files.length !== 0) {
                let reader = new FileReader();
                reader.onload = () => user_interface.add_module(reader.result);
                reader.readAsText(input_element.files[0]);
            }
        }.bind(this));
        input_element.click();
    }
    set_main_module_graphic() {
        if (this.floating_style.display === "none") {
            this.floating_style.display = "block";
            let floating_input_saved_value = this.main_module?.id ?? "";
            this.floating_input.value = floating_input_saved_value;
            this.floating_button.addEventListener("mouseup", function() {
                let new_module = modules[this.floating_input.value] ?? null;
                if (new_module === null) {
                    this.floating_input.value = floating_input_saved_value;
                } else {
                    this.floating_input.value = new_module.id;
                    this.floating_style.display = "none";
                    set_main_module(new_module);
                }
            });
        } else {
            this.floating_style.display = "none";
        }
    }
    render_view() {
        this.context.lineJoin = "round";
        this.context.font = "8px Courier";
        this.context.lineWidth = 1;
        this.context.fillStyle = "#000000";
        this.context.fillRect(0, 0, this.view.width, this.view.height);
        this.context.save();
        this.context.translate(-this.viewport.x, -this.viewport.y);
        this.context.scale(this.viewport.zoom, this.viewport.zoom);
        this.context.beginPath();
        this.context.moveTo(-1024, 0);
        this.context.lineTo(1024, 0);
        this.context.moveTo(0, -1024);
        this.context.lineTo(0, 1024);
        this.context.strokeStyle = "#808080";
        this.context.stroke();
        if (this.main_module !== null) {
            for (let element of this.main_module.__wire__) {
                this.context.beginPath();
                for (let path of element.path) {
                    let coord = [path.x, path.y];
                    let is_horizontal = path.is_horizontal;
                    this.context.moveTo(...coord);
                    for (let turn_dist of path.turn) {
                        coord[is_horizontal ? 0 : 1] += turn_dist;
                        this.context.lineTo(...coord);
                        is_horizontal = !is_horizontal;
                    }
                }
                this.context.fillStyle = this.context.strokeStyle = element.__signal__ ? element.active_stroke : element.stroke;
                this.context.lineWidth = element.__signal__ ? 3 : 2;
                this.context;
                this.context.stroke();
                for (let path of element.path) {
                    this.context.beginPath();
                    this.context.arc(path.x, path.y, this.context.lineWidth, 0, Math.PI * 2);
                    this.context.fill();
                }
            }
            for (let element of this.main_module.__submodule__) {
                this.context.lineWidth = 2;
                this.context.beginPath();
                this.context.rect(element.x, element.y, element.width, element.height);
                this.context.strokeStyle = element.stroke;
                this.context.stroke();
                this.context.fillStyle = element.fill;
                this.context.fill();
                this.context.fillStyle = element.stroke;
                this.context.fillText(element.module_id, element.x + 1, element.y + element.height - 1);
            }
            for (let element of this.main_module.__gate__) {
                this.context.lineWidth = 2;
                this.context.save();
                this.context.translate(element.x, element.y);
                this.context.rotate(element.orientation * Math.PI * 0.5);
                this.context.beginPath();
                this.context.moveTo(0, 0);
                switch (element.type) {
                    case "buffer": {
                        this.context.lineTo(element.width * 0.5, element.height);
                        this.context.lineTo(element.width, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        break;
                    }
                    case "not": {
                        this.context.lineTo(element.width * 0.5, element.height);
                        this.context.lineTo(element.width, 0);
                        this.context.closePath();
                        this.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                        this.context.strokeStyle = element.stroke;
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        break;
                    }
                    case "and": case "and_array": {
                        this.context.quadraticCurveTo(0, element.height, element.width * 0.5, element.height);
                        this.context.quadraticCurveTo(element.width, element.height, element.width, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        break;
                    }
                    case "or": case "or_array": {
                        this.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                        this.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                        this.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                        this.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        break;
                    }
                    case "xor": {
                        this.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                        this.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                        this.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                        this.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        this.context.beginPath();
                        this.context.moveTo(0, -element.height * 0.25);
                        this.context.quadraticCurveTo(0, 0, element.width * 0.5, 0);
                        this.context.quadraticCurveTo(element.width, 0, element.width, -element.height * 0.25);
                        this.context.stroke();
                        break;
                    }
                    case "nand": case "nand_array": {
                        this.context.quadraticCurveTo(0, element.height, element.width * 0.5, element.height);
                        this.context.quadraticCurveTo(element.width, element.height, element.width, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        break;
                    }
                    case "nor": case "nor_array": {
                        this.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                        this.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                        this.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                        this.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        break;
                    }
                    case "xnor": {
                        this.context.quadraticCurveTo(0, element.height * 0.5, element.width * 0.5, element.height);
                        this.context.quadraticCurveTo(element.width, element.height * 0.5, element.width, 0);
                        this.context.quadraticCurveTo(element.width, element.height * 0.25, element.width * 0.5, element.height * 0.25);
                        this.context.quadraticCurveTo(0, element.height * 0.25, 0, 0);
                        this.context.closePath();
                        this.context.strokeStyle = element.stroke;
                        this.context.arc(element.width * 0.5, element.height + 2, 2, 0, Math.PI * 2);
                        this.context.stroke();
                        this.context.fillStyle = element.fill;
                        this.context.fill();
                        this.context.beginPath();
                        this.context.moveTo(0, -element.height * 0.25);
                        this.context.quadraticCurveTo(0, 0, element.width * 0.5, 0);
                        this.context.quadraticCurveTo(element.width, 0, element.width, -element.height * 0.25);
                        this.context.stroke();
                        break;
                    }
                }
                this.context.restore();
            }
        }
        this.context.restore();
    }
    add_module_from_local_paths(local_paths) {
        setTimeout(function init_cbfunc() {
            if (local_paths.length !== 0) {
                this.add_module_init(local_paths.shift());
                setTimeout(init_cbfunc.bind(this), 64);
            }
        }.bind(this), 16);
    }
    sidebar = document.getElementById("sidebar");
    floating_window = document.getElementById("floating_window");
    floating_input = document.getElementById("floating_input");
    floating_button = document.getElementById("floating_button");
    view = document.getElementById("view");
    context = view.getContext("2d");
    viewport = {
        x: -0x100,
        y: -0x40,
        zoom: 1,
    };
    mouse = {
        move(x, y) {
            this.dx = x - this.x;
            this.dy = y - this.y;
            this.x = x;
            this.y = y;
        },
        x: 0,
        y: 0,
        is_pressed: false,
        dx: 0,
        dy: 0
    };
    modules_proto_json = {};
    modules = {};
    main_module = null;
    constructor() {
        this.view.width = innerWidth;
        this.view.height = innerHeight;
        this.sidebar_titles = {
            modules: new SidebarTitle("modules"),
            input: new SidebarTitle("input"),
            management: new SidebarTitle(
                "management",
                ["add_module_graphic", this.add_module_graphic.bind(this)]
            )
        };
        this.view.addEventListener("mousedown", function(event) {
            this.mouse.move(event.x, event.y);
            this.mouse.is_pressed = true;
        }.bind(this));
        document.addEventListener("mousemove", function(event) {
            this.mouse.move(event.x, event.y);
            if (this.mouse.is_pressed) {
                this.viewport.x -= this.mouse.dx;
                this.viewport.y -= this.mouse.dy;
            }
        }.bind(this));
        document.addEventListener("mouseup", function(event) {
            this.mouse.move(event.x, event.y);
            this.mouse.is_pressed = false;
        }.bind(this));
        this.view.addEventListener("wheel", function(event) {
            let new_zoom = this.viewport.zoom * (event.deltaY < 0 ? 1.0666666666666667 : 0.9375);
            let scale_offset = new_zoom / this.viewport.zoom;
            this.viewport.x = (event.x + this.viewport.x) * scale_offset - event.x;
            this.viewport.y = (event.y + this.viewport.y) * scale_offset - event.y;
            this.viewport.zoom = new_zoom;
        }.bind(this));
        addEventListener("resize", function() {
            this.view.width = innerWidth;
            this.view.height = innerHeight;
        }.bind(this));
        setInterval(function() {
            if (this.main_module !== null) {
                this.main_module.update_all();
            }
        }.bind(this), 64);
        setInterval(this.render_view.bind(this), 64);
    }
};

var user_interface = new UserInterface();
