#!/usr/bin/env python3
"""The test file."""
from ctypes import CDLL, cast, c_char_p
from typing import Optional, Union
from subprocess import run
from os.path import isfile

from piran import Random, build, compute
from log import is_ms_windows, Flag

SPEED_TEST_DIGITS = 10_000 # normally less than a second
TEST_DIGITS = 100_000 # normally less than a minute
CCharPointer =  Optional[bytes]
CString = bytes

piran_verbose = True

if is_ms_windows() is True:
    raise OSError("C library not compiled yet for Windows")

if isfile("./pi.so") is False:
    build()

piran_verbose = Flag('v', '--verbose').exists()

if isfile("./pi") is False:
    print("Computing hundred thousand decimals of π.")
    compute(TEST_DIGITS)

def test(r: Random) -> None:
    print(f"""{r._cursor_file_name}:{r.get_cursor()}
uint {tuple(r.uint(100) for i in range(3))}
sint {tuple(r.sint(-100, 100) for i in range(3))}
:{r.get_cursor()}
""")

r = Random(cursor="cursor_7f04414ce640")
test(r)

r2 = Random()
test(r2)
test(r2)
r2.close()
