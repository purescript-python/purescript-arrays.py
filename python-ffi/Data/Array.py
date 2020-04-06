import functools

_buitins = {"range": range, "filter": filter}

globals()["range"] = lambda start: lambda end: list(_buitins["range"](start, end))


replicate = lambda count: lambda value: [value for _ in range(count)]


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
        count = 0
        xs = lst
        while xs is not None:
            result[count] = xs.head
            count += 1
            xs = xs.tail
        return result

    def result(foldr):
        def ap(xs):
            return listToArray(foldr(curryCons)(emptyList)(xs))

        return ap

    return result


fromFoldableImpl = _mkFromFoldableImpl()

length = lambda xs: len(xs)

cons = lambda e: lambda l: [e, *l]

sonc = lambda xs: lambda x: [*xs, x]


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
    for i, x in reversed(enumerate(xs)):
        if f(x):
            return just(i)
    return nothing


def findLastIndexImpl(just):
    return lambda nothing: lambda f: lambda xs: _findLastIndexImpl(just, nothing, f, xs)


def _insertAtImpl(just, nothing, i, a, l):
    if i < 0 or i >= len(l):
        return nothing
    ll = l.copy()
    ll.insert(i, a)
    return just(ll)


_insertAt = lambda just: lambda nothing: lambda i: lambda a: lambda l: _insertAtImpl(
    just, nothing, i, a, l
)


def _deleteAtImpl(just, nothing, i, a, l):
    if i < 0 or i >= len(l):
        return nothing
    return just(l[:i] + l[i + 1 :])


_deletetAt = lambda just: lambda nothing: lambda i: lambda a: lambda l: _insertAtImpl(
    just, nothing, i, a, l
)


def _updateAtImpl(just, nothing, i, a, l):
    if i < 0 or i >= len(l):
        return nothing
    ll = l.copy()
    ll[i] = a
    return just(ll)


_updateAt = lambda just: lambda nothing: lambda i: lambda a: lambda l: _insertAtImpl(
    just, nothing, i, a, l
)

reverse = lambda xs: reversed(xs)


def concat(xss):
    result = []
    for x in xss:
        result.extend(x)
    return result


filter = lambda f: lambda xs: list(_buitins["filter"](f, xs))


def partition(f):
    def result(xs):
        yes = []
        no = []
        for x in xs:
            if f(x):
                yes.append(x)
            else:
                no.append(x)
        return {"yes": yes, "no": no}

    return result


sortImpl = lambda f: lambda xs: sorted(
    xs, key=functools.cmp_to_key(lambda a, b: f(a)(b))
)

slice = lambda s: lambda e: lambda xs: xs[s:e]

take = lambda n: lambda xs: xs[:n]
drop = lambda n: lambda xs: xs[n:]

zipWith = lambda f: lambda xs: lambda ys: list(map(f, zip(xs, ys)))

unsafeIndexImpl = lambda xs: lambda n: xs[n]
