"""The PiRan module."""
from os.path import isfile, getsize as get_len_of_file, abspath, dirname
from os import remove
from sys import maxsize, stdout, stderr
from ctypes import CDLL, cast as c_cast, c_char_p
from typing import Optional, IO, Union, cast

__author__ = "Firefnix"
__license__ = "GPL-3-or-later"
__version__ = "1.0"

location = abspath(dirname(__file__))
del dirname, abspath

def _required_digits(max_value: int) -> int:
    return len(str(max_value + 1))

def _assert_uint(arg: object) -> None:
    if (not isinstance(arg, int)) or arg < 0:
        raise ValueError(f"Must be an positive integer (is {arg})")

class Random:
    """Use random numbers, bytes and chars."""

    def __init__(self, pi_file_name: str = "pi",
        cursor: Union[str, int, None] = None) -> None:

        self._cursor_file_name: str
        if isfile(pi_file_name) is False:
            raise FileNotFoundError(f"{pi_file_name} not found")

        if isinstance(cursor, str) is True:
            self._cursor_file_name = cast(str, cursor)
        else:
            self._cursor_file_name = f"cursor_{hex(id(self))[2:]}"
            self.set_cursor(cast(int, cursor or 0))
        self._pi_file_name: str = pi_file_name

    def get_cursor(self) -> int:
        """Position in the PI file."""
        with open(self._cursor_file_name) as cursor_file:
            return int(cursor_file.read())

    def set_cursor(self, value: int) -> int:
        """Save the cursor value in cursor_file."""
        _assert_uint(value)
        with open(self._cursor_file_name, "w") as cursor_file:
            cursor_file.write(str(value))
        return value

    def add_to_cursor(self, value: int) -> int:
        """Return the changed cursor"""
        self.set_cursor(self.get_cursor() + value)
        return self.get_cursor()

    def close(self) -> int:
        """Delete the cursor file."""
        cursor = self.get_cursor()
        remove(self._cursor_file_name)
        return cursor

    def digits(self, length: int) -> str:
        with open(self._pi_file_name) as pi_file:
            return pi_file.read()[self.get_cursor():self.add_to_cursor(length)]

    def get_cursor_max(self) -> int:
        return get_len_of_file(self._cursor_file_name)

    def uint(self, max: int) -> int:
        return int(self.digits(_required_digits(max))) % max

    def sint(self, min: int, max: int) -> int:
        return self.uint(max - min) - max


def build(lib_file_name: str=f"{location}/pi.so", c_file_name: str=f"{location}/pi.c") -> None:
    from subprocess import run
    run(
        f"gcc -O2 -shared -Wl,-soname,pi -o {lib_file_name} -fPIC {c_file_name} -lgmp",
        shell=True, check=True
    )


def compute(digits: int, lib_file_name: str=f"{location}/pi.so", pi_file_name: str=f"{location}/pi") -> None:
    _assert_uint(digits)

    pi_lib: CDLL = CDLL(lib_file_name)
    if cast(int, pi_lib.calc_digits_and_write_in(digits, pi_file_name.encode("utf-8"))):
        raise MemoryError("Could not compute digits")
