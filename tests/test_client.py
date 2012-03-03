from unittest import TestCase

from sanction.credentials import BearerCredentials

from . import get_config
from . import start_server
from . import TestAdapterImpl

class TestClient(TestCase):

    def test_inst(self):
        from urlparse import urlparse
        from urlparse import parse_qsl
        from sanction.client import Client

        c = get_config()
        client = Client(TestAdapterImpl, c)
        uri = client.flow.authorization_uri()
        o = urlparse(uri)
        qs = dict(parse_qsl(o.query))

        self.assertEquals(qs["scope"], c["testadapterimpl.scope"])
        self.assertEquals(qs["redirect_uri"],
            c["testadapterimpl.redirect_uri"])
        self.assertEquals(qs["response_type"], "code")
        self.assertEquals(qs["client_id"], c["testadapterimpl.client_id"])
        
        start_server()
        cred = client.flow.authorization_received({
            "code": "test"
        })
        self.assertTrue(isinstance(cred, BearerCredentials))

        start_server()
        r = client.request("/me")

