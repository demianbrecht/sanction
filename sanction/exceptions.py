""" Module defining OAuth 2.0 exceptions

The :py:meth:`~sanction.exceptions.exception_factory` method is responsible
for instantiating an exception matching the OAuth2 error code. The intention
of this module is to prevent users from having to know about the internals
of the OAuth2 protocol (in this context, exceptions).
"""

from abc import ABCMeta
from abc import abstractproperty
from logging import getLogger

from sanction.util import safe_get

log = getLogger(__name__)

class BaseError(BaseException):
    """ Base exception class.

    This base class should be extended by all OAuth2 exceptions generated
    by the OAuth2 provider.
    """
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
        return "%s" % self.__description


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
    
    def __str__(self): #pragma: no cover
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
    """ Exceptions factory method.

    """
    for cls in BaseError.__subclasses__():
        if cls.error_name == error_name:
            return cls(data)

    raise NotImplementedError("Unhandled error: %s" % error_name)

