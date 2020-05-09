#!/usr/bin/env python3
"""The test file."""
from ctypes import CDLL, cast, c_char_p
from typing import Optional, Union
from subprocess import run
from os.path import isfile

from piran import Random, build, compute, piran_verbose
from log import is_ms_windows, Flag

SPEED_TEST_DIGITS: int = 10_000 # normally less than a second
TEST_DIGITS: int = 100_000 # normally less than a minute
CCharPointer =  Optional[bytes]
CString = bytes

piran_verbose = True

if is_ms_windows() is True:
    raise OSError("C library not compiled yet for Windows")

if isfile("./pi.so") is False:
    build()

verbose = Flag('v', '--verbose')

if isfile("./pi") is False:
    compute(10_000)

r = Random(cursor="cursor_7f04414ce640")
print("r.uint", *(r.uint for i in range(3)))
print("r.sint", *(r.sint for i in range(3)))
print(r.cursor)
print()

r2 = Random()
print(r2._cursor_file_name)
print("r2.uint", *(r2.uint for i in range(3)))
print("r2.sint", *(r2.sint for i in range(3)))
print(r2.cursor)
r2.close()
