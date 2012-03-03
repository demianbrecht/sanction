from unittest import TestCase

class TestCredentialsFactory(TestCase):

    def test_create(self):
        from sanction.credentials import credentials_factory
        data = {
            "access_token": "test_token",
            "token_type": "Bearer"
        }
        c = credentials_factory("Bearer", data)
        self.assertEquals(c.access_token, data["access_token"])

        self.assertEquals(c.http_header(), {"Authorization": "Bearer %s" % 
            data["access_token"]})

        self.assertEquals(c.query_param(), "access_token=%s" %
           data["access_token"])

        c.access_token = "foo"
        self.assertEquals(c.access_token, "foo")

        try:
            c = credentials_factory("foo", data)
            self.fail()

        except NotImplementedError: pass
