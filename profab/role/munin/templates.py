"""Functions for generating Munin configuration files
"""
from cStringIO import StringIO


APACHE_CONFIG = """
<VirtualHost *:80>
    DocumentRoot /var/cache/munin/www
</VirtualHost>
"""

MUNIN_CONFIG = """includedir /etc/munin/munin-conf.d
"""
