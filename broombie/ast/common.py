def q(obj):
    if obj is None:
        return "?"
    return str(obj)


def q_arr_str(arr_str):
    if arr_str is None:
        return "?"
    return " ".join(arr_str)


class Ast:
    """AST node base class."""
    precedence = 0

    def build(self, truth, lnodes, rnodes):
        """Called during AST building phase to build the AST subtree under this node."""
        return self

    def evaluate(self, truth):
        raise NotImplementedError()

    def __repr__(self):
        return "<{cls}:{self}>".format(cls=type(self).__name__, self=q(self))
