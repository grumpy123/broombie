from .errors import BroombieInternalError
from .truth import Truth


def q(obj):
    if obj is None:
        return "?"
    return str(obj)


def q_arr_str(arr_str):
    if arr_str is None:
        return "?"
    return " ".join(arr_str)


class Ast:
    """AST node base class."""
    precedence = 0

    def build(self, truth, lnodes, rnodes):
        """Called during AST building phase to build the AST subtree under this node."""
        return self

    def evaluate(self, truth):
        raise NotImplementedError()

    def __repr__(self):
        return "<{cls}:{self}>".format(cls=type(self).__name__, self=q(self))


class BinaryOperator(Ast):
    """Base class for all binary operators."""
    symbol = None

    def __init__(self):
        self.left_child = None
        self.right_child = None

    def build(self, truth, lnodes, rnodes):
        self.left_child = lnodes.pop()
        self.right_child = rnodes.pop()
        return self

    def __str__(self):
        return "({left} {symbol} {right})".format(left=q(self.left_child), symbol=q(self.symbol),
                                                  right=q(self.right_child))


class AddOperator(BinaryOperator):
    precedence = 6
    symbol = "+"

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) + self.right_child.evaluate(truth)


class SubtractOperator(BinaryOperator):
    precedence = 6
    symbol = "-"

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) - self.right_child.evaluate(truth)


class MultiplyOperator(BinaryOperator):
    precedence = 3
    symbol = "*"

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) * self.right_child.evaluate(truth)


class DivideOperator(BinaryOperator):
    precedence = 3
    symbol = "/"

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) // self.right_child.evaluate(truth)


class Number(Ast):
    precedence = 0

    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self, truth):
        return self.value

    def __str__(self):
        return str(self.value)


class RefPlaceholder(Ast):
    precedence = 1

    def __init__(self, name):
        super().__init__()
        self.name = name

    def build(self, truth, lnodes, rnodes):
        if self.name not in truth:
            # l-value, nothing to do
            return NameRef(self.name)

        func = truth[self.name]
        args = {}
        for a in func.arg_names:
            args[a] = rnodes.pop()
        return FunctionCall(self.name, func, args)

    def evaluate(self, truth):
        raise BroombieInternalError("Placeholder object is not (expected to be) callable.")

    def __str__(self):
        return self.name


class NameRef(Ast):
    precedence = 1

    def __init__(self, name):
        super().__init__()
        self.name = name

    def evaluate(self, truth):
        return truth[self.name].evaluate(truth)

    def __str__(self):
        return self.name


class Function(Ast):
    def __init__(self, name, arg_names, body):
        super().__init__()
        self.name = name
        self.arg_names = arg_names
        self.body = body

    def evaluate(self, truth):
        """
        :param truth: Truth object containing values for all args in arg_names
        :return:
        """
        return self.body.evaluate(truth)

    def __str__(self):
        args_str = "".join([" " + a for a in self.arg_names])
        return "{name}{args} = {body}".format(name=q(self.name), args=q(args_str), body=q(self.body))


class FunctionCall(Ast):
    precedence = 1

    def __init__(self, name, func, args):
        super().__init__()
        self.name = name
        self.func = func
        self.args = args

    def evaluate(self, truth):
        local_truth = Truth(truth.ground_truth())
        if self.args:
            for arg_name, arg_body in self.args.items():
                local_truth[arg_name] = Number(arg_body.evaluate(truth))
        return self.func.evaluate(local_truth)

    def __str__(self):
        return "{name} {func}".format(name=q(self.name), func=q(self.func))


class AssignOperator(Ast):
    precedence = 10

    def __init__(self):
        super().__init__()
        self.name = None
        self.args = None
        self.func = None

    def build(self, truth, lnodes, rnodes):
        assert all([isinstance(n, NameRef) for n in lnodes])
        self.name = lnodes[0].name
        self.args = [n.name for n in lnodes[1:]]
        lnodes.clear()
        self.func = Function(self.name, self.args, rnodes.pop())
        truth[self.name] = self.func
        return None

    def evaluate(self, truth):
        raise BroombieInternalError("Assignment object is not (expected to be) callable.")

    def __str__(self):
        return "{name} := {args} -> {func}".format(name=q(self.name), args=q_arr_str(self.args), func=q(self.func))


def build_ast(nodes, truth):
    """Converts list of typed nodes into AST.
    """
    # todo: error handling
    TERMINATOR = 1000
    lnodes = nodes
    next_precedence = 0
    while next_precedence < TERMINATOR:
        precedence = next_precedence
        next_precedence = TERMINATOR
        rnodes = list(reversed(lnodes))
        lnodes = []
        while rnodes:
            n = rnodes.pop()
            if precedence < n.precedence < next_precedence:
                next_precedence = n.precedence
            elif n.precedence == precedence:
                n = n.build(truth, lnodes, rnodes)
            if n is not None:
                lnodes.append(n)

    return lnodes.pop() if lnodes else None
