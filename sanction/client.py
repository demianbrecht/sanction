# vim: set ts=4 sw=4 et:

from json import loads
from urllib import urlencode
from urllib2 import urlopen
from urlparse import parse_qsl

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


    def request_token(self, data=None, parser=None, grant_type=None):
        data = data and data or {}
        if data.has_key("error"):
            raise IOError(data["error"])
        else:
            kwargs = {"grant_type": grant_type}
        if "code" in data: kwargs["code"] = data["code"]

        self.__get_access_token(self.client_id,
        self.client_secret, parser=parser, **kwargs)


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


    def __get_access_token(self, client_id, client_secret, code=None,
        grant_type=None, parser=None): 

        parser = parser and parser or loads
        o = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type and grant_type or "authorization_code"
        }
        if code is not None: o["code"] = code
        if self.redirect_uri is not None: 
            o["redirect_uri"] = self.redirect_uri

        h = urlopen(self.token_endpoint, urlencode(o))
        r = parser(h.read())

        for key in r:
            setattr(self, key, r[key])

        assert(self.access_token is not None)

