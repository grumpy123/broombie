from broombie.runtime.arith import compute, ADD, SUB, MUL, DIV
from .common import Ast, q


class BinaryOperator(Ast):
    """Base class for all binary operators."""
    operation = None

    def __init__(self):
        self.left_child = None
        self.right_child = None

    def build(self, truth, lnodes, rnodes):
        self.left_child = lnodes.pop()
        self.right_child = rnodes.pop()
        return self

    def evaluate(self, truth):
        left_val = self.left_child.evaluate(truth)
        right_val = self.right_child.evaluate(truth)
        return compute(self.operation, left_val, right_val)

    def __str__(self):
        return "({left} {operation} {right})".format(left=q(self.left_child), operation=q(self.operation),
                                                     right=q(self.right_child))


# AssignOperator is in ast.function package, as it's really a function definition operator


class AddOperator(BinaryOperator):
    precedence = 6
    operation = ADD


class SubtractOperator(BinaryOperator):
    precedence = 6
    operation = SUB


class MultiplyOperator(BinaryOperator):
    precedence = 3
    operation = MUL


class DivideOperator(BinaryOperator):
    precedence = 3
    operation = DIV
