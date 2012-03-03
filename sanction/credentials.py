from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty


class BaseCredentials(object):

    @abstractproperty
    def token_type(self): pass #pragma: no cover
    
    @abstractmethod
    def http_header(self): pass #pragma: no cover

    @abstractmethod
    def query_param(self): pass #pragma: no cover


class BearerCredentials(BaseCredentials):
    token_type = "bearer"

    def __init__(self, data):
        self.__access_token = data["access_token"] 


    @property
    def access_token(self):
        return self.__access_token


    @access_token.setter
    def access_token(self, value):
        self.__access_token = value


    def http_header(self):
        return {
            "Bearer": self.__access_token
        }

    def query_param(self):
        return "access_token=%s" % self.__access_token


def credentials_factory(token_type, data):
    for cls in BaseCredentials.__subclasses__():
        if cls.token_type == token_type.lower():
            return cls(data)

    raise NotImplementedError("Unhandled credentials type: %s" % token_type)
