from .ast import build_ast, AddOperator, SubtractOperator, MultiplyOperator, DivideOperator, AssignOperator, Number, \
    Object


class AstParser:
    def try_parse(self, token):
        return None


class KeywordParser(AstParser):
    def __init__(self, token, key_type):
        self.token = token
        self.key_type = key_type

    def try_parse(self, token):
        if token == self.token:
            return self.key_type()
        return None


class AddOperatorParser(KeywordParser):
    def __init__(self):
        super().__init__("+", AddOperator)


class SubtractOperatorParser(KeywordParser):
    def __init__(self):
        super().__init__("-", SubtractOperator)


class MultiplyOperatorParser(KeywordParser):
    def __init__(self):
        super().__init__("*", MultiplyOperator)


class DivideOperatorParser(KeywordParser):
    def __init__(self):
        super().__init__("/", DivideOperator)


class AssignOperatorParser(KeywordParser):
    def __init__(self):
        super().__init__("=", AssignOperator)


class NumberParser(AstParser):
    def try_parse(self, token):
        try:
            value = int(token)
            return Number(value)
        except ValueError:
            return None


class ObjectParser(AstParser):
    def try_parse(self, token):
        if token.isalpha():
            return Object(token)
        return None


elements = [AddOperatorParser(), SubtractOperatorParser(), MultiplyOperatorParser(), DivideOperatorParser(),
            AssignOperatorParser(), NumberParser(), ObjectParser()]


def parse_token(t):
    for e in elements:
        node = e.try_parse(t)
        if node:
            return node

    raise ValueError("Don't know how to parse '{t}'".format(t=t))


def parse(tokens):
    nodes = [
        parse_token(t) for t in tokens
    ]
    return build_ast(nodes)
