from ConfigParser import ConfigParser

from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationRequestFlow


class TestAdapterImpl(BaseAdapter, AuthorizationEndpointMixIn):

    def __init__(self, config, flow=AuthorizationRequestFlow):
        BaseAdapter.__init__(self, get_config(), flow=flow)
        self.authorization_endpoint = "http://localhost:4242"



def get_config():
    config = ConfigParser({}, dict)
    config.read("tests/tests.ini") 

    c = config._sections["sanction"]
    del c["__name__"]

    if "http_debug" in c:
        c["http_debug"] = c["http_debug"] == "true"

    return config._sections["sanction"]

