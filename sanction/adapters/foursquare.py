from urllib import urlencode

from sanction.adapters import BaseAdapter
from sanction.credentials import BaseCredentials
from sanction.credentials import BearerCredentials
from sanction.credentials import credentials_factory 
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import AuthorizationEndpointMixIn


class FoursquareAuthorizationRequestFlow(AuthorizationRequestFlow):
    def parse_access_token(self, data):
        """ Parses the access token

        Foursquare deviates from the :term:`OAuth2` spec by not passing
        back the "Bearer" token type, which is expected by sanction
        """
        data = AuthorizationRequestFlow.parse_access_token(self, data)
        data["token_type"] = "Bearer"
        return data 


class FoursquareCredentials(BearerCredentials):
    context = "foursquare"

    def query_param(self):
        """ query_param for Foursquare

        Foursquare uses oauth_token as the token key rather than access_token
        """
        return "oauth_token=%s" % self.access_token


class Foursquare(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = "https://foursquare.com/oauth2/authenticate"
    token_endpoint = "https://foursquare.com/oauth2/access_token"
    resource_endpoint = "https://api.foursquare.com/v2"

    def __init__(self, config, flow = None):
        BaseAdapter.__init__(self, config, FoursquareAuthorizationRequestFlow)

    def request(self, path, method="GET", body=None): #pragma: no cover 
        assert(isinstance(self.credentials, BaseCredentials))
        uri = "%s%s?%s" % (self.resource_endpoint, path,
            self.credentials.query_param())
        return self.service.request(uri, method, body) 

