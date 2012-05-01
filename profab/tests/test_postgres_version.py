import mock
from profab.role.postgres import AddRole

from unittest2 import TestCase

from profab.tests.mockboto.connection import MockConnection, regions
from profab.tests.mockfabric.connections import start_connection


class VersionPostgres(TestCase):
    """Test check postgres's version.
    """

    @mock.patch('profab.role.postgres.exists')
    @mock.patch('profab.role.postgres.sed')
    @mock.patch('profab.role.postgres.sudo', lambda s, user=None: start_connection() or '0 rows')
    def test_postgres_v9_1(self, sed, exist):
        # Arrange
        postgres_path = '/etc/postgresql'

        def side_effect(arg):
            output = {
                '/etc/postgresql/9.1': True,
                '/etc/postgresql/8.4': False,
            }
            return output[arg]

        exist.side_effect = side_effect 
        # Act
        pg_path = AddRole.get_configuration_path(postgres_path)
        # Assert
        self.assertEqual('/etc/postgresql/9.1', pg_path)

    @mock.patch('profab.role.postgres.exists')
    @mock.patch('profab.role.postgres.sed')
    @mock.patch('profab.role.postgres.sudo', lambda s, user=None: start_connection() or '0 rows')
    def test_postgres_v8_4(self, sed, exist):
        # Arrange
        postgres_path = '/etc/postgresql'

        def side_effect(arg):
            output = {
                '/etc/postgresql/9.1': False,
                '/etc/postgresql/8.4': True,
            }
            return output[arg]

        exist.side_effect = side_effect 
        # Act
        pg_path = AddRole.get_configuration_path(postgres_path)
        # Assert
        self.assertEqual('/etc/postgresql/8.4', pg_path)

    @mock.patch('profab.role.postgres.exists')
    @mock.patch('profab.role.postgres.sed')
    @mock.patch('profab.role.postgres.sudo', lambda s, user=None: start_connection() or '0 rows')
    def test_postgres_not_implemented(self, sed, exist):
        # Arrange
        postgres_path = '/etc/postgresql'

        def side_effect(arg):
            output = {
                '/etc/postgresql/9.1': False,
                '/etc/postgresql/8.4': False, 
            }
            return output[arg]

        exist.side_effect = side_effect 
        # Assert
        self.assertRaises(Exception, AddRole.get_configuration_path, postgres_path)

