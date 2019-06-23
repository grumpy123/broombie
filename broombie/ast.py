class Ast:
    num_left_children = 0
    num_right_children = 0

    def __init__(self):
        self.left_children = []
        self.right_children = []

    def needs_left(self):
        return len(self.left_children) < self.num_left_children

    def needs_right(self):
        return len(self.right_children) < self.num_right_children

    def add_left(self, n):
        self.left_children.append(n)

    def add_right(self, n):
        self.right_children.append(n)

    def is_complete(self):
        return not self.needs_left() and not self.needs_right()

    def evaluate(self, truth):
        raise NotImplementedError()


class BinaryOperator(Ast):
    num_left_children = 1
    num_right_children = 1


class AddOperator(BinaryOperator):
    def evaluate(self, truth):
        return self.left_children[0].evaluate(truth) + self.right_children[0].evaluate(truth)


class SubtractOperator(BinaryOperator):
    def evaluate(self, truth):
        return self.left_children[0].evaluate(truth) - self.right_children[0].evaluate(truth)


class MultiplyOperator(BinaryOperator):
    def evaluate(self, truth):
        return self.left_children[0].evaluate(truth) * self.right_children[0].evaluate(truth)


class DivideOperator(BinaryOperator):
    def evaluate(self, truth):
        return self.left_children[0].evaluate(truth) // self.right_children[0].evaluate(truth)


class AssignOperator(BinaryOperator):
    def evaluate(self, truth):
        assert isinstance(self.left_children[0], Object)
        truth[self.left_children[0].name] = self.right_children[0].evaluate(truth)


class Number(Ast):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def is_complete(self):
        return True

    def evaluate(self, truth):
        return self.value


class Object(Ast):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def is_complete(self):
        return True

    def evaluate(self, truth):
        return truth[self.name]


def build_ast(nodes):
    """Converts list of typed nodes into AST.
    """
    # todo: error handling
    lnodes = []
    rnodes = list(reversed(nodes))
    while rnodes:
        n = rnodes.pop()
        if n.is_complete():
            lnodes.append(n)
            continue
        while n.needs_left():
            n.add_left(lnodes.pop())
        while n.needs_right():
            n.add_right(get_right_child(rnodes))
        lnodes.append(n)

    # todo: Validate no leftover nodes
    return lnodes


def get_right_child(rnodes):
    return rnodes.pop()
