#!/usr/bin/env python
"""
Example of using PyDDL to solve an eight-puzzle. Each number is a tile that
can slide vertically or horizontally to fill in the blank space. This "hard"
instance (requiring the maximum of 31 steps) is taken from the following paper:

Reinefeld, Alexander. "Complete Solution of the Eight-Puzzle and the Benefit of
  Node Ordering in IDA*." International Joint Conference on Artificial
  Intelligence. 1993.

Initial State:
+---+---+---+
| 8   7   6 |
|     4   1 |
| 2   5   3 |
+---+---+---+

Goal State:
+---+---+---+
|     1   2 |
| 3   4   5 |
| 6   7   8 |
+---+---+---+
"""
from __future__ import print_function
from pyddl import Domain, Problem, Action, neg, planner

def problem(verbose):
    domain = Domain((
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
        Action(
            'move-down',
            parameters=(
                ('tile', 't'),
                ('position', 'px'),
                ('position', 'py'),
                ('position', 'by'),
            ),
            preconditions=(
                ('inc', 'by', 'py'),
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
        Action(
            'move-left',
            parameters=(
                ('tile', 't'),
                ('position', 'px'),
                ('position', 'py'),
                ('position', 'bx'),
            ),
            preconditions=(
                ('dec', 'bx', 'px'),
                ('blank', 'bx', 'py'),
                ('at', 't', 'px', 'py'),
            ),
            effects=(
                neg(('blank', 'bx', 'py')),
                neg(('at', 't', 'px', 'py')),
                ('blank', 'px', 'py'),
                ('at', 't', 'bx', 'py'),
            ),
        ),
        Action(
            'move-right',
            parameters=(
                ('tile', 't'),
                ('position', 'px'),
                ('position', 'py'),
                ('position', 'bx'),
            ),
            preconditions=(
                ('inc', 'bx', 'px'),
                ('blank', 'bx', 'py'),
                ('at', 't', 'px', 'py'),
            ),
            effects=(
                neg(('blank', 'bx', 'py')),
                neg(('at', 't', 'px', 'py')),
                ('blank', 'px', 'py'),
                ('at', 't', 'bx', 'py'),
            ),
        ),
    ))
    problem = Problem(
        domain,
        {
            'tile': (1, 2, 3, 4, 5, 6, 7, 8),
            'position': (1, 2, 3),
        },
        init=(
            ('inc', 1, 2),
            ('inc', 2, 3),
            ('dec', 3, 2),
            ('dec', 2, 1),
            ('at', 8, 1, 1),
            ('at', 7, 2, 1),
            ('at', 6, 3, 1),
            ('blank', 1, 2),
            ('at', 4, 2, 2),
            ('at', 1, 3, 2),
            ('at', 2, 1, 3),
            ('at', 5, 2, 3),
            ('at', 3, 3, 3),
        ),
        goal=(
            ('blank', 1, 1),
            ('at', 1, 2, 1),
            ('at', 2, 3, 1),
            ('at', 3, 1, 2),
            ('at', 4, 2, 2),
            ('at', 5, 3, 2),
            ('at', 6, 1, 3),
            ('at', 7, 2, 3),
            ('at', 8, 3, 3),
        )
    )

    def to_coordinates(state):
        grid = {}
        for p in state:
            if p[0] == 'at':
                grid[p[1]] = (p[2], p[3])
        return grid

    goal_coords = to_coordinates(problem.goals)

    def manhattan_distance_heuristic(state):
        state_coords = to_coordinates(state.predicates)
        dist = 0
        for k in goal_coords.keys():
            c1, r1 = goal_coords[k]
            c2, r2 = state_coords[k]
            dist += (abs(c1 - c2) + abs(r1 - r2))
        return dist

    plan = planner(problem, heuristic=manhattan_distance_heuristic, verbose=verbose)
    if plan is None:
        print('No Plan!')
    else:
        for action in plan:
            print(action)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)
