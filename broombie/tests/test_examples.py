from inspect import cleandoc

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


def _run(result, program):
    assert run(cleandoc(program)) == result
