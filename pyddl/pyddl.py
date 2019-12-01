"""
Classes and functions that allow creating a PDDL-like
problem and domain definition for planning
"""
from itertools import product
import operator as ops

NUM_OPS = {
    '>' : ops.gt,
    '<' : ops.lt,
    '=' : ops.eq,
    '>=': ops.ge,
    '<=': ops.le
}

class Domain(object):

    def __init__(self, actions=()):
        """
        Represents a PDDL-like Problem Domain
        @arg actions : list of Action objects
        """
        self.actions = tuple(actions)

    def ground(self, objects):
        """
        Ground all action schemas given a dictionary
        of objects keyed by type
        """
        grounded_actions = list()
        for action in self.actions:
            param_lists = [objects[t] for t in action.types]
            param_combos = set()
            for params in product(*param_lists):
                param_set = frozenset(params)
                if action.unique and len(param_set) != len(params):
                    continue
                if action.no_permute and param_set in param_combos:
                    continue
                param_combos.add(param_set)
                grounded_actions.append(action.ground(*params))
        return grounded_actions

class Problem(object):

    def __init__(self, domain, objects, init=(), goal=()):
        """
        Represents a PDDL Problem Specification
        @arg domain : Domain object specifying domain
        @arg objects : dictionary of object tuples keyed by type
        @arg init : tuple of initial state predicates
        @arg goal : tuple of goal state predicates
        """
        # Ground actions from domain
        self.grounded_actions = domain.ground(objects)

        # Parse Initial State
        predicates = list()
        functions = dict()
        for predicate in init:
            if predicate[0] == '=':
                functions[predicate[1]] = predicate[2]
            else:
                predicates.append(predicate)
        self.initial_state = State(predicates, functions)

        # Parse Goal State
        self.goals = list()
        self.num_goals = list()
        for g in goal:
            if g[0] in NUM_OPS:
                ng = _num_pred(NUM_OPS[g[0]], *g[1:])
                self.num_goals.append(ng)
            else:
                self.goals.append(g)

class State(object):

    def __init__(self, predicates, functions, cost=0, predecessor=None):
        """Represents a state for A* search"""
        self.predicates = frozenset(predicates)
        self.functions = tuple(functions.items())
        self.f_dict = functions
        self.predecessor = predecessor
        self.cost = cost

    def is_true(self, predicates, num_predicates):
        return (all(p in self.predicates for p in predicates) and
                all(np(self) for np in num_predicates))

    def apply(self, action, monotone=False):
        """
        Apply the action to this state to produce a new state.
        If monotone, ignore the delete list (for A* heuristic)
        """
        new_preds = set(self.predicates)
        new_preds |= set(action.add_effects)
        if not monotone:
            new_preds -= set(action.del_effects)
        new_functions = dict()
        new_functions.update(self.functions)
        for function, value in action.num_effects:
            new_functions[function] += value(self)
        return State(new_preds, new_functions, self.cost + 1, (self, action))

    def plan(self):
        """
        Follow backpointers to successor states
        to produce a plan.
        """
        plan = list()
        n = self
        while n.predecessor is not None:
            plan.append(n.predecessor[1])
            n = n.predecessor[0]
        plan.reverse()
        return plan

    # Implement __hash__ and __eq__ so we can easily
    # check if we've encountered this state before

    def __hash__(self):
        return hash((self.predicates, self.functions))

    def __eq__(self, other):
        return ((self.predicates, self.functions) ==
                (other.predicates, other.functions))

    def __str__(self):
        return ('Predicates:\n%s' % '\n'.join(map(str, self.predicates))
                +'\nFunctions:\n%s' % '\n'.join(map(str, self.functions)))
    def __lt__(self, other):
        return hash(self) < hash(other)

def neg(effect):
    """
    Makes the given effect a negative (delete) effect, like 'not' in PDDL.
    """
    return (-1, effect)

class Action(object):
    """
    An action schema
    """
    def __init__(self, name, parameters=(), preconditions=(), effects=(),
                 unique=False, no_permute=False):
        """
        A PDDL-like action schema
        @arg name : action name for display purposes
        @arg parameters : tuple of ('type', 'param_name') tuples indicating
                          action parameters
        @arg precondtions : tuple of preconditions for the action
        @arg effects : tuple of effects of the action
        @arg unique : if True, only ground with unique arguments (no duplicates)
        @arg no_permute : if True, do not ground an action twice with the same
                          set of (permuted) arguments
        """
        self.name = name
        if len(parameters) > 0:
            self.types, self.arg_names = zip(*parameters)
        else:
            self.types = tuple()
            self.arg_names = tuple()
        self.preconditions = preconditions
        self.effects = effects
        self.unique = unique
        self.no_permute = no_permute

    def ground(self, *args):
        return _GroundedAction(self, *args)

    def __str__(self):
        arglist = ', '.join(['%s - %s' % pair for pair in zip(self.arg_names, self.types)])
        return '%s(%s)' % (self.name, arglist)

def _grounder(arg_names, args):
    """
    Returns a function for grounding predicates and function symbols
    """
    namemap = dict()
    for arg_name, arg in zip(arg_names, args):
        namemap[arg_name] = arg
    def _ground_by_names(predicate):
        return predicate[0:1] + tuple(namemap.get(arg, arg) for arg in predicate[1:])
    return _ground_by_names

def _num_pred(op, x, y):
    """
    Returns a numerical predicate that is called on a State.
    """
    def predicate(state):
        operands = [0, 0]
        for i, o in enumerate((x, y)):
            if type(o) == int:
                operands[i] = o
            else:
                operands[i] = state.f_dict[o]
        return op(*operands)
    return predicate

def _num_effect(ground, sign, x):
    """
    Returns a numerical effect that is called on a State.
    """
    if type(x) != int:
        x = ground(x)

    def effect(state):
        if type(x) == int:
            return sign*x
        else:
            return sign*state.f_dict[x]

    return effect

class _GroundedAction(object):
    """
    An action schema that has been grounded with objects
    """
    def __init__(self, action, *args):
        self.name = action.name
        ground = _grounder(action.arg_names, args)

        # Ground Action Signature
        self.sig = ground((self.name,) + action.arg_names)

        # Ground Preconditions
        self.preconditions = list()
        self.num_preconditions = list()
        for pre in action.preconditions:
            if pre[0] in NUM_OPS:
                operands = [0, 0]
                for i in range(2):
                    if type(pre[i + 1]) == int:
                        operands[i] = pre[i + 1]
                    else:
                        operands[i] = ground(pre[i + 1])
                np = _num_pred(NUM_OPS[pre[0]], *operands)
                self.num_preconditions.append(np)
            else:
                self.preconditions.append(ground(pre))

        # Ground Effects
        self.add_effects = list()
        self.del_effects = list()
        self.num_effects = list()
        for effect in action.effects:
            if effect[0] == -1:
                self.del_effects.append(ground(effect[1]))
            elif effect[0] == '+=':
                function = ground(effect[1])
                value = _num_effect(ground, 1, effect[2])
                self.num_effects.append((function, value))
            elif effect[0] == '-=':
                function = ground(effect[1])
                value = _num_effect(ground, -1, effect[2])
                self.num_effects.append((function, value))
            else:
                self.add_effects.append(ground(effect))

    def __str__(self):
        arglist = ', '.join(map(str, self.sig[1:]))
        return '%s(%s)' % (self.sig[0], arglist)
