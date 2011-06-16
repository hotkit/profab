

class _Configuration(object):
    """Fetch a client configuration.
    """

    def __init__(self, client):
        """Load the configuration for the specified client.
        """
        # Set up the default configuration
        self.client = client
        self.host = 'ec2'
        self.keys = _Keys(api = 'test-api-key',
            secret = 'test-api-secret')
        overrides = self.load_configuration()
        _merge_attrs(self, overrides)

    def load_configuration(self):
        return {}


class _Keys(object):
    """Used for storage of keys.
    """

    def __init__(self, **kwargs):
        """Load the specified key values.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)


def _merge_attrs(host, attrs):
    for k, v in attrs.items():
        if hasattr(v, 'items'):
            if not hasattr(host, k):
                setattr(host, k, _Keys(**v))
            else:
                _merge_attrs(getattr(host, k), v)
        else:
            setattr(host, k, v)
