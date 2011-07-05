from unittest2 import TestCase
import mock

from profab import _Keys
from profab.authentication import get_private_key_filename
from profab.tests.mockboto.connection import MockConnection


class Keys(TestCase):
    def test_key_filename(self):
        config = _Keys(client='test-client--test_key_filename')
        cnx = MockConnection('key', 'secret')
        with mock.patch('socket.gethostname', lambda: 'test-host'):
            dir_made = []
            with mock.patch('os.mkdir', lambda p: dir_made.append(p)):
                filename = get_private_key_filename(config, cnx)
            self.assertTrue(dir_made)

    def test_key_filename_makes_new_key(self):
        config = _Keys(client='test-client--test_key_filename')
        cnx = MockConnection('key', 'secret')
        cnx._key_pairs.append(_Keys(name='another-host'))
        with mock.patch('socket.gethostname', lambda: 'test-host'):
            dir_made = []
            with mock.patch('os.mkdir', lambda p: dir_made.append(p)):
                filename = get_private_key_filename(config, cnx)
                self.assertTrue(dir_made)
                self.assertIn('test-host', cnx._key_pairs_created)
                cnx._key_pairs_created = []
                filename = get_private_key_filename(config, cnx)
                self.assertNotIn('test-host', cnx._key_pairs_created)
