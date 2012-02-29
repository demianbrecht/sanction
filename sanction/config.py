
def adapter_config(name, dict_):
    o = {}
    for k in dict_:
        if "." not in k:
            # global settings
            o[k] = dict_[k]
        elif "%s." % name == k[:len(name)+1]:
            # adapter settings
            o[k[k.find(".") + 1:]] = dict_[k]

    return o
