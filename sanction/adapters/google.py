from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import AuthorizationEndpointMixIn
from sanction.util import safe_get


class GoogleAuthorizationRequestFlow(AuthorizationRequestFlow):

    def authorization_uri(self, state=None):
        uri = AuthorizationRequestFlow.authorization_uri(self, state)
        access_type = safe_get("access_type", self.adapter.config,
            required=True)
        return "%s&access_type=%s" % (uri, access_type)


class Google(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
    token_endpoint = "https://accounts.google.com/o/oauth2/token"
    resource_endpoint = "https://www.googleapis.com/oauth2/v1"

    def __init__(self, config, flow=GoogleAuthorizationRequestFlow):
        BaseAdapter.__init__(self, config, flow=flow)

