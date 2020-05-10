"""The PiRan module."""
from os.path import isfile, join as osjoin, getsize
from os import remove, getcwd
from sys import maxsize, stdout, stderr
from ctypes import CDLL, cast as c_cast, c_char_p
from typing import Optional, IO, Union, cast

__author__ = "Firefnix"
__license__ = "GPL-3-or-later"
__version__ = "1.0"

CCharPointer =  Optional[bytes]

piran_path: str = getcwd()

def required_digits(max_value: int) -> int:
    return len(str(max_value + 1))


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
        self._pi_file_name: str = osjoin(piran_path, pi_file_name)

    def get_cursor(self) -> int:
        """Position in the PI file."""
        with open(self._cursor_file_name) as cursor_file:
            return int(cursor_file.read())

    def set_cursor(self, value: int) -> None:
        """Save the cursor value in cursor_file."""
        if not isinstance(value, int):
            raise TypeError("must be an int")
        with open(self._cursor_file_name, "w") as cursor_file:
            cursor_file.write(str(value))

    def add_to_cursor(self, value: int) -> int:
        """Return the changed cursor"""
        self.set_cursor(self.get_cursor() + value)
        return self.get_cursor()

    def close(self) -> None:
        """Delete the cursor file."""
        remove(self._cursor_file_name)

    @property
    def cursor_max(self) -> int:
        return getsize(self._cursor_file_name)

    def uint(self, max: int) -> int:
        return int(self.digits(required_digits(max))) % max

    def sint(self, min: int, max: int) -> int:
        return self.uint(max-min) - max

    def digits(self, length: int) -> str:
        with open(self._pi_file_name) as pi_file:
            return pi_file.read()[self.get_cursor():self.add_to_cursor(length)]


def build() -> None:
    from subprocess import run
    run(
        "gcc -O2 -shared -Wl,-soname,pi -o pi.so -fPIC pi.c -lgmp",
        shell=True, check=True
    )


def compute(digits: int, lib_file_name: str="./pi.so", pi_file_name: str="./pi") -> None:
    pi_lib: CDLL = CDLL(lib_file_name)
    if digits < 0:
        raise ValueError("'digits' must be an unsigned int")

    pi_char_p: CCharPointer = pi_lib.pi_str(digits)
    pi_c_str = c_cast(cast(Union, pi_char_p), c_char_p).value
    if pi_c_str is None:
        raise ValueError("pi_str returned NULL")

    pi_lib.free_string(pi_char_p)
    pi_str = pi_c_str.decode('ascii')

    with open(pi_file_name, "w") as pi_file:
        pi_file.write(pi_str)
