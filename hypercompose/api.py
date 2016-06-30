import json
import os
import pprint
import urlparse

from docker import Client

from .requests_aws4auth import AWS4Auth


class Hyper(Client):
    def __init__(self, config):
        self.config = json.load(open(os.path.expanduser(config)))
        clouds = self.config['clouds'].items()
        if len(clouds) != 1:
            raise RuntimeError("supports only one cloud in config")
        url, self.creds = clouds[0]
        url = urlparse.urlparse(url)
        base_url = "https://" + url.netloc
        Client.__init__(self, base_url, tls=True)
        self.auth = AWS4Auth(self.creds['accesskey'], self.creds['secretkey'],
                             url.netloc.split(".")[0], 'hyper')
        self._version = "1.23"

    def create_network(*arg, **kw):
        #ignore network creation
        pass

    # hack to log the requests
    def _set_request_timeout(self, kwargs):
        """Prepare the kwargs for an HTTP request by inserting the timeout
        parameter, if not already present."""
        pprint.pprint(kwargs)
        kwargs.setdefault('timeout', self.timeout)
        return kwargs
