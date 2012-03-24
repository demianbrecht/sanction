from flow import AuthorizationRequestFlow
from adapters import BaseAdapter


class Client(object):
    """ A convenience class to assist dealing with an OAuth2 flow.

    :param adapter: The adapter to use with this Client instance. Must be
                    a child class (not an instance of) 
                    :class:`sanction.adapters.BaseAdapter`.
    :param flow: A valid subclass of :class:`sanction.flow.ResourceFlow`
                 (which is the base class for all OAuth2 flows). Will 
                 default to :class:`sanction.flow.AuthorizationRequestFlow`
                 which is used for web server-based flows.
    """

    def __init__(self, adapter, config, flow=None):
        assert(issubclass(adapter, BaseAdapter))
        self.__adapter = adapter(config, flow)


    @property
    def adapter(self):
        """ The adapter instance bound to the :class:`Client` instance.

        Possibly the most useful thing that you can get from this is the
        :py:attr:`~sanction.adapters.BaseAdapter.credentials` for the current
        adapter. This will be available once a user has been authenticated
        by the OAuth2 provider and should be set when your application requests
        resources for a user who's already logged in (in order to avoid 
        :term:`stateless requests`).

        This accessor can be used to query the adapter directly. See
        :mod:`sanction.adapters` for further details as attributes may vary
        by adapter implementation.

        """
        return self.__adapter


    @property
    def flow(self):
        """ The OAuth2 flow being used by the :class:`Client` instance.

        This access can be used to operate on the current OAuth2 flow. For
        further details, see :mod:`sanction.flow`. To really understand what's
        going on in a given flow, it's important to have a solid understanding
        of the entire `OAuth2 protocol`_. However, this *should* not be
        typically used by the average user as flows are handled automatically. 

        .. _`oauth2 protocol`: http://oauth.net/2/
        """
        return self.__adapter.flow


    def request(self, path, method=None, body=None):
        return self.adapter.request(path, method, body)
