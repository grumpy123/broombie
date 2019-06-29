from .ast.function import RefPlaceholder, AssignOperator
from .ast.operators import AddOperator, SubtractOperator, MultiplyOperator, DivideOperator, \
    EqualOperator, DifferentOperator, LessOperator, LessOrEqualOperator, GreaterOperator, GreaterOrEqualOperator, \
    AndOperator, OrOperator, XorOperator
from .ast.types import Number, Bool
from .errors import BroombieParseError


class AstParser:
    def try_parse(self, token):
        raise NotImplementedError()


class KeywordParser(AstParser):
    def __init__(self, token, key_type):
        self.token = token
        self.key_type = key_type

    @staticmethod
    def for_operator(operator_type):
        return KeywordParser(operator_type.operator.value, operator_type)

    def try_parse(self, token):
        if token == self.token:
            return self.key_type()
        return None


class NumberParser(AstParser):
    def try_parse(self, token):
        try:
            value = int(token)
            return Number(value)
        except ValueError:
            return None


class BoolParser(AstParser):
    def try_parse(self, token):
        if token == "true":
            return Bool(True)
        if token == "false":
            return Bool(False)
        return None


class RefParser(AstParser):
    def try_parse(self, token):
        if token.isalpha():
            return RefPlaceholder(token)
        return None


elements = [
    KeywordParser.for_operator(AddOperator),
    KeywordParser.for_operator(SubtractOperator),
    KeywordParser.for_operator(MultiplyOperator),
    KeywordParser.for_operator(DivideOperator),

    KeywordParser.for_operator(EqualOperator),
    KeywordParser.for_operator(DifferentOperator),
    KeywordParser.for_operator(LessOperator),
    KeywordParser.for_operator(LessOrEqualOperator),
    KeywordParser.for_operator(GreaterOperator),
    KeywordParser.for_operator(GreaterOrEqualOperator),

    KeywordParser.for_operator(AndOperator),
    KeywordParser.for_operator(OrOperator),
    KeywordParser.for_operator(XorOperator),
    KeywordParser("=", AssignOperator),
    BoolParser(),
    NumberParser(),
    RefParser()
]


def parse_token(t):
    for e in elements:
        node = e.try_parse(t)
        if node:
            return node

    raise BroombieParseError(t)


def parse(tokens):
    return [parse_token(t) for t in tokens]
