import socket 

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from ConfigParser import ConfigParser
from json import dumps
from OpenSSL import SSL
from SocketServer import BaseServer
from threading import Event
from threading import Thread

from sanction.adapters import BaseAdapter
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationEndpointMixIn
from sanction.flow import AuthorizationRequestFlow
from sanction.flow import ResourceEndpointMixIn


test_port = 4242 
test_uri = "https://localhost:%d" % test_port

class TestAdapterImpl(BaseAdapter, AuthorizationEndpointMixIn):
    authorization_endpoint = "%s%s" % (test_uri, "/auth")
    token_endpoint = "%s%s" % (test_uri, "/token")
    resource_endpoint = "%s%s" % (test_uri, "/resource")

    def __init__(self, config, flow=None, service=None):
        BaseAdapter.__init__(self, get_config(), flow=flow, service=service)


def get_config():
    config = ConfigParser({}, dict)
    config.read("tests/tests.ini") 

    c = config._sections["sanction"]
    del c["__name__"]

    if "http_debug" in c:
        c["http_debug"] = c["http_debug"] == "true"

    return config._sections["sanction"]


class RequestHandler(BaseHTTPRequestHandler):
    def shutdown(self, param):
        BaseHTTPRequestHandler.shutdown(self)

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_GET(self):
        if self.path == "/resource/me":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(dumps({
                "foo":"bar"
            }))
        else:
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


def start_server():
    e = Event()
    t = Thread(target=spawn_server, args=(e,))
    t.daemon = True
    t.start()
    e.wait()

def spawn_server(e):
    s = TestServer(e)
    s.handle_request()
