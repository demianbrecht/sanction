from urlparse import parse_qsl
from urllib import urlencode

from sanction.adapters import BaseAdapter
from sanction.credentials import BaseCredentials
from sanction.credentials import BearerCredentials
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import AuthorizationEndpointMixIn
from sanction.util import safe_get

class FacebookAuthorizationRequestFlow(AuthorizationRequestFlow):

    def __init__(self, adapter):
        AuthorizationRequestFlow.__init__(self, adapter)

    def authorization_uri(self, state=None):
        data = {
            "response_type": "code",
            "client_id": self.client_id 
        }
        self.add_optional_attr("redirect_uri", self.redirect_uri, data)
        self.add_optional_attr("scope", self.scope, data)
        self.add_optional_attr("state", state, data)

        return "%s?%s" % (self.adapter.authorization_endpoint, urlencode(data))

    def parse_access_token(self, data):
        data = dict(parse_qsl(data))
        # facebook doesn't send this back and it's requred by the
        # credentials factory
        data["token_type"] = "Bearer"
        return data 


class FacebookCredentials(BearerCredentials):
    context = "facebook"

    def normalize_token(self, data):
        return {
            "access_token": data["access_token"],
            "expires_in": data["expires"]
        }

class Facebook(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = "https://www.facebook.com/dialog/oauth"
    token_endpoint = "https://graph.facebook.com/oauth/access_token"
    resource_endpoint = "https://graph.facebook.com"

    def __init__(self, config, flow=None):
        BaseAdapter.__init__(self, config, 
            flow=flow or FacebookAuthorizationRequestFlow)

    def request(self, path, method="GET", body=None): #pragma: no cover 
        assert(isinstance(self.credentials, BaseCredentials))
        uri = "%s%s?%s" % (self.resource_endpoint, path,
            self.credentials.query_param())
        return self.service.request(uri, method, body) 


