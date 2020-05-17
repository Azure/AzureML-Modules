import argparse
import logging
import torch

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

PACKAGE_NAME = 'azureml-designer-tutorial-modules'
VERSION = '0.0.1'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-path',
        help='The input directory.',
    )
    parser.add_argument(
        '--string-parameter', type=str,
        help='A string parameter.',
    )
    parser.add_argument(
        '--int-parameter', type=int,
        help='An int parameter.',
    )
    parser.add_argument(
        '--boolean-parameter', type=str,
        help='A boolean parameter.',
    )
    parser.add_argument(
        '--enum-parameter', type=str,
        help='A enum parameter.',
    )
    parser.add_argument(
        '--output-path',
        help='The output directory.',
    )

    args, _ = parser.parse_known_args()

    logger.info(f"Hello world with gpu docker image from {PACKAGE_NAME} {VERSION}")
    logger.info(f"Gpu count of this compute: {torch.cuda.device_count()}")

    str_param = args.string_parameter
    int_param = args.int_parameter
    bool_param = args.boolean_parameter
    enum_param = args.enum_parameter

    logger.debug(f"Received parameters:")
    logger.debug(f"    {str_param}")
    logger.debug(f"    {int_param}")
    logger.debug(f"    {bool_param}")
    logger.debug(f"    {enum_param}")

    logger.debug(f"Input path: {args.input_path}")

    logger.debug(f"Output path: {args.output_path}")
