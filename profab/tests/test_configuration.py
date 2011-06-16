from unittest2 import TestCase


class Configuration(TestCase):
    def test_load_config(self):
        from profab import _Configuration
        config = _Configuration('kirit')
        self.assertEquals(config.host, 'ec2')
        self.assertEquals(config.keys.api, 'test-api-key')
        self.assertEquals(config.keys.secret, 'test-api-secret')
