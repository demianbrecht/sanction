from sanction.adapters import BaseAdapter
from sanction.adapters import AuthorizationEndpointMixIn
from sanction.adapters import ResourceEndpointMixIn
from sanction.flow import AuthorizationRequest
from sanction.util import safe_get

class GoogleAuthorizationRequest(AuthorizationRequest):

    def __init__(self, grant_type, adapter):
        AuthorizationRequest.__init__(self, grant_type, adapter)
        self.__access_type = None


    def authorization_uri(self, state=None):
        uri = AuthorizationRequest.authorization_uri(self, state)
        access_type = safe_get("access_type", self.adapter.config, required=True)
        return "%s&access_type=%s" % (uri, access_type)


class Google(BaseAdapter, ResourceEndpointMixIn, AuthorizationEndpointMixIn):

    def __init__(self, config, flow=GoogleAuthorizationRequest):
        ResourceEndpointMixIn.__init__(self)
        AuthorizationEndpointMixIn.__init__(self)
        BaseAdapter.__init__(self, config, flow)

        self.authorization_endpoint = \
            "https://accounts.google.com/o/oauth2/auth"
