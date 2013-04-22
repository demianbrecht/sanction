# vim: set ts=4 sw=)
""" OAuth 2.0 client librar
"""

from json import loads
from datetime import datetime, timedelta
from time import mktime
try:
    from urllib import urlencode
    from urllib2 import Request, urlopen
    from urlparse import urlsplit, urlunsplit, parse_qsl

    # monkeypatch httpmessage
    from httplib import HTTPMessage
    def get_charset(self):
        try:
            data = filter(lambda s: 'Content-Type' in s, self.headers)[0]
            if 'charset' in data:
                cs = data[data.index(';') + 1:-2].split('=')[1].lower()
                return cs
        except IndexError:
            pass

        return 'utf-8'
    HTTPMessage.get_content_charset = get_charset 
except ImportError:
    from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
    from urllib.request import Request, urlopen


class Client(object):
    """ OAuth 2.0 client object
    """

    def __init__(self, auth_endpoint=None, token_endpoint=None,
        resource_endpoint=None, client_id=None, client_secret=None,
        redirect_uri=None, token_transport=None):
        assert(hasattr(token_transport, '__call__') or 
            token_transport in ('headers', 'query', None))

        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.resource_endpoint = resource_endpoint
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_transport = token_transport or 'query'
        self.token_expires = -1
        self.refresh_token = None

    def auth_uri(self, scope=None, scope_delim=None, state=None, **kwargs):
        """  Builds the auth URI for the authorization endpoint
        """
        scope_delim = scope_delim and scope_delim or ' '
        kwargs.update({
            'client_id': self.client_id,
            'response_type': 'code',
        })

        if scope is not None:
            kwargs['scope'] = scope_delim.join(scope)

        if state is not None:
            kwargs['state'] = state

        if self.redirect_uri is not None:
            kwargs['redirect_uri'] = self.redirect_uri

        return '%s?%s' % (self.auth_endpoint, urlencode(kwargs))

    def request_token(self, parser=None, exclude=None, **kwargs):
        """ Request an access token from the token endpoint.
        This is largely a helper method and expects the client code to
        understand what the server expects. Anything that's passed into
        ``**kwargs`` will be sent (``urlencode``d) to the endpoint. Client
        secret and client ID are automatically included, so are not required
        as kwargs. For example::

            # if requesting access token from auth flow:
            {
                'code': rval_from_auth,
            }

            # if refreshing access token:
            {
                'refresh_token': stored_refresh_token,
                'grant_type': 'refresh_token',
            }

        :param exclude: An iterable of fields to exclude from the ``POST``
                        data. This is useful for fields such as ``redirect_uri``
                        that are required during initial code/token exchange,
                        but will cause errors with some providers when
                        exchanging refresh tokens for new access tokens.
        :param parser: Callback to deal with returned data. Not all providers
                       use JSON.
        """
        kwargs = kwargs and kwargs or {}
        exclude = exclude or {}

        parser = parser and parser or loads
        kwargs.update({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'grant_type' in kwargs and kwargs['grant_type'] or \
                'authorization_code'
        })
        if self.redirect_uri is not None and 'redirect_uri' not in exclude:
            kwargs.update({'redirect_uri': self.redirect_uri})

        msg = urlopen(self.token_endpoint, urlencode(kwargs).encode(
            'utf-8'))
        data = parser(msg.read().decode(msg.info().get_content_charset() or
            'utf-8'))

        for key in data:
            setattr(self, key, data[key])

        # expires_in is RFC-compliant. if anything else is used by the
        # provider, token_expires must be set manually
        if hasattr(self, 'expires_in'):
            self.token_expires = mktime((datetime.utcnow() + timedelta(
                seconds=self.expires_in)).timetuple())

        assert(self.access_token is not None)

    def refresh(self):
        assert self.refresh_token is not None
        self.request_token(refresh_token=self.refresh_token,
            grant_type='refresh_token', exclude=('redirect_uri',))

    def request(self, url, method=None, data=None, parser=None): 
        """ Request user data from the resource endpoint
        :param url: The path to the resource and querystring if required
        :param method: HTTP method. Defaults to ``GET`` unless data is not None
                       in which case it defaults to ``POST``
        :param data: Data to be POSTed to the resource endpoint
        :param parser: Parser callback to deal with the returned data. Defaults
                       to ``json.loads`.`
        """
        assert(self.access_token is not None)
        parser = parser or loads

        if not method:
            method = 'GET' if not data else 'POST'

        if not hasattr(self.token_transport, '__call__'):
            transport = globals()['_transport_{}'.format(self.token_transport)]
        else:
            transport = self.token_transport

        req = transport('{}{}'.format(self.resource_endpoint, 
            url), self.access_token, data=data, method=method)

        resp = urlopen(req)
        data = resp.read()
        try:
            # try to decode it first using either the content charset, falling
            # back to utf8
            return parser(data.decode(resp.info().get_content_charset() or
                'utf-8'))
        except UnicodeDecodeError:
            # if we've gotten a decoder error, the calling code better know how
            # to deal with it. some providers (i.e. stackexchange) like to gzip
            # their responses, so this allows the client code to handle it
            # directly.
            return parser(data)

def _transport_headers(url, access_token, data=None, method=None):
    try:
        req = Request(url, data=data, method=method)
    except TypeError:
        req = Request(url, data=data)
        req.get_method = lambda: method

    req.headers.update({
        'Authorization': 'Bearer {}'.format(access_token)
    })
    return req

def _transport_query(url, access_token, data=None, method=None):
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    query.update({
        'access_token': access_token
    })
    url = urlunsplit((parts.scheme, parts.netloc, parts.path,
        urlencode(query), parts.fragment))
    try:
        req = Request(url, data=data, method=method)
    except TypeError:
        req = Request(url, data=data)
        req.get_method = lambda: method
    return req
