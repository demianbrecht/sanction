#!/usr/bin/env python

import logging

from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from ConfigParser import ConfigParser
from urlparse import urlparse
from urllib import urlencode
from urlparse import parse_qsl
from StringIO import StringIO
from gzip import GzipFile
from urllib import quote_plus

from sanction.client import Client

def get_config():
	config = ConfigParser({}, dict)
	config.read("example.ini") 

	c = config._sections["sanction"]
	del c["__name__"]

	if "http_debug" in c:
		c["http_debug"] = c["http_debug"] == "true"

	return config._sections["sanction"]


logging.basicConfig(format="%(message)s")
l = logging.getLogger(__name__)
config = get_config()


class Handler(BaseHTTPRequestHandler):
	route_handlers = {
		"/": "handle_root",
		"/login/google": "handle_google_login",
		"/oauth2/google": "handle_google",
		"/login/facebook": "handle_facebook_login",
		"/oauth2/facebook": "handle_facebook",
		"/login/foursquare": "handle_foursquare_login",
		"/oauth2/foursquare": "handle_foursquare",
		"/login/bitly": "handle_bitly_login",
		"/oauth2/bitly": "handle_bitly",
	}

	def do_GET(self):
		url = urlparse(self.path)
		if url.path in self.route_handlers:
			getattr(self, self.route_handlers[url.path])(
			dict(parse_qsl(url.query)))
		else:
			self.send_response(404)


	def handle_root(self, data):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write('''
			login with: <a href="/oauth2/google">Google</a>,
			<a href="/oauth2/facebook">Facebook</a>,
			<a href="/oauth2/foursquare">Foursquare</a>,
			<a href="/oauth2/bitly">Bitly</a>
		''')


	def handle_google(self, data):
		self.send_response(302)
		c = Client(auth_endpoint="https://accounts.google.com/o/oauth2/auth",
			client_id=config["google.client_id"],
			redirect_uri="http://localhost:8080/login/google")
		self.send_header("Location", c.auth_uri(
			scope=config["google.scope"].split(",")))	
		self.end_headers()


	def handle_google_login(self, data):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.log_message(self.path)
		self.end_headers()

		c = Client(token_endpoint="https://accounts.google.com/o/oauth2/token",
			resource_endpoint="https://www.googleapis.com/oauth2/v1",
			redirect_uri="http://localhost:8080/login/google",
			client_id=config["google.client_id"],
			client_secret=config["google.client_secret"])
		c.request_token(data=data)

		self.wfile.write("Access token: %s<br>" % c.access_token)

		data = c.request("/userinfo")
		self.wfile.write("First name: %s<br>" % data["name"])
		self.wfile.write("Last name: %s<br>" % data["family_name"])
		self.wfile.write("Email: %s<br>" % data["email"])

		
	def handle_facebook(self, data):
		self.send_response(302)
		c = Client(auth_endpoint="https://www.facebook.com/dialog/oauth",
				client_id=config["facebook.client_id"],
				redirect_uri="http://localhost:8080/login/facebook")
		self.send_header("Location", c.auth_uri(
			scope=config["facebook.scope"].split(","),
			scope_delim=","))
		self.end_headers()


	def handle_facebook_login(self, data):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.log_message(self.path)
		self.end_headers()

		c = Client(
			token_endpoint="https://graph.facebook.com/oauth/access_token",
			resource_endpoint="https://graph.facebook.com",
			redirect_uri="http://localhost:8080/login/facebook",
			client_id=config["facebook.client_id"],
			client_secret=config["facebook.client_secret"])
		c.request_token(data=data, 
			parser = lambda data: dict(parse_qsl(data)))

		d = c.request("/me")

		self.wfile.write("Access token: %s<br>" % c.access_token)
		self.wfile.write("First name: %s<br>" % d["first_name"])
		self.wfile.write("Last name: %s<br>" % d["last_name"])
		self.wfile.write("Email: %s<br>" % d["email"])

		# to see a wall post in action, uncomment this
		try:
			d = c.request("/me/feed", data=urlencode({
				"message": "test post from py-sanction"
			}))
			self.wfile.write(
				"I posted a message to your wall (in sandbox mode, nobody else will see it)")
		except:
			self.wfile.write(
				"Unable to post to your wall")

	def handle_foursquare(self, data):
		self.send_response(302)
		c = Client(auth_endpoint="https://foursquare.com/oauth2/authenticate",
				client_id=config["foursquare.client_id"],
				redirect_uri="http://localhost:8080/login/foursquare")
		self.send_header("Location", c.auth_uri())
		self.end_headers()


	def handle_foursquare_login(self, data):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.log_message(self.path)
		self.end_headers()

		c = Client(
			token_endpoint="https://foursquare.com/oauth2/access_token",
			resource_endpoint="https://api.foursquare.com/v2",
			redirect_uri="http://localhost:8080/login/foursquare",
			client_id=config["foursquare.client_id"],
			client_secret=config["foursquare.client_secret"],
			)
		c.access_token_key = "oauth_token"
		c.request_token(data=data)

		d = c.request("/users/24700343")

		self.wfile.write("Access token: %s<br>" % c.access_token)
		self.wfile.write("First name: %s<br>" % 
			d["response"]["user"]["firstName"])
		self.wfile.write("Last name: %s<br>" % 
			d["response"]["user"]["lastName"])
		self.wfile.write("Email: %s<br>" % 
			d["response"]["user"]["contact"]["email"])


	def handle_bitly(self, data):
		self.send_response(302)
		c = Client(auth_endpoint="https://bitly.com/oauth/authorize",
				client_id=config["bitly.client_id"],
				redirect_uri="http://localhost:8080/login/bitly")
		self.send_header("Location", c.auth_uri())
		self.end_headers()


	def handle_bitly_login(self, data):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.log_message(self.path)
		self.end_headers()

		c = Client(token_endpoint="https://api-ssl.bitly.com/oauth/access_token",
			resource_endpoint="https://api-ssl.bitly.com",
			redirect_uri="http://localhost:8080/login/bitly",
			client_id=config["bitly.client_id"],
			client_secret=config["bitly.client_secret"])
		c.request_token(data=data,
			parser = lambda data: dict(parse_qsl(data)))

		self.wfile.write("Access token: %s<br>" % c.access_token)

		data = c.request("/v3/user/info")["data"]
		self.wfile.write("Full name: %s<br>" % data["full_name"])
		self.wfile.write("Member since: %s<br>" % data["member_since"])


def main(): 
	l.setLevel(1)
	server = HTTPServer(("", 8080), Handler)
	l.info("starting server. press <ctrl>+c to exit")
	server.serve_forever()

if __name__=="__main__":
	main()

