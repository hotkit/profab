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
        commands = process_arguments('--munin', 'localhost')
        self.assertEquals(commands, [('munin', 'localhost')])

    def test_two_command(self):
        commands = process_arguments('postgres', 'munin')
        self.assertEquals(commands, [('postgres', None), ('munin', None)])

    def test_one_command_plus_one_configuration(self):
        commands = process_arguments('postgres', '--munin', 'localhost')
        self.assertEquals(commands, [('postgres', None), ('munin', 'localhost')])

    def test_two_command_plus_one_configuration(self):
        commands = process_arguments('postgres', 'munin', '--munin', 'localhost')
        self.assertEquals(commands, [('postgres', None), ('munin', None), ('munin', 'localhost')])
