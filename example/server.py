#!/usr/bin/env python
# vim: set ts=4 sw=4 et:

import logging
import sys, os

try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    from ConfigParser import ConfigParser
    from urlparse import urlparse, parse_qsl
    from urllib import urlencode
    from StringIO import StringIO
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from configparser import ConfigParser
    from urllib.parse import urlparse, parse_qsl, urlencode
    from io import StringIO

from gzip import GzipFile
from json import loads

# so we can run without installing
sys.path.append(os.path.abspath('../'))

from sanction.client import Client

ENCODING_UTF8 = 'utf-8'

def get_config():
    config = ConfigParser({}, dict)
    config.read('example.ini') 

    c = config._sections['sanction']
    if '__name__' in c:
        del c['__name__']

    if 'http_debug' in c:
        c['http_debug'] = c['http_debug'] == 'true'

    return config._sections['sanction']


logging.basicConfig(format='%(message)s')
l = logging.getLogger(__name__)
config = get_config()


class Handler(BaseHTTPRequestHandler):
    route_handlers = {
        '/': 'handle_root',
        '/login/google': 'handle_google_login',
        '/oauth2/google': 'handle_google',
        '/login/facebook': 'handle_facebook_login',
        '/oauth2/facebook': 'handle_facebook',
        '/login/foursquare': 'handle_foursquare_login',
        '/oauth2/foursquare': 'handle_foursquare',
        '/login/bitly': 'handle_bitly_login',
        '/oauth2/bitly': 'handle_bitly',
        '/login/github': 'handle_github_login',
        '/oauth2/github': 'handle_github',
        '/login/instagram': 'handle_instagram_login',
        '/oauth2/instagram': 'handle_instagram',
        '/login/stackexchange': 'handle_stackexchange_login',
        '/oauth2/stackexchange': 'handle_stackexchange',
        '/login/deviantart': 'handle_deviantart_login',
        '/oauth2/deviantart': 'handle_deviantart',
    }

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in self.route_handlers:
            getattr(self, self.route_handlers[url.path])(
            dict(parse_qsl(url.query)))
        else:
            self.send_response(404)

    def success(func):
        def wrapper(self, *args, **kwargs):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.log_message(self.path)
            self.end_headers()
            return func(self, *args, **kwargs)
        return wrapper

    @success
    def handle_root(self, data):
        self.wfile.write('''
            login with: <a href='/oauth2/google'>Google</a>,
            <a href='/oauth2/facebook'>Facebook</a>,
            <a href='/oauth2/github'>GitHub</a>,
            <a href='/oauth2/stackexchange'>Stack Exchange</a>,
            <a href='/oauth2/instagram'>Instagram</a>,
            <a href='/oauth2/foursquare'>Foursquare</a>,
            <a href='/oauth2/bitly'>Bitly</a>,
            <a href='/oauth2/deviantart'>Deviant Art</a>,
        '''.encode(ENCODING_UTF8))


    def handle_stackexchange(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://stackexchange.com/oauth',
            client_id=config['stackexchange.client_id'],
            redirect_uri='http://localhost/login/stackexchange')
        self.send_header('Location', c.auth_uri())
        self.end_headers()


    def __gunzip(self, data):
        s = StringIO(data)
        gz = GzipFile(fileobj=s, mode='rb')
        return gz.read()


    @success
    def handle_stackexchange_login(self, data):
        c = Client(token_endpoint='https://stackexchange.com/oauth/access_token',
            resource_endpoint='https://api.stackexchange.com/2.0',
            redirect_uri='http://localhost/login/stackexchange',
            client_id=config['stackexchange.client_id'],
            client_secret=config['stackexchange.client_secret'])

        c.request_token(code=data['code'],
            parser = lambda data: dict(parse_qsl(data)))

        self.dump_client(c)
        data = c.request('/me', qs={
            'site': 'stackoverflow.com',
            'key': config['stackexchange.key']
            }, parser=lambda c: loads(self.__gunzip(c)))['items'][0]

        self.dump_response(data)

        
    def dump_response(self, data):
        for k in data:
            self.wfile.write('{0}: {1}<br>'.format(k,
                data[k]).encode(ENCODING_UTF8))


    def dump_client(self, c):
        for k in c.__dict__:
            self.wfile.write('{0}: {1}<br>'.format(k,
                c.__dict__[k]).encode(ENCODING_UTF8))
        self.wfile.write('<hr/>'.encode(ENCODING_UTF8))

    def handle_google(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://accounts.google.com/o/oauth2/auth',
            client_id=config['google.client_id'],
            redirect_uri='http://localhost/login/google')
        self.send_header('Location', c.auth_uri(
            scope=config['google.scope'].split(','), access_type='offline'))    
        self.end_headers()


    @success
    def handle_google_login(self, data):
        c = Client(token_endpoint='https://accounts.google.com/o/oauth2/token',
            resource_endpoint='https://www.googleapis.com/oauth2/v1',
            redirect_uri='http://localhost/login/google',
            client_id=config['google.client_id'],
            client_secret=config['google.client_secret'])
        c.request_token(code=data['code'])

        self.dump_client(c)
        data = c.request('/userinfo')
        self.dump_response(data)

        if hasattr(c, 'refresh_token'):
            rc = Client(token_endpoint=c.token_endpoint,
                client_id=c.client_id,
                client_secret=c.client_secret,
                resource_endpoint=c.resource_endpoint)

            rc.request_token(grant_type='refresh_token', 
                refresh_token=c.refresh_token)
            self.wfile.write('<p>post refresh token:</p>'.encode(ENCODING_UTF8))
            self.dump_client(rc)

        
    def handle_facebook(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://www.facebook.com/dialog/oauth',
                client_id=config['facebook.client_id'],
                redirect_uri='http://localhost/login/facebook')
        self.send_header('Location', c.auth_uri(
            scope=config['facebook.scope'].split(','),
            scope_delim=','))
        self.end_headers()

    @success
    def handle_facebook_login(self, data):
        c = Client(
            token_endpoint='https://graph.facebook.com/oauth/access_token',
            resource_endpoint='https://graph.facebook.com',
            redirect_uri='http://localhost/login/facebook',
            client_id=config['facebook.client_id'],
            client_secret=config['facebook.client_secret'])

        c.request_token(code=data['code'],
            parser=lambda data: dict(parse_qsl(data)))

        self.dump_client(c)
        d = c.request('/me')
        self.dump_response(d)

        try:
            d = c.request('/me/feed', data=urlencode({
                'message': 'test post from py-sanction'
            }))
            self.wfile.write(
                'I posted a message to your wall (in sandbox mode, nobody '
                'else will see it)'.encode(ENCODING_UTF8))
        except:
            self.wfile.write(
                'Unable to post to your wall')


    def handle_foursquare(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://foursquare.com/oauth2/authenticate',
                client_id=config['foursquare.client_id'],
                redirect_uri='http://localhost/login/foursquare')
        self.send_header('Location', c.auth_uri())
        self.end_headers()


    @success
    def handle_foursquare_login(self, data):
        c = Client(
            token_endpoint='https://foursquare.com/oauth2/access_token',
            resource_endpoint='https://api.foursquare.com/v2',
            redirect_uri='http://localhost/login/foursquare',
            client_id=config['foursquare.client_id'],
            client_secret=config['foursquare.client_secret'],
            )
        c.access_token_key = 'oauth_token'
        c.request_token(code=data['code'])

        self.dump_client(c)
        d = c.request('/users/24700343')
        self.dump_response(d)


    def handle_bitly(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://bitly.com/oauth/authorize',
                client_id=config['bitly.client_id'],
                redirect_uri='http://localhost/login/bitly')
        self.send_header('Location', c.auth_uri())
        self.end_headers()


    @success
    def handle_bitly_login(self, data):
        c = Client(token_endpoint='https://api-ssl.bitly.com/oauth/access_token',
            resource_endpoint='https://api-ssl.bitly.com',
            redirect_uri='http://localhost/login/bitly',
            client_id=config['bitly.client_id'],
            client_secret=config['bitly.client_secret'])
        c.request_token(code=data['code'],
            parser=lambda data: dict(parse_qsl(data)))

        self.dump_client(c)
        data = c.request('/v3/user/info')['data']
        self.dump_response(data)


    def handle_github(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://github.com/login/oauth/authorize',
                client_id=config['github.client_id'],
                redirect_uri='http://localhost/login/github')
        self.send_header('Location', c.auth_uri())
        self.end_headers()


    @success
    def handle_github_login(self, data):
        c = Client(token_endpoint='https://github.com/login/oauth/access_token',
            resource_endpoint='https://api.github.com',
            redirect_uri='http://localhost/login/github',
            client_id=config['github.client_id'],
            client_secret=config['github.client_secret'])
        c.request_token(code=data['code'],
            parser=lambda data: dict(parse_qsl(data)))

        self.dump_client(c)
        data = c.request('/user')
        self.dump_response(data)


    def handle_instagram(self, data):
        self.send_response(302)
        c = Client(auth_endpoint='https://api.instagram.com/oauth/authorize/',
                client_id=config['instagram.client_id'],
                redirect_uri='http://localhost/login/instagram')
        self.send_header('Location', c.auth_uri())
        self.end_headers()


    @success
    def handle_instagram_login(self, data):
        c = Client(token_endpoint='https://api.instagram.com/oauth/access_token',
            resource_endpoint='https://api.instagram.com/v1',
            redirect_uri='http://localhost/login/instagram',
            client_id=config['instagram.client_id'],
            client_secret=config['instagram.client_secret'])
        c.request_token(code=data['code'])

        self.dump_client(c)
        data = c.request('/users/self')['data']
        self.dump_response(data)


    def handle_deviantart(self, data):
        self.send_response(302)
        c = Client(
            auth_endpoint='https://www.deviantart.com/oauth2/draft15/authorize',
            client_id=config['deviantart.client_id'],
            redirect_uri=config['deviantart.redirect_uri'])
        self.send_header('Location', c.auth_uri())
        self.end_headers()


    @success
    def handle_deviantart_login(self, data):
        c = Client(
            token_endpoint='https://www.deviantart.com/oauth2/draft15/token',
            resource_endpoint='https://www.deviantart.com/api/draft15',
            redirect_uri=config['deviantart.redirect_uri'],
            client_id=config['deviantart.client_id'],
            client_secret=config['deviantart.client_secret'])
        c.request_token(code=data['code'])

        self.dump_client(c)
        data = c.request('/user/whoami')
        self.dump_response(data)


if __name__ == '__main__':
    l.setLevel(1)
    server_address = ('', 80)
    server = HTTPServer(server_address, Handler)
    l.info('Starting server on %sport %s \nPress <ctrl>+c to exit' % server_address)
    server.serve_forever()

