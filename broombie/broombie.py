"""Broombie is an over-helpful, hyper-functional language.

Everything in Broombie is a function, including operators.

Language elements are separated by whitespace.

Functions are evaluated in left-first order
1 + 2 * 2
6

todo: Eval operator forces the next operator to be evaluated as sub-expression
= 1 + = 2 * 2
5

todo: support operator precedence?

"""
from .parser import parse
from .tokenizer import tokenize


def evaluate(roots):
    last = None
    for r in roots:
        last = r.evaluate()
    return last


def run(text):
    return evaluate(parse(tokenize(text)))
