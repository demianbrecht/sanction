from urlparse import parse_qsl
from urllib import quote_plus
from urllib import urlencode

from sanction.adapters import BaseAdapter
from sanction.credentials import BaseCredentials
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationRequestFlow


class StackExchangeAuthorizationRequestFlow(AuthorizationRequestFlow):
    def parse_access_token(self, data):
        """ StackExchange access token parser

        StackExchange sends back access data in URL format
        """
        data = dict(parse_qsl(data))
        data["token_type"] = "Bearer"
        return data 


class StackExchange(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = "https://stackexchange.com/oauth"
    token_endpoint = "https://stackexchange.com/oauth/access_token"
    resource_endpoint = "https://api.stackexchange.com/2.0"

    def __init__(self, config, flow = None):
        BaseAdapter.__init__(self, config,
            StackExchangeAuthorizationRequestFlow)

    def request(self, path, method="GET", body=None): #pragma: no cover 
        """ StackExchange API request

        StackExchange passes query params and also requires a "key" to be sent
        """
        assert(isinstance(self.credentials, BaseCredentials))
        uri = "%s%s?%s&%s&key=%s" % (self.resource_endpoint, path,
            self.credentials.query_param(), body,
            quote_plus(self.config["key"]))
        return self.service.request(uri, method) 
