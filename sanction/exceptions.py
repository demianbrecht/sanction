from abc import ABCMeta
from abc import abstractproperty

from sanction.util import safe_get

class BaseError(BaseException):
    __metaclass__ = ABCMeta

    def __init__(self, response):
        self.__description = safe_get("description", response)
        self.__error_uri = safe_get("error_uri", response)
        self.__state = safe_get("state", response)

    @abstractproperty
    def error_name(self): pass #pragma: no cover

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
    error_name = "access_denied"

class InvalidClientError(BaseError):
    error_name = "invalid_client"

class InvalidGrantError(BaseError):
    error_name = "invalid_grant"

class InvalidHTTPStatusError(BaseException):
    def __init__(self, status, reason):
        self.__status = status
        self.__reason = reason
    
    def __str__(self):
        return "%s (%d)" % (self.__reason,
            self.__status)

    @property
    def status(self):
        return self.__status

    @property
    def reason(self):
        return self.__reason

class InvalidScopeError(BaseError):
    error_name = "invalid_scope"

class InvalidStateError(BaseException):
    pass

class InvalidRequestError(BaseError):
    error_name = "invalid_request"

class ServerError(BaseError):
    error_name = "server_error"

class TemporarilyUnavailableError(BaseError):
    error_name = "temporarily_unavailable"

class UnauthorizedClientError(BaseError):
    error_name = "unauthorized_client"

class UnsupportedGrantType(BaseError):
    error_name = "unsupported_grant_type"

class UnsupportedResponseTypeError(BaseError):
    error_name = "unsupported_response_type"

def exception_factory(error_name, data):
    for cls in BaseError.__subclasses__():
        if cls.error_name == error_name:
            return cls(data)

    raise NotImplementedError("Unhandled error: %s" % error_name)
