from broombie.errors import BroombieInternalError, BroombieInvalidProgramError


def build_ast(nodes, truth):
    """Converts list of typed nodes into AST.

    It works in rounds, based on operator precedence and executed in order of the precedence. In each round it builds
    nodes of a given precedence, from left to right. Each node being built can:
    1. Consume any number of nodes from the left or right.
    2. (not used yet) Push new nodes to the left or right.
    3. Replace itself with a new node.

    Note: care must be given to create new nodes with precedence higher than currently being processed. We build each
    precedence exactly once, so a new node with lower precedence will never be procesed.
    """
    # todo: error handling
    TERMINATOR = 1000
    lnodes = nodes
    next_precedence = 0
    while next_precedence < TERMINATOR:
        precedence = next_precedence
        next_precedence = TERMINATOR
        rnodes = list(reversed(lnodes))
        lnodes = []
        while rnodes:
            n = rnodes.pop()
            if n.precedence >= precedence:
                if n.precedence == precedence:
                    n = n.build(truth, lnodes, rnodes)
                if n is not None:
                    if n.precedence < precedence:
                        raise BroombieInternalError(
                            "build returned {n} with low precedence, which was already processed.".format(n=n))
                    if precedence < n.precedence < next_precedence:
                        next_precedence = n.precedence
            if n is not None:
                lnodes.append(n)

    if not lnodes:
        return None

    if len(lnodes) > 1:
        raise BroombieInvalidProgramError("Invalid program, too many results.")
    return lnodes.pop()
