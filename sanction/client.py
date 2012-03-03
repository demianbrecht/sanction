from flow import AuthorizationRequestFlow
from adapters import BaseAdapter


class Client(object):

    def __init__(self, adapter, config, flow=AuthorizationRequestFlow):
        assert(issubclass(adapter, BaseAdapter))
        self.__adapter = adapter(config, flow)


    @property
    def adapter(self):
        return self.__adapter


    @property
    def flow(self):
        return self.__adapter.flow


    def request(self, path, method="GET", body=None):
        self.adapter.request(path, method, body)
