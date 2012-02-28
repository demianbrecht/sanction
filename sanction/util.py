
def safe_get(key, dict_, default=None, required=False):
    if key in dict_:
        return dict_[key]
    else:
        if not required:
            return default

    raise KeyError("%s is undefined" % key)

