from sanction.util import safe_get

map = {}

class BaseError(BaseException):
    def __init__(self, response):
        self.__description = safe_get("description", response)
        self.__error_uri = safe_get("error_uri", response)
        self.__state = safe_get("state", response)


    @property
    def description(self):
        return self.__description


    @property
    def error_uri(self):
        return self.__error_uri


    @property
    def state(self):
        return self.__state


    def __str__(self):
        return "<%s: %s>" % (self.__class__.__name__,
            self.__description)


class AccessDeniedError(BaseError):
    pass
map["access_denied"] = AccessDeniedError

class InvalidClientError(BaseError):
    pass
map["invalid_client"] = InvalidClientError

class InvalidGrantError(BaseError):
    pass
map["invalid_grant"] = InvalidGrantError

class InvalidScopeError(BaseError):
    pass
map["invalid_scope"] = InvalidScopeError

class InvalidRequestError(BaseError):
    pass
map["invalid_request"] = InvalidRequestError

class InvalidScopeError(BaseError):
    pass
map["invalid_scope"] = InvalidScopeError

class InvalidStateError(BaseError):
    pass


class ServerError(BaseError):
    pass
map["server_error"] = ServerError

class TemporarilyUnavailableError(BaseError):
    pass
map["temporarily_unavailable"] = TemporarilyUnavailableError


class UnauthorizedClientError(BaseError):
    pass
map["unauthorized_client"] = UnauthorizedClientError

class UnsupportedGrantType(BaseError):
    pass
map["unsupported_grant_type"] = UnsupportedGrantType


class UnsupportedResponseTypeError(BaseError):
    pass
map["unsupported_response_type"] = UnsupportedResponseTypeError

