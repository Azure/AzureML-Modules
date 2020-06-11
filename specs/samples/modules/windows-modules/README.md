# Windows Module

Windows modules are modules that can be executed on Windows compute.

### How to write the module spec

Set `os` field to `windows` in module spec and here is a sample:

```yaml
amlModuleIdentifier:
  moduleName: Hello Windows
  moduleVersion: 0.0.1
  namespace: microsoft.com/azureml/samples
metadata:
  annotations:
    tags: [AzureML, Sample]
description: A module with inputs and outputs.
inputs:
- name: Input path
  type: AnyDirectory
  description: The directory contains dataframe.
- name: String parameter
  type: String
  description: A parameter accepts a string value.
outputs:
- name: Output path
  type: AnyDirectory
  description: The directory contains a dataframe.
implementation:
  os: windows
  container:
    # The following amlEnvironment section is just a dummy definition for by passing the schema check
    amlEnvironment:
      python:
        condaDependencies:
          dependencies:
            - python=3.6.8
    command: [python, hello_world.py]
    args: [
      --input-path, {inputPath: Input path},
      --string-parameter, {inputValue: String parameter},
      --int-parameter, {inputValue: Int parameter},
      --boolean-parameter, {inputValue: Boolean parameter},
      --output-path, {outputPath: Output path},
    ]
```

Notice, conda and docker image are NOT supported on Windows compute yet, so the amlEnvironment and image fields won't take effects even defined in module spec. For short term, it's still required to add the dummy amlEnvironment section to pass the schema validation. We would fix it in the future version.

### Known limitations

- Windows compute doesn't support docker image. Modules are executed on the compute host directly.
- Users need to remote to compute target and run `pip install azureml-defaults --user --upgrade` manually, before executing Windows modules on it.
- Windows module doesn't support installing dependencies by defining them in module specification. Users can install dependencies in runtime code. Please see `hello-windows/hello_world.py` for reference.

### How to create Windows Compute

Here is a wiki for [Setup AzureML Windows Compute Cluster](https://eemo.visualstudio.com/TEE/_git/TEEGit?path=%2FOffline%2FSmartCompose%2Faml%2FSetup_AML_Windows_Compute_Cluster.md&version=GBhaoz%2Fsmartcompose&_a=preview).