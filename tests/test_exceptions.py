from unittest import TestCase

class TestBaseError(TestCase):

    def test_inst(self):
        from sanction.exceptions import BaseError
        e = BaseError({})

        self.assertEquals(e.description, None)
        self.assertEquals(e.error_uri, None)
        self.assertEquals(e.state, None)

        e = BaseError({
            "description": "foo",
            "error_uri": "bar",
            "state": "state"
        })

        self.assertEquals(e.description, "foo")
        self.assertEquals(e.error_uri, "bar")
        self.assertEquals(e.state, "state")


    def test_factory(self):
        from sanction.exceptions import AccessDeniedError
        from sanction.exceptions import exception_factory
        self.assertTrue(isinstance(exception_factory("access_denied", {}),
            AccessDeniedError))

        self.assertIsNotNone("%s" % exception_factory("invalid_client", {}))

        try:
            e = exception_factory("foo", {})
            self.fail()
        except: pass

