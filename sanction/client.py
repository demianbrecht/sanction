# vim: set ts=4 sw=4 et:
""" OAuth 2.0 client librar
"""

from json import loads
from urllib import urlencode
from urllib2 import urlopen


class Client(object):
    """ OAuth 2.0 client object
    """

    def __init__(self, auth_endpoint=None, token_endpoint=None,
        resource_endpoint=None, client_id=None, client_secret=None,
        redirect_uri=None):

        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.resource_endpoint = resource_endpoint
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_key = "access_token"

    def auth_uri(self, scope=None, scope_delim=None, state=None, **kwargs):
        """  Builds the auth URI for the authorization endpoint
        """
        scope_delim = scope_delim and scope_delim or " "
        kwargs.update({
            "client_id": self.client_id,
            "response_type": "code",
        })

        if scope is not None:
            kwargs["scope"] = scope_delim.join(scope)

        if state is not None:
            kwargs["state"] = state

        if self.redirect_uri is not None:
            kwargs["redirect_uri"] = self.redirect_uri

        return "%s?%s" % (self.auth_endpoint, urlencode(kwargs))

    def request_token(self, code=None, grant_type=None, parser=None, **kwargs):
        """ Request an access token from the token endpoint
        :param parser: Callback to deal with returned data. Not all providers
                       use JSON.
        :param grant_type: The grant type of the request. These may be types
                           such as authorization_code, client_credentials,
                           refresh_token, etc.
        :param kwargs: Any other data that should be sent along with the
                       token request to the token endpoint. For example, when
                       issuing a request to refresh a token, the refresh_token
                       param must be sent along with the request.
        """
        kwargs = kwargs and kwargs or {}

        if code is not None:
            kwargs.update({'code': code})

        parser = parser and parser or loads
        kwargs.update({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": grant_type and grant_type or "authorization_code"
        })
        if self.redirect_uri is not None:
            kwargs.update({'redirect_uri': self.redirect_uri})

        resp = parser(urlopen(self.token_endpoint, urlencode(
            kwargs)).read())

        for key in resp:
            setattr(self, key, resp[key])

        assert(self.access_token is not None)

    def request(self, path, query=None, data=None, parser=None):
        """ Request user data from the resource endpoint
        :param path: The path of the resource
        :param query: A dict of parameters to be sent as the request
                      querystring
        :param data: Data to be POSTed to the resource endpoint
        :param parser: Parser callback to deal with the returned data. Defaults
                       to ``json.loads`.`
        """
        assert(self.access_token is not None)
        parser = parser and parser or loads

        if query is None:
            query = {}

        query.update({
            self.access_token_key: self.access_token
        })

        path = "%s%s?%s" % (self.resource_endpoint, path, urlencode(query))

        return parser(urlopen(path, data).read())
