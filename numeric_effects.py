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
                ('>=', ('customer-money',), ('price', 'p')),
            ),
            effects=(
                ('-=', ('quantity', 'p'), 1),
                ('+=', ('account',), ('price', 'p')),
                ('-=', ('customer-money',), ('price', 'p')),
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
            ('=', ('customer-money',), 15),
            ('=', ('quantity', 'apples'), 10),
            ('=', ('quantity', 'oranges'), 10),
            ('=', ('price', 'apples'), 3),
            ('=', ('price', 'oranges'), 5),
        ),
        goal=(
            ('=', ('account',), 13),
        )
    )

    plan = planner(problem, verbose=True)
    if plan is None:
        print('No Plan!')
    else:
        state = problem.initial_state
        for action in plan:
            print(action)
            state = state.apply(action)
            print(state.f_dict)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option('-q', '--quiet',
                      action='store_false', dest='verbose', default=True,
                      help="don't print statistics to stdout")

    # Parse arguments
    opts, args = parser.parse_args()
    problem(opts.verbose)
