# metonic

Generation and manipulation of hypothetical [Metonic
cycles](https://en.wikipedia.org/wiki/Metonic_cycle).

## Installation

    pip install metonic
    
## Usage

In the ancient Greek calendars, the “standard” Metonic cycle of
ordinary (12-month, 354-day) and intercalary (13-month, 384-day)
[lunisolar years](https://en.wikipedia.org/wiki/Lunisolar_calendar)
conforms to a few rules:

- Nineteen years long
- Seven of the nineteen years are intercalary
- One intercalary year cannot follow another
- No more than two ordinary years may occur in succession

`metonic` generates Metonic cycles based on these descriptive rules
(or based on changes to these rules) and provides methods for
manipulating them.

Most of this is actually unnecessary. The trend over the last century
of scholarship has been to see the Greek (mostly meaning the Athenian)
calendar as very regular and conforming closely to astronomical
phenomena. Still, there is a lot of literature, primarily by Benjamin
D. Meritt, that views the calendar as very irregular. `metonic` might
be useful for exploring and understanding these earlier
reconstructions.

### Cycles of Ordinary and Intercalary Years

`metonic` represents cycles as strings of ordinary (“0”) and intercalary (“1”) years. The standard Athenian Metonic cycle is available as a constant:

    >>> import metonic
    >>> metonic.ATHENS
    '0100100101001001010'
	
This is a 19-year cycle of twelve ordinary and seven intercalary years. The first year of the first cycle is 432/431 BCE.

To get the year at any position of any cycle:

    >>> metonic.from_metonic(1, 1)
    -431
    >>> metonic.from_metonic(5, 12)
    -344
	
The values returned are [astronomical
years](https://en.wikipedia.org/wiki/Astronomical_year_numbering)—years
BCE are negative numbers and 1 BCE is 0. You can use another library
(eparkhontos)[https://pypi.org/project/eparkhontos/] to make it easier
to work with Greek and astronomical years

You can also get the Metonic cycle from the year:

    >>> metonic.to_metonic(-431)
    (1, 1)
    >>> metonic.to_metonic(-344)
    (5, 12)

### Generating Cycles

`cycle_set()` will generate all the unique cycles that satisfy the
given conditions: length of cycle (`n`), number of intercalary years
(`i_count`), maximum number of intercalary years in a row (`max_i`),
and maximum number of ordinary years in a row (`max_o`). The defaults
are those listed above (19 years, 7 intercalary, no more than 1
intercalary and 2 ordinary in a row):

    >>> for _ in metonic.cycle_set():
    ...     print(_)
    ...
    0010010010010010101
    0010010010010100101
    0010010010100100101
	
The cycles will be output in the lowest possible “alphabetical” order
(which is the same as numeric if these are treated as binary
numbers). These default parameters output three cycles because there
_are_ three unique cycles that satisfy those rules. Only the third
“exists in nature”. It might not look at first like this matches the
Athenian Metonic cycle:

    0010010010100100101
    0100100101001001010 # metonic.ATHENS
	
But since this is a cycle, it _repeats_ and the standard Athenian
cycle is just a version of this cycle shifted to the right.

    00100100101001001010010010010100100101 # × 2
     0100100101001001010                   # metonic.ATHENS
	  |  |  | |  |  | |                    # intercalary years line up
	 
When testing equivalency and uniqueness, `metonic` takes these
repetitions into account.

If you want to allow two intercalary years in a row you will get a
different set:

    >>> for _ in metonic.cycle_set(max_i=2):
    ...     print(_)
    ...
    0010010010010010011
    0010010010010010101
    0010010010010100101
    0010010010100100101


As you will if you allow 8 intercalary years or 4 ordinary in a row:

    >>> len(metonic.cycle_set(i_count=8))
    7
    >>> len(metonic.cycle_set(max_o=3))
    38 
	
`i_count` can be an iterable allowing multiple values, such as 7 _or_
8 intercalary years:

    >>> len(metonic.cycle_set(i_count=[7,8]))
    10
	
Or you can make up any rules you want:

    >>> metonic.cycle_set(n=5, i_count=2, max_o=3)
    ('00101',)

### Segments

`segments()` finds all the unique segments of a cycle of any given
length. For instance all the five year segments of the Athenian cycle:

    >>> for _ in metonic.segments(metonic.ATHENS, 5):
    ...     print(_)
    ...
    00100
    00101
    01001
    01010
    10010
    10100

Segments wrap from end to beginning. All the segments of length 4 for
the cycle "00001" are:

    >>> metonic.segments("00001", 4)
    ('0000', '0001', '0010', '0100', '1000')
   
The last three show this wrapping, i.e. (wrapping point indicated by
the bar (“|”):

    00001|00001
    0000
	 0001
	  001 0
	   01 00
	    1 000


### Testing segments against cycles

`in_cycle()` will test whether a segment is in a cycle or group of
cycles, wrapping when necessary:

    >>> metonic.in_cycle("0100", "00001")
    True
	
This true because "0100" matches a segment in "00001" treated as a ring:

    0000100001
	   0100
	   
If you test against an iterable, the test will be repeated for each
member of the iterable. The result will be a tuple of cycles for which
there is a match, an empty tuple if there are no matches:

    >>> metonic.in_cycle("0010101", metonic.cycle_set())
    ('0010010010010010101',)
	>>> metonic.in_cycle("11", metonic.cycle_set())
    ()
	
### All Combinations

`cycle_set()` begins with all possible combinations of ordinary and
intercalary years before reducing them to unique cycles. The
non-unique combinations can be gotten from `combinations()`. This
takes the same parameters and defaults as `cycle_set` so, with no
arguments, it returns a tuple of all combinations according to the
standard Metonic criteria:

    >>> len(metonic.combinations())
    57
	
The 57 combinations are 19 “rotations” of 3 unique cycles (19 × 3 =
57). The difference between `combinations()` and `cycle_set()` is that
`combinations()` returns all the rotations while `cycle_set()` only
returns one example of each unique cycle (specifically the one that
comes first in an alphabetical sort).

`cycle_set()` can also take an iterable of combinations. This:

    >>> c = metonic.combinations()
	>>> metonic.cycle_set(c)
	
is the same as calling `cycle_set()` by itself. Likewise for any combination of parameters:

    >>> c = metonic.combinations(i_count=8)
	>>> metonic.cycle_set(c)
	
is the same as:

    >>> metonic.cycle_set(i_count=8)
	
## Contributing

Bug reports and pull requests are welcome on GitHub at
https://github.com/seanredmond/metonic

