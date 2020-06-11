Definition of module spec
==================================



[[_TOC_]]

This document describes the specification to define an AzureML module. The spec should be in YAML file format.

### Module Definition

| Name                | Type                                                     | Required | Description                                                  |
| ------------------- | -------------------------------------------------------- | -------- | ------------------------------------------------------------ |
| amlModuleIdentifier | [ModuleIdentifier](#ModuleIndentifier)                   | Yes      | Identifies a specific version of the module.                 |
| jobType             | String                                                   | No       | Defines job type of the module. Could be `basic`, `mpi`, `hdinsight`, `parallel`. Defaults to `basic` if not specified. |
| description         | String                                                   | No       | Detailed description of the module. |
| metadata            | [MetaData](#MetaData)                                    | No       | A metadata structure to store additional information for the module. |
| isDeterministic     | Boolean                                                  | No       | Specify whether the module will always generate the same result when given the same input data. Defaults to `True` if not specified. Typically for modules which will load data from external resources, e.g. Import data from a given url, should set to `False` since the data to where the url points to may be updated. |
| inputs              | List<[InputPort](#InputPort) or [Parameter](#Parameter)> | No       | Defines input ports and parameters of the module.            |
| outputs             | List<[OutputPort](#OutputPort)>                          | No       | Defines output ports of the module.                          |
| implementation      | [Implementation](#Implementation)                        | Yes      | Defines the environment and command to run the module.       |
| version             | String                                                   | No       | Specify the version of the schema of spec. Current version is `microsoft.com/azureml/module/v2beta1` |



### ModuleIdentifier

ModuleIdentifier is a global unique identifier to a specific version of a module.

| Name          | Type    | Required | Description                                                  |
| ------------- | ------- | -------- | ------------------------------------------------------------ |
| namespace     | String  | No      | Refer to [Namespace](#Namespace) for details.                |
| moduleName    | String | Yes      | Name of the module. |
| moduleVersion | String  | Yes      | Version of the module. Could be arbitrary text, but it is recommended to follow the [Semantic Versioning](https://semver.org/) specification. |

#### Namespace

Namespace is used to avoid naming conflicts of modules created by different teams or organizations. It is recommended to follow below specification. If namespace is not specified in spec, AzureML workspace name will be used as default value.

```
$ORGANIZATION_NAME/$MODULE_PATH
```

* `ORGANIZATION_NAME` is the domain name of the organization, e.g. `microsoft.com`, `my-awesome-modules.com`.
* `MODULE_PATH` is the name organized in paths inside the organization. The path could contain multiple segments separated by `/`. The level depth is not restricted, the organization can define any depth of level to organize their own modules.
* Only lowercase letters `a-z`, `-` are allowed in the version string. `.` is only allowed in `ORGANIZATION_NAME` . `/` is only allowed to be used as separator.

Sample namespaces:

```
microsoft.com/office/smart-compose
my-awesome-modules.com/ner-bert
```



### MetaData

Metadata defines additional information for the module. Currently supports only one field `annotations`.

| Name        | Type                        | Required | Description                                       |
| ----------- | --------------------------- | -------- | ------------------------------------------------- |
| annotations | [Annotations](#Annotations) | No       | Refer to [Annotations](#Annotations) for details. |



### Annotations

Defines additional information for the module. Currently supported properties are listed below.

| Name        | Type         | Required | Description                                                  |
| ----------- | ------------ | -------- | ------------------------------------------------------------ |
| tags  | List<String> | No       | A list of tags to describe the category of the module. Each tag should be one word or a short phrase to describe the module, e.g. `Office`, `NLP`, `ImageClassification`. |
| contact     | String       | No       | The contact info of the module's author. Typically contains user or organization's name and email. e.g. `AzureML Studio Team <stcamlstudiosg@microsoft.com>`. |
| helpDocument | String       | No       | The url of the module's documentation. The url is shown as a link on AzureML Designer's page. |



### InputPort

Defines an input port of the module.

| Name        | Type                    | Required | Description                                                  |
| ----------- | ----------------------- | -------- | ------------------------------------------------------------ |
| name        | String                  | Yes      | Name of the input port. This field is used for program logic and cannot be duplicated with other inputs of the module. The name should not contain "_", "/", "@", "[", "]" since they are reserved for internal usage in the future. |
| type        | String or  List<String> | Yes      | Defines the data type(s) of this input port. Refer to [Data Types for Ports](#Data Types for Ports) for details. |
| optional    | Boolean                 | No       | Indicates whether this input is an optional port. Defaults to `False` if not specified. |
| description | String                  | No       | Detailed description to the input port.      |



### Parameter

Defines a parameter of the module.

| Name        | Type    | Required | Description                                                  |
| ----------- | ------- | -------- | ------------------------------------------------------------ |
| name        | String  | Yes      | Name of the parameter. This field is used for program logic and cannot be duplicated with other inputs of the module. The name should not contain "_", "/", "@", "[", "]" since they are reserved for internal usage in the future. |
| type        | String  | Yes      | Defines the type of this data. Refer to [Data Types for Parameters](#Data Types for Parameters) for details. |
| optional    | Boolean | No       | Indicates whether this input is optional. Default value is `False`. |
| default     | Dynamic | No       | The default value for this parameter. The type of this value is dynamic. e.g. If `type` field in Input is `Integer`, this value should be `Inteter`. If `type` is `String`, this value should also be `String`. This field is optional, defaults to `null` or `None` if not specified. |
| description | String  | No       | Detailed description to the parameter.                       |
| min         | Numeric | No       | The minimum value that can be accepted. This field only takes effect when `type` is `Integer` or `Float`. Specify `Integer` or `Float` values accordingly. |
| max         | Numeric | No       | The maximum value that can be accepted. Similar to `min`.    |
| options     | List    | No       | The acceptable values for the parameter. This field only takes effect when `type` is `Enum`. |



### OutputPort

Defines an output port of the module.

| Name        | Type   | Required | Description                                                  |
| ----------- | ------ | -------- | ------------------------------------------------------------ |
| name        | String | Yes      | Name of the output port. This field is used for program logic and cannot be duplicated with other inputs of the module. The name should not contain "_", "/", "@", "[", "]" since they are reserved for internal usage in the future. |
| type        | String | Yes      | Defines the data type(s) of this output port. Refer to [Data Types for Ports](#Data Types for Ports) for details. |
| description | String                  | No       | Detailed description to the output port.      |



### Implementation

This block defines how and where to run the module code.

| Name      | Type                    | Required | Description                                                  |
| --------- | ----------------------- | -------- | ------------------------------------------------------------ |
| container | [Container](#Container) | No[^1]   | Defines the required information for running. (For basic and mpi modules)               |
| hdinsight | [HDInsight](#HDInsight) | No[^1]   | Defines the required information for running. (For HDInsight modules) |
| parallel  | [Parallel](#Parallel)   | No[^1]   | Defines the required information for running. (For parallel modules) |
| os        | String                  | No       | Defines the operating system the module running on. Could be `windows` or `linux`. Defaults to `linux` if not specified. |

[^1]: Specify either one according to `jobType`. Could not specify multiple or none.



### Container

| Name           | Type                                                         | Required | Description                                                  |
| -------------- | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| amlEnvironment | [AmlEnvironment](#AmlEnvironment) or [AmlEnvironmentReference](#AmlEnvironmentReference) | No[^1]   | Specify the runtime environment for the module to run. Refer to [here](samples/modules/basic-modules/environment) for details. |
| image          | String                                                       | No[^1]   | Specify the docker image path. Refer to [here](samples/modules/basic-modules/environment) for details. |
| command        | List<String>                                                 | Yes      | Specify the command to start to run the module code.         |
| args           | List                                                         | No       | Specify the arguments used along with `command`. This list may consist place holders of Inputs and Outputs. See [CLI Argument Place Holders](#CLI Argument Place Holders) for details. |

[^1]: Specify either one from `amlEnvironment` or `image`. Not allowed to specify both or none.



### AmlEnvironment

An AmlEnvironment defines the runtime environment for the module to run, it is equivalent with the definition of the [Environment class in python SDK](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.environment%28class%29?view=azure-ml-py).

| Name   | Type          | Required | Description                                                  |
| ------ | ------------- | -------- | ------------------------------------------------------------ |
| docker | DockerSection | No       | This section configures settings related to the final Docker image built to the specifications of the environment and whether to use Docker containers to build the environment. |
| python | PythonSection | No       | This section specifies which Python environment and interpreter to use on the target compute. |

#### DockerSection

| Name      | Type   | Required | Description                                                  |
| --------- | ------ | -------- | ------------------------------------------------------------ |
| baseImage | String | No       | The base image used for Docker-based runs. Example value: "ubuntu:latest". If not specified, will use `mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04` by default. |

#### PythonSection

| Name                  | Type              | Required | Description                                                  |
| --------------------- | ----------------- | -------- | ------------------------------------------------------------ |
| condaDependenciesFile | String            | No       | The path to the conda dependencies file to use for this run. If a project contains multiple programs with different sets of dependencies, it may be convenient to manage those environments with separate files. The default is None. |
| condaDependencies     | CondaDependencies | No       | Same as `condaDependenciesFile`, but it is specifies the conda dependencies using an inline dictionary rather than a separated file. |



### AmlEnvironmentReference

It is also available to specify the runtime environment using a reference to an pre-registered amlEnvironment. The environment must be registered to the workspace before registering the module. In the module spec, specify the environment name and version to refer to the environment.

> **NOTE**:
>
> 1. The environment configuration will be retrieved from workspace and stored with the module when registering to workspace. Thus, when the environment got updated, it will not apply to the modules unless reregister the modules.
>
> 2. Currently not supported. Use [AmlEnvironment](#AmlEnvironment) instead.



| Name    | Type   | Required | Description                                                                |
|---------|--------|----------|----------------------------------------------------------------------------|
| name    | String | Yes      | Specify the environment name which have been registered to the workspace.  |
| version | String | No       | Specify the environment version. If not specified, use the latest version. |



### HDInsight

This section is used only for HDInsight modules.

| Name      | Type         | Required | Description                                                  |
| --------- | ------------ | -------- | ------------------------------------------------------------ |
| file      | String       | Yes      | File containing the application to execute, can be a python script or a jar file. It's a relative path to the snapshot folder. |
| files     | List<String> | No       | Files to be used in HDInsight session. Specify relative paths to the snapshot folder. |
| className | String       | No       | Main class name when main file is a jar.                     |
| jars      | List<String> | No       | Jar files to be used in HDInsight session. Specify relative paths to the snapshot folder. |
| pyFiles   | List<String> | No       | Python files to be used in HDInsight session. Specify relative paths to the snapshot folder. |
| archives  | List<String> | No       | Archives to be used in HDInsight session. Specify relative paths to the snapshot folder. |
| args      | List         | No       | Specify the arguments used along with `file`. This list may consist place holders of Inputs and Outputs. See [CLI Argument Place Holders](#CLI Argument Place Holders) for details. |



### Parallel

This section is used only for parallel modules. Refer to [here](samples/modules/parallel-modules) for details.

| Name           | Type                              | Required | Description                                                  |
| -------------- | --------------------------------- | -------- | ------------------------------------------------------------ |
| amlEnvironment | [AmlEnvironment](#AmlEnvironment) | No[^1]   | The environment in where the entry script runs. Some packages must be included to the environment to enable the parallel module run. Refer to [here](samples/modules/basic-modules/environment) for details. |
| image          | String                            | No[^1]   | Specify the docker image path. Refer to [here](samples/modules/basic-modules/environment) for details. |
| inputData      | String or List<String>            | Yes      | The input(s) provide the data to be split into mini_batches for parallel execution. Specify the name(s) of the corresponding input(s) here. |
| outputData     | String                            | Yes      | The output for the summarized result that generated by the user script. Specify the name of the corresponding output here. |
| entry          | String                            | Yes      | The user script to process mini_batches.                     |
| args           | List                              | No       | The arguments passed to the user script. This list may consist place holders of Inputs and Outputs. See [CLI Argument Place Holders](#CLI Argument Place Holders) for details. No need to set information about `inputData` and `outputData` here. |

[^1]: Specify either one from `amlEnvironment` or `image`. Not allowed to specify both or none.



### Data Types

Data Type is a short word or phrase that describes the data type of the Input or Output.

#### Data Types for Ports

Designer allows its user to connect an OutputPort to another module's InputPort that with the same data type.

Data type for a port could be an arbitrary string (except `<` and `>`), but it is strongly recommended to follow `PascalCase` style.

#### Data Types for Parameters

| Name    | Description                                                  |
| ------- | ------------------------------------------------------------ |
| String  | Indicates that the input value is a string.                  |
| Integer | Indicates that the input value is an integer.                |
| Float   | Indicates that the input value is a float.                   |
| Boolean | Indicates that the input value is a boolean value.           |
| Enum    | Indicates that the input value is a enumerated (limited list of) String values. |



### CLI Argument Place Holders

When invoking from a CLI interface, the arguments are specified with placeholders. The placeholders will be replaced with the actual value when running.

Example:

```yaml
args: [
   --trained-model-dir, {inputPath: Trained model},
   --test-feature-dir, {inputValue: Input test data},
   --no-cuda, {inputValue: No cuda},
   --local-rank, {inputValue: Local Rank},
   --test-batch-size, {inputValue: Test Batch Size},
   --output-eval-dir, {outputPath: Output evaluation results},
]
```

Placeholder is a dictionary that:

* The key may be either `inputValue` for inferring values from Parameters, `inputPath` for inferring values from Input Ports, or `outputPath` for Output Ports.
* The value should be the `name` of Input or Output.





### Appendix: Diff between AzureML module spec and Kubeflow component spec

| Path                                    | AzureML Module Spec                                          | Kubeflow Component Spec                                      |
| --------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| name                                    | -                                                            | Optional, only used as human readable name                   |
| amlModuleIdentifier                     | Required, a global unique identifier to a specific version of a module. | -                                                            |
| jobType                                 | Optional (use default value when missing), specify module type to determine compute target type to run the module. | -                                                            |
| description                             | Optional, human readable description                         | Optional, human readable description                         |
| metadata/annotations                    | Optional, set arbitrary key-value pairs such as tags, projectUrl, documentUrl, etc. | Optional, translated to Kubernetes annotations when the component task is executed on Kubernetes. |
| isDeterministic                         | Optional (use default value when missing)                    | -                                                            |
| inputs                                  | Optional, Defines the input ports and parameters             | Optional, Defines the inputs (no concept for port/parameters) |
| outputs                                 | Optional, Defines the output port                            | Optional, Defines output                                     |
| implementation/container/amlEnvironment | Required if image not specified                              | -                                                            |
| implementation/container/image          | Required if environment not specified                        | Required, the name of the docker image.                      |
| implementation/container/command        | Required, specifies the command to start to run the module code. | Optional, specifies the command to start to run the code. If not specified, the docker image's ENTRYPOINT will be used. |
| implementation/container/args           | Optional, arguments to the entrypoint.                       | Optional, arguments to the entrypoint.                       |