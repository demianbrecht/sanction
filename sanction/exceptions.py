from sanction.util import safe_get

exception_map = {}

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

class InvalidClientError(BaseError):
    pass

class InvalidGrantError(BaseError):
    pass

class InvalidScopeError(BaseError):
    pass

class InvalidRequestError(BaseError):
    pass

class InvalidScopeError(BaseError):
    pass

class InvalidStateError(BaseError):
    pass


class ServerError(BaseError):
    pass

class TemporarilyUnavailableError(BaseError):
    pass


class UnauthorizedClientError(BaseError):
    pass

class UnsupportedGrantType(BaseError):
    pass


class UnsupportedResponseTypeError(BaseError):
    pass


exception_map["access_denied"] = AccessDeniedError
exception_map["invalid_client"] = InvalidClientError
exception_map["invalid_grant"] = InvalidGrantError
exception_map["invalid_scope"] = InvalidScopeError
exception_map["invalid_request"] = InvalidRequestError
exception_map["invalid_scope"] = InvalidScopeError
exception_map["server_error"] = ServerError
exception_map["temporarily_unavailable"] = TemporarilyUnavailableError
exception_map["unauthorized_client"] = UnauthorizedClientError
exception_map["unsupported_grant_type"] = UnsupportedGrantType
exception_map["unsupported_response_type"] = UnsupportedResponseTypeError


class InvalidHttpStatusError(BaseException):
    pass

