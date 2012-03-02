from unittest import TestCase

from . import get_config

class TestClient(TestCase):

    def test_inst(self):
        from sanction.client import Client

