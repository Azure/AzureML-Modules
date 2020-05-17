# Additional includes

By default, The folder containing the module spec file will be treated as the base folder of the module running environment (a.k.a the *snapshot*). However, sometimes some common libraries lays on other top level folders. In this case, specify `additionalIncludes` to include additional file or folders to the snapshot. The file or folders in `additionalIncludes` will be copied to the snapshot folder by the module-cli when registering or upgrading the module.

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
  module_spec.yaml
  run.py
```

In the module spec file, specify additional includes like:

```yaml
implementation:
  container:
    additionalIncludes:
      - ../src/python/library1
      - ../src/python/library2
      - ../assets/LICENSE
    command: [python, run.py]
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

* `additionalIncludes` could either accept one or a list of items thus could accept multiple additional includes.

  ```yaml
  # One item (specify the item directly)
  implementation:
    container:
      additionalIncludes: ../assets/LICENSE
  
  # One item (specify as a list contains only one item)
  implementation:
    container:
      additionalIncludes:
        - ../assets/LICENSE
  
  # Multiple items (specify as a list)
  implementation:
    container:
      additionalIncludes:
        - ../src/python/library1
        - ../src/python/library2
        - ../assets/LICENSE
  ```

* Each item in `additionalIncludes` could either be a file or a folder. In the sample above, `../src/python/library1` and `../src/python/library2` are folders, while `../assets/LECENSE` is a file.

* Each item in `additionalIncludes` must be specified with relative file path from the folder containing the module spec file. Absolute file path not accepted.

* Specified additional file (or folder) will be copied directly into the base folder of snapshot. No parent folders included.

It would be helpful to test run the module before the module get registered to a workspace. For local testing, it is convinent to setup some symbol links in the snapshot base folder for additional files. We have created [a sample python script](module_entry/setup_env.py) to do the job automatically.

