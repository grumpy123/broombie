class Ast:
    precedence = 0

    def complete(self, lnodes, rnodes):
        pass

    def evaluate(self, truth):
        raise NotImplementedError()


class BinaryOperator(Ast):
    def __init__(self):
        self.left_child = None
        self.right_child = None

    def complete(self, lnodes, rnodes):
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


class AssignOperator(BinaryOperator):
    precedence = 10

    def evaluate(self, truth):
        assert isinstance(self.left_child, Object)
        truth[self.left_child.name] = self.right_child


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

    def evaluate(self, truth):
        return truth[self.name].evaluate(truth)


def build_ast(nodes):
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
                n.complete(lnodes, rnodes)
            if precedence < n.precedence < next_precedence:
                next_precedence = n.precedence
            lnodes.append(n)

    return lnodes
