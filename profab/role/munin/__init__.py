"""Sets up and configures Munin on the machine
"""
from cStringIO import StringIO

from fabric.api import settings, sudo
from fabric.contrib.files import exists
from fabric.operations import put

from profab import _logger
from profab.role import Role
from profab.role.munin.templates import APACHE_CONFIG, MUNIN_CONFIG


def _template(config):
    f = StringIO()
    f.write(config)
    return f


class AddRole(Role):
    """Adds the default Munin configuration.
    """
    packages = ['apache2', 'munin', 'munin-plugins-extra']
    
    def configure(self):
        """Adds the Munin web site to Apache.
        """
        if exists("/etc/apache2/sites-enabled/000-default"):
            _logger.warning("Removing Apache2 default site")
            sudo("a2dissite 000-default")

        _logger.info("Replace the Munin configuration file")
        put(_template(MUNIN_CONFIG), "/etc/munin/munin.conf",
            use_sudo=True)
        
        _logger.info("Configure Apache2 for Munin")
        put(_template(APACHE_CONFIG),
            "/etc/apache2/sites-available/munin.conf", use_sudo=True)
        sudo('a2ensite munin.conf')

        _logger.info("Finally we can restart Apache")
        sudo('service apache2 reload')


class Configure(Role):
    """Adds a Munin node to a server.
    """
    packages = [ 'munin-node', 'munin-plugins-extra']

    def configure(self):
        """Add the node configuration to the server, and the server
        configuration on the node.
        """
        _logger.info("Configuring node %s", self.server)
        sudo("service munin-node restart")

        with settings(host_string=self.parameter):
            _logger.info("Configuring server %s", self.parameter)
            sudo("service apache2 reload")
