# Inputs and outputs

The module could have inputs and outputs.

An input could either be an *Input Port* or a *Parameter*. Output could only be an *Output Port*.

Input ports and output ports typically refers to a file path or folder. In Designer, they will be displayed as a *port* on the module. They could be have arbitrary type names such as `CsvFile`, `ImageFolder` to describe the underlying data. A module's output port could be connected to another module's input port, given they have the same type name.

Parameters are input values passed to the module while executing. In Designer, they are displayed on the right panel of the module. Parameter could only have scalar values such as `Integer`, `String`, `Boolean`, `Enum`. Each parameter could have additional attributes such as `default`, `min`, `max`, etc.

Refer to [the module spec](../../../../module-spec-definition.md) for full description.

To define module inputs and outputs:
* Add `inputs` and `outputs` section to the module spec to specify the module interface.
* Add reference to the inputs and outputs in `implementation/container/args` section. A reference looks like `{inputValue: name of parameter}`, which will be replaced by the value of the parameter when invoking the module. In this example, `inputValue` is only used for referencing a parameter. Use `inputPath` and `outputPath` to reference input ports and output ports accordingly.
