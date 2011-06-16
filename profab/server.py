from profab import _Configuration, _logger


class Server(object):
    """Represents a server. Do not construct these instances directly,
    use one of the methods `start` or `connect`.
    """

    @classmethod
    def start(kls, client, *roles, **conections):
        """Start a server for the specified client with the given roles
        and connect the requested services.
        """
        config = _Configuration(client)
        _logger.info("New server for %s on %s with roles %s",
            config.client, config.host, roles)


    @classmethod
    def connect(kls, hostname):
        """Connect to a given server by the provided hostname.
        """
        pass

