def peekImpl(i):
    return lambda xs: lambda: xs[i]


def _pokeImpl(xs, i, a):
    xs[i] = a


pokeImpl = lambda i: lambda a: lambda xs: lambda: _pokeImpl(xs, i, a)
