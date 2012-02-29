from sanction.config import adapter_config
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import BaseFlow


class BaseAdapter(object):

    def __init__(self, config, flow=AuthorizationRequestFlow):
        assert(issubclass(flow, BaseFlow))

        self.__name = self.__class__.__name__.lower()
        self.__config = adapter_config(self.__name, config)
        self.__flow = flow(self.__config)


    @property
    def name(self):
        return self.__name


    @property
    def flow(self):
        return self.__flow


    @property
    def config(self):
        return self.__config


