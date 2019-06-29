from enum import Enum

from broombie.ast.types import Number, Bool
from broombie.errors import BroombieOperationNotSupportedError, BroombieInternalError


class Operator(Enum):
    Add = "+"
    Subtract = "-"
    Multiply = "*"
    Divide = "/"

    Equal = "=="
    Different = "!="
    Less = "<"
    LessOrEqual = "<="
    Greater = ">"
    GreaterOrEqual = ">="

    And = "and"
    Or = "or"
    Xor = "xor"


arith_operations = {
    Operator.Add: {Number: lambda a, b: a + b},
    Operator.Subtract: {Number: lambda a, b: a - b},
    Operator.Multiply: {Number: lambda a, b: a * b},
    Operator.Divide: {Number: lambda a, b: a // b},
}

comp_operations = {
    Operator.Equal: {Number: lambda a, b: a == b},
    Operator.Different: {Number: lambda a, b: a != b},
    Operator.Less: {Number: lambda a, b: a < b},
    Operator.LessOrEqual: {Number: lambda a, b: a <= b},
    Operator.Greater: {Number: lambda a, b: a > b},
    Operator.GreaterOrEqual: {Number: lambda a, b: a >= b},
}

bool_operations = {
    Operator.And: {Bool: lambda a, b: a and b},
    Operator.Or: {Bool: lambda a, b: a or b},
    Operator.Xor: {Bool: lambda a, b: a != b},
}


def confirm_same_types(operation, value1, value2):
    if type(value1) != type(value2):
        raise BroombieOperationNotSupportedError(operation, value1, value2)


def compute(operation, value1, value2):
    confirm_same_types(operation, value1, value2)
    data_type = type(value1)

    operation_map = arith_operations.get(operation)
    if operation_map:
        return _compute(operation, value1, value2, operation_map, data_type, data_type)

    operation_map = comp_operations.get(operation)
    if operation_map:
        return _compute(operation, value1, value2, operation_map, data_type, Bool)

    operation_map = bool_operations.get(operation)
    if operation_map:
        return _compute(operation, value1, value2, operation_map, data_type, Bool)

    raise BroombieInternalError("Operator {operation} is not implemented.".format(operation=operation.value))


def _compute(operation, value1, value2, operation_map, data_type, return_type):
    impl = operation_map.get(data_type)
    if impl is None:
        raise BroombieOperationNotSupportedError(operation, value1, value2)
    return return_type(impl(value1.value, value2.value))
