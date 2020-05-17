import argparse
from azureml.studio.core.logger import module_logger as logger
from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, save_data_frame_to_directory

PACKAGE_NAME = 'azureml-designer-tutorial-modules'
VERSION = '0.0.1'

from mpi4py import MPI

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

    logger.info(f"Hello world MPI from {PACKAGE_NAME} {VERSION}")

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    str_param = args.string_parameter
    int_param = args.int_parameter
    bool_param = args.boolean_parameter
    enum_param = args.enum_parameter

    logger.debug(f"Received parameters:")
    logger.debug(f"    {str_param}")
    logger.debug(f"    {int_param}")
    logger.debug(f"    {bool_param}")
    logger.debug(f"    {enum_param}")

    if rank > 0:
        logger.debug(f"I'm rank {rank}/{size}, wait for data.")
        data = comm.recv(source=0, tag=rank)
        logger.debug(f"Received shape of loaded DataFrame: {data} ")
    else:
        logger.debug(f"I'm rank 0/{size}, load and dump.")

        logger.debug(f"Input path: {args.input_path}")
        data_frame_directory = load_data_frame_from_directory(args.input_path)

        logger.debug(f"Shape of loaded DataFrame: {data_frame_directory.data.shape}")

        logger.debug(f"Output path: {args.output_path}")
        save_data_frame_to_directory(args.output_path, data_frame_directory.data)

        for i in range(1, size):
            data = data_frame_directory.data.shape
            logger.debug(f"Send shape to rank {i}")
            comm.send(data, dest=i, tag=i)

