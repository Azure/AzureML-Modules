Optional Inputs & Parameters
======================

This document introduces how to create modules  with optional inputs and parameters for Azure Machine Learning.

Use `optional` to make an input port or a parameter optional.
In the snippet bellow, two input ports and the parameter "Optional string parameter" are optional.
```yaml
inputs:
- name: Optional input path 1
  type: AnyDirectory
  optional: true
- name: Optional input path 2
  type: AnyDirectory
  optional: true
- name: String parameter
  type: String
  default: string value
  description: A parameter accepts a string value.
- name: Optional string parameter
  type: String
  optional: true
  description: A optional parameter accepts a string value.
```

In the args part, put optional parameter into a nested list inside `args` section:
```yaml
implementation:
  container:
    command: [python, optional_input.py]
    args: [
      --input-path, {inputPath: Input path},
      [--optional-input-path, {inputPath: Optional input path}],
      --string-param, {inputValue: String parameter},
      [--optional-string-param, {inputValue: Optional string parameter}],
    ]
```

When invoking the module, the command line will look like:

```bash
# When the optional input is linked, and the optional parameter is set.
python optional_input.py --input-path-1 /aaa/bbb --optional-input-path /xxx/yyy --string-param abc --optional-string-param def

# When the optional input is linked, and the optional parameter is not set.
python optional_input.py --input-path-1 /aaa/bbb --optional-input-path /xxx/yyy --string-param abc

# When the optional input is not linked, and the optional parameter is set.
python optional_input.py --input-path-1 /aaa/bbb --string-param abc --optional-string-param def

# When the optional input is not linked, and the optional parameter is not set.
python optional_input.py --input-path-1 /aaa/bbb --string-param abc
```
