import operator

def from_operator(op):
    def result(namespace, stack):
        one, two = stack.pop(), stack.pop()
        stack.push(op(two, one))

    return result

def dup(namespace, stack):
    one = stack.pop()
    stack.push(one)
    stack.push(one)

def swap(namespace, stack):
    one, two = stack.pop(), stack.pop()
    stack.push(one)
    stack.push(two)

def drop(namespace, stack):
    stack.pop()

def rot3(namespace, stack):
    one, two, three = stack.pop(), stack.pop(), stack.pop()
    stack.push(two)
    stack.push(one)
    stack.push(three)

stdlib = {
    '+': from_operator(operator.add),
    '*': from_operator(operator.mul),
    '-': from_operator(operator.sub),
    '^': from_operator(operator.pow),
    '/': from_operator(operator.truediv),
    # '//': from_operator(operator.floordiv),
    '.': dup,
    '\\': swap,
    '@': rot3,
    'd': drop,
    # 'sin', 'cos', 'pi', etc.
}

