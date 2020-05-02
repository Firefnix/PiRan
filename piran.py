"""The PiRan module."""
from os.path import isfile
from os import remove


class Random:
    """Use random numbers, bytes and chars Random."""

    def __init__(self, pi_file: str = "pi.txt", cursor: int = -1) -> None:
        """Check if the pi file exists and load the cursor."""
        if isfile(pi_file) is False:
            raise FileNotFoundError(f"{pi_file} not found")
        if cursor < 0:
            self.cursor = self.saved_cursor
        self._cursor_file_name = f"cursor_{hex(id(self))}"

    @property
    def cursor(self) -> int:
        """Position in the PI file."""
        return self._cursor

    @cursor.setter
    def cursor(self, value: int):
        self._cursor = value
        self.save()

    @property
    def saved_cursor(self) -> int:
        """Get the cursor value from cursor_file."""
        with open(self._cursor_file_name) as cursor_file:
            return int(cursor_file.read())

    @saved_cursor.setter
    def saved_cursor(self, value: int) -> int:
        """Save the cursor value in cursor_file."""
        if not isinstance(value, int):
            raise TypeError("must be an int")
        with open(self._cursor_file_name, "w") as cursor_file:
            cursor_file.write(str(value))
        return self.cursor

    def close(self):
        """Delete the cursor file."""
        remove(self._cursor_file_name)

    def save(self):
        """Save cursor in its file. Sytaxic sugar."""
        self.saved_cursor = self.cursor
