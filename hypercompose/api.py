import json
import os
import urlparse

from docker import Client

from requests_aws4auth import AWS4Auth

AWS4Auth.default_include_headers = ['host', 'content-type', 'date', 'x-hyper-*']
AWS4Auth.SECURITY_TOKEN_HEADER = 'x-hyper-security-token'
AWS4Auth.DATE_HEADER = 'x-hyper-date'
AWS4Auth.CONTENT_SHA256_HEADER = 'x-hyper-content-sha256'
AWS4Auth.CLIENT_CONTEXT_HEADER = 'x-hyper-client-context'
AWS4Auth.HEADER_PREFIX = 'x-hyper-'
AWS4Auth.SCOPE_SUFFIX = 'hyper_request'
AWS4Auth.KEY_PREFIX = 'HYPER'
AWS4Auth.AUTH_PREFIX = 'HYPER-HMAC-SHA256'
old_cano_path = AWS4Auth.amz_cano_path
AWS4Auth.amz_cano_path = lambda self, path: old_cano_path(self, path[1:])


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
        self._auth_configs['HttpHeaders'] = {'content-type': 'application/json'}

    def create_network(*arg, **kw):
        #ignore network creation
        pass
