from abc import ABCMeta
from abc import abstractproperty

from sanction.config import adapter_config


class ResourceEndpointMixIn(object):

    def __init__(self):
        self.__resource_endpoint = None
        self.__token_endpoint = None

    @property
    def resource_endpoint(self):
        return self.__resource_endpoint

    @resource_endpoint.setter
    def resource_endpoint(self, value):
        self.__resource_endpoint = value


    @property
    def token_endpoint(self):
        return self.__token_endpoint

    @token_endpoint.setter
    def token_endpoint(self, value):
        self.__token_endpoint = value


class AuthorizationEndpointMixIn(object):

    def __init__(self):
        self.__authorization_endpoint = None

    @property
    def authorization_endpoint(self):
        return self.__authorization_endpoint

    @authorization_endpoint.setter
    def authorization_endpoint(self, value):
        self.__authorization_endpoint = value


class BaseAdapter(object):

    def __init__(self, config, flow=None):
        if flow is None:
            from sanction.flow import AuthorizationRequest
            flow = AuthorizationRequest

        from sanction.flow import BaseFlow
        assert(issubclass(flow, BaseFlow))

        self.__name = self.__class__.__name__.lower()
        self.__config = adapter_config(self.__name, config)
        self.__flow = flow(self.__config, self)


    @property
    def name(self):
        return self.__name


    @property
    def flow(self):
        return self.__flow

    @property
    def config(self):
        return self.__config


    def request(self, method, uri, body=None, headers=None):
        pass


