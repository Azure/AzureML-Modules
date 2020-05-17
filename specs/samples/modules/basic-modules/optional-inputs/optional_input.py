import argparse

PACKAGE_NAME = 'azureml-designer-tutorial-modules'
VERSION = '0.0.1'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-path',
        help='The first input directory.',
    )
    parser.add_argument(
        '--optional-input-path',
        help='The second input directory.',
    )
    parser.add_argument(
        '--string-param', type=str,
        help='A string parameter.',
    )
    parser.add_argument(
        '--optional-string-param', type=str,
        help='An optional string parameter.',
    )
    parser.add_argument(
        '--int-param', type=int,
        help='An int parameter.',
    )
    parser.add_argument(
        '--optional-int-param', type=int,
        help='An optional int parameter.',
    )
    parser.add_argument(
        '--output-path',
        help='The output directory.',
    )

    args, _ = parser.parse_known_args()

    print(f"Sample module from {PACKAGE_NAME} {VERSION}")

    print(f"Received parameters:")
    for key in [
        'input_path', 'optional_input_path',
        'string_param', 'optional_string_param',
        'int_param', 'optional_int_param',
        'output_path'
    ]:
        print(key, getattr(args, key))
