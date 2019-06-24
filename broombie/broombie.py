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
from .parser import parse
from .tokenizer import tokenize


class Broombie:
    def __init__(self):
        self.truth = {}
        self.latest = None

    def evaluate(self, roots):
        last = None
        for r in roots:
            last = r.evaluate(self.truth)
        return last

    def _run_line(self, line):
        if not line.strip():
            return
        self.latest = self.evaluate(parse(tokenize(line)))

    def run(self, text):
        for line in text.splitlines():
            self._run_line(line)
        return self.latest


def run(text):
    repl = Broombie()
    return repl.run(text)
