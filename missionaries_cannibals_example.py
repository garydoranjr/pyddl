#!/usr/bin/env python
"""
Example of using PyDDL to solve the "Missionaries and Cannibals" Problem.
A boat must transport a group of 3 missionaries and 3 cannibals across a river,
but at no time can the cannibals outnumber the missionaries at either side of
the river.
"""
from pyddl import Domain, Problem, Action, neg, planner

def problem(verbose):
    domain = Domain((
        Action(
            'cross-right',
            preconditions=(
                ('at', 'left-bank'),
                ('>', ('occupants',), 0),
            ),
            effects=(
                neg(('at', 'left-bank')),
                ('at', 'right-bank'),
            ),
        ),
        Action(
            'cross-left',
            preconditions=(
                ('at', 'right-bank'),
                ('>', ('occupants',), 0),
            ),
            effects=(
                neg(('at', 'right-bank')),
                ('at', 'left-bank'),
            ),
        ),
        Action(
            'onboard-cannibal',
            parameters=(
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'l'),
                ('>', ('cannibals', 'l'), 0),
                ('<', ('occupants',), 2),
            ),
            effects=(
                ('-=', ('cannibals', 'l'), 1),
                ('+=', ('cannibals', 'boat'), 1),
                ('+=', ('occupants',), 1),
            ),
        ),
        Action(
            'onboard-missionary',
            parameters=(
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'l'),
                ('>', ('missionaries', 'l'), 0),
                ('>', ('missionaries', 'l'), ('cannibals', 'l')),
                ('<', ('occupants',), 2),
            ),
            effects=(
                ('-=', ('missionaries', 'l'), 1),
                ('+=', ('missionaries', 'boat'), 1),
                ('+=', ('occupants',), 1),
            ),
        ),
        Action(
            'offboard-cannibal',
            parameters=(
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'l'),
                ('>', ('cannibals', 'boat'), 0),
                ('>', ('missionaries', 'l'), ('cannibals', 'l')),
            ),
            effects=(
                ('-=', ('cannibals', 'boat'), 1),
                ('-=', ('occupants',), 1),
                ('+=', ('cannibals', 'l'), 1),
            ),
        ),
        Action(
            'offboard-missionary',
            parameters=(
                ('location', 'l'),
            ),
            preconditions=(
                ('at', 'l'),
                ('>', ('missionaries', 'boat'), 0),
            ),
            effects=(
                ('-=', ('missionaries', 'boat'), 1),
                ('-=', ('occupants',), 1),
                ('+=', ('missionaries', 'l'), 1),
            ),
        ),
    ))
    problem = Problem(
        domain,
        {
            'location': ('left-bank', 'right-bank'),
        },
        init=(
            ('at', 'left-bank'),
            ('=', ('missionaries', 'boat'), 0),
            ('=', ('cannibals', 'boat'), 0),
            ('=', ('occupants',), 0),
            ('=', ('missionaries', 'left-bank'), 3),
            ('=', ('cannibals', 'left-bank'), 3),
            ('=', ('missionaries', 'right-bank'), 0),
            ('=', ('cannibals', 'right-bank'), 0),
        ),
        goal=(
            ('=', ('missionaries', 'right-bank'), 3),
            ('=', ('cannibals', 'right-bank'), 3),
        )
    )

    plan = planner(problem, verbose=verbose)
    if plan is None:
        print 'No Plan!'
    else:
        for action in plan:
            print action

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)
