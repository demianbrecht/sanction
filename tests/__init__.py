from ConfigParser import ConfigParser

from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import ResourceEndpointMixIn

test_port = 4242 
test_uri = "https://localhost:%d" % test_port

class TestAdapterImpl(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = "%s%s" % (test_uri, "/auth")
    token_endpoint = "%s%s" % (test_uri, "/token")
    resource_endpoint = "%s%s" % (test_uri, "/resource")

    def __init__(self, config, flow=AuthorizationRequestFlow):
        BaseAdapter.__init__(self, get_config(), flow=flow)


def get_config():
    config = ConfigParser({}, dict)
    config.read("tests/tests.ini") 

    c = config._sections["sanction"]
    del c["__name__"]

    if "http_debug" in c:
        c["http_debug"] = c["http_debug"] == "true"

    return config._sections["sanction"]

