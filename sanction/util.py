def subclasses(cls, a = None):
        if a is None: a = set()
        for c in cls.__subclasses__():
            if c not in a:
                a.add(c)
                yield c
                for c in subclasses(c, a):
                    yield c

def safe_get(key, dict_, default=None, required=False):
    if key in dict_:
        return dict_[key]
    else:
        if not required:
            return default

    raise KeyError("%s is undefined" % key)

