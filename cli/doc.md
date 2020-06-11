# Module CLI design

This document describes the module cli usage details. For a quick walk through, refer to [this document](walk-through.md).

[[_TOC_]]



## General

The command line utility is part of the azure-cli-ml extension (the `az ml` commands). Module related commands are all under `az ml module` group and have some actions like `register`, `upgrade`, `download`, etc. to handle the corresponding scenarios.

###  Global options

All the commands in this document may apply to the following options:

##### `--subscription-id` `-s`
Specifies the subscription id for the workspace to operate on.

If not specified, will use the current active subscription id in the az cli environment.

Use the following commands to show or change current subscription in your environment.

* List subscriptions:
  ```bash
  az account list --output table
  ```

* Set active subscription:
  ```bash
  az account set --subscription "Subscription Name"
  ```

##### `--resource-group` `-g`
Specifies the resource group name for the workspace to operate on.

If not specified, the default configuration in az cli environment will be used.

Use the following command to set the default resource group name.

```bash
az ml folder attach -w "Your workspace name" -g "Your resource group name"
```

##### `--workspace-name` `-w`
Specifies name of the workspace to operate on.

If not specified, the default configuration in az cli environment will be used.

Use the following command to set the default resource group name.

```bash
az ml folder attach -w "Your workspace name" -g "Your resource group name"
```

##### `--namespace`

Specifies default namespace of the module.

Use the following command to set the default namespace.

**NOTE**: This parameter does not apply to `module list` command.

```bash
az configure --defaults module_namespace=<Namespace>
```

##### `--debug`

Increase logging verbosity to show all debug logs.

##### `--verbose`
Increase logging verbosity. Will show the full data that the CLI retrieved from server.

##### `--output` `-o`
Output format. Allowed values: `json`, `jsonc`, `table`,`tsv`. Default: `json`.

##### `--help` `-h`
Show this help message and exit.



## Usage scenarios

###  az ml module register

Register a module to the given workspace.

To register a module, a **module spec file** and **module implementation code (a.k.a. snapshot)** should be prepared in advance. We call it a **Module Package** in this document later on.

In the module package, there should be one yaml file to define the module spec. The module spec file must be located at the top level folder. The module spec could be with arbitrary file names, but must with a `.yaml` extension.

There can be multiple module spec files inside one module package, but the user will be enforced to specify the module spec path when registering the module via CLI command.

The module package could be located at various location with various format, such as:

* A path to a local folder.
* A link to a GitHub repo, could also contain subfolders like:
* A link to a DevOps build drop url. (Planned to support in the future)



Invoke a module register using the follow command:

```bash
az ml module register [--spec-file]
                      [--package-zip]
                      [--set-as-default-version]
                      [--amlignore-file]
```
> The parameters with `[]` (e.g. `[--spec-file]`) indicates that the parameter is optional.

##### `--spec-file` `-f`
The module spec file. Accepts either a local file path, a GitHub url, or a relative path inside the package specified by --package-zip.

##### `--package-zip` `-p`

The zip package contains the module spec and implemention code. Currently only accepts url to a DevOps build drop.

##### `--set-as-default-version` `-a`

If specified, will set the newly registered module as default version.

##### `--amlignore-file` `-i`

If specified, respect the given amlignore file when package snapshot.

#### Examples

```bash
# Register from a local path
az ml module register --spec-file /path/to/module/package/module_spec.yaml
# Register from GitHub
az ml module register --spec-file https://github.com/zzn2/sample_modules/tree/master/one_spec
# Register from DevOps build drop
az ml module register --spec-file relative/path/in/package/module_spec.yaml --package-zip=http://example.com/url/to/build/drop
# Register from a local path, with an .amlignore file specified
az ml module register --spec-file /path/to/module/package/module_spec.yaml --amlignore-file /path/to/common/.amlignore
```



### az ml module list

Lists the modules in the workspace.

```bash
az ml module list
```

#### Examples

```bash
# Show as table
az ml module list
```



### az ml module show

Shows detail information of a given module.

```bash
az ml module show --name
                 [--namespace]
                 [--version]
```

##### `--name` `-n`
Name of the module.

##### `--namespace`

Namespace of the module.

##### `--version`
Version of the module. If not specified, the default version will be shown.
#### Examples

```bash
# Show detailed information, including name, version, interfaces, etc.
az ml module show --name="My Awesome Module" --namespace=microsoft.com/office
# Show the detailed information for a specific version.
az ml module show --name="My Awesome Module" --namespace=microsoft.com/office --version=0.0.1
# Show detailed information for default namespace.
az ml module show --name="My Awesome Module"
```



### az ml module set-default-version

Sets a default version for a module.

```bash
az ml module set-default-version --name
                                 --version
                                [--namespace]
```

##### `--name` `-n`
Specify the name of the module.

##### `--namespace`

Specifies the namespace of the module.

##### `--version`
Specify the module version to be set as default.

#### Examples

```bash
az ml module set-as-default-version --name="My Awesome Module" --version=0.0.100
```



### az ml module disable

Disable a module.

```bash
az ml module disable --name
                    [--namespace]
```

##### `--name` `-n`

Specify the name of the module.

##### `--namespace`

Specifies the namespace of the module.

#### Examples

```bash
az ml module disable --name="My not-so-Awesome Module"
```



### az ml module enable

Enable a module.

```bash
az ml module enable --name
                   [--namespace]
```

##### `--name` `-n`

Specify the name of the module.

##### `--namespace`

Specifies the namespace of the module.

#### Examples

```bash
az ml module enable --name="My Awesome Module"
```



### az ml module download

Gets the url of a module package. The module spec and snapshot can be downloaded as a zip file from the url.
```bash
az ml module download --name
                     [--namespace]
                     [--version]
```
##### ``--name` `-n`
Specify the name of the module to be downloaded.

##### `--namespace`

Specifies the namespace of the module.

##### `--version`
Specify the module version. If not specified, will download the default version.
#### Examples

```bash
# Show download url for module default version
az ml module download "My Awesome Module"
# Show download url for specific version of module
az ml module download "My Awesome Module" --version=0.0.100
```

## Troubshooting

#### DataType registration

When registering module, following error message will be shown when using a new DataType. The DataType must be registered before registering module, refer to the following link to register DataType using python SDK: https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.graph.datatype?view=azure-ml-py#create-data-type-workspace--name--description--is-directory--parent-datatypes-none-

```
Error occurred when loading YAML file module_spec.yaml, details: Module Sample Module has invalid DataType references:
Input Input_Port uses DataType MyDataType which does not exist. Please create the DataType first.
Output Output_Port uses DataType MyDataType which does not exist. Please create the DataType first.
```

