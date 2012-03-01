from unittest import TestCase

class TestHTTPSServices(TestCase):

    def test_init(self):
        from sanction.services import HTTPSService
        from sanction.exceptions import InvalidHTTPStatusError
        s = HTTPSService()

        d = s.request(
            "https://accounts.google.com/ServiceLogin?service=mail")
        self.assertIsNotNone(d)

        try:
            s.request("https://google.com")
            self.fail()

        except InvalidHTTPStatusError as e:
            self.assertEquals(e.status, 301)
