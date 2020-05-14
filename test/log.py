"""Log system for PiRan."""
from typing import Union, Tuple, Optional
from platform import system
from sys import argv

def is_ms_windows() -> bool:
    """Return True if the system is Microsoft Windows, else False."""
    return "win" in system().lower()


def os_init() -> None:
    """Initialize OS's console."""
    if is_ms_windows() is True:
        from ctypes import windll
        kernel = windll.kernel32
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)

NO_ARG: int = -1

class Flag:
    _args: Tuple[str, ...] = tuple(argv)
    _args_len: int = len(_args)

    @staticmethod
    def is_an_arg(value: str) -> bool:
        return value == '-'
    def __init__(self, short_name: str, long_name: str, has_value: bool = False) -> None:
        """Create a Flag object"""
        self.short: str = short_name
        self.long: str = long_name
        self.has_value: bool = has_value

        self.pos: int = self.get_position()
        self.next: Optional[str] = self.get_next()
        self.val: Union[str, None] = self.get_value()

    def __str__(self) -> str:
        return self.val or ''
    def __bool__(self) -> bool:
        return self.pos != NO_ARG
    __nonzero__ = __bool__

    def get_position(self) -> int:
        """Returns the position of the flag in argv, or NO_ARG"""
        for i in range(len(self._args)):
            if self.is_an_arg(self._args[i][0]) and len(self._args[i]) > 1:
                if self.is_an_arg(self._args[i][1]):
                    if self._args[i][2:] == self.long:
                        return i
                elif self.short in self._args[i][1:]:
                    return i
        return NO_ARG

    def get_next(self) -> Optional[str]:
        """Returns the next argument or None"""
        if self.pos == NO_ARG or self.pos+1 >= self._args_len:
            return None
        return self._args[self.pos+1]

    def get_value(self) -> Optional[str]:
        """Returns the value corresponding to the flag or None
        (if has_value is False, None is returned anyway)"""
        if self.has_value is False or self.pos == NO_ARG:
            return None
        next_arg = self.next
        if next_arg is None:
            return None
        if self.is_an_arg(next_arg):
            return None
        return next_arg

    def exists(self) -> bool:
        return bool(self)
