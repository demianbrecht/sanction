from unittest import TestCase

from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationEndpointMixIn

from . import get_config
from . import TestAdapterImpl

class TestAdapter(TestCase):
    def test_init(self):
        from sanction.flow import ResourceFlow 
        a = TestAdapterImpl(get_config())

        self.assertEquals(a.name, "testadapterimpl")
        self.assertTrue(isinstance(a.flow, ResourceFlow))
        
        self.assertEquals(a.config["client_id"], "base_id")



