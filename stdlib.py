import operator
import math
from basic import Punc
from functools import reduce

def from_binary_operator(op, can_fold=True):
    def result(namespace, stack):
        one = stack.pop()
        if isinstance(one, list) and can_fold:
            # fold over array
            stack.push(reduce(op, one[1:], one[0])) 
        else:
            two = stack.pop()
            stack.push(op(two, one))

    return result

def from_unary_operator(op):
    def result(namespace, stack):
        item = stack.pop()
        # map over array; just apply to a scalar
        stack.push(list(map(op, item)) if isinstance(item, list) else op(item))

    return result

def from_const(const):
    def result(namespace, stack):
        stack.push(const)

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

def modf(namespace, stack):
    (f, i) = math.modf(stack.pop())
    stack.push(i)
    stack.push(f)

def make_array(namespace, stack):
    result = []
    while True:
        item = stack.pop()
        if isinstance(item, Punc) and item.value == '[':
            break
        result.insert(0, item)
    stack.push(result)

def expand_array(namespace, stack):
    for each in stack.pop():
        stack.push(each)

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
    'sin': from_unary_operator(math.sin),
    'cos': from_unary_operator(math.cos),
    'tan': from_unary_operator(math.tan),
    'asin': from_unary_operator(math.asin),
    'acos': from_unary_operator(math.acos),
    'atan': from_unary_operator(math.atan),
    'deg': from_unary_operator(math.degrees),
    'rad': from_unary_operator(math.radians),
    'pi': from_const(math.pi),
    'e': from_const(math.e),
    'ln': from_unary_operator(math.log),
    'log': from_binary_operator(math.log, can_fold=False),
    ':': modf,
    ']': make_array,
    '!': expand_array,
}

