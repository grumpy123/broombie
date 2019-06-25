class Ast:
    precedence = 0

    def complete(self, truth, lnodes, rnodes):
        pass

    def evaluate(self, truth):
        raise NotImplementedError()


class BinaryOperator(Ast):
    def __init__(self):
        self.left_child = None
        self.right_child = None

    def complete(self, truth, lnodes, rnodes):
        self.left_child = lnodes.pop()
        self.right_child = rnodes.pop()


class AddOperator(BinaryOperator):
    precedence = 6

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) + self.right_child.evaluate(truth)


class SubtractOperator(BinaryOperator):
    precedence = 6

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) - self.right_child.evaluate(truth)


class MultiplyOperator(BinaryOperator):
    precedence = 3

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) * self.right_child.evaluate(truth)


class DivideOperator(BinaryOperator):
    precedence = 3

    def evaluate(self, truth):
        return self.left_child.evaluate(truth) // self.right_child.evaluate(truth)


class AssignOperator(Ast):
    precedence = 10

    def complete(self, truth, lnodes, rnodes):
        assert all([isinstance(n, Object) for n in lnodes])
        self.name = lnodes[0].name
        self.args = [n.name for n in lnodes[1:]]
        lnodes.clear()
        self.func = Function(self.name, self.args, rnodes.pop())

    def evaluate(self, truth):
        truth[self.name] = self.func


class Number(Ast):
    precedence = 0

    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self, truth):
        return self.value


class Object(Ast):
    precedence = 1

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.func = None

    def complete(self, truth, lnodes, rnodes):
        if self.name not in truth:
            # l-value, nothing to do
            return
        self.func = truth[self.name]
        for a in self.func.args:
            truth[a] = rnodes.pop()

    def evaluate(self, truth):
        self.func = truth[self.name]
        return self.func.evaluate(truth)


class Function(Ast):
    def __init__(self, name, args, body):
        super().__init__()
        self.name = name
        self.args = args
        self.body = body

    def evaluate(self, truth):
        return self.body.evaluate(truth)


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
            if n.precedence == precedence:
                n.complete(truth, lnodes, rnodes)
            if precedence < n.precedence < next_precedence:
                next_precedence = n.precedence
            lnodes.append(n)

    assert len(lnodes) == 1
    return lnodes.pop()
