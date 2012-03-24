from sanction.config import adapter_config
from sanction.credentials import BaseCredentials
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import ResourceFlow
from sanction.flow import ResourceEndpointMixIn
from sanction.services import BaseService
from sanction.services import HTTPSService
from sanction.util import safe_get

class BaseAdapter(ResourceEndpointMixIn):
    """ The base class for all adapter implementations

    :param config: A ``dict`` containing configuration information derived
                   from a call to :py:meth:`~sanction.config.adapter_config`

    :param flow: Which :py:mod:`~sanction.flow` the adapter should use.
                 Defaults to
                 :py:class:`~sanction.flow.AuthorizationRequestFlow`

    :param service: Which :py:mod:`~sanction.service` the adapter should use.
                    Defaults to
                    :py:class:`~sanction.services.HTTPSService`
    """

    def __init__(self, config, flow=None, service=None):

        if flow is None:
            flow = AuthorizationRequestFlow
        else:
            assert(issubclass(flow, ResourceFlow))

        if service is None:
            service = HTTPSService
        else:
            assert(issubclass(service, BaseService))

        self.__name = self.__class__.__name__.lower()
        self.__credentials = None
        self.__config = adapter_config(self.__name, config)
        self.__service = service()
        self.__flow = flow(self)


    def request(self, path, method=None, body=None): 
        """ Sends a resource request to the :term:`OAuth2` provider.

        :param path: Path to the resource (i.e. ``"/me"`` for facebook user
                     data).
        :param method: HTTP verb to use in the request. Defaults to "GET".
        :param body: Body of the request. This should be a ``dict`` of
                     key/value pairs as expected by the provider API.
        """
        assert(isinstance(self.__credentials, BaseCredentials))
        uri = "%s%s" % (self.resource_endpoint, path)
        return self.service.request(uri, method, body,
            self.__credentials.http_header())


    @property
    def name(self):
        """ Name of the adapter.

        By default, this will be the lower-case version of the class name. For
        example, :py:class:`~sanction.adapters.facebook.Facebook` would be
        ``"facebook"``.
        """
        return self.__name


    @property
    def flow(self):
        """ :py:mod:`~sanction.flow` that the adapter has been told to use
        during :py:class:`~sanction.client.Client` instantiation.
        """
        return self.__flow


    @property
    def config(self):
        """ Config ``dict`` passed in during instantiation """
        return self.__config


    @property
    def service(self):
        """ The :py:mod:`~sanction.services` class that the adapter has been
        configured to use.
        """
        return self.__service


    @property
    def credentials(self):
        """ The :py:class:`~sanction.credentials.BaseCredentials` child class
        intance (i.e. :py:class:`~sanction.credentials.BearerCredentials`) to
        use for all requests.
        """
        return self.__credentials


    @credentials.setter
    def credentials(self, value):
        assert(isinstance(value, BaseCredentials))
        self.__credentials = value

