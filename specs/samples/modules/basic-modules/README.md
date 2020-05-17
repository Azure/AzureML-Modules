# Basic Module

To define a module, create a YAML file format contains the following parts:

* Basic identification information (`amlModuleIdentifier`).
* The additional `metadata` and  `description` of the module.
* The interface (`inputs` and `outputs`) of the module.
* The `implementation` of the module including the definition of the module's running environment and the command to invoke the module.

See also:

* [The module spec definition document](../../../module-spec-definition.md)
* [A sample yaml to get started](environment/conda-inline)

## Advanced topics

After getting started, here are some advanced topics:

* [Set module running environments](environment)
* [Add additional files into the module code base](additional-includes)
* [Use optional input ports or params](optional-inputs)
* [Modules used in office smart-compose](office)

