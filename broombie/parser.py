from .ast.function import RefPlaceholder, AssignOperator
from .ast.operators import AddOperator, SubtractOperator, MultiplyOperator, DivideOperator
from .ast.types import Number
from .errors import BroombieParseError


class AstParser:
    def try_parse(self, token):
        raise NotImplementedError()


class KeywordParser(AstParser):
    def __init__(self, token, key_type):
        self.token = token
        self.key_type = key_type

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


class RefParser(AstParser):
    def try_parse(self, token):
        if token.isalpha():
            return RefPlaceholder(token)
        return None


elements = [
    KeywordParser("+", AddOperator),
    KeywordParser("-", SubtractOperator),
    KeywordParser("*", MultiplyOperator),
    KeywordParser("/", DivideOperator),
    KeywordParser("=", AssignOperator),
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
