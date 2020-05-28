# Module spec guidance

This document takes a tutorial of how to define a module using a yaml spec.

## Create the first module

To create a module, the following parts are needed:
* A bundle of code that could be invoked from command line, usually a script file written in Python.
* A YAML file which defines the how to execute the module.

#### The module script

Create the script of the module:

```python
if __name__ == '__main__':
    print('Hello from AzureML!')
```

#### The module definition

Create the module definition file:

```yaml
amlModuleIdentifier:
  moduleName: First Module
  moduleVersion: 0.0.1
  namespace: microsoft.com/azureml/samples
metadata:
  annotations:
    tags: [AzureML, Sample]
description: First module created for AzureML.
implementation:
  container:
    amlEnvironment:
      python:
        condaDependencies:
          dependencies:
            - python=3.6.8
            - pip:
              - azureml-defaults
    command: [python, hello_world.py]
```

Refer to [the module spec definition](module-spec-definition.md) for details. Below are the spec briefly explained:

* `amlModuleIdentifier`: The information to identify the module.
* `metadata`: Additional metadata for the module.
* `implementation/container/amlEnvironment`: The environment in which the module script runs. See [Running environments](#Running environments) section for details.
* `command`: The command to invoke the module.

#### The full sample

Refer to [here](samples/modules/basic-modules/first-module) for the full sample.

#### Register the module to workspace and run

Refer to [register module to workspace and run](../notebooks/register-module-to-workspace-and-run.ipynb) to see the guidance.

## Inputs and outputs

The module could have inputs and outputs.

An input could either be an *Input Port* or a *Parameter*. Output could only be an *Output Port*.

Refer to [the document](samples/modules/basic-modules/inputs-and-outputs/README.md) to see how to set inputs and outputs for a module.

Refer to [here](samples/modules/basic-modules/inputs-and-outputs) to see a full example of a module with inputs and outputs.

### Optional inputs

Some inputs may be optional. Refer to [this document](samples/modules/basic-modules/optional-inputs/README.md) to see how to use optional inputs. And an example module with optional inputs could be found [here](samples/modules/basic-modules/optional-inputs).

## Running environments

The running environment of the module could either be specified by a docker image or a conda environment. Refer to [here](samples/modules/basic-modules/environment) to see samples for various running environments.

## Module snapshot

The module script may be separate to multiple files for better source code structure. When registering a module, the files located the same folder of the module spec yaml file will be packaged as a *snapshot* of the module. The folder is call base folder of snapshot.

Usually, some files (e.g. `__pycache__`) are not need to be packaged into snapshot. List the unneeded files into an `.amlignore` file to the base folder of the snapshot to ignore them. See [this documentation](topics/ignore-files.md) for details.

Also, sometimes some additional files may want to be included when packaging the snapshot. Refer to [this document](topics/additional-includes.md) to see how to include additional files to the snapshot.

## Various module types

Besides the basic modules, there are various types of modules to complete some specific advanced jobs.

### Mpi modules

An mpi module could run jobs across multiple computing nodes. Refer to [mpi modules](samples/modules/mpi-modules) for details.

### Parallel modules

A parallel module could run specific job in parallel. The input data will be separated to several *mini batches* and passed to the module script. Refer to [parallel modules](samples/modules/parallel-modules) for details.