from unittest import TestCase

from sanction.adapters import BaseAdapter

from . import get_config

class TestBaseAdapter(TestCase):
    def test_init(self):
        from sanction.flow import AuthorizationRequest
        a = BaseAdapter(get_config())

        self.assertEquals(a.name, "baseadapter")
        self.assertTrue(isinstance(a.flow, AuthorizationRequest))


class TestResourceEndpointMixIn(TestCase):
    def test_init(self):
        from sanction.adapters import ResourceEndpointMixIn
        a = ResourceEndpointMixIn()

        self.assertIsNone(a.resource_endpoint)
        self.assertIsNone(a.token_endpoint)

        a.resource_endpoint = "foo"
        self.assertEquals(a.resource_endpoint, "foo")

        a.token_endpoint = "bar"
        self.assertEquals(a.token_endpoint, "bar")


class TestAuthorizationEndpointMixIn(TestCase):
    def test_init(self):
        from sanction.adapters import AuthorizationEndpointMixIn
        a = AuthorizationEndpointMixIn()

        self.assertIsNone(a.authorization_endpoint)
        
        a.authorization_endpoint = "foo"
        self.assertEquals(a.authorization_endpoint, "foo")
