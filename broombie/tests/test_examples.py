from inspect import cleandoc

from broombie.ast.types import Number
from broombie.broombie import run


def test_literal():
    _run(0, "0")


def test_basic_expressions():
    _run(2, "1 + 1")
    _run(2, "3 - 1")
    _run(6, "2 * 3")
    _run(2, "4 / 2")


def test_nested_expressions():
    _run(3, "1 + 1 + 1")
    _run(1, "3 - 1 - 1")
    _run(3, "2 * 3 + 1 - 2 * 2")
    _run(5, "3 + 4 / 2")


def test_consts():
    _run(5, """
        a = 2
        b = 3
        a + b
    """)


def test_functions():
    _run(4, """
        f a = 2 * a
        f 2
    """)
    _run(10, """
        f x = 2 * x
        g x = x + 1
        f 2 + g 5
    """)
    _run(7, """
        f x = 2 * x
        g x = f 1 + x
        f 2 + g 1
    """)
    _run(7, """
        f x = 2 * x
        g x = f x + 1
        h x y = f x + g y
        h 2 1
    """)


def _run(expected_result, program):
    result = run(cleandoc(program))
    assert type(result) == Number
    assert result.value == expected_result
