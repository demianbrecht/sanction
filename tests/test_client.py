from unittest import TestCase

from . import get_config

class TestClient(TestCase):

    def test_inst(self):
        from sanction.client import Client
        from sanction.adapters.google import Google

        c = Client(Google, get_config())

        self.assertTrue(isinstance(c.adapter, Google))
