from urllib import urlencode

from sanction.adapters import BaseAdapter
from sanction.adapters import AuthorizationEndpointMixIn
from sanction.adapters import ResourceEndpointMixIn
from sanction.exceptions import InvalidStateError
from sanction.util import safe_get


class BaseFlow(object):

    def __init__(self, grant_type, adapter):
        assert(isinstance(adapter, BaseAdapter))

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


class AuthorizationRequest(BaseFlow):

    def __init__(self, config, adapter):
        BaseFlow.__init__(self, "authorization_code", adapter)
        self.__client_id = safe_get("client_id", config, required=True)
        self.__client_secret = safe_get("client_secret", config,
            required=True)
        self.__redirect_uri = safe_get("redirect_uri", config)
        self.__scope = safe_get("scope", config)


    def authorization_uri(self, state=None):
        assert(isinstance(self.adapter, AuthorizationEndpointMixIn)) 

        data = {
            "response_type": "code",
            "client_id": self.__client_id 
        }
        self.add_optional_attr("redirect_uri", self.__redirect_uri, data)
        self.add_optional_attr("scope", self.__scope, data)
        self.add_optional_attr("state", state, data)

        return "%s?%s" % (self.adapter.authorization_endpoint, urlencode(data))


    def authorization_received(self, data, expected_state=None):
        assert(isinstance(self.adapter, ResourceEndpointMixIn))

        if "code" in data:
            if expected_state is not None:
                if expected_state != data["state"]:
                    raise InvalidStateError


        elif "error" in data:
            pass
        else:
            raise Exception("Unhandled authorization data received")

