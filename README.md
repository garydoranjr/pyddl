PyDDL
=====
_STRIPS planner with PDDL-like problem specification in Python_

by Gary Doran (<gary.doran@case.edu>)

Installation
------------
PyDDL can be installed using `pip`:

    pip install -e git+https://github.com/garydoranjr/pyddl.git#egg=pyddl

or by running the setup script:

    python setup.py install

About
-----
This is a STRIPS-like planner that I wrote for an AI class assignment. A
planning domain and problem is specified in Python, in a manner that is intended
to be reminiscent of PDDL. However, only a small subset of PDDL-like constructs
are implemented. Planning is performed using A* search, but not too much trouble
has been taken to optimize the search efficiency. Therefore, PyDDL is best
suited for smaller problems.

Usage
-----
A planning domain is specified as a `Domain` object, and takes a list of
`Action` objects. Unlike PDDL, predicates do not need to be explicitly defined.
An `Action` takes a list of arguments similar to that for PDDL. For example, see
the eight-puzzle example script containing the following action:

    Action(
        'move-up',
        parameters=(
            ('tile', 't'),
            ('position', 'px'),
            ('position', 'py'),
            ('position', 'by'),
        ),
        preconditions=(
            ('dec', 'by', 'py'),
            ('blank', 'px', 'by'),
            ('at', 't', 'px', 'py'),
        ),
        effects=(
            neg(('blank', 'px', 'by')),
            neg(('at', 't', 'px', 'py')),
            ('blank', 'px', 'py'),
            ('at', 't', 'px', 'by'),
        ),
    ),

One difference from PDDL here is that parameters are typed using `(type, name)`
tuples rather than specifying types with predicates.

Similarly, a planning problem is specified with a `Problem` object, which takes
a planning domain, a dictionary of typed objects, a list of initial predicates,
and a list of goal predicates.

Once a problem has been constructed, it can be passed to the `planner` function
with optional arguments (e.g. a search heuristic) to generate a plan (if one
exists). The resulting plan is a sequence of `Action` objects to execute, or
`None` if no plan exists.

PyDDL supports some basic numeric functions, comparisons, and operations. See
the "missionaries and cannibals" problem for example usage.
