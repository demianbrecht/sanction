from unittest import TestCase

from sanction.adapters import BaseAdapter

from . import get_config

class TestBaseAdapter(TestCase):
    def test_init(self):
        from sanction.flow import AuthorizationRequestFlow
        a = BaseAdapter(get_config())

        self.assertEquals(a.name, "baseadapter")
 
        self.assertTrue(isinstance(a.flow, AuthorizationRequestFlow))


class TestAuthorizationEndpointMixIn(TestCase):
    def test_init(self):
        from sanction.flow import AuthorizationEndpointMixIn
        a = AuthorizationEndpointMixIn()

        self.assertIsNone(a.authorization_endpoint)
        
        a.authorization_endpoint = "foo"
        self.assertEquals(a.authorization_endpoint, "foo")
