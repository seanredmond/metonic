# metonic, Metonic cycle generator
# Copyright (C) 2023  Sean Redmond

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from metonic.__version__ import __version__
from itertools import product


ATHENS = "0100100101001001010"
METONIC_YEAR_ZERO = -431


def cycle_set(c=None, n=19, i_count=7, max_i=1, max_o=2):
    """Reduce a list of combinations to only unique cycles.

    Parameters:
    c (interable) -- List of combinations to reduce
    n (int) -- length of sequences (Default: 19)
    i_count (iterable, int) -- Number of intercalary years required. Can be an
        iterable of multiple valid options (Default: [7])
    max_i (int) -- Maximum number of allowed intercalary years in a row
        (Default: 1)
    max_o (int) -- Maximum number of allowed ordinary years in a row
        (Default: 2)

    Reduces list c of I/O combinations to only unique
    cycles. combinations() produces combinations that identical if
    they are treated as looping cycles -- that is, if the sequence
    represents a ring in which the end joins to the beginning, these
    sequences represent different "rotations" of the same ring.

    If no list of combinations is passed, a list is generated using
    combinations() with the n, i_count, max_i, and max_o criteria. If
    a list of combinations is supplied, these criteria parameters are
    ignored. Calling cycle_set() with all default parameters is the
    same as passing the default output of combinations() to
    cycle_set().

    """
    if c is None:
        return cycle_set(combinations(n, i_count, max_i, max_o))

    return __find_cycles(sorted(c))


def segments(c, n):
    """Generate all unique segments of cycle(s) c of n length.

    c (str, iterable) -- cycle(s) to segment
    n (int) -- length of segments to extract

    Find all the unique (i.e. without duplicates) segments of length n
    of a cycle or set of cycles c. If c is a string it will be used as
    a source of segments. c is treated as a proper cycle to segments
    may span the beginning and end of the string. If c is an iterable,
    the unique segments from all elements of the iterable will be
    returned.

    """
    if isinstance(c, str):
        padded = __cycle_pad(c, n)
        return tuple(sorted(set([padded[_ : _ + n] for _ in range(len(c))])))

    return tuple(sorted(set([a for b in [segments(_, n) for _ in c] for a in b])))


def in_cycle(test, cycle):
    """Test if a sequence occurs in a cycle or set of cycles

    Parameters:
    test (str) -- Sequence to test for
    cycle (str, iterable) -- cycle or list of cycles to test against

    Tests whether the test sequence occurs in cycle(c) c, including
    case in which the test sequence spans the end and beginning of
    cycle. If c is a str, result is True or False. If c is an
    iterable, each element is tested and the result is either a tuple
    of matching cycles, which may be empty.

    """
    if isinstance(cycle, str):
        return test in __cycle_pad(cycle, len(test))

    matches = tuple([_ for _ in cycle if in_cycle(test, _)])

    if len(matches):
        return tuple(matches)

    return ()


def combinations(n=19, i_count=[7], max_i=1, max_o=2):
    """Generate all valid combinations of ordinary and intercalary years.

    Parameters:
    n (int) -- length of sequences (Default: 19)
    i_count (iterable, int) -- Number of intercalary years required. Can be an
        iterable of multiple valid options (Default: [7])
    max_i (int) -- Maximum number of allowed intercalary years in a row
        (Default: 1)
    max_o (int) -- Maximum number of allowed ordinary years in a row
        (Default: 2)

    Generates all combinations of ordinary (0) and intercalary (1) of
    length n, that satisfy the criteria of i_count, max_im and
    max_o. The default values are the rules of the Metonic cycle: 19
    years long, 7 intercalary years in each cycle, there can not be
    successive intercalary years and no more that two ordinary years
    in a row. The actual Metonic cycle is one of three such possible
    cycles.

    """
    return tuple(
        __max_successive(
            __max_successive(
                __max_i_count(
                    [f"{{:0{n}b}}".format(_) for _ in range(0, 2**n)], i_count
                ),
                "1",
                max_i,
            ),
            "0",
            max_o,
        )
    )


def as_str(c):
    """Convert cycle to a string of “O” (ordinary) and  “I” (intercalary)."""
    return c.replace("0", "O").replace("1", "I")


def as_ints(c):
    """Convert cycle to tuple of 0's (ordinary) and 1's (intercalary)."""
    return tuple([int(_) for _ in c])


def to_metonic(year):
    """Get the Metonic cycle and position in cycle (1-19) for a year

    Parameters:
    year (int) -- An astronomical year (BCE is negative and 1 BCE is zero)

    Return a tuple. The first member is the Metonic cycle of the year,
    the second the position of the year (1-19) in the cycle.

    """
    return (
        ((year - METONIC_YEAR_ZERO) // 19) + 1,
        ((year - METONIC_YEAR_ZERO) % 19) + 1,
    )


def from_metonic(cycle, pos):
    """Get the year from the Metonic cycle and position

    Parameters:
    year (int) -- the Metonic cycle
    position (int) -- the position (1-19) in the cycle

    Returns an astronomical year of the given cycle and position.

    """
    return ((cycle - 1) * 19 + METONIC_YEAR_ZERO) + (pos - 1)


def version():
    """Return current version."""
    return __version__


def __cycle_pad(c, n):
    """Pad tail of cycle with enough characters of the head to treat as a ring."""
    return c + c[: n - 1]


def __max_i_count(m, i_count=[7]):
    """True if count if 1's in cycle is in i_count."""
    try:
        return [_ for _ in m if _.count("1") in i_count]
    except TypeError:
        return __max_i_count(m, (i_count,))


def __max_successive(m, c, n=1):
    """True of there is no sequence of successive character c in m longer than n."""
    ch = str(c)
    return [_ for _ in m if not ch * (n + 1) in __cycle_pad(_, n + 1)]


def __find_cycles(cycles):
    """Recursively find unique cycles, treated as rings, in m."""

    # I would prefer to use recursion and this can easily be tail-call
    # optimized, but since Python doesn't use TCO, it can exceed the
    # max recursion depth
    rv = ()
    padded = ()

    for cycle in cycles:
        if not any([cycle in _ for _ in padded]):
            # Save the cycle for return
            rv = rv + (cycle,)
            # Save cycle padded version for further comparisons
            padded = padded + (__cycle_pad(cycle, len(cycle)),)

    return rv
