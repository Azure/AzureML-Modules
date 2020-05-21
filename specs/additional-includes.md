# Additional includes

By default, The folder containing the module spec file will be treated as the base folder of the module running environment (a.k.a the *snapshot*). However, sometimes some common libraries lays on other top level folders. In this case, use *additional includes* to set the additional file or folders used by the module. The file or folders in additional includes will be copied to the snapshot folder by the module-cli when registering the module.

To specify additional includes, add a `{spec_file_name}.additional_includes`  file next to the module spec file. For example, if the module spec file is named `module_spec.yaml`, the additional includes file should be named `module_spec.additional_includes`.

As an example, for the following folder structure:

```
src/
  python/
    library1/
      hello.py
    library2/
      greetings.py
assets/
  LICENSE
module_entry/
  module_spec.additional_includes
  module_spec.yaml
  run.py
```

Inside the `module_spec.additional_includes` file:

```yaml
../src/python/library1
../src/python/library2
../assets/LICENSE
```

When packing snapshot, the contents inside the snapshot will be:

```
module_spec.yaml
run.py
library1/
  hello.py
library2/
  greetings.py
LICENSE
```

### Notes

* Additional includes file should be a plain text file, place each item in one line. The line break could be either `\r\n` or `\n`, but it is recommended to use `\n`.

* Specified additional file (or folder) will be copied directly into the base folder of snapshot. No parent folders included.

* Each item in the additional include file:

  * Could either be a file or a folder. In the sample above, `../src/python/library1` and `../src/python/library2` are folders, while `../assets/LECENSE` is a file.

  * Must be specified with relative file path from the folder containing the module spec file. Absolute file path not accepted.

    * Good: `../src`
    * Bad: `/`, `C:`

  * Recommend to contain a specific folder or file name.

    * Recommended: `../src`, `../src/python/library1`, `../assets/LICENSE`
    * Not recommended: `../../`, `~`, `/`

  * Recommend to use linux-style path. Windows-style path will not work properly on Linux platforms.

    * Recommended: `../src/python/library1`
    * Not recommended: `..\src\python\library1`.


It would be helpful to test run the module before the module get registered to a workspace. For local testing, it is convinent to setup some symbol links in the snapshot base folder for additional files. We have created [a sample python script](samples/modules/basic-modules/additional-includes/module_entry/setup_env.py) to do the job automatically.


### Sample module

Refer to [here](samples/modules/basic-modules/additional-includes/) for a sample module.
