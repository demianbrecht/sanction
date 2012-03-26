from json import loads
from unittest import TestCase

from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationEndpointMixIn

from . import get_config
from . import TestAdapterImpl
from . import start_server

class TestAdapter(TestCase):
    def test_init(self):
        from sanction.flow import ResourceFlow 
        a = TestAdapterImpl(get_config())

        self.assertEquals(a.name, "testadapterimpl")
        self.assertTrue(isinstance(a.flow, ResourceFlow))
        
        self.assertEquals(a.config["client_id"], "base_id")

        class DefaultAdapter(BaseAdapter, AuthorizationEndpointMixIn):
            token_endpoint = ""
            resource_endpoint = ""
            authorization_endpoint = ""

        a = DefaultAdapter({
            "defaultadapter.client_id": "",
            "defaultadapter.client_secret": "",
            "defaultadapter.redirect_uri": "",
            "defaultadapter.scope": ""
        })

    def test_service(self):
        from sanction.services import BaseService
        class TestService(BaseService):
            def request(self): # required
                pass

        a = TestAdapterImpl(get_config(), service=TestService)

        self.assertIsNotNone(a)

    def test_request(self):
        a = TestAdapterImpl(get_config())

        start_server()
        c = a.flow.authorization_received({
            "code":"test_code",
            "token_type":"Bearer",
            "expires_in":3600
        })

        start_server()
        r = loads(a.request("/me"))
        
        self.assertEquals(r["foo"], "bar")


class TestGoogle(TestCase):
    def test_flow(self):
        from urlparse import urlparse

        from sanction.adapters.google import Google
        from sanction.adapters.google import GoogleAuthorizationRequestFlow

        f = GoogleAuthorizationRequestFlow(Google(get_config()))
        uri = urlparse(f.authorization_uri())

        self.assertEquals(uri.netloc, "accounts.google.com")
        self.assertEquals(uri.scheme, "https")


class TestFacebook(TestCase):
    def test_flow(self):
        from urlparse import urlparse

        from sanction.adapters.facebook import Facebook
        from sanction.adapters.facebook import FacebookAuthorizationRequestFlow

        f = FacebookAuthorizationRequestFlow(Facebook(get_config()))
        uri = urlparse(f.authorization_uri())

        self.assertEquals(uri.netloc, "www.facebook.com")
        self.assertEquals(uri.scheme, "https")

    def test_parse(self):
        from sanction.adapters.facebook import Facebook
        from sanction.adapters.facebook import FacebookAuthorizationRequestFlow

        f = FacebookAuthorizationRequestFlow(Facebook(get_config()))
        data = f.parse_access_token("foo=bar&syn=ack")

        self.assertEquals(data["foo"], "bar")
        self.assertEquals(data["syn"], "ack")

    def test_normalize(self):
        from sanction.adapters.facebook import FacebookCredentials

        c = FacebookCredentials({
            "token_type": "Bearer",
            "expires": 3600,
            "access_token": "my_token"
        })
        self.assertEquals(c.expires_in, 3600)


class TestFoursquare(TestCase):
    def test_flow(self):
        from sanction.adapters.foursquare import Foursquare
        from sanction.adapters.foursquare import \
            FoursquareAuthorizationRequestFlow

        f = FoursquareAuthorizationRequestFlow(Foursquare(get_config()))
        data = f.parse_access_token('''{
            "foo":"bar",
            "syn":"ack"
        }''')

        self.assertEquals(data["foo"], "bar")
        self.assertEquals(data["syn"], "ack")

    def test_cred(self):
        from urlparse import parse_qsl
        from sanction.adapters.foursquare import FoursquareCredentials

        c = FoursquareCredentials({
           "access_token": "foo"
        })

        self.assertIsNotNone(dict(parse_qsl(c.query_param()))["oauth_token"])
       

