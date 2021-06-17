import operator
import math

def from_binary_operator(op):
    def result(namespace, stack):
        one, two = stack.pop(), stack.pop()
        stack.push(op(two, one))

    return result

def from_unary_operator(op):
    def result(namespace, stack):
        stack.push(op(stack.pop()))

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
    '+': from_binary_operator(operator.add),
    '*': from_binary_operator(operator.mul),
    'x': from_binary_operator(operator.mul),
    '-': from_binary_operator(operator.sub),
    '^': from_binary_operator(operator.pow),
    '/': from_binary_operator(operator.truediv),
    '_': from_unary_operator(math.floor),
    '.': dup,
    '\\': swap,
    '@': rot3,
    'd': drop,
    # 'sin', 'cos', 'pi', etc.
}

