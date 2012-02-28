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
