"""
Test support for parametrized increment/decrement values in numeric effects
"""
from __future__ import print_function
from pyddl import Domain, Problem, Action, planner

def problem(verbose):
    domain = Domain((
        Action(
            'sell',
            parameters=(
                ('product', 'p'),
            ),
            preconditions=(
                ('>', ('quantity', 'p'), 0),
            ),
            effects=(
                ('-=', ('quantity', 'p'), 1),
                ('+=', ('account',), ('price', 'p')),
            ),
        ),
    ))
    problem = Problem(
        domain,
        {
            'product': ('apples', 'oranges',),
        },
        init=(
            ('=', ('account',), 0),
            ('=', ('quantity', 'apples'), 10),
            ('=', ('quantity', 'oranges'), 10),
            ('=', ('price', 'apples'), 3),
            ('=', ('price', 'oranges'), 5),
        ),
        goal=(
            ('=', ('account',), 13),
        )
    )

    plan = planner(problem, verbose=verbose)
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
