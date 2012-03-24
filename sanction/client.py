""" The :py:class:`~sanction.client.Client` class is essentially a facade
exposing the most commonly used features of the ``sanction`` library.

"""

from flow import AuthorizationRequestFlow
from adapters import BaseAdapter


class Client(object):
    """ A convenience class to assist dealing with an :term:`OAuth2` flow.

    :param adapter: The adapter to use with this Client instance. Must be
                    a child class (not an instance of) 
                    :class:`sanction.adapters.BaseAdapter`.
    :param flow: A valid subclass of :class:`sanction.flow.ResourceFlow`
                 (which is the base class for all :term:`OAuth2` flows). Will 
                 default to :class:`sanction.flow.AuthorizationRequestFlow`
                 which is used for web server-based flows.
    """

    def __init__(self, adapter, config, flow=None):
        assert(issubclass(adapter, BaseAdapter))
        self.__adapter = adapter(config, flow)


    @property
    def adapter(self):
        """ The adapter instance bound to the :class:`Client` instance.

        Possibly the frequently used member of this class is 
        :py:attr:`~sanction.adapters.BaseAdapter.credentials` for the current
        adapter. This will be available once a user has been authenticated
        by the :term:`OAuth2` provider and should be set in code when your application
        requests resources for a user who's already logged in (in order to 
        avoid :term:`stateless requests`).

        This accessor can be used to query the adapter directly. See
        :mod:`sanction.adapters` for further details as attributes may vary
        by adapter implementation.

        """
        return self.__adapter


    @property
    def flow(self):
        """ The :term:`OAuth2` flow being used by the :class:`Client` instance.

        This access can be used to operate on the current :term:`OAuth2` flow. For
        further details, see :mod:`sanction.flow`. To really understand what's
        going on in a given flow, it's important to have a solid understanding
        of the entire `OAuth2 protocol`_. However, this *should* not be
        typically used by the average user as flows are handled automatically. 

        .. _`oauth2 protocol`: http://oauth.net/2/
        """
        return self.__adapter.flow


    def request(self, path, method=None, body=None):
        """ Requests a resource from the :term:`OAuth2` provider

        Individual provider API is not exposed in adapter implementations, so
        it's up to the client to know everything they need to know about their
        chosen provider's API in order to retrieve data.

        :param path: The path to the resource. **Note:** This should *not*
                     include the provider's address. For example, to access
                     facebook's user data, you would use "/me".
        :param method: The HTTP verb to be used in the request ("GET", "POST",
                       "DELETE", etc.). This will default to "GET" if not
                       specified.
        :param body: The body of the request. This should be a ``dict``
                     containing data expected by the API.
        """
        return self.adapter.request(path, method, body)
