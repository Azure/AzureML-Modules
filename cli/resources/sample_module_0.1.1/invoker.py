# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import sys


def execute(args):
    print('args: ({} items)'.format(len(args)))
    print('--------------------------------------------')
    for arg in args:
        print(arg)
    print('--------------------------------------------')


if __name__ == '__main__':
    execute(sys.argv)
