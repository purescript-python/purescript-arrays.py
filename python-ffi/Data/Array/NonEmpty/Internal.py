import functools
def fold1Impl(f): 
    def result(xs):
        acc = xs[0]
        lxs = len(xs)
        for i in range(1, lxs):
            acc = f(acc)(xs[i])
        return acc
  return result

class Cont:
    def __init__(self, fn):
        self.fn = fn

class ConsCell:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

def traverse1Impl(): 

    emptyList = None

    def finalCell(head):
        return ConsCell(head, emptyList)
    
    def consList(x):
        return lambda xs: ConsCell(x, xs)
    
    def listToArray(lst):
        arr = []
        xs = lst
        while xs != emptyList:
            arr.append(xs.head)
            xs = xs.tail
        return arr

    

    def _result(apply):
        def l0(map_):
            def l1(f):
                def buildFrom(x, ys):
                    return apply(map(consList)(f(x)))(ys)
                def go(acc, currentLen, xs):
                    if currentLen == 0:
                        return acc
                    else:
                        last = xs[currentLen - 1]
                        return Cont(lambda: go(buildFrom(last, acc), currentLen - 1, xs))
                def _result2(array):
                    acc = map_(finalCell)(f(array[array.length - 1]))
                    result = go(acc, array.length - 1, array)
                    while isinstance(result, Cont):
                        result = result.fn()

                    return map_(listToArray)(result)
                return _result2
            return l1
        return l0     
    return _result(None)

