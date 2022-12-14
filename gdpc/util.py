"""Generic utilities"""

__author__ = "Arthur van der Staaij"
__copyright__ = "Copyright 2022, Arthur van der Staaij"
__licence__ = "MIT"

import sys
import numpy as np

from typing import TypeVar, Generic
from contextlib import contextmanager
from dataclasses import dataclass


T = TypeVar("T")


def isign(x: int):
    """Returns the sign of [x].
        Note that isign(0) == 1."""
    return 1 if x >= 0 else -1


def clamp(x: T, minimum: T, maximum: T) -> T:
    """Clamps [x] to the range [minimum, maximum]"""
    return max(minimum, min(maximum, x))


@dataclass
class Range(Generic[T]):
    """A generic range"""
    min: T
    max: T


def eprint(*args, **kwargs):
    """print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


# Based on https://stackoverflow.com/q/2125702
@contextmanager
def stdoutToStderr():
    """Redirects stdout to stderr within its scope"""
    old_stdout = sys.stdout
    sys.stdout = sys.stderr
    try:
        yield
    finally:
        sys.stdout = old_stdout


# Based on https://stackoverflow.com/a/21032099
def normalized(a, order=2, axis=-1):
    """Normalizes [a] using the L[order] norm.
        If [axis] is specified, normalizes along that axis."""
    norm = np.atleast_1d(np.linalg.norm(a, order, axis))
    norm[norm == 0] = 1
    return a / np.expand_dims(norm, axis)


def inclusiveBetween(start, end, value):
    """**Raise an exception when the value is out of bounds**."""
    if not start <= value <= end:
        raise ValueError(
            f"The value {value} is not in the inclusive range "
            f"of {start} to {end}")

