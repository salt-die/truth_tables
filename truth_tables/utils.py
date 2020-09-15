from collections import defaultdict, OrderedDict

def prefix(body, prefix='   '):
    for line in body:
        yield prefix + line


class LRU(OrderedDict):
    def __init__(self, maxsize=128, /, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            self.popitem(last=False)


class CachedType(type):
    """Memoize instances of CachedType"""
    _instances = defaultdict(LRU)

    def __call__(cls, *args, **kwargs):
        lookup = *args, *sorted(kwargs.items())
        cls_dict = CachedType._instances[cls]

        if lookup not in cls_dict:
            cls_dict[lookup] = super(CachedType, cls).__call__(*args, **kwargs)

        return cls_dict[lookup]
