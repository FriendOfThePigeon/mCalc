
from basic import Sym, WS

class NotAFunction(Exception):
    pass

class Undefined(Exception):
    pass

class EvalError(Exception):
    pass

class NothingToPop(EvalError):
    pass

class Stack:
    def __init__(self):
        self._items = list()

    def push(self, item):
        self._items.insert(0, item)

    def pop(self):
        try:
            return self._items.pop(0)
        except IndexError:
            raise NothingToPop()

    def __str__(self):
        return str(self.as_list())

    def as_list(self):
        return list(reversed(self._items))


class Evaluator:
    def __init__(self, namespace, fixed_args):
        self.namespace = namespace
        self.fixed_args = fixed_args

    def _eval(self, item):
        if isinstance(item, list):
            return self.evaluate(item)
        elif isinstance(item, Sym):
            try:
                return self.namespace.get(item.value)
            except KeyError:
                raise Undefined(item.value)
        else:
            return item

    def evaluate(self, expr):
        stack = Stack()
        for item in expr:
            if isinstance(item, WS):
                continue
            evald = self._eval(item)
            if callable(evald):
                evald(self.namespace, stack, *self.fixed_args)
            else:
                stack.push(evald)
        return stack
