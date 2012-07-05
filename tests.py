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


	def test_request_token(self):
		# i don't want to bother mocking an oauth2 server, so i'm just going
		# to test failure cases and rely on manual testing for correct ones

		c = Client()
		try:
			c.request_token({ "error": "something bad happened" })
			self.fail("shouldn't hit here")
		except IOError:
			pass


	def test_facebook_client_credentials(self):
		c = Client(
			token_endpoint="https://graph.facebook.com/oauth/access_token",
			resource_endpoint="https://graph.facebook.com",
			client_id="285809954824916",
			client_secret="d985f6a3ecaffd11d61b3cd026b8753a")

		self.assertEquals(c.access_token, None)
		c.request_token(parser=lambda data: dict(parse_qsl(data)),
			grant_type="client_credentials")
		self.assertIsNotNone(c.access_token)

		data = c.request("/app")
		self.assertEquals(data["name"], "sanction")

	

