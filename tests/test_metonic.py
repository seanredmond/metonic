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

import metonic as met
import pytest


def test_version():
    assert met.version() == "0.0.1"


def test_as_str():
    assert met.as_str(met.ATHENS) == "OIOOIOOIOIOOIOOIOIO"


def test_as_ints():
    assert met.as_ints(met.ATHENS) == (
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
    )


def test_in_cycle_with_tuple():
    c = met.cycle_set()
    matches = met.in_cycle(met.ATHENS, c)
    assert isinstance(matches, tuple)
    assert matches == ("0010010010100100101",)

    assert met.in_cycle("11", c) == ()

    assert met.in_cycle("0101", c)


def test_in_cycle_with_str():
    c = met.cycle_set()
    met.in_cycle(met.ATHENS, c[0]) is False
    met.in_cycle(met.ATHENS, c[1]) is False
    met.in_cycle(met.ATHENS, c[2]) is True


def test_combinations():

    c = met.combinations(n=3, i_count=(1,))
    assert isinstance(c, tuple)
    assert c == ("001", "010", "100")

    c = met.combinations(n=5, i_count=2, max_i=1, max_o=4)
    assert c == ("00101", "01001", "01010", "10010", "10100")
    assert len(c) == 5

    c = met.combinations(n=5, i_count=2, max_i=2, max_o=4)
    # double the above combinations because "11" is allowed
    assert len(c) == 5 * 2

    c = met.combinations()
    # There are only three cycles that the satisfy the default
    # rules. This returns the 19 rotations of each, so the total is
    #
    #     3 * 19 = 57
    #
    assert len(c) == 3 * 19


def test_cycle_set():
    c = met.combinations(n=3, i_count=(1,))
    assert len(c) == 3

    # The three members of c are all cycles of each other
    print(met.cycle_set(c))
    assert met.cycle_set(c) == ("001",)

    # cycle set generates the same set on its own
    s = met.cycle_set(n=3, i_count=1)
    assert s == ("001",)

    c = met.combinations(n=5, i_count=2, max_i=2, max_o=4)
    assert len(c) == 10

    # the obove combinations are 5 rotations each of two distinct cycles
    assert met.cycle_set(c) == ("00011", "00101")

    # The default rule produce 3 19-year cycles
    default = met.cycle_set()
    assert len(default) == 3
    assert all([len(_) == 19 for _ in default])


def test_segments_with_str():
    assert met.segments(met.ATHENS, 5) == (
        "00100",
        "00101",
        "01001",
        "01010",
        "10010",
        "10100",
    )


def test_segments_with_tuple():
    assert met.segments(met.cycle_set(), 5) == (
        "00100",
        "00101",
        "01001",
        "01010",
        "10010",
        "10100",
        "10101",
    )


def test_large_cycle_set():
    # Recursive version exceeded max recursion depth
    met.cycle_set(max_o=4)


def test_to_metonic():
    assert met.to_metonic(-431) == (1, 1)
    assert met.to_metonic(-430) == (1, 2)
    assert met.to_metonic(-261) == (9, 19)
    assert met.to_metonic(-260) == (10, 1)


def test_from_metonic():
    assert met.from_metonic(1, 1) == -431
    assert met.from_metonic(1, 2) == -430
    assert met.from_metonic(9, 19) == -261
    assert met.from_metonic(10, 1) == -260
