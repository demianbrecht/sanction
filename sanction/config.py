
def adapter_config(name, dict_):
    """ Parses the given dict for values that should be processed for the given
    name.

    Some configuration values should be applied to all adapters, others to 
    specific ones. For example::
        
        http_debug = true
        facebook.client_secret = facebook_secret

    In the above code, every instance of a 
    :py:class:`~sanction.adapters.BaseAdapter` child class should receieve 
    ``http_debug`` whereas only 
    :py:class:`~sanction.adapters.facebook.Facebook` should receive
    ``facebook.client_secret``.

    :param name: The name of the adapter. This is the lower case version of 
                 the adapter class' name. For example,
                 :py:class:`~sanction.adapters.facebook.Facebook` would be 
                 ``"facebook"``

    :param dict_: The set of key/value pairs to build from.
    """

    o = {}
    for k in dict_:
        if "." not in k:
            # global settings
            o[k] = dict_[k]
        elif "%s." % name == k[:len(name)+1]:
            # adapter settings
            o[k[k.find(".") + 1:]] = dict_[k]

    return o
