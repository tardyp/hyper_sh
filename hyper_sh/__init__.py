from __future__ import print_function

import json
import os

from docker import Client as DockerClient

from .requests_aws4auth import AWS4Auth

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


DEFAULT_CONFIG_FILE = "~/.hyper/config.json"


class Client(DockerClient):
    @staticmethod
    def guess_config():
        default_config_file = os.path.expanduser(DEFAULT_CONFIG_FILE)
        if os.path.exists(default_config_file):
            config = default_config_file
        elif ('hyper_accesskey' in os.environ and 'hyper_secretkey' in os.environ and
              'hyper_endpoint' in os.environ):
            config = {
                'clouds': {
                    os.environ['hyper_endpoint']: {
                        "accesskey": os.environ['hyper_accesskey'],
                        "secretkey": os.environ['hyper_secretkey']
                    }
                }
            }
        else:
            raise RuntimeError("unable to guess config from default file or environment")
        return config

    def __init__(self, config=None):
        if config is None:
            config = self.guess_config()
        if isinstance(config, str):
            self.config = json.load(open(os.path.expanduser(config)))
        else:
            self.config = config
        clouds = list(self.config['clouds'].items())
        if len(clouds) != 1:
            raise RuntimeError("supports only one cloud in config")
        url, self.creds = clouds[0]
        url = urlparse(url)
        base_url = "https://" + url.netloc
        DockerClient.__init__(self, base_url, tls=True)
        self.auth = AWS4Auth(self.creds['accesskey'], self.creds['secretkey'], url.netloc.split(".")[0],
                             'hyper')
        self._version = "1.23"
