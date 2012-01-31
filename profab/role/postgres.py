"""Sets up and configures Postgres on the machine
"""
from fabric.api import run, sudo
from fabric.contrib.files import sed

from profab.role import Role


class AddRole(Role):
    """Adds the default Postgres configuration.
    """
    packages = ['postgresql']


    def configure(self, server):
        """Configure Postgres once it is running.
        """
        pguser = sudo('''psql -c "select * from pg_user '''
            '''where usename='ubuntu'"''', user='postgres')
        if '0 rows' in pguser:
            sudo('psql -c "create role ubuntu login superuser"',
                user='postgres')
            sudo('psql -c "create database ubuntu with owner=ubuntu"',
                user='postgres')
        pguser = run('''psql -x -c "select * from pg_user where '''
            '''usename='www-data'"''')
        if 'No rows' in pguser:
            run('createuser -l -S -D -I -R www-data')
            run('createdb -O www-data -E UTF-8 www-data')

        sed('/etc/postgresql/8.4/main/pg_hba.conf',
            '127.0.0.1/32', '127.0.0.1/16', use_sudo=True)
        sudo('`ls /etc/init.d/postgres*` restart')
