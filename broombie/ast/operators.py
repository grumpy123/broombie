from broombie.runtime.arith import compute, Operator
from .common import Ast, q


class BinaryOperator(Ast):
    """Base class for all binary operators."""
    operator = None

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
        return compute(self.operator, left_val, right_val)

    def __str__(self):
        return "({left} {operation} {right})".format(left=q(self.left_child), operation=q(self.operator),
                                                     right=q(self.right_child))


# AssignOperator is in ast.function package, as it's really a function definition operator


class AddOperator(BinaryOperator):
    precedence = 6
    operator = Operator.Add


class SubtractOperator(BinaryOperator):
    precedence = 6
    operator = Operator.Subtract


class MultiplyOperator(BinaryOperator):
    precedence = 3
    operator = Operator.Multiply


class DivideOperator(BinaryOperator):
    precedence = 3
    operator = Operator.Divide


class EqualOperator(BinaryOperator):
    precedence = 9
    operator = Operator.Equal


class DifferentOperator(BinaryOperator):
    precedence = 9
    operator = Operator.Different


class LessOperator(BinaryOperator):
    precedence = 9
    operator = Operator.Less


class LessOrEqualOperator(BinaryOperator):
    precedence = 9
    operator = Operator.LessOrEqual


class GreaterOperator(BinaryOperator):
    precedence = 9
    operator = Operator.Greater


class GreaterOrEqualOperator(BinaryOperator):
    precedence = 9
    operator = Operator.GreaterOrEqual


class AndOperator(BinaryOperator):
    precedence = 15
    operator = Operator.And


class OrOperator(BinaryOperator):
    precedence = 18
    operator = Operator.Or


class XorOperator(BinaryOperator):
    precedence = 12
    operator = Operator.Xor
