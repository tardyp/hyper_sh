import json
import logging
import os
import urlparse

from requests import Session

from dictns import Namespace

from requests_aws4auth import AWS4Auth

try:
    import httplib
except ImportError:
    import http.client as httplib

httplib.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
try:
    import httplib
except ImportError:
    import http.client as httplib

httplib.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class Hyper(Session):
    def __init__(self, config):
        self.config = json.load(open(os.path.expanduser(config)))
        clouds = self.config['clouds'].items()
        if len(clouds) != 1:
            raise RuntimeError("supports only one cloud in config")
        url, self.creds = clouds[0]
        url = urlparse.urlparse(url)
        self.url = "https://" + url.netloc
        Session.__init__(self)
        self.auth = AWS4Auth(self.creds['accesskey'], self.creds['secretkey'], url.netloc.split(".")[0], 'hyper')

    def get(self, *a, **kw):
        r = Session.get(self, *a, **kw)
        r.raise_for_status()
        return Namespace(r.json())

    def list_containers(self):
        return self.get(self.url + "/v1.23/containers/json", verify=False)
