from __future__ import print_function
from pyddl import Domain, Problem, Action, planner, neg 

#################################################### 
'''Solve Hanoi tower with [1...5] disks, 
developed for a small university project
 - @piopy'''

dischi=['start','middle','finish','orange','yellow','green','blue','purple']

global_domain=Domain((
        Action(
            'move',
            parameters=(
                ('position', 'X'),
                ('position', 'Y'),
                ('position', 'Z'),
            ),
            preconditions=(
                ('Clear',  'X'),
                ('Clear', 'Z'),
                ('On', 'X',  'Y'),
                ('smaller', 'X', 'Z'),
            ),
            effects=(
                neg(('Clear', 'Z')),
                neg(('On',  'X', 'Y')),
                ('Clear', 'Y'),
                ('Clear', 'X'),
                ('On',  'X',  'Z'),
            ),
        ),
    ))

def compile_on(num,dove):
    num=str(num)
    if num == '1' :return (('On', 'orange',  dove))
    if num == '2' :return (('On', 'orange', 'yellow'),
    ('On', 'yellow',  dove))
    if num == '3' :return (('On', 'orange', 'yellow'),
    ('On', 'yellow', 'green'),
    ('On', 'green', dove))
    if num == '4' :return (('On', 'orange', 'yellow'),
    ('On', 'yellow', 'green'),
    ('On', 'green', 'blue'),
    ('On', 'blue', dove))
    if num == '5' :return (('On', 'orange', 'yellow'),
    ('On', 'yellow', 'green'),
    ('On', 'green', 'blue'),
    ('On', 'blue', 'purple'),
    ('On', 'purple', dove))


def problem(verbose, number):
    domain = global_domain

    problem = Problem(
        domain,
        {
            'position': (dischi[:number+3]),
        },
        init=(
            ('Clear', 'orange'),
            ('Clear',  'middle'),
            ('Clear',  'finish'),

            ('smaller',  'orange',   'yellow'),
            ('smaller',  'orange',   'green'),
            ('smaller',  'orange',   'blue'),
            ('smaller',  'orange',   'purple'),
            ('smaller',  'orange',   'start'),
            ('smaller',  'orange',   'middle'),
            ('smaller',  'orange',   'finish'),

            ('smaller',  'yellow',   'green'),
            ('smaller',  'yellow',   'blue'),
            ('smaller',  'yellow',   'purple'),
            ('smaller',  'yellow',   'start'),
            ('smaller',  'yellow',   'middle'),
            ('smaller',  'yellow',   'finish'),
            
            ('smaller',  'green',   'blue'),
            ('smaller',  'green',   'purple'),
            ('smaller',  'green',   'start'),
            ('smaller',  'green',   'middle'),
            ('smaller',  'green',   'finish'),

            ('smaller',  'blue',   'purple'),
            ('smaller',  'blue',   'start'),
            ('smaller',  'blue',   'middle'),
            ('smaller',  'blue',   'finish'),

            ('smaller',  'purple',   'start'),
            ('smaller',  'purple',   'middle'),
            ('smaller',  'purple',   'finish'),

        ).__add__(compile_on(number,'start')),
        goal=(
            ('Clear',  'start'),
            ('Clear',  'middle'),
            ('Clear',  'orange'),
        ).__add__(compile_on(number,'finish'))
    )
    lista=[]
    plan = planner(problem, verbose=verbose)
    if str(number) == '1': return ['move(orange, start, finish)'] # found a bug with only 1 disk
    if plan is None:
        print('No Plan!')
    else:
        state = problem.initial_state
        for action in plan:
            if verbose: print(action)
            lista.append(str(action))
            state = state.apply(action)
            if verbose: print(state.f_dict)
    return analyze(lista)

def runquiet(number, verbose=False):
    number=str(number)
    if number == '1' : plan=problem(verbose=False,number=1)
    elif number == '2' : plan=problem(verbose=False,number=2)
    elif number == '3' : plan=problem(verbose=False,number=3)
    elif number == '4' : plan=problem(verbose=False,number=4)
    elif number == '5' : plan=problem(verbose=False,number=5)
    if verbose : print(plan)
    return plan


def analyze(lista):
    l=[]
    for step in lista:
        step=str(step)
        step=step.replace('move(','').replace(')','')
        steps=step.split(',')
        l.append(steps)
    return l




if __name__ == '__main__':
    runquiet(input("N° Disks: "),verbose=True)
