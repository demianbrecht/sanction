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

    def fetch(self, con, uri, method="GET", body=None, headers={}):
        con.request(method, uri, body, headers)
        r = con.getresponse()

        if r.status != 200:
            raise InvalidHTTPStatusError(r.status, r.reason)

        return r.read()


class HTTPSService(BaseService, HTTPRequestMixIn):

    def request(self, uri, method="GET", body=None, headers={}):
        o = urlparse(uri)
        assert(str(o.scheme) == "https")

        c = HTTPSConnection(o.netloc)
        c.set_debuglevel(1)

        uri = "%s?%s" % (o.path, o.query) if o.query != "" else o.path
        if len(o.query) is None:
            uri = o.path
        data = self.fetch(c, uri, method, body, 
            headers)

        c.close()
        return data

