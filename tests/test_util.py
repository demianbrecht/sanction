from unittest import TestCase
from . import get_config

class TestConfig(TestCase):

    def test_safe_get(self):
        from sanction.util import safe_get

        settings = {"foo": "bar"}

        self.assertEquals(safe_get("foo", settings), "bar")
        self.assertEquals(safe_get("bar", settings, required=False), None)
        self.assertEquals(safe_get("bar", settings, required=False,
            default="foo"), "foo")
        try:
            safe_get("bar", settings, required=True)
            self.fail()

        except KeyError: pass


class TestAdapterConfig(TestCase):

    def test_adapter_config(self):
        from sanction.config import adapter_config

        c = adapter_config("google", get_config())

        self.assertIsNotNone(c["client_id"])
        self.assertIsNotNone(c["client_secret"])
        self.assertIsNotNone(c["redirect_uri"])
        self.assertIsNotNone(c["scope"])
        self.assertEquals(c["http_debug"], True)
