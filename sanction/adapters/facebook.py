from urlparse import parse_qsl
from urllib import urlencode

from sanction.adapters import BaseAdapter
from sanction.credentials import BaseCredentials
from sanction.credentials import BearerCredentials
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import AuthorizationEndpointMixIn
from sanction.util import safe_get

class FacebookAuthorizationRequestFlow(AuthorizationRequestFlow):
    """ AuthorizationRequestFlow for Facebook.
    """

    def __init__(self, adapter):
        AuthorizationRequestFlow.__init__(self, adapter)

    def authorization_uri(self, state=None):
        """ Authorization URI for Facebook.

        Facebook deviates from the :term:`OAuth2` spec in that the scope is
        comma-delimited whereas the spec states that it should be space
        delimited.
        """
        data = {
            "response_type": "code",
            "client_id": self.client_id 
        }
        self.add_optional_attr("redirect_uri", self.redirect_uri, data)
        self.add_optional_attr("scope", self.scope, data)
        self.add_optional_attr("state", state, data)

        return "%s?%s" % (self.adapter.authorization_endpoint, urlencode(data))

    def parse_access_token(self, data):
        """ Parses the access token

        Facebook deviates from the :term:`OAuth2` spec by using URL formatting
        to pass back credentials rather than JSON.
        """
        data = dict(parse_qsl(data))
        # facebook doesn't send this back and it's requred by the
        # credentials factory
        data["token_type"] = "Bearer"
        return data 


class FacebookCredentials(BearerCredentials):
    """ Credentials for Facebook
    """
    context = "facebook"

    def normalize_token(self, data):
        """ Normalizes the token data for Facebook

        The expiration data from Facebook is returned under the key
        ``"expires"`` rather than ``"expires_in"``.
        """
        return {
            "access_token": data["access_token"],
            "expires_in": data["expires"],
            "refresh_token": "refresh_token" in data and data["refresh_token"]\
                or None
        }

class Facebook(BaseAdapter, AuthorizationEndpointMixIn):
    """ Facebook adapter implementation

    Facebook only supports the 
    :py:class:`~sanction.adapters.facebook.FacebookAuthorizationRequestFlow`,
    so the optional :py:class:`~sanction.flow` c'tor parameter is not
    available.

    :param config: A ``dict`` containing adapter configuration data.
    """
    authorization_endpoint = "https://www.facebook.com/dialog/oauth"
    token_endpoint = "https://graph.facebook.com/oauth/access_token"
    resource_endpoint = "https://graph.facebook.com"

    def __init__(self, config):
        BaseAdapter.__init__(self, config, FacebookAuthorizationRequestFlow)

    def request(self, path, method="GET", body=None): #pragma: no cover 
        """ Sends a request to Facebook

        Facebook parameters must be sent via query parameters rather than
        through HTTP headers.
        """
        assert(isinstance(self.credentials, BaseCredentials))
        uri = "%s%s?%s" % (self.resource_endpoint, path,
            self.credentials.query_param())
        return self.service.request(uri, method, body) 


