# Ignore files when creating snapshot

It is good to exclude some files (e.g.  `__pycache__`) when creating the module snapshot. Put an `.amlignore` or `.gitignore` file to to base folder of the module snapshot (in other words, the folder which contains the module spec yaml file) to ignore the uneeded files. Refer to [the AzureML doc](https://docs.microsoft.com/en-us/azure/machine-learning/concept-azure-machine-learning-architecture#snapshots) for detailed introduction of `.amlignore`.

## Shared .amlignore file

Besides putting an `.amlignore` file in the base folder of each module, it is also supported to create a shared `.amlignore` file, and specify the path to the shared `.amlignore` file when registering the module.

```bash
az ml module register --spec-file=path/to/module/spec.yaml --amlignore-file=path/to/shared/.amlignore
```

The shared `.amlignore` file will be copied to the module snapshot. If there is already an `.amlignore` file in the module snapshot folder, the contents of the two `.amlignore` files will be merged.

## Set a default shared .amlignore file

Instead of specifiying the `--amlignore-file` to every module register command, it is also possible to set the default `.amlignore` file using the following command:

```bash
az configure --defaults module_amlignore_file=/path/to/shared/.amlignore
```

By this setting, the shared `.amlignore` will be automatically applied when registering modules. The register command could be simplified to:

```bash
az ml module register --spec-file=path/to/module/spec.yaml
```

## Limitations

Currently,  `.amlignore` files located in subfolders of snapshot will not take effect.

