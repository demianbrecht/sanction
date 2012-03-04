from abc import ABCMeta
from abc import abstractproperty
from json import loads
from logging import getLogger
from urllib import urlencode

from sanction.credentials import credentials_factory
from sanction.exceptions import exception_factory
from sanction.exceptions import InvalidStateError
from sanction.util import safe_get

log = getLogger(__name__)

class ResourceEndpointMixIn(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def token_endpoint(self): pass #pragma: no cover

    @abstractproperty
    def resource_endpoint(self): pass #pragma: no cover


class AuthorizationEndpointMixIn(ResourceEndpointMixIn):
    __metaclass__ = ABCMeta

    @abstractproperty
    def authorization_endpoint(self): pass #pragma: no cover


class ResourceFlow(object):

    def __init__(self, grant_type, adapter):
        self.__grant_type = grant_type
        self.__adapter = adapter


    @property
    def grant_type(self):
        return self.__grant_type

    @property
    def adapter(self):
        return self.__adapter


    def add_optional_attr(self, name, attr, obj):
        if attr is not None:
            obj[name] = attr



class AuthorizationRequestFlow(ResourceFlow):

    def __init__(self, adapter):
        assert(isinstance(adapter, AuthorizationEndpointMixIn))
        assert(isinstance(adapter, ResourceEndpointMixIn))

        ResourceFlow.__init__(self, "authorization_code", adapter)

        self.__client_id = safe_get("client_id", adapter.config, 
            required=True)
        self.__client_secret = safe_get("client_secret", adapter.config,
            required=True)
        self.__redirect_uri = safe_get("redirect_uri", adapter.config)
        self.__scope = safe_get("scope", adapter.config)

    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def redirect_uri(self):
        return self.__redirect_uri

    @property
    def scope(self):
        return self.__scope

    def authorization_uri(self, state=None):

        data = {
            "response_type": "code",
            "client_id": self.__client_id 
        }
        self.add_optional_attr("redirect_uri", self.redirect_uri, data)
        self.add_optional_attr("scope", " ".join(self.scope.split(",")), data)
        self.add_optional_attr("state", state, data)

        return "%s?%s" % (self.adapter.authorization_endpoint, urlencode(data))


    def parse_access_token(self, data):
        return loads(data)


    def authorization_received(self, data, expected_state=None):
        if "code" in data:
            if expected_state is not None:
                if expected_state != data["state"]:
                    raise InvalidStateError("Expected %s, got %s." % (
                        expected_state, data["state"]))

            o = self.parse_access_token(self.adapter.service.request(
                self.adapter.token_endpoint, body=urlencode({
                    "code": data["code"],
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code"
                }), method="POST", headers={"Content-type":
                "application/x-www-form-urlencoded"}))

            self.adapter.credentials = credentials_factory(o["token_type"], o)
            return self.adapter.credentials 

        elif "error" in data:
            raise exception_factory(data["error"], data)

        raise Exception("Unhandled authorization data received")

