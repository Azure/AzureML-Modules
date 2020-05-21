# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

try:
    import yaml
except ImportError:
    raise ValueError('No PyYAML installed. Plese install using `pip install PyYAML`')

if not hasattr(yaml, 'load'):
    raise ValueError('No PyYAML installed. Plese install using `pip install PyYAML`')

from pathlib import Path


def iter_additional_files(spec_file):
    with open(spec_file) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)

    yield from spec.get('implementation', {}).get('container', {}).get('additionalFiles')


if __name__ == '__main__':
    for f in iter_additional_files('module_spec.yaml'):
        path = Path(f)
        if path.is_absolute():
            raise ValueError(f'Invalid additional file {path}: Only accept relative paths. (relative to the module spec file.)')

        if not path.exists():
            raise ValueError(f'Additional file {path} does not exist')

        Path(path.name).symlink_to(path)
        print(f'Created symbol link to {path}.')

    print('Done.')
