import socket

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from json import dumps
from logging import getLogger

from OpenSSL import SSL
from SocketServer import BaseServer
from threading import Event
from threading import Thread

from unittest import TestCase

from . import get_config
from . import TestAdapterImpl
from . import test_port
from . import test_uri
from . import start_server

log = getLogger(__name__)


class TestResourceFlow(TestCase):
    
    def test_inst(self):
        from sanction.flow import ResourceFlow
        from sanction.services import HTTPSService

        adapter = TestAdapterImpl(get_config())
        f = ResourceFlow("grant_type", adapter)

        self.assertEquals(f.grant_type, "grant_type")
        self.assertEquals(f.adapter, adapter)


    def test_optional_attr(self):
        from sanction.adapters import BaseAdapter
        from sanction.flow import ResourceFlow
        from sanction.services import HTTPSService

        self.__test_attr = "test"

        f = ResourceFlow("grant_type", TestAdapterImpl(get_config()))
        
        d = {}
        f.add_optional_attr("test_attr", self.__test_attr, d)
        self.assertEquals(self.__test_attr, d["test_attr"])


class TestAuthorizationRequestFlow(TestCase):

    def test_authorization_uri(self):
        from urlparse import urlparse
        from urlparse import parse_qsl
        from sanction.flow import AuthorizationRequestFlow

        f = AuthorizationRequestFlow(TestAdapterImpl(get_config()))

        uri = urlparse(f.authorization_uri())
        qs = dict(parse_qsl(uri.query))

        c = get_config()
        self.assertEquals(qs["scope"], c["testadapterimpl.scope"])
        self.assertEquals(qs["redirect_uri"], 
            c["testadapterimpl.redirect_uri"])
        self.assertEquals(qs["response_type"], "code")
        self.assertEquals(qs["client_id"], c["testadapterimpl.client_id"])


    def test_authorization_received(self):
        from sanction.credentials import BearerCredentials
        from sanction.flow import AuthorizationRequestFlow
        from sanction.exceptions import InvalidHTTPStatusError
        from sanction.exceptions import InvalidStateError
        from sanction.exceptions import InvalidClientError

        a = TestAdapterImpl(get_config())

        #unhandled data
        try:
            a.flow.authorization_received({})
            self.fail()
        except Exception:
            pass


        start_server()
        cred = a.flow.authorization_received({
            "code": "test_code",
            "token_type": "Bearer",
            "expires_in": 3600
        })
        self.assertTrue(isinstance(cred, BearerCredentials))
        self.assertEquals(cred.expires_in, 3600)

        start_server()
        try:
            a.request("/invalid")
            self.fail()
        except InvalidHTTPStatusError as e:
            self.assertEquals(e.reason, "Not Found")
            

        try:
            a.flow.authorization_received({
                "error":"invalid_client",
                "description":"test"
            })
            self.fail()
        except InvalidClientError:
            pass


        #invalid state
        try:
            a.flow.authorization_received({
                "code":"test",
                "state":"foo"
            }, expected_state="bar")
            self.fail()
        except InvalidStateError:
            pass

