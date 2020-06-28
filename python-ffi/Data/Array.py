import functools

_buitins = {"range": range, "filter": filter}


def _rangeImpl(start):
    def ap(end):
        step = 1 if start <= end else -1
        return tuple(_buitins["range"](start, end + step, step))

    return ap


globals()["range"] = _rangeImpl


replicate = lambda count: lambda value: tuple([value for _ in _buitins["range"](count)])


def _mkFromFoldableImpl():
    class Cons:
        def __init__(self, head, tail):
            self.head = head
            self.tail = tail

    emptyList = None

    def curryCons(head):
        def ap(tail):
            return Cons(head, tail)

        return ap

    def listToArray(lst):
        result = []
        xs = lst
        while xs is not None:
            result.append(xs.head)
            xs = xs.tail
        return tuple(result)

    def result(foldr):
        def ap(xs):
            return listToArray(foldr(curryCons)(emptyList)(xs))

        return ap

    return result

# TODO: discuss performance consideration with alternative implementation
# at least should we use 2-tuple instead of class?
# current implementation is aiming to mimic JS implementation as much as possible
# same problem in NonEmpty.Internal.py
fromFoldableImpl = _mkFromFoldableImpl()

length = lambda xs: len(xs)

cons = lambda e: lambda l: (e, *l)

snoc = lambda xs: lambda x: (*xs, x)


def unconsImpl(empty):
    def next_f(next_):
        def xs_(xs):
            if len(xs) == 0:
                return empty(None)
            else:
                return next_(xs[0])(xs[1:])

        return xs_

    return next_f


globals()["uncons'"] = unconsImpl


def _indexImpl(just, nothing, xs, i):
    if i < 0 or i >= len(xs):
        return nothing
    else:
        return just(xs[i])


indexImpl = lambda just: lambda nothing: lambda xs: lambda i: _indexImpl(
    just, nothing, xs, i
)


def _findIndexImpl(just, nothing, f, xs):
    for i, x in enumerate(xs):
        if f(x):
            return just(i)
    return nothing


findIndexImpl = lambda just: lambda nothing: lambda f: lambda xs: _findIndexImpl(
    just, nothing, f, xs
)


def _findLastIndexImpl(just, nothing, f, xs):
    for i, x in reversed(list(enumerate(xs))):
        if f(x):
            return just(i)
    return nothing


def findLastIndexImpl(just):
    return lambda nothing: lambda f: lambda xs: _findLastIndexImpl(just, nothing, f, xs)


def _insertAtImpl(just, nothing, i, a, l):
    if i < 0 or i > len(l):
        return nothing
    # TODO: discuss performance consideration with alternative implementation
    # (*l[i-1], a, *l[i:])
    ll = list(l)
    ll.insert(i, a)
    return just(tuple(ll))


_insertAt = lambda just: lambda nothing: lambda i: lambda a: lambda l: _insertAtImpl(
    just, nothing, i, a, l
)


def _deleteAtImpl(just, nothing, i, l):
    if i < 0 or i >= len(l):
        return nothing
    return just(l[:i] + l[i + 1 :])


_deleteAt = lambda just: lambda nothing: lambda i: lambda l: _deleteAtImpl(
    just, nothing, i, l
)


def _updateAtImpl(just, nothing, i, a, l):
    if i < 0 or i >= len(l):
        return nothing
    ll = list(l)
    ll[i] = a
    return just(tuple(ll))


_updateAt = lambda just: lambda nothing: lambda i: lambda a: lambda l: _updateAtImpl(
    just, nothing, i, a, l
)

reverse = lambda xs: tuple(reversed(xs))


def concat(xss):
    result = []
    for x in xss:
        result.extend(x)
    return tuple(result)


filter = lambda f: lambda xs: tuple(_buitins["filter"](f, xs))


def partition(f):
    def result(xs):
        yes = []
        no = []
        for x in xs:
            if f(x):
                yes.append(x)
            else:
                no.append(x)
        return {"yes": tuple(yes), "no": tuple(no)}

    return result


sortImpl = lambda f: lambda xs: tuple(
    sorted(xs, key=functools.cmp_to_key(lambda a, b: f(a)(b)))
)

slice = lambda s: lambda e: lambda xs: xs[s:e]

take = lambda n: lambda xs: xs[: max(n, 0)]
drop = lambda n: lambda xs: xs[max(n, 0) :]

zipWith = lambda f: lambda xs: lambda ys: tuple(
    map(lambda t: f(t[0])(t[1]), zip(xs, ys))
)

unsafeIndexImpl = lambda xs: lambda n: xs[n]
