"""The PiRan module."""
from os.path import isfile, join as osjoin, getsize
from os import remove, getcwd
from sys import maxsize, stdout, stderr
from ctypes import CDLL, cast as c_cast, c_char_p
from typing import Optional, IO, Tuple, Union, NoReturn, cast, Type, Any

__author__ = "Firefnix"
__license__ = "GPL-3-or-later"
__version__ = "1.0"

CCharPointer =  Optional[bytes]

piran_verbose: bool = False
piran_pad: int = len(str(maxsize)) - 1
piran_path: str = getcwd()
piran_uint_limit = int('9' * piran_pad)


def verb_print(*args: object, sep: str=' ', end: str='\n',
        file: IO[str]=stdout, flush: bool=False) -> None:
    if piran_verbose is True:
        print(*args, sep=sep, end=end, file=file, flush=flush)


class Random:
    """Use random numbers, bytes and chars."""

    def __init__(self, pi_file_name: str = "pi",
        cursor: Union[str, int, None] = None) -> None:
        self._cursor_file_name: str
        self._cursor: int

        if isfile(pi_file_name) is False:
            raise FileNotFoundError(f"{pi_file_name} not found")

        if isinstance(cursor, str) is True:
            self._cursor_file_name = cast(str, cursor)
            self._cursor = self.saved_cursor
        else:
            self._cursor = cast(int, cursor or 0)
            self._cursor_file_name = f"cursor_{hex(id(self))[2:]}"
        self._pi_file_name: str = osjoin(piran_path, pi_file_name)
        self.save()

    @property
    def cursor(self) -> int:
        """Position in the PI file."""
        return self._cursor

    @cursor.setter
    def cursor(self, value: int) -> None:
        self._cursor = value
        self.save()

    @property
    def saved_cursor(self) -> int:
        """Get the cursor value from cursor_file."""
        with open(self._cursor_file_name) as cursor_file:
            return int(cursor_file.read())

    @saved_cursor.setter
    def saved_cursor(self, value: int) -> None:
        """Save the cursor value in cursor_file."""
        if not isinstance(value, int):
            raise TypeError("must be an int")
        verb_print("save:", self.cursor, "in", self._cursor_file_name)
        with open(self._cursor_file_name, "w") as cursor_file:
            cursor_file.write(str(value))

    def close(self) -> None:
        """Delete the cursor file."""
        verb_print("remove:", self._cursor_file_name)
        remove(self._cursor_file_name)

    def save(self) -> None:
        """Save cursor in its file. Sytaxic sugar."""
        self.saved_cursor = self.cursor

    @property
    def cursor_max(self) -> int:
        return getsize(self._cursor_file_name)

    def _next_digits(self, digits: int=piran_pad) -> str:
        with open(self._pi_file_name) as pi_file:
            self.cursor += digits
            return pi_file.read()[self.cursor-digits:self.cursor]

    def uint(self, max: int) -> int:
        return int(self._next_digits())

    def sint(self, max: int) -> int:
        return int(self._next_digits()) - int(piran_uint_limit/2)

    def digits(self, length: int) -> str:
        return self._next_digits(length)

def build() -> None:
    from subprocess import run
    run(
        "gcc -O2 -shared -Wl,-soname,pi -o pi.so -fPIC pi.c -lgmp",
        shell=True, check=True
    )
    verb_print("compiled: pi.c -> pi.so")


def compute(digits: int, lib_file_name: str="./pi.so", pi_file_name: str="./pi") -> None:
    pi_lib: CDLL = CDLL(lib_file_name)
    if digits < 0:
        raise ValueError("'digits' must be an unsigned int")

    pi_char_p: CCharPointer = pi_lib.pi_str(digits)
    verb_print(f"allocated: {hex(cast(int, pi_char_p))}")

    pi_c_str: CCharPointer = c_cast(cast(Union, pi_char_p), c_char_p).value
    if pi_c_str is None:
        raise ValueError("pi_str returned NULL")

    verb_print(f"freed: {hex(cast(int, pi_char_p))}")
    pi_lib.free_string(pi_char_p)
    pi_str = pi_c_str.decode('ascii')

    with open(pi_file_name, "w") as pi_file:
        pi_file.write(pi_str)
