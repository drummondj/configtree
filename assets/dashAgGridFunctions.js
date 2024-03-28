var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};


dagfuncs.getGroupNames = function (params) {
    let values = JSON.parse(document.getElementById("group-names-options").innerHTML);
    return { values: values };
}


dagfuncs.CustomConfigValueEditor = class {

    // gets called once before the renderer is used
    init(params) {
        console.log(params);
        if (params.data.options || params.data.type == "Boolean") {
            var options;
            if (params.data.options) {
                options = params.data.options.split(" ");
            } else {
                options = ["true", "false"];
            }

            this.elementType = "select";
            this.eInput = document.createElement('select');
            this.eInput.value = params.value;
            this.eInput.name = params.name;
            this.eInput.style.width = params.column.actualWidth + "px";
            this.eInput.style.height = 'var(--ag-row-height) + 5px';
            this.eInput.style.borderWidth = 0;
            this.eInput.style.fontSize = 'calc(var(--ag-font-size) + 1px)';
            this.eInput.style.padding = '5px';
            for (var i = 0; i < options.length; i++) {
                var option = document.createElement("option");
                option.value = options[i];
                option.text = options[i];
                if (options[i] == params.value) {
                    option.selected = true;
                }
                this.eInput.appendChild(option);
            }
        } else if (params.data.type == "Integer" | params.data.type == "Float") {
            this.elementType = "input";
            this.eInput = document.createElement('input');
            this.eInput.value = params.value;
            this.eInput.style.height = 'var(--ag-row-height)';
            this.eInput.style.fontSize = 'calc(var(--ag-font-size) + 1px)';
            this.eInput.style.borderWidth = 0;
            this.eInput.style.width = '95%';
            this.eInput.type = "number";
            this.eInput.min = params.min;
            this.eInput.max = params.max;
            this.eInput.step = params.step || "any";
            this.eInput.required = params.required;
            this.eInput.placeholder = params.placeholder || "";
            this.eInput.name = params.name;
            this.eInput.disabled = params.disabled;
            this.eInput.title = params.title || ""
        } else {
            this.elementType = "input";
            this.eInput = document.createElement('input');
            this.eInput.value = params.value;
            this.eInput.style.height = 'var(--ag-row-height)';
            this.eInput.style.fontSize = 'calc(var(--ag-font-size) + 1px)';
            this.eInput.style.borderWidth = 0;
            this.eInput.style.width = '95%';
            this.eInput.type = "text";
            this.eInput.required = params.required;
            this.eInput.placeholder = params.placeholder || "";
            this.eInput.name = params.name;
            this.eInput.disabled = params.disabled;
            this.eInput.title = params.title || ""
        }
    }

    // gets called once when grid ready to insert the element
    getGui() {
        return this.eInput;
    }

    // focus and select can be done after the gui is attached
    afterGuiAttached() {
        this.eInput.showPicker();
    }

    // returns the new value after editing
    getValue() {
        return this.eInput.value;
    }

    // any cleanup we need to be done here
    destroy() {
        // but this example is simple, no cleanup, we could
        // even leave this method out as it's optional
    }

    // if true, then this editor will appear in a popup
    isPopup() {
        // and we could leave this method out also, false is the default
        return this.elementType == "select";
    }
}