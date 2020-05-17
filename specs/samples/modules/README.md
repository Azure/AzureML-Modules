# Sample Module

This directory contains some sample modules which help user get started.

| Module Folder               | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| [basic-modules/environment/conda-file](basic-modules/environment/conda-file)      | A hello world sample to create a module with an external Conda file. |
| [basic-modules/environment/conda-inline](basic-modules/environment/conda-inline)     | A hello world sample to create(basic-modules/environment/conda-inline-gpu) a module with inline Conda definitions. |
| [basic-modules/environment/conda-inline-gpu](basic-modules/environment/conda-inline-gpu) | A hello world sample to create a module with inline Conda definitions and AzureML GPU base image specified. |
| [basic-modules/environment/docker-cpu](basic-modules/environment/docker-cpu)       | A hello world sample to create a module with a cpu docker image. The corresponding Dockerfile could be found under [sample_dockerfiles](../sample_dockerfiles). |
| [basic-modules/environment/docker-gpu](basic-modules/environment/docker-gpu)       | A hello world sample to create a module with a gpu docker image. The corresponding Dockerfile could be found under [sample_dockerfiles](../sample_dockerfiles). |
| [basic-modules/optional-inputs](basic-modules/optional-inputs)             | A sample to create a module with optional inputs and parameters. |
| [basic-modules/additional-includes](basic-modules/additional-includes)         | A sample to create a module with *additionalIncludes* property to include some extra files/folders. |
| [basic-modules/office/compliant-file-rename](basic-modules/office/compliant-file-rename)       | A real module sample that scrubbing the exception message for compliance requirements. |
| [basic-modules/office/merge-n-files-together](basic-modules/office/merge-n-files-together)      | A real module sample that merging files into one.            |
| [mpi-modules/mpi-hello-world](mpi-modules/mpi-hello-world)                  | A hello world sample to create a MPI module.                 |
| [mpi-modules/mpi-train-mnist](mpi-modules/mpi-train-mnist) | A MNIST image classicification module with MPI traing. |
| [parallel-modules/parallel-copy-files](parallel-modules/parallel-copy-files)            | A hello world sample for parallel modules which copies files from input to output. |
| [parallel-modules/parallel-copy-files-docker](parallel-modules/parallel-copy-files-docker)            | A hello world sample for parallel modules that uses docker environment, which copies files from input to output. |
| [parallel-modules/parallel-score](parallel-modules/parallel-score) | A module to perform parallel score with the MNIST image classication model. |


Each module folder under this directory is a valid source of module to be registered with Azure CLI. The module specification of each module is `module_spec.yaml`.

Instruction of Azure CLI can be found in [this tutorial](../../../cli/walk-through.md).

## Register from local

Download the folder of sample module (e.g. `basic-modules/environment/additional-includes`) to local and register module like:

```bash
az ml module register --spec-file=additional-includes/module_spec.yaml
```

## Register from Devops artifacts

Most of the samples in this folder have been published as Devops artifacts [here](https://msdata.visualstudio.com/AzureML/_build/results?buildId=13856068&view=artifacts&type=publishedArtifacts). You can use the download link of these artifacts (e.g. [helloworld-conda-inline](https://msdata.visualstudio.com/AzureML/_apis/build/builds/13910313/artifacts?artifactName=helloworld-conda-inline&api-version=5.1&%24format=zip)), and register module like:

```bash
az ml module register --package-zip="https://msdata.visualstudio.com/AzureML/_apis/build/builds/13910313/artifacts?artifactName=helloworld-conda-inline&api-version=5.1&%24format=zip" --spec-file=module_spec.yaml
```

Note: `additionalIncludes` property is not supported for registering from Devops artifacts.

## Register from GitHub

There are several excellent modules available on GitHub.

### [Microsoft Recommenders](https://github.com/microsoft/recommenders/tree/master/reco_utils/azureml/azureml_designer_modules)

Here are the list of modules that available in Recommenders repository.

| Module Name         | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| Stratified Splitter | Python stratified splitter from Recommenders repo: https://github.com/Microsoft/Recommenders. |
| SAR Training        | SAR Train from Recommenders repo: https://github.com/Microsoft/Recommenders. |
| SAR Scoring         | SAR Scoring from Recommenders repo: https://github.com/Microsoft/Recommenders. |
| MAP                 | "Mean Average Precision at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders. |
| nDCG                | Normalized Discounted Cumulative Gain (nDCG) at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders. |
| Precision at K      | Precision at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders. |
| Recall at K         | Recall at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders. |

For example, module "Stratified Splitter" can be registered using

```bash
az ml module register --spec-file=https://github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/stratified_splitter.yaml
```

### Azure ML Internal Custom Modules

### [Wide and deep recommender](https://github.com/hirofumi-s-friends/CustomModules/tree/master/azureml-custom-module-examples/wide-and-deep-recommender)

Here are the list of modules for wide and deep recommender scenarios.

| Module Name                                       | Description                                                  |
| ------------------------------------------------- | ------------------------------------------------------------ |
| Convert Multi Parquet Files to DataFrameDirectory | Convert the multiple parquet files to the DataFrameDirectory format. |
| MPI Train Wide and Deep Recommender               | Train a recommender based on Wide & Deep model.              |
| Parallel Score Wide and Deep Recommender          | Score a dataset using the Wide and Deep recommendation model. |

For example, module "Convert Multi Parquet Files to DataFrameDirectory" can be registered using

```bash
az ml module register --spec-file=https://github.com/hirofumi-s-friends/CustomModules/blob/master/azureml-custom-module-examples/wide-and-deep-recommender/convert_multi_parquet_to_dfd.yaml
```
