from __future__ import print_function
from time import time
import heapq

def planner(problem, heuristic=None, state0=None, goal=None,
            monotone=False, verbose=True):
    """
    Implements A* search to find a plan for the given problem.
    Arguments:
    problem   - a pyddl Problem
    heuristic - a heuristic to use (h(state) = 0 by default)
    state0    - initial state (problem.initial_state by default)
    goal      - tuple containing goal predicates and numerical conditions
                (default is (problem.goals, problem.num_goals))
    monotone  - if True, only applies actions by ignoring delete lists
    verbose   - if True, prints statistics before returning
    """
    if heuristic is None:
        heuristic = null_heuristic
    if state0 is None:
        state0 = problem.initial_state
    if goal is None:
        goal = (problem.goals, problem.num_goals)

    states_explored = 0
    closed = set()
    fringe = [(heuristic(state0), -state0.cost, state0)]
    heapq.heapify(fringe)
    start = time()
    while True:
        if len(fringe) == 0:
            if verbose: print('States Explored: %d' % states_explored)
            return None

        # Get node with minimum evaluation function from heap
        h, _, node = heapq.heappop(fringe)
        states_explored += 1

        # Goal test
        if node.is_true(*goal):
            plan = node.plan()
            dur = time() - start
            if verbose:
                print('States Explored: %d' % states_explored)
                print('Time per state: %.3f ms' % (1000*dur / states_explored))
                print('Plan length: %d' % node.cost)
            return plan

        # Expand node if we haven't seen it before
        if node not in closed:
            closed.add(node)

            # Apply all applicable actions to get successors
            successors = set(node.apply(action, monotone)
                             for action in problem.grounded_actions
                             if node.is_true(action.preconditions,
                                             action.num_preconditions))

            # Compute heuristic and add to fringe
            for successor in successors:
                if successor not in closed:
                    f = successor.cost + heuristic(successor)
                    heapq.heappush(fringe, (f, -successor.cost, successor))


########## HEURISTICS ##########

def null_heuristic(state):
    """Admissible, but trivial heuristic"""
    return 0

def plan_cost(plan):
    """Convert a plan to a cost, handling nonexistent plans"""
    if plan is None:
        return float('inf')
    else:
        return len(plan)

def monotone_heuristic(problem):
    """Heuristic that finds plans using only add lists of actions"""
    def h(state):
        monotone_plan = planner(problem, null_heuristic, state, monotone=True, verbose=False)
        return plan_cost(monotone_plan)
    return h

def subgoal_heuristic(problem):
    """Heuristic that computes the max cost of plans across all subgoals"""
    def h(state):
        costs = []
        for g in problem.goals:
            subgoal_plan = planner(problem, null_heuristic, state, ((g,), ()))
            costs.append(plan_cost(subgoal_plan))
        for g in problem.num_goals:
            subgoal_plan = planner(problem, null_heuristic, state, ((), (g,)))
            costs.append(plan_cost(subgoal_plan))
        return max(costs)
    return h
