from sanction.config import adapter_config
from sanction.credentials import BaseCredentials
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import ResourceFlow
from sanction.flow import ResourceEndpointMixIn
from sanction.services import HTTPSService
from sanction.util import safe_get


class BaseAdapter(ResourceEndpointMixIn):

    def __init__(self, config, flow=AuthorizationRequestFlow,
        service=HTTPSService):

        self.__name = self.__class__.__name__.lower()
        self.__credentials = None
        self.__config = adapter_config(self.__name, config)
        self.__service = service()
        self.__flow = flow(self)


    def request(self, path, method="GET", body=None):
        assert(isinstance(self.__credentials, BaseCredentials))
        uri = "%s%s" % (self.resource_endpoint, path)
        return self.service.request(uri, method, body,
            self.__credentials.http_header())


    @property
    def name(self):
        return self.__name


    @property
    def flow(self):
        return self.__flow


    @property
    def config(self):
        return self.__config


    @property
    def service(self):
        return self.__service


    @property
    def credentials(self):
        return self.__credentials


    @credentials.setter
    def credentials(self, value):
        assert(isinstance(value, BaseCredentials))
        self.__credentials = value

