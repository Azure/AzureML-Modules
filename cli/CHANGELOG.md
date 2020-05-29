## 0.1.0.14574253

* Add support for the new `.additional_includes` file. Refer to [this doc](../specs/additional-includes.md) for details.
* Added `--amlignore-file` to specify a common `.amlignore` file when registering module. Also added `az configure --defaults module_amlignore_file=/path/to/amlignore` to set the default `.amlignore` file. Refer to [this doc](../specs/ignore-files.md) for details.
* Improved performance for `az ml module validate-spec` command escepcially when the module contains a large amount of files.



## 0.1.0.13766063

* Added a progress indicator for registering from local resources.
* Refined module download progress indicator display.
* Internal usage: Add support to override API endpoint using environment variable.
* Fixed the following bugs:
  * Fixed: Script entry with an absolute path will fail to register on windows platforms.
  * Fixed: The status indicator not cleared even when the operation has been done.



## 0.1.0.13405526

* Add more descriptions and examples to the `-h` output to each command.
* Removed "Contact", "Description" from module list view to prevent the table from getting too wide to fit into the screen.
* Fixed a corner case bug related to `additionalIncludes` which would cause register failure.



## 0.1.0.13349440

* Implemented `az ml module download` command to download module snapshot and optionally download module spec as a yaml file.
* Newly add `az ml module validate-spec` to validate the module spec before registering.
* Optimized display of module details page. (Add "All versions", etc.)
* Optimized performance by:
  * Optimized the register module logic, avoid uploading large files when validating module spec.
  * Fixed a buggy code which would consume cpu time when displaying the status indicator.
* Fixed issues in `additionalIncludes` when handling relative folder that without a specific name like  `../../` .



## 0.1.0.13082891

* Added support to register modules specs that contains `additionalIncludes`.
* Added a status indicator while excuting the CLI command to show the current status.
* Fixed known issues of last release:
  * Fixed: Columns in table view will be alphabetically sorted, which is not expected.
  * Fixed: Error message does not display in red.
  * Fixed: Warning message does not shown by default.



## 0.1.0.12943393

* Changed to new souce code, from `o16n` to `e13n`.
* Added `User-Agent` to http header to enable telemetry on server side.
* Known issues due to code base change:
  * Columns in table view will be alphabetically sorted, which is not expected.
  * Error message does not display in red, which is hard to read.
  * Warning message does not shown by default. (Could be shown when `--debug` parameter specified.)



## 0.1.0.12857466

* Merged `az ml module upgrade` to `az ml module register` commands.
* Updated default workspace and resource group setting. (to align with other `az ml` commands).
  * From `az configure --defaults aml_workspace=xxx group=xxx`
  * To `az ml folder attach -w xxx -g xxx`
    
    > Note: The new way only only take affect for one folder. When changed to another folder, need to set default workspace again.



## 0.1.0.12695397

* Changed to a part of azure-cli-ml (the `az ml` command set). All `module` commands moved to `az ml module`.
* To be aligned with other `az ml` commands, changed positional args to named args.
  e.g.
    `module show MODULE_NAME` becomes `az ml module show --name MODULE_NAME`.
	`module register FILE_OR_URL` becomes `az ml module register --spec-file=/path/to/spec.yaml`.
  The flag like `--name` (or a short form `-n`) / `--spec-file` must be specified in the new version CLI.
* Added support to register modules from a DevOps build drop.
* Added new version check functionality. A warning message (with upgrade guidance) will be shown if user is using an older version of CLI.
* Added more user guidance when user operating with non-default version of a module.
  - When doing a `module upgrade` without `--set-as-default-version` flag set, a warning message will be shown to notify the user that the default version is not changed.
  - When displaying modules, default version will be shown along with the version to notify the user if they differs. (TO BE DISCUSSED)
* Display RequestId when error raised from server side to help troubshooting.
* Optimized the output content for `--output json` format, which is the default format of azure-cli-ml. Hide unnecessary attributes for the end user.
* Optimized the table output format by wrapping long text to multilines. Would be helpful for when displaying modules with long descriptions.
