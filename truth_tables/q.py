"""
`q` for `q`uick class definitions!

class Point(q):
    x, y

This is all you need to get the __init__ and __repr__ one expects.

A simplified version of `https://github.com/salt-die/q`
"""
class AutoDict(dict):
    def __init__(self):
        super().__init__(__fields__={})  # Using a dict as an ordered-set

    def __missing__(self, key):
        if key.startswith('__'):
            raise KeyError(key)

        self['__fields__'][key] = None


class qMeta(type):
    def __prepare__(name, bases):
        return AutoDict()

    def __new__(meta, name, bases, namespace):
        attrs = {}
        for base in bases:
            attrs |= getattr(base, '__fields__', {})
        attrs |= namespace['__fields__']
        namespace['__fields__'] = attrs

        if attrs:
            init_header = f'def __init__(self, {", ".join(attrs)}):\n'
            init_body = '\n'.join(f'    self.{attr}={attr}' for attr in attrs)
            exec(init_header + init_body, namespace)

        repr_header = 'def __repr__(self):\n'
        args = ', '.join(f'{{self.{attr}!r}}' for attr in attrs)
        repr_body = f'    return f"{name}({args})"'
        exec(repr_header + repr_body, namespace)

        return super().__new__(meta, name, bases, namespace)


class q(metaclass=qMeta):
    pass
