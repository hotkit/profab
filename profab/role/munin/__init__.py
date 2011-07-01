"""Sets up and configures Munin on the machine
"""
from cStringIO import StringIO

from fabric.api import settings, sudo
from fabric.contrib.files import exists
from fabric.operations import put

from profab import _logger
from profab.role import Role


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

        _logger.info("Configure Apache2 for Munin")
        config_file = "/etc/apache2/sites-available/munin.conf"
        if not exists(config_file):
            config = StringIO()
            config.write("""
<VirtualHost *:80>
    DocumentRoot /var/cache/munin/www
</VirtualHost>
""")
            put(config, config_file, use_sudo=True)
            sudo('a2ensite munin.conf')
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
