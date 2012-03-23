from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

from sanction.util import subclasses

class BaseCredentials(object):

    @abstractproperty
    def context(self): pass #pragma: no cover

    @abstractproperty
    def token_type(self): pass #pragma: no cover
    
    @abstractmethod
    def http_header(self): pass #pragma: no cover

    @abstractmethod
    def query_param(self): pass #pragma: no cover


class BearerCredentials(BaseCredentials):
    token_type = "Bearer"
    context = None

    def __init__(self, data):
        BaseCredentials.__init__(self)
        data = self.normalize_token(data)
        self.__access_token = data["access_token"] 
        self.__expires_in = int(data["expires_in"])
        self.__refresh_token = data["refresh_token"]

    @property
    def expires_in(self):
        return self.__expires_in

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, value):
        self.__access_token = value

    @property
    def refresh_token(self):
        return self.__refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        self.__refresh_token = value


    def normalize_token(self, data):
        return {
            "access_token": data["access_token"],
            "expires_in": data["expires_in"],
            "refresh_token": "refresh_token" in data and data["refresh_token"]\
                or None
        }

    def http_header(self):
        return {
            "Authorization": "%s %s" % ("Bearer", self.__access_token)
        }

    def query_param(self):
        return "access_token=%s" % self.__access_token


def credentials_factory(token_type, context, data):
    a = filter(lambda c: c.token_type == token_type, 
        subclasses(BaseCredentials))
    c = filter(lambda c: c.context == context, a)
    # definitely shoudln't be more than one with the given context
    assert(len(c) < 2) 

    if len(c) > 0:
        return c[0](data)
    elif len(a) > 0:
        return a[0](data)
    else:
        raise NotImplementedError("Unhandled credentials type: %s" % token_type)

