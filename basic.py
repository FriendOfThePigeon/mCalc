
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Sym:
    def __init__(self, value):
        self.value = value

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


class ChildNamespace:
    def __init__(self, parent):
        self._parent = parent
        self._dict = dict()

    def get(self, key):
        return self._dict[key] if key in self._dict else parent.get(key)

    def _set_where_present(self, key, value):
        if key in self._dict:
            self._dict[key] = value
            return self
        return self._parent._set_where_present(key, value)

    def set(self, key, value):
        ns = self._set_where_present(key, value)
        if not ns:
            self._dict[key] = value
            
class BasicNamespace:
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

class ImmutableNamespace:
    def __init__(self, initial_dict):
        self._dict = initial_dict

    def get(self, key):
        return self._dict[key]

    def _set_where_present(self, key, value):
        return None

    def set(self, key, value):
        raise RefusedToMutate()
        
