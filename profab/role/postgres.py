"""Sets up and configures Postgres on the machine
"""
from fabric.api import run, sudo
from fabric.contrib.files import sed, exists

from profab.role import Role


class AddRole(Role):
    """Adds the default Postgres configuration.
    """
    packages = ['postgresql']


    def configure(self, server):
        """Configure Postgres once it is running.
        """
        pguser = sudo('''psql -x -c "select * from pg_user '''
            '''where usename='ubuntu'"''', user='postgres')
        if 'No rows' in pguser:
            sudo('psql -c "create role ubuntu login superuser"',
                user='postgres')
            sudo('psql -c "create database ubuntu with owner=ubuntu"',
                user='postgres')
        pguser = run('''psql -x -c "select * from pg_user where '''
            '''usename='www-data'"''')
        if 'No rows' in pguser:
            run('createuser -l -S -D -I -R www-data')
            run('createdb -O www-data -E UTF-8 www-data')

        postgres_path = self.get_configuration_path('/etc/postgresql')
        sed('%s/main/pg_hba.conf' % postgres_path,
            '127.0.0.1/32', '127.0.0.1/16', use_sudo=True)
        sudo('`ls /etc/init.d/postgres*` restart')


    @staticmethod
    def get_configuration_path(postgres_path):
        """Check version of postgres is 8.4 or 9.1 .
        """
        if exists('%s/9.1' % postgres_path):
            postgres_path = '%s/9.1' % postgres_path
        elif exists('%s/8.4' % postgres_path):
            postgres_path = '%s/8.4' % postgres_path
        else:
            msg = '''[Error] Support  postgres version 8.4 and 9.1 only. '''
            raise Exception(msg)
        return postgres_path
