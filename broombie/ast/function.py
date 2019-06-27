from broombie.errors import BroombieInternalError
from broombie.truth import Truth
from .common import Ast, q, q_arr_str


class RefPlaceholder(Ast):
    precedence = 1

    def __init__(self, name):
        super().__init__()
        self.name = name

    def build(self, truth, lnodes, rnodes):
        if self.name not in truth:
            # l-value, nothing to do
            return NameRef(self.name)

        return FunctionCall(self.name)

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


class Function:
    def __init__(self, name, arg_names, body):
        self.name = name
        self.arg_names = arg_names
        self.body = body

    def __str__(self):
        args_str = "".join([" " + a for a in self.arg_names])
        return "{name}{args}".format(name=q(self.name), args=q(args_str))

    def __repr__(self):
        return "<Function:{self}>".format(self=self)


class FunctionCall(Ast):
    precedence = 2

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.func = None
        self.args = None

    def build(self, truth, lnodes, rnodes):
        if self.name not in truth:
            raise BroombieInternalError("Expected to only get here if the function is defined.")

        self.func = truth[self.name]
        self.args = {}
        for a in self.func.arg_names:
            self.args[a] = rnodes.pop()
        return self

    def evaluate(self, truth):
        """Override of evaluate method. See notes on arguments.
        :param truth: Truth object containing values for all args in arg_names
        :return: Function result
        """
        local_truth = Truth(truth.ground_truth())
        if self.args:
            for arg_name, arg_body in self.args.items():
                local_truth[arg_name] = arg_body.evaluate(truth)
        return self.func.body.evaluate(local_truth)

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
        args = [n.name for n in lnodes[1:]]
        lnodes.clear()
        func = Function(self.name, args, rnodes.pop())
        truth[self.name] = func
        return None

    def evaluate(self, truth):
        raise BroombieInternalError("Assignment object is not (expected to be) callable.")

    def __str__(self):
        return "{name} := {args} -> {func}".format(name=q(self.name), args=q_arr_str(self.args), func=q(self.func))
