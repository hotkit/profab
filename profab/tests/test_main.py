from unittest2 import TestCase

from profab.main import process_arguments


class TestArguments(TestCase):
    def test_empty(self):
        commands = process_arguments()
        self.assertEquals(commands, [])

    def test_one_command(self):
        commands = process_arguments('postgres')
        self.assertEquals(commands, [('postgres', None)])

    def test_one_configuration(self):
        commands = process_arguments('--monitor', 'localhost')
        self.assertEquals(commands, [('monitor', 'localhost')])
