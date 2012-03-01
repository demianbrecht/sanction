from urllib import urlencode

from sanction.exceptions import exception_factory
from sanction.exceptions import InvalidStateError
from sanction.util import safe_get


class AuthorizationEndpointMixIn(object):

    def __init__(self):
        self.__authorization_endpoint = None

    @property
    def authorization_endpoint(self):
        return self.__authorization_endpoint

    @authorization_endpoint.setter
    def authorization_endpoint(self, value):
        self.__authorization_endpoint = value


class BaseEndpointMixIn(object):

    def __init__(self):
        self.__token_endpoint = None
        self.__resource_endpoint = None

    @property
    def token_endpoint(self):
        return self.__token_endpoint

    @token_endpoint.setter
    def token_endpoint(self, value):
        self.__token_endpoint = value

    @property
    def resource_endpoint(self):
        return self.__resource_endpoint

    @resource_endpoint.setter
    def resource_endpoint(self, value):
        self.__resource_endpoint = value


class BaseFlow(BaseEndpointMixIn):

    def __init__(self, grant_type, config, service):
        BaseEndpointMixIn.__init__(self)
        self.__grant_type = grant_type
        self.__config = config
        self.__service = service


    @property
    def config(self):
        return self.__config

    @property
    def grant_type(self):
        return self.__grant_type

    @property
    def service(self):
        return self.__service


    def add_optional_attr(self, name, attr, obj):
        if attr is not None:
            obj[name] = attr



class AuthorizationRequestFlow(BaseFlow, AuthorizationEndpointMixIn):

    def __init__(self, config, service):
        BaseFlow.__init__(self, "authorization_code", config, service)
        AuthorizationEndpointMixIn.__init__(self)

        self.__client_id = safe_get("client_id", config, required=True)
        self.__client_secret = safe_get("client_secret", config,
            required=True)
        self.__redirect_uri = safe_get("redirect_uri", config)
        self.__scope = safe_get("scope", config)


    def authorization_uri(self, state=None):

        data = {
            "response_type": "code",
            "client_id": self.__client_id 
        }
        self.add_optional_attr("redirect_uri", self.__redirect_uri, data)
        self.add_optional_attr("scope", self.__scope, data)
        self.add_optional_attr("state", state, data)

        return "%s?%s" % (self.authorization_endpoint, urlencode(data))


    def authorization_received(self, data, expected_state=None):

        if "code" in data:
            if expected_state is not None:
                if expected_state != data["state"]:
                    raise InvalidStateError()

            #TODO: Return credentials
            return

        elif "error" in data:
            raise exception_factory(data["error"], data)


        raise Exception("Unhandled authorization data received")

