"""A progress bar for sklearn"""

import re
import sys
from collections.abc import Iterable
from contextlib import contextmanager
from io import StringIO

from progiter import ProgIter

__all__ = ["skprogress"]

_FITS = re.compile(r"totalling (\d+) fits")


class ProgressIO(StringIO):
    """A subclass of StringIO that updates progress with progiter"""

    def __init__(self, real_stdout, initial_value: str | None = None, newline: str | None = None) -> None:
        super().__init__(initial_value, newline)
        self.prog: ProgIter | None = None
        self.real_stdout = real_stdout

    def _get_fits(self, s: str) -> int | None:
        """Get the total number of fits in string s"""
        matches = _FITS.search(s)

        if not matches:
            return

        return int(matches.group(1))

    def _update_prog(self, s):
        """Update the progress bar based on s"""
        if n := self._get_fits(s):
            self.real_stdout.write(s)
            if self.prog:
                self.prog.end()
            self.prog = ProgIter(total=n, stream=self.real_stdout)
            self.prog.begin()
        else:  # noqa: PLR5501
            if self.prog:
                # propagate information other than training records
                if (count := s.count("CV")) != 0:
                    self.prog.step(count)
                else:
                    self.real_stdout.write(s)

    def write(self, s: str) -> int:
        self._update_prog(s)

        return super().write(s)

    def writelines(self, lines: Iterable[str]) -> None:
        self._update_prog("\n".join(lines))

        return super().writelines(lines)


@contextmanager
def skprogress():
    real_stdout = sys.stdout
    sys.stdout = ProgressIO(real_stdout)
    yield sys.stdout
    sys.stdout = real_stdout
