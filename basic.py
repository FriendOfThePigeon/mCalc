from functools import reduce


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Sym:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '$' + self.value

class Punc:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '#' + self.value

class WS:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '_'

class Namespace:
    def get(self, key):
        raise NotImplementedError()

    def set(self, key, value):
        raise NotImplementedError()

    def has(self, key):
        raise NotImplementedError()

    def _set_where_present(self, key, value):
        raise NotImplementedError()

    def spawn(self):
        return ChildNamespace(self)


class ChildNamespace(Namespace):
    def __init__(self, parent):
        self._parent = parent
        self._dict = dict()

    def get(self, key):
        return self._dict[key] if key in self._dict else self._parent.get(key)

    def _set_where_present(self, key, value):
        if key in self._dict:
            self._dict[key] = value
            return self
        return self._parent._set_where_present(key, value)

    def set(self, key, value):
        ns = self._set_where_present(key, value)
        if not ns:
            self._dict[key] = value
            
class RootNamespace(Namespace):
    def __init__(self, initial_dict):
        self._dict = initial_dict

    def get(self, key):
        return self._dict[key]

    def _set_where_present(self, key, value):
        if key in self._dict:
            self._dict[key] = value
            return self
        return None

    def set(self, key, value):
        self._dict[key] = value
        
class RefusedToMutate(Exception):
    pass

class ImmutableNamespace(Namespace):
    def __init__(self, initial_dict):
        self._dict = initial_dict

    def get(self, key):
        return self._dict[key]

    def _set_where_present(self, key, value):
        return None

    def set(self, key, value):
        raise RefusedToMutate()
        
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
