"""Log system for PiRan."""


def is_ms_windows() -> bool:
    """Return True if the system is Microsoft Windows, else False."""
    return "win" in __import__("platform").system().lower()


def os_init():
    """Initialize OS's console."""
    if is_ms_windows() is False:
        return
    kernel = __import__("ctypes").windll.kernel32
    kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
