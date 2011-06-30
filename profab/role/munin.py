"""Sets up and configures Munin on the machine
"""
from profab.role import Role


class AddRole(Role):
    """Adds the default Munin configuration.
    """
    packages = ['apache2', 'munin', 'munin-plugins-extra']


class Configure(Role):
    """Adds a Munin node to a server.
    """
    packages = [ 'munin-node', 'munin-plugins-extra']

