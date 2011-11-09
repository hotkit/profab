"""Profab helps to manage servers on EC2.

"""
from simplejson import loads
import logging
import os


_logger = logging.getLogger('profab')


class Configuration(object):
    """Fetch a client configuration.
    """

    def __init__(self, client):
        """Load the configuration for the specified client.
        """
        # Set up the default configuration
        self.client = client
        self.host = 'ec2'
        self.region = 'us-east-1'
        self.keys = _Keys(api = 'test-api-key',
            secret = 'test-api-secret')
        self.ssh = _Keys(ubuntu=[])
        # Load overrides from a file and merge them with this object
        overrides = self.load_configuration()
        _merge_attrs(self, overrides)
        # Ensure that the running user's public key is on the server
        pub_key_file =  os.path.expanduser('~/.ssh/id_rsa.pub')
        pub_key = file(pub_key_file).readline()[:-1]
        if pub_key not in self.ssh.ubuntu:
            self.ssh.ubuntu.append(pub_key)

    def load_configuration(self):
        """Load the configuration from the default file for the customer.
        """
        pathname = os.path.expanduser('~/.profab/%s/ec2.json' % self.client)
        try:
            content = file(pathname).read()
        except IOError:
            _logger.error("No configuration file found at %s. "
                "Defaulting to empty configuration. "
                "This will probably lead to authentication failures.", pathname)
            content = "{}"
        return loads(content)


class _Keys(object):
    """Used for storage of keys.
    """

    def __init__(self, **kwargs):
        """Load the specified key values.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)


def _merge_attrs(host, attrs):
    """Sets attributes on an object based on values found in a dict in
    a nested manner.
    """
    for k, v in attrs.items():
        if hasattr(v, 'items'):
            if not hasattr(host, k):
                setattr(host, k, _Keys(**v))
            else:
                _merge_attrs(getattr(host, k), v)
        else:
            setattr(host, k, v)
