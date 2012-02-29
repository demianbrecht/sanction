from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationRequestFlow
from sanction.util import safe_get

class GoogleAuthorizationRequestFlow(AuthorizationRequestFlow):

    def __init__(self, grant_type, adapter):
        AuthorizationRequestFlow.__init__(self, grant_type, adapter)
        self.__access_type = None


    def authorization_uri(self, state=None):
        uri = AuthorizationRequestFlow.authorization_uri(self, state)
        access_type = safe_get("access_type", self.adapter.config, required=True)
        return "%s&access_type=%s" % (uri, access_type)


class Google(BaseAdapter):

    def __init__(self, config, flow=GoogleAuthorizationRequestFlow):
        BaseAdapter.__init__(self, config, flow)

        print "** %s" % self.flow.authorization_endpoint
        self.flow.authorization_endpoint = \
            "https://accounts.google.com/o/oauth2/auth"
        print "** %s" % self.flow.authorization_endpoint
