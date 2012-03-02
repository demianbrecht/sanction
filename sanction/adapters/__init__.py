from sanction.config import adapter_config
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import ResourceFlow
from sanction.services import HTTPSService
from sanction.util import safe_get


class BaseAdapter(object):

    def __init__(self, config, flow=AuthorizationRequestFlow,
        service=HTTPSService):

        self.__name = self.__class__.__name__.lower()
        self.__config = adapter_config(self.__name, config)
        self.__service = service()
        self.__flow = flow(self)


    @property
    def name(self):
        return self.__name


    @property
    def flow(self):
        return self.__flow


    @property
    def config(self):
        return self.__config


