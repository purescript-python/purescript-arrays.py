import functools

empty = lambda: []


def peekImpl(just):
    def _peekImpl(nothing, i, xs):
        if i >= 0 and (i < len(xs)):
            return just(xs[i])
        else:
            return nothing

    return lambda nothing: lambda i: lambda xs: lambda: _peekImpl(nothing, i, xs)


def _pokeImpl(i, a, xs):
    if i >= 0 and i < len(xs):
        xs[i] = a
        return True
    else:
        return False


poke = lambda i: lambda a: lambda xs: lambda: _pokeImpl(i, a, xs)


popImpl = (
    lambda just: lambda nothing: lambda xs: lambda: just(xs.pop())
    if len(xs) > 0
    else nothing
)


def _pushAllImpl(as_, xs):
    xs.extend(as_)
    return len(xs)


pushAll = lambda as_: lambda xs: lambda: _pushAllImpl(as_, xs)


# exports.pushAll = function (as) {
#   return function (xs) {
#     return function () {
#       return xs.push.apply(xs, as);
#     };
#   };
# };


shiftImpl = (
    lambda just: lambda nothing: lambda xs: lambda: just(xs.pop(0))
    if len(xs) > 0
    else nothing
)


def _unshiftAllImpl(as_, xs):
    xs[len(as_) :] = xs[:]
    xs[: len(as_)] = as_
    return len(xs)


unshiftAll = lambda as_: lambda xs: lambda: _unshiftAllImpl(as_, xs)


# exports.unshiftAll = function (as) {
#   return function (xs) {
#     return function () {
#       return xs.unshift.apply(xs, as);
#     };
#   };
# };


def _spliceImpl(i, howMany, bs, xs):
    s = i if i >= 0 else len(xs) + i
    removed = xs[s : s + howMany]
    xs[s + len(bs) :] = xs[s + len(removed) :]
    xs[s : s + len(bs)] = bs[:]
    return removed


splice = lambda i: lambda howMany: lambda bs: lambda xs: lambda: _spliceImpl(
    i, howMany, bs, xs
)

# exports.splice = function (i) {
#   return function (howMany) {
#     return function (bs) {
#       return function (xs) {
#         return function () {
#           return xs.splice.apply(xs, [i, howMany].concat(bs));
#         };
#       };
#     };
#   };
# };


unsafeFreeze = lambda xs: lambda: xs

unsafeThaw = lambda xs: lambda: xs

copyImpl = lambda xs: lambda: xs[:]

freeze = copyImpl
thaw = copyImpl


sortByImpl = lambda comp: lambda xs: lambda: sorted(
    xs, key=functools.cmp_to_key(lambda a, b: comp(a, b))
)


def toAssocArray(xs):
    return [{"value": x, "index": i} for i, x in enumerate(xs)]
