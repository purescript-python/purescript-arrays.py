_buitins = {"range": range}

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
