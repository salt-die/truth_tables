"""
`q` for `q`uick class definitions!

class Point(q):
    x, y

This is all you need to get the __init__ and __repr__ one expects.

A simplified version of `https://github.com/salt-die/q`
"""
class AutoDict(dict):
    def __init__(self):
        self.fields = {}  # Using a dict as an ordered-set

    def __missing__(self, key):
        if key.startswith('__'):
            raise KeyError(key)

        self.fields[key] = None


class qMeta(type):
    def __prepare__(name, bases):
        return AutoDict()

    def __new__(meta, name, bases, namespace):
        namespace['__fields__'] = fields = {}
        for base in reversed(bases):
            fields |= getattr(base, '__fields__', {})
        fields |= namespace.fields

        if fields:
            init_header = f'def __init__(self, {", ".join(fields)}):\n'
            init_body = '\n'.join(f'    self.{field}={field}' for field in fields)
            exec(init_header + init_body, globals(), namespace)

        args = ', '.join(f'{{self.{field}!r}}' for field in fields)
        repr_ = f'def __repr__(self):\n    return f"{name}({args})"'
        exec(repr_, globals(), namespace)

        return super().__new__(meta, name, bases, namespace)


class q(metaclass=qMeta):
    pass
