from sanction.util import safe_get

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


class InvalidRequestError(BaseError):
    pass


class UnauthorizedClientError(BaseError):
    pass


class AccessDeniedError(BaseError):
    pass


class UnsuportedResponseError(BaseError):
    pass


class InvalidScopeError(BaseError):
    pass


class ServerError(BaseError):
    pass


class TemporarilyUnavailableError(BaseError):
    pass


class InvalidStateError(BaseError):
    pass
