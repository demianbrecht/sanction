from unittest import TestCase

from . import get_config

class TestBaseFlow(TestCase):
    
    def test_inst(self):
        from sanction.adapters import BaseAdapter
        from sanction.flow import BaseFlow
        adapter = BaseAdapter(get_config())
        f = BaseFlow("grant_type", adapter)

        self.assertEquals(f.grant_type, "grant_type")
        self.assertEquals(f.adapter, adapter)

    def test_optional_attr(self):
        from sanction.adapters import BaseAdapter
        from sanction.flow import BaseFlow
        self.__test_attr = "test"

        f = BaseFlow("grant_type", BaseAdapter(get_config()))
        
        d = {}
        f.add_optional_attr("test_attr", self.__test_attr, d)
        self.assertEquals(self.__test_attr, d["test_attr"])


class TestAuthorizationRequest(TestCase):

    def test_authorization_uri(self):
        from urlparse import urlparse
        from urlparse import parse_qsl
        from sanction.flow import AuthorizationRequest
        from sanction.adapters.google import Google

        c = get_config()
        a = Google(get_config())
        uri = a.flow.authorization_uri()
        d = urlparse(uri)

        self.assertEquals(d.netloc, "accounts.google.com")
        qs = dict(parse_qsl(d.query))

        self.assertEquals(qs["redirect_uri"], c["google.redirect_uri"])
        self.assertEquals(qs["scope"], c["google.scope"])
        self.assertEquals(qs["access_type"], c["google.access_type"])
        self.assertEquals(qs["response_type"], "code")
        self.assertEquals(qs["client_id"], c["google.client_id"])


    def test_authorization_received(self):
        from sanction.flow import AuthorizationRequest
        from sanction.adapters.google import Google

