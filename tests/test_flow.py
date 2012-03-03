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

log = getLogger(__name__)

class RequestHandler(BaseHTTPRequestHandler):
    def shutdown(self, param):
        BaseHTTPRequestHandler.shutdown(self)

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        self.send_response(404)

    def do_POST(self):
        if self.path == "/token":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(dumps({
                "access_token":"test_token",
                "token_type":"Bearer"
            }))


class TestServer(HTTPServer):
    def __init__(self, e):
        BaseServer.__init__(self, ("", test_port), RequestHandler)
        ctx = SSL.Context(SSL.SSLv23_METHOD)

        pem = "tests/cert.pem"
        ctx.use_privatekey_file(pem)
        ctx.use_certificate_file(pem)

        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
            self.socket_type))

        self.server_bind()
        self.server_activate()
        e.set()

    def shutdown_request(self, foo):
        pass


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
        from sanction.flow import AuthorizationRequestFlow
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
            "token_type": "Bearer"
        })
        #TODO: Test credentials


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


def start_server():
    e = Event()
    t = Thread(target=spawn_server, args=(e,))
    t.daemon = True
    t.start()
    e.wait()

def spawn_server(e):
    s = TestServer(e)
    s.handle_request()

