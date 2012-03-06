from json import loads
from unittest import TestCase

from . import start_server

class TestHTTPSServices(TestCase):

    def test_init(self):
        from sanction.services import HTTPSService
        from sanction.exceptions import InvalidHTTPStatusError
        s = HTTPSService()

        start_server()
        try:
            d = s.request("https://localhost:4242")
            self.fail()
        except InvalidHTTPStatusError as e:
            self.assertEquals(e.status, 404)

        start_server()
        d = loads(s.request("https://localhost:4242/resource/me"))
        self.assertEquals(d["foo"], "bar")


