from broombie.ast.types import Number
from broombie.errors import BroombieOperationNotSupportedError

ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"

arith_operations = {
    ADD: {Number: lambda a, b: a + b},
    SUB: {Number: lambda a, b: a - b},
    MUL: {Number: lambda a, b: a * b},
    DIV: {Number: lambda a, b: a // b},
}


def confirm_same_types(operation, value1, value2):
    if type(value1) != type(value2):
        raise BroombieOperationNotSupportedError(operation, value1, value2)


def compute(operation, value1, value2):
    operation_map = arith_operations[operation]
    confirm_same_types(operation, value1, value2)
    data_type = type(value1)
    impl = operation_map.get(data_type)
    if impl is None:
        raise BroombieOperationNotSupportedError(operation, value1, value2)
    return data_type(impl(value1.value, value2.value))
