from json import loads
from unittest import TestCase

from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationEndpointMixIn

from . import get_config
from . import TestAdapterImpl
from . import start_server

class TestAdapter(TestCase):
    def test_init(self):
        from sanction.flow import ResourceFlow 
        a = TestAdapterImpl(get_config())

        self.assertEquals(a.name, "testadapterimpl")
        self.assertTrue(isinstance(a.flow, ResourceFlow))
        
        self.assertEquals(a.config["client_id"], "base_id")

    def test_request(self):
        a = TestAdapterImpl(get_config())

        start_server()
        c = a.flow.authorization_received({
            "code":"test_code",
            "token_type":"Bearer"
        })

        start_server()
        r = loads(a.request("/me"))
        
        self.assertEquals(r["foo"], "bar")
