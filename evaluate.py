
from basic import Sym

class NotAFunction(Exception):
    pass

class Undefined(Exception):
    pass

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
        evald = [self._eval(each) for each in expr]
        fun = evald[0]
        if not callable(fun):
            raise NotAFunction(expr[0])
        fun(self.namespace, *self.fixed_args, *evald[1:])

        
