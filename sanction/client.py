from flow import AuthorizationRequest
from adapters import BaseAdapter


class Client(object):

    def __init__(self, adapter, config, flow=AuthorizationRequest):
        assert(issubclass(adapter, BaseAdapter))
        self.__adapter = adapter(config, flow)


    @property
    def adapter(self):
        return self.__adapter

