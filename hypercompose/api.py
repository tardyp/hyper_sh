import json
import os
import urlparse

from docker import Client

from .requests_aws4auth import AWS4Auth


class Hyper(Client):
    def __init__(self, config):
        if isinstance(config, basestring):
            self.config = json.load(open(os.path.expanduser(config)))
        else:
            self.config = config
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
