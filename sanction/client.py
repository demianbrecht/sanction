from json import loads
from urllib import urlencode
from urllib2 import urlopen
from urlparse import parse_qsl

class Client(object):

	def __init__(self, auth_endpoint=None, token_endpoint=None,
			resource_endpoint=None, client_id=None, client_secret=None,
			redirect_uri=None, access_token_key=None):
		self.auth_endpoint = auth_endpoint
		self.token_endpoint = token_endpoint
		self.resource_endpoint = resource_endpoint
		self.redirect_uri = redirect_uri
		self.access_token_key = access_token_key and access_token_key or\
			"access_token"
		self.client_id = client_id
		self.client_secret = client_secret


	def get_auth_uri(self, scope=None, scope_delim=None, state=None,
		response_type=None, **kwargs):
		scope_delim = scope_delim and scope_delim or " "
		o = {
			"response_type": response_type and response_type or "code",
			"client_id": self.client_id,
		}
		if scope is not None: o["scope"] = scope_delim.join(scope)
		if state is not None: o["state"] = state
		if self.redirect_uri is not None: o["redirect_uri"] = self.redirect_uri
		for kw in kwargs:
			assert(kw not in o)
			o[kw] = kwargs[kw]

		return "%s?%s" % (self.auth_endpoint, urlencode(o))


	def auth_received(self, qs):
		o = _parse_rval(qs)
		if o.has_key("error"):
			raise IOError(o["error"])
		else:
			self.get_access_token(o["code"], self.client_id,
				self.client_secret)


	def get_access_token(self, code, client_id, client_secret, 
		grant_type=None): 
		o = {
			"code": code,
			"client_id": client_id,
			"client_secret": client_secret,
			"grant_type": grant_type and grant_type or "authorization_code"
		}
		if self.redirect_uri is not None: 
			o["redirect_uri"] = self.redirect_uri

		h = urlopen(self.token_endpoint, urlencode(o))
		r = _parse_rval(h.read())
		self.access_token = r["access_token"]

		keys = filter(lambda a: a in r, ("expires", "expires_in"))
		expires_key = len(keys) > 0 and keys[0] or None
		if expires_key is not None:
			self.expires_in = r[expires_key]

		self.token_type = r.get("token_type", None)


	def request(self, path, qs=None, data=None):
		assert(self.access_token is not None)
		if qs is None: qs = {}
		qs.update({
			self.access_token_key: self.access_token
		})
		path = "%s%s?%s" % (self.resource_endpoint, path, urlencode(qs))
		h = urlopen(path, data)
		return loads(h.read())


def _parse_rval(data):
	if isinstance(data, basestring):
		try:
			return loads(data)
		except:
			return dict(parse_qsl(data))
	return data

