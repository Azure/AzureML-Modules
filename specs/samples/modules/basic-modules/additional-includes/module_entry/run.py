# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import sys
sys.path.append('library2.zip')

from library1.hello import say_hello
from library2.greetings import greetings


if __name__ == '__main__':
    say_hello()
    greetings()
