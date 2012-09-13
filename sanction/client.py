# vim: set ts=4 sw=4 et:

from json import loads
from urllib import urlencode
from urllib2 import urlopen

class Client(object):

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
        scope_delim = scope_delim and scope_delim or " "
        o = {
            "client_id": self.client_id,
            "response_type": "code",
        }
        if scope is not None: o["scope"] = scope_delim.join(scope)
        if state is not None: o["state"] = state
        if self.redirect_uri is not None: o["redirect_uri"] = self.redirect_uri
        for kw in kwargs:
            assert(kw not in o)
            o[kw] = kwargs[kw]

        return "%s?%s" % (self.auth_endpoint, urlencode(o))


    def request_token(self, data=None, grant_type=None, parser=None, **kwargs):
        """ Request an access token from the token endpoint
        :param data: If applicable to the flow, this should be a dict 
                     containing data returned from the authorization
                     endpoint.
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
        data = data and data or {}
        if data.has_key("error"):
            raise IOError(data["error"])
        else:
            kwargs.update({'grant_type': grant_type})
        if "code" in data: kwargs.update({'code': data['code']})

        assert(self.token_endpoint is not None)

        parser = parser and parser or loads
        kwargs.update({
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": grant_type and grant_type or "authorization_code"
        })
        if self.redirect_uri is not None: 
            kwargs.update({'redirect_uri': self.redirect_uri})

        h = urlopen(self.token_endpoint, urlencode(kwargs))
        r = parser(h.read())

        for key in r:
            setattr(self, key, r[key])

        assert(self.access_token is not None)


    def request(self, path, qs=None, data=None, parser=None):
        assert(self.access_token is not None)
        parser = parser and parser or loads
        if qs is None: qs = {}
        qs.update({
            self.access_token_key: self.access_token
        })
        path = "%s%s?%s" % (self.resource_endpoint, path, urlencode(qs))
        h = urlopen(path, data)

        return parser(h.read())


