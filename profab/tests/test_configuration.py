from unittest2 import TestCase


class Configuration(TestCase):
    def test_load_config(self):
        from profab import _Configuration
        config = _Configuration('kirit')
