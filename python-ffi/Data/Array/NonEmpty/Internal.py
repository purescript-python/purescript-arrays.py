import functools


def fold1Impl(f):
    def result(xs):
        acc = xs[0]
        lxs = len(xs)
        for i in range(1, lxs):
            acc = f(acc)(xs[i])
        return acc
        # return functools.reduce(lambda acc, cur: f(acc)(cur), xs)

    return result


class Cont:
    def __init__(self, fn):
        self.fn = fn


def _mkTraverselImpl():
    class Cont:
        def __init__(self, fn):
            self.fn = fn

    class ConsCell:
        def __init__(self, head, tail):
            self.head = head
            self.tail = tail

    emptyList = None

    def finalCell(head):
        return ConsCell(head, emptyList)

    def consList(x):
        return lambda xs: ConsCell(x, xs)

    def listToArray(lst):
        arr = []
        xs = lst
        while xs is not emptyList:
            arr.append(xs.head)
            xs = xs.tail
        return tuple(arr)

    def kernel(apply, map_, f):
        def buildFrom(x, ys):
            return apply(map_(consList)(f(x)))(ys)

        def go(acc, currentLen, xs):
            if currentLen == 0:
                return acc
            else:
                last = xs[currentLen - 1]
                return Cont(lambda: go(buildFrom(last, acc), currentLen - 1, xs))

        def result(array):
            acc = map_(finalCell)(f(array[-1]))
            result = go(acc, len(array) - 1, array)
            while isinstance(result, Cont):
                result = result.fn()

            return map_(listToArray)(result)

        return result

    return lambda apply: lambda map_: lambda f: kernel(apply, map_, f)


traverse1Impl = _mkTraverselImpl()
