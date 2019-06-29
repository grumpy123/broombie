from broombie.errors import BroombieInternalError
from .common import Ast


class Value(Ast):
    precedence = 0
    value_type = None

    def __init__(self, value):
        super().__init__()
        if type(value) != self.value_type:
            raise BroombieInternalError(
                "Wrong value '{value}' for data type {type}.".format(value=value, type=self.value_type))
        self.value = value

    def evaluate(self, truth):
        return self

    def __str__(self):
        return str(self.value)


class Number(Value):
    precedence = 0
    value_type = int


class Bool(Value):
    precedence = 0
    value_type = bool
