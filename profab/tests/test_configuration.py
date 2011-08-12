from unittest2 import TestCase
import mock

from profab import _Configuration


class Configuration(TestCase):
    def test_load_test_config(self):
        config = _Configuration('test-client')
        self.assertEquals(config.host, 'ec2')
        self.assertEquals(config.region, 'us-east-1')
        self.assertEquals(config.keys.api, 'test-api-key')
        self.assertEquals(config.keys.secret, 'test-api-secret')


    def test_load_config(self):
        with mock.patch('profab._Configuration.load_configuration', lambda s: {
                    'host': 'ec2-eu',
                    'keys': { 'api': 'client-key', 'secret': 'client-secret'},
                    'ec2': {'s3': True},
                    'region': 'eu-west-1',
                }):
            config = _Configuration('client')
            self.assertEquals(config.host, 'ec2-eu')
            self.assertEquals(config.region, 'eu-west-1')
            self.assertEquals(config.keys.api, 'client-key')
            self.assertEquals(config.keys.secret, 'client-secret')
            self.assertEquals(config.ec2.s3, True)
