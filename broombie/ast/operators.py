from .common import Ast, q
from .types import Number


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

    def evaluate(self, truth):
        left_val = self.left_child.evaluate(truth)
        right_val = self.right_child.evaluate(truth)
        return self._calculate(left_val, right_val)

    def _calculate(self, left_val, right_val):
        raise NotImplementedError()

    def __str__(self):
        return "({left} {symbol} {right})".format(left=q(self.left_child), symbol=q(self.symbol),
                                                  right=q(self.right_child))


class AddOperator(BinaryOperator):
    precedence = 6
    symbol = "+"

    def _calculate(self, left_val, right_val):
        return Number(left_val.value + right_val.value)


class SubtractOperator(BinaryOperator):
    precedence = 6
    symbol = "-"

    def _calculate(self, left_val, right_val):
        return Number(left_val.value - right_val.value)


class MultiplyOperator(BinaryOperator):
    precedence = 3
    symbol = "*"

    def _calculate(self, left_val, right_val):
        return Number(left_val.value * right_val.value)


class DivideOperator(BinaryOperator):
    precedence = 3
    symbol = "/"

    def _calculate(self, left_val, right_val):
        return Number(left_val.value // right_val.value)

# AssignOperator is in ast.function package, as it's really a function definition operator
