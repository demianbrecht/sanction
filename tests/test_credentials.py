from unittest import TestCase

class TestCredentialsFactory(TestCase):

    def test_context(self):
        from sanction.credentials import BearerCredentials
        from sanction.credentials import credentials_factory

        class ContextCredentials(BearerCredentials):
            context = "my_context"
            token_type = "Bearer"

        c = credentials_factory("Bearer", "my_context", {
            "access_token":"test_token",
            "token_type":"Bearer",
            "expires_in":3600
        })

        self.assertTrue(isinstance(c, ContextCredentials))


    def test_create(self):
        from sanction.credentials import credentials_factory
        data = {
            "access_token": "test_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        c = credentials_factory("Bearer", "invalid", data)
        self.assertEquals(c.access_token, data["access_token"])

        self.assertEquals(c.http_header(), {"Authorization": "Bearer %s" % 
            data["access_token"]})

        self.assertEquals(c.query_param(), "access_token=%s" %
           data["access_token"])

        c.access_token = "foo"
        self.assertEquals(c.access_token, "foo")

        try:
            c = credentials_factory("foo", "invalid", data)
            self.fail()

        except NotImplementedError: pass
