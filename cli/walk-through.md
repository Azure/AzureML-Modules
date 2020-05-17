## prerequisite

* The Azure CLI (follow [the instructions here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) to install).

* Install the latest azure-cli-ml extension

  ```bash
  # Uninstall azure-cli-ml (the `az ml` commands)
  az extension remove -n azure-cli-ml

  # Install local version of azure-cli-ml (which includes `az ml module` commands)
  az extension add --source https://azuremlsdktestpypi.azureedge.net/CLI-SDK-Runners-Validation/13766063/azure_cli_ml-0.1.0.13766063-py3-none-any.whl --pip-extra-index-urls https://azuremlsdktestpypi.azureedge.net/CLI-SDK-Runners-Validation/13766063 --yes
  ```

* Confirm the version of installed azure-cli-ml

  ```bash
  az extension list -o table
  ```

* Prepare the environment

  ```bash
  # Login
  az login
  # Show account list, verify your default subscription
  az account list --output table
  # Set your default subscription if needed
  az account set -s "Your subscription name"

  # Configure workspace name and resource name
  # NOTE: This will set workspace setting only to the current folder. If you change to another folder, you need to set this again.
  az ml folder attach -w "Your workspace name" -g "Your resource group name"

  # Set default namespace of module to avoid specifying to each of the following commands
  az configure --defaults module_namespace=microsoft.com/office
  ```

* Set default output format to table to improve experience

  ```bash
  az configure
  ...
  Do you wish to change your settings? (y/N): y
  What default output format would you like?
   [1] json - JSON formatted output that most closely matches API responses.
   [2] jsonc - Colored JSON formatted output that most closely matches API responses.
   [3] table - Human-readable output format.
   [4] tsv - Tab- and Newline-delimited. Great for GREP, AWK, etc.
   [5] yaml - YAML formatted output. An alternative to JSON. Great for configuration files.
   [6] yamlc - Colored YAML formatted output. An alternative to JSON. Great for configuration files.
   [7] none - No output, except for errors and warnings.
  Please enter a choice [Default choice(1)]: 3
  ```

* Troubshooting:

  For issue `Unable to load extension 'azure-cli-ml: xxx'. Use --debug for more information.` , try to uninstall the azure-cli pip package (if any).

  ```bash
  pip uninstall azure-cli
  ```

  If the problem still exists, try to reinstall the azure cli according to [the installation guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).

## Scenarios

### Register module

Modules could either be registered from a local folder, a GitHub url, or a zip package (typically created by a DevOps CI build job). Some sample modules are available [here](../specs/samples/modules).

```bash
$ # Register from local folder
$ az ml module register --spec-file=resources/sample_module_0.1.0/module_spec.yaml
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.0              nlp, bert  Active


$ # Register from GitHub url
$ az ml module register --spec-file=https://github.com/zzn2/sample_modules/blob/master/4_mpi_module/mpi_module.yaml
Name        Namespace             Default version    Status
----------  --------------------  -----------------  --------
Mpi Module  microsoft.com/office  0.0.1              Active

$ # Register from a zip package build by DevOps
$ az ml module register --package-zip="https://dev.azure.com/weda/recommenders/_apis/build/builds/46/artifacts?artifactName=snapshot&api-version=5.1&%24format=zip" --spec-file stratified_splitter.yaml
Name                 Namespace          Default version    Tags          Status
-------------------  -----------------  -----------------  ------------  --------
Stratified Splitter  microsoft.com/cat  1.1.14             Recommenders  Active

$ # Same version could not be registered twice
$ az ml module register --spec-file=resources/sample_module_0.1.0/module_spec.yaml
Version 0.1.0 has already exist in module Sample Module (namespace: microsoft.com/office)

$ # Trying to register duplicate version returns exit code 0 (incidates succeed), easy for CI usage.
$ echo $?
0
```

### Validate module spec

Module spec could be validated before registering to the workspace.

```bash
$ # Valid spec
$ az ml module validate-spec -f resources/sample_module_0.1.2/module_spec.yaml
Name           Namespace             Tags       Status
-------------  --------------------  ---------  --------
Sample Module  microsoft.com/office  nlp, bert  Active

$ # Invalid specs
$ az ml module validate-spec -f resources/invalid_missing_entry/module_spec.yaml
Entry file 'invoker.py' doesn't exist in source directory.

$ az ml module validate-spec -f resources/invalid_missing_required_attributes/module_spec.yaml
Error occurred when loading YAML file module_spec.yaml, details: File 'module_spec.yaml' has parse error(s):
Location: #  Message: The properties ["implementation"] are required.
```

### List modules

```bash
$ az ml module list -o table
Name                 Namespace             Default version    Tags          Status
-------------------  --------------------  -----------------  ------------  --------
Sample Module        microsoft.com/office  0.1.0              nlp, bert     Active
Mpi Module           microsoft.com/office  0.0.1                            Active
Stratified Splitter  microsoft.com/cat     1.1.14             Recommenders  Active
```

### Module upgrading, version vs default version

One module could have multiple versions. Each module has a "default version", which will be applied when not specified.

Use `module register` command to register a new version of a module. By default, a `module register` command does not change the default version of a module (unless registering a new module for the first time).

```bash
$ az ml module register --spec-file=resources/sample_module_0.1.1/module_spec.yaml
Registered new version 0.1.1, but the module default version kept to be 0.1.0.
Use "az ml module set-default-version" or "az ml module register --set-as-default-version" to set default version.
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.0              nlp, bert  Active
```

 The default version could be changed when specified `--set-as-default-version` to the `module register`.

```bash
$ az ml module register --spec-file=resources/sample_module_0.1.2/module_spec.yaml --set-as-default-version
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.2              nlp, bert  Active
```

The default version could also be changed any time using a `module set-default-version` command:

```bash
$ az ml module set-default-version --name="Sample Module" --version=0.1.0
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.0              nlp, bert  Active
```

### Show detailed information of a module

Use `az ml module show` command to show the detailed information of a module.

```bash
$ az ml module show --name="Sample Module"
Property       Value
-------------  --------------------------------------------------
Name           Sample Module
Namespace      microsoft.com/office
Description    Basic module for demo.
Help document  http://readthedocs.com/proj
Contact        AzureML Studio Team <stcamlstudiosg@microsoft.com>
Registered by  Zhidong Zhu
Version        0.1.0
All versions   0.1.0 (Default), 0.1.1, 0.1.2
Tags           nlp, bert
Status         Active
```

By default, `az ml module show` shows the default version of a module. It is also able to show any specific version of a module with a `--version` option.
```bash
$ az ml module show --name="Sample Module" --version=0.1.1
Property       Value
-------------  --------------------------------------------------
Name           Sample Module
Namespace      microsoft.com/office
Description    Basic module for demo.
Help document  http://readthedocs.com/proj
Contact        AzureML Studio Team <stcamlstudiosg@microsoft.com>
Registered by  Zhidong Zhu
Version        0.1.1
All versions   0.1.0 (Default), 0.1.1, 0.1.2
Tags           nlp, bert
Status         Active
```

By default, `az ml module show` shows the modules in the default namespace specified with `az configure --defaults module_namespace=xx`. To list modules in non-default namespaces, specify the `--namespace` in the command line.

> Similar to `modle show`, Other commands also have  `--namespace` option.

```bash
$ az ml module show --name="Stratified Splitter" --namespace=microsoft.com/cat
Property       Value
-------------  ---------------------------------------------------------------------------------------------
Name           Stratified Splitter
Namespace      microsoft.com/cat
Description    Python stratified splitter from Recommenders repo: https://github.com/Microsoft/Recommenders.
Help document
Contact
Registered by  Zhidong Zhu
Version        1.1.14
All versions   1.1.14 (Default)
Tags           Recommenders
Status         Active
```

### Disable & enable modules

```bash
$ az ml module disable --name="Sample Module"
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.0              nlp, bert  Disabled
```

```bash
$ az ml module enable --name="Sample Module"
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.0              nlp, bert  Active
```

### Module download

Downloads the snapshot (or optionally the module spec as yaml) of a module.

```bash
$ # Download module to a specific folder
$ # If --target-dir not specified, will download to current working directory
$ mkdir ~/modules
$ az ml module download --name="Sample Module" --target-dir ~/modules
Snapshot
-------------------------------------------------------------------------
/root/modules/zhizhu-ws-25-Sample Module-microsoft.com_office-default.zip

$ # Download snapshot of specific version
$ az ml module download --name="Sample Module" --version=0.1.1 --target-dir ~/modules
Snapshot
-----------------------------------------------------------------------
/root/modules/zhizhu-ws-25-Sample Module-microsoft.com_office-0.1.1.zip

$ # Download module spec along with the snapshot of default version
$ az ml module download --name="Sample Module" --include-module-spec --target-dir ~/modules --overwrite
Module_spec                                                                 Snapshot
--------------------------------------------------------------------------  -------------------------------------------------------------------------
/root/modules/zhizhu-ws-25-Sample Module-microsoft.com_office-default.yaml  /root/modules/zhizhu-ws-25-Sample Module-microsoft.com_office-default.zip

$ # Register a module with large snapshot
$ az ml module register --spec-file=resources/sample_module_0.1.3/module_spec.yaml --set-as-default-version
Name           Namespace             Default version    Tags       Status
-------------  --------------------  -----------------  ---------  --------
Sample Module  microsoft.com/office  0.1.3              nlp, bert  Active

$ # Then download, to verify the progress bar
$ az ml module download --name="Sample Module" --version=0.1.3 --target-dir ~/modules
Snapshot
-----------------------------------------------------------------------
/root/modules/zhizhu-ws-26-Sample Module-microsoft.com_office-0.1.3.zip
```



