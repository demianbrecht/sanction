from flow import AuthorizationRequestFlow
from adapters import BaseAdapter


class Client(object):

    def __init__(self, adapter, config, flow=AuthorizationRequestFlow,
            key_file=None, cert_file=None):
        assert(issubclass(adapter, BaseAdapter))
        self.__adapter = adapter(config, flow)
        self.__adapter.key_file = key_file
        self.__adapter.cert_file = cert_file


    @property
    def adapter(self):
        return self.__adapter


    @property
    def flow(self):
        return self.__adapter.flow


