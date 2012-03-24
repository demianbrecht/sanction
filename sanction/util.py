""" A collection of utility functions used by the  :py:mod:`~sanction` library
"""

def subclasses(cls, a = None):
    """ Recursively retrieves all subclasses of the given class

    :param cls: The class to do the lookup on
    :param a: Found class. Used when called recursively.
    """
    if a is None: a = set()
    for c in cls.__subclasses__():
        if c not in a:
            a.add(c)
            yield c
            for c in subclasses(c, a):
                yield c


def safe_get(key, dict_, default=None, required=False):
    """ Retrieves a value from a ``dict``.

    :param dict_: The ``dict`` to look for the key in
    :param default: If ``key`` is not found, the default value to return
    :param required: Whether or not the value is required
    
    :rval: If ``required`` is ``True``, if ``default`` is set and
              ``key`` is not found, ``default`` will be returned, 
              otherwise ``KeyError`` will be raised. ``None`` is 
              returned if ``required`` is ``False``.
    """
    if key in dict_:
        return dict_[key]
    else:
        if not required:
            return default

    raise KeyError("%s is undefined" % key)

