from unittest import TestCase
from urlparse import (
	parse_qsl,
	urlparse
)

from sanction.client import Client

auth_endpoint = "http://example.com"
token_endpoint = "http://example.com/token"
resource_endpoint = "http://example.com/resource"
client_id = "client_id"
client_secret = "client_secret"
redirect_uri = "redirect_uri"


class SanctionTests(TestCase):
	def test_init(self):
		c = Client(
			auth_endpoint = auth_endpoint,
			token_endpoint = token_endpoint,
			resource_endpoint = resource_endpoint,
			client_id = client_id,
			client_secret = client_secret,
			redirect_uri = redirect_uri)
		
		self.assertEquals(c.auth_endpoint, auth_endpoint)
		self.assertEquals(c.token_endpoint, token_endpoint)
		self.assertEquals(c.resource_endpoint, resource_endpoint)
		self.assertEquals(c.client_id, client_id)
		self.assertEquals(c.client_secret, client_secret)
		self.assertEquals(c.redirect_uri, redirect_uri)


	def test_get_auth_uri(self):
		c = Client(auth_endpoint = auth_endpoint,
			client_id = client_id)
		uri = c.auth_uri()

		o = urlparse(uri)
		self.assertEquals(o.netloc, "example.com")
		d = dict(parse_qsl(o.query))

		self.assertEquals(d["response_type"], "code")
		self.assertEquals(d["client_id"], client_id)


	def test_auth_received(self):
		# i don't want to bother mocking an oauth2 server, so i'm just going
		# to test failure cases and rely on manual testing for correct ones

		c = Client()
		try:
			c.auth_received('{ "error": "something bad happened" }')
			self.fail("shouldn't hit here")
		except IOError:
			pass
		
	

