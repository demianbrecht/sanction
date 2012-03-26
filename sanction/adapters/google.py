from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import AuthorizationEndpointMixIn
from sanction.util import safe_get


class GoogleAuthorizationRequestFlow(AuthorizationRequestFlow):
    """ Authorization flow for Google
    """

    def authorization_uri(self, state=None):
        """ Google's authorization URI

        Google differs from the :term:`OAuth2` spec by appending the
        ``access_type`` request value through a URI query param.
        """
        uri = AuthorizationRequestFlow.authorization_uri(self, state)
        access_type = safe_get("access_type", self.adapter.config,
            required=True)
        return "%s&access_type=%s" % (uri, access_type)


class Google(BaseAdapter, AuthorizationEndpointMixIn):
    """ Google adapter implementation

    Google only supports the authorization request flow. As such, if another
    flow is set on :py:class:`~sanction.client.Client` instantiation it will
    be ignored.
    """
    authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
    token_endpoint = "https://accounts.google.com/o/oauth2/token"
    resource_endpoint = "https://www.googleapis.com/oauth2/v1"
    def __init__(self, config, flow = None):
            BaseAdapter.__init__(self, config, GoogleAuthorizationRequestFlow)

