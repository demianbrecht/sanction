from abc import ABCMeta
from abc import abstractmethod
from httplib import HTTPConnection
from httplib import HTTPSConnection
from logging import getLogger
from urlparse import urlparse

from sanction.exceptions import InvalidHTTPStatusError

log = getLogger(__name__)

class BaseService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def request(self, uri): pass #pragma: no cover


class HTTPRequestMixIn(object):

    def fetch(self, con, uri, method=None, body=None, headers=None):
        con.request(method or "GET", uri, body, headers or {})
        r = con.getresponse()

        if r.status != 200:
            raise InvalidHTTPStatusError(r.status, r.reason)

        return r.read()


class HTTPSService(BaseService, HTTPRequestMixIn):

    def request(self, uri, method=None, body=None, headers=None):
        o = urlparse(uri)
        assert(str(o.scheme) == "https")

        c = HTTPSConnection(o.netloc)

        uri = "%s?%s" % (o.path, o.query) if o.query != "" else o.path
        if len(o.query) == 0:
            uri = o.path
        data = self.fetch(c, uri, method, body, 
            headers or {})

        c.close()
        return data

