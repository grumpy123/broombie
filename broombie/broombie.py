"""Broombie is an over-helpful, hyper-functional language.

The main design goal of the language is to limit the use of special characters the minimum. Most special characters
require some key combination to be typed, and I hate key combinations :)

The second design goal is to have minimum syntax. No semi-colons at the end of statements, no braces around the
function body, etc. No parenthesis for function call.

Functions are evaluated in the classic order
1 + 2 * 2
5

There will be something in the syntax to differentiate between function call and function reference.

todo: support operator precedence

"""
from .ast import build_ast
from .parser import parse
from .tokenizer import tokenize
from .truth import Truth


class Broombie:
    def __init__(self):
        self.truth = Truth()
        self.latest = None

    def evaluate(self, statement):
        return statement.evaluate(self.truth)

    def _run_line(self, line):
        if not line.strip():
            return
        nodes = parse(tokenize(line))
        ast = build_ast(nodes, self.truth)
        self.latest = self.evaluate(ast)

    def run(self, text):
        for line in text.splitlines():
            self._run_line(line)
        return self.latest


def run(text):
    repl = Broombie()
    return repl.run(text)
