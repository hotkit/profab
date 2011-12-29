"""Sets up and configures Apache2 and WSGI on the machine
"""
from fabric.api import sudo
from fabric.contrib.files import exists

from profab.role import Role


class AddRole(Role):
    """Adds the default WSGI configuration.
    """
    packages = ['apache2', 'libapache2-mod-wsgi']


    def configure(self, server):
        """Configure Apache2 and WSGI once it is running.
        """
        if exists('/etc/apache2/sites-enabled/000-default'):
            sudo('a2dissite 000-default')
        sudo('service apache2 restart')

        if not exists('/home/www-data'):
            sudo('mkdir -p /home/www-data')
            sudo('chown www-data:www-data -Rv /home/www-data')
