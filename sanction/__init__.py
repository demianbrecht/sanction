from json import loads
from urllib import (
	urlencode,
)
from urlparse import parse_qsl

def get_authorization_uri(uri, client_id, scope=None, scope_delim=" ", state=None,
	redirect_uri=None, response_type=None, **kwargs):
	o = {
		"response_type": response_type is None and "code" or response_type,
		"client_id": client_id,
	}
	if scope is not None: o["scope"] = scope_delim.join(scope)
	if state is not None: o["state"] = state
	if redirect_uri is not None: o["redirect_uri"] = redirect_uri
	for kw in kwargs:
		assert(kw not in o)
		o[kw] = kwargs[kw]

	return "%s?%s" % (uri, urlencode(o))


def get_access_token(uri, client_id, client_secret, code, redirect_uri=None,
	grant_type=None): 
	o = {
		"client_id": client_id,
		"client_secret": client_secret,
		"code": code,
		"grant_type": grant_type and grant_type or "authorization_code"
	}
	if redirect_uri is not None: o["redirect_uri"] = redirect_uri

	r = parse_rval(urlopen(uri, o).read())
	import pdb; pdb.set_trace()


def parse_rval(data):
	try:
		return loads(data)
	except:
		return dict(parse_qsl(data))

