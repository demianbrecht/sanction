# vim: set ts=4 sw=4 et:
import json
import zlib

from functools import wraps
from unittest import TestCase
from uuid import uuid4
try:
    from urlparse import parse_qsl, urlparse
except ImportError:
    from urllib.parse import parse_qsl, urlparse

from mock import patch

from sanction import Client, transport_headers
from sanction.test import with_patched_client

AUTH_ENDPOINT = "http://example.com"
TOKEN_ENDPOINT = "http://example.com/token"
RESOURCE_ENDPOINT = "http://example.com/resource"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
REDIRECT_URI = "redirect_uri"
SCOPE = 'foo,bar'
STATE = str(uuid4())
ACCESS_TOKEN = 'access_token'



class TestClient(TestCase):
    def setUp(self):
        self.client = Client(auth_endpoint=AUTH_ENDPOINT,
            token_endpoint=TOKEN_ENDPOINT,
            resource_endpoint=RESOURCE_ENDPOINT,
            client_id=CLIENT_ID)

    def test_init(self):
        map(lambda c: self.assertEqual(*c),
            ((self.client.auth_endpoint, AUTH_ENDPOINT),
            (self.client.token_endpoint, TOKEN_ENDPOINT),
            (self.client.resource_endpoint, RESOURCE_ENDPOINT),
            (self.client.client_id, CLIENT_ID),))

    def test_auth_uri(self):
        parsed = urlparse(self.client.auth_uri(redirect_uri=REDIRECT_URI))
        qs = dict(parse_qsl(parsed.query))

        map(lambda c: self.assertEqual(*c),
            ((qs['redirect_uri'], REDIRECT_URI),
            (qs['response_type'], 'code'),
            (qs['client_id'], CLIENT_ID)))

        parsed = urlparse(self.client.auth_uri(scope=SCOPE))
        qs = dict(parse_qsl(parsed.query))

        self.assertEqual(qs['scope'], SCOPE)

        parsed = urlparse(self.client.auth_uri(state=STATE))
        qs = dict(parse_qsl(parsed.query))

        self.assertEqual(qs['state'], STATE)

    @with_patched_client(json.dumps({
        'access_token':'test_token',
        'expires_in': 300,
    }))
    def test_request_token_json(self):
        self.client.request_token()
        self.assertEqual(self.client.access_token, 'test_token')

        self.client.request_token(redirect_uri=REDIRECT_URI)
        self.assertEqual(self.client.access_token, 'test_token')

    @with_patched_client('access_token=test_token')
    def test_request_token_url(self):
        self.client.request_token()
        self.assertEqual(self.client.access_token, 'test_token')

    @with_patched_client(json.dumps({
        'access_token': 'refreshed_token',
    }))
    def test_refresh_token(self):
        self.client.refresh_token = 'refresh_token'
        self.client.refresh()
        self.assertEqual(self.client.access_token, 'refreshed_token')

    @with_patched_client(json.dumps({
        'userid': 1234
    }))
    def test_request(self):
        self.client.access_token = 'foo'
        data = self.client.request('/foo')
        self.assertEqual(data['userid'], 1234)

    @with_patched_client(zlib.compress(json.dumps({
        'userid': 1234
    }).encode('utf8')))
    def test_request_custom_parser(self):
        def _decompress(buf):
            return json.loads(zlib.decompress(buf).decode())

        self.client.access_token = 'foo'
        data = self.client.request('/foo', parser=_decompress)
        self.assertEqual(data['userid'], 1234)

    @with_patched_client(json.dumps({
        'userid': 1234
    }))
    def test_request_transport_headers(self):
        self.client.token_transport = transport_headers 
        self.client.access_token = 'foo'
        data = self.client.request('/foo')
        self.assertEqual(data['userid'], 1234)

    @with_patched_client(json.dumps({
        'userid': 1234
    }), headers={
        'Content-Type': 'text/html; charset=utf-8',
    })
    def test_request_with_charset(self):
        self.client.access_token = 'foo'
        data = self.client.request('/foo')
        self.assertEqual(data['userid'], 1234)

    @with_patched_client(json.dumps({
        'userid': 1234
    }))
    def test_custom_transport(self):
        def _transport(url, access_token, data=None, method=None,
            headers=None):

            self.assertEqual(url, 'http://example.com/resource/foo')
            self.assertEqual(access_token, 'foo')

        self.client.access_token = 'foo'
        self.client.token_transport = _transport
        data = self.client.request('/foo', headers={
            'Content-Type': 'application/json'})

        self.assertEqual(data['userid'], 1234)

    @with_patched_client(json.dumps({
        'userid': 1234
    }))
    def test_query_transport_with_headers(self):
        self.client.access_token = 'foo'
        data = self.client.request('/foo', headers={'Content-Type':
            'application/json'})

        self.assertEqual(data['userid'], 1234)

    @with_patched_client(json.dumps({
        'userid': 1234
    }))
    def test_header_transport_with_headers(self):
        self.client.access_token = 'foo'
        self.client.token_transport = transport_headers 
        data = self.client.request('/foo', headers={'Content-Type':
            'application/json'})

        self.assertEqual(data['userid'], 1234)
