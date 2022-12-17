"""
Gripper robot planning example.
A robot has two gripper arms. In this planning example, the robot moves five balls
from room A to room B.

Initial State:
|---rooma--+---roomb--+
|   ball1  |          |
|   ball2  |          |
|   ball3  |          |
|   ball4  |          |
|   ball5  |          |
|  >robot<            |
+---------------------+

Goal State:
|-rooma----+---roomb--+
|          |  ball1   |
|          |  ball2   |
|          |  ball3   |
|          |  ball4   |
|          |  ball5   |
|            >robot<  |
+---------------------+

"""

from pyddl import Domain, Problem, Action, neg, planner


def problem(verbose):
    domain = Domain((
        Action(
            'move',
            parameters=(
                ('Rooms', 'x'),
                ('Rooms', 'y'),
            ),
            preconditions=(
                ('ROOM', 'x'),
                ('ROOM', 'y'),
                ('at-robby', 'x'),
            ),
            effects=(
                ('at-robby', 'y'),
                neg(('at-robby', 'x')),
            ),
        ),
        Action(
            'pick-up',
            parameters=(
                ('Balls', 'x'),
                ('Rooms', 'y'),
                ('Robot-arms', 'z'),
            ),
            preconditions=(
                ('BALL', 'x'),
                ('ROOM', 'y'),
                ('GRIPPER', 'z'),
                ('at-ball', 'x', 'y'),
                ('at-robby', 'y'),
                ('free', 'z'),
            ),
            effects=(
                ('carry', 'z', 'x'),
                neg(('at-ball', 'x', 'y')),
                neg(('free', 'z')),
            ),
        ),
        Action(
            'drop',
            parameters=(
                ('Balls', 'x'),
                ('Rooms', 'y'),
                ('Robot-arms', 'z'),
            ),
            preconditions=(
                ('BALL', 'x'),
                ('ROOM', 'y'),
                ('GRIPPER', 'z'),
                ('carry', 'z', 'x'),
                ('at-robby', 'y'),
            ),
            effects=(
                ('at-ball', 'x', 'y'),
                ('free', 'z'),
                neg(('carry', 'z', 'x')),
            ),
        ),
    ))
    problem = Problem(
        domain,
        {
            'Rooms': ('rooma', 'roomb'),
            'Balls': ('ball1', 'ball2', 'ball3', 'ball4', 'ball5'),
            'Robot-arms': ('left', 'right'),
        },
        init=(
            # ??
            ('ROOM', 'rooma'),
            ('ROOM', 'roomb'),
            ('BALL', 'ball1'),
            ('BALL', 'ball2'),
            ('BALL', 'ball3'),
            ('BALL', 'ball4'),
            ('BALL', 'ball5'),
            ('GRIPPER', 'left'),
            ('GRIPPER', 'right'),

            ('free', 'left'),
            ('free', 'right'),
            ('at-robby', 'rooma'),
            ('at-ball', 'ball1', 'rooma'),
            ('at-ball', 'ball2', 'rooma'),
            ('at-ball', 'ball3', 'rooma'),
            ('at-ball', 'ball4', 'rooma'),
            ('at-ball', 'ball5', 'rooma'),
        ),
        goal=(
            ('at-ball', 'ball1', 'roomb'),
            ('at-ball', 'ball2', 'roomb'),
            ('at-ball', 'ball3', 'roomb'),
            ('at-ball', 'ball4', 'roomb'),
            ('at-ball', 'ball5', 'roomb'),
        )
    )

    plan = planner(problem, verbose=verbose)
    if plan is None:
        print('No Plan!')
    else:
        for action in plan:
            print(action)

if __name__ == '__main__':
    problem(verbose=True)
