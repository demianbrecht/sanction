from sanction.adapters import BaseAdapter
from sanction.credentials import BaseCredentials
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import AuthorizationEndpointMixIn

class DeviantArtAuthorizationRequestFlow(AuthorizationRequestFlow):
    def parse_access_token(self, data):
        """ Parses the access token

        DeviantArt deviates (haha) from the :term:`OAuth2` spec by not passing
        back the "Bearer" token type, which is expected by sanction
        """
        data = AuthorizationRequestFlow.parse_access_token(self, data)
        data["token_type"] = "Bearer"
        return data 


class DeviantArt(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = \
        "https://www.deviantart.com/oauth2/draft15/authorize"
    token_endpoint = "https://www.deviantart.com/oauth2/draft15/token"
    resource_endpoint = "https://www.deviantart.com/api/draft15"

    def __init__(self, config, flow = None):
        BaseAdapter.__init__(self, config, DeviantArtAuthorizationRequestFlow)

    def request(self, path, method="GET", body=None): #pragma: no cover 
        assert(isinstance(self.credentials, BaseCredentials))
        uri = "%s%s?%s" % (self.resource_endpoint, path,
            self.credentials.query_param())
        return self.service.request(uri, method, body) 

