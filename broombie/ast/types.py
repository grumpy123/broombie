from .common import Ast


class Number(Ast):
    precedence = 0

    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self, truth):
        return self

    def __str__(self):
        return str(self.value)
